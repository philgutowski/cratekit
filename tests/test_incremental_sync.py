"""U22: incremental sync per source, the watermark an audit, never a date floor.

KTD11: scope is most recent N deduped against what is owned, and a watermark
gates nothing, since a date floor once let a silent zero scope run mark a
playlist fully taken. R25 and R29: each source is its own job, a watermark
advances only on clean completion, a total lookup failure raises, crash debris
is never intake, and one run writes one importable file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from cratekit.sync import artifacts, marks, run, scope, sources, watermarks


@pytest.fixture
def cfg(tmp_path):
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    db_path = str(root / "db" / "master.db")
    library = {"root": str(root), "volume_id": "F1E2-D3C4", "db_path": db_path}
    built = config.from_dict({
        "schema_version": config.CURRENT_SCHEMA_VERSION, "library": library,
        "paths": {"download_staging": str(tmp_path / "staging")}, "profile": {"name": "full"},
    })
    config.save(built)
    config.reset_cache()
    return built


@pytest.fixture
def store(cfg) -> watermarks.WatermarkStore:
    return watermarks.WatermarkStore(cfg)


@pytest.fixture
def staging(cfg) -> Path:
    return Path(cfg.paths.download_staging)


@pytest.fixture
def registry(cfg) -> artifacts.ArtifactRegistry:
    return artifacts.ArtifactRegistry(cfg)


def _candidate(identity: str, recency: str) -> run.Candidate:
    return run.Candidate(identity=identity, recency=recency)


def _increment(cfg, source, run_id: str, *, call=run.increment, **given):
    """``call`` with the run's usual arguments, any of them given instead."""
    if "watermarks" not in given:
        given["watermarks"] = watermarks.WatermarkStore(cfg)
    if "artifacts" not in given:
        given["artifacts"] = artifacts.ArtifactRegistry(cfg)
    defaults = {"owned": set(), "limit": 10, "staging": Path(cfg.paths.download_staging)}
    return call(source, run_id=run_id, **{**defaults, **given})


class FakeSource:
    """A source the tests can script. Identity is a stable id, never a name."""

    def __init__(
        self, source_id: str, items: list[run.Candidate] | None = None, *,
        lookup_error: Exception | None = None, process_errors: dict[str, Exception] | None = None,
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
        self, candidate: run.Candidate, registry: artifacts.ArtifactRegistry, run_id: str
    ) -> None:
        error = self.process_errors.get(candidate.identity)
        if error is not None:
            raise error
        self.processed.append(candidate.identity)


class OfferingSource(FakeSource):
    """A source that offers for a decision, as ``LabelSource`` does, declared on the class."""

    acquires = False


def test_an_offering_source_writes_no_intake_file(cfg, store, staging, registry):
    """R-140. A completed offer is not an acquisition and must not claim one."""
    listed = [_candidate("r1", "3"), _candidate("r2", "2"), _candidate("r3", "1")]
    source = OfferingSource("labels", listed)
    parts = {"watermarks": store, "artifacts": registry, "staging": staging}
    result = _increment(cfg, source, "run-offer-1", **parts)
    assert result.shortfall is None
    assert result.processed == ("r1", "r2", "r3")
    # At the path the increment would have used, since an empty directory proves nothing.
    target = run.intake_path(staging, "run-offer-1")
    assert not target.exists()
    assert registry.intake_eligible([target]) == []


def test_an_offering_run_leaves_the_source_watermark_unset(cfg, store):
    """Read back from the store, because an unadvanced cursor is the claim."""
    source = OfferingSource("labels", [_candidate("r1", "3")])
    _increment(cfg, source, "run-offer-2", watermarks=store)
    assert store.read("labels") is None


