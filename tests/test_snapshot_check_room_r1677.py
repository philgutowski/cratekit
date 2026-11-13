"""The integrity check's throwaway copy is measured, and named when it has no room (R-1677).

Since R-1665 the check never opens the capture: it copies the database's file
set into the system's temporary directory and checks the copy. Nothing
measured the room that copy needs, and a temporary volume too small for it
made the check answer False, so the capture was recorded unverified and every
guarded write refused it as a capture that failed its integrity check, with
the remedy to report a defect. Nothing was wrong with the capture.

Two layers hold it now, and each is asserted here on its own:

1. **Measured before the copy** (``snapshot.assert_room_for_check``). When the
   real check will run, the capture measures the temporary volume before
   anything is written, beside the room for the capture itself, and counts
   both when they share one volume.
2. **Named when it still happens** (``rb_writer.integrity_ok`` with
   ``raise_copy_failure``). A throwaway copy that fails for lack of room
   refuses under the same slug, with the manifest saying not verified.

What never changes: a capture whose check did not complete is never recorded
verified, and a real integrity failure is never told as a room message.

Driven on the suite's real disposable database with the real check. No
library volume, no rekordbox, no live database.
"""

# ruff: noqa: F811, the fixtures below are imported from the R-1665 suite by name

from __future__ import annotations

import errno
import json
import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

from cratekit.core import config, snapshot
from cratekit.core import rb_writer as W
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode, Remedy
from tests.test_snapshot_wal_r1665 import (  # noqa: F401 - fixtures, used by name
    _cloud_sync_off,
    _nothing_is_running,
    _release_process_locks,
    cfg,
)

ROOM = "snapshot-check-temp-full"


@pytest.fixture
def scratch(tmp_path, monkeypatch) -> Path:
    """The temporary directory the throwaway copy goes in, made private to the test."""
    directory = tmp_path / "scratch"
    directory.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(directory))
    return directory


def _free_on(monkeypatch, where: Path, free: int | None, *, elsewhere: int | None = None) -> None:
    """Answer ``free`` for the volume holding ``where``, and the truth or ``elsewhere`` otherwise."""
    real = snapshot._free_bytes

    def answered(root: Path) -> int | None:
        if Path(root) == where or where in Path(root).parents:
            return free
        return real(root) if elsewhere is None else elsewhere

    monkeypatch.setattr(snapshot, "_free_bytes", answered)


def _separate_volumes(monkeypatch) -> None:
    monkeypatch.setattr(snapshot, "_same_volume", lambda _a, _b: False)


def _database(cfg) -> Path:
    return config.state_path("rekordbox_db", cfg)


def _check_needs(cfg) -> int:
    return sum(snapshot._allocated_size(path) for path in W.file_set(_database(cfg)))


def _stores(cfg) -> list[Path]:
    root = snapshot.store_root(cfg)
    return sorted(root.iterdir()) if root.exists() else []


def _no_room_in(scratch: Path, monkeypatch, code: int = errno.ENOSPC) -> None:
    """The throwaway copy fails as a full volume fails it; every other copy is real."""
    real = W._copy_file_set

    def copying(source, destination):
        if scratch == Path(destination) or scratch in Path(destination).parents:
            raise OSError(code, "No space left on device")
        return real(source, destination)

    monkeypatch.setattr(W, "_copy_file_set", copying)


# ═══════════════════════════════════════════════════════════════════════════
# Layer one: measured before anything is written
# ═══════════════════════════════════════════════════════════════════════════


def test_a_temporary_volume_too_small_for_the_check_refuses_before_anything_is_written(
    cfg, scratch, monkeypatch
):
    """The card's scenario: refused under the room slug, naming the volume and its room."""
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, 1000)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    cause = refused.value.cause
    assert cause.reason == ROOM
    assert str(scratch) in cause.message
    assert "1000 bytes free" in cause.message
    assert "integrity check" in cause.message
    assert cause.detail["root"] == str(scratch)
    assert cause.detail["free_bytes"] == 1000
    assert cause.detail["required_bytes"] == int(_check_needs(cfg) * snapshot.CAPACITY_HEADROOM)
    assert _stores(cfg) == [], "a capture directory was made before the refusal"
    assert list(scratch.iterdir()) == [], "a throwaway copy was made before the refusal"


