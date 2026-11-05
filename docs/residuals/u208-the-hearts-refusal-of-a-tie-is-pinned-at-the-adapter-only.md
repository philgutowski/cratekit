---
title: The hearts' refusal of a tie between agreeing releases is pinned at the adapter and through the favourites sweep, and nothing asserts the hearts never pass any_agreeing
found: at the review of #498, U208, 2026-11-05, round one.
issue: no
---

**The mechanism.** U208 lets the pairs pass `any_agreeing` to
`match_track`. The hearts (`modules/outbound/hearts.py`) must not; the
refusal is pinned by the adapter test without the flag and by the favourites
sweep over `_releases_for_three_rows` in `tests/test_outbound_tidal_account.py`,
whose row 2 is the tie. No test watches the hearts path's own call for the
flag.

**Measured cost.** None today: grep finds no `any_agreeing` in hearts.py,
export.py or set_cli.py, and the branch does not touch them. Reachability of
a regression unmeasured; no mutation of hearts.py was run.

**Closes when:** a test drives a heart over a tie with a recording fake and
asserts the flag absent, or a mutation of hearts.py passing it is killed.
Ledger only.
