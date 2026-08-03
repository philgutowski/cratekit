"""U8's capture half: the database and its coupled state, taken as one set (KTD21b).

Four properties are asserted here, and each one is asserted because getting it
wrong is silent:

1. **The capture set is DERIVED.** Every path comes from the state inventory. A
   companion list in the capture unit is the drift the inventory exists to
   abolish, and its cost is a database copied without the committed transactions
   the storage engine is still holding outside the main file: a copy that opens
   cleanly and is quietly behind. ``tests/test_config.py`` already asserts this
   module reaches for the derivation and spells no file suffix of its own; what
   is asserted HERE is that the capture actually covers every declared source.

2. **Absence is a recorded outcome, not an error.** A database with nothing
   outstanding beside it, and a library that has never run a sweep, are both
   normal. The manifest has to say which sources were there, because a restore
   that cannot tell "nothing to put back" from "we never looked" will do the
   wrong one.

3. **Everything the capture creates is private under any umask** (P1). Asserted
   by WALKING the capture rather than by naming the files in it (P3): the version
   of that test which hand-listed two files missed a third written by the same
   code in the same directory, and stayed green.

4. **The integrity verdict is part of the record and it gates.** No session
   commits behind a capture that did not verify.

Fully hermetic: an ordinary file standing in for the database, a stand-in
verifier, and no library volume anywhere.
"""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path

import pytest

from cratekit.core import config, snapshot
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests.test_config import valid_data


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library whose database and coupled state exist on disk."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    resolved = config.from_dict(valid_data(library))
    config.state_path("rekordbox_db", resolved).write_bytes(b"a database")
    return resolved


@pytest.fixture(autouse=True)
def _permissive_umask():
    """Run with every permission bit available.

    The whole point of an explicit mode is that it does not depend on the
    process umask, and a test running under a restrictive one would pass without
    the code setting anything at all.
    """
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
    """Put a real file inside the coupled directory the inventory declares."""
    coupled = config.library_coupled_dir(cfg)
    coupled.mkdir(parents=True, exist_ok=True)
    marker = coupled / "declines.json"
    marker.write_text(json.dumps({"declined": ["one"]}))
    return marker


# ═══════════════════════════════════════════════════════════════════════════
# The set is derived, and it covers everything the inventory declares
# ═══════════════════════════════════════════════════════════════════════════


def test_every_declared_source_appears_in_the_capture_record(cfg):
    """P4. A derivation that covers most of the real set is a list in disguise.

    The assertion iterates ``snapshot_sources`` rather than naming the paths, so
    a coupled entry added to the inventory later is covered on the day it is
    added and nobody has to remember this file exists.
    """
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
    """The failure this prevents is a database missing everything still outstanding.

    The companion paths are composed by the inventory, so this test composes them
    the same way rather than spelling a suffix, which is the exact drift the
    schema removed.
    """
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
    """The runtime half of the check above, which the schema alone cannot give.

    The schema is asserted by ``tests/test_config.py``, and a schema assertion
    proves the DECLARATION is sound. This proves the capture refuses if it is
    ever handed a set that is not, which is the case that costs unbounded disk.
    """
    store = snapshot.store_root(cfg)
    monkeypatch.setattr(config, "snapshot_sources", lambda _cfg: (store.parent,))
    with pytest.raises(CratekitError) as excinfo:
        snapshot.capture(cfg, verifier=_passes)
    assert "nest" in excinfo.value.cause.message


# ═══════════════════════════════════════════════════════════════════════════
# Permissions, derived by walking (P1, P3)
# ═══════════════════════════════════════════════════════════════════════════


