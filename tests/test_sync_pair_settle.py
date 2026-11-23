"""U231: an account playlist put in rekordbox's order finishes despite the provider's read lag.

The moves are sent with no read back between them, since the provider's reads
lag them for minutes. One judged reading after a settle window decides the
order, and an order the provider does not yet serve is left pending until two
readings agree. The fake account's served order is made to lag. D1 applies,
nothing here names a real account, person or track.
"""

from __future__ import annotations

import os
import time
from dataclasses import replace
from datetime import timedelta

import pytest

from cratekit.core import config, held_plan
from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs, tidal_account
from cratekit.sync import pair_cli
from tests._sync_builders import exited
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import VERB, _codes, _items, _said, plan_only, sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414
from tests.test_sync_pair_order import _reordered


def _ids(*content_ids: str) -> list[str]:
    return [f"t{one}" for one in content_ids]


@pytest.fixture
def owed(world):
    """One pair synced in GIG READY, then reordered in rekordbox, so its account side owes an order."""
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    exited(sync())
    _reordered(world, opener, "4", "3", "1", "2")
    return opener, world.titled("GIG READY Opener")


def _agreeing_at_once(monkeypatch) -> None:
    """Two readings agree however close together, as if minutes had passed between runs."""
    from cratekit.sync import pair_plan
    monkeypatch.setattr(pair_plan, "AGREE_AFTER", timedelta(0))


# The write sends its moves blind and reads the order once, after a window


def test_an_order_the_provider_serves_at_once_finishes_in_the_one_run(world, owed, cfg):
    opener, account_id = owed
    envelope = exited(sync())
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert pair_cli.PENDING not in _codes(envelope)
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("4", "3", "1", "2"))
    assert held.seen is None
    # The one settle reading waited the window, since nothing else was written.
    assert world.account.settle_waits and world.account.settle_waits[0] > 0
    assert held_plan.carried() == ([], [])


def test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok(
    world, owed, cfg
):
    opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    envelope = exited(sync())
    assert pair_cli.PENDING in _codes(envelope)
    assert "GIG READY Opener" in _said(envelope, pair_cli.PENDING)
    # Every move landed; the provider does not serve them yet.
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("1", "2", "3", "4")), (
        "the snapshot moved over an order nobody read"
    )
    assert held.seen == tuple(_ids("1", "2", "3", "4"))
    assert world.held(opener) == ["4", "3", "1", "2"]


def test_a_late_order_finishes_in_the_next_run_with_no_rekordbox_write_between(
    world, owed, cfg
):
    opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    exited(sync())
    ordered = len(world.account.ordered)
    # The provider catches up before the next sync.
    del world.account.served[account_id]
    plan = plan_only()
    assert [item for item in plan["items"] if item["pair"] == account_id] == [], (
        "a pair whose order landed planned a write"
    )
    exited(sync())
    assert len(world.account.ordered) == ordered, "the order was written a second time"
    assert world.held(opener) == ["4", "3", "1", "2"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("4", "3", "1", "2"))
    assert held.seen is None
    assert held_plan.carried() == ([], [])


def test_a_pending_pair_is_held_whole_until_a_later_reading_agrees(world, owed, cfg):
    opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    exited(sync())
    # The provider now serves a third order, between the two.
    world.account.served[account_id] = _ids("3", "1", "2", "4")
    world.rekordbox_add(opener, "5")
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert "GIG READY Opener" in _said(envelope, pair_cli.LEFT_OUT)
    # Nothing written on either side: the addition in rekordbox waits too.
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2", "5"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.seen == tuple(_ids("3", "1", "2", "4"))


def test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement(world, owed, cfg):
    _opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    exited(sync())
    ordered = len(world.account.ordered)
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered


def test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag(
    world, owed, cfg, monkeypatch
):
    """The provider serving the order from before the moves, however long, moves nothing again."""
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    exited(sync())
    ordered = len(world.account.ordered)
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered, "a lagging reading was ordered from"
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2"]
    assert "every move run" in _said(envelope, pair_cli.LEFT_OUT)


def _age(days: int) -> None:
    """Every run's steps and every carried record dated ``days`` back."""
    old = time.time() - days * 86400
    directory = config.state_path(held_plan.STATE_KEY)
    for one in [*directory.glob("*.json"), *held_plan.carried_dir().glob("*.json")]:
        os.utime(one, (old, old))


def test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept(
    world, owed, cfg, monkeypatch
):
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    readings = [_ids("1", "2", "3", "4"), _ids("2", "1", "3", "4")]
    world.account.served[account_id] = readings[0]
    exited(sync())
    ordered = len(world.account.ordered)
    for turn in range(4):
        world.account.served[account_id] = readings[(turn + 1) % 2]
        if turn == 2:
            _age(31)
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope), turn
    assert len(world.account.ordered) == ordered
    assert world.held(opener) == ["4", "3", "1", "2"], "rekordbox took a scramble"


def test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change(
    world, owed, cfg, monkeypatch
):
    """U234: the reorder is shown by two agreed readings after the stop in different orders."""
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    exited(sync())
    # The person puts the playlist in an order no move of the write passes.
    del world.account.served[account_id]
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope), "one reading was taken as agreed"
    # Two syncs read it agreed and write nothing, keeping that reading, settled.
    plan_only()
    plan_only()
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.stop_seen is not None
    assert held.stop_seen.order == tuple(_ids("2", "4", "1", "3")) and held.stop_seen.settled
    # Moved again: held until it agrees (U231), then as the order after the settled one (U234).
    world.account.playlists[account_id][:] = _ids("3", "2", "4", "1")
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope), "one reading was taken as agreed"
        assert world.held(opener) == ["4", "3", "1", "2"]
    exited(sync())
    assert world.held(opener) == ["3", "2", "4", "1"]
    assert world.account.playlists[account_id] == _ids("3", "2", "4", "1")
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("3", "2", "4", "1"))
    assert held.seen is None and held.stop_seen is None


def test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order(
    world, owed, cfg, monkeypatch
):
    """U234: one agreed reading off the path is not the person's reorder on that alone."""
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    exited(sync())
    del world.account.served[account_id]
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope)
    exited(sync())
    assert world.held(opener) == ["4", "3", "1", "2"], "rekordbox took the agreed reading"
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")


# A stop part way through the moves


def _stopping_after(
    world, monkeypatch, playlist_id: str, moves: int, *, known: bool = True
) -> list[int]:
    """Make the order on one playlist send ``moves`` moves and then refuse, as a failed move does.

    Counts are told before each move as the adapter tells them (R-1394);
    ``known`` tells the failed move as not landed, otherwise its fate is unknown.
    """
    from cratekit.modules.outbound import tidal_account

    real = world.account.order_tracks
    stops: list[int] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id != playlist_id or stops:
            return real(asked_id, remote_ids, expect=expect, begun=begun, **agreed)
        members = world.account.playlists[asked_id]
        before = list(members)
        planned = tidal_account._to_the_front(before, remote_ids)
        end = list(before)
        for one in planned:
            end.remove(one)
            end.insert(0, one)
        told = begun(tuple(before), tuple(end)) if begun is not None else None
        for index, one in enumerate(planned[:moves], start=1):
            if told is not None:
                told(index, index - 1)
            members.remove(one)
            members.insert(0, one)
        if told is not None and moves < len(planned):
            told(moves + 1, moves)
            if known:
                told(moves, moves)
        stops.append(moves)
        world.account.ordered.append((asked_id, tuple(remote_ids)))
        raise refuse(
            "unavailable-transient",
            f"the provider failed a move on the playlist {asked_id}",
            scope=Scope.RUN,
            origin=("test", "order"),
        )

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    return stops


def test_a_stop_part_way_then_a_continue_sends_no_move_again(world, owed, cfg, monkeypatch):
    opener, account_id = owed
    stops = _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert stops == [1]
    ordered = len(world.account.ordered)
    done = exited(drive(["--run", stopped["run_id"], *VERB]))
    assert len(world.account.ordered) == ordered, "a continue sent the moves again"
    # The provider serves the one move that landed: the pair waits, pending.
    assert pair_cli.PENDING in _codes(done)
    assert world.held(opener) == ["4", "3", "1", "2"]


def test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue(
    world, owed, cfg, monkeypatch
):
    opener, account_id = owed
    _stopping_after(world, monkeypatch, account_id, 2)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    # The failed move had in fact landed: every move is in.
    world.account.playlists[account_id][:] = _ids("4", "3", "1", "2")
    ordered = len(world.account.ordered)
    done = exited(drive(["--run", stopped["run_id"], *VERB]))
    assert len(world.account.ordered) == ordered
    assert pair_cli.PENDING not in _codes(done)
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("4", "3", "1", "2"))


def test_a_stop_part_way_agreed_on_the_moves_path_is_finished_from_rekordbox(
    world, owed, cfg, monkeypatch
):
    """U225's finish, once two readings agree, for a write whose moves were not all accepted."""
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert world.account.playlists[account_id] == reached
    exited(sync())
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2"], "rekordbox took the stopped order"


