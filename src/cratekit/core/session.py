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
import json
import logging
import os
import re
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence

from cratekit.cli import output
from cratekit.core import config, preflight, rb_writer, reconcile
from cratekit.core.cause import (
    Cause,
    CratekitError,
    Remediation,
    Scope,
    refuse,
    widest_scope,
)
from cratekit.core.exit_codes import Remedy
from cratekit.core.session_ack import ACK_SCHEMA_VERSION as ACK_SCHEMA_VERSION
from cratekit.core.session_ack import RULE_SESSION_AGES as RULE_SESSION_AGES
from cratekit.core.session_ack import SESSION_ACTOR as SESSION_ACTOR
from cratekit.core.session_ack import SESSION_MAX_BACKUP_AGE as SESSION_MAX_BACKUP_AGE
from cratekit.core.session_ack import Acknowledgment, assert_backup_acknowledged
from cratekit.core.session_ack import _shown_ages as _shown_ages
from cratekit.core.session_ack import ack_path as ack_path
from cratekit.core.session_ack import derive_actor as derive_actor
from cratekit.core.session_ack import has_controlling_terminal as has_controlling_terminal
from cratekit.core.session_ack import read_acknowledgment as read_acknowledgment
from cratekit.core.session_ack import record_acknowledgment as record_acknowledgment
from cratekit.core.session_analysis import analysis_files_under as analysis_files_under
from cratekit.core.session_analysis import analysis_files_unmoved
from cratekit.core.session_analysis import is_analysis_file as is_analysis_file
from cratekit.core.session_holders import _HELD as _HELD
from cratekit.core.session_holders import BOOT_DRIFT_SECONDS as BOOT_DRIFT_SECONDS
from cratekit.core.session_holders import UNKNOWN_IDENTITY as UNKNOWN_IDENTITY
from cratekit.core.session_holders import Holder, current_holder, session_lock
from cratekit.core.session_holders import SessionComposition as SessionComposition
from cratekit.core.session_holders import _open_lock_file as _open_lock_file
from cratekit.core.session_holders import abandon_orphaned_sessions as abandon_orphaned_sessions
from cratekit.core.session_holders import boot_identity as boot_identity
from cratekit.core.session_holders import holder_alive as holder_alive
from cratekit.core.session_holders import lock_path as lock_path
from cratekit.core.session_holders import machine_identity as machine_identity
from cratekit.core.session_holders import orphaned as orphaned
from cratekit.core.session_holders import process_exists as process_exists
from cratekit.core.session_holders import process_started as process_started
from cratekit.core.session_holders import read_lock_holder as read_lock_holder
from cratekit.core.session_holders import release_stale_lock as release_stale_lock
from cratekit.core.session_volumes import _MAPPED_PROVED as _MAPPED_PROVED
from cratekit.core.session_volumes import _MAPPED_REASONS as _MAPPED_REASONS
from cratekit.core.session_volumes import _MOUNT_REASONS as _MOUNT_REASONS
from cratekit.core.session_volumes import assert_mapped_file_volume as assert_mapped_file_volume
from cratekit.core.session_volumes import (
    assert_mapped_volume_identities as assert_mapped_volume_identities,
)
from cratekit.core.session_volumes import assert_volume_identity
from cratekit.core.session_volumes import expected_rule_identity as expected_rule_identity

logger = logging.getLogger(__name__)


def _defect(message: str, **refusal: Any) -> CratekitError:
    """An ``internal-error`` refusal, whose remedy is to report the defect."""
    return refuse("internal-error", message, remedy=Remedy.REPORT_DEFECT, **refusal)


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
            raise _defect(
                f"the session log entry declares schema {version!r} and this "
                f"build understands {LOG_SCHEMA_VERSION}; refusing to guess what "
                f"wrote it",
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
        raise _defect(
            f"no session is recorded with the identifier {session_id!r}: {exc}",
            detail={"session_id": session_id, "path": str(path)},
        ) from exc
    except OSError as exc:
        raise _defect(
            f"the session record at {path} could not be read, so whether a "
            f"session is recorded under {session_id!r} was not established: {exc}",
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
        raise _defect(
            f"{unread_clause(unreadable, cfg)}, so no session recorded in it can be "
            "read; refusing rather than answering that none is recorded",
            scope=Scope.RUN,
            detail={"log": str(log_dir(cfg)), "unlisted": True},
        )
    return parsed


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
        raise _defect(
            f"{unread_clause(unreadable, cfg)}, so this gate cannot vouch that no "
            "session ended unresolved; refusing rather than writing against a log "
            "it cannot read",
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
        raise _defect(
            f"session {session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.COMMITTED_UNVERIFIED)!r}; only a session that "
            f"committed behind a read-back that disagreed is resolved this way",
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
        # The record a gated session keeps (R-12, R-375) ENDS TERMINAL ON EVERY
        # PATH THAT CAN STILL WRITE THE LOG: a raise or a refused close abandons
        # it, a kill is left to :func:`abandon_orphaned_sessions` (R-598).
        # Abandoning is an attempt that never replaces the session's own error.
        record = (
            open_session(
                resolved,
                workflow=workflow,
                actor=acknowledgment.actor,
                acknowledged_at=acknowledgment.recorded_at.isoformat(),
                holder=claimant,
                now=now,
            )
            if keep is Keep.RECORD
            else None
        )
        try:
            with analysis_files_unmoved(watched) if watched else nullcontext():
                yield Gates(
                    workflow=workflow,
                    lock=held,
                    acknowledgment=acknowledgment,
                    volume=volume,
                    intent=intent,
                    record=record,
                )
            if record is not None:
                close_session(
                    record,
                    resolved,
                    state=SessionState.CLOSED,
                    intent=intent,
                    identity_provider=identity_provider,
                    mount_enumerator=mount_enumerator,
                    now=now,
                )
        except BaseException:
            if record is not None:
                try:
                    close_session(record, resolved, state=SessionState.ABANDONED, now=now)
                except Exception:  # noqa: BLE001 - the session's own error is the one to surface
                    logger.warning(
                        "session %s could not be recorded as abandoned",
                        record.session_id,
                        exc_info=True,
                    )
            raise


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
            # The reason, remediation and retryability carried over from the source's cause.
            raise CratekitError(
                replace(
                    exc.cause,
                    message=(
                        f"session {record.session_id} refused at source {source!r}; "
                        f"sources already committed are untouched"
                    ),
                    scope=widest_scope(exc.cause.scope, Scope.SOURCE),
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
        raise _defect(
            f"{state!r} is not a terminal session state, so closing into it would "
            f"release a capture the session still references",
            detail={"state": str(state), "session_id": record.session_id},
        )
    record.state = state
    record.ended = output.timestamp(now)
    write_record(record, cfg)
    return record


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
        raise _defect(
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
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
    except Exception as exc:  # noqa: BLE001 - a read-back that cannot run has not agreed
        logger.warning("the post-commit read-back could not run: %s", exc)
        # A typed failure is kept, since it says what to do (KTD25).
        failure = exc.cause if isinstance(exc, CratekitError) else Cause(
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
