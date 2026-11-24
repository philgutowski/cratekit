"""U55: both adopt verbs driving their own queued work, end to end, item by item.

The apply needs a cut-over library, recorded as ``tests/test_tree_writer.py``
does; properties of one approved apply are asserted over one drive. D1 applies.
"""

from __future__ import annotations

import dataclasses
import json
import sqlite3
from dataclasses import replace
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import apply_cli, artifacts, collection, scan_cli
from cratekit.adopt import placements as adopt_placements
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.cause import refuse
from cratekit.core.exit_codes import ExitCode
from cratekit.write.routing_pass import destination
from tests import adopt_fixtures
from tests._taxonomy_parses import counted, renamed_in_place, rewrite_keeping_time, unique
from tests.cli_drive import approve_and_queue, drive, drive_human
from tests.test_adoption import _bucket_and_genre
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION

#: The shipped taxonomy's tree, resolved once so the cutover and the plan agree.
DECLARED = taxonomy.default_taxonomy()
APPLY = ["adopt", "apply"]
GATE = "adopt.apply.approve"


# ── Fixtures ──


@pytest.fixture(autouse=True)
def _reader_cache():
    collection.reset_cache()
    yield
    collection.reset_cache()


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _platform_seams(monkeypatch):
    """What this machine cannot speak for on a temporary library; the guards are
    proved in ``tests/test_rb_writer_db.py``."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: False)
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 0},
    )
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: RECORDED_APP_VERSION)
    # The capture's check needs the key; compensated at the fixture, not the verifier.
    real_integrity_ok = rb_writer.integrity_ok
    monkeypatch.setattr(
        rb_writer, "integrity_ok", lambda target, **kwargs: real_integrity_ok(target, unlock=False)
    )


@pytest.fixture
def library(tmp_path, monkeypatch):
    root = tmp_path / "library"
    (root / "db").mkdir(parents=True)
    (root / "Music").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    return root


def _tracks() -> tuple[adopt_fixtures.Track, ...]:
    _bucket, genre = _bucket_and_genre(DECLARED)
    return (
        adopt_fixtures.Track("r-one", "one.flac", genre),
        adopt_fixtures.Track("r-two", "two.flac", genre),
        adopt_fixtures.Track("r-missing", "absent.flac", genre, on_disk=False),
    )


def _configured(root: Path, **library: object) -> config.Config:
    data = valid_data(
        root,
        rekordbox={"pinned_app_version": RECORDED_APP_VERSION, "validated_on": "2026-08-01"},
    )
    data["library"].update(library)
    return config.from_dict(data)


@pytest.fixture
def machine(library, monkeypatch):
    """A set-up machine, saved to disk since the real dispatcher loads configuration."""
    resolved = _configured(library)
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, _tracks())
    collection.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: lambda _path: resolved.library.volume_id
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    return resolved


def _record_cutover(cfg: config.Config, root_id: str, on: date = date(2026, 9, 2)) -> None:
    tree_registry.record_cutover(
        cfg,
        DECLARED.tree.id,
        root_id=root_id,
        on=on,
        source=tree_registry.DerivationSource.TAXONOMY,
    )


@pytest.fixture
def cut_over(machine):
    """A library whose tree the registry records as database native, so the write runs."""
    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        handle.session.commit()
        root_id = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    _record_cutover(machine, root_id)
    return machine


def _resume(job_id: str) -> list[str]:
    """The command line the job driver would spawn, through the real ``argv_for``."""
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def _job(handler_key: str):
    with jobs.open_store() as store:
        held = [job for job in jobs.list_jobs(store) if job.handler_key == handler_key]
    assert len(held) == 1, f"expected exactly one {handler_key} job, found {len(held)}"
    return held[0]


def _scan_job():
    return _job(registry.entry("adopt.scan").handler_key)


def _applied() -> str:
    """Approve and queue an apply, drive its resume to OK, and answer the job id."""
    _run_id, job_id = approve_and_queue(APPLY, GATE)
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    return job_id


def _worker(job_id: str, job_of=lambda job: job):
    """Run the apply worker directly on this job's one item, as the driver would."""
    handler = handlers.resolve(registry.entry("adopt.apply").handler_key)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    return handler(job_of(job), item, jobs.frozen_config(job))


