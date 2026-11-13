"""U15: bounded-concurrency acquisition that paces itself and knows when to stop.

WHY THIS EXISTS. The system Cratekit replaces downloads one track at a time, and
it arranges that by shelling out to the wrapped tool before every run to write a
concurrency of one and a three-to-nine second gap into that tool's own global
``settings.json``. Two things are wrong with it and this unit fixes both.

* The cap is not configurable, it is a constant buried in a subprocess call, and
  the file it writes to is shared with every other process using that tool. Two
  racing pacing writes and a kill landing mid-write have each reset that file to
  factory defaults, which are lossy audio into the tool's own directory. KTD20
  moved those settings into the adapter for exactly that reason, so the cap this
  module reads is ``AdapterSettings.concurrency`` and there is no second one.
* Every provider refusal is treated the same. The source retries any exception
  with capped exponential backoff, so a rate limit and a ban get the identical
  response, and the response to a ban is the one thing that makes it worse.

THE DISTINCTION THAT IS THE WHOLE UNIT. A throttle says "slower". A ban says
"stop". Retrying into a ban is what turns a throttle into a lockout, and a
lockout on a music provider is not a failed run, it is an account the user may
not get back. So:

* A rate-limit signal honours the provider's own retry hint when it gave one, or
  backs off exponentially, and keeps trying.
* A forbidden response or a bot challenge stops the ENTIRE run at once, parks it
  with a structured cause, and never makes a second request.

Two asymmetries follow from that, and both are deliberate:

1. When the evidence is mixed, BLOCKED wins over RATE_LIMITED. A false stop
   costs a re-run. A false retry costs the account. This mirrors the asymmetry
   ``adapter.TRANSIENT_MARKERS`` already uses: the reading whose mistake is
   unrecoverable is checked first.
2. A provider retry hint is jittered UPWARD only. Symmetric jitter on an explicit
   hint can return early, which is precisely the request the provider just asked
   us not to make.

WHY JITTER IS WIDE BY DEFAULT. Two runs started by the same person, or one run
whose workers all backed off from the same rate limit, re-converge on the same
schedule if the delay is fixed. They then arrive together, trip the limiter
together, and back off together: a retry storm built out of politeness. The
default width reproduces the source system's own proven window, which is three to
nine seconds around a six second nominal, and that window is a fifty percent
spread. It is expressed here as a fraction of the nominal rather than as a pair
of endpoints so that it stays a fifty percent spread when the nominal changes.

WHERE THE JOB ENGINE FITS. "Parks the job" is not something this module does. It
returns the structured cause a job engine parks ON, because the acquisition layer
sits below the engine and a module that reached up to park itself would be the
layering violation KTD23 exists to forbid. ``DownloadRun.parked`` is that seam:
a ``Cause`` that is non-retryable by construction and round-trips through JSON,
which is what KTD26's subprocess boundary requires of anything a job stores.

Layer note: MODULES. It may read the adapter's settings; it reads no config file
and names no verb.
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

#: Status codes the provider uses to say "too fast". Read from the response
#: object when there is one, because a machine-readable status beats prose that
#: happens to contain a number.
RATE_LIMIT_STATUSES = frozenset({429})

#: Status codes that mean the client, not the request, was refused. 403 is the
#: whole set on purpose. 401 is authentication and is already the adapter's
#: ``AdapterAuthFailed``; folding it in here would send a user with an expired
#: session to a remedy about their account standing.
BLOCKED_STATUSES = frozenset({403})

#: Phrases that mean a bot wall, a challenge, or a refusal of the client. Checked
#: BEFORE the rate-limit phrases: a bot wall commonly explains itself in the
#: language of rate limiting, and reading a wall as a limit is the mistake that
#: costs the account.
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

# Numeric statuses appearing in free text, matched on word boundaries. A bare
# substring search for "403" also matches a track identifier such as 40312, and a
# guard that stops a correct run on a coincidence is a guard someone will disable
# (P7). The boundary is what keeps the numeric evidence honest.
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

#: Attribute chains a client library might expose a status through. Ordered, and
#: the first one present wins. Written as a table rather than as a chain of
#: getattr calls so a fourth client shape is one line rather than a new branch.
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
    """The HTTP status a provider exception carries, if it carries one at all.

    Returns None rather than guessing. A guessed status feeds the classifier
    below, and the classifier decides whether to keep asking a provider that may
    have just refused us.
    """
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

    Precedence, and the reason for each step:

    1. **A structured status decides.** It is the provider's own machine-readable
       answer, and a 429 body routinely contains prose about what is forbidden.
       A status that says 429 while the body says "forbidden" is a throttle whose
       explanation is badly worded, not a ban.
    2. **Failing that, block phrases beat rate-limit phrases.** A bot wall
       frequently describes itself as a rate limit, and this is the direction
       where being wrong is unrecoverable.
    3. **Failing both, no signal.** Silence here does not mean the request
       succeeded; it means nothing about PACING was said, and the per-track
       classifier in the contract still has its own answer.

    A ``NoFileLanded`` says nothing about pacing, before any reading. Its text
    quotes what the downloader swallowed for a person to read (R-703), a
    track title or a tool message among it, and one "forbidden" there would
    stop every worker and park the run as an account block. The provider gate
    already counted any rate limit answer behind it at the transport.
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


#: Read one header without assuming the container preserves case. The parser
#: lives in ``core.provider_gate`` since R-705, because the gate reads the same
#: header off the raw response and two parsers of one header can disagree.
_header = provider_gate.header_value


def _as_seconds(value: object, now: datetime) -> float | None:
    """Coerce a retry hint to seconds, accepting both forms the header allows.

    Delegates to the ONE parser of ``Retry-After`` in the tree, the gate's,
    with this module's datetime reference turned into the epoch it reads.
    """
    return provider_gate.retry_after_seconds(value, now.timestamp())


def retry_hint_seconds(exc: BaseException, *, now: datetime | None = None) -> float | None:
    """How long the provider asked us to wait, or None if it did not say.

    Three sources in order: an attribute a client library set, the response
    header, then the exception's own text. The text form is last because it is
    the least reliable, but it is present because several clients stringify the
    header into the message and expose nothing else.
    """
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

#: The gap between acquisitions when configuration leaves it unset. Six seconds
#: with the default jitter fraction reproduces the three-to-nine second window
#: the source system settled on after tripping the provider's alarms with
#: anything faster. It is a DEFAULT, not a second configuration point: config
#: declares ``acquisition.pacing_delay_s`` and documents None as meaning "the
#: adapter's own default", which is this value.
DEFAULT_BASE_DELAY_S = 6.0

#: Half the nominal, either way, so a six second delay lands in [3, 9]. Wide
#: enough that two runs drawing independently do not stay in step for long, which
#: is the property that stops a shared rate limit from producing a shared retry.
DEFAULT_JITTER_FRACTION = 0.5

#: Below this width, two runs that started together stay together long enough to
#: arrive as a burst. Asserted rather than assumed, so lowering the default is a
#: decision somebody has to make deliberately.
MIN_DECORRELATING_JITTER = 0.25


@dataclass(frozen=True, slots=True)
class Pacing:
    """How this run waits: between acquisitions, and after being told to slow down.

    Held apart from ``AdapterSettings`` because these are MECHANISM. The cap and
    the nominal delay are the two things a user actually turns, and both live in
    the adapter's settings where KTD20 put them. Everything here is the shape of
    the waiting, which has one correct answer and no reason to be in a config
    file where it could be set to zero by somebody debugging.
    """

    base_delay_s: float = DEFAULT_BASE_DELAY_S
    jitter_fraction: float = DEFAULT_JITTER_FRACTION
    backoff_base_s: float = 1.0
    backoff_max_s: float = 300.0
    #: Total tries per track, first attempt included.
    max_attempts: int = 5
    #: A hint longer than this is treated as a stop rather than a wait. A
    #: provider that asks for a day has effectively refused us, and honouring it
    #: by sleeping is indistinguishable from a hung process; honouring it by
    #: truncating it is the early retry the hint existed to prevent. Parking is
    #: the only answer that is neither.
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

        ``pacing_delay_s`` is deliberately read with ``is None`` rather than with
        a falsy test. The two are different answers: None means the user left it
        to the adapter and gets the default above, while an explicit 0.0 means
        the user turned pacing off and gets exactly that. A falsy test collapses
        them and silently overrides a decision the user made.
        """
        delay = settings.pacing_delay_s
        base = DEFAULT_BASE_DELAY_S if delay is None else float(delay)
        return cls(base_delay_s=base, **overrides)  # type: ignore[arg-type]


