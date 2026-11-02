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


class _Answer:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


@pytest.mark.parametrize(
    "answer, reason",
    [
        (_Answer(1, stderr="gh: HTTP 403 Forbidden\n"), "HTTP 403"),
        (_Answer(1), "gh exited 1"),
        (_Answer(0, stdout="<html>proxy</html>"), "not JSON"),
        (_Answer(0, stdout='{"message": "Not Found"}'), "no workflow_runs"),
    ],
)
def test_a_failed_read_is_a_reason_never_an_empty_list(wait_ci, monkeypatch, answer, reason):
    monkeypatch.setattr(wait_ci.subprocess, "run", lambda *a, **k: answer)
    with pytest.raises(wait_ci.ReadFailed, match=reason):
        wait_ci.pull_request_runs("owner/name", "abc123")


def test_a_good_read_returns_the_runs(wait_ci, monkeypatch):
    answer = _Answer(0, stdout='{"total_count": 1, "workflow_runs": [{"name": "ci"}]}')
    monkeypatch.setattr(wait_ci.subprocess, "run", lambda *a, **k: answer)
    assert wait_ci.pull_request_runs("owner/name", "abc123") == [{"name": "ci"}]


def test_reads_that_keep_failing_end_unread_long_before_the_timeout(wait_ci):
    clock = _Clock()

    def read():
        raise wait_ci.ReadFailed("gh: HTTP 403 Forbidden")

    state, line = wait_ci.wait(read, timeout=3600, every=60, sleep=clock.sleep, clock=clock)
    assert state == wait_ci.UNREAD
    assert "HTTP 403" in line and "no pull request run" not in line
    assert clock.sleeps == wait_ci.READ_FAILURES - 1


def test_one_failed_read_is_waited_past(wait_ci):
    clock = _Clock()
    answers = iter(["fail", [_run("ci")]])

    def read():
        answer = next(answers)
        if answer == "fail":
            raise wait_ci.ReadFailed("gh: HTTP 502")
        return answer

    state, _ = wait_ci.wait(read, timeout=600, every=60, sleep=clock.sleep, clock=clock)
    assert state == wait_ci.PASSED


def test_failures_count_in_a_row_only(wait_ci):
    clock = _Clock()
    script = ["fail", "fail", [], "fail", "fail", [_run("ci")]]
    answers = iter(script)

    def read():
        answer = next(answers)
        if answer == "fail":
            raise wait_ci.ReadFailed("gh: HTTP 502")
        return answer

    state, _ = wait_ci.wait(read, timeout=3600, every=60, sleep=clock.sleep, clock=clock)
    assert state == wait_ci.PASSED


def test_main_exits_3_when_the_runs_cannot_be_read(wait_ci, monkeypatch, capsys):
    def refused(repo, sha):
        raise wait_ci.ReadFailed("gh: HTTP 403 Forbidden")

    monkeypatch.setattr(wait_ci, "pull_request_runs", refused)
    assert wait_ci.main(["abc123", "--repo", "owner/name", "--every", "0"]) == 3
    assert capsys.readouterr().out.startswith("unread: ")
