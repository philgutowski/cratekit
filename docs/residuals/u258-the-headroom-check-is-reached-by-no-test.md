---
title: The at risk test's headroom check over the widened key set is reached by no test
found: at the review of #687, U258, 2026-11-12.
issue: no
---

**The mechanism.** `test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
in `tests/test_reserved_causes.py` asserts that adding every kebab shaped
literal in the package to the key set reports no offender outside the two
table owners. No test plants a module that reaches it: the suite's only
planted run of the at risk test, in `tests/test_parse_memo.py`, plants a table
whose new kebab literals move a pin earlier in the same test. Running the check
over an empty population (row M10 of `docs/mutation/u258.md`) kills no test, on
the branch and, by the review's hand mutation, on `main` before it: the gap
predates U258. The round two review drove two plants that do reach it, a new
module holding `{"cancelled": 30}` (a declared cause that is not kebab shaped,
so no kebab pin moves) and `{"auth-failed": 30}` appended to
`acquire/adapter.py` (which already pins that literal): each fails first at the
headroom assertion, and with the check emptied each is still caught later, by
the literal holder pin and the named with integer pin. So the check is
unreached by the suite, and redundant with later pins for those two plants.

**Measured cost.** Maintainer facing. The check guards an argument in a
residual's prose, not a verb.

**Closes when:** a test runs the at risk test over the package plus a one line
plant like `{"cancelled": 30}` and sees it fail at the headroom assertion.
Ledger only.
