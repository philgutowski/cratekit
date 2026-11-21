---
title: Only a 404 or the client's not found class is a sighting, and what the account's thirteen vanished playlists answer is unmeasured
found: at the build of #889, U320, 2026-11-21.
issue: no
---

**The mechanism.** `sync.unavailable.answered_unavailable` counts a failure as
a sighting only when the nearest status along its chain is 404, or, with no
status, a declared cause of the client's class `ObjectNotFound` by its exact
name. tidalapi 0.8.11 raises that class for a 404. A playlist deleted, made
private or another user's may answer 401 or 403 rather than 404; such a
playlist is never recorded, never retired, and still stops every offer, and
`crate sync removed --retire` names it as not read whole rather than offering
it.

**Measured cost.** Not driven against the account. A179's run named 13 synced
playlists the account no longer lists whose ids do not open, without their
status. If they answer 404 the next two runs a day apart, or one
`--retire`, release them; if not, nothing offered changes on that account.

**Closes when:** the attended run of A179 (#842) records what those playlists
answer and whether the second run offers the track. Ledger only: it closes at
a sitting.
