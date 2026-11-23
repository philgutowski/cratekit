# R-1890, each row's plant against the base's guard

The thirteen rows of `r1890-rows.toml` each plant a guard's forbidden shape
in a part of a split module (or, for P8, P10 and P12, an import of or an
accessor in one). `r1890.md` measures each killed on the branch at
`d508dbd5`. This note is the other half: the same plant against the guard as
it stood on the base, `9b7c76ab`, with the base's version of each named test
file and of `tests/_source_guards.py` put in place for the run and restored
after, driven on 2026-11-23 by a script in the session's scratch directory.
Every plant passed the base's guard, so each row's kill is the branch's
change and not a guard that already saw the parts.

| row | base guard run | result on the base |
|---|---|---|
| P1 | `test_rb_writer_guard.py::test_no_refusal_returns_a_bare_integer_or_raises_a_bare_exception` | 1 passed |
| P2 | the same | 1 passed |
| P3 | `test_rb_writer_guard.py::test_every_refusal_this_module_raises_has_a_reserved_code_and_a_remedy` | 1 passed |
| P4 | the same | 1 passed |
| P5 | `test_cli_contract.py::test_the_core_writer_never_learns_the_gates_name_or_any_flag_string` | 1 passed |
| P6 | the beat grid suite's two package wide soft delete tests, base `_source_guards.py` | 2 passed |
| P7 | the same | 2 passed |
| P8 | `test_sync_night.py::test_the_night_module_reaches_no_launcher_no_decide_and_no_acknowledgment` | 1 passed |
| P9 | `test_config.py::test_the_restore_unit_derives_its_target_set_rather_than_listing_it` | 1 passed |
| P10 | `test_label_heard.py::test_nothing_on_the_heard_path_reaches_rekordbox_a_grid_a_tempo_or_a_rating` | 1 passed |
| P11 | `test_process_guard.py::test_no_module_hardcodes_a_rekordbox_process_name_outside_the_one_list` | 1 passed |
| P12 | none, `tests/test_split_modules.py` is new | not applicable |
| P13 | `test_restore.py::test_the_convergence_fallback_expires_the_moment_both_modules_share_a_build` | 1 passed |
