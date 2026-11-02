#!/usr/bin/env python3
"""Wait for the pull request run on one head commit, in one call (U196).

A cloud session used to poll CI with a check every few minutes, and every
wake sent its whole context again to read one line. This blocks instead, as a
tracked background job, and returns once with the verdict, so the session
wakes once.

    .venv/bin/python scripts/wait_ci.py <sha>                 # the repository's origin
    .venv/bin/python scripts/wait_ci.py <sha> --timeout 3600 --every 60

It reads `actions/runs?event=pull_request&head_sha=<sha>` over REST, because
the pull request run is the one that judges a pull request's range and its
card, and a push run on the same head can be green while that one is not. It
waits until at least one such run exists and every one of them is completed.

Exit 0 when every pull request run on the head ended `success`, `neutral` or
`skipped`; 1 when any ended otherwise; 2 when the wait ran out with a run
still pending or none started, which is also what a pull request that
conflicts with `main` looks like, since GitHub starts no run for it.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time

GREEN = ("success", "neutral", "skipped")

#: The three answers `verdict` gives. Pending covers both a run still going
#: and no run at all yet, since either one means the session waits.
PENDING, PASSED, FAILED = "pending", "green", "red"


def verdict(runs: list[dict]) -> tuple[str, str]:
    """Read the workflow runs on one head as pending, green or red, with a line.

    `runs` is the `workflow_runs` list of the REST answer. No run yet is
    pending, never green: an absent run is not a passing one.
    """
    if not runs:
        return PENDING, "no pull request run on this head yet"
    unfinished = [run for run in runs if run.get("status") != "completed"]
    if unfinished:
        names = ", ".join(sorted(str(run.get("name")) for run in unfinished))
        return PENDING, f"{len(unfinished)} of {len(runs)} run(s) still going: {names}"
    failed = [run for run in runs if run.get("conclusion") not in GREEN]
    if failed:
        named = ", ".join(sorted(f"{run.get('name')} {run.get('conclusion')}" for run in failed))
        return FAILED, f"{len(failed)} of {len(runs)} run(s) not green: {named}"
    return PASSED, f"{len(runs)} run(s), every one green"


def origin_repo() -> str:
    """`owner/name` of the checkout's origin, read from its URL."""
    url = subprocess.run(
        ["git", "remote", "get-url", "origin"], capture_output=True, text=True
    ).stdout.strip()
    match = re.search(r"github\.com[:/]([^/]+/[^/.]+?)(?:\.git)?$", url) or re.search(
        r"/git/([^/]+/[^/.]+?)(?:\.git)?$", url
    )
    if not match:
        raise SystemExit(f"wait_ci: cannot read owner and name from origin {url!r}")
    return match.group(1)


def pull_request_runs(repo: str, sha: str) -> list[dict]:
    """The pull request runs on one head, or an empty list when the read fails."""
    result = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}/actions/runs?event=pull_request&head_sha={sha}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    try:
        return json.loads(result.stdout).get("workflow_runs", [])
    except json.JSONDecodeError:
        return []


def wait(read, *, timeout: float, every: float, sleep=time.sleep, clock=time.monotonic):
    """Read until the verdict is not pending or the time runs out.

    `read` returns the runs; `sleep` and `clock` are the test's to replace.
    """
    deadline = clock() + timeout
    while True:
        state, line = verdict(read())
        if state != PENDING:
            return state, line
        if clock() + every > deadline:
            return PENDING, f"timed out: {line}"
        sleep(every)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("sha", help="the pull request's head commit")
    parser.add_argument("--repo", help="owner/name, default the checkout's origin")
    parser.add_argument("--timeout", type=float, default=3600.0, help="seconds, default 3600")
    parser.add_argument("--every", type=float, default=60.0, help="seconds between reads")
    args = parser.parse_args(argv)
    repo = args.repo or origin_repo()
    state, line = wait(
        lambda: pull_request_runs(repo, args.sha), timeout=args.timeout, every=args.every
    )
    print(f"{state}: {line}")
    return {PASSED: 0, FAILED: 1}.get(state, 2)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
