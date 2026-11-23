"""U15: the cap holds, the throttle is waited out, and the ban is never retried.

Every source is a double and every sleep is recorded, so the suite asserts on the
SCHEDULE a run would have slept.
"""

from __future__ import annotations

import ast
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.acquire.adapter import (
    AdapterAuthFailed,
    AdapterBroken,
    AdapterSettings,
    BaseAdapter,
    InvocationOutcome,
    InvocationResult,
    LosslessPolicy,
    Offer,
    Remedy,
    TrackOutcome,
    TrackRequest,
    TrackResult,
)
from cratekit.acquire.download import (
    BLOCK_MARKERS,
    BLOCK_REMEDIATION_STEPS,
    DEFAULT_BASE_DELAY_S,
    DEFAULT_JITTER_FRACTION,
    INERT_SIGNALS,
    MIN_DECORRELATING_JITTER,
    RATE_LIMIT_MARKERS,
    RETRYING_SIGNALS,
    STOPPING_SIGNALS,
    DownloadRun,
    Pacing,
    ProviderSignal,
    acquire_concurrently,
    acquire_paced,
    backoff_delay,
    blocked_cause,
    classify_signal,
    jitter,
    jitter_up,
    retry_hint_seconds,
    status_of,
)
from cratekit.core import config
from cratekit.core.cause import REASONS, Cause, Scope

REPO_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_SOURCE = REPO_ROOT / "src" / "cratekit" / "acquire" / "download.py"

FIXED_NOW = datetime(2026, 8, 1, 12, 0, 0, tzinfo=timezone.utc)



class Response:
    """The minimum of a client's response object: a status and some headers."""

    def __init__(self, status_code: int, headers: dict[str, str] | None = None) -> None:
        self.status_code = status_code
        self.headers = headers or {}


class ProviderError(Exception):
    """A provider client's exception, optionally carrying a response."""

    def __init__(self, message: str, response: Response | None = None) -> None:
        super().__init__(message)
        self.response = response


def rate_limited(message: str = "429 Too Many Requests", **kw) -> ProviderError:
    return ProviderError(message, Response(429, kw.get("headers")))


def blocked(message: str = "403 Forbidden") -> ProviderError:
    return ProviderError(message, Response(403))


@dataclass
class Instrumented:
    """A ``TrackSource`` recording concurrency (``peak``) and replaying a per key script."""

    script: dict[str, list[object]] = field(default_factory=dict)
    lossless: bool = True
    hold: float = 0.0

    live: int = 0
    peak: int = 0
    attempts: list[str] = field(default_factory=list)
    authenticated: int = 0
    auth_error: BaseException | None = None
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _barrier: threading.Event = field(default_factory=threading.Event)

    def authenticate(self) -> None:
        with self._lock:
            self.authenticated += 1
        if self.auth_error is not None:
            raise self.auth_error

    def offer(self, request: TrackRequest) -> Offer:
        return Offer(lossless=self.lossless)

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        with self._lock:
            self.attempts.append(request.key)
            index = self.attempts.count(request.key) - 1
            self.live += 1
            self.peak = max(self.peak, self.live)
        try:
            if self.hold:
                self._barrier.wait(timeout=self.hold)
            steps = self.script.get(request.key, [])
            outcome = steps[index] if index < len(steps) else None
            if isinstance(outcome, BaseException):
                raise outcome
            landed = destination / f"{request.key}.flac"
            landed.parent.mkdir(parents=True, exist_ok=True)
            landed.write_bytes(b"")
            return landed
        finally:
            with self._lock:
                self.live -= 1

    def release(self) -> None:
        self._barrier.set()


@dataclass
class Recorder:
    """A sleep that records instead of sleeping."""

    slept: list[float] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def __call__(self, seconds: float) -> None:
        with self._lock:
            self.slept.append(seconds)


@pytest.fixture
def settings(tmp_path) -> AdapterSettings:
    staging = tmp_path / "staging"
    staging.mkdir()
    return AdapterSettings(download_staging=staging)


