---
title: Nothing pins the order of the source guards' walk, so a guard that came to depend on it would pass a reordered walk
found: at the review of #932, U326, 2026-11-22.
issue: no
---

**The mechanism.** U326 replaced `ast.walk` and `ast.iter_child_nodes` in
`tests/_source_guards.py` with `_walk` and `_children`, exact equivalents in
the same breadth first order, checked by identity at every position over
3,951,477 nodes of 1,365 files from `src`, `tests` and the standard library.
The review then drove a depth first `_breadth_first` and a `_children` that
reverses its children: both killed nothing across the guard files and the
two beat grid suites, because every consumer today reduces a walk to a set,
`any` or `sorted`. A later guard that stops at the first match would depend
on the order with nothing to say so.

**Measured cost.** None today, by the review's mutants.

**Closes when:** a test beside the guards (a file #869, U312, owns, since
U326 added no tests) asserts `_walk` and `_children` agree with `ast.walk`
and `ast.iter_child_nodes` node for node over a fixture tree with list,
single and missing fields. Ledger only.
