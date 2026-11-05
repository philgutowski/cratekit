---
title: A pair's tie broken in favour of a release the account already holds is counted on the gate's line and in totals but named on no item
found: at the review of #498, U208, 2026-11-05, round one.
issue: no
---

**The mechanism.** `sync/pair_cli._items` marks `tied: True` only on account
add items. A tie whose chosen release is already on the account adds nothing,
so the row is counted in the facts line and `totals.tied` and appears on no
item.

**Measured cost.** Driven by the review: account holding 101 and 202 before
the first sync, the facts line says one row matched by a tie and no item
carries the flag, so a reader of the gate cannot find which row. Nothing is
written wrong.

**Closes when:** the gate names the tied rows themselves, for instance as the
facts line's list, with a test. Ledger only.