def backoff_delay(retry_index: int, pacing: Pacing) -> float:
    """The un-jittered exponential wait before retry number ``retry_index``.

    Pure and separate from the jitter so both halves can be asserted on their
    own: that the sequence doubles and that it stops doubling at the ceiling.
    """
    if retry_index < 0:
        raise ValueError("a retry index counts from zero")
    return min(pacing.backoff_max_s, pacing.backoff_base_s * (2.0**retry_index))


def jitter(rng: random.Random, seconds: float, fraction: float) -> float:
    """Spread a delay symmetrically around its nominal value."""
    if seconds <= 0 or fraction <= 0:
        return max(0.0, seconds)
    return max(0.0, seconds * rng.uniform(1.0 - fraction, 1.0 + fraction))


def jitter_up(rng: random.Random, seconds: float, fraction: float) -> float:
    """Spread a delay upward only, never below its nominal value.

    Used for a wait the PROVIDER named. Symmetric jitter on an explicit hint can
    return before the provider asked, which is the request it just told us not to
    make; the decorrelation is still needed, so it is taken entirely from the
    late side.
    """
    if seconds <= 0 or fraction <= 0:
        return max(0.0, seconds)
    return seconds * rng.uniform(1.0, 1.0 + fraction)


# ---------------------------------------------------------------------------
# The parked cause: the seam the job engine consumes
# ---------------------------------------------------------------------------

