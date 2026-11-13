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
  CORRECTED BY U271: given `--known-failures`, the driver reads the full
  baseline from the cloud battery's record instead when that record is for
  the same commit, on a clean tree, on this machine, with the same known
  failures file, so a call made right after `cloud_battery.py compare` on the
  same head pays one full run fewer. Any other call still pays it.
- **The null control IS a second full run, always.** CORRECTED BY U61. This
  bullet first said the control runs on the first Python row's derived importer
  subset. It does not: `measure_batch` passes subset `None` and the label
  `"full suite"` for it at `scripts/mutate.py:1002`. U61 measured the stages by
  sampling the driver's pytest children every three seconds: the baseline ran 3
  to 363 seconds, the control started at 366 as a second full run, and SIGINT at
  570 found it still going. The preflight is two full runs before any row.
- **So moving the control to a small subset cannot work.** Attempt two put a row
  whose target has one importing test file first, on the wrong reading above.
  It finished no row in 575 seconds for the reason the bullet above gives.
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

Row order does not change the control, which is a full run whatever comes first.
Order does matter for one thing: a zero row's promotion cannot finish, and every
row after an unfinished one waits behind it, so put the rows expected to measure
zero last.

To find out where a driver call's time goes, sample its children rather than
reading its output, because it prints nothing until it finishes. U61's wrapper
forks the driver, polls `pgrep -lf pytest` every three seconds, prints what
changed with the elapsed time, and sends SIGINT before the ceiling so the
driver's own restore runs.

## Related

- R-329 in `docs/residual-findings.md`, with three options for the driver and
  U61's correction to the second.
- `docs/mutation/u60-notes.md`, both of U60's attempts, and
  `docs/mutation/u61-notes.md`, the sampled stage timing.
