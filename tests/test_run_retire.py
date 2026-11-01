"""U170: old open gates are one line in ``crate status``, and ``crate run retire`` answers them.

Sitting 47 opened ``crate status`` on seventeen open gates from three weeks
before, each a run nobody would resume, above the three lines that mattered.
Status now collapses every open gate idle past a threshold, seven days by
default and ``reports.open_gate_stale_days`` in the file, into one line with
the count and the command, and ``crate run retire --older-than 7d`` answers
each of them ``abort`` as ``session`` after one confirm. A newer gate shows
and stays as before.

Driven through the real dispatcher on a temporary library. A run's age is set
the way it arises, by its ``created`` stamp and its record's last write.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone

import pytest

from cratekit.cli import gates, output, registry
from cratekit.cli.verbs import runs
from cratekit.core import config
from cratekit.core.exit_codes import ExitCode
from tests import test_doctor as doctor_suite
from tests.test_doctor import document_for, drive

#: The temporary library and its saved configuration, by assignment for the
#: reason ``tests/test_run_decide_continue.py`` gives for its own.
library = doctor_suite.library
configured = doctor_suite.configured

CONFIRM = "run.retire.confirm"

#: An ordinary gate, an explicit one, and one that offers no abort.
ORDINARY = ("profile.set", "profile.set.apply")
EXPLICIT = ("tag.remap", "tag.remap.confirm")
NO_ABORT = ("sync.pair", "sync.pair.rekordbox")


def _open(verb_gate: tuple[str, str], *, idle_days: float, started_days: float | None = None) -> str:
    """A run of ``verb`` stopped at ``gate``, started and last written that many days ago."""
    verb, gate = verb_gate
    now = datetime.now(timezone.utc)
    state = gates.new_run(registry.entry(verb))
    state.created = output.timestamp(now - timedelta(days=started_days or idle_days))
    state.open_gate = gate
    path = gates.save(state)
    written = (now - timedelta(days=idle_days)).timestamp()
    os.utime(path, (written, written))
    return state.run_id


def _json(argv: list[str]) -> tuple[int, dict]:
    code, out, err = drive(["--output", "json", *argv])
    assert out.strip(), err
    return code, json.loads(out)


def _status() -> dict:
    code, envelope = _json(["status"])
    assert code == int(ExitCode.OK), envelope
    return envelope["data"]


def _retire(*argv: str) -> tuple[int, dict]:
    return _json(["-d", f"{CONFIRM}=apply", "run", "retire", *argv])


# ---------------------------------------------------------------------------
# crate status
# ---------------------------------------------------------------------------


def test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before(configured):
    old = [_open(ORDINARY, idle_days=20), _open(EXPLICIT, idle_days=10)]
    new = _open(ORDINARY, idle_days=2)

    data = _status()

    keys = [check["key"] for check in data["checks"]]
    assert f"run.{new}" in keys
    assert not {f"run.{one}" for one in old} & set(keys), "an old gate was listed one by one"
    (line,) = [check for check in data["checks"] if check["key"] == "runs.old"]
    assert line["detail"].startswith("2 open gates idle for more than 7 days")
    assert "crate run retire --older-than 7d" in line["detail"]
    assert data["summary"]["open_runs"] == 3
    assert data["summary"]["old_gates"] == 2


def test_the_collapsed_line_names_the_dates_it_spans_and_reaches_a_person(configured):
    _open(ORDINARY, idle_days=20)
    _open(ORDINARY, idle_days=10)
    now = datetime.now(timezone.utc)

    _code, out, err = drive(["status"])
    said = out + err

    first = (now - timedelta(days=20)).date().isoformat()
    last = (now - timedelta(days=10)).date().isoformat()
    assert f"from {first} to {last}" in said
    assert "crate run retire --older-than 7d" in said


def test_status_with_no_old_gate_prints_no_collapsed_line(configured):
    _open(ORDINARY, idle_days=1)
    data = _status()
    assert "runs.old" not in {check["key"] for check in data["checks"]}
    assert data["summary"]["old_gates"] == 0


def test_status_reads_the_threshold_from_the_file(library):
    config.save(config.from_dict({**document_for(library), "reports": {"open_gate_stale_days": 3}}))
    config.reset_cache()
    four = _open(ORDINARY, idle_days=4)
    two = _open(ORDINARY, idle_days=2)

    data = _status()

    keys = {check["key"] for check in data["checks"]}
    assert f"run.{two}" in keys and f"run.{four}" not in keys
    (line,) = [check for check in data["checks"] if check["key"] == "runs.old"]
    assert "1 open gate idle for more than 3 days" in line["detail"]
    assert "crate run retire --older-than 3d" in line["detail"]


def test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed(configured):
    kept = _open(NO_ABORT, idle_days=30)
    data = _status()
    assert f"run.{kept}" in {check["key"] for check in data["checks"]}
    assert "runs.old" not in {check["key"] for check in data["checks"]}


def test_a_run_resumed_recently_is_not_old_however_long_ago_it_started(configured):
    resumed = _open(ORDINARY, idle_days=1, started_days=40)
    assert f"run.{resumed}" in {check["key"] for check in _status()["checks"]}


def test_a_run_started_recently_is_not_old_whatever_its_file_says(configured):
    """The later of the two times wins, so a record copied with an old date is still new."""
    run_id = _open(ORDINARY, idle_days=30, started_days=1)
    assert f"run.{run_id}" in {check["key"] for check in _status()["checks"]}


# ---------------------------------------------------------------------------
# crate run retire
# ---------------------------------------------------------------------------


def test_retire_asks_once_over_every_old_gate_and_answers_only_those(configured):
    old = sorted([_open(ORDINARY, idle_days=20), _open(EXPLICIT, idle_days=9)])
    new = _open(ORDINARY, idle_days=3)

    code, asked = _json(["run", "retire", "--older-than", "7d"])
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    shown = asked["cause"]["detail"]
    assert shown["gate"] == CONFIRM
    assert sorted(item["run_id"] for item in shown["shown"]["items"]) == old

    code, done = _retire("--older-than", "7d")
    assert code == int(ExitCode.OK), done
    assert done["data"]["summary"]["retired"] == 2
    for run_id in old:
        state = gates.load(run_id)
        assert state.open_gate is None
        (decision,) = state.decisions.values()
        assert (decision.option, decision.actor) == ("abort", "session")
    assert gates.load(new).open_gate == ORDINARY[1] and not gates.load(new).decisions
    assert "runs.old" not in {check["key"] for check in _status()["checks"]}


def test_an_explicit_gate_is_retired_with_abort_and_never_apply(configured):
    run_id = _open(EXPLICIT, idle_days=12)

    code, done = _retire()

    assert code == int(ExitCode.OK), done
    decision = gates.load(run_id).decisions[EXPLICIT[1]]
    assert decision.option == "abort" != "apply"
    assert decision.actor == runs.SESSION_ACTOR


def test_retire_lists_what_it_retired_and_what_it_kept(configured):
    retired = _open(ORDINARY, idle_days=10)
    kept = _open(NO_ABORT, idle_days=10)

    code, done = _retire()

    assert code == int(ExitCode.OK), done
    checks = {check["key"]: check for check in done["data"]["checks"]}
    assert checks[f"gate.{retired}.{ORDINARY[1]}"]["status"] == "retired"
    assert checks[f"gate.{kept}.{NO_ABORT[1]}"]["status"] == "kept"
    assert "no abort" in checks[f"gate.{kept}.{NO_ABORT[1]}"]["detail"]
    assert gates.load(kept).open_gate == NO_ABORT[1]
    assert done["data"]["summary"] == {
        "older_than": "7d",
        "retired": 1,
        "kept": 1,
        "unreadable": 0,
    }


def test_retire_with_nothing_old_asks_nothing_and_changes_nothing(configured):
    run_id = _open(ORDINARY, idle_days=2)

    code, envelope = _json(["run", "retire"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert gates.load(run_id).open_gate == ORDINARY[1]


def test_a_declined_retirement_answers_nothing(configured):
    run_id = _open(ORDINARY, idle_days=9)

    code, envelope = _json(["-d", f"{CONFIRM}=abort", "run", "retire"])

    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert gates.load(run_id).open_gate == ORDINARY[1] and not gates.load(run_id).decisions


def test_a_wider_threshold_retires_fewer(configured):
    twenty = _open(ORDINARY, idle_days=20)
    ten = _open(ORDINARY, idle_days=10)

    code, done = _retire("--older-than", "14d")

    assert code == int(ExitCode.OK), done
    assert gates.load(twenty).open_gate is None
    assert gates.load(ten).open_gate == ORDINARY[1]


def test_an_answer_given_over_one_plan_is_stale_once_another_gate_ages_in(configured):
    _open(ORDINARY, idle_days=10)
    code, asked = _json(["run", "retire"])
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    run_id = asked["run_id"]
    code, _out, err = drive(["run", "decide", run_id, CONFIRM, "apply"])
    assert code == int(ExitCode.OK), err

    later = _open(ORDINARY, idle_days=8)
    code, refused = _json(["--run", run_id, "run", "retire"])

    assert code == int(ExitCode.DECISION_STALE), refused
    assert gates.load(later).open_gate == ORDINARY[1]


def test_retire_never_retires_its_own_run(configured):
    """A retirement resumed on its own old run plans every old gate but that one."""
    _open(ORDINARY, idle_days=10)
    code, asked = _json(["run", "retire"])
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    own = asked["run_id"]
    written = (datetime.now(timezone.utc) - timedelta(days=9)).timestamp()
    state = gates.load(own)
    state.created = output.timestamp(datetime.now(timezone.utc) - timedelta(days=9))
    os.utime(gates.save(state), (written, written))

    found, _ = runs.old_gates(
        older_than=timedelta(days=7), now=datetime.now(timezone.utc), skip=own
    )
    assert own not in {one.run_id for one in found}

    code, done = _json(["-d", f"{CONFIRM}=apply", "--run", own, "run", "retire"])
    assert code == int(ExitCode.OK), done
    assert done["data"]["summary"]["retired"] == 1


def test_a_record_retire_cannot_read_is_said_and_not_dropped(configured):
    gates.run_dir().mkdir(parents=True, exist_ok=True)
    (gates.run_dir() / "2026-09-01T00:00:00Z-dead.json").write_text("{not json")
    _open(ORDINARY, idle_days=10)

    code, done = _retire()

    assert code == int(ExitCode.OK), done
    assert done["data"]["summary"]["unreadable"] == 1
    statuses = {check["key"]: check["status"] for check in done["data"]["checks"]}
    assert statuses["run.2026-09-01T00:00:00Z-dead"] == "unreadable"


@pytest.mark.parametrize("given", ["7", "0d", "-3d", "7h", "seven", "3651d", "1.5d"])
def test_an_age_that_is_not_a_whole_number_of_days_is_a_usage_error(configured, capsys, given):
    """The argument parser's refusal, on its own channel, naming the flag and the form."""
    run_id = _open(ORDINARY, idle_days=10)

    code, _out, _err = drive(["run", "retire", f"--older-than={given}"])

    assert code == int(ExitCode.USAGE)
    said = capsys.readouterr().err
    assert "--older-than" in said and "such as 7d" in said
    assert gates.load(run_id).open_gate == ORDINARY[1]


