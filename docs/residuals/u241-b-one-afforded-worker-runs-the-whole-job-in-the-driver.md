---
title: A machine that affords exactly one light worker runs the whole job in the driver, though one worker beside the driver would nearly halve it
found: while building #649, U241, 2026-11-10.
issue: no
---

**The mechanism.** `core/pool.py` runs a plan of one worker in the calling
process, by rule: for `map_workers`, whose caller only waits, a pool of one
is a second interpreter to run the work slower. `analysis/ahead.py` keeps
that rule for the stream. But the stream's reader is not waiting: the driver
is scoring vocals while the heads are measured, so a single worker child
beside it is real parallelism. A machine whose memory affords one light
worker and not two therefore runs serially where one child would let the
head and the vocal pass overlap.

**Measured cost.** Not driven as its own case. From the stage table, a track's
head and its vocal pass take about the same time after U241 (173 and 182
seconds over the set), so one child beside the driver would bring a run close
to the two worker figure. The band it applies to is narrow: available memory
that affords one worker of about 1.2 GB for a ten minute batch, after the
reserve and the driver's model, and not two.

**Closes when:** the stream is allowed one child when its plan is one worker
bound by available memory or the ceiling and its caller declares that it
works between reads, with the pressure, unreadable and insufficient bounds
still in process. That changes the pool's most guarded rule, so it is its own
unit. Ledger only.
