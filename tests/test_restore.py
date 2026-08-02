"""U32: restore, retention, and reconciliation.

The plan's six test scenarios, one section each, plus the four obligations that
were registered against this unit rather than written in its brief and the
hazards an author's own green suite cannot see.

* AE18. A completed session appears with its timestamp, workflow and change
  summary, and its capture restores the library to its pre-session bytes.
* Restoring across a later committed session refuses without the override, and
  the refusal names the affected trees and their counts.
* A restore whose window holds an advanced watermark, a consumed remote prefix
  and a written tombstone lists all three and blocks convergence until each one
  is dispositioned.
* A restore predating a cutover marks that tree unconverged, and both an
  ordinary destructive session and a run close refuse until it is cleared.
* Pruning refuses before the session it belongs to has committed, and retention
  respects the byte bound as well as the count and the age.
* With the capture store below threshold, a session refuses BEFORE snapshotting
  and leaves no partial file.

And the registered obligations:

* the restore replaces exactly the derived coupled set and keeps the storage
  engine's companion asymmetry;
* one session spans the plan and the run, and the off-machine backup restore
  takes that open guard rather than acquiring its own;
* the condemning session record is resolved after a successful restore, because
  the log survives the rollback that answers it;
* bare-metal recovery, where the library volume itself is gone, has a path of
  its own and is unreachable while the ordinary gates could be read.

EVERYTHING IS HERMETIC AND EVERY FIXTURE IS SYNTHETIC. The database in these
tests is a few bytes of text in a temporary directory, the integrity verdict is
injected, the volume identity is injected, and the terminal probe is injected. No
test here opens, copies, or names a real rekordbox database, and none of them
needs a library volume.
"""

from __future__ import annotations

import ast
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

#: The identity a foreign disk reports. Any value that is not the fixture's.
_ELSEWHERE = "0000-0000-not-this-disk"


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library, SAVED, so a second interpreter resolves the same one.

    The environment variable is set as well as the file, and it has to be: the
    suite's isolation fixture already points the library root somewhere, and
    ``from_dict`` relocates a configured root onto whatever the environment says.
    Writing only the file would leave the value under test and the value in force
    as two different directories, which is the P2 shape exactly.
    """
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
    config.state_path("rekordbox_db", built).write_bytes(b"database, generation one")
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


def matching_identity(cfg):
    return lambda _path: cfg.library.volume_id


def gate_seams(cfg, **overrides):
    """The real gates with only the platform seams injected."""
    arguments = {"identity_provider": matching_identity(cfg), "mount_enumerator": lambda: ()}
    arguments.update(overrides)
    return arguments


def acknowledge(cfg):
    return session.record_acknowledgment(cfg, terminal=lambda: True)


def always_verified(_path: Path) -> bool:
    """The integrity seam, answering yes.

    Injected rather than run, because the fixture database is a few bytes of text
    and the real check opens it as SQLite. That seam exists precisely so the
    battery can drive both verdicts without a rekordbox database, and the
    no-verdict branch is driven below.
    """
    return True


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
    """One session that captured, committed a source, and ended.

    The change summary is per tree because that is the only form in which the
    override refusal can name what a person is about to lose.
    """
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


@pytest.fixture
def held(cfg):
    """One open recovery session, the way the verb will hold it."""
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        yield open_session


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 1 (AE18): a completed session is listed and its capture restores
# ═══════════════════════════════════════════════════════════════════════════


def test_a_completed_session_is_listed_with_its_timestamp_workflow_and_changes(cfg):
    record, _captured = completed_session(cfg)

    listed = restore.list_sessions(cfg)

    assert [entry.session_id for entry in listed] == [record.session_id]
    only = listed[0]
    assert only.started == record.started
    assert only.workflow == "library-sweep"
    assert [(t.tree, t.created, t.updated) for t in only.change.trees] == [("routing", 3, 1)]
    assert only.restorable


def test_a_restore_returns_a_modified_database_to_its_pre_session_bytes(cfg, held):
    """The unit's own verification gate, run against a synthetic library.

    The half that needs real hardware is stated in the report rather than faked:
    this proves the mechanism returns the exact bytes, and it proves nothing
    about a real rekordbox database, which is a separate gate and is deferred.
    """
    before = config.state_path("rekordbox_db", cfg).read_bytes()
    record, _captured = completed_session(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    assert config.state_path("rekordbox_db", cfg).read_bytes() == before


def test_a_restore_returns_the_coupled_state_with_the_database(cfg, held):
    """The coupling IS the unit. Either both roll back or the capture is useless."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "after"})
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    assert json.loads(config.state_path("label_watermarks", cfg).read_text()) == {
        "source": "before"
    }


