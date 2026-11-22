"""The move to the system Trash, and the proof that one is available first.

R18 permits three things to happen to a music file: a tag write, a content
preserving rename, and R35's move to the Trash. There is no unlink, so when the
file's volume has no Trash this REFUSES rather than falling back to a delete.

**THE TRASH IS ON THE FILE'S OWN VOLUME** because a move within a filesystem is
an atomic, reversible rename, while across filesystems it is a copy and an
unlink. The device check makes that structural: a Trash that looks right on
another mount is caught before a byte moves.

**THE DESTINATION NAME IS RESERVED BEFORE THE RENAME**, since POSIX ``rename``
silently replaces a destination: two same named tracks trashed a week apart
would lose the first. A free name is claimed with an exclusive create, and the
rename replaces only that placeholder.

``Stat`` here and in ``candidates`` is each module's own stat seam; they read a
device number here and an inode there.

Layer note: MODULES. Platform differences arrive as parameters, so both branches
run in a test on one machine.
"""

from __future__ import annotations

import errno
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from cratekit.core import config
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy

#: Name collisions worked through before giving up; a thousand files of one name
#: is something upstream looping.
MAX_NAME_ATTEMPTS = 1000

#: The errno values that mean "this NAME is unacceptable" (one file) rather than
#: "this VOLUME is unusable" (the run). ``EILSEQ`` is looked up, since not every
#: platform defines it.
_NAME_REFUSED_BY_FILESYSTEM: frozenset[int] = frozenset(
    value
    for value in (errno.ENAMETOOLONG, errno.EINVAL, getattr(errno, "EILSEQ", None))
    if value is not None
)

#: The macOS and XDG Trash directory names.
_MACOS_HOME_TRASH = ".Trash"
_MACOS_VOLUME_TRASH = ".Trashes"
_XDG_HOME_TRASH = "Trash"
_XDG_VOLUME_TRASH_PREFIX = ".Trash-"
_XDG_FILES = "files"
_XDG_INFO = "info"

#: The XDG basedir data root and its fallback, read directly: the Trash belongs to
#: the desktop, not to this application's data directory.
_XDG_DATA_HOME = "XDG_DATA_HOME"
_XDG_DATA_FALLBACK = (".local", "share")


@dataclass(frozen=True, slots=True)
class TrashLayout:
    """Where a trashed file goes on this platform, and what has to go beside it.

    ``info`` is the XDG metadata directory, None on macOS. **THE INFO FILE IS NOT
    WRITTEN**: its ``Path`` is percent encoded, and a second encoder outside
    ``core.locations`` is forbidden (two encoders once deleted 144 files). A file
    with no info file is restorable by :func:`recover` and by hand; one with a
    wrong info file would be restored to the wrong place. The directory is still
    made, for the desktop's expected shape.
    """

    root: Path
    files: Path
    info: Path | None = None


@dataclass(frozen=True, slots=True)
class TrashStatus:
    """Whether this volume has a Trash this account can actually move a file into.

    ``problem`` is empty exactly when ``usable`` is true; it is the sentence
    doctor prints.
    """

    layout: TrashLayout | None
    usable: bool
    problem: str = ""
    #: True when the ONLY fault is a directory not created yet. Doctor probes with
    #: ``create=False``, and without this read a volume deletion would serve as a
    #: failure. Typed, so nobody branches on the sentence.
    absent: bool = False


def volume_root(path: Path | str) -> Path:
    """The mount point the given path sits on, walked up by device number (R1).

    No list of mount names, so nested mounts and other platforms work. Starts at
    the nearest existing ancestor, so a file about to be created is answered too.
    """
    current = Path(path)
    while not current.exists() and current != current.parent:
        current = current.parent
    device = current.stat().st_dev
    while current != current.parent:
        parent = current.parent
        try:
            if parent.stat().st_dev != device:
                return current
        except OSError:  # pragma: no cover - an ancestor this account cannot stat
            return current
        current = parent
    return current


