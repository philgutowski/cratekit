"""Feature Inventory row 31: library backup, and the age fact R15 reads.

THE FILE MIRROR runs any time, moving what it would overwrite or delete into a
dated archive first. THE DATABASE is held open and written by rekordbox and its
agent, and a copy taken while either lives is torn yet opens cleanly, so it is
excluded from the mirror and comes only from a gated, dated snapshot with both
confirmed gone; an outside analysis share rides that portion. Analysis files are
handed to rclone, never opened or authored. The age is published per portion,
the process probe is a seam and never an environment variable, the plan is data
so a dry run is the run neutralized, and a restore is a named decision behind
the destructive session gates. The database snapshot's capture and restore
plans live in ``backup_snapshot`` and the census proof in ``backup_proof``, both
re-exported here.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path

from cratekit.core import backup_facts, binaries, config, preflight, session
from cratekit.core.cause import CratekitError
from cratekit.core.processes import (
    REKORDBOX_PROCESSES,
    AbsenceUnconfirmed,
    ProcessLister,
    rekordbox_processes_running,
    running_process_names,
)
from cratekit.modules.tools import backup_record
from cratekit.modules.tools.backup_proof import EMPTIED_FLAG, _history, _unproven  # noqa: F401

#: Volume clutter no backup should carry: platform metadata and resource forks.
VOLUME_EXCLUDES: tuple[str, ...] = (
    ".DS_Store", ".Spotlight-V100/**", ".fseventsd/**", ".Trashes/**",
    ".DocumentRevisions-V100/**", ".TemporaryItems/**", "._*", "$RECYCLE.BIN/**",
    "System Volume Information/**",
)
#: Where rekordbox keeps its own settings, a fact about the application.
_SETTINGS_DIRS_BY_PLATFORM: dict[str, tuple[str, ...]] = {
    "darwin": ("Library/Application Support/Pioneer/rekordbox6",),
    "win32": ("AppData/Roaming/Pioneer/rekordbox6",),
}
#: Command labels, named once since the executor and the dry run both branch on them.
MIRROR = "mirror"
PRUNE_ARCHIVE = "prune-archive"
PRUNE_ARCHIVE_FOLDER = "prune-archive-folder"
SNAPSHOT_DATABASE = "snapshot-database"
SNAPSHOT_SETTINGS = "snapshot-settings"
SNAPSHOT_IDENTITY = "snapshot-identity"
SNAPSHOT_SHARE = "snapshot-share"
RESTORE_MIRROR = "restore-mirror"
RESTORE_DATABASE = "restore-database"
RESTORE_SHARE = "restore-share"
LIST_SNAPSHOTS = "list-snapshots"
LIST_SNAPSHOT_CONTENTS = "list-snapshot-contents"
LIST_SNAPSHOT_IDENTITY = "list-snapshot-identity"
LIST_SHARE = "list-share"
#: A quick run's commands, reading paths on standard input: added or changed,
#: rewritten keeping size and time, and removed (moved to the dated archive).
QUICK_SEND = "quick-send"
QUICK_RESEND = "quick-resend"
QUICK_ARCHIVE = "quick-archive"
QUICK_LABELS: frozenset[str] = frozenset({QUICK_SEND, QUICK_RESEND, QUICK_ARCHIVE})
#: A completed portion's ``kind``, the same words as ``backup_facts.KINDS``.
KINDS = ("full", "quick", "skipped", "snapshot", "unchanged")
KIND_FULL, KIND_QUICK, KIND_SKIPPED, KIND_SNAPSHOT, KIND_UNCHANGED = KINDS
#: Warnings, not refusals, for a rotation that failed after a backup that
#: succeeded: a failed listing removed nothing, a failed purge left the rest done.
ARCHIVE_LISTING_FAILED = "archive-listing-failed"
ARCHIVE_PURGE_FAILED = "archive-purge-failed"
#: The warning for an outside analysis share that is not a directory.
ANALYSIS_SHARE_ABSENT = "analysis-share-absent"
#: Where an outside share is mirrored under the snapshot root: not stamp shaped,
#: and one stable mirror rather than a copy per snapshot, which would fill a quota.
SHARE_DEST_DIRNAME = "analysis-share"
#: The share mirror's folder for a library with no identity a path can carry.
SHARE_UNRECORDED = "_unrecorded"
#: rclone's exit for a directory that does not exist (measured on the local backend).
RCLONE_DIRECTORY_NOT_FOUND = 3
#: Labels whose command transfers data, which a dry run neutralizes.
TRANSFERRING_LABELS: frozenset[str] = frozenset(
    {
        MIRROR, QUICK_SEND, QUICK_RESEND, QUICK_ARCHIVE, SNAPSHOT_DATABASE, SNAPSHOT_SETTINGS,
        SNAPSHOT_IDENTITY,
        SNAPSHOT_SHARE,
        RESTORE_MIRROR,
        RESTORE_DATABASE,
        RESTORE_SHARE,
    }
)

#: Warning: no identity marker was written, so a restore pulls it only by name.
SNAPSHOT_IDENTITY_NOT_WRITTEN = "snapshot-identity-not-written"
#: Warning: the record a quick run reads was not kept, so the next run is full.
BACKUP_RECORD_NOT_KEPT = "backup-record-not-kept"
#: A snapshot's identity marker: an empty file beside ``db/``, never in it.
IDENTITY_MARKER_PREFIX = "library-volume."
#: Dated archive folders a prune keeps; every folder since the last completed
#: mirror counts as one slot, so a retry never purges an attempt's overwrites.
DEFAULT_ARCHIVE_KEEP = 1
#: Mirrors a root holding none of the library's files deleting nothing: rclone
#: fails instead, counting a move into ``--backup-dir`` as a delete.
MOVE_NOTHING = ("--max-delete", "0")
#: One recursive listing of the remote; it changes nothing about what is compared.
FAST_LIST = "--fast-list"
#: The ways a run compared, as the words a report carries.
COMPARISON_FAST = "fast"
COMPARISON_FULL = "full"
COMPARISON_QUICK = "quick"
#: What makes rclone log its final totals as JSON: without the level they are
#: below what it prints, and a zero interval logs none.
MIRROR_STATS_ARGS: tuple[str, ...] = (
    "--use-json-log",
    "--stats", "1h",
    "--stats-log-level", "NOTICE",
)


class Refusal(StrEnum):
    """Why a portion will not run: one diagnosis with one fix per member, each
    with a reserved exit code."""

    RCLONE_MISSING = "rclone-missing"
    REMOTE_NOT_CONFIGURED = "remote-not-configured"
    DESTINATION_NOT_CONFIGURED = "destination-not-configured"
    LIBRARY_ROOT_ABSENT = "library-root-absent"
    # The root is not provably this library: another volume than the one
    # recorded (fixed by mounting the right one), or a folder holding none of
    # its files (also fixed by saying it was emptied on purpose).
    LIBRARY_ROOT_FOREIGN = "library-root-foreign"
    LIBRARY_ROOT_UNPROVEN = "library-root-unproven"
    REKORDBOX_RUNNING = "rekordbox-running"
    # The scan met a process it could not read, so "quit rekordbox" would be
    # false; the database portion refuses alone.
    REKORDBOX_ABSENCE_UNCONFIRMED = "rekordbox-absence-unconfirmed"
    DATABASE_ABSENT = "database-absent"
    RESTORE_NOT_CONFIRMED = "restore-not-confirmed"
    RESTORE_TARGET_ABSENT = "restore-target-absent"
    NO_SNAPSHOT_AVAILABLE = "no-snapshot-available"
    # A remote listing that failed, fixed by checking the remote and its
    # credential rather than by taking a backup.
    SNAPSHOT_LISTING_FAILED = "snapshot-listing-failed"
    # A transfer that was attempted and failed, unlike the conditions above.
    RESTORE_TRANSFER_FAILED = "restore-transfer-failed"
    # Retype the stamp; pick this library's snapshot or name its volume; name
    # a snapshot that predates the marker.
    SNAPSHOT_NAME_INVALID = "snapshot-name-invalid"
    SNAPSHOT_LIBRARY_MISMATCH = "snapshot-library-mismatch"
    SNAPSHOT_IDENTITY_UNRECORDED = "snapshot-identity-unrecorded"


#: Every refusal, derived so the reservation check cannot fall behind.
REFUSALS: tuple[Refusal, ...] = tuple(Refusal)


class BackupRefused(Exception):
    """A whole-run refusal. Per-portion refusals are reported, not raised."""

    def __init__(self, refusal: Refusal, detail: str) -> None:
        super().__init__(detail)
        self.refusal = refusal
        self.detail = detail


@dataclass(frozen=True, slots=True)
class Command:
    """One external invocation, as data, so a plan can be shown before it runs."""

    label: str
    argv: tuple[str, ...]
    #: What the runner pipes to the program, or None: a quick run's paths, read
    #: with ``--files-from-raw -``.
    feed: str | None = None


@dataclass(frozen=True, slots=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""
    #: Wall clock seconds, or None (never zero) when the runner did not time it.
    elapsed: float | None = None


Runner = Callable[[Command], CommandResult]

#: The destructive session gates as a seam: a callable returning a context
#: manager, the real gates, a pass-through, or a caller's open guard.
GateGuard = Callable[[], AbstractContextManager[object]]

#: The session log's workflow label for a restore.
RESTORE_WORKFLOW = "backup-restore"


def _restore_gates(cfg: config.Config, gates: GateGuard | None) -> AbstractContextManager[object]:
    """The gates a restore runs behind, real unless the caller injected otherwise.

    The library lock, the backup acknowledgment and the volume identity bind to
    destruction, not to database writes. It declares itself a RECOVERY, so a
    library latched ``committed-unverified`` does not refuse the restore its
    latch names as the remedy; all three gates still apply.
    """
    if gates is not None:
        return gates()
    return session.assert_gates(cfg, workflow=RESTORE_WORKFLOW, intent=session.Intent.RECOVERY)


def _warning(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


@dataclass(frozen=True, slots=True)
class PortionPlan:
    """What one portion will do, or why it will not.

    A refused portion carries no commands. ``warnings`` is what the run will
    not cover, carried to the outcome whether or not the portion runs.
    """

    portion: backup_facts.Portion
    refusal: Refusal | None = None
    detail: str = ""
    commands: tuple[Command, ...] = field(default_factory=tuple)
    warnings: tuple[Mapping[str, str], ...] = field(default_factory=tuple)
    #: One of :data:`KINDS`, or empty for a refused portion. A ``skipped`` or
    #: ``unchanged`` portion runs no command and still publishes its age.
    kind: str = ""
    #: Why the files portion is a full run, or empty.
    why: str = ""
    #: What the walk found changed since the record, or None where unread.
    changes: Mapping[str, int] | None = None
    #: What a completed run settles its record from: the walk, or the
    #: fingerprint. None keeps no record.
    basis: object = field(default=None, compare=False, repr=False)
    #: The token of the record a skip was proved against.
    record_token: str = ""
    #: The device the root was on when planned, which the full mirror is held
    #: to; -1 holds it to nothing and fails it.
    root_dev: int = -1
    #: Files outside the state folder the plan found: the census kept.
    held: int = 0

    @property
    def will_run(self) -> bool:
        return self.refusal is None and (bool(self.commands) or self.kind in _NOTHING_TO_SEND)


#: The kinds that complete with no command, because nothing changed.
_NOTHING_TO_SEND = frozenset({KIND_SKIPPED, KIND_UNCHANGED})


@dataclass(frozen=True, slots=True)
class BackupPlan:
    """The whole run, one entry per portion in declaration order. ``archive_keep``
    rides the plan so the preview and the run cannot disagree on it."""

    stamp: str
    portions: tuple[PortionPlan, ...]
    archive_keep: int = DEFAULT_ARCHIVE_KEEP

    def portion(self, which: backup_facts.Portion) -> PortionPlan:
        for entry in self.portions:
            if entry.portion is which:
                return entry
        raise KeyError(f"no plan for portion {which!r}")

    @property
    def refusals(self) -> tuple[PortionPlan, ...]:
        return tuple(p for p in self.portions if p.refusal is not None)


@dataclass(frozen=True, slots=True)
class PortionOutcome:
    """What one portion did, including what it could not finish but survived.

    ``warnings`` are real conditions that are not failures, as ``code`` and
    ``message`` pairs. Mapping fields make an instance unhashable, which is
    safe only while nothing hashes one.
    """

    portion: backup_facts.Portion
    ran: bool
    refusal: Refusal | None = None
    detail: str = ""
    results: tuple[CommandResult, ...] = field(default_factory=tuple)
    warnings: tuple[Mapping[str, str], ...] = field(default_factory=tuple)
    #: The commands as run, index for index with ``results``, so a failed
    #: return code has its argv beside it.
    commands: tuple[Command, ...] = field(default_factory=tuple)
    #: What the comparison did, from the command as run, or None with no mirror.
    comparison: Mapping[str, object] | None = None
    #: The plan's kind, reason and changes.
    kind: str = ""
    why: str = ""
    changes: Mapping[str, int] | None = None
    #: Wall clock seconds the portion took, its walk included.
    seconds: float | None = None


@dataclass(frozen=True, slots=True)
class BackupOutcome:
    """What one run of a plan did, including whether it was a rehearsal.

    ``dry_run`` is the value the run executed under, so a rehearsal can never
    report as a run that copied and published.
    """

    stamp: str
    portions: tuple[PortionOutcome, ...]
    dry_run: bool = False

    @property
    def ok(self) -> bool:
        """True when every portion planned to run completed; a refused portion
        does not fail the run."""
        return all(p.refusal is not None or p.ran for p in self.portions)


def settings_directories(
    *, home: Path | None = None, platform: str | None = None
) -> tuple[Path, ...]:
    """rekordbox's own settings directories on this platform, those that exist.
    They ride the database portion: they point at the database, and the running
    application writes them."""
    base = home or Path.home()
    relatives = _SETTINGS_DIRS_BY_PLATFORM.get(sys.platform if platform is None else platform, ())
    return tuple(p for p in (base / rel for rel in relatives) if p.is_dir())


def _require_destinations(cfg: config.Config) -> None:
    """Refuse the whole run before anything when a destination is not configured."""
    if not (cfg.backup.remote or "").strip():
        raise BackupRefused(
            Refusal.REMOTE_NOT_CONFIGURED,
            "no backup remote is configured. Cratekit ships no destination: the remote names an "
            "account that belongs to the user, so it is captured at setup and never defaulted.",
        )
    keys = ("dest", "archive_root", "db_dest_root")
    missing = [f"backup.{key}" for key in keys if not (getattr(cfg.backup, key) or "").strip()]
    if missing:
        raise BackupRefused(
            Refusal.DESTINATION_NOT_CONFIGURED,
            f"these backup destinations are not configured: {', '.join(missing)}. The mirror, the "
            f"dated archive, and the database snapshots are three distinct places on purpose, so "
            f"one of them being unset is not something to guess at.",
        )


def _rclone() -> str:
    """The rclone path, or a refusal in this module's own cause."""
    try:
        return binaries.resolve("rclone")
    except binaries.BinaryNotFound as exc:
        raise BackupRefused(
            Refusal.RCLONE_MISSING,
            f"{exc} It is the one program that talks to the remote, so nothing "
            f"here can proceed without it.",
        ) from exc