def test_the_room_refusal_is_a_precondition_not_a_defect(cfg, scratch, monkeypatch):
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, 0)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    assert refused.value.cause.code == ExitCode.PRECONDITION
    assert refused.value.cause.remediation.remedy != Remedy.REPORT_DEFECT
    assert "TMPDIR" in " ".join(refused.value.cause.remediation.steps)


def test_a_temporary_volume_that_will_not_report_its_room_refuses(cfg, scratch, monkeypatch):
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, None)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    assert refused.value.cause.reason == ROOM
    assert str(scratch) in refused.value.cause.message
    assert _stores(cfg) == []


def test_exactly_enough_room_on_the_temporary_volume_captures_verified(cfg, scratch, monkeypatch):
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, int(_check_needs(cfg) * snapshot.CAPACITY_HEADROOM))

    captured = snapshot.capture(cfg)

    assert captured.verified


def test_one_byte_short_on_the_temporary_volume_refuses(cfg, scratch, monkeypatch):
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, int(_check_needs(cfg) * snapshot.CAPACITY_HEADROOM) - 1)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    assert refused.value.cause.reason == ROOM


def test_the_measure_counts_every_file_the_check_copies_not_the_database_alone(
    cfg, scratch, monkeypatch
):
    """The playlist file and any companion ride along with the copy, so they are measured.

    Room for the database alone, with the file the binding saves beside it
    left out, is a copy that runs out part way.
    """
    database = _database(cfg)
    (database.parent / W.MASTER_PLAYLIST_XML).write_bytes(b"<playlists/>" * 8192)
    alone = int(snapshot._allocated_size(database) * snapshot.CAPACITY_HEADROOM)
    whole = int(_check_needs(cfg) * snapshot.CAPACITY_HEADROOM)
    assert whole - 1 > alone, "the playlist file is too small to tell the two apart"
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, whole - 1)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    assert refused.value.cause.reason == ROOM
    assert refused.value.cause.detail["estimated_bytes"] == _check_needs(cfg)


def test_a_temporary_volume_with_room_captures_verified_and_leaves_nothing(cfg, scratch):
    """Unchanged where there is room: the real check ran, passed, and cleaned up."""
    captured = snapshot.capture(cfg)

    assert captured.verified
    assert list(scratch.iterdir()) == []


def test_a_temporary_volume_shared_with_the_store_must_hold_both(cfg, scratch, monkeypatch):
    """The capture and its throwaway land on one volume, so the room is for both.

    Room for either alone, as two separate questions would each answer, is not
    room for the two, and the throwaway is copied after the capture is.
    """
    capture_needs = snapshot.assert_room_for_capture(cfg, free_bytes=1 << 60)
    both = int((capture_needs + _check_needs(cfg)) * snapshot.CAPACITY_HEADROOM)
    assert both - 1 >= int(capture_needs * snapshot.CAPACITY_HEADROOM)
    assert both - 1 >= int(_check_needs(cfg) * snapshot.CAPACITY_HEADROOM)
    monkeypatch.setattr(snapshot, "_same_volume", lambda _a, _b: True)
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: both - 1)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    assert refused.value.cause.reason == ROOM
    assert refused.value.cause.detail["required_bytes"] == both
    assert refused.value.cause.detail["shares_volume_with"] == str(snapshot.store_root(cfg))
    assert "also holds the capture store" in refused.value.cause.message
    assert _stores(cfg) == []


def test_a_shared_volume_with_room_for_both_captures_verified(cfg, scratch, monkeypatch):
    capture_needs = snapshot.assert_room_for_capture(cfg, free_bytes=1 << 60)
    both = int((capture_needs + _check_needs(cfg)) * snapshot.CAPACITY_HEADROOM)
    monkeypatch.setattr(snapshot, "_same_volume", lambda _a, _b: True)
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: both)

    assert snapshot.capture(cfg).verified


def test_separate_volumes_are_each_asked_only_their_own(cfg, scratch, monkeypatch):
    """The same room as above refuses when shared and is enough when separate."""
    capture_needs = snapshot.assert_room_for_capture(cfg, free_bytes=1 << 60)
    both = int((capture_needs + _check_needs(cfg)) * snapshot.CAPACITY_HEADROOM)
    _separate_volumes(monkeypatch)
    monkeypatch.setattr(snapshot, "_free_bytes", lambda _root: both - 1)

    assert snapshot.capture(cfg).verified