def requests_for(*keys: str) -> tuple[TrackRequest, ...]:
    return tuple(TrackRequest(key=key) for key in keys)


def run_pool(source, settings, *, pacing=None, sleep=None, **kw) -> DownloadRun:
    """Drive the pool with pacing off unless a test passes its own ``Pacing``."""
    return acquire_concurrently(
        adapter="fake", source=source, settings=settings, pacing=pacing or Pacing(base_delay_s=0.0),
        sleep=sleep or Recorder(), clock=lambda: FIXED_NOW, **kw,
    )



def test_every_signal_is_classified_as_retrying_stopping_or_inert():
    """Derived, not enumerated (P4): a new signal with no set would fall into the retry branch."""
    covered = RETRYING_SIGNALS | STOPPING_SIGNALS | INERT_SIGNALS
    assert covered == set(ProviderSignal)
    assert not (RETRYING_SIGNALS & STOPPING_SIGNALS)


def test_a_structured_rate_limit_status_reads_as_a_throttle():
    assert classify_signal(rate_limited()) is ProviderSignal.RATE_LIMITED


def test_a_structured_forbidden_status_reads_as_a_block():
    assert classify_signal(blocked()) is ProviderSignal.BLOCKED


def test_an_unrelated_status_carries_no_pacing_instruction():
    """A 503 is the contract's transient case and says nothing about pace."""
    assert classify_signal(ProviderError("boom", Response(503))) is ProviderSignal.NONE


@pytest.mark.parametrize("marker", BLOCK_MARKERS)
def test_every_block_phrase_stops_the_run(marker):
    assert classify_signal(ProviderError(f"provider said: {marker}")) is ProviderSignal.BLOCKED


@pytest.mark.parametrize("marker", RATE_LIMIT_MARKERS)
def test_every_rate_limit_phrase_only_slows_the_run(marker):
    assert classify_signal(ProviderError(f"provider said: {marker}")) is ProviderSignal.RATE_LIMITED


def test_a_bot_wall_describing_itself_as_a_rate_limit_still_stops():
    """A bot wall reads as rate limiting; retrying into a block cannot recover, so block wins."""
    exc = ProviderError("Access denied: rate limit exceeded for this client")
    assert classify_signal(exc) is ProviderSignal.BLOCKED


def test_a_status_beats_prose_that_merely_mentions_a_refusal():
    """The status is the machine-readable answer; body prose must not override it."""
    exc = rate_limited("429: this request is forbidden until you slow down")
    assert classify_signal(exc) is ProviderSignal.RATE_LIMITED


def test_a_number_that_merely_contains_a_status_is_not_a_status():
    """P7: key 40312 must not read as a forbidden response; word boundaries are needed."""
    assert classify_signal(ProviderError("track 40312 could not be read")) is ProviderSignal.NONE
    assert classify_signal(ProviderError("track 4291 could not be read")) is ProviderSignal.NONE


def test_the_status_is_read_from_whichever_attribute_the_client_exposes():
    class Flat(Exception):
        status = 429

    assert status_of(Flat()) == 429
    assert status_of(ProviderError("x", Response(403))) == 403
    assert status_of(ProviderError("no response")) is None



@pytest.mark.parametrize(
    "name,value,seconds",
    [("Retry-After", "45", 45.0), ("retry-after", "20", 20.0)],
    ids=["delta-seconds-honoured", "found-whatever-case-the-client-stored"],
)
def test_a_delta_seconds_header_is_honoured_whatever_its_case(name, value, seconds):
    """Header names match case insensitively, as a client library's dictionary does."""
    exc = rate_limited(headers={name: value})
    assert retry_hint_seconds(exc, now=FIXED_NOW) == seconds


def test_a_date_form_header_is_parsed_rather_than_dropped():
    when = FIXED_NOW + timedelta(minutes=30)
    stamp = when.strftime("%a, %d %b %Y %H:%M:%S GMT")
    exc = rate_limited(headers={"Retry-After": stamp})
    assert retry_hint_seconds(exc, now=FIXED_NOW) == pytest.approx(1800.0, abs=1.0)


