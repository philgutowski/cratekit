"""Ask the record catalogues what a track's genre is, or say why nobody answered.

DISCOGS, THEN BEATPORT (U282). Discogs, :mod:`cratekit.tagging.discogs`, is
asked first: it answers per release with styles collectors tagged, and in the
live trial of 2026-11-13 matched nine of ten files while Beatport refused every
lookup. Beatport is asked when Discogs gives no genre, and for the cover, which
Discogs never names. Traxsource and Bandcamp, :mod:`cratekit.tagging.shops`
with Beatport, answer this machine with bot challenges (R-791), so they stay
off the default walk. What every source shares is
:mod:`cratekit.tagging.catalogues`; this module holds the fetch, the walk and
the decision, and keeps every name its callers read off it.

A DISCOGS DECLINE GIVES WAY, A RECORD SHOP'S ENDS THE WALK (U282). When no
style names a folder the walk goes on, and Discogs' word names the file only
if Beatport writes no genre either. A shop's decline is its own word for the
track and carries its row's picture.

ONE QUESTION PER FILE (U289): every source is asked the title past the naming
verb's ``KEY - BPM - `` head (:func:`titles.question`), and its rows are
matched against the file's own text.

``no-hit`` NEEDS EVERY SOURCE ASKED TO HAVE SAID MISS: one beside an unread
source is no absence, so the hit names the unread and the file stays askable.
A refusal by every catalogue asked is said as one (U284), naming each with the
date it began refusing, and the network is the first step only for an outage.

THE GENRE IS RESOLVED BY :func:`cratekit.core.routing.suggest_tag`, never by a
map written here (R19; the suite scans these modules' literals for one). An
answer too coarse to be a final tag is a decline, or the two tagging verbs
would bounce the file between them; an unrecognised one is written and
flagged ``off_taxonomy`` for the report (R-650). A decline still names the
source and the word it declined.

EVERY FETCH IS PACED, THE FIRST INCLUDED, with jitter, so a process the job
engine spawns opens with no burst and two runs do not stay in step. The pacer
is this package's own, not ``acquire.download.Pacing``, which would bind
tagging to acquisition. ``requests`` is named in one function, so the backoff
is driven in the suite with nothing on the network.

Layer: modules.
"""

from __future__ import annotations

import logging
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from types import MappingProxyType
from typing import Any
from urllib.parse import quote_plus

from cratekit.core import art, routing
from cratekit.core.cause import CratekitError, Scope, rebuilt, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging import refused, titles
from cratekit.tagging.catalogues import (
    BANDCAMP,
    BEATPORT,
    CLOUDFLARE_CHALLENGE,
    DISCOGS,
    JITTER_FRACTION,
    MIN_INTERVAL_S,
    NOT_ASKED,
    NOT_SENT,
    PARSE_BREAK_REASON,
    REFUSALS_BEFORE_STOP,
    SCRAPED_WALK,
    SOURCES,
    TRAXSOURCE,
    UNREACHABLE_REASON,
    UNREAD_ANSWERS,
    WALK,
    Answer,
    Fetch,
    Fetched,
    Pacer,
    Refusals,
    SourceOutcome,
    unread_outcome,
)
from cratekit.tagging.catalogues import _title_matches as _title_matches
from cratekit.tagging.discogs import (
    _CREDENTIAL_REASON,
    CREDENTIAL_REASON,
    DISCOGS_API,
    DISCOGS_CREDENTIAL,
    DISCOGS_IDENTITY,
    DISCOGS_LOGIN_STEPS,
    DISCOGS_NO_TOKEN,
    DISCOGS_RELEASE,
    DISCOGS_RELEASES_READ,
    DISCOGS_REMAINING_FLOOR,
    DISCOGS_REMAINING_HEADER,
    DISCOGS_RESULTS_PER_PAGE,
    DISCOGS_SEARCH,
    DISCOGS_SLOWDOWN_S,
    DISCOGS_TOKEN_LOST,
    DISCOGS_TOKEN_REFUSED,
    DISCOGS_UNASKED_NOTES,
    DiscogsAsker,
    NotAsked,
    TokenCheck,
    TokenVerdict,
    _recorded_token,
    discogs_headers,
)
from cratekit.tagging.shops import (
    BANDCAMP_SEARCH,
    BEATPORT_IMAGE_EDGE,
    BEATPORT_SEARCH,
    TRAXSOURCE_SEARCH,
    _search_bandcamp,
    _search_beatport,
    _search_traxsource,
)
from cratekit.tagging.shops import _beatport_best as _beatport_best
from cratekit.tagging.tag import FetchImage, Searcher, SearchHit, SourceAnswer

