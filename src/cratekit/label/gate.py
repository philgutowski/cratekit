"""The label genre gate, asked when a sweep lists a release (R-798).

It asks the general catalogue, by the ISRC of the release's own tracks, through
:func:`cratekit.tagging.published.for_lookup`, and
:func:`cratekit.core.routing.kind_verdict` says whether the album's genre words
are the kind of music the label is followed for. This module owns the asking and
the sentence a person reads; the rules are the taxonomy's.

The lookup is the only thing that touches the catalogue: it paces itself and
remembers a refusal. Nothing here retries or waits out an answer. A catalogue
that could not be read holds nothing, and the release is filed as not judged.

A hold is not a rejection: it is recorded in ``held_offers`` with its words, is
judged again from them on every sweep, and can be returned by a person. No
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

#: The review kind a label release is filed under, declared here because
#: ``label.sweep`` imports this module and takes its ``KIND`` from it.
RELEASE_KIND = "label-release"

#: How many of a release's tracks are asked about, at most. The first track whose
#: album is the label's kind settles a pass; a second and third are asked only
#: while the release would be held, since one track's ISRC can sit on a
#: compilation of another kind. One is a bad row, two a coincidence.
TRACKS_ASKED = 3

#: How many releases in a row may come back unread before the rest are not
#: asked about, so an unreachable catalogue costs three timeouts, not one per
#: release of every label in the sweep.
UNREAD_IN_A_ROW = 3

#: The payload fields a filed release carries about the gate. ``GATE_FIELD`` is
#: a :class:`~cratekit.core.routing.KindVerdict` value or :data:`RETURNED`.
GATE_FIELD = "genre_gate"
GATE_NOTE_FIELD = "genre_gate_note"
#: The general catalogue's answer word for the release, or ``not-asked``.
GATE_ANSWER_FIELD = "genre_gate_answer"
#: The words the catalogue published, in its order, read back by ``label approved``.
GENRES_FIELD = "published_genres"

#: The job that wrote the stamp when it was not the sweep that filed the release
#: (R-815), so a count of what a sweep's gate did can leave it out.
GATE_RUN_FIELD = "genre_gate_run"

#: What :data:`GATE_FIELD` says of a release a person returned to review.
RETURNED = "returned"


def release_item_id(release_id: str) -> str:
    """The review item a release is, or would be, in the label-release queue."""
    return review.item_id_for(Queue.LABEL_RELEASE, RELEASE_KIND, {"release_id": release_id})


#: What a release with no published word says, by the answer that was given.
_NONE_SAID = {
    NO_ISRC: "none of its tracks carries an ISRC to ask the general catalogue with",
    Answer.MISS.value: "the general catalogue does not know its tracks",
    Answer.MATCHED.value: "the general catalogue knows it and publishes no genre for it",
}


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
            note = f": {self.note}" if self.note else ""
            return f"the general catalogue could not be read ({self.answer}){note}"
        said = _NONE_SAID.get(self.answer) or self.note
        return said or "the general catalogue was not asked about it"


def _isrcs(rows: Sequence[Any]) -> tuple[str, ...]:
    """Each row's ISRC as the provider spelled it, in order, once each, read by
    :func:`cratekit.acquire.match.row_isrc` so the match engine cannot disagree."""
    values = (match.row_isrc(row) for row in rows)
    found = (one.strip() for one in values if isinstance(one, str))
    return tuple(dict.fromkeys(one for one in found if one))


#: The answers that say the catalogue WAS ASKED AND HAD NO WORD, most telling
#: first: a track it knows outranks one it does not, and either outranks a value
#: that was never an ISRC. Read off a filed stamp by R-815; an unread answer and
#: ``not-asked`` are not here, since asking is still owed.
NO_WORD_ANSWERS: tuple[str, ...] = (Answer.MATCHED.value, Answer.MISS.value, NO_ISRC)


def published_words(
    rows: Sequence[Any],
    lookup: published.Lookup,
    *,
    enough: Callable[[tuple[str, ...]], bool] | None = None,
) -> Words:
    """Ask the general catalogue about one release, by its tracks' ISRCs.

    In order, :data:`TRACKS_ASKED` at most; the words are every word those
    albums publish, once each. ``enough`` is handed the words so far and stops
    the asking once they settle the caller's question; left None, the first
    track that publishes a genre is the answer.

    AN ANSWER THAT COULD NOT BE READ STOPS THE ASKING AND DROPS THE WORDS read
    before it: a verdict on half an answer is a hold on a guess. No ISRC on any
    row asks nothing and says so. With no word at all, the most telling answer
    (:data:`NO_WORD_ANSWERS`) is the release's, not the last one given.
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
            genres.update(dict.fromkeys(said.genres))
            if settled(tuple(genres)):
                break
        else:
            empty.setdefault(said.answer, said)
    if genres:
        return Words(tuple(genres), Answer.MATCHED.value)
    answer = next((one for one in NO_WORD_ANSWERS if one in empty), next(iter(empty)))
    return Words((), answer, empty[answer].note)


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
        return {
            GATE_FIELD: self.verdict.value, GATE_NOTE_FIELD: self.reason,
            GATE_ANSWER_FIELD: self.answer,
            **({GENRES_FIELD: list(self.genres)} if self.genres else {}),
        }

    def detail(self) -> dict[str, Any]:
        """What a hold records, so the release can be judged again with no request."""
        placed = [list(pair) for pair in self.placed]
        return {"genres": list(self.genres), "kind": self.kind, "placed": placed}


