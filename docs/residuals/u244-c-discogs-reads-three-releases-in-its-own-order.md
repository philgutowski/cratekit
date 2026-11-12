---
title: Discogs reads the first three releases its search names, so a track on a later one, or a better styled later pressing, is not seen
found: at the review of #673, U244, 2026-11-12.
issue: no
---

**The mechanism.** `DiscogsAsker._search` reads at most
`DISCOGS_RELEASES_READ` releases in the search's order. A track carried only
by the fourth result is a MISS; three gone results before a live fourth are a
MISS; the first matching release whose first style names no folder declines
the file even when a later pressing's style would. A styleless match does give
way to a later styled one since the fix round.

**Measured cost.** Driven at the review on recorded JSON only. Whether the
live search ever orders results this way was not measured, since the live API
is off limits in the cloud.

**Closes when:** the attended Discogs trial reads how often the match sits
past the third result, and the cap or the gone count is changed if it does.
Ledger only until then.
