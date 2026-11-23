"""A gate's answer binds to the facts it pins outside the digest, such as the database file."""

from __future__ import annotations

import json

import pytest

from cratekit.cli import gates
from tests.test_gate_not_reached import _state, digest_spec

LIVE = "/library/db/master.db"
COPY = "/library/rehearsal/master.db"


def _spec():
    return digest_spec("pinned.probe")


def _plan() -> dict:
    return {"digest": "sha256:same", "items": [{"a": 1}], "totals": {"count": 1}}


def _offered(pinned: dict[str, str] | None) -> gates.RunState:
    """The first act: the gate refuses open, and the person answers apply."""
    state = _state()
    with pytest.raises(gates.DecisionRequired):
        gates.Gates(state=state).require(_spec(), plan=_plan(), pinned=pinned)
    gates.record(state, _spec(), "apply", actor="a-person")
    return gates.RunState.from_json(json.loads(json.dumps(state.to_json())))


def test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json():
    state = _offered({"database": LIVE})
    assert state.pins == {"pinned.probe": {"database": LIVE}}
    assert state.decisions["pinned.probe"].digest == "sha256:same"


def test_a_run_no_pinning_gate_reached_keeps_the_record_it_had():
    state = _offered(None)
    assert "pins" not in state.to_json()
    assert state.pins == {}


def test_the_same_pin_on_the_continuation_takes_the_recorded_answer():
    state = _offered({"database": LIVE})
    chosen = gates.Gates(state=state).require(_spec(), plan=_plan(), pinned={"database": LIVE})
    assert chosen == "apply"


def test_another_pin_with_the_same_digest_is_stale_and_names_both_values():
    state = _offered({"database": LIVE})
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=_plan(), pinned={"database": COPY})
    cause = raised.value.cause
    assert cause.reason == "decision-stale"
    assert cause.detail["pinned"] == "database"
    assert cause.detail["expected"] == LIVE and cause.detail["actual"] == COPY
    assert LIVE in cause.message and COPY in cause.message
    assert state.pins == {"pinned.probe": {"database": LIVE}}, "the refused pin replaced it"


def test_an_answer_whose_run_pinned_nothing_is_stale_to_a_gate_that_now_pins():
    """Absence is not agreement: a run recorded with no pin answered over no file."""
    state = _offered(None)
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=_plan(), pinned={"database": LIVE})
    assert raised.value.cause.detail["expected"] == ""
    assert raised.value.cause.detail["actual"] == LIVE


def test_a_pinned_run_asked_with_no_pin_is_stale_too():
    state = _offered({"database": LIVE})
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=_plan())
    assert raised.value.cause.detail["pinned"] == "database"


def test_a_moved_digest_is_still_refused_before_the_pin_is_read():
    state = _offered({"database": LIVE})
    moved = {**_plan(), "digest": "sha256:other"}
    with pytest.raises(gates.DecisionStale) as raised:
        gates.Gates(state=state).require(_spec(), plan=moved, pinned={"database": LIVE})
    assert "pinned" not in raised.value.cause.detail
    assert raised.value.cause.detail["actual"] == "sha256:other"
