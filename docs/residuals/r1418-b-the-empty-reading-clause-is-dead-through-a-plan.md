---
title: The clause that passes no agreed reading for an empty plan reading is dead through a plan, and is pinned only by a synthetic stand in
found: at the review of #618, R-1418, 2026-11-07.
issue: no
---

**The mechanism.** `_write_account` in `src/cratekit/sync/pair_cli.py`
passes `agreed` at a finish only when `one.account_before` is not empty. The
block runs only under `if one.account_order`, and a plan with nothing listed
appends its additions in the merged order, so `wanted_keys` equals `firsts`
and the plan asks no order: no plan reaches the clause with an empty
reading. For the real adapter it is also equivalent, since an empty agreed
order holds a reading to nothing. Kept rather than dropped, because dropping
it changes the write guard with no failing test to prove it.

**Measured cost.** None. Four producers of a finish with an empty reading
were driven, the author's and the review's: the account emptied after the
stop with tracks added in rekordbox, only the unread track left on the
account, every account track unread under a rekordbox reorder; each asked no
order. A held plan from before U225 cannot carry `finishing_order`. Sibling
releases and R-1376's first sync stop argued from source only. The unit test
`test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading` pins the
clause on a hand built plan with an adapter stand in that takes no `agreed`,
the only such stand in in the tree, so it dies by a signature and not a
behaviour. A reader may believe the clause protects something.

**Closes when:** the clause is dropped by a unit that changes the account
write anyway, or a plan is found that reaches it. Ledger only, a maintainer
facing guard.
