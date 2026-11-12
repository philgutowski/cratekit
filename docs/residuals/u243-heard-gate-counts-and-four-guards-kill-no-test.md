---
title: The heard gate's counts for tracks left out and four guards of the fix rounds kill no test
found: at the review of #672, U243, 2026-11-12.
issue: no
---

**The mechanism.** Round two's mutation of the round one fix found seven
guards that killed nothing; round two's fix pinned the kept read's artist half
and the heard early return's year row. Still unpinned: the two subtractions
that give the heard screen's "already there" count, the exclusion of a track
the year already holds from ``HeardPlan.tombstoned``, the item's "removed from
the library" count, and the prune note's clause naming removed tracks. When a
removed track is still on the year, heard counts it "already there", which it
is, while the early return counts every merged track as left out.

**Measured cost.** None on any write: each is a count or a sentence on a gate.

**Closes when:** each count is pinned by a test, or the screen's counts are
drawn from one place. Ledger only.
