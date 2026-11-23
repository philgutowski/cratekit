"""What every catalogue source shares: its answer, its pacing and its refusal check.

ONE SOURCE'S OUTCOME HAS FIVE VALUES, NOT TWO. A genre or nothing would read
an outage, a changed page and a real absence alike as "not carried", and a
folder swept during an outage would complete clean. So a source answers
MATCHED, MISS, UNREACHABLE, BLOCKED or PARSE_BREAK, and only MISS may
contribute to a decline.

A BOT CHALLENGE IS BLOCKED, AND RECOGNISING IT IS THE WHOLE REMEDY (R-791,
U281). A 403, a spent 429 or a 200 challenge page is a refusal of this client,
never an outage and never a miss, and nothing here tries to get past one.

A PARSE BREAK IS NOT AN UNREACHABLE: one sends a person to their network, the
other to this parser, so the two refusals have slugs of their own. A break is
claimed only on positive evidence, so a guess that goes wrong degrades to a
miss rather than a false defect report.

Layer: modules.
"""

from __future__ import annotations

import random
import re
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType

from cratekit.tagging import refused, titles

#: The floor between two consecutive touches of any catalogue.
MIN_INTERVAL_S = 1.0

#: Half the floor again, either way, so two runs drawing independently do not
#: stay in step for long.
JITTER_FRACTION = 0.5

BEATPORT = "beatport"
DISCOGS = "discogs"
TRAXSOURCE = "traxsource"
BANDCAMP = "bandcamp"

#: Every source a file's record can name, in the order a record lists them, so
#: a record written before U244 still summarises.
SOURCES: tuple[str, ...] = (DISCOGS, BEATPORT, TRAXSOURCE, BANDCAMP)

#: The sources asked, in order, unless a caller names another walk (U282).
WALK: tuple[str, ...] = (DISCOGS, BEATPORT)

#: The walk before U244, kept so the two scraped parsers stay driven by the
#: suite. Never the default: both shops refuse this machine with a bot check.
SCRAPED_WALK: tuple[str, ...] = (BEATPORT, TRAXSOURCE, BANDCAMP)

#: The two slugs a walk raises, declared in ``cause.REASONS``.
UNREACHABLE_REASON = "catalogue-unreachable"
PARSE_BREAK_REASON = "catalogue-parse-broken"

#: The statuses read as a refusal of this client rather than a server that
#: could not answer: Cloudflare's interstitial is a 403, and a 429 that outlasted
#: the backoff is the catalogue declining to talk to this machine for now.
_BLOCK_STATUSES = frozenset({403, 429})

#: A dead page: no answer about the track, and not an outage either.
_GONE_STATUSES = frozenset({404, 410})

#: The challenge pages measured on 2026-10-01, matched on the TITLE so a track
#: called "Just a moment" cannot read as one.
_CHALLENGE_TITLE = re.compile(
    r"<title[^>]*>\s*(just a moment(?:\.\.\.|\u2026)|client challenge|attention required!)",
    re.IGNORECASE,
)

#: The two titles above that are Cloudflare's own pages, rather than a shop's.
_CLOUDFLARE_TITLE = re.compile(r"just a moment|attention required", re.IGNORECASE)

#: Spelled once, so the tag summary counts these refusals by the note's string.
CLOUDFLARE_CHALLENGE = "Cloudflare challenge"

#: The head of the note on an answer a catalogue was never sent, because it had
#: already refused this client in the run (U281).
NOT_SENT = "not asked: "

#: Refusals in a row that stop a run asking a catalogue (U281): one can be a
#: moment's challenge, three is a catalogue refusing this client.
REFUSALS_BEFORE_STOP = 3

#: Cloudflare's challenge machinery in a page body. A bot managed site may put
#: it on an ordinary page too, so Beatport reads it only over a page with no
#: payload (U281).
_CHALLENGE_BODY = re.compile(r"/cdn-cgi/challenge-platform/|window\._cf_chl_opt")

#: What the per source record says about a catalogue the walk never reached.
NOT_ASKED = "not-asked"


