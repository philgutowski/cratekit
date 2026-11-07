---
title: The pair verb's tests of the agreed order decide their stand in's refusal by the adapter's own rule
found: at the review of #613, R-1411, 2026-11-07.
issue: no
---

**The mechanism.** `_adapter_reading` in `tests/test_sync_pair_settle.py`,
the stand in for the adapter's order the verb tests drive, imports
`_in_agreed_order` from `modules/outbound/tidal_account.py` to decide
whether to refuse. So the verb tests judge the agreed rule by the rule
itself: a wrong rule that happens to pass the reading a test chose would not
be seen at the verb.

**Measured cost.** None today. Round one's mutation of `_in_agreed_order` to
always true killed 7 tests, 5 in the adapter's file and 2 in the verb's
through their end state assertions, so the rule is pinned, only not
independently at the verb.

**Closes when:** the verb tests' stand in refuses on readings written out by
hand per test, or drives the real adapter over a fake provider. Ledger only:
a maintainer facing test shape.
