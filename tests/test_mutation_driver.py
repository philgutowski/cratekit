"""Tests for ``scripts/mutate.py``, the mutation table driver, and its part
``scripts/mutate_table.py``.

They run against a throwaway fixture package with its own tiny suite and git
repository, never Cratekit's suite, so every count is one a reader can check by
hand: four functions, four tests.
"""

from __future__ import annotations

import contextlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import platformdirs
import pytest

from tests import _stealing_suite as stealing

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load(name: str, filename: str):
    """A script loaded by path, registered because it declares dataclasses."""
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mutate = _load("cratekit_mutate_driver", "mutate.py")
battery = _load("cratekit_cloud_battery_for_the_driver", "cloud_battery.py")


@pytest.fixture(autouse=True)
def _stand_in_filesystem_root(tmp_path_factory, monkeypatch):
    """R-1917: in these tests the driver's guard lists a stand in for the filesystem root.

    Tests elsewhere in the suite make and remove a probe at the real root on Linux
    (``tests/test_doctor.py``), so a guard over the real one would read a parallel
    worker's probe as a leak. Returns the real root, for the one test that reads it.
    """
    real = mutate.FILESYSTEM_ROOT
    monkeypatch.setattr(mutate, "FILESYSTEM_ROOT", tmp_path_factory.mktemp("filesystem-root"))
    return real

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

#: The fixture carries the real repository's `-q` hazard, so every run strips it.
PYPROJECT = """[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-q"
"""

#: Three tests that pass only when the child inherited the caller's environment.
TEST_ENVIRONMENT = '''import os

import pytest


@pytest.mark.parametrize("n", [1, 2, 3])
def test_tool_is_available(n):
    assert os.environ.get("MUTATE_FIXTURE_TOOL") == "present"
'''

#: Asserted inside the child, since the sandbox is gone when the run returns.
#: Compared with the CALLER's own values, which an absent sandbox would inherit.
TEST_SANDBOX = '''import os
from pathlib import Path

import platformdirs


def _callers(name):
    return Path(os.environ["MUTATE_FIXTURE_CALLER_" + name])


def test_the_child_is_not_pointed_at_the_callers_installation_state():
    for name in ("HOME", "CRATEKIT_CONFIG_DIR", "CRATEKIT_STATE_DIR"):
        value = os.environ.get(name)
        assert value, f"{name} is unset in the child"
        resolved = Path(value)
        callers = _callers(name)
        assert resolved != callers, f"{name} is the caller's own"
        assert callers not in resolved.parents, f"{name} is under the caller's own"


def test_a_write_to_the_resolved_config_directory_lands_in_the_sandbox():
    resolved = Path(platformdirs.user_config_dir("cratekit"))
    resolved.mkdir(parents=True, exist_ok=True)
    (resolved / "config.toml").write_text("a fixture configuration", encoding="utf-8")
    callers_home = _callers("HOME")
    assert resolved != callers_home
    assert callers_home not in resolved.parents
'''

#: Writes where it must not, and only on a mutated tree.
TEST_LEAK = '''import os
from pathlib import Path

from fixtpkg.guards import clamp


def test_writes_into_the_guarded_directory_only_when_the_guard_is_gone():
    if clamp(50) != 10:
        target = Path(os.environ["MUTATE_FIXTURE_LEAK_TARGET"])
        target.mkdir(parents=True, exist_ok=True)
        (target / "leaked.toml").write_text("a fixture configuration", encoding="utf-8")
'''

#: Failing ids holding a space and the summary separator, beside a passing
#: sibling sharing everything before the space (U268).
TEST_RED_SPACED = '''import pytest


@pytest.mark.parametrize("case", ["one two", "one three", "x - y"])
def test_that_fails(case):
    assert case == "one three"
'''

#: Passes only off the memory root (U273), logs where each run put it, and dies
#: to a row dropping the clamp guard wherever it runs.
TEST_PLACED = '''import os
import tempfile

import pytest
from fixtpkg.guards import clamp


@pytest.fixture
def placed_resource():
    if os.environ.get("PLACED_ERROR_IN_MEMORY") == "1" and os.path.realpath(
        tempfile.gettempdir()
    ).startswith(os.environ["PLACED_MEMORY"] + os.sep):
        raise RuntimeError("cannot be set up in memory")
    return True


def test_needs_a_disk():
    where = os.path.realpath(tempfile.gettempdir())
    with open(os.environ["PLACED_LOG"], "a", encoding="utf-8") as log:
        log.write(where + "\\n")
    assert clamp(50) == 10
    assert not where.startswith(os.environ["PLACED_MEMORY"] + os.sep)


def test_errors_in_memory(placed_resource):
    assert placed_resource
'''

PLACED_ID = "tests/test_placed.py::test_needs_a_disk"
PLACED_ERRORING_ID = "tests/test_placed.py::test_errors_in_memory"
RED_ID = "tests/test_red.py::test_that_fails"
CLAMP_KILLED = ["tests/test_guards.py::test_clamp_caps_at_the_limit"]

#: The extra test file each fixture kind carries beside the green package.
KINDS = {
    "red": {"test_red.py": "def test_that_fails():\n    assert False\n"},
    "red_spaced": {"test_red.py": TEST_RED_SPACED},
    "env": {"test_environment.py": TEST_ENVIRONMENT},
    "sandbox": {"test_sandbox.py": TEST_SANDBOX},
    "leak": {"test_leak.py": TEST_LEAK},
    "placed": {"test_placed.py": TEST_PLACED},
}


def _git(root: Path, *args: str) -> None:
    done = subprocess.run(
        ["git", "-c", "user.email=driver@test", "-c", "user.name=driver", *args],
        cwd=root, capture_output=True, check=False,
    )
    assert done.returncode == 0, done.stderr.decode()


def _commit(root: Path, message: str) -> None:
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", message)


def _build_fixture(root: Path, extra: dict[str, str] | None = None) -> Path:
    """A committed git repository holding a four test package."""
    files = {
        "pyproject.toml": PYPROJECT,
        "src/fixtpkg/__init__.py": "",
        "src/fixtpkg/guards.py": GUARDS,
        "src/fixtpkg/other.py": "def always_true():\n    return True\n",
        "tests/test_guards.py": TEST_GUARDS,
        "tests/test_other.py": "from fixtpkg.other import always_true\n\n\n"
        "def test_always_true():\n    assert always_true()\n",
        **{f"tests/{name}": text for name, text in (extra or {}).items()},
    }
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    _git(root, "init", "-q", "-b", "main")
    _commit(root, "fixture")
    return root


def _copy(template: Path, target: Path) -> Path:
    shutil.copytree(template, target)
    return target


@pytest.fixture(scope="session")
def green_template(tmp_path_factory) -> Path:
    return _build_fixture(tmp_path_factory.mktemp("green-template"))


@pytest.fixture
def repo(green_template, tmp_path) -> Path:
    """A private copy of the green fixture, git history included."""
    return _copy(green_template, tmp_path / "repo")


@pytest.fixture(scope="session")
def templates(tmp_path_factory):
    made: dict[str, Path] = {}

    def template(kind: str) -> Path:
        if kind not in made:
            made[kind] = _build_fixture(tmp_path_factory.mktemp(f"{kind}-template"), KINDS[kind])
        return made[kind]

    return template


def _kind_fixture(kind: str):
    def fixture(templates, tmp_path) -> Path:
        return _copy(templates(kind), tmp_path / f"{kind}-repo")

    return pytest.fixture(name=f"{kind}_repo")(fixture)


red_repo = _kind_fixture("red")
red_spaced_repo = _kind_fixture("red_spaced")
env_repo = _kind_fixture("env")
sandbox_repo = _kind_fixture("sandbox")
leak_repo = _kind_fixture("leak")


