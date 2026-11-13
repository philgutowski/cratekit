#!/usr/bin/env python3
"""The battery on a Linux cloud container, where part of the suite cannot pass.

The suite is a macOS proof. On Linux about 170 tests fail or error for reasons
bound to the machine: `hdiutil` volumes, the timing calibration pinned to the
Mac that wrote it, darwin paths, APFS normalisation. METHOD says the battery is
the merge gate and CI does not run the suite for exactly this reason, so a cloud
session cannot read "red" as "mine" and cannot read it as "not mine" either.

This makes the comparison the earlier cloud builder made by hand, once per
failing id: the failures on the base, measured on this same machine, are the
machine's; anything failing on the branch that did not fail on the base is the
branch's. Nothing is skipped, deselected or marked, so a test the branch fixes
shows up as gone and a test it breaks shows up as new.

    .venv/bin/python scripts/cloud_battery.py baseline      # on the base commit
    .venv/bin/python scripts/cloud_battery.py compare       # on the branch

`baseline` runs the suite on the checked out tree and writes the failing ids to
`.cloud-battery/baseline.txt` with the commit it measured, so a session runs it
once, on `origin/main`, before it branches. `compare` runs the suite again and
prints three lists: still failing (the machine's), newly failing (yours), and
no longer failing (the branch fixed them, or the test went away). It exits 1
when anything is newly failing, 2 when there is no baseline to compare against,
and 0 otherwise. Both run ruff and the scan first, and stop if either is red,
since those two must be clean on any platform.

The state directory is gitignored. A baseline measured on another machine is
not a baseline, so the file names its commit and the hostname it was measured
on and `compare` refuses one from elsewhere.

Both verbs read the clone's full history first (U200, from R-1191). A cloud
clone is shallow, so a test that reads an old commit fails on the base for
want of it, and a failure subtracted by node id hides every later failure of
that test, whatever its cause: that is how U195's defect reached `main`. So a
shallow clone is unshallowed from `origin main` before anything is measured,
and refused when the fetch cannot complete it. The baseline's header says
`history full`, and `compare`, like `scripts/mutate.py --known-failures`,
refuses a baseline that does not say so.

Every failing id is read whole (U268). The ids used to be cut out of pytest's
`-rfE` summary lines up to their first space, and 1,829 of the suite's ids hold
one, so two parametrized tests whose ids differ only after a space were one
entry: one failing on the base for the machine's reason excused the other
failing on the branch for the branch's. The suite run now loads a small
reporting plugin that writes, at the end of the run, the node id of every
report pytest's own terminal filed as failed or as an error, the very reports
those summary lines were printed from. The run is refused when the plugin
wrote nothing or its counts disagree with pytest's summary line. The header's
last field is `ids whole`, and `compare` and the driver refuse a baseline
without it, which is every baseline measured before U268.

Each run leaves a record the mutation driver may read in place of its own full
baseline (U271, Phillip's answer of 2026-11-13): `.cloud-battery/verdict.json`,
written by `compare` and by `baseline`. It names the commit the run measured,
read before the run, and whether the tree was clean throughout, read by
`git status --porcelain` before and after it, with HEAD unmoved; the host and
the kernel's boot id, since every cloud container is called `vm`; the checkout
and the interpreter; the sha256 of the known failures file the run was read
against; any `PYTEST_ADDOPTS` the run inherited; the verdict; and what the run
measured: the collected count, how many of those tests ran, pytest's exit
code, the failing ids and the collection errors. `scripts/mutate.py` reads
it only when every one of those keys is its own, and measures otherwise.
`last-compare.txt`, the line `release.py cut` reads, takes its commit from
before the run too and says `dirty` when the tree moved during it.
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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".cloud-battery"
BASELINE = STATE / "baseline.txt"
VERDICT = STATE / "last-compare.txt"
#: The run record's file name, inside ``STATE``, and the format the mutation
#: driver reads (U271). The name and the format are repeated in
#: ``scripts/mutate.py`` as ``BATTERY_VERDICT`` and ``BATTERY_VERDICT_FORMAT``,
#: and a test holds the two scripts to the same values.
RUN_RECORD_NAME = "verdict.json"
RUN_RECORD_FORMAT = 1
#: Linux's id for this boot of the kernel. Every cloud container is called
#: `vm`, so the host name alone names no machine; the boot id does, and it is
#: the same key `scripts/mutate.py` reads. Absent on macOS, where both read it
#: as empty.
BOOT_ID = Path("/proc/sys/kernel/random/boot_id")
PYTHON = ROOT / ".venv" / "bin" / "python"
RUFF = ROOT / ".venv" / "bin" / "ruff"

#: The header field saying the clone's whole history was present (U200).
FULL_HISTORY = "history full"
#: The header's last field, saying every id was stored whole (U268). `compare`
#: and the mutation driver require both.
WHOLE_IDS = "ids whole"

#: The command that measures a baseline again, named in every refusal of one.
REMEASURE = "`.venv/bin/python scripts/cloud_battery.py baseline` on origin/main"

#: The reporting plugin's module name and the variable naming its output file.
PLUGIN_MODULE = "cratekit_cloud_battery_report"
REPORT_VARIABLE = "CLOUD_BATTERY_REPORT_PATH"

# Loaded into the suite run with `-p`. It reads the reports pytest's terminal
# filed under `failed` and `error`, which are what the `-rfE` summary lines and
# the counts on the summary line are printed from, so it recognises exactly the
# failures those lines named, each by its whole `nodeid`. It writes on the xdist
# controller only, which receives every worker's reports; a worker has
# `workerinput` and writes nothing.
#
# It also writes the collected count, how many of those tests reported at all,
# and which errors were collection errors (U271), which the mutation driver
# reads from the run record: a run that stopped early, `-x` say, exits 1 like a
# complete red one, and only the count of tests that ran tells the two apart. The count is
# read as the driver's own plugin reads it: off the hook xdist fires on the
# controller when a worker finishes collecting, since the controller collects
# nothing itself, and off the session's items in a run without workers.
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
    if hasattr(config, "workerinput"):
        return
    out = os.environ.get("CLOUD_BATTERY_REPORT_PATH")
    if not out:
        return
    found = {"collected": _COLLECTED["count"], "ran": len(_RAN), "collect_errors": []}
    for category in ("failed", "error"):
        reports = terminalreporter.stats.get(category, [])
        found[category] = {
            "ids": [getattr(report, "nodeid", None) for report in reports],
            "counted": sum(
                1 for report in reports if getattr(report, "count_towards_summary", True)
            ),
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
    """Unshallow the clone at ``root`` from `origin main`; the reason it could not, or None.

    A complete clone runs no fetch. A shallow one fetches the rest of `main`'s
    history, then is read again, since a fetch can succeed and leave another
    shallow root behind.
    """
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


def full_history_or_refuse() -> bool:
    reason = ensure_full_history()
    if reason is None:
        return True
    print(f"history: REFUSED, {reason}")
    return False


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
    # No `-q` here: pyproject's addopts already carry one, and a second makes
    # `-qq`, which hides the summary line this reads. The mutation driver's
    # docstring records the same trap, met the same way.
    return [
        str(PYTHON),
        "-m",
        "pytest",
        "--tb=no",
        "-p",
        PLUGIN_MODULE,
        "-p",
        "no:cacheprovider",
    ]


@dataclass(frozen=True)
class SuiteRun:
    """What one run of the suite measured.

    ``collected``, ``ran`` and ``collect_errors`` are None when the run did
    not say; ``ran`` counts the tests that reported at all, every one of the
    collected in a run that was not stopped early,
    and ``exit_code`` is
    pytest's own, so a reader can tell a complete run (0 or 1) from an
    interrupted one.
    """

    ids: frozenset[str]
    summary: str
    collected: int | None
    collect_errors: frozenset[str] | None
    exit_code: int
    ran: int | None = None


def failing_ids() -> tuple[set[str], str]:
    """Run the suite and return the failing and erroring ids with the summary line."""
    suite = measure_suite()
    return set(suite.ids), suite.summary


def measure_suite() -> SuiteRun:
    """Run the suite and read every failing id whole, with what else the run measured."""
    with tempfile.TemporaryDirectory(prefix="cloud-battery-") as tmp:
        workspace = Path(tmp)
        (workspace / f"{PLUGIN_MODULE}.py").write_text(PLUGIN_SOURCE, encoding="utf-8")
        report_path = workspace / "report.json"
        # Inherit, then add: the suite reads the caller's environment, and a
        # fresh one would measure a different run.
        env = os.environ.copy()
        env[REPORT_VARIABLE] = str(report_path)
        env["PYTHONPATH"] = os.pathsep.join([str(workspace), env.get("PYTHONPATH", "")]).rstrip(
            os.pathsep
        )
        result = run(suite_command(), env=env)
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
    ids = read_report(report, summary)
    return SuiteRun(
        ids=frozenset(ids),
        summary=summary,
        collected=_read_count(report, "collected"),
        collect_errors=_read_collect_errors(report, ids),
        exit_code=result.returncode,
        ran=_read_count(report, "ran"),
    )


def _read_count(report: dict, key: str) -> int | None:
    """One of the report's counts, or None when it holds no count it could have read."""
    count = report.get(key)
    if isinstance(count, int) and not isinstance(count, bool) and count >= 0:
        return count
    return None


