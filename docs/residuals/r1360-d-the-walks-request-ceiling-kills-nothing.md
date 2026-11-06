---
title: The unpaged walk's request ceiling kills no test, ends a walk silently, and is credited with what the cap of one guard holds
found: at round two of R-1360's review (#585), 2026-11-06.
issue: no
---

**The mechanism.** The fix round bounded `playlist_tracks_unpaged`'s walk
at one request per declared track (`for _ask in range(declared)`), so that
removing the cap of one guard or the short page stop fails a test rather
than hanging the suite. With both of those guards in place the bound is
unreachable: each request either ends the walk or adds a track. Reverted to
an unbounded loop, halved, or cut to two requests, it leaves all 203 tests
of the touched files green. Were it reached, it would end the walk silently
with a first part, where the module's other walks spend their budget loudly
with `ListingTruncated`. The docstring says the walk asks at most one
request a declared track whatever a page holds; that ceiling rests on the
first page holding two tracks, since with that guard loosened a cap of one
asks one request more than the count.

**Measured cost.** None to a DJ: 20520 driven shapes at round two (nine
page behaviours, six caps, nineteen sizes, twenty declared values) never
reach the bound, and a first part ending a walk is read as a lag beside a
whole window, never as the playlist. Maintainer facing.

**Closes when:** the bound raises as the other walks' budgets do, with a
test that reaches it, or the docstring credits the guard. Ledger only.