log = logging.getLogger(__name__)

#: A request with no timeout blocks for ever, which looks exactly like work.
#: Fifteen seconds is the value the live system already paid for.
REQUEST_TIMEOUT_S = 15.0

#: The first wait after a rate limit answer, growing linearly with each
#: attempt: a shorter wait lands inside the window that refused the first.
RATE_LIMIT_BASE_WAIT_S = 30.0

#: Total attempts per fetch, the first included, so a spent rate limit is
#: reportable as UNREACHABLE instead of a loop that looks like work.
RATE_LIMIT_ATTEMPTS = 3

#: One browser identity for every page request. A catalogue that sees a client
#: library's user agent answers a different page, or none.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

#: Cloudflare's mitigation header and its challenge value, read only to say
#: what refused this client.
_CF_MITIGATED = "cf-mitigated"
_CF_CHALLENGE = "challenge"


def _requests_get(url: str, *, headers: dict[str, str], timeout: float) -> Any:
    """The one place ``requests`` is named, so every fetch takes a getter and
    the suite drives the backoff, and detonates this, with no network."""
    import requests  # noqa: PLC0415

    return requests.get(url, headers=headers, timeout=timeout)


def default_fetch(
    *,
    get: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    headers: dict[str, str] | None = None,
) -> Fetch:
    """The shipped fetch seam: one GET, one timeout, one rate limit policy.

    ``headers`` is :data:`HEADERS`, a browser's, unless a caller asking an API
    names its own. R22's classification lives here alone: a transport failure
    or a non 200 other than 429 is unreachable at once, and a 429 retries until
    the attempt cap is spent, with no wait after the last.
    """
    getter = _requests_get if get is None else get
    sent = HEADERS if headers is None else headers

    def fetch(url: str) -> Fetched:
        response, note, status = _answered(getter, sleep, url, sent)
        if response is None:
            return Fetched(note=note, status=status)
        return Fetched(text=response.text, status=status, headers=_headers_of(response))

    return fetch


def _headers_of(response: Any) -> Mapping[str, str]:
    """The answer's headers with lowercased names, since a name is case blind
    on the wire, or none when it carries none."""
    raw = getattr(response, "headers", None)
    if not isinstance(raw, Mapping):
        return MappingProxyType({})
    return MappingProxyType({str(name).lower(): str(value) for name, value in raw.items()})


def _answered(
    getter: Callable[..., Any],
    sleep: Callable[[float], None],
    url: str,
    headers: dict[str, str] = HEADERS,
) -> tuple[Any, str, int | None]:
    """One GET under the rate limit policy: the 200 response, or None and why,
    with the last status, None when the transport failed. Shared by the page
    and the image fetch, so a picture is asked on a search page's terms."""
    for attempt in range(RATE_LIMIT_ATTEMPTS):
        try:
            response = getter(url, headers=headers, timeout=REQUEST_TIMEOUT_S)
        # A bare except, on purpose: every way a transport fails is one fact,
        # and naming one client library's classes would let the next through.
        except Exception as exc:  # noqa: BLE001
            return None, f"transport failure: {exc}", None
        status = getattr(response, "status_code", None)
        if status == 429:
            if attempt + 1 < RATE_LIMIT_ATTEMPTS:
                sleep(RATE_LIMIT_BASE_WAIT_S * (attempt + 1))
                continue
            return (
                None,
                f"rate limited, {RATE_LIMIT_ATTEMPTS} attempts spent without an answer",
                status,
            )
        if status != 200:
            return None, _refusal_note(response, status), status
        return response, "", status
    return None, "rate limited, attempts spent", 429


