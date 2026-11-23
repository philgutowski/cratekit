"""Write genre and album art onto files that are missing them.

Genre is written only when the file has none, through ``cratekit.core.tags``.
Art is written only when the file carries no picture at all, through
``cratekit.core.art``; any picture it has is repaired in place first, whatever
the genre state, and never downloaded over. The two needs are independent, so
a tagged file with no picture is still searched. The picture comes off the
same catalogue row as the genre, so a file never wears another record's art,
and is fetched through an injected :data:`FetchImage`. A failed fetch, like a
search that finds nothing, is a decline, never a failure.

Seams the shell hands in, so this module reads tags and asks: a general
catalogue asked by ISRC for a file the record shops gave no genre
(:data:`PublishedGenre`, R-796); a registered label's genre, written before
any search (:data:`LabelGenre`, U178), with ``folder_genre`` answering
``--label`` by identifier (R-1476); and the labels a copyright line names
(:data:`CopyrightLabels`, U240), deciding a file only when exactly one, with
a genre, is named.

:func:`audio_files` is what a verb queues one item per and :func:`tag_one`
what its worker runs, so the queue and the walk cover one set of files.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace
from pathlib import Path

from cratekit.core import art, tags
from cratekit.core.cause import CratekitError, rebuilt, refuse
from cratekit.core.naming import AUDIO_EXTS
from cratekit.tagging import titles

Searcher = Callable[[str, str], "SearchHit | None"]

#: The general catalogue's seam: given the searcher's hit and the file's ISRC
#: tag (None for a file needing no genre), the hit to act on. Never raises;
#: shipped as :func:`cratekit.tagging.published.second_opinion`.
PublishedGenre = Callable[["SearchHit", "str | None"], "SearchHit"]

@dataclass(frozen=True, slots=True)
class LabelAnswer:
    """A registered label (its registry display name) and its genre."""

    label: str
    genre: str


#: The label registry's seam (U178): given a label's name, the label and its
#: genre, or None. Never raises; built by ``cratekit.tagging.cli``.
LabelGenre = Callable[[str], "LabelAnswer | None"]

@dataclass(frozen=True, slots=True)
class CopyrightLabel:
    """A registered label a copyright line names, and its genre or None.

    The genre travels with the name, so two labels sharing a display name
    never lend each other one (U240's review).
    """

    label: str
    genre: str | None = None


#: The copyright line's seam (U240): every registered label a line names, with
#: a genre or without. Never raises; built by ``cratekit.tagging.cli``.
CopyrightLabels = Callable[[str], "tuple[CopyrightLabel, ...]"]

#: The detail key a failed file's refusal carries its copyright line's labels
#: under when the line could not settle it (U240).
COPYRIGHT_LABELS_DETAIL = "copyright_labels"

#: How a file's label was named, when its genre was written (U240).
NAMED_BY_TAG = "tag"
NAMED_BY_FOLDER = "folder"
NAMED_BY_COPYRIGHT = "copyright"

#: The source a file's record names when its genre came from its label (U178):
#: never counted as a catalogue's, and never ``off_taxonomy``.
LABEL_GENRE = "label-genre"

#: The refusal a file that would not take its genre fails its item with (U178).
UNWRITTEN_REASON = "tag-folder-unwritten"


def _written(path: Path, genre: str, source: str) -> str:
    """Write ``genre`` onto ``path`` and return it, or refuse when the file would not take it.

    The writer's False is a failure, not a tag (U178): the item fails with the
    file named, and the rest of the folder goes on.
    """
    if not tags.write_genre(path, genre):
        raise refuse(
            UNWRITTEN_REASON,
            f"{path} would not take the genre {genre!r} from {source}, so it carries "
            f"none; nothing else about it was changed",
            steps=(
                "check the file can be written, is not locked and is not on a read "
                "only volume, then run the tagging verb over the folder again",
            ),
            origin=("tagging", "tag"),
            detail={"path": str(path), "genre": genre, "source": source},
        )
    return genre


#: This product's own staging trees, which :func:`audio_files` does not descend
#: into. A hand copy of ``acquire.cli.ACQUIRE_STAGING_DIRNAME`` and
#: ``master.cli.MASTER_STAGING_DIRNAME`` (importing them would break KTD23),
#: pinned to them by ``tests/test_tagging_engine.py``.
SKIPPED_DIRNAMES: frozenset[str] = frozenset(
    {".cratekit-acquire-staging", ".cratekit-master-staging"}
)

#: macOS's AppleDouble sidecar, ``._track.flac`` on an exFAT or FAT volume.
#: Two characters, since one would take ``...Ready For It.flac`` with it.
APPLEDOUBLE_PREFIX = "._"

#: Given a picture's URL, its bytes or None; shipped through
#: :func:`cratekit.tagging.searchers.for_images`.
FetchImage = Callable[[str], "bytes | None"]


@dataclass(frozen=True, slots=True)
class SourceAnswer:
    """What one catalogue said about one track, as the item's record keeps it.

    ``answer`` is a word, ``searchers.Answer``'s or ``not-asked``: this module
    sits below the searcher.
    """

    source: str
    answer: str
    source_genre: str = ""
    note: str = ""


@dataclass(frozen=True, slots=True)
class SearchHit:
    """What a catalogue search is willing to write, and what it was answering.

    ``source`` and ``source_genre`` ride a decline too (``genre`` None), so a
    person learns which alias is missing. ``art_url`` is the picture on the
    genre's own row, or the matching record shop's row for a source naming no
    picture (U282); a URL, since whether one is needed is :func:`tag_one`'s
    question. ``off_taxonomy`` marks the catalogue's own word passed through
    by :func:`cratekit.core.routing.suggest_tag` (R-650). ``art_source`` names
    the catalogue the picture belongs to when not ``source`` (R-796, U282).
    ``unread`` names the catalogues that left the question open (R-791,
    U244). ``ask_picture`` is a picture question left for :func:`tag_one` to
    ask only of a file with none (U282); ``asked`` is the question the
    catalogues were asked (U289); neither is part of a hit's value. Every
    field defaults empty, so a fake searcher works unchanged.
    """

    genre: str | None = None
    source: str = ""
    source_genre: str = ""
    art_url: str = ""
    off_taxonomy: bool = False
    answers: tuple[SourceAnswer, ...] = ()
    unread: tuple[str, ...] = ()
    art_source: str | None = None
    ask_picture: Callable[[SearchHit], SearchHit] | None = field(
        default=None, compare=False, repr=False
    )
    asked: titles.Question | None = field(default=None, compare=False)


#: Why a file was passed over: it has a genre (fill if empty); no catalogue
#: had it; a catalogue's word the taxonomy could not map, apart from no-hit
#: because only that one is the person's to fix; some catalogue went unread,
#: so no-hit would be false (R-791); or the general catalogue could not be
#: asked for want of an ISRC (R-796), also that catalogue's answer word.
HAS_GENRE = "has-genre"
NO_HIT = "no-hit"
UNMAPPED_GENRE = "unmapped-genre"
SOURCES_UNREAD = "sources-unread"
NO_ISRC = "no-isrc"
SKIP_REASONS: tuple[str, ...] = (HAS_GENRE, NO_HIT, UNMAPPED_GENRE, SOURCES_UNREAD, NO_ISRC)

#: What happened about a picture for a file that had none. ``PRESENT``: it has
#: one, never downloaded over. ``UNAVAILABLE``: a decline. ``ERROR``: the file
#: would not take one in hand. ``UNCHECKED``: the need was never known, never
#: read as ``PRESENT``.
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

    ``source`` and ``source_genre`` ride a skip too, so ``unmapped-genre``
    names its string. ``art_repair`` is the in place repair's status and
    ``art_fetch`` what happened about new art, each with its sentence and each
    ``unchecked`` by default, so nothing built without them claims a pass.
    ``off_taxonomy`` is a disposition of a write, never a skip reason (R-650).
    ``label_tag`` is a file's own label tag that named no label with a genre
    (U178); ``label`` the registered label whose genre was written, with
    ``source`` :data:`LABEL_GENRE`; ``label_from`` how it was named, and
    ``copyright_labels`` a line's labels when they did not decide (U240).
    ``asked_*`` is the question the catalogues were asked (U289).
    """

    path: Path
    genre_written: str | None
    skipped: str | None = None
    source: str = ""
    source_genre: str = ""
    off_taxonomy: bool = False
    answers: tuple[SourceAnswer, ...] = ()
    unread: tuple[str, ...] = ()
    art_repair: str = art.REPAIR_UNCHECKED
    art_repair_detail: str = ""
    art_fetch: str = ART_UNCHECKED
    art_fetch_detail: str = ""
    label: str = ""
    label_tag: str = ""
    label_from: str = ""
    copyright_labels: tuple[str, ...] = ()
    asked_artist: str = ""
    asked_title: str = ""
    asked_read: str = ""


def file_genres(path: Path) -> tuple[str, ...] | None:
    """Every genre value the file holds, or None when it could not be read.

    A failed read is never taken for a blank field.
    """
    try:
        values = tags.read_tag_values_checked(path, "genre") or ()
    except (tags.TagReadFailed, OSError):
        return None
    return tuple(word for word in (value.strip() for value in values) if word)


def relative(path: Path, root: Path) -> str:
    """``path`` as it reads under ``root``, or whole when it is not under it."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def audio_files(root: Path) -> tuple[Path, ...]:
    """Every audio file under ``root``, sorted. The set this engine covers.

    The one item derivation, so the queue and the walk cannot disagree; empty
    for a root that is no directory. Two producers are skipped by name, never
    every dot name (``...Ready For It.flac`` is a track): this product's
    staging trees, :data:`SKIPPED_DIRNAMES`, matched relative to ``root`` so a
    tree named directly is walked, and the AppleDouble sidecar.
    """
    if not root.is_dir():
        return ()
    return tuple(
        path
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path.suffix.lower() in AUDIO_EXTS
        and not path.name.startswith(APPLEDOUBLE_PREFIX)
        and not SKIPPED_DIRNAMES.intersection(path.relative_to(root).parts[:-1])
    )


def _art_settled(path: Path) -> dict[str, str] | None:
    """The art result for a file that needs no picture, or None when it needs one.

    Any picture settles it, sound or broken (the repair looks after a broken
    one); unreadable pictures are ``unchecked``, never sent to the web.
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

    A missing picture must not fail an item whose genre was just written.
    """

    def result(status: str, detail: str = "") -> dict[str, str]:
        return {"art_fetch": status, "art_fetch_detail": detail}

    # Whose row the picture belongs to: the hit's source unless it says otherwise.
    pictured_by = "" if hit is None else (
        hit.source if hit.art_source is None else hit.art_source
    )
    if hit is None or (not hit.art_url and not pictured_by):
        # A decline: no catalogue that names pictures matched.
        unread = hit.unread if hit is not None else ()
        named = f"{', '.join(unread)} went unread and no other catalogue" if unread else (
            "no catalogue"
        )
        if hit is not None and hit.source:
            # The genre's source is not asked for pictures, yet carried the track.
            return result(
                ART_UNAVAILABLE,
                f"{named} that is asked for pictures carried the track, so no "
                f"picture was named; {hit.source} answered about the genre and is "
                f"not asked for one",
            )
        return result(ART_UNAVAILABLE, f"{named} carried the track, so no picture was named")
    if not hit.art_url:
        return result(
            ART_UNAVAILABLE, f"{pictured_by or 'the catalogue'} named no picture for the track"
        )
    if fetch_image is None:
        return result(ART_UNAVAILABLE, "no image fetch was supplied, so the picture was not asked for")
    url = hit.art_url
    try:
        data = fetch_image(url)
    # A bare except: the seam is injected, and every failure is one fact.
    except Exception as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
    if not data:
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched")
    try:
        # Remembered by its bytes (U260), so an album's cover is encoded once.
        cdj = art.to_cdj_jpeg_remembered(data)
    except art.ArtError as exc:
        return result(ART_UNAVAILABLE, f"what {url} returned is not a usable picture: {exc}")
    try:
        written = art.write_front_cover(path, cdj.data)
    except Exception as exc:  # noqa: BLE001 - the contract is never raises
        return result(ART_ERROR, f"the picture could not be written: {exc}")
    if not written:
        return result(ART_ERROR, "the picture could not be written to the file")
    return result(ART_EMBEDDED, f"{cdj.width} by {cdj.height} from {pictured_by or url}")


def _picture_asked(hit: SearchHit) -> tuple[SearchHit, dict[str, str] | None]:
    """The hit with its picture's question asked (U282), and the art result if that failed.

    Asked after the genre is saved, only for a file with no picture. Never
    raises, for :func:`_art_embedded`'s reason.
    """
    ask = hit.ask_picture
    assert ask is not None
    try:
        return replace(ask(hit), ask_picture=None), None
    # A bare except, as the image fetch's.
    except Exception as exc:  # noqa: BLE001
        said = f"{exc.cause.reason}: {exc.cause.message}" if isinstance(exc, CratekitError) else str(exc)
        return replace(hit, ask_picture=None), {
            "art_fetch": ART_UNAVAILABLE,
            "art_fetch_detail": f"the picture could not be asked for: {said}",
        }


@dataclass(frozen=True, slots=True)
class _Labelled:
    """What the label tier found for one file: its answer, and how it got there."""

    answer: LabelAnswer | None
    own: str = ""
    named_by: str = ""
    copyright_labels: tuple[str, ...] = ()


def _by_label(
    path: Path,
    label_genre: LabelGenre,
    label: str | None,
    copyright_labels: CopyrightLabels | None = None,
    folder_genre: LabelGenre | None = None,
) -> _Labelled:
    """The registered genre for this file's label, the file's own label tag, and how it was named.

    The file's own tag wins, being likeliest right about itself; ``label``
    names a file that carries none. The copyright line comes last (U240) and
    decides only when it names exactly one registered label.
    """
    if copyright_labels is None:
        own = tags.read_tag(path, "label") or ""
        line = ""
    else:
        held = tags.read_tags(path, ("label", "copyright"))
        own = held["label"] or ""
        line = held["copyright"] or ""
    if own:
        return _Labelled(label_genre(own), own, NAMED_BY_TAG)
    typed = (label or "").strip()
    if typed:
        return _Labelled((folder_genre or label_genre)(typed), own, NAMED_BY_FOLDER)
    if copyright_labels is None or not line.strip():
        return _Labelled(None, own)
    named = tuple(copyright_labels(line))
    if len(named) != 1 or not named[0].genre:
        return _Labelled(None, own, copyright_labels=tuple(found.label for found in named))
    answer = LabelAnswer(label=named[0].label, genre=named[0].genre)
    return _Labelled(answer, own, NAMED_BY_COPYRIGHT)


def tag_one(
    path: Path,
    *,
    searcher: Searcher,
    fetch_image: FetchImage | None = None,
    published: PublishedGenre | None = None,
    label_genre: LabelGenre | None = None,
    label: str | None = None,
    copyright_labels: CopyrightLabels | None = None,
    folder_genre: LabelGenre | None = None,
) -> TagResult:
    """Tag ONE file, or report why it was passed over. The per item work.

    Fill if empty: a genre a file carries is curation, left for ``tag retag``.
    A catalogue's own word is written too, carrying ``off_taxonomy`` (R-650).
    The art repair runs first, whatever the genre state, and the search is
    skipped only for a file with both a genre and a picture.

    A decline never raises. A searcher that could not read any catalogue
    raises for a file needing its genre, and for one searched only for its art
    becomes an ``unavailable`` picture. The general catalogue is asked after
    the searcher, never instead of one that raised (R-796); ``no-isrc`` is the
    skip reason when nothing else explains the file.

    A registered label's genre is written before any search (U178), the
    picture still searched for; ``label`` is answered by ``folder_genre`` when
    given (R-1476) and ``copyright_labels`` reads a line (U240). A picture left
    unasked is asked only for a file with none, after the genre is saved
    (U282). A file with no tags is asked by its name (U289), read past the
    ``_PN`` tail a title tag never is (R-1724).
    """
    repair = art.repair_in_place(path)
    repaired = {"art_repair": repair.status, "art_repair_detail": repair.detail}
    existing = tags.read_genre_from_file(path)
    settled = _art_settled(path)
    if existing and settled is not None:
        return TagResult(
            path=path, genre_written=None, skipped=HAS_GENRE, **repaired, **settled
        )
    tier = (
        _Labelled(None)
        if existing or label_genre is None
        else _by_label(path, label_genre, label, copyright_labels, folder_genre)
    )
    by_label, label_tag = tier.answer, tier.own
    labelled: dict = {}
    if by_label is not None:
        label_tag = ""
        _written(path, by_label.genre, f"its label {by_label.label}")
        labelled = {
            "genre_written": by_label.genre,
            "source": LABEL_GENRE,
            "source_genre": by_label.genre,
            "label": by_label.label,
            "label_from": tier.named_by,
        }
        if settled is not None:
            return TagResult(path=path, **labelled, **repaired, **settled)
    # Every other file reaching this line is asked for its art only.
    needs_genre = not existing and by_label is None
    artist = tags.read_tag(path, "artist") or ""
    title_tag = tags.read_tag(path, "title")
    # A name is read past the older naming's tail, a title tag never (R-1724).
    title = title_tag or titles.name_title(path.stem)
    named = titles.by_name(path.stem) if not artist and not title_tag else None
    if named is not None:
        artist = named.artist
    try:
        hit = searcher(artist, title)
    except CratekitError as exc:
        if needs_genre and tier.copyright_labels and type(exc) is CratekitError:
            # A plain refusal only, so a searcher's ``Parked`` reaches the job as
            # itself; the line's labels ride on it, since a failed item keeps no
            # record (U240's review).
            raise rebuilt(
                exc,
                replace(
                    exc.cause,
                    detail={
                        **dict(exc.cause.detail or {}),
                        COPYRIGHT_LABELS_DETAIL: list(tier.copyright_labels),
                    },
                ),
            ) from exc
        if needs_genre:
            raise
        unread = {
            "art_fetch": ART_UNAVAILABLE,
            "art_fetch_detail": f"{exc.cause.reason}: {exc.cause.message}",
        }
        if by_label is not None:
            return TagResult(path=path, **labelled, **repaired, **unread)
        return TagResult(path=path, genre_written=None, skipped=HAS_GENRE, **repaired, **unread)
    if published is not None and hit is not None:
        # The ISRC is read only for a file the seam could be asked about; None
        # says nothing is to be asked, unlike a tag that is there and empty.
        wanted = needs_genre and not hit.genre
        hit = published(hit, (tags.read_tag(path, "isrc") or "") if wanted else None)
    written: str | None = None
    off_taxonomy = False
    if existing:
        skipped: str | None = HAS_GENRE
    elif by_label is not None:
        # WRITTEN ABOVE, before the search, and only reported here.
        skipped = None
        written = by_label.genre
    elif hit is None:
        skipped = NO_HIT
    elif not hit.genre:
        # A source genre means unmapped; with none, no-hit only when no
        # catalogue went unread (R-791).
        if hit.source_genre:
            skipped = UNMAPPED_GENRE
        elif hit.unread:
            skipped = SOURCES_UNREAD
        elif any(said.answer == NO_ISRC for said in hit.answers):
            skipped = NO_ISRC
        else:
            skipped = NO_HIT
    else:
        skipped = None
        written = _written(path, hit.genre, hit.source or "a catalogue")
        # Only on the branch that wrote: a tagged file's hit was for its art.
        off_taxonomy = hit.off_taxonomy
    # The picture is embedded after the genre, so the last save carries it.
    unasked: dict[str, str] | None = None
    if settled is None and hit is not None and hit.ask_picture is not None:
        hit, unasked = _picture_asked(hit)
    if settled is not None:
        pictured = settled
    elif unasked is not None:
        pictured = unasked
    else:
        pictured = _art_embedded(path, hit, fetch_image)
    found = (
        {
            "source": hit.source,
            "source_genre": hit.source_genre,
            "answers": hit.answers,
            "unread": hit.unread,
        }
        if hit
        else {}
    )
    if hit is not None and hit.asked is not None:
        # How a name was read outranks how its title was.
        read = hit.asked.read
        if named is not None and named.read in (titles.Read.BY_NAME, titles.Read.NAME_AMBIGUOUS):
            read = named.read
        found = {
            **found,
            "asked_artist": hit.asked.artist,
            "asked_title": hit.asked.title,
            "asked_read": read.value,
        }
    if by_label is not None:
        # The label is the genre's source, whatever answered about the picture.
        found = {
            **found,
            **{key: labelled[key] for key in ("source", "source_genre", "label", "label_from")},
        }
    return TagResult(
        path=path,
        genre_written=written,
        skipped=skipped,
        off_taxonomy=off_taxonomy,
        label_tag=label_tag,
        copyright_labels=tier.copyright_labels,
        **found,
        **repaired,
        **pictured,
    )


def tag_folder(
    root: Path,
    *,
    searcher: Searcher,
    fetch_image: FetchImage | None = None,
    published: PublishedGenre | None = None,
    label_genre: LabelGenre | None = None,
    label: str | None = None,
    copyright_labels: CopyrightLabels | None = None,
) -> list[TagResult]:
    """Tag every audio file under ``root``: the walk plus :func:`tag_one` per file."""
    return [
        tag_one(
            path,
            searcher=searcher,
            fetch_image=fetch_image,
            published=published,
            label_genre=label_genre,
            label=label,
            copyright_labels=copyright_labels,
        )
        for path in audio_files(root)
    ]


__all__ = [
    "APPLEDOUBLE_PREFIX",
    "ART_EMBEDDED",
    "ART_ERROR",
    "ART_FETCH_STATUSES",
    "ART_PRESENT",
    "ART_UNAVAILABLE",
    "ART_UNCHECKED",
    "HAS_GENRE",
    "LABEL_GENRE",
    "NAMED_BY_COPYRIGHT",
    "NAMED_BY_FOLDER",
    "NAMED_BY_TAG",
    "SKIPPED_DIRNAMES",
    "SKIP_REASONS",
    "NO_HIT",
    "NO_ISRC",
    "SOURCES_UNREAD",
    "UNMAPPED_GENRE",
    "COPYRIGHT_LABELS_DETAIL",
    "CopyrightLabel",
    "CopyrightLabels",
    "FetchImage",
    "LabelAnswer",
    "LabelGenre",
    "PublishedGenre",
    "SearchHit",
    "Searcher",
    "SourceAnswer",
    "TagResult",
    "UNWRITTEN_REASON",
    "audio_files",
    "file_genres",
    "relative",
    "tag_folder",
    "tag_one",
]
