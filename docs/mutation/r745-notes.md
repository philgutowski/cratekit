# R-745 mutation tables, read

Three tables, all the author's and not independent, measured by
`scripts/mutate.py` on `relay/223`. Every row named its subset,
`tests/test_export_collection.py`, and the tempo row added
`tests/test_no_beatgrid_ever.py`. Null control 0 on every table, no collect
drift, every restore verified against `git show HEAD`. A zero on the subset
was promoted to the full suite before it was reported.

**`r745-a.md`**, 13 rows over `write/collection_export.py`. 12 killed.

**`r745-b.md`**, 12 rows: four over the emitter and eight over
`cli/export_collection.py`. 10 killed.

**`r745-c.md`**, the three zeros measured again, each after the test it
bought. 3 killed.

**28 rows were measured, which is 3 over the cap of 25.** The 25 are
distinct mutations. The 3 over it are the re-measures in table c. Three more
were considered and dropped at the cap, logged in `r745-b-rows.toml` with
the reason each ranked below it: the folder's write permission, the same
family as C7; the provenance value made safe, maintainer facing; and the
warnings, a report line.

Table a stopped once on the driver's state leak guard and was resumed. The
write was a `doctor` run record from outside the session. R-756.

## The zeros, each the author could not kill on the first pass

- **E2, a tombstoned membership row written back.** User facing. The
  fixture's only tombstone was a track, so its key was dropped as a member
  the collection does not hold, and a removed place in a list was never
  seeded. Bought
  `test_a_membership_somebody_removed_is_not_written_back_into_the_playlist`
  and the test beside it for a marker that cannot be read. 2 kills in table c.
- **C2, the check for an existing file ahead of the copy.** User facing.
  Covered by the exclusive create behind it, which is the composite C3, 2
  kills. What the first guard alone decides is that the database is not
  copied for a file that is taken. Bought
  `test_an_existing_file_is_refused_before_the_database_is_copied`. 1 kill
  in table c.
- **C7, a file standing where a folder should be.** User facing. Covered by
  the question behind it, since a file cannot be written into either, under
  the same slug with a sentence about permissions. Bought the assertion on
  the sentence. 1 kill in table c.

## What the tables do not reach

E6 moved the tempo constant and killed one test, the output check in the
verb's own suite. The source scan in `tests/test_no_beatgrid_ever.py` was in
the subset and did not die, which is what it is written to do: it refuses an
interpolated value and takes a literal, so a different literal passes it.
The output check is the one guard on the value itself.
