---
title: The fixture rows test's check that every row is stamped reads two columns the binding fills itself, so it guards nothing
found: at the review of #685, U256, 2026-11-12.
issue: no
---

**The mechanism.** `tests/test_fixture_database_template.py::test_a_copy_carries_the_rows_the_safety_chain_reads`
asserts that no row of the four fixed tables has a null `created_at` or
`updated_at`. The binding gives both columns a default of its own, so they
are filled whether or not `_row` stamps them, and the check leaves out
`agentRegistry.date_1` and `date_2`, the only stamp columns `_row` has to
fill, which fail at the insert when unfilled.

**Measured cost.** None to a person. Round two drove three mutants of
`_row`: skipping both columns and skipping `updated_at` alone killed nothing,
and skipping `date_1` and `date_2` failed at the insert before the clause was
read. A reader may think the stamps are guarded by the clause when they are
guarded by the binding.

**Closes when:** the clause is removed, or rewritten to say what it holds.
Ledger only.
