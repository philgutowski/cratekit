# U126 mutation notes

The table in `u126.md` is the first batch, 22 rows, measured at 13:18 UTC on
2026-10-10: 19 killed and three zeros, all on user facing surfaces.

**F2_every_row_shows, zero, then a test.** Giving the link to a held row beside
an added one changed nothing any test read. The mixed add and present test now
asserts the held row's columns name no ContentLink and the added row's carry
the library's value, committed as `test(u126)`. The rerun of F2 is NOT
MEASURED: two driver runs were stopped by the driver's own state check,
because a live `crate intake set` from the installed copy was writing the job
store and its scratch under `~/Library/Application Support/cratekit` at the
time. The kill is by construction of that assertion and has not been run
through the driver.

**R6_answer_land and R7_answer_file, zero, an equivalent mutant.** Each landed
item in the answer starts from the planned row, which already carries the
planned link, so dropping the read back value from the answer changes nothing
an OK answer can show. What makes that true is the read back check: the verb
exits OK only when every added row holds the planned value. Two composites
are written as rows, `C1_land_answer_unchecked` (the check skipped) and
`C2_file_answer_unchecked` (a row with no planned value let through), each
`pairs_with` its zero. NOT MEASURED, for the same reason as F2.
`R3_check_skipped`, the same edit as C1, was measured in the first batch and
killed by two tests, which is the evidence C1 would repeat.

To finish: rerun `scripts/mutate.py docs/mutation/u126-rows.toml --resume`
with no `crate` process running.
