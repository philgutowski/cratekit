"""A gated database verb says when another run of it holds or just answered its gate (U186). The
apply already refuses ``decision-stale``; the warning tells a second session why its numbers
moved, and refuses nothing. D1 applies."""

from __future__ import annotations

import io
import json
import os
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from cratekit import cli
from cratekit.cli import doctor, gates, registry
from cratekit.cli.doctor import Probes
from cratekit.core.exit_codes import ExitCode
from cratekit.intake import analyzed_cli
from tests.cli_drive import drive
from tests.test_intake_land_native import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_intake_land_native import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_intake_land_native import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_intake_land_native import library as library  # noqa: PLC0414
from tests.test_intake_land_native import machine as machine  # noqa: PLC0414
from tests.test_intake_land_native import native_library as native_library  # noqa: PLC0414

VERB = ["inbox", "analyzed"]
GATE = analyzed_cli.APPROVE_GATE


def _planned() -> dict:
    """One plan of the clear, left at its gate, as a session's first command leaves it."""
    code, refused = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused


def _answered(option: str = "apply", actor: str = "a-person") -> str:
    """A plan answered by its second act and never continued, so its gate is closed."""
    run_id = _planned()["run_id"]
    code, decided = drive(["run", "decide", run_id, GATE, option, "--actor", actor])
    assert code == int(ExitCode.OK), decided
    return run_id


def _siblings(envelope: dict) -> list[str]:
    return [w["message"] for w in envelope["warnings"] if w["code"] == gates.SIBLING_RUN]


def _rewritten(run_id: str, *, gate: str | None = None, offers: dict | None = None, **fields):
    """Each answer on ``run_id`` with ``fields`` replaced, under ``gate`` if named, offers too."""
    state = gates.load(run_id)
    state.decisions = {gate or name: replace(d, **fields) for name, d in state.decisions.items()}
    if offers is not None:
        state.offers = offers
    gates.save(state)


def _answer_aged(run_id: str, age: timedelta) -> str:
    """Move every answer on ``run_id`` back by ``age``; returns the new stamp."""
    stamp = (datetime.now(timezone.utc) - age).replace(microsecond=0).isoformat()
    _rewritten(run_id, recorded=stamp)
    return stamp


def _decided(run_id: str, option: str = "apply", *more: str) -> tuple[int, dict]:
    return drive(["run", "decide", run_id, GATE, option, "--actor", "a-session", *more])


def _torn(name: str, text: str) -> None:
    """A run record nobody can read, left in the run folder."""
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    (gates.run_dir() / f"{name}.json").write_text(text)


# The plan at its gate
def test_with_no_other_run_the_gate_says_nothing_of_one(native_library):
    assert _siblings(_planned()) == []


def test_an_answer_ten_minutes_ago_is_named_with_its_actor_option_and_time(native_library):
    first = _answered()
    stamp = _answer_aged(first, timedelta(minutes=10))
    refused = _planned()
    # Still at its gate, with its usual code: the warning refuses nothing.
    assert refused["exit_code"] == int(ExitCode.DECISION_REQUIRED)
    assert refused["resumable"] is True
    (message,) = _siblings(refused)
    assert first in message
    assert f"answered {GATE} apply as a-person at {stamp}" in message


def test_an_answer_thirteen_hours_ago_is_history_and_says_nothing(native_library):
    _answer_aged(_answered(), timedelta(hours=13))
    assert _siblings(_planned()) == []


def test_an_answer_just_inside_twelve_hours_is_still_named(native_library):
    first = _answered()
    _answer_aged(first, timedelta(hours=11, minutes=50))
    (message,) = _siblings(_planned())
    assert first in message


def test_a_sibling_whose_gate_is_open_is_named_as_open(native_library):
    """The first plan is unanswered when the second one reads."""
    first = _planned()["run_id"]
    (message,) = _siblings(_planned())
    assert first in message
    assert f"holds the gate {GATE} open since" in message
    assert "unanswered" in message


