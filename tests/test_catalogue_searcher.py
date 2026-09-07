"""U1: the catalogue searcher, its network seam, and the two refusals it owes.

WHAT THIS SUITE IS ACTUALLY GUARDING. A tagger that reads a catalogue has one
failure that costs a library and never announces itself: a source that could not
be read reported as a source that had nothing. Every item then completes, the job
reports success, and a folder of untagged files looks exactly like a folder the
catalogues genuinely do not carry. So the properties under test are not "the
parser works". They are the three way distinction between an answer, an absence
and a silence, and the rule that only an absence may decline.

THE SECOND GUARD IS THE RESOLVER. This is the first caller of
``cratekit.core.routing.suggest_tag`` in ``src``, so under
``docs/solutions/workflow-issues/`` under
``adding-the-first-caller-makes-you-the-owner-of-its-unreviewed-defects.md``,
its failure paths are this unit's to drive rather than only its happy path. Three
of them are driven below: an exact refusal, an alias that lands on the fallback
bucket's display, and an alias that resolves to a SUB rather than to its parent
bucket. The third is the whole reason this module calls the shipped resolver
instead of reading ``tagging_alias`` itself, because a bare alias lookup returns
the pair and a caller that renders the bucket loses the sub.

NOTHING HERE OPENS A SOCKET. Every page is synthetic text handed to the injected
fetch seam, and one test detonates the module's own HTTP getter to prove the
injection displaces it rather than sitting beside it.

The fixtures read their genre strings off ``default_taxonomy()`` rather than
typing them, exactly as ``tests/test_genre_retag.py`` does, so a template edit
moves the fixture with it instead of leaving a test asserting about a value
nobody declares any more.
"""

from __future__ import annotations

import ast
import json
import random
from pathlib import Path

import pytest

from cratekit.core import routing
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import default_taxonomy
from cratekit.tagging import searchers

TAXONOMY = default_taxonomy()

#: Every display name the template declares, buckets and subs alike. The source
#: scan at the bottom asserts none of them appears as a literal in the module,
#: which is R19 held at the one layer that is most tempted to break it.
DISPLAYS = frozenset(
    {bucket.display for bucket in TAXONOMY.buckets}
    | {sub.display for bucket in TAXONOMY.buckets for sub in bucket.subs}
)

#: A source string the template declares an outright refusal for, derived the way
#: ``tests/test_routing_parity.py`` derives the same population.
REFUSED = sorted(
    {
        needle
        for rule in TAXONOMY.suggest
        if rule.equals and rule.decline
        for needle in rule.equals
    }
)


def _source_genre_for(*, sub: bool) -> str:
    """A vendor genre string the taxonomy resolves, to a sub or to a bucket.

    A catalogue emits display shaped names, so the display itself is a realistic
    source string, and asking the resolver which way it lands keeps the fixture
    honest when the template moves a genre between the two levels.
    """
    for bucket in TAXONOMY.buckets:
        entries = bucket.subs if sub else (bucket,)
        for entry in entries:
            answer = routing.suggest_tag(TAXONOMY, entry.display)
            if answer.declined or answer.tag != entry.display:
                continue
            if (answer.sub_id is not None) is sub:
                return entry.display
    raise AssertionError("the template declares no genre that resolves at this level")


def _source_genre_aliasing_to_the_fallback() -> str:
    """A vendor string the template aliases onto the fallback bucket's display.

    Read out of the alias table because the alias table is the only place that
    fact lives. Typing the string instead is how a fixture outlives the template
    that justified it, and this one guards AE5, the case where writing the
    resolver's own answer would launder a catch-all onto a file.
    """
    fallback = TAXONOMY.fallback.bucket
    for key, (bucket_id, _sub_id) in TAXONOMY._tagging_alias.items():  # noqa: SLF001
        if bucket_id != fallback:
            continue
        answer = routing.suggest_tag(TAXONOMY, key)
        if not answer.declined and answer.tag and TAXONOMY.is_too_coarse_as_source(answer.tag):
            return key
    raise AssertionError("the template aliases nothing onto the fallback bucket")


