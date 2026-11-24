"""U32: restore, retention and reconciliation, hermetic: every platform seam is injected."""

from __future__ import annotations

import ast
import dataclasses
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from cratekit.core import (
    config,
    convergence,
    rb_writer,
    reconcile,
    restore,
    session,
    snapshot,
    tree_registry,
)
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from cratekit.modules.tools import backup

UTC = timezone.utc
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

#: The bytes the fixture database holds, and so what every restore puts back.
_GENERATION_ONE = b"database, generation one"
#: A live log holding transactions no capture has.
_LIVE_LOG = b"the live log, transactions committed since the checkpoint"
#: An earlier attempt's staged log, whose only copy is where it sits.
_EARLIER_LOG = b"an earlier attempt's log, recoverable from nowhere else"

#: The identity a foreign disk reports. Any value that is not the fixture's.
_ELSEWHERE = "0000-0000-not-this-disk"


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A saved config with the environment matching, since ``from_dict`` relocates a root (P2)."""
    root = tmp_path / "library"
    (root / "Music").mkdir(parents=True)
    (root / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
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
            "backup": {
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        }
    )
    config.save(built)
    config.reset_cache()
    config.state_path("rekordbox_db", built).write_bytes(_GENERATION_ONE)
    return built


@pytest.fixture(autouse=True)
def _release_process_locks():
    """No test may leave this process believing it still holds a session lock."""
    yield
    session._HELD.clear()


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    """No rekordbox process, injected, so no test depends on this machine."""
    monkeypatch.setattr(
        "cratekit.core.processes.running_process_names", lambda: ()
    )


def _database(cfg) -> Path:
    """The live database the configuration names."""
    return config.state_path("rekordbox_db", cfg)


def matching_identity(cfg):
    return lambda _path: cfg.library.volume_id


def gate_seams(cfg, **overrides):
    """The real gates with only the platform seams injected."""
    arguments = {"identity_provider": matching_identity(cfg), "mount_enumerator": lambda: ()}
    arguments.update(overrides)
    return arguments


def acknowledge(cfg):
    return session.record_acknowledgment(cfg, terminal=lambda: True)


@pytest.fixture
def acked(cfg) -> None:
    """The acknowledgment recorded, as the gated verbs require."""
    acknowledge(cfg)


def always_verified(_path: Path) -> bool:
    """The integrity seam answering yes, since the fixture database is not SQLite."""
    return True


def _refusal(call, /, *arguments, **keywords):
    """The cause of the ``CratekitError`` that ``call`` raises, failing if none is."""
    return _refused(call, *arguments, **keywords).cause


def _refusal_entering(manager, /, *arguments, **keywords):
    """The cause entering ``manager(...)`` raises, failing if the manager admits the body."""
    with pytest.raises(CratekitError) as excinfo:
        with manager(*arguments, **keywords):
            raise AssertionError(f"{manager.__name__} admitted what it should refuse")
    return excinfo.value.cause


def _sweep_refusal(cfg):
    """The cause refusing an ordinary library sweep at the real gates."""
    return _refusal_entering(
        session.assert_gates, cfg, workflow="library-sweep", **gate_seams(cfg)
    )


def _raised(kind: type[BaseException], call, /, *arguments, **keywords):
    """The ``kind`` exception ``call`` raises, failing if it raises none."""
    with pytest.raises(kind) as excinfo:
        call(*arguments, **keywords)
    return excinfo.value


def _refused(call, /, *arguments, **keywords) -> CratekitError:
    """The ``CratekitError`` that ``call`` raises, failing if none is."""
    return _raised(CratekitError, call, *arguments, **keywords)


def write_state(cfg, key: str, payload) -> Path:
    """Put a document at one declared state entry and return its path."""
    path = config.state_path(key, cfg)
    config.atomic_write_bytes(
        (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8"), path
    )
    return path


def take_capture(cfg, *, stamp: str | None = None):
    return snapshot.capture(cfg, stamp=stamp, verifier=always_verified)


def completed_session(
    cfg,
    *,
    workflow: str = "library-sweep",
    trees=(("routing", 3, 1),),
    started: str | None = None,
    stamp: str | None = None,
    state: session.SessionState = session.SessionState.CLOSED,
):
    """One captured, committed, ended session with the change summary an override names."""
    record = session.open_session(cfg, workflow=workflow, sources=("source-a",))
    if started is not None:
        record.started = started
        session.write_record(record, cfg)
    captured = take_capture(cfg, stamp=stamp)
    session.attach_capture(record, captured.root, cfg)
    record.sources["source-a"] = str(session.SourceState.COMMITTED)
    record.change = session.ChangeSummary(
        tuple(
            session.TreeChange(tree=tree, created=created, updated=updated)
            for tree, created, updated in trees
        )
    )
    record.state = state
    record.ended = record.ended or "2026-08-02T00:00:00+00:00"
    session.write_record(record, cfg)
    return record, captured


def _planned(cfg, held, **session_options):
    """One completed session, and the restore plan for it under ``held``."""
    record, _captured = completed_session(cfg, **session_options)
    return record, restore.plan(cfg, record.session_id, held=held)


def _restored(cfg, record, held):
    """The plan for ``record`` under ``held``, and the outcome of running it."""
    decided = restore.plan(cfg, record.session_id, held=held)
    return decided, restore.run(decided, cfg, held=held)


def _routing_marker(cfg):
    """One recorded tree marker on ``routing``, the latch a pre-cutover restore leaves."""
    return reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )


@pytest.fixture
def held(cfg):
    """One open recovery session, the way the verb will hold it."""
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        yield open_session


@pytest.fixture
def record(cfg) -> session.SessionRecord:
    """One completed session, from ``completed_session``."""
    return completed_session(cfg)[0]


@pytest.fixture
def decided(cfg, held) -> restore.Plan:
    """The restore plan for one completed session, under ``held``."""
    return _planned(cfg, held)[1]


@pytest.fixture
def target(tmp_path) -> Path:
    """An empty directory to recover onto."""
    (tmp_path / "recovered").mkdir()
    return tmp_path / "recovered"


@pytest.fixture
def replacement(tmp_path) -> Path:
    """An empty replacement drive to recover onto."""
    (tmp_path / "replacement").mkdir()
    return tmp_path / "replacement"


# Scenario 1 (AE18): a completed session is listed and its capture restores


def test_a_completed_session_is_listed_with_its_timestamp_workflow_and_changes(cfg, record):
    listed = restore.list_sessions(cfg)
    assert [entry.session_id for entry in listed] == [record.session_id]
    only = listed[0]
    assert only.started == record.started
    assert only.workflow == "library-sweep"
    assert [(t.tree, t.created, t.updated) for t in only.change.trees] == [("routing", 3, 1)]
    assert only.restorable


def test_a_restore_returns_a_modified_database_to_its_pre_session_bytes(cfg, held):
    """Exact pre-session bytes come back, proven on a synthetic library only."""
    before = _database(cfg).read_bytes()
    record, _captured = completed_session(cfg)
    _database(cfg).write_bytes(b"database, generation two")
    _restored(cfg, record, held)
    assert _database(cfg).read_bytes() == before


def test_a_restore_returns_the_coupled_state_with_the_database(cfg, held):
    """The coupling IS the unit. Either both roll back or the capture is useless."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "after"})
    _database(cfg).write_bytes(b"database, generation two")
    _restored(cfg, record, held)
    assert json.loads(config.state_path("label_watermarks", cfg).read_text()) == {
        "source": "before"
    }


def test_a_coupled_file_the_capture_records_as_absent_is_removed_again(cfg, held, record):
    """Absence in a manifest is an instruction, so a file created later goes."""
    created_after = write_state(cfg, "tombstones", {"version": 1, "store": "tombstones"})
    assert created_after.exists()
    _restored(cfg, record, held)
    assert not created_after.exists()


def test_an_unusable_capture_is_still_listed_and_says_why(cfg):
    record, captured = completed_session(cfg)
    (captured.root / snapshot.MANIFEST_NAME).unlink()

    only = restore.list_sessions(cfg)[0]

    assert only.session_id == record.session_id
    assert not only.restorable
    assert "could not be read" in only.unusable


def test_a_capture_that_failed_its_integrity_check_is_never_restored_from(cfg, held):
    record = session.open_session(cfg, workflow="library-sweep")
    captured = snapshot.capture(cfg, verifier=lambda _path: False)
    session.attach_capture(record, captured.root, cfg)

    cause = _refusal(restore.plan, cfg, record.session_id, held=held)

    assert cause.reason == "snapshot-integrity-failed"


# Scenario 2: restoring across a later committed session


def test_restoring_across_a_later_committed_session_refuses_and_names_the_counts(cfg, held):
    older, _ = completed_session(cfg, started="2026-08-01T09:00:00+00:00", stamp="older")
    completed_session(
        cfg,
        started="2026-08-02T09:00:00+00:00",
        stamp="newer",
        trees=(("routing", 7, 2), ("intake", 1, 0)),
    )

    cause = _refusal(restore.plan, cfg, older.session_id, held=held)

    assert cause.reason == "restore-discards-committed-work"
    assert cause.code is ExitCode.DECISION_REQUIRED
    # Tree and count, since one aggregate cannot answer the question asked.
    assert "routing: 7 created, 2 updated" in cause.message
    assert "intake: 1 created, 0 updated" in cause.message


def test_the_override_has_to_name_exactly_the_sessions_it_discards(cfg, held):
    older, _ = completed_session(cfg, started="2026-08-01T09:00:00+00:00", stamp="older")
    newer, _ = completed_session(cfg, started="2026-08-02T09:00:00+00:00", stamp="newer")

    cause = _refusal(
        restore.plan, cfg, older.session_id, held=held, discarding=["not-that-session"]
    )
    assert cause.reason == "restore-discards-committed-work"

    decided = restore.plan(cfg, older.session_id, held=held, discarding=[newer.session_id])

    assert decided.discarded_sessions == (newer.session_id,)


def test_a_later_session_that_committed_nothing_does_not_need_an_override(cfg, held):
    """A session that wrote nothing discards nothing, so reaching past it must not ask."""
    older, _ = completed_session(cfg, started="2026-08-01T09:00:00+00:00", stamp="older")
    idle = session.open_session(cfg, workflow="library-sweep", sources=("source-b",))
    idle.started = "2026-08-02T09:00:00+00:00"
    session.close_session(idle, cfg, state=session.SessionState.ABANDONED)

    decided = restore.plan(cfg, older.session_id, held=held)

    assert decided.discarded_sessions == ()


# Scenario 3: reconciliation of what a restore cannot undo


def test_a_restore_lists_every_effect_it_cannot_undo_and_blocks_convergence(cfg, held):
    """An advanced watermark and a written tombstone do not roll back with the rows."""
    write_state(cfg, "label_watermarks", {"source": "2026-07-01"})
    record, _captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "2026-08-02"})
    write_state(cfg, "tombstones", {"version": 1, "store": "tombstones", "decisions": []})

    decided = restore.plan(cfg, record.session_id, held=held)

    effects = {
        (marker.identity, marker.effect)
        for marker in decided.markers
        if marker.kind is reconcile.Kind.EFFECT
    }
    assert effects == {
        ("label_watermarks", config.RollbackEffect.DOWNLOADED_FILE),
        ("label_watermarks", config.RollbackEffect.REMOTE_PLAYLIST_PREFIX),
        ("tombstones", config.RollbackEffect.TRASHED_FILE),
    }

    outcome = restore.run(decided, cfg, held=held)
    assert len(outcome.outstanding) == 3
    assert not outcome.converged
    assert not reconcile.converged(cfg)

    for marker_id in outcome.outstanding[:-1]:
        reconcile.close_marker(
            cfg, marker_id, disposition=reconcile.Disposition.ACCEPTED, actor="tester"
        )
    assert not reconcile.converged(cfg), "one open marker still blocks convergence"

    reconcile.close_marker(
        cfg, outcome.outstanding[-1], disposition=reconcile.Disposition.REPAIRED, actor="tester"
    )
    assert reconcile.converged(cfg)


def _one_effect_marker(cfg, *, session_id="s", capture_stamp="c"):
    """One EFFECT marker, which is the kind this module latches on."""
    return reconcile.record_markers(
        cfg,
        [
            reconcile.Marker(
                kind=reconcile.Kind.EFFECT,
                identity="label_watermarks",
                effect=config.RollbackEffect.DOWNLOADED_FILE,
                session_id=session_id,
                capture_stamp=capture_stamp,
                detail="audio landed and did not roll back",
            )
        ],
    )


def test_an_unreconciled_restore_refuses_the_next_ordinary_session(cfg, acked):
    _one_effect_marker(cfg)
    cause = _sweep_refusal(cfg)
    assert cause.reason == "restore-reconciliation-outstanding"
    assert cause.code is ExitCode.UNCONVERGED


