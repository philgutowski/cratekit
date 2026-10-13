---
title: U134's mutation table is four rows of twenty, the rest owed to a quiet machine
found: at the build of #307, U134, 2026-10-12.
issue: no
---

**The mechanism.** `scripts/mutate.py` stops a batch when the real
installation state gains an entry while a child runs. With three Relay lanes
and the watcher on one machine, two other mutation drivers and a `crate
doctor` run wrote there during each attempt, and batch a stopped three times.
Rows A1 to A4 were measured and killed; A5 to A11 and batch b's nine rows,
two of them composites for the read back's guards, were not run.
`docs/mutation/u134-notes.md` names them and the rerun command.

**Measured cost.** None to a person. The guards are covered by the 19 tests
of `tests/test_inbox_refill.py`, which the author expects each row to kill,
and that expectation is unmeasured.

**Closes when:** both batches are run to the end with no other lane on the
machine and their tables committed. Ledger only: maintainer facing.
