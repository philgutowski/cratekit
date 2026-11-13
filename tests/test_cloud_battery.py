"""Tests for ``scripts/cloud_battery.py``, the Linux battery read against the base.

U200, from R-1191: a cloud clone is shallow, so a test that reads old history
failed on every base for want of it, the baseline recorded it as the machine's
by node id, and every later failure of that test was subtracted unread. The
battery now fetches the full history before it measures, refuses when it
cannot, and writes a baseline header that says so, which `compare` and the
mutation driver read before they subtract anything.

U268: the failing ids used to be cut out of pytest's summary lines up to
their first space, so a parametrized test failing on the base for the
machine's reason excused a sibling whose id differs only after the space. The
scratch suite below fails one case as the base and another as the branch, and
`compare` must read the second as new; the report the ids now come from is
refused when it disagrees with the summary line.

The clones here are real: a local repository with three commits, cloned at
depth one over ``file://`` so git really writes a shallow clone, and unshallowed
by the real fetch.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import socket
import subprocess
import sys
from pathlib import Path

import pytest

from tests import _stealing_suite as stealing

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
    monkeypatch.setattr(battery, "measure_suite", must_not_run)

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
    monkeypatch.setattr(
        battery,
        "measure_suite",
        lambda: battery.SuiteRun(
            ids=frozenset({"tests/a.py::t"}),
            summary="1 failed",
            collected=1,
            collect_errors=frozenset(),
            exit_code=1,
        ),
    )

    assert battery.cmd_baseline(None) == 0

    header = (state / "baseline.txt").read_text(encoding="utf-8").splitlines()[0]
    assert header.endswith(" history full ids whole")
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
    monkeypatch.setattr(battery, "measure_suite", must_not_run)

    assert battery.read_baseline() is None
    assert battery.cmd_compare(None) == 2
    assert "full history" in capsys.readouterr().out


def test_compare_refuses_a_branch_it_cannot_unshallow(origin, tmp_path, monkeypatch):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    repo.rename(tmp_path / "gone")
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} history full ids whole\ntests/a.py::t\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "ROOT", clone)
    monkeypatch.setattr(battery, "BASELINE", baseline)

    def must_not_run(*_a, **_k):
        raise AssertionError("the suite ran on a shallow clone")

    monkeypatch.setattr(battery, "static_checks", must_not_run)
    monkeypatch.setattr(battery, "failing_ids", must_not_run)
    monkeypatch.setattr(battery, "measure_suite", must_not_run)

    assert battery.cmd_compare(None) == 1


# ---------------------------------------------------------------------------
# The suite run reads a work stealing run exactly, U251
# ---------------------------------------------------------------------------


def test_the_suite_command_leaves_the_distribution_to_addopts(monkeypatch):
    """The battery passes nothing that would override ``pyproject.toml``.

    ``-o``, a worker count or a distribution here would measure a different run
    from the one a person gets from ``pytest``, and the base and the branch
    would each be read under the option the battery chose.
    """
    seen = []

    def recording_run(cmd, env=None):
        seen.append(cmd)
        Path(env[battery.REPORT_VARIABLE]).write_text(
            '{"failed": {"ids": ["tests/a.py::t"], "counted": 1},'
            ' "error": {"ids": [], "counted": 0}}',
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(cmd, 1, stdout="1 failed, 2 passed\n", stderr="")

    monkeypatch.setattr(battery, "run", recording_run)
    assert battery.failing_ids() == ({"tests/a.py::t"}, "1 failed, 2 passed")
    (command,) = seen
    # The whole command, each token read for what it changes. A list of the
    # flags forbidden would let the next spelling past (`--maxprocesses=1`,
    # `--tx popen`, `-d`); an exact command lets nothing past unread. The one
    # plugin it loads is the battery's own reporter (U268), which reads the
    # run and changes nothing in it.
    assert command[0] == str(battery.PYTHON)
    assert command[1:] == [
        "-m",
        "pytest",
        "--tb=no",
        "-p",
        battery.PLUGIN_MODULE,
        "-p",
        "no:cacheprovider",
    ]


def test_a_failure_that_moved_between_workers_is_read_by_its_id(tmp_path, monkeypatch):
    """The real run, under the repository's distribution, with a stolen failure."""
    suite = stealing.write(tmp_path / "suite")
    log = tmp_path / "workers"
    stealing.prepare_environment(monkeypatch, log)
    monkeypatch.setattr(battery, "ROOT", suite)
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    ids, summary = battery.failing_ids()
    assert ids == {stealing.STOLEN_FAILURE}
    assert f"1 failed, {stealing.FULL_COUNT - 1} passed" in summary
    stealing.assert_the_failure_moved(log)


