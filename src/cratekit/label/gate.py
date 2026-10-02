"""The label genre gate, asked when a sweep lists a release (R-798).

WHAT IT IS FOR. At sitting 25, 36 of 186 tracks downloaded from followed labels
were not dance music, among them Christian music from another label with the
same name as a followed one. The gate in ``label approved`` had never held a
release, because no catalogue it read reported a genre, and it ran only after a
release was accepted, so the review queue carried everything.

WHAT IT ASKS. The general catalogue R-796 built, by the ISRC of the release's
own tracks, through :func:`cratekit.tagging.published.for_lookup`. The answer is
the album's genre words, and :func:`cratekit.core.routing.kind_verdict` says
whether they are the kind of music the label is followed for. This module owns
the asking and the sentence a person reads about it. It owns no rule: those are
the taxonomy's.

THE LOOKUP IS THE ONLY THING THAT TOUCHES THE CATALOGUE, and it paces every
request itself and remembers a refusal for the rest of the run. Nothing here
retries, waits out, or tries to get past an answer it did not like. A catalogue
that could not be read holds nothing: the release is filed for review as not
judged, and says the catalogue was unread.

A HOLD IS NOT A REJECTION. The release is recorded in the review database's
``held_offers`` with the words it was held on, is judged again from those words
on every sweep that reaches it, and can be returned to review by a person. No
tombstone is written.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from cratekit.acquire import match
from cratekit.core import review, routing
from cratekit.core.cause import CratekitError
from cratekit.core.review import Queue
from cratekit.core.routing import KindVerdict
from cratekit.core.taxonomy import Taxonomy
from cratekit.label import registry
from cratekit.label.catalogue import ReleasesUnasked, ReleaseUnresolvable
from cratekit.tagging import published
from cratekit.tagging.searchers import NOT_ASKED, Answer
from cratekit.tagging.tag import NO_ISRC

#: The review kind a label release is filed under. Declared here, once:
#: ``label.sweep`` takes its ``KIND`` from this, since that module imports this
#: one and the other direction would be a cycle.
RELEASE_KIND = "label-release"

#: How many of a release's tracks are asked about, at most. The genre is the
#: album's, so the first track whose album is the label's kind settles a pass.
#: A second and a third are asked when the one before is a recording the
#: catalogue does not list, AND WHEN ITS ALBUM WOULD HOLD THE RELEASE: one
#: track's ISRC can sit on a compilation of another kind, and a hold resting
#: on that alone would be a hold on a guess. Three, on the reasoning the
#: sweep's other bounds give: one is a bad row, two a coincidence.
TRACKS_ASKED = 3

#: How many releases IN A ROW may come back unread before the general catalogue
#: is not asked about the rest. Three, as the provider side's bound is. The
#: lookup itself remembers a refusal and stops, and does not remember an
#: outage, so without this a catalogue that is unreachable costs a transport
#: timeout for every release of every label in the sweep.
UNREAD_IN_A_ROW = 3

#: The payload fields a filed release carries about the gate. ``GATE_FIELD`` is
#: a :class:`~cratekit.core.routing.KindVerdict` value or :data:`RETURNED`.
GATE_FIELD = "genre_gate"
GATE_NOTE_FIELD = "genre_gate_note"
#: The general catalogue's answer word for the release, or ``not-asked``.
GATE_ANSWER_FIELD = "genre_gate_answer"
#: The words the catalogue published, in its order. Read back by
#: ``label approved`` so an accepted release is judged on the same words.
GENRES_FIELD = "published_genres"

#: The job that wrote the stamp, when it was not the sweep that filed the
#: release (R-815). ``crate label judge`` judges a release already in review
#: and says so here, so a reader counting what a SWEEP's gate did can leave its
#: answers out. A release stamped by the sweep that filed it carries none.
GATE_RUN_FIELD = "genre_gate_run"

#: What :data:`GATE_FIELD` says of a release a person returned to review.
RETURNED = "returned"


def release_item_id(release_id: str) -> str:
    """The review item a release is, or would be, in the label-release queue."""
    return review.item_id_for(Queue.LABEL_RELEASE, RELEASE_KIND, {"release_id": release_id})


@dataclass(frozen=True, slots=True)
class Words:
    """What the general catalogue published for one release's tracks.

    ``answer`` is the lookup's own word, :data:`NOT_ASKED` when nothing was
    asked. ``genres`` is non empty only for a match that published some.
    """

    genres: tuple[str, ...]
    answer: str
    note: str = ""

    @property
    def unread(self) -> bool:
        """Whether the catalogue could not be read, as opposed to having no answer."""
        return self.answer in published.UNREAD

    @property
    def why_none(self) -> str:
        """The sentence for a release with no published word, by what was answered."""
        if self.genres:
            return ""
        if self.unread:
            return (
                f"the general catalogue could not be read ({self.answer})"
                + (f": {self.note}" if self.note else "")
            )
        if self.answer == NO_ISRC:
            return "none of its tracks carries an ISRC to ask the general catalogue with"
        if self.answer == Answer.MISS.value:
            return "the general catalogue does not know its tracks"
        if self.answer == Answer.MATCHED.value:
            return "the general catalogue knows it and publishes no genre for it"
        return self.note or "the general catalogue was not asked about it"


def _isrcs(rows: Sequence[Any]) -> tuple[str, ...]:
    """Each row's ISRC value as the provider spelled it, in order, once each.

    Read through :func:`cratekit.acquire.match.row_isrc`, the one reader of
    where a row keeps it, so this module and the match engine cannot disagree
    about whether a row carries one.
    """
    found: dict[str, None] = {}
    for row in rows:
        value = match.row_isrc(row)
        if isinstance(value, str) and value.strip():
            found.setdefault(value.strip(), None)
    return tuple(found)


#: The answers that say the general catalogue WAS ASKED AND HAD NO WORD for a
#: release, most telling first. A track the catalogue KNOWS outranks one it
#: does not, and either outranks a value that was never an ISRC, which is the
#: order :func:`published_words` picks a wordless release's answer in.
#:
#: Public since R-815, which reads the same three off a filed release's stamp
#: to know the catalogue has already said all it has to say about it. An
#: answer that could not be read is not here, and neither is ``not-asked``:
#: nobody was told anything, so asking is still owed.
NO_WORD_ANSWERS: tuple[str, ...] = (Answer.MATCHED.value, Answer.MISS.value, NO_ISRC)


def published_words(
    rows: Sequence[Any],
    lookup: published.Lookup,
    *,
    enough: Callable[[tuple[str, ...]], bool] | None = None,
) -> Words:
    """Ask the general catalogue about one release, by its tracks' ISRCs.

    IN ORDER, :data:`TRACKS_ASKED` AT MOST, and the release's words are every
    word those tracks' albums publish, in the order met, once each.

    ``enough`` STOPS THE ASKING EARLY. It is handed the words so far and
    answers whether they already settle the caller's question. The gate passes
    "one of these is the label's kind", so a release whose first track is on an
    album of the label's kind costs one track's requests, and only a release
    that would be HELD is asked about again. Left as None the first track that
    publishes a genre is the answer.

    AN ANSWER THAT COULD NOT BE READ STOPS THE ASKING, AND THE RELEASE HAS NO
    WORDS. A refusal, an outage and an answer in a shape nobody knows are not
    "this track is unknown", and trying the next track against a catalogue that
    just refused would be the start of arguing with it. Words read before it
    are dropped with it: a verdict on half an answer is the hold on a guess
    this module exists not to make.

    NO ISRC ON ANY ROW ASKS NOTHING, and says so as its own answer, since a
    release nobody could ask about is not a release the catalogue does not know.

    WITH NO WORD AT ALL, THE MOST TELLING ANSWER IS THE RELEASE'S, not the last
    one given. A track the catalogue knows and publishes no genre for, beside
    one it does not know, is a release the catalogue KNOWS.
    """
    isrcs = _isrcs(rows)
    if not isrcs:
        return Words((), NO_ISRC)
    settled = enough if enough is not None else bool
    genres: dict[str, None] = {}
    empty: dict[str, published.Published] = {}
    for value in isrcs[:TRACKS_ASKED]:
        said = lookup(value)
        if said.answer in published.UNREAD:
            return Words((), said.answer, said.note)
        if said.answer == Answer.MATCHED.value and said.genres:
            for word in said.genres:
                genres.setdefault(word, None)
            if settled(tuple(genres)):
                break
        else:
            empty.setdefault(said.answer, said)
    if genres:
        return Words(tuple(genres), Answer.MATCHED.value)
    for answer in NO_WORD_ANSWERS:
        if answer in empty:
            return Words((), answer, empty[answer].note)
    said = next(iter(empty.values()))
    return Words((), said.answer, said.note)


@dataclass(frozen=True, slots=True)
class Judged:
    """One release judged at sweep time: the verdict and what it was judged on."""

    verdict: KindVerdict
    kind: str
    genres: tuple[str, ...]
    reason: str
    answer: str = NOT_ASKED
    placed: tuple[tuple[str, str], ...] = ()

    @property
    def held(self) -> bool:
        return self.verdict is KindVerdict.HOLD

    def stamp(self) -> dict[str, Any]:
        """What a filed release's payload says about the gate."""
        said: dict[str, Any] = {
            GATE_FIELD: self.verdict.value,
            GATE_NOTE_FIELD: self.reason,
            GATE_ANSWER_FIELD: self.answer,
        }
        if self.genres:
            said[GENRES_FIELD] = list(self.genres)
        return said

    def detail(self) -> dict[str, Any]:
        """What a hold records, so the release can be judged again with no request."""
        return {
            "genres": list(self.genres),
            "kind": self.kind,
            "placed": [list(pair) for pair in self.placed],
        }