def test_a_coupled_file_the_capture_records_as_absent_is_removed_again(cfg, held):
    """Absence in a manifest is an instruction, not a gap.

    The capture records the difference between "there was nothing to put back"
    and "we never looked". A restore that skipped the absent ones would leave a
    file the discarded session created standing behind a database that has never
    heard of it.
    """
    record, _captured = completed_session(cfg)
    created_after = write_state(cfg, "tombstones", {"version": 1, "store": "tombstones"})
    assert created_after.exists()

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

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

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, record.session_id, held=held)

    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 2: restoring across a later committed session
# ═══════════════════════════════════════════════════════════════════════════


def test_restoring_across_a_later_committed_session_refuses_and_names_the_counts(cfg, held):
    older, _ = completed_session(cfg, started="2026-08-01T09:00:00+00:00", stamp="older")
    completed_session(
        cfg,
        started="2026-08-02T09:00:00+00:00",
        stamp="newer",
        trees=(("routing", 7, 2), ("intake", 1, 0)),
    )

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, older.session_id, held=held)

    cause = excinfo.value.cause
    assert cause.reason == "restore-discards-committed-work"
    assert cause.code is ExitCode.DECISION_REQUIRED
    # Tree AND count, both, because one aggregate number cannot answer the
    # question the person is being asked.
    assert "routing: 7 created, 2 updated" in cause.message
    assert "intake: 1 created, 0 updated" in cause.message


def test_the_override_has_to_name_exactly_the_sessions_it_discards(cfg, held):
    older, _ = completed_session(cfg, started="2026-08-01T09:00:00+00:00", stamp="older")
    newer, _ = completed_session(cfg, started="2026-08-02T09:00:00+00:00", stamp="newer")

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, older.session_id, held=held, discarding=["not-that-session"])
    assert excinfo.value.cause.reason == "restore-discards-committed-work"

    decided = restore.plan(cfg, older.session_id, held=held, discarding=[newer.session_id])

    assert decided.discarded_sessions == (newer.session_id,)


def test_a_later_session_that_committed_nothing_does_not_need_an_override(cfg, held):
    """A refusal that fires on the ordinary case is a refusal people route around.

    A session that opened, refused, and abandoned wrote nothing, so a restore
    reaching past it discards nothing and must not ask.
    """
    older, _ = completed_session(cfg, started="2026-08-01T09:00:00+00:00", stamp="older")
    idle = session.open_session(cfg, workflow="library-sweep", sources=("source-b",))
    idle.started = "2026-08-02T09:00:00+00:00"
    session.close_session(idle, cfg, state=session.SessionState.ABANDONED)

    decided = restore.plan(cfg, older.session_id, held=held)

    assert decided.discarded_sessions == ()


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 3: reconciliation of what a restore cannot undo
# ═══════════════════════════════════════════════════════════════════════════


def test_a_restore_lists_every_effect_it_cannot_undo_and_blocks_convergence(cfg, held):
    """The plan's third scenario, exactly: three markers, three dispositions.

    The window holds an advanced watermark, whose advance both landed audio on
    the volume and consumed a playlist prefix at the provider, and a written
    tombstone, whose file is in the Trash. The rows roll back; none of those
    three does.
    """
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


def test_an_unreconciled_restore_refuses_the_next_ordinary_session(cfg):
    acknowledge(cfg)
    reconcile.record_markers(
        cfg,
        reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c"),
    )

    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
            raise AssertionError("the gates admitted a session they should have refused")

    assert excinfo.value.cause.reason == "restore-reconciliation-outstanding"
    assert excinfo.value.cause.code is ExitCode.UNCONVERGED


