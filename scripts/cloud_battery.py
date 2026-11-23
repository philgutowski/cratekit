#!/usr/bin/env python3
"""The battery on a Linux cloud container, where part of the suite cannot pass.

About 170 tests fail on Linux for reasons bound to the machine, so the failures
on the base, measured on this machine, are the machine's, and anything failing
on the branch that did not fail on the base is the branch's. Nothing is skipped.

    .venv/bin/python scripts/cloud_battery.py baseline      # on the base commit
    .venv/bin/python scripts/cloud_battery.py compare       # on the branch

`compare` exits 1 when anything is newly failing, 2 when there is no baseline
for this machine, and 0 otherwise. Both verbs stop on a red ruff or scan, and
unshallow a shallow clone first (U200). Every failing id is read whole off a
reporting plugin (U268). Each run writes `.cloud-battery/verdict.json` for the
mutation driver (U271). Temporary files go in one named place, `disk` or
`memory` (U273), and in memory the `ON_DISK` tests run again on disk.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".cloud-battery"
BASELINE = STATE / "baseline.txt"
VERDICT = STATE / "last-compare.txt"
#: A test holds these equal to `scripts/mutate.py`'s `BATTERY_VERDICT` and its format.
RUN_RECORD_NAME = "verdict.json"
RUN_RECORD_FORMAT = 1
#: Every cloud container is called `vm`, so the boot id names the machine. Absent on macOS.
BOOT_ID = Path("/proc/sys/kernel/random/boot_id")
PYTHON = ROOT / ".venv" / "bin" / "python"
RUFF = ROOT / ".venv" / "bin" / "ruff"

#: Header fields: whole history (U200), whole ids (U268), the temporary files' place (U273).
FULL_HISTORY = "history full"
WHOLE_IDS = "ids whole"
TEMP_FIELD = "temp"
MEMORY = "memory"
DISK = "disk"
PLACES = (MEMORY, DISK)

#: A run writes about 2 GB, and filling a memory filesystem fails tests for want of space.
MEMORY_ROOT = Path("/dev/shm")
MEMORY_FILESYSTEMS = frozenset({"tmpfs", "ramfs"})
MEMORY_FLOOR = 6 * 2**30
MOUNTS = Path("/proc/self/mounts")

#: Run again on disk after a run in memory: a memory filesystem's inodes sit below its bound.
ON_DISK: tuple[str, ...] = (
    "tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random",
)

#: Disk by default (U273): a test newly read as the machine's is never traded for speed.
DEFAULT_PLACE = DISK

#: The command that measures a baseline again, named in every refusal of one.
REMEASURE = "`.venv/bin/python scripts/cloud_battery.py baseline` on origin/main"

PLUGIN_MODULE = "cratekit_cloud_battery_report"
REPORT_VARIABLE = "CLOUD_BATTERY_REPORT_PATH"

# Loaded with `-p`; on the xdist controller only, it writes the whole ids pytest's terminal
# filed as failed and error, the collected count, how many tests reported, and collect errors.
PLUGIN_SOURCE = '''
import json
import os

import pytest

_COLLECTED = {"count": None}
_RAN = set()


def pytest_collection_finish(session):
    if session.items:
        _COLLECTED["count"] = len(session.items)


@pytest.hookimpl(optionalhook=True)
def pytest_xdist_node_collection_finished(node, ids):
    _COLLECTED["count"] = len(ids)


def pytest_runtest_logreport(report):
    _RAN.add(report.nodeid)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    out = os.environ.get("CLOUD_BATTERY_REPORT_PATH")
    if hasattr(config, "workerinput") or not out:
        return
    passed = terminalreporter.stats.get("passed", [])
    found = {
        "collected": _COLLECTED["count"],
        "ran": len(_RAN),
        "collect_errors": [],
        "passed": {"ids": [getattr(report, "nodeid", None) for report in passed]},
    }
    for category in ("failed", "error"):
        reports = terminalreporter.stats.get(category, [])
        found[category] = {
            "ids": [getattr(report, "nodeid", None) for report in reports],
            "counted": sum(1 for one in reports if getattr(one, "count_towards_summary", True)),
        }
        found["collect_errors"] += [
            getattr(report, "nodeid", None)
            for report in reports
            if getattr(report, "when", None) == "collect"
        ]
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(found, handle)
'''


def run(cmd: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)


def _shallow(root: Path) -> str:
    """`true`, `false`, or why git could not say, which is never read as `false`."""
    done = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"], cwd=root, capture_output=True, text=True
    )
    answer = done.stdout.strip()
    if done.returncode == 0 and answer in ("true", "false"):
        return answer
    return f"git could not say whether the clone is shallow: {(done.stderr or answer).strip()}"


def ensure_full_history(root: Path | None = None) -> str | None:
    """Unshallow the clone at ``root`` from `origin main`; the reason it could not, or None."""
    root = ROOT if root is None else root
    state = _shallow(root)
    if state == "false":
        return None
    if state != "true":
        return state
    fetch = subprocess.run(
        ["git", "fetch", "--unshallow", "origin", "main"], cwd=root, capture_output=True, text=True
    )
    after = _shallow(root)
    if after == "false":
        print("history: the shallow clone was unshallowed from origin main")
        return None
    detail = (fetch.stderr or fetch.stdout).strip()[-1000:]
    return (
        "the clone is still shallow after `git fetch --unshallow origin main`, so a test "
        "that reads old history would fail for want of it and be subtracted unread; "
        f"fetch the full history and run this again. {detail}"
    ).strip()


def head() -> str:
    return run(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()


def static_checks() -> bool:
    """Ruff and the scan, which must be clean on every platform."""
    ok = True
    for name, cmd in (
        ("ruff", [str(RUFF), "check", "src", "tests", "scripts"]),
        ("scan", [str(PYTHON), str(ROOT / "scripts" / "scan_repo.py")]),
    ):
        result = run(cmd)
        if result.returncode != 0:
            ok = False
            print(f"{name}: RED")
            print((result.stdout + result.stderr).strip()[-3000:])
        else:
            print(f"{name}: clean")
    return ok


def suite_command() -> list[str]:
    """The suite run: the repository's own addopts, and the reporting plugin."""
    # No `-q`: addopts carry one, and `-qq` hides the summary line this reads.
    return [str(PYTHON), "-m", "pytest", "--tb=no", "-p", PLUGIN_MODULE, "-p", "no:cacheprovider"]


