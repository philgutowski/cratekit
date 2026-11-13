---
title: An aware value from the binding would pass the date seam unclamped
found: at round one of the review of #800, U285, 2026-11-13.
issue: no
---

**The mechanism.** `core/rb_dates.placeable` hands an aware answer on as it
came, since comparing it with the naive bounds would raise `TypeError`. An
aware year 1 value would then overflow in the next reader that converts it.

**Measured cost.** None reachable: pyrekordbox 0.4.4, pinned by
`assert_binding_version`, never answers an aware value, so the branch is dead
for the shipped binding and its mutation row is killed only by a test double.

**Closes when:** a binding upgrade that answers aware values clamps them in
their own zone. Ledger only.
