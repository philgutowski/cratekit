"""R-1264, a paired account playlist listing a track it cannot read, on a disposable database.

``crate sync pair`` read each pair's account side through the reader that
refuses the whole playlist for one row naming no title or no artist, so a twin
``crate sync twins`` made over such a playlist (U213) stopped every pair at the
next sync. The account side is now read row by row, as the backfill reads it:
a track the reader refuses is unread, kept by its id, never added to either
side and never read as taken off the account, and while one is unread the
account takes no removal and no reorder and the snapshot does not move, the
rule a short listing already follows. A listing the reader cannot use at all
leaves its pair out of a sync of every pair, named, and the others sync.

Driven end to end through the dispatcher on the twins suite's world, the
residual's own driver.
"""

from __future__ import annotations

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
from tests.test_sync_twins import BROKEN, BROKEN_NAME, PHIL, _codes, _phil, backfill, sync_pair
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
    # THE SNAPSHOT DOES NOT MOVE while a track is unread, as for a short listing.
    after = pairs.PairStore(cfg).get(PHIL)
    assert after is not None and after.account == held.account


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


def test_while_a_track_is_unread_the_account_takes_no_removal(world, cfg):
    twin_id = _backfilled(world, untitled="t20")
    world.rekordbox_remove(twin_id, "1")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.held(twin_id) == ["3", "2"]
    assert world.account.playlists[PHIL] == ["t3", "t1", "t20", "t2"]
    # Once the account serves it whole, the removal the base still holds lands.
    world.names.pop("t20")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[PHIL] == ["t3", "t20", "t2"]
    assert pair_cli.UNREAD not in _codes(envelope)


def test_a_rekordbox_row_carrying_an_unread_tracks_isrc_is_not_added_to_the_account(world, cfg):
    _phil(world)
    assert backfill()[0] == int(ExitCode.OK)
    twin_id = world.twin("Phil 9-30-26")
    # The account lists track four with no title, and rekordbox gains its row.
    world.account.playlists[PHIL].append("t4")
    world.names["t4"] = ""
    world.rekordbox_add(twin_id, "4")
    code, envelope = sync_pair()
    assert code == int(ExitCode.OK), envelope
    assert world.account.playlists[PHIL].count("t4") == 1
    assert "4" in world.held(twin_id)


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
