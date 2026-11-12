# U256 mutation notes

Nine rows on the fixture database helper in `tests/test_rb_writer_db.py`, a
unit that changes tests only and writes or deletes nothing in the product,
so the table is sized as a read only one, measured at `0d2d72db`. Eight are
killed by the two focused files; the null control killed nothing in 18,654.

**T6 reads zero, and it is a maintainer facing backstop with no input.** The
refusal of a template build that left anything beside the database file
cannot be reached: a WAL build's last close folds the log into the main
file, and every probe build in both review rounds left the one file. Filed
as a residual.

**The known failures file was a scratch copy.** The driver was given a copy
of `.cloud-battery/baseline.txt` with one id appended by hand and its
measurement in a comment:
`tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
which failed alone on the base `f22557e9` three times of three, a fresh file
under this container's temporary directory getting inode 417,811 and one
under `/var/tmp` 615,956, both below the 2,000,000 bound, as the solutions
entry on the inode bound test records. The measured baseline file was not
edited.

The author ran this table; no independent table was run, so each zero reads
as the author could not kill it.