def test_a_recovery_is_not_refused_by_the_latch_whose_remedy_it_is(cfg, acked):
    """A latch may not condemn its own remedy, and a second restore is one (U8)."""
    _one_effect_marker(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        assert open_session.intent is session.Intent.RECOVERY


def test_the_markers_are_enumerated_before_anything_is_replaced(cfg, held):
    """The ordering is the correctness: afterwards every comparison is equal."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "after"})

    decided = restore.plan(cfg, record.session_id, held=held)

    assert decided.steps[0].act is restore.Act.RECORD
    assert all(step.act is not restore.Act.RECORD for step in decided.steps[1:])


def test_a_marker_is_keyed_on_a_persisted_identity_rather_than_a_display_name(cfg):
    """Markers key on the inventory key or stable tree id, never a renamable name."""
    declared = {entry.key for entry in config.STATE_FILES}
    write_state(cfg, "label_watermarks", {"source": "2026-08-02"})
    write_state(cfg, "tombstones", {"version": 1, "store": "tombstones"})

    markers = reconcile.effect_markers(
        cfg, captured={}, session_id="s", capture_stamp="c"
    )

    assert markers, "the derivation found nothing to key on"
    for marker in markers:
        assert marker.identity in declared
    trees = reconcile.tree_markers(["routing"], session_id="s")
    assert trees[0].identity == "routing"


def test_recording_the_same_marker_twice_does_not_reopen_a_closed_one(cfg):
    markers = reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    recorded = reconcile.record_markers(cfg, markers)
    reconcile.close_marker(
        cfg, recorded[0].marker.marker_id, disposition=reconcile.Disposition.REPAIRED, actor="t"
    )

    again = reconcile.record_markers(cfg, markers)

    assert len(again) == 1
    assert not again[0].outstanding


# Scenario 4: a restore predating a cutover


def _cut_over(cfg, tree_id: str = "routing") -> None:
    """Flip a tree to database-native, passing ``source`` only where the signature takes it."""
    extra = {}
    if "source" in inspect.signature(tree_registry.record_cutover).parameters:
        extra["source"] = tree_registry.DerivationSource.TAXONOMY
    tree_registry.record_cutover(
        cfg, tree_id, root_id="row-1", on=date(2026, 8, 2), **extra
    )


def _tree_is_recorded_short(cfg, tree_id: str) -> bool:
    """Whether the fact landed, asked of whichever store owns it on this build."""
    if tree_id in reconcile.unconverged_trees(cfg):
        return True
    try:
        from cratekit.core import convergence  # noqa: PLC0415
    except ImportError:
        return False
    return tree_id in convergence.read(cfg).blocking_trees()


def _assert_the_next_write_is_refused_over(cfg, tree_id: str) -> None:
    """The next governed write refuses over this tree; each store has its own slug."""
    if tree_id in reconcile.unconverged_trees(cfg):
        cause = _sweep_refusal(cfg)
        assert cause.reason == "restore-reconciliation-outstanding"
        assert cause.detail["unconverged_trees"] == [tree_id]
        return

    from cratekit.core import convergence  # noqa: PLC0415

    cause = _refusal(convergence.assert_converged, cfg, tree_id)
    assert cause.reason == "tree-unconverged"
    assert cause.detail["tree_id"] == tree_id


def test_a_restore_predating_a_cutover_marks_that_tree_unconverged(cfg, held, record):
    _cut_over(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    assert decided.unconverged == ("routing",)
    restore.run(decided, cfg, held=held)
    assert _tree_is_recorded_short(cfg, "routing")


def test_a_restore_taken_after_the_cutover_marks_nothing(cfg, held):
    """P7: a capture taken after the flip already says database native, so no rebuild."""
    _cut_over(cfg)
    record, decided = _planned(cfg, held)

    assert decided.unconverged == ()


def test_an_unconverged_tree_refuses_the_next_sync_and_the_next_close(cfg, acked):
    """A pre-cutover restore's tree marker refuses the next session and the next close."""
    _routing_marker(cfg)
    sync_refusal = _sweep_refusal(cfg)
    stranded = session.open_session(cfg, workflow="library-sweep")
    close_refusal = _refusal(session.close_session, stranded, cfg, **gate_seams(cfg))
    for refusal in (sync_refusal, close_refusal):
        assert refusal.reason == "restore-reconciliation-outstanding"
        assert refusal.code is ExitCode.UNCONVERGED
    assert "never by a decision" in close_refusal.message
    assert close_refusal.detail["unconverged_trees"] == ["routing"]


def test_a_pre_cutover_restore_leaves_the_next_session_refused(cfg, held, acked, record):
    """The same property end to end, the shape once measured as allowed."""
    _cut_over(cfg)
    decided, _outcome = _restored(cfg, record, held)
    assert decided.unconverged == ("routing",)
    assert _tree_is_recorded_short(cfg, "routing")
    _assert_the_next_write_is_refused_over(cfg, "routing")


def test_a_rebuild_can_declare_itself_and_is_not_refused_by_this_latch(cfg, acked):
    """A rebuild can declare ``Intent.RECOVERY`` and pass, so the latch has a remedy."""
    _routing_marker(cfg)
    with session.assert_gates(
        cfg,
        workflow="tree-rebuild",
        intent=session.Intent.RECOVERY,
        **gate_seams(cfg),
    ) as gates:
        assert gates.intent is session.Intent.RECOVERY


def test_abandoning_a_run_is_never_gated_on_convergence(cfg):
    """Only close is gated, or a run could be neither finished nor given up."""
    _one_effect_marker(cfg)
    stranded = session.open_session(cfg, workflow="library-sweep")

    ended = session.close_session(stranded, cfg, state=session.SessionState.ABANDONED)

    assert ended.state is session.SessionState.ABANDONED


def test_closing_the_effect_marker_lets_the_next_session_through(cfg, acked):
    recorded = _one_effect_marker(cfg)
    reconcile.close_marker(
        cfg,
        recorded[0].marker.marker_id,
        disposition=reconcile.Disposition.ACCEPTED,
        actor="phillip",
    )
    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"


def test_clearing_the_tree_marker_lets_the_next_session_through(cfg, acked):
    """A tree marker closed REPAIRED by a rebuild lifts the refusal."""
    recorded = _routing_marker(cfg)
    assert reconcile.unconverged_trees(cfg) == ("routing",)
    reconcile.close_marker(
        cfg,
        recorded[0].marker.marker_id,
        disposition=reconcile.Disposition.REPAIRED,
        actor="tree-rebuild",
        note="the convergence check after the rebuild reported no difference",
    )
    assert reconcile.unconverged_trees(cfg) == ()
    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"
    stranded = session.open_session(cfg, workflow="library-sweep")
    assert (
        session.close_session(stranded, cfg, **gate_seams(cfg)).state
        is session.SessionState.CLOSED
    )


def test_retraction_touches_the_transient_latch_and_nothing_else(cfg):
    """Retraction discharges the in-flight fact only, never a judgement."""
    reconcile.record_markers(
        cfg,
        [
            *reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c"),
            reconcile.in_flight_marker(capture_stamp="capture-1"),
        ],
    )
    _one_effect_marker(cfg)

    discharged = reconcile.retract_in_flight(cfg)

    assert len(discharged) == 1
    assert reconcile.unconverged_trees(cfg) == ("routing",)
    assert any(
        record.marker.kind is reconcile.Kind.EFFECT
        for record in reconcile.outstanding(cfg)
    )


# Scenario 5: retention


def _age_capture(root: Path, *, days: int, now: datetime) -> None:
    when = (now - timedelta(days=days)).timestamp()
    os.utime(root, (when, when))


def test_pruning_refuses_before_the_session_it_belongs_to_has_committed(cfg):
    record = session.open_session(cfg, workflow="library-sweep")
    captured = take_capture(cfg)
    session.attach_capture(record, captured.root, cfg)

    cause = _refusal(restore.prune, cfg, owning=record)

    assert "has not committed" in cause.message
    assert captured.root.is_dir()

    session.close_session(record, cfg, **gate_seams(cfg))
    assert restore.prune(cfg, owning=record) == ()


def test_retention_never_removes_a_capture_an_open_run_references(cfg):
    """R30 in one sentence: a capture an unfinished run may restore from is not old."""
    now = datetime.now(UTC)
    open_record = session.open_session(cfg, workflow="library-sweep")
    protected = take_capture(cfg, stamp="protected")
    session.attach_capture(open_record, protected.root, cfg)
    _age_capture(protected.root, days=400, now=now)
    orphan = take_capture(cfg, stamp="orphan")
    _age_capture(orphan.root, days=400, now=now)

    decided = restore.retention_plan(
        cfg, policy=restore.RetentionPolicy(keep=0), now=now
    )

    assert [entry.root for entry in decided.deleting] == [orphan.root]
    assert protected.root in [entry.root for entry in decided.keeping]


def test_retention_respects_the_age_bound(cfg):
    now = datetime.now(UTC)
    fresh = take_capture(cfg, stamp="fresh")
    stale = take_capture(cfg, stamp="stale")
    _age_capture(stale.root, days=90, now=now)

    decided = restore.retention_plan(
        cfg,
        policy=restore.RetentionPolicy(keep=0, max_age=timedelta(days=30)),
        protected_provider=set,
        now=now,
    )

    assert [entry.root for entry in decided.deleting] == [stale.root]
    assert [entry.root for entry in decided.keeping] == [fresh.root]


def test_retention_respects_the_byte_bound_as_well_as_count_and_age(cfg):
    """The byte bound deletes even when count and age would keep everything."""
    now = datetime.now(UTC)
    made = []
    for index in range(4):
        captured = take_capture(cfg, stamp=f"capture-{index}")
        _age_capture(captured.root, days=4 - index, now=now)
        made.append(captured)
    total = sum(
        sum(path.stat().st_size for path in entry.root.rglob("*") if path.is_file())
        for entry in made
    )

    decided = restore.retention_plan(
        cfg,
        policy=restore.RetentionPolicy(keep=0, max_age=None, max_bytes=total // 2),
        protected_provider=set,
        now=now,
    )

    assert decided.deleting, "the byte bound deleted nothing"
    assert sum(entry.size for entry in decided.keeping) <= total // 2
    # Oldest first, since the byte bound is the least specific of the three.
    assert decided.deleting[-1].root == made[0].root


def test_a_provider_that_raises_deletes_nothing(cfg):
    take_capture(cfg, stamp="only")

    def broken() -> set[Path]:
        raise RuntimeError("the log could not be read")

    decided = restore.retention_plan(
        cfg, policy=restore.RetentionPolicy(keep=0, max_age=None), protected_provider=broken
    )

    assert decided.deleting == ()


def test_prune_deletes_exactly_what_the_plan_named(cfg):
    now = datetime.now(UTC)
    keep = take_capture(cfg, stamp="keep")
    drop = take_capture(cfg, stamp="drop")
    _age_capture(drop.root, days=90, now=now)
    policy = restore.RetentionPolicy(keep=0, max_age=timedelta(days=30))

    decided = restore.retention_plan(cfg, policy=policy, protected_provider=set, now=now)
    removed = restore.prune(cfg, policy=policy, protected_provider=set, now=now)

    assert removed == tuple(entry.root for entry in decided.deleting)
    assert not drop.root.exists()
    assert keep.root.is_dir()


def test_the_capture_store_sharing_the_database_volume_is_reported(cfg):
    """R30: sharing the database volume is reported, not refused, by filesystem identifier."""
    take_capture(cfg, stamp="one")

    decided = restore.retention_plan(cfg)

    assert decided.shares_the_database_volume is True


# Scenario 6: capacity


def test_a_session_refuses_before_snapshotting_when_the_store_cannot_fit_one(
    cfg, monkeypatch, acked
):
    """A real session refuses at the capture, never committing behind a truncated copy."""
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 1)
    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
        record = session.open_session(cfg, workflow="library-sweep")
        cause = _refusal(snapshot.capture, cfg, verifier=always_verified)

    assert cause.reason == "snapshot-store-full"
    assert record.snapshot_path is None, "a refused capture is never attached"


def test_a_refused_capture_leaves_no_partial_file(cfg, monkeypatch):
    """Refuse before the copy, never part way, or a truncated capture is committed behind."""
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 1)
    store = snapshot.store_root(cfg)
    before = _fingerprint(store.parent)

    cause = _refusal(snapshot.capture, cfg, verifier=always_verified)

    assert cause.reason == "snapshot-store-full"
    assert cause.code is ExitCode.PRECONDITION
    assert cause.remediation.steps, "freeing disk is not a command, so it rides as steps"
    assert _fingerprint(store.parent) == before
    assert not store.exists() or not any(store.iterdir())


def test_the_capacity_estimate_is_derived_from_the_same_set_the_copy_uses(cfg):
    """An estimate built from its own list is a list in disguise (P4)."""
    write_state(cfg, "label_watermarks", {"source": "x" * 5000})

    needed = snapshot.assert_room_for_capture(cfg, free_bytes=10**9)

    assert needed >= 5000


def test_free_space_that_cannot_be_read_refuses_rather_than_passing(cfg, monkeypatch):
    """Unreadable free space refuses, since ``statvfs`` failing means the path is vanishing."""
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: None)

    cause = _refusal(snapshot.capture, cfg, verifier=always_verified)

    assert cause.reason == "snapshot-store-full"
    assert "could not be read" in cause.message


def test_the_capacity_estimate_counts_allocation_rather_than_apparent_size(cfg):
    """BLOCKING 3: allocated blocks, since small documents under-reported by up to 68x."""
    queue = config.state_path("review_queue", cfg)
    queue.mkdir(parents=True, exist_ok=True)
    for index in range(500):
        (queue / f"item-{index:05d}.json").write_bytes(b"x" * 120)

    estimate = snapshot.assert_room_for_capture(cfg, free_bytes=10**12)
    allocated = sum(
        entry.stat().st_blocks * 512 for entry in queue.iterdir() if entry.is_file()
    )

    assert estimate >= allocated, "the estimate is below what the queue alone occupies"
    apparent = sum(entry.stat().st_size for entry in queue.iterdir() if entry.is_file())
    assert allocated > apparent * 4, "the fixture is not the shape this test is about"


def _file_stats(root):
    """Each file under ``root`` with its ``stat``, skipping one that vanishes mid walk."""
    for current, _directories, files in os.walk(root):
        for name in files:
            try:
                yield Path(current) / name, (Path(current) / name).stat()
            except OSError:
                continue


def _fingerprint(root: Path) -> dict[str, int]:
    return {str(path): stat.st_size for path, stat in _file_stats(root)}


# The registered obligations: the derived set and the companion asymmetry


def test_a_restore_replaces_exactly_the_derived_coupled_set(cfg, held):
    """Every target comes from the inventory, and nothing else is reachable."""
    record, captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)

    allowed = restore.restorable_targets(cfg)
    touched = {step.target for step in decided.steps if step.target is not None}
    assert touched
    assert touched <= allowed


def test_no_restore_target_is_a_lock_or_a_record_that_survives_a_rollback(cfg):
    """No restore target is a lock or a rollback survivor, walked over the inventory (P3)."""
    allowed = restore.restorable_targets(cfg)
    local = config.library_local_dir(cfg)
    history = config.library_history_dir(cfg)

    for entry in config.STATE_FILES:
        if entry.root is not config.StateRoot.LIBRARY or entry.medium is config.Medium.KEYCHAIN:
            continue
        path = config.state_path(entry.key, cfg)
        if entry.snapshot is config.SnapshotRole.COUPLED:
            continue
        assert path not in allowed, f"{entry.key} is {entry.snapshot} and is reachable"

    for target in allowed:
        assert local not in target.parents and target != local
        assert history not in target.parents and target != history