def _unescape_mount(field: str) -> str:
    """A mount table path, whose spaces and the like are written as octal escapes."""
    return re.sub(r"\\([0-7]{3})", lambda m: chr(int(m.group(1), 8)), field)


def filesystem_of(path: Path) -> str | None:
    """The type of the filesystem holding ``path``: the longest, then latest, mount point."""
    try:
        lines = MOUNTS.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    target = os.path.realpath(path)
    best, kind = "", None
    for line in lines:
        fields = line.split()
        if len(fields) < 3:
            continue
        point = _unescape_mount(fields[1])
        inside = point == "/" or target == point or target.startswith(point.rstrip("/") + "/")
        if inside and len(point) >= len(best):
            best, kind = point, fields[2]
    return kind


def disk_root() -> Path:
    """Where a run on disk makes its directory: the temporary directory this process was given."""
    return Path(tempfile.gettempdir())


def place_root(place: str) -> tuple[Path | None, str]:
    """The directory a run in ``place`` makes its own in, or None and why it cannot."""
    if place == MEMORY:
        root = MEMORY_ROOT
        kind = filesystem_of(root)
        if kind not in MEMORY_FILESYSTEMS:
            return None, f"{root} is not a memory filesystem here ({kind or 'no mount table'})"
        if not os.access(root, os.W_OK):
            return None, f"{root} cannot be written"
        stats = os.statvfs(root)
        free = stats.f_bavail * stats.f_frsize
        if free < MEMORY_FLOOR:
            return None, (
                f"{root} has {free / 2**30:.1f} GiB free, under the "
                f"{MEMORY_FLOOR / 2**30:.0f} GiB a run needs, and a run that fills it fails "
                f"tests for want of space"
            )
        return root, ""
    if place == DISK:
        root = disk_root()
        kind = filesystem_of(root)
        if kind in MEMORY_FILESYSTEMS:
            return None, (
                f"the temporary directory {root} is on a memory filesystem ({kind}), so a run "
                f"there is not on disk; point TMPDIR at a directory on disk"
            )
        return root, ""
    return None, f"{place!r} is not a place for temporary files; name one of {', '.join(PLACES)}"


