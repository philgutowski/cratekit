"""R-705: one gate for every call to the streaming provider.

Six claims, one per requirement of the brief, and every one of them is about
the failure the eleventh attended sitting produced on the author's account:

1. **Pacing holds the interval**, read from the configuration, measured from
   the last call any process made, and a ``Retry-After`` the provider sends
   holds the next call for at least that long.
2. **The breaker trips on a rate limit that survives the ladder.** Six answers
   in a row, the count one spent ladder costs, and the trip is the job engine's
   own park: a sweep stops at the first surviving rate limit with every
   remaining item pending, and never claims the next label.
3. **The cooldown outlives the process.** A second process started inside the
   window refuses before it makes a call, and names the time the window lifts.
4. **One driver at a time.** Two real processes making calls through one gate
   never have a request in flight together and keep the interval between them.
   Both are read off the stamps the gate wrote and an ``O_EXCL`` marker, never
   off a gap the test timed between two sends, and every bound is one a busy
   machine can only widen (R-759).
5. **Spend is counted**, across processes, so a run can report what it cost.
6. **The two build sites attach the gate and nothing else builds a client.**

Every schedule is driven with a fake clock whose ``sleep`` advances it, so the
suite asserts on the waits a run would have taken rather than taking them. The
two process tests use the real clock and real sleeps, because the lock the
kernel holds cannot be faked, and their intervals are short. They assert on
the stamps the gate wrote rather than on times they measured themselves.
"""

from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import requests
from requests.structures import CaseInsensitiveDict

from cratekit.acquire import listing
from cratekit.core import config, jobs, provider_gate
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.provider_gate import (
    COOLDOWN,
    HELD,
    LOCK_WAIT_S,
    TRIP_AFTER,
    Gate,
    GateSettings,
    Spend,
)

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"


# ═══════════════════════════════════════════════════════════════════════════
# Doubles
# ═══════════════════════════════════════════════════════════════════════════


class Clock:
    """A wall clock that moves only when something sleeps on it."""

    def __init__(self, start: float = 1_700_000_000.0) -> None:
        self.now = start
        self.slept: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


class Response:
    def __init__(self, status_code: int = 200, headers: dict[str, str] | None = None) -> None:
        self.status_code = status_code
        self.headers = CaseInsensitiveDict(headers or {})


class Transport:
    """A stand-in for the client's ``requests.Session``: answers in order, the
    last answer repeating, and records every request it was asked to make."""

    def __init__(self, *answers: Any) -> None:
        self.answers = list(answers) or [Response()]
        self.calls: list[tuple[str, str]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        self.calls.append((method, url))
        answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
        if isinstance(answer, BaseException):
            raise answer
        return answer


def rate_limited(retry_after: str | None = None) -> Response:
    headers = {} if retry_after is None else {"Retry-After": retry_after}
    return Response(429, headers)


class TooManyRequests(Exception):
    """What the client raises off a 429, spelled here so the ladder test needs
    no provider library."""


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def paths(tmp_path: Path) -> tuple[Path, Path]:
    return tmp_path / "gate" / "provider_gate.json", tmp_path / "gate" / "provider_gate.lock"


def make_gate(
    paths: tuple[Path, Path],
    clock: Clock,
    *,
    min_interval_s: float = 1.0,
    cooldown_s: float = 900.0,
) -> Gate:
    state, lock = paths
    return Gate(
        GateSettings(min_interval_s=min_interval_s, cooldown_s=cooldown_s),
        path=state,
        lock_path=lock,
        clock=clock,
        sleep=clock.sleep,
    )


def send_through(gate: Gate, transport: Transport, url: str = "https://api.invalid/x") -> Any:
    return gate.call(lambda: transport.request("GET", url))


def trip(gate: Gate, transport: Transport | None = None) -> CratekitError:
    """Drive the breaker to its trip and return the refusal it raised."""
    transport = transport or Transport(rate_limited())
    with pytest.raises(CratekitError) as caught:
        for _ in range(TRIP_AFTER):
            send_through(gate, transport)
    return caught.value


# ═══════════════════════════════════════════════════════════════════════════
# 1. Pacing
# ═══════════════════════════════════════════════════════════════════════════


def test_consecutive_calls_wait_out_the_interval(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport()

    for _ in range(3):
        send_through(gate, transport)

    # The first call finds no earlier call and sleeps nothing; each later one
    # sleeps the whole interval, because nothing else moved the clock.
    assert clock.slept == [1.0, 1.0]
    assert len(transport.calls) == 3


def test_a_gap_already_longer_than_the_interval_sleeps_nothing(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport()

    send_through(gate, transport)
    clock.now += 5.0
    send_through(gate, transport)

    assert clock.slept == []


def test_the_interval_is_the_configured_one(paths, clock, tmp_path):
    """``[provider] min_interval_s`` is what the gate paces with, off the
    frozen configuration and not off a module constant."""
    cfg = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 2.5}))
    settings = GateSettings.from_config(cfg)
    gate = Gate(settings, path=paths[0], lock_path=paths[1], clock=clock, sleep=clock.sleep)
    transport = Transport()

    send_through(gate, transport)
    send_through(gate, transport)

    assert settings.min_interval_s == 2.5
    assert clock.slept == [2.5]


def test_the_interval_is_measured_from_the_last_call_by_any_gate(paths, clock):
    """Two gates over one state file, which is what two processes are, share
    one last call time: the second gate's first call waits on the first's."""
    first = make_gate(paths, clock, min_interval_s=1.0)
    second = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport()

    send_through(first, transport)
    send_through(second, transport)

    assert clock.slept == [1.0]


