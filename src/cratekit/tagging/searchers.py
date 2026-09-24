"""Ask three record catalogues what a track's genre is, or say why nobody answered.

WHY THE OUTCOME OF ONE SOURCE HAS FOUR VALUES AND NOT TWO. The obvious shape is
a genre or nothing, and it is the shape that quietly ruins a library. A source
that could not be reached returns nothing, a source whose markup changed returns
nothing, and a source that answered and did not carry the track returns nothing,
so a folder swept during an outage completes clean and every file in it is
recorded as a track the catalogues do not know. Absence read as evidence of
absence is the first failure pattern METHOD names, and this module is where it
would enter the tagging verbs. So each source answers MATCHED, MISS, UNREACHABLE
or PARSE_BREAK, and only MISS is permitted to contribute to a decline.

WHY A PARSE BREAK IS NOT AN UNREACHABLE. Splitting them costs one enum value and
buys the difference between "your network is down, try later" and "our scraper is
broken, report it". Folded together, a permanent defect in this product wears a
transient remedy, which is a person retrying for a week over something no retry
can fix. The live system this replaces keeps the first distinction and loses this
one.

A PARSE BREAK IS CLAIMED ONLY ON POSITIVE EVIDENCE, and the asymmetry is
deliberate. Beatport's search page is a Next.js document whose ``__NEXT_DATA__``
script is present with or without results, so a page missing it is a page this
parser has never seen. The other two are read row by row, where an absent row is
genuinely ambiguous: it is either an empty result set or a redesign. Those two
claim a break only when result rows ARE present and the parser reads none of
them. A guess that goes wrong therefore degrades to a miss, never to a false
defect report, because reporting a bootleg nobody sells as a broken scraper is
the more expensive mistake by far.

THE GENRE IS RESOLVED BY THE SHIPPED RESOLVER, NEVER BY A MAP WRITTEN HERE.
:func:`cratekit.core.routing.suggest_tag` already owns this question, runs the
taxonomy's own exact refusals before any alias lookup, and resolves a sub level
alias to the SUB's display rather than to its parent bucket's. A hand rolled
lookup over ``tagging_alias`` would be a weaker second opinion about a question
that has an owner, and it would lose the sub. R19 forbids a display name in code
below the modules layer, and this module is the most tempting place in the
repository to break that rule, because the system it replaces carries a hundred
line vendor to folder map. The suite scans this file's own literals for one.

AN ANSWER TOO COARSE TO BE A FINAL TAG IS A DECLINE, NOT A HIT.
``suggest_tag``'s last tier passes an unrecognized source string through
unchanged, and its alias tier can land on the fallback bucket's display.
:mod:`cratekit.tagging.retag` refuses exactly that value at its own write and
says why: writing it launders a catch-all into a value the corrective verb would
never select again, so the two tagging verbs would disagree about one catalogue
answer and bounce the file between them for ever. Declining leaves the file
askable, which is what a decline is for.

AN UNRECOGNIZED ANSWER THAT IS NOT TOO COARSE IS STILL WRITTEN, AND IS NOW SAID
OUT LOUD. That last tier existed so a genuinely new genre would survive long
enough for someone to notice it, and for a year nothing implemented the
noticing: the word went onto the file and the verb's report counted it as a
clean tag (R-650). The hit carries ``off_taxonomy`` up to the report, which names
the distinct strings and warns. Making the tier decline instead would be the
blanket genre bug in reverse, so what changed is the reporting and not the
resolving.

A DECLINE STILL NAMES WHAT IT DECLINED. The hit carries ``source`` and
``source_genre`` even when ``genre`` is None, so the item artifact and the verb's
report can say which catalogue answered and with what string. Without it a
person learns only that something was unmapped, which tells them nothing about
which alias their taxonomy is missing.

THE TWO REFUSALS HAVE SLUGS OF THEIR OWN, and that is the point of them rather
than a tidiness. ``cratekit.core.cause.REASONS`` declares
``catalogue-unreachable`` and ``catalogue-parse-broken``, added by this unit.
They share their exit codes with the classes above them and they do not share
their slugs, because the slug is the surface a person and a log filter read, and
the two send somebody to two different places: a network, or this parser. Riding
``unavailable-transient`` would put a permanent break behind "retry later" for
ever, and riding ``internal-error`` would mix an expected consequence of the web
moving in with the states this program says cannot happen.

EVERY FETCH IS PACED, INCLUDING THE FIRST. A pacer that waits only BETWEEN
touches lets a fresh process open with a burst, and a fresh process is exactly
what the job engine spawns per resume. The interval is jittered from an injected
random source so two runs that started together do not stay in step, which is how
a shared rate limit turns into a shared retry.

THE PACER IS THIS MODULE'S OWN AND NOT ``acquire.download.Pacing``. That one is a
bounded concurrent pool tied to the adapter contract, and importing it would bind
tagging to acquisition for the sake of one interval. The duplication is recorded
as a residual rather than hidden.

THE PICTURE RIDES THE GENRE'S ROW. A match carries the cover URL off the same
row that supplied its genre, Beatport's release image or Bandcamp's listing or
page image, and Traxsource names none, which is parity. The image is fetched
later, and only for a file with no picture, by :func:`default_image_fetch`,
which shares this module's pacer shape and rate limit policy.

``requests`` IS NAMED IN EXACTLY ONE FUNCTION. Everything above it takes a fetch
seam, and the default fetch takes its HTTP getter and its sleep as parameters, so
the rate limit backoff is driven in the suite with nothing on the network.

Layer: modules.
"""

