---
title: A database put back outside Cratekit leaves no restore record, so a landing it rolled back into a playlist already there can be offered
found: at the build of #913, R-1037, round one's B1 followed one file over, 2026-11-21.
issue: no
---

**The mechanism.** The pass sets aside every landing a `capture-restore`
session started after (`deletion.run._not_restored_since`), because a restore
takes a landing's rows away as a removal does. A database copied back by hand,
or put back by rekordbox's own backup restore, writes no Cratekit record. Then
only two guards are left: the landing's playlists must still be in the
database, and the first sighting must come at an update count past the
landing's own commit. A landing into a batch playlist that was already there,
put back outside Cratekit, and then passed by the count before any review,
meets neither.

**Measured cost.** Not driven, since the producer is a hand copy or rekordbox.
The cost would be an offer at the explicit gate of a file whose row nobody
removed, which a trash answer moves into the Trash with a tombstone; the Trash
keeps it and `tombstone list --revoke` undoes the tombstone.

**Closes when:** a fact a removal keeps and any rollback takes away is found
in the database (an attended comparison of a removal against a restore), or
the landing records whether it made each playlist and the pass offers nothing
of a landing into a playlist that was already there. Ledger only: it needs a
producer outside the product.
