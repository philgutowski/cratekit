"""U272: a capture's copy is on the disk before its manifest says it is verified.

Every file, directory and the store are flushed before the manifest's sync, a failing
flush is never recorded verified, and the full flush is asked for where there is one."""

# ruff: noqa: F811, the fixture below is imported from the capture suite by name

from __future__ import annotations

import errno
import os
import sys
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, snapshot
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from tests.test_restore import _refusal, _refused
from tests.test_snapshot import _fails, _passes, _write_coupled_state
from tests.test_snapshot import cfg as cfg  # noqa: PLC0414 - the fixture, used by name

try:
    import fcntl
except ImportError:  # pragma: no cover - every platform the suite runs on has it
    fcntl = None  # type: ignore[assignment]


def _identity(path: Path) -> tuple[int, int]:
    status = os.stat(path)
    return (status.st_dev, status.st_ino)


def _trace_flushes(monkeypatch) -> list[tuple[int, int]]:
    """Record every plain sync and full flush, in kernel order, as the inode it reached."""
    reached: list[tuple[int, int]] = []
    real_fsync = os.fsync

    def traced_fsync(fd):
        status = os.fstat(fd)
        reached.append((status.st_dev, status.st_ino))
        return real_fsync(fd)

    monkeypatch.setattr(os, "fsync", traced_fsync)
    full = getattr(fcntl, "F_FULLFSYNC", None) if fcntl is not None else None
    if full is not None:  # pragma: no cover - macOS only
        real_fcntl = fcntl.fcntl

        def traced_fcntl(fd, operation, *rest):
            if operation == full:
                status = os.fstat(fd)
                reached.append((status.st_dev, status.st_ino))
            return real_fcntl(fd, operation, *rest)

        monkeypatch.setattr(fcntl, "fcntl", traced_fcntl)
    return reached


def _whole_file_set(cfg) -> list[Path]:
    """Put every file the writer copies beside the database on disk, by derivation."""
    written = []
    for companion in config.sidecar_paths("rekordbox_db", cfg):
        companion.write_bytes(b"outstanding")
        written.append(companion)
    assert written, "the inventory declares no companion files, so this proves nothing"
    playlist = config.state_path("rekordbox_db", cfg).parent / rb_writer.MASTER_PLAYLIST_XML
    playlist.write_bytes(b"<playlists/>")
    written.append(playlist)
    return written


# The order: the copy is flushed before the manifest's own sync


def test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest(
    cfg, monkeypatch
):
    beside = _whole_file_set(cfg)
    marker = _write_coupled_state(cfg)
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=_passes)

    assert record.verified
    manifest_at = reached.index(_identity(record.manifest))
    before = set(reached[:manifest_at])
    coupled = record.root / config.library_coupled_dir(cfg).name
    expected = {
        "the database": record.database,
        **{f"companion {path.name}": record.root / path.name for path in beside},
        "the coupled file": coupled / marker.name,
        "the coupled directory": coupled,
        "the capture directory": record.root,
        "the store that holds it": record.root.parent,
    }
    for what, path in expected.items():
        assert _identity(path) in before, f"{what} was not flushed before the manifest"


def test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking(cfg, monkeypatch):
    """P3: the flush covers the capture as walked, not a list of what was meant."""
    _whole_file_set(cfg)
    _write_coupled_state(cfg)
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=_passes)

    before = set(reached[: reached.index(_identity(record.manifest))])
    walked = 0
    for current, directories, files in os.walk(record.root):
        here = Path(current)
        for name in [*directories, *files]:
            if here / name == record.manifest:
                continue
            walked += 1
            assert _identity(here / name) in before, f"{here / name} was not flushed first"
    assert walked >= 5, "the capture held too little for this to prove anything"


def test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it(cfg, monkeypatch):
    """The manifest's rename changes the directory, so it is flushed again before any commit."""
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=_passes)

    after = reached[reached.index(_identity(record.manifest)) + 1 :]
    assert _identity(record.root) in after
    assert _identity(record.root.parent) in after


def test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed(cfg, monkeypatch):
    """The flush follows the check, so a file the check adds is still flushed (R-1665)."""
    left: list[Path] = []

    def leaves_a_file(database):
        changed = Path(database).with_name("left-by-the-check")
        changed.write_bytes(b"changed")
        left.append(changed)
        return True

    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=leaves_a_file)

    assert left, "the check did not run"
    before = set(reached[: reached.index(_identity(record.manifest))])
    assert _identity(left[0]) in before, "the flush ran before the check"


