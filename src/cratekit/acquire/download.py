"""Bounded, paced acquisition that tells a throttle from a block (U15).

The concurrency cap is ``AdapterSettings.concurrency`` and nowhere else (KTD20).

A rate limit honours the provider's retry hint, or backs off, and keeps trying. A
forbidden response or a bot challenge stops the whole run at once and parks it, because
retrying into a block turns it into a lockout the account may not recover from. Mixed
evidence reads as BLOCKED, a provider's hint is jittered upward only, and jitter is wide
by default so runs do not re-converge into a retry storm.

The module returns the cause a job engine parks on (``DownloadRun.parked``) rather than
parking itself, as KTD23's layering requires. It reads the adapter's settings, no config
file, and names no verb.
"""

from __future__ import annotations

import random
import re
import threading
import time
from collections.abc import Callable, Iterable, Sequence
from concurrent.futures import Executor, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum

from cratekit.acquire.adapter import (
    AdapterAuthFailed,
    AdapterBroken,
    AdapterSettings,
    BaseAdapter,
    InvocationOutcome,
    InvocationResult,
    NoFileLanded,
    Remedy,
    TrackOutcome,
    TrackRequest,
    TrackResult,
    TrackSource,
    acquire_one,
)
from cratekit.core import provider_gate
from cratekit.core.cause import Cause, Remediation, Scope

# ---------------------------------------------------------------------------
# What the provider is telling us
# ---------------------------------------------------------------------------


class ProviderSignal(StrEnum):
    """How a failed request should change the pace, if at all."""

    #: Nothing about pacing. The per-track classifier already has the answer.
    NONE = "none"
    #: Slow down. The request itself was legitimate.
    RATE_LIMITED = "rate-limited"
    #: Stop. The provider has refused this client rather than this request.
    BLOCKED = "blocked"


#: Signals that mean "wait, then ask again".
RETRYING_SIGNALS = frozenset({ProviderSignal.RATE_LIMITED})

#: Signals that mean "make no further request on this run".
STOPPING_SIGNALS = frozenset({ProviderSignal.BLOCKED})

#: Signals that carry no pacing instruction at all.
INERT_SIGNALS = frozenset({ProviderSignal.NONE})

#: Status codes that mean "too fast", trusted over prose when present.
RATE_LIMIT_STATUSES = frozenset({429})

#: Status codes that refuse the client. Not 401, which is ``AdapterAuthFailed``.
BLOCKED_STATUSES = frozenset({403})

#: Phrases for a bot wall or a refused client, checked before the rate-limit phrases,
#: since a wall often explains itself as a rate limit.
BLOCK_MARKERS = (
    "forbidden",
    "access denied",
    "captcha",
    "are you a robot",
    "are you human",
    "unusual traffic",
    "automated traffic",
    "bot detect",
    "bot protection",
    "cloudflare",
    "attention required",
    "temporarily banned",
    "account suspended",
    "ip banned",
)

#: Phrases that mean "too fast" and nothing worse.
RATE_LIMIT_MARKERS = (
    "too many requests",
    "rate limit",
    "rate-limit",
    "ratelimit",
    "slow down",
    "throttled",
    "throttling",
)

# Statuses in free text, on word boundaries so a track id such as 40312 is no 403 (P7).
_BLOCK_STATUS_TEXT = re.compile(r"\b403\b")
_RATE_LIMIT_STATUS_TEXT = re.compile(r"\b429\b")

# The two shapes a retry hint takes in prose when it is not in a header.
_RETRY_AFTER_TEXT = re.compile(
    r"retry[-_ ]?after\s*[:=]?\s*(?P<seconds>\d+(?:\.\d+)?)", re.IGNORECASE
)
_RETRY_IN_TEXT = re.compile(
    r"(?:retry|try again)\s+in\s+(?P<seconds>\d+(?:\.\d+)?)\s*"
    r"(?:s|sec|secs|second|seconds)\b",
    re.IGNORECASE,
)