def test_a_retry_after_in_seconds_holds_the_next_call_at_least_that_long(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport(rate_limited("7"), Response())

    send_through(gate, transport)  # answered 429 with Retry-After 7
    send_through(gate, transport)

    assert clock.slept == [7.0], "the provider asked for seven seconds and got the interval"


def test_a_retry_after_as_an_http_date_is_honoured(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    from email.utils import formatdate

    when = formatdate(clock.now + 30.0, usegmt=True)
    transport = Transport(rate_limited(when), Response())

    send_through(gate, transport)
    send_through(gate, transport)

    assert clock.slept == [30.0]


def test_a_retry_after_shorter_than_the_interval_does_not_shorten_it(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport(rate_limited("0.2"), Response())

    send_through(gate, transport)
    send_through(gate, transport)

    assert clock.slept == [1.0]


def test_an_unreadable_retry_after_is_zero_rather_than_a_guess(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport(rate_limited("soon"), Response())

    send_through(gate, transport)
    send_through(gate, transport)

    assert clock.slept == [1.0]


# ═══════════════════════════════════════════════════════════════════════════
# 2. The breaker
# ═══════════════════════════════════════════════════════════════════════════


def test_the_trip_count_is_one_spent_ladder():
    """The gate cannot import the ladder, so the two numbers are pinned to
    each other here: an initial attempt plus every retry the ladder makes."""
    assert TRIP_AFTER == listing.DEFAULT_MAX_RETRIES + 1


def test_the_sixth_consecutive_rate_limit_answer_trips_and_records_the_cooldown(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0, cooldown_s=900.0)
    transport = Transport(rate_limited())

    refused = trip(gate, transport)

    assert len(transport.calls) == TRIP_AFTER, "the trip came before or after the ladder"
    assert refused.cause.reason == COOLDOWN
    assert refused.cause.retryable is False, "an automatic retry into a cooldown is the harm"
    written = json.loads(paths[0].read_text())
    assert written["tripped_at"] == clock.now
    assert written["lifts_at"] == clock.now + 900.0
    assert written["trips"] == 1
    assert refused.cause.detail["lifts_at"] == provider_gate._iso(clock.now + 900.0)
    assert refused.cause.detail["remaining_s"] == 900


def test_the_trip_is_the_job_engines_own_park(paths, clock):
    """Raised as ``Parked`` so the engine releases the item in flight and
    claims nothing further, without any worker knowing the gate exists."""
    gate = make_gate(paths, clock)

    refused = trip(gate)

    assert isinstance(refused, jobs.Parked)


def test_a_success_breaks_the_run_of_rate_limit_answers(paths, clock):
    gate = make_gate(paths, clock)
    five = [rate_limited()] * (TRIP_AFTER - 1)
    transport = Transport(*five, Response(), *five, Response())

    for _ in range(2 * TRIP_AFTER):
        send_through(gate, transport)

    assert len(transport.calls) == 2 * TRIP_AFTER
    assert json.loads(paths[0].read_text())["tripped_at"] is None


def test_a_retry_after_at_or_above_the_cooldown_trips_at_once(paths, clock):
    """A provider asking for the cooldown outright is not waited for six times."""
    gate = make_gate(paths, clock, cooldown_s=900.0)
    transport = Transport(rate_limited("900"))

    with pytest.raises(CratekitError) as caught:
        send_through(gate, transport)

    assert len(transport.calls) == 1
    assert caught.value.cause.reason == COOLDOWN
    assert json.loads(paths[0].read_text())["lifts_at"] == clock.now + 900.0


def test_a_retry_after_longer_than_the_cooldown_sets_the_lift_time(paths, clock):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    transport = Transport(rate_limited("3600"))

    with pytest.raises(CratekitError):
        send_through(gate, transport)

    assert json.loads(paths[0].read_text())["lifts_at"] == clock.now + 3600.0


def test_a_spent_ladder_through_the_gate_comes_out_as_the_park(paths, clock):
    """The ladder climbs on the client's own exception five times and the gate
    trips on the sixth answer, so what the ladder re-raises is the park and
    not the provider's error, and no seventh call is made."""
    gate = make_gate(paths, clock)
    transport = Transport(rate_limited())

    def page(limit: int, offset: int) -> Any:
        answer = send_through(gate, transport)
        if answer.status_code == 429:
            raise TooManyRequests("Too many requests")
        return answer

    with pytest.raises(jobs.Parked) as caught:
        listing.fetch_with_retry(page, limit=10, offset=0, sleep=clock.sleep)

    assert caught.value.cause.reason == COOLDOWN
    assert len(transport.calls) == TRIP_AFTER


def test_an_exception_out_of_send_is_a_call_and_not_a_rate_limit_answer(paths, clock):
    gate = make_gate(paths, clock)
    transport = Transport(rate_limited(), ConnectionError("reset"), rate_limited())

    send_through(gate, transport)
    with pytest.raises(ConnectionError):
        send_through(gate, transport)
    send_through(gate, transport)

    written = json.loads(paths[0].read_text())
    assert (written["calls"], written["rate_limited"], written["consecutive"]) == (3, 2, 2)


# ═══════════════════════════════════════════════════════════════════════════
# 2, continued. The breaker stops a run, with the rest pending
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path):
    built = config.from_dict(_config_data(tmp_path))
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def queue(tmp_path):
    root = tmp_path / "jobs"
    with jobs.open_store(root / jobs.QUEUE_FILENAME) as store:
        yield store, root


def test_the_breaker_stops_a_sweep_at_the_first_surviving_rate_limit_with_the_rest_pending(
    paths, clock, queue, cfg
):
    """Three labels queued, the provider rate limiting throughout. The first
    label's ladder is spent, the gate trips, and the engine blocks the job with
    all three items pending: it never claims the second label, which is the
    second ladder into a live limit the sitting paid for twenty times."""
    store, root = queue
    gate = make_gate(paths, clock)
    transport = Transport(rate_limited())
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )
    claimed: list[str] = []

    def page(limit: int, offset: int) -> Any:
        answer = send_through(gate, transport)
        if answer.status_code == 429:
            raise TooManyRequests("Too many requests")
        return answer

    def handle(_job, item):
        claimed.append(item.item_id)
        listing.fetch_with_retry(page, limit=10, offset=0, sleep=clock.sleep)
        return None

    result = jobs.drive(store, job.job_id, handle, root=root)

    assert claimed == ["a"], "the driver claimed past the trip"
    assert len(transport.calls) == TRIP_AFTER
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.job.cause is not None and result.job.cause.reason == COOLDOWN
    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {name: jobs.ItemState.PENDING for name in ("a", "b", "c")}


# ═══════════════════════════════════════════════════════════════════════════
# 3. The cooldown outlives the process
# ═══════════════════════════════════════════════════════════════════════════


def test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time(paths, clock):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    trip(gate)
    lifts = clock.now + 900.0
    clock.now += 100.0

    with pytest.raises(jobs.Parked) as caught:
        gate.assert_open()

    cause = caught.value.cause
    assert cause.reason == COOLDOWN
    assert cause.detail["lifts_at"] == provider_gate._iso(lifts)
    assert cause.detail["remaining_s"] == 800
    assert provider_gate._iso(lifts) in cause.message
    assert "800 seconds" in cause.message
    assert any(provider_gate._iso(lifts) in step for step in cause.remediation.steps)


def test_inside_the_cooldown_a_call_is_refused_before_it_is_sent(paths, clock):
    gate = make_gate(paths, clock)
    trip(gate)
    transport = Transport()

    with pytest.raises(jobs.Parked):
        send_through(gate, transport)

    assert transport.calls == []


def test_the_cooldown_lifts_and_calls_go_through_again(paths, clock):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    trip(gate)
    clock.now += 900.0
    transport = Transport()

    gate.assert_open()
    send_through(gate, transport)

    assert len(transport.calls) == 1


def test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another(paths, tmp_path):
    """The claim the brief makes literally: a REAL second process, over the
    same state file, refuses before any call and names the time it lifts."""
    state, lock = paths
    gate = Gate(GateSettings(cooldown_s=900.0), path=state, lock_path=lock, sleep=lambda s: None)
    trip(gate)
    lifts = json.loads(state.read_text())["lifts_at"]

    script = tmp_path / "second_process.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys
            from pathlib import Path
            from cratekit.core.cause import CratekitError
            from cratekit.core.provider_gate import Gate, GateSettings

            state, lock = Path(sys.argv[1]), Path(sys.argv[2])
            gate = Gate(GateSettings(), path=state, lock_path=lock)
            sent = []
            report = {}
            try:
                gate.assert_open()
            except CratekitError as exc:
                report["open"] = exc.cause.to_json()
            try:
                gate.call(lambda: sent.append(1))
            except CratekitError as exc:
                report["call"] = exc.cause.to_json()
            report["sent"] = len(sent)
            print(json.dumps(report))
            """
        )
    )
    done = _run_child(script, str(state), str(lock))

    report = json.loads(done.stdout)
    assert report["sent"] == 0, "the second process reached the provider"
    assert report["open"]["reason"] == COOLDOWN
    assert report["call"]["reason"] == COOLDOWN
    assert report["open"]["detail"]["lifts_at"] == provider_gate._iso(lifts)


# ═══════════════════════════════════════════════════════════════════════════
# 4. One driver at a time
# ═══════════════════════════════════════════════════════════════════════════


#: One driver process for both tests below. It waits at a barrier until both
#: drivers are up, so both are running when the calls begin, then makes its
#: calls through one real gate. Inside each send it records three things: the
#: ``last_call`` stamp the gate has just written to the shared file, the wall
#: clock as the send begins, and whether another send already held the in
#: flight marker, which ``O_EXCL`` answers without a clock.
_DRIVER = """
import json, os, sys, time
from pathlib import Path
from cratekit.core.provider_gate import Gate, GateSettings

state, lock, out, marker, barrier = (Path(arg) for arg in sys.argv[1:6])
count, interval, hold = int(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8])
gate = Gate(GateSettings(min_interval_s=interval), path=state, lock_path=lock)
calls, overlaps = [], 0

class Answer:
    status_code = 200
    headers = {}

def send():
    global overlaps
    sent = time.time()
    calls.append((json.loads(state.read_text())["last_call"], sent))
    try:
        fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        overlaps += 1
        time.sleep(hold)
        return Answer()
    try:
        time.sleep(hold)
    finally:
        os.close(fd)
        os.unlink(marker)
    return Answer()

(barrier / str(os.getpid())).touch()
give_up = time.monotonic() + 30  # a hang guard, not a measurement
while len(list(barrier.iterdir())) < 2:
    if time.monotonic() > give_up:
        sys.exit("the other driver never reached the barrier")
    time.sleep(0.005)

for _ in range(count):
    gate.call(send)
out.write_text(json.dumps({"calls": calls, "overlaps": overlaps}))
"""

#: How far a send may begin BEFORE its own stamp. The gate sleeps on the
#: monotonic clock and stamps with the wall clock, and the two can drift apart
#: by a slew; a busy machine only ever makes a send later than its stamp, never
#: earlier, so this allowance is for the clocks and not for the load.
_CLOCK_SKEW_S = 0.001


def _drive_two_processes(
    paths: tuple[Path, Path], tmp_path: Path, *, count: int, interval: float, hold: float
) -> list[dict[str, Any]]:
    """Run two drivers over one gate and return what each recorded. A driver
    still running when this returns, by a failed assertion or a timeout, is
    killed here, so it cannot hold the lock through the rest of the suite."""
    state, lock = paths
    script = tmp_path / "driver.py"
    script.write_text(_DRIVER)
    marker = tmp_path / "in_flight"
    barrier = tmp_path / "barrier"
    barrier.mkdir()
    outs = [tmp_path / "a.json", tmp_path / "b.json"]
    children = [
        _start_child(
            script,
            *(str(p) for p in (state, lock, out, marker, barrier)),
            str(count),
            str(interval),
            str(hold),
        )
        for out in outs
    ]
    try:
        for child in children:
            _stdout, stderr = child.communicate(timeout=60)
            assert child.returncode == 0, stderr
    finally:
        for child in children:
            if child.poll() is None:
                child.kill()
                child.communicate()
    assert json.loads(state.read_text())["calls"] == 2 * count
    return [json.loads(out.read_text()) for out in outs]


def test_two_processes_keep_the_interval_between_every_call(paths, tmp_path):
    """Two REAL processes, four calls each, through one gate over one file.
    Every call's stamp, as the gate wrote it for the next caller to read, is
    at least the interval after the stamp before it, and no send begins
    before its own stamp. Together those put every request at least the
    interval after the last one either process made. Sorted into one chain,
    at least one neighbouring pair always comes from different processes,
    however the calls happened to interleave.

    R-759. The version before this timed each send's own start with a wall
    clock and asserted the gaps against the interval less ten percent. What
    the gate spaces is its STAMP, and a send starts after the stamp and after
    the state file write that follows it, which is fsynced. That write took
    up to fourteen milliseconds longer for one call than for another at a
    load average of thirteen, enough to put two send starts 40.7 milliseconds
    apart against a fifty millisecond interval, and on the gate's log the
    same test read 0.039 and 0.031. The stamps carry no such noise. The gate
    computes each as the later of the clock and the last stamp plus the
    interval, so the first bound holds exactly, with no tolerance, and the
    second is a lower bound that a slow machine can only widen."""
    interval = 0.05
    reports = _drive_two_processes(paths, tmp_path, count=4, interval=interval, hold=0.0)

    calls = sorted(call for report in reports for call in report["calls"])
    assert len(calls) == 8
    stamps = [stamp for stamp, _sent in calls]
    for earlier, later in zip(stamps, stamps[1:]):
        assert later >= earlier + interval, f"two calls closer than the interval: {stamps}"
    early = [(stamp, sent) for stamp, sent in calls if sent < stamp - _CLOCK_SKEW_S]
    assert not early, f"a request went out before the gate's wait for it ended: {early}"


def test_two_processes_never_have_a_call_in_flight_together(paths, tmp_path):
    """Two REAL processes, four calls each, where every call holds the provider
    for a tenth of a second against an interval of a hundredth. No send ever
    finds another send's in flight marker.

    The hold is longer than the interval on purpose. With a hold shorter than
    it, the interval alone keeps the calls apart, and a gate whose lock did
    nothing would pass. Here only the lock can: a second process without it
    waits out a hundredth of a second and walks into a call still in flight.
    The verdict reads no clock, so a busy machine cannot change it."""
    reports = _drive_two_processes(paths, tmp_path, count=4, interval=0.01, hold=0.1)

    assert [report["overlaps"] for report in reports] == [0, 0], (
        f"two calls were in flight at once: {reports}"
    )


def test_a_lock_held_past_the_wait_is_refused_with_the_holder_named(paths, clock):
    """The wait is polled on the fake clock, so the whole two minutes pass in
    no time, and the refusal is the gate's own rather than a hang."""
    state, lock = paths
    gate = make_gate(paths, clock)
    lock.parent.mkdir(parents=True, exist_ok=True)
    holder = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)
    transport = Transport()
    try:
        with pytest.raises(jobs.Parked) as caught:
            send_through(gate, transport)
    finally:
        os.close(holder)

    assert caught.value.cause.reason == HELD
    assert caught.value.cause.retryable is False, "a held account is not a track to retry"
    assert transport.calls == []
    # The limit is the wait plus one interval, since a holder may sleep one
    # interval under the lock; the poll count cap and the time cap agree to
    # within one poll.
    assert sum(clock.slept) >= LOCK_WAIT_S + 1.0 - provider_gate.LOCK_POLL_S


