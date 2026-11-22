"""U230: which mirrored playlists ``mirror_downloads.queued_from`` names as having queued a track."""

from __future__ import annotations

import dataclasses

from cratekit.core import jobs
from cratekit.intake import cli as intake_cli
from cratekit.organize import mirror_downloads
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import _release_process_locks as _release_process_locks
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414


def _queue(cfg, reference: str, tracks=("r3",), *, source_id=mirror_downloads.SOURCE_ID) -> str:
    with jobs.open_store() as store:
        job = intake_cli.queue_playlist(
            store, cfg, handler_key=mirror_downloads.HANDLER, reference=reference,
            tracks={one: {"isrc": f"ISRC-{one}"} for one in tracks}, source_id=source_id,
        )
    return job.job_id


def test_each_track_is_named_with_every_playlist_whose_job_queued_it(acknowledged):
    _queue(acknowledged, "pl-a", ("r3", "r4"))
    _queue(acknowledged, "pl-b", ("r3",))
    assert mirror_downloads.queued_from(acknowledged) == {"r3": frozenset({"pl-a", "pl-b"}), "r4": frozenset({"pl-a"})}


def test_a_cancelled_job_another_source_and_another_library_name_nothing(acknowledged):
    cfg = acknowledged
    cancelled = _queue(cfg, "pl-gone")
    with jobs.open_store() as store:
        jobs.cancel(store, cancelled)
    _queue(cfg, "pl-sweep", source_id="playlist-sweep")
    _queue(dataclasses.replace(cfg, library=dataclasses.replace(cfg.library, volume_id="elsewhere")), "pl-elsewhere")
    assert mirror_downloads.queued_from(cfg) == {}
    _queue(cfg, "pl-a")
    assert mirror_downloads.queued_from(cfg) == {"r3": frozenset({"pl-a"})}


def test_a_queue_that_cannot_be_read_names_nothing(acknowledged, monkeypatch):
    _queue(acknowledged, "pl-a")
    def unreadable(_cfg):
        raise OSError("the queue is locked")
    monkeypatch.setattr(mirror_downloads, "_jobs", unreadable)
    assert mirror_downloads.queued_from(acknowledged) == {}
