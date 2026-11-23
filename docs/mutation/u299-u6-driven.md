# U299 row U6, driven by hand

The driver measured row U6 (`_library` drops the medium an entry names, so
every library entry reads as a file) at `c6164121` and it killed nothing on
the full suite, as `u299.md` records. No test held the medium of a library
entry. `tests/test_config.py::test_a_directory_entry_is_declared_a_directory_under_either_root`
was added for it on the branch, one installation and one library directory
entry each, twice.

Driven on the branch by hand with the same substitution in
`src/cratekit/core/state_files.py`, `medium=medium` under `root=StateRoot.LIBRARY`
replaced by `medium=Medium.FILE`, then `tests/test_config.py` and
`tests/test_snapshot.py` run with `-n 4`, the file restored after and checked
clean against `git status`:

    FAILED tests/test_config.py::test_a_directory_entry_is_declared_a_directory_under_either_root[session_log]
    FAILED tests/test_config.py::test_a_directory_entry_is_declared_a_directory_under_either_root[snapshots]

Read as killed by hand, two deaths, not by the driver.