def test_the_lock_file_is_never_unlinked(paths, clock):
    """Unlinking on release is how two holders come to hold one lock."""
    state, lock = paths
    gate = make_gate(paths, clock)

    send_through(gate, Transport())
    first = lock.stat().st_ino
    send_through(gate, Transport())

    assert lock.exists() and lock.stat().st_ino == first


# ═══════════════════════════════════════════════════════════════════════════
# 5. Spend
# ═══════════════════════════════════════════════════════════════════════════


def test_spend_counts_every_call_and_every_rate_limit_answer_across_gates(paths, clock):
    first = make_gate(paths, clock)
    second = make_gate(paths, clock)
    transport = Transport(Response(), rate_limited(), Response())

    send_through(first, transport)
    send_through(second, transport)
    send_through(first, transport)

    assert first.spend() == Spend(calls=3, rate_limited=1)
    assert provider_gate.spend(paths[0]) == Spend(calls=3, rate_limited=1)
    assert (first.calls, first.rate_limited) == (2, 0)
    assert (second.calls, second.rate_limited) == (1, 1)


def test_spend_since_is_the_difference_and_never_negative():
    assert Spend(12, 3).since(Spend(10, 1)) == Spend(2, 2)
    assert Spend(1, 0).since(Spend(5, 2)) == Spend(0, 0)


def test_a_call_is_counted_before_it_is_sent(paths, clock):
    """A crash mid request is still a call the account saw."""
    gate = make_gate(paths, clock)
    seen: list[int] = []

    def send() -> Any:
        seen.append(json.loads(paths[0].read_text())["calls"])
        return Response()

    gate.call(send)

    assert seen == [1]


def test_a_corrupt_state_file_reads_as_fresh_rather_than_locking_the_provider_out(paths, clock):
    state, _ = paths
    state.parent.mkdir(parents=True)
    state.write_text("{not json")
    gate = make_gate(paths, clock)

    send_through(gate, Transport())

    assert json.loads(state.read_text())["calls"] == 1


# ═══════════════════════════════════════════════════════════════════════════
# 6. The seam
# ═══════════════════════════════════════════════════════════════════════════


class _Answering(requests.adapters.BaseAdapter):
    """A transport adapter for a real ``requests.Session`` that answers every
    request with one status and records it, so the wrap is proven on the real
    object rather than on a stand-in with the same method name."""

    def __init__(self, status: int) -> None:
        super().__init__()
        self.status = status
        self.seen: list[str] = []

    def send(self, request, **kwargs):  # noqa: ANN001 - the base class signature
        self.seen.append(f"{request.method} {request.url}")
        answer = requests.Response()
        answer.status_code = self.status
        answer.headers = CaseInsensitiveDict()
        answer.url = request.url
        answer.request = request
        answer._content = b""
        return answer

    def close(self) -> None:
        pass


def test_attach_routes_every_request_of_a_real_session_through_the_gate_once(paths, clock):
    """``get`` and ``post`` both land in ``request``, and attaching twice, which
    is what a singleton tool built twice would do, wraps the original once."""
    gate = make_gate(paths, clock)
    session = requests.Session()
    answering = _Answering(200)
    session.mount("https://", answering)
    client = SimpleNamespace(request_session=session)

    assert gate.attach(client) is True
    session.get("https://api.invalid/one")
    session.post("https://api.invalid/two", data={"k": "v"})
    assert gate.attach(client) is True
    session.get("https://api.invalid/three")

    assert gate.calls == 3
    assert clock.slept == [1.0, 1.0]
    assert answering.seen == [
        "GET https://api.invalid/one",
        "POST https://api.invalid/two",
        "GET https://api.invalid/three",
    ]


def test_attach_sees_the_raw_rate_limit_status_on_a_real_session(paths, clock):
    gate = make_gate(paths, clock)
    session = requests.Session()
    session.mount("https://", _Answering(429))
    gate.attach(SimpleNamespace(request_session=session))

    with pytest.raises(jobs.Parked):
        for _ in range(TRIP_AFTER):
            session.get("https://api.invalid/x")

    assert gate.rate_limited == TRIP_AFTER


