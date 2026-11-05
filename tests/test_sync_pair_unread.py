"""R-1264, a paired account playlist listing a track it cannot read, on a disposable database.

``crate sync pair`` read each pair's account side through the reader that
refuses the whole playlist for one row naming no title or no artist, so a twin
``crate sync twins`` made over such a playlist (U213) stopped every pair at the
next sync. The account side is now read row by row, as the backfill reads it:
a track the reader refuses is unread, kept by its id, never added to either
side and never read as taken off the account. Unlike a withheld track it may
stay that way for good, so the pair still syncs whole: removals land on both
sides, the snapshot moves with the unread id recorded in its place, and a
reorder is written to the account whole, each unread track kept behind the
one listed before it. A listing the reader cannot use at all
leaves its pair out of a sync of every pair, named, and the others sync.

Driven end to end through the dispatcher on the twins suite's world, the
residual's own driver.
"""

from __future__ import annotations

import sqlite3

import pytest

from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.outbound import pairs
from cratekit.sync import pair_cli
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_twins import (
    BROKEN,
    BROKEN_NAME,
    PHIL,
    _codes,
    _phil,
    backfill,
    isrc,
    sync_pair,
)
from tests.test_sync_twins import db as db  # noqa: PLC0414
from tests.test_sync_twins import world as world  # noqa: PLC0414


def _unread(envelope) -> list[tuple[str, str, str, str]]:
    return [
        (one["remote_id"], one["artist"], one["title"], one["reason"])
        for one in envelope["data"]["items"]
        if one["side"] == "account" and one["action"] == "unread"
    ]


def _backfilled(world, *, untitled: str = "", nameless: str = "") -> str:
    """Phil's twin, made, with one of its account tracks unreadable from then on."""
    _phil(world)
    if untitled:
        world.names[untitled] = ""
    if nameless:
        world.artists[nameless] = ""
    assert backfill()[0] == int(ExitCode.OK)
    return world.twin("Phil 9-30-26")


def test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways(world, cfg):
    twin_id = _backfilled(world, untitled="t20")
    held = pairs.PairStore(cfg).get(PHIL)
    assert held is not None and "t20" in held.account
    world.account.playlists[PHIL].append("t4")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "1", "2", "4"]
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2", "t4"]
    assert _unread(envelope) == [
        ("t20", "Artist t20", "", "the account lists it with no title")
    ]
    assert pair_cli.UNREAD in _codes(envelope)
    # THE SNAPSHOT MOVES, the unread track in its place, as the account lists it.
    after = pairs.PairStore(cfg).get(PHIL)
    assert after is not None and after.account == ("t3", "t1", "t20", "t2", "t4")
    shown = envelope["data"]["totals"]
    assert shown["unread"] == 1


def test_a_track_naming_no_artist_is_unread_the_same_way(world, cfg):
    twin_id = _backfilled(world, nameless="t20")
    world.account.playlists[PHIL].append("t4")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "1", "2", "4"]
    assert _unread(envelope) == [
        ("t20", "", "Title t20", "the account lists it with no artist")
    ]


def test_an_unread_track_the_twin_holds_is_never_removed_or_added_again(world, cfg):
    twin_id = _backfilled(world, untitled="t3")
    assert world.held(twin_id) == ["3", "1", "2"]
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "1", "2"]
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2"]
    assert [one["remote_id"] for one in envelope["data"]["items"] if one["action"] in {
        "add", "remove"
    }] == []


def test_a_first_sync_never_offers_the_account_an_unread_track_it_already_lists(world, cfg):
    # A twin made off a short listing is held with no snapshot, so its next
    # sync is a first sync with no base to strip the unread track from.
    _phil(world)
    world.short.add(PHIL)
    assert backfill()[0] == int(ExitCode.OK)
    twin_id = world.twin("Phil 9-30-26")
    held = pairs.PairStore(cfg).get(PHIL)
    assert held is not None and held.first
    world.short.discard(PHIL)
    world.names["t3"] = ""
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert [
        one["remote_id"]
        for one in envelope["data"]["items"]
        if one["side"] == "account" and one["action"] == "add"
    ] == []
    assert world.account.added == []
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2"]
    assert world.held(twin_id) == ["3", "1", "2"]
    assert _unread(envelope)[0][0] == "t3"


def test_while_a_track_is_unread_a_rekordbox_removal_still_lands_on_the_account(world, cfg):
    twin_id = _backfilled(world, untitled="t20")
    world.rekordbox_remove(twin_id, "1")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "2"]
    assert world.account.playlists[PHIL] == ["t3", "t20", "t2"]
    # And once the account serves it whole, nothing comes back.
    world.names.pop("t20")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[PHIL] == ["t3", "t20", "t2"]
    assert world.held(twin_id) == ["3", "2"]
    assert pair_cli.UNREAD not in _codes(envelope)


