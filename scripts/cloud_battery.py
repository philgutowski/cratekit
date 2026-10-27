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
"""

from __future__ import annotations

import argparse
import re
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / ".cloud-battery"
BASELINE = STATE / "baseline.txt"
PYTHON = ROOT / ".venv" / "bin" / "python"
RUFF = ROOT / ".venv" / "bin" / "ruff"

# pytest's short summary lines, `-rfE`: "FAILED path::id - reason" and
# "ERROR path::id - reason". The id is everything before the first " - ".
SUMMARY_RE = re.compile(r"^(?:FAILED|ERROR) (\S+)")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


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


def failing_ids() -> tuple[set[str], str]:
    """Run the suite and return the failing and erroring ids with the summary line."""
    result = run(
        [str(PYTHON), "-m", "pytest", "-q", "--tb=no", "-rfE", "-p", "no:cacheprovider"]
    )
    ids = set()
    summary = ""
    for line in result.stdout.splitlines():
        match = SUMMARY_RE.match(line)
        if match:
            ids.add(match.group(1))
        if " passed" in line or " failed" in line or " error" in line:
            summary = line.strip()
    if not summary:
        print(result.stdout[-3000:])
        print(result.stderr[-3000:])
        raise SystemExit("pytest printed no summary line, so the run cannot be read")
    return ids, summary


def cmd_baseline(_args) -> int:
    if not static_checks():
        return 1
    ids, summary = failing_ids()
    STATE.mkdir(exist_ok=True)
    BASELINE.write_text(
        f"# commit {head()} host {socket.gethostname()}\n# {summary}\n"
        + "".join(f"{i}\n" for i in sorted(ids))
    )
    print(f"baseline at {head()}: {summary}")
    print(f"{len(ids)} machine bound failure(s) recorded in {BASELINE.relative_to(ROOT)}")
    return 0


def read_baseline() -> tuple[set[str], str] | None:
    if not BASELINE.exists():
        return None
    lines = BASELINE.read_text().splitlines()
    header = lines[0] if lines else ""
    match = re.match(r"# commit (\S+) host (\S+)", header)
    if not match:
        return None
    if match.group(2) != socket.gethostname():
        print(f"the baseline was measured on {match.group(2)}, not this machine; measure it again")
        return None
    ids = {line for line in lines if line and not line.startswith("#")}
    return ids, match.group(1)


def cmd_compare(_args) -> int:
    base = read_baseline()
    if base is None:
        print("no baseline for this machine: run `cloud_battery.py baseline` on origin/main first")
        return 2
    base_ids, base_commit = base
    if not static_checks():
        return 1
    ids, summary = failing_ids()
    still = sorted(ids & base_ids)
    new = sorted(ids - base_ids)
    gone = sorted(base_ids - ids)
    print(f"branch at {head()}: {summary}")
    print(f"baseline at {base_commit}: {len(base_ids)} failing")
    print()
    print(f"still failing, the machine's: {len(still)}")
    print(f"no longer failing: {len(gone)}")
    for i in gone:
        print(f"  {i}")
    print(f"NEWLY FAILING, yours: {len(new)}")
    for i in new:
        print(f"  {i}")
    return 1 if new else 0


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