@pytest.fixture
def places(tmp_path, monkeypatch) -> tuple[Path, Path]:
    """The battery's places read off a mount table of the test's own (U273):
    ``shm`` is a tmpfs and everything else ext4, the same on any machine."""
    root = tmp_path / "places"
    memory, disk = root / "shm", root / "disk"
    memory.mkdir(parents=True)
    disk.mkdir(parents=True)
    table = root / "mounts"
    table.write_text(
        f"/dev/vda / ext4 rw 0 0\ntmpfs {os.path.realpath(memory)} tmpfs rw 0 0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(mutate.BATTERY, "MOUNTS", table)
    monkeypatch.setattr(mutate.BATTERY, "MEMORY_ROOT", memory)
    monkeypatch.setattr(mutate.BATTERY, "MEMORY_FLOOR", 0)
    monkeypatch.setattr(mutate.BATTERY, "disk_root", lambda: disk)
    return memory, disk


@pytest.fixture
def placed_repo(templates, tmp_path, monkeypatch, places) -> tuple[Path, Path]:
    """The placed fixture in its own copy, and the log its test writes."""
    target = _copy(templates("placed"), tmp_path / "placed-repo")
    log = tmp_path / "placed.log"
    monkeypatch.setenv("PLACED_LOG", str(log))
    monkeypatch.setenv("PLACED_MEMORY", os.path.realpath(places[0]))
    return target, log


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


KILLER = ("K1", "if value > limit:", "if value > 10000:")
KILL = _row(*KILLER)


def _assert_untouched(repo: Path) -> None:
    assert (repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS
    assert mutate.dirty_targets(repo, [GUARDS_FILE]) == []


# The fixture, the surgery, and the subset


def test_the_green_fixture_is_green_and_collects_five(repo):
    result = mutate.run_pytest(repo, None)
    assert result.is_green
    assert result.collected == 5


def test_an_absent_ambiguous_or_empty_old_text_is_refused_before_any_write(repo):
    with pytest.raises(mutate.DriverRefusal, match="not present"):
        mutate.apply_mutation(GUARDS, "if value > 999:", "pass")
    # ``return value`` is in two functions, so a replacement would pick one blind.
    assert GUARDS.count("    return value\n") == 2
    with pytest.raises(mutate.DriverRefusal, match="appears 2 times"):
        mutate.apply_mutation(GUARDS, "    return value\n", "    return 0\n")
    with pytest.raises(mutate.DriverRefusal, match="null control"):
        mutate.apply_mutation(GUARDS, "", "# anything")
    assert mutate.apply_mutation("a\n", "", "# tail\n", allow_append=True) == "a\n# tail\n"
    before = (repo / GUARDS_FILE).read_bytes()
    with pytest.raises(mutate.DriverRefusal):
        with mutate.mutated(repo, GUARDS_FILE, "if value > 999:", "pass"):
            pass  # pragma: no cover - the context manager never opens
    assert (repo / GUARDS_FILE).read_bytes() == before


@pytest.mark.parametrize("raised", [None, ZeroDivisionError, KeyboardInterrupt])
def test_the_file_is_restored_on_every_path_out_of_the_block(repo, raised):
    path = repo / GUARDS_FILE
    before = path.read_bytes()
    with pytest.raises(raised) if raised else contextlib.nullcontext():
        with mutate.mutated(repo, GUARDS_FILE, "if value > limit:", "if value > 10000:"):
            assert b"10000" in path.read_bytes()
            if raised:
                raise raised
    assert path.read_bytes() == before


def test_a_restore_is_verified_against_head_not_against_its_snapshot(repo):
    path = repo / GUARDS_FILE
    path.write_text(GUARDS + "\n# an edit git has never seen\n", encoding="utf-8")
    with pytest.raises(mutate.RestoreVerificationError, match="git show HEAD"):
        mutate.verify_restore(repo, GUARDS_FILE)
    # A driver checking its own snapshot would call this restore correct.
    with pytest.raises(mutate.RestoreVerificationError):
        with mutate.mutated(repo, GUARDS_FILE, "if value > limit:", "if value > 10000:"):
            pass


def test_the_subset_is_the_importing_test_files_or_else_the_full_suite(repo):
    subset, why = mutate.derive_subset(repo, GUARDS_FILE)
    assert subset == ["tests/test_guards.py"] and "fixtpkg.guards" in why
    assert mutate.derive_subset(repo, "src/fixtpkg/other.py")[0] == ["tests/test_other.py"]
    subset, why = mutate.derive_subset(repo, "tests/test_guards.py")
    assert subset == ["tests/test_guards.py"] and "itself" in why
    (repo / "src" / "fixtpkg" / "orphan.py").write_text("X = 1\n", encoding="utf-8")
    subset, why = mutate.derive_subset(repo, "src/fixtpkg/orphan.py")
    assert subset is None and "none found" in why
    assert mutate.dotted_module("src/fixtpkg/__init__.py") == "fixtpkg"
    assert mutate.dotted_module("scripts/board.py") is None


def test_addopts_is_stripped_of_quiet_and_nothing_else(repo):
    assert mutate.pytest_addopts(repo) == ""
    (repo / "pyproject.toml").write_text(
        PYPROJECT.replace('addopts = "-q"', 'addopts = "-q --strict-markers"'), encoding="utf-8"
    )
    assert mutate.pytest_addopts(repo) == "--strict-markers"


# Measuring one row


def _baselines(repo: Path):
    return mutate.run_pytest(repo, None), mutate.run_pytest(repo, ["tests/test_guards.py"])


def _measure(repo: Path, baselines, *row):
    full, subset = baselines
    return mutate.measure_row(repo, _row(*row), ["tests/test_guards.py"], "importers", subset, full)


def test_one_row_kills_is_promoted_breaks_collection_or_is_refused(repo):
    baselines = _baselines(repo)
    killed = _measure(repo, baselines, *KILLER)
    assert (killed.status, killed.deaths, killed.promoted, killed.runs) == ("killed", 1, False, 1)
    assert killed.killed == CLAMP_KILLED

    zero = _measure(repo, baselines, "Z1", "return value * 2", "return value * 3")
    assert (zero.status, zero.deaths, zero.promoted, zero.runs) == ("zero", 0, True, 2)
    assert zero.collected == baselines[0].collected

    # A broken import takes its test file out of collection: zero ran, not zero died.
    broken = _measure(repo, baselines, "C1", "def describe(value):", "def describe(value:")
    assert (broken.status, broken.collect_drift, broken.promoted) == ("collect-error", True, False)
    assert broken.collected < broken.baseline_collected

    refused = _measure(repo, baselines, "A1", "    return value\n", "    return 0\n")
    assert (refused.status, refused.deaths, refused.runs) == ("refused", 0, 0)
    assert "appears 2 times" in refused.note


def test_parallel_workers_measure_what_a_serial_run_does(repo):
    """``-p`` loads the plugin in every worker, and a worker sees only its share."""
    serial = _measure(repo, _baselines(repo), *KILLER)
    assert serial.deaths > 0
    (repo / "pyproject.toml").write_text(
        PYPROJECT.replace('addopts = "-q"', 'addopts = "-q -n 2"'), encoding="utf-8"
    )
    _git(repo, "commit", "-am", "run the fixture suite across two workers")
    assert mutate.pytest_addopts(repo) == "-n 2"
    baselines = _baselines(repo)
    assert baselines[0].is_green and baselines[0].collected == 5
    parallel = _measure(repo, baselines, *KILLER)
    assert sorted(parallel.killed) == sorted(serial.killed)
    assert parallel.collected == serial.collected
    broken = _measure(repo, baselines, "C2", "def describe(value):", "def describe(value:")
    assert (broken.status, broken.collect_drift) == ("collect-error", True)
    assert broken.collected < broken.baseline_collected


def test_a_run_that_measured_nothing_is_not_a_refusal(repo):
    """A typo'd subset exits 4 with an EMPTY report, which would read as green."""
    with pytest.raises(mutate.MeasurementFailure, match="nothing was measured"):
        mutate.run_pytest(repo, ["tests/test_does_not_exist.py"])
    assert not issubclass(mutate.MeasurementFailure, mutate.DriverRefusal)


# The baseline, and the machine's known failures


def test_a_red_baseline_is_refused_and_the_failures_are_named(red_repo):
    with pytest.raises(mutate.DriverRefusal, match="BASELINE IS NOT GREEN: 1 failing"):
        mutate.measure_batch(red_repo, "red", [KILL])


def _listing(tmp_path: Path, header: str, *ids: str) -> Path:
    listed = tmp_path / "known.txt"
    listed.write_text(header + "\n" + "".join(f"{one}\n" for one in ids), encoding="utf-8")
    return listed


WHOLE = "# commit abc host here temp disk history full ids whole"


def test_a_baseline_red_only_by_the_machines_known_failures_is_green(red_repo, tmp_path, places):
    """The set is subtracted from every run, and never excuses a failure it does not name."""
    known = _listing(tmp_path, WHOLE, RED_ID)
    read = mutate.read_known_failures(known)
    assert read == frozenset({RED_ID})
    batch = mutate.measure_batch(red_repo, "red-known", [KILL], known=read, known_source=str(known))
    assert batch.valid, batch.invalid_reason
    assert batch.known_failures == 1
    assert "Temporary files: on disk, the place" in mutate.render_markdown(batch)
    row = batch.results[0]
    assert row.status == "killed"
    assert row.killed == CLAMP_KILLED
    not_it = frozenset({"tests/test_red.py::test_some_other"})
    with pytest.raises(mutate.DriverRefusal, match="BASELINE IS NOT GREEN"):
        mutate.measure_batch(red_repo, "red-still", [KILL], known=not_it)


def test_a_known_failure_whose_id_holds_a_space_is_subtracted_whole(
    red_spaced_repo, tmp_path, places
):
    """U268: cut at the first space, as the battery once kept them, they match nothing."""
    whole = sorted(
        {"tests/test_red.py::test_that_fails[one two]", "tests/test_red.py::test_that_fails[x - y]"}
    )
    known = _listing(tmp_path, WHOLE + "\n# 2 failed", *whole)
    read = mutate.read_known_failures(known)
    assert read == frozenset(whole)
    batch = mutate.measure_batch(
        red_spaced_repo, "spaced-known", [KILL], known=read, known_source=str(known)
    )
    assert batch.valid, batch.invalid_reason
    assert batch.known_failures == 2
    assert (batch.results[0].status, batch.results[0].killed) == ("killed", CLAMP_KILLED)
    cut = frozenset(
        {"tests/test_red.py::test_that_fails[one", "tests/test_red.py::test_that_fails[x"}
    )
    with pytest.raises(mutate.DriverRefusal, match="BASELINE IS NOT GREEN: 2 failing"):
        mutate.measure_batch(red_spaced_repo, "spaced-cut", [KILL], known=cut)


def test_a_zero_row_promoted_on_a_known_red_suite_stays_a_zero(red_repo):
    """The promoted full run reads the known set too, or the machine's failure is a kill."""
    rows = [_row("Z1", "return value * 2", "return value * 3", tests=("tests/test_guards.py",))]
    batch = mutate.measure_batch(red_repo, "red-zero", rows, known=frozenset({RED_ID}))
    assert batch.valid, batch.invalid_reason
    row = batch.results[0]
    assert (row.promoted, row.status, row.killed) == (True, "zero", [])


#: A spec the loader accepts, so a refusal after it is the known failures' own.
ONE_ROW_SPEC = (
    'name = "x"\npass_kind = "light"\n\n[[rows]]\nid = "G1"\n'
    'description = "Drop the guard"\nfile = "src/fixtpkg/guards.py"\n'
    "old = 'if value > limit:'\nnew = \"\"\n"
)


@pytest.mark.parametrize(
    ("stop", "heading", "code"),
    [
        ("DriverRefusal", "refused", 2),
        ("RestoreVerificationError", "RESTORE FAILED", 3),
        ("MeasurementFailure", "NOTHING MEASURED", 5),
        ("StateLeak", "STATE LEAK", 6),
        (None, "INVALID BATCH", 4),
    ],
)
def test_each_stop_exits_with_its_own_code(tmp_path, monkeypatch, capsys, stop, heading, code):
    """Other threads read these exit codes, so each is held: the docstring's table."""
    spec = tmp_path / "rows.toml"
    spec.write_text(ONE_ROW_SPEC, encoding="utf-8")

    def measured(*_a, **_k):
        if stop:
            raise getattr(mutate, stop)("why")
        return SimpleNamespace(
            baseline_source="measured", baseline_note="", valid=False, invalid_reason="why"
        )

    monkeypatch.setattr(mutate, "measure_batch", measured)
    monkeypatch.setattr(mutate, "write_outputs", lambda *_a: (tmp_path / "t.md", tmp_path / "t"))
    argv = ["mutate.py", str(spec), "--repo-root", str(tmp_path), "--out-dir", str(tmp_path)]
    assert mutate.main(argv) == code
    assert capsys.readouterr().err == f"{heading}: why\n"


def _refused(tmp_path: Path, capsys, listed: Path, root: Path | None = None) -> str:
    """Run the command on a known failures file, assert it refused, return its stderr."""
    spec = tmp_path / "rows.toml"
    spec.write_text(ONE_ROW_SPEC, encoding="utf-8")
    argv = ["mutate.py", str(spec), "--known-failures", str(listed)]
    argv += ["--repo-root", str(root or tmp_path), "--out-dir", str(tmp_path / "out")]
    capsys.readouterr()
    assert mutate.main(argv) == 2
    return capsys.readouterr().err


@pytest.mark.parametrize(
    ("header", "match", "said"),
    [
        ("# commit abc host here", "full history", "full history"),
        ("# commit abc host here history shallow", "full history", "full history"),
        ("# header", "full history", "full history"),
        ("# header history full", "full history", "full history"),
        ("# commit abc host here history full and more", "full history", "full history"),
        ("# commit abc host here history full ids whole and more", "full history", "full history"),
        ("# commit abc host here ids whole", "full history", "full history"),
        ("# header history full ids whole", "full history", "full history"),
        ("", "full history", "full history"),
        ("# commit abc host here history full", "first space", "first space"),
        ("# commit abc host here history full ids whole", "U273", "temporary files"),
        ("# commit abc host here temp history full ids whole", "U273", "temporary files"),
        ("# commit abc host here temp tmpfs history full ids whole", "U273", "temporary files"),
        ("# commit abc host here memory history full ids whole", "U273", "temporary files"),
    ],
    ids=[
        "before-u200", "shallow", "by-hand", "by-hand-with-field", "field-not-last",
        "whole-field-not-last", "whole-without-history", "by-hand-with-both-fields", "empty",
        "before-u268", "before-u273", "no-place", "not-a-place", "no-field",
    ],
)
def test_a_known_failures_file_the_battery_did_not_measure_is_refused_with_the_command(
    header, match, said, tmp_path, capsys
):
    """U200 (R-1191), U268 and U273: only a whole, placed, full history baseline is read."""
    listed = _listing(tmp_path, header, "tests/a.py::t[one")
    with pytest.raises(mutate.DriverRefusal, match=match):
        mutate.read_known_failures(listed)
    err = _refused(tmp_path, capsys, listed)
    assert said in err
    assert "scripts/cloud_battery.py baseline" in err


def test_known_failures_ignore_indented_comments_and_refuse_a_missing_file(tmp_path, capsys):
    listed = _listing(tmp_path, WHOLE, "  # indented", "", "  tests/a.py::t  ")
    assert mutate.read_known_failures(listed) == frozenset({"tests/a.py::t"})
    spec = tmp_path / "rows.toml"
    spec.write_text('name = "x"\npass_kind = "light"\n', encoding="utf-8")
    code = mutate.main(["mutate.py", str(spec), "--known-failures", str(tmp_path / "absent.txt")])
    assert code == 2


def test_known_failures_are_refused_on_a_shallow_clone(repo, tmp_path, capsys):
    """The driver reads git and never fetches."""
    shallow = tmp_path / "shallow"
    done = subprocess.run(
        ["git", "clone", "--depth", "1", repo.as_uri(), str(shallow)],
        capture_output=True, check=False,
    )
    assert done.returncode == 0, done.stderr
    with pytest.raises(mutate.DriverRefusal, match="shallow"):
        mutate.refuse_a_shallow_clone(shallow)
    not_a_repo = tmp_path / "not-a-repo"
    not_a_repo.mkdir()
    with pytest.raises(mutate.DriverRefusal, match="could not say"):
        mutate.refuse_a_shallow_clone(not_a_repo)
    mutate.refuse_a_shallow_clone(repo)
    assert "shallow" in _refused(tmp_path, capsys, _listing(tmp_path, WHOLE, "t"), shallow)


# The place the known failures were measured in, U273


def _known_file(tmp_path: Path, place: str, *ids: str, on_disk=()) -> Path:
    listed = tmp_path / "known.txt"
    listed.write_text(
        f"# commit abc host here temp {place} history full ids whole\n# 1 failed\n"
        + "".join(f"# on disk test {one}\n" for one in on_disk)
        + "# on disk summary 1 passed in 0.01s\n" * bool(on_disk)
        + "".join(f"{one}\n" for one in ids),
        encoding="utf-8",
    )
    return listed


def test_known_failures_carry_their_place_and_their_tests_on_disk(tmp_path):
    listed = _known_file(
        tmp_path, "memory", "tests/a.py::t", on_disk=("tests/b.py::u[a disk]", "tests/c.py::v")
    )
    read = mutate.read_known_failures(listed)
    assert read == frozenset({"tests/a.py::t"})
    assert read.place == "memory"
    assert read.on_disk == ("tests/b.py::u[a disk]", "tests/c.py::v")
    assert mutate.read_known_failures(_known_file(tmp_path, "disk", "tests/a.py::t")).on_disk == ()


def _batch_must_not_start(monkeypatch) -> None:
    def must_not_run(*_a, **_k):
        raise AssertionError("the batch started")

    monkeypatch.setattr(mutate, "measure_batch", must_not_run)


def test_a_place_this_machine_cannot_give_is_refused_before_anything_runs(
    repo, tmp_path, monkeypatch, places, capsys
):
    monkeypatch.setattr(mutate.BATTERY, "MEMORY_FLOOR", 2**80)
    _batch_must_not_start(monkeypatch)
    err = _refused(tmp_path, capsys, _known_file(tmp_path, "memory", "tests/a.py::t"), repo)
    assert "cannot now give a run with temporary files in memory" in err


def test_a_disk_the_rerun_cannot_have_is_refused_before_anything_runs(
    repo, tmp_path, monkeypatch, places, capsys
):
    """A disk rerun refused only after the memory run would be a full run spent."""
    monkeypatch.setattr(mutate.BATTERY, "disk_root", lambda: places[0])
    _batch_must_not_start(monkeypatch)
    listed = _known_file(tmp_path, "memory", "tests/a.py::t", on_disk=(PLACED_ID,))
    err = _refused(tmp_path, capsys, listed, repo)
    assert "run again on disk" in err and "memory filesystem" in err

    # With no test to run on disk, the memory run needs no disk and is not refused.
    class Measured(Exception):
        pass

    def reached(*_a, **_k):
        raise Measured

    monkeypatch.setattr(mutate, "measure_batch", reached)
    argv = ["mutate.py", str(tmp_path / "rows.toml"), "--repo-root", str(repo)]
    listed = _known_file(tmp_path, "memory", "tests/a.py::t")
    with pytest.raises(Measured):
        mutate.main([*argv, "--out-dir", str(tmp_path / "o"), "--known-failures", str(listed)])


def test_a_child_whose_place_is_gone_is_refused_rather_than_run_elsewhere(
    placed_repo, places, monkeypatch
):
    repo, log = placed_repo
    monkeypatch.setattr(mutate.BATTERY, "disk_root", lambda: places[0])
    known = mutate.KnownFailures(place="memory", on_disk=(PLACED_ID,))
    gone = "its tests on disk cannot keep its temporary files on disk"
    with pytest.raises(mutate.DriverRefusal, match=gone):
        mutate.run_pytest(repo, None, known=known, label="the row R1")
    monkeypatch.setattr(mutate.BATTERY, "MEMORY_FLOOR", 2**80)
    log.unlink()
    with pytest.raises(mutate.DriverRefusal, match="temporary files in memory"):
        mutate.run_pytest(repo, None, known=known, label="the row R1")
    assert not log.exists(), "a refused run ran nothing"


def _where(log: Path) -> list[str]:
    return log.read_text(encoding="utf-8").splitlines()


def test_a_child_runs_in_the_known_failures_place_and_the_listed_test_again_on_disk(
    placed_repo, places
):
    repo, log = placed_repo
    memory, disk = (os.path.realpath(one) for one in places)
    result = mutate.run_pytest(
        repo, None, known=mutate.KnownFailures(place="memory", on_disk=(PLACED_ID,))
    )
    # It failed in memory and passed on disk, and the disk run is what stands.
    assert result.is_green, result
    first, second = _where(log)
    assert first.startswith(memory + os.sep)
    assert second.startswith(disk + os.sep)
    assert list(Path(memory).iterdir()) == [] and list(Path(disk).iterdir()) == []
    without = mutate.run_pytest(repo, None, known=mutate.KnownFailures(place="memory"))
    assert without.failure_ids() == [PLACED_ID]


def test_a_run_on_disk_runs_once_and_one_with_no_place_inherits_the_temporary_directory(
    placed_repo, places, monkeypatch, tmp_path
):
    repo, log = placed_repo
    disk = os.path.realpath(places[1])
    assert mutate.run_pytest(repo, None, known=mutate.KnownFailures(place="disk")).is_green
    assert [w.startswith(disk + os.sep) for w in _where(log)] == [True]
    log.unlink()
    inherited = tmp_path / "inherited"
    inherited.mkdir()
    monkeypatch.setenv("TMPDIR", str(inherited))
    assert mutate.run_pytest(repo, None).is_green
    assert _where(log) == [os.path.realpath(inherited)]


def test_a_listed_test_erroring_in_memory_and_passing_on_disk_is_read_passing(
    placed_repo, places, monkeypatch
):
    repo, _log = placed_repo
    monkeypatch.setenv("PLACED_ERROR_IN_MEMORY", "1")
    unlisted = mutate.run_pytest(
        repo, None, known=mutate.KnownFailures(place="memory", on_disk=(PLACED_ID,))
    )
    assert unlisted.errored == (PLACED_ERRORING_ID,)
    known = mutate.KnownFailures(place="memory", on_disk=(PLACED_ID, PLACED_ERRORING_ID))
    assert mutate.run_pytest(repo, None, known=known).is_green


def test_a_subset_that_does_not_collect_the_listed_test_runs_nothing_on_disk(
    placed_repo, places
):
    repo, log = placed_repo
    known = mutate.KnownFailures(place="memory", on_disk=(PLACED_ID,))
    assert mutate.run_pytest(repo, ["tests/test_guards.py"], known=known).is_green
    assert not log.exists()


@pytest.mark.parametrize(
    ("nodeid", "paths", "runs"),
    [
        ("tests/a.py::t", None, True),
        ("tests/a.py::t", [], True),
        ("tests/a.py::t", ["tests/a.py"], True),
        ("tests/a.py::t", ["tests"], True),
        ("tests/a.py::t", ["tests/"], True),
        ("tests/a.py::t[x y]", ["tests/a.py::t"], True),
        ("tests/a.py::t", ["tests/a.py::t"], True),
        ("tests/a.py::t", ["tests/b.py"], False),
        ("tests/ab.py::t", ["tests/a"], False),
        ("tests/a.py::tt", ["tests/a.py::t"], False),
    ],
)
def test_a_listed_test_is_rerun_only_by_a_run_that_collects_it(nodeid, paths, runs):
    assert mutate.runs_node(nodeid, paths) is runs


def test_a_batch_in_memory_reads_the_listed_test_on_disk_and_says_so(placed_repo, places):
    repo, _log = placed_repo
    known = mutate.KnownFailures(place="memory", on_disk=(PLACED_ID,))
    batch = mutate.measure_batch(repo, "placed", [KILL], known=known)
    assert batch.valid, batch.invalid_reason
    (row,) = batch.results
    assert row.status == "killed"
    assert PLACED_ID in row.killed
    markdown = mutate.render_markdown(batch)
    assert "Temporary files: in memory" in markdown
    assert "1 test(s) the baseline ran on disk" in markdown
    with pytest.raises(mutate.DriverRefusal, match="BASELINE IS NOT GREEN"):
        mutate.measure_batch(
            repo, "placed-unlisted", [KILL], known=mutate.KnownFailures(place="memory")
        )


# The child's environment, and the installation state it must not reach (R-343)


def test_the_child_inherits_the_callers_environment(env_repo, monkeypatch):
    """A constructed environment once dropped ffmpeg off PATH and reddened 28 tests."""
    monkeypatch.setenv("MUTATE_FIXTURE_TOOL", "present")
    result = mutate.run_pytest(env_repo, None)
    assert result.is_green
    assert result.collected == 8


def test_a_baseline_red_from_a_scrubbed_environment_is_refused_naming_the_count(
    env_repo, monkeypatch
):
    """The subset stays green while the full run is red, so the damage reads as selective."""
    monkeypatch.delenv("MUTATE_FIXTURE_TOOL", raising=False)
    assert mutate.run_pytest(env_repo, ["tests/test_guards.py"]).is_green
    with pytest.raises(mutate.DriverRefusal) as caught:
        mutate.measure_batch(env_repo, "scrubbed", [_row("K1", "return value * 2", "return 0")])
    message = str(caught.value)
    assert "BASELINE IS NOT GREEN" in message
    assert "3 failing" in message
    assert "THE BATCH IS INVALID" in message
    assert "ENVIRONMENT" in message


def test_the_child_starts_in_a_sandbox_and_never_writes_the_callers_config(
    sandbox_repo, monkeypatch
):
    """The 2026-09-20 shape: a test undoing the isolation writes a configuration."""
    for name in ("HOME", "CRATEKIT_CONFIG_DIR", "CRATEKIT_STATE_DIR"):
        monkeypatch.setenv("MUTATE_FIXTURE_CALLER_" + name, os.environ[name])
    callers = Path(platformdirs.user_config_dir("cratekit"))
    before = sorted(p.name for p in callers.iterdir()) if callers.is_dir() else []
    result = mutate.run_pytest(sandbox_repo, None)
    assert result.is_green, result.failure_ids()
    assert result.collected == 7
    after = sorted(p.name for p in callers.iterdir()) if callers.is_dir() else []
    assert after == before, "the child wrote into the caller's own installation state"


def _guarded(tmp_path: Path, config: str | None = "the real configuration") -> Path:
    guarded = tmp_path / "guarded"
    guarded.mkdir()
    if config is not None:
        (guarded / "config.toml").write_text(config, encoding="utf-8")
    return guarded


def test_a_leak_during_the_baseline_names_the_phase(leak_repo, monkeypatch, tmp_path):
    guarded = _guarded(tmp_path, None)
    monkeypatch.setenv("MUTATE_FIXTURE_LEAK_TARGET", str(guarded))
    # The fixture writes only once the guard is gone, so the baseline sees it gone.
    target = leak_repo / GUARDS_FILE
    target.write_text(
        target.read_text(encoding="utf-8").replace("        return limit", "        return value"),
        encoding="utf-8",
    )
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.measure_batch(
            leak_repo, "leak-baseline", [_row("K1", "if value < lowest:", "if value < 1:")],
            allow_dirty=True, guard=mutate.take_state_guard((guarded,)),
        )
    message = str(caught.value)
    assert "the full baseline" in message
    assert str(guarded) in message
    assert "R-343" in message


def test_a_leak_under_a_row_names_that_row_and_stops_the_batch(leak_repo, monkeypatch, tmp_path):
    guarded = _guarded(tmp_path)
    monkeypatch.setenv("MUTATE_FIXTURE_LEAK_TARGET", str(guarded))
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.measure_batch(
            leak_repo, "leak-row", [_row("LEAKY", "        return limit", "        return value")],
            guard=mutate.take_state_guard((guarded,)),
        )
    message = str(caught.value)
    assert "row LEAKY" in message
    assert "the full baseline" not in message
    _assert_untouched(leak_repo)


def test_one_batch_writes_its_control_environment_and_guard_into_the_table(repo, tmp_path):
    """A silent scrub, an unnamed sandbox, or a guard passing unremarked is a defect."""
    guarded = _guarded(tmp_path)
    batch = mutate.measure_batch(
        repo, "written", [_row("K1", "if value > limit:", "if value > 1:")],
        guard=mutate.take_state_guard((guarded,)),
    )
    assert batch.valid is True
    assert (batch.control.id, batch.control.deaths, batch.control.status) == (
        "NULL_CONTROL", 0, "zero",
    )
    assert (repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS
    markdown, sidecar = mutate.write_outputs(batch, tmp_path / "docs" / "mutation")
    assert markdown.name == "written.md" and sidecar.name == "written.json"
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["rows"][0]["id"] == "K1"
    assert data["valid"] is True
    assert data["control"]["deaths"] == 0
    assert data["state_guarded"]
    assert data["reused_rows"] == 0
    text = markdown.read_text(encoding="utf-8")
    assert "fixture row K1" in text
    assert "PYTHONDONTWRITEBYTECODE=1" in text
    for name in [*mutate.SCRUBBED_ENV, *mutate.SANDBOXED_ENV]:
        assert name in text, name
    assert "the watched roots are unchanged" in text
    assert str(guarded) in text
    assert "1 entries" in text
    assert "not seen by this guard" in text, "the claim must say what it does not cover"
    assert "reused from a prior sidecar" not in text


def test_the_guarded_root_is_written_into_the_table_without_the_home_directory(
    repo, tmp_path, monkeypatch
):
    """The scan reads docs/mutation, and a home path there once failed every promoted row."""
    home = tmp_path / "home"
    guarded = home / "Library" / "Application Support" / "cratekit"
    guarded.mkdir(parents=True)
    monkeypatch.setattr(mutate.Path, "home", classmethod(lambda cls: home))
    batch = mutate.measure_batch(
        repo, "portable", [_row("K1", "if value > limit:", "if value > 1:")],
        guard=mutate.take_state_guard((guarded,)),
    )
    markdown = mutate.render_markdown(batch)
    assert str(home) not in markdown
    assert str(home) not in json.dumps(batch.to_dict())
    assert "~/Library/Application Support/cratekit" in markdown
    assert mutate.portable(tmp_path / "elsewhere") == str(tmp_path / "elsewhere")


def test_resume_reuses_an_unchanged_row_names_it_unwatched_and_measures_an_edited_one(
    repo, tmp_path
):
    guarded = _guarded(tmp_path, None)
    row = _row("K1", "if value > limit:", "if value > 1:")
    first = mutate.measure_batch(repo, "resume", [row], guard=mutate.take_state_guard((guarded,)))
    prior = first.to_dict()
    prior["rows"][0]["deaths"] = 99  # a marker only a reused row can carry
    resumed = mutate.measure_batch(
        repo, "resume", [row], prior=prior, guard=mutate.take_state_guard((guarded,))
    )
    assert (resumed.reused_rows, resumed.results[0].deaths) == (1, 99)
    markdown = mutate.render_markdown(resumed)
    assert "1 row(s) were reused from a prior sidecar" in markdown
    assert "did not watch" in markdown
    edited = mutate.measure_batch(repo, "resume", [KILL], prior=prior)
    assert edited.results[0].deaths == 1


def test_any_change_under_the_real_root_is_a_leak(tmp_path):
    """A new directory, a same size rewrite with its timestamps put back, and a root
    that did not exist being made: each reaches the real path."""
    root = tmp_path / "real"
    root.mkdir()
    config = root / "config.toml"
    config.write_text("pin = 1", encoding="utf-8")
    guard = mutate.take_state_guard((root,))
    (root / "jobs").mkdir()
    with pytest.raises(mutate.StateLeak):
        mutate.check_state_guard(guard, label="a child that made a directory")

    before = config.stat()
    guard = mutate.take_state_guard((root,))
    config.write_text("pin = 2", encoding="utf-8")
    os.utime(config, ns=(before.st_atime_ns, before.st_mtime_ns))
    assert config.stat().st_size == before.st_size
    with pytest.raises(mutate.StateLeak):
        mutate.check_state_guard(guard, label="a same size rewrite")

    absent = tmp_path / "not-yet"
    guard = mutate.take_state_guard((absent,))
    mutate.check_state_guard(guard, label="a clean child")
    absent.mkdir()
    with pytest.raises(mutate.StateLeak):
        mutate.check_state_guard(guard, label="a child that created it")


def test_a_child_that_leaks_and_then_hangs_is_still_caught(tmp_path, monkeypatch):
    """A timeout must not leave before the guard looks, or the next row is blamed."""
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
    """SANDBOXED_ENV is a hand copy of the conftest's table, so the two are pinned."""
    source = (Path(__file__).parent / "conftest.py").read_text(encoding="utf-8")
    start = source.index("def _isolate_state_roots(")
    body = source[start : source.index("def _isolate_keychain(", start)]
    isolated = set(re.findall(r'monkeypatch\.setenv\(\s*"([A-Z_]+)"', body))
    isolated |= set(re.findall(r'\(\s*"([A-Z_]+)",\s*"[a-z]+"\s*\)', body))
    assert isolated, "the conftest's isolation table was not found"
    assert isolated <= set(mutate.SANDBOXED_ENV), sorted(isolated - set(mutate.SANDBOXED_ENV))


def test_the_guarded_roots_follow_the_overrides_this_process_carries(monkeypatch, tmp_path):
    monkeypatch.setenv("CRATEKIT_CONFIG_DIR", str(tmp_path / "cfg"))
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "state"))
    assert mutate.installation_state_roots() == (tmp_path / "cfg", tmp_path / "state")
    # macOS answers both platformdirs calls with one directory, walked once.
    monkeypatch.setenv("CRATEKIT_STATE_DIR", str(tmp_path / "cfg"))
    assert mutate.installation_state_roots() == (tmp_path / "cfg",)


# The batch


def test_a_red_subset_baseline_is_refused_even_when_the_full_suite_is_green(repo):
    """An order dependent test passes in the full run and fails in its own subset."""
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
    _commit(repo, "an order dependent test")
    assert mutate.run_pytest(repo, None).is_green, "the whole suite is green, which is the point"
    subset, _ = mutate.derive_subset(repo, "src/fixtpkg/other.py")
    assert subset == ["tests/test_other.py", "tests/test_zorder.py"]
    row = _row("K1", "return True", "return False", file="src/fixtpkg/other.py")
    with pytest.raises(mutate.DriverRefusal, match="subset baseline"):
        mutate.measure_batch(repo, "redsubset", [row])


def test_an_uncommitted_or_untracked_target_is_refused(repo):
    (repo / "src" / "fixtpkg" / "new.py").write_text("X = 1\n", encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="HEAD"):
        mutate.measure_batch(repo, "new", [_row("K1", "X = 1", "X = 2", file="src/fixtpkg/new.py")])
    (repo / GUARDS_FILE).write_text(GUARDS + "\n# uncommitted\n", encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="uncommitted changes"):
        mutate.measure_batch(repo, "dirty", [KILL])


def test_a_null_control_that_kills_invalidates_the_whole_batch(repo, monkeypatch):
    """The 2026-08-10 trap: a test that fails whenever the guards file grows."""
    monkeypatch.setattr(mutate, "NULL_CONTROL_COMMENT", "\n# a control that is not a control\n")
    (repo / "tests" / "test_cleanliness.py").write_text(
        "from pathlib import Path\n\n\n"
        "def test_no_stray_comment():\n"
        "    text = Path('src/fixtpkg/guards.py').read_text()\n"
        "    assert 'not a control' not in text\n",
        encoding="utf-8",
    )
    _commit(repo, "a test that reacts to any edit")
    batch = mutate.measure_batch(repo, "bad", [_row("K1", "return value * 2", "return 0")])
    assert batch.valid is False
    assert "null control killed 1" in batch.invalid_reason
    assert batch.results == []


def test_a_full_batch_measures_every_row_owes_its_composites_and_restores_the_tree(repo):
    """A killer, zeros of each surface, a composite, a collection breaker, a refusal."""
    rows = [
        _row("K1", "if value > limit:", "if value > 10000:", surface="user"),
        _row("Z1", "return value * 2", "return value * 3", surface="user"),
        _row("Z1C", "if value < lowest:", "if value < -10000:", pairs_with="Z1"),
        _row("Z2", "value * 2", "value * 4", surface="user"),
        _row("Z3", "* 2", "* 5", surface="maintainer"),
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
    _assert_untouched(repo)
    note = {one: mutate.composite_note(batch, by_id[one]) for one in ("Z1", "Z2", "Z3")}
    assert note["Z1"] == "paired with `Z1C`, which killed 1"
    assert "NO COMPOSITE" in note["Z2"]
    assert "composite not required" in note["Z3"]
    markdown = mutate.render_markdown(batch)
    assert "NO COMPOSITE" in markdown
    assert "## Considered and dropped" in markdown
    assert "`D1`" in markdown
    assert "collection error" in markdown
    assert "Null control" in markdown


def test_the_sidecar_is_written_after_every_row_not_only_at_the_end(repo, tmp_path):
    progress = tmp_path / "docs" / "mutation" / "progress.json"
    rows = [KILL, _row("K2", "if value < lowest:", "if value < -10000:")]
    mutate.measure_batch(repo, "progress", rows, progress_path=progress)
    written = json.loads(progress.read_text(encoding="utf-8"))
    assert [one["id"] for one in written["rows"]] == ["K1", "K2"]
    assert written["control"]["deaths"] == 0


# Loading rows


def _spec(tmp_path: Path, **body) -> Path:
    spec = tmp_path / "rows.json"
    spec.write_text(json.dumps(body), encoding="utf-8")
    return spec


def _entry(row_id: str = "G1", **extra) -> dict:
    return {"id": row_id, "description": "d", "file": "f.py", "old": "a", "new": "b", **extra}


def test_a_toml_and_a_json_spec_load_the_same_way(tmp_path):
    spec = tmp_path / "rows.toml"
    spec.write_text(
        'name = "u34-round-2"\npass_kind = "light"\n\n[[rows]]\nid = "G1"\n'
        'description = "Drop the guard"\nfile = "src/fixtpkg/guards.py"\nsurface = "user"\n'
        "old = '''if value > limit:'''\nnew = \"\"\n\n[[dropped]]\nid = \"D1\"\n"
        'description = "Another guard."\nreason = "ranked below the cap"\n',
        encoding="utf-8",
    )
    name, pass_kind, rows, dropped = mutate.load_spec(spec)
    assert (name, pass_kind) == ("u34-round-2", "light")
    assert rows[0].id == "G1" and rows[0].surface == "user" and rows[0].new == ""
    assert dropped[0].reason == "ranked below the cap"
    spec = _spec(tmp_path, name="j", rows=[_entry(tests=["tests/test_guards.py"])])
    assert mutate.load_spec(spec)[2][0].tests == ("tests/test_guards.py",)


@pytest.mark.parametrize(
    ("body", "refusal"),
    [
        ({"rows": [_entry(), _entry()]}, "duplicate row id"),
        (
            {"pass_kind": "light", "rows": [_entry(f"G{n}") for n in range(26)]},
            "exceeds the light pass cap",
        ),
        ({"rows": [_entry(pairs_with="nobody")]}, "pairs_with"),
    ],
)
def test_a_spec_the_driver_cannot_trust_is_refused(tmp_path, body, refusal):
    with pytest.raises(mutate.DriverRefusal, match=refusal):
        mutate.load_spec(_spec(tmp_path, **body))


def test_a_batch_with_no_python_target_cannot_produce_a_control():
    with pytest.raises(mutate.DriverRefusal, match="null control needs a Python target"):
        mutate.null_control_row([_row("D1", "a", "b", file="docs/notes.md")])


# The replay pass, U297


def _replay_entry(n: int, **extra) -> dict:
    """One replay row as a row file spells it, naming where it came from."""
    source = {"table": "u1.json", "id": f"G{n}"}
    return _entry(f"u1.G{n}", old=f"a{n}", **{"source": source, **extra})


def test_a_replay_pass_has_no_row_cap_and_keeps_each_rows_source(tmp_path):
    spec = _spec(tmp_path, pass_kind="replay", rows=[_replay_entry(n) for n in range(46)])
    _, pass_kind, rows, _ = mutate.load_spec(spec)
    assert pass_kind == "replay" and len(rows) == 46
    assert rows[45].source == ("u1.json", "G45")


def _nameless() -> dict:
    nameless = _replay_entry(1)
    del nameless["source"]
    return nameless


@pytest.mark.parametrize(
    ("kind", "rows", "refusal"),
    [
        ("replay", [_replay_entry(0), _nameless()], "row u1.G1: a replay row names where it came"),
        ("light", [_replay_entry(n) for n in range(26)], "26 rows exceeds the light pass cap"),
        ("full", [_replay_entry(n) for n in range(46)], "46 rows exceeds the full pass cap of 45"),
        ("heavy", [_replay_entry(0)], r"one of \['full', 'light', 'replay'\]"),
        (
            "replay",
            [_replay_entry(0), _replay_entry(1, source={"table": "u1.json", "id": "G0"})],
            "u1.json row G0 is already the source",
        ),
    ],
    ids=["no-source", "light-cap", "full-cap", "unknown-kind", "one-source-twice"],
)
def test_a_replay_row_buys_no_cap_it_cannot_name(tmp_path, kind, rows, refusal):
    with pytest.raises(mutate.DriverRefusal, match=refusal):
        mutate.load_spec(_spec(tmp_path, pass_kind=kind, rows=rows))


@pytest.mark.parametrize(
    "source",
    ["u1.json#G0", {"table": "u1.json"}, {"table": "", "id": "G0"}, {"table": "u1.json", "id": 3}],
)
def test_a_half_named_source_is_refused_rather_than_read_as_named(tmp_path, source):
    spec = _spec(tmp_path, pass_kind="replay", rows=[_replay_entry(0, source=source)])
    with pytest.raises(mutate.DriverRefusal, match="row u1.G0: source must name the table"):
        mutate.load_spec(spec)


MAPPED = {"source": {"table": "u1.json", "id": "G9"}, "to": "u1.G0", "reason": "merged"}


def _mapped(tmp_path: Path, *entries: dict, pass_kind: str = "replay"):
    spec = _spec(tmp_path, pass_kind=pass_kind, rows=[_replay_entry(0)], mapped=list(entries))
    _, kind, rows, _ = mutate.load_spec(spec)
    return mutate.load_mapped(spec, kind, rows)


@pytest.mark.parametrize(
    ("entries", "refusal"),
    [
        ([{"to": "u1.G0", "reason": "merged"}], "mapped entry 0: it names no source"),
        ([{**MAPPED, "to": "u1.G7"}], "it maps to 'u1.G7', which is no row in this batch"),
        ([{**MAPPED, "reason": "  "}], "mapped entry 0: it gives no reason"),
        (
            [{**MAPPED, "source": {"table": "u1.json", "id": "G0"}}],
            "u1.json row G0 has a row of its own in this batch",
        ),
        ([MAPPED, MAPPED], "u1.json row G9 is mapped twice"),
    ],
)
def test_a_mapping_nothing_stands_behind_is_refused(tmp_path, entries, refusal):
    assert _mapped(tmp_path, MAPPED) == [
        mutate.Mapped(source=("u1.json", "G9"), to="u1.G0", reason="merged")
    ]
    with pytest.raises(mutate.DriverRefusal, match=refusal):
        _mapped(tmp_path, *entries)
    with pytest.raises(mutate.DriverRefusal, match="belongs to a replay pass, and this is a light"):
        _mapped(tmp_path, MAPPED, pass_kind="light")


MOVED = "the same text, now in src/fixtpkg/guards.py"


def _replay_rows() -> list:
    return [
        _row("u1.K1", *KILLER[1:], source=("u1.json", "K1"), tests=("tests/test_guards.py",)),
        _row("u1.K2", "if value < lowest:", "if value < -10000:", source=("u1.json", "K2"),
             moved=MOVED, tests=("tests/test_guards.py",)),
    ]


def test_a_replay_batch_spends_one_baseline_and_one_control_and_carries_its_sources(
    repo, tmp_path
):
    """Full baseline, one shared subset baseline, the control, a run a row: five, not seven."""
    mapped = [mutate.Mapped(source=("u1.json", "K9"), to="u1.K1", reason="merged into K1")]
    dropped = [mutate.Dropped(id="u1.K8", description="A row left out.", reason="unplaced")]
    batch = mutate.measure_batch(
        repo, "replayed", _replay_rows(), dropped, pass_kind="replay", mapped=mapped
    )
    assert batch.valid is True
    assert [(one.id, one.status, one.deaths) for one in batch.results] == [
        ("u1.K1", "killed", 1),
        ("u1.K2", "killed", 1),
    ]
    assert (batch.pytest_runs, batch.subset_baselines, batch.control.status) == (5, 1, "zero")
    assert (repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS
    _, sidecar = mutate.write_outputs(batch, tmp_path / "docs" / "mutation")
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["pass_kind"] == "replay"
    assert data["rows"][0]["source"] == {"table": "u1.json", "id": "K1"}
    assert "moved" not in data["rows"][0]
    assert data["rows"][1]["moved"] == MOVED
    assert data["mapped"] == [
        {"source": {"table": "u1.json", "id": "K9"}, "to": "u1.K1", "reason": "merged into K1"}
    ]
    markdown = mutate.render_markdown(batch)
    assert "Pass kind: replay." in markdown
    assert "it has no row cap and chooses no rows" in markdown
    assert "- Source: `u1.json`, row `K1`" in markdown
    assert f"- Moved: {MOVED}" in markdown
    assert "- `u1.json` row `K9` is covered by `u1.K1`: merged into K1" in markdown
    assert "Recorded rows this replay left out and did NOT measure" in markdown
    assert "METHOD caps" not in markdown


def test_a_replay_row_that_errors_still_names_its_source(repo, monkeypatch):
    real = mutate.measure_row

    def failing(repo_root, row, *args, **kwargs):
        if row.kind == "null-control":
            return real(repo_root, row, *args, **kwargs)
        raise mutate.MeasurementFailure("nothing readable")

    monkeypatch.setattr(mutate, "measure_row", failing)
    batch = mutate.measure_batch(repo, "errors", _replay_rows()[:1], pass_kind="replay")
    assert batch.results[0].status == "error"
    assert batch.results[0].to_dict()["source"] == {"table": "u1.json", "id": "K1"}


def _replay(repo: Path, rows=None, prior=None):
    rows = _replay_rows()[:1] if rows is None else rows
    return mutate.measure_batch(repo, "resumed", rows, pass_kind="replay", prior=prior)


def test_a_resumed_replay_reuses_its_rows_and_they_keep_their_sources(repo):
    rows = _replay_rows()
    prior = _replay(repo, rows).to_dict()
    prior["rows"][0]["deaths"] = 99  # a marker only a reused row can carry
    second = _replay(repo, rows, prior)
    assert (second.reused_rows, second.results[0].deaths) == (2, 99)
    assert second.results[0].source == {"table": "u1.json", "id": "K1"}
    assert second.results[1].moved == MOVED


def _delete_the_killing_test(repo: Path) -> None:
    tests = repo / "tests" / "test_guards.py"
    tests.write_text(
        tests.read_text(encoding="utf-8").replace(
            "def test_clamp_caps_at_the_limit():\n    assert clamp(50) == 10\n", ""
        ),
        encoding="utf-8",
    )


def test_a_replay_reuses_nothing_once_the_killing_test_is_gone_committed_or_not(repo):
    """A kill measured before its test was deleted is not a kill here, and a deletion
    not yet committed leaves the commit's name unchanged."""
    first = _replay(repo)
    assert first.results[0].status == "killed"
    _delete_the_killing_test(repo)
    assert "a tracked file differs from this commit" in mutate.replay_resume_refusal(
        repo, first.to_dict()
    )
    uncommitted = _replay(repo, prior=first.to_dict())
    assert uncommitted.head == first.head
    assert uncommitted.reused_rows == 0 and uncommitted.results[0].status == "zero"
    _git(repo, "commit", "-q", "-am", "the test that killed K1 is gone")
    second = _replay(repo, prior=first.to_dict())
    assert second.head != first.head
    assert second.reused_rows == 0
    assert (second.results[0].status, second.results[0].deaths) == ("zero", 0)


def test_a_light_pass_still_resumes_across_commits_as_it_always_did(repo):
    first = mutate.measure_batch(repo, "light", [KILL], pass_kind="light")
    (repo / "notes.txt").write_text("a commit that touches nothing measured\n", encoding="utf-8")
    _commit(repo, "another commit")
    prior = first.to_dict()
    prior["rows"][0]["deaths"] = 99
    second = mutate.measure_batch(repo, "light", [KILL], pass_kind="light", prior=prior)
    assert second.head != first.head
    assert (second.reused_rows, second.results[0].deaths) == (1, 99)


def test_a_reused_replay_row_says_where_it_came_from_as_the_row_file_does_now(repo):
    row = _replay_rows()[0]
    first = _replay(repo, [row])
    assert first.results[0].moved == ""
    said = _row(
        row.id, row.old, row.new, source=row.source, tests=row.tests,
        moved="anchored by hand, the guard is the same",
    )
    second = _replay(repo, [said], first.to_dict())
    assert second.reused_rows == 1
    assert second.results[0].moved == "anchored by hand, the guard is the same"
    assert second.results[0].source == {"table": "u1.json", "id": "K1"}


def test_a_replay_resumes_over_untracked_files_but_never_over_an_unreadable_status(
    repo, monkeypatch
):
    first = _replay(repo)
    (repo / "docs" / "mutation").mkdir(parents=True)
    (repo / "docs" / "mutation" / "resumed.json").write_text("{}", encoding="utf-8")
    assert mutate.replay_resume_refusal(repo, first.to_dict()) == ""
    assert mutate.replay_resume_refusal(repo, None) == ""
    assert _replay(repo, prior=first.to_dict()).reused_rows == 1
    real = mutate._git

    def no_status(repo_root, *args):
        if args[0] == "status":
            return subprocess.CompletedProcess(args, 128, b"", b"fatal")
        return real(repo_root, *args)

    monkeypatch.setattr(mutate, "_git", no_status)
    assert "git could not say" in mutate.replay_resume_refusal(repo, first.to_dict())


def _recorded_table(repo: Path, rows: list[dict], name: str = "u1.json") -> None:
    path = repo / "docs" / "mutation" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"name": Path(name).stem, "rows": rows}), encoding="utf-8")


