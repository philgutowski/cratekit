"""The snapshot half of the safety chain: capture, restore, and what pruning spares.

Three properties are guarded here, and each one is guarded because it failed in
the source system rather than because it looked important.

1. **The restore is write-ahead-log SYMMETRIC.** A snapshot captures the database
   file, its log, and its shared-memory index. A restore that put back only the
   database file while deleting the live sidecars silently reverted a snapshot
   taken with uncheckpointed frames to a pre-log state. Nothing raised. The
   library was simply older than the snapshot claimed, and only on the recovery
   path, which is the one path nobody rehearses.

2. **Pruning spares a snapshot an open run still references.** The source system
   claimed this in a comment and never did it: the scan globbed a filename its
   own run-state store never writes, read a status field that does not exist, and
   compared against a terminal set missing one of the two real values. Three
   independent mismatches, and every one of them fails the same silent way,
   because a scan that matches nothing returns nothing and pruning then deletes
   whatever it likes.

3. **Snapshotting does not prune.** The source pruned from inside the snapshot
   call, which put retention inside the write session, before the commit the
   snapshot exists to protect.

Fully hermetic: synthetic SQLite databases in a temporary directory, no library
volume, no rekordbox, no database key.
"""

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
from tests._pending import requires
from tests.test_config import valid_data


@pytest.fixture(autouse=True)
def _rekordbox_closed(monkeypatch):
    """Whether rekordbox happens to be running on this machine is irrelevant here.

    Patched in ``rb_writer`` itself, which is where the guards resolve the names.
    Patching a module that merely re-exports them rebinds nothing the guard reads,
    which is a mistake the source system's test suite records having made.
    """
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)


# ── the write-ahead-log round trip ───────────────────────────────────────────


def _wal_database_with_an_uncheckpointed_row(tmp_path: Path):
    """A database whose newest row lives only in an uncheckpointed log frame.

    The connection is left OPEN, and that is the point: it models rekordbox
    holding live frames at the instant a snapshot is taken, which is the only
    state in which the asymmetry bug is visible at all.
    """
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
    """Both sidecars are captured; only the log is put back.

    Asserted against the schema rather than against a literal pair, because a
    companion list maintained here is exactly the drift the declaration exists to
    remove, and the cost of that drift is a torn database.
    """
    assert set(W.db_sidecar_suffixes()) == {s.suffix for s in config.SQLITE_SIDECARS}
    assert set(W.restored_sidecar_suffixes()) == {
        s.suffix for s in config.SQLITE_SIDECARS if s.restored
    }
    assert set(W.restored_sidecar_suffixes()) < set(W.db_sidecar_suffixes())


def test_a_restore_never_puts_back_the_shared_memory_index(tmp_path):
    """The asymmetry, asserted directly rather than inferred from a round trip.

    The shared-memory index is derived from the log. Restoring a stale one beside
    a fresh log hands SQLite two disagreeing descriptions of one database, so it
    is captured (a capture must be complete) and never written back.
    """
    db_path, conn = _wal_database_with_an_uncheckpointed_row(tmp_path)
    snapshot = W.snapshot_db(db_path, stamp="s", root=tmp_path / "snaps")
    conn.close()

    assert (snapshot.with_name(snapshot.name + "-shm")).exists(), "the capture missed a sidecar"

    # Plant a live index that must not survive, and prove the restore cleared it
    # rather than replacing it with the snapshot's.
    live_shm = db_path.with_name(db_path.name + "-shm")
    live_shm.write_bytes(b"stale")
    W.restore_from_snapshot(snapshot, db_path=db_path)
    assert not live_shm.exists()


def test_the_legacy_playlist_file_travels_with_the_database(tmp_path):
    """It belongs to rekordbox, not to us, and it describes the database beside it.

    A restored database sitting next to a newer copy of this file describes two
    different libraries, which is why it is captured and put back even though it
    is not Cratekit state and has no row in the state inventory.
    """
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
    """R30: pruning never runs before the session it belongs to has committed.

    The source called pruning from inside the snapshot, which is inside the write
    session and therefore before the commit the snapshot protects. Retention is
    now a separate step a caller places after its own commit.
    """
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
    """Retention itself, with protection explicitly disabled.

    The provider is passed as None rather than left to default, which is the fix
    for a real defect in the ported test: calling the default provider reached
    into the developer's own runtime state, and it passed only because the broken
    scan found nothing. Fixing the scan would have made it non-hermetic.
    """
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
    """The plan's scenario, and the behaviour the source only ever claimed."""
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
    """Both of them, iterated from the vocabulary rather than named here.

    The source hardcoded five terminal values and MISSED one of the two the
    run-state store actually writes, so an abandoned run pinned its snapshot
    forever. Iterating the declaration is what makes that impossible to repeat.
    """
    vocabulary = W.RunStateVocabulary()
    record = {vocabulary.state_key: terminal, vocabulary.snapshot_key: "/anywhere/master.db"}
    assert W.default_protected_snapshot_paths(records=[record]) == set()


def test_protection_matches_the_directory_as_well_as_the_database_inside_it(tmp_path):
    """Both granularities, because two different callers record two different paths.

    The snapshot call returns the database file, which is what a session log
    records. A person reading a store by eye names the directory. Honouring only
    one of them makes protection depend on which one the caller happened to have.
    """
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
    """A real configuration pointing at a temporary library."""
    library = tmp_path / "library"
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    return config.from_dict(valid_data(library))


def test_the_default_provider_reads_the_directory_the_state_inventory_declares(configured):
    """Resolved through the inventory's own path builder, never through a glob.

    This is the fix for the defect that made protection a comment. The source
    typed one module's filename convention into another module, got it wrong, and
    nothing could tell, because a scan that matches nothing looks exactly like a
    scan that found nothing to protect.
    """
    run_state_dir = config.state_path("session_log", configured)
    run_state_dir.mkdir(parents=True)
    vocabulary = W.RunStateVocabulary()
    (run_state_dir / "20260801_120000.json").write_text(
        json.dumps({vocabulary.state_key: "running", vocabulary.snapshot_key: "/snaps/a/master.db"})
    )

    assert W.default_protected_snapshot_paths(configured) == {Path("/snaps/a/master.db").resolve()}


def test_the_scan_is_bounded_to_the_run_state_directory(configured):
    """One directory, one level. The source walked the whole state tree recursively.

    On a real installation that meant descending dozens of unrelated cache
    directories on every snapshot, to find a file that was never there.
    """
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
    """An unconfigured machine has no run-state store, so there is nothing to read.

    It answers empty rather than raising, because raising here would route into
    the pruning fail-safe and silently disable retention on every unconfigured
    machine.
    """
    assert W.default_protected_snapshot_paths() == set()


@requires("cratekit.core.session")
def test_the_session_log_declares_the_vocabulary_this_scan_reads():
    """The countdown on U8, written now so it cannot be forgotten later (P5).

    The writer cannot import the run-state store, so its vocabulary carries
    provisional defaults. The moment that store lands, this asserts the two
    agree. Without it, U8 could name its state field anything and protection
    would go back to being a comment, silently, exactly as it was before.
    """
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