BUCKET_GENRE = _source_genre_for(sub=False)
SUB_GENRE = _source_genre_for(sub=True)
FALLBACK_GENRE = _source_genre_aliasing_to_the_fallback()

ARTIST = "Bernard Badie"
TITLE = "Sunrise Mood"


# ---------------------------------------------------------------------------
# Synthetic pages. Every one of these is the shape the module's parser reads,
# built here rather than captured, because a live capture is an attended act and
# U6 records the unverified page shapes as a residual instead.
# ---------------------------------------------------------------------------


def _beatport_track(artist: str, title: str, genre: str, *, mix: str = "") -> dict:
    return {
        "track_name": title,
        "mix_name": mix,
        "artists": [{"artist_name": artist}],
        "genre": [{"genre_name": genre}] if genre else [],
    }


def _beatport_page(tracks: list[dict]) -> str:
    payload = {
        "props": {
            "pageProps": {
                "dehydratedState": {"queries": [{"state": {"data": {"tracks": {"data": tracks}}}}]}
            }
        }
    }
    return (
        '<html><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(payload)
        + "</script></html>"
    )


def _traxsource_page(rows: list[tuple[str, str, str]]) -> str:
    parts = ["<html>"]
    for index, (artist, title, genre) in enumerate(rows, start=1):
        parts.append(
            f'<div data-trid="{index}" class="trk-row">'
            f'<div class="trk-cell title"><a href="#">{title}</a></div>'
            f'<div class="trk-cell artists"><a class="com-artists" href="#">{artist}</a></div>'
            f'<div class="trk-cell genre"><a href="#">{genre}</a></div>'
            "</div>"
        )
    parts.append("</html>")
    return "".join(parts)


BANDCAMP_TRACK_URL = "https://example.bandcamp.com/track/sunrise-mood"


def _bandcamp_search_page(entries: list[tuple[str, str, str, str]]) -> str:
    parts = ["<html><ul>"]
    for url, heading, artist, genre in entries:
        cell = f'<div class="genre"> genre: {genre} </div>' if genre else ""
        parts.append(
            '<li class="searchresult track">'
            f'<div class="heading"><a href="{url}">{heading}</a></div>'
            f'<div class="subhead"> by {artist} </div>'
            f"{cell}</li>"
        )
    parts.append("</ul></html>")
    return "".join(parts)


def _bandcamp_track_page(tags: list[str]) -> str:
    body = "".join(f'<a class="tag" href="#">{tag}</a>' for tag in tags)
    return f"<html>{body}</html>"


UNREACHABLE = searchers.Fetched(note="synthetic transport failure")


def _routed(routes: dict[str, str | searchers.Fetched], seen: list[str] | None = None):
    """A fetch seam that answers by URL prefix and records what it was asked for."""

    def fetch(url: str) -> searchers.Fetched:
        if seen is not None:
            seen.append(url)
        for marker, answer in routes.items():
            if url.startswith(marker) or marker in url:
                return answer if isinstance(answer, searchers.Fetched) else searchers.Fetched(
                    text=answer
                )
        return searchers.Fetched(note=f"no route for {url}")

    return fetch


def _all_three(
    *,
    beatport: str | searchers.Fetched,
    traxsource: str | searchers.Fetched,
    bandcamp: str | searchers.Fetched,
    track_page: str | searchers.Fetched | None = None,
    seen: list[str] | None = None,
):
    routes: dict[str, str | searchers.Fetched] = {}
    if track_page is not None:
        routes["/track/"] = track_page
    routes[searchers.BEATPORT_SEARCH] = beatport
    routes[searchers.TRAXSOURCE_SEARCH] = traxsource
    routes[searchers.BANDCAMP_SEARCH] = bandcamp
    return _routed(routes, seen)


def _searcher(fetch, *, naps: list[float] | None = None, pacing=None):
    return searchers.catalogue_searcher(
        TAXONOMY,
        fetch=fetch,
        sleep=(naps.append if naps is not None else lambda _seconds: None),
        pacing=pacing,
    )


