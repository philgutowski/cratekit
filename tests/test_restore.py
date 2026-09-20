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


def _close_seams(cfg) -> dict:
    """The platform seams a GATED close now needs.

    ``close_session`` asserts the volume before its convergence gate, because that
    gate was silently permissive against a library whose volume had gone. These
    fixtures live in a temporary directory whose real identity is the boot volume,
    so the seam is injected here for exactly the reason it is injected in
    ``gate_seams``: the question under test is the gate, not this machine's disks.
    """
    return {"identity_provider": matching_identity(cfg), "mount_enumerator": lambda: ()}


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


def test_an_unreconciled_restore_refuses_the_next_ordinary_session(cfg):
    acknowledge(cfg)
    _one_effect_marker(cfg)

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
    _one_effect_marker(cfg)

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
    """Flip a tree to database-native, SURVIVING the unit that adds an argument.

    The unit that ships the rebuild makes ``source`` a required keyword on
    ``record_cutover``, because a tree that cut over on a source nothing can
    re-derive was never repairable. This branch cannot spell that value, since the
    enum arrives with it, and a helper that named it unconditionally would break on
    this branch while one that omitted it breaks on the merged tree. So the
    signature is asked. This is seven of this file's tests, and it is the whole
    difference between a merge that is a rename and a merge that is a debugging
    session.
    """
    extra = {}
    if "source" in inspect.signature(tree_registry.record_cutover).parameters:
        extra["source"] = tree_registry.DerivationSource.TAXONOMY
    tree_registry.record_cutover(
        cfg, tree_id, root_id="row-1", on=date(2026, 8, 2), **extra
    )


def _tree_is_recorded_short(cfg, tree_id: str) -> bool:
    """Whether the fact landed, ASKED OF WHICHEVER STORE OWNS IT ON THIS BUILD.

    ``core.convergence`` owns tree shortness and ``core.restore`` hands the fact to
    it whenever that module is present, falling back to this unit's own record on a
    build without it. A test that named one store would therefore assert the
    OPPOSITE of the truth on the other build, and this file already carries a
    ``@requires`` guard asserting the convergence side, so naming the reconcile
    side here would put two contradictory claims about one scenario in one file.
    What is invariant across both builds is that the fact is recorded somewhere
    that gates it, which is what this asks.
    """
    if tree_id in reconcile.unconverged_trees(cfg):
        return True
    try:
        from cratekit.core import convergence  # noqa: PLC0415
    except ImportError:
        return False
    return tree_id in convergence.read(cfg).blocking_trees()


def _assert_the_next_write_is_refused_over(cfg, tree_id: str) -> None:
    """The next governed write refuses and NAMES this tree, whichever store gates it.

    The two stores refuse in different vocabularies on purpose, because they are
    different refusals: this unit's is ``restore-reconciliation-outstanding`` at
    the session gate, and the convergence unit's is ``tree-unconverged`` at the
    writer. What is invariant, and what this asserts, is that a write is refused
    and that the refusal says which tree, because that is the whole point of
    recording it. Asserting one slug would make this file claim on a merged build
    the opposite of what the ``@requires`` guard beside it claims.
    """
    if tree_id in reconcile.unconverged_trees(cfg):
        with pytest.raises(CratekitError) as excinfo:
            with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
                raise AssertionError("the gates admitted a session over a short tree")
        cause = excinfo.value.cause
        assert cause.reason == "restore-reconciliation-outstanding"
        assert cause.detail["unconverged_trees"] == [tree_id]
        return

    from cratekit.core import convergence  # noqa: PLC0415

    with pytest.raises(CratekitError) as excinfo:
        convergence.assert_converged(cfg, tree_id)
    assert excinfo.value.cause.reason == "tree-unconverged"
    assert excinfo.value.cause.detail["tree_id"] == tree_id


def test_a_restore_predating_a_cutover_marks_that_tree_unconverged(cfg, held):
    record, _captured = completed_session(cfg)
    _cut_over(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)

    assert decided.unconverged == ("routing",)
    restore.run(decided, cfg, held=held)
    assert _tree_is_recorded_short(cfg, "routing")


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
    """RESTORED after fix round 1 removed it on a premise that was false.

    Round 1 removed the tree kind from the latch, reasoning that the refusal names
    a rebuild as its remedy, that a rebuild writes through
    ``write.trees.write_tree_membership``, and that ``write_tree_membership`` has
    no ``intent`` parameter and so cannot enter these gates as anything but an
    ordinary write. The last clause was true of this branch alone and false of the
    product: the unit that builds the rebuild gives that function both a
    ``purpose`` and an ``intent`` and declares ``Intent.RECOVERY`` precisely so
    this latch cannot refuse it. Removing the latch left a pre-cutover restore
    recording a fact that nothing anywhere read, with the next destructive session
    and the next run close both allowed over a library holding a tree that is
    provably short.
    """
    acknowledge(cfg)
    reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )

    with pytest.raises(CratekitError) as sync_refusal:
        with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
            raise AssertionError("the gates admitted a session over a short tree")

    stranded = session.open_session(cfg, workflow="library-sweep")
    with pytest.raises(CratekitError) as close_refusal:
        session.close_session(stranded, cfg, **_close_seams(cfg))

    for refusal in (sync_refusal, close_refusal):
        assert refusal.value.cause.reason == "restore-reconciliation-outstanding"
        assert refusal.value.cause.code is ExitCode.UNCONVERGED
    assert "never by a decision" in close_refusal.value.cause.message
    assert close_refusal.value.cause.detail["unconverged_trees"] == ["routing"]


