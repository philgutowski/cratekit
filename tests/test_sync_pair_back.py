"""U202, ``crate sync pair`` with no argument, the other way: a playlist made on the account comes to rekordbox.

Driven through the dispatcher on a disposable database and the fake account
U198's tests built, so a playlist one sync makes is one the next sync lists.
Every scenario the brief names is driven end to end, both explicit gates and
their recorded answers included: an account playlist made in a synced root
folder is made in the matching rekordbox folder and paired, and where a track
was added on one side and taken off the other since the last sync, the later
change wins, an unknown moment keeping the track and naming the call.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from cratekit.core import rb_writer
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli, pair_discover, pair_merge, pair_reverse
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import (
    _codes,
    _items,
    _said,
    plan_only,
    sync,
)
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414

#: A moment well before any sync a test drives, for the tracks a test starts with.
LONG_AGO = datetime(2026, 1, 1, tzinfo=timezone.utc)


def soon(minutes: int) -> datetime:
    """A moment after every sync a test drives so far, for a change made since."""
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


def stored(moment: datetime) -> str:
    """A moment as the database stores one, UTC text with its offset."""
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.000 +00:00")


def on_account(world, title: str, folder: str, *tracks: str) -> str:
    """A playlist the author makes on the account, by hand, inside one root folder."""
    folder_id = next(fid for fid, name in world.account.folders().items() if name == folder)
    playlist_id = world.account.create_playlist(title)
    world.account.move_to_folder(playlist_id, folder_id)
    world.account.playlists[playlist_id] = list(tracks)
    return playlist_id


def in_rekordbox(world, parent: str | None) -> dict[str, str]:
    """Every live node directly under ``parent``, name to identifier; None is the root."""
    rows = world.sql(
        "SELECT ID, Name, ParentID FROM djmdPlaylist WHERE COALESCE(rb_local_deleted, 0) = 0"
    )
    if parent is None:
        return {name: str(pid) for pid, name, at in rows if str(at or "") in ("root", "", "0")}
    return {name: str(pid) for pid, name, at in rows if str(at) == str(parent)}


@pytest.fixture
def gig(world):
    """GIG READY, synced once, so its account root folder is recorded."""
    folder = world.folder("GIG READY")
    world.playlist("Opener", "1", under=folder)
    for track in ("t1", "t2", "t3", "t4", "t5", "t6"):
        world.dates[track] = LONG_AGO
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    return folder


# ═══════════════════════════════════════════════════════════════════════════
# An account playlist in a synced folder comes to rekordbox
# ═══════════════════════════════════════════════════════════════════════════


def test_a_playlist_made_on_the_account_in_gig_ready_lands_in_its_folder_and_is_paired(
    world, cfg, gig
):
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4", "t2", "t5")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    inside = in_rekordbox(world, gig)
    assert set(inside) == {"Opener", "Closer"}
    assert world.held(inside["Closer"]) == ["4", "2", "5"]
    held = pairs.PairStore(cfg).get(closer)
    assert held is not None and held.rekordbox_id == inside["Closer"]
    assert held.made and held.folder == "GIG READY"
    assert held.account == ("t4", "t2", "t5")
    assert envelope["data"]["totals"]["created_in_rekordbox"] == [inside["Closer"]]
    # Nothing was written to the account playlist, which already held the list.
    assert world.account.playlists[closer] == ["t4", "t2", "t5"]


def test_a_second_run_plans_nothing(world, gig):
    on_account(world, "GIG READY Closer", "GIG READY", "t4", "t5")
    assert sync()[0] == int(ExitCode.OK)
    before = in_rekordbox(world, gig)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert in_rekordbox(world, gig) == before


def test_the_gate_shows_the_playlist_made_and_its_tracks(world, gig):
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4", "t5")
    plan = plan_only()
    (made,) = _items(plan, "rekordbox", "create")
    assert made["where"] == "GIG READY / Closer" and made["name"] == "Closer"
    assert made["account_id"] == closer and made["pair"] == closer
    assert [item["content_id"] for item in _items(plan, "rekordbox", "add")] == ["4", "5"]
    assert plan["totals"]["created_in_rekordbox"] == 1


def test_a_playlist_in_playlists_lands_at_the_rekordbox_root(world, cfg):
    world.playlist("Loose", "1")
    world.dates["t1"] = LONG_AGO
    assert sync()[0] == int(ExitCode.OK)
    late = on_account(world, "Playlists Late", "Playlists", "t3")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    root = in_rekordbox(world, None)
    assert "Late" in root and world.held(root["Late"]) == ["3"]
    assert pairs.PairStore(cfg).get(late).rekordbox_id == root["Late"]


def test_a_subfolder_the_title_names_is_used_and_one_it_does_not_is_not(world, gig):
    halloween = world.folder("Halloween", under=gig)
    on_account(world, "GIG READY Halloween Closer", "GIG READY", "t4")
    on_account(world, "GIG READY Winter Closer", "GIG READY", "t5")
    assert sync()[0] == int(ExitCode.OK)
    assert world.held(in_rekordbox(world, halloween)["Closer"]) == ["4"]
    assert world.held(in_rekordbox(world, gig)["Winter Closer"]) == ["5"]


def test_a_released_account_playlist_is_never_made_again(world, cfg, gig):
    opener = in_rekordbox(world, gig)["Opener"]
    account_id = world.titled("GIG READY Opener")
    world.delete_rekordbox(opener)
    assert sync()[0] == int(ExitCode.OK)
    assert account_id in pairs.PairStore(cfg).released().account
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert "Opener" not in in_rekordbox(world, gig)
    (left,) = _items(envelope["data"], "account-discovery", pair_discover.RELEASED)
    assert left["account_id"] == account_id
    assert "GIG READY Opener" in _said(envelope, pair_cli.NOT_BROUGHT)


def test_a_made_pair_whose_rekordbox_playlist_is_deleted_releases_its_account_playlist(
    world, cfg, gig
):
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4")
    assert sync()[0] == int(ExitCode.OK)
    world.delete_rekordbox(in_rekordbox(world, gig)["Closer"])
    assert sync()[0] == int(ExitCode.OK)
    assert pairs.PairStore(cfg).get(closer) is None
    assert closer in pairs.PairStore(cfg).released().account
    assert sync()[0] == int(ExitCode.OK)
    assert "Closer" not in in_rekordbox(world, gig)
    assert world.account.playlists[closer] == ["t4"]


def test_two_account_playlists_of_one_rekordbox_name_refuse_that_name_only(world, cfg, gig):
    first = on_account(world, "GIG READY Closer", "GIG READY", "t4")
    second = on_account(world, "GIG READY Closer", "GIG READY", "t5")
    other = on_account(world, "GIG READY Other", "GIG READY", "t6")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    inside = in_rekordbox(world, gig)
    assert "Closer" not in inside and "Other" in inside
    twice = _items(envelope["data"], "account-discovery", pair_discover.TWICE)
    assert sorted(item["account_id"] for item in twice) == sorted([first, second])
    store = pairs.PairStore(cfg)
    assert store.get(first) is None and store.get(second) is None
    assert store.get(other) is not None


def test_a_rekordbox_playlist_of_the_name_no_pair_holds_is_left_and_named(world, gig):
    world.playlist("Closer", "6", under=gig)
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    rows = [r for r in world.sql("SELECT ID FROM djmdPlaylist WHERE Name = 'Closer'")]
    assert len(rows) == 1
    (left,) = _items(envelope["data"], "account-discovery", pair_discover.TAKEN)
    assert left["account_id"] == closer and "no pair made" in left["why"]
    assert world.account.playlists[closer] == ["t4"]


def test_a_missing_track_is_queued_once_and_then_awaits(world, gig):
    world.codes["tx"] = "USZZZ2600099"
    on_account(world, "GIG READY Closer", "GIG READY", "t4", "tx")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert len(envelope["data"]["totals"]["queued_jobs"]) == 1
    assert world.held(in_rekordbox(world, gig)["Closer"]) == ["4"]
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert envelope["data"]["totals"]["queued_jobs"] == []
    assert pair_cli.AWAITING in _codes(envelope)


def test_skipping_the_rekordbox_gate_makes_nothing_and_the_next_sync_makes_it(world, cfg, gig):
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4")
    code, _envelope = sync(rekordbox="skip")
    assert code == int(ExitCode.OK)
    assert "Closer" not in in_rekordbox(world, gig)
    assert pairs.PairStore(cfg).get(closer) is None
    assert sync()[0] == int(ExitCode.OK)
    assert "Closer" in in_rekordbox(world, gig)


def test_skipping_the_account_gate_makes_the_rekordbox_side_and_no_snapshot(world, cfg, gig):
    closer = on_account(world, "GIG READY Closer", "GIG READY", "t4")
    assert sync(account="skip")[0] == int(ExitCode.OK)
    held = pairs.PairStore(cfg).get(closer)
    assert held is not None and held.made and held.first
    assert sync()[0] == int(ExitCode.OK)
    assert pairs.PairStore(cfg).get(closer).account == ("t4",)


def test_a_sync_naming_one_pair_brings_nothing_over(world, cfg, gig):
    on_account(world, "GIG READY Closer", "GIG READY", "t4")
    opener = world.titled("GIG READY Opener")
    code, envelope = sync([*pair_cli_verb(), opener])
    assert code == int(ExitCode.OK), envelope
    assert "Closer" not in in_rekordbox(world, gig)


def pair_cli_verb() -> list[str]:
    return ["sync", "pair"]


# ═══════════════════════════════════════════════════════════════════════════
# Where it goes: home_of, read on the database itself
# ═══════════════════════════════════════════════════════════════════════════


def _home(world, folder: str, title: str, **kwargs):
    handle = world.open()
    try:
        return pair_discover.home_of(
            handle,
            folder,
            title,
            tops=kwargs.get("tops", (frozenset(), frozenset())),
            favorites=kwargs.get("favorites", "All Favorites"),
            skip=kwargs.get("skip", ("ARCHIVE",)),
        )
    finally:
        rb_writer.close_db(handle)


def test_home_of_refuses_each_place_it_cannot_decide(world):
    gig = world.folder("GIG READY")
    world.folder("Deep", under=gig)
    world.folder("Deep", under=gig)
    world.folder("TWICE")
    world.folder("TWICE")
    archive = world.folder("ARCHIVE")
    assert archive
    assert "no live top level folder" in _home(world, "NOWHERE", "NOWHERE Closer")
    assert "2 top level folders" in _home(world, "TWICE", "TWICE Closer")
    assert "pair_skip_folders" in _home(world, "ARCHIVE", "ARCHIVE Closer")
    assert "only its folder's name" in _home(world, "GIG READY", "GIG READY")
    assert "2 folders named 'Deep'" in _home(world, "GIG READY", "GIG READY Deep Cuts")
    assert "Cratekit" in _home(
        world, "GIG READY", "GIG READY X", tops=(frozenset(), frozenset({"GIG READY"}))
    )
    assert "Cratekit" in _home(
        world, "GIG READY", "GIG READY X", tops=(frozenset({gig}), frozenset())
    )


def test_home_of_reads_the_longest_subfolder_and_strips_the_prefix(world):
    gig = world.folder("GIG READY")
    world.folder("Deep", under=gig)
    house = world.folder("Deep House", under=gig)
    home = _home(world, "GIG READY", "GIG READY Deep House Opener")
    assert isinstance(home, pair_discover.Home)
    assert (home.name, home.parent_id, home.where) == (
        "Opener",
        house,
        "GIG READY / Deep House / Opener",
    )
    plain = _home(world, "GIG READY", "Opener")
    assert (plain.name, plain.parent_id) == ("Opener", gig)
    root = _home(world, "Playlists", "Playlists GIG READY Opener")
    assert (root.name, root.parent_id, root.parent) == ("GIG READY Opener", "", "root")


def test_home_of_refuses_the_folder_holding_the_favourites(world):
    gig = world.folder("GIG READY")
    world.playlist("All Favorites", under=gig)
    assert "favourites" in _home(world, "GIG READY", "GIG READY Closer")


def test_the_write_refuses_a_name_taken_since_the_plan(world, cfg, gig):
    home = _home(world, "GIG READY", "GIG READY Closer")
    world.playlist("Closer", under=gig)
    handle = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        with pytest.raises(Exception) as caught:
            pair_reverse.create(cfg, handle, home, ("4",), source="test", analysis_roots=["/x"])
    finally:
        rb_writer.close_db(handle)
    assert getattr(caught.value, "cause", None) is not None
    assert caught.value.cause.reason == "decision-stale"


# ═══════════════════════════════════════════════════════════════════════════
# The later change wins
# ═══════════════════════════════════════════════════════════════════════════


def _rekordbox_removed(world, playlist_id: str, content_id: str, when: datetime | None) -> None:
    """Take a track out as rekordbox would, its row marked removed at ``when``."""
    world.rekordbox_remove(playlist_id, content_id)
    if when is not None:
        world.sql(
            "UPDATE djmdSongPlaylist SET updated_at = ? WHERE PlaylistID = ? AND ContentID = ?",
            stored(when),
            playlist_id,
            content_id,
        )


def _paired_on_both(world, gig) -> tuple[str, str]:
    """GIG READY Set, holding rows 4 and 5 on both sides, synced whole with its dates."""
    playlist = world.playlist("Set", "4", "5", under=gig)
    assert sync()[0] == int(ExitCode.OK)
    account_id = world.titled("GIG READY Set")
    assert sync()[0] == int(ExitCode.OK)
    return playlist, account_id


def test_the_snapshot_records_each_account_tracks_added_date(world, cfg, gig):
    _playlist, account_id = _paired_on_both(world, gig)
    held = pairs.PairStore(cfg).get(account_id)
    assert dict(held.account_added) == {
        "t4": LONG_AGO.isoformat(),
        "t5": LONG_AGO.isoformat(),
    }


def test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both(world, gig):
    playlist, account_id = _paired_on_both(world, gig)
    _rekordbox_removed(world, playlist, "5", soon(1))
    world.account.playlists[account_id] = ["t4", "t5"]
    world.dates["t5"] = soon(2)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(playlist) == ["4", "5"]
    assert world.account.playlists[account_id] == ["t4", "t5"]
    (call,) = _items(envelope["data"], "merge", pair_merge.ADDITION_LATER)
    assert call["added_on"] == "account" and call["removed_at"] and call["added_at"]
    assert "the addition was later" in _said(envelope, pair_cli.LATER_CHANGE)


def test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both(
    world, gig
):
    playlist, account_id = _paired_on_both(world, gig)
    world.dates["t5"] = soon(1)
    _rekordbox_removed(world, playlist, "5", soon(2))
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(playlist) == ["4"]
    assert world.account.playlists[account_id] == ["t4"]
    assert _items(envelope["data"], "merge", pair_merge.REMOVAL_LATER)
    assert "taken off both" in _said(envelope, pair_cli.LATER_CHANGE)


def test_without_its_added_date_the_account_reads_as_unchanged_and_the_removal_applies(
    world, gig
):
    """R-990 as it was: no later date on the account, so rekordbox's removal is applied."""
    playlist, account_id = _paired_on_both(world, gig)
    _rekordbox_removed(world, playlist, "5", soon(1))
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t4"]
    assert not _items(envelope["data"], "merge", pair_merge.TIME_UNKNOWN)


