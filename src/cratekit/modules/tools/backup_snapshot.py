"""The dated database snapshot: its capture plan, which snapshot a restore pulls, and the restore.

:mod:`cratekit.modules.tools.backup` re-exports every name here and is the
module to import, since this one reads its names and is loaded through it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from cratekit.core import analysis_store, backup_facts, config, preflight
from cratekit.modules.tools import backup_record
from cratekit.modules.tools.backup import (
    ANALYSIS_SHARE_ABSENT,
    IDENTITY_MARKER_PREFIX,
    KIND_SNAPSHOT,
    KIND_UNCHANGED,
    LIST_SHARE,
    LIST_SNAPSHOT_CONTENTS,
    LIST_SNAPSHOT_IDENTITY,
    LIST_SNAPSHOTS,
    RCLONE_DIRECTORY_NOT_FOUND,
    RESTORE_DATABASE,
    RESTORE_MIRROR,
    RESTORE_SHARE,
    SHARE_DEST_DIRNAME,
    SHARE_UNRECORDED,
    SNAPSHOT_DATABASE,
    SNAPSHOT_IDENTITY,
    SNAPSHOT_IDENTITY_NOT_WRITTEN,
    SNAPSHOT_SETTINGS,
    SNAPSHOT_SHARE,
    STAMP_EXAMPLE,
    VOLUME_EXCLUDES,
    AbsenceUnconfirmed,
    BackupRefused,
    Command,
    GateGuard,
    PortionPlan,
    ProcessLister,
    Refusal,
    Runner,
    _exclude_args,
    _mirror_excludes,
    _rclone,
    _require_destinations,
    _restore_gates,
    _warning,
    database_fileset,
    identity_marker,
    is_snapshot_name,
    rekordbox_processes_running,
    settings_directories,
    subprocess_runner,
)


def _plan_database(
    cfg: config.Config, *, rclone: str, stamp: str, process_lister: ProcessLister | None,
    settings_dirs: Sequence[Path] | None, snapshot_anyway: bool = True,
) -> PortionPlan:
    """The database portion: a dated snapshot, or none when nothing changed.

    The fingerprint reads the live database, so it is taken only below the
    process check, with both rekordbox processes confirmed gone.
    ``snapshot_anyway`` is a full check's: snapshot whether or not it changed.
    """
    uncovered = absent_analysis_share(cfg)
    try:
        running = rekordbox_processes_running(lister=process_lister)
    except AbsenceUnconfirmed as exc:
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE, refusal=Refusal.REKORDBOX_ABSENCE_UNCONFIRMED,
            detail=(
                f"{exc.cause.message}, so no snapshot of the database was taken. "
                f"Previous dated snapshots remain the backstop."
            ),
            warnings=uncovered,
        )
    if running:
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE, refusal=Refusal.REKORDBOX_RUNNING,
            detail=(
                f"{', '.join(running)} is running, so the database may be mid-write. A copy taken "
                f"now opens cleanly and is silently missing whatever the agent was writing, which "
                f"is worse than no copy at all. Previous dated snapshots remain the backstop."
            ),
            warnings=uncovered,
        )
    database = config.state_path("rekordbox_db", cfg)
    if not database.is_file():
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE, refusal=Refusal.DATABASE_ABSENT,
            detail=f"no rekordbox database at the configured path {database}",
            warnings=uncovered,
        )

    destination = f"{cfg.backup.db_dest_root}/{stamp}"
    first = (rclone, "copy", str(database), f"{destination}/db/", "--transfers", "4")
    commands = [Command(label=SNAPSHOT_DATABASE, argv=first)]
    # Each present sidecar into the SAME folder under the database's label, the
    # one the dry run translator and the executor branch on; a checkpointed
    # database has none.
    for sidecar in config.sidecar_paths("rekordbox_db", cfg):
        if sidecar.is_file():
            sent = (rclone, "copy", str(sidecar), f"{destination}/db/")
            commands.append(Command(label=SNAPSHOT_DATABASE, argv=sent))
    # THE MARKER FOLLOWS THE WHOLE DATABASE SET AND PRECEDES THE SETTINGS: it
    # must not sit beside a copy that failed, and a snapshot whose settings
    # failed still holds a usable database.
    warnings = [*uncovered, *snapshot_identity_warning(cfg)]
    marker = identity_marker(cfg.library.volume_id)
    if marker is not None:
        touch = (rclone, "touch", f"{destination}/{marker}")
        commands.append(Command(label=SNAPSHOT_IDENTITY, argv=touch))
    resolved_settings = settings_directories() if settings_dirs is None else tuple(settings_dirs)
    share = _outside_share(cfg)
    carried_share = share if share is not None and share.is_dir() else None
    fileset = database_fileset(cfg)
    folders = (*resolved_settings, *((carried_share,) if carried_share is not None else ()))
    key = backup_record.fingerprint_key(cfg, marker)
    fingerprint = backup_record.database_fingerprint(fileset, folders)
    if not snapshot_anyway and fingerprint is not None:
        held = backup_record.read_fingerprint()
        if (
            held is not None
            and held.get("fingerprint") == fingerprint
            and all(held.get(name) == value for name, value in key.items())
        ):
            return PortionPlan(
                portion=backup_facts.Portion.DATABASE, kind=KIND_UNCHANGED,
                detail=(
                    "the database, its settings and its analysis share are what "
                    "the last completed snapshot copied, so no new one is taken"
                ),
                warnings=tuple(warnings),
            )
    basis = None if fingerprint is None else (key, fingerprint, fileset, folders, process_lister)
    for directory in resolved_settings:
        commands.append(Command(
            label=SNAPSHOT_SETTINGS,
            argv=(
                rclone, "copy", str(directory), f"{destination}/{directory.name}",
                "--transfers", "8", "--checkers", "16",
            ),
        ))
    # THE SHARE GOES LAST, AND IN THIS PORTION: rekordbox writes it while it
    # analyses, so it needs this portion's gate, and it is gigabytes, so a
    # failure costs the settings nothing. It still fails the portion.
    if carried_share is not None:
        share = carried_share
        kept = share_destination(cfg, identity=cfg.library.volume_id)
        commands.append(
            Command(
                label=SNAPSHOT_SHARE,
                argv=(
                    rclone, "sync", str(share), f"{kept}/current",
                    *_exclude_args(VOLUME_EXCLUDES),
                    # What this sync would overwrite or delete moves to a dated
                    # folder first, so an emptied share never empties its copy.
                    "--backup-dir", f"{kept}/archive/{stamp}",
                    "--transfers", "8", "--checkers", "16",
                ),
            )
        )
    return PortionPlan(
        portion=backup_facts.Portion.DATABASE, kind=KIND_SNAPSHOT, commands=tuple(commands),
        warnings=tuple(warnings), basis=basis,
    )


def snapshot_identity_warning(cfg: config.Config) -> tuple[Mapping[str, str], ...]:
    """A warning when this configuration's snapshots cannot say whose they are.
    Asked of the configuration, since a queued backup's plan reaches nobody."""
    if identity_marker(cfg.library.volume_id) is not None:
        return ()
    why = "not recorded" if cfg.library.volume_id is None else "not a plain name"
    return (_warning(
        SNAPSHOT_IDENTITY_NOT_WRITTEN,
        f"this snapshot will not say which library it was taken from, because "
        f"{config.VOLUME_IDENTITY_KEY} is {why}. A restore will pull it only when its stamp "
        f"is named",
    ),)


