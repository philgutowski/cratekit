"""A capture of a database in write ahead log mode is one the restore can use (R-1665).

The capture records which of the engine's companion files it took by looking
at the capture directory, and the integrity check then opened that same
directory through the binding. Closing the check's handle was the last close
of the copy, so SQLite folded the log into the captured database and deleted
the captured log and its shared memory index. The manifest still listed both,
so ``restore.plan`` refused the capture as missing two files, and the undo of
the guarded write it was taken for could not run.

Two layers hold it now, and each is asserted here on its own:

1. **The check never opens the capture** (``rb_writer.integrity_ok``). It reads
   a private throwaway copy of the file set it is given, so what it checks is
   the capture's bytes and what it changes on close is only the copy's.
2. **A capture never records verified over a source the check changed or
   removed** (``snapshot.capture``). Whatever verifier ran, a manifest that
   says verified lists only bytes that are still there as they were copied.

Driven on the suite's real disposable database, which is built in WAL mode
because the real library runs in it, with the real check. No library volume,
no rekordbox, no live database.
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

import pytest

from cratekit.core import config, restore, session, snapshot
from cratekit.core import rb_writer as W
from cratekit.core.cause import CratekitError
from tests import test_rb_writer_db as fixture
from tests.test_restore import acknowledge, gate_seams


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A saved library whose database is the suite's real WAL disposable database."""
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
    fixture._build_disposable_database(config.state_path("rekordbox_db", built))
    return built


@pytest.fixture(autouse=True)
def _nothing_is_running(monkeypatch):
    """No rekordbox, injected in every place a probe is resolved."""
    from pyrekordbox.db6 import database as binding

    monkeypatch.setattr("cratekit.core.processes.running_process_names", lambda: ())
    monkeypatch.setattr(W, "rekordbox_running", lambda: False)
    monkeypatch.setattr(W, "rekordbox_agent_running", lambda: False)
    monkeypatch.setattr(binding, "get_rekordbox_pid", lambda *args, **kwargs: 0)


@pytest.fixture(autouse=True)
def _cloud_sync_off(monkeypatch):
    monkeypatch.setattr(
        W, "read_rekordbox_settings", lambda *args, **kwargs: {W.LIBRARY_SYNC_SETTING: 0}
    )


@pytest.fixture(autouse=True)
def _release_process_locks():
    yield
    session._HELD.clear()


def _database(cfg) -> Path:
    return config.state_path("rekordbox_db", cfg)


def _first_id(path: Path) -> str:
    conn = sqlite3.connect(path)
    try:
        return str(conn.execute("SELECT ID FROM djmdContent ORDER BY ID LIMIT 1").fetchone()[0])
    finally:
        conn.close()


def _title(path: Path, content_id: str) -> str:
    conn = sqlite3.connect(path)
    try:
        return str(
            conn.execute("SELECT Title FROM djmdContent WHERE ID = ?", (content_id,)).fetchone()[0]
        )
    finally:
        conn.close()


def _retitle(conn: sqlite3.Connection, content_id: str, title: str) -> None:
    conn.execute("UPDATE djmdContent SET Title = ? WHERE ID = ?", (title, content_id))
    conn.commit()


def _sidecar(path: Path, suffix: str) -> Path:
    return path.with_name(path.name + suffix)


def _digests(directory: Path) -> dict[str, str]:
    return {
        name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
        for name in sorted(os.listdir(directory))
        if (directory / name).is_file()
    }


def _close_into_a_session(cfg, captured: snapshot.Capture) -> session.SessionRecord:
    """Attach the capture to a session that committed and closed, as a write does."""
    record = session.open_session(cfg, workflow="library-sweep", sources=("source-a",))
    session.attach_capture(record, captured.root, cfg)
    record.sources["source-a"] = str(session.SourceState.COMMITTED)
    record.state = session.SessionState.CLOSED
    record.ended = "2026-08-02T00:00:00+00:00"
    session.write_record(record, cfg)
    return record


def _restore(cfg, record: session.SessionRecord) -> None:
    acknowledge(cfg)
    with restore.recovery_session(cfg, **gate_seams(cfg)) as held:
        decided = restore.plan(cfg, record.session_id, held=held)
        restore.run(decided, cfg, held=held)


# ═══════════════════════════════════════════════════════════════════════════
# The card's scenario: a WAL database with a handle open, the real check
# ═══════════════════════════════════════════════════════════════════════════