def places_needed(place: str) -> tuple[str, ...]:
    """The places a run in ``place`` uses: memory runs the listed tests on disk too."""
    return (MEMORY, DISK) if place == MEMORY and ON_DISK else (place,)


def refusal_for(place: str) -> str | None:
    """Why this machine cannot give a run in ``place`` every place it uses, or None."""
    for needed in places_needed(place):
        root, why = place_root(needed)
        if root is None:
            return why if needed == place else f"the tests run again on disk cannot be: {why}"
    return None


@contextmanager
def run_directory(place: str | None) -> Iterator[tuple[Path, Path | None]]:
    """A fresh workspace in ``place`` (None: inherited, no ``TMPDIR``) and its temporary dir."""
    if place is None:
        with tempfile.TemporaryDirectory(prefix="cloud-battery-") as tmp:
            yield Path(tmp), None
        return
    root, why = place_root(place)
    if root is None:
        raise SystemExit(f"temporary files: REFUSED, {why}")
    with tempfile.TemporaryDirectory(prefix="cloud-battery-", dir=root) as tmp:
        workspace = Path(tmp)
        temp = workspace / "tmp"
        temp.mkdir()
        yield workspace, temp


def _run_suite(place: str | None, extra: tuple[str, ...] = ()) -> tuple[dict, str, int]:
    """One suite run in ``place``: its report, its summary line and pytest's exit code."""
    with run_directory(place) as (workspace, temp):
        (workspace / f"{PLUGIN_MODULE}.py").write_text(PLUGIN_SOURCE, encoding="utf-8")
        report_path = workspace / "report.json"
        env = os.environ.copy()
        env[REPORT_VARIABLE] = str(report_path)
        if temp is not None:
            env["TMPDIR"] = str(temp)
        env["PYTHONPATH"] = os.pathsep.join([str(workspace), env.get("PYTHONPATH", "")]).rstrip(
            os.pathsep
        )
        result = run(suite_command() + list(extra), env=env)
        summary = ""
        for line in result.stdout.splitlines():
            if " passed" in line or " failed" in line or " error" in line:
                summary = line.strip()
        if not summary:
            print(result.stdout[-3000:])
            print(result.stderr[-3000:])
            raise SystemExit("pytest printed no summary line, so the run cannot be read")
        if not report_path.is_file():
            print(result.stdout[-3000:])
            print(result.stderr[-3000:])
            raise SystemExit(
                "pytest wrote no report of its failing tests, so the run cannot be read"
            )
        report = json.loads(report_path.read_text(encoding="utf-8"))
    return report, summary, result.returncode


@dataclass(frozen=True)
class SuiteRun:
    """What one run measured; None where it did not say. ``ids`` hold the on disk outcomes."""

    ids: frozenset[str]
    summary: str
    collected: int | None
    collect_errors: frozenset[str] | None
    exit_code: int
    ran: int | None = None
    place: str | None = None
    on_disk: tuple[str, ...] = ()
    on_disk_summary: str = ""


def failing_ids() -> tuple[set[str], str]:
    """Run the suite and return the failing and erroring ids with the summary line."""
    suite = measure_suite()
    return set(suite.ids), suite.summary


def measure_suite(place: str | None = None) -> SuiteRun:
    """Run the suite in ``place``; in memory, the ``ON_DISK`` tests' outcome comes from disk."""
    report, summary, exit_code = _run_suite(place)
    ids = read_report(report, summary)
    collect_errors = _read_collect_errors(report, ids)
    listed = tuple(ON_DISK) if place == MEMORY else ()
    on_disk_summary = ""
    if listed:
        ids, on_disk_summary = _rerun_on_disk(ids, listed)
    return SuiteRun(
        frozenset(ids), summary, _read_count(report, "collected"), collect_errors, exit_code,
        _read_count(report, "ran"), place, listed, on_disk_summary,
    )


