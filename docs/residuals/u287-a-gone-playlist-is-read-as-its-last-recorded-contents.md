---
title: A synced playlist sync removed reads as gone is held to what its jobs recorded, so a track added to it on the account since cannot keep a row
found: at the review of #373, U287, rounds one and two, 2026-11-15.
issue: no
---

**The mechanism.** A playlist neither the account's list nor its id finds is read as gone, and a failed open there is any provider failure (`PlaylistUnresolvable` wraps every exception), not a not found. Since round one a gone playlist holds what its finished intake jobs recorded, and one nothing records stops every offer. What it cannot hold is a track Phillip added to that playlist on the account after its sweep, a row the reader set aside at the sweep (a job queues only rows it can read), a row a short listing withheld, or, for a pair's or a mirror's job, a track the library owned when it was queued: if the playlist still exists and only failed to open, such a track reads as on no other synced playlist, and is offered.

**Measured cost.** Driven on fixtures through the fake catalogue by round two: a track moved onto a gone playlist after its sweep is offered. The real producer needs the account's list to omit an owned playlist (R-385, unmeasured) and its open to fail in the same run; not driven.

**Closes when:** the provider's not found is told apart from its other failures at `playlist_for`, so only a real not found reads as gone and anything else as not read whole. Ledger only.
