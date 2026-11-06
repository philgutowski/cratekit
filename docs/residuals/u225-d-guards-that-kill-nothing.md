---
title: Five guards U225 added to the stopped order read kill no test
found: at the reviews of #577, U225, rounds one and two, 2026-11-06.
issue: no
---

**The mechanism.** Each was mutated alone by the reviewers and the U225 test files stayed green:

- `plan_pair`'s folded base takes the stopped write's moment as its sync time (`synced = stopped_write.at if folded`); no scenario dates a change between the old snapshot and the stopped write's begin.
- `_Reader.stopped_write` returns None for a pair with no record (`held is None`) or a write with no begin time; neither input was produced.
- `_Reader.stopped_write` drops the stopped write when the snapshot's time cannot be read; the pair store always writes `timestamp()`.
- `stopped_writes` picks the latest stopped write by its ordering time, not its begin; the two differ only for a continue that fails before its order beside a second stopped run.
- `_write_account`'s start falls back to `account_now` for a plan held before U225, and `stopped_writes` compares a finish to a begin with `>`, where microseconds make `>=` the same.

**Measured cost.** None measured: 0 candidates were driven that reach a different outcome.

**Closes when:** a test reaches each, or the guard is removed as dead.