def _refusal_note(response: Any, status: object) -> str:
    """``HTTP <status>``, named a Cloudflare challenge when its ``Cf-Mitigated``
    header says so (U281)."""
    mitigated = _headers_of(response).get(_CF_MITIGATED, "")
    if mitigated.strip().lower() == _CF_CHALLENGE:
        return f"{CLOUDFLARE_CHALLENGE}, HTTP {status}"
    return f"HTTP {status}"


def default_image_fetch(
    *,
    get: Callable[..., Any] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    pacing: Pacer | None = None,
) -> FetchImage:
    """The shipped image seam: a paced GET, answering bytes or None.

    Paced like a search, since a folder of new files is a burst on the same
    servers. None for every failure, since a picture that cannot be had is a
    decline for its file; the reason is logged, having nowhere else to go.
    """
    getter = _requests_get if get is None else get
    pacer = Pacer(sleep=sleep) if pacing is None else pacing

    def fetch_image(url: str) -> bytes | None:
        pacer.wait()
        response, note, _status = _answered(getter, sleep, url)
        if response is None:
            log.debug("picture fetch failed for %s: %s", url, note)
            return None
        data = getattr(response, "content", None)
        return bytes(data) if data else None

    return fetch_image


#: How many addresses' pictures the worker's fetch keeps, least recently used
#: dropped first. A sweep takes files in path order, so an album's files sit
#: together and a few covers serve a landed folder.
IMAGE_MEMORY = 4


def remembering(
    fetch_image: FetchImage,
    *,
    keep: int | None = None,
    admit: Callable[[bytes], bool] | None = None,
) -> FetchImage:
    """``fetch_image``, answering an address it already fetched from memory.

    Keyed on the address as named; the encode is remembered on the bytes, by
    :func:`cratekit.core.art.to_cdj_jpeg_remembered`. Only an answer is
    remembered: a raise, None, nothing or bytes ``admit`` refuses is handed
    back and kept nowhere, so the next file asks again. A remembered answer
    makes no request and waits on no pacer. ``keep`` defaults to
    :data:`IMAGE_MEMORY`, read at each call.
    """
    held: OrderedDict[str, bytes] = OrderedDict()
    lock = threading.Lock()

    def fetch(url: str) -> bytes | None:
        with lock:
            data = held.get(url)
            if data is not None:
                held.move_to_end(url)
                return data
        data = fetch_image(url)
        if not data or (admit is not None and not admit(data)):
            return data
        with lock:
            held[url] = data
            held.move_to_end(url)
            bound = IMAGE_MEMORY if keep is None else keep
            while len(held) > bound:
                held.popitem(last=False)
        return data

    return fetch


def _query(artist: str, title: str) -> str:
    """One escaped query string for a record shop's search page, such as
    https://www.beatport.com/search?q=, handed to each shop as ``query``.

    Escaping is not cosmetic: an unescaped ampersand truncates the query and
    reports another search's page as a miss.
    """
    return quote_plus(f"{artist} {title}".strip())


def discogs_asker(
    *,
    token: str | None,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
    pacing: Pacer | None = None,
    unasked: str = DISCOGS_NO_TOKEN,
) -> DiscogsAsker:
    """Build the asker. With no token it asks nothing, and needs no fetch.

    The default fetch sends :func:`discogs_headers` under the shared timeout
    and rate limit ladder. An explicit ``pacing`` keeps its own sleep.
    """
    naps = time.sleep if sleep is None else sleep
    pacer = Pacer(sleep=naps) if pacing is None else pacing
    if fetch is None:
        sent = discogs_headers(token) if token is not None else {}
        fetch = default_fetch(sleep=naps, headers=sent)
    return DiscogsAsker(token=token, fetch=fetch, pacer=pacer, unasked=unasked)


def check_discogs_token(
    token: str,
    *,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
) -> TokenCheck:
    """Whether Discogs accepts ``token``, asked through a fresh asker built as
    a sweep builds one, never the process's shared one, which holds the
    recorded token."""
    return discogs_asker(token=token, fetch=fetch, sleep=sleep).identity()