def test_an_acquiring_source_still_writes_the_intake_file_and_advances(cfg, store, staging):
    """The default is pinned beside the new branch, so it cannot drift silently."""
    source = FakeSource("playlists", [_candidate("p1", "3"), _candidate("p2", "2")])
    assert not hasattr(source, "acquires"), "the double must not declare the attribute"
    result = _increment(cfg, source, "run-acquire-1", watermarks=store, staging=staging)
    assert result.shortfall is None
    target = run.intake_path(staging, "run-acquire-1")
    assert target.exists()
    assert "p1" in target.read_text(encoding="utf-8")
    assert store.read("playlists").cursor == "p1"


def test_one_run_records_only_the_acquiring_source_of_a_mixed_pair(cfg, store, staging):
    """One intake file, and an offer does not get to put its identities in it."""
    staging.mkdir(parents=True, exist_ok=True)
    acquiring = FakeSource("playlists", [_candidate("p1", "1")])
    offering = OfferingSource("labels", [_candidate("l1", "1")])
    results = _increment(
        cfg, [acquiring, offering], "run-mixed", call=run.run_independent, watermarks=store,
        staging=staging)
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


def test_errors_leave_the_watermark_unchanged_and_report_the_shortfall(cfg, store):
    listed = [_candidate("a", "3"), _candidate("b", "2")]
    source = FakeSource("labels", listed, process_errors={"b": RuntimeError("provider 429")})
    result = _increment(cfg, source, "run-1", watermarks=store)
    assert store.read("labels") is None
    assert result.errors
    assert result.shortfall is not None
    assert "b" in result.shortfall or result.errors


def test_every_lookup_failing_raises_and_does_not_advance(cfg, store):
    source = FakeSource("favorites", lookup_error=run.LookupFailure("every listing call failed"))
    with pytest.raises(CratekitError) as excinfo:
        _increment(cfg, source, "run-2", watermarks=store)
    assert excinfo.value.cause.reason == "sync-source-lookups-failed"
    assert store.read("favorites") is None


def test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited(cfg):
    """R-704: the source that caught the provider's error decides, the increment relays.
    A rate limit is retryable and says so; every other failure stays permanent."""

    def refusal(failure: run.LookupFailure):
        with pytest.raises(CratekitError) as excinfo:
            _increment(cfg, FakeSource("labels", lookup_error=failure), "run-r704")
        return excinfo.value
    plain = refusal(run.LookupFailure("labels down")).cause
    assert plain.reason == "sync-source-lookups-failed"
    assert plain.retryable is False
    assert plain.remediation.steps == ("retry this source when the provider is reachable",)
    assert "rate_limited" not in plain.detail
    failure = run.LookupFailure("TooManyRequests: Album unavailable", rate_limited=True)
    limited = refusal(failure)
    assert limited.__cause__ is failure
    cause = limited.cause
    assert cause.reason == "sync-source-lookups-failed"
    assert cause.retryable is True
    assert cause.remediation.remedy is Remedy.RESUME_JOB
    assert cause.detail == {"source_id": "labels", "rate_limited": True}
    assert "rate limited" in cause.message
    assert "TooManyRequests: Album unavailable" in cause.message
    assert watermarks.WatermarkStore(cfg).read("labels") is None


def test_one_source_failing_does_not_block_the_other(cfg, store, staging):
    failing = FakeSource("labels", lookup_error=run.LookupFailure("labels down"))
    ok = FakeSource("playlists", [_candidate("p1", "9")])
    results = _increment(
        cfg, [failing, ok], "run-3", call=run.run_independent, watermarks=store, staging=staging)
    assert isinstance(results["labels"], CratekitError)
    assert isinstance(results["playlists"], run.IncrementResult)
    assert store.read("labels") is None
    assert store.read("playlists") is not None
    assert store.read("playlists").cursor == "p1"


