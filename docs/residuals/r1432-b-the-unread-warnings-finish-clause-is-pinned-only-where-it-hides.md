---
title: The unread warning's finish clause asks the pair to write an order, and no test kills dropping that
found: at the mutation table of #630, R-1432, 2026-11-07.
issue: no
---

**The mechanism.** The `sync-pair-unread` warning in
`src/cratekit/sync/pair_cli.py` adds that a pair finishing a stopped order
puts each unread track where that order was taking it only when a pair with
an unread track both finishes a stopped order and asks the account an order
(`finishing_order and account_order`). A finish that asks no order moves
nothing, so the clause would say a move that is not made.

**Measured cost.** Row P11 of `docs/mutation/r1432.md`, the condition on an
account order dropped, killed none of 17493 tests on the full suite. Its
composite, P10, the clause never shown, killed 1, and the round two test
pins the clause absent on a plan that finishes nothing; what is not built is
a finishing plan with an unread track and no order to write, such as a
pending order whose end the account already shows. Not driven: whether such
a plan shows the warning at all.

**Closes when:** a verb test finishes a stopped order that asks no account
order over a playlist listing an unread track and reads the warning without
the clause. Ledger only: a wording guard.
