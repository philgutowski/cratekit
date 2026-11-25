"""``crate run show`` shows a waiting gate's whole screen from the run record (U961).

The screen a gate refuses with is kept with its run, beside the offer it
binds, so any process shows it without running the verb again.
"""

from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import sys

import pytest

from cratekit.cli import gates, registry, render
from cratekit.cli.verbs import runs
from cratekit.core.exit_codes import ExitCode
from tests.test_cli_contract import SRC_ROOT
from tests.test_cli_contract import _trap_standard_input as _trap_standard_input  # noqa: PLC0414
from tests.test_cli_contract import configured as configured  # noqa: PLC0414
from tests.test_cli_contract import library as library  # noqa: PLC0414
from tests.test_gate_not_reached import _drive, _reached, _state, digest_spec
from tests.test_gate_stale_screen import _switch_off_by_hand

SHOWN = "sha256:shown"
MOVED = "sha256:moved"
GATE = "stale.probe"
PROFILE_GATE = "profile.set.apply"
TO_SLIM = ["profile", "set", "slim"]


def _spec(*, explicit: bool = True) -> registry.GateSpec:
    return digest_spec(GATE, explicit=explicit)


def _plan(digest: str, *names: str) -> dict:
    return {"digest": digest, "items": [{"playlist": name} for name in names]}


def _reloaded(state: gates.RunState) -> gates.RunState:
    """``state`` through the record's own serialization, sorted keys and all."""
    return gates.RunState.from_json(json.loads(json.dumps(state.to_json(), sort_keys=True)))


def _answered(spec: registry.GateSpec | None = None) -> gates.RunState:
    spec = spec or _spec()
    state = _state()
    _reached(state, spec, plan=_plan(SHOWN, "One"), context={"area": "a"})
    gates.record(state, spec, "apply", actor="a-person")
    return _reloaded(state)


# The gate layer: what a refusal keeps
def test_a_refusal_keeps_its_screen_beside_the_offer_it_binds():
    state = _state()
    plan = _plan(SHOWN, "One", "Two")
    cause = _reached(state, _spec(), plan=plan, context={"area": "a"}, pinned={"database": "db-1"})
    screen = state.screens[GATE]
    assert screen.kind == gates.SCREEN_OPEN
    assert (screen.prompt, screen.options, screen.explicit) == (
        "Apply this plan?", ("apply", "abort"), True,
    )
    assert screen.digest == state.offers[GATE] == SHOWN
    assert screen.shown == cause.detail["shown"] == gates.shown_plan(plan, {"area": "a"})
    assert screen.pins == state.pins[GATE] == {"database": "db-1"}
    assert screen.cut is None
    kept = _reloaded(state)
    assert kept.screens == state.screens
    assert gates.waiting(kept) == gates.Waiting(GATE, screen=screen)


def test_the_kept_screen_reads_back_in_the_order_it_was_shown():
    """The record sorts its keys; the screen keeps the order its facts were shown in."""
    state = _state()
    context = {"zeta": 1, "alpha": {"second": 2, "first": 1}}
    _reached(state, _spec(), plan={"digest": SHOWN, "items": [{"title": "t", "artist": "a"}]},
             context=context)
    shown = _reloaded(state).screens[GATE].shown
    assert list(shown) == ["zeta", "alpha", "digest", "count", "items"]
    assert list(shown["alpha"]) == ["second", "first"]
    assert list(shown["items"][0]) == ["title", "artist"]


def test_a_stale_refusal_replaces_the_screen_and_its_offer_together():
    state = _answered()
    moved = _plan(MOVED, "One", "Made Between The Acts")
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=moved, context={"area": "a"})
    screen = state.screens[GATE]
    assert screen.kind == gates.SCREEN_STALE
    assert screen.digest == state.offers[GATE] == MOVED
    assert screen.shown == raised.value.cause.detail["shown"]
    assert [one["playlist"] for one in screen.shown["items"]] == ["One", "Made Between The Acts"]
    # No gate is marked open after a stale refusal, and the run still waits.
    assert state.open_gate is None
    assert gates.waiting(_reloaded(state)) == gates.Waiting(GATE, screen=screen)


