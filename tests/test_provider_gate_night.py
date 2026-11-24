"""U293: the night pass's line in the provider gate, and its night's ledger.

The unwatched night's budget is held in :class:`cratekit.core.provider_gate.Gate`,
under the lock, before the send. Driven on a fake clock and a recording transport.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta

import pytest

from cratekit.core import config, jobs, night_budget, provider_gate
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.provider_gate import Gate, GateSettings, Night
from tests.test_config import valid_data
from tests.test_provider_gate import Clock, Transport


def _gate(tmp_path, clock, **settings) -> Gate:
    return Gate(
        GateSettings(min_interval_s=1.0, **settings),
        path=tmp_path / "gate" / "provider_gate.json",
        lock_path=tmp_path / "gate" / "provider_gate.lock",
        clock=clock,
        sleep=clock.sleep,
    )


def _send(gate: Gate, transport: Transport) -> None:
    gate.call(lambda: transport.request("GET", "https://api.invalid/x"))


def _bump(gate: Gate, calls: int) -> None:
    """Another process's calls, as the shared state file records them."""
    data = json.loads(gate.path.read_text()) if gate.path.exists() else {}
    data["calls"] = int(data.get("calls", 0)) + calls
    gate.path.parent.mkdir(parents=True, exist_ok=True)
    gate.path.write_text(json.dumps(data))


@pytest.fixture
def clock() -> Clock:
    return Clock()


# 1. The line, call by call


def test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night(
    tmp_path, clock
):
    gate = _gate(tmp_path, clock)
    settings = gate.settings
    transport = Transport()

    with provider_gate.command() as scope:
        with provider_gate.night(0, 3, "2026-11-21", calls_per_hour=600, settings=settings):
            for _ in range(3):
                _send(gate, transport)
            with pytest.raises(jobs.Parked) as caught:
                _send(gate, transport)

    assert len(transport.calls) == 3, "a call past the night's line was sent"
    cause = caught.value.cause
    assert cause.reason == provider_gate.NIGHT
    assert cause.detail["spent"] == 3 and cause.detail["budget"] == 3
    assert cause.detail["night"] == "2026-11-21"
    assert "[provider] night_calls" in cause.message
    assert cause.retryable is False
    assert scope.stopped is cause


def test_another_processs_calls_count_against_the_night(tmp_path, clock):
    gate = _gate(tmp_path, clock)
    transport = Transport()

    with provider_gate.command():
        with provider_gate.night(0, 5, "n", calls_per_hour=600, settings=gate.settings):
            _send(gate, transport)
            _bump(gate, 4)
            with pytest.raises(jobs.Parked) as caught:
                _send(gate, transport)

    assert len(transport.calls) == 1
    assert caught.value.cause.detail["spent"] == 5


def test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops(tmp_path, clock):
    gate = _gate(tmp_path, clock)
    transport = Transport()

    with provider_gate.command():
        with provider_gate.night(100, 50, "n", calls_per_hour=600, settings=gate.settings):
            with pytest.raises(jobs.Parked) as caught:
                _send(gate, transport)

    assert transport.calls == []
    assert caught.value.cause.reason == provider_gate.NIGHT
    assert "cannot be read" in caught.value.cause.message


def test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling(tmp_path, clock):
    """Round one: the line is the lower of it and the ceiling, so the stop names the night."""
    gate = _gate(tmp_path, clock, calls_per_command=2)
    transport = Transport()

    with provider_gate.command():
        with provider_gate.night(0, 4, "n", calls_per_hour=600, settings=gate.settings) as held:
            assert held.budget == 2
            for _ in range(2):
                _send(gate, transport)
            with pytest.raises(jobs.Parked) as caught:
                _send(gate, transport)

    assert len(transport.calls) == 2
    assert caught.value.cause.reason == provider_gate.NIGHT
    assert "[provider] calls_per_command" in caught.value.cause.message


def test_the_line_is_held_to_what_the_command_has_left_of_its_ceiling(tmp_path, clock):
    """Round two: calls made before the night opened come off the line."""
    gate = _gate(tmp_path, clock, calls_per_command=5)
    transport = Transport()
    with provider_gate.command():
        _send(gate, transport)
        _send(gate, transport)
        with provider_gate.night(0, 100, "n", calls_per_hour=600, settings=gate.settings) as held:
            assert held.budget == 3


