---
title: A job whose analyze run item already failed source-missing under the shipped code cannot be finished by any resume
found: at the review of #555, U223, 2026-11-05.
issue: no
---

**The mechanism.** U223's staged report fallback finishes a job the shipped
code interrupted between the staged report and the commit, if nobody resumed
it under the shipped code. A60's job on the machine was resumed then, its
item failed `source-missing`, a permanent cause, and every `analyze.run`
failure is permanent, so both `crate analyze run ... --job` and
`crate job resume` refuse it as not retryable.

**Measured cost.** Driven by the round one reviewer: the shipped attempt and
resume, then the branch, printed command exit 30 "every failure is
permanent", `crate job resume` exit 30 `job-not-retryable`. The person queues
the folder again, which the refusal already names, and the renamed track is
skipped by its head.

**Closes when:** A60 (#423) retakes its interrupt on a fresh folder. Ledger
only: the requeue is the remedy shown.
