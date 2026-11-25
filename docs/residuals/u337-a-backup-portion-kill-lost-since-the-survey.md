---
title: The named portion guard of crate backup run was killed at the survey and is killed by no test on main
found: at the replay of U290's survey kill set, U337, 2026-11-25.
issue: yes
---

**The mechanism.** u50-author W1 makes `if portion is not None:` in `src/cratekit/backup/cli.py` read `if False:`, so a backup asked for one portion runs the whole plan for every item. At the survey's commit `ff8e5ec` six tests of `tests/test_backup_cli.py` kill it on Linux (`docs/mutation/u337-replay/u337-survey-a.json`, among them `test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion` and `test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`). On main every one of the six still exists by name, runs, and passes under the mutant: u337-1 read it zero on the full suite at `bd7fe681`, and the review drove it again on main, the mutant's failures equal to the unmutated control's machine failures. None of the six is a known failure on this container.

**Measured cost.** The one kill of the survey's 7,093 rows this card found lost on Linux: point 5 of U290 does not hold whole. Which commit lost it is unmeasured; between `ff8e5ec` and main the backup verb changed under U317 (`a94c7644`, an unchanged library skipped) and R-1761 (`c8fc8b7d`, a root it cannot prove refused), and its suite under U311, U312 and U332 (shared drives and steps). A guard on a path that writes a backup kills nothing (board bar d); whether a person can be shown a whole backup when they asked for a portion, past the guard, was not driven.

**Closes when:** a test asks `crate backup run` for one portion and fails when the other half runs, and W1 is measured killed on main; or the guard is shown dead and removed with the reason.
