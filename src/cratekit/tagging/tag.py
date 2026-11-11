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

A SECOND, GENERAL CATALOGUE IS A SEAM OF ITS OWN (R-796). The searcher asks the
record shops by artist and title and knows dance music; a file they gave no
usable genre for is offered to :data:`PublishedGenre`, which asks a general
catalogue by the file's ISRC. It is a parameter beside the image fetch rather
than a change to the searcher's signature, so the searcher is asked exactly as
it was, and what is read here is only the ISRC tag the seam needs.

A REGISTERED LABEL'S GENRE IS A TIER BEFORE THE SEARCH (U178). A label Phillip
follows for one style carries that style in the label registry, and a file of
it with no genre is given it through :data:`LabelGenre` without any catalogue
being asked, so a label whose records the shops refuse or do not carry costs
no blocked searches. The seam is handed a label NAME, the file's label tag, or
the verb's ``--label`` for a file that carries none, which the shell hands
over as the label's identifier so two labels sharing a display name are never
confused (R-1476). The registry lookup behind it is the shell's, so this
module reads one more tag and knows nothing of where labels are stored.

A FILE'S COPYRIGHT LINE NAMES ITS LABEL WHEN NOTHING ELSE DOES (U240). A file
with no label tag, swept with no ``--label``, has its copyright line handed to
:data:`CopyrightLabels`, which answers the registered labels the line names.
Exactly one, carrying a genre, tags the file as that label's; none, two, or
one with no genre leaves it to the catalogues as before. The matching is the
shell's too, so this module reads the line and asks.

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
from dataclasses import dataclass, replace
from pathlib import Path

from cratekit.core import art, tags
from cratekit.core.cause import CratekitError, rebuilt, refuse
from cratekit.core.naming import AUDIO_EXTS

Searcher = Callable[[str, str], "SearchHit | None"]

#: The general catalogue's seam. Given the searcher's hit and the file's ISRC
#: tag, the hit to act on. The ISRC is None for a file that needs no genre, so
#: nothing is asked for it and its record still says so; it is the tag's text,
#: possibly empty, for a file that does. The shipped one is
#: :func:`cratekit.tagging.published.second_opinion`. It answers and does not
#: raise: a general catalogue that could not be read is recorded on the hit.
PublishedGenre = Callable[["SearchHit", "str | None"], "SearchHit"]

@dataclass(frozen=True, slots=True)
class LabelAnswer:
    """A registered label and the genre it carries, as :data:`LabelGenre` answers.

    ``label`` is the registry's display name for the label, which is what the
    file's record names, whatever spelling the file's tag used to reach it.
    """

    label: str
    genre: str


#: The label registry's seam (U178). Given a label's name, as a file's label
#: tag or the verb's ``--label`` gives it, the label and its genre, or None for
#: a label the registry does not hold or holds with no genre. The shipped one is
#: built by ``cratekit.tagging.cli`` over the genres frozen into the job. It
#: answers and does not raise.
LabelGenre = Callable[[str], "LabelAnswer | None"]

@dataclass(frozen=True, slots=True)
class CopyrightLabel:
    """A registered label a copyright line names, as :data:`CopyrightLabels` answers.

    ``genre`` is the label's registered genre, or None for a label with none.
    It travels with the name rather than being looked up by it, so two labels
    sharing a display name can never lend each other a genre (U240's review).
    """

    label: str
    genre: str | None = None


#: The copyright line's seam (U240). Given a file's copyright line, every
#: registered label it names, with a genre or without, so a line naming two
#: can be told from a line naming one. The shipped one is built by
#: ``cratekit.tagging.cli`` over the needles and genres frozen into the job,
#: joined by the label's identifier. It answers and does not raise.
CopyrightLabels = Callable[[str], "tuple[CopyrightLabel, ...]"]

#: The detail key a failed file's refusal carries the labels its copyright line
#: named under, when the line could not settle it (U240), so the sweep's report
#: still says why a file the catalogues could not answer was asked of them.
COPYRIGHT_LABELS_DETAIL = "copyright_labels"

#: How a file's label was named, on a file its label's genre was written to
#: (U240): by its own label tag, by the verb's ``--label`` for the folder, or
#: by its copyright line. The record carries it so a person can see which.
NAMED_BY_TAG = "tag"
NAMED_BY_FOLDER = "folder"
NAMED_BY_COPYRIGHT = "copyright"

