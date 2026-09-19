"""Provider candidates for a missing row nothing names exactly (U79, R-302).

A typed tracklist line, a transcribed screenshot and a recognised set track
with no usable ISRC carry an artist and a title and nothing a provider can be
asked for by identifier. This module asks the catalogue's text search about one
such row and decides what the answer is allowed to mean.

A SEARCH IS A PROPOSAL, NEVER A PICK. A provider ranks by its own relevance: it
returns the remix beside the original, the radio edit beside the extended mix,
and an unrelated act of the same name beside all of them. A wrong pick downloads
the wrong track and spends a download, and an offer costs a person one answer,
so every doubt lands on the offer side:

- A row is LISTED without a person only when the answer holds candidates that
  fold to exactly the row, artist, title and version, under ``match``'s own fold,
  all of them carry ONE distinct identifier, every row of the answer could be
  read, the answer is shorter than the seam's page, and the row's title reads
  one way only. A row of the answer that could not be read, an exact candidate
  carrying no identifier, and a page that came back full could each hide a
  second exact candidate nobody can see, and a title whose dash tail may be a
  version or the end of the title is a row nobody can call exact, so each of
  those sends the row to review.
- Anything else with a candidate worth showing is OFFERED into the review queue,
  exact candidates first and then by score, keyed on the folded row, so the
  same line in two lists is one question and a second run re-offers nothing.
- A SCORE NEVER LISTS ANYTHING. It orders the screen and it drops hits that do
  not resemble the row at all, and that is the whole of what it does.
- No candidate is REPORTED, with how many hits the provider returned and the
  best score among them, never folded into "nothing to do".

An ACCEPTED item is read back on the next run, before any search is spent, and
the candidate the person chose is the track that is listed. A rejected item
stays rejected until somebody clears it, and an open one is not searched again,
because the question is already in front of a person.

Layer: modules. Nothing here writes a file or composes a download.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from cratekit.acquire import match
from cratekit.core import review
from cratekit.intake import cli as intake_cli
from cratekit.label.catalogue import TRACK_SEARCH_PAGE

#: The queue. The version confirm gate's own surface: its legacy file is the
#: source system's review of what a provider text search resolved a wanted
#: recording to, which is this question exactly, so it is not a new surface.
QUEUE = review.Queue.VERSION_MATCH

#: The kind, distinct from ``match.QUESTION_KIND`` on the same queue. That one
#: asks about a copy the LIBRARY holds and its payload is a ``TrackMatch``; this
#: one asks about tracks the PROVIDER holds, and neither reader reads the other.
KIND = "provider-candidate"

#: How many candidates one item offers. A person choosing between ten is still
#: choosing. Twice the library's ``APPROXIMATE_LIMIT``, because one ISRC is
#: commonly on a provider as a single, an album cut and a compilation (R-356)
#: and those are all exact, before any near miss is shown.
OFFER_LIMIT = 2 * match.APPROXIMATE_LIMIT

#: The score under which a hit that is not exact is not shown. NOT MEASURED
#: AGAINST A LIVE PROVIDER, and recorded as such in the ledger. It drops hits
#: that share a word with the row and nothing else. It never lists anything and
#: it never hides an exact candidate, so the cost of it being wrong is a near
#: miss a person has to find by hand, which the report names.
CANDIDATE_FLOOR = 60.0

#: What became of one row, one word a script can switch on.
LISTED = "listed"
ACCEPTED = "accepted"
OFFERED = "offered"
WAITING = "waiting"
REJECTED = "rejected"
NO_CANDIDATES = "no-candidates"
STALLED = "stalled"
#: An accepted candidate the library now holds, or that was deleted on purpose.
#: The verb's word and not this module's: it is set where the library is asked.
HELD = "held"

#: The states in which the row's ``track`` is a provider track to list.
NAMED = frozenset({LISTED, ACCEPTED})

#: The states in which a question is in front of a person.
ASKED = frozenset({OFFERED, WAITING})


@dataclass(frozen=True, slots=True)
class Candidate:
    """One provider track an answer held, read and compared with the row."""

    track: match.Wanted
    exact: bool
    score: float
    album: str = ""


@dataclass(frozen=True, slots=True)
class Answer:
    """One search answer, read. ``unreadable`` rows are counted, never dropped."""

    candidates: tuple[Candidate, ...]
    hits: int
    unreadable: int
    #: The row's title reads two ways, so no candidate can be called THE exact one.
    ambiguous: bool = False

    @property
    def full(self) -> bool:
        """The answer filled the seam's page, so it may have been cut short."""
        return self.hits >= TRACK_SEARCH_PAGE


