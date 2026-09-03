"""U55: both adopt verbs driving their own queued work, end to end.

WHAT THIS FILE IS FOR THAT NO OTHER FILE CAN BE. ``test_adopt_apply_cli.py``
drives the queueing path and the session, and ``test_adopt_collection.py`` drives
the read. Neither one runs an ITEM. Until this file existed, both handler keys
were in ``HANDLERS_NOT_YET_BOUND`` and the property "a queued adoption actually
happens" had nowhere to be asserted.

THE APPLY'S HAPPY PATH NEEDS A CUT-OVER LIBRARY, and that is the honest shape
rather than a convenience. ``write_tree_membership`` refuses a tree that is not
recorded as database native with a root the library actually has, and nothing in
``src`` records a cutover, so the only way to reach the write at all is to record
one here the way ``tests/test_tree_writer.py`` does. That asymmetry is this
build's, not this file's, and it is written down as a residual.

D1 APPLIES. Nothing here names a real volume, a real person, or a real track.
"""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from cratekit.adopt import apply as adopt_apply
from cratekit.adopt import apply_cli, artifacts, collection, scan_cli
from cratekit.adopt import scan as adopt_scan
from cratekit.cli import handlers, registry
from cratekit.core import config, jobs, preflight, rb_writer, session, taxonomy, tree_registry
from cratekit.core.exit_codes import ExitCode
from tests import adopt_fixtures
from tests.cli_drive import approve_and_queue, drive
from tests.test_adoption import _bucket_and_genre
from tests.test_config import valid_data
from tests.test_rb_writer_db import RECORDED_APP_VERSION

#: The tree the shipped taxonomy declares, resolved once so the cutover the
#: fixture records and the tree the plan names cannot drift apart.
DECLARED = taxonomy.default_taxonomy()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
    """Everything about THIS machine a temporary library cannot speak for.

    The three process probes and the cloud-sync marker, patched where the guards
    resolve them. That each of these guards refuses is proved directly, against
    the same seams driven the other way, in ``tests/test_rb_writer_db.py``.
    """
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
    # The capture's integrity check reaches for the key by default and an
    # unencrypted fixture fails it, which would report every session here as
    # having no verified recovery point. Compensated at the FIXTURE, never by
    # giving the writer a verifier argument, for the reason
    # ``tests/test_tree_writer.py`` gives: a writer that accepts one accepts
    # ``lambda _: True``.
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


@pytest.fixture
def machine(library, monkeypatch):
    """A set-up machine with a library the adopt verbs can act on.

    Saved to disk rather than monkeypatched, because every test here drives the
    real dispatcher and the dispatcher loads configuration for itself in the
    parser construction every invocation runs first.
    """
    resolved = config.from_dict(
        valid_data(
            library,
            rekordbox={
                "pinned_app_version": RECORDED_APP_VERSION,
                "validated_on": "2026-08-01",
            },
        )
    )
    config.save(resolved)
    config.reset_cache()
    adopt_fixtures.build(resolved, _tracks())
    collection.reset_cache()
    monkeypatch.setattr(
        preflight, "default_identity_provider", lambda: (lambda _path: resolved.library.volume_id)
    )
    monkeypatch.setattr(preflight, "local_mount_points", lambda: ())
    session.record_acknowledgment(resolved, terminal=lambda: True)
    return resolved


