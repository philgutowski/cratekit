# R-773 mutation tables, read

Two tables, both the author's and not independent, measured by
`scripts/mutate.py` on `relay/229`. Every row named its subset,
`tests/test_export_collection.py`, and the proof row added
`tests/test_intake_imported.py`. Null control 0 on both tables, 10,903
collected against 10,903, no collect drift, every restore verified against
`git show HEAD`.

**`r773-a.md`**, 14 rows over `write/collection_export.py`: eleven over the
new guards in `mounted_location` and `render`, three over guards the unit
already had. 14 killed.

**`r773-b.md`**, 12 rows: ten over `cli/export_collection.py`, one over the
registry entry, one over the proof in `intake/imported_cli.py` that the
landing tests rest on. 12 killed.

**26 rows were measured, which is 1 over the cap of 25.** The count was not
added up across the two files before the second ran. All 26 are distinct
mutations. Two more were considered and dropped, logged in
`r773-b-rows.toml` with the reason each ranked below the cap.

**No zero, and that reads as the author could not find one.** It is not a
claim that there is none. Two rows would have been zeros and were met before
they were measured, which a reader should know:

- **M11, the order the prefixes are named in.** The mixed row test held one
  prefix under no rule, so nothing decided the order. Two rows under a second
  prefix were added before the table ran. 1 kill.
- **S1, the sample row over `is_file_path`.** First written as a mutation no
  test input could tell from the original, a value opening with a slash that
  is also a location. Replaced by one that takes a streamed track as a path.
  5 kills.

Table a stopped once on the driver's state leak guard, at its fourth row, and
was resumed. The write was an `adopt.move` run record made by an attended
session on the installed copy, from outside this session. R-756 again. Table
a was resumed a second time after the emitter's outcome type was renamed,
which changed the text of four rows, and those four were measured again.

## What the tables say beyond the counts

- **M3 and M4, the finding itself, kill 5 each and not 13.** Writing a placed
  row as recorded fails the landing and its import proof on the moved layout,
  the literal location test, and three emitter tests. The other eight verbs
  that take an export pass on the moved layout either way, because what each
  asserts does not depend on where a location points. They hold "unchanged
  results", which is what the brief asks of them. They do not hold the fix.
- **C1, an empty prefix map handed to the emitter, kills 3.** The verb level
  composite for it is P1: with the proof itself granted for any export, 7
  tests die across the two files, so the import proof is what the landing
  tests are measuring and not the export's shape.