def test_a_capture_taken_while_a_handle_holds_the_log_restores_what_it_recorded(cfg):
    """The row only the log holds at the capture comes back, through plan and run.

    The caller's connection keeps the log from folding, so the newest title
    exists only in the captured ``-wal``. Before the fix the check's close
    deleted that file from the capture and the plan refused the capture.
    """
    database = _database(cfg)
    content = _first_id(database)
    live = sqlite3.connect(database)
    try:
        live.execute("PRAGMA wal_autocheckpoint=0")
        _retitle(live, content, "only in the log")
        assert _sidecar(database, "-wal").stat().st_size > 0, "nothing was left in the log"

        captured = snapshot.capture(cfg)
    finally:
        live.close()

    assert captured.verified, "the real check did not pass a sound capture"
    on_disk = {entry.captured for entry in captured.sources if entry.present}
    assert _sidecar(captured.database, "-wal") in on_disk
    assert all(path.exists() for path in on_disk), "the manifest lists a file the capture lost"

    record = _close_into_a_session(cfg, captured)
    conn = sqlite3.connect(database)
    try:
        _retitle(conn, content, "written by the session")
    finally:
        conn.close()

    _restore(cfg, record)

    assert _title(database, content) == "only in the log"


def test_a_capture_taken_through_the_callers_own_handle_restores(cfg):
    """The ordinary call shape: the caller's open handle, its fold run first.

    The fold truncates the log rather than removing it, so the capture still
    holds an empty log and the index beside the database, and the check's close
    used to delete both from the capture all the same.
    """
    database = _database(cfg)
    handle = W.open_db(database)
    try:
        assert _sidecar(database, "-wal").exists(), "the open handle kept no log"
        captured = snapshot.capture(cfg, db=handle)
    finally:
        W.close_db(handle)

    assert captured.verified
    present = [entry for entry in captured.sources if entry.present]
    assert any(entry.captured == _sidecar(captured.database, "-wal") for entry in present)
    assert all(entry.captured.exists() for entry in present)

    record = _close_into_a_session(cfg, captured)
    _restore(cfg, record)
    assert W.integrity_ok(database)


def test_the_check_leaves_the_capture_exactly_as_it_was_copied(cfg, monkeypatch):
    """What is captured is what was copied: the check reads, and changes nothing."""
    seen: dict[str, dict[str, str]] = {}
    real = W.integrity_ok

    def watched(path, **kwargs):
        directory = Path(path).parent
        seen["before"] = _digests(directory)
        answer = real(path, **kwargs)
        seen["after"] = _digests(directory)
        return answer

    monkeypatch.setattr(W, "integrity_ok", watched)
    database = _database(cfg)
    live = sqlite3.connect(database)
    try:
        live.execute("PRAGMA wal_autocheckpoint=0")
        _retitle(live, _first_id(database), "only in the log")
        captured = snapshot.capture(cfg)
    finally:
        live.close()

    assert captured.verified
    assert seen["before"] == seen["after"]
    assert {database.name + "-wal", database.name + "-shm"} <= set(seen["after"])


def test_the_captured_database_still_verifies_after_the_capture(cfg):
    """The check can be asked again of the capture, and answers the same."""
    database = _database(cfg)
    live = sqlite3.connect(database)
    try:
        live.execute("PRAGMA wal_autocheckpoint=0")
        _retitle(live, _first_id(database), "only in the log")
        captured = snapshot.capture(cfg)
    finally:
        live.close()

    assert captured.verified
    assert W.integrity_ok(captured.database) is True
    assert W.integrity_ok(captured.database) is True
    assert _sidecar(captured.database, "-wal").exists()


def test_a_database_in_rollback_journal_mode_captures_and_restores_as_before(cfg):
    """The control: no log, nothing beside the database, nothing changes."""
    database = _database(cfg)
    conn = sqlite3.connect(database)
    try:
        assert conn.execute("PRAGMA journal_mode=DELETE").fetchone()[0] == "delete"
    finally:
        conn.close()
    content = _first_id(database)

    captured = snapshot.capture(cfg)

    assert captured.verified
    companions = {_sidecar(database, suffix) for suffix in W.db_sidecar_suffixes()}
    assert all(not entry.present for entry in captured.sources if entry.source in companions)
    before = _title(database, content)
    record = _close_into_a_session(cfg, captured)
    conn = sqlite3.connect(database)
    try:
        _retitle(conn, content, "written by the session")
    finally:
        conn.close()

    _restore(cfg, record)

    assert _title(database, content) == before


# ═══════════════════════════════════════════════════════════════════════════
# Layer one: the check reads a throwaway copy
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("encrypted", [False, True], ids=["plain", "encrypted"])
def test_the_check_changes_nothing_in_the_file_set_it_is_given(cfg, tmp_path, encrypted):
    database = _database(cfg)
    if encrypted:
        fixture._encrypt_in_place(database)
    live = sqlite3.connect(database) if not encrypted else None
    try:
        if live is not None:
            live.execute("PRAGMA wal_autocheckpoint=0")
            _retitle(live, _first_id(database), "only in the log")
        copied = W.snapshot_db(database, stamp="s", root=tmp_path / "snaps")
    finally:
        if live is not None:
            live.close()
    before = _digests(copied.parent)

    assert W.integrity_ok(copied) is True
    assert _digests(copied.parent) == before


