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
  audio is carved;
* every attempt is recorded in the ledger the moment it is made, whether or
  not an answer came back, so a crash mid set does not forget the calls it
  already spent;
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

**THE HOST IS A CONSTANT, RECORDED RATHER THAN HIDDEN.** ACRCloud's identify
endpoint is regional and an account belongs to one region. The source system
kept the host beside the credentials; here the two credentials are the whole
recognition surface, so the host is the module's default and the attended
binding is where a different region would be discovered. A configuration
field is the right home and is filed as a residual, not built here.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import subprocess
import tempfile
import time
from collections.abc import Callable, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Protocol

from cratekit.acquire import match
from cratekit.acquire.match import Wanted
from cratekit.core import binaries, config, secrets
from cratekit.core.cause import CratekitError, refuse
from cratekit.core.exit_codes import Remedy

# ---------------------------------------------------------------------------
# The grid, the bound, the endpoint
# ---------------------------------------------------------------------------

#: The identify endpoint's regional host. See the module docstring.
HOST = "identify-us-west-2.acrcloud.com"
ENDPOINT = "/v1/identify"

#: One chunk is twelve seconds of 16 kHz mono PCM, which is under the service's
#: one megabyte sample limit and gives it more to fingerprint than the 8 kHz
#: alternative. Chunks are taken every twenty five seconds: at roughly three
#: per minute the grid catches a short edit without paying for overlap.
CHUNK_S = 12
INTERVAL_S = 25
SAMPLE_RATE = 16000

#: The most calls one recording may cost. A two hour set on the grid above is
#: 288 calls, so this admits any set a person would play and refuses a file
#: that is not a set at all before the first call rather than after the
#: three hundredth. A run needing more is refused, never trimmed: a recording
#: identified for its first three hours and silently not for its fourth is a
#: report over audio nothing looked at.
MAX_CALLS_PER_RUN = 400

#: What the service's status codes mean, as families. A NON ZERO CODE IS NOT A
#: MISS: only 1001 is. The two quota codes and the four credential codes end
#: the run, because every later call would meet the same answer, and the
#: 2000s and 3000 are per chunk and transient.
_QUOTA_CODES = frozenset({3003, 3015})
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
_MISS_CODE = 1001
_MATCH_CODE = 0

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


# ---------------------------------------------------------------------------
# The two seams
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Request:
    """One signed identify call, ready to send. Carries no credential but the
    access key the service requires in the clear; the signing key never leaves
    :func:`sign`."""

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


def http_transport(request: Request) -> Response:
    """The shipped transport, one multipart post. Imported lazily because a
    process listing jobs has no business loading an HTTP client."""
    import requests  # noqa: PLC0415 - see the docstring

    answer = requests.post(
        request.url,
        files={"sample": (request.filename, request.sample, "audio/wav")},
        data=dict(request.fields),
        timeout=_TIMEOUT_S,
    )
    return Response(status=int(answer.status_code), body=bytes(answer.content))


class FfmpegCarver:
    """The shipped carver. Resolves both binaries through :mod:`core.binaries`
    at call time, so an override or a fallback directory is honoured, and runs
    them with the credential stripped environment that module builds."""

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
    host: str = HOST,
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


