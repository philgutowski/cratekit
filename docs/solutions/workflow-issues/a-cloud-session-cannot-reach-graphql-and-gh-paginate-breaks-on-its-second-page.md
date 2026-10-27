---
title: "A Claude Code cloud session cannot reach GitHub GraphQL, and gh api --paginate breaks on its second page there, so the board is read over REST a numbered page at a time"
date: 2026-10-27
category: workflow-issues
module: "scripts/board.py, scripts/scan_repo.py, scripts/cloud_battery.py"
problem_type: workflow_issue
component: development_workflow
severity: high
root_cause: environment_constraint
resolution_type: workflow_improvement
applies_when:
  - "gh issue, gh repo view or gh project fails with GitHub GraphQL is not available from Claude Code sessions"
  - "gh api --paginate fails on a repositories/<id>/ path with Numeric-ID repository paths are not supported"
  - "scripts/scan_repo.py flags a personal identifier named skills or attach on every file that contains the word"
  - "the suite shows about 170 failures on a Linux container, most of them in tests/test_doctor.py and the backup and restore suites"
tags: [cloud, github, graphql, rest, proxy, pagination, scan, battery, linux]
---

## The trap

A Claude Code cloud session reaches GitHub through a proxy that refuses every
GraphQL call by name, with its own token and with any other. `gh issue list`,
`gh repo view`, `gh project item-edit` and `gh api graphql` all fail with
"GitHub GraphQL is not available from Claude Code sessions", so `board.py
next`, `show`, `start`, `sync` and `audit` failed before their first read.
The search API is refused too ("sessions are bound to their configured
repositories"), so there is no total to check an issue read against.

`gh api --paginate` on `repos/<owner>/<repo>/issues` fetched the first page
and failed on the second: GitHub writes its `Link: <...>; rel="next"` header
with the repository by number, `repositories/<id>/issues?page=2`, and the
proxy rejects numeric repository paths. The first page came back whole, so a
read that trusted it would have seen a hundred issues of three hundred and
thirty five and said nothing.

Two more, found the same afternoon. `scripts/scan_repo.py` reads the names of
mounted volumes as the author's identity, and the container mounts the
harness's fixtures at the mount root under names such as `skills` and
`attach`, so the scan flagged nine test files and the vendored licence for
containing an English word. And the suite carries about 170 failures on the
container that are the machine's: the session runs as root, which reads a
directory whose mode says it cannot, so every "unreadable directory" test in
`tests/test_doctor.py`, the backup and restore suites and `tests/test_adoption.py`
fails; there is no `hdiutil`; the timing calibration is pinned to one Mac.

## The resolution

- `board.py` reads the issues over REST when the GraphQL count is refused
  (`load_issues_rest`), asking for `page=1`, `page=2`, ... explicitly and
  ending on the first page shorter than a hundred, which is whole by
  construction, and `repo_slug` parses the origin remote when `gh repo view`
  is refused. `board.py cloud` is the queue for a cloud session and reads
  each card's comments the same way. `start`, `sync` and `audit` without
  `--labels-only` stay local.
- `scan_repo.py` skips the detected identity tier under `CLAUDE_CODE_REMOTE`.
  The declared tiers, the identity file and `CRATEKIT_SCAN_IDENTITY`, still
  apply there.
- `scripts/cloud_battery.py baseline` measures the machine's failures on the
  base commit on that container, and `compare` reads the branch against them,
  so a session fixes what is newly failing and reports the rest by count.
  Nothing is skipped or marked.

## The rule

On a cloud container, every GitHub read is `gh api` on a
`repos/<owner>/<repo>/...` path with an explicit page number, or a GitHub MCP
tool. Never `--paginate`, never a GraphQL verb, never a search path. A red
suite there is read against the base's red, never as green and never as
yours, and the macOS battery stays the merge gate.