def test_a_date_already_in_the_past_is_no_wait_at_all():
    stamp = (FIXED_NOW - timedelta(minutes=5)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    exc = rate_limited(headers={"Retry-After": stamp})
    assert retry_hint_seconds(exc, now=FIXED_NOW) == 0.0


def test_an_attribute_beats_a_header_and_a_header_beats_the_message():
    class WithAttribute(Exception):
        retry_after = 7

    assert retry_hint_seconds(WithAttribute(), now=FIXED_NOW) == 7.0
    assert retry_hint_seconds(ProviderError("Retry-After: 12"), now=FIXED_NOW) == 12.0
    assert retry_hint_seconds(ProviderError("try again in 90 seconds"), now=FIXED_NOW) == 90.0


def test_no_hint_at_all_reads_as_no_hint_rather_than_as_zero():
    """Zero would mean "retry immediately", which is the opposite instruction."""
    assert retry_hint_seconds(ProviderError("429 too many requests")) is None
    assert retry_hint_seconds(ProviderError("nonsense"), now=FIXED_NOW) is None


def test_a_nonsense_header_is_ignored_rather_than_guessed_at():
    exc = rate_limited(headers={"Retry-After": "soon"})
    assert retry_hint_seconds(exc, now=FIXED_NOW) is None



def test_the_default_window_reproduces_the_proven_one():
    """Six seconds at fifty percent spread is the source system's [3, 9]."""
    rng = random.Random(0)
    draws = [jitter(rng, DEFAULT_BASE_DELAY_S, DEFAULT_JITTER_FRACTION) for _ in range(2000)]
    assert min(draws) >= 3.0
    assert max(draws) <= 9.0
    assert max(draws) - min(draws) > 5.0


def test_the_default_jitter_is_wide_enough_to_decorrelate():
    assert DEFAULT_JITTER_FRACTION >= MIN_DECORRELATING_JITTER


def test_backoff_doubles_and_then_stops_at_its_ceiling():
    pacing = Pacing(backoff_base_s=1.0, backoff_max_s=8.0)
    assert [backoff_delay(i, pacing) for i in range(6)] == [1.0, 2.0, 4.0, 8.0, 8.0, 8.0]


def test_a_provider_hint_is_jittered_upward_only():
    """Symmetric jitter on an explicit hint must not return before the provider asked."""
    rng = random.Random(1)
    draws = [jitter_up(rng, 30.0, 0.5) for _ in range(500)]
    assert min(draws) >= 30.0
    assert max(draws) <= 45.0


def test_an_unset_delay_and_an_explicit_zero_are_different_answers(settings):
    """None means "the adapter decides"; 0.0 means pacing was turned off and stays off."""
    assert Pacing.from_settings(settings).base_delay_s == DEFAULT_BASE_DELAY_S
    off = AdapterSettings(download_staging=settings.download_staging, pacing_delay_s=0.0)
    assert Pacing.from_settings(off).base_delay_s == 0.0


def test_a_pacing_policy_refuses_values_that_cannot_mean_anything():
    with pytest.raises(ValueError, match="between 0 and 1"):
        Pacing(jitter_fraction=1.5)
    with pytest.raises(ValueError, match="attempted at least once"):
        Pacing(max_attempts=0)
    with pytest.raises(ValueError, match="ceiling cannot be below"):
        Pacing(backoff_base_s=10.0, backoff_max_s=1.0)
    with pytest.raises(ValueError, match="cannot be negative"):
        Pacing(base_delay_s=-1.0)



@pytest.mark.parametrize("cap", [1, 2, 3])
def test_the_cap_bounds_simultaneous_acquisitions(tmp_path, cap):
    """Observed on the double: a barrier forces overlap, so no cap shows a peak of eight."""
    staging = tmp_path / "staging"
    staging.mkdir()
    settings = AdapterSettings(download_staging=staging, concurrency=cap)
    source = Instrumented(hold=0.05)
    keys = tuple(f"t{i}" for i in range(8))

    timer = threading.Timer(0.4, source.release)
    timer.start()
    try:
        run = run_pool(source, settings, requests=requests_for(*keys))
    finally:
        timer.cancel()
        source.release()

    assert source.peak <= cap
    assert run.invocation.outcome is InvocationOutcome.OK
    assert len(run.invocation.acquired()) == len(keys)


def test_an_injected_pool_cannot_widen_the_cap(tmp_path):
    """The semaphore is the invariant: a shared executor must not raise the cap."""
    staging = tmp_path / "staging"
    staging.mkdir()
    settings = AdapterSettings(download_staging=staging, concurrency=2)
    source = Instrumented(hold=0.05)
    timer = threading.Timer(0.4, source.release)
    timer.start()
    with ThreadPoolExecutor(max_workers=8) as pool:
        try:
            run_pool(source, settings, requests=requests_for(*[f"t{i}" for i in range(8)]),
                     executor=pool)
        finally:
            timer.cancel()
            source.release()
    assert source.peak <= 2


def test_results_come_back_in_request_order_whatever_order_they_finished_in(settings):
    keys = tuple(f"t{i}" for i in range(6))
    paced = AdapterSettings(download_staging=settings.download_staging, concurrency=4)
    run = run_pool(Instrumented(), paced, requests=requests_for(*keys))
    assert tuple(r.key for r in run.invocation.results) == keys


def _config_dict(tmp_path, **acquisition):
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True, exist_ok=True)
    return {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(library), "volume_id": "F1E2-D3C4",
            "db_path": str(library / "db" / "master.db"),
        },
        "paths": {"download_staging": str(tmp_path / "staging")}, "profile": {"name": "slim"},
        "acquisition": acquisition,
    }


