"""Stand directories in as mount points, so a test can hold two volumes on one disk.

Only ``preflight.containing_mount``'s climb is replaced; the identity
comparison, state machine and refusals are the real ones.
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

    ``otherwise`` is the identity of every other path, the library root's disk.
    An identity may be a callable, asked on every read, to swap the disk between
    assertions. ``enumerated`` is what the mount table lists, by default the
    stand-ins. ``slots_under`` declares this pretend platform's ``/Volumes``: a
    directory there that is no stand-in is an empty mount slot, which
    ``preflight.identity_source`` refuses to read through, as on a real machine.
    """
    # The REAL climb, captured once: a test that ejects a volume calls this again,
    # and the module attribute would then be the first stand-in.
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
