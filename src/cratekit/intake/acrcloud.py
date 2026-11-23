"""The recognition identifier: ACRCloud, behind the seam ``recognize.identify`` declares.

**SPENDING IS THE DESIGN CONSTRAINT.** Every chunk sent is a paid call, so:

* the credentials are read through :mod:`cratekit.core.secrets` at CALL time,
  after the presence gate in :mod:`cratekit.intake.recognize` has passed;
* the call count is KNOWN BEFORE THE FIRST CALL, because the grid is a
  function of the duration alone, and it is checked against the per run cap
  and the month's ledger before any audio is carved;
* every attempt is recorded in the ledger the moment it is made, so a crash
  mid set does not forget calls already spent;
* a run whose calls stop getting answers stops after a few, so an offline
  machine costs a handful of attempts and not a set;
* a spend refusal (this module's bound or the service's quota answer) is a
  DIFFERENT cause from a chunk the service did not recognise. The source
  system once read a 565 call batch of quota refusals as content misses.

**EVERYTHING THAT TOUCHES THE OUTSIDE IS INJECTED.** The carver (ffmpeg and
ffprobe) and the transport (one HTTP post per chunk) are parameters with
shipped defaults, so the suite runs with no credential and no binary.

**THE HOST AND THE MONTHLY BOUND ARE THE USER'S** (R-301): ``recognition.host``
because an account belongs to one region, and ``recognition.monthly_calls``.
Neither has a default HERE, so no caller reaches the paid path with a host or
a month nobody chose.

**THE RESPONSE MAPPING IS UNVERIFIED against a live account.** The status
families are the source system's, with 3015 moved from quota to miss and 3100
added as transient from the vendor's published table.
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
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Protocol

from cratekit.acquire import match
from cratekit.acquire.match import Wanted
from cratekit.core import binaries, config, secrets
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake.recognize import Identified, Progress

#: The identify endpoint's path. The regional host is ``recognition.host``.
ENDPOINT = "/v1/identify"

#: Twelve seconds of 16 kHz mono PCM, under the service's one megabyte sample
#: limit, every twenty five seconds: a short edit is caught without paying
#: for overlap.
CHUNK_S = 12
INTERVAL_S = 25
SAMPLE_RATE = 16000

#: The most calls one RUN may cost. A two hour set is 288 calls. A recording
#: that needs more is identified in PARTS (R-706), never trimmed: a report
#: over its first three hours only is a report over audio nothing looked at.
MAX_CALLS_PER_RUN = 400

#: The most even parts one recording is identified in (Part A, B and C, by
#: Phillip's decision of 2026-09-24). Three parts is over eight hours; a file
#: needing more is refused before the first call as not one set.
MAX_PARTS = 3

#: How often the identify counter speaks, in calls sent (R-924), besides the
#: first and the last: about a line every half minute on a long set.
PROGRESS_EVERY = 20

#: Attempts in a row with no answer (an unreadable answer, a non 200 status, a
#: transport that raised, a transient code) before the run stops. A match or a
#: miss resets the count. Five is a network blip; more is a machine offline.
UNREACHED_STOP = 5

#: Status code families. A NON ZERO CODE IS NOT A MISS: only 1001 and the two
#: no-fingerprint codes are. Quota and credential codes end the run, because
#: every later call meets the same answer; the rest of the 2000s, 3000 and
#: 3100 are per chunk and transient.
_MATCH_CODE = 0
_MISS_CODES = frozenset({1001, 2004, 3015})
_QUOTA_CODES = frozenset({3003})
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
_TRANSIENT_CODES = frozenset({3000, 3100})

#: The service's own protocol constants, sent with every request.
_DATA_TYPE = "audio"
_SIGNATURE_VERSION = "1"
_TIMEOUT_S = 30

#: ffprobe's arguments before the file: the duration in seconds, bare.
_PROBE_ARGS = "-v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1"


class Outcome(StrEnum):
    """What one chunk's answer was, as a family rather than a code."""

    MATCH = "match"
    MISS = "miss"
    QUOTA = "quota"
    AUTH = "auth"
    TRANSIENT = "transient"
    UNCLASSIFIED = "unclassified"


#: The two families that are an ANSWER about the audio, so the only two the
#: recognition cache keeps or serves.
_KEPT_OUTCOMES = frozenset({Outcome.MATCH, Outcome.MISS})


