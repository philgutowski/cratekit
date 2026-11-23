---
title: The analysis store's source scan of the backup engine reads backup.py by name, so the restore plan U311 moved to backup_snapshot.py is outside it
found: at the review of #868, U311, 2026-11-22.
issue: no
---

**The mechanism.**
`tests/test_analysis_store.py::test_the_backup_module_moves_analysis_files_and_never_opens_one`
reads the source of `src/cratekit/modules/tools/backup.py` and refuses a call
that opens or writes an analysis file. U311 split the engine, and the restore
plan now lives in `backup_snapshot.py`. Driven at review: a
`target.joinpath("x.dat").write_bytes(b"")` placed at the top of
`_plan_restore_inside_the_gates` fails the test on the base, in `backup.py`,
and passes it on the branch, in `backup_snapshot.py`. The two guards of the
same shape in `tests/modules/test_tools.py`, U311's own file, were widened in
the same unit to walk every file the engine is split across.

**Measured cost.** None today: the planner writes no analysis file, and the
behaviour comparison shows every file a restore plan writes unchanged.

**Closes when:** the scan reads every `backup*.py` under `modules/tools`, as
the two `test_tools.py` guards now do. The file is not U311's; the suite card
#869 (U312) owns it. Ledger only.