@dataclass(frozen=True, slots=True)
class Proposal:
    """What one row came to: its state, the sentence, and the track if named."""

    wanted: match.Wanted
    state: str
    reason: str
    track: match.Wanted | None = None
    item_id: str | None = None
    offered: int = 0

    def to_json(self) -> dict[str, Any]:
        return {
            "artist": self.wanted.artist,
            "title": self.wanted.listed,
            "state": self.state,
            "reason": self.reason,
            "id": self.track.ref if self.track is not None else None,
            "item_id": self.item_id,
            "candidates": self.offered,
        }


def identity(wanted: match.Wanted) -> dict[str, str]:
    """What a row's question is addressed by: the folded row and nothing else.

    KEYED ON THE ROW, not on the list it arrived in and not on its position, so
    the same line typed into two tracklists is one question with one answer.
    The three fields are the ones the exact test compares.
    """
    return {
        "artist": match.fold(wanted.artist),
        "title": match.fold(wanted.title),
        "version": wanted.version_key,
    }


def item_id(wanted: match.Wanted) -> str:
    return review.item_id_for(QUEUE, KIND, identity(wanted))


def query_title(wanted: match.Wanted) -> str:
    """The title half of the search: the title, and the version when it names one.

    A provider searches one string, and a remix asked for by its plain title is
    ranked under the original and can fall off the page. A qualifier that means
    no version at all, original mix, is left out, since a provider that spells
    the record without it would rank it lower for the extra words.
    """
    return f"{wanted.title} {wanted.version}".strip() if wanted.version_key else wanted.title


def _tokens(wanted: match.Wanted) -> frozenset[tuple[str, str]]:
    """Every (recording, version) the row reads as, the ambiguous reading too.

    BOTH READINGS MARK A CANDIDATE EXACT, AND NEITHER LISTS IT. A title whose
    dash tail may be a version or the end of the title is two rows to the exact
    test, and a candidate matching either one is a candidate a person might have
    meant, so it leads the screen. ``match.Wanted.readings`` says the second
    reading is for what to OFFER and that nothing identifying is derived from
    it, and the string cannot say which reading is the first, so a row with two
    readings is never listed without a person: see :func:`sole_exact`.
    """
    return frozenset((one.recording, one.version_key) for one in wanted.readings)


def _album_of(row: object) -> str:
    album = row.get("album") if isinstance(row, Mapping) else getattr(row, "album", None)
    if isinstance(album, str):
        return album.strip()
    name = album.get("name") if isinstance(album, Mapping) else getattr(album, "name", None)
    return name.strip() if isinstance(name, str) else ""


def read_answer(wanted: match.Wanted, rows: tuple[Any, ...]) -> Answer:
    """The provider's rows as candidates, in the provider's order.

    A ROW THAT CANNOT BE READ IS COUNTED. Dropped, an answer of one exact track
    and one unreadable row would read as one exact candidate and list a guess.
    """
    from rapidfuzz import fuzz

    exact_tokens = _tokens(wanted)
    candidates: list[Candidate] = []
    unreadable = 0
    for position, row in enumerate(rows, start=1):
        try:
            track = match.read_row(row, origin=match.TIDAL, position=position)
        except match.UnreadableList:
            unreadable += 1
            continue
        candidates.append(
            Candidate(
                track=track,
                exact=(track.recording, track.version_key) in exact_tokens,
                score=round(float(fuzz.token_sort_ratio(wanted.recording, track.recording)), 1),
                album=_album_of(row),
            )
        )
    return Answer(
        candidates=tuple(candidates),
        hits=len(rows),
        unreadable=unreadable,
        ambiguous=wanted.other_reading is not None,
    )