def test_one_warning_per_other_run(native_library):
    open_one = _planned()["run_id"]
    answered = _answered()
    found = _siblings(_planned())
    assert len(found) == 2
    assert any(open_one in m and "open since" in m for m in found)
    assert any(answered in m and "answered" in m for m in found)


def test_a_run_of_another_verb_is_never_named(native_library):
    for verb, gate in (("inbox.refill", "inbox.refill.approve"), ("inbox.rotate", None)):
        now = datetime.now(timezone.utc).isoformat
        other = gates.RunState(run_id=f"other-{verb}", verb=verb, created=now(), open_gate=gate)
        if gate is None:
            answer = gates.Decision("approve", "a-person", now(), "sha256:x")
            other.decisions["inbox.rotate.approve"] = answer
        gates.save(other)
    assert _siblings(_planned()) == []


def test_a_run_never_warns_about_itself(native_library):
    """The same run continued to its gate again is the asker, not a sibling."""
    run_id = _planned()["run_id"]
    code, again = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), again
    assert again["run_id"] == run_id
    assert _siblings(again) == []


def test_a_record_that_cannot_be_read_is_said_rather_than_read_as_no_run(native_library):
    _torn("torn", "{ not json")
    (message,) = _siblings(_planned())
    assert "1 run record could not be read (torn)" in message
    assert "inbox.analyzed" in message


def test_the_warning_prints_on_the_screen_a_person_reads(native_library):
    first = _planned()["run_id"]
    out, err = io.StringIO(), io.StringIO()
    code = cli.run(VERB, stdout=out, stderr=err)
    assert code == int(ExitCode.DECISION_REQUIRED)
    lines = [line for line in err.getvalue().splitlines() if line.startswith("warning [")]
    assert any(line.startswith(f"warning [{gates.SIBLING_RUN}]:") and first in line for line in lines)


def test_a_verb_that_writes_no_database_is_outside_the_warning():
    """The scope is the brief's, a verb declaring a database writing surface."""
    assert gates.writes_the_database("inbox.analyzed") is True
    assert gates.writes_the_database("session.ack") is False
    assert gates.writes_the_database("no.such.verb") is False


# crate run decide
def test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan(native_library):
    first = _answered()
    second = _planned()["run_id"]
    assert gates.load(first).decisions[GATE].digest == gates.load(second).offers[GATE]
    code, decided = _decided(second)
    assert code == int(ExitCode.OK), decided
    (message,) = _siblings(decided)
    assert first in message and f"answered {GATE} apply as a-person" in message
    # Recorded all the same: the warning informs and refuses nothing.
    assert gates.load(second).decisions[GATE].option == "apply"


def test_an_answer_the_app_gave_is_named_as_the_apps_at_the_gate_and_at_decide(native_library):
    """U962: the app answers over the digest it showed, and its sibling reads ``as app``."""
    first = _planned()["run_id"]
    shown = gates.load(first).offers[GATE]
    code, decided = drive(
        ["run", "decide", first, GATE, "apply", "--actor", "app", "--expect-digest", shown]
    )
    assert code == int(ExitCode.OK), decided
    second = _planned()
    (message,) = _siblings(second)
    assert first in message and f"answered {GATE} apply as app at" in message
    code, decided = _decided(second["run_id"])
    assert code == int(ExitCode.OK), decided
    (message,) = _siblings(decided)
    assert first in message and f"answered {GATE} apply as app" in message


#: The siblings a decide says nothing of: how the sibling is left, this run's offers, its answer.
QUIET = {
    "the-sibling-answered-another-plan":
        (lambda: _rewritten(_answered(), digest="sha256:other"), None, "apply"),
    "the-sibling-aborted": (lambda: _answered(option="abort"), None, "apply"),
    "this-answer-is-abort": (_answered, None, "abort"),
    "a-sibling-answered-thirteen-hours-ago":
        (lambda: _answer_aged(_answered(), timedelta(hours=13)), None, "apply"),
    "both-answers-are-abort": (lambda: _answered(option="abort"), None, "abort"),
    "this-run-was-offered-no-digest": (lambda: _rewritten(_answered(), digest=None), {}, "apply"),
    "the-sibling-answered-another-gate":
        (lambda: _rewritten(_answered(), gate="another.gate"), None, "apply"),
}