from __future__ import annotations

import json
import logging
import random
import re
import time
import unicodedata
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from urllib.parse import quote_plus

from cratekit.core import routing
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging.tag import FetchImage, Searcher, SearchHit

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# The numbers, stated rather than left to a caller
# ---------------------------------------------------------------------------

#: A request that carries no timeout blocks for ever, and a tagging sweep that
#: blocks for ever looks exactly like one that is working. Fifteen seconds is the
#: value the live system already paid for.
REQUEST_TIMEOUT_S = 15.0

#: The first wait after a rate limit answer, growing linearly with each attempt.
#: Thirty seconds is the live system's value too: shorter waits arrive inside the
#: same window that refused the first request.
RATE_LIMIT_BASE_WAIT_S = 30.0

#: Total attempts per fetch, the first included. A cap is what makes an exhausted
#: rate limit reportable as UNREACHABLE instead of a loop that looks like work.
RATE_LIMIT_ATTEMPTS = 3

#: The floor between two consecutive touches of any catalogue.
MIN_INTERVAL_S = 1.0

#: Half the floor again, either way, so the interval lands in [1.0, 1.5]. Wide
#: enough that two runs drawing independently do not stay in step for long.
JITTER_FRACTION = 0.5

#: One browser identity for every request this module makes. A catalogue that
#: sees a default client library user agent answers a different page, or none.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

BEATPORT = "beatport"
TRAXSOURCE = "traxsource"
BANDCAMP = "bandcamp"

#: The fallback order. Beatport carries the richest genre field, Traxsource
#: covers the house and soul catalogue Beatport thins out, and Bandcamp catches
#: the self released records neither of the first two stocks.
SOURCES: tuple[str, ...] = (BEATPORT, TRAXSOURCE, BANDCAMP)

BEATPORT_SEARCH = "https://www.beatport.com/search"
TRAXSOURCE_SEARCH = "https://www.traxsource.com/search/tracks"
BANDCAMP_SEARCH = "https://bandcamp.com/search"

#: The two slugs this module raises, named once so the tests assert against these
#: rather than against a string typed in three places. Both are declared in
#: ``cause.REASONS``, and they are two slugs rather than one because they send a
#: person to two different places: a catalogue nobody could read is somebody's
#: network, and a page whose shape moved is this parser.
UNREACHABLE_REASON = "catalogue-unreachable"
PARSE_BREAK_REASON = "catalogue-parse-broken"

#: Bandcamp tags are free text a seller typed, so the list holds release
#: descriptors beside genres. These are the descriptors. Deliberately no genre
#: word appears here: a tag too coarse to write is the declared taxonomy's
#: judgement to make, not this module's.
_TAG_NOISE = frozenset({"edit", "edits", "remix", "remixes", "extended mix"})


# ---------------------------------------------------------------------------
# The per source outcome, which is this module's core type
# ---------------------------------------------------------------------------


class Answer(Enum):
    """What one catalogue did when it was asked.

    MISS is the only value that means "this catalogue does not carry the track".
    The other three mean, in order, that it does, that we could not ask, and that
    we asked and could not read the reply.
    """

    MATCHED = "matched"
    MISS = "miss"
    UNREACHABLE = "unreachable"
    PARSE_BREAK = "parse-break"


