"""The snapshot half of the safety chain: capture, restore, and what pruning spares.

Each property guarded here failed silently in the source system: the restore is
write-ahead-log symmetric, pruning spares a snapshot an open run still references,
and snapshotting does not prune."""

from __future__ import annotations

import importlib
import json
import os
import sqlite3
import time
from pathlib import Path

import pytest

from cratekit.core import config
from cratekit.core import rb_writer as W
from tests.test_config import valid_data


@pytest.fixture(autouse=True)
def _rekordbox_closed(monkeypatch):
    """Patched in ``rb_writer`` itself, where the guards resolve the names."""
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)


# ── the write-ahead-log round trip ───────────────────────────────────────────


def _wal_database_with_an_uncheckpointed_row(tmp_path: Path):
    """A database whose newest row is only in the log, left OPEN as rekordbox's is."""
    db_path = tmp_path / "master.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA wal_autocheckpoint=0")  # never fold the log in on its own
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, tag TEXT)")
    conn.execute("INSERT INTO t (tag) VALUES ('baseline')")
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")  # baseline is now IN the file
    conn.execute("INSERT INTO t (tag) VALUES ('wal_only')")  # this one stays in the log
    conn.commit()
    return db_path, conn


def _tags(db_path: Path) -> set[str]:
    conn = sqlite3.connect(db_path)
    try:
        return {row[0] for row in conn.execute("SELECT tag FROM t")}
    finally:
        conn.close()


def test_restore_preserves_uncheckpointed_wal_rows(tmp_path):
    """The regression guard. Without the symmetric restore this loses a row."""
    db_path, conn = _wal_database_with_an_uncheckpointed_row(tmp_path)
    wal = db_path.with_name(db_path.name + "-wal")
    assert wal.exists() and wal.stat().st_size > 0, "the fixture did not leave a live log"

    snapshot = W.snapshot_db(db_path, stamp="s", root=tmp_path / "snaps")
    conn.close()  # rekordbox quits; the live database checkpoints on the way out

    W.restore_from_snapshot(snapshot, db_path=db_path)

    assert _tags(db_path) == {"baseline", "wal_only"}


def test_restore_roundtrips_a_checkpointed_db(tmp_path):
    """The control. It isolates the defect to the log path, not to the harness."""
    db_path = tmp_path / "master.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, tag TEXT)")
    conn.execute("INSERT INTO t (tag) VALUES ('a')")
    conn.execute("INSERT INTO t (tag) VALUES ('b')")
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    conn.close()

    snapshot = W.snapshot_db(db_path, stamp="s", root=tmp_path / "snaps")
    W.restore_from_snapshot(snapshot, db_path=db_path)

    assert _tags(db_path) == {"a", "b"}


def test_the_capture_set_is_derived_from_the_state_schema():
    """Both sidecars are captured, only the log put back, read off the schema so no list drifts."""
    assert set(W.db_sidecar_suffixes()) == {s.suffix for s in config.SQLITE_SIDECARS}
    assert set(W.restored_sidecar_suffixes()) == {
        s.suffix for s in config.SQLITE_SIDECARS if s.restored
    }
    assert set(W.restored_sidecar_suffixes()) < set(W.db_sidecar_suffixes())


def test_a_restore_never_puts_back_the_shared_memory_index(tmp_path):
    """The shared-memory index is captured, never put back, as a stale one contradicts the log."""
    db_path, conn = _wal_database_with_an_uncheckpointed_row(tmp_path)
    snapshot = W.snapshot_db(db_path, stamp="s", root=tmp_path / "snaps")
    conn.close()

    assert (snapshot.with_name(snapshot.name + "-shm")).exists(), "the capture missed a sidecar"

    # Plant a live index, and prove the restore cleared it rather than restoring it.
    live_shm = db_path.with_name(db_path.name + "-shm")
    live_shm.write_bytes(b"stale")
    W.restore_from_snapshot(snapshot, db_path=db_path)
    assert not live_shm.exists()


def test_the_legacy_playlist_file_travels_with_the_database(tmp_path):
    """rekordbox's legacy playlist file describes the database beside it, so it travels with it."""
    db_path = tmp_path / "master.db"
    sqlite3.connect(db_path).close()
    legacy = db_path.parent / W.MASTER_PLAYLIST_XML
    legacy.write_text("original")

    snapshot = W.snapshot_db(db_path, stamp="s", root=tmp_path / "snaps")
    assert (snapshot.parent / W.MASTER_PLAYLIST_XML).read_text() == "original"

    legacy.write_text("moved on")
    W.restore_from_snapshot(snapshot, db_path=db_path)
    assert legacy.read_text() == "original"