def _memberships(cfg: config.Config) -> dict[str, list[str]]:
    """What the database holds, read through a fresh handle rather than the report."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        found: dict[str, list[str]] = {}
        for row in handle.get_playlist():
            songs = handle.get_playlist_songs(PlaylistID=str(row.ID))
            members = [str(entry.ContentID) for entry in songs]
            if members:
                found[str(row.Name)] = sorted(members)
        return found
    finally:
        rb_writer.close_db(handle)


# ── Both keys are bound ──


def test_both_adopt_keys_resolve_to_a_worker():
    """The R-203 half this unit closes, asserted against the table rather than prose."""
    for name in ("adopt.scan", "adopt.apply"):
        key = registry.entry(name).handler_key
        assert handlers.is_known(key), f"{key} still has no worker"
        assert handlers.unbound_reason(key) is None
        assert callable(handlers.resolve(key))


# ── The scan ──


def test_a_scan_queues_one_item_per_live_row_and_drives_them_all(machine, monkeypatch):
    """Pending to done through the real resume argv, counted from the artifacts, on the
    frozen configuration (KTD9), the taxonomy parsed once per census (U247)."""
    text = unique(taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
    _active_copy(machine, text)
    parses = counted(monkeypatch)
    seen: list[str] = []
    real = artifacts.produced

    def recording(cfg, job, item, report):
        seen.append(str(jobs.store_dir(cfg)))
        return real(cfg, job, item, report)

    monkeypatch.setattr(scan_cli.artifacts, "produced", recording)

    code, queued = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), queued
    job = _scan_job()
    frozen_root = str(jobs.store_dir(jobs.frozen_config(job)))
    with jobs.open_store() as store:
        assert {item.item_id for item in jobs.items(store, job.job_id)} == {
            "r-one",
            "r-two",
            "r-missing",
            *adopt_fixtures.BASELINE_CONTENT_IDS,
        }

    code, resumed = drive(["adopt", "scan", "--job", job.job_id])
    assert code == int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        assert jobs.get(store, job.job_id).state is jobs.JobState.SUCCEEDED
        assert all(item.state is jobs.ItemState.DONE for item in jobs.items(store, job.job_id))

    reports = {report["content_id"]: report for report in artifacts.committed(machine, job.job_id)}
    assert reports["r-one"]["readability"] == str(adopt_scan.Readability.READABLE)
    assert reports["r-one"]["disposition"] == str(adopt_scan.Disposition.ROUTE)
    assert reports["r-missing"]["readability"] == str(adopt_scan.Readability.MISSING)
    assert reports["r-missing"]["disposition"] == str(adopt_scan.Disposition.EXCLUDED)

    census = resumed["data"]["progress"]["census"]
    assert census["categories"][str(adopt_scan.Readability.READABLE)] == 2
    assert census["categories"][str(adopt_scan.Readability.MISSING)] == 1
    assert set(census["categories"]) == {str(member) for member in adopt_scan.Readability}, (
        "a summary listing only the categories it saw cannot tell 'none here' "
        "from 'this build does not look'"
    )
    counted_rows = sum(census["categories"].values())
    assert counted_rows == len(artifacts.committed(machine, job.job_id))
    assert counted_rows == resumed["data"]["progress"]["total"]

    assert seen and set(seen) == {frozen_root}
    assert counted_rows >= 3
    assert parses.of(text) == 1, (
        f"{counted_rows} rows parsed the active copy {parses.of(text)} times"
    )


@pytest.mark.parametrize("tombstones", [False, True])
def test_an_empty_library_queues_nothing_and_says_so(machine, tombstones):
    """The honest zero: nothing queued, still success; the baseline rows are removed first."""
    adopt_fixtures.build(machine, ())
    _empty_the_collection(machine)
    if tombstones:
        _add_tombstone(machine)

    code, envelope = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    expected = "collection-all-tombstones" if tombstones else "collection-empty"
    assert [warning["code"] for warning in envelope["warnings"]] == [expected]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


@pytest.mark.parametrize("edit", ["deleted", "tombstoned"])
def test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item(machine, edit):
    """A row deleted since the queueing fails its own item with its own slug."""
    drive(["adopt", "scan"])
    job = _scan_job()

    if edit == "deleted":
        _sql(machine, "DELETE FROM djmdContent WHERE ID = ?", ("r-two",))
    else:
        _sql(machine, "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", ("r-two",))

    code, _resumed = drive(["adopt", "scan", "--job", job.job_id])
    assert code != int(ExitCode.OK)
    with jobs.open_store() as store:
        items = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert items["r-two"].state is jobs.ItemState.FAILED
    assert items["r-one"].state is jobs.ItemState.DONE
    assert items["r-two"].cause is not None
    assert items["r-two"].cause.reason == "adopt-item-absent", "a removed track read as a defect"


@pytest.mark.parametrize("verb", ["adopt.scan", "adopt.apply"])
def test_a_job_queued_with_no_items_refuses_rather_than_reporting_success(machine, verb):
    """A zero item job would be SUCCEEDED for work never done, so it refuses."""
    payload: dict = {"tree": DECLARED.tree.id}
    argv = ["adopt", "scan"]
    if verb == "adopt.apply":
        plan = apply_cli.current_plan(machine, DECLARED)
        run_id = _record_decision(APPLY, GATE)
        payload = {
            "tree": plan.tree,
            "digest": plan.digest(),
            apply_cli.ACTOR_KEY: "a-person",
            jobs.GATE_RUN_KEY: run_id,
        }
        argv = ["--run", run_id, *APPLY]
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store, handler_key=registry.entry(verb).handler_key, payload=payload, cfg=machine
        )
    code, envelope = drive([*argv, "--job", job.job_id])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "internal-error"
    assert "no items" in envelope["cause"]["message"]


def test_a_configured_volume_rewrite_reaches_the_census(machine, tmp_path):
    """S1's prefix map reaches the census; the older root is a temporary directory (R1)."""
    older = str(tmp_path / "an-older-root")
    adopt_fixtures.build(machine, ())
    _empty_the_collection(machine)
    _insert_under(machine, older, "r-elsewhere", _tracks()[0].genre)
    (Path(machine.library.root) / "Music" / "one.flac").write_bytes(b"\x00" * 64)

    found = {track.content_id: track for track in apply_cli.census(machine, DECLARED)}
    assert found["r-elsewhere"].readability is adopt_scan.Readability.UNMAPPED

    mapped = _configured(
        Path(machine.library.root), location_prefix_map=[{"from": older, "to": "{library.root}"}]
    )
    collection.reset_cache()
    resolved = {track.content_id: track for track in apply_cli.census(mapped, DECLARED)}
    assert resolved["r-elsewhere"].readability is adopt_scan.Readability.READABLE, (
        "the volume rewrite was ignored"
    )
    assert resolved["r-elsewhere"].disposition is adopt_scan.Disposition.ROUTE


# ── The apply ──


