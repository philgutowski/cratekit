---
title: The stale cancel's race guards, the queued recheck under the lock and the reconcile of running rows, are reached by no test
found: at the mutation table of #379, U182, 2026-11-01.
issue: no
---

**The mechanism.** `_cancel_queued` in `src/cratekit/cli/jobs.py` takes the job's driver lock and cancels only while the row still says queued, and catches a driver that took the lock between the listing and the cancel. `_cancel_stale` reconciles running rows before it reads them. Each guards a race between the listing and the cancel inside one command, and no test interleaves a driver there, so reverting any of them leaves the suite green (rows M11 and the review's M3, M4 and M10).

**Measured cost.** Not driven: a driver taking a job inside the few milliseconds between the listing and its cancel was not produced. The listing's own lock check (row M6) is killed, so a job held when the command starts is never offered.

**Closes when:** a test holds a job's lock from a second process between the listing and the cancel, through a seam in the loop. Ledger only, maintainer facing.
