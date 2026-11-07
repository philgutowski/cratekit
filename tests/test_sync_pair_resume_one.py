"""U210: a stop inside one paired playlist's account writes, finished by a continue of the run.

The single pair world ``tests/test_sync_pair.py`` builds, synced once and then
changed so both sides owe a write, with every account write sent through a
real provider gate (``tests/test_sync_pair_resume.py``), so ``--calls`` stops
the write between its removal and its addition, after rekordbox's commit.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from datetime import timedelta

import pytest

from cratekit.core import held_plan, jobs
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair import ACCOUNT, sync
from tests.test_sync_pair import db as db  # noqa: PLC0414
from tests.test_sync_pair import world as world  # noqa: PLC0414
from tests.test_sync_pair_resume import CEILING, VERB, gate_the_account, to_the_write, write

# ═══════════════════════════════════════════════════════════════════════════
# One paired playlist: a stop inside the account's writes
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def paired(world, monkeypatch):
    """A pair synced once, then changed so both sides owe a write.

    The account gains t4, so rekordbox adds row 4; rekordbox loses row 2 and
    gains row 5, so the account takes t2 off and adds t5. The account's
    writes are a removal, an addition and possibly an order, each one gated
    call, and a ceiling of one stops it after the removal.
    """
    made = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(made.args())[0] == int(ExitCode.OK)
    gate_the_account(made.account, monkeypatch)
    made.account.playlists[ACCOUNT].append("t4")
    made.rekordbox_remove("2")
    made.rekordbox_add("5")
    return made


def test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice(
    paired, cfg
):
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    code, stopped = write(run_id, args, 1)
    assert code == CEILING, stopped
    assert world.on_account() == ["t1", "t3", "t4"], "the removal did not land first"
    assert sorted(world.held()) == ["1", "3", "4", "5"], "rekordbox was not written first"

    code, done = write(run_id, args, 100)
    assert code == int(ExitCode.OK), done
    assert sorted(world.on_account()) == ["t1", "t3", "t4", "t5"]
    assert sorted(world.held()) == ["1", "3", "4", "5"]
    assert len(world.held()) == 4, "rekordbox was written twice"
    held = pairs.PairStore(cfg).get(ACCOUNT)
    assert held is not None
    assert sorted(held.account) == ["t1", "t3", "t4", "t5"], "the snapshot did not move"
    assert done["data"]["totals"]["rekordbox_added"] == 0, "the rekordbox commit ran again"


def test_a_track_lost_from_the_part_written_account_playlist_refuses_stale(paired):
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    assert write(run_id, args, 1)[0] == CEILING
    world.account.playlists[ACCOUNT].remove("t1")

    code, refused = write(run_id, args, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["why"] for one in refused["cause"]["detail"]["moved"]] == [
        "lost 1 track(s) this run was not taking off since the plan"
    ]
    assert world.on_account() == ["t3", "t4"]


def test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale(paired):
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    assert write(run_id, args, 1)[0] == CEILING
    world.rekordbox_add("6")

    code, refused = write(run_id, args, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    moved = refused["cause"]["detail"]["moved"]
    assert [(one["side"], one["why"]) for one in moved] == [
        ("rekordbox", "has gained 1 track(s) since this run wrote it")
    ]


def test_steps_that_cannot_be_read_are_said_and_the_continue_refuses_rather_than_writes_twice(
    paired,
):
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    assert write(run_id, args, 1)[0] == CEILING
    held_plan.steps_path(run_id).write_text("{ not json")

    code, refused = write(run_id, args, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    sides = {one["side"] for one in refused["cause"]["detail"]["moved"]}
    assert sides == {"account", "rekordbox"}
    assert sorted(world.held()) == ["1", "3", "4", "5"]


def test_a_step_that_cannot_be_recorded_stops_the_write(paired, monkeypatch):
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)

    def refused(self, key, step, value=True):
        raise OSError("read-only file system")

    monkeypatch.setattr(held_plan.Steps, "mark", refused)
    code, stopped = write(run_id, args, 100)
    assert stopped["cause"]["reason"] == pair_cli.STEPS_UNWRITTEN, stopped
    assert code != int(ExitCode.OK)
    assert world.on_account() == ["t1", "t2", "t3", "t4"], "the account was written"




def test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale(paired):
    """Round one's blocking finding: the order the plan read is held until the write orders."""
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    assert write(run_id, args, 1)[0] == CEILING
    world.account.playlists[ACCOUNT] = ["t4", "t3", "t1"]

    code, refused = write(run_id, args, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["why"] for one in refused["cause"]["detail"]["moved"]] == [
        "was reordered since the plan"
    ]
    assert world.on_account() == ["t4", "t3", "t1"], "the author's order was written over"


def test_a_track_withheld_on_the_part_written_playlist_refuses_stale(paired):
    world = paired
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    assert write(run_id, args, 1)[0] == CEILING
    world.account.playlists[ACCOUNT].append("t8")
    world.withheld.add("t8")

    code, refused = write(run_id, args, 100)
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["why"] for one in refused["cause"]["detail"]["moved"]] == [
        "withholds a different number of tracks than the plan read"
    ]


