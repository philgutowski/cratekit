---
title: The CLI's portion narrowing in crate backup run is a second layer since U317, and kills no test
found: at the replay of U290's survey kill set, U337, 2026-11-25.
issue: no
---

**The mechanism.** u50-author W1 makes `if portion is not None:` in `src/cratekit/backup/cli.py` read `if False:`, so the CLI no longer narrows the plan to the named portion. Since U317 (`a94c7644`, a feature card outside U290) `plan_backup` plans only the named portion itself, so a backup asked for one portion still runs that portion alone, and the CLI's narrowing is a second layer covered by the first. Measured by the review on `tests/test_backup_cli.py`: at `a619edb0`, U317's parent, the mutant fails 14 tests against the unmutated control's 8, the six kills `docs/mutation/u337-replay/u337-survey-a.json` reads at the survey's commit; at `a94c7644`, 8 against 8. `u337-1.json` reads it zero on main.

**Measured cost.** None to a person: what a backup does is unchanged, and the refactor lost no kill here (`survey-before.json` names the row as changed by a feature card). A guard layer that kills nothing is maintainer facing (METHOD: remove each guard layer alone).

**Closes when:** the CLI's narrowing is removed as redundant with `plan_backup`'s, or a test drives the CLI with a plan that is not already narrowed and W1 is measured killed.
