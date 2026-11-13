"""U281: Beatport's refusal is read as one, and a run stops asking a catalogue that refused it.

Measured at sitting 97 on 2026-11-13: every Beatport lookup since 03:49Z that
day answered HTTP 403 with ``Cf-Mitigated: challenge`` and Cloudflare's "Just a
moment..." page, 190 of 190 across five runs, and each one was recorded
``unreachable``, a paced request per file. These are the searcher's half of the
card: the read of the refusal, the per run count that stops asking, and the two
rules that must hold through both, that a refused file is never a miss and that
a catalogue which answered is never stopped. The sweep's half, the worker's run
scope and the warning's words, is in ``tests/test_tag_workers.py``.

Every page here is a fake or a recorded shape. Nothing touches the network.
"""

from __future__ import annotations

import pytest

from cratekit.core.cause import CratekitError
from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import published, searchers
from tests.test_catalogue_searcher import (
    ARTIST,
    BUCKET_GENRE,
    TITLE,
    _beatport_page,
    _beatport_track,
)
from tests.test_discogs_searcher import SENT, release, results

TAXONOMY = default_taxonomy()

#: The page Beatport served at sitting 97, in the shape Cloudflare serves it.
CHALLENGE_PAGE = (
    '<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title>'
    "</head><body><script>window._cf_chl_opt={}</script>"
    '<script src="/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1"></script>'
    "</body></html>"
)

#: The headers that 403 carried, as a client library hands them over.
CHALLENGE_HEADERS = {"Server": "cloudflare", "Cf-Mitigated": "challenge"}


class _Response:
    """The fields the shipped fetch reads off an answer: status, text and headers."""

    def __init__(self, status_code: int, text: str = "", headers: dict | None = None) -> None:
        self.status_code = status_code
        self.text = text
        self.content = b""
        self.headers = dict(headers or {})


def _over_the_wire(beatport, *, discogs=None, seen: list[str] | None = None):
    """The shipped fetch over a getter answering Beatport and Discogs by URL.

    ``beatport`` is one reply, or a list taken one per Beatport request.
    ``discogs`` answers the search, and the one release it names, and is a
    miss when not given.
    """
    replies = list(beatport) if isinstance(beatport, list) else None
    search = discogs if discogs is not None else _Response(200, results())

    def get(url, headers, timeout):
        if seen is not None:
            seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return replies.pop(0) if replies is not None else beatport
        if url.startswith(searchers.DISCOGS_SEARCH):
            return search
        if url.startswith(searchers.DISCOGS_RELEASE):
            return _Response(200, release(1))
        raise OSError(f"no route for {url}")

    return searchers.default_fetch(get=get, sleep=lambda _s: None)


def _searcher(fetch, *, refusals=None, token: str | None = SENT, discogs=None):
    """The default walk, Beatport then Discogs, over ``fetch``."""
    asker = discogs or searchers.discogs_asker(token=token, fetch=fetch, sleep=lambda _s: None)
    return searchers.catalogue_searcher(
        TAXONOMY,
        fetch=fetch,
        sleep=lambda _s: None,
        discogs=asker,
        refusals=refusals,
    )


def _beatport(hit) -> searchers.SourceAnswer:
    (said,) = [one for one in hit.answers if one.source == searchers.BEATPORT]
    return said


def _beatport_requests(seen: list[str]) -> int:
    return sum(url.startswith(searchers.BEATPORT_SEARCH) for url in seen)


def _discogs_searches(seen: list[str]) -> int:
    return sum(url.startswith(searchers.DISCOGS_SEARCH) for url in seen)


REFUSED = _Response(403, CHALLENGE_PAGE, CHALLENGE_HEADERS)
MISSED = _Response(200, _beatport_page([]))


# ---------------------------------------------------------------------------
# A. Beatport's answer, read the way the fallbacks' is
# ---------------------------------------------------------------------------


def test_a_403_carrying_cloudflares_challenge_header_is_blocked_and_named():
    hit = _searcher(_over_the_wire(REFUSED))(ARTIST, TITLE)

    said = _beatport(hit)
    assert said.answer == "blocked"
    assert said.note == "the catalogue refused this client, Cloudflare challenge, HTTP 403"
    assert searchers.BEATPORT in hit.unread


def test_a_403_without_the_header_is_blocked_and_says_only_the_status():
    hit = _searcher(_over_the_wire(_Response(403, "", {"Server": "nginx"})))(ARTIST, TITLE)

    said = _beatport(hit)
    assert said.answer == "blocked"
    assert said.note == "the catalogue refused this client, HTTP 403"
    assert searchers.CLOUDFLARE_CHALLENGE not in said.note