#: Attribute chains a client may expose a status through; the first present wins.
_STATUS_PATHS: tuple[tuple[str, ...], ...] = (
    ("response", "status_code"),
    ("response", "status"),
    ("status_code",),
    ("status",),
)


def _walk(obj: object, path: Sequence[str]) -> object | None:
    for name in path:
        obj = getattr(obj, name, None)
        if obj is None:
            return None
    return obj


def status_of(exc: BaseException) -> int | None:
    """The HTTP status a provider exception carries, or None rather than a guess."""
    for path in _STATUS_PATHS:
        value = _walk(exc, path)
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return None


def classify_signal(exc: BaseException) -> ProviderSignal:
    """Read a provider failure as a pacing instruction.

    A structured status decides first, since a 429 body often mentions "forbidden".
    Failing that, block phrases beat rate-limit phrases, the direction where being
    wrong is unrecoverable. Otherwise no signal. A ``NoFileLanded`` is never a signal:
    its text quotes tool output, and one "forbidden" there would park the run (R-703).
    """
    if isinstance(exc, NoFileLanded):
        return ProviderSignal.NONE
    status = status_of(exc)
    if status is not None:
        if status in BLOCKED_STATUSES:
            return ProviderSignal.BLOCKED
        if status in RATE_LIMIT_STATUSES:
            return ProviderSignal.RATE_LIMITED
        return ProviderSignal.NONE

    text = str(exc).lower()
    if _BLOCK_STATUS_TEXT.search(text) or any(m in text for m in BLOCK_MARKERS):
        return ProviderSignal.BLOCKED
    if _RATE_LIMIT_STATUS_TEXT.search(text) or any(m in text for m in RATE_LIMIT_MARKERS):
        return ProviderSignal.RATE_LIMITED
    return ProviderSignal.NONE


#: Reads one header case-insensitively with the gate's parser, so the two agree (R-705).
_header = provider_gate.header_value


def _as_seconds(value: object, now: datetime) -> float | None:
    """Coerce a retry hint to seconds through the gate's one ``Retry-After`` parser."""
    return provider_gate.retry_after_seconds(value, now.timestamp())


def retry_hint_seconds(exc: BaseException, *, now: datetime | None = None) -> float | None:
    """How long the provider asked us to wait (attribute, header, then text), or None."""
    reference = now or datetime.now(timezone.utc)

    value = getattr(exc, "retry_after", None)
    if value is None:
        value = _header(_walk(exc, ("response", "headers")), "Retry-After")
    if value is None:
        text = str(exc)
        match = _RETRY_AFTER_TEXT.search(text) or _RETRY_IN_TEXT.search(text)
        if match is not None:
            value = match.group("seconds")
    return _as_seconds(value, reference)


# ---------------------------------------------------------------------------
# Pacing policy
# ---------------------------------------------------------------------------

#: The gap between acquisitions when ``acquisition.pacing_delay_s`` is None. With the
#: default jitter it gives the replaced system's proven window of three to nine seconds.
DEFAULT_BASE_DELAY_S = 6.0

#: Half the nominal either way, wide enough that independent runs fall out of step.
DEFAULT_JITTER_FRACTION = 0.5

#: The narrowest jitter that still keeps runs started together from arriving as a burst.
MIN_DECORRELATING_JITTER = 0.25


