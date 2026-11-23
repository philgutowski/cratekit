# U326 mutation notes

The first table, twelve rows at `92ce20f`, measured two rows over the state
root and library root that `tempfile.mkdtemp` made under one session
directory (R1, both roots inside the base temp, 4 kills; R2, a state root
per test, 19 kills). That change was reverted at `83fd3f1` for what it did
to ext4's placement of each test's directory (the record says why), so the
rows went with it and the table here is the second, ten rows at `6983377`.

The second table's first run refused a red baseline read from `compare`'s
record on `6983377`, on
`tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`,
which passed alone three times on the branch and twice on the base: the inode
test known to be intermittent on ext4 under a parallel run (u282, u298). The
driver was run again with `--measure-baseline`, and its own baseline was
green. Nothing was written into the baseline file.

R5, the Discogs detonator's teardown failure, is the one zero, promoted to
the full suite in both tables. It is U283's, unchanged by this unit, and is
filed as a residual.
