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


def _stopping_after(world, monkeypatch, playlist_id: str, moves: int) -> list[int]:
    """Make the order on one playlist send ``moves`` moves and then refuse, as a failed move does."""
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
        if begun is not None:
            begun(tuple(before), tuple(end))
        for one in planned[:moves]:
            members.remove(one)
            members.insert(0, one)
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
