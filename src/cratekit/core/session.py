"""The destructive-session boundary: the lock, the acknowledgment, and the log.

1. **Three gates on every destructive session** (KTD24). The trigger is
   destruction, not a database write, because a restore destroys a library
   while writing no row.
2. **A library-scoped lock** (KTD21, KTD17), beside the library so a second
   machine contends with the first. The holder is named by host, machine, boot,
   pid and process start time, since a bare pid is reused and machine-local.
3. **A session log the pruning scan can read.** The vocabulary is
   :data:`RUN_STATE_VOCABULARY`, proven by driving a real record through the
   writer's scan, because a scan that matches nothing fails silently.
4. **An acknowledgment an agent cannot mint for itself** (R34, KTD18). Minted by
   a person at a terminal; no flag, config key or environment variable
   satisfies it. One exception (U138): a gate answered by the actor ``session``
   may mint without a terminal while every backup portion reads under five days.

THE ORDER OF THE THREE GATES IS LOAD BEARING: the volume first, since resolving
paths on the wrong volume is already the damage; the acknowledgment second, a
pure read; the lock last, the only gate that writes, so a refused session
writes nothing.

A destructive session fingerprints every analysis file it could touch before
the write and refuses if one moved, the runtime half the beat grid source scan
cannot see.

LAYER: infrastructure. It names no verb and carries remediation tokens only (D2).
"""

from __future__ import annotations

import fnmatch
import functools
import hashlib
import json
import logging
import math
import os
import re
import socket
import subprocess
import sys
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli import output
from cratekit.core import backup_facts, config, locations, preflight, rb_writer, reconcile
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
# The session log's vocabulary, spelled the way ``rb_writer``'s scan expects.
# ---------------------------------------------------------------------------


class SessionState(StrEnum):
    """Where one destructive session got to. Five answers, and only two are ends.

    ``AWAITING_IMPORT`` is not finished, or the next run writes over the node the
    import was meant to create. ``COMMITTED_UNVERIFIED`` is not terminal, so its
    capture stays protected and the next write refused until a person resolves it.
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

#: The ``detail`` key naming the process that owns an open record.
HOLDER_KEY = "holder"

#: What the writer's snapshot-protection scan reads, derived from the above.
RUN_STATE_VOCABULARY = rb_writer.RunStateVocabulary(
    state_key=STATE_KEY,
    terminal_states=frozenset(str(state) for state in TERMINAL_STATES),
    snapshot_key=SNAPSHOT_KEY,
)

#: Bumped only when the log's on-disk shape changes incompatibly.
LOG_SCHEMA_VERSION = 1


class SourceState(StrEnum):
    """Per-source progress inside one session (R29), so a resume neither redoes
    committed work nor skips uncommitted work."""

    PENDING = "pending"
    COMMITTED = "committed"
    REFUSED = "refused"


# ---------------------------------------------------------------------------
# The change summary
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TreeChange:
    """What one session did to one tree, in counts.

    ``tree`` is a stable identifier, never a display name, which a rename would
    orphan silently (R19).
    """

    tree: str
    created: int = 0
    updated: int = 0
    #: Rows removed from the collection (U288), written only when not zero so
    #: older records read back unchanged.
    removed: int = 0

    def to_json(self) -> dict[str, Any]:
        shown: dict[str, Any] = {"tree": self.tree, "created": self.created, "updated": self.updated}
        if self.removed:
            shown["removed"] = self.removed
        return shown

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> TreeChange:
        return cls(
            tree=str(data["tree"]),
            created=int(data.get("created", 0)),
            updated=int(data.get("updated", 0)),
            removed=int(data.get("removed", 0)),
        )


@dataclass(frozen=True, slots=True)
class ChangeSummary:
    """Every tree a session touched, with per-tree counts, because a restore asks
    a person to approve discarding work tree by tree (U32)."""

    trees: tuple[TreeChange, ...] = ()

    @property
    def created(self) -> int:
        return sum(entry.created for entry in self.trees)

    @property
    def updated(self) -> int:
        return sum(entry.updated for entry in self.trees)

    def merged(self, other: ChangeSummary) -> ChangeSummary:
        """Combine two summaries, adding counts for a tree both name, sorted so
        the recorded bytes do not depend on source order."""
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
                    removed=seen.removed + entry.removed,
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

    Mutable, and every transition is persisted as it happens, because a record
    written only on a clean finish is absent for the runs that need recovery.
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
    """Where session records live, through ``state_path`` and never composed here,
    so it is the same directory the writer's protection scan reads."""
    return config.state_path("session_log", cfg)


#: Everything outside this whitelist is replaced before an identifier becomes a
#: filename, since a blacklist is wrong on the next filesystem.
_UNSAFE_IN_A_FILENAME = re.compile(r"[^A-Za-z0-9._-]")


def log_path(session_id: str, cfg: config.Config) -> Path:
    """One session's record, under a name every filesystem this library can sit on accepts.

    The identifier keeps its colons; the filename may not, since exFAT and FAT
    reject them. Sanitising also stops a supplied separator composing a record
    outside the directory the pruning scan reads.
    """
    return log_dir(cfg) / f"{_UNSAFE_IN_A_FILENAME.sub('-', session_id)}.json"


def new_session_id(now: datetime | None = None) -> str:
    """A sortable identifier for one session, in the run record's identifier space."""
    return output.new_run_id(now)