# ---------------------------------------------------------------------------
# Every failing id is read and compared whole, U268
# ---------------------------------------------------------------------------

#: A scratch suite whose ids differ only after a space, or after ` - `, the
#: separator a summary line puts after an id. Which cases fail is read from the
#: environment, so one suite plays the base and then the branch.
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


def _spaced_suite(root: Path) -> Path:
    (root / "tests").mkdir(parents=True)
    # Its own ini, so the run is this suite's alone and not the repository's.
    (root / "pytest.ini").write_text("[pytest]\naddopts = -q\n", encoding="utf-8")
    (root / "tests" / "test_spaced.py").write_text(SPACED_SUITE, encoding="utf-8")
    return root


@pytest.fixture
def spaced(tmp_path, monkeypatch) -> Path:
    """The battery pointed at the scratch suite, with nothing but the suite real."""
    suite = _spaced_suite(tmp_path / "suite")
    state = suite / ".cloud-battery"
    for name in stealing.INHERITED_RUN_STATE:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(battery, "ROOT", suite)
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
    monkeypatch.setattr(battery, "VERDICT", state / "last-compare.txt")
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    monkeypatch.setattr(battery, "ensure_full_history", lambda root=None: None)
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    monkeypatch.setattr(battery, "head", lambda: "abc1234")
    return suite


def _measure_then_compare(monkeypatch, capsys, *, base: str, branch: str) -> tuple[int, str]:
    monkeypatch.setenv(FAILING_VARIABLE, base)
    assert battery.cmd_baseline(None) == 0
    capsys.readouterr()
    monkeypatch.setenv(FAILING_VARIABLE, branch)
    code = battery.cmd_compare(None)
    return code, capsys.readouterr().out


def _listed_under(out: str, heading: str) -> list[str]:
    """The ids `compare` printed under one of its three headings."""
    lines = out.splitlines()
    start = next(n for n, line in enumerate(lines) if line.startswith(heading))
    listed = []
    for line in lines[start + 1 :]:
        if not line.startswith("  "):
            break
        listed.append(line[2:])
    return listed


SPACED = "tests/test_spaced.py::test_case"


def test_a_new_failure_that_differs_from_the_machines_only_after_a_space_is_yours(
    spaced, monkeypatch, capsys
):
    """The card's own case: today's reader kept `test_case[one` for both."""
    code, out = _measure_then_compare(monkeypatch, capsys, base="one two", branch="one three")

    assert code == 1
    assert _listed_under(out, "NEWLY FAILING, yours") == [f"{SPACED}[one three]"]
    assert _listed_under(out, "no longer failing") == [f"{SPACED}[one two]"]
    assert "still failing, the machine's: 0" in out


def test_an_id_holding_the_summary_separator_is_read_whole(spaced, monkeypatch, capsys):
    code, out = _measure_then_compare(monkeypatch, capsys, base="x - y", branch="x - z|x - y")

    assert code == 1
    assert _listed_under(out, "NEWLY FAILING, yours") == [f"{SPACED}[x - z]"]
    assert "still failing, the machine's: 1" in out
    baseline = (spaced / ".cloud-battery" / "baseline.txt").read_text(encoding="utf-8")
    assert f"\n{SPACED}[x - y]\n" in baseline


def test_an_erroring_id_is_read_whole(spaced, monkeypatch, capsys):
    code, out = _measure_then_compare(monkeypatch, capsys, base="setup a", branch="setup b")

    assert code == 1
    erroring = "tests/test_spaced.py::test_with_resource"
    assert _listed_under(out, "NEWLY FAILING, yours") == [f"{erroring}[setup b]"]
    assert _listed_under(out, "no longer failing") == [f"{erroring}[setup a]"]


def test_the_same_failures_on_the_branch_are_the_machines(spaced, monkeypatch, capsys):
    """A control: the whole ids still match themselves, so nothing reads as new."""
    failing = "one two|x - y|setup a"
    code, out = _measure_then_compare(monkeypatch, capsys, base=failing, branch=failing)

    assert code == 0
    assert "still failing, the machine's: 3" in out
    assert "NEWLY FAILING, yours: 0" in out


