---
title: A two genre track doubled in a third band folder gets one move listed twice under one id
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** `adopt move`'s `build_move_plan` asks every tree path
bucket once per entry. A track with a second genre has two entries; a third
band folder holding it in two bands is not claimed by either, so both entries
ask it and plan the same move.

**Measured cost.** Driven at round one with the double seeded through the
writer: the gate showed two rows with one id, counts moves 2 and
memberships_removed 2; the worker removed 1 and succeeded. The gate overstates
by one; nothing is lost. The producer (a hand filed double in a third folder)
was not driven through a verb.

**Closes when:** the tree path questions are asked once per track, not per
entry. Ledger only: a count, nothing written wrong.