def test_a_recovery_is_not_refused_by_the_latch_whose_remedy_it_is(cfg):
    """The lesson U8 paid for, applied to the second latch.

    A second restore is one of the things a person may legitimately do about the
    first one. A latch that condemned its own remedy would leave a library with
    no exit but a hand-edited file.
    """
    acknowledge(cfg)
    reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )

    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        assert open_session.intent is session.Intent.RECOVERY


def test_the_markers_are_enumerated_before_anything_is_replaced(cfg, held):
    """The ordering IS the correctness. Afterwards every comparison is equal.

    Driven by asserting the recording step comes first in the one list both the
    preview and the write walk, rather than by trusting the prose.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "after"})

    decided = restore.plan(cfg, record.session_id, held=held)

    assert decided.steps[0].act is restore.Act.RECORD
    assert all(step.act is not restore.Act.RECORD for step in decided.steps[1:])


def test_a_marker_is_keyed_on_a_persisted_identity_rather_than_a_display_name(cfg):
    """A record keyed on anything a user can rename diverges instead of converging.

    The identity of an effect marker is the inventory key, which this product
    chooses and nobody can rename; the identity of a tree marker is the
    taxonomy's stable tree identifier. Neither is derived from anything a person
    sees in rekordbox.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 4: a restore predating a cutover
# ═══════════════════════════════════════════════════════════════════════════


def _cut_over(cfg, tree_id: str = "routing") -> None:
    tree_registry.record_cutover(cfg, tree_id, root_id="row-1", on=date(2026, 8, 2))


def test_a_restore_predating_a_cutover_marks_that_tree_unconverged(cfg, held):
    record, _captured = completed_session(cfg)
    _cut_over(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)

    assert decided.unconverged == ("routing",)
    restore.run(decided, cfg, held=held)
    assert reconcile.unconverged_trees(cfg) == ("routing",)


def test_a_restore_taken_after_the_cutover_marks_nothing(cfg, held):
    """P7 in the same file as the guard: run it against correct behaviour too.

    A capture taken after the flip holds a registry that already says database
    native, so restoring it changes nothing about which medium owns the tree and
    must not demand a rebuild.
    """
    _cut_over(cfg)
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)

    assert decided.unconverged == ()


def test_an_unconverged_tree_refuses_the_next_sync_and_the_next_close(cfg):
    acknowledge(cfg)
    reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )

    with pytest.raises(CratekitError) as sync_refusal:
        with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
            raise AssertionError("unreachable")

    stranded = session.open_session(cfg, workflow="library-sweep")
    with pytest.raises(CratekitError) as close_refusal:
        session.close_session(stranded, cfg)

    for refusal in (sync_refusal, close_refusal):
        assert refusal.value.cause.reason == "restore-reconciliation-outstanding"
    assert "never by a decision" in close_refusal.value.cause.message


def test_abandoning_a_run_is_never_gated_on_convergence(cfg):
    """Closing is the claim that the work finished; abandoning is the opposite.

    Gating both would leave somebody with a run they can neither finish nor give
    up on, and a refusal with no way past it is how people learn to edit state
    files by hand.
    """
    reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )
    stranded = session.open_session(cfg, workflow="library-sweep")

    ended = session.close_session(stranded, cfg, state=session.SessionState.ABANDONED)

    assert ended.state is session.SessionState.ABANDONED


def test_clearing_the_tree_marker_lets_the_next_session_through(cfg):
    acknowledge(cfg)
    recorded = reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )
    reconcile.close_marker(
        cfg, recorded[0].marker.marker_id, disposition=reconcile.Disposition.REPAIRED, actor="rebuild"
    )

    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 5: retention
# ═══════════════════════════════════════════════════════════════════════════


def _age_capture(root: Path, *, days: int, now: datetime) -> None:
    when = (now - timedelta(days=days)).timestamp()
    os.utime(root, (when, when))