def test_older_than_reads_whole_days():
    assert runs.older_than("7d") == timedelta(days=7)
    assert runs.older_than(f"{config.MAX_OPEN_GATE_STALE_DAYS}d").days == config.MAX_OPEN_GATE_STALE_DAYS


# ---------------------------------------------------------------------------
# the one predicate
# ---------------------------------------------------------------------------


def test_a_gate_exactly_at_the_threshold_is_not_yet_old(configured):
    now = datetime.now(timezone.utc)
    state = gates.new_run(registry.entry(ORDINARY[0]))
    state.created = output.timestamp(now - timedelta(days=30))
    state.open_gate = ORDINARY[1]
    path = gates.save(state)
    at = (now - timedelta(days=7)).timestamp()
    os.utime(path, (at, at))

    assert gates.old_gate(state, path, older_than=timedelta(days=7), now=now) is None
    later = now + timedelta(seconds=1)
    assert gates.old_gate(state, path, older_than=timedelta(days=7), now=later) is not None


def test_a_gate_whose_verb_is_gone_is_old_and_kept(configured):
    run_id = _open(ORDINARY, idle_days=10)
    state = gates.load(run_id)
    state.verb = "no.such.verb"
    path = gates.save(state)
    written = (datetime.now(timezone.utc) - timedelta(days=10)).timestamp()
    os.utime(path, (written, written))

    old = gates.old_gate(state, path, older_than=timedelta(days=7), now=datetime.now(timezone.utc))

    assert old is not None and not old.retirable
    assert "not a verb in this build" in old.kept