def test_a_rerun_after_a_clean_sync_processes_only_unowned_items(cfg, store, staging, registry):
    first = FakeSource("playlists", [_candidate("old", "1"), _candidate("mid", "2")])
    parts = {"watermarks": store, "artifacts": registry, "staging": staging}
    first_result = _increment(cfg, first, "run-4a", **parts)
    assert first_result.shortfall is None
    assert store.read("playlists") is not None
    owned = set(first.processed)
    relisted = [_candidate("new", "3"), _candidate("old", "1"), _candidate("mid", "2")]
    second = FakeSource("playlists", relisted)
    second_result = _increment(cfg, second, "run-4b", owned=owned, **parts)
    assert second.processed == ["new"]
    assert second_result.processed == ("new",)


def test_a_watermark_does_not_empty_the_scope_of_unowned_items(cfg, store):
    """KTD11. The silent zero-scope failure used the watermark as a date floor."""
    store.advance("playlists", cursor="zzz", items=99, library_id=cfg.library.volume_id)
    listed = [_candidate("still-unowned", "1"), _candidate("also-unowned", "2")]
    taken = scope.scoped(listed, owned=set(), limit=10)
    assert [item.identity for item in taken] == ["still-unowned", "also-unowned"]
    source = FakeSource("playlists", listed)
    result = _increment(cfg, source, "run-ktd11", watermarks=store)
    assert source.processed == ["still-unowned", "also-unowned"]
    assert result.shortfall is None
    assert store.read("playlists").cursor == "also-unowned"


def test_crash_debris_is_not_next_run_intake(cfg, staging, registry, tmp_path):
    staging.mkdir(parents=True, exist_ok=True)
    debris = staging / "aborted-download.flac"
    debris.write_bytes(b"partial")
    kept = staging / "finished-download.flac"
    kept.write_bytes(b"complete")
    registry.register(kept, run_id="run-5", source_id="labels", complete=True)
    eligible = registry.intake_eligible(staging.iterdir())
    leftover = registry.debris(staging.iterdir())
    assert kept in eligible
    assert debris in leftover
    assert debris not in eligible


def test_two_sources_in_one_run_share_one_importable_file(cfg, store, staging, registry):
    staging.mkdir(parents=True, exist_ok=True)
    labels = FakeSource("labels", [_candidate("l1", "1")])
    playlists = FakeSource("playlists", [_candidate("p1", "1")])
    parts = {"watermarks": store, "artifacts": registry, "staging": staging}
    _increment(cfg, [labels, playlists], "run-6", call=run.run_independent, **parts)
    importables = list(staging.glob("*_synced.xml"))
    assert len(importables) == 1
    assert importables[0].name == "run-6_synced.xml"
    text = importables[0].read_text(encoding="utf-8")
    assert "l1" in text and "p1" in text


def test_external_marks_wait_for_local_output_and_recheck(cfg, tmp_path):
    output = tmp_path / "missing.xml"
    pending = [marks.PendingMark(target_id="pl-1", kind="prefix")]
    applied: list[str] = []

    def deferred(still_wanted: bool) -> None:
        marks.apply_deferred(
            pending, local_output=output, recheck=lambda mark: still_wanted,
            apply=lambda mark: applied.append(mark.target_id))
    with pytest.raises(CratekitError) as blocked:
        deferred(True)
    assert blocked.value.cause.reason == "sync-marks-blocked"
    assert applied == []
    output.write_text("<COLLECTION/>", encoding="utf-8")
    deferred(False)
    assert applied == []
    deferred(True)
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
    _increment(cfg, source, "run-7", boundary=lambda source_id: Boundary(source_id))
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


# U64: the playlists cursor is a set of identifiers


def test_recording_swept_ids_unions_them_in_first_seen_order(cfg, store):
    lib = cfg.library.volume_id
    store.record_swept("playlists", ["pl-a", "pl-b"], library_id=lib)
    mark = store.record_swept("playlists", ["pl-b", "pl-c"], library_id=lib)
    assert mark is not None
    assert mark.swept == ("pl-a", "pl-b", "pl-c")
    assert (mark.cursor, mark.items) == ("pl-c", 3)
    assert store.read("playlists").swept == ("pl-a", "pl-b", "pl-c")


