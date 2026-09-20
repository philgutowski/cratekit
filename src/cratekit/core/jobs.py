"""The job engine: resumable, interruptible, observable long work, with no daemon.

KTD8 in one sentence: a SQLite database in write-ahead-log mode is the single
source of truth, and one driver per job is enforced by a lock whose staleness is
decided by holder liveness rather than by a timeout. Everything else here follows
from a defect in the source system that this module is built not to inherit.

**Why status is a cause and not an exit code (KTD25).** The source supervisor
writes ``status = "succeeded" if code == 0 else "failed"``. That single line
collapses the whole failure space at the one boundary where it is most expensive
to lose, and the real reason then has to be smuggled back through a side channel.
A job here records a ``Cause``, so a throttled provider and a missing
acknowledgment are both ``blocked`` and are still two different things with two
different fixes.

**Why the engine spawns a subprocess (KTD26).** In-process handlers would make
this module import every feature module, walking around the lazy-import stubs
that keep the help screen cheap on a slim install: help stays clean while running
a job crashes on a dependency nobody installed. A subprocess also preserves the
detached, reattachable, disk-truth model the source supervisor already proves.

**Why durability is not inherited for free.** Neither state writer in the source
flushes before replacing. An atomic rename guarantees that a reader sees the old
file or the new one; it guarantees nothing about either having reached the
device. ``commit_artifact`` closes that, and the ORDER it enforces is the point:
the artifact is durable BEFORE the row that claims it flips to done, so a kill in
the gap costs one item and can never produce a false success.

**Why a total failure raises.** Recorded in the source repository as a real
incident: a phase where every lookup failed returned an empty list, downstream
read that as "nothing new", and a playlist was marked fully downloaded with zero
tracks in it. Empty means "verified empty" only when the lookups succeeded.

Layer note: INFRASTRUCTURE. It reads configuration and touches the disk, and it
names no verb: the command line a job re-invokes is built by the CLI layer and
handed in, because a verb string down here is the KTD23 violation this repository
fails the build for.
"""

from __future__ import annotations

import json
import os
import signal
import sqlite3
import subprocess
import sys
import tomllib
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterator, Mapping, Sequence

from cratekit.cli.output import new_run_id, timestamp
from cratekit.core import config
from cratekit.core.cause import (
    Cause,
    CratekitError,
    JobBlocked,
    JobCancelled,
    Remediation,
    Scope,
    name_the_database,
    refuse,
)
from cratekit.core.exit_codes import Remedy

#: The queue's own schema version. A cross-version resume REFUSES rather than
#: guessing: the source system versions exactly one of its twenty-one state
#: files, and every unversioned one is a file that cannot be migrated without
#: reverse-engineering whatever wrote it.
SCHEMA_VERSION = 1

#: The database inside the declared ``job_queue`` state directory. The DIRECTORY
#: is the declared entry, not this file, because the queue keeps a lock and a log
#: per job beside the database and all of them belong to the same root.
QUEUE_FILENAME = "queue.db"


class JobState(StrEnum):
    """Where a job is. ``blocked`` always carries a cause saying why.

    ``cancelled`` is a first-class state rather than a flavour of failed. The
    source registry derives status from an exit code alone, so a job the user
    stopped on purpose is indistinguishable from one that broke, and R22 names
    that distinction explicitly.
    """

    QUEUED = "queued"
    RUNNING = "running"
    BLOCKED = "blocked"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ItemState(StrEnum):
    """Where one unit of work inside a job is.

    ``claimed`` exists so a kill between claiming and finishing is recoverable.
    Without it a driver would have to choose between redoing everything and
    trusting that whatever it started got finished.
    """

    PENDING = "pending"
    CLAIMED = "claimed"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


