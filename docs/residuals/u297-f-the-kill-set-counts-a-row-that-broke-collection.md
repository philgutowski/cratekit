---
title: killset.py list counts a row that broke collection and recorded a death as a recorded kill, 24 of 8,541, while check ranks it under one
found: at the review of #854, U297, round one, 2026-11-21.
issue: no
---

**The mechanism.** The reader calls a row killed when its table recorded at
least one death, which is the rule the survey of U290 used and what
reproduces its 8,541 and its 7,093 live rows. 24 of those rows have the
status `collect-error`: the mutation broke an import, the collected count
moved, and the driver says of such a row that it is neither a zero nor a
clean kill. `rows` writes the 20 of them that are live into a replay, and
`check` ranks one under a kill: it holds it to no less after than before,
and reports a clean kill that became one.

**Measured cost.** An area card's replay holds up to 20 rows across the tree
whose before measurement is a collection error, each held only to staying
one. Counted, never driven on a card.

**Closes when:** U315's audit says which the definition of done means, or
the 20 are measured and those that break collection for a reason of the
row's own making are dropped from the set. Ledger only.
