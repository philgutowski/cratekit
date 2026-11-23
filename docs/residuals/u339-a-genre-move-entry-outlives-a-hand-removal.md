---
title: A genre move entry outlives a membership taken out by hand, so a later hand placement in the old folder is moved again
found: at the build of #988, U339, 2026-11-23; driven at its review round one.
issue: no
---

**The mechanism.** `tag set` records, in `adopt/genre_moves.py`, the genre folder the tree files a written row in under its old genre, and the entry is spent when an `adopt move` job reads the row back out of that folder, or when a later `tag set` gives the row that folder's genre again. Review round one drove three producers of an entry nothing spends, a row the tree did not hold in its old folder, a genre moved there and back, and a genre moved twice; the fix round records a folder only where the tree holds the row and spends an entry a row is given back, which closes the first two, and round two's fix spends every folder a track leaves in one job, which closes the third and a fourth round two drove (a track leaving two folders in one job spent one entry). Left: when the person takes the track out of the old folder in rekordbox before `adopt move` runs, no move is planned and the entry stays, and a later hand placement of the track in that folder, as a second genre folder (U340), is planned for removal.

**Measured cost.** The removal a stale entry plans is shown at `adopt.move.approve`, naming the folder it leaves, so it is never made unseen; a person approving without reading it loses that one placement. Review round one drove the removal with the placement seeded through `rb_writer`, since a hand placement in rekordbox cannot be driven here.

**Closes when:** an entry is spent when the move plan finds the row holds nothing in its folder, read on the worker's own pass, with a test placing a track back by hand after the entry is moot.
