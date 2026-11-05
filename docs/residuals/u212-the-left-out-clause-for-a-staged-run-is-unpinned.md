---
title: A run listing with a failed job and every finished row staged answers ok, and no test reaches it
found: at the review of #506, U212, 2026-11-05, round one F6.
issue: no
---

**The mechanism.** `missing_cli._listed` refuses a run listing that wrote
nothing while jobs were left out, so a pass with failed jobs never reads as
one with nothing to download. U212 added `and not staged_rows` to that
refusal: a run whose finished jobs' only missing tracks are staged answers ok,
with the skipped row still failing and naming the job, the same answer the
listed case gives. Round one drove the shape (its `drive_d3.py`) and found it
consistent; the mutation row that drops the clause kills nothing.

**Measured cost.** None found. The shape is unpinned.

**Closes when:** a test drives `intake missing --run --skip-failed` over a run
with a failed job and a finished job whose only missing track is staged.
Ledger only.
