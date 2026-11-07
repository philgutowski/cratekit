"""U230: a download an account edit queued is filed there even though that playlist already lists it.

Driven on U204's disposable world with U227's producers: the track is put in
a mirrored genre playlist on the account, the downloads step queues it, it
lands, and the landing files it by its own tags into another band. Then the
playlist the person edited holds the track in its own base, as sitting 86
read the live ledger: never agreed, so its account side is its base, or
agreed with the track. Before U230 the next organize read no account edit at
all and mirrored rekordbox's place onto the account. What is asserted is what
the database and the account hold afterwards.

THE BASE IS WRITTEN BY HAND here, through the ledger's own file. The run that
queues the download keeps a held track out of an agreed snapshot
(``mirror_edits.agreed_after``), and driven here it leaves no snapshot
holding the track after the queue or the landing, so what produced the
sitting's base is unmeasured on this tree; the record says so.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json

from cratekit.core import config
from cratekit.modules.outbound import ledger
from cratekit.modules.outbound import mirror_edits as edits
from tests.test_organize_mirror_edits_u204 import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import _items
from tests.test_organize_mirror_edits_u204 import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_organize_mirror_edits_u204 import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import configured as configured  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import installed as installed  # noqa: PLC0414
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
    # Driven: the producers leave the edited playlist's snapshot without the
    # track, which is U227's shape. The sitting's base is set by hand.
    assert "r3" not in (_snapshot(world, EDITED) or frozenset())
    _set_base(world, EDITED, agreed)


def test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it(world):
    """Sitting 86's shape, the brief's verification: planned into the edited
    playlist as landed for the account's edit, then a further organize plans
    nothing."""
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
    """An agreed snapshot of the queuing playlist takes a queued track only
    once the library took the edit, so it is never lifted, and the account
    side reads as no change, U227's reading."""
    _landed_with_base(world, {"r3"})

    _area, step, _queue = world.run_all()

    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}


def test_a_move_in_rekordbox_after_the_carry_still_stands(world):
    """Once: the library took the edit, and a person's move in rekordbox after
    it is rekordbox's, mirrored onto the account."""
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
    """The queue names its playlist by its remote identifier, read back to the
    title the mirror recorded it under: a job from another playlist lifts
    nothing here."""
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    from cratekit.organize import mirror_downloads

    _landed_with_base(world, None)
    with jobs.open_store() as store:
        (real,) = [
            one
            for one in jobs.list_jobs(store)
            if (one.payload or {}).get("source_id") == mirror_downloads.SOURCE_ID
        ]
        jobs.cancel(store, real.job_id)
        other = intake_cli.queue_playlist(
            store,
            world.cfg,
            handler_key=mirror_downloads.HANDLER,
            reference=world.remote("Deep House Low"),
            tracks={"r3": {"isrc": "ISRC00000003"}},
            source_id=mirror_downloads.SOURCE_ID,
        )
        store.conn.execute("UPDATE jobs SET created = ? WHERE job_id = ?", (real.created, other.job_id))
    assert mirror_downloads.queued_from(world.cfg) == {"r3": frozenset({world.remote("Deep House Low")})}

    _area, step, _queue = world.run_all()

    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}


def _rotate_landed_batch(world) -> None:
    """The landing's batch leaves INBOX for INBOX / Old, as ``inbox rotate`` moves it."""
    import sqlite3

    conn = sqlite3.connect(world.db)
    try:
        conn.execute(
            "UPDATE djmdPlaylist SET ParentID = ? WHERE Name = ? AND ParentID = ?",
            (world.old, "2026-11-02 Landed", world.inbox),
        )
        assert conn.total_changes == 1
        conn.commit()
    finally:
        conn.close()


def test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands(world):
    """The review of U230, round one, BLOCKING: once the edit was carried the
    mirror agrees the edited playlist with the track, and once the landing's
    batch left INBOX no other snapshot holds it, so a person's drag in
    rekordbox back into the band the landing's tags chose must stand, not be
    carried back as the landing's."""
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
