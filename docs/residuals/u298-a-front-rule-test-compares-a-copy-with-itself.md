---
title: The front rule's copy test in tests/test_sync_pair_stopped.py compares a function with itself since the copy became a call
found: at the review of #855, U298, 2026-11-21.
issue: no
---

**The mechanism.** `tests/test_sync_pair_stopped.py` holds 25 tests, a permutation over four tracks and a track held twice, that assert `pair_stopped.front_moves` equals `tidal_account._to_the_front`. U298 made `_to_the_front` a call of `front_moves`, so each test now asserts that a function equals itself, and no mutation of the rule can fail them.

**Measured cost.** None to a run, and the rule is still held: the review mutated `== 1` to `>= 1` in `front_moves` and 29 other tests failed, among them `tests/test_outbound_order.py` and `tests/test_sync_pair_settle.py`. What is lost is 25 tests that test nothing, named for a copy that is gone.

**Closes when:** the sync area card deletes the 25 tests or turns them into assertions of the rule's own answers. Ledger only.
