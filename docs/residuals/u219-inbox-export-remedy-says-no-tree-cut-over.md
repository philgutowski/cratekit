---
title: route inbox on a library whose only native tree is the intake tree says no tree has cut over
found: at the review of #537, U219, round one, 2026-11-05.
issue: no
---

**The mechanism.** Since U219 `route inbox` files into the routing tree only,
so on a library where the intake tree has cut over and the routing tree has
not, its planner finds no routed tree and carries the export remedy, whose
first clause is "no tree has cut over". The resort says `no-derivable-tree`
for the same library, which is true.

**Measured cost.** Driven on a registry with `inbox` native alone: the
warning reads "no tree has cut over". The sentence's remedy, the export path,
is still the right one, so a person is sent the right way with one false
clause. Not measured on a real library mid cutover; the author's library has
both trees native.

**Closes when:** the export remedy says the routing tree has not cut over,
which is true in both cases, with `tests/test_routing_workers.py` and the
`r695` rows that spell it moved with it.
