"""U8's capture half: the database and its coupled state, taken as one set (KTD21b).

The set is derived from the state inventory, absence is recorded rather than an
error, everything created is private under any umask (P1, P3), and the integrity
verdict gates."""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path

import pytest

from cratekit.core import config, snapshot
from cratekit.core.exit_codes import ExitCode
from tests.test_config import valid_data
from tests.test_restore import _refusal


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    resolved = config.from_dict(valid_data(library))
    config.state_path("rekordbox_db", resolved).write_bytes(b"a database")
    return resolved


@pytest.fixture(autouse=True)
def _permissive_umask():
    """Run with every permission bit available, so only an explicit mode passes."""
    previous = os.umask(0)
    try:
        yield
    finally:
        os.umask(previous)


def _passes(_path):
    return True


def _fails(_path):
    return False


def _write_coupled_state(cfg) -> Path:
    coupled = config.library_coupled_dir(cfg)
    coupled.mkdir(parents=True, exist_ok=True)
    marker = coupled / "declines.json"
    marker.write_text(json.dumps({"declined": ["one"]}))
    return marker


# The set is derived, and it covers everything the inventory declares


def test_every_declared_source_appears_in_the_capture_record(cfg):
    """P4: iterates ``snapshot_sources``, so a later inventory entry is covered the day it lands."""
    _write_coupled_state(cfg)
    record = snapshot.capture(cfg, verifier=_passes)

    recorded = {entry.source for entry in record.sources}
    for source in config.snapshot_sources(cfg):
        assert source in recorded, f"{source} is a declared source and was not captured"


def test_the_database_and_the_coupled_directory_land_under_one_stamp(cfg):
    marker = _write_coupled_state(cfg)
    record = snapshot.capture(cfg, verifier=_passes)

    database = config.state_path("rekordbox_db", cfg)
    assert record.database == record.root / database.name
    assert record.database.read_bytes() == b"a database"

    coupled = config.library_coupled_dir(cfg)
    landed = record.root / coupled.name / marker.name
    assert landed.read_text() == marker.read_text()
    assert record.root.parent == snapshot.store_root(cfg)


def test_the_files_the_engine_keeps_beside_the_database_travel_with_it(cfg):
    """The engine's companion files travel with it, composed by the inventory, never a suffix."""
    written = []
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"outstanding")
        written.append(companion)
    assert written, "the inventory declares no companion files, so this proves nothing"

    record = snapshot.capture(cfg, verifier=_passes)
    for companion in written:
        assert (record.root / companion.name).read_bytes() == b"outstanding"


def test_an_absent_source_is_recorded_as_absent_rather_than_failing(cfg):
    """A checkpointed database has nothing beside it, and that is normal."""
    record = snapshot.capture(cfg, verifier=_passes)

    absent = [entry for entry in record.sources if not entry.present]
    assert absent, "nothing was absent, so this asserts nothing about absence"
    for entry in absent:
        assert entry.captured is None
        assert not entry.source.exists()

    reread = snapshot.read_manifest(record.root)
    assert {e.source for e in reread.sources if not e.present} == {
        e.source for e in absent
    }


def test_the_capture_store_is_never_captured_by_a_capture(cfg):
    """Otherwise the tenth capture costs the sum of the first nine, forever."""
    store = snapshot.store_root(cfg)
    for source in config.snapshot_sources(cfg):
        assert source != store
        assert store not in source.parents
        assert source not in store.parents

    record = snapshot.capture(cfg, verifier=_passes)
    assert not (record.root / store.name).exists()


def test_a_source_that_would_nest_the_store_refuses(cfg, monkeypatch):
    """The runtime half of the schema check, refusing a set that would nest the store."""
    store = snapshot.store_root(cfg)
    monkeypatch.setattr(config, "snapshot_sources", lambda _cfg: (store.parent,))
    cause = _refusal(snapshot.capture, cfg, verifier=_passes)
    assert "nest" in cause.message


# Permissions, derived by walking (P1, P3)


def test_every_file_and_directory_in_a_capture_is_private_under_any_umask(cfg):
    """Directories too, since directory write permission lets any account replace a 0600 file."""
    _write_coupled_state(cfg)
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"outstanding")
    record = snapshot.capture(cfg, verifier=_passes)

    checked = 0
    for current, directories, files in os.walk(record.root):
        here = Path(current)
        for name in directories:
            mode = stat.S_IMODE((here / name).stat().st_mode)
            assert mode == config.PRIVATE_DIR_MODE, f"{here / name} is {oct(mode)}"
            checked += 1
        for name in files:
            mode = stat.S_IMODE((here / name).stat().st_mode)
            assert mode == config.PRIVATE_FILE_MODE, f"{here / name} is {oct(mode)}"
            checked += 1
    assert checked >= 3, "the walk found almost nothing, so it is the walk that is broken"
    assert stat.S_IMODE(record.root.stat().st_mode) == config.PRIVATE_DIR_MODE


