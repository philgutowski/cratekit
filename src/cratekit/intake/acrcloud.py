"""The recognition identifier: ACRCloud, behind the seam ``recognize.identify`` declares.

``recognize.identify`` has carried an injection point since U37 and nothing
behind it, so ``crate intake identify`` refused on every real call and both
queued intake verbs reconciled forever (R-132, R-203). This module is the
implementation the injection point exists for.

**SPENDING IS THE DESIGN CONSTRAINT.** Every chunk sent is a paid call, so the
shape of this module is the shape of a bounded spend:

* the credentials are read through :mod:`cratekit.core.secrets` at CALL time,
  after the presence gate in :mod:`cratekit.intake.recognize` has passed, and
  never from a literal or an environment variable this module reads itself;
* the number of calls a recording needs is KNOWN BEFORE THE FIRST ONE, because
  the sampling grid is a function of the duration alone, and that estimate is
  checked against a per run cap and against the month's ledger before any
  audio is carved and before the grid itself is built;
* every attempt is recorded in the ledger the moment it is made, whether or
  not an answer came back, so a crash mid set does not forget the calls it
  already spent;
* a run whose calls stop getting answers stops after a few of them, so an
  offline machine or a host that rejects every post costs a handful of
  attempts and not a whole set of them;
* a spend refusal, whether it is this module's own bound or the service
  answering that the account's quota is spent, is a DIFFERENT cause from a
  chunk the service did not recognise. The source system once read a 565 call
  batch of quota refusals as content misses, and that is the defect the
  distinction exists to make impossible here.

**EVERYTHING THAT TOUCHES THE OUTSIDE IS INJECTED.** The carver (ffmpeg and
ffprobe) and the transport (one HTTP post per chunk) are parameters with
shipped defaults, so the suite drives the whole mapping through fakes and the
battery passes with no credential recorded and no binary installed. The live
key binding and the first paid call are R-132's attended half.

**THE HOST AND THE MONTHLY BOUND ARE THE USER'S, read from the frozen
configuration (R-301).** ACRCloud's identify endpoint is regional and an
account belongs to one region, so the host is ``recognition.host``; the month
is bounded by ``recognition.monthly_calls``, which has a default, so a machine
nobody configured is still bounded. Neither has a default HERE: ``identify``
takes both as required arguments and ``bound_identifier`` builds them from the
section it is handed, so no caller reaches the paid path with a host or a
month nobody chose.

**THE RESPONSE MAPPING IS THE SOURCE SYSTEM'S, corrected once, and unverified
against a live account.** The status families below are the ones
``DJ_setid/acr.py`` classified, with 3015 moved from the quota family to the
miss family and 3100 added as transient on the strength of the vendor's
published table as remembered at review; neither correction has met a real
answer. The first attended run is where the table is checked.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import math
import subprocess
import tempfile
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Protocol

from cratekit.acquire import match
from cratekit.acquire.match import Wanted
from cratekit.core import binaries, config, secrets
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake.recognize import Identified

# ---------------------------------------------------------------------------
# The grid, the bound, the endpoint
# ---------------------------------------------------------------------------

#: The identify endpoint's path. The regional host is ``recognition.host``.
ENDPOINT = "/v1/identify"

#: One chunk is twelve seconds of 16 kHz mono PCM, which is under the service's
#: one megabyte sample limit and gives it more to fingerprint than the 8 kHz
#: alternative. Chunks are taken every twenty five seconds: at roughly three
#: per minute the grid catches a short edit without paying for overlap.
CHUNK_S = 12
INTERVAL_S = 25
SAMPLE_RATE = 16000

#: The most calls one RUN may cost. A two hour set on the grid above is 288
#: calls, so one run admits any set a person would play. A recording that
#: needs more is not trimmed: a recording identified for its first three hours
#: and silently not for its fourth is a report over audio nothing looked at.
#: Since R-706 it is identified in PARTS instead, see :data:`MAX_PARTS`.
MAX_CALLS_PER_RUN = 400

#: The most even parts one recording is identified in, each a run under the
#: bound above. A live recording longer than one run is an ordinary input for
#: this author, the eleventh sitting met a five hour mix, and Phillip decided
#: on 2026-09-24 that such a set is split into even parts named Part A, Part B
#: and Part C at most. Three parts is over eight hours of audio, and a file
#: needing more is refused before the first call as not one set, which is the
#: refusal the per run bound was written for.
MAX_PARTS = 3

#: How many attempts in a row may get no answer before the run stops. An
#: answer this build cannot read, an HTTP status that is not 200, a transport
#: that raised, or a transient code from the service all count; a match or a
#: miss resets the count. Five is a network blip; more is a machine that is
#: offline or a host that rejects every post, and paying a whole set into
#: that is the 565 call batch wearing a different hat.
UNREACHED_STOP = 5

#: What the service's status codes mean, as families. A NON ZERO CODE IS NOT A
#: MISS: only 1001 and the two no-fingerprint codes are. The quota code and
#: the four credential codes end the run, because every later call would
#: meet the same answer, and the rest of the 2000s, 3000 and 3100 are per
#: chunk and transient.
_MATCH_CODE = 0
_MISS_CODES = frozenset({1001, 2004, 3015})
_QUOTA_CODES = frozenset({3003})
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
_TRANSIENT_CODES = frozenset({3000, 3100})

#: The service's own protocol constants, sent with every request.
_DATA_TYPE = "audio"
_SIGNATURE_VERSION = "1"
_TIMEOUT_S = 30


class Outcome(StrEnum):
    """What one chunk's answer was, as a family rather than a code."""

    MATCH = "match"
    MISS = "miss"
    QUOTA = "quota"
    AUTH = "auth"
    TRANSIENT = "transient"
    UNCLASSIFIED = "unclassified"


