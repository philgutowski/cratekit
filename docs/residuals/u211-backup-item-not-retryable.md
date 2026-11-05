---
title: A backup job whose database item met an unconfirmed rekordbox absence cannot be resumed, only queued again
found: at the review of #505, U211, 2026-11-05.
issue: no
---

**The mechanism.** `backup/cli._engine_refusal` rebuilds a portion refusal
from the reservation table, with no `retryable`, so the database item a job
recorded under `rekordbox-absence-unconfirmed` is permanent. The scan's own
refusal said `retryable=True`, and that is lost on the way. Since review round
two the dispatcher answers the job's verdict as it is, failed and not
resumable with the job's own step, rather than as a kept run.

**Measured cost.** Driven by review round two and by
`tests/test_process_scan_jobs.py`: `crate job resume` refuses the job with
`job-not-retryable`, and a fresh `crate backup run` once the process has
exited takes the snapshot. The files portion mirrored on the first run either
way. The person runs the backup again rather than resuming it.

**Closes when:** the engine refusal for this slug is retryable, so `job
resume` retakes the database item once the scan reads clean. Ledger only: the
workflow finishes with a fresh run, and nothing is lost or misreported.
