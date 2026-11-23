# Mutation table: u325-after-l-28

Measured by `scripts/mutate.py` on 2026-11-23 02:23 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 72.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 46, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 70 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u179.T3_rehearsal_stop_wording` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u46-author.M1_no_items_enqueued` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 17 | killed |
| `u46-round-2.M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 2 | killed |
| `u46-round-2.M7B_engine_refusal_swallowed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 23 | killed |
| `u278.M1_gate_follows_state` | `src/cratekit/core/config.py` | user | 4 file(s) | 478 | 6 | killed |
| `r790-d.R1_grouping_kinds` | `src/cratekit/core/review.py` | user | 2 file(s) | 201 | 1 | killed |
| `r790-d.R2_label_beyond` | `src/cratekit/core/review.py` | user | 2 file(s) | 201 | 7 | killed |
| `r797-b.M4_the_writer_never_files_into_one` | `src/cratekit/adopt/move_cli.py` | user | 3 file(s) | 198 | 1 | killed |
| `r797-b.M5_the_writer_can_leave_one` | `src/cratekit/adopt/move_cli.py` | user | 3 file(s) | 198 | 3 | killed |
| `u90-c.C6_wrapper_reads_nothing` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 198 | 8 | killed |
| `u90-c5.C5_record_threshold_unconverted` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 198 | 1 | killed |
| `r798-c.H6_a_returned_release_passes_at_approval` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 195 | 3 | killed |
| `r798-d.H7_again_an_owned_release_is_not_asked_about` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 195 | 1 | killed |
| `r788-d.A2_vocal_rows_never_written` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 192 | 3 | killed |
| `r788-d.A3_present_rows_handed_over` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 192 | 2 | killed |
| `u132.V5_nothing` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 2 | killed |
| `u132.V6_backup_name` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 1 | killed |
| `u133-a.P12_verb_warning` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 1 | killed |
| `r835-b.M1_only_the_batch_years_marked` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-b.M5_deleted_folder_said` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.M4_recheck_before_rename_again` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u261.W3_compare_by_value_not_bytes` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 187 | 1 | killed |
| `u261.W5_session_fields_guard_sample` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 187 | 1 | killed |
| `r598-a.A6_record_holder_is_a_second_lookup` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 185 | 1 | killed |
| `r598-a.A7_sweep_ignores_the_shown_list` | `src/cratekit/core/session.py` | user | 2 file(s) | 185 | 1 | killed |
| `u181.T5_rescore_never_run` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 4 | killed |
| `u181.T6_plan_warnings_not_lifted` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 1 | killed |
| `u205.S1_account_lookup_ignores_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 177 | 17 | killed |
| `u205.S2_account_rejection_read_as_wait` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 177 | 2 | killed |
| `u278.M3_pointer_reads_state_dir` | `src/cratekit/core/config.py` | user | 3 file(s) | 418 | 3 | killed |
| `r924.C1_set_identify_not_told` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 165 | 4 | killed |
| `r924.C3_recording_drops_progress` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 165 | 2 | killed |
| `u202-composites.R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.R1_recheck_name` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.W1_landed_then_raised` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u277.M11_worker_detail_without_canary` | `src/cratekit/label/cli.py` | user | 3 file(s) | 158 | 3 | killed |
| `u277.M12_worker_message_without_canary` | `src/cratekit/label/cli.py` | user | 3 file(s) | 158 | 2 | killed |
| `u221.R16_release_any_rekordbox_side` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 1 | killed |
| `u221.R17_release_a_pair_that_is_no_twin` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u221.R18_release_writes_nothing` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 6 | killed |
| `u185.G2_unread_refuses` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G3_pending_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 7 | killed |
| `u185.G4_second_reading_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u267.M6_release_keeps_rows` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 154 | 1 | killed |
| `u267.M9_done_reading_closes_shared` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 154 | 64 | killed |
| `r925.S1_no_folder_check` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 1 | killed |
| `r925.S3_no_write` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 154 | 4 | killed |
| `r798-c.H2_only_a_hold_in_force_is_dropped` | `src/cratekit/core/review.py` | user | 4 file(s) | 396 | 1 | killed |
| `u123.T1_adapter_vouching` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 149 | 1 | killed |
| `u123.T2_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 149 | 1 | killed |
| `u27-adopt-apply-author.A3_missing_gate_refuses_under_the_wrong_reason` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 27 | 1 | killed |
| `u27-adopt-apply-author.S1_no_session_at_all` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 27 | 6 | killed |
| `u27-adopt-apply-author.S4_workflow_is_not_the_verb` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 27 | 1 | killed |
| `r647-a.B16_serial_recorded_in_the_clear` | `src/cratekit/core/session.py` | maintainer | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r647-a.B17_macos_probe_reads_nothing` | `src/cratekit/core/session.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u219.C1_rebuild_items_filtered` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u219.C2_rebuild_named_intake` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 5 | killed |
| `u219.K2_accept_actor` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u129-author.A12_archive_backfill_swallows_all` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u129-author.A3_abort_still_writes` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u129-author.A18_frozen_name_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 24 | 2 | killed |
| `u281.C1_refusal_said_as_blocked` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 5 | killed |
| `u281.W7_worker_run_key_without_attempt` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 1 | killed |
| `r815-a.W4_the_next_ordinal_is_past_the_floor` | `src/cratekit/core/review.py` | user | 3 file(s) | 376 | 2 | killed |
| `r840-c.C1_the_function_is_handed_the_payload_as_it_stands` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 34 | killed |
| `r840-c.C2_the_function_is_only_handed_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 4 | killed |
| `r837-a.A17_sweep_hand_off` | `src/cratekit/sync/cli.py` | user | 5 file(s) | 371 | 1 | killed |
| `r1677.R1_raise_after_copy` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 134 | 1 | killed |
| `r1677.R3_copied_never_set` | `src/cratekit/core/rb_writer.py` | user | 4 file(s) | 134 | 1 | killed |
| `r926.G10_no_temporary_allowance` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 134 | 17 | killed |
| `r926.G9_temporary_unresolved` | `src/cratekit/core/config.py` | maintainer | 2 file(s) | 22933 | 0 (promoted) | zero |
| `r1665.W3_no_release_of_the_copy` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `u267.M5_handle_after_close` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `u267.M7_release_any_handle` | `src/cratekit/core/rb_writer.py` | maintainer | 1 file(s) | 15 | 1 | killed |
| `r1032.S1_protocol_default_on` | `src/cratekit/modules/outbound/tidal_account.py` | user | 4 file(s) | 367 | 15 | killed |
| `r1634.M17_check_drops_how` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 131 | 5 | killed |
| `u277.M10_next_says_no_canary` | `src/cratekit/label/sync_cli.py` | user | 2 file(s) | 131 | 12 | killed |
| `u135.A13_live_inbox_ignores_parent` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A2_set_order_falls_to_name_order` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A5_recorded_inbox_skips_job_key` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u194.W24_write_copy_bytes_stale` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 128 | 1 | killed |
| `u194.W25_write_copy_read_back` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 128 | 2 | killed |
| `r924.A5_cadence_halved` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `r924.A6_last_call_unsaid` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 2 | killed |
| `u129-author.A7_with_archive_omits_digest` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r840-c.C4_no_name_is_the_empty_string` | `src/cratekit/label/catalogue.py` | user | 2 file(s) | 354 | 2 | killed |
| `u243.D14_screen_never_says_ignored` | `src/cratekit/deletion/cli.py` | user | 2 file(s) | 349 | 2 | killed |
| `r301.F1_section_not_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 349 | 8 | killed |
| `r924.A3_cached_count_zero` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `r924.A7_kept_chunks_counted` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `u153.P1_into_colour_flag` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 116 | 11 | killed |
| `u153.P6_place_pink_guard` | `src/cratekit/favorites/placement.py` | user | 3 file(s) | 116 | 2 | killed |
| `u267.M10_done_reading_leaks_own` | `src/cratekit/core/rb_writer.py` | user | 2 file(s) | 115 | 3 | killed |

