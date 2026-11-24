---
title: A replay row widened to the full suite can record an unrelated death as its kill
found: at the kill set replay of #981, U332, 2026-11-24.
issue: no
---

**The mechanism.** `scripts/mutate.py` promotes a row whose subset kills
nothing to the full suite, and counts any death there as the row's kill.
`u317.Q10_token_not_struck` (`_strike_token(cfg)` to `pass` in
`src/cratekit/modules/tools/backup.py`) names `tests/test_backup_quick.py` as
its subset, which errors at setup on a container without rclone, so the
driver widened it. In U332's before batch 1, on `324cafa`, the full suite
recorded one death,
`tests/test_jobs.py::test_everything_the_queue_writes_is_owner_only_under_any_umask`,
a test that drives only the job queue and never reaches the backup. The after
batch, whose row named that file, widened too and recorded none, so
`killset.py check` reads the row as lost. Two later full suite runs of the same
mutation on the base killed nothing, so the death did not reproduce: one
intermittent failure became a recorded kill.

**Measured cost.** None to a person using the verbs. The row's own killers,
`test_a_failed_run_by_another_installation_makes_the_next_run_full` and
`test_a_run_that_fails_strikes_the_token_from_the_library_fact`, kill it on
both sides once rclone is present (`docs/mutation/u332-replay-q10-rclone-before.json`
and `-after.json`, `check` exits 0 on the pair). The cost is a maintainer
reading a lost kill that is not one, and the reverse: a kill recorded on an
intermittent death stands for a guard no test holds.

**Closes when:** a promoted row's death is confirmed by running the dying
tests again under the mutation, or a death in a test that never imports the
mutated module is reported apart from the kill. Ledger only: maintainer facing.
