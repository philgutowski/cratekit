"""An answer bound to the digest its screen showed, and the app's answers always bound (U962).

``crate run decide RUN GATE OPTION --expect-digest D`` records nothing unless the
run offers ``D`` for that gate now, and ``--actor app`` on a gate that binds a
plan is refused without it. Every refusal that held before still holds under
``app``; without either flag the verb is as it was.
"""

from __future__ import annotations

import json

import pytest

from cratekit.cli import gates, registry, render
from cratekit.core import config, session
from cratekit.core.exit_codes import ExitCode
from tests.test_cli_contract import _trap_standard_input as _trap_standard_input  # noqa: PLC0414
from tests.test_cli_contract import configured as configured  # noqa: PLC0414
from tests.test_cli_contract import library as library  # noqa: PLC0414
from tests.test_gate_not_reached import (
    FIRST,
    SECOND,
    UNBOUND,
    _drive,
    _open_at_first,
    _reached,
    _state,
    _unreached,
)

#: The actor the app answers as, spelled as the brief spells it.
APP = "app"
#: ``profile set``'s gate, which binds the plan's digest.
GATE = "profile.set.apply"
SHOWN = "sha256:first"
NEVER_SHOWN = "sha256:never-shown"


def _plan(digest: str) -> dict:
    return {"digest": digest, "items": [{"playlist": digest}]}


def _mismatched(state: gates.RunState, spec: registry.GateSpec, expect: str, actor: str = APP):
    """The cause ``record`` refuses ``expect`` with, the run as it was before."""
    before = state.to_json()
    with pytest.raises(gates.DigestMismatch) as raised:
        gates.record(state, spec, "apply", actor=actor, expect=expect)
    assert state.to_json() == before, "the refusal wrote the decision or touched the gate"
    return raised.value.cause


# The gate layer


def test_an_expected_digest_the_run_offers_records_the_answer_over_it():
    state = _open_at_first()
    gates.record(state, FIRST, "apply", actor=APP, expect=SHOWN)
    answer = state.decisions[FIRST.name]
    assert (answer.option, answer.actor, answer.digest) == ("apply", APP, SHOWN)
    assert state.open_gate is None


def test_an_expected_digest_the_run_does_not_offer_is_refused_naming_both():
    cause = _mismatched(_open_at_first(), FIRST, NEVER_SHOWN)
    assert cause.reason == "decision-digest-mismatch"
    assert cause.code == ExitCode.PRECONDITION
    assert NEVER_SHOWN in cause.message and SHOWN in cause.message
    assert cause.detail == {
        "gate": FIRST.name,
        "run_id": "r",
        "verb": "probe",
        "expected": NEVER_SHOWN,
        "offered": SHOWN,
        "show": "crate run show r",
    }
    assert cause.remediation.steps[0] == "show the gate's current screen: crate run show r"
    assert "--expect-digest" in cause.remediation.steps[1]


def test_the_mismatch_is_not_an_open_gate_to_any_reader():
    """No answer remedy and no screen: either would invite the answer just refused."""
    cause = _mismatched(_open_at_first(), FIRST, NEVER_SHOWN)
    assert cause.reason != "decision-required"
    assert cause.remediation.remedy is None
    assert not render.is_gate_screen(cause)


def test_a_gate_reached_with_no_digest_offers_none_to_expect():
    state = _state()
    _reached(state, SECOND)
    cause = _mismatched(state, SECOND, SHOWN)
    assert cause.detail["offered"] is None
    assert "offers no digest for it" in cause.message


def test_a_gate_that_binds_no_plan_never_offers_the_digest_expected():
    state = _open_at_first()
    before = state.to_json()
    with pytest.raises(gates.DigestMismatch):
        gates.record(state, UNBOUND, "proceed", actor=APP, expect=SHOWN)
    assert state.to_json() == before


def test_an_expected_digest_is_refused_under_any_actor():
    cause = _mismatched(_open_at_first(), FIRST, NEVER_SHOWN, actor="a-person")
    assert cause.reason == "decision-digest-mismatch"


def test_a_gate_not_reached_is_still_refused_as_not_reached_with_a_digest_expected():
    state = _open_at_first()
    before = state.to_json()
    with pytest.raises(gates.GateNotReached):
        gates.record(state, SECOND, "apply", actor=APP, expect=SHOWN)
    assert state.to_json() == before


