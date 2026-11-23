---
title: Ten recorded kills on sync's files read zero on the base U304 replayed, four of them noise and six lost before it
found: at the kill set replay of #861, U304, 2026-11-23.
issue: no
---

**The mechanism.** `killset.py rows` read 658 live rows for `src/cratekit/sync/`, each recorded as killed by its own table. Replayed on `c9192091`, before U304's first edit, ten read zero even promoted to the full suite (`docs/mutation/u304-replay-before.md`). Four were recorded as killed only by a test that has nothing to do with the row: `r1376.F15_null`, `r1411.W5_agreed_at_every_order` and `r1446.M10_kept_order_with_unread` by the inode bound test of #702 (`test_repair_rows.py`), which fails on a container's disk by itself, and `r1372.K18_let_go_on_any_record` by a set inspiration backfill test, each after promotion. Their recorded kill was the machine's, not the mutation's. Six were killed by sync's own tests when recorded and are not now: `r1372.K16_no_let_go_at_done`, `r1376.F2_first_stop_empty_id`, `r1376.F8_fold_on_first_sync`, `r1411.E3_refused_order_passes_no_expect`, `u130-a.A1_removal_beats_addition` and `u130-b.B3_account_isrc_not_first`. Some later change to those tests or that code, before `c9192091`, stopped them killing.

**Measured cost.** None to a person today. The six are guards no test holds: a plan that folds on a first sync (`F8`), a removal that beats an addition (`A1`), an account ISRC read out of order (`B3`), and three narrower ones. U304 kept every kill that stood on the base, and these were not standing.

**Closes when:** each of the six is read against its test as it is now, and either a test kills it again or a line says why it is equivalent; the four noise rows are marked in the kill set so `killset.py rows` stops offering them. Ledger only.