# ---------------------------------------------------------------------------
# A. The walk, and the order it takes
# ---------------------------------------------------------------------------


def test_a_beatport_match_carries_the_tag_the_source_name_and_the_raw_genre():
    """The hit has to name where it came from and what the catalogue actually said.

    Without the raw string a decline downstream can only report that something
    was unmapped, which tells a person nothing about which alias their taxonomy
    is missing. R24 spends that string in the report, so it has to survive the
    resolution rather than being consumed by it.
    """
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre == BUCKET_GENRE
    assert hit.source == searchers.BEATPORT
    assert hit.source_genre == BUCKET_GENRE
    assert hit.art is None


def test_a_beatport_miss_falls_through_to_traxsource_and_the_hit_names_traxsource():
    """The fallback order is behaviour, not an implementation detail.

    A source that answered and had nothing is the one outcome that permits the
    walk to continue, and the hit has to name the source that actually answered
    so a later disagreement between catalogues is traceable to one of them.
    """
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([(ARTIST, TITLE, BUCKET_GENRE)]),
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.source == searchers.TRAXSOURCE
    assert hit.genre == BUCKET_GENRE


def test_an_unreachable_first_source_does_not_stop_the_walk():
    """A silence from one catalogue must not decide the answer for the other two.

    This is the difference between "we could not ask" and "we asked and it did
    not know", held at the one place where collapsing them would be cheapest.
    """
    fetch = _all_three(
        beatport=UNREACHABLE,
        traxsource=_traxsource_page([(ARTIST, TITLE, BUCKET_GENRE)]),
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.source == searchers.TRAXSOURCE


def test_a_bandcamp_match_takes_the_genre_off_the_listing_when_it_carries_one():
    """The third source answers too, and the cheap path costs one fetch.

    A track page fetch that the listing already answered is a second pace wait
    per file for nothing, which over a folder is the difference between a sweep
    that finishes and one somebody kills.
    """
    seen: list[str] = []
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page(
            [(BANDCAMP_TRACK_URL, TITLE, ARTIST, BUCKET_GENRE.lower())]
        ),
        seen=seen,
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.source == searchers.BANDCAMP
    assert hit.genre == BUCKET_GENRE
    assert not [url for url in seen if "/track/" in url]


def test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page():
    """Bandcamp's genre often lives on the track page rather than in the listing.

    Two touches is the honest cost of that source, and each one is paced, so the
    schedule has to grow by one wait rather than the second fetch slipping past
    the pacer.
    """
    naps: list[float] = []
    seen: list[str] = []
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([(BANDCAMP_TRACK_URL, TITLE, ARTIST, "")]),
        track_page=_bandcamp_track_page([BUCKET_GENRE.lower()]),
        seen=seen,
    )
    hit = _searcher(fetch, naps=naps)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre == BUCKET_GENRE
    assert [url for url in seen if "/track/" in url] == [BANDCAMP_TRACK_URL]
    assert len(naps) == len(seen)


# ---------------------------------------------------------------------------
# B. The two refusals, and the decline that is not one
# ---------------------------------------------------------------------------


def test_three_sources_that_all_answered_with_no_match_decline():
    """A decline is a question the next run asks again, which is the promise
    ``tag.py`` already makes about a searcher that returns nothing. Three
    catalogues that answered and did not carry the track is genuine absence, so
    it must not raise and must not be dressed up as a failure.
    """
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([]),
    )
    assert _searcher(fetch)(ARTIST, TITLE) is None


def test_a_source_that_never_answered_raises_rather_than_declining():
    """Three silences is not an absence, and reporting it as one is the merge
    bar's named cost: a clean report over state the tool could not read. The
    refusal has to be typed and carry a remedy about the network.
    """
    fetch = _all_three(beatport=UNREACHABLE, traxsource=UNREACHABLE, bandcamp=UNREACHABLE)
    with pytest.raises(CratekitError) as raised:
        _searcher(fetch)(ARTIST, TITLE)
    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.remediation.remedy is Remedy.RETRY_LATER
    assert sorted(cause.detail["sources"]) == sorted(searchers.SOURCES)