def _ran(report: dict) -> set[str]:
    ran: set[str] = set()
    for category in ("passed", "failed", "error"):
        entry = report.get(category)
        listed = entry.get("ids") if isinstance(entry, dict) else None
        if not isinstance(listed, list):
            raise SystemExit(
                f"the on disk run's report has no list of {category} tests, so whether each "
                f"listed test ran there cannot be read: {entry!r}"
            )
        ran.update(listed)
    return ran


def _rerun_on_disk(ids: set[str], listed: tuple[str, ...]) -> tuple[set[str], str]:
    """The ids with the listed tests' outcome from a run on disk that ran exactly those."""
    disk_report, disk_summary, _ = _run_suite(DISK, listed)
    disk_ids = read_report(disk_report, disk_summary)
    ran = _ran(disk_report)
    unread = {
        one
        for one in set(listed) - ran
        if not any(one.startswith(f"{path}::") for path in disk_ids)
    }
    stray = ran - set(listed) - {path for path in disk_ids if "::" not in path}
    if unread or stray:
        raise SystemExit(
            f"the on disk run ({disk_summary}) did not run exactly the tests listed to run "
            f"on disk, so it cannot stand for them: not run {sorted(unread)}, "
            f"run unlisted {sorted(stray)}"
        )
    return (ids - set(listed)) | disk_ids, disk_summary


def _read_count(report: dict, key: str) -> int | None:
    """One of the report's counts, or None when it holds no count it could have read."""
    count = report.get(key)
    return count if isinstance(count, int) and not isinstance(count, bool) and count >= 0 else None


def _read_collect_errors(report: dict, ids: set[str]) -> frozenset[str] | None:
    """The collection errors, or None (unknown) unless each is one of the ids read whole."""
    listed = report.get("collect_errors")
    if isinstance(listed, list) and all(isinstance(one, str) and one in ids for one in listed):
        return frozenset(listed)
    return None


def _summary_count(summary: str, pattern: str) -> int:
    match = re.search(rf"\b(\d+) {pattern}\b", summary)
    return int(match.group(1)) if match else 0


def read_report(report: dict, summary: str) -> set[str]:
    """The whole ids of a run's report, refused unless it agrees with the summary line."""
    expected = {
        "failed": _summary_count(summary, "failed"),
        "error": _summary_count(summary, "errors?"),
    }
    ids: set[str] = set()
    for category, count in expected.items():
        entry = report.get(category)
        if not isinstance(entry, dict) or entry.get("counted") != count:
            raise SystemExit(
                f"the run's report of {category} tests does not agree with pytest's summary "
                f"line ({summary}), so the run cannot be read: {entry!r}"
            )
        listed = entry.get("ids")
        if not isinstance(listed, list) or len(listed) < count:
            raise SystemExit(
                f"the run's report lists fewer {category} tests than pytest's summary line "
                f"({summary}) counts, so the run cannot be read: {entry!r}"
            )
        for nodeid in listed:
            if (
                not isinstance(nodeid, str)
                or not nodeid
                or nodeid != nodeid.strip()
                or nodeid.startswith("#")
                or nodeid.splitlines() != [nodeid]
            ):
                raise SystemExit(
                    f"a {category} test's id cannot be stored whole, one a line, so the run "
                    f"cannot be read: {nodeid!r}"
                )
            ids.add(nodeid)
    return ids


def _checked_run(place: str) -> tuple[str, SuiteRun, TreeState] | None:
    """History, ruff and the scan, then the suite in ``place``; None when one refused."""
    if (reason := ensure_full_history()) is not None:
        print(f"history: REFUSED, {reason}")
        return None
    if not static_checks():
        return None
    at = head()
    before = tree_state()
    measured = measure_suite(place)
    return at, measured, measured_tree(before, tree_state())


