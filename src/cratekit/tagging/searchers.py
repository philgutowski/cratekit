"""Ask the record catalogues what a track's genre is, or say why nobody answered.

DISCOGS, THEN BEATPORT (U282). Discogs is asked first, through its documented
API with a person's own token, because it answers, per release, with styles
DJs and collectors tagged: in the live trial of 2026-11-13 it matched nine of
ten untagged files while Beatport refused every lookup. Beatport is asked when
Discogs gives no genre, by a miss, a decline, a refusal or no token recorded,
and it still carries the cover, which Discogs never names (the picture section
below). U244 asked them the other way round. The two record shop pages that
followed Beatport before U244, Traxsource and Bandcamp, answer this machine
with bot challenges on every search (R-791). Their parsers stay in the tree
and off the walk, so a record of what they answered still reads, and a walk
that names them still drives them. See the Discogs section below for what
that source answers and why.

A DECLINE FROM DISCOGS GIVES WAY; A RECORD SHOP'S ENDS THE WALK (U282). When
none of a release's styles names a folder, the walk goes on to Beatport, and
Discogs' first style names the file only if Beatport writes no genre either:
beside a Beatport miss the file is ``unmapped-genre`` with that word, and
beside a Beatport refusal it is the same with Beatport unread, never a
``no-hit`` and never an outage, since Discogs was read. A record shop's
decline is its own word for the track and carries its row's picture, and on
any walk it settles the file as it always has.

WHY THE OUTCOME OF ONE SOURCE HAS FOUR VALUES AND NOT TWO. The obvious shape is
a genre or nothing, and it is the shape that quietly ruins a library. A source
that could not be reached returns nothing, a source whose markup changed returns
nothing, and a source that answered and did not carry the track returns nothing,
so a folder swept during an outage completes clean and every file in it is
recorded as a track the catalogues do not know. Absence read as evidence of
absence is the first failure pattern METHOD names, and this module is where it
would enter the tagging verbs. So each source answers MATCHED, MISS, UNREACHABLE,
BLOCKED or PARSE_BREAK, and only MISS is permitted to contribute to a decline.

A BOT CHALLENGE IS AN ANSWER OF ITS OWN, AND RECOGNISING IT IS THE WHOLE REMEDY
(R-791). Measured from the author's machine on 2026-10-01 with these headers,
Traxsource answered 403 with Cloudflare's "Just a moment..." page and Bandcamp
answered 200 with a "Client Challenge" page carrying no rows. The second read as
a MISS, so a Beatport miss turned every such file into a clean ``no-hit`` and
the two fallbacks vanished from the record. A fallback page recognised as a
challenge or a block is BLOCKED, and nothing here tries to get past one: no
header trick, no browser, no solver.

BEATPORT'S REFUSAL IS READ THE SAME WAY SINCE U281. R-791 left Beatport out of
the check because it was answering then. From 2026-11-13 it answered every
lookup from the author's machine with a 403 carrying ``Cf-Mitigated:
challenge``, which read as ``unreachable`` and sent a person to their network,
so a Beatport page with no payload to parse, a refusal or a challenge page,
goes through :func:`unread_outcome`, and a 200 challenge page from it is
BLOCKED rather than a parse break (R-794). A page that carries the payload is
read as results whatever script it carries.

A RUN STOPS ASKING A CATALOGUE THAT REFUSED IT THREE TIMES IN A ROW (U281).
:class:`Refusals` counts one run's refusals in a row per catalogue, and once a
catalogue reaches :data:`REFUSALS_BEFORE_STOP` the walk sends it nothing more
in that run: each later file records it BLOCKED with a note saying it was not
asked and why, so it stays among the unread sources and the file stays
askable. Any other answer from it ends the run of refusals, the next run asks
again from its first file, and Discogs keeps its own memory and is asked
whatever Beatport said. A picture's question asks Beatport under the same
count (U282).

``no-hit`` NEEDS EVERY SOURCE ASKED TO HAVE SAID MISS. One MISS beside a source
that could not be read is not an absence, because the unread one may carry the
track, so the hit says which sources went unread and the file stays untagged
and askable. Every source's answer rides the hit either way, so a later reader
can tell what each catalogue said.

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
page image, and Traxsource names none, which is parity. Discogs names none
either: its covers are out of U244's scope, and Beatport stays the art source.
SO A GENRE DISCOGS DECIDED LEAVES THE PICTURE'S QUESTION OPEN (U282). The hit
carries it, ``ask_picture``, over the record shops the walk never reached,
and :func:`cratekit.tagging.tag.tag_one` asks it only for a file with no
picture, so the cover arrives from the row it arrived from before Discogs was
asked first, and a file that has one, ``tag suggest`` and ``tag retag`` send
Beatport nothing after a Discogs match. A Discogs decline beside a Beatport
row that matched takes that row's picture. The image is fetched
later, and only for a file with no picture, by :func:`default_image_fetch`,
which shares this module's pacer shape and rate limit policy. An album's files
name one address, so the worker's fetch, :func:`for_images`, is one per process
and remembers the bytes the last few addresses answered (U260): an album whose
files sit together in the sweep costs one paced request, not one per track.

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
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from typing import Any
from urllib.parse import quote_plus, urlencode

from cratekit import __version__
from cratekit.core import art, routing, secrets
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.taxonomy import Taxonomy
from cratekit.tagging import titles
from cratekit.tagging.tag import FetchImage, Searcher, SearchHit, SourceAnswer

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
DISCOGS = "discogs"
TRAXSOURCE = "traxsource"
BANDCAMP = "bandcamp"

#: Every source a file's record can name, in the order a record lists them.
#: Readers of records count over this, so a record written before U244, when
#: the walk was Beatport, Traxsource and Bandcamp, still summarises.
#: Discogs first, as the walk asks it and the tag summary counts it (U282).
SOURCES: tuple[str, ...] = (DISCOGS, BEATPORT, TRAXSOURCE, BANDCAMP)

#: The sources asked, in order, unless a caller names another walk. Discogs
#: first since U282: it answers per release, with styles collectors and DJs
#: tagged, and matched nine of ten untagged files in the live trial of
#: 2026-11-13 while Beatport refused every lookup. Beatport is asked when
#: Discogs gives no genre, by a miss, a decline, a refusal or no token, and
#: for the cover of a file Discogs tagged that has none, since Discogs names
#: no picture. U244 asked them the other way round.
WALK: tuple[str, ...] = (DISCOGS, BEATPORT)

#: The walk before U244, kept so the two scraped parsers stay driven by the
#: suite and a person can still name it. Never the default: both shops refuse
#: this machine with a bot check on every search.
SCRAPED_WALK: tuple[str, ...] = (BEATPORT, TRAXSOURCE, BANDCAMP)

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

#: The statuses a fallback reads as a refusal of this client rather than as a
#: server that could not answer. Cloudflare serves its interstitial with a 403,
#: and a 429 that outlasted the backoff is the catalogue declining to talk to
#: this machine for now.
_BLOCK_STATUSES = frozenset({403, 429})

#: The statuses a Bandcamp track page answers when the listing that named it is
#: dead. No answer about the track, and not an outage either.
_GONE_STATUSES = frozenset({404, 410})

#: The page titles of the two challenge pages measured on 2026-10-01, matched on
#: the TITLE so a track that happens to be called "Just a moment" cannot read as
#: one. Cloudflare's block page, "Attention Required!", is the same refusal in
#: another dress, and its interstitial is written with three dots or with the
#: single ellipsis character depending on the build that served it.
_CHALLENGE_TITLE = re.compile(
    r"<title[^>]*>\s*(just a moment(?:\.\.\.|\u2026)|client challenge|attention required!)",
    re.IGNORECASE,
)

#: The two titles above that are Cloudflare's own pages, rather than a shop's.
_CLOUDFLARE_TITLE = re.compile(r"just a moment|attention required", re.IGNORECASE)

#: The words a note carries when what refused this client was Cloudflare's
#: challenge, spelled once so the tag summary counts those refusals by the same
#: string the note was written with (U281).
CLOUDFLARE_CHALLENGE = "Cloudflare challenge"

#: The header Cloudflare names its mitigation in, and the value it gives for a
#: challenge. Read only to say what refused this client; nothing answers it.
_CF_MITIGATED = "cf-mitigated"
_CF_CHALLENGE = "challenge"

#: The head of the note on an answer a catalogue was never sent, because it had
#: already refused this client in the run (U281, and Discogs' memory since
#: U244). The answer is BLOCKED, so the file stays unread and askable, and the
#: summary tells a refusal sent from one remembered by this head.
NOT_SENT = "not asked: "

#: How many refusals in a row from one catalogue stop a run asking it (U281).
#: Three, because one refusal can be a moment's challenge and three in a row
#: is a catalogue refusing this client, which every further request only
#: confirms at a paced second and a half each.
REFUSALS_BEFORE_STOP = 3

#: Cloudflare's own challenge machinery, present in the body of the interstitial
#: measured on 2026-10-01 whatever its title says. Script paths and a global a
#: bot managed site may also put on an ordinary page, so Beatport reads it only
#: when its page carries no payload (U281); the fallbacks read it first, R-791's
#: order, and their residual says so.
_CHALLENGE_BODY = re.compile(r"/cdn-cgi/challenge-platform/|window\._cf_chl_opt")

#: What the per source record says about a catalogue the walk never reached,
#: because an earlier one matched. Not an :class:`Answer`, which is what a
#: catalogue did when it WAS asked.
NOT_ASKED = "not-asked"


# ---------------------------------------------------------------------------
# The per source outcome, which is this module's core type
# ---------------------------------------------------------------------------


class Answer(Enum):
    """What one catalogue did when it was asked.

    MISS is the only value that means "this catalogue does not carry the track".
    The other four mean, in order, that it does, that we could not ask, that it
    answered with a bot challenge or a block instead of a result, and that we
    asked and could not read the reply.
    """

    MATCHED = "matched"
    MISS = "miss"
    UNREACHABLE = "unreachable"
    BLOCKED = "blocked"
    PARSE_BREAK = "parse-break"


#: The answers that leave the question open: the catalogue was asked and what
#: came back says nothing about the track. One tuple, read by the verb's
#: warnings and by the general catalogue, so the three words are spelled once.
UNREAD_ANSWERS: tuple[str, ...] = (
    Answer.BLOCKED.value,
    Answer.UNREACHABLE.value,
    Answer.PARSE_BREAK.value,
)


@dataclass(frozen=True, slots=True)
class SourceOutcome:
    """One catalogue's answer, with the source that gave it and what it said.

    ``art_url`` is the picture on the row that answered, the same row as
    ``source_genre``, or empty when that row named none.

    ``words`` is every word a source answered when it answers several, in its
    own order, Discogs' styles (U244). Empty for a source that answers one, and
    then ``source_genre`` is the word. When it is not empty the tag is chosen
    among them by :func:`choose_word`, never by ``source_genre`` alone.
    """

    source: str
    answer: Answer
    source_genre: str = ""
    note: str = ""
    art_url: str = ""
    words: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Fetched:
    """One HTTP touch, as either the page text or the reason there is none.

    ``text`` of None IS the unreachable outcome. The fetch seam deliberately does
    not return a :class:`SourceOutcome`, because a fetch is given a URL and knows
    no source name; the caller that knew which catalogue it was asking attaches
    that.

    ``status`` is the HTTP status of the last answer, or None when there was no
    answer at all. It is what lets a fallback tell a 403 block from a server that
    fell over, which the note alone would make a string match.
    """

    text: str | None = None
    note: str = ""
    status: int | None = None
    #: The answer's headers, names lowercased, on a 200 only (U244). Empty for
    #: every other answer and for a fetch that reads none. Discogs reads its
    #: remaining request count here; nothing else does.
    headers: Mapping[str, str] = field(
        default_factory=lambda: MappingProxyType({}), compare=False
    )


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


@dataclass
class Refusals:
    """One run's refusals in a row, per catalogue, and when to stop asking (U281).

    Held BESIDE THE PACER, and like it handed to a searcher rather than kept in
    one, because a worker builds its searcher per file and a count that lived
    in the searcher would start again at every file. A run's worker hands in
    the run's own, :func:`for_run`; a searcher built with none gets a fresh
    one, which lasts as long as that searcher.

    PER CATALOGUE, so a catalogue that refuses never stops another being asked,
    and IN A ROW, so any answer that is not a refusal, a match, a miss, an
    outage or a parse break, ends the run of refusals: only
    :data:`REFUSALS_BEFORE_STOP` refusals with nothing between them stop it.

    A STOPPED CATALOGUE IS ANSWERED BLOCKED, NEVER MISS. The file was not
    asked about and nothing is known of the track, so the answer is the one
    its last refusal gave, with a note saying it was not sent and quoting that
    refusal, and the file stays among the unread and askable.
    """

    limit: int = REFUSALS_BEFORE_STOP
    running: dict[str, int] = field(default_factory=dict)
    last: dict[str, SourceOutcome] = field(default_factory=dict)

    def stopped(self, source: str) -> SourceOutcome | None:
        """The answer for a catalogue this run no longer asks, or None to ask it."""
        if self.running.get(source, 0) < self.limit:
            return None
        return SourceOutcome(
            source,
            Answer.BLOCKED,
            note=(
                f"{NOT_SENT}{source} refused this client on its last {self.limit} "
                f"lookups in this sweep, so it is not asked again until the next "
                f"sweep. Then, {self.last[source].note}"
            ),
        )

    def heard(self, outcome: SourceOutcome) -> None:
        """Count a refusal ``outcome.source`` answered, or end its run of them."""
        if outcome.answer is Answer.BLOCKED:
            self.running[outcome.source] = self.running.get(outcome.source, 0) + 1
            self.last[outcome.source] = outcome
        else:
            self.running.pop(outcome.source, None)
            self.last.pop(outcome.source, None)


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
    headers: dict[str, str] | None = None,
) -> Fetch:
    """The shipped fetch seam: one GET, one timeout, one rate limit policy.

    ``headers`` is what the request says about itself, :data:`HEADERS` unless a
    caller names its own. The three record shop pages are asked as a browser
    because they serve pages; :mod:`cratekit.tagging.published` asks a public
    API and says what it is, and Discogs is asked with
    :func:`discogs_headers` for the same reason.

    R22's classification lives here and nowhere else, so there is one answer to
    "was that source unreachable" rather than three that drift. A transport
    failure and any non 200 other than 429 are unreachable immediately; a 429
    waits and retries until the attempt cap is spent, and a spent cap is
    unreachable rather than a miss.

    The last refusal does NOT sleep on its way out. A wait after the final
    attempt is time spent on a request nobody is going to make.
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
    """The answer's headers with lowercased names, or none when it carries none.

    Lowercased because a header name is case blind on the wire and a reader
    that asked for one spelling would miss the other.
    """
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
    """One GET under the rate limit policy: the 200 response, or None and why.

    The last status rides along, None when the transport itself failed, so a
    caller can tell a block from an outage without reading the note.

    Shared by the page fetch and the image fetch, so a picture is asked for on
    exactly the terms a search page is, one timeout, one backoff, one cap.
    """
    for attempt in range(RATE_LIMIT_ATTEMPTS):
        try:
            response = getter(url, headers=headers, timeout=REQUEST_TIMEOUT_S)
        # A bare except, on purpose. This IS the transport layer, and every
        # way it can fail is one fact: the source could not be read. Naming
        # the exception classes of whatever getter a caller injected would
        # bind this seam to one client library and let the next one through.
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
    """``HTTP <status>``, named a Cloudflare challenge when the answer says it is one.

    Read off the ``Cf-Mitigated`` header Cloudflare sends with its challenge,
    measured on Beatport's 403 on 2026-11-13 (U281). The header is only read,
    to say what refused this client; nothing is sent differently because of it.
    """
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
        response, note, _status = _answered(getter, sleep, url)
        if response is None:
            log.debug("picture fetch failed for %s: %s", url, note)
            return None
        data = getattr(response, "content", None)
        return bytes(data) if data else None

    return fetch_image


