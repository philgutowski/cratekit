"""U210: the steps a run's write records beside its held plan, read back only for that plan.

D1 applies. Nothing here names a real account, a real person or a real track.
"""

from __future__ import annotations

import json
import os
import time

from cratekit.core import held_plan
from tests.test_rebuild import _platform_seams as _platform_seams  # noqa: PLC0414
from tests.test_rebuild import cfg as cfg  # noqa: PLC0414
from tests.test_rebuild import library as library  # noqa: PLC0414


def test_steps_marked_are_read_back_for_the_same_run_and_plan(cfg):
    steps = held_plan.Steps("run-a", "digest-1")
    steps.begin()
    steps.mark("new:7", "making")
    steps.mark("new:7", "made", "pl-3")
    read, why = held_plan.load_steps("run-a", "digest-1")
    assert why == ""
    assert read.started()
    assert read.has("new:7", "making")
    assert read.get("new:7", "made") == "pl-3"
    assert not read.has("new:8", "making")


def test_no_steps_file_is_no_step_and_says_nothing(cfg):
    read, why = held_plan.load_steps("run-b", "digest-1")
    assert (read.started(), why) == (False, "")


def test_steps_recorded_against_another_plan_are_not_read_and_say_why(cfg):
    held_plan.Steps("run-c", "digest-1").mark("acc", "done")
    read, why = held_plan.load_steps("run-c", "digest-2")
    assert not read.started()
    assert "digest" in why


def test_steps_that_do_not_parse_are_not_read_and_say_why(cfg):
    held_plan.Steps("run-d", "digest-1").begin()
    held_plan.steps_path("run-d").write_text("{ not json")
    read, why = held_plan.load_steps("run-d", "digest-1")
    assert not read.started()
    assert why.startswith("the run's steps could not be read")


def test_steps_of_another_version_are_not_read(cfg):
    path = held_plan.steps_path("run-e")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"version": 99, "run_id": "run-e", "digest": "d", "steps": {"a": {"done": True}}})
    )
    read, why = held_plan.load_steps("run-e", "d")
    assert not read.started()
    assert "version" in why


def test_release_lets_go_of_the_plan_and_its_steps(cfg):
    held_plan.Steps("run-f", "d").mark("acc", "account")
    held_plan.path("run-f").parent.mkdir(parents=True, exist_ok=True)
    held_plan.path("run-f").write_text("{}")
    held_plan.release("run-f")
    assert not held_plan.path("run-f").exists()
    assert not held_plan.steps_path("run-f").exists()


def test_prune_keeps_the_kept_runs_old_steps_and_removes_another_runs(cfg):
    held_plan.Steps("run-g", "d").begin()
    held_plan.Steps("run-h", "d").begin()
    old = time.time() - held_plan.KEEP.total_seconds() - 60
    for run_id in ("run-g", "run-h"):
        os.utime(held_plan.steps_path(run_id), (old, old))
    assert held_plan.prune(keep="run-g") == 1
    assert held_plan.steps_path("run-g").exists()
    assert not held_plan.steps_path("run-h").exists()