def test_the_reconciliation_lock_is_its_own_entry_and_lives_elsewhere(cfg):
    """U11's lesson, and this is the unit that proves it, because this is the restore."""
    document = config.state_file(reconcile.STATE_KEY)
    lock = config.state_file(reconcile.LOCK_KEY)

    assert document.snapshot is config.SnapshotRole.SURVIVES_ROLLBACK
    assert lock.snapshot is config.SnapshotRole.NEVER_RESTORED
    assert reconcile.lock_path(cfg).parent != reconcile.path_for(cfg).parent
    assert reconcile.lock_path(cfg) not in restore.restorable_targets(cfg)


def test_the_live_companion_files_are_cleared_before_anything_is_copied(cfg, held, decided):
    acts = [step.act for step in decided.steps if step.act is not restore.Act.RECORD]
    first_copy = next(
        index for index, act in enumerate(acts) if act in {restore.Act.REPLACE, restore.Act.REPLACE_TREE}
    )
    assert all(act is restore.Act.CLEAR for act in acts[:first_copy])
    cleared = {step.target for step in decided.steps if step.act is restore.Act.CLEAR}
    assert cleared == set(config.sidecar_paths("rekordbox_db", cfg))


def test_only_the_companion_the_inventory_declares_restored_is_written_back(cfg, held):
    """A stale shared-memory index beside a fresh log gives the engine two views."""
    database = _database(cfg)
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"companion, generation one")
    record, _captured = completed_session(cfg)
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"companion, generation two")

    _restored(cfg, record, held)
    restored = set(config.sidecar_paths("rekordbox_db", cfg, restored_only=True))
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        if companion in restored:
            assert companion.read_bytes() == b"companion, generation one"
        else:
            assert not companion.exists(), "a derived companion was written back"
    assert database.exists()


def _restore_sources() -> str:
    """``restore.py`` and its parts (U300), so a scan of the module reads all of it."""
    from tests._split_modules import source_of  # noqa: PLC0415

    return source_of("cratekit.core.restore")


def test_the_restore_module_spells_no_companion_suffix_of_its_own(cfg):
    """A literal companion suffix here is the list the schema abolishes."""
    source = _restore_sources()
    assert "sidecar_paths" in source
    assert not re.search(r"""["'][^"']*-(?:wal|shm)""", source)


# The registered obligations: one held session, and the resolved record


def test_one_session_spans_the_plan_and_the_run(cfg, held, decided):
    """A real second process is refused between plan and run, so no commit fits between."""
    contender = _lock_taken_in_another_process(session.lock_path(cfg))
    assert contender != 0, "the library lock was released between the plan and the run"
    restore.run(decided, cfg, held=held)
    assert _lock_taken_in_another_process(session.lock_path(cfg)) != 0


def _lock_taken_in_another_process(path: Path) -> int:
    """Try the lock from a real second interpreter, since a thread proves nothing; 0 is taken."""
    script = (
        "import fcntl, os, sys\n"
        "handle = open(sys.argv[1], 'a+')\n"
        "try:\n"
        "    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
        "except OSError:\n"
        "    sys.exit(3)\n"
        "sys.exit(0)\n"
    )
    return subprocess.run(
        [sys.executable, "-c", script, str(path)], capture_output=True
    ).returncode


def test_the_backup_restore_runs_inside_the_already_open_session(cfg, held, target):
    """Handed the held guard, the backup plan and run never take the lock again."""
    commands = []

    def runner(command):
        commands.append(command.label)
        return backup.CommandResult(returncode=0, stdout="2026-08-01T000000Z\n")

    decided = backup.plan_restore(
        cfg,
        target=target,
        confirmed=True,
        snapshot="2026-08-01T000000Z",
        runner=runner,
        process_lister=lambda: (),
        gates=held.guard,
    )
    backup.run_restore(decided, cfg, runner=runner, dry_run=True, gates=held.guard)
    assert backup.RESTORE_DATABASE in commands
    assert _lock_taken_in_another_process(session.lock_path(cfg)) != 0


def test_a_successful_restore_resolves_the_record_that_condemns_the_library(cfg, held):
    """The restore resolves the latch it remedies, or the next write is still refused."""
    record, _captured = completed_session(
        cfg, state=session.SessionState.COMMITTED_UNVERIFIED
    )
    _decided, outcome = _restored(cfg, record, held)
    assert outcome.resolved == (record.session_id,)
    assert (
        session.read_record(record.session_id, cfg).state is session.SessionState.ABANDONED
    )
    session.assert_no_unresolved_session(cfg)


def test_the_recovery_session_closes_its_own_record_on_both_paths(cfg, acked):
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        good = open_session.record.session_id
    assert session.read_record(good, cfg).state is session.SessionState.CLOSED
    with pytest.raises(RuntimeError):
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            bad = open_session.record.session_id
            raise RuntimeError("the restore failed part way")
    assert session.read_record(bad, cfg).state is session.SessionState.ABANDONED


def test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished(cfg, acked):
    """The record closes after the analysis watch judges (R-375)."""
    grids = Path(cfg.library.root) / "PIONEER" / "USBANLZ"
    grids.mkdir(parents=True)
    grid = grids / "ANLZ0000.DAT"
    grid.write_bytes(b"a grid")
    with pytest.raises(CratekitError) as excinfo:
        with restore.recovery_session(
            cfg, analysis_roots=[grids.parent], **gate_seams(cfg)
        ) as open_session:
            refused = open_session.record.session_id
            grid.write_bytes(b"a different grid, longer")

    assert excinfo.value.cause.reason == "anlz-modified"
    assert session.read_record(refused, cfg).state is session.SessionState.ABANDONED


def test_a_restore_refuses_without_each_of_the_three_gates(cfg):
    """KTD24: three refusals, three distinct codes, nothing written on any."""

    def refuse_with(**arguments) -> ExitCode:
        before = _fingerprint(cfg.library.root)
        cause = _refusal_entering(restore.recovery_session, cfg, **arguments)
        assert _fingerprint(cfg.library.root) == before
        return cause.code

    wrong_volume = refuse_with(
        identity_provider=lambda _path: _ELSEWHERE, mount_enumerator=lambda: ()
    )
    no_acknowledgment = refuse_with(**gate_seams(cfg))

    acknowledge(cfg)
    lock = session.lock_path(cfg)
    config.mkdir_private(lock.parent)
    lock.touch()
    with _holding(lock):
        held_lock = refuse_with(**gate_seams(cfg))

    codes = (held_lock, no_acknowledgment, wrong_volume)
    assert codes == (
        ExitCode.LIBRARY_BUSY,
        ExitCode.ACK_REQUIRED,
        ExitCode.LIBRARY_UNAVAILABLE,
    )
    assert len(set(codes)) == 3, "three refusals that cannot be told apart is one refusal"


class _holding:
    """Hold an advisory lock on a path from a second file description."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.handle = None

    def __enter__(self):
        import fcntl

        self.handle = open(self.path, "a+")
        fcntl.flock(self.handle, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc_info) -> None:
        if self.handle is not None:
            self.handle.close()


# The registered obligation: bare-metal recovery


def _volume_is_gone(cfg) -> dict:
    """The configured library unreachable, as a dead disk; ``mount_probe`` answers yes."""
    shutil.rmtree(cfg.library.root, ignore_errors=True)
    return _foreign_volume(cfg)


@pytest.fixture
def seams(cfg) -> dict:
    """The volume seams of a library whose disk is gone."""
    return _volume_is_gone(cfg)


def _session_onto(cfg, target, seams, *, acknowledged=True, terminal=True, **more):
    """A bare-metal session onto ``target`` through the volume seams ``seams``."""
    return restore.bare_metal_session(
        cfg,
        target=target,
        acknowledged=acknowledged,
        terminal=lambda: terminal,
        **more,
        **seams,
    )


def test_bare_metal_recovery_is_refused_while_the_library_is_reachable(cfg, target):
    # Only the identity gate can refuse, on a phrase the stub refusal lacks (U96 row C5).
    seams = {**gate_seams(cfg), "mount_probe": lambda _path: True}
    cause = _refusal_entering(_session_onto, cfg, target, seams)
    assert cause.reason == "recovery-target-refused"
    assert "nothing to recover from bare metal" in cause.message


def test_a_volume_mounted_elsewhere_is_not_the_same_as_a_volume_that_is_gone(
    cfg, tmp_path, target, seams
):
    """Three answers, not two: present, absent, and mounted elsewhere."""
    somewhere = tmp_path / "somewhere-else"
    somewhere.mkdir()
    seams["identity_provider"] = (
        lambda path: cfg.library.volume_id if path == somewhere else _ELSEWHERE
    )
    seams["mount_enumerator"] = lambda: (somewhere,)
    cause = _refusal_entering(_session_onto, cfg, target, seams)
    assert "not absent" in cause.message


def test_a_platform_that_cannot_report_an_identity_is_not_a_volume_that_is_gone(cfg, target, seams):
    seams["identity_provider"] = lambda _path: None
    cause = _refusal_entering(_session_onto, cfg, target, seams)
    assert "not absent" in cause.message


def test_bare_metal_recovery_refuses_the_stub_an_unmounted_volume_leaves_behind(
    cfg, tmp_path, seams
):
    """An unmounted volume's empty folder is refused by filesystem identifier."""
    seams["mount_probe"] = lambda _path: False
    stub = Path(cfg.library.root)
    stub.mkdir(parents=True)
    cause = _refusal_entering(_session_onto, cfg, stub, seams)
    assert "empty folder an unmounted volume leaves behind" in cause.message


@pytest.mark.parametrize(
    "name, why",
    [
        (
            "library/Music",
            "a subdirectory of the configured root is the same empty folder one "
            "level down, and an equality test passes it",
        ),
        (
            "library 1",
            "an operating system that finds a mount point occupied mounts the "
            "volume beside it under a suffixed name, so the stale stub and the "
            "live volume sit next to each other with names one character apart",
        ),
    ],
)
def test_bare_metal_recovery_refuses_the_stubs_beside_and_beneath_the_mount_point(
    cfg, tmp_path, name, why, seams
):
    """ACCEPTED 1: the equality test caught one shape of the internal disk, not three."""
    seams["mount_probe"] = lambda _path: False
    target = tmp_path / name
    target.mkdir(parents=True)
    cause = _refusal_entering(_session_onto, cfg, target, seams)
    assert "unmounted volume leaves behind" in cause.message, why


def test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory(
    cfg, tmp_path, seams
):
    """ACCEPTED 2: the occupancy check is recursive, as the default layout nests the database."""
    target = tmp_path / "recovered"
    (target / "db").mkdir(parents=True)
    (target / "db" / "master.db").write_bytes(b"somebody else's library")
    cause = _refusal_entering(_session_onto, cfg, target, seams)
    assert "named for replacement" in cause.message


def test_bare_metal_recovery_opens_over_databases_it_would_not_replace(cfg, tmp_path, seams):
    """R-592: databases the recovery would not replace neither refuse it nor are touched."""
    target = tmp_path / "recovered"
    left = {
        ".cratekit/queue.db": b"the queue the mirror carried",
        ".cratekit/snapshots/one/master.db": b"a capture the mirror carried",
        "deep/er/master.db": b"somebody else's library, elsewhere on the drive",
    }
    for relative, body in left.items():
        (target / relative).parent.mkdir(parents=True, exist_ok=True)
        (target / relative).write_bytes(body)

    with _session_onto(cfg, target, seams) as open_session:
        assert open_session.authorises == target

    assert {r: (target / r).read_bytes() for r in left} == left


def test_the_occupancy_fileset_is_the_one_the_restore_plan_writes(cfg, tmp_path):
    """The guard and the transfer re-base the database separately; held together here."""
    fileset = restore.recovered_database_fileset(cfg, tmp_path)
    assert fileset[0] == tmp_path / "db" / "master.db"
    assert fileset[0] == backup.database_target_for(cfg, tmp_path)
    assert {p.name for p in fileset[1:]} >= {"master.db-wal", "master.db-shm"}
    assert all(p.parent == fileset[0].parent for p in fileset)

    outside = dataclasses.replace(
        cfg,
        library=dataclasses.replace(
            cfg.library,
            db_path=tmp_path / "home" / "master.db",
            db_outside_root_acknowledged_on="2026-09-21",
        ),
    )
    assert restore.recovered_database_fileset(outside, tmp_path)[0] == tmp_path / "master.db"
    assert restore.recovered_database_fileset(outside, tmp_path)[0] == (
        backup.database_target_for(outside, tmp_path)
    )


def test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library(cfg, tmp_path, seams):
    """A companion alone occupies a target, since every companion is cleared (R-592)."""
    target = tmp_path / "recovered"
    (target / "db").mkdir(parents=True)
    (target / "db" / "master.db-wal").write_bytes(b"somebody else's library")
    cause = _refusal_entering(_session_onto, cfg, target, seams)
    assert "named for replacement" in cause.message
    with _session_onto(cfg, target, seams, replacing_existing=True) as open_session:
        assert open_session.workflow == "bare-metal-recovery"

    # Distinct, not read off the constants: one log field keeps the weaker gates visible.
    labels = {
        restore.BARE_METAL_WORKFLOW, restore.CAPTURE_RESTORE_WORKFLOW, backup.RESTORE_WORKFLOW
    }
    assert len(labels) == 3, "two workflows that land in the same log field share a label"


def test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision(cfg, target, seams):
    """R34's acknowledgment lived on the dead volume, so a terminal and a decision stand in."""
    no_terminal = _refusal_entering(_session_onto, cfg, target, seams, terminal=False)
    assert "no controlling terminal" in no_terminal.message
    not_accepted = _refusal_entering(_session_onto, cfg, target, seams, acknowledged=False)
    assert "explicit decision" in not_accepted.message


def test_bare_metal_recovery_takes_the_installation_lock_not_the_library_one(cfg, target, seams):
    """Every gate KTD21 publishes sits on the disk that died. This is the substitute."""
    with _session_onto(cfg, target, seams) as open_session:
        assert open_session.lock == restore.recovery_lock_path()
        assert _lock_taken_in_another_process(restore.recovery_lock_path()) != 0

    entry = config.state_file(restore.RECOVERY_LOCK_KEY)
    assert entry.root is config.StateRoot.INSTALLATION
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED


# The hazards a green suite cannot see


def test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order(cfg, held, record):
    """A preview built by a second code path is a report about a different program."""
    _database(cfg).write_bytes(b"database, generation two")
    decided = restore.plan(cfg, record.session_id, held=held)
    rehearsed = restore.run(decided, cfg, held=held, dry_run=True)
    assert rehearsed.performed == decided.steps
    assert _database(cfg).read_bytes() == b"database, generation two"
    real = restore.run(decided, cfg, held=held)
    assert real.performed == rehearsed.performed
    assert _database(cfg).read_bytes() == _GENERATION_ONE