def test_the_challenge_header_is_read_whatever_case_its_name_and_value_arrive_in():
    hit = _searcher(_over_the_wire(_Response(403, "", {"CF-MITIGATED": " Challenge "})))(
        ARTIST, TITLE
    )

    assert searchers.CLOUDFLARE_CHALLENGE in _beatport(hit).note


def test_another_mitigation_is_not_called_a_challenge():
    hit = _searcher(_over_the_wire(_Response(403, "", {"Cf-Mitigated": "block"})))(
        ARTIST, TITLE
    )

    assert _beatport(hit).note == "the catalogue refused this client, HTTP 403"


def test_a_200_just_a_moment_page_is_blocked_not_a_parse_break():
    """R-794: the challenge carries no ``__NEXT_DATA__``, so parsed first it
    was a parser defect and, beside an unread Discogs, a refusal telling the
    person to report one."""
    hit = _searcher(_over_the_wire(_Response(200, CHALLENGE_PAGE)))(ARTIST, TITLE)

    said = _beatport(hit)
    assert said.answer == "blocked"
    assert searchers.CLOUDFLARE_CHALLENGE in said.note
    assert "Just a moment..." in said.note


def test_a_200_page_carrying_only_cloudflares_script_is_blocked():
    page = (
        "<html><head><title>beatport</title></head><body>"
        '<script src="/cdn-cgi/challenge-platform/h/b/x"></script></body></html>'
    )
    hit = _searcher(_over_the_wire(_Response(200, page)))(ARTIST, TITLE)

    said = _beatport(hit)
    assert said.answer == "blocked"
    assert searchers.CLOUDFLARE_CHALLENGE in said.note


def test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken():
    with pytest.raises(CratekitError) as raised:
        _searcher(
            _over_the_wire(_Response(200, CHALLENGE_PAGE), discogs=_Response(503))
        )(ARTIST, TITLE)

    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.detail["answers"] == ["blocked", "unreachable"]


def test_a_bandcamp_client_challenge_title_is_blocked_and_not_called_cloudflare():
    page = searchers.Fetched(
        text="<html><head><title>Client Challenge</title></head></html>", status=200
    )
    said = searchers.unread_outcome(searchers.BANDCAMP, page)

    assert said is not None and said.answer is searchers.Answer.BLOCKED
    assert searchers.CLOUDFLARE_CHALLENGE not in said.note


@pytest.mark.parametrize(
    "reply",
    [_Response(503), _Response(500), _Response(502, CHALLENGE_PAGE)],
    ids=["503", "500", "502-with-a-page"],
)
def test_a_server_error_from_beatport_stays_unreachable(reply):
    hit = _searcher(_over_the_wire(reply))(ARTIST, TITLE)

    assert _beatport(hit).answer == "unreachable"


def test_a_transport_failure_from_beatport_stays_unreachable():
    def get(url, headers, timeout):
        if url.startswith(searchers.BEATPORT_SEARCH):
            raise OSError("name or service not known")
        if url.startswith(searchers.DISCOGS_SEARCH):
            return _Response(200, results())
        raise OSError(f"no route for {url}")

    fetch = searchers.default_fetch(get=get, sleep=lambda _s: None)
    hit = _searcher(fetch)(ARTIST, TITLE)

    said = _beatport(hit)
    assert said.answer == "unreachable"
    assert "name or service not known" in said.note


def test_a_429_that_outlasts_the_backoff_is_blocked_as_the_fallbacks_read_it():
    hit = _searcher(_over_the_wire(_Response(429)))(ARTIST, TITLE)

    said = _beatport(hit)
    assert said.answer == "blocked"
    assert "rate limited" in said.note


def test_a_beatport_answer_with_results_still_matches():
    page = _beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)])
    hit = _searcher(_over_the_wire(_Response(200, page)))(ARTIST, TITLE)

    assert hit.genre == BUCKET_GENRE
    assert _beatport(hit).answer == "matched"


# ---------------------------------------------------------------------------
# B. Three refusals in a row stop the run asking, and nothing else does
# ---------------------------------------------------------------------------


def _sweep(replies, *, refusals, discogs=None, count: int | None = None):
    """``count`` files searched as a worker searches them, one searcher per file.

    One searcher per file is the worker's shape, and the reason the count is
    handed in: a count kept by the searcher would start again at every file.
    """
    seen: list[str] = []
    fetch = _over_the_wire(list(replies), discogs=discogs, seen=seen)
    asker = searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None)
    hits = [
        _searcher(fetch, refusals=refusals, discogs=asker)(ARTIST, f"{TITLE} {n}")
        for n in range(count if count is not None else len(replies))
    ]
    return hits, seen