def test_the_configured_cap_travels_from_config_into_the_adapter_settings(tmp_path, monkeypatch):
    """R10's "configurable" half, through the real loader so the key is READ out of a file."""
    data = _config_dict(tmp_path, concurrency=4, pacing_delay_s=2.0)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, data["library"]["root"])
    built = AdapterSettings.from_config(config.from_dict(data))
    assert built.concurrency == 4
    assert Pacing.from_settings(built).base_delay_s == 2.0


def test_the_shipped_default_cap_is_one_so_nothing_speeds_up_by_upgrading(tmp_path, monkeypatch):
    """R10 makes the cap configurable, not faster by default."""
    data = _config_dict(tmp_path)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, data["library"]["root"])
    assert AdapterSettings.from_config(config.from_dict(data)).concurrency == 1


@pytest.mark.parametrize("bad", [0, -1, "two", True])
def test_configuration_refuses_a_cap_that_would_acquire_nothing(tmp_path, bad):
    problems = config.validate(_config_dict(tmp_path, concurrency=bad))
    assert any("acquisition.concurrency" in problem for problem in problems), problems



def test_a_rate_limit_backs_off_and_eventually_succeeds(settings):
    sleeps = Recorder()
    source = Instrumented(script={"t": [rate_limited(), rate_limited()]})
    run = run_pool(
        source, settings, requests=requests_for("t"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0, backoff_base_s=1.0), sleep=sleeps,
    )

    assert run.ok
    assert run.invocation.results[0].outcome is TrackOutcome.ACQUIRED
    assert source.attempts == ["t", "t", "t"]
    assert sleeps.slept == [1.0, 2.0]


def test_the_providers_own_retry_hint_replaces_our_backoff(settings):
    """Honouring the hint is the difference between polite and merely persistent."""
    sleeps = Recorder()
    source = Instrumented(script={"t": [rate_limited(headers={"Retry-After": "40"})]})
    run = run_pool(
        source, settings, requests=requests_for("t"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0, backoff_base_s=1.0), sleep=sleeps,
    )
    assert run.ok
    assert sleeps.slept == [40.0]


def test_exhausting_the_attempts_leaves_the_track_requeueable(settings):
    """A throttle that never lifts is transient: permanent feeds quarantine, never re-queued."""
    source = Instrumented(script={"t": [rate_limited()] * 10})
    run = run_pool(
        source, settings, requests=requests_for("t"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0, max_attempts=3),
    )
    assert source.attempts == ["t", "t", "t"]
    assert run.invocation.results[0].outcome is TrackOutcome.UNAVAILABLE_TRANSIENT
    assert run.invocation.requeue_keys() == ("t",)
    assert run.invocation.quarantine_keys() == ()


