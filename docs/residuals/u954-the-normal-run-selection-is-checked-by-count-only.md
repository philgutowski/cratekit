---
title: The rekordbox visit's Normal run selection is checked by its count alone, so a wrong row clicked out keeps the count
found: at the review of #997, U954, 2026-11-23.
issue: no
---

**The mechanism.** U954's Analyze Tracks path selects the rows without `dyn`
by selecting all and Command clicking each `dyn` row out, then checks that
the status line reads the batch less the `dyn` count. A plain row clicked out
in place of a `dyn` one keeps that count, so the Normal run can take a `dyn`
row and overwrite its Dynamic grid while leaving a plain row unanalysed by
Normal. The Dynamic selection before it was count checked the same way.

**Measured cost.** Not driven in rekordbox, which no cloud session opens. The
reviewer drove `crate analyze check` over the outcome: on a fresh batch the
plain row left out reads waiting, so it is caught; on a second visit, where
that row was already analysed, a `dyn` row left with a one tempo grid reads
done.

**Closes when:** the visit checks the selection's rows, not only their count
(the My Tag column read off the screenshot, or a check of each `dyn` row's
grid after the visit), or an attended sitting shows the count check enough.
Ledger only: it closes at an attended sitting.
