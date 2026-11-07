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


# ═══════════════════════════════════════════════════════════════════════════
# R-1372: a pair's steps carried past its run
# ═══════════════════════════════════════════════════════════════════════════


def _age(where, days: int = 31) -> None:
    then = time.time() - days * 86400
    os.utime(where, (then, then))


def test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age(cfg):
    steps = held_plan.Steps("run-a", "d1", {"pl-1": {"account": "x", "ordering": {"at": "y"}}})
    steps.done["pl-2"] = {"account": "z"}
    held_plan.carry(steps, "pl-1")
    where = held_plan.carried_path("run-a", "pl-1")
    assert where.parent == held_plan.carried_dir()
    _age(where, 400)
    records, problems = held_plan.carried()
    assert problems == []
    assert [(one.run_id, one.digest, one.done) for one in records] == [
        ("run-a", "d1", {"pl-1": {"account": "x", "ordering": {"at": "y"}}})
    ]


def test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked(cfg):
    steps = held_plan.Steps("run-a", "d1", {"pl-1": {"account": "x"}})
    steps.begin()
    held_plan.carry(steps, "pl-1")
    held_plan.path("run-a").write_text("{}")
    for where in (held_plan.path("run-a"), held_plan.steps_path("run-a"),
                  held_plan.carried_path("run-a", "pl-1")):
        _age(where)
    assert held_plan.prune() == 2
    held_plan.release("run-a")
    assert held_plan.carried_path("run-a", "pl-1").exists()
    assert held_plan.let_go("run-a", "pl-1") is True
    assert not held_plan.carried_path("run-a", "pl-1").exists()
    # A record already gone is let go.
    assert held_plan.let_go("run-a", "pl-1") is True
    assert held_plan.carried() == ([], [])


def test_two_items_of_one_run_are_carried_apart(cfg):
    steps = held_plan.Steps("run-a", "d1", {"pl-1": {"account": "x"}, "new:9": {"made": "pl-9"}})
    held_plan.carry(steps, "pl-1")
    held_plan.carry(steps, "new:9")
    records, _problems = held_plan.carried()
    assert sorted(next(iter(one.done)) for one in records) == ["new:9", "pl-1"]
    held_plan.let_go("run-a", "pl-1")
    records, _problems = held_plan.carried()
    assert [one.done for one in records] == [{"new:9": {"made": "pl-9"}}]


def test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write(cfg):
    held_plan.carry(held_plan.Steps("run-a", "d1", {"pl-1": {"account": "x"}}), "pl-1")
    directory = held_plan.carried_dir()
    (directory / "run-b.0123.json").write_text("{not json")
    (directory / "run-c.0123.json").write_text(json.dumps({"version": 99}))
    moved = held_plan.carried_path("run-d", "pl-4")
    moved.write_text(
        json.dumps(
            {
                "version": held_plan.CARRIED_VERSION,
                "run_id": "run-d",
                "digest": "d",
                "key": "pl-5",
                "steps": {},
            }
        )
    )
    unkeyed = held_plan.carried_path("run-e", "pl-5")
    unkeyed.write_text(
        json.dumps(
            {
                "version": held_plan.CARRIED_VERSION,
                "run_id": "run-e",
                "digest": "d",
                "key": "pl-5",
                "steps": [],
            }
        )
    )
    records, problems = held_plan.carried()
    assert [one.run_id for one in records] == ["run-a"]
    assert len(problems) == 4, problems
    for run_id in ("run-b", "run-c", "run-d", "run-e"):
        assert sum(run_id in problem for problem in problems) == 1, (run_id, problems)


def test_a_carry_that_cannot_be_written_raises(cfg, monkeypatch):
    from cratekit.core import config

    def refused(payload, where, **_kw):
        raise PermissionError("read only")

    monkeypatch.setattr(config, "atomic_write_bytes", refused)
    with pytest.raises(OSError):
        held_plan.carry(held_plan.Steps("run-a", "d1", {"pl-1": {}}), "pl-1")


