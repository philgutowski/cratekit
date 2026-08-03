"""The move to the system Trash, and the proof that one is available first.

R18 permits exactly three things to happen to a music file: a metadata tag write,
a content-preserving rename, and the move to the system Trash performed by R35.
There is no fourth, and in particular there is no unlink. So this module has one
job and one refusal: it moves a file into the Trash for the volume the file is
on, and when there is no such Trash it REFUSES rather than falling back to a
delete. A fallback would be the product doing the single thing it promised never
to do, at the one moment nobody could check the result afterwards.

**WHY THE TRASH HAS TO BE ON THE FILE'S OWN VOLUME, in mechanics rather than in
principle.** A move within a filesystem is a rename: the bytes never move, the
operation is atomic, and it is reversible by renaming back. A move ACROSS
filesystems is a copy followed by an unlink, which is not atomic, takes as long
as the file is big, and ends with the original genuinely deleted. Every desktop
platform solves this the same way, with a Trash per volume, and this follows the
platform rather than inventing anything. The device check below is what makes
that structural rather than hopeful: it compares device numbers, so a Trash
directory that LOOKS right and sits on another mount is caught before a byte
moves.

**WHY THE DESTINATION NAME IS RESERVED BEFORE THE RENAME.** POSIX ``rename``
silently REPLACES an existing destination. Two tracks with the same file name
removed a week apart, and the second one trashed over the first, is data loss
performed by the recovery mechanism. So a free name is claimed with an exclusive
create first, which fails if anything is already there, and the rename then
replaces the placeholder this process just made and nothing else.

ONE NAMING DECISION, RECORDED. ``Stat`` is declared here and in ``candidates``,
and they are one idea specialised per module rather than two ideas sharing a
name: each is "the stat seam THIS module reads through", and they differ only in
what they read off the result, an inode there and a device number here. Both
exist for the same reason, which is that the branch each one guards is otherwise
unreachable without a second disk or a broken filesystem.

Layer note: MODULES. It names no verb, and its platform differences arrive as
parameters so both branches are reachable in a test on one machine, which is the
same seam ``core.locations`` uses for the Windows path separator.
"""

from __future__ import annotations

import errno
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from cratekit.core import config
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy

#: How many name collisions to work through before giving up. A Trash holding a
#: thousand files of one name is not a case worth serving; it is a signal that
#: something upstream is looping, and refusing says so while continuing to search
#: would spend an unbounded amount of time saying nothing.
MAX_NAME_ATTEMPTS = 1000

#: The errno values that mean "this NAME is unacceptable" rather than "this
#: VOLUME is unusable". Listed rather than collapsed into a bare ``except
#: OSError`` because the two need opposite blast radii: a name the filesystem
#: will not take costs one file, and a disk that is full or read only costs the
#: run. ``EILSEQ`` is looked up rather than named, since not every platform
#: defines it and a missing attribute here would be an import-time crash.
_NAME_REFUSED_BY_FILESYSTEM: frozenset[int] = frozenset(
    value
    for value in (
        errno.ENAMETOOLONG,
        errno.EINVAL,
        getattr(errno, "EILSEQ", None),
    )
    if value is not None
)

#: The macOS per-volume Trash directory, and the XDG one. Named rather than
#: written inline so the two platform branches read as one decision with two
#: answers rather than as scattered literals.
_MACOS_HOME_TRASH = ".Trash"
_MACOS_VOLUME_TRASH = ".Trashes"
_XDG_HOME_TRASH = "Trash"
_XDG_VOLUME_TRASH_PREFIX = ".Trash-"
_XDG_FILES = "files"
_XDG_INFO = "info"

#: The environment variable the XDG basedir specification uses for the data root,
#: and the relative fallback when it is unset. Read directly rather than through
#: platformdirs, because platformdirs answers "where does THIS APPLICATION keep
#: its data" and the Trash belongs to the desktop rather than to us.
_XDG_DATA_HOME = "XDG_DATA_HOME"
_XDG_DATA_FALLBACK = (".local", "share")


@dataclass(frozen=True, slots=True)
class TrashLayout:
    """Where a trashed file goes on this platform, and what has to go beside it.

    ``info`` is the XDG specification's metadata directory, which is where a
    Linux desktop keeps the record of where each trashed file came from. macOS
    keeps that association in the volume's own index and has no such directory,
    so ``info`` is None there. Modelling it as an optional field rather than as
    two functions keeps one caller for both platforms.

    **THE INFO FILE IS NOT WRITTEN, and that is a decision rather than an
    omission.** The specification says its ``Path`` value is percent-encoded like
    a URI, and this repository forbids a second percent-encoder anywhere outside
    ``core.locations``, by a guard, because the last time two encoders existed in
    one tree they disagreed about accented filenames and 144 files were deleted.
    A trashed file with no info file is visible in the trash directory and is
    restorable by :func:`recover` and by hand; a trashed file with a wrong info
    file can be restored by the desktop to the wrong place. The directory is
    still created so a real implementation, written when there is a Linux user to
    write it for, drops into the shape the desktop already expects.
    """

    root: Path
    files: Path
    info: Path | None = None