def test_a_run_waiting_only_on_a_person_is_never_old(configured):
    state = gates.new_run(registry.entry(ORDINARY[0]))
    state.created = output.timestamp(datetime.now(timezone.utc) - timedelta(days=40))
    path = gates.save(state)
    assert gates.old_gate(state, path, older_than=timedelta(days=7), now=datetime.now(timezone.utc)) is None


# ---------------------------------------------------------------------------
# reports.open_gate_stale_days
# ---------------------------------------------------------------------------


def test_the_threshold_defaults_to_a_week_and_moves_with_the_file(library):
    assert config.from_dict(document_for(library)).reports.open_gate_stale_days == 7
    moved = config.from_dict({**document_for(library), "reports": {"open_gate_stale_days": 21}})
    assert moved.reports.open_gate_stale_days == 21


@pytest.mark.parametrize("value", [0, -1, True, "7", 7.5, config.MAX_OPEN_GATE_STALE_DAYS + 1])
def test_a_threshold_that_is_not_a_positive_whole_number_of_days_is_named(library, value):
    problems = config.validate({**document_for(library), "reports": {"open_gate_stale_days": value}})
    assert len(problems) == 1 and "reports.open_gate_stale_days" in problems[0], problems


def test_the_ceiling_itself_is_a_threshold(library):
    ceiling = config.MAX_OPEN_GATE_STALE_DAYS
    assert config.validate({**document_for(library), "reports": {"open_gate_stale_days": ceiling}}) == []


