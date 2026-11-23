---
title: "A kill set replay of thousands of rows is paid in starts, null controls and zero promotions, not in tests"
date: 2026-11-23
category: workflow-issues
module: "scripts/mutate.py, scripts/killset.py, scripts/cloud_battery.py"
problem_type: workflow_issue
component: development_workflow
severity: medium
root_cause: environment_constraint
resolution_type: workflow_improvement
applies_when:
  - "a card replays the recorded kills of many files, a thousand rows or more, on a cloud container"
  - "a replay batch is cut at the two hour background job limit and its resume measures every subset baseline and the null control again"
tags: [cloud, mutation, replay, killset, batches, null-control, zero, xdist, helpers]
---

## The trap

U325 (#930) measured U298's kill set replay, 3,725 rows before and again
after, on four core cloud containers where a background job is stopped at two
hours. Sizing batches by the tests each row runs got the cost wrong three
ways, each measured there:

- **A row's start costs more than its tests.** A light row (a subset of a
  hundred or two tests) took about 20 seconds at two xdist workers, of which
  the tests were a few: the controller, the workers' imports and collection
  are paid by every row. At two workers that start is paid twice in cores.
- **Every batch pays a full suite null control**, and a resume pays it again
  with every subset baseline. The suite took 7 min 18 s at four workers, so
  the null control is about 15 minutes at two workers and 30 at one. Four
  lanes of one worker paid it four times per two hour window, about 40
  percent of the machine.
- **A zero row is promoted to the full suite**, the same 15 or 30 minutes.
  Zeros cluster: in `tests/test_restore_cli.py`, where 27 of 98 tests fail on
  the container for want of a Mac, a quarter of the rows read zero, and one
  batch of 132 rows needed four runs and seven hours. The zeros were zeros on
  the base too, so no kill was lost, but each cost a full suite on both sides.

## What to do

- **Read the full baseline, never measure it per batch.** Give each worktree
  its own `.venv`, run `cloud_battery.py compare` in it once against the
  known failures file the batches will pass, keep the tree clean (row files
  and `--out-dir` outside it), and every batch there reads the battery's
  verdict (U271).
- **Pack by subset and by measured cost**: one subset baseline per subset,
  about 20 seconds a light row at two workers (13 seconds at one), 0.031
  seconds a test at two workers, and a zero allowance. Heavy rows (a subset
  of a thousand tests or more) run two workers wide; light rows one worker
  wide, where the start is paid once. Size each batch to finish inside the
  job cap, since a resume pays the null control and the subset baselines
  again.
- **Run the after rows beside the before rows.** `killset.py rows --after`
  reads only a finished table, so write it over a provisional table of every
  before row (the rows measured so far as measured, the rest as killed with
  their row subset) and defer from the after batches any row the before side
  reads as not killed: `check` asks nothing of it.
- **Ask for helper sessions.** The coordinator can start helpers, each its
  own container and four cores, that run a list of batches at the pinned
  commit with the same driver and push the tables to their own branch. U325
  offloaded its fifty light batches to six helpers and had every row
  measured about fifteen hours after its first batch started, where one
  container alone was on course for about forty.
- **A row that breaks a guard can leave the machine changed.** A row that
  breaks `core/config.py`'s test root guard lets
  `tests/test_config_test_root.py` write a directory at the filesystem
  root, and from then on eight of its tests fail on that container: later
  rows read killed by those eight alone, and the next null control dies.
  The harness refuses to remove it, so such rows run on a fresh container,
  one guard breaking row to a container, checked for the directory before
  the baseline and after each batch (residual `u325-a`).
- **A row #855 left killed only by an inode bound test**, under no scratch
  copy, is measured again against one before it is believed (see the inode
  entry beside this one). U325's one such row read zero then, on both sides.
