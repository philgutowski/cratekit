"""Tests for ``scripts/mutate.py``, the mutation table driver.

This script certifies every future measurement on this project, so a defect here
is not one wrong table. It is every table the script ever writes, wrong and
confidently so. That is why these tests run against a THROWAWAY FIXTURE PACKAGE
with its own tiny suite and its own git repository, never against Cratekit's own
suite: a driver checked only against the suite it was written for has never once
been compared to a known answer.

The fixture is four functions and four tests, so every count in this file is one
a reader can verify by hand. Each test names the driver rule it is protecting.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import platformdirs
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_driver():
    """Load ``scripts/mutate.py`` by path.

    Same reason ``test_portability.py`` loads the repository scanner this way:
    it lives in ``scripts/`` because it runs standalone, and importing it as
    part of the package would put a review tool inside the shipped tree.

    The ``sys.modules`` registration is required rather than tidy: the driver
    declares dataclasses, and ``@dataclass`` resolves annotations by looking its
    own module up in ``sys.modules``. A module loaded by path and never
    registered is not there, and the decorator fails on a None.
    """
    spec = importlib.util.spec_from_file_location(
        "cratekit_mutate_driver", REPO_ROOT / "scripts" / "mutate.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mutate = _load_driver()


# ---------------------------------------------------------------------------
# The fixture package
# ---------------------------------------------------------------------------

GUARDS = '''"""Two guards and one function nothing tests."""


def clamp(value, limit=10):
    """Cap a value. The guard here is tested."""
    if value > limit:
        return limit
    return value


def floor(value, lowest=0):
    """A second guard, so an over-narrow old text has somewhere to be ambiguous."""
    if value < lowest:
        return lowest
    return value


def describe(value):
    """A message the suite asserts on with ``in``."""
    return f"value is {value}"


def unmeasured(value):
    """Nothing imports this, so mutating it kills nothing."""
    return value * 2
'''

OTHER = '''def always_true():
    return True
'''

TEST_GUARDS = '''from fixtpkg.guards import clamp, describe, floor


def test_clamp_caps_at_the_limit():
    assert clamp(50) == 10


def test_clamp_passes_a_small_value():
    assert clamp(3) == 3


def test_floor_raises_a_low_value():
    assert floor(-4) == 0


def test_describe_names_the_value():
    assert "value is 3" in describe(3)
'''

TEST_OTHER = '''from fixtpkg.other import always_true


def test_always_true():
    assert always_true()
'''

PYPROJECT = """[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-q"
"""

#: The fixture mirrors the exact `-q` hazard the real repository has, so the
#: driver's addopts stripping is exercised on every run rather than asserted once.


def _git(root: Path, *args: str) -> None:
    done = subprocess.run(
        ["git", "-c", "user.email=driver@test", "-c", "user.name=driver", *args],
        cwd=root,
        capture_output=True,
        check=False,
    )
    assert done.returncode == 0, done.stderr.decode()


TEST_ENVIRONMENT = '''"""Three tests that stand in for the 28 audio tests ffmpeg took down.

They pass only when the child process inherited the caller's environment. A
driver that built a fresh environment, or trimmed PATH, fails all three on the
full run while every subset row stays green, which reads as selective damage and
is not.
"""

import os


def test_tool_is_available_one():
    assert os.environ.get("MUTATE_FIXTURE_TOOL") == "present"


def test_tool_is_available_two():
    assert os.environ.get("MUTATE_FIXTURE_TOOL") == "present"


def test_tool_is_available_three():
    assert os.environ.get("MUTATE_FIXTURE_TOOL") == "present"
'''


TEST_SANDBOX = '''"""The child must start life in a throwaway installation state. R-343.

Two properties, both asserted from inside the child because the sandbox is
deleted the moment the driver's run returns and the parent cannot look into it
afterwards.
"""

import os
from pathlib import Path

import platformdirs

#: The CALLER's own value for each sandboxed variable, handed across under a
#: name the sandbox does not touch. Comparing against these, and not against a
#: sentinel made for the test, is what makes an absent sandbox fail: with no
#: redirect the child simply inherits these very values.
CALLER_PREFIX = "MUTATE_FIXTURE_CALLER_"


def _callers(name: str) -> Path:
    return Path(os.environ[CALLER_PREFIX + name])


def test_the_child_is_not_pointed_at_the_callers_installation_state():
    for name in ("HOME", "CRATEKIT_CONFIG_DIR", "CRATEKIT_STATE_DIR"):
        value = os.environ.get(name)
        assert value, f"{name} is unset in the child"
        resolved = Path(value)
        callers = _callers(name)
        assert resolved != callers, f"{name} is the caller's own"
        assert callers not in resolved.parents, f"{name} is under the caller's own"


def test_a_write_to_the_resolved_config_directory_lands_in_the_sandbox():
    """The exact 2026-09-20 shape, written by hand.

    A test that has undone the suite's isolation resolves this path and writes a
    configuration to it. What ``monkeypatch.undo()`` restores is the value the
    PROCESS started with, so this asserts the process started in a sandbox.
    platformdirs reads HOME on macOS, so this covers the HOME redirect
    specifically rather than the Cratekit overrides beside it.
    """
    resolved = Path(platformdirs.user_config_dir("cratekit"))
    resolved.mkdir(parents=True, exist_ok=True)
    (resolved / "config.toml").write_text("a fixture configuration", encoding="utf-8")

    callers_home = _callers("HOME")
    assert resolved != callers_home
    assert callers_home not in resolved.parents
'''

TEST_LEAK = '''"""A test that writes where it must not, so the guard has something to catch.

It writes ONLY on a mutated tree, which is what lets one fixture drive both the
leak named for a row and the clean baseline that has to precede it.
"""

import os
from pathlib import Path

from fixtpkg.guards import clamp


def test_writes_into_the_guarded_directory_only_when_the_guard_is_gone():
    if clamp(50) != 10:
        target = Path(os.environ["MUTATE_FIXTURE_LEAK_TARGET"])
        target.mkdir(parents=True, exist_ok=True)
        (target / "leaked.toml").write_text("a fixture configuration", encoding="utf-8")
'''


def _build_fixture(
    root: Path,
    *,
    red: bool = False,
    env_dependent: bool = False,
    sandbox: bool = False,
    leaky: bool = False,
) -> Path:
    """A committed git repository holding a four test package."""
    (root / "src" / "fixtpkg").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "pyproject.toml").write_text(PYPROJECT, encoding="utf-8")
    (root / "src" / "fixtpkg" / "__init__.py").write_text("", encoding="utf-8")
    (root / "src" / "fixtpkg" / "guards.py").write_text(GUARDS, encoding="utf-8")
    (root / "src" / "fixtpkg" / "other.py").write_text(OTHER, encoding="utf-8")
    (root / "tests" / "test_guards.py").write_text(TEST_GUARDS, encoding="utf-8")
    (root / "tests" / "test_other.py").write_text(TEST_OTHER, encoding="utf-8")
    if red:
        (root / "tests" / "test_red.py").write_text(
            "def test_that_fails():\n    assert False\n", encoding="utf-8"
        )
    if env_dependent:
        (root / "tests" / "test_environment.py").write_text(TEST_ENVIRONMENT, encoding="utf-8")
    if sandbox:
        (root / "tests" / "test_sandbox.py").write_text(TEST_SANDBOX, encoding="utf-8")
    if leaky:
        (root / "tests" / "test_leak.py").write_text(TEST_LEAK, encoding="utf-8")
    _git(root, "init", "-q", "-b", "main")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "fixture")
    return root


@pytest.fixture(scope="session")
def green_template(tmp_path_factory) -> Path:
    return _build_fixture(tmp_path_factory.mktemp("green-template"))


@pytest.fixture(scope="session")
def red_template(tmp_path_factory) -> Path:
    return _build_fixture(tmp_path_factory.mktemp("red-template"), red=True)


@pytest.fixture
def repo(green_template, tmp_path) -> Path:
    """A private copy of the green fixture, git history included."""
    target = tmp_path / "repo"
    shutil.copytree(green_template, target)
    return target


@pytest.fixture
def red_repo(red_template, tmp_path) -> Path:
    target = tmp_path / "red-repo"
    shutil.copytree(red_template, target)
    return target


@pytest.fixture(scope="session")
def env_template(tmp_path_factory) -> Path:
    return _build_fixture(tmp_path_factory.mktemp("env-template"), env_dependent=True)


@pytest.fixture
def env_repo(env_template, tmp_path) -> Path:
    target = tmp_path / "env-repo"
    shutil.copytree(env_template, target)
    return target


@pytest.fixture(scope="session")
def sandbox_template(tmp_path_factory) -> Path:
    return _build_fixture(tmp_path_factory.mktemp("sandbox-template"), sandbox=True)


@pytest.fixture
def sandbox_repo(sandbox_template, tmp_path) -> Path:
    target = tmp_path / "sandbox-repo"
    shutil.copytree(sandbox_template, target)
    return target


@pytest.fixture(scope="session")
def leak_template(tmp_path_factory) -> Path:
    return _build_fixture(tmp_path_factory.mktemp("leak-template"), leaky=True)


@pytest.fixture
def leak_repo(leak_template, tmp_path) -> Path:
    target = tmp_path / "leak-repo"
    shutil.copytree(leak_template, target)
    return target


GUARDS_FILE = "src/fixtpkg/guards.py"


def _row(row_id: str, old: str, new: str, **kwargs) -> "mutate.Row":
    return mutate.Row(
        id=row_id,
        description=kwargs.pop("description", f"fixture row {row_id}"),
        file=kwargs.pop("file", GUARDS_FILE),
        old=old,
        new=new,
        **kwargs,
    )


# ═══════════════════════════════════════════════════════════════════════════
# The fixture is what it claims to be
# ═══════════════════════════════════════════════════════════════════════════


def test_the_green_fixture_is_green_and_collects_five(repo):
    """Every count below is read against this one, so assert it first."""
    result = mutate.run_pytest(repo, None)
    assert result.is_green
    assert result.collected == 5


# ═══════════════════════════════════════════════════════════════════════════
# Applying a mutation: exact, unique, or refused
# ═══════════════════════════════════════════════════════════════════════════


def test_an_absent_old_text_is_refused(repo):
    """A row that cannot be applied must not silently become a zero row."""
    with pytest.raises(mutate.DriverRefusal, match="not present"):
        mutate.apply_mutation(GUARDS, "if value > 999:", "pass")


def test_an_ambiguous_old_text_is_refused(repo):
    """``return value`` appears in two functions here, exactly as it does in real code.

    A replacement that hit the wrong one of two identical sites still produces a
    number. The number is about an experiment nobody chose to run, which is
    worse than no number.
    """
    assert GUARDS.count("    return value\n") == 2
    with pytest.raises(mutate.DriverRefusal, match="appears 2 times"):
        mutate.apply_mutation(GUARDS, "    return value\n", "    return 0\n")


def test_a_refused_row_never_touches_the_file(repo):
    """The refusal happens before the write, so a bad row leaves no wreckage."""
    before = (repo / GUARDS_FILE).read_bytes()
    with pytest.raises(mutate.DriverRefusal):
        with mutate.mutated(repo, GUARDS_FILE, "if value > 999:", "pass"):
            pass  # pragma: no cover - the context manager never opens
    assert (repo / GUARDS_FILE).read_bytes() == before


def test_an_empty_old_text_is_reserved_for_the_control(repo):
    with pytest.raises(mutate.DriverRefusal, match="null control"):
        mutate.apply_mutation(GUARDS, "", "# anything")
    assert mutate.apply_mutation("a\n", "", "# tail\n", allow_append=True) == "a\n# tail\n"


# ═══════════════════════════════════════════════════════════════════════════
# Restore, on every path out of the block
# ═══════════════════════════════════════════════════════════════════════════


def test_restore_after_a_normal_row(repo):
    path = repo / GUARDS_FILE
    before = path.read_bytes()
    with mutate.mutated(repo, GUARDS_FILE, "if value > limit:", "if value > 10000:"):
        assert b"10000" in path.read_bytes()
    assert path.read_bytes() == before


def test_restore_after_an_exception_mid_row(repo):
    """A crash mid row must never leave a mutated file behind."""
    path = repo / GUARDS_FILE
    before = path.read_bytes()
    with pytest.raises(ZeroDivisionError):
        with mutate.mutated(repo, GUARDS_FILE, "if value > limit:", "if value > 10000:"):
            raise ZeroDivisionError("a row blew up")
    assert path.read_bytes() == before


def test_restore_after_a_keyboard_interrupt(repo):
    """The impatient operator path. ``finally`` covers it; drive it rather than assume it."""
    path = repo / GUARDS_FILE
    before = path.read_bytes()
    with pytest.raises(KeyboardInterrupt):
        with mutate.mutated(repo, GUARDS_FILE, "if value > limit:", "if value > 10000:"):
            raise KeyboardInterrupt
    assert path.read_bytes() == before


def test_restore_verification_fails_when_disk_does_not_match_head(repo):
    """The check itself has to bite, or it is decoration."""
    path = repo / GUARDS_FILE
    path.write_text(GUARDS + "\n# an edit git has never seen\n", encoding="utf-8")
    with pytest.raises(mutate.RestoreVerificationError, match="git show HEAD"):
        mutate.verify_restore(repo, GUARDS_FILE)


def test_a_dirty_target_makes_the_context_manager_refuse_at_restore(repo):
    """Restoring a contaminated snapshot is caught, because HEAD is the reference.

    A driver verifying against its own snapshot would call this restore correct.
    It restored the file to a state git has never seen.
    """
    path = repo / GUARDS_FILE
    path.write_text(GUARDS + "\n# uncommitted\n", encoding="utf-8")
    with pytest.raises(mutate.RestoreVerificationError):
        with mutate.mutated(repo, GUARDS_FILE, "if value > limit:", "if value > 10000:"):
            pass


# ═══════════════════════════════════════════════════════════════════════════
# Subset derivation
# ═══════════════════════════════════════════════════════════════════════════


def test_subset_derivation_picks_the_importing_test_files(repo):
    subset, why = mutate.derive_subset(repo, GUARDS_FILE)
    assert subset == ["tests/test_guards.py"]
    assert "fixtpkg.guards" in why


def test_subset_derivation_excludes_a_test_file_that_does_not_import(repo):
    subset, _ = mutate.derive_subset(repo, "src/fixtpkg/other.py")
    assert subset == ["tests/test_other.py"]


def test_a_mutated_test_file_is_its_own_subset(repo):
    subset, why = mutate.derive_subset(repo, "tests/test_guards.py")
    assert subset == ["tests/test_guards.py"] and "itself" in why


def test_an_unimported_module_falls_back_to_the_full_suite(repo):
    (repo / "src" / "fixtpkg" / "orphan.py").write_text("X = 1\n", encoding="utf-8")
    subset, why = mutate.derive_subset(repo, "src/fixtpkg/orphan.py")
    assert subset is None and "none found" in why


def test_dotted_module_reads_a_package_initializer_as_the_package():
    assert mutate.dotted_module("src/fixtpkg/__init__.py") == "fixtpkg"
    assert mutate.dotted_module("scripts/board.py") is None


# ═══════════════════════════════════════════════════════════════════════════
# The quiet flag hazard
# ═══════════════════════════════════════════════════════════════════════════


def test_addopts_is_stripped_of_quiet_and_nothing_else(repo):
    """A second ``-q`` becomes ``-qq`` and suppresses the summary line."""
    assert mutate.pytest_addopts(repo) == ""
    (repo / "pyproject.toml").write_text(
        PYPROJECT.replace('addopts = "-q"', 'addopts = "-q --strict-markers"'), encoding="utf-8"
    )
    assert mutate.pytest_addopts(repo) == "--strict-markers"


# ═══════════════════════════════════════════════════════════════════════════
# Measuring one row
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def baselines(repo):
    full = mutate.run_pytest(repo, None)
    subset = mutate.run_pytest(repo, ["tests/test_guards.py"])
    return full, subset


def test_a_row_that_kills_reports_its_node_ids(repo, baselines):
    """Node ids come off report objects, so a parametrized id survives intact."""
    full, subset = baselines
    result = mutate.measure_row(
        repo,
        _row("K1", "if value > limit:", "if value > 10000:"),
        ["tests/test_guards.py"],
        "importers",
        subset,
        full,
    )
    assert result.status == "killed"
    assert result.deaths == 1
    assert result.killed == ["tests/test_guards.py::test_clamp_caps_at_the_limit"]
    assert result.promoted is False
    assert result.runs == 1


def test_a_row_that_kills_zero_is_promoted_to_the_full_suite(repo, baselines):
    """A zero on a subset is not yet a zero. Promotion is the difference."""
    full, subset = baselines
    result = mutate.measure_row(
        repo,
        _row("Z1", "return value * 2", "return value * 3"),
        ["tests/test_guards.py"],
        "importers",
        subset,
        full,
    )
    assert result.status == "zero"
    assert result.deaths == 0
    assert result.promoted is True
    assert result.runs == 2
    assert result.collected == full.collected


def test_a_row_that_breaks_collection_is_flagged_not_reported_as_a_zero(repo, baselines):
    """The failure this driver exists for.

    A mutation that breaks the module's import takes the whole test file out of
    collection. Zero tests fail because zero tests ran, and a hand rolled driver
    writes down a calm, confident, entirely false zero.
    """
    full, subset = baselines
    result = mutate.measure_row(
        repo,
        _row("C1", "def describe(value):", "def describe(value:"),
        ["tests/test_guards.py"],
        "importers",
        subset,
        full,
    )
    assert result.status == "collect-error"
    assert result.collect_drift is True
    assert result.collected < result.baseline_collected
    assert result.promoted is False


# ═══════════════════════════════════════════════════════════════════════════
# Under parallel workers the driver measures the same things
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def parallel_repo(repo) -> Path:
    """The green fixture with the real repository's parallel ``addopts``.

    The driver inherits ``addopts``, so the day the battery went parallel every
    driver run did too. ``-p`` loads the reporting plugin in each worker as well
    as the controller, and a worker sees only its own share of the tests, so a
    plugin that let every process write the report would record whichever
    partial count flushed last. Committed, because the driver refuses a dirty
    target and should meet this fixture the way it meets the real tree.
    """
    pyproject = repo / "pyproject.toml"
    pyproject.write_text(
        PYPROJECT.replace('addopts = "-q"', 'addopts = "-q -n 2"'), encoding="utf-8"
    )
    _git(repo, "commit", "-am", "run the fixture suite across two workers")
    return repo


def test_the_collected_count_survives_parallel_workers(parallel_repo):
    assert mutate.pytest_addopts(parallel_repo) == "-n 2"
    result = mutate.run_pytest(parallel_repo, None)
    assert result.is_green
    assert result.collected == 5


def test_a_kill_under_parallel_workers_names_the_same_tests_as_a_serial_run(
    repo, baselines, tmp_path
):
    """Both runs mutate the same line, so the two death lists must be equal."""
    full, subset = baselines
    row = _row("K1", "if value > limit:", "if value > 10000:")
    serial = mutate.measure_row(repo, row, ["tests/test_guards.py"], "importers", subset, full)
    assert serial.deaths > 0, "the fixture row must kill, or this test compares nothing"

    pyproject = repo / "pyproject.toml"
    pyproject.write_text(
        PYPROJECT.replace('addopts = "-q"', 'addopts = "-q -n 2"'), encoding="utf-8"
    )
    _git(repo, "commit", "-am", "run the fixture suite across two workers")
    parallel_full = mutate.run_pytest(repo, None)
    parallel_subset = mutate.run_pytest(repo, ["tests/test_guards.py"])
    parallel = mutate.measure_row(
        repo, row, ["tests/test_guards.py"], "importers", parallel_subset, parallel_full
    )
    assert sorted(parallel.killed) == sorted(serial.killed)
    assert parallel.collected == serial.collected


def test_a_broken_collection_is_still_flagged_under_parallel_workers(parallel_repo):
    full = mutate.run_pytest(parallel_repo, None)
    subset = mutate.run_pytest(parallel_repo, ["tests/test_guards.py"])
    result = mutate.measure_row(
        parallel_repo,
        _row("C2", "def describe(value):", "def describe(value:"),
        ["tests/test_guards.py"],
        "importers",
        subset,
        full,
    )
    assert result.status == "collect-error"
    assert result.collect_drift is True
    assert result.collected < result.baseline_collected


def test_a_run_that_measured_nothing_is_not_a_refusal(repo):
    """An unmeasurable run and a rejected row are different states.

    A refusal means the row never ran and the tree was never touched. This means
    pytest ran and produced nothing readable, and folding the two together is
    how "I could not observe" becomes "there is nothing there".

    Measured, not assumed: a subset path with a typo in it makes pytest exit 4
    with an EMPTY report. Read as a result that is zero collected, zero failures
    and nothing flagged, which is indistinguishable from a green run, so every
    row naming that path would report a serene zero.
    """
    with pytest.raises(mutate.MeasurementFailure, match="nothing was measured"):
        mutate.run_pytest(repo, ["tests/test_does_not_exist.py"])
    assert not issubclass(mutate.MeasurementFailure, mutate.DriverRefusal)


def test_a_refused_row_is_recorded_as_refused_not_as_a_zero(repo, baselines):
    full, subset = baselines
    result = mutate.measure_row(
        repo,
        _row("A1", "    return value\n", "    return 0\n"),
        ["tests/test_guards.py"],
        "importers",
        subset,
        full,
    )
    assert result.status == "refused"
    assert result.deaths == 0
    assert result.runs == 0
    assert "appears 2 times" in result.note


# ═══════════════════════════════════════════════════════════════════════════
# The batch: baselines, the control, and the whole table
# ═══════════════════════════════════════════════════════════════════════════


def test_a_red_baseline_is_refused_and_the_failures_are_named(red_repo):
    """A batch measured against a red baseline reads every row as a death."""
    with pytest.raises(mutate.DriverRefusal, match="BASELINE IS NOT GREEN: 1 failing"):
        mutate.measure_batch(
            red_repo, "red", [_row("K1", "if value > limit:", "if value > 10000:")]
        )


def test_the_child_inherits_the_callers_environment(env_repo, monkeypatch):
    """Inherit and add, never build fresh.

    Three tests in this fixture read a variable that exists only in the calling
    shell. A driver that handed the child a constructed environment fails all
    three, which is the shape of the 2026-08-10 incident where a trimmed PATH
    dropped ffmpeg and took 28 audio tests with it.
    """
    monkeypatch.setenv("MUTATE_FIXTURE_TOOL", "present")
    result = mutate.run_pytest(env_repo, None)
    assert result.is_green
    assert result.collected == 8


def test_a_baseline_red_from_a_scrubbed_environment_is_refused_naming_the_count(
    env_repo, monkeypatch
):
    """The layer before the null control, and the one that stops the waste earliest.

    With the tool missing, the full run is red and every subset row is still
    green, so the damage reads as selective. The refusal has to name the count
    and say the batch is invalid, or the agent reads the deaths as signal.
    """
    monkeypatch.delenv("MUTATE_FIXTURE_TOOL", raising=False)
    subset = mutate.run_pytest(env_repo, ["tests/test_guards.py"])
    assert subset.is_green, "the subset is unaffected, which is what makes this dangerous"

    with pytest.raises(mutate.DriverRefusal) as caught:
        mutate.measure_batch(env_repo, "scrubbed", [_row("K1", "return value * 2", "return 0")])
    message = str(caught.value)
    assert "BASELINE IS NOT GREEN" in message
    assert "3 failing" in message
    assert "THE BATCH IS INVALID" in message
    assert "ENVIRONMENT" in message


def test_the_scrubbed_variables_are_named_in_the_table(repo):
    """A silent scrub is the same defect one variable smaller."""
    batch = mutate.measure_batch(repo, "envnote", [_row("K1", "if value > limit:", "if value > 1:")])
    markdown = mutate.render_markdown(batch)
    assert "PYTHONDONTWRITEBYTECODE=1" in markdown
    for name in mutate.SCRUBBED_ENV:
        assert name in markdown


# ═══════════════════════════════════════════════════════════════════════════
# The installation state the child must not reach. R-343.
# ═══════════════════════════════════════════════════════════════════════════


def _hand_the_callers_values_across(monkeypatch) -> None:
    """Give the fixture this process's own sandboxed values, under untouched names."""
    for name in ("HOME", "CRATEKIT_CONFIG_DIR", "CRATEKIT_STATE_DIR"):
        monkeypatch.setenv("MUTATE_FIXTURE_CALLER_" + name, os.environ[name])


def test_the_child_starts_in_a_sandboxed_installation_state(sandbox_repo, monkeypatch):
    """Every sandboxed variable points somewhere other than the caller's own.

    The assertions are inside the fixture's own suite, because the sandbox is
    deleted when the driver's run returns. A red run here IS the failure. The
    comparison is against this process's real values, because with no sandbox
    the child inherits exactly those, and a sentinel made for the test would
    still differ from them.
    """
    _hand_the_callers_values_across(monkeypatch)

    result = mutate.run_pytest(sandbox_repo, None)

    assert result.is_green, result.failure_ids()
    assert result.collected == 7


def test_a_child_writing_a_config_does_not_reach_the_callers_own(sandbox_repo, monkeypatch):
    """The regression test for 2026-09-20, asserted from the caller's side.

    The fixture resolves the platformdirs config directory and writes a
    configuration to it, which is exactly what destroyed the real one. Nothing
    may appear in this process's equivalent. Under the suite that equivalent is
    the conftest's temporary home, never the machine's own.
    """
    _hand_the_callers_values_across(monkeypatch)

    callers = Path(platformdirs.user_config_dir("cratekit"))
    before = sorted(p.name for p in callers.iterdir()) if callers.is_dir() else []

    result = mutate.run_pytest(sandbox_repo, None)

    assert result.is_green, result.failure_ids()
    after = sorted(p.name for p in callers.iterdir()) if callers.is_dir() else []
    assert after == before, "the child wrote into the caller's own installation state"


def test_a_leak_during_the_baseline_names_the_phase(leak_repo, monkeypatch, tmp_path):
    """A leak before any row has run cannot be blamed on a row."""
    guarded = tmp_path / "guarded"
    guarded.mkdir()
    monkeypatch.setenv("MUTATE_FIXTURE_LEAK_TARGET", str(guarded))
    # Reaching the baseline's child needs the write to happen on the clean tree,
    # which the fixture does only when the guard is already gone. Mutating the
    # file on disk before the batch starts is how the baseline sees it.
    target = leak_repo / GUARDS_FILE
    target.write_text(
        target.read_text(encoding="utf-8").replace("        return limit", "        return value"),
        encoding="utf-8",
    )

    guard = mutate.take_state_guard((guarded,))
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.measure_batch(
            leak_repo,
            "leak-baseline",
            [_row("K1", "if value < lowest:", "if value < 1:")],
            allow_dirty=True,
            guard=guard,
        )

    message = str(caught.value)
    assert "the full baseline" in message
    assert str(guarded) in message
    assert "R-343" in message


def test_a_leak_under_a_row_names_that_row_and_stops_the_batch(
    leak_repo, monkeypatch, tmp_path
):
    """The row is named, the batch stops, and the tree is left clean.

    The fixture writes only on a mutated tree, so the baseline and the null
    control pass through untouched and the first child that leaks is the row's.
    """
    guarded = tmp_path / "guarded"
    guarded.mkdir()
    (guarded / "config.toml").write_text("the real configuration", encoding="utf-8")
    monkeypatch.setenv("MUTATE_FIXTURE_LEAK_TARGET", str(guarded))

    guard = mutate.take_state_guard((guarded,))
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.measure_batch(
            leak_repo,
            "leak-row",
            [_row("LEAKY", "        return limit", "        return value")],
            guard=guard,
        )

    message = str(caught.value)
    assert "row LEAKY" in message
    assert "the full baseline" not in message

    # The abort must not also leave a mutant, which is the failure mode that
    # made a driver exit clean over a contaminated tree once before.
    assert (leak_repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS
    assert mutate.dirty_targets(leak_repo, [GUARDS_FILE]) == []


def test_the_guard_is_reported_in_the_table_when_nothing_moved(repo, tmp_path):
    """A guard that passes silently is the same defect one layer up."""
    guarded = tmp_path / "guarded"
    guarded.mkdir()
    (guarded / "config.toml").write_text("the real configuration", encoding="utf-8")

    batch = mutate.measure_batch(
        repo,
        "guardnote",
        [_row("K1", "if value > limit:", "if value > 1:")],
        guard=mutate.take_state_guard((guarded,)),
    )
    markdown = mutate.render_markdown(batch)

    assert "the watched roots are unchanged" in markdown
    assert str(guarded) in markdown
    assert "1 entries" in markdown
    assert "not seen by this guard" in markdown, "the claim must say what it does not cover"
    assert "reused from a prior sidecar" not in markdown
    assert batch.to_dict()["state_guarded"]
    assert batch.to_dict()["reused_rows"] == 0


def test_the_guarded_root_is_written_into_the_table_without_the_home_directory(
    repo, tmp_path, monkeypatch
):
    """The table and sidecar land in docs/mutation, which the repository scan reads.

    Written raw, the account name in the home path failed the cleanliness test
    on every promoted row's full suite run, and four rows of this unit's own
    table reported a death that was that test alone.
    """
    home = tmp_path / "home"
    guarded = home / "Library" / "Application Support" / "cratekit"
    guarded.mkdir(parents=True)
    monkeypatch.setattr(mutate.Path, "home", classmethod(lambda cls: home))

    batch = mutate.measure_batch(
        repo,
        "portable",
        [_row("K1", "if value > limit:", "if value > 1:")],
        guard=mutate.take_state_guard((guarded,)),
    )
    markdown = mutate.render_markdown(batch)

    assert str(home) not in markdown
    assert str(home) not in json.dumps(batch.to_dict())
    assert "~/Library/Application Support/cratekit" in markdown
    assert mutate.portable(tmp_path / "elsewhere") == str(tmp_path / "elsewhere")


def test_rows_reused_on_resume_are_named_as_unwatched_in_the_table(repo, tmp_path):
    """A resumed row was measured by an earlier process whose children this run never saw."""
    guarded = tmp_path / "guarded"
    guarded.mkdir()
    rows = [_row("K1", "if value > limit:", "if value > 1:")]
    first = mutate.measure_batch(repo, "resume", rows, guard=mutate.take_state_guard((guarded,)))

    resumed = mutate.measure_batch(
        repo, "resume", rows, prior=first.to_dict(), guard=mutate.take_state_guard((guarded,))
    )
    markdown = mutate.render_markdown(resumed)

    assert resumed.reused_rows == 1
    assert "1 row(s) were reused from a prior sidecar" in markdown
    assert "did not watch" in markdown


def test_a_directory_created_inside_the_real_root_is_a_leak(tmp_path):
    """The jobs directory is made before the first job is written into it."""
    root = tmp_path / "real"
    root.mkdir()
    (root / "config.toml").write_text("the real configuration", encoding="utf-8")
    guard = mutate.take_state_guard((root,))

    (root / "jobs").mkdir()
    with pytest.raises(mutate.StateLeak):
        mutate.check_state_guard(guard, label="a child that made a directory")


def test_a_same_size_rewrite_of_a_small_file_is_a_leak(tmp_path):
    """The 2026-09-20 overwrite kept the path and could have kept the size.

    Content is hashed for small files precisely so this does not depend on the
    filesystem's timestamp granularity, so the timestamps are pinned back to
    their old values here to prove the hash alone carries it.
    """
    root = tmp_path / "real"
    root.mkdir()
    config = root / "config.toml"
    config.write_text("pin = 1", encoding="utf-8")
    before = config.stat()
    guard = mutate.take_state_guard((root,))

    config.write_text("pin = 2", encoding="utf-8")
    os.utime(config, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert config.stat().st_size == before.st_size

    with pytest.raises(mutate.StateLeak):
        mutate.check_state_guard(guard, label="a same size rewrite")


def test_a_child_that_leaks_and_then_hangs_is_still_caught(tmp_path, monkeypatch):
    """TimeoutExpired must not leave run_pytest before the guard has looked.

    Otherwise the row loop files the timeout as an ordinary error row, the next
    row's child runs on the damaged machine, and that row is the one blamed.
    """
    root = tmp_path / "real"
    root.mkdir()
    guard = mutate.take_state_guard((root,))

    def leak_then_hang(command, **kwargs):
        (root / "config.toml").write_text("a fixture configuration", encoding="utf-8")
        raise subprocess.TimeoutExpired(command, kwargs.get("timeout", 0))

    monkeypatch.setattr(mutate.subprocess, "run", leak_then_hang)
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.run_pytest(tmp_path, None, timeout=1, guard=guard, label="row HANG")
    assert "row HANG" in str(caught.value)


def test_the_sandbox_covers_every_variable_the_conftest_isolates():
    """SANDBOXED_ENV is a hand copy of the conftest's table, so pin the two together.

    A variable added to the conftest's isolation and not here would be exactly
    the R-343 mechanism reopened for that one root: undone in a test, restored
    to the real machine, unwatched.
    """
    source = (Path(__file__).parent / "conftest.py").read_text(encoding="utf-8")
    start = source.index("def _isolate_state_roots(")
    end = source.index("def _isolate_keychain(", start)
    body = source[start:end]
    isolated = set(re.findall(r'monkeypatch\.setenv\(\s*"([A-Z_]+)"', body))
    isolated |= set(re.findall(r'\(\s*"([A-Z_]+)",\s*"[a-z]+"\s*\)', body))

    assert isolated, "the conftest's isolation table was not found"
    assert isolated <= set(mutate.SANDBOXED_ENV), sorted(isolated - set(mutate.SANDBOXED_ENV))


def test_the_sandboxed_variables_are_named_in_the_table(repo):
    """The same rule the scrub note lives by, applied to what is ADDED."""
    batch = mutate.measure_batch(
        repo, "addednote", [_row("K1", "if value > limit:", "if value > 1:")]
    )
    markdown = mutate.render_markdown(batch)
    for name in mutate.SANDBOXED_ENV:
        assert name in markdown, name


def test_an_absent_installation_state_that_a_child_creates_is_a_leak(tmp_path):
    """Reaching the real path at all is the thing being guarded against.

    A machine with no configuration yet is the state every machine starts in,
    and a child that creates the directory there has still reached it.
    """
    absent = tmp_path / "not-yet"
    guard = mutate.take_state_guard((absent,))
    mutate.check_state_guard(guard, label="a clean child")

    absent.mkdir()
    with pytest.raises(mutate.StateLeak):
        mutate.check_state_guard(guard, label="a child that created it")


def test_the_guarded_roots_follow_the_overrides_this_process_carries(monkeypatch, tmp_path):
    """Which is what keeps this suite off the real machine's own directory."""
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfg"))
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "state"))
    assert mutate.installation_state_roots() == (tmp_path / "cfg", tmp_path / "state")

    # macOS answers both platformdirs calls with one directory, so a resolved
    # pair that agrees must collapse to a single root rather than be walked twice.
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "cfg"))
    assert mutate.installation_state_roots() == (tmp_path / "cfg",)


