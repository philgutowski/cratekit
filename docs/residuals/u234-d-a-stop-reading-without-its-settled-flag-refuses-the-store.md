---
title: A pair's reading after a stop with no settled flag makes the whole pairs store unusable
found: at round two of the review of #623, U234, 2026-11-07.
issue: no
---

**The mechanism.** `PairStore._stop_reading` in `modules/outbound/pairs.py`
refuses a `stop_seen` record missing `settled`, and one unusable pair refuses
the store, as every other malformed field of a pair does. The shape without
it was written only by this branch's commits before its first fix round,
never on `main` or in a release.

**Measured cost.** Driven by the branch's own parametrized test, which
asserts the refusal. No store of that shape is known to exist, so nobody
pays it; a store written by an unmerged commit of a cloud branch would need
the field added by hand.

**Closes when:** never needed while no such store exists. Ledger only.