def test_one_source_that_answered_holds_back_the_refusal():
    """Two silences and one absence is still an absence, because a catalogue did
    answer. Raising here would turn an ordinary bootleg into a failed job every
    time one of three sites was down.
    """
    fetch = _all_three(
        beatport=UNREACHABLE,
        traxsource=UNREACHABLE,
        bandcamp=_bandcamp_search_page([]),
    )
    assert _searcher(fetch)(ARTIST, TITLE) is None


def test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal():
    """AE6. A markup change is a defect in this product wearing a network
    failure's clothes. Folding it into the unreachable refusal sends somebody to
    their router over a broken parser, and it is a permanent state carrying a
    transient remedy, so it gets its own reason and names the source.
    """
    fetch = _all_three(
        beatport="<html>a page this parser has never seen</html>",
        traxsource=UNREACHABLE,
        bandcamp=UNREACHABLE,
    )
    with pytest.raises(CratekitError) as raised:
        _searcher(fetch)(ARTIST, TITLE)
    cause = raised.value.cause
    assert cause.reason == searchers.PARSE_BREAK_REASON
    assert cause.reason != searchers.UNREACHABLE_REASON
    assert cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert cause.detail["sources"] == [searchers.BEATPORT]
    assert searchers.BEATPORT in " ".join(cause.remediation.steps)


def test_a_traxsource_page_holding_rows_the_parser_cannot_read_is_a_parse_break():
    """The parse break is claimed on POSITIVE evidence: result rows are present
    and the parser read none of them. An empty result set carries no rows at all
    and stays a miss, which is what keeps an unsold bootleg from being reported
    as a defect in this software.
    """
    broken = '<html><div data-trid="1" class="trk-row"><span>moved</span></div></html>'
    fetch = _all_three(beatport=UNREACHABLE, traxsource=broken, bandcamp=UNREACHABLE)
    with pytest.raises(CratekitError) as raised:
        _searcher(fetch)(ARTIST, TITLE)
    assert raised.value.cause.reason == searchers.PARSE_BREAK_REASON
    assert raised.value.cause.detail["sources"] == [searchers.TRAXSOURCE]


def test_a_traxsource_page_with_no_rows_at_all_is_a_miss_rather_than_a_parse_break():
    """The other half of the same rule, and the one that keeps the first half
    safe to ship: a search that legitimately found nothing must not be reported
    as a scraper that broke.
    """
    fetch = _all_three(
        beatport=UNREACHABLE,
        traxsource=_traxsource_page([]),
        bandcamp=UNREACHABLE,
    )
    assert _searcher(fetch)(ARTIST, TITLE) is None


# ---------------------------------------------------------------------------
# C. Resolution through the shipped resolver
# ---------------------------------------------------------------------------


def test_a_source_genre_that_aliases_to_a_sub_resolves_to_the_subs_display():
    """This is the whole reason the module calls ``suggest_tag`` rather than
    reading ``tagging_alias`` itself. The alias answers a (bucket, sub) pair, and
    a caller that renders the bucket writes the parent's name onto a track the
    taxonomy places one level deeper.
    """
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, SUB_GENRE)]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    answer = routing.suggest_tag(TAXONOMY, SUB_GENRE)
    assert answer.sub_id is not None
    assert hit.genre == SUB_GENRE
    assert hit.genre != TAXONOMY.bucket(answer.bucket_id).display


@pytest.mark.parametrize("refused", REFUSED)
def test_a_source_genre_the_taxonomy_refuses_outright_declines(refused: str):
    """The template names these strings because they are catch-all buckets from
    a source taxonomy. Accepting one as a final tag is the blanket genre bug the
    tagging entry point exists to prevent, and it must be prevented at the point
    of first contact rather than at the write.
    """
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, refused)]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre is None
    assert hit.source_genre == refused


