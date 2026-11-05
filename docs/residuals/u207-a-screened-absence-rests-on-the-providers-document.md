---
title: A code a batch of ISRCs leaves out is read as filed under nothing on the provider's document alone, never on a live answer
found: at the review of #497, U207, 2026-11-05.
issue: no
---

**The mechanism.** `acquire.isrc_screen` reads a code that a multi code answer of `GET /tracks?filter[isrc]=` does not name as filed under nothing, and `TidalAccount.match_track` and `TidalCatalogue.tracks_for_isrc` then answer it not found with no request. Two things say an omitted code is lacking: the platform's published document (version 1.10.224), which says several codes return one track per code, and the screen's refusal of any answer it cannot attribute whole. No live request has confirmed it, because the container that built U207 had no app credential.

**Measured cost.** Not driven against the live API. Driven on fixtures by the round one review: a screened absence is remembered by `sync pair` as a `pairs.Miss` and by the mirror as a ledger miss. Both carry the same reason and key the account session path writes, and both are reused until the row's code changes. If the live answer ever omits a held code, up to twenty rows per request would be remembered as unmatched, where before U207 one wrong empty answer cost one row. Until the app credentials are recorded at the attended sitting U205 owes, the screen makes no request at all.

**Closes when:** the attended live read compares one batch answer against the same codes asked one at a time and they agree, recorded in the sitting record. Ledger only; the screen is off until the app is registered, and the read is owed as an attended card.
