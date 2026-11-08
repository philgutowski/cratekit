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
from cratekit.modules.outbound import pairs, tidal_account
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


def test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change(
    world, owed, cfg, monkeypatch
):
    """U234: the reorder is shown by two agreed readings after the stop in different orders."""
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
    # Two syncs read it agreed and write nothing, keeping that reading, settled.
    plan_only()
    plan_only()
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.stop_seen is not None
    assert held.stop_seen.order == tuple(_ids("2", "4", "1", "3")) and held.stop_seen.settled
    # And the person moves it again: U231 holds the new reading until it agrees,
    # then U234 holds it until it agrees as the order after the settled one.
    world.account.playlists[account_id][:] = _ids("3", "2", "4", "1")
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope), "one reading was taken as agreed"
        assert world.held(opener) == ["4", "3", "1", "2"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["3", "2", "4", "1"]
    assert world.account.playlists[account_id] == _ids("3", "2", "4", "1")
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("3", "2", "4", "1"))
    assert held.seen is None and held.stop_seen is None


def test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order(
    world, owed, cfg, monkeypatch
):
    """U234: one agreed reading off the path is not the person's reorder on that alone.

    Until U234 this reading led and was written into rekordbox.
    """
    opener, account_id = owed
    _agreeing_at_once(monkeypatch)
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    del world.account.served[account_id]
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["4", "3", "1", "2"], "rekordbox took the agreed reading"
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")


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
    # Round one's row 1: the finishing write moves nothing until the adapter's
    # own reading is the one the plan agreed on, not merely the same tracks.
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
    """Round two's review: the refused finish's record does not hide the stopped write it finishes.

    Read in its place, the next run took the provider serving the order from
    before the moves as the person's reorder and wrote it into rekordbox.
    """
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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


# ═══════════════════════════════════════════════════════════════════════════
# R-1411: a finish that also adds a track is held to the agreed reading
# ═══════════════════════════════════════════════════════════════════════════


