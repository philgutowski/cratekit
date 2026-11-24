"""The job engine's scenarios: a job driven to each end, then read by the job verbs (U301).

On the job engine suite's configured library, each item committing a report.
"""

from __future__ import annotations

import pytest

from cratekit.core import jobs
from cratekit.core.cause import CratekitError
from cratekit.core.exit_codes import ExitCode
from tests.test_jobs import _blocked, _lossy, _throttled
from tests.test_jobs import cfg as cfg  # noqa: PLC0414

OK = int(ExitCode.OK)
#: A handler no registry binds, so `crate job resume` refuses rather than
#: spawning a worker that would outlive the scenario.
KEY = "core.scenario"


def _queued(store, cfg, *items: str) -> str:
    return jobs.enqueue(store, handler_key=KEY, payload={"x": 1}, cfg=cfg, item_ids=items).job_id


def _drive(store, job_id: str, handle) -> None:
    try:
        jobs.drive(store, job_id, handle, root=jobs.store_dir())
    except CratekitError:
        pass


def test_jobs_driven_to_each_end_and_read_back(stage, cfg, tmp_path):
    reports = tmp_path / "reports"

    def produced(_job, item):
        staged = tmp_path / f"{item.item_id}.staged"
        staged.write_text(item.item_id)
        return jobs.Produced(staged=staged, final=reports / f"{item.item_id}.txt")

    def broken(_job, item):
        raise CratekitError(_throttled()) if item.item_id != "a" else RuntimeError("gone")

    def parked(_job, item):
        if item.item_id == "b":
            raise jobs.Parked(_blocked())
        return produced(_job, item)

    def declined(_job, item):
        if item.item_id == "b":
            raise jobs.Declined(_lossy())
        return produced(_job, item)

    with jobs.open_store(jobs.queue_path()) as store:
        done = _queued(store, cfg, "a", "b")
        _drive(store, done, produced)
        failed = _queued(store, cfg, "a", "b")
        _drive(store, failed, broken)
        partial = _queued(store, cfg, "a", "b", "c")
        _drive(store, partial, lambda job, item: broken(job, item) if item.item_id == "c" else None)
        blocked = _queued(store, cfg, "a", "b", "c")
        _drive(store, blocked, parked)
        skipped = _queued(store, cfg, "a", "b")
        _drive(store, skipped, declined)
        cancelled = _queued(store, cfg, "a")
        jobs.cancel(store, cancelled)
        waiting = _queued(store, cfg, "a")
        with pytest.raises(CratekitError):
            jobs.raise_for_state(jobs.get(store, failed))

    stage.crate("job", "list")
    stage.json("job", "list", "--all")
    for job_id in (done, failed, partial, blocked, skipped, cancelled, waiting):
        stage.crate("job", "show", job_id)
    stage.json("job", "show", blocked)
    stage.crate("job", "resume", failed)
    stage.json("job", "resume", blocked)
    stage.crate("job", "cancel", waiting)
    stage.json("job", "cancel", done)
    stage.crate("job", "list", "--all")
