---
title: The same band move made in both genre folders on the account is held on every run
found: at the review of #989, U340, 2026-11-23.
issue: no
---

**The mechanism.** The account's edit rule (`modules/outbound/mirror_edits.py`)
reads a track added to two band playlists at once as not saying which one it
belongs in, before U340's `_second_genre_tags` is asked. A two folder track
moved Low to High in both Deep House and Tech House on the account is the
natural edit, and it is held.

**Measured cost.** Driven at round one over three runs: listed as held each
time, "added on the account to 2 band playlists at once"; the library stays
in Low and Low, the account in High and High. Undoing one of the two on the
account lets the other through and both folders move. Nothing is lost or
written; the reason does not fit a track that belongs in both.

**Closes when:** the rule reads two band additions in the two folders of a
track's genre and second genre as one band move. Ledger only.
