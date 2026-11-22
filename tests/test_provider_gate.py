"""R-705: one gate for every call to the streaming provider.

1. Pacing holds the configured interval, measured from the last call any
   process made, and a ``Retry-After`` holds the next call at least that long.
2. The breaker trips on a rate limit that survives the ladder, as the job
   engine's own park, with the rest of a sweep pending.
3. The cooldown outlives the process.
4. One driver at a time: two real processes never overlap and keep the
   interval, read off the gate's stamps and an ``O_EXCL`` marker (R-759).
5. Spend is counted across processes. 6. Only the two build sites build a
   client, and both attach the gate. 7. The call ceiling per command (U193).

Schedules run on a fake clock whose ``sleep`` advances it. The two process
tests use the real clock and real sleeps, since a kernel lock cannot be faked.
"""

from __future__ import annotations

import fcntl
import io
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from email.utils import formatdate
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import requests
from requests.structures import CaseInsensitiveDict

from cratekit import cli
from cratekit.acquire import adapter as adapter_module
from cratekit.acquire import download, listing, provider_session, vendored
from cratekit.acquire.adapter import AdapterSettings, Offer, TrackOutcome, TrackRequest
from cratekit.cli import PROVIDER_SPEND, continue_command
from cratekit.cli.registry import landed_entries
from cratekit.core import config, jobs, provider_gate, secrets
from cratekit.core.cause import REASONS, Cause, CratekitError, Remediation
from cratekit.core.exit_codes import ExitCode
from cratekit.core.provider_gate import (
    BUDGET,
    CALLS_ENV,
    CEILING,
    COOLDOWN,
    HELD,
    LOCK_WAIT_S,
    TRIP_AFTER,
    Gate,
    GateSettings,
    Spend,
)
from cratekit.label import catalogue, tidal_catalogue
from cratekit.modules.outbound import account, tidal_account
from tests.cli_drive import drive

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
_START = 1_700_000_000.0


# ── Doubles ──────────────────────────────────────────────────────────────

class Clock:
    """A wall clock that moves only when something sleeps on it."""

    def __init__(self, start: float = _START) -> None:
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
    """What the client raises off a 429, so the ladder needs no provider library."""


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
    calls_per_command: int | None = None,
) -> Gate:
    extra = {} if calls_per_command is None else {"calls_per_command": calls_per_command}
    settings = GateSettings(min_interval_s=min_interval_s, cooldown_s=cooldown_s, **extra)
    return Gate(settings, path=paths[0], lock_path=paths[1], clock=clock, sleep=clock.sleep)


def ceiling_gate(paths, clock, ceiling: int) -> Gate:
    return make_gate(paths, clock, calls_per_command=ceiling)


def send_through(gate: Gate, transport: Transport, url: str = "https://api.invalid/x") -> Any:
    return gate.call(lambda: transport.request("GET", url))


def trip(gate: Gate, transport: Transport | None = None) -> CratekitError:
    """Drive the breaker to its trip and return the refusal it raised."""
    transport = transport or Transport(rate_limited())
    with pytest.raises(CratekitError) as caught:
        for _ in range(TRIP_AFTER):
            send_through(gate, transport)
    return caught.value


def parked(action) -> str:
    """Run ``action``, which must raise the gate's park; return its reason."""
    with pytest.raises(jobs.Parked) as caught:
        action()
    return caught.value.cause.reason


def written(paths) -> dict[str, Any]:
    return json.loads(paths[0].read_text())


def hold_lock(lock: Path) -> int:
    lock.parent.mkdir(parents=True, exist_ok=True)
    holder = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(holder, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return holder


# ── 1. Pacing ────────────────────────────────────────────────────────────

def test_consecutive_calls_wait_out_the_interval(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport()
    for _ in range(3):
        send_through(gate, transport)
    # The first call sleeps nothing; each later one the whole interval.
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
    """``[provider] min_interval_s`` off the frozen configuration, not a constant."""
    cfg = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 2.5}))
    settings = GateSettings.from_config(cfg)
    gate = Gate(settings, path=paths[0], lock_path=paths[1], clock=clock, sleep=clock.sleep)
    transport = Transport()
    send_through(gate, transport)
    send_through(gate, transport)
    assert settings.min_interval_s == 2.5
    assert clock.slept == [2.5]


def test_the_interval_is_measured_from_the_last_call_by_any_gate(paths, clock):
    """Two gates over one state file, as two processes are, share one last call."""
    first = make_gate(paths, clock, min_interval_s=1.0)
    second = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport()
    send_through(first, transport)
    send_through(second, transport)
    assert clock.slept == [1.0]


@pytest.mark.parametrize(
    ("retry_after", "slept"),
    [
        ("7", 7.0),
        (formatdate(_START + 30.0, usegmt=True), 30.0),
        ("0.2", 1.0),
        ("soon", 1.0),
    ],
    ids=["seconds-hold-the-next-call", "http-date-honoured", "shorter-keeps-the-interval",
         "unreadable-is-zero"],
)
def test_a_retry_after_holds_the_next_call_at_least_that_long(paths, clock, retry_after, slept):
    """Never shorter than the interval, and an unreadable value is zero, not a guess."""
    gate = make_gate(paths, clock, min_interval_s=1.0)
    transport = Transport(rate_limited(retry_after), Response())
    send_through(gate, transport)
    send_through(gate, transport)
    assert clock.slept == [slept]


# ── 2. The breaker ───────────────────────────────────────────────────────

def test_the_trip_count_is_one_spent_ladder():
    """The gate cannot import the ladder: an initial attempt plus every retry."""
    assert TRIP_AFTER == listing.DEFAULT_MAX_RETRIES + 1


