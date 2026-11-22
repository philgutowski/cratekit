"""Every intake shape becomes one ``Wanted`` list (R13).

A set URL, a pasted tracklist (a transcribed screenshot too) and a file on
disk arrive differently; matching and acquisition know one shape. A URL is
not a file: fetching a playlist belongs to the playlist verb.
"""

from __future__ import annotations

from pathlib import Path

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
        raise refuse("intake-list-unusable", str(exc), origin=("intake.normalize",)) from exc


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
        # The stem is the only identity; matching then asks rather than joins.
        artist = "unknown"
    return (
        Wanted(
            artist=artist,
            title=title,
            origin=match.TEXT,
            ref=str(path.resolve()),
        ),
    )
