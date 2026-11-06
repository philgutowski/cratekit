---
title: A window that starts lagging between the sync pair plan and its write stops every pair's write as moved
found: at round one of U226's review (#578), 2026-11-06.
issue: no
---

**The mechanism.** `crate sync pair`'s plan holds a pair whose account
window lags a partial unpaged read (`sync-pair-account-lagging`) and syncs
every other pair. The check before the write reads the same lag as a moved
list (`pair_cli.check`), and a moved list stops the whole write as
`decision-stale` with nothing written, as any list moved since the plan
does.

**Measured cost.** Driven at round one through the verb: two pairs planned
clean, the second's window lagging from inside the check, exit 11, "1
list(s) moved since the plan ... nothing was written", the first pair's add
unwritten too. A fresh `crate sync pair` a few minutes later is the way on,
as the answer and the guide say. The producer, a partial unpaged read whose
window starts lagging in the seconds between plan and check, was not driven
live.

**Closes when:** the check leaves a lagging pair out of the write as the
plan does, the rest written, if a sitting shows the lag reaching the check.
Ledger only: the run refuses with nothing written and names the way on.
