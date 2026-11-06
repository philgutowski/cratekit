---
title: A write stopped part way through its order is forgotten once its run's steps are older than a held plan is kept, and the next sync pair writes its scramble into rekordbox
found: at the review of #577, U225, round two, 2026-11-06.
issue: yes
---

**The mechanism.** `core/held_plan.recorded_steps` reads a run's steps only while they are younger than `KEEP`, thirty days, the age a held plan is kept for its continue. U225's fresh plan finds a write stopped part way through a pair's order only through those steps. A pair left scrambled by such a write and not synced for thirty days is planned as before U225: the stopped write's own moves read as the person's reorder on the account, the account leads, and rekordbox is put in the scramble. Nothing says a record aged out.

**Measured cost.** Driven by the round two reviewer on the fake account: the fixture's stop, its steps file's time set 31 days back, then a fresh `crate sync pair`. The gate said "order follows the account's", the plan carried a rekordbox `order` item, and rekordbox became 2, 7, 1, 3, 4, 5, 6, the brief's exact cost, with only `sync-pair-written` said. The producer, thirty days without a sync after a stop, was simulated by the file's time and not produced by the system.

**Closes when:** a stopped write's ordering record is kept until the pair's snapshot passes it, whatever its age, or a plan that finds a pair's ordering record aged out says so on the gate and leaves the pair's order alone.