def stamp_for(now: datetime) -> str:
    """The dated folder one run writes into: UTC, so it sorts as text, which the
    prune and the newest snapshot rely on."""
    return now.astimezone(timezone.utc).strftime(_STAMP_FORMAT)


_STAMP_FORMAT = "%Y-%m-%dT%H%M%SZ"
_STAMP_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{6}Z")
#: What a refusal shows; a test holds it to :func:`is_stamp`.
STAMP_EXAMPLE = "2026-01-31T235959Z"


def is_stamp(value: str) -> bool:
    """Whether ``value`` is a folder name :func:`stamp_for` could have written.
    Shape and calendar both, so a value reaching a remote path is a name, never
    a path."""
    if not _STAMP_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _STAMP_FORMAT)
    except ValueError:
        return False
    return True


#: The source system's dated folder, local time with an underscore, in the
#: same layout, so a restore can pull what it wrote.
_LEGACY_FORMAT = "%Y-%m-%d_%H%M%S"
_LEGACY_SHAPE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{6}")


def is_snapshot_name(value: str) -> bool:
    """Whether ``value`` names a dated snapshot folder, this product's or the
    source's: wider than :func:`is_stamp` and as safe. A source snapshot never
    carries a marker, so only a named restore pulls it."""
    if is_stamp(value):
        return True
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _LEGACY_FORMAT)
    except ValueError:
        return False
    return True


