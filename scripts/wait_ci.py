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
conflicts with `main` looks like, since GitHub starts no run for it; 3 when
the runs could not be read three times in a row (a refused token, a
repository the session cannot reach), with the reason. A single failed read
is waited past, never read as no run.
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
#: and no run at all yet, since either one means the session waits. Unread is
#: `wait`'s alone: the runs could not be read, which is not the same as none.
PENDING, PASSED, FAILED, UNREAD = "pending", "green", "red", "unread"

#: Failed reads in a row before the wait stops and says it could not read.
READ_FAILURES = 3


class ReadFailed(Exception):
    """The runs could not be read: the reason, never an empty list."""


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


def _gh_runs(repo: str, sha: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", "api", f"repos/{repo}/actions/runs?event=pull_request&head_sha={sha}"],
        capture_output=True,
        text=True,
    )


def pull_request_runs(repo: str, sha: str) -> list[dict]:
    """The pull request runs on one head; `ReadFailed` when they cannot be read.

    Every way the read can fail is a `ReadFailed` with its reason, `gh` missing
    from the path included, so no unreadable state leaves `main` as a traceback
    and an exit 1 a session would read as red.
    """
    try:
        result = _gh_runs(repo, sha)
    except OSError as exc:
        raise ReadFailed(f"gh could not run: {exc}") from None
    if result.returncode != 0:
        reason = (result.stderr or result.stdout or "").strip().splitlines()
        raise ReadFailed(reason[-1] if reason else f"gh exited {result.returncode}")
    try:
        answer = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ReadFailed("the answer was not JSON") from None
    if not isinstance(answer, dict) or not isinstance(answer.get("workflow_runs"), list):
        raise ReadFailed("the answer carried no workflow_runs list")
    return answer["workflow_runs"]


def wait(read, *, timeout: float, every: float, sleep=time.sleep, clock=time.monotonic):
    """Read until the verdict is not pending, the reads keep failing, or time runs out.

    `read` returns the runs or raises `ReadFailed`; `sleep` and `clock` are the
    test's to replace. A failed read is waited past, and `READ_FAILURES` of them
    in a row end the wait as unread with the last reason, so a refused token
    costs minutes rather than the whole timeout and is never told as no run.
    """
    deadline = clock() + timeout
    failures = 0
    while True:
        try:
            runs = read()
        except ReadFailed as exc:
            failures += 1
            if failures >= READ_FAILURES:
                return UNREAD, f"could not read the runs {failures} times in a row: {exc}"
            state, line = PENDING, f"could not read the runs: {exc}"
        else:
            failures = 0
            state, line = verdict(runs)
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
    return {PASSED: 0, FAILED: 1, UNREAD: 3}.get(state, 2)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