@pytest.mark.parametrize(("sibling", "offers", "option"), QUIET.values(), ids=list(QUIET))
def test_decide_says_nothing_of_a_sibling_whose_answer_this_one_does_not_repeat(
    native_library, sibling, offers, option):
    sibling()
    second = _planned()["run_id"]
    if offers is not None:
        _rewritten(second, offers=offers)
    code, decided = _decided(second, option)
    assert code == int(ExitCode.OK), decided
    assert _siblings(decided) == []


def test_decide_continue_carries_the_warning_on_the_verbs_own_envelope(native_library):
    first = _answered()
    code, continued = _decided(_planned()["run_id"], "apply", "--continue")
    assert continued["verb"] == "inbox.analyzed", continued
    found = _siblings(continued)
    assert len(found) == 1 and first in found[0]


# crate doctor
def _blocked(run_id: str, verb: str, gate: str, age: timedelta, now: datetime) -> None:
    when = now - age
    gates.save(gates.RunState(run_id=run_id, verb=verb, created=when.isoformat(), open_gate=gate))
    stamp = when.timestamp()
    os.utime(gates.run_path(run_id), (stamp, stamp))


def _open_gates(now: datetime | None = None) -> doctor.Finding:
    inputs = doctor._Inputs(None, None, Probes(now=now or datetime.now(timezone.utc)))
    return doctor.answer(next(c for c in doctor.CHECKS if c.key == doctor.OPEN_GATES_CHECK), inputs)


def test_doctor_lists_a_gate_open_two_days_and_not_one_open_an_hour():
    now = datetime.now(timezone.utc)
    _blocked("old-plan", "inbox.analyzed", GATE, timedelta(days=2), now)
    _blocked("new-plan", "inbox.analyzed", GATE, timedelta(hours=1), now)
    finding = _open_gates(now)
    assert finding.status is doctor.Status.INFO
    assert "old-plan" in finding.detail
    assert "inbox.analyzed" in finding.detail
    assert "2 days" in finding.detail
    assert "new-plan" not in finding.detail


def test_doctor_names_a_session_ack_left_blocked_as_sitting_51_left_one():
    now = datetime.now(timezone.utc)
    _blocked("second-ack", "session.ack", "session.ack.backup", timedelta(days=3), now)
    finding = _open_gates(now)
    assert finding.status is doctor.Status.INFO
    assert "second-ack" in finding.detail and "session.ack" in finding.detail


def test_doctor_with_no_runs_says_none_has_sat_at_a_gate():
    finding = _open_gates()
    assert finding.status is doctor.Status.INFO
    assert "no run" in finding.detail


def test_doctor_says_a_record_it_could_not_read_and_still_never_fails():
    _torn("torn", "{ not json")
    finding = _open_gates()
    assert finding.status is doctor.Status.INFO
    assert "could not be read" in finding.detail and "torn" in finding.detail


def test_an_answered_run_two_days_old_is_not_blocked():
    now = datetime.now(timezone.utc)
    _blocked("done", "inbox.analyzed", GATE, timedelta(days=2), now)
    state = gates.load("done")
    gates.record(state, next(g for g in registry.entry("inbox.analyzed").gates if g.name == GATE), "apply", actor="x")
    gates.save(state)
    os.utime(gates.run_path("done"), ((now - timedelta(days=2)).timestamp(),) * 2)
    assert "done" not in _open_gates(now).detail


