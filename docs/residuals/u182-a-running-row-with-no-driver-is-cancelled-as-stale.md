---
title: A stale cancel reconciles a running row no live driver holds and then cancels it, while the brief says never a running one
found: at the review of #379, U182, 2026-11-01.
issue: no
---

**The mechanism.** `crate job cancel --stale-days N` first reconciles every intake job of the library whose row says running, the disk truth every job verb reports from: a row that says running while no driver holds its lock was killed, and it reads as queued again. A job reconciled this way that is older than N days is then offered and cancelled like any queued job. Fable drove it at round one: a job 90 days old, its row set running, no lock held, a real run, state cancelled.

**Measured cost.** None false: the job was not running, only its row said so, and `crate job resume` reopens it. The record reads "never a running one" as never a job a live driver holds, which the lock check under the cancel guarantees.

**Closes when:** Phillip says the brief meant the row, in which case a reconciled job is listed as left with its reason. Ledger only.