@dataclass(frozen=True, slots=True)
class Pacing:
    """How this run waits: between acquisitions, and after being told to slow down.

    Mechanism, kept out of config so nobody can set it to zero; the cap and the
    nominal delay live in ``AdapterSettings`` (KTD20).
    """

    base_delay_s: float = DEFAULT_BASE_DELAY_S
    jitter_fraction: float = DEFAULT_JITTER_FRACTION
    backoff_base_s: float = 1.0
    backoff_max_s: float = 300.0
    #: Total tries per track, first attempt included.
    max_attempts: int = 5
    #: A longer hint parks the run: sleeping it looks hung, truncating it retries early.
    retry_hint_ceiling_s: float = 900.0

    def __post_init__(self) -> None:
        if self.base_delay_s < 0:
            raise ValueError("a pacing delay cannot be negative")
        if not 0.0 <= self.jitter_fraction <= 1.0:
            raise ValueError(
                "jitter_fraction is a fraction of the nominal delay and must be "
                "between 0 and 1; above 1 it would produce negative delays"
            )
        if self.backoff_base_s <= 0:
            raise ValueError("a backoff needs a positive base to double")
        if self.backoff_max_s < self.backoff_base_s:
            raise ValueError("the backoff ceiling cannot be below its own base")
        if self.max_attempts < 1:
            raise ValueError("a track has to be attempted at least once")
        if self.retry_hint_ceiling_s <= 0:
            raise ValueError("a retry hint ceiling of zero parks every rate limit")

    @classmethod
    def from_settings(cls, settings: AdapterSettings, **overrides: float | int) -> Pacing:
        """Take the nominal delay from the adapter, keep the rest as mechanism.

        ``is None`` rather than a falsy test, so an explicit 0.0 turns pacing off
        instead of restoring the default.
        """
        delay = settings.pacing_delay_s
        base = DEFAULT_BASE_DELAY_S if delay is None else float(delay)
        return cls(base_delay_s=base, **overrides)  # type: ignore[arg-type]


def backoff_delay(retry_index: int, pacing: Pacing) -> float:
    """The un-jittered exponential wait before retry ``retry_index``, capped."""
    if retry_index < 0:
        raise ValueError("a retry index counts from zero")
    return min(pacing.backoff_max_s, pacing.backoff_base_s * (2.0**retry_index))


def jitter(rng: random.Random, seconds: float, fraction: float) -> float:
    """Spread a delay symmetrically around its nominal value."""
    if seconds <= 0 or fraction <= 0:
        return max(0.0, seconds)
    return max(0.0, seconds * rng.uniform(1.0 - fraction, 1.0 + fraction))


def jitter_up(rng: random.Random, seconds: float, fraction: float) -> float:
    """Spread a delay upward only, for a wait the provider named, so no retry is early."""
    if seconds <= 0 or fraction <= 0:
        return max(0.0, seconds)
    return seconds * rng.uniform(1.0, 1.0 + fraction)


# ---------------------------------------------------------------------------
# The parked cause: the seam the job engine consumes
# ---------------------------------------------------------------------------

#: What a person does about a provider block, as sentences: D2 keeps command text in
#: the CLI layer.
BLOCK_REMEDIATION_STEPS = (
    "Stop acquiring from this provider until you know why it refused.",
    "Sign in to the provider directly and check the account is in good standing.",
    "Wait for the block to lift before resuming; a resumed job re-requests only "
    "what did not land.",
    "If it repeats immediately, lower the concurrency cap and raise the pacing "
    "delay before the next attempt.",
)


def blocked_cause(
    *,
    adapter: str,
    key: str,
    signal: ProviderSignal,
    detail: str,
    attempts: int,
    retry_hint_s: float | None = None,
) -> Cause:
    """The structured reason a run stopped, in the shape a job engine parks on.

    ``retryable`` is False, the load-bearing field, since an automatic retry here is
    the harm. ``scope`` is RUN, because a block is about the client, so no watermark
    advances.
    """
    return Cause(
        reason="provider-blocked",
        message=(
            f"{adapter} was refused by the provider while acquiring {key}: {detail}. "
            f"Stopped after {attempts} attempt(s) without retrying, because retrying "
            f"into a block is what turns it into a lockout"
        ),
        remediation=Remediation(steps=BLOCK_REMEDIATION_STEPS),
        scope=Scope.RUN,
        retryable=False,
        origin=("acquire.download",),
        detail={
            "adapter": adapter,
            "key": key,
            "signal": str(signal),
            "attempts": attempts,
            "retry_hint_s": retry_hint_s,
        },
    )


