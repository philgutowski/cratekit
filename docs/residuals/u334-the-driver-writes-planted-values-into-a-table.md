---
title: The mutation driver writes killing node ids as pytest names them, so a table quoting the portability guard's planted values fails the scan
found: at the kill set replay of #983, U334, 2026-11-24.
issue: no
---

**The mechanism.** `tests/test_portability.py::test_guard_covers_every_shipped_surface` is parametrized over planted offences, a home directory and access tokens among them, and pytest writes each case's values into its node id. `scripts/mutate.py` records the killing node ids whole in the table's `.json` and `.md`, so a replay row that test kills, `u28-skills-independent.X1_placeholder_exemption`, carried the planted home path and token into `docs/mutation/`, and `scripts/scan_repo.py` and `test_portability.py::test_the_repository_itself_is_clean` refused the tree. U334 wrote those values as placeholders by hand, as the u313 tables had done.

**Measured cost.** One red battery on the branch, caught before the merge; a maintainer hand edits a measured table. Nobody using the verbs pays.

**Closes when:** the driver writes a killing node id through the scan's own placeholder rule before recording it, or the guard's case ids are given by `ids=` naming the offence rather than its text, with a test that a replay of that row passes the scan. Ledger only: maintainer facing.
