"""A stale answer's refusal shows the plan an answer recorded after it applies (R-1334).

``Gates.require`` records the digest it is offered on the run before it
compares a recorded answer, and ``crate run decide`` binds the next answer to
that offer. So after a ``decision-stale`` refusal, an answer recorded on the
run is taken over the MOVED plan, and the resume applies it. The refusal used
to carry the two digests and nothing else, so the plan applied was one no
screen had shown: the review of U222 drove a playlist made between the acts
onto the account that way. The refusal now carries the moved plan exactly as
an open gate shows it, so the screen a person answers is the plan applied.

The same shape one place over, an unknown option inside ``require`` after the
offer was recorded, shows its plan the same way. D1 applies.
"""

from __future__ import annotations

import io
import json

import pytest

from cratekit import cli
from cratekit.cli import gates, registry, render
from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests.test_cli_contract import _trap_standard_input as _trap_standard_input  # noqa: PLC0414
from tests.test_cli_contract import configured as configured  # noqa: PLC0414
from tests.test_cli_contract import library as library  # noqa: PLC0414

SHOWN = "sha256:shown"
MOVED = "sha256:moved"


def _spec(*, explicit: bool = True) -> registry.GateSpec:
    return registry.GateSpec(
        name="stale.probe",
        options=("apply", "abort"),
        prompt="Apply this plan?",
        explicit=explicit,
        digest_source="plan",
    )


def _plan(digest: str, *names: str) -> dict:
    return {"digest": digest, "items": [{"playlist": name} for name in names]}


def _answered(spec: registry.GateSpec | None = None) -> gates.RunState:
    """The first act and the decide: the gate shown over one playlist, answered apply."""
    spec = spec or _spec()
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(spec, plan=_plan(SHOWN, "One"), context={"area": "a"})
    gates.record(state, spec, "apply", actor="a-person")
    return gates.RunState.from_json(json.loads(json.dumps(state.to_json())))


def _stale(state: gates.RunState, plan: dict, **kwargs) -> dict:
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=plan, **kwargs)
    return raised.value.cause.detail


# ---------------------------------------------------------------------------
# The gate layer
# ---------------------------------------------------------------------------


def test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it():
    state = _answered()
    moved = _plan(MOVED, "One", "Made Between The Acts")

    detail = _stale(state, moved, context={"area": "a"})

    assert detail["shown"] == gates.shown_plan(moved, {"area": "a"})
    assert detail["shown"]["digest"] == detail["actual"] == MOVED
    assert detail["expected"] == SHOWN
    assert detail["options"] == ["apply", "abort"]
    assert detail["prompt"] == "Apply this plan?"
    assert detail["explicit"] is True


def test_the_answer_recorded_after_a_stale_refusal_binds_the_plan_it_showed():
    """The decide after the refusal binds the digest on its screen, and that plan applies."""
    state = _answered()
    moved = _plan(MOVED, "One", "Made Between The Acts")
    detail = _stale(state, moved)

    gates.record(state, _spec(), "apply", actor="a-person")

    assert state.decisions["stale.probe"].digest == detail["shown"]["digest"]
    assert gates.Gates(state=state).require(_spec(), plan=moved) == "apply"


def test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan():
    state = _answered()
    _stale(state, _plan(MOVED, "One", "Two"))
    gates.record(state, _spec(), "apply", actor="a-person")
    newer = _plan("sha256:newer", "One", "Two", "Three")

    detail = _stale(state, newer)

    assert detail["expected"] == MOVED
    assert detail["shown"]["items"] == newer["items"]


def test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own():
    """Every existing refusal stays: the code, the reason, the remedy and the message."""
    state = _answered()
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=_plan(MOVED, "Two"))
    cause = raised.value.cause

    assert cause.code is ExitCode.DECISION_STALE
    assert cause.reason == "decision-stale"
    assert str(cause.remediation.remedy) == "replan-then-decide"
    assert cause.message == (
        "the decision on 'stale.probe' was made against a plan that has since changed"
    )
    # The answer recorded before is kept as it was: the refusal decides nothing.
    assert state.decisions["stale.probe"].digest == SHOWN


def test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does():
    """No context and no plan: absent stays absent, and the options still reach the screen."""
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(gates.DecisionRequired) as opened:
        gates.Gates(state=state).require(_spec(), digest=SHOWN)
    gates.record(state, _spec(), "apply", actor="a-person")
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), digest=MOVED)

    assert "shown" not in opened.value.cause.detail
    assert "shown" not in raised.value.cause.detail
    assert raised.value.cause.detail["options"] == ["apply", "abort"]


def test_a_stale_a_verb_raises_itself_keeps_the_detail_it_had():
    """A write handle's own stale, after the gate passed, binds nothing new and shows nothing."""
    cause = gates.DecisionStale(_spec(), "r", SHOWN, MOVED).cause
    assert cause.detail == {"gate": "stale.probe", "run_id": "r", "expected": SHOWN, "actual": MOVED}


