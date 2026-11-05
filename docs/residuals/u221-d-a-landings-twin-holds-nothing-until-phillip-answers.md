---
title: A twin a landing makes holds nothing, so a track the landing missed is queued again at the next sync pair without a release, until Phillip says whether it should be held too
found: at the build of #549, U221, 2026-11-05.
issue: no
---

**The mechanism.** `sync/twins.pair_landed` marks a landing's twin with an
empty hold, so `crate sync pair` queues a track that twin lacks as any pair's,
through intake. Only `crate sync twins` (the backfill) records a hold. The
card asked Phillip, under "Question for Phillip" on #549, whether a landing's
twin should hold its misses too; no answer had come by the landing, and the
build took the recommended option, leaving it as it was.

**Measured cost.** None new: before U221 a landing's misses were queued again
the same way. The sweep that made the twin was Phillip's choice to download
that playlist, so a retry of its misses is a download he chose. Driven by
`tests/test_sync_twins_hold.py`, the landing test records an empty hold.

**Closes when:** Phillip answers. If he picks holding a landing's misses,
`pair_landed` records them as the backfill does, a small card. Ledger only.