class Answer(Enum):
    """What one catalogue did when it was asked. Only MISS means it does not
    carry the track."""

    MATCHED = "matched"
    MISS = "miss"
    UNREACHABLE = "unreachable"
    BLOCKED = "blocked"
    PARSE_BREAK = "parse-break"


#: The answers that leave the question open, spelled once.
UNREAD_ANSWERS: tuple[str, ...] = (
    Answer.BLOCKED.value,
    Answer.UNREACHABLE.value,
    Answer.PARSE_BREAK.value,
)


@dataclass(frozen=True, slots=True)
class SourceOutcome:
    """One catalogue's answer, with the source that gave it and what it said.

    ``art_url`` is the picture on the row that supplied ``source_genre``.
    ``words`` is every word a source answers when it answers several, Discogs'
    styles (U244); the tag is then chosen among them, never by
    ``source_genre`` alone.
    """

    source: str
    answer: Answer
    source_genre: str = ""
    note: str = ""
    art_url: str = ""
    words: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Fetched:
    """One HTTP touch: the page text, or None and the reason there is none.

    ``status`` is the last HTTP status, or None when nothing answered, so a
    caller tells a 403 block from a server that fell over.
    """

    text: str | None = None
    note: str = ""
    status: int | None = None
    #: The answer's headers, names lowercased, on a 200 only (U244).
    headers: Mapping[str, str] = field(
        default_factory=lambda: MappingProxyType({}), compare=False
    )


#: The one seam every network touch goes through.
Fetch = Callable[[str], Fetched]


@dataclass
class Pacer:
    """The wait before every touch of a catalogue, jittered and injectable, so
    the suite asserts the schedule instead of enduring it."""

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

    Handed to a searcher like the pacer, because a worker builds its searcher
    per file. Any answer that is not a refusal ends the run of them. A stopped
    catalogue is answered BLOCKED, never MISS, quoting its last refusal, so the
    file stays unread and askable.
    """

    limit: int = REFUSALS_BEFORE_STOP
    running: dict[str, int] = field(default_factory=dict)
    last: dict[str, SourceOutcome] = field(default_factory=dict)
    #: Whether this run's answers move the record of when each catalogue began
    #: refusing (U284); only a sweep's run count does.
    record: bool = False

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
        if not self.record:
            return
        # An outage or a parse break says nothing about whether it would refuse.
        if outcome.answer is Answer.BLOCKED:
            refused.refused(outcome.source)
        elif outcome.answer in (Answer.MATCHED, Answer.MISS):
            refused.answered(outcome.source)


#: The matcher is :mod:`cratekit.tagging.titles` (U280), read here by its old
#: names.
_normalized = titles.normalized
_identifies = titles.identifies
_words = titles.words
_DASH = titles.DASH


def _artist_parts(value: str, separators: str) -> list[str]:
    parts = [_normalized(part) for part in re.split(separators, value)]
    # Initials and conjunctions match everything by substring.
    return [part for part in parts if len(part) > 2]


def _artist_matches(searched: str, found: str) -> bool:
    """Whether at least one credited name is shared, since a release and a file
    each credit names the other drops."""
    searched_parts = _artist_parts(searched, r"[,&]")
    found_parts = _artist_parts(found, r"[,&/]")
    return any(
        left == right or left in right or right in left
        for left in searched_parts
        for right in found_parts
    )


def _title_matches(searched: str, found: str, *, artist: str) -> bool:
    """Whether the file's title names the same recording as a catalogue's title.

    The file read into its parts (:func:`titles.read_file`), the row by its own
    structure (:func:`titles.read_row`), matched by :func:`titles.matches`:
    whole words, and a side with no letter or digit matches nothing.
    """
    return titles.matches(titles.read_file(searched, artist), titles.read_row(found))


def unread_outcome(source: str, page: Fetched) -> SourceOutcome | None:
    """The outcome for a page nobody can read a result off, or None to parse it.

    BLOCKED for a refusal of this client, a 403, a spent 429 or a known
    challenge page, naming a Cloudflare challenge when one said so.
    UNREACHABLE for any other page with no text: an outage sends a person
    elsewhere. Public because the general catalogue reads its refusals here
    too (R-796).
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