def sample_offsets(
    duration_s: float, *, chunk_s: int = CHUNK_S, interval_s: int = INTERVAL_S
) -> tuple[int, ...]:
    """Where the chunks are taken from, as seconds, for a recording this long.

    A recording shorter than one chunk still gets its opening chunk, so a
    zero result over a short file is a real answer rather than a grid that
    was empty. Nothing is taken past the point where a whole chunk no longer
    fits, so the last chunk is never padded with silence.
    """
    whole = int(duration_s)
    if whole <= 0:
        return ()
    if whole < chunk_s:
        return (0,)
    return tuple(range(0, whole - chunk_s + 1, interval_s))


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
    """The monthly call counter, serialized under its sibling lock.

    ADVISORY BY NATURE. The service's answer carries no remaining quota field,
    so the count here is what THIS machine spent and can drift from the
    account when another tool shares the key. The live quota code is the real
    ceiling; this ledger is what stops a run that would obviously exceed it
    from making the first call.

    A ledger that cannot be READ counts as zero rather than refusing, because a
    corrupt counter must not lock recognition out; a ledger that cannot be
    WRITTEN raises, because a call that was made and not counted is exactly the
    drift the counter exists to prevent.
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

    @contextmanager
    def _locked(self):
        config._mkdir_private(self.lock_path.parent)
        descriptor = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, config.PRIVATE_FILE_MODE)
        handle = os.fdopen(descriptor, "r+b")
        try:
            try:
                import fcntl  # noqa: PLC0415 - POSIX only, guarded below

                fcntl.flock(handle, fcntl.LOCK_EX)
            except ImportError:
                pass
            yield
        finally:
            handle.close()

    def record(self, calls: int, month: str | None = None) -> int:
        """Add ``calls`` to the month and return the new total."""
        if calls <= 0:
            return self.used(month)
        key = month or current_month()
        with self._locked():
            counts = self._read()
            counts[key] = counts.get(key, 0) + int(calls)
            config._mkdir_private(self.path.parent)
            fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as out:
                    json.dump(counts, out, indent=2, sort_keys=True)
                if config._CAN_SET_MODE:
                    os.chmod(tmp, config.PRIVATE_FILE_MODE)
                os.replace(tmp, self.path)
            except BaseException:
                if os.path.exists(tmp):
                    os.unlink(tmp)
                raise
            return counts[key]


@dataclass(frozen=True, slots=True)
class Budget:
    """What a run may spend. ``monthly`` of None means the month is not bounded
    by this tool, and the ledger still counts."""

    per_run: int = MAX_CALLS_PER_RUN
    monthly: int | None = None


def assert_within(budget: Budget, *, planned: int, used_this_month: int) -> None:
    """Refuse BEFORE the first call when the plan exceeds either bound."""
    if planned > budget.per_run:
        raise refuse(
            "intake-recognition-spend-bound",
            f"this recording would take {planned} recognition calls and the per "
            f"run bound is {budget.per_run}; nothing was sent. A file this long "
            f"is not one set, so split it rather than raising the bound",
            origin=("intake.acrcloud",),
            detail={"planned": planned, "bound": budget.per_run, "kind": "per-run"},
        )
    if budget.monthly is not None and used_this_month + planned > budget.monthly:
        raise refuse(
            "intake-recognition-spend-bound",
            f"this recording would take {planned} recognition calls, "
            f"{used_this_month} were already spent this month, and the monthly "
            f"bound is {budget.monthly}; nothing was sent",
            remedy=Remedy.RETRY_LATER,
            origin=("intake.acrcloud",),
            detail={
                "planned": planned,
                "used": used_this_month,
                "bound": budget.monthly,
                "kind": "monthly",
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
    if code == _MISS_CODE:
        return Outcome.MISS, code, message
    if code in _QUOTA_CODES:
        return Outcome.QUOTA, code, message
    if code in _AUTH_CODES:
        return Outcome.AUTH, code, message
    if 2000 <= code < 3000 or code == 3000:
        return Outcome.TRANSIENT, code, message
    return Outcome.UNCLASSIFIED, code, message


@dataclass(frozen=True, slots=True)
class Match:
    """One recognised chunk: where it was taken and what the service said."""

    offset_s: int
    wanted: Wanted
    score: int


def _first_artist(entries: object) -> str:
    """The primary artist, read the way the list readers read one: the first
    named entry, never a join. A comma is legal inside one artist's name."""
    if isinstance(entries, str):
        return entries.strip()
    if not isinstance(entries, (list, tuple)):
        return ""
    for entry in entries:
        name = entry.get("name") if isinstance(entry, Mapping) else entry
        if isinstance(name, str) and name.strip():
            return name.strip()
    return ""


