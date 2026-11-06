"""U227: which adoption ledger entries ``mirror_downloads.filed`` reads as a landing's filing.

The mutation table's zero rows, pinned at the reader itself, where the edit
rule's own guards cannot cover them: the earliest approval since the queue
(R11), a track owned by one row (R13), the earliest job holding the track
(R14) and this library's adopt approvals alone (R24). Driven on U204's
disposable world, with the queue and the ledger written as their own writers
write them and each time set by hand.
"""

from __future__ import annotations

import dataclasses

from cratekit.adopt import apply as adoption
from cratekit.core import jobs, taxonomy
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

DECLARED = taxonomy.default_taxonomy()
QUEUED = "2026-11-06T15:00:00+00:00"
LATER_QUEUED = "2026-11-06T15:30:00+00:00"
LANDING_FILED = "2026-11-06T15:11:15+00:00"
REFILED = "2026-11-06T16:00:00+00:00"


def _queue(cfg, created: str, *, handler: str = mirror_downloads.HANDLER, payload=None) -> str:
    with jobs.open_store() as store:
        if payload is None:
            job = intake_cli.queue_playlist(
                store,
                cfg,
                handler_key=handler,
                reference="pl-tech-house-med",
                tracks={"r3": {"isrc": "ISRC00000003"}},
                source_id=mirror_downloads.SOURCE_ID,
            )
        else:
            job = jobs.enqueue(store, handler_key=handler, payload=payload, cfg=cfg, item_ids=("x",))
        store.conn.execute("UPDATE jobs SET created = ? WHERE job_id = ?", (created, job.job_id))
    return job.job_id


def _entry(cfg, content_id: str, genre: str, band: str, applied: str, digest: str) -> None:
    bucket = DECLARED.bucket_for_display(genre)
    (sub,) = [one.id for one in DECLARED.energy.bands if one.display == band]
    adoption.mark_applied(
        cfg,
        adoption.AppliedEntry(
            entry_id=f"{DECLARED.tree.id}:{content_id}:{bucket}:{sub}",
            tree=DECLARED.tree.id,
            content_id=content_id,
            bucket=bucket,
            sub=sub,
            actor="session",
            digest=digest,
            applied=applied,
        ),
    )


def _filed(cfg, owner=None):
    return mirror_downloads.filed(cfg, DECLARED, owner or {"r3": {"3"}})


def test_the_earliest_approval_since_the_queue_is_the_landings(world):
    """R11: of two approvals neither an adopt job carries, the earlier is the landing's."""
    cfg = world.cfg
    _queue(cfg, QUEUED)
    _entry(cfg, "3", "Deep House", "Low", LANDING_FILED, "landing")
    _entry(cfg, "3", "Tech House", "High", REFILED, "another")
    assert _filed(cfg) == {"r3": frozenset({("Deep House", "Low")})}


def test_a_track_two_rows_own_is_read_by_neither(world):
    """R13: which row the landing made is not something two owners say."""
    cfg = world.cfg
    _queue(cfg, QUEUED)
    _entry(cfg, "3", "Deep House", "Low", LANDING_FILED, "landing")
    assert _filed(cfg, {"r3": {"3", "9"}}) == {}
    assert _filed(cfg, {"r3": {"3"}}) == {"r3": frozenset({("Deep House", "Low")})}


def test_the_earliest_job_holding_the_track_dates_its_queue(world):
    """R14: a second job for the track, queued after the landing filed, moves nothing."""
    cfg = world.cfg
    _queue(cfg, QUEUED)
    _queue(cfg, LATER_QUEUED)
    _entry(cfg, "3", "Deep House", "Low", LANDING_FILED, "landing")
    assert _filed(cfg) == {"r3": frozenset({("Deep House", "Low")})}


def test_only_this_librarys_adopt_approvals_are_a_persons(world):
    """R24: an adopt job another library queued says nothing of this library's ledger."""
    cfg = world.cfg
    _queue(cfg, QUEUED)
    _entry(cfg, "3", "Deep House", "Low", LANDING_FILED, "shared-digest")
    elsewhere = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, volume_id="another-library-volume")
    )
    _queue(elsewhere, QUEUED, handler="adopt.apply", payload={"digest": "shared-digest"})
    assert _filed(cfg) == {"r3": frozenset({("Deep House", "Low")})}
    # This library's own adopt job carrying it makes it a person's filing.
    _queue(cfg, QUEUED, handler="adopt.apply", payload={"digest": "shared-digest"})
    assert _filed(cfg) == {}
