---
title: The reservation guards read Refusal names only in the module that declares Refusal, so the restore and database plans U311 moved to backup_snapshot.py are outside them
found: at the review of #868, U311, 2026-11-22.
issue: no
---

**The mechanism.** `tests/test_reserved_causes.py` resolves a `Refusal.X` name
only inside the module that declares the enum. U311 split the backup engine,
and the restore plan, snapshot resolution and the database capture plan now
live in `src/cratekit/modules/tools/backup_snapshot.py`, which imports
`Refusal` from `backup.py`. Two readings follow. The named cause population
for `modules/tools/backup.py` shrank from seventeen slugs to seven, and the
pin in `tests/ratchets/reserved_causes/modules.tools.py` was measured again to
match. And `test_no_module_in_the_package_keeps_a_second_reservation_table`
is blind there: driven at review, a `{Refusal.REKORDBOX_RUNNING:
ExitCode.PRECONDITION}` table appended to `backup.py` fails it, and the same
table appended to `backup_snapshot.py` passes it (a string keyed table there
is still caught).

**Measured cost.** None today: no second table exists and every refusal's
exit code is unchanged, which the behaviour comparison shows. A table added
to `backup_snapshot.py` later would go unseen.

**Closes when:** the reader follows a `Refusal` imported from the declaring
module, so a sibling's names join their population and the second table
guard reads them. The file is not U311's; the suite card #869 (U312) owns it.
Ledger only.
