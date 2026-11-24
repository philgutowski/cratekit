---
title: One case of the sync pair merge fold runs the same merge as another
found: at the review of #984, U335, 2026-11-24.
issue: no
---

**The mechanism.** `test_the_side_that_leads_the_order` in `tests/test_sync_pair_merge.py` holds the cases `with_no_change..._leads_again-rekordbox` and `the_stopped_writes_order_is_not_read_against_the_base-stopped` with identical parameters. The base ran the same merge in the two tests they were folded from, so the fold kept every assertion and one case is redundant.

**Measured cost.** One merge run twice, under a millisecond; no guard lost.

**Closes when:** one of the two cases is given the input its base test's name describes, or the two are named as one. Ledger only.