def returned_stamp() -> dict[str, Any]:
    """The gate fields of a release a person returned to review."""
    return {
        GATE_FIELD: RETURNED,
        GATE_NOTE_FIELD: "returned to review by hand after the genre gate held it",
        GATE_ANSWER_FIELD: NOT_ASKED,
    }


def recorded_genres(source: Mapping[str, Any], field: str) -> tuple[str, ...] | None:
    """The published words a hold or a payload recorded, or None when it holds none.

    None for a field that is absent, empty or not a list of words. A caller
    reads None as "nothing was recorded", never as "the release has no genre".
    """
    held = source.get(field)
    if not isinstance(held, list):
        return None
    words = tuple(word.strip() for word in held if isinstance(word, str) and word.strip())
    return words or None


def release_id_of(store: review.ReviewStore, item: review.Item) -> str:
    """The release a review item names, from its IDENTITY before its payload.

    The identity is what the item is addressed by and is what the sweep keyed
    on. An item that arrived through ``review import`` carries none, because
    the export format does not, and then the payload's own copy of the
    identifier is all there is. Empty for an item naming no release at all.
    One reader, for ``label approved`` and ``label judge``.
    """
    identity = review.identity_of(store, item.item_id) or {}
    for value in (identity.get("release_id"), item.payload.get("identity")):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def returned_by(standing: review.Hold | None, payload: Mapping[str, Any]) -> bool:
    """Whether a person returned this release to review, by either record.

    The hold is the record of a return. A release the gate held at a SWEEP also
    carries the word on its payload, written when it was filed, and that copy
    is what survives a queue exported to another machine. A release returned
    while it was already in review has the hold alone, since a decided item's
    payload is never rewritten. Believing either is the safe direction: a
    returned release held a second time is music a person asked for and never
    gets.
    """
    return (standing is not None and standing.state == review.HOLD_RETURNED) or (
        payload.get(GATE_FIELD) == RETURNED
    )


