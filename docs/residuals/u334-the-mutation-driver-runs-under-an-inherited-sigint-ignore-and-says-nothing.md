---
title: The mutation driver runs under an inherited SIGINT ignore and says nothing, so an interrupt guard's kill reads zero
found: at the kill set replay of #983, U334, 2026-11-24.
issue: no
---

**The mechanism.** `scripts/mutate.py` and `scripts/cloud_battery.py` measure in whatever signal dispositions their process inherited. Started under `nohup` and a shell's `&`, SIGINT is ignored, every pytest child and every pool worker inherits that, and a mutant that removes `src/cratekit/core/pool.py`'s own `signal.signal(signal.SIGINT, signal.SIG_IGN)` in the stream worker survives `tests/test_pool_stream.py::test_the_terminals_interrupt_does_not_kill_a_stream_worker`. Neither the table nor its markdown records the disposition, so the zero reads as a lost kill.

**Measured cost.** One row of 2,592 in U334's replay, `u241.M01_worker_takes_the_interrupt`, read zero in after batch 4 and was measured again as a one row batch, killed on both sides. Maintainer facing: a false loss costs a re-measure, and a false zero on a new row would read as a guard nothing kills.

**Closes when:** the driver records the SIGINT disposition it measured under and refuses, or resets SIGINT to the default before its first run, when the inherited one is ignored, with a test that starts it so. Ledger only: maintainer facing.
