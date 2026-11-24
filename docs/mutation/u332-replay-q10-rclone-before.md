# Mutation table: u332-replay-q10-rclone-before

Measured by `scripts/mutate.py` on 2026-11-24 09:04 UTC, branch `HEAD` at `324cafa5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 3.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-24 09:04 UTC for commit `324cafa562b9`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 1, each measured by this driver.

Known failures: 102 node ids whose failure is this machine's and not the tree's, read from `known-rclone.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u317.Q10_token_not_struck` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 143 | 2 | killed |

## Row definitions

### `u317.Q10_token_not_struck`

run_backup: the record's token stays in the library's fact while a run sends, so a failed run of another installation leaves its record trusted (round two's finding)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q10_token_not_struck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`, `tests/test_jobs.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_failed_run_by_another_installation_makes_the_next_run_full`
  - `tests/test_backup_quick.py::test_a_run_that_fails_strikes_the_token_from_the_library_fact`

Old text:

```
                    _strike_token(cfg)
```

New text:

```
                    pass
```