def test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call(world, gig):
    playlist, account_id = _paired_on_both(world, gig)
    world.sql(
        "DELETE FROM djmdSongPlaylist WHERE PlaylistID = ? AND ContentID = ?", playlist, "5"
    )
    world.dates["t5"] = soon(1)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.held(playlist) == ["4", "5"]
    assert world.account.playlists[account_id] == ["t4", "t5"]
    (call,) = _items(envelope["data"], "merge", pair_merge.TIME_UNKNOWN)
    assert call["removed_at"] == "" and call["title"] == "Title t5"
    assert "Title t5" in _said(envelope, pair_cli.TIME_UNKNOWN)


def test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment(world, gig):
    playlist, account_id = _paired_on_both(world, gig)
    _rekordbox_removed(world, playlist, "5", None)
    world.dates["t5"] = soon(1)
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t4", "t5"]
    assert pair_cli.TIME_UNKNOWN in _codes(envelope)


def test_a_track_put_back_in_rekordbox_after_the_account_took_it_out_stays_and_is_named(
    world, gig
):
    playlist, account_id = _paired_on_both(world, gig)
    world.account.playlists[account_id] = ["t4"]
    _rekordbox_removed(world, playlist, "5", None)
    world.rekordbox_add(playlist, "5")
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[account_id] == ["t4", "t5"]
    (call,) = _items(envelope["data"], "merge", pair_merge.TIME_UNKNOWN)
    assert call["added_on"] == "rekordbox" and call["added_at"]