#: K1 is the clamp guard exactly as ``_replay_rows`` and ``_replay_spec`` replay it.
CLAMP = {"file": GUARDS_FILE, "old": "if value > limit:", "new": "if value > 10000:"}
RECORDED = [
    {"id": "K1", "deaths": 1, **CLAMP},
    {"id": "K9", "deaths": 3},
    {"id": "Z1", "deaths": 0, **CLAMP},
    {"id": "T1", "deaths": True, **CLAMP},
]


@pytest.mark.parametrize(
    "source, refusal",
    [
        (("no-such-table.json", "K1"), "docs/mutation/no-such-table.json is not a recorded table"),
        (("u1.json", "K7"), "docs/mutation/u1.json holds no row 'K7'"),
        (("u1.json", "Z1"), "row 'Z1' recorded no death"),
        (("u1.json", "T1"), "row 'T1' recorded no death"),
        (("notes.json", "K1"), "docs/mutation/notes.json is not a recorded table"),
        (("../../elsewhere/u1.json", "K1"), "is not a recorded table"),
    ],
)
def test_a_replay_row_naming_a_source_no_table_recorded_is_refused(repo, source, refusal):
    """26 new rows under a table's name were once measured as a replay."""
    _recorded_table(repo, RECORDED)
    mapped = [mutate.Mapped(source=("u1.json", "K9"), to="u1.K1", reason="merged")]
    mutate.refuse_unrecorded_sources(repo, _replay_rows()[:1], mapped)
    (repo / "docs" / "mutation" / "notes.json").write_text("[1, 2]", encoding="utf-8")
    elsewhere = repo / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "u1.json").write_text(json.dumps({"rows": RECORDED}), encoding="utf-8")
    row = _row("u1.K1", "if value > limit:", "if value > 10000:", source=source)
    with pytest.raises(mutate.DriverRefusal, match=re.escape(refusal)):
        mutate.refuse_unrecorded_sources(repo, [row], [])
    covered = mutate.Mapped(source=source, to="u1.K1", reason="merged")
    with pytest.raises(mutate.DriverRefusal, match=r"the mapping to u1\.K1: "):
        mutate.refuse_unrecorded_sources(repo, _replay_rows()[:1], [covered])