#: The source a file's record names when its genre came from its label's
#: registered genre rather than from a catalogue (U178). A DISPOSITION OF ITS
#: OWN: not a catalogue hit, so it is never counted as one of theirs, and not
#: ``off_taxonomy``, since the word was checked against the taxonomy when it
#: was registered.
LABEL_GENRE = "label-genre"

#: The refusal a file that would not take its genre fails its item with (U178).
UNWRITTEN_REASON = "tag-folder-unwritten"


def _written(path: Path, genre: str, source: str) -> str:
    """Write ``genre`` onto ``path`` and return it, or refuse when the file would not take it.

    THE WRITER'S FALSE IS A FAILURE, NOT A TAG (U178). ``tags.write_genre``
    returns False rather than raising, so one bad file cannot abort a batch,
    and a caller that ignored it reported a genre the file does not carry: a
    locked file came back ``tagged`` while it sat untagged, which is the clean
    report over a write never performed. The item fails with the file named
    and the rest of the folder goes on, as a catalogue nobody could read does.
    The catalogue path had the same unchecked write before this unit and is
    checked by the same call.
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


#: Directory names :func:`audio_files` does not descend into: this product's own
#: per item staging trees, whose contents belong to an attempt rather than to the
#: library.
#:
#: THE NAMES ARE A HAND COPY AND THE COPY IS PINNED. The authoritative constants
#: are ``acquire.cli.ACQUIRE_STAGING_DIRNAME`` and
#: ``master.cli.MASTER_STAGING_DIRNAME``, and importing either one here would put
#: a CLI shell behind an engine that the shells are supposed to sit on top of
#: (KTD23). ``tests/test_tagging_engine.py`` asserts this set equals those two
#: constants, because an unpinned hand copy is the shape that survives the rename
#: it was supposed to follow.
SKIPPED_DIRNAMES: frozenset[str] = frozenset(
    {".cratekit-acquire-staging", ".cratekit-master-staging"}
)

#: What macOS names its AppleDouble sidecar with. The finder writes
#: ``._track.flac`` beside every file on an exFAT or FAT volume, carrying the
#: audio suffix and none of the audio. Two characters rather than one, because
#: one would take ``...Ready For It.flac`` with it.
APPLEDOUBLE_PREFIX = "._"

#: Given a picture's URL, its bytes, or None when there are none to be had. The
#: shipped one is :func:`cratekit.tagging.searchers.default_image_fetch`, paced
#: like every other catalogue touch.
FetchImage = Callable[[str], "bytes | None"]


@dataclass(frozen=True, slots=True)
class SourceAnswer:
    """What one catalogue said about one track, as the item's record keeps it.

    ``answer`` is a string rather than the searcher's enum because this module
    sits below the searcher and only carries the word: one of
    ``cratekit.tagging.searchers.Answer``'s values, or ``not-asked`` for a
    catalogue the walk never reached.
    """

    source: str
    answer: str
    source_genre: str = ""
    note: str = ""


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

    ``off_taxonomy`` says the genre above is the catalogue's OWN word, passed
    through by the last tier of :func:`cratekit.core.routing.suggest_tag` because
    nothing in the declared table matched it. It rides the hit rather than being
    worked out here, because the only place that can tell it apart from a
    declared tag with no bucket is the tier that answered (R-650).

    ``art_source`` names the catalogue whose row the picture question belongs
    to when that is not ``source``. None, the default, means the two are one
    catalogue. The general catalogue supplies a genre and is never asked for a
    picture (R-796), so a hit it became the source of carries the record shop
    whose row matched, or the empty string when no shop's did, and the report
    about the picture is then written about the shops and not about it.

    ``answers`` is every catalogue's answer, so the item's record can say what
    each one said rather than only the disposition they added up to. ``unread``
    names the catalogues asked whose answer left the question open, blocked,
    unreachable or unparsable. On a decline it is what keeps the file from
    reading as ``no-hit`` (R-791); on a match it only keeps the record's two
    fields agreeing.

    All of them default to empty so a caller that predates them, and a fake
    searcher in a suite, keep working unchanged.
    """

    genre: str | None = None
    source: str = ""
    source_genre: str = ""
    art_url: str = ""
    off_taxonomy: bool = False
    answers: tuple[SourceAnswer, ...] = ()
    unread: tuple[str, ...] = ()
    art_source: str | None = None


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
#:
#: ``SOURCES_UNREAD`` IS NOT A KIND OF ``NO_HIT`` EITHER (R-791). Some catalogue
#: answered MISS and another could not be read, so whether any catalogue
#: carries the track is unknown. Reporting it ``no-hit`` told a person three
#: catalogues were searched when one was, and they tagged by hand on that
#: belief. The file stays untagged and the next run asks again.
#:
#: ``NO_ISRC`` IS NOT A KIND OF ``NO_HIT`` EITHER (R-796). The record shops did
#: not carry the track and the general catalogue, which is asked by ISRC, could
#: not be asked because the file carries none. Whether that catalogue knows the
#: track is unknown, so the file is not reported as one no catalogue carries.
#: It is also the WORD the general catalogue's entry in a file's answers
#: carries for that case, one string for one fact.
HAS_GENRE = "has-genre"
NO_HIT = "no-hit"
UNMAPPED_GENRE = "unmapped-genre"
SOURCES_UNREAD = "sources-unread"
NO_ISRC = "no-isrc"
SKIP_REASONS: tuple[str, ...] = (HAS_GENRE, NO_HIT, UNMAPPED_GENRE, SOURCES_UNREAD, NO_ISRC)

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

    ``off_taxonomy`` IS A THIRD DISPOSITION AND NOT A FOURTH SKIP REASON. The
    file was written, so ``skipped`` is None and ``genre_written`` holds the
    word; what it adds is that the word came from the catalogue rather than from
    the declared table. It is a separate field precisely because the closed set
    above is about files this engine passed over, and folding a write into it
    would make a count of what was tagged disagree with what is on disk (R-650).
    It can only be true on a write: the skips leave it False, because a file
    this engine did not tag has no tag of this engine's to qualify.

    ``answers`` and ``unread`` are carried off the hit as they came, so the
    record says what every catalogue answered. Both are empty for a file nothing
    was asked about.

    ``label_tag`` is the file's own label tag when it was read and named no label
    with a genre, and empty otherwise. The verb reads it to say when a file's
    tag outranked ``--label`` and the file was searched instead (U178).

    ``label`` names the registered label whose genre was written, and is empty
    for every other file (U178). On that file ``source`` is :data:`LABEL_GENRE`
    and ``source_genre`` the label's word, whatever catalogue was asked about
    its picture, so a count of what each catalogue tagged never takes it in.

    ``label_from`` says how that label was named, one of :data:`NAMED_BY_TAG`,
    :data:`NAMED_BY_FOLDER` and :data:`NAMED_BY_COPYRIGHT`, and is empty
    wherever ``label`` is (U240). ``copyright_labels`` is every registered
    label the file's copyright line named when that was not one label with a
    genre, so a file asked of the catalogues says why its line did not decide
    it; empty when the line was not read, named nothing, or decided it.
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