def _passed(records, account_id: str, moment: datetime):
    return pair_stopped.passed_by(
        records,
        account_id=account_id,
        moment=moment,
        new=pair_cli.NEW,
        account=pair_cli.STEP_ACCOUNT,
        made=pair_cli.STEP_MADE,
    )


def test_a_snapshot_passes_the_carried_records_of_its_pair_that_began_before_it():
    from datetime import timedelta

    before = _WHEN.isoformat()
    after = (_WHEN + timedelta(seconds=5)).isoformat()
    records = [
        _steps("run-1", {"pl-1": {"account": before, "ordering": _ordering()}}),
        _steps("run-2", {"pl-1": {"account": after, "ordering": _ordering()}}),
        _steps("run-3", {"pl-2": {"account": before}}),
        _steps("run-4", {f"{pair_cli.NEW}x": {"made": "pl-1", "account": before}}),
        _steps("run-5", {f"{pair_cli.NEW}y": {"account": before}}),
        _steps("run-6", {"pl-1": {"account": True}}),
    ]
    moment = _WHEN + timedelta(seconds=1)
    assert _passed(records, "pl-1", moment) == [("run-1", "pl-1"), ("run-4", f"{pair_cli.NEW}x")]
    # A snapshot at the very moment a write began passes it, as the plan reads it.
    assert _passed(records, "pl-1", _WHEN) == [("run-1", "pl-1"), ("run-4", f"{pair_cli.NEW}x")]
    assert _passed(records, "pl-9", moment) == []


def test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop():
    """A carried record outlives a pair forgotten and marked again, and is not the new pair's."""
    from datetime import timedelta
    from types import SimpleNamespace

    write = _read(_steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering()}}))
    reader = SimpleNamespace(stopped=(write, ()))

    def read(marked: str, synced: str = ""):
        held = SimpleNamespace(marked=marked, synced=synced)
        return pair_cli._Reader.stopped_write(reader, "pl-1", held)

    assert read((_WHEN + timedelta(seconds=1)).isoformat()) is None
    assert read((_WHEN - timedelta(seconds=1)).isoformat()).run_id == "run-1"
    # Marked the same moment the write began is the pair it began on.
    assert read(_WHEN.isoformat()).run_id == "run-1"
    # A mark that cannot be read as a moment leaves the snapshot to decide.
    assert read("").run_id == "run-1"
    assert read("", synced=(_WHEN - timedelta(seconds=1)).isoformat()).run_id == "run-1"
    assert read("", synced=(_WHEN + timedelta(seconds=1)).isoformat()) is None


def test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark():
    """R-1376: a pair released after a stop and paired again has no snapshot, and the stop predates the mark."""
    from datetime import timedelta
    from types import SimpleNamespace

    write = _read(_steps("run-1", {"pl-1": {"account": _WHEN.isoformat(), "ordering": _ordering()}}))
    reader = SimpleNamespace(stopped=(write, ()))
    assert pair_cli._Reader.first_stop(reader, "pl-1").run_id == "run-1"
    assert pair_cli._Reader.first_stop(reader, "pl-9") is None
    # An account side still to be made has no playlist to have stopped on.
    assert pair_cli._Reader.first_stop(reader, "") is None
    # The pair's own rule still keeps it from a pair marked after it.
    held = SimpleNamespace(marked=(_WHEN + timedelta(seconds=1)).isoformat(), synced="")
    assert pair_cli._Reader.stopped_write(reader, "pl-1", held) is None


def test_a_carried_record_naming_another_run_is_named(cfg):
    where = held_plan.carried_path("run-f", "pl-6")
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text(
        json.dumps(
            {
                "version": held_plan.CARRIED_VERSION,
                "run_id": "run-x",
                "digest": "d",
                "key": "pl-6",
                "steps": {},
            }
        )
    )
    records, problems = held_plan.carried()
    assert records == []
    assert len(problems) == 1 and "run-f" in problems[0], problems


