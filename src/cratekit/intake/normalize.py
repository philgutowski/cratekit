"""Every intake shape becomes one ``Wanted`` list (R13).

A set URL, a pasted tracklist, a public playlist, and a file already on disk
look different on the way in. Matching and acquisition only know one shape.
This module is the conversion. After it returns, the rest of the pipeline
does not care which door the list walked through.

Screenshot intake is not an OCR problem. The operator transcribes the image
and this module reads the same pasted text the tracklist door already
accepts.

A URL is not a file. Fetching a playlist belongs to the playlist verb, which
has a provider session. This module refuses a URL handed to the text reader
rather than treating the address as a title.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from cratekit.acquire import match
from cratekit.acquire.match import Wanted
from cratekit.core.cause import refuse
from cratekit.core.naming import AUDIO_EXTS

_URL_SCHEME = ("http://", "https://")


def is_url(value: str) -> bool:
    text = value.strip().lower()
    return text.startswith(_URL_SCHEME)


def from_tracklist(text: str) -> tuple[Wanted, ...]:
    """Pasted artist-title lines, including a transcribed screenshot."""
    try:
        return match.read_text_lines(text)
    except match.UnreadableList as exc:
        raise refuse(
            "intake-list-unusable",
            str(exc),
            origin=("intake.normalize",),
        ) from exc


def from_path(path: Path) -> tuple[Wanted, ...]:
    """A text file of artist-title lines, never a web address."""
    name = str(path)
    if is_url(name):
        raise refuse(
            "intake-list-unusable",
            f"{name} is a web address rather than a list on this machine",
            origin=("intake.normalize",),
            detail={"source": name},
        )
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise refuse(
            "intake-list-unusable",
            f"{name} could not be read: {exc.strerror}",
            origin=("intake.normalize",),
            detail={"source": name},
        ) from exc
    return from_tracklist(raw)


def from_audio_file(path: Path) -> tuple[Wanted, ...]:
    """One file already on disk. No network, no recognition."""
    if not path.is_file():
        raise refuse(
            "intake-list-unusable",
            f"{path} is not a file on this machine",
            origin=("intake.normalize",),
            detail={"source": str(path)},
        )
    if path.suffix.lower() not in AUDIO_EXTS:
        raise refuse(
            "intake-list-unusable",
            f"{path.name} is not an audio file this pipeline ingests",
            origin=("intake.normalize",),
            detail={"source": str(path)},
        )
    from cratekit.core import tags

    artist = tags.read_tag(path, "artist") or ""
    title = tags.read_tag(path, "title") or path.stem
    if not artist:
        # A file with no artist tag still has to become a Wanted. The stem
        # is the only identity we have; matching will then ask rather than
        # invent a join.
        artist = "unknown"
    return (
        Wanted(
            artist=artist,
            title=title,
            origin=match.TEXT,
            ref=str(path.resolve()),
        ),
    )


def from_wanted(rows: Iterable[Wanted]) -> tuple[Wanted, ...]:
    """Identity. A caller that already has Wanted rows stays on this type."""
    return tuple(rows)
