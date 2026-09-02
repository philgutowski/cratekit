"""The destructive-session boundary: the lock, the acknowledgment, and the log.

The capture the guarded writer takes is only worth something if a person can
spend it, and only safe if nothing can commit behind one that was never checked.
This module is that spend, and it is four separate things that have to agree:

1. **Three gates, in one order, on every destructive session** (KTD24). The
   trigger is DESTRUCTION, not a database write. A backup restore replaces a live
   database and its companion files while writing no row at all, so a rule bound
   to writes would leave the one operation that destroys a library outside the
   safety spine entirely.

2. **A library-scoped lock** (KTD21, KTD17). Both the lock and the log sit beside
   the library rather than beside an installation, so a second machine contends
   with the first instead of holding an invisible lock of its own. The holder is
   named by host, boot identity, process identifier and process start time,
   because a bare process identifier means nothing across machines and is reused
   after a restart.

3. **A session log the pruning scan can actually read.** The source system's
   equivalent got the filename, the state field and one of the two terminal
   values wrong, and nothing failed, because a scan that matches nothing returns
   nothing: every capture was prunable while a comment said otherwise. The
   vocabulary is published here as :data:`RUN_STATE_VOCABULARY` and a test in
   ``tests/test_rb_snapshot.py`` builds a real record, feeds it to the writer's
   scan, and asserts the capture comes back protected. An existence check on a
   field name is not enough; the version that failed had the right-looking names.

4. **An acknowledgment that an agent cannot mint for itself** (R34, KTD18).
   Minting is a separate act, by a person, at a controlling terminal, recorded
   with the backup age that was shown at the time. A destructive session consults
   the RECORD. No flag, no configuration key and no environment variable
   satisfies it, because the one operation that removes a user's files must not
   be gated on something the process removing them can assert about itself.

THE ORDER OF THE THREE GATES IS LOAD BEARING, and it is not the order they are
listed in the plan:

* the VOLUME goes first, because a destructive session has to refuse before it
  resolves a single path. Resolving paths against the wrong volume is already
  the damage, and both the lock and the acknowledgment are library-scoped paths;
* the ACKNOWLEDGMENT goes second, because it is a pure read;
* the LOCK goes last, because it is the only gate that WRITES anything. That is
  what makes "a refused session writes nothing" true on the disk rather than
  approximately true, which is the property ``tests/test_write_session.py``
  asserts by comparing the whole state tree before and after.

WHAT THE SOURCE SCAN CANNOT SEE, AND WHY THIS MODULE OWES THE RUNTIME HALF.
``tests/test_no_beatgrid_ever.py`` forbids, by name, every symbol that
serialises an analysis file. That scan sees only the symbols this package
spells, and reading those files stays legal by decision, so a grid rewritten
through a handle the binding already returned is invisible to it. A destructive
session therefore fingerprints every analysis file it could touch before the
write and compares afterwards, and refuses if one moved.

LAYER: infrastructure. It may read configuration and do input and output. It
names no verb and carries remediation TOKENS only (D2); every verb name that
reaches a persisted record arrives as a parameter from the layer that owns one.
"""

from __future__ import annotations

import json
import logging
import os
import re
import socket
import sys
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli import output
from cratekit.core import backup_facts, config, preflight, rb_writer, reconcile
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Remediation,
    Scope,
    refuse,
    widest_scope,
)
from cratekit.core.exit_codes import Remedy

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# The session log's vocabulary
#
# These three answers are not free choices. ``rb_writer.RunStateVocabulary``
# declares provisional defaults and its docstring makes this unit accountable for
# them, so the log is spelled the way that scan already expects rather than the
# scan being taught a second spelling.
# ---------------------------------------------------------------------------


class SessionState(StrEnum):
    """Where one destructive session got to. Five answers, and only two are ends.

    ``AWAITING_IMPORT`` is a first-class state rather than a flag on a finished
    run. A session whose XML half is written and whose import has not happened is
    not finished, and treating it as finished is how the next run writes over the
    node that import was meant to create.

    ``COMMITTED_UNVERIFIED`` is deliberately NOT terminal. Post-commit rollback
    does not exist, so a read-back that disagrees leaves a library nobody can
    vouch for; keeping the state open is what keeps its capture protected from
    pruning and what keeps the next write refused until a person resolves it.
    """

    OPEN = "open"
    AWAITING_IMPORT = "awaiting-import"
    COMMITTED_UNVERIFIED = "committed-unverified"
    CLOSED = "closed"
    ABANDONED = "abandoned"


#: The states that RELEASE a capture. Everything else still references one.
TERMINAL_STATES: frozenset[SessionState] = frozenset(
    {SessionState.CLOSED, SessionState.ABANDONED}
)

#: The record field the pruning scan reads to decide whether a session is over.
STATE_KEY = "state"

#: The record field naming the capture that session is the undo for.
SNAPSHOT_KEY = "snapshot_path"

#: What the guarded writer's snapshot-protection scan should read, DERIVED from
#: the declarations above rather than restated as three more strings. The two
#: modules agreeing is asserted by driving a real record through the real scan,
#: not by comparing spellings, because the version of this that failed had the
#: right-looking spellings and matched nothing.
RUN_STATE_VOCABULARY = rb_writer.RunStateVocabulary(
    state_key=STATE_KEY,
    terminal_states=frozenset(str(state) for state in TERMINAL_STATES),
    snapshot_key=SNAPSHOT_KEY,
)

#: Bumped only when the log's on-disk shape changes incompatibly.
LOG_SCHEMA_VERSION = 1


class SourceState(StrEnum):
    """Per-source progress inside one session (R29).

    The boundary is one source per run, committed and captured independently, so
    a refusal at source two leaves source one committed and says so. Without a
    per-source state a resume either redoes committed work or skips uncommitted
    work, and there is no way to tell which from the outside.
    """

    PENDING = "pending"
    COMMITTED = "committed"
    REFUSED = "refused"


# ---------------------------------------------------------------------------
# The change summary
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TreeChange:
    """What one session did to one tree, in counts.

    ``tree`` is a STABLE IDENTIFIER supplied by the caller, never a display name
    (R19). A record keyed on the name a user sees is orphaned the moment they
    rename it, and the orphan is invisible: the code simply finds no entry.
    """

    tree: str
    created: int = 0
    updated: int = 0

    def to_json(self) -> dict[str, Any]:
        return {"tree": self.tree, "created": self.created, "updated": self.updated}

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> TreeChange:
        return cls(
            tree=str(data["tree"]),
            created=int(data.get("created", 0)),
            updated=int(data.get("updated", 0)),
        )


