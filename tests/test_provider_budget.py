"""U278: one allowance per account, whatever state is redirected, and a reserve.

A copy with ``CRATEKIT_STATE_DIR`` redirected once spent calls the live gate never
saw. One gate per account (unless ``CRATEKIT_PROVIDER_GATE_DIR``), a rolling hourly
budget across processes parking as ``provider-budget``, a reserve reads stop short
of, doctor's standing, and a sweep's cost said first. Clocks are fake but one test.
"""

from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit import cli
from cratekit.cli import doctor, registry
from cratekit.core import config, jobs, provider_gate
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.provider_gate import ACCOUNT, APP, BUDGET, Gate, GateSettings
from cratekit.intake import rehearsal
from cratekit.label import kept_listing, kept_reads, playlists_cli
from cratekit.label import registry as labels
from tests import test_label_sync as ls
from tests.cli_drive import drive
from tests.test_provider_gate import Clock

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"


class Ok:
    status_code = 200
    headers: dict[str, str] = {}


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def paths(tmp_path: Path) -> tuple[Path, Path]:
    return tmp_path / "gate" / "provider_gate.json", tmp_path / "gate" / "provider_gate.lock"


def make_gate(paths, clock, *, per_hour: int = 8, share: float = 0.25, per_command=None) -> Gate:
    extra = {} if per_command is None else {"calls_per_command": per_command}
    settings = GateSettings(min_interval_s=1.0, calls_per_hour=per_hour, reserve_share=share, **extra)
    return Gate(settings, path=paths[0], lock_path=paths[1], clock=clock, sleep=clock.sleep)


@pytest.fixture
def gate(paths, clock) -> Gate:
    """Eight calls an hour with a quarter in reserve: reads stop at six."""
    return make_gate(paths, clock, per_hour=8, share=0.25)


def spend_calls(gate: Gate, n: int, *, identity: str = ACCOUNT) -> list[int]:
    sent: list[int] = []
    for _ in range(n):
        gate.call(lambda: sent.append(1) or Ok(), identity=identity)
    return sent


def refused(gate: Gate, *, identity: str = ACCOUNT) -> tuple[CratekitError, list[int]]:
    sent: list[int] = []
    with pytest.raises(CratekitError) as caught:
        gate.call(lambda: sent.append(1) or Ok(), identity=identity)
    return caught.value, sent


def _frees(epoch: float) -> float:
    return provider_gate._bucket(epoch) + provider_gate.BUCKET_S + provider_gate.WINDOW_S


# ── 1. One gate per account, whatever state is redirected ───────────────

def test_a_redirected_state_directory_still_resolves_the_one_gate(monkeypatch, tmp_path):
    """A copy's ``CRATEKIT_STATE_DIR`` moves everything but the gate and its lock."""
    monkeypatch.delenv(config.ENV_PROVIDER_GATE_DIR, raising=False)
    live = config.state_path(provider_gate.STATE_KEY)
    live_lock = config.state_path(provider_gate.LOCK_KEY)
    live_queue = config.state_path("job_queue")
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "copy" / "state"))
    assert config.state_path("job_queue") != live_queue, "the redirect moved nothing"
    assert config.state_path(provider_gate.STATE_KEY) == live
    assert config.state_path(provider_gate.LOCK_KEY) == live_lock
    assert Gate().path == live
    assert Gate().lock_path == live_lock
    assert not live.is_relative_to(tmp_path / "copy")


