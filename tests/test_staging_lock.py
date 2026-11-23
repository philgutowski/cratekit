"""U293: one pass stages at a time.

The driver lock's rules over the staging folder: the kernel's liveness, a file
never unlinked, and a holder holding again by count. A second descriptor stands
in for a second process.
"""

from __future__ import annotations

import fcntl
import json
import os
import stat

import pytest

from cratekit.core import staging_lock
from cratekit.core.cause import REASONS, CratekitError
from cratekit.core.exit_codes import ExitCode


def _foreign_hold():
    path = staging_lock.lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = open(path, "a+")  # noqa: SIM115 - held for the test
    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return handle


def test_the_holder_is_written_and_the_lock_released_after():
    with staging_lock.held("crate sync land", run_id="run-1"):
        holder = json.loads(staging_lock.lock_path().read_text())
        assert holder["verb"] == "crate sync land" and holder["run_id"] == "run-1"
        assert holder["pid"] == os.getpid() and holder["started"]
    other = _foreign_hold()
    other.close()
    assert staging_lock.lock_path().exists(), "the lock file was unlinked"


def test_the_lock_file_is_private():
    with staging_lock.held("crate sync land"):
        mode = stat.S_IMODE(staging_lock.lock_path().stat().st_mode)
    assert mode & 0o077 == 0


def test_a_second_holder_refuses_naming_the_first():
    path = staging_lock.lock_path()
    other = _foreign_hold()
    other.seek(0)
    other.truncate()
    json.dump({"pid": 99, "verb": "crate sync night", "run_id": "night-run",
               "started": "2026-11-22T03:00:00+00:00"}, other)
    other.flush()
    try:
        with pytest.raises(CratekitError) as caught:
            with staging_lock.held("crate sync land", run_id="manual"):
                pytest.fail("the body ran beside another holder")
    finally:
        other.close()
    cause = caught.value.cause
    assert cause.reason == staging_lock.HELD
    assert "crate sync night, pid 99, run night-run" in cause.message
    assert "crate sync land stages nothing" in cause.message
    assert cause.detail["holder"]["run_id"] == "night-run"
    assert cause.detail["lock"] == str(path)
    assert cause.retryable is True


def test_a_holder_that_cannot_be_read_still_refuses():
    other = _foreign_hold()
    other.write("not json")
    other.flush()
    try:
        with pytest.raises(CratekitError) as caught:
            with staging_lock.held("crate sync land"):
                pass
    finally:
        other.close()
    assert "a pass whose holder could not be read" in caught.value.cause.message


def test_one_process_holds_it_again_by_count_and_releases_at_the_outermost():
    with staging_lock.held("crate sync night", run_id="night"):
        with staging_lock.held("crate sync land", run_id="land"):
            assert staging_lock._DEPTH == 2
            # THE OUTER HOLDER STAYS NAMED: the night holds the pass it runs.
            assert json.loads(staging_lock.lock_path().read_text())["run_id"] == "night"
        assert staging_lock._HANDLE is not None, "the inner hold released the outer"
        with pytest.raises(BlockingIOError):
            _foreign_hold().close()
    assert staging_lock._HANDLE is None and staging_lock._DEPTH == 0


def test_an_exception_in_the_body_releases_the_lock():
    with pytest.raises(ValueError):
        with staging_lock.held("crate sync land"):
            raise ValueError("boom")
    assert staging_lock._HANDLE is None
    _foreign_hold().close()


def test_the_reason_is_declared_as_the_library_busy():
    assert REASONS[staging_lock.HELD] is ExitCode.LIBRARY_BUSY