def sole_exact(answer: Answer) -> Candidate | None:
    """The one candidate the row may be listed as without a person, or ``None``.

    FIVE CONDITIONS, EACH REMOVABLE ALONE. The row's title reads one way. The
    answer did not fill the page, since a second exact candidate could sit past
    the cut. Every row of the answer was read. Every exact candidate carries an
    identifier. Those identifiers are one.
    """
    exact = [one for one in answer.candidates if one.exact]
    if answer.ambiguous or answer.full:
        return None
    if answer.unreadable or not exact:
        return None
    if any(not one.track.ref for one in exact):
        return None
    if len({one.track.ref for one in exact}) != 1:
        return None
    return exact[0]


def shown(answer: Answer) -> tuple[Candidate, ...]:
    """The candidates an item offers: exact first, then best score, one per id.

    A candidate with no identifier cannot be downloaded and is not an option.
    The provider's own order breaks a tie, so a repeat run offers the same list.
    """
    ranked = sorted(
        (
            (not one.exact, -one.score, position, one)
            for position, one in enumerate(answer.candidates)
            if one.track.ref and (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=lambda entry: entry[:3],
    )
    seen: set[str] = set()
    kept: list[Candidate] = []
    for _not_exact, _score, _position, one in ranked:
        if one.track.ref in seen:
            continue
        seen.add(one.track.ref)
        kept.append(one)
    return tuple(kept)


def _summary(one: Candidate) -> str:
    said = f"{one.track.artist} - {one.track.listed}"
    if one.album:
        said += f" [{one.album}]"
    return f"{said} ({'exact' if one.exact else f'score {one.score:g}'})"


def _option(one: Candidate) -> review.Option:
    return review.Option(
        option_id=one.track.ref,
        summary=_summary(one),
        detail={
            "track": intake_cli.frozen(one.track),
            "exact": one.exact,
            "score": one.score,
            "album": one.album,
        },
    )


def _why_offered(answer: Answer, offered: tuple[Candidate, ...]) -> str:
    exact = len({one.track.ref for one in offered if one.exact})
    if exact and answer.ambiguous:
        return (
            "its title reads two ways, as a version or as the end of the title, so "
            "no candidate can be called the exact one without a person"
        )
    if exact > 1:
        return (
            f"the provider holds {exact} tracks that match it exactly, and which "
            f"release to download is not something the row decides"
        )
    if exact and answer.full:
        return (
            f"one candidate matches it exactly and the provider's answer filled its "
            f"page of {answer.hits}, so another exact one may sit past the cut"
        )
    if exact and answer.unreadable:
        return (
            f"one candidate matches it exactly and {answer.unreadable} row(s) of the "
            f"answer could not be read, so it may not be the only one"
        )
    if exact:
        return (
            "one candidate matches it exactly and another exact one carries no "
            "identifier, so it may not be the only one"
        )
    return "no candidate matches it exactly, and a near miss is never picked from a score"


def settled(items: review.ReviewStore, wanted: match.Wanted) -> Proposal | None:
    """What the queue already says about this row, or ``None`` when it says nothing.

    READ BEFORE ANY SEARCH, so an answered row and a row already in front of a
    person spend no provider call.

    AN ACCEPTANCE NAMES ITS CANDIDATE OR IT IS NOT ONE. Accepted with no option
    over an item that offered one candidate is that candidate, since nothing
    else was on the screen. Over several it is a yes to nobody knows which, and
    the row stalls with clearing named as the way through, never the first.
    """
    held = review.find(items, item_id(wanted))
    if held is None:
        return None
    if held.verdict is None:
        return Proposal(
            wanted,
            WAITING,
            f"offered for review with {len(held.options)} candidate(s) and not yet answered",
            item_id=held.item_id,
            offered=len(held.options),
        )
    if held.verdict is review.Verdict.REJECTED:
        return Proposal(
            wanted,
            REJECTED,
            "every provider candidate was rejected in review, so it is not searched "
            "for again until that answer is cleared",
            item_id=held.item_id,
            offered=len(held.options),
        )
    chosen = held.option
    if chosen is None and len(held.options) == 1:
        chosen = held.options[0].option_id
    option = next((one for one in held.options if one.option_id == chosen), None)
    if option is None:
        return Proposal(
            wanted,
            STALLED,
            f"accepted in review without naming which of its {len(held.options)} "
            f"candidates, so there is nothing to list",
            item_id=held.item_id,
            offered=len(held.options),
        )
    said = (option.detail or {}).get("track")
    track = intake_cli.thawed(said) if isinstance(said, Mapping) else None
    if track is None or not track.ref or track.ref != option.option_id:
        return Proposal(
            wanted,
            STALLED,
            f"the accepted candidate {option.option_id} does not carry the track it "
            f"was offered as, so there is nothing to list",
            item_id=held.item_id,
            offered=len(held.options),
        )
    return Proposal(
        wanted,
        ACCEPTED,
        f"accepted in review as {option.summary}",
        track=track,
        item_id=held.item_id,
        offered=len(held.options),
    )


def propose(
    items: review.ReviewStore,
    wanted: match.Wanted,
    answer: Answer,
    *,
    handler_key: str,
) -> Proposal:
    """List the row, offer its candidates, or say there are none. Never pick."""
    sole = sole_exact(answer)
    if sole is not None:
        return Proposal(
            wanted,
            LISTED,
            f"the provider's search holds exactly one track matching it, {_summary(sole)}",
            track=sole.track,
        )
    offered = shown(answer)
    if not offered:
        best = max((one.score for one in answer.candidates), default=None)
        return Proposal(
            wanted,
            NO_CANDIDATES,
            (
                "the provider's search returned nothing for it"
                if not answer.hits
                else f"the provider's search returned {answer.hits} hit(s) and none "
                f"resembles it"
                + (f", the best scoring {best:g}" if best is not None else "")
                + (f"; {answer.unreadable} could not be read" if answer.unreadable else "")
            ),
        )
    withheld = len(offered) - OFFER_LIMIT if len(offered) > OFFER_LIMIT else 0
    on_screen = offered[:OFFER_LIMIT]
    held = review.offer(
        items,
        queue=QUEUE,
        kind=KIND,
        identity=identity(wanted),
        payload={
            "wanted": intake_cli.frozen(wanted),
            "why": _why_offered(answer, offered),
            "hits": answer.hits,
            "unreadable": answer.unreadable,
            "withheld": withheld,
            "candidates": [
                {
                    "id": one.track.ref,
                    "artist": one.track.artist,
                    "title": one.track.listed,
                    "album": one.album,
                    "exact": one.exact,
                    "score": one.score,
                }
                for one in on_screen
            ],
        },
        options=[_option(one) for one in on_screen],
        handler_key=handler_key,
    )
    return Proposal(
        wanted,
        OFFERED,
        _why_offered(answer, offered),
        item_id=held.item_id,
        offered=len(on_screen),
    )


__all__ = [
    "ACCEPTED",
    "ASKED",
    "CANDIDATE_FLOOR",
    "HELD",
    "KIND",
    "LISTED",
    "NAMED",
    "NO_CANDIDATES",
    "OFFERED",
    "OFFER_LIMIT",
    "QUEUE",
    "REJECTED",
    "STALLED",
    "WAITING",
    "Answer",
    "Candidate",
    "Proposal",
    "identity",
    "item_id",
    "propose",
    "query_title",
    "read_answer",
    "settled",
    "shown",
    "sole_exact",
]
