---
title: The mutation driver's controller only write guard kills no test, because every worker write is followed by one of the controller's
found: at the review of #680, U251, 2026-11-12, and measured as row W4 of its mutation table.
issue: no
---

**The mechanism.** The reporting plugin that `scripts/mutate.py` writes into
each child run returns from `_flush` in an xdist worker (`if _IS_WORKER: return`),
so only the controller writes the report. With the guard gone, a worker writes
only when it finishes collecting and when one of its own tests fails; it
collects the whole suite, so its count is right, and the controller writes
again after every report a worker forwards, so the controller's write is the
last one. Row W4 of `docs/mutation/u251.md` removed the guard: zero kills on
`tests/test_mutation_driver.py`, and zero on the promoted full run of 18,551.
The review drove the same in memory: 8 of 8 stealing runs and every parallel
driver test passed.

**Measured cost.** None found. No run was produced in which a worker's write
lands after the controller's last, so the guard holds against a race nothing
here provokes.

**Closes when:** a fixture makes a worker write after the controller's last
write (a worker failure in its teardown after the controller has written,
for instance) and a test fails without the guard, or the guard is shown to be
unneeded and removed with its docstring. Ledger only.
