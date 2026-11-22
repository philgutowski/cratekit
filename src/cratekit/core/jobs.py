"""The job engine: resumable, interruptible, observable long work, with no daemon.

KTD8: a SQLite database in write-ahead-log mode is the single source of truth,
and one driver per job is enforced by a lock whose staleness is decided by
holder liveness, never by a timeout.

* A job's status is a ``Cause``, never an exit code (KTD25), so a throttled
  provider and a missing acknowledgment are both blocked and still two
  different things with two different fixes.
* A job runs in a detached subprocess (KTD26), so this module imports no
  feature module and a slim install's help stays cheap.
* An artifact is durable BEFORE the row that claims it flips to done
  (``commit_artifact``), so a kill costs the items claimed, one, or one batch
  for a handler that takes several (U270), and never a false success.
* A total failure raises: empty means "verified empty" only when the lookups
  succeeded.

Layer: INFRASTRUCTURE. It names no verb (KTD23): the command line a job
re-invokes is built by the CLI layer and handed in.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tomllib
from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli.output import new_run_id, timestamp
from cratekit.core import config
from cratekit.core.cause import (
    Cause,
    CratekitError,
    JobBlocked,
    JobCancelled,
    Remediation,
    Scope,
    refuse,
)
from cratekit.core.exit_codes import Remedy
from cratekit.core.private_store import PrivateStore

#: The queue's own schema version; a cross-version resume refuses rather than guessing.
SCHEMA_VERSION = 1

#: The database inside the declared ``job_queue`` directory, which also holds
#: each job's lock and log.
QUEUE_FILENAME = "queue.db"


class JobState(StrEnum):
    """Where a job is. ``blocked`` always carries a cause saying why.

    ``cancelled`` is its own state, never a flavour of failed, so a job a
    person stopped is told apart from one that broke (R22).
    """

    QUEUED = "queued"
    RUNNING = "running"
    BLOCKED = "blocked"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ItemState(StrEnum):
    """Where one unit of work inside a job is.

    ``claimed`` makes a kill between claiming and finishing recoverable: the
    claimed item is redone, and everything done stays done.
    """

    PENDING = "pending"
    CLAIMED = "claimed"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


#: States from which nothing moves: a recorded answer, never re-driven.
TERMINAL_STATES: frozenset[JobState] = frozenset(
    {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
)

#: The forward-only edges between OPEN states. Any open state may also jump to
#: a terminal one, which is what lets a cancel land from anywhere. The one
#: backward edge is ``reopen``, a named function so a rewind is greppable.
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


# The records


@dataclass(frozen=True, slots=True)
class Job:
    """One queued piece of long work, and everything a resume needs to redo it.

    ``payload`` and ``config_toml`` are FROZEN AT QUEUE TIME (KTD9), so a job's
    inputs never change under it while it waits. ``library_id`` is stored
    because the queue is per installation and a library per configuration.
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

    ``item_id`` is a stable identifier from whatever queued the job, never a
    display name (R19). ``ordinal`` fixes the claim order, so a resumed run
    walks the same sequence and redoes exactly one item, or one batch (U270).
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

    The staged file and the path it belongs at; the engine owns the
    flush-then-rename between them, so a handler cannot get the order wrong.
    """

    staged: Path | None = None
    final: Path | None = None


# Storage

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

    For the files somebody else creates under the umask: SQLite's database and
    sidecars, and a job's log. A missing file is normal, as a database with no
    uncheckpointed transactions has no log.
    """
    if not hasattr(os, "chmod"):  # pragma: no cover - platforms without POSIX modes
        return
    try:
        os.chmod(path, config.PRIVATE_FILE_MODE)
    except OSError:
        pass


class JobStore(PrivateStore):
    """The connection to the queue, and the one place its pragmas are decided."""

    _own_only = staticmethod(_own_only)


def store_dir(cfg: config.Config | None = None) -> Path:
    """The declared job-queue directory, resolved through U2 and never composed here."""
    return config.state_path("job_queue", cfg)


def queue_path(cfg: config.Config | None = None) -> Path:
    return store_dir(cfg) / QUEUE_FILENAME


def open_store(path: Path | None = None) -> JobStore:
    """Open, and create if needed, the queue, its directory made private.

    Through ``config.mkdir_private``, because unlink and rename follow the
    DIRECTORY's mode, so a private file in an open directory is not private.
    """
    resolved = path or queue_path()
    config.mkdir_private(resolved.parent)
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


