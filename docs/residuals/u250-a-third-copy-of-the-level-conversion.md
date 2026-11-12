---
title: crate analyze restamp converts a stored level by its own copy of the tag reader's rule
found: at the review of #679, U250, 2026-11-12.
issue: no
---

**The mechanism.** U250 made `tags.whole_number` the one conversion the energy
and vocal readers and `rebuild.read_truth` take from a stored level's text to a
number. `_as_level` in `src/cratekit/analysis/cli.py` is a third copy of the
same rule, written before it and still standing. Today the two agree: `int` of
the text, None for an absent value and for one that is not a number.

**Measured cost.** None today. A change to `whole_number` (a decimal read as its
whole part, say) would leave `crate analyze restamp` reading a stored level the
old way while routing reads it the new way, and no test compares the two.

**Closes when:** `_as_level` calls `tags.whole_number`, or is deleted for it.
Ledger only: out of U250's scope, which named the derivation's three readers.