@dataclass(frozen=True, slots=True)
class DownloadRun:
    """One paced acquisition: what landed, and why it stopped if it stopped early.

    ``invocation`` is the contract-shaped report; ``parked`` is the cause, present only
    when the provider refused the client. A parked run never reports a clean
    invocation, which would advance the watermark past tracks it never reached.
    """

    invocation: InvocationResult
    parked: Cause | None = None
    #: Every delay slept, in order, so the pacing is observable on the result.
    schedule: tuple[float, ...] = ()

    def __post_init__(self) -> None:
        if self.parked is None:
            return
        if self.invocation.ok:
            raise ValueError(
                "a parked run reported a clean invocation; a clean invocation "
                "advances the watermark, and advancing it across a provider block "
                "silently skips everything the run never reached"
            )
        if self.parked.retryable:
            raise ValueError(
                "a parked run carries a retryable cause; the whole distinction "
                "this unit draws is that a block is not retried, and an engine "
                "reads that field rather than the message"
            )

    @property
    def ok(self) -> bool:
        return self.parked is None and self.invocation.ok


# ---------------------------------------------------------------------------
# Observing a refusal without changing it
# ---------------------------------------------------------------------------


class _SignalProbe:
    """A ``TrackSource`` wrapper that watches for pacing signals and re-raises.

    It sees the live exception, retry hint included, before the per-track step turns
    it into a result, and re-raises it unchanged. One probe per attempt, so nothing
    is shared.
    """

    __slots__ = ("_clock", "_inner", "retry_hint", "signal")

    def __init__(self, inner: TrackSource, *, clock: Callable[[], datetime]) -> None:
        self._inner = inner
        self._clock = clock
        self.signal = ProviderSignal.NONE
        self.retry_hint: float | None = None

    def authenticate(self) -> None:
        self._inner.authenticate()

    def offer(self, request: TrackRequest):
        try:
            return self._inner.offer(request)
        except BaseException as exc:
            self._observe(exc)
            raise

    def fetch(self, request: TrackRequest, destination):
        try:
            return self._inner.fetch(request, destination)
        except BaseException as exc:
            self._observe(exc)
            raise

    def _observe(self, exc: BaseException) -> None:
        signal = classify_signal(exc)
        if signal in INERT_SIGNALS:
            return
        self.signal = signal
        self.retry_hint = retry_hint_seconds(exc, now=self._clock())


# ---------------------------------------------------------------------------
# The bounded pool
# ---------------------------------------------------------------------------


@dataclass
class _Run:
    """Mutable state shared by the workers of one acquisition."""

    adapter: str
    source: TrackSource
    settings: AdapterSettings
    pacing: Pacing
    sleep: Callable[[float], None]
    rng: random.Random
    clock: Callable[[], datetime]
    gate: threading.Semaphore
    stop: threading.Event = field(default_factory=threading.Event)
    lock: threading.Lock = field(default_factory=threading.Lock)
    parked: Cause | None = None
    failure: tuple[InvocationOutcome, str, Remedy] | None = None
    slept: list[float] = field(default_factory=list)


def _rest(run: _Run, seconds: float) -> None:
    """Sleep, and record what was slept, under one lock."""
    if seconds <= 0:
        return
    with run.lock:
        run.slept.append(seconds)
    run.sleep(seconds)


def _draw(run: _Run, seconds: float, *, upward_only: bool = False) -> float:
    """Jitter a delay. ``random.Random`` is shared, so the draw is serialised."""
    with run.lock:
        if upward_only:
            return jitter_up(run.rng, seconds, run.pacing.jitter_fraction)
        return jitter(run.rng, seconds, run.pacing.jitter_fraction)


def _stop_with_park(run: _Run, cause: Cause) -> None:
    """Record the first block and halt the run. Later blocks are the same block."""
    with run.lock:
        if run.parked is None and run.failure is None:
            run.parked = cause
    run.stop.set()


def _stop_with_failure(run: _Run, exc: AdapterAuthFailed | AdapterBroken) -> None:
    """Record the first adapter-level failure and halt; later ones are its consequences."""
    outcome = (
        InvocationOutcome.AUTH_FAILED
        if isinstance(exc, AdapterAuthFailed)
        else InvocationOutcome.ADAPTER_BROKEN
    )
    with run.lock:
        if run.failure is None and run.parked is None:
            run.failure = (outcome, str(exc), exc.remedy)
    run.stop.set()


