# Mutation notes: r705

Author's table, no independent verifier (METHOD, 2026-09-07). Twenty five
rows in two batches, `r705-a-rows.toml` on the gate module and
`r705-b-rows.toml` on the seams, the light pass cap exactly. Split so each
batch ran in the foreground under the harness ceiling; part A took 16 pytest
runs and part B 15, each a full baseline plus one subset per row.

**MEASURED, every row killed.** `r705-a.md`, `r705-b.md` and their JSON
sidecars carry the numbers, at head `97ed633`, every row's restore verified
against HEAD, 79 collected on every row. No zero row, so no composite was
owed. Every row's subset was `tests/test_provider_gate.py`.

## How the guard was watched, and what that narrows

The driver's state leak guard halted the first attempt at part A during the
full baseline: the real installation state directory grew from 10,379 to
10,406 entries while the baseline ran. The writer was read before rerunning,
not assumed: the installed copy's `crate analyze vocals --recursive` job
`2026-09-24T21:04:27Z-fbe8`, the same job that halted R-689's, R-693's,
R-694's and R-695's tables, was three hours in and writing analysis
artifacts under the real jobs directory. It is not this session's to stop.

Both batches were then run with `CRATEKIT_CONFIG_DIR` and
`CRATEKIT_STATE_DIR` pointed at a fresh empty temporary directory, which the
driver documents as the override that wins over the platform path, the same
mechanism that makes the guard safe under its own suite. The guard therefore
watched that temporary root, empty before and after every child: a child
resolving the installation root the product's way would have written there
and been seen. What that narrows, stated rather than hidden: a child reaching
the real directory by a hard coded path would not have been seen, because
that directory was out of the guard's view for the run. The two temporary
roots were `/tmp/r705-guard.dnF9K8` and `/tmp/r705-guard.6K38kf`, both empty
at the end, both left for the system to clear.

## Part A, the gate module

| Row | What it reverts | Kills |
|---|---|---|
| G1 | the shared interval halved | 9 |
| G2 | the interval measured from now rather than from the last call any process made | 9 |
| G3 | a Retry-After no longer holds the next call | 3 |
| G4 | the breaker trips after seven answers rather than six | 3 |
| G5 | a Retry-After at or above the cooldown no longer trips at once | 5 |
| G6 | the trip lifts at once, no cooldown recorded | 8 |
| G7 | a success no longer breaks the run of rate limit answers | 1 |
| G8 | a call inside the cooldown is made anyway | 2 |
| G9 | an opener asking inside the cooldown is told to go ahead | 4 |
| G10 | a Retry-After wait slept holding the lock | 1 |
| G11 | the lock wait limit drops the one interval a holder may sleep | 1 |
| G12 | a park the tool swallowed is forgotten | 1 |
| G13 | this process's call counter never moves | 6 |

## Part B, the seams

| Row | What it reverts | Kills |
|---|---|---|
| S1 | the client opener builds a client inside the cooldown | 1 |
| S2 | the client's transport is not gated | 10 |
| S3 | the vendored adapter builds the tool inside the cooldown | 1 |
| S4 | the tool's own session is not gated | 1 |
| S5 | a park the tool swallowed inside its login reads as a rejected session | 1 |
| S6 | a park the tool swallowed inside a download reads as no file | 2 |
| S7 | acquire_one softens the park at the lookup | 1 |
| S8 | acquire_one softens the park at the fetch | 1 |
| S9 | the playlist read wraps the park into an unresolvable playlist | 1 |
| S10 | an infinite interval passes validation | 2 |
| S11 | the spend line is never put on the envelope | 5 |
| S12 | the dispatcher emits the envelope without the spend | 5 |

Nothing was dropped below the cap.

## What a normal label sweep costs, and the run time the interval implies

The brief asks for the call count of a normal sweep against the chosen
interval. No live sweep was run, the account is the thing this unit protects,
so the count is derived from two measurements and says which is which.

**Measured on the tree:** one offered release costs two catalogue calls, one
album read and one page of its tracks, pinned by
`test_one_offered_release_costs_two_calls_on_the_catalogue` over the tree's
own `release_tracks`. **Measured at the eleventh sitting, A7:** the sweep of
47 labels settled 27 and offered 1,701 releases. The offer checks on those
27 labels were therefore at least 3,402 calls, before the per label listing,
about four to ten calls a label across the three release methods and their
pages, and before verification. Call it about 3,600 calls for 27 labels,
about 135 a label, and about 6,300 for the whole registry of 47.

At the default interval of one second, a full registry sweep is about
6,300 seconds, one hour and forty five minutes, against a crawl that
unpaced reached the limit in minutes. At half a second it is about 53
minutes. The interval is one line in `[provider]`; the default stays at one
second because the limit's own number is not published and the sitting's
crawl, at whatever rate the client managed, was over it.