def parse_match(payload: Mapping[str, Any], *, offset_s: int) -> Match | None:
    """The top hit of a MATCH answer as a ``Wanted`` row, or None.

    None is returned for a match that names no artist or no title, because
    the half that is left is not unique to the recording it means, which is
    the same rule every list reader applies. The caller counts it as a miss
    rather than silently dropping it.

    The title is split the way the readers split one, so ``Wanted.version``
    and the recording token agree with a pasted tracklist naming the same
    record. ``origin`` is ``text`` because a recognised track names a
    recording and not a provider row: it carries no identifier acquisition
    could ask for, and freezing it as a provider row would queue an item
    nothing can fetch.
    """
    metadata = payload.get("metadata") or {}
    music = metadata.get("music") if isinstance(metadata, Mapping) else None
    if not isinstance(music, list) or not music:
        return None
    top = music[0]
    if not isinstance(top, Mapping):
        return None
    raw_title = str(top.get("title") or "").strip()
    artist = _first_artist(top.get("artists"))
    if not artist or not raw_title:
        return None
    title, version = match.split_title(raw_title)
    if not title:
        return None
    external = top.get("external_ids") or {}
    isrc = str(external.get("isrc") or "").strip() if isinstance(external, Mapping) else ""
    score_raw = top.get("score", 0)
    try:
        score = int(score_raw)
    except (TypeError, ValueError):
        score = 0
    return Match(
        offset_s=offset_s,
        wanted=Wanted(
            artist=artist,
            title=title,
            version=version,
            isrc=isrc or None,
            origin=match.TEXT,
            spelled=raw_title,
            other_reading=match.split_ambiguous(raw_title),
        ),
        score=score,
    )


def fold(matches: Sequence[Match]) -> tuple[Match, ...]:
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
# Identification
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Recognition:
    """What one identification did, beyond the rows it returns."""

    rows: tuple[Wanted, ...]
    calls: int
    chunks: int
    misses: int
    unreached: int
    matches: tuple[Match, ...] = field(default_factory=tuple)


Credentials = Callable[[], tuple[str, str]]


def keychain_credentials() -> tuple[str, str]:
    """The access key and the signing key, retrieved NOW. The presence gate
    has already passed, so a failure here is the keychain refusing to hand
    over what it said it held, and that is reported as the gate class."""
    try:
        return (
            secrets.get(str(secrets.Credential.IDENTIFY_KEY)),
            secrets.get(str(secrets.Credential.IDENTIFY_SIGNING_KEY)),
        )
    except secrets.CredentialError as exc:
        raise refuse(
            "intake-recognition-unready",
            f"the recognition credentials are recorded and could not be read: {exc}",
            remedy=Remedy.SET_CREDENTIAL,
            origin=("intake.acrcloud",),
            detail={"credential": getattr(exc, "name", None)},
        ) from exc


