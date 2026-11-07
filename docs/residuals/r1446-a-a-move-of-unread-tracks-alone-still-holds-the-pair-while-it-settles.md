---
title: A move of unread tracks alone after a settled reading still holds the pair while it settles, under a line saying the account's order will be read as yours
found: at the build of #639, R-1446, 2026-11-07.
issue: no
---

**The mechanism.** `_moved_since_stop` in `src/cratekit/sync/pair_cli.py`
still compares the readings kept after a stop over every id the account
lists, an unread one (R-1264) included, so a person who moves only an unread
track after a sync read the account settled is held by U234's
`sync-pair-account-settling` refusal, problem `order-moved-since-stop`, until
a reading at least `AGREE_AFTER` later agrees. Only then does `plan_pair`
ask whether a readable track moved (`_readable_moved`) and, finding none,
finish the stopped write. The hold's line says that once a later reading
agrees "the account's order is read as yours", which is true of the unread
track's place and not of the readable tracks' order, which the finish puts
in rekordbox's.

**Measured cost.** Driven by the card's own test
(`test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`):
the pair is left out of two syncs before the third finishes it, nothing
written while it waits and rekordbox's order kept after. A delay and a
hold line that overstates what the person's move will do; no order is lost.
Kept deliberately: the card requires the stop with its rekordbox side
skipped to keep today's result, whose existing test pins those two holds.

**Closes when:** a settled change that moves only unread tracks is read
without the hold, or the hold's line names that only tracks the account
cannot read moved. Ledger only: a wording and a delay, nothing lost.