def test_recording_nothing_swept_records_nothing(cfg, store):
    """R-135. A pass that completed no playlist is not a clean completion."""
    assert store.record_swept("playlists", [], library_id=cfg.library.volume_id) is None
    assert not store.path.exists()
    store.record_swept("playlists", ["pl-a"], library_id=cfg.library.volume_id, now="t1")
    kept = store.record_swept("playlists", [], library_id=cfg.library.volume_id, now="t2")
    assert kept is not None and kept.recorded == "t1"


def test_a_record_with_no_swept_list_writes_none_and_reads_as_empty(cfg, store):
    """The other sources' records are unchanged by the new field."""
    store.advance("labels", cursor="r1", items=1, library_id=cfg.library.volume_id)
    assert "swept" not in store.path.read_text(encoding="utf-8")
    assert store.read("labels").swept == ()


@pytest.mark.parametrize("swept", ["pl-a", ["pl-a", ""], ["pl-a", 7]])
def test_a_swept_list_that_is_not_identifiers_is_unusable(cfg, store, swept):
    import json
    store.record_swept("playlists", ["pl-a"], library_id=cfg.library.volume_id)
    document = json.loads(store.path.read_text(encoding="utf-8"))
    document["sources"]["playlists"]["swept"] = swept
    store.path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(CratekitError) as caught:
        store.read("playlists")
    assert caught.value.cause.reason == "sync-watermark-unusable"


def test_the_playlist_exclusions_in_the_order_a_person_is_told():
    from cratekit.favorites import placeholders
    from cratekit.label.catalogue import AccountPlaylist
    from cratekit.sync import playlists

    def decide(name, playlist_id="pl-1", tracks=None, recorded=(), in_flight=()):
        return playlists.exclusion(
            AccountPlaylist(playlist_id, name, tracks),
            recorded=frozenset(recorded), in_flight=frozenset(in_flight))
    E = playlists.Excluded
    assert decide("Warmup") is None
    assert decide("Warmup", tracks=3) is None
    assert decide(playlists.SWEPT_PREFIX + "Warmup", recorded={"pl-1"}) is E.SWEPT
    assert decide("Warmup", recorded={"pl-1"}, in_flight={"pl-1"}) is E.RECORDED
    assert decide(placeholders.placeholder_name("2026-Q1"), in_flight={"pl-1"}) is E.PLACEHOLDER
    assert decide("Warmup", in_flight={"pl-1"}, tracks=0) is E.IN_FLIGHT
    assert decide("Warmup", tracks=0) is E.EMPTY
    assert decide("Warmup", recorded={"pl-2"}, in_flight={"pl-2"}) is None
    # A TITLE IN THE CURSOR IS NOT AN IDENTIFIER IN IT.
    assert decide("Warmup", recorded={"Warmup"}) is None
    assert decide("downloaded Warmup") is None
    assert decide("DOWNLOADEDWarmup") is None


def test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule():
    """R-361: label batch debris is any name ending ` LIBRARY`, case sensitive."""
    from cratekit.label.catalogue import AccountPlaylist
    from cratekit.sync import playlists

    def decide(name, playlist_id="pl-1", tracks=3, recorded=(), in_flight=()):
        return playlists.exclusion(
            AccountPlaylist(playlist_id, name, tracks),
            recorded=frozenset(recorded), in_flight=frozenset(in_flight))
    E = playlists.Excluded
    assert playlists.LIBRARY_PLAYLIST_SUFFIX == " LIBRARY"
    assert str(E.LABEL_DEBRIS) == "label-debris"
    assert decide("Colorize LIBRARY") is E.LABEL_DEBRIS
    # Case exactly, since the batch never writes another case and a person might.
    assert decide("Colorize Library") is None
    assert decide("Colorize library") is None
    # The swept prefix is decided first, so already swept debris keeps its reason.
    assert decide(playlists.SWEPT_PREFIX + "Colorize LIBRARY") is E.SWEPT
    # The accepted collision: a person's playlist named this way is excluded too.
    assert decide("My Night LIBRARY") is E.LABEL_DEBRIS
    assert decide("Colorize 2026") is None
    # A suffix, not a substring: the leading space is part of the rule.
    assert decide("ColorizeLIBRARY") is None
    assert decide("LIBRARY Colorize") is None
    assert decide("Colorize LIBRARY 2") is None
    # Ahead of the cursor and the open jobs, in the order a person is told.
    assert decide("Colorize LIBRARY", recorded={"pl-1"}, in_flight={"pl-1"}) is E.LABEL_DEBRIS
    assert decide("Colorize LIBRARY", tracks=0) is E.LABEL_DEBRIS
    assert playlists.is_library_debris("") is False
    assert playlists.is_library_debris(None) is False


