---
title: After every move of an order was accepted, a reorder by hand back onto the moves' path holds the pair until it is moved off it or released
found: at the review of #595, U231, 2026-11-07.
issue: no
---

**The mechanism.** When every move was accepted, `_pending` reads an agreed
reading on the moves' path short of their end as a lag however long it
agrees, so it never moves from it. A person who puts the account playlist
back to one of those orders by hand is held the same way, and the pair's
membership stops syncing both ways meanwhile.

**Measured cost.** Driven by round one's review (T6): three runs each held
the pair, and a track added in rekordbox never reached the account. The held
message now says a reorder by hand back onto the path is read the same way,
and that moving it off the path in the provider's player or releasing the
pair frees it (T6b shows an off path order merged as the person's).

**Closes when:** the held message's remedy is enough for Phillip, or a later
card offers a verb that releases a pending order. Ledger only: the product
says what holds it and how to free it.
