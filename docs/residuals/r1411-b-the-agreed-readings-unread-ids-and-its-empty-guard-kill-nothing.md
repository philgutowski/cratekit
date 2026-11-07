---
title: Which reading a finish is held to is pinned only for readable tracks, and its guard for an empty reading kills nothing
found: at the review of #613, R-1411, 2026-11-07.
issue: yes
---

**The mechanism.** `_write_account` in `sync/pair_cli.py` passes
`one.account_before` as the agreed reading of a finishing order, the
listing with its unread ids in place (`listed_order`). Holding the finish to
`one.account_now`, the readable tracks alone, survives every test of the
seven files the card touched (164), and so does dropping the clause
`and one.account_before`, which only a held plan from before U225 could
reach.

**Measured cost.** None on the branch. Round two drove the mutation to
`account_now` on a scratch copy: rekordbox 4, 2, 1, 3 with t3 unread on the
account, a stop after one move (account 3, 1, 2, 4), the check and the
adapter serving the lag 1, 2, 3, 4. On the branch the finish is refused
with nothing moved; under the mutation the agreed reading is 1, 2, 4, the
lag passes, and the moves leave 2, 4, 1, 3 for an asked 4, 2, 3, 1 under
exit 0, reported written. The branch's code is right; the guard is
reached by no test.

**Closes when:** a verb test drives a finish over a playlist with an unread
track whose first stopped move was that track, refused from a lag and
finished once served as the move left it. Earns an issue: a guard on a path
that writes kills nothing.
