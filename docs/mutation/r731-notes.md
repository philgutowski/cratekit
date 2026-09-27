# R-731 mutation notes

**Verdict: measured, 25 rows in three batches, 25 killed, no zero standing.**
Written on `relay/221`, 2026-09-27, by the author, so a kill here is the
author's and the absence of a zero is the author not finding one, which is not
the same as there being none. Independent tables on this repository have found
1.2 to 1.7 times what the author's did.

| Batch | Rows | Killed | Zero | Wall clock |
|---|---|---|---|---|
| `r731-a` | 11 | 11 | 0 | 4 min 12 s |
| `r731-b` | 12 | 12 | 0 | 4 min 23 s |
| `r731-c` | 2 | 2 | 0 | 3 min 48 s |

Every batch ran in the foreground, one at a time, with nothing else touching
the tree, and `git status` showed no change under `src` after each.

## What the rows cover

- **M01 to M11 and M23, M25, `adopt/plan.py`.** The unread guard, the filter
  of held subs to the competing set, the same sub exemption, the renamed
  playlist exception to it, the rule that an unnamed sub must be a held one,
  the withholding itself, the bucket a withheld entry keeps, the two digest
  keys each removed alone, the check inside `with_verdicts`, the review list's
  filter, the collision count's subtraction, and the planned sub belt.
- **M12 to M15, `adopt/apply_cli.py`.** The tree read reaching the plan, and
  the three gate facts each removed alone.
- **M16 to M20, `adopt/placements.py`.** The two refusals that answer unread,
  each removed alone, the recorded node, the both names rule, and the read
  flag.
- **M21, M22 and M24, `core/routing.py`.** The no reading sub, the single sub
  and the sub class subtraction.

## Two rows that measured zero first

`M24` and `M25` measured zero on the full suite, 10,520 collected, in batch
c's first run. Both are inert on the shipped template, where no sub class
shares an identifier with a band. `test_a_sub_class_is_removed_from_the_bands_by_identifier`
and `test_a_planned_sub_outside_the_competing_set_is_never_withheld` reach
them on a template edited to share one. The second run of batch c, over the
same row text, killed both. The table in `r731-c.md` is the second run. The
first exists only in the commit before it.

Both are maintainer facing: a person's own template could declare the clash,
and no producer of one was driven.

## One invalid batch

Batch a's first run was INVALID. The null control lost
`tests/test_provider_gate.py::test_two_processes_never_call_at_once_and_keep_the_interval`
with 10,520 collected against 10,520, load average 15.57 on 11 cores. That is
R-711 to the letter. The test passed alone, 79 of 79 in its file, and the same
batch run again was valid. One occurrence, so no rate.

## Dropped

Nothing was dropped to the cap. Not given a row: the tier condition in
`competing_subs`, since the one shipped bucket that routes by source also has
its energy dimension off and either clause alone gives the same answer, and
`withheld_by_placement`'s membership test, which the review list's filter
already decides.
