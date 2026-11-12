---
title: A tombstone can stand over a version an active row still holds, so the label verbs take a held track off its year
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** `crate delete review` tombstones the version of a row it
trashes even when another active row records the same artist and title under
a different file. Since U243 the label verbs read that tombstone track by
track, so the version comes off its label year playlist although the library
still holds a copy of it.

**Measured cost.** The round one review drove the deletion half end to end
(row 1 removed, row 2 active, one title, two files, a tombstone written while
row 2 stayed) and the prune half is the branch's own test; the two were not
joined in one run. A person who keeps a second copy loses the track from one
account playlist, and can put it back by hand.

**Closes when:** the label side, or the recorder, declines a tombstone whose
version an active row still holds, with a test over both halves in one run.
Ledger only.
