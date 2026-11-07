---
title: An order that is not a finish still plans its moves from a reading checked by membership alone
found: at the review of #613, R-1411, 2026-11-07.
issue: no
---

**The mechanism.** R-1411 holds only a finish of a stopped order to the
plan's reading (`one.finishing_order` in `_write_account`). A fresh order,
or one after additions and removals, still plans its moves from the
adapter's reading checked by what it holds (`_settled`), so a provider
serving an older order of the same tracks seconds after the plan's reading
has the moves sent by position from it, as R-1411's cost was.

**Measured cost.** Not driven. Whether the provider serves an order older
than the plan's to a reading seconds later, outside a stopped write, rests
on Sitting 86's reads 3 seconds apart disagreeing 28 minutes after moves.
The mutation passing the plan's reading at every order survives every test
(row W5 of `docs/mutation/r1411.md`), so the scope limit is pinned by
nothing either way.

**Closes when:** every order write is held to the plan's reading, or a
measurement shows the provider never serves an older order to a reading
after the plan's outside a stopped write. Ledger only until driven.