@dataclass(frozen=True, slots=True)
class SourceOutcome:
    """One catalogue's answer, with the source that gave it and what it said.

    ``art_url`` is the picture on the row that answered, the same row as
    ``source_genre``, or empty when that row named none.
    """

    source: str
    answer: Answer
    source_genre: str = ""
    note: str = ""
    art_url: str = ""


@dataclass(frozen=True, slots=True)
class Fetched:
    """One HTTP touch, as either the page text or the reason there is none.

    ``text`` of None IS the unreachable outcome. The fetch seam deliberately does
    not return a :class:`SourceOutcome`, because a fetch is given a URL and knows
    no source name; the caller that knew which catalogue it was asking attaches
    that.
    """

    text: str | None = None
    note: str = ""


#: The one seam every network touch goes through. Given a URL, it answers with
#: the page or with the reason there is none.
Fetch = Callable[[str], Fetched]


# ---------------------------------------------------------------------------
# Pacing
# ---------------------------------------------------------------------------


@dataclass
class Pacer:
    """The wait before every touch of a catalogue, jittered and injectable.

    ``sleep`` is a parameter rather than a call to :func:`time.sleep` so the
    suite asserts the schedule instead of enduring it, and ``entropy`` is a
    parameter so a seeded run reproduces. Both are the difference between a rate
    limit policy that is tested and one that is merely written down.
    """

    minimum_s: float = MIN_INTERVAL_S
    jitter_fraction: float = JITTER_FRACTION
    entropy: random.Random = field(default_factory=random.Random)
    sleep: Callable[[float], None] = time.sleep

    def wait(self) -> float:
        """Sleep the next interval and return how long it was."""
        delay = self.minimum_s * (1.0 + self.entropy.random() * self.jitter_fraction)
        self.sleep(delay)
        return delay


# ---------------------------------------------------------------------------
# The default fetch, and the only function that names ``requests``
# ---------------------------------------------------------------------------


def _requests_get(url: str, *, headers: dict[str, str], timeout: float) -> Any:
    """THE ONE PLACE ``requests`` IS NAMED, and the reason it is a function.

    Held apart so :func:`default_fetch` takes a getter as a parameter and the
    rate limit backoff above it is driven with nothing on the network. The suite
    also detonates this symbol, which only proves anything because an injected
    getter never reaches it.
    """
    import requests  # noqa: PLC0415

    return requests.get(url, headers=headers, timeout=timeout)