def test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back(world, cfg):
    """From the review's round one: a snapshot held back replayed the addition."""
    twin_id = _backfilled(world, untitled="t20")
    world.account.playlists[PHIL].append("t4")
    assert sync_pair()[0] == int(ExitCode.OK)
    assert world.held(twin_id) == ["3", "1", "2", "4"]
    world.rekordbox_remove(twin_id, "4")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "1", "2"]
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2"]
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "1", "2"]


def test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back(world, cfg):
    """The same, the other way: rekordbox's addition is not replayed over the account's removal."""
    twin_id = _backfilled(world, untitled="t20")
    world.rekordbox_add(twin_id, "5")
    assert sync_pair()[0] == int(ExitCode.OK)
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2", "t5"]
    world.account.playlists[PHIL].remove("t5")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "1", "2"]
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2"]


def test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account(world, cfg):
    _phil(world)
    assert backfill()[0] == int(ExitCode.OK)
    twin_id = world.twin("Phil 9-30-26")
    # The account lists track four with no title, and rekordbox gains its row.
    world.account.playlists[PHIL].append("t4")
    world.names["t4"] = ""
    world.rekordbox_add(twin_id, "4")
    # The provider would name another release of it, which the account lacks.
    world.account.catalog["4"] = "t24"
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[PHIL].count("t4") == 1
    assert "t24" not in world.account.playlists[PHIL]
    assert "4" in world.held(twin_id)
    assert dict(pairs.PairStore(cfg).get(PHIL).links)["t4"] == "4"


def test_a_pair_whose_listing_carries_a_row_with_no_id_is_left_out_and_the_others_sync(world, cfg):
    _phil(world)
    world.playlist(BROKEN, BROKEN_NAME, ["t4", "t5"])
    assert backfill()[0] == int(ExitCode.OK)
    phil = world.twin("Phil 9-30-26")
    world.account.playlists[BROKEN].append("")
    world.account.playlists[PHIL].append("t6")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(phil) == ["3", "1", "2", "6"]
    (left,) = [one for one in envelope["warnings"] if one["code"] == pair_cli.LEFT_OUT]
    assert BROKEN in left["message"] and "provider identifier" in left["message"]
    # Named alone, the pair refuses as itself.
    code, alone = drive(["sync", "pair", BROKEN])
    assert alone["cause"]["reason"] == "intake-list-unusable", alone


def test_a_refusal_that_is_not_about_one_pair_still_stops_the_run(world, cfg):
    _phil(world)
    world.playlist(BROKEN, BROKEN_NAME, ["t4", "t5"])
    assert backfill()[0] == int(ExitCode.OK)
    world.broken[BROKEN] = refuse(
        "credential-missing", "the provider session expired", origin=("tests",)
    )
    world.account.playlists[PHIL].append("t6")
    code, envelope = sync_pair()
    assert envelope["cause"]["reason"] == "credential-missing", envelope
    assert world.held(world.twin("Phil 9-30-26")) == ["3", "1", "2"]


