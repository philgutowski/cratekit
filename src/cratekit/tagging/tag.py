"""Write genre (and later art) onto files that are missing them.

Genre is written only when the file has none. Art is written only when a
searcher returns bytes and the file has no usable picture. Both writes go
through ``cratekit.core.tags``, never through a bare mutagen ID3 stream.

A searcher that returns nothing is a decline, not a failure. The file
stays untagged and the next run asks again.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from cratekit.core import tags
from cratekit.core.naming import AUDIO_EXTS

Searcher = Callable[[str, str], "SearchHit | None"]


@dataclass(frozen=True, slots=True)
class SearchHit:
    """What a catalogue search is willing to write, and what it was answering.

    ``source`` and ``source_genre`` are carried even when ``genre`` is None,
    because that combination is a DECLINE and a decline that cannot say what it
    declined is one nobody can act on. The searcher resolves a catalogue's raw
    string through the declared taxonomy, and when the taxonomy has no alias for
    it the only useful thing to report is the string itself, so a person learns
    which alias they are missing rather than only that something was unmapped.

    Both default to empty so a caller that predates them, and a fake searcher in
    a suite, keep working unchanged.
    """

    genre: str | None = None
    art: bytes | None = None
    source: str = ""
    source_genre: str = ""


@dataclass(frozen=True, slots=True)
class TagResult:
    path: Path
    genre_written: str | None
    skipped: str | None = None


def tag_folder(root: Path, *, searcher: Searcher) -> list[TagResult]:
    """Tag every audio file under ``root``. ``searcher`` is required."""
    results: list[TagResult] = []
    if not root.is_dir():
        return results
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in AUDIO_EXTS:
            continue
        existing = tags.read_genre_from_file(path)
        if existing:
            results.append(TagResult(path=path, genre_written=None, skipped="has-genre"))
            continue
        artist = tags.read_tag(path, "artist") or ""
        title = tags.read_tag(path, "title") or path.stem
        hit = searcher(artist, title)
        if hit is None or not hit.genre:
            results.append(TagResult(path=path, genre_written=None, skipped="no-hit"))
            continue
        tags.write_genre(path, hit.genre)
        results.append(TagResult(path=path, genre_written=hit.genre))
    return results