# R-1394: a stopped write is finished only from a reading its moves could have left


def _three_moves(world, opener) -> None:
    """Rekordbox in an order three moves to the front put the account in: 4, 3, 2, 1 from 1, 2, 3, 4."""
    _reordered(world, opener, "4", "3", "2", "1")


def test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees(
    world, owed, cfg, monkeypatch
):
    """Two readings agreeing on the order before the moves are a lag."""
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    assert reached == _ids("2", "1", "3", "4")
    # The provider serves the order from before any move, for longer than AGREE_AFTER.
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    ordered = len(world.account.ordered)
    for _ in range(3):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered, "moves were sent from a lagging reading"
    assert world.account.playlists[account_id] == reached
    assert world.held(opener) == ["4", "3", "2", "1"]
    assert "accepted 1 of the 3 moves" in _said(envelope, pair_cli.LEFT_OUT)


def test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished(
    world, owed, cfg, monkeypatch
):
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert pair_cli.LEFT_OUT in _codes(envelope)
    # Now served as it stands, one move in: two readings agree, and it finishes.
    del world.account.served[account_id]
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1")
    assert world.held(opener) == ["4", "3", "2", "1"]
    # The finish moves nothing until the adapter's reading is the one the plan agreed on.
    assert world.account.expected[-1] == (account_id, tuple(_ids("2", "1", "3", "4")))


def test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after(
    world, owed, cfg, monkeypatch
):
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1, known=False)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    ordered = len(world.account.ordered)
    for _ in range(3):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered, "moves were sent with one's landing unknown"
    assert world.account.playlists[account_id] == reached
    assert "whether it landed is not known" in _said(envelope, pair_cli.LEFT_OUT)
    # The move had landed after all, and the provider now serves it.
    world.account.playlists[account_id][:] = _ids("3", "2", "1", "4")
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1")
    assert world.held(opener) == ["4", "3", "2", "1"]


def test_a_stopped_writes_counts_are_carried_past_its_runs_steps(world, owed, cfg, monkeypatch):
    """R-1372's carried record holds the counts too, so a run whose steps are gone still holds a lag."""
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    held_plan.steps_path(stopped["run_id"]).unlink()
    reached = list(world.account.playlists[account_id])
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    ordered = len(world.account.ordered)
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered, "moves were sent from a lagging reading"
    assert world.account.playlists[account_id] == reached


def test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending(
    world, owed, cfg, monkeypatch
):
    """The refused finish's record does not hide the stopped write it finishes,
    or the lagging order would be read as the person's reorder."""
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    stopping = world.account.order_tracks
    refusals: list[tuple[str, ...] | None] = []

    def refusing(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id == account_id and not refusals:
            refusals.append(expect)
            raise refuse(
                "outbound-remove-refused",
                f"the playlist {asked_id} does not hold what was last known of it",
                scope=Scope.ITEM,
                origin=("test", "order"),
            )
        return stopping(asked_id, remote_ids, expect=expect, begun=begun, **agreed)

    monkeypatch.setattr(world.account, "order_tracks", refusing)
    exited(sync())
    code, envelope = sync()
    assert code != int(ExitCode.OK), envelope
    assert refusals == [tuple(reached)], "the finish was not refused, or not held to its reading"
    assert world.account.playlists[account_id] == reached
    # The provider now serves the order from before any move.
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert world.held(opener) == ["4", "3", "2", "1"], "a lag was merged into rekordbox"
    assert world.account.playlists[account_id] == reached
    # Served as it stands, the stopped write is finished.
    del world.account.served[account_id]
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1")
    assert world.held(opener) == ["4", "3", "2", "1"]


def test_a_first_move_refused_on_its_412s_is_sent_again_from_the_start_once(
    world, owed, cfg, monkeypatch
):
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 0)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    ordered = len(world.account.ordered)
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert len(world.account.ordered) == ordered + 1, "the moves were not sent again once"
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1")
    assert world.held(opener) == ["4", "3", "2", "1"]


def test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves(
    world, owed, cfg, monkeypatch
):
    """A moving step from before R-1394 says nothing of how far the moves got."""
    from cratekit.sync import pair_stopped

    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    real = pair_stopped.moving_step

    def uncounted(**kwargs):
        step = real(**kwargs)
        step.pop(pair_stopped.SENT)
        step.pop(pair_stopped.LANDED)
        return step

    monkeypatch.setattr(pair_stopped, "moving_step", uncounted)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    ordered = len(world.account.ordered)
    for _ in range(2):
        code, envelope = sync()
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered
    assert world.account.playlists[account_id] == reached
    assert "recorded no count" in _said(envelope, pair_cli.LEFT_OUT)
    # Shown as the moves leave it, it finishes with nothing moved.
    world.account.playlists[account_id][:] = _ids("4", "3", "2", "1")
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT not in _codes(envelope)
    assert len(world.account.ordered) == ordered
    assert world.held(opener) == ["4", "3", "2", "1"]


# Which pairs keep the account's order


def test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs(world, cfg):
    crates = world.folder("Crates")
    deep = world.playlist("Deep", "1", "2", "3", under=crates)
    exited(sync())
    account_id = world.titled("Crates Deep")
    _reordered(world, deep, "3", "1", "2")
    world.rekordbox_add(deep, "4")
    plan = plan_only()
    assert _items(plan, "account", "order") == []
    assert [item["action"] for item in plan["items"] if item["side"] == "account"] == ["add"]
    exited(sync())
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    assert world.account.ordered == []
    assert world.held(deep) == ["3", "1", "2", "4"]


def test_the_config_key_keeps_the_account_order_of_every_pair(world, cfg, monkeypatch):
    every = replace(cfg, outbound=replace(cfg.outbound, pair_order_every_pair=True))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: every)
    crates = world.folder("Crates")
    deep = world.playlist("Deep", "1", "2", "3", under=crates)
    exited(sync())
    account_id = world.titled("Crates Deep")
    _reordered(world, deep, "3", "1", "2")
    exited(sync())
    assert world.account.playlists[account_id] == _ids("3", "1", "2")


# Records, the agreement gap, the window and the scope


def test_a_write_that_keeps_no_record_sends_no_order(world, owed, cfg, monkeypatch):
    """Moves sent with no read back must be recorded, or a later sync sends them again."""
    _opener, account_id = owed
    real_hold = pair_cli._hold
    monkeypatch.setattr(pair_cli, "_hold", lambda *args, **kwargs: "the state directory is full")
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.ordered == [], "an order went out with nothing to record it by"
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    assert stopped["cause"]["reason"] == pair_cli.STEPS_UNWRITTEN
    assert "GIG READY Opener" in stopped["cause"]["message"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("1", "2", "3", "4"))
    # Once a plan can be held again, the order is sent once and recorded.
    monkeypatch.setattr(pair_cli, "_hold", real_hold)
    envelope = exited(sync())
    assert len(world.account.ordered) == 1
    assert pair_cli.PENDING in _codes(envelope)


def test_two_readings_agree_only_once_minutes_apart(world, owed, cfg, monkeypatch):
    """The agreement rule's gap, AGREE_AFTER, is what a later run waits out."""
    from cratekit.sync import pair_model
    opener, account_id = owed
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    code, envelope = sync()
    assert pair_cli.LEFT_OUT in _codes(envelope)
    kept = pairs.PairStore(cfg).get(account_id)
    assert kept is not None and kept.seen == tuple(reached)
    # Read again at once, it agrees too soon: held, and the older reading kept.
    code, envelope = sync()
    assert pair_cli.LEFT_OUT in _codes(envelope)
    again = pairs.PairStore(cfg).get(account_id)
    assert again is not None and again.seen_at == kept.seen_at, "a too soon reading replaced the older"
    assert world.account.playlists[account_id] == reached
    # Minutes on, the same reading agrees, and the stopped write is finished.
    from datetime import UTC, datetime

    later = pair_cli.AGREE_AFTER + timedelta(seconds=1)
    monkeypatch.setattr(pair_model, "_now", lambda: datetime.now(UTC) + later)
    envelope = exited(sync())
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2"), (
        envelope["warnings"], pairs.PairStore(cfg).get(account_id)
    )
    assert world.held(opener) == ["4", "3", "1", "2"]


def test_a_reading_kept_from_before_the_moves_is_no_agreement(world, owed, cfg, monkeypatch):
    """A reading kept for an earlier write does not vouch for this one's."""
    _opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    # A reading equal to this one, kept before the moves began.
    pairs.PairStore(cfg).see(account_id, reached, at="2026-01-01T00:00:00+00:00")
    code, envelope = sync()
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert world.account.playlists[account_id] == reached


def test_the_settle_window_counts_the_time_spent_on_other_writes(world, owed, cfg, monkeypatch):
    """Only what is left of the window is waited."""
    from datetime import UTC, datetime

    from cratekit.sync import pair_model

    start = datetime(2026, 11, 6, 12, 0, tzinfo=UTC)
    ticks = iter(range(0, 10_000, 20))
    monkeypatch.setattr(pair_model, "_now", lambda: start + timedelta(seconds=next(ticks)))
    exited(sync())
    assert world.account.settle_waits
    assert world.account.settle_waits[0] <= pair_cli.SETTLE_SECONDS - 20


