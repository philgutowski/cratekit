"""U220: a pair whose account order is refused stops alone, and a continue of the run finishes it.

Sitting 62's live ``crate sync pair`` added six tracks to one paired playlist
and then its order was refused; the refusal stopped the whole write, so it
never reached the other 101 pairs nor the rekordbox side of a playlist the
account had made. Driven through the dispatcher on the disposable database
and the fake account the discovery suite builds: one pair's order refuses,
every other pair and the playlist brought into rekordbox are still written,
the stop names the pair and the run, and a continue of the run puts it in
order, passing the adapter the check's own listing to agree with first.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import pytest

from cratekit.core.cause import Remedy, Scope, refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_back import in_rekordbox, on_account
from tests.test_sync_pair_discover import VERB, sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414


def _reordered(world, playlist_id: str, *content_ids: str) -> None:
    """Put a rekordbox playlist's memberships in this order, as a person dragging them would."""
    for number, content_id in enumerate(content_ids, start=1):
        world.sql(
            "UPDATE djmdSongPlaylist SET TrackNo = ? WHERE PlaylistID = ? AND ContentID = ?",
            number,
            playlist_id,
            content_id,
        )


def _refusing(world, monkeypatch, refused_on: set[str], *, reason: str = "outbound-remove-refused"):
    """Make the account's order refuse on the named playlists, as the live adapter refused."""
    real = world.account.order_tracks

    def order_tracks(playlist_id, remote_ids, *, expect=None, begun=None, **agreed):
        if playlist_id in refused_on:
            world.account.expected.append((playlist_id, expect))
            if reason == "credential-missing":
                raise refuse(
                    reason,
                    "the streaming provider rejected the session",
                    remedy=Remedy.REAUTHENTICATE_PROVIDER,
                    scope=Scope.ITEM,
                    origin=("test", "order"),
                )
            raise refuse(
                reason,
                f"the playlist {playlist_id} read back after a move is not what it held "
                f"with that track moved to the front, so nothing more was moved",
                scope=Scope.RUN,
                origin=("test", "order"),
                detail={"playlist_id": playlist_id, "problem": "read-back-differs"},
            )
        return real(playlist_id, remote_ids, expect=expect, begun=begun, **agreed)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)


@pytest.fixture
def owed(world):
    """Two pairs synced once in GIG READY, then changed so each owes the account a write.

    Opener is reordered in rekordbox, so its account side owes an order;
    Second gains a track in rekordbox, so its account side owes an addition;
    and a playlist made on the account in the synced folder owes rekordbox a
    new playlist.
    """
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", under=gig)
    second = world.playlist("Second", "4", "5", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "3", "1", "2")
    world.rekordbox_add(second, "6")
    on_account(world, "GIG READY Closer", "GIG READY", "t7", "t8")
    return gig, opener, second


def test_a_refused_order_stops_its_pair_alone_and_every_other_write_lands(
    world, owed, cfg, monkeypatch
):
    gig, opener, _second = owed
    opener_account = world.titled("GIG READY Opener")
    second_account = world.titled("GIG READY Second")
    _refusing(world, monkeypatch, {opener_account})

    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    # Every other write landed: the other pair's addition and the playlist
    # brought into rekordbox.
    assert world.account.playlists[second_account] == ["t4", "t5", "t6"]
    inside = in_rekordbox(world, gig)
    assert "Closer" in inside and world.held(inside["Closer"]) == ["7", "8"]
    # The refused pair's tracks are all still there, its order not done.
    assert world.account.playlists[opener_account] == ["t1", "t2", "t3"]
    assert world.held(opener) == ["3", "1", "2"]
    # Its snapshot did not move, so the next sync still reads the order as owed.
    held = pairs.PairStore(cfg).get(opener_account)
    assert held is not None and held.account == ("t1", "t2", "t3")
    # The stop says which pair did not finish, how far the run got, and how to go on.
    cause = stopped["cause"]
    assert cause["reason"] == "outbound-remove-refused"
    run_id = stopped["run_id"]
    assert [one["account_id"] for one in cause["detail"]["unordered"]] == [opener_account]
    assert cause["detail"]["finished"] == 2
    assert "GIG READY Opener" in cause["message"]
    assert f"crate --run {run_id} sync pair" in cause["message"]