def cmd_baseline(args) -> int:
    place = getattr(args, "temp", None) or DEFAULT_PLACE
    why = refusal_for(place)
    if why is not None:
        print(f"temporary files: REFUSED, {why}")
        return 1
    if (done := _checked_run(place)) is None:
        return 1
    at, measured, tree = done
    STATE.mkdir(exist_ok=True)
    lines = [
        f"# commit {at} host {socket.gethostname()} {TEMP_FIELD} {place} "
        f"{FULL_HISTORY} {WHOLE_IDS}",
        f"# {measured.summary}",
        *(f"# on disk test {one}" for one in measured.on_disk),
    ]
    if measured.on_disk:
        lines.append(f"# on disk summary {measured.on_disk_summary}")
    BASELINE.write_text(
        "".join(f"{line}\n" for line in lines) + "".join(f"{i}\n" for i in sorted(measured.ids)),
        encoding="utf-8",
    )
    # Clean by construction against the file just written; the release reads compare's only.
    record_run("baseline", "clean", measured, tree, file_digest(BASELINE))
    print(f"baseline at {at}: {measured.summary}")
    print(_place_line(measured))
    print(f"{len(measured.ids)} machine bound failure(s) recorded in {BASELINE.relative_to(ROOT)}")
    return 0


def _place_line(measured: SuiteRun) -> str:
    line = f"temporary files: {measured.place}"
    if measured.on_disk:
        line += (
            f", then {len(measured.on_disk)} test(s) again on disk, whose outcome there "
            f"stands: {measured.on_disk_summary}"
        )
    return line


@dataclass(frozen=True)
class Baseline:
    ids: set[str]
    commit: str
    place: str
    on_disk: tuple[str, ...]


ON_DISK_PREFIX = "# on disk test "


def read_baseline() -> Baseline | None:
    if not BASELINE.exists():
        return None
    lines = BASELINE.read_text(encoding="utf-8").splitlines()
    header = lines[0] if lines else ""
    match = re.match(
        rf"# commit (\S+) host (\S+)(?: {TEMP_FIELD} (\S+))?(?: (history \S+))?(?: (ids \S+))?$",
        header,
    )
    if not match:
        return None
    if match.group(2) != socket.gethostname():
        print(f"the baseline was measured on {match.group(2)}, not this machine; measure it again")
        return None
    if match.group(4) != FULL_HISTORY:
        print(
            "the baseline does not say it was measured with full history, so a test a "
            "shallow clone held red may be in it; measure it again"
        )
        return None
    if match.group(5) != WHOLE_IDS:
        print(
            "the baseline does not say its ids are whole: it was measured before U268, "
            "which kept each failing id only up to its first space, so a new failure "
            "sharing that prefix would read as the machine's; measure it again with "
            f"{REMEASURE}"
        )
        return None
    if match.group(3) not in PLACES:
        print(
            "the baseline does not say where its temporary files were: it was measured "
            "before U273, and a run in memory is never read against one whose place is "
            f"unknown; measure it again with {REMEASURE}"
        )
        return None
    ids = {line for line in lines if line and not line.startswith("#")}
    on_disk = tuple(ln.removeprefix(ON_DISK_PREFIX) for ln in lines if ln.startswith(ON_DISK_PREFIX))
    return Baseline(ids, match.group(1), match.group(3), on_disk)


def cmd_compare(args) -> int:
    base = read_baseline()
    if base is None:
        print("no baseline for this machine: run `cloud_battery.py baseline` on origin/main first")
        return 2
    requested = getattr(args, "temp", None)
    if requested is not None and requested != base.place:
        print(
            f"temporary files: REFUSED, the baseline kept its temporary files in {base.place} "
            f"and this compare asks for {requested}, and a run one way is never read against "
            f"a baseline measured the other; compare with `--temp {base.place}`, or measure "
            f"the baseline again with `--temp {requested}`"
        )
        return 2
    why = refusal_for(base.place)
    if why is not None:
        print(
            f"temporary files: REFUSED, the baseline kept its temporary files in {base.place} "
            f"and this machine cannot now: {why}"
        )
        return 2
    known_digest = file_digest(BASELINE)
    if (done := _checked_run(base.place)) is None:
        return 1
    at, measured, tree = done
    ids = measured.ids
    still = sorted(ids & base.ids)
    new = sorted(ids - base.ids)
    gone = sorted(base.ids - ids)
    print(f"branch at {at}: {measured.summary}")
    print(f"baseline at {base.commit}: {len(base.ids)} failing")
    print(_place_line(measured))
    if measured.on_disk != base.on_disk:
        print(
            f"the tests run on disk differ from the baseline's: now {list(measured.on_disk)}, "
            f"then {list(base.on_disk)}"
        )
    print()
    print(f"still failing, the machine's: {len(still)}")
    for heading, listed in (("no longer failing", gone), ("NEWLY FAILING, yours", new)):
        print(f"{heading}: {len(listed)}")
        for i in listed:
            print(f"  {i}")
    verdict = "red" if new else "clean"
    record_verdict(verdict, tree)
    record_run("compare", verdict, measured, tree, known_digest)
    return 1 if new else 0


