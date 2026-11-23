# Mutation table: u325-after-l-17

Measured by `scripts/mutate.py` on 2026-11-22 23:44 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 112.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 11, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u110-b.B1_pass_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 7 | killed |
| `u110-b.B2_name_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 27 | killed |
| `u110-b.B3_check_pass` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 5 | killed |
| `u110-b.B4_recheck_xml` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 1 | killed |
| `u110-b.B5_recheck_native` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 1 | killed |
| `u110-b.B6_intake_lock` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 1 | killed |
| `u110-b.B7_name_overrides` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 33 | killed |
| `u110-b.B8_shown_playlist` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 437 | 1 | killed |
| `u181.S3_stop_goes_on` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M18_left_open_taken` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M19_left_open_identity` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M20_cancelled_driven` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M21_all_cancelled_done` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M22_skip_failed` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M11_land_runs_named` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u183.M12_preflight_way_back` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M14_retryable_intake_continues` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M15_continue_command_words` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 9 | killed |
| `u183.M1_pass_run_as_given` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 16 | killed |
| `u183.M2_land_record_resolves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 3 | killed |
| `u183.M3_recorded_pass_needs_a_job` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M6_unreadable_record` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M7_remember_saves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M8_remember_called` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 5 | killed |
| `r261.W1_worker_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 2 | killed |
| `r261.W2_remedy` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.W3_retryable` | `src/cratekit/label/cli.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.D1_discovery_record` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `r261.D2_transient_class` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.D3_held_guard` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 1 | killed |
| `r261.R2_roster_keeps_discovery` | `src/cratekit/label/tidal_catalogue.py` | user | 4 file(s) | 522 | 3 | killed |
| `u75-a.A1_kind_filter` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A3_nothing_accepted_before_the_catalogue` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A5_only_the_seams_exception_is_gone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A6_no_identifier_is_not_asked_of_the_provider` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-a.A7_each_row_read_alone` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B11_write_failure_is_the_verbs_refusal` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B1_outage_threshold` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B3_only_a_provider_failure_counts` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B7_same_recording_listed_once` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u75-b.B9_name_digests_the_provenance` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 2 | killed |
| `u75-zeros.B6_missing_and_nothing_listable_refuses` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u294.M05_suggest_step_band` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M06_served_is_every_row` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 9 | killed |
| `u294.M07_followers_another_spelling` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M08_alias_files_stale_check` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M09_digest_drops_words` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M10_digest_drops_answers` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M11_unknown_word_accepted` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 4 | killed |
| `u294.M12_settled_answer_taken` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M13_unanswerable_accepted` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M14_answered_twice` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 2 | killed |
| `u294.M15_text_not_threaded` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M16_settled_unreached` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 3 | killed |
| `u294.M18_no_reload_after_words` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M20_abort_applies` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M24_notes_dropped` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 2 | killed |
| `u294.M25_folder_stale_check` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `r790-b.L1_guard_counts_held` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-b.L2_round_records_beyond` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 8 | killed |
| `r790-b.L3_set_passes_offer` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-b.L4_bound_is_said` | `src/cratekit/label/cli.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G1_offer_bounded_by_limit` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G2_entry_overrides` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 4 | killed |
| `r790-c.G3_offer_floor` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r790-c.G4_offer_read_back` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 5 | killed |
| `r790-c.G5_rename_keeps_offer` | `src/cratekit/label/registry.py` | user | 4 file(s) | 332 | 1 | killed |
| `r757-c1.S1_resume_drops_the_full_flag` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-c2.S5_unread_number_printed_as_zero` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-c2.S6_twin_in_the_other_mode_says_nothing` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 758 | 1 | killed |
| `u166.A11_warning_names_batch` | `src/cratekit/intake/land_cli.py` | user | 7 file(s) | 258 | 3 | killed |
| `u166.A1_parent_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A2_removed_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 2 | killed |
| `u166.A3_plain_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 23 | killed |
| `u166.A5_present_rows_too` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A6_always_create` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 2 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 5 | killed |
| `u166.A8_digest_key` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A9_reserved_batch` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u254.C1_append_unsynced` | `src/cratekit/core/config.py` | user | 4 file(s) | 952 | 1 | killed |
| `u254.C2_append_one_write` | `src/cratekit/core/config.py` | user | 4 file(s) | 952 | 1 | killed |
| `u254.C3_append_test_root` | `src/cratekit/core/config.py` | maintainer | 4 file(s) | 952 | 2 | killed |
| `u254.C4_append_not_append` | `src/cratekit/core/config.py` | user | 4 file(s) | 952 | 54 | killed |
| `r770-b.B1_landing_never_takes_the_native_path` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 59 | 40 | killed |
| `u161.L1_landing_pins_nothing` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u161.P6_screen_drops_path` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 59 | 3 | killed |
| `r746-b.N2_base_drive_swap_disabled` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `r746-b.N3_folder_path_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `r746-b.N4_device_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `r746-b.N5_present_file_planned_as_an_add` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 3 | killed |
| `r746-d.N1_first_device_wins` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 3 | killed |
| `u161.P1_path_back_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 5 | killed |
| `u161.P2_parent_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 4 | killed |
| `u161.P3_file_name_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.P4_device_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.P5_master_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.S1_playlist_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `u161.S2_columns_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `u212.N1_second_copy_compare` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |

## Row definitions

### `u110-b.B1_pass_names_file`

--pass no longer names the intake file, so sync mark cannot find the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B1_pass_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`
  - `tests/test_intake_land_names.py::test_a_second_landing_under_the_same_pass_is_refused_and_not_merged`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_for_the_date_and_tidal_playlists`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`
  - `tests/test_intake_land_names.py::test_sync_mark_and_export_archive_still_find_their_pass_from_the_intake_file`
  - `tests/test_intake_land_names.py::test_the_gate_screen_names_the_playlist_before_anything_moves`