@pytest.fixture
def cut_over(machine):
    """A library whose taxonomy tree the registry records as database native.

    THE ONLY WAY THE APPLY'S WRITE PATH IS REACHABLE AT ALL. ``anchored_root``
    refuses a tree still on the bridge, and ``Registry.mode`` treats an
    unrecorded tree as being on the bridge, so without this the write refuses on
    every library there is. Recording it here rather than through a verb is not a
    shortcut: no verb records one.
    """
    target = rb_writer.live_db_path(machine)
    handle = rb_writer.open_db(target, unlock=False, cfg=machine)
    try:
        root = rb_writer.ensure_folder(handle, DECLARED.tree.display)
        handle.session.commit()
        root_id = str(root.ID)
    finally:
        rb_writer.close_db(handle)
    tree_registry.record_cutover(
        machine,
        DECLARED.tree.id,
        root_id=root_id,
        on=date(2026, 9, 2),
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    return machine


def _resume(job_id: str) -> list[str]:
    """The command line the job driver would spawn for this job.

    THROUGH THE REAL ``argv_for`` rather than by hand, which is the only thing
    that can tell a resume that works from one refused for ever: the approval
    gate is explicit, so a resume that minted a fresh run would meet it again
    with nothing recorded and exit DECISION_REQUIRED on every respawn.
    """
    from cratekit.cli import jobs as cli_jobs

    with jobs.open_store() as store:
        return cli_jobs.argv_for(jobs.get(store, job_id))


def _job(handler_key: str):
    with jobs.open_store() as store:
        held = [job for job in jobs.list_jobs(store) if job.handler_key == handler_key]
    assert len(held) == 1, f"expected exactly one {handler_key} job, found {len(held)}"
    return held[0]


def _memberships(cfg: config.Config) -> dict[str, list[str]]:
    """What the database actually holds, read back through a fresh handle.

    READ BACK RATHER THAN TAKEN FROM THE REPORT, which is the whole point of the
    apply's happy path assertion: a ``MembershipReport`` saying it added two rows
    is the writer's own account of itself, and the seam defect this unit fixes
    produced exactly that account over a write that landed nothing.
    """
    target = rb_writer.live_db_path(cfg)
    handle = rb_writer.open_db(target, unlock=False, cfg=cfg)
    try:
        found: dict[str, list[str]] = {}
        for row in handle.get_playlist():
            members = [
                str(entry.ContentID)
                for entry in handle.get_playlist_songs(PlaylistID=str(row.ID))
            ]
            if members:
                found[str(row.Name)] = sorted(members)
        return found
    finally:
        rb_writer.close_db(handle)


# ---------------------------------------------------------------------------
# Both keys are bound
# ---------------------------------------------------------------------------


def test_both_adopt_keys_resolve_to_a_worker():
    """The R-203 half this unit closes, asserted against the table rather than prose."""
    for name in ("adopt.scan", "adopt.apply"):
        key = registry.entry(name).handler_key
        assert handlers.is_known(key), f"{key} still has no worker"
        assert handlers.unbound_reason(key) is None
        assert callable(handlers.resolve(key))


# ---------------------------------------------------------------------------
# The scan
# ---------------------------------------------------------------------------


def test_a_scan_queues_one_item_per_live_row_and_drives_them_all(machine):
    """Pending to done through the real resume argv, and the artifact read back.

    THE THIRD ITEM IS THE ONE WORTH READING BACK. Its file is not on disk, so a
    worker that reported every row as readable would still drive to done and the
    counts would still add up; only the artifact says which category the row
    actually landed in.
    """
    code, queued = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), queued
    job = _job(registry.entry("adopt.scan").handler_key)
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
        assert all(
            item.state is jobs.ItemState.DONE for item in jobs.items(store, job.job_id)
        )

    reports = {
        report["content_id"]: report for report in artifacts.committed(machine, job.job_id)
    }
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


def test_the_reported_counts_come_from_the_artifacts_and_not_from_the_queue(machine):
    """Derived from what RAN. The items alone would report five of five either way."""
    drive(["adopt", "scan"])
    job = _job(registry.entry("adopt.scan").handler_key)
    _code, resumed = drive(["adopt", "scan", "--job", job.job_id])

    counted = sum(resumed["data"]["progress"]["census"]["categories"].values())
    assert counted == len(artifacts.committed(machine, job.job_id))
    assert counted == resumed["data"]["progress"]["total"]


def test_an_empty_library_queues_nothing_and_says_so(machine):
    """THE HONEST ZERO. Nothing is queued, and the exit code is still success."""
    adopt_fixtures.build(machine, ())
    collection.reset_cache()
    # The two rows the disposable build seeds carry no location, so a library
    # with only those still has live rows. Remove them to reach the true zero.
    _empty_the_collection(machine)

    code, envelope = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), envelope
    assert envelope["outcome"] == "no_op"
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == ["collection-empty"]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_library_of_tombstones_is_a_different_zero_from_an_empty_one(machine):
    """Both census to nothing, and only the collection can tell them apart."""
    _empty_the_collection(machine)
    _add_tombstone(machine)
    collection.reset_cache()

    code, envelope = drive(["adopt", "scan"])
    assert code == int(ExitCode.OK), envelope
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "collection-all-tombstones"
    ]
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item(machine):
    """The nil path, named rather than raised as a KeyError.

    The collection is re-read at drive time and is not frozen, so this is
    reachable input rather than a hypothetical.
    """
    drive(["adopt", "scan"])
    job = _job(registry.entry("adopt.scan").handler_key)

    _delete_row(machine, "r-two")
    collection.reset_cache()

    code, resumed = drive(["adopt", "scan", "--job", job.job_id])
    assert code != int(ExitCode.OK)
    with jobs.open_store() as store:
        states = {item.item_id: item.state for item in jobs.items(store, job.job_id)}
    assert states["r-two"] is jobs.ItemState.FAILED
    assert states["r-one"] is jobs.ItemState.DONE
    with jobs.open_store() as store:
        failed = [
            item for item in jobs.items(store, job.job_id) if item.item_id == "r-two"
        ][0]
    assert failed.cause is not None
    assert failed.cause.reason == "adopt-item-absent"


