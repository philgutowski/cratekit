---
title: analyze adopt's half read warning counts the notes of rows it left beside the rows that took half an answer
found: at review round one of #994, U342, 2026-11-23, on code the branch did not change.
issue: no
---

**The mechanism.** `analysis/head_adopt_cli.py`, `_half`: the warning names
only rows that took half of rekordbox's answer, but its bracket prints
`plan.notes`, the notes of every row, left ones included.

**Measured cost.** Driven at review round one: a mixed plan said `1 row(s)
took only half of rekordbox's answer (3 key-empty, 1 tempo-zero)`, the two
extra notes from rows left as `no-head-unanswered`; a copy of the base gives
the same sentence with a `no-head` and a `no-reference` row. A count in a
warning that overstates; nothing is written or lost.

**Closes when:** the bracket counts the notes of the rows it names. Ledger only.