def test_a_continue_of_the_run_puts_the_refused_pair_in_order_and_moves_nothing_else(
    world, owed, cfg, monkeypatch
):
    _gig, opener, _second = owed
    opener_account = world.titled("GIG READY Opener")
    refused_on = {opener_account}
    _refusing(world, monkeypatch, refused_on)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    run_id = stopped["run_id"]
    added = list(world.account.added)

    refused_on.clear()
    code, done = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.playlists[opener_account] == ["t3", "t1", "t2"]
    assert world.held(opener) == ["3", "1", "2"]
    assert world.account.added == added, "a continue added a track a second time"
    # The continue handed the adapter the check's own listing to agree with
    # before its first move, since this run had seen the order refused.
    assert world.account.expected[-1] == (opener_account, ("t1", "t2", "t3"))
    assert done["data"]["totals"]["finished_before"] == 2
    held = pairs.PairStore(cfg).get(opener_account)
    assert held is not None and held.account == ("t3", "t1", "t2")


def test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote(
    world, owed
):
    opener_account = world.titled("GIG READY Opener")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[opener_account] == ["t3", "t1", "t2"]
    assert world.account.expected == [(opener_account, None)]


def test_a_rejected_session_on_the_order_still_stops_the_whole_write(world, owed, monkeypatch):
    opener_account = world.titled("GIG READY Opener")
    _refusing(world, monkeypatch, {opener_account}, reason="credential-missing")
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert stopped["cause"]["reason"] == "credential-missing"
    assert "unordered" not in (stopped["cause"].get("detail") or {})


def test_the_order_refusals_that_stop_one_pair_are_the_two_an_order_raises():
    assert pair_cli.ORDER_REFUSALS == {"outbound-remove-refused", "unavailable-transient"}


def test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved(
    world, owed, monkeypatch
):
    """U220's round two, read again by R-1420: a change under a refusal that no record names.

    U220 passed the continue its own listing to agree with, so a move that
    landed somewhere the read back did not expect was ordered from. Since
    U231 the adapter records its moves before the first is sent, and this
    fake changes the playlist without telling ``begun``: a refusal with no
    moves recorded sent none, so the change is someone else's, and the
    continue holds it as moved with nothing written. A fresh sync then
    takes the account's order as the person's.
    """
    _gig, opener, _second = owed
    opener_account = world.titled("GIG READY Opener")
    refused_on = {opener_account}
    real = world.account.order_tracks

    def order_tracks(playlist_id, remote_ids, *, expect=None, begun=None, **agreed):
        if playlist_id in refused_on:
            world.account.expected.append((playlist_id, expect))
            world.account.playlists[playlist_id][:] = ["t1", "t3", "t2"]
            raise refuse(
                "outbound-remove-refused",
                "read back after a move is not what it held",
                scope=Scope.RUN,
                origin=("test", "order"),
                detail={"playlist_id": playlist_id, "problem": "read-back-differs"},
            )
        return real(playlist_id, remote_ids, expect=expect, begun=begun, **agreed)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    refused_on.clear()
    asked = len(world.account.expected)
    code, refused = drive(["--run", stopped["run_id"], *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert len(world.account.expected) == asked, "the continue asked the account an order"
    assert world.account.playlists[opener_account] == ["t1", "t3", "t2"]
    assert world.held(opener) == ["3", "1", "2"]


def test_the_stop_carries_every_unfinished_pairs_steps_once():
    """Round two: the stop asks the person to do what each refusal asks, so it shows each."""
    def cause(steps):
        return refuse(
            "outbound-remove-refused",
            "refused",
            steps=steps,
            scope=Scope.RUN,
            origin=("test", "order"),
        ).cause

    unordered = [
        pair_cli.Done(account_id="a", name="A", order_refused=cause(("look at A",))),
        pair_cli.Done(account_id="b", name="B", order_refused=cause(("look at B", "look at A"))),
    ]
    said = pair_cli._unordered(unordered, None, None, run_id="r", argv=None)
    assert said.remediation.steps == ("look at A", "look at B")
    assert said.detail["fresh"] is True
    assert [one["account_id"] for one in said.detail["unordered"]] == ["a", "b"]
    assert "run crate sync pair again" in said.message


# ═══════════════════════════════════════════════════════════════════════════
# R-1420: a continue of a refused order writes nothing over a person's reorder
# ═══════════════════════════════════════════════════════════════════════════


def _ids(*content_ids: str) -> list[str]:
    return [f"t{one}" for one in content_ids]


@pytest.fixture
def refused_once(world, monkeypatch):
    """One pair in GIG READY reordered in rekordbox to 4, 3, 1, 2, its account order refused once.

    The order is refused before any move is sent, as the adapter refuses a
    reading it would not trust, so the account still stands as the plan
    read it. Answers rekordbox's playlist, the account's, the refused run and
    the set of playlists still refusing, emptied.
    """
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "4", "3", "1", "2")
    account_id = world.titled("GIG READY Opener")
    refused_on = {account_id}
    _refusing(world, monkeypatch, refused_on)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert stopped["cause"]["reason"] == "outbound-remove-refused", stopped
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    refused_on.clear()
    return opener, account_id, stopped["run_id"]


def test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since(
    world, refused_once, cfg
):
    """R-1420: the person's 2, 4, 1, 3 passed the check and was written over with 4, 3, 1, 2."""
    opener, account_id, run_id = refused_once
    # The person reorders the playlist on the account between the two commands.
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    ordered = list(world.account.ordered)

    code, refused = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["detail"]["moved"] == [
        {
            "side": "account",
            "playlist_id": account_id,
            "name": "GIG READY Opener",
            "why": "was reordered since the plan",
        }
    ]
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3"), (
        "the continue wrote over the person's reorder"
    )
    assert world.account.ordered == ordered, "the continue asked the account an order"
    assert world.held(opener) == ["4", "3", "1", "2"], "rekordbox was written"
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("1", "2", "3", "4"))

    # A fresh sync merges the person's order as a fresh sync does.
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3")
    assert world.held(opener) == ["2", "4", "1", "3"]


