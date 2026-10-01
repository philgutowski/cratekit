# R-797 mutation tables, read

Three tables, the author's and not independent, measured by
`scripts/mutate.py` on `relay/237` after the first review's fix round, each in
the foreground and waited on. Every null control killed 0 of the full suite,
11,356 collected against 11,356, every row's collected count equalled its
subset's baseline, and after each table `git diff` over `src` and `tests` was
empty.

| Table | Rows | Killed | Zero |
|---|---|---|---|
| `r797-a.md`, the loader's guards on a former place and where one competes | 9 | 9 | 0 |
| `r797-b.md`, the placement reader, the move plan and the writer's list | 8 | 8 | 0 |
| `r797-c.md`, the report's count and what a genre has in the tree | 8 | 8 | 0 |

25 rows, the cap, one pass. No zero, so no composite was owed.

Subsets, named on every row and not derived. Table a ran
`tests/test_taxonomy.py`, `tests/test_adopt_former_place.py`,
`tests/test_adopt_placements.py` and `tests/test_routing_parity.py`, 1,016
collected. Table b ran `tests/test_adopt_former_place.py`,
`tests/test_adopt_move.py` and `tests/test_adopt_placements.py`, 187
collected. Table c ran `tests/test_report_genres.py`, 27 collected.

## What the cap dropped, and why each ranked below it

Nine candidate rows were written down and not measured. Each is in its
table's `dropped` list with its reason, and each guard has a test that names
it. They ranked below the 25 because the cost of each is a label on a row
that is listed either way, a second arm of a guard family already measured,
or a guard on a file the driver's null control does not cover.

- Table a: a former place whose own identifier is a band of the declaring
  bucket, band names counted live only where bands are, and one identifier
  declared by two buckets.
- Table b: the verdict reason on a listed track, a track holding a band
  beside the former place read as holding only the former place, and the
  tree path's own listing, which M7 removes one step earlier.
- Table c: an unclaimed word keyed on its case fold, only the named genres
  becoming check rows, and `rates = false` on the promoted bucket, which is a
  line of the template and not of a Python file.

## What no row measures

The template itself. The driver's null control is a comment appended to a
Python target, so no row mutates `taxonomy.default.toml`. What holds its
lines is the parity suite, which asks the frozen legacy code which strings it
filed in the old playlist and holds the new bucket's aliases equal to that
set, and the loader's refusals, which fire on the shipped file if a line of
the former place is wrong.

## The second review round, and what `r797-d` is

The first three tables were measured after the first fix round. The second
round then moved the line three rows mutate: T9, a former place competing
where it sits as well, now a line of the index the loader builds, M6, a track
listed once and not beside its move, whose guard was replaced by the rule that
a place is settled in one bucket, and M8, the reason a file the census could
not read is listed under. `r797-d` is the same three guards against the lines
as they stand, each row naming the one it measures again: 3 rows, 3 killed,
null control 0 of 11,367 collected against 11,367. The other 22 rows' lines
did not move.

The guards the second round ADDED are past the cap and were not measured.
Each has a test that names it:

- a track with no reading leaving a former place for the no reading sub, and
  still left when it holds a stale band, four tests in
  `tests/test_adopt_former_place.py` beginning `test_a_track_with_no_reading`
  and `test_a_stale_band_with_no_reading`;
- the fallback tier not read as a genre naming a bucket,
  `test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`;
- a verdict on the holding bucket,
  `test_a_verdict_on_the_holding_bucket_is_the_reason_a_track_there_is_left`;
- a former place held twice not listed beside the move that leaves it,
  `test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`;
- a too coarse word counted apart, and the spellings routing does not file
  under a sub named on its row, two tests in `tests/test_report_genres.py`;
- what decided a move with no reading, asserted in the first of the tests
  above. That one came from the author's own read after the review and not
  from a finding.