def test_the_pointer_names_where_the_gate_lives(monkeypatch, tmp_path):
    monkeypatch.setenv(config.ENV_PROVIDER_GATE_DIR, str(tmp_path / "elsewhere"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(tmp_path / "copy" / "state"))
    assert config.state_path(provider_gate.STATE_KEY) == tmp_path / "elsewhere" / "provider_gate.json"
    assert config.state_path(provider_gate.LOCK_KEY) == tmp_path / "elsewhere" / "provider_gate.lock"


def test_the_suite_points_the_gate_into_the_tests_own_state():
    """conftest isolation: no test resolves the real gate."""
    pointed = os.environ.get(config.ENV_PROVIDER_GATE_DIR)
    assert pointed, "conftest left the gate pointer unset"
    assert config.state_path(provider_gate.STATE_KEY).parent == Path(pointed)
    assert Path(pointed) == config.installation_state_dir()


def test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate(monkeypatch, tmp_path):
    """A copy's call moves the live gate's count, and the copy's state holds no gate."""
    monkeypatch.delenv(config.ENV_PROVIDER_GATE_DIR, raising=False)
    live = Gate()
    before = live.window_spend(ACCOUNT)
    copy_state = tmp_path / "copy" / "state"
    monkeypatch.setenv(config.ENV_STATE_DIR, str(copy_state))
    from_the_copy = Gate(GateSettings(min_interval_s=0.001))
    from_the_copy.call(lambda: Ok())
    assert from_the_copy.path == live.path
    assert Gate(path=live.path, lock_path=live.lock_path).window_spend(ACCOUNT) == before + 1
    assert not (copy_state / "provider_gate.json").exists()
    assert not copy_state.exists() or not any(copy_state.rglob("provider_gate*"))


@pytest.mark.parametrize("pointed", [True, False])
def test_a_rehearsal_spends_from_the_live_gate(tmp_path, monkeypatch, pointed):
    """Under ``intake.rehearsal.redirected`` the gate stays live and the pointer is untouched."""
    if not pointed:
        monkeypatch.delenv(config.ENV_PROVIDER_GATE_DIR, raising=False)
    live = config.state_path(provider_gate.STATE_KEY)
    before = os.environ.get(config.ENV_PROVIDER_GATE_DIR)
    area = SimpleNamespace(local=tmp_path / "area", cfg=None)
    with rehearsal.redirected(area):
        assert config.installation_state_dir() == tmp_path / "area" / "state"
        assert config.state_path(provider_gate.STATE_KEY) == live
        assert Gate().path == live
        assert os.environ.get(config.ENV_PROVIDER_GATE_DIR) == before


# ── 2. A rolling budget, per identity ────────────────────────────────────

def test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees(gate, clock):
    with provider_gate.command():
        sent = spend_calls(gate, 6)
        error, more = refused(gate)
    assert len(sent) == 6 and more == [], "a call past the read line was sent"
    cause = error.cause
    assert cause.reason == BUDGET
    assert cause.retryable is False
    detail = cause.detail
    assert detail["identity"] == ACCOUNT
    assert detail["spent"] == 6
    assert detail["line"] == 6
    assert detail["budget"] == 8
    assert detail["frees_at"] == provider_gate._iso(_frees(clock.now - 5))
    assert "6 calls" in cause.message and "frees at" in cause.message
    assert any("--calls-per-hour" in step for step in cause.remediation.steps)
    assert isinstance(error, jobs.Parked), "the hour's line is a park, never a retry"


def test_the_budget_counts_every_command_and_every_gate_on_the_file(paths, clock):
    """Many small commands are one window."""
    for _ in range(3):
        with provider_gate.command():
            spend_calls(make_gate(paths, clock), 2)
    with provider_gate.command():
        error, sent = refused(make_gate(paths, clock))
    assert error.cause.reason == BUDGET and sent == []


def test_the_window_frees_as_its_oldest_minute_ages_out(gate, clock):
    with provider_gate.command():
        spend_calls(gate, 6)
        error, _ = refused(gate)
    frees = error.cause.detail["frees_at"]
    clock.now = _frees(1_700_000_000.0) - 1
    with provider_gate.command():
        still, _ = refused(gate)
    assert still.cause.detail["frees_at"] == frees
    clock.now += 1
    with provider_gate.command():
        assert len(spend_calls(gate, 1)) == 1


def test_one_identity_at_its_line_leaves_the_other_open(gate):
    with provider_gate.command():
        spend_calls(gate, 6, identity=ACCOUNT)
        error, _ = refused(gate, identity=ACCOUNT)
        assert error.cause.detail["identity"] == ACCOUNT
        assert len(spend_calls(gate, 6, identity=APP)) == 6
        app_error, _ = refused(gate, identity=APP)
    assert app_error.cause.detail["identity"] == APP
    assert gate.window_spend(ACCOUNT) == 6
    assert gate.window_spend(APP) == 6


def test_a_file_written_before_the_window_reads_as_nothing_spent(paths, clock):
    state, _ = paths
    state.parent.mkdir(parents=True)
    state.write_text(json.dumps({"calls": 9000, "rate_limited": 3, "last_call": 0}))
    gate = make_gate(paths, clock)
    assert gate.window_spend(ACCOUNT) == 0
    with provider_gate.command():
        assert len(spend_calls(gate, 1)) == 1
    assert json.loads(state.read_text())["calls"] == 9001, "the running total was not kept"


def test_minutes_older_than_the_window_are_pruned_from_the_file(paths, clock):
    gate = make_gate(paths, clock, per_hour=100)
    with provider_gate.command():
        spend_calls(gate, 2)
    clock.now += 2 * provider_gate.WINDOW_S
    with provider_gate.command():
        spend_calls(gate, 1)
    window = json.loads(paths[0].read_text())["window"]
    assert sum(window[ACCOUNT].values()) == 1
    assert len(window[ACCOUNT]) == 1


def test_the_count_is_written_before_the_send(paths, clock):
    gate = make_gate(paths, clock, per_hour=100)
    seen: list[int] = []

    def send() -> Ok:
        seen.append(sum(json.loads(paths[0].read_text())["window"][ACCOUNT].values()))
        return Ok()

    with provider_gate.command():
        gate.call(send)
    assert seen == [1]


def test_a_cooldown_still_refuses_first_and_keeps_its_own_reason(paths, clock):
    """A trip in the window refuses as the cooldown; the budget never trips the breaker."""
    gate = make_gate(paths, clock, per_hour=8)
    with provider_gate.command():
        spend_calls(gate, 6)
        error, _ = refused(gate)
    data = json.loads(paths[0].read_text())
    assert error.cause.reason == BUDGET
    assert data["trips"] == 0 and data["lifts_at"] is None
    data["lifts_at"] = clock.now + 900
    data["tripped_at"] = clock.now
    paths[0].write_text(json.dumps(data))
    with provider_gate.command():
        cooling, _ = refused(gate)
    assert cooling.cause.reason == provider_gate.COOLDOWN


_SPENDER = """
import sys
from pathlib import Path
from cratekit.core.provider_gate import Gate, GateSettings

class Ok:
    status_code = 200
    headers = {}

state, lock = Path(sys.argv[1]), Path(sys.argv[2])
gate = Gate(GateSettings(min_interval_s=0.001, calls_per_hour=1000), path=state, lock_path=lock)
for _ in range(5):
    gate.call(lambda: Ok())
"""


def test_two_processes_count_toward_one_window(paths, tmp_path):
    state, lock = paths
    script = tmp_path / "spender.py"
    script.write_text(_SPENDER)
    env = dict(os.environ, PYTHONPATH=str(SRC_ROOT), PYTHONDONTWRITEBYTECODE="1")
    children = [
        subprocess.Popen([sys.executable, str(script), str(state), str(lock)], env=env)
        for _ in range(2)
    ]
    assert [child.wait(timeout=60) for child in children] == [0, 0]
    assert Gate(GateSettings(), path=state, lock_path=lock).window_spend(ACCOUNT) == 10


@pytest.mark.parametrize("identity", [ACCOUNT, APP], ids=["account", "app-credentials"])
def test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer(gate, clock, identity):
    """Calls stamped ahead still count and free an hour after now (round one, R4)."""
    ahead = clock.now
    clock.now += 30 * 86_400
    with provider_gate.command():
        spend_calls(gate, 6, identity=identity)
    clock.now = ahead
    with provider_gate.command():
        error, _ = refused(gate, identity=identity)
    assert error.cause.detail["frees_at"] == provider_gate.iso(_frees(ahead))
    clock.now = _frees(ahead)
    with provider_gate.command():
        assert len(spend_calls(gate, 1, identity=identity)) == 1


def test_a_settle_the_filesystem_refuses_leaves_a_cooldown_a_cooldown(gate, paths, clock, monkeypatch):
    with provider_gate.command():
        spend_calls(gate, 1)
    data = json.loads(paths[0].read_text())
    data["lifts_at"] = clock.now + 4 * provider_gate.WINDOW_S
    data["tripped_at"] = clock.now
    paths[0].write_text(json.dumps(data))
    clock.now += 2 * provider_gate.WINDOW_S

    def refuse_writes(*args, **kwargs):
        raise OSError(28, "No space left on device")

    # The settle's write is refused, and the refusal is still the cooldown's park.
    with monkeypatch.context() as patched:
        patched.setattr(config, "atomic_write_bytes", refuse_writes)
        with provider_gate.command():
            cooling, sent = refused(gate)
    assert cooling.cause.reason == provider_gate.COOLDOWN and sent == []
    data["lifts_at"] = None
    data["window"] = {ACCOUNT: {str(provider_gate._bucket(clock.now - 2 * provider_gate.WINDOW_S)): 1}}
    paths[0].write_text(json.dumps(data))
    monkeypatch.setattr(config, "atomic_write_bytes", refuse_writes)
    with provider_gate.command(), pytest.raises(OSError):
        gate.call(lambda: Ok())  # the count before the send still raises, as before U278


# ── 3. A reserve for writes and goes ─────────────────────────────────────

def test_a_read_stops_at_the_reserve_while_a_go_still_runs(gate):
    with provider_gate.command():
        spend_calls(gate, 6)
        error, _ = refused(gate)
    assert error.cause.detail["line"] == 6
    with provider_gate.command(reserve=True):
        assert len(spend_calls(gate, 2)) == 2
        at_budget, sent = refused(gate)
    assert sent == []
    assert at_budget.cause.reason == BUDGET
    assert at_budget.cause.detail["line"] == 8


@pytest.mark.parametrize(
    ("scope", "read_mode"),
    [({"reserve": True}, True), ({"calls": 8}, False), ({"calls": 6}, False)],
    ids=["a-write-verb-running-a-read-mode", "calls-up-to-the-budget-on-a-read",
         "a-raised-ceiling-never-spends-the-reserve"],
)
def test_a_read_is_held_to_the_read_line(gate, scope, read_mode):
    """#742: ``--calls`` up to the budget on a read still stops at the reserve line."""
    with provider_gate.command(**scope):
        if read_mode:
            provider_gate.reading()
        assert len(spend_calls(gate, 6)) == 6
        error, sent = refused(gate)
    assert sent == []
    assert error.cause.reason == BUDGET
    assert error.cause.detail["line"] == 6


def test_reading_never_widens_a_read_scope(paths, clock):
    with provider_gate.command() as scope:
        provider_gate.reading()
        assert scope.reserve is False


@pytest.mark.parametrize(("share", "line"), [(0.0, 8), (0.25, 6), (0.5, 4), (0.9, 0)])
def test_the_read_line_is_the_budget_less_the_reserve(share, line):
    settings = GateSettings(calls_per_hour=8, reserve_share=share)
    assert provider_gate.line_for(settings) == line
    assert provider_gate.line_for(settings, reserve=True) == 8


def test_calls_above_the_hours_budget_is_refused_before_any_call(gate):
    with provider_gate.command(calls=9):
        error, sent = refused(gate)
    assert sent == []
    assert error.cause.reason == BUDGET
    assert error.cause.detail["raised"] == 9
    assert error.cause.detail["budget"] == 8
    assert "--calls 8 or lower" in error.cause.remediation.steps[0]


def test_calls_within_the_write_line_runs_for_a_write(gate):
    with provider_gate.command(calls=7, reserve=True):
        assert len(spend_calls(gate, 1)) == 1


def test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child(gate):
    with provider_gate.command(calls_per_hour=16):
        assert os.environ[provider_gate.BUDGET_ENV] == "16"
        assert len(spend_calls(gate, 12)) == 12
        error, _ = refused(gate)
    assert error.cause.detail["budget"] == 16
    assert provider_gate.BUDGET_ENV not in os.environ
    with provider_gate.command():
        back, _ = refused(gate)
    assert back.cause.detail["budget"] == 8


def test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope(gate, monkeypatch):
    """A detached child's library caller reads the raised hour off the environment."""
    monkeypatch.setenv(provider_gate.BUDGET_ENV, "16")
    assert len(spend_calls(gate, 12)) == 12
    error, _ = refused(gate)
    assert error.cause.detail["budget"] == 16


@pytest.mark.parametrize(
    ("per_command", "reserve"),
    [(4, False), (6, True)],
    ids=["never-past-the-hours-budget", "held-to-the-hour-when-doubling-would-pass-it"],
)
def test_a_ceilings_continue_never_names_a_ceiling_past_the_hours_budget(paths, clock, per_command, reserve):
    """A doubled ceiling of six would name twelve, above an hour of eight, so no hour."""
    gate = make_gate(paths, clock, per_command=per_command)
    with provider_gate.command(reserve=reserve):
        spend_calls(gate, per_command)
        error, _ = refused(gate)
    assert error.cause.reason == provider_gate.CEILING
    assert error.cause.detail["higher"] == 8
    assert error.cause.detail["calls_per_hour"] is None


def test_the_budget_reason_is_declared_as_a_policy_refusal():
    assert REASONS[BUDGET] == ExitCode.REFUSED_BY_POLICY


# ── 4. Doctor says where the account stands ──────────────────────────────

def _budget_finding(standing, *, now: float = 1_700_000_000.0):
    asked: list[float] = []
    probes = doctor.Probes(
        provider_standing=lambda at: asked.append(at) or standing,
        now=datetime.fromtimestamp(now, tz=timezone.utc),
    )
    return doctor._check_provider_budget(SimpleNamespace(probes=probes, cfg=None))


def test_doctor_shows_each_identitys_spend_against_its_line_and_the_reserve(paths, clock):
    gate = make_gate(paths, clock, per_hour=1500)
    with provider_gate.command():
        spend_calls(gate, 3)
        spend_calls(gate, 2, identity=APP)
    finding = _budget_finding(provider_gate.read_standing(clock.now, path=paths[0]), now=clock.now)
    assert finding.key == doctor.BUDGET_CHECK
    assert finding.status is doctor.Status.INFO
    assert "3 of 1500 calls on the account" in finding.detail
    assert "2 of 1500 under Cratekit's app credentials" in finding.detail
    assert "reads stop at 1125" in finding.detail
    assert "375 kept for writes and downloads" in finding.detail
    assert "no cooldown" in finding.detail
    assert str(paths[0]) in finding.detail


def test_doctor_names_a_cooldown_and_when_it_lifts(paths, clock):
    paths[0].parent.mkdir(parents=True)
    paths[0].write_text(json.dumps({"tripped_at": clock.now - 60, "lifts_at": clock.now + 840}))
    finding = _budget_finding(provider_gate.read_standing(clock.now, path=paths[0]), now=clock.now)
    assert f"cooling down until {provider_gate._iso(clock.now + 840)}" in finding.detail


def test_doctor_names_an_identity_at_its_read_line_and_when_it_frees(paths, clock):
    oldest = provider_gate._bucket(clock.now - 1800)
    standing = provider_gate.Standing(
        window={ACCOUNT: {oldest: 125, provider_gate._bucket(clock.now): 1000}},
        now=clock.now,
        path=paths[0],
    )
    finding = _budget_finding(standing, now=clock.now)
    frees = oldest + provider_gate.BUCKET_S + provider_gate.WINDOW_S
    assert f"the account is at its read line until {provider_gate.iso(frees)}" in finding.detail
    assert "the app credentials is at" not in finding.detail


def test_doctor_says_an_unreadable_gate_rather_than_nothing_spent(paths, clock):
    paths[0].parent.mkdir(parents=True)
    paths[0].write_text("{not json")
    assert provider_gate.read_standing(clock.now, path=paths[0]) is None
    assert "could not be read" in _budget_finding(None, now=clock.now).detail


# ── 5. A sweep says its cost before it starts ────────────────────────────

def test_a_fresh_kept_listing_costs_nothing_and_an_aged_one_a_call_an_answer(monkeypatch):
    now = [datetime(2026, 11, 12, tzinfo=timezone.utc)]
    monkeypatch.setattr(kept_reads, "clock", lambda: now[0])
    entry = labels.LabelEntry(label_id="tide-works", name="Tide Works")
    assert kept_listing.estimate(entry) is None, "a label never listed has no estimate"
    kept = kept_listing.KeptListing.load(entry)
    kept.keep_named("Act One", [("1", "Act One")])
    kept.keep_named("Act Two", [("2", "Act Two")])
    kept.keep_searched("Tide Works", ["1", "2"])
    kept.flush()
    assert kept_listing.estimate(entry) == 0
    now[0] += kept_reads.KEPT_FOR + timedelta(minutes=1)
    assert kept_listing.estimate(entry) == 3


def _spent_on_the_account(n: int) -> None:
    """Put ``n`` calls in the gate's window: one real, the rest written into its state at once."""
    gate = Gate(GateSettings(min_interval_s=0.0001, calls_per_hour=100_000))
    gate.call(lambda: Ok())
    state, now = gate._read(), time.time()
    for _ in range(n - 1):
        state.count(ACCOUNT, now)
    state.calls += n - 1
    gate._write(state)
    assert gate.window_spend(ACCOUNT) == n


def _configure(monkeypatch, tmp_path, **provider) -> None:
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = ls.valid_data(root)
    data["profile"] = {"name": "full"}
    if provider:
        data["provider"] = provider
    config.save(config.from_dict(data))
    config.reset_cache()


@pytest.fixture
def two_followed(monkeypatch, tmp_path):
    _configure(monkeypatch, tmp_path, calls_per_hour=400, reserve_share=0.25)
    fake = ls.bind(
        monkeypatch,
        {"tide-works": [("r1", "2026", 2)], "deep-current": [("r2", "2026", 2)]},
    )
    ls.register("Tide Works")
    ls.register("Deep Current")
    return fake


def _estimate_check(envelope) -> list[dict]:
    return [c for c in envelope["data"]["checks"] if c["key"] == "label.sync.estimate"]


def test_a_sweep_says_its_estimate_and_runs_when_the_hour_holds_it(two_followed):
    code, envelope = ls.sync("--next")
    assert code == int(ExitCode.OK), envelope
    said = _estimate_check(envelope)
    assert len(said) == 1
    assert "about 200 calls" in said[0]["detail"]
    assert "2 labels" in said[0]["detail"]


def test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call(two_followed,):
    _spent_on_the_account(150)  # 300 is the read line; 150 left, 200 estimated
    code, envelope = ls.sync("--next")
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = envelope["cause"]
    assert cause["reason"] == BUDGET
    assert cause["detail"]["estimate"] == 200
    assert cause["detail"]["left"] == 150
    assert two_followed.asked_for == [], "a label was listed before the refusal"
    assert any("--next --label" in step for step in cause["remediation"]["steps"])


def test_a_genre_walk_is_refused_in_its_own_words_over_its_group_alone(two_followed):
    """U341: the estimate and the refusal speak of the one group asked."""
    labels.RegistryStore().edit("Tide Works", genre="Deep House")
    _spent_on_the_account(250)  # 50 of 300 left; the group is one label at 100
    code, envelope = ls.sync("--next", "--genre", "deep house")
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = envelope["cause"]
    assert cause["message"].startswith(
        "walking the labels of genre 'Deep House' may ask the streaming provider about "
        "100 calls over 1 label,"
    )
    assert cause["detail"]["labels"] == 1
    assert two_followed.asked_for == []


def test_a_genre_walk_at_the_terminal_is_refused_over_its_group_alone(two_followed):
    """U341: the walk's own call site says the group, as ``--next``'s does."""
    labels.RegistryStore().edit("Tide Works", genre="Deep House")
    _spent_on_the_account(250)
    code, envelope = ls.sync("--genre", "Deep House")
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["message"].startswith(
        "walking the labels of genre 'Deep House' may ask the streaming provider about "
        "100 calls over 1 label,"
    )
    assert two_followed.asked_for == []


def test_one_label_named_is_not_held_to_the_sweeps_estimate(two_followed):
    _spent_on_the_account(150)
    code, envelope = ls.sync("--next", "--label", "Tide Works")
    assert code == int(ExitCode.OK), envelope


def test_next_counts_no_label_past_the_first_saved_question(two_followed):
    """``--next`` prints the saved question again with no call, so nothing refuses it."""
    code, first = ls.sync("--next")
    assert code == int(ExitCode.OK), first
    assert first["data"]["summary"]["question"]["label_id"] == "tide-works"
    asked = list(two_followed.asked_for)
    _spent_on_the_account(250)  # 50 of 300 left; Deep Current alone is 100
    code, again = ls.sync("--next")
    assert code == int(ExitCode.OK), again
    assert again["data"]["summary"]["question"]["label_id"] == "tide-works"
    assert two_followed.asked_for == asked, "a label was listed for a saved question"
    (said,) = _estimate_check(again)
    assert "about 0 calls" in said["detail"]


def test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class(gate):
    """A ``run decide --continue`` go spends its verb's declared reserve in process."""
    with provider_gate.command() as outer:
        spend_calls(gate, 6)
        with provider_gate.command(reserve=True) as inner:
            assert inner is outer
            assert len(spend_calls(gate, 2)) == 2
        assert outer.reserve is False
        error, _ = refused(gate)
    assert error.cause.detail["line"] == 6


def test_a_read_dispatched_inside_a_write_runs_under_the_read_line(gate):
    with provider_gate.command(reserve=True) as outer:
        spend_calls(gate, 6)
        with provider_gate.command():
            error, _ = refused(gate)
        assert outer.reserve is True
    assert error.cause.detail["line"] == 6


def test_spending_never_reaches_past_the_class_the_verb_declared(gate):
    with provider_gate.command():
        spend_calls(gate, 6)
        with provider_gate.spending():
            error, _ = refused(gate)
    assert error.cause.detail["line"] == 6
    with provider_gate.command(reserve=True) as scope:
        provider_gate.reading()
        with provider_gate.spending():
            assert len(spend_calls(gate, 2)) == 2
        assert scope.reserve is False


# ── The dispatcher's classes and its --calls refusal ─────────────────────

def _entry_named(name: str):
    return next(one for one in registry.landed_entries() if one.name == name)


@pytest.mark.parametrize(
    ("verb", "report", "spends"),
    [
        ("acquire.download", False, True),
        ("export.playlist", False, True),
        ("organize", False, True),
        ("organize", True, False),
        ("label.sync", False, True),
        ("label.harvest", False, False),
        ("job.resume", False, False),
        ("run.decide", False, False),
        ("doctor", False, False),
    ],
)
def test_these_commands_are_classed_by_their_verbs_writes_and_a_report(verb, report, spends):
    assert cli.spends_reserve(_entry_named(verb), SimpleNamespace(report=report)) is spends


@pytest.fixture
def configured(monkeypatch, tmp_path):
    _configure(monkeypatch, tmp_path)


@pytest.mark.parametrize(
    ("verb", "within", "past"),
    [
        (["job", "resume", "2026-11-12T00:00:00Z-none"], "1500", "1501"),
        (["doctor"], "1200", "1600"),
    ],
    ids=["the-continue-a-parked-job-prints-is-not-refused-by-its-own-calls",
         "refused-before-a-verb-that-makes-no-call-runs"],
)
def test_calls_past_the_budget_is_refused_before_the_verb_runs(configured, verb, within, past):
    """Checked against the hour's budget, so a raised ``--calls`` job resume reaches the job."""
    _, envelope = drive(["--calls", within, *verb])
    assert (envelope.get("cause") or {}).get("reason") != BUDGET, envelope
    code, envelope = drive(["--calls", past, *verb])
    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    assert envelope["cause"]["reason"] == BUDGET
    assert envelope["cause"]["detail"]["budget"] == 1500
    assert envelope["outcome"] == "failed", "a command line to fix is not a park"


def test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs(paths, clock):
    """A run with a raised hour stops at its ceiling, naming that hour beside the ceiling."""
    gate = make_gate(paths, clock, per_command=4)
    with provider_gate.command(calls=6, calls_per_hour=20, reserve=True):
        spend_calls(gate, 6)
        error, _ = refused(gate)
    cause = error.cause
    assert cause.reason == provider_gate.CEILING
    assert cause.detail["higher"] == 12
    assert cause.detail["calls_per_hour"] == 20
    assert "--calls 12 --calls-per-hour 20 job resume JOB_ID" in cause.remediation.steps[0]
    named = dataclasses.replace(cause, detail={**dict(cause.detail), "job_id": "J-1"})
    assert cli.continue_command(["acquire", "download"], _entry_named("acquire.download"), named) == (
        "crate --calls 12 --calls-per-hour 20 job resume J-1"
    )


def test_a_continue_within_the_configured_hour_names_no_hour(paths, clock):
    gate = make_gate(paths, clock, per_command=2)
    with provider_gate.command(reserve=True):
        spend_calls(gate, 2)
        error, _ = refused(gate)
    assert error.cause.detail["calls_per_hour"] is None
    command = cli.continue_command(
        ["--calls-per-hour", "9", "label", "harvest", "X"], _entry_named("label.harvest"), error.cause
    )
    assert command == "crate --calls 4 label harvest X", "a stale hour was carried"


def test_a_crawl_forecast_above_the_hour_names_the_hour():
    def estimate(releases: int, ceiling: int, spent: int) -> playlists_cli.Estimate:
        return playlists_cli.Estimate(
            label_id="x", name="X", releases=releases, pace_s=1.0, kept=0, kept_age="",
            ceiling=ceiling, spent=spent, budget=1500,
        )

    est = estimate(720, 500, 40)
    assert f"--calls {est.one_run} --calls-per-hour {est.one_run} before" in est.shown()["call ceiling"]
    assert "--calls-per-hour" not in estimate(100, 50, 0).shown()["call ceiling"]