def test_a_job_queued_with_no_items_refuses_rather_than_reporting_success(machine):
    """A job frozen by a build before this one carries no items at all.

    ``core.jobs`` reports a zero item job as SUCCEEDED by design, so driving one
    would report a census over a library it never read.
    """
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=registry.entry("adopt.scan").handler_key,
            payload={"tree": DECLARED.tree.id},
            cfg=machine,
        )
    code, envelope = drive(["adopt", "scan", "--job", job.job_id])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "internal-error"
    assert "no items" in envelope["cause"]["message"]


def test_the_configuration_reaching_the_scan_worker_is_the_frozen_one(machine):
    """KTD9, driven on a key NO environment variable overrides.

    ``frozen_config`` reapplies environment overrides and the suite sets
    ``CRATEKIT_LIBRARY_ROOT`` globally, so the obvious version of this test cannot
    fail. The artifact root is resolved from the handed configuration, so moving
    the queue's own directory is what makes the difference visible.
    """
    seen: list[str] = []
    real = artifacts.produced

    def recording(cfg, job, item, report):
        seen.append(str(jobs.store_dir(cfg)))
        return real(cfg, job, item, report)

    drive(["adopt", "scan"])
    job = _job(registry.entry("adopt.scan").handler_key)
    frozen_root = str(jobs.store_dir(jobs.frozen_config(job)))

    import unittest.mock

    with unittest.mock.patch.object(scan_cli.artifacts, "produced", recording):
        drive(["adopt", "scan", "--job", job.job_id])
    assert seen and set(seen) == {frozen_root}


# ---------------------------------------------------------------------------
# The apply
# ---------------------------------------------------------------------------


def test_an_apply_over_a_cut_over_library_writes_the_memberships(cut_over):
    """The happy path, read back from the database rather than from the report.

    THE READ BACK IS THE ASSERTION. The seam defect this unit fixes produced a
    ``MembershipReport`` naming a session that ran over a write that landed
    nothing, so a test that trusted the report would have passed against it.
    """
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    with jobs.open_store() as store:
        assert [item.item_id for item in jobs.items(store, job_id)] == [
            apply_cli.current_plan(cut_over, DECLARED).digest()
        ]

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


def test_the_apply_writes_no_tag_and_leaves_every_file_byte_identical(cut_over):
    """R16. Nothing in this build supplies a ``tag_value``, so nothing is written.

    Measured against the files' own bytes rather than argued from the call, which
    is the only thing that can tell a tag write that did not happen from one whose
    caller believes it did not.
    """
    music = Path(cut_over.library.root) / "Music"
    before = {path: path.read_bytes() for path in sorted(music.glob("*.flac"))}
    assert before, "the fixture wrote no files, so this assertion is empty"

    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, _resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK)

    assert {path: path.read_bytes() for path in sorted(music.glob("*.flac"))} == before


def test_a_second_drive_adds_no_second_membership_row(cut_over):
    """Idempotent, which is what makes the crash between the two writes survivable."""
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    drive(_resume(job_id))
    first = _memberships(cut_over)

    # THE WORKER IS RUN AGAIN DIRECTLY, because ``jobs.retry`` refuses a job that
    # SUCCEEDED and there is nothing left in it to resume. What is under test is
    # the worker's own idempotence, not the queue's.
    collection.reset_cache()
    handler = handlers.resolve(registry.entry("adopt.apply").handler_key)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    produced = handler(job, item, jobs.frozen_config(job))

    assert _memberships(cut_over) == first
    # READ THE STAGED FILE, not the committed one. ``jobs.drive`` owns the
    # flush-then-rename and nothing drove this call, so the committed artifact is
    # still the FIRST run's and reading it would assert the wrong run's numbers.
    report = json.loads(produced.staged.read_text(encoding="utf-8"))
    assert report["added"] == 0
    assert report["already_present"] == len(
        [row for rows in first.values() for row in rows]
    )


