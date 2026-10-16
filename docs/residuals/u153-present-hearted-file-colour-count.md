---
title: A landing's gate overstates the Pink count and omits a held note for a hearted file already present and coloured
found: at the review of #334, U153, 2026-10-16.
issue: no
---

**The mechanism.** The native landing's `_favorites_plan` reads each row's
colour only for the owned hearts (`joining`), not for the hearts items
(`kept`). A hearts item whose target is already a row in the collection, an
action `PRESENT` row rather than a new `ADD` one, can carry a colour a person
set by hand. `favorites_facts` counts `len(plan.items) + len(plan.colour)` as
the rows to colour, so the gate screen counts that present row among the Pink
writes, and at apply `placement.place` builds `to_colour` from every item's
`by_target` row, where `colour.write_pink` correctly declines to overwrite the
colour. The row is held and never reported, because `held` is computed only
from the owned hearts.

**Measured cost.** None to the library: the write is fill only on every path,
so a colour a person chose is never overwritten, driven by the suite. The cost
is to the operator's gate screen, which can promise one more Pink write than
the commit delivers, and to the held report, which omits a present row it left
alone. Not driven: a hearted file that lands `PRESENT` over an existing
coloured row was not reproduced, so the reachability is unmeasured. In the
common case every hearts item is a new, uncoloured row, so the count is exact.

**Closes when:** `_favorites_plan` reads the colour of a present item's
existing row the way it reads an owned heart's, folding an uncoloured one into
the colour set and a coloured one into `held`, and `favorites_facts` counts
only the rows actually to be coloured. Ledger only unless a present coloured
hearted file is driven and shown to mislead, which would meet board bar (b).