def test_a_pre_cutover_restore_leaves_the_next_session_refused(cfg, held):
    """The same property driven end to end rather than from a hand-written marker.

    This is the shape the verifier measured as ALLOWED after round 1: a real
    restore whose capture predates a cutover, followed by an ordinary session.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    _cut_over(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    assert decided.unconverged == ("routing",)
    assert _tree_is_recorded_short(cfg, "routing")
    _assert_the_next_write_is_refused_over(cfg, "routing")


def test_a_rebuild_can_declare_itself_and_is_not_refused_by_this_latch(cfg):
    """The premise the round-1 removal rested on, asserted in the true direction.

    A latch may not condemn its own remedy. The remedy here is a rebuild, and what
    makes the latch legitimate is that a rebuild CAN declare ``Intent.RECOVERY``
    and pass. Driven against the session gate directly, because
    ``write_tree_membership`` gains its ``intent`` parameter with the unit that
    ships the rebuild and this branch must not assert the shape of somebody else's
    signature.
    """
    acknowledge(cfg)
    reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )

    with session.assert_gates(
        cfg,
        workflow="tree-rebuild",
        intent=session.Intent.RECOVERY,
        **gate_seams(cfg),
    ) as gates:
        assert gates.intent is session.Intent.RECOVERY


def test_abandoning_a_run_is_never_gated_on_convergence(cfg):
    """Closing is the claim that the work finished; abandoning is the opposite.

    Gating both would leave somebody with a run they can neither finish nor give
    up on, and a refusal with no way past it is how people learn to edit state
    files by hand.
    """
    _one_effect_marker(cfg)
    stranded = session.open_session(cfg, workflow="library-sweep")

    ended = session.close_session(stranded, cfg, state=session.SessionState.ABANDONED)

    assert ended.state is session.SessionState.ABANDONED


def test_closing_the_effect_marker_lets_the_next_session_through(cfg):
    acknowledge(cfg)
    recorded = _one_effect_marker(cfg)
    reconcile.close_marker(
        cfg,
        recorded[0].marker.marker_id,
        disposition=reconcile.Disposition.ACCEPTED,
        actor="phillip",
    )

    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"


def test_clearing_the_tree_marker_lets_the_next_session_through(cfg):
    """RESTORED, and it means something again now that the tree kind latches.

    Fix round 1 deleted this along with the latch it exercised, so nothing
    required that a tree marker refuse anything OR that closing one lift the
    refusal. The disposition here is REPAIRED and the actor is a rebuild, which is
    the only act that legitimately closes one: this is exactly the call the unit
    that ships the rebuild makes after its convergence check reports no
    difference, so the transition path is driven rather than described. An
    ACCEPTED disposition of a tree is the softening path and is refused elsewhere.
    """
    acknowledge(cfg)
    recorded = reconcile.record_markers(
        cfg, reconcile.tree_markers(["routing"], session_id="s", capture_stamp="c")
    )
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
        session.close_session(stranded, cfg, **_close_seams(cfg)).state
        is session.SessionState.CLOSED
    )


def test_retraction_touches_the_transient_latch_and_nothing_else(cfg):
    """The retraction is for the transient fact only, never for a judgement.

    A general delete would answer every refusal this module raises by removing the
    marker that raised it, with no record that anything was outstanding. So it is
    not addressable by identifier at all: it takes no marker and discharges
    exactly one kind.
    """
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

    session.close_session(record, cfg, **_close_seams(cfg))
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


def test_free_space_that_cannot_be_read_refuses_rather_than_passing(cfg, monkeypatch):
    """ACCEPTED 4, reversed on the argument that the reviewer made and this accepts.

    The branch used to fail OPEN on the reasoning that a platform which will not
    report free space has not reported a full disk. But every supported platform
    answers ``statvfs``, so the branch is unreachable except on ``OSError``, which
    means on a path that is disappearing or unreadable underneath the question.
    Reading the one signal that something is wrong as the all-clear is what a
    capacity check exists to not do.
    """
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: None)

    with pytest.raises(CratekitError) as excinfo:
        snapshot.capture(cfg, verifier=always_verified)

    assert excinfo.value.cause.reason == "snapshot-store-full"
    assert "could not be read" in excinfo.value.cause.message


def test_the_capacity_estimate_counts_allocation_rather_than_apparent_size(cfg):
    """BLOCKING 3: a queue directory of small documents under-reported by up to 68x.

    ``review_queue`` and ``label_outcomes`` are both directories of small
    documents, and a filesystem allocates whole blocks. The apparent size of two
    thousand 120-byte documents is a quarter of a megabyte and the copy needs
    nearer ten. The estimate must be above what the copy costs, and the test asks
    the FILESYSTEM what that is rather than restating the arithmetic.
    """
    queue = config.state_path("review_queue", cfg)
    queue.mkdir(parents=True, exist_ok=True)
    for index in range(500):
        (queue / f"item-{index:05d}.json").write_bytes(b"x" * 120)

    estimate = snapshot.assert_room_for_capture(cfg, free_bytes=10**12)
    allocated = sum(
        entry.stat().st_blocks * 512 for entry in queue.iterdir() if entry.is_file()
    )

    assert estimate >= allocated, (
        "the estimate is below what the queue directory alone already occupies"
    )
    apparent = sum(entry.stat().st_size for entry in queue.iterdir() if entry.is_file())
    assert allocated > apparent * 4, "the fixture is not the shape this test is about"


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
    """Make the configured library genuinely unreachable, the way a dead disk is.

    ``mount_probe`` answers yes, which is what a genuine replacement drive is: a
    real mount point of its own. A temporary directory is not one on any platform,
    so without the seam every bare-metal test would refuse for a reason no real
    recovery meets, and the refusals this file actually drives would be
    unreachable. The seam makes the target STRICTER on nothing and looser on
    exactly one axis, which each stub test then drives directly by answering no.
    """
    shutil.rmtree(cfg.library.root, ignore_errors=True)
    return {
        "identity_provider": lambda _path: _ELSEWHERE,
        "mount_enumerator": lambda: (),
        "mount_probe": lambda _path: True,
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
    seams["mount_probe"] = lambda _path: False
    stub = Path(cfg.library.root)
    stub.mkdir(parents=True)

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=stub, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "empty folder an unmounted volume leaves behind" in excinfo.value.cause.message


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
    cfg, tmp_path, name, why
):
    """ACCEPTED 1: the equality test caught one shape of the internal disk, not three."""
    seams = _volume_is_gone(cfg)
    seams["mount_probe"] = lambda _path: False
    target = tmp_path / name
    target.mkdir(parents=True)

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "unmounted volume leaves behind" in excinfo.value.cause.message, why


def test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory(
    cfg, tmp_path
):
    """ACCEPTED 2: the glob was not recursive, so it missed the product's own layout.

    The containment rule pulls the database inside the library root and the
    default install puts it in a subdirectory, which is the layout this file's own
    fixture uses, so the non-recursive check passed on precisely the arrangement it
    exists to catch.
    """
    seams = _volume_is_gone(cfg)
    target = tmp_path / "recovered"
    (target / "db").mkdir(parents=True)
    (target / "db" / "master.db").write_bytes(b"somebody else's library")

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=target, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "named for replacement" in excinfo.value.cause.message


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
        assert open_session.workflow == "bare-metal-recovery"

    # A LITERAL above, and DISTINCT here. Three workflow labels land in one log
    # field, and both constants' docstrings say the separate label is what keeps
    # the weaker gates visible afterwards. Reading the expected value off the
    # constant leaves that claim unpinned: the label could be set equal to either
    # of the other two and the suite would stay green while the log lost the
    # distinction it exists to keep.
    assert (
        len(
            {
                restore.BARE_METAL_WORKFLOW,
                restore.CAPTURE_RESTORE_WORKFLOW,
                backup.RESTORE_WORKFLOW,
            }
        )
        == 3
    ), "two workflows that land in the same log field share a label"


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

    assert "not held by this process" in excinfo.value.cause.message
    assert config.state_path("rekordbox_db", cfg).exists()


def test_a_restore_handed_an_ordinary_write_session_is_refused(cfg, held):
    record, _captured = completed_session(cfg)
    pretending = restore.Held(
        workflow=held.workflow,
        lock=held.lock,
        intent=session.Intent.WRITE,
        issued_by=held.issued_by,
        authorises=held.authorises,
        gates=held.gates,
        record=held.record,
        token=held.token,
    )

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, record.session_id, held=pretending)

    assert "declares itself a recovery" in excinfo.value.cause.message


def test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded(cfg, held):
    """A preview that reported convergence because it wrote nothing would lie."""
    _one_effect_marker(cfg)
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


# ═══════════════════════════════════════════════════════════════════════════
# The nine blocking defects two adversarial reviews found, each driven by the
# reviewer's own reproduction. A fix with no test is a fix until somebody edits
# the file next to it.
# ═══════════════════════════════════════════════════════════════════════════


def _foreign_volume(cfg) -> dict:
    """The library is present and readable and is NOT the volume we were set up against.

    A reformatted, cloned or re-UUID'd disk. ``preflight`` calls this
    FOREIGN_VOLUME and ``restore._VOLUME_IS_GONE`` counts it as gone, which is
    what makes it the exact shape the bypass was composed from.
    """
    return {
        "identity_provider": lambda _path: _ELSEWHERE,
        "mount_enumerator": lambda: (),
        "mount_probe": lambda _path: True,
    }


def test_blocking_1_a_bare_metal_session_cannot_be_spent_on_the_library_it_refused(
    cfg, tmp_path
):
    """The whole bypass, composed exactly as the review composed it.

    With the library present and readable and its identity foreign,
    ``recovery_session`` refuses with ``library-volume-mismatch``, which is
    correct. ``bare_metal_session`` against a replacement drive then yields a
    ``Held`` whose installation-scoped lock satisfied every check ``plan`` and
    ``run`` made, and both performed every step against ``cfg.library.root``:
    the database and the whole coupled tree rewritten on the volume the identity
    gate had just refused, with no acknowledgment, with the library lock free for
    a second process, while the validated target received nothing.

    THE REFUSAL CHANGED SHAPE WITH U95 AND THE BYPASS IS STILL SHUT. ``plan`` now
    derives every path from the session, so this composition no longer refuses
    for authorising the wrong directory: it looks for the session under the
    replacement, where nothing has been recovered yet, and refuses because it is
    not there. What matters is unchanged and is what is asserted: the call
    refuses, the refusal is about the replacement and never the library, and the
    library the identity gate refused is byte for byte as it was.
    """
    record, _captured = completed_session(cfg)
    before = _tree_bytes(cfg.library.root)
    seams = _foreign_volume(cfg)
    library_seams = {
        key: value for key, value in seams.items() if key != "mount_probe"
    }

    with pytest.raises(CratekitError) as ordinary:
        with restore.recovery_session(cfg, **library_seams):
            raise AssertionError("the ordinary restore admitted a foreign volume")
    assert ordinary.value.cause.reason == "library-volume-mismatch"

    replacement = tmp_path / "replacement"
    replacement.mkdir()

    with restore.bare_metal_session(
        cfg,
        target=replacement,
        acknowledged=True,
        terminal=lambda: True,
        **seams,
    ) as bare_metal:
        assert bare_metal.issued_by is restore.Guard.BARE_METAL
        assert bare_metal.authorises == replacement
        assert not bare_metal.authorises_path(cfg.library.root)

        with pytest.raises(CratekitError) as refused:
            restore.plan(cfg, record.session_id, held=bare_metal)

    cause = refused.value.cause
    assert "no session is recorded" in cause.message
    assert str(replacement) in cause.message
    assert str(cfg.library.root) not in cause.message
    assert _tree_bytes(cfg.library.root) == before
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )


# ═══════════════════════════════════════════════════════════════════════════
# U95: every path comes from the directory the session authorises
# ═══════════════════════════════════════════════════════════════════════════


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
    """Stand in for the mirror pull: the dead library's contents, on the new drive.

    A plain copy, so every manifest and every session record on the replacement
    still names the configured root in absolute paths, which is exactly what a
    real recovery would find and is the case the re-basing exists for.
    """
    shutil.copytree(cfg.library.root, replacement)
    return replacement


def _bare_metal(cfg, replacement: Path):
    return restore.bare_metal_session(
        cfg,
        target=replacement,
        acknowledged=True,
        replacing_existing=True,
        terminal=lambda: True,
        **_foreign_volume(cfg),
    )


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
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")
    write_state(cfg, "label_watermarks", {"source": "after"})
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
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
    assert recovered_db.read_bytes() == b"database, generation one"
    recovered_marks = replacement / config.state_path("label_watermarks", cfg).relative_to(
        cfg.library.root
    )
    assert json.loads(recovered_marks.read_bytes()) == {"source": "before"}
    assert _tree_bytes(cfg.library.root) == library_before


def test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else(cfg, tmp_path):
    """Same steps, same order, same relative positions: only the root differs."""
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, captured = completed_session(cfg)
    replacement = _recovered_onto(cfg, tmp_path / "replacement")

    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as library_session:
        at_home = restore.plan(cfg, record.session_id, held=library_session)
    with _bare_metal(cfg, replacement) as bare_metal:
        moved = restore.plan(cfg, record.session_id, held=bare_metal)

    moved_capture = replacement / captured.root.relative_to(cfg.library.root)
    assert _rendered(moved, library=replacement, capture=moved_capture) == _rendered(
        at_home, library=cfg.library.root, capture=captured.root
    )


def test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds(
    cfg, tmp_path
):
    """The session record made it across and the capture did not.

    The capture is sitting right there at the configured root, readable, and
    taking it would be the bypass run in the other direction: bytes from a volume
    the identity gate refused, written onto the replacement. It refuses, and the
    refusal names the replacement's store.
    """
    record, captured = completed_session(cfg)
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    moved_capture = replacement / captured.root.relative_to(cfg.library.root)
    shutil.rmtree(moved_capture)
    library_before = _tree_bytes(cfg.library.root)
    replacement_before = _tree_bytes(replacement)

    with _bare_metal(cfg, replacement) as bare_metal:
        with pytest.raises(CratekitError) as refused:
            restore.plan(cfg, record.session_id, held=bare_metal)

    assert not moved_capture.exists() and captured.root.is_dir()
    assert str(replacement) in refused.value.cause.message
    assert str(cfg.library.root) not in refused.value.cause.message
    assert _tree_bytes(cfg.library.root) == library_before
    assert _tree_bytes(replacement) == replacement_before


def test_u95_a_live_recovery_session_plan_is_unchanged_by_golden(cfg, held):
    """The library path is pinned, so the re-rooting cannot leak into it.

    The literal below was produced by ``main`` before U95 and is reproduced by
    this branch. ``_rooted`` handing back the SAME OBJECT is the stronger half:
    there is no second configuration for a library session to drift towards.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, captured = completed_session(cfg)

    assert restore._rooted(cfg, held) is cfg
    assert restore._rebased(captured.root, cfg, held) == captured.root
    manifest = snapshot.read_manifest(captured.root)
    assert restore._rebased_capture(manifest, cfg, held) is manifest

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
    cfg, tmp_path
):
    """A plan is a value, and its targets were fixed when it was built."""
    record, _captured = completed_session(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as library_session:
        for_the_library = restore.plan(cfg, record.session_id, held=library_session)
    library_before = _tree_bytes(cfg.library.root)
    replacement_before = _tree_bytes(replacement)

    with _bare_metal(cfg, replacement) as bare_metal:
        for dry_run in (True, False):
            with pytest.raises(CratekitError) as refused:
                restore.run(for_the_library, cfg, held=bare_metal, dry_run=dry_run)
            cause = refused.value.cause
            assert "authorises" in cause.message
            assert cause.detail["authorises"] == str(replacement)
            assert _under(cause.detail["writing"], cfg.library.root)

    assert _tree_bytes(cfg.library.root) == library_before
    assert _tree_bytes(replacement) == replacement_before


def test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session(cfg, tmp_path):
    record, _captured = completed_session(cfg)
    replacement = _recovered_onto(cfg, tmp_path / "replacement")
    with _bare_metal(cfg, replacement) as bare_metal:
        for_the_target = restore.plan(cfg, record.session_id, held=bare_metal)
    replacement_before = _tree_bytes(replacement)

    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as library_session:
        # Compared INSIDE the block, because opening and closing a library session
        # writes its own record, which is not what is under test.
        inside = _tree_bytes(cfg.library.root)
        with pytest.raises(CratekitError) as refused:
            restore.run(for_the_target, cfg, held=library_session)
        assert _tree_bytes(cfg.library.root) == inside

    cause = refused.value.cause
    assert "authorises" in cause.message
    assert cause.detail["authorises"] == str(cfg.library.root)
    assert _under(cause.detail["writing"], replacement)
    assert _tree_bytes(replacement) == replacement_before


def test_u95_a_library_session_still_refuses_a_configuration_for_another_library(
    cfg, held, tmp_path
):
    """The re-rooting is for the bare-metal guard alone.

    A library session passed its gates against ONE configured library. Handing
    ``plan`` a configuration naming another must refuse, as it always did, rather
    than be quietly re-aimed at the directory the session authorises.
    """
    record, _captured = completed_session(cfg)
    other = tmp_path / "another-library"
    (other / "db").mkdir(parents=True)
    elsewhere = dataclasses.replace(
        cfg,
        library=dataclasses.replace(
            cfg.library, root=other, db_path=other / "db" / "master.db"
        ),
    )

    with pytest.raises(CratekitError) as refused:
        restore.plan(elsewhere, record.session_id, held=held)

    cause = refused.value.cause
    assert "authorises" in cause.message
    assert cause.detail["writing"] == str(other)
    assert cause.detail["authorises"] == str(cfg.library.root)


def test_u95_a_database_outside_the_library_is_not_carried_onto_the_target(cfg, tmp_path):
    """The acknowledged layout: the database was never under the library root.

    It is not relative to the library, so there is no position to carry it to,
    and it sits outside the one directory this session authorises. The plan
    refuses naming it rather than writing a database somewhere nobody validated.
    """
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
        assert restore._rooted(apart, bare_metal).library.db_path == outside
        with pytest.raises(CratekitError) as refused:
            restore.plan(apart, record.session_id, held=bare_metal)

    cause = refused.value.cause
    assert "authorises" in cause.message
    assert _under(cause.detail["writing"], outside.parent)
    assert outside.read_bytes() == b"a database outside the library"
    assert _tree_bytes(replacement) == replacement_before


def test_u95_the_staging_directory_is_a_write_location_and_is_authorised_too(
    cfg, held, tmp_path
):
    """Companions are RENAMED into it, and it is not a step target.

    So the per-step check never saw it. A plan whose staging directory has been
    aimed outside the session refuses, in both modes, before any log is moved.
    """
    record, _captured = completed_session(cfg)
    database = config.state_path("rekordbox_db", cfg)
    log = database.with_name(database.name + "-wal")
    log.write_bytes(b"transactions no capture holds")
    decided = restore.plan(cfg, record.session_id, held=held)
    stray = tmp_path / "not-the-library" / "staged"
    aimed_away = dataclasses.replace(decided, pre_restore_root=stray)

    for dry_run in (True, False):
        with pytest.raises(CratekitError) as refused:
            restore.run(aimed_away, cfg, held=held, dry_run=dry_run)
        assert refused.value.cause.detail["writing"] == str(stray)

    assert log.read_bytes() == b"transactions no capture holds"
    assert not stray.exists()


def test_u95_a_recorded_path_outside_the_configured_root_is_not_moved(cfg, tmp_path):
    """Re-basing answers "where under the library was this", and only that."""
    replacement = tmp_path / "replacement"
    replacement.mkdir()
    stranger = tmp_path / "somewhere" / "else.db"

    with _bare_metal(cfg, replacement) as bare_metal:
        assert restore._rebased(stranger, cfg, bare_metal) == stranger
        assert restore._rebased(cfg.library.root, cfg, bare_metal) == replacement
        assert restore._rebased(
            cfg.library.root / "db" / "master.db", cfg, bare_metal
        ) == replacement / "db" / "master.db"
        rooted = restore._rooted(cfg, bare_metal)

    assert rooted.library.root == replacement
    assert rooted.library.db_path == replacement / "db" / "master.db"
    assert rooted.library.volume_id == cfg.library.volume_id
    assert cfg.library.root != replacement


def test_blocking_1_a_held_naming_an_unrelated_lock_this_process_holds_is_refused(
    cfg, tmp_path
):
    """ACCEPTED 3: lock membership is a set of paths, so any lock at all satisfied it.

    The token answers the question the lock cannot: was this value issued by one
    of this module's own guards, and is that guard still inside its block.
    """
    record, _captured = completed_session(cfg)
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

        with pytest.raises(CratekitError) as excinfo:
            restore.plan(cfg, record.session_id, held=forged)

    assert "not held by this process" in excinfo.value.cause.message


def test_blocking_1_a_token_is_withdrawn_when_its_guard_returns(cfg):
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        assert open_session.token is not None
        assert id(open_session.token) in restore._ISSUED
    assert id(open_session.token) not in restore._ISSUED


def _wal_path(cfg) -> Path:
    """The live write-ahead log, resolved through the inventory rather than spelled."""
    database = config.state_path("rekordbox_db", cfg)
    companions = config.sidecar_paths("rekordbox_db", cfg)
    return next(path for path in companions if path.name.startswith(database.name))


def test_blocking_2_a_capture_whose_database_is_gone_refuses_before_the_log_is_touched(
    cfg, held
):
    """The reviewer's exact sequence, and the bytes that used to be unrecoverable.

    The live log holds transactions committed since the last checkpoint. None of
    them is in the main file and none of them is in ANY capture, because every
    capture predates them. The plan was CLEAR log, CLEAR index, REPLACE database;
    the CLEAR was ``unlink`` with no staging and no backup, and
    ``assert_verified`` read a verdict out of the manifest without asking whether
    the bytes it was about were still there. So a capture whose database had gone
    planned and rehearsed clean, and the real run unlinked the log and raised.
    """
    record, captured = completed_session(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")
    log = _wal_path(cfg)
    log.write_bytes(b"committed transactions the main file does not hold")
    captured.database.unlink()

    with pytest.raises(CratekitError) as excinfo:
        restore.plan(cfg, record.session_id, held=held)

    assert excinfo.value.cause.reason == "snapshot-integrity-failed"
    assert "no longer on disk" in excinfo.value.cause.message
    assert log.read_bytes() == b"committed transactions the main file does not hold"


def test_blocking_2_the_live_log_is_moved_aside_rather_than_deleted(cfg, held):
    """Even on the SUCCESS path, because the bytes postdate every capture.

    A restore that succeeds is still discarding the only copy of every
    transaction committed since the last checkpoint. Deleting them is a decision
    the restore is not entitled to make on the user's behalf.
    """
    record, _captured = completed_session(cfg)
    log = _wal_path(cfg)
    log.write_bytes(b"committed transactions the main file does not hold")

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    assert not log.exists(), "the engine must not find a log beside a replaced database"
    kept = decided.pre_restore_root / log.name
    assert kept.read_bytes() == b"committed transactions the main file does not hold"


def test_blocking_2_a_failure_mid_restore_is_a_structured_refusal(cfg, held, monkeypatch):
    """A raw OSError carries no reason, no remedy, and no reserved exit code.

    The window opens on a full volume, a permission error or an I/O error, which
    is exactly the set of conditions under which people restore.
    """
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    def _explode(_source, _target):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(restore, "_replace_file", _explode)

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held)

    cause = excinfo.value.cause
    assert cause.reason == "restore-step-failed"
    assert cause.code is ExitCode.PRECONDITION
    assert cause.remediation.steps
    # The latch written first is still standing, which is the whole point of
    # writing it first.
    assert decided.latch.marker_id in [
        r.marker.marker_id for r in reconcile.outstanding(cfg)
    ]


def test_blocking_2_a_restore_checks_the_library_volume_has_room_for_the_copy(cfg, held):
    """One call site, inside ``capture``, so a restore checked nothing at all."""
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

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
    """Scenario A: the second restore's markers used to be dropped by ``setdefault``.

    A different window, over an entirely different set of orphaned files,
    producing the same kind, identity and effect. The store could not represent
    two, so ``outstanding()`` returned empty, ``assert_converged`` passed, and the
    audio the second restore discarded was owned by nobody with no one told.
    """
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
    """Scenario B, which survives the correct remedy being carried out.

    One rebuild used to close the tree forever: a later pre-cutover restore of the
    same tree derived the marker correctly and had it swallowed by the closed
    record of the first, so ``unconverged_trees()`` returned empty and an
    incremental sync structurally could not see the gap.
    """
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
    """The property the original identifier was built for, kept.

    The old test passed the SAME session and stamp on both calls, which is why it
    could only ever prove this half.
    """
    markers = reconcile.tree_markers(["routing"], session_id="run-1", capture_stamp="c")
    reconcile.record_markers(cfg, markers)
    recorded = reconcile.record_markers(cfg, markers)

    assert len(recorded) == 1


def test_blocking_5_an_interrupted_restore_in_a_none_effect_window_latches(cfg, held):
    """Seven of the twelve coupled entries declare ``RollbackEffect.NONE``.

    A restore whose window touched only those wrote nothing anywhere before it
    started replacing files, so a hard kill after ``replace-file`` left the
    database rolled back, the coupled state at the later generation, an empty
    reconciliation store, and ``assert_gates(intent=WRITE)`` ALLOWED. The only
    trace was a non-terminal session record nothing consults.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    assert decided.markers == (), "this fixture must have no effect markers at all"
    assert decided.steps[0].act is restore.Act.RECORD
    assert decided.steps[-1].act is restore.Act.RELEASE

    # Perform everything except the last step, which is the interruption.
    for step in decided.steps[:-1]:
        restore._perform(step, decided, cfg)

    with pytest.raises(CratekitError) as excinfo:
        with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)):
            raise AssertionError("the gates admitted a session after a half restore")

    assert excinfo.value.cause.reason == "restore-reconciliation-outstanding"
    assert "never seen to finish" in excinfo.value.cause.message


def test_blocking_5_a_restore_that_completes_retracts_its_own_latch(cfg):
    acknowledge(cfg)
    record, _captured = completed_session(cfg)

    with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
        decided = restore.plan(cfg, record.session_id, held=open_session)
        outcome = restore.run(decided, cfg, held=open_session)

    assert outcome.outstanding == ()
    assert outcome.converged
    # Asked OUTSIDE the recovery session, because the library lock does not nest
    # and the question is whether the NEXT ordinary session is admitted.
    with session.assert_gates(cfg, workflow="library-sweep", **gate_seams(cfg)) as gates:
        assert gates.workflow == "library-sweep"


def test_blocking_5_a_rehearsal_does_not_latch_anything(cfg, held):
    """A rehearsal performs nothing at all, including the latch."""
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    restore.run(decided, cfg, held=held, dry_run=True)

    assert reconcile.records(cfg) == ()


def test_blocking_6_a_second_attempt_never_deletes_the_only_surviving_copy(
    cfg, tmp_path
):
    """The crash state, then a capture that cannot be read, then the second run.

    ``_replace_directory`` began by removing both working names unconditionally.
    After a crash between the two renames ``coupled`` is absent and
    ``coupled.replaced`` holds the ONLY copy of the live pre-restore state, so a
    second run destroyed it before ``copytree`` and then failed, leaving the live
    directory absent, the old state gone, and a partial new one under
    ``.restoring``. The work the abandoned restore did existed nowhere.
    """
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
    """The dry run used to compare the loop's output to the loop's input.

    ``rehearsed.performed == plan.steps == real.performed`` can never fail,
    whatever ``_perform`` would have done, because everything a step depends on
    lives inside ``_perform``, which a rehearsal skips wholesale. Measured: a
    REPLACE whose source had been deleted rehearsed as six steps performed with
    no refusal.
    """
    record, captured = completed_session(cfg)
    write_state(cfg, "label_watermarks", {"source": "x"})
    decided = restore.plan(cfg, record.session_id, held=held)

    replacement = next(
        step for step in decided.steps if step.act is restore.Act.REPLACE
    )
    replacement.source.unlink()

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert excinfo.value.cause.reason == "snapshot-integrity-failed"
    assert str(captured.root) in str(excinfo.value.cause.detail)


def test_the_rehearsal_refuses_a_target_directory_nobody_can_write_to(cfg, held):
    """The other case the empty rehearsal reported clean."""
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    database_dir = config.state_path("rekordbox_db", cfg).parent
    database_dir.chmod(0o500)

    try:
        with pytest.raises(CratekitError) as excinfo:
            restore.run(decided, cfg, held=held, dry_run=True)
    finally:
        database_dir.chmod(0o700)

    assert excinfo.value.cause.reason == "restore-step-failed"
    assert "not writable" in excinfo.value.cause.message


def test_a_plan_built_before_a_later_commit_is_refused_at_run(cfg, held):
    """ACCEPTED 5: ``run`` re-validated nothing about the plan it was handed.

    So a plan built before a later session committed executed unchanged and
    discarded it, while a freshly built plan refused with
    ``restore-discards-committed-work``. A plan is a value and the log is not.
    """
    record, _captured = completed_session(cfg, started="2026-08-01T00:00:00+00:00")
    decided = restore.plan(cfg, record.session_id, held=held)

    completed_session(cfg, started="2026-08-03T00:00:00+00:00", stamp="later-capture")

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held)

    assert excinfo.value.cause.reason == "restore-discards-committed-work"
    assert config.state_path("rekordbox_db", cfg).exists()


def test_a_reconciliation_store_on_an_unmounted_volume_is_not_an_empty_one(cfg):
    """ACCEPTED: ``close_session``'s gate takes no volume assertion.

    So with the library volume unmounted the document's path simply did not
    exist, ``_read`` returned an empty store, and the latch passed silently. All
    four readers are asked through one function, so all four still answer alike.
    """
    stranded = session.open_session(cfg, workflow="library-sweep")
    shutil.rmtree(cfg.library.root)

    for reader in (reconcile.records, reconcile.outstanding, reconcile.converged):
        with pytest.raises(CratekitError) as excinfo:
            reader(cfg)
        assert excinfo.value.cause.reason == "restore-record-unusable"

    with pytest.raises(CratekitError):
        session.close_session(stranded, cfg)


def test_a_same_length_edit_inside_a_coupled_directory_still_marks(cfg, held):
    """ACCEPTED: the digest compared names and sizes, so the failure was under-marking.

    ``label_outcomes`` is a directory of small documents AND the one COUPLED
    directory entry carrying a declared out-of-band effect, so the one place a
    same-length edit is most likely is the one place missing it costs a marker.
    """
    outcomes = config.state_path("label_outcomes", cfg)
    outcomes.mkdir(parents=True, exist_ok=True)
    (outcomes / "label-a.json").write_bytes(b'{"taken": "aaaa"}')
    record, _captured = completed_session(cfg)
    (outcomes / "label-a.json").write_bytes(b'{"taken": "bbbb"}')

    decided = restore.plan(cfg, record.session_id, held=held)

    assert "label_outcomes" in [marker.identity for marker in decided.markers]


def test_pruning_with_no_session_named_asks_the_log_instead_of_skipping(cfg):
    """ACCEPTED: the guard was opt-in and the default was to opt out.

    ``owning=None`` is the easy call shape to write and was the one that checked
    nothing.
    """
    session.open_session(cfg, workflow="library-sweep")

    with pytest.raises(CratekitError) as excinfo:
        restore.prune(cfg)

    assert "not reached a terminal state" in excinfo.value.cause.message


def test_the_tree_shortness_handoff_calls_the_module_that_owns_the_gate(
    cfg, held, monkeypatch
):
    """BLOCKING 8: two modules recorded one fact and neither referenced the other.

    A successful rebuild cleared ``core.convergence``'s flag and left this unit's
    marker standing, so every destructive session kept refusing after the remedy
    had been carried out correctly. ``core.convergence`` owns the fact now; this
    asserts the handoff is made with the arguments U36's own signature declares,
    against that module when it is present.

    IT PATCHES THE OWNING MODULE'S FUNCTION, which is R-21 item 6 and is what the
    U36 merge owed. While the two modules were apart this reached for a private
    helper on ``restore`` that resolved the import at call time; item 3 deleted
    that helper, and a test patching an attribute that no longer exists raises
    ``AttributeError`` at setup rather than reporting anything about the handoff.
    Patching the real function is also the stronger assertion: it fails if the
    signature U36 declares and the call this module makes ever come apart.
    """
    calls: list[tuple] = []

    def _mark(configuration, tree_ids, *, reason, now=None):
        calls.append((configuration, tuple(tree_ids), reason))

    monkeypatch.setattr(convergence, "mark_unconverged", _mark)

    record, _captured = completed_session(cfg)
    _cut_over(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    # The reason is a LITERAL. It is the vocabulary the OWNING module records
    # reasons in, so its value is the whole point of naming it once, and an
    # expected value read back off the constant that produced it passes at every
    # value the constant can take.
    assert calls == [(cfg, ("routing",), "restore-predates-cutover")]
    assert restore.PRE_CUTOVER_RESTORE == "restore-predates-cutover"
    assert reconcile.unconverged_trees(cfg) == (), (
        "the fact was recorded twice, which is the duplication this fixes"
    )


def test_the_tree_mark_happens_after_the_coupled_state_is_replaced(cfg, held):
    """The record that holds tree shortness is itself a COUPLED entry.

    Marking before the replacement would write the mark and then overwrite it.
    """
    record, _captured = completed_session(cfg)
    _cut_over(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    acts = [step.act for step in decided.steps]

    assert acts.index(restore.Act.MARK_TREES) > acts.index(restore.Act.REPLACE)
    assert acts.index(restore.Act.MARK_TREES) < acts.index(restore.Act.RELEASE)


# ═══════════════════════════════════════════════════════════════════════════
# The register entry this unit owns, gating a real guard, plus the obligation
# that no longer has a register entry to hang on.
#
# An entry in tests/_pending.py that no @requires cites gates NO test: it is an
# unenforced countdown wearing the costume of an enforced one, and this unit
# shipped two of them. The one still pending is cited below with its full
# assertion body, so the moment U27 lands it runs and has to pass.
#
# THE OTHER ONE'S UNIT LANDED. U36 shipped cratekit.write.rebuild on `main` in
# this session and issue #36 closed, so its register entry had to go: a register
# owing a closed unit a module is what scripts/board.py audit exits 2 on, and the
# obligation on it was owned by nobody the moment #36 closed. What replaces it is
# below, and it needs no register key at all, which is the point.
# ═══════════════════════════════════════════════════════════════════════════


def test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build():
    """The countdown that survived its own register entry being deleted.

    ``restore._hand_tree_shortness_over`` resolves ``core.convergence`` AT CALL
    TIME and falls back to recording tree shortness in this unit's own store,
    because ``core.convergence`` is not in this build and a module-level import of
    a module that does not exist is a breakage rather than a handoff. On a tree
    where both modules are present that fallback is dead weight recording a fact a
    rebuild does not clear, which is precisely how the two answers came apart in
    the first place.

    IT IS ASSERTED WITHOUT A SKIP AND WITHOUT A REGISTER KEY. The obligation used
    to ride on ``@requires("cratekit.write.rebuild")``, which stopped working in
    both directions at once when U36 landed: the register entry became a
    ``board.py`` contradiction, and the guard behind it would have gone live on a
    tree where the fallback was still there. A test that asks what THIS BUILD
    contains and asserts the right thing for it has neither problem. It passes
    here, where the fallback is correct and load bearing, and it fails on the
    first tree that holds both modules with the fallback still in place, naming
    the three deletions. That is R-21 item 3 in ``docs/residual-findings.md``,
    made self-announcing rather than left on a checklist.
    """
    import importlib.util  # noqa: PLC0415

    source = Path(inspect.getfile(restore)).read_text(encoding="utf-8")
    try:
        landed = importlib.util.find_spec("cratekit.core.convergence") is not None
    except ModuleNotFoundError:
        landed = False

    if not landed:
        # The fallback is the correct shape for this build, so assert it is there
        # and that it is LATCHED rather than merely written down. An earlier round
        # recorded the fact without latching it and the result was a fact nothing
        # read.
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
    """The wiring this unit proved at the seam and could not call.

    The shape being prevented is specific and was found by review: a plan that
    takes the lock and gives it back, followed by a run that takes it again,
    leaves a window in which a second process passes the same gates and commits,
    after which the run copies a snapshot over a commit its plan was built
    before. ``backup.plan_restore`` and ``backup.run_restore`` each default to
    acquiring their own, so the verb must pass the already-open guard in as
    ``gates``.
    """
    import cratekit.session.restore_cli as restore_cli  # noqa: PLC0415

    source = Path(restore_cli.__file__).read_text()
    assert "recovery_session" in source, (
        "the restore verbs do not enter the one session that spans the whole verb"
    )
    assert re.search(r"gates\s*=\s*\w+\.guard", source), (
        "the off-machine restore is not handed the already-open guard, so it takes "
        "the library lock a second time and leaves a window a commit fits in"
    )
    assert "assert_gates" not in source, (
        "the verb enters the destructive-session gates itself rather than through "
        "recovery_session, which is how the two acquisitions come back"
    )


# ═══════════════════════════════════════════════════════════════════════════
# Fix round 2: what the first round's fixes broke, each driven by the
# verifier's own reproduction. A fix round fails by being too restrictive or by
# relocating a hole rather than closing it, and all of these were one of those.
# ═══════════════════════════════════════════════════════════════════════════


def test_round2_a_completed_restore_discharges_an_earlier_interrupted_one(cfg):
    """The latch's own printed remedy was one it could not discharge.

    Restore 1 interrupted after RECORD; restore 2 run to completion successfully.
    The latch keyed on the restore's OWN recovery session, and RELEASE retracted
    only its own row, so restore 1's latch stood, the outcome reported itself
    unconverged, and the next ordinary session refused with
    ``remedy=restore-from-snapshot`` and the text "an unfinished restore is closed
    by finishing one". It was not.
    """
    acknowledge(cfg)
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


def test_round2_repeating_a_failing_restore_does_not_accumulate_latches(cfg):
    """The product's own printed step is "run the restore again, it is safe to repeat".

    Following it produced a second permanent row every time, because the latch
    keyed on a recovery session identifier that is new on every attempt. Two
    attempts of one restore are one restore, and what identifies a restore is the
    capture it is putting back.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)

    for _attempt in range(3):
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            decided = restore.plan(cfg, record.session_id, held=open_session)
            restore._perform(decided.steps[0], decided, cfg)

    open_records = reconcile.outstanding(cfg)
    assert len(open_records) == 1, [r.marker.marker_id for r in open_records]
    assert open_records[0].marker.identity == _captured_stamp(cfg, record)