def test_the_run_record_carries_the_sibling_warning_nowhere(native_library):
    """No new state: the warning is computed, never written into a record."""
    _planned()
    record = json.loads(gates.run_path(_planned()["run_id"]).read_text())
    assert gates.SIBLING_RUN not in json.dumps(record)


# Edge cases of the warning's scope
def _old_open(run_id: str, age: timedelta) -> None:
    """An inbox clear left at its gate ``age`` ago."""
    _blocked(run_id, "inbox.analyzed", GATE, age, datetime.now(timezone.utc))


def test_a_verb_writing_no_database_says_nothing_of_its_own_siblings():
    """``run retire`` is gated and writes no database row, so its second plan is silent."""
    _old_open("left-plan", timedelta(days=3))
    code, first = drive(["run", "retire", "--older-than", "1d"])
    assert code == int(ExitCode.DECISION_REQUIRED), first
    code, second = drive(["run", "retire", "--older-than", "1d"])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert first["run_id"] not in json.dumps(second["warnings"])
    assert _siblings(second) == []


def test_a_refusal_before_the_gate_names_no_sibling(machine):
    """Only a run persisted at its gate warns; a verb refused earlier is not at one."""
    _old_open("left-plan", timedelta(hours=1))
    code, refused = drive(VERB)
    assert code not in (int(ExitCode.OK), int(ExitCode.DECISION_REQUIRED)), refused
    assert _siblings(refused) == []


def test_a_reading_that_breaks_says_so_and_leaves_the_gate_as_it_was(native_library, monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("a probe")
    monkeypatch.setattr(gates, "siblings", broken)
    refused = _planned()
    assert refused["exit_code"] == int(ExitCode.DECISION_REQUIRED)
    assert refused["resumable"] is True
    assert refused["cause"]["reason"] == "decision-required"
    (message,) = _siblings(refused)
    assert "could not be read (RuntimeError: a probe)" in message


def test_an_answer_with_no_recorded_time_is_named_as_unrecorded(native_library):
    first = _answered()
    _rewritten(first, recorded="")
    (message,) = _siblings(_planned())
    assert first in message and "at an unrecorded time" in message


def test_a_record_missing_a_field_is_named_unreadable_at_the_gate_and_in_doctor(native_library):
    _torn("half", json.dumps({"version": 1, "run_id": "half"}))
    (message,) = _siblings(_planned())
    finding = _open_gates()
    assert "could not be read (half)" in message
    assert finding.status is doctor.Status.INFO
    assert "could not be read (half)" in finding.detail


def test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate(native_library):
    """An approved plan stays approved when the run stops again at the cloud sync gate."""
    first = _answered()
    state = gates.load(first)
    state.open_gate = "write.cloudsync.unreadable"
    gates.save(state)
    code, decided = _decided(_planned()["run_id"])
    assert code == int(ExitCode.OK), decided
    (message,) = _siblings(decided)
    assert first in message
    # Named by the answer that put it there, and by the gate it waits at.
    assert f"answered {GATE} apply as a-person" in message
    assert "holds the gate write.cloudsync.unreadable open since" in message
    assert "unanswered" not in message


def test_decide_continue_says_a_sibling_once_when_the_verb_stops_at_its_gate_again(native_library):
    """The answer was over a plan the continuation no longer reads, so it stops stale, the
    sibling named once."""
    first = _answered()
    _rewritten(first, digest="sha256:moved")
    second = _planned()["run_id"]
    _rewritten(second, offers={GATE: "sha256:moved"})
    code, continued = _decided(second, "apply", "--continue")
    assert code == int(ExitCode.DECISION_STALE), continued
    found = _siblings(continued)
    assert len(found) == 1 and first in found[0]


def test_doctor_leaves_a_gate_open_twenty_hours_off_the_list():
    now = datetime.now(timezone.utc)
    _blocked("this-morning", "inbox.analyzed", GATE, timedelta(hours=20), now)
    finding = _open_gates(now)
    assert "this-morning" not in finding.detail
    assert "no run has sat at a gate for more than a day" in finding.detail
