# r925 mutation notes

Author's table, 20 rows, one pass, measured on head 7e6c33f. 18 killed, 2
zero, each zero promoted to the full suite of 12859. The author ran it, so a
zero reads as "the author could not kill it".

The unit writes one text file under download staging, or under `--out`, and
adds a read only field to `job show`. The table is scoped to the new guards
in `intake set`, `cli.jobs` and the renderer, and each zero gets one line.

The first launch of the driver was stopped by the harness's background time
limit after fourteen rows and left R1's mutation in `src/cratekit/cli/render.py`.
The file was restored from `git show HEAD:` and the table resumed with
`--resume`, which reused the fourteen measured rows; every row reports
`head_verified`.

- **J6_non_mapping_payload, zero.** A `tracks` payload that is not a mapping
  is a shape no shipped producer writes: `frozen_rows` always returns a dict.
  Maintainer facing, kept as a guard so a hand edited queue does not crash
  `job show`.
- **J7_non_mapping_row_dropped, zero.** Same reasoning for one frozen row
  that is not a mapping. Maintainer facing.

A row dropped before measuring: a resume that rewrites the tracklist. The
mutation that would produce it rebuilds an identification result inside
`_resume`, which is more code than the guard it tests, so the property is
held by `test_a_resumed_set_writes_no_tracklist` alone and is unmeasured by
this table.
