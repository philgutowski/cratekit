# Rows driven by hand, before and after U298

Round one of U325's review found two gaps in the replay, each driven by hand
here at both commits with `drive_rows` (the row's own test files, one xdist
worker, `PYTHONDONTWRITEBYTECODE=1`, run unmutated and mutated; a death is a
test that fails mutated and passes unmutated, so the machine's own failures
cancel; each source restored and read equal to `git show HEAD` afterwards).
The `-before` files ran on `539638eb`, the `-after` files on `db120fdb`.

- **`src/cratekit/modules/outbound/shell.py`**, which U298's first fix round
  edited (a docstring) after #855 had written the replay's row files, so its
  14 recorded kills were never in them. `u325-shell-rows.toml` is what
  `killset.py rows` writes for the file at `539638eb`; each text stands once
  at both commits. All 14 are killed at both, by the same tests by name:
  `drive-shell-before.json`, `drive-shell-after.json`.
- **`u115.F17_bound_is_zero`**, in `src/cratekit/write/row_defaults.py`,
  read zero by `u325-before-l-06` because its one killing test,
  `tests/test_repair_rows.py::test_the_real_bound_is_a_fresh_files_inode_and_leaves_no_file_behind`,
  is on the scratch copy of the machine's failures, although it passes alone
  on this container. Driven here it is killed by that test at both commits:
  `drive-f17-before.json`, `drive-f17-after.json`.

So neither gap hides a lost kill.
