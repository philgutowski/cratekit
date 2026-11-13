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

U273: a run keeps its temporary files in one named place, memory or disk,
which the baseline's header names and `compare` and the driver follow; the
tests that need a real disk run a second time on disk after a run in memory.
The places here are read off a mount table the test writes, so they are the
same on the container, where this file may itself run in memory, and on the
Mac, which has no mount table.

The clones here are real: a local repository with three commits, cloned at
depth one over ``file://`` so git really writes a shallow clone, and unshallowed
by the real fetch.
"""

from __future__ import annotations

import importlib.util
import os
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

    assert battery.cmd_baseline(None) == 1
    assert not (state / "baseline.txt").exists()


def test_a_baseline_header_says_it_was_measured_with_full_history(
    origin, tmp_path, monkeypatch, places
):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    state = clone / ".cloud-battery"
    monkeypatch.setattr(battery, "ROOT", clone)
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    monkeypatch.setattr(
        battery, "failing_ids", lambda place: battery.Run({"tests/a.py::t"}, "1 failed", place)
    )

    assert battery.cmd_baseline(None) == 0

    header = (state / "baseline.txt").read_text(encoding="utf-8").splitlines()[0]
    assert header.endswith(" temp memory history full ids whole")
    assert _is_shallow(clone) == "false"
    assert battery.read_baseline() == battery.Baseline(
        {"tests/a.py::t"}, header.split()[2], "memory", ()
    )


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


def test_compare_refuses_a_branch_it_cannot_unshallow(origin, tmp_path, monkeypatch, places):
    repo, _ = origin
    clone = _clone(repo, tmp_path / "clone", shallow=True)
    repo.rename(tmp_path / "gone")
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} temp disk history full ids whole\n"
        "tests/a.py::t\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "ROOT", clone)
    monkeypatch.setattr(battery, "BASELINE", baseline)

    def must_not_run(*_a, **_k):
        raise AssertionError("the suite ran on a shallow clone")

    monkeypatch.setattr(battery, "static_checks", must_not_run)
    monkeypatch.setattr(battery, "failing_ids", must_not_run)

    assert battery.cmd_compare(None) == 1


# ---------------------------------------------------------------------------
# The suite run reads a work stealing run exactly, U251
# ---------------------------------------------------------------------------


def test_the_suite_command_leaves_the_distribution_to_addopts(monkeypatch, places):
    """The battery passes nothing that would override ``pyproject.toml``.

    ``-o``, a worker count or a distribution here would measure a different run
    from the one a person gets from ``pytest``, and the base and the branch
    would each be read under the option the battery chose.
    """
    seen = []
    temps = []

    def recording_run(cmd, env=None):
        seen.append(cmd)
        temps.append(Path(env["TMPDIR"]))
        assert temps[-1].is_dir()
        Path(env[battery.REPORT_VARIABLE]).write_text(
            '{"failed": {"ids": ["tests/a.py::t"], "counted": 1},'
            ' "error": {"ids": [], "counted": 0}}',
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(cmd, 1, stdout="1 failed, 2 passed\n", stderr="")

    monkeypatch.setattr(battery, "run", recording_run)
    assert battery.failing_ids("disk") == battery.Run(
        {"tests/a.py::t"}, "1 failed, 2 passed", "disk"
    )
    (command,) = seen
    # The run's temporary directory is a fresh one in the place, gone after it.
    (temp,) = temps
    assert temp.parent.parent == places[1]
    assert not temp.exists()
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


def test_a_failure_that_moved_between_workers_is_read_by_its_id(tmp_path, monkeypatch, places):
    """The real run, under the repository's distribution, with a stolen failure."""
    suite = stealing.write(tmp_path / "suite")
    log = tmp_path / "workers"
    stealing.prepare_environment(monkeypatch, log)
    monkeypatch.setattr(battery, "ROOT", suite)
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    measured = battery.failing_ids("disk")
    ids, summary = measured.ids, measured.summary
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
def spaced(tmp_path, monkeypatch, places) -> Path:
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
    monkeypatch.setattr(battery, "ON_DISK", ())
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

    measured = battery.failing_ids("memory")
    ids, summary = measured.ids, measured.summary

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

    assert battery.read_baseline() is None
    out = capsys.readouterr().out
    assert "first space" in out
    assert "scripts/cloud_battery.py baseline" in out
    assert battery.cmd_compare(None) == 2