def test_an_apply_over_a_cut_over_library_writes_the_memberships(cut_over, monkeypatch):
    """The happy path, read back from the database rather than from the report.

    No tag and every byte kept (R16), the actor in the payload (R34), one capture
    per job (KTD6), a second run adds no row, and no favourites class refuses (U132).
    """
    from cratekit.core import active_taxonomy
    from cratekit.write import genre_favorites, trees

    plan = apply_cli.current_plan(cut_over, DECLARED)
    by_identifier = adopt_apply.membership_plan(plan.applicable(), DECLARED)
    by_location = apply_cli.membership_locations(plan.applicable(), DECLARED)
    assert set(by_identifier) == set(by_location)
    assert by_identifier != by_location

    root, prefix_map = cut_over.library.root, collection.prefix_rules(cut_over)
    index = trees.index_active_rows(
        collection.read_collection(cut_over), root=root, prefix_map=prefix_map
    )
    wanted = [value for values in by_identifier.values() for value in values]
    matched = trees.match_indexed_rows(wanted, index, root=root, prefix_map=())
    assert wanted and not any(match.outcome is trees.MatchOutcome.MATCHED for match in matched), (
        "content identifiers matched a location index, so the seam claim is wrong"
    )

    wanted = [value for values in by_location.values() for value in values]
    matched = trees.match_indexed_rows(wanted, index, root=root, prefix_map=prefix_map)
    assert all(match.outcome is trees.MatchOutcome.MATCHED for match in matched)

    music = Path(cut_over.library.root) / "Music"
    before = {path: path.read_bytes() for path in sorted(music.glob("*.flac"))}
    assert before, "the fixture wrote no files, so this assertion is empty"

    _run_id, job_id = approve_and_queue(APPLY, GATE)
    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == [
            apply_cli.current_plan(cut_over, DECLARED).digest()
        ]
        assert jobs.get(store, job_id).payload[apply_cli.ACTOR_KEY] == "a-person"

    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.SUCCEEDED

    written = _memberships(cut_over)
    assert written, "the apply reported success and the database holds no membership"
    assert sorted(row for rows in written.values() for row in rows) == ["r-one", "r-two"]

    ledger = adopt_apply.read(cut_over)
    plan = apply_cli.current_plan(cut_over, DECLARED)
    assert ledger.entry_ids() == {entry.entry_id for entry in plan.applicable()}

    assert {path: path.read_bytes() for path in sorted(music.glob("*.flac"))} == before
    assert artifacts.committed(cut_over, job_id)[-1]["actor"] == "a-person"
    captures = sorted(p for p in rb_writer.snapshot_root(cut_over).iterdir() if p.is_dir())
    assert len(captures) == 1, captures

    collection.reset_cache()
    produced = _worker(job_id)
    assert _memberships(cut_over) == written
    report = json.loads(produced.staged.read_text(encoding="utf-8"))
    assert report["added"] == 0
    assert report["already_present"] == len([row for rows in written.values() for row in rows])

    real = active_taxonomy.load

    def narrowed(cfg):
        declared = real(cfg)
        kept = tuple(e for e in declared.sub_classes if e.signal != taxonomy.SIGNAL_PLAYLIST)
        assert len(kept) == len(declared.sub_classes) - 1
        return dataclasses.replace(declared, sub_classes=kept)

    monkeypatch.setattr(active_taxonomy, "load", narrowed)
    collection.reset_cache()
    report = json.loads(_worker(job_id).staged.read_text(encoding="utf-8"))
    assert report["added"] == 0
    assert report["favorites"]["cause"] == genre_favorites.CLASS_UNDECLARED
    (note,) = apply_cli.favorites_warnings({"favorites": report["favorites"]})
    assert note["code"] == genre_favorites.CLASS_UNDECLARED


def test_an_apply_records_the_node_of_each_destination_it_filed_into(cut_over):
    """R-1991: a folder renamed after an adoption is still read as its genre's.

    The record is read back from the state file and each node from a fresh
    handle, so the playlist it names is the one bearing the destination's names.
    """
    from cratekit.core import convergence

    plan = apply_cli.current_plan(cut_over, DECLARED)
    wanted = {(entry.bucket, entry.sub) for entry in plan.applicable()}
    assert wanted, "the fixture plans nothing, so this assertion is empty"
    assert convergence.read(cut_over).tree(plan.tree) is None

    _applied()

    record = convergence.read(cut_over).tree(plan.tree)
    assert record is not None and not record.unconverged
    assert {(entry.bucket, entry.sub) for entry in record.nodes} == wanted
    handle = rb_writer.open_db(rb_writer.live_db_path(cut_over), unlock=False, cfg=cut_over)
    try:
        for entry in record.nodes:
            playlist = handle.get_playlist(ID=entry.playlist_id)
            folder = handle.get_playlist(ID=entry.folder_id)
            assert str(playlist.ParentID) == entry.folder_id
            assert (str(folder.Name), str(playlist.Name)) == destination(
                DECLARED, entry.bucket, entry.sub
            )
    finally:
        rb_writer.close_db(handle)


def test_planned_destinations_name_each_pair_once_and_skip_what_names_none(monkeypatch):
    """A pair two destinations share is recorded as neither; a vocal addition by its
    vocal sub; a destination the taxonomy no longer declares is skipped, as the
    membership mapping skips it, never raised before the write."""
    entries = [
        SimpleNamespace(bucket="one", sub="high"),
        SimpleNamespace(bucket="two", sub="high"),
        SimpleNamespace(bucket="two", sub="low"),
        SimpleNamespace(bucket="gone", sub="high"),
    ]
    sung = [SimpleNamespace(bucket="two", sub="low", vocal_sub="with_vox")]
    plan = SimpleNamespace(applicable=lambda: entries, vocal_additions=lambda: sung)
    names = {
        ("one", "high"): ("Shared", "High"),
        ("two", "high"): ("Shared", "High"),
        ("two", "low"): ("Two", "Low"),
        ("two", "with_vox"): ("Two", "with vox"),
    }

    def named(_declared, bucket, sub):
        return names[(bucket, sub)]

    monkeypatch.setattr(apply_cli, "destination", named)
    assert apply_cli.planned_destinations(plan, DECLARED) == {
        ("Two", "Low"): ("two", "low"),
        ("Two", "with vox"): ("two", "with_vox"),
    }


def test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run(cut_over):
    """A ledger holding every entry, as a kill leaves it, still gets its memberships."""
    plan = apply_cli.current_plan(cut_over, DECLARED)
    for entry in plan.applicable():
        adopt_apply.mark_applied(
            cut_over,
            adopt_apply.AppliedEntry(
                entry_id=entry.entry_id,
                tree=entry.tree,
                content_id=entry.content_id,
                bucket=entry.bucket,
                sub=entry.sub,
                actor="a-person",
                digest=plan.digest(),
                applied="2026-09-02T00:00:00Z",
            ),
        )

    job_id = _applied()
    report = artifacts.committed(cut_over, job_id)[-1]
    assert report["gathered"] == [], "the loop had nothing outstanding, as this test needs"
    assert report["added"] == 2, "memberships came from the run, not the plan"
    assert _memberships(cut_over)