def test_an_answer_recorded_drops_the_screen_and_leaves_nothing_waiting():
    """Run records are never pruned, so an answer leaves the record as small as it was."""
    state = _state()
    _reached(state, _spec(), plan=_plan(SHOWN, "One"))
    gates.record(state, _spec(), "apply", actor="a-person")
    assert state.screens == {}
    assert "screens" not in state.to_json(), "a run with nothing waiting kept a screen"
    assert gates.waiting(state) is None, "an answered gate read as waiting"


def test_a_screen_kept_beside_an_answer_over_its_plan_is_not_waiting():
    """The record the dispatcher leaves when a verb fails after its gate passed."""
    state = _state()
    _reached(state, _spec(), plan=_plan(SHOWN, "One"))
    kept = state.screens[GATE]
    gates.record(state, _spec(), "apply", actor="a-person")
    state.screens[GATE] = kept
    assert gates.waiting(state) is None, "an answered gate read as waiting"


def test_a_gate_that_passes_keeps_no_screen():
    spec = _spec(explicit=False)
    state = _state()
    _reached(state, spec, plan=_plan(SHOWN, "One"))
    assert GATE in state.screens
    assert gates.Gates(state=state, supplied={GATE: "apply"}).require(
        spec, plan=_plan(SHOWN, "One")) == "apply"
    assert state.screens == {}


def test_an_unknown_inline_option_keeps_its_screen_and_the_run_waits_on_it():
    spec = _spec(explicit=False)
    state = _state()
    plan = _plan(SHOWN, "One")
    with pytest.raises(gates.UnknownOption) as raised:
        gates.Gates(state=state, supplied={GATE: "bogus"}).require(spec, plan=plan)
    screen = state.screens[GATE]
    assert screen.kind == gates.SCREEN_UNKNOWN_OPTION
    assert screen.shown == raised.value.cause.detail["shown"]
    assert screen.digest == state.offers[GATE] == SHOWN
    assert state.open_gate is None
    assert gates.waiting(_reloaded(state)) == gates.Waiting(GATE, screen=screen)


def test_a_recorded_option_the_gate_no_longer_offers_still_waits_on_its_screen():
    """A decision from a build whose gate offered it: every resume refuses it."""
    state = _answered()
    state.decisions[GATE] = gates.Decision("retired", "a-person", "now", SHOWN)
    with pytest.raises(gates.UnknownOption):
        gates.Gates(state=state).require(_spec(), plan=_plan(SHOWN, "One"))
    assert gates.waiting(state).screen is state.screens[GATE]


# The gate layer: a screen is never shown behind its offer
def test_a_screen_whose_digest_is_not_the_current_offer_is_never_shown():
    state = _state()
    _reached(state, _spec(), plan=_plan(SHOWN, "One"))
    state.offers[GATE] = MOVED
    found = gates.waiting(state)
    assert found.gate == GATE and found.screen is None
    assert "no longer matches the plan and facts" in found.missing


def test_a_screen_whose_pins_are_not_the_runs_is_never_shown():
    state = _state()
    _reached(state, _spec(), plan=_plan(SHOWN, "One"), pinned={"database": "db-1"})
    state.pins[GATE] = {"database": "db-2"}
    assert gates.waiting(state).screen is None


def test_a_gate_reached_with_no_digest_after_a_digest_was_offered_shows_no_screen():
    """The screen carries the plan this call read, and binds no offer: it is not current."""
    state = _state()
    _reached(state, _spec(), plan=_plan(SHOWN, "One"))
    _reached(state, _spec(), context={"area": "read with no digest"})
    assert state.screens[GATE].digest is None
    assert gates.waiting(state).screen is None


