---
title: tag set reads a row on a padded or retired namesake of the genre as already carrying it, and makes a live row beside it
found: at the review of #1008, R-1967, round one, 2026-11-23.
issue: no
---

**The mechanism.** `plan_set` in `tagging/genre_set.py` decides `already-that-genre` by the row's genre name stripped (`collection.genre_of(row).strip()`, through the binding's association proxy, which reads a tombstone's name too), and decides the mint by `metadata.resolve_genre_id`, an exact name and an active row only. A named row linked to a lookup row named the genre with a trailing space, or to a tombstone of the genre, reads `already-that-genre` while the plan mints, and the apply makes a live row of the genre beside the one that row keeps.

**Measured cost.** Driven by the reviewer on a hand built library: row 10 on an active row named "Afro House" with a trailing space, and again on a tombstone of "Afro House"; `tag set "Afro House"` over rows 10 and 11 made the row, linked row 11, left row 10 where it was, and the next plan read both `already-that-genre`. The producer is unmeasured: one candidate was driven (a native landing of a file whose genre tag carries a trailing space, which minted the name unpadded and did not produce it), rekordbox itself was not driven, and the tombstone link was built by a hand UPDATE. Reading a tombstone linked row as carrying the genre predates R-1967; what R-1967 adds is the live row made beside it.

**Closes when:** the plan reads a row as carrying the genre only when it links the genre's active row, or refuses the mint while a named row links a lookup row whose stripped name is the genre, with the padded and the tombstone namesakes as its tests. Ledger only, since no producer is driven.