#: How many addresses' pictures the worker's fetch keeps, the least recently
#: used dropped first. A sweep takes files in sorted path order, so an album's
#: files usually sit together and a few covers hold every album of a landed
#: folder; a folder interleaving more albums than this asks once per file, as
#: it did before. A few source pictures is little memory.
IMAGE_MEMORY = 4


def remembering(
    fetch_image: FetchImage,
    *,
    keep: int | None = None,
    admit: Callable[[bytes], bool] | None = None,
) -> FetchImage:
    """``fetch_image``, answering an address it already fetched from memory.

    KEYED ON THE ADDRESS EXACTLY AS NAMED, because the address is what was
    asked for; the encode that follows is remembered on the bytes themselves,
    by :func:`cratekit.core.art.to_cdj_jpeg_remembered`, never on this key.

    ONLY AN ANSWER IS REMEMBERED. A fetch that raises raises as it did, and one
    that answers None or nothing, or bytes ``admit`` refuses, is handed back as
    it was and kept nowhere, so the next file naming the address asks again
    exactly as it did before. The shipped admission is
    :func:`cratekit.core.art.decodes`, so bytes that are not a picture are a
    failure each file meets on its own request, never a remembered answer.

    A remembered answer makes no request, so it waits on no pacer; every
    request that IS made still goes through ``fetch_image`` and waits first.
    ``keep`` defaults to :data:`IMAGE_MEMORY`, read at each call.
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


# ---------------------------------------------------------------------------
# Matching, shared by every source asked by artist and title
# ---------------------------------------------------------------------------


#: The matcher itself is :mod:`cratekit.tagging.titles` (U280): these are the
#: few of its readers the searchers below use by their old names.
_normalized = titles.normalized
_identifies = titles.identifies
_words = titles.words
_DASH = titles.DASH

#: The last bracketed group of a title, alone, for the Discogs query: "(Part 1)"
#: of "(Not Just) Knee Deep (Part 1)". Never a reader of a title's words, which
#: :mod:`cratekit.tagging.titles` is.
_LAST_GROUP = re.compile(r"\s*\([^()]*\)\s*$")


def _last_group_stripped(value: str) -> str:
    return _LAST_GROUP.sub("", value).strip()


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


def _title_matches(searched: str, found: str, *, artist: str) -> bool:
    """Whether the file's title, ``searched``, names the same recording as a
    catalogue's title, ``found``, for a file by the searched ``artist``.

    The file's side is read into its parts once (:func:`titles.read_file`),
    the head, a track number, the artist's credit, the title and what follows
    it, and the row by its own structure (:func:`titles.read_row`); they match
    when the file's title and one of the row's titles name one recording, or,
    for a name only a list of version words could read
    (:attr:`titles.Outcome.AMBIGUOUS`), when the row writes the same split of
    a title from its version (:func:`titles.matches`). Whole words, never
    characters, and a side with no letter or digit matches nothing. Every
    reader of a title by artist and title asks this, Discogs included, and
    Beatport's scoring reads the same parse.
    """
    return titles.matches(titles.read_file(searched, artist), titles.read_row(found))


def _query(artist: str, title: str) -> str:
    """One escaped query string for the three record shop pages.

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

    THE TITLE IS READ AS THE SHARED MATCHER READS IT (R-1534, R-1631). A
    title of no letter or digit scores no row, and a row whose name carries
    none is passed over. The title is ranked without its ``KEY - BPM - ``
    head, so a headed file ranks its rows as a plain one does. The top tier
    is the title the row's name with its mix in brackets, so a file's own mix
    outranks the same title's other mixes; the next is the title's core word
    for word the row's name; the last is the shared match
    (:func:`titles.matches`), the title read as a file's and the name as a
    catalogue's, or a split of the file's "Artist - X" name that the row's
    name and mix write together (:func:`titles.read_beatport_row`, R-1646), so a
    row "Love (feat. X)" never scores against "Love Is The
    Message", a row "(Intro)" or "Intro" never against "Sunrise Mood
    (Intro)", and a row "(Sunrise Mood)" never against "Mood". No tier reads
    a row's name inside the title's brackets, or the title inside the name's.
    A credit with no name is no credit: the empty string is in every searched
    artist.
    """
    title_normalized = _normalized(title)
    if not _identifies(title_normalized):
        return None
    proper = titles.without_head(title_normalized)
    whole_title = _words(titles.own_core(proper)[0])
    searched_title = titles.read_file(title_normalized, artist)
    searched = _artist_parts(artist, r"[,&]")

    best_score = 0
    best: _Pick | None = None
    for track in tracks:
        genre = _beatport_genre(track)
        if not genre:
            continue
        name = _normalized(track.get("track_name", ""))
        if not _identifies(name):
            continue
        mix = _normalized(track.get("mix_name", ""))
        credited = [_normalized(entry.get("artist_name", "")) for entry in track.get("artists", [])]
        credited = [other for other in credited if other]

        artist_score = 0
        for part in searched:
            if any(part == other or part in other or other in part for other in credited):
                artist_score += 1
        if artist_score == 0:
            continue

        if _words(proper) == _words(f"{name} ({mix})"):
            title_score = 4
        elif whole_title == _words(name):
            title_score = 3
        elif titles.matches(searched_title, titles.read_beatport_row(name, mix)):
            title_score = 2
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
    # A PAYLOAD IS READ FIRST, AND THE REFUSAL CHECK THE FALLBACKS USE ONLY
    # WHEN THERE IS NONE (U281). A 403 or a spent 429 has no text, so it is
    # always checked: a refusal of this client and not an outage. A 200
    # challenge page carries no payload, so without the check it would read as
    # a parser defect (R-794). A page that does carry Beatport's payload is a
    # results page whatever script Cloudflare added to it, so the challenge
    # script's mark is never read over one (U281's review).
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
        if refused is not None:
            return refused
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
# The fallbacks' refusal check, shared by the two of them
# ---------------------------------------------------------------------------


def unread_outcome(source: str, page: Fetched) -> SourceOutcome | None:
    """The outcome for a page nobody can read a result off, or None.

    BLOCKED for a page this client was refused, a 403 or a spent 429, or a 200
    whose title is a known challenge. UNREACHABLE for every other page with no
    text. None for a page that is worth parsing.

    EVERY CATALOGUE THIS MODULE SCRAPES, BEATPORT INCLUDED SINCE U281, AND THE
    GENERAL CATALOGUE. R-791 kept Beatport out because it was answering then;
    its 403 on every lookup from 2026-11-13 is the refusal this check exists
    for. The general catalogue in :mod:`cratekit.tagging.published` reads its
    refusals through this one check (R-796), which is why the name is public.
    A 5xx, a timeout or a failed name lookup stays UNREACHABLE: those are an
    outage, and the two send a person to different places.

    A CLOUDFLARE CHALLENGE IS NAMED, with :data:`CLOUDFLARE_CHALLENGE` in the
    note, when the refusal's header, one of Cloudflare's two page titles or its
    challenge script said so, so the sweep's warning can say what refused it.

    RECOGNISED AND SAID, NEVER ANSWERED. Nothing here retries a challenge, alters
    a header or solves anything. The note names what was seen so a person reading
    the artifact knows it was a refusal of this machine and not an outage.
    """
    if page.status in _BLOCK_STATUSES:
        return SourceOutcome(
            source,
            Answer.BLOCKED,
            note=f"the catalogue refused this client, {page.note or f'HTTP {page.status}'}",
        )
    if page.text is None:
        return SourceOutcome(source, Answer.UNREACHABLE, note=page.note)
    challenge = _CHALLENGE_TITLE.search(page.text)
    if challenge:
        title = challenge.group(1)
        named = f", a {CLOUDFLARE_CHALLENGE}" if _CLOUDFLARE_TITLE.match(title) else ""
        return SourceOutcome(
            source,
            Answer.BLOCKED,
            note=f"the catalogue answered with a bot check page, {title!r}{named}",
        )
    if _CHALLENGE_BODY.search(page.text):
        return SourceOutcome(
            source,
            Answer.BLOCKED,
            note=f"the catalogue answered with a {CLOUDFLARE_CHALLENGE} page",
        )
    return None


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
    refused = unread_outcome(TRAXSOURCE, page)
    if refused is not None:
        return refused

    # ``unread_outcome`` answered for every page with no text, so this is the page.
    rows = _traxsource_rows(page.text or "")
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
        if not _title_matches(title, found_title.group(1).strip(), artist=artist):
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


def _bandcamp_heading_matches(title: str, heading: str, artist: str) -> bool:
    # A listing heading is sometimes "Artist - Title" rather than the title
    # alone, and dropping the credit is the difference between a match and a
    # miss on a self released record. ONLY A HEAD THAT NAMES THE ARTIST IS
    # DROPPED, AND THEN IT IS NEVER READ: a heading "Sunrise Mood - Original
    # Mix" is a title and its version, and reading its tail as the title
    # matched a file titled "Original Mix" to another recording, while a
    # heading "Probe - Friday Night Mix" read whole is "probe" and its version,
    # which met a file named "05B - 98 - Probe - Body" (R-1631).
    head, dash, rest = heading.partition(_DASH)
    if dash and _artist_matches(artist, head):
        return _title_matches(title, rest, artist=artist)
    return _title_matches(title, heading, artist=artist)


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
    refused = unread_outcome(BANDCAMP, page)
    if refused is not None:
        return refused

    # ``unread_outcome`` answered for every page with no text, so this is the page.
    entries = _BC_RESULT.findall(page.text or "")
    headings_read = 0
    # A LISTING THAT MATCHED AND WHOSE TRACK PAGE COULD NOT BE READ is not a
    # miss either: the catalogue named the track and the refusal hid its genre.
    # Kept rather than returned while unreachable, because a later listing may
    # still answer. A BLOCK ends the walk over listings: every further track page
    # is a paced request to a catalogue that has just refused this client.
    # A track page that is GONE, 404 or 410, is a dead listing and no answer
    # about the track, so it is passed over the way the loop always did; holding
    # it as unreachable would leave the file undecidable for as long as the dead
    # link stays listed.
    track_unread: SourceOutcome | None = None
    for entry in entries:
        heading = _BC_HEADING.search(entry)
        if not heading:
            continue
        headings_read += 1
        track_url, text = heading.group(1).split("?")[0], heading.group(2).strip()
        if not _bandcamp_heading_matches(title, text, artist):
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
            unread = unread_outcome(BANDCAMP, track_page)
            if unread is None:
                text = track_page.text or ""
                genre = genre or _bandcamp_tag(_BC_TAG.findall(text), declared)
                art_url = art_url or _bandcamp_art(_BC_OG_IMAGE.search(text))
            elif not genre and unread.answer is Answer.BLOCKED:
                track_unread = unread
                break
            elif not genre and track_page.status not in _GONE_STATUSES:
                track_unread = track_unread or unread
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
    if track_unread is not None:
        return track_unread
    return SourceOutcome(BANDCAMP, Answer.MISS)


# ---------------------------------------------------------------------------
# Discogs, asked through its documented API with a person's own token (U244)
# ---------------------------------------------------------------------------
#
# WHY DISCOGS, AND WHY FIRST. Its releases carry a coarse genre and a finer
# style ("Disco", "Nu-Disco", "Deep House"), mostly tagged by DJs and
# collectors, so the dance records Beatport does not sell are covered well, and
# it is an API a person signs up to rather than a page that answers a bot
# check. It is asked first since U282, after it matched nine of ten untagged
# files in the live trial of 2026-11-13. Signed in, it allows
# about sixty requests a minute.
#
# A SEARCH, THEN THE RELEASES IT NAMES. The database search names releases and
# carries no tracklist, so the first few releases it names are read, each by
# its own number, and one is accepted only when one of its tracks, or its own
# title for a single, matches the searched title through the shared
# ``_title_matches``, which refuses a title that strips to nothing, and
# an artist matches through ``_artist_matches``. A wrong release is worse than a
# miss: its style would be written onto the file for good.
#
# THE STYLES RIDE THE HIT AND THE GENRES RIDE THE NOTE. Styles are the field a
# folder can be chosen from, so all of them ride the outcome in Discogs' order
# and :func:`_resolved` takes the first that names a folder. Genres ("Electronic",
# "Funk / Soul") are too coarse to choose by and are kept as context.
#
# THE TOKEN IS A CREDENTIAL AND GOES IN ONE PLACE. It is read from the keychain
# through ``core.secrets``, sent only in the ``Authorization`` header, and never
# put in a URL, a note, a record, a log line or a refusal. Every note the asker
# writes is scrubbed of it as well, because a transport failure's message is a
# client library's text and not this module's to bound.
#
# NO TOKEN IS NOT A MISS. With none recorded Discogs is ``not-asked``, its note
# says how to record one, and the walk names it among the unread sources, so a
# folder swept without a token is never recorded as tracks no catalogue
# carries. A token the API rejects is a run's refusal naming the remedy, never
# an outage: every later file would be refused the same way.
#
# A REFUSAL IS REMEMBERED FOR THE PROCESS, as the general catalogue's is. A 429
# that outlasted the shared backoff is BLOCKED, and the next file is answered
# BLOCKED from memory rather than waiting out the backoff again. The asker is
# one per process for that reason and for its pacer: one interval across the
# run, never one per file.

#: The API's root and the two reads this source makes.
DISCOGS_API = "https://api.discogs.com"
DISCOGS_SEARCH = f"{DISCOGS_API}/database/search"
DISCOGS_RELEASE = f"{DISCOGS_API}/releases/"

#: How many search results are asked for, and how many of the releases they
#: name are read. Each release is a paced request, so three is the cost a miss
#: may spend, about five seconds a track at the pacer's interval.
DISCOGS_RESULTS_PER_PAGE = 10
DISCOGS_RELEASES_READ = 3

#: The remaining request count at or under which the next request waits
#: :data:`DISCOGS_SLOWDOWN_S` first. Discogs counts requests over a moving
#: minute and says how many are left on every answer, so slowing down there is
#: cheaper than meeting a 429 and the thirty second ladder behind it.
DISCOGS_REMAINING_FLOOR = 5
DISCOGS_SLOWDOWN_S = 10.0

#: The header Discogs counts down in.
DISCOGS_REMAINING_HEADER = "x-discogs-ratelimit-remaining"

#: The credential, by the name ``crate login`` records it under.
DISCOGS_CREDENTIAL = secrets.Credential.DISCOGS_TOKEN

#: How a person records the token, said wherever its absence is.
DISCOGS_LOGIN_STEPS = (
    "make a personal access token in your Discogs account's developer settings, "
    "put it in a file, and record it with crate login discogs-token --from-file PATH"
)

#: The ``not-asked`` notes for a walk with no token to send. Two, because a
#: token never recorded and one recorded whose value the keychain no longer
#: holds are two facts. The tag summary counts both as "no token".
DISCOGS_NO_TOKEN = f"not asked: no Discogs token is recorded; {DISCOGS_LOGIN_STEPS}"
DISCOGS_TOKEN_LOST = (
    f"not asked: a Discogs token is recorded and the keychain no longer holds it; "
    f"{DISCOGS_LOGIN_STEPS}"
)
DISCOGS_UNASKED_NOTES: tuple[str, ...] = (DISCOGS_NO_TOKEN, DISCOGS_TOKEN_LOST)

#: The head of the ``not-asked`` note for a token Discogs refused, earlier or
#: on this file (U282's review). The walk goes on to the record shops instead
#: of stopping there, so this head is what the tag summary counts the files by
#: and warns about: a person who recorded a token is told it no longer works,
#: even when Beatport settled every file.
DISCOGS_TOKEN_REFUSED = f"{NOT_SENT}Discogs refused the recorded token: "

#: A personal token is one printable word. Anything else would make the header
#: invalid, and a client library that refuses an invalid header names its value
#: in the error, so a malformed token is refused before it is sent.
_TOKEN_SHAPE = re.compile(r"[!-~]+")

#: What stands in for the token in any text that might have carried it.
_SCRUBBED = "[token]"

#: Why a credential refusal is raised with this slug: the product's one slug for
#: a credential the run cannot use, as the catalogue app's rejection uses it.
_CREDENTIAL_REASON = "credential-missing"


def discogs_headers(token: str) -> dict[str, str]:
    """What every Discogs request says about itself, the token in its one place.

    Discogs asks every client for a User-Agent that names it, so this tool names
    itself and its version and nothing about the person running it.
    """
    return {
        "User-Agent": f"Cratekit/{__version__}",
        "Accept": "application/json",
        "Authorization": f"Discogs token={token}",
    }


@dataclass(frozen=True, slots=True)
class NotAsked:
    """A source the walk passed over with a reason, recorded ``not-asked``."""

    source: str
    note: str


@dataclass(frozen=True, slots=True)
class _Release:
    """The parts of one Discogs release this reader uses."""

    release_id: int
    title: str
    artists: str
    tracks: tuple[tuple[str, str], ...]
    styles: tuple[str, ...]
    genres: tuple[str, ...]


def _words_of(value: object) -> tuple[str, ...] | None:
    """The non empty strings of a list, or None when the field is not a list."""
    if not isinstance(value, list):
        return None
    return tuple(word.strip() for word in value if isinstance(word, str) and word.strip())


#: Discogs' numeral for a second artist of the same name, "Moodymann (2)".
_DISAMBIGUATION = re.compile(r"\s*\(\d+\)$")

#: Discogs files an article last, "Prodigy, The", which the comma split of
#: ``_artist_matches`` would read as two artists, one of them "the".
_ARTICLE_LAST = re.compile(r"^(?P<name>.+?),\s*(?P<article>the|a|an)$", re.IGNORECASE)


def _discogs_name(name: str) -> str:
    """One Discogs artist name in the form a file's tag spells it.

    The disambiguating numeral and the variation mark are Discogs' own and are
    dropped, and an article filed last is put back first, so "Prodigy, The" is
    one artist, "The Prodigy", and not a second one called "the" that every
    artist named The anything matches.
    """
    bare = _DISAMBIGUATION.sub("", name.strip().rstrip("*").strip())
    moved = _ARTICLE_LAST.match(bare)
    return f"{moved['article']} {moved['name']}" if moved else bare


def _credited(value: object) -> str:
    """The names of a Discogs artist list, joined as ``_artist_matches`` reads them."""
    if not isinstance(value, list):
        return ""
    names = (entry.get("name") for entry in value if isinstance(entry, dict))
    return ", ".join(
        _discogs_name(name) for name in names if isinstance(name, str) and name.strip()
    )


def _tracks_of(rows: object) -> list[dict[str, Any]]:
    """Every track of a tracklist, the sub tracks under an index row included."""
    if not isinstance(rows, list):
        return []
    found: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("type_", "track") == "track":
            found.append(row)
        found.extend(_tracks_of(row.get("sub_tracks")))
    return found


def _discogs_release(payload: dict[str, Any], release_id: int) -> _Release | None:
    """The release, or None when the answer is not a release this reader knows.

    A TRACKLIST IS WHAT MAKES IT ONE. Every release Discogs serves carries one,
    so an answer without a list there is a shape this reader was never written
    against. Styles and genres are optional on Discogs, and a field that is
    absent is no words; a field that is present and not a list is not.
    """
    tracklist = payload.get("tracklist")
    styles = _words_of(payload.get("styles", []))
    genres = _words_of(payload.get("genres", []))
    if not isinstance(tracklist, list) or styles is None or genres is None:
        return None
    title = payload.get("title")
    tracks = tuple(
        (str(row.get("title") or "").strip(), _credited(row.get("artists")))
        for row in _tracks_of(tracklist)
    )
    return _Release(
        release_id=release_id,
        title=title.strip() if isinstance(title, str) else "",
        artists=_credited(payload.get("artists")),
        tracks=tracks,
        styles=styles,
        genres=genres,
    )


def _release_matches(release: _Release, artist: str, title: str) -> bool:
    """Whether a release carries the searched recording.

    A TRACK of the release whose title matches, credited to a matching artist,
    the track's own credit when it names one and the release's otherwise. Or, for
    a single, the release's own title and artist, both through the shared
    :func:`_title_matches`, which refuses a title that strips to nothing rather
    than reading it as a substring of every title (R-1534).
    """
    for track_title, track_artists in release.tracks:
        credited = track_artists or release.artists
        if credited and _title_matches(title, track_title, artist=artist):
            if _artist_matches(artist, credited):
                return True
    return bool(
        release.artists
        and _title_matches(title, release.title, artist=artist)
        and _artist_matches(artist, release.artists)
    )


def _release_note(release: _Release) -> str:
    styles = ", ".join(release.styles) or "none"
    genres = ", ".join(release.genres) or "none"
    return f"release {release.release_id} lists styles {styles} and genres {genres}"


#: What a read answered when the release it asked for is gone.
_GONE = object()


@dataclass
class DiscogsAsker:
    """One process's way of asking Discogs, with what it has learned on the way.

    ``token`` is None when none is recorded, and ``unasked`` is then the note
    every file is recorded ``not-asked`` with. ``remaining`` is the last count
    Discogs said was left, and ``refused`` the first refusal it answered, after
    which nothing more is asked in this process. ``rejected`` is why the token
    was refused, after which it is never sent again in this process: every
    later file is refused the same way without a request.

    The token is left out of the ``repr``, so a debugging print of an asker, or
    of anything holding one, does not carry it.

    Built by :func:`discogs_asker`, and by :func:`for_discogs` for a worker.
    """

    token: str | None = field(repr=False)
    fetch: Fetch
    pacer: Pacer
    unasked: str = DISCOGS_NO_TOKEN
    remaining: int | None = None
    refused: SourceOutcome | None = None
    rejected: str | None = None

    def ask(self, artist: str, title: str) -> SourceOutcome | NotAsked:
        """Discogs' answer about one track, or why it was not asked."""
        if self.token is None:
            return NotAsked(DISCOGS, self.unasked)
        if self.rejected is not None:
            raise _rejected(f"{self.rejected}, earlier in this run, so Discogs was not asked")
        if not _TOKEN_SHAPE.fullmatch(self.token):
            self.rejected = "the recorded Discogs token is not one printable word"
            raise _rejected(f"{self.rejected}, so it was not sent")
        if self.refused is not None:
            return SourceOutcome(
                DISCOGS,
                Answer.BLOCKED,
                note=(
                    f"{NOT_SENT}Discogs refused this client earlier in this run and "
                    f"is not asked again in it. Then, {self.refused.note}"
                ),
            )
        said = self._search(artist, title)
        if said.answer is Answer.BLOCKED:
            self.refused = said
        return said

    def _scrub(self, text: str) -> str:
        return text.replace(self.token, _SCRUBBED) if self.token else text

    def _said(self, answer: Answer, note: str = "") -> SourceOutcome:
        return SourceOutcome(DISCOGS, answer, note=self._scrub(note))

    def _read(self, url: str, *, release: bool) -> dict[str, Any] | SourceOutcome | object:
        """One paced touch: the JSON object, the answer its absence is, or gone.

        THE COUNT DISCOGS SENT LAST DECIDES WHETHER TO WAIT FIRST, so a run
        slows down before a 429 rather than after one. A RELEASE THAT IS GONE,
        404 or 410, is a dead result and no answer about the track, and is
        passed over as Bandcamp's dead listings are; a search answering one is
        an API that moved, and is unreachable.
        """
        if self.remaining is not None and self.remaining <= DISCOGS_REMAINING_FLOOR:
            self.pacer.sleep(DISCOGS_SLOWDOWN_S)
            self.remaining = None
        self.pacer.wait()
        page = self.fetch(url)
        if page.text is not None:
            self.remaining = _remaining(page.headers)
        if page.status == 401:
            self.rejected = "Discogs answered 401 to the token this installation records"
            raise _rejected(self.rejected)
        if release and page.status in _GONE_STATUSES:
            return _GONE
        refused = unread_outcome(DISCOGS, page)
        if refused is not None:
            return self._said(refused.answer, refused.note)
        try:
            payload = json.loads(page.text or "")
        except ValueError:
            return self._said(
                Answer.UNREACHABLE,
                "the answer was not JSON, so it did not come from the Discogs API",
            )
        if not isinstance(payload, dict):
            return self._said(
                Answer.PARSE_BREAK, "the answer was JSON and not an object"
            )
        return payload

    def _search(self, artist: str, title: str) -> SourceOutcome:
        # THE MIX IS LEFT OUT OF THE QUESTION, its last bracketed group only, and
        # a title that is nothing but brackets is asked whole: an empty track
        # field asks Discogs for every release by the artist.
        bare = _last_group_stripped(title.strip()) or title.strip()
        query = urlencode(
            {
                "type": "release",
                "artist": artist.strip(),
                "track": bare,
                "per_page": DISCOGS_RESULTS_PER_PAGE,
            }
        )
        found = self._read(f"{DISCOGS_SEARCH}?{query}", release=False)
        if isinstance(found, SourceOutcome):
            return found
        assert isinstance(found, dict)
        results = found.get("results")
        if not isinstance(results, list):
            return self._said(
                Answer.PARSE_BREAK, "the search answer carries no list of results"
            )
        numbers = [
            entry["id"]
            for entry in results
            if isinstance(entry, dict)
            and type(entry.get("id")) is int
            and entry.get("type", "release") == "release"
        ]
        if results and not numbers:
            # Results are present and none names a release by number, which is
            # the only evidence that tells a reshaped answer from an empty one.
            return self._said(
                Answer.PARSE_BREAK,
                "the search answered results and none names a release by number",
            )
        held: SourceOutcome | None = None
        styleless: SourceOutcome | None = None
        for number in numbers[:DISCOGS_RELEASES_READ]:
            read = self._read(f"{DISCOGS_RELEASE}{number}", release=True)
            if read is _GONE:
                continue
            if isinstance(read, SourceOutcome):
                # A BLOCK ENDS THE WALK OVER RELEASES: every further read is a
                # paced request to an API that has just refused this client.
                # Anything else unread is held, since a later release may answer.
                if read.answer is Answer.BLOCKED:
                    return read
                held = held or read
                continue
            assert isinstance(read, dict)
            release = _discogs_release(read, number)
            if release is None:
                held = held or self._said(
                    Answer.PARSE_BREAK,
                    f"release {number} answered without a tracklist this reader knows",
                )
                continue
            if not _release_matches(release, artist, title):
                continue
            matched = SourceOutcome(
                DISCOGS,
                Answer.MATCHED,
                source_genre=release.styles[0] if release.styles else "",
                note=_release_note(release),
                words=release.styles,
            )
            if not release.styles:
                # A PRESSING WITH NO STYLE IS KEPT, NOT RETURNED. Another pressing
                # of the same recording may carry the styles, and a match that
                # can name no style would decline the file where it need not.
                styleless = styleless or matched
                continue
            return matched
        # AN UNREAD PRESSING OUTRANKS A STYLELESS MATCH (round two): what it held
        # is unknown, and the match alone would let the general catalogue write
        # its album word over a style Discogs may have had.
        if held is not None:
            return held
        if styleless is not None:
            return styleless
        # A RELEASE THAT COULD NOT BE READ IS NOT A MISS: it may have been the
        # one carrying the track.
        return held if held is not None else self._said(Answer.MISS)