def _acquire_with_retries(run: _Run, request: TrackRequest) -> TrackResult | None:
    """One track, retried under the pacing policy. None means the run stopped.

    The pacing delay is taken inside the semaphore, so the cap bounds the request
    rate; a backoff waits outside it, so a throttled track idles no slot. Every
    acquisition waits first, so a batch never starts as one burst.
    """
    result: TrackResult | None = None

    for attempt in range(run.pacing.max_attempts):
        if run.stop.is_set():
            return None
        probe = _SignalProbe(run.source, clock=run.clock)
        with run.gate:
            if run.stop.is_set():
                return None
            _rest(run, _draw(run, run.pacing.base_delay_s))
            if run.stop.is_set():
                return None
            try:
                result = acquire_one(probe, request, run.settings)
            except (AdapterAuthFailed, AdapterBroken) as exc:
                _stop_with_failure(run, exc)
                return None

        if probe.signal in STOPPING_SIGNALS:
            _stop_with_park(
                run,
                blocked_cause(
                    adapter=run.adapter,
                    key=request.key,
                    signal=probe.signal,
                    detail=result.detail or str(probe.signal),
                    attempts=attempt + 1,
                    retry_hint_s=probe.retry_hint,
                ),
            )
            return None

        if probe.signal in RETRYING_SIGNALS:
            hint = probe.retry_hint
            if hint is not None and hint > run.pacing.retry_hint_ceiling_s:
                _stop_with_park(
                    run,
                    blocked_cause(
                        adapter=run.adapter,
                        key=request.key,
                        signal=probe.signal,
                        detail=(
                            f"the provider asked for {hint:g}s, beyond this run's "
                            f"{run.pacing.retry_hint_ceiling_s:g}s ceiling, which is a "
                            f"refusal wearing a wait"
                        ),
                        attempts=attempt + 1,
                        retry_hint_s=hint,
                    ),
                )
                return None
            if attempt + 1 < run.pacing.max_attempts:
                if hint is None:
                    _rest(run, _draw(run, backoff_delay(attempt, run.pacing)))
                else:
                    _rest(run, _draw(run, hint, upward_only=True))
                continue

        return result

    return result


def _soften(result: TrackResult) -> TrackResult:
    """Downgrade a permanent unavailability to a transient one.

    A failed invocation may not carry a permanent result, which feeds quarantine;
    after a block the earlier answer cannot be trusted, and re-queueing costs a lookup.
    """
    if result.outcome is not TrackOutcome.UNAVAILABLE_PERMANENT:
        return result
    return TrackResult(
        key=result.key,
        outcome=TrackOutcome.UNAVAILABLE_TRANSIENT,
        detail=(
            f"{result.detail} (reported permanent, but the invocation failed before "
            f"it finished, so it stays re-queueable)"
        ),
        remedy=Remedy.RETRY_LATER,
    )


