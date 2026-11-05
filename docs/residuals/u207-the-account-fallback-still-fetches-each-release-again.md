---
title: Without the app credentials an ISRC lookup still costs one request plus one per release, through the client library
found: at the plan of #497, U207, 2026-11-05.
issue: no
---

**The mechanism.** Under the app client (U205) an ISRC lookup is one request, with the artists and releases included. Without it, `TidalAccount.match_track` and `TidalCatalogue.tracks_for_isrc` call the client library's `Session.get_tracks_by_isrc`. At 0.8.11 that makes one catalogue v2 call and then a `session.track(id)` for every release the answer names. The account path also has no batch form, so the U207 screen makes no request there.

**Measured cost.** Read from the library's source, not driven live. A code filed under a single, an album cut and three compilations costs six account calls rather than one. This is the live path until the app is registered.

**Closes when:** the app credentials are recorded at the attended sitting U205 owes, which moves every lookup to the one request path. Alternatively, a later card moves the account path to a v2 request of its own after a live probe of what the account token's answer includes. Ledger only.
