---
title: A removal gives every renumbered row one count, the final one, and rekordbox was read on one row of one playlist
found: at review round one of #1002, U955, 2026-11-23.
issue: no
---

**The mechanism.** `CollectionRemoval.commit` stamps every membership row it
renumbers, in every playlist and for every removed track, with one
`rb_local_usn`, the removal's final `localUpdateCount`, and one `updated_at`.
A202 at sitting 104 read rekordbox 7.2.19's own Remove from Collection on one
moved row in one playlist, whose count equalled the final count. That fits
both one count on every moved row and successive counts ending at the final
one, and nothing measured several moved rows, several playlists or several
removed tracks at once. The confinement admits only the shape this product
writes.

**Measured cost.** Not driven against rekordbox, which no cloud session may
open. Driven through the verb on the `one_offered` fixture: 7 rows in 3
playlists moved, all holding the one final count. If rekordbox numbers them
apart, the library differs from rekordbox's own state in the count of rows
rekordbox itself does not read for playback.

**Closes when:** an attended sitting reads rekordbox's removal of one track
with two survivors after it on each of two playlists, column by column on two
dated copies, and the stamp rule is kept or changed to match. Ledger only: it
closes only at an attended sitting.
