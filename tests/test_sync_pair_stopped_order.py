"""U225: a sync pair after a stopped order write finishes it from the leading side.

The stopped write's own moves are never read as a reorder, so its scramble
never reaches rekordbox; an account off the moves' path leads only once a
later sync read it in another order (U234). D1 applies.
"""

from __future__ import annotations

from datetime import timedelta

import pytest

from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs, tidal_account
from cratekit.sync import pair_cli, pair_stopped
from tests.cli_drive import drive
from tests.test_outbound_workers import _less_work as _less_work  # noqa: PLC0414
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import VERB, _codes, _said, plan_only, sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414
from tests.test_sync_pair_order import _reordered

#: Rekordbox's order after three tracks added and one moved, so rekordbox leads.
LED = ("4", "5", "1", "6", "2", "7", "3")


def _as_before_u231(monkeypatch) -> None:
    """Record each ordering step as v0.13.1 did, with no moving step (U234)."""
    real = pair_stopped.ordering_step

    def ordering_step(**kwargs):
        step = real(**kwargs)
        step.pop(pair_stopped.MOVES_RECORDED, None)
        return step

    monkeypatch.setattr(pair_stopped, "ordering_step", ordering_step)


def _stopping(world, monkeypatch, playlist_id: str, moves: int) -> list[int]:
    """Stop one playlist's order after ``moves`` adapter moves by a read back refusal (U220)."""
    _as_before_u231(monkeypatch)
    real = world.account.order_tracks
    stops: list[int] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id != playlist_id or len(stops) >= 1:
            return real(asked_id, remote_ids, expect=expect, begun=begun, **agreed)
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


def _synced(world, name: str, *content_ids: str) -> tuple[str, str]:
    """A GIG READY playlist of ``content_ids`` synced once: (rekordbox id, account id)."""
    made = world.playlist(name, *content_ids, under=world.folder("GIG READY"))
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    return made, world.titled(f"GIG READY {name}")


@pytest.fixture
def stopped(world, monkeypatch):
    """Synced on four, three added, stopped after two moves: (rekordbox, account, run)."""
    intro, account_id = _synced(world, "Intro", "1", "2", "3", "4")
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


def _agreeing_at_once(monkeypatch) -> None:
    """Two readings agree however close together, as if minutes had passed between runs (U234)."""
    from cratekit.sync import pair_plan
    monkeypatch.setattr(pair_plan, "AGREE_AFTER", timedelta(0))


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
    # U234. On the path, so the gate never says it read the account off it.
    assert "so its moves are not read as anybody's" in line, line
    assert "none of its moves leaves" not in line, line
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.FINISHING in _codes(envelope)
    assert "none of its moves leaves" not in _said(envelope, pair_cli.FINISHING)
    said = _said(envelope, pair_cli.FINISHING)
    assert run_id in said and "GIG READY Intro" in said


def test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads(
    world, stopped, monkeypatch
):
    """U234: settled readings off the path in two orders show the move; none on it is kept."""
    _agreeing_at_once(monkeypatch)
    intro, account_id, _run = stopped
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.stop_seen is None, "a reading on the path was kept"
    members = world.account.playlists[account_id]
    members.remove("t3")
    members.insert(0, "t3")
    plan_only()
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.stop_seen is not None and held.stop_seen.settled
    members.remove("t5")
    members.insert(0, "t5")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope), "one reading of the new order led"
    assert world.held(intro) == list(LED)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t5", "t3", "t2", "t7", "t1", "t4", "t6"]
    assert world.held(intro) == ["5", "3", "2", "7", "1", "4", "6"]
    assert "the account was reordered since syncs after the stop read it settled" in _said(
        envelope, pair_cli.FINISHING
    )


def test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons(world, stopped):
    """U234: one reading off the path may be the provider's partial state, so rekordbox leads."""
    intro, account_id, _run = stopped
    members = world.account.playlists[account_id]
    members.remove("t3")
    members.insert(0, "t3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED), "rekordbox took an order the reading alone led"
    assert world.account.playlists[account_id] == _ids(*LED)
    assert "none of its moves leaves" in _said(envelope, pair_cli.FINISHING)


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


def test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing(
    world, stopped
):
    """R-1420: a refusal with no moves recorded sent none (U231), so the next sync finishes it."""
    intro, account_id, run_id = stopped
    reached = list(world.account.playlists[account_id])
    code, refused = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["why"] for one in refused["cause"]["detail"]["moved"]] == [
        "was reordered since the plan"
    ]
    assert world.account.playlists[account_id] == reached
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids(*LED)
    assert world.held(intro) == list(LED)
    plan = plan_only()
    assert [item for item in plan["items"] if item["pair"] == account_id] == []
    code, first = drive(VERB)
    assert "finishes run" not in first["cause"]["detail"]["shown"][f"pair {account_id}"]


