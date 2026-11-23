---
title: A base cannot be captured with a branch's scenarios once the test modules they borrow import a module the branch added
found: at the behaviour comparison of #867, U310, 2026-11-22.
issue: no
---

**The mechanism.** `behaviour_compare.py capture --rev` swaps only `src/`,
so scenarios and fixtures come from the working tree. This card's scenarios
borrow fixtures from `tests/test_adoption.py` and `tests/test_deletion.py`,
and after the split those test modules import `cratekit.adopt.revert_changed`,
which the base does not have. A capture of the base from the branch's tree
fails at collection, every scenario unrecorded. DEVELOPING's rule that a
scenario names nothing the base lacks holds for the scenario file and not for
the test modules it imports.

**Measured cost.** The comparison was read against the base capture taken
before the first edit, with the base's own fixtures, which holds it more
strictly; nothing was lost here. A later card that wants to recapture this
base from its own tree will meet the same refusal.

**Closes when:** the capture refuses with the import named, or scenario
fixtures live in a module that imports only what every revision has. Ledger
only.
