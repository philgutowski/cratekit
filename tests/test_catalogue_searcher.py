"""U1: the catalogue searcher, its network seam, and the two refusals it owes.

A source that could not be read must not report nothing, so what is tested is
an answer, an absence and a silence, and that only an absence may decline. No
socket is opened, and genres come from ``default_taxonomy()``.
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
from cratekit.core.taxonomy import default_taxonomy, load_taxonomy
from cratekit.tagging import catalogues, discogs, searchers, shops

TAXONOMY = default_taxonomy()

#: Every display name the template declares, buckets and subs alike, which no
#: catalogue module may hold as a literal (R19).
DISPLAYS = frozenset(
    {bucket.display for bucket in TAXONOMY.buckets}
    | {sub.display for bucket in TAXONOMY.buckets for sub in bucket.subs}
)

#: A source string the template declares an outright refusal for.
REFUSED = sorted(
    {
        needle
        for rule in TAXONOMY.suggest
        if rule.equals and rule.decline
        for needle in rule.equals
    }
)


def _source_genre_for(*, sub: bool) -> str:
    """A vendor genre string the taxonomy resolves, to a sub or to a bucket, as asked."""
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
    """A vendor string aliased onto the fallback bucket's display, read out of the
    alias table so it cannot outlive the template (AE5)."""
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


class _Response:
    """The attributes this module reads off an HTTP response: ``text`` and ``content``."""

    def __init__(self, status_code: int, text: str = "", *, content: bytes = b"") -> None:
        self.status_code = status_code
        self.text = text
        self.content = content


# Synthetic pages in the shapes the parsers read; live captures are attended.


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

#: A listing thumbnail, ``_7``; the searcher asks for ``_10``, the original.
BANDCAMP_LISTING_ART = "https://f4.bcbits.com/img/a0123456789_7.jpg"
BANDCAMP_PAGE_ART = "https://f4.bcbits.com/img/a0123456789_5.jpg"
BANDCAMP_ORIGINAL = "https://f4.bcbits.com/img/a0123456789_10.jpg"


def _bandcamp_search_page(
    entries: list[tuple[str, str, str, str]], *, art: str | None = BANDCAMP_LISTING_ART
) -> str:
    parts = ["<html><ul>"]
    for url, heading, artist, genre in entries:
        cell = f'<div class="genre"> genre: {genre} </div>' if genre else ""
        picture = f'<div class="art"><img src="{art}" class="thumb"></div>' if art else ""
        parts.append(
            '<li class="searchresult track">'
            f"{picture}"
            f'<div class="heading"><a href="{url}">{heading}</a></div>'
            f'<div class="subhead"> by {artist} </div>'
            f"{cell}</li>"
        )
    parts.append("</ul></html>")
    return "".join(parts)


def _bandcamp_track_page(tags: list[str], *, og_image: str | None = None) -> str:
    head = f'<meta property="og:image" content="{og_image}">' if og_image else ""
    body = "".join(f'<a class="tag" href="#">{tag}</a>' for tag in tags)
    return f"<html><head>{head}</head>{body}</html>"


UNREACHABLE = searchers.Fetched(note="synthetic transport failure")
EMPTY_BEATPORT = _beatport_page([])
EMPTY_TRAXSOURCE = _traxsource_page([])
EMPTY_BANDCAMP = _bandcamp_search_page([])
#: A Bandcamp listing for the track that names no genre, so its page is read.
GENRELESS_LISTING = _bandcamp_search_page([(BANDCAMP_TRACK_URL, TITLE, ARTIST, "")])


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
    beatport: str | searchers.Fetched = EMPTY_BEATPORT,
    traxsource: str | searchers.Fetched = EMPTY_TRAXSOURCE,
    bandcamp: str | searchers.Fetched = EMPTY_BANDCAMP,
    track_page: str | searchers.Fetched | None = None,
    seen: list[str] | None = None,
):
    """The three shops' search pages, each an empty result unless named."""
    routes: dict[str, str | searchers.Fetched] = {}
    if track_page is not None:
        routes["/track/"] = track_page
    routes[searchers.BEATPORT_SEARCH] = beatport
    routes[searchers.TRAXSOURCE_SEARCH] = traxsource
    routes[searchers.BANDCAMP_SEARCH] = bandcamp
    return _routed(routes, seen)