def _of(judgment: routing.KindJudgment, words: Words | None = None) -> Judged:
    return Judged(
        verdict=judgment.verdict,
        kind=judgment.kind,
        genres=words.genres if words is not None else (),
        reason=judgment.reason,
        answer=words.answer if words is not None else NOT_ASKED,
        placed=judgment.placed,
    )


def judge_words(declared: Taxonomy, kind: str | None, words: Words) -> Judged:
    """The verdict for one release whose published words have been asked for.

    A release with no word is NOT JUDGED, with the sentence that says which
    kind of nothing it was, an unread catalogue or a track nobody lists.
    """
    settled = routing.kind_settled(declared, kind)
    if settled is not None:
        return _of(settled, words)
    if not words.genres:
        return Judged(
            KindVerdict.NOT_JUDGED,
            routing.label_kind(declared, kind),
            (),
            words.why_none,
            words.answer,
        )
    return _of(routing.kind_verdict(declared, kind, words.genres), words)


def judge_recorded(
    declared: Taxonomy, kind: str | None, genres: tuple[str, ...] | None
) -> Judged | None:
    """The verdict a filed release's own record settles, or None when it settles none.

    ``genres`` is what :func:`recorded_genres` read off the release. Two
    releases need nobody asked: one whose published words were recorded when
    it was filed, judged on them against the label's kind as it is now, and
    one on a label no word could change the verdict for. None means the
    catalogue is still owed a question. One spelling, for ``label approved``
    and ``label judge``.
    """
    if genres is not None:
        return judge_words(declared, kind, Words(genres, Answer.MATCHED.value))
    if routing.kind_settled(declared, kind) is not None:
        return judge_words(declared, kind, Words((), NOT_ASKED))
    return None


