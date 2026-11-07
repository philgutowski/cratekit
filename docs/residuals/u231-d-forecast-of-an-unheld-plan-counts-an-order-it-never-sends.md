---
title: The gate's forecast for a plan that could not be held counts the account order calls a write that keeps no record never makes
found: at the review of #595, U231, 2026-11-07.
issue: no
---

**The mechanism.** Since round one's fix a write that keeps no record sends
no order (`_write_account`), but `_expected` still counts the order's
reading, moves and settle reading when `steps` is None.

**Measured cost.** Driven by round two's review (C2): `_expected` answered
ten write calls on the owed pair while the write sent none. A number too high
on the gate's provider calls line, on a run that then stops naming why.

**Closes when:** `_expected` leaves an order out when the plan is not held.
Ledger only.