def test_the_sixth_consecutive_rate_limit_answer_trips_and_records_the_cooldown(paths, clock):
    gate = make_gate(paths, clock, min_interval_s=1.0, cooldown_s=900.0)
    transport = Transport(rate_limited())
    refused = trip(gate, transport)
    assert len(transport.calls) == TRIP_AFTER, "the trip came before or after the ladder"
    assert refused.cause.reason == COOLDOWN
    assert refused.cause.retryable is False, "an automatic retry into a cooldown is the harm"
    state = written(paths)
    assert state["tripped_at"] == clock.now
    assert state["lifts_at"] == clock.now + 900.0
    assert state["trips"] == 1
    assert refused.cause.detail["lifts_at"] == provider_gate._iso(clock.now + 900.0)
    assert refused.cause.detail["remaining_s"] == 900


def test_the_trip_is_the_job_engines_own_park(paths, clock):
    """Raised as ``Parked`` so the engine releases the item and claims nothing further."""
    assert isinstance(trip(make_gate(paths, clock)), jobs.Parked)


def test_a_success_breaks_the_run_of_rate_limit_answers(paths, clock):
    gate = make_gate(paths, clock)
    five = [rate_limited()] * (TRIP_AFTER - 1)
    transport = Transport(*five, Response(), *five, Response())
    for _ in range(2 * TRIP_AFTER):
        send_through(gate, transport)
    assert len(transport.calls) == 2 * TRIP_AFTER
    assert written(paths)["tripped_at"] is None


@pytest.mark.parametrize(
    ("retry_after", "lifts_after"),
    [("900", 900.0), ("3600", 3600.0)],
    ids=["at-the-cooldown", "longer-than-the-cooldown"],
)
def test_a_retry_after_at_or_above_the_cooldown_trips_at_once(paths, clock, retry_after, lifts_after):
    """Not waited for six times, and a longer one sets the lift time."""
    gate = make_gate(paths, clock, cooldown_s=900.0)
    transport = Transport(rate_limited(retry_after))
    with pytest.raises(CratekitError) as caught:
        send_through(gate, transport)
    assert len(transport.calls) == 1
    assert caught.value.cause.reason == COOLDOWN
    assert written(paths)["lifts_at"] == clock.now + lifts_after


def _paged(gate: Gate, transport: Transport):
    def page(limit: int, offset: int) -> Any:
        answer = send_through(gate, transport)
        if answer.status_code == 429:
            raise TooManyRequests("Too many requests")
        return answer

    return page


def test_a_spent_ladder_through_the_gate_comes_out_as_the_park(paths, clock):
    """What the ladder re-raises is the park, not the provider's error; no seventh call."""
    transport = Transport(rate_limited())
    with pytest.raises(jobs.Parked) as caught:
        listing.fetch_with_retry(
            _paged(make_gate(paths, clock), transport), limit=10, offset=0, sleep=clock.sleep
        )
    assert caught.value.cause.reason == COOLDOWN
    assert len(transport.calls) == TRIP_AFTER


def test_an_exception_out_of_send_is_a_call_and_not_a_rate_limit_answer(paths, clock):
    gate = make_gate(paths, clock)
    transport = Transport(rate_limited(), ConnectionError("reset"), rate_limited())
    send_through(gate, transport)
    with pytest.raises(ConnectionError):
        send_through(gate, transport)
    send_through(gate, transport)
    state = written(paths)
    assert (state["calls"], state["rate_limited"], state["consecutive"]) == (3, 2, 2)


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


def _item_states(store, job) -> dict[str, Any]:
    return {item.item_id: item.state for item in jobs.items(store, job.job_id)}


def test_the_breaker_stops_a_sweep_at_the_first_surviving_rate_limit_with_the_rest_pending(
    paths, clock, queue, cfg
):
    """The first label's ladder trips the gate; the job blocks with all three
    items pending and the second label is never claimed."""
    store, root = queue
    transport = Transport(rate_limited())
    page = _paged(make_gate(paths, clock), transport)
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=list("abc"))
    claimed: list[str] = []

    def handle(_job, item):
        claimed.append(item.item_id)
        listing.fetch_with_retry(page, limit=10, offset=0, sleep=clock.sleep)

    result = jobs.drive(store, job.job_id, handle, root=root)
    assert claimed == ["a"], "the driver claimed past the trip"
    assert len(transport.calls) == TRIP_AFTER
    assert result.job.state is jobs.JobState.BLOCKED
    assert result.job.cause is not None and result.job.cause.reason == COOLDOWN
    assert _item_states(store, job) == {name: jobs.ItemState.PENDING for name in "abc"}


# ── 3. The cooldown outlives the process ─────────────────────────────────

def test_inside_the_cooldown_assert_open_refuses_naming_the_lift_time(paths, clock):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    trip(gate)
    lifts = provider_gate._iso(clock.now + 900.0)
    clock.now += 100.0
    with pytest.raises(jobs.Parked) as caught:
        gate.assert_open()
    cause = caught.value.cause
    assert cause.reason == COOLDOWN
    assert cause.detail["lifts_at"] == lifts
    assert cause.detail["remaining_s"] == 800
    assert lifts in cause.message
    assert "800 seconds" in cause.message
    assert any(lifts in step for step in cause.remediation.steps)


@pytest.mark.parametrize(
    ("after", "sent"), [(0.0, 0), (900.0, 1)],
    ids=["inside-a-call-is-refused-before-it-is-sent", "lifted-calls-go-through-again"],
)
def test_the_cooldown_refuses_a_call_until_it_lifts(paths, clock, after, sent):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    trip(gate)
    clock.now += after
    transport = Transport()
    if sent:
        gate.assert_open()
        send_through(gate, transport)
    else:
        parked(lambda: send_through(gate, transport))
    assert len(transport.calls) == sent


