"""Write genre and album art onto files that are missing them.

Genre is written only when the file has none. Art is written only when the
file carries NO picture at all, the source system's rule: a file with any
embedded picture is repaired in place and never re-downloaded. Genre goes
through ``cratekit.core.tags`` and art through ``cratekit.core.art``, never
through a bare mutagen ID3 stream.

ART AND GENRE ARE TWO INDEPENDENT NEEDS, so a file with a genre and no picture
is still searched, and one with both is not. The picture's URL comes off the
SAME catalogue row the genre came off, the one the searcher's artist and title
gate chose, because a cover taken from a different row is how a file ends up
wearing another record's art. The image itself is fetched through an injected
:data:`FetchImage`, so the suite drives every branch with nothing on the
network. A fetch that fails, or bytes that are not a picture, are a DECLINE,
``unavailable``, and never an item failure.

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

#: Given a picture's URL, its bytes, or None when there are none to be had. The
#: shipped one is :func:`cratekit.tagging.searchers.default_image_fetch`, paced
#: like every other catalogue touch.
FetchImage = Callable[[str], "bytes | None"]


@dataclass(frozen=True, slots=True)
class SearchHit:
    """What a catalogue search is willing to write, and what it was answering.

    ``source`` and ``source_genre`` are carried even when ``genre`` is None,
    because that combination is a DECLINE and a decline that cannot say what it
    declined is one nobody can act on. The searcher resolves a catalogue's raw
    string through the declared taxonomy, and when the taxonomy has no alias for
    it the only useful thing to report is the string itself, so a person learns
    which alias they are missing rather than only that something was unmapped.

    ``art_url`` is the picture on the SAME catalogue row as the genre, or empty
    when that row names none. A URL rather than bytes, because whether the file
    needs a picture at all is :func:`tag_one`'s question and a searcher that
    downloaded eagerly would spend a paced fetch on every file that already has
    one.

    All of them default to empty so a caller that predates them, and a fake
    searcher in a suite, keep working unchanged.
    """

    genre: str | None = None
    source: str = ""
    source_genre: str = ""
    art_url: str = ""


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

#: What happened about a picture for a file that had none, or why nothing was
#: asked. ``PRESENT`` is the never re-download rule holding: the file carries a
#: picture, whatever state the repair left it in. ``UNAVAILABLE`` is a DECLINE,
#: no catalogue row named a picture, or the one it named could not be fetched or
#: was not an image. ``ERROR`` is a picture in hand that the file would not
#: take. ``UNCHECKED`` says the need was never known, a container with no
#: picture handling or a file that could not be read, and it is not a kind of
#: ``PRESENT``, because reading "could not look" as "has art" is absence read
#: as evidence.
ART_EMBEDDED = "embedded"
ART_PRESENT = "present"
ART_UNAVAILABLE = "unavailable"
ART_ERROR = "error"
ART_UNCHECKED = "unchecked"
ART_FETCH_STATUSES: tuple[str, ...] = (
    ART_EMBEDDED,
    ART_PRESENT,
    ART_UNAVAILABLE,
    ART_ERROR,
    ART_UNCHECKED,
)


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

    ``art_fetch`` is what happened about NEW art, one of
    :data:`ART_FETCH_STATUSES`, and ``art_fetch_detail`` its sentence. The two
    art fields answer two questions, the picture a file already had and the
    picture it was missing, so neither is called ``art``, which is also this
    module's name for :mod:`cratekit.core.art`. The default is ``unchecked``
    for the same reason as the repair's.
    """

    path: Path
    genre_written: str | None
    skipped: str | None = None
    source: str = ""
    source_genre: str = ""
    art_repair: str = art.REPAIR_UNCHECKED
    art_repair_detail: str = ""
    art_fetch: str = ART_UNCHECKED
    art_fetch_detail: str = ""


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


def _art_settled(path: Path) -> dict[str, str] | None:
    """The art result for a file that needs no picture, or None when it needs one.

    ANY picture settles it, sound or broken, because the source system never
    re-downloaded over art a file already carried and the repair above this
    call is what looks after a broken one. A file whose pictures could not be
    looked at is ``unchecked`` rather than needing one, so an unreadable file is
    never sent to the web on the strength of a read that failed.
    """
    try:
        pictures = art.read_pictures(path)
    except (tags.UnsupportedContainer, art.UnreadableFile) as exc:
        return {"art_fetch": ART_UNCHECKED, "art_fetch_detail": str(exc)}
    if pictures:
        return {"art_fetch": ART_PRESENT, "art_fetch_detail": ""}
    return None