def test_a_file_that_cannot_be_collected_is_read_by_its_path(spaced, monkeypatch):
    (spaced / "tests" / "test_broken.py").write_text("import not_a_module_here\n")
    monkeypatch.setenv(FAILING_VARIABLE, "")

    ids, summary = battery.failing_ids()

    assert ids == {"tests/test_broken.py"}
    assert "1 error" in summary


def test_a_baseline_written_before_u268_is_refused_with_the_command_that_measures_it(
    tmp_path, monkeypatch, capsys
):
    """Today's file kept ids cut at a space, so it is never read beside whole ids."""
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} history full\n# 1 failed\n"
        "tests/a.py::t[one\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)

    def must_not_run(*_a, **_k):
        raise AssertionError("compare ran against a baseline it should refuse")

    monkeypatch.setattr(battery, "ensure_full_history", must_not_run)
    monkeypatch.setattr(battery, "failing_ids", must_not_run)
    monkeypatch.setattr(battery, "measure_suite", must_not_run)

    assert battery.read_baseline() is None
    out = capsys.readouterr().out
    assert "first space" in out
    assert "scripts/cloud_battery.py baseline" in out
    assert battery.cmd_compare(None) == 2


def test_a_whole_baseline_reads_back_every_id_unchanged(tmp_path, monkeypatch):
    baseline = tmp_path / "baseline.txt"
    ids = {f"{SPACED}[one two]", f"{SPACED}[x - y]", "tests/test_été.py::t"}
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} history full ids whole\n# 3 failed\n"
        + "".join(f"{i}\n" for i in sorted(ids)),
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)

    assert battery.read_baseline() == (ids, "abc123")


def _report(failed=(), errors=(), failed_counted=None, errors_counted=None) -> dict:
    return {
        "failed": {
            "ids": list(failed),
            "counted": len(failed) if failed_counted is None else failed_counted,
        },
        "error": {
            "ids": list(errors),
            "counted": len(errors) if errors_counted is None else errors_counted,
        },
    }


def test_a_report_that_agrees_with_the_summary_line_is_read():
    report = _report(failed=[f"{SPACED}[one two]"], errors=["tests/test_broken.py"])
    ids = battery.read_report(report, "1 failed, 4 passed, 1 error in 0.10s")
    assert ids == {f"{SPACED}[one two]", "tests/test_broken.py"}


def test_a_plural_count_on_the_summary_line_is_read():
    """pytest writes `1 error` and `2 errors`; both are counts, never a refusal."""
    report = _report(
        failed=["tests/a.py::t[a b]", "tests/a.py::t[a c]"],
        errors=["tests/b.py::u[x - y]", "tests/c.py"],
    )
    ids = battery.read_report(report, "2 failed, 9 passed, 2 errors in 0.10s")
    assert ids == {"tests/a.py::t[a b]", "tests/a.py::t[a c]", "tests/b.py::u[x - y]", "tests/c.py"}


