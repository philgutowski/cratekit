---
title: The invariant set guard reads comprehensions only and a few spellings of a set, so the same rebuild in another form passes it
found: at the review of #675, U246, 2026-11-12.
issue: no
---

**The mechanism.** `tests/test_comprehension_sets.py` refuses a set built anew
per element from names that do not vary, in a comprehension's condition or as
the set a membership test in its element tests against. It does not read a
`for` statement's body, nor the iterable of a comprehension's second or later
`for` clause, which is also evaluated once per outer element. Round one's
wider walk over the 336 modules found one live instance of the first kind:
`modules/outbound/hearts.py`, around line 89, builds a set comprehension over
the constant `REMOVE_FLAGS` once per flag key it tests.

Round two probed sixty shapes; besides those two it still passes `{*ys}`,
`set().union(ys)`, `dict(pairs)`, `collections.Counter(ys)`, `{**a, **b}`, a
set operation or method on the set in an element (`a in set(ys) | extra`,
`set(ys).isdisjoint(x.tags)`), and a lambda handed to `filter` or `sorted`
outside a comprehension. It still flags three that vary: a walrus bound name,
`set(next(it))` and `set(queue.pop())`. Some of its own lines kill none of its
self tests (round two's table: a lambda's keyword only parameters, the vendored
exclusion, a walk that skips modules, which a clean tree cannot pin).

**Measured cost.** Not measured. The hearts loop runs over the flags of one
command line, so its size is a handful; nothing on a library sized path was
found in any of these shapes; a wider scan of the 315 modules found the
eleven sites on `main` and none on the branch.

**Closes when:** the guard reads a `for` statement's body and a later `for`
clause's iterable with the same free name rule, and the hearts loop builds its
set once. Ledger only: a maintainer facing cost.
