# Mutation table: u311-replay-after-d1

Measured by `scripts/mutate.py` on 2026-11-23 04:02 UTC, branch `cloud/868-tools-backup-refactor` at `ad43c6e3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22415 collected. pytest invocations for this batch: 38.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `5224c6668bba`, and this tree is at `ad43c6e31902`).

Subset baselines: 2, each measured by this driver.

Known failures: 149 node ids whose failure is this machine's and not the tree's, read from a scratch file measured by `cloud_battery.py baseline` on the base with a stand in `rclone` on the path and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22415 against 22415. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r221-a.E1_outcome_forgets_the_run` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 721 | 5 | killed |
| `r221-a.E2_outcome_payload_drops_the_key` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 721 | 7 | killed |
| `r338-a.B3_capture_is_a_copy` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-a.B4_no_undo_archive` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r338-a.B5_one_mirror_for_every_library` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 4 | killed |
| `r338-a.B6_identity_interpolated_raw` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 3 | killed |
| `r338-a.B7_rehearsal_transfers_the_share` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 721 | 1 | killed |
| `r338-a.B8_contained_share_copied_twice` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 8 | killed |
| `r338-b.R1_missing_directory_refuses` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r338-b.R2_missing_directory_exit_moved` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 721 | 1 | killed |
| `r338-b.R4_empty_listing_read_as_held` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-b.R5_pulled_under_the_watch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-b.R6_switch_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-b.R7_restore_is_a_sync` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-b.R8_unmarked_snapshot_orphans_the_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r338-b.R9_contained_restore_asks_about_a_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-c.C1_absent_share_never_said` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 4 | killed |
| `r338-c.C2_carried_share_still_warned` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r338-c.C3_rehearsed_restore_pulls_the_share` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-a.M1_named_identity_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r388-a.M2_identity_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-a.M3_contents_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 2 | killed |
| `r388-a.M4_contents_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-a.M5_root_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-a.M6_root_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-b.M10_named_stamp_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-b.M11_db_folder_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-b.M7_share_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-b.M8_share_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-b.M9_root_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 721 | 1 | killed |
| `r388-c.M17_slug_respelled` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 721 | 4 | killed |
| `r1761.P11_move_nothing_dropped` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 405 | 1 | killed |
| `r1761.P12_history_census_ignored` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 405 | 1 | killed |
| `r1761.P13_history_record_ignored` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 405 | 142 | killed |

## Row definitions

### `r221-a.E1_outcome_forgets_the_run`

The outcome records False whatever the run was, which is the state before this unit: a rehearsal and a real run render identically

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E1_outcome_forgets_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_outcome_itself_records_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=dry_run)
```

New text:

```
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=False)
```

### `r221-a.E2_outcome_payload_drops_the_key`