def test_attach_declines_a_client_with_no_transport(paths, clock):
    gate = make_gate(paths, clock)

    assert gate.attach(SimpleNamespace()) is False
    assert gate.attach(SimpleNamespace(request_session=object())) is False


def test_the_product_builds_a_provider_client_at_exactly_two_sites():
    """Both attach the gate, and a third site would be a caller the gate
    cannot see. The vendored tool's own constructor is one of the two, and
    ``acquire/vendored.py`` attaches to the session it builds."""
    package = SRC_ROOT / "cratekit"
    found = sorted(
        str(path.relative_to(package))
        for path in package.rglob("*.py")
        if "tidalapi.Session(" in path.read_text(encoding="utf-8")
    )
    assert found == ["_vendor/downloader/config.py", "acquire/provider_session.py"]


def test_the_two_reasons_are_declared_with_their_codes():
    assert REASONS[COOLDOWN] is ExitCode.UPSTREAM_UNAVAILABLE
    assert REASONS[HELD] is ExitCode.LIBRARY_BUSY


def test_the_state_files_are_declared_beside_the_credential():
    for key in (provider_gate.STATE_KEY, provider_gate.LOCK_KEY):
        entry = config.state_file(key)
        assert entry.root is config.StateRoot.INSTALLATION
        assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert config.state_path(provider_gate.STATE_KEY).parent == config.state_path(
        provider_gate.LOCK_KEY
    ).parent


# ═══════════════════════════════════════════════════════════════════════════
# The configuration
# ═══════════════════════════════════════════════════════════════════════════


def _config_data(tmp_path: Path, **overrides: Any) -> dict[str, Any]:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {
            "root": str(root),
            "volume_id": "F1E2-D3C4",
            "db_path": str(root / "db" / "master.db"),
        },
        "paths": {"download_staging": str(tmp_path / "staging")},
        "profile": {"name": "full"},
    }
    data.update(overrides)
    return data


def test_the_provider_defaults_are_conservative_and_named(tmp_path):
    section = config.from_dict(_config_data(tmp_path)).provider
    assert section.min_interval_s == config.DEFAULT_PROVIDER_MIN_INTERVAL_S == 1.0
    assert section.cooldown_s == config.DEFAULT_PROVIDER_COOLDOWN_S == 900
    assert GateSettings() == GateSettings.from_config(config.from_dict(_config_data(tmp_path)))


def test_the_provider_section_round_trips_through_the_file(tmp_path):
    built = config.from_dict(
        _config_data(tmp_path, provider={"min_interval_s": 0.5, "cooldown_s": 1800})
    )
    config.save(built)
    config.reset_cache()

    again = config.load()

    assert again.provider == built.provider
    assert GateSettings.from_config(again) == GateSettings(min_interval_s=0.5, cooldown_s=1800.0)


@pytest.mark.parametrize("value", [0, -1, 0.0, True, "1", float("nan"), float("inf")])
def test_a_non_positive_interval_is_refused_naming_the_key(tmp_path, value):
    problems = config.validate(_config_data(tmp_path, provider={"min_interval_s": value}))
    assert len(problems) == 1
    assert "provider.min_interval_s" in problems[0]
    assert "no value that switches pacing off" in problems[0]


@pytest.mark.parametrize("value", [0, -5, 1.5, True, "900"])
def test_a_cooldown_that_is_not_a_positive_whole_number_is_refused(tmp_path, value):
    problems = config.validate(_config_data(tmp_path, provider={"cooldown_s": value}))
    assert len(problems) == 1
    assert "provider.cooldown_s" in problems[0]


def test_an_absent_provider_section_is_not_a_problem(tmp_path):
    assert config.validate(_config_data(tmp_path, provider={})) == []
    assert config.validate(_config_data(tmp_path)) == []


# ═══════════════════════════════════════════════════════════════════════════
# Helpers for the process tests
# ═══════════════════════════════════════════════════════════════════════════


def _child_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(SRC_ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _start_child(script: Path, *args: str) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, str(script), *args],
        env=_child_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _run_child(script: Path, *args: str) -> subprocess.CompletedProcess:
    done = subprocess.run(
        [sys.executable, str(script), *args],
        env=_child_env(),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    return done


# ═══════════════════════════════════════════════════════════════════════════
# The seams: every client build site asks the gate and attaches it
# ═══════════════════════════════════════════════════════════════════════════


from cratekit.acquire import adapter as adapter_module  # noqa: E402 - the seam section
from cratekit.acquire import provider_session, vendored  # noqa: E402
from cratekit.acquire.adapter import (  # noqa: E402
    AdapterSettings,
    Offer,
    TrackOutcome,
    TrackRequest,
)
from cratekit.core import secrets  # noqa: E402
from cratekit.label import catalogue, tidal_catalogue  # noqa: E402
from cratekit.modules.outbound import account, tidal_account  # noqa: E402

STORED = {
    "token_type": "Bearer",
    "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2",
    "expiry_time": 946684800.0,
}


class _LoginClient:
    """A provider client whose login goes out through its transport, as the
    real one's does, so the wrap is proven to cover the login itself."""

    def __init__(self, transport: Transport | None = None) -> None:
        self.request_session = transport or Transport()
        self.token_type = None
        self.access_token = None
        self.refresh_token = None
        self.expiry_time = None

    def load_oauth_session(self, token_type, access_token, refresh_token=None, expiry_time=None, is_pkce=False):
        self.request_session.request("POST", "https://auth.invalid/token")
        self.token_type, self.access_token = token_type, access_token
        self.refresh_token, self.expiry_time = refresh_token, expiry_time
        return True


def _record_session() -> None:
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))


def test_client_session_attaches_the_gate_before_the_login_goes_out(paths, clock, monkeypatch):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    gate = make_gate(paths, clock)

    opened = provider_session.client_session(gate=gate)

    assert opened is client
    assert client.request_session._cratekit_gate is gate
    assert gate.calls == 1, "the login was not the first paced call"
    assert client.request_session.calls == [("POST", "https://auth.invalid/token")]


def test_client_session_refuses_inside_the_cooldown_before_building_a_client(
    paths, clock, monkeypatch
):
    built: list[int] = []

    def factory():
        built.append(1)
        return _LoginClient()

    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", factory)
    _record_session()
    gate = make_gate(paths, clock)
    trip(gate)

    with pytest.raises(jobs.Parked) as caught:
        provider_session.client_session(gate=gate)

    assert caught.value.cause.reason == COOLDOWN
    assert built == [], "a client was built inside the cooldown"


def test_client_session_with_no_gate_still_paces_at_the_defaults(clock, monkeypatch):
    """A caller that hands over nothing gets a gate, never a way past one."""
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()

    provider_session.client_session()

    attached = client.request_session._cratekit_gate
    assert attached.settings == GateSettings()
    assert attached.path == config.state_path(provider_gate.STATE_KEY)


def test_the_catalogue_opener_paces_with_the_frozen_configuration(tmp_path, monkeypatch):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    cfg = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 3.0, "cooldown_s": 60}))

    tidal_catalogue.open_catalogue(cfg)

    assert client.request_session._cratekit_gate.settings == GateSettings(3.0, 60.0)


def test_the_account_opener_paces_with_the_frozen_configuration(tmp_path, monkeypatch):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    cfg = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 3.0, "cooldown_s": 60}))

    tidal_account.open_account(cfg)

    assert client.request_session._cratekit_gate.settings == GateSettings(3.0, 60.0)


def test_catalogue_resolve_hands_the_configuration_to_the_opener(tmp_path, monkeypatch):
    """``resolve`` used to discard its configuration; the gate needs it."""
    handed: list[Any] = []
    monkeypatch.setattr(tidal_catalogue, "open_catalogue", lambda cfg=None: handed.append(cfg))
    _record_session()
    cfg = config.from_dict(_config_data(tmp_path))

    catalogue.resolve(cfg)

    assert handed == [cfg]


def test_account_resolve_hands_the_configuration_to_the_opener(tmp_path, monkeypatch):
    handed: list[Any] = []
    monkeypatch.setattr(tidal_account, "open_account", lambda cfg=None: handed.append(cfg) or object())
    _record_session()
    cfg = config.from_dict(_config_data(tmp_path))

    account.resolve(cfg)

    assert handed == [cfg]