def test_a_red_subset_baseline_is_refused_even_when_the_full_suite_is_green(repo):
    """The same trap at row scale, and a full suite baseline alone cannot see it.

    The planted shape is an order dependent test: ``test_zorder`` passes on the
    full run because ``test_guards`` sets a flag first, and fails when its own
    subset runs without it. A driver that baselined only the whole suite would
    read that failure as a death on every row touching ``other.py``.
    """
    (repo / "src" / "fixtpkg" / "state.py").write_text("READY = False\n", encoding="utf-8")
    (repo / "tests" / "test_guards.py").write_text(
        "import fixtpkg.state\n"
        + TEST_GUARDS
        + "\n\ndef test_sets_ready():\n    fixtpkg.state.READY = True\n",
        encoding="utf-8",
    )
    (repo / "tests" / "test_zorder.py").write_text(
        "import fixtpkg.state\n"
        "from fixtpkg.other import always_true\n\n\n"
        "def test_needs_an_earlier_file():\n"
        "    assert fixtpkg.state.READY and always_true()\n",
        encoding="utf-8",
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "an order dependent test")

    assert mutate.run_pytest(repo, None).is_green, "the whole suite is green, which is the point"
    subset, _ = mutate.derive_subset(repo, "src/fixtpkg/other.py")
    assert subset == ["tests/test_other.py", "tests/test_zorder.py"]

    with pytest.raises(mutate.DriverRefusal, match="subset baseline"):
        mutate.measure_batch(
            repo, "redsubset", [_row("K1", "return True", "return False", file="src/fixtpkg/other.py")]
        )


