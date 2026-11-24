---
title: A playlist whose live rows read 1 to N while a row marked removed holds one of those places is never planned by the repair
found: at the review of #1058, U958, round two, 2026-11-24.
issue: no
---

**The mechanism.** `crate repair numbers` plans only a playlist whose live rows
are not 1 to N, as the card asks ("a contiguous playlist is never written").
A row marked removed that shares a live place (rekordbox's own renumbering
after a hand removal leaves one, sitting 107: a marked row at 55 under live
rows renumbered 1 to 555) is moved to 0 only when a product add or removal
next touches the playlist; until then the doctor row reads OK. `read_back` and
`gap_violations` would call the same state a failure, since they judge a
playlist the repair or a removal wrote.

**Measured cost.** Driven on the repair suite's fixture: a playlist 1, 2, 3 with
a marked row at 3 plans nothing and the doctor reads OK. Whether rekordbox's
Remove from Playlist can take a marked row that shares the shown position's
number is unmeasured.

**Closes when:** the attended card's hand removal reads such a playlist, or the
repair plans a playlist with a marked row on a place. Ledger only.