def test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run(cut_over):
    """The crash-repair property, driven rather than argued.

    A ledger that already holds every entry makes ``apply_outstanding`` gather
    nothing, which is exactly the state a kill between the two writes leaves. If
    the mapping came from the run, the memberships would never land. It comes from
    the plan, so they do.
    """
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

    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, resumed = drive(_resume(job_id))
    assert code == int(ExitCode.OK), resumed

    report = artifacts.committed(cut_over, job_id)[-1]
    assert report["gathered"] == [], "the loop had nothing outstanding, as this test needs"
    assert report["added"] == 2, (
        "the memberships were derived from what this run applied rather than from "
        "the plan, so a kill between the membership write and the ledger mark "
        "would be permanent"
    )
    assert _memberships(cut_over)


def test_an_uncut_library_marks_nothing_and_the_job_stays_resumable(machine):
    """The state every real library is in, and the refusal is the honest answer.

    An unrecorded registry IS the bridge: ``Registry.mode`` defaults to XML, so
    "no record" and "recorded as bridge" are one state raising one refusal. Both
    it and ``RegistrySkew`` carry the slug ``tree-unconverged``, so this asserts on
    the refusal's own detail rather than on a slug that cannot tell them apart.
    """
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert resumed["cause"]["inner"]["reason"] == "tree-unconverged"
    assert resumed["cause"]["inner"]["detail"]["tree_id"] == DECLARED.tree.id
    assert adopt_apply.read(machine).entry_ids() == frozenset(), (
        "the ledger marked entries over an adoption that placed nothing, so the "
        "next run would find nothing outstanding and the gap would be permanent"
    )
    with jobs.open_store() as store:
        assert jobs.get(store, job_id).state is jobs.JobState.FAILED


def test_a_registry_naming_a_root_the_library_does_not_have_is_its_own_refusal(machine):
    """Distinguishable from the bridge case by DETAIL, since both share a slug."""
    tree_registry.record_cutover(
        machine,
        DECLARED.tree.id,
        root_id="no-such-root",
        on=date(2026, 9, 2),
        source=tree_registry.DerivationSource.TAXONOMY,
    )
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, resumed = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert resumed["cause"]["inner"]["reason"] == "tree-unconverged"
    assert resumed["cause"]["inner"]["detail"]["root_id"] == "no-such-root", (
        "the two tree refusals share a slug, so only the detail tells them apart"
    )


def test_a_plan_with_nothing_applicable_queues_nothing(machine):
    """The apply's honest zero. The gate still fires; the queue stays empty."""
    _empty_the_collection(machine)
    _add_unroutable(machine)
    collection.reset_cache()

    run_id, envelope = _answer_gate(["adopt", "apply"], "adopt.apply.approve")
    assert envelope["outcome"] == "no_op", envelope
    assert envelope["data"]["job_id"] == ""
    assert [warning["code"] for warning in envelope["warnings"]] == [
        "adoption-nothing-applicable"
    ]
    del run_id
    with jobs.open_store() as store:
        assert jobs.list_jobs(store) == ()


def test_a_collection_that_moved_after_approval_refuses_rather_than_applying(cut_over):
    """R34 held at the WORKER as well as at the gate.

    The gate refuses a stale decision on the way in. This is the same refusal one
    layer down, and it is what stops a job frozen yesterday from applying a write
    set nobody has seen.
    """
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    _delete_row(cut_over, "r-two")
    collection.reset_cache()

    handler = handlers.resolve(registry.entry("adopt.apply").handler_key)
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
    with pytest.raises(Exception) as excinfo:
        handler(job, item, jobs.frozen_config(job))
    assert excinfo.value.cause.reason == "decision-stale"
    assert adopt_apply.read(cut_over).entry_ids() == frozenset()


def test_the_approving_actor_travels_in_the_payload(cut_over):
    """R34 asks WHICH ACTOR asserted the decision, and the worker has no run.

    ``approval.grant`` refuses an empty actor, so without the frozen key the only
    actor a worker could supply is one it invented.
    """
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    with jobs.open_store() as store:
        payload = jobs.get(store, job_id).payload
    assert payload[apply_cli.ACTOR_KEY] == "a-person"

    drive(_resume(job_id))
    report = artifacts.committed(cut_over, job_id)[-1]
    assert report["actor"] == "a-person"


