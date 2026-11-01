---
title: The full label playlists build's estimate leaves out the listing's own pages, read again on each of its runs
found: at the review of #402, U191, 2026-10-31.
issue: no
---

**The mechanism.** `Estimate.calls` in `src/cratekit/label/playlists_cli.py`
counts two calls per listed release, the track reads. The listing itself, a
page of 100 releases a call, is read before the crawl gate and again by the run
that answers it and by the run that applies the plan, and none of those pages
is in the figure.

**Measured cost.** On Defected's 12,368 releases that is about 124 calls a run,
about 370 across the three runs, beside an estimate of 24,736. The screen calls
its figure a floor and says the apply reads again, so nothing false is said.
Computed from the page size, not driven against the provider.

**Closes when:** the estimate adds the listing's pages for each run it will
spend them on, or the resume of the full build (the U191 residual on the
breaker) keeps the listing too. Ledger only.
