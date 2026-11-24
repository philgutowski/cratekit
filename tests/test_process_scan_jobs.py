"""U211, review round two: a backup job is never offered as a run to continue.

Its cause is the job's verdict. The fixtures are ``tests/test_backup_cli.py``'s.
"""

from __future__ import annotations

from cratekit.core import processes
from cratekit.core.exit_codes import ExitCode
from tests.test_backup_cli import _drive
from tests.test_backup_cli import _nothing_is_running as _nothing_is_running  # noqa: PLC0414
from tests.test_backup_cli import cfg as cfg  # noqa: PLC0414
from tests.test_backup_cli import rclone as rclone  # noqa: PLC0414
from tests.test_process_scan import DYING, FakeProcess, finder
from tests.test_process_scan import table as table  # noqa: PLC0414


def _a_job_the_scan_refused(monkeypatch, table) -> str:
    """A backup filed over a dying process, the fake table read carefully, not as empty."""
    monkeypatch.setattr(
        processes,
        "running_process_names",
        lambda: tuple(name for _pid, name in processes.running_processes()),
    )
    table(FakeProcess(300, raises=DYING), finder())
    _code, first = _drive(["backup", "run"])
    return first["data"]["job_id"]


def test_a_backup_job_refused_by_the_scan_is_not_offered_as_a_run_to_continue(
    cfg, rclone, monkeypatch, table
):
    job_id = _a_job_the_scan_refused(monkeypatch, table)
    code, ran = _drive(["backup", "run", "--job", job_id])
    cause = ran["cause"]
    assert cause["reason"] == processes.UNCONFIRMED, ran
    assert ran["resumable"] is False, ran
    assert ran["outcome"] != "blocked", ran
    assert "continue" not in (cause.get("detail") or {}), cause
    steps = cause["remediation"]["steps"]
    assert not any("--run" in step for step in steps), steps


def test_a_fresh_backup_takes_the_snapshot_once_the_process_has_exited(
    cfg, rclone, monkeypatch, table
):
    """What the job's verdict leaves a person to do, driven to the end."""
    _drive(["backup", "run", "--job", _a_job_the_scan_refused(monkeypatch, table)])
    table(finder())
    code, fresh = _drive(["backup", "run"])
    code, done = _drive(["backup", "run", "--job", fresh["data"]["job_id"]])
    assert code == int(ExitCode.OK), done