@dataclass(frozen=True)
class TreeState:
    """HEAD's full sha and whether nothing differs from it; empty and False when git cannot say."""

    commit: str
    clean: bool


def tree_state() -> TreeState:
    """Read HEAD and the status of the checkout, untracked files included."""
    sha = run(["git", "rev-parse", "HEAD"])
    commit = sha.stdout.strip() if sha.returncode == 0 else ""
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        commit = ""
    # Untracked files listed whatever `status.showUntrackedFiles` says.
    status = run(["git", "status", "--porcelain", "--untracked-files=all"])
    clean = bool(commit) and status.returncode == 0 and not status.stdout.strip()
    return TreeState(commit=commit, clean=clean)


def measured_tree(before: TreeState, after: TreeState) -> TreeState:
    """The tree a run measured: the commit read before it, clean only if nothing moved."""
    clean = before.clean and after.clean and before.commit == after.commit
    return TreeState(commit=before.commit, clean=clean)


def file_digest(path: Path) -> str:
    """The sha256 of a file's bytes, or empty when it cannot be read."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def boot_id() -> str:
    """This boot's id, or empty where the kernel keeps none (macOS)."""
    try:
        return BOOT_ID.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def record_verdict(verdict: str, tree: TreeState) -> None:
    """Write the full sha read before the run and the verdict, or `dirty`, for `release.py cut`."""
    if not tree.clean:
        verdict = "dirty"
    STATE.mkdir(exist_ok=True)
    VERDICT.write_text(f"{tree.commit} {verdict}\n")


def record_run(
    source: str, verdict: str, suite: SuiteRun, tree: TreeState, known_digest: str
) -> None:
    """Write the run record `scripts/mutate.py` may read in place of its baseline, atomically."""
    record = {
        "format": RUN_RECORD_FORMAT,
        "source": source,
        "commit": tree.commit,
        "clean_tree": tree.clean,
        "host": socket.gethostname(),
        "boot_id": boot_id(),
        "root": str(ROOT),
        "python": str(PYTHON),
        "known_failures_sha256": known_digest,
        "verdict": verdict,
        "summary": suite.summary,
        "collected": suite.collected,
        "ran": suite.ran,
        "exit_code": suite.exit_code,
        # A value here edits the run, and the driver reads no record of an edited run.
        "pytest_addopts": os.environ.get("PYTEST_ADDOPTS", ""),
        "failing": sorted(suite.ids),
        "collect_errors": None if suite.collect_errors is None else sorted(suite.collect_errors),
        "when": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }
    STATE.mkdir(exist_ok=True)
    partial = STATE / f".{RUN_RECORD_NAME}.partial"
    partial.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    os.replace(partial, STATE / RUN_RECORD_NAME)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    baseline = sub.add_parser("baseline", help="measure the machine's failures on this commit")
    baseline.add_argument(
        "--temp",
        choices=PLACES,
        default=None,
        help="where the run keeps its temporary files; disk unless memory is named, and "
        "memory only on a memory filesystem with room for a run",
    )
    baseline.set_defaults(func=cmd_baseline)
    compare = sub.add_parser("compare", help="run the suite and diff it against the baseline")
    compare.add_argument(
        "--temp",
        choices=PLACES,
        default=None,
        help="where the run keeps its temporary files; the baseline's place, and refused "
        "when it names the other",
    )
    compare.set_defaults(func=cmd_compare)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