def test_the_membership_write_needs_locations_and_not_content_identifiers(cut_over):
    """The seam mismatch, MEASURED rather than argued.

    ``membership_plan`` groups content identifiers and ``write_tree_membership``
    decodes every value as a recorded location, so handing one to the other
    matches nothing and reports a session that ran over a write that landed
    nothing. Driven directly here, both ways, so the plan's claim is a number in
    this repository.
    """
    plan = apply_cli.current_plan(cut_over, DECLARED)
    by_identifier = adopt_apply.membership_plan(plan.applicable(), DECLARED)
    by_location = apply_cli.membership_locations(plan.applicable(), DECLARED)
    assert set(by_identifier) == set(by_location)
    assert by_identifier != by_location

    handle = rb_writer.open_db(rb_writer.live_db_path(cut_over), unlock=False, cfg=cut_over)
    try:
        from cratekit.write import trees

        index = trees.index_active_rows(
            collection.read_collection(cut_over),
            root=cut_over.library.root,
            prefix_map=collection.prefix_rules(cut_over),
        )
        wanted = [value for values in by_identifier.values() for value in values]
        matched = trees.match_indexed_rows(
            wanted, index, root=cut_over.library.root, prefix_map=()
        )
        assert wanted and not any(
            match.outcome is trees.MatchOutcome.MATCHED for match in matched
        ), "content identifiers matched a location index, so the seam claim is wrong"

        wanted = [value for values in by_location.values() for value in values]
        matched = trees.match_indexed_rows(
            wanted,
            index,
            root=cut_over.library.root,
            prefix_map=collection.prefix_rules(cut_over),
        )
        assert all(match.outcome is trees.MatchOutcome.MATCHED for match in matched)
    finally:
        rb_writer.close_db(handle)


def test_one_capture_per_apply_job_whatever_the_entry_count(cut_over):
    """KTD6's measured cost, pinned so an item-per-entry shape cannot creep back.

    ``write_tree_membership`` runs a full ``snapshot.capture`` inside its session,
    so one item per track would copy the whole rekordbox database once per track.
    """
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    drive(_resume(job_id))

    captures = sorted(p for p in rb_writer.snapshot_root(cut_over).iterdir() if p.is_dir())
    assert len(captures) == 1, captures


# ---------------------------------------------------------------------------
# Library surgery the fixtures above need
# ---------------------------------------------------------------------------


def _connect(cfg: config.Config):
    import sqlite3

    return sqlite3.connect(Path(cfg.library.db_path))


def _empty_the_collection(cfg: config.Config) -> None:
    conn = _connect(cfg)
    try:
        conn.execute("DELETE FROM djmdContent")
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()


def _delete_row(cfg: config.Config, content_id: str) -> None:
    conn = _connect(cfg)
    try:
        conn.execute("DELETE FROM djmdContent WHERE ID = ?", (content_id,))
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()


def _add_tombstone(cfg: config.Config) -> None:
    adopt_fixtures.build(cfg, ())
    _empty_the_collection(cfg)
    conn = _connect(cfg)
    try:
        conn.execute(
            "INSERT INTO djmdContent (ID, FolderPath, rb_local_deleted, created_at, "
            "updated_at) VALUES (?, ?, 1, ?, ?)",
            ("r-gone", "file://localhost/gone.flac", "2026-09-02", "2026-09-02"),
        )
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()


def _add_unroutable(cfg: config.Config) -> None:
    """One live row whose genre nothing can route, so the plan holds it and cannot act."""
    conn = _connect(cfg)
    try:
        conn.execute(
            "INSERT INTO djmdContent (ID, FolderPath, rb_local_deleted, created_at, "
            "updated_at) VALUES (?, ?, 0, ?, ?)",
            ("r-blank", "file://localhost/blank.flac", "2026-09-02", "2026-09-02"),
        )
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()


def _answer_gate(verb: list[str], gate: str) -> tuple[str, dict]:
    """R34's two acts, then the third drive, WITHOUT asserting it queued.

    ``tests.cli_drive.approve_and_queue`` asserts a job comes back, which is
    exactly what the no-op paths here do not do.
    """
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, gate, refused["cause"]["detail"]["options"][0], "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    code, envelope = drive(["--run", run_id, *verb])
    assert code == int(ExitCode.OK), envelope
    return run_id, envelope


# ---------------------------------------------------------------------------
# The gaps the first mutation round found, closed
# ---------------------------------------------------------------------------


