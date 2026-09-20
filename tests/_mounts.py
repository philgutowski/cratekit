"""Stand directories in as mount points, so a test can hold two volumes on one disk.

Every temporary directory a test makes sits on one filesystem, so the real
``preflight.containing_mount`` climbs from any of them to the same mount point
and an identity provider keyed by mount cannot tell two "volumes" apart. The
volume assertion is only interesting when it can. This replaces the climb, and
nothing else: the identity comparison, the state machine and the refusals that
read it are all the real ones.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Mapping

from cratekit.core import preflight

Identity = str | None | Callable[[], str | None]


def stand_in(
    monkeypatch,
    mounted: Mapping[Path, Identity],
    *,
    otherwise: str | None,
    enumerated: tuple[Path, ...] | None = None,
    slots_under: Path | None = None,
) -> None:
    """Treat each key of ``mounted`` as a mount point holding the volume it names.

    ``otherwise`` is the identity of every path under none of them, which is the
    disk the library root sits on in these tests. An identity may be a callable,
    asked on every read, which is how a test swaps the disk under a mount path
    between one assertion and the next. ``enumerated`` is what the mount table
    lists, and defaults to the stand-ins themselves.

    ``slots_under`` declares a directory as the place this pretend platform
    mounts volumes, one level down, which is what ``/Volumes`` is on macOS. With
    it set, a directory standing there that is NOT one of the stand-ins is an
    empty mount slot, the thing an unclean eject leaves behind, and
    ``preflight.identity_source`` refuses to read an identity through it exactly
    as it does on a real machine. Without it no path crosses a slot.
    """
    # The REAL climb, even on a second call. A test that ejects a volume calls
    # this again without it, and reading the module attribute then would capture
    # the first stand-in, which still believes the volume is mounted.
    real_climb = getattr(preflight.containing_mount, "real_climb", preflight.containing_mount)
    held = {Path(mount).resolve(): identity for mount, identity in mounted.items()}

    def containing_mount(path: Path) -> Path:
        deepest = preflight.deepest_existing(Path(path))
        # Deepest first, because a volume mounted inside another is the one a
        # path under it is on, and the real climb stops at the first mount too.
        for mount in sorted(held, key=lambda mount: len(mount.parts), reverse=True):
            if deepest == mount or mount in deepest.parents:
                return mount
        return real_climb(Path(path))

    def identity_of(path: Path) -> str | None:
        key = Path(path).resolve()
        if key not in held:
            return otherwise
        identity = held[key]
        return identity() if callable(identity) else identity

    real_is_mount = getattr(preflight.is_mount_point, "real_is_mount", preflight.is_mount_point)

    def is_mount_point(path: Path) -> bool:
        return Path(path).resolve() in held or real_is_mount(Path(path))

    is_mount_point.real_is_mount = real_is_mount  # type: ignore[attr-defined]
    declared = () if slots_under is None else ((Path(slots_under).resolve(), 1),)
    containing_mount.real_climb = real_climb  # type: ignore[attr-defined]
    monkeypatch.setattr(preflight, "is_mount_point", is_mount_point)
    monkeypatch.setattr(preflight, "volume_mount_locations", lambda: declared)
    listed = tuple(held) if enumerated is None else tuple(enumerated)
    monkeypatch.setattr(preflight, "containing_mount", containing_mount)
    monkeypatch.setattr(preflight, "default_identity_provider", lambda: identity_of)
    monkeypatch.setattr(preflight, "local_mount_points", lambda: listed)