# R-263: a source that records no cursor is not a source that never ran


def _row(cfg, source_id: str) -> dict[str, str]:
    rows = [row for row in watermarks.status_rows(cfg) if row["source_id"] == source_id]
    assert len(rows) == 1, rows
    return rows[0]


def test_a_clean_labels_sweep_is_not_reported_as_never_having_run(cfg):
    """The cost, driven: a sweep that succeeds, then the row doctor prints."""
    source = OfferingSource("labels", [_candidate("r1", "3"), _candidate("r2", "2")])
    result = _increment(cfg, source, "run-r263")
    assert result.shortfall is None
    assert result.processed == ("r1", "r2")
    row = _row(cfg, "labels")
    assert row["state"] == "unrecorded"
    assert "no clean increment has completed" not in row["detail"]
    assert "crate label sync" in row["detail"]


def test_the_labels_spec_agrees_with_the_source_that_offers():
    """The declaration on the spec and the one on the source are one fact."""
    from cratekit.label import sweep
    by_id = {spec.source_id: spec for spec in sources.SPECS}
    assert sweep.LabelSource.acquires is False
    assert by_id["labels"].no_cursor


def test_favorites_is_not_reported_as_never_having_run(cfg):
    """METHOD's fifth pattern, one source over: nothing records this cursor."""
    row = _row(cfg, "favorites")
    assert row["state"] == "unrecorded"
    assert "no clean increment has completed" not in row["detail"]


def test_a_source_that_records_a_cursor_still_reports_never_then_completed(cfg):
    """The third state is declared per source, never granted to the absence."""
    assert sources.SPECS[-1].source_id == "playlists"
    assert sources.SPECS[-1].no_cursor is None
    row = _row(cfg, "playlists")
    assert row["state"] == "never"
    assert row["detail"] == "no clean increment has completed"
    watermarks.WatermarkStore(cfg).record_swept("playlists", ["pl-1"], library_id="F1E2-D3C4")
    row = _row(cfg, "playlists")
    assert row["state"] == "completed"
    assert "cursor pl-1" in row["detail"]


def test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion(cfg):
    """A record an earlier build wrote no longer moves, and the row says so."""
    watermarks.WatermarkStore(cfg).advance(
        "labels", cursor="old-release", items=4, library_id="F1E2-D3C4",
        now="2026-08-01T00:00:00+00:00")
    row = _row(cfg, "labels")
    assert row["state"] == "unrecorded"
    assert "crate label sync" in row["detail"]
    assert "2026-08-01T00:00:00+00:00" in row["detail"]
    assert "no longer moves" in row["detail"]


def test_doctor_prints_the_labels_row_it_is_given(cfg):
    """The consumer, driven, so the finding a person reads carries the fix."""
    from cratekit.cli import doctor
    found = {f.key: f for f in doctor._source_findings(cfg)}
    labels = found["source.labels.watermark"]
    assert "no clean increment has completed" not in labels.detail
    assert "crate label sync" in labels.detail
    assert found["source.playlists.watermark"].detail == "no clean increment has completed"