def test_the_latest_refusal_is_named_when_two_gates_wait():
    """The open gate's screen stays its own, and the gate the run last refused at is named."""
    first, second = digest_spec("probe.first"), digest_spec("probe.second")
    state = _state()
    _reached(state, second, plan=_plan("sha256:second", "Two"))
    with pytest.raises(gates.UnknownOption):
        gates.Gates(state=state, supplied={"probe.first": "bogus"}).require(
            digest_spec("probe.first", explicit=False), plan=_plan("sha256:first", "One"))
    assert state.open_gate == "probe.second"
    assert gates.waiting(state).gate == first.name
    state.screens["probe.first"] = dataclasses.replace(
        state.screens["probe.first"], saved="2000-01-01T00:00:00+00:00")
    assert gates.waiting(state).gate == second.name


# Records from before this card
def _old_record(**extra) -> dict:
    """A run record as written before U961: no screens key."""
    return {
        "version": gates.RUN_SCHEMA_VERSION, "run_id": "r", "verb": "probe", "created": "now",
        "decisions": {}, "offers": {GATE: SHOWN}, "pending_human_action": None,
        "open_gate": GATE, "argv": ["probe", "--all"], **extra,
    }


def test_a_record_from_before_this_card_loads_unchanged_and_names_its_missing_screen():
    record = _old_record()
    state = gates.RunState.from_json(record)
    assert state.to_json() == record, "an older record changed shape on load"
    found = gates.waiting(state)
    assert (found.gate, found.screen) == (GATE, None)
    assert "no screen of stale.probe that can be shown" in found.missing


def test_a_stale_answer_from_before_this_card_waits_with_its_screen_missing():
    record = _old_record(
        open_gate=None,
        offers={GATE: MOVED},
        decisions={GATE: {"option": "apply", "actor": "cli", "recorded": "now", "digest": SHOWN}},
    )
    found = gates.waiting(gates.RunState.from_json(record))
    assert (found.gate, found.screen) == (GATE, None)


def test_an_unreadable_kept_screen_is_left_out_and_the_gate_named_missing():
    for broken in ("not a screen", {"kind": "open"}, {"shown": "{not json"}):
        state = gates.RunState.from_json(_old_record(screens={GATE: broken}))
        assert state.screens == {}
        assert gates.waiting(state).missing is not None


def test_nothing_waits_on_a_run_that_offered_nothing():
    assert gates.waiting(_state()) is None


# The size bound
def test_a_shown_within_the_limit_is_kept_whole():
    shown = gates.shown_plan(_plan(SHOWN, "One"), {"area": "a"})
    assert gates.cut_shown(shown) == (shown, None)


def test_an_oversized_plan_keeps_its_digest_count_and_first_items_and_says_it_was_cut():
    plan = _plan(SHOWN, *(f"playlist {index:05d} " + "x" * 40 for index in range(5000)))
    shown = gates.shown_plan(plan, {"area": "a", "left": ["one", "two"]})
    kept, cut = gates.cut_shown(shown)
    assert len(gates._compact(kept)) <= gates.SCREEN_LIMIT
    count = len(kept["items"])
    assert 0 < count < 5000
    assert kept["items"] == plan["items"][:count]
    assert (kept["digest"], kept["count"], kept["area"], kept["left"]) == (
        SHOWN, 5000, "a", ["one", "two"])
    assert cut == {"limit": gates.SCREEN_LIMIT, "lists": {"items": {"kept": count, "left_out": 5000 - count}}}
    # As many as fit: one more passes the limit.
    longer = {**kept, "items": plan["items"][: count + 1]}
    assert len(gates._compact(longer)) > gates.SCREEN_LIMIT
    assert list(kept) == list(shown), "the cut reordered the facts"


def test_facts_too_large_to_keep_leave_only_the_digest_and_the_count():
    shown = {"note": "y" * (gates.SCREEN_LIMIT + 1), "digest": SHOWN, "count": 3, "items": []}
    kept, cut = gates.cut_shown(shown)
    assert kept == {"digest": SHOWN, "count": 3}
    assert cut == {"limit": gates.SCREEN_LIMIT, "dropped": ["note", "items"]}