def test_a_configured_volume_rewrite_reaches_the_census(machine, tmp_path):
    """S1's prefix map, driven through the census rather than assumed.

    Measured on 2026-09-02: dropping ``prefix_map`` from ``census`` killed ZERO
    tests across the whole suite, because every fixture in this repository records
    its locations under the configured root already. The source library records
    most of its active rows under an OLDER VOLUME NAME, which is the failure S1
    exists to prevent and which no test could see.
    """
    # A root this machine is not, built under the test's own temporary directory
    # rather than spelled as a volume path: R1 forbids a shipped artifact naming a
    # volume, and what the census has to resolve is a prefix rather than a mount.
    older = str(tmp_path / "an-older-root")
    rows = _tracks()
    adopt_fixtures.build(machine, ())
    _empty_the_collection(machine)
    _insert_under(machine, older, "r-elsewhere", rows[0].genre)
    (Path(machine.library.root) / "Music" / "one.flac").write_bytes(b"\x00" * 64)

    unmapped = apply_cli.census(machine, DECLARED)
    found = {track.content_id: track for track in unmapped}
    assert found["r-elsewhere"].readability is adopt_scan.Readability.UNMAPPED

    root = Path(machine.library.root)
    data = valid_data(
        root,
        rekordbox={
            "pinned_app_version": RECORDED_APP_VERSION,
            "validated_on": "2026-08-01",
        },
    )
    data["library"]["location_prefix_map"] = [{"from": older, "to": "{library.root}"}]
    mapped = config.from_dict(data)
    collection.reset_cache()
    routed = apply_cli.census(mapped, DECLARED)
    resolved = {track.content_id: track for track in routed}
    assert resolved["r-elsewhere"].readability is adopt_scan.Readability.READABLE, (
        "the census ignored the configured volume rewrite, so a library recorded "
        "under an older volume name resolves nowhere"
    )
    assert resolved["r-elsewhere"].disposition is adopt_scan.Disposition.ROUTE


def test_an_apply_job_queued_with_no_items_refuses_rather_than_driving(machine):
    """The sibling of the scan's guard, which the first mutation round found absent.

    Measured on 2026-09-02: deleting this refusal from ``apply_cli._resume`` killed
    zero tests. A job frozen by a build before this one carries no items, and
    ``core.jobs`` reports a zero item job as SUCCEEDED by design, so driving one
    reports an adoption over a library it never touched.
    """
    plan = apply_cli.current_plan(machine, DECLARED)
    run_id, refused = _record_decision(["adopt", "apply"], "adopt.apply.approve")
    del refused
    with jobs.open_store() as store:
        job = jobs.enqueue(
            store,
            handler_key=registry.entry("adopt.apply").handler_key,
            payload={
                "tree": plan.tree,
                "digest": plan.digest(),
                apply_cli.ACTOR_KEY: "a-person",
                jobs.GATE_RUN_KEY: run_id,
            },
            cfg=machine,
        )
    code, envelope = drive(["--run", run_id, "adopt", "apply", "--job", job.job_id])
    assert code != int(ExitCode.OK)
    assert envelope["cause"]["reason"] == "internal-error"
    assert "no items" in envelope["cause"]["message"]


@pytest.mark.parametrize("verb", ["adopt.scan", "adopt.apply"])
def test_an_interrupted_job_exits_with_its_own_cause_and_not_ok(machine, verb):
    """R-225, at its WIDER edge, which the first mutation round found untested.

    Measured on 2026-09-02: narrowing each resume branch's predicate from "closed
    and carrying a cause" to "FAILED" killed zero tests, because every driven
    failure here reaches FAILED. A run stopped by a signal is CANCELLED and
    carries the cause ``jobs.cancel`` builds, so the narrow predicate reports an
    interrupted adoption through a normal envelope and exits 0. That exact shape
    was driven on the two outbound verbs on 2026-09-02 as exit 0 over a job with
    none of its items done.
    """
    if verb == "adopt.scan":
        drive(["adopt", "scan"])
        job = _job(registry.entry("adopt.scan").handler_key)
        argv = ["adopt", "scan", "--job", job.job_id]
        job_id = job.job_id
    else:
        run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
        argv = ["--run", run_id, "adopt", "apply", "--job", job_id]

    with jobs.open_store() as store:
        jobs.cancel(store, job_id, stage="interrupted")
        cancelled = jobs.get(store, job_id)
    assert cancelled.state is jobs.JobState.CANCELLED
    assert cancelled.cause is not None, "the fixture built a cause-free cancel"

    code, envelope = drive(argv)
    assert code != int(ExitCode.OK), (
        "an interrupted adoption reported through a normal envelope, so a person "
        "whose work did not happen is told it finished"
    )
    assert envelope["cause"]["reason"] == cancelled.cause.reason