def _captured_stamp(cfg, record) -> str:
    return snapshot.read_manifest(restore.capture_root_of(record.snapshot_path)).stamp


def test_round2_three_attempts_stage_their_logs_side_by_side(cfg):
    """The latch collapses across attempts and the staged bytes must NOT.

    The second attempt's write-ahead log is not the first attempt's, and writing
    one over the other destroys the very bytes the staging exists to keep.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    roots = set()

    for attempt in range(3):
        log = _wal_path(cfg)
        log.write_bytes(f"attempt {attempt}".encode())
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
    """The rule must not refuse a restore the volume can genuinely hold.

    Round 1 demanded ``1.10 * sum(every captured source)``, which refused a
    restore whose real high-water mark was a third of that, on exactly the volume
    state a person restores from. This is the P7 half of the capacity rule: run it
    against correct behaviour too.
    """
    _build_capacity_shape(cfg, database=8, wal=4, items=2000)
    record, _captured = completed_session(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    estimate = restore.space_peak_bytes(decided)
    summed = sum(
        snapshot.incoming_bytes(entry.source)
        for entry in snapshot.read_manifest(decided.capture_root).sources
        if entry.captured is not None
    )

    assert estimate < summed, "the estimate is no better than summing everything"
    outcome = restore.run(decided, cfg, held=held)
    assert outcome.converged


def _build_capacity_shape(cfg, *, database: int, wal: int, items: int) -> None:
    """One of the shapes the capacity rule was measured against. Sizes in MiB."""
    config.state_path("rekordbox_db", cfg).write_bytes(b"d" * (database * 1024 * 1024))
    _wal_path(cfg).write_bytes(b"w" * (wal * 1024 * 1024))
    queue = config.state_path("review_queue", cfg)
    queue.mkdir(parents=True, exist_ok=True)
    for index in range(items):
        (queue / f"item-{index:05d}.json").write_bytes(b"x" * 120)


def _allocated_tree(root: Path) -> int:
    """Blocks occupied under ``root``, the way a filesystem counts them."""
    total = 0
    for current, _directories, files in os.walk(root):
        here = Path(current)
        for name in files:
            try:
                total += here.joinpath(name).stat().st_blocks * 512
            except OSError:
                continue
    return total


class _PeakSampler:
    """Samples occupied blocks around every primitive a restore uses to move bytes.

    THE PEAK IS INSIDE A STEP, NOT BETWEEN STEPS, which is why this wraps the
    primitives rather than ``_perform``. A replacement holds the old copy and the
    staged new one at the same time, and that overlap IS the high-water mark; a
    sampler that only looked before and after each step would miss precisely the
    quantity the capacity rule exists to bound.
    """

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
        ({"database": 8, "wal": 4, "items": 2000}, False),
        ({"database": 8, "wal": 4, "items": 2000}, True),
        ({"database": 1, "wal": 8, "items": 2000}, False),
    ],
)
def test_round3_the_capacity_estimate_is_above_the_measured_peak(
    cfg, held, monkeypatch, shape, wipe_live
):
    """BLOCKING 1: the single-step rule was a false ACCEPTANCE, measured four ways.

    Two kinds of step grow the library PERMANENTLY, so every later step starts
    from a higher floor and the maximum of one step cannot see it. A ``CLEAR`` is
    a rename, so the live log keeps its blocks under another name forever and the
    ``REPLACE`` that follows frees nothing; and any target that is not there live
    frees nothing either. On a real 64 MiB volume squeezed to just above what the
    rule demanded, the preflight passed and the restore died inside the coupled
    copy with ENOSPC, leaving the database restored and the coupled state not.

    The estimate is compared against a peak MEASURED by sampling occupied blocks
    around every rename and copy the run makes, rather than against arithmetic
    restated from the implementation, because restating it would agree with a
    wrong implementation exactly as readily as with a right one.
    """
    _build_capacity_shape(cfg, **shape)
    record, _captured = completed_session(cfg)
    if wipe_live:
        shutil.rmtree(config.library_coupled_dir(cfg), ignore_errors=True)
        config.state_path("rekordbox_db", cfg).unlink()

    decided = restore.plan(cfg, record.session_id, held=held)
    estimate = restore.space_peak_bytes(decided)

    sampler = _PeakSampler(Path(cfg.library.root))
    sampler.install(monkeypatch)
    restore.run(decided, cfg, held=held)

    assert estimate >= sampler.peak, (
        f"the estimate {estimate} is BELOW the measured high-water mark "
        f"{sampler.peak}, so a volume between the two passes the preflight and "
        f"dies part way through the restore"
    )


def test_round3_a_volume_between_the_two_rules_is_refused(cfg, held, monkeypatch):
    """The gap the single-step rule opened, driven directly.

    Free space above what that rule demanded and below the real high-water mark is
    exactly the band in which the preflight passed and the restore ran out of room
    with the two halves at different generations.

    The seam is taken through the ``monkeypatch`` fixture rather than by assigning
    to the module and restoring in a ``finally``: an assignment is undone only by
    the block that made it, so a rewrite that moves an assertion above the
    ``try`` leaks a stubbed free-space probe into every test that runs after it in
    the same process, and a suite whose capacity probe is a lambda is green for
    the wrong reason.
    """
    _build_capacity_shape(cfg, database=8, wal=4, items=2000)
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    largest_single = max(
        snapshot.incoming_bytes(step.source)
        for step in decided.steps
        if step.act in (restore.Act.REPLACE, restore.Act.REPLACE_TREE)
    )
    estimate = restore.space_peak_bytes(decided)
    assert estimate > largest_single, "the estimate is still one step's worth"

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: int(largest_single * 1.2))
    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert excinfo.value.cause.reason == "snapshot-store-full"
    assert config.state_path("rekordbox_db", cfg).read_bytes()[:1] == b"d"


def test_round3_a_staged_log_is_counted_as_permanent_growth(cfg, held):
    """The specific blindness: a CLEAR is a rename and the REPLACE frees nothing.

    The estimate must be at least the restored companion's captured size on top of
    whatever the rest of the plan needs, because those blocks are never given back.
    """
    _build_capacity_shape(cfg, database=1, wal=8, items=10)
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    staged = {step.target for step in decided.steps if step.act is restore.Act.CLEAR}
    companions = sum(
        snapshot.incoming_bytes(step.source)
        for step in decided.steps
        if step.act is restore.Act.REPLACE and step.target in staged
    )
    assert companions > 0, "this fixture writes no companion back"
    assert restore.space_peak_bytes(decided) >= companions


def test_round2_the_restore_capacity_refusal_names_the_library_volume(
    cfg, held, monkeypatch
):
    """The refusal reused the capture message and sent people to prune captures.

    The captures may be on another volume entirely, which this unit computes and
    the retention plan carries.

    The seam is taken through ``monkeypatch`` for the reason spelled out at the
    round 3 test above: an assignment restored in a ``finally`` is undone only by
    the block that made it, so a later rewrite that moves an assertion above the
    ``try`` leaks a stubbed free-space probe into every test that runs after it in
    the same process. This was the last direct assignment of the eight sites, and
    leaving one instance of a pattern the file condemns forty lines earlier is how
    the pattern comes back.
    """
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 1)
    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert excinfo.value.cause.reason == "snapshot-store-full"
    assert "LIBRARY volume" in " ".join(excinfo.value.cause.remediation.steps)


def test_round2_a_pre_cutover_restore_is_gated_rather_than_merely_recorded(cfg, held):
    """Round 1 relocated this hole rather than closing it.

    ``LATCHING_KINDS`` dropped the tree kind and the fallback still recorded into
    this unit's own store, so on a build without ``core.convergence`` the fact was
    written down and read by nothing at all.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    _cut_over(cfg)

    decided = restore.plan(cfg, record.session_id, held=held)
    restore.run(decided, cfg, held=held)

    assert reconcile.Kind.UNCONVERGED_TREE in reconcile.LATCHING_KINDS, (
        "the tree kind must stay in the latching set: the unit that ships the "
        "rebuild DERIVES its own exemption from this set by subtracting that one "
        "member by name, so removing it here silently widens what that unit holds"
    )
    assert _tree_is_recorded_short(cfg, "routing")
    _assert_the_next_write_is_refused_over(cfg, "routing")