def test_snapshotting_does_not_prune(tmp_path):
    """R30: pruning never runs before the session it belongs to has committed."""
    root = tmp_path / "snaps"
    db_path = tmp_path / "master.db"
    sqlite3.connect(db_path).close()

    for index in range(8):
        W.snapshot_db(db_path, stamp=f"run{index}", root=root)

    assert len(list(root.iterdir())) == 8, "snapshotting pruned, which R30 forbids"


# ── retention, and what it must spare ────────────────────────────────────────


def _snapshot_dir(root: Path, name: str, order: int, *, real: bool = True) -> Path:
    directory = root / name
    directory.mkdir(parents=True)
    if real:
        (directory / "master.db").write_bytes(b"db")
    stamp = time.time() - 10_000 + order
    os.utime(directory, (stamp, stamp))
    return directory


def test_prunes_to_newest_five_and_spares_non_snapshots(tmp_path):
    """Retention itself, with the provider passed as None so the test stays hermetic."""
    snapshots = [_snapshot_dir(tmp_path, f"run{index}", index) for index in range(8)]
    bystander = _snapshot_dir(tmp_path, "not-a-snapshot", 0, real=False)

    pruned = W.prune_snapshots(tmp_path, keep=5, protected_provider=None)

    assert sorted(path.name for path in pruned) == ["run0", "run1", "run2"]
    assert all(not path.exists() for path in pruned)
    assert all(path.exists() for path in snapshots[3:])
    assert bystander.exists(), "a directory holding no database is not a snapshot"


def test_never_prunes_below_one_and_a_missing_root_is_a_no_op(tmp_path):
    assert W.prune_snapshots(tmp_path / "missing", protected_provider=None) == []
    only = _snapshot_dir(tmp_path, "only", 1)
    assert W.prune_snapshots(tmp_path, keep=1, protected_provider=None) == []
    assert only.exists()
    assert W.prune_snapshots(tmp_path, keep=0, protected_provider=None) == []
    assert only.exists()


def test_a_snapshot_a_non_terminal_run_references_survives_pruning(tmp_path):
    doomed = _snapshot_dir(tmp_path, "run0", 0)
    for index in range(1, 8):
        _snapshot_dir(tmp_path, f"run{index}", index)

    held = {(doomed / "master.db").resolve()}
    pruned = W.prune_snapshots(tmp_path, keep=5, protected_provider=lambda: held)

    assert doomed.exists(), "an open run's recovery point was deleted"
    assert sorted(path.name for path in pruned) == ["run1", "run2"]


def test_the_same_snapshot_is_released_once_its_run_reaches_a_terminal_state(tmp_path):
    """The other half. Protection that never releases is a store that never shrinks."""
    doomed = _snapshot_dir(tmp_path, "run0", 0)
    for index in range(1, 8):
        _snapshot_dir(tmp_path, f"run{index}", index)

    vocabulary = W.RunStateVocabulary()
    open_run = {vocabulary.state_key: "running", vocabulary.snapshot_key: str(doomed / "master.db")}
    closed_run = dict(open_run) | {vocabulary.state_key: sorted(vocabulary.terminal_states)[0]}

    def provider(records):
        return lambda: W.default_protected_snapshot_paths(records=records)

    assert W.prune_snapshots(tmp_path, keep=5, protected_provider=provider([open_run])) != []
    assert doomed.exists()

    pruned = W.prune_snapshots(tmp_path, keep=5, protected_provider=provider([closed_run]))
    assert doomed in pruned and not doomed.exists()


@pytest.mark.parametrize("terminal", sorted(W.RunStateVocabulary().terminal_states))
def test_every_declared_terminal_state_releases_its_snapshot(terminal):
    """Iterated from the vocabulary, since a hardcoded list once missed a real terminal state."""
    vocabulary = W.RunStateVocabulary()
    record = {vocabulary.state_key: terminal, vocabulary.snapshot_key: "/anywhere/master.db"}
    assert W.default_protected_snapshot_paths(records=[record]) == set()


def test_protection_matches_the_directory_as_well_as_the_database_inside_it(tmp_path):
    """Both, because a session log records the file and a person names the directory."""
    doomed = _snapshot_dir(tmp_path, "run0", 0)
    for index in range(1, 8):
        _snapshot_dir(tmp_path, f"run{index}", index)

    by_directory = {doomed.resolve()}
    assert W.prune_snapshots(tmp_path, keep=5, protected_provider=lambda: by_directory) != []
    assert doomed.exists()


def test_a_failing_protection_provider_deletes_nothing(tmp_path):
    """Fail safe. A transient error elsewhere must not cost a recovery point."""
    for index in range(8):
        _snapshot_dir(tmp_path, f"run{index}", index)

    def broken():
        raise RuntimeError("the run-state store is unreadable right now")

    assert W.prune_snapshots(tmp_path, keep=5, protected_provider=broken) == []
    assert len(list(tmp_path.iterdir())) == 8


