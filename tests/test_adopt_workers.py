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
        by_id = {str(row.ID): row for row in handle.get_playlist()}
        found: dict[str, list[str]] = {}
        for row in handle.get_playlist():
            members = [
                str(entry.ContentID)
                for entry in handle.get_playlist_songs(PlaylistID=str(row.ID))
            ]
            if members:
                found[str(by_id[str(row.ID)].Name)] = sorted(members)
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
    assert report["gathered"] == {}, "the loop had nothing outstanding, as this test needs"
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