Old text:

```
    if pass_name is not None:
        return pass_name
    if name
```

New text:

```
    if name
```

### `u110-b.B2_name_names_file`

--name alone no longer names the intake file, breaking a landing typed the old way

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B2_name_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 27 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_partly_imported_batch_is_not_imported`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_retire_that_cannot_rename_is_a_refusal_and_changes_nothing`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_a_stub_listing_is_refused_as_the_export`
  - `tests/test_intake_imported.py::test_a_verified_run_stays_open_with_its_placements_still_owed`
  - `tests/test_intake_imported.py::test_a_waiting_run_with_no_export_named_is_refused_and_says_what_to_pass`
  - `tests/test_intake_imported.py::test_an_export_taken_before_the_import_proves_nothing_and_changes_nothing`
  - `tests/test_intake_imported.py::test_an_intake_file_no_waiting_run_names_is_still_refused_as_the_export`
  - `tests/test_intake_imported.py::test_an_open_run_holding_a_capture_is_never_taken_for_a_landing`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - ... and 12 more, see the JSON sidecar

Old text:

```
    if name is not None:
        return name
    return default_name
```

New text:

```
    return default_name
```

### `u110-b.B3_check_pass`

A --pass holding a slash or nothing is not refused before the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B3_check_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[ padded]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[a/b]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[a\\b]`

Old text:

```
    _check_pass(pass_name)

```

New text:

```
(empty)
```

### `u110-b.B4_recheck_xml`

The xml landing does not ask again under the lock whether its default name is still free

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B4_recheck_xml`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_default_name_taken_after_the_gate_is_refused_under_the_lock`

Old text:

```
            _still_free(cfg, batch)

```

New text:

```
            pass

```

### `u110-b.B5_recheck_native`

The native landing does not ask again under the lock whether its default name is still free

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B5_recheck_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing`

Old text:

```
                _still_free(cfg, planned.batch)

```

New text:

```
                pass

```

### `u110-b.B6_intake_lock`

The landing takes only the batch lock and not the intake file's

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B6_intake_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`

Old text:

```
    with landing.batch_lock(batch), landing.intake_lock(stem):
```

New text:

```
    with landing.batch_lock(batch):
```

### `u110-b.B7_name_overrides`

--name is ignored and the default name is always taken

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B7_name_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_a_second_landing_under_a_held_batch_name_refuses_and_moves_nothing`
  - `tests/test_intake_land.py::test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output`
  - `tests/test_intake_land.py::test_another_spelling_of_a_held_batch_folder_is_refused`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_moves_nothing`
  - `tests/test_intake_land.py::test_the_gate_screen_a_person_reads_names_the_files_and_the_intake_file`
  - `tests/test_intake_land.py::test_the_lock_is_held_for_the_whole_of_the_apply`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_every_target_taken]`
  - `tests/test_intake_land.py::test_the_refused_item_is_marked_in_the_plan_payload`
  - `tests/test_intake_land_names.py::test_a_name_a_person_gives_may_be_landed_into_again`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        ctx.args.name
        if ctx.args.name is not None
        else batch_name.readable(
```

New text:

```
        batch_name.readable(
```

### `u110-b.B8_shown_playlist`

The xml gate screen no longer names the batch playlist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B8_shown_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 437 against a baseline of 437
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_the_gate_screen_names_the_playlist_before_anything_moves`

Old text:

```
        "playlist": planned.batch,

```

New text:

```
(empty)
```

### `u181.S3_stop_goes_on`

sync land _vocals: an answer of stop takes the pass on

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S3_stop_goes_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`

Old text:

```
    if option != WITHOUT_VOCALS_GO:
```

New text:

```
    if option is None:
```

### `u182.M18_left_open_taken`

_left_behind: name the pass's own jobs on the left open row too

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M18_left_open_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
    left = [hold for hold in holds if not taken or _run_of(hold.job) != taken]
```

New text:

```
    left = list(holds)
```

### `u182.M19_left_open_identity`

_left_behind: group by the label alone, so a typed URL and a sweep's id are two playlists

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M19_left_open_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        grouped.setdefault(hold.identity or hold.label(), []).append(hold)
```

New text:

```
        grouped.setdefault(hold.label(), []).append(hold)
```

### `u182.M20_cancelled_driven`

_intake: drive cancelled jobs with the rest, so a continued pass stops on a cancelled job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M20_cancelled_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
    live = [job for job in found if job.state is not jobs.JobState.CANCELLED]