@dataclass(frozen=True, slots=True)
class Request:
    """One signed identify call. Carries the access key the service requires
    in the clear; the signing key is consumed by :func:`sign`."""

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
    """The shipped transport, one multipart post over ONE session per process,
    because a fresh TLS handshake per chunk is a minute on a two hour set.
    ``requests`` is imported lazily: a process listing jobs has no use for it.
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


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    env = binaries.subprocess_env()
    return subprocess.run(argv, capture_output=True, text=True, env=env, check=False)


class FfmpegCarver:
    """The shipped carver. Resolves both binaries through :mod:`core.binaries`
    at call time, so an override is honoured, and runs them with that module's
    credential stripped environment. One process per chunk, seeking before
    the input so the seek is fast.
    """

    def duration(self, source: Path) -> float:
        result = _run([binaries.resolve("ffprobe"), *_PROBE_ARGS.split(), str(source)])
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
            argv = [binaries.resolve("ffmpeg"), "-ss", str(offset_s), "-t", str(chunk_s)]
            argv += ["-i", str(source), "-ar", str(SAMPLE_RATE), "-ac", "1", "-y"]
            argv += ["-loglevel", "error", str(target)]
            result = _run(argv)
            if result.returncode != 0 or not target.is_file():
                raise RuntimeError(
                    f"ffmpeg could not carve {source.name} at {offset_s}s: "
                    f"{result.stderr.strip() or 'no output'}"
                )
            return target.read_bytes()


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


def planned_calls(duration_s: float, *, chunk_s: int = CHUNK_S, interval_s: int = INTERVAL_S) -> int:
    """How many chunks a recording this long costs, WITHOUT building the grid.

    Arithmetic so the budget is checked before the grid exists: a broken
    header answering two billion seconds is refused by the cap rather than
    allocating two billion offsets. A duration that is not finite is zero.
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
    """Where the chunks are taken from, in seconds. A recording shorter than
    one chunk still gets its opening one, and nothing is taken past the point
    where a whole chunk fits, so no chunk is padded with silence."""
    count = planned_calls(duration_s, chunk_s=chunk_s, interval_s=interval_s)
    return tuple(offset * interval_s for offset in range(count))