#: The two families that are an ANSWER about the audio, and so the only two the
#: recognition cache keeps or serves.
_KEPT_OUTCOMES = frozenset({Outcome.MATCH, Outcome.MISS})


# ---------------------------------------------------------------------------
# The two seams
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Request:
    """One signed identify call, ready to send. Carries the access key the
    service requires in the clear and nothing else secret: the signing key is
    consumed by :func:`sign` and appears in no field."""

    url: str
    fields: Mapping[str, str]
    sample: bytes
    filename: str


@dataclass(frozen=True, slots=True)
class Response:
    """What came back: the HTTP status and the raw body."""

    status: int
    body: bytes


Transport = Callable[[Request], Response]


class Carver(Protocol):
    """The audio half: how long the recording is, and one chunk of it as PCM."""

    def duration(self, source: Path) -> float:
        """Seconds of audio in ``source``. Raises when the file cannot be read."""

    def carve(self, source: Path, offset_s: int, chunk_s: int) -> bytes:
        """``chunk_s`` seconds from ``offset_s`` as a 16 kHz mono WAV."""


_SESSION: Any = None


def http_transport(request: Request) -> Response:
    """The shipped transport, one multipart post over ONE session per process.

    A session rather than a bare post, because a set is hundreds of posts to
    one host and a fresh TLS handshake per chunk is a minute of setup on a two
    hour recording. Imported lazily because a process listing jobs has no
    business loading an HTTP client.
    """
    global _SESSION
    if _SESSION is None:
        import requests  # noqa: PLC0415 - see the docstring

        _SESSION = requests.Session()
    answer = _SESSION.post(
        request.url,
        files={"sample": (request.filename, request.sample, "audio/wav")},
        data=dict(request.fields),
        timeout=_TIMEOUT_S,
    )
    return Response(status=int(answer.status_code), body=bytes(answer.content))


class FfmpegCarver:
    """The shipped carver. Resolves both binaries through :mod:`core.binaries`
    at call time, so an override or a fallback directory is honoured, and runs
    them with the credential stripped environment that module builds.

    ONE PROCESS PER CHUNK, with the seek before the input so it is a fast
    seek. That is a few hundred spawns on a long set and it is recorded as
    accepted rather than optimised here: the attended first run is where the
    real cost is measured, and a single decode sliced in memory is the
    obvious next shape if it matters.
    """

    def duration(self, source: Path) -> float:
        result = subprocess.run(
            [
                binaries.resolve("ffprobe"),
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(source),
            ],
            capture_output=True,
            text=True,
            env=binaries.subprocess_env(),
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"ffprobe could not read {source.name}: {result.stderr.strip() or 'no output'}"
            )
        try:
            return float(result.stdout.strip())
        except ValueError as exc:
            raise RuntimeError(
                f"ffprobe reported no duration for {source.name}: {result.stdout.strip()!r}"
            ) from exc

    def carve(self, source: Path, offset_s: int, chunk_s: int) -> bytes:
        with tempfile.TemporaryDirectory(prefix="cratekit-recognize-") as scratch:
            target = Path(scratch) / "chunk.wav"
            result = subprocess.run(
                [
                    binaries.resolve("ffmpeg"),
                    "-ss",
                    str(offset_s),
                    "-t",
                    str(chunk_s),
                    "-i",
                    str(source),
                    "-ar",
                    str(SAMPLE_RATE),
                    "-ac",
                    "1",
                    "-y",
                    "-loglevel",
                    "error",
                    str(target),
                ],
                capture_output=True,
                text=True,
                env=binaries.subprocess_env(),
                check=False,
            )
            if result.returncode != 0 or not target.is_file():
                raise RuntimeError(
                    f"ffmpeg could not carve {source.name} at {offset_s}s: "
                    f"{result.stderr.strip() or 'no output'}"
                )
            return target.read_bytes()


# ---------------------------------------------------------------------------
# Signing and the request
# ---------------------------------------------------------------------------


def sign(*, access_key: str, timestamp: str, signing_key: str) -> str:
    """The service's request signature: HMAC-SHA1 over the line-joined tuple,
    base64 encoded. The tuple's order is the protocol's, not a choice."""
    to_sign = "\n".join(
        ["POST", ENDPOINT, access_key, _DATA_TYPE, _SIGNATURE_VERSION, timestamp]
    )
    digest = hmac.new(signing_key.encode(), to_sign.encode(), hashlib.sha1).digest()
    return base64.b64encode(digest).decode()


def request_for(
    sample: bytes,
    *,
    access_key: str,
    signing_key: str,
    host: str,
    timestamp: str | None = None,
) -> Request:
    """One identify call for ``sample``. The signing key is consumed here and
    appears in no field of the result."""
    stamp = timestamp if timestamp is not None else str(int(time.time()))
    return Request(
        url=f"https://{host}{ENDPOINT}",
        fields={
            "access_key": access_key,
            "sample_bytes": str(len(sample)),
            "timestamp": stamp,
            "signature": sign(access_key=access_key, timestamp=stamp, signing_key=signing_key),
            "data_type": _DATA_TYPE,
            "signature_version": _SIGNATURE_VERSION,
        },
        sample=sample,
        filename="chunk.wav",
    )


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------


def planned_calls(duration_s: float, *, chunk_s: int = CHUNK_S, interval_s: int = INTERVAL_S) -> int:
    """How many chunks a recording this long costs, WITHOUT building the grid.

    Arithmetic rather than ``len(sample_offsets(...))`` on purpose: the budget
    is checked against this number before the grid exists, so a probe that
    reports a nonsense duration (a broken header answering two billion
    seconds) is refused by the per run cap rather than allocating two billion
    offsets on the way to it. A duration that is not a finite number is zero
    chunks, and the caller refuses that as a recording it cannot measure.
    """
    if not math.isfinite(duration_s):
        return 0
    whole = int(duration_s)
    if whole <= 0:
        return 0
    if whole < chunk_s:
        return 1
    return (whole - chunk_s) // interval_s + 1


