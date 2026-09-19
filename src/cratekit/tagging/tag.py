"""Write genre (and later art) onto files that are missing them.

Genre is written only when the file has none. Art is written only when a
searcher returns bytes and the file has no usable picture. Both writes go
through ``cratekit.core.tags``, never through a bare mutagen ID3 stream.

Art a file ALREADY carries is repaired first, in place and without the web, by
:func:`cratekit.core.art.repair_in_place`. That runs whatever the genre state,
because the files the vendored downloader left with a zeroed picture block are
mostly files that were tagged long ago.

A searcher that returns nothing is a decline, not a failure. The file
stays untagged and the next run asks again.

THE FOLDER WALK AND THE PER FILE WORK ARE TWO FUNCTIONS, and the split is
what makes this engine drivable as a job. :func:`audio_files` is what a
verb queues one item per, and :func:`tag_one` is what its worker runs for
one of them. :func:`tag_folder` is the same walk applied to every file, so
the two callers cannot come to disagree about which files this engine
covers. A shell that derived the items from its own walk would be a second
opinion about that set, and the drift runs in the expensive direction, a
job reporting done over files it never queued.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from cratekit.core import art, tags
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


#: Why a file was passed over. ``HAS_GENRE`` is the fill-if-empty policy this
#: engine exists to hold; ``NO_HIT`` is a catalogue that answered and had
#: nothing; ``UNMAPPED_GENRE`` is a catalogue that answered with a string the
#: declared taxonomy could not turn into a tag.
#:
#: THE THIRD ONE IS NOT A KIND OF THE SECOND, and telling them apart is the
#: whole reason it exists. A person whose folder came back untagged needs to
#: know whether the catalogues have never heard of these tracks or whether
#: their own taxonomy is missing an alias, because only one of those is theirs
#: to fix.
HAS_GENRE = "has-genre"
NO_HIT = "no-hit"
UNMAPPED_GENRE = "unmapped-genre"


@dataclass(frozen=True, slots=True)
class TagResult:
    """What happened to one file, and what the catalogue said about it.

    ``source`` and ``source_genre`` are carried off the hit even when nothing
    was written, so a skip reason of ``unmapped-genre`` reaches the job's
    committed artifact with the string that could not be mapped. A reason with
    no string beside it tells a person a gap exists and not which one.

    ``art_repair`` is what the in place picture repair found and did, one of
    :data:`cratekit.core.art.REPAIR_STATUSES`, and ``art_repair_detail`` its
    sentence. It is independent of ``skipped``: a file skipped for its genre
    still had its art looked at. The default is ``unchecked`` rather than ``ok``
    so a result built without the repair cannot claim the repair passed.

    NOT CALLED ``art``, because :class:`SearchHit` already has an ``art`` and it
    means picture bytes to write. One name meaning bytes on one class and a
    status on the other, in one file, is the defect ``docs/METHOD.md`` hunts.
    """

    path: Path
    genre_written: str | None
    skipped: str | None = None
    source: str = ""
    source_genre: str = ""
    art_repair: str = art.REPAIR_UNCHECKED
    art_repair_detail: str = ""


def audio_files(root: Path) -> tuple[Path, ...]:
    """Every audio file under ``root``, sorted. The set this engine covers.

    ONE OWNER FOR THE ITEM DERIVATION. A verb queues one job item per entry
    here and :func:`tag_folder` tags one file per entry here, so the queue and
    the walk cannot describe two different sets. Sorted, so two runs over one
    unchanged folder agree about the order as well as the membership.

    A root that is not a directory is EMPTY rather than an error, because the
    caller that meets that case first is a shell deciding whether it has
    anything to queue, and "nothing to do" is the honest answer to give it.
    """
    if not root.is_dir():
        return ()
    return tuple(
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in AUDIO_EXTS
    )


def tag_one(path: Path, *, searcher: Searcher) -> TagResult:
    """Tag ONE file, or report why it was passed over. The per item work.

    FILL IF EMPTY, BY CONSTRUCTION. A file that already carries a genre is
    skipped and never overwritten, because that value is somebody's curation
    until ``crate tag retag`` decides the taxonomy calls it too coarse. The two
    verbs own this field under two different policies and this is where the
    first one lives.

    A DECLINE IS NOT A FAILURE and this function never raises for one. The
    searcher raises when it could not read a catalogue at all, and that
    propagates, because an item that reported done having learned nothing is
    the clean-report-over-unreadable-state cost the merge bar names.

    THE ART REPAIR RUNS FIRST, before the genre check can return. A file that
    already carries a genre is exactly the file the source system repaired, so a
    repair placed after that return would never reach it. The repair never
    raises, so a picture that cannot be fixed is reported and the genre work on
    the same file still happens.
    """
    repair = art.repair_in_place(path)
    repaired = {"art_repair": repair.status, "art_repair_detail": repair.detail}
    existing = tags.read_genre_from_file(path)
    if existing:
        return TagResult(path=path, genre_written=None, skipped=HAS_GENRE, **repaired)
    artist = tags.read_tag(path, "artist") or ""
    title = tags.read_tag(path, "title") or path.stem
    hit = searcher(artist, title)
    if hit is None:
        return TagResult(path=path, genre_written=None, skipped=NO_HIT, **repaired)
    if not hit.genre:
        # THE SOURCE GENRE IS WHAT SEPARATES THE TWO REASONS. A hit carrying one
        # means a catalogue answered and the taxonomy could not map its word; a
        # hit carrying none means nothing was found to map.
        reason = UNMAPPED_GENRE if hit.source_genre else NO_HIT
        return TagResult(
            path=path,
            genre_written=None,
            skipped=reason,
            source=hit.source,
            source_genre=hit.source_genre,
            **repaired,
        )
    tags.write_genre(path, hit.genre)
    return TagResult(
        path=path,
        genre_written=hit.genre,
        source=hit.source,
        source_genre=hit.source_genre,
        **repaired,
    )


def tag_folder(root: Path, *, searcher: Searcher) -> list[TagResult]:
    """Tag every audio file under ``root``. ``searcher`` is required.

    The walk plus :func:`tag_one` per file, and nothing else. Every policy
    decision lives one function down, where the job worker reaches it too.
    """
    return [tag_one(path, searcher=searcher) for path in audio_files(root)]


__all__ = [
    "HAS_GENRE",
    "NO_HIT",
    "UNMAPPED_GENRE",
    "SearchHit",
    "Searcher",
    "TagResult",
    "audio_files",
    "tag_folder",
    "tag_one",
]
