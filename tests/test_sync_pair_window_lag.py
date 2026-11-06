"""U226: a sync pair plan reads an account playlist as it stands, not the window that lags it.

Sitting 84's rehearsal of ``crate sync pair`` read Space Moods in an order the
provider's window read still served minutes after the playlist was moved
back, and planned a rekordbox ``order`` item from it: applying it would have
put an order nobody holds into rekordbox. These tests drive the verb through
the dispatcher on the disposable database and the discovery suite's live
catalogue, whose window read is made to serve an older order while its
unpaged read serves the playlist as it stands.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import (
    VERB,
    Listed,
    LivePlaylist,
    _codes,
    _said,
    sync,
)
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414


def _lagging_window(world, monkeypatch, served: dict[str, list[str]], *, whole: bool) -> None:
    """Serve each named account playlist's window read in an older order; the unpaged read as it is.

    ``whole`` declares the playlist's count, so the unpaged read can be read
    as the whole playlist; without it the count is undeclared, as the
    discovery suite's catalogue leaves it.
    """

    def tracks(self, limit=None, offset=0):
        members = self.world.account.playlists.get(self.playlist_id, [])
        if limit is not None and self.playlist_id in served:
            members = served[self.playlist_id]
        size = self.page_size if limit is None else limit
        return [
            Listed(one, self.world.codes.get(one, ""), self.world.dates.get(one))
            for one in members[offset : offset + size]
        ]

    monkeypatch.setattr(LivePlaylist, "tracks", tracks)
    if whole:
        monkeypatch.setattr(
            LivePlaylist,
            "num_tracks",
            property(lambda self: len(self.world.account.playlists.get(self.playlist_id, []))),
        )


def _two_pairs(world):
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", "2", "3", under=gig)
    second = world.playlist("Second", "4", "5", under=gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    return opener, second


def test_a_window_that_serves_an_old_order_plans_no_rekordbox_order(world, monkeypatch, cfg):
    """The measured rehearsal: the unpaged read is whole, so the plan reads the playlist as it is."""
    opener, _second = _two_pairs(world)
    account_id = world.titled("GIG READY Opener")
    _lagging_window(world, monkeypatch, {account_id: ["t3", "t1", "t2"]}, whole=True)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(opener) == ["1", "2", "3"], "rekordbox took an order nobody holds"
    assert world.account.playlists[account_id] == ["t1", "t2", "t3"]
    held = pairs.PairStore(cfg).get(account_id)
    assert held is not None and held.account == ("t1", "t2", "t3")


def test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why(
    world, monkeypatch, cfg
):
    opener, second = _two_pairs(world)
    account_id = world.titled("GIG READY Opener")
    second_id = world.titled("GIG READY Second")
    world.rekordbox_add(second, "6")
    # The unpaged read is a first page of two, the window an older order of three.
    monkeypatch.setattr(LivePlaylist, "page_size", 2)
    _lagging_window(world, monkeypatch, {account_id: ["t3", "t1", "t2"]}, whole=False)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert pair_cli.LEFT_OUT in _codes(envelope), envelope
    said = _said(envelope, pair_cli.LEFT_OUT)
    assert account_id in said and "unpaged" in said
    # Nothing was written for the held pair; the other pair still synced.
    assert world.held(opener) == ["1", "2", "3"]
    assert world.account.playlists[account_id] == ["t1", "t2", "t3"]
    assert world.account.playlists[second_id] == ["t4", "t5", "t6"]


def test_a_named_pair_whose_window_lags_refuses_as_itself(world, monkeypatch):
    opener, _second = _two_pairs(world)
    account_id = world.titled("GIG READY Opener")
    monkeypatch.setattr(LivePlaylist, "page_size", 2)
    _lagging_window(world, monkeypatch, {account_id: ["t3", "t1", "t2"]}, whole=False)
    code, envelope = sync([*VERB, account_id])
    assert code == int(ExitCode.UPSTREAM_UNAVAILABLE), envelope
    assert envelope["cause"]["reason"] == "sync-pair-account-lagging"
    assert world.held(opener) == ["1", "2", "3"]


def test_the_check_before_the_write_reads_the_playlist_as_it_stands(world, monkeypatch):
    """A window that starts lagging between the plan and the write is not read as a move."""
    opener, second = _two_pairs(world)
    second_id = world.titled("GIG READY Second")
    world.rekordbox_add(second, "6")
    real = pair_cli.check

    def check(*args, **kwargs):
        _lagging_window(world, monkeypatch, {second_id: ["t5", "t4"]}, whole=True)
        return real(*args, **kwargs)

    monkeypatch.setattr(pair_cli, "check", check)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[second_id] == ["t4", "t5", "t6"]


def test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved(world, monkeypatch):
    """Round one's review: the check reads a partial unpaged read's lag as a move, naming it."""
    opener, second = _two_pairs(world)
    second_id = world.titled("GIG READY Second")
    world.rekordbox_add(second, "6")
    real = pair_cli.check

    def check(*args, **kwargs):
        monkeypatch.setattr(LivePlaylist, "page_size", 1)
        _lagging_window(world, monkeypatch, {second_id: ["t5", "t4"]}, whole=False)
        return real(*args, **kwargs)

    monkeypatch.setattr(pair_cli, "check", check)
    code, envelope = sync()
    assert code != int(ExitCode.OK), envelope
    moved = envelope["cause"]["detail"]["moved"]
    assert [one["playlist_id"] for one in moved] == [second_id]
    assert "unpaged" in moved[0]["why"]
    assert world.account.playlists[second_id] == ["t4", "t5"]


def test_the_runs_totals_carry_each_read_backs_readings_and_wait(world, monkeypatch):
    opener, _second = _two_pairs(world)
    account_id = world.titled("GIG READY Opener")
    world.sql(
        "UPDATE djmdSongPlaylist SET TrackNo = CASE ContentID WHEN '3' THEN 1 "
        "WHEN '1' THEN 2 ELSE 3 END WHERE PlaylistID = ?",
        opener,
    )
    record = {
        "playlist_id": account_id,
        "after": "move",
        "readings": 2,
        "waited": 1.0,
        "window_lagged": 1,
        "outcome": "done",
    }
    real = world.account.order_tracks

    def order_tracks(playlist_id, remote_ids, *, expect=None):
        world.account.judged.append(dict(record))
        return real(playlist_id, remote_ids, expect=expect)

    monkeypatch.setattr(world.account, "order_tracks", order_tracks)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t3", "t1", "t2"]
    assert envelope["data"]["totals"]["read_backs"] == [record]
