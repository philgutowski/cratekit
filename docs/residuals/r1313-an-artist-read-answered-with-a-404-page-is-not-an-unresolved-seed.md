---
title: An artist read answered with a 404 page is not an unresolved seed, since the catalogue reads that not found by its class alone
found: at round one of #561's review, R-1313, 2026-11-06, the class one file over.
issue: no
---

**The mechanism.** `label.tidal_catalogue._artist_identified` answers a seed
the provider has no artist for by catching the client's `ObjectNotFound`. A
404 whose body is a page never becomes that class (R-1313's mechanism), so the
client's decode error propagates out of the artist read with the 404 three
context links down, and the label roster reports a failed read rather than
"no artist with identifier".

**Measured cost.** Driven by the review: `session.artist` raising the
installed client's failure for a 404 page propagates as `JSONDecodeError`,
`nearest_status` 404. Not introduced by R-1313, which changed the four readers
its brief named. Whether the provider answers an artist read with a page is
the attended measurement R-1313 left out of scope.

**Closes when:** `_artist_identified` also answers `None` when
`core.cause.answered_not_found` holds, with a test raising the failure through
`tests/provider_answers.client_failure`. Ledger only: the producer is
unmeasured, and the cost is a refusal worded as a failed read.