def _outside_share(cfg: config.Config) -> Path | None:
    """The analysis share when the mirror does NOT reach it, else None, asked of
    ``analysis_store`` so the backup and the analysis watch agree."""
    if analysis_store.watch_roots(cfg) == (Path(cfg.library.root),):
        return None
    return analysis_store.share_root(cfg)


def share_destination(cfg: config.Config, *, identity: str | None) -> str:
    """Where one library's outside share is mirrored on the remote, keyed by the
    volume identity through :func:`identity_marker`, so two libraries under one
    root never sync over each other."""
    marker = identity_marker(identity)
    key = SHARE_UNRECORDED if marker is None else marker[len(IDENTITY_MARKER_PREFIX):]
    return f"{cfg.backup.db_dest_root}/{SHARE_DEST_DIRNAME}/{key}"


def absent_analysis_share(cfg: config.Config) -> tuple[Mapping[str, str], ...]:
    """A warning when an outside analysis share is not there to be carried, which
    is normal before any analysis and also what a wrong ``db_path`` looks like.
    Asked of the configuration, since a queued backup's plan reaches nobody."""
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
    return (_warning(
        ANALYSIS_SHARE_ABSENT,
        f"the analysis share {share} sits outside the library root {cfg.library.root} and is not a "
        f"directory, so this backup carries no beat grids or analysis. That is expected only for a "
        f"library rekordbox has not analysed yet",
    ),)


