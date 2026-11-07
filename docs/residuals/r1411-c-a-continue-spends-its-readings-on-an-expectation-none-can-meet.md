---
title: A continue of a refused finish is held to the check's listing beside the plan's reading, so when the check listed the lag no reading can meet both
found: at the review of #613, R-1411, 2026-11-07.
issue: no
---

**The mechanism.** On a continue of a run whose finish was refused,
`_write_account` still passes `expect`, the continue's check listing
compared exactly (`steps.has(STEP_ORDER_REFUSED)`), whose order the check
never judged, while `agreed` is the plan's reading. When the check listed
the lag, a true reading fails `expect` and a lagging one fails `agreed`.

**Measured cost.** Driven by round two through the real adapter over the
order suite's provider: 4 openings and 7 seconds of pauses spent on a
refusal that is knowable before the first read, and a true reading refused
once. The outcome is the safe one, nothing moved, and the next sync
finishes once the check serves the truth too. No data cost.

**Closes when:** a continue whose plan finishes a stopped order passes the
plan's reading alone, or `expect` is dropped where `agreed` covers it.
Ledger only.