def test_a_snapshot_directory_is_recognised_by_shape_not_by_filename(tmp_path):
    """The database's filename belongs to the user's rekordbox install, not to us."""
    named = tmp_path / "run0"
    named.mkdir()
    (named / "someone_elses_name.db").write_bytes(b"db")
    assert W.snapshot_database_in(named) == named / "someone_elses_name.db"
    assert W.snapshot_database_in(tmp_path / "run0" / "nothing-here") is None


# ── the default provider reads what the state inventory declares ─────────────


@pytest.fixture
def configured(tmp_path, monkeypatch):
    library = tmp_path / "library"
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    return config.from_dict(valid_data(library))


def test_the_default_provider_reads_the_directory_the_state_inventory_declares(configured):
    """Resolved through the inventory's own path builder, never a glob that can match nothing."""
    run_state_dir = config.state_path("session_log", configured)
    run_state_dir.mkdir(parents=True)
    vocabulary = W.RunStateVocabulary()
    (run_state_dir / "20260801_120000.json").write_text(
        json.dumps({vocabulary.state_key: "running", vocabulary.snapshot_key: "/snaps/a/master.db"})
    )

    assert W.default_protected_snapshot_paths(configured) == {Path("/snaps/a/master.db").resolve()}


def test_the_scan_is_bounded_to_the_run_state_directory(configured):
    """One directory, one level, never the whole state tree."""
    run_state_dir = config.state_path("session_log", configured)
    (run_state_dir / "nested").mkdir(parents=True)
    vocabulary = W.RunStateVocabulary()
    payload = json.dumps(
        {vocabulary.state_key: "running", vocabulary.snapshot_key: "/snaps/b/master.db"}
    )
    (run_state_dir / "nested" / "run.json").write_text(payload)

    assert W.default_protected_snapshot_paths(configured) == set()


def test_unreadable_and_malformed_records_are_skipped_not_fatal(configured):
    """One damaged file must not stop the scan protecting everything else."""
    run_state_dir = config.state_path("session_log", configured)
    run_state_dir.mkdir(parents=True)
    (run_state_dir / "broken.json").write_text("{not json")
    (run_state_dir / "list.json").write_text("[]")
    vocabulary = W.RunStateVocabulary()
    (run_state_dir / "good.json").write_text(
        json.dumps({vocabulary.state_key: "running", vocabulary.snapshot_key: "/snaps/c/master.db"})
    )

    assert W.default_protected_snapshot_paths(configured) == {Path("/snaps/c/master.db").resolve()}


def test_the_default_provider_protects_nothing_without_configuration():
    """It answers empty rather than raising, which would disable retention via the fail-safe."""
    assert W.default_protected_snapshot_paths() == set()


def test_the_session_log_declares_the_vocabulary_this_scan_reads():
    """The session log and this scan share one vocabulary, or protection lapses (U8, P5)."""
    session = importlib.import_module("cratekit.core.session")
    declared = getattr(session, "RUN_STATE_VOCABULARY", None)
    assert isinstance(declared, W.RunStateVocabulary), (
        "the session log must publish a RunStateVocabulary as RUN_STATE_VOCABULARY "
        "so the snapshot-protection scan reads the field names and terminal set "
        "that store actually writes, rather than the provisional defaults"
    )
    assert declared == W.RunStateVocabulary(), (
        "the writer's provisional vocabulary disagrees with the session log's. "
        "Update rb_writer.RunStateVocabulary's defaults to match, or pass the "
        "session log's instance into default_protected_snapshot_paths."
    )


def test_a_real_session_record_makes_its_capture_protected_from_pruning():
    """Derived, not compared: a real session record must make its capture protected."""
    session = importlib.import_module("cratekit.core.session")
    library = Path(os.environ["CRATEKIT_LIBRARY_ROOT"])
    (library / "db").mkdir(parents=True, exist_ok=True)
    cfg = config.from_dict(valid_data(library))

    capture_path = library / "captures" / "one" / "master.db"
    record = session.open_session(cfg, workflow="a-destructive-workflow")
    session.attach_capture(record, capture_path, cfg)

    assert W.default_protected_snapshot_paths(cfg) == {capture_path.resolve()}

    # A finished session RELEASES it. The volume seam is injected because a gated
    # close asserts the volume, which is not the question here.
    session.close_session(
        record,
        cfg,
        identity_provider=lambda _path: cfg.library.volume_id,
        mount_enumerator=lambda: (),
    )
    assert W.default_protected_snapshot_paths(cfg) == set()