def test_every_file_and_directory_in_a_capture_is_private_under_any_umask(cfg):
    """A 0600 file inside a 0777 directory is not a private file.

    Directory write permission governs unlink and rename, so any local account
    can replace the file whatever its own mode says. Both are checked, and the
    set is derived by walking the capture rather than by listing what was copied.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The verdict is part of the record, and it gates
# ═══════════════════════════════════════════════════════════════════════════


def test_a_capture_that_verifies_is_the_only_one_anything_may_commit_behind(cfg):
    good = snapshot.capture(cfg, stamp="verified", verifier=_passes)
    assert good.verified
    snapshot.assert_verified(good)  # does not raise

    bad = snapshot.capture(cfg, stamp="unverified", verifier=_fails)
    assert not bad.verified
    with pytest.raises(CratekitError) as excinfo:
        snapshot.assert_verified(bad)
    assert excinfo.value.cause.reason == "snapshot-integrity-failed"


def test_a_verifier_that_raises_counts_as_not_having_verified(cfg):
    """Failing CLOSED, because the verdict gates the only undo a session has."""

    def explodes(_path):
        raise RuntimeError("the check itself broke")

    record = snapshot.capture(cfg, verifier=explodes)
    assert record.integrity_verified is False
    with pytest.raises(CratekitError):
        snapshot.assert_verified(record)


def test_the_verdict_survives_a_round_trip_through_the_manifest(cfg):
    record = snapshot.capture(cfg, verifier=_fails)
    reread = snapshot.read_manifest(record.root)
    assert reread.integrity_verified is False
    assert reread.stamp == record.stamp
    assert reread.database == record.database
    assert not reread.verified


# ═══════════════════════════════════════════════════════════════════════════
# Stamps, manifests, and the things that refuse
# ═══════════════════════════════════════════════════════════════════════════


def test_a_stamp_is_sortable_and_carries_no_character_a_filesystem_rejects():
    first = snapshot.new_stamp()
    assert ":" not in first and " " not in first and "/" not in first
    assert first != snapshot.new_stamp(), "two stamps in one second collided"


def test_a_stamps_random_tail_is_sixty_four_bits():
    """The tail is an IDENTITY, not decoration, and its width is pinned as one.

    ``restore`` derives one staged-companion directory per ATTEMPT from this
    string, and a restore repeated after a failure runs several attempts inside
    one second, so the second-resolution prefix is identical across them and the
    whole of the distinctness rests on the tail. A collision has one attempt's
    ``os.replace`` put its write-ahead log over another's, and those bytes are in
    no capture: it is precisely the loss the staging exists to prevent. At the
    original sixteen bits a run of eight attempts collides about once in two
    thousand runs, which is a rate a person meets.

    Written as a LITERAL sixteen hexadecimal characters rather than as
    ``len(secrets.token_hex(n))``, because an expected value computed from the
    thing under test is an assertion that passes at every width.
    """
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{6}Z-[0-9a-f]{16}", snapshot.new_stamp())


def test_a_sparse_file_is_charged_the_room_its_copy_will_actually_need(tmp_path):
    """``ALLOCATION_UNIT`` is observable on exactly one shape, so drive that shape.

    ``_allocated_file`` returns the larger of ``st_blocks * 512`` and the length
    rounded up to :data:`snapshot.ALLOCATION_UNIT`. For an ordinary file on a
    filesystem whose block size is also 4,096 those two agree, which is why the
    constant survived being changed to 1 with nothing red. They differ only for a
    SPARSE file, whose ``st_blocks`` under-reports what the destination will
    occupy because this module's copier does not preserve holes, and that is the
    case the ``max`` exists for.

    The length is deliberately not a multiple of the unit: at 10 MiB exactly, both
    candidate answers are the same number and the test would prove nothing.
    """
    sparse = tmp_path / "sparse.bin"
    with sparse.open("wb") as handle:
        handle.truncate(10 * 1024 * 1024 + 1)
    assert sparse.stat().st_blocks * 512 < sparse.stat().st_size, (
        "this filesystem did not make a sparse file, so there is nothing here for "
        "the rounding term to be larger than"
    )

    # 10,485,761 bytes rounds up to 2,561 units of 4,096, which is 10,489,856,
    # plus one directory entry. With the unit at 1 the answer is 10,485,761.
    assert snapshot.incoming_bytes(sparse) == 10489856 + snapshot.DIRECTORY_ENTRY_OVERHEAD
    assert snapshot.freed_bytes(sparse) == 10489856


def test_writing_a_second_capture_into_an_existing_stamp_refuses(cfg):
    snapshot.capture(cfg, stamp="same", verifier=_passes)
    with pytest.raises(CratekitError) as excinfo:
        snapshot.capture(cfg, stamp="same", verifier=_passes)
    assert excinfo.value.cause.code is ExitCode.INTERNAL


def test_a_missing_database_refuses_in_the_library_class_rather_than_crashing(cfg):
    config.state_path("rekordbox_db", cfg).unlink()
    with pytest.raises(CratekitError) as excinfo:
        snapshot.capture(cfg, verifier=_passes)
    assert excinfo.value.cause.code is ExitCode.LIBRARY_UNAVAILABLE


def test_an_unreadable_manifest_refuses_rather_than_reporting_an_empty_capture(cfg):
    record = snapshot.capture(cfg, verifier=_passes)
    (record.root / snapshot.MANIFEST_NAME).write_text("{not json")
    with pytest.raises(CratekitError):
        snapshot.read_manifest(record.root)


def test_a_manifest_from_a_later_build_is_refused_rather_than_guessed_at(cfg):
    record = snapshot.capture(cfg, verifier=_passes)
    path = record.root / snapshot.MANIFEST_NAME
    data = json.loads(path.read_text())
    data["schema_version"] = snapshot.MANIFEST_SCHEMA_VERSION + 1
    path.write_text(json.dumps(data))
    with pytest.raises(CratekitError):
        snapshot.read_manifest(record.root)


def test_a_capture_is_a_snapshot_directory_as_far_as_pruning_is_concerned(cfg):
    """The capture and the retention it is protected by must agree on what one IS.

    Pruning finds a capture by looking for a database file inside a directory. A
    capture layout that put the database somewhere else would be invisible to
    retention, which sounds safe and is not: an invisible capture is also one
    nothing can spare deliberately.
    """
    from cratekit.core import rb_writer

    record = snapshot.capture(cfg, verifier=_passes)
    assert rb_writer.snapshot_database_in(record.root) == record.database