def test_a_ceiling_raised_through_the_environment_never_widens_a_firing(monkeypatch):
    """Round two, finding 6: the night refuses --calls and the unseen variable is held."""
    monkeypatch.setenv(provider_gate.CALLS_ENV, "600")
    settings = GateSettings(calls_per_command=500)
    with provider_gate.command():
        with provider_gate.night(0, 1200, "n", calls_per_hour=600, settings=settings) as held:
            assert held.budget == 500


def _hand_a_line_past_the_ceiling(scope) -> None:
    scope.night = Night(start=0, budget=10, night="n")


def _the_line_off_the_environment(scope) -> None:
    assert scope.night == Night(start=0, budget=100, night="n")


@pytest.mark.parametrize(
    ("ceiling", "bump", "line", "in_scope", "reason"),
    [
        pytest.param(2, 0, None, _hand_a_line_past_the_ceiling, provider_gate.CEILING,
                     id="the-ceiling-still-holds-beside-a-line-above-it"),
        pytest.param(2, 0, "0:100:n", _the_line_off_the_environment, provider_gate.CEILING,
                     id="a-line-read-off-the-environment-is-held-beside-the-ceiling"),
        pytest.param(50, 10, "10:2:n", None, provider_gate.NIGHT,
                     id="an-inherited-night-line-stops-a-child-at-the-nights-remainder"),
    ],
)
def test_the_lower_of_the_ceiling_and_a_handed_line_stops_the_third_call(
    tmp_path, clock, monkeypatch, ceiling, bump, line, in_scope, reason
):
    """A line from a parent or the environment can only lower; the ceiling holds beside it."""
    gate = _gate(tmp_path, clock, calls_per_command=ceiling)
    transport = Transport()
    if bump:
        _bump(gate, bump)
    if line:
        monkeypatch.setenv(provider_gate.NIGHT_ENV, line)
    with provider_gate.command() as scope:
        if in_scope:
            in_scope(scope)
        _send(gate, transport)
        _send(gate, transport)
        with pytest.raises(jobs.Parked) as caught:
            _send(gate, transport)
    assert caught.value.cause.reason == reason


@pytest.mark.parametrize("text", ["", "x", "1:2", "a:2:n", "1:b:n", "1:2:", "-1:2:n"])
def test_a_night_line_that_cannot_be_read_off_the_environment_is_none(text):
    assert Night.from_env(text) is None


def test_the_night_lowers_the_hour_and_never_raises_it(tmp_path, clock):
    settings = GateSettings(calls_per_hour=1500)
    with provider_gate.command():
        with provider_gate.night(0, 10, "n", calls_per_hour=600, settings=settings):
            assert provider_gate.hourly(settings) == 600
        with provider_gate.night(0, 10, "n", calls_per_hour=3000, settings=settings):
            assert provider_gate.hourly(settings) == 1500
        assert provider_gate.hourly(settings) == 1500
    with provider_gate.command(calls_per_hour=5000):
        with provider_gate.night(0, 10, "n", calls_per_hour=600, settings=settings):
            assert provider_gate.hourly(settings) == 600


def test_the_hour_the_night_lowers_holds_the_call(tmp_path, clock):
    gate = _gate(tmp_path, clock, calls_per_hour=1500)
    transport = Transport()

    with provider_gate.command(reserve=True):
        with provider_gate.night(0, 100, "n", calls_per_hour=2, settings=gate.settings):
            _send(gate, transport)
            _send(gate, transport)
            with pytest.raises(jobs.Parked) as caught:
                _send(gate, transport)

    assert caught.value.cause.reason == provider_gate.BUDGET


def test_a_nested_night_keeps_the_lower_line(tmp_path, clock):
    settings = GateSettings()
    with provider_gate.command() as scope:
        with provider_gate.night(0, 10, "n", calls_per_hour=600, settings=settings):
            with provider_gate.night(4, 100, "n", calls_per_hour=600, settings=settings) as inner:
                assert inner.budget == 6
                assert scope.night == inner
            assert scope.night == Night(start=0, budget=10, night="n")


def test_the_line_reaches_a_child_through_the_environment_and_is_put_back(monkeypatch):
    monkeypatch.setenv(provider_gate.NIGHT_ENV, "earlier")
    settings = GateSettings()
    with provider_gate.command():
        with provider_gate.night(7, 8, "n", calls_per_hour=600, settings=settings):
            assert os.environ[provider_gate.NIGHT_ENV] == "7:8:n"
            assert os.environ[provider_gate.BUDGET_ENV] == "600"
        assert os.environ[provider_gate.NIGHT_ENV] == "earlier"