def _decoded(response: Response) -> Mapping[str, Any] | None:
    """The answer as a mapping, or None for anything this build cannot read."""
    if response.status != 200:
        return None
    try:
        parsed = json.loads(response.body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    return parsed if isinstance(parsed, Mapping) else None


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
    credentials: Credentials = keychain_credentials,
    budget: Budget | None = None,
    ledger: Ledger | None = None,
    host: str = HOST,
    month: str | None = None,
) -> Recognition:
    """Identify the tracks in ``source``. Bounded before the first call.

    The order is the spend order. The duration is read and the grid planned
    BEFORE the credentials are retrieved, so a file that is not a set never
    prompts the keychain. The budget is checked against the plan BEFORE the
    first chunk is carved. Each attempt is recorded in the ledger before its
    answer is read, so a crash between the two leaves the call counted.

    Three answers end the run and two do not. A quota or a credential answer
    ends it, because every later call would meet the same one; an answer this
    build cannot classify ends it, because a run that keeps paying into an
    answer it does not understand is the 565 call batch. A transient answer,
    or a transport that raised, skips the CHUNK and the run goes on, and the
    count of chunks that never got an answer is returned rather than folded
    into the misses, because coverage that is incomplete is not a result.
    """
    spend = budget or Budget()
    counter = ledger or Ledger()
    try:
        duration_s = carver.duration(source)
    except (RuntimeError, OSError, binaries.BinaryNotFound) as exc:
        raise _failed(
            f"{source.name} could not be measured, so no chunk was carved and nothing "
            f"was sent: {exc}",
            source=str(source),
        ) from exc
    offsets = sample_offsets(duration_s)
    if not offsets:
        raise _failed(
            f"{source.name} holds no audio to identify (duration {duration_s:.1f}s), so "
            f"nothing was sent",
            source=str(source),
        )
    assert_within(spend, planned=len(offsets), used_this_month=counter.used(month))
    access_key, signing_key = credentials()

    found: list[Match] = []
    calls = misses = unreached = 0
    for offset in offsets:
        try:
            sample = carver.carve(source, offset, CHUNK_S)
        except (RuntimeError, OSError, binaries.BinaryNotFound) as exc:
            raise _failed(
                f"{source.name} could not be carved at {offset}s after {calls} call(s): {exc}",
                source=str(source),
                offset_s=offset,
                calls=calls,
            ) from exc
        request = request_for(
            sample, access_key=access_key, signing_key=signing_key, host=host
        )
        calls += 1
        counter.record(1, month)
        try:
            response = transport(request)
        except Exception:  # noqa: BLE001 - the transport's failures are open ended
            unreached += 1
            continue
        payload = _decoded(response)
        if payload is None:
            unreached += 1
            continue
        outcome, code, message = classify(payload)
        if outcome is Outcome.MATCH:
            parsed = parse_match(payload, offset_s=offset)
            if parsed is None:
                misses += 1
            else:
                found.append(parsed)
        elif outcome is Outcome.MISS:
            misses += 1
        elif outcome is Outcome.QUOTA:
            raise _quota_refusal(code, message, calls=calls)
        elif outcome is Outcome.AUTH:
            raise _auth_refusal(code, message)
        elif outcome is Outcome.TRANSIENT:
            unreached += 1
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
    if unreached and unreached == len(offsets):
        raise _failed(
            f"none of the {calls} call(s) for {source.name} got an answer, so nothing "
            f"is known about it; the calls were counted",
            source=str(source),
            calls=calls,
        )
    matches = fold(found)
    return Recognition(
        rows=tuple(one.wanted for one in matches),
        calls=calls,
        chunks=len(offsets),
        misses=misses,
        unreached=unreached,
        matches=matches,
    )


def bound_identifier(
    *,
    transport: Transport | None = None,
    carver: Carver | None = None,
    budget: Budget | None = None,
    ledger: Ledger | None = None,
) -> Callable[[Path], tuple[Wanted, ...]]:
    """The identifier in the seam's own shape, over the shipped seams.

    RESOLVED AT CALL TIME, not at import: the transport and the carver are
    looked up when the returned callable runs, so nothing here touches a
    binary or a network until a recording is actually handed over.
    """

    def run(source: Path) -> tuple[Wanted, ...]:
        return identify(
            source,
            transport=transport or http_transport,
            carver=carver or FfmpegCarver(),
            budget=budget,
            ledger=ledger,
        ).rows

    return run


__all__ = [
    "CHUNK_S",
    "ENDPOINT",
    "HOST",
    "INTERVAL_S",
    "LEDGER_KEY",
    "LEDGER_LOCK_KEY",
    "MAX_CALLS_PER_RUN",
    "SAMPLE_RATE",
    "Budget",
    "Carver",
    "FfmpegCarver",
    "Ledger",
    "Match",
    "Outcome",
    "Recognition",
    "Request",
    "Response",
    "Transport",
    "assert_within",
    "bound_identifier",
    "classify",
    "current_month",
    "fold",
    "http_transport",
    "identify",
    "keychain_credentials",
    "parse_match",
    "request_for",
    "sample_offsets",
    "sign",
]
