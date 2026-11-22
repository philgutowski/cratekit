"""The database portion's plan: a dated snapshot behind the process gate, and the share.

Split out of :mod:`cratekit.modules.tools.backup`, which re-exports every name
here and is the module to import; this one reads the backup module's labels and
helpers, so it is loaded through it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from cratekit.core import analysis_store, backup_facts, config
from cratekit.modules.tools import backup_record
from cratekit.modules.tools.backup import (
    ANALYSIS_SHARE_ABSENT,
    IDENTITY_MARKER_PREFIX,
    KIND_SNAPSHOT,
    KIND_UNCHANGED,
    SHARE_DEST_DIRNAME,
    SHARE_UNRECORDED,
    SNAPSHOT_DATABASE,
    SNAPSHOT_IDENTITY,
    SNAPSHOT_IDENTITY_NOT_WRITTEN,
    SNAPSHOT_SETTINGS,
    SNAPSHOT_SHARE,
    VOLUME_EXCLUDES,
    AbsenceUnconfirmed,
    Command,
    PortionPlan,
    ProcessLister,
    Refusal,
    _exclude_args,
    _warning,
    database_fileset,
    identity_marker,
    rekordbox_processes_running,
    settings_directories,
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
            portion=backup_facts.Portion.DATABASE,
            refusal=Refusal.REKORDBOX_ABSENCE_UNCONFIRMED,
            detail=(
                f"{exc.cause.message}, so no snapshot of the database was taken. "
                f"Previous dated snapshots remain the backstop."
            ),
            warnings=uncovered,
        )
    if running:
        return PortionPlan(
            portion=backup_facts.Portion.DATABASE,
            refusal=Refusal.REKORDBOX_RUNNING,
            detail=(
                f"{', '.join(running)} is running, so the database may be "
                f"mid-write. A copy taken now opens cleanly and is silently "
                f"missing whatever the agent was writing, which is worse than no "
                f"copy at all. Previous dated snapshots remain the backstop."
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
    commands = [
        Command(
            label=SNAPSHOT_DATABASE,
            argv=(rclone, "copy", str(database), f"{destination}/db/", "--transfers", "4"),
        )
    ]
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
        commands.append(
            Command(label=SNAPSHOT_IDENTITY, argv=(rclone, "touch", f"{destination}/{marker}"))
        )
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
        commands.append(
            Command(
                label=SNAPSHOT_SETTINGS,
                argv=(
                    rclone, "copy", str(directory), f"{destination}/{directory.name}",
                    "--transfers", "8", "--checkers", "16",
                ),
            )
        )
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
    return (
        _warning(
            SNAPSHOT_IDENTITY_NOT_WRITTEN,
            f"this snapshot will not say which library it was taken from, "
            f"because {config.VOLUME_IDENTITY_KEY} is {why}. A restore will "
            f"pull it only when its stamp is named",
        ),
    )


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
    return (
        _warning(
            ANALYSIS_SHARE_ABSENT,
            f"the analysis share {share} sits outside the library root "
            f"{cfg.library.root} and is not a directory, so this backup "
            f"carries no beat grids or analysis. That is expected only for a "
            f"library rekordbox has not analysed yet",
        ),
    )