def test_a_pacing_delay_is_taken_before_every_acquisition_including_the_first(settings):
    """At a cap above one, skipping the first delay sends the batch as a burst."""
    sleeps = Recorder()
    paced = AdapterSettings(download_staging=settings.download_staging, concurrency=2)
    run_pool(
        Instrumented(), paced, requests=requests_for("a", "b", "c"),
        pacing=Pacing(base_delay_s=5.0, jitter_fraction=0.0), sleep=sleeps,
    )
    assert sleeps.slept == [5.0, 5.0, 5.0]



def test_a_forbidden_response_stops_immediately_and_does_not_retry(settings):
    sleeps = Recorder()
    source = Instrumented(script={"t": [blocked()] * 10})
    run = run_pool(
        source, settings, requests=requests_for("t"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0, max_attempts=5), sleep=sleeps,
    )

    assert source.attempts == ["t"], "a block was retried; that is the lockout"
    assert sleeps.slept == []
    assert run.parked is not None
    assert run.parked.reason == "provider-blocked"
    assert run.parked.retryable is False
    assert run.ok is False


def test_a_block_halts_the_tracks_that_had_not_started(settings):
    """"Stops immediately" measured across the queue, not just the one track."""
    source = Instrumented(script={"a": [blocked()]})
    keys = tuple(f"k{i}" for i in range(40))
    run = run_pool(
        source, settings, requests=(TrackRequest(key="a"), *requests_for(*keys)),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0),
    )
    assert run.parked is not None
    assert len(source.attempts) < len(keys)


def test_a_blocked_run_never_advances_a_watermark_and_never_quarantines(settings):
    """The three behaviours a block requires, asserted on the shipped result."""
    source = Instrumented(script={"a": [blocked()]})
    run = run_pool(
        source, settings, requests=requests_for("a", "b"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0),
    )
    assert run.invocation.advances_watermark is False
    assert run.invocation.quarantine_keys() == ()
    assert set(run.invocation.requeue_keys()) == {"a", "b"}
    assert run.invocation.remedy is Remedy.PAUSE_AND_CHECK_ACCOUNT


def test_a_permanent_verdict_reached_before_a_block_is_softened(settings):
    """A bot wall answers with any status, so a delisted track before a block stays requeueable."""
    source = Instrumented(script={"gone": [ProviderError("404 not found")], "wall": [blocked()]})
    run = run_pool(
        source, settings, requests=requests_for("gone", "wall"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0),
    )
    assert run.parked is not None
    by_key = {r.key: r for r in run.invocation.results}
    assert by_key["gone"].outcome is TrackOutcome.UNAVAILABLE_TRANSIENT
    assert "re-queueable" in by_key["gone"].detail


def test_a_retry_hint_longer_than_the_ceiling_is_a_refusal_wearing_a_wait(settings):
    """It parks: sleeping looks hung and truncating is the early retry the hint prevents."""
    sleeps = Recorder()
    source = Instrumented(script={"t": [rate_limited(headers={"Retry-After": "86400"})] * 5})
    run = run_pool(
        source, settings, requests=requests_for("t"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0, retry_hint_ceiling_s=900.0),
        sleep=sleeps,
    )
    assert source.attempts == ["t"]
    assert sleeps.slept == []
    assert run.parked is not None
    assert run.parked.detail["retry_hint_s"] == 86400.0


def test_the_parked_cause_is_what_a_job_engine_can_actually_park_on(settings):
    """The U10 seam re-invokes the command line (KTD26), so ``retryable`` survives the JSON."""
    source = Instrumented(script={"t": [blocked()]})
    run = run_pool(
        source, settings, requests=requests_for("t"),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0),
    )
    cause = run.parked
    assert cause is not None
    restored = Cause.from_json(cause.to_json())
    assert restored.reason == "provider-blocked"
    assert restored.retryable is False
    assert restored.scope is Scope.RUN
    assert restored.remediation.steps == BLOCK_REMEDIATION_STEPS
    assert restored.origin == ("acquire.download",)