def returned_stamp() -> dict[str, Any]:
    """The gate fields of a release a person returned to review."""
    return {
        GATE_FIELD: RETURNED,
        GATE_NOTE_FIELD: "returned to review by hand after the genre gate held it",
        GATE_ANSWER_FIELD: NOT_ASKED,
    }


def recorded_genres(source: Mapping[str, Any], field: str) -> tuple[str, ...] | None:
    """The published words a hold or a payload recorded, or None when it holds none.

    A caller reads None as "nothing was recorded", never as "no genre".
    """
    held = source.get(field)
    if not isinstance(held, list):
        return None
    words = tuple(word.strip() for word in held if isinstance(word, str) and word.strip())
    return words or None


def release_id_of(store: review.ReviewStore, item: review.Item) -> str:
    """The release a review item names, from its identity before its payload.

    An item that arrived through ``review import`` carries no identity, so the
    payload's copy is all there is. Empty for an item naming no release.
    """
    identity = review.identity_of(store, item.item_id) or {}
    for value in (identity.get("release_id"), item.payload.get("identity")):
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def hold_release_id(held: review.Hold) -> str:
    """The release a hold names, from its identity before its payload (an
    imported item's hold carries an empty identity)."""
    return str(held.identity.get("release_id") or held.payload.get("identity") or "")


def returned_by(standing: review.Hold | None, payload: Mapping[str, Any]) -> bool:
    """Whether a person returned this release to review, by either record.

    The hold records a return; a release held at a sweep also carries the word
    on its payload, which survives an exported queue. Believing either is the
    safe direction: a returned release held again is music a person never gets.
    """
    return (standing is not None and standing.state == review.HOLD_RETURNED) or (
        payload.get(GATE_FIELD) == RETURNED
    )


def _of(judgment: routing.KindJudgment, words: Words | None = None) -> Judged:
    genres, answer = (words.genres, words.answer) if words is not None else ((), NOT_ASKED)
    return Judged(judgment.verdict, judgment.kind, genres, judgment.reason, answer, judgment.placed)


def judge_words(declared: Taxonomy, kind: str | None, words: Words) -> Judged:
    """The verdict for one release whose published words have been asked for.

    A release with no word is NOT JUDGED, with the sentence saying which kind
    of nothing it was.
    """
    settled = routing.kind_settled(declared, kind)
    if settled is not None:
        return _of(settled, words)
    if not words.genres:
        label_kind = routing.label_kind(declared, kind)
        return Judged(KindVerdict.NOT_JUDGED, label_kind, (), words.why_none, words.answer)
    return _of(routing.kind_verdict(declared, kind, words.genres), words)


def judge_recorded(
    declared: Taxonomy, kind: str | None, genres: tuple[str, ...] | None
) -> Judged | None:
    """The verdict a filed release's own record settles, or None when it settles none.

    ``genres`` is what :func:`recorded_genres` read. Recorded words are judged
    against the label's kind as it is now, and a label no word could change
    the verdict for needs nobody asked; None means the catalogue is still owed
    a question. What a caller does with a hold is its own: a recorded pass can
    rest on one track, so ``label judge`` asks again before holding and
    ``label approved`` holds on it (R-798), a difference kept as a residual.
    """
    if genres is not None:
        return judge_words(declared, kind, Words(genres, Answer.MATCHED.value))
    if routing.kind_settled(declared, kind) is not None:
        return judge_words(declared, kind, Words((), NOT_ASKED))
    return None


