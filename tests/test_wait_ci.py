"""`scripts/wait_ci.py` reads a head's pull request runs as one verdict (U196).

The REST answer is served by the test, and the clock and the sleep are replaced
so a timeout is measured without waiting.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from subprocess import CompletedProcess

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


def _pair(conclusion):
    return [_run("ci"), _run("board", conclusion=conclusion)]


@pytest.mark.parametrize(
    "runs, state, words",
    [
        ([], "pending", ["no pull request run"]),
        ([_run("ci"), _run("board", "in_progress", None)], "pending", ["1 of 2", "board"]),
        *[(_pair(c), "green", ["2 run(s)"]) for c in ("success", "neutral", "skipped")],
        *[
            (_pair(c), "red", [f"board {c}"])
            for c in ("failure", "cancelled", "timed_out", "action_required", None)
        ],
    ],
)
def test_the_verdict_on_one_head(wait_ci, runs, state, words):
    """No run yet is pending, never green; one run not green makes the head red."""
    got, line = wait_ci.verdict(runs)
    assert got == state
    assert all(word in line for word in words), line


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


def _wait(wait_ci, script, timeout=600):
    """Wait over ``script``, its last answer repeating; "fail" is a failed read."""
    clock, reads = _Clock(), iter(range(10**6))

    def read():
        answer = script[min(next(reads), len(script) - 1)]
        if answer == "fail":
            raise wait_ci.ReadFailed("gh: HTTP 403 Forbidden")
        return answer

    state, line = wait_ci.wait(read, timeout=timeout, every=60, sleep=clock.sleep, clock=clock)
    return state, line, clock


@pytest.mark.parametrize(
    "script, timeout, state, sleeps",
    [
        ([[], [_run("ci", "queued", None)], [_run("ci")]], 600, "green", 2),
        ([[_run("ci", conclusion="failure")]], 600, "red", 0),  # red without waiting
        ([[]], 300, "pending", 5),  # timed out, never sleeping past the deadline
        (["fail"], 3600, "unread", 2),  # long before the timeout, never told as no run
        # A failed read is waited past, and failures count in a row only.
        (["fail", "fail", [], "fail", "fail", [_run("ci")]], 3600, "green", 5),
    ],
)
def test_wait_reads_until_a_verdict_unread_or_timed_out(wait_ci, script, timeout, state, sleeps):
    got, line, clock = _wait(wait_ci, script, timeout)
    assert (got, clock.sleeps) == (state, sleeps)
    assert clock.now <= timeout
    if state == "pending":
        assert line.startswith("timed out")
    if state == "unread":
        assert "HTTP 403" in line and "no pull request run" not in line
        assert sleeps == wait_ci.READ_FAILURES - 1


def test_main_exits_by_verdict(wait_ci, monkeypatch, capsys):
    def refused(repo, sha):
        raise wait_ci.ReadFailed("gh: HTTP 403 Forbidden")

    for read, extra, code, prefix in [
        (lambda repo, sha: _pair("failure"), ["--every", "1", "--timeout", "1"], 1, "red: "),
        (lambda repo, sha: [], ["--every", "1", "--timeout", "0"], 2, "pending: "),
        (lambda repo, sha: [_run("ci")], [], 0, "green: "),
        (refused, ["--every", "0"], 3, "unread: "),
    ]:
        monkeypatch.setattr(wait_ci, "pull_request_runs", read)
        assert wait_ci.main(["abc123", "--repo", "owner/name", *extra]) == code
        assert capsys.readouterr().out.startswith(prefix)


def _answer(returncode=0, stdout="", stderr=""):
    return CompletedProcess([], returncode, stdout, stderr)


@pytest.mark.parametrize(
    "answer, reason",
    [
        (_answer(1, stderr="gh: HTTP 403 Forbidden\n"), "HTTP 403"),
        (_answer(1), "gh exited 1"),
        (_answer(0, stdout="<html>proxy</html>"), "not JSON"),
        (_answer(0, stdout='{"message": "Not Found"}'), "no workflow_runs"),
        (_answer(0, stdout="[]"), "no workflow_runs"),
        (FileNotFoundError(2, "No such file or directory", "gh"), "gh could not run"),
        (_answer(0, stdout='{"total_count": 1, "workflow_runs": [{"name": "ci"}]}'), None),
    ],
)
def test_a_failed_read_is_a_reason_never_an_empty_list(wait_ci, monkeypatch, answer, reason):
    def run(*a, **k):
        if isinstance(answer, Exception):
            raise answer
        return answer

    monkeypatch.setattr(wait_ci.subprocess, "run", run)
    if reason is None:
        assert wait_ci.pull_request_runs("owner/name", "abc123") == [{"name": "ci"}]
        return
    with pytest.raises(wait_ci.ReadFailed, match=reason):
        wait_ci.pull_request_runs("owner/name", "abc123")