def test_a_table_that_is_not_json_is_not_a_recorded_table(repo):
    (repo / "docs" / "mutation").mkdir(parents=True)
    (repo / "docs" / "mutation" / "u1.json").write_text("{ not json", encoding="utf-8")
    with pytest.raises(mutate.DriverRefusal, match="docs/mutation/u1.json is not a recorded table"):
        mutate.refuse_unrecorded_sources(repo, _replay_rows()[:1], [])


@pytest.mark.parametrize(
    "change",
    [{"file": "src/fixtpkg/other.py"}, {"old": "return True"}, {"new": "if value > 1:"}],
)
def test_a_new_row_under_a_recorded_name_is_refused_unless_it_says_it_moved(repo, change):
    _recorded_table(repo, RECORDED)
    text = {**CLAMP, **change}

    def borrowed(moved: str = "") -> "mutate.Row":
        return _row(
            "u1.K1", text["old"], text["new"], file=text["file"], source=("u1.json", "K1"),
            moved=moved,
        )

    with pytest.raises(
        mutate.DriverRefusal,
        match="row u1.K1: its file or text is not what docs/mutation/u1.json recorded for 'K1'",
    ):
        mutate.refuse_unrecorded_sources(repo, [borrowed()], [])
    mutate.refuse_unrecorded_sources(repo, [borrowed("the guard was split out by hand")], [])
    with pytest.raises(mutate.DriverRefusal, match="gives no moved reason"):
        mutate.refuse_unrecorded_sources(repo, [borrowed("  ")], [])