def parts_needed(planned: int, *, per_run: int = MAX_CALLS_PER_RUN) -> int:
    """How many runs a grid of ``planned`` chunks takes, without building it."""
    if planned <= 0:
        return 0
    return -(-planned // per_run)


def partition(
    offsets: tuple[int, ...], *, per_run: int = MAX_CALLS_PER_RUN
) -> tuple[tuple[int, ...], ...]:
    """The grid as the fewest EVEN, contiguous parts each at or under ``per_run``.

    Sizes differ by at most one, in grid order, so a five hour mix is two
    halves and not a full run and a sliver. An empty grid is no parts.
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


#: The two declared state entries the ledger lives in. Installation scoped,
#: because the counter is bound to the credential's quota, not to a library.
LEDGER_KEY = "identify_usage"
LEDGER_LOCK_KEY = "identify_usage_lock"


def current_month(now: datetime | None = None) -> str:
    """The ledger's month key, local time, because a quota resets on the
    person's calendar and not on UTC's."""
    return (now or datetime.now()).strftime("%Y-%m")


class Ledger:
    """The monthly call counter, on core's lock and core's atomic writer.

    ADVISORY: the service reports no remaining quota, so this counts what THIS
    machine spent. The live quota code is the real ceiling; this stops a run
    that would obviously exceed ``recognition.monthly_calls`` before it starts.

    A ledger that cannot be READ counts as zero, because a corrupt counter must
    not lock recognition out; one that cannot be LOCKED or WRITTEN raises,
    because a call made and not counted is the drift it exists to prevent. One
    lock and one write per call, so no crash window opens between the post
    and the count.
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
        config.mkdir_private(self.lock_path.parent)
        config.mkdir_private(self.path.parent)
        with config.exclusive_lock(self.lock_path):
            counts = self._read()
            counts[key] = counts.get(key, 0) + calls
            payload = json.dumps(counts, indent=2, sort_keys=True) + "\n"
            config.atomic_write_bytes(payload.encode("utf-8"), self.path)
            return counts[key]


@dataclass(frozen=True, slots=True)
class Budget:
    """What a run may spend. ``monthly`` of None leaves the month unbounded
    (the ledger still counts); only a hand built budget says that, because
    :meth:`from_config` always carries the section's bound."""

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

    A file that is not a set is refused before the first call; a long set is
    not. The same cause and ``per-run`` kind as the run bound, so the detail
    still tells this build's bound from the service's quota answer.
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
    """Refuse a RUN that would exceed the per run bound. Asked of every part
    before the first call, so the bound is a property of the spend and not of
    the partition that happened to be built."""
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

    READ BY THE LIST READERS' OWN ROW READER, ``match.read_row``, so a
    recognised track and the same track pasted in a tracklist fold to one
    identity. None for a hit naming no artist or no title, which the reader
    refuses; the caller counts it as a miss. ``origin`` is ``text`` because a
    recognised track carries no identifier acquisition could fetch.
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
    """One row per track played, in the order first heard.

    ADJACENT answers naming the same recording (by ISRC when both carry one,
    by the recording's identity otherwise) fold to one, keeping the FIRST
    offset and the best score. A record played twice in a set stays twice.
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
    # The identity, not the token: two titles that fold to nothing by one
    # artist share a token, and played back to back they are two rows.
    return (
        one.wanted.distinct == other.wanted.distinct
        and one.wanted.version_key == other.wanted.version_key
    )


#: The declared state entry the cache lives in, one document per recording and
#: chunk plan. Installation scoped: an answer is a fact about the audio, paid
#: for on the credential's quota.
CACHE_KEY = "identify_cache"

#: The cache document's own version. A document carrying any other is a miss.
CACHE_VERSION = 1

#: How much of the recording is read at a time while it is digested.
_DIGEST_BLOCK = 1 << 20


def content_digest(source: Path) -> str:
    """The sha256 of the recording's BYTES, streamed.

    A path, a size or a modification time is not unique to the audio: a set
    exported over another keeps the path, a copy keeps neither. Reading the
    whole file costs time; a stale answer would cost money and a false
    tracklist.
    """
    hashed = hashlib.sha256()
    with source.open("rb") as handle:
        while block := handle.read(_DIGEST_BLOCK):
            hashed.update(block)
    return hashed.hexdigest()


@dataclass(frozen=True, slots=True)
class ChunkPlan:
    """Everything that decides what one chunk's answer is an answer ABOUT:
    which audio, which slices carved how, and which regional host. Change any
    one and a kept answer answers a different question, so all are in the key
    and the document carries the plan to be checked again on the way in."""

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

    The service's RAW answer is kept, so a later build that reads answers
    better reads kept ones better too. ONLY AN ANSWER IS KEPT, a match or a
    miss, in both directions: a transient, quota or credential answer says
    nothing about the audio, and keeping one would make a blip a permanent
    hole. A document that cannot be read, or disagrees with its plan, is a
    miss: the cost is money, never a false tracklist. A write failure raises
    to the caller, who reports it.

    THE WRITE IS A LOCKED MERGE: two passes over one recording can overlap,
    and a writer that replaced the document would drop what the other paid
    for, so it is read again under a sibling lock and laid over.
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
        with config.exclusive_lock(path.with_suffix(".lock")):
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


Credentials = Callable[[], tuple[str, str]]


def keychain_credentials() -> tuple[str, str]:
    """The access key and the signing key, retrieved NOW.

    The presence gate has passed, so a failure is the keychain refusing what it
    said it held. The exception's own remedy is passed on, because telling a
    person to record a credential into a store that cannot hold one is the
    wrong instruction.
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
    progress: Progress | None = None,
) -> Identified:
    """Identify the tracks in ``source``. Bounded before the first call.

    The order is the spend order: the duration is read and the call count
    computed BEFORE the credentials are retrieved, so a file that is not a set
    never prompts the keychain, and the budget is checked BEFORE the grid is
    built or a chunk carved. Each attempt is in the ledger before its answer
    is read.

    A quota or credential answer ends the run, because every later call meets
    the same one; so does an answer this build cannot classify, rather than
    paying into it. A transient answer skips the CHUNK until
    ``UNREACHED_STOP`` arrive in a row, and the unanswered count is returned
    apart from the misses, because incomplete coverage is not a result.

    A CHUNK ALREADY ANSWERED IS NOT PAID FOR AGAIN: kept answers for the
    recording's chunk plan are read before anything is carved, and a
    recording kept whole never retrieves a credential. The parts ceiling reads
    the WHOLE grid, since it refuses a file that is not a set; the run and
    monthly bounds read only what is owed, since they bound spend. ``refresh``
    reads nothing kept, because the service's catalogue grows and a kept miss
    may be nameable now. WHAT WAS PAID FOR IS KEPT ON THE WAY OUT, a raise
    included, so the pass after a quota reset pays for the rest, not the set.

    ``budget`` AND ``host`` HAVE NO DEFAULT (R-301): a default is how nothing
    got chosen. :func:`bound_identifier` builds both from the configuration.

    A SET LONGER THAN ONE RUN IS IDENTIFIED IN PARTS (R-706): the grid is cut
    by :func:`partition`, the run bound is asked of every part and the month
    once over the whole set before the first call, and one pass walks the
    parts in grid order and folds once, so a record across a cut is one row.
    The parts are places in the grid, never files.

    ``progress`` is told the plan before the first call, then the count sent
    as it climbs (R-924); a recording the cache answers whole sends nothing.
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
    # Bytes that cannot be digested are identified WITHOUT the cache rather
    # than refused (the carver decides whether audio can be sent), and the
    # cost is said, because the next pass will pay again.
    try:
        plan, unkept = ChunkPlan(digest=content_digest(source), offsets=offsets, host=host), ""
    except OSError as exc:
        plan, unkept = None, f"the recording could not be read for its digest ({type(exc).__name__})"
    kept = kept_in.read(plan) if plan is not None and not refresh else {}
    owed = [offset for offset in offsets if offset not in kept]
    run = _Pass(source, transport, carver, counter, host, month, kept)
    try:
        result = _identified(run, parts, owed, spend=spend, credentials=credentials, progress=progress)
    finally:
        # Keeps what a pass that RAISED had already paid for. A failed write
        # must not replace the refusal on its way out; on a pass that returned
        # it is reported instead.
        if run.paid and plan is not None:
            try:
                kept_in.write(plan, run.paid)
            except (config.ConfigLockUnavailable, OSError) as exc:
                unkept = f"{type(exc).__name__}: {exc}"
    return replace(
        result,
        cache_unwritten=unkept if run.paid else "",
        digest=plan.digest if plan is not None else "",
    )


@dataclass(slots=True)
class _Pass:
    """One pass's seams and running counts. ``paid`` is filled as each answer
    arrives, so the caller keeps it whether the pass returns or raises."""

    source: Path
    transport: Transport
    carver: Carver
    counter: Ledger
    host: str
    month: str | None = None
    kept: Mapping[int, Mapping[str, Any]] = field(default_factory=dict)
    keys: tuple[str, str] = ("", "")
    paid: dict[int, Mapping[str, Any]] = field(default_factory=dict)
    found: list[Match] = field(default_factory=list)
    calls: int = 0
    misses: int = 0
    unreached: int = 0
    streak: int = 0

    def heard(self, payload: Mapping[str, Any], offset: int) -> None:
        """Count one KEPT family answer, fresh or kept alike, so a chunk means
        the same on the pass that paid for it and the pass that did not."""
        matched = classify(payload)[0] is Outcome.MATCH
        parsed = parse_match(payload, offset_s=offset) if matched else None
        if parsed is None:
            self.misses += 1
        else:
            self.found.append(parsed)

    def chunk(self, offset: int) -> int:
        """One chunk: served from what is kept, or carved, counted and sent.
        Returns the calls sent so far; raises the answers that end the run."""
        if offset in self.kept:
            self.heard(self.kept[offset], offset)
            return self.calls
        source, calls = self.source, self.calls
        try:
            sample = self.carver.carve(source, offset, CHUNK_S)
        except (RuntimeError, OSError, binaries.BinaryNotFound) as exc:
            raise _failed(
                f"{source.name} could not be carved at {offset}s after {calls} call(s): {exc}",
                source=str(source),
                offset_s=offset,
                calls=calls,
            ) from exc
        access_key, signing_key = self.keys
        request = request_for(sample, access_key=access_key, signing_key=signing_key, host=self.host)
        try:
            self.counter.record(1, self.month)
        except (config.ConfigLockUnavailable, OSError) as exc:
            raise _failed(
                f"the recognition ledger could not record a call ({exc}), so the "
                f"call was not made; {calls} call(s) were made before it",
                calls=calls,
            ) from exc
        self.calls = calls = calls + 1
        outcome, code, message, payload = _answer(self.transport, request)
        if outcome in _KEPT_OUTCOMES:
            self.streak = 0
            self.paid[offset] = payload or {}
            self.heard(payload or {}, offset)
        elif outcome is Outcome.QUOTA:
            raise _quota_refusal(code, message, calls=calls)
        elif outcome is Outcome.AUTH:
            raise _auth_refusal(code, message)
        elif outcome is Outcome.TRANSIENT:
            self.unreached += 1
            self.streak += 1
            if self.streak >= UNREACHED_STOP:
                raise _failed(
                    f"{self.streak} calls in a row for {source.name} got no usable answer, the "
                    f"last one {message}, so the run stopped after {calls} call(s) rather "
                    f"than paying the rest of the set into a service it cannot reach; "
                    f"the calls were counted",
                    source=str(source),
                    calls=calls,
                    unreached=self.unreached,
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
        return calls


def _identified(
    run: _Pass, parts: tuple[tuple[int, ...], ...], owed: list[int], *,
    spend: Budget, credentials: Credentials, progress: Progress | None = None,
) -> Identified:
    """The pass itself. Every part is asked of the run bound, and the month
    once over ``owed``, the whole set's, BEFORE any part starts, so an
    oversize part, first or last, is refused with nothing spent."""
    counter, month, still_owed = run.counter, run.month, frozenset(owed)
    for part in parts:
        assert_run_within(spend, planned=sum(1 for offset in part if offset in still_owed))
    keys = ("", "")
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
    # AFTER EVERY REFUSAL THAT SPENDS NOTHING, so a run told it is about to pay
    # is a run that will, and one refused by a bound or a missing key is told
    # only the refusal.
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
    run.keys = keys
    for part in parts:
        for offset in part:
            before = run.calls
            calls = run.chunk(offset)
            if progress is not None and calls > before and _worth_saying(calls, len(owed)):
                progress(f"identifying: sent {calls} of {len(owed)} call(s)")
    if run.unreached and run.unreached == len(offsets):
        raise _failed(
            f"none of the {run.calls} call(s) for {run.source.name} got an answer, so nothing "
            f"is known about it; the calls were counted",
            source=str(run.source),
            calls=run.calls,
        )
    return Identified(
        rows=tuple(one.wanted for one in fold(run.found)),
        calls=run.calls,
        chunks=len(offsets),
        misses=run.misses,
        unreached=run.unreached,
        cached=len(offsets) - len(owed),
        parts=len(parts),
    )


def _plan_line(chunks: int, *, cached: int, parts: int) -> str:
    """What identification will cost, said before the first call is sent."""
    owed = chunks - cached
    if owed == 0:
        return (
            f"identifying: all {chunks} chunk(s) are answered from the recognition "
            f"cache, so no call is sent"
        )
    split = f" in {parts} parts" if parts > 1 else ""
    return (
        f"identifying: {chunks} chunk(s) planned, {cached} answered from the "
        f"recognition cache, {owed} paid call(s) to send{split}"
    )


def _worth_saying(calls: int, owed: int) -> bool:
    """The first call, every :data:`PROGRESS_EVERY`, and the last."""
    return calls == 1 or calls == owed or calls % PROGRESS_EVERY == 0


def bound_identifier(
    recognition: config.RecognitionConfig,
    *,
    transport: Transport | None = None,
    carver: Carver | None = None,
    ledger: Ledger | None = None,
    cache: RecognitionCache | None = None,
    refresh: bool = False,
    progress: Progress | None = None,
) -> Callable[[Path], Identified]:
    """The identifier in the seam's own shape, over the shipped seams.

    RESOLVED AT CALL TIME, so nothing touches a binary or a network until a
    recording is handed over, and a suite that replaces a seam on the module
    reaches the paid path. ``recognition`` is the ONLY source of the host and
    the monthly bound.
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
            progress=progress,
        )

    return run
