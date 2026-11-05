---
title: The account's added date of a playlist track was read off the client's parse, never off a live listing
found: at the build of #490, U202, 2026-11-05.
issue: no
---

**The mechanism.** U202 reads when the account says each playlist track was
added from the `date_added` the provider's client copies off a playlist item's
`dateAdded`, as its own comment says playlist items carry. No live listing of
the author's playlists was read from the container, so whether the tracks
endpoint the listing walks serves the date, and whether reordering a playlist
on the account moves it, were not observed.

**Measured cost.** Not driven. With no date, every call is unknown and keeps
the track, named on the gate, which is the rule before U202. If a reorder
moved the date, a track reordered on the account and taken out in rekordbox
since the last sync would be kept and named rather than taken off.

**Closes when:** the attended sitting lists one paired playlist live, reads a
date on every track, reorders one track on the account and lists it again.
Ledger only.