#: The one asker this process asks Discogs through, built on first use.
_shared_discogs: list[DiscogsAsker] = []


def for_discogs() -> DiscogsAsker:
    """The asker a worker should use, one per process, looked up at call time.

    One per process, so the pacer, the remaining count and a refusal are the
    run's and not a file's. A test replaces this attribute. Building one reads
    the keychain and touches no network.
    """
    if not _shared_discogs:
        token, note = _recorded_token()
        _shared_discogs.append(discogs_asker(token=token, unasked=note or DISCOGS_NO_TOKEN))
    return _shared_discogs[0]


def choose_word(
    declared: Taxonomy, words: Sequence[str], *, source: str, named_only: bool
) -> tuple[str, str] | None:
    """The first of a source's words that maps to a folder, with the tag to write.

    Shared by Discogs' styles and the general catalogue's album genres. "Maps
    to a folder" is the shipped resolver naming a bucket, not declining, not
    too coarse to be a final tag and not the fallback; with ``named_only`` the
    tag must also name a folder by an exact declaration. In the source's order,
    the only ranking it publishes.
    """
    fallback = declared.fallback.bucket
    for word in words:
        suggestion = routing.suggest_tag(declared, word, source=source)
        tag = suggestion.tag
        if suggestion.declined or not tag:
            continue
        bucket = suggestion.bucket_id or declared.bucket_for_display(tag)
        if bucket is None or bucket == fallback:
            continue
        if declared.is_too_coarse_as_source(tag):
            continue
        if named_only and declared.named_folder(tag) is None:
            continue
        return word, tag
    return None


#: The record shops asked by artist and title through the shared fetch seam;
#: Discogs is asked through its asker, which holds a token.
_SEARCHES: Mapping[str, Callable[..., SourceOutcome]] = MappingProxyType(
    {
        BEATPORT: _search_beatport,
        TRAXSOURCE: _search_traxsource,
        BANDCAMP: _search_bandcamp,
    }
)


def _answers(
    walk: Sequence[str],
    outcomes: Sequence[SourceOutcome],
    passed: Sequence[NotAsked] = (),
) -> tuple[SourceAnswer, ...]:
    """Every source of the walk's answer, in the walk's order, ``not-asked`` for
    the rest, so a record never leaves a skipped catalogue to be inferred."""
    said = {outcome.source: outcome for outcome in outcomes}
    why = {skipped.source: skipped.note for skipped in passed}
    return tuple(
        SourceAnswer(
            source=source,
            answer=said[source].answer.value,
            source_genre=said[source].source_genre,
            note=said[source].note,
        )
        if source in said
        else SourceAnswer(source=source, answer=NOT_ASKED, note=why.get(source, ""))
        for source in walk
    )


def _unread_sources(
    outcomes: Sequence[SourceOutcome], passed: Sequence[NotAsked] = ()
) -> tuple[str, ...]:
    """The sources whose answer said nothing about the track, the ones passed
    over for want of a credential included (U244). On a match too, so a
    record's ``unread`` and its answers never disagree."""
    return tuple(
        outcome.source
        for outcome in outcomes
        if outcome.answer not in (Answer.MISS, Answer.MATCHED)
    ) + tuple(skipped.source for skipped in passed)


def _resolved(declared: Taxonomy, outcome: SourceOutcome) -> SearchHit:
    """Turn one catalogue's raw genre into the tag to write, or into a decline
    that still says what it declined. ``off_taxonomy`` rides only a genre that
    is going to be written: a file gets one disposition, never two."""
    if outcome.words:
        # The first word that names a folder (U244); with none, a decline
        # naming the first word, since a style written raw names no folder.
        picked = choose_word(declared, outcome.words, source=outcome.source, named_only=True)
        return SearchHit(
            genre=picked[1] if picked else None,
            source=outcome.source,
            source_genre=picked[0] if picked else outcome.source_genre,
            art_url=outcome.art_url,
        )
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


