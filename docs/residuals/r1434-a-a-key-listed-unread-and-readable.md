---
title: A row the account lists as one unread release and one readable is counted as readable by no test
found: at the mutation table of #631, R-1434, 2026-11-07.
issue: yes
---

**The mechanism.** `plan_pair` in `src/cratekit/sync/pair_cli.py` takes the
unread keys as `{alias(remote_id) for remote_id in unread} - readable_keys`
(R-1264), so a row held as two releases, one the provider lists with no
title and one it reads, is a readable row: it is ordered by the merge, kept in
the base, and read as taken off when it is. Without the subtraction the row is
unread: left out of the order the merge asks, stripped from the base, and its
removal on either side is not read.

**Measured cost.** Row S4 of `docs/mutation/r1434.md`, the subtraction
dropped, killed none of 17559 tests on the full suite; its composite, no
track unread at all, is measured in the same table, so the unread set is
pinned and its narrowing to rows with no readable release is not. What a
person pays was not driven: no test builds a row matched to two releases
(U208) whose first the provider lists unreadably, and the producer on the
account is unmeasured.

**Closes when:** a verb test syncs a pair whose account lists one row as an
unread release and a readable one, reorders or removes that row in rekordbox,
and shows the account follows; dropping the subtraction then fails it. It
earns an issue under the board bar's (d), a guard on a path that writes kills
nothing.
