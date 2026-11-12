"""U278: one allowance per account, whatever state is redirected, and a reserve.

On 2026-11-12 a disposable copy, set up with ``CRATEKIT_STATE_DIR`` pointed at
scratch, got a provider gate of its own. Fifty three small commands on it,
each under its own call ceiling, spent about 7,800 catalogue calls in twenty
minutes that the live gate never saw, and the live breaker then refused the
label go Phillip had approved. Five claims, one per requirement of the brief:

1. **One gate per account.** ``provider_gate.json`` and its lock resolve under
   the platform's installation state directory whatever ``CRATEKIT_STATE_DIR``
   says, unless ``CRATEKIT_PROVIDER_GATE_DIR`` names another place; a
   rehearsal shares it and never copies it.
2. **A rolling budget, per identity.** Every call is counted in the gate file
   for the hour it falls in, across commands and processes, and a call past
   the line is not sent and parks as ``provider-budget``, naming the spend,
   the line and when it frees. One identity at its line leaves the other open.
3. **A reserve.** A read stops at ``calls_per_hour * (1 - reserve_share)``,
   a write or a download may spend the rest, and ``--calls`` never reaches
   past the line its class may spend to.
4. **Doctor says where the account stands**, read from the one gate.
5. **A sweep says its cost first**, and refuses before its first call when
   it would cross into the reserve.

Every schedule runs on a fake clock, as the gate's own suite does, except the
two process test, which uses real processes because a lock the kernel holds
cannot be faked.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.core import config, jobs, provider_gate, rehearsal
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.core.provider_gate import ACCOUNT, APP, BUDGET, Gate, GateSettings

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"


class Clock:
    """A wall clock that moves only when something sleeps on it."""

    def __init__(self, start: float = 1_700_000_000.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.now += seconds


class Ok:
    status_code = 200
    headers: dict[str, str] = {}


@pytest.fixture
def clock() -> Clock:
    return Clock()


@pytest.fixture
def paths(tmp_path: Path) -> tuple[Path, Path]:
    return tmp_path / "gate" / "provider_gate.json", tmp_path / "gate" / "provider_gate.lock"


def make_gate(paths, clock, *, per_hour: int = 8, share: float = 0.25) -> Gate:
    state, lock = paths
    return Gate(
        GateSettings(min_interval_s=1.0, calls_per_hour=per_hour, reserve_share=share),
        path=state,
        lock_path=lock,
        clock=clock,
        sleep=clock.sleep,
    )


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


# ═══════════════════════════════════════════════════════════════════════════
# 1. One gate per account, whatever state is redirected
# ═══════════════════════════════════════════════════════════════════════════


def test_a_redirected_state_directory_still_resolves_the_one_gate(monkeypatch, tmp_path):
    """The copy's ``CRATEKIT_STATE_DIR`` moves every other installation entry
    and leaves the gate and its lock where the live run finds them."""
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


def test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate(
    monkeypatch, tmp_path
):
    """The sitting's failure, driven: a call from a copy moves the count a
    live gate reads, and the copy's own state directory holds no gate."""
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
    """``core.rehearsal.redirected`` moves the state directory into its area;
    the gate stays the live one, whether or not the pointer is set, and the
    pointer is left as it was."""
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


# ═══════════════════════════════════════════════════════════════════════════
# 2. A rolling budget, per identity
# ═══════════════════════════════════════════════════════════════════════════