def _child(script: Path, *args: Any) -> dict[str, Any]:
    env = dict(os.environ, PYTHONPATH=str(SRC_ROOT), PYTHONDONTWRITEBYTECODE="1")
    return {"args": [sys.executable, str(script), *map(str, args)], "env": env, "text": True,
            "stdout": subprocess.PIPE, "stderr": subprocess.PIPE}


def _run_child(script: Path, *args: Any) -> str:
    done = subprocess.run(**_child(script, *args), timeout=60, check=False)
    assert done.returncode == 0, done.stderr
    return done.stdout


_SECOND_PROCESS = """
import json, sys
from pathlib import Path
from cratekit.core.cause import CratekitError
from cratekit.core.provider_gate import Gate, GateSettings

state, lock = Path(sys.argv[1]), Path(sys.argv[2])
gate = Gate(GateSettings(), path=state, lock_path=lock)
sent, report = [], {}
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


def test_a_cooldown_written_by_one_process_refuses_a_verb_started_in_another(paths, tmp_path):
    """A REAL second process refuses before any call, naming the lift time. The
    trip runs on a fake clock set to the real time, so its waits pass at once."""
    state, lock = paths
    clock = Clock(time.time())
    trip(make_gate(paths, clock, cooldown_s=900.0))
    lifts = json.loads(state.read_text())["lifts_at"]
    script = tmp_path / "second_process.py"
    script.write_text(_SECOND_PROCESS)
    report = json.loads(_run_child(script, state, lock))
    assert report["sent"] == 0, "the second process reached the provider"
    assert report["open"]["reason"] == COOLDOWN
    assert report["call"]["reason"] == COOLDOWN
    assert report["open"]["detail"]["lifts_at"] == provider_gate._iso(lifts)


# ── 4. One driver at a time ──────────────────────────────────────────────

#: One driver for both process tests. It waits at a barrier for the other,
#: then calls through one real gate, recording in each send the ``last_call``
#: stamp the gate just wrote, the wall clock, and whether another send held
#: the ``O_EXCL`` in flight marker.
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

#: How far a send may begin BEFORE its own stamp: the gate sleeps on the
#: monotonic clock and stamps with the wall clock. Load only makes sends later.
_CLOCK_SKEW_S = 0.001


def _drive_two_processes(
    paths: tuple[Path, Path], tmp_path: Path, *, count: int, interval: float, hold: float
) -> list[dict[str, Any]]:
    """Run two drivers over one gate and return what each recorded; a driver
    still running on the way out is killed so it cannot hold the lock."""
    state, lock = paths
    script = tmp_path / "driver.py"
    script.write_text(_DRIVER)
    marker = tmp_path / "in_flight"
    barrier = tmp_path / "barrier"
    barrier.mkdir()
    outs = [tmp_path / "a.json", tmp_path / "b.json"]
    children = [
        subprocess.Popen(**_child(script, state, lock, out, marker, barrier, count, interval, hold))
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
    """Every stamp is at least the interval after the one before, and no send
    begins before its own stamp. R-759: stamps, never send times measured here."""
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
    """Each call holds the provider ten times the interval, so only the lock
    keeps two sends apart. The verdict reads no clock."""
    reports = _drive_two_processes(paths, tmp_path, count=4, interval=0.01, hold=0.1)
    assert [report["overlaps"] for report in reports] == [0, 0], (
        f"two calls were in flight at once: {reports}"
    )


def test_a_lock_held_past_the_wait_is_refused_with_the_holder_named(paths, clock):
    """The wait is polled on the fake clock, so the refusal comes without a hang."""
    gate = make_gate(paths, clock)
    holder = hold_lock(paths[1])
    transport = Transport()
    try:
        with pytest.raises(jobs.Parked) as caught:
            send_through(gate, transport)
    finally:
        os.close(holder)
    assert caught.value.cause.reason == HELD
    assert caught.value.cause.retryable is False, "a held account is not a track to retry"
    assert transport.calls == []
    # The limit is the wait plus one interval, to within one poll.
    assert sum(clock.slept) >= LOCK_WAIT_S + 1.0 - provider_gate.LOCK_POLL_S


def test_the_lock_file_is_never_unlinked(paths, clock):
    """Unlinking on release is how two holders come to hold one lock."""
    lock = paths[1]
    gate = make_gate(paths, clock)
    send_through(gate, Transport())
    first = lock.stat().st_ino
    send_through(gate, Transport())
    assert lock.exists() and lock.stat().st_ino == first


def test_a_wait_the_provider_asked_for_is_taken_with_the_lock_released(paths, clock):
    """A Retry-After past the interval is slept OUTSIDE the lock; one interval
    is slept under it. The sleep probes the lock and records whether it got it."""
    lock = paths[1]
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
    for _ in range(3):
        send_through(gate, transport)
    assert taken_while_sleeping == [(300.0, True), (1.0, False)]
    assert len(transport.calls) == 3


# ── 5. Spend ─────────────────────────────────────────────────────────────

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
    gate.call(lambda: seen.append(written(paths)["calls"]) or Response())
    assert seen == [1]


def test_a_corrupt_state_file_reads_as_fresh_rather_than_locking_the_provider_out(paths, clock):
    state, _ = paths
    state.parent.mkdir(parents=True)
    state.write_text("{not json")
    send_through(make_gate(paths, clock), Transport())
    assert json.loads(state.read_text())["calls"] == 1


def test_process_spend_is_this_process_alone(paths, clock):
    before = provider_gate.process_spend()
    gate = make_gate(paths, clock)
    transport = Transport(rate_limited(), Response())
    send_through(gate, transport)
    send_through(gate, transport)
    assert provider_gate.process_spend().since(before) == Spend(calls=2, rate_limited=1)


def test_one_offered_release_costs_two_calls_on_the_catalogue():
    """The figure docs/mutation/r705-notes.md stands on, measured on the tree's
    own ``release_tracks``: one album read and one page of its tracks."""
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


# ── 6. The seam ──────────────────────────────────────────────────────────

class _Answering(requests.adapters.BaseAdapter):
    """An adapter for a real ``requests.Session`` that answers every request
    with one status and records it, so the wrap is proven on the real object."""

    def __init__(self, status: int, content: bytes = b"") -> None:
        super().__init__()
        self.status, self.content = status, content
        self.seen: list[str] = []

    def send(self, request, **kwargs):  # noqa: ANN001 - the base class signature
        self.seen.append(f"{request.method} {request.url}")
        answer = requests.Response()
        answer.status_code = self.status
        answer.headers = CaseInsensitiveDict()
        answer.url = request.url
        answer.request = request
        answer._content = self.content
        return answer

    def close(self) -> None:
        pass


def test_attach_routes_every_request_of_a_real_session_through_the_gate_once(paths, clock):
    """``get`` and ``post`` both land in ``request``; attaching twice wraps once."""
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
    """Both attach the gate; a third site would be a caller the gate cannot see."""
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
    state, lock = (config.state_path(k) for k in (provider_gate.STATE_KEY, provider_gate.LOCK_KEY))
    assert state.parent == lock.parent


# ── The configuration ────────────────────────────────────────────────────

def _config_data(tmp_path: Path, **overrides: Any) -> dict[str, Any]:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = {
        "schema_version": config.CURRENT_SCHEMA_VERSION,
        "library": {"root": str(root), "volume_id": "F1E2-D3C4", "db_path": str(root / "db" / "master.db")},
        "paths": {"download_staging": str(tmp_path / "staging")},
        "profile": {"name": "full"},
    }
    data.update(overrides)
    return data


def _save(tmp_path: Path, **provider: Any) -> config.Config:
    built = config.from_dict(_config_data(tmp_path, provider=provider))
    config.save(built)
    config.reset_cache()
    return built


def test_the_provider_defaults_are_conservative_and_named(tmp_path):
    section = config.from_dict(_config_data(tmp_path)).provider
    assert section.min_interval_s == config.DEFAULT_PROVIDER_MIN_INTERVAL_S == 1.0
    assert section.cooldown_s == config.DEFAULT_PROVIDER_COOLDOWN_S == 900
    assert GateSettings() == GateSettings.from_config(config.from_dict(_config_data(tmp_path)))


def test_the_provider_section_round_trips_through_the_file(tmp_path):
    built = _save(tmp_path, min_interval_s=0.5, cooldown_s=1800)
    again = config.load()
    assert again.provider == built.provider
    assert GateSettings.from_config(again) == GateSettings(min_interval_s=0.5, cooldown_s=1800.0)


def test_the_gates_defaults_are_the_configurations(monkeypatch):
    """One owner of the two numbers, read when settings are built, not at import."""
    assert GateSettings() == GateSettings(
        min_interval_s=config.DEFAULT_PROVIDER_MIN_INTERVAL_S,
        cooldown_s=config.DEFAULT_PROVIDER_COOLDOWN_S,
    )
    monkeypatch.setattr(config, "DEFAULT_PROVIDER_MIN_INTERVAL_S", 4.0)
    assert GateSettings().min_interval_s == 4.0


_BAD = {
    "min_interval_s": ([0, -1, 0.0, True, "1", float("nan"), float("inf")],
                       "no value that switches pacing off"),
    "cooldown_s": ([0, -5, 1.5, True, "900"], None),
    "calls_per_command": ([0, -1, 1.5, True, "500"], "no value that switches the ceiling off"),
}


@pytest.mark.parametrize(
    ("key", "value", "phrase"),
    [(key, value, phrase) for key, (values, phrase) in _BAD.items() for value in values],
    ids=[f"{key}={value!r}" for key, (values, _) in _BAD.items() for value in values],
)
def test_a_provider_number_that_is_not_positive_is_refused_naming_the_key(tmp_path, key, value, phrase):
    """A non positive interval, or a cooldown or ceiling that is not a positive
    whole number, is one problem naming the key, refused at load."""
    data = _config_data(tmp_path, provider={key: value})
    problems = config.validate(data)
    assert len(problems) == 1
    assert f"provider.{key}" in problems[0]
    if phrase:
        assert phrase in problems[0]
    with pytest.raises(config.ConfigError):
        config.from_dict(data)


def test_an_absent_provider_section_is_not_a_problem(tmp_path):
    assert config.validate(_config_data(tmp_path, provider={})) == []
    assert config.validate(_config_data(tmp_path)) == []


# ── The seams: every client build site asks the gate and attaches it ─────

STORED = {
    "token_type": "Bearer", "access_token": "FAKE-value-1",
    "refresh_token": "FAKE-value-2", "expiry_time": 946684800.0,
}


class _LoginClient:
    """A provider client whose login goes out through its transport, as the
    real one's does, so the wrap is proven to cover the login itself."""

    def __init__(self, transport: Transport | None = None) -> None:
        self.request_session = transport or Transport()
        self.token_type = self.access_token = self.refresh_token = self.expiry_time = None

    def load_oauth_session(self, token_type, access_token, refresh_token=None, expiry_time=None, is_pkce=False):
        self.request_session.request("POST", "https://auth.invalid/token")
        self.token_type, self.access_token = token_type, access_token
        self.refresh_token, self.expiry_time = refresh_token, expiry_time
        return True