@pytest.mark.parametrize("root_id", [None, "no-such-root"])
def test_an_uncut_library_marks_nothing_and_the_job_stays_resumable(machine, root_id):
    """An unrecorded registry is the bridge, and one naming another root refuses too;
    both are ``tree-unconverged``, told apart by the detail."""
    if root_id is not None:
        _record_cutover(machine, root_id)
    _run_id, job_id = approve_and_queue(APPLY, GATE)
    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert resumed["cause"]["inner"]["reason"] == "tree-unconverged"
    detail = resumed["cause"]["inner"]["detail"]
    if root_id is None:
        assert detail["tree_id"] == DECLARED.tree.id
    else:
        assert detail["root_id"] == root_id, "only the detail tells them apart"
    assert adopt_apply.read(machine).entry_ids() == frozenset(), (
        "the ledger marked unplaced entries"
    )
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.FAILED


def test_a_plan_with_nothing_applicable_queues_nothing(machine):
    """The apply's honest zero. The gate still fires; the queue stays empty."""
    _empty_the_collection(machine)
    _sql(
        machine,
        "INSERT INTO djmdContent (ID, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES (?, ?, 0, ?, ?)",
        ("r-blank", "file://localhost/blank.flac", "2026-09-02", "2026-09-02"),
    )

    run_id = _record_decision(APPLY, GATE)
    code, envelope = drive(["--run", run_id, *APPLY])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op", envelope
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["adoption-nothing-applicable"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_collection_that_moved_after_approval_refuses_rather_than_applying(cut_over):
    """R34 at the worker as well as the gate; an unattributed payload writes no row."""
    _run_id, job_id = approve_and_queue(APPLY, GATE)

    def unauthorised(job):
        return replace(job, payload={**job.payload, apply_cli.ACTOR_KEY: ""})

    with pytest.raises(Exception):
        _worker(job_id, unauthorised)
    assert _memberships(cut_over) == {}, "an unauthorised run wrote rows"

    _sql(cut_over, "DELETE FROM djmdContent WHERE ID = ?", ("r-two",))
    with pytest.raises(Exception) as excinfo:
        _worker(job_id)
    assert excinfo.value.cause.reason == "decision-stale"
    assert adopt_apply.read(cut_over).entry_ids() == frozenset()


def test_an_interrupted_job_exits_with_its_own_cause_and_not_ok(machine):
    """R-225: a census or apply stopped by a signal is CANCELLED and exits non zero."""
    drive(["adopt", "scan"])
    scan_id = _scan_job().job_id
    run_id, apply_id = approve_and_queue(APPLY, GATE)

    for job_id, argv in (
        (scan_id, ["adopt", "scan", "--job", scan_id]),
        (apply_id, ["--run", run_id, *APPLY, "--job", apply_id]),
    ):
        with jobs.open_store() as store:
            jobs.cancel(store, job_id, stage="interrupted")
            cancelled = jobs.get(store, job_id)
        assert cancelled.state is jobs.JobState.CANCELLED
        assert cancelled.cause is not None, "the fixture built a cause-free cancel"

        code, envelope = drive(argv)
        assert code != int(ExitCode.OK), "an interrupt reported as finished"
        assert envelope["cause"]["reason"] == cancelled.cause.reason


def test_a_parked_adoption_leaves_blocked_and_non_zero(machine, monkeypatch):
    """R-290 for ``adopt apply``, which ``tests/test_job_outcome.py`` cannot drive and
    names; it fails if this is removed."""

    def parks(job, item, cfg):
        raise jobs.Parked(refuse("provider-blocked", "the run must stop", origin=("test",)).cause)

    run_id, job_id = approve_and_queue(APPLY, GATE)
    monkeypatch.setattr(handlers, "resolve", lambda _key: parks)

    code, envelope = drive(["--run", run_id, *APPLY, "--job", job_id])

    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.BLOCKED, envelope
    assert envelope["outcome"] == "blocked", envelope
    assert code != int(ExitCode.OK), envelope
    assert envelope["cause"]["reason"] == "provider-blocked"


def test_an_apply_whose_entries_failed_raises_rather_than_reporting_success(cut_over, monkeypatch):
    """``jobs.drive`` fails only on a raise, so the worker raises after committing."""
    real = apply_cli.apply_outstanding

    def failing(cfg, plan, declared, **kwargs):
        report, gathered = real(cfg, plan, declared, **kwargs)
        return replace(report, failed={"e-1": "the taxonomy no longer declares this sub"}), gathered

    monkeypatch.setattr(apply_cli, "apply_outstanding", failing)

    _run_id, job_id = approve_and_queue(APPLY, GATE)
    code, envelope = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["inner"]["reason"] == "adopt-entries-failed", envelope
    assert artifacts.committed(cut_over, job_id), "the artifact was not committed"


def test_the_apply_opens_its_own_handle_with_write_intent(cut_over, monkeypatch):
    """``require_closed=True`` on the apply's own handle, so the pin refusal is the open's."""
    plan = apply_cli.current_plan(cut_over, DECLARED)
    for seam, answer, reason in (
        ("rekordbox_running", lambda: True, "rekordbox-running"),
        ("read_installed_app_version", lambda **_: "9.9.9.0002", "app-version-pin-drift"),
    ):
        with monkeypatch.context() as patched:
            patched.setattr(rb_writer, seam, answer)
            with pytest.raises(Exception) as excinfo:
                apply_cli._write_memberships(cut_over, plan, DECLARED)
        assert excinfo.value.cause.reason == reason, seam


def test_a_track_the_tree_write_could_not_place_is_never_marked_applied(cut_over, monkeypatch):
    """R-148: a row the writer could not resolve to one live row is never marked applied."""
    from cratekit.write import trees

    real = apply_cli._write_memberships

    def one_skipped(cfg, plan, declared):
        report = real(cfg, plan, declared)
        skipped = trees.RowMatch("a-location-two-rows-claim", trees.MatchOutcome.AMBIGUOUS)
        return replace(report, skipped=(skipped,))

    monkeypatch.setattr(apply_cli, "_write_memberships", one_skipped)

    _run_id, job_id = approve_and_queue(APPLY, GATE)
    code, envelope = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["inner"]["reason"] == "adopt-entries-failed", envelope
    assert "a-location-two-rows-claim" in envelope["cause"]["inner"]["message"], (
        "the refusal counted the unplaced rows without naming them, which is not "
        "something a person can act on"
    )
    assert adopt_apply.read(cut_over).entry_ids() == frozenset(), (
        "an unplaced track recorded as adopted"
    )


# ── Library surgery the tests above need ──


def _sql(cfg: config.Config, statement: str, parameters: tuple = ()) -> None:
    """One statement against the library database, then the reader cache forgotten."""
    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(statement, parameters)
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()


def _empty_the_collection(cfg: config.Config) -> None:
    _sql(cfg, "DELETE FROM djmdContent")


def _add_tombstone(cfg: config.Config) -> None:
    adopt_fixtures.build(cfg, ())
    _empty_the_collection(cfg)
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, FolderPath, rb_local_deleted, created_at, "
        "updated_at) VALUES (?, ?, 1, ?, ?)",
        ("r-gone", "file://localhost/gone.flac", "2026-09-02", "2026-09-02"),
    )


