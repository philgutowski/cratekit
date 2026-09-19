"""Second source candidates for a track the configured provider does not carry (U80).

A bootleg, a white label, an unreleased promo: a set holds tracks no streaming
catalogue sells, and before this module every one of them ended the set short
with no route inside the product. The source system searched SoundCloud and
then YouTube with ``yt-dlp``, ranked what came back, and wrote a review file a
person judged before anything downloaded (``DJ_setid/fetch_others.py``). This
module is that search half, and it keeps the source system's order.

A SEARCH IS A PROPOSAL, NEVER A PICK, as it is for the provider's own search
(:mod:`cratekit.intake.candidates`). A second source is an upload somebody
titled by hand, a DJ mix that happens to carry the track name, a re-upload at a
lower bitrate. Nothing here is ever listed or downloaded without a person, so
every ranked hit is an OPTION on one review item and the score only orders the
screen. That is also why there is no floor: a bootleg's upload title is noisy
by nature, and a hit dropped for a low score is a hit nobody can choose.

THE NETWORK IS A PARAMETER. :class:`FallbackSearcher` is the seam, and the one
implementation that touches the network, :class:`YtDlpSearcher`, runs a
subprocess through an injectable runner. The suite drives it with a fake runner
and never executes ``yt-dlp``.

AN ANSWER THAT COULD NOT BE READ IS NOT AN EMPTY ONE. A nonzero exit, a timeout
and a program that could not be started all raise :class:`FallbackUnavailable`,
so "the search failed" can never read as "nothing was found". That is why the
subprocess is run WITHOUT ``--ignore-errors``, which the source system passed:
it turns a failed search into an empty answer at exit zero.

Layer: modules. Nothing here writes a file or downloads anything.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Protocol

from cratekit.acquire import match
from cratekit.core import binaries, review

#: The queue. Declared by U11 for exactly this question and unused until now.
QUEUE = review.Queue.FALLBACK_SOURCE

#: The one kind on it: which upload, if any, is the wanted recording.
KIND = "fallback-candidate"

#: The platforms searched, in order. SoundCloud first, then YouTube, as the
#: source system did: a bootleg or an edit is most often a SoundCloud upload,
#: and the order is also the tie break between two equal scores.
SOUNDCLOUD = "soundcloud"
YOUTUBE = "youtube"
PLATFORMS: tuple[str, ...] = (SOUNDCLOUD, YOUTUBE)

#: Hits asked of each platform, the source system's ``SEARCH_N``.
SEARCH_LIMIT = 4

#: The binary the shipped searcher runs.
BINARY = "yt-dlp"

#: A "track" longer than this is almost always a DJ mix or a set that matched
#: on stuffed keywords, so its score is scaled by :data:`MIX_FACTOR`. Both are
#: the source system's values, carried over unmeasured here.
LIKELY_MIX_SECONDS = 900
MIX_FACTOR = 0.4

#: What became of one row, one word a script can switch on.
OFFERED = "offered"
WAITING = "waiting"
ACCEPTED = "accepted"
REJECTED = "rejected"
STALLED = "stalled"
NO_CANDIDATES = "no-candidates"


class FallbackUnavailable(Exception):
    """A second source could not answer a search. Never read as "nothing found"."""


@dataclass(frozen=True, slots=True)
class Hit:
    """One upload a second source returned for a query."""

    platform: str
    url: str
    title: str
    uploader: str
    duration: int | None = None


@dataclass(frozen=True, slots=True)
class Answer:
    """Every platform's hits for one row, and how many lines could not be read."""

    hits: tuple[Hit, ...]
    unreadable: int = 0


class FallbackSearcher(Protocol):
    """The seam. One search of one platform, or :class:`FallbackUnavailable`."""

    def search(self, platform: str, query: str, limit: int) -> Answer: ...


#: The fields ``yt-dlp`` prints per hit, one JSON object a line.
_FIELDS = "%(.{title,uploader,channel,webpage_url,url,duration})j"

#: The ``yt-dlp`` search prefix for each platform.
_PREFIX: Mapping[str, str] = {SOUNDCLOUD: "scsearch", YOUTUBE: "ytsearch"}

#: Seconds one search may take. The source system's value.
TIMEOUT_SECONDS = 180


def _hit(platform: str, line: str) -> Hit | None:
    """One printed line as a hit, or ``None`` when it names no usable page.

    A SoundCloud search in flat mode can yield an ``api.soundcloud.com`` URL
    the extractor cannot resolve again, so only the web page URL is kept for
    those, the source system's rule.
    """
    said = json.loads(line)
    if not isinstance(said, dict):
        raise ValueError("not an object")
    url = said.get("webpage_url") or said.get("url") or ""
    if "api.soundcloud.com" in str(url):
        url = said.get("webpage_url") or ""
    if not isinstance(url, str) or not url:
        return None
    duration = said.get("duration")
    return Hit(
        platform=platform,
        url=url,
        title=str(said.get("title") or ""),
        uploader=str(said.get("uploader") or said.get("channel") or ""),
        duration=(
            int(duration)
            if isinstance(duration, (int, float))
            and not isinstance(duration, bool)
            and math.isfinite(duration)
            and duration > 0
            else None
        ),
    )


