---
title: "rekordbox's Remove from Playlist takes the row whose TrackNo equals the shown position, so a playlist with a gap loses the wrong track"
date: 2026-11-24
category: database-writes
module: "src/cratekit/core/rb_nodes.py, src/cratekit/core/rb_removal.py"
problem_type: binding_quirk
component: rekordbox_write
severity: high
resolution_type: workflow_change
applies_when:
  - "A track is removed from a playlist by hand in rekordbox, by an attended session or by Phillip"
  - "The playlist's live rows are not numbered 1 to N, a gap left by a product removal (the soft delete keeps TrackNo) or by anything else"
tags: [rekordbox, TrackNo, djmdSongPlaylist, remove-from-playlist, renumber, r-1853, u958, a218, sitting-107]
---

## The trap

rekordbox shows a playlist's rows at positions 1 to N whatever their stored
`TrackNo`. At sitting 107 BY GENRE + ENERGY / Tech House / High held 556 live
rows numbered 1 to 557 with 548 missing. The throwaway A218 one, at `TrackNo`
557, showed at position 556. Remove from Playlist on it, from its own row
menu, removed What Da Hell, the row at `TrackNo` 556. rekordbox then
renumbered the live rows 1 to 555, so a second removal at the same sitting
took the right row. One observation, read from the database before and after.

## How common it is

On the live library on 2026-11-24, 45 of 737 playlists held live numbers that
were not 1 to N, 39 of them under BY GENRE + ENERGY. 589 of the 773 missing
positions were held by a row this product marked removed
(`rb_nodes.remove_memberships` keeps `TrackNo`, R-758 and R-1853), 184 by
no row.

## What U958 changed

- Every removal this product makes closes its playlist up at the commit:
  the live rows 1 to N in the order rekordbox shows them, the removed rows at
  0, proven from SQL (`rb_positions.close_gaps`, run by `commit_guarded`).
- `crate repair numbers` numbers the playlists older removals left gapped,
  and `crate doctor`'s `library.playlist_numbers` line counts them.
- Until the repair has run on a library, a hand removal in a playlist the
  doctor line names may still take the wrong row: read the playlist again
  after, against a copy taken before. To put a wrongly removed track back,
  use the row menu's Add To Playlist; it appends at the end.
- What rekordbox does with a removed row at `TrackNo` 0 is unmeasured; the
  attended card reads it.