```

New text:

```
    live = list(found)
```

### `u182.M21_all_cancelled_done`

_intake: go on when every job was cancelled, so the listing refuses a pass with nothing resolved

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M21_all_cancelled_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
        if not live:
            report.check(
```

New text:

```
        if False:
            report.check(
```

### `u182.M22_skip_failed`

_missing: list without --skip-failed, so a pass with a cancelled copy stops at the listing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M22_skip_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`

Old text:

```
        argv.append("--skip-failed")
```

New text:

```
        pass
```

### `u183.M11_land_runs_named`

_unknown_pass: name no land run beside a recent pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M11_land_runs_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    lands = _land_runs_of(passes)
```

New text:

```
    lands: dict[str, str] = {}
```

### `u183.M12_preflight_way_back`

_preflight: a rekordbox or backup refusal no longer ends with the command that comes back

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M12_preflight_way_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`

Old text:

```
        raise tail.with_steps(exc, f"then run it again: {again}") from None
```

New text:

```
        raise
```

### `u183.M14_retryable_intake_continues`

_intake: a retryable ended intake job stops as one that cannot continue, so its way on ends at the resume

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M14_retryable_intake_continues`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`

Old text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry))
```

New text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry), continues=False)
```

### `u183.M15_continue_command_words`

_continue_command: drop the flag, so every printed continuation starts a new pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M15_continue_command_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_an_unknown_id_refuses_before_any_step_and_names_the_recent_passes`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_two_earlier_passes_holding_open_jobs_are_a_choice_named_not_made`

Old text:

```
    return f"crate sync land --pass-run {pass_run}"
```

New text:

```
    return f"crate sync land {pass_run}"
```

### `u183.M1_pass_run_as_given`

_resolve: never take the given id as a pass run, so a pass id is looked up as a land record and refused

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M1_pass_run_as_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`
  - `tests/test_sync_land.py::test_a_job_another_driver_holds_ends_the_pass_with_that_drivers_refusal`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_failed_names_its_retry_not_a_continuation`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_left_open_row_names_each_playlist_its_age_size_and_copies`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if _pass_jobs(store, given, cfg):
            return given
```

New text:

```
        if False:
            return given
```

### `u183.M2_land_record_resolves`

_resolve: ignore the land run's recorded pass, so the land run's own id is refused as it was before U183

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M2_land_record_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if recorded:
```

New text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if False:
```

### `u183.M3_recorded_pass_needs_a_job`

_resolve: take a land run's recorded pass with no intake job of this library, so the pass fails at the fourth step again

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M3_recorded_pass_needs_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_land_run_whose_pass_no_intake_job_carries_is_refused_not_continued`

Old text:

```
            if _pass_jobs(store, recorded, cfg):
                report.check(
```

New text:

```
            if True:
                report.check(
```

### `u183.M6_unreadable_record`

_land_record: let a record that cannot be read raise out of the resolver

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M6_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    except (CratekitError, AttributeError, KeyError, TypeError, ValueError, OSError):
        return None
    return state if
```

New text:

```
    except KeyError:
        return None
    return state if
```

### `u183.M7_remember_saves`

_remember: record the pass on the run without saving, so a run that stops before the dispatcher saves keeps nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M7_remember_saves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
    gates.save(ctx.run)
```

New text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
```

### `u183.M8_remember_called`

sync_land: never record the pass on the land run

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M8_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
        if run_id:
            _remember(ctx, report, run_id)
```

New text:

```
        if False:
            _remember(ctx, report, run_id)
```

### `r261.W1_worker_refuses`

