"""Provider candidates for a missing row nothing names exactly (U79, R-302).

A typed tracklist line, a transcribed screenshot or a set track with no usable
ISRC carries an artist and a title and nothing a provider can be asked for by
identifier. This module asks the catalogue's text search about such a row and
decides what the answer is allowed to mean.

A SEARCH IS A PROPOSAL, NEVER A PICK. A provider ranks by its own relevance,
and a wrong pick spends a download where an offer costs one answer, so every
doubt lands on the offer side:

- A row is LISTED without a person only when the answer holds candidates that
  fold to exactly the row under ``match``'s own fold, all carry ONE distinct
  identifier, every row of the answer was read, the answer's last page is
  shorter than the seam's page, and the row's title reads one way only. A full
  page is read on to the next within a bound (R-879). Anything that could hide
  a second exact candidate sends the row to review.
- Anything else with a candidate worth showing is OFFERED into the review
  queue, exact candidates first and then by score, keyed on the folded row.
- A SCORE NEVER LISTS ANYTHING. It orders the screen and drops hits that do
  not resemble the row at all.
- No candidate is REPORTED, with the hit count and the best score.

An ACCEPTED item is read back on the next run before any search is spent. A
rejected item stays rejected until cleared, and an open one is not searched
again, because the question is already in front of a person.

Layer: modules. Nothing here writes a file or composes a download.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

from cratekit.acquire import match
from cratekit.core import review
from cratekit.intake import cli as intake_cli

#: The queue: the version confirm gate's own surface, whose legacy file is this
#: question exactly, what a provider text search resolved a recording to.
QUEUE = review.Queue.VERSION_MATCH

#: The kind, distinct from ``match.QUESTION_KIND`` on the same queue, which asks
#: about a copy the LIBRARY holds; this one asks about tracks the PROVIDER holds.
KIND = "provider-candidate"

#: How many candidates one item offers: twice the library's limit, because one
#: ISRC is commonly a single, an album cut and a compilation, all exact (R-356).
OFFER_LIMIT = 2 * match.APPROXIMATE_LIMIT

#: The score under which a hit that is not exact is not shown. NOT MEASURED
#: AGAINST A LIVE PROVIDER. It never lists anything and never hides an exact
#: candidate, so being wrong costs a near miss a person finds by hand.
CANDIDATE_FLOOR = 60.0

#: The most rows the provider's client says one search serves, across pages.
SEARCH_CEILING = 300


def __getattr__(name: str) -> int:
    """``SEARCH_PAGES``, worked out when asked for, since the page size is a toggle's.

    How many pages :func:`search_pages` reads at most: as many whole pages as
    fit under :data:`SEARCH_CEILING`, past which an empty page would be the
    provider declining to serve, not the end of what it holds (R-879).
    """
    if name == "SEARCH_PAGES":
        from cratekit.label.catalogue import TRACK_SEARCH_PAGE  # noqa: PLC0415 - a toggle's

        return SEARCH_CEILING // TRACK_SEARCH_PAGE
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
    #: How many of the provider's pages the answer was read from.
    pages: int = 1
    #: How many rows the LAST page read held. ``None`` for one page, which is
    #: every row, so a single page answer is read as it always was.
    last_page: int | None = None

    @property
    def full(self) -> bool:
        """The last page read filled the seam's page: a full then a short page is the end."""
        from cratekit.label.catalogue import TRACK_SEARCH_PAGE  # noqa: PLC0415 - a toggle's

        last = self.hits if self.last_page is None else self.last_page
        return last >= TRACK_SEARCH_PAGE

    @property
    def exact_refs(self) -> frozenset[str]:
        """The distinct identifiers the exact candidates carry."""
        return frozenset(one.track.ref for one in self.candidates if one.exact and one.track.ref)


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

    KEYED ON THE ROW, not its list or position, so the same line in two
    tracklists is one question. The title is its :func:`match.title_identity`,
    so two titles of emoji alone by one artist are two questions.
    """
    return wanted.folded_row()


def item_id(wanted: match.Wanted) -> str:
    return review.item_id_for(QUEUE, KIND, identity(wanted))


def query_title(wanted: match.Wanted) -> str:
    """The title half of the search: the title, and the version when it names one.

    A remix asked for by its plain title ranks under the original and can fall
    off the page. A qualifier meaning no version, original mix, is left out.
    """
    return f"{wanted.title} {wanted.version}".strip() if wanted.version_key else wanted.title


def _tokens(wanted: match.Wanted) -> frozenset[tuple[str, str]]:
    """Every (recording, version) the row reads as, the ambiguous reading too.

    BOTH READINGS MARK A CANDIDATE EXACT, AND NEITHER LISTS IT: a candidate
    matching either leads the screen, and a row with two readings is never
    listed without a person (:func:`sole_exact`). THE RECORDING'S IDENTITY, NOT
    ITS TOKEN, since two titles that fold to nothing share a token.
    """
    return frozenset((one.distinct, one.version_key) for one in wanted.readings)


def _album_of(row: object) -> str:
    album = row.get("album") if isinstance(row, Mapping) else getattr(row, "album", None)
    if isinstance(album, str):
        return album.strip()
    name = album.get("name") if isinstance(album, Mapping) else getattr(album, "name", None)
    return name.strip() if isinstance(name, str) else ""


def read_answer(wanted: match.Wanted, rows: tuple[Any, ...]) -> Answer:
    """The provider's rows as candidates, in the provider's order.

    A ROW THAT CANNOT BE READ IS COUNTED, or one exact track and one unreadable
    row would read as one exact candidate and list a guess.
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
                exact=(track.distinct, track.version_key) in exact_tokens,
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