def _read_collect_errors(report: dict, ids: set[str]) -> frozenset[str] | None:
    """The collection errors, or None when the report does not say which they were.

    Each must be one of the ids already read whole. A report that lists none of
    its own, or one it does not list as failing or erroring, is not read: the
    run itself is still read for `compare`, and the record says the collection
    errors are unknown, which the mutation driver refuses to stand for its
    baseline.
    """
    listed = report.get("collect_errors")
    if not isinstance(listed, list) or not all(
        isinstance(nodeid, str) and nodeid in ids for nodeid in listed
    ):
        return None
    return frozenset(listed)


def _summary_count(summary: str, pattern: str) -> int:
    match = re.search(rf"\b(\d+) {pattern}\b", summary)
    return int(match.group(1)) if match else 0


def read_report(report: dict, summary: str) -> set[str]:
    """The whole ids of a run's report, refused unless it agrees with the summary line.

    Each id must survive a baseline file unchanged, one a line and compared
    exactly, so an id that is empty, holds anything `str.splitlines` breaks a
    line at, starts with `#` or is padded with spaces is refused rather than
    stored altered.
    """
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


def cmd_baseline(_args) -> int:
    if not full_history_or_refuse():
        return 1
    if not static_checks():
        return 1
    at = head()
    before = tree_state()
    suite = measure_suite()
    tree = measured_tree(before, tree_state())
    ids, summary = suite.ids, suite.summary
    STATE.mkdir(exist_ok=True)
    BASELINE.write_text(
        f"# commit {at} host {socket.gethostname()} {FULL_HISTORY} {WHOLE_IDS}\n"
        f"# {summary}\n" + "".join(f"{i}\n" for i in sorted(ids)),
        encoding="utf-8",
    )
    # Its own failures are the known ones by construction, so the verdict is
    # clean against the file just written; the release reads compare's only.
    record_run("baseline", "clean", suite, tree, file_digest(BASELINE))
    print(f"baseline at {at}: {summary}")
    print(f"{len(ids)} machine bound failure(s) recorded in {BASELINE.relative_to(ROOT)}")
    return 0


