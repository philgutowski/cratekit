---
title: A stopped run named as finishing after a sync that finished its pair without moving the snapshot is named on every later gate, with no end date
found: at the review of #591, R-1372, round one, 2026-11-06.
issue: no
---

**The mechanism.** R-1373's shape, lengthened by R-1372. A sync that finishes a stopped pair's order on the account gate alone moves no snapshot, so the stopped run's carried record is not passed by one, and the next gate names the pair as finishing that run again. Before R-1372 the stopped run's steps aged out after thirty days and the sentence ended; its carried record now outlives them until a snapshot passes it.

**Measured cost.** Driven by the round one reviewer: the stop, a sync with rekordbox skipped, both runs aged 31 days and pruned, a rekordbox reorder, a fresh gate. The gate still named the stopped run; both sides ended in the person's new order, so nothing wrong was written. The cost is a false sentence on the gate until a sync of both sides.

**Closes when:** R-1373 closes, a finished pair's order recorded where the next plan reads it, or the sentence said only when the plan writes the pair's order.
