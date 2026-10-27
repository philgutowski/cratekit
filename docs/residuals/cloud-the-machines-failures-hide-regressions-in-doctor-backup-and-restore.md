---
title: On a Linux container the machine's known failures sit in doctor, backup and restore, so a regression there is invisible until a Mac runs the suite
found: at the Fable review of the cloud-first commits, 2026-10-27.
issue: no
---

**The mechanism.** The cloud battery subtracts the base's failures, and 122
of the 167 measured at `82bdfb3` are in five files: `tests/test_doctor.py`
50, `tests/test_restore_cli.py` 27, `tests/test_backup_comparison.py` 24,
`tests/test_restore.py` 8 and `tests/test_backup_cli.py` 8. A branch that
breaks one of those tests for its own reason lands with a clean cloud
battery and a mutation table that never credits the kill.

**Measured cost.** Measured over the baseline file; by design, not a defect
of the lane. Most of the doctor failures are root reading a directory whose
mode says it cannot be read.

**Closes when:** the suite's unreadable directory tests skip their
assertion only when the process can read past a mode, so they pass on the
container rather than fail there, or the cloud runs as a user that is not
root. Until then a card in doctor, backup or restore names the macOS battery
in its OWED paragraph. Ledger only.
