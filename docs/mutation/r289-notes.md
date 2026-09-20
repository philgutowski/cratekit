# R-289 and R-291 mutation tables, read

Three tables, all the author's and none independent, measured by
`scripts/mutate.py` on `relay/167`. Every restore was verified against
`git show HEAD:<path>` by the driver and the tree was confirmed clean with
`git diff HEAD -- src` after each batch.

**`r289-a.md`**, 6 rows over `tagging/tag.py` at `67f5b71`, null control 0 of
9063, no collect drift. 5 killed, one zero. The subset was the four test files
importing the module.

**`r289-b.md`**, 15 rows at `67f5b71`: nine over `acquire/cli.py`, two over
`acquire/fallback_cli.py`, one more call site row, and three over
`core/jobs.py`. Null control 0 of 9063, no collect drift. 11 killed, four zeros.

**`r289-c.md`**, 2 rows at `c09434a`, re-measuring two of batch B's zeros
against the guards those zeros bought. Null control 0 of 9065. Both killed.

**23 rows in all, 21 distinct mutations and 2 re-measures, under the light cap
of 25.** Seven more were considered and logged as dropped in the row files with
the reason each was ranked below the cap.

Split into three batches rather than one for a mechanical reason: the harness
this ran under kills a foreground command at 600 seconds, batch B alone took 25
pytest invocations, and a driver killed mid row leaves a partial mutation in the
source that has to be restored by hand.

## The four zeros, and what each one owes

- **A6, the `[:-1]` slice on the staging directory match.** Including the file's
  own name in the match is a BEHAVIOUR PRESERVING mutation and the zero is
  correct rather than a gap. A name that equals a staging directory name, for
  instance `.cratekit-acquire-staging`, carries no suffix at all under
  `pathlib`, since a leading dot with no second dot is all stem, so it can never
  pass the `AUDIO_EXTS` filter that runs before this clause. The composite METHOD
  asks for on a user facing zero is **A3**, the same clause with the guard itself
  removed, which killed 4. The slice is precision about what the clause means,
  not a second guard.

- **B7, the missing staging tree guard.** Covered by `_children`, which answers
  an empty tuple for a directory it cannot list, including one that is not
  there. Two layers hold the same case and removing either alone leaves the
  other, which is exactly METHOD's "a guard covered by another guard is a guard
  nothing covers". The layer that actually holds it is measured: **B9r** kills.
  The guard stays because it says the intent at the top of the function rather
  than leaving it to an exception handler three calls down.

- **B8, `_children` returning unsorted.** Maintainer facing, one line, no
  composite. The sweep's result order is asserted in one test and that test
  builds one item directory, so ordering has nothing to disagree about there.
  Nothing a person sees depends on the order in which empty directories are
  removed.

- **D2, halving `_ID_CHUNK` from 500 to 250.** Maintainer facing, one line.
  METHOD asks for coefficient mutations because a bound a multiplier can move
  under a green suite is not pinned, and here the honest reading is that the
  bound has a floor and no ceiling: any chunk size at or below SQLite's
  statement parameter limit is correct, so halving MUST kill nothing. The
  direction that matters is up, and that is **D1**, raising the chunk past the
  limit, which killed.

## The two zeros that bought a guard

Both were real holes rather than redundancy, and each one is now a test.

- **B2**, `_reclaim` appending to the removal record whether or not `rmdir`
  returned, killed nothing across 9063 tests. Nothing read the return value
  against a directory that could not be removed, which is the reachable case:
  the refused landing's directory holds evidence on purpose and will never go.
  `test_the_sweep_does_not_report_a_directory_it_could_not_remove` drives it and
  **B2r** kills.

- **B9**, letting an unlistable directory raise out of `_children`, killed
  nothing. The sweep runs at the head of `acquire download`, before the verb has
  started its real work, so an unreadable directory under the staging tree would
  have answered a person's download request with an unhandled `PermissionError`
  over housekeeping they did not ask for.
  `test_a_job_directory_that_cannot_be_LISTED_does_not_fail_the_verb` drives it
  at mode `0o111`, the same shape `tests/test_restore.py`'s round seven test
  uses, and **B9r** kills.

## What the kills say

The tagging walk's two skips are independent and each is held on its own: A1
removes the AppleDouble skip and A3 the staging skip, and each kills without the
other. A2 is the defect the code review caught, widening the sidecar prefix from
`._` to `.`, and it kills through the counterexample test alone, which is the
test that exists because the first cut of this guard shipped that widening. A4
shows the set's membership is load bearing rather than decorative: forgetting
the master staging tree kills 2, so the tree that lands inside the music library
is covered by its own cases and not by the acquisition tree's. A5 shows the
relative anchoring is load bearing too.

The sweep's shape is pinned from every direction that could reverse a decision
in it. B1 swaps `rmdir` for `rmtree` and kills, which is the evidence file the
whole "empty only" rule exists to protect. B3 removes the terminal filter and
B4 reads an unknown identifier as finished, and both kill, so neither the open
job rule nor the foreign store rule leans on the other. B5 and B6 both kill, so
the order of the two reclaims and the presence of the second are each held.

All three call sites kill: C1 for `acquire download`, C2 and C3 for the two
paths of `acquire fallback fetch`. That was the code review's second finding,
and the two fallback rows are what make the fix a measurement rather than a
claim.

D1 and D3 kill, so both properties `jobs.states_of` was written for are held:
the chunking that survives a caller asking about more names than one statement
takes, and the rule that a name with no row is absent from the answer rather
than given a state.

## One flake, not a finding of this branch

Batch C's first attempt refused with a red baseline, one failure in
`tests/test_write_session.py::test_an_unresolved_session_keeps_its_capture_out_of_the_pruner`.
That test passes alone, the full suite was green immediately before and
immediately after, and the second attempt at the same batch had a green
baseline. Recorded as a residual rather than chased, since nothing on this
branch touches that module and a one in three appearance under `-n auto` is the
shape of a parallel ordering or clock sensitivity.