## Zero rows and what they owe

- `r647-a.B16_serial_recorded_in_the_clear` (maintainer facing): maintainer facing, composite not required
- `r647-a.B17_macos_probe_reads_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r926.G9_temporary_unresolved` (maintainer facing): maintainer facing, composite not required
- `u129-author.A7_with_archive_omits_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u179.T3_rehearsal_stop_wording`

attended: word a rehearsal's acknowledgment stop as a landing's, naming no rehearsal

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T3_rehearsal_stop_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`

Old text:

```
            if stop.step == REHEARSE
            else (f"then plan the landing again: crate {command}",)
```

New text:

```
            if False
            else (f"then plan the landing again: crate {command}",)
```

### `u46-author.M1_no_items_enqueued`

Queue the recording with no item, so the driver has nothing to claim

- File: `src/cratekit/master/cli.py`
- Source: `u46-author.json`, row `M1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 17 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_queueing_a_recording_gives_the_driver_one_item_to_claim`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            item_ids=(str(payload[SOURCE]),),
```

New text:

```
(empty)
```

### `u46-round-2.M6_staging_not_cleared`

Leave a previous attempt's partial encode in the staging directory

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M6_staging_not_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `u46-round-2.M7B_engine_refusal_swallowed`

Translate the engine's encoder-failed into a generic internal defect

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M7B_engine_refusal_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 23 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_refuses`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            str(exc.refusal),
            exc.detail,
```

New text:

```
            "internal-error",
            "the mastering engine refused",
```

### `u278.M1_gate_follows_state`

state_path: drop the gate's own resolution, so the gate follows a redirected CRATEKIT_STATE_DIR and a copy gets a fresh hour

- File: `src/cratekit/core/config.py`
- Source: `u278.json`, row `M1_gate_follows_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_config.py`, `tests/test_isrc_cache.py`
- Collected: 478 against a baseline of 478
- Kills: 6 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_redirected_state_directory_still_resolves_the_one_gate`
  - `tests/test_provider_budget.py::test_a_rehearsal_spends_from_the_live_gate[False]`
  - `tests/test_provider_budget.py::test_a_rehearsal_spends_from_the_live_gate[True]`
  - `tests/test_provider_budget.py::test_the_pointer_names_where_the_gate_lives`

Old text:

```
        if key in _PROVIDER_GATE_KEYS:
            return provider_gate_dir() / entry.relative

```

New text:

```
(empty)
```

### `r790-d.R1_grouping_kinds`

grouped: count every kind in the queue, harvested label names included

- File: `src/cratekit/core/review.py`
- Source: `r790-d.json`, row `R1_grouping_kinds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_harvested_label_name_is_not_counted_as_a_label_release`

Old text:

```
    kinds = kinds or GROUPED_KINDS.get(declared)
```

New text:

```
    kinds = kinds
```

### `r790-d.R2_label_beyond`

grouped by label: report no recorded beyond

- File: `src/cratekit/core/review.py`
- Source: `r790-d.json`, row `R2_label_beyond`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 201 against a baseline of 201
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                "beyond": latest[key].beyond if key in latest else None,
```

New text:

```
                "beyond": None,
```

### `r797-b.M4_the_writer_never_files_into_one`

membership_moves: resolve the target the way a place left is resolved, so a frozen row naming a former place as its target is written

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r797-b.json`, row `M4_the_writer_never_files_into_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_move_whose_target_is_a_former_place_is_refused_and_nothing_is_written`

Old text:

```
            target = destination(declared, move.bucket, move.target)
```

New text:

```
            target = placements.named_place(declared, move.bucket, move.target)
```

### `r797-b.M5_the_writer_can_leave_one`

membership_moves: resolve a place left through destination, which knows no former place, so every move out of the old playlist refuses

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r797-b.json`, row `M5_the_writer_can_leave_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 198 against a baseline of 198
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_second_run_after_the_move_plans_nothing_and_writes_nothing`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_none_is_left_in_both`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`

Old text:

```
                placements.named_place(declared, move.bucket, sub) for sub in move.remove
```

New text:

```
                destination(declared, move.bucket, sub) for sub in move.remove
```

