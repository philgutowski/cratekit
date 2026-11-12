"""A throwaway suite in which a test queued behind a busy worker has to move.

U251 runs the suite with ``--dist worksteal``: a worker that runs out of tests
takes half of the queue of the busiest one. The mutation driver and the Linux
battery both read a run's failures and counts, so each has to read a run in
which tests really moved between workers, and a fixture of fast tests may
finish before any worker goes idle and so never steals at all.

This suite cannot finish without a move. ``tests/test_first.py`` opens with a
test that holds its worker until one of the tests queued behind it in the same
file has run on another worker. Work stealing hands each of two workers half of
the collection in order, so all of ``test_first.py`` starts on one worker, and
the only way one of its queued tests reaches the other is a steal; the holding
test gives up after a minute and fails, so a run that never moved anything is
red rather than slow and green. A steal takes the TAIL of the busy worker's
queue, and the last queued test fails on purpose, so the one failure a reader
must report is a test that ran on a worker it was not first given to.

The suite's ``addopts`` are the repository's own with the worker count set to
two, so it runs under whatever distribution ``pyproject.toml`` names. Every
test records the worker it ran on in the directory ``LOG_VARIABLE`` names.

Under xdist's default distribution a queued test usually moves too, but not
every time, so a run of this suite does not tell the two distributions apart;
the two pins in ``tests/test_suite_distribution.py`` are what hold the option.
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
    """The repository's ``addopts`` with its worker count set to two.

    Two, not ``auto``: the split this suite relies on is halves, and a run of
    sixteen tests across every core of a large machine would spend its time
    starting workers.
    """
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