def _no_hit(hit) -> bool:
    """True for the decline every source asked earned by answering MISS, a hit
    with no genre, not None, since R-791."""
    return (
        hit is not None
        and hit.genre is None
        and hit.source == ""
        and hit.unread == ()
        and len(hit.answers) == len(searchers.SCRAPED_WALK)
    )


def _searcher(fetch, *, naps: list[float] | None = None, pacing=None):
    """The searcher over the scraped walk, which keeps the two shop parsers driven."""
    return searchers.catalogue_searcher(
        TAXONOMY,
        fetch=fetch,
        sleep=(naps.append if naps is not None else lambda _seconds: None),
        pacing=pacing,
        walk=searchers.SCRAPED_WALK,
    )


def _hit(*, naps: list[float] | None = None, pacing=None, **pages):
    """The scraped walk's hit for ARTIST and TITLE over :func:`_all_three`'s pages."""
    return _searcher(_all_three(**pages), naps=naps, pacing=pacing)(ARTIST, TITLE)


def _row(genre: str, *, artist: str = ARTIST, title: str = TITLE) -> str:
    """A Beatport page of one row for the track, carrying ``genre``."""
    return _beatport_page([_beatport_track(artist, title, genre)])


def _track_pages(seen: list[str]) -> list[str]:
    return [url for url in seen if "/track/" in url]


# A. The walk, and the order it takes


def test_a_beatport_match_carries_the_tag_the_source_name_and_the_raw_genre():
    """The hit names where it came from and the raw string, which R24's report spends."""
    hit = _hit(beatport=_row(BUCKET_GENRE))
    assert hit is not None
    assert hit.genre == BUCKET_GENRE
    assert hit.source == searchers.BEATPORT
    assert hit.source_genre == BUCKET_GENRE
    assert hit.art_url == "", "a row naming no release picture names no picture"


@pytest.mark.parametrize("beatport", [EMPTY_BEATPORT, UNREACHABLE], ids=["miss", "unreachable"])
def test_a_beatport_miss_or_silence_falls_through_to_traxsource_which_names_itself(beatport):
    """A silence from one catalogue must not decide the answer for the others.
    Traxsource names no picture, which is parity."""
    hit = _hit(beatport=beatport, traxsource=_traxsource_page([(ARTIST, TITLE, BUCKET_GENRE)]))
    assert hit is not None
    assert hit.source == searchers.TRAXSOURCE
    assert hit.genre == BUCKET_GENRE
    assert hit.art_url == ""


def test_a_bandcamp_listing_genre_costs_one_fetch_and_its_picture_is_the_original():
    """A track page the listing already answered is a pace wait for nothing."""
    seen: list[str] = []
    listing = [(BANDCAMP_TRACK_URL, TITLE, ARTIST, BUCKET_GENRE.lower())]
    hit = _hit(bandcamp=_bandcamp_search_page(listing), seen=seen)
    assert hit is not None
    assert hit.source == searchers.BANDCAMP
    assert hit.genre == BUCKET_GENRE
    assert hit.art_url == BANDCAMP_ORIGINAL
    assert not _track_pages(seen)


def test_a_bandcamp_listing_with_no_genre_spends_a_second_fetch_on_the_track_page():
    """The genre on the track page costs one more paced wait, never an unpaced fetch."""
    naps: list[float] = []
    seen: list[str] = []
    hit = _hit(
        bandcamp=GENRELESS_LISTING,
        track_page=_bandcamp_track_page([BUCKET_GENRE.lower()]),
        seen=seen,
        naps=naps,
    )
    assert hit is not None
    assert hit.genre == BUCKET_GENRE
    assert _track_pages(seen) == [BANDCAMP_TRACK_URL]
    assert len(naps) == len(seen)