_MARKER_IDENTITY = re.compile(r"[0-9a-z][0-9a-z_-]*(?:\.[0-9a-z_-]+)*")


def identity_marker(identity: str | None) -> str | None:
    """The marker filename for one volume identity, normalized, or None for an
    identity that is not plainly a name, which must never reach a path."""
    if identity is None:
        return None
    folded = preflight.normalize_identity(identity)
    if not _MARKER_IDENTITY.fullmatch(folded):
        return None
    return IDENTITY_MARKER_PREFIX + folded


def _exclude_args(patterns: Sequence[str]) -> tuple[str, ...]:
    return tuple(arg for pattern in patterns for arg in ("--exclude", pattern))


def database_fileset(cfg: config.Config) -> tuple[Path, ...]:
    """The database and its SQLite sidecars as one set, from the state inventory,
    so a copy never travels without its write-ahead log."""
    return (config.state_path("rekordbox_db", cfg), *config.sidecar_paths("rekordbox_db", cfg))


def _mirror_excludes(cfg: config.Config) -> tuple[str, ...]:
    """Volume clutter, plus the database fileset anchored at the volume root."""
    root = cfg.library.root
    patterns = list(VOLUME_EXCLUDES)
    for path in database_fileset(cfg):
        try:
            patterns.append("/" + path.relative_to(root).as_posix())
        except ValueError:
            # A database outside the library root is not in the mirror's tree.
            continue
    return tuple(patterns)