def _insert_under(cfg: config.Config, prefix: str, content_id: str, genre: str) -> None:
    """One live row whose recorded location sits under a volume this machine is not."""
    from cratekit.core import locations

    _sql(
        cfg,
        "INSERT OR IGNORE INTO djmdGenre (ID, Name, created_at, updated_at) "
        "SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM djmdGenre WHERE Name = ?)",
        ("900", genre, "2026-09-02", "2026-09-02", genre),
    )
    _sql(
        cfg,
        "INSERT INTO djmdContent (ID, FolderPath, GenreID, rb_local_deleted, "
        "created_at, updated_at) VALUES (?, ?, (SELECT ID FROM djmdGenre WHERE Name = ?), "
        "0, ?, ?)",
        (
            content_id,
            locations.location_url(Path(prefix) / "Music" / "one.flac"),
            genre,
            "2026-09-02",
            "2026-09-02",
        ),
    )


def _record_decision(verb: list[str], gate: str) -> str:
    """R34's first two acts, without the third drive. Answers the gate run."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(["run", "decide", run_id, gate, "approve", "--actor", "a-person"])
    assert decided == int(ExitCode.OK), envelope
    return run_id


# ── R-731: a track that already holds a competing place is withheld, not doubled ──


def _energy_bucket() -> taxonomy.Bucket:
    return next(
        bucket
        for bucket in DECLARED.buckets
        if bucket.sub_by_source is None
        and bucket.energy.enabled
        and adopt_scan.classify_genre(DECLARED, bucket.display)[1] == bucket.id
    )


def _style_bucket() -> taxonomy.Bucket:
    return next(
        bucket for bucket in DECLARED.buckets if not bucket.energy.enabled and len(bucket.subs) > 1
    )


def _band(level: int) -> str:
    return next(band.id for band in DECLARED.energy.bands if level <= band.max)


#: One placed library: each track, its file's energy, the sub it sits in (a sub, a
#: sub class, or None), and the sub the plan names.
_PLACED_ENERGY = (
    ("p-med-reads-high", "8", "band:5", "band:8"),
    ("p-nowhere", "8", None, "band:8"),
    ("p-vox-only", "5", "class:with_vox", "band:5"),
    ("p-candy-only", "2", "class:candy", "band:2"),
    ("p-sink-now-reads", "5", "sink", "band:5"),
    ("p-band-no-reading", None, "band:9", "sink"),
    ("p-same", "5", "band:5", "band:5"),
)

#: Three added, four withheld counting the style one, one already in place.
_ADDED = {"p-nowhere", "p-vox-only", "p-candy-only"}
_WITHHELD_BAND = {"p-med-reads-high", "p-sink-now-reads", "p-band-no-reading"}
_WITHHELD_STYLE = {"p-style"}


def _sub_id(spec: str) -> str:
    kind, _, value = spec.partition(":")
    if kind == "band":
        return _band(int(value))
    if kind == "sink":
        return DECLARED.energy.no_energy_sub.id
    return value


@pytest.fixture(scope="module")
def silence(tmp_path_factory) -> Path:
    """One real FLAC, encoded once and copied per track, because ffmpeg is slow."""
    from tests._containers import synth_container

    return synth_container(tmp_path_factory.mktemp("synth"), ".flac")


def _file_into(handle, root, bucket_id: str, sub_id: str, content_id: str):
    """File one track under a destination's declared names, as a cutover adopts."""
    folder_display, sub_display = destination(DECLARED, bucket_id, sub_id)
    folder = rb_writer.ensure_folder(handle, folder_display, parent=root)
    playlist = rb_writer.ensure_playlist(handle, sub_display, folder)
    rb_writer.add_memberships(handle, playlist, [content_id])
    return folder, playlist


@pytest.fixture
def placed(machine, silence):
    """A cut over library already filing tracks, with real containers and tags."""
    import shutil

    from cratekit.core import tags

    energy, style = _energy_bucket(), _style_bucket()
    first, second = style.subs[0], style.subs[1]
    style_genre = next(
        source for source, sub in style.sub_by_source.map.items() if sub == second.id
    )
    tracks = [
        adopt_fixtures.Track(content_id, f"{content_id}.flac", energy.display)
        for content_id, _tag, _held, _planned in _PLACED_ENERGY
    ]
    tracks.append(adopt_fixtures.Track("p-style", "p-style.flac", style_genre))
    adopt_fixtures.build(machine, tuple(tracks))
    collection.reset_cache()

    music = Path(machine.library.root) / "Music"
    readings = {content_id: tag for content_id, tag, _held, _planned in _PLACED_ENERGY}
    readings["p-style"] = "8"
    for content_id, tag in readings.items():
        path = music / f"{content_id}.flac"
        shutil.copyfile(silence, path)
        if tag is not None:
            assert tags.write_tags(path, {"energylevel": tag}) is True

    seeded = [
        (energy.id, _sub_id(held), content_id)
        for content_id, _tag, held, _planned in _PLACED_ENERGY
        if held is not None
    ]
    seeded.append((style.id, first.id, "p-style"))

    handle = rb_writer.open_db(rb_writer.live_db_path(machine), unlock=False, cfg=machine)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        for bucket_id, sub_id, content_id in seeded:
            _file_into(handle, root, bucket_id, sub_id, content_id)
        handle.session.commit()
        root_id = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    _record_cutover(machine, root_id, on=date(2026, 9, 27))
    return machine


