"""Tests for ``scripts/cloud_battery.py``, the Linux battery read against the base.

The clones are real (U200), shallow over ``file://`` and unshallowed by the real
fetch; the scratch suites below fail chosen whole ids (U268); and the places are
read off a mount table the test writes (U273), so they are the same on the
container and on the Mac, which has no mount table.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import socket
import subprocess
import sys
from itertools import takewhile
from pathlib import Path

import pytest

from tests import _stealing_suite as stealing

REPO_ROOT = Path(__file__).resolve().parent.parent
HOST = socket.gethostname()


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
    cmd = ["git", "-c", "user.email=battery@test", "-c", "user.name=battery", *args]
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)


def _must_not_run(*_a, **_k):
    raise AssertionError("the suite ran when it should have been refused")


def _refuse_runs(monkeypatch, *names: str) -> None:
    for name in names or ("ensure_full_history", "measure_suite"):
        monkeypatch.setattr(battery, name, _must_not_run)


def _point(monkeypatch, root: Path, head: str | None = None) -> Path:
    """The battery pointed at ``root``, its history and static checks passed; the state dir."""
    state = root / ".cloud-battery"
    for name in stealing.INHERITED_RUN_STATE:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(battery, "ROOT", root)
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
    monkeypatch.setattr(battery, "VERDICT", state / "last-compare.txt")
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    monkeypatch.setattr(battery, "ensure_full_history", lambda root=None: None)
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    if head is not None:
        monkeypatch.setattr(battery, "head", lambda: head)
    return state


def _baseline_file(
    tmp_path, monkeypatch, place="disk", on_disk=(), *, fields=None, ids=("tests/a.py::t",)
) -> Path:
    """A baseline for this host; ``fields`` replaces everything after the host."""
    fields = f" temp {place} history full ids whole" if fields is None else fields
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {HOST}{fields}\n# 1 failed\n"
        + "".join(f"# on disk test {one}\n" for one in on_disk)
        + "".join(f"{i}\n" for i in ids),
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)
    return baseline


def _suite(root: Path, name: str, source: str, addopts: str = "-q") -> Path:
    """A scratch suite with its own ini, so the run is this suite's alone."""
    (root / "tests").mkdir(parents=True)
    (root / "pytest.ini").write_text(f"[pytest]\naddopts = {addopts}\n", encoding="utf-8")
    (root / "tests" / name).write_text(source, encoding="utf-8")
    return root