def plan_backup(
    cfg: config.Config, *, now: datetime | None = None,
    process_lister: ProcessLister | None = None, archive_keep: int = DEFAULT_ARCHIVE_KEEP,
    settings_dirs: Sequence[Path] | None = None, full: bool = False, check: bool = False,
    only: backup_facts.Portion | None = None, emptied: bool = False,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> BackupPlan:
    """Decide what a run would do, for the dry run and the run alike. Touches no
    remote and copies nothing.

    ``full`` lists the remote folder by folder; ``check`` (or ``full``) is a full
    check, comparing every file and snapshotting the database regardless.
    Otherwise files run full only for a reason, else quick or skipped, and the
    database is snapshotted only when it changed. ``only`` plans one portion.
    The files portion first proves the root is the library by volume identity
    and census; ``emptied`` is the only way past the census.
    """
    _require_destinations(cfg)
    moment = now or datetime.now(timezone.utc)
    stamp = stamp_for(moment)
    rclone = binaries.find("rclone")
    portions: list[PortionPlan] = []
    wanted = tuple(p for p in backup_facts.Portion if only is None or p is only)

    if rclone is None:
        why = (
            "rclone was not found. Every portion needs it: it is the one program that talks "
            "to the remote."
        )
        refused = (PortionPlan(p, refusal=Refusal.RCLONE_MISSING, detail=why) for p in wanted)
        return BackupPlan(stamp=stamp, archive_keep=archive_keep, portions=tuple(refused))

    if backup_facts.Portion.FILES in wanted:
        asked = "a full check was asked for" if check or full else _full_reason(cfg, now=moment)
        portions.append(
            _plan_files(
                cfg, rclone=rclone, stamp=stamp, archive_keep=archive_keep, full=full, asked=asked,
                emptied=emptied,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
        )
    if backup_facts.Portion.DATABASE in wanted:
        portions.append(
            _plan_database(
                cfg, rclone=rclone, stamp=stamp, process_lister=process_lister,
                settings_dirs=settings_dirs,
                snapshot_anyway=check or full,
            )
        )
    return BackupPlan(stamp=stamp, archive_keep=archive_keep, portions=tuple(portions))


def _full_reason(cfg: config.Config, *, now: datetime) -> str:
    """Why the next run must be a full check by the calendar, or an empty string,
    read off the files portion's age; an unreadable fact file is a reason too."""
    try:
        reported = backup_facts.ages(cfg, now=now)
    except backup_facts.BackupFactsUnreadable as exc:
        return f"the record of the last full check could not be read: {exc}"
    files = next(entry for entry in reported if entry.portion is backup_facts.Portion.FILES)
    return files.full_check_overdue


#: The summary key under which a files fact carries its record's token.
RECORD_TOKEN = "record"


def _strike_token(cfg: config.Config) -> None:
    """Strike the record's token from the library's files fact, leaving the rest
    as it was; a fact with no token is not rewritten."""
    fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    if fact is None or fact.summary is None or RECORD_TOKEN not in fact.summary:
        return
    backup_facts.record(
        cfg, backup_facts.Portion.FILES, completed_at=fact.completed_at,
        destination=fact.destination, kind=fact.kind,
        summary={name: value for name, value in fact.summary.items() if name != RECORD_TOKEN},
    )


def _record_unpublished(cfg: config.Config, manifest: backup_record.Manifest) -> str:
    """Why the files fact says another writer reached the mirror, or empty.

    The record is this installation's and the mirror is not: another
    installation, or an older build, publishes a files fact without this
    record's token, so unless the fact carries it the run is full.
    """
    try:
        fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    except backup_facts.BackupFactsUnreadable as exc:
        return f"the record of the last backup's age could not be read: {exc}"
    held = (fact.summary or {}).get(RECORD_TOKEN) if fact is not None else None
    if fact is None or not manifest.token or held != manifest.token:
        return (
            "the library's backup age was published by a run that did not keep "
            "this record, another installation or an older build, so the mirror "
            "may have changed since it was kept"
        )
    return ""


def _self_written(cfg: config.Config) -> frozenset[str]:
    """The fact file under the library root, which every run rewrites after its
    transfer, so counting it would make every run a change."""
    try:
        rel = config.state_path("backup_facts", cfg).relative_to(cfg.library.root)
    except ValueError:
        return frozenset()
    return frozenset({rel.as_posix()})


def _plan_files(
    cfg: config.Config, *, rclone: str, stamp: str, archive_keep: int, full: bool = False,
    asked: str = "a full check was asked for", emptied: bool = False,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> PortionPlan:
    """The files portion: a full check, a quick run of the difference, or a skip.

    ``asked`` is why a full check is due, or empty; the library is walked either
    way, to settle the next record. A root not proven to be the library (an
    empty mount point would empty the mirror) refuses with no command."""
    root = cfg.library.root
    if not root.is_dir():
        return PortionPlan(
            portion=backup_facts.Portion.FILES, refusal=Refusal.LIBRARY_ROOT_ABSENT,
            detail=f"the library root {root} is not a directory; mount the volume first",
        )
    foreign = _not_the_recorded_volume(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    if foreign:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_FOREIGN,
            detail=foreign,
        )
    excludes = _mirror_excludes(cfg)
    state_dirname = cfg.library.state_dirname
    why = asked
    manifest: backup_record.Manifest | None = None
    if not why:
        manifest, why = backup_record.read_manifest()
    if manifest is not None and not why:
        why = backup_record.manifest_mismatch(manifest, cfg, excludes)
    if manifest is not None and not why:
        why = _record_unpublished(cfg, manifest)
    trusted = manifest.entries if manifest is not None and not why else {}
    try:
        root_dev = os.stat(root).st_dev
    except OSError:
        root_dev = -1
    try:
        hashed = [rel for rel, entry in trusted.items() if entry.sha256 is not None]
        before = backup_record.walk(root, excludes, hash_paths=hashed)
    except backup_record.WalkRefused as exc:
        before = None
        why = why or f"the library could not be walked: {exc}"
    if before is not None:
        root_dev = before.root_dev
        anything = bool(before.entries)
        held = backup_record.count_held(before.entries, state_dirname)
    else:
        # The walk refused, so the floor and the census are counted another way.
        anything, held = backup_record.probe(root, excludes, state_dirname)
    unproven, new_library = _unproven(cfg, anything=anything, held=held, emptied=emptied)
    if unproven:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_UNPROVEN,
            detail=unproven,
        )
    proof = {"root_dev": root_dev, "held": held}
    # A ROOT HOLDING NONE OF THE LIBRARY'S FILES IS MIRRORED DELETING NOTHING,
    # whatever is on record, unless emptied on purpose: a failed run can have
    # sent files no census counted. A skip runs nothing and a quick run archives
    # only paths the record held, so both are planned as usual.
    move_nothing = held == 0 and not emptied
    if new_library:
        why = (
            "the library holds no file outside its state folder and no backup of it is on record, "
            "so it runs as a new library's first backup, which deletes nothing from the mirror"
        )
    if not why and before is not None:
        found = backup_record.difference(trusted, before.entries, self_written=_self_written(cfg))
        if not found.anything:
            return PortionPlan(
                portion=backup_facts.Portion.FILES, kind=KIND_SKIPPED,
                detail="nothing changed since the last completed backup",
                changes=found.counts(), basis=before,
                record_token=manifest.token if manifest is not None else "",
                **proof,
            )
        uncomposed = backup_record.first_uncomposed(found.paths)
        if len(found.paths) > backup_record.QUICK_LIMIT:
            why = (
                f"{len(found.paths)} paths changed, more than the "
                f"{backup_record.QUICK_LIMIT} a quick run is for"
            )
        elif uncomposed is not None:
            why = (
                f"the changed name {uncomposed!r} is not in composed Unicode form, "
                f"and a quick run looks each name up on the remote, where a remote "
                f"that composes names would not find it"
            )
        else:
            return PortionPlan(
                portion=backup_facts.Portion.FILES, kind=KIND_QUICK,
                commands=_quick_commands(
                    cfg, rclone=rclone, stamp=stamp, archive_keep=archive_keep, found=found
                ),
                detail=_rotation_detail(archive_keep), changes=found.counts(), basis=before,
                **proof,
            )
    return PortionPlan(
        portion=backup_facts.Portion.FILES, kind=KIND_FULL, why=why,
        commands=_full_commands(
            cfg, rclone=rclone, stamp=stamp, archive_keep=archive_keep, full=full,
            move_nothing=move_nothing,
        ),
        detail=_rotation_detail(archive_keep), basis=before, **proof,
    )


def _not_the_recorded_volume(
    cfg: config.Config, *, identity_provider: preflight.IdentityProvider | None,
    mount_enumerator: preflight.MountEnumerator | None,
) -> str:
    """Why the root is on a volume other than the library's, or an empty string.

    Through the volume gate, read for what it found: a recorded identity read
    elsewhere refuses. An identity unread, never recorded, or whose read raised
    is no answer and is left to the census, which holds on every platform.
    """
    try:
        session.assert_volume_identity(
            cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
        )
    except CratekitError as exc:
        found = exc.cause.detail or {}
        recorded, observed = found.get("recorded_identity"), found.get("observed_identity")
        if recorded is None or observed is None:
            return ""
        return (
            f"the volume at the library root {cfg.library.root} is not the one "
            f"recorded for this library (recorded {recorded}, observed {observed}), "
            f"so the folder there is not proven to be this library and nothing "
            f"was sent or archived; mount the library's own volume and back up again"
        )
    except Exception:  # noqa: BLE001 - an unread identity is left to the census
        return ""
    return ""


def _quick_commands(
    cfg: config.Config, *, rclone: str, stamp: str, archive_keep: int,
    found: backup_record.Difference,
) -> tuple[Command, ...]:
    """A quick run's commands: the difference sent, rewritten and archived. None
    lists the remote (``--no-traverse``), and the archive is this run's dated
    folder, so a quick run is undoable as a full one is."""
    root, dest = str(cfg.library.root), str(cfg.backup.dest)
    archive = f"{cfg.backup.archive_root}/{stamp}"
    listed = ("--files-from-raw", "-", "--no-traverse")
    commands: list[Command] = []
    send = (*found.added, *found.changed)
    if send:
        commands.append(
            Command(
                label=QUICK_SEND,
                argv=(
                    rclone, "copy", root, dest, *listed, "--backup-dir", archive,
                    "--transfers", "8", "--checkers", "16", *MIRROR_STATS_ARGS,
                ),
                feed=backup_record.paths_list(send),
            )
        )
    resend = tuple(sorted((*found.rewritten, *found.doubted)))
    if resend:
        # THE ONE PLACE A TIME IS IGNORED: these kept size and time while their
        # content moved, or were doubts, and rclone would find each current.
        commands.append(
            Command(
                label=QUICK_RESEND,
                argv=(
                    rclone, "copy", root, dest, *listed, "--ignore-times",
                    "--backup-dir", archive, "--transfers", "8", "--checkers", "16",
                    *MIRROR_STATS_ARGS,
                ),
                feed=backup_record.paths_list(resend),
            )
        )
    if found.removed:
        # A path already gone from the remote is no error to rclone, so a
        # retried run archives what is left and nothing else.
        moved = (rclone, "move", dest, archive, *listed, *MIRROR_STATS_ARGS)
        feed = backup_record.paths_list(found.removed)
        commands.append(Command(label=QUICK_ARCHIVE, argv=moved, feed=feed))
    if archive_keep >= 0:
        commands.append(_prune_listing(cfg, rclone))
    return tuple(commands)


def _prune_listing(cfg: config.Config, rclone: str) -> Command:
    listing = (rclone, "lsf", f"{cfg.backup.archive_root}/", "--dirs-only")
    return Command(label=PRUNE_ARCHIVE, argv=listing)


def _full_commands(
    cfg: config.Config, *, rclone: str, stamp: str, archive_keep: int, full: bool,
    move_nothing: bool = False,
) -> tuple[Command, ...]:
    """The full check, the mirror and its rotation; ``move_nothing`` adds
    :data:`MOVE_NOTHING` for a root holding none of the library's files."""
    root = cfg.library.root
    archive = f"{cfg.backup.archive_root}/{stamp}"
    commands = [
        Command(
            label=MIRROR,
            argv=(
                rclone, "sync", str(root), str(cfg.backup.dest),
                *_exclude_args(_mirror_excludes(cfg)),
                # What the sync would overwrite or delete moves here FIRST, so
                # one run is always undoable.
                "--backup-dir", archive,
                "--transfers", "8", "--checkers", "16",
                # The full mode is the absence of this one option and nothing else.
                *(() if full else (FAST_LIST,)),
                *(MOVE_NOTHING if move_nothing else ()),
                *MIRROR_STATS_ARGS,
            ),
        )
    ]
    if archive_keep >= 0:
        # Its own command, run only after the mirror succeeds, so a failed
        # backup never removes its rollback. A negative keep disables pruning.
        commands.append(_prune_listing(cfg, rclone))
    return tuple(commands)


def _rotation_detail(archive_keep: int) -> str:
    """What the plan says the rotation keeps, one sentence per behaviour of
    :func:`_prune_archive`."""
    if archive_keep < 0:
        return "keeping every dated archive folder"
    if archive_keep == 0:
        return "keeping no dated archive folder"
    return (
        f"keeping the newest {archive_keep} dated archive folder(s), and counting every folder "
        f"written since the last completed mirror as one of them"
    )


def subprocess_runner(command: Command) -> CommandResult:
    """Run one command with the fallback directories on PATH and no credentials."""
    import subprocess

    started = time.monotonic()
    completed = subprocess.run(
        list(command.argv), capture_output=True, text=True, env=binaries.subprocess_env(),
        check=False, **({"input": command.feed} if command.feed is not None else {}),
    )
    return CommandResult(
        returncode=completed.returncode, stdout=completed.stdout or "",
        stderr=completed.stderr or "",
        elapsed=time.monotonic() - started,
    )


def comparison_mode(command: Command) -> str:
    """Which listing one mirror command used, read off the command as run."""
    return COMPARISON_FAST if FAST_LIST in command.argv else COMPARISON_FULL


def _parsed(line: str) -> object:
    try:
        return json.loads(line)
    except ValueError:
        return None


def _logged(stderr: str) -> list[dict]:
    """The JSON objects one command logged, skipping every line that is not one."""
    return [entry for entry in map(_parsed, stderr.splitlines()) if isinstance(entry, dict)]


def _count(stats: Mapping[str, object], key: str) -> int | float | None:
    """One total, or None when rclone gave no number; a bool is refused, being
    an ``int`` to ``isinstance``."""
    value = stats.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def comparison_report(command: Command, result: CommandResult) -> dict[str, object]:
    """What one mirror's comparison did: the mode, the time, and the counts.

    A count that could not be read is None, never zero. ``checked`` is rclone's
    count of files found on both sides; ``seconds`` is the whole command, and
    ``transfer_seconds`` rclone's own total. The last totals logged are read.
    """
    stats: Mapping[str, object] = {}
    for entry in _logged(result.stderr):
        found = entry.get("stats")
        if isinstance(found, dict):
            stats = found
    return {
        "mode": comparison_mode(command),
        "seconds": result.elapsed,
        "checked": _count(stats, "checks"),
        "sent": _count(stats, "transfers"),
        "sent_bytes": _count(stats, "bytes"),
        "transfer_seconds": _count(stats, "transferTime"),
        # rclone's own names and counting; how many files went to the archive
        # is not derived from them.
        "renames": _count(stats, "renames"),
        "deletes": _count(stats, "deletes"),
    }


def _said(stderr: str) -> str:
    """What a failed command said, line by line: a logged object as its message,
    the totals dropped, and a plain line kept as written."""
    lines: list[str] = []
    for line in stderr.splitlines():
        entry = _parsed(line)
        if not isinstance(entry, dict):
            lines.append(line)
        elif "stats" not in entry:
            lines.append(str(entry.get("msg", "")))
    said = "\n".join(piece.strip() for piece in lines if piece.strip())
    return said or stderr.strip()


def _summary(
    entry: PortionPlan, comparison: Mapping[str, object] | None, seconds: float, *,
    token: str = "",
) -> dict[str, object]:
    """What a fact records about the run that completed it; ``record`` is the
    token a later quick run or skip trusts the record by."""
    out: dict[str, object] = {"seconds": round(seconds, 1)}
    if token:
        out[RECORD_TOKEN] = token
    if entry.why:
        out["why"] = entry.why
    if entry.changes is not None:
        out.update(entry.changes)
    if comparison is not None:
        for name in ("sent", "archived", "checked"):
            if comparison.get(name) is not None:
                out[name] = comparison[name]
    return out


def quick_report(ran: Sequence[tuple[Command, CommandResult]]) -> dict[str, object]:
    """What a quick run's commands did, summed from each command's totals:
    ``sent`` by the copies, ``archived`` by the move and the copies' archive,
    ``checked`` the paths a copy found current. A total any command did not
    give makes its sum None, never zero."""

    def total(labels: frozenset[str], key: str) -> int | float | None:
        found = [comparison_report(c, r)[key] for c, r in ran if c.label in labels]
        if not found:
            return 0
        if any(value is None for value in found):
            return None
        return sum(found)  # type: ignore[arg-type]

    sending = frozenset({QUICK_SEND, QUICK_RESEND})
    elapsed = [result.elapsed for _, result in ran]
    return {
        "mode": COMPARISON_QUICK,
        "seconds": None if any(e is None for e in elapsed) else sum(elapsed),  # type: ignore[arg-type]
        "sent": total(sending, "sent"),
        "sent_bytes": total(sending, "sent_bytes"),
        "checked": total(sending, "checked"),
        # rclone counts each move into the archive as a rename.
        "archived": total(QUICK_LABELS, "renames"),
    }


PAYLOAD_VERSION = 1


def _listed(command: Command) -> dict[str, int]:
    """How many paths a command read on standard input, never the paths."""
    if command.feed is None:
        return {}
    return {"paths": len(backup_record.paths_from(command.feed))}


def _kind_fields(kind: str, why: str, changes: Mapping[str, int] | None) -> dict:
    return {
        "kind": kind or None, "why": why or None,
        "changes": dict(changes) if changes is not None else None,
    }


def plan_payload(plan: BackupPlan) -> dict:
    """A plan as plain data. Human rendering stays with the CLI."""
    return {
        "payload_version": PAYLOAD_VERSION, "stamp": plan.stamp,
        "portions": [
            {
                "portion": entry.portion.value, "will_run": entry.will_run,
                "refusal": entry.refusal.value if entry.refusal else None, "detail": entry.detail,
                "commands": [
                    {"label": c.label, "argv": list(c.argv), **_listed(c)}
                    for c in entry.commands
                ],
                "warnings": [dict(warning) for warning in entry.warnings],
                **_kind_fields(entry.kind, entry.why, entry.changes),
            }
            for entry in plan.portions
        ],
    }


def outcome_payload(outcome: BackupOutcome) -> dict:
    """Render the outcome; nothing here interprets a return code. Fields that
    join leave ``PAYLOAD_VERSION`` as it is: it is bumped only when a field is
    removed or changes meaning."""
    return {
        "payload_version": PAYLOAD_VERSION, "stamp": outcome.stamp, "ok": outcome.ok,
        "dry_run": outcome.dry_run,
        "portions": [
            {
                "portion": entry.portion.value, "ran": entry.ran,
                "refusal": entry.refusal.value if entry.refusal else None, "detail": entry.detail,
                "warnings": [dict(warning) for warning in entry.warnings],
                "comparison": dict(entry.comparison) if entry.comparison is not None else None,
                # STRICT: both come from the same runner calls, and a mismatch
                # would pair a return code with the wrong argv.
                "commands": [
                    {
                        "label": command.label,
                        "argv": list(command.argv),
                        "returncode": result.returncode, **_listed(command),
                    }
                    for command, result in zip(entry.commands, entry.results, strict=True)
                ],
                **_kind_fields(entry.kind, entry.why, entry.changes),
                "seconds": entry.seconds,
            }
            for entry in outcome.portions
        ],
    }


def dry_run_argv(command: Command) -> tuple[str, ...]:
    """The same command, made to report instead of transfer."""
    if command.label in TRANSFERRING_LABELS:
        return (*command.argv, "--dry-run")
    return command.argv


def run_backup(
    cfg: config.Config, plan: BackupPlan, *, runner: Runner = subprocess_runner,
    now: datetime | None = None, dry_run: bool = False, publish: bool = True,
) -> BackupOutcome:
    """Execute a plan and publish the age fact for each portion that completed.

    Published per portion and only on success, so a skipped portion keeps the
    age of its last real run. ``dry_run`` runs the same plan with every
    transferring command neutralized and publishes nothing.
    """
    moment = now or datetime.now(timezone.utc)
    outcomes: list[PortionOutcome] = []
    if dry_run:
        publish = False

    for entry in plan.portions:
        if entry.refusal is not None:
            outcomes.append(PortionOutcome(
                portion=entry.portion, ran=False, refusal=entry.refusal,
                detail=entry.detail, warnings=entry.warnings,
            ))
            continue

        started = time.monotonic()
        planned = {"kind": entry.kind, "why": entry.why, "changes": entry.changes}
        if not dry_run and entry.commands:
            # THE RECORD GOES BEFORE THE FIRST TRANSFER IT DESCRIBES, and one that
            # cannot be removed stops the portion, so a failed run never leaves a
            # record that answers "nothing changed" over a half rewritten remote.
            try:
                backup_record.invalidate(_record_path(entry.portion))
                if entry.portion is backup_facts.Portion.FILES:
                    # The token goes from the fact too, so every installation's
                    # record is untrusted until a completed run publishes again.
                    _strike_token(cfg)
            # An unreadable fact file raises out of here, before anything is sent.
            except OSError as exc:
                outcomes.append(PortionOutcome(
                    portion=entry.portion, ran=False,
                    detail=(
                        f"{entry.portion.value} portion failed before sending "
                        f"anything: the record of the last backup could not be "
                        f"removed ahead of the transfer: {exc}"
                    ),
                    warnings=entry.warnings, **planned,
                ))
                continue

        results: list[CommandResult] = []
        warnings: list[Mapping[str, str]] = list(entry.warnings)
        failed: CommandResult | None = None
        # Every runner call goes through ``recorded``, the prune's included, so
        # ``executed`` and ``results`` are built by the same calls.
        executed: list[Command] = []
        comparison: Mapping[str, object] | None = None
        quick: list[tuple[Command, CommandResult]] = []
        marker_failed = False

        def recorded(command: Command, _executed: list[Command] = executed) -> CommandResult:
            _executed.append(command)
            return runner(command)

        for command in entry.commands:
            if command.label == PRUNE_ARCHIVE:
                # A failed rotation does not fail a portion whose mirror
                # completed, and is reported as a warning. A preview is the same
                # call with the purge suppressed.
                pruned, warning = _prune_archive(
                    cfg, command,
                    runner=recorded, keep=plan.archive_keep,
                    purge=not dry_run,
                )
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
            if dry_run:
                command = Command(
                    label=command.label, argv=dry_run_argv(command), feed=command.feed
                )
            elif command.label in QUICK_LABELS and isinstance(entry.basis, backup_record.Walk):
                # THE PLAN'S WALK CAN BE MINUTES OLD: each quick command runs only
                # while the root is the walked volume, and an archive only while
                # every removed path is still absent.
                stale = backup_record.still_removed(
                    cfg.library.root, entry.basis.root_dev,
                    backup_record.paths_from(command.feed)
                    if command.label == QUICK_ARCHIVE else (),
                )
                if stale:
                    failed = CommandResult(returncode=1, stderr=f"nothing was archived: {stale}")
                    break
            elif command.label == MIRROR:
                # The same question of the full sync: the root must still be the
                # planned device and, where it held the library's files, hold one.
                lost = backup_record.root_still_holds(
                    cfg.library.root, entry.root_dev, _mirror_excludes(cfg),
                    cfg.library.state_dirname, files=entry.held != 0,
                )
                if lost:
                    failed = CommandResult(
                        returncode=1, stderr=f"nothing was sent or archived: {lost}"
                    )
                    break
            result = recorded(command)
            results.append(result)
            if command.label == MIRROR:
                # Read whether or not it succeeded, to say how far it got.
                comparison = comparison_report(command, result)
            if command.label in QUICK_LABELS:
                quick.append((command, result))
                comparison = quick_report(quick)
            if result.returncode != 0 and command.label == SNAPSHOT_IDENTITY:
                marker_failed = True
                # NOT A FAILURE: the whole database set has copied. What is lost
                # is said: the snapshot is unmarked and pulled only by name.
                warnings.append(_warning(
                    SNAPSHOT_IDENTITY_NOT_WRITTEN,
                    f"the database was copied and the marker saying which library it was taken "
                    f"from could not be written (exit {result.returncode}). A restore will "
                    f"pull this snapshot only when its stamp is named",
                ))
                continue
            if result.returncode != 0:
                failed = result
                break

        if failed is not None:
            said = _said(failed.stderr)[-400:]
            if (
                executed
                and executed[-1].label == MIRROR
                and _moves_nothing(executed[-1])
                # rclone names the option it stopped on, "max-delete
                # threshold reached", read off the option itself.
                and MOVE_NOTHING[0].lstrip("-") in failed.stderr
            ):
                said += (
                    f". The library holds none of its files outside its state folder, so this "
                    f"mirror was told to delete nothing from the remote, and the remote holds "
                    f"files it would have moved into the archive. Mount the library's volume and "
                    f"back up again; if the library was emptied on purpose, back it up with "
                    f"{EMPTIED_FLAG}"
                )
            outcomes.append(PortionOutcome(
                portion=entry.portion, ran=False,
                detail=f"{entry.portion.value} portion failed: {said}",
                results=tuple(results), warnings=tuple(warnings),
                commands=tuple(executed), comparison=comparison,
                seconds=time.monotonic() - started, **planned,
            ))
            continue

        if publish and entry.commands:
            # Only after every command returned zero and only where a record was
            # removed above, so a skip keeps its record and a rehearsal neither.
            kept, token = _settle_record(cfg, entry, at=moment, marker_failed=marker_failed)
            if kept is not None:
                warnings.append(kept)
        else:
            # A skip carries the token of the record it was proved against.
            token = entry.record_token
        if publish and entry.portion is backup_facts.Portion.FILES:
            # The census every completed files portion leaves, a skip included.
            try:
                backup_record.write_census(cfg, entry.held, at=moment)
            except OSError as exc:
                warnings.append(_warning(
                    BACKUP_RECORD_NOT_KEPT,
                    f"the files portion completed and the count of the library's files the "
                    f"next backup is checked against was not kept: {exc}. The next backup "
                    f"proves the library against the older count, or the record",
                ))
        seconds = time.monotonic() - started + _walk_seconds(entry)
        if publish:
            backup_facts.record(
                cfg, entry.portion, completed_at=moment,
                destination=_destination_for(cfg, entry.portion),
                # Both read off the command as run: a portion with no mirror
                # moves neither, and a full check is the mirror in either mode.
                full_comparison=(
                    comparison is not None
                    and comparison["mode"] == COMPARISON_FULL
                ),
                full_check=(
                    comparison is not None
                    and comparison["mode"] in (COMPARISON_FAST, COMPARISON_FULL)
                ),
                kind=entry.kind or None,
                summary=_summary(entry, comparison, seconds, token=token),
            )
        outcomes.append(PortionOutcome(
            portion=entry.portion, ran=True, results=tuple(results),
            warnings=tuple(warnings), commands=tuple(executed), comparison=comparison,
            seconds=seconds, **planned,
        ))

    # ``dry_run`` and not ``not publish``: a real run asked to publish nothing
    # still copied the library.
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=dry_run)


def _moves_nothing(command: Command) -> bool:
    """Whether a mirror command was told to delete nothing from the remote."""
    argv = command.argv
    return any(argv[i : i + len(MOVE_NOTHING)] == MOVE_NOTHING for i in range(len(argv)))


def _record_path(portion: backup_facts.Portion) -> Path:
    """The record a portion's transfer would make untrue."""
    if portion is backup_facts.Portion.DATABASE:
        return backup_record.fingerprint_path()
    return backup_record.manifest_path()


def _walk_seconds(entry: PortionPlan) -> float:
    """The seconds the plan spent walking the library for this portion."""
    return entry.basis.seconds if isinstance(entry.basis, backup_record.Walk) else 0.0


def _settle_record(
    cfg: config.Config, entry: PortionPlan, *, at: datetime, marker_failed: bool = False
) -> tuple[Mapping[str, str] | None, str]:
    """Keep the record a completed portion leaves, or the warning why not, and
    the files token or "". Files trust what both walks agree on; the database
    fingerprint is retaken (processes scanned again first) and kept only when
    unchanged and the marker was written."""
    basis = entry.basis
    try:
        if isinstance(basis, backup_record.Walk):
            excludes = _mirror_excludes(cfg)
            after = backup_record.walk(
                cfg.library.root, excludes,
                hash_paths=[rel for rel, e in basis.entries.items() if e.sha256 is not None],
                racy_after_ns=basis.racy_after_ns,
            )
            token = backup_record.new_token()
            backup_record.write_manifest(
                cfg, excludes, backup_record.settled(basis, after), at=at, token=token
            )
            return None, token
        if isinstance(basis, tuple):
            key, fingerprint, fileset, folders, lister = basis
            if marker_failed:
                why = "the snapshot's identity marker could not be written"
            elif _not_confirmed_gone(lister):
                why = "rekordbox was not confirmed gone after the copy"
            elif backup_record.database_fingerprint(fileset, folders) == fingerprint:
                backup_record.write_fingerprint(key, fingerprint, at=at)
                return None, ""
            else:
                why = "the database or a folder beside it changed while it was copied"
        else:
            why = "what it held before the transfer could not be read"
    except (backup_record.WalkRefused, OSError) as exc:
        why = str(exc)
    return _warning(
        BACKUP_RECORD_NOT_KEPT,
        f"the {entry.portion.value} portion completed and the record the next run compares against "
        f"was not kept: {why}. The next backup of it is a full one",
    ), ""


def _not_confirmed_gone(lister: ProcessLister | None) -> bool:
    try:
        return bool(rekordbox_processes_running(lister=lister))
    except AbsenceUnconfirmed:
        return True


def _destination_for(cfg: config.Config, portion: backup_facts.Portion) -> str:
    if portion is backup_facts.Portion.DATABASE:
        return str(cfg.backup.db_dest_root or "")
    return str(cfg.backup.dest or "")


def _rotation_floor(cfg: config.Config) -> str | None:
    """The stamp of the last completed mirror to this destination, after which a
    dated folder belongs to the run now finishing, or None (no folder settled).
    An unreadable fact file raises, so no purge runs on it."""
    fact = backup_facts.read_facts(cfg).get(backup_facts.Portion.FILES)
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
    return stamp_for(fact.completed_at)


def _prune_archive(
    cfg: config.Config, listing: Command, *, runner: Runner, keep: int, purge: bool = True
) -> tuple[list[CommandResult], Mapping[str, str] | None]:
    """Remove all but the newest ``keep`` dated archive folders, after the mirror
    succeeded, and say so. A failed listing purges nothing; neither it nor a
    failed purge fails the portion, each returning one warning. ``purge`` false
    is the rehearsal. Folders after :func:`_rotation_floor`, read only here, are
    one slot unless ``keep`` is zero."""
    out: list[CommandResult] = []
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
            "message": (
                f"the archive rotation did not run: listing "
                f"{cfg.backup.archive_root}/ exited {result.returncode}, so "
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
            ),
        }
    if keep < 0 or not purge:
        return out, None
    floor = _rotation_floor(cfg)
    names = sorted(line.strip().rstrip("/") for line in result.stdout.splitlines() if line.strip())
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
    settled = names[: len(names) - len(held)]
    slots = keep - 1 if held else keep
    unremoved = 0
    for stale in settled[: max(0, len(settled) - slots)]:
        purged = runner(Command(
            label=PRUNE_ARCHIVE_FOLDER,
            # The same rclone the listing used, from its own argv, so the
            # one that deletes is never a second resolution.
            argv=(listing.argv[0], "purge", f"{cfg.backup.archive_root}/{stale}"),
        ))
        out.append(purged)
        if purged.returncode != 0:
            unremoved += 1
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
            "message": (
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
                f"under {cfg.backup.archive_root}/ could not be removed and will use remote space "
                f"until a later run removes them. The backup itself completed"
            ),
        }
    return out, None