def _filed(cfg: config.Config) -> dict[str, set[tuple[str, str]]]:
    """Every track's places in the tree, as folder and playlist names, read back."""
    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        names = {str(row.ID): (str(row.Name), str(row.ParentID)) for row in handle.get_playlist()}
        found: dict[str, set[tuple[str, str]]] = {}
        for playlist_id, (name, parent) in names.items():
            for entry in handle.get_playlist_songs(PlaylistID=playlist_id):
                found.setdefault(str(entry.ContentID), set()).add(
                    (names.get(parent, ("", ""))[0], name)
                )
        return found
    finally:
        rb_writer.close_db(handle)


def _shown(verb: list[str]) -> dict:
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    return refused["cause"]["detail"]["shown"]


def destination_names(bucket_id: str, sub_id: str) -> tuple[str, str]:
    return destination(DECLARED, bucket_id, sub_id)


def test_an_uncut_library_reads_neither_its_tree_nor_its_vocals(machine):
    """With no cutover the tree is not read, so no vocal membership is planned."""
    _calibrate(machine)
    _tag_vox(machine, "a1")
    plan = apply_cli.current_plan(machine, DECLARED)

    assert plan.placements.read is False
    assert plan.vocals.read is False
    assert plan.vocal_additions() == ()
    shown = _shown(APPLY)
    assert (shown["placements"], shown["vocals"]) == ("unread", "unread")


def test_an_approved_apply_leaves_a_withheld_track_where_it_sat(placed):
    """The gate counts and lists the withheld; an approved apply leaves each where it
    sat, adds the rest and removes nothing, and a second apply adds nothing. A
    renamed planned sub withholds rather than doubles, and a move after an approval
    is a stale decision."""
    plan = apply_cli.current_plan(placed, DECLARED)
    assert plan.placements.read is True
    withheld = {entry.content_id: entry for entry in plan.held_elsewhere()}
    assert set(withheld) == _WITHHELD_BAND | _WITHHELD_STYLE
    assert {entry.content_id for entry in plan.applicable()} == _ADDED | {"p-same"}
    for content_id, _tag, held, planned in _PLACED_ENERGY:
        if content_id in withheld:
            assert withheld[content_id].holds == (_sub_id(held),), content_id
            assert withheld[content_id].sub == _sub_id(planned), content_id

    first_shown = _shown(APPLY)
    assert first_shown["placements"] == "read"
    assert first_shown["withheld_by_placement"] == {"total": 4, "band": 3, "style": 1}
    assert {item["content_id"] for item in first_shown["items"]} == _ADDED | {"p-same"}
    listed = {row["content_id"]: row for row in first_shown["held_elsewhere"]}
    assert set(listed) == _WITHHELD_BAND | _WITHHELD_STYLE
    row = listed["p-med-reads-high"]
    assert (row["bucket"], row["kind"]) == (_energy_bucket().id, "band")
    assert (row["holds"], row["planned"], row["energy"]) == ([_band(5)], _band(8), 8)
    assert row["location"].endswith("p-med-reads-high.flac")
    assert listed["p-band-no-reading"]["energy"] is None
    assert listed["p-style"]["kind"] == "style"

    _code, text = drive_human(APPLY)
    for content_id in _WITHHELD_BAND | _WITHHELD_STYLE:
        assert f"content_id={content_id}" in text, content_id
    assert "withheld_by_placement:" in text

    before = _filed(placed)
    job_id = _applied()
    after = _filed(placed)
    for content_id in _WITHHELD_BAND | _WITHHELD_STYLE:
        assert after[content_id] == before[content_id], content_id
        assert len(after[content_id]) == 1, content_id
    assert after["p-same"] == before["p-same"]
    for content_id, _tag, _held, planned in _PLACED_ENERGY:
        if content_id in _ADDED:
            gained = after[content_id] - before.get(content_id, set())
            assert gained == {destination_names(_energy_bucket().id, _sub_id(planned))}
    # NOTHING IS REMOVED BY THIS UNIT, from any playlist.
    for content_id, places in before.items():
        assert places <= after[content_id], content_id

    report = artifacts.committed(placed, job_id)[-1]
    assert (report["added"], report["already_present"]) == (len(_ADDED), 1)
    plan = apply_cli.current_plan(placed, DECLARED)
    assert adopt_apply.read(placed).entry_ids() == {
        entry.entry_id for entry in plan.entries if entry.content_id in _ADDED | {"p-same"}
    }

    collection.reset_cache()
    second_shown = _shown(APPLY)
    assert second_shown["held_elsewhere"] == first_shown["held_elsewhere"]
    assert second_shown["withheld_by_placement"] == first_shown["withheld_by_placement"]
    assert second_shown["digest"] == first_shown["digest"]

    second_job = _applied()
    report = artifacts.committed(placed, second_job)[-1]
    assert (report["added"], report["already_present"]) == (0, len(_ADDED) + 1)
    assert _filed(placed) == after

    # A track in the planned sub under another name is withheld, not doubled.
    _rename_recorded(placed, _energy_bucket().id, _band(5), "Middle of the night")
    before = _filed(placed)

    shown = _shown(APPLY)
    listed = {row["content_id"]: row for row in shown["held_elsewhere"]}
    assert "p-same" in listed
    assert listed["p-same"]["holds"] == [_band(5)]
    assert listed["p-same"]["planned"] == _band(5)
    assert listed["p-same"]["holds_under_another_name"] == [_band(5)]
    assert listed["p-med-reads-high"]["holds_under_another_name"] == [_band(5)]
    assert "p-same" not in {item["content_id"] for item in shown["items"]}

    _applied()
    after = _filed(placed)
    assert after["p-same"] == before["p-same"]
    assert after["p-med-reads-high"] == before["p-med-reads-high"]

    # A track moved after the approval is a stale decision, run on the worker directly.
    _run_id, job_id = approve_and_queue(APPLY, GATE)

    handle = rb_writer.open_db(rb_writer.live_db_path(placed), unlock=False, cfg=placed)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        _file_into(handle, root, _energy_bucket().id, _band(1), "p-med-reads-high")
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    before = _filed(placed)

    with pytest.raises(Exception) as raised:
        _worker(job_id)
    assert raised.value.cause.reason == "decision-stale"
    assert _filed(placed) == before