def sample_offsets(
    duration_s: float, *, chunk_s: int = CHUNK_S, interval_s: int = INTERVAL_S
) -> tuple[int, ...]:
    """Where the chunks are taken from, as seconds, for a recording this long.

    A recording shorter than one chunk still gets its opening chunk, so a
    zero result over a short file is a real answer rather than a grid that
    was empty. Nothing is taken past the point where a whole chunk no longer
    fits, so the last chunk is never padded with silence.
    """
    count = planned_calls(duration_s, chunk_s=chunk_s, interval_s=interval_s)
    return tuple(offset * interval_s for offset in range(count))


def parts_needed(planned: int, *, per_run: int = MAX_CALLS_PER_RUN) -> int:
    """How many runs a grid of ``planned`` chunks takes, without building it.

    Arithmetic for the same reason :func:`planned_calls` is: the ceiling on
    parts is checked against this number before any grid exists.
    """
    if planned <= 0:
        return 0
    return -(-planned // per_run)


def partition(
    offsets: tuple[int, ...], *, per_run: int = MAX_CALLS_PER_RUN
) -> tuple[tuple[int, ...], ...]:
    """The grid as the fewest EVEN, contiguous parts each at or under ``per_run``.

    A grid that fits one run is one part, itself. A longer one is cut into
    :func:`parts_needed` slices whose sizes differ by at most one, in grid
    order, so the parts of a five hour mix are two halves and not a full run
    and a remainder. Even parts are what the eleventh sitting cut by hand, and
    they are what keeps every part a set's worth of audio rather than one of
    them a sliver. An empty grid is no parts at all.
    """
    count = parts_needed(len(offsets), per_run=per_run)
    if count == 0:
        return ()
    base, extra = divmod(len(offsets), count)
    parts: list[tuple[int, ...]] = []
    start = 0
    for index in range(count):
        size = base + (1 if index < extra else 0)
        parts.append(tuple(offsets[start : start + size]))
        start += size
    return tuple(parts)


# ---------------------------------------------------------------------------
# The ledger and the budget
# ---------------------------------------------------------------------------

#: The two declared state entries the ledger lives in. Installation scoped,
#: because the counter is bound to the credential's quota and not to a library.
LEDGER_KEY = "identify_usage"
LEDGER_LOCK_KEY = "identify_usage_lock"


def current_month(now: datetime | None = None) -> str:
    """The ledger's month key, local time, because a quota resets on the
    person's calendar and not on UTC's."""
    return (now or datetime.now()).strftime("%Y-%m")


class Ledger:
    """The monthly call counter, on core's lock and core's atomic writer.

    ADVISORY BY NATURE. The service's answer carries no remaining quota field,
    so the count here is what THIS machine spent and can drift from the
    account when another tool shares the key. The live quota code is the real
    ceiling; this ledger is what stops a run that would obviously exceed
    ``recognition.monthly_calls`` from making the first call.

    A ledger that cannot be READ counts as zero rather than refusing, because a
    corrupt counter must not lock recognition out; a ledger that cannot be
    LOCKED or WRITTEN raises, because a call that was made and not counted is
    exactly the drift the counter exists to prevent. The lock is
    ``config._exclusive_lock``, which refuses rather than proceeding unlocked,
    and the write is ``config.atomic_write_bytes``, which fsyncs before the
    rename; both are the properties the outbound ledger already stands on.

    ONE LOCK, ONE PARSE AND ONE WRITE PER CALL, and that is accepted rather than
    batched: the cost is a millisecond against a network round trip, and
    batching would reopen the crash window between the post and the count.
    """

    def __init__(self, path: Path | None = None, lock_path: Path | None = None) -> None:
        self.path = path if path is not None else config.state_path(LEDGER_KEY)
        self.lock_path = (
            lock_path if lock_path is not None else config.state_path(LEDGER_LOCK_KEY)
        )

    def _read(self) -> dict[str, int]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        if not isinstance(data, dict):
            return {}
        counts: dict[str, int] = {}
        for key, value in data.items():
            try:
                counts[str(key)] = int(value)
            except (TypeError, ValueError):
                continue
        return counts

    def used(self, month: str | None = None) -> int:
        return self._read().get(month or current_month(), 0)

    def record(self, calls: int, month: str | None = None) -> int:
        """Add ``calls`` to the month and return the new total."""
        if calls <= 0:
            return self.used(month)
        key = month or current_month()
        config._mkdir_private(self.lock_path.parent)
        config._mkdir_private(self.path.parent)
        with config._exclusive_lock(self.lock_path):
            counts = self._read()
            counts[key] = counts.get(key, 0) + calls
            payload = json.dumps(counts, indent=2, sort_keys=True) + "\n"
            config.atomic_write_bytes(payload.encode("utf-8"), self.path)
            return counts[key]


@dataclass(frozen=True, slots=True)
class Budget:
    """What a run may spend. ``monthly`` of None means the month is not bounded
    by this tool and the ledger still counts; only a caller that builds a
    budget by hand can say that, because the shipped path builds it with
    :meth:`from_config` and the section always carries a bound."""

    per_run: int = MAX_CALLS_PER_RUN
    monthly: int | None = None

    @classmethod
    def from_config(cls, recognition: config.RecognitionConfig) -> Budget:
        """The shipped budget: the per run cap, and the month the user set."""
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=recognition.monthly_calls)


