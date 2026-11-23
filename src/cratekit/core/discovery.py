"""Which audio files a queued verb's item list is, and where an item's file is.

One walker for every verb that queues a folder, in two modes (U93).

The item id is a POSIX path relative to the frozen folder: ``job_items`` is
keyed on ``(job_id, item_id)``, so a recursive walk cannot use bare names, and
the id is persisted, so its separator must not depend on the machine.

A directory symlink is not walked (``followlinks=False``, so no loop is
possible), and every declined link is counted and returned for the verb's
envelope. Dot directories are pruned and dotfiles skipped, since an AppleDouble
sidecar such as ``._track.flac`` carries the audio suffix.
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

    The omissions travel to the caller's envelope rather than being logged, as
    two lists because they have two remedies: a declined link needs nothing, an
    unreadable folder needs someone to act.
    """

    items: tuple[str, ...]
    skipped_links: tuple[str, ...]
    unreadable: tuple[str, ...]


def _is_audio(path: Path) -> bool:
    """An item candidate: a real file, not a dotfile, carrying an audio suffix.

    ``is_file`` follows a link, so a file symlink is an item; only a directory
    link is declined (U93).
    """
    return (
        path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in AUDIO_EXTS
    )


def scan_audio(folder: Path, *, recursive: bool = False) -> Scan:
    """The item ids for the audio under ``folder``, sorted, dotfiles skipped.

    One level by default, unchanged since before U93; recursive returns POSIX
    relative paths. A top level file has the same id in both modes.
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
        # os.walk swallows an error by default, so an unlistable folder would
        # vanish silently; collect it to be reported.
        unreadable.append(_relative_or_absolute(folder, getattr(error, "filename", None)))

    root = str(folder)
    for parent, dirnames, filenames in os.walk(root, followlinks=False, onerror=note):
        here = Path(parent)
        # Prune in place: the slice is the only thing os.walk reads back.
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
            # The dotfile rule lives in _is_audio alone, so a mutation of it is seen.
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
    """An error's path, relative when it can be, whole when not, and never dropped."""
    if named is None:
        return "an unnamed folder under this tree"
    try:
        return _relative(folder, Path(named))
    except ValueError:
        return named


#: How many omitted paths a warning spells out before it counts the rest.
SHOWN = 5


def _named(paths: tuple[str, ...]) -> str:
    shown = list(paths[:SHOWN])
    rest = len(paths) - len(shown)
    return ", ".join(shown) + (f", and {rest} more" if rest else "")


def _folders(count: int) -> str:
    """"1 folder" and "2 folders". A plural only sentence reads as a defect."""
    return f"{count} folder" if count == 1 else f"{count} folders"


def link_warning(paths: tuple[str, ...], verb: str = "queued") -> dict[str, str] | None:
    """What a recursive walk declined to enter, phrased for an envelope.

    ``verb`` is what the caller would have done with the tracks inside (U94).
    """
    if not paths:
        return None
    return {
        "code": "linked-folder-skipped",
        "message": (
            f"{_folders(len(paths))} under this tree "
            f"{'is a symbolic link' if len(paths) == 1 else 'are symbolic links'} "
            f"and {'was' if len(paths) == 1 else 'were'} not walked, so no track "
            f"inside {'it' if len(paths) == 1 else 'one'} was {verb}: {_named(paths)}"
        ),
    }


def unreadable_warning(paths: tuple[str, ...], verb: str = "queued") -> dict[str, str] | None:
    """What a recursive walk could not list, phrased for an envelope."""
    if not paths:
        return None
    return {
        "code": "folder-unreadable",
        "message": (
            f"{_folders(len(paths))} under this tree could not be read, so no "
            f"track inside {'it' if len(paths) == 1 else 'one'} was {verb}; check "
            f"the permissions on {'it' if len(paths) == 1 else 'them'} and that the "
            f"volume is healthy: {_named(paths)}"
        ),
    }


def walk_warnings(
    skipped_links: Sequence[str] = (), unreadable: Sequence[str] = (), *, verb: str = "queued"
) -> tuple[dict[str, str], ...]:
    """Both omissions as envelope warnings, in the order they are read.

    Takes the lists, not a ``Scan``, so a resume phrases the frozen lists the
    same way the queue did, without re-walking.
    """
    said = (
        link_warning(tuple(skipped_links), verb),
        unreadable_warning(tuple(unreadable), verb),
    )
    return tuple(one for one in said if one is not None)


#: The payload keys a queued verb freezes a walk under, spelled once for every resume.
PAYLOAD_RECURSIVE = "recursive"
PAYLOAD_SKIPPED_LINKS = "skipped_links"
PAYLOAD_UNREADABLE = "unreadable_folders"


def frozen_walk(scan: Scan, *, recursive: bool) -> dict[str, object]:
    """The part of a job payload that records what the walk was and what it missed."""
    return {
        PAYLOAD_RECURSIVE: recursive,
        PAYLOAD_SKIPPED_LINKS: list(scan.skipped_links),
        PAYLOAD_UNREADABLE: list(scan.unreadable),
    }


def warnings_of(payload: Mapping[str, Any] | None) -> tuple[dict[str, str], ...]:
    """The walk's omissions read back off a frozen payload, for a resume.

    An older payload carries neither key and gives no warnings.
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

    An absolute id would discard the base and ``..`` walks out of it. No id
    this module makes does either, so a refusal is reported as a defect.
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