def audio_files(root: Path) -> tuple[Path, ...]:
    """Every audio file under ``root``, sorted. The set this engine covers.

    ONE OWNER FOR THE ITEM DERIVATION. A verb queues one job item per entry
    here and :func:`tag_folder` tags one file per entry here, so the queue and
    the walk cannot describe two different sets. Sorted, so two runs over one
    unchanged folder agree about the order as well as the membership.

    A root that is not a directory is EMPTY rather than an error, because the
    caller that meets that case first is a shell deciding whether it has
    anything to queue, and "nothing to do" is the honest answer to give it.

    TWO PRODUCERS ARE SKIPPED BY NAME, and the walk is otherwise total. Both
    put files carrying an audio suffix under this root and neither one is a
    track:

    * this product's own per item staging trees, :data:`SKIPPED_DIRNAMES`, whose
      contents are the partial download a killed attempt left and the landing
      ``checked_landing`` refused and deliberately left as evidence. Driven
      before this guard: ``audio_files`` over a download root holding
      ``.cratekit-acquire-staging/<job>/0/1.mp3`` returned that file, so
      ``crate tag folder <download_staging>`` queued both kinds as items and a
      tag write would have altered the evidence;
    * macOS's AppleDouble sidecar, :data:`APPLEDOUBLE_PREFIX`. The finder writes
      ``._track.flac`` beside every file on an exFAT or FAT volume, which is what
      a DJ stick is, and the sidecar carries the audio suffix. It is the reason
      ``analysis/cli._audio_in`` skips what it skips.

    **NOT "every dot name", which is what this said first and is wrong here.**
    A leading dot is not reserved on any filesystem this product runs on, and
    the DJ library it walks is full of counterexamples: ``...And Justice For
    All`` is an album directory and ``...Ready For It.flac`` is a track. A broad
    hidden-name rule drops both, silently, and the verb then reports that the
    folder holds no audio it can tag. That is a worse defect than the one the
    guard exists for, and it is worse in the direction this project's merge bar
    cares about, a clean report over files the tool declined to see. Skipping
    the two producers by name costs nothing, because both names are this
    product's own or the operating system's own and neither is a title.

    The directory names are matched RELATIVE TO ``root``. A person who points
    the verb straight at a staging tree has named it deliberately and gets its
    files; what is skipped is a staging tree this walk descended into on its
    own.
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

    # WHOSE ROW THE PICTURE QUESTION BELONGS TO. The hit's source, unless the hit
    # says otherwise: a genre from the general catalogue leaves the picture with
    # the record shop that matched, or with nobody.
    pictured_by = "" if hit is None else (
        hit.source if hit.art_source is None else hit.art_source
    )
    if hit is None or (not hit.art_url and not pictured_by):
        # A DECLINE: no catalogue that names pictures matched, so none named
        # one. Which kind of decline it was decides the sentence, never whether
        # there is one.
        unread = hit.unread if hit is not None else ()
        named = f"{', '.join(unread)} could not be read and no other catalogue" if unread else (
            "no catalogue"
        )
        if hit is not None and hit.source:
            # THE GENRE'S SOURCE IS NOT A PICTURE'S. Saying no catalogue carried
            # the track would be false of the one that just answered about it.
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
    return result(ART_EMBEDDED, f"{cdj.width} by {cdj.height} from {pictured_by or url}")


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
) -> _Labelled:
    """The registered genre for this file's label, the file's own label tag, and how it was named.

    Read only for a file needing a genre. The tag comes back beside the answer
    so a file whose tag named no label with a genre can say so in its record.

    THE FILE'S OWN TAG WINS, and ``label`` names the label of a file that
    carries none. A folder the verb was told is one label's can still hold a
    file whose tag says otherwise, and that file is the one most likely to be
    right about itself: if its own label has no genre it is searched as
    before, rather than given a genre the person meant for the rest.

    THE COPYRIGHT LINE COMES LAST (U240), read only for a file with no tag and
    no ``label``, so every sweep given ``--label`` tags exactly as it did. One
    open reads both fields. The line decides the file only when it names
    exactly one registered label: two is a line this tier cannot settle, and
    the file is asked of the catalogues rather than given either genre.
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
        return _Labelled(label_genre(typed), own, NAMED_BY_FOLDER)
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
) -> TagResult:
    """Tag ONE file, or report why it was passed over. The per item work.

    FILL IF EMPTY, BY CONSTRUCTION. A file that already carries a genre is
    never overwritten, because that value is somebody's curation until ``crate
    tag retag`` decides the taxonomy calls it too coarse. The two verbs own this
    field under two different policies and this is where the first one lives.
    Its ``skipped`` is ``has-genre`` whether or not it was searched for art.

    A WRITE HAS TWO KINDS AND THE REPORT TELLS THEM APART. A tag the declared
    table produced and a word a catalogue used that nothing in the table knows
    are both written here, deliberately, since refusing the second is how a new
    genre stops entering the library at all. Only the first is a clean tag, so
    the second carries ``off_taxonomy`` up to the verb's report rather than
    counting as one of them (R-650).

    THE SEARCH IS SKIPPED ONLY WHEN A FILE HAS BOTH a genre and a picture. Art
    and genre are independent needs, so a tagged file with no picture is asked
    about, and only its art is written. ``fetch_image`` is optional so a caller
    that predates art keeps working; without it a needed picture is reported
    ``unavailable`` rather than fetched.

    A DECLINE IS NOT A FAILURE and this function never raises for one. The
    searcher raises when it could not read a catalogue at all, and that
    propagates for a file that needs its GENRE, because an item that reported
    done having learned nothing is the clean-report-over-unreadable-state cost
    the merge bar names.

    A TAGGED FILE SEARCHED ONLY FOR ITS ART DOES NOT FAIL on that refusal. Its
    genre was never needed and a missing picture is a decline, so the refusal
    becomes ``unavailable`` with the refusal's own sentence, which says the
    catalogues could not be read rather than that they lacked the track. Before
    art, this file was a clean ``has-genre`` skip. Letting the refusal through
    would fail every such file in an outage, and on a parse break, which is not
    retryable, fail it on every run.

    THE GENERAL CATALOGUE IS ASKED AFTER THE SEARCHER AND NEVER INSTEAD OF IT
    (R-796). ``published`` is handed whatever hit the searcher returned, with
    the file's ISRC tag when the file needs a genre and None when it does not,
    and answers with the hit to act on. It is optional so a caller that
    predates it keeps working. A searcher that RAISED is not offered to it: no
    record shop was read, and the general catalogue's album level answer is not
    to stand in for a Beatport nobody could ask.

    A FILE THE GENERAL CATALOGUE COULD NOT BE ASKED ABOUT IS NOT A NO-HIT. When
    nothing else explains the file, no declined word and no unread source, and
    the general catalogue's answer is ``no-isrc``, that is the skip reason.

    A REGISTERED LABEL'S GENRE IS WRITTEN BEFORE ANY SEARCH (U178). A file with
    no genre whose label ``label_genre`` answers for is given the label's word,
    and neither the searcher nor the general catalogue is asked about its genre.
    FILL IF EMPTY STILL HOLDS: a file that already carries a genre keeps it and
    is never looked up. A file of the label with no picture is still searched,
    for its art only, exactly as a tagged file with no picture is, and a
    refusal there is an ``unavailable`` picture and never a failed item. The
    genre is saved first so that refusal cannot cost it. ``label`` is the
    verb's ``--label``, the label of a file whose tag names none, as the
    name or identifier the seam resolves, and
    ``copyright_labels`` reads the label of a file that has neither off its
    copyright line (U240). Without it no line is read.

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
    tier = (
        _Labelled(None)
        if existing or label_genre is None
        else _by_label(path, label_genre, label, copyright_labels)
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
    # A FILE NEEDS ITS GENRE FROM A CATALOGUE only when it has none and its
    # label gave none. Every other file reaching this line is asked for its art.
    needs_genre = not existing and by_label is None
    artist = tags.read_tag(path, "artist") or ""
    title = tags.read_tag(path, "title") or path.stem
    try:
        hit = searcher(artist, title)
    except CratekitError as exc:
        if needs_genre and tier.copyright_labels and type(exc) is CratekitError:
            # A PLAIN REFUSAL ONLY: ``rebuilt`` keeps the job's own carried
            # types and no other, and a searcher's ``Parked`` must reach the
            # job as itself (U240's review, round two).
            # THE LINE'S LABELS RIDE ON THE REFUSAL (U240's review), because a
            # file whose item fails keeps no record, and the sweep's report is
            # where a person reads why its line did not settle it.
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
        # THE ISRC TAG IS READ ONLY FOR A FILE THE SEAM COULD BE ASKED ABOUT, one
        # that needs a genre and whose searcher gave none. None tells the seam
        # nothing is to be asked, which is a different fact from a tag that is
        # there and empty, and it spares the open on every file a record shop
        # already settled.
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
        # THE SOURCE GENRE IS WHAT SEPARATES THE TWO REASONS. A hit carrying one
        # means a catalogue answered and the taxonomy could not map its word; a
        # hit carrying none means nothing was found to map, and that is a
        # no-hit only when no catalogue went unread (R-791).
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
        # THE FLAG IS TAKEN HERE AND NOWHERE ELSE, on the one branch that put a
        # word on the file. A file that already had a genre carries a hit too,
        # because it was searched for its art, and reading that hit's flag would
        # report a word this run never wrote.
        off_taxonomy = hit.off_taxonomy
    # THE PICTURE IS EMBEDDED AFTER THE GENRE IS SAVED, so the last save a file
    # sees is the one carrying its art, whatever the genre write does to the
    # rest of the tag block.
    pictured = settled if settled is not None else _art_embedded(path, hit, fetch_image)
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
    if by_label is not None:
        # THE LABEL IS WHERE THE GENRE CAME FROM, whatever catalogue answered
        # about the picture, so the record's source is the label's and only the
        # answers say what the catalogues were asked.
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
    """Tag every audio file under ``root``. ``searcher`` is required.

    The walk plus :func:`tag_one` per file, and nothing else. Every policy
    decision lives one function down, where the job worker reaches it too.
    """
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
    "tag_folder",
    "tag_one",
]
