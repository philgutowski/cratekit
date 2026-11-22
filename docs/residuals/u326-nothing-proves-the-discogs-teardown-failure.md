---
title: Nothing proves the Discogs detonator's teardown failure, which is the only failure it raises
found: at the mutation table of #932, U326, 2026-11-22.
issue: no
---

**The mechanism.** `_no_live_discogs` in `tests/conftest.py` (U283) records
each address a test sends to the live Discogs API through the shipped getter,
raises `ConnectionError`, and fails the test at teardown over what it
recorded. The teardown failure is the whole guard: setup folds a transport
failure into an unreachable answer and stores the token, so the raise alone
fails nothing. U326's row R5 replaced `if reached:` with `if False:` and the
full suite, 22,933 tests, killed nothing. Unchanged by U326.

**Measured cost.** Not driven past the row. A test that reached the live API
by mistake would pass with the token stored and a note, which is the outcome
the guard's docstring says it exists to prevent.

**Closes when:** a test in a file #869 (U312) owns drives a setup step with
the shipped getter under the guard and asserts the test fails, in a pytester
run as `tests/test_host_process_table.py` does for the process tripwire.
Ledger only.
