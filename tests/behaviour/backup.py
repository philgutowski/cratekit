"""Backup's scenarios: a backup capture, its refusals, and the restore plan from it (U297, U311).

The restore suite's stand in for rclone logs what would be copied where, which
is the capture's record. The refusals answer `processes.running_process_names`
with rekordbox or its agent, and the resume after it is gone finishes.
"""

from __future__ import annotations

from cratekit.core.exit_codes import ExitCode
from tests.test_restore import acknowledge
from tests.test_restore import cfg as cfg  # noqa: PLC0414
from tests.test_restore_cli import CONFIRM, _fake_rclone
from tests.test_restore_cli import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_restore_cli import (
    _release_process_locks as _release_process_locks,  # noqa: PLC0414
)
from tests.test_restore_cli import installed as installed  # noqa: PLC0414

OK = int(ExitCode.OK)
PLAN = ("restore", "run", "--from-backup", "--dry-run")
PROCESSES = "cratekit.core.processes.running_process_names"


def test_backup_capture_and_the_restore_plan(stage, installed, monkeypatch):
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    queued = stage.json("backup", "run")
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    ran = stage.json("backup", "run", "--job", job_id)
    assert ran.code == OK, ran.stdout
    assert ran.envelope["data"]["state"] == "succeeded", ran.stdout
    assert "remote:database-snapshots" in log.read_text()
    stage.crate("backup", "run", "--job", job_id)

    assert stage.crate(*PLAN).code == int(ExitCode.DECISION_REQUIRED)
    refused = stage.json(*PLAN)
    assert refused.code == int(ExitCode.DECISION_REQUIRED), refused.stdout
    run_id = refused.envelope["run_id"]
    assert stage.decide(run_id, CONFIRM, "restore").code == OK
    walked = stage.json("--run", run_id, *PLAN)
    assert walked.code == OK, walked.stdout
    assert walked.envelope["data"]["totals"]["dry_run"] is True


def test_a_second_capture_and_a_full_check(stage, installed, monkeypatch):
    """A second backup after the database changed, and a full check, both through the queue.

    The first is shown in a person's rendering as it queues and as it runs, so
    the capture holds both forms; the second takes the `--check` path, which
    lists the remote and snapshots the database whether or not it changed.
    """
    from cratekit.core import config

    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    first = stage.json("backup", "run")
    assert first.code == OK, first.stdout
    assert stage.json("backup", "run", "--job", first.envelope["data"]["job_id"]).code == OK

    config.state_path("rekordbox_db", installed).write_bytes(b"database, generation two")
    queued = stage.crate("backup", "run")
    assert queued.code == OK, queued.stderr
    second = stage.json("backup", "run")
    assert second.code == OK, second.stdout
    resumed = stage.crate("backup", "run", "--job", second.envelope["data"]["job_id"])
    assert resumed.code == OK, resumed.stderr

    checked = stage.json("backup", "run", "--check")
    assert checked.code == OK, checked.stdout
    full = stage.json("backup", "run", "--check", "--job", checked.envelope["data"]["job_id"])
    assert full.code == OK, full.stdout
    assert full.envelope["data"]["state"] == "succeeded", full.stdout
    assert "remote:database-snapshots" in log.read_text()


def test_a_rehearsal_copies_nothing(stage, installed, monkeypatch):
    """`crate backup run --dry-run`, queued and run: the plan walked, no age recorded."""
    acknowledge(installed)
    _fake_rclone(installed, monkeypatch)

    queued = stage.json("backup", "run", "--dry-run")
    assert queued.code == OK, queued.stdout
    job_id = queued.envelope["data"]["job_id"]
    ran = stage.json("backup", "run", "--dry-run", "--job", job_id)
    assert ran.code == OK, ran.stdout
    stage.crate("backup", "run", "--dry-run", "--job", job_id)


def test_a_backup_refuses_while_rekordbox_or_its_agent_runs(stage, installed, monkeypatch):
    """The database portion refuses under each process, and a fresh job copies it once both are gone.

    The refusal is permanent on its job, which the suite asserts of its own
    accord, so the job that refused is asked about once more after the process
    is gone and a new one is queued to take the copy.
    """
    acknowledge(installed)
    log = _fake_rclone(installed, monkeypatch)

    for name in ("rekordbox", "rekordboxAgent"):
        monkeypatch.setattr(PROCESSES, lambda name=name: (name,))
        queued = stage.json("backup", "run")
        assert queued.code == OK, queued.stdout
        job_id = queued.envelope["data"]["job_id"]
        refused = stage.json("backup", "run", "--job", job_id)
        assert refused.code != OK, refused.stdout
        shown = stage.crate("backup", "run", "--job", job_id)
        assert shown.code == refused.code, shown.stderr

    assert "remote:database-snapshots" not in log.read_text()
    monkeypatch.setattr(PROCESSES, lambda: ())
    assert stage.json("backup", "run", "--job", job_id).code != OK
    fresh = stage.json("backup", "run")
    assert fresh.code == OK, fresh.stdout
    finished = stage.json("backup", "run", "--job", fresh.envelope["data"]["job_id"])
    assert finished.code == OK, finished.stdout
    assert finished.envelope["data"]["state"] == "succeeded", finished.stdout
    assert "remote:database-snapshots" in log.read_text()
