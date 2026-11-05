# R-1264 mutation tables, read

Two tables, the author's and not independent, measured by `scripts/mutate.py`
on the cloud container, so a Linux measure of a macOS suite, green net of the
machine's failures.

`r1264.md`, at `eab4de53`: 24 rows over `sync/pair_cli.py` (22) and
`intake/cli.py` (2). Null control 0 of 16646. 20 killed, 4 zero, each zero
promoted to the full suite.

`r1264-composites.md`, at `fca9c16f`: M7 measured again over the test written
to kill it, killed 1. Null control 0 of 16647.

## The zeros

- M7, the account add filter on an unread key: every unread test synced over a
  base, which already strips the key. `fca9c16f` drives a first sync (a twin
  made off a short listing is held with no snapshot) and kills it.
- M16, the unread comparison on a pair this run part wrote: a residual file,
  since no resume test reaches a part written pair whose unread set moved. Its
  composite is M14, the same comparison on the unwritten path, killed 1.
- M23, a twice listed track's first mention's date: a U202 line moved into
  `_added_dates` unchanged. Its composite is M22, which drops the dates, killed
  6.
- M24, the linked content id on an unread item: maintainer facing, one line.

## The known failures the composites run subtracted

`.cloud-battery/baseline.txt` as measured on the base `7bbd2cbf`, 161 ids,
plus `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
which reddened the composites run's baseline. Run alone on the base and on
the branch it passed once and then failed, as the solutions entry on the inode
bound describes, and `TMPDIR=/var/tmp/r1264` no longer helps: files made there
now get inodes near 600,000, below the 2,000,000 bound. The id was added in a
scratch copy passed to the driver, with that measurement as its comment; the
measured baseline file was not edited. The first table ran with the measured
file alone and a green baseline.