#: States from which nothing moves. Re-driving one is a defect rather than a
#: retry: a terminal state is a recorded answer about work that already happened.
TERMINAL_STATES: frozenset[JobState] = frozenset(
    {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
)

#: The forward-only edges between OPEN states. Any open state may additionally
#: jump straight to a terminal state, which is the source system's own shape and
#: is what lets a cancel land from anywhere. The single backward edge in the
#: engine is ``reopen``, and it is a named function rather than a table entry so
#: that rewinding a job is always a deliberate, greppable act.
_FORWARD: Mapping[JobState, tuple[JobState, ...]] = MappingProxyType(
    {
        JobState.QUEUED: (JobState.RUNNING, JobState.BLOCKED),
        JobState.RUNNING: (JobState.BLOCKED,),
        JobState.BLOCKED: (JobState.QUEUED, JobState.RUNNING),
        JobState.SUCCEEDED: (),
        JobState.FAILED: (),
        JobState.CANCELLED: (),
    }
)


# ---------------------------------------------------------------------------
# The records
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Job:
    """One queued piece of long work, and everything a resume needs to redo it.

    ``payload`` and ``config_toml`` are FROZEN AT QUEUE TIME (KTD9). The recorded
    bug this closes: a base export re-resolved on resume, found a different file
    than the one the run was planned against, and could empty the output. A job
    that re-reads live configuration is a job whose inputs change under it while
    it waits in the queue.

    ``library_id`` is stored because the queue is installation-scoped while a
    library is per configuration. A queue drained after the user reconfigures
    would otherwise run against a volume nobody chose.
    """

    job_id: str
    handler_key: str
    payload: Mapping[str, Any]
    config_fingerprint: str
    config_toml: str
    library_id: str
    state: JobState
    created: str
    updated: str
    stage: str | None = None
    cause: Cause | None = None
    attempts: int = 0
    pid: int | None = None

    def is_open(self) -> bool:
        return self.state not in TERMINAL_STATES


@dataclass(frozen=True, slots=True)
class Item:
    """One claimable unit inside a job.

    ``item_id`` is a stable identifier supplied by whatever queued the job, never
    a display name (R19). ``ordinal`` fixes the claim order so a resumed run
    walks the same sequence, which is what makes "exactly one item reprocessed" a
    checkable property rather than a hope.
    """

    job_id: str
    item_id: str
    ordinal: int
    state: ItemState
    artifact: str | None = None
    claimed_by: str | None = None
    cause: Cause | None = None


@dataclass(frozen=True, slots=True)
class Produced:
    """What one item's handler produced, before it is durable.

    Two paths rather than one, because the durability rule needs both: the staged
    file is what was written, the final path is where it belongs, and the engine
    owns the flush-then-rename between them. A handler that renamed the file
    itself would have taken the ordering decision this module exists to enforce.
    """

    staged: Path | None = None
    final: Path | None = None


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

_SCHEMA = (
    "CREATE TABLE IF NOT EXISTS queue_schema (version INTEGER NOT NULL)",
    """
    CREATE TABLE IF NOT EXISTS jobs (
        job_id             TEXT PRIMARY KEY,
        handler_key        TEXT NOT NULL,
        payload            TEXT NOT NULL,
        config_fingerprint TEXT NOT NULL,
        config_toml        TEXT NOT NULL,
        library_id         TEXT NOT NULL,
        state              TEXT NOT NULL,
        stage              TEXT,
        cause              TEXT,
        attempts           INTEGER NOT NULL DEFAULT 0,
        pid                INTEGER,
        created            TEXT NOT NULL,
        updated            TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS job_items (
        job_id     TEXT NOT NULL,
        item_id    TEXT NOT NULL,
        ordinal    INTEGER NOT NULL,
        state      TEXT NOT NULL,
        artifact   TEXT,
        claimed_by TEXT,
        claimed_at TEXT,
        cause      TEXT,
        PRIMARY KEY (job_id, item_id)
    )
    """,
    "CREATE INDEX IF NOT EXISTS job_items_claim ON job_items (job_id, state, ordinal)",
)


def _own_only(path: Path) -> None:
    """Force owner-only permissions on one file, tolerating absence.

    Everything in the queue directory that Cratekit writes THROUGH its own writer
    already lands at an explicit mode. These are the ones written by somebody
    else: SQLite creates the database and its sidecars, and the operating system
    creates a job's log when the child's output is redirected into it. All of them
    inherit the umask, and under a permissive umask that is a world-readable queue
    holding every job's frozen configuration.

    Absence is normal rather than exceptional: a database with no uncheckpointed
    transactions legitimately has no log beside it.
    """
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    try:
        os.chmod(path, config.PRIVATE_FILE_MODE)
    except OSError:
        pass


def _make_private(path: Path) -> None:
    """The database AND its sidecars, because the log is where the data actually is.

    The suffixes come from the config module's declared set rather than from a
    pair of literals here. That set exists precisely so nobody keeps a second copy
    of it, and a copy that forgets the write-ahead log is a copy that leaves the
    queue's real contents unprotected until the next checkpoint.
    """
    _own_only(path)
    for sidecar in config.SQLITE_SIDECARS:
        _own_only(path.with_name(path.name + sidecar.suffix))


class JobStore:
    """The connection to the queue, and the one place its pragmas are decided.

    ``synchronous=FULL`` rather than the write-ahead log's default of NORMAL.
    NORMAL lets a commit be lost on a power cut, and the commit that matters here
    is the one flipping an item to done AFTER its artifact is durable. Losing that
    ordering re-opens exactly the window ``commit_artifact`` exists to close, and
    a job queue is not hot enough for the difference to be worth measuring.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        # isolation_level=None turns OFF the driver's implicit transaction
        # management, which is what makes BEGIN IMMEDIATE below the real thing.
        # Left on, the driver opens a DEFERRED transaction that takes its write
        # lock at the first WRITE, which is after the SELECT that chose the item,
        # and that gap is precisely how two drivers claim the same item.
        #
        # THE DRIVER'S ERROR CARRIES NO PATH AND NO ERRNO, so the whole opening
        # sequence is named. A queue file this account cannot open raises
        # ``sqlite3.OperationalError("unable to open database file")``, which is
        # not an ``OSError``: no errno, no filename, no ``__cause__``. Every
        # errno-shaped classification in the package was blind to it, and the
        # verb exited "this is a defect; report it" over a chmod on the file this
        # program keeps its own state in. The pragmas are inside the same block
        # because a database on a read only volume connects and then refuses the
        # write-ahead-log pragma with SQLITE_READONLY.
        #
        # It records the path on the SAME exception and re-raises it untouched,
        # so the traceback, the class and every existing catcher are unaffected.
        try:
            self.conn = sqlite3.connect(str(path), isolation_level=None, timeout=30.0)
            self.conn.row_factory = sqlite3.Row
            # The mode goes on BEFORE the write-ahead-log pragma, because SQLite
            # gives the log and shared-memory files the permissions the database
            # file has when it creates them. Doing it afterwards would leave two
            # umask-moded sidecars beside a correctly moded database, which is
            # the "file mode without the directory mode" defect one level along:
            # the queue's real contents live in the log until a checkpoint.
            _make_private(path)
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.execute("PRAGMA synchronous=FULL")
            # A concurrent writer holds the database for one small transaction,
            # so waiting is right and failing immediately is not. The busy
            # timeout is the difference between two processes serializing and one
            # of them raising "database is locked" at the user.
            self.conn.execute("PRAGMA busy_timeout=30000")
        except sqlite3.Error as exc:
            name_the_database(exc, path)
            raise

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> JobStore:
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    @contextmanager
    def immediate(self) -> Iterator[sqlite3.Connection]:
        """A transaction that takes the write lock UP FRONT.

        KTD8 says items are claimed in an immediate transaction, and this is why:
        a read-then-write under a deferred transaction lets two drivers both read
        the same pending row before either writes, and SQLite resolves that by
        failing one of them at COMMIT, after the work has already been decided.
        """
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield self.conn
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        self.conn.execute("COMMIT")


def store_dir(cfg: config.Config | None = None) -> Path:
    """The declared job-queue directory. Resolved through U2, never composed here.

    U2 owns where state lives. Composing a path in this module would be a second
    opinion about a decision that has already been made and written down, which is
    how the source system ended up with two different directories both meaning
    local state.
    """
    return config.state_path("job_queue", cfg)


def queue_path(cfg: config.Config | None = None) -> Path:
    return store_dir(cfg) / QUEUE_FILENAME


def open_store(path: Path | None = None) -> JobStore:
    """Open, and create if needed, the queue. Directory mode included.

    The directory is created through the config module's private-directory helper
    rather than through ``Path.mkdir``. That is deliberate reuse, not convenience:
    a 0600 file inside a 0777 directory is not private, because unlink and rename
    are governed by the DIRECTORY's mode, and a second careful implementation here
    is the copy that later drifts. See ``config._mkdir_private`` for why the
    obvious ``mode=`` argument does not fix it.
    """
    resolved = path or queue_path()
    config._mkdir_private(resolved.parent)
    store = JobStore(resolved)
    _initialize(store)
    return store


def _initialize(store: JobStore) -> None:
    for statement in _SCHEMA:
        store.conn.execute(statement)
    row = store.conn.execute("SELECT version FROM queue_schema").fetchone()
    if row is None:
        store.conn.execute("INSERT INTO queue_schema (version) VALUES (?)", (SCHEMA_VERSION,))
        return
    found = int(row["version"])
    if found != SCHEMA_VERSION:
        raise refuse(
            "job-schema-mismatch",
            f"the job queue was written at schema {found} and this build speaks "
            f"{SCHEMA_VERSION}; a cross-version resume refuses rather than guessing "
            f"what the other version meant by a row",
            steps=(
                "finish or cancel the jobs the other version queued, then let this "
                "one start a fresh queue",
            ),
            scope=Scope.RUN,
            origin=("jobs",),
            detail={"found": found, "expected": SCHEMA_VERSION},
        )


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def _cause_from_text(text: str | None) -> Cause | None:
    """Read a stored cause, degrading an unreadable one into a visible failure.

    Returning None would be wrong in a way that matters: None is what a SUCCESS
    looks like, so an unparseable cause would erase the evidence that something
    went wrong at all.
    """
    if not text:
        return None
    try:
        return Cause.from_json(json.loads(text))
    except (ValueError, KeyError, TypeError):
        return Cause(
            reason="no-evidence",
            message="a stored cause could not be read back",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=("jobs",),
        )


def _coerce_job_state(raw: str) -> JobState:
    """Read a state string, degrading an unrecognized one into an OPEN state.

    Ported from the source system's ``_coerce``: a malformed record degrades
    rather than raising. The DIRECTION is the load-bearing half. An unknown state
    becomes ``queued``, never a terminal one, because the item ledger already
    prevents duplicate work on a re-drive, while a record that coerced to
    ``succeeded`` would be a false success nothing downstream can detect.
    """
    try:
        return JobState(raw)
    except ValueError:
        return JobState.QUEUED


def _coerce_item_state(raw: str) -> ItemState:
    """The same rule one level down: unknown means not yet done."""
    try:
        return ItemState(raw)
    except ValueError:
        return ItemState.PENDING


def _job_from_row(row: sqlite3.Row) -> Job:
    try:
        payload = json.loads(row["payload"])
    except ValueError:
        payload = {}
    return Job(
        job_id=row["job_id"],
        handler_key=row["handler_key"],
        payload=payload if isinstance(payload, dict) else {},
        config_fingerprint=row["config_fingerprint"],
        config_toml=row["config_toml"],
        library_id=row["library_id"],
        state=_coerce_job_state(row["state"]),
        created=row["created"],
        updated=row["updated"],
        stage=row["stage"],
        cause=_cause_from_text(row["cause"]),
        attempts=int(row["attempts"] or 0),
        pid=row["pid"],
    )


def _item_from_row(row: sqlite3.Row) -> Item:
    return Item(
        job_id=row["job_id"],
        item_id=row["item_id"],
        ordinal=int(row["ordinal"]),
        state=_coerce_item_state(row["state"]),
        artifact=row["artifact"],
        claimed_by=row["claimed_by"],
        cause=_cause_from_text(row["cause"]),
    )


def get(store: JobStore, job_id: str) -> Job:
    """One job, or refuse naming the identifier that did not resolve."""
    row = store.conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None:
        raise refuse(
            "job-unknown",
            f"no job in this installation's queue has the identifier {job_id!r}",
            steps=("check the identifier against the jobs this installation has queued",),
            scope=Scope.RUN,
            origin=("jobs",),
            detail={"job_id": job_id},
        )
    return _job_from_row(row)


def list_jobs(store: JobStore, *, states: Sequence[JobState] | None = None) -> tuple[Job, ...]:
    """Every job, newest first, optionally filtered to a set of states."""
    if states:
        placeholders = ", ".join("?" for _ in states)
        rows = store.conn.execute(
            f"SELECT * FROM jobs WHERE state IN ({placeholders}) ORDER BY created DESC",
            tuple(str(state) for state in states),
        ).fetchall()
    else:
        rows = store.conn.execute("SELECT * FROM jobs ORDER BY created DESC").fetchall()
    return tuple(_job_from_row(row) for row in rows)


#: How many identifiers go into one ``IN`` clause. SQLite's compiled parameter
#: limit is the floor this respects, and the caller that needs chunking at all is
#: the one sweeping a staging tree that has never been swept, which is exactly the
#: state that produces thousands of names at once.
_ID_CHUNK = 500


def states_of(store: JobStore, job_ids: Sequence[str]) -> dict[str, JobState]:
    """Where each named job got to, leaving out the names this queue does not hold.

    TWO COLUMNS, WHICH IS THE POINT OF IT EXISTING beside ``get`` and
    ``list_jobs``. Both of those hydrate a whole :class:`Job`, so both JSON
    decode the payload and carry the frozen configuration TOML of every row they
    touch. A caller that only wants to know where a job got to pays for all of
    it: measured 2026-09-20 over a store of succeeded download jobs each
    freezing a two hundred track list, ``list_jobs`` filtered to the terminal
    states took a median 54 ms at 500 jobs and 224 ms at 2000, and the store
    grows about 16 kB per job. Answering from ``job_id`` and ``state`` alone is
    flat in the payload size.

    AN IDENTIFIER WITH NO ROW IS ABSENT FROM THE RESULT rather than mapped to
    anything. "This queue has never heard of it" is not a state a job can be in,
    and folding it into one would take the difference away from the caller that
    needs to act on it.
    """
    found: dict[str, JobState] = {}
    wanted = list(job_ids)
    for start in range(0, len(wanted), _ID_CHUNK):
        chunk = wanted[start : start + _ID_CHUNK]
        placeholders = ", ".join("?" for _ in chunk)
        rows = store.conn.execute(
            f"SELECT job_id, state FROM jobs WHERE job_id IN ({placeholders})", tuple(chunk)
        ).fetchall()
        found.update({row["job_id"]: _coerce_job_state(row["state"]) for row in rows})
    return found


def items(store: JobStore, job_id: str) -> tuple[Item, ...]:
    rows = store.conn.execute(
        "SELECT * FROM job_items WHERE job_id = ? ORDER BY ordinal", (job_id,)
    ).fetchall()
    return tuple(_item_from_row(row) for row in rows)


def progress(store: JobStore, job_id: str) -> dict[str, Any]:
    """Counts per item state, plus the totals a progress display needs.

    Derived by GROUPING the ledger rather than by keeping counters on the job row.
    A counter and the rows it counts can disagree after a crash; a query cannot.
    """
    rows = store.conn.execute(
        "SELECT state, COUNT(*) AS n FROM job_items WHERE job_id = ? GROUP BY state",
        (job_id,),
    ).fetchall()
    counts = {str(state): 0 for state in ItemState}
    for row in rows:
        counts[str(_coerce_item_state(row["state"]))] += int(row["n"])
    total = sum(counts.values())
    settled = (
        counts[str(ItemState.DONE)]
        + counts[str(ItemState.FAILED)]
        + counts[str(ItemState.SKIPPED)]
    )
    return {"total": total, "settled": settled, "counts": counts}


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def enqueue(
    store: JobStore,
    *,
    handler_key: str,
    payload: Mapping[str, Any],
    cfg: config.Config,
    item_ids: Sequence[str] = (),
    job_id: str | None = None,
) -> Job:
    """Queue a job, freezing the configuration it will run against (KTD9).

    The WHOLE configuration is frozen, not the handful of keys a handler happens
    to read today. A frozen subset means the next person who reads one more key
    silently un-freezes it, and nothing fails until a resume produces the wrong
    answer months later.
    """
    now = timestamp()
    identifier = job_id or new_run_id()
    with store.immediate() as conn:
        conn.execute(
            "INSERT INTO jobs (job_id, handler_key, payload, config_fingerprint, "
            "config_toml, library_id, state, stage, cause, attempts, pid, created, "
            "updated) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, 0, NULL, ?, ?)",
            (
                identifier,
                handler_key,
                json.dumps(dict(payload), sort_keys=True),
                cfg.fingerprint(),
                cfg.to_toml_bytes().decode("utf-8"),
                cfg.library.volume_id,
                str(JobState.QUEUED),
                now,
                now,
            ),
        )
        for ordinal, item_id in enumerate(item_ids):
            conn.execute(
                "INSERT INTO job_items (job_id, item_id, ordinal, state) VALUES (?, ?, ?, ?)",
                (identifier, str(item_id), ordinal, str(ItemState.PENDING)),
            )
    return get(store, identifier)


def _touch(conn: sqlite3.Connection, job_id: str, **columns: Any) -> None:
    """Update job columns, always moving ``updated`` with them.

    One writer for every job-row change, so the timestamp cannot be forgotten at
    one call site and present at the others, which is how a status display starts
    reporting that a running job has been idle for an hour.
    """
    columns["updated"] = timestamp()
    assignments = ", ".join(f"{name} = ?" for name in columns)
    conn.execute(
        f"UPDATE jobs SET {assignments} WHERE job_id = ?", (*columns.values(), job_id)
    )


def transition(
    store: JobStore,
    job_id: str,
    state: JobState,
    *,
    cause: Cause | None = None,
    stage: str | None = None,
) -> Job:
    """Move a job forward, refusing an edge the state machine does not declare.

    ``blocked`` REQUIRES a cause, and the check is here rather than in each
    caller's head. A job parked with no reason is the source supervisor again:
    the status says something stopped, and the remediation lives in a log file
    somebody has to go and read.
    """
    current = get(store, job_id)
    if state is not current.state:
        jump_to_terminal = state in TERMINAL_STATES and current.is_open()
        if not jump_to_terminal and state not in _FORWARD[current.state]:
            raise refuse(
                "internal-error",
                f"job {job_id} cannot move from {current.state} to {state}; "
                f"transitions are forward-only and a terminal state is an answer, "
                f"not a step",
                remedy=Remedy.REPORT_DEFECT,
                origin=("jobs",),
                detail={"job_id": job_id, "from": str(current.state), "to": str(state)},
            )
    if state is JobState.BLOCKED and cause is None:
        raise refuse(
            "internal-error",
            f"job {job_id} was parked with no cause; a throttled provider and a "
            f"missing acknowledgment are both blocked and need different fixes",
            remedy=Remedy.REPORT_DEFECT,
            origin=("jobs",),
            detail={"job_id": job_id},
        )
    with store.immediate() as conn:
        _touch(
            conn,
            job_id,
            state=str(state),
            cause=json.dumps(cause.to_json()) if cause is not None else None,
            stage=stage if stage is not None else current.stage,
        )
    return get(store, job_id)


def reopen(store: JobStore, job_id: str, *, stage: str | None = None) -> Job:
    """The one backward edge: a job whose driver died goes back to queued.

    Named rather than being an entry in the transition table, so rewinding is
    always a deliberate act somebody can find. The source system's equivalent is
    ``force_state`` and its rationale holds here: a resume re-enters a stage
    whole, and the frozen inputs make that safe because the item ledger already
    records what is finished.
    """
    current = get(store, job_id)
    if not current.is_open():
        raise refuse(
            "internal-error",
            f"job {job_id} is {current.state} and a terminal state is never reopened",
            remedy=Remedy.REPORT_DEFECT,
            origin=("jobs",),
            detail={"job_id": job_id, "state": str(current.state)},
        )
    with store.immediate() as conn:
        _touch(
            conn,
            job_id,
            state=str(JobState.QUEUED),
            stage=stage if stage is not None else current.stage,
            pid=None,
        )
    return get(store, job_id)


def retry(store: JobStore, job_id: str) -> Job:
    """Re-open a job that ended CANCELLED or FAILED, and re-arm its failed items.

    The other deliberate reversal, and it is narrower than ``reopen``. A cancelled
    job is one a person stopped and may want back; a failed one is one whose
    failures may have been transient. A SUCCEEDED job is neither, and re-opening
    it would overwrite a recorded answer with a fresh attempt at nothing, since
    every item is already done.

    Items that are DONE stay done. That is the whole promise of a resume: R22 says
    completed work is not repeated, and "completed" means the item's artifact is
    durable, never that the job as a whole ended tidily.
    """
    current = get(store, job_id)
    if current.state is JobState.SUCCEEDED:
        raise refuse(
            "internal-error",
            f"job {job_id} succeeded; there is nothing left in it to resume",
            remedy=Remedy.REPORT_DEFECT,
            origin=("jobs",),
            detail={"job_id": job_id, "state": str(current.state)},
        )
    if current.is_open():
        return current
    with store.immediate() as conn:
        conn.execute(
            "UPDATE job_items SET state = ?, cause = NULL, claimed_by = NULL "
            "WHERE job_id = ? AND state IN (?, ?)",
            (
                str(ItemState.PENDING),
                job_id,
                str(ItemState.FAILED),
                str(ItemState.CLAIMED),
            ),
        )
        _touch(conn, job_id, state=str(JobState.QUEUED), cause=None, pid=None)
    return get(store, job_id)


def block(store: JobStore, job_id: str, cause: Cause) -> Job:
    """Park a job with the reason it is parked.

    A thin wrapper, and it exists to make the requirement callable: R22's
    ``blocked`` is one state covering several situations, and the cause is what
    tells a throttled provider apart from a gate nobody has answered.
    """
    return transition(store, job_id, JobState.BLOCKED, cause=cause)


def raise_for_state(job: Job) -> None:
    """Refuse for a job that did not end cleanly. THE ONE MAPPING every shell uses.

    A queued verb's resume drives the job and then reports it, and a report is a
    normal envelope the dispatcher exits 0 over. Two endings must never reach it:

    * ``blocked``, a run a worker PARKED. It raises :class:`JobBlocked`, which the
      dispatcher reads as ``Outcome.BLOCKED``. A blocked job is OPEN, so the
      predicate below never saw it, and thirteen shells reported ``ok`` over a
      provider that had just refused the client (R-290).
    * any CLOSED job carrying a cause, ``failed`` or ``cancelled``. ``drive``
      raises only when EVERY attempted item failed, so a job where one item
      completed and another did not returns normally, recorded failed (R-225).
      Cancelled is included deliberately: a run stopped with a signal left work
      undone. It raises :class:`JobCancelled`, which the dispatcher reads as
      ``Outcome.CANCELLED``, so a person who stopped a run is not told it broke.
      ``succeeded`` carries no cause and is not reached.

    CALL IT OUTSIDE THE ``is_open`` BRANCH THAT DRIVES. A job already failed on
    entry is not open, so the drive is skipped, and a check inside that branch is
    skipped with it: the second ask about a half failed job then exits 0 for ever.
    ``backup`` paid for that placement first.

    THE JOB'S OWN CAUSE IS RE-RAISED, never reworded. It already carries the
    counts, the retryable flag that follows the items (R-380), the remedy those
    items earned and the failing item's cause nested inside it, and a second
    wording for one condition is how two surfaces come to disagree about it.

    WHY ONE FUNCTION. The predicate was copied into ten shells by hand and
    forgotten in three, and no copy could have known about a state added after it
    was written. ``tests/test_job_outcome.py`` refuses a shell that drives without
    calling this, and refuses a hand rolled copy.
    """
    if job.state is JobState.BLOCKED:
        # ``transition`` refuses to park a job without a cause, so a blocked row
        # with none was written by something other than this engine. It is still
        # not a success, and the refusal says what is actually known.
        #
        # STILL AS THE BLOCKED TYPE. The first version raised the plain refusal,
        # and the envelope then said ``failed`` over a row ``job show`` calls
        # blocked, the disagreement this function exists to remove.
        if job.cause is None:
            raise JobBlocked(
                refuse(
                    "internal-error",
                    f"job {job.job_id} is blocked and records no reason for it",
                    remedy=Remedy.REPORT_DEFECT,
                    origin=("jobs",),
                    detail={"job_id": job.job_id, "state": str(job.state)},
                ).cause
            )
        raise JobBlocked(job.cause)
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
            raise JobCancelled(job.cause)
        raise CratekitError(job.cause)


def cancel(store: JobStore, job_id: str, *, stage: str | None = None) -> Job:
    """Stop a job and record it as CANCELLED, which is not FAILED (R22).

    The distinction is the requirement. Deriving it from an exit code, which is
    what the source registry does, makes a job the user stopped look identical to
    one that broke, and the two want opposite things from whoever reads the list.
    """
    current = get(store, job_id)
    if not current.is_open():
        return current
    where = stage if stage is not None else current.stage
    return transition(
        store,
        job_id,
        JobState.CANCELLED,
        stage=where,
        cause=Cause(
            reason="cancelled",
            message=(
                f"job {job_id} was cancelled" + (f" at stage {where!r}" if where else "")
            ),
            remediation=Remediation(remedy=Remedy.RESUME_JOB),
            scope=Scope.RUN,
            retryable=True,
            origin=("jobs",),
            detail={"job_id": job_id, "stage": where},
        ),
    )


# ---------------------------------------------------------------------------
# Claiming, and the durability rule
# ---------------------------------------------------------------------------


def claim(store: JobStore, job_id: str, driver: str) -> Item | None:
    """Take the next pending item, or None when there is nothing left.

    The SELECT and the UPDATE are inside ONE immediate transaction. Splitting them
    is the classic double claim: two drivers read the same lowest pending ordinal,
    both write, and the second write silently wins.
    """
    with store.immediate() as conn:
        row = conn.execute(
            "SELECT item_id FROM job_items WHERE job_id = ? AND state = ? "
            "ORDER BY ordinal LIMIT 1",
            (job_id, str(ItemState.PENDING)),
        ).fetchone()
        if row is None:
            return None
        conn.execute(
            "UPDATE job_items SET state = ?, claimed_by = ?, claimed_at = ? "
            "WHERE job_id = ? AND item_id = ?",
            (str(ItemState.CLAIMED), driver, timestamp(), job_id, row["item_id"]),
        )
        claimed = conn.execute(
            "SELECT * FROM job_items WHERE job_id = ? AND item_id = ?",
            (job_id, row["item_id"]),
        ).fetchone()
    return _item_from_row(claimed)


def _fsync_directory(path: Path) -> None:
    """Flush a directory entry, so a rename survives a power cut.

    Renaming a file atomically updates the DIRECTORY, and an unflushed directory
    loses that update exactly as an unflushed file loses its contents. Guarded
    because a directory is not openable on every platform, and a portability
    failure here would be worse than the durability gap it closes (R1).
    """
    try:
        fd = os.open(str(path), os.O_RDONLY)
    except OSError:  # pragma: no cover - platform dependent
        return
    try:
        os.fsync(fd)
    except OSError:  # pragma: no cover - platform dependent
        pass
    finally:
        os.close(fd)


def commit_artifact(staged: Path, final: Path) -> Path:
    """Make a staged file durable AND put it in place, in that order.

    Three steps, and the order is the contract KTD8 states:

    1. flush the staged file's contents to the device,
    2. rename it into place, which is atomic within one filesystem,
    3. flush the directory, so the rename itself is durable.

    Only after this returns may the item's row flip to done. A row that flips
    first and a machine that dies second leaves a job claiming an artifact that
    does not exist, and that is a false success no later run can detect, because
    "done" is exactly what a resume trusts.
    """
    config._mkdir_private(final.parent)
    with open(staged, "rb+") as handle:
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(staged, final)
    _fsync_directory(final.parent)
    return final


def complete_item(
    store: JobStore, job_id: str, item_id: str, *, artifact: Path | str | None = None
) -> None:
    """Flip one item to done. Call this only AFTER ``commit_artifact`` returned."""
    with store.immediate() as conn:
        conn.execute(
            "UPDATE job_items SET state = ?, artifact = ?, claimed_by = NULL "
            "WHERE job_id = ? AND item_id = ?",
            (str(ItemState.DONE), str(artifact) if artifact else None, job_id, item_id),
        )


def fail_item(store: JobStore, job_id: str, item_id: str, cause: Cause) -> None:
    with store.immediate() as conn:
        conn.execute(
            "UPDATE job_items SET state = ?, cause = ?, claimed_by = NULL "
            "WHERE job_id = ? AND item_id = ?",
            (str(ItemState.FAILED), json.dumps(cause.to_json()), job_id, item_id),
        )


def release_claims(store: JobStore, job_id: str, *, driver: str | None = None) -> int:
    """Return orphaned claims to pending, and say how many there were.

    Called when a job is re-driven after its previous driver died. A claimed item
    was started and not finished, so it is redone: that is the "exactly one item
    reprocessed" cost of a kill, and it is bounded by design because everything
    already flipped to done stays done.
    """
    with store.immediate() as conn:
        if driver is None:
            cursor = conn.execute(
                "UPDATE job_items SET state = ?, claimed_by = NULL "
                "WHERE job_id = ? AND state = ?",
                (str(ItemState.PENDING), job_id, str(ItemState.CLAIMED)),
            )
        else:
            cursor = conn.execute(
                "UPDATE job_items SET state = ?, claimed_by = NULL "
                "WHERE job_id = ? AND state = ? AND claimed_by = ?",
                (str(ItemState.PENDING), job_id, str(ItemState.CLAIMED), driver),
            )
        return int(cursor.rowcount or 0)


# ---------------------------------------------------------------------------
# The frozen configuration, and drift
# ---------------------------------------------------------------------------


def frozen_config(job: Job) -> config.Config:
    """The configuration this job was QUEUED against, rebuilt from its own bytes."""
    return config.from_dict(tomllib.loads(job.config_toml))


def _flatten(data: Mapping[str, Any], prefix: str = "") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in data.items():
        dotted = f"{prefix}{key}"
        if isinstance(value, Mapping):
            flat.update(_flatten(value, f"{dotted}."))
        else:
            flat[dotted] = value
    return flat


def drift(job: Job, current: config.Config) -> tuple[str, ...]:
    """The dotted keys that changed since this job was queued (KTD9).

    It NAMES them rather than refusing. The requirement is that a job runs against
    its frozen inputs and reports what moved, because a user is entitled to know
    that the run they are watching is not using the setting they just edited.
    Refusing instead would make every configuration edit cancel the queue.

    The fingerprint is checked first because it is one hash comparison and the
    common answer is "nothing moved"; the per-key diff only runs when something
    actually did.
    """
    if job.config_fingerprint == current.fingerprint():
        return ()
    before = _flatten(tomllib.loads(job.config_toml))
    after = _flatten(current.to_toml_dict())
    return tuple(
        sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
    )


# ---------------------------------------------------------------------------
# One driver per job
# ---------------------------------------------------------------------------


def lock_path(job_id: str, *, root: Path | None = None) -> Path:
    return (root or store_dir()) / f"{job_id}.lock"


class DriverHeld(CratekitError):
    """Another driver is alive and holding this job."""


def _held_cause(job_id: str, holder_text: str, path: Path) -> Cause:
    try:
        holder = json.loads(holder_text)
        who = f"pid {holder.get('pid')}, since {holder.get('acquired')}"
    except (ValueError, TypeError, AttributeError):
        who = "holder unknown"
    return Cause(
        reason="job-driver-held",
        message=(
            f"another driver is running job {job_id} ({who}); one driver per job, "
            f"and a live one is never evicted"
        ),
        remediation=Remediation(remedy=Remedy.WAIT_FOR_HOLDER),
        scope=Scope.RUN,
        retryable=True,
        origin=("jobs",),
        detail={"job_id": job_id, "lock": str(path)},
    )


@contextmanager
def driver_lock(job_id: str, *, root: Path | None = None) -> Iterator[Path]:
    """Hold the one-driver-per-job lock, or refuse naming the live holder.

    Staleness is decided by HOLDER LIVENESS, never by a timeout, and the mechanism
    is the reason: the kernel releases an advisory lock when the holder's process
    dies, so a crashed driver's lock is already gone and a slow one's is not. A
    timeout cannot tell those apart, and any timeout long enough to be safe for a
    slow run is too long to be useful after a crash.

    THE LOCK FILE IS NEVER UNLINKED. Unlinking on release is the classic way to
    lose the exclusion: one process holds the lock on an inode and unlinks the
    name, another creates a fresh file at that name and locks the new inode, and
    both believe they are alone. The pid written inside is informational, for the
    refusal message; it is never the liveness test.
    """
    path = lock_path(job_id, root=root)
    config._mkdir_private(path.parent)
    # os.open with an explicit mode rather than the builtin open(), which creates
    # at 0666 masked by the umask and would leave a world-writable lock any local
    # account could hold, making every future drive of this job refuse.
    handle = os.fdopen(os.open(path, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE), "r+")
    try:
        try:
            import fcntl
        except ImportError:  # pragma: no cover - POSIX only in practice
            # No advisory locks here. Proceeding unlocked is the honest
            # degradation: refusing would make the product unusable on that
            # platform, and a claim is still a transaction, so duplicate work is
            # prevented even with the lock absent.
            fcntl = None
        if fcntl is not None:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                handle.seek(0)
                raise DriverHeld(_held_cause(job_id, handle.read(), path)) from None
        handle.seek(0)
        handle.truncate()
        json.dump({"pid": os.getpid(), "acquired": timestamp()}, handle)
        handle.flush()
        yield path
    finally:
        handle.close()  # closing the descriptor releases the lock; the file stays


def assert_free(job_id: str, *, root: Path | None = None) -> None:
    """Refuse when a live driver already holds this job.

    Deliberately a check and not an exclusion. Whatever spawns after it takes the
    lock properly and refuses on its own if it loses the race in between; what
    this buys is that the refusal reaches the person who typed the command,
    instead of being written into a detached child's log where nobody is looking.
    """
    with driver_lock(job_id, root=root):
        pass


def reconcile(store: JobStore, job_id: str, *, root: Path | None = None) -> Job:
    """Re-derive an open job's state from disk truth before anybody reports on it.

    The source supervisor's disk-truth invariant with its false-success hole
    closed. A job whose row still says running while no live driver holds its lock
    was killed, and a kill is evidence of nothing: it becomes queued again, its
    orphaned claims go back to pending, and nothing it had already finished is
    redone.

    Never call this while holding the driver lock for the same job. It takes the
    lock itself, because taking the lock IS the question it is asking.
    """
    job = get(store, job_id)
    if job.state is not JobState.RUNNING:
        return job
    try:
        with driver_lock(job_id, root=root):
            release_claims(store, job_id)
            return reopen(store, job_id)
    except DriverHeld:
        # Somebody is genuinely driving it. Running is the truth here, not a
        # stale row, and evicting a live holder is the one thing this must not do.
        return job


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------


def evidence_or_raise(
    *,
    attempted: int,
    succeeded: int,
    failed_cause: Cause | None = None,
    retryable: bool = True,
) -> None:
    """Refuse to report an empty success when everything actually failed.

    The recorded incident: a phase where every lookup failed returned an empty
    list, the caller read that as "nothing new", and an external mark was applied
    to a playlist holding zero tracks. Empty is a legitimate result only when the
    lookups succeeded, and the two are indistinguishable unless one of them raises.

    Attempting nothing is NOT this case and does not raise. A job with no items is
    a genuine no-op, and treating it as a failure would make an up-to-date source
    look broken.

    ``retryable`` FOLLOWS THE ITEMS. The slug stays ``no-evidence`` because the
    evidence rule is still true. Hardcoding it true, which this function did,
    wrapped a permanent item failure as something to retry later (R-380, and the
    remaining engine half of R-266).
    """
    if attempted == 0 or succeeded > 0:
        return
    extra: dict[str, Any] = {}
    if retryable:
        extra["remedy"] = Remedy.RETRY_LATER
    else:
        extra["steps"] = (
            "the failed items cannot succeed on resume; inspect each item's cause",
        )
    raise refuse(
        "no-evidence",
        f"all {attempted} items failed, so there is no evidence of success; an "
        f"empty result from a total failure is indistinguishable from having found "
        f"nothing, and only one of those may advance anything downstream",
        scope=Scope.SOURCE,
        retryable=retryable,
        origin=("jobs",),
        detail={"attempted": attempted},
        inner=failed_cause,
        **extra,
    )


# ---------------------------------------------------------------------------
# Interruption
# ---------------------------------------------------------------------------


@dataclass
class Interrupt:
    """A signal that arrived, held until the driver reaches a safe point.

    The handler does NOTHING except record. That is what makes "mid-write
    interruption aborts before commit, never during" true rather than hoped for:
    the loop decides where an interruption may take effect, and the durable rename
    is deliberately not one of those places.
    """

    signalled: bool = False
    signal_number: int | None = None
    stage: str | None = None

    def note(self, number: int) -> None:
        self.signalled = True
        self.signal_number = number


@contextmanager
def interruptible(*, stage: str | None = None) -> Iterator[Interrupt]:
    """Record SIGINT and SIGTERM instead of dying on them.

    Whatever was installed before is restored, so a caller that drives two jobs in
    one process does not leave the first one's handler behind. Handlers can only
    be installed on the main thread, so a worker thread degrades to no handling
    rather than raising: an engine unusable from a thread would be a worse defect
    than an uninterruptible one.
    """
    state = Interrupt(stage=stage)
    installed: list[tuple[int, Any]] = []

    def handler(number, frame) -> None:
        state.note(number)

    for number in (signal.SIGINT, signal.SIGTERM):
        try:
            installed.append((number, signal.signal(number, handler)))
        except (ValueError, OSError):  # pragma: no cover - non-main thread
            pass
    try:
        yield state
    finally:
        for number, previous in installed:
            try:
                signal.signal(number, previous)
            except (ValueError, OSError):  # pragma: no cover - non-main thread
                pass


# ---------------------------------------------------------------------------
# Driving
# ---------------------------------------------------------------------------

#: What one item's work looks like. It returns what it produced, and the engine
#: owns making that durable, because the flush-then-rename ordering is the one
#: thing a handler must not be able to get wrong.
Handler = Callable[[Job, Item], "Produced | None"]


@dataclass
class DriveResult:
    """What one drive pass did, for the caller that has to report it."""

    job: Job
    processed: int = 0
    failed: int = 0
    interrupted: bool = False
    drifted: tuple[str, ...] = field(default_factory=tuple)


def _failure_verdict(
    failed: Sequence[Cause],
) -> tuple[str, bool, Remediation]:
    """Reason, retryable, and remediation for a job whose items failed.

    The item rows already carry the honest causes. The job cause a person is
    told to act on has to read them: a wrapper that always says the failure is
    transient tells someone to resume work that cannot succeed (R-380).
    """
    if not failed or any(cause.retryable for cause in failed):
        return (
            "unavailable-transient",
            True,
            Remediation(remedy=Remedy.RESUME_JOB),
        )
    reasons = {cause.reason for cause in failed}
    reason = failed[0].reason if len(reasons) == 1 else failed[-1].reason
    return (
        reason,
        False,
        Remediation(
            steps=(
                "the failed items cannot succeed on resume; inspect each item's cause",
            )
        ),
    )


def _partial_failure_cause(
    job_id: str,
    result: DriveResult,
    inner: Cause | None,
    failed: Sequence[Cause],
) -> Cause:
    reason, retryable, remediation = _failure_verdict(failed)
    transient = sum(1 for cause in failed if cause.retryable)
    permanent = sum(1 for cause in failed if not cause.retryable)
    message = (
        f"job {job_id} finished {result.processed} items and failed "
        f"{result.failed}; the failures keep the job from succeeding and the "
        f"successes are already durable"
    )
    if not retryable:
        message += "; every failure is permanent so resuming this job cannot succeed"
    elif transient and permanent:
        message += f" ({transient} retryable, {permanent} permanent)"
    return Cause(
        reason=reason,
        message=message,
        remediation=remediation,
        scope=Scope.SOURCE,
        retryable=retryable,
        origin=("jobs",),
        detail={
            "job_id": job_id,
            "processed": result.processed,
            "failed": result.failed,
            "retryable_failed": transient,
            "permanent_failed": permanent,
        },
        inner=inner,
    )


class Parked(CratekitError):
    """A handler's answer that the RUN must stop, not that the item failed.

    Raised by a per item worker when the provider refused the CLIENT rather than
    the track: a forbidden response, a bot wall, a wait so long it is a refusal.
    The acquisition layer returns that as a structured cause because it sits
    below the engine and may not park itself (KTD23), and this is the seam the
    engine parks ON.

    WHY A TYPE AND NOT A FIELD ON THE CAUSE. ``refuse`` defaults every cause to
    ``Scope.RUN``, so nearly every item refusal in the package already condemns
    the run by declaration, and keying the park on scope would park a master job
    over ``output-exists``. Keying it on ``retryable`` would park on a lossless
    refusal. A handler that wants the job parked says so with a raise nobody
    else makes by accident, which also keeps the act greppable.

    THE ITEM IS RELEASED, NOT FAILED. A block is a fact about the client and not
    about the track in flight, so the track goes back to pending and the next
    resume, which is a person's deliberate act after checking their account,
    redoes it. Failing it would strand it: ``retry`` re-arms failed items only
    for a TERMINAL job, and a blocked job is open.
    """

    def __init__(self, cause: Cause) -> None:
        super().__init__(cause)


def _internal_item_cause(item: Item, exc: Exception) -> Cause:
    return Cause(
        reason="internal-error",
        message=f"{type(exc).__name__}: {exc}",
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        scope=Scope.ITEM,
        origin=("jobs.drive",),
        detail={"item_id": item.item_id},
    )


def drive(
    store: JobStore,
    job_id: str,
    handle: Handler,
    *,
    root: Path | None = None,
    stage: str = "items",
    current_config: config.Config | None = None,
) -> DriveResult:
    """Run a job's items to completion under one driver, resumably.

    The loop's shape IS the unit's contract, so each step says which property it
    provides:

    * the driver lock is taken FIRST, so a second driver refuses before it has
      touched a row;
    * orphaned claims are released once, so a killed run's single unfinished item
      is redone and nothing else is;
    * the interrupt flag is checked BETWEEN items and BEFORE a commit, never
      inside one;
    * an item's artifact is made durable before its row flips to done;
    * a total failure records the job as failed and then raises, rather than
      returning an empty success.

    ``handle`` receives the job and the item and returns what it produced. It runs
    against ``frozen_config(job)``, which it reads off the job rather than loading
    fresh, because reloading is precisely the resume bug KTD9 closes.
    """
    with driver_lock(job_id, root=root) as lock:
        job = get(store, job_id)
        if not job.is_open():
            raise refuse(
                "internal-error",
                f"job {job_id} is {job.state} and a terminal state is not re-driven",
                remedy=Remedy.REPORT_DEFECT,
                origin=("jobs",),
                detail={"job_id": job_id, "state": str(job.state)},
            )
        drifted = drift(job, current_config) if current_config is not None else ()
        # Anything still claimed belongs to a driver that is gone, because this
        # process now holds the only lock that permits claiming.
        release_claims(store, job_id)
        with store.immediate() as conn:
            _touch(conn, job_id, attempts=job.attempts + 1, pid=os.getpid())
        job = transition(store, job_id, JobState.RUNNING, stage=stage)

        driver = f"{os.getpid()}@{lock.name}"
        result = DriveResult(job=job, drifted=drifted)
        last_cause: Cause | None = None
        failed_causes: list[Cause] = []

        with interruptible(stage=stage) as interrupt:
            while True:
                if interrupt.signalled:
                    result.interrupted = True
                    break
                item = claim(store, job_id, driver)
                if item is None:
                    break
                try:
                    produced = handle(job, item)
                except Parked as exc:
                    # BEFORE the item boundary below, which would fail the item
                    # and claim the next one. The next claim is the second
                    # request into a block, which is the one thing the pacing
                    # layer exists to never make. The item goes back to pending
                    # and the job records why it stopped.
                    release_claims(store, job_id, driver=driver)
                    result.job = block(store, job_id, exc.cause.at("jobs.drive"))
                    return result
                except CratekitError as exc:
                    last_cause = exc.cause.at("jobs.drive")
                    fail_item(store, job_id, item.item_id, last_cause)
                    result.failed += 1
                    failed_causes.append(last_cause)
                    continue
                except Exception as exc:  # noqa: BLE001 - the item boundary converts
                    last_cause = _internal_item_cause(item, exc)
                    fail_item(store, job_id, item.item_id, last_cause)
                    result.failed += 1
                    failed_causes.append(last_cause)
                    continue

                if interrupt.signalled:
                    # The checkpoint that makes the guarantee real. The item is
                    # RELEASED rather than committed, so a resume redoes it whole
                    # instead of inheriting a half-written artifact, and the
                    # commit below is never entered with a signal outstanding.
                    release_claims(store, job_id, driver=driver)
                    result.interrupted = True
                    break

                artifact: Path | None = None
                if produced is not None and produced.staged is not None:
                    if produced.final is None:
                        raise refuse(
                            "internal-error",
                            "an item produced a staged file with nowhere to put it",
                            remedy=Remedy.REPORT_DEFECT,
                            origin=("jobs",),
                            detail={"job_id": job_id, "item_id": item.item_id},
                        )
                    artifact = commit_artifact(produced.staged, produced.final)
                complete_item(store, job_id, item.item_id, artifact=artifact)
                result.processed += 1

        if result.interrupted:
            result.job = cancel(store, job_id, stage=stage)
            return result

        attempted = result.processed + result.failed
        items_retryable = any(cause.retryable for cause in failed_causes)
        if attempted and not result.processed:
            # Recorded BEFORE raising. A raise that leaves the row saying running
            # is the unpersisted-decision half of the same incident: whatever
            # restarts next would have to guess what happened here.
            result.job = transition(
                store,
                job_id,
                JobState.FAILED,
                stage=stage,
                cause=_partial_failure_cause(
                    job_id, result, last_cause, failed_causes
                ),
            )
            evidence_or_raise(
                attempted=attempted,
                succeeded=0,
                failed_cause=last_cause,
                retryable=items_retryable,
            )
        if result.failed:
            result.job = transition(
                store,
                job_id,
                JobState.FAILED,
                stage=stage,
                cause=_partial_failure_cause(
                    job_id, result, last_cause, failed_causes
                ),
            )
        else:
            result.job = transition(store, job_id, JobState.SUCCEEDED, stage=stage)
        return result


# ---------------------------------------------------------------------------
# Detached execution (KTD26)
# ---------------------------------------------------------------------------

#: The payload key every verb freezes its GATE RUN under, so a resume can carry it.
#:
#: WHY THIS IS ONE NAMED CONSTANT RATHER THAN A STRING EACH SHELL SPELLS. A verb
#: that declares an ``explicit`` gate is answerable only by a separate act
#: recorded against a run (R34), and the child this module spawns is a fresh
#: process that mints a NEW run whenever the argv omits ``--run``. So a queued
#: job whose argv does not carry the approving run meets its own gate with
#: nothing recorded, exits DECISION_REQUIRED, and does the same on every respawn:
#: the queue holds work nothing can advance. Three shipped verbs had that shape
#: and two of them were live, measured 2026-08-23.
#:
#: IT IS DELIBERATELY NOT ``run_id``. ``sync.favorites`` already freezes a
#: ``run_id``, and it is the INTAKE run shared across that sync's sources, which
#: is a different thing that happens to default to the same value. Its builder
#: emitted that one as ``--run-id`` and looked correct while restoring no gate
#: state at all. Two concepts under one name is how that defect read as a fix, so
#: the gate run gets a name of its own and the two can never be confused again.
GATE_RUN_KEY = "gate_run_id"

#: The module the engine re-invokes. A MODULE rather than a console script: a
#: console script is a generated wrapper whose location depends on how the
#: package was installed, and shelling out to exactly those wrappers is what the
#: source supervisor does and what this plan deletes.
ENTRY_MODULE = "cratekit.cli"


def child_command(argv: Sequence[str], *, executable: str | None = None) -> list[str]:
    """The command line that re-invokes this product for one job.

    ``argv`` is built by the CLI layer from the queued handler key and the frozen
    payload, and arrives here already assembled. This module never names a verb:
    doing so would put a CLI concept in the infrastructure layer, which the
    layering guard fails the build for, and would give the engine a second opinion
    about what a verb is called.
    """
    return [executable or sys.executable, "-m", ENTRY_MODULE, *argv]


def log_path(job_id: str, *, root: Path | None = None) -> Path:
    return (root or store_dir()) / f"{job_id}.log"


def spawn(
    store: JobStore,
    job: Job,
    argv: Sequence[str],
    *,
    root: Path | None = None,
    executable: str | None = None,
    env: Mapping[str, str] | None = None,
) -> int:
    """Start a job DETACHED, record the child's pid, and return it.

    Detached means its own session, so the job survives the window that started
    it, which is the model the source supervisor already proves. Standard input is
    the null device: R33 says a gate is answered by name from a later process, and
    a detached job able to reach a prompt would wait forever for somebody who is
    not there.

    The pid is recorded for REPORTING only. Liveness is decided by the driver
    lock, because a pid is reused and a lock is not.
    """
    target = log_path(job.job_id, root=root)
    config._mkdir_private(target.parent)
    with open(target, "ab") as sink:
        _own_only(target)
        child = subprocess.Popen(
            child_command(argv, executable=executable),
            stdout=sink,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
            env=dict(env) if env is not None else None,
        )
    with store.immediate() as conn:
        _touch(conn, job.job_id, pid=child.pid)
    return child.pid


__all__ = [
    "ENTRY_MODULE",
    "GATE_RUN_KEY",
    "QUEUE_FILENAME",
    "SCHEMA_VERSION",
    "TERMINAL_STATES",
    "DriveResult",
    "assert_free",
    "DriverHeld",
    "Handler",
    "Interrupt",
    "Item",
    "ItemState",
    "Job",
    "Parked",
    "JobState",
    "JobStore",
    "Produced",
    "block",
    "cancel",
    "child_command",
    "claim",
    "commit_artifact",
    "complete_item",
    "drift",
    "drive",
    "driver_lock",
    "enqueue",
    "evidence_or_raise",
    "fail_item",
    "frozen_config",
    "get",
    "interruptible",
    "items",
    "list_jobs",
    "lock_path",
    "log_path",
    "open_store",
    "progress",
    "queue_path",
    "raise_for_state",
    "reconcile",
    "release_claims",
    "reopen",
    "retry",
    "spawn",
    "states_of",
    "store_dir",
    "transition",
]
