---
title: A pair whose two account tracks carry one ISRC honours a rekordbox removal of their row only half
found: at the review of #330, U149, 2026-11-01.
issue: no
---

**The mechanism.** When two tracks of an account playlist carry one ISRC, both are linked to the one library row, by the twins' backfill and equally by `sync pair`'s own `_owned`. `plan_pair` maps a row back to one remote id only, so when that row is taken out of the rekordbox playlist, the next `sync pair` takes one of the two account tracks off and adds the row back to rekordbox, since the other account track still holds it.

**Measured cost.** Driven by the review on a fake account: account `[t1, t10, t2]` with `t10` carrying `t1`'s ISRC, the row removed in rekordbox, and the sync removed `t10` from the account and put the row back. The removal a DJ made in rekordbox is undone. How often the live account lists one recording twice under two identifiers was not measured.

**Closes when:** a pair links each row to at most one account track, or reads a removed row as removing every account track linked to it. The class predates U149 in `sync pair`; ledger only until a live listing shows it.
