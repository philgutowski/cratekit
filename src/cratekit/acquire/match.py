"""Three-state matching (U16): each list line resolves to matched, needs review
or missing, and a version difference is never silently treated as matched.

Four properties hold:

1. **Ownership is on-disk truth.** The index walks the music tree, reading each
   file's tags and falling back to its filename, never an export, because an
   export can lag the disk.
2. **A fuzzy hit is discovery, never identity.** Every approximate hit resolves
   to needs review with the difference named, so a generous score costs one
   question rather than one wrong join.
3. **A version is part of the identity.** Two records agreeing on the recording
   and disagreeing on the version are a question that names what differs.
4. **One internal shape.** Every reader produces a ``Wanted``, so a list gives
   the same match and the same review item identity from any source. That
   identity is a function of the list line and of which question is asked, never
   of the library, so it is the same on every machine (:func:`question_shape`,
   and the residual titled "A question answered on one machine does not settle a
   different question about the same line"). A one-word dash tail the string
   cannot settle is carried both ways and resolves to needs review
   (:func:`split_ambiguous`, and the residual titled "The one-word dash class
   cannot converge on state across the three readers").

Suppression is not a fourth payload array. A tombstoned version (R36) is
reported on its own channel and sits in none of the three arrays, so nothing
reading ``missing`` fetches it. It is decided last, after every question about
the library, because the disk wins over a stale tombstone and a tombstone
governs what is fetched, not what a person is asked. Nothing here opens a
socket; fetching belongs to the intake verbs.

This module holds the candidates, resolution and the verdict's application, and
re-exports what :mod:`cratekit.acquire.match_identity`,
:mod:`cratekit.acquire.match_list` and :mod:`cratekit.acquire.match_library` hold.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter
from typing import Any

from cratekit.acquire.match_identity import (
    ASKS_ABOUT_KEY,
    ASKS_ABOUT_READING,
    ASKS_ABOUT_RECORDING,
    ASKS_ABOUT_VERSION,
    DIGEST_WIDTH,
    KEY_QUESTIONS,
    OWNING_RULES,
    PAYLOAD_STATES,
    QUESTION_KIND,
    QUESTION_SHAPES,
    TOMBSTONE_KIND,
    UNCREDITED_KIND,
    VERSION_WORDS,
    MatchState,
    Why,
    _digest,
    _sorted_words,
    bare_title,
    credited_members,
    digest,
    every_question_identity,
    fold,
    fold_isrc,
    isrc_token,
    key_token,
    listed_title,
    question_identity,
    question_shape,
    recording_identity,
    recording_token,
    same_title,
    split_ambiguous,
    split_title,
    split_version,
    title_identity,
    tombstone_fold,
    version_identity,
    version_token,
)
from cratekit.acquire.match_library import (
    LibraryIndex,
    Owned,
    _spelled_out,
    index_library,
    index_paths,
    remembered,
    reset_cache,
)
from cratekit.acquire.match_list import (
    READERS,
    SPOTIFY,
    TEXT,
    TIDAL,
    UnreadableList,
    Wanted,
    listed_names,
    read_row,
    read_spotify_items,
    read_text_lines,
    read_text_rows,
    read_tidal_tracks,
    row_isrc,
)
from cratekit.core import naming

#: The score at or above which an approximate recording hit is worth showing a
#: person. Generous on purpose: nothing above it becomes a match, only a question
#: unless its title falls under :data:`APPROXIMATE_TITLE_FLOOR` (U286), so a low
#: floor costs queue noise and a high one reports missing a track the library
#: holds under another spelling. Lowering it is a product change, priced in the
#: residual titled "The ambiguous reading class is queued as a question and does
#: not gate the run".
APPROXIMATE_FLOOR = 82

#: How many approximate candidates are offered for one wanted track: choosing
#: among five is choosing, among forty is scrolling. Spent twice, as the number
#: of recordings :func:`_resembling` keeps after the title test (U286), and as a
#: truncation of the candidate list, because one recording can be held as
#: several versions at several keys. Spelled out lookup hits ride on top of the
#: five (card 833).
APPROXIMATE_LIMIT = 5

#: The score the title alone must reach, by ``token_set_ratio``, for a discovery
#: hit to be offered (U286). The discovery score reads artist and title together,
#: so a shared artist carries an unrelated short title over
#: :data:`APPROXIMATE_FLOOR`; the artist agreeing is necessary, never sufficient.
#: 66 is the highest integer floor keeping every one letter change of a three
#: letter title (66.67), while the unrelated pairs measured score at most 61.5.
APPROXIMATE_TITLE_FLOOR = 66



# ---------------------------------------------------------------------------
# Keys: the relative major and minor trap
# ---------------------------------------------------------------------------


def key_disagreement(wanted: str | None, owned: str | None) -> Why | None:
    """How two Camelot codes disagree, or None when there is nothing to say.

    Absence is not disagreement, or most of a real playlist would be queued. The
    relative case, 8A against 8B, gets its own answer because it shares a wheel
    position and looks like agreement while being a minor and a major recording.
    """
    if not wanted or not owned:
        return None
    left = naming.parse_camelot(wanted)
    right = naming.parse_camelot(owned)
    if left is None or right is None:
        return None
    if left == right:
        return None
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS


# ---------------------------------------------------------------------------
# One resolved track
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Candidate:
    """One owned version offered as the answer to a version question.

    Addressed by recording, version and key, not by file, so two copies of one
    version at one key are one candidate with two paths and a rename orphans no
    decision. The key is in the grouping because it is shown. Artist and title
    travel with it because an approximate hit offers a different recording.
    """

    candidate_id: str
    artist: str
    title: str
    version: str
    key: str | None
    difference: Why
    paths: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.candidate_id, "artist": self.artist, "title": self.title,
            "version": self.version, "key": self.key, "difference": str(self.difference),
            "paths": list(self.paths),
        }


#: How a source is asked for a version this library does not hold. Identifiers,
#: because the next verb switches on them.
BY_ISRC = "isrc"
BY_SEARCH = "search"


@dataclass(frozen=True, slots=True)
class Acquisition:
    """One way to go and get a missing version. Data on the row, not a question.

    Whether a missing track is also a review item is the residual titled "Two
    briefs disagree about whether a missing track is a review item". Two shapes,
    because a provider holding the ISRC need not guess and one without needs
    text; both name the exact version asked for, never some other cut.
    """

    option_id: str
    how: str
    query: str
    artist: str
    title: str
    version: str
    isrc: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.option_id, "how": self.how, "query": self.query, "artist": self.artist,
            "title": self.title, "version": self.version, "isrc": self.isrc,
        }


def acquisition_options(wanted: Wanted) -> tuple[Acquisition, ...]:
    """What a source can be asked for, most precise first."""
    built: list[Acquisition] = []
    if wanted.isrc:
        built.append(
            Acquisition(
                option_id=f"aq_{_digest(BY_ISRC, wanted.isrc)}", how=BY_ISRC, query=wanted.isrc,
                artist=wanted.artist, title=wanted.title, version=wanted.version, isrc=wanted.isrc,
            )
        )
    built.append(
        Acquisition(
            option_id=f"aq_{_digest(BY_SEARCH, wanted.distinct, wanted.version_key)}",
            how=BY_SEARCH,
            query=f"{wanted.artist} {wanted.listed}".strip(),
            artist=wanted.artist,
            title=wanted.title,
            version=wanted.version,
        )
    )
    return tuple(built)


#: The whys that mean a stored verdict could not be applied. The item is resolved
#: in the queue, so ``review list`` hides it and ``review resolve`` refuses it;
#: the verb names ``review clear``, the remedy that works.
STALLED: frozenset[Why] = frozenset({Why.CANDIDATE_GONE, Why.VERDICT_UNSPECIFIC})


@dataclass(frozen=True, slots=True)
class TrackMatch:
    """One wanted track, the state it resolved to, and why.

    ``match_id`` derives from the recording, the version and the key alone, so the
    same list from three sources gives the same rows; the key is in it because it
    is in the state. The provider's reference travels under ``wanted``.
    """

    wanted: Wanted
    state: MatchState
    why: Why
    candidates: tuple[Candidate, ...] = ()
    paths: tuple[str, ...] = ()
    item_id: str | None = None
    suppression_id: str | None = None
    acquisitions: tuple[Acquisition, ...] = ()
    #: Candidates the offer limit kept back. Reported rather than dropped, so a
    #: rejection is a rejection of what was shown and everybody knows it.
    withheld: int = 0

    @property
    def match_id(self) -> str:
        return (
            f"mt_{_digest(self.wanted.distinct, self.wanted.version_key, self.wanted.key_key)}"
        )

    @property
    def identity(self) -> dict[str, str]:
        """THE TOMBSTONE identity (R36). See :func:`version_identity`."""
        return self.wanted.identity

    @property
    def question_identity(self) -> dict[str, str]:
        """The review item identity: the list line, and which question was asked.

        Every value is read off ``wanted``, never off this machine's library, so
        one line opens one item on every machine, which ``review export`` and
        ``review import`` need. ``why`` picks one of four shapes
        (:func:`question_shape`); an answer crossing between the two key whys is
        caught in :func:`apply_verdict`. Refuses on a row that is not a question.
        """
        return self.wanted.question(self.why)

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.match_id,
            "state": str(self.state),
            "why": str(self.why),
            "artist": self.wanted.artist,
            "title": self.wanted.title,
            "version": self.wanted.version,
            "key": self.wanted.key,
            "isrc": self.wanted.isrc,
            "candidates": [candidate.to_json() for candidate in self.candidates],
            "candidates_withheld": self.withheld,
            "acquisition": [option.to_json() for option in self.acquisitions],
            "paths": list(self.paths),
            "review_item": self.item_id,
            "suppression": self.suppression_id,
            # Provenance, the only key that may differ between two services.
            "source": {"origin": self.wanted.origin, "ref": self.wanted.ref},
        }


@dataclass(frozen=True, slots=True)
class MatchResult:
    """Every track in one list, resolved.

    The payload derives from ``PAYLOAD_STATES``, so its arrays cannot fall out of
    step with the states.
    """

    matches: tuple[TrackMatch, ...]

    def __len__(self) -> int:
        return len(self.matches)

    def of(self, state: MatchState) -> tuple[TrackMatch, ...]:
        return tuple(found for found in self.matches if found.state is state)

    @property
    def suppressed(self) -> tuple[TrackMatch, ...]:
        return self.of(MatchState.SUPPRESSED)

    def payload(self) -> dict[str, list[dict[str, Any]]]:
        return {
            str(state): [found.to_json() for found in self.of(state)]
            for state in PAYLOAD_STATES
        }


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


def _candidates_for(wanted: Wanted, owned: Sequence[Owned]) -> tuple[Candidate, ...]:
    """Group owned files into one candidate per recording, version and key,
    naming what differs.

    By recording so different recordings never share a candidate, read by its
    identity so two titles folding to nothing stay apart, and by key because a
    candidate shows one key.
    """
    grouped: dict[tuple[str, str, str], list[Owned]] = {}
    for held in owned:
        grouped.setdefault((held.distinct, held.version_key, held.key_key), []).append(held)
    built: list[Candidate] = []
    token = isrc_token(wanted.isrc)
    # Insertion order, not sorted: the approximate pass hands rows best score
    # first, and the offer limit must drop the worst.
    for recording, version_key, key in grouped:
        rows = grouped[(recording, version_key, key)]
        first = rows[0]
        if not _same_recording(wanted, first, token):
            difference = Why.TITLE_APPROXIMATE
        elif version_key != wanted.version_key and not _carries(first, token):
            # An ISRC settles the version too, so only the key is left to ask.
            difference = Why.VERSION_DIFFERS
        else:
            difference = key_disagreement(wanted.key, key) or Why.EXACT
        built.append(
            Candidate(
                candidate_id=f"cd_{_digest(recording, version_key, key)}",
                artist=first.artist,
                title=first.title,
                version=first.version,
                # The folded key, since one value stands for every path here.
                key=key or None,
                difference=difference,
                paths=tuple(str(row.path) for row in rows),
            )
        )
    return tuple(built)


def _carries(held: Owned, token: str) -> bool:
    """Whether ``held`` carries this ISRC. Empty carries nothing."""
    return bool(token) and held.isrc == token


def _same_recording(wanted: Wanted, held: Owned, token: str) -> bool:
    """Whether ``held`` is the recording ``wanted`` names under any rule
    :func:`resolve_one` applies, so a credited or ISRC hit at another version is a
    version question, not a resemblance. ``token`` is the row's folded ISRC.
    """
    if not same_title(held.title, wanted.title):
        return False
    if held.distinct == wanted.distinct:
        return True
    return fold(wanted.artist) in held.members or _carries(held, token)


def _approximate(wanted: Wanted, index: LibraryIndex, *, limit: int | None) -> tuple[Owned, ...]:
    """Recordings that merely resemble the wanted one. Discovery, never identity.

    Scored on the folded recording token, so artist and title both count, by
    ``ratio`` over words sorted once per name, which is ``token_sort_ratio``
    (U265). The scorer is imported here so ``crate --help`` does not pay for it.
    ``limit`` caps the recordings returned, ``None`` returning all over the floor.
    """
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    recordings, sorted_choices = index.sorted_recordings()
    found = process.extract(
        _sorted_words(wanted.recording),
        sorted_choices,
        scorer=fuzz.ratio,
        score_cutoff=APPROXIMATE_FLOOR,
        limit=limit,
    )
    # Best score first, ties in position order; the offer limit relies on it.
    return tuple(
        held for _sorted, _score, position in found for held in index.versions(recordings[position])
    )


def _title_resembles(wanted: Wanted, held: Owned) -> bool:
    """Whether ``held``'s title resembles the wanted one on its own (U286).

    ``token_set_ratio`` of the folded titles against
    :data:`APPROXIMATE_TITLE_FLOOR`, with three allowances, because a wrong drop
    downloads a duplicate where a wrong offer costs one question: a title folding
    to nothing is left to the discovery score, titles equal once spaces are gone
    agree (``O.K.`` and ``OK``), and a file with artist and title swapped agrees
    when each half agrees with the other side's other half.
    """
    asked, found = fold(wanted.title), fold(held.title)
    if not asked or not found:
        return True
    if _agree(asked, found):
        return True
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)


def _agree(one: str, other: str) -> bool:
    """Whether two folded names agree for :func:`_title_resembles`: equal once
    spaces are gone, as written or spelled out by :data:`_SPELLED_OUT` (card 833),
    or ``token_set_ratio`` at or over :data:`APPROXIMATE_TITLE_FLOOR`. Spelled out
    is compared by equality, never a ratio, since ``2`` read as ``to`` scores 80
    against ``Tom``. An empty side agrees with nothing here."""
    from rapidfuzz import fuzz

    if one and (
        one.replace(" ", "") == other.replace(" ", "")
        or _spelled_out(one) == _spelled_out(other)
    ):
        return True
    return fuzz.token_set_ratio(one, other) >= APPROXIMATE_TITLE_FLOOR






def _resembling(wanted: Wanted, index: LibraryIndex) -> tuple[Owned, ...]:
    """What the approximate pass offers: discovery hits whose title resembles too,
    best score first, at most :data:`APPROXIMATE_LIMIT` recordings, led by any the
    spelled out lookup finds outside those five (card 833).

    Filtered before the cap (U286), so an artist's unrelated short titles cannot
    push a real near match out. A lookup hit rides on top of the five, and the
    offer's truncation reports what it pushes out as withheld.
    """
    scored: list[Owned] = []
    recordings = 0
    for _recording, versions in groupby(
        _approximate(wanted, index, limit=None), key=attrgetter("recording")
    ):
        held = tuple(versions)
        if not _title_resembles(wanted, held[0]):
            continue
        scored.extend(held)
        recordings += 1
        if recordings == APPROXIMATE_LIMIT:
            break
    # Not among the five, not merely not scored. No title test: a lookup hit is
    # the row's title spelled out.
    offered = {held.recording for held in scored}
    looked_up = [
        held
        for recording in index.spelled_alike(wanted.recording)
        if recording not in offered
        for held in index.versions(recording)
    ]
    return tuple(looked_up + scored)


def standing_tombstone(
    wanted: Wanted, *, suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str], companions: bool = True,
) -> str | None:
    """The identifier of the tombstone standing over this version, or None.

    Asked under every spelling in :attr:`Wanted.suppression_spellings`, since a
    missed consult re-acquires something deleted on purpose. Public because the
    verb reports a tombstone that did not suppress.
    """
    for identity in wanted.suppression_spellings:
        if suppresses(TOMBSTONE_KIND, identity):
            return suppression_id(TOMBSTONE_KIND, identity)
    # The companion is asked second, so a listing both answer is reported under
    # the tombstone a person wrote. ``companions=False`` is for a caller about to
    # call the record stale: a companion cannot say which credited row it is.
    if not companions:
        return None
    for identity in wanted.uncredited_spellings:
        if suppresses(UNCREDITED_KIND, identity):
            return suppression_id(UNCREDITED_KIND, identity)
    return None


def _held_exactly(wanted: Wanted, index: LibraryIndex) -> bool:
    """Whether the library holds this recording at this version, the evidence
    that settles an ambiguous reading (:func:`split_ambiguous`)."""
    return any(
        held.version_key == wanted.version_key
        for held in index.held(wanted.artist, wanted.title)
    )


def _other_reading_the_library_holds(wanted: Wanted, index: LibraryIndex) -> Wanted | None:
    """The reading :func:`split_title` declined that the library holds exactly.

    The bar is the highest there is, because a near hit says nothing about
    whether a tail is a version. The answer picks the question and the candidate
    offered, never the parse: the caller keeps the reading the list spelled, so
    no identity depends on the disk.
    """
    for reading in wanted.readings[1:]:
        if _held_exactly(reading, index):
            return reading
    return None


def resolve_one(
    wanted: Wanted, index: LibraryIndex, *, suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> TrackMatch:
    """Resolve one wanted track against the library and the tombstones.

    ``suppresses`` has no default, since "nothing is suppressed" is the
    permissive answer a forgetful caller would get silently. Every question about
    the library comes first and the tombstones last, just before a track is
    called missing, because R36 governs what is fetched, not what is asked.
    Everything identifying derives from ``wanted`` as the reader built it, so it
    is a function of the list and not of this machine's disk.
    """
    # The ISRC first, exact and cheap: a hit settles recording and version, not
    # key. It agrees only with the title, by :func:`same_title`, so a file with
    # the row's ISRC under another title is asked about below, never owned. When
    # it settles a row, the paths are the files carrying it.
    carrying = index.held_by_isrc(isrc_token(wanted.isrc))
    settled = [held for held in carrying if same_title(held.title, wanted.title)]
    doubtful = [held for held in carrying if not same_title(held.title, wanted.title)]
    owned = index.held(wanted.artist, wanted.title)
    if settled:
        exact, agreed = settled, Why.ISRC_EXACT
    else:
        exact = [held for held in owned if held.version_key == wanted.version_key]
        agreed = (
            Why.EXACT
            if any(held.recording == wanted.recording for held in exact)
            else Why.CREDITED_EXACT
        )

    if exact:
        # Every held copy, not the first the walk returned, so the state never
        # depends on directory order.
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None}:
            return TrackMatch(
                wanted=wanted, state=MatchState.MATCHED, why=agreed,
                paths=tuple(str(held.path) for held in exact),
            )
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            # The relative case wins, as the one that looks like agreement.
            why=Why.KEY_RELATIVE if Why.KEY_RELATIVE in disagreements else Why.KEY_DIFFERS,
            candidates=_candidates_for(wanted, exact),
        )

    if owned:
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,
            candidates=_candidates_for(wanted, owned),
        )

    if doubtful:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
        return TrackMatch(
            wanted=wanted, state=MatchState.NEEDS_REVIEW, why=Why.TITLE_APPROXIMATE,
            candidates=_candidates_for(wanted, doubtful),
        )

    # The other reading, asked about rather than assumed: after the branches above
    # so a tie goes to the string the list spelled, before the approximate pass
    # so the question is a precise one.
    confirming = _other_reading_the_library_holds(wanted, index)
    if confirming is not None:
        # Only the files at that version, never the head's other versions.
        held = [
            row
            for row in index.held(confirming.artist, confirming.title)
            if row.version_key == confirming.version_key
        ]
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.READING_AMBIGUOUS,
            # Scored against what the list said, so the held file reads as the
            # different recording being asked about.
            candidates=_candidates_for(wanted, held),
        )

    near = _resembling(wanted, index)
    if near:
        offered = _candidates_for(wanted, near)
        return TrackMatch(
            wanted=wanted,
            state=MatchState.NEEDS_REVIEW,
            why=Why.TITLE_APPROXIMATE,
            candidates=offered[:APPROXIMATE_LIMIT],
            # Said out loud, so a rejection is of what was shown.
            withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),
        )

    standing = standing_tombstone(
        wanted, suppresses=suppresses, suppression_id=suppression_id
    )
    if standing is not None:
        return TrackMatch(
            wanted=wanted, state=MatchState.SUPPRESSED, why=Why.TOMBSTONED, suppression_id=standing,
        )

    return TrackMatch(
        wanted=wanted,
        state=MatchState.MISSING,
        why=Why.NOT_IN_LIBRARY,
        acquisitions=acquisition_options(wanted),
    )


def resolve_all(
    wanted: Sequence[Wanted], index: LibraryIndex, *,
    suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> MatchResult:
    """Resolve a whole list, preserving its order inside each state."""
    return MatchResult(
        matches=tuple(
            resolve_one(
                one, index, suppresses=suppresses, suppression_id=suppression_id
            )
            for one in wanted
        )
    )


def _former_candidate_id(candidate: Candidate) -> str:
    """The identifier ``candidate`` had before titles were read by identity
    (card 834). Equal to :attr:`Candidate.candidate_id` wherever a title folds to
    something."""
    token = recording_token(candidate.artist, candidate.title)
    return f"cd_{_digest(token, version_token(candidate.version), candidate.key or '')}"


def current_option(found: TrackMatch, option: str, title: object) -> str:
    """The candidate a recorded answer names today, by its identifier and the
    title it was given about.

    ``option`` unchanged unless it names no candidate on offer and a candidate's
    :func:`_former_candidate_id` is ``option`` with a title equal by
    :func:`same_title`; then that candidate's identifier. The title keeps the old
    identifier from answering for another file under it. ``None`` carries nothing.
    """
    if title is None or any(one.candidate_id == option for one in found.candidates):
        return option
    carried = [
        one for one in found.candidates
        if _former_candidate_id(one) == option and same_title(one.title, title)
    ]
    # At most one fits: together they fix one group of :func:`_candidates_for`.
    return carried[0].candidate_id if carried else option


def apply_verdict(
    found: TrackMatch, *, accepted: bool | None, option: str | None, offered: Sequence[str],
    item_id: str, suppresses: Callable[[str, Mapping[str, Any]], bool],
    suppression_id: Callable[[str, Mapping[str, Any]], str],
) -> TrackMatch:
    """Fold a recorded decision into a track that would otherwise need review.

    ``accepted`` None, undecided or unreadable, leaves the question answerable,
    so an unknown verdict never freezes an item out of ``review clear``. A
    decision naming a candidate no longer offered is not applied, since ownership
    is on-disk truth. An acceptance naming no candidate applies only when exactly
    one is on offer and it is the one in ``offered``, the candidate shown when the
    answer was given; otherwise it stalls like a gone candidate, because both key
    whys share one item and the library can change under a settled answer. A
    rejection consults the tombstones, since it reaches missing by another road.
    """
    if accepted is None:
        return TrackMatch(
            wanted=found.wanted, state=found.state, why=found.why, candidates=found.candidates,
            paths=found.paths, item_id=item_id, withheld=found.withheld,
        )
    if not accepted:
        standing = standing_tombstone(
            found.wanted, suppresses=suppresses, suppression_id=suppression_id
        )
        if standing is not None:
            return TrackMatch(
                wanted=found.wanted, state=MatchState.SUPPRESSED, why=Why.TOMBSTONED,
                candidates=found.candidates, item_id=item_id, suppression_id=standing,
                withheld=found.withheld,
            )
        return TrackMatch(
            wanted=found.wanted,
            state=MatchState.MISSING,
            why=Why.VERDICT_REJECTED,
            candidates=found.candidates,
            item_id=item_id,
            # A rejection is a missing row, so it says what to go and get.
            acquisitions=acquisition_options(found.wanted),
            withheld=found.withheld,
        )
    if option is None:
        # The candidate the answer was about, when it was about exactly one.
        about = offered[0] if len(offered) == 1 else None
        if about is None or len(found.candidates) != 1:
            chosen = []
            unresolved = Why.VERDICT_UNSPECIFIC
        else:
            # Bound: a different candidate on offer today reads as gone.
            chosen = [c for c in found.candidates if c.candidate_id == about]
            unresolved = Why.CANDIDATE_GONE
    else:
        chosen = [c for c in found.candidates if c.candidate_id == option]
        unresolved = Why.CANDIDATE_GONE
    if not chosen:
        return TrackMatch(
            wanted=found.wanted, state=MatchState.NEEDS_REVIEW, why=unresolved,
            candidates=found.candidates, item_id=item_id, withheld=found.withheld,
        )
    return TrackMatch(
        wanted=found.wanted, state=MatchState.MATCHED, why=Why.VERDICT_ACCEPTED,
        candidates=tuple(chosen),
        paths=tuple(path for candidate in chosen for path in candidate.paths), item_id=item_id,
        withheld=found.withheld,
    )


__all__ = [
    "APPROXIMATE_FLOOR", "APPROXIMATE_LIMIT", "APPROXIMATE_TITLE_FLOOR", "ASKS_ABOUT_KEY",
    "ASKS_ABOUT_READING", "ASKS_ABOUT_RECORDING", "ASKS_ABOUT_VERSION", "BY_ISRC", "BY_SEARCH",
    "DIGEST_WIDTH", "KEY_QUESTIONS", "PAYLOAD_STATES", "OWNING_RULES", "QUESTION_KIND",
    "QUESTION_SHAPES", "READERS", "SPOTIFY", "STALLED", "TEXT", "TIDAL", "TOMBSTONE_KIND",
    "UNCREDITED_KIND", "VERSION_WORDS", "Acquisition", "Candidate", "LibraryIndex", "MatchResult",
    "MatchState", "Owned", "TrackMatch", "UnreadableList", "Wanted", "Why", "acquisition_options",
    "apply_verdict", "bare_title", "credited_members", "current_option", "digest", "fold",
    "fold_isrc", "index_library", "index_paths", "isrc_token", "key_disagreement", "key_token",
    "listed_names", "listed_title", "every_question_identity", "question_identity",
    "question_shape", "read_row", "read_spotify_items", "read_text_lines", "read_text_rows",
    "read_tidal_tracks", "remembered", "reset_cache", "row_isrc", "recording_identity",
    "recording_token", "resolve_all", "resolve_one", "same_title", "split_ambiguous", "split_title",
    "split_version", "standing_tombstone", "title_identity", "tombstone_fold", "version_identity",
    "version_token",
]