def test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue(world, monkeypatch):
    made = world(account=("1",), rekordbox=("1", "2"))
    assert sync(made.args())[0] == int(ExitCode.OK)
    gate_the_account(made.account, monkeypatch)
    made.account.playlists[ACCOUNT].append("t-missing")
    made.codes["t-missing"] = "GBZZZ2600099"
    made.rekordbox_add("5")
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    # The account's addition fails after rekordbox's commit and the queue.
    made.account.fail_on = frozenset({ACCOUNT})
    made.account.provider_error = True
    code, failed = write(run_id, args, 100)
    assert code != int(ExitCode.OK), failed
    with jobs.open_store() as store:
        queued = pair_cli.pair_jobs(made.cfg, store)
    assert len(queued) == 1

    made.account.fail_on = frozenset()
    code, done = write(run_id, args, 100)
    assert code == int(ExitCode.OK), done
    with jobs.open_store() as store:
        assert len(pair_cli.pair_jobs(made.cfg, store)) == 1, "the continue queued a second job"
    assert done["data"]["totals"]["queued_jobs"] == []
    assert sorted(made.on_account()) == ["t-missing", "t1", "t2", "t5"]


def test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan(
    world, cfg, monkeypatch
):
    """The pair was unmarked when the plan was made and is marked now, by this run alone."""
    made = world(account=("1", "2"), rekordbox=("2", "3"))
    gate_the_account(made.account, monkeypatch)
    args = made.args()
    run_id, _first = to_the_write(args)
    lookups = len(made.account.matches)
    made.account.fail_on = frozenset({ACCOUNT})
    made.account.provider_error = True
    code, failed = write(run_id, args, 100)
    assert code != int(ExitCode.OK), failed
    assert pairs.PairStore(cfg).get(ACCOUNT) is not None, "the pair was not marked"

    made.account.fail_on = frozenset()
    code, done = write(run_id, args, 100)
    assert code == int(ExitCode.OK), done
    assert pair_cli.REPLANNED not in {w["code"] for w in done["warnings"]}
    assert len(made.account.matches) == lookups, "the continue planned again"
    assert sorted(made.on_account()) == ["t1", "t2", "t3"]
    assert sorted(made.held()) == ["1", "2", "3"]


def _one_move_a_call(account) -> None:
    """Order as the live adapter does: one gated move to the front per track moved (U220)."""

    def order(playlist_id, remote_ids, *, expect=None, begun=None):
        account.expected.append((playlist_id, expect))
        members = account.playlists[playlist_id]
        once = {one for one in members if members.count(one) == 1}
        wanted = [one for one in dict.fromkeys(remote_ids) if one in once]
        keep = 0
        for one in reversed(members):
            if one in set(wanted) and keep < len(wanted) and one == wanted[-1 - keep]:
                keep += 1
        moving = list(reversed(wanted[: len(wanted) - keep]))
        if moving and begun is not None:
            # U231. TOLD BEFORE THE FIRST MOVE, as the adapter tells it.
            end = list(members)
            for one in moving:
                end.remove(one)
                end.insert(0, one)
            begun(tuple(members), tuple(end))
        for one in moving:
            account._bump(playlist_id)
            members.remove(one)
            members.insert(0, one)
        account.ordered.append((playlist_id, tuple(remote_ids)))
        return tuple(members)

    account.order_tracks = order


def test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it(
    world, monkeypatch
):
    """Round two of U210, and U231: a continue sends none of the moves a stop left in doubt.

    How many moves reached the provider before the stop is not known, and a
    move sent again from a reading that lags lands on whatever stands at its
    position, so the continue only reads the order: pending. Two later
    readings that agree on an order on the moves' path then finish it from
    rekordbox, as U225 finishes a stopped write: the continue's own reading
    and the next sync's.
    """
    made = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(made.args())[0] == int(ExitCode.OK)
    gate_the_account(made.account, monkeypatch)
    _one_move_a_call(made.account)
    made.rekordbox_order("3", "2", "1")
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    code, stopped = write(run_id, args, 1)
    assert code == CEILING, stopped
    assert made.on_account() == ["t2", "t1", "t3"], "the stop did not fall between the moves"

    moves = len(made.account.ordered)
    code, done = write(run_id, args, 100)
    assert code == int(ExitCode.OK), done
    assert len(made.account.ordered) == moves, "the continue sent the order again"
    assert made.on_account() == ["t2", "t1", "t3"]
    assert pair_cli.PENDING in {w["code"] for w in done["warnings"]}
    # The continue's reading is kept on the pair; a later one that agrees
    # with it, read at least AGREE_AFTER on, finishes the order.
    monkeypatch.setattr(pair_cli, "AGREE_AFTER", timedelta(0))
    code, finished = sync(args)
    assert code == int(ExitCode.OK), finished
    assert made.on_account() == ["t3", "t2", "t1"]
    code, again = sync(args)
    assert code == int(ExitCode.OK), again
    assert again["outcome"] == "no_op"


def test_a_park_that_is_not_the_ceiling_names_the_command_that_continues_the_run(
    world, monkeypatch
):
    made = world(account=("1", "2", "3"), rekordbox=("1", "2", "3"))
    assert sync(made.args())[0] == int(ExitCode.OK)
    gate_the_account(made.account, monkeypatch, limited_on=2)
    made.account.playlists[ACCOUNT].append("t4")
    made.rekordbox_remove("2")
    made.rekordbox_add("5")
    args = [*VERB, ACCOUNT]
    run_id, _first = to_the_write(args)
    code, parked = write(run_id, args, 100)
    assert parked["cause"]["reason"] == "provider-cooldown", parked
    message = parked["cause"]["message"]
    assert f"run {run_id} finished 0 of 1 pair(s)" in message
    assert message.endswith(f"once that has passed: crate --run {run_id} sync pair {ACCOUNT}")
