---
title: A job identifier enqueue mints twice is refused as an internal error naming no job, with only the tail's width between a collision and that refusal
found: at the review of #626, U235, 2026-11-07.
issue: no
---

**The mechanism.** `core/jobs.py:enqueue` names a job with
`cli.output.new_run_id()` when the caller passes no id, and inserts it with
no check. When two minted ids meet, the INSERT raises `IntegrityError:
UNIQUE constraint failed: jobs.job_id`, which the dispatcher surfaces as
`internal-error` with the remedy to report a defect, naming neither the new
job nor the one that holds the id. U235 widened the tail to sixty four bits,
so the width is now the only line; R-22 records that the capture stamp got a
second line, a deterministic refusal in restore, and the job queue did not.

**Measured cost.** Driven only by forcing: a scratch plugin making two of the
earlier pass test's tail draws equal produced the refusal on 13 of 91 pairs.
At sixty four bits a minted collision is about one in 10^19 per pair inside
one second, and none of the enqueue call sites under `src` passes a job id of
its own, so no person can produce one by hand. Nothing is lost when it
happens: the insert is refused inside its transaction.

**Closes when:** `enqueue` catches the duplicate key on its INSERT and either
mints again or refuses naming the identifier and the job that holds it.
Ledger only.