# Reading


def _cause_from_text(text: str | None) -> Cause | None:
    """Read a stored cause; an unreadable one becomes a visible failure, never None.

    None is what a success looks like, so it would erase the evidence.
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
    """Read a state string; an unknown one becomes ``queued``, never terminal.

    A re-drive is safe because the item ledger prevents duplicate work, while
    an unknown read as ``succeeded`` would be an undetectable false success.
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


def _job_row(conn: sqlite3.Connection, job_id: str) -> sqlite3.Row:
    """One job's row, or refuse naming the identifier that did not resolve."""
    row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    if row is None:
        raise refuse(
            "job-unknown",
            f"no job in this installation's queue has the identifier {job_id!r}",
            steps=("check the identifier against the jobs this installation has queued",),
            scope=Scope.RUN,
            origin=("jobs",),
            detail={"job_id": job_id},
        )
    return row


def get(store: JobStore, job_id: str) -> Job:
    """One job, or refuse naming the identifier that did not resolve."""
    return _job_from_row(_job_row(store.conn, job_id))


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


#: Identifiers per ``IN`` clause, under SQLite's parameter limit; an unswept
#: staging tree can name thousands at once.
_ID_CHUNK = 500


def states_of(store: JobStore, job_ids: Sequence[str]) -> dict[str, JobState]:
    """Where each named job got to, leaving out the names this queue does not hold.

    Reads two columns only, so the cost is flat in the payload size, where
    ``get`` and ``list_jobs`` decode every payload and frozen configuration.
    An identifier with no row is ABSENT, never mapped to a state, so the caller
    can tell "never heard of it" from any state.
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
    """Counts per item state and the totals, grouped from the ledger, never a counter."""
    rows = store.conn.execute(
        "SELECT state, COUNT(*) AS n FROM job_items WHERE job_id = ? GROUP BY state",
        (job_id,),
    ).fetchall()
    counts = {str(state): 0 for state in ItemState}
    for row in rows:
        counts[str(_coerce_item_state(row["state"]))] += int(row["n"])
    total = sum(counts.values())
    settled = sum(
        counts[str(state)] for state in (ItemState.DONE, ItemState.FAILED, ItemState.SKIPPED)
    )
    return {"total": total, "settled": settled, "counts": counts}


def reported(store: JobStore, job: Job, extra: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """One job as the ``job_state`` payload every queued verb emits.

    ``extra`` rides UNDER ``progress``: the ``job_state/1`` schema closes its
    top level and leaves ``progress`` open (U51).
    """
    counted = dict(progress(store, job.job_id))
    if extra:
        counted.update(extra)
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": counted,
    }


# Writing


def enqueue(
    store: JobStore,
    *,
    handler_key: str,
    payload: Mapping[str, Any],
    cfg: config.Config,
    item_ids: Sequence[str] = (),
    job_id: str | None = None,
) -> Job:
    """Queue a job, freezing the WHOLE configuration it will run against (KTD9)."""
    now = timestamp()
    identifier = job_id or new_run_id()
    with store.immediate() as conn:
        conn.execute(
            "INSERT INTO jobs (job_id, handler_key, payload, config_fingerprint, "
            "config_toml, library_id, state, stage, cause, attempts, pid, created, "
            "updated) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, 0, NULL, ?, ?)",
            (
                identifier, handler_key, json.dumps(dict(payload), sort_keys=True),
                cfg.fingerprint(), cfg.to_toml_bytes().decode("utf-8"), cfg.library.volume_id,
                str(JobState.QUEUED), now, now,
            ),
        )
        for ordinal, item_id in enumerate(item_ids):
            conn.execute(
                "INSERT INTO job_items (job_id, item_id, ordinal, state) VALUES (?, ?, ?, ?)",
                (identifier, str(item_id), ordinal, str(ItemState.PENDING)),
            )
    return get(store, identifier)


def _touch(conn: sqlite3.Connection, job_id: str, **columns: Any) -> None:
    """Update job columns, always moving ``updated`` with them: the one job-row writer."""
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

    ``blocked`` REQUIRES a cause, checked here, so no job is parked without a reason.
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
                remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
                detail={"job_id": job_id, "from": str(current.state), "to": str(state)},
            )
    if state is JobState.BLOCKED and cause is None:
        raise refuse(
            "internal-error",
            f"job {job_id} was parked with no cause; a throttled provider and a "
            f"missing acknowledgment are both blocked and need different fixes",
            remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
            detail={"job_id": job_id},
        )
    with store.immediate() as conn:
        _touch(
            conn, job_id, state=str(state),
            cause=json.dumps(cause.to_json()) if cause is not None else None,
            stage=stage if stage is not None else current.stage,
        )
    return get(store, job_id)


def reopen(store: JobStore, job_id: str, *, stage: str | None = None) -> Job:
    """The one backward edge: a job whose driver died goes back to queued.

    Safe because a resume re-enters a stage whole over frozen inputs, and the
    item ledger already records what is finished.
    """
    current = get(store, job_id)
    if not current.is_open():
        raise refuse(
            "internal-error",
            f"job {job_id} is {current.state} and a terminal state is never reopened",
            remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
            detail={"job_id": job_id, "state": str(current.state)},
        )
    with store.immediate() as conn:
        _touch(
            conn, job_id, state=str(JobState.QUEUED),
            stage=stage if stage is not None else current.stage, pid=None,
        )
    return get(store, job_id)


def refreeze(store: JobStore, job_id: str, key: str, value: str) -> Job:
    """Rewrite one string value on a SUCCEEDED job's frozen payload (U140).

    Only a succeeded job, which never runs again, is written, so no resume
    reads the changed value (KTD9). State and payload are read INSIDE the
    write's transaction, so a concurrent writer is never overwritten.
    """
    with store.immediate() as conn:
        current = _job_from_row(_job_row(conn, job_id))
        if current.state is not JobState.SUCCEEDED:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state}, and only a succeeded job's frozen "
                f"payload is rewritten, since any other may still run against it",
                remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
                detail={"job_id": job_id, "state": str(current.state), "key": key},
            )
        payload = dict(current.payload)
        payload[key] = str(value)
        _touch(conn, job_id, payload=json.dumps(payload, sort_keys=True))
    return get(store, job_id)


def join_run(store: JobStore, job_id: str, run_id: str) -> Job:
    """Give a QUEUED job that carries no run the run ``run_id`` (U227).

    Only ``run_id`` is written, which no worker reads: it says which pass
    drives the job, never what it resolves. Only a job no driver has started
    and that carries no run is written, so nothing ran on the old payload and
    no job moves between passes. Read and written INSIDE one immediate
    transaction, so two passes cannot both take it.
    """
    wanted = str(run_id or "").strip()
    if not wanted:
        raise refuse(
            "internal-error",
            f"job {job_id} was asked to join a blank run, which is no pass",
            remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
            detail={"job_id": job_id},
        )
    with store.immediate() as conn:
        current = _job_from_row(_job_row(conn, job_id))
        held = str((current.payload or {}).get("run_id") or "")
        if current.state is not JobState.QUEUED or held:
            raise refuse(
                "internal-error",
                f"job {job_id} is {current.state} and carries the run {held or 'none'}, "
                f"and only a queued job that carries no run joins one, since any other "
                f"has run against its payload or belongs to another pass",
                remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
                detail={"job_id": job_id, "state": str(current.state), "run_id": held},
            )
        payload = dict(current.payload)
        payload["run_id"] = wanted
        _touch(conn, job_id, payload=json.dumps(payload, sort_keys=True))
    return get(store, job_id)


def retry(store: JobStore, job_id: str) -> Job:
    """Re-open a job that ended CANCELLED or FAILED, and re-arm its failed items.

    A SUCCEEDED job is refused: every item is done. DONE items stay done (R22).
    A closed job whose cause is not retryable is REFUSED and nothing re-armed
    (R-390), since the engine's own verdict (R-380) already said a resume
    cannot succeed. A cancelled job re-arms, and so does a FAILED job with no
    cause, as a missing verdict is not a permanent one.
    """
    current = get(store, job_id)
    if current.state is JobState.SUCCEEDED:
        raise refuse(
            "internal-error",
            f"job {job_id} succeeded; there is nothing left in it to resume",
            remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
            detail={"job_id": job_id, "state": str(current.state)},
        )
    if current.is_open():
        return current
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
            f"job {job_id} {current.state} with a cause that is not retryable, "
            f"so resuming it cannot succeed and its items were left as they are",
            steps=(
                "inspect each failed item's cause on the job's own record",
                "queue the work again the way it was queued the first time, "
                "once the reason is addressed",
            ),
            origin=("jobs",),
            detail={
                "job_id": job_id,
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )
    with store.immediate() as conn:
        conn.execute(
            "UPDATE job_items SET state = ?, cause = NULL, claimed_by = NULL "
            "WHERE job_id = ? AND state IN (?, ?)",
            (str(ItemState.PENDING), job_id, str(ItemState.FAILED), str(ItemState.CLAIMED)),
        )
        _touch(conn, job_id, state=str(JobState.QUEUED), cause=None, pid=None)
    return get(store, job_id)


#: The detail key a mixed permanent job cause carries its sorted reasons under.
PERMANENT_REASONS = "permanent_reasons"


def _permanent_reasons_of(cause: Cause) -> dict[str, Any]:
    """The mixed job cause's reasons as one detail entry, or nothing."""
    reasons = cause.detail.get(PERMANENT_REASONS)
    return {PERMANENT_REASONS: tuple(reasons)} if reasons else {}