def test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked():
    hits, seen = _sweep([REFUSED] * 3, refusals=searchers.Refusals(), count=5)

    assert _beatport_requests(seen) == 3
    for hit in hits[3:]:
        said = _beatport(hit)
        assert said.answer == "blocked"
        assert said.note.startswith(searchers.NOT_SENT)
        assert "refused this client on its last 3 lookups in this sweep" in said.note
        # The refusal it is standing on is quoted, so the record still says what
        # Beatport answered when it was last asked.
        assert said.note.endswith(
            "Then, the catalogue refused this client, Cloudflare challenge, HTTP 403"
        )
        assert searchers.BEATPORT in hit.unread


def test_a_stopped_beatport_never_reads_as_a_miss_or_a_clean_no_hit():
    """The card's merge blocker: a refused file stays askable."""
    hits, _seen = _sweep([REFUSED] * 3, refusals=searchers.Refusals(), count=6)

    for hit in hits:
        assert hit.genre is None
        assert _beatport(hit).answer != "miss"
        assert hit.unread == (searchers.BEATPORT,)


def test_discogs_is_still_asked_on_every_file_beatport_was_not():
    hits, seen = _sweep([REFUSED] * 3, refusals=searchers.Refusals(), count=5)

    assert _discogs_searches(seen) == 5
    for hit in hits:
        (discogs,) = [one for one in hit.answers if one.source == searchers.DISCOGS]
        assert discogs.answer == "miss"


def test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread():
    refusals = searchers.Refusals()
    _sweep([REFUSED] * 3, refusals=refusals)
    seen: list[str] = []
    fetch = _over_the_wire([], discogs=_Response(200, results(1)), seen=seen)
    hit = _searcher(fetch, refusals=refusals)(ARTIST, TITLE)

    assert _beatport_requests(seen) == 0
    assert hit.genre is not None
    assert hit.source == searchers.DISCOGS
    assert hit.unread == (searchers.BEATPORT,)


def test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline():
    refusals = searchers.Refusals()
    _sweep([REFUSED] * 3, refusals=refusals)
    with pytest.raises(CratekitError) as raised:
        _searcher(_over_the_wire([]), refusals=refusals, token=None)(ARTIST, TITLE)

    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.detail["answers"] == ["blocked"]


def test_blocked_miss_blocked_blocked_does_not_stop_the_run():
    hits, seen = _sweep(
        [REFUSED, MISSED, REFUSED, REFUSED, MISSED], refusals=searchers.Refusals()
    )

    assert _beatport_requests(seen) == 5
    assert [_beatport(hit).answer for hit in hits] == [
        "blocked",
        "miss",
        "blocked",
        "blocked",
        "miss",
    ]


def test_an_outage_between_refusals_ends_the_run_of_them():
    """Only refusals with nothing between them stop the run; an outage is an
    answer of its own, so the count starts again after it."""
    _hits, seen = _sweep(
        [REFUSED, REFUSED, _Response(503), REFUSED, REFUSED], refusals=searchers.Refusals()
    )

    assert _beatport_requests(seen) == 5


def test_a_match_resets_the_count_as_a_miss_does():
    page = _Response(200, _beatport_page([_beatport_track(ARTIST, f"{TITLE} 2", BUCKET_GENRE)]))
    _hits, seen = _sweep([REFUSED, REFUSED, page, REFUSED, REFUSED], refusals=searchers.Refusals())

    assert _beatport_requests(seen) == 5


def test_a_new_run_asks_again_from_its_first_file():
    first = searchers.Refusals()
    _sweep([REFUSED] * 3, refusals=first, count=5)

    hits, seen = _sweep([REFUSED] * 3, refusals=searchers.Refusals(), count=4)

    assert _beatport_requests(seen) == 3
    assert not _beatport(hits[0]).note.startswith(searchers.NOT_SENT)


def test_a_searcher_given_no_count_keeps_its_own_for_its_life():
    seen: list[str] = []
    fetch = _over_the_wire([REFUSED] * 3, seen=seen)
    search = _searcher(fetch)
    for n in range(5):
        search(ARTIST, f"{TITLE} {n}")

    assert _beatport_requests(seen) == 3


def test_a_stopped_catalogue_is_answered_without_a_wait():
    """The point of stopping is the paced second and a half per file, so a
    catalogue answered from the count is not waited for either."""
    refusals = searchers.Refusals()
    _sweep([REFUSED] * 3, refusals=refusals)
    naps: list[float] = []
    fetch = _over_the_wire([])
    asker = searchers.discogs_asker(token=None, fetch=fetch, sleep=lambda _s: None)
    search = searchers.catalogue_searcher(
        TAXONOMY,
        fetch=fetch,
        pacing=searchers.Pacer(sleep=naps.append),
        discogs=asker,
        refusals=refusals,
    )
    with pytest.raises(CratekitError):
        search(ARTIST, TITLE)

    assert naps == []