def test_a_stopped_write_that_skipped_rekordbox_still_finishes_its_order(world, monkeypatch):
    intro, account_id = _synced(world, "Intro", "1", "2", "3", "4")
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
    from cratekit.sync import held_plan

    assert held_plan.steps_path(run_id).exists()
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert pair_cli.FINISHING not in _codes(again)
    assert [item for item in again["data"]["items"] if item["pair"] == account_id] == []


def test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write(world, stopped):
    from cratekit.sync import held_plan

    held_plan.steps_path("2026-11-05T17:42:49Z-5ddd").write_text("{not json")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    said = _said(envelope, pair_cli.STOPPED_UNREAD)
    assert "2026-11-05T17:42:49Z-5ddd" in said
    # The record that can be read is still read.
    assert pair_cli.FINISHING in _codes(envelope)


def test_an_addition_the_provider_left_out_is_never_read_as_taken_off(world, monkeypatch):
    """A track the provider would not add is left out silently, never read as taken off."""
    intro, account_id = _synced(world, "Intro", "1", "2", "3", "4")
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
    # And the order is still finished from the side that led it.
    assert world.held(intro) == list(LED), "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made(
    world, monkeypatch
):
    """Record both or neither: a base moved for the account alone loses its removal."""
    intro, account_id = _synced(world, "Intro", "1", "2", "3", "4")
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
    """A later run that failed in its additions keeps its steps but hides no stopped write."""
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


# R-1372: a stopped write is kept past the age a held plan is kept for


def _aged(run_id: str, days: int = 31) -> None:
    """Date a run's held plan and steps ``days`` back, as that long without a sync leaves them."""
    import os
    import time

    from cratekit.sync import held_plan

    then = time.time() - days * 86400
    for where in (held_plan.path(run_id), held_plan.steps_path(run_id)):
        if where.exists():
            os.utime(where, (then, then))


def test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led(
    world, stopped
):
    intro, account_id, run_id = stopped
    _aged(run_id)
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the plan writes rekordbox the scramble of a write stopped more than thirty days ago"
    )
    assert [item["action"] for item in pair if item["side"] == "account"] == ["order"]
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert f"finishes run {run_id}" in first["cause"]["detail"]["shown"][f"pair {account_id}"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED), "rekordbox took an order nobody chose"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished(world, stopped):
    """A later run's hold prunes the aged plan and steps, and the stop is still read."""
    from cratekit.sync import held_plan

    intro, account_id, run_id = stopped
    _aged(run_id)
    held_plan.prune()
    assert not held_plan.steps_path(run_id).exists()
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED), "rekordbox took an order nobody chose"
    assert world.account.playlists[account_id] == _ids(*LED)
    assert run_id in _said(envelope, pair_cli.FINISHING)


def test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it(
    world, stopped
):
    """The run plans again, its gates refuse the new plan stale, and a fresh sync then finishes it."""
    intro, account_id, run_id = stopped
    _aged(run_id)
    code, refused = drive(["--run", run_id, *VERB])
    assert code != int(ExitCode.OK), refused
    assert world.account.playlists[account_id] == ["t2", "t7", "t1", "t3", "t4", "t5", "t6"]
    assert world.held(intro) == list(LED)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED), "rekordbox took an order nobody chose"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go(world, stopped):
    from cratekit.sync import held_plan

    _intro, account_id, run_id = stopped
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    # The snapshot moved past the stop, so nothing of it is kept past its run.
    records, problems = held_plan.carried()
    assert problems == []
    assert [one.run_id for one in records] == [], "a stop the snapshot passed is still kept"
    _aged(run_id)
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert pair_cli.FINISHING not in _codes(again)
    assert [item for item in again["data"]["items"] if item["pair"] == account_id] == []