def test_a_rehearsal_never_clears_the_live_companion_files(cfg, held):
    """Clearing is itself destructive, so a preview that cleared would do the damage."""
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"companion, generation two")
    record, decided = _planned(cfg, held)
    restore.run(decided, cfg, held=held, dry_run=True)

    for companion in config.sidecar_paths("rekordbox_db", cfg):
        assert companion.read_bytes() == b"companion, generation two"


def test_a_restore_refuses_while_rekordbox_holds_the_database(cfg, held, monkeypatch, decided):
    monkeypatch.setattr(
        "cratekit.core.processes.running_process_names", lambda: ("rekordbox",)
    )
    cause = _refusal(restore.run, decided, cfg, held=held)
    assert cause.reason == "rekordbox-running"


@pytest.mark.parametrize(
    "document, why",
    [
        ("[]", "a top-level list"),
        ('"nothing"', "a scalar"),
        ('{"schema_version": 99, "markers": []}', "a version this build does not know"),
        ('{"schema_version": 1, "markers": null}', "a null marker list"),
        ('{"schema_version": 1, "markers": [{"kind": "effect"}]}', "a marker with no identity"),
        (
            '{"schema_version": 1, "markers": [{"kind": "invented", "identity": "x"}]}',
            "a kind this build does not know",
        ),
        ("not json at all", "bytes that are not JSON"),
    ],
)
def test_a_wrong_document_is_never_read_as_an_empty_one(cfg, document, why):
    """A malformed record refuses, or one more write deletes every prior marker (U11)."""
    path = reconcile.path_for(cfg)
    config.mkdir_private(path.parent)
    path.write_text(document)

    cause = _refusal(reconcile.outstanding, cfg)

    assert cause.reason == "restore-record-unusable", why


def _run_side_by_side(script: str, argument_lists) -> None:
    """One worker per argument list, all released at once by closing stdin, each to succeed."""
    environment = {**os.environ, "PYTHONPATH": str(SRC_ROOT)}
    preamble = (
        "import sys\n"
        "from cratekit.core import config, reconcile\n"
        "cfg = config.load()\n"
        "print('ready', flush=True)\n"
        "sys.stdin.read()\n"
    )
    running = [
        subprocess.Popen(
            [sys.executable, "-c", preamble + script, *arguments],
            env=environment,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for arguments in argument_lists
    ]
    for process in running:
        process.stdout.readline()
    for process in running:
        process.stdin.close()
    for process in running:
        with process:
            err = process.stderr.read()
        assert process.returncode == 0, err


def test_the_reconciliation_record_survives_eight_concurrent_writers(cfg):
    """The read-modify-write is locked, proven with real processes; unlocked lost most markers."""
    script = (
        "worker = sys.argv[1]\n"
        "for index in range(8):\n"
        "    reconcile.record_markers(\n"
        "        cfg,\n"
        "        reconcile.tree_markers([f'tree-{worker}-{index}'], session_id='s'),\n"
        "    )\n"
    )
    _run_side_by_side(script, [[str(worker)] for worker in range(8)])

    assert len(reconcile.records(cfg)) == 64


def test_a_disposition_is_not_lost_under_concurrency(cfg):
    """A dropped revocation leaves a marker standing forever, so nobody finds out."""
    recorded = reconcile.record_markers(
        cfg, reconcile.tree_markers([f"tree-{index}" for index in range(20)], session_id="s")
    )
    script = (
        "for marker_id in sys.argv[1:]:\n"
        "    reconcile.close_marker(\n"
        "        cfg, marker_id, disposition=reconcile.Disposition.ACCEPTED, actor='t'\n"
        "    )\n"
    )
    _run_side_by_side(
        script,
        [
            [entry.marker.marker_id for entry in recorded[:10]],
            [entry.marker.marker_id for entry in recorded[10:]],
        ],
    )

    assert reconcile.outstanding(cfg) == ()


def test_every_coupled_entry_declares_what_leaves_the_coupled_set(cfg):
    """P4: the literal is parsed, since a default makes "decided nothing" read as "nobody"."""
    # The module defining the inventory, wherever it lives (U299 moved it out of config.py).
    source = Path(inspect.getsourcefile(config.coupled_state_files)).read_text()
    tree = ast.parse(source)
    coupled = {entry.key for entry in config.coupled_state_files()}
    declared: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id in ("StateFile", "_library")):
            continue
        fields = {keyword.arg: keyword.value for keyword in node.keywords}
        key = fields.get("key") or (node.args[0] if node.args else None)
        if not isinstance(key, ast.Constant) or key.value not in coupled:
            continue
        assert "rollback_effects" in fields, f"{key.value!r} declares no rollback effects"
        declared.add(key.value)
    assert declared == coupled


def test_the_effect_set_a_restore_reconciles_is_the_set_the_inventory_declares(cfg):
    """Derived from the same predicate the replace side uses, so they cannot differ."""
    from_inventory = {
        (entry.key, effect)
        for entry, effect in config.out_of_band_effects()
    }
    assert from_inventory
    assert all(
        effect is not config.RollbackEffect.NONE for _key, effect in from_inventory
    )
    coupled = {entry.key for entry in config.coupled_state_files()}
    assert {key for key, _effect in from_inventory} <= coupled


def test_a_capture_whose_manifest_names_a_path_outside_the_set_is_refused(cfg, held):
    """Refusing beats restoring the subset this build happens to recognise."""
    record, captured = completed_session(cfg)
    manifest = json.loads((captured.root / snapshot.MANIFEST_NAME).read_text())
    manifest["sources"].append(
        {"source": str(cfg.library.root / "Music" / "somebody.flac"), "captured": None,
         "directory": False}
    )
    (captured.root / snapshot.MANIFEST_NAME).write_text(json.dumps(manifest))

    cause = _refusal(restore.plan, cfg, record.session_id, held=held)

    assert "not a path any restore may replace" in cause.message


def test_the_unconverged_decision_reads_the_captured_registry_not_a_date(cfg):
    """Date arithmetic is off by up to a day, so the captured registry is read."""
    source = _restore_sources()
    assert "read_path" in source
    assert "cutover_on" not in source


def test_a_held_session_used_after_its_block_is_refused(cfg, acked):
    """A ``Held`` outlives its block, so being inside it is asked at the call."""
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        record, _captured = completed_session(cfg)
        decided = restore.plan(cfg, record.session_id, held=open_session)
    assert not open_session.still_open
    cause = _refusal(restore.run, decided, cfg, held=open_session)
    assert "not held by this process" in cause.message
    assert _database(cfg).exists()


def test_a_restore_handed_an_ordinary_write_session_is_refused(cfg, held, record):
    pretending = dataclasses.replace(held, intent=session.Intent.WRITE)
    cause = _refusal(restore.plan, cfg, record.session_id, held=pretending)
    assert "declares itself a recovery" in cause.message


def test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded(cfg, held):
    """A preview that reported convergence because it wrote nothing would lie."""
    _one_effect_marker(cfg)
    record, decided = _planned(cfg, held)
    rehearsed = restore.run(decided, cfg, held=held, dry_run=True)

    assert rehearsed.outstanding
    assert not rehearsed.converged


def test_the_restore_module_names_no_verb(cfg):
    """D2. Every verb name that reaches a record arrives from the layer that owns one."""
    from cratekit.cli import registry

    source = _restore_sources()
    for name in registry.VERB_NAMES:
        assert f'"{name}"' not in source
    assert restore.CAPTURE_RESTORE_WORKFLOW not in registry.VERB_NAMES
    assert restore.BARE_METAL_WORKFLOW not in registry.VERB_NAMES


# The nine blocking defects two adversarial reviews found, each driven as reproduced.


def _foreign_volume(cfg) -> dict:
    """The library is present but its identity is foreign, which counts as gone."""
    return {
        "identity_provider": lambda _path: _ELSEWHERE,
        "mount_enumerator": lambda: (),
        "mount_probe": lambda _path: True,
    }


def test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused(
    cfg, replacement, record
):
    """A bare-metal ``Held`` never plans against the library the identity gate refused."""
    before = _tree_bytes(cfg.library.root)
    seams = _foreign_volume(cfg)
    library_seams = {
        key: value for key, value in seams.items() if key != "mount_probe"
    }
    ordinary = _refusal_entering(restore.recovery_session, cfg, **library_seams)
    assert ordinary.reason == "library-volume-mismatch"
    with _session_onto(cfg, replacement, seams) as bare_metal:
        assert bare_metal.issued_by is restore.Guard.BARE_METAL
        assert bare_metal.authorises == replacement
        assert not bare_metal.authorises_path(cfg.library.root)
        cause = _refusal(restore.plan, cfg, record.session_id, held=bare_metal)

    assert "no session is recorded" in cause.message
    assert str(replacement) in cause.message
    assert str(cfg.library.root) not in cause.message
    assert _tree_bytes(cfg.library.root) == before
    assert _database(cfg).read_bytes() == _GENERATION_ONE


# U95: every path comes from the directory the session authorises


def _tree_bytes(root) -> dict[str, bytes]:
    """Every file under ``root`` and its bytes, so "untouched" means the whole tree."""
    base = Path(root)
    return {
        str(path.relative_to(base)): path.read_bytes()
        for path in sorted(base.rglob("*"))
        if path.is_file()
    }


def _under(path, root) -> bool:
    where, base = Path(path).resolve(), Path(root).resolve()
    return where == base or base in where.parents


def _recovered_onto(cfg, replacement: Path) -> Path:
    """Stand in for the mirror pull: a copy whose records still name the configured root."""
    shutil.copytree(cfg.library.root, replacement)
    return replacement


def _bare_metal(cfg, replacement: Path):
    return _session_onto(cfg, replacement, _foreign_volume(cfg), replacing_existing=True)


def _rendered(decided, *, library, capture) -> list[tuple[str, str, str]]:
    """A plan with its temporary directories named rather than spelled."""

    def name(path):
        if path is None:
            return "-"
        for label, base in (("<capture>", capture), ("<library>", library)):
            if _under(path, base):
                relative = Path(path).resolve().relative_to(Path(base).resolve())
                return f"{label}/{relative}" if str(relative) != "." else label
        return f"<elsewhere>/{Path(path).name}"

    return [(str(step.act), name(step.target), name(step.source)) for step in decided.steps]


def test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target(cfg, tmp_path):
    """The capability R-8 item 3 asked for, end to end, against a recovered copy."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    _database(cfg).write_bytes(b"database, generation two")
    write_state(cfg, "label_watermarks", {"source": "after"})
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    # The configured root is stripped of state so no read can be answered by a twin.
    shutil.rmtree(config.library_state_dir(cfg))
    library_before = _tree_bytes(cfg.library.root)

    with _bare_metal(cfg, replacement) as bare_metal:
        decided = restore.plan(cfg, record.session_id, held=bare_metal)

        written = [step.target for step in decided.steps if step.target is not None]
        read = [step.source for step in decided.steps if step.source is not None]
        assert written and read
        for path in (*written, *read, decided.pre_restore_root, decided.capture_root):
            assert _under(path, replacement), path
            assert not _under(path, cfg.library.root), path

        outcome = restore.run(decided, cfg, held=bare_metal)

    assert outcome.performed == decided.steps
    assert restore.Act.REPLACE_TREE in {step.act for step in decided.steps}
    recovered_db = replacement / "db" / "master.db"
    assert recovered_db.read_bytes() == _GENERATION_ONE
    recovered_marks = replacement / config.state_path("label_watermarks", cfg).relative_to(
        cfg.library.root
    )
    assert json.loads(recovered_marks.read_bytes()) == {"source": "before"}
    assert _tree_bytes(cfg.library.root) == library_before


def _effects(decided) -> set:
    return {
        (marker.identity, marker.effect)
        for marker in decided.markers
        if marker.kind is reconcile.Kind.EFFECT
    }


def test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else(cfg, tmp_path):
    """Same steps, order, relative positions and decisions, and no invented effect."""
    write_state(cfg, "label_watermarks", {"source": "2026-07-01"})
    record, captured = completed_session(cfg)
    write_state(cfg, "tombstones", {"version": 1, "store": "tombstones", "decisions": []})
    replacement = _recovered_onto(cfg, tmp_path / "replacement")

    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as library_session:
        at_home = restore.plan(cfg, record.session_id, held=library_session)
    shutil.rmtree(config.library_state_dir(cfg))
    with _bare_metal(cfg, replacement) as bare_metal:
        moved = restore.plan(cfg, record.session_id, held=bare_metal)

    moved_capture = replacement / captured.root.relative_to(cfg.library.root)
    assert _rendered(moved, library=replacement, capture=moved_capture) == _rendered(
        at_home, library=cfg.library.root, capture=captured.root
    )
    assert _effects(at_home) == {("tombstones", config.RollbackEffect.TRASHED_FILE)}
    assert _effects(moved) == _effects(at_home)
    assert moved.unconverged == at_home.unconverged
    assert moved.discarded_sessions == at_home.discarded_sessions


def test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds(
    cfg, tmp_path
):
    """The refused library's capture is never read; the refusal names the replacement."""
    record, captured = completed_session(cfg)
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    moved_capture = replacement / captured.root.relative_to(cfg.library.root)
    shutil.rmtree(moved_capture)
    library_before = _tree_bytes(cfg.library.root)
    replacement_before = _tree_bytes(replacement)

    with _bare_metal(cfg, replacement) as bare_metal:
        refused = _refusal(restore.plan, cfg, record.session_id, held=bare_metal)

    assert not moved_capture.exists() and captured.root.is_dir()
    assert str(replacement) in refused.message
    assert str(cfg.library.root) not in refused.message
    assert _tree_bytes(cfg.library.root) == library_before
    assert _tree_bytes(replacement) == replacement_before


