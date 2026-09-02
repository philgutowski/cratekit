"""U22: incremental sync per source, watermark as audit, not as a date floor.

KTD11 is the load bearing rule. Scope is most-recent-N plus dedup against what
is owned. A watermark records how far a clean source got and gates nothing on
its own. The source system used the watermark as a date floor, a silent
zero-scope run marked a playlist fully taken, and that is the defect this unit
must not reintroduce.

R25 and R29 sit on top of that: each source is its own job, one failing does
not block the others, a watermark advances only on clean completion, a total
lookup failure raises rather than looking like an empty catalogue, crash debris
is never next-run intake, and every source in one run accumulates into one
importable file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core import config, profiles
from cratekit.core.cause import CratekitError
from cratekit.sync import artifacts, marks, run, scope, sources, watermarks


@pytest.fixture
def cfg(tmp_path):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    built = config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": {
                "root": str(root),
                "volume_id": "F1E2-D3C4",
                "db_path": str(root / "db" / "master.db"),
            },
            "paths": {"download_staging": str(tmp_path / "staging")},
            "profile": {"name": "full"},
        }
    )
    config.save(built)
    config.reset_cache()
    return built


def _candidate(identity: str, recency: str) -> run.Candidate:
    return run.Candidate(identity=identity, recency=recency)


class FakeSource:
    """A source the tests can script. Identity is a stable id, never a name."""

    def __init__(
        self,
        source_id: str,
        items: list[run.Candidate] | None = None,
        *,
        lookup_error: Exception | None = None,
        process_errors: dict[str, Exception] | None = None,
    ) -> None:
        self.id = source_id
        self.items = list(items or [])
        self.lookup_error = lookup_error
        self.process_errors = dict(process_errors or {})
        self.processed: list[str] = []

    def list_recent(self, n: int) -> list[run.Candidate]:
        if self.lookup_error is not None:
            raise self.lookup_error
        return list(self.items[:n])

    def process(
        self,
        candidate: run.Candidate,
        registry: artifacts.ArtifactRegistry,
        run_id: str,
    ) -> None:
        error = self.process_errors.get(candidate.identity)
        if error is not None:
            raise error
        self.processed.append(candidate.identity)


class OfferingSource(FakeSource):
    """A source whose ``process`` offers for a decision rather than acquiring.

    ``LabelSource`` is the real one: it calls ``review.offer``, which queues an
    item and hands it back with a verdict of ``None``. Nothing has landed in the
    library, so a run over this source must leave no intake file and no
    watermark behind. Declared as a class attribute rather than set on an
    instance because that is where the real source declares it, and a test that
    patched it per instance would not prove the class carries it.
    """

    acquires = False


def test_an_offering_source_writes_no_intake_file(cfg):
    """R-140. A completed offer is not an acquisition and must not claim one."""
    store = watermarks.WatermarkStore(cfg)
    staging = Path(cfg.paths.download_staging)
    registry = artifacts.ArtifactRegistry(cfg)
    source = OfferingSource(
        "labels",
        [_candidate("r1", "3"), _candidate("r2", "2"), _candidate("r3", "1")],
    )

    result = run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=registry,
        run_id="run-offer-1",
        staging=staging,
    )

    assert result.shortfall is None
    assert result.processed == ("r1", "r2", "r3")
    # Asserted at the path the increment would have used, computed here from the
    # same helper the increment calls. A directory that happens to be empty
    # proves nothing about which file was skipped.
    target = run.intake_path(staging, "run-offer-1")
    assert not target.exists()
    assert registry.intake_eligible([target]) == []


def test_an_offering_run_leaves_the_source_watermark_unset(cfg):
    """Read back from the store, because an unadvanced cursor is the claim."""
    store = watermarks.WatermarkStore(cfg)
    source = OfferingSource("labels", [_candidate("r1", "3")])

    run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-offer-2",
        staging=Path(cfg.paths.download_staging),
    )

    assert store.read("labels") is None


def test_an_acquiring_source_still_writes_the_intake_file_and_advances(cfg):
    """The default is pinned beside the new branch, so it cannot drift silently."""
    store = watermarks.WatermarkStore(cfg)
    staging = Path(cfg.paths.download_staging)
    source = FakeSource("playlists", [_candidate("p1", "3"), _candidate("p2", "2")])
    assert not hasattr(source, "acquires"), (
        "this double must NOT declare the attribute; it is what proves a source "
        "written before the declaration existed still acquires"
    )

    result = run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-acquire-1",
        staging=staging,
    )

    assert result.shortfall is None
    target = run.intake_path(staging, "run-acquire-1")
    assert target.exists()
    assert "p1" in target.read_text(encoding="utf-8")
    assert store.read("playlists").cursor == "p1"


def test_one_run_records_only_the_acquiring_source_of_a_mixed_pair(cfg):
    """One intake file, and an offer does not get to put its identities in it."""
    store = watermarks.WatermarkStore(cfg)
    staging = Path(cfg.paths.download_staging)
    staging.mkdir(parents=True, exist_ok=True)
    acquiring = FakeSource("playlists", [_candidate("p1", "1")])
    offering = OfferingSource("labels", [_candidate("l1", "1")])

    results = run.run_independent(
        [acquiring, offering],
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-mixed",
        staging=staging,
    )

    assert results["labels"].shortfall is None
    assert results["playlists"].shortfall is None
    importables = list(staging.glob("*_synced.xml"))
    assert len(importables) == 1
    text = importables[0].read_text(encoding="utf-8")
    assert "p1" in text
    assert "l1" not in text
    assert store.read("playlists") is not None
    assert store.read("labels") is None


def test_the_label_source_declares_that_it_does_not_acquire():
    """Asserted on the class, so an instance cannot be what carries the promise."""
    from cratekit.label import sweep

    assert sweep.LabelSource.acquires is False


def test_errors_leave_the_watermark_unchanged_and_report_the_shortfall(cfg):
    store = watermarks.WatermarkStore(cfg)
    source = FakeSource(
        "labels",
        [_candidate("a", "3"), _candidate("b", "2")],
        process_errors={"b": RuntimeError("provider 429")},
    )

    result = run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-1",
        staging=Path(cfg.paths.download_staging),
    )

    assert store.read("labels") is None
    assert result.errors
    assert result.shortfall is not None
    assert "b" in result.shortfall or result.errors


def test_every_lookup_failing_raises_and_does_not_advance(cfg):
    store = watermarks.WatermarkStore(cfg)
    source = FakeSource(
        "favorites",
        lookup_error=run.LookupFailure("every listing call failed"),
    )

    with pytest.raises(CratekitError) as excinfo:
        run.increment(
            source,
            owned=set(),
            limit=10,
            watermarks=store,
            artifacts=artifacts.ArtifactRegistry(cfg),
            run_id="run-2",
            staging=Path(cfg.paths.download_staging),
        )

    assert excinfo.value.cause.reason == "sync-source-lookups-failed"
    assert store.read("favorites") is None


def test_one_source_failing_does_not_block_the_other(cfg):
    store = watermarks.WatermarkStore(cfg)
    staging = Path(cfg.paths.download_staging)
    failing = FakeSource(
        "labels",
        lookup_error=run.LookupFailure("labels down"),
    )
    ok = FakeSource("playlists", [_candidate("p1", "9")])

    results = run.run_independent(
        [failing, ok],
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-3",
        staging=staging,
    )

    assert isinstance(results["labels"], CratekitError)
    assert isinstance(results["playlists"], run.IncrementResult)
    assert store.read("labels") is None
    assert store.read("playlists") is not None
    assert store.read("playlists").cursor == "p1"


def test_a_rerun_after_a_clean_sync_processes_only_unowned_items(cfg):
    store = watermarks.WatermarkStore(cfg)
    staging = Path(cfg.paths.download_staging)
    registry = artifacts.ArtifactRegistry(cfg)
    first = FakeSource(
        "playlists",
        [_candidate("old", "1"), _candidate("mid", "2")],
    )

    first_result = run.increment(
        first,
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=registry,
        run_id="run-4a",
        staging=staging,
    )
    assert first_result.shortfall is None
    assert store.read("playlists") is not None

    owned = set(first.processed)
    second = FakeSource(
        "playlists",
        [_candidate("new", "3"), _candidate("old", "1"), _candidate("mid", "2")],
    )
    second_result = run.increment(
        second,
        owned=owned,
        limit=10,
        watermarks=store,
        artifacts=registry,
        run_id="run-4b",
        staging=staging,
    )

    assert second.processed == ["new"]
    assert second_result.processed == ("new",)


def test_a_watermark_does_not_empty_the_scope_of_unowned_items(cfg):
    """KTD11. The silent zero-scope failure used the watermark as a date floor."""
    store = watermarks.WatermarkStore(cfg)
    store.advance(
        "playlists",
        cursor="zzz",
        items=99,
        library_id=cfg.library.volume_id,
    )
    listed = [_candidate("still-unowned", "1"), _candidate("also-unowned", "2")]

    taken = scope.scoped(listed, owned=set(), limit=10)
    assert [item.identity for item in taken] == ["still-unowned", "also-unowned"]

    source = FakeSource("playlists", listed)
    result = run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-ktd11",
        staging=Path(cfg.paths.download_staging),
    )
    assert source.processed == ["still-unowned", "also-unowned"]
    assert result.shortfall is None
    assert store.read("playlists").cursor == "also-unowned"


def test_crash_debris_is_not_next_run_intake(cfg, tmp_path):
    staging = Path(cfg.paths.download_staging)
    staging.mkdir(parents=True, exist_ok=True)
    debris = staging / "aborted-download.flac"
    debris.write_bytes(b"partial")
    kept = staging / "finished-download.flac"
    kept.write_bytes(b"complete")

    registry = artifacts.ArtifactRegistry(cfg)
    registry.register(kept, run_id="run-5", source_id="labels", complete=True)

    eligible = registry.intake_eligible(staging.iterdir())
    leftover = registry.debris(staging.iterdir())

    assert kept in eligible
    assert debris in leftover
    assert debris not in eligible


def test_two_sources_in_one_run_share_one_importable_file(cfg):
    staging = Path(cfg.paths.download_staging)
    staging.mkdir(parents=True, exist_ok=True)
    store = watermarks.WatermarkStore(cfg)
    registry = artifacts.ArtifactRegistry(cfg)
    labels = FakeSource("labels", [_candidate("l1", "1")])
    playlists = FakeSource("playlists", [_candidate("p1", "1")])

    run.run_independent(
        [labels, playlists],
        owned=set(),
        limit=10,
        watermarks=store,
        artifacts=registry,
        run_id="run-6",
        staging=staging,
    )

    importables = list(staging.glob("*_synced.xml"))
    assert len(importables) == 1
    assert importables[0].name == "run-6_synced.xml"
    text = importables[0].read_text(encoding="utf-8")
    assert "l1" in text and "p1" in text


def test_external_marks_wait_for_local_output_and_recheck(cfg, tmp_path):
    output = tmp_path / "missing.xml"
    pending = [marks.PendingMark(target_id="pl-1", kind="prefix")]
    applied: list[str] = []

    with pytest.raises(CratekitError) as blocked:
        marks.apply_deferred(
            pending,
            local_output=output,
            recheck=lambda mark: True,
            apply=lambda mark: applied.append(mark.target_id),
        )
    assert blocked.value.cause.reason == "sync-marks-blocked"
    assert applied == []

    output.write_text("<COLLECTION/>", encoding="utf-8")
    marks.apply_deferred(
        pending,
        local_output=output,
        recheck=lambda mark: False,
        apply=lambda mark: applied.append(mark.target_id),
    )
    assert applied == []

    marks.apply_deferred(
        pending,
        local_output=output,
        recheck=lambda mark: True,
        apply=lambda mark: applied.append(mark.target_id),
    )
    assert applied == ["pl-1"]


def test_increment_opens_one_boundary_per_source(cfg):
    opened: list[str] = []

    class Boundary:
        def __init__(self, source_id: str) -> None:
            self.source_id = source_id

        def __enter__(self):
            opened.append(self.source_id)
            return self

        def __exit__(self, *exc):
            return False

    source = FakeSource("favorites", [_candidate("f1", "1")])
    run.increment(
        source,
        owned=set(),
        limit=10,
        watermarks=watermarks.WatermarkStore(cfg),
        artifacts=artifacts.ArtifactRegistry(cfg),
        run_id="run-7",
        staging=Path(cfg.paths.download_staging),
        boundary=lambda source_id: Boundary(source_id),
    )
    assert opened == ["favorites"]


def test_source_watermarks_are_library_scoped_and_coupled():
    for key in ("source_watermarks", "sync_artifacts"):
        entry = config.state_file(key)
        assert entry.root is config.StateRoot.LIBRARY
        assert entry.snapshot is config.SnapshotRole.COUPLED
        lock = config.state_file(f"{key}_lock")
        assert lock.snapshot is config.SnapshotRole.NEVER_RESTORED


def test_declared_sources_are_stable_ids_not_display_names():
    assert sources.DECLARED == ("favorites", "labels", "playlists")
    for source_id in sources.DECLARED:
        assert source_id.islower()
        assert " " not in source_id


def test_sync_all_queues_one_job_per_enabled_source(cfg):
    from cratekit.core import jobs
    from cratekit.sync import cli

    class Args:
        job = None

    class Ctx:
        args = Args()
        entry = type("E", (), {"handler_key": "sync.all", "name": "sync.all"})()

        def envelope(self, *, data, outcome=None):
            return data

    payload = cli.queue_all(Ctx())
    expected = sources.enabled(profiles.resolve(cfg.profile.name, cfg.modules.explicit))
    assert payload["summary"]["queued"] == len(expected)
    assert tuple(payload["summary"]["sources"]) == expected
    with jobs.open_store() as store:
        queued = list(jobs.list_jobs(store))
    assert len(queued) == len(expected)
    assert {job.payload["source_id"] for job in queued} == set(expected)
    run_ids = {job.payload.get("run_id") for job in queued}
    assert len(run_ids) == 1 and None not in run_ids, (
        "every source in one sync.all invocation must share one run id, or "
        "each increment writes its own intake file and R29 is broken"
    )
