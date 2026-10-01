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

The second review round's changes came after these tables. They are named in
the record with the tests that hold them.
