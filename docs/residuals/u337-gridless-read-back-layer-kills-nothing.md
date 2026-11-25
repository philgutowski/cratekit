---
title: The read back layer of assert_created_rows_are_gridless kills no test, at the survey's commit or on main
found: at the replay of U290's survey kill set, U337, 2026-11-25.
issue: yes
---

**The mechanism.** `assert_created_rows_are_gridless` in `src/cratekit/core/rb_writer.py` reads each row this session created back from SQL and refuses one carrying an analysis value. Two recorded guards of that read back are killed by no test: r746-a G7 (`if value not in EMPTY_ON_CREATE:` made `if False:`, so a value read from SQL is never a violation) and r746-d G5 (a content row held to the playlist tables' five columns, so a key or a rate rides in). Their recorded killers, `tests/test_intake_land_native.py::test_an_analysis_value_reaching_the_row_is_refused_from_sql_before_the_commit` and `::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`, run and pass on Linux, and pass under either mutant: the taint they plant is refused by another layer first, so this layer, removed alone, is covered by nothing (METHOD: remove each guard layer alone).

**Measured cost.** Measured, not driven to a user: each mutant read zero on the full suite at `bd7fe681` (`docs/mutation/u337-replay/u337-1.json`) and at the survey's commit `ff8e5ec` (`u337-survey-a.json`); the one kill under U290, in U298's partial table, was all `tests/test_config_test_root.py`, the r926 folder. A guard on the guarded writer's path, the absolute rule against writing a beat grid, kills nothing (board bar d). Which layer refuses the taint first, and whether a planted value can reach SQL past it, is unmeasured.

**Closes when:** a test plants an analysis value that only the SQL read back can see (past the in memory judge and any later check) and both rows are measured killed, or the layer is shown redundant and removed with a composite naming what covers it.