def default_fetch(
    *,
    get: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> Fetch:
    """The shipped fetch seam: one GET, one timeout, one rate limit policy.

    R22's classification lives here and nowhere else, so there is one answer to
    "was that source unreachable" rather than three that drift. A transport
    failure and any non 200 other than 429 are unreachable immediately; a 429
    waits and retries until the attempt cap is spent, and a spent cap is
    unreachable rather than a miss.

    The last refusal does NOT sleep on its way out. A wait after the final
    attempt is time spent on a request nobody is going to make.
    """
    getter = _requests_get if get is None else get

    def fetch(url: str) -> Fetched:
        response, note = _answered(getter, sleep, url)
        if response is None:
            return Fetched(note=note)
        return Fetched(text=response.text)

    return fetch


def _answered(
    getter: Callable[..., Any], sleep: Callable[[float], None], url: str
) -> tuple[Any, str]:
    """One GET under the rate limit policy: the 200 response, or None and why.

    Shared by the page fetch and the image fetch, so a picture is asked for on
    exactly the terms a search page is, one timeout, one backoff, one cap.
    """
    for attempt in range(RATE_LIMIT_ATTEMPTS):
        try:
            response = getter(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_S)
        # A bare except, on purpose. This IS the transport layer, and every
        # way it can fail is one fact: the source could not be read. Naming
        # the exception classes of whatever getter a caller injected would
        # bind this seam to one client library and let the next one through.
        except Exception as exc:  # noqa: BLE001
            return None, f"transport failure: {exc}"
        status = getattr(response, "status_code", None)
        if status == 429:
            if attempt + 1 < RATE_LIMIT_ATTEMPTS:
                sleep(RATE_LIMIT_BASE_WAIT_S * (attempt + 1))
                continue
            return None, f"rate limited, {RATE_LIMIT_ATTEMPTS} attempts spent without an answer"
        if status != 200:
            return None, f"HTTP {status}"
        return response, ""
    return None, "rate limited, attempts spent"


def default_image_fetch(
    *,
    get: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    pacing: Pacer | None = None,
) -> FetchImage:
    """The shipped image seam: a paced GET, answering bytes or None.

    PACED LIKE A SEARCH, because the picture lives on the same catalogue's
    servers and a folder of new files is a burst of them. None rather than a
    refusal for every failure, because a picture that cannot be had is a
    decline for its file and :func:`cratekit.tagging.tag.tag_one` says so. The
    reason is logged, since the bytes seam has nowhere else to carry it.
    """
    getter = _requests_get if get is None else get
    pacer = Pacer(sleep=sleep) if pacing is None else pacing

    def fetch_image(url: str) -> bytes | None:
        pacer.wait()
        response, note = _answered(getter, sleep, url)
        if response is None:
            log.debug("picture fetch failed for %s: %s", url, note)
            return None
        data = getattr(response, "content", None)
        return bytes(data) if data else None

    return fetch_image


# ---------------------------------------------------------------------------
# Matching, shared by all three sources
# ---------------------------------------------------------------------------


def _normalized(value: str) -> str:
    """NFC, lowercased, trimmed. Catalogue text and file tags disagree about all
    three, and a comparison that skips normalizing misses on the accent alone."""
    return unicodedata.normalize("NFC", value).lower().strip()


def _without_trailing_bracket(value: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*$", "", value).strip()


def _artist_parts(value: str, separators: str) -> list[str]:
    parts = [_normalized(part) for part in re.split(separators, value)]
    # Two characters and under are initials and conjunctions, and they match
    # everything by substring, which is how a loose comparison turns into no
    # comparison at all.
    return [part for part in parts if len(part) > 2]


def _artist_matches(searched: str, found: str) -> bool:
    """Whether at least one credited name is shared.

    A release credits remixers and features the file's tag does not, and the file
    credits the ones the release drops, so an all names comparison rejects almost
    every genuine match.
    """
    searched_parts = _artist_parts(searched, r"[,&]")
    found_parts = _artist_parts(found, r"[,&/]")
    return any(
        left == right or left in right or right in left
        for left in searched_parts
        for right in found_parts
    )


def _title_matches(searched: str, found: str) -> bool:
    """Whether two titles name the same recording.

    The bracketed suffix is stripped from both sides first, because a catalogue
    calls it an extended mix and a file calls it nothing at all, and that suffix
    is the single commonest reason an exact comparison misses.
    """
    left, right = _normalized(searched), _normalized(found)
    bare_left, bare_right = _without_trailing_bracket(left), _without_trailing_bracket(right)
    if bare_left == bare_right or bare_left in bare_right or bare_right in bare_left:
        return True
    return left in right or right in left


def _query(artist: str, title: str) -> str:
    """One escaped query string for all three catalogues.

    Escaping is not cosmetic here: an unescaped ampersand truncates the query at
    the first delimiter, which returns a page for a different search and reports
    it as a miss.
    """
    return quote_plus(f"{artist} {title}".strip())


# ---------------------------------------------------------------------------
# Beatport
# ---------------------------------------------------------------------------

_NEXT_DATA = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.DOTALL
)


def _beatport_tracks(page: str) -> list[dict[str, Any]] | None:
    """The track objects on a search page, or None when the shape is unknown.

    None and an empty list are different answers and the caller treats them
    differently: an empty list is a search that found nothing, and None is a page
    this parser has never seen.
    """
    found = _NEXT_DATA.search(page)
    if not found:
        return None
    try:
        payload = json.loads(found.group(1))
    except ValueError:
        return None
    queries = (
        payload.get("props", {})
        .get("pageProps", {})
        .get("dehydratedState", {})
        .get("queries", [])
    )
    for query in queries:
        data = query.get("state", {}).get("data", {})
        if "tracks" in data:
            return data["tracks"].get("data", [])
    return None


def _beatport_genre(track: dict[str, Any]) -> str:
    genres = track.get("genre") or []
    if not genres:
        return ""
    return genres[0].get("genre_name") or ""


_BEATPORT_IMAGE_SIZE = re.compile(r"image_size/\d+x\d+/")

#: The edge Beatport is asked to serve a cover at. The source system's value,
#: large enough that the re-encode to the CDJ size only ever shrinks.
BEATPORT_IMAGE_EDGE = 1400


def _web_url(value: object) -> str:
    """``value`` when it is an http or https URL, else empty.

    A payload field is text somebody else chose, and this one becomes a GET.
    Anything that is not a web address is no picture rather than a request.
    """
    text = value.strip() if isinstance(value, str) else ""
    return text if text.startswith(("https://", "http://")) else ""


def _beatport_art(track: dict[str, Any]) -> str:
    """The row's release cover, resized, or empty when the row names none.

    ``release.release_image_uri`` is the field the source system read. Whether
    the payload this module parses still carries it is owed to an attended run.
    """
    release = track.get("release")
    uri = _web_url(release.get("release_image_uri") if isinstance(release, dict) else "")
    edge = BEATPORT_IMAGE_EDGE
    return _BEATPORT_IMAGE_SIZE.sub(f"image_size/{edge}x{edge}/", uri)


@dataclass(frozen=True, slots=True)
class _Pick:
    """The best scoring Beatport row's genre and picture, read off ONE row."""

    genre: str
    art_url: str = ""


def _beatport_best(tracks: Iterable[dict[str, Any]], artist: str, title: str) -> _Pick | None:
    """The genre and picture off the best scoring track, or None when nothing scores.

    Rows carrying no genre are skipped rather than scored. A row that cannot
    supply the genre is not a candidate, and letting one win on title alone
    would turn a source that could have answered into a decline.

    BOTH FIELDS COME OFF THE ONE WINNING ROW. A picture taken from a different
    row than the genre is how a file ends up wearing another record's cover, so
    the artist and title gate that picks the genre picks the picture too.
    """
    title_normalized = _normalized(title)
    bare_title = _without_trailing_bracket(title_normalized)
    searched = _artist_parts(artist, r"[,&]")

    best_score = 0
    best: _Pick | None = None
    for track in tracks:
        genre = _beatport_genre(track)
        if not genre:
            continue
        name = _normalized(track.get("track_name", ""))
        mix = _normalized(track.get("mix_name", ""))
        credited = [_normalized(entry.get("artist_name", "")) for entry in track.get("artists", [])]

        artist_score = 0
        for part in searched:
            if any(part == other or part in other or other in part for other in credited):
                artist_score += 1
        if artist_score == 0:
            continue

        if bare_title == name or title_normalized == f"{name} ({mix})":
            title_score = 3
        elif name and (bare_title in name or name in bare_title):
            title_score = 2
        elif name and name in title_normalized:
            title_score = 1
        else:
            continue

        # Title dominates by an order of magnitude, because a shared artist over
        # a different record is a wrong answer and a shared record with one
        # credit missing is a right one.
        score = title_score * 10 + artist_score
        if score > best_score:
            best_score = score
            best = _Pick(genre, _beatport_art(track))
    return best


def _search_beatport(
    artist: str, title: str, *, fetch: Fetch, pacer: Pacer, **_: Any
) -> SourceOutcome:
    pacer.wait()
    page = fetch(f"{BEATPORT_SEARCH}?q={_query(artist, title)}")
    if page.text is None:
        return SourceOutcome(BEATPORT, Answer.UNREACHABLE, note=page.note)
    tracks = _beatport_tracks(page.text)
    if tracks is None:
        return SourceOutcome(
            BEATPORT,
            Answer.PARSE_BREAK,
            note="the search page carries no readable track payload",
        )
    pick = _beatport_best(tracks, artist, title)
    if pick is None:
        return SourceOutcome(BEATPORT, Answer.MISS)
    return SourceOutcome(
        BEATPORT, Answer.MATCHED, source_genre=pick.genre, art_url=pick.art_url
    )


# ---------------------------------------------------------------------------
# Traxsource
# ---------------------------------------------------------------------------

_TRAX_ROW = re.compile(r'data-trid="\d+"')
_TRAX_TITLE = re.compile(r'class="trk-cell title".*?<a[^>]*>([^<]+)</a>', re.DOTALL)
_TRAX_ARTISTS = re.compile(r'class="com-artists"[^>]*>([^<]+)</a>')
_TRAX_GENRE = re.compile(r'class="trk-cell genre".*?<a[^>]*>([^<]+)</a>', re.DOTALL)


def _traxsource_rows(page: str) -> list[str]:
    """The result rows, sliced at their own markers rather than matched whole.

    A non greedy match to a closing tag breaks the moment a row gains a nested
    element, and a row on this page gains them often. Slicing between markers
    cannot be wrong about where a row ends, only generous.
    """
    starts = [found.start() for found in _TRAX_ROW.finditer(page)]
    if not starts:
        return []
    bounds = [*starts, len(page)]
    return [page[bounds[index] : bounds[index + 1]] for index in range(len(starts))]


def _search_traxsource(
    artist: str, title: str, *, fetch: Fetch, pacer: Pacer, **_: Any
) -> SourceOutcome:
    pacer.wait()
    page = fetch(f"{TRAXSOURCE_SEARCH}?term={_query(artist, title)}&page=1")
    if page.text is None:
        return SourceOutcome(TRAXSOURCE, Answer.UNREACHABLE, note=page.note)

    rows = _traxsource_rows(page.text)
    titles_read = 0
    for row in rows:
        found_title = _TRAX_TITLE.search(row)
        if not found_title:
            continue
        titles_read += 1
        found_genre = _TRAX_GENRE.search(row)
        if not found_genre:
            continue
        found_artist = _TRAX_ARTISTS.search(row)
        credited = found_artist.group(1).strip() if found_artist else ""
        if not _title_matches(title, found_title.group(1).strip()):
            continue
        if credited and not _artist_matches(artist, credited):
            continue
        return SourceOutcome(
            TRAXSOURCE, Answer.MATCHED, source_genre=found_genre.group(1).strip()
        )

    if rows and titles_read == 0:
        # Rows are present and this parser read none of them, which is the only
        # evidence that separates a redesign from an empty result set.
        return SourceOutcome(
            TRAXSOURCE,
            Answer.PARSE_BREAK,
            note="result rows are present and none of them parsed",
        )
    return SourceOutcome(TRAXSOURCE, Answer.MISS)


# ---------------------------------------------------------------------------
# Bandcamp
# ---------------------------------------------------------------------------

_BC_RESULT = re.compile(r'class="searchresult.*?</li>', re.DOTALL)
_BC_HEADING = re.compile(
    r'class="heading">\s*<a[^>]*href="(https://[^"]+bandcamp\.com/track/[^"]+)"[^>]*>'
    r"\s*(.*?)\s*</a>",
    re.DOTALL,
)
_BC_SUBHEAD = re.compile(r'class="subhead">\s*(.*?)\s*</div>', re.DOTALL)
_BC_BY = re.compile(r"by\s+(.*?)$")
_BC_LISTING_GENRE = re.compile(r'class="genre">\s*genre:\s*(.*?)\s*</div>', re.DOTALL)
_BC_TAG = re.compile(r'<a class="tag"[^>]*>([^<]+)</a>')
_BC_LISTING_ART = re.compile(r'<img src="(https://f4\.bcbits\.com/img/[^"]+)"')
_BC_OG_IMAGE = re.compile(r'<meta property="og:image"\s+content="([^"]+)"')
_BC_IMAGE_SIZE = re.compile(r"_\d+\.jpg$")


def _bandcamp_art(found: re.Match[str] | None) -> str:
    """The picture a listing or a track page names, at its largest, or empty.

    Bandcamp encodes the size in the file name's last number, and ``_10`` is the
    original upload. The source system asked for that one.
    """
    if found is None:
        return ""
    return _BC_IMAGE_SIZE.sub("_10.jpg", _web_url(found.group(1)))


def _bandcamp_credited(entry: str) -> str:
    subhead = _BC_SUBHEAD.search(entry)
    if not subhead:
        return ""
    credited = _BC_BY.search(subhead.group(1).strip())
    return credited.group(1).strip() if credited else ""


def _bandcamp_heading_matches(title: str, heading: str) -> bool:
    if _title_matches(title, heading):
        return True
    # A listing heading is sometimes "Artist - Title" rather than the title
    # alone, and dropping the credit is the difference between a match and a
    # miss on a self released record.
    if " - " in heading:
        return _title_matches(title, heading.split(" - ", 1)[1])
    return False


def _bandcamp_tag(tags: Sequence[str], declared: Taxonomy) -> str:
    """Choose one tag out of a seller's list, asking the taxonomy which it knows.

    Bandcamp answers with free text rather than with a genre field, so something
    has to choose, and the only chooser that is not arbitrary is the declared
    taxonomy: the first tag it RECOGNIZES wins. Capitalized tags are location
    tags by Bandcamp's own convention and are skipped. When it recognizes none,
    the first remaining tag is returned raw, so the decline downstream names a
    real string a person can add an alias for rather than nothing at all.
    """
    candidates = [tag for tag in tags if tag == tag.lower() and tag not in _TAG_NOISE]
    for tag in candidates:
        suggestion = routing.suggest_tag(declared, tag)
        if suggestion.bucket_id is not None and not suggestion.declined:
            return tag
    return candidates[0] if candidates else ""


def _search_bandcamp(
    artist: str, title: str, *, fetch: Fetch, pacer: Pacer, declared: Taxonomy
) -> SourceOutcome:
    pacer.wait()
    page = fetch(f"{BANDCAMP_SEARCH}?q={_query(artist, title)}&item_type=t")
    if page.text is None:
        return SourceOutcome(BANDCAMP, Answer.UNREACHABLE, note=page.note)

    entries = _BC_RESULT.findall(page.text)
    headings_read = 0
    for entry in entries:
        heading = _BC_HEADING.search(entry)
        if not heading:
            continue
        headings_read += 1
        track_url, text = heading.group(1).split("?")[0], heading.group(2).strip()
        if not _bandcamp_heading_matches(title, text):
            continue
        credited = _bandcamp_credited(entry)
        if credited and not _artist_matches(artist, credited):
            continue

        listed = _BC_LISTING_GENRE.search(entry)
        genre = listed.group(1).strip() if listed else ""
        art_url = _bandcamp_art(_BC_LISTING_ART.search(entry))
        if not genre or not art_url:
            # The genre usually lives on the track page rather than in the
            # listing, and so does the picture when the listing shows none. This
            # is the second touch, and it is paced like the first. The listing's
            # own answer wins where it gave one.
            pacer.wait()
            track_page = fetch(track_url)
            if track_page.text is not None:
                genre = genre or _bandcamp_tag(_BC_TAG.findall(track_page.text), declared)
                art_url = art_url or _bandcamp_art(_BC_OG_IMAGE.search(track_page.text))
        if genre:
            return SourceOutcome(
                BANDCAMP, Answer.MATCHED, source_genre=genre, art_url=art_url
            )

    if entries and headings_read == 0:
        return SourceOutcome(
            BANDCAMP,
            Answer.PARSE_BREAK,
            note="search results are present and none of them parsed",
        )
    return SourceOutcome(BANDCAMP, Answer.MISS)


# ---------------------------------------------------------------------------
# The walk, and what it does when nobody answered
# ---------------------------------------------------------------------------

_SEARCHES = (_search_beatport, _search_traxsource, _search_bandcamp)


def _resolved(declared: Taxonomy, outcome: SourceOutcome) -> SearchHit:
    """Turn one catalogue's raw genre into the tag to write, or into a decline.

    The hit is returned either way, because a decline that cannot say what it
    declined is a decline nobody can act on.

    A TAG AND A DECLINE ARE THE TWO OUTCOMES, AND ``off_taxonomy`` QUALIFIES THE
    FIRST ONE ONLY. It rides a genre that is actually going to be written, so a
    pass through string this taxonomy calls too coarse to be a final tag is a
    plain decline and carries no flag: a file gets one disposition, never two.
    """
    suggestion = routing.suggest_tag(declared, outcome.source_genre)
    tag = suggestion.tag
    if suggestion.declined or not tag or declared.is_too_coarse_as_source(tag):
        tag = None
    return SearchHit(
        genre=tag,
        source=outcome.source,
        source_genre=outcome.source_genre,
        art_url=outcome.art_url,
        off_taxonomy=tag is not None and suggestion.off_taxonomy,
    )


def _decide(outcomes: Sequence[SourceOutcome], artist: str, title: str) -> None:
    """Refuse, or return None to decline, once every source has been asked.

    The precedence is the point of the whole module. One source that ANSWERED,
    even to say it does not carry the track, is enough to make this a genuine
    absence and to make declining honest. Only when nobody answered does the
    question become which refusal, and a parse break beats an unreachable there
    because a broken parser is actionable today and a network is not.
    """
    if any(outcome.answer is Answer.MISS for outcome in outcomes):
        return None

    broken = [outcome for outcome in outcomes if outcome.answer is Answer.PARSE_BREAK]
    if broken:
        named = ", ".join(outcome.source for outcome in broken)
        raise refuse(
            PARSE_BREAK_REASON,
            f"{named} answered and the page did not carry a shape this parser "
            f"recognizes, so nothing was learned about {artist!r} {title!r}. This "
            f"is a defect in this software rather than a fact about the catalogue",
            remedy=Remedy.REPORT_DEFECT,
            steps=(
                f"report that the {named} parser in cratekit.tagging.searchers needs "
                f"rewriting against the page shape now being served; retrying and "
                f"waiting will not move it",
            ),
            scope=Scope.RUN,
            retryable=False,
            origin=("tagging", "searchers"),
            detail={
                "sources": [outcome.source for outcome in broken],
                "notes": [outcome.note for outcome in broken],
            },
        )

    raise refuse(
        UNREACHABLE_REASON,
        f"none of {', '.join(SOURCES)} could be read, so nothing is known about "
        f"{artist!r} {title!r}. This is not the same as the catalogues not "
        f"carrying it, and it is not recorded as one",
        remedy=Remedy.RETRY_LATER,
        steps=(
            "check this machine's network connection and run the tagging job again; "
            "the job resumes at the item it stopped on",
        ),
        scope=Scope.RUN,
        retryable=True,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
        },
    )


