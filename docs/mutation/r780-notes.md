# R-780 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/231` at `3b4f7df`, in the foreground, one at a
time. Null control 0 on each, 10,976 collected against 10,976, no collect
drift, every restore verified against `git show HEAD`.

**`r780-a.md`**, 12 rows: the plan's own guards in `adopt/move.py` and
`adopt/placements.py`. 12 killed. The two largest kills are the two halves
of the finding: `A1`, the plan asking only the entry's bucket, which is
R-780 as filed, 22 kills, and `A2`, the tree path adding a sub in a bucket
the genre does not name, 11 kills.

**`r780-b.md`**, 6 rows: the worker's check in `adopt/move_cli.py`, with
R-758's "a sub nobody was shown is removed" as the fixed sample. 6 killed.
`B2`, the worker asking the entry's own bucket rather than the bucket the
move names, kills 17: every driven approved run refuses a tree path move.

**18 rows, 18 killed, no zero.** Five rows were considered and not run,
each named in `r780-b-rows.toml` with the reason it ranked below the cap.
The cap was not reached: the unit's diff has no further guard worth a row
that is not a wording or a reason's name.

## The watched roots were not the real ones, and why

The first attempt at table a stopped in its baseline with the driver's own
refusal, `STATE LEAK`: the fingerprint of `~/Library/Application
Support/cratekit` moved while the full suite ran, at an unchanged entry
count. The writer was not a child of the driver. A live `crate sync labels`
job, the author's own, queued at 18:00 UTC and running beside this session,
was writing `provider_gate.json` and the job queue's write ahead log in the
real state directory, and the guard cannot tell a concurrent writer from a
leak.

Both tables were then measured with `CRATEKIT_CONFIG_DIR` and
`CRATEKIT_STATE_DIR` pointed at an empty scratch directory, so the roots the
driver fingerprints were that directory and not the real ones. Every child
was sandboxed exactly as before, since the driver sets each child's roots
inside its own workspace whatever the caller's are. What was lost is the
second check: a child that reached the real machine during these two runs
would not have been seen by this guard. The header of each table says which
roots it watched. Filed as R-783.

## Rows that were met before they were measured

Two rows would have been zeros on the suite as first written, and a reader
should know the tests that kill them were written for the review's findings
before the table ran.

- **`A3` and `B5`, a verdict on the bucket asked.** The first version
  honoured a verdict only on the entry's own bucket. The review found it,
  and `test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`
  drives both the plan and the worker. 2 and 1 kills.
- **`B3`, a renamed target read as done.** Dropping the routed check from the
  worker's "done" test let a track whose one place is a renamed playlist read
  as finished. The review found it, and
  `test_a_target_held_only_under_another_name_is_not_done` refuses it. 1 kill.

## One guard where there were three

The band only check of the tree path was written three times before the
table: at the selection of buckets, at the decision, and at the doubled
listing. A row removing any one was covered by the other two and would have
measured nothing. `tree_path_decides` is now the one predicate all three ask,
and `A5` removes it. 1 kill.
