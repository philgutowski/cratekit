---
title: About 140 backup and restore tests are the machine's on a cloud container, because rclone is not installed there
found: building #868, U311, 2026-11-22.
issue: no
---

**The mechanism.** The cloud container has no `rclone` on the path, and
installing it from a session was refused. Every test that resolves the
program before its own stand in answers fails on the base, so
`scripts/cloud_battery.py baseline` records it as the machine's: 55 in
`tests/test_backup_quick.py`, 33 in `tests/test_backup_unproven_root.py`, 27
in `tests/test_restore_cli.py`, 24 in `tests/test_backup_comparison.py`, and
more in `test_restore.py` and `test_backup_cli.py`, of the baseline's 249.
`compare` then subtracts them from the branch, so a backup change can break
one unseen. U311 drove its backup and restore suites base against branch
with a stand in `rclone` on the path that exits 0: 24 files, the same 107
failures on both, the rest of them the root and stand in limits.

**Measured cost.** A cloud unit that touches the backup engine is proved by
its own base against branch run and the behaviour comparison, not by the
battery, for these tests.

**Closes when:** the cloud environment's setup script installs `rclone`, so
these tests run in the battery; an environment change for Phillip's approval,
not a code change. Ledger only.