### `u90-c.C6_wrapper_reads_nothing`

load_vocal_threshold stops delegating, so every caller sees an uncalibrated library

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c.json`, row `C6_wrapper_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 198 against a baseline of 198
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`
  - `tests/test_metadata_cli.py::test_a_present_vocal_calibration_is_its_own_threshold`

Old text:

```
    return None if record is None else record["threshold"]
```

New text:

```
    return None
```

### `u90-c5.C5_record_threshold_unconverted`

The one reader returns the stored threshold as written rather than the checked float

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c5.json`, row `C5_record_threshold_unconverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    return {**record, "threshold": threshold}
```

New text:

```
    return dict(record)
```

### `r798-c.H6_a_returned_release_passes_at_approval`

label approved: judge a release a person returned, so it is held a second time when it is accepted

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-c.json`, row `H6_a_returned_release_passes_at_approval`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`
- Collected: 195 against a baseline of 195
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_held_at_approval_is_returned_by_name_and_listed_the_next_time`
  - `tests/test_label_genre_gate.py::test_a_returned_mark_on_the_payload_alone_is_believed`
  - `tests/test_label_genre_gate.py::test_a_returned_release_is_listed_at_approval_and_not_judged_again`

Old text:

```
        if release.returned:
            continue
```

New text:

```
        if False:
            continue
```

### `r798-d.H7_again_an_owned_release_is_not_asked_about`

label approved: ask the general catalogue about a release the library holds in full. H7 measured again, against the line as the second review left it, where ownership is read off the one resolution of each release

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-d.json`, row `H7_again_an_owned_release_is_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_the_catalogue_is_not_asked_about_a_release_the_library_already_holds`

Old text:

```
        elif owned(release):
```

New text:

```
        elif False:
```

### `r788-d.A2_vocal_rows_never_written`

planned_memberships: the vocal additions are left out of the write, so the gate lists memberships the apply never performs

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r788-d.json`, row `A2_vocal_rows_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 192 against a baseline of 192
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_one_apply_writes_the_entries_and_the_vocal_subs_in_one_mapping`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`

Old text:

```
    for key, rows in vocal_locations(plan, declared).items():
```

New text:

```
    for key, rows in ():
```

### `r788-d.A3_present_rows_handed_over`

vocal_locations: every planned membership is handed to the writer, the present ones too

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r788-d.json`, row `A3_present_rows_handed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 192 against a baseline of 192
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_only_the_additions_reach_the_writer_under_the_declared_names`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    return _locations(plan.vocal_additions(), declared, lambda entry: entry.vocal_sub)
```

New text:

```
    return _locations(plan.vocal_memberships(), declared, lambda entry: entry.vocal_sub)
```

### `u132.V5_nothing`

A plan that writes nothing still asks the gate

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V5_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_what_is_held_is_said_and_written_around`

Old text:

```
    if not found.writes:

```

New text:

```
    if False:

```

### `u132.V6_backup_name`

A backup takes the name an earlier backup holds

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V6_backup_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_backup_never_takes_an_earlier_backups_name`

Old text:

```
    while candidate.exists():

```

New text:

```
    while False:

```

### `u133-a.P12_verb_warning`

The verb drops the keyword rule warning

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u133-a.json`, row `P12_verb_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
    ] + [{"code": KEYWORD_RULE, "message": sentence} for sentence in found.keywords]

```

New text:

```
    ]

```

### `r835-b.M1_only_the_batch_years_marked`

mark_cli._item: a year the landed batch did not file is marked anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M1_only_the_batch_years_marked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_year_the_batch_did_not_file_is_left_alone`

Old text:

```
    if year.year not in filed:
        return {
```

New text:

```
    if False:
        return {
```

### `r835-b.M5_deleted_folder_said`

mark_cli.label_mark: a label folder deleted on the account is listed as if it were there, and the read fails every run

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M5_deleted_folder_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`

Old text:

```
            if shape.folder_id in remote.folders()
```

New text:

```
            if True
```

### `r835-c.M4_recheck_before_rename_again`

mark_cli.label_mark: a title changed between the plan and the write is renamed anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-c.json`, row `M4_recheck_before_rename_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_title_changed_between_the_plan_and_the_write_is_not_renamed`

Old text:

```
            if now.get(identity) != item["built_as"]:
```

New text:

```
            if False:
```

### `u261.W3_compare_by_value_not_bytes`

write_back: compare the dicts by Python equality rather than the bytes set_json stores, so a value that changed type (an int expiry for a float) is not written

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W3_compare_by_value_not_bytes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        unchanged = _canonical(refreshed)
        if unchanged is not None and unchanged == _canonical(stored):
```

New text:

```
        unchanged = refreshed
        if unchanged == stored:
```

### `u261.W5_session_fields_guard_sample`

write_back (existing guard, sampled): accept a blob carrying no session field, so a file that is not a session replaces the stored one

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W5_session_fields_guard_sample`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_write_back_with_no_session_fields_is_ignored`

Old text:

```
    if not any(field in refreshed for field in SESSION_FIELDS):
        return False
```

New text:

```
    if False:
        return False
```

### `r598-a.A6_record_holder_is_a_second_lookup`

assert_gates: record current_holder() in the record rather than the claimant the lock took, so a supplied holder splits the two copies

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A6_record_holder_is_a_second_lookup`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`

Old text:

```
                holder=claimant,
                intent=intent,
```

New text:

```
                holder=current_holder(),
                intent=intent,
```

### `r598-a.A7_sweep_ignores_the_shown_list`

abandon_orphaned_sessions: end every orphan rather than only those shown, so one answer ends records the question never listed

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A7_sweep_ignores_the_shown_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        if (shown is None or record.session_id in shown) and orphaned(record, here=here)
```

New text:

```
        if orphaned(record, here=here)
```

### `u181.T5_rescore_never_run`

tail.run: the analyze step never rescores

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T5_rescore_never_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`

Old text:

```
        if step == ANALYZE:
            rescore(chain, folder, cfg, unable=unable)
```

New text:

```
        if False:
            rescore(chain, folder, cfg, unable=unable)
