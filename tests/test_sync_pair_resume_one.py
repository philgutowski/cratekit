"""U210: a stop inside one paired playlist's account writes, finished by a continue of the run.

The single pair world ``tests/test_sync_pair.py`` builds, synced once and then
changed so both sides owe a write, with every account write sent through a
real provider gate (``tests/test_sync_pair_resume.py``), so ``--calls`` stops
the write between its removal and its addition, after rekordbox's commit.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

from cratekit.core import held_plan
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