def write_record(record: SessionRecord, cfg: config.Config) -> Path:
    """Persist one session record atomically, owner-readable only (P1), since a
    torn record is a session nobody can restore from."""
    path = log_path(record.session_id, cfg)
    config.atomic_write_bytes(
        json.dumps(record.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n", path
    )
    return path


def read_record(session_id: str, cfg: config.Config) -> SessionRecord:
    """Read one session record, or refuse naming the session.

    Absence and a refused read are two answers, so they get two handlers.
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


def _listed(directory: Path) -> list[str] | None:
    """The names in ``directory``, ``None`` when it is not there; raises when it is there and refused.

    Asked of the listing itself, since a glob and ``isdir`` both read a refused
    directory as empty or absent.
    """
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return None
    except NotADirectoryError:
        if os.path.lexists(directory):
            raise
        return None


def log_unlisted(unreadable: Sequence[Path], cfg: config.Config) -> bool:
    """Whether the unread half :func:`scan_log` returned is the log itself, not a record in it."""
    return log_dir(cfg) in unreadable


def unread_clause(unreadable: Sequence[Path], cfg: config.Config) -> str:
    """The unread half as a refusal says it: the listing refused, or how many
    entries, so a permission problem is not reported as a damaged file."""
    if log_unlisted(unreadable, cfg):
        return "the session log exists and cannot be listed by this account"
    return (
        f"the session log holds {len(unreadable)} entr"
        + ("y" if len(unreadable) == 1 else "ies")
        + " this build cannot read"
    )


def scan_log(cfg: config.Config) -> tuple[tuple[SessionRecord, ...], tuple[Path, ...]]:
    """Read the log once and return BOTH halves: what parsed, and what did not.

    Reporting drops the unread half; a gate may not, or it fails open on a
    record a later build wrote. A log that is there and cannot be listed is
    returned as the log directory itself in the unread half (R-1255).
    """
    directory = log_dir(cfg)
    try:
        names = _listed(directory)
    except OSError as exc:
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), (directory,)
    if names is None:
        return (), ()
    entries = sorted(directory / name for name in names if fnmatch.fnmatchcase(name, "*.json"))
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

    An unreadable entry is skipped, a policy for reporting only, since a gate
    that borrowed it would fail open. A log that cannot be listed refuses
    rather than answering that no session is recorded (R-1255).
    """
    parsed, unreadable = scan_log(cfg)
    if log_unlisted(unreadable, cfg):
        raise refuse(
            "internal-error",
            f"{unread_clause(unreadable, cfg)}, so no session recorded in it can be "
            "read; refusing rather than answering that none is recorded",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            detail={"log": str(log_dir(cfg)), "unlisted": True},
        )
    return parsed


# ---------------------------------------------------------------------------
# The lock holder
# ---------------------------------------------------------------------------

#: Recorded in place of a value this platform cannot answer, so a degraded
#: identity is never read as a confident one. The kernel still does the exclusion.
UNKNOWN_IDENTITY = "unknown"


@dataclass(frozen=True, slots=True)
class Holder:
    """Who holds the session lock, identified across machines and restarts.

    ``machine`` tells apart machines sharing a host name, so a holder from this
    machine's previous boot can be judged gone (R-647); ``pid`` is reused after
    a restart, ``boot`` detects that, and ``started`` tells apart two processes
    given one pid in one boot. An unknown machine is never evidence a holder is gone.
    """

    host: str
    boot: str
    pid: int
    started: str
    machine: str = UNKNOWN_IDENTITY

    def to_json(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "machine": self.machine,
            "boot": self.boot,
            "pid": self.pid,
            "started": self.started,
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Holder:
        return cls(
            host=str(data.get("host", UNKNOWN_IDENTITY)),
            machine=str(data.get("machine", UNKNOWN_IDENTITY)),
            boot=str(data.get("boot", UNKNOWN_IDENTITY)),
            pid=int(data.get("pid", 0)),
            started=str(data.get("started", UNKNOWN_IDENTITY)),
        )

    def describe(self) -> str:
        return f"process {self.pid} on {self.host} (boot {self.boot}, started {self.started})"


def boot_identity() -> str:
    """This boot of this machine, or the declared unknown. Imports psutil lazily."""
    try:
        import psutil

        return f"{psutil.boot_time():.0f}"
    except Exception as exc:  # noqa: BLE001 - an unanswerable identity is not a failure
        logger.debug("boot identity is unavailable on this platform: %s", exc)
        return UNKNOWN_IDENTITY


#: The files a Linux machine keeps its identity in, the systemd one first.
_LINUX_MACHINE_ID_FILES = ("/etc/machine-id", "/var/lib/dbus/machine-id")

#: How the macOS hardware identity reads in the platform registry's output.
_IOREG_UUID = re.compile(r'"IOPlatformUUID"\s*=\s*"([^"]+)"')


def _raw_machine_identity() -> str | None:
    """The platform's own identifier for this machine, or None when it will not say."""
    if sys.platform == "darwin":
        completed = subprocess.run(
            ["/usr/sbin/ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        found = _IOREG_UUID.search(completed.stdout)
        return found.group(1) if found else None
    if sys.platform.startswith("linux"):
        for candidate in _LINUX_MACHINE_ID_FILES:
            try:
                text = Path(candidate).read_text().strip()
            except OSError:
                continue
            if text:
                return text
        return None
    if sys.platform == "win32":
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography"
        ) as key:
            return str(winreg.QueryValueEx(key, "MachineGuid")[0]) or None
    return None


@functools.cache
def machine_identity() -> str:
    """This machine, as an identity no other machine shares, or the declared unknown.

    Recorded as a digest, since it is only compared and a hardware serial does
    not belong in a record. Cached, since the macOS answer costs a subprocess.
    A cloned Linux image shares one identity, a case this narrows, not closes.
    """

    try:
        raw = _raw_machine_identity()
    except Exception as exc:  # noqa: BLE001 - an unanswerable identity is not a failure
        logger.debug("machine identity is unavailable on this platform: %s", exc)
        raw = None
    if not raw:
        return UNKNOWN_IDENTITY
    return hashlib.sha256(f"cratekit-machine:{raw}".encode()).hexdigest()[:32]


def process_started(pid: int) -> str:
    """When a process began, or the declared unknown, also for a process that
    does not exist; liveness is asked separately by :func:`process_exists`."""
    try:
        import psutil

        return f"{psutil.Process(pid).create_time():.3f}"
    except Exception as exc:  # noqa: BLE001 - see the docstring
        logger.debug("process start time is unavailable for %s: %s", pid, exc)
        return UNKNOWN_IDENTITY


def process_exists(pid: int) -> bool | None:
    """Whether a process with this identifier exists, or None when this cannot say.

    None is not False, or an unanswerable platform would clear a live holder's claim.
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
        machine=machine_identity(),
        boot=boot_identity(),
        pid=pid,
        started=process_started(pid),
    )


#: How far apart two readings of one boot's start may land, since a clock
#: adjustment moves the wall clock boot reading.
BOOT_DRIFT_SECONDS = 60.0


def _gone_since_an_earlier_boot(holder: Holder, reference: Holder) -> bool:
    """Whether a holder from another boot is provably from THIS machine's earlier one.

    Proven only when the machine identity is known and equal, the holder's boot
    is earlier past the drift margin, and no process with its pid runs at all
    (R-647). Start times are not compared, since a stepped clock shifts a live
    process's start time with the boot reading on Linux.
    """
    if UNKNOWN_IDENTITY in (holder.machine, reference.machine):
        return False
    if holder.machine != reference.machine:
        return False
    try:
        earlier_by = float(reference.boot) - float(holder.boot)
    except ValueError:
        return False
    if not math.isfinite(earlier_by) or earlier_by <= BOOT_DRIFT_SECONDS:
        return False
    return process_exists(holder.pid) is False


def holder_alive(holder: Holder, *, here: Holder | None = None) -> bool:
    """Whether a recorded holder is still running.

    FAILS TOWARDS ALIVE on every question this process cannot answer, since
    guessing dead lets one machine clear another's lock. A holder from this
    machine's earlier boot is gone (R-647). Existence and identity are asked
    separately: pids are recycled, but an unanswerable start time is not a mismatch.
    """
    reference = here or current_holder()
    if holder.host != reference.host:
        return True
    if UNKNOWN_IDENTITY in (holder.boot, reference.boot):
        return True
    if holder.boot != reference.boot:
        return not _gone_since_an_earlier_boot(holder, reference)
    if holder.started == UNKNOWN_IDENTITY:
        return True
    exists = process_exists(holder.pid)
    if exists is not True:
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

    A programming error, checked before the kernel, which would report it as a
    foreign holder and tell the caller to wait for itself.
    """


#: Lock paths this process currently holds, read before the kernel is asked.
_HELD: set[str] = set()


def lock_path(cfg: config.Config) -> Path:
    """The whole-run lock, beside the library, distinct from the writer's narrow
    lock so a second process refuses at the door rather than part way through."""
    return config.state_path("session_lock", cfg)


def read_lock_holder(path: Path | str) -> Holder | None:
    """Who the lock file says holds it, or None when it says nobody or is unreadable.

    The content is advisory, only to name a holder; the kernel does the exclusion.
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
        # A damaged record answers None too; the shell tells it from absent.
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
    """Open the lock file, private, creating the directory private with it, since
    a replaceable lock file in an open directory loses the exclusion (P1)."""
    config.mkdir_private(target.parent)
    # Explicit mode, not the umask; read-write since the holder is replaced.
    descriptor = os.open(target, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
    handle = os.fdopen(descriptor, "r+")
    if hasattr(os, "chmod"):  # guarded: a POSIX mode is meaningless on some platforms
        try:
            # Fixes the mode of a lock an earlier build created.
            os.chmod(target, config.PRIVATE_FILE_MODE)
        except OSError as exc:
            # Not fatal: another account's file cannot be chmodded.
            logger.debug("could not set the mode on the session lock at %s: %s", target, exc)
    return handle


def _lock_held_refusal(target: Path, holder: Holder | None) -> CratekitError:
    """The refusal for a lock somebody else has, with the right remedy token.

    A running holder is waited for; a held lock whose holder is gone, reachable
    on a networked filesystem, is released by an explicit act.
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

    THE FILE IS NEVER UNLINKED, or a second process locks a fresh inode at the
    same name and both believe they hold it.
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
            # The writer's own acquisition, so the two cannot differ.
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

    Returns the holder cleared, or None. Refuses while the holder still runs.
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


def orphaned(record: SessionRecord, *, here: Holder | None = None) -> bool:
    """Whether an open record's owner is provably gone, so nothing will ever end it.

    Only an ``open`` record that names a holder :func:`holder_alive` judges gone
    (R-598); the other states wait on an import or a restore, and an intake
    landing stays open across processes with no holder. An unreadable holder is alive.
    """
    if record.state is not SessionState.OPEN:
        return False
    recorded = record.detail.get(HOLDER_KEY)
    if not isinstance(recorded, Mapping):
        return False
    try:
        holder = Holder.from_json(recorded)
    except (TypeError, ValueError):
        return False
    return not holder_alive(holder, here=here)


def abandon_orphaned_sessions(
    cfg: config.Config,
    *,
    only: Iterable[str] | None = None,
    now: datetime | None = None,
) -> tuple[SessionRecord, ...]:
    """End every open record whose owner is provably gone, and return them.

    A SIGKILL or a power loss (R-647) leaves a record ``open`` for ever. ``only``
    limits the sweep to the records the caller showed (R-648). Abandoning is
    the ungated close; a recorded commit still reads as work a restore discards.
    """
    here = current_holder()
    shown = None if only is None else frozenset(only)
    return tuple(
        close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        for record in records(cfg)
        if (shown is None or record.session_id in shown) and orphaned(record, here=here)
    )


# ---------------------------------------------------------------------------
# The backup acknowledgment (KTD18, R34)
# ---------------------------------------------------------------------------

#: The library-scoped state entry this acknowledgment is written to.
ACK_KEY = "backup_ack"

#: Bumped only when the record's shape changes incompatibly.
ACK_SCHEMA_VERSION = 1

#: How long one acknowledgment answers for, bounded since an unbounded one is a
#: permanent affirmative (R34).
DEFAULT_ACK_VALIDITY = timedelta(hours=12)

#: The actor a session records its answer to the acknowledgment's gate under (U138).
SESSION_ACTOR = "session"

#: The oldest any backup portion may be for a session to mint (U138).
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

#: Which rule minted an acknowledgment; an older record reads as the terminal rule.
RULE_TERMINAL = "terminal"
RULE_SESSION_AGES = "session-ages"


@dataclass(frozen=True, slots=True)
class ShownAge:
    """One backup portion's age AS IT WAS SHOWN when the person answered,
    recorded rather than recomputed (KTD18)."""

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
    #: The rule that minted it, :data:`RULE_TERMINAL` or :data:`RULE_SESSION_AGES`.
    rule: str = RULE_TERMINAL
    #: The actor the run record holds for the gate's answer, or None. Never
    #: :attr:`actor`, which is derived.
    decided_by: str | None = None

    def valid_at(self, moment: datetime) -> bool:
        return moment < self.expires_at

    def to_json(self) -> dict[str, Any]:
        # No version bump for the two U138 keys, so older builds still read it.
        return {
            "schema_version": ACK_SCHEMA_VERSION,
            "actor": self.actor,
            "recorded_at": self.recorded_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "shown": [entry.to_json() for entry in self.shown],
            "rule": self.rule,
            "decided_by": self.decided_by,
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
            rule=str(data.get("rule") or RULE_TERMINAL),
            decided_by=(
                str(data["decided_by"]) if data.get("decided_by") is not None else None
            ),
        )


def has_controlling_terminal() -> bool:
    """Whether this invocation has a terminal a person could be sitting at.

    A terminal check, not a read, since no verb reads standard input (R33).
    Falls back to the output stream where there is no terminal device.
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
    """Who this invocation is, derived from the invocation and never supplied (R34),
    or an agent could name itself into the audit trail.

    Reads ``pwd`` directly, since the convenience wrapper's module offers a
    password prompt the static guard forbids.
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
    """The backup ages, read from the FACT file, since the backup module is opt-in.

    An unreadable fact file refuses rather than showing nothing, which would read
    as a library with no portions; an absent one mints normally. The remedy
    travels from ``read_facts``, so a permission is not reported as corruption.
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


def _too_old_for_a_session(shown: Sequence[ShownAge]) -> list[str]:
    """Each portion a session may not mint over, with why, in the order shown.

    An unknown age counts against the session, since could not tell is never
    fresh enough.
    """
    limit = SESSION_MAX_BACKUP_AGE.total_seconds()
    named = []
    for entry in shown:
        if entry.state != backup_facts.AgeState.KNOWN or entry.age_seconds is None:
            named.append(f"the {entry.portion} portion's age is not known ({entry.state})")
        elif entry.age_seconds >= limit:
            named.append(
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"
            )
    return named


def record_acknowledgment(
    cfg: config.Config,
    *,
    now: datetime | None = None,
    validity: timedelta = DEFAULT_ACK_VALIDITY,
    terminal: Callable[[], bool] | None = None,
    decided_by: str | None = None,
) -> Acknowledgment:
    """Mint the acknowledgment. A separate act from answering it, by a person.

    ``terminal`` is a test seam, not an override. THERE IS NO ACTOR PARAMETER
    and no affirmative one, or the gate would be under the control of what it
    gates. ``decided_by`` is a rule selector (U138): :data:`SESSION_ACTOR`
    swaps the terminal check for the rule that every portion reads under
    :data:`SESSION_MAX_BACKUP_AGE`.
    """

    moment = now or datetime.now(timezone.utc)
    if decided_by == SESSION_ACTOR:
        shown = _shown_ages(cfg, moment)
        stale = _too_old_for_a_session(shown)
        if stale:
            raise refuse(
                "backup-acknowledgment-backup-too-old",
                f"a session mints the backup acknowledgment only while every backup "
                f"portion is under {SESSION_MAX_BACKUP_AGE.days} days old, and "
                f"{'; '.join(stale)}; run a backup first, or a person acknowledges "
                f"from a terminal",
                remedy=Remedy.RUN_BACKUP,
                scope=Scope.RUN,
                detail={
                    "library": str(cfg.library.root),
                    "portions": [entry.to_json() for entry in shown],
                    "max_age_days": SESSION_MAX_BACKUP_AGE.days,
                },
            )
        rule = RULE_SESSION_AGES
    else:
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
        shown = _shown_ages(cfg, moment)
        rule = RULE_TERMINAL
    acknowledgment = Acknowledgment(
        actor=derive_actor(),
        recorded_at=moment,
        expires_at=moment + validity,
        shown=shown,
        rule=rule,
        decided_by=decided_by,
    )
    config.atomic_write_bytes(
        json.dumps(acknowledgment.to_json(), indent=2, sort_keys=True).encode("utf-8") + b"\n",
        ack_path(cfg),
    )
    return acknowledgment


def read_acknowledgment(cfg: config.Config) -> Acknowledgment | None:
    """The recorded acknowledgment, or None when this library has none.

    A file that exists and cannot be understood refuses, since reporting it as
    absent hides what is broken.
    """
    try:
        raw = ack_path(cfg).read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        # A read that did not happen, which establishes nothing about presence.
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

    Absent and expired are one refusal, since the remedy is one act.
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

#: Which refusal slug each mount verdict raises, a table so a new mount state
#: with no entry fails a test rather than falling to a default.
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

    At destructive strength, so an unreadable identity is fatal. The
    precondition error is converted here so one condition has one identity.
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
# The volume gate, for every volume a prefix rule points at
# ---------------------------------------------------------------------------

#: Which refusal slug each mount verdict raises for a prefix rule target, apart
#: from ``_MOUNT_REASONS`` since those slugs carry the library volume's remedy.
_MAPPED_REASONS: Mapping[preflight.MountState, str] = MappingProxyType(
    {
        preflight.MountState.NOT_MOUNTED: "mapped-volume-unmounted",
        preflight.MountState.MOUNTED_ELSEWHERE: "mapped-volume-mismatch",
        preflight.MountState.FOREIGN_VOLUME: "mapped-volume-mismatch",
        preflight.MountState.IDENTITY_UNAVAILABLE: "mapped-volume-mismatch",
        preflight.MountState.IDENTITY_NOT_RECORDED: "mapped-volume-mismatch",
    }
)

#: The verdicts under which a rule's target HAS proved its identity, so the two
#: tables are total over the enum. ``LIBRARY_PATH_MISSING`` means the identity
#: matched; a missing directory is refused per row, only when a row uses it.
_MAPPED_PROVED: frozenset[preflight.MountState] = frozenset(
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)


def expected_rule_identity(cfg: config.Config, rule: locations.PrefixRule) -> str | None:
    """The identity a rule's target must show, or None when nothing says.

    A rule's own identity first; a target inside the library root (lexically,
    by the resolver's test) is held to the library's. Anything else is None,
    never the library's, since an ejected drive's leftover directory on the
    boot disk would match it.
    """
    if rule.volume_id:
        return rule.volume_id
    inside = locations.resolve_recorded_path(rule.target or "/", root=cfg.library.root)
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None


#: The path crosses a place this platform mounts volumes and nothing is mounted there.
_EMPTY_MOUNT_SLOT = "mount_slot_empty"
_UNREACHABLE = "unreachable"


def _held_to(rule: locations.PrefixRule) -> str:
    """Whose identity the comparison used, since a rule inside the root records none."""
    if rule.volume_id:
        return "the volume recorded on that rule"
    return "the library's volume, which a target inside the library root is held to"


def _mapped_steps(
    key: str,
    rule: locations.PrefixRule,
    probe: str,
    status: preflight.MountStatus,
    observed: str | None,
) -> tuple[str, ...]:
    """What a person does about one rule. One act, naming the rule and the disk."""
    state = status.state
    if state is preflight.MountState.IDENTITY_NOT_RECORDED:
        if observed:
            return (
                f"the volume at {probe} identifies as {observed} now; confirm that "
                f"is the disk those tracks live on, then record it as volume_id on "
                f"{key}",
            )
        return (
            f"with the right disk mounted at {probe}, record its identity as "
            f"volume_id on {key}",
        )
    if state is preflight.MountState.NOT_MOUNTED:
        return (f"mount the volume {key} points at, or correct that rule's 'to' ({probe})",)
    if state is preflight.MountState.MOUNTED_ELSEWHERE:
        return (
            f"that volume is mounted at {status.found_at}; mount it at {probe}, or "
            f"correct the 'to' of {key}",
        )
    if state is preflight.MountState.FOREIGN_VOLUME:
        if rule.volume_id and observed:
            return (
                f"mount the volume recorded on {key} at {probe}, or, if the volume "
                f"there now ({observed}) is the right one, record it as that "
                f"rule's volume_id",
            )
        return (f"mount the right volume at {probe}, or correct the 'to' of {key}",)
    return (
        f"no identity can be read for the filesystem {probe} sits on, so nothing "
        f"can prove which disk {key} reaches; move those tracks under the library "
        f"root or remove the rule",
    )


def _mapped_problem(rule: locations.PrefixRule, status: preflight.MountStatus) -> str:
    """One clause on what was observed at a rule's target. No verb for the person."""
    state = status.state
    if state is preflight.MountState.IDENTITY_NOT_RECORDED:
        return (
            "that target is not under the library root as configuration spells "
            "it and the rule records no volume identity, so nothing proves which "
            "disk it reaches"
        )
    if state is preflight.MountState.NOT_MOUNTED:
        return f"{_held_to(rule)} is not mounted"
    if state is preflight.MountState.MOUNTED_ELSEWHERE:
        return f"{_held_to(rule)} is mounted at {status.found_at} instead"
    if state is preflight.MountState.FOREIGN_VOLUME:
        return (
            f"a different volume is there than {_held_to(rule)}: expected identity "
            f"{status.recorded_identity}, mounted identity {status.observed_identity}"
        )
    return f"no volume identity is readable for the filesystem at {status.mount_point}"


def _assert_rule_volume(
    cfg: config.Config,
    index: int,
    rule: locations.PrefixRule,
    probe: Path,
    *,
    identity_provider: preflight.IdentityProvider | None,
    mount_enumerator: preflight.MountEnumerator | None,
) -> preflight.MountStatus:
    """Prove ``probe``, a path reached through rule ``index``, is on that rule's volume.

    An empty mount slot is an unattached drive whatever identity a walk upward
    finds, so ``preflight.identity_source`` is asked before any identity.
    """
    key = f"library.location_prefix_map[{index}]"
    target = rule.target or "/"
    detail: dict[str, Any] = {
        "rule": index,
        "source": rule.source,
        "target": target,
        "probed": str(probe),
    }
    opening = f"prefix rule {index} maps {rule.source} onto {target}, and "
    closing = ", so this destructive session refuses rather than follow that rule"
    identity_of = identity_provider or preflight.default_identity_provider()
    try:
        source = preflight.identity_source(probe)
        if source is None:
            raise refuse(
                "mapped-volume-unmounted",
                f"{opening}{probe} is where a volume mounts and nothing is "
                f"mounted there now{closing}",
                steps=(f"mount the volume {key} points at, or correct that rule's 'to'",),
                scope=Scope.RUN,
                detail={**detail, "state": _EMPTY_MOUNT_SLOT},
            )
        try:
            return preflight.assert_library_volume(
                probe,
                expected_rule_identity(cfg, rule),
                destructive=True,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
        except preflight.LibraryVolumeError as exc:
            status = exc.status
            if status.state in _MAPPED_PROVED:
                return status
            # Indexed, no default: an undecided verdict must fail.
            reason = _MAPPED_REASONS[status.state]
            observed = status.observed_identity
            if status.state is preflight.MountState.IDENTITY_NOT_RECORDED:
                # Read from the accepted mount, so the step can name the identity.
                observed = identity_of(source)
            raise refuse(
                reason,
                f"{opening}{_mapped_problem(rule, status)}{closing}",
                steps=_mapped_steps(key, rule, str(probe), status, observed),
                scope=Scope.RUN,
                detail={
                    **detail,
                    "state": str(status.state),
                    "recorded_identity": status.recorded_identity,
                    "observed_identity": observed,
                },
            ) from exc
    except OSError as exc:
        # Could not look is its own refusal, not an internal defect.
        raise refuse(

            "mapped-volume-mismatch",
            f"{opening}which volume {probe} sits on could not be established "
            f"({exc}){closing}",
            steps=(
                f"make the way to {probe} readable by this account, or correct "
                f"the 'to' of {key}",
            ),
            scope=Scope.RUN,
            detail={**detail, "state": _UNREACHABLE},
        ) from exc


def assert_mapped_volume_identities(
    cfg: config.Config,
    rules: Sequence[locations.PrefixRule],
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> tuple[preflight.MountStatus, ...]:
    """Refuse unless every prefix rule's target sits on the volume it was recorded on.

    A pass following a rule writes off the library root, often onto the archive
    disk. Every rule is asked, since knowing which a row uses means resolving
    paths first. A present directory is not an identity.
    """
    return tuple(
        _assert_rule_volume(
            cfg,
            index,
            rule,
            Path(rule.target or "/"),
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
        for index, rule in enumerate(rules)
    )


def assert_mapped_file_volume(
    cfg: config.Config,
    rules: Sequence[locations.PrefixRule],
    index: int,
    path: Path | str,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> preflight.MountStatus:
    """Prove the volume ONE FILE reached through rule ``index`` actually sits on.

    The file's own directory is probed, since a nested mount or symlink can sit
    between it and the target, and per file, since a drive can be swapped
    during a long pass.
    """
    return _assert_rule_volume(
        cfg,
        index,
        rules[index],
        Path(path).parent,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )


# ---------------------------------------------------------------------------
# The three gates
# ---------------------------------------------------------------------------


class Intent(StrEnum):
    """What a destructive session is FOR. Two answers, differing on exactly one gate.

    Not an override: every gate applies to both. A recovery skips only the
    unresolved-session latch, whose own remedy is a restore.
    """

    WRITE = "write"
    RECOVERY = "recovery"


class Keep(StrEnum):
    """What the gates keep in the session log for the body they admit.

    Not a boolean, which is what a blanket affirmative looks like (R34).
    ``RECORD`` is owed by every body that takes a capture.
    """

    NOTHING = "nothing"
    RECORD = "record"


@dataclass(frozen=True, slots=True)
class Gates:
    """What passing the gates established, handed to the body of the session."""

    workflow: str
    lock: Path
    acknowledgment: Acknowledgment
    volume: preflight.MountStatus
    intent: Intent = Intent.WRITE
    #: The open session record when ``keep`` asked for one, else ``None``.
    record: SessionRecord | None = None


def assert_no_unresolved_session(cfg: config.Config) -> None:
    """Refuse every further write while a session ended ``committed-unverified``.

    Enforced at the gate, not per workflow, since there is no post-commit
    rollback. Reads the log strictly: an unparsable entry refuses, or the gate
    fails open.
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
            f"{unread_clause(unreadable, cfg)}, so this gate cannot vouch that no "
            "session ended unresolved; refusing rather than writing against a log "
            "it cannot read",
            remedy=Remedy.REPORT_DEFECT,
            scope=Scope.RUN,
            detail={
                "unreadable": [str(path) for path in unreadable],
                "unlisted": log_unlisted(unreadable, cfg),
            },
        )


def resolve_unverified_session(
    session_id: str, cfg: config.Config, *, now: datetime | None = None
) -> SessionRecord:
    """Close one ``committed-unverified`` record, once a person has dealt with it.

    A separate act, since the log survives the restore that remedies it.
    Refuses any other state, which would release a live run's capture.
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
    keep: Keep = Keep.NOTHING,
) -> Iterator[Gates]:
    """The one entry point every destructive operation passes through (KTD24).

    Volume, then acknowledgment, then lock, each with its own code, so a
    refused session writes nothing. ``workflow`` is supplied since this layer
    names no verb (D2), and reaches the log only with ``keep`` (R-375).

    ``keep=Keep.RECORD`` is owed by a body that takes a capture, since the log
    is what makes it an undo (R-12). The record opens here, between the lock
    and the analysis watch, so a watch refusal closes it abandoned.

    ``intent=RECOVERY`` skips only the two latches, whose remedy is a recovery.
    ``analysis_roots`` arms the runtime half of R17's fifth surface: analysis
    files beneath them are fingerprinted and a moved one refuses. Empty by
    default, guarded against the unit that owes the roots (P5).
    """
    resolved = cfg if cfg is not None else config.load()
    volume = assert_volume_identity(
        resolved,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )
    if intent is not Intent.RECOVERY:
        assert_no_unresolved_session(resolved)
        # The unreconciled-restore latch, at the gate so no caller forgets it.
        reconcile.assert_converged(resolved)
    acknowledgment = assert_backup_acknowledged(resolved, now=now)
    watched = list(analysis_roots)
    # One claimant, so the record names the process the lock names.
    claimant = holder or current_holder()
    with session_lock(resolved, path=lock, holder=claimant) as held:
        keeping = (
            _recorded(
                resolved,
                workflow=workflow,
                acknowledgment=acknowledgment,
                holder=claimant,
                intent=intent,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
                now=now,
            )
            if keep is Keep.RECORD
            else nullcontext()
        )
        with keeping as record:
            with analysis_files_unmoved(watched) if watched else nullcontext():
                yield Gates(
                    workflow=workflow,
                    lock=held,
                    acknowledgment=acknowledgment,
                    volume=volume,
                    intent=intent,
                    record=record,
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
    holder: Holder | None = None,
    now: datetime | None = None,
) -> SessionRecord:
    """Start a session record and persist it before any work happens, so a
    crashed run has one and its capture is protected (R30).

    ``holder`` lets :func:`orphaned` prove the owner gone (R-598); only the
    gates pass one, and a record without one is never orphaned.
    """
    record = SessionRecord(
        session_id=session_id or new_session_id(now),
        workflow=workflow,
        started=output.timestamp(now),
        state=SessionState.OPEN,
        actor=actor,
        acknowledged_at=acknowledged_at,
        sources={source: str(SourceState.PENDING) for source in sources},
        detail={HOLDER_KEY: holder.to_json()} if holder is not None else {},
    )
    write_record(record, cfg)
    return record


def attach_capture(record: SessionRecord, capture_path: Path | str, cfg: config.Config) -> None:
    """Record which capture this session is the undo for, and persist it at once,
    or retention may prune it while the write runs."""

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

    A committed source is skipped on resume, the record is persisted after
    each, and a refusal reports both halves. ``run_one`` raises to refuse and
    its cause is carried underneath (KTD25). The scope is widened, never
    narrowed, so a run-wide cause is not reported as one source's.
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
        record_commit(record, source, change, cfg)
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

    Only a TERMINAL state releases a capture, so a non-terminal one refuses.
    Closing is gated on convergence, since a restore can land while an
    ``awaiting-import`` session is open without the lock; abandoning is not,
    or a run could be neither finished nor given up. A RECOVERY closes
    ungated. The volume is asserted first, since an unmounted library reads as
    an empty reconciliation record.
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
# The record a gated session keeps (R-12, R-375)
# ---------------------------------------------------------------------------


@contextmanager
def _recorded(
    cfg: config.Config,
    *,
    workflow: str,
    acknowledgment: Acknowledgment,
    holder: Holder,
    intent: Intent,
    identity_provider: preflight.IdentityProvider | None,
    mount_enumerator: preflight.MountEnumerator | None,
    now: datetime | None,
) -> Iterator[SessionRecord]:
    """Hold an open session record for the body of one gated session.

    Private, reached only through ``assert_gates(keep=Keep.RECORD)``, so it
    records what the gates passed. IT ENDS TERMINAL ON EVERY PATH THAT CAN STILL
    WRITE THE LOG: a raise or a refused close abandons it, a kill is left to
    :func:`abandon_orphaned_sessions` (R-598). Abandoning is an attempt that
    never replaces the session's own error.
    """
    record = open_session(
        cfg,
        workflow=workflow,
        actor=acknowledgment.actor,
        acknowledged_at=acknowledgment.recorded_at.isoformat(),
        holder=holder,
        now=now,
    )
    try:
        yield record
        close_session(
            record,
            cfg,
            state=SessionState.CLOSED,
            intent=intent,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
        try:
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise


def record_commit(
    record: SessionRecord, source: str, change: ChangeSummary, cfg: config.Config
) -> None:
    """Record that one source's commit landed, and persist it at once, so a
    later failure still reads to a restore as work it would discard."""
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
    write_record(record, cfg)


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

    The run record's own type, not a parallel one. Verb names arrive as
    parameters (D2).
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

    The XML creates the rows a database surface writes, so no database surface
    runs before a person imports it.
    """
    record.state = SessionState.AWAITING_IMPORT
    record.pending = pending
    write_record(record, cfg)
    return record


#: The record field saying an import was PROVEN, by what, and which file.
#: Written only by :func:`mark_import_verified`.
IMPORT_VERIFIED_KEY = "import_verified"


def mark_import_verified(
    record: SessionRecord,
    cfg: config.Config,
    *,
    evidence: str,
    now: datetime | None = None,
) -> SessionRecord:
    """Move a session out of the un-imported state, once the import is proven.

    THE ONLY WAY OUT OF ``awaiting-import`` (R-501). Returns the record to
    ``open``, since ending a run is ``close_run``'s claim. ``evidence`` is
    required; the artifact is kept so the file can still be retired. Refuses
    any other state.
    """
    if record.state is not SessionState.AWAITING_IMPORT:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
            remedy=Remedy.REPORT_DEFECT,
            detail={"session_id": record.session_id, "state": str(record.state)},
        )
    pending = record.pending
    record.detail[IMPORT_VERIFIED_KEY] = {
        "at": output.timestamp(now),
        "evidence": evidence,
        "artifact": pending.artifact if pending is not None else None,
    }
    record.state = SessionState.OPEN
    record.pending = None
    write_record(record, cfg)
    return record


def owes_only_deferred_routing(record: SessionRecord) -> bool:
    """True when the one thing this open run still owes is a deferred placement.

    The cutover precheck's question: open, no capture, and a proven import,
    since that placement needs the tree the cutover creates.
    """
    return (
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
    )


def assert_database_surface_allowed(record: SessionRecord) -> None:
    """Refuse a database write while this run's XML output has not been imported,
    in the pending-human class since nothing is broken."""
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
    """Hang one cause at the TAIL of another's chain, displacing nothing."""

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

    The writing session's cache cannot see a stale view. CLOSING A DATABASE DOES
    NOT RELEASE IT, so the writer's full close is used. On disagreement the
    session ends ``committed-unverified``, since there is no rollback. A
    read-back that could not run and a running rekordbox are chained beneath
    the cause, never replacing it (KTD25).
    """
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg))
    agreed = False
    handle = None
    failure: Cause | None = None
    try:
        handle = open_fresh()
        agreed = bool(expect(handle))
    except CratekitError as exc:
        # Kept, since a typed failure says what to do (KTD25).
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

    # The rekordbox probe goes at the tail, keeping the read-back's own chain.
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
#: binding's three on purpose, since R17's fifth surface names a fourth (P4).
ANLZ_NAME_PATTERN = re.compile(r"^ANLZ[0-9]{4}\.(?:DAT|EXT|2EX|3EX)$", re.IGNORECASE)


def is_analysis_file(path: Path | str) -> bool:
    """Whether a path names one of rekordbox's per-track analysis files."""
    return bool(ANLZ_NAME_PATTERN.match(Path(path).name))


def analysis_files_under(roots: Iterable[Path | str]) -> tuple[Path, ...]:
    """Every analysis file beneath the given directories, sorted.

    DERIVED BY WALKING (P3), since the write to catch is the unintended one a
    hand-list omits.
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

    Size too, since a rewrite inside one clock tick leaves the time alone.
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

    An appearing file means rekordbox analysed during the session, worth surfacing.
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

    THIS IS THE HALF THE SOURCE SCAN CANNOT DO, a grid rewritten through a
    handle the binding returned. The remedy is the capture. THE COMPARISON RUNS
    ON BOTH PATHS, since a body that raised is retried; its error is carried
    beneath the refusal.
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
    "BOOT_DRIFT_SECONDS",
    "DEFAULT_ACK_VALIDITY",
    "HOLDER_KEY",
    "IMPORT_VERIFIED_KEY",
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
    "Keep",
    "SessionComposition",
    "SessionRecord",
    "SessionState",
    "ShownAge",
    "SourceState",
    "TreeChange",
    "abandon_orphaned_sessions",
    "ack_path",
    "analysis_drift",
    "analysis_files_under",
    "analysis_files_unmoved",
    "assert_backup_acknowledged",
    "assert_database_surface_allowed",
    "assert_gates",
    "assert_mapped_file_volume",
    "assert_mapped_volume_identities",
    "assert_no_unresolved_session",
    "assert_volume_identity",
    "attach_capture",
    "boot_identity",
    "close_session",
    "commit_sources",
    "current_holder",
    "derive_actor",
    "expected_rule_identity",
    "fingerprint_analysis_files",
    "has_controlling_terminal",
    "holder_alive",
    "is_analysis_file",
    "lock_path",
    "log_dir",
    "log_unlisted",
    "log_path",
    "machine_identity",
    "mark_awaiting_import",
    "mark_import_verified",
    "new_session_id",
    "open_session",
    "orphaned",
    "owes_only_deferred_routing",
    "pending_import",
    "process_exists",
    "process_started",
    "read_acknowledgment",
    "read_lock_holder",
    "read_record",
    "record_acknowledgment",
    "record_commit",
    "records",
    "release_stale_lock",
    "resolve_unverified_session",
    "scan_log",
    "session_lock",
    "unread_clause",
    "verify_commit",
    "write_record",
]
