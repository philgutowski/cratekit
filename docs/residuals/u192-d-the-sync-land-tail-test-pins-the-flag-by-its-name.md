---
title: The sync land tail test pins its queue only call by the flag's name rather than by what the flag changes
found: at the review of #403, U192, 2026-11-01.
issue: no
---

**The mechanism.** `tests/test_sync_land.py::test_each_tail_step_queues_only_and_drives_its_job_through_one_job_command` and the tail step test in `tests/test_analysis_workers.py` assert that the queue call carries `--queue-only` and that the commands read queue then `--job`. Without the flag the queue call drives the job and the `--job` call re-reports a succeeded job, so the job is still driven once and only those name based assertions die.

**Measured cost.** Driven by the review: dropping the flag from `sync_land` killed only the assertion naming it. Nothing a person sees differs today; a later rewrite of the pass could keep the name and change the behaviour.

**Closes when:** the tests read what the flag decides, which call drove the job and how a failure in the queue call reaches the pass, rather than the flag's spelling. Ledger only, maintainer facing.