def test_a_fresh_sync_over_the_same_two_reorders_takes_the_accounts_order(world, cfg):
    """What the continue now leaves to: the merge a fresh sync makes of both reorders."""
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    account_id = world.titled("GIG READY Opener")
    _reordered(world, opener, "4", "3", "1", "2")
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3")
    assert world.held(opener) == ["2", "4", "1", "3"]


def test_a_continue_of_a_refused_order_the_account_still_stands_in_finishes_it(
    world, refused_once, cfg
):
    opener, account_id, run_id = refused_once
    code, done = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2"]
    assert world.account.expected[-1] == (account_id, tuple(_ids("1", "2", "3", "4")))
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == tuple(_ids("4", "3", "1", "2"))


def _refused_with_an_addition(world, monkeypatch):
    """The 4, 3, 1, 2 reorder and track 5 added in rekordbox, the addition landed, the order refused."""
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "4", "3", "1", "2")
    world.rekordbox_add(opener, "5")
    account_id = world.titled("GIG READY Opener")
    refused_on = {account_id}
    _refusing(world, monkeypatch, refused_on)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4", "5")
    refused_on.clear()
    return opener, account_id, stopped["run_id"]


def test_a_continue_of_a_refused_order_that_also_added_finishes_it(world, cfg, monkeypatch):
    opener, account_id, run_id = _refused_with_an_addition(world, monkeypatch)
    added = list(world.account.added)
    code, done = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2", "5")
    assert world.held(opener) == ["4", "3", "1", "2", "5"]
    assert world.account.added == added, "a continue added a track a second time"


def test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since(
    world, cfg, monkeypatch
):
    opener, account_id, run_id = _refused_with_an_addition(world, monkeypatch)
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3", "5")
    ordered = list(world.account.ordered)
    code, refused = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["why"] for one in refused["cause"]["detail"]["moved"]] == [
        "was reordered since the plan"
    ]
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3", "5")
    assert world.account.ordered == ordered
    assert world.held(opener) == ["4", "3", "1", "2", "5"]


