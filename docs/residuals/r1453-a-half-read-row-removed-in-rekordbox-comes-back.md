---
title: A rekordbox removal of a row the account lists as one unread release and one readable is undone once the unread release reads
found: at the review of #643, R-1453, 2026-11-09.
issue: no
---

**The mechanism.** `plan_pair` in `src/cratekit/sync/pair_cli.py` takes every
release of a removed track off the account (U208), but reads those releases
from `account_now`, the readable ids alone, so a row held as two releases, the
first listed with no title and the second read, loses only the readable one
when the person removes the row in rekordbox. The unread release stays on the
account, the snapshot moves holding it, and its link to the row is kept. Once
the provider lists it with its title again, the merge reads it as held on the
account since the last sync and never in rekordbox, and adds the row back to
rekordbox. It is R-1287's mechanism, an unread track never taken off either
side, reaching a row R-1264 counts as readable, which R-1287's entry does not
name.

**Measured cost.** Driven on the twins world by round one of the review: the
R-1453 removal test's state (row four held as t4 and t24, t4 untitled, row four
removed in rekordbox, two syncs) leaves the account listing t4; with t4's title
served again, the next sync plans a rekordbox addition of t4 and rekordbox goes
from 3, 1, 2 back to 3, 4, 1, 2, and stays so over two more syncs. The person's
removal is reversed with nothing said. The producer on the account, one row
listed as two releases with the first unread and then corrected, is unmeasured
(R-1264, R-1287). The removal test leaves t4's staying unasserted so it does not
pin the defect; the brief's "the account drops the row" is met for the readable
release only.

**Closes when:** a rekordbox removal of such a row takes its unread release off
the account by id too, or the snapshot keeps the unread release out of the
account's base until it reads; R-1287's close would close this one with it.
Ledger only: its producer is unmeasured, as R-1287's is.