def block(store: JobStore, job_id: str, cause: Cause) -> Job:
    """Park a job with the reason it is parked."""
    return transition(store, job_id, JobState.BLOCKED, cause=cause)


def raise_for_state(job: Job) -> None:
    """Refuse for a job that did not end cleanly. THE ONE MAPPING every shell uses.

    * ``blocked`` raises :class:`JobBlocked`; a blocked job is OPEN, so a
      closed-only check reports ``ok`` over a parked run (R-290).
    * any CLOSED job carrying a cause raises: ``cancelled`` as
      :class:`JobCancelled`, ``failed`` as the plain error, since ``drive``
      raises only when EVERY item failed (R-225).

    CALL IT OUTSIDE THE ``is_open`` BRANCH THAT DRIVES, or a job already failed
    on entry exits 0 for ever. The job's own cause is re-raised, never
    reworded. ``tests/test_job_outcome.py`` refuses a shell that drives without
    calling this, or rolls its own copy.
    """
    if job.state is JobState.BLOCKED:
        # ``transition`` refuses to park a job without a cause, so a causeless
        # blocked row was written elsewhere. It is still refused as BLOCKED, so
        # the envelope agrees with the job listing.
        if job.cause is None:
            raise JobBlocked(
                refuse(
                    "internal-error",
                    f"job {job.job_id} is blocked and records no reason for it",
                    remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
                    detail={"job_id": job.job_id, "state": str(job.state)},
                ).cause
            )
        raise JobBlocked(job.cause)
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
            raise JobCancelled(job.cause)
        raise CratekitError(job.cause)


