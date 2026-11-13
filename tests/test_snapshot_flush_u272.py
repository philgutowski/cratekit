"""U272: a capture's copy is on the disk before its manifest says it is verified.

The restore point every guarded write commits behind is a capture, and the
manifest is what vouches for it. Before this unit the manifest went through
the synced atomic writer while the copy it vouches for was never flushed, so a
power cut inside the write back window could leave a manifest saying verified
beside a copy that is short or empty. The integrity check reads the copy back
through the page cache, so it passes whether or not the bytes reached the
drive, and cannot see that gap.

Three properties are asserted here, each by driving a real capture:

1. **Order, by system call.** Every flush is traced as the inode it reached,
   through both the plain sync and the full flush a platform offers, and the
   database, each companion file, the legacy playlist file, a coupled file,
   every capture directory and the store are flushed BEFORE the manifest's own
   sync, and the capture directory again after it.
2. **A failing flush is never recorded as verified.** The capture refuses, so
   no caller can commit behind it even by forgetting to ask, and the manifest
   it leaves says not verified, wherever the flush failed.
3. **The full flush is asked for where the platform has one** (macOS, where a
   plain sync does not empty the drive's own cache), the plain sync answers
   only a filesystem that does not support it, and any other error raises.

Fully hermetic, as ``tests/test_snapshot.py`` is: an ordinary file stands in
for the database and a stand in verifier gives the verdict.
"""

from __future__ import annotations

import errno
import os
from pathlib import Path

import pytest

from cratekit.core import config, rb_writer, snapshot
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import Remedy
from tests.test_config import valid_data
from tests.test_snapshot import _fails, _passes, _write_coupled_state

try:
    import fcntl
except ImportError:  # pragma: no cover - every platform the suite runs on has it
    fcntl = None  # type: ignore[assignment]


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    """A configured library whose database exists on disk, as ``tests/test_snapshot.py`` builds."""
    library = tmp_path / "library"
    (library / "Music").mkdir(parents=True)
    (library / "db").mkdir(parents=True)
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(library))
    resolved = config.from_dict(valid_data(library))
    config.state_path("rekordbox_db", resolved).write_bytes(b"a database")
    return resolved


def _identity(path: Path) -> tuple[int, int]:
    status = os.stat(path)
    return (status.st_dev, status.st_ino)


def _trace_flushes(monkeypatch) -> list[tuple[int, int]]:
    """Record every plain sync and every full flush, in order, as the inode it reached.

    Traced at the system call wrappers rather than at the capture's own helper,
    so the manifest's sync inside the shared atomic writer is in the same list
    and the order between the two is the order the kernel was asked in.
    """
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


# ═══════════════════════════════════════════════════════════════════════════
# The order: the copy is flushed before the manifest's own sync
# ═══════════════════════════════════════════════════════════════════════════


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
    """P3: the flush covers the directory that exists, not a list of what was meant.

    Asserted by walking the finished capture, so a fifth thing the writer
    learns to copy is covered the day it lands and this test needs no edit.
    """
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
    """The record itself survives before anything commits behind it.

    The shared atomic writer syncs the manifest's bytes and renames it into
    place, and a rename is a change to the directory. Without this second
    flush the restore point's record could vanish after the write it protects
    had committed.
    """
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=_passes)

    after = reached[reached.index(_identity(record.manifest)) + 1 :]
    assert _identity(record.root) in after
    assert _identity(record.root.parent) in after


def test_an_unverified_capture_is_flushed_in_the_same_order(cfg, monkeypatch):
    """The verdict changes what the manifest says, never whether the copy is flushed."""
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, verifier=_fails)

    assert not record.verified
    before = set(reached[: reached.index(_identity(record.manifest))])
    assert _identity(record.database) in before
    assert _identity(record.root) in before


# ═══════════════════════════════════════════════════════════════════════════
# A failing flush is never recorded as verified
# ═══════════════════════════════════════════════════════════════════════════


def _failing_flush(monkeypatch, fails_on, *, after: int = 0) -> list[Path]:
    """Make ``config.flush_to_disk`` raise an input output error on one path.

    ``after`` lets that path flush that many times first, which is how the
    flush that follows the manifest is reached on its own.
    """
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
    with pytest.raises(CratekitError) as refused:
        snapshot.capture(cfg, stamp=stamp, verifier=_passes)
    return refused.value


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
    with pytest.raises(CratekitError) as gate:
        snapshot.assert_verified(left)
    assert gate.value.cause.reason == "snapshot-integrity-failed"


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


# ═══════════════════════════════════════════════════════════════════════════
# The flush itself: the full flush where the platform has one
# ═══════════════════════════════════════════════════════════════════════════


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


def test_the_full_flush_is_asked_for_where_the_platform_offers_one(written, monkeypatch):
    calls = _record_calls(monkeypatch)

    config.flush_to_disk(written)

    assert calls == [("full", 51)]


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


def test_where_no_full_flush_exists_the_plain_sync_is_the_flush(written, monkeypatch):
    calls = _record_calls(monkeypatch)
    monkeypatch.setattr(config, "_FULL_FLUSH", None)

    config.flush_to_disk(written)

    assert calls == [("sync",)]


def test_a_plain_sync_that_fails_raises(written, monkeypatch):
    monkeypatch.setattr(config, "_FULL_FLUSH", None)

    def fails(fd):
        raise OSError(errno.EIO, "Input/output error")

    monkeypatch.setattr(os, "fsync", fails)

    with pytest.raises(OSError) as raised:
        config.flush_to_disk(written)

    assert raised.value.errno == errno.EIO
    assert raised.value.filename == str(written), "the error does not say which file failed"


def test_a_directory_is_flushed_through_the_same_call(tmp_path, monkeypatch):
    calls = _record_calls(monkeypatch)
    monkeypatch.setattr(config, "_FULL_FLUSH", None)

    config.flush_to_disk(tmp_path)

    assert calls == [("sync",)]


def test_a_path_that_is_not_there_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        config.flush_to_disk(tmp_path / "absent")


def test_the_platforms_full_flush_is_the_one_asked_for():
    """Read from the platform, never spelled: macOS has it, Linux has none."""
    expected = getattr(fcntl, "F_FULLFSYNC", None) if fcntl is not None else None
    assert config._FULL_FLUSH == expected


def test_a_capture_outside_the_configured_store_is_flushed_too(cfg, tmp_path, monkeypatch):
    """Every capture, Phillip's answer of 2026-11-13: a rehearsal's included.

    A rehearsal drives the same verb with its library state redirected, so its
    capture goes through this same function into a store that is not the
    library's, and promises the same thing to the rehearsal's own gate.
    """
    elsewhere = tmp_path / "rehearsal-store"
    reached = _trace_flushes(monkeypatch)

    record = snapshot.capture(cfg, root=elsewhere, verifier=_passes)

    assert record.root.parent == elsewhere
    before = set(reached[: reached.index(_identity(record.manifest))])
    assert _identity(record.database) in before
    assert _identity(elsewhere) in before