def test_uncommitted_changes_to_a_target_are_refused(repo):
    (repo / GUARDS_FILE).write_text(GUARDS + "\n# uncommitted\n", encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="uncommitted changes"):
        mutate.measure_batch(repo, "dirty", [_row("K1", "if value > limit:", "if value > 10000:")])


def test_an_untracked_target_is_refused(repo):
    (repo / "src" / "fixtpkg" / "new.py").write_text("X = 1\n", encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="HEAD"):
        mutate.measure_batch(
            repo, "untracked", [_row("K1", "X = 1", "X = 2", file="src/fixtpkg/new.py")]
        )


def test_the_null_control_runs_automatically_and_kills_zero(repo):
    """The control is the check that makes every other number believable."""
    batch = mutate.measure_batch(repo, "control", [_row("K1", "return value * 2", "return 0")])
    assert batch.valid is True
    assert batch.control is not None
    assert batch.control.id == "NULL_CONTROL"
    assert batch.control.deaths == 0
    assert batch.control.status == "zero"
    assert (repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS


def test_a_null_control_that_kills_invalidates_the_whole_batch(repo, monkeypatch):
    """The 2026-08-10 trap, reproduced.

    A scratch copy carrying no ``.git`` failed a repository cleanliness test and
    made every row, including impossible ones, show one death. Here the same
    shape is planted: a test that fails whenever the guards file grows. The
    control catches it, the batch is declared invalid, and no rows run.
    """
    monkeypatch.setattr(
        mutate,
        "NULL_CONTROL_COMMENT",
        "\n# a control that is not a control\n",
    )
    (repo / "tests" / "test_cleanliness.py").write_text(
        "from pathlib import Path\n\n\n"
        "def test_no_stray_comment():\n"
        "    text = Path('src/fixtpkg/guards.py').read_text()\n"
        "    assert 'not a control' not in text\n",
        encoding="utf-8",
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "a test that reacts to any edit")

    batch = mutate.measure_batch(repo, "bad", [_row("K1", "return value * 2", "return 0")])
    assert batch.valid is False
    assert "null control killed 1" in batch.invalid_reason
    assert batch.results == []


def test_a_full_batch_measures_every_row_and_restores_the_tree(repo):
    """One end to end run: a killer, a zero, a collection breaker, a refusal."""
    rows = [
        _row("K1", "if value > limit:", "if value > 10000:", surface="user"),
        _row("Z1", "return value * 2", "return value * 3", surface="maintainer"),
        _row("C1", "def describe(value):", "def describe(value:"),
        _row("A1", "    return value\n", "    return 0\n"),
    ]
    dropped = [mutate.Dropped(id="D1", description="A fifth row.", reason="below the cap")]
    batch = mutate.measure_batch(repo, "endtoend", rows, dropped)

    assert batch.valid is True
    by_id = {one.id: one for one in batch.results}
    assert by_id["K1"].status == "killed" and by_id["K1"].deaths == 1
    assert by_id["Z1"].status == "zero" and by_id["Z1"].promoted is True
    assert by_id["C1"].status == "collect-error"
    assert by_id["A1"].status == "refused"

    # Nothing survives the batch on disk.
    assert (repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS
    assert mutate.dirty_targets(repo, [GUARDS_FILE]) == []

    markdown = mutate.render_markdown(batch)
    assert "## Considered and dropped" in markdown
    assert "`D1`" in markdown
    assert "collection error" in markdown
    assert "Null control" in markdown


def test_a_user_facing_zero_without_a_composite_is_called_out(repo):
    """METHOD's severity floor, encoded: a user facing zero owes a composite."""
    rows = [_row("Z1", "return value * 2", "return value * 3", surface="user")]
    batch = mutate.measure_batch(repo, "zeronote", rows)
    note = mutate.composite_note(batch, batch.results[0])
    assert "NO COMPOSITE" in note
    assert "NO COMPOSITE" in mutate.render_markdown(batch)


def test_a_maintainer_facing_zero_is_exempt_and_says_so(repo):
    rows = [_row("Z1", "return value * 2", "return value * 3")]
    batch = mutate.measure_batch(repo, "zeroexempt", rows)
    assert "composite not required" in mutate.composite_note(batch, batch.results[0])


def test_a_paired_composite_is_reported_with_its_partner_count(repo):
    rows = [
        _row("Z1", "return value * 2", "return value * 3", surface="user"),
        _row("Z1C", "if value < lowest:", "if value < -10000:", pairs_with="Z1"),
    ]
    batch = mutate.measure_batch(repo, "paired", rows)
    note = mutate.composite_note(batch, batch.results[0])
    assert "paired with `Z1C`, which killed 1" == note


def test_outputs_land_as_markdown_and_a_json_sidecar(repo, tmp_path):
    batch = mutate.measure_batch(repo, "written", [_row("K1", "if value > limit:", "if value > 1:")])
    markdown, sidecar = mutate.write_outputs(batch, tmp_path / "docs" / "mutation")
    assert markdown.name == "written.md" and sidecar.name == "written.json"
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["rows"][0]["id"] == "K1"
    assert data["valid"] is True
    assert data["control"]["deaths"] == 0
    # Full descriptions, not only counts.
    assert "fixture row K1" in markdown.read_text(encoding="utf-8")


def test_resume_reuses_a_row_whose_text_has_not_changed(repo):
    row = _row("K1", "if value > limit:", "if value > 10000:")
    first = mutate.measure_batch(repo, "resume", [row])
    prior = first.to_dict()
    prior["rows"][0]["deaths"] = 99  # a marker only a reused row can carry
    second = mutate.measure_batch(repo, "resume", [row], prior=prior)
    assert second.results[0].deaths == 99


def test_the_sidecar_is_written_after_every_row_not_only_at_the_end(repo, tmp_path):
    """A batch here runs for minutes. A sidecar written only on success resumes nothing."""
    progress = tmp_path / "docs" / "mutation" / "progress.json"
    rows = [
        _row("K1", "if value > limit:", "if value > 10000:"),
        _row("K2", "if value < lowest:", "if value < -10000:"),
    ]
    mutate.measure_batch(repo, "progress", rows, progress_path=progress)
    written = json.loads(progress.read_text(encoding="utf-8"))
    assert [one["id"] for one in written["rows"]] == ["K1", "K2"]
    assert written["control"]["deaths"] == 0


def test_resume_re_measures_a_row_whose_text_changed(repo):
    first = mutate.measure_batch(repo, "resume", [_row("K1", "if value > limit:", "if value > 1:")])
    prior = first.to_dict()
    prior["rows"][0]["deaths"] = 99
    edited = _row("K1", "if value > limit:", "if value > 10000:")
    second = mutate.measure_batch(repo, "resume", [edited], prior=prior)
    assert second.results[0].deaths == 1


# ═══════════════════════════════════════════════════════════════════════════
# Loading rows
# ═══════════════════════════════════════════════════════════════════════════


def test_a_toml_spec_round_trips(tmp_path):
    spec = tmp_path / "rows.toml"
    spec.write_text(
        'name = "u34-round-2"\n'
        'pass_kind = "light"\n\n'
        "[[rows]]\n"
        'id = "G1"\n'
        'description = "Drop the guard"\n'
        'file = "src/fixtpkg/guards.py"\n'
        'surface = "user"\n'
        "old = '''if value > limit:'''\n"
        'new = ""\n\n'
        "[[dropped]]\n"
        'id = "D1"\n'
        'description = "Another guard."\n'
        'reason = "ranked below the cap"\n',
        encoding="utf-8",
    )
    name, pass_kind, rows, dropped = mutate.load_spec(spec)
    assert (name, pass_kind) == ("u34-round-2", "light")
    assert rows[0].id == "G1" and rows[0].surface == "user" and rows[0].new == ""
    assert dropped[0].reason == "ranked below the cap"


def test_a_json_spec_loads_the_same_way(tmp_path):
    spec = tmp_path / "rows.json"
    spec.write_text(
        json.dumps(
            {
                "name": "j",
                "rows": [
                    {
                        "id": "G1",
                        "description": "d",
                        "file": "src/fixtpkg/guards.py",
                        "old": "a",
                        "new": "b",
                        "tests": ["tests/test_guards.py"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    _, _, rows, _ = mutate.load_spec(spec)
    assert rows[0].tests == ("tests/test_guards.py",)


def test_duplicate_row_ids_are_refused(tmp_path):
    spec = tmp_path / "rows.json"
    body = {"id": "G1", "description": "d", "file": "f.py", "old": "a", "new": "b"}
    spec.write_text(json.dumps({"rows": [body, dict(body)]}), encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="duplicate row id"):
        mutate.load_spec(spec)


def test_exceeding_the_pass_cap_is_refused_and_names_the_log(tmp_path):
    """METHOD caps a light pass at 25 rows. Nominal scoping did not hold."""
    spec = tmp_path / "rows.json"
    rows = [
        {"id": f"G{n}", "description": "d", "file": "f.py", "old": "a", "new": "b"}
        for n in range(26)
    ]
    spec.write_text(json.dumps({"pass_kind": "light", "rows": rows}), encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="exceeds the light pass cap"):
        mutate.load_spec(spec)


def test_a_pairs_with_naming_no_row_is_refused(tmp_path):
    spec = tmp_path / "rows.json"
    spec.write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "id": "G1",
                        "description": "d",
                        "file": "f.py",
                        "old": "a",
                        "new": "b",
                        "pairs_with": "nobody",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(mutate.DriverRefusal, match="pairs_with"):
        mutate.load_spec(spec)


def test_a_batch_with_no_python_target_cannot_produce_a_control(tmp_path):
    """No control, no batch. The control is not optional."""
    with pytest.raises(mutate.DriverRefusal, match="null control needs a Python target"):
        mutate.null_control_row([_row("D1", "a", "b", file="docs/notes.md")])
