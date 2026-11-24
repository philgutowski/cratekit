"""U230: a queued download is filed where the edit put it though that playlist lists it. D1."""

from __future__ import annotations

import json

from cratekit.core import config
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound import mirror_edits as edits
from tests.test_organize_mirror_edits_u204 import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import _items, _queued
from tests.test_organize_mirror_edits_u204 import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import _release_process_locks as _release_process_locks
from tests.test_organize_mirror_edits_u204 import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import configured as configured  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import library as library  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import world as world  # noqa: PLC0414
from tests.test_organize_mirror_edits_u227 import MOVED_AT, _queued_landed_and_filed

EDITED = "Tech House Med"


def _snapshot(world, title: str):
    """The recorded snapshot of one mirrored playlist, ``None`` for one never agreed."""
    for folder in ledger.mirror_folders(world.cfg).values():
        if title in folder.playlists:
            return folder.playlists[title].agreed
    raise AssertionError(title)


def _set_base(world, title: str, agreed) -> None:
    """Write one playlist's snapshot in the ledger's file: a list, or absent for never agreed."""
    path = config.state_path("outbound_writes", world.cfg)
    document = json.loads(path.read_text(encoding="utf-8"))
    for record in document["mirrors"].values():
        entry = record["playlists"].get(title)
        if entry is None:
            continue
        if agreed is None:
            entry.pop("agreed", None)
        else:
            entry["agreed"] = sorted(agreed)
    path.write_text(json.dumps(document), encoding="utf-8")
    assert _snapshot(world, title) == (None if agreed is None else frozenset(agreed))


def _landed_with_base(world, agreed) -> None:
    _queued_landed_and_filed(world)
    # The producers leave the edited snapshot without the track (U227's shape).
    assert "r3" not in (_snapshot(world, EDITED) or frozenset())
    _set_base(world, EDITED, agreed)


def test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it(world):
    """Sitting 86's shape: carried into the edited playlist as landed, and once only."""
    _landed_with_base(world, None)
    _area, step, _queue = world.run_all()
    (change,) = _items(step)
    assert change["edit"] == edits.MOVE and change["joins"] == ["Tech House / Med"]
    assert "landed for the account's edit" in change["why"]
    assert world.places("3") == {("Tech House", "Med")}
    assert world.held(EDITED) == ["r3"]
    assert "r3" not in world.held("Deep House Low")
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Tech House", "Med")}
    assert world.held(EDITED) == ["r3"]


def test_an_agreed_snapshot_holding_the_track_is_the_librarys_word(world):
    """An agreed snapshot holds a queued track only once the library took the edit: never lifted."""
    _landed_with_base(world, {"r3"})
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}


def test_a_move_in_rekordbox_after_the_carry_still_stands(world):
    """Once the library took the edit, a person's move in rekordbox after it is rekordbox's."""
    _landed_with_base(world, None)
    _area, step, _queue = world.run_all()
    assert [one["edit"] for one in _items(step)] == [edits.MOVE]
    world.move_in_rekordbox("3", ("Deep House", "Med"), MOVED_AT)
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Med")}
    assert "r3" not in world.held(EDITED)


def test_another_playlists_snapshot_holding_the_track_keeps_rekordboxs_place(world):
    """A row another mirrored playlist's snapshot held is never read as landed."""
    _landed_with_base(world, None)
    _set_base(world, "Deep House Med", {"r3"})
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}


def test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base(world):
    """The queue names its playlist by remote identifier: a job from another one lifts nothing."""
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    from cratekit.organize import mirror_downloads
    _landed_with_base(world, None)
    (real,) = _queued(world.cfg)
    with jobs.open_store() as store:
        jobs.cancel(store, real.job_id)
        other = intake_cli.queue_playlist(
            store, world.cfg, handler_key=mirror_downloads.HANDLER,
            reference=world.remote("Deep House Low"), tracks={"r3": {"isrc": "ISRC00000003"}},
            source_id=mirror_downloads.SOURCE_ID,
        )
        store.conn.execute("UPDATE jobs SET created = ? WHERE job_id = ?", (real.created, other.job_id))
    assert mirror_downloads.queued_from(world.cfg) == {"r3": frozenset({world.remote("Deep House Low")})}
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}


def _rotate_landed_batch(world) -> None:
    """The landing's batch leaves INBOX for INBOX / Old, as ``inbox rotate`` moves it."""
    ((landed,),) = world.sql("SELECT ID FROM djmdPlaylist WHERE Name = ? AND ParentID = ?", "2026-11-02 Landed", world.inbox)
    world.into_old(landed)


def test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands(world):
    """Review round one, BLOCKING: a drag back after the carry and the rotation is a person's."""
    _landed_with_base(world, None)
    _area, step, _queue = world.run_all()
    assert [one["edit"] for one in _items(step)] == [edits.MOVE]
    assert _snapshot(world, EDITED) == frozenset({"r3"})
    _rotate_landed_batch(world)
    world.run_all()
    world.move_in_rekordbox("3", ("Deep House", "Low"), MOVED_AT)
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}
    assert "r3" not in world.held(EDITED)
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}
