---
title: A bound knowable before the first call is asked before the loop, and one name over two guards hides which is which
date: 2026-09-24
category: integration-issues
module: src/cratekit/intake/acrcloud.py
problem_type: integration_issue
component: tooling
severity: medium
root_cause: missing_validation
resolution_type: code_fix
applies_when:
  - "A per-run cap guards a loop that spends a metered quota"
  - "One constant is read both as a spend bound and as a not-one-set refusal"
---

# A bound knowable before the first call is asked before the loop, and one name over two guards hides which is which

## Problem

`MAX_CALLS_PER_RUN = 400` in `intake/acrcloud.py` did two jobs under one name. It bounded what one run may spend, and it refused any set whose chunk grid was longer than that. A 5 hour 5 minute mix hit the refusal, so sitting 11 split it by hand with ffmpeg and the parts landed as unrelated playlists.

## Cause

The two guards were never separated. Once they were, a second trap showed up (R-706, task 218). The per part run guard was first written inside the spend loop, so it refused only after earlier iterations had already spent calls. The suite and the first mutation row were green; the adversarial review found it.

A part is a place in the chunk grid, never a file. The carver already reads any offset, so no file split was ever needed.

## What to do next time

- Keep the run bound (spend) and the whole-set refusal (ceiling of three parts) as separate guards with separate names.
- Any bound knowable before the first call, the per part run bound and the month's owed spend, is asked before the loop over the whole plan, not per iteration.
- A test for such a guard must assert zero calls were made on refusal, not only that a refusal was raised.
- Partition the grid with `acrcloud.partition` into the fewest even parts at or under the bound, and freeze `parts` beside `calls` on the queued job so the set lands as one batch.
