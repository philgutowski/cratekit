# U60 mutation table: NOT MEASURED

**Verdict.** The author could not run the table. No row was measured, so this
unit carries no death counts at all, not even the author's. The rows are
committed in `docs/mutation/u60-rows.toml`, twenty rows and two dropped, and they
run unchanged with `./.venv/bin/python scripts/mutate.py docs/mutation/u60-rows.toml`
in any session that can hold one command for longer than ten minutes. The gap is
R-329.

## Why, measured on 2026-09-10

- The full suite on the committed tree: 7235 passed and 1 skipped, collected
  7236, in 357.79 seconds, wall 359.
- `measure_batch` runs a full suite baseline unconditionally at
  `scripts/mutate.py:957`, on every call, `--resume` included. `--resume` reuses
  finished rows and nothing else.
- The null control targets the first Python row's file and runs on that module's
  derived importer subset. No test imports `cratekit.deletion.cli`, so with a
  deletion row first the control's subset was empty and it ran the full suite.
- This task runs every command in the foreground under a 600 second ceiling, and
  a backgrounded driver is forbidden by METHOD's driver rules and by the task.
- **Attempt 1.** A `perl` alarm sent SIGINT at 570 seconds. The traceback put the
  interruption inside the null control, `measure_batch` at `:1002`. No sidecar
  was written, and `git status --porcelain` was empty after the driver's own
  restore.
- **Attempt 2.** The first row was moved to `src/cratekit/sync/cli.py`, whose one
  importing test file is `tests/test_incremental_sync.py`, so the control could
  run on a subset. SIGINT at 575 seconds. No row finished, no sidecar was
  written, and the tree was clean. The stage it was interrupted in was NOT
  captured, because the output was cut to its last twelve lines, so where the
  time went on this attempt is unmeasured.
- Promoting a zero needs a second full run inside the same call, so even a
  preflight that fit would have left every zero row unpromoted.

## What stands in, and it is not a table

Each branch the brief scopes the table to is DRIVEN through the shipped verb by at
least one test. That is coverage and not a death count, which is the difference
METHOD's mutation section exists to make.

| branch | driven by, in `tests/test_deletion.py` |
|---|---|
| confirm, trash | `test_delete_review_trashes_a_confirmed_file`: file moved, tombstone recorded, watermark at or past the handled row |
| confirm, abort | `test_delete_review_abort_moves_nothing`, and the abort half of `test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history` |
| empty plan, not a baseline | the second run of `test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`: ok, `items: []`, file in place |
| baseline | `test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`, `test_delete_review_exits_ok_after_the_recorded_decision` |
| display context | the R-134 test pins all three keys on both runs; `test_delete_review_prints_the_baseline_to_a_person_not_only_to_json` pins the rendered line |

One measurement does exist, taken by hand and not by the driver. The new
registry guard,
`tests/test_cli_contract.py::test_a_verb_declaring_the_queueing_contract_has_a_shell_that_queues`,
was run against the unchanged tree before the drop and failed naming
`delete.review` alone. That is the state row `G1_contract_restored` reproduces,
so G1 kills at least that one test. Every other row is unmeasured.
