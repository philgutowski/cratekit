# U87 mutation tables, read

Three files, `u87.md`, `u87-b.md` and `u87-c.md`, 13 rows in all over the
guards U87 wrote in `src/cratekit/write/routing_cli.py` for the rating pass of
`route inbox --export`, plus two existing guards sampled: the star curve's
boundary in `core/routing.py` and the rating writer's id filter in
`write/rbxml.py`. Split so each batch finishes inside one foreground call. Two
rows were considered and dropped, logged in `u87-b-rows.toml`: the rated total
taken from the plan rather than the writer, and the ratings applied before the
membership. Both are equivalent on every reachable input, for the reasons given
there.

**12 of 13 rows kill. The one zero is a maintainer row, promoted to the full
suite by the driver, and every row's restore was verified against HEAD.** These
are the author's own tables, so a zero reads as "the author could not kill it".

Every user surface row kills. G8, rating only the first collection row that
names a file, killed nothing on its first run in `u87-b.md`. A test was added,
`test_two_rows_naming_one_file_are_both_rated`, and the row re-run alone in
`u87-c.md` kills one.

The zero, one line:

- **S2, the rating writer's id filter.** No test hands the writer an id the
  collection lacks, and U87's caller cannot: every planned id is a collection
  row of the same bytes.