def test_round2_a_successful_restore_over_an_unremovable_old_copy_still_succeeds(
    cfg, held
):
    """A restore that landed correctly reported failure and latched the library.

    ``_replace_directory`` removes the old copy AFTER the swap. An unwritable
    subtree inside a coupled directory is invisible to a check that probes only
    the top of each target, so the swap landed, the rmtree raised, RELEASE was
    never reached, and the latch became permanent. That fed straight into the
    latch that a repeat could not discharge.
    """
    acknowledge(cfg)
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


def test_round2_a_directory_replacement_checks_its_parent_not_itself(cfg, held):
    """``_replace_directory`` writes in the target's PARENT and renames the target.

    Probing the target answered a question nobody was asking and let a genuinely
    unwritable parent through.
    """
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    coupled_parent = config.library_coupled_dir(cfg).parent
    coupled_parent.chmod(0o500)

    try:
        with pytest.raises(CratekitError) as excinfo:
            restore.run(decided, cfg, held=held, dry_run=True)
    finally:
        coupled_parent.chmod(0o700)

    assert excinfo.value.cause.reason == "restore-step-failed"
    assert str(coupled_parent) in excinfo.value.cause.message


def test_round2_a_held_rebuilt_around_a_live_token_is_refused(cfg, tmp_path):
    """RESIDUAL 6: the discriminator narrowed the bypass rather than closing it.

    ``Held`` is exported, is a plain frozen dataclass, and carries its token in a
    public field, so inside a ``bare_metal_session`` a caller could read the real
    token off the value the guard yielded and rebuild a ``Held`` around it claiming
    a different guard and a different authorised directory. Every check passed,
    because the only question asked was whether the token was live.
    """
    record, _captured = completed_session(cfg)
    seams = _foreign_volume(cfg)
    replacement = tmp_path / "replacement"
    replacement.mkdir()

    with restore.bare_metal_session(
        cfg, target=replacement, acknowledged=True, terminal=lambda: True, **seams
    ) as bare_metal:
        laundered = restore.Held(
            workflow=restore.CAPTURE_RESTORE_WORKFLOW,
            lock=bare_metal.lock,
            intent=session.Intent.RECOVERY,
            issued_by=restore.Guard.LIBRARY_SESSION,
            authorises=Path(cfg.library.root),
            token=bare_metal.token,
        )
        assert not laundered.still_open

        with pytest.raises(CratekitError) as excinfo:
            restore.plan(cfg, record.session_id, held=laundered)

    assert "not held by this process" in excinfo.value.cause.message
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )


def test_round2_a_close_against_a_husk_is_refused_by_the_volume_gate(cfg):
    """FIX 4: the guard was ``root.is_dir()``, which every unmount leaves true.

    An ordinary Linux umount leaves the mount directory, a stale ``/Volumes`` stub
    IS that directory, and a library root that is a subdirectory of its mount point
    has a parent that survives. In all three the root exists and everything under
    it is gone, the reader cannot tell that from a library with nothing recorded
    yet, and ``close_session`` was allowed in that state over an open latch.

    THE FIX IS AT THE GATE RATHER THAN IN THE READER, and the reason is worth
    keeping: from inside the reader those two states are the same two facts, so a
    rule strict enough to catch the husk also refused the first run of every fresh
    install, which is a guard firing on correct behaviour. The gate has the
    recorded volume identity and the seams to ask about it, and ``assert_gates``
    already asserts it; this close was the one path that did not.
    """
    reconcile.record_markers(cfg, [reconcile.in_flight_marker(capture_stamp="c-1")])
    stranded = session.open_session(cfg, workflow="library-sweep")
    assert not reconcile.converged(cfg)

    root = Path(cfg.library.root)
    for child in root.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    assert root.is_dir(), "the fixture is not the shape this test is about"

    # What a stale stub reports: the identity of whatever disk the mount point
    # now sits on, which is not the volume this library was set up against. That
    # is the signal the reader does not have and the gate does.
    with pytest.raises(CratekitError) as excinfo:
        session.close_session(
            stranded,
            cfg,
            identity_provider=lambda _path: _ELSEWHERE,
            mount_enumerator=lambda: (),
        )

    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE

    # ABANDONING is still allowed, deliberately: gating it would leave somebody
    # with a run they can neither finish nor give up on.
    ended = session.close_session(stranded, cfg, state=session.SessionState.ABANDONED)
    assert ended.state is session.SessionState.ABANDONED


def test_round2_the_readers_still_answer_identically_on_a_gone_library(cfg):
    """The reader half that IS decidable: a root that is not there at all."""
    reconcile.record_markers(cfg, [reconcile.in_flight_marker(capture_stamp="c-1")])
    shutil.rmtree(cfg.library.root)

    for reader in (reconcile.records, reconcile.outstanding, reconcile.converged):
        with pytest.raises(CratekitError) as excinfo:
            reader(cfg)
        assert excinfo.value.cause.reason == "restore-record-unusable"


def test_round2_a_write_against_a_husk_does_not_rebuild_the_state_tree(cfg):
    """The other half of FIX 4: recording recreated the tree on the internal disk."""
    root = Path(cfg.library.root)
    for child in root.iterdir():
        shutil.rmtree(child) if child.is_dir() else child.unlink()

    with pytest.raises(CratekitError) as excinfo:
        reconcile.record_markers(cfg, [reconcile.in_flight_marker(capture_stamp="c")])

    assert excinfo.value.cause.reason == "restore-record-unusable"
    assert not config.library_state_dir(cfg).exists()


def test_round2_a_library_with_a_database_and_no_state_yet_is_not_refused(cfg):
    """P7: run the guard against correct behaviour too.

    A library this installation has been pointed at and has not yet written to has
    no state directory and is not a husk, and refusing it would fire on the first
    run of every fresh install.
    """
    shutil.rmtree(config.library_state_dir(cfg), ignore_errors=True)
    assert Path(cfg.library.db_path).exists()

    assert reconcile.records(cfg) == ()
    assert reconcile.converged(cfg)


def test_round2_the_real_mount_probe_is_armed_by_default(cfg, tmp_path):
    """NOTE 8: the seam is public, so prove the DEFAULT path refuses.

    Every bare-metal test injects ``mount_probe`` because a temporary directory is
    not a mount point on any platform and the refusals under test are unreachable
    without it. That makes it worth asserting once, here, that supplying nothing
    leaves the real probe in force.
    """
    seams = _volume_is_gone(cfg)
    del seams["mount_probe"]
    sibling = tmp_path / "library 1"
    sibling.mkdir()

    with pytest.raises(CratekitError) as excinfo:
        with restore.bare_metal_session(
            cfg, target=sibling, acknowledged=True, terminal=lambda: True, **seams
        ):
            raise AssertionError("unreachable")

    assert "unmounted volume leaves behind" in excinfo.value.cause.message


def test_round3_an_unwritable_coupled_directory_refuses_at_the_rehearsal(cfg, held):
    """BLOCKING 2: dropping the target probe for a tree replacement was a regression.

    ``_replace_directory`` renames the target to ``.replaced``, and renaming a
    directory rewrites that directory's own parent entry, so it needs write
    permission on the TARGET. With the coupled directory at 0o500 and its parent
    writable, the rehearsal reported all seven steps performed with no refusal and
    the real run staged the log aside, replaced the database, and died on the
    rename with the coupled state half replaced and the latch standing.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    coupled = config.library_coupled_dir(cfg)
    assert any(
        step.act is restore.Act.REPLACE_TREE and step.target == coupled
        for step in decided.steps
    ), "the plan does not replace the coupled directory, so this proves nothing"
    assert os.access(coupled.parent, os.W_OK), "the parent must stay writable"
    coupled.chmod(0o500)

    try:
        with pytest.raises(CratekitError) as excinfo:
            restore.run(decided, cfg, held=held, dry_run=True)
    finally:
        coupled.chmod(0o700)

    assert excinfo.value.cause.reason == "restore-step-failed"
    assert str(coupled) in excinfo.value.cause.message
    # Nothing was touched: the rehearsal refused before the first destructive step.
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )
    assert reconcile.outstanding(cfg) == ()


def test_round3_staged_companions_are_bounded_by_the_keep_count(cfg):
    """The staging is unbounded in the other direction on purpose, so bound it here.

    A staged log is never deleted by the restore that made it, and each attempt
    takes a fresh directory, so attempts accumulate copies on the volume being
    restored onto. Pruned only from the step that claims a restore finished,
    because a failed attempt's log is the one most likely to be wanted.

    EVERY NUMBER HERE IS A LITERAL, and the earlier version of this test had
    ``restore.KEEP_STAGED_ATTEMPTS`` in all three of them: the loop count, the
    expected surviving count, and the expected surviving payload. That version
    passed at every value of the constant except zero, so it asserted "the prune
    keeps the newest and drops the oldest" and asserted nothing whatever about the
    bound being five. Silently changing five to one then deleted four attempts'
    worth of write-ahead log, which ``_stage_companion_aside`` calls the only
    surviving record of work nobody can otherwise recover, with the suite green.
    Six restores, five survivors, and the first one gone.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    store = None

    for attempt in range(6):
        _wal_path(cfg).write_bytes(f"attempt {attempt}".encode())
        with restore.recovery_session(cfg, **gate_seams(cfg)) as open_session:
            decided = restore.plan(cfg, record.session_id, held=open_session)
            restore.run(decided, cfg, held=open_session)
            store = decided.pre_restore_root.parent

    kept = sorted(entry for entry in store.iterdir() if entry.is_dir())
    assert len(kept) == 5, "six attempts must leave five staged directories"
    # The NEWEST survive: the oldest stranded log is the one given up first.
    surviving = {
        path.read_bytes()
        for root in kept
        for path in root.iterdir()
        if path.name.endswith("wal")
    }
    assert surviving == {
        b"attempt 1",
        b"attempt 2",
        b"attempt 3",
        b"attempt 4",
        b"attempt 5",
    }


