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
from cratekit.core.taxonomy import default_taxonomy, load_taxonomy
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


#: A listing thumbnail in the shape Bandcamp serves and the source system read.
#: ``_7`` is a thumbnail size; the searcher asks for ``_10``, the original.
BANDCAMP_LISTING_ART = "https://f4.bcbits.com/img/a0123456789_7.jpg"
BANDCAMP_PAGE_ART = "https://f4.bcbits.com/img/a0123456789_5.jpg"


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


def _no_hit(hit) -> bool:
    """True for the decline every source asked earned, by answering MISS.

    A DECLINE IS A HIT WITH NO GENRE AND NOT None since R-791, because None
    cannot carry the three answers the item's record owes. A decline beside an
    unread source names it in ``unread`` and is not this.
    """
    return (
        hit is not None
        and hit.genre is None
        and hit.source == ""
        and hit.unread == ()
        and len(hit.answers) == len(searchers.SOURCES)
    )


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
    assert hit.art_url == "", "a row naming no release picture names no picture"


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
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert _no_hit(hit)
    assert [said.answer for said in hit.answers] == ["miss"] * 3


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
    """Two silences and one absence holds back the refusal, because a catalogue
    did answer. Raising here would turn an ordinary bootleg into a failed job
    every time one of three sites was down.

    IT IS NOT A NO-HIT, corrected by R-791. The two silences may carry the
    track, so the decline names them and the file is not reported as one no
    catalogue carries.
    """
    fetch = _all_three(
        beatport=UNREACHABLE,
        traxsource=UNREACHABLE,
        bandcamp=_bandcamp_search_page([]),
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None and hit.genre is None and hit.source == ""
    assert hit.unread == (searchers.BEATPORT, searchers.TRAXSOURCE)


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
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None and hit.genre is None
    assert [said.answer for said in hit.answers] == ["unreachable", "miss", "unreachable"]


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


def test_a_source_genre_nothing_in_the_table_knows_is_written_and_flagged():
    """R-650. The last tier's word reaches the file AND says it was that word.

    The tier exists so a genuinely new genre survives long enough for somebody to
    notice it, and for a year nothing carried the fact that made noticing
    possible. This is the carry: the hit is a normal write, and ``off_taxonomy``
    is what separates it from a tag the declared table produced.
    """
    unknown = "gqom"
    assert routing.suggest_tag(TAXONOMY, unknown).off_taxonomy is True, (
        "the template now declares this string, so this test is asserting about "
        "a tier it no longer reaches"
    )
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, unknown)]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre == unknown
    assert hit.off_taxonomy is True


