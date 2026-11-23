"""The guarded writer's refusals, driven through a whole verb (U300).

Each scenario queues `crate rebuild` on the routing suite's library and runs
the job under one condition the guarded writer or the session refuses:
rekordbox or its agent running at open, rekordbox started before the commit,
Cloud Library Sync on, the library lock held on another handle, and the
backup acknowledgment absent or expired. A rebuild opens without the
application version check, so `core_gates.py` drives that one. The
capture holds what each refusal printed, its exit code, and that nothing was
written. A whitelist violation and a delete have no verb that produces them,
so `tests/test_rb_writer_db.py` drives those against the writer itself.
"""

from __future__ import annotations

import json
import sys

from cratekit.core import config, rb_writer, session
from cratekit.core.exit_codes import ExitCode
from tests.test_routing_workers import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_routing_workers import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_routing_workers import acknowledged as acknowledged  # noqa: PLC0414
from tests.test_routing_workers import configured as configured  # noqa: PLC0414
from tests.test_routing_workers import library as library  # noqa: PLC0414
from tests.test_routing_workers import native as native  # noqa: PLC0414
from tests.test_routing_workers import stocked as stocked  # noqa: PLC0414

OK = int(ExitCode.OK)
VERB = ("rebuild", "--actor", "a-person")


def _refused_run(stage, reason: str) -> None:
    """Queue the rebuild, run it once as JSON and once as a person reads it."""
    queued = stage.json(*VERB)
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    ran = stage.json(*VERB, "--job", job_id)
    assert reason in ran.stdout, ran.stdout
    stage.crate(*VERB, "--job", job_id)


def test_rekordbox_running_at_open(stage, acknowledged, native, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_running", lambda: True)
    _refused_run(stage, "rekordbox-running")


def test_the_agent_running_at_open(stage, acknowledged, native, monkeypatch):
    monkeypatch.setattr(rb_writer, "rekordbox_agent_running", lambda: True)
    _refused_run(stage, "rekordbox-running")


def test_rekordbox_started_before_the_commit(stage, acknowledged, native, monkeypatch):
    """Closed at open, running by the commit: the commit's own re-check refuses."""

    def running() -> bool:
        frame = sys._getframe(1)
        while frame is not None:
            if frame.f_code.co_name == "commit_guarded":
                return True
            frame = frame.f_back
        return False

    monkeypatch.setattr(rb_writer, "rekordbox_running", running)
    _refused_run(stage, "rekordbox-running")



def test_cloud_library_sync_on(stage, acknowledged, native, monkeypatch):
    monkeypatch.setattr(
        rb_writer,
        "read_rekordbox_settings",
        lambda *args, **kwargs: {rb_writer.LIBRARY_SYNC_SETTING: 1},
    )
    _refused_run(stage, "cloud-sync-active")


def test_the_session_lock_held_elsewhere(stage, acknowledged, native):
    """The library lock taken on another handle, with no holder recorded."""
    target = session.lock_path(acknowledged)
    config.mkdir_private(target.parent)
    with open(target, "a+") as handle:
        rb_writer._acquire_exclusive(handle)
        try:
            _refused_run(stage, "session-lock-held")
        finally:
            rb_writer._release_exclusive(handle)


def test_no_backup_acknowledgment(stage, acknowledged, native):
    session.ack_path(acknowledged).unlink()
    _refused_run(stage, "backup-acknowledgment-missing")


def test_an_expired_backup_acknowledgment(stage, acknowledged, native):
    path = session.ack_path(acknowledged)
    recorded = json.loads(path.read_text())
    recorded["recorded_at"] = "2026-01-01T00:00:00+00:00"
    recorded["expires_at"] = "2026-01-02T00:00:00+00:00"
    path.write_text(json.dumps(recorded))
    config.reset_cache()
    _refused_run(stage, "backup-acknowledgment-missing")