def cancel(store: JobStore, job_id: str, *, stage: str | None = None) -> Job:
    """Stop a job and record it as CANCELLED, which is not FAILED (R22)."""
    current = get(store, job_id)
    if not current.is_open():
        return current
    where = stage if stage is not None else current.stage
    return transition(
        store, job_id, JobState.CANCELLED, stage=where,
        cause=Cause(
            reason="cancelled",
            message=f"job {job_id} was cancelled" + (f" at stage {where!r}" if where else ""),
            remediation=Remediation(remedy=Remedy.RESUME_JOB),
            scope=Scope.RUN,
            retryable=True,
            origin=("jobs",),
            detail={"job_id": job_id, "stage": where},
        ),
    )


# Claiming, and the durability rule


def claim(store: JobStore, job_id: str, driver: str) -> Item | None:
    """Take the next pending item, or None when there is nothing left."""
    claimed = claim_batch(store, job_id, driver, 1)
    return claimed[0] if claimed else None


def claim_batch(store: JobStore, job_id: str, driver: str, limit: int) -> tuple[Item, ...]:
    """Take up to ``limit`` pending items in ordinal order, or none when nothing is left (U270).

    The select and the update share ONE immediate transaction, or two drivers
    could claim the same item. Items come back in claim order.
    """
    if limit < 1:
        raise refuse(
            "internal-error",
            f"a batch of {limit} items was asked for; a batch takes at least one",
            remedy=Remedy.REPORT_DEFECT, origin=("jobs",),
            detail={"job_id": job_id, "limit": limit},
        )
    with store.immediate() as conn:
        rows = conn.execute(
            "SELECT item_id FROM job_items WHERE job_id = ? AND state = ? "
            "ORDER BY ordinal LIMIT ?",
            (job_id, str(ItemState.PENDING), limit),
        ).fetchall()
        claimed: list[Item] = []
        stamp = timestamp()
        for row in rows:
            conn.execute(
                "UPDATE job_items SET state = ?, claimed_by = ?, claimed_at = ? "
                "WHERE job_id = ? AND item_id = ?",
                (str(ItemState.CLAIMED), driver, stamp, job_id, row["item_id"]),
            )
            claimed.append(
                _item_from_row(
                    conn.execute(
                        "SELECT * FROM job_items WHERE job_id = ? AND item_id = ?",
                        (job_id, row["item_id"]),
                    ).fetchone()
                )
            )
    return tuple(claimed)