def test_a_settle_reading_refused_for_another_reason_stops_the_write(world, owed, monkeypatch):
    """Only an order's own refusals leave it pending; a rejected session still stops."""
    from cratekit.core.cause import Remedy

    def rejected(playlist_id, *, wait=0.0):
        raise refuse(
            "credential-missing",
            "the streaming provider rejected the session",
            remedy=Remedy.REAUTHENTICATE_PROVIDER,
            scope=Scope.ITEM,
            origin=("test", "settle"),
        )

    monkeypatch.setattr(world.account, "settled_order", rejected)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert stopped["cause"]["reason"] == "credential-missing"


def test_a_root_playlist_named_gig_ready_is_not_under_gig_ready(world, cfg):
    """The scope is the folder, not a playlist of that name."""
    root = world.playlist("GIG READY", "1", "2", "3")
    exited(sync())
    _reordered(world, root, "3", "1", "2")
    plan = plan_only()
    assert _items(plan, "account", "order") == []


def test_a_pending_run_does_not_count_its_pending_pair_as_synced(world, owed):
    """The headline says pending, not synced, for a pair whose snapshot did not move."""
    _opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    envelope = exited(sync())
    said = _said(envelope, pair_cli.WRITTEN)
    assert said.startswith("0 pair(s) synced"), said
    assert "1 pending" in said


def test_the_config_key_is_true_or_false():
    problems = config._validate_pair_order_every_pair({"outbound": {"pair_order_every_pair": "yes"}})
    assert problems and config.PAIR_ORDER_EVERY_PAIR_KEY in problems[0]
    assert config._validate_pair_order_every_pair({"outbound": {"pair_order_every_pair": True}}) == []
    assert config._validate_pair_order_every_pair({}) == []


@pytest.mark.parametrize(
    "seen",
    [{"order": "t1", "at": "2026-11-06T00:00:00+00:00"}, {"order": ["t1", ""], "at": "x"}, {"order": ["t1"]}],
)
def test_a_reading_kept_on_a_pair_that_is_not_an_order_refuses_the_store(cfg, seen):
    import json

    from cratekit.core.cause import CratekitError

    store = pairs.PairStore(cfg)
    store.mark("acc", "rb", name="Mine")
    raw = json.loads(store.path.read_text())
    raw["pairs"]["acc"]["seen"] = seen
    store.path.write_text(json.dumps(raw))
    with pytest.raises(CratekitError):
        store.get("acc")


def test_a_pair_document_from_before_u231_reads_with_no_reading_kept(cfg):
    store = pairs.PairStore(cfg)
    store.mark("acc", "rb", name="Mine")
    held = store.get("acc")
    assert held is not None and held.seen is None and held.seen_at == ""


# A continue's record and window, and a new rekordbox side's scope


@pytest.mark.parametrize("damage", ["unreadable", "gone"])
def test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again(
    world, owed, cfg, monkeypatch, damage
):
    """The carried record says the moves went when the run's steps cannot.

    Parked in its settle reading with every move sent, so the continue's check
    finds the playlist as the plan read it and passes.
    """
    from cratekit.core import jobs

    _opener, account_id = owed
    real = world.account.settled_order
    parks: list[int] = []

    def parking(playlist_id, *, wait=0.0):
        if not parks:
            parks.append(1)
            raise jobs.Parked(
                refuse("provider-cooldown", "a cooldown", scope=Scope.RUN, origin=("test", "settle")).cause
            )
        return real(playlist_id, wait=wait)

    monkeypatch.setattr(world.account, "settled_order", parking)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    run_id = stopped["run_id"]
    where = held_plan.steps_path(run_id)
    if damage == "gone":
        where.unlink()
    else:
        where.write_text("{not json\n")
    ordered = len(world.account.ordered)
    code, done = drive(["--run", run_id, *VERB])
    assert len(world.account.ordered) == ordered, "a continue sent the moves again"
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("1", "2", "3", "4"))


def test_a_continues_settle_window_is_counted_from_when_the_moves_began(
    world, owed, cfg, monkeypatch
):
    """A continue waits only what is left of the window the moves began."""
    from datetime import UTC, datetime

    from cratekit.sync import pair_model

    _opener, account_id = owed
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    monkeypatch.setattr(pair_model, "_now", lambda: datetime.now(UTC) + timedelta(seconds=20))
    exited(drive(["--run", stopped["run_id"], *VERB]))
    assert world.account.settle_waits[-1] <= pair_cli.SETTLE_SECONDS - 15


def test_a_rekordbox_side_to_be_made_is_under_gig_ready_only_inside_the_folder(cfg):
    """The same scope rule for a pair whose rekordbox side is new."""
    from cratekit.sync import pair_discover, pair_plan
    from cratekit.write import playlist_pair

    made = playlist_pair.Playlist(
        playlist_id="", name="x", attribute=0, removed=False, ancestors=()
    )
    inside = pair_discover.Home(folder="", name="Opener", parent_id="7", path=("GIG READY", "Opener"))
    named = pair_discover.Home(folder="", name="GIG READY", parent_id="", path=("GIG READY",))
    assert pair_plan._keeps_order(cfg, made, inside) is True
    assert pair_plan._keeps_order(cfg, made, named) is False


# R-1411: a finish that also adds a track is held to the agreed reading


def _adapter_reading(world, monkeypatch, playlist_id: str, reading: list[str]) -> list[object]:
    """Make the adapter's own reading before the order serve ``reading``, and plan its moves from it.

    Judged against the ``agreed`` reading by the adapter's rule, it is refused
    with nothing moved; passed, each move goes by that reading's position onto
    the playlist as it really stands. Answers the ``agreed`` each order was
    asked with.
    """
    from cratekit.modules.outbound import tidal_account

    real = world.account.order_tracks
    asked: list[object] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, agreed=None):
        if asked_id != playlist_id:
            return real(asked_id, remote_ids, expect=expect, begun=begun, agreed=agreed)
        asked.append(None if agreed is None else tuple(agreed))
        members = world.account.playlists[asked_id]
        assert sorted(reading) == sorted(members), "the reading lags what the write left"
        if agreed is not None and not tidal_account._in_agreed_order(list(reading), agreed):
            raise refuse(
                "outbound-remove-refused",
                f"the playlist {asked_id} read 4 time(s) does not hold what was last "
                f"known of it, so the reading may lag a write and no track was moved",
                scope=Scope.RUN,
                origin=("test", "order"),
                detail={"playlist_id": asked_id, "problem": "read-differs"},
            )
        planned = tidal_account._to_the_front(list(reading), remote_ids)
        if not planned:
            return tuple(members)
        end = list(reading)
        for one in planned:
            end = tidal_account._fronted(end, one)
        told = begun(tuple(reading), tuple(end)) if begun is not None else None
        now = list(reading)
        for number, one in enumerate(planned, start=1):
            if told is not None:
                told(number, number - 1)
            at = now.index(one)
            members.insert(0, members.pop(at))
            now = tidal_account._fronted(now, one)
        world.account.ordered.append((asked_id, tuple(remote_ids)))
        return tuple(now)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    return asked


def _stopped_then_added(world, owed, monkeypatch):
    """A stop after one of three moves, served as that move left it, then track 5 added in rekordbox,
    so the finish also adds it."""
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    assert reached == _ids("2", "1", "3", "4")
    world.rekordbox_add(opener, "5")
    return opener, account_id, reached


def test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move(
    world, owed, cfg, monkeypatch
):
    """R-1411: the adapter's reading lags the stopped move, holding the added track."""
    opener, account_id, reached = _stopped_then_added(world, owed, monkeypatch)
    asked = _adapter_reading(world, monkeypatch, account_id, _ids("1", "2", "3", "4", "5"))
    codes = []
    for _ in range(4):
        code, envelope = sync()
        codes.append(code)
    # Held once, then refused twice with nothing moved, its addition landed.
    assert codes[0] == codes[2] == int(ExitCode.OK)
    assert codes[1] != int(ExitCode.OK) and codes[3] != int(ExitCode.OK)
    assert world.account.playlists[account_id] == [*reached, "t5"], "moves were sent from a lag"
    assert world.held(opener) == ["4", "3", "2", "1", "5"], "a lag was merged into rekordbox"
    # Each finish held to the plan's agreed reading, with the landed addition once it was.
    assert asked == [tuple(reached), (*reached, "t5")], "the finish was not held to its reading"
    # Served as the moves left it, the stopped write finishes.
    _adapter_reading(world, monkeypatch, account_id, [*reached, "t5"])
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1", "5")
    assert world.held(opener) == ["4", "3", "2", "1", "5"]


def test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes(
    world, owed, cfg, monkeypatch
):
    opener, account_id, reached = _stopped_then_added(world, owed, monkeypatch)
    for _ in range(2):
        exited(sync())
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1", "5")
    assert world.held(opener) == ["4", "3", "2", "1", "5"]
    assert world.account.agreed[0] == (account_id, tuple(reached))


