---
title: A sync of every pair that fails part way says nothing of the pairs it already wrote
found: at the second review of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** `sync_pair` applies the pairs in one comprehension, so a
failure on one pair raises out of it and the envelope carries the failure
alone. A rekordbox playlist made and paired before the failure, and the pairs
written before it, are in no item and no warning.

**Measured cost.** Driven by the second review with three account playlists
brought over and the second failing: the first fully synced, the second
paired with no snapshot, the third not made, and the envelope reported none of
it. Nothing false is said and nothing is lost; the next sync converges.

**Closes when:** the verb answers a failure with the pairs it wrote before
it. Ledger only.
