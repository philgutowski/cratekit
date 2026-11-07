---
title: Two pairs listing two releases of one recording still queue it twice in one sync pair command
found: at the review of #600, R-1385, 2026-11-07.
issue: no
---

**The mechanism.** R-1385 keeps a track queued once by its remote id: `_Reader.asked` and `_Reader.held_by_jobs` in `src/cratekit/sync/pair_cli.py` are keyed by the account's track id. Two pairs listing two releases of one recording, two ids carrying one ISRC, each plan an `acquire`, and so does a pair beside another pair's job holding the other release.

**Measured cost.** Driven by round one's review: pair A listing `t40` and pair B listing `t41`, both coded `USZZZ2600040`, queued two jobs in one command with no awaiting row. Whether the second job downloads a second copy or resolves owned by the first file's ISRC when it runs was not driven. `main` behaves the same.

**Closes when:** the plan also keys what is asked and held by ISRC, as U208 aliases releases by ISRC within one pair. Ledger only until a second copy of one recording is seen in the library.