class ShareRestore(StrEnum):
    """What a restore does about the analysis share, in one word.

    Four facts, so a boolean would fold two into "nothing was pulled". Single
    words, since a hyphenated value would read as cause shaped.
    """

    #: Under the library root, so the mirror half carries it.
    MIRRORED = "mirrored"
    #: Outside the root, held on the remote, and a transfer is planned.
    PULLED = "pulled"
    #: Outside the root and not on the remote: rows come back without grids.
    ABSENT = "absent"
    #: Outside the root and landing under the analysis watch, so not pulled and
    #: the remote not asked.
    WITHHELD = "withheld"


@dataclass(frozen=True, slots=True)
class RestorePlan:
    """What a restore will do, including the sidecars it clears first.

    ``absent_sidecars`` are the suffixes to write back that this snapshot does
    not hold (a checkpointed database has no log), named rather than
    transferred so a person is told they were absent.
    """

    target: Path
    database_target: Path
    snapshot: str | None
    clears: tuple[Path, ...]
    commands: tuple[Command, ...] = field(default_factory=tuple)
    absent_sidecars: tuple[str, ...] = field(default_factory=tuple)
    #: The identity the snapshot's marker records, or None for an unmarked
    #: snapshot pulled because it was named.
    recorded_volume: str | None = None
    #: What this restore does about the analysis share.
    share: ShareRestore = ShareRestore.MIRRORED


def database_target_for(cfg: config.Config, target: Path) -> Path:
    """Where the database lands under a restore target: the configured database
    path rebased from the library root, never an assumed vendor layout."""
    database = config.state_path("rekordbox_db", cfg)
    try:
        return target / database.relative_to(cfg.library.root)
    except ValueError:
        # A database outside the library root lands under its own name.
        return target / database.name


def latest_snapshot(cfg: config.Config, *, runner: Runner) -> str | None:
    """The newest dated snapshot on the remote by name, which is newest by time
    only because ``stamp_for`` writes a sortable UTC stamp, or None."""
    names = _snapshot_names(cfg, runner=runner)
    return names[-1] if names else None


def _snapshot_names(cfg: config.Config, *, runner: Runner) -> tuple[str, ...] | None:
    """Every dated snapshot folder on the remote, oldest first, or None if unlisted.

    Only names a backup could have written, so a hand made folder is never
    offered as the newest. None (no answer) and empty are different answers.
    """
    result = runner(Command(
        label=LIST_SNAPSHOTS,
        argv=(_rclone(), "lsf", f"{cfg.backup.db_dest_root}/", "--dirs-only"),
    ))
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A root no backup has written yet is an empty root, not a remote that
        # did not answer, and its answer is to take a backup.
        return ()
    if result.returncode != 0:
        return None
    return tuple(
        sorted(
            name
            for name in (line.strip().rstrip("/") for line in result.stdout.splitlines())
            if is_snapshot_name(name)
        )
    )


#: How many of the newest snapshots the default walk reads a marker from: a
#: judgement, enough to step over a week of another library's nightly backups.
NEWEST_WALK = 8


@dataclass(frozen=True, slots=True)
class ResolvedSnapshot:
    """Which snapshot a restore will pull, and whose its marker says it is.
    ``named`` is whether a person chose the stamp, which a stamp taken off a
    listing and handed down is not."""

    stamp: str
    recorded_volume: str | None
    named: bool