def run_restore(
    plan: RestorePlan, cfg: config.Config, *, runner: Runner = subprocess_runner,
    dry_run: bool = False, gates: GateGuard | None = None,
) -> tuple[CommandResult, ...]:
    """Clear the stale sidecars before any command, then copy: never a stale log
    beside a database that has started to change. ``dry_run`` neutralizes the
    transfers and skips the clearing, which is itself destructive, and still
    passes the gates, so a rehearsal never previews a library being changed."""
    with _restore_gates(cfg, gates):
        if dry_run:
            # The rehearsal's results are read too, or a failing preview
            # would report as a passing one.
            return _ran(
                tuple(runner(Command(label=c.label, argv=dry_run_argv(c))) for c in plan.commands),
                plan,
            )
        plan.database_target.parent.mkdir(parents=True, exist_ok=True)
        for stale in plan.clears:
            stale.unlink(missing_ok=True)
        return _ran(tuple(runner(command) for command in plan.commands), plan)


def _ran(results: tuple[CommandResult, ...], plan: RestorePlan) -> tuple[CommandResult, ...]:
    """Every transfer's return code, read; raises on the first that failed, since
    a partly restored set matches nothing. The cleared sidecars are not put
    back, and the refusal says so."""
    # STRICT: both callers walk ``plan.commands`` once, so a length that differs
    # is a driver defect, and tolerating it would skip the tail unread.
    for command, result in zip(plan.commands, results, strict=True):
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
                f"the transfer {command.label!r} exited {result.returncode} and the restore did "
                f"not complete. The live companion files beside {plan.database_target.name} were "
                f"cleared before it began and have not been put back, so run the restore again "
                f"once the remote is reachable rather than opening the library first.",
            )
    return results