def _rename_recorded(cfg: config.Config, bucket_id: str, sub_id: str, to: str) -> None:
    """Rename one destination's playlist in rekordbox after a write recorded its node."""
    from cratekit.core import convergence

    handle = rb_writer.open_db(rb_writer.live_db_path(cfg), unlock=False, cfg=cfg)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        folder_display, sub_display = destination_names(bucket_id, sub_id)
        folder = rb_writer.ensure_folder(handle, folder_display, parent=root)
        playlist = rb_writer.ensure_playlist(handle, sub_display, folder)
        node = convergence.DestinationNode(
            bucket=bucket_id,
            sub=sub_id,
            folder_id=str(folder.ID),
            playlist_id=str(playlist.ID),
        )
        playlist.Name = to
        handle.session.commit()
    finally:
        rb_writer.close_db(handle)
    convergence.record_nodes(cfg, DECLARED.tree.id, [node])


# ── R-788: a vox tagged track is filed under its bucket's vocal sub ─────────

VOX = "with_vox"

#: Who carries the tag in the placed library, and what the plan does about each.
_VOX_ADDED = {"p-nowhere", "p-same"}
_VOX_PRESENT = {"p-vox-only"}
_VOX_WITHHELD = {"p-med-reads-high"}
_VOX_TAGGED = _VOX_ADDED | _VOX_PRESENT | _VOX_WITHHELD


def _tag_vox(cfg: config.Config, *content_ids: str) -> None:
    """Give these tracks the vox My Tag as rows, the way the vocals verb leaves them."""
    from pyrekordbox.db6 import tables
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    from cratekit.write import metadata_cli
    from tests.test_rb_writer_db import _row

    def tag(row_id, name, parent, uuid):
        return _row(
            tables.DjmdMyTag,
            ID=row_id,
            Name=name,
            Attribute=0,
            ParentID=parent,
            Seq=0,
            UUID=uuid,
            rb_local_deleted=0,
        )

    engine = create_engine(f"sqlite:///{rb_writer.live_db_path(cfg)}")
    with Session(engine) as db_session:
        if db_session.get(tables.DjmdMyTag, "9000") is None:
            db_session.add(tag("9000", metadata_cli.CATEGORY, "0", "vocals-category"))
            db_session.add(tag("9001", metadata_cli.VALUE_VOX, "9000", "vox-value"))
        for content_id in content_ids:
            db_session.add(
                _row(
                    tables.DjmdSongMyTag,
                    ID=f"vox-{content_id}",
                    MyTagID="9001",
                    ContentID=content_id,
                    TrackNo=0,
                    UUID=f"vox-{content_id}",
                    rb_local_deleted=0,
                )
            )
        db_session.commit()
    engine.dispose()