class Asking:
    """The general catalogue as the gate asks it, release after release.

    One per run of whatever is asking: the worker keeps one for a whole sweep
    job, across its labels, and ``label approved`` makes one per invocation.

    AFTER :data:`UNREAD_IN_A_ROW` RELEASES IN A ROW THAT COULD NOT BE READ, THE
    REST ARE NOT ASKED ABOUT, and each says so. The count is of releases, not
    requests, and a release that was answered ends the run, whatever the
    answer. A release with no ISRC asked nothing, so it neither ends a run nor
    extends one.

    THE LOOKUP IS LOOKED UP AT CALL TIME when none was handed in, off
    :mod:`cratekit.tagging.published`, which is the contract that module states
    and what lets a suite hand in a fake.
    """

    def __init__(self, lookup: published.Lookup | None = None) -> None:
        self._lookup = lookup
        self._unread_in_a_row = 0

    @property
    def given_up(self) -> bool:
        """Whether the bound was reached, so the next release would not be asked about.

        For a caller that pays to ask, R-815's, which reads a release's rows
        from the provider first: it stops before the read, not after it.
        """
        return self._unread_in_a_row >= UNREAD_IN_A_ROW

    def words(
        self,
        rows: Sequence[Any],
        *,
        enough: Callable[[tuple[str, ...]], bool] | None = None,
    ) -> Words:
        if self.given_up:
            return Words(
                (),
                NOT_ASKED,
                f"the general catalogue could not be read for {UNREAD_IN_A_ROW} "
                f"releases in a row, so the rest were not asked about",
            )
        lookup = self._lookup if self._lookup is not None else published.for_lookup()
        words = published_words(rows, lookup, enough=enough)
        if words.unread:
            self._unread_in_a_row += 1
        elif words.answer != NO_ISRC:
            self._unread_in_a_row = 0
        return words


def judge_rows(
    declared: Taxonomy, kind: str | None, rows: Sequence[Any], asking: Asking
) -> Judged:
    """Ask the general catalogue about a release's rows, and judge what it says.

    The one way a release is asked about, for the sweep and for
    ``label approved``, so the two cannot come to ask differently. The asking
    stops at the first track whose album is the label's kind.
    """

    def passes(genres: tuple[str, ...]) -> bool:
        return routing.kind_verdict(declared, kind, genres).verdict is KindVerdict.PASS

    return judge_words(declared, kind, asking.words(rows, enough=passes))


#: Reads one release's rows and its year. ``Catalogue.release_tracks``' shape.
TrackReader = Callable[[str], tuple[tuple[Any, ...], int | None]]


class StandingHolds:
    """The holds the review database already carries, as the sweep asks for them."""

    def __init__(self, store: review.ReviewStore) -> None:
        self.store = store

    def of(self, release_id: str) -> review.Hold | None:
        """The hold on one release, in force or returned, or None."""
        return review.find_hold(
            self.store, queue=Queue.LABEL_RELEASE, item_id=release_item_id(release_id)
        )

    def in_force(self, label_id: str) -> tuple[review.Hold, ...]:
        """Every hold in force on one label's releases."""
        return review.holds(self.store, queue=Queue.LABEL_RELEASE, group=label_id)