def _record_session() -> None:
    secrets.set_json(secrets.Credential.PROVIDER_SESSION, dict(STORED))


@pytest.fixture
def login(monkeypatch):
    """Store a session and make the client factory hand out one fake client
    answering ``answers``; returns that client."""

    def make(*answers: Any) -> _LoginClient:
        client = _LoginClient(Transport(*answers))
        monkeypatch.setattr(provider_session, "CLIENT_FACTORY", lambda: client)
        _record_session()
        return client

    return make


def test_client_session_attaches_the_gate_before_the_login_goes_out(paths, clock, login):
    client = login()
    gate = make_gate(paths, clock)
    opened = provider_session.client_session(gate=gate)
    assert opened is client
    assert client.request_session._cratekit_gate is gate
    assert gate.calls == 1, "the login was not the first paced call"
    assert client.request_session.calls == [("POST", "https://auth.invalid/token")]


def test_client_session_refuses_inside_the_cooldown_before_building_a_client(paths, clock, monkeypatch):
    built: list[int] = []
    monkeypatch.setattr(
        provider_session, "CLIENT_FACTORY", lambda: built.append(1) or _LoginClient()
    )
    _record_session()
    gate = make_gate(paths, clock)
    trip(gate)
    assert parked(lambda: provider_session.client_session(gate=gate)) == COOLDOWN
    assert built == [], "a client was built inside the cooldown"