def _adapter_reading(world, monkeypatch, playlist_id: str, reading: list[str]) -> list[object]:
    """Make the adapter's own reading before the order serve ``reading``, and plan its moves from it.

    The fake account's order stands in for the adapter's: its reading, one
    the provider serves seconds after the plan's, holds every track the
    write left (the membership check passes) and stands in ``reading``'s
    order. Judged by the adapter's own rule against the ``agreed`` reading
    the write passes, it is refused with nothing moved as the adapter
    refuses it; passed, each move is sent by the position that reading gives
    it, as the adapter sends it, onto the playlist as it really stands.
    Answers the ``agreed`` each order was asked with.
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
    """A stop after one of three moves, served as that move left it, then a track added in rekordbox.

    Two readings agree on the account as the one move left it and the plan
    finishes the stopped write, which now also adds track 5 to the account.
    """
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
    # Held once while two readings agree, then the finish refused with nothing
    # moved, its addition landed and the stopped write left pending, twice.
    assert codes[0] == codes[2] == int(ExitCode.OK)
    assert codes[1] != int(ExitCode.OK) and codes[3] != int(ExitCode.OK)
    assert world.account.playlists[account_id] == [*reached, "t5"], "moves were sent from a lag"
    assert world.held(opener) == ["4", "3", "2", "1", "5"], "a lag was merged into rekordbox"
    # Each finish held to the reading the plan agreed on: the order the one
    # move left, and once the refused finish's addition landed, with it.
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
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
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
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
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


# ═══════════════════════════════════════════════════════════════════════════
# R-1411, round one's review: the agreed reading is the plan's, on every path
# ═══════════════════════════════════════════════════════════════════════════


def _refused_finish(world, monkeypatch, account_id: str, lag: list[str]) -> tuple[list[object], str]:
    """The adapter's reading lagging the stopped move: held once, then the finish refused.

    Answers the agreed readings asked and the run whose finish was refused,
    for a continue of it.
    """
    asked = _adapter_reading(world, monkeypatch, account_id, lag)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    code, refused = sync()
    assert code != int(ExitCode.OK), refused
    return asked, refused["run_id"]


@pytest.mark.parametrize("adding", [True, False])
def test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks(
    world, owed, cfg, monkeypatch, adding
):
    """Row 1 of round one: on a continue the check's listing is read for what it holds, not its order.

    The provider serves the order from before the stopped move to the
    continue's check and to the adapter alike, so the check's listing is
    the lag; held to it, the moves went by position from the lag and left
    4, 3, 1, 2 under an ok exit.
    """
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
    # Round two's row 4: the continue reached the adapter and was refused there.
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
    """Row 2 of round one: a held plan that cannot be read leaves no check listing to pass."""
    opener, account_id, reached = _stopped_then_added(world, owed, monkeypatch)
    asked = _adapter_reading(world, monkeypatch, account_id, _ids("1", "2", "3", "4", "5"))
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
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
    # Refused, read-differs: the plan made again in this command, its finish
    # held to that plan's own reading of the account, which the write's
    # addition is not yet on.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["detail"]["problem"] == "read-differs", envelope
    assert world.account.playlists[account_id] == [*reached, "t5"], "moves were sent from a lag"
    assert asked == [tuple(reached)], "the finish planned again passed no agreed reading"
    assert world.held(opener) == ["4", "3", "2", "1", "5"]


# ═══════════════════════════════════════════════════════════════════════════
# U234. A pending order agreed off its moves' path is the provider's state
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def longer(world):
    """One GIG READY pair synced on seven tracks, then reversed in rekordbox, so its account owes six moves."""
    gig = world.folder("GIG READY")
    closer = world.playlist("Closer", "1", "2", "3", "4", "5", "6", "7", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, closer, "7", "6", "5", "4", "3", "2", "1")
    return closer, world.titled("GIG READY Closer")


def _stopping_off_the_path(world, monkeypatch, playlist_id: str) -> list[int]:
    """Sitting 87's stop: three moves told as accepted, the fourth ending on its 412s, the account off the path.

    The counts are told as the adapter tells them (R-1394): before each
    move, and brought back down after each 412. The second move had in fact
    landed under its 412 and was sent again by its position, which took t1
    to the front, so the provider holds an order no count of the moves leaves.
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
    """Sitting 87, through U231's hold: no rekordbox order from the agreed half done order."""
    closer, account_id = longer
    _agreeing_at_once(monkeypatch)
    stops = _stopping_off_the_path(world, monkeypatch, account_id)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert stops == [3]
    left = list(world.account.playlists[account_id])
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the plan writes rekordbox the provider's half done order"
    )
    assert [item["action"] for item in pair if item["side"] == "account"] == ["order"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == ["7", "6", "5", "4", "3", "2", "1"]
    assert world.account.playlists[account_id] == _ids("7", "6", "5", "4", "3", "2", "1")
    assert (account_id, tuple(left)) in world.account.agreed, "the rest moved from another reading"
    assert "none of its moves leaves" in _said(envelope, pair_cli.FINISHING)

# R-1418: the reading a finish is held to carries the unread tracks in place
# ═══════════════════════════════════════════════════════════════════════════


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

    The account lists t9 with no title, so the plan keeps it unread behind
    t4, and rekordbox's 2, 3, 4, 1 puts it first of four moves to the front.
    The stop leaves every readable track where it stood: a reading lagging
    that move differs from the one it left only by where t9 stands, so a
    finish held to the readable tracks alone takes the lag and sends the
    remaining moves by position from it.
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
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    code, envelope = sync()
    # Refused at the adapter with nothing moved, its addition landed and
    # rekordbox untouched by the lag.
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["detail"]["problem"] == "read-differs", envelope
    assert world.account.playlists[account_id] == [*reached, "t5"], "moves were sent from a lag"
    assert world.held(opener) == ["2", "3", "4", "1", "5"], "a lag was merged into rekordbox"
    # Held to the plan's reading with the unread id in its place, not to the
    # tracks the provider could read.
    assert asked == [tuple(reached)], "the finish was not held to the unread track's place"
    # Served as the move left it, the stopped write finishes.
    _adapter_reading(world, monkeypatch, account_id, [*reached, "t5"])
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    # The readable tracks in rekordbox's order, and t9 where the stopped
    # write was taking it, behind t4, not in front where its one move left
    # it (R-1432).
    assert world.account.playlists[account_id] == [*_ids("2", "3", "4"), "t9", *_ids("1", "5")]
    assert world.held(opener) == ["2", "3", "4", "1", "5"]


def _finished_after_one_move(
    world, monkeypatch, account_id: str, envelopes: list[dict] | None = None
) -> list[str]:
    """Stop the account order after its first move, then sync until the stopped write finishes.

    Answers the playlist as the stopped move left it, and keeps each later
    sync's answer in ``envelopes`` when given. The provider serves the
    account as it stands, so the pending order is read at once and the
    readings agree on the next sync.
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

    The account lists t1 to t4 and then t9 with no title, and rekordbox's
    2, 3, 4, 1 asks 2, 3, 4, 9, 1. The finish reads every readable track as
    the write would have left it, and places t9 by that write's own target,
    behind t4, rather than behind the track the stopped move left it after,
    which is none, so the front.
    """
    opener, account_id = owed
    _reordered(world, opener, "2", "3", "4", "1")
    _listed_unread(monkeypatch, "t9")
    world.account.playlists[account_id].append("t9")
    envelopes: list[dict] = []
    reached = _finished_after_one_move(world, monkeypatch, account_id, envelopes)
    assert reached == ["t9", *_ids("1", "2", "3", "4")]
    assert world.account.playlists[account_id] == [*_ids("2", "3", "4"), "t9", "t1"]
    # The gate says so, rather than that the unread track stays where it is
    # (the review's round one).
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
    """R-1432: an unread track at the tail the stopped write kept stays at the tail.

    Rekordbox's 1, 3, 2, 4 asks 1, 3, 2, 4, 9, whose moves are t3 then t1,
    so t9 is never moved; the write stops after t3's, and the finish leaves
    t9 behind t4 as both the listing and the target place it.
    """
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
    """R-1432, the review's round one: the stopped write's target names t9, the account no longer lists it.

    The finish places only what the account lists, so t9 is neither in the
    order it asks nor in the snapshot it records.
    """
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
    """R-1432 with U234: an order off the stopped write's path is its partial state until readings settle.

    The person drags t9 between t2 and t3 before any sync reads the stop, so
    the first reading is off the path and nothing kept says a person moved
    it: the stopped write is finished, t9 where it was taking it, and
    rekordbox keeps its order.
    """
    opener, account_id = _stopped_after_t9s_move(world, owed, monkeypatch)
    world.account.playlists[account_id] = [*_ids("1", "2"), "t9", *_ids("3", "4")]
    envelopes: list[dict] = []
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        envelopes.append(envelope)
    assert any(pair_cli.FINISHING in _codes(one) for one in envelopes), envelopes
    assert world.held(opener) == ["2", "3", "4", "1"]
    assert world.account.playlists[account_id] == [*_ids("2", "3", "4"), "t9", "t1"]


def test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it(
    world, owed, cfg, monkeypatch
):
    """R-1432, the review's round one, with U234: only a finish places an unread track by the target.

    The stop skips rekordbox, so nothing of it is folded and rekordbox's
    2, 3, 4, 1 still leads against the old base. The person drags t9
    between t2 and t3, two plans read that settled, and the person then
    drags it between t3 and t4: settled readings show a reorder, and since
    R-1446 one of the unread track alone, so the plan finishes the stopped
    write with rekordbox leading and t9 keeps the place the person gave it,
    behind t3, rather than the one the stopped write was taking it to,
    behind t4.
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
        code, envelope = _synced_keeping_gates(envelopes)
        assert code == int(ExitCode.OK), envelope
        envelopes.append(envelope)
        assert (pair_cli.LEFT_OUT in _codes(envelope)) is left_out, envelope
    assert world.held(opener) == ["2", "3", "4", "1"]
    assert world.account.playlists[account_id] == [*_ids("2", "3"), "t9", *_ids("4", "1")], (
        "the person's move of t9 was overridden by the stopped write's target"
    )
    # Nor does the gate say so (the review's round two): the finish clause of
    # R-1432 is not shown, since t9 is not put where the target takes it.
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


# ═══════════════════════════════════════════════════════════════════════════
# R-1446. A settled move of an unread track alone is no reorder of the readable ones
# ═══════════════════════════════════════════════════════════════════════════


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

    The account lists t1 to t4 and then t9 with no title, rekordbox's
    2, 3, 4, 1 asks 2, 3, 4, 9, 1, and the write stops after its first
    move put t9 in front, rekordbox written, so the bases are what the
    stopped write left. The person drags t9 between t2 and t3, plans read
    that settled, and the person drags it between t3 and t4. Every
    readable track still stands where the stopped write left it, so no
    reorder of them is shown: the stopped write is finished, rekordbox
    keeps the order the DJ made, and the account is put in it, t9 kept
    where the person put it. Before, the readings compared t9's place too,
    the account led, and its half done order was put into rekordbox as
    1, 2, 3, 4.
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
        code, envelope = _synced_keeping_gates(envelopes)
        assert code == int(ExitCode.OK), envelope
        envelopes.append(envelope)
        assert (pair_cli.LEFT_OUT in _codes(envelope)) is left_out, envelope
    assert world.held(opener) == ["2", "3", "4", "1"], "the DJ's rekordbox order was undone"
    # The readable tracks finished in rekordbox's order, and t9 where the
    # person put it, behind t3, since its settled move was theirs.
    assert world.account.playlists[account_id] == [*_ids("2", "3"), "t9", *_ids("4", "1")]
    finishing = [
        _said(one, pair_cli.FINISHING) for one in envelopes if pair_cli.FINISHING in _codes(one)
    ]
    assert finishing, envelopes
    assert not any("so its order leads" in one for one in finishing), finishing
    assert any("order follows rekordbox" in one for one in finishing), finishing
    assert any("only tracks the account cannot read were moved since" in one for one in finishing)
    # The gate says t9 stays where it was put, and never that the finish
    # takes it where the stopped order was taking it.
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
    """R-1446 keeps U234: a settled reorder of the readable tracks is the person's, an unread track listed beside them.

    The same stop, rekordbox written. Plans read the account settled with
    t9 between t2 and t3, then the person moves t3 to the front, leaving
    t9 where it was. Held while the change settles, the account's order
    is then read as theirs and leads, as U234 made it, and rekordbox
    takes it.
    """
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
        code, envelope = _synced_keeping_gates(envelopes)
        assert code == int(ExitCode.OK), envelope
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
    """R-1446, one step over: an order refused before its first move, then only t9 moved by hand.

    U234 reads an account off the path of a write known to have sent no
    move as the person's at once (R-1420). Off the path here only by where
    the person put t9, which neither side's merge reads, so the readable
    tracks still stand where the write began: the stopped write is
    finished, rekordbox keeps its order, and t9 stays where it was put.
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
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["2", "3", "4", "1"], "the DJ's rekordbox order was undone"
    assert world.account.playlists[account_id] == [*_ids("2"), "t9", *_ids("3", "4", "1")]


def test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place(
    world, owed, cfg, monkeypatch
):
    """R-1446, the review's round one: t8 and t9 listed untitled, only t8 moved after a settled reading.

    The stop leaves t9 in front where its interrupted move put it. The person
    moves t8 behind t1, plans read that settled, and the person moves t8
    behind t2. No readable track moved, so the stopped write is finished and
    rekordbox keeps its order; t8 keeps the place the person gave it, and
    t9, which nobody moved, is put where the stopped order was taking it,
    not left at the front. Before, every unread track kept the listing's
    place once one was moved, so t9 stayed first.
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
    # The gate says the one moved stays and the other goes where the
    # stopped order was taking it.
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

    A plan that read nothing of the account holds no order to agree on, so
    the finish asks the adapter what it always asked, and a stand in that
    does not take ``agreed`` is asked as before. No sync was found to make
    such a plan: an emptied playlist finishing a stopped write adds in the
    merged order and asks no order (the record's driven candidate), so the
    plan is built by hand.
    """
    from cratekit.sync import pair_merge
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
    after = pair_cli._write_account(
        one, Before1411(), "acct", done, _InMemorySteps(), account_listed=None
    )
    assert asked == [("acct", ("t6", "t5"), None)]
    assert after == ("t6", "t5")
    assert done.order_refused is None


# ═══════════════════════════════════════════════════════════════════════════
# R-1432. Where a finish puts an unread track, read alone
# ═══════════════════════════════════════════════════════════════════════════


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
    assert pair_cli._with_unread_placed(ordered, listed) == expected
    assert pair_cli._with_unread_placed(ordered, listed, ()) == expected


@pytest.mark.parametrize(
    ("ordered", "listed", "target", "expected"),
    [
        # The brief's: the stopped move put t9 in front, the target puts it behind t4.
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
        # An unread id listed since, which the target does not name, follows
        # the track listed before it; the one it names follows the target.
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
    assert pair_cli._with_unread_placed(ordered, listed, target) == expected


# ═══════════════════════════════════════════════════════════════════════════
# R-1446. Whether a reorder read after a stop moved a readable track, read alone
# ═══════════════════════════════════════════════════════════════════════════


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
    settled = pairs.StopReading("run-1", tuple(kept), "2026-11-07T00:00:00+00:00", settled=True)
    write = _write_from(START, TARGET)
    assert pair_cli._readable_moved(write, settled, reading, unread, moved_nothing=False) is moved


def test_with_no_settled_reading_a_reorder_stands_as_read():
    """R-1446: a reorder read with no settled reading kept to compare is left as it was read."""
    write = _write_from(START, TARGET)
    reading = ["t1", "t2", "t3", "t9", "t4"]
    assert pair_cli._readable_moved(write, None, reading, {"t9"}, moved_nothing=False)
    unsettled = pairs.StopReading("run-1", tuple(reading), "2026-11-07T00:00:00+00:00")
    assert pair_cli._readable_moved(write, unsettled, reading, {"t9"}, moved_nothing=False)


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
    write = _write_from(START, TARGET)
    assert pair_cli._readable_moved(write, None, reading, unread, moved_nothing=True) is moved


def test_an_unread_track_moved_since_the_stop_is_read_by_the_track_before_it():
    """R-1446: an unread id is moved when the id listed just before it is another, over ids both hold."""
    write = _write_from(START, TARGET)
    kept = pairs.StopReading("run-1", ("t9", "t1", "t8", "t2", "t3", "t4"), "2026-11-07T00:00:00+00:00", settled=True)
    assert pair_cli._unread_moved(
        write, kept, ["t9", "t1", "t2", "t8", "t3", "t4"], {"t8": None, "t9": None},
        moved_nothing=False,
    ) == {"t8"}
    # Two unread tracks swapped are both moved; a track added since moves none.
    assert pair_cli._unread_moved(
        write, kept, ["t1", "t9", "t8", "t2", "t3", "t4"], {"t8": None, "t9": None},
        moved_nothing=False,
    ) == {"t8", "t9"}
    assert pair_cli._unread_moved(
        write, kept, ["t9", "t5", "t1", "t8", "t2", "t3", "t4"], {"t8": None, "t9": None},
        moved_nothing=False,
    ) == set()
    # A write that sent nothing is read against where it began.
    assert pair_cli._unread_moved(
        write, None, ["t1", "t2", "t9", "t3", "t4"], {"t9": None}, moved_nothing=True
    ) == {"t9"}
    # With no settled reading there is nothing to compare.
    unsettled = pairs.StopReading("run-1", ("t1", "t9"), "2026-11-07T00:00:00+00:00", settled=False)
    assert pair_cli._unread_moved(
        write, unsettled, ["t9", "t1"], {"t9": None}, moved_nothing=False
    ) == set()
    assert pair_cli._unread_moved(write, None, ["t9", "t1"], {"t9": None}, moved_nothing=False) == set()