@pytest.mark.parametrize("stop", ["credential-missing", "parked"])
def test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since(
    world, cfg, monkeypatch, stop
):
    """R-1420, one step over: an order stopped before ``begun`` by a stop that is no order refusal.

    A rejected session stops the whole write and a cooldown parks it, each
    after the order was marked begun and before any move was sent, so the
    run carries ``ordering`` and no ``order-refused``. The person's reorder
    on the account before the continue is held as moved all the same.
    """
    from cratekit.core import jobs

    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "4", "3", "1", "2")
    account_id = world.titled("GIG READY Opener")
    real = world.account.order_tracks
    stopping = [True]

    def order_tracks(playlist_id, remote_ids, *, expect=None, begun=None, **agreed):
        if playlist_id == account_id and stopping:
            stopping.clear()
            if stop == "parked":
                raise jobs.Parked(
                    refuse(
                        "provider-cooldown", "a cooldown", scope=Scope.RUN, origin=("test", "order")
                    ).cause
                )
            raise refuse(
                "credential-missing",
                "the streaming provider rejected the session",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
                scope=Scope.ITEM,
                origin=("test", "order"),
            )
        return real(playlist_id, remote_ids, expect=expect, begun=begun, **agreed)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    assert world.account.playlists[account_id] == _ids("1", "2", "3", "4")
    world.account.playlists[account_id][:] = _ids("2", "4", "1", "3")
    code, refused = drive(["--run", stopped["run_id"], *VERB])
    assert world.account.playlists[account_id] == _ids("2", "4", "1", "3"), (
        "the continue wrote over the person's reorder"
    )
    assert code == int(ExitCode.DECISION_STALE), refused
    assert world.held(opener) == ["4", "3", "1", "2"]


@pytest.mark.parametrize("stop", ["credential-missing", "parked", "refused"])
def test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing(
    world, cfg, monkeypatch, stop
):
    """Round one's row 2: whatever stopped the order before any move, the continue agrees first.

    A refused order's continue passed the check's listing as ``expect``;
    one parked or stopped with the whole write passed nothing, so a reorder
    landing between the check and the adapter's reading was ordered from.
    """
    from cratekit.core import jobs

    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "4", "3", "1", "2")
    account_id = world.titled("GIG READY Opener")
    real = world.account.order_tracks
    stopping = [True]

    def order_tracks(playlist_id, remote_ids, *, expect=None, begun=None, **agreed):
        if playlist_id == account_id and stopping:
            stopping.clear()
            if stop == "parked":
                raise jobs.Parked(
                    refuse(
                        "provider-cooldown", "a cooldown", scope=Scope.RUN, origin=("test", "order")
                    ).cause
                )
            if stop == "refused":
                raise refuse(
                    "outbound-remove-refused",
                    "the reading may lag a write and no track was moved",
                    scope=Scope.RUN,
                    origin=("test", "order"),
                    detail={"playlist_id": playlist_id, "problem": "read-differs"},
                )
            raise refuse(
                "credential-missing",
                "the streaming provider rejected the session",
                remedy=Remedy.REAUTHENTICATE_PROVIDER,
                scope=Scope.ITEM,
                origin=("test", "order"),
            )
        return real(playlist_id, remote_ids, expect=expect, begun=begun, **agreed)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    code, done = drive(["--run", stopped["run_id"], *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.expected[-1] == (account_id, tuple(_ids("1", "2", "3", "4")))
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
    assert world.held(opener) == ["4", "3", "1", "2"]


@pytest.mark.parametrize("damage", ["unreadable", "gone"])
def test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first(
    world, cfg, monkeypatch, damage
):
    """Round two's row 1: the record carried beside the run's steps still says the order began.

    The order parked before any move, then the run's steps file is lost: the
    continue reads the carried record, as it does for moves already sent,
    and hands the adapter the check's listing to agree with.
    """
    from cratekit.core import held_plan, jobs

    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", "4", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    _reordered(world, opener, "4", "3", "1", "2")
    account_id = world.titled("GIG READY Opener")
    real = world.account.order_tracks
    stopping = [True]

    def order_tracks(playlist_id, remote_ids, *, expect=None, begun=None, **agreed):
        if playlist_id == account_id and stopping:
            stopping.clear()
            raise jobs.Parked(
                refuse("provider-cooldown", "a cooldown", scope=Scope.RUN, origin=("test", "order")).cause
            )
        return real(playlist_id, remote_ids, expect=expect, begun=begun, **agreed)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    code, stopped = sync()
    assert code != int(ExitCode.OK), stopped
    run_id = stopped["run_id"]
    where = held_plan.steps_path(run_id)
    if damage == "gone":
        where.unlink()
    else:
        where.write_text("{not json\n")
    code, done = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.OK), done
    assert world.account.expected[-1] == (account_id, tuple(_ids("1", "2", "3", "4")))
    assert world.account.playlists[account_id] == _ids("4", "3", "1", "2")
