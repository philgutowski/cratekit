---
title: Twenty three tests build a real Probes and read the suite's own install origin
found: at the review of #340, U159, 2026-10-28.
issue: no
---

**The mechanism.** `tests/test_backup_comparison.py`, `tests/test_cutover_cli.py`,
`tests/test_cli_contract.py`, `tests/test_config.py` and one test in
`tests/test_doctor.py` build `doctor.Probes()` with its defaults, so the new
`install_origin` seam reads the copy the suite runs on. Today that reads as an
index install because the source tree's egg-info comes first on the path, so
no test reaches `git ls-remote`.

**Measured cost.** None here: a spy over the full suite saw 0 release reads.
On a checkout without the egg-info and a copy installed from git, each of the
23 would run `git ls-remote` with a ten second timeout.

**Closes when:** those tests build their probes from `doctor_machines.green`
or pass the two release seams. Ledger only.