def _replay_spec(repo: Path, *, source_id: str = "K1") -> Path:
    spec = repo / "replay-rows.json"
    row = {"id": "u1.K1", "description": "the clamp", **CLAMP, "tests": ["tests/test_guards.py"]}
    spec.write_text(
        json.dumps(
            {
                "name": "u1-replay",
                "pass_kind": "replay",
                "rows": [{**row, "source": {"table": "u1.json", "id": source_id}}],
                "mapped": [
                    {"source": {"table": "u1.json", "id": "K9"}, "to": "u1.K1", "reason": "merged"}
                ],
            }
        ),
        encoding="utf-8",
    )
    return spec


def test_the_command_checks_the_sources_and_hands_the_mappings_to_the_table(
    repo, tmp_path, capsys
):
    _recorded_table(repo, RECORDED)
    out = tmp_path / "out"
    argv = ["--repo-root", str(repo), "--out-dir", str(out)]
    assert mutate.main(["mutate.py", str(_replay_spec(repo)), *argv]) == 0
    data = json.loads((out / "u1-replay.json").read_text(encoding="utf-8"))
    assert data["rows"][0]["status"] == "killed"
    assert data["mapped"] == [
        {"source": {"table": "u1.json", "id": "K9"}, "to": "u1.K1", "reason": "merged"}
    ]
    capsys.readouterr()
    assert mutate.main(["mutate.py", str(_replay_spec(repo, source_id="K7")), *argv]) == 2
    assert "refused: row u1.K1: docs/mutation/u1.json holds no row 'K7'" in capsys.readouterr().err