def _remaining(headers: Mapping[str, str]) -> int | None:
    """The request count Discogs said is left, or None when it said none."""
    raw = headers.get(DISCOGS_REMAINING_HEADER, "").strip()
    # ASCII DIGITS ONLY: ``isdigit`` is true of a superscript two, which ``int``
    # refuses, and a header is text somebody else chose.
    return int(raw) if raw.isascii() and raw.isdigit() else None


def _rejected(why: str) -> CratekitError:
    """A token Discogs cannot use, as the run's refusal, typed as a rejection.

    BUILT FROM ``secrets.CredentialRejected``, so the remedy is the one the
    credential store declares for a credential that IS set and was refused:
    record a new one. RUN SCOPE, because every later file would be refused the
    same way. The token is never in the sentence.
    """
    typed = secrets.CredentialRejected(why, name=str(DISCOGS_CREDENTIAL))
    error = refuse(
        _CREDENTIAL_REASON,
        f"{why}. Discogs was not read and nothing was recorded as a miss",
        remedy=Remedy(str(typed.remedy)),
        steps=(DISCOGS_LOGIN_STEPS,),
        scope=Scope.RUN,
        retryable=False,
        origin=("tagging", "searchers"),
        detail={"credential": str(DISCOGS_CREDENTIAL), "source": DISCOGS},
    )
    error.__cause__ = typed
    return error


