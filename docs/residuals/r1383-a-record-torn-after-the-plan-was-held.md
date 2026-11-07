---
title: A landing record torn after a sync pair's plan was held at its gate is not looked for again, so the held plan queues its download with a clean report
found: at the review of #599, R-1383, 2026-11-07.
issue: no
---

**The mechanism.** `sync pair` plans once and its two gates reuse the held plan (U209), so the hold R-1383 added is decided when the plan is made. A session log record that turns unreadable between the plan and the answered gates is never read by the write, which queues the plan's `acquire` with `sync-pair-written` only.

**Measured cost.** Driven by round one's review by hand: records readable, `t40` lacking with an ISRC, the gate shown, the record then torn, both gates answered, and `t40` queued with no warning naming the record. A duplicate download needs a landing of that very track written and torn inside the window between the plan and the answer; that natural producer was not driven. Records are written atomically, so a torn one is a defect or a hand edit.

**Closes when:** the write reads the scan again before it queues and holds what the fresh scan cannot rule out, or the window is shown to have no producer. Ledger only: the producer is a hand edit inside a gate's window.