def _fsync_directory(path: Path) -> None:
    """Flush a directory entry, so a rename survives a power cut.

    Guarded because a directory is not openable on every platform (R1).
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
    """Make a staged file durable AND put it in place, in that order (KTD8).

    Flush the file, rename it into place, flush the directory. Only after this
    returns may the item's row flip to done, or a kill leaves a "done" item
    with no artifact, a false success a resume trusts.
    """
    config.mkdir_private(final.parent)
    with open(staged, "rb+") as handle:
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(staged, final)
    _fsync_directory(final.parent)
    return final


# Item reports: where one is staged, and where it lands (U57, U298)
#
# A report is the only record of the items deliberately NOT written (R16). It
# lives under the queue root, never the library. The configuration is a
# parameter everywhere here, since ``store_dir()`` alone loads the CURRENT one
# (KTD9).


def read_reports(paths: Iterable[Path]) -> tuple[dict[str, Any], ...]:
    """The reports at ``paths`` that parse to a mapping, in the order given.

    One that cannot be parsed is SKIPPED, never raised on: the summary is a
    display over artifacts already committed.
    """
    found: list[dict[str, Any]] = []
    for path in paths:
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(parsed, dict):
            found.append(parsed)
    return tuple(found)


def by_ordinal(paths: Iterable[Path]) -> list[Path]:
    """The ordinal named files among ``paths``, sorted as numbers, in item order."""
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))


@dataclass(frozen=True, slots=True)
class Artifacts:
    """The two directory names under the queue root one feature's item reports use.

    ``staging`` is a SIBLING of ``final``, never a temp directory, because
    :func:`commit_artifact` renames and that is atomic only within one
    filesystem. The names are arguments because a core module may not name a
    feature package (KTD23).
    """

    final: str
    staging: str

    def __post_init__(self) -> None:
        for name in (self.final, self.staging):
            if not name or "/" in name or name in {".", ".."}:
                raise ValueError(
                    f"{name!r} is not a directory name; a report location is one "
                    f"path component under the queue root"
                )
        if self.final == self.staging:
            raise ValueError(
                "the staging and final directories must differ, or a commit is an "
                "os.replace of a file onto itself"
            )

    def final_dir(self, cfg: config.Config, job_id: str) -> Path:
        """Where one job's committed reports sit."""
        return store_dir(cfg) / self.final / job_id

    def staging_dir(self, cfg: config.Config, job_id: str) -> Path:
        """Where one job's attempts are staged, a directory per item."""
        return store_dir(cfg) / self.staging / job_id

    @staticmethod
    def write(path: Path, payload: dict[str, Any]) -> Path:
        """Serialize one item's report. Sorted keys so two runs produce one file."""
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def final_path(self, cfg: config.Config, job_id: str, ordinal: int) -> Path:
        """Where this item's report belongs once committed, named for the ORDINAL.

        Never for the item identifier, which a filename would turn into a path
        traversal.
        """
        directory = self.final_dir(cfg, job_id)
        config.mkdir_private(directory)
        return directory / f"{ordinal:04d}.json"

    def staged_path(self, cfg: config.Config, job_id: str, ordinal: int) -> Path:
        """A CLEARED staging directory for one attempt at one item.

        Whatever is in it belongs to an attempt that did not finish.
        """
        directory = self.staging_dir(cfg, job_id) / str(ordinal)
        if directory.exists():
            shutil.rmtree(directory)
        config.mkdir_private(directory)
        return directory / f"{ordinal:04d}.json"

    def produced(self, cfg: config.Config, job, item, report: dict[str, Any]) -> Produced:
        """Stage one item's report and hand the engine both paths."""
        return Produced(
            staged=self.write(self.staged_path(cfg, job.job_id, item.ordinal), report),
            final=self.final_path(cfg, job.job_id, item.ordinal),
        )

    def committed(
        self,
        cfg: config.Config,
        job_id: str,
        *,
        ordered: Callable[[Iterable[Path]], Iterable[Path]] = by_ordinal,
    ) -> tuple[dict[str, Any], ...]:
        """Every committed report for this job, in item order.

        READ BACK, never held in memory, so a report covers the items a previous
        process finished too. ``ordered`` says which files are reports and in
        what order.
        """
        directory = self.final_dir(cfg, job_id)
        if not directory.is_dir():
            return ()
        return read_reports(ordered(directory.glob("*.json")))


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
    """Return orphaned claims to pending, only ``driver``'s when named, and count them.

    A claimed item was started and not finished, so it is redone: the bounded
    cost of a kill, one item or one batch (U270).
    """
    query = "UPDATE job_items SET state = ?, claimed_by = NULL WHERE job_id = ? AND state = ?"
    params: tuple[str, ...] = (str(ItemState.PENDING), job_id, str(ItemState.CLAIMED))
    if driver is not None:
        query += " AND claimed_by = ?"
        params += (driver,)
    with store.immediate() as conn:
        return int(conn.execute(query, params).rowcount or 0)