def test_the_block_reason_is_declared_in_the_closed_registry():
    """S4's rule: a refusal with no reserved code collapses at the process boundary."""
    assert "provider-blocked" in REASONS


def test_a_parked_run_cannot_report_a_clean_invocation():
    """The unit's claim as a type. A clean invocation advances the watermark."""
    clean = InvocationResult(adapter="fake", outcome=InvocationOutcome.OK, requested=("t",))
    with pytest.raises(ValueError, match="advances the watermark"):
        DownloadRun(invocation=clean, parked=blocked_cause(
            adapter="fake", key="t", signal=ProviderSignal.BLOCKED, detail="x", attempts=1,
        ))


def test_a_parked_run_cannot_carry_a_retryable_cause():
    broken = InvocationResult(
        adapter="fake", outcome=InvocationOutcome.ADAPTER_BROKEN, requested=("t",),
        remedy=Remedy.PAUSE_AND_CHECK_ACCOUNT,
    )
    retryable = Cause(
        reason="provider-blocked", message="x",
        remediation=blocked_cause(
            adapter="f", key="t", signal=ProviderSignal.BLOCKED, detail="d", attempts=1
        ).remediation,
        retryable=True,
    )
    with pytest.raises(ValueError, match="retryable cause"):
        DownloadRun(invocation=broken, parked=retryable)



def test_two_concurrent_runs_draw_distinct_schedules(settings):
    """Each run gets its own generator; the jitter width prevents a retry storm."""
    keys = requests_for(*[f"t{i}" for i in range(12)])
    first = run_pool(
        Instrumented(), settings, requests=keys, pacing=Pacing(base_delay_s=DEFAULT_BASE_DELAY_S),
    )
    second = run_pool(
        Instrumented(), settings, requests=keys, pacing=Pacing(base_delay_s=DEFAULT_BASE_DELAY_S),
    )

    assert len(first.schedule) == len(second.schedule) == len(keys)
    assert sorted(first.schedule) != sorted(second.schedule)
    assert len(set(first.schedule)) == len(keys), "one run repeated a delay"


def test_two_runs_backing_off_from_the_same_limit_do_not_wake_together(settings):
    """The storm case: a shared limiter hits both runs at the same instant."""
    schedules = []
    for _ in range(2):
        run = run_pool(
            Instrumented(script={f"t{i}": [rate_limited()] for i in range(8)}), settings,
            requests=requests_for(*[f"t{i}" for i in range(8)]),
            pacing=Pacing(base_delay_s=0.0, backoff_base_s=10.0),
        )
        schedules.append(sorted(run.schedule))
    assert schedules[0] != schedules[1]


def test_a_seeded_generator_makes_a_run_reproducible(settings):
    """Decorrelation is the default; a caller wanting a fixed schedule supplies the generator."""
    keys = requests_for("a", "b", "c")
    pacing = Pacing(base_delay_s=4.0)
    one = run_pool(Instrumented(), settings, requests=keys, pacing=pacing, rng=random.Random(7))
    two = run_pool(Instrumented(), settings, requests=keys, pacing=pacing, rng=random.Random(7))
    assert sorted(one.schedule) == sorted(two.schedule)



def test_a_dead_session_at_authentication_reports_auth_failure_not_missing_tracks(settings):
    """AE9. The report that made the source system's outage look like an empty catalogue."""
    source = Instrumented(auth_error=AdapterAuthFailed("session rejected"))
    run = run_pool(source, settings, requests=requests_for("a", "b"), alternatives=("other",))
    assert run.invocation.outcome is InvocationOutcome.AUTH_FAILED
    assert run.invocation.advances_watermark is False
    assert set(run.invocation.requeue_keys()) == {"a", "b"}
    assert run.parked is None
    assert source.attempts == []