def test_pruning_refuses_before_the_session_it_belongs_to_has_committed(cfg):
    record = session.open_session(cfg, workflow="library-sweep")
    captured = take_capture(cfg)
    session.attach_capture(record, captured.root, cfg)

    with pytest.raises(CratekitError) as excinfo:
        restore.prune(cfg, owning=record)

    assert "has not committed" in excinfo.value.cause.message
    assert captured.root.is_dir()

    session.close_session(record, cfg)
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
    """The bound the source system has no equivalent of, and the reason for three.

    Every capture here is inside the age bound and inside the count bound, so
    neither of the other two would delete anything. A run of small captures that
    fills a volume is exactly what the third bound exists for.
    """
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
    # Oldest first: the byte bound is the least specific of the three and should
    # give up the least useful capture.
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
    """R30 asks that it does not, and the recommended layout means it does.

    Reported rather than refused, because refusing would make the product
    unusable in the layout it recommends, which is the shape of a guard people
    switch off. The comparison is on the filesystem identifier, so a symlink or a
    nested mount cannot make it confidently wrong.
    """
    take_capture(cfg, stamp="one")

    decided = restore.retention_plan(cfg)

    assert decided.shares_the_database_volume is True


# ═══════════════════════════════════════════════════════════════════════════
# Scenario 6: capacity
# ═══════════════════════════════════════════════════════════════════════════


def test_a_session_refuses_before_snapshotting_when_the_store_cannot_fit_one(
    cfg, monkeypatch
):
    """The plan's sixth scenario, driven through a real destructive session.

    The session opens, passes all three gates, and then refuses at the capture
    rather than committing behind a truncated copy. The free-space probe is the
    injected seam; everything else is the real path.
    """
    acknowledge(cfg)
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 1)

    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
        record = session.open_session(cfg, workflow="library-sweep")
        with pytest.raises(CratekitError) as excinfo:
            snapshot.capture(cfg, verifier=always_verified)

    assert excinfo.value.cause.reason == "snapshot-store-full"
    assert record.snapshot_path is None, "a refused capture is never attached"


def test_a_refused_capture_leaves_no_partial_file(cfg, monkeypatch):
    """The whole property: refuse BEFORE the copy, not part way through it.

    A copy that ran out of room leaves a truncated database inside a directory
    that looks like a capture, and the session then commits behind it. The state
    tree is compared byte for byte on both sides of the refusal.
    """
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 1)
    store = snapshot.store_root(cfg)
    before = _fingerprint(store.parent)

    with pytest.raises(CratekitError) as excinfo:
        snapshot.capture(cfg, verifier=always_verified)

    cause = excinfo.value.cause
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


def test_a_platform_that_cannot_report_free_space_does_not_refuse(cfg, monkeypatch):
    """None is not zero, and reading silence as a full disk breaks a working machine."""
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: None)

    captured = snapshot.capture(cfg, verifier=always_verified)

    assert captured.root.is_dir()


def _fingerprint(root: Path) -> dict[str, int]:
    found: dict[str, int] = {}
    if not root.exists():
        return found
    for current, _directories, files in os.walk(root):
        for name in files:
            path = Path(current) / name
            try:
                found[str(path)] = path.stat().st_size
            except OSError:
                continue
    return found


# ═══════════════════════════════════════════════════════════════════════════
# The registered obligations: the derived set and the companion asymmetry
# ═══════════════════════════════════════════════════════════════════════════


def test_a_restore_replaces_exactly_the_derived_coupled_set(cfg, held):
    """Every target comes from the inventory, and nothing else is reachable."""
    record, captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)

    allowed = restore.restorable_targets(cfg)
    touched = {step.target for step in decided.steps if step.target is not None}
    assert touched
    assert touched <= allowed


def test_no_restore_target_is_a_lock_or_a_record_that_survives_a_rollback(cfg):
    """The hazard this unit exists to prove is closed, asserted over the whole set.

    A restore that replaced a directory holding a lock would swap the inode every
    holder is waiting on, and both processes would then believe they had
    exclusive access with nothing raised. Derived by walking the inventory rather
    than by naming the two locks somebody happens to remember (P3).
    """
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


def test_the_live_companion_files_are_cleared_before_anything_is_copied(cfg, held):
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)

    acts = [step.act for step in decided.steps if step.act is not restore.Act.RECORD]
    first_copy = next(
        index for index, act in enumerate(acts) if act in {restore.Act.REPLACE, restore.Act.REPLACE_TREE}
    )
    assert all(act is restore.Act.CLEAR for act in acts[:first_copy])
    cleared = {step.target for step in decided.steps if step.act is restore.Act.CLEAR}
    assert cleared == set(config.sidecar_paths("rekordbox_db", cfg))