# The frozen configuration, and drift


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

    It NAMES them and never refuses, or every configuration edit would cancel
    the queue. The fingerprint is compared first, the common "nothing moved".
    """
    if job.config_fingerprint == current.fingerprint():
        return ()
    before = _flatten(tomllib.loads(job.config_toml))
    # A frozen adapter name is folded to its current one as the loader folds
    # it, only when it is a string, so a rename does not read as drift (U197).
    if isinstance(before.get("acquisition.adapter"), str):
        before["acquisition.adapter"] = config.current_adapter_name(
            before["acquisition.adapter"]
        )
    after = _flatten(current.to_toml_dict())
    return tuple(
        sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
    )


# One driver per job


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

    Staleness is HOLDER LIVENESS, never a timeout: the kernel releases an
    advisory lock when its holder dies. THE LOCK FILE IS NEVER UNLINKED, or a
    second process could lock a fresh inode at the same name. The pid inside
    is for the refusal message only.
    """
    path = lock_path(job_id, root=root)
    # No advisory locks on a platform reads as had: a claim is still a
    # transaction, so duplicate work is prevented even with the lock absent.
    handle, had = config.lock_now(path)
    try:
        if not had:
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

    A check, not an exclusion, so the refusal reaches the person who typed the
    command rather than a detached child's log.
    """
    with driver_lock(job_id, root=root):
        pass


def reconcile(store: JobStore, job_id: str, *, root: Path | None = None) -> Job:
    """Re-derive an open job's state from disk truth before anybody reports on it.

    A job still ``running`` with no live driver holding its lock was killed: it
    is queued again and its orphaned claims released. Never call this holding
    the same job's driver lock; taking the lock IS the question.
    """
    job = get(store, job_id)
    if job.state is not JobState.RUNNING:
        return job
    try:
        with driver_lock(job_id, root=root):
            release_claims(store, job_id)
            return reopen(store, job_id)
    except DriverHeld:
        # Somebody is genuinely driving it, and a live holder is never evicted.
        return job


# Evidence


def evidence_or_raise(
    *,
    attempted: int,
    succeeded: int,
    failed_cause: Cause | None = None,
    retryable: bool = True,
    permanent_reasons: Sequence[str] = (),
) -> None:
    """Refuse to report an empty success when everything actually failed.

    Empty is a result only when the lookups succeeded. Attempting nothing is a
    genuine no-op and does not raise. ``retryable`` FOLLOWS THE ITEMS (R-380).
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
    message = (
        f"all {attempted} items failed, so there is no evidence of success; an "
        f"empty result from a total failure is indistinguishable from having found "
        f"nothing, and only one of those may advance anything downstream"
    )
    detail: dict[str, Any] = {"attempted": attempted}
    if len(permanent_reasons) > 1:
        # The item stays nested as ``inner``, and the mixed reasons ride beside it (R-391).
        message += (
            f"; the failures carry {len(permanent_reasons)} distinct permanent "
            f"reasons: {', '.join(permanent_reasons)}"
        )
        detail[PERMANENT_REASONS] = tuple(permanent_reasons)
    raise refuse(
        "no-evidence",
        message,
        scope=Scope.SOURCE,
        retryable=retryable,
        origin=("jobs",),
        detail=detail,
        inner=failed_cause,
        **extra,
    )


