"""A decide on a digest bound gate its run has not reached is refused (R-1349).

``gates.record`` takes an answer's digest from the run's ``offers``, which
only :meth:`Gates.require` fills, when the gate is reached. So a ``crate run
decide`` on a gate the run had not reached yet, the second of two gates for
one, recorded an answer with no digest, ``require`` compares a recorded
digest only when there is one, and the resume applied whatever plan it read
at that gate without its screen ever being shown. The review of R-1334 drove
three folders onto the account that way through ``crate organize``.

The decide is now refused, under its own reason, ``gate-not-reached``, which
is not ``decision-required`` and carries no ``answer-decision`` remedy, so no
screen and no verb reads it as the open gate it is not. A gate reached and
left open, offered or not, still takes an answer, as does a gate the run
already answered, and a gate that binds no plan is unchanged. D1 applies.
"""

from __future__ import annotations

import io
import json

import pytest

from cratekit import cli
from cratekit.cli import gates, registry, render
from cratekit.core.exit_codes import ExitCode
from tests.test_cli_contract import _trap_standard_input as _trap_standard_input  # noqa: PLC0414
from tests.test_cli_contract import configured as configured  # noqa: PLC0414
from tests.test_cli_contract import library as library  # noqa: PLC0414

FIRST = registry.GateSpec(
    name="probe.first",
    options=("apply", "abort"),
    prompt="Apply the first plan?",
    explicit=True,
    digest_source="plan",
)
SECOND = registry.GateSpec(
    name="probe.second",
    options=("apply", "abort"),
    prompt="Apply the second plan?",
    explicit=True,
    digest_source="plan",
)
UNBOUND = registry.GateSpec(
    name="probe.unbound",
    options=("proceed", "abort"),
    prompt="Proceed?",
    explicit=True,
)


def _plan(digest: str) -> dict:
    return {"digest": digest, "items": [{"playlist": digest}]}


def _state(**kwargs) -> gates.RunState:
    return gates.RunState(run_id="r", verb="probe", created="now", **kwargs)


def _open_at_first() -> gates.RunState:
    """The first gate reached and left open over its plan; the second never reached."""
    state = _state(argv=("probe", "--all"))
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(FIRST, plan=_plan("sha256:first"))
    return state


def _refused(state: gates.RunState, spec: registry.GateSpec, option: str = "apply") -> dict:
    before = state.to_json()
    with pytest.raises(gates.GateNotReached) as raised:
        gates.record(state, spec, option, actor="a-person")
    # NOTHING WRITTEN: not the decision, not the open gate.
    assert state.to_json() == before
    return raised.value.cause.to_json()


# ---------------------------------------------------------------------------
# The gate layer
# ---------------------------------------------------------------------------


def test_a_decide_on_a_digest_gate_the_run_has_not_reached_is_refused_and_writes_nothing():
    cause = _refused(_open_at_first(), SECOND)

    assert cause["reason"] == "gate-not-reached"
    assert cause["detail"] == {
        "gate": "probe.second",
        "run_id": "r",
        "verb": "probe",
        "open_gate": "probe.first",
        "continue": "crate --run r probe --all",
    }
    assert "probe.second" in cause["message"] and "probe.first" in cause["message"]


def test_the_refusal_names_the_open_gate_first_and_then_the_run_that_reaches_this_one():
    steps = _refused(_open_at_first(), SECOND)["remediation"]["steps"]

    assert steps == [
        "answer the gate the run waits at first: crate run decide r probe.first <option>",
        "then continue the run: crate --run r probe --all; it puts probe.second and its "
        "plan on the screen if it reaches it, and its report says why if it does not",
        "then, once the run shows probe.second, answer it: crate run decide r probe.second <option>",
    ]


def test_a_run_waiting_at_no_gate_is_told_to_continue_to_this_one():
    state = _state()
    steps = _refused(state, SECOND)["remediation"]["steps"]

    # A run recorded before it kept a command line names the verb's words.
    assert steps == [
        "continue the run: crate --run r probe ...; it puts probe.second and its plan on "
        "the screen if it reaches it, and its report says why if it does not",
        "then, once the run shows probe.second, answer it: crate run decide r probe.second <option>",
    ]