def test_only_the_companion_the_inventory_declares_restored_is_written_back(cfg, held):
    """The asymmetry, driven rather than asserted about the source text.

    The shared-memory index is derived from the log, so restoring a stale one
    beside a fresh log hands the engine two disagreeing views of one database.
    Both are captured; exactly one comes back.
    """
    database = config.state_path("rekordbox_db", cfg)
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"companion, generation one")
    record, _captured = completed_session(cfg)
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"companion, generation two")

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    restored = set(config.sidecar_paths("rekordbox_db", cfg, restored_only=True))
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        if companion in restored:
            assert companion.read_bytes() == b"companion, generation one"
        else:
            assert not companion.exists(), (
                "a derived companion was written back beside a restored database"
            )
    assert database.exists()


def test_the_restore_module_spells_no_companion_suffix_of_its_own(cfg):
    """The same guard config already applies to the capture side, stated here too.

    A literal suffix in this module is the companion list the schema exists to
    abolish, and the specific cost is a restore that puts back a file the
    inventory says it must not.
    """
    source = Path(restore.__file__).read_text()
    assert "sidecar_paths" in source
    assert not re.search(r"""["'][^"']*-(?:wal|shm)""", source)


# ═══════════════════════════════════════════════════════════════════════════
# The registered obligations: one held session, and the resolved record
# ═══════════════════════════════════════════════════════════════════════════


def test_one_session_spans_the_plan_and_the_run(cfg, held):
    """A plan that gives the lock back leaves a window a second process commits in.

    Driven by the strongest available evidence: a second acquisition of the
    library lock inside the held block is refused as a foreign holder would be,
    so the lock demonstrably never left this process between the plan and the
    run.
    """
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    contender = _lock_taken_in_another_process(session.lock_path(cfg))
    assert contender != 0, "the library lock was released between the plan and the run"
    restore.run(decided, cfg, held=held)
    assert _lock_taken_in_another_process(session.lock_path(cfg)) != 0


def _lock_taken_in_another_process(path: Path) -> int:
    """Try to take the lock in a REAL second interpreter. Zero means it succeeded.

    A thread would share this interpreter's open file descriptions, and an
    advisory lock is held per description, so a thread can only ever prove what
    this process already believes.
    """
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


def test_the_backup_restore_runs_inside_the_already_open_session(cfg, held, tmp_path):
    """The composition the command line owes, proven at the seam it goes through.

    ``plan_restore`` and ``run_restore`` each enter their ``gates`` seam. Handed
    the held session's pass-through guard, neither takes the library lock again,
    which is what makes the plan and the run one acquisition rather than two with
    a window between them.
    """
    target = tmp_path / "recovered"
    target.mkdir()
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
    """The latch survives its own remedy, so answering it is a deliberate step.

    Without this a user who did precisely what the refusal asked would find the
    next write still refused, with the remedy already spent and nothing left to
    spend.
    """
    record, _captured = completed_session(
        cfg, state=session.SessionState.COMMITTED_UNVERIFIED
    )

    decided = restore.plan(cfg, record.session_id, held=held)
    outcome = restore.run(decided, cfg, held=held)

    assert outcome.resolved == (record.session_id,)
    assert (
        session.read_record(record.session_id, cfg).state is session.SessionState.ABANDONED
    )
    # And the proof that matters: the next ordinary session is admitted.
    session.assert_no_unresolved_session(cfg)


def test_the_recovery_session_closes_its_own_record_on_both_paths(cfg):
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        good = open_session.record.session_id
    assert session.read_record(good, cfg).state is session.SessionState.CLOSED

    with pytest.raises(RuntimeError):
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            bad = open_session.record.session_id
            raise RuntimeError("the restore failed part way")
    assert session.read_record(bad, cfg).state is session.SessionState.ABANDONED