def test_an_unknown_option_is_still_refused_with_a_digest_expected():
    with pytest.raises(gates.UnknownOption):
        gates.record(_open_at_first(), FIRST, "maybe", actor=APP, expect=SHOWN)


def test_a_bound_answer_is_still_stale_when_the_plan_moves_before_it_is_used():
    state = _open_at_first()
    gates.record(state, FIRST, "apply", actor=APP, expect=SHOWN)
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(FIRST, plan=_plan("sha256:moved"))
    assert raised.value.cause.detail["expected"] == SHOWN


def test_a_bound_answer_is_still_stale_when_a_pinned_fact_moves():
    state = _state()
    _reached(state, FIRST, plan=_plan(SHOWN), pinned={"database": "a"})
    gates.record(state, FIRST, "apply", actor=APP, expect=SHOWN)
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(FIRST, plan=_plan(SHOWN), pinned={"database": "b"})
    assert raised.value.cause.detail["pinned"] == "database"


def test_with_no_digest_expected_the_record_is_as_it_was():
    """The offer the run holds is what binds, whatever screen was shown, as before U962."""
    state = _open_at_first()
    state.offers[FIRST.name] = "sha256:moved"
    gates.record(state, FIRST, "apply", actor="a-person")
    assert state.decisions[FIRST.name].digest == "sha256:moved"


# Through the dispatcher, on profile set's plan gate


