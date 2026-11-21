---
title: A playlist or history list that keeps other tracks keeps the gap a removed track's TrackNo leaves, and what rekordbox does there is unmeasured
found: at the build of #839, U288, 2026-11-21.
issue: no
---

**The mechanism.** A178 and A185 each removed a track alone in its playlist and
its history list, so neither measured whether rekordbox renumbers the
`TrackNo` of the members after a removed one. The binding's own
`remove_from_playlist` renumbers them; Cratekit's soft delete of a membership
never has. The removal renumbers nothing, so an INBOX playlist holding the
other tracks of the pass keeps a gap where the removed one was, and the
confinement refuses any renumbering as a change it did not plan.

**The next append collided, fixed in round one.** Review round one drove it: `rb_writer.add_memberships`
appends through the binding's `add_to_playlist`, which numbers a new row as
the row count plus one. After a removal INBOX / Analyze held 1, 2, 3, 5, and
the next landing put its new track at 5 beside the live one already there;
without the removal it went to 6. `add_memberships` now numbers an append past
the highest position the playlist holds, so the gap stays a gap.

**Measured cost.** Not driven against rekordbox. A gap is what every soft
deleted membership has always left in a live playlist, and rekordbox orders a
list by `TrackNo`, so the order shown is unchanged; whether rekordbox reads a
gap as anything else is the measurement.

**Closes when:** an attended sitting removes one track from a playlist and a
history list holding others with Remove from Collection, compares the copies,
and the removal imitates what it finds. Ledger only: it closes at a sitting.
