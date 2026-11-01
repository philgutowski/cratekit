"""U186: a gated database verb says when another run of it holds or just answered its gate.

At sitting 51 two sessions drove ``crate inbox analyzed`` at once and nothing
said the other existed. The write was safe, since the apply plans again on the
write handle and refuses ``decision-stale``, and the second session still lost
twenty minutes finding out why its numbers moved. These tests drive the clear
through the real dispatcher against the disposable database the native landing
suite builds, and read the run records the dispatcher itself persisted.

Nothing here is refused: the warning informs, and the tests say so by
asserting the second run still exits at its gate with the exit code it always
had. D1 applies.
"""

from __future__ import annotations

import io
import json
import os
from datetime import datetime, timedelta, timezone

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


def _answer_aged(run_id: str, age: timedelta) -> str:
    """Move every answer on ``run_id`` back by ``age``; returns the new stamp."""
    state = gates.load(run_id)
    stamp = (datetime.now(timezone.utc) - age).replace(microsecond=0).isoformat()
    state.decisions = {
        name: gates.Decision(d.option, d.actor, stamp, d.digest)
        for name, d in state.decisions.items()
    }
    gates.save(state)
    return stamp


# ---------------------------------------------------------------------------
# The plan at its gate
# ---------------------------------------------------------------------------


def test_with_no_other_run_the_gate_says_nothing_of_one(native_library):
    refused = _planned()

    assert _siblings(refused) == []


def test_an_answer_ten_minutes_ago_is_named_with_its_actor_option_and_time(native_library):
    first = _answered()
    stamp = _answer_aged(first, timedelta(minutes=10))

    refused = _planned()

    # STILL AT ITS GATE, with the code it always had: the warning refuses nothing.
    assert refused["exit_code"] == int(ExitCode.DECISION_REQUIRED)
    assert refused["resumable"] is True
    (message,) = _siblings(refused)
    assert first in message
    assert f"answered {GATE} apply as a-person at {stamp}" in message


def test_an_answer_thirteen_hours_ago_is_history_and_says_nothing(native_library):
    first = _answered()
    _answer_aged(first, timedelta(hours=13))

    assert _siblings(_planned()) == []


def test_an_answer_just_inside_twelve_hours_is_still_named(native_library):
    first = _answered()
    _answer_aged(first, timedelta(hours=11, minutes=50))

    (message,) = _siblings(_planned())
    assert first in message


def test_a_sibling_whose_gate_is_open_is_named_as_open(native_library):
    """Sitting 51's pair: the first plan unanswered when the second one reads."""
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
        other = gates.RunState(
            run_id=f"other-{verb}",
            verb=verb,
            created=datetime.now(timezone.utc).isoformat(),
            open_gate=gate,
        )
        if gate is None:
            other.decisions["inbox.rotate.approve"] = gates.Decision(
                "approve", "a-person", datetime.now(timezone.utc).isoformat(), "sha256:x"
            )
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
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    (gates.run_dir() / "torn.json").write_text("{ not json")

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


# ---------------------------------------------------------------------------
# crate run decide
# ---------------------------------------------------------------------------


def test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan(
    native_library,
):
    first = _answered()
    second = _planned()["run_id"]
    assert gates.load(first).decisions[GATE].digest == gates.load(second).offers[GATE]

    code, decided = drive(["run", "decide", second, GATE, "apply", "--actor", "a-session"])

    assert code == int(ExitCode.OK), decided
    (message,) = _siblings(decided)
    assert first in message and f"answered {GATE} apply as a-person" in message
    # RECORDED ALL THE SAME: the warning informs and refuses nothing.
    assert gates.load(second).decisions[GATE].option == "apply"


def test_decide_says_nothing_when_the_sibling_answered_another_plan(native_library):
    first = _answered()
    state = gates.load(first)
    held = state.decisions[GATE]
    state.decisions[GATE] = gates.Decision(held.option, held.actor, held.recorded, "sha256:other")
    gates.save(state)
    second = _planned()["run_id"]

    code, decided = drive(["run", "decide", second, GATE, "apply", "--actor", "a-session"])

    assert code == int(ExitCode.OK), decided
    assert _siblings(decided) == []


def test_decide_says_nothing_when_the_sibling_aborted(native_library):
    _answered(option="abort")
    second = _planned()["run_id"]

    code, decided = drive(["run", "decide", second, GATE, "apply", "--actor", "a-session"])

    assert code == int(ExitCode.OK), decided
    assert _siblings(decided) == []


def test_decide_says_nothing_when_this_answer_is_abort(native_library):
    _answered()
    second = _planned()["run_id"]

    code, decided = drive(["run", "decide", second, GATE, "abort", "--actor", "a-session"])

    assert code == int(ExitCode.OK), decided
    assert _siblings(decided) == []


def test_decide_says_nothing_over_a_sibling_answered_thirteen_hours_ago(native_library):
    first = _answered()
    _answer_aged(first, timedelta(hours=13))
    second = _planned()["run_id"]

    code, decided = drive(["run", "decide", second, GATE, "apply", "--actor", "a-session"])

    assert code == int(ExitCode.OK), decided
    assert _siblings(decided) == []


def test_decide_continue_carries_the_warning_on_the_verbs_own_envelope(native_library):
    first = _answered()
    second = _planned()["run_id"]

    code, continued = drive(
        ["run", "decide", second, GATE, "apply", "--actor", "a-session", "--continue"]
    )

    assert continued["verb"] == "inbox.analyzed", continued
    found = _siblings(continued)
    assert len(found) == 1 and first in found[0]


# ---------------------------------------------------------------------------
# crate doctor
# ---------------------------------------------------------------------------


def _blocked(run_id: str, verb: str, gate: str, age: timedelta, now: datetime) -> None:
    when = now - age
    gates.save(gates.RunState(run_id=run_id, verb=verb, created=when.isoformat(), open_gate=gate))
    stamp = when.timestamp()
    os.utime(gates.run_path(run_id), (stamp, stamp))


def _open_gates(now: datetime) -> doctor.Finding:
    inputs = doctor._Inputs(None, None, Probes(now=now))
    return doctor.answer(
        next(c for c in doctor.CHECKS if c.key == doctor.OPEN_GATES_CHECK), inputs
    )


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
    finding = _open_gates(datetime.now(timezone.utc))

    assert finding.status is doctor.Status.INFO
    assert "no run" in finding.detail


def test_doctor_says_a_record_it_could_not_read_and_still_never_fails():
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    (gates.run_dir() / "torn.json").write_text("{ not json")

    finding = _open_gates(datetime.now(timezone.utc))

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
    second = _planned()["run_id"]

    record = json.loads(gates.run_path(second).read_text())

    assert gates.SIBLING_RUN not in json.dumps(record)