#: The configuration key a monthly refusal names, so a person on a larger plan
#: is told the one line to change.
MONTHLY_KEY = "recognition.monthly_calls"


def assert_one_set(budget: Budget, *, planned: int) -> None:
    """Refuse a recording that would take more than :data:`MAX_PARTS` runs.

    THE REFUSAL THE PER RUN BOUND WAS WRITTEN FOR, kept at the ceiling rather
    than at one run: a file that is not a set at all is refused before the
    first call, and a long set is not. Same cause and same ``per-run`` kind as
    before R-706, so a reader of the detail tells this build's own bound from
    the service's quota answer as they always could; ``parts`` and ``ceiling``
    say how far the bound now stretches.
    """
    ceiling = budget.per_run * MAX_PARTS
    if planned > ceiling:
        raise refuse(
            "intake-recognition-spend-bound",
            f"this recording would take {planned} recognition calls, which is more "
            f"than {MAX_PARTS} parts of the per run bound of {budget.per_run}; "
            f"nothing was sent. A file this long is not one set, so split it "
            f"rather than raising the bound",
            origin=("intake.acrcloud",),
            detail={
                "planned": planned,
                "bound": budget.per_run,
                "parts": MAX_PARTS,
                "ceiling": ceiling,
                "kind": "per-run",
            },
        )


def assert_run_within(budget: Budget, *, planned: int) -> None:
    """Refuse a RUN that would exceed the per run bound.

    Asked of every part before the first call of any. By construction a part
    is at or under the bound, so this is the guard that makes that a property
    of the spend rather than of the partition that happened to be built.
    """
    if planned > budget.per_run:
        raise refuse(
            "intake-recognition-spend-bound",
            f"this run would take {planned} recognition calls and the per run "
            f"bound is {budget.per_run}; nothing was sent for it",
            origin=("intake.acrcloud",),
            detail={"planned": planned, "bound": budget.per_run, "kind": "per-run"},
        )


def assert_month_within(budget: Budget, *, planned: int, used_this_month: int) -> None:
    """Refuse BEFORE the first call when the month cannot afford the plan."""
    if budget.monthly is not None and used_this_month + planned > budget.monthly:
        raise refuse(
            "intake-recognition-spend-bound",
            f"this recording would take {planned} recognition calls, "
            f"{used_this_month} were already spent this month, and the monthly "
            f"bound is {budget.monthly}; nothing was sent. Wait for next month, "
            f"or raise {MONTHLY_KEY} in the configuration if the plan allows more",
            remedy=Remedy.RETRY_LATER,
            origin=("intake.acrcloud",),
            detail={
                "planned": planned,
                "used": used_this_month,
                "bound": budget.monthly,
                "kind": "monthly",
                "key": MONTHLY_KEY,
            },
        )


# ---------------------------------------------------------------------------
# The response mapping
# ---------------------------------------------------------------------------


def classify(payload: Mapping[str, Any]) -> tuple[Outcome, int, str]:
    """The family one answer belongs to, with the code and message it carried."""
    status = payload.get("status") or {}
    if not isinstance(status, Mapping):
        return Outcome.UNCLASSIFIED, -1, "status is not an object"
    code = status.get("code")
    message = str(status.get("msg") or "")
    if not isinstance(code, int) or isinstance(code, bool):
        return Outcome.UNCLASSIFIED, -1, message or "status carries no code"
    if code == _MATCH_CODE:
        return Outcome.MATCH, code, message
    if code in _MISS_CODES:
        return Outcome.MISS, code, message
    if code in _QUOTA_CODES:
        return Outcome.QUOTA, code, message
    if code in _AUTH_CODES:
        return Outcome.AUTH, code, message
    if 2000 <= code < 3000 or code in _TRANSIENT_CODES:
        return Outcome.TRANSIENT, code, message
    return Outcome.UNCLASSIFIED, code, message


@dataclass(frozen=True, slots=True)
class Match:
    """One recognised chunk: where it was taken and what the service said."""

    offset_s: int
    wanted: Wanted
    score: int


def parse_match(payload: Mapping[str, Any], *, offset_s: int) -> Match | None:
    """The top hit of a MATCH answer as a ``Wanted`` row, or None.

    READ BY THE LIST READERS' OWN ROW READER. The hit is a mapping with a
    title, a list of artists and an ISRC under ``external_ids``, which is the
    shape a provider row has, and ``match.read_row`` is what turns one of
    those into a ``Wanted``. Reading it here through a second reader would
    mean a recognised track and the same track pasted in a tracklist could
    stop folding to one identity the day the readers learn a new artist
    shape. None for a hit naming no artist or no title, which the reader
    refuses for the reason it refuses any such row: the half that is left is
    not unique to the recording it means. The caller counts it as a miss.

    ``origin`` is ``text`` because a recognised track names a recording and
    not a provider row: it carries no identifier acquisition could ask for,
    and freezing it as a provider row would queue an item nothing can fetch.
    """
    metadata = payload.get("metadata") or {}
    music = metadata.get("music") if isinstance(metadata, Mapping) else None
    if not isinstance(music, list) or not music:
        return None
    top = music[0]
    if not isinstance(top, Mapping):
        return None
    try:
        wanted = match.read_row(top, origin=match.TEXT, position=offset_s)
    except match.UnreadableList:
        return None
    try:
        score = int(top.get("score", 0))
    except (TypeError, ValueError):
        score = 0
    return Match(offset_s=offset_s, wanted=wanted, score=score)