def test_a_declared_tag_with_no_bucket_reaches_the_file_without_the_flag():
    """The pair the flag exists for, driven through the real pages.

    ``bucket_id is None`` is true of this answer and of the one above, and only
    one of them is worth telling anybody about. The template declares this tag
    and says in a comment why it has no folder, so reporting it would put the
    template author's own deliberate gap in front of them on every sweep.
    """
    declared = routing.suggest_tag(TAXONOMY, "melodic techno")
    assert declared.bucket_id is None and declared.tag and not declared.declined
    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, "melodic techno")]),
        traxsource="",
        bandcamp="",
    )
    hit = _searcher(fetch)(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre == declared.tag
    assert hit.off_taxonomy is False


def test_an_unknown_source_genre_a_taxonomy_calls_too_coarse_is_a_plain_decline():
    """One file gets ONE disposition, and a decline outranks the flag.

    No string in the shipped template reaches the last tier and is also declared
    too coarse, so the producer here is a DIFFERENT taxonomy, which is a thing
    this product supports rather than a hypothetical: the template is a file a
    person edits. Declaring a coarse string without a matching refusal is the
    ordinary way to reach this, and the hit must be the decline it already was,
    carrying no flag about a word it is not going to write.
    """
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

    fetch = _all_three(
        beatport=_beatport_page([_beatport_track(ARTIST, TITLE, "Bootleg")]),
        traxsource="",
        bandcamp="",
    )
    hit = searchers.catalogue_searcher(
        other, fetch=fetch, sleep=lambda _seconds: None
    )(ARTIST, TITLE)
    assert hit is not None
    assert hit.genre is None
    assert hit.off_taxonomy is False
    assert hit.source_genre == "Bootleg"


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


# ---------------------------------------------------------------------------
# F. U85: the picture rides the genre's row, and is fetched on the same terms
# ---------------------------------------------------------------------------

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
    """The hazard the brief names: a cover from a different row is the wrong cover.

    Three rows. The first is an exact title with a picture and NO genre, so it is
    not a candidate at all and must not lend its picture. The second wins, and
    both fields are its own. The third shares the artist, loses on title, and is
    the LAST row scanned, so a picture read off the loop's final row shows here.
    """
    genreless = _with_art(_beatport_track(ARTIST, TITLE, ""), OTHER_ART)
    winner = _with_art(_beatport_track(ARTIST, TITLE, BUCKET_GENRE), BEATPORT_ART)
    loser = _with_art(_beatport_track(ARTIST, f"{TITLE} Reprise Dub", SUB_GENRE), OTHER_ART)

    hit = _searcher(_beatport_only([genreless, winner, loser]))(ARTIST, TITLE)

    assert hit is not None
    assert hit.source_genre == BUCKET_GENRE
    assert hit.art_url.endswith("/image_size/1400x1400/cover-one.jpg")


def test_a_row_whose_artist_does_not_match_lends_neither_genre_nor_picture():
    stranger = _with_art(_beatport_track("Somebody Else", TITLE, BUCKET_GENRE), BEATPORT_ART)
    fetch = _all_three(
        beatport=_beatport_page([stranger]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([]),
    )

    hit = _searcher(fetch)(ARTIST, TITLE)
    assert _no_hit(hit)
    assert hit.art_url == ""


@pytest.mark.parametrize("uri", ["", "file:///etc/passwd", "javascript:alert(1)", 7])
def test_a_release_picture_that_is_not_a_web_address_is_no_picture(uri):
    fetch = _beatport_only([_with_art(_beatport_track(ARTIST, TITLE, BUCKET_GENRE), uri)])

    hit = _searcher(fetch)(ARTIST, TITLE)

    assert hit is not None and hit.genre == BUCKET_GENRE
    assert hit.art_url == ""


def test_a_traxsource_hit_names_no_picture_which_is_parity():
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([(ARTIST, TITLE, BUCKET_GENRE)]),
        bandcamp="",
    )

    hit = _searcher(fetch)(ARTIST, TITLE)

    assert hit is not None and hit.source == searchers.TRAXSOURCE
    assert hit.art_url == ""


def test_a_bandcamp_listing_picture_is_asked_for_at_its_original_size():
    seen: list[str] = []
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page([(BANDCAMP_TRACK_URL, TITLE, ARTIST, BUCKET_GENRE.lower())]),
        seen=seen,
    )

    hit = _searcher(fetch)(ARTIST, TITLE)

    assert hit is not None
    assert hit.art_url == "https://f4.bcbits.com/img/a0123456789_10.jpg"
    assert not [url for url in seen if "/track/" in url]


def test_a_bandcamp_listing_with_a_genre_and_no_picture_reads_the_track_pages_og_image():
    naps: list[float] = []
    seen: list[str] = []
    fetch = _all_three(
        beatport=_beatport_page([]),
        traxsource=_traxsource_page([]),
        bandcamp=_bandcamp_search_page(
            [(BANDCAMP_TRACK_URL, TITLE, ARTIST, BUCKET_GENRE.lower())], art=None
        ),
        track_page=_bandcamp_track_page(["gqom"], og_image=BANDCAMP_PAGE_ART),
        seen=seen,
    )

    hit = _searcher(fetch, naps=naps)(ARTIST, TITLE)

    assert hit is not None
    assert hit.genre == BUCKET_GENRE, "the listing's genre wins over the page's tags"
    assert hit.art_url == "https://f4.bcbits.com/img/a0123456789_10.jpg"
    assert [url for url in seen if "/track/" in url] == [BANDCAMP_TRACK_URL]
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


