"""U225, pure: a write stopped part way through its order, read back from its run's steps.

The front rule copied from the account adapter is held to the adapter's own,
the orders a stopped write can have left are the ones that rule passes
through, and a record of a write is read back only as this unit writes it.
``tests/test_sync_pair_stopped_order.py`` drives the same rules through the verb.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import itertools
import json
import os
import time
from datetime import UTC, datetime

import pytest

from cratekit.core import held_plan
from cratekit.modules.outbound import tidal_account
from cratekit.sync import pair_cli, pair_stopped
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414

START = ("a", "b", "c", "d", "e")
TARGET = ("d", "a", "e", "b", "c")


# ═══════════════════════════════════════════════════════════════════════════
# The front rule, held to the adapter's
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("before", list(itertools.permutations("abcd")))
def test_the_copied_front_rule_is_the_adapters_on_every_order_of_four(before):
    for asked in (("d", "c", "b", "a"), ("b", "d"), ("a", "x", "c"), ("c", "a", "d", "b")):
        assert pair_stopped.front_moves(list(before), asked) == tidal_account._to_the_front(
            list(before), asked
        ), (before, asked)


def test_the_front_rule_passes_over_a_track_held_twice_or_not_held():
    before = ["a", "b", "a", "c"]
    assert pair_stopped.front_moves(before, ("c", "a", "b", "z")) == tidal_account._to_the_front(
        before, ("c", "a", "b", "z")
    )
    assert "a" not in pair_stopped.front_moves(before, ("c", "a", "b"))


# ═══════════════════════════════════════════════════════════════════════════
# The orders a stopped write can have left
# ═══════════════════════════════════════════════════════════════════════════


def test_every_order_the_moves_pass_through_ends_at_the_target():
    seen = pair_stopped.passed(START, TARGET)
    assert seen[0] == START
    assert seen[-1] == TARGET
    assert len(seen) == len(pair_stopped.front_moves(list(START), TARGET)) + 1
    # Each step is the one before it with one track taken to the front.
    for before, after in itertools.pairwise(seen):
        moved = after[0]
        assert after == (moved, *[one for one in before if one != moved])


def test_the_account_standing_part_way_along_the_moves_is_reached():
    for state in pair_stopped.passed(START, TARGET):
        assert pair_stopped.reached(START, TARGET, state), state


def test_a_move_the_write_never_makes_is_not_reached():
    seen = set(pair_stopped.passed(START, TARGET))
    others = [order for order in itertools.permutations(START) if order not in seen]
    assert others
    for order in others:
        assert not pair_stopped.reached(START, TARGET, order), order


def test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison():
    part = pair_stopped.passed(START, TARGET)[2]
    assert pair_stopped.reached(START, TARGET, (*part, "z"))
    assert pair_stopped.reached(START, TARGET, ("z", *part))
    assert pair_stopped.reached(START, TARGET, tuple(one for one in part if one != "b"))
    # But a move among the tracks both hold is still a move.
    moved = (*part[:3], part[4], part[3])
    assert moved not in set(pair_stopped.passed(START, TARGET))
    assert not pair_stopped.reached(START, TARGET, (*moved, "z"))


def test_finishing_from_part_way_lands_on_the_target_with_an_addition_where_it_stood():
    part = pair_stopped.passed(START, TARGET)[2]
    assert pair_stopped.finished(part, TARGET) == TARGET
    assert pair_stopped.finished((*part, "z"), TARGET) == (*TARGET, "z")
    assert pair_stopped.finished(START, TARGET) == TARGET


# ═══════════════════════════════════════════════════════════════════════════
# The record of a write, read back
# ═══════════════════════════════════════════════════════════════════════════

_WHEN = datetime(2026, 11, 5, 17, 42, 49, tzinfo=UTC)


def _ordering(**changed):
    step = pair_stopped.ordering_step(
        at=_WHEN.isoformat(),
        start=START,
        target=TARGET,
        leader="rekordbox",
        rekordbox=[("1", "r1"), ("2", "r2")],
        written=True,
        links={"t9": "9"},
    )
    step.update(changed)
    return step


def _steps(run_id: str, done: dict) -> held_plan.Steps:
    return held_plan.Steps(run_id, "digest", done)


def _read(*records):
    return pair_stopped.stopped_writes(
        records,
        new=pair_cli.NEW,
        account=pair_cli.STEP_ACCOUNT,
        ordering=pair_cli.STEP_ORDERING,
        made=pair_cli.STEP_MADE,
        done=pair_cli.STEP_DONE,
    )


def test_a_write_begun_ordered_and_not_finished_is_read_back_whole():
    began = (_WHEN.replace(second=40)).isoformat()
    record = _steps("run-1", {"pl-1": {"account": began, "ordering": _ordering()}})
    at, write = _read(record)["pl-1"]
    assert at == _WHEN.replace(second=40)
    assert write == pair_stopped.StoppedWrite(
        run_id="run-1",
        account_id="pl-1",
        at=_WHEN,
        start=START,
        target=TARGET,
        leader="rekordbox",
        rekordbox=(("1", "r1"), ("2", "r2")),
        written=True,
        links={"t9": "9"},
    )


def test_a_finished_or_unordered_write_is_no_stopped_one():
    began = _WHEN.isoformat()
    finished = _steps("run-1", {"pl-1": {"account": began, "ordering": _ordering(), "done": "pl-1"}})
    assert _read(finished) == {}
    unordered = _steps("run-1", {"pl-1": {"account": began}})
    assert _read(unordered) == {}


def test_a_later_run_that_finished_the_pair_hides_the_stopped_write_in_either_order():
    early = _steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering()}})
    later = _WHEN.replace(hour=18).isoformat()
    finished = _steps("run-2", {"pl-1": {"account": later, "done": "pl-1"}})
    assert _read(early, finished) == {}
    assert _read(finished, early) == {}
    # A run that finished the pair before the stopped write began hides nothing.
    earlier = _WHEN.replace(hour=16).isoformat()
    before = _steps("run-0", {"pl-1": {"account": earlier, "done": "pl-1"}})
    assert _read(before, early)["pl-1"][1].run_id == "run-1"


def test_a_later_run_that_stopped_before_its_order_began_hides_nothing():
    """Round one's review: its steps are kept, and it is no finish."""
    early = _steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering()}})
    later = _WHEN.replace(hour=18).isoformat()
    failed = _steps("run-2", {"pl-1": {"account": later, "rekordbox": {}, "queued": ""}})
    assert _read(early, failed)["pl-1"][1].run_id == "run-1"
    assert _read(failed, early)["pl-1"][1].run_id == "run-1"


