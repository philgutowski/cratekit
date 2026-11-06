---
title: The sync pair forecast counts a long playlist's unpaged walk as if the provider caps it at a hundred
found: at round one of R-1360's review (#585), 2026-11-06.
issue: no
---

**The mechanism.** `sync.pair_calls.unpaged_calls` counts the unpaged
read's walk as one request and one more for every 99 tracks past the first
hundred, the listing seam's recorded page size. The cap of the client's no
window read was not measured live, and the forecast test holds it only to a
stand in capped at a hundred.

**Measured cost.** None driven: a provider serving more a request spends
fewer calls than forecast, so a run's expected calls read high for long
playlists; one serving fewer, which nothing suggests, spends more than
forecast and the ceiling's margin covers it.

**Closes when:** the cap is measured at the attended sitting R-1360's
landing filed, and the forecast follows it. Ledger only.
