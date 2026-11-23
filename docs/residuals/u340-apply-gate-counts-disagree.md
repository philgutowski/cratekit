---
title: The adopt apply gate's own counts disagree for a two genre track
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** `AdoptionPlan.counts()` and `energy_readings()` count one
entry per track (`firsts()`), while `withheld_by_placement()` and
`vocal_counts()` count every entry, a second genre's included.

**Measured cost.** Driven at round one: a track in both folders at Med with
its energy changed to 8 showed `counts.withheld` 1 beside
`withheld_by_placement.total` 2. A count an independent table does not
reproduce; nothing is written wrong.

**Closes when:** every count on the gate says whether it counts tracks or
placements, and the two kinds agree. Ledger only.
