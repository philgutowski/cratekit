---
title: tag second ignores a --leave identifier that matches no chosen row without a word
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** `tagging/second.py` holds out a chosen row named by
`--leave` and says nothing about an identifier that matches none. `tag rows`
carries its unmatched ones as a warning (`rows-leave-unmatched`).

**Measured cost.** Driven at round one: `tag second "Melodic House"` on row t3
with `--leave nope` showed held-out 0, no warning, and t3 planned as a write.
A mistyped identifier writes a row the person meant to hold.

**Closes when:** the verb warns as `tag rows` does. Ledger only.
