---
title: A sync pair that finished a stopped order without moving the snapshot leaves the next gate saying the pair finishes that stopped run again
found: at the review of #577, U225, round two, 2026-11-06.
issue: no
---

**The mechanism.** A run that finishes a pair releases its own steps on success. When it finished the pair's order but did not move the pair's snapshot, on the account gate alone or over a short account listing, the stopped run's ordering record is still the latest the next plan reads, and it began after the snapshot, so the next gate's pair line and the `sync-pair-finishing` warning name the pair as finishing that run again.

**Measured cost.** Driven by the round two reviewer: the fixture's stop, then `sync pair` with rekordbox skipped (the account in rekordbox's order, the steps file gone, the snapshot still the four tracks), then a fresh gate. The sentence is false; the plan held no item and both sides ended in rekordbox's order, so nothing wrong was written. A short listing after a stop says the same while nothing is planned.

**Closes when:** a finished pair's order is recorded where the next plan reads it, for example a run's finished pairs kept as a record of their own once its plan is released, or the sentence is said only when the plan writes the pair's order.