def test_a_carried_directory_that_cannot_be_listed_is_named_never_read_as_none(cfg):
    """No directory is no record; one that cannot be listed says so (the round one review)."""
    assert held_plan.carried() == ([], [])
    where = held_plan.carried_dir()
    where.parent.mkdir(parents=True, exist_ok=True)
    where.write_text("not a directory")
    records, problems = held_plan.carried()
    assert records == []
    assert len(problems) == 1 and "could not be listed" in problems[0], problems


def test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan(cfg):
    """The run's steps say whether the pair finished, which the copy, taken before, cannot."""
    began = {"account": _WHEN.isoformat(), "ordering": _ordering()}
    held_plan.Steps("run-1", "d1", {"pl-1": {**began, "done": "pl-1"}}).begin()
    held_plan.carry(held_plan.Steps("run-1", "d1", {"pl-1": dict(began)}), "pl-1")
    stopped, unread = pair_cli._Reader.stopped.func(None)
    assert unread == ()
    assert stopped == {}, "a pair its own run finished is read as stopped from its copy"
    # Steps under another plan of the same run are not the copy's run as it wrote.
    held_plan.Steps("run-1", "d2", {"pl-1": {**began, "done": "pl-1"}}).begin()
    stopped, _unread = pair_cli._Reader.stopped.func(None)
    assert stopped["pl-1"][1].run_id == "run-1"


# ═══════════════════════════════════════════════════════════════════════════
# R-1394: how far a pending write's moves can have got
# ═══════════════════════════════════════════════════════════════════════════


def test_positions_counts_the_moves_that_leave_each_order_on_the_path():
    seen = pair_stopped.passed(START, TARGET)
    for index, state in enumerate(seen):
        assert pair_stopped.positions(START, TARGET, state) == (index,), state
    assert pair_stopped.positions(START, TARGET, ("e", "d", "c", "b", "a")) == ()
    # A track added since is left out, as reached leaves it out.
    assert pair_stopped.positions(START, TARGET, ("z", *seen[2])) == (2,)


def test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count():
    # The first move fronts e and the second a, back in front of it; with e
    # taken off since, the order before them and after each read the same.
    seen = pair_stopped.passed(START, TARGET)
    assert seen[1][0] == "e"
    shown = tuple(one for one in seen[0] if one != "e")
    assert pair_stopped.positions(START, TARGET, shown) == (0, 1, 2)


def _pending(moving: dict, *, moved: bool = False):
    began = _WHEN.replace(second=40).isoformat()
    steps = {"account": began, "ordering": _ordering(), "moving": moving}
    if moved:
        steps["moved"] = began
    record = _steps("run-1", {"pl-1": steps})
    found = pair_stopped.stopped_writes(
        [record],
        new=pair_cli.NEW,
        account=pair_cli.STEP_ACCOUNT,
        ordering=pair_cli.STEP_ORDERING,
        made=pair_cli.STEP_MADE,
        done=pair_cli.STEP_DONE,
        moving=pair_cli.STEP_MOVING,
        moved=pair_cli.STEP_MOVED,
    )
    return found["pl-1"][1]


def _moving(**counts):
    return pair_stopped.moving_step(at=_WHEN.isoformat(), start=START, end=TARGET, **counts)


def test_a_moving_step_reads_back_its_counts():
    write = _pending(_moving(sent=2, landed=1))
    assert (write.landed, write.sent) == (1, 2)
    assert write.pending and not write.moved


def test_every_move_accepted_reads_as_every_move_landed_whatever_the_counts():
    total = len(pair_stopped.front_moves(START, TARGET))
    write = _pending(_moving(sent=1, landed=0), moved=True)
    assert (write.landed, write.sent) == (total, total)