def test_an_oversized_plan_is_kept_cut_in_the_record_its_refusal_saves():
    plan = _plan(SHOWN, *(f"playlist {index:05d} " + "x" * 40 for index in range(5000)))
    state = _state()
    cause = _reached(state, _spec(), plan=plan)
    assert len(cause.detail["shown"]["items"]) == 5000, "the refusal itself was cut"
    screen = _reloaded(state).screens[GATE]
    assert (screen.digest, screen.shown["digest"], screen.shown["count"]) == (SHOWN, SHOWN, 5000)
    assert screen.cut["lists"]["items"]["left_out"] == 5000 - len(screen.shown["items"])
    assert len(json.dumps(state.to_json())) < 2 * gates.SCREEN_LIMIT


# Through the dispatcher
def _json(argv: list[str]) -> tuple[int, dict]:
    code, out, _ = _drive(["--output", "json", *argv])
    return code, json.loads(out)


def _gate_of(run_id: str) -> dict | None:
    code, shown = _json(["run", "show", run_id])
    assert code == int(ExitCode.OK), shown
    return shown["data"]["summary"]["gate"]


def _in_another_process(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "cratekit.cli", *argv], capture_output=True, text=True,
        stdin=subprocess.DEVNULL, env={**os.environ, "PYTHONPATH": str(SRC_ROOT)},
    )


def test_run_show_in_another_process_shows_the_screen_the_refusal_carried(configured):
    refused = _in_another_process("--output", "json", *TO_SLIM)
    assert refused.returncode == int(ExitCode.DECISION_REQUIRED), refused.stderr
    envelope = json.loads(refused.stdout)
    detail, run_id = envelope["cause"]["detail"], envelope["run_id"]
    shown = _in_another_process("--output", "json", "run", "show", run_id)
    assert shown.returncode == int(ExitCode.OK), shown.stderr
    gate = json.loads(shown.stdout)["data"]["summary"]["gate"]
    assert gate == {
        "name": PROFILE_GATE,
        "kind": "open",
        "prompt": detail["prompt"],
        "options": detail["options"],
        "explicit": detail["explicit"],
        "digest": detail["shown"]["digest"],
        "shown": detail["shown"],
        "pins": {},
        "cut": None,
        "writes_database": False,
        "answer": f"crate run decide {run_id} {PROFILE_GATE} <option>",
        "continue": gates.continue_command(gates.load(run_id)),
        "screen_missing": None,
    }
    assert gates.load(run_id).offers[PROFILE_GATE] == gate["digest"]


def _printed(err: str, first: str) -> str:
    """The gate screen a refusal printed to a person, from its first line to the end."""
    return err[err.rindex(first):]


def test_run_show_prints_the_screen_the_refusal_printed(configured):
    """Line for line, in the order the verb showed its facts, which JSON sorts."""
    code, refused = _json(TO_SLIM)
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    code, _, err = _drive(["--run", run_id, *TO_SLIM])
    assert code == int(ExitCode.DECISION_REQUIRED)
    printed = _printed(err, refused["cause"]["detail"]["prompt"])
    assert printed == render.render_gate(gates.DecisionRequired(
        registry.entry("profile.set").gates[0], run_id, gates.load(run_id).screens[PROFILE_GATE].shown,
    ).cause)
    code, out, _ = _drive(["run", "show", run_id])
    assert code == int(ExitCode.OK)
    assert printed in out


def test_an_answer_recorded_and_the_run_continued_leaves_no_gate(configured):
    _, refused = _json(TO_SLIM)
    run_id = refused["run_id"]
    assert _drive(["run", "decide", run_id, PROFILE_GATE, "apply"])[0] == 0
    assert _gate_of(run_id) is None
    assert _drive(["--run", run_id, *TO_SLIM])[0] == 0
    assert _gate_of(run_id) is None
    assert "screens" not in json.loads(gates.run_path(run_id).read_text())


