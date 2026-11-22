"""Second source candidates for a track the configured provider does not carry (U80).

A search of SoundCloud then YouTube with ``yt-dlp`` is a proposal, never a pick: every
ranked hit is an option on one review item and the score only orders the screen. A
search that could not be read raises :class:`FallbackUnavailable`, never an empty
answer. The download half (U81) is a second seam; both take an injectable runner.

Layer: modules. Nothing here writes a file except the fetcher's download.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Protocol

from cratekit.acquire import match
from cratekit.core import binaries, review

#: The queue, declared by U11 for this question.
QUEUE = review.Queue.FALLBACK_SOURCE

#: The one kind on it: which upload, if any, is the wanted recording.
KIND = "fallback-candidate"

#: The platforms searched, in order, which is also the tie break between equal scores.
SOUNDCLOUD = "soundcloud"
YOUTUBE = "youtube"
PLATFORMS: tuple[str, ...] = (SOUNDCLOUD, YOUTUBE)

#: Hits asked of each platform, the source system's ``SEARCH_N``.
SEARCH_LIMIT = 4

#: The binary the shipped searcher runs.
BINARY = "yt-dlp"

#: A "track" longer than this is almost always a mix, so its score is scaled by
#: :data:`MIX_FACTOR`. Both are the source system's values, unmeasured here.
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

#: Seconds one search may take.
TIMEOUT_SECONDS = 180


def _hit(platform: str, line: str) -> Hit | None:
    """One printed line as a hit, or ``None`` when it names no usable page."""
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
    """The shipped searcher: ``yt-dlp`` in flat playlist mode, nothing downloaded."""

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
        # One argument, never a shell; the search prefix keeps the query from reading
        # as an option.
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


# The download half (U81)

#: What an accepted upload is saved as: a second source is lossy anyway, and one
#: container keeps every fetched file on the ID3 path the later stages read.
FETCH_SUFFIX = ".mp3"

#: Seconds one download may take, so a stalled download cannot hold the claim forever.
FETCH_TIMEOUT_SECONDS = 900


class FallbackFetcher(Protocol):
    """The download seam. One upload into one empty directory, or :class:`FallbackUnavailable`."""

    def fetch(self, url: str, directory: Path) -> Path: ...


#: The stem a download is saved under, fixed because ``yt-dlp`` reads its output name
#: as a template and a percent sign in a title would read as a field.
FETCH_STEM = "fetched"


class YtDlpFetcher:
    """The shipped fetcher: ``yt-dlp`` extracting the audio as MP3 into one directory."""

    def __init__(
        self,
        binary: str,
        *,
        run: Callable[..., Any] = subprocess.run,
        timeout: float = FETCH_TIMEOUT_SECONDS,
    ) -> None:
        self.binary = binary
        self._run = run
        self._timeout = timeout

    def argv(self, url: str, directory: Path) -> list[str]:
        # The upload's metadata is dropped on conversion only, so the worker strips
        # tags itself (R17). The option terminator keeps the address from reading as an option,
        # and ``--no-playlist`` keeps a set page from fetching the set.
        return [
            self.binary,
            "--no-playlist",
            "--no-warnings",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
            "--postprocessor-args",
            "ExtractAudio:-map_metadata -1",
            "--output",
            str(directory / f"{FETCH_STEM}.%(ext)s"),
            "--",
            url,
        ]

    def fetch(self, url: str, directory: Path) -> Path:
        argv = self.argv(url, directory)
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
                f"the download did not finish within {self._timeout:g} seconds"
            ) from exc
        except OSError as exc:
            raise FallbackUnavailable(f"{BINARY} could not be started ({exc})") from exc
        if done.returncode != 0:
            said = (done.stderr or "").strip().splitlines()
            raise FallbackUnavailable(
                f"the download failed with exit status {done.returncode}"
                + (f" ({said[-1]})" if said else "")
            )
        return landed_in(directory)


def landed_in(directory: Path) -> Path:
    """The one MP3 a download left in its directory, or :class:`FallbackUnavailable`.

    An exit of zero is not a file: none or two MP3s would make the track a guess.
    The directory is cleared before every attempt, so anything in it is this one's.
    """
    found = (
        sorted(
            one for one in directory.iterdir()
            if one.is_file() and one.suffix.lower() == FETCH_SUFFIX
        )
        if directory.is_dir()
        else []
    )
    if len(found) != 1:
        there = sorted(one.name for one in directory.iterdir()) if directory.is_dir() else []
        raise FallbackUnavailable(
            f"the download reported success and left {len(found)} {FETCH_SUFFIX} file(s)"
            + (f" (the folder holds: {', '.join(there)})" if there else "")
        )
    return found[0]


def yt_dlp_fetcher() -> YtDlpFetcher:
    """The shipped fetcher, or :class:`binaries.BinaryNotFound` naming the fix."""
    return YtDlpFetcher(binaries.resolve(BINARY))


def query(wanted: match.Wanted) -> str:
    """The text searched: the artist and the title as the row carries it."""
    return f"{wanted.artist} {wanted.listed}".strip()


def search_all(searcher: FallbackSearcher, wanted: match.Wanted) -> Answer:
    """Every platform, in order, for one row; one failure fails the row whole,
    since the failed half may hold the track.
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

    Half sequence similarity, half the share of the row's words the upload carries,
    scaled down past :data:`LIKELY_MIX_SECONDS` because a mix naming the track is not it.
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
    """Best score first, then platform order, then the platform's own; one per URL."""
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
    """The folded row, keyed like the provider's question, so one track in two lists
    is one question; the queue and kind keep it apart from the provider's item.
    """
    return wanted.folded_row()


def item_id(wanted: match.Wanted) -> str:
    return review.item_id_for(QUEUE, KIND, identity(wanted))


def _summary(one: Candidate) -> str:
    hit = one.hit
    length = f", {hit.duration // 60}:{hit.duration % 60:02d}" if hit.duration else ""
    return f"{hit.uploader} - {hit.title} ({hit.platform}{length}, score {one.score:g})"


def settled(items: review.ReviewStore, wanted: match.Wanted) -> Proposal | None:
    """What the queue already says about this row, or ``None`` when nobody was asked."""
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
    "ACCEPTED", "BINARY", "FETCH_STEM", "FETCH_SUFFIX", "FETCH_TIMEOUT_SECONDS", "KIND",
    "LIKELY_MIX_SECONDS", "MIX_FACTOR", "NO_CANDIDATES", "OFFERED", "PLATFORMS", "QUEUE",
    "REJECTED", "SEARCH_LIMIT", "SOUNDCLOUD", "STALLED", "TIMEOUT_SECONDS", "WAITING", "YOUTUBE",
    "Answer", "Candidate", "FallbackFetcher", "FallbackSearcher", "FallbackUnavailable", "Hit",
    "Proposal", "YtDlpFetcher", "YtDlpSearcher", "identity", "item_id", "landed_in", "propose",
    "query", "ranked", "score", "search_all", "settled", "yt_dlp_fetcher", "yt_dlp_searcher",
]