```

### `u181.T6_plan_warnings_not_lifted`

tail.land: the landing gate screen's warnings are not lifted onto the chain

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T6_plan_warnings_not_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_warning_the_landing_plan_carries_rides_the_passes_own_warnings`

Old text:

```
        lift_plan_warnings(chain, cause)
```

New text:

```
        pass
```

### `u205.S1_account_lookup_ignores_app`

outbound account: ISRC lookups go to the account session whatever the opener built

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S1_account_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 177 against a baseline of 177
- Kills: 17 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_a_track_read_is_no_track_and_is_asked_once`
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[400]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[500]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[503]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[data-not-a-list]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-an-object]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-json]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_that_was_only_expired_is_answered_on_the_next_rung`
  - `tests/test_catalogue_app.py::test_a_release_whose_artists_did_not_come_back_is_unreadable_and_chooses_nothing`
  - `tests/test_catalogue_app.py::test_a_transport_failure_whose_text_holds_404_is_not_read_as_no_track`
  - `tests/test_catalogue_app.py::test_an_exact_track_reference_is_read_from_the_app`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        self._lookups = catalogue if catalogue is not None else session
```

New text:

```
        self._lookups = session
```

### `u205.S2_account_rejection_read_as_wait`

outbound account: a rejected app credential is translated as the account's failure, a wait, never naming the app

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S2_account_rejection_read_as_wait`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`

Old text:

```
        except catalogue_api.AppCredentialsRejected as exc:
            # THE APP'S CREDENTIAL, NOT THE ACCOUNT'S.
```

New text:

```
        except ZeroDivisionError as exc:
            # THE APP'S CREDENTIAL, NOT THE ACCOUNT'S.
```

### `u278.M3_pointer_reads_state_dir`

provider_gate_dir: fall back to installation_state_dir, which honours CRATEKIT_STATE_DIR

- File: `src/cratekit/core/config.py`
- Source: `u278.json`, row `M3_pointer_reads_state_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_config.py`
- Collected: 418 against a baseline of 418
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_call_made_under_a_redirected_state_directory_is_counted_by_the_live_gate`
  - `tests/test_provider_budget.py::test_a_redirected_state_directory_still_resolves_the_one_gate`
  - `tests/test_provider_budget.py::test_a_rehearsal_spends_from_the_live_gate[False]`

Old text:

```
        return Path(override)
    return Path(platformdirs.user_state_dir(_APP_NAME))


#: The state entries resolved
```

New text:

```
        return Path(override)
    return installation_state_dir()


#: The state entries resolved
```

### `r924.C1_set_identify_not_told`

intake set does not hand its progress to identification

- File: `src/cratekit/intake/cli.py`
- Source: `r924.json`, row `C1_set_identify_not_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 165 against a baseline of 165
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
            result = pipeline.identify_only(
                held.path,
                refresh=bool(ctx.args.refresh),
                recognition=cfg.recognition,
                progress=ctx.progress,
            )
```

New text:

```
            result = pipeline.identify_only(
                held.path,
                refresh=bool(ctx.args.refresh),
                recognition=cfg.recognition,
            )
```

### `r924.C3_recording_drops_progress`

_recording does not pass its progress to the fetch

- File: `src/cratekit/intake/cli.py`
- Source: `r924.json`, row `C3_recording_drops_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 165 against a baseline of 165
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_human_fetch_runs_its_watcher`

Old text:

```
            address, Path(cfg.library.root), found, progress=progress
```

New text:

```
            address, Path(cfg.library.root), found
```

### `u202-composites.R2_confined`