@pytest.mark.parametrize(
    "counts",
    [
        {},
        {"sent": "2", "landed": 1},
        {"sent": 1, "landed": 2},
        {"sent": 99, "landed": 0},
        {"sent": 2, "landed": -1},
        {"sent": True, "landed": 0},
    ],
)
def test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known(counts):
    moving = _moving()
    moving.pop(pair_stopped.SENT)
    moving.pop(pair_stopped.LANDED)
    moving.update(counts)
    write = _pending(moving)
    assert (write.landed, write.sent) == (0, len(pair_stopped.front_moves(START, TARGET)))


def _read_moving(*records):
    return pair_stopped.stopped_writes(
        records,
        new=pair_cli.NEW,
        account=pair_cli.STEP_ACCOUNT,
        ordering=pair_cli.STEP_ORDERING,
        made=pair_cli.STEP_MADE,
        done=pair_cli.STEP_DONE,
        moving=pair_cli.STEP_MOVING,
        moved=pair_cli.STEP_MOVED,
    )


def test_a_later_write_that_sent_no_move_does_not_hide_a_pending_one():
    """R-1394, round two: a refused finish left the account where the pending moves left it."""
    early = _WHEN.replace(second=40).isoformat()
    pending = _steps(
        "run-1",
        {"pl-1": {"account": early, "ordering": _ordering(), "moving": _moving(sent=1, landed=1)}},
    )
    later = _WHEN.replace(hour=18).isoformat()
    refused = _steps("run-2", {"pl-1": {"account": later, "ordering": _ordering(at=later)}})
    for records in ((pending, refused), (refused, pending)):
        write = _read_moving(*records)["pl-1"][1]
        assert write.run_id == "run-1" and write.pending, records
    # A later write that did send moves is the one read, as before.
    sending = _steps(
        "run-3",
        {
            "pl-1": {
                "account": later,
                "ordering": _ordering(at=later),
                "moving": _moving(sent=1, landed=0),
            }
        },
    )
    assert _read_moving(pending, sending)["pl-1"][1].run_id == "run-3"


# ═══════════════════════════════════════════════════════════════════════════
# U234. A reading kept after a stop, and what shows a reorder against it
# ═══════════════════════════════════════════════════════════════════════════


def test_a_reading_in_another_order_is_a_reorder():
    assert pair_stopped.reordered(["t1", "t2", "t3"], ["t2", "t1", "t3"])
    assert not pair_stopped.reordered(["t1", "t2", "t3"], ["t1", "t2", "t3"])


def test_a_track_added_or_taken_off_between_two_readings_is_no_reorder():
    assert not pair_stopped.reordered(["t1", "t2", "t3"], ["t1", "t9", "t2", "t3"])
    assert not pair_stopped.reordered(["t1", "t2", "t3"], ["t1", "t3"])
    assert pair_stopped.reordered(["t1", "t2", "t3"], ["t9", "t3", "t1"])


def test_two_readings_sharing_fewer_than_two_tracks_show_no_order():
    assert not pair_stopped.reordered(["t1"], ["t1", "t2"])
    assert not pair_stopped.reordered(["t1", "t2"], ["t3", "t4"])


def test_a_track_held_twice_is_read_at_its_first_place():
    assert not pair_stopped.reordered(["t1", "t2", "t1"], ["t1", "t2"])
    assert pair_stopped.reordered(["t2", "t1", "t2"], ["t1", "t2"])


def test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves(cfg):
    from cratekit.modules.outbound import pairs

    store = pairs.PairStore(cfg)
    store.mark("acc", "rb", name="Mine")
    assert store.get("acc").stop_seen is None
    kept = pairs.StopReading("run-a", ("t2", "t1"), "2026-11-07T00:00:00+00:00")
    store.see_stop("acc", kept)
    assert store.get("acc").stop_seen == kept
    later = pairs.StopReading(
        "run-a",
        ("t2", "t1"),
        "2026-11-07T00:00:00+00:00",
        settled=True,
        after=("t1", "t2"),
        after_at="2026-11-07T00:10:00+00:00",
    )
    store.see_stop("acc", later)
    assert store.get("acc").stop_seen == later
    # Links alone do not move the snapshot, so the reading stays.
    store.record("acc", links={"t1": "1"})
    assert store.get("acc").stop_seen == later
    store.record("acc", account=("t1", "t2"), rekordbox=())
    assert store.get("acc").stop_seen is None
    assert store.see_stop("other", kept) is None