def test_client_session_with_no_gate_still_paces_at_the_defaults(login):
    """A caller that hands over nothing gets a gate, never a way past one."""
    client = login()
    provider_session.client_session()
    attached = client.request_session._cratekit_gate
    assert attached.settings == GateSettings()
    assert attached.path == config.state_path(provider_gate.STATE_KEY)


@pytest.mark.parametrize(
    ("module", "opener"),
    [(tidal_catalogue, "open_catalogue"), (tidal_account, "open_account")],
    ids=["catalogue", "account"],
)
def test_each_opener_paces_with_the_frozen_configuration(tmp_path, login, module, opener):
    client = login()
    cfg = config.from_dict(_config_data(tmp_path, provider={"min_interval_s": 3.0, "cooldown_s": 60}))
    getattr(module, opener)(cfg)
    assert client.request_session._cratekit_gate.settings == GateSettings(3.0, 60.0)


@pytest.mark.parametrize(
    ("module", "opener", "resolve", "returns"),
    [
        (tidal_catalogue, "open_catalogue", catalogue.resolve, None),
        (tidal_account, "open_account", account.resolve, object()),
    ],
    ids=["catalogue", "account"],
)
def test_resolve_hands_the_configuration_to_the_opener(tmp_path, monkeypatch, module, opener, resolve, returns):
    """``resolve`` used to discard its configuration; the gate needs it."""
    handed: list[Any] = []
    monkeypatch.setattr(module, opener, lambda cfg=None: handed.append(cfg) or returns)
    _record_session()
    cfg = config.from_dict(_config_data(tmp_path))
    resolve(cfg)
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
    source._gate = make_gate(paths, clock)  # the test's clock and paths
    return source


def _swallowing(action):
    """A downloader that runs ``action`` in ``item`` and, as the tool does,
    swallows any exception and answers "no file"."""

    class SwallowingDownload:
        def __init__(self, **_kwargs: Any) -> None:
            pass

        def item(self, **_kwargs: Any) -> tuple[bool, str]:
            try:
                action()
            except Exception:  # noqa: BLE001 - what the tool does
                pass
            return False, ""

    return SwallowingDownload


def test_the_vendored_adapter_attaches_the_gate_to_an_injected_session(tmp_path, paths, clock):
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)
    source.authenticate()
    source.offer(TrackRequest(key="x"))
    source.offer(TrackRequest(key="y"))
    assert session.request_session._cratekit_gate is source._gate
    assert source._gate.calls == 2
    assert clock.slept == [1.0]


def test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool(tmp_path, paths, clock):
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)
    trip(source._gate)
    assert parked(source.authenticate) == COOLDOWN
    assert session.request_session.calls == []


def test_a_rate_limited_login_comes_out_of_client_session_as_the_park(paths, clock, login):
    """Not an outage to wait out, nor a rejected session to log in again over."""
    login(rate_limited("900"))
    assert parked(lambda: provider_session.client_session(gate=make_gate(paths, clock))) == COOLDOWN


def test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park(tmp_path, paths, clock, monkeypatch):
    """Never a rejected session parked as credential-missing. The tool's two
    classes are the smallest doubles the real ``authenticate`` accepts."""
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
            # As the real tool: every exception in the login is an answer of False.
            try:
                self.session.request_session.request("POST", "https://auth.invalid/token")
            except Exception:  # noqa: BLE001 - the tool's own shape
                return False
            return True

    monkeypatch.setattr(tool_config, "Settings", Settings)
    monkeypatch.setattr(tool_config, "Tidal", Tidal)
    assert parked(source.authenticate) == COOLDOWN
    assert session.request_session._cratekit_gate is gate
    assert (gate.calls, gate.rate_limited) == (1, 1)


def test_a_trip_the_tool_swallowed_during_a_download_comes_out_of_fetch_as_the_park(tmp_path, paths, clock):
    """``fetch`` asks the gate again after the tool returns, so the track goes
    back to pending rather than failing."""
    source = _vendored(tmp_path, paths, clock, session=_ToolSession())
    source.authenticate()
    source._downloader = _swallowing(lambda: trip(source._gate))
    source._tidal = object()
    assert parked(lambda: source.fetch(TrackRequest(key="x"), tmp_path / "staging")) == COOLDOWN


def test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch(tmp_path, paths, clock):
    """The held refusal is a park too, swallowed and asked for again after."""
    session = _ToolSession()
    source = _vendored(tmp_path, paths, clock, session=session)
    source.authenticate()
    holder = hold_lock(paths[1])
    source._downloader = _swallowing(
        lambda: session.request_session.request("GET", "https://api.invalid/stream")
    )
    source._tidal = object()
    try:
        with pytest.raises(jobs.Parked) as caught:
            source.fetch(TrackRequest(key="x"), tmp_path / "staging")
    finally:
        os.close(holder)
    assert caught.value.cause.reason == HELD


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
def test_acquire_one_lets_the_park_through_rather_than_failing_the_track(tmp_path, paths, clock, at):
    """Both broad catches in ``acquire_one`` soften an exception; never the park."""
    parked = trip(make_gate(paths, clock))
    settings = AdapterSettings(download_staging=tmp_path / "staging")
    with pytest.raises(jobs.Parked) as caught:
        adapter_module.acquire_one(_TrippingSource(parked, at=at), TrackRequest(key="x"), settings)
    assert caught.value is parked