def discogs_asker(
    *,
    token: str | None,
    fetch: Fetch | None = None,
    sleep: Callable[[float], None] | None = None,
    pacing: Pacer | None = None,
    unasked: str = DISCOGS_NO_TOKEN,
) -> DiscogsAsker:
    """Build the asker. With no token it asks nothing, and needs no fetch.

    The default fetch sends :func:`discogs_headers` and nothing else, under the
    shared timeout and rate limit ladder. An explicit ``pacing`` keeps its own
    sleep, as :func:`catalogue_searcher`'s does.
    """
    naps = time.sleep if sleep is None else sleep
    pacer = Pacer(sleep=naps) if pacing is None else pacing
    if fetch is None:
        sent = discogs_headers(token) if token is not None else {}
        fetch = default_fetch(sleep=naps, headers=sent)
    return DiscogsAsker(token=token, fetch=fetch, pacer=pacer, unasked=unasked)


def _recorded_token() -> tuple[str | None, str]:
    """The token the keychain holds, or None and the note saying why not.

    THE PRESENCE INDEX FIRST, so an installation that never recorded a token
    never touches the keychain. A recorded token the keychain no longer holds is
    an absence, said as such. A keychain that cannot be read at all is a broken
    machine and is refused, never read as no token: a person who recorded one
    would otherwise watch Discogs go unasked with no word of why.
    """
    name = str(DISCOGS_CREDENTIAL)
    if not secrets.exists(name):
        return None, DISCOGS_NO_TOKEN
    try:
        return secrets.get(name), ""
    except secrets.CredentialMissing:
        return None, DISCOGS_TOKEN_LOST
    except secrets.CredentialError as exc:
        raise refuse(
            _CREDENTIAL_REASON,
            f"the Discogs token is recorded and the keychain could not be read for it "
            f"({type(exc).__name__}), so Discogs was not asked and nothing was "
            f"recorded as a miss",
            remedy=Remedy(str(exc.remedy)),
            scope=Scope.RUN,
            origin=("tagging", "searchers"),
            detail={"credential": name},
        ) from exc