class Asking:
    """The general catalogue as the gate asks it, release after release.

    One per run of whatever is asking. AFTER :data:`UNREAD_IN_A_ROW` RELEASES IN
    A ROW THAT COULD NOT BE READ, THE REST ARE NOT ASKED ABOUT, and each says
    so. A release answered ends the run of unread ones; one with no ISRC asked
    nothing and neither ends nor extends it. The lookup is looked up at call
    time when none was handed in, so a suite can hand in a fake.
    """

    def __init__(self, lookup: published.Lookup | None = None) -> None:
        self._lookup = lookup
        self._unread_in_a_row = 0

    @property
    def given_up(self) -> bool:
        """Whether the bound was reached, so a caller that pays to ask stops first."""
        return self._unread_in_a_row >= UNREAD_IN_A_ROW

    def words(
        self, rows: Sequence[Any], *, enough: Callable[[tuple[str, ...]], bool] | None = None
    ) -> Words:
        if self.given_up:
            return Words((), NOT_ASKED, (
                f"the general catalogue could not be read for {UNREAD_IN_A_ROW} "
                f"releases in a row, so the rest were not asked about"
            ))
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
    """Ask about a release's rows and judge what is said, the one way for the
    sweep and ``label approved``, stopping at the first track of the label's kind."""

    def passes(genres: tuple[str, ...]) -> bool:
        return routing.kind_verdict(declared, kind, genres).verdict is KindVerdict.PASS

    return judge_words(declared, kind, asking.words(rows, enough=passes))


#: Reads one release's rows, its year and any shortfall (R-515), as
#: ``Catalogue.release_tracks`` does.
TrackReader = Callable[[str], tuple[tuple[Any, ...], int | None, Any]]


class StandingHolds:
    """The holds the review database already carries, as the sweep asks for them."""

    def __init__(self, store: review.ReviewStore) -> None:
        self.store = store

    def of(self, release_id: str) -> review.Hold | None:
        """The hold on one release, in force or returned, or None."""
        item_id = release_item_id(release_id)
        return review.find_hold(self.store, queue=Queue.LABEL_RELEASE, item_id=item_id)

    def in_force(self, label_id: str) -> tuple[review.Hold, ...]:
        """Every hold in force on one label's releases."""
        return review.holds(self.store, queue=Queue.LABEL_RELEASE, group=label_id)


class SweepGate:
    """The gate one sweep item asks, release by release.

    ``tracks`` reads a release's rows; the worker hands the remembered
    :class:`~cratekit.label.catalogue.ReleaseTracks` the ownership question
    uses, so no release is read twice. ``standing`` answers the holds already
    carried. ``asking`` lasts the sweep job, so an unreachable catalogue is
    given up on once; ``lookup`` builds one for this gate alone.
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

        ``label_kind`` is None for the default, as for a release in review on a
        label the registry no longer holds (R-815). Nothing is read when no word
        could change the verdict. A release whose tracks could not be read is
        not judged; a ``CratekitError`` passes through, an act that is the
        person's. A release that would be held is asked about again by its next
        tracks first (:data:`TRACKS_ASKED`).
        """
        settled = routing.kind_settled(self.declared, label_kind)
        if settled is not None:
            return _of(settled)
        kind = routing.label_kind(self.declared, label_kind)

        def unjudged(why: str) -> Judged:
            return Judged(KindVerdict.NOT_JUDGED, kind, (), why)

        try:
            rows, _year, _short = self._tracks(release_id)
        except CratekitError:
            raise
        except ReleaseUnresolvable:
            return unjudged("the provider no longer has the release, so its tracks were not read")
        except ReleasesUnasked as exc:
            return unjudged(f"its tracks were not read: {exc}")
        except Exception as exc:  # noqa: BLE001 - not judged, and the release is filed
            why = f"its tracks could not be read from the provider ({type(exc).__name__}: {exc})"
            return unjudged(why)
        return judge_rows(self.declared, label_kind, rows, self._asking)

    def rejudge(self, entry: registry.LabelEntry, held: review.Hold) -> Judged:
        """Judge a standing hold again from the words it recorded, with no request,
        which is how a change of kind or rules releases a hold.

        A HOLD WHOSE WORDS CANNOT BE READ BACK STAYS HELD on its reason: releasing
        it would file a release on a row nobody could read.
        """
        genres = recorded_genres(held.detail, "genres")
        if genres is None:
            kind = routing.label_kind(self.declared, entry.kind)
            return Judged(KindVerdict.HOLD, kind, (), held.reason)
        verdict = routing.kind_verdict(self.declared, entry.kind, genres)
        return _of(verdict, Words(genres, Answer.MATCHED.value))


__all__ = [
    "GATE_ANSWER_FIELD", "GATE_FIELD", "GATE_NOTE_FIELD", "GATE_RUN_FIELD", "GENRES_FIELD",
    "NO_WORD_ANSWERS", "RELEASE_KIND", "RETURNED", "TRACKS_ASKED", "UNREAD_IN_A_ROW", "Asking",
    "Judged", "StandingHolds", "SweepGate", "TrackReader", "hold_release_id", "Words",
    "judge_recorded", "judge_rows", "judge_words", "published_words", "recorded_genres",
    "release_id_of", "release_item_id", "returned_by", "returned_stamp",
]
