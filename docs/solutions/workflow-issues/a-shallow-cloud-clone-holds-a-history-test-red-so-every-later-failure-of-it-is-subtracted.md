---
title: "A shallow cloud clone holds a history test red on the base, so the Linux battery and the mutation driver subtract every later failure of it"
date: 2026-11-03
category: workflow-issues
module: "scripts/cloud_battery.py, scripts/mutate.py, tests/test_restart_and_residual_files.py"
problem_type: workflow_issue
component: testing_framework
severity: high
root_cause: environment_dependency
resolution_type: workflow_improvement
applies_when:
  - "A cloud session's baseline lists a test that reads an old commit, a tag, or git log"
  - "A mutation row that should plainly kill a test reads as a zero in the cloud"
  - "The macOS battery fails a test the cloud's compare reported as still the machine's"
symptoms:
  - "AssertionError: the split base a984968 is not in this clone"
  - "git rev-parse --is-shallow-repository prints true on the container"
  - "A row's one killing test is among the known failures, so the row reads 0 kills"
tags:
  - "cloud-lane"
  - "shallow-clone"
  - "mutation-driver"
  - "known-failures"
  - "linux"
---

# A shallow cloud clone hides a new failure behind the machine's old one

## What happened

U195 reworded a sentence of a moved restart record on purpose, and the test
that holds every moved paragraph byte for byte against the split base failed
on the Mac at the v0.5.0 cut. U195's cloud battery had read 0 newly failing.
On U199, the mutation row that empties the new rewording table first read as a
zero, though it plainly breaks that same test.

## Why

The container's clone is shallow. The test reads `a984968` with `git show`,
which is absent, so it failed on every cloud base for that reason. The battery
and the driver subtract a known failure by node id, not by cause, so once the
history reddened the test, nothing else that broke it could be seen: not
U195's rewording, and not U199's mutant. Five tests of
`tests/modules/test_reports.py` were held unread the same way.

## What to do

Before the baseline, unshallow: `git fetch --unshallow origin main`. Then a
history test fails only for its own reason, and the base's baseline names it
only if the base is really broken. For the mutation driver's known failures,
use a baseline measured on the branch head with full history when the branch
fixes a test the base fails, since the base's list still names it; measure
that file, never edit one by hand. The earlier entry on CI's shallow checkout,
`a-cause-read-from-a-log-is-not-a-cause-driven-by-reproducing-it.md`, is the
same trap on GitHub's runner.