pair_reverse.create: the twins' confinement check is not run before the commit

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202-composites.json`, row `R2_confined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_write_outside_the_playlist_made_is_refused_with_nothing_written`

Old text:

```
                twins.assert_confined(
                    db,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
```

### `u202.R1_recheck_name`

pair_reverse.recheck: a name taken since the plan is made again

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `R1_recheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_the_write_refuses_a_name_taken_since_the_plan`

Old text:

```
    if taken:
        raise _stale(
```

New text:

```
    if False:
        raise _stale(
```

### `u202.W1_landed_then_raised`

pair_reverse.create: a commit that lands and then raises no longer tells the caller, so the playlist made stays unpaired (the second review's BLOCKING finding)

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `W1_landed_then_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_commit_that_lands_and_then_raises_still_pairs_the_playlist`

Old text:

```
                    if on_commit is not None and playlist_id:
                        on_commit(playlist_id)
                raise
```

New text:

```
                raise
```

### `u277.M11_worker_detail_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's detail

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M11_worker_detail_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_offer_window.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
                **({"reverified": canaries[0].to_json()} if canaries else {}),
```

New text:

```
                **({}),
```

### `u277.M12_worker_message_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's message

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M12_worker_message_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_offer_window.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
            f"{asked_again}",
```

New text:

```
            f"",
```

### `u221.R16_release_any_rekordbox_side`

PairStore.release_hold: drop the rekordbox check, so a twin paired again since the plan is released

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R16_release_any_rekordbox_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`

Old text:

```
                    or held.rekordbox_id != str(rekordbox_id)
```

New text:

```
                    or False
```

### `u221.R17_release_a_pair_that_is_no_twin`

PairStore.release_hold: drop the twin check, so a pair that is no twin records a hold

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R17_release_a_pair_that_is_no_twin`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`

Old text:

```
                    or not held.twin
                    or held.rekordbox_id
```

New text:

```
                    or held.rekordbox_id
```

### `u221.R18_release_writes_nothing`

PairStore.release_hold: never write, so an approved release answers released and the next sync still holds

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R18_release_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`

Old text:

```
            if released:
                self._write(pairs)
            return released
```

New text:

```
            return released
```

### `u185.G2_unread_refuses`

assert_foreign_untouched: a handle with no reading at open reads the subtree now and goes on

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G2_unread_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`

Old text:

```
    before = foreign_tree.reading_at_open(db)
    if before is None:
```

New text:

```
    before = foreign_tree.reading_at_open(db) or foreign_tree.read(db.session)
    if before is None:
```

### `u185.G3_pending_leg`

assert_foreign_untouched: drop the pending object leg, keep the second reading

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G3_pending_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 7 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_renaming_the_folder_is_refused_and_rolled_back`

Old text:

```
    violations = foreign_tree.pending_touches(pending_objects(session, db), before)
```

New text:

```
    violations = []
```

### `u185.G4_second_reading_leg`

assert_foreign_untouched: drop the second reading from SQL, keep the pending objects

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G4_second_reading_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
    violations += foreign_tree.differences(before, foreign_tree.read(session))
```

New text:

```
    violations += []
```

### `u267.M6_release_keeps_rows`

SharedRead.release: keep the identity map, so the next reader takes a row an earlier reader loaded as the row the database holds now

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M6_release_keeps_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_release_forgets_every_row_so_the_next_reader_reads_afresh`

Old text:

```
        db.session.expunge_all()
```

New text:

```
        db.session.flush()
```

### `u267.M9_done_reading_closes_shared`

done_reading: close the handle whatever its owner, so the first reader closes the shared handle under the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M9_done_reading_closes_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 154 against a baseline of 154
- Kills: 64 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_playlist_two_folders_down_is_left_where_it_is`
  - `tests/test_organize.py::test_a_prefixed_but_unmarked_playlist_has_its_own_reason`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - ... and 49 more, see the JSON sidecar

Old text:

```
    if shared is None:
        close_db(db)
    else:
        shared.release(db)
```

New text:

```
    close_db(db)
```

### `r925.S1_no_folder_check`

intake set skips the free tracklist folder check, so a folder that is a file is found only after the spend

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S1_no_folder_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/intake/test_set_fetch.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_folder_is_a_file_is_refused_before_any_spend`

Old text:

```
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
```

New text:

```
        out = Path(ctx.args.out or cfg.paths.download_staging / TRACKLISTS_DIR)
```

### `r925.S3_no_write`

intake set writes no tracklist and says it wrote one

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S3_no_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/intake/test_set_fetch.py`
- Collected: 154 against a baseline of 154
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resumed_set_writes_no_tracklist`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_a_set_writes_its_tracklist_where_out_says`
  - `tests/intake/test_workers.py::test_a_set_writes_the_tracklist_identify_writes_for_the_same_rows`

Old text:

```
    try:
        path = _write_tracklist(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
```

New text:

```
    try:
        path = _tracklist_path(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
```

### `r798-c.H2_only_a_hold_in_force_is_dropped`

review.release_hold: drop a hold in any state, so the record that a person returned a release is lost and it can be held again

- File: `src/cratekit/core/review.py`
- Source: `r798-c.json`, row `H2_only_a_hold_in_force_is_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_review_queue.py`, `tests/test_label_offer_window.py`, `tests/test_label_approved.py`
- Collected: 396 against a baseline of 396
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_releasing_drops_a_hold_in_force_and_keeps_a_returned_one`

Old text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ? AND state = ?",
            (_assert_declared_queue(queue), item_id, HOLD_HELD),
```

New text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ?",
            (_assert_declared_queue(queue), item_id),
```

### `u123.T1_adapter_vouching`

Drop the adapter's ledger check before a playlist removal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T1_adapter_vouching`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_outbound_tidal_account.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
            raise refuse(
                "outbound-remove-refused",
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

New text:

```
        if False:
            raise refuse(
                "outbound-remove-refused",
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

### `u123.T2_read_back`

Trust the delete and never read the playlist back

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T2_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_outbound_tidal_account.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`

Old text:

```
        if again is not _ABSENT and again is not None:
```

New text:

```
        if False:
```

### `u27-adopt-apply-author.A3_missing_gate_refuses_under_the_wrong_reason`

Report a verb declaring no approval gate as a configuration problem

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A3_missing_gate_refuses_under_the_wrong_reason`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_verb_declaring_no_plan_digested_gate_refuses_rather_than_applying`

Old text:

```
            reason="internal-error",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
```

New text:

```
            reason="config-unusable",
            message=(
                f"{entry.name} declares no gate digested against the plan, so "
```

### `u27-adopt-apply-author.S1_no_session_at_all`

Run the apply loop with no destructive session around it (the residual's condition, unchanged)

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S1_no_session_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 27 against a baseline of 27
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_a_volume_whose_identity_moved_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_an_unacknowledged_machine_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
    with session.assert_gates(
        cfg,
        workflow=WORKFLOW,
        analysis_roots=watched,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    ):
```

New text:

```
    if True:
```

### `u27-adopt-apply-author.S4_workflow_is_not_the_verb`

Record the session under a name that is not this verb's

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S4_workflow_is_not_the_verb`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_workflow_name_and_the_registry_verb_name_cannot_drift`

Old text:

```
WORKFLOW = "adopt.apply"
```

New text:

```
WORKFLOW = "adoption"
```

### `r647-a.B16_serial_recorded_in_the_clear`

machine_identity: return the raw platform identifier instead of its digest, so a hardware serial is written into every lock and session record

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B16_serial_recorded_in_the_clear`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return hashlib.sha256(f"cratekit-machine:{raw}".encode()).hexdigest()[:32]
```

New text:

```
    return raw
```

### `r647-a.B17_macos_probe_reads_nothing`

_raw_machine_identity: the macOS branch finds nothing, so every holder on a Mac names no machine and a power loss is a dead end there

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B17_macos_probe_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return found.group(1) if found else None
```

New text:

```
        return None
```

### `u219.C1_rebuild_items_filtered`

crate rebuild: queue every native tree again, the intake tree included

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `C1_rebuild_items_filtered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_of_every_tree_leaves_the_intake_tree_alone`

Old text:

```
        items = tuple(t for t in tree_items(entries, tree_id) if engine.derivable(declared, t))
```

New text:

```
        items = tuple(t for t in tree_items(entries, tree_id))
```

### `u219.C2_rebuild_named_intake`

crate rebuild --tree inbox: queue it rather than asking the acceptance gate

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `C2_rebuild_named_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_naming_the_intake_tree_refuses_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`
  - `tests/test_resort_scope.py::test_the_routing_tree_stays_marked_after_inbox_is_accepted`

Old text:

```
        if tree_id is not None and not engine.derivable(declared, tree_id):
```

New text:

```
        if False:
```

### `u219.K2_accept_actor`

rebuild accept: record the command line's actor string rather than who answered the gate (R34)

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `K2_accept_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`

Old text:

```
        cfg, declared, tree_id, actor=ctx.gate.state.decisions[spec.name].actor
    )
```

New text:

```
        cfg, declared, tree_id, actor=ctx.args.actor
    )
```

### `u129-author.A12_archive_backfill_swallows_all`

Catch Exception around plan_archive so a credential refusal becomes a warning

- File: `src/cratekit/export/set_cli.py`
- Source: `u129-author.json`, row `A12_archive_backfill_swallows_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_refuses_a_credential_error`

Old text:

```
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc.cause.message}",
                }
            )
            continue

```

New text:

```
        except Exception as exc:
            warnings.append(
                {
                    "code": "export-archive-backfill-refused",
                    "message": f"{name}: {exc}",
                }
            )
            continue

```

### `u129-author.A3_abort_still_writes`

Apply the account playlist even when the gate said abort

- File: `src/cratekit/intake/cli.py`
- Source: `u129-author.json`, row `A3_abort_still_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_an_abort_on_the_account_gate_queues_the_set_and_writes_no_playlist`

Old text:

```
    if option != "apply" or not built.writes:
        return notes, built.payload

```

New text:

```
    if not built.writes:
        return notes, built.payload

```

### `u129-author.A18_frozen_name_ignored`

Ignore the frozen INSPIRATION name on the job and recompute it

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u129-author.json`, row `A18_frozen_name_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_a_credential_fails`
  - `tests/test_u129_set_account_playlist.py::test_export_set_backfill_names_playlists_already_made_when_one_fails`

Old text:

```
    return str(payload.get(intake_cli.PLAYLIST_NAME) or "").strip()

```

New text:

```
    return ""

```

### `u281.C1_refusal_said_as_blocked`

_unread_phrase: say a refusal as 'blocked on N' again, the wording the card replaces

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C1_refusal_said_as_blocked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
    if word != searchers.Answer.BLOCKED.value:
        return f"{source} {word} on {count}"
```

New text:

```
    if True:
        return f"{source} {word} on {count}"
```

### `u281.W7_worker_run_key_without_attempt`

tagging.cli.handle: name the run by the job alone, so a resumed run inherits the last run's stop

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `W7_worker_run_key_without_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}@{job.attempts}")
```

New text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}")
```

### `r815-a.W4_the_next_ordinal_is_past_the_floor`

_NEXT_ORDINAL: allocate one past the highest item alone, as before

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W4_the_next_ordinal_is_past_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`, `tests/test_review_queue.py`
- Collected: 376 against a baseline of 376
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_ordinal_a_withheld_item_held_is_never_given_to_a_later_one`
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
    "(SELECT MAX(COALESCE((SELECT MAX(ordinal) FROM review_items), 0), "
    "COALESCE((SELECT MAX(ordinal) FROM ordinal_floor), 0)) + 1)"
```

New text:

```
    "(SELECT COALESCE((SELECT MAX(ordinal) FROM review_items), 0) + 1)"
```

### `r840-c.C1_the_function_is_handed_the_payload_as_it_stands`

review.redescribe: hand the function an empty payload and not the stored one, so a caller changing one field writes that field alone

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C1_the_function_is_handed_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_person_reads_each_release_without_asking_for_json`
  - `tests/test_label_artists.py::test_a_rewrite_given_a_function_is_handed_the_payload_and_writes_what_it_returns`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_imported_item_is_read_by_the_identifier_its_payload_carries`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_label_marked_any_has_nothing_held_and_nobody_is_asked`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            wanted = payload(_payload_of(held["payload"]))
```

New text:

```
            wanted = payload({})
```

### `r840-c.C2_the_function_is_only_handed_an_open_item`

review.redescribe: read the payload of any item, so the function is called for one that is decided or carries a verdict this build cannot read

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C2_the_function_is_only_handed_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[accepted]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[rejected]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_an_item_with_an_unreadable_verdict`

Old text:

```
                "SELECT payload FROM review_items WHERE item_id = ? AND verdict IS NULL",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

New text:

```
                "SELECT payload FROM review_items WHERE item_id = ?",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

### `r837-a.A17_sweep_hand_off`

sync.cli: the sweep is handed no set playlist, so the exclusion has nothing to exclude

- File: `src/cratekit/sync/cli.py`
- Source: `r837-a.json`, row `A17_sweep_hand_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
            set_built=set_built,
```

New text:

```
            set_built=frozenset(),
```

### `r1677.R1_raise_after_copy`

integrity_ok: raise the copy failure for any OSError, after the copy too, so an open that fails is told as no room

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1677.json`, row `R1_raise_after_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        if raise_copy_failure and not copied:
```

New text:

```
        if raise_copy_failure:
```

### `r1677.R3_copied_never_set`

integrity_ok: never mark the copy made, so an error after it raises as a copy failure

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1677.json`, row `R3_copied_never_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_check_room_r1677.py`, `tests/test_snapshot_wal_r1665.py`, `tests/test_rb_writer_db.py`, `tests/test_intake_land_rehearse.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_check_room_r1677.py::test_an_open_that_fails_after_the_copy_is_a_failed_check_not_a_copy_failure`

Old text:

```
        with disposable_copy(snapshot_database) as checked:
            copied = True
```

New text:

```
        with disposable_copy(snapshot_database) as checked:
            copied = False
```

### `r926.G10_no_temporary_allowance`

The primitives lose the system temporary allowance, the strict rule the review round measured at 101 refusals

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G10_no_temporary_allowance`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 134 against a baseline of 134
- Kills: 17 (killed)
- Killed:
  - `tests/test_config_test_root.py::test_a_scratch_write_in_the_system_temporary_folder_lands_without_a_root`
  - `tests/test_provider_gate.py::test_a_ceiling_stop_a_verb_swallowed_is_still_said`
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_client_session_as_the_park`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls`
  - `tests/test_provider_gate.py::test_a_verb_at_its_ceiling_is_blocked_and_names_the_exact_command_that_continues`
  - `tests/test_provider_gate.py::test_a_verb_at_the_hours_line_is_blocked_and_keeps_what_it_did`
  - `tests/test_provider_gate.py::test_calls_another_process_made_are_not_reported_as_this_runs`
  - `tests/test_provider_gate.py::test_calls_on_the_command_line_lets_one_run_pass_and_the_next_is_back_at_the_ceiling`
  - `tests/test_provider_gate.py::test_client_session_attaches_the_gate_before_the_login_goes_out`
  - `tests/test_provider_gate.py::test_client_session_with_no_gate_still_paces_at_the_defaults`
  - `tests/test_provider_gate.py::test_rate_limit_answers_are_named_in_the_spend_line`
  - `tests/test_provider_gate.py::test_the_account_opener_paces_with_the_frozen_configuration`
  - `tests/test_provider_gate.py::test_the_catalogue_opener_paces_with_the_frozen_configuration`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_calls_already_given`
  - `tests/test_provider_gate.py::test_the_continue_command_replaces_a_spaced_calls_already_given`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if system_temporary:
        allowed.append(
```

New text:

```
    if False:
        allowed.append(
```

### `r926.G9_temporary_unresolved`

The system temporary directory is compared as spelled, /var against /private/var on macOS, so every scratch write is refused

- File: `src/cratekit/core/config.py`
- Source: `r926.json`, row `G9_temporary_unresolved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_config_test_root.py`, `tests/test_provider_gate.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        allowed.append(Path(tempfile.gettempdir()).resolve())
```

New text:

```
        allowed.append(Path(tempfile.gettempdir()))
```

### `r1665.W3_no_release_of_the_copy`

integrity_ok: release only the session, leaving the pooled connection on the throwaway copy open while it is removed

- File: `src/cratekit/core/rb_writer.py`
- Source: `r1665.json`, row `W3_no_release_of_the_copy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
                # left open would hold its files while it goes.
                close_db(db)
```

New text:

```
                # left open would hold its files while it goes.
                db.close()
```

### `u267.M5_handle_after_close`

SharedRead.handle: drop the refusal after close, so a closed shared read reopens silently

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M5_handle_after_close`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if self._closed:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

New text:

```
        if False:
            raise _defect("a read handle was asked of a shared read that was already closed")
```

### `u267.M7_release_any_handle`

SharedRead.release: drop the refusal of a handle that is not its own

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M7_release_any_handle`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_shared_read_refuses_a_handle_not_its_own_and_a_read_after_close`

Old text:

```
        if db is not self._db:
            raise _defect("a handle that is not the shared read's own was released through it")
```

New text:

```
        if False:
            raise _defect("a handle that is not the shared read's own was released through it")
```

### `r1032.S1_protocol_default_on`

TidalAccount.match_track: default any_agreeing on, so the hearts, the pairs and the exports, which never pass it, break the tie R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `S1_protocol_default_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_set.py`, `tests/test_sync_pair.py`
- Collected: 367 against a baseline of 367
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
        album: str = "",
        any_agreeing: bool = False,
    ) -> str | None:
        """The one provider track this row names exactly, or ``None``.
```

New text:

```
        album: str = "",
        any_agreeing: bool = True,
    ) -> str | None:
        """The one provider track this row names exactly, or ``None``.
```

### `r1634.M17_check_drops_how`

label sync --next: the reverified line no longer says how the release was asked

- File: `src/cratekit/label/sync_cli.py`
- Source: `r1634.json`, row `M17_check_drops_how`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`
- Collected: 131 against a baseline of 131
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`

Old text:

```
                f"{listing.canary.how()}: {listing.canary.said()}",
```

New text:

```
                f": {listing.canary.said()}",
```

### `u277.M10_next_says_no_canary`

_listing_checks: never say the reverified line, so --next is silent about which release it re-verified

- File: `src/cratekit/label/sync_cli.py`
- Source: `u277.json`, row `M10_next_says_no_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_sync.py`
- Collected: 131 against a baseline of 131
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_provider_crediting_another_label_still_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_turns_the_same_shape_into_nothing_new`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_held_releases_whose_lines_name_another_act_still_refuse`
  - `tests/test_label_canary.py::test_the_record_names_the_release_re_verified_and_what_it_answered`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
    if listing.canary is not None:
```

New text:

```
    if False:
```

### `u135.A13_live_inbox_ignores_parent`

live_inbox_named matches the name anywhere, not only under the intake root

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A13_live_inbox_ignores_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True

```

New text:

```
        if True:
            return True

```

### `u135.A2_set_order_falls_to_name_order`

INBOX members follow landing file name order even when a set playlist is planned

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A2_set_order_falls_to_name_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
            if plan.set_playlist is not None:
                ordered = []
                seen: set[str] = set()
                for member in plan.set_playlist.members:
                    target = str(member.target) if member.target else ""
                    if not target or target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
                for row in plan.rows:
                    target = str(row.target)
                    if target not in by_target or target in claimed:
                        continue
                    held = by_target[target]
                    if held in seen:
                        continue
                    ordered.append(held)
                    seen.add(held)
            else:
                ordered = [
                    by_target[str(row.target)]
                    for row in plan.rows
                    if str(row.target) in by_target and str(row.target) not in claimed
                ]

```

New text:

```
            ordered = [
                by_target[str(row.target)]
                for row in plan.rows
                if str(row.target) in by_target and str(row.target) not in claimed
            ]

```

### `u135.A5_recorded_inbox_skips_job_key`

recorded_inbox_playlist ignores the job key so any closed batch playlist is treated as this job's

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A5_recorded_inbox_skips_job_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py`
- Collected: 12 against a baseline of 12
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_dated_batch_from_before_the_unit_is_named_as_a_leftover_and_not_joined`

Old text:

```
        and record.detail[BATCH_PLAYLIST_KEY].get(INBOX_JOB_KEY) == job_id

```

New text:

```
        and True

```

### `u194.W24_write_copy_bytes_stale`

write_copy: drop the byte check after the second plan, so an edit made since is written over

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W24_write_copy_bytes_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`

Old text:

```
    if as_read(raw) != before:
```

New text:

```
    if False:
```

### `u194.W25_write_copy_read_back`

write_copy: drop the read back, so a copy that does not load is left as every verb's declaration

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W25_write_copy_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 128 against a baseline of 128
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`

Old text:

```
    problem = _read_back(cfg, path, written)
    if problem is not None:
```

New text:

```
    problem = _read_back(cfg, path, written)
    if False:
```

### `r924.A5_cadence_halved`

The counter speaks every tenth call rather than every twentieth

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A5_cadence_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    return calls == 1 or calls == owed or calls % PROGRESS_EVERY == 0
```

New text:

```
    return calls == 1 or calls == owed or calls % (PROGRESS_EVERY // 2) == 0
```

### `r924.A6_last_call_unsaid`

The counter does not say the last call

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A6_last_call_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    return calls == 1 or calls == owed or calls % PROGRESS_EVERY == 0
```

New text:

```
    return calls == 1 or calls % PROGRESS_EVERY == 0
```

### `u129-author.A7_with_archive_omits_digest`

Fold archive items into the landing without changing the digest

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A7_with_archive_omits_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    identity = {
        "land": payload["digest"],
        "archive": archived.payload["digest"],
    }

```

New text:

```
    identity = {
        "land": payload["digest"],
    }

```

### `r840-c.C4_no_name_is_the_empty_string`

artist_name: answer with the text of whatever the artist's name attribute holds, so an object with no name reads None

- File: `src/cratekit/label/catalogue.py`
- Source: `r840-c.json`, row `C4_no_name_is_the_empty_string`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`
- Collected: 354 against a baseline of 354
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held2-]`
  - `tests/test_label_tidal_catalogue.py::test_an_artist_that_is_already_text_or_has_no_name_is_read_as_what_it_is[held3-]`

Old text:

```
    return name if isinstance(name, str) else ""
```

New text:

```
    return str(name)
```

### `u243.D14_screen_never_says_ignored`

deletion.cli._shown: the count of rows excused as no local file is never put on the gate screen

- File: `src/cratekit/deletion/cli.py`
- Source: `u243.json`, row `D14_screen_never_says_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion_streaming.py`, `tests/test_deletion.py`
- Collected: 349 against a baseline of 349
- Kills: 2 (killed)
- Killed:
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_deletion_streaming.py::test_delete_review_trashes_a_removed_file_beside_streaming_rows`

Old text:

```
    if ignored:
        shown["ignored, not local files"] = ignored
```

New text:

```
    if False:
        shown["ignored, not local files"] = ignored
```

### `r301.F1_section_not_built`

The recognition section is never read from the file, so every install gets the default

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `F1_section_not_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/intake/test_workers.py`
- Collected: 349 against a baseline of 349
- Kills: 8 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_queued_set_freezes_the_recognition_section_it_was_identified_under`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[set]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[set]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-host-identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_the_fingerprint_changes_when_any_value_changes[recognition-monthly_calls-250]`
  - `tests/test_config.py::test_the_recognition_defaults_bound_the_month_and_name_one_region`

Old text:

```
        recognition=_build(RecognitionConfig, data.get("recognition") or {}),
```

New text:

```
        recognition=RecognitionConfig(),
```

### `r924.A3_cached_count_zero`

The plan line is told nothing was cached

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A3_cached_count_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`

Old text:

```
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
        progress(_plan_line(len(offsets), cached=0, parts=len(parts)))
```

### `r924.A7_kept_chunks_counted`

A chunk the cache answered speaks the counter as if it were paid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A7_kept_chunks_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`

Old text:

```
            if progress is not None and calls > before and _worth_saying(calls, len(owed)):
```

New text:

```
            if progress is not None and _worth_saying(calls, len(owed)):
```

### `u153.P1_into_colour_flag`

plan_placements: never mark a placement for colour, so no heart takes Pink

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P1_into_colour_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 116 against a baseline of 116
- Kills: 11 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_the_author_took_out_of_all_favorites_is_never_put_back`
  - `tests/test_favorites_backfill.py::test_a_member_coloured_by_hand_between_the_two_acts_is_refused_by_the_write`
  - `tests/test_favorites_backfill.py::test_a_second_run_finds_the_same_hearts_and_writes_nothing`
  - `tests/test_favorites_backfill.py::test_an_unreadable_account_refuses_only_when_a_heart_needs_placing`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_backfill.py::test_the_backfill_colours_the_members_placed_before_it_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_a_heart_named_as_a_heart_is_not_listed_again_as_a_recolour`
  - `tests/test_favorites_placement.py::test_a_row_coloured_by_hand_between_two_plans_moves_the_digest`
  - `tests/test_favorites_placement.py::test_the_plan_names_each_uncoloured_heart_for_pink_and_holds_a_coloured_one`
  - `tests/test_favorites_placement.py::test_the_write_colours_the_planned_rows_and_only_those`
  - `tests/test_favorites_placement.py::test_the_write_leaves_a_row_coloured_by_hand_after_the_plan`

Old text:

```
            into_colour=one.content_id in takes,
```

New text:

```
            into_colour=False,
```

### `u153.P6_place_pink_guard`

place: colour even with no Pink id, so write_pink blanks a colour by setting it to the empty id

- File: `src/cratekit/favorites/placement.py`
- Source: `u153.json`, row `P6_place_pink_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 116 against a baseline of 116
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_with_no_pink_row_the_plan_places_and_colours_nothing_and_says_why`
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
    if pink and to_colour:
```

New text:

```
    if to_colour:
```

### `u267.M10_done_reading_leaks_own`

done_reading: never close a reader's own handle, so every reader of the run that answers a gate leaks one

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M10_done_reading_leaks_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_reader_with_no_shared_read_closes_its_own_handle`
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`
  - `tests/test_organize_one_read.py::test_the_report_says_exactly_what_it_said_with_an_open_per_step`

Old text:

```
    if shared is None:
        close_db(db)
```

New text:

```
    if shared is None:
        pass
```