def _write_calibration(cfg: config.Config, text: str) -> None:
    from cratekit.write import metadata_cli

    path = config.state_path(metadata_cli.STATE_KEY_VOCAL_CALIBRATION, cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _calibrate(cfg: config.Config) -> None:
    """Record a with vox cut for this library, the way a calibration leaves one."""
    _write_calibration(cfg, json.dumps({"threshold": 5.0}))


@pytest.fixture
def voxed(placed):
    """The placed library, calibrated, with four of its tracks carrying the vox tag."""
    _calibrate(placed)
    _tag_vox(placed, *sorted(_VOX_TAGGED))
    return placed


def _vocal_place() -> tuple[str, str]:
    return destination_names(_energy_bucket().id, VOX)


def _never(what: str):
    def never(*_args, **_kwargs):
        raise AssertionError(what)

    return never


def test_an_untagged_membership_of_a_vocal_sub_is_never_removed(placed):
    """A calibrated library with no vox tag plans no vocal membership; an untagged
    track in the vocal sub is never removed from it."""
    _calibrate(placed)
    shown = _shown(APPLY)
    assert shown["vocals"] == "no-tag"
    assert set(shown["vocal"].values()) == {0}
    assert shown["vocal_memberships"] == []

    _tag_vox(placed, "p-nowhere")
    vocal = _vocal_place()
    assert vocal in _filed(placed)["p-vox-only"]
    _applied()
    after = _filed(placed)
    assert vocal in after["p-vox-only"]
    assert vocal in after["p-nowhere"]


def test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags(placed, monkeypatch):
    """Without a cut the routing pass files nothing under the vocal sub and opens no
    tag table; a tag from the default cut is not the person's answer."""
    _tag_vox(placed, *sorted(_VOX_TAGGED))
    vocal = _vocal_place()
    with monkeypatch.context() as patched:
        patched.setattr(
            adopt_placements, "vox_tagged", _never("the tag tables were read with no cut on record")
        )
        assert apply_cli.current_plan(placed, DECLARED).vocals.state == "uncalibrated"
    shown = _shown(APPLY)

    assert shown["vocals"] == "uncalibrated"
    assert set(shown["vocal"].values()) == {0}
    assert shown["vocal_memberships"] == []

    _applied()
    after = _filed(placed)
    assert {cid for cid, places in after.items() if vocal in places} == {"p-vox-only"}


def test_a_calibration_that_cannot_be_read_refuses_before_the_library_is_walked(voxed, monkeypatch):
    """A taxonomy with no vocal sub reads neither the calibration nor the tag, in the
    move verb's plan and its worker's too."""
    from cratekit.adopt import move_cli
    from cratekit.write import metadata_cli

    _write_calibration(voxed, '{"threshold": 5.')

    with monkeypatch.context() as patched:
        patched.setattr(
            apply_cli, "census", _never("the census ran before the calibration was read")
        )
        with pytest.raises(Exception) as raised:
            apply_cli.current_plan(voxed, DECLARED)
    assert raised.value.cause.reason == "vocal-calibration-unreadable"

    monkeypatch.setattr(
        adopt_placements, "vox_tagged", _never("the tag tables were read with nowhere to file")
    )
    declared = replace(
        DECLARED, sub_classes=tuple(e for e in DECLARED.sub_classes if not e.additive)
    )
    plan = apply_cli.current_plan(voxed, declared)

    assert plan.vocals.state == "no-sub"
    assert plan.vocal_memberships() == ()
    assert plan.placements.read is True

    monkeypatch.setattr(
        metadata_cli, "load_vocal_threshold", _never("the move verb read the vocals")
    )
    assert move_cli.current_plan(voxed, DECLARED) is not None
    plain = apply_cli.current_plan(voxed, DECLARED, vocals=False)
    assert plain.vocals.read is False
    assert plain.vocal_memberships() == ()
    with pytest.raises(AssertionError):
        apply_cli.current_plan(voxed, DECLARED)


def test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else(voxed):
    """The gate names the vocal count and lists every membership. An approved apply
    adds the vocal sub beside the band, never adds an untagged track and removes
    nothing; it resumes against the plan it approved. A track tagged after approval
    is stale, and a renamed vocal playlist gains no second one."""
    plan = apply_cli.current_plan(voxed, DECLARED)
    bucket = _energy_bucket().id
    assert plan.vocals.state == "read"
    assert plan.vocals.calibrated is True
    assert plan.vocals.tagged == _VOX_TAGGED
    assert plan.vocals.filed == {bucket: {"p-vox-only"}}
    assert {entry.content_id for entry in plan.vocal_additions()} == _VOX_ADDED
    assert {entry.vocal_sub for entry in plan.vocal_additions()} == {VOX}

    before = _filed(voxed)
    vocal = _vocal_place()
    first_shown = _shown(APPLY)
    assert first_shown["vocals"] == "read"
    assert first_shown["vocal"] == {
        "add": len(_VOX_ADDED),
        "present": len(_VOX_PRESENT),
        "under-another-name": 0,
        "no-sub": 0,
        "no-bucket": 0,
        "withheld": len(_VOX_WITHHELD),
    }
    listed = {row["content_id"]: row for row in first_shown["vocal_memberships"]}
    assert set(listed) == _VOX_ADDED | _VOX_PRESENT
    assert {cid for cid, row in listed.items() if not row["present"]} == _VOX_ADDED
    assert (listed["p-nowhere"]["bucket"], listed["p-nowhere"]["sub"]) == (bucket, VOX)
    assert listed["p-nowhere"]["location"].endswith("p-nowhere.flac")
    # The entries an apply places are what they were. The vocal sub is beside.
    assert {item["content_id"] for item in first_shown["items"]} == _ADDED | {"p-same"}

    job_id = _applied()
    after = _filed(voxed)

    band = {content_id: planned for content_id, _tag, _held, planned in _PLACED_ENERGY}
    for content_id in _VOX_ADDED:
        gained = after[content_id] - before.get(content_id, set())
        expected = {vocal}
        if content_id in _ADDED:
            expected.add(destination_names(bucket, _sub_id(band[content_id])))
        assert gained == expected, content_id
    # ALREADY THERE: no second row, and its band is added as it always was.
    assert vocal in before["p-vox-only"] and vocal in after["p-vox-only"]
    # WITHHELD STAYS WITHHELD, vocal sub included.
    assert after["p-med-reads-high"] == before["p-med-reads-high"]
    assert vocal not in after["p-med-reads-high"]
    for content_id in after:
        if content_id not in _VOX_TAGGED:
            assert vocal not in after[content_id], content_id
    for content_id, places in before.items():
        assert places <= after[content_id], content_id

    report = artifacts.committed(voxed, job_id)[-1]
    assert (report["added"], report["already_present"]) == (len(_ADDED) + len(_VOX_ADDED), 1)
    assert "/".join(vocal) in report["playlists"]

    collection.reset_cache()
    second_shown = _shown(APPLY)
    assert second_shown["vocal"]["add"] == 0
    assert second_shown["vocal"]["present"] == len(_VOX_ADDED) + len(_VOX_PRESENT)
    assert [row["id"] for row in second_shown["vocal_memberships"]] == [
        row["id"] for row in first_shown["vocal_memberships"]
    ]
    assert all(row["present"] for row in second_shown["vocal_memberships"])
    assert second_shown["digest"] == first_shown["digest"]

    second_job = _applied()
    assert artifacts.committed(voxed, second_job)[-1]["added"] == 0
    assert _filed(voxed) == after

    # A TRACK TAGGED AFTER THE APPROVAL IS A STALE DECISION.
    _run_id, job_id = approve_and_queue(APPLY, GATE)
    _tag_vox(voxed, "p-candy-only")
    before = _filed(voxed)

    with pytest.raises(Exception) as raised:
        _worker(job_id)
    assert raised.value.cause.reason == "decision-stale"
    assert _filed(voxed) == before

    # A renamed vocal playlist gains no second one: the plan adds none.
    _rename_recorded(voxed, _energy_bucket().id, VOX, "Singers")

    shown = _shown(APPLY)
    assert shown["vocal"]["add"] == 0
    assert shown["vocal"]["under-another-name"] == len(_VOX_TAGGED | {"p-candy-only"})
    assert shown["vocal_memberships"] == []

    _applied()
    after = _filed(voxed)
    assert all(vocal not in places for places in after.values())
    assert (vocal[0], "Singers") in after["p-vox-only"]


# ── The active taxonomy, parsed once a run (U247) ──


def _active_copy(cfg: config.Config, text: str) -> Path:
    path = config.state_path("taxonomy_active", cfg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit(machine, monkeypatch):
    """R-690: the read stays per item, so an edit keeping length, time and inode counts."""
    before = unique(taxonomy.shipped_template_text(taxonomy.DEFAULT_TEMPLATE_NAME))
    display = DECLARED.buckets[0].display
    after, renamed = renamed_in_place(before, display)
    path = _active_copy(machine, before)
    judged_by: list[taxonomy.Taxonomy] = []
    real = adopt_scan.scan_rows

    def watching(rows, declared, **kwargs):
        judged_by.append(declared)
        if len(judged_by) == 1:
            rewrite_keeping_time(path, after)
        return real(rows, declared, **kwargs)

    monkeypatch.setattr(adopt_scan, "scan_rows", watching)

    code, queued = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), queued
    code, resumed = drive(["adopt", "scan", "--job", _scan_job().job_id])
    assert code == int(ExitCode.OK), resumed
    assert len(judged_by) >= 3
    assert judged_by[0] == taxonomy.load_taxonomy(before)
    assert judged_by[0].buckets[0].display == display
    assert all(declared == taxonomy.load_taxonomy(after) for declared in judged_by[1:])
    assert judged_by[1].buckets[0].display == renamed