def test_a_session_that_dies_mid_run_stops_the_pool_and_keeps_what_landed(settings):
    source = Instrumented(script={"b": [AdapterAuthFailed("expired")]})
    run = run_pool(
        source, settings, requests=requests_for("a", "b", "c"), alternatives=("other",),
        pacing=Pacing(base_delay_s=0.0, jitter_fraction=0.0),
    )
    assert run.invocation.outcome is InvocationOutcome.AUTH_FAILED
    assert run.invocation.advances_watermark is False
    assert "b" in run.invocation.requeue_keys()


def test_a_broken_adapter_reports_breakage_rather_than_a_block(settings):
    """The two failures have different remedies, so they must stay apart."""
    source = Instrumented(auth_error=AdapterBroken("the tool is not installed"))
    run = run_pool(source, settings, requests=requests_for("a"))
    assert run.invocation.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert run.parked is None


def test_an_empty_request_list_is_a_clean_no_op(settings):
    run = run_pool(Instrumented(), settings, requests=())
    assert run.ok
    assert run.invocation.results == ()



class Paced(BaseAdapter):
    name = "paced-fake"


def test_a_built_adapter_runs_through_the_pool_under_its_own_settings(tmp_path):
    """``acquire_paced`` is the paced twin of ``BaseAdapter.acquire``; only the tool is replaced."""
    staging = tmp_path / "staging"
    staging.mkdir()
    settings = AdapterSettings(download_staging=staging, concurrency=2, pacing_delay_s=0.0)
    source = Instrumented()
    adapter = Paced(settings, source=source)

    run = acquire_paced(adapter, requests_for("a", "b"), sleep=Recorder(), clock=lambda: FIXED_NOW)

    assert run.ok
    assert run.invocation.adapter == "paced-fake"
    assert len(run.invocation.acquired()) == 2


def test_a_built_adapter_that_cannot_run_reports_the_contract_shape(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()

    class Absent(BaseAdapter):
        name = "absent-fake"

        def _source(self, scope):
            raise AdapterBroken("the tool is not installed", remedy=Remedy.INSTALL_ADAPTER)

    adapter = Absent(AdapterSettings(download_staging=staging))
    run = acquire_paced(adapter, requests_for("a"))
    assert run.invocation.outcome is InvocationOutcome.ADAPTER_BROKEN
    assert run.invocation.remedy is Remedy.INSTALL_ADAPTER
    assert run.parked is None



def test_the_pool_declares_no_second_cap_and_no_second_delay():
    """R10's second half: pacing is the adapter's, never a shared file, read from the source."""
    source = DOWNLOAD_SOURCE.read_text()
    assert "settings.concurrency" in source

    # Docstrings are excluded: the module describes the file it replaced (P7).
    banned = ("settings.json", "downloads_concurrent_max", "download_delay_sec")
    tree = ast.parse(source)
    docstrings = {
        id(node.body[0].value)
        for node in ast.walk(tree)
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        and node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    }
    offenders = [
        (node.value, name)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in docstrings
        for name in banned
        if name in node.value
    ]
    assert offenders == [], f"{offenders}: that is the shared settings file KTD20 removed"

    # The only concurrency value in the module is the semaphore reading the adapter's field.
    assignments = re.findall(r"^\s*(?:max_)?concurrency\s*[:=]", source, re.MULTILINE)
    assert assignments == [], assignments


def test_a_lossless_policy_refusal_still_short_circuits_before_any_fetch(settings):
    """The pool changes what surrounds the per-track step, never the step itself."""
    strict = AdapterSettings(
        download_staging=settings.download_staging, lossless_policy=LosslessPolicy.STRICT
    )
    source = Instrumented(lossless=False)
    run = run_pool(source, strict, requests=requests_for("t"))
    assert run.invocation.results[0].outcome is TrackOutcome.REFUSED_BY_POLICY
    assert source.attempts == []


def test_a_result_the_pool_returns_is_the_contracts_own_type(settings):
    run = run_pool(Instrumented(), settings, requests=requests_for("t"))
    assert isinstance(run.invocation, InvocationResult)
    assert all(isinstance(r, TrackResult) for r in run.invocation.results)
