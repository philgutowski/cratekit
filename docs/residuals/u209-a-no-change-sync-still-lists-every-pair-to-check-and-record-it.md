---
title: A sync pair with nothing to change still lists every account playlist once more to check it and record its snapshot
found: at the build of #499, U209, 2026-11-05.
issue: no
---

**The mechanism.** With both gates applied, U209's check lists each paired
account playlist once before the write, and a pair with nothing to write
records that listing as its snapshot. So a no change sync of every pair costs
one plan plus one listing per pair, against three plans plus one listing per
pair before. Skipping the check and the write when the plan writes nothing
would save the listings, but the snapshot and its sync moment would then stay
where they were, and a pair whose first sync never completed would stay
first, so a later removal on one side would be added back from the other.
Kept as the conservative call.

**Measured cost.** One listing per pair per no change sync, about one to two
provider calls each at a hundred tracks a page; not measured live.

**Closes when:** Phillip asks for a no change sync to stop after its plan, and
the skip excludes any pair that is first or unmarked. Ledger only.
