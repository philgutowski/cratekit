---
title: A later pair raising outside an order's own refusals after an earlier pair's moves went out skips the settle reading of every order sent
found: at the review of #595, U231, 2026-11-07.
issue: no
---

**The mechanism.** `sync_pair` reads every order sent once all pairs are
written (`_settle`). A later pair whose write raises anything that stops the
whole write leaves the loop before `_settle`, so an earlier pair's order is
not read, no reading is kept on it, and no pending warning names it.

**Measured cost.** Driven by round one's review (T2d): the carried record
held `moving` and `moved`, no move was sent again, the pair was held two
runs and finished on the run after the provider caught up. One extra run
while the provider lags; the state is honest.

**Closes when:** the settle runs in a `finally` that cannot itself mask a
park, or the stop names the pairs whose order it did not read. Ledger only.