def test_a_stale_refusal_shows_in_run_show_as_the_moved_plan(configured):
    _, refused = _json(TO_SLIM)
    run_id = refused["run_id"]
    assert _drive(["run", "decide", run_id, PROFILE_GATE, "apply"])[0] == 0
    _switch_off_by_hand("analysis")
    code, stale = _json(["--run", run_id, *TO_SLIM])
    assert code == int(ExitCode.DECISION_STALE)
    detail = stale["cause"]["detail"]
    gate = _gate_of(run_id)
    assert (gate["kind"], gate["digest"], gate["shown"]) == (
        "stale", detail["actual"], detail["shown"])
    _, _, err = _drive(["--run", run_id, *TO_SLIM])
    printed = _printed(err, render.STALE_SCREEN)
    _, out, _ = _drive(["run", "show", run_id])
    assert printed in out
    # Answered over the screen it showed, the moved plan applies and nothing waits.
    assert _drive(["run", "decide", run_id, PROFILE_GATE, "apply"])[0] == 0
    assert gates.load(run_id).decisions[PROFILE_GATE].digest == gate["digest"]
    assert _gate_of(run_id) is None


def test_an_unknown_option_shows_in_run_show_with_its_prompt_and_its_run(configured):
    code, refused = _json(["-d", f"{PROFILE_GATE}=bogus", *TO_SLIM])
    assert code == int(ExitCode.DECISION_REQUIRED)
    run_id = refused["run_id"]
    gate = _gate_of(run_id)
    assert (gate["kind"], gate["shown"]) == ("unknown-option", refused["cause"]["detail"]["shown"])
    assert gate["prompt"] == registry.entry("profile.set").gates[0].prompt
    _, out, _ = _drive(["run", "show", run_id])
    assert f"answer:  crate run decide {run_id} {PROFILE_GATE} <option>" in out
    assert "<run>" not in out


def test_a_run_from_before_this_card_shows_its_missing_screen_and_the_command(configured):
    _, refused = _json(TO_SLIM)
    run_id = refused["run_id"]
    record = json.loads(gates.run_path(run_id).read_text())
    del record["screens"]
    gates.run_path(run_id).write_text(json.dumps(record))
    gate = _gate_of(run_id)
    command = gates.continue_command(gates.load(run_id))
    assert gate["screen_missing"]["command"] == command
    assert "no screen of profile.set.apply that can be shown" in gate["screen_missing"]["reason"]
    assert (gate["digest"], gate["shown"], gate["pins"], gate["kind"]) == (None, None, None, None)
    assert gate["options"] == ["apply", "abort"]
    _, out, _ = _drive(["run", "show", run_id])
    assert "with no screen to show" in out and f"show it: {command}" in out
    assert "  digest:" not in out


def _saved_cut_run() -> tuple[str, registry.Entry]:
    """A database writer's run left at its gate over a plan past the limit."""
    owner = next(
        one for one in registry.ENTRIES
        if gates.writes_the_database(one.name)
        and any(spec.digest_source is not None for spec in one.gates)
    )
    spec = next(one for one in owner.gates if one.digest_source is not None)
    state = gates.RunState(run_id="cut-run", verb=owner.name, created="2026-11-25T00:00:00+00:00",
                           argv=tuple(owner.name.split(".")))
    plan = _plan(SHOWN, *(f"playlist {index:05d} " + "x" * 40 for index in range(5000)))
    _reached(state, spec, plan=plan)
    gates.save(state)
    return state.run_id, owner


def test_a_cut_screen_says_so_in_run_show_and_names_the_whole_plans_command(configured):
    run_id, owner = _saved_cut_run()
    gate = _gate_of(run_id)
    assert gate["writes_database"] is True
    assert (gate["digest"], gate["shown"]["count"]) == (SHOWN, 5000)
    assert gate["cut"]["lists"]["items"]["left_out"] == 5000 - len(gate["shown"]["items"])
    _, out, _ = _drive(["run", "show", run_id])
    assert out.index("The run kept this screen short") < out.index("  items:")
    assert f"  whole:   {gates.continue_command(gates.load(run_id))}" in out


def test_run_show_stays_on_its_declared_surface(configured):
    from cratekit.cli import output

    _, refused = _json(TO_SLIM)
    _, shown = _json(["run", "show", refused["run_id"]])
    assert shown["data"]["summary"]["gate"] is not None
    assert output.envelope_problems(shown) == []


def test_the_gate_is_read_by_one_reader():
    """``run show`` builds its gate from :func:`gates.waiting` alone."""
    assert runs.waiting_gate(_state()) is None
