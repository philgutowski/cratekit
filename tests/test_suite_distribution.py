"""The suite's idle workers take queued tests from a busy one. U251.

Under xdist's default distribution a worker that draws a long test keeps the
tests queued behind it while the others sit idle, so a full run ends when the
unluckiest queue drains. Measured 2026-11-12 on a four core container, one run
each way: 789 seconds against 629, and a spread between the workers' summed
test seconds of 178 against 67. ``--dist worksteal`` lets an idle worker take
half of the busiest one's queue.

These pin the option where every reader of it looks: pytest's own ``addopts``,
the mutation driver's copy of them, and a real run in which a test had to move.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

from tests import _stealing_suite as stealing

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _option(tokens: list[str], flag: str) -> str | None:
    """The value given to ``flag``, written as two tokens or as ``flag=value``."""
    for index, token in enumerate(tokens):
        if token == flag and index + 1 < len(tokens):
            return tokens[index + 1]
        if token.startswith(f"{flag}="):
            return token.split("=", 1)[1]
    return None


def test_the_suite_runs_on_every_core_and_steals_queued_work():
    tokens = stealing.repository_addopts()
    assert _option(tokens, "-n") == "auto", tokens
    assert _option(tokens, "--dist") == "worksteal", tokens


def test_the_mutation_driver_passes_the_distribution_on():
    """The driver rebuilds ``addopts`` for its children, stripped of ``-q``.

    Stripping and not clearing is what carries this option to every baseline
    and row run with no edit to the driver; this pins that it still does.
    """
    mutate = _load("cratekit_mutate_driver_u251", REPO_ROOT / "scripts" / "mutate.py")
    tokens = mutate.pytest_addopts(REPO_ROOT).split()
    assert _option(tokens, "-n") == "auto", tokens
    assert _option(tokens, "--dist") == "worksteal", tokens


def test_a_run_whose_tests_moved_reports_every_test_once(tmp_path, monkeypatch):
    """A plain run of the stealing suite: the moved failure, and the right count."""
    suite = stealing.write(tmp_path / "suite")
    log = tmp_path / "log"
    stealing.prepare_environment(monkeypatch, log)
    done = subprocess.run(
        [sys.executable, "-m", "pytest", "--tb=no", "-rfE", "-p", "no:cacheprovider"],
        cwd=suite,
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    failures = [line for line in done.stdout.splitlines() if line.startswith(("FAILED", "ERROR"))]
    assert [line.split()[1] for line in failures] == [stealing.STOLEN_FAILURE], done.stdout
    assert f"1 failed, {stealing.FULL_COUNT - 1} passed" in done.stdout, done.stdout
    stealing.assert_the_failure_moved(log)
