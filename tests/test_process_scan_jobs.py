"""U211, from review round two: a job is never offered as a run to continue.

The dispatcher keeps the run of the scan's own refusal, so ``--run`` continues
it with its answers. A backup job whose database item met the same refusal
records the reason on the failed item and summarises it on the job's cause,
and running the verb again under ``--run`` cannot retake that item, so the
job's cause is answered as the job's verdict, never as a kept run. Driven
through the dispatcher over the fake process table of
``tests/test_process_scan.py``. The fixtures are ``tests/test_backup_cli.py``'s,
in a file of their own because that suite's library and the sync pair suite's
both answer to the name ``cfg``.
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


def _careful(monkeypatch) -> None:
    """The backup suite fakes an empty machine; this one reads the fake table carefully."""
    monkeypatch.setattr(
        processes,
        "running_process_names",
        lambda: tuple(name for _pid, name in processes.running_processes()),
    )


def test_a_backup_job_refused_by_the_scan_is_not_offered_as_a_run_to_continue(
    cfg, rclone, monkeypatch, table
):
    _careful(monkeypatch)
    table(FakeProcess(300, raises=DYING), finder())
    code, first = _drive(["backup", "run"])
    job_id = first["data"]["job_id"]

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
    _careful(monkeypatch)
    table(FakeProcess(300, raises=DYING), finder())
    code, first = _drive(["backup", "run"])
    _drive(["backup", "run", "--job", first["data"]["job_id"]])

    table(finder())
    code, fresh = _drive(["backup", "run"])
    code, done = _drive(["backup", "run", "--job", fresh["data"]["job_id"]])

    assert code == int(ExitCode.OK), done