class SweepGate:
    """The gate one sweep item asks, release by release.

    ``tracks`` reads a release's rows. The worker hands the same remembered
    reader the ownership question uses,
    :class:`~cratekit.label.catalogue.ReleaseTracks`, so the gate adds no
    provider call for a release that question already read, and that reader's
    one outage rule covers both askers. ``standing`` answers the holds the
    review database already carries.

    ``asking`` is how the general catalogue is asked. The worker hands one that
    lasts the sweep job, so an unreachable catalogue is given up on once and
    not once per label. ``lookup`` is for a caller with a lookup and no
    ``Asking``, and builds one for this gate alone.
    """

    def __init__(
        self,
        declared: Taxonomy,
        *,
        tracks: TrackReader,
        standing: StandingHolds | None = None,
        lookup: published.Lookup | None = None,
        asking: Asking | None = None,
    ) -> None:
        self.declared = declared
        self._tracks = tracks
        self._standing = standing
        self._asking = asking if asking is not None else Asking(lookup)

    def standing(self, release_id: str) -> review.Hold | None:
        """The hold this release already has, in any state, or None."""
        return self._standing.of(release_id) if self._standing is not None else None

    def in_force(self, label_id: str) -> tuple[review.Hold, ...]:
        """Every hold in force on one label, the ones a sweep's window may not reach."""
        return self._standing.in_force(label_id) if self._standing is not None else ()

    def judge(self, entry: registry.LabelEntry, release_id: str) -> Judged:
        """Judge one release the sweep is about to file, by its label's kind."""
        return self.judge_as(entry.kind, release_id)

    def judge_as(self, label_kind: str | None, release_id: str) -> Judged:
        """Judge one release against the kind its label is followed as.

        ``label_kind`` is the registry entry's, or None for the default. Apart
        from :meth:`judge` because a release ALREADY IN REVIEW can be on a
        label the registry no longer holds, which has no entry to hand over
        and is judged as the default kind (R-815). One body, so the sweep and
        the verb that judges the queue cannot come to ask differently.

        NOTHING IS READ WHEN THE WORDS COULD NOT CHANGE THE VERDICT: a label
        followed for any kind, a taxonomy with no rule for this vocabulary, and
        a label marked with a kind the taxonomy does not name.

        A RELEASE WHOSE TRACKS COULD NOT BE READ IS NOT JUDGED, and neither is
        one the reader did not ask for because the provider is failing. A
        ``CratekitError`` passes through unchanged, as at every other seam
        boundary of the sweep: an expired session names an act that is the
        person's to take.

        A RELEASE THAT WOULD BE HELD IS ASKED ABOUT AGAIN, by its next tracks,
        before it is. See :data:`TRACKS_ASKED`.
        """
        settled = routing.kind_settled(self.declared, label_kind)
        if settled is not None:
            return _of(settled)
        kind = routing.label_kind(self.declared, label_kind)

        def unjudged(why: str) -> Judged:
            return Judged(KindVerdict.NOT_JUDGED, kind, (), why)

        try:
            rows, _year = self._tracks(release_id)
        except CratekitError:
            raise
        except ReleaseUnresolvable:
            return unjudged("the provider no longer has the release, so its tracks were not read")
        except ReleasesUnasked as exc:
            return unjudged(f"its tracks were not read: {exc}")
        except Exception as exc:  # noqa: BLE001 - not judged, and the release is filed
            return unjudged(
                f"its tracks could not be read from the provider ({type(exc).__name__}: {exc})"
            )
        return judge_rows(self.declared, label_kind, rows, self._asking)

    def rejudge(self, entry: registry.LabelEntry, held: review.Hold) -> Judged:
        """Judge a standing hold again, from the words it recorded. No request.

        This is how a change to the label's kind, or to the taxonomy's rules,
        releases a hold: the same words are put to the rules as they stand now.

        A HOLD WHOSE WORDS CANNOT BE READ BACK STAYS HELD, with the reason it
        was held on. Releasing it would file a release the gate once placed
        elsewhere on the strength of a row nobody could read, and a person can
        still return it by hand.
        """
        genres = recorded_genres(held.detail, "genres")
        if genres is None:
            return Judged(
                KindVerdict.HOLD,
                routing.label_kind(self.declared, entry.kind),
                (),
                held.reason,
            )
        words = Words(genres, Answer.MATCHED.value)
        return _of(routing.kind_verdict(self.declared, entry.kind, genres), words)


__all__ = [
    "GATE_ANSWER_FIELD",
    "GATE_FIELD",
    "GATE_NOTE_FIELD",
    "GATE_RUN_FIELD",
    "GENRES_FIELD",
    "NO_WORD_ANSWERS",
    "RELEASE_KIND",
    "RETURNED",
    "TRACKS_ASKED",
    "UNREAD_IN_A_ROW",
    "Asking",
    "Judged",
    "StandingHolds",
    "SweepGate",
    "TrackReader",
    "Words",
    "judge_recorded",
    "judge_rows",
    "judge_words",
    "published_words",
    "recorded_genres",
    "release_id_of",
    "release_item_id",
    "returned_by",
    "returned_stamp",
]
