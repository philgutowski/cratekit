"""U209 over a sync of every pair: the held plan, the made side's folder, and no change.

Driven through ``crate sync pair`` with no argument on the disposable database
and live fake account ``tests/test_sync_pair_discover.py`` builds, where a
rekordbox playlist the author made is paired with an account playlist the
sync makes.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from cratekit.sync import pair_cli
from tests.cli_drive import drive
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import _release_process_locks as _release_process_locks  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import gates_pass as gates_pass  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414
from tests.test_sync_pair_discover import VERB, sync
from tests.test_sync_pair_discover import db as db  # noqa: PLC0414
from tests.test_sync_pair_discover import world as world  # noqa: PLC0414

APPLY = ["apply", "--actor", "a-person"]


def _to_the_write() -> str:
    code, first = drive(VERB)
    assert code == int(ExitCode.DECISION_REQUIRED), first
    run_id = first["run_id"]
    drive(["run", "decide", run_id, first["cause"]["detail"]["gate"], *APPLY])
    code, second = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_REQUIRED), second
    drive(["run", "decide", run_id, second["cause"]["detail"]["gate"], *APPLY])
    return run_id


def test_a_playlist_of_the_title_made_in_the_folder_before_the_write_refuses_stale(world):
    folder_id = world.account.create_folder("GIG READY")
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", "2", under=gig)
    run_id = _to_the_write()
    theirs = world.account.create_playlist("GIG READY Opener")
    world.account.move_to_folder(theirs, folder_id)
    code, refused = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    moved = refused["cause"]["detail"]["moved"]
    assert moved == [
        {
            "side": "account-folder",
            "playlist_id": folder_id,
            "name": "GIG READY",
            "why": "now holds a playlist titled 'GIG READY Opener'",
        }
    ]
    assert world.account.playlists[theirs] == []
    assert len([t for t in world.account.titles.values() if t == "GIG READY Opener"]) == 1


def test_a_root_folder_the_plan_makes_made_before_the_write_refuses_stale(world):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", under=gig)
    run_id = _to_the_write()
    world.account.create_folder("GIG READY")
    code, refused = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert refused["cause"]["detail"]["moved"][0]["side"] == "account-folder"
    assert world.account.folders_created == ["GIG READY"], "a second folder was made"


def test_a_made_pair_whose_rekordbox_side_moved_before_the_write_refuses_stale(world):
    gig = world.folder("GIG READY")
    opener = world.playlist("Opener", "1", under=gig)
    run_id = _to_the_write()
    world.rekordbox_add(opener, "2")
    code, refused = drive(["--run", run_id, *VERB])
    assert code == int(ExitCode.DECISION_STALE), refused
    assert [one["playlist_id"] for one in refused["cause"]["detail"]["moved"]] == [opener]
    assert world.account.created == []


def test_a_no_change_sync_of_every_made_pair_asks_nothing_about_a_track(world, cfg):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", "2", "3", under=gig)
    world.playlist("Closer", "4", "5", under=gig)
    # Row five is a track the account has none of: asked once, remembered.
    del world.account.catalog["5"]
    assert sync()[0] == int(ExitCode.OK)
    asked = len(world.account.matches)
    assert asked == 5
    code, envelope = sync()
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert len(world.account.matches) == asked, world.account.matches[asked:]
    assert envelope["data"]["totals"]["calls"] == {"plan": 0, "check": 0, "write": 0}


def test_every_pair_plans_once_across_its_gates(world):
    gig = world.folder("GIG READY")
    world.playlist("Opener", "1", "2", under=gig)
    code, first = drive(VERB)
    asked = len(world.account.matches)
    assert asked == 2
    run_id = first["run_id"]
    drive(["run", "decide", run_id, first["cause"]["detail"]["gate"], *APPLY, "--continue"])
    code, done = drive(["run", "decide", run_id, pair_cli.ACCOUNT_GATE, *APPLY, "--continue"])
    assert code == int(ExitCode.OK), done
    assert len(world.account.matches) == asked
    assert world.account.playlists[world.titled("GIG READY Opener")] == ["t1", "t2"]