# The snapshot plans, re-exported. Imported last because that module reads this
# one's names: import this module, never that one first.
from cratekit.modules.tools.backup_snapshot import (  # noqa: E402, F401
    NEWEST_WALK,
    ResolvedSnapshot,
    RestorePlan,
    ShareRestore,
    _not_this_librarys,
    _outside_share,
    _plan_database,
    _plan_restore_inside_the_gates,
    _snapshot_names,
    absent_analysis_share,
    database_target_for,
    latest_snapshot,
    plan_restore,
    resolve_snapshot,
    share_destination,
    share_is_held,
    snapshot_filenames,
    snapshot_identities,
    snapshot_identity_warning,
)

__all__ = [
    "BACKUP_RECORD_NOT_KEPT", "COMPARISON_FAST", "COMPARISON_FULL", "COMPARISON_QUICK",
    "DEFAULT_ARCHIVE_KEEP", "FAST_LIST", "MIRROR", "MIRROR_STATS_ARGS", "PAYLOAD_VERSION",
    "QUICK_ARCHIVE", "QUICK_LABELS", "QUICK_RESEND", "QUICK_SEND", "KINDS", "KIND_FULL",
    "KIND_QUICK", "KIND_SKIPPED", "KIND_SNAPSHOT", "KIND_UNCHANGED", "RECORD_TOKEN",
    "REFUSALS", "REKORDBOX_PROCESSES", "RESTORE_WORKFLOW", "VOLUME_EXCLUDES",
    "BackupOutcome", "GateGuard", "BackupPlan", "BackupRefused", "Command", "CommandResult",
    "PortionOutcome", "PortionPlan", "Refusal", "ANALYSIS_SHARE_ABSENT", "LIST_SHARE",
    "LIST_SNAPSHOT_CONTENTS", "RESTORE_MIRROR", "RESTORE_SHARE", "SNAPSHOT_SHARE",
    "RestorePlan", "ShareRestore", "absent_analysis_share", "comparison_mode",
    "comparison_report", "database_fileset", "database_target_for", "dry_run_argv",
    "latest_snapshot", "plan_backup", "snapshot_filenames", "plan_payload", "plan_restore",
    "outcome_payload", "quick_report", "rekordbox_processes_running", "run_backup",
    "run_restore", "running_process_names", "share_destination", "share_is_held",
    "settings_directories", "stamp_for", "subprocess_runner",
]
