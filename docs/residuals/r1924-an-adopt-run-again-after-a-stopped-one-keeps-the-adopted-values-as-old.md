---
title: An analyze adopt run again after one that stopped among its files keeps the adopted tags as its old ones
found: at the review of #970, R-1924, 2026-11-23.
issue: no
---

**The mechanism.** An adopt stopped after its files and before its rows
leaves the files adopted and the rows old (R-1925). Run again, the adopt plans
the rows and keeps, as each file's before value, the tags the stopped run
wrote. A restore of the second run is faithful to its capture: the rows go
back and the files keep the adopted tags, since that is what they held before
it. Only a restore of the stopped session, discarding the second, puts both
sides back, and no answer names that session.

**Measured cost.** Driven at review round one: stopped adopt, adopt again
(exit 0, 5 rows), `restore run` of the second: exit 0, ok, 5 of 5 read back,
rows old and files adopted. `restore run` of the stopped session with the
second discarded put every surface back.

**Closes when:** the adopt's answer after a stopped run names the stopped
session as the one whose restore undoes both, or the adopt takes its before
values from that session's record. Ledger only; it closes with R-1925.