# ═══════════════════════════════════════════════════════════════════════════
# Fix round 4: the halves of a claimed fix that nothing could see
# ═══════════════════════════════════════════════════════════════════════════


def _staged_attempt(store: Path, name: str, *, age: int, payload: bytes = b"") -> Path:
    """One staged-companion directory, aged so the prune's order is decided.

    Ordered on ``st_mtime`` because the prune is, and set explicitly rather than
    left to creation order: several directories made inside one call are
    separated by microseconds, and a test whose subject is which one gets deleted
    should not rest on that.
    """
    attempt = store / name
    attempt.mkdir(parents=True)
    (attempt / "master.db-wal").write_bytes(payload)
    when = 1_700_000_000 + age
    os.utime(attempt, (when, when))
    return attempt


def test_round4_a_completed_restore_survives_a_staged_attempt_it_cannot_prune(cfg):
    """Round 3 added a second instance of the defect round 2 fixed, with no test.

    ``_prune_staged_companions`` is called from the RELEASE branch of ``_perform``,
    which is OUTSIDE the try that turns an ``OSError`` into a refusal, and by then
    ``reconcile.retract_in_flight`` has already discharged the latch. A staged
    directory an earlier attempt left behind that this account cannot remove
    therefore makes ``shutil.rmtree`` raise ``PermissionError`` at the end of a
    restore that has already landed. Without the ``except OSError`` inside that
    loop it escapes ``run`` raw: no reason, no remedy, no reserved exit code, and
    ``recovery_session`` closes the record ABANDONED for a restore that completed.

    This is ``test_round2_a_successful_restore_over_an_unremovable_old_copy_still
    _succeeds`` one function away, and it is modelled on it deliberately: round 2
    proved the invariant at ``_replace_directory`` and round 3 reintroduced the
    same shape somewhere else.
    """
    acknowledge(cfg)
    record, _captured = completed_session(cfg)
    _wal_path(cfg).write_bytes(b"transactions no capture holds")

    store = config.state_path("rekordbox_db", cfg).parent / restore.PRE_RESTORE_DIR
    # One attempt older than everything else, holding a log this account cannot
    # delete, and enough younger ones that the prune has to reach it.
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
    assert session.read_record(recovery_id, cfg).state is session.SessionState.CLOSED, (
        "the completed restore's own record was closed ABANDONED"
    )
    # The prune ran and did what it could: the oldest removable attempt is gone.
    assert not fillers[0].exists(), "the prune never reached the bound"
    # And the one it could not remove is still there, logged rather than raised.
    assert (locked / "master.db-wal").read_bytes() == b"the earliest log"
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )


def test_round4_an_unwritable_state_directory_refuses_at_the_rehearsal(cfg, held):
    """The parent half of ``_assert_writable``, which no test could see.

    ``_replace_directory`` stages a sibling beside its target, so every staging
    write lands in the target's PARENT. The only test in the area chmods the
    TARGET and asserts the parent stays writable, so it structurally cannot see
    this half, and the one test that does chmod a parent builds a plan whose
    coupled step is a REMOVE rather than a REPLACE_TREE, so a different step
    refuses and the parent probe is never consulted.

    With the probe gone nothing refuses at all: the rehearsal reports every step
    performed, and the real run stages the log aside, replaces the database, and
    dies inside ``shutil.copytree`` into the unwritable parent, leaving the
    database at the new generation and the coupled state at the old. No other step
    covers it, because the database's parent is ``<library>/db`` and this one is
    ``<library>/<state>``.

    THE REFUSAL IS READ OFF ``detail["unwritable"]`` RATHER THAN OUT OF THE
    MESSAGE, and the difference is the whole point of this test. The parent here
    is ``<library>/.cratekit`` and the target is ``<library>/.cratekit/coupled``,
    so the parent's path is a PREFIX of the target's; a substring test against the
    message is satisfied by the sentence's second half, "would stop at <target>",
    no matter what the first half names. Measured: deleting the unwritable
    directory from the message entirely left that assertion green, so it could not
    tell the parent probe from the target probe, which is the one distinction this
    test exists to make. The detail field carries the probe's own answer and
    nothing else, so it can. The message is asserted too, anchored at the front
    rather than searched, because a person reads the sentence and not the detail
    dictionary: an anchored match cannot be satisfied by the target's path and
    goes red when the directory is dropped out of the sentence.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    coupled = config.library_coupled_dir(cfg)
    assert any(
        step.act is restore.Act.REPLACE_TREE and step.target == coupled
        for step in decided.steps
    ), "the plan does not replace the coupled directory, so this proves nothing"
    parent = coupled.parent
    assert parent != config.state_path("rekordbox_db", cfg).parent, (
        "the coupled parent and the database parent must be different directories"
    )
    parent.chmod(0o500)
    assert os.access(coupled, os.W_OK), "the target must stay writable"

    try:
        with pytest.raises(CratekitError) as excinfo:
            restore.run(decided, cfg, held=held, dry_run=True)
    finally:
        parent.chmod(0o700)

    assert excinfo.value.cause.reason == "restore-step-failed"
    assert excinfo.value.cause.detail["unwritable"] == str(parent)
    assert excinfo.value.cause.message.startswith(f"{parent} is not writable")
    # Nothing was touched: the rehearsal refused before the first destructive step.
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )
    assert reconcile.outstanding(cfg) == ()


def _playlist_xml_path(cfg) -> Path:
    """rekordbox's own playlist document, which travels with the database.

    Named through ``rb_writer`` rather than spelled, and it matters here because
    it is the one restorable source that is NOT inside the coupled directory and
    is not a database sidecar, which is what puts a REMOVE step ahead of the
    coupled REPLACE_TREE in an ordinary plan.
    """
    return config.state_path("rekordbox_db", cfg).parent / rb_writer.MASTER_PLAYLIST_XML


def test_round4_the_peak_of_an_ordinary_plan_is_an_exact_number(cfg, held):
    """The one assertion shape that can see a 2,048-byte term.

    Every other capacity test asserts an inequality: the estimate is above the
    measured peak, below the sum of everything, above the largest single step.
    All three survive charging ``freed_bytes`` the directory-entry overhead, which
    is the asymmetry ``snapshot.freed_bytes`` says is load bearing, because what a
    step gives back reaches the peak only through the running total and only at a
    LATER step, and on this product's plans the largest step is last. So the whole
    term is worth one directory entry and nothing could see it.

    Derived BY HAND from the four quantities pinned below, not by calling
    ``space_peak_bytes``:

    * replace the database:   peak = 0 + 6,144 = 6,144;  occupied = 6,144 - 4,096 = 2,048
    * remove the absent xml:  it is not there live, so this frees nothing
    * replace the coupled tree: peak = max(6,144, 2,048 + 8,192) = 10,240

    With the entry overhead charged on both sides the two ``freed`` figures become
    6,144 and the answer becomes 8,192.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    captured = {
        entry.source.name: entry.captured
        for entry in snapshot.read_manifest(decided.capture_root).sources
        if entry.captured is not None
    }
    # The shape this arithmetic assumes, pinned so a filesystem that allocates
    # differently fails HERE and says so rather than failing on the total.
    assert snapshot.incoming_bytes(captured["master.db"]) == 6144
    assert snapshot.incoming_bytes(captured["coupled"]) == 8192
    assert snapshot.freed_bytes(config.state_path("rekordbox_db", cfg)) == 4096
    assert snapshot.freed_bytes(config.library_coupled_dir(cfg)) == 4096

    assert restore.space_peak_bytes(decided) == 10240