@pytest.mark.parametrize(
    ("report", "summary"),
    [
        (_report(), "1 failed, 2 passed in 0.10s"),
        (_report(failed=["tests/a.py::t"]), "2 failed in 0.10s"),
        (_report(errors=["tests/a.py::t"]), "1 passed in 0.10s"),
        (_report(failed=[], failed_counted=1), "1 failed in 0.10s"),
        ({"failed": {"ids": [], "counted": 0}}, "1 passed in 0.10s"),
        (_report(failed=[""]), "1 failed in 0.10s"),
        (_report(failed=["tests/a.py::t[a\nb]"]), "1 failed in 0.10s"),
        (_report(failed=["tests/a.py::t[a\rb]"]), "1 failed in 0.10s"),
        (_report(failed=["tests/a\x0bb.py::t"]), "1 failed in 0.10s"),
        (_report(failed=["tests/a\u2028b.py::t"]), "1 failed in 0.10s"),
        (_report(failed=[" tests/a.py::t"]), "1 failed in 0.10s"),
        (_report(failed=["# tests/a.py::t"]), "1 failed in 0.10s"),
        (_report(failed=[None]), "1 failed in 0.10s"),
    ],
    ids=[
        "a-failure-the-report-missed",
        "fewer-failures-than-the-summary",
        "an-error-the-summary-never-counted",
        "counted-but-not-listed",
        "no-error-entry",
        "an-empty-id",
        "a-line-break",
        "a-carriage-return",
        "a-vertical-tab",
        "a-line-separator",
        "padded",
        "a-comment",
        "not-a-string",
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
        battery.failing_ids()


# ---------------------------------------------------------------------------
# The run record the mutation driver reads in place of its full baseline, U271
# ---------------------------------------------------------------------------
#
# The driver reads it only when it is for the same commit, on a clean tree, on
# this machine, with the same known failures file, so what the battery writes
# for each of those keys is what these pin. The driver's side, reading it and
# refusing every difference, is in `tests/test_mutation_driver.py`.


def test_the_suite_run_reads_the_collected_count_and_the_collection_errors(spaced, monkeypatch):
    (spaced / "tests" / "test_broken.py").write_text("import not_a_module_here\n")
    monkeypatch.setenv(FAILING_VARIABLE, "")

    suite = battery.measure_suite()

    assert suite.ids == {"tests/test_broken.py"}
    assert suite.collect_errors == {"tests/test_broken.py"}
    assert suite.exit_code == 2


def test_a_complete_run_records_what_it_collected_and_pytests_exit(spaced, monkeypatch):
    monkeypatch.setenv(FAILING_VARIABLE, "one two")

    suite = battery.measure_suite()

    # Four cases of test_case and two of test_with_resource, every one run.
    assert suite.collected == 6
    assert suite.ran == 6
    assert suite.ids == {f"{SPACED}[one two]"}
    assert suite.collect_errors == set()
    assert suite.exit_code == 1


def test_the_collected_count_is_read_under_the_repositorys_distribution(tmp_path, monkeypatch):
    """Under xdist the controller collects nothing itself; the count is a worker's."""
    suite = stealing.write(tmp_path / "suite")
    stealing.prepare_environment(monkeypatch, tmp_path / "workers")
    monkeypatch.setattr(battery, "ROOT", suite)
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))

    assert battery.measure_suite().collected == stealing.FULL_COUNT


@pytest.fixture
def judged_repo(tmp_path, monkeypatch) -> Path:
    """A git repository holding the spaced suite, the battery pointed at it."""
    root = _spaced_suite(tmp_path / "repo")
    (root / ".gitignore").write_text(".cloud-battery/\n__pycache__/\n", encoding="utf-8")
    assert _git(root, "init", "-b", "main").returncode == 0
    assert _git(root, "add", "-A").returncode == 0
    assert _git(root, "commit", "-m", "suite").returncode == 0
    state = root / ".cloud-battery"
    for name in stealing.INHERITED_RUN_STATE:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(battery, "ROOT", root.resolve())
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
    monkeypatch.setattr(battery, "VERDICT", state / "last-compare.txt")
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    monkeypatch.setattr(battery, "ensure_full_history", lambda root=None: None)
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    monkeypatch.setenv(FAILING_VARIABLE, "one two")
    return root


def _record(root: Path) -> dict:
    return json.loads((root / ".cloud-battery" / "verdict.json").read_text(encoding="utf-8"))