def test_a_night_outside_a_command_is_a_defect():
    with pytest.raises(RuntimeError):
        with provider_gate.night(0, 1, "n", calls_per_hour=1, settings=GateSettings()):
            pass


def test_the_nights_reason_is_a_policy_refusal():
    assert REASONS[provider_gate.NIGHT] is ExitCode.REFUSED_BY_POLICY


# 2. The night's ledger


def _set_total(calls: int) -> None:
    path = config.state_path(provider_gate.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"calls": calls}))


AT_THREE = datetime(2026, 11, 22, 3, 0).astimezone()
AT_ONE_PM = datetime(2026, 11, 22, 13, 0).astimezone()


def test_a_night_runs_noon_to_noon_local_time():
    assert night_budget.night_of(AT_THREE) == "2026-11-21"
    assert night_budget.night_of(AT_ONE_PM) == "2026-11-22"
    assert night_budget.frees_at(AT_THREE) == AT_THREE.replace(hour=12)
    assert night_budget.frees_at(AT_ONE_PM) == AT_ONE_PM.replace(hour=12) + timedelta(days=1)


def test_a_firing_is_charged_before_its_first_call_and_closed_after():
    _set_total(20)

    opened = night_budget.open_night(100, now=AT_THREE)

    assert (opened.start, opened.spent_before, opened.remaining) == (20, 0, 100)
    assert night_budget.read().open_start == 20, "no mark before the first call"
    _set_total(45)
    assert night_budget.spent_tonight(AT_THREE) == 25
    assert night_budget.close_night(opened) == 25
    ledger = night_budget.read()
    assert (ledger.night, ledger.spent, ledger.open_start) == ("2026-11-21", 25, None)


@pytest.mark.parametrize(
    ("spent", "later", "expected"),
    [
        pytest.param(60, timedelta(hours=1), {"spent_before": 60, "remaining": 40},
                     id="a-second-firing-of-the-night-has-only-what-is-left"),
        pytest.param(100, timedelta(days=1), {"spent_before": 0, "night": "2026-11-22"},
                     id="the-next-night-starts-from-nothing"),
    ],
)
def test_a_later_firing_is_charged_what_its_own_night_spent(spent, later, expected):
    _set_total(0)
    first = night_budget.open_night(100, now=AT_THREE)
    _set_total(spent)
    night_budget.close_night(first)
    opened = night_budget.open_night(100, now=AT_THREE + later)
    assert {key: getattr(opened, key) for key in expected} == expected


def test_a_spent_night_refuses_and_names_when_it_frees():
    _set_total(0)
    first = night_budget.open_night(10, now=AT_THREE)
    _set_total(10)
    night_budget.close_night(first)

    with pytest.raises(CratekitError) as caught:
        night_budget.open_night(10, now=AT_THREE)

    cause = caught.value.cause
    assert cause.reason == provider_gate.NIGHT
    assert cause.detail["spent"] == 10 and cause.detail["budget"] == 10
    assert cause.detail["frees_at"].startswith("2026-11-22T12:00")


@pytest.mark.parametrize(
    ("marked", "total", "expected"),
    [
        pytest.param(200, 500, {"spent_before": 300, "remaining": 900},
                     id="a-dead-firings-mark-from-an-earlier-night-is-charged-to-tonight"),
        pytest.param(900, 1, {"spent_before": 0, "start": 1},
                     id="an-earlier-nights-mark-above-the-total-is-dropped-at-the-new-night"),
    ],
)
def test_an_earlier_nights_unclosed_mark_at_the_new_night(marked, total, expected):
    """Review rounds one and two: such a firing was once free after noon, or refused every night."""
    _set_total(marked)
    night_budget.open_night(1200, now=AT_THREE - timedelta(days=1))  # never closed
    _set_total(total)
    opened = night_budget.open_night(1200, now=AT_THREE)
    assert {key: getattr(opened, key) for key in expected} == expected


