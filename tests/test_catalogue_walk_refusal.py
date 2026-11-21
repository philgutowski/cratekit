"""U322: a refusing catalogue no longer stops tag suggest and tag backlog asking the ones that answer.

Measured at sitting 102 on 2026-11-21: ``crate tag backlog --catalogue`` on a
copy of the library asked the catalogues about 10 of 675 rows and stopped.
Discogs matched three of them and read no genre on the other seven, while
Beatport answered every lookup with Cloudflare's challenge. ``suggest`` read a
row as unread when only Beatport refused it, so three such rows in a row
stopped the walk, and 665 rows were never sent to Discogs or Deezer. U281's
own stop, which passes Beatport over after three refusals, never got the
chance to take effect.

The walk here is the shipped searcher over recorded pages, Discogs' empty
result set and Beatport's 403 carrying ``Cf-Mitigated: challenge``, and a
general catalogue that records what it was asked. Nothing touches the network.
"""

from __future__ import annotations

from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import published, searchers, suggest
from tests import test_tag_suggest as _suggest_suite
from tests.test_beatport_refusal import (
    REFUSED,
    _beatport_requests,
    _discogs_searches,
    _over_the_wire,
)
from tests.test_catalogue_searcher import ARTIST, TITLE
from tests.test_discogs_searcher import SENT

machine = _suggest_suite.machine

TAXONOMY = default_taxonomy()

#: An ISRC per row, so the general catalogue has something to be asked by.
ISRCS = tuple(f"GBAYE00000{n:02d}" for n in range(8))

#: What a refusal by every catalogue asked stops the walk with, as it is now.
STOPPED = f"not asked: the catalogues could not be read for {suggest.STOP_AFTER_UNREAD} rows in a row"


class _General:
    """The general catalogue, answering one word for every ISRC it is asked."""

    def __init__(self, answer: str = "miss", genres: tuple[str, ...] = ()):
        self.answer = answer
        self.genres = genres
        self.asked: list[object] = []

    def __call__(self, isrc: object) -> published.Published:
        self.asked.append(isrc)
        return published.Published(published.SOURCE, self.answer, genres=self.genres)


def _walk(beatport=REFUSED, *, discogs=None, token=SENT, general=None, rows=8, suggestions=True):
    """``rows`` rows asked as ``tag suggest --catalogue`` asks them, one searcher a run."""
    seen: list[str] = []
    fetch = _over_the_wire(beatport, discogs=discogs, seen=seen)
    asker = searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    search = searchers.catalogue_searcher(
        TAXONOMY, fetch=fetch, sleep=lambda _s: None, discogs=asker
    )
    opinion = None
    if general is not None:
        opinion = published.second_opinion(
            TAXONOMY, lookup=general, past_a_refusing_shop=suggestions
        )
    return search, opinion, seen


def _asked(machine, search, opinion, rows=8, unasked=frozenset()):
    lookup = suggest.catalogue_lookup(search, opinion)
    with suggest.KeptCatalogue(machine, lookup, unasked=unasked) as kept:
        answers = [
            kept.answer(str(n), ARTIST, f"{TITLE} {n}", ISRCS[n % len(ISRCS)]) for n in range(rows)
        ]
    return kept, answers


# ---------------------------------------------------------------------------
# A. The defect: a refusing Beatport beside a Discogs that answers
# ---------------------------------------------------------------------------


def test_a_discogs_miss_beside_a_refusing_beatport_does_not_stop_the_walk(machine):
    """The card's defect, red on main: the walk stopped at the third row."""
    search, _opinion, seen = _walk()
    kept, answers = _asked(machine, search, None)

    assert not kept.stopped
    assert kept.asked == 8
    assert _discogs_searches(seen) == 8
    # U281's own stop is what passes Beatport over, after its third refusal.
    assert _beatport_requests(seen) == searchers.REFUSALS_BEFORE_STOP
    assert all(STOPPED not in answer.note for answer in answers)


