"""A throwaway suite in which a test queued behind a busy worker has to move.

U251 runs the suite with ``--dist worksteal``, and the mutation driver and
the Linux battery must read a run where tests really moved. Here
``tests/test_first.py`` opens with a test that holds its worker until a test
queued behind it in the same file has run on the other worker, which only a
steal can do; it gives up after a minute and fails, so a run with no move is
red. A steal takes the queue's TAIL, and the last queued test fails on
purpose, so the failure to report ran on a worker it was not first given.

``addopts`` are the repository's own with two workers; every test records its
worker in the directory ``LOG_VARIABLE`` names. The default distribution
usually moves a test too, so ``tests/test_suite_distribution.py`` pins the option.
"""

from __future__ import annotations

import json
import shlex
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The environment variable naming the directory each test records its worker in.
LOG_VARIABLE = "STEALING_SUITE_LOG"

#: The one test that fails, and the one that holds its worker.
STOLEN_FAILURE = "tests/test_first.py::test_queued_6"
HOLDER = "test_holds_its_worker"

#: Collected by a full run, and by the subset of the first three files.
FULL_COUNT = 16
SUBSET = ["tests/test_first.py", "tests/test_second.py", "tests/test_third.py"]
SUBSET_COUNT = 14

#: Variables an enclosing xdist worker or caller sets, which would otherwise
#: leak into the throwaway run and change what it is.
INHERITED_RUN_STATE = (
    "PYTEST_ADDOPTS",
    "PYTEST_XDIST_WORKER",
    "PYTEST_XDIST_WORKER_COUNT",
    "PYTEST_XDIST_TESTRUNUID",
)

_RECORD = '''import os
from pathlib import Path


def worker():
    return os.environ.get("PYTEST_XDIST_WORKER", "controller")


def record(name):
    """Write this test's worker atomically, so a reader never sees half a name."""
    log = Path(os.environ["{variable}"])
    partial = log / (name + ".partial")
    partial.write_text(worker(), encoding="utf-8")
    os.replace(partial, log / name)
'''

_FIRST = """import os
import time
from pathlib import Path

from stealing_record import record, worker


def {holder}():
    record("{holder}")
    log = Path(os.environ["{variable}"])
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        moved = [
            entry
            for entry in log.glob("test_queued_*")
            if not entry.name.endswith(".partial") and entry.read_text(encoding="utf-8") != worker()
        ]
        if moved:
            return
        time.sleep(0.05)
    raise AssertionError("no test queued behind this one ran on another worker in a minute")


def test_queued_1():
    record("test_queued_1")


def test_queued_2():
    record("test_queued_2")


def test_queued_3():
    record("test_queued_3")


def test_queued_4():
    record("test_queued_4")


def test_queued_5():
    record("test_queued_5")


def test_queued_6():
    record("test_queued_6")
    assert False, "the last queued test fails on purpose, so its report has to cross workers"
"""


def _passing(prefix: str, count: int) -> str:
    return "\n\n".join(f"def test_{prefix}_{n}():\n    pass\n" for n in range(1, count + 1))


def repository_addopts(root: Path = REPO_ROOT) -> list[str]:
    """The repository's own ``addopts``, split as pytest splits them."""
    with (root / "pyproject.toml").open("rb") as handle:
        data = tomllib.load(handle)
    raw = data["tool"]["pytest"]["ini_options"].get("addopts", "")
    return list(raw) if isinstance(raw, list) else shlex.split(raw)


def two_worker_addopts() -> list[str]:
    """The repository's ``addopts`` with two workers, the halves this suite relies on."""
    tokens = repository_addopts()
    for index, token in enumerate(tokens):
        if token in ("-n", "--numprocesses") and index + 1 < len(tokens):
            tokens[index + 1] = "2"
            return tokens
        if token.startswith("--numprocesses="):
            tokens[index] = "--numprocesses=2"
            return tokens
        if token.startswith("-n"):
            tokens[index] = "-n2"
            return tokens
    return [*tokens, "-n", "2"]


def write(root: Path) -> Path:
    """Write the suite into ``root``, which must not exist yet; returns ``root``."""
    tests = root / "tests"
    tests.mkdir(parents=True)
    addopts = shlex.join(two_worker_addopts())
    (root / "pyproject.toml").write_text(
        "[tool.pytest.ini_options]\n"
        'testpaths = ["tests"]\n'
        'pythonpath = ["tests"]\n'
        f"addopts = {json.dumps(addopts)}\n",
        encoding="utf-8",
    )
    (tests / "stealing_record.py").write_text(
        _RECORD.replace("{variable}", LOG_VARIABLE), encoding="utf-8"
    )
    (tests / "test_first.py").write_text(
        _FIRST.replace("{variable}", LOG_VARIABLE).replace("{holder}", HOLDER),
        encoding="utf-8",
    )
    (tests / "test_second.py").write_text(_passing("second", 5), encoding="utf-8")
    (tests / "test_third.py").write_text(_passing("third", 2), encoding="utf-8")
    (tests / "test_fourth.py").write_text(_passing("fourth", 2), encoding="utf-8")
    return root


def prepare_environment(monkeypatch, log: Path) -> None:
    """Point the suite's worker log at ``log`` and drop any enclosing run's state."""
    log.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv(LOG_VARIABLE, str(log))
    for name in INHERITED_RUN_STATE:
        monkeypatch.delenv(name, raising=False)


def workers(log: Path) -> dict[str, str]:
    """Each recorded test's name and the worker it ran on."""
    return {
        entry.name: entry.read_text(encoding="utf-8")
        for entry in log.iterdir()
        if not entry.name.endswith(".partial")
    }


def assert_the_failure_moved(log: Path) -> None:
    """The failing test ran on a different worker from the one that held."""
    seen = workers(log)
    assert HOLDER in seen and "test_queued_6" in seen, seen
    assert seen["test_queued_6"] != seen[HOLDER], seen
    assert {seen[HOLDER], seen["test_queued_6"]} <= {"gw0", "gw1"}, seen
