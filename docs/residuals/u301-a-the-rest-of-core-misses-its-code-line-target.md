---
title: The rest of core ends a fifth smaller in lines but misses its code line target by about 550
found: at the record of #858, U301, 2026-11-22.
issue: no
---

**The mechanism.** #858 asked the rest of core (`core/review.py`, `jobs.py`,
`pool.py`, `provider_gate.py` and ten smaller modules, with the parts split
from them) to end at or under 10,816 lines and 5,771 code lines. Measured by
`scripts/refactor_measure.py lines` on the merged head it ends at 10,113 lines,
met, and 6,323 code lines, about 550 over. The cut came from prose, which
Phillip allowed on #847, from folding copied steps into helpers, and from the
duplication; what is left is mostly code a recorded mutation kill anchors byte
for byte, refusal and message text that is output, and the import lines the
splits added (each part imports what it reads from its parent and the parent
imports it back).

**Measured cost.** None to a person: behaviour is frozen and compared base
against branch. The cost is point 2 of #847's audit, which reads code lines
as well as lines.

**Closes when:** the final audit (#872) reads the epic's totals; a further
cut of these modules' code would have to rewrite anchored guards and carry
their kills by hand, which is a card of its own if the audit wants it.
Ledger only.