def read_baseline() -> tuple[set[str], str] | None:
    if not BASELINE.exists():
        return None
    lines = BASELINE.read_text(encoding="utf-8").splitlines()
    header = lines[0] if lines else ""
    match = re.match(r"# commit (\S+) host (\S+)(?: (history \S+))?(?: (ids \S+))?$", header)
    if not match:
        return None
    if match.group(2) != socket.gethostname():
        print(f"the baseline was measured on {match.group(2)}, not this machine; measure it again")
        return None
    if match.group(3) != FULL_HISTORY:
        print(
            "the baseline does not say it was measured with full history, so a test a "
            "shallow clone held red may be in it; measure it again"
        )
        return None
    if match.group(4) != WHOLE_IDS:
        print(
            "the baseline does not say its ids are whole: it was measured before U268, "
            "which kept each failing id only up to its first space, so a new failure "
            "sharing that prefix would read as the machine's; measure it again with "
            f"{REMEASURE}"
        )
        return None
    ids = {line for line in lines if line and not line.startswith("#")}
    return ids, match.group(1)


def cmd_compare(_args) -> int:
    base = read_baseline()
    if base is None:
        print("no baseline for this machine: run `cloud_battery.py baseline` on origin/main first")
        return 2
    base_ids, base_commit = base
    # Read beside the ids it holds, so the record names the file they came from.
    known_digest = file_digest(BASELINE)
    if not full_history_or_refuse():
        return 1
    if not static_checks():
        return 1
    at = head()
    before = tree_state()
    suite = measure_suite()
    tree = measured_tree(before, tree_state())
    ids, summary = suite.ids, suite.summary
    still = sorted(ids & base_ids)
    new = sorted(ids - base_ids)
    gone = sorted(base_ids - ids)
    print(f"branch at {at}: {summary}")
    print(f"baseline at {base_commit}: {len(base_ids)} failing")
    print()
    print(f"still failing, the machine's: {len(still)}")
    print(f"no longer failing: {len(gone)}")
    for i in gone:
        print(f"  {i}")
    print(f"NEWLY FAILING, yours: {len(new)}")
    for i in new:
        print(f"  {i}")
    verdict = "red" if new else "clean"
    record_verdict(verdict, tree)
    record_run("compare", verdict, suite, tree, known_digest)
    return 1 if new else 0


