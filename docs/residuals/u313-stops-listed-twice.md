---
title: mutate.py's stops are listed twice, in STOPS and in main's except tuple, and the test of their exit codes lists them a third time by hand
found: at the review of #870, U313, round two, 2026-11-22.
issue: no
---

**The mechanism.** `scripts/mutate.py` maps each exception that stops a batch to its heading and exit code in `STOPS`, and `main` catches them with an `except` tuple written out by hand beside it. `test_each_stop_exits_with_its_own_code` in `tests/test_mutation_driver.py` lists the same four stops by hand too. A stop added to `STOPS` and not to the tuple would escape `main` as a traceback instead of exiting with its code, and the test would still pass: the review added a fifth stop with code 7 to `STOPS` in a scratch copy and the test passed 5 of 5.

**Measured cost.** None today: no such stop exists, and every exit code that exists is held by the test (each swapped code fails it). It is the seam shape of two lists that must agree.

**Closes when:** `main` catches `tuple(STOPS)` and the test is parametrized over `STOPS` itself plus the invalid batch, so a new stop is caught and held without a second edit. Ledger only; it was found after the unit's two fix rounds were spent.