def _xdg_data_home(home: Path) -> Path:
    return Path(os.environ.get(_XDG_DATA_HOME) or home.joinpath(*_XDG_DATA_FALLBACK))


def layout_for(
    path: Path | str,
    *,
    home: Path | None = None,
    uid: int | None = None,
    platform: str = sys.platform,
) -> TrashLayout:
    """Where a file at ``path`` belongs when it is trashed, on this platform.

    On the home volume the desktop's own Trash, which the user knows how to
    open; elsewhere the volume's, since the home one would mean a cross device
    copy. ``home``, ``uid`` and ``platform`` are parameters so every branch runs
    on one machine.
    """
    resolved_home = Path(home) if home is not None else Path.home()
    resolved_uid = uid if uid is not None else (os.getuid() if hasattr(os, "getuid") else 0)
    on_home_volume = volume_root(path) == volume_root(resolved_home)

    if platform == "darwin":
        if on_home_volume:
            root = resolved_home / _MACOS_HOME_TRASH
        else:
            root = volume_root(path) / _MACOS_VOLUME_TRASH / str(resolved_uid)
        return TrashLayout(root=root, files=root)

    if on_home_volume:
        root = _xdg_data_home(resolved_home) / _XDG_HOME_TRASH
    else:
        root = volume_root(path) / f"{_XDG_VOLUME_TRASH_PREFIX}{resolved_uid}"
    return TrashLayout(root=root, files=root / _XDG_FILES, info=root / _XDG_INFO)


#: The stat a device number is read through, so the Trash on ANOTHER filesystem
#: is reachable without mounting a second disk.
Stat = Callable[[str], object]


def probe(
    path: Path | str,
    *,
    home: Path | None = None,
    uid: int | None = None,
    platform: str = sys.platform,
    create: bool = True,
    stat: Stat = os.stat,
) -> TrashStatus:
    """Answer whether a file at ``path`` could be trashed, WITHOUT trashing it.

    Reports rather than raises, for doctor; the pass calls :func:`assert_usable`.
    ``create`` makes a missing per volume Trash as the desktop would on first
    use; doctor turns it off so its check cannot pass by having run.
    """
    layout = layout_for(path, home=home, uid=uid, platform=platform)
    target = layout.files
    if create and not target.is_dir():
        try:
            config.mkdir_private(target)
            if layout.info is not None:
                config.mkdir_private(layout.info)
        except OSError as exc:
            return TrashStatus(layout, False, f"{layout.root} could not be created: {exc}")
    if not target.is_dir():
        return TrashStatus(
            layout, False, f"{target} is not a directory", absent=not target.exists()
        )
    if not os.access(target, os.W_OK | os.X_OK):
        return TrashStatus(layout, False, f"{target} is not writable by this account")
    try:
        same_device = stat(str(target)).st_dev == stat(str(volume_root(path))).st_dev
    except OSError as exc:  # pragma: no cover - the directory vanished mid-probe
        return TrashStatus(layout, False, f"{target} could not be inspected: {exc}")
    if not same_device:
        return TrashStatus(
            layout,
            False,
            f"{target} is on a different filesystem from {path}, so moving a "
            f"file there would be a copy and a delete rather than a move",
        )
    return TrashStatus(layout, True)


def _unavailable(message: str, scope: Scope, **detail: str) -> CratekitError:
    return refuse(
        "trash-unavailable",
        message,
        remedy=Remedy.RUN_DOCTOR,
        scope=scope,
        origin=("deletion.trash",),
        detail=detail,
    )


def assert_usable(
    path: Path | str,
    *,
    home: Path | None = None,
    uid: int | None = None,
    platform: str = sys.platform,
    stat: Stat = os.stat,
) -> TrashLayout:
    """Return the layout, or refuse. Called immediately before every move."""
    status = probe(path, home=home, uid=uid, platform=platform, stat=stat)
    if not status.usable or status.layout is None:
        raise _unavailable(
            f"the volume holding {path} has no usable Trash: {status.problem}. Deletion refuses "
            "rather than unlinking the file, because the move to the Trash is the only "
            "destructive act this product performs on a music file and an unlink has no undo",
            Scope.RUN,
            path=str(path),
            problem=status.problem,
        )
    return status.layout


