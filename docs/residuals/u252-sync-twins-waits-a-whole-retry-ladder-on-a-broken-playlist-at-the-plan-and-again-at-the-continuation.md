---
title: crate sync twins waits a whole retry ladder on a playlist the provider cannot list, at the plan and again at the continuation
found: at the build of #681, U252, 2026-11-12.
issue: no
---

**The mechanism.** `crate sync twins` reads each downloaded account playlist
through `label.cli._listed`, whose window read pages through
`listing.fetch_with_retry`. A provider failure that is not a Cratekit
refusal declaring itself not retryable, a timeout or a server error, climbs
the whole ladder, 1, 2, 4, 8 and 16 seconds, before the playlist is left and
named. The plan reads every playlist, and the continuation after the
approval gate plans again to hold the write to the approved digest, so a
playlist the provider cannot list costs one ladder at the plan and another
at the continuation. The ladder is correct for what it is given: a timeout
can succeed on the next attempt, and a refusal that cannot
(`ListingNotPaginated`, an expired session refused `credential-missing`)
already leaves it at once, which `test_a_refusal_that_is_not_about_one_playlist_still_stops_the_run`
shows in the same file. What is open is a product question, not a defect:
whether a backfill that already leaves a playlist it could not read and
reads it again next run should climb the ladder for it, and whether the
continuation should read again a playlist the plan already left.

**Measured cost.** On the tree, before U252 faked the sleep in the tests,
`tests/test_sync_twins.py` measured 31 seconds per reading of one broken
playlist (31.18, 62.33 and 93.55 seconds for one, two and three readings).
A DJ whose provider times out on one playlist waits about 31 seconds at the
plan and 31 more after approving, per broken playlist; nothing is written
wrongly and the other playlists' twins are made. Not driven against the live
provider.

**Closes when:** Phillip decides whether the twins backfill should read a
playlist once without the ladder, or the continuation reuse the plan's
refusal for a playlist it left, and a card builds the answer. Ledger only:
it costs time, not data, truth or a finishing workflow, so it meets none of
the board bar's four costs. U252's card left this question out of scope.
