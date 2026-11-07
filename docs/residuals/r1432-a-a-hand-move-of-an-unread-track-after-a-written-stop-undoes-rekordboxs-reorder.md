---
title: A person's move of an unread track after a stop whose rekordbox side was written lets the account lead and undoes rekordbox's reorder
found: at the review of #630, R-1432, 2026-11-07.
issue: yes
---

**The mechanism.** `plan_pair` in `src/cratekit/sync/pair_cli.py` reads the
account as standing on a stopped write's path only when every track the
listing and the write's start share stands where the write's moves could
have left it (`pair_stopped.reached`), and an unread track (R-1264) is one of
those. So a person who drags an unread track the stopped write had moved
takes the account off the path, and the account leads as a reorder. Where
the stopped write also committed rekordbox, the plan folds it into the base,
and the account's order, the stopped write's half done order of the readable
tracks with the person's one move, is put into rekordbox.

**Measured cost.** Driven by Fable's round one review of #630 (its D1), the
same on main: the account t1 to t4 then untitled t9, rekordbox reordered to
2, 3, 4, 1, a write stopped after its first move put t9 in front, rekordbox
written. The person drags t9 between t2 and t3; the next sync is left out
waiting for readings to agree, the one after writes under
`sync-pair-finishing`: the account t1, t2, t9, t3, t4 and rekordbox 1, 2, 3, 4.
The DJ's rekordbox reorder, which the stopped write was carrying, is undone
by a move of a track rekordbox never held. Not driven: whether a person
reads the gate's finishing line before applying it.

**Closes when:** a move of an unread track alone after a stop is read as
the person's move of that track and not as a reorder of the readable ones,
so the stopped write still finishes the readable tracks' order; or the gate
names that the account's lead comes from an unread track alone. It earns an
issue under the board bar's (a): a playlist order the DJ made in rekordbox is
written over.