# B. The two refusals, and the decline that is not one


def test_three_sources_that_all_answered_with_no_match_decline():
    """Three catalogues that answered and did not carry the track is absence, a
    decline the next run asks again, never a failure."""
    hit = _hit()
    assert _no_hit(hit)
    assert [said.answer for said in hit.answers] == ["miss"] * 3


def test_a_source_that_never_answered_raises_rather_than_declining():
    """Three silences is not an absence: the refusal is typed and names the network."""
    with pytest.raises(CratekitError) as raised:
        _hit(beatport=UNREACHABLE, traxsource=UNREACHABLE, bandcamp=UNREACHABLE)
    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.remediation.remedy is Remedy.RETRY_LATER
    assert sorted(cause.detail["sources"]) == sorted(searchers.SCRAPED_WALK)


def test_one_source_that_answered_holds_back_the_refusal():
    """A catalogue did answer, so an ordinary bootleg is no failed job."""
    hit = _hit(beatport=UNREACHABLE, traxsource=UNREACHABLE)
    assert hit is not None and hit.genre is None and hit.source == ""
    assert hit.unread == (searchers.BEATPORT, searchers.TRAXSOURCE)


@pytest.mark.parametrize(
    ("pages", "source"),
    [
        ({"beatport": "<html>a page this parser has never seen</html>"}, searchers.BEATPORT),
        (
            {
                "beatport": UNREACHABLE,
                "traxsource": '<html><div data-trid="1" class="trk-row"><span>moved</span>'
                "</div></html>",
            },
            searchers.TRAXSOURCE,
        ),
    ],
    ids=["beatport payload missing", "traxsource rows unread"],
)
def test_a_page_that_parsed_to_nothing_recognizable_raises_its_own_refusal(pages, source):
    """AE6. A markup change is a permanent defect, not the network's transient remedy;
    a shop row parser claims it only when rows are present and none read."""
    with pytest.raises(CratekitError) as raised:
        _hit(**{"traxsource": UNREACHABLE, "bandcamp": UNREACHABLE, **pages})
    cause = raised.value.cause
    assert cause.reason == searchers.PARSE_BREAK_REASON
    assert cause.reason != searchers.UNREACHABLE_REASON
    assert cause.remediation.remedy is Remedy.REPORT_DEFECT
    assert cause.detail["sources"] == [source]
    assert source in " ".join(cause.remediation.steps)


def test_a_traxsource_page_with_no_rows_at_all_is_a_miss_rather_than_a_parse_break():
    """A search that found nothing must not be reported as a scraper that broke."""
    hit = _hit(beatport=UNREACHABLE, bandcamp=UNREACHABLE)
    assert hit is not None and hit.genre is None
    assert [said.answer for said in hit.answers] == ["unreachable", "miss", "unreachable"]


# C. Resolution through the shipped resolver


def test_a_source_genre_that_aliases_to_a_sub_resolves_to_the_subs_display():
    """The reason the module calls ``suggest_tag``: a bare alias lookup's caller
    rendering the bucket writes the parent's name."""
    hit = _hit(beatport=_row(SUB_GENRE))
    assert hit is not None
    answer = routing.suggest_tag(TAXONOMY, SUB_GENRE)
    assert answer.sub_id is not None
    assert hit.genre == SUB_GENRE
    assert hit.genre != TAXONOMY.bucket(answer.bucket_id).display


@pytest.mark.parametrize("word", [*REFUSED, FALLBACK_GENRE])
def test_a_genre_refused_outright_or_aliased_to_the_fallback_declines_naming_it(word: str):
    """A catch-all accepted as a final tag is the blanket genre bug (AE5); the decline
    names the source and the raw string (AE1)."""
    hit = _hit(beatport=_row(word))
    assert hit is not None
    assert hit.genre is None
    assert hit.source == searchers.BEATPORT
    assert hit.source_genre == word


def test_the_resolver_fixtures_still_reach_the_tiers_they_name():
    assert routing.suggest_tag(TAXONOMY, "gqom").off_taxonomy is True
    declared = routing.suggest_tag(TAXONOMY, "melodic techno")
    assert declared.bucket_id is None and declared.tag and not declared.declined


