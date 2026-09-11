---
title: "The mutation driver does not fit inside a ten minute foreground call"
date: 2026-09-10
category: workflow-issues
module: "scripts/mutate.py"
problem_type: workflow_issue
component: testing_framework
severity: medium
root_cause: unverified_assumption
resolution_type: documentation_update
applies_when:
  - "A unit's mutation table is about to be run from an unattended relay task, where every command runs in the foreground under a 600 second ceiling"
  - "The first Python row of a rows file targets a module that no test file imports"
  - "You are about to spend a second ceiling length call on the driver hoping --resume will carry progress"
symptoms:
  - "The driver is interrupted by the alarm with no sidecar written and no row measured"
  - "The traceback ends inside measure_batch's null control rather than inside a row"
tags:
  - "mutation-driver"
  - "relay"
  - "foreground-ceiling"
  - "null-control"
  - "resume"
---

# The mutation driver does not fit inside a ten minute foreground call

## What happened

U60 ran as relay task 78, which runs every command in the foreground and caps a
single command at 600 seconds. Its table was twenty rows over one five file test
subset that runs in 29 seconds. Two driver calls, each stopped by a `perl` alarm
sending SIGINT just under the ceiling, measured ZERO rows between them and cost
nineteen minutes. The driver's own `finally` restored the target both times, so
the tree stayed clean, which is the one thing that went right.

## The arithmetic, which is what to check before starting

- **The full baseline is paid on every call.** `measure_batch` runs the whole
  suite at `scripts/mutate.py:957` unconditionally, `--resume` included, and
  `--resume` reuses finished rows and nothing else. The suite was 358 seconds.
- **The null control can be a second full run.** It targets the first Python
  row's file and runs on that module's derived importer subset. When no test
  file imports the module, and a CLI shell driven through `cli.run` is exactly
  that case, the subset is empty and the control runs the full suite. That was
  attempt one: interrupted inside the control at 570 seconds.
- **Moving the control to a small subset was not enough.** Attempt two put a row
  whose target has one importing test file first. It still finished no row in
  575 seconds, and where that time went was not captured, so the remaining cost
  is unmeasured rather than explained.
- **A zero can never be promoted inside the ceiling.** Promotion is a second full
  run inside the same call, after the full baseline. So even a preflight that
  fits leaves every zero unconfirmed.

## What not to spend the time on

- **More resumed calls.** Each one buys only what is left after its own baseline,
  and none of them can promote a zero.
- **Backgrounding the driver.** METHOD's driver rules forbid it and so does a relay
  task, and a backgrounded driver outlived its parent twice on this project.
- **A lighter hand rolled driver.** METHOD forbids that too, because three of
  this project's incidents were hand rolled driver mistakes.
- **`PYTEST_ADDOPTS` with a parallel runner.** Not tried. It would change how the
  collected count is reported, and that count is the check the driver compares
  every row against.

## What to do instead

The battery already measures the full suite. Read that number before writing any
rows. If it is past roughly four minutes, the table will not finish inside a relay
task: write the rows, commit them, record the gap against R-329 with the unit's
own measurements, and land the unit. Do not spend ceiling length calls finding
out. If the table must run, it runs attended or outside the task session, and the
committed rows file is all it needs.

When a rows file does run, put a row whose target has a small importer set first,
so the null control does not become a second full suite.

## Related

- R-329 in `docs/residual-findings.md`, with three options for the driver.
- `docs/mutation/u60-notes.md`, both attempts' measurements.
