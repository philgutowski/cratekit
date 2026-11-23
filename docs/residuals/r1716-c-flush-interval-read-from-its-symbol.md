---
title: The held reads' flush interval kills no test, since the one test of it reads the interval from the symbol
found: at the mutation table of #1010, R-1716, 2026-11-23.
issue: no
---

**The mechanism.** `sync/removed_kept.py` writes the held reads every
`FLUSH_EVERY` (50) changes and on the way out. Row K19 of
`docs/mutation/r1716.md`, `FLUSH_EVERY` at 500, killed none of 22,995: the
test of the interval counts to `FLUSH_EVERY` itself, and every verb test
ends its run, which writes the store on the way out.

**Measured cost.** None to a person: the interval bounds what a killed
process loses, at most that many reads to be read again, and the way out
writes the rest. Maintainer facing.

**Closes when:** a test pins the interval at 50 by number, or holds that a
process killed after 60 new reads leaves at least 50 written. Ledger only.