def test_u95_a_live_recovery_session_plan_is_unchanged_by_golden(cfg, held):
    """A golden from before U95 pins the library plan, and ``_rooted`` returns the same object."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, captured = completed_session(cfg)

    assert restore._rooted(cfg, held) is cfg
    manifest = snapshot.read_manifest(captured.root)
    root = Path(cfg.library.root)
    assert restore._rebased_capture(manifest, root, root) is manifest

    decided = restore.plan(cfg, record.session_id, held=held)

    assert _rendered(decided, library=cfg.library.root, capture=captured.root) == GOLDEN_PLAN
    assert _under(decided.pre_restore_root, cfg.library.root / "db" / restore.PRE_RESTORE_DIR)
    assert decided.capture_root == captured.root


GOLDEN_PLAN = [
    ("record-reconciliation", "-", "-"),
    ("clear-companion", "<library>/db/master.db-wal", "-"),
    ("clear-companion", "<library>/db/master.db-shm", "-"),
    ("replace-file", "<library>/db/master.db", "<capture>/master.db"),
    ("remove-absent", "<library>/db/masterPlaylists6.xml", "-"),
    ("replace-directory", "<library>/.cratekit/coupled", "<capture>/coupled"),
    ("release-restore-latch", "-", "-"),
]


def test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session(
    cfg, tmp_path, record
):
    """A plan is a value, and its targets were fixed when it was built."""
    _database(cfg).write_bytes(b"database, generation two")
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as library_session:
        for_the_library = restore.plan(cfg, record.session_id, held=library_session)
    library_before = _tree_bytes(cfg.library.root)
    replacement_before = _tree_bytes(replacement)
    with _bare_metal(cfg, replacement) as bare_metal:
        for dry_run in (True, False):
            cause = _refusal(
                restore.run, for_the_library, cfg, held=bare_metal, dry_run=dry_run
            )
            assert "authorises" in cause.message
            assert cause.detail["authorises"] == str(replacement)
            assert _under(cause.detail["writing"], cfg.library.root)

    assert _tree_bytes(cfg.library.root) == library_before
    assert _tree_bytes(replacement) == replacement_before


def test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session(cfg, tmp_path, record):
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    with _bare_metal(cfg, replacement) as bare_metal:
        for_the_target = restore.plan(cfg, record.session_id, held=bare_metal)
    replacement_before = _tree_bytes(replacement)
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as library_session:
        # Compared inside the block, since the session writes its own record.
        inside = _tree_bytes(cfg.library.root)
        cause = _refusal(restore.run, for_the_target, cfg, held=library_session)
        assert _tree_bytes(cfg.library.root) == inside

    assert "authorises" in cause.message
    assert cause.detail["authorises"] == str(cfg.library.root)
    assert _under(cause.detail["writing"], replacement)
    assert _tree_bytes(replacement) == replacement_before


def test_u95_a_library_session_still_refuses_a_configuration_for_another_library(
    cfg, held, tmp_path, record
):
    """Re-rooting is the bare-metal guard's alone; a library session refuses another library."""
    other = tmp_path / "another-library"
    (other / "db").mkdir(parents=True)
    elsewhere = dataclasses.replace(
        cfg,
        library=dataclasses.replace(
            cfg.library, root=other, db_path=other / "db" / "master.db"
        ),
    )
    cause = _refusal(restore.plan, elsewhere, record.session_id, held=held)
    assert "authorises" in cause.message
    assert cause.detail["writing"] == str(other)
    assert cause.detail["authorises"] == str(cfg.library.root)


def test_u95_a_database_outside_the_library_refuses_a_bare_metal_plan_by_name(
    cfg, tmp_path
):
    """A database outside the root has no position on the target, so the plan refuses by name."""
    outside = tmp_path / "home" / "rekordbox" / "master.db"
    outside.parent.mkdir(parents=True)
    outside.write_bytes(b"a database outside the library")
    apart = dataclasses.replace(
        cfg, library=dataclasses.replace(cfg.library, db_path=outside)
    )
    record, _captured = completed_session(apart)
    replacement = _recovered_onto(apart, tmp_path / "replacement")
    replacement_before = _tree_bytes(replacement)

    with _bare_metal(apart, replacement) as bare_metal:
        refused = _refusal(restore.plan, apart, "no-such-session", held=bare_metal)
        refused_run = _refusal(restore.plan, apart, record.session_id, held=bare_metal)

    for cause in (refused, refused_run):
        assert cause.reason == "recovery-target-refused"
        assert cause.detail["database"] == str(outside)
        assert cause.remediation.steps
    assert outside.read_bytes() == b"a database outside the library"
    assert _tree_bytes(replacement) == replacement_before


def test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too(
    cfg, held, tmp_path, record
):
    """Staging is no step target, so it is authorised separately, in both modes."""
    database = _database(cfg)
    log = database.with_name(database.name + "-wal")
    log.write_bytes(b"transactions no capture holds")
    decided = restore.plan(cfg, record.session_id, held=held)
    stray = tmp_path / "not-the-library" / "staged"
    aimed_away = dataclasses.replace(decided, pre_restore_root=stray)
    for dry_run in (True, False):
        refused = _refusal(restore.run, aimed_away, cfg, held=held, dry_run=dry_run)
        assert refused.detail["writing"] == str(stray)

    assert log.read_bytes() == b"transactions no capture holds"
    assert not stray.exists()


@pytest.mark.parametrize(
    "aimed_at",
    [
        lambda cfg, decided: Path(cfg.library.root),
        lambda cfg, decided: Path(cfg.library.root) / "Music",
        lambda cfg, decided: decided.pre_restore_root.parent,
    ],
    ids=["the-library-root", "a-directory-in-the-library", "the-staging-store-itself"],
)
def test_u95_staging_inside_the_library_but_not_under_its_store_is_refused(
    cfg, held, tmp_path, aimed_at
):
    """The closing step prunes staging's parent, which for the root would delete its siblings."""
    bystander = Path(cfg.library.root).parent / "a-neighbouring-volume"
    bystander.mkdir()
    (bystander / "keep.txt").write_bytes(b"not this restore's to touch")
    record, decided = _planned(cfg, held)
    tampered = dataclasses.replace(decided, pre_restore_root=aimed_at(cfg, decided))
    before = _tree_bytes(cfg.library.root)

    for dry_run in (True, False):
        refused = _refusal(restore.run, tampered, cfg, held=held, dry_run=dry_run)
        assert "stages live companion files" in refused.message

    assert (bystander / "keep.txt").read_bytes() == b"not this restore's to touch"
    assert _tree_bytes(cfg.library.root) == before


def test_u95_plan_checks_its_own_answer_rather_than_trusting_the_derivation(
    cfg, held, tmp_path, monkeypatch, record
):
    """The plan side guard, tripped through the staging seam; a preview refuses too."""
    stray = tmp_path / "not-the-library" / "staged" / "attempt"
    monkeypatch.setattr(restore, "_pre_restore_root", lambda _cfg, now=None: stray)
    refused = _refusal(restore.plan, cfg, record.session_id, held=held)
    assert refused.detail["writing"] == str(stray)
    assert not stray.exists()


def test_u95_a_step_aimed_at_the_authorised_directory_itself_is_refused(cfg, held):
    """The authorised root itself is no restore target, or it would stage above it."""
    record, captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    rogue = restore.Step(
        act=restore.Act.REPLACE_TREE,
        target=Path(cfg.library.root),
        source=captured.root,
        detail="replace the whole library with a capture directory",
    )
    tampered = dataclasses.replace(decided, steps=(*decided.steps, rogue))
    before = _tree_bytes(cfg.library.root)

    for dry_run in (True, False):
        refused = _refusal(restore.run, tampered, cfg, held=held, dry_run=dry_run)
        assert "not a path any restore" in refused.message

    assert _tree_bytes(cfg.library.root) == before


def test_u95_a_recorded_path_is_moved_by_the_rule_config_uses_and_only_once(tmp_path):
    """Re-basing answers "where under the library was this", and only that."""
    mounts = tmp_path / "mounts"
    old, new = mounts / "lib", mounts / "new"

    assert restore._rebased(old, old, new) == new
    assert restore._rebased(old / "db" / "master.db", old, new) == new / "db" / "master.db"
    # under neither root: left where it says it is
    stranger = tmp_path / "home" / "master.db"
    assert restore._rebased(stranger, old, new) == stranger
    # a sibling whose NAME starts the same way is not inside
    sibling = mounts / "library2" / "x"
    assert restore._rebased(sibling, old, new) == sibling
    # spelled with dots: config calls these inside and outside, so this does too
    dotted_in = f"{mounts}/a/../lib/db/m.db"
    assert restore._rebased(dotted_in, old, new) == new / "db" / "m.db"
    dotted_out = Path(f"{old}/db/../../other/m.db")
    assert restore._rebased(dotted_out, old, new) == dotted_out
    assert restore._rebased(old / "x", Path(f"{mounts}/a/../lib"), new) == new / "x"
    # equal roots: every library session
    assert restore._rebased(old / "x", old, old) == old / "x"

    # Idempotent when the target is mounted inside the configured root.
    inside = old / "new"
    once = restore._rebased(old / ".cratekit" / "history" / "x", old, inside)
    assert once == inside / ".cratekit" / "history" / "x"
    assert restore._rebased(once, old, inside) == once


def test_u95_a_bare_metal_session_roots_the_configuration_at_its_target(cfg, replacement):
    with _bare_metal(cfg, replacement) as bare_metal:
        rooted = restore._rooted(cfg, bare_metal)

    assert rooted.library.root == replacement
    assert rooted.library.db_path == replacement / "db" / "master.db"
    assert rooted.library.volume_id == cfg.library.volume_id
    assert rooted is not cfg and cfg.library.root != replacement


def test_blocking_1_a_held_naming_an_unrelated_lock_this_process_holds_is_refused(
    cfg, tmp_path, record
):
    """ACCEPTED 3: the token, not lock membership, proves a live guard issued it."""
    unrelated = tmp_path / "something-else.lock"
    with session.session_lock(path=unrelated) as lock:
        forged = restore.Held(
            workflow=restore.CAPTURE_RESTORE_WORKFLOW,
            lock=lock,
            intent=session.Intent.RECOVERY,
            issued_by=restore.Guard.LIBRARY_SESSION,
            authorises=Path(cfg.library.root),
        )
        assert str(lock.absolute()) in session._HELD
        assert not forged.still_open
        cause = _refusal(restore.plan, cfg, record.session_id, held=forged)

    assert "not held by this process" in cause.message


def test_blocking_1_a_token_is_withdrawn_when_its_guard_returns(cfg, acked):
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        assert open_session.token is not None
        assert id(open_session.token) in restore._ISSUED
    assert id(open_session.token) not in restore._ISSUED


def _wal_path(cfg) -> Path:
    """The live write-ahead log, resolved through the inventory rather than spelled."""
    database = _database(cfg)
    companions = config.sidecar_paths("rekordbox_db", cfg)
    return next(path for path in companions if path.name.startswith(database.name))


def test_blocking_2_a_capture_whose_database_is_gone_refuses_before_the_log_is_touched(
    cfg, held
):
    """Refused at plan, since the live log holds transactions no capture has."""
    record, captured = completed_session(cfg)
    _database(cfg).write_bytes(b"database, generation two")
    log = _live_log(cfg, b"committed transactions the main file does not hold")
    captured.database.unlink()
    cause = _refusal(restore.plan, cfg, record.session_id, held=held)
    assert cause.reason == "snapshot-integrity-failed"
    assert "no longer on disk" in cause.message
    assert log.read_bytes() == b"committed transactions the main file does not hold"


def test_blocking_2_the_live_log_is_moved_aside_rather_than_deleted(cfg, held, record):
    """Even on success the log is staged, since its bytes postdate every capture."""
    log = _live_log(cfg, b"committed transactions the main file does not hold")
    decided, _outcome = _restored(cfg, record, held)
    assert not log.exists(), "the engine must not find a log beside a replaced database"
    kept = decided.pre_restore_root / log.name
    assert kept.read_bytes() == b"committed transactions the main file does not hold"


def test_blocking_2_a_failure_mid_restore_is_a_structured_refusal(cfg, held, monkeypatch, decided):
    """A raw OSError carries no reason, remedy or exit code, and failure is when people restore."""
    def _explode(_source, _target):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(restore, "_replace_file", _explode)
    cause = _refusal(restore.run, decided, cfg, held=held)
    assert cause.reason == "restore-step-failed"
    assert cause.code is ExitCode.PRECONDITION
    assert cause.remediation.steps
    # The latch written first is still standing.
    standing = [r.marker.marker_id for r in reconcile.outstanding(cfg)]
    assert decided.latch.marker_id in standing


def test_blocking_2_a_restore_checks_the_library_volume_has_room_for_the_copy(cfg, held, decided):
    """One call site, inside ``capture``, so a restore checked nothing at all."""
    calls: list[tuple[int, str]] = []
    original = snapshot.assert_room_for

    def _watch(needed, destination, **kwargs):
        calls.append((needed, str(destination)))
        return original(needed, destination, **kwargs)

    snapshot.assert_room_for = _watch
    try:
        restore.run(decided, cfg, held=held, dry_run=True)
    finally:
        snapshot.assert_room_for = original

    assert calls, "the restore never asked whether the library volume has room"
    assert calls[0][0] > 0


def test_blocking_4_two_restores_producing_the_same_triple_are_two_markers(cfg):
    """Scenario A: or the second restore's discarded audio is owned by nobody."""
    first = reconcile.Marker(
        kind=reconcile.Kind.EFFECT,
        identity="label_watermarks",
        effect=config.RollbackEffect.DOWNLOADED_FILE,
        session_id="run-1",
        capture_stamp="capture-1",
    )
    reconcile.record_markers(cfg, [first])
    reconcile.close_marker(
        cfg, first.marker_id, disposition=reconcile.Disposition.ACCEPTED, actor="phillip"
    )
    assert reconcile.converged(cfg)

    second = reconcile.Marker(
        kind=reconcile.Kind.EFFECT,
        identity="label_watermarks",
        effect=config.RollbackEffect.DOWNLOADED_FILE,
        session_id="run-2",
        capture_stamp="capture-2",
    )
    reconcile.record_markers(cfg, [second])

    assert first.marker_id != second.marker_id
    assert [r.marker.marker_id for r in reconcile.outstanding(cfg)] == [second.marker_id]
    assert not reconcile.converged(cfg)


def test_blocking_4_a_rebuilt_tree_does_not_pay_for_every_later_restore(cfg):
    """Scenario B: one rebuild does not close the tree against later restores."""
    first = reconcile.tree_markers(["routing"], session_id="run-1", capture_stamp="c-1")
    recorded = reconcile.record_markers(cfg, first)
    reconcile.close_marker(
        cfg,
        recorded[0].marker.marker_id,
        disposition=reconcile.Disposition.REPAIRED,
        actor="phillip",
    )
    assert reconcile.unconverged_trees(cfg) == ()

    second = reconcile.tree_markers(["routing"], session_id="run-2", capture_stamp="c-2")
    reconcile.record_markers(cfg, second)

    assert reconcile.unconverged_trees(cfg) == ("routing",)