def test_a_whole_baseline_reads_back_every_id_unchanged(tmp_path, monkeypatch):
    baseline = tmp_path / "baseline.txt"
    ids = {f"{SPACED}[one two]", f"{SPACED}[x - y]", "tests/test_été.py::t"}
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} temp memory history full ids whole\n"
        "# 3 failed\n" + "".join(f"{i}\n" for i in sorted(ids)),
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)

    assert battery.read_baseline() == battery.Baseline(ids, "abc123", "memory", ())


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
        battery.failing_ids("disk")


# ---------------------------------------------------------------------------
# Temporary files in one named place, memory or disk, U273
# ---------------------------------------------------------------------------


def _synthetic_places(module, root: Path, monkeypatch) -> tuple[Path, Path]:
    """A mount table of the test's own: ``root/shm`` a tmpfs, everything else ext4.

    The places are read off the mount table, so a table written here makes
    them the same on the container, where the suite itself may run in memory,
    and on the Mac, which has no table at all.
    """
    memory = root / "shm"
    disk = root / "disk"
    memory.mkdir(parents=True)
    disk.mkdir(parents=True)
    table = root / "mounts"
    table.write_text(
        f"/dev/vda / ext4 rw 0 0\ntmpfs {os.path.realpath(memory)} tmpfs rw 0 0\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(module, "MOUNTS", table)
    monkeypatch.setattr(module, "MEMORY_ROOT", memory)
    monkeypatch.setattr(module, "MEMORY_FLOOR", 0)
    monkeypatch.setattr(module, "disk_root", lambda: disk)
    return memory, disk


@pytest.fixture
def places(tmp_path, monkeypatch) -> tuple[Path, Path]:
    return _synthetic_places(battery, tmp_path / "places", monkeypatch)


def _baseline_file(tmp_path, monkeypatch, place: str, on_disk=()) -> Path:
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} temp {place} history full ids whole\n"
        "# 1 failed\n"
        + "".join(f"# on disk test {one}\n" for one in on_disk)
        + "tests/a.py::t\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)
    return baseline


def _must_not_run(*_a, **_k):
    raise AssertionError("the suite ran when it should have been refused")


@pytest.mark.parametrize(("measured", "asked"), [("memory", "disk"), ("disk", "memory")])
def test_a_compare_in_the_other_place_from_its_baseline_is_refused(
    measured, asked, places, tmp_path, monkeypatch, capsys
):
    _baseline_file(tmp_path, monkeypatch, measured)
    monkeypatch.setattr(battery, "ensure_full_history", _must_not_run)
    monkeypatch.setattr(battery, "failing_ids", _must_not_run)

    assert battery.main(["compare", "--temp", asked]) == 2

    out = capsys.readouterr().out
    assert "REFUSED" in out
    assert f"--temp {measured}" in out


@pytest.mark.parametrize("place", ["memory", "disk"])
def test_a_compare_naming_no_place_runs_in_the_baselines(place, places, tmp_path, monkeypatch):
    _baseline_file(tmp_path, monkeypatch, place)
    monkeypatch.setattr(battery, "STATE", tmp_path / "state")
    monkeypatch.setattr(battery, "VERDICT", tmp_path / "state" / "last-compare.txt")
    monkeypatch.setattr(battery, "ensure_full_history", lambda root=None: None)
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    seen = []

    def measured(where):
        seen.append(where)
        return battery.Run({"tests/a.py::t"}, "1 failed", where)

    monkeypatch.setattr(battery, "failing_ids", measured)

    assert battery.main(["compare"]) == 0
    assert battery.main(["compare", "--temp", place]) == 0
    assert seen == [place, place]


def test_a_compare_is_refused_when_the_machine_cannot_give_the_baselines_place_now(
    places, tmp_path, monkeypatch, capsys
):
    _baseline_file(tmp_path, monkeypatch, "memory")
    monkeypatch.setattr(battery, "MEMORY_FLOOR", 2**80)
    monkeypatch.setattr(battery, "ensure_full_history", _must_not_run)
    monkeypatch.setattr(battery, "failing_ids", _must_not_run)

    assert battery.main(["compare"]) == 2
    out = capsys.readouterr().out
    assert "REFUSED" in out and "GiB" in out


