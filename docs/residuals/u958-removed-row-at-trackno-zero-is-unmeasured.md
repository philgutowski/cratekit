---
title: A membership row this product marks removed is put at TrackNo 0, and what rekordbox does with a marked row at 0 is unmeasured
found: at the build of #1058, U958, 2026-11-24.
issue: no
---

**The mechanism.** `rb_positions.close_gaps`, run by `commit_guarded`, numbers
the live rows of every playlist a membership removal touched 1 to N and moves
every row marked `rb_local_deleted` 1 in that playlist to `TrackNo` 0, its
`TrackNo` alone, so no marked row shares a place with a live one. `crate
repair numbers` does the same over the playlists it plans. Sitting 107 (A218)
showed rekordbox leaving a marked row at 55 out of the shown positions, so a
marked row is not counted as a place; nothing measured rekordbox reading,
syncing or removing around a marked row at 0. A row at 0 was chosen because
rekordbox's Remove from Playlist takes the row numbered as the shown position,
which is never 0, and a marked row left on its old number would share a place
with the live row closed up onto it.

**Measured cost.** Not driven against rekordbox, which no cloud session may
open. On fixtures every reader in src skips a marked row, and `add_memberships`
appends past the highest number over every row, so 0 changes no append.

**Closes when:** the attended card's hand removal reads a playlist the repair
closed up, holding a marked row at 0, before and after, and rekordbox removes
the selected track and leaves the marked row as it was. Ledger only: it closes
only at an attended sitting.