@dataclass(frozen=True, slots=True)
class TrashStatus:
    """Whether this volume has a Trash this account can actually move a file into.

    ``problem`` is empty exactly when ``usable`` is true. It is a sentence rather
    than a token because the reader is doctor, which is going to print it, and
    because each way this fails needs a different act from the user: create the
    directory, fix its permissions, or work out why the mount is not the mount
    they think it is.
    """

    layout: TrashLayout | None
    usable: bool
    problem: str = ""


def volume_root(path: Path | str) -> Path:
    """The mount point the given path sits on, found by device number.

    WALKED RATHER THAN NAMED. Every platform spells its mount root differently
    and several spell it more than one way, so a function that knew the names
    would be a function that is wrong on the next platform and, worse, wrong on a
    nested mount on this one. Walking up while the device number stays the same
    finds the real boundary on any platform with no list to maintain (R1).

    The walk starts at the nearest existing ancestor, so this answers for a file
    that is about to be created as readily as for one that is there.
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
    override = os.environ.get(_XDG_DATA_HOME)
    if override:
        return Path(override)
    return home.joinpath(*_XDG_DATA_FALLBACK)


def layout_for(
    path: Path | str,
    *,
    home: Path | None = None,
    uid: int | None = None,
    platform: str = sys.platform,
) -> TrashLayout:
    """Where a file at ``path`` belongs when it is trashed, on this platform.

    The home volume and every other volume are different answers, which is not an
    optimization: on the home volume the desktop's own Trash is the one the user
    already knows how to open, and a per-volume directory beside it would be a
    second trash only this product knows about. On any other volume there is no
    home trash to use, because using it would make the move a cross-device copy.

    ``home``, ``uid`` and ``platform`` are parameters so that both branches are
    reachable from one machine. A platform branch that can only run on the
    platform it is for is a branch that ships untested.
    """
    resolved_home = Path(home) if home is not None else Path.home()
    resolved_uid = uid if uid is not None else (os.getuid() if hasattr(os, "getuid") else 0)
    on_home_volume = volume_root(path) == volume_root(resolved_home)

    if platform == "darwin":
        if on_home_volume:
            root = resolved_home / _MACOS_HOME_TRASH
            return TrashLayout(root=root, files=root)
        root = volume_root(path) / _MACOS_VOLUME_TRASH / str(resolved_uid)
        return TrashLayout(root=root, files=root)

    if on_home_volume:
        root = _xdg_data_home(resolved_home) / _XDG_HOME_TRASH
    else:
        root = volume_root(path) / f"{_XDG_VOLUME_TRASH_PREFIX}{resolved_uid}"
    return TrashLayout(root=root, files=root / _XDG_FILES, info=root / _XDG_INFO)


#: The stat this module reads a device number through. A seam for the same reason
#: the platform is one: the branch that matters most here is the one where the
#: Trash turns out to be on ANOTHER filesystem, and a test cannot mount a second
#: disk to reach it.
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

    This is what doctor calls, which is why it reports rather than raises: a
    health check names every problem it found, and an exception names one. The
    deletion pass calls :func:`assert_usable`, which is this plus a refusal.

    ``create`` is on by default because the per-volume Trash is created on first
    use by the desktop too, so a volume nobody has ever trashed anything on
    legitimately has no directory yet and that is not a fault. It is a parameter
    so doctor can ask the question without making the directory it is asking
    about exist, which would make the check pass by having run.
    """
    layout = layout_for(path, home=home, uid=uid, platform=platform)
    target = layout.files
    if create and not target.is_dir():
        try:
            config._mkdir_private(target)
            if layout.info is not None:
                config._mkdir_private(layout.info)
        except OSError as exc:
            return TrashStatus(layout, False, f"{layout.root} could not be created: {exc}")
    if not target.is_dir():
        return TrashStatus(layout, False, f"{target} is not a directory")
    if not os.access(target, os.W_OK | os.X_OK):
        return TrashStatus(layout, False, f"{target} is not writable by this account")
    try:
        same_device = (
            stat(str(target)).st_dev == stat(str(volume_root(path))).st_dev
        )
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
        raise refuse(
            "trash-unavailable",
            f"the volume holding {path} has no usable Trash: {status.problem}. "
            f"Deletion refuses rather than unlinking the file, because the move "
            f"to the Trash is the only destructive act this product performs on "
            f"a music file and an unlink has no undo",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("deletion.trash",),
            detail={"path": str(path), "problem": status.problem},
        )
    return status.layout


def _is_a_directory(directory: Path) -> bool:
    """Whether the destination is still a directory this account can look at.

    Asked only when a create has already failed, to decide whether the failure
    was about the NAME or about the place it was going. It swallows the error
    because the answer it owes is a boolean and the caller is already holding the
    exception that matters.
    """
    try:
        return directory.is_dir()
    except OSError:  # pragma: no cover - a path the account cannot even stat
        return False


