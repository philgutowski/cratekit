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

    def order_tracks(playlist_id, remote_ids, *, expect=None):
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
        return real(playlist_id, remote_ids, expect=expect)

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
