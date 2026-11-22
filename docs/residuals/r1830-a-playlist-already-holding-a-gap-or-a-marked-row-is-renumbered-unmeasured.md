---
title: A playlist already holding a gap or a row marked removed below a removed track is renumbered by a rule rekordbox was not measured on
found: at the build of #925, R-1830, 2026-11-22.
issue: no
---

**The mechanism.** Sitting 102 (A197) measured one shape: a playlist made by
hand at `TrackNo` 1, 2 and 3, every row live, the middle track removed. #925
applies the binding's rule (`rb_writer.renumbered_positions`) to every
playlist the removal leaves: each surviving row above a deleted row goes
down by one per deleted row below it, a row marked `rb_local_deleted` 1
counting as a row and moving with the rest, and a gap an earlier removal
left staying a gap (1, 2, 3, 5 with 2 removed reads 1, 2, 4). Cratekit's own
INBOX playlists hold both shapes: U288's removals before #925 left gaps, and
the INBOX rotation and `intake analyzed` soft delete memberships in live
playlists. Whether rekordbox closes every gap, renumbers only its live rows,
or leaves a marked row's number, was not measured. Nor was how far
`localUpdateCount` moves for a renumbering, or whether the renumbered row's
`updated_at` and `rb_local_usn` stayed byte for byte (the sitting's words
are "otherwise unchanged", read here as every column but `TrackNo`).

**Measured cost.** Not driven against rekordbox. Every number stays distinct
and in its order, so the order rekordbox shows is the order before, and the
next append still goes past the highest position.

**Closes when:** an attended sitting reads, on copies before and after a
Remove from Collection, a playlist holding a gap below the removed track, and
the renumbered row's every column, and the rule is kept or given what
rekordbox does. Ledger only.
