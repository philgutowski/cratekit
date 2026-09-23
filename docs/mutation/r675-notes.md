# Mutation notes: r675

Two tables, `r675.md` and `r675-b.md`, one pass each, the author's own. Every
zero reads as "the author could not kill it", not as "nothing can".

## The pass

`r675.md`: 23 rows, under the light cap, 19 over the unit's own diff in
`write/naming_cli.py` and `intake/repair_cli.py` and 4 over the guard's
existing layers, run after the review's fix round at `d29eb6c`. Subset of 2
files, the two suites that drive the referenced guard end to end, 128
collected on every subset row, baseline 10063, null control 0. Twenty one
killed on the subset, two promoted to the full suite and not killed.

## The two zeros, and what they were

`E1_existence_not_asked` dropped the existence half of dark, R-500's rejected
first cut, and `E3_not_a_path_is_dark` dropped the resolution half, so a row
the resolver calls not a path was dark too. Both are existing layers, and
both went unkilled for one reason: the new leaf rule shadowed them in every
fixture the suite had. A row whose file exists at the recorded path references
that file by its as recorded key, so the candidate is held and left out of
the leaf index, and the row's darkness never reaches a comparison. A colon
form row, `tidal:tracks:12345`, has no leaf any candidate carries. Under the
first table's fixtures each layer was a guard covered by another guard.

Neither is redundant on the tree. The existence test is what lets a track in
a downloads folder share its name with a library file the plan would rename:
without it the row is dark, its leaf matches, and the verb refuses over a
file it holds. The resolution test is what excuses a device relative row, no
leading slash, whose leaf is a candidate's. Each got the test that reaches it
alone, `test_a_row_whose_file_exists_elsewhere_does_not_hold_a_namesake_in_the_library`
and `test_a_device_relative_row_neither_blocks_nor_protects`, at `f5c4ce2`.

`r675-b.md` re-runs the two rows: both killed, one each, 130 collected on the
subset, baseline 10065, null control 0.

## What was not measured

No timing row, because the unit adds no bound with a coefficient. The 0.05
second read over 17341 rows and 54 candidates was measured once on the live
database copy and is recorded in the ledger as one number, not a rate.
