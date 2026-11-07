---
title: A hand pair's first sync outside GIG READY puts rekordbox in the account's order
found: at the review of #608, R-1404, round one, 2026-11-07.
issue: no
---

**The mechanism.** A first sync has no base, and `pair_merge.merge` lets the account lead on it, as every first sync always has (U130); R-1376's `test_a_first_sync_of_an_account_playlist_with_no_stop_is_planned_as_before` pins it. Outside GIG READY the account's order is never written afterwards, so a rekordbox playlist paired by hand in its own order takes the account's at its first sync and never gets its own back.

**Measured cost.** Driven by the round one reviewer: a hand pair of an account playlist 1, 2, 3 and a rekordbox playlist 3, 1, 2 with the key off; the first sync writes rekordbox 1, 2, 3, the gate saying the order follows the account's. Unchanged by #608, the same on main.

**Closes when:** Phillip answers the second question on #608; keeping it closes this as decided. Ledger only.