@dataclass(frozen=True)
class TreeState:
    """The checkout as git reads it: HEAD's full sha, and whether nothing differs from it.

    ``commit`` is empty and ``clean`` is False whenever git could not say,
    because no answer is not an empty status.
    """

    commit: str
    clean: bool


def tree_state() -> TreeState:
    """Read HEAD and the status of the checkout, untracked files included."""
    sha = run(["git", "rev-parse", "HEAD"])
    commit = sha.stdout.strip() if sha.returncode == 0 else ""
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        commit = ""
    # Untracked files listed whatever the checkout's own git config says, since
    # `status.showUntrackedFiles=no` would otherwise hide a test file nobody
    # committed from both this reading and the driver's.
    status = run(["git", "status", "--porcelain", "--untracked-files=all"])
    clean = bool(commit) and status.returncode == 0 and not status.stdout.strip()
    return TreeState(commit=commit, clean=clean)


def measured_tree(before: TreeState, after: TreeState) -> TreeState:
    """The tree a run measured: the commit read before it, clean only if nothing moved.

    A commit made while the suite ran is not what the suite measured, and a
    file changed and put back while it ran may have been read changed, so a
    change seen at either end, or a HEAD that moved, makes the run unclean.
    """
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
    """Write the verdict for the commit just measured, for `release.py cut` (U159).

    The full sha, so a release refuses a verdict from any other commit, and
    `dirty` in place of the verdict when the tree was not clean throughout the
    run, since then the run measured something no commit holds. The sha is the
    one read before the run (U271): read after it, a commit made while the
    suite ran was named as the commit it measured.
    """
    if not tree.clean:
        verdict = "dirty"
    STATE.mkdir(exist_ok=True)
    VERDICT.write_text(f"{tree.commit} {verdict}\n")


def record_run(
    source: str, verdict: str, suite: SuiteRun, tree: TreeState, known_digest: str
) -> None:
    """Write the run record `scripts/mutate.py` may read in place of its full baseline (U271).

    Written at the end of every run that reached its reading, a dirty or
    interrupted one included, and the driver reads the keys and refuses the
    record unless each is its own. A run stopped before that, by a red ruff or
    scan or a report it could not read, leaves the previous record in place,
    which still names the commit and the tree it measured. Written to a
    temporary file and moved into place, so a reader never meets half of one.
    """
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
        # The suite inherits the caller's environment, and a value here edits
        # the run (a deselection, `-x`); the driver scrubs it from its own runs
        # and reads no record of a run it edited.
        "pytest_addopts": os.environ.get("PYTEST_ADDOPTS", ""),
        "failing": sorted(suite.ids),
        "collect_errors": None if suite.collect_errors is None else sorted(suite.collect_errors),
        "when": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }
    STATE.mkdir(exist_ok=True)
    target = STATE / RUN_RECORD_NAME
    partial = STATE / f".{RUN_RECORD_NAME}.partial"
    partial.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    os.replace(partial, target)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("baseline", help="measure the machine's failures on this commit").set_defaults(
        func=cmd_baseline
    )
    sub.add_parser("compare", help="run the suite and diff it against the baseline").set_defaults(
        func=cmd_compare
    )
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