def test_blocking_4_recording_one_restore_twice_is_still_idempotent(cfg):
    """Recording the same restore twice stays idempotent."""
    markers = reconcile.tree_markers(["routing"], session_id="run-1", capture_stamp="c")
    reconcile.record_markers(cfg, markers)
    recorded = reconcile.record_markers(cfg, markers)

    assert len(recorded) == 1


def test_blocking_5_an_interrupted_restore_in_a_none_effect_window_latches(
    cfg, held, acked, decided
):
    """A restore with no effect markers still latches before replacing."""
    assert decided.markers == (), "this fixture must have no effect markers at all"
    assert decided.steps[0].act is restore.Act.RECORD
    assert decided.steps[-1].act is restore.Act.RELEASE

    # Everything but the last step, which is the interruption.
    for step in decided.steps[:-1]:
        restore._perform(step, decided, cfg)

    cause = _sweep_refusal(cfg)
    assert cause.reason == "restore-reconciliation-outstanding"
    assert "never seen to finish" in cause.message


def test_blocking_5_a_restore_that_completes_retracts_its_own_latch(cfg, acked, record):
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        decided = restore.plan(cfg, record.session_id, held=open_session)
        outcome = restore.run(decided, cfg, held=open_session)

    assert outcome.outstanding == ()
    assert outcome.converged
    # Asked outside the recovery session, since the library lock does not nest.
    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"


def test_blocking_5_a_rehearsal_does_not_latch_anything(cfg, held, decided):
    """A rehearsal performs nothing at all, including the latch."""
    restore.run(decided, cfg, held=held, dry_run=True)
    assert reconcile.records(cfg) == ()


def test_blocking_6_a_second_attempt_never_deletes_the_only_surviving_copy(
    cfg, tmp_path
):
    """After a crash between renames ``coupled.replaced`` is the only copy; never delete it."""
    target = tmp_path / "coupled"
    previous = tmp_path / "coupled.replaced"
    previous.mkdir()
    (previous / "watermarks.json").write_bytes(b"the only copy of the live state")
    assert not target.exists()

    source = tmp_path / "capture" / "coupled"
    (source / "unreadable").mkdir(parents=True)
    (source / "unreadable" / "item.json").write_bytes(b"{}")
    (source / "unreadable").chmod(0o000)
    try:
        with pytest.raises(OSError):
            restore._replace_directory(source, target)
    finally:
        (source / "unreadable").chmod(0o755)

    assert (target / "watermarks.json").read_bytes() == (
        b"the only copy of the live state"
    ), "the only surviving copy of the pre-restore state was destroyed"
    assert not (tmp_path / "coupled.restoring").exists()


def test_blocking_6_the_single_failure_shape_is_unchanged(cfg, tmp_path):
    """The shape that was already right, kept: the old directory is findable."""
    target = tmp_path / "coupled"
    target.mkdir()
    (target / "live.json").write_bytes(b"live")
    source = tmp_path / "capture" / "coupled"
    source.mkdir(parents=True)
    (source / "captured.json").write_bytes(b"captured")

    restore._replace_directory(source, target)

    assert (target / "captured.json").read_bytes() == b"captured"
    assert not (tmp_path / "coupled.replaced").exists()
    assert not (tmp_path / "coupled.restoring").exists()


def test_the_rehearsal_refuses_a_replacement_whose_source_is_gone(cfg, held):
    """A rehearsal checks each step's preconditions, so a missing source refuses."""
    record, captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "x"})
    decided = restore.plan(cfg, record.session_id, held=held)

    replacement = next(
        step for step in decided.steps if step.act is restore.Act.REPLACE
    )
    replacement.source.unlink()

    cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)

    assert cause.reason == "snapshot-integrity-failed"
    assert str(captured.root) in str(cause.detail)


def test_the_rehearsal_refuses_a_target_directory_nobody_can_write_to(cfg, held, decided):
    """The other case the empty rehearsal reported clean."""
    database_dir = _database(cfg).parent
    database_dir.chmod(0o500)
    try:
        cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    finally:
        database_dir.chmod(0o700)

    assert cause.reason == "restore-step-failed"
    assert "not writable" in cause.message


def test_a_plan_built_before_a_later_commit_is_refused_at_run(cfg, held):
    """ACCEPTED 5: ``run`` revalidates, since a plan is a value and the log is not."""
    record, _captured = completed_session(cfg, started="2026-08-01T00:00:00+00:00")
    decided = restore.plan(cfg, record.session_id, held=held)

    completed_session(cfg, started="2026-08-03T00:00:00+00:00", stamp="later-capture")

    cause = _refusal(restore.run, decided, cfg, held=held)

    assert cause.reason == "restore-discards-committed-work"
    assert _database(cfg).exists()


def test_a_reconciliation_store_on_an_unmounted_volume_is_not_an_empty_one(cfg):
    """A missing store path refuses rather than reading as empty, in all readers."""
    stranded = session.open_session(cfg, workflow="library-sweep")
    shutil.rmtree(cfg.library.root)

    for reader in (reconcile.records, reconcile.outstanding, reconcile.converged):
        cause = _refusal(reader, cfg)
        assert cause.reason == "restore-record-unusable"

    _refusal(session.close_session, stranded, cfg)


def test_a_same_length_edit_inside_a_coupled_directory_still_marks(cfg, held):
    """The digest reads content, not length."""
    outcomes = config.state_path("label_outcomes", cfg)
    outcomes.mkdir(parents=True, exist_ok=True)
    (outcomes / "label-a.json").write_bytes(b'{"taken": "aaaa"}')
    record, _captured = completed_session(cfg)
    (outcomes / "label-a.json").write_bytes(b'{"taken": "bbbb"}')

    decided = restore.plan(cfg, record.session_id, held=held)

    assert "label_outcomes" in [marker.identity for marker in decided.markers]


def test_pruning_with_no_session_named_asks_the_log_instead_of_skipping(cfg):
    """``owning=None`` asks the log rather than checking nothing."""
    session.open_session(cfg, workflow="library-sweep")

    cause = _refusal(restore.prune, cfg)

    assert "not reached a terminal state" in cause.message


def test_the_tree_shortness_handoff_calls_the_module_that_owns_the_gate(
    cfg, held, monkeypatch
):
    """BLOCKING 8: handed once to its owner, patched for real so signature drift fails (R-21)."""
    calls: list[tuple] = []

    def _mark(configuration, tree_ids, *, reason, now=None):
        calls.append((configuration, tuple(tree_ids), reason))

    monkeypatch.setattr(convergence, "mark_unconverged", _mark)
    record, _captured = completed_session(cfg)
    _cut_over(cfg)
    _restored(cfg, record, held)

    # A literal, since a value read off the constant passes at any value.
    assert calls == [(cfg, ("routing",), "restore-predates-cutover")]
    assert restore.PRE_CUTOVER_RESTORE == "restore-predates-cutover"
    assert reconcile.unconverged_trees(cfg) == (), "the fact was recorded twice"


def test_the_tree_mark_happens_after_the_coupled_state_is_replaced(cfg, held, record):
    """The shortness record is coupled, so marking before the replace is overwritten."""
    _cut_over(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    acts = [step.act for step in decided.steps]
    assert acts.index(restore.Act.MARK_TREES) > acts.index(restore.Act.REPLACE)
    assert acts.index(restore.Act.MARK_TREES) < acts.index(restore.Act.RELEASE)


# The register entry this unit owns, and the obligation U36's landing left without one.


def test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build():
    """The call-time fallback must go once both modules share a build (R-21 item 3)."""
    import importlib.util  # noqa: PLC0415

    # With its parts, since U300 moved ``_hand_tree_shortness_over`` to ``restore_perform``.
    source = _restore_sources()
    try:
        landed = importlib.util.find_spec("cratekit.core.convergence") is not None
    except ModuleNotFoundError:
        landed = False

    if not landed:
        # The fallback is correct here, and it must latch, not merely record.
        assert "_convergence_module" in source, (
            "the call-time resolution is gone while core.convergence is still "
            "absent, so this build's restore imports a module that is not here"
        )
        assert reconcile.Kind.UNCONVERGED_TREE in reconcile.LATCHING_KINDS
        return

    assert "_convergence_module" not in source, (
        "core.convergence is in this build, so the handoff is an ordinary import: "
        "delete _convergence_module, delete the fallback branch in "
        "_hand_tree_shortness_over, and import the module at the top of restore.py"
    )
    assert "Kind.UNCONVERGED_TREE" not in source, (
        "core.convergence owns tree shortness in this build, so restore.py must "
        "not still filter a kind it can no longer record"
    )


def test_the_restore_verbs_hold_one_session_across_both_halves():
    """The verbs pass the open guard as ``gates``, or a commit fits between plan and run."""
    import cratekit.session.restore_cli as restore_cli  # noqa: PLC0415

    source = Path(restore_cli.__file__).read_text()
    assert "recovery_session" in source, "the verbs do not enter the one spanning session"
    assert re.search(r"gates\s*=\s*\w+\.guard", source), "the open guard is not handed on"
    assert "assert_gates" not in source, "the verb enters the gates itself, a second lock"


# Fix round 2: what the first round's fixes broke, each driven as the verifier reproduced it.


def test_round2_a_completed_restore_discharges_an_earlier_interrupted_one(cfg, acked):
    """A completed restore discharges an earlier interrupted one's latch."""
    first, _capture_one = completed_session(cfg, stamp="capture-one")
    second, _capture_two = completed_session(
        cfg, started="2026-08-03T00:00:00+00:00", stamp="capture-two"
    )
    with restore.recovery_session(cfg, **gate_seams(cfg)) as one:
        interrupted = restore.plan(cfg, first.session_id, held=one)
        restore._perform(interrupted.steps[0], interrupted, cfg)
    assert len(reconcile.outstanding(cfg)) == 1
    with restore.recovery_session(cfg, **gate_seams(cfg)) as two:
        decided = restore.plan(
            cfg, second.session_id, held=two, discarding=(first.session_id,)
        )
        outcome = restore.run(decided, cfg, held=two)

    assert outcome.outstanding == ()
    assert outcome.converged
    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"


def test_round2_repeating_a_failing_restore_does_not_accumulate_latches(cfg, acked, record):
    """Repeated attempts are one restore, keyed on the capture, so one latch row."""
    for _attempt in range(3):
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            decided = restore.plan(cfg, record.session_id, held=open_session)
            restore._perform(decided.steps[0], decided, cfg)

    open_records = reconcile.outstanding(cfg)
    assert len(open_records) == 1, [r.marker.marker_id for r in open_records]
    assert open_records[0].marker.identity == _captured_stamp(cfg, record)


def _captured_stamp(cfg, record) -> str:
    return snapshot.read_manifest(restore.capture_root_of(record.snapshot_path)).stamp


def test_round2_three_attempts_stage_their_logs_side_by_side(cfg, acked, record):
    """The latch collapses across attempts but staged logs must not overwrite."""
    roots = set()
    for attempt in range(3):
        _live_log(cfg, f"attempt {attempt}".encode())
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            decided = restore.plan(cfg, record.session_id, held=open_session)
            restore._perform(decided.steps[0], decided, cfg)
            for step in decided.steps:
                if step.act is restore.Act.CLEAR:
                    restore._perform(step, decided, cfg)
            roots.add(decided.pre_restore_root)

    assert len(roots) == 3
    kept = sorted(
        path.read_bytes()
        for root in roots
        for path in root.iterdir()
        if path.name.endswith("wal")
    )
    assert kept == [b"attempt 0", b"attempt 1", b"attempt 2"]


def test_round2_a_restore_that_fits_is_not_refused(cfg, held):
    """P7: a restore the volume can hold is not refused by summing every source."""
    _build_capacity_shape(cfg, **_CAPACITY_SHAPE)
    record, decided = _planned(cfg, held)
    estimate = restore.space_peak_bytes(decided)
    summed = sum(snapshot.incoming_bytes(entry.source) for entry in _captured_entries(decided))

    assert estimate < summed, "the estimate is no better than summing everything"
    outcome = restore.run(decided, cfg, held=held)
    assert outcome.converged


#: The database heavy shape the capacity rule was measured against, at a sixteenth of the
#: original, where every ratio compared reads the same since a document takes a whole block.
_CAPACITY_SHAPE = {"database": 512, "wal": 256, "items": 125}


def _build_capacity_shape(cfg, *, database: int, wal: int, items: int) -> None:
    """One of the shapes the capacity rule was measured against. Sizes in KiB."""
    _database(cfg).write_bytes(b"d" * (database * 1024))
    _wal_path(cfg).write_bytes(b"w" * (wal * 1024))
    queue = config.state_path("review_queue", cfg)
    queue.mkdir(parents=True, exist_ok=True)
    for index in range(items):
        (queue / f"item-{index:05d}.json").write_bytes(b"x" * 120)


def _allocated_tree(root: Path) -> int:
    """Blocks occupied under ``root``, the way a filesystem counts them."""
    return sum(stat.st_blocks * 512 for _path, stat in _file_stats(root))


class _PeakSampler:
    """Samples occupied blocks around every byte-moving primitive, where copies overlap."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.baseline = _allocated_tree(root)
        self.peak = 0

    def sample(self) -> None:
        self.peak = max(self.peak, _allocated_tree(self.root) - self.baseline)

    def install(self, monkeypatch) -> None:
        import shutil as real_shutil  # noqa: PLC0415

        sampler = self

        class _Shim:
            def __init__(self, wrapped, names):
                self._wrapped = wrapped
                for name in names:
                    setattr(self, name, self._wrap(getattr(wrapped, name)))

            def _wrap(self, call):
                def sampled(*args, **kwargs):
                    sampler.sample()
                    result = call(*args, **kwargs)
                    sampler.sample()
                    return result

                return sampled

            def __getattr__(self, name):
                return getattr(self._wrapped, name)

        monkeypatch.setattr(
            restore, "shutil", _Shim(real_shutil, ("copyfile", "copytree", "rmtree"))
        )
        monkeypatch.setattr(restore, "os", _Shim(os, ("replace",)))


@pytest.mark.parametrize(
    "shape, wipe_live",
    [
        (_CAPACITY_SHAPE, False),
        (_CAPACITY_SHAPE, True),
        ({"database": 64, "wal": 512, "items": 125}, False),
    ],
)
def test_round3_the_capacity_estimate_is_above_the_measured_peak(
    cfg, held, monkeypatch, shape, wipe_live
):
    """BLOCKING 1: the estimate bounds the measured peak, measured rather than restated."""
    _build_capacity_shape(cfg, **shape)
    record, _captured = completed_session(cfg)
    if wipe_live:
        shutil.rmtree(config.library_coupled_dir(cfg), ignore_errors=True)
        _database(cfg).unlink()

    decided = restore.plan(cfg, record.session_id, held=held)
    estimate = restore.space_peak_bytes(decided)

    sampler = _PeakSampler(Path(cfg.library.root))
    sampler.install(monkeypatch)
    restore.run(decided, cfg, held=held)

    assert estimate >= sampler.peak, f"the estimate {estimate} is BELOW {sampler.peak}"


def test_round3_a_volume_between_the_two_rules_is_refused(cfg, held, monkeypatch):
    """Free space between one step's worth and the real peak is refused."""
    _build_capacity_shape(cfg, **_CAPACITY_SHAPE)
    record, decided = _planned(cfg, held)

    largest_single = max(
        snapshot.incoming_bytes(step.source)
        for step in decided.steps
        if step.act in (restore.Act.REPLACE, restore.Act.REPLACE_TREE)
    )
    estimate = restore.space_peak_bytes(decided)
    assert estimate > largest_single, "the estimate is still one step's worth"

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: int(largest_single * 1.2))
    cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)

    assert cause.reason == "snapshot-store-full"
    assert _database(cfg).read_bytes()[:1] == b"d"


