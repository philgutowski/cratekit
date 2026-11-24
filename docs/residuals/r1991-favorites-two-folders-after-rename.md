---
title: After a genre folder adopt apply recorded is renamed, the next adoption into a band the record lacks binds the genre to two folders and favorites refresh leaves both alone
found: at the review of #1022, R-1991, 2026-11-23.
issue: no
---

**The mechanism.** `adopt apply` finds its playlists by display name, so after
a rename it files a band the record lacks into a new folder bearing the
genre's name, and now records that playlist (R-1991), beside the renamed
folder the record already binds for another band. The genre's bucket is then
bound to two folder rows, and `genre_favorites` refuses to choose between
them.

**Measured cost.** Driven at round one with the real verbs: after the second
apply the `favorites refresh` gate shows "folders left alone: 2", each named,
and that genre's Favorites are not written until the two folders are merged
by hand. On the same chain the base files eight tracks into the second folder
and the branch two; the same tear is reachable on the base through a rebuild.

**Closes when:** adoption resolves a destination through the record's folder
for its bucket before it falls back to the display name, as
`_under_recorded_folders` does for Favorites. Ledger only: the gate names both
folders and a hand merge ends it.
