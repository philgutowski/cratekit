---
title: Test slice 1 ends 3.5 percent smaller, not 14, because structure alone gives no more
found: at the build of #981, U332, 2026-11-24.
issue: no
---

**The mechanism.** #981 asked slice 1 of the test tree (the 200 files from
`tests/__init__.py` to `tests/test_catalogue_app.py` in path order, 73,259
lines at `55e958b`) to end at or under 62,155 lines, so the four slices
together bring `tests/` under point 5's bar of 249,132. Eight builders cut it
by Phillip's answer A on #847: parametrize folds, shared setup within a file
or a support file of the slice, deleting a test only where another checks all
it checks, and prose cut to the rule and its reason. They reached 70,702 by `scripts/refactor_measure.py lines`, 2,557
lines fewer. Every builder stopped short and measured why (1.6 to 7.0 percent
per group): the tests left are distinct end to end scenarios whose setup
differs test to test; a table of strings is as long as the tests it would
replace; the prose left is almost all one line reasons, residual titles and
decisions; and 5,189 lines are not the card's to cut (`tests/conftest.py`,
`tests/_pending.py`, the reserved cause pins). About 13,600 of the slice's lines
are blank, mostly the two between top level definitions. The cuts that would
reach the number are formatting (dropping those blank lines, joining calls
already split over lines) or deleting tests that still guard something, and the
card took neither. R-1941 measured the same wall across the whole suite.

**Measured cost.** None to a person using the verbs. Point 5 of #847 stays
unmet by about 8,547 lines in this slice; the question on #981 asked Phillip
how to treat the miss, and the card took the recommended option, land with
the miss named.

**Closes when:** the audit card after the four slices (#987) settles point 5,
by a decision to accept what structure gives, to lower the bar, or to count
lines another way. Ledger only: maintainer facing.
