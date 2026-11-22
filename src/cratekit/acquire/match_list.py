"""The one internal shape every list becomes, and its three readers (U305).

Split from :mod:`cratekit.acquire.match`, which re-exports every public name.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, replace
from typing import Any

from cratekit.acquire.match_identity import (
    _DASH,
    _ORDINAL,
    Recorded,
    Why,
    _credits_in,
    _equivalent_versions,
    _head_of,
    _spellings_of,
    every_question_identity,
    fold,
    key_token,
    listed_title,
    question_identity,
    split_ambiguous,
    split_title,
    title_identity,
    version_identity,
)

# ---------------------------------------------------------------------------
# The one internal shape (R13)
# ---------------------------------------------------------------------------

#: The three list origins this unit reads. Values are stable identifiers that
#: travel in a list document, so they are never display names (R19).
TIDAL = "tidal"
SPOTIFY = "spotify"
TEXT = "text"


@dataclass(frozen=True, slots=True)
class Wanted(Recorded):
    """One track an external list asks for, in the shape everything downstream reads.

    ``ref`` is the source's own identifier and is PROVENANCE, never identity.
    Keying anything on it would make the same record from two services two
    different questions, and a person would answer both.
    """

    artist: str
    title: str
    version: str = ""
    key: str | None = None
    isrc: str | None = None
    origin: str = TEXT
    ref: str = ""
    #: THE TITLE AS THE SOURCE SPELLED IT, VERSION AND ALL. Carried rather than
    #: recomputed because the tombstone identity is a hash of a title, the other
    #: side of that hash reads a library row's Title column verbatim, and a title
    #: this module took apart and put back together is a different string. A
    #: source that split the title from the version has the two put back together
    #: by the reader, from the row's OWN title, so a featured credit the row
    #: spelled survives into every address composed from it. Empty only for a
    #: ``Wanted`` built by hand, where :attr:`listed` composes the fallback.
    spelled: str = ""
    #: THE OTHER WAY THIS LISTING'S TITLE READS, as (title, version), when its
    #: dash tail is a bare one-word qualifier and the string alone cannot say
    #: whether that is a version or the end of a title. ``None`` when the title
    #: has only one reading, which is almost every title. See
    #: :func:`split_ambiguous` and :attr:`readings`.
    other_reading: tuple[str, str] | None = None
    #: WHETHER THE ROW BILLED MORE THAN ONE ARTIST. :attr:`artist` keeps the
    #: first and drops the rest, and a provider that lists a guest beside the
    #: main artist has credited them without a word of it reaching the title.
    #: Read only by :attr:`uncredited_spellings`, which must not take a title
    #: with no bracketed credit as a listing that credited nobody.
    several_artists: bool = False

    def folded_row(self) -> dict[str, str]:
        """The three fields a review question about this row is addressed by.

        The ones the exact test compares, so one line typed into two lists is
        one question. The title is its :func:`title_identity`, the fold for
        every title that folds to something, so two titles of emoji alone by
        one artist are two questions.
        """
        return {
            "artist": fold(self.artist),
            "title": title_identity(self.title),
            "version": self.version_key,
        }

    @property
    def key_key(self) -> str:
        return key_token(self.key)

    @property
    def listed(self) -> str:
        """The title this track is ADDRESSED BY, which is the one it arrived as.

        THE SEAM, and getting it wrong is invisible from either side alone. The
        deletion pass hashes a library row's Title column verbatim. Round one of
        this file hashed a title that had been split and recomposed into round
        parentheses, so the two sides agreed only when the row happened to use
        that one spelling out of the several a row really uses. Four other
        spellings of one version missed, including the dash form this module
        learned to parse, and a miss is silent on both sides: nothing knows a
        tombstone exists, so nothing reports one.

        Composition is the fallback and not the rule, and where it happens moved.
        A reader that is handed a version in its own field composes at the point
        it still has the row's own title, credits included; this fallback is what
        is left for a ``Wanted`` somebody built by hand, and it composes from
        :attr:`title`, which has had its credits taken off. See :func:`_from_row`
        for what that costs when it is the only composition there is.
        """
        return self.spelled or listed_title(self.title, self.version)

    @property
    def identity(self) -> dict[str, str]:
        """THE TOMBSTONE identity (R36), which is U24's and not this module's."""
        return version_identity(artist=self.artist, title=self.listed)

    @property
    def readings(self) -> tuple[Wanted, ...]:
        """This listing, and the other way its title reads. Conservative first.

        One entry for a title with one reading. Two when the dash tail is a bare
        one-word qualifier, which no rule over the string can resolve: see
        :func:`split_ambiguous`. The second entry carries the SAME spelled
        string, because the address a deletion recorded is what the row said and
        does not change with how this module reads it.

        ONE CONSUMER, :func:`_other_reading_the_library_holds`, and it uses the
        second entry to decide what to OFFER with a question. Nothing identifying
        is derived from it: not the match identifier, not the review item, and
        since this round not an address either. See :attr:`addresses` for why the
        last of those had to go.
        """
        if self.other_reading is None:
            return (self,)
        title, version = self.other_reading
        return (
            self,
            replace(self, title=title, version=version, other_reading=None),
        )

    @property
    def addresses(self) -> tuple[str, ...]:
        """Every TITLE STRING a library row could carry for this exact version.

        Built from the spelling's own head rather than from the matching title,
        for the reason :func:`_head_of` gives.

        THE READING THE LIST SPELLED, AND NOT THE OTHER ONE, which is the same
        policy :func:`_spellings_of` applies to the same ambiguity and the two
        were pointing in opposite directions. That function refuses to compose
        ``Sun Path - Live`` from a head and a version, argued out loud, because a
        deletion of a composition genuinely called "Sun Path - Live" would then
        silently withhold the live cut. This walked both readings, so a list line
        spelling ``Aurora Bloom - Sun Path - Live`` composed ``Sun Path (Live)``
        and ``Sun Path [Live]`` and a deletion of the live cut silently withheld
        a listing that may well mean the composition. Same cost, opposite
        direction, one ambiguity. :func:`tombstone_fold` settles which way both go:
        a missed suppression re-acquires something and REPORTS it, an over-eager
        one withholds music somebody wants and says nothing, and those two costs
        are not comparable. So an undecidable reading never crosses into an
        address, in either direction, and the residual is a dash-spelled listing
        re-acquiring a version deleted under its bracketed spelling.

        THE CREDIT IS A PRECONDITION OF COMPOSING AT ALL, and until this round it
        was a sentence in a docstring while the code did the opposite for three
        real shapes. ``_head_of`` locates the version as a bracketed SUFFIX, so a
        listing that put its credit after the version, ``Sun Path (Live) (feat.
        Mira)``, or split the version over several groups, ``Sun Path (feat.
        Mira) (Extended) (Remastered)``, fell back to the matching title, which
        has had its credits taken off. Every address then composed was the PLAIN
        record's, so deleting the plain ``Sun Path (Live)`` silently withheld the
        credited recording somebody had asked for, in none of the three arrays,
        at exit zero. That is the over-eager suppression :func:`tombstone_fold`
        rejects by name, and it is the more expensive of the two costs.

        So the fallback is checked rather than trusted: composition happens only
        when the head still carries every credit the listing spelled. When it
        does not, the listing is addressed by exactly what it said and by nothing
        else, which costs a missed suppression that gets reported.
        """
        found: list[str] = []
        spelled = self.listed
        head = _head_of(spelled, self.version) or self.title
        composed: tuple[str, ...] = ()
        if _credits_in(head) == _credits_in(spelled):
            composed = tuple(
                built
                for text in _equivalent_versions(self.version)
                for built in _spellings_of(head, text)
            )
        for spelling in (spelled, *composed):
            if spelling not in found:
                found.append(spelling)
        return tuple(found)

    @property
    def suppression_spellings(self) -> tuple[dict[str, str], ...]:
        """Every identity one version of this recording could have been recorded under.

        CONSULTING IS NOT RECORDING, and the two get different rules. A recorder
        must write one identity, or one deletion becomes several records; a
        consulter that asks under one spelling and misses re-acquires a track
        somebody deleted on purpose, with nothing raised anywhere. So the store
        is asked under the spelling this list used AND under every other spelling
        a library row carries for the same version: the three bracket and dash
        conventions, the multi-group form, and the null qualifiers
        :data:`_NULL_VERSIONS` already declares equal to no qualifier at all.

        A PROVIDER ROW USED TO REACH EXACTLY ONE OF THEM. Its version arrives in
        its own field, so ``spelled`` is empty, and the set collapsed to the
        single parenthesised composition; a tombstone written from ``Sun Path -
        Nightwave Remix`` or ``Sun Path [Nightwave Remix]`` was invisible to it
        and the track was re-acquired at exit zero.

        This does NOT loosen KTD16. Every spelling here names the SAME version of
        the same recording, so no lookup can cross a version boundary and a
        tombstone over one remix can still never suppress another. What it will
        not do is widen INWARDS: nothing composed here drops a featured credit
        the listing spelled, because that would let a deletion of the plain
        record withhold the credited one. That sentence was an assertion for
        three rounds and is a checked precondition now: see :attr:`addresses`.
        """
        seen: list[dict[str, str]] = []
        for title in self.addresses:
            built = version_identity(artist=self.artist, title=title)
            if built not in seen:
                seen.append(built)
        return tuple(seen)

    @property
    def uncredited_spellings(self) -> tuple[dict[str, str], ...]:
        """The identities to ask the COMPANION kind under, which is often none.

        THE SHAPE :attr:`suppression_spellings` CANNOT REACH, CLOSED FROM THE
        OTHER SIDE. The residual titled "A deleted track the tombstone consult
        cannot reach is listed for download" is the record of what it cost while
        it was open. A provider carrying its version in its own field
        spells ``Sun Path`` and ``Nightwave Remix``. The library row somebody
        deleted read ``Sun Path (feat. Mira) (Nightwave Remix)``, the tombstone
        is addressed by that string, and nothing here can compose a guest it was
        never handed. It reported missing, ``intake missing`` listed it, and the
        next download fetched back a file a person had removed. So the deletion
        pass records a companion with the credit groups out, under
        :data:`UNCREDITED_KIND`, and this is what asks for it.

        ONLY A LISTING THAT SPELLED NO CREDIT ASKS AT ALL, and that is the guard
        rather than a saving. A listing crediting Zed that asked here would be
        withheld by a deletion of the recording that credits Mira, which is the
        over eager direction :func:`tombstone_fold` rejects by name. A listing
        that spelled its credit reaches its own tombstone verbatim through
        :attr:`suppression_spellings` and needs nothing from this.

        "SPELLED NO CREDIT" HAS TO BE SOMETHING THIS OBJECT SAW, and there are
        two ways it can fail to have seen one. A ``Wanted`` built by hand carries
        no :attr:`spelled` at all: the verb builds one from a HELD FILE, whose
        title the index has already taken the credits off, so an empty answer
        there means nobody looked and not that nobody was credited. And a
        provider row that bills a guest in its ARTISTS list has credited them
        with nothing in the title to show it, which :attr:`several_artists`
        carries. Neither asks. Each costs a missed suppression that is reported.

        IT WIDENS NOTHING THE ENGINE DID NOT ALREADY CALL ONE VERSION. A credit
        names a performer and comes off the matching title, so this listing
        resolves OWNED against that credited row while the row is held.
        ``test_the_companion_reaches_exactly_what_ownership_reached`` drives
        both halves, so the sentence is a measurement. And a deletion of the
        PLAIN record writes no companion, so it can never withhold the credited
        one from here.

        The same spellings, because the companion kept whatever bracket shape
        the row used and only lost its credits.
        """
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
            return ()
        return self.suppression_spellings

    def question(self, why: Why) -> dict[str, str]:
        """THE REVIEW ITEM identity, which is this module's.

        Separate from :attr:`identity` because they address different things: a
        tombstone outlives every list and a question is one thing somebody was
        asked. See :func:`question_identity` for why the key is in it.

        ONE ARGUMENT, AND IT IS WHICH QUESTION THIS IS, not what the library
        holds. The argument it used to take was ``about_the_key``, a boolean the
        LIBRARY set on a field of the resolved row, and an identity a machine's
        disk gets a vote in is not an identity. Deleting it took the question
        with it and collapsed the key question onto the version question, so the
        replacement is the WHY, which names the question rather than the disk:
        every VALUE here is still read off ``self``, which is the list line and
        nothing else. :func:`question_shape` argues both halves.
        """
        return question_identity(self.artist, self.title, self.version, self.key, why)

    def questions(self) -> tuple[dict[str, str], ...]:
        """Every identity this line can have been asked under, one per shape.

        For the row that is no longer a question: resolution owned it, and the
        items an earlier run filed about it are retired through these. See
        :func:`every_question_identity`.
        """
        return every_question_identity(self.artist, self.title, self.version, self.key)


def _field(row: object, name: str, default: Any = None) -> Any:
    """Read ``name`` from a mapping or from an object attribute.

    Both, because the same reader has to serve a list document that was written
    to disk and a provider client's live track objects. Supporting only the
    first would make the intake verbs convert every object before calling this,
    which is a second normalization step and therefore a second place for the
    shapes to disagree.
    """
    if isinstance(row, Mapping):
        value = row.get(name, default)
    else:
        value = getattr(row, name, default)
    return default if value is None else value


def row_isrc(row: object) -> Any:
    """The ISRC a provider row carries, as the row spelled it, or None.

    From the row itself, else from its ``external_ids``, which is where a
    public playlist row keeps it. PUBLIC, because the label genre gate asks a
    general catalogue by this value and must find it wherever this module's
    own reader would: a second reader that knew one of the two places
    would call a release unaskable while its rows carried the identifier.
    """
    external = _field(row, "external_ids", {})
    return _field(row, "isrc") or (_field(external, "isrc") if external else None)


def _first_named(entries: object) -> str:
    """The first non-empty name in a list of artists, whatever they are made of.

    A BARE STRING IS A LIST OF ONE. Two rows spelling their artists
    ``{"artists": "Aurora Bloom"}`` and ``{"artists": "Nova Reef"}`` both read as
    no artist at all, so both hashed to an identity carrying only the title and
    both landed on the same identifier for two different recordings. It is not
    split on a comma: a comma is legal inside an artist's own name, and guessing
    where one artist ends is the wrong-join risk this module exists to remove.
    """
    if isinstance(entries, str):
        return entries.strip()
    if not isinstance(entries, (list, tuple)):
        return ""
    for entry in entries:
        if isinstance(entry, str) and entry.strip():
            return entry.strip()
        name = _field(entry, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return ""


def _bills_several(row: object) -> bool:
    """Whether a provider row names more than one artist, under either field.

    Counted the way :func:`_first_named` reads, a string or a mapping or an
    object with a name, so the two cannot disagree about what an entry is. A
    bare string is a list of one and is never split, for the reason given there.
    """
    for field_name in ("artist", "artists"):
        entries = _field(row, field_name)
        if not isinstance(entries, (list, tuple)):
            continue
        named = [entry for entry in entries if _first_named([entry])]
        if len(named) > 1:
            return True
    return False


def _artist_of(row: object) -> str:
    """The primary artist, from whichever of the four shapes a provider used.

    THE LIST UNDER ``artist`` IS THE ONE THAT WAS MISSING, and it read as no
    artist at all rather than as a shape this reader does not know. A row
    spelling its artists ``{"artist": ["Two", "Names"]}`` produced an empty
    artist, hashed to an identity matching nothing, and reported a track the
    library plainly held as missing with no warning and exit zero, right beside
    the ``{"artists": [...]}`` spelling of the same track landing matched. A
    list is read here exactly as a list under ``artists`` is read, first entry
    first, because two spellings of one shape must not be two answers.

    THE BARE STRING UNDER ``artists`` WAS MISSING FOR THE SAME REASON and cost
    more, because it silently failed to read an artist that was RIGHT THERE. Two
    rows carrying ``{"name": "Sun Path", "artists": "Aurora Bloom"}`` and
    ``{"name": "Sun Path", "artists": "Nova Reef"}`` both produced an empty
    artist and therefore one identity for two different recordings. See
    :func:`_first_named`.
    """
    single = _field(row, "artist")
    if isinstance(single, str) and single.strip():
        return single.strip()
    if isinstance(single, (list, tuple)):
        return _first_named(single) or _first_named(_field(row, "artists", ()))
    if single is not None:
        name = _field(single, "name", "")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return _first_named(_field(row, "artists", ()))


def read_tidal_tracks(rows: Iterable[object]) -> tuple[Wanted, ...]:
    """Provider playlist rows, where the version is its OWN field.

    This is the shape that makes the three readers worth having. The provider
    carries "Someone Remix" beside the title; the public playlist API below
    carries it inside the title; pasted text carries it inside the title too.
    All three fold to one version token, so all three ask one question.
    """
    return tuple(
        _from_row(row, origin=TIDAL, position=position)
        for position, row in enumerate(rows, start=1)
    )


def read_spotify_items(items: Iterable[object]) -> tuple[Wanted, ...]:
    """Public playlist items, each of which wraps the track it holds.

    A row that is already a track is accepted too. The wrapper is what the
    playlist endpoint returns and the bare track is what the tracks endpoint
    returns, and refusing one of them would put the choice of endpoint into this
    module's contract.
    """
    found: list[Wanted] = []
    for position, item in enumerate(items, start=1):
        inner = _field(item, "track")
        found.append(
            _from_row(
                inner if inner is not None else item, origin=SPOTIFY, position=position
            )
        )
    return tuple(found)


def read_text_lines(text: str, *, allow_empty: bool = False) -> tuple[Wanted, ...]:
    """Pasted "Artist - Title" lines. Blank lines and ``#`` comments are skipped.

    A line that carries no separator is REFUSED rather than read as a title with
    no artist. A tracklist with one malformed line is far more often a tracklist
    somebody pasted wrong than a record by nobody, and reading it as anonymous
    would put a track in the queue that no source can ever match.

    A file with NO readable line in it at all is refused for the same reason the
    document reader refuses a newer format: reading it anyway reports a clean
    match over nothing, and "every track on your list is owned" and "your list
    was empty" are the same three empty arrays and the same exit zero.
    ``allow_empty`` is for the one caller that has a positive declaration to go
    on, a list document whose ``tracks`` array is present and empty.
    """
    found: list[Wanted] = []
    for number, raw in enumerate(str(text).splitlines(), start=1):
        line = _ORDINAL.sub("", raw).strip()
        if not line or line.startswith("#"):
            continue
        found.append(_line(line, raw=raw, number=number))
    if not found and not allow_empty:
        raise UnreadableList(
            "this list holds no track lines at all; a blank list and a list whose "
            "every track is owned produce the same empty result and the same "
            "exit status, so it is refused rather than reported clean"
        )
    return tuple(found)


def read_text_rows(rows: Iterable[object], *, allow_empty: bool = True) -> tuple[Wanted, ...]:
    """A list document's ``tracks`` array, where each entry is ONE line.

    Read entry by entry rather than joined into one blob and re-split. The join
    put three defects in one line of code: a refusal named a line number in a
    string nobody has, a row that happened to carry a newline silently became two
    tracks, and the array's length stopped being the number of tracks read.

    Blank and ``#`` rows are still skipped, and that is deliberate rather than
    an oversight: a document written from a pasted tracklist carries the pasted
    lines verbatim, comments included, and the two spellings of one list have to
    read the same. What is NOT allowed is a row hiding a second track inside it.
    """
    found: list[Wanted] = []
    for position, raw in enumerate(rows, start=1):
        text = str(raw)
        if "\n" in text or "\r" in text:
            raise UnreadableList(
                f"track {position} carries a line break, so one entry in the "
                f"array would become two tracks and the list would be longer "
                f"than it declares",
                line=position,
            )
        line = _ORDINAL.sub("", text).strip()
        if not line or line.startswith("#"):
            continue
        found.append(_line(line, raw=text, number=position))
    if not found and not allow_empty:
        raise UnreadableList("this list holds no track lines at all")
    return tuple(found)


def _line(line: str, *, raw: str, number: int) -> Wanted:
    artist, separator, title = line.partition(_DASH)
    if not separator or not artist.strip() or not title.strip():
        raise UnreadableList(
            f"line {number} is not an 'Artist - Title' line: {raw.strip()!r}",
            line=number,
        )
    return _from_row(
        {"artist": artist, "title": title}, origin=TEXT, position=number
    )


#: Origin to the reader that speaks it. A list document names its origin and the
#: reader is looked up here, so adding a fourth source is one entry plus one
#: reader rather than a branch somebody has to find.
READERS: Mapping[str, Callable[[Iterable[object]], tuple[Wanted, ...]]] = {
    TIDAL: read_tidal_tracks,
    SPOTIFY: read_spotify_items,
}


def _from_row(row: object, *, origin: str, position: int) -> Wanted:
    """One row, POSITIVELY recognized or refused.

    BOTH HALVES ARE REQUIRED, and demanding only one of them was the same defect
    wearing a weaker rule. ``read_text_lines`` refuses a line with no artist by
    name, and this path accepted one: an artist-less row keeps its title, and a
    title alone is not unique to the recording it names. Two rows reading "Sun
    Path" by two different artists then carried ONE match identifier, both
    resolved matched against one unrelated file whose own artist tag was absent,
    and one of the two vanished from any payload a consumer keys by id, at exit
    zero, with no warning and no question.

    Three more things went wrong with no guard at all: two rows carrying nothing
    but an identifier folded to one match identifier; an unreadable row matched
    any junk file in the library whose name folded to nothing and was reported
    owned; and a row whose artists arrived in a shape this reader did not know
    reported a held track missing.
    """
    raw_title = _raw_title(row)
    declared = str(_field(row, "version", "")).strip()
    title, embedded = split_title(raw_title)
    isrc = row_isrc(row)
    artist = _artist_of(row)
    if not artist or not title:
        absent = "artist" if title else "title"
        raise UnreadableList(
            f"track {position} names no {absent}, and the half that is left is "
            f"not unique to the recording it means: it matches any file in the "
            f"library agreeing on that half, and two rows differing only in the "
            f"missing one are a single identifier",
            line=position,
        )
    return Wanted(
        artist=artist,
        title=title,
        version=declared or embedded,
        key=(str(_field(row, "key", "")).strip() or None),
        isrc=(str(isrc).strip() or None) if isrc else None,
        origin=origin,
        ref=str(_field(row, "id", "")).strip(),
        # THE ROW'S OWN TITLE, WITH ITS VERSION IN IT. A row that spelled the two
        # together is addressed by exactly what it said. A row that declared its
        # version in a separate field never spelled them together, so the two are
        # composed HERE, FROM THE ROW'S TITLE rather than from the matching one,
        # and that word is the whole of the correction. The matching title has
        # had its featured credits taken off, because a guest vocalist names a
        # performer rather than an edit, so composing the address from it turned
        # a provider row for ``Sun Path (feat. Mira)`` into every address of the
        # PLAIN record: a tombstone over the literal library row ``Sun Path
        # (Extended) (Remastered)`` then suppressed a listing for the credited
        # recording, in none of the three arrays, at exit zero, with acquisition
        # skipping a track nobody had deleted. ``Wanted.addresses`` cannot catch
        # that, because by the time it compares the credits the composition has
        # already dropped it and the comparison is vacuous on both sides.
        spelled=listed_title(raw_title, declared) if declared else raw_title,
        # ONLY WHEN THE ROW SPELLED THE TWO TOGETHER. A declared version leaves
        # nothing ambiguous, because the source already said which part is the
        # version.
        other_reading=None if declared else split_ambiguous(raw_title),
        several_artists=_bills_several(row),
    )


def _raw_title(row: object) -> str:
    """The title one provider row spells, its version and brackets still in it."""
    return str(_field(row, "title", "") or _field(row, "name", "")).strip()


def listed_names(row: object) -> tuple[str, str, str]:
    """The provider id, the artist and the title as one row lists them (U213).

    Read the way :func:`read_row` reads them, for naming a row it REFUSED: a
    caller that plans many playlists sets that one track aside by its id and
    says which it was, rather than refusing every playlist over it. The title
    is the row's own spelling, unsplit, since a refused row has no reading.
    """
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)


def read_row(row: object, *, origin: str, position: int) -> Wanted:
    """ONE provider shaped row as a ``Wanted``, for a reader outside this module.

    The recognition identifier receives a hit in exactly the shape a provider
    row has, a mapping with a title, a list of artists and an ISRC under
    ``external_ids``, and reading it here rather than in a second reader is
    what keeps a recognised track and the same track pasted in a tracklist
    folding to one identity: every rule the readers learned about artists,
    versions, spellings and ambiguous titles applies to both or to neither.
    Raises :class:`UnreadableList` for a row naming no artist or no title.
    """
    return _from_row(row, origin=origin, position=position)


class UnreadableList(ValueError):
    """A pasted tracklist carries a line this reader will not guess at.

    A plain exception rather than a structured cause, because this module sits
    below the layer that owns the failure vocabulary. The verb converts it, in
    the one place that is allowed to know what a remediation looks like.
    """

    def __init__(self, message: str, *, line: int | None = None) -> None:
        super().__init__(message)
        self.line = line