def _first_act() -> str:
    code, out, _ = _drive(["--output", "json", "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED), out
    return json.loads(out)["run_id"]


def _shown(run_id: str) -> dict:
    """The gate ``run show`` puts in front of the app, as its JSON carries it (U961)."""
    code, out, _ = _drive(["--output", "json", "run", "show", run_id])
    assert code == int(ExitCode.OK), out
    return json.loads(out)["data"]["summary"]["gate"]


def _decided(run_id: str, *extra: str) -> tuple[int, dict]:
    code, out, _ = _drive(["--output", "json", "run", "decide", run_id, GATE, "apply", *extra])
    return code, json.loads(out)


def _switch_off_by_hand(module: str) -> None:
    document = config.load().to_toml_dict()
    document["modules"] = {module: False}
    config.save(config.from_dict(document))
    config.reset_cache()


def _moved_on_the_screen(run_id: str) -> str:
    """Another process plans the run again over a moved plan; the gate waits over it."""
    _switch_off_by_hand("analysis")
    code, out, _ = _drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_REQUIRED), out
    return _shown(run_id)["digest"]


def _profile() -> str:
    config.reset_cache()
    return config.load().profile.name


def test_the_app_answers_over_the_digest_it_showed_and_the_run_continues(configured):
    run_id = _first_act()
    shown = _shown(run_id)["digest"]
    assert shown is not None

    code, envelope = _decided(run_id, "--actor", APP, "--expect-digest", shown, "--continue")
    assert code == int(ExitCode.OK), envelope
    assert _profile() == "slim"
    answer = gates.load(run_id).decisions[GATE]
    assert (answer.actor, answer.digest) == (APP, shown)
    (note,) = [w for w in envelope["warnings"] if w["code"] == "decision-recorded"]
    assert f"{GATE} answered apply as app on run {run_id}" in note["message"]


def test_a_plan_moved_between_the_show_and_the_answer_is_refused_and_the_run_waits(configured):
    run_id = _first_act()
    shown = _shown(run_id)["digest"]
    moved = _moved_on_the_screen(run_id)
    assert moved != shown
    before = gates.load(run_id).to_json()

    code, envelope = _decided(run_id, "--actor", APP, "--expect-digest", shown, "--continue")
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "decision-digest-mismatch"
    assert shown in cause["message"] and moved in cause["message"]
    assert (cause["detail"]["expected"], cause["detail"]["offered"]) == (shown, moved)
    assert f"crate run show {run_id}" in cause["remediation"]["steps"][0]
    assert not envelope.get("resumable"), envelope
    # Nothing written, nothing continued: the gate still waits over the moved plan.
    assert gates.load(run_id).to_json() == before
    assert GATE not in gates.load(run_id).decisions
    assert _shown(run_id)["digest"] == moved
    assert _profile() != "slim"

    # The app shows the moved plan, and an answer over it is taken.
    code, envelope = _decided(run_id, "--actor", APP, "--expect-digest", moved, "--continue")
    assert code == int(ExitCode.OK), envelope
    assert gates.load(run_id).decisions[GATE].digest == moved


def test_the_mismatch_a_person_reads_names_both_digests_and_no_gate_screen(configured):
    run_id = _first_act()
    shown = _shown(run_id)["digest"]
    moved = _moved_on_the_screen(run_id)

    code, _, err = _drive(["run", "decide", run_id, GATE, "apply", "--expect-digest", shown])
    assert code == int(ExitCode.PRECONDITION)
    assert shown in err and moved in err, err
    assert f"crate run show {run_id}" in err, err
    assert "options:" not in err, "a gate screen invites the very answer just refused"


def test_the_app_answering_a_plan_gate_with_no_digest_is_refused_before_anything_is_recorded(
    configured,
):
    run_id = _first_act()
    before = gates.load(run_id).to_json()

    code, envelope = _decided(run_id, "--actor", APP, "--continue")
    assert code == int(ExitCode.PRECONDITION), envelope
    cause = envelope["cause"]
    assert cause["reason"] == "decision-digest-required"
    assert cause["remediation"]["remedy"] is None
    assert f"crate run show {run_id}" in cause["remediation"]["steps"][0]
    assert "--actor app --expect-digest <digest>" in cause["remediation"]["steps"][1]
    assert gates.load(run_id).to_json() == before
    assert _profile() != "slim"


def test_the_app_on_a_gate_not_reached_is_still_refused(configured):
    run_id = _first_act()
    shown = _shown(run_id)["digest"]
    before = _unreached(run_id).to_json()

    code, envelope = _decided(run_id, "--actor", APP, "--expect-digest", shown)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "gate-not-reached"
    assert gates.load(run_id).to_json() == before


def test_a_stale_plan_at_the_continue_still_refuses_after_a_matching_answer(configured):
    run_id = _first_act()
    shown = _shown(run_id)["digest"]
    code, envelope = _decided(run_id, "--actor", APP, "--expect-digest", shown)
    assert code == int(ExitCode.OK), envelope

    _switch_off_by_hand("analysis")
    code, out, _ = _drive(["--output", "json", "--run", run_id, "profile", "set", "slim"])
    assert code == int(ExitCode.DECISION_STALE), out
    assert json.loads(out)["cause"]["detail"]["expected"] == shown
    assert _profile() != "slim"


def test_the_answer_reads_as_the_apps_in_run_show(configured):
    run_id = _first_act()
    shown = _shown(run_id)["digest"]
    _decided(run_id, "--actor", APP, "--expect-digest", shown)

    code, out, _ = _drive(["--output", "json", "run", "show", run_id])
    rows = {row["key"]: row for row in json.loads(out)["data"]["checks"]}
    assert rows[f"gate.{GATE}"]["detail"] == "apply (recorded by app)"
    code, out, _ = _drive(["run", "show", run_id])
    assert f"gate.{GATE}: apply (recorded by app)" in out, out


def test_a_decide_with_no_flags_binds_whatever_the_run_offers_as_it_did(configured, monkeypatch):
    """A person at a terminal, after the plan moved: the answer binds the offer held now."""
    monkeypatch.setattr(session, "has_controlling_terminal", lambda: True)
    run_id = _first_act()
    _shown(run_id)
    moved = _moved_on_the_screen(run_id)

    code, envelope = _decided(run_id)
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["summary"]["actor"] == "cli"
    assert envelope["data"]["summary"]["actor_because"] == "a terminal, and no --actor"
    answer = gates.load(run_id).decisions[GATE]
    assert (answer.actor, answer.digest) == ("cli", moved)


def test_a_person_who_names_the_digest_is_held_to_it_too(configured):
    run_id = _first_act()
    before = gates.load(run_id).to_json()

    code, envelope = _decided(run_id, "--actor", "a-person", "--expect-digest", NEVER_SHOWN)
    assert code == int(ExitCode.PRECONDITION), envelope
    assert envelope["cause"]["reason"] == "decision-digest-mismatch"
    assert gates.load(run_id).to_json() == before


@pytest.mark.parametrize("actor", ["App", "the-app", "a-person"])
def test_only_the_app_is_held_to_a_digest(configured, actor):
    """Any other actor answers a plan gate with no digest as before."""
    run_id = _first_act()
    code, envelope = _decided(run_id, "--actor", actor)
    assert code == int(ExitCode.OK), envelope
    assert gates.load(run_id).decisions[GATE].actor == actor