class YtDlpSearcher:
    """The shipped searcher: ``yt-dlp`` in flat playlist mode, nothing downloaded.

    ``run`` is ``subprocess.run`` in production and a fake in every test.
    """

    def __init__(
        self,
        binary: str,
        *,
        run: Callable[..., Any] = subprocess.run,
        timeout: float = TIMEOUT_SECONDS,
    ) -> None:
        self.binary = binary
        self._run = run
        self._timeout = timeout

    def argv(self, platform: str, query: str, limit: int) -> list[str]:
        # ONE ARGUMENT, NEVER A SHELL. The query is a person's text and the
        # search prefix in front of it keeps it from ever reading as an option.
        return [
            self.binary,
            "--flat-playlist",
            "--no-warnings",
            "--print",
            _FIELDS,
            f"{_PREFIX[platform]}{limit}:{query}",
        ]

    def search(self, platform: str, query: str, limit: int) -> Answer:
        argv = self.argv(platform, query, limit)
        try:
            done = self._run(
                argv,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                env=binaries.subprocess_env(),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise FallbackUnavailable(
                f"the {platform} search did not answer within {self._timeout:g} seconds"
            ) from exc
        except OSError as exc:
            raise FallbackUnavailable(f"{BINARY} could not be started ({exc})") from exc
        if done.returncode != 0:
            said = (done.stderr or "").strip().splitlines()
            raise FallbackUnavailable(
                f"the {platform} search failed with exit status {done.returncode}"
                + (f" ({said[-1]})" if said else "")
            )
        hits: list[Hit] = []
        unreadable = 0
        for line in (done.stdout or "").splitlines():
            if not line.strip():
                continue
            try:
                one = _hit(platform, line)
            except ValueError:
                unreadable += 1
                continue
            if one is None:
                unreadable += 1
            else:
                hits.append(one)
        return Answer(hits=tuple(hits), unreadable=unreadable)


def yt_dlp_searcher() -> YtDlpSearcher:
    """The shipped searcher, or :class:`binaries.BinaryNotFound` naming the fix."""
    return YtDlpSearcher(binaries.resolve(BINARY))


def query(wanted: match.Wanted) -> str:
    """The text searched: the artist and the title as the row carries it."""
    return f"{wanted.artist} {wanted.listed}".strip()


def search_all(searcher: FallbackSearcher, wanted: match.Wanted) -> Answer:
    """Every platform, in order, for one row. One failure fails the row whole.

    A row whose SoundCloud answer arrived and whose YouTube search failed is not
    offered on half an answer, because the half that failed may hold the one
    upload that is the track.
    """
    hits: list[Hit] = []
    unreadable = 0
    for platform in PLATFORMS:
        answer = searcher.search(platform, query(wanted), SEARCH_LIMIT)
        hits.extend(answer.hits)
        unreadable += answer.unreadable
    return Answer(hits=tuple(hits), unreadable=unreadable)


@dataclass(frozen=True, slots=True)
class Candidate:
    """One hit, scored against the row."""

    hit: Hit
    score: float


def score(wanted: match.Wanted, hit: Hit) -> float:
    """0 to 100: how much the upload's uploader and title read like the row.

    The source system's measure over ``match``'s own fold: half the sequence
    similarity of the two strings, half the share of the row's words the upload
    carries. An upload longer than :data:`LIKELY_MIX_SECONDS` is scaled down,
    because a mix that names the track in its title is not the track.
    """
    want = match.fold(f"{wanted.artist} {wanted.listed}")
    have = match.fold(f"{hit.uploader} {hit.title}")
    if not want or not have:
        return 0.0
    ratio = SequenceMatcher(None, want, have).ratio()
    want_words = set(want.split())
    coverage = len(want_words & set(have.split())) / len(want_words)
    said = 50.0 * ratio + 50.0 * coverage
    if hit.duration is not None and hit.duration > LIKELY_MIX_SECONDS:
        said *= MIX_FACTOR
    return round(said, 1)


def ranked(wanted: match.Wanted, answer: Answer) -> tuple[Candidate, ...]:
    """Best score first, then platform order, then the platform's own order.

    ONE CANDIDATE PER URL. The same upload returned twice is one option, and
    the ordering is total so a repeat run offers the same screen.
    """
    order = {platform: n for n, platform in enumerate(PLATFORMS)}
    scored = sorted(
        (
            (-score(wanted, hit), order.get(hit.platform, len(order)), position, hit)
            for position, hit in enumerate(answer.hits)
        ),
        key=lambda entry: entry[:3],
    )
    seen: set[str] = set()
    kept: list[Candidate] = []
    for negative, _platform, _position, hit in scored:
        if hit.url in seen:
            continue
        seen.add(hit.url)
        kept.append(Candidate(hit=hit, score=-negative))
    return tuple(kept)


@dataclass(frozen=True, slots=True)
class Proposal:
    """What one row came to: its state, the sentence, and the chosen URL if any."""

    wanted: match.Wanted
    state: str
    reason: str
    item_id: str | None = None
    offered: int = 0
    url: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {
            "artist": self.wanted.artist,
            "title": self.wanted.listed,
            "state": self.state,
            "reason": self.reason,
            "item_id": self.item_id,
            "candidates": self.offered,
            "url": self.url,
        }


def identity(wanted: match.Wanted) -> dict[str, str]:
    """The folded row, the same three fields the provider's question is keyed on.

    Keyed on the row and not on the list, so one track in two lists is one
    question. A different queue and kind keep it a different item from the
    provider's question about the same row.
    """
    return {
        "artist": match.fold(wanted.artist),
        "title": match.fold(wanted.title),
        "version": wanted.version_key,
    }


def item_id(wanted: match.Wanted) -> str:
    return review.item_id_for(QUEUE, KIND, identity(wanted))


def _summary(one: Candidate) -> str:
    hit = one.hit
    length = f", {hit.duration // 60}:{hit.duration % 60:02d}" if hit.duration else ""
    return f"{hit.uploader} - {hit.title} ({hit.platform}{length}, score {one.score:g})"


def settled(items: review.ReviewStore, wanted: match.Wanted) -> Proposal | None:
    """What the queue already says about this row, or ``None`` when nobody was asked.

    READ BEFORE ANY SEARCH, so a row already in front of a person or already
    answered spends no search. An acceptance names its upload or it stalls,
    the provider question's rule.
    """
    held = review.find(items, item_id(wanted))
    if held is None:
        return None
    count = len(held.options)
    if held.verdict is None:
        return Proposal(
            wanted,
            WAITING,
            f"offered for review with {count} second source candidate(s) and not yet answered",
            item_id=held.item_id,
            offered=count,
        )
    if held.verdict is review.Verdict.REJECTED:
        return Proposal(
            wanted,
            REJECTED,
            "every second source candidate was rejected in review, so it is not "
            "searched for again until that answer is cleared",
            item_id=held.item_id,
            offered=count,
        )
    chosen = held.option
    if chosen is None and count == 1:
        chosen = held.options[0].option_id
    option = next((one for one in held.options if one.option_id == chosen), None)
    if option is None:
        return Proposal(
            wanted,
            STALLED,
            f"accepted in review without naming which of its {count} candidates",
            item_id=held.item_id,
            offered=count,
        )
    return Proposal(
        wanted,
        ACCEPTED,
        f"accepted in review as {option.summary}",
        item_id=held.item_id,
        offered=count,
        url=option.option_id,
    )


def propose(
    items: review.ReviewStore,
    wanted: match.Wanted,
    answer: Answer,
    *,
    handler_key: str,
) -> Proposal:
    """Offer every ranked candidate on one item, or say there are none. Never pick."""
    on_screen = ranked(wanted, answer)
    if not on_screen:
        return Proposal(
            wanted,
            NO_CANDIDATES,
            "SoundCloud and YouTube returned nothing for it"
            + (
                f"; {answer.unreadable} line(s) of their answers could not be read"
                if answer.unreadable
                else ""
            ),
        )
    held = review.offer(
        items,
        queue=QUEUE,
        kind=KIND,
        identity=identity(wanted),
        payload={
            "wanted": {
                "artist": wanted.artist,
                "title": wanted.listed,
                "version": wanted.version,
            },
            "query": query(wanted),
            "unreadable": answer.unreadable,
            "candidates": [
                {
                    "url": one.hit.url,
                    "platform": one.hit.platform,
                    "uploader": one.hit.uploader,
                    "title": one.hit.title,
                    "duration": one.hit.duration,
                    "score": one.score,
                }
                for one in on_screen
            ],
        },
        options=[
            review.Option(
                option_id=one.hit.url,
                summary=_summary(one),
                detail={
                    "platform": one.hit.platform,
                    "uploader": one.hit.uploader,
                    "title": one.hit.title,
                    "duration": one.hit.duration,
                    "score": one.score,
                },
            )
            for one in on_screen
        ],
        handler_key=handler_key,
    )
    return Proposal(
        wanted,
        OFFERED,
        f"{len(on_screen)} second source candidate(s) offered for review; none is "
        f"picked from a score",
        item_id=held.item_id,
        offered=len(on_screen),
    )


__all__ = [
    "ACCEPTED",
    "BINARY",
    "KIND",
    "LIKELY_MIX_SECONDS",
    "MIX_FACTOR",
    "NO_CANDIDATES",
    "OFFERED",
    "PLATFORMS",
    "QUEUE",
    "REJECTED",
    "SEARCH_LIMIT",
    "SOUNDCLOUD",
    "STALLED",
    "TIMEOUT_SECONDS",
    "WAITING",
    "YOUTUBE",
    "Answer",
    "Candidate",
    "FallbackSearcher",
    "FallbackUnavailable",
    "Hit",
    "Proposal",
    "YtDlpSearcher",
    "identity",
    "item_id",
    "propose",
    "query",
    "ranked",
    "score",
    "search_all",
    "settled",
    "yt_dlp_searcher",
]