#: The one asker this process asks Discogs through, built on first use.
_shared_discogs: list[DiscogsAsker] = []


def for_discogs() -> DiscogsAsker:
    """The asker a worker should use, one per process, looked up at call time.

    ONE PER PROCESS, so the pacer, the remaining count and a refusal are the
    run's and not a file's: a worker builds its searcher per file, and an asker
    per file would open every file with a fresh interval and ask an API that
    refused the file before. A test replaces this attribute, as it does
    :func:`for_taxonomy`. Building one reads the keychain and touches no network.
    """
    if not _shared_discogs:
        token, note = _recorded_token()
        _shared_discogs.append(discogs_asker(token=token, unasked=note or DISCOGS_NO_TOKEN))
    return _shared_discogs[0]


def choose_word(
    declared: Taxonomy, words: Sequence[str], *, source: str, named_only: bool
) -> tuple[str, str] | None:
    """The first of a source's words that maps to a folder, with the tag to write.

    The one chooser for a source that answers several words, shared by Discogs'
    styles and the general catalogue's album genres. "Maps to a folder" is the
    shipped resolver answering, as ``source``'s word, with a bucket or a word
    that is a bucket's own name, not declining, not a name the taxonomy calls
    too coarse to be a final tag, and not the fallback bucket. With
    ``named_only`` the tag must also name a folder by an exact declaration,
    :meth:`Taxonomy.named_folder`, the test a vocabulary row passes to load.

    IN THE SOURCE'S ORDER, because that order is the only ranking it publishes,
    and nothing here forms an opinion about music. The tag is the resolver's
    answer and nothing here adjusts it.
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


# ---------------------------------------------------------------------------
# The walk, and what it does when nobody answered
# ---------------------------------------------------------------------------

#: The record shops asked by artist and title through the shared fetch seam.
#: Discogs is not here: it is asked through its asker, which holds a token.
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
    """Every source of the walk's answer, in the walk's order, ``not-asked`` for the rest.

    EVERY SOURCE OF THE WALK, ALWAYS, so a reader of one file's record never has
    to work out from a missing entry whether a catalogue was skipped or
    forgotten. A source the walk never reached because an earlier one matched
    says so, and one it passed over says why in its note.
    """
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
    """The sources whose answer said nothing about the track.

    The ones asked that answered blocked, unreachable or unparsable, and the
    ones passed over for want of a credential, since whether those carry the
    track is just as unknown (U244). On a match too, not only on a decline, so
    a record whose answers show an unreachable Discogs before a Beatport match
    says so in ``unread`` as well, and the two fields of one record cannot
    disagree.
    """
    return tuple(
        outcome.source
        for outcome in outcomes
        if outcome.answer not in (Answer.MISS, Answer.MATCHED)
    ) + tuple(skipped.source for skipped in passed)


def _resolved(declared: Taxonomy, outcome: SourceOutcome) -> SearchHit:
    """Turn one catalogue's raw genre into the tag to write, or into a decline.

    The hit is returned either way, because a decline that cannot say what it
    declined is a decline nobody can act on.

    A TAG AND A DECLINE ARE THE TWO OUTCOMES, AND ``off_taxonomy`` QUALIFIES THE
    FIRST ONE ONLY. It rides a genre that is actually going to be written, so a
    pass through string this taxonomy calls too coarse to be a final tag is a
    plain decline and carries no flag: a file gets one disposition, never two.
    """
    if outcome.words:
        # SEVERAL WORDS, AND THE FIRST THAT NAMES A FOLDER IS THE ONE (U244).
        # None that does is a decline naming the source's first word, never the
        # resolver's pass through of it: a style written raw would put a word
        # on the file that no folder holds.
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

    The precedence is the point of the whole module. A decline needs at least
    one source that ANSWERED, and it is a genuine absence, ``no-hit``, only when
    EVERY source asked answered MISS. When some of them were blocked, unreachable
    or unparsable beside a MISS, the decline names them in ``unread`` and the
    file is not reported as one no catalogue carries (R-791). Only when nobody
    answered at all does the question become which refusal, and a parse break
    beats an unreachable there because a broken parser is actionable today and a
    network is not. A blocked source is not an answer about the track, so
    refusals of this client raise the unreachable refusal and say so.

    The decline is a :class:`SearchHit` with no genre rather than None, because
    None cannot carry the answers the item's record owes.

    A SOURCE PASSED OVER FOR WANT OF A TOKEN IS NOT AN ANSWER EITHER (U244). It
    rides ``unread`` beside a MISS, so the file is not ``no-hit``, and beside
    refusals it is named in the refusal's steps. A walk that asked nothing at
    all is a decline naming what it passed over, never an outage.
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

    ``walk`` is :data:`WALK` unless a caller names another, each a source of
    :data:`SOURCES` named once. ``discogs`` is the asker Discogs is asked
    through; with none given, Discogs is a source with no token and is recorded
    ``not-asked``, so a direct caller never reaches the keychain. A worker hands
    in :func:`for_discogs` through :func:`for_taxonomy`.

    A factory rather than a module level function because
    :data:`cratekit.tagging.tag.Searcher` is ``(artist, title) -> SearchHit |
    None`` and cannot carry a taxonomy or a seam. Both bind here, once, at
    construction.

    An explicit ``pacing`` keeps its OWN sleep. Passing both is a caller saying
    two different things about one schedule, and the more specific object is the
    one that meant it.

    ``refusals`` is the run's :class:`Refusals`, beside the pacer (U281). A
    catalogue it says to stop asking is answered from it without a wait or a
    request, on the walk and on a picture's question alike. Discogs is never
    under it: its asker remembers its own refusal, and it is asked whatever
    Beatport answered.

    A MATCH ENDS THE WALK, SAVE A DECLINE FROM A SOURCE THAT NAMES NO PICTURE
    (U282). A Discogs match whose styles name no folder is held and the walk
    goes on; its word names the file only if no later source writes a genre.
    A genre Discogs decided carries the picture's question over the record
    shops after it, :func:`_pictured`.
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

    def shop(source: str, artist: str, title: str) -> SourceOutcome:
        """One record shop's answer, or the run's word that it is not sent (U281)."""
        stopped = counted.stopped(source)
        if stopped is not None:
            return stopped
        outcome = _SEARCHES[source](artist, title, fetch=touch, pacer=pacer, declared=declared)
        counted.heard(outcome)
        return outcome

    def search(artist: str, title: str) -> SearchHit | None:
        outcomes: list[SourceOutcome] = []
        passed: list[NotAsked] = []
        declined: SearchHit | None = None
        shown: SourceOutcome | None = None
        rejected: CratekitError | None = None
        for place, source in enumerate(order):
            if source == DISCOGS:
                try:
                    said = asker.ask(artist, title)
                except CratekitError as refusal:
                    # A REJECTED TOKEN WAITS FOR THE RECORD SHOPS (U282's review).
                    # Raised at once it would stop every file before Beatport,
                    # its genres and its covers; held, it is raised only where
                    # Discogs was asked after Beatport before, when no shop
                    # matched, and the file is otherwise Beatport's as it was.
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
                outcome = shop(source, artist, title)
            outcomes.append(outcome)
            if outcome.answer is not Answer.MATCHED:
                continue
            if source in _SEARCHES:
                shown = outcome
            resolved = _resolved(declared, outcome)
            if resolved.genre is None and source not in _SEARCHES:
                # A DECLINE FROM A SOURCE THAT NAMES NO PICTURE GIVES WAY (U282).
                # None of Discogs' styles names a folder, so the walk goes on to
                # the record shops, and its word names the file only if none of
                # them writes a genre. A record shop's decline is its own word
                # for the track, carries its row's picture, and ends the walk as
                # it always has.
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
            return _pictured(hit, order[place + 1 :], artist, title, shop)
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
            raise rejected
        return _decide(order, outcomes, passed, artist, title)

    return search


def _lent(hit: SearchHit, shown: SourceOutcome | None) -> SearchHit:
    """A hit from a source that names no picture, given the one a record shop's row named.

    THE PICTURE IS THE SHOP'S WHOSE ROW MATCHED, its own ``art_source``, or
    nobody's, the empty string, when no shop's row did. Never the hit's source,
    so the report about a missing picture is never written about a catalogue
    that is not asked for one.
    """
    if shown is None:
        return replace(hit, art_url="", art_source="")
    return replace(hit, art_url=shown.art_url, art_source=shown.source)


def _pictured(
    hit: SearchHit,
    rest: Sequence[str],
    artist: str,
    title: str,
    shop: Callable[[str, str, str], SourceOutcome],
) -> SearchHit:
    """A genre decided by a source that names no picture, with the picture's question (U282).

    No record shop's row has matched by then, since a shop's match, a genre or
    a decline, ends the walk. So the shops the walk never reached are the
    picture's question, carried on the hit as
    ``ask_picture`` and asked by :func:`cratekit.tagging.tag.tag_one` only for
    a file that has no picture. Each such shop is recorded ``not-asked`` with
    a note saying why, until it is.

    THE QUESTION ASKS THE SHOPS IN THE WALK'S ORDER UNTIL ONE MATCHES, the
    same row the walk would have reached before Discogs was asked first, under
    the run's count of refusals, so a refusing Beatport is stopped after three
    whether the walk or a picture asked it. Its answer replaces the
    ``not-asked``, a refusal or an outage joins ``unread``, and a match's row
    names the picture whatever its genre: the genre is already decided.
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
            outcome = shop(source, artist, title)
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

    ``refusals`` is the run's count of refusals in a row, :func:`for_run`'s,
    handed in by a sweep's worker so a catalogue that refused the run three
    times is not asked by its later files (U281). A caller that hands none
    gets a count that lasts this one searcher.
    """
    return catalogue_searcher(declared, discogs=for_discogs(), refusals=refusals)


#: The run whose refusals this process is counting, and the count (U281). One
#: slot: a process drives one run at a time, and a run that is not this one
#: starts its own count, so nothing lingers past the run that made it.
_run_refusals: list[tuple[str, Refusals]] = []


def for_run(run: str) -> Refusals:
    """The refusal count of the run named ``run``, looked up rather than kept by a worker.

    THE RUN OWNS ITS COUNT. The job engine hands a handler the job and the item
    and no scope of the run, and a worker builds its searcher per file, so the
    count is found by the run's identity: the same name returns the same
    count, and any other name a fresh one. A sweep's worker names its run by
    the job and the drive's attempt, which only ever grows, so a new sweep and
    a resumed run each ask a refusing catalogue again from their first file,
    as U281 asks. A test replaces this attribute, as it does
    :func:`for_taxonomy`; :func:`reset_runs` forgets the count.
    """
    if not _run_refusals or _run_refusals[0][0] != run:
        _run_refusals[:] = [(run, Refusals())]
    return _run_refusals[0][1]


def reset_runs() -> None:
    """Forget the run whose refusals were being counted."""
    _run_refusals.clear()


#: The one image fetch this process asks through, built on first use (U260).
_images: list[FetchImage] = []


def for_images() -> FetchImage:
    """The image fetch a worker should use, looked up rather than constructed.

    The same shape and the same reason as :func:`for_taxonomy`: a test replaces
    this attribute on this module, and a worker that built its own fetch inline
    would leave it nowhere to hand a fake in. Building one touches no network.
    R-226's limit applies here too.

    ONE PER PROCESS, unlike the searcher's binder and like
    :func:`cratekit.tagging.published.for_lookup` (U260). The worker asks for
    its seam once per file, and an album's files all name one address, so the
    memory :func:`remembering` keeps is only worth having if the next file
    meets the same fetch. A job is driven in one process, so the memory lasts
    the run and no longer; :func:`reset_images` drops it. The default fetch is
    looked up on this module when the shared one is built, so a test that
    replaces it and resets is asking through its own.
    """
    if not _images:
        _images.append(remembering(default_image_fetch(), admit=art.decodes))
    return _images[0]


def reset_images() -> None:
    """Forget the shared image fetch and every picture it remembered."""
    _images.clear()


__all__ = [
    "BANDCAMP",
    "BANDCAMP_SEARCH",
    "BEATPORT",
    "BEATPORT_IMAGE_EDGE",
    "BEATPORT_SEARCH",
    "CLOUDFLARE_CHALLENGE",
    "DISCOGS",
    "DISCOGS_API",
    "DISCOGS_CREDENTIAL",
    "DISCOGS_LOGIN_STEPS",
    "DISCOGS_NO_TOKEN",
    "DISCOGS_RELEASE",
    "DISCOGS_RELEASES_READ",
    "DISCOGS_REMAINING_FLOOR",
    "DISCOGS_REMAINING_HEADER",
    "DISCOGS_RESULTS_PER_PAGE",
    "DISCOGS_SEARCH",
    "DISCOGS_SLOWDOWN_S",
    "DISCOGS_TOKEN_LOST",
    "DISCOGS_TOKEN_REFUSED",
    "DISCOGS_UNASKED_NOTES",
    "HEADERS",
    "IMAGE_MEMORY",
    "JITTER_FRACTION",
    "MIN_INTERVAL_S",
    "NOT_ASKED",
    "NOT_SENT",
    "PARSE_BREAK_REASON",
    "SCRAPED_WALK",
    "RATE_LIMIT_ATTEMPTS",
    "RATE_LIMIT_BASE_WAIT_S",
    "REFUSALS_BEFORE_STOP",
    "REQUEST_TIMEOUT_S",
    "SOURCES",
    "TRAXSOURCE",
    "TRAXSOURCE_SEARCH",
    "UNREACHABLE_REASON",
    "UNREAD_ANSWERS",
    "WALK",
    "Answer",
    "DiscogsAsker",
    "Fetch",
    "Fetched",
    "NotAsked",
    "Pacer",
    "Refusals",
    "SourceOutcome",
    "catalogue_searcher",
    "choose_word",
    "default_fetch",
    "default_image_fetch",
    "discogs_asker",
    "discogs_headers",
    "for_discogs",
    "for_images",
    "for_run",
    "for_taxonomy",
    "remembering",
    "reset_images",
    "reset_runs",
    "unread_outcome",
]