def _art_embedded(path: Path, hit: SearchHit | None, fetch_image: FetchImage | None) -> dict:
    """Fetch the hit's picture and embed it, or say why there is none. Never raises.

    NEVER RAISES, because a picture that cannot be had must not fail an item
    whose genre was just written. Every way the picture is missing is
    ``unavailable`` with a sentence, and a picture in hand that the file would
    not take is ``error``.
    """

    def result(status: str, detail: str = "") -> dict[str, str]:
        return {"art_fetch": status, "art_fetch_detail": detail}

    if hit is None:
        return result(ART_UNAVAILABLE, "no catalogue carried the track, so no picture was named")
    if not hit.art_url:
        return result(
            ART_UNAVAILABLE, f"{hit.source or 'the catalogue'} named no picture for the track"
        )
    if fetch_image is None:
        return result(ART_UNAVAILABLE, "no image fetch was supplied, so the picture was not asked for")
    url = hit.art_url
    try:
        data = fetch_image(url)
    # A bare except, on purpose. The seam is injected, and every way it can fail
    # is one fact for this file: the picture could not be had.
    except Exception as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
    if not data:
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched")
    try:
        cdj = art.to_cdj_jpeg(data)
    except art.ArtError as exc:
        return result(ART_UNAVAILABLE, f"what {url} returned is not a usable picture: {exc}")
    try:
        written = art.write_front_cover(path, cdj.data)
    except Exception as exc:  # noqa: BLE001 - the contract is never raises
        return result(ART_ERROR, f"the picture could not be written: {exc}")
    if not written:
        return result(ART_ERROR, "the picture could not be written to the file")
    return result(ART_EMBEDDED, f"{cdj.width} by {cdj.height} from {hit.source or url}")


def tag_one(
    path: Path, *, searcher: Searcher, fetch_image: FetchImage | None = None
) -> TagResult:
    """Tag ONE file, or report why it was passed over. The per item work.

    FILL IF EMPTY, BY CONSTRUCTION. A file that already carries a genre is
    never overwritten, because that value is somebody's curation until ``crate
    tag retag`` decides the taxonomy calls it too coarse. The two verbs own this
    field under two different policies and this is where the first one lives.
    Its ``skipped`` is ``has-genre`` whether or not it was searched for art.

    THE SEARCH IS SKIPPED ONLY WHEN A FILE HAS BOTH a genre and a picture. Art
    and genre are independent needs, so a tagged file with no picture is asked
    about, and only its art is written. ``fetch_image`` is optional so a caller
    that predates art keeps working; without it a needed picture is reported
    ``unavailable`` rather than fetched.

    A DECLINE IS NOT A FAILURE and this function never raises for one. The
    searcher raises when it could not read a catalogue at all, and that
    propagates, because an item that reported done having learned nothing is
    the clean-report-over-unreadable-state cost the merge bar names. That now
    includes a tagged file searched only for its art, and it is the same
    trade: the item fails and a retry asks again.

    THE ART REPAIR RUNS FIRST, before the genre check can return. A file that
    already carries a genre is exactly the file the source system repaired, so a
    repair placed after that return would never reach it. The repair never
    raises, so a picture that cannot be fixed is reported and the genre work on
    the same file still happens.
    """
    repair = art.repair_in_place(path)
    repaired = {"art_repair": repair.status, "art_repair_detail": repair.detail}
    existing = tags.read_genre_from_file(path)
    settled = _art_settled(path)
    if existing and settled is not None:
        return TagResult(
            path=path, genre_written=None, skipped=HAS_GENRE, **repaired, **settled
        )
    artist = tags.read_tag(path, "artist") or ""
    title = tags.read_tag(path, "title") or path.stem
    hit = searcher(artist, title)
    written: str | None = None
    if existing:
        skipped: str | None = HAS_GENRE
    elif hit is None:
        skipped = NO_HIT
    elif not hit.genre:
        # THE SOURCE GENRE IS WHAT SEPARATES THE TWO REASONS. A hit carrying one
        # means a catalogue answered and the taxonomy could not map its word; a
        # hit carrying none means nothing was found to map.
        skipped = UNMAPPED_GENRE if hit.source_genre else NO_HIT
    else:
        skipped = None
        tags.write_genre(path, hit.genre)
        written = hit.genre
    # THE PICTURE IS EMBEDDED AFTER THE GENRE IS SAVED, so the last save a file
    # sees is the one carrying its art, whatever the genre write does to the
    # rest of the tag block.
    pictured = settled if settled is not None else _art_embedded(path, hit, fetch_image)
    found = {"source": hit.source, "source_genre": hit.source_genre} if hit else {}
    return TagResult(
        path=path, genre_written=written, skipped=skipped, **found, **repaired, **pictured
    )


def tag_folder(
    root: Path, *, searcher: Searcher, fetch_image: FetchImage | None = None
) -> list[TagResult]:
    """Tag every audio file under ``root``. ``searcher`` is required.

    The walk plus :func:`tag_one` per file, and nothing else. Every policy
    decision lives one function down, where the job worker reaches it too.
    """
    return [
        tag_one(path, searcher=searcher, fetch_image=fetch_image) for path in audio_files(root)
    ]


__all__ = [
    "ART_EMBEDDED",
    "ART_ERROR",
    "ART_FETCH_STATUSES",
    "ART_PRESENT",
    "ART_UNAVAILABLE",
    "ART_UNCHECKED",
    "HAS_GENRE",
    "NO_HIT",
    "UNMAPPED_GENRE",
    "FetchImage",
    "SearchHit",
    "Searcher",
    "TagResult",
    "audio_files",
    "tag_folder",
    "tag_one",
]
