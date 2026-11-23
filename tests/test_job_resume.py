"""U10's verification: a long job killed at three different stages resumes each time.

A real driver in a real process is SIGKILLed part way through an item, the one
signal it cannot handle, so every recovery is the NEXT process reading the disk.
Finished items stay finished (R22) and the item in flight is redone whole, so
the attempt count is exactly the items plus the kills.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pytest

from cratekit.core import config, jobs
from tests.test_jobs import _attempts, _child_env
from tests.test_jobs import cfg as cfg  # noqa: PLC0414

WORKER = Path(__file__).resolve().parent / "job_worker.py"

#: No item is called this, so a round with it runs straight through.
NEVER_STALL = "stall-on-nothing"


class Scenario:
    """One job, its queue, and the ability to run a real driver against it."""

    def __init__(self, tmp_path: Path, cfg: config.Config, count: int) -> None:
        self.root = tmp_path / "jobs"
        self.ledger = tmp_path / "attempts.log"
        self.ledger.write_text("")
        self.item_ids = [f"item-{index:03d}" for index in range(count)]
        self.store = jobs.open_store(self.root / jobs.QUEUE_FILENAME)
        self.job = jobs.enqueue(
            self.store,
            handler_key="job.resume",
            payload={"items": self.item_ids},
            cfg=cfg,
            item_ids=self.item_ids,
            job_id="the-long-job",
        )

    def close(self) -> None:
        self.store.close()

    def spawn(self, stall: str) -> subprocess.Popen:
        return subprocess.Popen(
            [
                sys.executable,
                str(WORKER),
                "drive",
                str(self.store.path),
                self.job.job_id,
                str(self.root),
                str(self.ledger),
                stall,
            ],
            env=_child_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def kill_during(self, item_id: str) -> None:
        """Run a driver until it reaches ``item_id``, then SIGKILL it there."""
        worker = self.spawn(item_id)
        marker = self.root / f"stalled-{item_id}"
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline and not marker.exists():
            if worker.poll() is not None:
                out, err = worker.communicate()
                raise AssertionError(f"the driver exited early: {err or out}")
            time.sleep(0.02)
        assert marker.exists(), f"the driver never reached {item_id}"
        worker.kill()
        worker.wait(timeout=30)

    def run_to_completion(self) -> None:
        worker = self.spawn(NEVER_STALL)
        out, err = worker.communicate(timeout=120)
        assert worker.returncode == 0, err or out

    def attempts(self) -> list[str]:
        return _attempts(self.ledger)

    def item_states(self) -> dict[str, jobs.ItemState]:
        return {item.item_id: item.state for item in jobs.items(self.store, self.job.job_id)}

    def artifacts(self) -> list[str]:
        out = self.root.parent / "jobs" / "out"
        return sorted(path.stem for path in out.glob("*.txt")) if out.is_dir() else []


@pytest.fixture
def scenario(tmp_path, cfg):
    built = Scenario(tmp_path, cfg, count=6)
    yield built
    built.close()


def test_a_job_killed_mid_item_resumes_with_exactly_one_item_reprocessed(scenario):
    """The killed item, claimed and never completed, is redone; nothing else is,
    because "done" means its artifact was already durable."""
    scenario.kill_during("item-002")
    # Right after the kill one item is stranded in claimed.
    stranded = scenario.item_states()
    assert stranded["item-002"] is jobs.ItemState.CLAIMED
    assert stranded["item-000"] is jobs.ItemState.DONE
    assert "item-002" not in scenario.artifacts(), "a half-done item left an artifact"
    reconciled = jobs.reconcile(scenario.store, scenario.job.job_id, root=scenario.root)
    assert reconciled.state is jobs.JobState.QUEUED
    assert scenario.item_states()["item-002"] is jobs.ItemState.PENDING
    scenario.run_to_completion()
    assert set(scenario.item_states().values()) == {jobs.ItemState.DONE}
    assert scenario.artifacts() == scenario.item_ids
    attempts = scenario.attempts()
    assert len(attempts) == len(scenario.item_ids) + 1, attempts
    assert attempts.count("item-002") == 2
    assert all(attempts.count(item) == 1 for item in ("item-000", "item-001", "item-003"))


def test_a_long_job_killed_at_three_different_stages_resumes_correctly_each_time(scenario):
    """Six items, three kills, nine attempts, the three killed items twice each."""
    killed_on = ("item-000", "item-002", "item-004")
    for item_id in killed_on:
        scenario.kill_during(item_id)
        # Each round comes back to a drivable state on its own.
        assert (
            jobs.reconcile(scenario.store, scenario.job.job_id, root=scenario.root).state
            is jobs.JobState.QUEUED
        )
        assert jobs.ItemState.CLAIMED not in set(scenario.item_states().values())
    scenario.run_to_completion()
    final = jobs.get(scenario.store, scenario.job.job_id)
    assert final.state is jobs.JobState.SUCCEEDED
    assert set(scenario.item_states().values()) == {jobs.ItemState.DONE}
    assert scenario.artifacts() == scenario.item_ids
    attempts = scenario.attempts()
    assert len(attempts) == len(scenario.item_ids) + len(killed_on), attempts
    for item_id in scenario.item_ids:
        expected = 2 if item_id in killed_on else 1
        assert attempts.count(item_id) == expected, (item_id, attempts)
    # Four drivers ran, and none repeated a finished item.
    assert final.attempts == len(killed_on) + 1


def test_a_resumed_driver_runs_against_the_frozen_configuration(scenario, tmp_path):
    """KTD9 across a process boundary: the child rebuilds the configuration from
    the job's own bytes, so an edit made while it sat interrupted changes nothing."""
    scenario.kill_during("item-001")
    frozen = jobs.frozen_config(jobs.get(scenario.store, scenario.job.job_id))
    moved = config.from_dict(
        {**frozen.to_toml_dict(), "paths": {"download_staging": str(tmp_path / "somewhere-else")}}
    )
    config.save(moved)
    config.reset_cache()
    scenario.run_to_completion()
    job = jobs.get(scenario.store, scenario.job.job_id)
    assert jobs.frozen_config(job).paths.download_staging == frozen.paths.download_staging
    assert jobs.drift(job, moved) == ("paths.download_staging",)