def test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused(
    world, owed, cfg, monkeypatch
):
    opener, account_id, reached = _stopped_then_added(world, owed, monkeypatch)
    real_add = world.account.add_tracks

    def added_first(asked_id, remote_ids):
        answer = real_add(asked_id, remote_ids)
        members = world.account.playlists[asked_id]
        for one in reversed(answer):
            members.insert(0, members.pop(members.index(one)))
        return answer

    monkeypatch.setattr(world.account, "add_tracks", added_first)
    asked = _adapter_reading(world, monkeypatch, account_id, ["t5", *reached])
    for _ in range(2):
        exited(sync())
    assert asked[0] == tuple(reached)
    assert world.account.playlists[account_id] == _ids("4", "3", "2", "1", "5")
    assert world.held(opener) == ["4", "3", "2", "1", "5"]


def test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move(
    world, owed, cfg, monkeypatch
):
    """The other half of R-1411: a track taken off in rekordbox, the reading lagging the move."""
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    world.rekordbox_remove(opener, "3")
    asked = _adapter_reading(world, monkeypatch, account_id, _ids("1", "2", "4"))
    for _ in range(2):
        code, envelope = sync()
    assert code != int(ExitCode.OK), envelope
    assert asked == [tuple(reached)], "the finish was not held to the agreed reading"
    assert world.account.playlists[account_id] == _ids("2", "1", "4"), "moves were sent from a lag"
    assert world.held(opener) == ["4", "2", "1"], "a lag was merged into rekordbox"
    _adapter_reading(world, monkeypatch, account_id, _ids("2", "1", "4"))
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "2", "1")
    assert world.held(opener) == ["4", "2", "1"]


# R-1411: the agreed reading is the plan's, on every path


def _refused_finish(world, monkeypatch, account_id: str, lag: list[str]) -> tuple[list[object], str]:
    """The adapter's reading lagging the stopped move: held once, then the finish refused.
    Answers the agreed readings asked and the refused run."""
    asked = _adapter_reading(world, monkeypatch, account_id, lag)
    exited(sync())
    code, refused = sync()
    assert code != int(ExitCode.OK), refused
    return asked, refused["run_id"]


@pytest.mark.parametrize("adding", [True, False])
def test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks(
    world, owed, cfg, monkeypatch, adding
):
    """On a continue the check's listing is read for what it holds, not its order,
    since it may be the lag the adapter is served too."""
    opener, account_id = owed
    _three_moves(world, opener)
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    added = ["t5"] if adding else []
    if adding:
        world.rekordbox_add(opener, "5")
    lag = [*_ids("1", "2", "3", "4"), *added]
    asked, run_id = _refused_finish(world, monkeypatch, account_id, lag)
    assert world.account.playlists[account_id] == [*reached, *added]
    world.account.served[account_id] = list(lag)
    before = len(asked)
    code, envelope = drive(["--run", run_id, *VERB])
    assert world.account.playlists[account_id] == [*reached, *added], "moves were sent from a lag"
    # The continue reached the adapter and was refused there.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["detail"]["problem"] == "read-differs", envelope
    assert len(asked) == before + 1, "the continue stopped before its order"
    assert asked[-1] == tuple(reached), "the continue was not held to the plan's reading"
    assert world.held(opener) == ["4", "3", "2", "1", *(["5"] if adding else [])]
    # Served as the moves left it, a later sync finishes the stopped write.
    del world.account.served[account_id]
    _adapter_reading(world, monkeypatch, account_id, [*reached, *added])
    for _ in range(3):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == [*_ids("4", "3", "2", "1"), *added]


def test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading(
    world, owed, cfg, monkeypatch
):
    """A held plan that cannot be read leaves no check listing to pass."""
    opener, account_id, reached = _stopped_then_added(world, owed, monkeypatch)
    asked = _adapter_reading(world, monkeypatch, account_id, _ids("1", "2", "3", "4", "5"))
    exited(sync())
    answers = {pair_cli.REKORDBOX_GATE: "apply", pair_cli.ACCOUNT_GATE: "apply"}
    run_id = None
    for _ in range(3):
        resume = ["--run", run_id] if run_id else []
        code, envelope = drive([*resume, *VERB])
        if code != int(ExitCode.DECISION_REQUIRED):
            break
        run_id = envelope["run_id"]
        gate = envelope["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, answers[gate], "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
        if gate == pair_cli.ACCOUNT_GATE:
            held_plan.path(run_id).write_text("{not json")
    # Refused, read-differs: held to the replanned reading, which lacks the addition.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["detail"]["problem"] == "read-differs", envelope
    assert world.account.playlists[account_id] == [*reached, "t5"], "moves were sent from a lag"
    assert asked == [tuple(reached)], "the finish planned again passed no agreed reading"
    assert world.held(opener) == ["4", "3", "2", "1", "5"]


# U234. A pending order agreed off its moves' path is the provider's state


@pytest.fixture
def longer(world):
    """One GIG READY pair synced on seven tracks, then reversed in rekordbox, so its account owes six moves."""
    gig = world.folder("GIG READY")
    closer = world.playlist("Closer", "1", "2", "3", "4", "5", "6", "7", under=gig)
    exited(sync())
    _reordered(world, closer, "7", "6", "5", "4", "3", "2", "1")
    return closer, world.titled("GIG READY Closer")


def _stopping_off_the_path(world, monkeypatch, playlist_id: str) -> list[int]:
    """Three moves told as accepted, the fourth ending on its 412s, the account off the path.

    Counts are told as the adapter tells them (R-1394). A move that landed
    under its 412 was sent again, so no count of the moves leaves the order.
    """
    real = world.account.order_tracks
    stops: list[int] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id != playlist_id or stops:
            return real(asked_id, remote_ids, expect=expect, begun=begun, **agreed)
        members = world.account.playlists[asked_id]
        before = list(members)
        end = list(before)
        for one in tidal_account._to_the_front(before, remote_ids):
            end.remove(one)
            end.insert(0, one)
        told = begun(tuple(before), tuple(end))
        for sent, landed in ((1, 0), (2, 1), (1, 1), (2, 1), (3, 2), (4, 3), (3, 3)):
            told(sent, landed)
        members[:] = _ids("4", "1", "3", "2", "5", "6", "7")
        stops.append(3)
        world.account.ordered.append((asked_id, tuple(remote_ids)))
        raise refuse(
            "unavailable-transient",
            f"the provider failed a move on the playlist {asked_id}",
            scope=Scope.RUN,
            origin=("test", "order"),
        )

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    return stops


def test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox(
    world, longer, cfg, monkeypatch
):
    """Through U231's hold, no rekordbox order from the agreed half done order."""
    closer, account_id = longer
    _agreeing_at_once(monkeypatch)
    stops = _stopping_off_the_path(world, monkeypatch, account_id)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert stops == [3]
    left = list(world.account.playlists[account_id])
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope)
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the plan writes rekordbox the provider's half done order"
    )
    assert [item["action"] for item in pair if item["side"] == "account"] == ["order"]
    envelope = exited(sync())
    assert world.held(closer) == ["7", "6", "5", "4", "3", "2", "1"]
    assert world.account.playlists[account_id] == _ids("7", "6", "5", "4", "3", "2", "1")
    assert (account_id, tuple(left)) in world.account.agreed, "the rest moved from another reading"
    assert "none of its moves leaves" in _said(envelope, pair_cli.FINISHING)

# R-1418: the reading a finish is held to carries the unread tracks in place


def _listed_unread(monkeypatch, *remote_ids: str) -> None:
    """Make the account list each of ``remote_ids`` with no title, so a plan keeps it unread by its id (R-1264)."""
    from tests.test_sync_pair_discover import LivePlaylist

    real = LivePlaylist.tracks

    def tracks(self, limit=None, offset=0):
        listed = real(self, limit, offset)
        for one in listed:
            if one.id in remote_ids:
                one.name = ""
        return listed

    monkeypatch.setattr(LivePlaylist, "tracks", tracks)


def test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place(
    world, owed, cfg, monkeypatch
):
    """R-1418: the one move that landed put a track the provider cannot read in front.

    A lagging reading differs only by where t9 stands, so a finish held to the
    readable tracks alone would take the lag and move by position from it.
    """
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    assert reached == ["t9", *_ids("1", "2", "3", "4")]
    world.rekordbox_add(opener, "5")
    asked = _adapter_reading(world, monkeypatch, account_id, [*_ids("1", "2", "3", "4"), "t9", "t5"])
    envelope = exited(sync())
    assert pair_cli.LEFT_OUT in _codes(envelope)
    code, envelope = sync()
    # Refused with nothing moved, its addition landed, rekordbox untouched.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["detail"]["problem"] == "read-differs", envelope
    assert world.account.playlists[account_id] == [*reached, "t5"], "moves were sent from a lag"
    assert world.held(opener) == ["2", "3", "4", "1", "5"], "a lag was merged into rekordbox"
    # Held to the plan's reading with the unread id in its place.
    assert asked == [tuple(reached)], "the finish was not held to the unread track's place"
    # Served as the move left it, the stopped write finishes.
    _adapter_reading(world, monkeypatch, account_id, [*reached, "t5"])
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    # t9 where the stopped write was taking it, behind t4, not in front (R-1432).
    assert world.account.playlists[account_id] == [*_ids("2", "3", "4"), "t9", *_ids("1", "5")]
    assert world.held(opener) == ["2", "3", "4", "1", "5"]


