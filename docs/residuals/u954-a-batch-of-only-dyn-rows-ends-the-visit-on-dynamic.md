---
title: A rekordbox visit over a batch whose every row is dyn ends on Dynamic, so the next launch's Auto Analysis dialog is cancelled
found: at the review of #997, U954, 2026-11-23.
issue: no
---

**The mechanism.** The brief asks that every visit end with the shared
Analysis Mode on Normal. U954 ends it on Normal by making the last Analyze
Tracks OK a Normal run on rows without `dyn`; a batch whose every row carries
`dyn` has no such row, and the visit may touch no track outside INBOX /
Analyze, so it ends on Dynamic. The skill and the landing's warning say so,
and the next launch's dialog is cancelled by the skill's step 2 for that
known cause. A visit that stops between its Dynamic OK and its last Normal
one ends the same way.

**Measured cost.** Driven as a landing of one and of two variable tracks: the
warning now says the visit ends on Dynamic. The next visit then takes the
Analyze Tracks path, which costs its selection by hand and nothing analysed
wrong.

**Closes when:** a way to leave Normal set with no row of the batch to
analyse is settled at an attended sitting: sitting 104 put the mode back by
analysing a throwaway AIFF alone on Normal, under CLAUDE.md's clause for a
probe, and whether a visit may do that routinely, or whether a Normal
Analyze Tracks dialog answered Cancel keeps its mode, is unmeasured; or
Phillip accepts the exception. Ledger only: it closes at an attended
sitting.
