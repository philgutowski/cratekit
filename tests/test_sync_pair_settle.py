"""U231: an account playlist put in rekordbox's order finishes despite the provider's read lag.

Sitting 86's live ``crate sync pair`` read each account playlist back after
every move it made; the provider's reads lagged the moves for minutes, so 32
of 65 orders stopped with every move landed, and the write made 5,794 calls
against a forecast of 4,142. Now the moves are sent with no read back between
them, one judged reading after a settle window decides the order, and an
order the provider does not yet serve is left pending on the pair until two
readings agree. Driven through the dispatcher on the disposable database and
the discovery suite's fake account, whose served order is made to lag.

D1 applies. Nothing here names a real account, a real person or a real track.
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
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "4", "3", "1", "2")
    return opener, world.titled("GIG READY Opener")


def _agreeing_at_once(monkeypatch) -> None:
    """Two readings agree however close together, as if minutes had passed between runs."""
    monkeypatch.setattr(pair_cli, "AGREE_AFTER", timedelta(0))


# ═══════════════════════════════════════════════════════════════════════════
# The write sends its moves blind and reads the order once, after a window
# ═══════════════════════════════════════════════════════════════════════════


def test_an_order_the_provider_serves_at_once_finishes_in_the_one_run(world, owed, cfg):
    opener, account_id = owed
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    ordered = len(world.account.ordered)
    # The provider catches up before the next sync.
    del world.account.served[account_id]
    plan = plan_only()
    assert [item for item in plan["items"] if item["pair"] == account_id] == [], (
        "a pair whose order landed planned a write"
    )
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert len(world.account.ordered) == ordered, "the order was written a second time"
    assert world.held(opener) == ["4", "3", "1", "2"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("4", "3", "1", "2"))
    assert held.seen is None
    assert held_plan.carried() == ([], [])


def test_a_pending_pair_is_held_whole_until_a_later_reading_agrees(world, owed, cfg):
    opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    # The provider now serves a third order, between the two.
    world.account.served[account_id] = _ids("3", "1", "2", "4")
    world.rekordbox_add(opener, "5")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    ordered = len(world.account.ordered)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered


def test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag(
    world, owed, cfg, monkeypatch
):
    """The provider serving the order from before the moves, however long, moves nothing again."""
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    ordered = len(world.account.ordered)
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert len(world.account.ordered) == ordered, "a lagging reading was ordered from"
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2"]


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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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


def test_a_pending_pair_the_person_reordered_by_hand_is_merged_as_their_change(
    world, owed, cfg, monkeypatch
):
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    # The person puts the playlist in an order no move of the write passes.
    del world.account.served[account_id]
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope), "one reading was taken as agreed"
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["2", "4", "1", "3"]
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3")
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("2", "4", "1", "3"))
    assert held.seen is None


# ═══════════════════════════════════════════════════════════════════════════
# A stop part way through the moves
# ═══════════════════════════════════════════════════════════════════════════


def _stopping_after(
    world, monkeypatch, playlist_id: str, moves: int, *, known: bool = True
) -> list[int]:
    """Make the order on one playlist send ``moves`` moves and then refuse, as a failed move does.

    The caller is told the counts before each move as the adapter tells it
    (R-1394): ``known`` is the next move ended on its last 412, which changed
    nothing, so it is told as not landed; otherwise its fate is not known.
    """
    from cratekit.modules.outbound import tidal_account

    real = world.account.order_tracks
    stops: list[int] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None):
        if asked_id != playlist_id or stops:
            return real(asked_id, remote_ids, expect=expect, begun=begun)
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
    code, done = drive(["--run", stopped["run_id"], *VERB])
    assert code == int(ExitCode.OK), done
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
    code, done = drive(["--run", stopped["run_id"], *VERB])
    assert code == int(ExitCode.OK), done
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert world.account.playlists[account_id] == reached
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2"], "rekordbox took the stopped order"


# ═══════════════════════════════════════════════════════════════════════════
# R-1394: a stopped write is finished only from a reading its moves could have left
# ═══════════════════════════════════════════════════════════════════════════


def _three_moves(world, opener) -> None:
    """Rekordbox in an order three moves to the front put the account in: 4, 3, 2, 1 from 1, 2, 3, 4."""
    _reordered(world, opener, "4", "3", "2", "1")


def test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees(
    world, owed, cfg, monkeypatch
):
    """T7 of U231's round one: two readings agreeing on the order before the moves are a lag."""
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
    # Shown as the moves leave it, it finishes with nothing moved.
    world.account.playlists[account_id][:] = _ids("4", "3", "2", "1")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT not in _codes(envelope)
    assert len(world.account.ordered) == ordered
    assert world.held(opener) == ["4", "3", "2", "1"]


# ═══════════════════════════════════════════════════════════════════════════
# Which pairs keep the account's order
# ═══════════════════════════════════════════════════════════════════════════