def read_pages(wanted: match.Wanted, pages: Sequence[tuple[Any, ...]]) -> Answer:
    """Several pages of one search, read as one answer that knows its last page."""
    answer = read_answer(wanted, tuple(row for page in pages for row in page))
    return replace(answer, pages=len(pages), last_page=len(pages[-1]) if pages else 0)


def _settled_early(answer: Answer) -> bool:
    """Whether another page could change what :func:`sole_exact` says. ``True`` if not.

    Each of these refuses the row however many pages follow, so reading on
    would spend a provider call on a question already answered.
    """
    exact = [one for one in answer.candidates if one.exact]
    return (
        answer.ambiguous
        or bool(answer.unreadable)
        or any(not one.track.ref for one in exact)
        or len(answer.exact_refs) > 1
    )


def search_pages(
    search: Callable[[int], Iterable[Any]],
    wanted: match.Wanted,
    *,
    bound: int | None = None,
) -> Answer:
    """One search read page by page, until what past the cut is ruled in or out.

    ``search`` is handed the offset of each page (R-879). A common query fills
    its first page, and a full page alone would refuse nearly every row. The
    walk stops at a short page, the end of the listing; at an answer no further
    page can make listable; or at ``bound`` pages, default ``SEARCH_PAGES``,
    still full and refused. NOTHING IS LOWERED: the exact test is the same.
    """
    from cratekit.label.catalogue import TRACK_SEARCH_PAGE  # noqa: PLC0415 - a toggle's

    bound = SEARCH_CEILING // TRACK_SEARCH_PAGE if bound is None else bound
    pages: list[tuple[Any, ...]] = []
    while True:
        pages.append(tuple(search(len(pages) * TRACK_SEARCH_PAGE)))
        answer = read_pages(wanted, pages)
        if not answer.full or _settled_early(answer) or len(pages) >= bound:
            return answer


def sole_exact(answer: Answer) -> Candidate | None:
    """The one candidate the row may be listed as without a person, or ``None``.

    FIVE CONDITIONS, EACH REMOVABLE ALONE: one reading of the title, a last page
    that did not fill (a second exact one could sit past the cut), every row
    read, every exact candidate identified, and those identifiers one.
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

    One with no identifier cannot be downloaded and is not an option. The
    provider's order breaks a tie, so a repeat run offers the same list.
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

    READ BEFORE ANY SEARCH, so an answered or open row spends no provider call.
    AN ACCEPTANCE NAMES ITS CANDIDATE OR IT IS NOT ONE: with no option over one
    candidate it is that one, over several it stalls, never taking the first.
    """
    held = review.find(items, item_id(wanted))
    if held is None:
        return None

    def held_as(state: str, reason: str, track: match.Wanted | None = None) -> Proposal:
        return Proposal(wanted, state, reason, track, held.item_id, len(held.options))

    if held.verdict is None:
        return Proposal(
            wanted,
            WAITING,
            f"offered for review with {len(held.options)} candidate(s) and not yet answered",
            item_id=held.item_id,
            offered=len(held.options),
        )
    if held.verdict is review.Verdict.REJECTED:
        return held_as(
            REJECTED,
            "every provider candidate was rejected in review, so it is not searched "
            "for again until that answer is cleared",
        )
    chosen = held.option
    if chosen is None and len(held.options) == 1:
        chosen = held.options[0].option_id
    option = next((one for one in held.options if one.option_id == chosen), None)
    if option is None:
        return held_as(
            STALLED,
            f"accepted in review without naming which of its {len(held.options)} "
            f"candidates, so there is nothing to list",
        )
    said = (option.detail or {}).get("track")
    track = intake_cli.thawed(said) if isinstance(said, Mapping) else None
    if track is None or not track.ref or track.ref != option.option_id:
        return held_as(
            STALLED,
            f"the accepted candidate {option.option_id} does not carry the track it "
            f"was offered as, so there is nothing to list",
        )
    return held_as(ACCEPTED, f"accepted in review as {option.summary}", track)


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
        # A MATCH WITH NO IDENTIFIER IS SAID AS THAT, not as "none resembles it",
        # which would send a person after a spelling problem they do not have.

        unnamed = sum(
            1
            for one in answer.candidates
            if not one.track.ref and (one.exact or one.score >= CANDIDATE_FLOOR)
        )
        best = max((one.score for one in answer.candidates if one.track.ref), default=None)
        return Proposal(
            wanted,
            NO_CANDIDATES,
            (
                "the provider's search returned nothing for it"
                if not answer.hits
                else f"the provider's search returned {answer.hits} hit(s) and none "
                f"that can be downloaded resembles it"
                + (f", the best scoring {best:g}" if best is not None else "")
                + (
                    f"; {unnamed} that do resemble it carry no identifier"
                    if unnamed
                    else ""
                )
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
    "SEARCH_CEILING",
    "SEARCH_PAGES",  # noqa: F822 - served by __getattr__
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
    "read_pages",
    "search_pages",
    "settled",
    "shown",
    "sole_exact",
]