def test_acquire_one_still_softens_an_ordinary_failure(tmp_path):
    """A dead track is still one unavailable track and never the run."""
    settings = AdapterSettings(download_staging=tmp_path / "staging")
    source = _TrippingSource(RuntimeError("the provider had nothing"), at="offer")  # type: ignore[arg-type]
    result = adapter_module.acquire_one(source, TrackRequest(key="x"), settings)
    assert result.outcome is not TrackOutcome.ACQUIRED


def test_a_successful_call_clears_the_remembered_park(paths, clock):
    gate = make_gate(paths, clock, cooldown_s=900.0)
    trip(gate)
    clock.now += 900.0
    send_through(gate, Transport())
    gate.raise_if_parked()


def test_the_download_pacing_reads_retry_after_through_the_gates_parser(clock):
    """One parser of the header: the download probe reads what the gate reads."""
    reference = datetime.fromtimestamp(clock.now, tz=timezone.utc)
    for raw in ("45", formatdate(clock.now + 90.0, usegmt=True)):
        exc = RuntimeError("throttled")
        exc.response = SimpleNamespace(headers={"retry-after": raw})  # type: ignore[attr-defined]
        assert download.retry_hint_seconds(exc, now=reference) == provider_gate.retry_after_seconds(
            raw, clock.now
        )
    assert download._as_seconds("nonsense", reference) is None
    assert provider_gate.retry_after_seconds("nonsense", clock.now) is None


def test_the_playlist_read_lets_the_park_through(paths, clock):
    """The one catch in the catalogue that wrapped every exception."""
    parked = trip(make_gate(paths, clock))

    class Client:
        def playlist(self, identifier: str) -> Any:
            raise parked

    with pytest.raises(jobs.Parked) as caught:
        tidal_catalogue.TidalCatalogue(Client()).playlist_for(
            "0f1e2d3c-4b5a-4968-8776-a5b4c3d2e1f0"
        )
    assert caught.value is parked


# ── 5, continued. Every run that reached the provider says what it spent ─

HARVEST = ["label", "harvest", "https://example.invalid/playlist/harvest"]


@pytest.fixture
def installed(tmp_path, monkeypatch):
    """A machine the real dispatcher can load, with every module on, paced
    through a REAL gate on a short interval."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True, exist_ok=True)
    (root / "db").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return _save(tmp_path, min_interval_s=0.01)


def _spend_warnings(envelope: dict) -> list[str]:
    return [w["message"] for w in envelope.get("warnings", ()) if w.get("code") == PROVIDER_SPEND]


def _after_opening(monkeypatch, then) -> None:
    """Run ``then`` after the real catalogue opener has opened."""
    original = tidal_catalogue.open_catalogue

    def opening(cfg=None):
        opened = original(cfg)
        then()
        return opened

    monkeypatch.setattr(tidal_catalogue, "open_catalogue", opening)


def _another_process_spends_forty() -> None:
    state_path = config.state_path(provider_gate.STATE_KEY)
    state = json.loads(state_path.read_text())
    state["calls"] += 40
    state_path.write_text(json.dumps(state))


def _line(calls: int, limited: str) -> str:
    noun = "call" if calls == 1 else "calls"
    return (
        f"{calls} {noun} to the streaming provider this run, {limited} answered with a "
        f"rate limit; {calls} on the account and none under Cratekit's app credentials"
    )


@pytest.mark.parametrize(
    ("answers", "after", "reason", "said"),
    [
        ((), None, None, _line(1, "none")),
        ((rate_limited(), Response()), "two-requests", None, _line(3, "1")),
        ((rate_limited("900"),), None, COOLDOWN, _line(1, "1")),
        ((), "forty-elsewhere", None, _line(1, "none")),
    ],
    ids=["reports-its-calls", "names-rate-limit-answers", "survives-a-refusal",
         "excludes-another-processs-calls"],
)
def test_a_run_that_reached_the_provider_reports_its_calls(
    installed, monkeypatch, login, answers, after, reason, said
):
    """Through the REAL dispatcher, only the client faked. Rate limit answers
    are named, a refused run reports its cost, another process's calls are not
    this run's. Requests after opening are plain requests on the gated transport."""
    client = login(*answers)
    if after == "two-requests":
        _after_opening(monkeypatch, lambda: [
            client.request_session.request("GET", f"https://api.invalid/{p}") for p in "ab"
        ])
    elif after == "forty-elsewhere":
        _after_opening(monkeypatch, _another_process_spends_forty)
    code, envelope = drive(HARVEST)
    assert code != int(ExitCode.OK), "the fake client cannot serve a playlist"
    if reason is not None:
        assert envelope["cause"]["reason"] == reason
    assert _spend_warnings(envelope) == [said]


def test_the_spend_line_reaches_a_person_on_the_human_output(installed, login):
    login()
    out, err = io.StringIO(), io.StringIO()
    cli.run(HARVEST, stdout=out, stderr=err)
    shown = out.getvalue() + err.getvalue()
    assert f"warning [{PROVIDER_SPEND}]: 1 call to the streaming provider this run" in shown


def test_a_run_that_never_reached_the_provider_carries_no_spend_line(installed):
    code, envelope = drive(["label", "registry", "add", "Hotflush Recordings"])
    assert code == int(ExitCode.OK), envelope
    assert _spend_warnings(envelope) == []


