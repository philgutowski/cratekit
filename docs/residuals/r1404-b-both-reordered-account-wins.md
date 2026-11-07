---
title: Both sides reordered since a base whose sides disagree, the account wins and rekordbox's newer reorder is undone
found: at the review of #608, R-1404, round one, 2026-11-07.
issue: no
---

**The mechanism.** `pair_merge.merge` lets the account lead when both sides changed order since the base, the rule since U130. Outside GIG READY the account's order is not written, so the account's order that wins is one rekordbox already left behind.

**Measured cost.** Driven by the round one reviewer: a root hand pair whose rekordbox was reordered 3, 1, 2 and synced, then rekordbox reordered 2, 3, 1 and the account reordered t3, t1, t2 together; the sync writes rekordbox back to 3, 1, 2, the gate naming the account as the order's leader. Two reorders between two syncs on two sides is rare, and the brief named this case out of scope.

**Closes when:** the both reordered rule is decided for pairs whose account order is not kept, with the answer to #608's question. Ledger only.