def test_resuming_a_replay_from_another_commits_sidecar_says_nothing_is_reused(
    repo, tmp_path, capsys
):
    _recorded_table(repo, RECORDED)
    out = tmp_path / "out"
    spec = _replay_spec(repo)
    argv = ["mutate.py", str(spec), "--repo-root", str(repo), "--out-dir", str(out), "--resume"]
    assert mutate.main(argv) == 0
    _commit(repo, "the table and its rows")
    capsys.readouterr()
    assert mutate.main(argv) == 0
    err = capsys.readouterr().err
    assert "resume: nothing of u1-replay.json is reused: it was measured at" in err
    assert "so every row is measured again" in err
    assert json.loads((out / "u1-replay.json").read_text(encoding="utf-8"))["reused_rows"] == 0
    assert mutate.main(argv) == 0
    assert "measured again" not in capsys.readouterr().err
    assert json.loads((out / "u1-replay.json").read_text(encoding="utf-8"))["reused_rows"] == 1


def test_a_capped_pass_writes_the_sidecar_and_dropped_rows_it_always_wrote(repo):
    """No replay key reaches a table that is not a replay, so old readers read new tables."""
    dropped = [mutate.Dropped(id="D1", description="A fifth row.", reason="below the cap")]
    batch = mutate.measure_batch(repo, "light", [KILL], dropped, pass_kind="light")
    data = batch.to_dict()
    assert "mapped" not in data
    assert "source" not in data["rows"][0] and "moved" not in data["rows"][0]
    assert "source" not in data["control"]
    markdown = mutate.render_markdown(batch)
    assert "## Mapped" not in markdown
    assert "METHOD caps a light pass at 25 rows." in markdown