def fold(matches: list[Match] | tuple[Match, ...]) -> tuple[Match, ...]:
    """One row per track played, in the order they were first heard.

    A track that plays for three minutes answers seven chunks in a row, and
    seven rows for one record is a tracklist nobody would write. Adjacent
    answers naming the same recording, by ISRC when both carry one and by
    the recording token otherwise, fold to one, keeping the FIRST offset and
    the best score. Only ADJACENT answers fold: a record played twice in a
    set was played twice, and a DJ who does that meant to.
    """
    folded: list[Match] = []
    for found in matches:
        if folded and _same_recording(folded[-1], found):
            last = folded[-1]
            if found.score > last.score:
                folded[-1] = Match(offset_s=last.offset_s, wanted=found.wanted, score=found.score)
            continue
        folded.append(found)
    return tuple(folded)


def _same_recording(one: Match, other: Match) -> bool:
    if one.wanted.isrc and other.wanted.isrc:
        return one.wanted.isrc == other.wanted.isrc
    return (
        one.wanted.recording == other.wanted.recording
        and one.wanted.version_key == other.wanted.version_key
    )


# ---------------------------------------------------------------------------
# The recognition cache
# ---------------------------------------------------------------------------

#: The declared state entry the cache lives in. A directory, one document per
#: recording and chunk plan. Installation scoped, beside the ledger, because an
#: answer is a fact about the audio and was paid for on the credential's quota.
CACHE_KEY = "identify_cache"

#: The cache document's own version. A document carrying any other is a miss.
CACHE_VERSION = 1

#: How much of the recording is read at a time while it is digested.
_DIGEST_BLOCK = 1 << 20


def content_digest(source: Path) -> str:
    """The sha256 of the recording's BYTES, streamed.

    THE BYTES AND NOTHING ELSE. A path, a size and a modification time are each
    an identity that is not unique to the thing it identifies: a second set
    exported over the first keeps the path, a re-encode can keep the size, and
    a copy keeps neither while holding the same audio. The whole file is
    read, which is seconds for a compressed set and longer for a lossless one
    on a slow volume, and it is paid on every pass because it is the only
    thing that can say the audio has not changed. That is time, and what a
    stale answer would cost is money and a false tracklist.
    """
    hashed = hashlib.sha256()
    with source.open("rb") as handle:
        while block := handle.read(_DIGEST_BLOCK):
            hashed.update(block)
    return hashed.hexdigest()


