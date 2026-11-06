"""U225: a sync pair after a stopped order write finishes it from the leading side.

Sitting 62's ``crate sync pair`` added tracks to one paired account playlist
and then stopped part way through putting it in order, leaving the account in
an order neither side held. The next fresh ``crate sync pair`` read the
stopped write's own moves as the person's reorder on the account, let the
account lead, and planned to put that scramble into rekordbox. Driven through
the dispatcher on the disposable database and the discovery suite's fake
account, whose order is made to stop after two moves exactly as the adapter
would have made them, then a fresh run of the verb.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

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
from tests.test_sync_pair_discover import VERB, _codes, _said, plan_only, sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414
from tests.test_sync_pair_order import _reordered

#: Rekordbox's order once the person has added three tracks and moved one,
#: so rekordbox alone changed order since the last sync and leads.
LED = ("4", "5", "1", "6", "2", "7", "3")


def _stopping(world, monkeypatch, playlist_id: str, moves: int) -> list[int]:
    """Make the account's order on one playlist stop after ``moves`` moves, as the adapter makes them.

    The moves are the shipped adapter's own (``_to_the_front``), each a track
    taken to the front, and the stop is the refusal a read back that differs
    raises (U220), which stops that pair alone. Answers a list the number of
    stops is appended to.
    """
    real = world.account.order_tracks
    stops: list[int] = []

    def order_tracks(asked_id, remote_ids, *, expect=None):
        if asked_id != playlist_id or len(stops) >= 1:
            return real(asked_id, remote_ids, expect=expect)
        members = world.account.playlists[asked_id]
        for one in tidal_account._to_the_front(list(members), remote_ids)[:moves]:
            members.remove(one)
            members.insert(0, one)
        stops.append(moves)
        raise refuse(
            "outbound-remove-refused",
            f"the playlist {asked_id} read back after a move is not what it held with "
            f"that track moved to the front, so nothing more was moved",
            scope=Scope.RUN,
            origin=("test", "order"),
            detail={"playlist_id": asked_id, "problem": "read-back-differs"},
        )

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    return stops


@pytest.fixture
def stopped(world, monkeypatch):
    """Sitting 62's shape: synced on four tracks, three added in rekordbox, the order stopped after two moves.

    Answers the rekordbox playlist, the account playlist and the stopped run.
    """
    gig = world.folder("GIG READY")
    intro = world.playlist("Intro", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Intro")
    world.rekordbox_add(intro, "5", "6", "7")
    _reordered(world, intro, *LED)
    stops = _stopping(world, monkeypatch, account_id, 2)
    code, refused = sync()
    assert code != int(ExitCode.OK), refused
    assert stops == [2], "the order never ran"
    # The additions landed and two moves were made: an order neither side holds.
    assert world.account.playlists[account_id] == ["t2", "t7", "t1", "t3", "t4", "t5", "t6"]
    assert world.held(intro) == list(LED)
    return intro, account_id, refused["run_id"]


def _ids(*content_ids: str) -> list[str]:
    return [f"t{one}" for one in content_ids]


def test_a_fresh_sync_orders_the_account_to_rekordbox_and_plans_no_rekordbox_order(
    world, stopped
):
    intro, account_id, _run = stopped
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the plan writes rekordbox the stopped write's scramble"
    )
    assert [item["action"] for item in pair if item["side"] == "account"] == ["order"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED), "rekordbox took an order nobody chose"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_the_gate_names_the_pair_as_finishing_the_stopped_run(world, stopped):
    _intro, account_id, run_id = stopped
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert f"finishes run {run_id}" in line
    assert "order follows rekordbox's" in line
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.FINISHING in _codes(envelope)
    said = _said(envelope, pair_cli.FINISHING)
    assert run_id in said and "GIG READY Intro" in said


def test_a_move_the_person_made_on_the_account_after_the_stop_still_leads(world, stopped):
    intro, account_id, _run = stopped
    members = world.account.playlists[account_id]
    members.remove("t3")
    members.insert(0, "t3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t3", "t2", "t7", "t1", "t4", "t5", "t6"]
    assert world.held(intro) == ["3", "2", "7", "1", "4", "5", "6"]
    assert "the account was reordered since" in _said(envelope, pair_cli.FINISHING)


def test_rekordbox_reordered_since_the_stop_leads(world, stopped):
    intro, account_id, _run = stopped
    moved = ("3", "4", "5", "1", "6", "2", "7")
    _reordered(world, intro, *moved)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(moved)
    assert world.account.playlists[account_id] == _ids(*moved)


def test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account(
    world, stopped
):
    intro, account_id, _run = stopped
    world.rekordbox_remove(intro, "6")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == ["4", "5", "1", "2", "7", "3"]
    assert world.account.playlists[account_id] == _ids("4", "5", "1", "2", "7", "3")


def test_a_track_added_on_the_account_after_the_stop_is_kept_and_the_order_still_finishes(
    world, stopped
):
    intro, account_id, _run = stopped
    world.account.playlists[account_id].append("t8")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == [*LED, "8"]
    assert world.account.playlists[account_id] == _ids(*LED, "8")


def test_a_stopped_write_finished_by_its_continue_leaves_nothing_for_the_next_sync(
    world, stopped
):
    intro, account_id, run_id = stopped
    code, done = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.playlists[account_id] == _ids(*LED)
    plan = plan_only()
    assert [item for item in plan["items"] if item["pair"] == account_id] == []
    code, first = drive(VERB)
    assert "finishes run" not in first["cause"]["detail"]["shown"][f"pair {account_id}"]


def test_a_stopped_write_that_skipped_rekordbox_still_finishes_its_order(world, monkeypatch):
    gig = world.folder("GIG READY")
    intro = world.playlist("Intro", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Intro")
    world.rekordbox_add(intro, "5", "6", "7")
    _reordered(world, intro, *LED)
    stops = _stopping(world, monkeypatch, account_id, 2)
    code, refused = sync(rekordbox="skip")
    assert code != int(ExitCode.OK), refused
    assert stops == [2]
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.account == ("t1", "t2", "t3", "t4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED)
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_pair_with_no_stopped_write_is_planned_as_before(world, monkeypatch):
    gig = world.folder("GIG READY")
    intro = world.playlist("Intro", "1", "2", "3", under=gig)
    world.playlist("Other", "4", "5", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Intro")
    other = world.titled("GIG READY Other")
    # A person's reorder on the account leads, as it always has.
    world.account.playlists[account_id] = ["t3", "t1", "t2"]
    stops = _stopping(world, monkeypatch, other, 1)
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert "finishes run" not in first["cause"]["detail"]["shown"][f"pair {account_id}"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert stops == []
    assert world.held(intro) == ["3", "1", "2"]
    assert pair_cli.FINISHING not in _codes(envelope)


def test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot(world, stopped):
    _intro, account_id, run_id = stopped
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    # The stopped run's record is still kept, and the snapshot is later.
    from cratekit.core import held_plan

    assert held_plan.steps_path(run_id).exists()
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert pair_cli.FINISHING not in _codes(again)
    assert [item for item in again["data"]["items"] if item["pair"] == account_id] == []


def test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write(world, stopped):
    from cratekit.core import held_plan

    held_plan.steps_path("2026-11-05T17:42:49Z-5ddd").write_text("{not json")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    said = _said(envelope, pair_cli.STOPPED_UNREAD)
    assert "2026-11-05T17:42:49Z-5ddd" in said
    # The record that can be read is still read.
    assert pair_cli.FINISHING in _codes(envelope)


def test_an_addition_the_provider_left_out_is_never_read_as_taken_off(world, monkeypatch):
    """The adapter leaves out of its answer a track the provider would not add, and raises nothing.

    A base built from the additions the write asked for would read that track
    as taken off the account since, and take it out of rekordbox.
    """
    gig = world.folder("GIG READY")
    intro = world.playlist("Intro", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Intro")
    world.rekordbox_add(intro, "5", "6", "7")
    _reordered(world, intro, *LED)
    real_add = world.account.add_tracks

    def add_tracks(playlist_id, remote_ids):
        return real_add(playlist_id, tuple(one for one in remote_ids if one != "t6"))

    monkeypatch.setattr(world.account, "add_tracks", add_tracks)
    stops = _stopping(world, monkeypatch, account_id, 2)
    code, refused = sync()
    assert code != int(ExitCode.OK), refused
    assert stops == [2]
    assert "t6" not in world.account.playlists[account_id]
    monkeypatch.setattr(world.account, "add_tracks", real_add)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert "6" in world.held(intro), "a track the provider never added was taken out of rekordbox"
    # And the order is still finished from the side that led it (round one's review).
    assert world.held(intro) == list(LED), "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made(
    world, monkeypatch
):
    """Record both or neither: a base moved for the account alone loses its removal."""
    gig = world.folder("GIG READY")
    intro = world.playlist("Intro", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Intro")
    world.account.playlists[account_id].remove("t2")
    world.rekordbox_add(intro, "5", "6", "7")
    _reordered(world, intro, *LED)
    stops = _stopping(world, monkeypatch, account_id, 2)
    code, refused = sync(rekordbox="skip")
    assert code != int(ExitCode.OK), refused
    assert stops == [2]
    assert "2" in world.held(intro), "the skipped side was written"
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert "t2" not in world.account.playlists[account_id], "the account's removal was undone"
    assert world.held(intro) == ["4", "5", "1", "6", "7", "3"]
    assert world.account.playlists[account_id] == _ids("4", "5", "1", "6", "7", "3")


def test_a_later_run_that_failed_before_its_order_began_does_not_hide_the_stopped_write(
    world, stopped, monkeypatch
):
    """Round one's review: a run that began its account write and failed in its additions.

    Its steps are kept, since only a finished run lets them go, and it is the
    latest run to touch the account; it must not hide the write that stopped
    part way through its order.
    """
    from cratekit.modules.outbound import account as outbound_account

    intro, account_id, run_id = stopped
    world.rekordbox_add(intro, "8")
    real_add = world.account.add_tracks

    def failing(playlist_id, remote_ids):
        raise outbound_account.provider_failure(RuntimeError("timed out"), "add tracks")

    monkeypatch.setattr(world.account, "add_tracks", failing)
    code, refused = sync()
    assert code != int(ExitCode.OK), refused
    monkeypatch.setattr(world.account, "add_tracks", real_add)
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert f"finishes run {run_id}" in first["cause"]["detail"]["shown"][f"pair {account_id}"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == [*LED, "8"], "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == _ids(*LED, "8")