def test_round3_a_staged_log_is_counted_as_permanent_growth(cfg, held):
    """A CLEAR is a rename, so the restored companion's size is never given back."""
    _build_capacity_shape(cfg, database=1024, wal=8192, items=10)
    record, decided = _planned(cfg, held)

    staged = {step.target for step in decided.steps if step.act is restore.Act.CLEAR}
    companions = sum(
        snapshot.incoming_bytes(step.source)
        for step in decided.steps
        if step.act is restore.Act.REPLACE and step.target in staged
    )
    assert companions > 0, "this fixture writes no companion back"
    assert restore.space_peak_bytes(decided) >= companions


def test_round2_the_restore_capacity_refusal_names_the_library_volume(
    cfg, held, monkeypatch, decided
):
    """The capacity refusal names the library volume, not the capture store."""
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 1)
    cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    assert cause.reason == "snapshot-store-full"
    assert "LIBRARY volume" in " ".join(cause.remediation.steps)


def test_round2_a_pre_cutover_restore_is_gated_rather_than_merely_recorded(
    cfg, held, acked, record
):
    """A pre-cutover restore is gated, not merely recorded in a store nothing reads."""
    _cut_over(cfg)
    _restored(cfg, record, held)
    assert reconcile.Kind.UNCONVERGED_TREE in reconcile.LATCHING_KINDS, (
        "the tree kind must stay in the latching set: the unit that ships the "
        "rebuild DERIVES its own exemption from this set by subtracting that one "
        "member by name, so removing it here silently widens what that unit holds"
    )
    assert _tree_is_recorded_short(cfg, "routing")
    _assert_the_next_write_is_refused_over(cfg, "routing")


def test_round2_a_successful_restore_over_an_unremovable_old_copy_still_succeeds(cfg, held, acked):
    """An unremovable old copy must not fail a landed restore or leave the latch permanent."""
    queue = config.state_path("review_queue", cfg)
    (queue / "locked").mkdir(parents=True, exist_ok=True)
    (queue / "locked" / "item.json").write_bytes(b"{}")
    record, _captured = completed_session(cfg)
    (queue / "locked").chmod(0o500)
    try:
        decided = restore.plan(cfg, record.session_id, held=held)
        outcome = restore.run(decided, cfg, held=held)
    finally:
        for leftover in queue.parent.glob("*.replaced/**/locked"):
            leftover.chmod(0o700)
        if (queue / "locked").exists():
            (queue / "locked").chmod(0o700)

    assert outcome.converged, "a restore that landed correctly reported failure"
    assert (queue / "locked" / "item.json").read_bytes() == b"{}"
    assert reconcile.outstanding(cfg) == ()


def test_round2_a_directory_replacement_checks_its_parent_not_itself(cfg, held, decided):
    """``_replace_directory`` writes in the target's parent, so the parent is probed."""
    coupled_parent = config.library_coupled_dir(cfg).parent
    coupled_parent.chmod(0o500)
    try:
        cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    finally:
        coupled_parent.chmod(0o700)

    assert cause.reason == "restore-step-failed"
    assert str(coupled_parent) in cause.message


def test_round2_a_held_rebuilt_around_a_live_token_is_refused(cfg, replacement, record):
    """RESIDUAL 6: a ``Held`` rebuilt around a live token is refused."""
    seams = _foreign_volume(cfg)
    with _session_onto(cfg, replacement, seams) as bare_metal:
        laundered = restore.Held(
            workflow=restore.CAPTURE_RESTORE_WORKFLOW,
            lock=bare_metal.lock,
            intent=session.Intent.RECOVERY,
            issued_by=restore.Guard.LIBRARY_SESSION,
            authorises=Path(cfg.library.root),
            token=bare_metal.token,
        )
        assert not laundered.still_open
        cause = _refusal(restore.plan, cfg, record.session_id, held=laundered)

    assert "not held by this process" in cause.message
    assert _database(cfg).read_bytes() == _GENERATION_ONE


def test_round2_a_close_against_a_husk_is_refused_by_the_volume_gate(cfg):
    """FIX 4: a close over an unmounted husk is refused at the gate, which knows the identity."""
    reconcile.record_markers(cfg, [reconcile.in_flight_marker(capture_stamp="c-1")])
    stranded = session.open_session(cfg, workflow="library-sweep")
    assert not reconcile.converged(cfg)

    root = Path(cfg.library.root)
    for child in root.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    assert root.is_dir(), "the fixture is not the shape this test is about"

    # A stale stub reports the identity of whatever disk now holds the mount point.
    cause = _refusal(
        session.close_session,
        stranded,
        cfg,
        identity_provider=lambda _path: _ELSEWHERE,
        mount_enumerator=lambda: (),
    )

    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE

    # Abandoning stays allowed, or a run could be neither finished nor given up.
    ended = session.close_session(stranded, cfg, state=session.SessionState.ABANDONED)
    assert ended.state is session.SessionState.ABANDONED


def test_round2_the_readers_still_answer_identically_on_a_gone_library(cfg):
    """The reader half that IS decidable: a root that is not there at all."""
    reconcile.record_markers(cfg, [reconcile.in_flight_marker(capture_stamp="c-1")])
    shutil.rmtree(cfg.library.root)

    for reader in (reconcile.records, reconcile.outstanding, reconcile.converged):
        cause = _refusal(reader, cfg)
        assert cause.reason == "restore-record-unusable"


def test_round2_a_write_against_a_husk_does_not_rebuild_the_state_tree(cfg):
    """The other half of FIX 4: recording recreated the tree on the internal disk."""
    root = Path(cfg.library.root)
    for child in root.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()

    cause = _refusal(
        reconcile.record_markers, cfg, [reconcile.in_flight_marker(capture_stamp="c")]
    )

    assert cause.reason == "restore-record-unusable"
    assert not config.library_state_dir(cfg).exists()


def test_round2_a_library_with_a_database_and_no_state_yet_is_not_refused(cfg):
    """P7: a library with no state yet is a fresh install, not a husk."""
    shutil.rmtree(config.library_state_dir(cfg), ignore_errors=True)
    assert Path(cfg.library.db_path).exists()

    assert reconcile.records(cfg) == ()
    assert reconcile.converged(cfg)


def test_round2_the_real_mount_probe_is_armed_by_default(cfg, tmp_path, seams):
    """NOTE 8: supplying no ``mount_probe`` leaves the real probe armed."""
    del seams["mount_probe"]
    sibling = tmp_path / "library 1"
    sibling.mkdir()
    cause = _refusal_entering(_session_onto, cfg, sibling, seams)
    assert "unmounted volume leaves behind" in cause.message


def _replacing_the_coupled_tree(cfg, held):
    """A plan that replaces the coupled directory, and that directory."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    _record, decided = _planned(cfg, held)
    coupled = config.library_coupled_dir(cfg)
    assert any(
        step.act is restore.Act.REPLACE_TREE and step.target == coupled
        for step in decided.steps
    ), "the plan does not replace the coupled directory, so this proves nothing"
    return decided, coupled


def test_round3_an_unwritable_coupled_directory_refuses_at_the_rehearsal(cfg, held):
    """BLOCKING 2: renaming the coupled directory needs write permission on it."""
    decided, coupled = _replacing_the_coupled_tree(cfg, held)
    assert os.access(coupled.parent, os.W_OK), "the parent must stay writable"
    coupled.chmod(0o500)
    try:
        cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    finally:
        coupled.chmod(0o700)

    assert cause.reason == "restore-step-failed"
    assert str(coupled) in cause.message
    # Nothing was touched: the rehearsal refused before the first destructive step.
    assert _database(cfg).read_bytes() == _GENERATION_ONE
    assert reconcile.outstanding(cfg) == ()


def test_round3_staged_companions_are_bounded_by_the_keep_count(cfg, acked, record):
    """Staged attempts are pruned to five, newest kept, pinned by literals."""
    store = None
    for attempt in range(6):
        _wal_path(cfg).write_bytes(f"attempt {attempt}".encode())
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            decided = restore.plan(cfg, record.session_id, held=open_session)
            restore.run(decided, cfg, held=open_session)
            store = decided.pre_restore_root.parent

    kept = sorted(entry for entry in store.iterdir() if entry.is_dir())
    assert len(kept) == 5, "six attempts must leave five staged directories"
    # The newest survive.
    surviving = {
        path.read_bytes()
        for root in kept
        for path in root.iterdir()
        if path.name.endswith("wal")
    }
    assert surviving == {f"attempt {attempt}".encode() for attempt in range(1, 6)}


# Fix round 4: the halves of a claimed fix that nothing could see


def _staged_attempt(store: Path, name: str, *, age: int, payload: bytes = b"") -> Path:
    """One staged-companion directory with an explicit mtime, which the prune orders on."""
    attempt = store / name
    attempt.mkdir(parents=True)
    (attempt / "master.db-wal").write_bytes(payload)
    when = 1_700_000_000 + age
    os.utime(attempt, (when, when))
    return attempt


def test_round4_a_completed_restore_survives_a_staged_attempt_it_cannot_prune(cfg, acked, record):
    """An unprunable staged attempt is logged, not raised, or a landed restore closes ABANDONED."""
    _wal_path(cfg).write_bytes(b"transactions no capture holds")
    store = _database(cfg).parent / restore.PRE_RESTORE_DIR
    # The oldest attempt is undeletable, with enough younger ones to reach it.
    locked = _staged_attempt(store, "attempt-locked", age=0, payload=b"the earliest log")
    fillers = [
        _staged_attempt(store, f"attempt-{index}", age=index + 1)
        for index in range(restore.KEEP_STAGED_ATTEMPTS)
    ]
    locked.chmod(0o500)
    try:
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            recovery_id = open_session.record.session_id
            decided = restore.plan(cfg, record.session_id, held=open_session)
            outcome = restore.run(decided, cfg, held=open_session)
    finally:
        locked.chmod(0o700)

    assert outcome.converged, "a restore that landed correctly reported failure"
    assert session.read_record(recovery_id, cfg).state is session.SessionState.CLOSED
    assert not fillers[0].exists(), "the prune never reached the bound"
    assert (locked / "master.db-wal").read_bytes() == b"the earliest log"
    assert _database(cfg).read_bytes() == _GENERATION_ONE


def test_round4_an_unwritable_state_directory_refuses_at_the_rehearsal(cfg, held):
    """The coupled target's unwritable parent refuses, read off an anchored message."""
    decided, coupled = _replacing_the_coupled_tree(cfg, held)
    parent = coupled.parent
    assert parent != _database(cfg).parent, "the two parents must be different directories"
    parent.chmod(0o500)
    assert os.access(coupled, os.W_OK), "the target must stay writable"
    try:
        cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    finally:
        parent.chmod(0o700)

    assert cause.reason == "restore-step-failed"
    assert cause.detail["unwritable"] == str(parent)
    assert cause.message.startswith(f"{parent} is not writable")
    # Nothing was touched: the rehearsal refused before the first destructive step.
    assert _database(cfg).read_bytes() == _GENERATION_ONE
    assert reconcile.outstanding(cfg) == ()


def _playlist_xml_path(cfg) -> Path:
    """The playlist document, which puts a REMOVE ahead of the coupled REPLACE_TREE."""
    return _database(cfg).parent / rb_writer.MASTER_PLAYLIST_XML


def _captured_entries(decided) -> list:
    """The manifest entries of the plan's capture that hold a captured copy."""
    manifest = snapshot.read_manifest(decided.capture_root)
    return [entry for entry in manifest.sources if entry.captured is not None]


def _assert_the_pinned_allocations(cfg, decided) -> None:
    """Pinned so a filesystem that allocates differently fails here."""
    captured = {entry.source.name: entry.captured for entry in _captured_entries(decided)}
    assert snapshot.incoming_bytes(captured["master.db"]) == 6144
    assert snapshot.incoming_bytes(captured["coupled"]) == 8192
    assert snapshot.freed_bytes(_database(cfg)) == 4096
    assert snapshot.freed_bytes(config.library_coupled_dir(cfg)) == 4096