def _free_name(directory: Path, name: str) -> Path:
    """Claim an unused name in ``directory``, atomically, and return it.

    The claim is an exclusive create rather than a "does it exist" test followed
    by a rename. The test-then-act version has a window in it, and what falls
    through that window is one trashed file silently replacing another, which is
    the deletion mechanism destroying the copy it exists to preserve.

    A NAME THE FILESYSTEM WILL NOT ACCEPT IS A FACT ABOUT THAT NAME. Numbering a
    collision makes the name longer, so a file already at the length limit has no
    numbered alternative, and the exclusive create comes back with a length error
    rather than a collision. That refuses at ``Scope.ITEM``, like running out of
    numbers does, because the next file's name is a different length and the
    caller is entitled to keep going.
    """
    stem, dot, suffix = name.rpartition(".")
    for attempt in range(1, MAX_NAME_ATTEMPTS + 1):
        if attempt == 1:
            candidate = directory / name
        elif dot and stem:
            # ``stem`` is empty for a dotfile-shaped name such as ``.flac``,
            # where the whole name is the suffix. Numbering it through the
            # extension branch produces " 2.flac", with a leading space and the
            # original name nowhere in it.
            candidate = directory / f"{stem} {attempt}{dot}{suffix}"
        else:
            candidate = directory / f"{name} {attempt}"
        try:
            handle = os.open(candidate, os.O_CREAT | os.O_EXCL | os.O_WRONLY, config.PRIVATE_FILE_MODE)
        except FileExistsError:
            continue
        except OSError as exc:
            if exc.errno not in _NAME_REFUSED_BY_FILESYSTEM or not _is_a_directory(directory):
                # Out of space, read only, no permission: every one of those is
                # about the volume and the next file will meet it too, so it goes
                # up as it came and the caller stops the run.
                #
                # THE DIRECTORY IS CHECKED BEFORE THE ERRNO IS BELIEVED, because
                # the same two errno values can be facts about the DESTINATION
                # rather than about the name: an over-long Trash path, or a
                # directory the filesystem will not accept a create in at all.
                # Attributing that to the name would report one item scoped skip
                # per confirmed file, hundreds of them, each blaming a track,
                # while the one true sentence about the Trash is never said.
                raise
            raise refuse(
                "trash-unavailable",
                f"the Trash at {directory} cannot hold a file named "
                f"{candidate.name!r} ({exc}), so this one file has nowhere to "
                f"land; nothing was moved for it",
                remedy=Remedy.RUN_DOCTOR,
                scope=Scope.ITEM,
                origin=("deletion.trash",),
                detail={"directory": str(directory), "name": candidate.name},
            ) from exc
        os.close(handle)
        return candidate
    raise refuse(
        "trash-unavailable",
        f"the Trash at {directory} already holds {MAX_NAME_ATTEMPTS} files named "
        f"like {name!r}, so this move has nowhere to land",
        remedy=Remedy.RUN_DOCTOR,
        scope=Scope.ITEM,
        origin=("deletion.trash",),
        detail={"directory": str(directory), "name": name},
    )


def move_to_trash(
    path: Path | str,
    *,
    layout: TrashLayout,
) -> Path:
    """Move one file into the Trash and return where it landed.

    A RENAME, never a copy. The device was proved equal by :func:`assert_usable`
    before this was called, and the rename would fail loudly rather than silently
    copying if that proof were wrong, which is the property that makes the check
    a check rather than a comment.

    The placeholder is removed on any failure. Leaving one behind would put an
    empty file with a real track's name in the user's Trash, which is worse than
    the failure itself: it looks exactly like the file that was supposed to be
    there.
    """
    source = Path(path)
    target = _free_name(layout.files, source.name)
    try:
        os.replace(source, target)
    except BaseException:
        # The placeholder is ours and nothing else can have replaced it, because
        # it was created with O_EXCL and nothing between then and here writes to
        # this directory under this name.
        try:
            target.unlink()
        except OSError:  # pragma: no cover - the placeholder was already gone
            pass
        raise
    return target


def recover(target: Path | str, original: Path | str) -> Path:
    """Put a trashed file back. The undo, exercised by the suite rather than promised.

    It exists because "the file is recoverable" is the whole justification for
    trashing rather than deleting, and a claim nothing runs is a claim nobody has
    checked. It refuses to overwrite, for the reason every other write here does.
    """
    destination = Path(original)
    if destination.exists():
        raise refuse(
            "trash-unavailable",
            f"{destination} is occupied again, so restoring the trashed copy "
            f"would overwrite whatever is there now",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.ITEM,
            origin=("deletion.trash",),
            detail={"original": str(destination), "trashed": str(target)},
        )
    os.replace(Path(target), destination)
    return destination


#: The probe signature doctor consumes, named so the check and this module cannot
#: drift into two shapes for one question (U27 owns the check itself).
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
