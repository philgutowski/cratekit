---
title: Three verbs convert a stored level by their own copies of the tag reader's rule
found: at the review of #679, U250, 2026-11-12.
issue: no
---

**The mechanism.** U250 made `tags.whole_number` the one conversion the energy
and vocal readers and `rebuild.read_truth` take from a stored level's text to a
number. Three copies of the same rule stand outside it, each written before it:
`_as_level` in `src/cratekit/analysis/cli.py` (`crate analyze restamp`),
`_as_level` in `src/cratekit/vocals/cli.py`, and `_as_int` in
`src/cratekit/modules/tools/setbuilder.py`, which strips the text first. Round
two of the review drove all three against `whole_number` over 17 values (None,
padded, decimal, underscore, non ASCII digits, NUL, hex) and all four agree
today.

**Measured cost.** None today. A change to `whole_number` (a decimal read as its
whole part, say) would leave those verbs reading a stored level the old way
while routing reads it the new way, and no test compares them.

**Closes when:** each copy calls `tags.whole_number`, or is deleted for it.
Ledger only: out of U250's scope, which named the derivation's three readers.
