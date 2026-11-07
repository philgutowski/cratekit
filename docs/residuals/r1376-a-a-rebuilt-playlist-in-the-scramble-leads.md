---
title: A rekordbox playlist rebuilt in a stopped write's half done order, and paired again, is read as a rekordbox reorder since the stop, and the gate names a finish that keeps the scramble
found: at the review of #597, R-1376, round one, 2026-11-07.
issue: no
---

**The mechanism.** R-1376's first sync reads the stop on a re-paired account playlist and measures each side's change of order against what the stopped write left (`pair_merge.merge(..., stopped=...)`). A new rekordbox playlist built in the account's half done order, as importing the scrambled account playlist into rekordbox would make it, differs from the old pair's rekordbox order, so rekordbox is read as reordered since the stop and leads. Both sides end in the scramble, the gate says the pair "finishes run X's write ... so its moves are not read as anybody's; order follows rekordbox's", and the new snapshot lets the carried record go, so the stop is then forgotten.

**Measured cost.** Driven by the round one reviewer on the fake account: the U225 stop, the rekordbox playlist deleted, the pair released, a rebuilt playlist made as 2, 7, 1, 3, 4, 5, 6, hand paired, both gates applied. Nothing is written wrong: rekordbox already held that order, put there by the person, and the account already held it. The person reads a finishing sentence over a pair whose stopped order is never reached. The base reached the same end state and said nothing.

**Closes when:** the finishing sentence is said only where the finish changes the order, or names that rekordbox's order was taken as the person's. Ledger only: no write is wrong, and the sentence's clauses each hold under U225's reorder since rule.
