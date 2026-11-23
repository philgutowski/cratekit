"""The label sweep's scenarios: the releases it offers for a label, through every verb that drives it (U308).

A sweep queued before U109 still resumes through `crate sync labels`, `label
import` runs one label's sweep, and `label harvest` offers a playlist's labels;
one release is tombstoned and one label cannot be listed.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.label_fakes import FakeTrack
from tests.test_label_workers import (
    LABELS,
    PLAYLIST,
    SLUGS,
    bind,
    bury,
    playlist_of,
    queued_sweep,
    readable,
)
from tests.test_label_workers import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
QUEUE = ("review", "list", "--queue", "label-release", "--all")


def test_a_sweep_offers_each_labels_releases(stage, installed, monkeypatch):
    for name in LABELS:
        assert stage.crate("label", "registry", "add", name).code == OK
    assert stage.crate("sync", "labels").code != OK
    bury(installed, "hf-2")
    bind(monkeypatch, readable(*SLUGS[:2]))
    job_id = queued_sweep()
    swept = stage.crate("sync", "labels", "--job", job_id)
    assert swept.code != OK, swept.stdout  # kompakt cannot be listed, so its item fails
    assert stage.json("sync", "labels", "--job", job_id).code != OK
    stage.json(*QUEUE)
    assert stage.crate("review", "list", "--queue", "label-release", "--group-by", "label").code == OK

    # One label's sweep queued by `label import`, and run on the same worker.
    bind(monkeypatch, readable(SLUGS[2]))
    queued = stage.json("label", "import", "Kompakt")
    assert queued.code == OK, queued.stdout
    imported = stage.crate("label", "import", "Kompakt", "--job", queued.envelope["data"]["job_id"])
    assert imported.code == OK, imported.stderr
    assert stage.crate("label", "import", "Nobody Follows This").code != OK
    stage.json(*QUEUE)


def test_harvest_offers_the_labels_behind_a_playlist(stage, installed, monkeypatch):
    bind(
        monkeypatch,
        playlist_of(
            FakeTrack("t1", copyright="2026 Anjunadeep"),
            FakeTrack("t2", copyright="(P) 2025 Mystery Distro"),
            FakeTrack("t3"),
        ),
    )
    assert stage.crate("label", "harvest", PLAYLIST).code == OK
    assert stage.json("label", "harvest", PLAYLIST).code == OK
    assert stage.crate("label", "harvest", "https://example.invalid/playlist/none").code != OK
    stage.json(*QUEUE)