The renderer stops carrying the flag, so every reader of a rendered run is back to guessing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E2_outcome_payload_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_the_outcome_itself_records_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        "dry_run": outcome.dry_run,
        "portions": [
```

New text:

```
        "portions": [
```

### `r338-a.B3_capture_is_a_copy`

_plan_database: capture the share with copy and not sync, so a grid rekordbox deleted stays in the mirror for ever and the mirror stops being the share

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B3_capture_is_a_copy`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`

Old text:

```
                    rclone, "sync", str(share), f"{kept}/current",
```

New text:

```
                    rclone, "copy", str(share), f"{kept}/current",
```

### `r338-a.B4_no_undo_archive`

_plan_database: drop the backup-dir, so a share emptied by a reinstall empties its only copy with nothing to undo it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B4_no_undo_archive`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`

Old text:

```
                    "--backup-dir", f"{kept}/archive/{stamp}",

```

New text:

```
(empty)
```

### `r338-a.B5_one_mirror_for_every_library`

share_destination: key every library's share under the one unrecorded folder, so two libraries under one snapshot root archive each other's grids

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B5_one_mirror_for_every_library`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_restore_puts_an_outside_share_back_beside_the_database`
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_analysis_store.py::test_an_unmarked_snapshot_pulls_this_librarys_share`
  - `tests/test_analysis_store.py::test_two_libraries_under_one_snapshot_root_keep_two_share_mirrors`

Old text:

```
    key = SHARE_UNRECORDED if marker is None else marker[len(IDENTITY_MARKER_PREFIX):]
```

New text:

```
    key = SHARE_UNRECORDED
```

### `r338-a.B6_identity_interpolated_raw`

share_destination: interpolate the configured identity as typed and unvalidated, so a value with a separator writes the share somewhere else on the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B6_identity_interpolated_raw`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_library_with_no_usable_identity_still_carries_its_share`
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_analysis_store.py::test_an_unmarked_snapshot_pulls_this_librarys_share`

Old text:

```
    key = SHARE_UNRECORDED if marker is None else marker[len(IDENTITY_MARKER_PREFIX):]
```

New text:

```
    key = SHARE_UNRECORDED if identity is None else identity
```

### `r338-a.B7_rehearsal_transfers_the_share`

TRANSFERRING_LABELS: leave the share's capture out, so a dry run really syncs gigabytes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-a.json`, row `B7_rehearsal_transfers_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_rehearsed_backup_transfers_no_share`

Old text:

```
        SNAPSHOT_SHARE,
        RESTORE_MIRROR,
```

New text:

```
        RESTORE_MIRROR,
```

### `r338-a.B8_contained_share_copied_twice`

_outside_share: read every layout as the outside one, so a share the mirror already carries is synced a second time

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B8_contained_share_copied_twice`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_portion_with_no_prune_command_carries_no_warning`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing`
  - `tests/test_analysis_store.py::test_a_contained_restore_neither_lists_nor_pulls_a_share`
  - `tests/test_analysis_store.py::test_a_contained_share_is_not_copied_twice`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`

Old text:

```
    if analysis_store.watch_roots(cfg) == (Path(cfg.library.root),):
        return None
    return analysis_store.share_root(cfg)
```

New text:

```
    if False:
        return None
    return analysis_store.share_root(cfg)
```

### `r338-b.R1_missing_directory_refuses`

share_is_held: stop reading rclone's missing directory exit as no mirror, so every backup older than this fix refuses its restore

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R1_missing_directory_refuses`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_the_share_is_listed_before_anything_is_cleared`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        return False
```

New text:

```
    if False:
        return False
```

### `r338-b.R2_missing_directory_exit_moved`

RCLONE_DIRECTORY_NOT_FOUND: move the exit to 4, rclone's file not found, a nearby value, so a missing mirror refuses

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-b.json`, row `R2_missing_directory_exit_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_the_share_is_listed_before_anything_is_cleared`

Old text:

```
RCLONE_DIRECTORY_NOT_FOUND = 3
```

New text:

```
RCLONE_DIRECTORY_NOT_FOUND = 4
```

### `r338-b.R4_empty_listing_read_as_held`

share_is_held: read a listing that names nothing as a mirror, so a copy from an empty folder is planned and reported as pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R4_empty_listing_read_as_held`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_lists_empty_is_absent_too`
  - `tests/test_restore_cli.py::test_a_restore_in_the_outside_layout_says_whether_the_share_came_back[-pulled1-absent]`

Old text:

```
    return bool(result.stdout.strip())
```

New text:

```
    return True
```

### `r338-b.R5_pulled_under_the_watch`

_plan_restore_inside_the_gates: stop withholding a landing place the analysis watch covers, the defect the built in review found: a live restore ends refused after the database is replaced

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R5_pulled_under_the_watch`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_that_would_land_under_the_analysis_watch_is_withheld_and_not_asked_about`
  - `tests/test_restore_cli.py::test_a_live_restore_in_the_outside_layout_withholds_the_share_and_closes_clean`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if not pull_share:
```

### `r338-b.R6_switch_ignored`

_plan_restore_inside_the_gates: ignore pull_share, so the bare metal recovery asks the remote about a share it will not pull and can be refused over it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R6_switch_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_caller_that_will_not_spend_the_database_half_is_not_refused_over_the_share`
  - `tests/test_restore_cli.py::test_a_database_that_was_never_on_the_lost_volume_is_not_recovered_onto_the_new_one`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if analysis_store.is_watched(cfg, landing):
```

### `r338-b.R7_restore_is_a_sync`

_plan_restore_inside_the_gates: pull the share with sync, which deletes every analysis file beside the restored database that the mirror never saw

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R7_restore_is_a_sync`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_restore_puts_an_outside_share_back_beside_the_database`
  - `tests/test_analysis_store.py::test_a_restore_writes_the_share_with_a_copy_and_only_beside_the_database`

Old text:

```
                        rclone, "copy",
                        f"{share_destination(cfg, identity=whose)}/current",
```

New text:

```
                        rclone, "sync",
                        f"{share_destination(cfg, identity=whose)}/current",
```

### `r338-b.R8_unmarked_snapshot_orphans_the_share`

_plan_restore_inside_the_gates: drop the fallback to this library's identity, so a snapshot whose marker failed to write looks for its share under the unrecorded folder

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R8_unmarked_snapshot_orphans_the_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_unmarked_snapshot_pulls_this_librarys_share`

Old text:

```
        whose = resolved.recorded_volume or cfg.library.volume_id
```

New text:

```
        whose = resolved.recorded_volume
```

### `r338-b.R9_contained_restore_asks_about_a_share`

_plan_restore_inside_the_gates: treat every layout as the outside one on restore, so a contained library lists and pulls a share mirror it never wrote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R9_contained_restore_asks_about_a_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_contained_restore_neither_lists_nor_pulls_a_share`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`

Old text:

```
    share = ShareRestore.MIRRORED
    if _outside_share(cfg) is not None:
```

New text:

```
    share = ShareRestore.MIRRORED
    if True:
```

### `r338-c.C1_absent_share_never_said`

absent_analysis_share: never warn, so an outside share that is not a directory reads as a share that was carried

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C1_absent_share_never_said`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_that_is_not_there_is_said_and_not_synced`
  - `tests/test_analysis_store.py::test_the_absent_share_warning_survives_a_refused_database_portion`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
```

New text:

```
    share = _outside_share(cfg)
    if True:
        return ()
```

### `r338-c.C2_carried_share_still_warned`

absent_analysis_share: warn whenever the share is outside the root, carried or not, which is the retired warning back under a new code

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C2_carried_share_still_warned`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`

Old text:

```
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
```

New text:

```
    share = _outside_share(cfg)
    if share is None:
        return ()
```

### `r338-c.C3_rehearsed_restore_pulls_the_share`

TRANSFERRING_LABELS: leave the share's restore out, so a rehearsed restore really downloads it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-c.json`, row `C3_rehearsed_restore_pulls_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_rehearsed_restore_transfers_no_share`

Old text:

```
        RESTORE_DATABASE,
        RESTORE_SHARE,
    }
```

New text:

```
        RESTORE_DATABASE,
    }
```

### `r388-a.M1_named_identity_listing_back_to_absence`

A named snapshot whose identity marker listing exits 1 raises no-snapshot-available again, the defect the unit fixes

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M1_named_identity_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`
  - `tests/modules/test_tools.py::test_an_identity_listing_that_fails_is_not_read_as_an_unmarked_snapshot`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed, so which library
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed, so which library
```

### `r388-a.M2_identity_listing_message_reworded`

Reword could not be listed to could not be read in the identity listing refusal (R-387's row)

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M2_identity_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
could not "
            f"be listed, so which library
```

New text:

```
could not "
            f"be read, so which library
```

### `r388-a.M3_contents_listing_back_to_absence`

A named snapshot whose db folder listing exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M3_contents_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_snapshot_that_cannot_be_listed_refuses_before_clearing`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed; a restore
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the snapshot {snapshot} under {cfg.backup.db_dest_root} could not "
            f"be listed; a restore
```

### `r388-a.M4_contents_listing_message_reworded`

Reword could not be listed to could not be read in the contents listing refusal, the sidecar row R-387 recorded as G9

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M4_contents_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`

Old text:

```
could not "
            f"be listed; a restore
```

New text:

```
could not "
            f"be read; a restore
```

### `r388-a.M5_root_listing_back_to_absence`

A snapshot root listing that exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M5_root_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_root_that_cannot_be_listed_is_not_reported_as_empty`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the dated database snapshots under {root} could not be listed
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the dated database snapshots under {root} could not be listed
```

### `r388-a.M6_root_listing_message_reworded`

Reword could not be listed to could not be read in the root listing refusal

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M6_root_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_root_that_cannot_be_listed_is_not_reported_as_empty`

Old text:

```
snapshots under {root} could not be listed, so 
```

New text:

```
snapshots under {root} could not be read, so 
```

### `r388-b.M10_named_stamp_absent_read_as_failure`

Drop the exit 3 branch on the identity listing, so a mistyped stamp sends the person to the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M10_named_stamp_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-identity-2026-08-01T000000Z-the snapshot 2026-08-01T000000Z was not found]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A mistyped or pruned stamp.
```

New text:

```
    if False:
        # A mistyped or pruned stamp.
```

### `r388-b.M11_db_folder_absent_read_as_failure`

Drop the exit 3 branch on the contents listing, so a cut off backup sends the person to the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M11_db_folder_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A backup cut off before its database folder was written.
```

New text:

```
    if False:
        # A backup cut off before its database folder was written.
```

### `r388-b.M7_share_listing_back_to_absence`

An analysis share listing that exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M7_share_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_could_not_be_listed_refuses_before_the_sidecars_go`

Old text:

```
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the analysis share mirror
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the analysis share mirror
```

### `r388-b.M8_share_listing_message_reworded`

Reword could not be listed to could not be read in the share listing refusal

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M8_share_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_could_not_be_listed_refuses_before_the_sidecars_go`

Old text:

```
could not "
            f"be listed (exit {result.returncode})
```

New text:

```
could not "
            f"be read (exit {result.returncode})
```

### `r388-b.M9_root_absent_read_as_failure`

Drop the exit 3 branch on the root listing, so a root no backup wrote is a listing failure

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M9_root_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshots-None-no dated database snapshot was found]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A root no backup has written yet is an empty root, not a remote that
        # did not answer, and its answer is to take a backup.
        return ()

```

New text:

```
(empty)
```

### `r388-c.M17_slug_respelled`

Respell the enum value, so the engine raises a slug nothing reserved

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r388-c.json`, row `M17_slug_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 721 against a baseline of 721
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`
  - `tests/modules/test_tools.py::test_every_refusal_cause_has_a_reserved_exit_code`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
    SNAPSHOT_LISTING_FAILED = "snapshot-listing-failed"
```

New text:

```
    SNAPSHOT_LISTING_FAILED = "snapshot-listing-error"
```

### `r1761.P11_move_nothing_dropped`

_full_commands: a new library's mirror is not told to delete nothing, so a stray state folder archives the mirror

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P11_move_nothing_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 405 against a baseline of 405
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_the_first_backup_of_a_new_empty_library_runs`

Old text:

```
                *(MOVE_NOTHING if move_nothing else ()),
```

New text:

```
                *(()),
```

### `r1761.P12_history_census_ignored`

_history: the census is not read, so a failed run that removed the record leaves no history

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P12_history_census_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 405 against a baseline of 405
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_a_walk_that_refused_is_counted_so_the_floor_still_holds`

Old text:

```
    census = backup_record.read_census(cfg)
    if census is not None:
```

New text:

```
    census = backup_record.read_census(cfg)
    if False:
```

### `r1761.P13_history_record_ignored`

_history: the record is not read, so an upgrade from a record with no census has no history

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P13_history_record_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 405 against a baseline of 405
- Kills: 142 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`
  - `tests/modules/test_tools.py::test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup`
  - `tests/modules/test_tools.py::test_a_record_that_cannot_be_read_purges_nothing`
  - `tests/modules/test_tools.py::test_a_refused_portion_leaves_its_previous_age_untouched`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive`
  - ... and 127 more, see the JSON sidecar

Old text:

```
        manifest is not None
        and manifest.library_root == str(cfg.library.root)
```

New text:

```
        manifest is None
        and manifest.library_root == str(cfg.library.root)
```