def test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one():
    """The scraped walk, where three catalogues are scraped: Traxsource refuses
    every search and is stopped, Beatport and Bandcamp answer and are asked on
    every file."""
    seen: list[str] = []
    empty_bandcamp = "<html><ul class='result-items'></ul></html>"

    def get(url, headers, timeout):
        seen.append(url)
        if url.startswith(searchers.BEATPORT_SEARCH):
            return MISSED
        if url.startswith(searchers.TRAXSOURCE_SEARCH):
            return REFUSED
        if url.startswith(searchers.BANDCAMP_SEARCH):
            return _Response(200, empty_bandcamp)
        raise OSError(f"no route for {url}")

    fetch = searchers.default_fetch(get=get, sleep=lambda _s: None)
    refusals = searchers.Refusals()
    hits = [
        searchers.catalogue_searcher(
            TAXONOMY,
            fetch=fetch,
            sleep=lambda _s: None,
            walk=searchers.SCRAPED_WALK,
            refusals=refusals,
        )(ARTIST, f"{TITLE} {n}")
        for n in range(5)
    ]

    assert sum(url.startswith(searchers.TRAXSOURCE_SEARCH) for url in seen) == 3
    assert _beatport_requests(seen) == 5
    assert sum(url.startswith(searchers.BANDCAMP_SEARCH) for url in seen) == 5
    for hit in hits:
        assert hit.unread == (searchers.TRAXSOURCE,)


def test_discogs_is_never_under_the_count():
    """Discogs remembers its own refusal; the count is the scraped catalogues'."""
    refusals = searchers.Refusals()
    for _ in range(searchers.REFUSALS_BEFORE_STOP + 1):
        refusals.heard(searchers.SourceOutcome(searchers.DISCOGS, searchers.Answer.BLOCKED))
    seen: list[str] = []
    fetch = _over_the_wire(MISSED, seen=seen)
    hit = _searcher(fetch, refusals=refusals)(ARTIST, TITLE)

    assert _discogs_searches(seen) == 1
    (discogs,) = [one for one in hit.answers if one.source == searchers.DISCOGS]
    assert discogs.answer == "miss"


def test_the_limit_is_three():
    assert searchers.REFUSALS_BEFORE_STOP == 3


# ---------------------------------------------------------------------------
# C. The run's count, found by the run
# ---------------------------------------------------------------------------


def test_one_run_name_is_one_count_and_another_name_a_fresh_one():
    first = searchers.for_run("job-a@1")
    assert searchers.for_run("job-a@1") is first

    resumed = searchers.for_run("job-a@2")
    assert resumed is not first
    assert searchers.for_run("job-b@1") is not resumed


def test_a_run_met_again_after_another_starts_afresh():
    """One slot: a run that is no longer the process's run keeps nothing."""
    first = searchers.for_run("job-a@1")
    first.heard(searchers.SourceOutcome(searchers.BEATPORT, searchers.Answer.BLOCKED))
    searchers.for_run("job-b@1")

    assert searchers.for_run("job-a@1").running == {}


def test_forgetting_the_runs_drops_the_count():
    first = searchers.for_run("job-a@1")
    searchers.reset_runs()

    assert searchers.for_run("job-a@1") is not first


def test_the_binder_hands_the_run_count_to_the_searcher(monkeypatch):
    seen: list[str] = []
    fetch = _over_the_wire([REFUSED] * 3, seen=seen)
    monkeypatch.setattr(searchers, "default_fetch", lambda **_kw: fetch)
    monkeypatch.setattr(
        searchers,
        "for_discogs",
        lambda: searchers.discogs_asker(token=SENT, fetch=fetch, sleep=lambda _s: None),
    )
    monkeypatch.setattr(searchers.time, "sleep", lambda _s: None)
    run = searchers.for_run("job-a@1")
    for n in range(5):
        searchers.for_taxonomy(TAXONOMY, refusals=run)(ARTIST, f"{TITLE} {n}")

    assert _beatport_requests(seen) == 3


# ---------------------------------------------------------------------------
# D. The general catalogue's gate is unchanged
# ---------------------------------------------------------------------------


def _never_asked(isrc: object) -> published.Published:
    raise AssertionError(f"the general catalogue was asked about {isrc!r}")


@pytest.mark.parametrize("stopped", [False, True], ids=["refused", "not-sent"])
def test_deezer_is_still_not_asked_beside_a_blocked_beatport(stopped):
    refusals = searchers.Refusals()
    if stopped:
        _sweep([REFUSED] * 3, refusals=refusals)
    hit = _searcher(_over_the_wire(REFUSED), refusals=refusals)(ARTIST, TITLE)
    assert _beatport(hit).answer == "blocked"

    decided = published.second_opinion(TAXONOMY, lookup=_never_asked)(hit, "USRC17607839")

    (general,) = [one for one in decided.answers if one.source == published.SOURCE]
    assert general.answer == searchers.NOT_ASKED
    assert decided.genre is None
