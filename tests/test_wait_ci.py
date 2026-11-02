"""`scripts/wait_ci.py` reads a head's pull request runs as one verdict (U196).

The REST answer is served by the test, since the network is the one boundary a
test cannot cross. `verdict` and `wait` run for real on what it serves, with
the clock and the sleep replaced so a timeout is measured without waiting.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "wait_ci.py"


@pytest.fixture
def wait_ci():
    spec = importlib.util.spec_from_file_location("wait_ci_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(name: str, status: str = "completed", conclusion: str | None = "success") -> dict:
    return {"name": name, "status": status, "conclusion": conclusion}


def test_no_run_yet_is_pending_never_green(wait_ci):
    state, line = wait_ci.verdict([])
    assert state == wait_ci.PENDING
    assert "no pull request run" in line


def test_a_run_still_going_is_pending_and_named(wait_ci):
    runs = [_run("ci"), _run("board", status="in_progress", conclusion=None)]
    state, line = wait_ci.verdict(runs)
    assert state == wait_ci.PENDING
    assert "1 of 2" in line and "board" in line


@pytest.mark.parametrize("conclusion", ["success", "neutral", "skipped"])
def test_every_run_completed_green_is_green(wait_ci, conclusion):
    state, line = wait_ci.verdict([_run("ci"), _run("board", conclusion=conclusion)])
    assert state == wait_ci.PASSED
    assert "2 run(s)" in line


@pytest.mark.parametrize(
    "conclusion", ["failure", "cancelled", "timed_out", "action_required", None]
)
def test_one_run_not_green_makes_the_head_red(wait_ci, conclusion):
    state, line = wait_ci.verdict([_run("ci"), _run("board", conclusion=conclusion)])
    assert state == wait_ci.FAILED
    assert f"board {conclusion}" in line


class _Clock:
    """A clock the sleep moves, so a wait is measured without waiting."""

    def __init__(self):
        self.now = 0.0
        self.sleeps = 0

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps += 1
        self.now += seconds


def test_wait_returns_once_the_runs_finish(wait_ci):
    answers = iter([[], [_run("ci", status="queued", conclusion=None)], [_run("ci")]])
    clock = _Clock()
    state, _ = wait_ci.wait(
        lambda: next(answers), timeout=600, every=60, sleep=clock.sleep, clock=clock
    )
    assert state == wait_ci.PASSED
    assert clock.sleeps == 2


def test_wait_returns_red_without_waiting_out_the_clock(wait_ci):
    clock = _Clock()
    state, _ = wait_ci.wait(
        lambda: [_run("ci", conclusion="failure")],
        timeout=600,
        every=60,
        sleep=clock.sleep,
        clock=clock,
    )
    assert state == wait_ci.FAILED
    assert clock.sleeps == 0


def test_wait_times_out_as_pending_and_says_so(wait_ci):
    clock = _Clock()
    state, line = wait_ci.wait(lambda: [], timeout=300, every=60, sleep=clock.sleep, clock=clock)
    assert state == wait_ci.PENDING
    assert line.startswith("timed out")
    # It never sleeps past the deadline: five reads at 0, 60, 120, 180, 240,
    # and the sixth would land at 300 plus a read.
    assert clock.now <= 300


def test_main_exits_by_verdict(wait_ci, monkeypatch, capsys):
    monkeypatch.setattr(
        wait_ci, "pull_request_runs", lambda repo, sha: [_run("ci", conclusion="failure")]
    )
    assert wait_ci.main(["abc123", "--repo", "owner/name", "--every", "1", "--timeout", "1"]) == 1
    assert capsys.readouterr().out.startswith("red: ")
    monkeypatch.setattr(wait_ci, "pull_request_runs", lambda repo, sha: [])
    assert wait_ci.main(["abc123", "--repo", "owner/name", "--every", "1", "--timeout", "0"]) == 2
    monkeypatch.setattr(wait_ci, "pull_request_runs", lambda repo, sha: [_run("ci")])
    assert wait_ci.main(["abc123", "--repo", "owner/name"]) == 0


def test_a_failed_read_is_no_run_rather_than_a_crash(wait_ci, monkeypatch):
    class Refused:
        returncode = 1
        stdout = ""

    monkeypatch.setattr(wait_ci.subprocess, "run", lambda *a, **k: Refused())
    assert wait_ci.pull_request_runs("owner/name", "abc123") == []
