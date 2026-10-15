---
title: The account mirror copies the tree as it was before the same organize run's database writes, so the account lags rekordbox by one run
found: at the build of #326, U147, 2026-10-15.
issue: no
---

**The mechanism.** `crate organize` plans both areas, asks both gates, then
writes (`organize/cli.py`). The mirror step (`organize/account_mirror.py`) is
planned from the tree before the database area's adoption and filing write
to it, so a track the run files reaches the account at the next run. Driven:
`test_a_second_run_after_a_full_apply_plans_nothing` now plans mirror steps on
the second run and nothing on the third. Re-planning after the database apply
would write what no gate showed.

**Measured cost.** One sitting of delay for tracks the same run filed; nothing
false is said, since the gate shows the plan it will write. Options for the
author: a second account gate after the database apply, a mirror only rerun
at the end of a sitting (`crate organize --only mirror`, which works today),
or accept the lag.

**Closes when:** the author picks one. Ledger only: nothing is lost or misstated.