def acquire_concurrently(
    *,
    adapter: str,
    source: TrackSource,
    requests: Iterable[TrackRequest],
    settings: AdapterSettings,
    pacing: Pacing | None = None,
    alternatives: Sequence[str] = (),
    sleep: Callable[[float], None] = time.sleep,
    rng: random.Random | None = None,
    executor: Executor | None = None,
    clock: Callable[[], datetime] | None = None,
) -> DownloadRun:
    """Acquire every request under a bounded, paced, signal-aware pool.

    The cap is ``settings.concurrency`` (KTD20), also enforced by a semaphore so a
    larger ``executor`` cannot widen it. A fresh ``rng`` per run decorrelates
    concurrent runs (R10).
    """
    ordered = tuple(requests)
    requested = tuple(request.key for request in ordered)
    resolved = pacing or Pacing.from_settings(settings)

    run = _Run(
        adapter=adapter,
        source=source,
        settings=settings,
        pacing=resolved,
        sleep=sleep,
        rng=rng if rng is not None else random.Random(),
        clock=clock or (lambda: datetime.now(timezone.utc)),
        gate=threading.Semaphore(settings.concurrency),
    )

    try:
        source.authenticate()
    except (AdapterAuthFailed, AdapterBroken) as exc:
        return DownloadRun(
            invocation=_failed(adapter, exc, requested, alternatives),
        )

    slots: list[TrackResult | None] = [None] * len(ordered)

    def work(index: int) -> None:
        slots[index] = _acquire_with_retries(run, ordered[index])

    if ordered:
        owned = executor is None
        pool = executor or ThreadPoolExecutor(
            max_workers=max(1, min(settings.concurrency, len(ordered))),
            thread_name_prefix="cratekit-acquire",
        )
        try:
            list(pool.map(work, range(len(ordered))))
        finally:
            if owned:
                pool.shutdown(wait=True)

    outcome = InvocationOutcome.OK
    detail = ""
    remedy: Remedy | None = None
    if run.failure is not None:
        outcome, detail, remedy = run.failure
    elif run.parked is not None:
        # ADAPTER_BROKEN advances no watermark, quarantines nothing and keeps the rest
        # queued, as a block needs; the parked cause says why.
        outcome = InvocationOutcome.ADAPTER_BROKEN
        detail = run.parked.message
        remedy = Remedy.PAUSE_AND_CHECK_ACCOUNT

    landed = [r for r in slots if r is not None]
    if outcome is not InvocationOutcome.OK:
        landed = [_soften(r) for r in landed]

    return DownloadRun(
        invocation=InvocationResult(
            adapter=adapter,
            outcome=outcome,
            results=tuple(landed),
            requested=requested,
            detail=detail,
            remedy=remedy,
            alternatives=tuple(alternatives),
        ),
        parked=run.parked,
        schedule=tuple(run.slept),
    )


def _failed(
    adapter: str,
    exc: AdapterAuthFailed | AdapterBroken,
    requested: Sequence[str],
    alternatives: Sequence[str],
) -> InvocationResult:
    """Shape an adapter-level failure exactly as the sequential loop does."""
    outcome = (
        InvocationOutcome.AUTH_FAILED
        if isinstance(exc, AdapterAuthFailed)
        else InvocationOutcome.ADAPTER_BROKEN
    )
    return InvocationResult(
        adapter=adapter,
        outcome=outcome,
        requested=tuple(requested),
        detail=str(exc),
        remedy=exc.remedy,
        alternatives=tuple(alternatives),
    )


def acquire_paced(adapter: BaseAdapter, requests: Iterable[TrackRequest], **options) -> DownloadRun:
    """Drive a built adapter through the pool, credential live only for the run.

    The credential is the adapter's session scope, the drive's inside a download job
    (U274). It uses ``BaseAdapter``'s private hooks on purpose, as the paced
    replacement for ``BaseAdapter.acquire``'s loop, so the credential rule lives once.
    """
    ordered = tuple(requests)
    alternatives = adapter._alternatives()
    try:
        with adapter._session_scope() as scope:
            source = adapter._injected if adapter._injected is not None else adapter._source(scope)
            return acquire_concurrently(
                adapter=adapter.name,
                source=source,
                requests=ordered,
                settings=adapter.settings,
                alternatives=alternatives,
                **options,
            )
    except (AdapterAuthFailed, AdapterBroken) as exc:
        return DownloadRun(
            invocation=_failed(
                adapter.name, exc, [request.key for request in ordered], alternatives
            )
        )


__all__ = [
    "BLOCKED_STATUSES", "BLOCK_MARKERS", "BLOCK_REMEDIATION_STEPS", "DEFAULT_BASE_DELAY_S",
    "DEFAULT_JITTER_FRACTION", "INERT_SIGNALS", "MIN_DECORRELATING_JITTER", "RATE_LIMIT_MARKERS",
    "RATE_LIMIT_STATUSES", "RETRYING_SIGNALS", "STOPPING_SIGNALS", "DownloadRun", "Pacing",
    "ProviderSignal", "acquire_concurrently", "acquire_paced", "backoff_delay", "blocked_cause",
    "classify_signal", "jitter", "jitter_up", "retry_hint_seconds", "status_of",
]