def test_a_world_readable_source_does_not_produce_a_world_readable_capture(cfg):
    """The copier preserves the SOURCE's bits, and a rekordbox database is not private."""
    database = config.state_path("rekordbox_db", cfg)
    os.chmod(database, 0o666)
    record = snapshot.capture(cfg, verifier=_passes)
    assert stat.S_IMODE(record.database.stat().st_mode) == config.PRIVATE_FILE_MODE


# The verdict is part of the record, and it gates


def test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind(cfg):
    good = snapshot.capture(cfg, stamp="verified", verifier=_passes)
    assert good.verified
    snapshot.assert_verified(good)  # does not raise

    bad = snapshot.capture(cfg, stamp="unverified", verifier=_fails)
    assert not bad.verified
    cause = _refusal(snapshot.assert_verified, bad)
    assert cause.reason == "snapshot-integrity-failed"


def test_a_verifier_that_raises_counts_as_not_having_verified(cfg):
    """Failing CLOSED, because the verdict gates the only undo a session has."""

    def explodes(_path):
        raise RuntimeError("the check itself broke")

    record = snapshot.capture(cfg, verifier=explodes)
    assert record.integrity_verified is False
    _refusal(snapshot.assert_verified, record)


def test_the_verdict_survives_a_round_trip_through_the_manifest(cfg):
    record = snapshot.capture(cfg, verifier=_fails)
    reread = snapshot.read_manifest(record.root)
    assert reread.integrity_verified is False
    assert reread.stamp == record.stamp
    assert reread.database == record.database
    assert not reread.verified


# Stamps, manifests, and the things that refuse


def test_a_stamp_is_sortable_and_carries_no_character_a_filesystem_rejects():
    first = snapshot.new_stamp()
    assert ":" not in first and " " not in first and "/" not in first
    assert first != snapshot.new_stamp(), "two stamps in one second collided"


def test_a_stamps_random_tail_is_sixty_four_bits():
    """The tail alone keeps restore attempts in one second apart, so its width is a LITERAL."""
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{6}Z-[0-9a-f]{16}", snapshot.new_stamp())


def test_a_sparse_file_is_charged_the_room_its_copy_will_actually_need(tmp_path):
    """Only a sparse file shows ``ALLOCATION_UNIT``, as its ``st_blocks`` under-reports the copy."""
    sparse = tmp_path / "sparse.bin"
    with sparse.open("wb") as handle:
        handle.truncate(10 * 1024 * 1024 + 1)
    assert sparse.stat().st_blocks * 512 < sparse.stat().st_size, (
        "this filesystem did not make a sparse file, so there is nothing here for "
        "the rounding term to be larger than"
    )

    # 2,561 units of 4,096 plus one 2,048-byte directory entry, a LITERAL so it pins
    # the constants rather than reading them.
    assert snapshot.incoming_bytes(sparse) == 10491904
    assert snapshot.freed_bytes(sparse) == 10489856


def test_writing_a_second_capture_into_an_existing_stamp_refuses(cfg):
    snapshot.capture(cfg, stamp="same", verifier=_passes)
    cause = _refusal(snapshot.capture, cfg, stamp="same", verifier=_passes)
    assert cause.code is ExitCode.INTERNAL


def test_a_missing_database_refuses_in_the_library_class_rather_than_crashing(cfg):
    config.state_path("rekordbox_db", cfg).unlink()
    cause = _refusal(snapshot.capture, cfg, verifier=_passes)
    assert cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_an_unreadable_manifest_refuses_rather_than_reporting_an_empty_capture(cfg):
    record = snapshot.capture(cfg, verifier=_passes)
    (record.root / snapshot.MANIFEST_NAME).write_text("{not json")
    _refusal(snapshot.read_manifest, record.root)


def test_a_manifest_from_a_later_build_is_refused_rather_than_guessed_at(cfg):
    record = snapshot.capture(cfg, verifier=_passes)
    path = record.root / snapshot.MANIFEST_NAME
    data = json.loads(path.read_text())
    data["schema_version"] = snapshot.MANIFEST_SCHEMA_VERSION + 1
    path.write_text(json.dumps(data))
    _refusal(snapshot.read_manifest, record.root)


def test_a_capture_is_a_snapshot_directory_as_far_as_pruning_is_concerned(cfg):
    """Pruning must see a capture as a snapshot, or nothing could spare it deliberately."""
    from cratekit.core import rb_writer

    record = snapshot.capture(cfg, verifier=_passes)
    assert rb_writer.snapshot_database_in(record.root) == record.database