@pytest.mark.parametrize(
    ("word", "written", "flagged"),
    [
        ("gqom", "gqom", True),
        ("melodic techno", routing.suggest_tag(TAXONOMY, "melodic techno").tag, False),
        (f"  {BUCKET_GENRE}\n", BUCKET_GENRE, None),
    ],
    ids=["unknown word", "declared tag with no bucket", "padded genre"],
)
def test_a_genre_resolves_to_what_is_written_and_flags_only_the_unknown(word, written, flagged):
    """R-650: the last tier's word reaches the file and says it was that word. A
    padded string resolves as the trimmed one."""
    hit = _hit(beatport=_row(word))
    assert hit is not None
    assert hit.genre == written
    if flagged is not None:
        assert hit.off_taxonomy is flagged


def test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline():
    """One file gets one disposition, and a decline outranks the flag, under a
    taxonomy a person can make."""
    template = (
        Path(__file__).parent / "taxonomies" / "second.toml"
    ).read_text(encoding="utf-8")
    edited = template.replace(
        'too_coarse_as_source = ["", "Misc"]',
        'too_coarse_as_source = ["", "Misc", "Bootleg"]',
    )
    assert edited != template
    other = load_taxonomy(edited)
    answer = routing.suggest_tag(other, "Bootleg")
    assert (answer.off_taxonomy, answer.tag) == (True, "Bootleg")
    assert other.is_too_coarse_as_source("Bootleg")

    hit = searchers.catalogue_searcher(
        other,
        fetch=_all_three(beatport=_row("Bootleg")),
        sleep=lambda _seconds: None,
        walk=searchers.SCRAPED_WALK,
    )(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre is None
    assert hit.off_taxonomy is False
    assert hit.source_genre == "Bootleg"


# D. Pacing and the rate limit


def test_the_pacer_sleeps_before_every_fetch_including_the_first():
    """A pacer waiting only BETWEEN touches opens every run with a burst."""
    naps: list[float] = []
    _hit(naps=naps)
    assert len(naps) == 3
    assert all(nap >= searchers.MIN_INTERVAL_S for nap in naps)


def test_jitter_is_drawn_from_the_injected_random_source():
    """Runs waiting one fixed interval stay in step, a shared limit's shared retry."""

    def schedule(seed: int) -> list[float]:
        naps: list[float] = []
        _hit(pacing=searchers.Pacer(entropy=random.Random(seed), sleep=naps.append))
        return naps

    assert schedule(1) == schedule(1)
    assert schedule(1) != schedule(2)
    assert len(set(schedule(1))) > 1


def test_a_source_answering_429_twice_then_200_succeeds_and_the_backoff_grew():
    """A rate limit is a wait that grows, or the retry lands in the refusing window."""
    waits: list[float] = []
    replies = iter([_Response(429), _Response(429), _Response(200, "ok")])
    fetch = searchers.default_fetch(
        get=lambda url, headers, timeout: next(replies), sleep=waits.append
    )
    page = fetch("https://example.test/search")
    assert page.text == "ok"
    assert waits == [searchers.RATE_LIMIT_BASE_WAIT_S, searchers.RATE_LIMIT_BASE_WAIT_S * 2]


def test_a_source_that_spends_its_attempts_on_429_is_unreachable():
    """A spent rate limit is no miss, capped, with no sleep after the last refusal."""
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


def _no_route(url, headers, timeout):
    raise OSError("no route to host")


@pytest.mark.parametrize(
    ("get", "named"),
    [(lambda url, headers, timeout: _Response(503), "503"), (_no_route, "no route to host")],
    ids=["503", "transport failure"],
)
def test_a_non_200_or_a_transport_failure_is_unreachable_rather_than_a_miss(get, named):
    """R22: a 503 or a raise read as "not carried" completes an outage clean."""
    page = searchers.default_fetch(get=get, sleep=lambda _s: None)("https://example.test/search")
    assert page.text is None
    assert named in page.note


def test_the_default_fetch_passes_its_timeout_to_the_http_getter():
    """A fetch with no timeout blocks for ever; the VALUE is asserted."""
    seen: dict[str, object] = {}

    def get(url, headers, timeout):
        seen["timeout"] = timeout
        seen["headers"] = headers
        return _Response(200, "ok")

    searchers.default_fetch(get=get, sleep=lambda _s: None)("https://example.test/search")
    assert seen["timeout"] == searchers.REQUEST_TIMEOUT_S
    assert seen["headers"] is searchers.HEADERS


# E. The seam, the binders, and the rule the module has to keep


def test_an_artist_and_title_that_need_escaping_reach_the_seam_as_a_quoted_url():
    """An unescaped ampersand truncates the query and reports another page as a miss."""
    seen: list[str] = []
    _searcher(_all_three(seen=seen))("Fred & Ginger", "Trois / Quatre?")
    first = seen[0]
    assert first.startswith(searchers.BEATPORT_SEARCH)
    assert " " not in first
    assert "%26" in first and "%2F" in first and "%3F" in first


def test_the_injected_seam_and_the_binders_never_reach_the_http_getter(monkeypatch):
    """R18 and KTD11: an injected fetch displaces the real getter rather than sitting
    beside it, and a worker's binders build without touching the network."""

    def detonate(*args, **kwargs):
        raise AssertionError("the suite reached the network")

    monkeypatch.setattr(searchers, "_requests_get", detonate)
    assert _hit(beatport=_row(BUCKET_GENRE)) is not None
    assert callable(searchers.for_taxonomy(TAXONOMY))
    assert callable(searchers.for_images())


@pytest.mark.parametrize("module", [searchers, catalogues, discogs, shops])
def test_the_module_names_no_declared_genre_display(module):
    """R19 over the source: a vendor to folder map pasted here works for one
    library and quietly does nothing in the next."""
    source = Path(module.__file__).read_text(encoding="utf-8")
    literals = {
        node.value
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    assert not literals & DISPLAYS


# F. U85: the picture rides the genre's row, and is fetched on the same terms

BEATPORT_ART = "https://geo-media.beatport.com/image_size/250x250/cover-one.jpg"
OTHER_ART = "https://geo-media.beatport.com/image_size/250x250/cover-two.jpg"


def _with_art(track: dict, uri: str) -> dict:
    return {**track, "release": {"release_image_uri": uri}}


def _beatport_only(tracks: list[dict]):
    return _all_three(beatport=_beatport_page(tracks), traxsource="", bandcamp="")


def test_a_beatport_hit_carries_its_release_picture_resized_to_the_source_edge():
    fetch = _beatport_only([_with_art(_beatport_track(ARTIST, TITLE, BUCKET_GENRE), BEATPORT_ART)])
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.art_url == "https://geo-media.beatport.com/image_size/1400x1400/cover-one.jpg"


def test_the_picture_comes_off_the_same_row_as_the_genre_and_never_another():
    """A cover from a different row is the wrong cover: the third row loses and is
    scanned last, so a picture read off the final row shows."""
    genreless = _with_art(_beatport_track(ARTIST, TITLE, ""), OTHER_ART)
    winner = _with_art(_beatport_track(ARTIST, TITLE, BUCKET_GENRE), BEATPORT_ART)
    loser = _with_art(_beatport_track(ARTIST, f"{TITLE} Reprise Dub", SUB_GENRE), OTHER_ART)

    hit = _searcher(_beatport_only([genreless, winner, loser]))(ARTIST, TITLE)

    assert hit is not None
    assert hit.source_genre == BUCKET_GENRE
    assert hit.art_url.endswith("/image_size/1400x1400/cover-one.jpg")


def test_a_row_whose_artist_does_not_match_lends_neither_genre_nor_picture():
    stranger = _with_art(_beatport_track("Somebody Else", TITLE, BUCKET_GENRE), BEATPORT_ART)
    hit = _hit(beatport=_beatport_page([stranger]))
    assert _no_hit(hit)
    assert hit.art_url == ""


@pytest.mark.parametrize("uri", ["", "file:///etc/passwd", "javascript:alert(1)", 7])
def test_a_release_picture_that_is_not_a_web_address_is_no_picture(uri):
    fetch = _beatport_only([_with_art(_beatport_track(ARTIST, TITLE, BUCKET_GENRE), uri)])
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None and hit.genre == BUCKET_GENRE
    assert hit.art_url == ""


def test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image():
    naps: list[float] = []
    seen: list[str] = []
    hit = _hit(
        bandcamp=_bandcamp_search_page(
            [(BANDCAMP_TRACK_URL, TITLE, ARTIST, BUCKET_GENRE.lower())], art=None
        ),
        track_page=_bandcamp_track_page(["gqom"], og_image=BANDCAMP_PAGE_ART),
        seen=seen,
        naps=naps,
    )
    assert hit is not None
    assert hit.genre == BUCKET_GENRE, "the listing's genre wins over the page's tags"
    assert hit.art_url == BANDCAMP_ORIGINAL
    assert _track_pages(seen) == [BANDCAMP_TRACK_URL]
    assert len(naps) == len(seen), "the page touch was not paced"


def test_the_image_fetch_is_paced_and_answers_the_bytes():
    naps: list[float] = []
    calls: list[str] = []

    def get(url, headers, timeout):
        calls.append(url)
        assert len(naps) == 1, "the pace wait must come before the request"
        return _Response(200, content=b"\xff\xd8picture")

    fetch_image = searchers.default_image_fetch(get=get, sleep=naps.append)

    assert fetch_image("https://example.test/cover.jpg") == b"\xff\xd8picture"
    assert calls == ["https://example.test/cover.jpg"]
    assert searchers.MIN_INTERVAL_S <= naps[0] <= searchers.MIN_INTERVAL_S * 1.5


@pytest.mark.parametrize(
    "get",
    [
        lambda url, headers, timeout: _Response(404, content=b"page"),
        lambda url, headers, timeout: _Response(500, content=b"page"),
        _no_route,
    ],
    ids=["404", "500", "transport failure"],
)
def test_an_image_that_cannot_be_had_is_none_rather_than_a_refusal(get):
    fetch_image = searchers.default_image_fetch(get=get, sleep=lambda _s: None)
    assert fetch_image("https://example.test/cover.jpg") is None


def test_an_image_fetch_that_meets_a_rate_limit_backs_off_like_a_search():
    waits: list[float] = []
    replies = iter([_Response(429), _Response(200, content=b"bytes")])
    pacer = searchers.Pacer(sleep=lambda _s: None)
    fetch_image = searchers.default_image_fetch(
        get=lambda url, headers, timeout: next(replies), sleep=waits.append, pacing=pacer
    )

    assert fetch_image("https://example.test/cover.jpg") == b"bytes"
    assert waits == [searchers.RATE_LIMIT_BASE_WAIT_S]


# R-791. A bot challenge is its own answer, and no-hit needs every source's MISS.
# The pages are the two measured on 2026-10-01, reduced, served through the
# shipped ``default_fetch``.

CLOUDFLARE_INTERSTITIAL = (
    '<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title>'
    '<meta http-equiv="refresh" content="390"></head><body>'
    "<script>window._cf_chl_opt={}</script>"
    '<script src="/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1"></script>'
    "</body></html>"
)
BANDCAMP_CLIENT_CHALLENGE = (
    "<!DOCTYPE html><html><head><title>Client Challenge</title></head>"
    '<body><div id="loading-error" hidden>A required part of this site '
    "couldn't load.</div><script src=\"/challenge.js\"></script></body></html>"
)


def _over_the_wire(routes: dict[str, _Response], seen: list[str] | None = None):
    """The shipped searcher over the shipped fetch, with a getter answering by URL."""

    def get(url, headers, timeout):
        if seen is not None:
            seen.append(url)
        for marker, reply in routes.items():
            if url.startswith(marker) or marker in url:
                return reply
        raise OSError(f"no route for {url}")

    fetch = searchers.default_fetch(get=get, sleep=lambda _s: None)
    return _searcher(fetch)


def _wire(*, seen=None, track=None, title=TITLE, beatport=None, traxsource=None, bandcamp=None):
    """The hit over the wire, each shop answering an empty 200 unless named."""
    routes = {} if track is None else {"/track/": track}
    routes[searchers.BEATPORT_SEARCH] = beatport or _Response(200, EMPTY_BEATPORT)
    routes[searchers.TRAXSOURCE_SEARCH] = traxsource or _Response(200, EMPTY_TRAXSOURCE)
    routes[searchers.BANDCAMP_SEARCH] = bandcamp or _Response(200, EMPTY_BANDCAMP)
    return _over_the_wire(routes, seen)(ARTIST, title)


def _said(hit) -> list[tuple[str, str]]:
    return [(said.source, said.answer) for said in hit.answers]


def test_a_bandcamp_client_challenge_page_is_blocked_rather_than_a_miss():
    """A 200 with no rows is no empty result when its title is a bot check; read
    as one, Bandcamp reported MISS on every file."""
    hit = _wire(bandcamp=_Response(200, BANDCAMP_CLIENT_CHALLENGE))
    assert hit.genre is None and hit.source == ""
    assert _said(hit) == [
        (searchers.BEATPORT, "miss"),
        (searchers.TRAXSOURCE, "miss"),
        (searchers.BANDCAMP, "blocked"),
    ]
    assert hit.unread == (searchers.BANDCAMP,)
    assert "Client Challenge" in hit.answers[2].note


@pytest.mark.parametrize(
    ("reply", "word"),
    [
        (_Response(403, CLOUDFLARE_INTERSTITIAL), "blocked"),
        (_Response(200, CLOUDFLARE_INTERSTITIAL), "blocked"),
        (_Response(429), "blocked"),
        (
            _Response(200, CLOUDFLARE_INTERSTITIAL.replace("Just a moment...", "Verifying")),
            "blocked",
        ),
        (_Response(503), "unreachable"),
    ],
    ids=["403 interstitial", "title on a 200", "spent 429", "challenge script", "503 outage"],
)
def test_a_fallbacks_refusal_is_blocked_and_its_outage_unreachable(reply, word):
    """A refusal of this client, by status, challenge title or Cloudflare's script,
    is BLOCKED; a server that fell over is an outage, a different place to go."""
    hit = _wire(traxsource=reply)
    assert _said(hit)[1] == (searchers.TRAXSOURCE, word)
    assert hit.unread == (searchers.TRAXSOURCE,)
    if reply.status_code == 403:
        assert "403" in hit.answers[1].note


def test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit():
    """R-791's cost: a file no catalogue carries when two were never read."""
    hit = _wire(
        traxsource=_Response(403, CLOUDFLARE_INTERSTITIAL),
        bandcamp=_Response(200, BANDCAMP_CLIENT_CHALLENGE),
    )
    assert not _no_hit(hit)
    assert hit.genre is None
    assert hit.unread == (searchers.TRAXSOURCE, searchers.BANDCAMP)
    assert [answer for _source, answer in _said(hit)] == ["miss", "blocked", "blocked"]


def test_three_misses_on_real_empty_listings_are_still_a_no_hit():
    hit = _wire()
    assert _no_hit(hit)
    assert [answer for _source, answer in _said(hit)] == ["miss", "miss", "miss"]


def test_a_match_records_the_sources_it_never_reached_as_not_asked():
    """Every record lists three answers, never an absent entry to guess at."""
    hit = _wire(beatport=_Response(200, _row(BUCKET_GENRE)))
    assert hit.genre == BUCKET_GENRE
    assert _said(hit) == [
        (searchers.BEATPORT, "matched"),
        (searchers.TRAXSOURCE, searchers.NOT_ASKED),
        (searchers.BANDCAMP, searchers.NOT_ASKED),
    ]
    assert hit.answers[0].source_genre == BUCKET_GENRE
    assert hit.unread == ()


def test_beatport_answering_403_is_blocked_like_the_fallbacks():
    """U281: Beatport's 403 on every lookup from 2026-11-13 is a refusal, not an outage."""
    with pytest.raises(CratekitError) as raised:
        _wire(
            beatport=_Response(403, CLOUDFLARE_INTERSTITIAL),
            traxsource=_Response(503),
            bandcamp=_Response(503),
        )
    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.detail["answers"] == ["blocked", "unreachable", "unreachable"]
    assert cause.detail["notes"][0] == "the catalogue refused this client, HTTP 403"


def test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked():
    """With no MISS the file is refused, and the step says a network check will
    not move a bot check."""
    with pytest.raises(CratekitError) as raised:
        _wire(
            beatport=_Response(503),
            traxsource=_Response(403, CLOUDFLARE_INTERSTITIAL),
            bandcamp=_Response(200, BANDCAMP_CLIENT_CHALLENGE),
        )
    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.detail["answers"] == ["unreachable", "blocked", "blocked"]
    steps = " ".join(cause.remediation.steps)
    assert "traxsource, bandcamp refused this client" in steps


@pytest.mark.parametrize(
    ("reply", "word"),
    [(_Response(200, BANDCAMP_CLIENT_CHALLENGE), "blocked"), (_Response(503), "unreachable")],
    ids=["challenge", "outage"],
)
def test_a_bandcamp_track_page_unread_is_not_a_miss(reply, word):
    """The listing named the track and its page went unread: no absence."""
    hit = _wire(track=reply, bandcamp=_Response(200, GENRELESS_LISTING))
    assert _said(hit)[2] == (searchers.BANDCAMP, word)
    assert hit.unread == (searchers.BANDCAMP,)


def test_a_track_called_just_a_moment_in_a_real_listing_is_not_a_challenge():
    """The check reads the page TITLE, so a row carrying the phrase is a result."""
    title = "Just a moment..."
    row = _traxsource_page([(ARTIST, title, BUCKET_GENRE)])
    hit = _wire(title=title, traxsource=_Response(200, row))
    assert hit.source == searchers.TRAXSOURCE and hit.genre == BUCKET_GENRE


def test_the_interstitial_title_written_with_one_ellipsis_character_is_blocked():
    page = "<html><head><title>Just a moment\N{HORIZONTAL ELLIPSIS}</title></head></html>"
    hit = _wire(bandcamp=_Response(200, page))
    assert _said(hit)[2] == (searchers.BANDCAMP, "blocked")


def test_a_bandcamp_track_page_that_is_gone_is_a_dead_listing_and_still_a_miss():
    """A 404 track page is no answer about the track; held as unreachable, the
    file would stay undecidable while the dead link is listed."""
    assert _no_hit(_wire(track=_Response(404), bandcamp=_Response(200, GENRELESS_LISTING)))


def test_a_blocked_bandcamp_track_page_stops_the_walk_over_further_listings():
    """Every further track page is a paced request to a catalogue that refused."""
    seen: list[str] = []
    second = "https://other.bandcamp.com/track/sunrise-mood"
    listing = [(BANDCAMP_TRACK_URL, TITLE, ARTIST, ""), (second, TITLE, ARTIST, "")]
    _wire(
        seen=seen,
        track=_Response(200, BANDCAMP_CLIENT_CHALLENGE),
        bandcamp=_Response(200, _bandcamp_search_page(listing)),
    )
    assert _track_pages(seen) == [BANDCAMP_TRACK_URL]


def test_a_match_after_an_unreachable_source_names_it_in_unread_too():
    """The record's two fields agree, though the match decides the disposition."""
    hit = _wire(
        beatport=_Response(503),
        traxsource=_Response(200, _traxsource_page([(ARTIST, TITLE, BUCKET_GENRE)])),
    )
    assert hit.source == searchers.TRAXSOURCE
    assert hit.unread == (searchers.BEATPORT,)