def _is_a_directory(directory: Path) -> bool:
    """Whether the destination is still a directory this account can look at."""
    try:
        return directory.is_dir()
    except OSError:  # pragma: no cover - a path the account cannot even stat
        return False


def _free_name(directory: Path, name: str) -> Path:
    """Claim an unused name in ``directory`` with an exclusive create, and return it.

    No test then act window, through which one trashed file would replace
    another. A name the filesystem will not take (a numbered name past the
    length limit) refuses at ``Scope.ITEM``, as running out of numbers does,
    since the next file's name differs.
    """
    stem, dot, suffix = name.rpartition(".")
    for attempt in range(1, MAX_NAME_ATTEMPTS + 1):
        if attempt == 1:
            candidate = directory / name
        elif dot and stem:
            # ``stem`` is empty for a name such as ``.flac``, numbered whole below.
            candidate = directory / f"{stem} {attempt}{dot}{suffix}"
        else:
            candidate = directory / f"{name} {attempt}"
        try:
            handle = os.open(
                candidate, os.O_CREAT | os.O_EXCL | os.O_WRONLY, config.PRIVATE_FILE_MODE
            )
        except FileExistsError:
            continue
        except OSError as exc:
            if exc.errno not in _NAME_REFUSED_BY_FILESYSTEM or not _is_a_directory(directory):
                # A fact about the volume, which the next file meets too, so it
                # goes up as it came and the run stops. The directory is checked
                # before the errno is believed: the same values can be about an
                # over long Trash path, which would blame every track in turn.
                raise
            raise _unavailable(
                f"the Trash at {directory} cannot hold a file named {candidate.name!r} ({exc}), so "
                "this one file has nowhere to land; nothing was moved for it",
                Scope.ITEM,
                directory=str(directory),
                name=candidate.name,
            ) from exc
        os.close(handle)
        return candidate
    raise _unavailable(
        f"the Trash at {directory} already holds {MAX_NAME_ATTEMPTS} files named "
        f"like {name!r}, so this move has nowhere to land",
        Scope.ITEM,
        directory=str(directory),
        name=name,
    )


def move_to_trash(path: Path | str, *, layout: TrashLayout) -> Path:
    """Move one file into the Trash with a RENAME and return where it landed.

    The device was proved equal by :func:`assert_usable`, and a wrong proof makes
    the rename fail loudly. The placeholder is removed on any failure, since an
    empty file with a track's name looks like the track.
    """
    source = Path(path)
    target = _free_name(layout.files, source.name)
    try:
        os.replace(source, target)
    except BaseException:
        # The placeholder is ours: created with O_EXCL, and nothing since writes
        # this name.
        try:
            target.unlink()
        except OSError:  # pragma: no cover - the placeholder was already gone
            pass
        raise
    return target


def recover(target: Path | str, original: Path | str) -> Path:
    """Put a trashed file back, refusing to overwrite. The undo, run by the suite."""
    destination = Path(original)
    if destination.exists():
        raise _unavailable(
            f"{destination} is occupied again, so restoring the trashed copy "
            f"would overwrite whatever is there now",
            Scope.ITEM,
            original=str(destination),
            trashed=str(target),
        )
    os.replace(Path(target), destination)
    return destination


#: The probe signature doctor consumes (U27 owns the check).
Probe = Callable[..., TrashStatus]


__all__ = [
    "MAX_NAME_ATTEMPTS",
    "Probe",
    "Stat",
    "TrashLayout",
    "TrashStatus",
    "assert_usable",
    "layout_for",
    "move_to_trash",
    "probe",
    "recover",
    "volume_root",
]
