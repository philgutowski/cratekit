# Mutation table: u325-after-deferred-01

Measured by `scripts/mutate.py` on 2026-11-23 04:28 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 8.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 04:28 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 2, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r592-b.B5_step_names_no_file` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.S6_the_named_decision_is_withdrawn` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 10 | killed |
| `u96-a.A13_completed_halves_recorded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 98 | 1 | killed |
| `u27-restore-cli-author.S1_plan_takes_its_own_lock` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 257 | 10 | killed |

## Row definitions

### `r592-b.B5_step_names_no_file`

rerun_step: say the database rather than its file name, so the step does not say which file to remove

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B5_step_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
        f"before running the recovery again, remove {database_target.name} and any "
```

New text:

```
        f"before running the recovery again, remove the database and any "
```

### `u27-restore-cli-author.P3_convergence_is_reported_for_a_run_that_spent_no_capture`

Answer the capture restore's own question when no capture restore happened

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `P3_convergence_is_reported_for_a_run_that_spent_no_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`

Old text:

```
    if outcome is not None:
        totals["converged"] = outcome.converged
        totals["outstanding"] = len(outcome.outstanding)
```

New text:

```
    totals["converged"] = outcome.converged if outcome is not None else True
    if outcome is not None:
        totals["outstanding"] = len(outcome.outstanding)
```

### `u27-restore-cli-author.S6_the_named_decision_is_withdrawn`

Tell the off-machine restore no decision exists, which R33 makes it refuse on

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S6_the_named_decision_is_withdrawn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_report_names_the_snapshot_that_arrived`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled`

Old text:

```
                    confirmed=True,
```

New text:

```
                    confirmed=False,
```

### `u96-a.A13_completed_halves_recorded`

Never record a completed half, so a database failure does not say the mirror arrived

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A13_completed_halves_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
            completed.append(half)
```

New text:

```
            pass
```

### `u27-restore-cli-author.S1_plan_takes_its_own_lock`

Let the off-machine PLAN acquire the library lock itself instead of taking the open guard

- File: `src/cratekit/session/restore_cli.py`
- Source: `u27-restore-cli-author.json`, row `S1_plan_takes_its_own_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 257 against a baseline of 257
- Kills: 10 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_rehearsal_is_still_refused_while_rekordbox_is_running`
  - `tests/test_restore_cli.py::test_a_target_directory_that_does_not_exist_is_still_the_absent_refusal`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_report_names_the_snapshot_that_arrived`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled`

Old text:

```
                    include_mirror=include_mirror,
                    gates=held.guard,
```

New text:

```
                    include_mirror=include_mirror,
```