def test_an_unverified_capture_is_flushed_in_the_same_order(cfg, monkeypatch):
    """The verdict changes what the manifest says, never whether the copy is flushed."""
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=_fails)

    assert not record.verified
    before = set(reached[: reached.index(_identity(record.manifest))])
    assert _identity(record.database) in before
    assert _identity(record.root) in before


# A failing flush is never recorded as verified


def _failing_flush(monkeypatch, fails_on, *, after: int = 0) -> list[Path]:
    """Make ``config.flush_to_disk`` raise on one path, after ``after`` flushes of it."""
    real = config.flush_to_disk
    seen: list[Path] = []

    def flaky(path):
        path = Path(path)
        seen.append(path)
        if fails_on(path):
            if seen.count(path) > after:
                raise OSError(errno.EIO, "Input/output error", str(path))
        return real(path)

    monkeypatch.setattr(config, "flush_to_disk", flaky)
    return seen


def _refused_capture(cfg, stamp: str) -> CratekitError:
    return _refused(snapshot.capture, cfg, stamp=stamp, verifier=_passes)


@pytest.mark.parametrize(
    "where",
    ["the database", "a companion file", "a coupled file", "the capture directory", "the store"],
)
def test_a_capture_whose_flush_fails_refuses_and_says_it_is_not_verified(cfg, monkeypatch, where):
    _whole_file_set(cfg)
    marker = _write_coupled_state(cfg)
    stamp = "flush-fails"
    root = snapshot.store_root(cfg) / stamp
    database = config.state_path("rekordbox_db", cfg)
    companion = config.sidecar_paths("rekordbox_db", cfg)[0]
    target = {
        "the database": root / database.name,
        "a companion file": root / companion.name,
        "a coupled file": root / config.library_coupled_dir(cfg).name / marker.name,
        "the capture directory": root,
        "the store": root.parent,
    }[where]
    _failing_flush(monkeypatch, lambda path: path == target)

    refusal = _refused_capture(cfg, stamp)

    assert refusal.cause.reason == "snapshot-integrity-failed"
    assert refusal.cause.remediation.remedy == Remedy.MOUNT_LIBRARY_VOLUME
    assert str(target) in refusal.cause.message
    assert "Input/output error" in refusal.cause.message
    left = snapshot.read_manifest(root)
    assert left.integrity_verified is False
    assert not left.verified
    gate = _refusal(snapshot.assert_verified, left)
    assert gate.reason == "snapshot-integrity-failed"


def test_a_flush_that_fails_after_the_manifest_leaves_it_saying_not_verified(cfg, monkeypatch):
    stamp = "flush-fails-late"
    root = snapshot.store_root(cfg) / stamp
    seen = _failing_flush(monkeypatch, lambda path: path == root, after=1)

    refusal = _refused_capture(cfg, stamp)

    assert seen.count(root) == 2, "the failure was not the flush after the manifest"
    assert refusal.cause.reason == "snapshot-integrity-failed"
    assert snapshot.read_manifest(root).integrity_verified is False


def test_a_failed_flush_does_not_change_what_was_copied(cfg, monkeypatch):
    """Nothing about what is copied changes: the refusal leaves the whole set in place."""
    beside = _whole_file_set(cfg)
    marker = _write_coupled_state(cfg)
    stamp = "flush-fails-copied"
    root = snapshot.store_root(cfg) / stamp
    _failing_flush(monkeypatch, lambda path: path == root)

    _refused_capture(cfg, stamp)

    database = config.state_path("rekordbox_db", cfg)
    assert (root / database.name).read_bytes() == b"a database"
    for path in beside:
        assert (root / path.name).read_bytes() == path.read_bytes()
    coupled = root / config.library_coupled_dir(cfg).name / marker.name
    assert coupled.read_text() == marker.read_text()


