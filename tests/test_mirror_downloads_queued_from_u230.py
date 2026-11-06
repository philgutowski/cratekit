"""U230: which mirrored playlists ``mirror_downloads.queued_from`` names as having queued a track.

The edit rule reads the base of the playlist whose mirror job queued a track
as it stood at the queue, so the reader must name that playlist and no other:
the job's own source, from this library's mirror jobs that did not fail or
were not cancelled, and nothing when the queue cannot be read. Driven on
U204's disposable world with the queue written by its own writer.
"""

from __future__ import annotations

import dataclasses

from cratekit.core import jobs
from cratekit.intake import cli as intake_cli
from cratekit.organize import mirror_downloads
from tests.test_organize_mirror_edits_u204 import _field_policies as _field_policies  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_organize_mirror_edits_u204 import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import configured as configured  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import installed as installed  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import library as library  # noqa: PLC0414
from tests.test_organize_mirror_edits_u204 import world as world  # noqa: PLC0414


def _queue(cfg, reference: str, tracks=("r3",), *, source_id=mirror_downloads.SOURCE_ID) -> str:
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store,
            cfg,
            handler_key=mirror_downloads.HANDLER,
            reference=reference,
            tracks={one: {"isrc": f"ISRC-{one}"} for one in tracks},
            source_id=source_id,
        )
    return job.job_id


def test_each_track_is_named_with_every_playlist_whose_job_queued_it(world):
    _queue(world.cfg, "pl-a", ("r3", "r4"))
    _queue(world.cfg, "pl-b", ("r3",))
    assert mirror_downloads.queued_from(world.cfg) == {
        "r3": frozenset({"pl-a", "pl-b"}),
        "r4": frozenset({"pl-a"}),
    }


def test_a_cancelled_job_another_source_and_another_library_name_nothing(world):
    cancelled = _queue(world.cfg, "pl-gone")
    with jobs.open_store() as store:
        jobs.cancel(store, cancelled)
    _queue(world.cfg, "pl-sweep", source_id="playlist-sweep")
    elsewhere = dataclasses.replace(
        world.cfg,
        library=dataclasses.replace(world.cfg.library, volume_id="another-library-volume"),
    )
    _queue(elsewhere, "pl-elsewhere")
    assert mirror_downloads.queued_from(world.cfg) == {}
    _queue(world.cfg, "pl-a")
    assert mirror_downloads.queued_from(world.cfg) == {"r3": frozenset({"pl-a"})}


def test_a_queue_that_cannot_be_read_names_nothing(world, monkeypatch):
    _queue(world.cfg, "pl-a")

    def unreadable(_cfg):
        raise OSError("the queue is locked")

    monkeypatch.setattr(mirror_downloads, "_jobs", unreadable)
    assert mirror_downloads.queued_from(world.cfg) == {}
