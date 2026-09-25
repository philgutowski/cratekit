# R-704 mutation notes

**Verdict: measured, 18 rows in one batch, every row killed.** Written on
`relay/216`, 2026-09-25, by the author, so a kill here is the author's and
there is no zero to qualify.

| Batch | Rows | Killed | Zero |
|---|---|---|---|
| `r704-a` | 18 | 18 | 0 |

## What the rows cover

- **S1 to S6, the classifier.** `sweep._lookup_failure` asks the declared
  cause chain by the provider's type or status, and the implicit context chain
  by a structured 429 status only. Each layer is removed or narrowed alone:
  the cause check, the cause walk, the context check, the context walk cut to
  one level, the context read by type, and the status set moved to 503.
- **S7 to S10, the four boundaries.** Each of the sweep's four provider
  boundaries, the listing probe, the crawl, the artist resolve and the
  verifier, hands the classifier a plain error in place of the one it caught.
  The first round of tests drove only the crawl and the verifier, so S7 and S9
  would have been user facing zeros; a test for each was written before the
  batch, `test_a_rate_limit_at_every_other_sweep_boundary_is_retryable`.
- **R1 to R6, the increment.** The branch, the retryable flag, the remedy, the
  detail marker, the flag stored on `LookupFailure`, and the sentence.
- **E1 and E2, a sample of existing guards on the path.** The verifier's
  refusal pass through, which is what lets the provider gate's `Parked` reach
  the job engine unflattened, and the job verdict's any over all.

## What the batch did not see

- **The provider gate.** The fakes make no HTTP call, so no row exercises the
  gate's trip. Live, a listing that stays rate limited through its ladder parks
  before the sweep's boundary; the tests say so in the listing helper's
  docstring.
- **The real installation state was not the watched root.** The installed
  copy's `analyze vocals` job `2026-09-24T21:04:27Z-fbe8` was still writing
  `jobs/` under the real root, and the first attempt stopped on that with 23
  new entries during the baseline, before any row. The batch was rerun with
  `CRATEKIT_STATE_DIR` and `CRATEKIT_CONFIG_DIR` pointed at an empty temporary
  root, `r704-watch`, which held 0 entries before and after. Every child still
  ran in the driver's own sandbox. Unlike R-703's notes, the real root outside
  `jobs/` was not hashed before and after this run.

## Found at the review and not fixed here

- **A mixed job re-arms its permanent items.** `jobs.retry` re-arms every
  failed item once any failure is retryable. Filed R-716.
- **Transport failures other than a rate limit stay permanent.** Filed R-717.
- **An ownership read that meets a rate limit offers the release.**
  `OwnedReleases._holds` answers not owned on any provider error, and stops
  asking after three in a row. That is R-259's stated decision, an extra offer
  a person declines over a withheld one, and its docstring says so, so it is
  not filed again.
- **A rate limited discovery search is skipped as read.** Already R-467.