The worker returns success over a sweep that left something unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W1_worker_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
    if source.unread:
        _refuse_unread(
```

New text:

```
    if False:
        _refuse_unread(
```

### `r261.W2_remedy`

The refusal tells the person to resume even when only a missing method is unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W2_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        remedy=Remedy.RESUME_JOB if transient else Remedy.REPORT_DEFECT,
```

New text:

```
        remedy=Remedy.RESUME_JOB,
```

### `r261.W3_retryable`

The refusal is retryable whatever was unread

- File: `src/cratekit/label/cli.py`
- Source: `r261.json`, row `W3_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
        retryable=transient,
```

New text:

```
        retryable=True,
```

### `r261.D1_discovery_record`

_discover skips a failed listing without recording it, which is R-393 as it was

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D1_discovery_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`

Old text:

```
                unread.append(
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
```

New text:

```
                (
                    Unread(
                        artist=str(getattr(artist, "name", "") or artist_id),
```

### `r261.D2_transient_class`

_discover marks every listing failure transient, a listing that cannot page included

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D2_transient_class`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`

Old text:

```
                        transient=not isinstance(
```

New text:

```
                        transient=True or not isinstance(
```

### `r261.D3_held_guard`

_discover records a held artist the roster reads again (the review finding)

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `D3_held_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`

Old text:

```
                if str(getattr(artist, "id", "") or artist_id) in held_ids:
                    continue
```

New text:

```
                if str(getattr(artist, "id", "") or artist_id) in ():
                    continue
```

### `r261.R2_roster_keeps_discovery`

LabelRoster.unread keeps only its own missing listings and loses what discovery handed in

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r261.json`, row `R2_roster_keeps_discovery`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_failure_on_one_discovered_artist_skips_that_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_climbs_the_ladder_before_it_is_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`

Old text:

```
        self.unread = (*unread, *missing)
```

New text:

```
        self.unread = (*missing,)
```

### `u75-a.A1_kind_filter`

Drop the kind filter, so an accepted harvested label name, which shares the queue, is read as a release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A1_kind_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_harvested_label_shares_the_queue_and_is_not_a_release`

Old text:

```
        kinds=(sweep.KIND,),

```

New text:

```
(empty)
```

### `u75-a.A3_nothing_accepted_before_the_catalogue`

Remove the early return, so a queue with nothing accepted resolves the catalogue and spends a login

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A3_nothing_accepted_before_the_catalogue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_nothing_accepted_is_a_no_op_that_never_opens_the_catalogue`

Old text:

```
    if not accepted:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

New text:

```
    if False:
        # ASKED BEFORE THE CATALOGUE IS RESOLVED
```

### `u75-a.A5_only_the_seams_exception_is_gone`

Catch LookupError again instead of the seam's own class, the review's first finding

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A5_only_the_seams_exception_is_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_lookup_error_that_is_not_the_seams_own_is_never_read_as_a_gone_release`

Old text:

```
    except catalogue.ReleaseUnresolvable as exc:
        return _Failed(release, GONE, str(exc))
```

New text:

```
    except LookupError as exc:
        return _Failed(release, GONE, str(exc))
```

### `u75-a.A6_no_identifier_is_not_asked_of_the_provider`

Remove the empty identifier guard, so the provider is asked for a release with no name

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A6_no_identifier_is_not_asked_of_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_an_accepted_item_naming_no_release_is_a_named_failure`

Old text:

```
    if not release.release_id:
        return _Failed(release, NO_IDENTIFIER, "the review item names no release identifier")

```

New text:

```
(empty)
```

### `u75-a.A7_each_row_read_alone`

Let one unreadable row escape, which costs the run instead of one line

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-a.json`, row `A7_each_row_read_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_one_unreadable_row_is_reported_and_the_rest_of_the_release_still_lists`

Old text:

```
        except match.UnreadableList as exc:
            unreadable.append(str(exc))
```

New text:

```
        except ZeroDivisionError as exc:
            unreadable.append(str(exc))
```

### `u75-b.B11_write_failure_is_the_verbs_refusal`

Remove the OSError conversion, so a full disk reaches a person as an internal error

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B11_write_failure_is_the_verbs_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_write_the_disk_refuses_is_the_verbs_refusal_and_not_an_internal_error`

Old text:

```
        except OSError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

New text:

```
        except ZeroDivisionError as exc:
            # A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL.
```

### `u75-b.B1_outage_threshold`

Raise the outage threshold from three to thirty, a realistic slip, so a dead provider is asked about every release

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B1_outage_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_provider_that_stopped_answering_is_not_asked_about_every_release`

Old text:

```
OUTAGE_AFTER = 3
```

New text:

```
OUTAGE_AFTER = 30
```

### `u75-b.B3_only_a_provider_failure_counts`

Count a gone release towards an outage

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B3_only_a_provider_failure_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_a_gone_release_does_not_count_towards_an_outage`

Old text:

```
            in_a_row = in_a_row + 1 if outcome.kind == PROVIDER else 0
```

New text:

```
            in_a_row = in_a_row + 1
```

### `u75-b.B7_same_recording_listed_once`

Remove the match id dedupe, so a single and its album list one recording twice

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B7_same_recording_listed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_same_recording_on_two_releases_is_listed_once_under_the_first`

Old text:

```
            elif settled.match_id in seen:
                counts["duplicate"] += 1

```

New text:

```
(empty)
```

### `u75-b.B9_name_digests_the_provenance`

Digest the tracks alone, the review's fourth finding, so a corrected year meets the emitter's refusal

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-b.json`, row `B9_name_digests_the_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_approved.py::test_the_list_name_moves_with_anything_the_emitter_would_write`
  - `tests/test_label_approved.py::test_the_same_tracks_with_a_corrected_year_take_a_new_name_and_are_not_refused`

Old text:

```
        "provenance": [
            dataclasses.asdict(provenance[track["id"]]) for track in body["tracks"]
        ],
```

New text:

```
        "provenance": [],
```

### `u75-zeros.B6_missing_and_nothing_listable_refuses`

Remove the refusal for missing tracks none of which carries a provider identifier

- File: `src/cratekit/label/approved_cli.py`
- Source: `u75-zeros.json`, row `B6_missing_and_nothing_listable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_approved.py::test_missing_tracks_none_of_which_can_be_asked_for_is_refused_and_not_a_no_op`

Old text:

```
    if missing and not listed:
```

New text:

```
    if False:
```

### `u294.M05_suggest_step_band`

the suggest step plans at medium rather than the backlog's floor

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M05_suggest_step_band`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_the_suggest_step_plans_at_the_backlogs_floor`

Old text:

```
        band=backlog.FLOOR,
```

New text:

```
        band=suggest.MEDIUM,
```

### `u294.M06_served_is_every_row`

the rows step keeps every backlog row rather than the served ones

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M06_served_is_every_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 9 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_the_fourth_step_refusing_stops_the_campaign_after_the_words`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    served = frozenset(row.content_id for row in plan.rows if row.status == backlog.SERVED)
```

New text:

```
    served = frozenset(row.content_id for row in plan.rows)
```

### `u294.M07_followers_another_spelling`

the follow step writes a row whose file carries another spelling than the answer filed

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M07_followers_another_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`

Old text:

```
    narrowed = rows.narrowed(whole, keep - other)
```

New text:

```
    narrowed = rows.narrowed(whole, keep)
```

### `u294.M08_alias_files_stale_check`

the words step drops its check that the alias would retag the files the gate listed

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M08_alias_files_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`

Old text:

```
        if (planned.edit.display, files) != (shown.genre, shown.files):
```

New text:

```
        if planned.edit.display != shown.genre:
```

### `u294.M09_digest_drops_words`

the digest leaves out the words and their files, so a file that came to carry a word moves nothing

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M09_digest_drops_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`

Old text:

```
            "words": [word.to_json() for word in words],
```

New text:

```
            "words": [],
```

### `u294.M10_digest_drops_answers`

the digest leaves out the answers, so an answer changed between the gate and the apply is not stale

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M10_digest_drops_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_the_digest_moves_with_an_answer_a_proposal_or_a_row`

Old text:

```
            "answers": [answer.to_json() for answer in given],
            "words": [word.to_json() for word in words],
```

New text:

```
            "answers": [],
            "words": [word.to_json() for word in words],
```

### `u294.M11_unknown_word_accepted`

an answer naming no word the backlog holds is dropped rather than refused

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M11_unknown_word_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias0-folder0-leave_word0-names no word]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias1-folder1-leave_word1-names no word]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias2-folder2-leave_word2-names no word]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses_before_anything_is_written`

Old text:

```
            if _held_by_copy(declared, spelling, kind, genre):
```

New text:

```
            if True:
```

### `u294.M12_settled_answer_taken`

an answer to a settled word is dropped whatever it says, rather than refused

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M12_settled_answer_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias7-folder7-leave_word7-already has its one answer]`

Old text:

```
            if _same_as_settled(word, kind, genre):
```

New text:

```
            if True:
```

### `u294.M13_unanswerable_accepted`

an answer to a word neither verb takes is not refused

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M13_unanswerable_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias8-folder8-leave_word8-cannot be answered]`

Old text:

```
        if word.unanswerable is not None:
            raise _invalid(
```

New text:

```
        if False:
            raise _invalid(
```

### `u294.M14_answered_twice`

a word answered twice takes the last answer rather than refusing

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M14_answered_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias5-folder5-leave_word5-answered twice]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias6-folder6-leave_word6-answered twice]`

Old text:

```
        if word.spelling in found:
```

New text:

```
        if False:
```

### `u294.M15_text_not_threaded`

each word's edit is planned on the copy as it stands, not on the text the words before it leave

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M15_text_not_threaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_alias_to_the_folder_another_answer_makes_is_planned_on_that_folder`

Old text:

```
        text = edit.after
```

New text:

```
        text = text
```

### `u294.M16_settled_unreached`

the campaign runs a settled word's answer even when it moves no row

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M16_settled_unreached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    return [word for word in plan.words if word.settled and word.reached]
```

New text:

```
    return [word for word in plan.words if word.settled]
```

### `u294.M18_no_reload_after_words`

the rows that follow are planned on the taxonomy as it was before the words step wrote the copy

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M18_no_reload_after_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`

Old text:

```
            # THE COPY MOVED, so the rows that follow are planned on it.
            declared = active_taxonomy.load(cfg)
```

New text:

```
            # THE COPY MOVED, so the rows that follow are planned on it.
            pass
```

### `u294.M20_abort_applies`

an aborted gate goes on to the steps as if applied

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M20_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_declined_campaign_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=facts) != APPLY:
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=facts) not in (APPLY, "abort"):
```

### `u294.M24_notes_dropped`

the gate and the report carry none of the backlog's own notes

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M24_notes_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_catalogue_nobody_could_read_is_said_at_the_gate`
  - `tests/test_tag_campaign.py::test_the_gate_and_the_report_say_what_the_verbs_could_not_read`

Old text:

```
        if note["code"] in _CARRIED and note["code"] != backlog_cli.ROWS_JOINING
```

New text:

```
        if False
```

### `u294.M25_folder_stale_check`

the words step drops its check that the folder edit is the one the gate listed

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M25_folder_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_that_would_copy_another_bucket_after_the_gate_stops_the_words_as_stale`

Old text:

```
            if fresh != (shown.genre, shown.bucket, shown.like, shown.copy):
```

New text:

```
            if False:
```

### `r790-b.L1_guard_counts_held`

_refuse_unfinished: leave held releases out of the confirmed-none count, so a dead verifier reads as nothing new

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L1_guard_counts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_dead_verifier_on_a_later_sweep_refuses_rather_than_reporting_nothing_new`

Old text:

```
    unconfirmed = len(source.dropped) + source.held_unconfirmed
```

New text:

```
    unconfirmed = len(source.dropped)
```

### `r790-b.L2_round_records_beyond`

handle: record every round as nothing beyond

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L2_round_records_beyond`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_label_whose_window_is_already_held_records_its_beyond_with_nothing_filed`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                beyond=listing.beyond,
```

New text:

```
                beyond=0,
```

### `r790-b.L3_set_passes_offer`

registry_cmd set: drop --offer on the way to the store, so set reports an edit it never wrote

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L3_set_passes_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`

Old text:

```
            seed_artists=seeds,
            track_limit=track_limit,
            offer=offer,
```

New text:

```
            seed_artists=seeds,
            track_limit=track_limit,
```

### `r790-b.L4_bound_is_said`

_detail: stop saying the track limit bounds an offer

- File: `src/cratekit/label/cli.py`
- Source: `r790-b.json`, row `L4_bound_is_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`

Old text:

```
            + (f", bounded by the track limit to {bound}" if entry.offer > bound else "")
```

New text:

```
            + ""
```

### `r790-c.G1_offer_bounded_by_limit`

effective_offer: stop bounding the window by the track limit, so the increment slices what the listing reported

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G1_offer_bounded_by_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`

Old text:

```
    return min(offer, effective_limit(entry))
```

New text:

```
    return offer
```

### `r790-c.G2_entry_overrides`

effective_offer: ignore a label's own offer

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G2_entry_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_window_defaults_to_the_configuration_and_the_entry_overrides_it`

Old text:

```
    offer = entry.offer if entry.offer is not None and entry.offer > 0 else default
```

New text:

```
    offer = default
```

### `r790-c.G3_offer_floor`

check_offer: accept zero at the store

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G3_offer_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_an_offer_below_one_refuses_at_the_store`

Old text:

```
    if isinstance(offer, bool) or not isinstance(offer, int) or offer < 1:
```

New text:

```
    if isinstance(offer, bool) or not isinstance(offer, int) or offer < 0:
```

### `r790-c.G4_offer_read_back`

_entry_from: read every stored offer as unset

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G4_offer_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_offer_survives_a_rename_and_an_unrelated_edit`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_raising_a_label_offer_after_a_sweep_files_the_difference`
  - `tests/test_label_offer_window.py::test_the_registry_says_when_the_track_limit_bounds_an_offer`

Old text:

```
        offer=_coerce_int(raw.get("offer")),
```

New text:

```
        offer=None,
```

### `r790-c.G5_rename_keeps_offer`

rename: rebuild the entry field by field without the offer, the shape every copy had before

- File: `src/cratekit/label/registry.py`
- Source: `r790-c.json`, row `G5_rename_keeps_offer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_label_registry_verbs.py`
- Collected: 332 against a baseline of 332
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_label_offer_survives_a_rename_and_an_unrelated_edit`

Old text:

```
            current[label_id] = replace(existing, name=new_name)
```

New text:

```
            current[label_id] = LabelEntry(
                label_id=existing.label_id,
                name=new_name,
                match=existing.match,
                seed_artists=existing.seed_artists,
                track_limit=existing.track_limit,
            )
```

### `r757-c1.S1_resume_drops_the_full_flag`

backup_argv: never emit --full, so a resumed full job's command line is a fast one

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S1_resume_drops_the_full_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_full_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`

Old text:

```
    if payload.get(FULL):
        argv.append("--full")
```

New text:

```
    if False:
        argv.append("--full")
```

### `r757-c2.S5_unread_number_printed_as_zero`

comparison_warning: print a total that was not read as 0

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S5_unread_number_printed_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_sentence_never_prints_an_unread_number_as_zero`

Old text:

```
            return f"an unread number of {unit}"
```

New text:

```
            return f"0 {unit}"
```

### `r757-c2.S6_twin_in_the_other_mode_says_nothing`

_already_queued: drop the sentence saying the open job runs the other comparison, the review's fix

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S6_twin_in_the_other_mode_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_second_ask_in_the_other_mode_is_told_the_open_job_differs`

Old text:

```
    if asked_full is not None and asked_full != _is_full(job):
```

New text:

```
    if False:
```

### `u166.A11_warning_names_batch`

awaiting_analysis: name the batch playlist again instead of Analyze

- File: `src/cratekit/intake/land_cli.py`
- Source: `u166.json`, row `A11_warning_names_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
                f"{collection.analyze_name} playlist, which holds every row waiting "
```

New text:

```
                f"{collection.playlist} playlist, which holds every row waiting "
```

### `u166.A1_parent_check`

analyze_playlist: take a live Analyze anywhere, not only directly under the root

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A1_parent_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_analyze_playlist_outside_the_root_is_never_written_into`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") != str(root_id):
            continue
        if rb_writer.node_removed(row)
```

New text:

```
        if False:
            continue
        if rb_writer.node_removed(row)
```

### `u166.A2_removed_check`

analyze_playlist: take a removed Analyze as the queue

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A2_removed_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removed_or_smart_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_analyze_removed_after_the_approval_is_refused_and_nothing_lands`

Old text:

```
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
```

New text:

```
        if int(getattr(row, "Attribute", -1)) != 0:
```

### `u166.A3_plain_check`

analyze_playlist: take a folder or smart playlist named Analyze as the queue

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A3_plain_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removed_or_smart_node_named_analyze_is_never_written_into`

Old text:

```
        if rb_writer.node_removed(row) or int(getattr(row, "Attribute", -1)) != 0:
```

New text:

```
        if rb_writer.node_removed(row):
```

### `u166.A4_no_add`

apply_rows: add nothing to Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A4_no_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 23 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root`
  - `tests/test_inbox_analyzed.py::test_a_membership_whose_collection_row_is_missing_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_removed_or_smart_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_a_row_marked_analysed_with_no_analysis_path_stays`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_the_collection_already_held_is_not_added_to_analyze`
  - `tests/test_inbox_analyzed.py::test_a_row_with_an_analysis_path_and_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_a_second_clear_plans_nothing`
  - `tests/test_inbox_analyzed.py::test_a_second_landing_adds_its_own_beside_them_and_the_playlist_is_never_made_twice`
  - `tests/test_inbox_analyzed.py::test_a_track_held_twice_is_one_row_cleared_and_counted_once`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_an_analysis_finished_after_the_approval_is_refused_by_the_engine`
  - `tests/test_inbox_analyzed.py::test_an_analyze_playlist_outside_the_root_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_analyze_removed_after_the_approval_is_refused_and_nothing_lands`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
```

New text:

```
            if False:
                analyze = _analyze_row(db, plan, anchor)
```

### `u166.A5_present_rows_too`

apply_rows: add every row the plan names, present ones too

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A5_present_rows_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_the_collection_already_held_is_not_added_to_analyze`

Old text:

```
                        db, analyze, [content_id for _row, content_id in added_ids]
```

New text:

```
                        db, analyze, list(by_target.values())
```

### `u166.A6_always_create`

_analyze_row: make a new Analyze every landing

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A6_always_create`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_row_the_collection_already_held_is_not_added_to_analyze`
  - `tests/test_inbox_analyzed.py::test_a_second_landing_adds_its_own_beside_them_and_the_playlist_is_never_made_twice`

Old text:

```
    return found if found is not None else db.create_playlist(ANALYZE, parent=anchor)
```

New text:

```
    return db.create_playlist(ANALYZE, parent=anchor)
```

### `u166.A7_record_count`

apply_rows: record the batch's memberships only on success

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A7_record_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_of_five_adds_five_memberships_to_analyze_under_the_root`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
```

New text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships,
```

### `u166.A8_digest_key`

identity: leave the found Analyze out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A8_digest_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_analyze_removed_after_the_approval_is_refused_and_nothing_lands`

Old text:

```
    analyze = {"analyze": plan.analyze_playlist_id} if plan.to_add() else {}
```

New text:

```
    analyze = {}
```

### `u166.A9_reserved_batch`

plan_rows: let a batch take the name Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A9_reserved_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 258 against a baseline of 258
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_batch_named_analyze_is_refused_before_the_gate_and_nothing_moves`

Old text:

```
    if batch == ANALYZE:
```

New text:

```
    if False:
```

### `u254.C1_append_unsynced`

append_durable_bytes: return without syncing the appended record

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C1_append_unsynced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 952 against a baseline of 952
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_every_append_is_synced_before_the_mark_returns`

Old text:

```
            view = view[os.write(fd, view) :]
        os.fsync(fd)
```

New text:

```
            view = view[os.write(fd, view) :]
```

### `u254.C2_append_one_write`

append_durable_bytes: make one write call and drop what it did not take

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C2_append_one_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 952 against a baseline of 952
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`

Old text:

```
        while view:
            view = view[os.write(fd, view) :]
```

New text:

```
        if view:
            view = view[os.write(fd, view) :]
```

### `u254.C3_append_test_root`

append_durable_bytes: drop the test root refusal

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C3_append_test_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 952 against a baseline of 952
- Kills: 2 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_an_append_outside_every_temporary_folder_is_refused`
  - `tests/test_config_test_root.py::test_an_append_outside_the_root_is_refused_with_the_isolation_in_place`

Old text:

```
    _refuse_write_outside_test_root(path, system_temporary=True)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

### `u254.C4_append_not_append`

append_durable_bytes: open for writing at the start of the file rather than its end

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C4_append_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 952 against a baseline of 952
- Kills: 54 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_journal_this_process_never_wrote_appends`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_revert_after_a_partial_apply_restores_what_it_wrote`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY)
```

### `r770-b.B1_landing_never_takes_the_native_path`

intake_land: ignore the switch, so a native intake tree is landed through the bridge

- File: `src/cratekit/intake/land_cli.py`
- Source: `r770-b.json`, row `B1_landing_never_takes_the_native_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 40 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_changed_playlist_or_an_added_file_still_moves_the_digest`
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_default_name_taken_after_the_approval_is_refused_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_key_reaching_the_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_intake_land_native.py::test_a_landing_given_no_pass_names_none`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column`
  - ... and 25 more, see the JSON sidecar

Old text:

```
    if medium.native:
```

New text:

```
    if False:
```

### `u161.L1_landing_pins_nothing`

ask_then_write: pin nothing, so every native write's answer is free of the file again

- File: `src/cratekit/intake/land_cli.py`
- Source: `u161.json`, row `L1_landing_pins_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`

Old text:

```
            spec, plan=data, context=shown(rows), pinned={DATABASE_PIN: str(opened)}
```

New text:

```
            spec, plan=data, context=shown(rows), pinned={}
```

### `u161.P6_screen_drops_path`

collection_facts: show the root's name where the database path was, so the screen no longer says which file is written

- File: `src/cratekit/intake/land_cli.py`
- Source: `u161.json`, row `P6_screen_drops_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "reads and writes": str(rows.database),
```

New text:

```
        "reads and writes": str(rows.root_name),
```

### `r746-b.N2_base_drive_swap_disabled`

stored_folder_path: the mounted path is stored whatever the property table records

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N2_base_drive_swap_disabled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_stored_path_is_nfc_and_the_swap_is_anchored_on_a_whole_component`

Old text:

```
        if text == current or text.startswith(current + os.sep):
```

New text:

```
        if False:
```

### `r746-b.N3_folder_path_not_restamped`

_restamp: the row keeps the path the binding stored, the planned path is never put on it

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N3_folder_path_not_restamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`

Old text:

```
    if str(content.FolderPath) != row.folder_path:
        content.FolderPath = row.folder_path
```

New text:

```
    if False:
        content.FolderPath = row.folder_path
```

### `r746-b.N4_device_not_restamped`

_restamp: the row keeps the device the binding chose

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N4_device_not_restamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_rows_carry_the_library_device_and_not_the_bindings_first`

Old text:

```
    if str(content.DeviceID) != plan.device_id:
        content.DeviceID = plan.device_id
```

New text:

```
    if False:
        content.DeviceID = plan.device_id
```

### `r746-b.N5_present_file_planned_as_an_add`

plan_rows: a file the collection already holds is planned as an add, so it would be added twice

- File: `src/cratekit/intake/native.py`
- Source: `r746-b.json`, row `N5_present_file_planned_as_an_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`

Old text:

```
            action, why = (ADD if held is None else PRESENT), ""
```

New text:

```
            action, why = ADD, ""
```

### `r746-d.N1_first_device_wins`

choose_device: every device matches, so the first by identifier is stamped rather than the library's own. Measured again with the wrong device sorting first

- File: `src/cratekit/intake/native.py`
- Source: `r746-d.json`, row `N1_first_device_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_rows_carry_the_library_device_and_not_the_bindings_first`

Old text:

```
        (device for device in devices if dbid and str(device.MasterDBID) == dbid),
```

New text:

```
        (device for device in devices if dbid),
```

### `u161.P1_path_back_in_digest`

native.identity: digest str(plan.database) again, the line U161 removed, so a copy rehearsal can never match

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P1_path_back_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_decision_recorded_against_the_path_bearing_digest_is_stale_and_writes_nothing`
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "database": str(plan.database),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P2_parent_in_digest`

native.identity: digest the database's folder under another key, a path the old key's name check would not see

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P2_parent_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "where": str(plan.database.parent),
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P3_file_name_in_digest`

native.identity: digest the database's file name alone, which a copy named differently from master.db would not share

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P3_file_name_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_an_answer_given_over_one_file_is_stale_when_the_continuation_opens_another`
  - `tests/test_intake_land_native.py::test_the_same_files_against_a_copy_at_another_path_digest_equal_and_each_screen_names_its_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "file": plan.database.name,
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

### `u161.P4_device_out`

native.identity: drop the device, so an answer for one library is not stale for another with the same master id

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P4_device_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "master_db_id": plan.master_db_id,
```

### `u161.P5_master_out`

native.identity: drop the master id, the other half of the library identity that replaced the path

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `P5_master_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`
  - `tests/test_intake_land_native.py::test_the_engine_identity_names_the_device_and_master_id_and_no_database_path`

Old text:

```
        "device": plan.device_id,
        "master_db_id": plan.master_db_id,
```

New text:

```
        "device": plan.device_id,
```

### `u161.S1_playlist_out`

native.identity: drop the batch playlist's name from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S1_playlist_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`

Old text:

```
        "playlist": plan.playlist,
        "batch_playlist": plan.batch_playlist_id,
```

New text:

```
        "batch_playlist": plan.batch_playlist_id,
```

### `u161.S2_columns_out`

native.identity: drop each row's columns from the engine digest (sample of an existing guard)

- File: `src/cratekit/intake/native.py`
- Source: `u161.json`, row `S2_columns_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_engine_digest_moves_with_one_row_and_one_playlist_and_not_with_the_path`

Old text:

```
                "content_id": row.content_id,
                "columns": row.columns(),
```

New text:

```
                "content_id": row.content_id,
```

### `u212.N1_second_copy_compare`

naming_cli.second_copy: two different ISRCs read as one recording

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N1_second_copy_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_another_recording_keeps_the_plain_collision`

Old text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) == mine else ""
```

New text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) != "" else ""
```

