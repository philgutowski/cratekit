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


# ═══════════════════════════════════════════════════════════════════════════
# R-1372: a stopped write is kept past the age a held plan is kept for
# ═══════════════════════════════════════════════════════════════════════════


def _aged(run_id: str, days: int = 31) -> None:
    """Date a run's held plan and steps ``days`` back, as that long without a sync leaves them.

    The round two review of U225 drove the finding this way: the producer,
    thirty days without a sync after a stop, is the files' time.
    """
    import os
    import time

    from cratekit.core import held_plan

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
    from cratekit.core import held_plan

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
    from cratekit.core import held_plan

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
    from cratekit.core import held_plan

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
    from cratekit.core import held_plan

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
    from cratekit.core import held_plan

    gig = world.folder("GIG READY")
    intro = world.playlist("Intro", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Intro")
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
    from cratekit.core import held_plan

    _intro, account_id, run_id = stopped
    code, envelope = sync(rekordbox="skip")
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids(*LED)
    # The stopped run is still kept, since no snapshot passed it; the finishing run is not.
    records, _problems = held_plan.carried()
    assert [one.run_id for one in records] == [run_id]
    assert envelope["run_id"] != run_id


# ═══════════════════════════════════════════════════════════════════════════
# R-1376: a pair released after a stopped order and paired again
# ═══════════════════════════════════════════════════════════════════════════


def _released(world, intro: str, account_id: str) -> str:
    """The stopped pair's rekordbox playlist deleted, a sync releasing it, and a new one in rekordbox's order.

    Answers the new rekordbox playlist, made at the root, where no sync of
    every pair discovers it, holding the stopped pair's tracks in the order
    rekordbox held them, as a person rebuilding the playlist would.
    """
    world.delete_rekordbox(intro)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.RELEASED in _codes(envelope)
    assert pairs.PairStore(world.cfg).get(account_id) is None
    # The release wrote nothing on the account: it still holds the scramble.
    assert world.account.playlists[account_id] == ["t2", "t7", "t1", "t3", "t4", "t5", "t6"]
    return world.playlist("Rebuilt", *LED)


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
    from cratekit.core import held_plan

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


def test_a_released_pair_reordered_on_the_account_since_is_paired_as_any_first_sync(
    world, stopped
):
    """A move off the stopped write's path is somebody's, so the account leads as on any first sync."""
    intro, account_id, run_id = stopped
    rebuilt = _released(world, intro, account_id)
    world.account.playlists[account_id] = _ids("7", "6", "5", "4", "3", "2", "1")
    paired = [*VERB, account_id, "--rekordbox", rebuilt]
    code, first = drive(paired)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    assert "finishes run" not in first["cause"]["detail"]["shown"][f"pair {account_id}"]
    code, envelope = sync(paired)
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.FINISHING not in _codes(envelope)
    assert world.held(rebuilt) == ["7", "6", "5", "4", "3", "2", "1"]


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
    # The first sync's account leads, as it always has.
    assert world.held(mine) == ["3", "1", "2"]
    assert world.account.playlists[theirs] == _ids("3", "1", "2")