def test_the_latest_stopped_write_on_a_pair_is_the_one_read():
    early = _steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering()}})
    later = _WHEN.replace(hour=18).isoformat()
    stopped_later = _steps(
        "run-2", {"pl-1": {"account": later, "ordering": _ordering(at=later)}}
    )
    assert _read(early, stopped_later)["pl-1"][1].run_id == "run-2"
    assert _read(stopped_later, early)["pl-1"][1].run_id == "run-2"


def test_a_made_pair_is_read_under_the_account_playlist_it_was_made_as():
    record = _steps(
        "run-1",
        {
            f"{pair_cli.NEW}55": {
                "made": "pl-7",
                "account": _WHEN.isoformat(),
                "ordering": _ordering(),
            }
        },
    )
    assert _read(record)["pl-7"][1].account_id == "pl-7"
    unmade = _steps("run-1", {f"{pair_cli.NEW}55": {"account": _WHEN.isoformat()}})
    assert _read(unmade) == {}


@pytest.mark.parametrize(
    "spoiled",
    [
        {"at": "not a moment"},
        {"from": "a"},
        {"to": ["a", ""]},
        {"leader": 3},
        {"rekordbox": [["1"]]},
        {"rekordbox_written": "yes"},
        {"links": {"t9": ""}},
    ],
)
def test_a_record_not_of_this_form_is_no_stopped_write(spoiled):
    record = _steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering(**spoiled)}})
    assert _read(record) == {}


def test_a_record_from_before_u225_reads_as_no_write_at_all():
    record = _steps("run-1", {"pl-1": {"account": True, "ordering": True}})
    assert _read(record) == {}
    # And a finish recorded with no time hides nothing.
    early = _steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering()}})
    untimed = _steps("run-2", {"pl-1": {"account": True, "done": "pl-1"}})
    assert _read(early, untimed)["pl-1"][1].run_id == "run-1"


# ═══════════════════════════════════════════════════════════════════════════
# Every run's steps, read by a later plan
# ═══════════════════════════════════════════════════════════════════════════


def test_every_kept_runs_steps_are_read_and_an_unreadable_one_is_named(cfg):
    held_plan.Steps("run-a", "d1", {"pl-1": {"account": "x"}}).begin()
    held_plan.Steps("run-b", "d2", {}).begin()
    held_plan.steps_path("run-c").write_text("{not json")
    held_plan.steps_path("run-d").write_text(json.dumps({"version": 99, "run_id": "run-d"}))
    held_plan.steps_path("run-e").write_text(
        json.dumps({"version": held_plan.STEPS_VERSION, "run_id": "run-x", "steps": {}})
    )
    held_plan.steps_path("run-f").write_text(
        json.dumps({"version": held_plan.STEPS_VERSION, "run_id": "run-f", "steps": {"k": 1}})
    )
    records, problems = held_plan.recorded_steps()
    assert sorted(one.run_id for one in records) == ["run-a", "run-b"]
    assert next(one for one in records if one.run_id == "run-a").done == {"pl-1": {"account": "x"}}
    assert len(problems) == 4
    for run_id in ("run-c", "run-d", "run-e", "run-f"):
        assert sum(run_id in problem for problem in problems) == 1, (run_id, problems)


def test_a_record_older_than_a_held_plan_is_kept_is_none(cfg):
    held_plan.Steps("run-old", "d1", {"pl-1": {"account": "x"}}).begin()
    where = held_plan.steps_path("run-old")
    long_ago = time.time() - held_plan.KEEP.total_seconds() - 60
    os.utime(where, (long_ago, long_ago))
    assert held_plan.recorded_steps() == ([], [])
    # A held plan beside it is not a record of steps.
    held_plan.path("run-new").write_text("{}")
    assert held_plan.recorded_steps() == ([], [])
