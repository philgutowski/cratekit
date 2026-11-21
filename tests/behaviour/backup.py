"""Backup's scenarios: a backup capture and the restore plan from it (U297).

`crate backup run` is queued and run, so every portion, the database capture
into its dated destination among them, reaches the program that would copy
it. That program is the restore suite's stand in for rclone, which logs each
invocation and answers the listings a restore makes, so the log in the state
directory is the capture's record of what would have been copied where.
`crate restore run --from-backup --dry-run` then stops at its gate, which
shows the plan, and walks it once the gate is answered, performing none of it.
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