def _head(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD").stdout.strip()


def test_compare_records_every_key_the_driver_reads(judged_repo):
    assert battery.cmd_baseline(None) == 0
    assert battery.cmd_compare(None) == 0

    record = _record(judged_repo)
    baseline = judged_repo / ".cloud-battery" / "baseline.txt"
    assert record["format"] == battery.RUN_RECORD_FORMAT
    assert record["source"] == "compare"
    assert record["commit"] == _head(judged_repo)
    assert record["clean_tree"] is True
    assert record["host"] == socket.gethostname()
    assert record["root"] == str(judged_repo.resolve())
    assert record["python"] == sys.executable
    assert record["known_failures_sha256"] == hashlib.sha256(baseline.read_bytes()).hexdigest()
    assert record["verdict"] == "clean"
    assert record["collected"] == 6
    assert record["ran"] == 6
    assert record["pytest_addopts"] == ""
    assert record["exit_code"] == 1
    assert record["failing"] == [f"{SPACED}[one two]"]
    assert record["collect_errors"] == []
    assert (judged_repo / ".cloud-battery" / "last-compare.txt").read_text() == (
        f"{_head(judged_repo)} clean\n"
    )


def test_baseline_records_its_run_against_the_file_it_wrote(judged_repo):
    assert battery.cmd_baseline(None) == 0

    record = _record(judged_repo)
    baseline = judged_repo / ".cloud-battery" / "baseline.txt"
    assert record["source"] == "baseline"
    assert record["verdict"] == "clean"
    assert record["commit"] == _head(judged_repo)
    assert record["known_failures_sha256"] == hashlib.sha256(baseline.read_bytes()).hexdigest()
    # The release reads compare's verdict only, never a baseline's.
    assert not (judged_repo / ".cloud-battery" / "last-compare.txt").exists()


def test_a_red_compare_is_recorded_red(judged_repo, monkeypatch):
    assert battery.cmd_baseline(None) == 0
    monkeypatch.setenv(FAILING_VARIABLE, "one two|one three")
    assert battery.cmd_compare(None) == 1

    record = _record(judged_repo)
    assert record["verdict"] == "red"
    assert record["failing"] == [f"{SPACED}[one three]", f"{SPACED}[one two]"]


def _committing_during_the_run(root: Path, real):
    def measure():
        measured = real()
        (root / "later.txt").write_text("committed while the suite ran\n", encoding="utf-8")
        assert _git(root, "add", "later.txt").returncode == 0
        assert _git(root, "commit", "-m", "later").returncode == 0
        return measured

    return measure


def test_a_commit_made_during_the_run_is_never_recorded_as_measured(judged_repo, monkeypatch):
    """The sha is read before the run: the run measured that commit, not the next."""
    assert battery.cmd_baseline(None) == 0
    measured_head = _head(judged_repo)
    monkeypatch.setattr(
        battery, "measure_suite", _committing_during_the_run(judged_repo, battery.measure_suite)
    )

    assert battery.cmd_compare(None) == 0

    record = _record(judged_repo)
    assert _head(judged_repo) != measured_head
    assert record["commit"] == measured_head
    assert record["clean_tree"] is False
    last = (judged_repo / ".cloud-battery" / "last-compare.txt").read_text()
    assert last == f"{measured_head} dirty\n"


@pytest.mark.parametrize("when", ["before", "during"])
def test_a_change_to_the_tree_marks_the_run_unclean(judged_repo, monkeypatch, when):
    assert battery.cmd_baseline(None) == 0
    stray = judged_repo / "stray.txt"
    if when == "before":
        stray.write_text("untracked\n", encoding="utf-8")
    else:
        real = battery.measure_suite

        def measure():
            measured = real()
            stray.write_text("untracked\n", encoding="utf-8")
            return measured

        monkeypatch.setattr(battery, "measure_suite", measure)

    assert battery.cmd_compare(None) == 0
    assert _record(judged_repo)["clean_tree"] is False
    assert (judged_repo / ".cloud-battery" / "last-compare.txt").read_text().endswith(" dirty\n")


def test_a_tree_git_cannot_read_is_never_recorded_clean(tmp_path, monkeypatch):
    """Absence is not evidence: no answer from git is not an empty status."""
    monkeypatch.setattr(battery, "ROOT", tmp_path)
    state = battery.tree_state()
    assert state.commit == ""
    assert state.clean is False


def test_the_record_names_a_pytest_addopts_the_run_inherited(judged_repo, monkeypatch):
    """The suite inherits it and it edits the run, so the driver must be able to see it."""
    monkeypatch.setenv("PYTEST_ADDOPTS", "-p no:cacheprovider")
    assert battery.cmd_baseline(None) == 0
    assert _record(judged_repo)["pytest_addopts"] == "-p no:cacheprovider"


def test_an_untracked_file_hidden_by_git_config_is_still_seen(judged_repo):
    assert _git(judged_repo, "config", "status.showUntrackedFiles", "no").returncode == 0
    (judged_repo / "stray.txt").write_text("untracked\n", encoding="utf-8")
    assert battery.tree_state().clean is False


def test_collection_errors_the_report_does_not_list_as_errors_are_unknown():
    report = {"collect_errors": ["tests/test_broken.py"]}
    assert battery._read_collect_errors(report, {"tests/test_broken.py"}) == {
        "tests/test_broken.py"
    }
    assert battery._read_collect_errors(report, {"tests/test_other.py"}) is None
    assert battery._read_collect_errors({}, {"tests/test_broken.py"}) is None
