---
title: The two processes claiming one job test waits a fixed half second for both to start
found: at the test trim of #858, U301, 2026-11-22.
issue: no
---

**The mechanism.** `tests/test_jobs.py::test_two_processes_claiming_the_same_job_never_claim_one_item_twice`
starts two real worker processes and gives them a fixed 0.5 second sleep to
import before they race. Under a load average near 10 on the four core cloud
container one worker had not finished importing in time, claimed nothing, and
the test failed once. The test's code is the base's, unchanged by U301.

**Measured cost.** A false red under load, seen once in several runs; no
product defect. Not on the base's Linux baseline list.

**Closes when:** the workers signal that they are ready (a marker file each,
as the suite's other process tests do) and the race starts on both signals.
Ledger only.