def test_an_apply_whose_entries_failed_raises_rather_than_reporting_success(
    cut_over, monkeypatch
):
    """``apply_plan`` RETURNS its failures, and ``jobs.drive`` fails only on a raise.

    Measured on 2026-09-02: deleting this raise killed zero tests, because every
    failure driven elsewhere in this file comes out of the membership write rather
    than out of the loop. The report is substituted rather than provoked: what is
    under test is the worker turning a returned failure into a raised one, and
    there is no input to this build that makes ``apply_plan`` fail an entry
    without also failing the write.
    """
    real = apply_cli.apply_outstanding

    def failing(cfg, plan, declared, **kwargs):
        report, gathered = real(cfg, plan, declared, **kwargs)
        from dataclasses import replace as _replace

        return _replace(report, failed={"e-1": "the taxonomy no longer declares this sub"}), gathered

    monkeypatch.setattr(apply_cli, "apply_outstanding", failing)

    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, envelope = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["inner"]["reason"] == "adopt-entries-failed", envelope
    assert artifacts.committed(cut_over, job_id), (
        "the artifact was not committed before the raise, so what happened to the "
        "failed entry survives nowhere"
    )


def test_the_apply_opens_its_own_handle_with_write_intent(cut_over, monkeypatch):
    """The two-process refusal runs BEFORE anything opens, which is a write's open.

    Measured on 2026-09-02: flipping ``require_closed`` to False on the apply's own
    handle killed zero tests, because nothing here has rekordbox running. Driven
    directly against ``_write_memberships`` rather than through the verb, so the
    refusal that arrives is the OPEN's rather than the session's.
    """
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    plan = apply_cli.current_plan(cut_over, DECLARED)
    with pytest.raises(Exception) as excinfo:
        apply_cli._write_memberships(cut_over, plan, DECLARED)
    assert excinfo.value.cause.reason == "rekordbox-running"


def test_the_application_pin_is_what_the_write_intent_open_uniquely_holds(
    cut_over, monkeypatch
):
    """The composite the two-process row owes, because that half is doubly guarded.

    Measured on 2026-09-02: flipping ``require_closed`` to False on the apply's own
    handle killed zero tests EVEN WITH the refusal above driven, and the reason is
    that ``cratekit.core.session`` asserts rekordbox closed for itself before it
    verifies a commit. So the two-process half of that flag is covered twice and
    reverting it changes nothing a test can see.

    The APPLICATION PIN is not. ``assert_app_version`` runs only inside
    ``open_db``'s ``require_closed`` branch and nothing else on this path asks it,
    so a rekordbox that has updated itself since the pin was recorded reaches the
    membership commit with the flag off. This is what the flag holds alone.
    """
    monkeypatch.setattr(rb_writer, "read_installed_app_version", lambda **_: "9.9.9.0002")
    plan = apply_cli.current_plan(cut_over, DECLARED)
    with pytest.raises(Exception) as excinfo:
        apply_cli._write_memberships(cut_over, plan, DECLARED)
    assert excinfo.value.cause.reason == "app-version-pin-drift", (
        "the apply opened a database whose application has moved since the pin "
        "was recorded, and nothing outside the open would have asked"
    )


def _insert_under(cfg: config.Config, prefix: str, content_id: str, genre: str) -> None:
    """One live row whose recorded location sits under a volume this machine is not."""
    import sqlite3

    from cratekit.core import locations

    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        row = conn.execute("SELECT ID FROM djmdGenre WHERE Name = ?", (genre,)).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO djmdGenre (ID, Name, created_at, updated_at) "
                "VALUES (?, ?, ?, ?)",
                ("900", genre, "2026-09-02", "2026-09-02"),
            )
            genre_id = "900"
        else:
            genre_id = row[0]
        conn.execute(
            "INSERT INTO djmdContent (ID, FolderPath, GenreID, rb_local_deleted, "
            "created_at, updated_at) VALUES (?, ?, ?, 0, ?, ?)",
            (
                content_id,
                locations.location_url(Path(prefix) / "Music" / "one.flac"),
                genre_id,
                "2026-09-02",
                "2026-09-02",
            ),
        )
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()


def _record_decision(verb: list[str], gate: str) -> tuple[str, dict]:
    """R34's first two acts, without the third drive."""
    code, refused = drive(verb)
    assert code == int(ExitCode.DECISION_REQUIRED), refused
    run_id = refused["run_id"]
    decided, envelope = drive(
        ["run", "decide", run_id, gate, "approve", "--actor", "a-person"]
    )
    assert decided == int(ExitCode.OK), envelope
    return run_id, refused


