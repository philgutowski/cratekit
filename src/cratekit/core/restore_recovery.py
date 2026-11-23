"""Bare-metal recovery onto a replacement drive: its target checks and its session.

Part of :mod:`cratekit.core.restore`, which re-exports every name here; read them there. A
name of restore outside this file, every seam a test patches, and ``os`` and ``shutil``,
which a test patches on restore to sample the disk, are read through ``restore`` at call
time so a patch on restore bites here too (U300).
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Iterator, Sequence

from cratekit.core import (
    config,
    preflight,
    session,
)
from cratekit.core.cause import CratekitError, Scope, refuse

if TYPE_CHECKING:
    from cratekit.core.restore import Held


#: The restore logger, so a record reads as it did before the split.
logger = logging.getLogger("cratekit.core.restore")


def _restore():
    """``restore`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import restore

    return restore


#: The mount verdicts that mean the configured library is NOT THERE, as opposed
#: to present or unknown.
_VOLUME_IS_GONE: frozenset[preflight.MountState] = frozenset(
    {
        preflight.MountState.NOT_MOUNTED,
        preflight.MountState.LIBRARY_PATH_MISSING,
        preflight.MountState.FOREIGN_VOLUME,
    }
)


def recovery_lock_path() -> Path:
    """The installation-scoped lock a bare-metal recovery takes.

    Needs no configuration, since every KTD21 gate lives beside the lost library.
    """
    return config.state_path(_restore().RECOVERY_LOCK_KEY)


def _refuse_target(message: str, steps: Sequence[str], **detail: object) -> CratekitError:
    return refuse(
        "recovery-target-refused",
        message,
        steps=tuple(steps),
        scope=Scope.RUN,
        origin=("restore",),
        detail=dict(detail),
    )


def assert_library_volume_is_gone(
    cfg: config.Config,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> preflight.MountState:
    """Refuse unless the library this installation names is genuinely unreachable.

    Keeps the cases apart: a present library must use the three real gates, so
    the weaker substitutes are reachable only when it is gone. Absent is gone,
    mounted elsewhere is alive, and an unreported identity is not "gone".
    """
    try:
        preflight.assert_library_volume(
            cfg.library.root,
            cfg.library.volume_id,
            destructive=True,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
    except preflight.LibraryVolumeError as exc:
        if exc.status.state in _VOLUME_IS_GONE:
            return exc.status.state
        raise _refuse_target(
            f"the library volume is not absent, it is {exc.status.state.value}; a "
            f"bare-metal recovery substitutes weaker gates for the library-scoped "
            f"ones and is refused whenever the real ones could be read",
            steps=(
                "mount the library where this installation expects it and use the "
                "ordinary restore, which passes all three gates",
            ),
            state=str(exc.status.state),
            configured_root=str(cfg.library.root),
        ) from exc
    raise _refuse_target(
        f"the library at {cfg.library.root} is mounted and is the volume this "
        f"installation was set up against, so there is nothing to recover from "
        f"bare metal",
        steps=("use the ordinary restore, which passes all three gates",),
        configured_root=str(cfg.library.root),
    )


#: Answers "is this directory the root of its own filesystem". A seam, since the
#: real answer needs a mounted volume. A probe that always answers yes disables
#: the boot-disk check; nothing in ``src/`` passes one, and
#: ``test_round2_the_real_mount_probe_is_armed_by_default`` keeps the default real.
MountProbe = Callable[[Path], bool]


def _is_mount_point(path: Path) -> bool:
    """Whether a directory is the root of its own filesystem.

    Asked of the filesystem identifier, since an unmounted volume leaves an empty
    folder on the internal disk at the same path.
    """
    try:
        return path.stat().st_dev != path.parent.stat().st_dev
    except OSError:
        return False


def recovered_database_fileset(cfg: config.Config, target: Path) -> tuple[Path, ...]:
    """Where a recovery onto ``target`` lands the database, then each companion.

    Repeats ``backup.database_target_for``'s re-basing, since this layer does not
    import the backup module;
    ``test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`` holds them
    together.
    """
    database = config.state_path("rekordbox_db", cfg)
    try:
        landing = target / database.relative_to(cfg.library.root)
    except ValueError:
        landing = target / database.name
    companions = tuple(
        landing.with_name(landing.name + sidecar.suffix)
        for sidecar in config.state_file("rekordbox_db").sidecars
    )
    return (landing, *companions)


def assert_recovery_target(
    cfg: config.Config,
    target: Path | str,
    *,
    replacing_existing: bool = False,
    mount_probe: MountProbe | None = None,
) -> Path:
    """Refuse a bare-metal target that is not one. Reads only; creates nothing.

    The stub check covers a target at or inside the configured root and one beside
    it (a suffixed mount name), each answered by the filesystem identifier.
    """
    where = Path(target)
    if not where.is_dir():
        raise _refuse_target(
            f"the recovery target {where} is not a directory that exists",
            steps=("mount or create the volume to recover onto, then run this again",),
            target=str(where),
        )
    probe = mount_probe or _restore()._is_mount_point
    configured = Path(cfg.library.root).resolve()
    resolved = where.resolve()
    inside_configured = resolved == configured or configured in resolved.parents
    beside_configured = resolved.parent == configured.parent
    if (inside_configured or beside_configured) and not probe(where):
        raise _refuse_target(
            (
                f"{where} is at or inside the path this installation's library was "
                f"mounted at"
                if inside_configured
                else f"{where} sits in the directory this installation's library "
                f"mounts into, under a name one this system chose"
            )
            + ", and is not a mount point now, so it is the empty folder an "
            "unmounted volume leaves behind; recovering into it would write the "
            "library onto the internal disk, where the volume will hide it the "
            "moment it is plugged back in",
            steps=(
                "mount the replacement volume at this path first, or name a "
                "different target",
            ),
            target=str(where),
            configured_root=str(configured),
        )
    # Only where THIS library's database lands, since the mirror deletes nothing
    # and reruns must pass (R-592).
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
    if existing and not replacing_existing:
        raise _refuse_target(
            f"{where} already holds {existing[0].name}; a recovery that replaced "
            f"it would destroy a library nobody named for replacement",
            steps=("name this target for replacement explicitly, or choose another",),
            target=str(where),
            holds=[str(entry) for entry in existing[:20]],
        )
    return where


@contextmanager
def bare_metal_session(
    cfg: config.Config,
    *,
    target: Path | str,
    acknowledged: bool,
    replacing_existing: bool = False,
    terminal: Callable[[], bool] | None = None,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
    mount_probe: MountProbe | None = None,
) -> Iterator[Held]:
    """Hold the substitute gates for the case where the library volume is gone.

    Every KTD21 gate is library-scoped and died with the volume (R-8), so each is
    substituted:

    * VOLUME: the configured library is unreachable and the target is a real
      mount, not an unmounted volume's stub;
    * ACKNOWLEDGMENT: an explicit decision at a controlling terminal, by an actor
      derived from the process; WEAKER than R34's record, which is on the dead volume;
    * LOCK: installation-scoped, since no shared volume is left to contend over.

    The read-only assertions run before the lock, so a refusal changes nothing.
    :func:`plan` and :func:`run` derive every path from this session through
    :func:`_rooted` (:data:`RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH`). The caller is
    the recovery verb in ``cratekit.session.restore_cli``, which spends it on the
    off-machine restore. A target already holding a library holds a lock this does
    not take, and needs ``replacing_existing``.
    """
    assert_library_volume_is_gone(
        cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
    )
    where = assert_recovery_target(
        cfg, target, replacing_existing=replacing_existing, mount_probe=mount_probe
    )
    probe = terminal or session.has_controlling_terminal
    if not probe():
        raise _refuse_target(
            "this invocation has no controlling terminal, so there is nobody here "
            "to accept a recovery that replaces a library; the acknowledgment this "
            "substitutes for is a person's act and its record is on the volume "
            "that died",
            steps=("run the recovery from a terminal a person is sitting at",),
            target=str(where),
        )
    if not acknowledged:
        raise _refuse_target(
            "a bare-metal recovery writes a whole library onto the target and is "
            "not performed without an explicit decision naming that target",
            steps=("name the target and accept the replacement explicitly",),
            target=str(where),
        )
    actor = session.derive_actor()
    logger.warning(
        "bare-metal recovery accepted by %s onto %s, with library-scoped gates "
        "unreachable",
        actor,
        where,
    )
    with session.session_lock(path=recovery_lock_path()) as lock:
        # THE TARGET RIDES ON THE VALUE, so the paths come from what was validated.
        with _restore()._issued(
            workflow=_restore().BARE_METAL_WORKFLOW,
            lock=lock,
            issued_by=_restore().Guard.BARE_METAL,
            authorises=where,
        ) as held:
            yield held
