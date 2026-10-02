# R-788 mutation tables, read

Four tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/245` after both of the review's fix rounds, one
at a time, each waited on with nothing else touching the tree. Every null
control killed 0 of the full suite, 12,120 collected against 12,120, every
row's collected count equalled its subset's baseline, every row's
`head_verified` is true, no row was promoted, and after each table
`git status` showed the tables' own files and nothing else.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r788-a.md`, who gains a vocal membership | 7 | 7 | 0 |
| `r788-b.md`, the bucket rule and the digest | 7 | 7 | 0 |
| `r788-c.md`, the readers | 7 | 7 | 0 |
| `r788-d.md`, the verb | 4 | 4 | 0 |

25 rows, the cap, one pass. No zero, so no composite was owed.

Four tables and not one, on R-821's arithmetic, and on this run the
arithmetic was worse than recorded. The machine was loaded, the suite took
122 to 131 seconds where it takes 61 to 67, and three of the four tables ran
past the 600 second foreground ceiling. Table a took 653 seconds. The harness
did not kill those runs. It moved each to the background, the session waited
on the driver's process and started nothing else, and each finished with its
restore verified. A seven row table is too large for a loaded machine to
finish in the foreground.

Subsets, named on every row and not derived. Every row but one ran
`tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`,
`tests/test_adopt_former_place.py` and `tests/test_adopt_workers.py`, 188
collected. The move worker's row ran `tests/test_adopt_move.py` and
`tests/test_adopt_workers.py`, 162.

## The rows that die on one test

Seven rows are held by a single test each. Each is a real death, and each is
one deleted test away from a zero.

- `P9_unplaced_entry_gains` and `A5_move_worker_reads_vocals`. Killed by the
  two tests written while these rows were being planned. Before them the
  placing rule's own half sat behind the plan blanking the bucket first, and
  the move worker's read was driven only through the gate.
- `P10_manual_class_is_vocal`, `P17_withheld_presence_is_planned`,
  `P19_answered_genre_files_nothing` and `A1_census_before_the_calibration`.
  One direct test each.
- `L6_removed_node_is_a_place`. The removed playlist filter both readers now
  share. One test of the vocal reader kills it. The placement reader's own
  test of a removed playlist is in `tests/test_adopt_move.py`, which this
  row's subset did not run, so the count is of the subset and not of the
  suite.

## What the cap dropped, and why each ranked below it

Eight candidate rows were written down and not measured.

- `Vocals.filing` without the tree being read. The same line as the measured
  calibration row, and a test of each reason nothing can be filed asserts it.
- `vocal_sub` matching an additive class of any identifier. The loader allows
  one additive class, so the mutation changes nothing a shipped or a loaded
  taxonomy can reach. A test of it exists.
- `vocal_sub` without the identifier clash. The display name clash on the
  same line was measured, and the identifier clash has its own test.
- The digest without the vocal state. A test asserts five states give five
  digests.
- A collision verdict leaving an addition's state as it was. The state is
  shown and is not written from: a withheld entry is never planned whatever
  its state says.
- `vox_tagged` answering the empty set for a library with no tag. Changes the
  word on the plan and no write.
- `vocal_standing` reading the calibration for a taxonomy with no vocal sub.
  A refusal either way, never a write, and a driven test holds it.
- The gate without its vocal list. The conformance of the gate's facts to the
  document is asserted by one direct test.

## Not measured by any row

- The live run. Rehearsed on a copy, applied on an equal digest, and the
  twelve read in their subs. Owed to an attended sitting.
- Whether rekordbox soft deletes a My Tag association or deletes the row. The
  reader skips a marked row and was driven against rows a test spelled.
- A renamed vocal playlist under a renamed FOLDER. The reader finds it by its
  recorded node and the plan adds nothing there. Only the playlist rename was
  driven on a database.
