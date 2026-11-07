---
title: The ordering step's start keeps a pair's unread ids, and no test kills dropping them
found: at the mutation table of #618, R-1418, 2026-11-07.
issue: yes
---

**The mechanism.** `_write_account` in `src/cratekit/sync/pair_cli.py`
records the ordering step's start from `one.account_before or
one.account_now`, the plan's whole reading with its unread ids (R-1264).
`pair_stopped.stopped_write` reads that start only for a write with no
moving step, one that stopped after its ordering step and before its first
move was sent; every other stopped write starts from the moving step's own
record. A start without the unread ids leaves them out of `reached` and
`positions`, which compare only the tracks the start and the listing share,
so where an unread track stands is not read when the next plan decides
whether the account stands on the stopped write's path.

**Measured cost.** Row F7 of `docs/mutation/r1418.md`, the start recorded
from the readable tracks alone, killed none of 17440 tests on the full
suite. Its composite, a stopped write with no moving step read with no
start at all, killed 4 on its subset, so the start is read and pinned; its
unread ids are not. What a person pays was not driven: no sync was built
that stops between the ordering step and the first send with an unread
track a person then moves.

**Closes when:** a verb test stops a write before its first move over a
playlist listing an unread track, moves that track, and shows the next plan
reads the move as the person's; or the start is shown not to need the
unread ids. It earns an issue under the board bar's (d), a guard on a path
that writes kills nothing.