def _decide(
    walk: Sequence[str],
    outcomes: Sequence[SourceOutcome],
    passed: Sequence[NotAsked],
    artist: str,
    title: str,
) -> SearchHit:
    """Refuse, or return the decline, once every source has been asked.

    A decline needs one source that ANSWERED, and is ``no-hit`` only when every
    source asked said MISS; unread sources beside a MISS ride ``unread``
    (R-791), as does one passed over for want of a token (U244). Only when
    nobody answered is it a refusal, and a parse break beats an unreachable,
    since a broken parser is actionable today and a network is not. A walk
    that asked nothing is a decline naming what it passed over, never an
    outage. The decline is a :class:`SearchHit` with no genre, which carries
    the answers the record owes.
    """
    if not outcomes or any(outcome.answer is Answer.MISS for outcome in outcomes):
        return SearchHit(
            answers=_answers(walk, outcomes, passed),
            unread=_unread_sources(outcomes, passed),
        )

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

    blocked = [outcome.source for outcome in outcomes if outcome.answer is Answer.BLOCKED]
    if len(blocked) == len(outcomes):
        raise _refused_by_all(outcomes, passed, artist, title)
    steps = [
        "check this machine's network connection and run the tagging job again; "
        "the job resumes at the item it stopped on",
    ]
    if blocked:
        steps.append(
            f"{', '.join(blocked)} refused this client, with a bot check, a block "
            f"page or a rate limit that outlasted the backoff, rather than a "
            f"result; this tool does not try to get past one, so those catalogues "
            f"stay unread until they answer this machine again"
        )
    steps.extend(f"{skipped.source} was {skipped.note}" for skipped in passed)
    asked = ", ".join(outcome.source for outcome in outcomes)
    raise refuse(
        UNREACHABLE_REASON,
        f"none of {asked} could be read, so nothing is known about "
        f"{artist!r} {title!r}. This is not the same as the catalogues not "
        f"carrying it, and it is not recorded as one",
        remedy=Remedy.RETRY_LATER,
        steps=tuple(steps),
        scope=Scope.RUN,
        retryable=True,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "answers": [outcome.answer.value for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
        },
    )


#: The detail keys of a refusal by every catalogue asked (U284): each refusing
#: catalogue with the date it began, and the note Discogs was passed over with.
REFUSED_DETAIL = "refused"
DISCOGS_DETAIL = "discogs"


def refusing_since(since: Mapping[str, str]) -> str:
    """The refusing catalogues in words, each with the date it began when one is recorded."""
    return ", ".join(
        f"{source}, refusing since {began}" if began else source
        for source, began in since.items()
    )


def _refused_by_all(
    outcomes: Sequence[SourceOutcome],
    passed: Sequence[NotAsked],
    artist: str,
    title: str,
) -> CratekitError:
    """The refusal of a file every catalogue asked refused, said as a refusal (U284).

    Not an outage, so the network is not the first step; the slug and the retry
    stay, since nothing is known of the track. The token is named when Discogs
    went unasked for want of one, because with one recorded such a file is
    left askable and a pass carries on to its landing (#790).
    """
    since = refused.since(outcome.source for outcome in outcomes)
    named = refusing_since(since)
    unasked = next((skipped.note for skipped in passed if skipped.source == DISCOGS), "")
    steps: list[str] = []
    if unasked:
        steps.append(
            f"record a Discogs token, then run the tagging job again: "
            f"{DISCOGS_LOGIN_STEPS}. With one recorded Discogs is asked first, "
            f"and a file it searched and could not tag while every other "
            f"catalogue refuses is left untagged and askable rather than "
            f"failing, so a sync pass or a label go carries on to its landing"
        )
    steps.append(
        f"{', '.join(since)} refused this client, with a bot check, a block page "
        f"or a rate limit that outlasted the backoff, rather than a result; this "
        f"tool does not try to get past one, so a later run asks again and the "
        f"job resumes at the item it stopped on"
    )
    steps.extend(f"{skipped.source} was {skipped.note}" for skipped in passed)
    return refuse(
        UNREACHABLE_REASON,
        f"every catalogue asked refused this client: {named}, so nothing is "
        f"known about {artist!r} {title!r}. A refusal is not the catalogues not "
        f"carrying it, and it is not recorded as one",
        remedy=Remedy.RETRY_LATER,
        steps=tuple(steps),
        scope=Scope.RUN,
        retryable=True,
        origin=("tagging", "searchers"),
        detail={
            "sources": [outcome.source for outcome in outcomes],
            "answers": [outcome.answer.value for outcome in outcomes],
            "notes": [outcome.note for outcome in outcomes],
            REFUSED_DETAIL: since,
            DISCOGS_DETAIL: unasked,
        },
    )