def catalogue_searcher(
    declared: Taxonomy,
    *,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
    pacing: Pacer | None = None,
) -> Searcher:
    """Build the searcher that asks the three catalogues, in order.

    A factory rather than a module level function because
    :data:`cratekit.tagging.tag.Searcher` is ``(artist, title) -> SearchHit |
    None`` and cannot carry a taxonomy or a seam. Both bind here, once, at
    construction.

    An explicit ``pacing`` keeps its OWN sleep. Passing both is a caller saying
    two different things about one schedule, and the more specific object is the
    one that meant it.
    """
    naps = time.sleep if sleep is None else sleep
    pacer = Pacer(sleep=naps) if pacing is None else pacing
    touch = default_fetch(sleep=naps) if fetch is None else fetch

    def search(artist: str, title: str) -> SearchHit | None:
        outcomes: list[SourceOutcome] = []
        for ask in _SEARCHES:
            outcome = ask(artist, title, fetch=touch, pacer=pacer, declared=declared)
            outcomes.append(outcome)
            if outcome.answer is Answer.MATCHED:
                return _resolved(declared, outcome)
        return _decide(outcomes, artist, title)

    return search


def for_taxonomy(declared: Taxonomy) -> Searcher:
    """The searcher a worker should use, looked up rather than constructed.

    ``ItemHandler`` is a fixed callable, so a worker that built its own searcher
    inline would leave a test nowhere to hand in a fake and R18's no network
    proof unwritable. A worker calls this at call time and a test replaces this
    attribute on this module, which is the shipped shape
    :func:`cratekit.modules.outbound.account.resolve` already uses.

    THE SUBSTITUTION IS IN PROCESS ONLY. The child that ``crate job resume``
    spawns is a fresh process and inherits nothing patched here, so a detached
    run always gets the live searcher. R-226, recorded rather than worked around.

    ``declared`` is required and is the library's active taxonomy (R-685); a
    shipped default reached for here tagged by a declaration the library does
    not hold.
    """
    return catalogue_searcher(declared)


def for_images() -> FetchImage:
    """The image fetch a worker should use, looked up rather than constructed.

    The same shape and the same reason as :func:`for_taxonomy`: a test replaces
    this attribute on this module, and a worker that built its own fetch inline
    would leave it nowhere to hand a fake in. Building one touches no network.
    R-226's limit applies here too.
    """
    return default_image_fetch()


__all__ = [
    "BANDCAMP",
    "BANDCAMP_SEARCH",
    "BEATPORT",
    "BEATPORT_IMAGE_EDGE",
    "BEATPORT_SEARCH",
    "HEADERS",
    "JITTER_FRACTION",
    "MIN_INTERVAL_S",
    "PARSE_BREAK_REASON",
    "RATE_LIMIT_ATTEMPTS",
    "RATE_LIMIT_BASE_WAIT_S",
    "REQUEST_TIMEOUT_S",
    "SOURCES",
    "TRAXSOURCE",
    "TRAXSOURCE_SEARCH",
    "UNREACHABLE_REASON",
    "Answer",
    "Fetch",
    "Fetched",
    "Pacer",
    "SourceOutcome",
    "catalogue_searcher",
    "default_fetch",
    "default_image_fetch",
    "for_images",
    "for_taxonomy",
]