def test_a_restore_refuses_without_each_of_the_three_gates(cfg):
    """KTD24 binds to destruction, and a restore is the sharpest case of it.

    Three refusals, three distinct codes, and nothing written on any of them.
    """

    def refuse_with(**arguments) -> ExitCode:
        before = _fingerprint(cfg.library.root)
        with pytest.raises(CratekitError) as excinfo:
            with restore.recovery_session(cfg, **arguments):
                raise AssertionError("the gates admitted a recovery they should have refused")
        assert _fingerprint(cfg.library.root) == before
        return excinfo.value.cause.code

    wrong_volume = refuse_with(
        identity_provider=lambda _path: _ELSEWHERE, mount_enumerator=lambda: ()
    )
    no_acknowledgment = refuse_with(**gate_seams(cfg))

    acknowledge(cfg)
    lock = session.lock_path(cfg)
    config._mkdir_private(lock.parent)
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


# ═══════════════════════════════════════════════════════════════════════════
# The registered obligation: bare-metal recovery
# ═══════════════════════════════════════════════════════════════════════════


def _volume_is_gone(cfg) -> dict:
    """Make the configured library genuinely unreachable, the way a dead disk is."""
    shutil.rmtree(cfg.library.root, ignore_errors=True)
    return {
        "identity_provider": lambda _path: _ELSEWHERE,
        "mount_enumerator": lambda: (),
    }


def test_bare_metal_recovery_is_refused_while_the_library_is_reachable(cfg, tmp_path):
    target = tmp_path / "recovered"
    target.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg,
            target=target,
            acknowledged=True,
            terminal=lambda: True,
            **gate_seams(cfg),
        ):
            raise AssertionError("unreachable")

    cause = excinfo.value.cause
    assert cause.reason == "recovery-target-refused"
    assert "mounted" in cause.message


def test_a_volume_mounted_elsewhere_is_not_the_same_as_a_volume_that_is_gone(cfg, tmp_path):
    """Three answers, not two. The lesson the liveness probe already records."""
    seams = _volume_is_gone(cfg)
    somewhere = tmp_path / "somewhere-else"
    somewhere.mkdir()
    seams["identity_provider"] = (
        lambda path: cfg.library.volume_id if path == somewhere else _ELSEWHERE
    )
    seams["mount_enumerator"] = lambda: (somewhere,)
    target = tmp_path / "recovered"
    target.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "not absent" in excinfo.value.cause.message


def test_a_platform_that_cannot_report_an_identity_is_not_a_volume_that_is_gone(cfg, tmp_path):
    seams = _volume_is_gone(cfg)
    seams["identity_provider"] = lambda _path: None
    target = tmp_path / "recovered"
    target.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "not absent" in excinfo.value.cause.message


def test_bare_metal_recovery_refuses_the_stub_an_unmounted_volume_leaves_behind(cfg, tmp_path):
    """The hazard in one test: the mount point is now an empty folder on the boot disk.

    Restoring into it fills the internal disk and puts the result somewhere the
    volume hides the moment it is plugged back in. The check is on the filesystem
    identifier rather than on the path, because the path looks exactly right.
    """
    seams = _volume_is_gone(cfg)
    stub = Path(cfg.library.root)
    stub.mkdir(parents=True)

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=stub, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "empty folder an unmounted volume leaves behind" in excinfo.value.cause.message


def test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library(cfg, tmp_path):
    seams = _volume_is_gone(cfg)
    target = tmp_path / "recovered"
    target.mkdir()
    (target / "master.db").write_bytes(b"somebody else's library")

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "named for replacement" in excinfo.value.cause.message

    with restore.bare_metal_session(
        cfg,
        target=target,
        acknowledged=True,
        replacing_existing=True,
        terminal=lambda: True,
        **seams,
    ) as open_session:
        assert open_session.workflow == restore.BARE_METAL_WORKFLOW


def test_bare_metal_recovery_needs_a_terminal_and_an_explicit_decision(cfg, tmp_path):
    """The substitute for the acknowledgment, and its honest limit.

    The recorded acknowledgment R34 asks for lives on the volume that died, so
    there is no record to consult. What remains is that a detached invocation
    cannot proceed and that the decision is explicit.
    """
    seams = _volume_is_gone(cfg)
    target = tmp_path / "recovered"
    target.mkdir()

    with pytest.raises(CratekitError) as no_terminal:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=True, terminal=lambda: False, **seams
        ):
            raise AssertionError("unreachable")
    assert "no controlling terminal" in no_terminal.value.cause.message

    with pytest.raises(CratekitError) as not_accepted:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=False, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")
    assert "explicit decision" in not_accepted.value.cause.message