def test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale(world, cfg):
    twin_id = _backfilled(world, untitled="t20")
    world.account.playlists[PHIL].append("t4")
    code, envelope = drive(["sync", "pair"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    run_id = envelope["run_id"]
    # Another track the account cannot read joins after the plan was shown.
    world.account.playlists[PHIL].append("t5")
    world.names["t5"] = ""
    for _ in range(2):
        gate = envelope["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
        code, envelope = drive(["--run", run_id, "sync", "pair"])
        if code != int(ExitCode.DECISION_REQUIRED):
            break
    stale = envelope
    assert stale["cause"]["reason"] == "decision-stale", stale
    assert "tracks it cannot read" in stale["cause"]["message"], stale
    assert world.held(twin_id) == ["3", "1", "2"]


def test_a_plan_whose_unread_tracks_differ_digests_differently(world, cfg):
    _backfilled(world, untitled="t20")
    world.account.playlists[PHIL].append("t4")
    code, first = drive(["sync", "pair"])
    assert code == int(ExitCode.DECISION_REQUIRED), first
    world.account.playlists[PHIL].append("t5")
    world.names["t5"] = ""
    code, second = drive(["sync", "pair"])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    assert first["cause"]["detail"]["shown"]["digest"] != second["cause"]["detail"]["shown"]["digest"]
    facts = [str(one) for one in second["cause"]["detail"]["shown"].values()]
    assert any("lists 2 track(s) with no title or no artist" in one for one in facts), facts
    world.account.playlists[PHIL].remove("t5")
    code, third = drive(["sync", "pair"])
    assert third["cause"]["detail"]["shown"]["digest"] == first["cause"]["detail"]["shown"]["digest"]


def test_unread_tracks_trading_places_after_the_plan_is_not_stale(world, cfg):
    """From the review's round one: the same set in other places moved nothing written."""
    _backfilled(world, untitled="t20")
    world.names["t2"] = ""
    world.account.playlists[PHIL].append("t4")
    code, envelope = drive(["sync", "pair"])
    assert code == int(ExitCode.DECISION_REQUIRED), envelope
    run_id = envelope["run_id"]
    # t20 and t2 trade places; the readable tracks keep theirs.
    world.account.playlists[PHIL] = ["t3", "t1", "t2", "t20", "t4"]
    for _ in range(2):
        gate = envelope["cause"]["detail"]["gate"]
        decided, said = drive(["run", "decide", run_id, gate, "apply", "--actor", "a-person"])
        assert decided == int(ExitCode.OK), said
        code, envelope = drive(["--run", run_id, "sync", "pair"])
        if code != int(ExitCode.DECISION_REQUIRED):
            break
    assert code == int(ExitCode.OK), envelope
    assert pairs.PairStore(cfg).get(PHIL).account == ("t3", "t1", "t2", "t20", "t4")


def _rekordbox_move_last(world, twin_id: str, content_id: str) -> None:
    conn = sqlite3.connect(world.cfg.library.db_path)
    try:
        (top,) = conn.execute(
            "SELECT MAX(TrackNo) FROM djmdSongPlaylist WHERE PlaylistID = ?", (twin_id,)
        ).fetchone()
        conn.execute(
            "UPDATE djmdSongPlaylist SET TrackNo = ?, updated_at = '2026-11-05 12:00:00' "
            "WHERE PlaylistID = ? AND ContentID = ?",
            (int(top) + 1, twin_id, content_id),
        )
        conn.commit()
    finally:
        conn.close()


def test_a_rekordbox_reorder_while_a_track_is_unread_reaches_the_account_and_stands(world, cfg):
    """From the review's round two: a withheld account order let the next sync undo it."""
    twin_id = _backfilled(world, untitled="t20")
    _rekordbox_move_last(world, twin_id, "1")
    assert world.held(twin_id) == ["3", "2", "1"]
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    # THE ORDER IS WRITTEN WHOLE, the unread track behind the one listed before it.
    assert world.account.playlists[PHIL] == ["t3", "t2", "t1", "t20"]
    assert world.held(twin_id) == ["3", "2", "1"]
    for _ in range(2):
        code, envelope = sync_pair()
        assert code == int(ExitCode.OK), envelope
        assert world.held(twin_id) == ["3", "2", "1"]
        assert world.account.playlists[PHIL] == ["t3", "t2", "t1", "t20"]


def _siblings(world, listing: list[str]) -> str:
    """Phil's twin with t4 and t24 both releases of row four, settled by three syncs."""
    _phil(world)
    world.codes["t24"] = isrc("4")
    world.account.playlists[PHIL] = list(listing)
    assert backfill()[0] == int(ExitCode.OK)
    twin_id = world.twin("Phil 9-30-26")
    for _ in range(3):
        assert sync_pair()[0] == int(ExitCode.OK)
    return twin_id


@pytest.mark.parametrize(
    ("listing", "unread"),
    [
        (["t3", "t4", "t1", "t20", "t2", "t24"], "t4"),
        (["t3", "t24", "t1", "t20", "t2", "t4"], "t24"),
    ],
)
def test_a_release_turning_unread_beside_a_readable_one_moves_nothing(world, cfg, listing, unread):
    """From the review's round two: the row's key sat at the readable release's place."""
    twin_id = _siblings(world, listing)
    held = world.held(twin_id)
    account = list(world.account.playlists[PHIL])
    world.names[unread] = ""
    for _ in range(2):
        code, envelope = sync_pair()
        assert code == int(ExitCode.OK), envelope
        assert world.held(twin_id) == held
        assert world.account.playlists[PHIL] == account
    # And a person's rekordbox reorder then stands.
    _rekordbox_move_last(world, twin_id, "1")
    moved = world.held(twin_id)
    for _ in range(2):
        code, envelope = sync_pair()
        assert code == int(ExitCode.OK), envelope
        assert world.held(twin_id) == moved
