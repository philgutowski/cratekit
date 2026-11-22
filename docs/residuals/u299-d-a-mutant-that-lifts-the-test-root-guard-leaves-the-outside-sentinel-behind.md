---
title: A mutant that lifts the test root guard leaves the suite's outside sentinel on the machine, and every later run there fails eight tests and reads false kills
found: at the kill set replay of #856, U299, 2026-11-22.
issue: no
---

**The mechanism.** `tests/test_config_test_root.py` points its writes at
`OUTSIDE`, `/cratekit-r926-outside-every-test-root`, and asserts the refusal
left nothing there. A row that disables the guard in `core/config.py`
(`r926.G1_never_checks` is one) lets the write land, so the directory is left
holding `config.toml`, its migrate lock, `ledger.json` and `session.lock`.
`scripts/mutate.py` guards the two state roots under the home directory and
nothing else, so the directory outlives the row. On U299's replay, slice 3
met it twice: every later row whose subset held that file read eight extra
deaths from it (`u254.C2_append_one_write`, whose own recorded killer still
died), and the after pass's baseline refused, eight tests red, until the
directory was removed by hand.

**Measured cost.** None to a user. To a replay, a row after the culprit that
lost its real kill can still read killed from the eight sentinel tests, and
the next batch on the same container refuses at its baseline. U299's check
read each affected row's kills by name.

**Closes when:** the driver includes the sentinel in what it guards and
restores (or the test removes what an escaped write left, in a finalizer),
so no row's verdict depends on the rows before it. Ledger only.