def test_a_damaged_copy_still_fails_the_check(cfg, tmp_path):
    """The throwaway copy carries the damage, so the verdict is still about these bytes."""
    copied = W.snapshot_db(_database(cfg), stamp="s", root=tmp_path / "snaps")
    conn = sqlite3.connect(copied)
    try:
        (size,) = conn.execute("PRAGMA page_size").fetchone()
        (root,) = conn.execute(
            "SELECT rootpage FROM sqlite_master WHERE name = 'djmdContent'"
        ).fetchone()
    finally:
        conn.close()
    raw = bytearray(copied.read_bytes())
    # The table's root page given a type byte no b-tree page carries.
    raw[(root - 1) * size] = 0x07
    copied.write_bytes(bytes(raw))

    assert W.integrity_ok(copied) is False


def test_a_check_whose_copy_cannot_be_made_has_not_passed(cfg, tmp_path, monkeypatch):
    copied = W.snapshot_db(_database(cfg), stamp="s", root=tmp_path / "snaps")

    def no_room(*_args, **_kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(W, "_copy_file_set", no_room)

    assert W.integrity_ok(copied) is False


def test_the_check_removes_its_throwaway_copy(cfg, tmp_path, monkeypatch):
    made: list[Path] = []
    real = W._copy_file_set

    def recorded(source, destination):
        made.append(Path(destination))
        return real(source, destination)

    monkeypatch.setattr(W, "_copy_file_set", recorded)
    copied = W.snapshot_db(_database(cfg), stamp="s", root=tmp_path / "snaps")
    made.clear()

    assert W.integrity_ok(copied) is True
    assert made, "the check did not copy"
    assert not made[0].exists()
    assert made[0] != copied.parent


# ═══════════════════════════════════════════════════════════════════════════
# Layer two: nothing records verified over what the check changed
# ═══════════════════════════════════════════════════════════════════════════


def _hermetic(tmp_path, monkeypatch):
    """A capture with an ordinary file standing in for the database and both companions."""
    from tests.test_config import valid_data

    library = tmp_path / "hermetic"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    resolved = config.from_dict(valid_data(library))
    database = config.state_path("rekordbox_db", resolved)
    database.write_bytes(b"a database")
    for suffix in W.db_sidecar_suffixes():
        _sidecar(database, suffix).write_bytes(b"a companion")
    return resolved


@pytest.mark.parametrize("suffix", ["-wal", "-shm"])
def test_a_check_that_removes_a_captured_companion_is_not_recorded_verified(
    tmp_path, monkeypatch, suffix
):
    resolved = _hermetic(tmp_path, monkeypatch)

    def removes(database):
        _sidecar(Path(database), suffix).unlink()
        return True

    captured = snapshot.capture(resolved, verifier=removes)

    assert not captured.verified
    assert snapshot.read_manifest(captured.root).integrity_verified is False
    with pytest.raises(CratekitError) as excinfo:
        snapshot.assert_verified(captured)
    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


def test_a_check_that_rewrites_the_captured_database_is_not_recorded_verified(
    tmp_path, monkeypatch
):
    resolved = _hermetic(tmp_path, monkeypatch)

    def rewrites(database):
        Path(database).write_bytes(b"a database the check changed")
        return True

    captured = snapshot.capture(resolved, verifier=rewrites)

    assert not captured.verified


def test_a_check_that_removes_a_captured_coupled_file_is_not_recorded_verified(
    tmp_path, monkeypatch
):
    resolved = _hermetic(tmp_path, monkeypatch)
    coupled = config.library_coupled_dir(resolved)
    coupled.mkdir(parents=True, exist_ok=True)
    (coupled / "declines.json").write_text(json.dumps({"declined": ["one"]}))

    def removes(database):
        for entry in Path(database).parent.iterdir():
            if entry.is_dir():
                for child in entry.iterdir():
                    child.unlink()
                entry.rmdir()
                return True
        raise AssertionError("the capture held no coupled directory")

    captured = snapshot.capture(resolved, verifier=removes)

    assert not captured.verified


def test_a_check_that_leaves_the_capture_alone_is_recorded_verified(tmp_path, monkeypatch):
    """The control for the three above: the guard refuses changes, not checks."""
    resolved = _hermetic(tmp_path, monkeypatch)

    captured = snapshot.capture(resolved, verifier=lambda _database: True)

    assert captured.verified
    assert snapshot.read_manifest(captured.root).integrity_verified is True