@dataclass(frozen=True, slots=True)
class ChangeSummary:
    """Every tree a session touched, with per-tree counts.

    PER TREE, not one total, and that is a requirement rather than a nicety. A
    session spans several trees, and U32's restore asks a person to approve
    discarding work in tree-and-count terms. One aggregate number makes that
    judgement impossible: "forty changes" says nothing about whether the forty
    were in the tree the user cares about.
    """

    trees: tuple[TreeChange, ...] = ()

    @property
    def created(self) -> int:
        return sum(entry.created for entry in self.trees)

    @property
    def updated(self) -> int:
        return sum(entry.updated for entry in self.trees)

    def merged(self, other: ChangeSummary) -> ChangeSummary:
        """Combine two summaries, adding counts for a tree both name.

        Keyed on the stable identifier, and sorted on the way out so the recorded
        bytes are a function of the content alone rather than of the order the
        sources happened to run in.
        """
        totals: dict[str, TreeChange] = {entry.tree: entry for entry in self.trees}
        for entry in other.trees:
            seen = totals.get(entry.tree)
            totals[entry.tree] = (
                entry
                if seen is None
                else TreeChange(
                    tree=entry.tree,
                    created=seen.created + entry.created,
                    updated=seen.updated + entry.updated,
                )
            )
        return ChangeSummary(tuple(sorted(totals.values(), key=lambda e: e.tree)))

    def to_json(self) -> dict[str, Any]:
        return {
            "trees": [entry.to_json() for entry in self.trees],
            "created": self.created,
            "updated": self.updated,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> ChangeSummary:
        return cls(tuple(TreeChange.from_json(entry) for entry in (data.get("trees") or ())))


# ---------------------------------------------------------------------------
# The session record and its log
# ---------------------------------------------------------------------------


@dataclass
class SessionRecord:
    """One destructive session, as the log holds it.

    Mutable on purpose: a session evolves, and every transition is persisted as
    it happens rather than at the end. A record written only on a clean finish is
    a record that is absent for exactly the runs somebody needs to recover from.
    """

    session_id: str
    workflow: str
    started: str
    state: SessionState = SessionState.OPEN
    snapshot_path: str | None = None
    change: ChangeSummary = field(default_factory=ChangeSummary)
    actor: str | None = None
    acknowledged_at: str | None = None
    sources: dict[str, str] = field(default_factory=dict)
    ended: str | None = None
    pending: output.PendingHumanAction | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def terminal(self) -> bool:
        return self.state in TERMINAL_STATES

    def committed_sources(self) -> tuple[str, ...]:
        return tuple(
            sorted(k for k, v in self.sources.items() if v == str(SourceState.COMMITTED))
        )

    def remaining_sources(self) -> tuple[str, ...]:
        return tuple(
            sorted(k for k, v in self.sources.items() if v != str(SourceState.COMMITTED))
        )

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": LOG_SCHEMA_VERSION,
            "session_id": self.session_id,
            "workflow": self.workflow,
            "started": self.started,
            STATE_KEY: str(self.state),
            SNAPSHOT_KEY: self.snapshot_path,
            "change": self.change.to_json(),
            "actor": self.actor,
            "acknowledged_at": self.acknowledged_at,
            "sources": dict(sorted(self.sources.items())),
            "ended": self.ended,
            "pending_human_action": self.pending.to_json() if self.pending else None,
            "detail": dict(sorted(self.detail.items())),
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> SessionRecord:
        version = data.get("schema_version")
        if version != LOG_SCHEMA_VERSION:
            raise refuse(
                "internal-error",
                f"the session log entry declares schema {version!r} and this "
                f"build understands {LOG_SCHEMA_VERSION}; refusing to guess what "
                f"wrote it",
                remedy=Remedy.REPORT_DEFECT,
                detail={"schema_version": version},
            )
        pending = data.get("pending_human_action")
        return cls(
            session_id=str(data["session_id"]),
            workflow=str(data["workflow"]),
            started=str(data["started"]),
            state=SessionState(str(data[STATE_KEY])),
            snapshot_path=data.get(SNAPSHOT_KEY),
            change=ChangeSummary.from_json(data.get("change") or {}),
            actor=data.get("actor"),
            acknowledged_at=data.get("acknowledged_at"),
            sources=dict(data.get("sources") or {}),
            ended=data.get("ended"),
            pending=output.PendingHumanAction.from_json(pending) if pending else None,
            detail=dict(data.get("detail") or {}),
        )


def log_dir(cfg: config.Config) -> Path:
    """Where session records live, resolved through the declared state inventory.

    Through ``state_path`` and never composed here. The entry is library-scoped
    and SURVIVES a rollback, and it is the SAME directory the guarded writer's
    protection scan reads. A module that built its own path under a state root
    would have invented a store the inventory does not know about, which is
    precisely the defect that made that scan match nothing.
    """
    return config.state_path("session_log", cfg)


#: Everything outside this set is replaced before an identifier becomes a
#: filename. Deliberately a WHITELIST: a blacklist of the characters one
#: filesystem rejects is a blacklist that is wrong on the next filesystem.
_UNSAFE_IN_A_FILENAME = re.compile(r"[^A-Za-z0-9._-]")


def log_path(session_id: str, cfg: config.Config) -> Path:
    """One session's record, under a name every filesystem this library can sit on accepts.

    THE IDENTIFIER AND THE FILENAME ARE DIFFERENT QUESTIONS. The identifier keeps
    the shape the run identifier space uses, colons and all, because that is what
    makes a session addressable in the same breath as a run. The filename may not:
    this path is composed on whatever filesystem the USER's library lives on, and
    this store is library-scoped. exFAT and FAT are ordinary choices for a library
    volume, because that is what a CDJ reads, and a colon is not a legal character
    on either; on Windows it is the alternate-data-stream separator rather than a
    character at all. ``snapshot.new_stamp`` reaches the same conclusion from the
    other side and states the same reason.

    Sanitising also closes a second hole. ``open_session`` accepts a supplied
    identifier, and a path separator inside one would compose a record OUTSIDE the
    directory the pruning scan reads: a session that protects no capture and that
    no gate can see.
    """
    return log_dir(cfg) / f"{_UNSAFE_IN_A_FILENAME.sub('-', session_id)}.json"


def new_session_id(now: datetime | None = None) -> str:
    """A sortable, addressable identifier for one session.

    The SAME identifier space the run record already uses, rather than a second
    one invented here. Two identifier schemes in one product is how a support
    conversation ends up unable to say which record a number refers to.
    """
    return output.new_run_id(now)


def write_record(record: SessionRecord, cfg: config.Config) -> Path:
    """Persist one session record atomically, owner-readable only.

    Atomic because it is written on the way out of a refusal as well as on the
    way to a clean finish, and a torn record is a session nobody can restore
    from. The shared writer gives it an explicit mode and creates the directory
    private, so neither depends on the process umask (P1).
    """
    path = log_path(record.session_id, cfg)
    config.atomic_write_bytes(
        json.dumps(record.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def read_record(session_id: str, cfg: config.Config) -> SessionRecord:
    """Read one session record, or refuse naming the session.

    TWO HANDLERS, BECAUSE ABSENCE AND REFUSAL ARE TWO ANSWERS. One handler over
    every ``OSError`` said "no session is recorded with that identifier" for a
    record this account was not allowed to open, which reads absence out of a
    read that never happened. A directory on the way to the file that the
    operating system will not traverse fails exactly the same way, and under it
    nothing has been observed at all.
    """
    path = log_path(session_id, cfg)
    try:
        raw = path.read_bytes()
    except FileNotFoundError as exc:
        raise refuse(
            "internal-error",
            f"no session is recorded with the identifier {session_id!r}: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": session_id, "path": str(path)},
        ) from exc
    except OSError as exc:
        raise refuse(
            "internal-error",
            f"the session record at {path} could not be read, so whether a "
            f"session is recorded under {session_id!r} was not established: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": session_id, "path": str(path)},
        ) from exc
    return SessionRecord.from_json(json.loads(raw.decode("utf-8")))


def scan_log(cfg: config.Config) -> tuple[tuple[SessionRecord, ...], tuple[Path, ...]]:
    """Read the log once and return BOTH halves: what parsed, and what did not.

    ONE SCAN WITH TWO CONSUMERS, rather than two scans that can disagree about
    one directory, which is the defect class this module exists to abolish. What
    differs between the consumers is the POLICY they apply to the second half,
    and the policies are opposites for good reasons:

    * reporting drops what it cannot read, because a single damaged file must not
      stop the product describing every other session;
    * a GATE may not, because a scan that drops what it cannot read fails OPEN.
      A bumped schema version or a state value a later build introduced would
      make an unresolved commit invisible and admit the very write the refusal
      exists to stop.

    Returning both halves is what lets each consumer say which one it is.
    """
    try:
        entries = sorted(log_dir(cfg).glob("*.json"))
    except OSError:
        return (), ()
    parsed: list[SessionRecord] = []
    unreadable: list[Path] = []
    for entry in entries:
        try:
            parsed.append(SessionRecord.from_json(json.loads(entry.read_text())))
        except (OSError, ValueError, KeyError, TypeError, CratekitError) as exc:
            logger.debug("session record %s could not be read: %s", entry, exc)
            unreadable.append(entry)
    return tuple(parsed), tuple(unreadable)


def records(cfg: config.Config) -> tuple[SessionRecord, ...]:
    """Every readable session record, newest identifier last.

    An unreadable or foreign entry is SKIPPED rather than fatal, for the same
    reason the writer's own scan skips one: a single damaged file must not stop
    the product reporting on every other session, and the directory is shared
    with whatever a later build writes there.

    THAT POLICY IS FOR REPORTING AND FOR NOTHING ELSE. A gate that borrowed it
    would fail open; see :func:`scan_log` and :func:`assert_no_unresolved_session`.
    """
    return scan_log(cfg)[0]


# ---------------------------------------------------------------------------
# The lock holder
# ---------------------------------------------------------------------------

#: Recorded in place of a value this platform cannot answer. A holder carrying it
#: is still a usable holder: the exclusion itself is done by the kernel, and this
#: identity exists to NAME the holder in a refusal and to judge whether a
#: recorded holder is still alive. Naming the gap is what stops a caller reading
#: a degraded identity as a confident one.
UNKNOWN_IDENTITY = "unknown"


@dataclass(frozen=True, slots=True)
class Holder:
    """Who holds the session lock, identified across machines and restarts.

    Four fields, and each one closes a way the other three lie:

    * ``host`` alone cannot tell two machines apart from one machine's two runs;
    * ``pid`` alone is meaningless on another machine and is REUSED after a
      restart, so a stale record can name a live and entirely unrelated process;
    * ``boot`` distinguishes this boot of this machine from the last one, which
      is what makes a recycled identifier detectable;
    * ``started`` distinguishes this process from the next one to receive the
      same identifier within one boot.
    """

    host: str
    boot: str
    pid: int
    started: str

    def to_json(self) -> dict[str, Any]:
        return {"host": self.host, "boot": self.boot, "pid": self.pid, "started": self.started}

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Holder:
        return cls(
            host=str(data.get("host", UNKNOWN_IDENTITY)),
            boot=str(data.get("boot", UNKNOWN_IDENTITY)),
            pid=int(data.get("pid", 0)),
            started=str(data.get("started", UNKNOWN_IDENTITY)),
        )

    def describe(self) -> str:
        return f"process {self.pid} on {self.host} (boot {self.boot}, started {self.started})"


def boot_identity() -> str:
    """This boot of this machine, or the declared unknown.

    Read lazily through the process library so a caller that never touches the
    lock never loads the extension module, which is the same discipline
    ``core.processes`` already applies for the same reason.
    """
    try:
        import psutil

        return f"{psutil.boot_time():.0f}"
    except Exception as exc:  # noqa: BLE001 - an unanswerable identity is not a failure
        logger.debug("boot identity is unavailable on this platform: %s", exc)
        return UNKNOWN_IDENTITY


def process_started(pid: int) -> str:
    """When a process began, or the declared unknown.

    Returns the unknown for a process that does not exist, which is the same
    answer as a platform that cannot say. The caller discriminates on liveness
    separately, so collapsing the two here costs nothing and keeps this a probe
    rather than a judgement.
    """
    try:
        import psutil

        return f"{psutil.Process(pid).create_time():.3f}"
    except Exception as exc:  # noqa: BLE001 - see the docstring
        logger.debug("process start time is unavailable for %s: %s", pid, exc)
        return UNKNOWN_IDENTITY


def process_exists(pid: int) -> bool | None:
    """Whether a process with this identifier exists, or None when this cannot say.

    THE LIVENESS QUESTION, SPLIT OFF FROM THE IDENTITY ONE. ``process_started``
    deliberately collapses "no such process" into "cannot answer" and says the
    caller discriminates separately; this is that discrimination, and without it
    the collapse is a defect rather than a simplification. A caller comparing
    start times alone reads an unanswerable start time as a mismatch, and a
    mismatch reads as DEAD, which is how a live holder's claim on the library
    gets cleared out from under it.

    Three answers, not two. None is not False: a platform that cannot say must
    not be read as a platform saying no.
    """
    try:
        import psutil

        return bool(psutil.pid_exists(pid))
    except Exception as exc:  # noqa: BLE001 - an unanswerable question is not a failure
        logger.debug("process existence is unavailable for %s: %s", pid, exc)
        return None


def current_holder() -> Holder:
    """This process, as the lock file will record it."""
    pid = os.getpid()
    return Holder(
        host=socket.gethostname(),
        boot=boot_identity(),
        pid=pid,
        started=process_started(pid),
    )


def holder_alive(holder: Holder, *, here: Holder | None = None) -> bool:
    """Whether a recorded holder is still running.

    FAILS TOWARDS ALIVE, deliberately, on every question this process cannot
    answer: a holder on another host, a holder from another boot of this host, a
    holder whose record carries no start time, or a live process whose start time
    this platform will not report. Guessing "dead" would let one machine clear
    another machine's lock, and the operation the lock protects is the one that
    removes files.

    "DOES IT EXIST" AND "IS IT THE SAME PROCESS" ARE ASKED SEPARATELY, and that
    separation is the whole correctness of the last two lines. The start time is
    compared as well as the identifier because identifiers are recycled: without
    it, a record left by a crashed run names whatever process later inherited
    that number, and clearing on that basis is exactly backwards. But an
    unanswerable start time is not a mismatch. A shared machine that refuses to
    report another account's process start time would otherwise make every one of
    its live holders read as dead, and the remedy a caller then prints is
    "release the stale lock" against a session that is writing right now.
    """
    reference = here or current_holder()
    if holder.host != reference.host or holder.boot != reference.boot:
        return True
    if UNKNOWN_IDENTITY in (holder.boot, reference.boot):
        return True
    if holder.started == UNKNOWN_IDENTITY:
        return True
    exists = process_exists(holder.pid)
    if exists is not True:
        # False is a confident "gone", which is the one answer that may clear a
        # claim. None is "this platform will not say", which may not.
        return exists is None
    observed = process_started(holder.pid)
    if observed == UNKNOWN_IDENTITY:
        return True
    return observed == holder.started


# ---------------------------------------------------------------------------
# The lock
# ---------------------------------------------------------------------------


class SessionComposition(CratekitError):
    """A session was opened inside a session, in one process.

    Reported as a PROGRAMMING ERROR rather than as contention, which is the whole
    reason this is checked before the kernel is asked. Advisory locks are held per
    open file description, so a second acquisition in one process fails exactly
    the way a foreign holder does: the caller would be told to wait for a holder
    that is itself, forever.
    """


#: Lock paths this PROCESS currently holds. The composition check reads it before
#: the kernel is asked; see :class:`SessionComposition` for why the order matters.
_HELD: set[str] = set()


def lock_path(cfg: config.Config) -> Path:
    """The whole-run lock, beside the library.

    A different file from the guarded writer's own lock, and deliberately so.
    That one is narrow: it is held from capture through smoke test so two writers
    cannot interleave. This one is wide: it is held for a whole destructive
    session, so a second Cratekit process refuses at the door rather than part
    way through.
    """
    return config.state_path("session_lock", cfg)


def read_lock_holder(path: Path | str) -> Holder | None:
    """Who the lock file says holds it, or None when it says nobody.

    An unreadable or empty file answers None. The lock file's CONTENT is
    advisory: the exclusion is the kernel's, and this record exists so a refusal
    can name a holder instead of saying only that something is in the way.
    """
    try:
        raw = Path(path).read_text()
    except OSError:
        return None
    if not raw.strip():
        return None
    try:
        data = json.loads(raw)
    except ValueError:
        return None
    if not isinstance(data, Mapping) or not data.get("holder"):
        return None
    try:
        return Holder.from_json(data["holder"])
    except (TypeError, ValueError, AttributeError):
        # THE DOCSTRING'S PROMISE, KEPT. ``Holder.from_json`` coerces the pid
        # with a bare ``int()``, so a record carrying a non numeric one raised
        # straight out of a function whose first line says an unreadable file
        # answers None. That was only reachable through a live contention race
        # until ``session.release`` landed and made reading this file the first
        # thing a plain invocation does, at which point a corrupted lock record
        # became a traceback wearing a generic internal error instead of a
        # refusal from the verb's own vocabulary. Structurally damaged and
        # absent are still different conditions and the SHELL distinguishes
        # them, by asking whether the file has bytes in it.
        return None


def _write_holder(handle: Any, holder: Holder | None) -> None:
    """Record, or clear, the holder inside the already-locked file."""
    handle.seek(0)
    handle.truncate()
    if holder is not None:
        handle.write(json.dumps({"holder": holder.to_json()}, sort_keys=True))
    handle.flush()
    os.fsync(handle.fileno())


def _open_lock_file(target: Path) -> Any:
    """Open the lock file, private, creating the directory private with it.

    The directory mode is part of the file mode: a private lock file inside a
    world-writable directory can be unlinked and replaced by any local account,
    and that takes the mutual exclusion with it (P1).
    """
    config._mkdir_private(target.parent)
    # Opened through the low-level call with an explicit mode rather than the
    # builtin, which creates at 0666 masked by the umask, and in read-write
    # rather than append mode, because the holder record is REPLACED on every
    # acquisition and an append-mode handle ignores where it was told to write.
    descriptor = os.open(target, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
    handle = os.fdopen(descriptor, "r+")
    if hasattr(os, "chmod"):  # guarded: a POSIX mode is meaningless on some platforms
        try:
            # The creation mode above applies only when this call CREATED the
            # file. A lock left behind by an earlier build is already there and
            # would keep its old mode forever without this.
            os.chmod(target, config.PRIVATE_FILE_MODE)
        except OSError as exc:
            # Best effort and deliberately not fatal, exactly as the writer's own
            # lock treats it: a second person on a shared machine cannot change
            # the mode of a file the first one created, and refusing there would
            # trade a cosmetic problem for no mutual exclusion at all.
            logger.debug("could not set the mode on the session lock at %s: %s", target, exc)
    return handle


def _lock_held_refusal(target: Path, holder: Holder | None) -> CratekitError:
    """The refusal for a lock somebody else has, with the right remedy token.

    Two remedies, chosen on evidence rather than on assumption. A holder that is
    still running is waited for. A lock still held while its recorded holder is
    gone is a lock somebody has to release, which is an explicit act and never
    something this code does on its own.

    THE HONEST LIMIT. With the advisory backend used here the kernel drops a
    lock when its holder dies, so the second branch is unreachable on a local
    filesystem. It exists because the backend is not the only thing that can hold
    this file: a networked filesystem whose locking semantics differ can leave
    exactly that state, and a refusal that named the wrong remedy there would
    send a user to wait for a process that no longer exists.
    """
    if holder is not None and holder_alive(holder):
        return refuse(
            "session-lock-held",
            f"another destructive session holds the library lock at {target}: "
            f"{holder.describe()}",
            remedy=Remedy.WAIT_FOR_HOLDER,
            scope=Scope.SESSION,
            detail={"lock": str(target), "holder": holder.to_json()},
        )
    return refuse(
        "session-lock-held",
        f"the library lock at {target} is held and its recorded holder is not "
        f"running"
        + (f": {holder.describe()}" if holder is not None else " and is unrecorded"),
        remedy=Remedy.RELEASE_STALE_LOCK,
        scope=Scope.SESSION,
        detail={
            "lock": str(target),
            "holder": holder.to_json() if holder is not None else None,
            "stale": True,
        },
    )


@contextmanager
def session_lock(
    cfg: config.Config | None = None,
    *,
    path: Path | str | None = None,
    holder: Holder | None = None,
) -> Iterator[Path]:
    """Hold the whole-run lock for one destructive session.

    THE FILE IS NEVER UNLINKED. Unlinking it to tidy up races a live holder that
    holds a lock on the inode: the second process creates a fresh file at the
    same name, locks that instead, and both then believe they have exclusive
    access with nothing raised. Releasing clears the recorded holder and leaves
    the file, which costs one empty file and nothing else.
    """
    target = Path(path) if path is not None else lock_path(cfg or config.load())
    key = str(target.absolute())
    if key in _HELD:
        raise SessionComposition(
            Cause(
                reason="internal-error",
                message=(
                    f"a destructive session was opened inside another one in this "
                    f"process, on {target}. Sessions do not nest: the second "
                    f"acquisition can never succeed, and reporting it as a foreign "
                    f"holder would tell a caller to wait for itself"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                scope=Scope.RUN,
                origin=("session",),
                detail={"lock": str(target)},
            )
        )

    handle = _open_lock_file(target)
    acquired = False
    try:
        try:
            # The SAME two-backend acquisition the guarded writer uses, called
            # rather than reimplemented. A third implementation of one primitive
            # is a third chance for one of them to differ on a platform nobody
            # tests, and the difference would be invisible until two writers ran.
            rb_writer._acquire_exclusive(handle)
        except OSError as exc:
            raise _lock_held_refusal(target, read_lock_holder(target)) from exc
        acquired = True
        _HELD.add(key)
        _write_holder(handle, holder or current_holder())
        yield target
    finally:
        if acquired:
            _HELD.discard(key)
            try:
                _write_holder(handle, None)
            except OSError as exc:
                logger.debug("could not clear the holder record on %s: %s", target, exc)
            try:
                rb_writer._release_exclusive(handle)
            except OSError as exc:  # pragma: no cover - the close below still frees it
                logger.debug("could not release the lock on %s: %s", target, exc)
        handle.close()


def release_stale_lock(
    cfg: config.Config | None = None, *, path: Path | str | None = None
) -> Holder | None:
    """Clear a dead holder's record. An EXPLICIT act, never an automatic one.

    Returns the holder that was cleared, or None when there was nothing recorded.

    Refuses while the recorded holder is still running, because the alternative
    is one run clearing another run's claim on the library mid-write. That is not
    a theoretical courtesy: the whole point of the lock is that the operation
    underneath it cannot be interleaved.
    """
    target = Path(path) if path is not None else lock_path(cfg or config.load())
    recorded = read_lock_holder(target)
    if recorded is None:
        return None
    if holder_alive(recorded):
        raise refuse(
            "session-lock-held",
            f"the library lock at {target} is held by {recorded.describe()}, which "
            f"is still running, so its claim is not stale and is not releasable",
            remedy=Remedy.WAIT_FOR_HOLDER,
            scope=Scope.SESSION,
            detail={"lock": str(target), "holder": recorded.to_json()},
        )

    handle = _open_lock_file(target)
    try:
        try:
            rb_writer._acquire_exclusive(handle)
        except OSError as exc:
            raise refuse(
                "session-lock-held",
                f"the library lock at {target} could not be taken even though its "
                f"recorded holder {recorded.describe()} is gone, so something else "
                f"is holding the file",
                remedy=Remedy.WAIT_FOR_HOLDER,
                scope=Scope.SESSION,
                detail={"lock": str(target), "holder": recorded.to_json()},
            ) from exc
        _write_holder(handle, None)
        rb_writer._release_exclusive(handle)
    finally:
        handle.close()
    return recorded


# ---------------------------------------------------------------------------
# The backup acknowledgment (KTD18, R34)
# ---------------------------------------------------------------------------

#: The state entry this acknowledgment is written to. Library-scoped, because the
#: thing acknowledged is a backup of THIS library.
ACK_KEY = "backup_ack"

#: Bumped only when the record's shape changes incompatibly.
ACK_SCHEMA_VERSION = 1

#: How long one acknowledgment answers for. Bounded because an unbounded one is
#: not an acknowledgment, it is a permanent affirmative wearing a timestamp, and
#: R34 exists to forbid exactly that. Long enough that a person is not re-asked
#: inside one working session, short enough that yesterday's answer does not
#: cover today's deletion.
DEFAULT_ACK_VALIDITY = timedelta(hours=12)


@dataclass(frozen=True, slots=True)
class ShownAge:
    """One backup portion's age AS IT WAS SHOWN when the person answered.

    Recorded rather than recomputed, because the question a person answered was
    "given this, proceed?" and re-deriving the number later answers a different
    question. KTD18 asks for the acknowledgment and the age together for that
    reason: an acknowledgment with no age is a click, not a decision.
    """

    portion: str
    state: str
    age_seconds: float | None = None
    completed_at: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "portion": self.portion,
            "state": self.state,
            "age_seconds": self.age_seconds,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> ShownAge:
        return cls(
            portion=str(data["portion"]),
            state=str(data["state"]),
            age_seconds=data.get("age_seconds"),
            completed_at=data.get("completed_at"),
        )


@dataclass(frozen=True, slots=True)
class Acknowledgment:
    """One recorded acknowledgment, with the actor and the window it answers for."""

    actor: str
    recorded_at: datetime
    expires_at: datetime
    shown: tuple[ShownAge, ...] = ()

    def valid_at(self, moment: datetime) -> bool:
        return moment < self.expires_at

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": ACK_SCHEMA_VERSION,
            "actor": self.actor,
            "recorded_at": self.recorded_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "shown": [entry.to_json() for entry in self.shown],
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Acknowledgment:
        version = data.get("schema_version")
        if version != ACK_SCHEMA_VERSION:
            raise refuse(
                "internal-error",
                f"the backup acknowledgment declares schema {version!r} and this "
                f"build understands {ACK_SCHEMA_VERSION}",
                remedy=Remedy.REPORT_DEFECT,
                detail={"schema_version": version},
            )
        return cls(
            actor=str(data["actor"]),
            recorded_at=datetime.fromisoformat(str(data["recorded_at"])),
            expires_at=datetime.fromisoformat(str(data["expires_at"])),
            shown=tuple(ShownAge.from_json(entry) for entry in (data.get("shown") or ())),
        )


def has_controlling_terminal() -> bool:
    """Whether this invocation has a terminal a person could be sitting at.

    A TERMINAL CHECK, NOT A READ, and the distinction is the whole reason this
    function exists. R33 says no verb reads standard input, because a prompt
    cannot be answered by a detached job and cannot be recorded as having been
    answered by anyone. Opening the controlling terminal device asks whether a
    person COULD be there without consuming a byte from anywhere, and it does not
    change behaviour under a pipe the way an input-stream probe does.

    Falls back to asking the output stream on a platform with no controlling
    terminal device, so the check degrades rather than declaring every invocation
    on such a platform unable to acknowledge anything, ever.
    """
    ctermid = getattr(os, "ctermid", None)
    if ctermid is not None:
        try:
            descriptor = os.open(ctermid(), os.O_RDONLY)
        except OSError:
            return False
        os.close(descriptor)
        return True
    stream = sys.__stdout__
    try:
        return bool(stream is not None and stream.isatty())
    except (OSError, ValueError):  # pragma: no cover - a closed stream
        return False


def derive_actor() -> str:
    """Who this invocation is, derived from the invocation and never supplied.

    R34's sharpest clause. If a caller could name the actor, an agent driving the
    command line would mint the gate protecting the one operation that removes
    files, and the audit trail would record whatever name it chose. So the
    account is read from the process identity rather than taken as an argument,
    and ``record_acknowledgment`` has no parameter that could carry one.

    The account database is read directly rather than through the convenience
    wrapper, because that wrapper's module also offers a password prompt and this
    package's static guard forbids importing it at all.
    """
    account = os.environ.get("USER") or os.environ.get("USERNAME") or UNKNOWN_IDENTITY
    try:
        import pwd

        account = pwd.getpwuid(os.getuid()).pw_name
    except Exception as exc:  # noqa: BLE001 - no account database on this platform
        logger.debug("falling back to the environment for the account name: %s", exc)
    return f"{account}@{socket.gethostname()}"


def ack_path(cfg: config.Config) -> Path:
    """Where the acknowledgment lives, resolved through the state inventory."""
    return config.state_path(ACK_KEY, cfg)


def _shown_ages(cfg: config.Config, now: datetime) -> tuple[ShownAge, ...]:
    """The backup ages, read from the FACT file rather than from the backup module.

    ``core.backup_facts`` already answers this question and already explains why
    it is a file and not a call: the backup module is opt-in, so importing it
    here would make a slim install raise inside the warning that runs immediately
    before the riskiest operation in the product. Asking it a second way would
    give two answers to one question, which is the drift this whole layer exists
    to remove.

    AN UNREADABLE FACT FILE REFUSES RATHER THAN SHOWING NOTHING. Returning an
    empty tuple would write an acknowledgment whose ``shown`` list is empty,
    which is byte for byte what a library declaring no portions at all would
    write, and ``backup_facts`` argues at length that "could not read" must never
    collapse into any other answer because the remedies differ. It matters more
    here than anywhere: this record is the evidence that a person decided, and an
    acknowledgment with no age is a click rather than a decision. An ABSENT file
    is untouched by this and still mints normally, as every library does before
    its first backup.

    AND THE REMEDY TRAVELS, which this function used to argue for and then not
    do. It named ``REPAIR_BACKUP_FACTS`` unconditionally, so the paragraph above
    was true of the refusal and false of the act it offered: a person whose
    configuration directory this account cannot traverse was told to repair or
    reset the record of when their music was last protected, over a file that
    was very likely intact, in the refusal standing immediately before the
    riskiest operation in the product. ``read_facts`` distinguishes a permission
    from a corruption from a newer schema at the raise site, and ``cli.doctor``
    and the backup shell both carry that through already. This is the third
    consumer joining them, spelled the way they spell it.
    """
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
            f"the backup ages this acknowledgment has to show cannot be read: "
            f"{exc}. Recording an acknowledgment now would say a person was shown "
            f"a clean sheet they were never shown",
            remedy=Remedy(str(exc.remedy)),
            scope=Scope.RUN,
            detail={"path": str(exc.path), "library": str(cfg.library.root)},
        ) from exc
    return tuple(
        ShownAge(
            portion=str(entry.portion),
            state=str(entry.state),
            age_seconds=entry.age.total_seconds() if entry.age is not None else None,
            completed_at=(
                entry.completed_at.isoformat() if entry.completed_at is not None else None
            ),
        )
        for entry in reported
    )


def record_acknowledgment(
    cfg: config.Config,
    *,
    now: datetime | None = None,
    validity: timedelta = DEFAULT_ACK_VALIDITY,
    terminal: Callable[[], bool] | None = None,
) -> Acknowledgment:
    """Mint the acknowledgment. A separate act from answering it, by a person.

    ``terminal`` is a seam so the battery can drive both sides of the check
    without a terminal and without one being absent. It is NOT an override: it
    answers "is there a terminal", and a caller that lies about that has not
    supplied an acknowledgment, it has supplied a different answer to a question
    the record still records honestly.

    THERE IS NO ACTOR PARAMETER, and there is no affirmative parameter either.
    Both absences are the point: a session consults this record, so anything that
    let the invocation assert its own way past it would put the gate under the
    control of the thing it gates.
    """
    moment = now or datetime.now(timezone.utc)
    probe = terminal or has_controlling_terminal
    if not probe():
        raise refuse(
            "backup-acknowledgment-no-terminal",
            "this invocation has no controlling terminal, so there is nobody here "
            "to acknowledge that the database and the music files are backed up; "
            "the acknowledgment is recorded by a person and consulted by the run",
            remedy=Remedy.ACKNOWLEDGE_BACKUP,
            scope=Scope.RUN,
            detail={"library": str(cfg.library.root)},
        )
    acknowledgment = Acknowledgment(
        actor=derive_actor(),
        recorded_at=moment,
        expires_at=moment + validity,
        shown=_shown_ages(cfg, moment),
    )
    config.atomic_write_bytes(
        json.dumps(acknowledgment.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n",
        ack_path(cfg),
    )
    return acknowledgment


def read_acknowledgment(cfg: config.Config) -> Acknowledgment | None:
    """The recorded acknowledgment, or None when this library has none.

    Absent is normal and is not an error: it is the state of every library before
    a person has answered once. A file that exists and cannot be understood IS an
    error, for the same reason the backup fact file treats one that way: reporting
    a damaged record as an absent one sends the user to redo something that is
    already done, and hides the thing that is actually broken.
    """
    try:
        raw = ack_path(cfg).read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        # NOT "exists and could not be read". Absent is caught above by its own
        # class, and everything reaching here is a read that did not happen: an
        # untraversable parent raises exactly this and establishes nothing about
        # what is under it. The same sentence is written one module over, in
        # ``backup_facts``, for the same reason.
        raise refuse(
            "internal-error",
            f"the backup acknowledgment could not be read, and whether it is "
            f"even there was not established: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            detail={"path": str(ack_path(cfg))},
        ) from exc
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise refuse(
            "internal-error",
            f"the backup acknowledgment is not readable as JSON: {exc}",
            remedy=Remedy.REPORT_DEFECT,
            detail={"path": str(ack_path(cfg))},
        ) from exc
    return Acknowledgment.from_json(data)


def assert_backup_acknowledged(
    cfg: config.Config, *, now: datetime | None = None
) -> Acknowledgment:
    """Consult the RECORD. Never an assertion made on this command line (R34).

    Absent and expired are one refusal with one remedy, and they are one because
    the answer to both is the same act by the same person. What they are not is
    an affirmative anything can supply: there is no parameter here that says yes,
    and the gate deliberately has no way to be told to skip itself.
    """
    moment = now or datetime.now(timezone.utc)
    acknowledgment = read_acknowledgment(cfg)
    if acknowledgment is not None and acknowledgment.valid_at(moment):
        return acknowledgment
    recorded = acknowledgment.recorded_at.isoformat() if acknowledgment else None
    raise refuse(
        "backup-acknowledgment-missing",
        (
            "this destructive session has no backup acknowledgment within its "
            "validity window"
            + (f"; the last one was recorded at {recorded}" if recorded else "")
        ),
        remedy=Remedy.ACKNOWLEDGE_BACKUP,
        scope=Scope.SESSION,
        detail={
            "library": str(cfg.library.root),
            "recorded_at": recorded,
            "expired": acknowledgment is not None,
        },
    )


# ---------------------------------------------------------------------------
# The volume gate
# ---------------------------------------------------------------------------

#: Which refusal slug each mount verdict raises. A TABLE rather than a chain of
#: branches so that a state added to the mount vocabulary with no entry here
#: fails a test instead of falling through to a default, which is how a new
#: refusal ends up wearing an unrelated code.
_MOUNT_REASONS: Mapping[preflight.MountState, str] = MappingProxyType(
    {
        preflight.MountState.NOT_MOUNTED: "library-volume-unmounted",
        preflight.MountState.LIBRARY_PATH_MISSING: "library-volume-unmounted",
        preflight.MountState.MOUNTED_ELSEWHERE: "library-volume-mismatch",
        preflight.MountState.FOREIGN_VOLUME: "library-volume-mismatch",
        preflight.MountState.IDENTITY_UNAVAILABLE: "library-volume-mismatch",
        preflight.MountState.IDENTITY_NOT_RECORDED: "library-volume-mismatch",
    }
)


def assert_volume_identity(
    cfg: config.Config,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> preflight.MountStatus:
    """Refuse unless the configured path holds the volume this library was set up on.

    Bound at DESTRUCTIVE strength, which is the only setting that makes an
    unreadable identity fatal. A read-only workflow on a platform with no
    identity adapter may proceed, because its worst case is a wrong report; this
    one may not, because its worst case is deleted music.

    The precondition layer raises its own exception type carrying no reason slug
    and no exit code, so it is converted here. Letting it escape would give one
    condition two identities at the process boundary, which is exactly the
    collapse the cause type exists to prevent.
    """
    try:
        return preflight.assert_library_volume(
            cfg.library.root,
            cfg.library.volume_id,
            destructive=True,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
    except preflight.LibraryVolumeError as exc:
        reason = _MOUNT_REASONS.get(exc.status.state, "library-volume-mismatch")
        raise refuse(
            reason,
            f"{exc.detail}, so this destructive session refuses before it "
            f"resolves a single path",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            scope=Scope.RUN,
            detail={
                "state": str(exc.status.state),
                "configured_root": str(exc.status.configured_root),
                "recorded_identity": exc.status.recorded_identity,
                "observed_identity": exc.status.observed_identity,
            },
        ) from exc


# ---------------------------------------------------------------------------
# The three gates
# ---------------------------------------------------------------------------


class Intent(StrEnum):
    """What a destructive session is FOR. Two answers, differing on exactly one gate.

    NOT A FLAG AND NOT AN OVERRIDE. The volume assertion, the acknowledgment and
    the lock apply to both answers unchanged: a recovery still has to be the
    right disk, still has to be acknowledged by a person, and still has to be the
    only session running. The single difference is the unresolved-session latch,
    and the reason is that the latch's own remedy is a recovery.

    A latch that condemned its own remedy would be a library with no exit. The
    refusal a ``committed-unverified`` session raises names
    ``restore-from-snapshot``, and a restore is itself a destructive session, so
    without this declaration the product tells a user to restore and then refuses
    the restore, with the only way out being to hand-edit a file in the log.
    """

    WRITE = "write"
    RECOVERY = "recovery"


@dataclass(frozen=True, slots=True)
class Gates:
    """What passing the gates established, handed to the body of the session."""

    workflow: str
    lock: Path
    acknowledgment: Acknowledgment
    volume: preflight.MountStatus
    intent: Intent = Intent.WRITE


def assert_no_unresolved_session(cfg: config.Config) -> None:
    """Refuse every further write while a session ended ``committed-unverified``.

    Post-commit rollback does not exist. A commit whose read-back disagreed left
    a library nobody can vouch for, and the only honest thing to do with the next
    write is refuse it until a person has looked. Enforced HERE, at the gate
    every destructive session passes through, rather than in each workflow: a
    refusal a caller can forget is a refusal that is eventually forgotten.

    IT READS THE LOG STRICTLY, which is the difference between this and every
    reporting caller. An entry this build cannot parse is counted, not skipped:
    a gate whose scan silently drops what it cannot read fails OPEN, so bumping
    the schema version on one file, or a state value a later build introduced,
    would make an unresolved commit vanish from the scan and admit the next
    destructive session against a library nobody can vouch for.
    """
    parsed, unreadable = scan_log(cfg)
    unresolved = [
        record for record in parsed if record.state is SessionState.COMMITTED_UNVERIFIED
    ]
    if unresolved:
        first = unresolved[0]
        raise refuse(
            "session-committed-unverified",
            f"session {first.session_id} committed and its read-back through a "
            f"fresh connection disagreed, so what this library holds cannot be "
            f"vouched for; every further write is refused until a person resolves "
            f"it. A recovery is not a further write and is not refused here",
            remedy=Remedy.RESTORE_FROM_SNAPSHOT,
            scope=Scope.RUN,
            detail={
                "sessions": [record.session_id for record in unresolved],
                "snapshot_path": first.snapshot_path,
                "change": first.change.to_json(),
            },
        )
    if unreadable:
        raise refuse(
            "internal-error",
            f"the session log holds {len(unreadable)} entr"
            + ("y" if len(unreadable) == 1 else "ies")
            + " this build cannot read, so this gate cannot vouch that no session "
            "ended unresolved; refusing rather than writing against a log it "
            "cannot read",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            detail={"unreadable": [str(path) for path in unreadable]},
        )


def resolve_unverified_session(
    session_id: str, cfg: config.Config, *, now: datetime | None = None
) -> SessionRecord:
    """Close one ``committed-unverified`` record, once a person has dealt with it.

    THE LATCH SURVIVES ITS OWN REMEDY, which is the whole reason this is a
    separate act. The session log is declared ``SURVIVES_ROLLBACK``, deliberately
    and for a good reason: rolling it back would erase the record of which
    sessions are restorable, which is exactly what a user needs in order to
    restore again. The consequence is that restoring the library from the capture
    the record names does not remove the record. Without this, a user who did
    precisely what the refusal asked would find the next write still refused,
    with the remedy already spent and nothing left to spend.

    It refuses on any other state. Ending somebody else's OPEN session from
    outside would release a capture a live run is still writing behind, and
    ending a CLOSED one is a no-op dressed as an action.
    """
    record = read_record(session_id, cfg)
    if record.state is not SessionState.COMMITTED_UNVERIFIED:
        raise refuse(
            "internal-error",
            f"session {session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.COMMITTED_UNVERIFIED)!r}; only a session that "
            f"committed behind a read-back that disagreed is resolved this way",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": session_id, "state": str(record.state)},
        )
    return close_session(record, cfg, state=SessionState.ABANDONED, now=now)


@contextmanager
def assert_gates(
    cfg: config.Config | None = None,
    *,
    workflow: str,
    intent: Intent = Intent.WRITE,
    now: datetime | None = None,
    lock: Path | str | None = None,
    holder: Holder | None = None,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    analysis_roots: Iterable[Path | str] = (),
) -> Iterator[Gates]:
    """The one entry point every destructive operation passes through (KTD24).

    Three refusals, three distinct codes, and nothing written on any of them:

    * a lock held elsewhere refuses in the library-busy class;
    * a missing or expired acknowledgment refuses in the acknowledgment class;
    * a volume whose recorded identity does not match refuses in the
      library-unavailable class.

    ``workflow`` is the caller's name for the operation and is recorded in the
    session log. It arrives as a parameter because this layer names no verb (D2);
    the layer that owns verb names supplies one.

    ``intent`` is a DECLARATION, not an override, and it changes exactly the two
    LATCHES: a ``RECOVERY`` session is held neither by the unresolved-session
    latch nor by the unreconciled-restore latch, because a recovery is what each
    of those refusals names as its remedy. See :class:`Intent`. All three of the
    gates below apply to it unchanged.

    THE ORDER IS ARGUED IN THE MODULE DOCSTRING and is not the order the plan
    lists them in. Volume, then acknowledgment, then lock: the first two read
    only, and the third is the one that creates a file, so a refused session
    leaves the state tree byte for byte as it found it.

    ``analysis_roots`` arms the runtime half of R17's fifth surface for the body
    of this session: every rekordbox analysis file beneath those directories is
    fingerprinted before the body runs and compared afterwards, and a file that
    moved refuses. It is EMPTY by default and the caller names what it could
    touch, because the alternative is walking a whole music volume on every
    destructive session to watch files nothing intends to open. That default is
    a softening path, so it is closed the way P5 says to close one: a guard
    registered against the unit that owes the roots, not a sentence in a
    docstring hoping somebody supplies them.
    """
    resolved = cfg if cfg is not None else config.load()
    volume = assert_volume_identity(
        resolved,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )
    if intent is not Intent.RECOVERY:
        assert_no_unresolved_session(resolved)
        # The second latch, and it lives HERE for the reason the first one does:
        # a refusal a caller can forget is a refusal that is eventually
        # forgotten. A restore that left effects it could not undo, or trees that
        # need rebuilding, refuses every ordinary destructive session until a
        # person has closed each one. Read-only work is untouched, because
        # nothing below this line runs for a caller that is not about to write.
        reconcile.assert_converged(resolved)
    acknowledgment = assert_backup_acknowledged(resolved, now=now)
    watched = list(analysis_roots)
    with session_lock(resolved, path=lock, holder=holder) as held:
        with analysis_files_unmoved(watched) if watched else nullcontext():
            yield Gates(
                workflow=workflow,
                lock=held,
                acknowledgment=acknowledgment,
                volume=volume,
                intent=intent,
            )


# ---------------------------------------------------------------------------
# The session boundary: one source per run (R29)
# ---------------------------------------------------------------------------


def open_session(
    cfg: config.Config,
    *,
    workflow: str,
    sources: Sequence[str] = (),
    session_id: str | None = None,
    actor: str | None = None,
    acknowledged_at: str | None = None,
    now: datetime | None = None,
) -> SessionRecord:
    """Start a session record and persist it before any work happens.

    Persisted UP FRONT rather than at the end, because the record is what a
    recovery reads and a run that crashed is exactly the run with no clean end.
    An open record also protects its capture from pruning the moment it exists,
    which is the property R30 turns on.
    """
    record = SessionRecord(
        session_id=session_id or new_session_id(now),
        workflow=workflow,
        started=output.timestamp(now),
        state=SessionState.OPEN,
        actor=actor,
        acknowledged_at=acknowledged_at,
        sources={source: str(SourceState.PENDING) for source in sources},
    )
    write_record(record, cfg)
    return record


def attach_capture(record: SessionRecord, capture_path: Path | str, cfg: config.Config) -> None:
    """Record which capture this session is the undo for, and persist it at once.

    Written the instant the capture exists rather than at the end of the session.
    The field is what the pruning scan reads, so a capture whose session has not
    recorded it yet is a capture retention is free to delete while the write it
    protects is still running.
    """
    record.snapshot_path = str(capture_path)
    write_record(record, cfg)


def commit_sources(
    record: SessionRecord,
    source_ids: Iterable[str],
    run_one: Callable[[str], ChangeSummary],
    *,
    cfg: config.Config,
) -> SessionRecord:
    """Run one source at a time, committing and recording each independently (R29).

    THREE PROPERTIES, and each one is a failure the source system has:

    * a source already marked committed is SKIPPED, so a resume neither redoes
      landed work nor needs the caller to remember what landed;
    * the record is persisted after every source, so "which landed" is a fact on
      disk rather than a value in a process that may not survive;
    * a refusal part way leaves the committed sources committed and REPORTS both
      halves, rather than failing the whole run and leaving a user to work out
      what happened by inspection.

    ``run_one`` returns the change summary for the source it committed. It raises
    to refuse, and whatever it raised is carried underneath the refusal this
    produces rather than replaced by it (KTD25).

    THE SCOPE IS WIDENED, NEVER NARROWED. This wrapper knows that ONE SOURCE
    refused and knows nothing about how much the underlying cause condemns, so it
    may add its own scope and may not replace a wider one. A drive that was
    ejected mid-run raises at ``Scope.RUN``; rewriting that to ``Scope.SOURCE``
    would tell the aggregate at boundary 4 that only this source is condemned,
    and the watermark it then advances for the sources beside it is advanced
    against a library that is no longer mounted.
    """
    for source in source_ids:
        if record.sources.get(source) == str(SourceState.COMMITTED):
            logger.info("source %s already committed in session %s", source, record.session_id)
            continue
        record.sources.setdefault(source, str(SourceState.PENDING))
        try:
            change = run_one(source)
        except CratekitError as exc:
            record.sources[source] = str(SourceState.REFUSED)
            write_record(record, cfg)
            raise CratekitError(
                Cause(
                    reason=exc.cause.reason,
                    message=(
                        f"session {record.session_id} refused at source {source!r}; "
                        f"sources already committed are untouched"
                    ),
                    remediation=exc.cause.remediation,
                    scope=widest_scope(exc.cause.scope, Scope.SOURCE),
                    retryable=exc.cause.retryable,
                    origin=(*exc.cause.origin, "session"),
                    detail={
                        "session_id": record.session_id,
                        "refused_source": source,
                        "committed": list(record.committed_sources()),
                        "remaining": list(record.remaining_sources()),
                    },
                    inner=exc.cause,
                )
            ) from exc
        record.sources[source] = str(SourceState.COMMITTED)
        record.change = record.change.merged(change)
        write_record(record, cfg)
    return record


def close_session(
    record: SessionRecord,
    cfg: config.Config,
    *,
    state: SessionState = SessionState.CLOSED,
    intent: Intent = Intent.WRITE,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    now: datetime | None = None,
) -> SessionRecord:
    """End a session, releasing the capture it referenced.

    Only a TERMINAL state releases a capture, so this refuses to close into a
    non-terminal one. Closing into ``awaiting-import`` would say the session is
    over while a person still has something to do, and would make its capture
    prunable at the moment it is most likely to be needed.

    CLOSING IS GATED ON CONVERGENCE AND ABANDONING IS NOT, which is the same
    split ``close_run`` already makes for the same reason. Closing is the CLAIM
    that the run finished, and a run cannot have finished into a library holding
    a restore nobody reconciled; abandoning is the opposite claim, and gating it
    would leave somebody with a run they can neither finish nor give up on.

    The gate is not vacuous even though the library lock is exclusive, and the
    reason is worth stating because the obvious reading is that it must be. A
    session that ended ``awaiting-import`` is OPEN across processes with the lock
    long since released, so a restore can land between that session's write and
    its close. That close is exactly the one this refuses: the export it is
    reporting as imported was written against a library that has since been
    rolled back underneath it.

    ``intent`` selects, and does not override. A RECOVERY closes normally,
    because a restore is what the refusal names as its own remedy and a latch
    that condemned its remedy leaves a library with no exit but a hand-edited
    file.

    THE VOLUME IS ASSERTED BEFORE THE CONVERGENCE GATE, and it was not, which made
    that gate silently permissive in one specific state. ``assert_gates`` asserts
    the volume first and every other reader of the reconciliation record sits
    behind it; this close does not go through ``assert_gates`` at all. With the
    library volume gone, the record's path simply does not exist, and the reader
    cannot tell that from a library with nothing recorded yet, so an open
    reconciliation marker vanished and the close it should have refused was
    allowed. The reader cannot be made to tell the difference without the recorded
    volume identity, and this is where that identity is available. Asserted only on
    the gated path, because abandoning is deliberately not gated: gating it would
    leave somebody with a run they can neither finish nor give up on.
    """
    if state is SessionState.CLOSED and intent is not Intent.RECOVERY:
        assert_volume_identity(
            cfg,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
        reconcile.assert_converged(cfg)
    if state not in TERMINAL_STATES:
        raise refuse(
            "internal-error",
            f"{state!r} is not a terminal session state, so closing into it would "
            f"release a capture the session still references",
            remedy=Remedy.REPORT_DEFECT,
            detail={"state": str(state), "session_id": record.session_id},
        )
    record.state = state
    record.ended = output.timestamp(now)
    write_record(record, cfg)
    return record


# ---------------------------------------------------------------------------
# The un-imported XML output (a first-class run state)
# ---------------------------------------------------------------------------


def pending_import(
    record: SessionRecord,
    *,
    artifact: Path | str,
    summary: str,
    verify_verb: str,
    blocks: Sequence[str] = (),
    steps: Sequence[str] = (),
) -> output.PendingHumanAction:
    """Build the pending action that says an XML output is waiting to be imported.

    It uses the SAME type the command-line layer already puts on a run record and
    the same ``blocks`` tuple its own check already enforces, rather than a
    parallel mechanism. Two mechanisms for one idea is how the source system ends
    up saying "import this" eleven different ways and then forgetting.

    Every verb name arrives as a parameter. This layer must not spell one (D2),
    and the layer that owns them can.
    """
    return output.PendingHumanAction(
        kind="rekordbox_import",
        id=output.new_pending_id(record.session_id),
        summary=summary,
        verify_verb=verify_verb,
        artifact=str(artifact),
        steps=tuple(steps),
        blocks=tuple(blocks),
    )


def mark_awaiting_import(
    record: SessionRecord, pending: output.PendingHumanAction, cfg: config.Config
) -> SessionRecord:
    """Move a session into the un-imported state and persist it.

    THE DERIVED INVARIANT, stated here because it is the reason this state
    exists: within one run, XML surfaces are strictly upstream of database
    surfaces, and a database surface is never written for a row that does not yet
    exist. The XML is what CREATES the row, and a person performs that import. So
    a run holding an un-imported XML output has, by construction, database
    surfaces it cannot write yet, and writing them anyway would address rows the
    database does not contain.
    """
    record.state = SessionState.AWAITING_IMPORT
    record.pending = pending
    write_record(record, cfg)
    return record


def assert_database_surface_allowed(record: SessionRecord) -> None:
    """Refuse a database write while this run's XML output has not been imported.

    See :func:`mark_awaiting_import` for the invariant. The refusal is in the
    pending-human class rather than a failure class, because nothing is broken:
    the tool has finished its half and a person has not yet finished theirs.
    """
    if record.state is not SessionState.AWAITING_IMPORT:
        return
    pending = record.pending
    raise refuse(
        "awaiting-import",
        f"session {record.session_id} has an XML output that has not been "
        f"imported, and a database surface is never written for a row that does "
        f"not yet exist",
        remedy=Remedy.COMPLETE_PENDING_ACTION,
        steps=tuple(pending.steps) if pending is not None else (),
        scope=Scope.RUN,
        detail={
            "session_id": record.session_id,
            "pending_id": pending.id if pending is not None else None,
            "verify_verb": pending.verify_verb if pending is not None else None,
            "artifact": pending.artifact if pending is not None else None,
        },
    )


# ---------------------------------------------------------------------------
# The post-commit read-back (AE13)
# ---------------------------------------------------------------------------


def _chained(outer: Cause | None, beneath: Cause | None) -> Cause | None:
    """Hang one cause at the TAIL of another's chain, displacing nothing.

    A cause that collapses at any hop cannot be recovered downstream, and the
    cheap way to collapse one is to attach a second fact where a first already
    sits. Appending keeps both, in the order a reader wants them: most specific
    first, most general last.
    """
    if outer is None:
        return beneath
    if beneath is None:
        return outer
    return replace(outer, inner=_chained(outer.inner, beneath))


def verify_commit(
    record: SessionRecord,
    cfg: config.Config,
    *,
    expect: Callable[[Any], bool],
    reopen: Callable[[], Any] | None = None,
    now: datetime | None = None,
) -> bool:
    """Re-read what was committed THROUGH A FRESH CONNECTION, and refuse if it disagrees.

    The existing smoke test re-reads inside the session that wrote, so it cannot
    see a stale view by construction: the session's own cache answers before the
    database does. A second connection is the only thing that reads what the file
    actually holds.

    CLOSING A DATABASE DOES NOT RELEASE IT. The binding closes its session and
    leaves the engine's pooled connection open, so the process still holds the
    file and the companion files beside it, and a restore over them then produces
    an input-output error against a database that is perfectly intact. The
    release goes through the writer's own full close for that reason.

    ON DISAGREEMENT there is nothing to roll back, because post-commit rollback
    does not exist. So the session ends ``committed-unverified``: no watermark
    advances, nothing is marked done, the record keeps its capture path and its
    change summary, and every further write against this library refuses until a
    person resolves it. Whether rekordbox is running is re-asserted and REPORTED
    SEPARATELY, carried underneath this cause rather than replacing it, because
    "the read-back disagreed" and "the application is open" are different facts
    with different fixes and the second may well explain the first.

    A READ-BACK THAT COULD NOT RUN IS A THIRD FACT and it travels too, as the
    first link of that same chain. It still ends the session unverified, because
    a commit landed and nothing has confirmed what it landed; what it must not do
    is arrive as "the database disagrees" when the truth is that the volume was
    ejected, the pin drifted, or the file could not be opened at all. Those are
    recoverable and this one is not, and collapsing the first into the second is
    the exact loss the cause chain exists to prevent.
    """
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg))
    agreed = False
    handle = None
    failure: Cause | None = None
    try:
        handle = open_fresh()
        agreed = bool(expect(handle))
    except CratekitError as exc:
        # A TYPED read-back failure is the most specific fact in the whole
        # chain and is the one that says what to do. Logging it and throwing it
        # away would report "the drive is unplugged" as "the database disagrees",
        # which is a recoverable condition wearing an unrecoverable one's face,
        # and is exactly the collapse KTD25 exists to stop.
        logger.warning("the post-commit read-back could not run: %s", exc)
        failure = exc.cause
    except Exception as exc:  # noqa: BLE001 - a read-back that cannot run has not agreed
        logger.warning("the post-commit read-back could not run: %s", exc)
        failure = Cause(
            reason="internal-error",
            message=f"the post-commit read-back could not run: {exc}",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            scope=Scope.RUN,
            origin=("session",),
            detail={"session_id": record.session_id, "error": str(exc)},
        )
    finally:
        if handle is not None:
            rb_writer.close_db(handle)

    if agreed:
        return True

    # BOTH facts, in one chain, and neither displacing the other. A read-back
    # that could not run and an application holding the database open are
    # different facts with different fixes, and the second may well explain the
    # first. The probe goes at the TAIL so a typed read-back failure keeps
    # whatever chain it arrived with.
    inner: Cause | None = failure
    try:
        rb_writer.assert_rekordbox_closed("verifying a commit")
    except CratekitError as exc:
        inner = _chained(inner, exc.cause)

    record.state = SessionState.COMMITTED_UNVERIFIED
    record.ended = output.timestamp(now)
    write_record(record, cfg)
    raise refuse(
        "session-committed-unverified",
        f"session {record.session_id} committed and the read-back through a fresh "
        f"connection did not agree; no watermark has advanced and nothing is "
        f"marked done",
        remedy=Remedy.RESTORE_FROM_SNAPSHOT,
        scope=Scope.RUN,
        detail={
            "session_id": record.session_id,
            "snapshot_path": record.snapshot_path,
            "change": record.change.to_json(),
        },
        inner=inner,
    )


# ---------------------------------------------------------------------------
# The runtime half of R17's fifth surface: analysis files must not move
# ---------------------------------------------------------------------------

#: The names rekordbox gives the per-track analysis files, WIDER than the
#: binding's own pattern on purpose.
#:
#: The binding recognises three of them. R17's fifth surface names four, and the
#: fourth is a real grid-bearing file, so recognising only what the binding
#: recognises would leave one of the four unwatched. A test asserts the two
#: directions that matter: every name the binding matches this also matches, and
#: this additionally matches the fourth. Being WIDER is safe here, because the
#: consequence of watching one extra file is nothing, and the consequence of
#: missing one is a rewritten grid nobody notices (P4).
ANLZ_NAME_PATTERN = re.compile(r"^ANLZ[0-9]{4}\.(?:DAT|EXT|2EX|3EX)$", re.IGNORECASE)


def is_analysis_file(path: Path | str) -> bool:
    """Whether a path names one of rekordbox's per-track analysis files."""
    return bool(ANLZ_NAME_PATTERN.match(Path(path).name))


def analysis_files_under(roots: Iterable[Path | str]) -> tuple[Path, ...]:
    """Every analysis file beneath the given directories, sorted.

    DERIVED BY WALKING (P3). A session that listed the files it intended to touch
    would watch exactly the ones it already knew about, and the write this guard
    exists to catch is the one nobody intended: a rename helper in the binding
    rewrites every analysis file for a track as a side effect, so the file that
    moves is precisely the one a hand-list omits.
    """
    found: list[Path] = []
    for root in roots:
        base = Path(root)
        if base.is_file():
            if is_analysis_file(base):
                found.append(base)
            continue
        if not base.is_dir():
            continue
        for current, _directories, files in os.walk(base):
            for name in files:
                if is_analysis_file(name):
                    found.append(Path(current) / name)
    return tuple(sorted(set(found)))


def fingerprint_analysis_files(paths: Iterable[Path | str]) -> dict[str, tuple[int, int]]:
    """Modification time and size per analysis file, as a comparable mapping.

    The size travels with the time because a filesystem's timestamp granularity
    is not infinite: a rewrite inside one tick of the clock leaves the time alone,
    and a grid rewrite almost always changes the length of the tag it lives in.
    Two weak signals that fail in different ways beat one that fails silently.
    """
    out: dict[str, tuple[int, int]] = {}
    for path in paths:
        target = Path(path)
        try:
            stat = target.stat()
        except OSError:
            continue
        out[str(target)] = (stat.st_mtime_ns, stat.st_size)
    return out


def analysis_drift(
    before: Mapping[str, tuple[int, int]], after: Mapping[str, tuple[int, int]]
) -> tuple[str, ...]:
    """Every analysis file that changed, vanished, or appeared between two reads.

    All three count. A modified file is the obvious one; a vanished file is a
    grid destroyed rather than rewritten; and an appearing file is rekordbox
    analysing while this session ran, which the process guard is supposed to have
    made impossible and which is therefore worth surfacing rather than ignoring.
    """
    problems: list[str] = []
    for path, signature in sorted(before.items()):
        found = after.get(path)
        if found is None:
            problems.append(f"{path} was removed")
        elif found != signature:
            problems.append(f"{path} was modified")
    for path in sorted(set(after) - set(before)):
        problems.append(f"{path} appeared")
    return tuple(problems)


@contextmanager
def analysis_files_unmoved(roots: Iterable[Path | str]) -> Iterator[dict[str, tuple[int, int]]]:
    """Refuse if any analysis file under ``roots`` moved while the body ran.

    THIS IS THE HALF THE SOURCE SCAN CANNOT DO. The name scan in
    ``tests/test_no_beatgrid_ever.py`` forbids every symbol that serialises one of
    these files, and reading them stays legal by decision, so a grid rewritten
    through a handle the binding already returned names none of the forbidden
    symbols and is invisible to it. This compares the files themselves.

    The refusal is deliberate about its remedy: a grid that has already been
    rewritten cannot be un-rewritten from here, and the capture the session is
    running behind is the undo.

    THE COMPARISON RUNS ON BOTH PATHS, and the failing one is the path that
    matters more. A body that raised is a body the user will RETRY, so a grid
    rewritten before an unrelated refusal would be re-rewritten on the next
    attempt and never once reported. Putting the comparison after a bare yield
    would skip it for exactly those runs: the guard would watch only the sessions
    that had nothing to hide. Whatever the body raised is carried underneath this
    refusal rather than replaced by it, because "the smoke test failed" and "a
    beat grid moved" are two facts and only one of them is the inviolable rule.
    """
    watched = list(analysis_files_under(roots))
    before = fingerprint_analysis_files(watched)
    raised: BaseException | None = None
    try:
        yield before
    except BaseException as exc:
        raised = exc
        raise
    finally:
        drift = analysis_drift(
            before, fingerprint_analysis_files(analysis_files_under(roots))
        )
        if drift:
            refusal = refuse(
                "anlz-modified",
                "rekordbox analysis files moved during this session, and the beat "
                "grid lives in those files:\n  - " + "\n  - ".join(drift),
                remedy=Remedy.RESTORE_FROM_SNAPSHOT,
                scope=Scope.SESSION,
                detail={"changed": list(drift), "watched": len(watched)},
                inner=raised.cause if isinstance(raised, CratekitError) else None,
            )
            if raised is not None:
                raise refusal from raised
            raise refusal


__all__ = [
    "ACK_KEY",
    "ACK_SCHEMA_VERSION",
    "ANLZ_NAME_PATTERN",
    "DEFAULT_ACK_VALIDITY",
    "LOG_SCHEMA_VERSION",
    "RUN_STATE_VOCABULARY",
    "SNAPSHOT_KEY",
    "STATE_KEY",
    "TERMINAL_STATES",
    "UNKNOWN_IDENTITY",
    "Acknowledgment",
    "ChangeSummary",
    "Gates",
    "Holder",
    "Intent",
    "SessionComposition",
    "SessionRecord",
    "SessionState",
    "ShownAge",
    "SourceState",
    "TreeChange",
    "ack_path",
    "analysis_drift",
    "analysis_files_under",
    "analysis_files_unmoved",
    "assert_backup_acknowledged",
    "assert_database_surface_allowed",
    "assert_gates",
    "assert_no_unresolved_session",
    "assert_volume_identity",
    "attach_capture",
    "boot_identity",
    "close_session",
    "commit_sources",
    "current_holder",
    "derive_actor",
    "fingerprint_analysis_files",
    "has_controlling_terminal",
    "holder_alive",
    "is_analysis_file",
    "lock_path",
    "log_dir",
    "log_path",
    "mark_awaiting_import",
    "new_session_id",
    "open_session",
    "pending_import",
    "process_exists",
    "process_started",
    "read_acknowledgment",
    "read_lock_holder",
    "read_record",
    "record_acknowledgment",
    "records",
    "release_stale_lock",
    "resolve_unverified_session",
    "scan_log",
    "session_lock",
    "verify_commit",
    "write_record",
]