def test_adapter_settings_carry_the_gate_settings_off_the_configuration(tmp_path):
    cfg = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 0.25, "cooldown_s": 3600}))

    settings = AdapterSettings.from_config(cfg)

    assert settings.gate == GateSettings(min_interval_s=0.25, cooldown_s=3600.0)


class _ToolSession:
    """The vendored tool's session with a real transport shape."""

    def __init__(self, transport: Transport | None = None) -> None:
        self.request_session = transport or Transport()

    def track(self, key: str) -> Any:
        self.request_session.request("GET", f"https://api.invalid/tracks/{key}")
        return SimpleNamespace(audio_quality="LOSSLESS")


def _vendored(tmp_path: Path, paths, clock, **kwargs: Any) -> vendored._VendoredSource:
    staging = tmp_path / "staging"
    staging.mkdir(exist_ok=True)
    settings = AdapterSettings(download_staging=staging, gate=GateSettings(min_interval_s=1.0))
    source = vendored._VendoredSource(settings, tmp_path / "token.json", **kwargs)
    # The gate is built from the settings; the clock is swapped so the test
    # drives its schedule, the paths so it shares nothing with another test.
    source._gate = make_gate(paths, clock)
    return source


def test_the_vendored_adapter_attaches_the_gate_to_an_injected_session(tmp_path, paths, clock):
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)

    source.authenticate()
    source.offer(TrackRequest(key="x"))
    source.offer(TrackRequest(key="y"))

    assert session.request_session._cratekit_gate is source._gate
    assert source._gate.calls == 2
    assert clock.slept == [1.0]


def test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool(
    tmp_path, paths, clock
):
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)
    trip(source._gate)

    with pytest.raises(jobs.Parked) as caught:
        source.authenticate()

    assert caught.value.cause.reason == COOLDOWN
    assert session.request_session.calls == []


def test_a_rate_limited_login_comes_out_of_client_session_as_the_park(paths, clock, monkeypatch):
    """The login is a paced call like any other. Translated with the rest of
    the login's failures it would read as an outage to wait out, or worse as
    a rejected session to log in again over."""
    client = _LoginClient(Transport(rate_limited("900")))
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()

    with pytest.raises(jobs.Parked) as caught:
        provider_session.client_session(gate=make_gate(paths, clock))

    assert caught.value.cause.reason == COOLDOWN


def test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park(
    tmp_path, paths, clock, monkeypatch
):
    """The tool's login is wrapped in the same translation as the client's,
    and a park read as a rejected session would park the job under
    credential-missing. The tool's two classes are the smallest doubles the
    real ``authenticate`` path accepts, since nothing offline drives it
    otherwise; the gate is attached before the login, so the login is the one
    counted call and the one rate limited answer."""
    import cratekit._vendor.downloader.config as tool_config

    source = _vendored(tmp_path, paths, clock)
    gate = source._gate
    session = _ToolSession(Transport(rate_limited("900")))

    class Settings:
        def __init__(self) -> None:
            self.data = SimpleNamespace()

    class Tidal:
        def __init__(self, _settings: Any) -> None:
            self.session = session
            self.data = SimpleNamespace(is_pkce=True)
            self.file_path = self.path_base = ""
            self.token_from_storage = False

        def read(self, _path: str) -> bool:
            return True

        def login_token(self, do_pkce: bool = False) -> bool:
            # What the real tool does: every exception inside the login is
            # caught, the session file is deleted, and the answer is False.
            try:
                self.session.request_session.request("POST", "https://auth.invalid/token")
            except Exception:  # noqa: BLE001 - the tool's own shape
                return False
            return True

    monkeypatch.setattr(tool_config, "Settings", Settings)
    monkeypatch.setattr(tool_config, "Tidal", Tidal)

    with pytest.raises(jobs.Parked) as caught:
        source.authenticate()

    assert caught.value.cause.reason == COOLDOWN
    assert session.request_session._cratekit_gate is gate
    assert (gate.calls, gate.rate_limited) == (1, 1)


def test_a_trip_the_tool_swallowed_during_a_download_comes_out_of_fetch_as_the_park(
    tmp_path, paths, clock
):
    """The wrapped tool answers "no file" over any exception, the trip included.
    ``fetch`` asks the gate again after the tool returns, so the park reaches
    the worker and the track goes back to pending rather than failing."""
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)
    source.authenticate()
    gate = source._gate

    class SwallowingDownload:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        def item(self, **_kwargs: Any) -> tuple[bool, str]:
            try:
                trip(gate)
            except jobs.Parked:
                pass  # what the tool does with every exception
            return False, ""

    source._downloader = SwallowingDownload
    source._tidal = object()

    with pytest.raises(jobs.Parked) as caught:
        source.fetch(TrackRequest(key="x"), tmp_path / "staging")

    assert caught.value.cause.reason == COOLDOWN


class _TrippingSource:
    """A track source whose lookup or fetch raises the gate's park."""

    def __init__(self, parked: CratekitError, *, at: str) -> None:
        self.parked = parked
        self.at = at

    def authenticate(self) -> None:
        pass

    def offer(self, request: TrackRequest) -> Offer:
        if self.at == "offer":
            raise self.parked
        return Offer(lossless=True, detail="LOSSLESS")

    def fetch(self, request: TrackRequest, destination: Path) -> Path:
        raise self.parked


@pytest.mark.parametrize("at", ["offer", "fetch"])
def test_acquire_one_lets_the_park_through_rather_than_failing_the_track(
    tmp_path, paths, clock, at
):
    """Both broad catches in ``acquire_one`` turn an exception into one
    unavailable track; the park is the one exception that must not be."""
    parked = trip(make_gate(paths, clock))
    settings = AdapterSettings(download_staging=tmp_path / "staging")

    with pytest.raises(jobs.Parked) as caught:
        adapter_module.acquire_one(_TrippingSource(parked, at=at), TrackRequest(key="x"), settings)

    assert caught.value is parked


def test_acquire_one_still_softens_an_ordinary_failure(tmp_path):
    """The pass through is for the park alone: a dead track is still one
    unavailable track and never the run."""
    settings = AdapterSettings(download_staging=tmp_path / "staging")
    source = _TrippingSource(RuntimeError("the provider had nothing"), at="offer")  # type: ignore[arg-type]

    result = adapter_module.acquire_one(source, TrackRequest(key="x"), settings)

    assert result.outcome is not TrackOutcome.ACQUIRED


# ═══════════════════════════════════════════════════════════════════════════
# 5, continued. Every run that reached the provider says what it spent
# ═══════════════════════════════════════════════════════════════════════════


import io  # noqa: E402 - the dispatcher section