# ── 7. The call ceiling, a line per command (U193) ───────────────────────

def test_a_command_stops_before_the_call_past_its_ceiling_with_the_count_at_the_ceiling(paths, clock):
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


def test_the_ceiling_never_says_kept_over_work_a_continue_does_again(paths, clock):
    """U217: not every command keeps what it read, so the stop claims nothing kept."""
    gate = ceiling_gate(paths, clock, 1)
    transport = Transport()
    with provider_gate.command():
        send_through(gate, transport)
        with pytest.raises(jobs.Parked) as caught:
            send_through(gate, transport)
    message = caught.value.cause.message
    assert "is kept" not in message
    assert "remaining items stay queued" in message
    assert "read and did not keep is read again when it continues" in message


def test_the_stop_is_remembered_so_a_swallowing_tool_still_parks(paths, clock):
    """The ceiling comes out of ``raise_if_parked`` like a trip does."""
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
        parked(lambda: send_through(gate, transport))
    assert len(transport.calls) == 6


def test_a_nested_dispatch_keeps_the_outer_commands_count(paths, clock):
    """``run decide --continue`` must not spend one command's ceiling twice."""
    gate = ceiling_gate(paths, clock, 2)
    transport = Transport()
    with provider_gate.command() as outer:
        send_through(gate, transport)
        with provider_gate.command(calls=50) as inner:
            assert inner is outer
            send_through(gate, transport)
            parked(lambda: send_through(gate, transport))
    assert len(transport.calls) == 2


def test_a_raised_ceiling_lasts_one_run_and_the_next_is_back_at_the_configured_one(paths, clock, monkeypatch):
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
        parked(lambda: send_through(gate, transport))
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
def test_a_detached_child_reads_the_raised_ceiling_off_the_environment(monkeypatch, value, raised):
    """A value that is not a positive whole number leaves the configured ceiling."""
    monkeypatch.setenv(CALLS_ENV, value)
    with provider_gate.command() as scope:
        assert scope.raised == raised
        assert provider_gate.ceiling(GateSettings(calls_per_command=3)) == (raised or 3)


def test_the_ceiling_parks_a_job_and_the_resumed_job_continues(paths, clock, queue, cfg):
    """Three items, two calls each, a ceiling of three: the job blocks naming
    itself with the second item pending, and the resume the refusal names finishes it."""
    store, root = queue
    gate = ceiling_gate(paths, clock, 3)
    transport = Transport()
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=list("abc"))

    def handle(_job, item):
        send_through(gate, transport)
        send_through(gate, transport)

    with provider_gate.command():
        first = jobs.drive(store, job.job_id, handle, root=root)
    assert first.job.state is jobs.JobState.BLOCKED
    assert first.job.cause is not None and first.job.cause.reason == CEILING
    assert first.job.cause.detail["job_id"] == job.job_id
    assert "crate --calls 6 job resume JOB_ID" in first.job.cause.remediation.steps[0]
    assert len(transport.calls) == 3
    assert _item_states(store, job) == {
        "a": jobs.ItemState.DONE,
        "b": jobs.ItemState.PENDING,
        "c": jobs.ItemState.PENDING,
    }
    # The two items left take four calls, one past the configured three.
    with provider_gate.command(calls=first.job.cause.detail["higher"]):
        second = jobs.drive(store, job.job_id, handle, root=root)
    assert second.job.state is jobs.JobState.SUCCEEDED
    assert len(transport.calls) == 7


def _cause(reason: str, remedy, message: str, **detail: Any) -> Cause:
    return Cause(
        reason=reason, message=message, remediation=Remediation(remedy=remedy), detail=detail
    )


def test_a_park_that_names_its_job_keeps_its_own_job_id(paths, clock, queue, cfg):
    store, root = queue
    job = jobs.enqueue(store, handler_key="job.resume", payload={}, cfg=cfg, item_ids=["a"])

    def handle(_job, _item):
        raise jobs.Parked(_cause(COOLDOWN, jobs.Remedy.RETRY_LATER, "held", job_id="another"))

    result = jobs.drive(store, job.job_id, handle, root=root)
    assert result.job.cause.detail["job_id"] == "another"


def test_a_separate_session_such_as_the_media_segment_fetch_is_not_counted(paths, clock):
    """The downloader fetches media segments through a session of its own; a
    command at its ceiling still fetches them."""
    gate = ceiling_gate(paths, clock, 1)
    client = SimpleNamespace(request_session=Transport())
    assert gate.attach(client)
    with provider_gate.command() as scope:
        client.request_session.request("GET", "https://api.invalid/track")
        with requests.Session() as segments:
            segments.mount("https://", _Answering(200, b"segment"))
            fetched = [segments.get(f"https://cdn.invalid/{n}").content for n in range(3)]
        parked(lambda: client.request_session.request("GET", "https://api.invalid/next"))
    assert fetched == [b"segment"] * 3
    assert scope.spent() == 1
    assert gate.calls == 1


def test_the_ceiling_defaults_to_five_hundred_and_round_trips(tmp_path):
    section = config.from_dict(_config_data(tmp_path)).provider
    assert section.calls_per_command == config.DEFAULT_PROVIDER_CALLS_PER_COMMAND == 500
    assert GateSettings().calls_per_command == 500
    _save(tmp_path, calls_per_command=2000)
    assert GateSettings.from_config(config.load()).calls_per_command == 2000


def test_the_ceiling_reason_is_declared_as_a_policy_refusal():
    assert REASONS[CEILING] is ExitCode.REFUSED_BY_POLICY


# ── 7, through the real dispatcher ───────────────────────────────────────