@pytest.fixture
def places(tmp_path, monkeypatch) -> tuple[Path, Path]:
    """A mount table of the test's own: ``shm`` a tmpfs, everything else ext4."""
    root = tmp_path / "places"
    memory, disk = root / "shm", root / "disk"
    for one in (memory, disk):
        one.mkdir(parents=True)
    table = root / "mounts"
    table.write_text(
        f"/dev/vda / ext4 rw 0 0\ntmpfs {os.path.realpath(memory)} tmpfs rw 0 0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "MOUNTS", table)
    monkeypatch.setattr(battery, "MEMORY_ROOT", memory)
    monkeypatch.setattr(battery, "MEMORY_FLOOR", 0)
    monkeypatch.setattr(battery, "disk_root", lambda: disk)
    return memory, disk


# Full history before anything is measured, U200


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
    return repo, _git(repo, "rev-list", "--max-parents=0", "HEAD").stdout.strip()


def _clone(origin_repo: Path, dest: Path, *, shallow: bool) -> Path:
    args = ["clone", *(["--depth", "1"] if shallow else [])]
    done = _git(origin_repo.parent, *args, origin_repo.as_uri(), str(dest))
    assert done.returncode == 0, done.stderr
    return dest


def _is_shallow(repo: Path) -> str:
    return _git(repo, "rev-parse", "--is-shallow-repository").stdout.strip()


def _shallow_clone(origin, tmp_path, monkeypatch) -> tuple[Path, Path]:
    """A shallow clone with the battery pointed at it, its history read for real."""
    clone = _clone(origin[0], tmp_path / "clone", shallow=True)
    real = battery.ensure_full_history
    state = _point(monkeypatch, clone)
    monkeypatch.setattr(battery, "ensure_full_history", real)
    assert _is_shallow(clone) == "true"
    return clone, state


def test_a_shallow_clone_is_unshallowed_and_the_baseline_header_says_so(
    origin, tmp_path, monkeypatch, places
):
    clone, state = _shallow_clone(origin, tmp_path, monkeypatch)
    first = origin[1]
    assert _git(clone, "cat-file", "-e", first).returncode != 0, "the old commit is absent"
    monkeypatch.setattr(
        battery,
        "measure_suite",
        lambda place=None: battery.SuiteRun(
            frozenset({"tests/a.py::t"}), "1 failed", 1, frozenset(), 1, place=place
        ),
    )
    assert battery.cmd_baseline(None) == 0
    assert _is_shallow(clone) == "false"
    assert _git(clone, "cat-file", "-e", first).returncode == 0
    header = (state / "baseline.txt").read_text(encoding="utf-8").splitlines()[0]
    assert header.endswith(" temp disk history full ids whole")
    assert battery.read_baseline() == battery.Baseline(
        {"tests/a.py::t"}, header.split()[2], "disk", ()
    )


def test_a_remote_that_cannot_serve_the_history_refuses_baseline_and_compare(
    origin, tmp_path, monkeypatch, capsys, places
):
    clone, state = _shallow_clone(origin, tmp_path, monkeypatch)
    origin[0].rename(tmp_path / "gone")
    _refuse_runs(monkeypatch, "static_checks", "measure_suite")
    assert battery.cmd_baseline(None) == 1
    assert not (state / "baseline.txt").exists()
    assert "history: REFUSED, the clone is still shallow" in capsys.readouterr().out
    assert _is_shallow(clone) == "true"
    _baseline_file(tmp_path, monkeypatch)
    assert battery.cmd_compare(None) == 1


def test_a_complete_clone_runs_no_fetch(origin, tmp_path, monkeypatch):
    """Every git call is recorded: a fetch failing on a complete clone still returns None."""
    clone = _clone(origin[0], tmp_path / "clone", shallow=False)
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


def test_a_directory_git_cannot_read_is_never_read_as_complete_or_clean(tmp_path, monkeypatch):
    """Absence is not evidence: no answer from git is neither `false` nor an empty status."""
    assert battery.ensure_full_history(tmp_path) is not None
    monkeypatch.setattr(battery, "ROOT", tmp_path)
    assert battery.tree_state() == battery.TreeState(commit="", clean=False)


@pytest.mark.parametrize(
    ("fields", "said"),
    [
        ("", ["full history"]),
        (" history shallow", ["full history"]),
        (" history full", ["first space", "scripts/cloud_battery.py baseline"]),
        (" history full ids whole", ["U273", "scripts/cloud_battery.py baseline"]),
        (" temp tmpfs history full ids whole", ["U273"]),
        (" temp elsewhere history full ids whole", ["U273"]),
    ],
    ids=["before-u200", "shallow", "before-u268", "before-u273", "a-filesystem", "unknown"],
)
def test_a_baseline_without_a_field_compare_needs_is_refused_saying_why(
    fields, said, tmp_path, monkeypatch, capsys
):
    """A baseline from before U268 kept ids cut at a space, so it is never read beside whole ids."""
    _baseline_file(tmp_path, monkeypatch, fields=fields, ids=("tests/a.py::t[one",))
    _refuse_runs(monkeypatch)
    assert battery.read_baseline() is None
    out = capsys.readouterr().out
    assert all(text in out for text in said), out
    assert battery.cmd_compare(None) == 2


# The suite run reads a work stealing run exactly, U251


def test_the_suite_command_leaves_the_distribution_to_addopts(monkeypatch, places):
    """The battery passes nothing that would override ``pyproject.toml``."""
    seen = []

    def recording_run(cmd, env=None):
        seen.append((cmd, Path(env["TMPDIR"])))
        assert seen[-1][1].is_dir()
        Path(env[battery.REPORT_VARIABLE]).write_text(
            '{"failed": {"ids": ["tests/a.py::t"], "counted": 1},'
            ' "error": {"ids": [], "counted": 0}}',
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(cmd, 1, stdout="1 failed, 2 passed\n", stderr="")

    monkeypatch.setattr(battery, "run", recording_run)
    measured = battery.measure_suite("disk")
    assert (measured.ids, measured.summary, measured.place) == (
        {"tests/a.py::t"}, "1 failed, 2 passed", "disk"
    )
    # A fresh temporary directory in the place, gone after the run.
    ((command, temp),) = seen
    assert temp.parent.parent == places[1]
    assert not temp.exists()
    # The whole command, so no new spelling of a worker count or distribution gets past.
    assert command[0] == str(battery.PYTHON)
    assert command[1:] == [
        *("-m", "pytest", "--tb=no", "-p", battery.PLUGIN_MODULE, "-p", "no:cacheprovider")
    ]


def test_a_failure_that_moved_between_workers_is_read_by_its_id(tmp_path, monkeypatch, places):
    """The real run, under the repository's distribution, with a stolen failure.

    Under xdist the controller collects nothing itself, so the count is a worker's.
    """
    suite = stealing.write(tmp_path / "suite")
    log = tmp_path / "workers"
    stealing.prepare_environment(monkeypatch, log)
    monkeypatch.setattr(battery, "ROOT", suite)
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    measured = battery.measure_suite("disk")
    assert measured.ids == {stealing.STOLEN_FAILURE}
    assert f"1 failed, {stealing.FULL_COUNT - 1} passed" in measured.summary
    assert measured.collected == stealing.FULL_COUNT
    stealing.assert_the_failure_moved(log)


# Every failing id is read and compared whole, U268

#: Ids that differ only after a space, or after ` - `, the separator a summary
#: line puts after an id; which fail is read from the environment.
SPACED_SUITE = '''import os

import pytest
FAILING = set(filter(None, os.environ.get("BATTERY_FIXTURE_FAILING", "").split("|")))
@pytest.mark.parametrize("case", ["one two", "one three", "x - y", "x - z"])
def test_case(case):
    assert case not in FAILING
@pytest.fixture(params=["setup a", "setup b"])
def resource(request):
    if request.param in FAILING:
        raise RuntimeError("the fixture cannot be set up")
    return request.param
def test_with_resource(resource):
    assert resource
'''

FAILING_VARIABLE = "BATTERY_FIXTURE_FAILING"
SPACED = "tests/test_spaced.py::test_case"
RESOURCE = "tests/test_spaced.py::test_with_resource"


@pytest.fixture
def spaced(tmp_path, monkeypatch, places) -> Path:
    """The battery pointed at the scratch suite, with nothing but the suite real."""
    suite = _suite(tmp_path / "suite", "test_spaced.py", SPACED_SUITE)
    _point(monkeypatch, suite, head="abc1234")
    monkeypatch.setattr(battery, "ON_DISK", ())
    return suite


def _listed_under(out: str, heading: str) -> list[str]:
    """The ids `compare` printed under one of its headings."""
    lines = out.splitlines()
    start = next(n for n, line in enumerate(lines) if line.startswith(heading))
    return [line[2:] for line in takewhile(lambda one: one.startswith("  "), lines[start + 1 :])]


@pytest.mark.parametrize(
    ("base", "branch", "new", "gone", "still"),
    [
        ("one two", "one three", [f"{SPACED}[one three]"], [f"{SPACED}[one two]"], 0),
        ("x - y", "x - z|x - y", [f"{SPACED}[x - z]"], [], 1),
        ("setup a", "setup b", [f"{RESOURCE}[setup b]"], [f"{RESOURCE}[setup a]"], 0),
        ("one two|x - y|setup a", "one two|x - y|setup a", [], [], 3),
    ],
    ids=["after-a-space", "the-summary-separator", "an-error", "the-same-failures"],
)
def test_compare_reads_each_failure_by_its_whole_id(
    spaced, monkeypatch, capsys, base, branch, new, gone, still
):
    monkeypatch.setenv(FAILING_VARIABLE, base)
    assert battery.cmd_baseline(None) == 0
    capsys.readouterr()
    monkeypatch.setenv(FAILING_VARIABLE, branch)
    assert battery.cmd_compare(None) == (1 if new else 0)
    out = capsys.readouterr().out
    assert _listed_under(out, "NEWLY FAILING, yours") == new
    assert _listed_under(out, "no longer failing") == gone
    assert f"NEWLY FAILING, yours: {len(new)}" in out
    assert f"still failing, the machine's: {still}" in out
    if still:
        baseline = (spaced / ".cloud-battery" / "baseline.txt").read_text(encoding="utf-8")
        assert f"\n{SPACED}[x - y]\n" in baseline


def test_a_file_that_cannot_be_collected_is_read_by_its_path(spaced, monkeypatch):
    (spaced / "tests" / "test_broken.py").write_text("import not_a_module_here\n")
    monkeypatch.setenv(FAILING_VARIABLE, "")
    for place in ("memory", None):
        suite = battery.measure_suite(place)
        assert suite.ids == suite.collect_errors == {"tests/test_broken.py"}
        assert "1 error" in suite.summary
        assert suite.exit_code == 2


def test_a_whole_baseline_reads_back_unchanged(tmp_path, monkeypatch):
    ids = {f"{SPACED}[one two]", f"{SPACED}[x - y]", "tests/test_été.py::t"}
    listed = ("tests/a.py::needs[a disk]", "tests/b.py::too")
    _baseline_file(tmp_path, monkeypatch, "memory", on_disk=listed, ids=sorted(ids))
    assert battery.read_baseline() == battery.Baseline(ids, "abc123", "memory", listed)


def _report(failed=(), errors=(), failed_counted=None, errors_counted=None) -> dict:
    counted = (failed_counted, errors_counted)
    return {
        key: {"ids": list(ids), "counted": len(ids) if count is None else count}
        for key, ids, count in zip(("failed", "error"), (failed, errors), counted, strict=True)
    }


@pytest.mark.parametrize(
    ("failed", "errors", "summary"),
    [
        ([f"{SPACED}[one two]"], ["tests/test_broken.py"], "1 failed, 4 passed, 1 error in 0.1s"),
        (["tests/a.py::t[a b]", "tests/a.py::t[a c]"], ["tests/b.py::u[x - y]", "tests/c.py"],
         "2 failed, 9 passed, 2 errors in 0.10s"),
    ],
    ids=["singular", "plural"],
)
def test_a_report_that_agrees_with_the_summary_line_is_read(failed, errors, summary):
    """pytest writes `1 error` and `2 errors`; both are counts, never a refusal."""
    assert battery.read_report(_report(failed, errors), summary) == {*failed, *errors}


@pytest.mark.parametrize(
    ("report", "summary"),
    [
        (_report(), "1 failed, 2 passed in 0.10s"),
        (_report(failed=["tests/a.py::t"]), "2 failed in 0.10s"),
        (_report(errors=["tests/a.py::t"]), "1 passed in 0.10s"),
        (_report(failed=[], failed_counted=1), "1 failed in 0.10s"),
        ({"failed": {"ids": [], "counted": 0}}, "1 passed in 0.10s"),
        *(
            (_report(failed=[nodeid]), "1 failed in 0.10s")
            for nodeid in (
                *("", "tests/a.py::t[a\nb]", "tests/a.py::t[a\rb]", "tests/a\x0bb.py::t"),
                *("tests/a\u2028b.py::t", " tests/a.py::t", "# tests/a.py::t", None),
            )
        ),
    ],
    ids=[
        *("a-failure-the-report-missed", "fewer-failures-than-the-summary"),
        *("an-error-the-summary-never-counted", "counted-but-not-listed", "no-error-entry"),
        *("an-empty-id", "a-line-break", "a-carriage-return", "a-vertical-tab"),
        *("a-line-separator", "padded", "a-comment", "not-a-string"),
    ],
)
def test_a_report_that_cannot_be_read_whole_is_refused(report, summary):
    with pytest.raises(SystemExit, match="cannot be read"):
        battery.read_report(report, summary)


def test_a_run_that_wrote_no_report_is_refused(spaced, monkeypatch):
    """A summary line alone is never read for ids, whatever it says."""

    def summary_only(cmd, env=None):
        return subprocess.CompletedProcess(cmd, 1, stdout="1 failed, 2 passed\n", stderr="")

    monkeypatch.setattr(battery, "run", summary_only)
    with pytest.raises(SystemExit, match="wrote no report"):
        battery.measure_suite("disk")


# The run record the mutation driver reads in place of its full baseline, U271;
# the driver's side is in `tests/test_mutation_driver.py`.


@pytest.fixture
def judged_repo(tmp_path, monkeypatch, places) -> Path:
    """A git repository holding the spaced suite, the battery pointed at it."""
    root = _suite(tmp_path / "repo", "test_spaced.py", SPACED_SUITE)
    (root / ".gitignore").write_text(".cloud-battery/\n__pycache__/\n", encoding="utf-8")
    for args in (("init", "-b", "main"), ("add", "-A"), ("commit", "-m", "suite")):
        assert _git(root, *args).returncode == 0
    _point(monkeypatch, root.resolve())
    monkeypatch.setenv(FAILING_VARIABLE, "one two")
    return root


def _record(root: Path) -> dict:
    return json.loads((root / ".cloud-battery" / "verdict.json").read_text(encoding="utf-8"))


def _last(root: Path) -> str:
    return (root / ".cloud-battery" / "last-compare.txt").read_text()


def _head(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def _digest(root: Path) -> str:
    return hashlib.sha256((root / ".cloud-battery" / "baseline.txt").read_bytes()).hexdigest()


def test_each_run_records_every_key_the_driver_reads(judged_repo, monkeypatch):
    """A `PYTEST_ADDOPTS` the run inherited edits it, so the record names it."""
    monkeypatch.setenv("PYTEST_ADDOPTS", "-p no:cacheprovider")
    assert battery.cmd_baseline(None) == 0
    record, head = _record(judged_repo), _head(judged_repo)
    assert (record["source"], record["verdict"], record["commit"]) == ("baseline", "clean", head)
    assert record["known_failures_sha256"] == _digest(judged_repo)
    # The release reads compare's verdict only, never a baseline's.
    assert not (judged_repo / ".cloud-battery" / "last-compare.txt").exists()

    assert battery.cmd_compare(None) == 0
    record = _record(judged_repo)
    expected = dict(
        format=battery.RUN_RECORD_FORMAT, source="compare", commit=head, clean_tree=True,
        host=HOST, root=str(judged_repo.resolve()), python=sys.executable,
        known_failures_sha256=_digest(judged_repo), verdict="clean", collected=6, ran=6,
        exit_code=1, pytest_addopts="-p no:cacheprovider", failing=[f"{SPACED}[one two]"],
        collect_errors=[],
    )
    assert {key: record[key] for key in expected} == expected
    assert _last(judged_repo) == f"{head} clean\n"

    monkeypatch.setenv(FAILING_VARIABLE, "one two|one three")
    assert battery.cmd_compare(None) == 1
    record = _record(judged_repo)
    assert record["verdict"] == "red"
    assert record["failing"] == [f"{SPACED}[one three]", f"{SPACED}[one two]"]
    assert _last(judged_repo) == f"{head} red\n"


def _during_the_run(monkeypatch, act) -> None:
    real = battery.measure_suite

    def measure(place=None):
        measured = real(place)
        act()
        return measured

    monkeypatch.setattr(battery, "measure_suite", measure)


def _commit_later(root: Path) -> None:
    with open(root / "later.txt", "a", encoding="utf-8") as later:
        later.write("committed while the suite ran\n")
    assert _git(root, "add", "later.txt").returncode == 0
    assert _git(root, "commit", "-m", "later").returncode == 0


def test_a_commit_made_during_the_run_is_never_recorded_as_measured(judged_repo, monkeypatch):
    """The sha is read before the run, for the baseline's header and for the record."""
    measured_head = _head(judged_repo)
    _during_the_run(monkeypatch, lambda: _commit_later(judged_repo))
    assert battery.cmd_baseline(None) == 0
    header = (judged_repo / ".cloud-battery" / "baseline.txt").read_text().splitlines()[0]
    assert measured_head.startswith(header.split()[2])
    assert _record(judged_repo)["clean_tree"] is False

    compared_head = _head(judged_repo)
    assert compared_head != measured_head
    assert battery.cmd_compare(None) == 0
    record = _record(judged_repo)
    assert _head(judged_repo) != compared_head
    assert record["commit"] == compared_head
    assert record["clean_tree"] is False
    assert _last(judged_repo) == f"{compared_head} dirty\n"


@pytest.mark.parametrize("when", ["before", "during", "hidden"])
def test_a_change_to_the_tree_marks_the_run_unclean(judged_repo, monkeypatch, when):
    assert battery.cmd_baseline(None) == 0
    stray = judged_repo / "stray.txt"
    if when == "during":
        _during_the_run(monkeypatch, lambda: stray.write_text("untracked\n", encoding="utf-8"))
    else:
        if when == "hidden":
            assert _git(judged_repo, "config", "status.showUntrackedFiles", "no").returncode == 0
        stray.write_text("untracked\n", encoding="utf-8")
        assert battery.tree_state().clean is False
    assert battery.cmd_compare(None) == 0
    assert _record(judged_repo)["clean_tree"] is False
    assert _last(judged_repo).endswith(" dirty\n")


def test_collection_errors_the_report_does_not_list_as_errors_are_unknown():
    report = {"collect_errors": ["tests/test_broken.py"]}
    broken = {"tests/test_broken.py"}
    assert battery._read_collect_errors(report, broken) == broken
    assert battery._read_collect_errors(report, {"tests/test_other.py"}) is None
    assert battery._read_collect_errors({}, broken) is None


SKIPPING_SUITE = '''import pytest

@pytest.fixture
def broken():
    raise RuntimeError("cannot be set up")
def test_passes():
    assert True
@pytest.mark.skip(reason="skipped")
def test_skipped():
    assert False
@pytest.mark.xfail(run=False, reason="never run")
def test_never_run():
    assert False
def test_setup_error(broken):
    assert broken
'''


@pytest.mark.parametrize("workers", [[], ["-p", "xdist", "-n", "2"]], ids=["serial", "workers"])
def test_a_skip_an_unrun_xfail_and_a_setup_error_each_count_as_run(tmp_path, monkeypatch, workers):
    """Counted only by their call, these would read as unrun and the record never be read."""
    addopts = " ".join(["-q", *workers])
    root = _suite(tmp_path / "suite", "test_kinds.py", SKIPPING_SUITE, addopts)
    _point(monkeypatch, root)
    suite = battery.measure_suite()
    assert suite.ids == {"tests/test_kinds.py::test_setup_error"}
    assert suite.collected == suite.ran == 4


# Temporary files in one named place, memory or disk, U273


@pytest.mark.parametrize(("measured", "asked"), [("memory", "disk"), ("disk", "memory")])
def test_a_compare_in_the_other_place_from_its_baseline_is_refused(
    measured, asked, places, tmp_path, monkeypatch, capsys
):
    _baseline_file(tmp_path, monkeypatch, measured)
    _refuse_runs(monkeypatch)
    assert battery.main(["compare", "--temp", asked]) == 2
    out = capsys.readouterr().out
    assert "REFUSED" in out
    assert f"--temp {measured}" in out


@pytest.mark.parametrize("place", ["memory", "disk"])
def test_a_compare_naming_no_place_runs_in_the_baselines(place, places, tmp_path, monkeypatch):
    _point(monkeypatch, tmp_path)
    _baseline_file(tmp_path, monkeypatch, place)
    seen = []

    def measured(where=None):
        seen.append(where)
        return battery.SuiteRun(
            frozenset({"tests/a.py::t"}), "1 failed", 1, frozenset(), 1, ran=1, place=where
        )

    monkeypatch.setattr(battery, "measure_suite", measured)
    assert battery.main(["compare"]) == 0
    assert battery.main(["compare", "--temp", place]) == 0
    assert seen == [place, place]


def test_a_place_the_machine_cannot_give_refuses_baseline_and_compare(
    places, tmp_path, monkeypatch, capsys
):
    monkeypatch.setattr(battery, "MEMORY_FLOOR", 2**80)
    _refuse_runs(monkeypatch)
    assert battery.main(["baseline", "--temp", "memory"]) == 1
    assert "REFUSED" in capsys.readouterr().out
    _baseline_file(tmp_path, monkeypatch, "memory")
    assert battery.main(["compare"]) == 2
    out = capsys.readouterr().out
    assert "REFUSED" in out and "GiB" in out


def test_a_mount_table_is_read_by_its_longest_mount_point(tmp_path, monkeypatch):
    table = tmp_path / "mounts"
    table.write_text(
        "/dev/vda / ext4 rw 0 0\n"
        "tmpfs /dev/shm tmpfs rw 0 0\n"
        "tmpfs /srv/with\\040space tmpfs rw 0 0\n"
        "/dev/vdb /srv ext4 rw 0 0\n"
        "overlay /data ext4 rw 0 0\n"
        "tmpfs /data tmpfs rw 0 0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "MOUNTS", table)
    # The later of two mounts at `/data` covers the earlier.
    for path, kind in (
        *(("/dev/shm/x", "tmpfs"), ("/dev/shmother", "ext4"), ("/srv/with space/x", "tmpfs")),
        *(("/srv/x", "ext4"), ("/data/x", "tmpfs"), ("/opt/x", "ext4")),
    ):
        assert battery.filesystem_of(Path(path)) == kind, path
    monkeypatch.setattr(battery, "MOUNTS", tmp_path / "absent")
    assert battery.filesystem_of(Path("/dev/shm/x")) is None


def test_each_place_is_given_only_where_it_is_what_it_names(places, monkeypatch):
    memory, disk = places
    assert battery.place_root("memory") == (memory, "")
    assert battery.place_root("disk") == (disk, "")
    assert battery.place_root("elsewhere")[0] is None
    monkeypatch.setattr(battery, "MEMORY_FLOOR", 2**80)
    root, why = battery.place_root("memory")
    assert root is None and "GiB" in why
    monkeypatch.setattr(battery, "MEMORY_FLOOR", 0)
    monkeypatch.setattr(battery, "MEMORY_ROOT", memory.parent / "disk")
    root, why = battery.place_root("memory")
    assert root is None and "not a memory filesystem" in why
    monkeypatch.setattr(battery, "disk_root", lambda: memory)
    root, why = battery.place_root("disk")
    assert root is None and "memory filesystem" in why


def test_a_memory_run_whose_disk_rerun_cannot_be_given_is_refused_before_it_runs(
    places, tmp_path, monkeypatch, capsys
):
    """The disk the rerun needs is checked first, never after a whole run in memory."""
    monkeypatch.setattr(battery, "disk_root", lambda: places[0])
    _refuse_runs(monkeypatch)
    assert battery.main(["baseline", "--temp", "memory"]) == 1
    assert "run again on disk" in capsys.readouterr().out
    _baseline_file(tmp_path, monkeypatch, "memory")
    assert battery.main(["compare"]) == 2
    assert "run again on disk" in capsys.readouterr().out
    monkeypatch.setattr(battery, "ON_DISK", ())
    assert battery.refusal_for("memory") is None


#: Writes where each test's temporary directory was; one test passes only on disk.
PLACED_SUITE = '''import os
import tempfile
from pathlib import Path

import pytest
def _note(name):
    with open(os.environ["PLACED_LOG"], "a", encoding="utf-8") as log:
        log.write(f"{name} {os.path.realpath(tempfile.gettempdir())}\\n")
def _in_memory():
    return os.path.realpath(tempfile.gettempdir()).startswith(os.environ["PLACED_MEMORY"] + os.sep)
def test_needs_a_disk():
    _note("needs_a_disk")
    assert not _in_memory()
def test_needs_a_disk_and_fails_there_too():
    _note("fails_on_disk")
    assert os.environ.get("PLACED_DISK_FAILS") != "1"
def test_anywhere(tmp_path):
    _note("anywhere")
    (tmp_path / "f").write_text("x")
def test_skipped_on_disk():
    if not _in_memory():
        pytest.skip("only in memory")
'''

NEEDS_A_DISK = "tests/test_placed.py::test_needs_a_disk"
FAILS_ON_DISK = "tests/test_placed.py::test_needs_a_disk_and_fails_there_too"


@pytest.fixture
def placed(tmp_path, monkeypatch, places) -> tuple[Path, Path, Path]:
    """The battery pointed at the placed suite, its places synthetic and real directories."""
    memory, _ = places
    suite = _suite(tmp_path / "suite", "test_placed.py", PLACED_SUITE)
    log = tmp_path / "placed.log"
    _point(monkeypatch, suite, head="abc1234")
    monkeypatch.setenv("PLACED_LOG", str(log))
    monkeypatch.setenv("PLACED_MEMORY", os.path.realpath(memory))
    monkeypatch.setattr(battery, "ON_DISK", (NEEDS_A_DISK,))
    return suite, log, memory


def _where(log: Path) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        name, where = line.split(" ", 1)
        seen.setdefault(name, []).append(where)
    return seen


def test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk(placed):
    _suite_root, log, memory = placed
    disk = memory.parent / "disk"
    measured = battery.measure_suite("memory")
    # In memory it failed; on disk it passed, and the disk run is what stands.
    assert measured.ids == set()
    assert measured.place == "memory"
    assert measured.on_disk == (NEEDS_A_DISK,)
    assert measured.on_disk_summary.startswith("1 passed")
    seen = _where(log)
    real_memory, real_disk = os.path.realpath(memory), os.path.realpath(disk)
    assert [w.startswith(real_memory + os.sep) for w in seen["needs_a_disk"]] == [True, False]
    assert seen["needs_a_disk"][1].startswith(real_disk + os.sep)
    assert all(w.startswith(real_memory + os.sep) for w in seen["anywhere"])
    assert len(seen["anywhere"]) == 1, "only the listed test runs a second time"
    # Each run's directory is removed when it ends.
    assert list(memory.iterdir()) == [] and list(disk.iterdir()) == []


def test_on_disk_the_suite_runs_once_and_never_in_memory(placed):
    _suite_root, log, memory = placed
    measured = battery.measure_suite("disk")
    assert measured.ids == set()
    assert measured.on_disk == ()
    seen = _where(log)
    assert len(seen["needs_a_disk"]) == 1
    real_memory = os.path.realpath(memory) + os.sep
    assert not any(w.startswith(real_memory) for ws in seen.values() for w in ws)


@pytest.mark.parametrize(
    ("listed", "failing", "summary"),
    [((NEEDS_A_DISK, FAILS_ON_DISK), {FAILS_ON_DISK}, "1 failed"), ((), {NEEDS_A_DISK}, "")],
    ids=["a-listed-test-failing-on-disk", "an-unlisted-test-failing-in-memory"],
)
def test_the_disk_run_stands_only_for_the_tests_listed(placed, monkeypatch, listed, failing, summary):
    monkeypatch.setattr(battery, "ON_DISK", listed)
    if listed:
        monkeypatch.setenv("PLACED_DISK_FAILS", "1")
    measured = battery.measure_suite("memory")
    assert measured.ids == failing
    assert measured.on_disk == listed
    assert summary in measured.on_disk_summary


@pytest.mark.parametrize(
    "listed",
    ["tests/test_placed.py::test_skipped_on_disk", "tests/test_placed.py::test_not_there"],
    ids=["skipped-on-disk", "not-collected"],
)
def test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused(listed, placed, monkeypatch):
    monkeypatch.setattr(battery, "ON_DISK", (NEEDS_A_DISK, listed))
    with pytest.raises(SystemExit, match="cannot"):
        battery.measure_suite("memory")


def test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk(placed, capsys):
    suite, _log, _memory = placed
    baseline = suite / ".cloud-battery" / "baseline.txt"
    assert battery.main(["baseline", "--temp", "memory"]) == 0
    lines = baseline.read_text(encoding="utf-8").splitlines()
    assert lines[0] == f"# commit abc1234 host {HOST} temp memory history full ids whole"
    assert f"# on disk test {NEEDS_A_DISK}" in lines
    assert any(line.startswith("# on disk summary 1 passed") for line in lines)
    assert "temporary files: memory, then 1 test(s) again on disk" in capsys.readouterr().out
    # The record: the listed test's outcome on disk, and the memory run's counts.
    record = json.loads((suite / ".cloud-battery" / "verdict.json").read_text(encoding="utf-8"))
    assert NEEDS_A_DISK not in record["failing"]
    assert record["collected"] == record["ran"] == 4
    assert record["exit_code"] == 1, "the memory run failed the listed test"
    assert record["known_failures_sha256"] == hashlib.sha256(baseline.read_bytes()).hexdigest()

    assert battery.main(["compare"]) == 0
    assert "NEWLY FAILING, yours: 0" in capsys.readouterr().out

    # Naming no place is disk, the default (U273).
    assert battery.main(["baseline"]) == 0
    lines = baseline.read_text(encoding="utf-8").splitlines()
    assert " temp disk " in lines[0]
    assert not any(line.startswith("# on disk") for line in lines)