def test_round4_the_peak_of_an_ordinary_plan_is_an_exact_number(cfg, held):
    """An exact peak, derived by hand: 6,144 for the database, then max(6,144, 2,048 + 8,192)."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, decided = _planned(cfg, held)

    _assert_the_pinned_allocations(cfg, decided)

    assert restore.space_peak_bytes(decided) == 10240


def test_round4_a_removal_ahead_of_a_tree_replacement_lowers_the_peak(cfg, held):
    """A smaller removal ahead of the tree lowers the peak, derived by hand:
    max(6,144, 2,048 - 8,192 + 1,060,864) = 1,054,720."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    queue = config.state_path("review_queue", cfg)
    assert config.library_coupled_dir(cfg) in queue.parents, "the capture would not carry it"
    queue.mkdir(parents=True, exist_ok=True)
    (queue / "item-00000.json").write_bytes(b"q" * 1024 * 1024)
    record, _captured = completed_session(cfg)
    # Created after the capture, so the plan removes it and frees real bytes.
    playlists = _playlist_xml_path(cfg)
    playlists.write_bytes(b"p" * 8192)
    decided = restore.plan(cfg, record.session_id, held=held)

    acts = [step.act for step in decided.steps if step.target is not None]
    assert acts.index(restore.Act.REMOVE) < acts.index(restore.Act.REPLACE_TREE), acts
    captured = {entry.source.name: entry.captured for entry in _captured_entries(decided)}
    assert snapshot.incoming_bytes(captured["master.db"]) == 6144
    assert snapshot.incoming_bytes(captured["coupled"]) == 1060864
    assert snapshot.freed_bytes(_database(cfg)) == 4096
    assert snapshot.freed_bytes(config.library_coupled_dir(cfg)) == 1052672
    assert snapshot.freed_bytes(playlists) == 8192

    assert restore.space_peak_bytes(decided) == 1054720


def test_round4_the_default_retention_count_is_five(cfg):
    """``DEFAULT_KEEP`` is five, over seven captures all past the age bound."""
    now = datetime.now(UTC)
    made = [take_capture(cfg, stamp=f"capture-{index}") for index in range(7)]
    for index, captured in enumerate(made):
        _age_capture(captured.root, days=90 - index, now=now)

    decided = restore.retention_plan(cfg, protected_provider=set, now=now)

    assert len(decided.keeping) == 5, "the default count is not five"
    assert len(decided.deleting) == 2
    assert [entry.root for entry in decided.deleting] == [made[1].root, made[0].root]


def test_round4_a_volume_just_above_what_the_rule_demands_is_not_refused(
    cfg, held, monkeypatch
):
    """P7: free space exactly what the rule demands is accepted (``>=``, not ``>``)."""
    _build_capacity_shape(cfg, **_CAPACITY_SHAPE)
    record, decided = _planned(cfg, held)

    demanded = int(restore.space_peak_bytes(decided) * snapshot.CAPACITY_HEADROOM)
    summed = sum(snapshot.incoming_bytes(entry.source) for entry in _captured_entries(decided))
    assert restore.space_peak_bytes(decided) < summed, "the round 1 rule would accept it too"

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: demanded)
    outcome = restore.run(decided, cfg, held=held)

    assert outcome.converged, "the tightest volume the rule allows was refused"
    assert _database(cfg).read_bytes()[:1] == b"d"


def test_round5_the_capacity_headroom_decides_a_refusal_at_two_literal_volumes(
    cfg, held, monkeypatch
):
    """``CAPACITY_HEADROOM`` is in ``(1.05, 1.10]``: 10,752 free bytes refused, 11,264 accepted."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, decided = _planned(cfg, held)

    _assert_the_pinned_allocations(cfg, decided)

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 10752)
    cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)

    assert cause.reason == "snapshot-store-full"
    assert cause.detail["required_bytes"] == 11264
    assert _database(cfg).read_bytes() == _GENERATION_ONE

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 11264)
    outcome = restore.run(decided, cfg, held=held)

    assert outcome.converged, "the volume the headroom asks for was refused"


def _live_log(cfg, payload: bytes = _LIVE_LOG) -> Path:
    """The live write-ahead log, holding ``payload``."""
    log = _wal_path(cfg)
    log.write_bytes(payload)
    return log


def _occupy(decided, name: str, payload: bytes) -> Path:
    """An earlier attempt's ``name`` at the resting place this plan stages into."""
    decided.pre_restore_root.mkdir(parents=True)
    (decided.pre_restore_root / name).write_bytes(payload)
    return decided.pre_restore_root / name


def _shm_path(cfg) -> Path:
    """The live shared-memory index, resolved through the inventory like the log."""
    database = _database(cfg)
    companions = config.sidecar_paths("rekordbox_db", cfg)
    return next(
        path
        for path in companions
        if path.name.startswith(database.name) and path != _wal_path(cfg)
    )


def test_round5_a_staged_companion_is_never_written_over(cfg, held):
    """A staged log is the only copy of its transactions, so it is never written over."""
    log = _live_log(cfg)
    record, decided = _planned(cfg, held)
    assert log in [
        step.target for step in decided.steps if step.act is restore.Act.CLEAR
    ], "this plan does not stage the log aside, so it proves nothing"

    # An earlier attempt's log under the name this one wants.
    survivor = _occupy(decided, log.name, _EARLIER_LOG)
    cause = _refusal(restore.run, decided, cfg, held=held)
    assert cause.reason == "restore-staging-occupied"
    assert cause.code is ExitCode.PRECONDITION
    assert survivor.read_bytes() == _EARLIER_LOG
    assert log.read_bytes() == _LIVE_LOG, "the live log was moved anyway"


def test_round6_the_occupied_staging_is_a_repeat_rather_than_a_defect(cfg, held):
    """An occupied staging is retryable, said in steps, and a fresh plan completes."""
    log = _live_log(cfg)
    record, _captured = completed_session(cfg)
    _database(cfg).write_bytes(b"database, generation two")
    decided = restore.plan(cfg, record.session_id, held=held)
    _occupy(decided, log.name, b"an earlier attempt's log")
    cause = _refusal(restore.run, decided, cfg, held=held)
    assert cause.retryable is True, "a condition a repeat clears is retryable"
    assert cause.remediation.remedy is None, "steps, not a token telling the user to file a bug"
    assert any("safe to repeat" in step for step in cause.remediation.steps), cause.remediation
    assert cause.detail["target"] == str(log)
    assert cause.detail["staged"] == str(decided.pre_restore_root / log.name)
    assert cause.detail["staging_root"] == str(decided.pre_restore_root)
    assert cause.detail["already_staged"] == [log.name]

    # Do what the steps say; a fresh plan takes a fresh staging directory.
    again = restore.plan(cfg, record.session_id, held=held)
    assert again.pre_restore_root != decided.pre_restore_root
    outcome = restore.run(again, cfg, held=held)
    assert outcome.converged, "the retry the refusal recommends does not work"
    assert _database(cfg).read_bytes() == _GENERATION_ONE
    assert (decided.pre_restore_root / log.name).read_bytes() == (
        b"an earlier attempt's log"
    ), "the retry destroyed the bytes the refusal existed to protect"


def test_round6_the_rehearsal_refuses_the_collision_the_real_run_refuses(cfg, held):
    """The rehearsal refuses the run's collision before the first companion moves."""
    log = _wal_path(cfg)
    index = _shm_path(cfg)
    log.write_bytes(_LIVE_LOG)
    index.write_bytes(b"the live shared-memory index")
    record, decided = _planned(cfg, held)
    cleared = [step.target for step in decided.steps if step.act is restore.Act.CLEAR]
    assert cleared == [log, index], f"both companions are not cleared in order: {cleared}"

    # The second companion's resting name is occupied.
    _occupy(decided, index.name, b"an earlier attempt's index")
    rehearsal = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    assert rehearsal.reason == "restore-staging-occupied"
    assert log.read_bytes() == _LIVE_LOG, "the rehearsal moved the first companion"
    real = _refusal(restore.run, decided, cfg, held=held)
    assert real.reason == rehearsal.reason, "the rehearsal and the run disagree"
    assert log.read_bytes() == _LIVE_LOG, "the run refused half done, a companion moved"
    assert _database(cfg).read_bytes() == _GENERATION_ONE


def test_round6_the_performing_backstop_names_what_it_already_moved(cfg, held, monkeypatch):
    """A collision landing after the preflight names the companion already moved, driven."""
    log = _wal_path(cfg)
    index = _shm_path(cfg)
    log.write_bytes(_LIVE_LOG)
    index.write_bytes(b"the live shared-memory index")
    record, decided = _planned(cfg, held)

    real_stage = restore._stage_companion_aside

    def stage_then_race(target: Path, staging: Path) -> None:
        real_stage(target, staging)
        intruder = staging / index.name
        if target != index and not intruder.exists():
            intruder.write_bytes(b"an earlier attempt's index")

    monkeypatch.setattr(restore, "_stage_companion_aside", stage_then_race)

    cause = _refusal(restore.run, decided, cfg, held=held)

    assert cause.reason == "restore-staging-occupied"
    assert cause.detail["already_staged"] == sorted([log.name, index.name])
    assert log.name in cause.message
    assert str(decided.pre_restore_root) in cause.message
    assert any(
        str(decided.pre_restore_root) in step for step in cause.remediation.steps
    ), f"no step says where the moved companion is: {cause.remediation.steps}"
    assert (decided.pre_restore_root / log.name).read_bytes() == _LIVE_LOG, "not where it says"


def test_round6_a_dangling_link_at_the_resting_name_is_a_name_already_taken(cfg, held):
    """A dangling link at the resting name is a taken name, so ``lexists`` is asked."""
    log = _live_log(cfg)
    record, decided = _planned(cfg, held)
    decided.pre_restore_root.mkdir(parents=True)
    taken = decided.pre_restore_root / log.name
    taken.symlink_to(decided.pre_restore_root / "a-target-that-is-not-there")
    assert not taken.exists(), "this link resolves, so it is not the shape under test"
    assert taken.is_symlink()
    cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    assert cause.reason == "restore-staging-occupied"
    assert taken.is_symlink(), "the link was replaced, which is the defect"
    assert log.read_bytes() == _LIVE_LOG


def test_round6_a_dangling_link_at_the_live_companion_is_still_moved_aside(cfg, held):
    """A dangling live companion link is moved aside, since the engine creates through it."""
    log = _wal_path(cfg)
    log.symlink_to(log.parent / "somewhere-that-is-not-there")
    assert not log.exists() and log.is_symlink()
    record, decided = _planned(cfg, held)

    outcome = restore.run(decided, cfg, held=held)

    assert outcome.converged
    assert not log.is_symlink(), "a dangling link the engine writes through is still there"
    staged = decided.pre_restore_root / log.name
    assert staged.is_symlink(), "the link was not moved aside, it was lost"


def test_round6_a_dangling_link_at_the_live_name_does_not_defeat_the_collision_guard(
    cfg, held
):
    """The guard's early return asks ``lexists`` too (found by mutation)."""
    log = _wal_path(cfg)
    log.symlink_to(log.parent / "somewhere-that-is-not-there")
    record, decided = _planned(cfg, held)
    survivor = _occupy(decided, log.name, _EARLIER_LOG)
    cause = _refusal(restore.run, decided, cfg, held=held, dry_run=True)
    assert cause.reason == "restore-staging-occupied"
    assert survivor.read_bytes() == _EARLIER_LOG, "renamed over the only copy"
    assert log.is_symlink(), "the live name was consumed by a rehearsal"


def test_round7_an_unreadable_staging_directory_still_refuses_the_same_way(cfg, held):
    """``_staged_names`` never raises: mode ``0o111`` sees the occupant while iterdir fails."""
    log = _live_log(cfg)
    record, decided = _planned(cfg, held)
    survivor = _occupy(decided, log.name, _EARLIER_LOG)
    decided.pre_restore_root.chmod(0o111)
    try:
        assert os.path.lexists(survivor), "the occupant is hidden from lexists too"
        with pytest.raises(OSError):
            list(decided.pre_restore_root.iterdir())

        cause = _refusal(restore.run, decided, cfg, held=held)
    finally:
        decided.pre_restore_root.chmod(0o700)

    assert cause.reason == "restore-staging-occupied", cause.reason
    assert cause.code is ExitCode.PRECONDITION
    assert cause.retryable is True
    assert cause.detail["target"] == str(log)
    assert cause.detail["staged"] == str(survivor)
    assert cause.detail["staging_root"] == str(decided.pre_restore_root)
    assert cause.detail["already_staged"] == [], "the listing failed, so nothing is known"
    assert survivor.name in cause.message, cause.message
    assert survivor.read_bytes() == _EARLIER_LOG
    assert log.read_bytes() == _LIVE_LOG, "the live log was moved anyway"


def test_round6_a_retry_after_a_partial_failure_still_runs(cfg, held):
    """A retry after a partial failure proceeds and keeps the earlier staged log."""
    log = _live_log(cfg, b"the first attempt's log")
    record, _captured = completed_session(cfg)
    _database(cfg).write_bytes(b"database, generation two")
    first = restore.plan(cfg, record.session_id, held=held)

    def _explode(_source, _target):
        raise OSError(28, "No space left on device")

    with pytest.MonkeyPatch.context() as full_disk:
        full_disk.setattr(restore, "_replace_file", _explode)
        cause = _refusal(restore.run, first, cfg, held=held)
    assert cause.reason == "restore-step-failed"
    stranded = first.pre_restore_root / log.name
    assert stranded.read_bytes() == b"the first attempt's log"
    log.write_bytes(b"the second attempt's log")
    second = restore.plan(cfg, record.session_id, held=held)
    outcome = restore.run(second, cfg, held=held)
    assert outcome.converged, "the retry the sibling refusal promises was refused"
    assert _database(cfg).read_bytes() == _GENERATION_ONE
    assert stranded.read_bytes() == b"the first attempt's log", "the retry overwrote it"
    assert (second.pre_restore_root / log.name).read_bytes() == (
        b"the second attempt's log"
    )


def test_round4_the_residual_findings_this_module_names_still_exist():
    """restore.py cites residual titles, which must resolve and be cited in docstring prose."""
    ledgers = [*sorted((REPO_ROOT / "docs" / "ledger").glob("*.md"))]
    ledgers.append(REPO_ROOT / "docs" / "residual-findings.md")
    text = "".join(path.read_text(encoding="utf-8") for path in ledgers)
    headings = {found.strip() for found in re.findall(r"^## R-\d+\.\s*(.+)$", text, re.MULTILINE)}
    names = ("RESIDUAL_CAPTURE_VOLUME_UNREPORTED", "RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH")
    named = {getattr(restore, name) for name in names}

    assert named <= headings, sorted(named - headings)

    # Each name is cited in prose, not only defined and exported.
    source = Path(inspect.getfile(restore)).read_text(encoding="utf-8")
    documented = [
        ast.get_docstring(node) or ""
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
    ]
    assert documented, "restore.py parsed to no docstrings at all"
    for name in names:
        assert any(name in text for text in documented), f"no docstring cites {name}"