@pytest.mark.parametrize("status", [404, 500])
def test_an_image_that_is_not_there_is_none_rather_than_a_refusal(status):
    fetch_image = searchers.default_image_fetch(
        get=lambda url, headers, timeout: _Response(status, content=b"page"),
        sleep=lambda _s: None,
    )

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


def test_an_image_fetch_whose_transport_fails_is_none():
    def get(url, headers, timeout):
        raise OSError("no route to host")

    fetch_image = searchers.default_image_fetch(get=get, sleep=lambda _s: None)

    assert fetch_image("https://example.test/cover.jpg") is None


def test_the_image_binder_hands_back_a_fetch_without_touching_the_network(monkeypatch):
    def detonate(*args, **kwargs):
        raise AssertionError("the binder reached the network")

    monkeypatch.setattr(searchers, "_requests_get", detonate)
    assert callable(searchers.for_images())


# ---------------------------------------------------------------------------
# R-791. A bot challenge is its own answer, and no-hit needs every source's MISS
# ---------------------------------------------------------------------------
#
# THE PAGES BELOW ARE THE TWO MEASURED ON 2026-10-01 from the author's machine
# with this module's own headers, reduced to the part the check reads: Traxsource
# answered 403 with Cloudflare's interstitial, Bandcamp answered 200 with a page
# titled "Client Challenge" and no rows. They go through the shipped
# ``default_fetch`` with a fake getter, so the status a fallback reads is the one
# the transport layer really hands it, not one a test typed into ``Fetched``.

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


def _said(hit) -> list[tuple[str, str]]:
    return [(said.source, said.answer) for said in hit.answers]


def test_a_bandcamp_client_challenge_page_is_blocked_rather_than_a_miss():
    """The finding's own shape: a 200 with no rows is not an empty result set
    when its title is a bot check, and reading it as one is what made Bandcamp
    report MISS on every file it was sent."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(200, BANDCAMP_CLIENT_CHALLENGE),
        }
    )(ARTIST, TITLE)

    assert hit.genre is None and hit.source == ""
    assert _said(hit) == [
        (searchers.BEATPORT, "miss"),
        (searchers.TRAXSOURCE, "miss"),
        (searchers.BANDCAMP, "blocked"),
    ]
    assert hit.unread == (searchers.BANDCAMP,)
    assert "Client Challenge" in hit.answers[2].note


def test_a_traxsource_403_interstitial_is_blocked_rather_than_unreachable():
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(403, CLOUDFLARE_INTERSTITIAL),
            searchers.BANDCAMP_SEARCH: _Response(200, _bandcamp_search_page([])),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[1] == (searchers.TRAXSOURCE, "blocked")
    assert "403" in hit.answers[1].note
    assert hit.unread == (searchers.TRAXSOURCE,)


def test_the_challenge_title_alone_blocks_a_fallback_even_on_a_200():
    """Cloudflare does not always send its interstitial with a 403, so the title
    is checked on a page that arrived as a success too."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, CLOUDFLARE_INTERSTITIAL),
            searchers.BANDCAMP_SEARCH: _Response(200, _bandcamp_search_page([])),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[1] == (searchers.TRAXSOURCE, "blocked")