def _beside_refusals(rejected: CratekitError, outcomes: Sequence[SourceOutcome]) -> CratekitError:
    """A token Discogs rejected, naming the record shops that refused too, and
    since when, when every shop asked refused (U284)."""
    if not outcomes or any(outcome.answer is not Answer.BLOCKED for outcome in outcomes):
        return rejected
    since = refused.since(outcome.source for outcome in outcomes)
    cause = rejected.cause
    return rebuilt(
        rejected,
        replace(
            cause,
            remediation=replace(
                cause.remediation,
                steps=(
                    *cause.remediation.steps,
                    f"meanwhile every record shop asked refused this client too: "
                    f"{refusing_since(since)}",
                ),
            ),
            detail={
                **dict(cause.detail or {}),
                REFUSED_DETAIL: since,
                DISCOGS_DETAIL: DISCOGS_TOKEN_REFUSED,
            },
        ),
    )


def catalogue_searcher(
    declared: Taxonomy,
    *,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
    pacing: Pacer | None = None,
    walk: Sequence[str] = WALK,
    discogs: DiscogsAsker | None = None,
    refusals: Refusals | None = None,
) -> Searcher:
    """Build the searcher that asks the walk's catalogues, in order.

    ``walk`` names each of :data:`SOURCES` at most once. ``discogs`` is the
    asker; with none, Discogs has no token and is ``not-asked``, so a direct
    caller never reaches the keychain. An explicit ``pacing`` keeps its own
    sleep, the more specific object meaning it. ``refusals`` is the run's
    :class:`Refusals` (U281), over the record shops only: Discogs' asker
    remembers its own refusal.

    A match ends the walk, save a Discogs decline, which is held while the
    shops are asked (U282); a genre Discogs decided carries the picture's
    question over the shops after it, :func:`_pictured`.
    """
    order = tuple(walk)
    unknown = [source for source in order if source not in SOURCES]
    if unknown or len(set(order)) != len(order):
        raise ValueError(
            f"a walk names each of {', '.join(SOURCES)} at most once, not {order!r}"
        )
    naps = time.sleep if sleep is None else sleep
    pacer = Pacer(sleep=naps) if pacing is None else pacing
    touch = default_fetch(sleep=naps) if fetch is None else fetch
    asker = discogs_asker(token=None, sleep=naps) if discogs is None else discogs
    counted = Refusals() if refusals is None else refusals

    def shop(source: str, artist: str, title: str, track: str) -> SourceOutcome:
        """One record shop's answer, or the run's word that it is not sent (U281).
        Asked for ``track``, matched against ``title`` (U289)."""
        stopped = counted.stopped(source)
        if stopped is not None:
            return stopped
        outcome = _SEARCHES[source](
            artist, title, fetch=touch, pacer=pacer, declared=declared, track=track, query=_query
        )
        counted.heard(outcome)
        return outcome

    def search(artist: str, title: str) -> SearchHit | None:
        # The question is read once and every source is asked it (U289); the
        # hit carries it, so the record says what was asked.
        asked = titles.question(title, artist)
        hit = answer(asked.artist, title, asked.title)
        return None if hit is None else replace(hit, asked=asked)

    def answer(artist: str, title: str, track: str) -> SearchHit | None:
        outcomes: list[SourceOutcome] = []
        passed: list[NotAsked] = []
        declined: SearchHit | None = None
        shown: SourceOutcome | None = None
        rejected: CratekitError | None = None
        for place, source in enumerate(order):
            if source == DISCOGS:
                try:
                    said = asker.ask(artist, title, track=track)
                except CratekitError as refusal:
                    # A rejected token waits for the record shops (U282's
                    # review): raised at once, it would stop every file before
                    # Beatport; held, it is raised only when no shop matched.
                    if refusal.cause.reason != _CREDENTIAL_REASON:
                        raise
                    rejected = refusal
                    passed.append(
                        NotAsked(DISCOGS, f"{DISCOGS_TOKEN_REFUSED}{refusal.cause.message}")
                    )
                    continue
                if isinstance(said, NotAsked):
                    passed.append(said)
                    continue
                outcome = said
            else:
                outcome = shop(source, artist, title, track)
            outcomes.append(outcome)
            if outcome.answer is not Answer.MATCHED:
                continue
            if source in _SEARCHES:
                shown = outcome
            resolved = _resolved(declared, outcome)
            if resolved.genre is None and source not in _SEARCHES:
                # A Discogs decline gives way to the shops (U282); its word
                # names the file only if none of them writes a genre.
                declined = declined or resolved
                continue
            hit = replace(
                declined if resolved.genre is None and declined is not None else resolved,
                answers=_answers(order, outcomes, passed),
                unread=_unread_sources(outcomes, passed),
            )
            if hit.source in _SEARCHES:
                return hit
            if hit.genre is None:
                return _lent(hit, shown)
            return _pictured(hit, order[place + 1 :], artist, title, track, shop)
        if declined is not None:
            return _lent(
                replace(
                    declined,
                    answers=_answers(order, outcomes, passed),
                    unread=_unread_sources(outcomes, passed),
                ),
                shown,
            )
        if rejected is not None:
            raise _beside_refusals(rejected, outcomes) from rejected.__cause__
        return _decide(order, outcomes, passed, artist, title)

    return search