def test_the_refusal_is_not_an_open_gate_to_any_reader():
    """Not ``decision-required``, no answer remedy, no gate screen, its own exit code."""
    with pytest.raises(gates.GateNotReached) as raised:
        gates.record(_open_at_first(), SECOND, "apply", actor="a-person")
    cause = raised.value.cause

    assert cause.reason != "decision-required"
    assert cause.remediation.remedy is None
    assert not render.is_gate_screen(cause)
    assert cause.code == ExitCode.PRECONDITION


def test_an_unknown_option_is_refused_as_it_was_on_a_gate_not_reached():
    with pytest.raises(gates.UnknownOption):
        gates.record(_open_at_first(), SECOND, "maybe", actor="a-person")


def test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed():
    state = _open_at_first()

    gates.record(state, FIRST, "apply", actor="a-person")

    assert state.decisions["probe.first"].digest == "sha256:first"
    assert state.open_gate is None


def test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide():
    state = _state()
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(SECOND)
    assert "probe.second" not in state.offers

    gates.record(state, SECOND, "apply", actor="a-person")

    assert state.decisions["probe.second"].option == "apply"
    assert state.decisions["probe.second"].digest is None
    assert state.open_gate is None


def test_a_gate_already_answered_takes_a_new_answer_once_the_run_waits_elsewhere():
    """Reached with no digest and answered, then the run went on to another gate."""
    state = _state()
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(SECOND)
    gates.record(state, SECOND, "apply", actor="a-person")
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(FIRST, plan=_plan("sha256:first"))

    gates.record(state, SECOND, "abort", actor="a-person")

    assert state.decisions["probe.second"].option == "abort"


def test_a_gate_offered_and_answered_takes_a_new_answer_over_its_offer():
    state = _open_at_first()
    gates.record(state, FIRST, "apply", actor="a-person")
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(SECOND, plan=_plan("sha256:second"))

    gates.record(state, FIRST, "abort", actor="a-person")

    assert state.decisions["probe.first"].option == "abort"
    assert state.decisions["probe.first"].digest == "sha256:first"


def test_a_gate_that_binds_no_plan_takes_an_answer_before_it_is_reached():
    state = _open_at_first()

    gates.record(state, UNBOUND, "proceed", actor="a-person")

    assert state.decisions["probe.unbound"].option == "proceed"
    assert state.open_gate == "probe.first"


def test_a_handed_off_run_holds_the_offer_its_decide_binds(tmp_path, monkeypatch):
    """``hand_off`` mints a run with its offer, so an answer on it is one over a shown plan."""
    handed = _state(offers={"probe.second": "sha256:second"})

    gates.record(handed, SECOND, "abort", actor="a-person")

    assert handed.decisions["probe.second"].digest == "sha256:second"


def test_retire_records_on_an_open_gate_only_so_it_is_untouched():
    """``run retire`` records ``abort`` on a run's open gate, which ``record`` takes."""
    state = _open_at_first()

    gates.record(state, FIRST, gates.RETIRE_OPTION, actor="session")

    assert state.decisions["probe.first"].option == gates.RETIRE_OPTION


# ---------------------------------------------------------------------------
# Through the dispatcher
# ---------------------------------------------------------------------------


def _drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def _unreached(run_id: str) -> gates.RunState:
    """A real verb's run with a digest bound gate it has not reached: profile set's, reset."""
    state = gates.load(run_id)
    state.offers.clear()
    state.open_gate = None
    gates.save(state)
    return state


def test_through_the_dispatcher_the_refusal_saves_nothing_and_prints_no_gate_screen(configured):
    _, out, _ = _drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]
    before = _unreached(run_id).to_json()

    code, out, _ = _drive(["--output", "json", "run", "decide", run_id, "profile.set.apply", "apply"])

    assert code == int(ExitCode.PRECONDITION), out
    assert json.loads(out)["cause"]["reason"] == "gate-not-reached"
    assert gates.load(run_id).to_json() == before

    code, _, err = _drive(["run", "decide", run_id, "profile.set.apply", "apply"])

    assert code == int(ExitCode.PRECONDITION)
    assert "has not reached the gate 'profile.set.apply'" in err
    assert f"crate --run {run_id} profile set slim" in err
    # No gate screen: it would invite the very answer just refused.
    assert "options:" not in err
    assert "answer:  crate run decide" not in err
    assert gates.load(run_id).to_json() == before
