---
title: A stop on a pair's own first sync, with the account reordered past it since, is no longer named on the gate
found: at the review of #597, R-1376, round one, 2026-11-07.
issue: no
---

**The mechanism.** R-1376 makes a first sync fold nothing, since it has no base, so a first sync names a stop only when its order is finished (`finishing` is set from `folded or stopped`). A pair marked whose first sync stopped part way through its order after committing rekordbox, with the account then reordered off the stopped write's path, plans as any first sync with the account leading, and the gate no longer says a stopped write was found.

**Measured cost.** Driven by the round one reviewer: a hand pairing whose first sync's order stopped before any move, the account then reordered to 3, 2, 1, 4. The base's gate said "finishes run X's write ... whose additions and removals are read as that write's; the account was reordered since, so its order is read as yours", whose first clause was untrue on a first sync, which folds nothing. The branch's says only "order follows the account's". Both end at 3, 2, 1, 4 on both sides. Nothing is written differently.

**Closes when:** the gate names a stop it found and set aside as a person's reorder, on a first sync as on a later one, without claiming a fold. Ledger only.
