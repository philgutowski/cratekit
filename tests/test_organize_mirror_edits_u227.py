"""U227: a download an account edit queued is filed where the edit put it, once it lands.

Sitting 85, driven again on U204's disposable world: a track the library lacks
is put in a mirrored genre playlist on the account, the downloads step queues
it, it lands, and the landing files it by its own tags into another band in a
commit of its own, recording each place in the adoption ledger. Before U227
the next organize read that filing as a change made in rekordbox later than
the account's, kept rekordbox's place, and mirrored the track off the playlist
the person put it in. What is asserted is what the database and the account
hold afterwards.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import sqlite3

from cratekit.adopt import apply as adoption
from cratekit.cli.output import timestamp
from cratekit.core import taxonomy
from cratekit.modules.outbound import mirror_edits as edits
from tests.test_organize_mirror_edits_u204 import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import _items, _land_and_file, _queued
from tests.test_organize_mirror_edits_u204 import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_organize_mirror_edits_u204 import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import configured as configured  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import installed as installed  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import library as library  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import world as world  # noqa: PLC0414

DECLARED = taxonomy.default_taxonomy()
#: When the person put the track in the playlist on the account.
ACCOUNT_AT = "2026-11-06T14:56:32.535000+00:00"
#: When the landing's filing placed it in rekordbox, later than the account's.
FILED_AT = "2026-11-06 15:11:15.593 +00:00"
#: When a person moved it in rekordbox after the landing.
MOVED_AT = "2026-11-06 16:00:00.000 +00:00"


def _file_by_tags(world, content_id: str, to: tuple[str, str], at: str) -> None:
    """The landing's own filing: one band membership at ``at``, recorded in the adoption ledger."""
    genre, band = to
    conn = sqlite3.connect(world.db)
    try:
        conn.execute(
            "INSERT INTO djmdSongPlaylist (ID, PlaylistID, ContentID, TrackNo, "
            "rb_local_deleted, created_at, updated_at) VALUES (?, ?, ?, 1, 0, ?, ?)",
            (f"filed-{content_id}", world.playlists[to], content_id, at, at),
        )
        conn.commit()
    finally:
        conn.close()
    bucket = DECLARED.bucket_for_display(genre)
    (sub,) = [one.id for one in DECLARED.energy.bands if one.display == band]
    adoption.mark_applied(
        world.cfg,
        adoption.AppliedEntry(
            entry_id=f"{DECLARED.tree.id}:{content_id}:{bucket}:{sub}",
            tree=DECLARED.tree.id,
            content_id=content_id,
            bucket=bucket,
            sub=sub,
            actor="session",
            digest="landing",
            applied=timestamp(),
        ),
    )


def _queued_landed_and_filed(world, to=("Deep House", "Low")) -> None:
    world.put_in("Tech House Med", "r3", at=ACCOUNT_AT)
    world.run_all()
    assert len(_queued(world.cfg)) == 1
    _land_and_file(world, matched_as="r3")
    _file_by_tags(world, "3", to, FILED_AT)
    assert world.places("3") == {to}


def test_a_queued_track_filed_elsewhere_by_its_tags_is_filed_where_the_account_put_it(world):
    _queued_landed_and_filed(world)

    _area, step, _queue = world.run_all()

    (change,) = _items(step)
    assert change["edit"] == edits.MOVE and change["joins"] == ["Tech House / Med"]
    assert "landed for the account's edit" in change["why"]
    assert world.places("3") == {("Tech House", "Med")}
    # The account keeps it where the person put it, and is not given the band
    # its tags chose.
    assert world.held("Tech House Med") == ["r3"]
    assert "r3" not in world.held("Deep House Low")
    # ONCE: the next run reads nothing to carry and nothing to undo.
    _area, step, _queue = world.run_all()
    assert _items(step) == []
    assert world.places("3") == {("Tech House", "Med")}
    assert world.held("Tech House Med") == ["r3"]


def test_a_move_made_in_rekordbox_after_the_landing_still_stands(world):
    _queued_landed_and_filed(world)
    world.move_in_rekordbox("3", ("Deep House", "Med"), MOVED_AT)

    _area, step, _queue = world.run_all()

    assert _items(step) == []
    (kept,) = [one for one in step.items if one.get("track") == "r3"]
    assert kept["outcome"] == edits.REKORDBOX
    assert "rekordbox's place stands" in kept["why"]
    assert world.places("3") == {("Deep House", "Med")}
    assert "r3" not in world.held("Tech House Med")


def test_a_filing_recorded_before_the_download_was_queued_is_not_the_landings(world):
    """A row the library filed before the queue is no row the landing made."""
    world.put_in("Tech House Med", "r3", at=ACCOUNT_AT)
    _land_and_file(world, matched_as="r3")
    _file_by_tags(world, "3", ("Deep House", "Low"), FILED_AT)
    # The job is queued after the filing: a hand made stand in for a queue
    # that froze a track the library already filed.
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli
    from cratekit.organize import mirror_downloads

    with jobs.open_store() as store:
        intake_cli.queue_playlist(
            store,
            world.cfg,
            handler_key=mirror_downloads.HANDLER,
            reference=world.remote("Tech House Med"),
            tracks={"r3": {"isrc": "ISRC00000003"}},
            source_id=mirror_downloads.SOURCE_ID,
        )

    _area, step, _queue = world.run_all()

    assert _items(step) == []
    assert world.places("3") == {("Deep House", "Low")}
