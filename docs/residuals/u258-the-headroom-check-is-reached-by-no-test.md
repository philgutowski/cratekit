---
title: The at risk test's headroom check over the widened key set is reached by no test
found: at the review of #687, U258, 2026-11-12.
issue: no
---

**The mechanism.** `test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
in `tests/test_reserved_causes.py` asserts that adding every kebab shaped
literal in the package to the key set reports no offender outside the two
table owners. On the tree that dictionary is empty whatever population it is
computed over, and every planted module that would make it non empty first
moves a kebab literal pin, which fails earlier in the same test. Running the
check over an empty population (row M10 of `docs/mutation/u258.md`) kills no
test, on the branch and, by the review's hand mutation, on `main` before it:
the gap predates U258.

**Measured cost.** Maintainer facing. The check guards an argument in a
residual's prose, not a verb.

**Closes when:** a test drives the check over a planted population whose pins
are supplied with it, or the check is moved to a test of its own that a plant
can reach. Ledger only.
