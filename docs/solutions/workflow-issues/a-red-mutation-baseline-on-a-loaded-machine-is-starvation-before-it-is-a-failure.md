---
title: "A red mutation baseline on a loaded machine is starvation before it is a failure"
date: 2026-09-20
category: workflow-issues
module: "scripts/mutate.py"
problem_type: workflow_issue
component: mutation_driver
root_cause: environment
resolution_type: process_change
applies_when:
  - "scripts/mutate.py refuses a batch because its baseline is not green, and the battery was green minutes earlier"
  - "A session runs unattended under Relay, where a background job is forbidden and the harness kills a foreground command at 600 seconds"
  - "Many suites or drivers have run on this machine in the last day"
symptoms:
  - "BASELINE IS NOT GREEN from the driver, with hundreds of failing tests that pass when their files are run alone"
  - "A load average in double digits and almost no free pages in vm_stat"
  - "A driver killed at the tool ceiling leaves a mutation in the source file"
related_components:
  - test_suite
  - relay
tags:
  - mutation-table
  - red-baseline
  - starvation
  - foreground
  - relay
  - r-290
---

# A red mutation baseline on a loaded machine is starvation before it is a failure

## What happened

The first sitting of the R-290 unit committed its fix by 01:44 on 2026-09-20 and
then spent three hours and twenty minutes trying to measure a 21 row table. The
driver refused three times on a red baseline. The session diagnosed it
correctly in its own log, load 16 and all 341 suspect tests green when run
alone, and kept retrying anyway. At 05:06 the machine ran out of memory and the
login session died, taking the whole Relay run with it. The cause was outside
the repository: a file sync client mirroring the workspace, build caches and
all, had grown to tens of gigabytes resident on an 18 GB machine.

The second sitting measured 25 rows on the same code shape in two foreground
passes of 511 and 473 seconds, baseline green, with 3.3 GB free at the start.
Load reached 12.8 during the second pass and the baseline stayed green, so the
load average alone is not the tell. Free memory is.

## What to do

- The driver's refusal is correct. A red baseline makes every row read as a
  death. Do not work around it and do not retry it on the same machine state.
- Before suspecting the code, run `vm_stat` and `uptime`. A few thousand free
  pages, or swapouts in the millions, is the answer. Run the failing files alone
  and serially: green there means the environment.
- If the box is starved and nobody is attending, that is a BLOCKED outcome with
  the evidence in it. Three retries cost a 52 task run.

## Foreground under the 600 second ceiling, without a kill

METHOD says to run the driver as a tracked background job, because a foreground
run killed at the harness ceiling leaves a mutation in the source. Relay forbids
a background job. Both hold if the driver is stopped CLEANLY before the ceiling:
start `scripts/mutate.py <spec> --resume` as a child, send it SIGINT at about
510 seconds, and wait for it. The interrupt arrives as `KeyboardInterrupt`, the
driver's `finally` restores the file and verifies the restore, and the sidecar,
written after every row, lets the next call resume. Each call re-pays the full
baseline, the subset baselines and the null control, measured here at roughly
two and a half minutes, so budget six minutes of rows per call. Check
`git status` between calls: only the table's own two files may be untracked.

The other way, used by the R-118 unit, is to split the spec into batches that
each finish under the ceiling. It costs the same overhead per batch and leaves
several tables instead of one.

## Seen again on U92, 2026-09-20, in a shape the entry above would not have matched

The tell described above is "hundreds of failing tests". U92's driver refused
with TWENTY FIVE, every one of them in `tests/test_rebuild.py` and always the
same twenty five. That does not read as starvation. It reads as selective
damage, which is the exact false reading `run_pytest`'s own comment warns about
for the ffmpeg case, and it sent the session looking for a cause in the driver.

**It was the same thing, and about twenty minutes went into proving it was not
the driver.** The driver's environment was rebuilt by hand, piece by piece, and
the full suite was run green under every one: the same `-o addopts` with `-q`
stripped, `-p no:cacheprovider`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH`
prepended with a temp directory, the four `PYTEST_*` variables scrubbed, output
captured to a pipe rather than a terminal, and finally the reporting plugin
itself extracted from `mutate.py` and loaded with `-p`. Five green full runs
against two red driver runs. Then the third driver run, at a HIGHER load
average than the second, came back valid with all nine rows killed.

Two things generalise:

- **The cluster size does not distinguish starvation from damage, and the file
  does not either.** `tests/test_rebuild.py` builds a real disposable database
  per test and one of its tests spawns four child processes that take a file
  lock a hundred times between them, so it is the file on this suite most
  sensitive to a machine with nothing left to give. A single file going red is
  still environment first.
- **Rebuilding the driver's environment by hand is a dead end.** It is a long
  list, every item of it is green, and the list is not where the answer is. The
  cheap checks in "What to do" above are `uptime`, `vm_stat`, and running the
  failing file alone. When those say environment, the next move is to run the
  driver again, not to model it.

**The null control earned its place.** The second refusal was not the baseline,
which was green that time, but the automatic control row killing the same
twenty five. A batch that had skipped the control would have reported those
twenty five as deaths on whichever row happened to run under the same
conditions, and the table would have looked better than the truth rather than
worse.
