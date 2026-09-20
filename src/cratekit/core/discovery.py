"""Which audio files a queued verb's item list is, and where an item's file is.

ONE WALKER, TWO MODES, AND THE ITEM IS ALWAYS RELATIVE TO THE FROZEN FOLDER.
``analyze restamp`` and ``analyze vocals`` each carried their own copy of a one
level ``iterdir`` scan, identical except for the docstring, and U93 needed both
to grow the same recursive mode. Two copies of a rule that has to agree is how
the source system ended up with five memberships of one extension tuple, so the
rule moved down here where both can reach it.

**THE ITEM ID IS A POSIX RELATIVE PATH, AND UNDER RECURSION IT HAS TO BE.**
``job_items`` is keyed ``PRIMARY KEY (job_id, item_id)``, ``core.jobs``. A
recursive walk that kept bare filenames would hand ``enqueue`` two rows called
``track.flac`` the moment a library held that name in two genre folders, which
is every library, and the insert would raise. The separator is POSIX on every
platform because the id is persisted in a database and read back by a resume,
possibly by a later build, and a stored ``\\`` is a fact about the machine that
queued the job rather than about the job.

**A DIRECTORY SYMLINK IS NOT WALKED, AND THE SKIP IS DECLARED.** ``os.walk`` is
called with ``followlinks=False``, which makes a symlink loop impossible by
construction rather than by a visited set that has to be correct. The cost is
that a genre folder kept as a link to another volume is invisible to a recursive
pass, and a pass that reports cleanly over a subtree it never read is the exact
shape this project files as a defect. So every declined link is counted and
returned, and the verb that called for the walk says so on its envelope.

**DOT DIRECTORIES ARE PRUNED FOR THE REASON DOTFILES ARE SKIPPED.** macOS writes
an AppleDouble sidecar, ``._track.flac``, beside every file on the exFAT volume a
DJ stick is, and it carries the audio suffix. Queued as an item it is decoded,
refused as undecodable, and then refused as missing on the next claim. A dot
DIRECTORY is the same argument one level up: ``.Spotlight-V100`` and
``.Trashes`` sit at the root of that same stick and hold nothing anybody queued.
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS

_ORIGIN = ("core", "discovery")


@dataclass(frozen=True)
class Scan:
    """One walk's answer: the item ids, and the two kinds of thing it did not read.

    The omissions are carried beside the items rather than logged, because the
    only honest place for either is the envelope of the verb that asked, and a
    walker that printed them would be a lower layer deciding how a CLI reports.

    They are two lists and not one because they have two remedies. A declined
    link is a choice this module made and there is nothing to fix; an unreadable
    folder is a permission or a failing disk and somebody has to act.
    """

    items: tuple[str, ...]
    skipped_links: tuple[str, ...]
    unreadable: tuple[str, ...]


def _is_audio(path: Path) -> bool:
    """An item candidate: a real file, not a dotfile, carrying an audio suffix.

    The dotfile clause is not tidiness. ``._track.flac`` is a sidecar with the
    audio suffix, and it is the one that fails a whole job on the next claim.

    ``is_file`` FOLLOWS A LINK, so a track that is a symlink to a file on
    another volume is an item and is tagged through the link. That is what the
    one level scan has always done and U93 did not narrow it, because narrowing
    it would change the default mode every existing job was queued under. Only
    a DIRECTORY link is declined, and the docstring above says only that.
    """
    return (
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
    )


def scan_audio(folder: Path, *, recursive: bool = False) -> Scan:
    """The item ids for the audio under ``folder``, sorted, dotfiles skipped.

    One level by default, which is byte for byte what both queued verbs did
    before U93, so an existing job, an existing resume and ``analyze calibrate``
    are unchanged. Recursive walks the tree and returns POSIX relative paths.

    The two modes agree where they overlap: a top level file's relative path is
    its own name, so switching a folder of loose tracks to recursive produces
    the same item list rather than a second spelling of it.
    """
    if not folder.is_dir():
        return Scan(items=(), skipped_links=(), unreadable=())
    if not recursive:
        return Scan(
            items=tuple(sorted(path.name for path in folder.iterdir() if _is_audio(path))),
            skipped_links=(),
            unreadable=(),
        )

    items: list[str] = []
    skipped: list[str] = []
    unreadable: list[str] = []

    def note(error: OSError) -> None:
        """``os.walk`` SWALLOWS AN ERROR BY DEFAULT, which is the whole hazard.

        Without a callback a folder the process cannot list, a permission the
        library volume carries or an enclosure failing under the walk, simply
        contributes no items and the pass reports cleanly over it. Unlike a
        declined link there is nothing in the output a person could notice, so
        the omission has to be collected here to be sayable at all.
        """
        named = getattr(error, "filename", None)
        unreadable.append(_relative_or_absolute(folder, named))

    root = str(folder)
    for parent, dirnames, filenames in os.walk(root, followlinks=False, onerror=note):
        here = Path(parent)
        # PRUNE IN PLACE, which is the only thing ``os.walk`` reads back. A
        # filtered copy assigned to a new name leaves the walk descending
        # everything, and the bug is silent because the result is a superset.
        kept: list[str] = []
        for name in sorted(dirnames):
            if name.startswith("."):
                continue
            if (here / name).is_symlink():
                skipped.append(_relative(folder, here / name))
                continue
            kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            # THE DOTFILE RULE IS NOT REPEATED HERE. ``_is_audio`` carries it,
            # and a second copy in front of it is a layer that covers the first,
            # which makes reverting either one kill nothing.
            path = here / name
            if _is_audio(path):
                items.append(_relative(folder, path))
    return Scan(
        items=tuple(sorted(items)),
        skipped_links=tuple(sorted(skipped)),
        unreadable=tuple(sorted(set(unreadable))),
    )


def _relative(folder: Path, path: Path) -> str:
    """The id for one path: its position under the folder, POSIX separated."""
    return path.relative_to(folder).as_posix()


def _relative_or_absolute(folder: Path, named: str | None) -> str:
    """An error's path named relatively when it can be, and never dropped.

    ``OSError.filename`` is whatever the platform put there, and on some failures
    it is absent or outside the tree. A path that will not relativise is reported
    whole rather than discarded, because the point of collecting it is that it is
    the only trace of the omission.
    """
    if named is None:
        return "an unnamed folder under this tree"
    try:
        return _relative(folder, Path(named))
    except ValueError:
        return named


#: How many omitted paths a warning spells out before it counts the rest. Small
#: because the sentence is read in a terminal, and the count carries the size.
SHOWN = 5


def _named(paths: tuple[str, ...]) -> str:
    shown = list(paths[:SHOWN])
    rest = len(paths) - len(shown)
    return ", ".join(shown) + (f", and {rest} more" if rest else "")


def _folders(count: int) -> str:
    """"1 folder" and "2 folders". A plural only sentence reads as a defect."""
    return f"{count} folder" if count == 1 else f"{count} folders"


def link_warning(paths: tuple[str, ...]) -> dict[str, str] | None:
    """What a recursive walk declined to enter, phrased for an envelope."""
    if not paths:
        return None
    return {
        "code": "linked-folder-skipped",
        "message": (
            f"{_folders(len(paths))} under this tree "
            f"{'is a symbolic link' if len(paths) == 1 else 'are symbolic links'} "
            f"and {'was' if len(paths) == 1 else 'were'} not walked, so no track "
            f"inside {'it' if len(paths) == 1 else 'one'} was queued: {_named(paths)}"
        ),
    }


def unreadable_warning(paths: tuple[str, ...]) -> dict[str, str] | None:
    """What a recursive walk could not list, phrased for an envelope."""
    if not paths:
        return None
    return {
        "code": "folder-unreadable",
        "message": (
            f"{_folders(len(paths))} under this tree could not be read, so no "
            f"track inside {'it' if len(paths) == 1 else 'one'} was queued; check "
            f"the permissions on {'it' if len(paths) == 1 else 'them'} and that the "
            f"volume is healthy: {_named(paths)}"
        ),
    }


def walk_warnings(
    skipped_links: Sequence[str] = (), unreadable: Sequence[str] = ()
) -> tuple[dict[str, str], ...]:
    """Both omissions as envelope warnings, in the order they are read.

    TAKES THE LISTS AND NOT A ``Scan`` so a RESUME can say the same thing. The
    resume never re-walks, because re-walking would report a tree as it is now
    over a job queued against the tree as it was; it reads the lists the queue
    froze into the payload and phrases them here, through this one function, so
    the queue and the resume cannot describe one omission two ways.
    """
    said = (
        link_warning(tuple(skipped_links)),
        unreadable_warning(tuple(unreadable)),
    )
    return tuple(one for one in said if one is not None)


#: The payload keys a queued verb freezes a walk under, spelled once. A resume
#: reads them back, so two verbs spelling them two ways would make one of the
#: two resumes report nothing while looking correct.
PAYLOAD_RECURSIVE = "recursive"
PAYLOAD_SKIPPED_LINKS = "skipped_links"
PAYLOAD_UNREADABLE = "unreadable_folders"


def frozen_walk(scan: Scan, *, recursive: bool) -> dict[str, object]:
    """The part of a job payload that records what the walk was and what it missed.

    NOT named ``frozen``. ``intake/cli.py`` already has a ``frozen``, one Wanted
    row as a dict, and one word meaning two things in two modules is a shape this
    project files as a defect rather than as a coincidence.
    """
    return {
        PAYLOAD_RECURSIVE: recursive,
        PAYLOAD_SKIPPED_LINKS: list(scan.skipped_links),
        PAYLOAD_UNREADABLE: list(scan.unreadable),
    }


def warnings_of(payload: Mapping[str, Any] | None) -> tuple[dict[str, str], ...]:
    """The walk's omissions read back off a frozen payload, for a resume.

    Tolerant of a payload written by an older build, which carries neither key
    and produces no warnings, which is the correct answer for a job that was
    queued one level.
    """
    held = payload or {}
    return walk_warnings(
        _strings(held.get(PAYLOAD_SKIPPED_LINKS)),
        _strings(held.get(PAYLOAD_UNREADABLE)),
    )


def _strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(one) for one in value)


def item_path(folder: Path, item_id: str) -> Path:
    """The file one item id names inside ``folder``, refusing to leave it.

    THE JOIN IS THE REASON THIS IS A FUNCTION AND NOT AN EXPRESSION. Since U93
    an item id may carry separators, and ``Path("/library") / "/etc/passwd"``
    evaluates to ``/etc/passwd``: an absolute right hand side discards the base
    entirely, silently, and a ``..`` segment walks out of it one level at a
    time. Every id this module produces is relative and free of ``..``, so this
    fires only on a store some other build or some other hand wrote, which is
    why it is reported as a defect rather than as something a person can fix by
    retyping the command.
    """
    candidate = Path(item_id)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise _escapes(folder, item_id)
    return folder / candidate


def _escapes(folder: Path, item_id: str) -> CratekitError:
    return refuse(
        "internal-error",
        f"the job item {item_id!r} does not name a file inside {folder}, so "
        f"nothing was read and nothing was written. An item is a relative path "
        f"under the folder the job froze",
        remedy=Remedy.REPORT_DEFECT,
        origin=_ORIGIN,
        detail={"item": item_id, "folder": str(folder)},
    )