def snapshot_identities(cfg: config.Config, snapshot: str, *, runner: Runner) -> tuple[str, ...]:
    """Every identity a dated snapshot's markers record, normalized and sorted;
    empty means listed with no marker, and an empty marker is the empty identity.
    A failed listing raises, never passing as an unmarked snapshot."""
    result = runner(Command(
        label=LIST_SNAPSHOT_IDENTITY,
        argv=(_rclone(), "lsf", f"{cfg.backup.db_dest_root}/{snapshot}/", "--files-only"),
    ))
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A mistyped or pruned stamp. The folder is absent, so the remote and
        # its credential are not what a person should go and check.
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} was not found under {cfg.backup.db_dest_root}",
        )
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed, so which library it was taken from is unknown; a restore "
            f"is not planned against a snapshot this account cannot see",
        )
    found = {
        preflight.normalize_identity(name[len(IDENTITY_MARKER_PREFIX):])
        for name in (line.strip() for line in result.stdout.splitlines())
        if name.startswith(IDENTITY_MARKER_PREFIX)
    }
    return tuple(sorted(found))


def resolve_snapshot(
    cfg: config.Config, *, snapshot: str | None = None, snapshot_volume: str | None = None,
    accept_unrecorded: bool | None = None, runner: Runner = subprocess_runner,
) -> ResolvedSnapshot:
    """Decide which snapshot is pulled, and refuse one that is not this library's.

    Called before the verb's gate and again under it. A stamp's shape is checked
    before the remote is asked. ``snapshot_volume`` replaces the expected
    identity for this call. An unmarked snapshot is pulled only when named
    (``accept_unrecorded``). With no stamp, the first of the newest
    ``NEWEST_WALK`` marked for the expected identity is the answer.
    """
    _require_destinations(cfg)
    root = cfg.backup.db_dest_root
    wanted = snapshot_volume if snapshot_volume is not None else cfg.library.volume_id
    # AN EMPTY IDENTITY IS NO IDENTITY, or an empty marker and a blank expected
    # value would match each other and a snapshot naming nobody pass as verified.
    expected = (preflight.normalize_identity(wanted) or None) if wanted is not None else None
    whose = (
        f"the volume this restore was told to expect is {expected or 'empty'}"
        if snapshot_volume is not None
        else f"this library is recorded as volume {expected}"
        if expected is not None
        else f"this library records no {config.VOLUME_IDENTITY_KEY} to compare it with"
    )

    if snapshot is not None:
        if not is_snapshot_name(snapshot):
            raise BackupRefused(
                Refusal.SNAPSHOT_NAME_INVALID,
                f"{snapshot!r} is not a snapshot stamp. A stamp is the dated folder name a backup "
                f"wrote, like {STAMP_EXAMPLE}, and nothing else is put into a path on the remote.",
            )
        recorded = snapshot_identities(cfg, snapshot, runner=runner)
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
        accepted = True if accept_unrecorded is None else accept_unrecorded
        if not recorded and snapshot_volume is None and accepted:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=None, named=True)
        raise _not_this_librarys(
            cfg, snapshot, recorded, whose=whose, stated=snapshot_volume is not None
        )

    names = _snapshot_names(cfg, runner=runner)
    if names is None:
        raise BackupRefused(
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the dated database snapshots under {root} could not be listed, so "
            f"whether one exists is unknown; a restore is not planned against a "
            f"remote that did not answer",
        )
    if not names:
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"no dated database snapshot was found under {root}",
        )
    newest = names[::-1][:NEWEST_WALK]
    seen: dict[str, tuple[str, ...]] = {}
    for name in newest:
        seen[name] = snapshot_identities(cfg, name, runner=runner)
        if seen[name] == (expected,):
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
    raise _not_this_librarys(
        cfg, newest[0], seen[newest[0]], whose=whose, stated=snapshot_volume is not None,
        walked=len(newest),
    )