def test_a_pair_outside_gig_ready_gets_no_order_write_and_its_membership_still_syncs(world, cfg):
    crates = world.folder("Crates")
    deep = world.playlist("Deep", "1", "2", "3", under=crates)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("Crates Deep")
    _reordered(world, deep, "3", "1", "2")
    world.rekordbox_add(deep, "4")
    plan = plan_only()
    assert _items(plan, "account", "order") == []
    assert [item["action"] for item in plan["items"] if item["side"] == "account"] == ["add"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    assert world.account.ordered == []
    assert world.held(deep) == ["3", "1", "2", "4"]


def test_the_config_key_keeps_the_account_order_of_every_pair(world, cfg, monkeypatch):
    every = replace(cfg, outbound=replace(cfg.outbound, pair_order_every_pair=True))
    monkeypatch.setattr(config, "load", lambda *args, **kwargs: every)
    crates = world.folder("Crates")
    deep = world.playlist("Deep", "1", "2", "3", under=crates)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("Crates Deep")
    _reordered(world, deep, "3", "1", "2")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("3", "1", "2")


# ═══════════════════════════════════════════════════════════════════════════
# Round one's review
# ═══════════════════════════════════════════════════════════════════════════


def test_a_write_that_keeps_no_record_sends_no_order(world, owed, cfg, monkeypatch):
    """R1 of round one: moves sent with no read back must be recorded, or a later sync sends them again."""
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert len(world.account.ordered) == 1
    assert pair_cli.PENDING in _codes(envelope)


def test_two_readings_agree_only_once_minutes_apart(world, owed, cfg, monkeypatch):
    """R4 of round one: the agreement rule's gap, AGREE_AFTER, is what a later run waits out."""
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
    monkeypatch.setattr(pair_cli, "_now", lambda: datetime.now(UTC) + later)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2"), (
        envelope["warnings"], pairs.PairStore(cfg).get(account_id)
    )
    assert world.held(opener) == ["4", "3", "1", "2"]


def test_a_reading_kept_from_before_the_moves_is_no_agreement(world, owed, cfg, monkeypatch):
    """R4 of round one: a reading kept for an earlier write does not vouch for this one's."""
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
    """R4 of round one: only what is left of the window is waited."""
    from datetime import UTC, datetime

    start = datetime(2026, 11, 6, 12, 0, tzinfo=UTC)
    ticks = iter(range(0, 10_000, 20))
    monkeypatch.setattr(pair_cli, "_now", lambda: start + timedelta(seconds=next(ticks)))
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.settle_waits
    assert world.account.settle_waits[0] <= pair_cli.SETTLE_SECONDS - 20


def test_a_settle_reading_refused_for_another_reason_stops_the_write(world, owed, monkeypatch):
    """R4 of round one: only an order's own refusals leave it pending; a rejected session still stops."""
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
    """R6 of round one: the scope is the folder, not a playlist of that name."""
    root = world.playlist("GIG READY", "1", "2", "3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, root, "3", "1", "2")
    plan = plan_only()
    assert _items(plan, "account", "order") == []


def test_a_pending_run_does_not_count_its_pending_pair_as_synced(world, owed):
    """R7 of round one: the headline says pending, not synced, for a pair whose snapshot did not move."""
    _opener, account_id = owed
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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


# ═══════════════════════════════════════════════════════════════════════════
# Round two's review
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("damage", ["unreadable", "gone"])
def test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again(
    world, owed, cfg, monkeypatch, damage
):
    """R4 of round two: the carried record says the moves went when the run's steps cannot.

    The run parks in its settle reading with every move sent, the provider
    serving the order from before them, so the check before the continue's
    write finds the playlist as the plan read it and passes.
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
    """R5 of round two: a continue waits only what is left of the window the moves began."""
    from datetime import UTC, datetime

    _opener, account_id = owed
    _stopping_after(world, monkeypatch, account_id, 1)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    monkeypatch.setattr(pair_cli, "_now", lambda: datetime.now(UTC) + timedelta(seconds=20))
    code, done = drive(["--run", stopped["run_id"], *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.settle_waits[-1] <= pair_cli.SETTLE_SECONDS - 15


def test_a_rekordbox_side_to_be_made_is_under_gig_ready_only_inside_the_folder(cfg):
    """R6 of round two: the same rule for a pair whose rekordbox side is new."""
    from cratekit.sync import pair_discover
    from cratekit.write import playlist_pair

    made = playlist_pair.Playlist(
        playlist_id="", name="x", attribute=0, removed=False, ancestors=()
    )
    inside = pair_discover.Home(folder="", name="Opener", parent_id="7", path=("GIG READY", "Opener"))
    named = pair_discover.Home(folder="", name="GIG READY", parent_id="", path=("GIG READY",))
    assert pair_cli._keeps_order(cfg, made, inside) is True
    assert pair_cli._keeps_order(cfg, made, named) is False