def test_the_store_and_the_temporary_directory_on_this_disk_are_one_volume(tmp_path):
    (tmp_path / "a").mkdir()
    assert snapshot._same_volume(tmp_path / "a", tmp_path / "not" / "yet" / "made")


def test_a_store_not_yet_made_is_read_as_the_volume_of_its_nearest_parent(tmp_path):
    """The first capture's store does not exist yet, and is its parent's volume.

    Without the walk the store would answer no device at all, which counts as
    shared, and a separate temporary volume would be asked for the capture's
    room too: a false refusal on the first guarded write.
    """
    assert snapshot._device(tmp_path / "not" / "yet" / "made") == os.stat(tmp_path).st_dev
    assert snapshot._device(tmp_path) == os.stat(tmp_path).st_dev


def test_two_volumes_with_different_devices_are_separate(tmp_path, monkeypatch):
    """The direction that lets a write proceed: a separate temporary volume is not asked for both."""
    devices = {tmp_path / "scratch": 7, tmp_path / "store": 8}
    monkeypatch.setattr(snapshot, "_device", lambda path: devices[Path(path)])
    assert not snapshot._same_volume(tmp_path / "scratch", tmp_path / "store")
    devices[tmp_path / "store"] = 7
    assert snapshot._same_volume(tmp_path / "scratch", tmp_path / "store")


def test_no_temporary_directory_at_all_refuses_before_anything_is_written(cfg, monkeypatch):
    def none_usable():
        raise FileNotFoundError(errno.ENOENT, "No usable temporary directory found")

    monkeypatch.setattr(W, "disposable_root", none_usable)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    assert refused.value.cause.reason == ROOM
    assert "no temporary directory could be found" in refused.value.cause.message
    assert _stores(cfg) == []


def test_a_volume_whose_device_cannot_be_read_counts_as_shared(tmp_path, monkeypatch):
    """The direction that refuses more is the one taken when the answer is unknown."""
    real = snapshot._device

    def unreadable(path: Path) -> int:
        if path == tmp_path / "a":
            raise OSError(errno.EIO, "unreadable")
        return real(path)

    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    monkeypatch.setattr(snapshot, "_device", unreadable)
    assert snapshot._same_volume(tmp_path / "a", tmp_path / "b")


def test_a_stand_in_verifier_makes_no_throwaway_so_nothing_measures_one(cfg, scratch, monkeypatch):
    _separate_volumes(monkeypatch)
    _free_on(monkeypatch, scratch, 0)

    assert snapshot.capture(cfg, verifier=lambda _path: True).verified


def test_the_temporary_directory_measured_is_the_one_the_check_copies_into(scratch):
    assert W.disposable_root() == scratch
    with W.disposable_copy(_make_database(scratch.parent / "src")) as copied:
        assert copied.parent.parent == scratch


def _make_database(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "master.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE t (x)")
    conn.commit()
    conn.close()
    return path


def test_the_file_set_measured_is_the_one_the_check_copies(tmp_path, monkeypatch):
    """One list, so the measure and the copy cannot drift apart (P4)."""
    source = _make_database(tmp_path / "src")
    for suffix in W.db_sidecar_suffixes():
        source.with_name(source.name + suffix).write_bytes(b"companion")
    (source.parent / W.MASTER_PLAYLIST_XML).write_bytes(b"<xml/>")
    destination = tmp_path / "dst"
    destination.mkdir()

    W._copy_file_set(source, destination)

    assert sorted(p.name for p in destination.iterdir()) == sorted(
        p.name for p in W.file_set(source)
    )


# ═══════════════════════════════════════════════════════════════════════════
# Layer two: named when the copy still runs out of room
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("code", [errno.ENOSPC, errno.EDQUOT], ids=["no-space", "quota"])
def test_a_check_whose_copy_runs_out_of_room_is_refused_and_recorded_unverified(
    cfg, scratch, monkeypatch, code
):
    """The measure passed and the volume filled anyway: the room slug, never verified."""
    _no_room_in(scratch, monkeypatch, code)

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg)

    cause = refused.value.cause
    assert cause.reason == ROOM
    assert str(scratch) in cause.message
    assert cause.detail["errno"] == code
    [made] = _stores(cfg)
    manifest = json.loads((made / snapshot.MANIFEST_NAME).read_text())
    assert manifest["integrity_verified"] is False
    assert list(scratch.iterdir()) == [], "the throwaway was left behind"