def test_round4_a_removal_ahead_of_a_tree_replacement_lowers_the_peak(cfg, held):
    """The ``Act.REMOVE`` subtraction is observable, and nothing asserted it.

    ``_file_steps`` appends steps in MANIFEST order, and rekordbox's playlist
    document sits beside the database rather than inside the coupled directory, so
    a plan that removes it does so BEFORE the coupled tree is replaced. The
    subtraction then lowers the running total and therefore lowers the peak for
    every later step. The direction is safe, because the removal genuinely happens
    first and ``_remove`` raises rather than failing silently, but the arithmetic
    was unguarded.

    THE PROPORTIONS ARE THE TEST. An earlier version removed a 1 MiB document
    ahead of an 8 KiB coupled tree, which drove the running total so far below
    zero that the coupled step could not reach the database step's 6,144 either
    way; DOUBLING the subtraction killed nothing, so the term was pinned for
    PRESENCE and not for magnitude while this docstring said it was derived by
    hand. So the removal is now SMALLER than the tree that follows it, which is
    the only arrangement in which the subtraction reaches the peak at all.

    Derived BY HAND from the five quantities pinned below:

    * replace the database:    peak = 0 + 6,144 = 6,144;  occupied = 2,048
    * remove an 8 KiB xml:     occupied = 2,048 - 8,192 = -6,144
    * replace the coupled tree: peak = max(6,144, -6,144 + 1,060,864) = 1,054,720

    The coupled figure is the ordinary plan's 8,192 plus the queue this fixture
    puts inside it before the capture: one directory entry at 2,048, and one
    1 MiB document at 1,048,576 blocks plus its own 2,048 entry.

    Every wrong version of the subtraction now moves the answer. Dropping it
    gives 1,062,912, doubling it gives 1,046,528, and charging the entry overhead
    the way ``incoming_bytes`` does gives 1,052,672. An over-count puts the
    estimate BELOW the real peak, which is the direction that lets a preflight
    pass on a volume that cannot hold the restore.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    queue = config.state_path("review_queue", cfg)
    assert config.library_coupled_dir(cfg) in queue.parents, (
        "the queue must be inside the coupled directory or the capture does not "
        "carry it and this fixture proves nothing"
    )
    queue.mkdir(parents=True, exist_ok=True)
    (queue / "item-00000.json").write_bytes(b"q" * 1024 * 1024)
    record, _captured = completed_session(cfg)
    # Created AFTER the capture, so the manifest records it absent and the plan
    # removes it, and it is on disk now, so removing it gives real bytes back.
    playlists = _playlist_xml_path(cfg)
    playlists.write_bytes(b"p" * 8192)
    decided = restore.plan(cfg, record.session_id, held=held)

    acts = [step.act for step in decided.steps if step.target is not None]
    assert acts.index(restore.Act.REMOVE) < acts.index(restore.Act.REPLACE_TREE), (
        "the removal must precede the tree replacement or this proves nothing"
    )
    captured = {
        entry.source.name: entry.captured
        for entry in snapshot.read_manifest(decided.capture_root).sources
        if entry.captured is not None
    }
    assert snapshot.incoming_bytes(captured["master.db"]) == 6144
    assert snapshot.incoming_bytes(captured["coupled"]) == 1060864
    assert snapshot.freed_bytes(config.state_path("rekordbox_db", cfg)) == 4096
    assert snapshot.freed_bytes(config.library_coupled_dir(cfg)) == 1052672
    assert snapshot.freed_bytes(playlists) == 8192
    # Those five literals already say the removal is SMALLER than the tree behind
    # it, which is the proportion the whole test turns on. Restating it as
    # ``freed_bytes(playlists) < incoming_bytes(coupled)`` would read both sides
    # back out of the code under test, which is the shape this round is removing.

    assert restore.space_peak_bytes(decided) == 1054720


def test_round4_the_default_retention_count_is_five(cfg):
    """``DEFAULT_KEEP`` survived being changed to one, because nothing used it.

    Every retention test passes an explicit ``RetentionPolicy``, so the default
    was reachable only through ``retention_plan(cfg)`` with no policy, and the one
    test that did that asserted something else entirely. Seven captures, all past
    the default age bound, and the count is the only thing standing between them
    and deletion: five survive because the count protects the first five, and the
    two the count does not reach are old enough for the age bound to take.
    """
    now = datetime.now(UTC)
    made = [take_capture(cfg, stamp=f"capture-{index}") for index in range(7)]
    for index, captured in enumerate(made):
        _age_capture(captured.root, days=90 - index, now=now)

    decided = restore.retention_plan(cfg, protected_provider=set, now=now)

    assert len(decided.keeping) == 5, "the default count is not five"
    assert len(decided.deleting) == 2
    # Newest first, so the two oldest are the two that go.
    assert [entry.root for entry in decided.deleting] == [made[1].root, made[0].root]


def test_round4_a_volume_just_above_what_the_rule_demands_is_not_refused(
    cfg, held, monkeypatch
):
    """P7 on the capacity rule: a fix round fails by being too strict just as often.

    Round 2's defect was a FALSE REFUSAL, from a rule that demanded 1.10 times the
    sum of every captured source. Round 3 replaced it with a running total, and
    nothing synthesised a free-space value just ABOVE what the new rule demands to
    prove it still lets a restore through. Free space is pinned to exactly what
    the preflight asks for, which is the tightest volume that may proceed, and the
    restore has to land.

    WHAT THIS CANNOT SEE IS THE HEADROOM'S VALUE, and an earlier version of it
    implied otherwise. Its precondition read
    ``demanded < int(summed * CAPACITY_HEADROOM)`` with ``demanded`` computed from
    the same constant, so the constant appeared on both sides and CANCELLED: the
    whole assertion reduced to "the peak is below the sum", and changing 1.10 to
    1.00 left it, and the entire suite, green. The precondition below says that
    directly, without pretending to constrain a value it cannot. The value itself
    is pinned with literals in the test that follows.

    The boundary is still worth asking relationally, and only relationally: the
    claim here is that free space equal to EXACTLY what the rule demands is
    accepted, which is a statement about the comparison operator in
    ``assert_room_for`` and turns red if ``>=`` ever becomes ``>``.
    """
    _build_capacity_shape(cfg, database=8, wal=4, items=2000)
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    demanded = int(restore.space_peak_bytes(decided) * snapshot.CAPACITY_HEADROOM)
    summed = sum(
        snapshot.incoming_bytes(entry.source)
        for entry in snapshot.read_manifest(decided.capture_root).sources
        if entry.captured is not None
    )
    assert restore.space_peak_bytes(decided) < summed, (
        "this volume is not tight enough to say anything: the round 1 rule "
        "demanded the same multiple of the SUM, so it would have accepted this "
        "one too"
    )

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: demanded)
    outcome = restore.run(decided, cfg, held=held)

    assert outcome.converged, "the tightest volume the rule allows was refused"
    assert config.state_path("rekordbox_db", cfg).read_bytes()[:1] == b"d"


def test_round5_the_capacity_headroom_decides_a_refusal_at_two_literal_volumes(
    cfg, held, monkeypatch
):
    """``CAPACITY_HEADROOM`` governs a REFUSAL and nothing could see its value.

    Measured on the round 4 tip: changing it from 1.10 to 1.00 left the whole
    suite green, 3,297 passed. It died only at 0.0. Every test that touched it
    computed its own input from it, so the constant cancelled and the assertions
    reduced to statements that are true at every value above zero.

    1.00 IS THE VALUE SOMEBODY REACHES FOR, which is what makes the blindness
    expensive rather than theoretical: the constant's own docstring names false
    refusals as the pressure on it. At 1.00 a restore is allowed to start on a
    volume holding precisely the estimate, another process writes during the copy,
    and ``shutil.copytree`` dies part way through the coupled tree with the
    database already at the new generation and the coupled state at the old.

    SO BOTH FREE-SPACE FIGURES ARE LITERALS, and neither the input nor the
    expected answer reads the constant or calls ``space_peak_bytes``. The plan is
    the ordinary one whose peak is 10,240 bytes, derived by hand above from the
    four quantities pinned again here:

    * 10,240 x 1.05 = 10,752 free bytes must still be REFUSED
    * 10,240 x 1.10 = 11,264 free bytes must be ACCEPTED

    Together they bound the constant into ``(1.05, 1.10]``. At 1.00 or 1.05 the
    first half goes red, at 1.15 the second does.
    """
    write_state(cfg, "label_watermarks", {"source": "before"})
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    captured = {
        entry.source.name: entry.captured
        for entry in snapshot.read_manifest(decided.capture_root).sources
        if entry.captured is not None
    }
    # The shape the two literals are derived from, pinned so a filesystem that
    # allocates differently fails HERE and says which quantity moved.
    assert snapshot.incoming_bytes(captured["master.db"]) == 6144
    assert snapshot.incoming_bytes(captured["coupled"]) == 8192
    assert snapshot.freed_bytes(config.state_path("rekordbox_db", cfg)) == 4096
    assert snapshot.freed_bytes(config.library_coupled_dir(cfg)) == 4096

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 10752)
    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert excinfo.value.cause.reason == "snapshot-store-full"
    assert excinfo.value.cause.detail["required_bytes"] == 11264
    # The rehearsal refused, so the library is byte for byte as it was found.
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )

    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: 11264)
    outcome = restore.run(decided, cfg, held=held)

    assert outcome.converged, "the volume the headroom asks for was refused"


def _shm_path(cfg) -> Path:
    """The live shared-memory index, resolved through the inventory like the log."""
    database = config.state_path("rekordbox_db", cfg)
    companions = config.sidecar_paths("rekordbox_db", cfg)
    return next(
        path
        for path in companions
        if path.name.startswith(database.name) and path != _wal_path(cfg)
    )


def test_round5_a_staged_companion_is_never_written_over(cfg, held):
    """The staging side had a probabilistic answer where the capture side has a rule.

    ``_stage_companion_aside`` called ``_mkdir_private``, which RETURNS SILENTLY on
    a directory that already exists, and then ``os.replace``, which overwrites. The
    only thing standing between two attempts and one destroyed log was the 64 bits
    of random in the stamp. ``snapshot.capture`` refuses an occupied stamp outright
    one module away, on the same reasoning, so the asymmetry was accidental rather
    than argued.

    The bytes at stake are the ones this whole staging exists for: a write-ahead
    log holds transactions that are in the main file nowhere and in no capture at
    all, so overwriting a staged one destroys the only copy that exists anywhere.
    Refusing costs a restore that can be run again; not refusing costs the work.

    EVERY FIELD OF THE REFUSAL IS PINNED, not only its slug. The round that added
    this guard asserted ``reason == "internal-error"`` and nothing else, and that
    slug is the eleventh use of one string in this module: swapping the remedy,
    deleting the whole detail dictionary and replacing the entire message all left
    the suite green. The slug is now this condition's own, and it is asserted here
    with the remediation, the retryability and the detail, because those are what a
    person actually receives.
    """
    log = _wal_path(cfg)
    log.write_bytes(b"the live log, transactions committed since the checkpoint")
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    assert log in [
        step.target for step in decided.steps if step.act is restore.Act.CLEAR
    ], "this plan does not stage the log aside, so it proves nothing"

    # An earlier attempt's log, already resting under the name this one wants.
    decided.pre_restore_root.mkdir(parents=True)
    survivor = decided.pre_restore_root / log.name
    survivor.write_bytes(b"an earlier attempt's log, recoverable from nowhere else")

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held)

    cause = excinfo.value.cause
    assert cause.reason == "restore-staging-occupied"
    assert cause.code is ExitCode.PRECONDITION
    assert survivor.read_bytes() == (
        b"an earlier attempt's log, recoverable from nowhere else"
    )
    assert log.read_bytes() == (
        b"the live log, transactions committed since the checkpoint"
    ), "the live log was moved anyway"


def test_round6_the_occupied_staging_is_a_repeat_rather_than_a_defect(cfg, held):
    """The refusal used to say "report a defect and do not retry", and a retry works.

    Driven rather than argued: the refusal fires, and then a fresh plan and a fresh
    run of the SAME restore complete, because a fresh attempt takes a fresh staging
    directory. Telling somebody to file a bug for a condition they clear by running
    the command again is a support failure, and the sibling refusal a hundred lines
    away, for the same class of interrupted restore, already says the true thing.

    THE REMEDY IS ASSERTED AS ABSENT ON PURPOSE. This refusal carries STEPS rather
    than a remedy token, which is the shape the sibling uses and the shape the
    reason registry argues for whenever the answer is a sentence rather than a
    command this product runs.
    """
    log = _wal_path(cfg)
    log.write_bytes(b"the live log, transactions committed since the checkpoint")
    record, _captured = completed_session(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")
    decided = restore.plan(cfg, record.session_id, held=held)
    decided.pre_restore_root.mkdir(parents=True)
    (decided.pre_restore_root / log.name).write_bytes(b"an earlier attempt's log")

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held)

    cause = excinfo.value.cause
    assert cause.retryable is True, "a condition a repeat clears is retryable"
    assert cause.remediation.remedy is None, (
        "this refusal answers with steps, not with a remedy token, and the token it "
        "used to carry told the user to file a bug"
    )
    assert any("safe to repeat" in step for step in cause.remediation.steps), (
        f"nothing in {cause.remediation.steps} tells the user a repeat is safe"
    )
    assert cause.detail["target"] == str(log)
    assert cause.detail["staged"] == str(decided.pre_restore_root / log.name)
    assert cause.detail["staging_root"] == str(decided.pre_restore_root)
    assert cause.detail["already_staged"] == [log.name]

    # And now do exactly what the steps say. A fresh plan takes a fresh staging
    # directory, so the restore it refused completes.
    again = restore.plan(cfg, record.session_id, held=held)
    assert again.pre_restore_root != decided.pre_restore_root
    outcome = restore.run(again, cfg, held=held)

    assert outcome.converged, "the retry the refusal recommends does not work"
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )
    assert (decided.pre_restore_root / log.name).read_bytes() == (
        b"an earlier attempt's log"
    ), "the retry destroyed the bytes the refusal existed to protect"


def test_round6_the_rehearsal_refuses_the_collision_the_real_run_refuses(cfg, held):
    """The whole plan is checked before any of it is performed, or it is not.

    The guard was added to the PERFORMING path only, which put it after the point
    it exists to protect: ``_stage_companion_aside`` runs once per companion, so
    with both companions live and the SECOND one's resting name occupied, the
    first was already renamed out of the live tree before anything raised. The run
    aborted with the live write-ahead log gone and the database never replaced,
    which is the exact half done state the module says the staging prevents.

    And the rehearsal was worse than useless. Measured on the branch that shipped
    it: with the collision present, ``dry_run=True`` reported all eight steps
    performed and refused nothing, and the real run then refused. A rehearsal that
    passes over a run that refuses is the most misleading shape this module has.
    """
    log = _wal_path(cfg)
    index = _shm_path(cfg)
    log.write_bytes(b"the live log, transactions committed since the checkpoint")
    index.write_bytes(b"the live shared-memory index")
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)
    cleared = [step.target for step in decided.steps if step.act is restore.Act.CLEAR]
    assert cleared == [log, index], (
        f"this plan does not clear both companions in order, so it proves nothing: "
        f"{cleared}"
    )

    # The SECOND companion's resting name is the occupied one, so a guard that
    # only fires while performing fires after the first has already moved.
    decided.pre_restore_root.mkdir(parents=True)
    (decided.pre_restore_root / index.name).write_bytes(b"an earlier attempt's index")

    with pytest.raises(CratekitError) as rehearsal:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert rehearsal.value.cause.reason == "restore-staging-occupied"
    assert log.read_bytes() == (
        b"the live log, transactions committed since the checkpoint"
    ), "the rehearsal moved the first companion, which a rehearsal performs nothing"

    with pytest.raises(CratekitError) as real:
        restore.run(decided, cfg, held=held)

    assert real.value.cause.reason == rehearsal.value.cause.reason, (
        "the rehearsal and the run disagree about this plan"
    )
    assert log.read_bytes() == (
        b"the live log, transactions committed since the checkpoint"
    ), "the run refused after moving the first companion, which is the half done state"
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )


def test_round6_the_performing_backstop_names_what_it_already_moved(cfg, held, monkeypatch):
    """The preflight decides; this one exists for the window after it.

    A directory can be occupied between the check and the rename, so the guard on
    the performing path stays. What it must NOT be is the primary, and what it must
    not do is describe only the file it declined to touch: the previous refusal
    named ``master.db-shm``, the companion still sitting in the live tree, and said
    nothing about ``master.db-wal``, the one it had already moved and the one whose
    disappearance the person is looking at.

    The race is driven rather than described: the collision is planted after the
    first companion has really been staged, which is the only state this backstop
    can be reached in.
    """
    log = _wal_path(cfg)
    index = _shm_path(cfg)
    log.write_bytes(b"the live log, transactions committed since the checkpoint")
    index.write_bytes(b"the live shared-memory index")
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    real_stage = restore._stage_companion_aside

    def stage_then_race(target: Path, staging: Path) -> None:
        real_stage(target, staging)
        # Somebody else lands the second companion's resting name in the window.
        intruder = staging / index.name
        if target != index and not intruder.exists():
            intruder.write_bytes(b"an earlier attempt's index")

    monkeypatch.setattr(restore, "_stage_companion_aside", stage_then_race)

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held)

    cause = excinfo.value.cause
    assert cause.reason == "restore-staging-occupied"
    # The companion this run already moved is named, in the detail AND in the
    # sentence, alongside where it now is.
    assert cause.detail["already_staged"] == sorted([log.name, index.name])
    assert log.name in cause.message
    assert str(decided.pre_restore_root) in cause.message
    assert any(
        str(decided.pre_restore_root) in step for step in cause.remediation.steps
    ), f"no step says where the moved companion is: {cause.remediation.steps}"
    assert (decided.pre_restore_root / log.name).read_bytes() == (
        b"the live log, transactions committed since the checkpoint"
    ), "the log this run moved is not where the refusal says it is"


def test_round6_a_dangling_link_at_the_resting_name_is_a_name_already_taken(cfg, held):
    """``Path.exists`` follows symlinks, so a broken link read as a free name.

    The rule the guard states is that a name already TAKEN means two attempts, and
    a name holding a dangling link is taken. Asked with ``exists``, the guard let
    the rename through and ``os.replace`` put the live log where the link was,
    which both destroys the link and stages a log under a name a later attempt
    believes is free. This is absence read as evidence of absence.
    """
    log = _wal_path(cfg)
    log.write_bytes(b"the live log, transactions committed since the checkpoint")
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    decided.pre_restore_root.mkdir(parents=True)
    taken = decided.pre_restore_root / log.name
    taken.symlink_to(decided.pre_restore_root / "a-target-that-is-not-there")
    assert not taken.exists(), "this link resolves, so it is not the shape under test"
    assert taken.is_symlink()

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert excinfo.value.cause.reason == "restore-staging-occupied"
    assert taken.is_symlink(), "the link was replaced, which is the defect"
    assert log.read_bytes() == (
        b"the live log, transactions committed since the checkpoint"
    )


def test_round6_a_dangling_link_at_the_live_companion_is_still_moved_aside(cfg, held):
    """The same read, one line earlier, and the cost is the opposite one.

    A dangling link at ``master.db-wal`` is a name the storage engine follows and
    CREATES THROUGH, so leaving it beside a replaced database means the next log
    is written wherever the link points. ``Path.exists`` resolves the link, answers
    False, and the early return skipped it as though the companion were absent.
    """
    log = _wal_path(cfg)
    log.symlink_to(log.parent / "somewhere-that-is-not-there")
    assert not log.exists() and log.is_symlink()
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    outcome = restore.run(decided, cfg, held=held)

    assert outcome.converged
    assert not log.is_symlink(), (
        "a dangling link is still a name the engine writes through, and it is "
        "still beside the replaced database"
    )
    staged = decided.pre_restore_root / log.name
    assert staged.is_symlink(), "the link was not moved aside, it was lost"


def test_round6_a_dangling_link_at_the_live_name_does_not_defeat_the_collision_guard(
    cfg, held
):
    """The two ``lexists`` reads are separate holes and the second was uncovered.

    Found by mutation: changing the guard's OWN early return back to ``exists``
    killed nothing, because the caller's early return already asked ``lexists``
    and the tests drove only that side. The combination is what the mutation
    described. A dangling link at the live companion's name and an earlier
    attempt's log at the resting name: the guard resolves the link, answers "no
    live companion here", returns without refusing, and the caller then renames
    the link over the one surviving copy of transactions that are in no capture.

    Both conditions are the same absence-read-as-evidence-of-absence shape, and
    each of them has to be asked with the read that sees a name rather than a
    file.
    """
    log = _wal_path(cfg)
    log.symlink_to(log.parent / "somewhere-that-is-not-there")
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    decided.pre_restore_root.mkdir(parents=True)
    survivor = decided.pre_restore_root / log.name
    survivor.write_bytes(b"an earlier attempt's log, recoverable from nowhere else")

    with pytest.raises(CratekitError) as excinfo:
        restore.run(decided, cfg, held=held, dry_run=True)

    assert excinfo.value.cause.reason == "restore-staging-occupied"
    assert survivor.read_bytes() == (
        b"an earlier attempt's log, recoverable from nowhere else"
    ), "the link was renamed over the only copy of those transactions"
    assert log.is_symlink(), "the live name was consumed by a rehearsal"


def test_round7_an_unreadable_staging_directory_still_refuses_the_same_way(cfg, held):
    """``_staged_names`` swallows ``OSError``, and nothing drove the swallow.

    Found by mutation: deleting the ``try``/``except`` in ``_staged_names`` and
    letting the error escape killed NOTHING, while the docstring on that function
    makes a load bearing claim, that it never raises, because it runs only to
    DESCRIBE a refusal that is already decided. An unreadable directory must not
    replace that refusal with a different one, and a claim no test drives is a
    comment.

    The branch is reachable and this is the shape that reaches it. With the
    staging directory at mode ``0o111`` the account may traverse it and may not
    read it: ``os.path.lexists`` still answers True for the occupant, so the guard
    still decides to refuse, and ``iterdir`` raises ``PermissionError``. Without
    the swallow that error escapes ``_preflight`` raw, and a person restoring a
    library receives an unhandled ``PermissionError`` instead of the sentence that
    tells them a repeat is safe.

    THE DEGRADED OUTPUT IS PINNED TOO, because it is what the swallow produces
    rather than an accident of it: ``already_staged`` empties, and the message
    falls back to naming the resting file it refused to overwrite. Both are the
    honest answer here, since the directory genuinely cannot be listed, and both
    would otherwise be free to change under a green suite. What must NOT degrade
    is the refusal itself, which still names the slug, the target, the resting
    name and the staging root, and still leaves every byte where it was.
    """
    log = _wal_path(cfg)
    log.write_bytes(b"the live log, transactions committed since the checkpoint")
    record, _captured = completed_session(cfg)
    decided = restore.plan(cfg, record.session_id, held=held)

    decided.pre_restore_root.mkdir(parents=True)
    survivor = decided.pre_restore_root / log.name
    survivor.write_bytes(b"an earlier attempt's log, recoverable from nowhere else")
    decided.pre_restore_root.chmod(0o111)
    try:
        assert os.path.lexists(survivor), (
            "this directory hides its occupant from lexists too, so the guard "
            "never reaches the listing and the test proves nothing"
        )
        with pytest.raises(OSError):
            list(decided.pre_restore_root.iterdir())

        with pytest.raises(CratekitError) as excinfo:
            restore.run(decided, cfg, held=held)
    finally:
        decided.pre_restore_root.chmod(0o700)

    cause = excinfo.value.cause
    assert cause.reason == "restore-staging-occupied", (
        "an unreadable staging directory replaced the decided refusal with a "
        "different failure"
    )
    assert cause.code is ExitCode.PRECONDITION
    assert cause.retryable is True
    assert cause.detail["target"] == str(log)
    assert cause.detail["staged"] == str(survivor)
    assert cause.detail["staging_root"] == str(decided.pre_restore_root)
    assert cause.detail["already_staged"] == [], (
        "the listing failed, so the honest answer is that this refusal cannot "
        "say what else is in there"
    )
    assert survivor.name in cause.message, (
        f"with nothing listable the message must still name the file it refused "
        f"to overwrite: {cause.message}"
    )
    assert survivor.read_bytes() == (
        b"an earlier attempt's log, recoverable from nowhere else"
    )
    assert log.read_bytes() == (
        b"the live log, transactions committed since the checkpoint"
    ), "the live log was moved anyway"


def test_round6_a_retry_after_a_partial_failure_still_runs(cfg, held, monkeypatch):
    """A restore that refuses to run is as bad as one that half runs.

    The new refusal sits on a destructive path's preflight, so the failure mode it
    can introduce is over restriction. The shape most at risk is the one the
    sibling refusal explicitly promises: an attempt dies part way through, leaving
    a staged log behind, and the person runs the restore again. That must proceed,
    and the earlier attempt's log must survive it.
    """
    log = _wal_path(cfg)
    log.write_bytes(b"the first attempt's log")
    record, _captured = completed_session(cfg)
    config.state_path("rekordbox_db", cfg).write_bytes(b"database, generation two")

    first = restore.plan(cfg, record.session_id, held=held)

    def _explode(_source, _target):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(restore, "_replace_file", _explode)
    with pytest.raises(CratekitError) as excinfo:
        restore.run(first, cfg, held=held)
    assert excinfo.value.cause.reason == "restore-step-failed"
    stranded = first.pre_restore_root / log.name
    assert stranded.read_bytes() == b"the first attempt's log"

    # Put right what the error named, then do what the refusal said.
    monkeypatch.undo()
    log.write_bytes(b"the second attempt's log")
    second = restore.plan(cfg, record.session_id, held=held)
    outcome = restore.run(second, cfg, held=held)

    assert outcome.converged, "the retry the sibling refusal promises was refused"
    assert config.state_path("rekordbox_db", cfg).read_bytes() == (
        b"database, generation one"
    )
    assert stranded.read_bytes() == b"the first attempt's log", (
        "the retry overwrote the bytes the first attempt staged"
    )
    assert (second.pre_restore_root / log.name).read_bytes() == (
        b"the second attempt's log"
    )


def test_round4_the_residual_findings_this_module_names_still_exist():
    """Source references residual findings by TITLE, and the titles have to resolve.

    ``docs/residual-findings.md`` is appended to by every branch, and the standing
    rule renumbers an entry when two of them reach for one number at a merge. A
    number written into a docstring therefore repoints SILENTLY: it still reads as
    a citation and it now names somebody else's finding. That has already happened
    in this repository, where ``core/convergence.py`` said "See R-15" and R-15 on
    the merged tree was a different entry.

    So the module names them by title and this asserts the titles resolve. A
    renumber leaves this green, which is correct. A retitle or a deletion turns it
    red, which is also correct.

    THE CITATION HALF ASKS WHERE THE NAME APPEARS, NOT HOW OFTEN. It used to count
    occurrences and require three, which is the definition, the export and one
    citation; the count was exactly three, so it had no slack in either direction.
    Dropping the ``__all__`` export while keeping the citation was a FALSE RED, and
    three mentions anywhere at all, none of them prose, was a false green. Parsing
    the docstrings answers the question that was being asked in the first place.
    """
    headings = {
        match.group(1).strip()
        for match in re.finditer(
            r"^## R-\d+\.\s*(.+)$",
            (REPO_ROOT / "docs" / "residual-findings.md").read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    }
    named = {
        restore.RESIDUAL_CAPTURE_VOLUME_UNREPORTED,
        restore.RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH,
    }

    assert named <= headings, sorted(named - headings)

    # And each name is actually CITED IN PROSE, rather than defined, exported and
    # then ignored while the docstrings go back to writing a number.
    source = Path(inspect.getfile(restore)).read_text(encoding="utf-8")
    documented = [
        ast.get_docstring(node) or ""
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef)
    ]
    assert documented, "restore.py parsed to no docstrings at all"
    for name in (
        "RESIDUAL_CAPTURE_VOLUME_UNREPORTED",
        "RESIDUAL_BARE_METAL_HAS_NO_WRITE_PATH",
    ):
        assert any(name in text for text in documented), (
            f"no docstring in restore.py cites {name}"
        )
