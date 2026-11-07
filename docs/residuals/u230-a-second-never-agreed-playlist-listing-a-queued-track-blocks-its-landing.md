---
title: A second never agreed mirrored playlist that lists a queued track counts as a snapshot holding it, so the landing is not read and the account loses the track from both playlists
found: at the review of #594, U230, 2026-11-06.
issue: no
---

**The mechanism.** `Mirrored.base` is the account side of a playlist never
agreed, and `decide` counts every base as a snapshot holding the track. U230
lifts that reading for the queuing playlist alone. A track queued from
`Tech House Med` and also listed on a never agreed `Tech House with vox` is
read by the later change rule, so rekordbox's place stands and the mirror
takes the track off both account playlists.

**Measured cost.** Driven on U204's world by round one of the review, with
the second playlist's snapshot removed by hand; the same with that playlist
agreed carries correctly. A newly mirrored playlist is the candidate
producer and was not driven.

**Closes when:** a never agreed base the account side alone gives is not read
as a snapshot that held the track for the landed check, or a producer is
shown not to exist. Ledger only, reachability unmeasured.