def _two_more_calls(monkeypatch, client, *, swallow: bool = False) -> list[str]:
    """Two calls beyond the login, as the catalogue would make; ``swallow``
    catches the stop as a verb that walks a list per item might."""
    caught: list[str] = []

    def more() -> None:
        for path in ("a", "b"):
            try:
                client.request_session.request("GET", f"https://api.invalid/{path}")
            except CratekitError as exc:
                if not swallow:
                    raise
                caught.append(exc.cause.reason)

    _after_opening(monkeypatch, more)
    return caught


def _capped(tmp_path, login, monkeypatch, **provider: Any) -> _LoginClient:
    _save(tmp_path, min_interval_s=0.01, **provider)
    client = login()
    _two_more_calls(monkeypatch, client)
    return client


@pytest.fixture
def capped(installed, tmp_path, login, monkeypatch):
    """The installed machine at one call per command, a client logged in, and
    two calls beyond the login."""
    return _capped(tmp_path, login, monkeypatch, calls_per_command=1)


@pytest.mark.parametrize(
    ("provider", "reason"),
    [({"calls_per_command": 1}, CEILING), ({"calls_per_hour": 2, "reserve_share": 0.5}, BUDGET)],
    ids=["its-ceiling-names-the-exact-command-that-continues", "the-hours-line-U278"],
)
def test_a_verb_at_its_line_is_blocked_and_the_call_past_it_is_not_sent(
    installed, tmp_path, login, monkeypatch, provider, reason
):
    """A park, never a failure. A ceiling stop names the exact command that
    continues, global options kept, and says the stop once."""
    client = _capped(tmp_path, login, monkeypatch, **provider)
    code, envelope = drive(HARVEST)
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["outcome"] == "blocked"
    cause = envelope["cause"]
    assert cause["reason"] == reason
    assert len(client.request_session.calls) == 1, "a call past the line was sent"
    if reason == CEILING:
        expected = "crate --output json --calls 2 " + " ".join(HARVEST)
        assert cause["detail"]["continue"] == expected
        assert cause["remediation"]["steps"][0].endswith(expected)
        said = [w for w in envelope.get("warnings", ()) if w.get("code") == CEILING]
        assert said == [], "the refusal already says the stop; a warning says it twice"


def test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling(capped):
    _, raised = drive(["--calls", "3", *HARVEST])
    assert (raised.get("cause") or {}).get("reason") != CEILING, raised
    assert len(capped.request_session.calls) == 3
    _, again = drive(HARVEST)
    assert again["cause"]["reason"] == CEILING
    assert len(capped.request_session.calls) == 4
    assert CALLS_ENV not in os.environ


@pytest.mark.parametrize("given", [["--calls=2"], ["--calls", "2"]], ids=["joined", "spaced"])
def test_the_continue_command_replaces_a_calls_already_given(capped, given):
    _, envelope = drive([*given, *HARVEST])
    assert len(capped.request_session.calls) == 2
    assert envelope["cause"]["detail"]["continue"] == (
        "crate --output json --calls 4 " + " ".join(HARVEST)
    )


@pytest.mark.parametrize("value", ["0", "-2", "many"])
def test_a_calls_that_is_not_a_positive_whole_number_is_a_usage_error(value, capsys):
    out, err = io.StringIO(), io.StringIO()
    assert cli.run(["--calls", value, *HARVEST], stdout=out, stderr=err) == int(ExitCode.USAGE)
    assert "positive whole number" in capsys.readouterr().err


def test_a_ceiling_stop_a_verb_swallowed_is_still_said(installed, tmp_path, login, monkeypatch):
    """Else a verb that catches the park per item shows a report over reads the
    ceiling stopped."""
    _save(tmp_path, min_interval_s=0.01, calls_per_command=1)
    caught = _two_more_calls(monkeypatch, login(), swallow=True)
    _, envelope = drive(HARVEST)
    assert caught == [CEILING, CEILING]
    said = [w["message"] for w in envelope.get("warnings", ()) if w.get("code") == CEILING]
    assert len(said) == 1, envelope
    assert "was not read from the provider" in said[0]
    assert "crate --output json --calls 2 " + " ".join(HARVEST) in said[0]


@pytest.mark.parametrize(
    ("verb", "detail", "asked"),
    [
        (
            "label.harvest",
            {"ceiling": 500, "higher": 1000, "job_id": "2026-11-02T00:00:00Z-ab12"},
            [(HARVEST, "crate --calls 1000 job resume 2026-11-02T00:00:00Z-ab12")],
        ),
        (
            "sync.pair",
            {"ceiling": 5000, "higher": 6000, "run_id": "run-7"},
            [
                (["sync", "pair"], "crate --run run-7 --calls 6000 sync pair"),
                (["--run", "run-7", "sync", "pair"], "crate --run run-7 --calls 6000 sync pair"),
                (
                    ["--run=run-7", "--calls", "10", "sync", "pair"],
                    "crate --run=run-7 --calls 6000 sync pair",
                ),
            ],
        ),
        (
            "sync.pair",
            {"ceiling": 5000, "higher": 10000, "fresh": True},
            [
                (["--run", "run-7", "sync", "pair"], "crate --calls 10000 sync pair"),
                (["--run=run-7", "sync", "pair"], "crate --calls 10000 sync pair"),
            ],
        ),
    ],
    ids=["a-job-resumes-that-job", "a-run-continues-that-run-once",
         "a-run-that-cannot-continue-starts-anew"],
)
def test_the_continue_command_names_the_job_or_run_to_continue(verb, detail, asked):
    """U210. A cause naming its run continues THAT run, once, whatever the
    command line held; a write that recorded no steps is named without it."""
    entry = next(one for one in landed_entries() if one.name == verb)
    cause = _cause(CEILING, jobs.Remedy.FIX_COMMAND_LINE, "stopped", **detail)
    for argv, expected in asked:
        assert continue_command(argv, entry, cause) == expected
