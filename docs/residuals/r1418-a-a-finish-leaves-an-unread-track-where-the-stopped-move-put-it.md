---
title: A finish of a stopped order leaves an unread track where the stopped move put it, not where the stopped write was taking it
found: at the build of #618, R-1418, 2026-11-07.
issue: yes
---

**The mechanism.** `_with_unread_placed` in `src/cratekit/sync/pair_cli.py`
puts each unread track back behind the track the account lists before it
now. A write stopped part way through its order may already have moved an
unread track, and the plan that finishes it places that track by where the
stopped move left it, since nothing of the stopped write's target is read
for an unread id. So the finish makes the interrupted move permanent for the
one track the merge cannot read.

**Measured cost.** Driven by
`test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
in `tests/test_sync_pair_settle.py`: the account lists t1, t2, t3, t4, then
t9 with no title; rekordbox's 2, 3, 4, 1 asks 2, 3, 4, 9, 1, whose first
move puts t9 in front; the write stops there and the finish, once served as
the move left it, leaves t9, t2, t3, t4, t1, t5, where the stopped write's
own target put t9 behind t4. Every readable track is in rekordbox's order and
no track is lost or added; the cost is the place on the account of one
track rekordbox does not hold, which the gate the person answered shows as
planned. Not driven: whether a person notices or minds.

Pre-existing on main since U225 and R-1264; this branch changes no
behaviour, and its own scenario is the producer.

**Closes when:** the plan of a finish places an unread track the stopped
write moved from that write's target. It earns an issue under the board
bar's (a): the account playlist's order is the person's, and a track
Cratekit moved and cannot read is left where its interrupted move put it,
reported finished.
