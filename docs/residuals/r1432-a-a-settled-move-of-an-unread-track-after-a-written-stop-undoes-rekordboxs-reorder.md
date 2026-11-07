---
title: A move of an unread track alone, read settled after a stop whose rekordbox side was written, lets the account lead and undoes rekordbox's reorder
found: at the review of #630, R-1432, 2026-11-07.
issue: yes
---

**The mechanism.** `plan_pair` in `src/cratekit/sync/pair_cli.py` finishes
a stopped write whether the account stands on its moves' path or off it
(U225, U234), until readings kept after the stop show the order changed
since a sync read it settled (`_moved_since_stop`). Those readings compare
every track the account lists, an unread one (R-1264) among them, so a
person who moves only an unread track, which neither side's merge reads,
is read as reordering the account. The plan then finishes nothing, the
account leads, and its readable tracks, still in the stopped write's half
done order, are put into rekordbox.

**Measured cost.** Found by Fable's round one review of #630 (its D1) on the
base before U234, where the first reading off the path already led. Driven
again on the branch with U234 merged in: the account t1 to t4 then untitled
t9, rekordbox reordered to 2, 3, 4, 1, a write stopped after its first move
put t9 in front, rekordbox written. The person drags t9 between t2 and t3;
plans read that settled, and the person drags it between t3 and t4. Two
syncs leave the pair out while the change settles, and the third writes
under `sync-pair-finishing` ("reordered since syncs after the stop read it
settled"): rekordbox 1, 2, 3, 4 and the account t1, t2, t3, t9, t4. The DJ's
rekordbox reorder, which the stopped write was carrying, is undone by moves
of a track rekordbox never held. With the stop's rekordbox side skipped,
rekordbox leads and keeps its order (the branch's test of that case). Not
driven: whether a person reads the gate's line before applying it.

**Closes when:** a settled change of order that moves only unread tracks is
not read as a reorder of the readable ones, so the stopped write still
finishes their order; or the gate names that the account's lead comes from
unread tracks alone. It earns an issue under the board bar's (a): a playlist
order the DJ made in rekordbox is written over.
