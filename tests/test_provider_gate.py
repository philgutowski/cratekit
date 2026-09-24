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
5. **Spend is counted**, across processes, so a run can report what it cost.
6. **The two build sites attach the gate and nothing else builds a client.**

Every schedule is driven with a fake clock whose ``sleep`` advances it, so the
suite asserts on the waits a run would have taken rather than taking them. The
two process tests use the real clock and real sleeps, because the lock the
kernel holds cannot be faked, and their intervals are short.
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


def test_two_processes_never_call_at_once_and_keep_the_interval(paths, tmp_path):
    """Two REAL processes, each making four calls through one gate, each call
    holding the provider for twenty milliseconds. Read together, no two calls
    overlap and every gap between starts is the interval. The tolerance on
    the gap is the write of the state file between a call's stamp and its
    request, a millisecond against a fifty millisecond interval."""
    state, lock = paths
    interval = 0.05
    script = tmp_path / "driver.py"
    script.write_text(
        textwrap.dedent(
            """
            import json, sys, time
            from pathlib import Path
            from cratekit.core.provider_gate import Gate, GateSettings

            state, lock, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
            count, interval = int(sys.argv[4]), float(sys.argv[5])
            gate = Gate(GateSettings(min_interval_s=interval), path=state, lock_path=lock)
            spans = []

            class Answer:
                status_code = 200
                headers = {}

            def send():
                started = time.time()
                time.sleep(0.02)
                spans.append((started, time.time()))
                return Answer()

            for _ in range(count):
                gate.call(send)
            out.write_text(json.dumps(spans))
            """
        )
    )
    outs = [tmp_path / "a.json", tmp_path / "b.json"]
    children = [
        _start_child(script, str(state), str(lock), str(out), "4", str(interval)) for out in outs
    ]
    for child in children:
        stdout, stderr = child.communicate(timeout=60)
        assert child.returncode == 0, stderr

    spans = sorted(span for out in outs for span in json.loads(out.read_text()))
    assert len(spans) == 8
    for (_, earlier_end), (later_start, _) in zip(spans, spans[1:]):
        assert later_start >= earlier_end, f"two calls overlapped: {spans}"
    gaps = [later[0] - earlier[0] for earlier, later in zip(spans, spans[1:])]
    assert all(gap >= interval * 0.9 for gap in gaps), gaps
    assert json.loads(state.read_text())["calls"] == 8


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
        with pytest.raises(CratekitError) as caught:
            send_through(gate, transport)
    finally:
        os.close(holder)

    assert caught.value.cause.reason == HELD
    assert caught.value.cause.retryable is True
    assert transport.calls == []
    # The poll count cap and the time cap agree to within one poll.
    assert sum(clock.slept) >= LOCK_WAIT_S - provider_gate.LOCK_POLL_S


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
    assert found == ["_vendor/tidal_dl_ng/config.py", "acquire/provider_session.py"]


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


@pytest.mark.parametrize("value", [0, -1, 0.0, True, "1", float("nan")])
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
