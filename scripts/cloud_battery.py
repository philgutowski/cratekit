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
VERDICT = STATE / "last-compare.txt"
PYTHON = ROOT / ".venv" / "bin" / "python"
RUFF = ROOT / ".venv" / "bin" / "ruff"

# pytest's short summary lines, `-rfE`: "FAILED path::id - reason" and
# "ERROR path::id - reason". The id is everything before the first " - ".
SUMMARY_RE = re.compile(r"^(?:FAILED|ERROR) (\S+)")


#: The header's last field, which `compare` and the mutation driver require.
FULL_HISTORY = "history full"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


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


def failing_ids() -> tuple[set[str], str]:
    """Run the suite and return the failing and erroring ids with the summary line."""
    # No `-q` here: pyproject's addopts already carry one, and a second makes
    # `-qq`, which hides the summary line this reads. The mutation driver's
    # docstring records the same trap, met the same way.
    result = run([str(PYTHON), "-m", "pytest", "--tb=no", "-rfE", "-p", "no:cacheprovider"])
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
    if not full_history_or_refuse():
        return 1
    if not static_checks():
        return 1
    ids, summary = failing_ids()
    STATE.mkdir(exist_ok=True)
    BASELINE.write_text(
        f"# commit {head()} host {socket.gethostname()} {FULL_HISTORY}\n# {summary}\n"
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
    match = re.match(r"# commit (\S+) host (\S+)(?: (history \S+))?$", header)
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
    ids = {line for line in lines if line and not line.startswith("#")}
    return ids, match.group(1)


def cmd_compare(_args) -> int:
    base = read_baseline()
    if base is None:
        print("no baseline for this machine: run `cloud_battery.py baseline` on origin/main first")
        return 2
    base_ids, base_commit = base
    if not full_history_or_refuse():
        return 1
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
    record_verdict("red" if new else "clean")
    return 1 if new else 0


def record_verdict(verdict: str) -> None:
    """Write the verdict for the commit just measured, for `release.py cut` (U159).

    The full sha, so a release refuses a verdict from any other commit, and
    `dirty` in place of the verdict when the tree carried uncommitted changes,
    since then the run measured something no commit holds.
    """
    sha = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    if run(["git", "status", "--porcelain"]).stdout.strip():
        verdict = "dirty"
    STATE.mkdir(exist_ok=True)
    VERDICT.write_text(f"{sha} {verdict}\n")


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
