# Mutation table: u325-after-clean-p1

Measured by `scripts/mutate.py` on 2026-11-23 05:57 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 3.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-23 05:57 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 1, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r926.P1_config_path_leaves_root` | `src/cratekit/core/config.py` | user | 4 file(s) | 299 | 19 | killed |

## Row definitions

### `r926.P1_config_path_leaves_root`

The brief's path resolution mutant: config_path answers a folder outside every temporary root, as a missed redirect would

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `P1_config_path_leaves_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_config_update.py`, `tests/test_config_migration.py`
- Collected: 299 against a baseline of 299
- Kills: 19 (killed)
- Killed:
  - `tests/test_config.py::test_every_entry_with_a_named_accessor_resolves_to_the_same_path`
  - `tests/test_config.py::test_every_file_and_directory_this_unit_creates_is_private_under_any_umask`
  - `tests/test_config.py::test_the_default_location_round_trips_end_to_end`
  - `tests/test_config.py::test_the_migration_lock_file_is_one_of_the_files_that_audit_covers`
  - `tests/test_config_test_root.py::test_with_the_isolation_a_save_lands_in_the_temporary_root`
  - `tests/test_config_update.py::test_a_profile_change_made_while_the_wizard_was_deciding_survives_the_wizard`
  - `tests/test_config_update.py::test_a_profile_decision_is_stale_when_the_membership_moved_before_the_write`
  - `tests/test_config_update.py::test_a_refusal_inside_the_cycle_writes_nothing_and_releases_the_lock`
  - `tests/test_config_update.py::test_a_wizard_that_finished_while_a_profile_change_was_deciding_survives_it`
  - `tests/test_config_update.py::test_an_incomplete_document_reaches_the_revision_as_it_is_spelled`
  - `tests/test_config_update.py::test_an_invalid_revision_is_refused_before_a_byte_is_written`
  - `tests/test_config_update.py::test_save_takes_the_same_lock_so_it_cannot_land_inside_another_cycle`
  - `tests/test_config_update.py::test_the_wizard_does_not_hold_the_write_lock_while_it_asks`
  - `tests/test_config_update.py::test_three_real_processes_writing_at_once_all_keep_their_answers`
  - `tests/test_config_update.py::test_two_wizards_answering_one_key_differently_refuse_and_write_nothing`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    return state_path("config")
```

New text:

```
    return Path(os.sep, "cratekit-r926-mutant", "config.toml")
```