def test_bare_metal_recovery_takes_the_installation_lock_not_the_library_one(cfg, tmp_path):
    """Every gate KTD21 publishes sits on the disk that died. This is the substitute."""
    seams = _volume_is_gone(cfg)
    target = tmp_path / "recovered"
    target.mkdir()

    with restore.bare_metal_session(
        cfg, target=target, acknowledged=True, terminal=lambda: True, **seams
    ) as open_session:
        assert open_session.lock == restore.recovery_lock_path()
        assert _lock_taken_in_another_process(restore.recovery_lock_path()) != 0

    entry = config.state_file(restore.RECOVERY_LOCK_KEY)
    assert entry.root is config.StateRoot.INSTALLATION
    assert entry.snapshot is config.SnapshotRole.NEVER_RESTORED


# ═══════════════════════════════════════════════════════════════════════════
# The hazards a green suite cannot see
# ═══════════════════════════════════════════════════════════════════════════


def test_a_dry_run_and_a_real_run_walk_the_same_list_in_the_same_order(cfg, held):
    """A preview built by a second code path is a report about a different program."""
    record, _captured = completed_session(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")

    decided = restore.plan(cfg, record.session_id, held=held)
    rehearsed = restore.run(decided, cfg, held=held, dry_run=True)

    assert rehearsed.performed == decided.steps
    assert config.state_path("rekordbox_db", cfg).read_bytes() == b"database, generation two"

    real = restore.run(decided, cfg, held=held)

    assert real.performed == rehearsed.performed
    assert config.state_path("rekordbox_db", cfg).read_bytes() == b"database, generation one"


def test_a_rehearsal_never_clears_the_live_companion_files(cfg, held):
    """Clearing is itself destructive, so a preview that cleared would do the damage."""
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"companion, generation two")
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held, dry_run=True)

    for companion in config.sidecar_paths("rekordbox_db", cfg):
        assert companion.read_bytes() == b"companion, generation two"


def test_a_restore_refuses_while_rekordbox_holds_the_database(cfg, held, monkeypatch):
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    monkeypatch.setattr(
        "cratekit.core.processes.running_process_names", lambda: ("rekordbox",)
    )

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held)

    assert excinfo.value.cause.reason == "rekordbox-running"


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
    """The defect U11 shipped, refused here field by field.

    Every one of these reports that nothing is outstanding if the only guard is
    ``json.loads`` raising, and an empty result is then handed to the writer, so
    one further record deletes every prior marker from the disk.
    """
    path = reconcile.path_for(cfg)
    config._mkdir_private(path.parent)
    path.write_text(document)

    with pytest.raises(CratekitError) as excinfo:
        reconcile.outstanding(cfg)

    assert excinfo.value.cause.reason == "restore-record-unusable", why