def test_a_call_at_the_line_is_not_sent_and_names_the_spend_and_when_it_frees(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
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
    assert detail["frees_at"] == provider_gate._iso(
        provider_gate._bucket(clock.now - 5) + provider_gate.BUCKET_S + provider_gate.WINDOW_S
    )
    assert "6 calls" in cause.message and "frees at" in cause.message
    assert any("--calls-per-hour" in step for step in cause.remediation.steps)
    assert isinstance(error, jobs.Parked), "the hour's line is a park, never a retry"


def test_the_budget_counts_every_command_and_every_gate_on_the_file(paths, clock):
    """Fifty three small commands are one window, not fifty three."""
    for _ in range(3):
        with provider_gate.command():
            spend_calls(make_gate(paths, clock), 2)
    with provider_gate.command():
        error, sent = refused(make_gate(paths, clock))
    assert error.cause.reason == BUDGET and sent == []


def test_the_window_frees_as_its_oldest_minute_ages_out(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command():
        spend_calls(gate, 6)
        error, _ = refused(gate)
    frees = error.cause.detail["frees_at"]

    clock.now = provider_gate._bucket(1_700_000_000.0) + provider_gate.BUCKET_S + provider_gate.WINDOW_S - 1
    with provider_gate.command():
        still, _ = refused(gate)
    assert still.cause.detail["frees_at"] == frees

    clock.now += 1
    with provider_gate.command():
        assert len(spend_calls(gate, 1)) == 1


def test_one_identity_at_its_line_leaves_the_other_open(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
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
    written = json.loads(state.read_text())
    assert written["calls"] == 9001, "the running total was not kept"


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
    """The breaker keeps its meaning: a trip inside the window refuses as the
    cooldown, never as the budget, and the budget never trips the breaker."""
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


def test_two_processes_count_toward_one_window(paths, tmp_path):
    state, lock = paths
    script = tmp_path / "spender.py"
    script.write_text(
        textwrap.dedent(
            """
            import sys
            from pathlib import Path
            from cratekit.core.provider_gate import Gate, GateSettings

            class Ok:
                status_code = 200
                headers = {}

            state, lock = Path(sys.argv[1]), Path(sys.argv[2])
            gate = Gate(GateSettings(min_interval_s=0.001, calls_per_hour=1000),
                        path=state, lock_path=lock)
            for _ in range(5):
                gate.call(lambda: Ok())
            """
        )
    )
    env = dict(os.environ, PYTHONPATH=str(SRC_ROOT), PYTHONDONTWRITEBYTECODE="1")
    children = [
        subprocess.Popen([sys.executable, str(script), str(state), str(lock)], env=env)
        for _ in range(2)
    ]
    assert [child.wait(timeout=60) for child in children] == [0, 0]
    gate = Gate(GateSettings(), path=state, lock_path=lock)
    assert gate.window_spend(ACCOUNT) == 10


# ═══════════════════════════════════════════════════════════════════════════
# 3. A reserve for writes and goes
# ═══════════════════════════════════════════════════════════════════════════


def test_a_read_stops_at_the_reserve_while_a_go_still_runs(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
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


def test_a_write_verb_running_a_read_mode_is_held_to_the_read_line(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(reserve=True):
        provider_gate.reading()
        spend_calls(gate, 6)
        error, _ = refused(gate)
    assert error.cause.detail["line"] == 6


def test_reading_never_widens_a_read_scope(paths, clock):
    with provider_gate.command() as scope:
        provider_gate.reading()
        assert scope.reserve is False


@pytest.mark.parametrize(("share", "line"), [(0.0, 8), (0.25, 6), (0.5, 4), (0.9, 0)])
def test_the_read_line_is_the_budget_less_the_reserve(share, line):
    assert provider_gate.line_for(GateSettings(calls_per_hour=8, reserve_share=share)) == line
    assert provider_gate.line_for(
        GateSettings(calls_per_hour=8, reserve_share=share), reserve=True
    ) == 8


def test_calls_above_the_hours_budget_is_refused_before_any_call(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(calls=9):
        error, sent = refused(gate)
    assert sent == []
    assert error.cause.reason == BUDGET
    assert error.cause.detail["raised"] == 9
    assert error.cause.detail["budget"] == 8
    assert "--calls 8 or lower" in error.cause.remediation.steps[0]


def test_calls_up_to_the_budget_on_a_read_still_stops_at_the_reserve(paths, clock):
    """The brief: refused only ABOVE the budget; #742: never into the reserve."""
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(calls=8):
        assert len(spend_calls(gate, 6)) == 6
        error, sent = refused(gate)
    assert sent == []
    assert error.cause.reason == BUDGET
    assert error.cause.detail["line"] == 6


def test_calls_within_the_write_line_runs_for_a_write(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(calls=7, reserve=True):
        assert len(spend_calls(gate, 1)) == 1


def test_a_raised_ceiling_never_spends_the_reserve(paths, clock):
    """#742's second point: ``--calls`` on a read stops at the reserve line."""
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(calls=6):
        spend_calls(gate, 6)
        error, _ = refused(gate)
    assert error.cause.reason == BUDGET


def test_the_hour_raised_for_one_run_lasts_that_run_and_reaches_a_child(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(calls_per_hour=16):
        assert os.environ[provider_gate.BUDGET_ENV] == "16"
        assert len(spend_calls(gate, 12)) == 12
        error, _ = refused(gate)
    assert error.cause.detail["budget"] == 16
    assert provider_gate.BUDGET_ENV not in os.environ
    with provider_gate.command():
        back, _ = refused(gate)
    assert back.cause.detail["budget"] == 8


def test_a_ceilings_continue_never_names_a_ceiling_past_the_hours_budget(paths, clock):
    gate = Gate(
        GateSettings(min_interval_s=1.0, calls_per_command=4, calls_per_hour=8, reserve_share=0.25),
        path=paths[0],
        lock_path=paths[1],
        clock=clock,
        sleep=clock.sleep,
    )
    with provider_gate.command():
        spend_calls(gate, 4)
        error, _ = refused(gate)
    assert error.cause.reason == provider_gate.CEILING
    assert error.cause.detail["higher"] == 8


def test_the_budget_reason_is_declared_as_a_policy_refusal():
    assert REASONS[BUDGET] == ExitCode.REFUSED_BY_POLICY


# ═══════════════════════════════════════════════════════════════════════════
# 4. Doctor says where the account stands
# ═══════════════════════════════════════════════════════════════════════════


def _budget_finding(standing, *, now: float = 1_700_000_000.0):
    from datetime import datetime, timezone  # noqa: PLC0415
    from types import SimpleNamespace  # noqa: PLC0415

    from cratekit.cli import doctor  # noqa: PLC0415

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

    from cratekit.cli import doctor  # noqa: PLC0415

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
    paths[0].write_text(
        json.dumps({"tripped_at": clock.now - 60, "lifts_at": clock.now + 840})
    )
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
    finding = _budget_finding(None, now=clock.now)
    assert "could not be read" in finding.detail


# ═══════════════════════════════════════════════════════════════════════════
# 5. A sweep says its cost before it starts
# ═══════════════════════════════════════════════════════════════════════════


def _entry(label_id: str = "tide-works", name: str = "Tide Works"):
    from cratekit.label import registry as labels  # noqa: PLC0415

    return labels.LabelEntry(label_id=label_id, name=name)


def test_a_fresh_kept_listing_costs_nothing_and_an_aged_one_a_call_an_answer(monkeypatch):
    from datetime import datetime, timedelta, timezone  # noqa: PLC0415

    from cratekit.label import kept_listing, kept_reads  # noqa: PLC0415

    now = [datetime(2026, 11, 12, tzinfo=timezone.utc)]
    monkeypatch.setattr(kept_reads, "clock", lambda: now[0])
    entry = _entry()
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
    """Put ``n`` account calls in the one gate's window, as other commands would."""
    gate = Gate(GateSettings(min_interval_s=0.0001, calls_per_hour=100_000))
    for _ in range(n):
        gate.call(lambda: Ok())


@pytest.fixture
def two_followed(monkeypatch, tmp_path):
    from tests import test_label_sync as ls  # noqa: PLC0415

    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = ls.valid_data(root)
    data["profile"] = {"name": "full"}
    data["provider"] = {"calls_per_hour": 400, "reserve_share": 0.25}
    config.save(config.from_dict(data))
    config.reset_cache()
    fake = ls.bind(
        monkeypatch,
        {
            "tide-works": [("r1", "2026", 2)],
            "deep-current": [("r2", "2026", 2)],
        },
    )
    ls.register("Tide Works")
    ls.register("Deep Current")
    return fake


def test_a_sweep_says_its_estimate_and_runs_when_the_hour_holds_it(two_followed):
    from tests import test_label_sync as ls  # noqa: PLC0415

    code, envelope = ls.sync("--next")
    assert code == int(ExitCode.OK), envelope
    said = [c for c in envelope["data"]["checks"] if c["key"] == "label.sync.estimate"]
    assert len(said) == 1
    assert "about 200 calls" in said[0]["detail"]
    assert "2 labels" in said[0]["detail"]


def test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call(
    two_followed,
):
    from tests import test_label_sync as ls  # noqa: PLC0415

    _spent_on_the_account(150)  # 300 is the read line; 150 left, 200 estimated
    code, envelope = ls.sync("--next")

    assert code == int(ExitCode.REFUSED_BY_POLICY), envelope
    cause = envelope["cause"]
    assert cause["reason"] == BUDGET
    assert cause["detail"]["estimate"] == 200
    assert cause["detail"]["left"] == 150
    assert two_followed.asked_for == [], "a label was listed before the refusal"
    assert any("--next --label" in step for step in cause["remediation"]["steps"])


def test_one_label_named_is_not_held_to_the_sweeps_estimate(two_followed):
    from tests import test_label_sync as ls  # noqa: PLC0415

    _spent_on_the_account(150)
    code, envelope = ls.sync("--next", "--label", "Tide Works")
    assert code == int(ExitCode.OK), envelope


def test_a_verb_dispatched_again_inside_a_scope_runs_under_its_own_class(paths, clock):
    """``run decide --continue`` dispatches the run's verb again in its own
    process: a go continued that way spends the reserve its verb declares, and
    the outer command's class comes back after it."""
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command() as outer:
        spend_calls(gate, 6)
        with provider_gate.command(reserve=True) as inner:
            assert inner is outer
            assert len(spend_calls(gate, 2)) == 2
        assert outer.reserve is False
        error, _ = refused(gate)
    assert error.cause.detail["line"] == 6


def test_a_read_dispatched_inside_a_write_runs_under_the_read_line(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command(reserve=True) as outer:
        spend_calls(gate, 6)
        with provider_gate.command():
            error, _ = refused(gate)
        assert outer.reserve is True
    assert error.cause.detail["line"] == 6


def test_spending_never_reaches_past_the_class_the_verb_declared(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
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


def test_next_counts_no_label_past_the_first_saved_question(two_followed):
    """``--next`` prints the first label's saved question again with no call,
    so the labels after it cost nothing and cannot refuse it."""
    from tests import test_label_sync as ls  # noqa: PLC0415

    code, first = ls.sync("--next")
    assert code == int(ExitCode.OK), first
    assert first["data"]["summary"]["question"]["label_id"] == "tide-works"
    asked = list(two_followed.asked_for)

    _spent_on_the_account(250)  # 50 of 300 left; Deep Current alone is 100
    code, again = ls.sync("--next")

    assert code == int(ExitCode.OK), again
    assert again["data"]["summary"]["question"]["label_id"] == "tide-works"
    assert two_followed.asked_for == asked, "a label was listed for a saved question"
    (said,) = [c for c in again["data"]["checks"] if c["key"] == "label.sync.estimate"]
    assert "about 0 calls" in said["detail"]


def test_a_minute_stamped_in_the_future_counts_for_an_hour_from_now_and_no_longer(paths, clock):
    """A clock set back: the calls it stamped ahead still count, so no fresh
    hour, and free an hour after now, never days later (round one, R4)."""
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    ahead = clock.now
    clock.now += 30 * 86_400
    with provider_gate.command():
        spend_calls(gate, 6)
    clock.now = ahead
    with provider_gate.command():
        error, _ = refused(gate)
    frees = provider_gate._bucket(ahead) + provider_gate.BUCKET_S + provider_gate.WINDOW_S
    assert error.cause.detail["frees_at"] == provider_gate.iso(frees)
    clock.now = frees
    with provider_gate.command():
        assert len(spend_calls(gate, 1)) == 1


def test_an_hour_raised_in_the_environment_reaches_a_call_outside_any_scope(
    paths, clock, monkeypatch
):
    """A detached child's library caller reads the raised hour off the environment."""
    monkeypatch.setenv(provider_gate.BUDGET_ENV, "16")
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    assert len(spend_calls(gate, 12)) == 12
    error, _ = refused(gate)
    assert error.cause.detail["budget"] == 16


# ═══════════════════════════════════════════════════════════════════════════
# The dispatcher's classes and its --calls refusal
# ═══════════════════════════════════════════════════════════════════════════


def _entry_named(name: str):
    from cratekit.cli import registry  # noqa: PLC0415

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
def test_these_commands_are_classed_by_their_verbs_writes_and_a_report(
    verb, report, spends
):
    from cratekit import cli  # noqa: PLC0415

    args = SimpleNamespace(report=report)
    assert cli.spends_reserve(_entry_named(verb), args) is spends


@pytest.fixture
def configured(monkeypatch, tmp_path):
    from tests import test_label_sync as ls  # noqa: PLC0415

    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    data = ls.valid_data(root)
    data["profile"] = {"name": "full"}
    config.save(config.from_dict(data))
    config.reset_cache()


def test_the_continue_a_parked_job_prints_is_not_refused_by_its_own_calls(configured):
    """Round one's blocker: ``crate --calls 1500 job resume JOB_ID`` is what a
    download stopped at a raised ceiling prints, and ``job resume`` reads; the
    check is against the hour's budget, so it reaches the job."""
    from tests.cli_drive import drive  # noqa: PLC0415

    _, at_budget = drive(["--calls", "1500", "job", "resume", "2026-11-12T00:00:00Z-none"])
    assert (at_budget.get("cause") or {}).get("reason") != BUDGET, at_budget

    code, past = drive(["--calls", "1501", "job", "resume", "2026-11-12T00:00:00Z-none"])
    assert code == int(ExitCode.REFUSED_BY_POLICY), past
    assert past["cause"]["reason"] == BUDGET
    assert past["cause"]["detail"]["budget"] == 1500


def test_calls_past_the_budget_is_refused_before_a_verb_that_makes_no_call_runs(configured):
    from tests.cli_drive import drive  # noqa: PLC0415

    code, envelope = drive(["--calls", "1200", "doctor"])
    assert (envelope.get("cause") or {}).get("reason") != BUDGET, envelope
    code, envelope = drive(["--calls", "1600", "doctor"])
    assert envelope["cause"]["reason"] == BUDGET
    assert envelope["outcome"] == "failed", "a command line to fix is not a park"


def test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs(paths, clock):
    """Round two's second blocker: a run with its hour raised stops at its
    ceiling, and the continue it names carries that hour beside the ceiling."""
    from cratekit import cli  # noqa: PLC0415

    gate = Gate(
        GateSettings(min_interval_s=1.0, calls_per_command=4, calls_per_hour=8, reserve_share=0.25),
        path=paths[0],
        lock_path=paths[1],
        clock=clock,
        sleep=clock.sleep,
    )
    with provider_gate.command(calls=6, calls_per_hour=20, reserve=True):
        spend_calls(gate, 6)
        error, _ = refused(gate)
    cause = error.cause
    assert cause.reason == provider_gate.CEILING
    assert cause.detail["higher"] == 12
    assert cause.detail["calls_per_hour"] == 20
    assert "--calls 12 --calls-per-hour 20 job resume JOB_ID" in cause.remediation.steps[0]
    import dataclasses  # noqa: PLC0415

    named = dataclasses.replace(cause, detail={**dict(cause.detail), "job_id": "J-1"})
    entry = _entry_named("acquire.download")
    assert cli.continue_command(["acquire", "download"], entry, named) == (
        "crate --calls 12 --calls-per-hour 20 job resume J-1"
    )


def test_a_continue_within_the_configured_hour_names_no_hour(paths, clock):
    from cratekit import cli  # noqa: PLC0415

    gate = Gate(
        GateSettings(min_interval_s=1.0, calls_per_command=2, calls_per_hour=8, reserve_share=0.25),
        path=paths[0],
        lock_path=paths[1],
        clock=clock,
        sleep=clock.sleep,
    )
    with provider_gate.command(reserve=True):
        spend_calls(gate, 2)
        error, _ = refused(gate)
    assert error.cause.detail["calls_per_hour"] is None
    entry = _entry_named("label.harvest")
    command = cli.continue_command(
        ["--calls-per-hour", "9", "label", "harvest", "X"], entry, error.cause
    )
    assert command == "crate --calls 4 label harvest X", "a stale hour was carried"


def test_a_minute_from_the_future_on_the_app_credentials_is_settled_too(paths, clock):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    ahead = clock.now
    clock.now += 30 * 86_400
    with provider_gate.command():
        spend_calls(gate, 6, identity=APP)
    clock.now = ahead
    with provider_gate.command():
        refused(gate, identity=APP)
    clock.now = provider_gate._bucket(ahead) + provider_gate.BUCKET_S + provider_gate.WINDOW_S
    with provider_gate.command():
        assert len(spend_calls(gate, 1, identity=APP)) == 1


def test_a_settle_the_filesystem_refuses_leaves_a_cooldown_a_cooldown(paths, clock, monkeypatch):
    gate = make_gate(paths, clock, per_hour=8, share=0.25)
    with provider_gate.command():
        spend_calls(gate, 1)
    data = json.loads(paths[0].read_text())
    data["lifts_at"] = clock.now + 4 * provider_gate.WINDOW_S
    data["tripped_at"] = clock.now
    paths[0].write_text(json.dumps(data))
    clock.now += 2 * provider_gate.WINDOW_S

    def refuse_writes(*args, **kwargs):
        raise OSError(28, "No space left on device")

    # A minute past the hour wants settling, the write is refused, and the
    # refusal is still the cooldown's park and never an OSError.
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


def test_a_crawl_forecast_above_the_hour_names_the_hour():
    from cratekit.label import playlists_cli  # noqa: PLC0415

    est = playlists_cli.Estimate(
        label_id="x", name="X", releases=720, pace_s=1.0, kept=0, kept_age="",
        ceiling=500, spent=40, budget=1500,
    )
    said = est.shown()["call ceiling"]
    assert f"--calls {est.one_run} --calls-per-hour {est.one_run} before" in said
    small = playlists_cli.Estimate(
        label_id="x", name="X", releases=100, pace_s=1.0, kept=0, kept_age="",
        ceiling=50, spent=0, budget=1500,
    )
    assert "--calls-per-hour" not in small.shown()["call ceiling"]


def test_a_ceilings_continue_is_held_to_the_hour_when_doubling_would_pass_it(paths, clock):
    """Doubled, the ceiling of six would name twelve, above an hour of eight:
    the continue names eight, which the hour holds, and so no hour at all."""
    gate = Gate(
        GateSettings(min_interval_s=1.0, calls_per_command=6, calls_per_hour=8, reserve_share=0.25),
        path=paths[0],
        lock_path=paths[1],
        clock=clock,
        sleep=clock.sleep,
    )
    with provider_gate.command(reserve=True):
        spend_calls(gate, 6)
        error, _ = refused(gate)
    assert error.cause.reason == provider_gate.CEILING
    assert error.cause.detail["higher"] == 8
    assert error.cause.detail["calls_per_hour"] is None
