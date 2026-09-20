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
from dataclasses import dataclass
from pathlib import Path

from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.naming import AUDIO_EXTS

_ORIGIN = ("core", "discovery")


@dataclass(frozen=True)
class Scan:
    """One walk's answer: the item ids, and what the walk declined to enter.

    ``skipped_links`` is carried beside the items rather than logged, because
    the only honest place for it is the envelope of the verb that asked, and a
    walker that printed it would be a lower layer deciding how a CLI reports.
    """

    items: tuple[str, ...]
    skipped_links: tuple[str, ...]


def _is_audio(path: Path) -> bool:
    """An item candidate: a real file, not a dotfile, carrying an audio suffix.

    The dotfile clause is not tidiness. ``._track.flac`` is a sidecar with the
    audio suffix, and it is the one that fails a whole job on the next claim.
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
        return Scan(items=(), skipped_links=())
    if not recursive:
        return Scan(
            items=tuple(sorted(path.name for path in folder.iterdir() if _is_audio(path))),
            skipped_links=(),
        )

    items: list[str] = []
    skipped: list[str] = []
    root = str(folder)
    for parent, dirnames, filenames in os.walk(root, followlinks=False):
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
    return Scan(items=tuple(sorted(items)), skipped_links=tuple(sorted(skipped)))


def _relative(folder: Path, path: Path) -> str:
    """The id for one path: its position under the folder, POSIX separated."""
    return path.relative_to(folder).as_posix()


def skipped_links_warning(scan: Scan) -> dict[str, str] | None:
    """What a recursive walk declined to enter, phrased for an envelope.

    Here rather than at each verb so the two queued verbs cannot describe one
    omission two ways. ``None`` when there is nothing to say, which is every non
    recursive call and every tree with no links in it.
    """
    if not scan.skipped_links:
        return None
    shown = list(scan.skipped_links[:5])
    rest = len(scan.skipped_links) - len(shown)
    named = ", ".join(shown) + (f", and {rest} more" if rest else "")
    return {
        "code": "linked-folder-skipped",
        "message": (
            f"{len(scan.skipped_links)} folders under this tree are symbolic links "
            f"and were not walked, so no track inside one was queued: {named}"
        ),
    }


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