@dataclass(frozen=True, slots=True)
class ChunkPlan:
    """Everything that decides what one chunk's answer is an answer ABOUT.

    The recording's content digest says which audio. The offsets, the chunk
    length and the sample rate say which slices of it were sent and how they
    were carved. The host says which regional bucket was asked. Change any one
    and an answer kept under the old plan is an answer to a different
    question, so every one of them is in the key and a cache document carries
    the whole plan so it can be checked again on the way back in.
    """

    digest: str
    offsets: tuple[int, ...]
    host: str
    chunk_s: int = CHUNK_S
    interval_s: int = INTERVAL_S
    sample_rate: int = SAMPLE_RATE

    def material(self) -> dict[str, Any]:
        return {
            "digest": self.digest,
            "offsets": list(self.offsets),
            "chunk_s": self.chunk_s,
            "interval_s": self.interval_s,
            "sample_rate": self.sample_rate,
            "host": self.host,
        }

    def key(self) -> str:
        canonical = json.dumps(self.material(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class RecognitionCache:
    """What the service already answered about a recording, kept per chunk.

    AT THE TRANSPORT BOUNDARY. What is kept is the service's RAW answer for one
    offset, not a parsed row, so a later build that reads an answer better
    reads the kept one better too, and the fold runs over kept and fresh
    answers alike.

    ONLY AN ANSWER IS KEPT. A match and a miss are answers. A transient code,
    a transport that raised, a quota refusal and a credential refusal are not:
    each says nothing about the audio, and keeping one would turn a network
    blip into a permanent hole in every later tracklist. The same rule is
    applied again on the way back in, so a document written by anything else
    cannot serve one either.

    A DOCUMENT THAT CANNOT BE READ, OR THAT DISAGREES WITH THE PLAN IT WAS
    ASKED FOR, IS A MISS. The cost of a miss is money and never a false
    tracklist, which is the right way round for a cache to fail. A document
    that cannot be WRITTEN raises to the caller, who reports it rather than
    failing a pass whose answers are already paid for.

    THE WRITE IS A LOCKED MERGE, NOT A REPLACE. Two passes over one recording
    can overlap, ``intake identify`` and ``intake set`` started together or a
    gap filling pass beside a slow one, and each read the document when it
    began. A writer that replaced the document with what IT knew would drop
    the answers the other paid for, so the document is read again under a
    sibling lock and what this pass paid for is laid over it.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root if root is not None else config.state_path(CACHE_KEY)

    def path_for(self, plan: ChunkPlan) -> Path:
        return self.root / f"{plan.key()}.json"

    def read(self, plan: ChunkPlan) -> dict[int, Mapping[str, Any]]:
        """The kept answers for ``plan``, by offset. Empty when there are none."""
        try:
            document = json.loads(self.path_for(plan).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        if not isinstance(document, dict):
            return {}
        if document.get("version") != CACHE_VERSION or document.get("plan") != plan.material():
            return {}
        kept = document.get("answers")
        if not isinstance(kept, dict):
            return {}
        planned = set(plan.offsets)
        answers: dict[int, Mapping[str, Any]] = {}
        for said, payload in kept.items():
            try:
                offset = int(said)
            except (TypeError, ValueError):
                continue
            if offset not in planned or not isinstance(payload, dict):
                continue
            if classify(payload)[0] not in _KEPT_OUTCOMES:
                continue
            answers[offset] = payload
        return answers

    def write(self, plan: ChunkPlan, answers: Mapping[int, Mapping[str, Any]]) -> None:
        """Lay ``answers`` over what is already kept for ``plan``, under its lock."""
        path = self.path_for(plan)
        with config._exclusive_lock(path.with_suffix(".lock")):
            merged = {**self.read(plan), **answers}
            document = {
                "version": CACHE_VERSION,
                "plan": plan.material(),
                "answers": {
                    str(offset): dict(merged[offset])
                    for offset in sorted(merged)
                    if classify(merged[offset])[0] in _KEPT_OUTCOMES
                },
            }
            payload = json.dumps(document, indent=2, sort_keys=True) + "\n"
            config.atomic_write_bytes(payload.encode("utf-8"), path)


# ---------------------------------------------------------------------------
# Identification
# ---------------------------------------------------------------------------

Credentials = Callable[[], tuple[str, str]]


def keychain_credentials() -> tuple[str, str]:
    """The access key and the signing key, retrieved NOW.

    The presence gate has already passed, so a failure here is the keychain
    refusing to hand over what it said it held, and the exception already
    says what kind: no entry after all, a backend that cannot be reached, or
    an index that cannot be read. The remedy each of those carries is the one
    the person is given, because telling somebody to record a credential into
    a store that cannot hold one is the wrong instruction the secrets module
    names three types to avoid.
    """
    try:
        return (
            secrets.get(str(secrets.Credential.IDENTIFY_KEY)),
            secrets.get(str(secrets.Credential.IDENTIFY_SIGNING_KEY)),
        )
    except secrets.CredentialError as exc:
        missing = isinstance(exc, secrets.CredentialMissing)
        raise refuse(
            "credential-missing" if missing else "intake-recognition-unready",
            f"the recognition credentials could not be read: {exc}",
            remedy=Remedy(str(exc.remedy)),
            origin=("intake.acrcloud",),
            detail={"credential": getattr(exc, "name", None), "kind": type(exc).__name__},
        ) from exc


def _answer(transport: Transport, request: Request) -> tuple[Outcome, int, str, Mapping[str, Any] | None]:
    """One call's answer as a family. Everything that is not a readable 200
    is TRANSIENT with a synthetic code, so the loop has one dispatch."""
    try:
        response = transport(request)
    except Exception as exc:  # noqa: BLE001 - the transport's failures are open ended
        return Outcome.TRANSIENT, -1, f"{type(exc).__name__}: {exc}", None
    if response.status != 200:
        return Outcome.TRANSIENT, -1, f"HTTP {response.status}", None
    try:
        payload = json.loads(response.body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return Outcome.TRANSIENT, -1, "the answer was not JSON", None
    if not isinstance(payload, Mapping):
        return Outcome.TRANSIENT, -1, "the answer was not an object", None
    outcome, code, message = classify(payload)
    return outcome, code, message, payload


def _quota_refusal(code: int, message: str, *, calls: int) -> CratekitError:
    return refuse(
        "intake-recognition-spend-bound",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
        f"after {calls} call(s) this run; the account's quota is used up and every "
        f"further call would meet the same answer",
        remedy=Remedy.RETRY_LATER,
        origin=("intake.acrcloud",),
        detail={"code": code, "kind": "provider-quota", "calls": calls},
    )


def _auth_refusal(code: int, message: str) -> CratekitError:
    return refuse(
        "auth-failed",
        f"the recognition service rejected the recorded credentials: code {code} "
        f"({message or 'no message'}); the key or the signing key is wrong for this "
        f"account, and no further call was made",
        remedy=Remedy.SET_CREDENTIAL,
        origin=("intake.acrcloud",),
        detail={"code": code},
    )


def _failed(message: str, **detail: Any) -> CratekitError:
    return refuse(
        "intake-recognition-failed",
        message,
        remedy=Remedy.RETRY_LATER,
        retryable=True,
        origin=("intake.acrcloud",),
        detail=detail,
    )


def identify(
    source: Path,
    *,
    transport: Transport,
    carver: Carver,
    budget: Budget,
    host: str,
    credentials: Credentials = keychain_credentials,
    ledger: Ledger | None = None,
    cache: RecognitionCache | None = None,
    refresh: bool = False,
    month: str | None = None,
) -> Identified:
    """Identify the tracks in ``source``. Bounded before the first call.

    The order is the spend order. The duration is read and the call count
    computed BEFORE the credentials are retrieved, so a file that is not a
    set never prompts the keychain. The budget is checked against the count
    BEFORE the grid is built and before the first chunk is carved. Each
    attempt is recorded in the ledger before its answer is read, so a crash
    between the two leaves the call counted.

    Three answers end the run and two do not. A quota or a credential answer
    ends it, because every later call would meet the same one; an answer this
    build cannot classify ends it, because a run that keeps paying into an
    answer it does not understand is the 565 call batch. A transient answer,
    or a transport that raised, skips the CHUNK and the run goes on, until
    ``UNREACHED_STOP`` of them arrive in a row, and the count of chunks that
    never got an answer is returned rather than folded into the misses,
    because coverage that is incomplete is not a result and the caller has
    to be able to say so.

    A CHUNK ALREADY ANSWERED IS NOT PAID FOR AGAIN. The recording is digested
    and the kept answers for its chunk plan are read before anything is
    carved. A kept chunk skips the carve, the ledger and the transport, and a
    recording whose every chunk is kept never RETRIEVES a credential, so the
    second of ``intake identify`` then ``intake set`` spends nothing. The
    presence gate in :mod:`cratekit.intake.recognize` still runs first, so a
    machine with no key recorded is refused there whatever is kept. The parts
    ceiling, :func:`assert_one_set`, still reads the WHOLE grid, because it is
    what refuses a file that is not a set; the run bound and the monthly bound
    read only what is owed, because they are bounds on spend.

    A MISS IS KEPT UNTIL SOMEBODY ASKS AGAIN. The service's catalogue grows,
    so a chunk it could not name last season may be one it can name now, and
    nothing here can know that without paying. ``refresh`` is how a person
    says so: nothing kept is read, every chunk is paid for, and what comes
    back is laid over the document.

    WHAT WAS PAID FOR IS KEPT ON THE WAY OUT, WHICHEVER WAY THAT IS. A quota
    refusal on the hundred and twentieth chunk raises, and the hundred and
    nineteen answers before it are written first, so the pass after the quota
    resets pays for the rest and not for the set. What this does not cover is
    a process that dies outright between the first answer and the write.

    ``budget`` AND ``host`` HAVE NO DEFAULT (R-301). A default is how the
    shipped path came to bound no month and ask one region: nothing passed
    them, so nothing was chosen. :func:`bound_identifier` builds both from the
    configuration's recognition section.

    A SET LONGER THAN ONE RUN IS IDENTIFIED IN PARTS, NOT REFUSED (R-706). The
    grid is cut by :func:`partition` into even contiguous slices each at or
    under the per run bound, and every slice is a run: the run bound is asked
    of every part before the first call of any, so an oversize part is
    refused with nothing spent. The month's bound is asked ONCE, over everything
    the whole set owes, before the first call of the first part, so a set the
    month cannot afford spends nothing rather than its first part. One pass
    walks the parts in grid order and folds the answers once, so a record
    playing across the cut is one row and not two, and the caller receives
    one result for one set. The parts are never files: the carver reads any
    offset of the recording, so the cut is a place in the grid, and nothing
    is written to disk to make it. ``parts`` on the result says how many.
    """
    spend = budget
    counter = ledger or Ledger()
    kept_in = cache or RecognitionCache()
    try:
        duration_s = float(carver.duration(source))
    except (RuntimeError, OSError, ValueError, binaries.BinaryNotFound) as exc:
        raise _failed(
            f"{source.name} could not be measured, so no chunk was carved and nothing "
            f"was sent: {exc}",
            source=str(source),
        ) from exc
    planned = planned_calls(duration_s)
    if planned == 0:
        raise _failed(
            f"{source.name} holds no audio to identify (duration {duration_s!r}), so "
            f"nothing was sent",
            source=str(source),
        )
    assert_one_set(spend, planned=planned)
    offsets = sample_offsets(duration_s)
    parts = partition(offsets, per_run=spend.per_run)
    plan, unkept = _plan_for(source, offsets, host=host)
    kept = kept_in.read(plan) if plan is not None and not refresh else {}
    owed = [offset for offset in offsets if offset not in kept]
    paid: dict[int, Mapping[str, Any]] = {}
    try:
        result = _identified(
            source,
            parts=parts,
            kept=kept,
            owed=owed,
            paid=paid,
            transport=transport,
            carver=carver,
            credentials=credentials,
            spend=spend,
            counter=counter,
            host=host,
            month=month,
        )
    finally:
        # ``paid`` is filled as the answers arrive, so this keeps what a pass
        # that RAISED had already paid for. A failed write must not replace
        # the refusal on its way out, and on the way out of a pass that
        # returned it is reported instead.
        if paid and plan is not None:
            try:
                kept_in.write(plan, paid)
            except (config.ConfigLockUnavailable, OSError) as exc:
                unkept = f"{type(exc).__name__}: {exc}"
    return replace(
        result,
        cache_unwritten=unkept if paid else "",
        digest=plan.digest if plan is not None else "",
    )


def _identified(
    source: Path,
    *,
    parts: tuple[tuple[int, ...], ...],
    kept: Mapping[int, Mapping[str, Any]],
    owed: list[int],
    paid: dict[int, Mapping[str, Any]],
    transport: Transport,
    carver: Carver,
    credentials: Credentials,
    spend: Budget,
    counter: Ledger,
    host: str,
    month: str | None,
) -> Identified:
    """The pass itself. ``paid`` is the caller's, filled as each answer arrives,
    so the caller can keep it whether this returns or raises.

    ``parts`` is the grid, cut. Every part is asked of the run bound and the
    month is asked once over ``owed``, the whole set's, BEFORE any part
    starts, so a partition that handed back an oversize part, first or last,
    is refused with nothing spent rather than after the parts before it.
    """
    still_owed = frozenset(owed)
    for part in parts:
        assert_run_within(spend, planned=sum(1 for offset in part if offset in still_owed))
    keys = ("", "")
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()

    found: list[Match] = []
    calls = misses = unreached = streak = 0
    offsets = tuple(offset for part in parts for offset in part)
    for part in parts:
        for offset in part:
            calls, misses, unreached, streak = _one_chunk(
                source,
                offset,
                kept=kept,
                paid=paid,
                found=found,
                transport=transport,
                carver=carver,
                keys=keys,
                counter=counter,
                host=host,
                month=month,
                counts=(calls, misses, unreached, streak),
            )
    if unreached and unreached == len(offsets):
        raise _failed(
            f"none of the {calls} call(s) for {source.name} got an answer, so nothing "
            f"is known about it; the calls were counted",
            source=str(source),
            calls=calls,
        )
    matches = fold(found)
    return Identified(
        rows=tuple(one.wanted for one in matches),
        calls=calls,
        chunks=len(offsets),
        misses=misses,
        unreached=unreached,
        cached=len(offsets) - len(owed),
        parts=len(parts),
    )


def _one_chunk(
    source: Path,
    offset: int,
    *,
    kept: Mapping[int, Mapping[str, Any]],
    paid: dict[int, Mapping[str, Any]],
    found: list[Match],
    transport: Transport,
    carver: Carver,
    keys: tuple[str, str],
    counter: Ledger,
    host: str,
    month: str | None,
    counts: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """One chunk of the pass: served from what is kept, or carved, counted and
    sent. Returns the running ``(calls, misses, unreached, streak)``, and
    raises the three answers that end the run."""
    calls, misses, unreached, streak = counts
    access_key, signing_key = keys
    if offset in kept:
        parsed = _heard(kept[offset], offset_s=offset)
        if parsed is None:
            misses += 1
        else:
            found.append(parsed)
        return calls, misses, unreached, streak
    try:
        sample = carver.carve(source, offset, CHUNK_S)
    except (RuntimeError, OSError, binaries.BinaryNotFound) as exc:
        raise _failed(
            f"{source.name} could not be carved at {offset}s after {calls} call(s): {exc}",
            source=str(source),
            offset_s=offset,
            calls=calls,
        ) from exc
    request = request_for(sample, access_key=access_key, signing_key=signing_key, host=host)
    calls += 1
    try:
        counter.record(1, month)
    except (config.ConfigLockUnavailable, OSError) as exc:
        raise _failed(
            f"the recognition ledger could not record a call ({exc}), so the "
            f"call was not made; {calls - 1} call(s) were made before it",
            calls=calls - 1,
        ) from exc
    outcome, code, message, payload = _answer(transport, request)
    if outcome in _KEPT_OUTCOMES:
        streak = 0
        paid[offset] = payload or {}
        parsed = _heard(payload or {}, offset_s=offset)
        if parsed is None:
            misses += 1
        else:
            found.append(parsed)
    elif outcome is Outcome.QUOTA:
        raise _quota_refusal(code, message, calls=calls)
    elif outcome is Outcome.AUTH:
        raise _auth_refusal(code, message)
    elif outcome is Outcome.TRANSIENT:
        unreached += 1
        streak += 1
        if streak >= UNREACHED_STOP:
            raise _failed(
                f"{streak} calls in a row for {source.name} got no usable answer, the "
                f"last one {message}, so the run stopped after {calls} call(s) rather "
                f"than paying the rest of the set into a service it cannot reach; "
                f"the calls were counted",
                source=str(source),
                calls=calls,
                unreached=unreached,
            )
    else:
        raise _failed(
            f"the recognition service answered {source.name} at {offset}s with code "
            f"{code} ({message or 'no message'}), which this build cannot classify, "
            f"so the run stopped after {calls} call(s) rather than paying into an "
            f"answer it does not understand",
            code=code,
            offset_s=offset,
            calls=calls,
        )
    return calls, misses, unreached, streak


def _plan_for(
    source: Path, offsets: tuple[int, ...], *, host: str
) -> tuple[ChunkPlan | None, str]:
    """The chunk plan for ``source``, or None and why the cache is out of reach.

    A recording whose bytes cannot be read for a digest is identified WITHOUT
    the cache rather than refused: the carver is what decides whether the
    audio can be sent, and a digest that failed says nothing about that. What
    it costs is said, because the next pass will pay again.
    """
    try:
        digest = content_digest(source)
    except OSError as exc:
        return None, f"the recording could not be read for its digest ({type(exc).__name__})"
    return ChunkPlan(digest=digest, offsets=tuple(offsets), host=host), ""


def _heard(payload: Mapping[str, Any], *, offset_s: int) -> Match | None:
    """The match one KEPT family answer names, or None for a miss.

    One reading for a fresh answer and a kept one, so a chunk means the same
    thing on the pass that paid for it and on the pass that did not.
    """
    if classify(payload)[0] is not Outcome.MATCH:
        return None
    return parse_match(payload, offset_s=offset_s)


def bound_identifier(
    recognition: config.RecognitionConfig,
    *,
    transport: Transport | None = None,
    carver: Carver | None = None,
    ledger: Ledger | None = None,
    cache: RecognitionCache | None = None,
    refresh: bool = False,
) -> Callable[[Path], Identified]:
    """The identifier in the seam's own shape, over the shipped seams.

    RESOLVED AT CALL TIME, not at import: the transport and the carver are
    looked up when the returned callable runs, so nothing here touches a
    binary or a network until a recording is actually handed over, and a
    suite that replaces either on the module reaches the paid path.

    ``recognition`` is the configuration's section, the one a queued job
    freezes, and it is the ONLY source of the host and the monthly bound.
    """
    budget = Budget.from_config(recognition)

    def run(source: Path) -> Identified:
        return identify(
            source,
            transport=transport or http_transport,
            carver=carver or FfmpegCarver(),
            budget=budget,
            host=recognition.host,
            ledger=ledger,
            cache=cache,
            refresh=refresh,
        )

    return run


__all__ = [
    "CACHE_KEY",
    "CACHE_VERSION",
    "CHUNK_S",
    "ENDPOINT",
    "INTERVAL_S",
    "LEDGER_KEY",
    "LEDGER_LOCK_KEY",
    "MAX_CALLS_PER_RUN",
    "MAX_PARTS",
    "MONTHLY_KEY",
    "SAMPLE_RATE",
    "UNREACHED_STOP",
    "Budget",
    "Carver",
    "ChunkPlan",
    "FfmpegCarver",
    "Ledger",
    "Match",
    "Outcome",
    "RecognitionCache",
    "Request",
    "Response",
    "Transport",
    "assert_month_within",
    "assert_one_set",
    "assert_run_within",
    "bound_identifier",
    "classify",
    "content_digest",
    "current_month",
    "fold",
    "http_transport",
    "identify",
    "keychain_credentials",
    "parse_match",
    "partition",
    "parts_needed",
    "planned_calls",
    "request_for",
    "sample_offsets",
    "sign",
]
