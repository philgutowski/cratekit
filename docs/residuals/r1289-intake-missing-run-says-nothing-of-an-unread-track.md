---
title: crate intake missing over a sync all pass says nothing of a track the pass named unread
found: at the review of #547, R-1289, 2026-11-05.
issue: no
---

**The mechanism.** Since R-1289 `crate sync all` queues a swept playlist's
readable tracks and names a track the account lists with no title or no
artist in its summary and the `sync-playlists-unread` warning. The job it
queues holds no item for that track, and `crate intake missing --run` reads
jobs only, so its list and its summary carry no word of it.

**Measured cost.** Driven by the review's round one: `sync all` over a
playlist of 101 and an untitled 103, the job resumed to success, then
`intake missing --run RUN`: exit 0, no warning, and `103` absent from the
whole envelope. The GUIDE calls that verb the one that lists the whole pass at
once, so a person who reads only its list sees a clean pass. The pass's own
warning named the track one verb earlier.

**Closes when:** Phillip answers the question on #547 about a playlist that
left a track unread. Its third option, carrying the unread tracks on the job
so the missing report lists them, closes this; the first, the build's
conservative call, leaves it as recorded. Ledger only until that answer.