def test_a_baseline_naming_no_place_was_measured_before_u273_and_is_refused(
    tmp_path, monkeypatch, capsys
):
    baseline = tmp_path / "baseline.txt"
    baseline.write_text(
        f"# commit abc123 host {socket.gethostname()} history full ids whole\n# 1 failed\n"
        "tests/a.py::t\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(battery, "BASELINE", baseline)
    monkeypatch.setattr(battery, "ensure_full_history", _must_not_run)
    monkeypatch.setattr(battery, "failing_ids", _must_not_run)

    assert battery.read_baseline() is None
    out = capsys.readouterr().out
    assert "U273" in out and "scripts/cloud_battery.py baseline" in out
    assert battery.cmd_compare(None) == 2


@pytest.mark.parametrize("place", ["tmpfs", "elsewhere"], ids=["a-filesystem", "unknown"])
def test_a_baseline_naming_a_place_that_is_not_one_is_refused(place, tmp_path, monkeypatch):
    _baseline_file(tmp_path, monkeypatch, place)
    assert battery.read_baseline() is None


def test_a_baseline_reads_back_its_place_and_its_tests_on_disk(tmp_path, monkeypatch):
    listed = ("tests/a.py::needs[a disk]", "tests/b.py::too")
    _baseline_file(tmp_path, monkeypatch, "memory", on_disk=listed)
    assert battery.read_baseline() == battery.Baseline(
        {"tests/a.py::t"}, "abc123", "memory", listed
    )


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
    assert battery.filesystem_of(Path("/dev/shm/x")) == "tmpfs"
    assert battery.filesystem_of(Path("/dev/shmother")) == "ext4"
    assert battery.filesystem_of(Path("/srv/with space/x")) == "tmpfs"
    assert battery.filesystem_of(Path("/srv/x")) == "ext4"
    assert battery.filesystem_of(Path("/data/x")) == "tmpfs", "the later mount covers the earlier"
    assert battery.filesystem_of(Path("/home/x")) == "ext4"
    monkeypatch.setattr(battery, "MOUNTS", tmp_path / "absent")
    assert battery.filesystem_of(Path("/dev/shm/x")) is None


def test_memory_is_a_place_only_on_a_memory_filesystem_with_room(places, monkeypatch):
    memory, _ = places
    assert battery.place_root("memory") == (memory, "")
    assert battery.default_place() == "memory"

    monkeypatch.setattr(battery, "MEMORY_FLOOR", 2**80)
    root, why = battery.place_root("memory")
    assert root is None and "GiB" in why
    assert battery.default_place() == "disk"

    monkeypatch.setattr(battery, "MEMORY_FLOOR", 0)
    monkeypatch.setattr(battery, "MEMORY_ROOT", memory.parent / "disk")
    root, why = battery.place_root("memory")
    assert root is None and "not a memory filesystem" in why
    assert battery.default_place() == "disk"


def test_disk_is_refused_when_the_temporary_directory_is_itself_in_memory(places, monkeypatch):
    memory, disk = places
    assert battery.place_root("disk") == (disk, "")
    monkeypatch.setattr(battery, "disk_root", lambda: memory)
    root, why = battery.place_root("disk")
    assert root is None and "memory filesystem" in why
    assert battery.place_root("elsewhere")[0] is None


def test_a_baseline_in_a_place_the_machine_cannot_give_is_refused(places, monkeypatch, capsys):
    monkeypatch.setattr(battery, "MEMORY_FLOOR", 2**80)
    monkeypatch.setattr(battery, "ensure_full_history", _must_not_run)
    monkeypatch.setattr(battery, "failing_ids", _must_not_run)
    assert battery.main(["baseline", "--temp", "memory"]) == 1
    assert "REFUSED" in capsys.readouterr().out


#: A scratch suite that writes where each test's temporary directory was, and
#: one test that passes only on disk, as the inode test does.
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
    memory, disk = places
    suite = tmp_path / "suite"
    (suite / "tests").mkdir(parents=True)
    (suite / "pytest.ini").write_text("[pytest]\naddopts = -q\n", encoding="utf-8")
    (suite / "tests" / "test_placed.py").write_text(PLACED_SUITE, encoding="utf-8")
    log = tmp_path / "placed.log"
    state = suite / ".cloud-battery"
    for name in stealing.INHERITED_RUN_STATE:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("PLACED_LOG", str(log))
    monkeypatch.setenv("PLACED_MEMORY", os.path.realpath(memory))
    monkeypatch.setattr(battery, "ROOT", suite)
    monkeypatch.setattr(battery, "STATE", state)
    monkeypatch.setattr(battery, "BASELINE", state / "baseline.txt")
    monkeypatch.setattr(battery, "VERDICT", state / "last-compare.txt")
    monkeypatch.setattr(battery, "PYTHON", Path(sys.executable))
    monkeypatch.setattr(battery, "ensure_full_history", lambda root=None: None)
    monkeypatch.setattr(battery, "static_checks", lambda: True)
    monkeypatch.setattr(battery, "head", lambda: "abc1234")
    monkeypatch.setattr(battery, "ON_DISK", (NEEDS_A_DISK,))
    return suite, log, memory


def _where(log: Path) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        name, where = line.split(" ", 1)
        seen.setdefault(name, []).append(where)
    return seen


def test_in_memory_the_whole_suite_runs_there_and_the_listed_tests_again_on_disk(placed):
    _suite, log, memory = placed
    disk = memory.parent / "disk"

    measured = battery.failing_ids("memory")

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
    # Each run's directory is removed when it ends, so nothing is left in memory.
    assert list(memory.iterdir()) == [] and list(disk.iterdir()) == []


def test_on_disk_the_suite_runs_once_and_never_in_memory(placed):
    _suite, log, memory = placed

    measured = battery.failing_ids("disk")

    assert measured.ids == set()
    assert measured.on_disk == ()
    seen = _where(log)
    assert len(seen["needs_a_disk"]) == 1
    assert not any(
        w.startswith(os.path.realpath(memory) + os.sep) for ws in seen.values() for w in ws
    )


def test_a_listed_test_failing_on_disk_is_recorded_failing(placed, monkeypatch):
    monkeypatch.setattr(battery, "ON_DISK", (NEEDS_A_DISK, FAILS_ON_DISK))
    monkeypatch.setenv("PLACED_DISK_FAILS", "1")

    measured = battery.failing_ids("memory")

    assert measured.ids == {FAILS_ON_DISK}
    assert "1 failed" in measured.on_disk_summary


def test_an_unlisted_test_failing_in_memory_stays_failing(placed, monkeypatch):
    """The disk run stands only for the tests it was asked to run."""
    monkeypatch.setattr(battery, "ON_DISK", ())
    measured = battery.failing_ids("memory")
    assert measured.ids == {NEEDS_A_DISK}
    assert measured.on_disk == ()


@pytest.mark.parametrize(
    "listed",
    ["tests/test_placed.py::test_skipped_on_disk", "tests/test_placed.py::test_not_there"],
    ids=["skipped-on-disk", "not-collected"],
)
def test_an_on_disk_run_that_did_not_run_a_listed_test_is_refused(listed, placed, monkeypatch):
    monkeypatch.setattr(battery, "ON_DISK", (NEEDS_A_DISK, listed))
    with pytest.raises(SystemExit, match="cannot"):
        battery.failing_ids("memory")


def test_a_baseline_header_names_its_place_and_lists_its_tests_on_disk(placed, capsys):
    suite, _log, _memory = placed
    assert battery.main(["baseline"]) == 0
    lines = (suite / ".cloud-battery" / "baseline.txt").read_text(encoding="utf-8").splitlines()
    assert lines[0] == (
        f"# commit abc1234 host {socket.gethostname()} temp memory history full ids whole"
    )
    assert f"# on disk test {NEEDS_A_DISK}" in lines
    assert any(line.startswith("# on disk summary 1 passed") for line in lines)
    assert "temporary files: memory, then 1 test(s) again on disk" in capsys.readouterr().out

    assert battery.main(["compare"]) == 0
    out = capsys.readouterr().out
    assert "NEWLY FAILING, yours: 0" in out

    assert battery.main(["baseline", "--temp", "disk"]) == 0
    lines = (suite / ".cloud-battery" / "baseline.txt").read_text(encoding="utf-8").splitlines()
    assert " temp disk " in lines[0]
    assert not any(line.startswith("# on disk") for line in lines)
