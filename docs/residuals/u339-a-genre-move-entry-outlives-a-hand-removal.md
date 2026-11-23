---
title: A genre move entry outlives a membership taken out by hand, so a later hand placement in the old folder is moved again
found: at the build of #988, U339, 2026-11-23.
issue: no
---

**The mechanism.** `tag set` records, in `adopt/genre_moves.py`, the bucket each row's old genre filed it in, and the entry is spent only when an `adopt move` job reads the row back out of that bucket. When the person takes the track out of the old genre folder in rekordbox before `adopt move` runs, no move is planned, so the entry is never spent. If the person later puts the same track in that folder by hand, as a second genre folder (U340), the next `adopt move` plans a move taking it out again.

**Measured cost.** Not driven past reading: the move is shown at `adopt.move.approve` with the folder it leaves, so it is never made unseen, and the person can decline it. Nothing is lost without a gate.

**Closes when:** an entry is spent when the plan finds the row holds nothing in its old bucket, or entries carry the date and expire, with a test placing a track back by hand after the entry is moot.