def test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk(
    world, stopped
):
    """A record the snapshot passed and that was never let go, read by a later plan."""
    from cratekit.sync import held_plan

    _intro, account_id, run_id = stopped
    kept = {one: one.read_bytes() for one in held_plan.carried_dir().glob("*.json")}
    assert kept, "the stop was not kept past its run"
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    for where, payload in kept.items():
        where.write_bytes(payload)
    _aged(run_id)
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert pair_cli.FINISHING not in _codes(again)
    assert [item for item in again["data"]["items"] if item["pair"] == account_id] == []


def test_a_kept_stop_that_cannot_be_read_is_named(world, stopped):
    from cratekit.sync import held_plan

    _intro, _account_id, run_id = stopped
    _aged(run_id)
    held_plan.prune()
    for one in held_plan.carried_dir().glob("*.json"):
        one.write_text("{not json")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert run_id in _said(envelope, pair_cli.STOPPED_UNREAD)


def test_a_stop_that_cannot_be_kept_past_its_run_moves_nothing(world, monkeypatch):
    """The record is kept before the first move, so a write that cannot keep it stops first."""
    from cratekit.sync import held_plan

    intro, account_id = _synced(world, "Intro", "1", "2", "3", "4")
    world.rekordbox_add(intro, "5", "6", "7")
    _reordered(world, intro, *LED)

    def refused(steps, key):
        raise PermissionError("read only")

    monkeypatch.setattr(held_plan, "carry", refused)
    code, envelope = sync()
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == pair_cli.STEPS_UNWRITTEN, envelope["cause"]
    # The additions landed and not one track was moved.
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4", "5", "6", "7")


def test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own(
    world, stopped
):
    """Its own carried record is let go when the pair is done, whatever the snapshot did."""
    from cratekit.sync import held_plan

    _intro, account_id, run_id = stopped
    code, envelope = sync(rekordbox="skip")
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids(*LED)
    # The stopped run is still kept, since no snapshot passed it; the finishing run is not.
    records, _problems = held_plan.carried()
    assert [one.run_id for one in records] == [run_id]
    assert envelope["run_id"] != run_id


# R-1376: a pair released after a stopped order and paired again


def _released(world, intro: str, account_id: str, *, root: bool = False) -> str:
    """The stopped pair released and a new one made, its account order kept in GIG READY (U231)."""
    world.delete_rekordbox(intro)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.RELEASED in _codes(envelope)
    assert pairs.PairStore(world.cfg).get(account_id) is None
    # The release wrote nothing on the account: it still holds the scramble.
    assert world.account.playlists[account_id] == ["t2", "t7", "t1", "t3", "t4", "t5", "t6"]
    if root:
        return world.playlist("Rebuilt", *LED)
    [(gig,)] = world.sql(
        "SELECT ID FROM djmdPlaylist WHERE Name = ? AND Attribute = 1 "
        "AND COALESCE(rb_local_deleted, 0) = 0",
        "GIG READY",
    )
    return world.playlist("Rebuilt", *LED, under=str(gig))


def test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble(
    world, stopped
):
    intro, account_id, run_id = stopped
    rebuilt = _released(world, intro, account_id)
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    code, first = drive(paired)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert f"finishes run {run_id}" in line, line
    assert "order follows rekordbox's" in line, line
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert world.held(rebuilt) == list(LED), "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == _ids(*LED)
    assert run_id in _said(envelope, pair_cli.FINISHING)
    # Finished, the stop is let go and the next sync plans nothing.
    code, again = sync()
    assert code == int(ExitCode.OK), again
    assert pair_cli.FINISHING not in _codes(again)
    assert [item for item in again["data"]["items"] if item["pair"] == account_id] == []


def test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble(
    world, stopped
):
    """Only the carried record is left, and it outlives the release."""
    from cratekit.sync import held_plan

    intro, account_id, run_id = stopped
    rebuilt = _released(world, intro, account_id)
    _aged(run_id)
    held_plan.prune()
    assert not held_plan.steps_path(run_id).exists()
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    plan = plan_only(paired)
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the first sync writes rekordbox the stopped write's scramble"
    )
    assert [item["action"] for item in pair if item["side"] == "account"] == ["order"]
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert world.held(rebuilt) == list(LED), "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == _ids(*LED)
    # The new pair's snapshot passed the stop, so it is let go.
    records, problems = held_plan.carried()
    assert problems == []
    assert run_id not in [one.run_id for one in records], "a stop the new pair finished is kept"