def _not_this_librarys(
    cfg: config.Config, stamp: str, recorded: tuple[str, ...], *, whose: str, stated: bool,
    walked: int = 0,
) -> BackupRefused:
    """The refusal for a snapshot not shown to be this library's: no marker (it
    predates markers or its backup was cut off, so both are said), two markers
    (no stated identity can vouch for it), or one marker for another volume."""
    root = cfg.backup.db_dest_root
    looked = (
        f"none of the {walked} newest snapshots under {root} says it was taken "
        f"from this library. The newest, {stamp},"
        if walked
        else f"the snapshot {stamp} under {root}"
    )
    if not recorded:
        if stated:
            return BackupRefused(
                Refusal.SNAPSHOT_LIBRARY_MISMATCH,
                f"{looked} does not say which library it was taken from, and {whose}. An expected "
                f"identity cannot be confirmed against a snapshot that records none.",
            )
        return BackupRefused(
            Refusal.SNAPSHOT_IDENTITY_UNRECORDED,
            f"{looked} does not say which library it was taken from. That is true of every "
            f"snapshot taken before identities were recorded, and also of one whose backup did not "
            f"finish, so check it holds a whole database before pulling it. It is pulled only when "
            f"it is named: --snapshot {stamp}",
        )
    if len(recorded) > 1:
        return BackupRefused(
            Refusal.SNAPSHOT_LIBRARY_MISMATCH,
            f"{looked} carries {len(recorded)} identities, "
            f"{' and '.join(r or '(empty)' for r in recorded)}, so two libraries "
            f"wrote into it and the database it holds is whichever copy landed "
            f"last. No expected volume can vouch for it; name another snapshot.",
        )
    return BackupRefused(
        Refusal.SNAPSHOT_LIBRARY_MISMATCH,
        f"{looked} says it was taken from the library on volume {recorded[0] or '(empty)'}, and "
        f"{whose}. Restoring it would put another library's database here.",
    )


def snapshot_filenames(cfg: config.Config, snapshot: str, *, runner: Runner) -> frozenset[str]:
    """The filenames a dated database snapshot holds. A failed listing refuses,
    since read as no sidecars it would report a restore the remote never saw."""
    result = runner(
        Command(
            label=LIST_SNAPSHOT_CONTENTS,
            argv=(
                _rclone(), "lsf",
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
                "--files-only",
            ),
        )
    )
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A backup cut off before its database folder was written. Nothing is
        # there to restore, which is an absence and not a remote fault.
        raise BackupRefused(
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} holds no "
            f"database folder, so there is nothing in it to restore",
        )
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed; a restore cannot be planned against a snapshot this "
            f"account cannot see",
        )
    return frozenset(
        line.strip().rstrip("/") for line in result.stdout.splitlines() if line.strip()
    )


def share_is_held(cfg: config.Config, *, identity: str | None, runner: Runner) -> bool:
    """Whether the remote holds a mirror of this library's outside share. An
    empty or missing directory is a backup from before the share was carried;
    any other failed listing refuses rather than reading as "no share"."""
    result = runner(Command(
        label=LIST_SHARE,
        argv=(_rclone(), "lsf", f"{share_destination(cfg, identity=identity)}/current/"),
    ))
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        return False
    if result.returncode != 0:
        raise BackupRefused(
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the analysis share mirror under {cfg.backup.db_dest_root} could not "
            f"be listed (exit {result.returncode}), so whether this library's beat "
            f"grids are in the backup is unknown; a restore is not planned against "
            f"a remote that did not answer",
        )
    return bool(result.stdout.strip())


def plan_restore(
    cfg: config.Config, *, target: Path | str, confirmed: bool, snapshot: str | None = None,
    snapshot_volume: str | None = None, accept_unrecorded: bool | None = None,
    include_mirror: bool = False, pull_share: bool = True, runner: Runner = subprocess_runner,
    process_lister: ProcessLister | None = None, gates: GateGuard | None = None,
) -> RestorePlan:
    """Decide a restore behind the gates; ``confirmed`` is a named decision, never
    a prompt. ``include_mirror`` adds the file half, a copy and never a sync, which
    would delete salvaged files. ``pull_share`` off withholds an outside share
    unasked. Only the configuration check, which resolves no path, precedes the
    gates: resolving a path against the wrong volume is already the damage."""
    _require_destinations(cfg)
    with _restore_gates(cfg, gates):
        return _plan_restore_inside_the_gates(
            cfg, target=Path(target), confirmed=confirmed, snapshot=snapshot,
            snapshot_volume=snapshot_volume, accept_unrecorded=accept_unrecorded,
            include_mirror=include_mirror, pull_share=pull_share, runner=runner,
            process_lister=process_lister,
        )


