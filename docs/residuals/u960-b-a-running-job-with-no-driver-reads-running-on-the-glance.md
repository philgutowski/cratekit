---
title: The status glance reads a running job whose driver died as running until something reconciles it
found: at review round one of #1079, U960, 2026-11-25.
issue: no
---

**The mechanism.** The glance lists jobs in state `running` off the queue,
as `crate job list --state running` does. A job whose driver was killed
keeps `running` in the queue until `crate job show` or a resume reconciles
it against its driver lock (`jobs.reconcile`), which a read only glance does
not do.

**Measured cost.** Driven with a job moved to `running` and no driver lock
held: the glance and `job list` both read `running`, and `attention` reads
`running`; after `crate job show` reconciled it to `queued`, the glance read
`ok`. A killed driver, the real producer, was not driven. The menu bar icon
would say running for work nothing is doing.

**Closes when:** the menu bar app's card (#1085) decides whether the glance
asks the driver lock read only (`jobs.assert_free` without the reconcile) so
a job with no live driver reads apart from one that runs. Ledger only.