# Under the repository's work stealing distribution, U251


def test_the_count_and_the_failure_survive_a_steal(tmp_path, monkeypatch):
    """The count is the collection's, not one worker's queue, and the stolen failure
    reaches the report, for the full suite and for a row's three file subset."""
    repo = stealing.write(tmp_path / "stealing-repo")
    _git(repo, "init", "-q", "-b", "main")
    _commit(repo, "a suite whose tests move between workers")
    runs = ((None, stealing.FULL_COUNT), (list(stealing.SUBSET), stealing.SUBSET_COUNT))
    for paths, count in runs:
        log = tmp_path / f"workers-{count}"  # a fresh log, or the holder sees the last run's
        stealing.prepare_environment(monkeypatch, log)
        result = mutate.run_pytest(repo, paths)
        assert result.collected == count
        assert list(result.failed) == [stealing.STOLEN_FAILURE]
        assert not result.errored
        assert not result.collect_errors
        stealing.assert_the_failure_moved(log)


# The full baseline read from the battery's verdict for the same commit, U271.
# The verdicts are written by the battery itself, run for real over the fixture,
# except where a test changes one field of a real one to name the key it tests.


@pytest.fixture
def battery_on(monkeypatch):
    """Point the battery at a fixture and run its verbs there for real, replacing only
    the history fetch and the static checks, which read the real repository."""
    for name in stealing.INHERITED_RUN_STATE:
        monkeypatch.delenv(name, raising=False)

    def point(root: Path) -> Path:
        (root / ".gitignore").write_text(".cloud-battery/\n__pycache__/\n", encoding="utf-8")
        _commit(root, "ignore the battery's state")
        state = root / ".cloud-battery"
        monkeypatch.setattr(battery, "ROOT", root.resolve())
        monkeypatch.setattr(battery, "STATE", state)
        monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
        monkeypatch.setattr(battery, "VERDICT", state / "last-compare.txt")
        monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
        monkeypatch.setattr(battery, "ensure_full_history", lambda root=None: None)
        monkeypatch.setattr(battery, "static_checks", lambda: True)
        assert battery.cmd_baseline(None) == 0
        return state

    return point


def _known(state: Path) -> tuple[frozenset[str], str]:
    path = state / "baseline.txt"
    return mutate.read_known_failures(path), mutate.file_digest(path)


def _batch(root: Path, state: Path, name: str, *, verdict: bool = True):
    known, digest = _known(state)
    return mutate.measure_batch(
        root, name, [KILL], known=known, known_source=".cloud-battery/baseline.txt",
        known_digest=digest,
        battery_verdict=(state / mutate.BATTERY_VERDICT.name) if verdict else None,
    )


def _read_verdict(root: Path, state: Path, *, digest: str | None = None):
    known, measured = _known(state)
    return mutate.read_battery_verdict(
        root, state / mutate.BATTERY_VERDICT.name, known=known,
        known_digest=measured if digest is None else digest,
    )


@pytest.fixture
def judged(red_repo, battery_on) -> tuple[Path, Path]:
    """The red fixture with the battery's baseline and a clean compare on its head:
    the one failing test is the machine's."""
    state = battery_on(red_repo)
    assert battery.cmd_compare(None) == 0
    return red_repo, state


def _rows_as_measured(batch) -> list[tuple]:
    return [(one.id, one.status, one.deaths, tuple(one.killed)) for one in batch.results]


def test_a_clean_verdict_for_this_commit_stands_for_the_full_baseline_and_says_so(judged):
    root, state = judged
    read = _batch(root, state, "read")
    measured = _batch(root, state, "measured", verdict=False)
    assert read.valid, read.invalid_reason
    assert measured.valid, measured.invalid_reason
    assert (read.baseline_source, measured.baseline_source) == ("read", "measured")
    assert read.pytest_runs == measured.pytest_runs - 1
    assert read.baseline_collected == measured.baseline_collected == 6
    assert _rows_as_measured(read) == _rows_as_measured(measured)
    assert _rows_as_measured(read) == [("K1", "killed", 1, tuple(CLAMP_KILLED))]
    # The null control still ran the full suite here, held to the verdict's count.
    assert read.control is not None and read.control.status == "zero"
    assert read.control.runs == 1
    assert read.control.collected == read.baseline_collected
    assert read.subset_baselines == measured.subset_baselines == 1
    text = mutate.render_markdown(read)
    assert "Full baseline: READ, not measured by this driver" in text
    assert "`cloud_battery.py compare`" in text
    assert "Subset baselines: 1, each measured by this driver" in text
    assert "The null control below ran the full suite in this driver's own environment" in text
    assert mutate.BATTERY_VERDICT.as_posix() in text
    assert (read.to_dict()["baseline_source"], read.to_dict()["subset_baselines"]) == ("read", 1)
    text = mutate.render_markdown(measured)
    assert "Full baseline: measured by this driver" in text
    assert "READ" not in text


def test_a_verdict_for_another_commit_or_over_a_changed_tree_is_not_read(judged):
    """Untracked counts, even hidden by git config: the suite reads files nobody committed."""
    root, state = judged
    _git(root, "config", "status.showUntrackedFiles", "no")
    (root / "tests" / "test_uncommitted.py").write_text(
        "def test_nobody_committed():\n    assert True\n", encoding="utf-8"
    )
    batch = _batch(root, state, "hidden")
    assert batch.baseline_source == "measured"
    assert "uncommitted or untracked" in batch.baseline_note
    _commit(root, "a later commit")
    batch = _batch(root, state, "moved")
    assert batch.valid, batch.invalid_reason
    assert batch.baseline_source == "measured"
    assert "it is for commit" in batch.baseline_note