def test_a_source_genre_that_aliases_to_the_fallback_bucket_declines():
    """AE5. The resolver answers with the fallback bucket's display, which is a
    value ``retag.py`` refuses at its own write for the stated reason: writing it
    launders a catch-all into a value the corrective verb would never select
    again, and the two tagging verbs would then bounce the file for ever.
    """
    answer = routing.suggest_tag(TAXONOMY, FALLBACK_GENRE)
    assert not answer.declined and answer.tag
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, FALLBACK_GENRE)]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre is None
    assert hit.source_genre == FALLBACK_GENRE


def test_a_matched_track_whose_genre_is_declined_still_names_the_raw_string():
    """A decline that cannot say what it declined is a decline nobody can act
    on. AE1 spends this string in the item artifact and in the verb's report, so
    it has to reach the caller alongside the source that supplied it.
    """
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, REFUSED[0])]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre is None
    assert hit.source == searchers.BEATPORT
    assert hit.source_genre == REFUSED[0]


def test_a_source_genre_with_surrounding_whitespace_resolves_the_same_as_the_trimmed_one():
    """Scraped text arrives with whatever the markup put around it, and a lookup
    that misses on a leading space degrades to a decline that looks exactly like
    a taxonomy gap. The raw string is preserved untrimmed, because it is what the
    page said.
    """
    padded = f"  {BUCKET_GENRE}\n"
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, padded)]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre == BUCKET_GENRE


# ---------------------------------------------------------------------------
# D. Pacing and the rate limit
# ---------------------------------------------------------------------------


def test_the_pacer_sleeps_before_every_fetch_including_the_first():
    """A fresh process holds no memory of the last run, so a pacer that waits
    only BETWEEN touches opens every run with a burst. Over a folder of a
    thousand files that burst is what gets an address rate limited.
    """
    naps: list[float] = []
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([]),
    )
    _searcher(fetch, naps=naps)(ARTIST, TITLE)
    assert len(naps) == 3
    assert all(nap >= searchers.MIN_INTERVAL_S for nap in naps)


def test_jitter_is_drawn_from_the_injected_random_source():
    """Two runs that started together and wait the same fixed interval stay in
    step for ever, which is how a shared rate limit produces a shared retry. The
    entropy is injected so the schedule is reproducible under a seed and
    assertable without waiting it.
    """

    def schedule(seed: int) -> list[float]:
        naps: list[float] = []
        pacer = searchers.Pacer(entropy=random.Random(seed), sleep=naps.append)
        fetch = _all_three(
            beatport=_beatport_page([]),
            traxsource=_traxsource_page([]),
            bandcamp=_bandcamp_search_page([]),
        )
        _searcher(fetch, pacing=pacer)(ARTIST, TITLE)
        return naps

    assert schedule(1) == schedule(1)
    assert schedule(1) != schedule(2)
    assert len(set(schedule(1))) > 1


def test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew():
    """The rate limit answer is a wait, not a failure, and the wait has to grow
    or the retry arrives inside the same window that refused the first request.
    Driven through the injected getter so the thirty second base is asserted
    rather than endured.
    """
    waits: list[float] = []
    replies = iter([_Response(429), _Response(429), _Response(200, "ok")])
    fetch = searchers.default_fetch(
        get=lambda url, headers, timeout: next(replies), sleep=waits.append
    )
    page = fetch("https://example.test/search")
    assert page.text == "ok"
    assert waits == [searchers.RATE_LIMIT_BASE_WAIT_S, searchers.RATE_LIMIT_BASE_WAIT_S * 2]


def test_a_source_that_spends_its_attempts_on_429_is_unreachable():
    """An exhausted rate limit is a source that never answered, so it must not
    contribute a miss. It is also the one shape where an unbounded retry looks
    like progress, which is why the cap exists and why the last refusal does not
    sleep again on its way out.
    """
    waits: list[float] = []
    calls: list[str] = []

    def get(url, headers, timeout):
        calls.append(url)
        return _Response(429)

    fetch = searchers.default_fetch(get=get, sleep=waits.append)
    page = fetch("https://example.test/search")
    assert page.text is None
    assert len(calls) == searchers.RATE_LIMIT_ATTEMPTS
    assert len(waits) == searchers.RATE_LIMIT_ATTEMPTS - 1