def test_a_beatport_miss_beside_two_blocked_fallbacks_is_not_a_no_hit():
    """The cost R-791 names: this file was reported as one no catalogue carries
    when two of the three were never read. The decline names both."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(403, CLOUDFLARE_INTERSTITIAL),
            searchers.BANDCAMP_SEARCH: _Response(200, BANDCAMP_CLIENT_CHALLENGE),
        }
    )(ARTIST, TITLE)

    assert not _no_hit(hit)
    assert hit.genre is None
    assert hit.unread == (searchers.TRAXSOURCE, searchers.BANDCAMP)
    assert [answer for _source, answer in _said(hit)] == ["miss", "blocked", "blocked"]


def test_three_misses_on_real_empty_listings_are_still_a_no_hit():
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(200, _bandcamp_search_page([])),
        }
    )(ARTIST, TITLE)

    assert _no_hit(hit)
    assert [answer for _source, answer in _said(hit)] == ["miss", "miss", "miss"]


def test_a_match_records_the_sources_it_never_reached_as_not_asked():
    """Every record lists three answers, so a match names the two the walk
    stopped before rather than leaving a reader to guess what an absent entry
    meant."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(
                200, _beatport_page([_beatport_track(ARTIST, TITLE, BUCKET_GENRE)])
            ),
        }
    )(ARTIST, TITLE)

    assert hit.genre == BUCKET_GENRE
    assert _said(hit) == [
        (searchers.BEATPORT, "matched"),
        (searchers.TRAXSOURCE, searchers.NOT_ASKED),
        (searchers.BANDCAMP, searchers.NOT_ASKED),
    ]
    assert hit.answers[0].source_genre == BUCKET_GENRE
    assert hit.unread == ()


def test_a_fallback_that_spends_its_attempts_on_429_is_blocked():
    """The brief names a 429 among the refusals a fallback reads as blocked."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(429),
            searchers.BANDCAMP_SEARCH: _Response(200, _bandcamp_search_page([])),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[1] == (searchers.TRAXSOURCE, "blocked")


def test_a_fallback_answering_503_is_still_unreachable_rather_than_blocked():
    """A server that fell over is an outage, not a refusal of this client, and
    the two send a person to different places."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(503),
            searchers.BANDCAMP_SEARCH: _Response(200, _bandcamp_search_page([])),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[1] == (searchers.TRAXSOURCE, "unreachable")
    assert hit.unread == (searchers.TRAXSOURCE,)


def test_beatport_answering_403_is_unreachable_as_it_always_was():
    """Beatport's read is unchanged by R-791, and a block check that reached it
    would change a source the finding measured as answering."""
    with pytest.raises(CratekitError) as raised:
        _over_the_wire(
            {
                searchers.BEATPORT_SEARCH: _Response(403, CLOUDFLARE_INTERSTITIAL),
                searchers.TRAXSOURCE_SEARCH: _Response(503),
                searchers.BANDCAMP_SEARCH: _Response(503),
            }
        )(ARTIST, TITLE)

    assert raised.value.cause.detail["answers"] == ["unreachable"] * 3


def test_three_refusals_raise_unreachable_and_say_the_fallbacks_were_blocked():
    """A blocked catalogue is not an answer about the track, so a file nobody
    answered MISS for is still refused rather than declined, and the step tells
    the person a network check will not move a bot check."""
    with pytest.raises(CratekitError) as raised:
        _over_the_wire(
            {
                searchers.BEATPORT_SEARCH: _Response(503),
                searchers.TRAXSOURCE_SEARCH: _Response(403, CLOUDFLARE_INTERSTITIAL),
                searchers.BANDCAMP_SEARCH: _Response(200, BANDCAMP_CLIENT_CHALLENGE),
            }
        )(ARTIST, TITLE)

    cause = raised.value.cause
    assert cause.reason == searchers.UNREACHABLE_REASON
    assert cause.detail["answers"] == ["unreachable", "blocked", "blocked"]
    steps = " ".join(cause.remediation.steps)
    assert "traxsource, bandcamp refused this client" in steps