@pytest.mark.parametrize(
    ("start", "spoil"),
    [
        pytest.param(10, lambda: config.state_path(provider_gate.STATE_KEY).write_text("{"),
                     id="a-gate-unreadable-at-the-close-is-none-and-keeps-the-mark"),
        pytest.param(50, lambda: _set_total(5),
                     id="a-total-below-its-own-mark-at-close-keeps-the-mark"),
    ],
)
def test_a_close_that_cannot_count_the_firing_is_none_and_keeps_the_mark(start, spoil):
    _set_total(start)
    opened = night_budget.open_night(100, now=AT_THREE)
    spoil()
    assert night_budget.close_night(opened) is None
    assert night_budget.read().open_start == start


def test_outside_any_command_a_line_off_the_environment_holds_the_call(
    tmp_path, clock, monkeypatch
):
    """Review round one's zero row: the line is asked outside a scope too."""
    gate = _gate(tmp_path, clock)
    transport = Transport()
    monkeypatch.setenv(provider_gate.NIGHT_ENV, "0:1:n")

    _send(gate, transport)
    with pytest.raises(jobs.Parked) as caught:
        _send(gate, transport)

    assert caught.value.cause.reason == provider_gate.NIGHT
    assert len(transport.calls) == 1


def test_a_dead_firings_mark_is_charged_in_full_and_folded_on_a_refusal():
    _set_total(0)
    night_budget.open_night(10, now=AT_THREE)  # never closed
    _set_total(12)

    with pytest.raises(CratekitError):
        night_budget.open_night(10, now=AT_THREE)

    ledger = night_budget.read()
    assert ledger.spent == 12 and ledger.open_start is None


@pytest.mark.parametrize(
    "text",
    ["{", "[]", '{"schema": 2}', '{"schema": 1, "spent": -1}',
     '{"schema": 1, "spent": 0, "open": {"start": "x"}}', '{"schema": 1, "spent": true}'],
)
def test_a_ledger_that_cannot_be_read_refuses(text):
    path = night_budget.ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

    with pytest.raises(CratekitError) as caught:
        night_budget.open_night(100, now=AT_THREE)

    assert caught.value.cause.reason == provider_gate.NIGHT


def _a_gate_that_cannot_be_read() -> None:
    path = config.state_path(provider_gate.STATE_KEY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{")


def _a_total_below_an_earlier_firings_mark() -> None:
    _set_total(50)
    night_budget.open_night(100, now=AT_THREE)
    _set_total(5)


@pytest.mark.parametrize(
    ("setup", "said"),
    [
        pytest.param(_a_gate_that_cannot_be_read, "provider gate's state file could not be read",
                     id="a-gate-that-cannot-be-read-refuses-the-night"),
        pytest.param(_a_total_below_an_earlier_firings_mark, "below the mark",
                     id="a-total-below-an-earlier-firings-mark-refuses"),
    ],
)
def test_a_total_the_night_cannot_trust_refuses_saying_why(setup, said):
    setup()
    with pytest.raises(CratekitError) as caught:
        night_budget.open_night(100, now=AT_THREE)
    assert said in caught.value.cause.message


def test_the_ledger_sits_beside_the_gate_whatever_the_state_directory(monkeypatch, tmp_path):
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "elsewhere"))
    assert night_budget.ledger_path().parent == config.provider_gate_dir()


def test_the_night_defaults_sit_below_every_line_above_them():
    provider = config.ProviderConfig()
    assert provider.night_calls_per_hour < provider.calls_per_hour
    # SITTING 94: about 7,800 catalogue calls in twenty minutes locked the account.
    assert provider.night_calls < 7_800 and provider.night_calls_per_hour < 7_800
    assert provider.night_calls <= 2 * provider.calls_per_hour


@pytest.mark.parametrize("key", ["night_calls", "night_calls_per_hour"])
@pytest.mark.parametrize("value", [0, -1, True, 1.5, "10"])
def test_a_night_line_that_is_not_a_positive_whole_number_refuses_at_load(tmp_path, key, value):
    data = valid_data(tmp_path / "library")
    data["provider"] = {key: value}
    with pytest.raises(config.ConfigError) as caught:
        config.from_dict(data)
    assert f"provider.{key}" in str(caught.value)


def test_the_night_lines_round_trip_through_the_file(tmp_path):
    data = valid_data(tmp_path / "library")
    data["provider"] = {"night_calls": 300, "night_calls_per_hour": 90}
    built = config.from_dict(data)
    assert (built.provider.night_calls, built.provider.night_calls_per_hour) == (300, 90)
