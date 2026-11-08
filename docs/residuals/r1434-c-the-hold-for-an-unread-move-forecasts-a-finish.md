---
title: The hold for a move of an unread track forecasts a finish that a title served since makes untrue
found: at review round two of #631, R-1434, 2026-11-08.
issue: no
---

**The mechanism.** `_moved_since_stop` in `src/cratekit/sync/pair_cli.py`
holds a pair off the stopped write's path by a track the plan cannot read,
and its message ends that the track stays where the person put it and the
others are finished in the stopped order. That is the outcome only while the
track stays unread: when the provider serves its title before the move
settles, the next plan reads the move and the account's order leads, by the
rule for a track read since the stop.

**Measured cost.** Driven by the review (test 3's setup, t9's title served
after the hold): the hold's forecast, then the account leads and rekordbox
takes 1, 2, 9, 3, 4. The outcome is the rule's; only the forecast the person
read is stale. A wording finding, so no issue.

**Closes when:** the hold says what follows while the track is unread and
that a title served since lets the account's order lead, or the plan holds
its forecast to the reading that settles it.
