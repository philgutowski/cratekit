---
title: A two genre track doubled in a third band folder gets one move listed twice, and a Soul track's doubled R&B bands block adopt move
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

Round two drove a worse member of the class: a Soul track whose second genre
is a third folder (Deep House), seeded in two R&B bands. The plan asks the
tree path once per entry and the Deep House entry plans an R&B move, while
the worker checks it against the Soul entry, which reads those bands as
settled: every run refuses `decision-stale`, nothing is written, and the
track never reaches Soul. With the genres reversed the moves are written and
the job fails with the track in neither. The same at round one's head, so
the fix round did not make it worse; the double was seeded, and
`docs/cutover.md` records two live tracks holding two bands, neither with a
second genre. A Soul plus Deep House track in the old Soul / R&B playlist is
likewise moved out by one entry and listed `former-place-not-named-by-genre`
by the other.

**Closes when:** the tree path questions are asked once per track, by the
entry the worker checks against. Ledger only while no second genre track is
known to hold two bands; it earns an issue (the bar's c) once one does.