def test_a_check_whose_copy_fails_for_another_reason_is_unverified_not_a_room_message(
    cfg, scratch, monkeypatch
):
    _no_room_in(scratch, monkeypatch, errno.EACCES)

    captured = snapshot.capture(cfg)

    assert not captured.verified
    with pytest.raises(CratekitError) as refused:
        snapshot.assert_verified(captured)
    assert refused.value.cause.reason == "snapshot-integrity-failed"


def test_a_capture_that_fails_its_real_check_is_never_told_as_a_room_message(
    cfg, scratch, monkeypatch
):
    """A real integrity failure keeps its own refusal, whatever the volume holds."""

    def refused_open(*_args, **_kwargs):
        raise W.RekordboxUnavailable("the copy does not open")

    monkeypatch.setattr(W, "open_db", refused_open)

    captured = snapshot.capture(cfg)

    assert not captured.verified
    with pytest.raises(CratekitError) as refused:
        snapshot.assert_verified(captured)
    assert refused.value.cause.reason == "snapshot-integrity-failed"
    assert list(scratch.iterdir()) == []


def test_a_stand_in_verifier_raising_the_copy_failure_is_refused_under_the_room_slug(cfg, scratch):
    def full(path):
        raise W.IntegrityCheckCopyFailed(Path(path), OSError(errno.ENOSPC, "full"))

    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg, verifier=full)

    assert refused.value.cause.reason == ROOM


def test_the_check_raises_the_copy_failure_only_when_asked(cfg, tmp_path, scratch, monkeypatch):
    copied = W.snapshot_db(_database(cfg), stamp="s", root=tmp_path / "snaps")
    _no_room_in(scratch, monkeypatch)

    assert W.integrity_ok(copied) is False
    with pytest.raises(W.IntegrityCheckCopyFailed) as failed:
        W.integrity_ok(copied, raise_copy_failure=True)
    assert failed.value.error.errno == errno.ENOSPC
    assert failed.value.source == copied
    assert failed.value.scratch == scratch


def test_a_scratch_directory_that_cannot_be_made_is_a_copy_failure(
    cfg, tmp_path, scratch, monkeypatch
):
    copied = W.snapshot_db(_database(cfg), stamp="s", root=tmp_path / "snaps")

    def no_directory(*_args, **_kwargs):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(W.tempfile, "mkdtemp", no_directory)

    with pytest.raises(W.IntegrityCheckCopyFailed):
        W.integrity_ok(copied, raise_copy_failure=True)


def test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure(
    cfg, tmp_path, scratch, monkeypatch
):
    """Only the copy raises: what the check meets once it has its copy answers False."""
    copied = W.snapshot_db(_database(cfg), stamp="s", root=tmp_path / "snaps")

    def no_room_to_open(*_args, **_kwargs):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(W, "open_db", no_room_to_open)

    assert W.integrity_ok(copied, raise_copy_failure=True) is False
    assert list(scratch.iterdir()) == []


def test_a_damaged_database_is_a_failed_check_when_the_copy_failure_is_asked_for(tmp_path, scratch):
    damaged = tmp_path / "damaged" / "master.db"
    damaged.parent.mkdir()
    damaged.write_bytes(b"not a database at all" * 100)

    assert W.integrity_ok(damaged, raise_copy_failure=True) is False


@pytest.mark.parametrize(
    ("code", "room"),
    [(errno.ENOSPC, True), (errno.EDQUOT, True), (errno.EACCES, False), (errno.EIO, False)],
)
def test_only_a_full_volume_or_quota_is_read_as_no_room(tmp_path, code, room):
    failed = W.IntegrityCheckCopyFailed(tmp_path / "x.db", OSError(code, "copy failed"))
    refusal = snapshot.check_had_no_room(failed)
    assert (refusal is not None) is room
    if room:
        assert refusal.cause.reason == ROOM