def test_a_bandcamp_track_page_behind_a_challenge_is_blocked_rather_than_a_miss():
    """The second touch, one function over: the listing named the track and the
    challenge hid its genre, which is not the catalogue lacking it."""
    hit = _over_the_wire(
        {
            "/track/": _Response(200, BANDCAMP_CLIENT_CHALLENGE),
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(
                200, _bandcamp_search_page([(BANDCAMP_TRACK_URL, TITLE, ARTIST, "")])
            ),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[2] == (searchers.BANDCAMP, "blocked")
    assert hit.unread == (searchers.BANDCAMP,)


def test_a_bandcamp_track_page_that_cannot_be_reached_is_unreachable_rather_than_a_miss():
    hit = _over_the_wire(
        {
            "/track/": _Response(503),
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(
                200, _bandcamp_search_page([(BANDCAMP_TRACK_URL, TITLE, ARTIST, "")])
            ),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[2] == (searchers.BANDCAMP, "unreachable")


def test_a_track_called_just_a_moment_in_a_real_listing_is_not_a_challenge():
    """The check reads the page TITLE, so a result row carrying the phrase is a
    result and not a refusal."""
    title = "Just a moment..."
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(
                200, _traxsource_page([(ARTIST, title, BUCKET_GENRE)])
            ),
        }
    )(ARTIST, title)

    assert hit.source == searchers.TRAXSOURCE and hit.genre == BUCKET_GENRE


def test_cloudflare_challenge_machinery_in_the_body_blocks_whatever_the_title_says():
    """The title is one dress; the interstitial's own script path is the
    measured marker that does not change with the wording."""
    page = CLOUDFLARE_INTERSTITIAL.replace("Just a moment...", "Verifying you are human")
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, page),
            searchers.BANDCAMP_SEARCH: _Response(200, _bandcamp_search_page([])),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[1] == (searchers.TRAXSOURCE, "blocked")


def test_the_interstitial_title_written_with_one_ellipsis_character_is_blocked():
    page = "<html><head><title>Just a moment\u2026</title></head></html>"
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(200, page),
        }
    )(ARTIST, TITLE)

    assert _said(hit)[2] == (searchers.BANDCAMP, "blocked")


def test_a_bandcamp_track_page_that_is_gone_is_a_dead_listing_and_still_a_miss():
    """A 404 on the track page is a listing whose record was removed, which is
    no answer about the track; holding it as unreachable would leave the file
    undecidable for as long as the dead link stays listed."""
    hit = _over_the_wire(
        {
            "/track/": _Response(404),
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(
                200, _bandcamp_search_page([(BANDCAMP_TRACK_URL, TITLE, ARTIST, "")])
            ),
        }
    )(ARTIST, TITLE)

    assert _no_hit(hit)


def test_a_blocked_bandcamp_track_page_stops_the_walk_over_further_listings():
    """Every further track page is a paced request to a catalogue that has just
    refused this client."""
    seen: list[str] = []
    second = "https://other.bandcamp.com/track/sunrise-mood"
    _over_the_wire(
        {
            "/track/": _Response(200, BANDCAMP_CLIENT_CHALLENGE),
            searchers.BEATPORT_SEARCH: _Response(200, _beatport_page([])),
            searchers.TRAXSOURCE_SEARCH: _Response(200, _traxsource_page([])),
            searchers.BANDCAMP_SEARCH: _Response(
                200,
                _bandcamp_search_page(
                    [(BANDCAMP_TRACK_URL, TITLE, ARTIST, ""), (second, TITLE, ARTIST, "")]
                ),
            ),
        },
        seen,
    )(ARTIST, TITLE)

    assert [url for url in seen if "/track/" in url] == [BANDCAMP_TRACK_URL]


def test_a_match_after_an_unreachable_source_names_it_in_unread_too():
    """The record's two fields agree: answers shows Beatport unreachable, so
    unread says so, though the match decides the disposition."""
    hit = _over_the_wire(
        {
            searchers.BEATPORT_SEARCH: _Response(503),
            searchers.TRAXSOURCE_SEARCH: _Response(
                200, _traxsource_page([(ARTIST, TITLE, BUCKET_GENRE)])
            ),
        }
    )(ARTIST, TITLE)

    assert hit.source == searchers.TRAXSOURCE
    assert hit.unread == (searchers.BEATPORT,)


class _Response:
    """The attributes this module reads off an HTTP response, and no more.

    Defined as the last thing in the file on purpose: it is a fixture for the
    default fetch's tests rather than a description of anything the module owns,
    and the module's own contract with a getter is exactly these fields:
    ``text`` for a page and ``content`` for a picture.
    """

    def __init__(self, status_code: int, text: str = "", *, content: bytes = b"") -> None:
        self.status_code = status_code
        self.text = text
        self.content = content