def _lent(hit: SearchHit, shown: SourceOutcome | None) -> SearchHit:
    """A hit from a source that names no picture, given the one a record shop's
    matched row named, or nobody's: never the hit's source, which is not asked
    for one."""
    if shown is None:
        return replace(hit, art_url="", art_source="")
    return replace(hit, art_url=shown.art_url, art_source=shown.source)


def _pictured(
    hit: SearchHit,
    rest: Sequence[str],
    artist: str,
    title: str,
    track: str,
    shop: Callable[[str, str, str, str], SourceOutcome],
) -> SearchHit:
    """A genre decided by a source that names no picture, with the picture's question (U282).

    The shops the walk never reached ride the hit as ``ask_picture``, asked by
    :func:`cratekit.tagging.tag.tag_one` only for a file with no picture, and
    recorded ``not-asked`` until then. It asks them in the walk's order under
    the run's count of refusals until one matches, whose row names the
    picture whatever its genre; a refusal or an outage joins ``unread``.
    """
    lent = _lent(hit, None)
    later = tuple(source for source in rest if source in _SEARCHES)
    if not later:
        return lent
    note = (
        f"{NOT_SENT}{hit.source} gave the genre, and a record shop after it is "
        f"asked only for the picture of a file that has none"
    )
    waiting = tuple(
        replace(said, note=note) if said.source in later else said for said in lent.answers
    )

    def ask_picture(current: SearchHit) -> SearchHit:
        answers = list(current.answers)
        unread = list(current.unread)
        for source in later:
            outcome = shop(source, artist, title, track)
            entry = SourceAnswer(
                source=source,
                answer=outcome.answer.value,
                source_genre=outcome.source_genre,
                note=outcome.note,
            )
            answers = [entry if said.source == source else said for said in answers]
            if outcome.answer.value in UNREAD_ANSWERS and source not in unread:
                unread.append(source)
            if outcome.answer is Answer.MATCHED:
                return replace(
                    current,
                    answers=tuple(answers),
                    unread=tuple(unread),
                    art_url=outcome.art_url,
                    art_source=source,
                )
        return replace(current, answers=tuple(answers), unread=tuple(unread))

    return replace(lent, answers=waiting, ask_picture=ask_picture)