# Detached execution (KTD26)

#: The payload key every verb freezes its GATE RUN under, so a resume carries it
#: and the respawned child meets its explicit gate with the approval recorded
#: (R34). Deliberately not ``run_id``, which is the INTAKE run, another concept.
GATE_RUN_KEY = "gate_run_id"

#: The module the engine re-invokes, a module and never an installed console script.
ENTRY_MODULE = "cratekit.cli"


def child_command(argv: Sequence[str], *, executable: str | None = None) -> list[str]:
    """The command line that re-invokes this product for one job.

    ``argv`` arrives assembled by the CLI layer; this module never names a verb.
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

    Its own session, so it outlives the window that started it, and standard
    input is the null device, so it can never wait at a prompt (R33). The pid
    is for reporting; liveness is the driver lock's.
    """
    target = log_path(job.job_id, root=root)
    config.mkdir_private(target.parent)
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


# The shell a queued verb drives its job through (U298)


def advance(ctx, store: JobStore, job: Job, *, origin: Sequence[str], nothing_to_run: str):
    """Reconcile, refuse an empty job, drive it, and raise if it did not finish.

    NOT NAMED ``drive``: ``tests/test_handlers.py`` counts every call named
    ``drive`` and allows one. A job with no items is REFUSED, never driven,
    since :func:`drive` would take it straight to succeeded; ``nothing_to_run``
    says what that would have done. Returns as :func:`resumed` does.
    """
    job = reconcile(store, job.job_id)
    if job.is_open() and not items(store, job.job_id):
        raise refuse(
            "internal-error",
            f"job {job.job_id} has no items to run, so driving it would "
            f"{nothing_to_run}. It was queued by a build that did not record "
            f"what its items were",
            remedy=Remedy.REPORT_DEFECT,
            origin=tuple(origin),
            detail={"job_id": job.job_id},
        )
    return resumed(ctx, store, job)


def resumed(ctx, store: JobStore, job: Job):
    """Drive a reconciled job if it is still open, and raise if it did not end cleanly.

    The raise is OUTSIDE the ``is_open`` branch (R-225). Returns the job as it
    stands and the driver's warnings.
    """
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        _result, warnings = ctx.run_job(store, job)
        job = get(store, job.job_id)
    raise_for_state(job)
    return job, warnings


# The drive loop lives in ``core.jobs_drive``; it reads the names above, so it
# is imported last.
from cratekit.core.jobs_drive import (  # noqa: E402
    BatchHandler,
    Batching,
    Declined,
    DriveResult,
    Handler,
    Interrupt,
    Parked,
    decline_item,
    drive,
    interruptible,
)

# Each keeps the module path it had here, so a pickle or a repr reads as before.
for _moved in (Batching, Declined, DriveResult, Interrupt, Parked, decline_item, drive, interruptible):
    _moved.__module__ = __name__
del _moved

__all__ = [
    "ENTRY_MODULE", "GATE_RUN_KEY", "QUEUE_FILENAME", "SCHEMA_VERSION", "TERMINAL_STATES",
    "Artifacts", "BatchHandler", "Batching", "DriveResult", "assert_free", "DriverHeld", "Handler",
    "Interrupt", "Item", "ItemState", "Job", "Declined", "Parked", "JobState", "JobStore",
    "Produced", "advance", "block", "by_ordinal", "cancel", "child_command", "claim",
    "claim_batch", "commit_artifact", "complete_item", "decline_item", "drift", "drive",
    "driver_lock", "enqueue", "evidence_or_raise", "fail_item", "frozen_config", "get",
    "interruptible", "items", "join_run", "list_jobs", "lock_path", "log_path", "open_store",
    "progress", "queue_path", "raise_for_state", "read_reports", "reconcile", "release_claims",
    "reopen", "reported", "resumed", "retry", "spawn", "states_of", "store_dir", "transition",
]