def test_a_manifest_that_cannot_be_written_after_a_failed_flush_still_refuses(cfg, monkeypatch):
    """The refusal is the guard; the unverified manifest is the record of it."""
    stamp = "flush-and-manifest-fail"
    root = snapshot.store_root(cfg) / stamp
    _failing_flush(monkeypatch, lambda path: path == root)

    def no_room(payload, path, **kwargs):
        raise OSError(errno.ENOSPC, "No space left on device", str(path))

    monkeypatch.setattr(config, "atomic_write_bytes", no_room)

    refusal = _refused_capture(cfg, stamp)

    assert refusal.cause.reason == "snapshot-integrity-failed"
    assert not (root / snapshot.MANIFEST_NAME).exists()


# The flush itself: the full flush where the platform has one


@pytest.fixture
def written(tmp_path) -> Path:
    target = tmp_path / "copy.db"
    target.write_bytes(b"bytes")
    return target


def _record_calls(monkeypatch, *, full_answers=None) -> list[tuple]:
    calls: list[tuple] = []

    def full(fd, operation):
        calls.append(("full", operation))
        if full_answers is not None:
            raise full_answers

    monkeypatch.setattr(config, "_FULL_FLUSH", 51)
    monkeypatch.setattr(config, "_full_flush", full)
    monkeypatch.setattr(os, "fsync", lambda fd: calls.append(("sync",)))
    return calls


@pytest.mark.parametrize(
    ("full", "directory", "expected"),
    [(51, False, [("full", 51)]), (None, False, [("sync",)]), (None, True, [("sync",)])],
    ids=["full-flush-offered", "no-full-flush", "a-directory"],
)
def test_the_full_flush_is_asked_for_where_the_platform_offers_one(
    written, monkeypatch, full, directory, expected
):
    """With no full flush the plain sync is the flush, and a directory takes the same call."""
    calls = _record_calls(monkeypatch)
    monkeypatch.setattr(config, "_FULL_FLUSH", full)

    config.flush_to_disk(written.parent if directory else written)

    assert calls == expected


@pytest.mark.parametrize(
    "answer",
    sorted({errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.ENOTTY}),
    ids=errno.errorcode.get,
)
def test_a_filesystem_without_the_full_flush_gets_the_plain_sync(written, monkeypatch, answer):
    calls = _record_calls(monkeypatch, full_answers=OSError(answer, os.strerror(answer)))

    config.flush_to_disk(written)

    assert calls == [("full", 51), ("sync",)]


def test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back(
    written, monkeypatch
):
    calls = _record_calls(monkeypatch, full_answers=OSError(errno.EIO, "Input/output error"))

    with pytest.raises(OSError) as raised:
        config.flush_to_disk(written)

    assert raised.value.errno == errno.EIO
    assert calls == [("full", 51)]


def test_a_plain_sync_that_fails_raises(written, monkeypatch):
    monkeypatch.setattr(config, "_FULL_FLUSH", None)

    def fails(fd):
        raise OSError(errno.EIO, "Input/output error")

    monkeypatch.setattr(os, "fsync", fails)

    with pytest.raises(OSError) as raised:
        config.flush_to_disk(written)

    assert raised.value.errno == errno.EIO
    assert raised.value.filename == str(written), "the error does not say which file failed"


def test_a_path_that_is_not_there_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        config.flush_to_disk(tmp_path / "absent")


def test_the_platforms_full_flush_is_the_one_asked_for():
    """macOS asks the drive to empty its cache, stated per platform, never read back."""
    if sys.platform == "darwin":  # pragma: no cover - the Mac battery
        assert config._FULL_FLUSH is not None
        assert config._FULL_FLUSH == fcntl.F_FULLFSYNC
    else:
        assert config._FULL_FLUSH is None


def test_a_capture_outside_the_configured_store_is_flushed_too(cfg, tmp_path, monkeypatch):
    """Every capture is flushed, a rehearsal's included (Phillip, 2026-11-13)."""
    elsewhere = tmp_path / "rehearsal-store"
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, root=elsewhere, verifier=_passes)

    assert record.root.parent == elsewhere
    before = set(reached[: reached.index(_identity(record.manifest))])
    assert _identity(record.database) in before
    assert _identity(elsewhere) in before


def test_a_capture_directory_the_walk_cannot_read_raises_rather_than_being_skipped(tmp_path):
    """A directory ``os.walk`` cannot read raises, since a skipped one would go unflushed."""
    store = tmp_path / "store"
    store.mkdir()

    with pytest.raises(FileNotFoundError):
        snapshot._flush(store / "gone", store)