def test_a_pinned_stale_keeps_the_detail_it_had():
    """U161's stale moves no digest, so it binds nothing new and is left as it was."""
    state = gates.RunState(run_id="r", verb="probe", created="now")
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(_spec(), plan=_plan(SHOWN, "One"), pinned={"database": "a"})
    gates.record(state, _spec(), "apply", actor="a-person")

    detail = _stale(state, _plan(SHOWN, "One"), pinned={"database": "b"})

    assert detail["pinned"] == "database"
    assert "shown" not in detail and "options" not in detail


def test_an_unknown_inline_option_shows_the_plan_its_offer_recorded():
    """The same shape one place over: the offer is recorded, and the screen invites a decide."""
    spec = _spec(explicit=False)
    state = gates.RunState(run_id="r", verb="probe", created="now")
    plan = _plan(SHOWN, "One")
    with pytest.raises(gates.UnknownOption) as raised:
        gates.Gates(state=state, supplied={spec.name: "bogus"}).require(spec, plan=plan)

    detail = raised.value.cause.detail
    assert detail["shown"] == gates.shown_plan(plan)
    assert state.offers[spec.name] == detail["shown"]["digest"]
    assert detail["options"] == ["apply", "abort"]
    # Its message is the one it had.
    assert raised.value.cause.message == "'bogus' is not an option for 'stale.probe'; it offers apply, abort"


def test_an_unknown_option_raised_outside_require_keeps_the_detail_it_had():
    cause = gates.UnknownOption(_spec(), "bogus").cause
    assert cause.detail == {"gate": "stale.probe", "options": ["apply", "abort"]}


# ---------------------------------------------------------------------------
# The screen a person reads
# ---------------------------------------------------------------------------


def test_the_stale_screen_shows_the_moved_plan_and_the_answer_it_takes():
    state = _answered(_spec(explicit=False))
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(
            _spec(explicit=False), plan=_plan(MOVED, "One", "Made Between The Acts")
        )

    screen = render.render_gate(raised.value.cause)

    assert screen.splitlines()[0] == (
        "The plan moved since this gate was answered. This is the plan this run "
        "reads now, and an answer recorded on the run now is taken over it:"
    )
    assert "playlist=Made Between The Acts" in screen
    assert f"  digest: {MOVED}" in screen
    assert "  answer:  crate run decide r stale.probe <option>" in screen
    # An inline answer is still compared with the recorded one, so it is not offered.
    assert "-d stale.probe" not in screen


def test_the_open_gates_screen_is_unchanged():
    spec = _spec(explicit=False)
    with pytest.raises(gates.DecisionRequired) as raised:
        gates.Gates(state=gates.RunState(run_id="r", verb="probe", created="now")).require(spec)
    assert render.render_gate(raised.value.cause).splitlines() == [
        "Apply this plan?",
        "",
        "  gate:    stale.probe",
        "  options: apply, abort",
        "",
        "  answer:  crate run decide r stale.probe <option>",
        "  then:    add --continue to answer and carry on the run in one command",
        "  or:      rerun with -d stale.probe=<option>",
    ]


# ---------------------------------------------------------------------------
# Through the dispatcher
# ---------------------------------------------------------------------------


def _drive(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(argv, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def _switch_off_by_hand(module: str) -> None:
    document = config.load().to_toml_dict()
    document["modules"] = {module: False}
    config.save(config.from_dict(document))
    config.reset_cache()


def test_through_the_dispatcher_the_stale_refusal_shows_the_moved_plan_and_a_decide_applies_it(
    configured,
):
    """``profile set``'s two acts with a module switched by hand between them."""
    _, out, _ = _drive(["--output", "json", "profile", "set", "slim"])
    run_id = json.loads(out)["run_id"]
    assert _drive(["run", "decide", run_id, "profile.set.apply", "apply"])[0] == 0
    _switch_off_by_hand("analysis")

    code, out, _ = _drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])

    assert code == int(ExitCode.DECISION_STALE)
    detail = json.loads(out)["cause"]["detail"]
    assert detail["shown"]["digest"] == detail["actual"]
    # A person at a terminal is shown the same plan.
    code, _, err = _drive(["--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_STALE)
    assert "The plan moved since this gate was answered" in err
    assert f"digest: {detail['actual']}" in err
    assert f"answer:  crate run decide {run_id} profile.set.apply <option>" in err

    assert _drive(["run", "decide", run_id, "profile.set.apply", "apply"])[0] == 0
    assert gates.load(run_id).decisions["profile.set.apply"].digest == detail["shown"]["digest"]
    code, out, _ = _drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])

    assert code == int(ExitCode.OK), out
    config.reset_cache()
    assert config.load().profile.name == "slim"