def test_a_non_200_other_than_429_is_unreachable_rather_than_a_miss():
    """R22's classification, at the one boundary where the wrong answer is
    invisible: a 503 that read as "the catalogue does not carry this track"
    would let a whole outage complete as a clean sweep.
    """
    fetch = searchers.default_fetch(
        get=lambda url, headers, timeout: _Response(503), sleep=lambda _s: None
    )
    page = fetch("https://example.test/search")
    assert page.text is None
    assert "503" in page.note


def test_a_transport_failure_is_unreachable_rather_than_a_miss():
    """The same rule for the case that never reaches a status code at all. A
    getter that raises is the commonest shape of an unreachable source and the
    easiest one to swallow into a bare except that returns nothing.
    """

    def get(url, headers, timeout):
        raise OSError("no route to host")

    fetch = searchers.default_fetch(get=get, sleep=lambda _s: None)
    page = fetch("https://example.test/search")
    assert page.text is None
    assert "no route to host" in page.note


def test_the_default_fetch_passes_its_timeout_to_the_http_getter():
    """A fetch with no timeout blocks for ever, and nothing else in this suite
    would notice: the run simply never returns. The VALUE is asserted rather than
    its presence, because a timeout of zero and a timeout of fifteen seconds are
    the same shape and different products.
    """
    seen: dict[str, object] = {}

    def get(url, headers, timeout):
        seen["timeout"] = timeout
        seen["headers"] = headers
        return _Response(200, "ok")

    searchers.default_fetch(get=get, sleep=lambda _s: None)("https://example.test/search")
    assert seen["timeout"] == searchers.REQUEST_TIMEOUT_S
    assert seen["headers"] is searchers.HEADERS


# ---------------------------------------------------------------------------
# E. The seam, the binder, and the rule the module has to keep
# ---------------------------------------------------------------------------


def test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url():
    """A title carrying an ampersand or a space builds a URL that either escapes
    it or silently truncates the query at the first delimiter, which returns the
    wrong page and reports it as a miss.
    """
    seen: list[str] = []
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([]),
        seen=seen,
    )
    _searcher(fetch)("Fred & Ginger", "Trois / Quatre?")
    first = seen[0]
    assert first.startswith(searchers.BEATPORT_SEARCH)
    assert " " not in first
    assert "%26" in first and "%2F" in first and "%3F" in first


def test_the_injected_seam_displaces_the_real_http_getter(monkeypatch):
    """R18's proof at this layer. An injected fetch that sits BESIDE the real
    getter rather than replacing it passes every other test here and opens a
    socket in production for every file.
    """

    def detonate(*args, **kwargs):
        raise AssertionError("the suite reached the network")

    monkeypatch.setattr(searchers, "_requests_get", detonate)
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)]),
        traxsource="",
        bandcamp="",
    )
    assert _searcher(fetch)(ARTIST, TITLE) is not None


def test_the_binder_hands_back_a_searcher_without_touching_the_network(monkeypatch):
    """KTD11. A worker looks its searcher up here rather than constructing one,
    so a test can substitute a fake by patching this module. Building one must
    stay free of network work, because the binder is called per item.
    """

    def detonate(*args, **kwargs):
        raise AssertionError("the binder reached the network")

    monkeypatch.setattr(searchers, "_requests_get", detonate)
    bound = searchers.for_taxonomy(TAXONOMY)
    assert callable(bound)


def test_the_module_names_no_declared_genre_display():
    """R19, asserted over the source rather than trusted. This module is the most
    tempted place in the repository to paste a vendor to folder map, because the
    system it replaces has one, and a map pasted here works for one library and
    quietly does nothing in the next.
    """
    source = Path(searchers.__file__).read_text(encoding="utf-8")
    literals = {
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    assert not literals & DISPLAYS


class _Response:
    """The two attributes this module reads off an HTTP response, and no more.

    Defined as the last thing in the file on purpose: it is a fixture for the
    default fetch's tests rather than a description of anything the module owns,
    and the module's own contract with a getter is exactly these two fields.
    """

    def __init__(self, status_code: int, text: str = "") -> None:
        self.status_code = status_code
        self.text = text
