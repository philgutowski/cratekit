# Mutation notes: R-221, the queued backup says which kind of run it was

Two batches, `r221-a` and `r221-b`, **20 rows under the cap of 25**, the
author's own and not an independent table. **19 killed, one zero.** Null
control zero in each batch, of 9085 collected, and every row's restore
verified against `git show HEAD:`.

Both batches ran in the FOREGROUND, which is how a Relay session runs this
driver: `docs/METHOD.md` prefers a tracked background job, and a session that
cannot wait on one across turns takes the batch split instead. Batch a took 5
minutes 39 and batch b 3 minutes 32, each under the harness tool ceiling. The
split is for that ceiling alone, not for any difference between the rows.

## The zero

`E3_outcome_reads_publish_instead`, maintainer surface, **one line and no
composite**, which is what METHOD asks for a maintainer facing zero.

`run_backup` records `dry_run=dry_run` rather than `dry_run=not publish`, and
the row swaps one for the other. It killed nothing and the row's own
description **predicted that before it was measured**: the two expressions
agree on every path reachable today, because `dry_run` forces `publish` false
and no caller in `src` passes `publish=False` on its own. The distinction is
real and it is about a run that does not exist yet: a caller can ask a real run
to publish nothing, and that run still copied the library, while a rehearsal is
the one that did not. The row is here so the prediction is measured rather than
asserted, which is the same shape R-44's table logged for its empty slot guard.

The code review raised the same point independently and did not report it as a
finding, on the same reachability grounds.

## The one zero that was NOT left standing

`W6_twin_branch_says_it_unconditionally` measured a real ZERO on its first
pass, on a USER facing surface. Making the twin branch carry the rehearsal
word unconditionally killed nothing: the existing twin cases assert the
already-queued code is PRESENT, the rehearsal twin case asserts this one is,
and nothing asked what a real twin is NOT told. So a person asking twice for a
real backup could have been told the job they are being handed copies nothing,
with a green suite.

It bought `test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`.
Re-measured after that test landed, it kills 1. Batch a was then re-run whole
rather than resumed, so every row in the published table is measured against
one tree at one collected count, 9085.

## Considered and dropped, with reasons

Four rows were considered and are NOT measured.

- **The rehearsal sentence's wording.** METHOD says to reword a message
  mutation rather than append, and the suite matches on `"copies nothing"`, so
  a reword kills the four tests that read it. It is the same measurement
  `W1_rehearsal_never_said` already makes and it was ranked below the cap as a
  duplicate rather than as untested.
- **`backup_argv` dropping the rehearsal flag from the resume.** A real guard
  and not this round's diff: it is U50's, it has its own test
  (`test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`), and
  the round's own diff plus a fixed sample is what METHOD scopes a table to.
- **`_open_twin`'s flag comparison.** Same reason, R-223's guard, with
  `test_a_rehearsal_and_a_real_run_are_two_jobs` on it.
- **`published_ages` reading the live configuration rather than the frozen
  one.** R-154's guard, not this round's, and `test_the_ages_reported_are_the_ones_this_job_published`
  holds it.

## What the numbers say about the cover

The three lowest counts are `W3`, `W4`, `W6`, `R1` through `R4`, each killing
exactly one test. That is the shape a set of narrow guards produces: each is
the only guard on one branch, and one test per branch is what covers it. It is
worth knowing that a single test failing to collect would take any one of them
to zero, which is why the collected count is on every row.
