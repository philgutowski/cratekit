# U965, notes on the mutation tables

Two tables, since no container compiles Swift: `u965.md` measures the Python
fixture guard, `tests/test_app_fixtures.py` and its three fixtures, with
`scripts/mutate.py`; `u965-swift.md` measures the Swift guards in
`app/Sources/CrateEngine/`, each reverted in its own pushed commit and read on
the App workflow.

**The Python table's baseline.** The driver first refused at `00d899e1`,
reading the battery's compare at that commit, which had found R-1413's inode
bound test, `tests/test_repair_rows.py::test_an_id_above_the_bound_that_is_the_files_inode_is_not_random`,
failing. That test failed alone 4 of 4 times on the base commit `60863868`
too, a new file's inode on this container's ext4 near 650,000 wherever it was
made (`/tmp`, `/var/tmp`, the home and every other writable directory tried),
under the test's 2,000,000 bound, and it passed in two of the four full runs
made here, so it is the machine's. The driver was run again with
`--measure-baseline` at `d7cae1cc`, measured a green full baseline net of the
247 known failures as measured, and every row ran. No id was written into the
known failures file.

**The two zeros**, each maintainer facing:

- `N4_resolved_roots_not_fixed` kills nothing on Linux, where the temporary
  directory is no symlink, so its resolved form equals the form given. On
  macOS `/var` is a symlink to `/private/var`, and a path a verb resolved
  would keep the run's temporary root without this line; unmeasured here,
  and read when the Mac's standing battery runs `tests/test_app_fixtures.py`.
- `C2_inventory_subset` kills nothing because no stray fixture exists; the
  equality it weakens is what fails on one, driven by review round one with a
  `.DS_Store`, which the fix round now passes over as hidden.
