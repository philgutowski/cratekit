---
title: A track hearted on the account and put in an older month, landed into another month, reads that landing's month as a change made in rekordbox
found: at the review of #579, U227, 2026-11-06.
issue: no
---

**The mechanism.** U227 reads a landing's own filing as the landing's only in
the genre rule (`mirror_edits._decide_genre`, with `filed`). The Favorites
rule's later change path (`_decide_favorites` through `_later`) has the same
shape. Suppose a track the library lacks is put in month `2026-10` on the
account and is also hearted, and its landing then places it in All Favorites
and `2026-11` as a heart of the pass. The next refresh reads `2026-11` as
rekordbox's later change, keeps it, and the mirror takes the track off
`2026-10` on the account.

**Measured cost.** The rule was driven over `decide` by Fable's round one: the
result is REKORDBOX, "placed in Favorites 2026-11 in rekordbox at ..., so
rekordbox's place stands". The producer, a hearts landing whose month differs
from the one the person chose, was not driven, so reachability is unmeasured.
It is outside the card's genre scope.

**Closes when:** a landing's placed hearts (the landing record's
`placement.PLACED_KEY`) are handed to the Favorites rule as `filed` is to the
genre rule, and a test drives the month case. Ledger only.