@pytest.mark.parametrize(
    "kept",
    [
        {"order": "t1", "at": "2026-11-07T00:00:00+00:00", "run": "r", "settled": False},
        {"order": ["t1", ""], "at": "2026-11-07T00:00:00+00:00", "run": "r", "settled": False},
        {"order": ["t1"], "run": "r", "settled": False},
        {"order": ["t1"], "at": "2026-11-07T00:00:00+00:00", "settled": False},
        {"order": ["t1"], "at": "2026-11-07T00:00:00+00:00", "run": "", "settled": False},
        {"order": ["t1"], "at": "2026-11-07T00:00:00+00:00", "run": "r"},
        {"order": ["t1"], "at": "2026-11-07T00:00:00+00:00", "run": "r", "settled": "yes"},
        {
            "order": ["t1"],
            "at": "2026-11-07T00:00:00+00:00",
            "run": "r",
            "settled": True,
            "after": {"order": ["t1"]},
        },
        {
            "order": ["t1"],
            "at": "2026-11-07T00:00:00+00:00",
            "run": "r",
            "settled": True,
            "after": {"order": [""], "at": "2026-11-07T00:00:00+00:00"},
        },
        ["t1"],
    ],
)
def test_a_reading_after_a_stop_that_is_not_an_order_refuses_the_store(cfg, kept):
    from cratekit.core.cause import CratekitError
    from cratekit.modules.outbound import pairs

    store = pairs.PairStore(cfg)
    store.mark("acc", "rb", name="Mine")
    raw = json.loads(store.path.read_text())
    raw["pairs"]["acc"]["stop_seen"] = kept
    store.path.write_text(json.dumps(raw))
    with pytest.raises(CratekitError):
        store.get("acc")


def _write(**moments) -> pair_stopped.StoppedWrite:
    return pair_stopped.StoppedWrite(
        run_id="run-a",
        account_id="acc",
        at=datetime(2026, 11, 7, 10, tzinfo=UTC),
        start=("t1", "t2"),
        target=("t2", "t1"),
        leader="rekordbox",
        rekordbox=(),
        written=True,
        links={},
        **moments,
    )


def test_a_kept_reading_counts_only_for_its_run_at_or_after_its_moves():
    from types import SimpleNamespace

    from cratekit.modules.outbound import pairs

    def held(at: str, run: str = "run-a"):
        return SimpleNamespace(stop_seen=pairs.StopReading(run, ("t1", "t2"), at))

    write = _write()
    found = pair_cli._kept_after(held("2026-11-07T10:00:00+00:00"), write)
    assert found is not None and found.order == ("t1", "t2")
    assert pair_cli._kept_after(held("2026-11-07T09:59:59+00:00"), write) is None
    assert pair_cli._kept_after(held("2026-11-07T11:00:00+00:00", "run-b"), write) is None
    assert pair_cli._kept_after(held("not a moment"), write) is None
    assert pair_cli._kept_after(None, write) is None
    assert pair_cli._kept_after(SimpleNamespace(stop_seen=None), write) is None
    # A write that sent its moves blind is read after they began, not its order step.
    blind = _write(moving_at=datetime(2026, 11, 7, 12, tzinfo=UTC))
    assert pair_cli._kept_after(held("2026-11-07T11:00:00+00:00"), blind) is None
    assert pair_cli._kept_after(held("2026-11-07T12:00:00+00:00"), blind) is not None