# ---------------------------------------------------------------------------
# review round one: the guards a first suite left unpinned
# ---------------------------------------------------------------------------


def test_retire_reads_its_default_threshold_from_the_file(library):
    config.save(config.from_dict({**document_for(library), "reports": {"open_gate_stale_days": 3}}))
    config.reset_cache()
    four = _open(ORDINARY, idle_days=4)
    two = _open(ORDINARY, idle_days=2)

    code, done = _retire()

    assert code == int(ExitCode.OK), done
    assert done["data"]["summary"]["older_than"] == "3d"
    assert gates.load(four).open_gate is None
    assert gates.load(two).open_gate == ORDINARY[1]


def test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again(configured):
    """``_retire_one`` reads the run again and records nothing on a gate that moved."""
    run_id = _open(ORDINARY, idle_days=10)
    found, _ = runs.old_gates(older_than=timedelta(days=7), now=datetime.now(timezone.utc))
    (planned,) = found
    code, _out, err = drive(["run", "decide", run_id, ORDINARY[1], "apply", "--actor", "a-person"])
    assert code == int(ExitCode.OK), err

    assert runs._retire_one(planned) is False
    decision = gates.load(run_id).decisions[ORDINARY[1]]
    assert (decision.option, decision.actor) == ("apply", "a-person")
    assert runs._moved_check(planned)["status"] == "moved"


def test_an_answer_is_stale_once_a_planned_run_is_resumed_even_if_it_stays_old(configured):
    """The digest covers when each gate went idle, not only which runs are planned."""
    run_id = _open(ORDINARY, idle_days=20)
    code, asked = _json(["run", "retire"])
    assert code == int(ExitCode.DECISION_REQUIRED), asked
    retire_run = asked["run_id"]
    code, _out, err = drive(["run", "decide", retire_run, CONFIRM, "apply"])
    assert code == int(ExitCode.OK), err

    path = gates.run_path(run_id)
    touched = (datetime.now(timezone.utc) - timedelta(days=12)).timestamp()
    os.utime(path, (touched, touched))
    code, refused = _json(["--run", retire_run, "run", "retire"])

    assert code == int(ExitCode.DECISION_STALE), refused
    assert gates.load(run_id).open_gate == ORDINARY[1]


def test_a_hand_edited_start_stamp_is_aged_by_the_records_last_write(configured):
    run_id = _open(ORDINARY, idle_days=10)
    state = gates.load(run_id)
    state.created = "yesterday"
    path = gates.save(state)
    written = (datetime.now(timezone.utc) - timedelta(days=10)).timestamp()
    os.utime(path, (written, written))

    data = _status()

    assert f"run.{run_id}" not in {check["key"] for check in data["checks"]}
    assert data["summary"]["old_gates"] == 1


def test_a_record_whose_time_cannot_be_read_is_never_old(configured, monkeypatch):
    """Absence of a reading is not age: an unstattable record is as new as now."""
    run_id = _open(ORDINARY, idle_days=30)
    state = gates.load(run_id)

    class Gone:
        def stat(self):
            raise FileNotFoundError(2, "No such file or directory")

    now = datetime.now(timezone.utc)
    assert gates.idle_since(state, Gone()) >= now
    assert gates.old_gate(state, Gone(), older_than=timedelta(days=7), now=now) is None
