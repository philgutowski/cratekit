---
title: The empty identifier guard in first_stop is an equivalent mutant, so its pure assertion pins nothing
found: at the review of #597, R-1376, round one, 2026-11-07.
issue: no
---

**The mechanism.** `_Reader.first_stop` answers None for an empty account playlist identifier before it looks the stop up, but the lookup `stopped[0].get("")` answers None anyway, since no stop is keyed by an empty identifier.

**Measured cost.** Maintainer facing: the reviewer's row removing the guard killed no test of 84. None at the verbs.

**Closes when:** the guard is dropped, or kept as documentation with this line. Ledger only.
