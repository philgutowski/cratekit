---
title: A synced playlist that lists one track twice is never held by sync removed, so every run reads it again
found: at the review of #1010, R-1716, round two, 2026-11-23.
issue: no
---

**The mechanism.** `SyncedReads.keep` holds a read only when
`len(listing.refs)` equals the account listing's track count. The reader
builds the playlist's order with one entry per id, so a playlist holding one
track twice reads one ref fewer than the provider counts, and is read again
on every run.

**Measured cost.** Calls only, no wrong answer. Driven in review round two:
a playlist of three rows over two ids was asked on four of four commands and
never held; with 20 such among 60 synced playlists at 3 calls each, the runs
spent 183, 63 and 63 calls. How many of the live account's synced playlists
repeat a track is not measured.

**Closes when:** the read carries its row count beside its distinct ids and
the guard compares that, with a test of a playlist listing a track twice
held. Ledger only.