def _finished_after_one_move(
    world, monkeypatch, account_id: str, envelopes: list[dict] | None = None
) -> list[str]:
    """Stop the account order after its first move, then sync until the stopped write finishes.

    Answers the playlist as the stopped move left it, keeping each later
    sync's answer in ``envelopes`` when given.
    """
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    reached = list(world.account.playlists[account_id])
    for _ in range(2):
        code, envelope = _synced_keeping_gates(envelopes)
        assert code == int(ExitCode.OK), envelope
        if envelopes is not None:
            envelopes.append(envelope)
    return reached


def _synced_keeping_gates(envelopes: list[dict] | None):
    """``sync()``, each gate answered apply, keeping every envelope it was asked at in ``envelopes``."""
    run_id = None
    for _ in range(3):
        code, envelope = drive([*(["--run", run_id] if run_id else []), *VERB])
        if code != int(ExitCode.DECISION_REQUIRED):
            return code, envelope
        if envelopes is not None:
            envelopes.append(envelope)
        run_id = envelope["run_id"]
        gate = envelope["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
    return code, envelope


def test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it(
    world, owed, cfg, monkeypatch
):
    """R-1432: the stopped write's first move put t9, which the provider cannot read, in front.

    The finish places t9 by the write's own target, behind t4, not at the front.
    """
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    envelopes: list[dict] = []
    reached = _finished_after_one_move(world, monkeypatch, account_id, envelopes)
    assert reached == ["t9", *_ids("1", "2", "3", "4")]
    assert world.account.playlists[account_id] == [*_ids("2", "3", "4"), "t9", "t1"]
    # The gate says so, rather than that the unread track stays where it is.
    finishing = [one for one in envelopes if pair_cli.FINISHING in _codes(one)]
    assert finishing, envelopes
    said = _said(finishing[-1], pair_cli.UNREAD)
    assert (
        "a pair finishing a stopped order puts each where that order was taking it, "
        "or else behind the track it follows" in said
    )
    shown = [
        str(fact)
        for one in envelopes
        if one.get("cause")
        for fact in one["cause"]["detail"]["shown"].values()
    ]
    assert any(
        "the account's order puts each where the stopped order was taking it" in one
        for one in shown
    ), shown
    assert world.held(opener) == ["2", "3", "4", "1"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == (*_ids("2", "3", "4"), "t9", "t1")


def test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place(
    world, owed, cfg, monkeypatch
):
    """R-1432: an unread track at the tail the stopped write kept stays at the tail."""
    opener, account_id = owed
    _reordered(world, opener, "1", "3", "2", "4")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    reached = _finished_after_one_move(world, monkeypatch, account_id)
    assert reached == [*_ids("3", "1", "2", "4"), "t9"]
    assert world.account.playlists[account_id] == [*_ids("1", "3", "2", "4"), "t9"]
    assert world.held(opener) == ["1", "3", "2", "4"]


def test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back(
    world, owed, cfg, monkeypatch
):
    """R-1432: the finish places only what the account lists, so a t9 taken off stays off."""
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == ["t9", *_ids("1", "2", "3", "4")]
    asked_before = len(world.account.ordered)
    world.account.playlists[account_id].remove("t9")
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("2", "3", "4", "1")
    asked = world.account.ordered[asked_before:]
    assert asked and all("t9" not in order for _playlist, order in asked), asked
    assert world.held(opener) == ["2", "3", "4", "1"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("2", "3", "4", "1"))


def _stopped_after_t9s_move(world, owed, monkeypatch, *, rekordbox: str = "apply"):
    """R-1418's stop: t9 untitled behind t4, rekordbox's 2, 3, 4, 1, a stop after t9's move to the front."""
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync(rekordbox=rekordbox)
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == ["t9", *_ids("1", "2", "3", "4")]
    return opener, account_id


def test_a_hand_move_of_the_unread_track_read_first_after_the_stop_is_finished_by_the_target(
    world, owed, cfg, monkeypatch
):
    """R-1432 with U234: an order off the stopped write's path is its partial state until readings settle,
    so the finish puts t9 where it was taking it."""
    opener, account_id = _stopped_after_t9s_move(world, owed, monkeypatch)
    world.account.playlists[account_id] = [*_ids("1", "2"), "t9", *_ids("3", "4")]
    envelopes: list[dict] = []
    for _ in range(2):
        envelope = exited(sync())
        envelopes.append(envelope)
    assert any(pair_cli.FINISHING in _codes(one) for one in envelopes), envelopes
    assert world.held(opener) == ["2", "3", "4", "1"]
    assert world.account.playlists[account_id] == [*_ids("2", "3", "4"), "t9", "t1"]


def test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it(
    world, owed, cfg, monkeypatch
):
    """R-1432 with U234: only a finish places an unread track by the target.

    Settled readings show the person's move of t9 alone (R-1446), so t9 keeps
    the place the person gave it, behind t3, while rekordbox still leads.
    """
    opener, account_id = _stopped_after_t9s_move(world, owed, monkeypatch, rekordbox="skip")
    world.account.playlists[account_id] = [*_ids("1", "2"), "t9", *_ids("3", "4")]
    # The pending stop is read first, then its reading is kept and settled.
    for _ in range(4):
        plan_only()
        held = pairs.PairStore(cfg).get(account_id)
        if held is not None and held.stop_seen is not None and held.stop_seen.settled:
            break
    assert held is not None and held.stop_seen is not None and held.stop_seen.settled, held
    world.account.playlists[account_id] = [*_ids("1", "2", "3"), "t9", "t4"]
    envelopes: list[dict] = []
    # Held while the change settles, then written: rekordbox still leads.
    for left_out in (True, True, False):
        envelope = exited(_synced_keeping_gates(envelopes))
        envelopes.append(envelope)
        assert (pair_cli.LEFT_OUT in _codes(envelope)) is left_out, envelope
    assert world.held(opener) == ["2", "3", "4", "1"]
    assert world.account.playlists[account_id] == [*_ids("2", "3"), "t9", *_ids("4", "1")], (
        "the person's move of t9 was overridden by the stopped write's target"
    )
    # Nor does the gate show R-1432's finish clause, since t9 is not placed by the target.
    warned = [_said(one, pair_cli.UNREAD) for one in envelopes if pair_cli.UNREAD in _codes(one)]
    assert warned, envelopes
    assert not any("finishing a stopped order" in one for one in warned), warned
    shown = [
        str(fact)
        for one in envelopes
        if one.get("cause")
        for fact in one["cause"]["detail"]["shown"].values()
    ]
    assert any("with no title or no artist" in one for one in shown), shown
    assert not any("where the stopped order was taking it" in one for one in shown), shown


# R-1446. A settled move of an unread track alone is no reorder of the readable ones


def _settled_then_moved(world, cfg, account_id: str, settled: list[str], moved: list[str]) -> None:
    """Have plans keep and settle ``settled`` as the account's order after the stop, then list ``moved``."""
    world.account.playlists[account_id] = list(settled)
    for _ in range(4):
        plan_only()
        held = pairs.PairStore(cfg).get(account_id)
        if held is not None and held.stop_seen is not None and held.stop_seen.settled:
            break
    assert held is not None and held.stop_seen is not None and held.stop_seen.settled, held
    world.account.playlists[account_id] = list(moved)


def test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write(
    world, owed, cfg, monkeypatch
):
    """R-1446: the person moves only t9, which neither side's merge reads, after a stop whose rekordbox side was written.

    No readable track moved, so no reorder is shown: the stopped write is
    finished in rekordbox's order and t9 kept where the person put it.
    """
    opener, account_id = _stopped_after_t9s_move(world, owed, monkeypatch)
    _settled_then_moved(
        world,
        cfg,
        account_id,
        [*_ids("1", "2"), "t9", *_ids("3", "4")],
        [*_ids("1", "2", "3"), "t9", "t4"],
    )
    envelopes: list[dict] = []
    # Held while the change settles, as any change after a settled reading is.
    for left_out in (True, True, False):
        envelope = exited(_synced_keeping_gates(envelopes))
        envelopes.append(envelope)
        assert (pair_cli.LEFT_OUT in _codes(envelope)) is left_out, envelope
    assert world.held(opener) == ["2", "3", "4", "1"], "the DJ's rekordbox order was undone"
    # Rekordbox's order, and t9 behind t3 where the person put it.
    assert world.account.playlists[account_id] == [*_ids("2", "3"), "t9", *_ids("4", "1")]
    finishing = [
        _said(one, pair_cli.FINISHING) for one in envelopes if pair_cli.FINISHING in _codes(one)
    ]
    assert finishing, envelopes
    assert not any("so its order leads" in one for one in finishing), finishing
    assert any("order follows rekordbox" in one for one in finishing), finishing
    assert any("only tracks the account cannot read were moved since" in one for one in finishing)
    # The gate says t9 stays where it was put.
    shown = [
        str(fact)
        for one in envelopes
        if one.get("cause")
        for fact in one["cause"]["detail"]["shown"].values()
    ]
    assert any(
        "only tracks the account lists with no title or no artist were moved since" in one
        for one in shown
    ), shown
    assert not any("where the stopped order was taking it" in one for one in shown), shown
    warned = [_said(one, pair_cli.UNREAD) for one in envelopes if pair_cli.UNREAD in _codes(one)]
    assert warned and not any("finishing a stopped order" in one for one in warned), warned
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == (*_ids("2", "3"), "t9", *_ids("4", "1"))
    assert held.stop_seen is None


def test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads(
    world, owed, cfg, monkeypatch
):
    """R-1446 keeps U234: a settled reorder of the readable tracks is the person's, an unread track listed beside them."""
    opener, account_id = _stopped_after_t9s_move(world, owed, monkeypatch)
    _settled_then_moved(
        world,
        cfg,
        account_id,
        [*_ids("1", "2"), "t9", *_ids("3", "4")],
        [*_ids("3", "1", "2"), "t9", "t4"],
    )
    envelopes: list[dict] = []
    for left_out in (True, True, False):
        envelope = exited(_synced_keeping_gates(envelopes))
        envelopes.append(envelope)
        assert (pair_cli.LEFT_OUT in _codes(envelope)) is left_out, envelope
    assert world.held(opener) == ["3", "1", "2", "4"], "the person's settled reorder did not lead"
    finishing = [
        _said(one, pair_cli.FINISHING) for one in envelopes if pair_cli.FINISHING in _codes(one)
    ]
    assert any(
        "reordered since syncs after the stop read it settled" in one for one in finishing
    ), finishing
    assert not any("cannot read were moved since" in one for one in finishing), finishing


def test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder(
    world, owed, cfg, monkeypatch
):
    """R-1446: an order refused before its first move, then only t9 moved by hand.

    Off the path only by t9, which the merge does not read, so it is no
    reorder (R-1420 aside): the write is finished and t9 stays where it was put.
    """
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    real = world.account.order_tracks
    refused: list[str] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id != account_id or refused:
            return real(asked_id, remote_ids, expect=expect, begun=begun, **agreed)
        refused.append(asked_id)
        raise refuse(
            "outbound-remove-refused",
            f"the playlist {asked_id} read differs, so nothing was moved",
            scope=Scope.RUN,
            origin=("test", "order"),
            detail={"playlist_id": asked_id, "problem": "read-differs"},
        )

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert refused and world.account.playlists[account_id] == [*_ids("1", "2", "3", "4"), "t9"]
    world.account.playlists[account_id][:] = [*_ids("1", "2"), "t9", *_ids("3", "4")]
    envelopes: list[dict] = []
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        envelopes.append(envelope)
    assert world.held(opener) == ["2", "3", "4", "1"], "the DJ's rekordbox order was undone"
    assert world.account.playlists[account_id] == [*_ids("2"), "t9", *_ids("3", "4", "1")]
    # The note says it was read against where the write began, not a settled order.
    finishing = [
        _said(one, pair_cli.FINISHING) for one in envelopes if pair_cli.FINISHING in _codes(one)
    ]
    assert any(
        "stands off its path only by where tracks the account cannot read stand" in one
        for one in finishing
    ), finishing
    assert not any("were moved since" in one for one in finishing), finishing


def test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place(
    world, owed, cfg, monkeypatch
):
    """R-1446: t8 and t9 listed untitled, only t8 moved after a settled reading.

    t8 keeps the place the person gave it, and t9, which nobody moved, goes
    where the stopped order was taking it, not left at the front.
    """
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t8", "t9")
    world.account.playlists[account_id].extend(["t8", "t9"])
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == ["t9", *_ids("1", "2", "3", "4"), "t8"]
    _settled_then_moved(
        world,
        cfg,
        account_id,
        ["t9", "t1", "t8", *_ids("2", "3", "4")],
        ["t9", *_ids("1", "2"), "t8", *_ids("3", "4")],
    )
    envelopes: list[dict] = []
    for _ in range(3):
        code, envelope = _synced_keeping_gates(envelopes)
        assert code == int(ExitCode.OK), envelope
        envelopes.append(envelope)
    assert world.held(opener) == ["2", "3", "4", "1"], "the DJ's rekordbox order was undone"
    listed = world.account.playlists[account_id]
    assert listed[0] != "t9", listed
    assert listed == [*_ids("2"), "t8", *_ids("3", "4"), "t9", "t1"], listed
    # The gate says the one moved stays and the other goes where the order was taking it.
    shown = [
        str(fact)
        for one in envelopes
        if one.get("cause")
        for fact in one["cause"]["detail"]["shown"].values()
    ]
    assert any(
        "each one moved stays where it was put, any other goes where the stopped order "
        "was taking it" in one
        for one in shown
    ), shown
    # The unread lines keep R-1432's exception, since t9 is placed by the target.
    assert any("the account's order puts each where the stopped order was" in one for one in shown)
    warned = [_said(one, pair_cli.UNREAD) for one in envelopes if pair_cli.UNREAD in _codes(one)]
    assert any("except that a pair finishing a stopped order" in one for one in warned), warned


def test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them(
    world, owed, cfg, monkeypatch
):
    """R-1446: t7, t8 and t9 listed untitled, t7 and t8 dragged as a block.

    Both stay together where the person put them, since a block moves whole;
    t9, which nobody moved, goes where the stopped order was taking it.
    """
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t7", "t8", "t9")
    world.account.playlists[account_id].extend(["t7", "t8", "t9"])
    _agreeing_at_once(monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == ["t9", *_ids("1", "2", "3", "4"), "t7", "t8"]
    _settled_then_moved(
        world,
        cfg,
        account_id,
        ["t9", "t1", "t7", "t8", *_ids("2", "3", "4")],
        ["t9", *_ids("1", "2", "3"), "t7", "t8", "t4"],
    )
    envelopes: list[dict] = []
    for _ in range(3):
        code, envelope = _synced_keeping_gates(envelopes)
        assert code == int(ExitCode.OK), envelope
        envelopes.append(envelope)
    assert world.held(opener) == ["2", "3", "4", "1"], "the DJ's rekordbox order was undone"
    assert world.account.playlists[account_id] == [
        *_ids("2", "3"), "t7", "t8", "t4", "t9", "t1"
    ], world.account.playlists[account_id]


def test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order(world, owed, cfg, monkeypatch):
    """R-1432: with every track read, the finish leaves the account in rekordbox's order, as before."""
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    reached = _finished_after_one_move(world, monkeypatch, account_id)
    assert reached == _ids("4", "1", "2", "3")
    assert world.account.playlists[account_id] == _ids("2", "3", "4", "1")
    assert world.held(opener) == ["2", "3", "4", "1"]


class _InMemorySteps(pair_cli.PairSteps):
    """One pair's steps kept in memory, as a run's record keeps them, with nothing on disk."""

    def __init__(self) -> None:
        super().__init__(steps=object(), key="the-pair")
        self.kept: dict[str, object] = {}

    def has(self, step: str) -> bool:
        return step in self.kept

    def get(self, step: str, default=None):
        return self.kept.get(step, default)

    def mark(self, step: str, value=True) -> None:
        self.kept[step] = value

    def carry(self) -> None:
        return None

    def carried(self, step: str):
        return None


def test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading():
    """R-1418: ``agreed`` is passed only when the plan read the account it finishes.

    A stand in that does not take ``agreed`` is asked as before. No sync makes
    such a plan, so it is built by hand.
    """
    from cratekit.sync import pair_merge, pair_write
    from cratekit.write import playlist_pair

    one = pair_cli.PairPlan(
        target=pair_cli.Target(account_id="acct", rekordbox_id="7", marked=True),
        name="Opener",
        rekordbox_name="Opener",
        first=False,
        merged=pair_merge.Merged(
            order=("remote:t6", "remote:t5"), leader="rekordbox", first=False
        ),
        account_now=(),
        rekordbox_before=(),
        change=playlist_pair.Change(playlist_id="7", before=()),
        account_adds=("t5", "t6"),
        account_order=("t6", "t5"),
        finishing_order=True,
    )
    asked: list[tuple[str, tuple[str, ...], object]] = []

    class Before1411:
        """An adapter of the protocol as it stood before R-1411, which takes no ``agreed``."""

        def add_tracks(self, playlist_id, remote_ids):
            return tuple(remote_ids)

        def order_tracks(self, playlist_id, remote_ids, *, expect=None, begun=None):
            asked.append((playlist_id, tuple(remote_ids), expect))
            return tuple(remote_ids)

    done = pair_cli.Done(account_id="acct")
    after = pair_write._write_account(
        one, Before1411(), "acct", done, _InMemorySteps(), account_listed=None
    )
    assert asked == [("acct", ("t6", "t5"), None)]
    assert after == ("t6", "t5")
    assert done.order_refused is None


# R-1432. Where a finish puts an unread track, read alone


@pytest.mark.parametrize(
    ("ordered", "listed", "expected"),
    [
        (["t2", "t1"], ["t9", "t1", "t2"], ("t9", "t2", "t1")),
        (["t2", "t1"], ["t1", "t9", "t2"], ("t2", "t1", "t9")),
        (["t2", "t1"], ["t1", "t2", "t9"], ("t2", "t9", "t1")),
        (["t2", "t1"], ["t1", "t2"], ("t2", "t1")),
    ],
)
def test_with_no_stopped_write_an_unread_track_follows_the_one_listed_before_it(
    ordered, listed, expected
):
    """R-1264's rule, unchanged where no write stopped: behind the track listed before it."""
    from cratekit.sync import pair_plan
    assert pair_plan._with_unread_placed(ordered, listed) == expected
    assert pair_plan._with_unread_placed(ordered, listed, ()) == expected


@pytest.mark.parametrize(
    ("ordered", "listed", "target", "expected"),
    [
        # The stopped move put t9 in front, the target puts it behind t4.
        (
            ["t2", "t3", "t4", "t1", "t5"],
            ["t9", "t1", "t2", "t3", "t4", "t5"],
            ["t2", "t3", "t4", "t9", "t1"],
            ("t2", "t3", "t4", "t9", "t1", "t5"),
        ),
        # Two unread ids the target names, in either order the moves left them.
        (
            ["t2", "t1"],
            ["u2", "u1", "t1", "t2"],
            ["t2", "u1", "u2", "t1"],
            ("t2", "u1", "u2", "t1"),
        ),
        (
            ["t2", "t1"],
            ["u1", "u2", "t1", "t2"],
            ["t2", "u1", "u2", "t1"],
            ("t2", "u1", "u2", "t1"),
        ),
        # The track the target puts before it is gone: behind the one before that.
        (
            ["t2", "t1"],
            ["t9", "t1", "t2"],
            ["t2", "t3", "t9", "t1"],
            ("t2", "t9", "t1"),
        ),
        # First in the target: the front.
        (["t2", "t1"], ["t1", "t2", "t9"], ["t9", "t2", "t1"], ("t9", "t2", "t1")),
        # An unread id the target does not name follows the track listed before it.
        (
            ["t2", "t1"],
            ["t9", "t8", "t1", "t2"],
            ["t2", "t9", "t1"],
            ("t2", "t9", "t8", "t1"),
        ),
        # An unread id of the target the playlist no longer holds is never put back.
        (["t2", "t1"], ["t1", "t2"], ["t2", "t9", "t1"], ("t2", "t1")),
    ],
)
def test_at_a_finish_an_unread_track_is_placed_by_the_stopped_writes_target(
    ordered, listed, target, expected
):
    """R-1432: each unread id the target names stands behind the track the target puts before it."""
    from cratekit.sync import pair_plan
    assert pair_plan._with_unread_placed(ordered, listed, target) == expected


# R-1434: a stopped write over an unread track, read by the tracks the plan reads


def _with_unread_t9(world, owed, monkeypatch):
    """The account lists t1 to t4 and then t9 with no title, and rekordbox is reordered 2, 3, 4, 1.
    Answers the rekordbox playlist and the account playlist."""
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    return opener, account_id


def _stopped_before_the_first_send(world, owed, monkeypatch):
    """The write stops after its ordering step and before its first move is sent,
    as a dropped connection does, so no moving step is recorded."""
    opener, account_id = _with_unread_t9(world, owed, monkeypatch)
    world.account.fail_on = frozenset({account_id})
    world.account.transient = True
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    world.account.fail_on = frozenset()
    assert world.account.ordered == [], "a move was sent"
    assert world.account.playlists[account_id] == [*_ids("1", "2", "3", "4"), "t9"]
    assert world.held(opener) == ["2", "3", "4", "1"]
    return opener, account_id


def _moved(world, account_id: str, remote_id: str, at: int) -> None:
    """The person moves one track on the account, to ``at``."""
    members = world.account.playlists[account_id]
    members.remove(remote_id)
    members.insert(at, remote_id)


def _moved_twice_and_synced(world, account_id: str, remote_id: str, *, plans: int, syncs: int):
    """The person moves ``remote_id`` behind t1, ``plans`` plans read it, then behind t2, and ``syncs`` syncs run.

    Two moves read the agreement window apart are the person's reorder (U234).
    Answers each sync's envelope, in order.
    """
    _moved(world, account_id, remote_id, 1)
    for _ in range(plans):
        plan_only()
    _moved(world, account_id, remote_id, 2)
    assert world.account.playlists[account_id][:3] == ["t1", "t2", remote_id]
    envelopes: list[dict] = []
    for _ in range(syncs):
        envelope = exited(sync())
        envelopes.append(envelope)
    return envelopes


def test_a_stop_before_the_first_send_with_nothing_moved_is_finished_from_its_start(
    world, owed, cfg, monkeypatch
):
    """R-1434: the account still stands where the write began, so the finish puts it in the asked order."""
    opener, account_id = _stopped_before_the_first_send(world, owed, monkeypatch)
    envelope = exited(sync())
    assert pair_cli.FINISHING in _codes(envelope)
    assert world.account.playlists[account_id] == ["t2", "t3", "t4", "t9", "t1"]
    assert world.held(opener) == ["2", "3", "4", "1"]


def test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put(
    world, owed, cfg, monkeypatch
):
    """R-1434: a move of a track the plan cannot read is never read as a reorder of the tracks it can.

    Judged with t9 in the path, the move would read off the path and the old
    readable order would undo rekordbox's reorder.
    """
    _agreeing_at_once(monkeypatch)
    opener, account_id = _stopped_before_the_first_send(world, owed, monkeypatch)
    _moved_twice_and_synced(world, account_id, "t9", plans=2, syncs=2)
    assert world.held(opener) == ["2", "3", "4", "1"], "rekordbox took the order the write began from"
    # The readable tracks in rekordbox's order, t9 where the person put it, behind t2.
    assert world.account.playlists[account_id] == ["t2", "t9", "t3", "t4", "t1"]


def test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put(
    world, owed, cfg, monkeypatch
):
    """R-1434: the same for a write whose moves went, its first taking t9 to the front (R-1418).
    The path is read on the readable tracks, so moves of t9 never lead."""
    _agreeing_at_once(monkeypatch)
    opener, account_id = _with_unread_t9(world, owed, monkeypatch)
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == ["t9", *_ids("1", "2", "3", "4")]
    envelopes = _moved_twice_and_synced(world, account_id, "t9", plans=4, syncs=3)
    assert world.held(opener) == ["2", "3", "4", "1"], "rekordbox took the order the moves left"
    assert world.account.playlists[account_id] == ["t2", "t9", "t3", "t4", "t1"]
    # The hold while the second move settles promises what the finish then does.
    held = [
        _said(one, pair_cli.LEFT_OUT)
        for one in envelopes
        if pair_cli.LEFT_OUT in _codes(one) and "read it settled" in _said(one, pair_cli.LEFT_OUT)
    ]
    assert held, "the second move was not held to settle"
    for line in held:
        assert "the account's order is read as yours" not in line, line
        assert "with no title or no artist stays where you put it and the others are finished" in line, line


def test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved(
    world, owed, cfg, monkeypatch
):
    """R-1434: the ordering step's start keeps the unread ids, so a track read since is judged by its place.

    Readable now, t9's move by the person leads; a start without it would read
    every move of t9 as on the path and put it back.
    """
    from tests.test_sync_pair_discover import LivePlaylist

    _agreeing_at_once(monkeypatch)
    reads = LivePlaylist.tracks
    opener, account_id = _stopped_before_the_first_send(world, owed, monkeypatch)
    monkeypatch.setattr(LivePlaylist, "tracks", reads)
    _moved_twice_and_synced(world, account_id, "t9", plans=2, syncs=2)
    assert world.account.playlists[account_id] == _ids("1", "2", "9", "3", "4")
    assert world.held(opener) == ["1", "2", "9", "3", "4"]


def _five_owed(world):
    """A pair of the playlist 1 to 5 synced once. Answers the rekordbox playlist and the account playlist."""
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", "5", under=gig)
    exited(sync())
    return opener, world.titled("GIG READY Opener")


def _order_dropped_once(world, monkeypatch, playlist_id: str) -> None:
    """The next order of ``playlist_id`` is dropped before any move is begun; a removal still lands."""
    real = world.account.order_tracks
    dropped: list[tuple[str, ...]] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id != playlist_id or dropped:
            return real(asked_id, remote_ids, expect=expect, begun=begun, **agreed)
        dropped.append(tuple(remote_ids))
        raise refuse("unavailable-transient", "dropped", scope=Scope.RUN, origin=("test", "order"))

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)


def test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads(world, cfg, monkeypatch):
    """R-1434: the path is the stopped write's own, read on the tracks the plan reads.

    It is the whole start's path cut to the readable tracks, never one worked
    out again without t5, on which the person's move would read as on the path.
    """
    _agreeing_at_once(monkeypatch)
    opener, account_id = _five_owed(world)
    _reordered(world, opener, "1", "3", "2", "5", "4")
    world.account.fail_on = frozenset({account_id})
    world.account.transient = True
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    world.account.fail_on = frozenset()
    assert world.account.ordered == [], "a move was sent"
    _listed_unread(monkeypatch, "t5")
    world.account.playlists[account_id] = ["t3", "t1", "t2", "t4", "t5"]
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["3", "1", "2", "5", "4"], "the person's reorder did not lead"
    assert world.account.playlists[account_id] == ["t3", "t1", "t2", "t4", "t5"]


def test_a_reorder_after_a_finish_stopped_before_its_first_send_leads(world, cfg, monkeypatch):
    """R-1434: the same for a finish whose target places an unread track by the write it finishes (R-1432).
    Its own path, with t9 behind t2, never shows the person's order."""
    _agreeing_at_once(monkeypatch)
    opener, account_id = _five_owed(world)
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    _reordered(world, opener, "1", "3", "2", "5", "4")
    _order_dropped_once(world, monkeypatch, account_id)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    world.rekordbox_remove(opener, "5")
    _order_dropped_once(world, monkeypatch, account_id)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == [*_ids("1", "2", "3", "4"), "t9"]
    world.account.playlists[account_id] = ["t3", "t1", "t2", "t4", "t9"]
    for _ in range(3):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["3", "1", "2", "4"], "the person's reorder did not lead"
    assert world.account.playlists[account_id] == ["t3", "t1", "t2", "t4", "t9"]


@pytest.mark.parametrize("unread", [False, True], ids=["all-read", "t9-unread"])
def test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads(world, owed, cfg, monkeypatch, unread):
    """R-1434: a write known to have sent no move left the account where it began.

    Any other order is the person's (R-1420), even a drag to the top that
    stands where the write's first move would have put it.
    """
    _agreeing_at_once(monkeypatch)
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    if unread:
        _listed_unread(monkeypatch, "t9")
        world.account.playlists[account_id].append("t9")
    world.account.fail_on = frozenset({account_id})
    world.account.transient = True
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    world.account.fail_on = frozenset()
    assert world.account.ordered == [], "a move was sent"
    _moved(world, account_id, "t4", 0)
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["4", "1", "2", "3"], "the person's drag did not lead"
    assert world.account.playlists[account_id] == [*_ids("4", "1", "2", "3"), *(["t9"] if unread else [])]


# R-1446. Whether a reorder read after a stop moved a readable track, read alone


def _write_from(start: list[str], target: list[str]):
    from datetime import UTC, datetime

    from cratekit.sync import pair_stopped

    return pair_stopped.StoppedWrite(
        run_id="run-1",
        account_id="acct",
        at=datetime(2026, 11, 7, tzinfo=UTC),
        start=tuple(start),
        target=tuple(target),
        leader="rekordbox",
        rekordbox=(),
        written=True,
        links={},
    )


START = ["t1", "t2", "t3", "t4", "t9"]
TARGET = ["t2", "t3", "t4", "t9", "t1"]


@pytest.mark.parametrize(
    ("kept", "reading", "unread", "moved"),
    [
        # Only the unread track moved between the settled reading and now.
        (["t1", "t2", "t9", "t3", "t4"], ["t1", "t2", "t3", "t9", "t4"], {"t9"}, False),
        # A readable track moved, the unread one with it or not.
        (["t1", "t2", "t9", "t3", "t4"], ["t3", "t1", "t2", "t9", "t4"], {"t9"}, True),
        (["t1", "t2", "t9", "t3", "t4"], ["t9", "t3", "t1", "t2", "t4"], {"t9"}, True),
        # With t9 readable now, its move is a reorder of the tracks the merge reads.
        (["t1", "t2", "t9", "t3", "t4"], ["t1", "t2", "t3", "t9", "t4"], set(), True),
        # Two unread tracks moving round each other.
        (["u1", "t1", "u2", "t2"], ["u2", "t1", "t2", "u1"], {"u1", "u2"}, False),
    ],
)
def test_a_settled_reorder_moved_a_readable_track_only_when_one_moved(kept, reading, unread, moved):
    """R-1446: the settled reading and now are compared with every unread id left out."""
    from cratekit.sync import pair_plan
    settled = pairs.StopReading("run-1", tuple(kept), "2026-11-07T00:00:00+00:00", settled=True)
    write = _write_from(START, TARGET)
    assert pair_plan._readable_moved(write, settled, reading, unread, moved_nothing=False) is moved


def test_with_no_settled_reading_a_reorder_stands_as_read():
    """R-1446: a reorder read with no settled reading kept to compare is left as it was read."""
    from cratekit.sync import pair_plan
    write = _write_from(START, TARGET)
    reading = ["t1", "t2", "t3", "t9", "t4"]
    assert pair_plan._readable_moved(write, None, reading, {"t9"}, moved_nothing=False)
    unsettled = pairs.StopReading("run-1", tuple(reading), "2026-11-07T00:00:00+00:00")
    assert pair_plan._readable_moved(write, unsettled, reading, {"t9"}, moved_nothing=False)


@pytest.mark.parametrize(
    ("reading", "unread", "moved"),
    [
        # Off the path only by where the unread track stands.
        (["t1", "t2", "t9", "t3", "t4"], {"t9"}, False),
        # A readable track off the path.
        (["t2", "t1", "t9", "t3", "t4"], {"t9"}, True),
        (["t2", "t1", "t3", "t4", "t9"], {"t9"}, True),
        # Nothing unread: the place of t9 is read too.
        (["t1", "t2", "t9", "t3", "t4"], set(), True),
    ],
)
def test_after_a_write_that_sent_nothing_only_readable_tracks_off_its_path_are_a_reorder(
    reading, unread, moved
):
    """R-1446: a write known to have sent no move is off its path only where a readable track is."""
    from cratekit.sync import pair_plan
    write = _write_from(START, TARGET)
    assert pair_plan._readable_moved(write, None, reading, unread, moved_nothing=True) is moved


def test_the_unread_tracks_moved_since_the_stop_are_those_off_the_order_both_readings_share():
    """R-1446: the moved unread ids are those outside the longest run both orders share, readable ids held."""
    from cratekit.sync import pair_plan
    write = _write_from(START, TARGET)
    kept = pairs.StopReading("run-1", ("t9", "t1", "t8", "t2", "t3", "t4"), "2026-11-07T00:00:00+00:00", settled=True)
    assert pair_plan._unread_moved(
        write, kept, ["t9", "t1", "t2", "t8", "t3", "t4"], {"t8": None, "t9": None},
        moved_nothing=False,
    ) == {"t8"}
    # t9 moved behind t1 is the one moved, not t8; a track added since moves none.
    assert pair_plan._unread_moved(
        write, kept, ["t1", "t9", "t8", "t2", "t3", "t4"], {"t8": None, "t9": None},
        moved_nothing=False,
    ) == {"t9"}
    three = {"t7": None, "t8": None, "t9": None}
    # A block of two dragged together is moved whole.
    block = pairs.StopReading(
        "run-1", ("t9", "t1", "t7", "t8", "t2", "t3", "t4"), "2026-11-07T00:00:00+00:00",
        settled=True,
    )
    assert pair_plan._unread_moved(
        write, block, ["t9", "t1", "t2", "t3", "t7", "t8", "t4"], three, moved_nothing=False
    ) == {"t7", "t8"}
    # One moved in front of another, or away from in front of it, moves only itself.
    ahead = pairs.StopReading(
        "run-1", ("t9", "t1", "t7", "t2", "t3", "t4", "t8"), "2026-11-07T00:00:00+00:00",
        settled=True,
    )
    assert pair_plan._unread_moved(
        write, ahead, ["t7", "t9", "t1", "t2", "t3", "t4", "t8"], three, moved_nothing=False
    ) == {"t7"}
    away = pairs.StopReading(
        "run-1", ("t7", "t9", "t1", "t2", "t3", "t4", "t8"), "2026-11-07T00:00:00+00:00",
        settled=True,
    )
    assert pair_plan._unread_moved(
        write, away, ["t9", "t1", "t2", "t7", "t3", "t4", "t8"], three, moved_nothing=False
    ) == {"t7"}
    assert pair_plan._unread_moved(
        write, kept, ["t9", "t5", "t1", "t8", "t2", "t3", "t4"], {"t8": None, "t9": None},
        moved_nothing=False,
    ) == set()
    # A write that sent nothing is read against where it began.
    assert pair_plan._unread_moved(
        write, None, ["t1", "t2", "t9", "t3", "t4"], {"t9": None}, moved_nothing=True
    ) == {"t9"}
    # With no settled reading there is nothing to compare.
    unsettled = pairs.StopReading("run-1", ("t1", "t9"), "2026-11-07T00:00:00+00:00", settled=False)
    assert pair_plan._unread_moved(
        write, unsettled, ["t9", "t1"], {"t9": None}, moved_nothing=False
    ) == set()
    assert pair_plan._unread_moved(write, None, ["t9", "t1"], {"t9": None}, moved_nothing=False) == set()