def for_taxonomy(declared: Taxonomy, *, refusals: Refusals | None = None) -> Searcher:
    """The searcher a worker should use, looked up rather than constructed.

    A worker calls this at call time so a test can replace it on this module
    (R18); a child ``crate job resume`` spawns inherits no patch (R-226).
    ``declared`` is the library's active taxonomy (R-685). ``refusals`` is the
    run's count, :func:`for_run`'s (U281); with none, it lasts this searcher.
    """
    return catalogue_searcher(declared, discogs=for_discogs(), refusals=refusals)


#: The run whose refusals this process is counting, and the count (U281). One
#: slot, since a process drives one run at a time.
_run_refusals: list[tuple[str, Refusals]] = []


def for_run(run: str) -> Refusals:
    """The refusal count of the run named ``run``, looked up rather than kept by a worker.

    The same name returns the same count, any other a fresh one; a sweep names
    its run by job and attempt, so a resumed run asks again from its first
    file (U281). The one count that keeps the record of when each catalogue
    began refusing (U284). A test replaces this attribute.
    """
    if not _run_refusals or _run_refusals[0][0] != run:
        _run_refusals[:] = [(run, Refusals(record=True))]
    return _run_refusals[0][1]


def reset_runs() -> None:
    """Forget the run whose refusals were being counted."""
    _run_refusals.clear()


#: The one image fetch this process asks through, built on first use (U260).
_images: list[FetchImage] = []


def for_images() -> FetchImage:
    """The image fetch a worker should use, looked up as :func:`for_taxonomy` is.

    One per process (U260), so an album's files, which name one address, meet
    the same memory; the run's process holds it and :func:`reset_images` drops
    it. Building one touches no network.
    """
    if not _images:
        _images.append(remembering(default_image_fetch(), admit=art.decodes))
    return _images[0]


def reset_images() -> None:
    """Forget the shared image fetch and every picture it remembered."""
    _images.clear()


__all__ = [
    "BANDCAMP", "BANDCAMP_SEARCH", "BEATPORT", "BEATPORT_IMAGE_EDGE", "BEATPORT_SEARCH",
    "CLOUDFLARE_CHALLENGE", "CREDENTIAL_REASON", "DISCOGS", "DISCOGS_API", "DISCOGS_CREDENTIAL",
    "DISCOGS_IDENTITY", "DISCOGS_LOGIN_STEPS", "DISCOGS_NO_TOKEN", "DISCOGS_RELEASE",
    "DISCOGS_RELEASES_READ", "DISCOGS_REMAINING_FLOOR", "DISCOGS_REMAINING_HEADER",
    "DISCOGS_RESULTS_PER_PAGE", "DISCOGS_SEARCH", "DISCOGS_SLOWDOWN_S", "DISCOGS_TOKEN_LOST",
    "DISCOGS_TOKEN_REFUSED", "DISCOGS_DETAIL", "DISCOGS_UNASKED_NOTES", "HEADERS", "IMAGE_MEMORY",
    "JITTER_FRACTION", "MIN_INTERVAL_S", "NOT_ASKED", "NOT_SENT", "PARSE_BREAK_REASON",
    "SCRAPED_WALK", "RATE_LIMIT_ATTEMPTS", "RATE_LIMIT_BASE_WAIT_S", "REFUSALS_BEFORE_STOP",
    "REQUEST_TIMEOUT_S", "SOURCES", "TRAXSOURCE", "TRAXSOURCE_SEARCH", "REFUSED_DETAIL",
    "UNREACHABLE_REASON", "UNREAD_ANSWERS", "WALK", "Answer", "DiscogsAsker", "Fetch", "Fetched",
    "NotAsked", "Pacer", "Refusals", "SourceOutcome", "TokenCheck", "TokenVerdict",
    "catalogue_searcher", "check_discogs_token", "choose_word", "default_fetch",
    "default_image_fetch", "discogs_asker", "discogs_headers", "for_discogs", "for_images",
    "for_run", "for_taxonomy", "remembering", "reset_images", "refusing_since", "reset_runs",
    "unread_outcome",
]