def test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble(
    world, stopped
):
    """Marked with no snapshot, the pair's next sync is still a first one, and the stop predates the mark."""
    intro, account_id, run_id = stopped
    rebuilt = _released(world, intro, account_id)
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    code, envelope = sync(paired, account="skip")
    assert code == int(ExitCode.OK), envelope
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.first, "the skipped account left a snapshot"
    assert world.held(rebuilt) == list(LED)
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert f"finishes run {run_id}" in line, line
    # Still a first sync, with no base built from a snapshot it never took.
    assert "first sync, additions only" in line, line
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(rebuilt) == list(LED), "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order(
    world, stopped
):
    """U234: a hand pairing has no reading kept, so rekordbox's order stands off the path."""
    intro, account_id, run_id = stopped
    rebuilt = _released(world, intro, account_id)
    world.account.playlists[account_id] = _ids("7", "6", "5", "4", "3", "2", "1")
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    code, first = drive(paired)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert f"finishes run {run_id}" in line and "none of its moves leaves" in line, line
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.FINISHING in _codes(envelope)
    assert world.held(rebuilt) == list(LED), "the rebuilt playlist took an order nobody chose"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before(world):
    gig = world.folder("GIG READY")
    world.playlist("Intro", "1", "2", "3", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    theirs = world.account.create_playlist("Theirs")
    world.account.playlists[theirs] = _ids("3", "1", "2")
    mine = world.playlist("Mine", "1", "2", "3")
    paired = [*VERB, theirs, "--rekordbox", mine]
    code, first = drive(paired)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert "finishes run" not in first["cause"]["detail"]["shown"][f"pair {theirs}"]
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.FINISHING not in _codes(envelope)
    # R-1416, CHANGED BY PHILLIP'S DECISION on #608, not weakened: a root pair's
    # account order is not kept (U231), so rekordbox keeps its order.
    assert world.held(mine) == ["1", "2", "3"]
    assert world.account.playlists[theirs] == _ids("3", "1", "2")


def test_a_first_sync_of_an_account_playlist_with_no_stop_under_gig_ready_follows_the_account(
    world,
):
    """R-1416 leaves a pair whose account order is kept as it was: the account leads its first sync."""
    gig = world.folder("GIG READY")
    world.playlist("Intro", "1", "2", "3", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    theirs = world.account.create_playlist("Theirs")
    world.account.playlists[theirs] = _ids("3", "1", "2")
    mine = world.playlist("Mine", "1", "2", "3", under=gig)
    paired = [*VERB, theirs, "--rekordbox", mine]
    code, first = drive(paired)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert "order follows the account's" in first["cause"]["detail"]["shown"][f"pair {theirs}"]
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert world.held(mine) == ["3", "1", "2"]
    assert world.account.playlists[theirs] == _ids("3", "1", "2")


def test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync(
    world, stopped
):
    """Outside GIG READY the account's order is left as it is (U231), and rekordbox keeps its own."""
    intro, account_id, run_id = stopped
    rebuilt = _released(world, intro, account_id, root=True)
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    code, first = drive(paired)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert f"finishes run {run_id}" in line, line
    assert "order follows rekordbox's" in line, line
    assert "kept only for pairs under GIG READY" in line, line
    pair = [item for item in plan_only(paired)["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the first sync writes rekordbox the stopped write's scramble"
    )
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert world.held(rebuilt) == list(LED), "rekordbox took the stopped write's scramble"
    assert world.account.playlists[account_id] == ["t2", "t7", "t1", "t3", "t4", "t5", "t6"]
    assert run_id in _said(envelope, pair_cli.FINISHING)
    # R-1404. Every later sync keeps rekordbox's order, named alone or with every pair.
    for again in (paired, VERB):
        code, envelope = sync(again)
        assert code == int(ExitCode.OK), envelope
        assert world.held(rebuilt) == list(LED), "a later sync wrote the scramble into rekordbox"
    assert world.account.playlists[account_id] == ["t2", "t7", "t1", "t3", "t4", "t5", "t6"]


def test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it(
    world, cfg
):
    """A pending order (U231) read by a first sync by hand holds the pair, never finishing from a lagging read."""
    from tests.test_sync_pair_order import _reordered

    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Opener")
    _reordered(world, opener, "4", "3", "1", "2")
    world.account.served[account_id] = _ids("1", "2", "3", "4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.PENDING in _codes(envelope)
    world.delete_rekordbox(opener)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.RELEASED in _codes(envelope)
    assert pairs.PairStore(cfg).get(account_id) is None
    rebuilt = world.playlist("Rebuilt", "4", "3", "1", "2", under=gig)
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    # The provider still serves the order the moves began from: held, twice.
    for _ in range(2):
        code, envelope = sync(paired)
        assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
        assert envelope["cause"]["detail"]["problem"] == "order-pending", envelope
        assert world.held(rebuilt) == ["4", "3", "1", "2"]
        assert pairs.PairStore(cfg).get(account_id) is None
    # Served as the moves leave it, the first sync finishes the order.
    del world.account.served[account_id]
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.FINISHING in _codes(envelope)
    assert world.held(rebuilt) == ["4", "3", "1", "2"]
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
# U234. An account the stop left off its moves' path is not read as a reorder

#: Seven tracks reversed, so the adapter's moves front t2 to t7 in turn.
BACK = ("7", "6", "5", "4", "3", "2", "1")
#: The account as a stop left it after a move answered 412 but landed and was
#: sent again; no count of the adapter's moves leaves it.
LEFT = ("4", "1", "3", "2", "5", "6", "7")


def _left_off_the_path(world, monkeypatch, playlist_id: str) -> list[int]:
    """Stop the order on one playlist with the account at :data:`LEFT`, recorded as before U231."""
    _as_before_u231(monkeypatch)
    real = world.account.order_tracks
    stops: list[int] = []

    def order_tracks(asked_id, remote_ids, *, expect=None, begun=None, **agreed):
        if asked_id != playlist_id or stops:
            return real(asked_id, remote_ids, expect=expect, begun=begun, **agreed)
        world.account.playlists[asked_id][:] = _ids(*LEFT)
        stops.append(len(stops))
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
def strayed(world, monkeypatch):
    """A GIG READY pair of seven reversed, stopped off the path: (rekordbox, account, run)."""
    closer, account_id = _synced(world, "Closer", "1", "2", "3", "4", "5", "6", "7")
    _reordered(world, closer, *BACK)
    stops = _left_off_the_path(world, monkeypatch, account_id)
    code, refused = sync()
    assert code != int(ExitCode.OK), refused
    assert stops, "the order never ran"
    assert world.account.playlists[account_id] == _ids(*LEFT)
    assert world.held(closer) == list(BACK)
    return closer, account_id, refused["run_id"]


def test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox(world, strayed):
    """No rekordbox order from the half done account order, and the account is put back."""
    closer, account_id, _run = strayed
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == [], (
        "the plan writes rekordbox the stopped write's half done order"
    )
    assert [item["action"] for item in pair if item["side"] == "account"] == ["order"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == list(BACK), "rekordbox took an order nobody chose"
    assert world.account.playlists[account_id] == _ids(*BACK)
    # Sent again from the reading the plan judged, and held to it.
    assert (account_id, tuple(_ids(*LEFT))) in world.account.agreed
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids(*BACK))
    assert held.stop_seen is None, "the snapshot moved and kept the stop's reading"


def test_the_gate_says_the_account_was_read_off_the_moves_path(world, strayed):
    _closer, account_id, run_id = strayed
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert f"finishes run {run_id}" in line
    assert "none of its moves leaves" in line, line
    assert "read as yours" not in line, line
    assert "order follows rekordbox's" in line
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    said = _said(envelope, pair_cli.FINISHING)
    assert run_id in said and "none of its moves leaves" in said, said


def test_an_account_left_off_its_path_outside_gig_ready_leaves_rekordbox_untouched(
    world, strayed
):
    """Moved out of GIG READY since the stop: rekordbox keeps its order, the account is left (R-1404)."""
    closer, account_id, _run = strayed
    world.sql("UPDATE djmdPlaylist SET ParentID = 'root' WHERE ID = ?", closer)
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert pair == [], pair
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == list(BACK), "rekordbox took the half done order"
    assert world.account.playlists[account_id] == _ids(*LEFT)


def test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads(
    world, strayed, monkeypatch
):
    """The person moved the account after syncs read it settled, so the new settled order is theirs."""
    _agreeing_at_once(monkeypatch)
    closer, account_id, run_id = strayed
    plan_only()
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.stop_seen == pairs.StopReading(
        run_id, tuple(_ids(*LEFT)), held.stop_seen.at, settled=True
    )
    members = world.account.playlists[account_id]
    members.remove("t6")
    members.insert(0, "t6")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    assert "changed since a sync read it settled" in _said(envelope, pair_cli.LEFT_OUT)
    # R-1434: a reorder of tracks the plan reads is promised the lead it then takes.
    assert "when the account's order is read as yours" in _said(envelope, pair_cli.LEFT_OUT)
    assert world.held(closer) == list(BACK)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t6", "t4", "t1", "t3", "t2", "t5", "t7"]
    assert world.held(closer) == ["6", "4", "1", "3", "2", "5", "7"]
    assert "reordered since syncs after the stop read it settled" in _said(
        envelope, pair_cli.FINISHING
    )


def test_a_kept_reading_that_never_settled_shows_no_reorder(world, strayed):
    """The provider moving between two plans is not the person: a lag on the path is not kept."""
    closer, account_id, _run = strayed
    world.account.served[account_id] = _ids("1", "2", "3", "4", "5", "6", "7")
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.stop_seen is None
    del world.account.served[account_id]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == list(BACK), "rekordbox took the half done order"
    assert world.account.playlists[account_id] == _ids(*BACK)


def test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes(
    world, strayed, monkeypatch
):
    """An order on the path read steadily may be a lag; the partial state after it is finished."""
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    for served in (("2", "1", "3", "4", "5", "6", "7"), ("1", "2", "3", "4", "5", "6", "7")):
        world.account.served[account_id] = _ids(*served)
        plan_only()
        plan_only()
        held = pairs.PairStore(world.cfg).get(account_id)
        assert held is not None and held.stop_seen is None, served
    del world.account.served[account_id]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT not in _codes(envelope)
    assert world.held(closer) == list(BACK), "rekordbox took the half done order"
    assert world.account.playlists[account_id] == _ids(*BACK)


def test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between(
    world, strayed, monkeypatch
):
    """B, then the settled order, then B again holds B anew, never on B's first clock."""
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    plan_only()
    plan_only()
    after = _ids("6", "4", "1", "3", "2", "5", "7")
    world.account.served[account_id] = after
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope)
    for between in (_ids(*LEFT), _ids("2", "1", "3", "4", "5", "6", "7")):
        world.account.served[account_id] = between
        plan_only()
        held = pairs.PairStore(world.cfg).get(account_id)
        assert held is not None and held.stop_seen.after is None, between
        world.account.served[account_id] = after
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope), "the order after led on its old clock"
    assert world.held(closer) == list(BACK)


def test_a_differing_order_that_moves_again_before_it_settles_is_held_again(
    world, strayed, monkeypatch
):
    """The order after a settled one leads only once two readings of it agree."""
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    plan_only()
    plan_only()
    for served in (("6", "4", "1", "3", "2", "5", "7"), ("5", "4", "1", "3", "2", "6", "7")):
        world.account.served[account_id] = _ids(*served)
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope), served
    assert world.held(closer) == list(BACK)
    # The order it moved to is the one waited on: read again, it leads.
    world.account.playlists[account_id][:] = _ids("5", "4", "1", "3", "2", "6", "7")
    del world.account.served[account_id]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == ["5", "4", "1", "3", "2", "6", "7"]


def test_a_reading_that_moved_before_it_settled_starts_again(world, strayed, monkeypatch):
    """Another partial state then this one: the second reading is kept afresh, never settled as the first."""
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    world.account.served[account_id] = _ids("1", "3", "2", "4", "5", "6", "7")
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.stop_seen.order == tuple(_ids("1", "3", "2", "4", "5", "6", "7"))
    del world.account.served[account_id]
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and held.stop_seen.order == tuple(_ids(*LEFT))
    assert not held.stop_seen.settled
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT not in _codes(envelope), "the partial state was held as a reorder"
    assert world.held(closer) == list(BACK)
    assert world.account.playlists[account_id] == _ids(*BACK)


def test_a_differing_order_waits_the_agreement_window(world, strayed, monkeypatch):
    """With the window kept, a settled reading and one new reading agree with nothing yet."""
    from cratekit.sync import pair_plan
    closer, account_id, _run = strayed
    plan_only()
    plan_only()
    held = pairs.PairStore(world.cfg).get(account_id)
    assert held is not None and not held.stop_seen.settled, "settled inside the window"
    _agreeing_at_once(monkeypatch)
    plan_only()
    monkeypatch.setattr(pair_plan, "AGREE_AFTER", timedelta(minutes=5))
    world.account.served[account_id] = _ids("6", "4", "1", "3", "2", "5", "7")
    for _ in range(2):
        code, envelope = sync()
        assert code == int(ExitCode.OK), envelope
        assert pair_cli.LEFT_OUT in _codes(envelope)
    assert world.held(closer) == list(BACK)


def test_two_syncs_reading_the_same_order_off_the_path_are_no_reorder(
    world, strayed, monkeypatch
):
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    plan_only()
    plan = plan_only()
    pair = [item for item in plan["items"] if item["pair"] == account_id]
    assert [item for item in pair if item["side"] == "rekordbox"] == []
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == list(BACK)
    assert world.account.playlists[account_id] == _ids(*BACK)


def test_a_reading_kept_for_another_run_shows_no_reorder(world, strayed, monkeypatch):
    """A reading is evidence only for the stop it was read after (identity, not order alone)."""
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    pairs.PairStore(world.cfg).see_stop(
        account_id,
        pairs.StopReading(
            "another-run",
            tuple(_ids(*BACK)),
            "2099-01-01T00:00:00+00:00",
            settled=True,
            after=tuple(_ids(*LEFT)),
            after_at="2099-01-01T00:00:00+00:00",
        ),
    )
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == list(BACK)
    assert world.account.playlists[account_id] == _ids(*BACK)


def test_a_reading_kept_before_the_stop_shows_no_reorder(world, strayed, monkeypatch):
    _agreeing_at_once(monkeypatch)
    closer, account_id, run_id = strayed
    pairs.PairStore(world.cfg).see_stop(
        account_id,
        pairs.StopReading(
            run_id,
            tuple(_ids(*BACK)),
            "2000-01-01T00:00:00+00:00",
            settled=True,
            after=tuple(_ids(*LEFT)),
            after_at="2000-01-01T00:00:00+00:00",
        ),
    )
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == list(BACK)
    assert world.account.playlists[account_id] == _ids(*BACK)


def test_a_track_added_on_the_account_between_two_readings_is_no_reorder(
    world, strayed, monkeypatch
):
    _agreeing_at_once(monkeypatch)
    closer, account_id, _run = strayed
    plan_only()
    plan_only()
    world.account.playlists[account_id].insert(3, "t8")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT not in _codes(envelope)
    assert "reordered since" not in str(envelope)
    assert [one for one in world.held(closer) if one != "8"] == list(BACK)


def test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder(
    world, stopped, monkeypatch
):
    """U234: only an order off the path is compared with the kept reading; on it, the stop finishes."""
    _agreeing_at_once(monkeypatch)
    intro, account_id, _run = stopped
    plan_only()
    plan_only()
    # One more of the write's own moves shows: still on its path, in another order.
    members = world.account.playlists[account_id]
    members.remove("t6")
    members.insert(0, "t6")
    assert members == ["t6", "t2", "t7", "t1", "t3", "t4", "t5"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(intro) == list(LED), "rekordbox took a point on the stopped write's path"
    assert world.account.playlists[account_id] == _ids(*LED)


def test_a_stop_this_version_recorded_with_no_move_sent_leaves_a_reorder_the_persons(
    world, monkeypatch
):
    """U234 keeps R-1420: an order refused before any move sent nothing, so the account leads."""
    closer, account_id = _synced(world, "Closer", "1", "2", "3", "4")
    _reordered(world, closer, "4", "3", "1", "2")
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
    assert refused and world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    line = first["cause"]["detail"]["shown"][f"pair {account_id}"]
    assert "none of its moves was sent" in line and "none of its moves leaves" not in line, line
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(closer) == ["2", "4", "1", "3"]
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3")