# ---------------------------------------------------------------------------
# The gaps the code review found, closed
# ---------------------------------------------------------------------------


def test_a_row_tombstoned_between_queueing_and_driving_fails_its_own_item(machine):
    """rekordbox SOFT deletes, and the reader carries a tombstone on purpose.

    Driven on 2026-09-02 before the fix: the item's row was still in the index so
    the absence guard passed it, ``scan_rows`` then skipped it for being deleted,
    and the single-value unpack raised ``ValueError`` out of the worker. A person
    who removed one track from rekordbox while a census was queued was told to
    report a defect, and every retry told them again.

    The hard-delete twin one test above covers the other half of the condition.
    Both are here because they are different library edits reaching one guard.
    """
    drive(["adopt", "scan"])
    job = _job(registry.entry("adopt.scan").handler_key)

    _tombstone_row(machine, "r-two")

    code, resumed = drive(["adopt", "scan", "--job", job.job_id])
    assert code != int(ExitCode.OK)
    with jobs.open_store() as store:
        items = {item.item_id: item for item in jobs.items(store, job.job_id)}
    assert items["r-two"].state is jobs.ItemState.FAILED
    assert items["r-one"].state is jobs.ItemState.DONE
    assert items["r-two"].cause is not None
    assert items["r-two"].cause.reason == "adopt-item-absent", (
        "a track removed in rekordbox during a queued census reported as an "
        "internal defect rather than as the library edit it is"
    )
    del resumed


def test_a_track_the_tree_write_could_not_place_is_never_marked_applied(
    cut_over, monkeypatch
):
    """R-148's hazard in its new shape: surfaced by the writer, marked by the caller.

    ``write_tree_membership`` SURFACES a row it could not resolve to exactly one
    active library row rather than raising, correctly. The caller then marked
    every outstanding entry applied, including that one, so a track that never
    reached a playlist was recorded as adopted and ``outstanding`` would never
    offer it again. The ledger would say the library holds something it does not.

    Driven by making the write report one row skipped, which is the shape a
    library with two live rows for one file produces.
    """
    from cratekit.write import trees

    real = apply_cli._write_memberships

    def one_skipped(cfg, plan, declared):
        report = real(cfg, plan, declared)
        from dataclasses import replace as _replace

        skipped = trees.RowMatch("a-location-two-rows-claim", trees.MatchOutcome.AMBIGUOUS)
        return _replace(report, skipped=(skipped,))

    monkeypatch.setattr(apply_cli, "_write_memberships", one_skipped)

    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    code, envelope = drive(_resume(job_id))

    assert code != int(ExitCode.OK)
    assert envelope["cause"]["inner"]["reason"] == "adopt-entries-failed", envelope
    assert "a-location-two-rows-claim" in envelope["cause"]["inner"]["message"], (
        "the refusal counted the unplaced rows without naming them, which is not "
        "something a person can act on"
    )
    assert adopt_apply.read(cut_over).entry_ids() == frozenset(), (
        "a track the tree write could not place was recorded as adopted, so the "
        "next run would never offer it again"
    )


def test_the_approval_is_refused_before_anything_is_written(cut_over):
    """``require_approval`` runs inside the loop, which is AFTER the tree write.

    A payload carrying no actor would have written playlist rows into a person's
    database and only then discovered the run was never authorised. The refusal
    is minted up front so it costs nothing.
    """
    _run_id, job_id = approve_and_queue(["adopt", "apply"], "adopt.apply.approve")
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        item = jobs.items(store, job_id)[0]
        unauthorised = replace(job, payload={**job.payload, apply_cli.ACTOR_KEY: ""})

    handler = handlers.resolve(registry.entry("adopt.apply").handler_key)
    with pytest.raises(Exception):
        handler(unauthorised, item, jobs.frozen_config(job))

    assert _memberships(cut_over) == {}, (
        "an unauthorised run wrote membership rows before anything asked whether "
        "it was authorised"
    )


def _tombstone_row(cfg: config.Config, content_id: str) -> None:
    """Set rekordbox's own soft-delete marker, which is what a removal really is."""
    import sqlite3

    conn = sqlite3.connect(Path(cfg.library.db_path))
    try:
        conn.execute(
            "UPDATE djmdContent SET rb_local_deleted = 1 WHERE ID = ?", (content_id,)
        )
        conn.commit()
    finally:
        conn.close()
    collection.reset_cache()