#: What a person does about a provider block. Sentences rather than commands,
#: because none of this is a command: D2 keeps command text in the CLI layer, and
#: ``Remediation.steps`` exists for a fix that is not a command at all.
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

    ``retryable`` is False and that is the load-bearing field. An engine deciding
    whether to re-run reads it rather than the exit code, because the exit code's
    class remediation for anything upstream is "retry later" and this is the one
    member of that class where an automatic retry is the harm.

    ``scope`` is RUN rather than ITEM. A block is a fact about the client, not
    about the track that happened to be in flight when it arrived, so no
    watermark may advance for any source in this run.
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

    Two fields rather than one because they answer different questions and a
    caller needs both. ``invocation`` is the contract-shaped report every other
    acquisition path already produces, so the sync layer's watermark and
    quarantine decisions are unchanged. ``parked`` is the reason a job engine
    parks on, present only when the provider refused the client outright.

    The invariant below is the unit's own claim stated as a type. A run that was
    blocked must never report a clean invocation, because a clean invocation
    advances the source's watermark, and a watermark advanced across a block
    skips every track the run never reached.
    """

    invocation: InvocationResult
    parked: Cause | None = None
    #: Every delay actually slept, in the order the sleeps happened. Carried so
    #: the decorrelation property is observable on the result rather than only by
    #: patching the clock, and so an operator can see what a run spent waiting.
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

    The contract's per-track step turns an exception into a classified result, so
    by the time a caller sees the result the exception object, its response, and
    its headers are gone. Reconstructing a rate limit from the message text alone
    would lose the retry hint, which is the one piece of information the provider
    volunteered.

    So this observes at the only point where the live exception exists and then
    re-raises it UNCHANGED. Nothing about the per-track classification moves. One
    probe is constructed per attempt, which is what keeps it free of shared state
    under concurrency: there is no lock here because there is nothing to share.
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
    """Record an adapter-level failure and halt, matching the sequential loop.

    First writer wins for the same reason the sequential loop returns on the
    first one: after the session dies, every other worker's failure is a
    consequence rather than a second cause, and reporting the consequence sends
    the user to the wrong remedy.
    """
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

    The pacing delay is taken INSIDE the semaphore and the backoff OUTSIDE it,
    and the difference is the point of each. The pacing delay is what bounds the
    request RATE, so it has to occupy a slot or the cap would bound only the
    moment of the call. A backoff is a track waiting its turn again, so holding a
    slot through it would let one rate-limited track idle capacity that other
    tracks could use.

    Unlike the sequential loop, EVERY acquisition waits first, including the
    first one. At a cap above one, skipping the first delay would send the whole
    first batch at the same instant, which is the synchronised burst the pacing
    exists to prevent. At a cap of one it costs a single extra delay per run.
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

    Applied to every result of a FAILED invocation, and required rather than
    tidy: ``InvocationResult`` refuses to carry a permanent result under a failed
    outcome, because permanent feeds quarantine and quarantine is never
    re-queued. A run that classified one track as delisted and was then blocked
    has no way to know the first answer was honest, since a bot wall answers
    with whatever status it likes. Keeping the track re-queueable costs one
    lookup on the next run. Getting it wrong costs the track forever.
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

    The cap is ``settings.concurrency`` and is read from there rather than
    declared here, so there is exactly one place it is configured (KTD20). A
    semaphore enforces it in addition to the pool's own worker count, because the
    pool is replaceable through ``executor`` while the invariant is not: a caller
    handing in a larger pool must not thereby widen the cap.

    ``rng`` defaults to a fresh generator per run. That is what makes two
    concurrent runs draw different schedules without either knowing the other
    exists, which is the decorrelation R10 asks for.
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
        # ADAPTER_BROKEN is the only invocation outcome that gives a block the
        # three behaviours it needs: no watermark advances, nothing is
        # quarantined, and everything that did not land stays queued. What it
        # cannot express is WHY, which is what the parked cause carries.
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

    The run's credential is the adapter's own session scope. Inside a drive of
    a download job the vendored adapter's scope is the drive's (U274), so the
    session outlives this call and is erased when the drive closes.

    This reaches into ``BaseAdapter``'s session scope and source hooks on
    purpose. ``download`` is part of the adapter framework rather than a client
    of it: it is the paced replacement for the sequential loop that
    ``BaseAdapter.acquire`` calls, so it needs the same two hooks that loop is
    given. Re-implementing the credential scope here instead would be a second
    place where "no plaintext token survives a run" has to be remembered.
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
    "BLOCKED_STATUSES",
    "BLOCK_MARKERS",
    "BLOCK_REMEDIATION_STEPS",
    "DEFAULT_BASE_DELAY_S",
    "DEFAULT_JITTER_FRACTION",
    "INERT_SIGNALS",
    "MIN_DECORRELATING_JITTER",
    "RATE_LIMIT_MARKERS",
    "RATE_LIMIT_STATUSES",
    "RETRYING_SIGNALS",
    "STOPPING_SIGNALS",
    "DownloadRun",
    "Pacing",
    "ProviderSignal",
    "acquire_concurrently",
    "acquire_paced",
    "backoff_delay",
    "blocked_cause",
    "classify_signal",
    "jitter",
    "jitter_up",
    "retry_hint_seconds",
    "status_of",
]