def _plan_restore_inside_the_gates(
    cfg: config.Config, *, target: Path, confirmed: bool, snapshot: str | None,
    snapshot_volume: str | None, accept_unrecorded: bool | None, include_mirror: bool,
    pull_share: bool, runner: Runner, process_lister: ProcessLister | None,
) -> RestorePlan:
    """The planning body, which the gate wraps as one block."""
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
    if not target.is_dir():
        raise BackupRefused(
            Refusal.RESTORE_TARGET_ABSENT,
            f"the restore target {target} does not exist; create or mount it first",
        )
    running = rekordbox_processes_running(lister=process_lister)
    if running:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
            f"{', '.join(running)} is running. Restoring underneath a live "
            f"rekordbox replaces the file it holds open, which leaves the "
            f"application and the disk describing two different libraries.",
        )

    # A STAMP, AND THIS LIBRARY'S, before it is put into a single path.
    resolved = resolve_snapshot(
        cfg, snapshot=snapshot, snapshot_volume=snapshot_volume,
        accept_unrecorded=accept_unrecorded, runner=runner,
    )
    chosen = resolved.stamp

    database_target = database_target_for(cfg, target)
    # THE SIDECARS ARE CLEARED BEFORE ANYTHING IS COPIED: SQLite would replay a
    # stale log onto the restored file. Suffixes come from the state inventory.
    clears = tuple(
        database_target.with_name(database_target.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    rclone = _rclone()
    base = f"{cfg.backup.db_dest_root}/{chosen}/db"
    commands = []
    if include_mirror:
        commands.append(
            Command(
                label=RESTORE_MIRROR,
                # THE BACKUP MIRROR'S OWN EXCLUDES: an old mirror can still hold
                # the database, which comes from the snapshot and nowhere else.
                argv=(
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(_mirror_excludes(cfg)),
                    "--transfers", "8", "--checkers", "16",
                ),
            )
        )
    into = f"{database_target.parent}/"
    commands.append(Command(
        label=RESTORE_DATABASE, argv=(rclone, "copy", f"{base}/{database_target.name}", into)
    ))
    # Only the sidecars the inventory writes back, and only those the snapshot
    # holds: a stale index beside a fresh log disagrees with it, and the
    # snapshot copies a sidecar only when present.
    held = snapshot_filenames(cfg, chosen, runner=runner)
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        if name not in held:
            absent.append(sidecar.suffix)
            continue
        commands.append(
            Command(label=RESTORE_DATABASE, argv=(rclone, "copy", f"{base}/{name}", into))
        )
    # THE SHARE COMES BACK LAST, WITH A COPY, AND ONLY FROM A LISTING, since the
    # sidecars are already cleared when a missing mirror would fail. A copy, never
    # a sync: the share beside the database may hold analysis the mirror never
    # saw. A landing
    # under the analysis watch is WITHHELD: the session around a live restore
    # refuses at its close on changed analysis files. Whose share: the
    # snapshot's marker, else this configuration's identity.
    share = ShareRestore.MIRRORED
    if _outside_share(cfg) is not None:
        landing = database_target.parent / analysis_store.SHARE_DIRNAME
        whose = resolved.recorded_volume or cfg.library.volume_id
        if not pull_share or analysis_store.is_watched(cfg, landing):
            share = ShareRestore.WITHHELD
        elif share_is_held(cfg, identity=whose, runner=runner):
            share = ShareRestore.PULLED
            commands.append(
                Command(
                    label=RESTORE_SHARE,
                    argv=(
                        rclone, "copy",
                        f"{share_destination(cfg, identity=whose)}/current",
                        str(landing),
                        "--transfers", "8", "--checkers", "16",
                    ),
                )
            )
        else:
            share = ShareRestore.ABSENT
    return RestorePlan(
        target=target, database_target=database_target, snapshot=chosen, clears=clears,
        commands=tuple(commands), absent_sidecars=tuple(absent),
        recorded_volume=resolved.recorded_volume, share=share,
    )