from cratekit import cli  # noqa: E402
from cratekit.cli import PROVIDER_SPEND  # noqa: E402
from tests.cli_drive import drive  # noqa: E402


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """A machine the real dispatcher can load, with every module on."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True, exist_ok=True)
    (root / "db").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    # A short interval, because these runs go through a REAL gate on the real
    # clock, and the login is one paced call among the few each test makes.
    built = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 0.01}))
    config.save(built)
    config.reset_cache()
    return built


def _spend_warnings(envelope: dict) -> list[str]:
    return [w["message"] for w in envelope.get("warnings", ()) if w.get("code") == PROVIDER_SPEND]


def test_a_run_that_reached_the_provider_reports_its_calls(installed, monkeypatch):
    """Driven through the REAL dispatcher and the real catalogue opener: the
    only fake is the client, whose login goes out through its transport, so
    the one call this run makes is the login the gate paced."""
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()

    code, envelope = drive(["label", "harvest", "https://example.invalid/playlist/harvest"])

    assert code != int(ExitCode.OK), "the fake client cannot serve a playlist"
    assert _spend_warnings(envelope) == [
        "1 call to the streaming provider this run, none answered with a rate limit; "
        "1 on the account and none under Cratekit's app credentials"
    ]


def test_the_spend_line_reaches_a_person_on_the_human_output(installed, monkeypatch):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    out, err = io.StringIO(), io.StringIO()

    cli.run(["label", "harvest", "https://example.invalid/playlist/harvest"], stdout=out, stderr=err)

    shown = out.getvalue() + err.getvalue()
    assert f"warning [{PROVIDER_SPEND}]: 1 call to the streaming provider this run" in shown


def test_rate_limit_answers_are_named_in_the_spend_line(installed, monkeypatch):
    """The counts come off the shared file, so answers any process received
    while this verb ran are in the line."""
    client = _LoginClient(Transport(rate_limited(), Response()))
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    original = tidal_catalogue.open_catalogue

    def opening(cfg=None):
        catalogue_over_client = original(cfg)
        # Two more calls the verb did not make itself, one of them rate
        # limited. The transport is already gated, so these are plain requests
        # on it; a gated call made from INSIDE a gated call would wait on the
        # lock it already holds, which is what the wrap exists to make
        # impossible for the client's own code to do.
        client.request_session.request("GET", "https://api.invalid/a")
        client.request_session.request("GET", "https://api.invalid/b")
        return catalogue_over_client

    monkeypatch.setattr(tidal_catalogue, "open_catalogue", opening)

    _, envelope = drive(["label", "harvest", "https://example.invalid/playlist/harvest"])

    assert _spend_warnings(envelope) == [
        "3 calls to the streaming provider this run, 1 answered with a rate limit; "
        "3 on the account and none under Cratekit's app credentials"
    ]


def test_a_run_that_never_reached_the_provider_carries_no_spend_line(installed):
    code, envelope = drive(["label", "registry", "add", "Hotflush Recordings"])

    assert code == int(ExitCode.OK), envelope
    assert _spend_warnings(envelope) == []


def test_the_spend_line_survives_a_refusal(installed, monkeypatch):
    """The sitting's failed downloads spent calls into a live limit and the
    screen said nothing; a refused run reports what it cost as well."""
    client = _LoginClient(Transport(rate_limited("900")))
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()

    code, envelope = drive(["label", "harvest", "https://example.invalid/playlist/harvest"])

    assert envelope["cause"]["reason"] == COOLDOWN
    assert _spend_warnings(envelope) == [
        "1 call to the streaming provider this run, 1 answered with a rate limit; "
        "1 on the account and none under Cratekit's app credentials"
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 1, continued. What a sweep costs per release, measured on the tree
# ═══════════════════════════════════════════════════════════════════════════


def test_one_offered_release_costs_two_calls_on_the_catalogue():
    """The number the run time estimate in docs/mutation/r705-notes.md stands
    on. Measured on the tree's own ``release_tracks`` over a counting client,
    not on a fixture written beside the estimate: one album read and one page
    of its tracks, for a release under one page. The eleventh sitting's sweep
    offered 1,701 releases, so the offer checks alone were at least 3,402
    calls before any listing or verification."""
    reads: list[str] = []

    class Album:
        num_tracks = 3
        year = 2024

        def tracks(self, limit: int = 100, offset: int = 0) -> list[Any]:
            reads.append(f"tracks limit={limit} offset={offset}")
            return [SimpleNamespace(id=n, name=f"t{n}") for n in range(3)]

    class Client:
        def album(self, identity: str) -> Album:
            reads.append(f"album {identity}")
            return Album()

    rows, year, _short = tidal_catalogue.TidalCatalogue(Client()).release_tracks("r1")

    assert (len(rows), year) == (3, 2024)
    assert len(reads) == 2, reads
    assert reads[0] == "album r1" and reads[1].startswith("tracks ")


# ═══════════════════════════════════════════════════════════════════════════
# What the review found, each driven
# ═══════════════════════════════════════════════════════════════════════════


def test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released(paths, clock):
    """A Retry-After longer than the interval is slept OUTSIDE the lock, so a
    second driver waits on the same not_before off the file rather than on
    the holder, and the lock is never held past one request and one interval.
    The sleep callback tries the lock while the gate sleeps and records
    whether it got it."""
    state, lock = paths
    gate = make_gate(paths, clock, min_interval_s=1.0)
    taken_while_sleeping: list[tuple[float, bool]] = []

    def sleeping(seconds: float) -> None:
        probe = os.open(lock, os.O_RDWR)
        try:
            fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
            taken_while_sleeping.append((seconds, True))
            fcntl.flock(probe, fcntl.LOCK_UN)
        except BlockingIOError:
            taken_while_sleeping.append((seconds, False))
        finally:
            os.close(probe)
        clock.now += seconds

    gate._sleep = sleeping
    transport = Transport(rate_limited("300"), Response(), Response())

    send_through(gate, transport)  # 429, Retry-After 300
    send_through(gate, transport)  # sleeps 300 with the lock released
    send_through(gate, transport)  # sleeps one interval, under the lock

    assert taken_while_sleeping == [(300.0, True), (1.0, False)]
    assert len(transport.calls) == 3


def test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch(
    tmp_path, paths, clock
):
    """The held refusal is a park too, and the tool swallows it like any
    other exception; fetch asks the gate afterwards and gets it back."""
    state, lock = paths
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)
    source.authenticate()
    lock.parent.mkdir(parents=True, exist_ok=True)
    holder = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)

    class SwallowingDownload:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        def item(self, **_kwargs: Any) -> tuple[bool, str]:
            try:
                session.request_session.request("GET", "https://api.invalid/stream")
            except Exception:  # noqa: BLE001 - what the tool does
                pass
            return False, ""

    source._downloader = SwallowingDownload
    source._tidal = object()
    try:
        with pytest.raises(jobs.Parked) as caught:
            source.fetch(TrackRequest(key="x"), tmp_path / "staging")
    finally:
        os.close(holder)

    assert caught.value.cause.reason == HELD


def test_a_successful_call_clears_the_remembered_park(paths, clock):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    trip(gate)
    clock.now += 900.0

    send_through(gate, Transport())
    gate.raise_if_parked()


def test_the_download_pacing_reads_retry_after_through_the_gates_parser(clock):
    """One parser of the header in the tree: the download probe's reading of
    an exception's Retry-After equals the gate's reading of the same value."""
    from datetime import datetime, timezone
    from email.utils import formatdate

    from cratekit.acquire import download

    reference = datetime.fromtimestamp(clock.now, tz=timezone.utc)
    dated = formatdate(clock.now + 90.0, usegmt=True)
    for raw in ("45", dated):
        exc = RuntimeError("throttled")
        exc.response = SimpleNamespace(headers={"retry-after": raw})  # type: ignore[attr-defined]
        assert download.retry_hint_seconds(exc, now=reference) == provider_gate.retry_after_seconds(
            raw, clock.now
        )
    assert download._as_seconds("nonsense", reference) is None
    assert provider_gate.retry_after_seconds("nonsense", clock.now) is None


def test_the_gates_defaults_are_the_configurations(monkeypatch):
    """One owner of the two numbers, read when a settings object is built and
    not bound at import, so a gate built with no settings and one built off
    the file agree, and a changed default is seen without a reload."""
    assert GateSettings() == GateSettings(
        min_interval_s=config.DEFAULT_PROVIDER_MIN_INTERVAL_S,
        cooldown_s=config.DEFAULT_PROVIDER_COOLDOWN_S,
    )
    monkeypatch.setattr(config, "DEFAULT_PROVIDER_MIN_INTERVAL_S", 4.0)
    assert GateSettings().min_interval_s == 4.0


def test_the_playlist_read_lets_the_park_through(paths, clock):
    """The one catch in the catalogue that wrapped every exception; the
    sibling seam boundaries already passed a CratekitError through."""
    parked = trip(make_gate(paths, clock))

    class Client:
        def playlist(self, identifier: str) -> Any:
            raise parked

    with pytest.raises(jobs.Parked) as caught:
        tidal_catalogue.TidalCatalogue(Client()).playlist_for(
            "0f1e2d3c-4b5a-4968-8776-a5b4c3d2e1f0"
        )

    assert caught.value is parked


def test_process_spend_is_this_process_alone(paths, clock):
    before = provider_gate.process_spend()
    gate = make_gate(paths, clock)
    transport = Transport(rate_limited(), Response())

    send_through(gate, transport)
    send_through(gate, transport)

    assert provider_gate.process_spend().since(before) == Spend(calls=2, rate_limited=1)


def test_calls_another_process_made_are_not_reported_as_this_runs(installed, monkeypatch):
    """The shared file moves while this verb runs, as it does under a Relay
    sweep; the line reports what THIS process spent, one login."""
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    original = tidal_catalogue.open_catalogue

    def opening(cfg=None):
        opened = original(cfg)
        # Another process: forty calls written straight into the shared file.
        state_path = config.state_path(provider_gate.STATE_KEY)
        written = json.loads(state_path.read_text())
        written["calls"] += 40
        state_path.write_text(json.dumps(written))
        return opened

    monkeypatch.setattr(tidal_catalogue, "open_catalogue", opening)

    _, envelope = drive(["label", "harvest", "https://example.invalid/playlist/harvest"])

    assert _spend_warnings(envelope) == [
        "1 call to the streaming provider this run, none answered with a rate limit; "
        "1 on the account and none under Cratekit's app credentials"
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 7. The call ceiling, a line per command (U193)
# ═══════════════════════════════════════════════════════════════════════════

from cratekit.core.provider_gate import CALLS_ENV, CEILING  # noqa: E402


def ceiling_gate(paths, clock, ceiling: int) -> Gate:
    state, lock = paths
    return Gate(
        GateSettings(min_interval_s=1.0, cooldown_s=900.0, calls_per_command=ceiling),
        path=state,
        lock_path=lock,
        clock=clock,
        sleep=clock.sleep,
    )


def test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling(
    paths, clock
):
    gate = ceiling_gate(paths, clock, 3)
    transport = Transport()

    with provider_gate.command() as scope:
        for _ in range(3):
            send_through(gate, transport)
        with pytest.raises(jobs.Parked) as caught:
            send_through(gate, transport)
        spent = scope.spent()

    assert len(transport.calls) == 3, "the call past the ceiling was sent"
    assert spent == 3
    cause = caught.value.cause
    assert cause.reason == CEILING
    assert cause.detail["calls"] == 3 and cause.detail["ceiling"] == 3
    assert cause.detail["raised"] is False
    assert "made 3 calls" in cause.message
    assert "[provider] calls_per_command" in cause.message
    assert scope.stopped is cause
    assert gate.spend().calls == 3, "the refused call was counted"


def test_the_stop_is_remembered_so_a_swallowing_tool_still_parks(paths, clock):
    """The vendored downloader catches every exception inside its calls, so
    the ceiling must come out of ``raise_if_parked`` like a trip does."""
    gate = ceiling_gate(paths, clock, 1)
    transport = Transport()

    with provider_gate.command():
        send_through(gate, transport)
        try:
            send_through(gate, transport)
        except CratekitError:
            pass  # what the tool does with it
        with pytest.raises(jobs.Parked) as caught:
            gate.raise_if_parked()

    assert caught.value.cause.reason == CEILING


def test_outside_a_command_nothing_is_capped(paths, clock):
    gate = ceiling_gate(paths, clock, 2)
    transport = Transport()

    for _ in range(5):
        send_through(gate, transport)

    assert len(transport.calls) == 5


def test_a_command_is_charged_only_for_its_own_calls(paths, clock):
    gate = ceiling_gate(paths, clock, 2)
    transport = Transport()
    for _ in range(4):
        send_through(gate, transport)

    with provider_gate.command():
        send_through(gate, transport)
        send_through(gate, transport)
        with pytest.raises(jobs.Parked):
            send_through(gate, transport)

    assert len(transport.calls) == 6


def test_a_nested_dispatch_keeps_the_outer_commands_count(paths, clock):
    """``run decide --continue`` dispatches the verb again in the same process;
    a fresh count there would let one command spend its ceiling twice."""
    gate = ceiling_gate(paths, clock, 2)
    transport = Transport()

    with provider_gate.command() as outer:
        send_through(gate, transport)
        with provider_gate.command(calls=50) as inner:
            assert inner is outer
            send_through(gate, transport)
            with pytest.raises(jobs.Parked):
                send_through(gate, transport)

    assert len(transport.calls) == 2


def test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one(
    paths, clock, monkeypatch
):
    monkeypatch.delenv(CALLS_ENV, raising=False)
    gate = ceiling_gate(paths, clock, 2)
    transport = Transport()

    with provider_gate.command(calls=5) as scope:
        assert os.environ[CALLS_ENV] == "5", "a job's detached child would not see it"
        assert provider_gate.ceiling(gate.settings) == 5
        for _ in range(5):
            send_through(gate, transport)
        with pytest.raises(jobs.Parked) as caught:
            send_through(gate, transport)
    assert scope.spent() == 5
    assert caught.value.cause.detail["raised"] is True
    assert "--calls" in caught.value.cause.message
    assert CALLS_ENV not in os.environ, "the raised ceiling outlived its run"

    with provider_gate.command():
        assert provider_gate.ceiling(gate.settings) == 2
        send_through(gate, transport)
        send_through(gate, transport)
        with pytest.raises(jobs.Parked):
            send_through(gate, transport)

    assert len(transport.calls) == 7


def test_a_raised_ceiling_restores_a_variable_the_shell_already_held(monkeypatch):
    monkeypatch.setenv(CALLS_ENV, "900")
    with provider_gate.command(calls=40) as scope:
        assert scope.raised == 40
        assert os.environ[CALLS_ENV] == "40"
    assert os.environ[CALLS_ENV] == "900"


@pytest.mark.parametrize(
    ("value", "raised"),
    [("700", 700), ("0", None), ("-3", None), ("abc", None), ("1.5", None), ("", None), ("²", None)],
)
def test_a_detached_child_reads_the_raised_ceiling_off_the_environment(
    monkeypatch, value, raised
):
    """A job's child is a fresh process and a fresh scope. A value that is not a
    positive whole number leaves the configured ceiling, the lower one, in place."""
    monkeypatch.setenv(CALLS_ENV, value)
    with provider_gate.command() as scope:
        assert scope.raised == raised
        assert provider_gate.ceiling(GateSettings(calls_per_command=3)) == (raised or 3)


def test_the_ceiling_parks_a_job_and_the_resumed_job_continues(paths, clock, queue, cfg):
    """Three items, two calls each, a ceiling of three. The first item is done,
    the second stops part way and goes back to pending, the job is blocked and
    names itself, and the next run, a fresh command under the raised ceiling
    the refusal names, finishes the job."""
    store, root = queue
    gate = ceiling_gate(paths, clock, 3)
    transport = Transport()
    job = jobs.enqueue(
        store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a", "b", "c"]
    )

    def handle(_job, item):
        send_through(gate, transport)
        send_through(gate, transport)
        return None

    with provider_gate.command():
        first = jobs.drive(store, job.job_id, handle, root=root)

    assert first.job.state is jobs.JobState.BLOCKED
    assert first.job.cause is not None and first.job.cause.reason == CEILING
    assert first.job.cause.detail["job_id"] == job.job_id
    # What ``job show`` reads when a detached child stopped: the resume form.
    assert "crate --calls 6 job resume JOB_ID" in first.job.cause.remediation.steps[0]
    assert len(transport.calls) == 3
    states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states == {
        "a": jobs.ItemState.DONE,
        "b": jobs.ItemState.PENDING,
        "c": jobs.ItemState.PENDING,
    }

    # The resume the refusal names raises the ceiling for its run; the two
    # items left take four calls, one past the configured three.
    with provider_gate.command(calls=first.job.cause.detail["higher"]):
        second = jobs.drive(store, job.job_id, handle, root=root)

    assert second.job.state is jobs.JobState.SUCCEEDED
    assert len(transport.calls) == 7


def test_a_park_that_names_its_job_keeps_its_own_job_id(paths, clock, queue, cfg):
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])
    from cratekit.core.cause import Cause, Remediation  # noqa: PLC0415

    def handle(_job, _item):
        raise jobs.Parked(
            Cause(
                reason=COOLDOWN,
                message="held",
                remediation=Remediation(remedy=jobs.Remedy.RETRY_LATER),
                detail={"job_id": "another"},
            )
        )

    result = jobs.drive(store, job.job_id, handle, root=root)

    assert result.job.cause.detail["job_id"] == "another"


def test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted(paths, clock):
    """The vendored downloader fetches media segments through a session of its
    own, never the client's transport; those are not provider calls and a
    command at its ceiling still fetches them."""
    gate = ceiling_gate(paths, clock, 1)
    client = SimpleNamespace(request_session=Transport())
    assert gate.attach(client)

    class _Segments(requests.adapters.BaseAdapter):
        def send(self, request, **kwargs):
            answer = requests.Response()
            answer.status_code = 200
            answer._content = b"segment"
            answer.request = request
            return answer

        def close(self):
            pass

    with provider_gate.command() as scope:
        client.request_session.request("GET", "https://api.invalid/track")
        with requests.Session() as segments:
            segments.mount("https://", _Segments())
            fetched = [segments.get(f"https://cdn.invalid/{n}").content for n in range(3)]
        with pytest.raises(jobs.Parked):
            client.request_session.request("GET", "https://api.invalid/next")

    assert fetched == [b"segment"] * 3
    assert scope.spent() == 1
    assert gate.calls == 1


def test_the_ceiling_defaults_to_five_hundred_and_round_trips(tmp_path):
    section = config.from_dict(_config_data(tmp_path)).provider
    assert section.calls_per_command == config.DEFAULT_PROVIDER_CALLS_PER_COMMAND == 500
    assert GateSettings().calls_per_command == 500

    built = config.from_dict(_config_data(tmp_path, provider={"calls_per_command": 2000}))
    config.save(built)
    config.reset_cache()
    assert GateSettings.from_config(config.load()).calls_per_command == 2000


@pytest.mark.parametrize("value", [0, -1, 1.5, True, "500"])
def test_a_ceiling_that_is_not_a_positive_whole_number_refuses_at_load(tmp_path, value):
    problems = config.validate(_config_data(tmp_path, provider={"calls_per_command": value}))
    assert len(problems) == 1
    assert "provider.calls_per_command" in problems[0]
    assert "no value that switches the ceiling off" in problems[0]
    with pytest.raises(config.ConfigError):
        config.from_dict(_config_data(tmp_path, provider={"calls_per_command": value}))


def test_the_ceiling_reason_is_declared_as_a_policy_refusal():
    assert REASONS[CEILING] is ExitCode.REFUSED_BY_POLICY


# ── through the real dispatcher ──────────────────────────────────────────


HARVEST = ["label", "harvest", "https://example.invalid/playlist/harvest"]


@pytest.fixture
def one_call(installed, tmp_path):
    """The installed machine with a ceiling of one call per command."""
    built = config.from_dict(
        _config_data(tmp_path, provider={"min_interval_s": 0.01, "calls_per_command": 1})
    )
    config.save(built)
    config.reset_cache()
    return built


def _two_more_calls(monkeypatch, client, *, swallow: bool = False) -> list[str]:
    """Two calls beyond the login, as the catalogue would make; ``swallow``
    catches the stop the way a verb that walks a list per item might."""
    original = tidal_catalogue.open_catalogue
    caught: list[str] = []

    def opening(cfg=None):
        opened = original(cfg)
        for path in ("a", "b"):
            try:
                client.request_session.request("GET", f"https://api.invalid/{path}")
            except CratekitError as exc:
                if not swallow:
                    raise
                caught.append(exc.cause.reason)
        return opened

    monkeypatch.setattr(tidal_catalogue, "open_catalogue", opening)
    return caught


def test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues(
    one_call, monkeypatch
):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    _two_more_calls(monkeypatch, client)

    code, envelope = drive(HARVEST)

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["outcome"] == "blocked"
    cause = envelope["cause"]
    assert cause["reason"] == CEILING
    assert len(client.request_session.calls) == 1, "a call past the ceiling was sent"
    # ``drive`` asks for the json envelope, and the global options are kept.
    expected = "crate --output json --calls 2 " + " ".join(HARVEST)
    assert cause["detail"]["continue"] == expected
    assert cause["remediation"]["steps"][0].endswith(expected)
    said = [w for w in envelope.get("warnings", ()) if w.get("code") == CEILING]
    assert said == [], "the refusal already says the stop; a warning says it twice"


def test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling(
    one_call, monkeypatch
):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    _two_more_calls(monkeypatch, client)

    _, raised = drive(["--calls", "3", *HARVEST])
    assert (raised.get("cause") or {}).get("reason") != CEILING, raised
    assert len(client.request_session.calls) == 3

    _, again = drive(HARVEST)
    assert again["cause"]["reason"] == CEILING
    assert len(client.request_session.calls) == 4
    assert CALLS_ENV not in os.environ


def test_the_continue_command_replaces_a_calls_already_given(one_call, monkeypatch):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    _two_more_calls(monkeypatch, client)

    _, envelope = drive(["--calls=2", *HARVEST])

    assert envelope["cause"]["detail"]["continue"] == (
        "crate --output json --calls 4 " + " ".join(HARVEST)
    )


def test_the_continue_command_replaces_a_spaced_calls_already_given(one_call, monkeypatch):
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    _two_more_calls(monkeypatch, client)

    _, envelope = drive(["--calls", "2", *HARVEST])

    assert len(client.request_session.calls) == 2
    assert envelope["cause"]["detail"]["continue"] == (
        "crate --output json --calls 4 " + " ".join(HARVEST)
    )


@pytest.mark.parametrize("value", ["0", "-2", "many"])
def test_a_calls_that_is_not_a_positive_whole_number_is_a_usage_error(value, capsys):
    out, err = io.StringIO(), io.StringIO()
    assert cli.run(["--calls", value, *HARVEST], stdout=out, stderr=err) == int(ExitCode.USAGE)
    assert "positive whole number" in capsys.readouterr().err


def test_a_ceiling_stop_a_verb_swallowed_is_still_said(one_call, monkeypatch):
    """A verb that catches the park per item and answers would otherwise show a
    report over reads the ceiling stopped."""
    client = _LoginClient()
    monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
    _record_session()
    caught = _two_more_calls(monkeypatch, client, swallow=True)

    _, envelope = drive(HARVEST)

    assert caught == [CEILING, CEILING]
    said = [w["message"] for w in envelope.get("warnings", ()) if w.get("code") == CEILING]
    assert len(said) == 1, envelope
    assert "was not read from the provider" in said[0]
    assert "crate --output json --calls 2 " + " ".join(HARVEST) in said[0]


def test_the_continue_command_for_a_job_resumes_that_job():
    from cratekit.cli import continue_command  # noqa: PLC0415
    from cratekit.cli.registry import landed_entries  # noqa: PLC0415
    from cratekit.core.cause import Cause, Remediation  # noqa: PLC0415

    entry = next(one for one in landed_entries() if one.name == "label.harvest")
    cause = Cause(
        reason=CEILING,
        message="stopped",
        remediation=Remediation(remedy=jobs.Remedy.FIX_COMMAND_LINE),
        detail={"ceiling": 500, "higher": 1000, "job_id": "2026-11-02T00:00:00Z-ab12"},
    )

    assert continue_command(HARVEST, entry, cause) == (
        "crate --calls 1000 job resume 2026-11-02T00:00:00Z-ab12"
    )


def test_the_continue_command_names_the_run_a_stopped_write_recorded_its_steps_under():
    """U210. A cause naming its run continues THAT run, once, whatever the command line held."""
    from cratekit.cli import continue_command  # noqa: PLC0415
    from cratekit.cli.registry import landed_entries  # noqa: PLC0415
    from cratekit.core.cause import Cause, Remediation  # noqa: PLC0415

    entry = next(one for one in landed_entries() if one.name == "sync.pair")
    cause = Cause(
        reason=CEILING,
        message="stopped",
        remediation=Remediation(remedy=jobs.Remedy.FIX_COMMAND_LINE),
        detail={"ceiling": 5000, "higher": 6000, "run_id": "run-7"},
    )

    assert continue_command(["sync", "pair"], entry, cause) == (
        "crate --run run-7 --calls 6000 sync pair"
    )
    assert continue_command(["--run", "run-7", "sync", "pair"], entry, cause) == (
        "crate --run run-7 --calls 6000 sync pair"
    )
    assert continue_command(["--run=run-7", "--calls", "10", "sync", "pair"], entry, cause) == (
        "crate --run=run-7 --calls 6000 sync pair"
    )


def test_the_continue_command_of_a_run_that_cannot_be_continued_starts_a_new_one():
    """U210. A write that recorded no steps is named without its run."""
    from cratekit.cli import continue_command  # noqa: PLC0415
    from cratekit.cli.registry import landed_entries  # noqa: PLC0415
    from cratekit.core.cause import Cause, Remediation  # noqa: PLC0415

    entry = next(one for one in landed_entries() if one.name == "sync.pair")
    cause = Cause(
        reason=CEILING,
        message="stopped",
        remediation=Remediation(remedy=jobs.Remedy.FIX_COMMAND_LINE),
        detail={"ceiling": 5000, "higher": 10000, "fresh": True},
    )
    assert continue_command(["--run", "run-7", "sync", "pair"], entry, cause) == (
        "crate --calls 10000 sync pair"
    )
    assert continue_command(["--run=run-7", "sync", "pair"], entry, cause) == (
        "crate --calls 10000 sync pair"
    )
