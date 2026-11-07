---
title: A pair outside GIG READY reordered in rekordbox has its order put back to the account's two syncs later
found: at the review of #597, R-1376, round two, 2026-11-07.
issue: yes
---

**The mechanism.** Since U231 (#595) a pair whose rekordbox playlist is not under GIG READY never has its account order written (`_keeps_order`, unless `outbound.pair_order_every_pair`). A reorder made in rekordbox leads the next sync, which writes nothing on the account and moves the snapshot, so the snapshot holds rekordbox's new order and the account's old one. On the sync after, neither side has changed order since that snapshot, `pair_merge.merge` lets the account lead by default, and the plan writes the account's old order into rekordbox.

**Measured cost.** Driven on main at 1cadb924 with no R-1376 code: a pair made by hand of an account playlist 1, 2, 3 and a root rekordbox playlist 1, 2, 3, the rekordbox playlist reordered to 3, 1, 2; the next sync answers `sync-pair-nothing` and leaves 3, 1, 2; the one after answers `sync-pair-written` and rekordbox holds 1, 2, 3 again. A DJ's reorder of any paired playlist outside GIG READY is undone in the library with nothing said. It is also the way a stopped write's scramble still reaches rekordbox for a pair released and paired again at the root (R-1376): that pair's first sync keeps rekordbox's order and leaves the account in the scramble, and the next sync writes the scramble into rekordbox (driven on the merged branch).

**Closes when:** a sync of a pair whose account order is not kept never writes rekordbox an order the account did not change to since the snapshot, and the root case is driven through the dispatcher. It meets the board bar: a person using the shipped verbs pays it, a write into the library.
