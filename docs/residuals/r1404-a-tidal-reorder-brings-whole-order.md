---
title: Outside GIG READY a Tidal reorder after a rekordbox reorder brings Tidal's whole stale order into rekordbox
found: at the review of #608, R-1404, round one, 2026-11-07.
issue: no
---

**The mechanism.** Outside GIG READY the account's order is never written (U231), so once rekordbox leads a reorder the pair's snapshot holds rekordbox's new order and the account's old one, and since R-1404 rekordbox keeps leading while neither side moves. When the account then changes order since that snapshot, `pair_merge.merge` lets the account lead and its whole order stands, the tracks it never moved included, since the merge places a whole order and has no reading of a move.

**Measured cost.** Driven by the round one reviewer through the dispatcher on the disposable database: a hand pair at the root of 1 to 5, rekordbox reordered 5, 4, 3, 2, 1 and synced (nothing written), then tracks 1 and 2 swapped on the account: rekordbox becomes 2, 1, 3, 4, 5. The gate says "order follows the account's" before it writes, so it is said, not silent. It is the card's own scenario ("the account reordered to 2, 3, 1 should still lead rekordbox") and U231's recorded call, kept as built; a merge of the account's moves alone would leave that scenario's rekordbox at 3, 1, 2.

**Closes when:** Phillip answers the Question for Phillip on #608: keep it as built (then this closes as decided), apply only the moved tracks, or never take the account's order into rekordbox outside GIG READY (either a card of its own). Ledger only until he answers.