def test_the_reconciliation_record_survives_eight_concurrent_writers(cfg):
    """The unlocked read-modify-write, driven with real processes.

    A thread shares this interpreter's memory and its locks, so it can only prove
    that a value was kept. Only a separate process shows what reached the disk,
    which is the whole question. Eight processes recording twenty five markers
    each must leave two hundred on the disk; the unlocked version of this loses
    more than half of them and every losing call returns a record reporting
    success.
    """
    script = (
        "import sys\n"
        "from cratekit.core import config, reconcile\n"
        "worker = sys.argv[1]\n"
        "cfg = config.load()\n"
        "for index in range(25):\n"
        "    reconcile.record_markers(\n"
        "        cfg,\n"
        "        reconcile.tree_markers([f'tree-{worker}-{index}'], session_id='s'),\n"
        "    )\n"
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(SRC_ROOT)
    running = [
        subprocess.Popen(
            [sys.executable, "-c", script, str(worker)],
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for worker in range(8)
    ]
    for process in running:
        out, err = process.communicate()
        assert process.returncode == 0, err or out

    assert len(reconcile.records(cfg)) == 200


def test_a_disposition_is_not_lost_under_concurrency(cfg):
    """A dropped revocation leaves a marker standing forever, so nobody finds out."""
    recorded = reconcile.record_markers(
        cfg, reconcile.tree_markers([f"tree-{index}" for index in range(20)], session_id="s")
    )
    script = (
        "import sys\n"
        "from cratekit.core import config, reconcile\n"
        "cfg = config.load()\n"
        "for marker_id in sys.argv[1:]:\n"
        "    reconcile.close_marker(\n"
        "        cfg, marker_id, disposition=reconcile.Disposition.ACCEPTED, actor='t'\n"
        "    )\n"
    )
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(SRC_ROOT)
    halves = [
        [entry.marker.marker_id for entry in recorded[:10]],
        [entry.marker.marker_id for entry in recorded[10:]],
    ]
    running = [
        subprocess.Popen(
            [sys.executable, "-c", script, *half],
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for half in halves
    ]
    for process in running:
        out, err = process.communicate()
        assert process.returncode == 0, err or out

    assert reconcile.outstanding(cfg) == ()


def test_every_coupled_entry_declares_what_leaves_the_coupled_set(cfg):
    """P4, enforced by PARSING the literal rather than by reading the runtime value.

    A default answer makes "somebody decided nothing happens" and "nobody
    decided" look identical at run time, and the second is how the next state
    entry with a real out-of-band effect is silently never reconciled. The source
    is parsed because that is the only place the difference is visible.
    """
    source = Path(config.__file__).read_text()
    tree = ast.parse(source)
    coupled = {entry.key for entry in config.coupled_state_files()}
    declared: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "StateFile"):
            continue
        fields = {keyword.arg: keyword.value for keyword in node.keywords}
        key = fields.get("key")
        if not isinstance(key, ast.Constant) or key.value not in coupled:
            continue
        assert "rollback_effects" in fields, (
            f"the coupled entry {key.value!r} does not say what its records caused "
            f"outside the set a restore replaces"
        )
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

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, record.session_id, held=held)

    assert "not a path any restore may replace" in excinfo.value.cause.message


def test_the_unconverged_decision_reads_the_captured_registry_not_a_date(cfg):
    """Date arithmetic is wrong by up to a day in both directions.

    Asserted structurally: the module reaches for the registry reader that takes
    an explicit path, which exists for this one caller, and it does not compare
    a cutover date against anything.
    """
    source = Path(restore.__file__).read_text()
    assert "read_path" in source
    assert "cutover_on" not in source


def test_a_held_session_used_after_its_block_is_refused(cfg):
    """A ``Held`` is an ordinary value and outlives the block that yielded it.

    Requiring one as a parameter makes it impossible to reach the write without
    having entered the guard ONCE, which is not the same as being inside it. This
    is the difference, and it is asked at the moment of the call rather than at
    construction, because that is the moment the answer can have changed.
    """
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        record, _captured = completed_session(cfg)
        decided = restore.plan(cfg, record.session_id, held=open_session)
    assert not open_session.still_open

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=open_session)

    assert "no longer held by this process" in excinfo.value.cause.message
    assert config.state_path("rekordbox_db", cfg).exists()


def test_a_restore_handed_an_ordinary_write_session_is_refused(cfg, held):
    record, _captured = completed_session(cfg)
    pretending = restore.Held(
        workflow=held.workflow,
        lock=held.lock,
        intent=session.Intent.WRITE,
        gates=held.gates,
        record=held.record,
    )

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, record.session_id, held=pretending)

    assert "declares itself a recovery" in excinfo.value.cause.message


def test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded(cfg, held):
    """A preview that reported convergence because it wrote nothing would lie."""
    reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    rehearsed = restore.run(decided, cfg, held=held, dry_run=True)

    assert rehearsed.outstanding
    assert not rehearsed.converged


def test_the_restore_module_names_no_verb(cfg):
    """D2. Every verb name that reaches a record arrives from the layer that owns one."""
    from cratekit.cli import registry

    source = Path(restore.__file__).read_text()
    for name in registry.VERB_NAMES:
        assert f'"{name}"' not in source
    assert restore.CAPTURE_RESTORE_WORKFLOW not in registry.VERB_NAMES
    assert restore.BARE_METAL_WORKFLOW not in registry.VERB_NAMES