def test_a_red_verdict_for_this_commit_refuses_the_batch(red_repo, battery_on):
    state = battery_on(red_repo)
    (red_repo / "tests" / "test_branch.py").write_text(
        "def test_the_branch_broke():\n    assert False\n", encoding="utf-8"
    )
    _commit(red_repo, "the branch breaks a test")
    assert battery.cmd_compare(None) == 1
    with pytest.raises(mutate.DriverRefusal) as caught:
        _batch(red_repo, state, "red-verdict")
    message = str(caught.value)
    assert "BASELINE IS NOT GREEN: 1 failing" in message
    assert "read from the battery's verdict" in message
    assert "tests/test_branch.py::test_the_branch_broke" in message


def _edited_verdict(state: Path, **fields) -> None:
    path = state / mutate.BATTERY_VERDICT.name
    record = json.loads(path.read_text(encoding="utf-8"))
    record.update(fields)
    path.write_text(json.dumps(record), encoding="utf-8")


@pytest.mark.parametrize(
    ("fields", "why"),
    [
        ({"clean_tree": False}, "was not clean throughout"),
        ({"host": "another-machine"}, "on another machine"),
        ({"boot_id": "another-boot"}, "on another machine"),
        ({"root": "/elsewhere/cratekit"}, "in another checkout"),
        ({"python": "/elsewhere/bin/python"}, "with another interpreter"),
        ({"known_failures_sha256": "0" * 64}, "another known failures file"),
        ({"exit_code": 2}, "did not complete"),
        ({"collected": 0}, "no collected count"),
        ({"format": 2}, "a record this driver cannot read"),
        ({"verdict": "red"}, "disagrees with the ids it lists"),
        ({"failing": "tests/test_red.py::test_that_fails"}, "a record this driver cannot read"),
        ({"commit": "unknown"}, "it is for commit"),
        ({"ran": 5}, "so the run stopped early"),
        ({"ran": None}, "so the run stopped early"),
        ({"pytest_addopts": "-x"}, "inherited PYTEST_ADDOPTS"),
        ({"collect_errors": None}, "a record this driver cannot read"),
        ({"collect_errors": ["tests/test_red.py::test_that_fails"]}, "disagrees with the ids"),
    ],
    ids=[
        "dirty-during-the-run", "another-host", "another-boot", "another-checkout",
        "another-interpreter", "another-known-failures-file", "an-interrupted-run",
        "nothing-collected", "another-format", "a-verdict-its-ids-contradict", "ids-not-a-list",
        "no-commit", "fewer-ran-than-collected", "no-count-of-what-ran", "an-edited-run",
        "collection-errors-unknown", "a-collection-error-read-clean",
    ],
)
def test_a_verdict_that_differs_in_any_key_is_not_read(judged, fields, why):
    root, state = judged
    _edited_verdict(state, **fields)
    result, note = _read_verdict(root, state)
    assert result is None
    assert why in note
    assert note.startswith("the battery's verdict was not read")


def test_an_unreadable_absent_or_unkeyed_verdict_is_not_read(judged):
    """The verdict is net of the machine's failures, so a run without them reads none."""
    root, state = judged
    result, note = _read_verdict(root, state, digest="")
    assert result is None and "no known failures file" in note
    path = state / mutate.BATTERY_VERDICT.name
    path.write_text("{ not json", encoding="utf-8")
    result, note = _read_verdict(root, state)
    assert result is None and "a record this driver cannot read" in note
    path.unlink()
    result, note = _read_verdict(root, state)
    assert result is None and "no battery verdict" in note


def test_the_verdict_names_no_machine_or_path_in_the_table(judged):
    """The table is committed to a public repository."""
    root, state = judged
    _edited_verdict(state, host="phillips-own-machine")
    text = mutate.render_markdown(_batch(root, state, "named"))
    assert "phillips-own-machine" not in text
    assert str(root) not in text
    assert "on another machine" in text


def test_the_command_line_reads_the_verdict_and_measures_on_request(judged):
    root, state = judged
    spec = root.parent / "rows.toml"
    spec.write_text(
        'name = "cli"\npass_kind = "light"\n\n[[rows]]\nid = "K1"\n'
        'description = "Raise the clamp\'s limit"\nfile = "src/fixtpkg/guards.py"\n'
        "old = 'if value > limit:'\nnew = 'if value > 10000:'\n",
        encoding="utf-8",
    )
    base = ["mutate.py", str(spec), "--repo-root", str(root)]
    base += ["--known-failures", str(state / "baseline.txt")]
    assert mutate.main([*base, "--out-dir", str(root.parent / "read")]) == 0
    read = json.loads((root.parent / "read" / "cli.json").read_text(encoding="utf-8"))
    assert read["baseline_source"] == "read"
    out = ["--out-dir", str(root.parent / "measured"), "--measure-baseline"]
    assert mutate.main([*base, *out]) == 0
    measured = json.loads((root.parent / "measured" / "cli.json").read_text(encoding="utf-8"))
    assert measured["baseline_source"] == "measured"
    assert "--measure-baseline" in measured["baseline_note"]
    assert measured["pytest_runs"] == read["pytest_runs"] + 1
    assert [r["killed"] for r in measured["rows"]] == [r["killed"] for r in read["rows"]]


def test_the_driver_and_the_battery_name_one_record():
    assert mutate.BATTERY_VERDICT == Path(".cloud-battery") / battery.RUN_RECORD_NAME
    assert battery.STATE.name == mutate.BATTERY_VERDICT.parent.as_posix()
    assert mutate.BATTERY_VERDICT_FORMAT == battery.RUN_RECORD_FORMAT
    assert mutate.BOOT_ID == battery.BOOT_ID


def test_a_run_that_stopped_early_with_exit_one_is_not_read(red_repo, battery_on):
    """Serially, a test ending the session exits 1 as a complete red run does, and
    compare still reads it clean; only the count of tests that reported tells."""
    state = battery_on(red_repo)
    (red_repo / "tests" / "test_zzz_stop.py").write_text(
        "import pytest\n\n\ndef test_a_stop():\n    pytest.exit('stop', returncode=1)\n\n\n"
        "def test_b_never_run():\n    assert True\n",
        encoding="utf-8",
    )
    _commit(red_repo, "a test that stops the session")
    assert battery.cmd_compare(None) == 0
    record = json.loads((state / mutate.BATTERY_VERDICT.name).read_text(encoding="utf-8"))
    assert record["exit_code"] == 1
    assert record["ran"] < record["collected"]
    result, note = _read_verdict(red_repo, state)
    assert result is None
    assert "stopped early" in note


def test_a_status_git_cannot_read_is_never_a_clean_tree(judged):
    root, state = judged
    (root / ".git" / "index").write_bytes(b"not an index")
    result, note = _read_verdict(root, state)
    assert result is None
    assert "git could not read this tree's status" in note


def test_an_entry_added_directly_under_the_root_stops_the_batch_at_that_row(
    leak_repo, monkeypatch, tmp_path
):
    """R-1917: a child that leaves a folder at the filesystem root is caught where it ran,
    though it touched neither watched root. A stand in plays the root."""
    guarded = _guarded(tmp_path)
    top = tmp_path / "stand-in-root"
    (top / "usr").mkdir(parents=True)
    monkeypatch.setenv("MUTATE_FIXTURE_LEAK_TARGET", str(top / "left-behind"))
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.measure_batch(
            leak_repo, "leak-top", [_row("LEAKY", "        return limit", "        return value")],
            guard=mutate.take_state_guard((guarded,), top=top),
        )
    message = str(caught.value)
    assert "row LEAKY" in message
    assert "added left-behind" in message
    assert "R-1917" in message
    assert "the full baseline" not in message
    _assert_untouched(leak_repo)


def test_a_name_added_removed_or_retyped_under_the_root_is_a_leak_and_a_deeper_write_is_not(
    tmp_path,
):
    top = tmp_path / "stand-in-root"
    (top / "tmp").mkdir(parents=True)
    (top / "etc").mkdir()
    guard = mutate.take_state_guard((), top=top)
    assert guard.describe() == f"the names directly under {top} (2)"
    (top / "tmp" / "churn").write_text("a child's scratch file", encoding="utf-8")
    (top / "tmp" / "deeper").mkdir()
    mutate.check_state_guard(guard, label="a child writing in its temporary folder")

    sentinel = top / "cratekit-r926-outside-every-test-root"
    sentinel.mkdir()
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.check_state_guard(guard, label="row G1")
    assert "added cratekit-r926-outside-every-test-root" in str(caught.value)
    assert "row G1" in str(caught.value)

    guard = mutate.take_state_guard((), top=top)
    sentinel.rmdir()
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.check_state_guard(guard, label="a child that removed one")
    assert "removed cratekit-r926-outside-every-test-root" in str(caught.value)

    guard = mutate.take_state_guard((), top=top)
    (top / "etc").rmdir()
    (top / "etc").write_text("a file where a folder was", encoding="utf-8")
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.check_state_guard(guard, label="a child that replaced one")
    assert "changed etc" in str(caught.value)

    guard = mutate.take_state_guard((), top=top)
    shutil.rmtree(top)
    with pytest.raises(mutate.StateLeak) as caught:
        mutate.check_state_guard(guard, label="a child that took the root away")
    assert "can no longer be listed (FileNotFoundError)" in str(caught.value)
    assert "removed tmp" not in str(caught.value)


def test_the_guard_lists_the_filesystem_root_by_default(tmp_path, _stand_in_filesystem_root):
    real = _stand_in_filesystem_root
    assert real == Path(os.path.abspath(os.sep))
    assert mutate.top_level_entries(real), "the filesystem root read as empty"
    (mutate.FILESYSTEM_ROOT / "a-name").mkdir()
    guard = mutate.take_state_guard((tmp_path,))
    assert guard.top == mutate.FILESYSTEM_ROOT != real
    assert guard.top_entries == ("a-name\tdir",)


def test_a_root_that_cannot_be_listed_refuses_the_batch_rather_than_reading_as_unchanged(
    tmp_path,
):
    """Two unreadable listings are equal, so a guard taken over one would pass every child."""
    with pytest.raises(mutate.DriverRefusal) as refused:
        mutate.take_state_guard((), top=tmp_path / "missing")
    assert "R-1917" in str(refused.value)
    assert "FileNotFoundError" in str(refused.value)
