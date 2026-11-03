"""Tests for ``scripts/cloud_battery.py``, the Linux battery read against the base.

U200, from R-1191: a cloud clone is shallow, so a test that reads old history
failed on every base for want of it, the baseline recorded it as the machine's
by node id, and every later failure of that test was subtracted unread. The
battery now fetches the full history before it measures, refuses when it
cannot, and writes a baseline header that says so, which `compare` and the
mutation driver read before they subtract anything.

The clones here are real: a local repository with three commits, cloned at
depth one over ``file://`` so git really writes a shallow clone, and unshallowed
by the real fetch.
"""

from __future__ import annotations

import importlib.util
import socket
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_battery():
    """Load ``scripts/cloud_battery.py`` by path, as the driver's tests load it."""
    spec = importlib.util.spec_from_file_location(
        "cratekit_cloud_battery", REPO_ROOT / "scripts" / "cloud_battery.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


battery = _load_battery()


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-c", "user.email=battery@test", "-c", "user.name=battery", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def origin(tmp_path) -> tuple[Path, str]:
    """A repository on `main` with three commits; returns it and its first commit."""
    repo = tmp_path / "origin"
    repo.mkdir()
    assert _git(repo, "init", "-b", "main").returncode == 0
    for n in range(3):
        (repo / "f.txt").write_text(f"{n}\n", encoding="utf-8")
        assert _git(repo, "add", "f.txt").returncode == 0
        assert _git(repo, "commit", "-m", f"c{n}").returncode == 0
    first = _git(repo, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
    return repo, first


def _clone(origin_repo: Path, dest: Path, *, shallow: bool) -> Path:
    args = ["clone"]
    if shallow:
        args += ["--depth", "1"]
    done = _git(origin_repo.parent, *args, origin_repo.as_uri(), str(dest))
    assert done.returncode == 0, done.stderr
    return dest


def _is_shallow(repo: Path) -> str:
    return _git(repo, "rev-parse", "--is-shallow-repository").stdout.strip()


def test_a_shallow_clone_is_unshallowed_and_its_history_read_passes_after(origin, tmp_path):
    repo, first = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    assert _is_shallow(clone) == "true"
    assert _git(clone, "cat-file", "-e", first).returncode != 0, "the old commit is absent"

    assert battery.ensure_full_history(clone) is None

    assert _is_shallow(clone) == "false"
    assert _git(clone, "cat-file", "-e", first).returncode == 0


def test_a_remote_that_cannot_serve_the_history_is_refused(origin, tmp_path):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    repo.rename(tmp_path / "gone")

    reason = battery.ensure_full_history(clone)

    assert reason is not None
    assert "shallow" in reason
    assert _is_shallow(clone) == "true"


def test_a_complete_clone_runs_no_fetch(origin, tmp_path, monkeypatch):
    """Every git call is recorded, so a fetch is seen whether or not it succeeds.

    A None alone cannot show it, since a fetch that fails on a complete clone
    still leaves it complete, which the review of U200 drove.
    """
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=False)
    assert _is_shallow(clone) == "false"
    calls: list[list[str]] = []
    real_run = subprocess.run

    def recording_run(cmd, *args, **kwargs):
        calls.append(list(cmd))
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(battery.subprocess, "run", recording_run)

    assert battery.ensure_full_history(clone) is None
    assert calls, "ensure_full_history read nothing"
    assert not any("fetch" in cmd for cmd in calls), calls


def test_a_directory_git_cannot_read_is_refused_not_read_as_complete(tmp_path):
    """Absence is not evidence: an unreadable answer is a refusal, never `false`."""
    reason = battery.ensure_full_history(tmp_path)
    assert reason is not None


def test_a_baseline_that_cannot_fetch_the_history_writes_nothing(origin, tmp_path, monkeypatch):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    repo.rename(tmp_path / "gone")
    state = tmp_path / "state"
    monkeypatch.setattr(battery, "ROOT", clone)
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")

    def must_not_run(*_a, **_k):
        raise AssertionError("the suite ran on a shallow clone")

    monkeypatch.setattr(battery, "static_checks", must_not_run)
    monkeypatch.setattr(battery, "failing_ids", must_not_run)

    assert battery.cmd_baseline(None) == 1
    assert not (state / "baseline.txt").exists()


def test_a_baseline_header_says_it_was_measured_with_full_history(origin, tmp_path, monkeypatch):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    state = clone / ".cloud-battery"
    monkeypatch.setattr(battery, "ROOT", clone)
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    monkeypatch.setattr(battery, "failing_ids", lambda: ({"tests/a.py::t"}, "1 failed"))

    assert battery.cmd_baseline(None) == 0

    header = (state / "baseline.txt").read_text(encoding="utf-8").splitlines()[0]
    assert header.endswith(" history full")
    assert _is_shallow(clone) == "false"
    assert battery.read_baseline() == ({"tests/a.py::t"}, header.split()[2])


@pytest.mark.parametrize(
    "header",
    [
        "# commit abc123 host {host}",
        "# commit abc123 host {host} history shallow",
    ],
    ids=["before-u200", "shallow"],
)
def test_compare_refuses_a_baseline_not_measured_with_full_history(
    header, tmp_path, monkeypatch, capsys
):
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        header.format(host=socket.gethostname()) + "\n# 1 failed\ntests/a.py::t\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)

    def must_not_run(*_a, **_k):
        raise AssertionError("compare ran against a baseline it should refuse")

    monkeypatch.setattr(battery, "ensure_full_history", must_not_run)
    monkeypatch.setattr(battery, "failing_ids", must_not_run)

    assert battery.read_baseline() is None
    assert battery.cmd_compare(None) == 2
    assert "full history" in capsys.readouterr().out


def test_compare_refuses_a_branch_it_cannot_unshallow(origin, tmp_path, monkeypatch):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    repo.rename(tmp_path / "gone")
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} history full\ntests/a.py::t\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "ROOT", clone)
    monkeypatch.setattr(battery, "BASELINE", baseline)

    def must_not_run(*_a, **_k):
        raise AssertionError("the suite ran on a shallow clone")

    monkeypatch.setattr(battery, "static_checks", must_not_run)
    monkeypatch.setattr(battery, "failing_ids", must_not_run)

    assert battery.cmd_compare(None) == 1
