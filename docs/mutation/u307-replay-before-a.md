# Mutation table: u307-replay-before-a

Measured by `scripts/mutate.py` on 2026-11-22 21:03 UTC, branch `HEAD` at `f6d5cad9`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 338.

Full baseline: measured by this driver (the battery's verdict was not read: it was read against another known failures file).

Subset baselines: 66, each measured by this driver.

Known failures: 252 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/known-u307.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1037.N1_landed_not_recorded` | `src/cratekit/intake/native.py` | user | 3 file(s) | 148 | 32 | killed |
| `r1037.N2_joined_not_made` | `src/cratekit/intake/native.py` | user | 3 file(s) | 148 | 5 | killed |
| `r1037.N3_identity_wrong` | `src/cratekit/intake/native.py` | user | 3 file(s) | 148 | 21 | killed |
| `r1037.N4_size_not_read` | `src/cratekit/intake/native.py` | user | 3 file(s) | 148 | 12 | killed |
| `r1037.N5_count_before_commit` | `src/cratekit/intake/native.py` | user | 3 file(s) | 148 | 1 | killed |
| `r1037.N6_before_empty` | `src/cratekit/intake/native.py` | user | 3 file(s) | 148 | 5 | killed |
| `r1255.N1_landings_of_pass_refuses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 2 | killed |
| `r1255.N2_landed_passes_refuses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 1 | killed |
| `r1844.N13_landing_writes_no_uuid` | `src/cratekit/intake/native.py` | user | 2 file(s) | 101 | 5 | killed |
| `r746-b.N2_base_drive_swap_disabled` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `r746-b.N3_folder_path_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `r746-b.N4_device_not_restamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `r746-b.N5_present_file_planned_as_an_add` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 3 | killed |
| `r746-d.N1_first_device_wins` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 3 | killed |
| `r770-d.C7_unresolved_target_planned_as_an_add` | `src/cratekit/intake/native.py` | user | 2 file(s) | 106 | 1 | killed |
| `r777.N15_any_pass` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 2 | killed |
| `r777.N16_pass_not_recorded` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 1 | killed |
| `r923.N1_landing_sets_nothing` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 1 | killed |
| `u113-c.C1_native_batch_always` | `src/cratekit/intake/native.py` | user | 2 file(s) | 79 | 8 | killed |
| `u113-c.C2_native_batch_keeps_claimed` | `src/cratekit/intake/native.py` | user | 2 file(s) | 79 | 9 | killed |
| `u113-c.C3_native_found_by_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 20 | 1 | killed |
| `u113-c.C4_native_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 20 | 4 | killed |
| `u113-c.C5_removed_node_holds_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 20 | 1 | killed |
| `u115.F1_landing_keeps_random_id` | `src/cratekit/intake/native.py` | user | 6 file(s) | 241 | 38 | killed |
| `u120.N3_identity_without_hearts` | `src/cratekit/intake/native.py` | user | 1 file(s) | 19 | 1 | killed |
| `u120.N4_skipped_is_raised` | `src/cratekit/intake/native.py` | user | 1 file(s) | 19 | 2 | killed |
| `u121.S22_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 73 | 5 | killed |
| `u126.F1_read_always` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u126.F3_counts_undigested` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u126.P1_no_read` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 9 | killed |
| `u126.P2_not_shown` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 4 | killed |
| `u126.R1_binding_value_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 52 | killed |
| `u126.R2_fill_if_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 52 | killed |
| `u126.R3_check_skipped` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 2 | killed |
| `u126.R5_read_back_file_id` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 52 | killed |
| `u126.S1_file_id_kept` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 53 | killed |
| `u126.S2_defaults_left_null` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u127-b.N6b_digest_blind_to_vox` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N10_record_silent` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N11_missing_unreported` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N12_unscored_dropped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N14_read_back_skipped` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 5 | killed |
| `u127.N1_cut_strict` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 2 | killed |
| `u127.N2_every_add_tagged` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 7 | killed |
| `u127.N3_default_cut_when_uncalibrated` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 2 | killed |
| `u127.N4_unreadable_refuses` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N5_no_category_check` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N7_digest_blind_to_cut` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 1 | killed |
| `u127.N8_tag_never_written` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 7 | killed |
| `u127.N9_tag_every_added` | `src/cratekit/intake/native.py` | user | 9 file(s) | 328 | 65 | killed |
| `u128-b.N1_native_owned_unwritten` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 4 | killed |
| `u128-b.N2_native_record_no_pass` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 2 | killed |
| `u128-b.N4_native_dropped_left_lost` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u135.A13_live_inbox_ignores_parent` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A14_set_order_reverses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 85 | 3 | killed |
| `u135.A1_removed_namesake_written_into` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A2_set_order_falls_to_name_order` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A4_live_inbox_named_always_false` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A5_recorded_inbox_skips_job_key` | `src/cratekit/intake/native.py` | user | 1 file(s) | 12 | 1 | killed |
| `u135.A7_leftover_joins_numbered_twin` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u135.A8_job_key_not_stamped` | `src/cratekit/intake/native.py` | user | 1 file(s) | 1 | 1 | killed |
| `u146-c.N1_owned_held_planned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u146-c.N2_owned_not_written` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u146-c.N4_owned_needs_a_heart_file` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-e.N3_owned_out_of_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u150.F2_record_provider` | `src/cratekit/intake/native.py` | user | 2 file(s) | 90 | 1 | killed |
| `u153.N1_restamp_id_text` | `src/cratekit/intake/native.py` | user | 2 file(s) | 37 | 9 | killed |
| `u153.N3_landing_colour_owned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u156.L18_digest_native` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 5 | killed |
| `u156.L19_write_called` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 21 | killed |
| `u156.L20_recorded` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 3 | killed |
| `u157.N1_writable_unasked` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N2_digest_rows` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N3_no_write` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 5 | killed |
| `u157.N4_trust_the_writer` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u157.N5_no_record` | `src/cratekit/intake/native.py` | user | 3 file(s) | 129 | 1 | killed |
| `u161.P1_path_back_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 5 | killed |
| `u161.P2_parent_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 4 | killed |
| `u161.P3_file_name_in_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.P4_device_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.P5_master_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 2 | killed |
| `u161.S1_playlist_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `u161.S2_columns_out` | `src/cratekit/intake/native.py` | user | 1 file(s) | 59 | 1 | killed |
| `u163.W10_search_convention` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W11_search_tie` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W12_readback_active` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W13_identified_words` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W14_album_artist_link` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 2 | killed |
| `u163.W1_words_planned` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 15 | killed |
| `u163.W2_first_value` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W3_year_digits` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 2 | killed |
| `u163.W4_year_written` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W5_album_artist_mint` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W6_album_by_artist` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W7_unmoved` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W8_mint_once` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 1 | killed |
| `u163.W9_creations_named` | `src/cratekit/intake/native.py` | user | 3 file(s) | 294 | 32 | killed |
| `u164.R1_record_filed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 105 | 7 | killed |
| `u165.N1_digest` | `src/cratekit/intake/native.py` | user | 4 file(s) | 152 | 1 | killed |
| `u166.A1_parent_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A2_removed_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 2 | killed |
| `u166.A3_plain_check` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 23 | killed |
| `u166.A5_present_rows_too` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A6_always_create` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 2 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 5 | killed |
| `u166.A8_digest_key` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u166.A9_reserved_batch` | `src/cratekit/intake/native.py` | user | 7 file(s) | 258 | 1 | killed |
| `u173.M24_analyze_name` | `src/cratekit/intake/native.py` | user | 1 file(s) | 33 | 1 | killed |
| `u174.N1_landed_passes_closed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 228 | 1 | killed |
| `u174.N2_landed_passes_committed` | `src/cratekit/intake/native.py` | user | 3 file(s) | 228 | 1 | killed |
| `u174.N3_landed_passes_workflow` | `src/cratekit/intake/native.py` | maintainer | 3 file(s) | 228 | 1 | killed |
| `u174.N4_landed_passes_pass_key` | `src/cratekit/intake/native.py` | maintainer | 3 file(s) | 228 | 1 | killed |
| `r301.B1_shipped_month_unbounded` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 5 | killed |
| `r301.B2_bound_host_ignored` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 3 | killed |
| `r301.B3_refusal_detail_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 5 | killed |
| `r301.B4_refusal_message_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 3 | killed |
| `r301.S1_month_ignores_ledger` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 6 | killed |
| `r706-a.A1_ceiling_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 6 | killed |
| `r706-a.A2_ceiling_one_part_wider` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 4 | killed |
| `r706-a.A3_max_parts_four` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 5 | killed |
| `r706-a.A4_month_asked_of_one_run` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 1 | killed |
| `r706-a.A5_run_guard_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 2 | killed |
| `r706-a.A6_run_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 312 | 2 | killed |
| `r706-a.A7_ceiling_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 312 | 1 | killed |
| `r706-b.B1_partition_front_loads_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 1 | killed |
| `r706-b.B2_parts_needed_floors` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 8 | killed |
| `r706-b.B3_partition_drops_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 5 | killed |
| `r706-b.B4_parts_reported_as_one` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 7 | killed |
| `r706-b.B5_chunks_count_the_first_part` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 6 | killed |
| `r706-b.B6_grid_not_partitioned` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 312 | 7 | killed |
| `r924.A1_no_plan_line` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 255 | 4 | killed |
| `r924.A2_plan_before_the_bounds` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 255 | 1 | killed |
| `r924.A3_cached_count_zero` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `r924.A4_split_on_one_part` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `r924.A5_cadence_halved` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `r924.A6_last_call_unsaid` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 2 | killed |
| `r924.A7_kept_chunks_counted` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 119 | 1 | killed |
| `u103-a.A10_write_is_a_merge` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A1_read_serves_only_answers` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A2_write_keeps_only_answers` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A3_document_must_carry_its_plan` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A5_offset_must_be_planned` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A6_digest_in_the_key` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 5 | killed |
| `u103-a.A7_offsets_in_the_key` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 2 | killed |
| `u103-a.A9_refresh_reads_nothing_kept` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 2 | killed |
| `u57-recognition-and-items.M11_unreached_stop_tenfold` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M12_quota_reads_as_failure` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 4 | killed |
| `u57-recognition-and-items.M16_grid_off_by_one` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 69 | killed |
| `u57-recognition-and-items.M18_missing_credential_is_unready` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u57-recognition-and-items.M1_miss_family_loses_1001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 48 | killed |
| `u57-recognition-and-items.M2_quota_family_empty` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 6 | killed |
| `u57-recognition-and-items.M3_auth_family_loses_3001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M4_transient_range_dropped` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 4 | killed |
| `u57-recognition-and-items.M5_empty_music_not_none` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `u57-recognition-and-items.M6_score_constant` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 2 | killed |
| `u57-recognition-and-items.M7_fold_never_takes_best_score` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 244 | 1 | killed |
| `r1056.F1_no_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F2_empty_year_counts` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F3_any_label_counts` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 4 | killed |
| `r1056.F4_non_list_read_as_empty` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F5_non_dict_entry_skipped` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F6_text_year_accepted` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 2 | killed |
| `r1056.F7_bool_tracks_accepted` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `r1056.F8_no_zero_pad` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 33 | 1 | killed |
| `u150.F1_blank_ref_claims` | `src/cratekit/intake/label_filing.py` | user | 2 file(s) | 90 | 2 | killed |
| `u156.L10_staging_dropped` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L11_unlanded_named` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L12_empty_year` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L13_tree_reused` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 4 | killed |
| `u156.L14_folder_reused` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 6 | killed |
| `u156.L15_year_reused` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 5 | killed |
| `u156.L16_live_at_write` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L17_digest_years` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L1_year_bound` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 3 | killed |
| `u156.L21_read_back` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L2_bridge_guard` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L3_wrong_kind` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 2 | killed |
| `u156.L4_two_of_a_name` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L5_nfc_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 3 | killed |
| `u156.L6_removed_nodes` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L7_year_boundary` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u156.L8_year_anchor` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 2 | killed |
| `u156.L9_no_year_named` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 4 | killed |
| `u177.C1_label_fold` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `u177.C2_no_label_filed` | `src/cratekit/intake/label_filing.py` | user | 1 file(s) | 58 | 1 | killed |
| `r1255.R1_rotation_unlisted_from_scan` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 89 | 2 | killed |
| `r1255.R2_plan_carries_unlisted` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 89 | 1 | killed |
| `u111-c.C3_inboxed_suffix` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 3 | killed |
| `u111-c.C4_removal_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 2 | killed |
| `u111-c.C5_move_threshold` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 3 | killed |
| `u111-c.C6_plan_taken_again` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 1 | killed |
| `u111-c.C7_old_creation_planned` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 2 | killed |
| `u111-d.C10_two_olds_refused` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 1 | killed |
| `u111-d.C9_committed_records_only` | `src/cratekit/intake/rotate.py` | user | 1 file(s) | 41 | 1 | killed |
| `u113-c.C7_unproven_import_names` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 46 | 1 | killed |
| `u113-c.C9_earliest_name_wins` | `src/cratekit/intake/rotate.py` | user | 2 file(s) | 46 | 1 | killed |
| `u166.R2_rotate_reserved` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 74 | 1 | killed |
| `u175.R1_account_ids_unrecorded` | `src/cratekit/intake/rotate.py` | user | 4 file(s) | 98 | 3 | killed |
| `u214.M15_unread_is_not_none` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 2 | killed |
| `u214.M16_old_only_under_inbox` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M18_folder_unknown` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M19_folder_unread_reason` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M1_old_named_as_old` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 5 | killed |
| `u214.M20_unread_unlisted` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M2_left_row_count` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 4 | killed |
| `u214.M3_live_left_collected` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 8 | killed |
| `u214.M4_digest_without_count` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 1 | killed |
| `u214.M5_rotation_old_display` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 3 | killed |
| `u214.M6_live_old_display` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 3 | killed |
| `u214.M7_label_rows` | `src/cratekit/intake/rotate.py` | user | 6 file(s) | 201 | 2 | killed |
| `r1255.B1_batch_name_clause` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 105 | 2 | killed |
| `u110-a.A2_favorites_word` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 132 | 2 | killed |
| `u110-a.A5_several_labels` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 132 | 1 | killed |
| `u110-a.A6_folder_safe` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 132 | 1 | killed |
| `u110-a.A7_join_order` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 132 | 2 | killed |
| `u110-a.A8_labels_first` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 132 | 1 | killed |
| `u113-a.A4_batch_name_not_taken` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 32 | 2 | killed |
| `u113-a.A5_landing_names_its_own` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 32 | 1 | killed |
| `u154.R5_unreadable_record_fails_open` | `src/cratekit/intake/batch_name.py` | user | 1 file(s) | 43 | 1 | killed |
| `u164.B1_taken_recorded` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 137 | 4 | killed |
| `u164.B2_native_names` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 112 | 2 | killed |
| `u175.N1_date_first` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 102 | 54 | killed |
| `u175.N2_no_date` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 102 | 54 | killed |
| `u175.N3_date_form` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 102 | 54 | killed |
| `u175.N4_clock_not_seam` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 102 | 54 | killed |
| `u175.N7_held_not_held` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 102 | 8 | killed |
| `u175.N8_counter_before_date` | `src/cratekit/intake/batch_name.py` | user | 4 file(s) | 102 | 9 | killed |
| `u175.N9_landing_not_held` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 80 | 1 | killed |
| `u179.N1_one_label_only_when_all_named` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 59 | 3 | killed |
| `u179.N2_label_case_folded` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 59 | 1 | killed |
| `u179.N3_name_made_free` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 59 | 1 | killed |
| `u113-a.A2_queue_order` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 22933 | 0 (promoted) | zero |
| `u113-a.A3_no_pass_splits_nothing` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u113-a.A8_pending_any_state` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 32 | 1 | killed |
| `u120.B2_first_mention_wins` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 50 | 2 | killed |
| `u128-b.A6b_abandoned_counts` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128-b.A8b_ambiguous_is_an_answer` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128-b.A9b_emptied_left_lost` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128.A10_no_warning` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 5 | killed |
| `u128.A1_owned_not_mirrored` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 13 | killed |
| `u128.A2_rerun_unseen` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 2 | killed |
| `u128.A3_rerun_keeps_owned` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 1 | killed |
| `u128.A4_untied_carried_silent` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 2 | killed |
| `u128.A7_any_pass_counts` | `src/cratekit/intake/account_playlists.py` | user | 3 file(s) | 71 | 2 | killed |
| `u145.M3_landing_heart_undated` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 19 | 11 | killed |
| `u145.M4_states_carried_only` | `src/cratekit/intake/account_playlists.py` | user | 2 file(s) | 64 | 8 | killed |
| `u146-b.A1_superseded_ignored` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.A2_owned_reads_carried` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 12 | killed |
| `u146-b.A3_report_paths_dropped` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 11 | killed |
| `u165.F1_reset_cache` | `src/cratekit/intake/filing.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.F2_compare` | `src/cratekit/intake/filing.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.F3_differing_files` | `src/cratekit/intake/filing.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.F4_vox_predicted` | `src/cratekit/intake/filing.py` | user | 4 file(s) | 152 | 1 | killed |
| `u165.F5_report_failed` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u165.F6_unplaced` | `src/cratekit/intake/filing.py` | user | 4 file(s) | 152 | 1 | killed |
| `r740-b.E2_average_bpm_nonzero` | `src/cratekit/intake/collection_xml.py` | user | 5 file(s) | 108 | 8 | killed |
| `r770-d.S1_composite_the_splice_takes_a_stub` | `src/cratekit/intake/collection_xml.py` | user | 4 file(s) | 108 | 2 | killed |
| `u37-author-light.G1_stub_listing` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 17 | 1 | killed |
| `u37-author-light.G3_gridless_bpm` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 42 | 1 | killed |
| `u166.C12_ack_first` | `src/cratekit/intake/analyzed_cli.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u166.C13_read_back_call` | `src/cratekit/intake/analyzed_cli.py` | user | 3 file(s) | 1066 | 1 | killed |
| `u173.M21_gate_name` | `src/cratekit/intake/analyzed_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.D1_keep_is_not_accept` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 35 | 1 | killed |
| `u102-a.D2_open_is_not_accepted` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 35 | 1 | killed |
| `u37-author-light.G5_path_repair_queue` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 164 | 3 | killed |

## Zero rows and what they owe

- `u146-e.N3_owned_out_of_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u113-a.A2_queue_order` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u113-a.A3_no_pass_splits_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u165.F5_report_failed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1037.N1_landed_not_recorded`

_record_landing_commit: never write collection_landed, so no landed row is ever offered

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N1_landed_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 148 against a baseline of 148
- Kills: 32 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landing_of_another_database_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_one_of_whose_playlists_is_gone_offers_nothing`
  - `tests/test_delete_landed_removed.py::test_a_landing_record_with_no_update_count_offers_nothing[12]`
  - `tests/test_delete_landed_removed.py::test_a_landing_record_with_no_update_count_offers_nothing[None]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    if landed is not None:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
```

New text:

```
    if False:
        record.detail[LANDED_ROWS_KEY] = dict(landed)
```

### `r1037.N2_joined_not_made`

_landed_rows: record every playlist the rows joined, made or already there

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N2_joined_not_made`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 148 against a baseline of 148
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`

Old text:

```
    playlists = sorted({str(one) for one in joined if one and str(one) not in before})
```

New text:

```
    playlists = sorted({str(one) for one in joined if one})
```

### `r1037.N3_identity_wrong`

_landed_rows: record no database identity

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N3_identity_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 148 against a baseline of 148
- Kills: 21 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_first_run_takes_absent_landed_rows_as_history_and_offers_the_next_removal`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_file_a_new_row_now_references_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_sync_removed_recorded_is_one_candidate_at_its_recorded_number`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_record_written_before_rows_named_their_uuid_keeps_the_playlist_proof_alone`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_a_restore_to_before_the_landing_offers_nothing_and_the_screen_counts_it`
  - `tests/test_delete_landed_removed.py::test_a_row_held_under_the_landed_id_but_another_uuid_proves_nothing`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        "database_identity": plan.master_db_id,
```

New text:

```
        "database_identity": "",
```

### `r1037.N4_size_not_read`

_landed_rows: record no file size, so no landed file can be proved by its size

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N4_size_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 148 against a baseline of 148
- Kills: 12 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_declined_landed_removal_is_not_offered_again_and_a_trashed_one_is_retired`
  - `tests/test_delete_landed_removed.py::test_a_handled_landing_whose_playlist_went_later_is_not_counted`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_outright_is_offered_trashed_and_tombstoned_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_playlist_the_rotation_soft_deleted_still_proves_a_landing_of_one_row`
  - `tests/test_delete_landed_removed.py::test_a_removal_seen_once_keeps_its_number_across_runs_and_is_not_hidden`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_only_the_unreferenced_file_is_trashed_and_only_it_is_tombstoned`
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_every_row_it_made_as_the_database_holds_it`

Old text:

```
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS},
```

New text:

```
                    "columns": {name: _plain(getattr(content, name, None)) for name in LANDED_COLUMNS if name != "FileSize"},
```

### `r1037.N5_count_before_commit`

_landed_rows: record a count short of the one the commit left

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N5_count_before_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_every_row_it_made_as_the_database_holds_it`

Old text:

```
        sequence = int(db.get_local_usn())
```

New text:

```
        sequence = int(db.get_local_usn()) - 1
```

### `r1037.N6_before_empty`

apply_rows: read no playlist before the landing, so a playlist already there is recorded as made

- File: `src/cratekit/intake/native.py`
- Source: `r1037.json`, row `N6_before_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`
- Collected: 148 against a baseline of 148
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landing_after_a_restore_is_still_offered_when_removed`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_names_none_and_its_removal_is_kept`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_put_back_by_hand_is_never_offered`
  - `tests/test_delete_landed_removed.py::test_a_restored_landing_into_a_playlist_already_there_is_never_offered`

Old text:

```
        playlists_before = frozenset(str(row.ID) for row in db.get_playlist())
```

New text:

```
        playlists_before = frozenset()
```

### `r1255.N1_landings_of_pass_refuses`

native.landings_of_pass: drop the unread half again, so sync mark says a recorded landing never committed

- File: `src/cratekit/intake/native.py`
- Source: `r1255.json`, row `N1_landings_of_pass_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 90 against a baseline of 90
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_sync_mark.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_landing`

Old text:

```
    land the pass again.
    """
    records = session.records(cfg)
```

New text:

```
    land the pass again.
    """
    records = session.scan_log(cfg)[0]
```

### `r1255.N2_landed_passes_refuses`

native.landed_passes: drop the unread half again, so organize plans no native pass over a log it could not list

- File: `src/cratekit/intake/native.py`
- Source: `r1255.json`, row `N2_landed_passes_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`

Old text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.records(cfg)
```

New text:

```
    cannot list refuses rather than reading as no landing (R-1255).
    """
    records = session.scan_log(cfg)[0]
```

### `r1844.N13_landing_writes_no_uuid`

native landing: the record names each row with an empty UUID

- File: `src/cratekit/intake/native.py`
- Source: `r1844.json`, row `N13_landing_writes_no_uuid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_delete_landed_removed.py`, `tests/test_intake_land_native.py`
- Collected: 101 against a baseline of 101
- Kills: 5 (killed)
- Killed:
  - `tests/test_delete_landed_removed.py::test_a_landed_row_marked_soft_deleted_still_proves_its_landing`
  - `tests/test_delete_landed_removed.py::test_a_landed_row_removed_after_its_playlist_was_deleted_by_hand_is_offered_once`
  - `tests/test_delete_landed_removed.py::test_a_landing_into_a_playlist_already_there_is_offered_while_another_row_remains`
  - `tests/test_delete_landed_removed.py::test_an_offer_withdrawn_when_the_landings_last_rows_go_is_counted`
  - `tests/test_delete_landed_removed.py::test_the_landing_record_names_each_row_by_the_uuid_the_database_holds`

Old text:

```
                    LANDED_UUID_KEY: str(getattr(content, "UUID", None) or ""),
```

New text:

```
                    LANDED_UUID_KEY: "",
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

### `r770-d.C7_unresolved_target_planned_as_an_add`

native.plan_rows: read a target the matcher could not resolve as a file the collection does not hold

- File: `src/cratekit/intake/native.py`
- Source: `r770-d.json`, row `C7_unresolved_target_planned_as_an_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land_native.py`
- Collected: 106 against a baseline of 106
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_the_engine_refuses_a_target_it_cannot_resolve_instead_of_planning_an_add`

Old text:

```
        if match.outcome is trees.MatchOutcome.UNRESOLVED:
```

New text:

```
        if False:
```

### `r777.N15_any_pass`

landings_of_pass counts a landing of another pass

- File: `src/cratekit/intake/native.py`
- Source: `r777.json`, row `N15_any_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`

Old text:

```
            and record.detail.get(PASS_KEY) == name

```

New text:

```
(empty)
```

### `r777.N16_pass_not_recorded`

The native landing's commit no longer records the pass

- File: `src/cratekit/intake/native.py`
- Source: `r777.json`, row `N16_pass_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`

Old text:

```
    if plan.pass_name:
        record.detail[PASS_KEY] = plan.pass_name
```

New text:

```
    if False:
        record.detail[PASS_KEY] = plan.pass_name
```

### `r923.N1_landing_sets_nothing`

The native landing no longer sets rekordbox's defaults on a row it creates

- File: `src/cratekit/intake/native.py`
- Source: `r923.json`, row `N1_landing_sets_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes`

Old text:

```
        if getattr(content, column, None) is None:
```

New text:

```
        if False:
```

### `u113-c.C1_native_batch_always`

The native write always makes the batch playlist, empty when every row was claimed

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C1_native_batch_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 79 against a baseline of 79
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
            if ordered or not accounts:
```

New text:

```
            if True:
```

### `u113-c.C2_native_batch_keeps_claimed`

The native batch playlist holds the claimed rows too

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C2_native_batch_keeps_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`
- Collected: 79 against a baseline of 79
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_intake_land_account_playlists_native.py::test_two_swept_playlists_land_as_two_playlist_rows_under_their_exact_names`

Old text:

```
                if str(row.target) in by_target and str(row.target) not in claimed
```

New text:

```
                if str(row.target) in by_target
```

### `u113-c.C3_native_found_by_name`

An account playlist is found by its name under INBOX and added to, rather than created

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C3_native_found_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
                created = db.create_playlist(one.name, parent=anchor)
```

New text:

```
                created = rb_writer.ensure_playlist(db, one.name, anchor)
```

### `u113-c.C4_native_record_unnamed`

The native landing record does not list the account playlists by identifier

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C4_native_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`

Old text:

```
        record.detail[INBOX_PLAYLISTS_KEY] = [
```

New text:

```
        record.detail["inbox_playlists_unread"] = [
```

### `u113-c.C5_removed_node_holds_name`

A removed node under INBOX still holds its name, so a free exact name takes a count

- File: `src/cratekit/intake/native.py`
- Source: `u113-c.json`, row `C5_removed_node_holds_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`

Old text:

```
        if not rb_writer.node_removed(row):
```

New text:

```
        if True:
```

### `u115.F1_landing_keeps_random_id`

The native landing keeps the random rb_file_id the binding minted instead of the landed file's inode

- File: `src/cratekit/intake/native.py`
- Source: `u115.json`, row `F1_landing_keeps_random_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 241 against a baseline of 241
- Kills: 38 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))

```

New text:

```
(empty)
```

### `u120.N3_identity_without_hearts`

identity: the digest leaves the hearts out

- File: `src/cratekit/intake/native.py`
- Source: `u120.json`, row `N3_identity_without_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`

Old text:

```
    favorites = {"favorites": plan.favorites.identity()} if plan.favorites is not None else {}
```

New text:

```
    favorites = {}
```

### `u120.N4_skipped_is_raised`

_favorites_plan: a home that cannot be resolved raises through the landing

- File: `src/cratekit/intake/native.py`
- Source: `u120.json`, row `N4_skipped_is_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_two_source_playlists_skip_the_placement_too`
  - `tests/test_intake_land_hearts_native.py::test_with_no_source_playlist_the_batch_lands_and_the_placement_is_skipped_and_said`

Old text:

```
    try:
        home = placement.resolve_home(db, source)
    except CratekitError as exc:
```

New text:

```
    try:
        home = placement.resolve_home(db, source)
    except ValueError as exc:
```

### `u121.S22_record_unnamed`

_record_landing_commit: the set playlist is not named on the record

- File: `src/cratekit/intake/native.py`
- Source: `u121.json`, row `S22_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    if set_written is not None and plan.set_playlist is not None:
```

New text:

```
    if False:
```

### `u126.F1_read_always`

Read the library's link whatever the plan adds, so a landing of held files refuses on a split library

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `F1_read_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.library_link(db)
```

### `u126.F3_counts_undigested`

Digest the value alone, so the counts the screen shows can change under an approval

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `F3_counts_undigested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_content_link_counts_move_the_digest`

Old text:

```
            {"value": plan.link.value, "carriers": plan.link.carriers, "rows": plan.link.rows}
```

New text:

```
            {"value": plan.link.value}
```

### `u126.P1_no_read`

Skip the library read and plan a fixed value, the binding's shape of a guess

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `P1_no_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_library_with_no_majority_content_link_refuses_before_the_gate`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_an_approval_taken_at_one_content_link_is_not_applied_at_another`
  - `tests/test_intake_land_native.py::test_the_content_link_counts_move_the_digest`
  - `tests/test_intake_land_native.py::test_the_content_link_moves_the_digest`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_native.py::test_the_rows_carry_the_librarys_content_link_and_not_the_bindings`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
        row_link.library_link(db) if any(row.action == ADD for row in rows) else None
```

New text:

```
        row_link.LibraryLink(value=7, carriers=0, rows=0)
        if any(row.action == ADD for row in rows)
        else None
```

### `u126.P2_not_shown`

Drop ContentLink from a row's columns, so the screen and the row's part of the digest omit it

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `P2_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_the_content_link_moves_the_digest`
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
            **(
                {rb_writer.CONTENT_LINK_COLUMN: self.content_link}
                if self.content_link is not None
                else {}
            ),
```

New text:

```
(empty)
```

### `u126.R1_binding_value_kept`

Drop the restamp of ContentLink, so the row keeps the binding's value

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R1_binding_value_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 52 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    pass
```

### `u126.R2_fill_if_null`

Set ContentLink only when the binding left it NULL, which it never does

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R2_fill_if_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 52 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

New text:

```
    if getattr(content, rb_writer.CONTENT_LINK_COLUMN, None) is None:
        setattr(content, rb_writer.CONTENT_LINK_COLUMN, row.content_link)
```

### `u126.R3_check_skipped`

Skip the read back's ContentLink check

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R3_check_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_assert_rows_identified_holds_the_link_to_the_one_planned`

Old text:

```
        if landed.content_link is None or row.content_link != landed.content_link
```

New text:

```
        if False
```

### `u126.R5_read_back_file_id`

Read back the file id column where the link should be

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `R5_read_back_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 52 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 37 more, see the JSON sidecar

Old text:

```
        None if row[3] is None else int(row[3]),
```

New text:

```
        None if row[2] is None else int(row[2]),
```

### `u126.S1_file_id_kept`

Sample, U115: drop the file id restamp, so the row keeps the binding's random id

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S1_file_id_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 53 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 38 more, see the JSON sidecar

Old text:

```
    setattr(content, rb_writer.FILE_ID_COLUMN, file_id_of(row.target))
```

New text:

```
    pass
```

### `u126.S2_defaults_left_null`

Sample, R-923: drop the defaults fill, so the binding's NULLs stay

- File: `src/cratekit/intake/native.py`
- Source: `u126.json`, row `S2_defaults_left_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes`

Old text:

```
        if getattr(content, column, None) is None:
            setattr(content, column, value)
```

New text:

```
        pass
```

### `u127-b.N6b_digest_blind_to_vox`

Drop each added row's score and answer from the digest, after the engine test

- File: `src/cratekit/intake/native.py`
- Source: `u127-b.json`, row `N6b_digest_blind_to_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_engine_digest_covers_each_rows_score_and_answer`

Old text:

```
                "rows": [[str(row.target), row.voxlevel, row.vox] for row in plan.to_add()],
```

New text:

```
                "rows": [[str(row.target)] for row in plan.to_add()],
```

### `u127.N10_record_silent`

Record no commit under the vocals key, so a restore cannot count the tags

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N10_record_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`

Old text:

```
    if vox_written > 0:
```

New text:

```
    if vox_written > 10**6:
```

### `u127.N11_missing_unreported`

Never report a planned tag that adoption does not read back

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N11_missing_unreported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`

Old text:

```
            row.target for row, content_id in added_ids if row.vox and content_id not in voxed
```

New text:

```
            row.target for row, content_id in added_ids if False
```

### `u127.N12_unscored_dropped`

Name no unscored file on the landed record

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N12_unscored_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`

Old text:

```
    unscored = {row.target for row in plan.vox_unscored()}
```

New text:

```
    unscored = set()
```

### `u127.N14_read_back_skipped`

Never read the tag back, so every landed row reports untagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N14_read_back_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            _vox_read_back(db) if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

New text:

```
            (frozenset(), "") if any(row.vox for row, _ in added_ids) else (frozenset(), "")
```

### `u127.N1_cut_strict`

Compare the score strictly above the cut, so a file exactly at the cut is not tagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N1_cut_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        values = metadata_cli.vocal_tag_values(level, None, cut + 0.5)
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

### `u127.N2_every_add_tagged`

Tag every added row whatever its score, the guess the brief forbids

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N2_every_add_tagged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[below]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[zero]`
  - `tests/test_intake_land_vox_native.py::test_the_digest_moves_when_a_tag_is_planned`
  - `tests/test_intake_land_vox_native.py::test_the_screen_counts_the_tagged_rows_against_the_cut`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`

Old text:

```
        scored.append(replace(row, voxlevel=level, vox=metadata_cli.VALUE_VOX in values))
```

New text:

```
        scored.append(replace(row, voxlevel=level, vox=True))
```

### `u127.N3_default_cut_when_uncalibrated`

Tag from the vocals verb's default cut on a library with no calibration instead of blocking

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N3_default_cut_when_uncalibrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_calibration_tags_nothing_and_says_why`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`

Old text:

```
    if cut is None:
        return rows, None, VOX_UNCALIBRATED
```

New text:

```
    if cut is None:
        cut = metadata_cli.DEFAULT_VOCAL_THRESHOLD
```

### `u127.N4_unreadable_refuses`

Let an unreadable calibration refuse the landing rather than block the tag

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N4_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_an_unreadable_calibration_tags_nothing_and_lands_the_batch`

Old text:

```
    except CratekitError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
```

New text:

```
    except ValueError as exc:
        # AN UNREADABLE CALIBRATION BLOCKS THE TAG, NOT THE LANDING. The
```

### `u127.N5_no_category_check`

Skip the writer's question at plan time, so a library with no category fails after the moves

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N5_no_category_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_library_with_no_category_to_copy_tags_nothing_and_lands_the_batch`

Old text:

```
    if not rb_writer.my_tag_writable(db):
        return rows, cut, VOX_NO_CATEGORY
```

New text:

```
    if False:
        return rows, cut, VOX_NO_CATEGORY
```

### `u127.N7_digest_blind_to_cut`

Drop the cut from the digest

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N7_digest_blind_to_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_the_digest_moves_with_the_cut`

Old text:

```
                "cut": plan.vox_cut,
```

New text:

```
                "cut": None,
```

### `u127.N8_tag_never_written`

Write no tag at the apply, the defect R-841 measured

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N8_tag_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_vox_native.py::test_a_file_with_no_score_gets_no_tag_and_is_named`
  - `tests/test_intake_land_vox_native.py::test_a_hand_placed_tag_on_a_row_already_present_survives`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[above]`
  - `tests/test_intake_land_vox_native.py::test_a_landed_row_is_tagged_vox_exactly_when_its_score_clears_the_cut[exactly-at-the-cut]`
  - `tests/test_intake_land_vox_native.py::test_a_library_with_another_category_only_gains_the_vocals_category`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_the_vocals_verb_uses`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`

Old text:

```
            vox_written = _tag_vox(db, added_ids)
```

New text:

```
            vox_written = 0
```

### `u127.N9_tag_every_added`

Write the tag on every added row, not only those the plan tagged

- File: `src/cratekit/intake/native.py`
- Source: `u127.json`, row `N9_tag_every_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 328 against a baseline of 328
- Kills: 65 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_account_playlists_native.py::test_a_job_queued_with_no_name_lands_in_the_batch_playlist_as_before`
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_the_rotation_removed_never_takes_a_new_landings_tracks`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_a_second_landing_of_one_playlist_the_next_week_takes_its_own_date`
  - `tests/test_intake_land_account_playlists_native.py::test_a_track_both_playlists_brought_in_is_a_member_of_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_an_undated_playlist_from_before_u175_is_left_as_it_is`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - ... and 50 more, see the JSON sidecar

Old text:

```
    content_ids = [content_id for row, content_id in added if row.vox]
```

New text:

```
    content_ids = [content_id for row, content_id in added]
```

### `u128-b.N1_native_owned_unwritten`

The native commit joins no owned row to its playlist, the new rows alone

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N1_native_owned_unwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`

Old text:

```
                        member.content_id
                        if member.target is None
```

New text:

```
                        ""
                        if member.target is None
```

### `u128-b.N2_native_record_no_pass`

The native landing's record names no pass, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N2_native_record_no_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
```

New text:

```
                ingest.INBOX_PASS_KEY: "",
```

### `u128-b.N4_native_dropped_left_lost`

A native playlist holding nothing writable drops its left rows

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N4_native_dropped_left_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_whose_only_file_is_unsupported_still_names_it_as_left`

Old text:

```
            dropped.extend((one.name, row) for row in left)
```

New text:

```
            pass
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

### `u135.A14_set_order_reverses`

INBOX set-order walk appends members in reverse position order

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A14_set_order_reverses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`
- Collected: 85 against a baseline of 85
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
                for member in plan.set_playlist.members:

```

New text:

```
                for member in reversed(plan.set_playlist.members):

```

### `u135.A1_removed_namesake_written_into`

Drop the node_removed skip so a soft-deleted set-named INBOX playlist is written into

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A1_removed_namesake_written_into`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_removed_set_named_inbox_playlist_is_not_written_into`

Old text:

```
    for row in list(db.get_playlist(Name=plan.playlist)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
            return row
    return db.create_playlist(plan.playlist, parent=anchor)

```

New text:

```
    return rb_writer.ensure_playlist(db, plan.playlist, anchor)

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

### `u135.A4_live_inbox_named_always_false`

Never detect a live set-named INBOX playlist, so a hand-made one reads as made

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A4_live_inbox_named_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`

Old text:

```
    for row in list(db.get_playlist(Name=name)):
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == str(root_id):
            return True
    return False

```

New text:

```
    return False

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

### `u135.A7_leftover_joins_numbered_twin`

A numbered twin of the set name under INBOX is no longer named as a leftover

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A7_leftover_joins_numbered_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_numbered_leftover_inbox_playlist_is_named_on_the_screen_and_not_joined`

Old text:

```
        if held.startswith(prefix) and held[len(prefix) :].isdigit():
            named.append(held)

```

New text:

```
        if False:
            named.append(held)

```

### `u135.A8_job_key_not_stamped`

A set landing's batch playlist record carries no job key

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A8_job_key_not_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`

Old text:

```
        if plan.set_job_id:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

New text:

```
        if False:
            kept[INBOX_JOB_KEY] = plan.set_job_id

```

### `u146-c.N1_owned_held_planned`

_favorites_plan: an owned heart All Favorites holds is planned again beside a landing, and its month made

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N1_owned_held_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_is_no_write_beside_a_landing`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`

Old text:

```
        if one.content_id in in_source or one.content_id in seen:
```

New text:

```
        if one.content_id in seen:
```

### `u146-c.N2_owned_not_written`

apply_rows: the owned hearts are planned and shown and never written

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N2_owned_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
```

New text:

```
(empty)
```

### `u146-c.N4_owned_needs_a_heart_file`

_favorites_plan: owned hearts are placed only when a landed file is a heart too

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N4_owned_needs_a_heart_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`

Old text:

```
    if not (kept or owned) or not source:
```

New text:

```
    if not kept or not source:
```

### `u146-e.N3_owned_out_of_digest`

FavoritesPlan.identity: the owned hearts are not digested, so an answer given for one set of them stands for another

- File: `src/cratekit/intake/native.py`
- Source: `u146-e.json`, row `N3_owned_out_of_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.owned:
            identity["owned"] = [
```

New text:

```
        if self.owned and False:
            identity["owned"] = [
```

### `u150.F2_record_provider`

native._record_commit: write no provider tracks on the landing's record

- File: `src/cratekit/intake/native.py`
- Source: `u150.json`, row `F2_record_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_landed_rows_provider_track_for_the_account_mirror`

Old text:

```
        record.detail[label_filing.PROVIDER_KEY] = dict(labels_written.provider)
```

New text:

```
        pass
```

### `u153.N1_restamp_id_text`

native _restamp: do not coerce the minted ID to text, so a colour on an existing row cannot flush beside a new one

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N1_restamp_id_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 37 against a baseline of 37
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_an_undated_heart_lands_in_the_undated_playlist`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
    content.ID = str(content.ID)
```

New text:

```
    content.ID = content.ID
```

### `u153.N3_landing_colour_owned`

native apply: drop the owned hearts from the colour set, so an owned heart is placed but not coloured

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N3_landing_colour_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`

Old text:

```
                to_colour.extend(plan.favorites.colour)
```

New text:

```
                to_colour.extend([])
```

### `u156.L18_digest_native`

native.identity: leave the label plan out of the landing's digest

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L18_digest_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`
  - `tests/test_intake_land_labels_native.py::test_an_answer_given_for_one_label_is_stale_for_another`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_between_one_label_and_each_files_own`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_label`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_manifests_bytes`

Old text:

```
    filed = {"labels": label_filing.identity(plan.labels)} if plan.labels is not None else {}
```

New text:

```
    filed = {}
```

### `u156.L19_write_called`

apply_rows: plan the labels and never write them

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L19_write_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 21 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`
  - `tests/test_intake_land_labels_native.py::test_a_file_two_rows_file_in_two_years_names_both_on_its_item`
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_label_tag_spelled_decomposed_files_under_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_with_its_label_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_landing_with_label_records_no_provider_track`
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_left_in_staging_is_not_said_to_be_in_the_intake_playlist`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
```

New text:

```
                labels_written = None
```

### `u156.L20_recorded`

_record_landing_commit: write the labels and record nothing of them on the session

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L20_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_landing_with_label_records_no_provider_track`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_year_filed_and_counts_it_under_the_catalogue_tree`

Old text:

```
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
```

New text:

```
    if False:
        label_filing.record_commit(record, labels_written, cfg)
```

### `u157.N1_writable_unasked`

_dyn_plan: skip the writer's own question, so a library with no category to copy plans a tag the commit refuses

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N1_writable_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_library_with_no_category_to_copy_lands_and_names_the_variable_rows`

Old text:

```
    if not rb_writer.my_tag_writable(db):
        return read, cut, DYN_NO_CATEGORY

```

New text:

```
(empty)
```

### `u157.N2_digest_rows`

identity: the dyn block names each row's answer only, not its drift or verdict

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N2_digest_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_engine_digest_covers_each_rows_drift_verdict_and_answer`

Old text:

```
[str(row.target), row.drift, row.drift_verdict, row.dyn]
```

New text:

```
[str(row.target), row.dyn]
```

### `u157.N3_no_write`

apply: the dyn tag is never written

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N3_no_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[exactly-at-the-cut]`
  - `tests/test_intake_land_dyn_native.py::test_a_landed_row_is_tagged_dyn_exactly_when_its_drift_reads_variable[moving]`
  - `tests/test_intake_land_dyn_native.py::test_a_removed_membership_is_no_mark_to_the_shared_reader`
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_counted_on_the_session`
  - `tests/test_intake_land_dyn_native.py::test_the_warning_names_both_selections_and_counts_each`

Old text:

```
            dyn_written = _tag_dyn(db, added_ids)
```

New text:

```
            dyn_written = 0
```

### `u157.N4_trust_the_writer`

apply: report each row's dyn from the plan, not the read back

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N4_trust_the_writer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_a_tag_written_under_a_removed_value_is_said_and_never_counted`

Old text:

```
                    dyn=content_id in dyned,
```

New text:

```
                    dyn=row.dyn,
```

### `u157.N5_no_record`

_record_landing_commit: record no dyn tags on the session

- File: `src/cratekit/intake/native.py`
- Source: `u157.json`, row `N5_no_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_dyn_native.py`, `tests/test_drift.py`, `tests/test_analyze_check.py`
- Collected: 129 against a baseline of 129
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_dyn_native.py::test_the_tag_is_written_under_one_value_and_counted_on_the_session`

Old text:

```
    if dyn_written > 0:
        session.record_commit(
```

New text:

```
    if False:
        session.record_commit(
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

### `u163.W10_search_convention`

_Resolver._shaped: store NULL in SearchStr whatever the library's convention

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W10_search_convention`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_mint_follows_the_librarys_searchstr_convention`

Old text:

```
        return replace(word, search=word.name if convention == SEARCH_NAME else convention)
```

New text:

```
        return replace(word, search=None)
```

### `u163.W11_search_tie`

search_convention: answer the first ranked convention on a tie

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W11_search_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_tied_searchstr_convention_mints_null`

Old text:

```
    if not ranked or (len(ranked) > 1 and ranked[0][1] == ranked[1][1]):
```

New text:

```
    if not ranked:
```

### `u163.W12_readback_active`

_words_back: read the artist through any row, tombstones included

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W12_readback_active`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`

Old text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} AND a.{active} "
```

New text:

```
            f"LEFT JOIN {rb_writer.ARTIST_TABLE} a ON a.ID = c.{ARTIST_COLUMN} "
```

### `u163.W13_identified_words`

assert_rows_identified: never compare the words read back

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W13_identified_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_landed_row_whose_word_reads_back_wrong_is_refused`

Old text:

```
        if row.words.get(column) != want
```

New text:

```
        if False
```

### `u163.W14_album_artist_link`

_Mints._mint: mint an album with no album artist

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W14_album_artist_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none`

Old text:

```
        if word.table == rb_writer.ALBUM_TABLE:
            columns[ALBUM_ARTIST]
```

New text:

```
        if False:
            columns[ALBUM_ARTIST]
```

### `u163.W1_words_planned`

plan_rows: never plan the words, so no row carries artist, album, genre or year

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W1_words_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 15 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_the_gate_screen_names_every_row_its_columns_the_playlist_and_the_database`
  - `tests/test_intake_land_words.py::test_a_file_with_no_artist_leaves_the_column_empty`
  - `tests/test_intake_land_words.py::test_a_mint_follows_the_librarys_searchstr_convention`
  - `tests/test_intake_land_words.py::test_a_multi_value_id3_frame_lands_its_first_value_as_the_word`
  - `tests/test_intake_land_words.py::test_a_tied_searchstr_convention_mints_null`
  - `tests/test_intake_land_words.py::test_a_tombstoned_namesake_is_skipped_for_the_active_row_after_it`
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`
  - `tests/test_intake_land_words.py::test_a_word_the_library_holds_links_its_active_row_and_mints_nothing`
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`
  - `tests/test_intake_land_words.py::test_a_word_whose_only_namesake_is_a_tombstone_is_minted`
  - `tests/test_intake_land_words.py::test_adoption_reads_the_landed_rows_genre_with_rekordbox_closed`
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`
  - `tests/test_intake_land_words.py::test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none`
  - `tests/test_intake_land_words.py::test_the_read_back_takes_no_word_through_a_tombstoned_lookup_row`
  - `tests/test_intake_land_words.py::test_two_files_with_one_new_artist_mint_it_once`

Old text:

```
    rows = _words_plan(db, rows)

```

New text:

```
    rows = rows

```

### `u163.W2_first_value`

_word: keep the NUL joined ID3 value whole (round one's fix)

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W2_first_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_multi_value_id3_frame_lands_its_first_value_as_the_word`

Old text:

```
    first = (value or "").split("\x00")[0]
```

New text:

```
    first = value or ""
```

### `u163.W3_year_digits`

year_of: accept any four characters as a year

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W3_year_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_the_year_is_the_four_digits_the_date_tag_opens_with[0000-None]`
  - `tests/test_intake_land_words.py::test_the_year_is_the_four_digits_the_date_tag_opens_with[circa 2021-None]`

Old text:

```
    if len(head) != 4 or not head.isdigit() or int(head) == 0:
```

New text:

```
    if len(head) != 4:
```

### `u163.W4_year_written`

_Mints.link: drop the ReleaseYear write

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W4_year_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_the_library_lacks_is_minted_and_linked_in_the_one_commit`

Old text:

```
        if row.year is not None:
            setattr(content, YEAR_COLUMN, row.year)
```

New text:

```
        if False:
            setattr(content, YEAR_COLUMN, row.year)
```

### `u163.W5_album_artist_mint`

_active_album_id: look up an album whose album artist is minted, instead of minting it

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W5_album_artist_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_an_album_whose_album_artist_is_minted_is_minted_beside_a_namesake_with_none`

Old text:

```
    if album_artist is not None and not album_artist.row_id:
        return ""
```

New text:

```
    if False:
        return ""
```

### `u163.W6_album_by_artist`

_active_album_id: find the album by name alone, ignoring its album artist

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W6_album_by_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_an_album_links_the_one_its_album_artist_holds`

Old text:

```
        if str(getattr(row, ALBUM_ARTIST, None) or "") == want
```

New text:

```
        if True
```

### `u163.W7_unmoved`

_assert_words_unmoved: never refuse a word that moved since the plan

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W7_unmoved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_a_word_minted_by_another_hand_since_the_plan_refuses_and_writes_nothing`

Old text:

```
            if _rows_of(now) != _rows_of(word):
```

New text:

```
            if False:
```

### `u163.W8_mint_once`

_Mints.id_of: mint a new word again for every row

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W8_mint_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_words.py::test_two_files_with_one_new_artist_mint_it_once`

Old text:

```
        if key not in self._made:
            self._made[key] = self._mint(word)
```

New text:

```
        if True:
            self._made[key] = self._mint(word)
```

### `u163.W9_creations_named`

apply_rows: name only the content table in creations, so a mint is refused

- File: `src/cratekit/intake/native.py`
- Source: `u163.json`, row `W9_creations_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_words.py`, `tests/test_intake_land_native.py`, `tests/test_rb_writer_guard.py`
- Collected: 294 against a baseline of 294
- Kills: 32 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - `tests/test_intake_land_native.py::test_a_landing_given_a_pass_names_it_on_the_record_sync_mark_reads`
  - `tests/test_intake_land_native.py::test_a_landing_given_no_pass_names_none`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_a_row_whose_content_link_did_not_take_is_refused_after_the_commit`
  - `tests/test_intake_land_native.py::test_a_row_whose_file_id_did_not_take_is_refused_after_the_commit_naming_the_session`
  - `tests/test_intake_land_native.py::test_a_second_approved_run_over_the_landed_files_adds_nothing`
  - `tests/test_intake_land_native.py::test_a_suffix_the_database_has_no_type_for_is_left_in_staging_and_the_batch_lands`
  - `tests/test_intake_land_native.py::test_after_the_write_no_analysis_value_exists_on_the_new_rows_column_by_column`
  - `tests/test_intake_land_native.py::test_an_analysis_product_row_for_the_new_row_is_refused_from_sql_before_the_commit`
  - `tests/test_intake_land_native.py::test_an_answer_continued_over_the_file_it_was_given_over_lands`
  - `tests/test_intake_land_native.py::test_folder_path_is_stored_under_the_base_drive_rekordbox_records`
  - `tests/test_intake_land_native.py::test_the_rows_carry_every_default_rekordbox_writes_on_a_row_it_makes`
  - `tests/test_intake_land_native.py::test_the_rows_carry_the_landed_files_inode_as_their_file_id`
  - ... and 17 more, see the JSON sidecar

Old text:

```
                db, creations=(rb_writer.CONTENT_TABLE, *mints.tables())
```

New text:

```
                db, creations=(rb_writer.CONTENT_TABLE,)
```

### `u164.R1_record_filed`

_record_landing_commit: never record the filed batch and its folder

- File: `src/cratekit/intake/native.py`
- Source: `u164.json`, row `R1_record_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_rehearse.py`
- Collected: 105 against a baseline of 105
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_name_landed_into_again_goes_back_to_its_folder_unless_the_folder_is_gone`
  - `tests/test_intake_land_filed.py::test_shelve_over_a_batch_landed_filed_reports_nothing_to_do`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_landing_that_adds_no_row_needs_no_majority`
  - `tests/test_intake_land_native.py::test_the_same_files_staged_again_are_refused_at_the_move_and_the_collection_is_unchanged`
  - `tests/test_intake_land_rehearse.py::test_a_name_the_live_batch_folder_holds_is_refused_at_the_area_as_it_will_be_live`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_a_batch_filed_in_another_year_is_refused`

Old text:

```
    if plan.folder is not None and plan.batch:
        record.detail[FILED_BATCH_KEY]
```

New text:

```
    if False:
        record.detail[FILED_BATCH_KEY]
```

### `u165.N1_digest`

identity: leave the predictions out of the digest

- File: `src/cratekit/intake/native.py`
- Source: `u165.json`, row `N1_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_land_only_files_nothing_and_digests_apart_from_a_landing_that_files`

Old text:

```
        {"filing": [one.identity() for one in plan.filing]} if plan.filing is not None else {}
```

New text:

```
        {}
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

### `u173.M24_analyze_name`

native: the queue playlist renamed, so the skill sends a session to a playlist no landing fills

- File: `src/cratekit/intake/native.py`
- Source: `u173.json`, row `M24_analyze_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_it_selects_the_playlist_every_landing_fills`

Old text:

```
ANALYZE = "Analyze"
```

New text:

```
ANALYZE = "Analysis"
```

### `u174.N1_landed_passes_closed`

landed_passes: drop the closed state check, so an open landing's pass is planned

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N1_landed_passes_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N2_landed_passes_committed`

landed_passes: drop the committed source check, so a refused landing's pass is planned

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N2_landed_passes_committed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and record.state is session.SessionState.CLOSED
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N3_landed_passes_workflow`

landed_passes: drop the workflow check, so any closed session naming a pass is read as a landing

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N3_landed_passes_workflow`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                if record.workflow == WORKFLOW
                and record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                if record.state is session.SessionState.CLOSED
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

### `u174.N4_landed_passes_pass_key`

landed_passes: drop the pass key check, so a landing of no pass is listed as a pass named None

- File: `src/cratekit/intake/native.py`
- Source: `u174.json`, row `N4_landed_passes_pass_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_intake_land_native.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_landed_passes_reads_only_closed_committed_landings`

Old text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
                and record.detail.get(PASS_KEY)
            }
```

New text:

```
                and str(session.SourceState.COMMITTED) in record.sources.values()
            }
```

### `r301.B1_shipped_month_unbounded`

The shipped budget carries no monthly bound, which is the tree before this unit

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B1_shipped_month_unbounded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_shipped_budget_bounds_the_month_the_section_names`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_monthly_bound_is_the_one_the_verb_meets[set]`

Old text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=recognition.monthly_calls)
```

New text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=None)
```

### `r301.B2_bound_host_ignored`

The bound identifier asks the default region whatever the section names

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B2_bound_host_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_is_the_one_every_paid_call_is_sent_to[set]`

Old text:

```
            host=recognition.host,
```

New text:

```
            host=config.DEFAULT_RECOGNITION_HOST,
```

### `r301.B3_refusal_detail_no_key`

The monthly refusal's detail no longer names the key that raises the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B3_refusal_detail_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
                "key": MONTHLY_KEY,

```

New text:

```
(empty)
```

### `r301.B4_refusal_message_no_key`

The monthly refusal's message is reworded so it no longer names the key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B4_refusal_message_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
            f"or raise {MONTHLY_KEY} in the configuration if the plan allows more",
```

New text:

```
            f"or adjust the configured bound if the plan allows more",
```

### `r301.S1_month_ignores_ledger`

Sample of an existing guard: the monthly check ignores what the month already spent

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `S1_month_ignores_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_monthly_refusal_names_the_key_that_raises_the_bound`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`

Old text:

```
    if budget.monthly is not None and used_this_month + planned > budget.monthly:
```

New text:

```
    if budget.monthly is not None and planned > budget.monthly:
```

### `r706-a.A1_ceiling_dropped`

Drop the parts ceiling, so a file of any length is cut into as many parts as it takes

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A1_ceiling_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_nonsense_duration_is_refused_by_the_bound_before_any_grid_exists`
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_per_run_bound_refuses_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    assert_one_set(spend, planned=planned)
    offsets = sample_offsets(duration_s)
```

New text:

```
    offsets = sample_offsets(duration_s)
```

### `r706-a.A2_ceiling_one_part_wider`

The ceiling admits one part more than MAX_PARTS, a coefficient row on the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A2_ceiling_one_part_wider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    ceiling = budget.per_run * MAX_PARTS
```

New text:

```
    ceiling = budget.per_run * (MAX_PARTS + 1)
```

### `r706-a.A3_max_parts_four`

MAX_PARTS moves from three to four, the decision's Part A, B and C plus one

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A3_max_parts_four`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
MAX_PARTS = 3
```

New text:

```
MAX_PARTS = 4
```

### `r706-a.A4_month_asked_of_one_run`

The month is asked about one run's worth rather than the whole set, so a set the month cannot afford spends its first part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A4_month_asked_of_one_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`

Old text:

```
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
```

New text:

```
        assert_month_within(
            spend, planned=min(len(owed), spend.per_run), used_this_month=counter.used(month)
        )
```

### `r706-a.A5_run_guard_dropped`

Drop the per part run guard, so an oversize part is paid for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A5_run_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[one-oversize-part]`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`

Old text:

```
    for part in parts:
        assert_run_within(spend, planned=sum(1 for offset in part if offset in still_owed))
    keys = ("", "")
```

New text:

```
    keys = ("", "")
```

### `r706-a.A6_run_message_reworded`

Reword the per part run refusal, do not append to it

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A6_run_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[one-oversize-part]`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`

Old text:

```
            f"this run would take {planned} recognition calls and the per run "
```

New text:

```
            f"this part needs {planned} recognition calls and the per run "
```

### `r706-a.A7_ceiling_message_reworded`

Reword the ceiling refusal so it no longer says the file is not one set

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A7_ceiling_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`

Old text:

```
            f"nothing was sent. A file this long is not one set, so split it "
```

New text:

```
            f"nothing was sent. A file this long is too long, so split it "
```

### `r706-b.B1_partition_front_loads_the_remainder`

The remainder goes to the first part whole instead of one chunk to each of the first parts, so a cut is uneven and can exceed the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B1_partition_front_loads_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`

Old text:

```
        size = base + (1 if index < extra else 0)
```

New text:

```
        size = base + (extra if index == 0 else 0)
```

### `r706-b.B2_parts_needed_floors`

parts_needed floors instead of ceiling, so 732 chunks is one part of 732

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B2_parts_needed_floors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 8 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[732-400-sizes4]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    return -(-planned // per_run)
```

New text:

```
    return max(1, planned // per_run)
```

### `r706-b.B3_partition_drops_the_remainder`

Every part is cut to the base size, so the remainder chunks fall out of the grid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B3_partition_drops_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
        parts.append(tuple(offsets[start : start + size]))
```

New text:

```
        parts.append(tuple(offsets[start : start + base]))
```

### `r706-b.B4_parts_reported_as_one`

The result says one part whatever the cut

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B4_parts_reported_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
        parts=len(parts),
```

New text:

```
        parts=1,
```

### `r706-b.B5_chunks_count_the_first_part`

The walked grid is rebuilt from the first part only, so chunks and cached count one part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B5_chunks_count_the_first_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    offsets = tuple(offset for part in parts for offset in part)
```

New text:

```
    offsets = tuple(parts[0]) if parts else ()
```

### `r706-b.B6_grid_not_partitioned`

identify hands the whole grid over as one part, so the run guard meets a 5 hour mix

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B6_grid_not_partitioned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 312 against a baseline of 312
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_served_from_the_cache_as_one_plan`
  - `tests/intake/test_recognition.py::test_a_split_set_that_owes_only_a_gap_meets_the_run_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    parts = partition(offsets, per_run=spend.per_run)
```

New text:

```
    parts = (offsets,)
```

### `r924.A1_no_plan_line`

Identification never states its plan before the first call

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A1_no_plan_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
    if False:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

### `r924.A2_plan_before_the_bounds`

The plan line is said before the month bound and the credential read, so a refused run is told it will pay

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A2_plan_before_the_bounds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_run_the_month_refuses_is_not_told_it_will_pay`

Old text:

```
    keys = ("", "")
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
    # AFTER EVERY REFUSAL THAT SPENDS NOTHING, so a run told it is about to pay
    # is a run that will, and one refused by a bound or a missing key is told
    # only the refusal.
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
    keys = ("", "")
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
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

### `r924.A4_split_on_one_part`

A set identified in one part is said to be in parts

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A4_split_on_one_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`

Old text:

```
    split = f" in {parts} parts" if parts > 1 else ""
```

New text:

```
    split = f" in {parts} parts" if parts >= 1 else ""
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

### `u103-a.A10_write_is_a_merge`

Replace the cache document with this pass's answers instead of laying them over what is kept

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A10_write_is_a_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_write_is_a_merge_so_an_overlapping_pass_does_not_drop_what_another_paid_for`

Old text:

```
            merged = {**self.read(plan), **answers}
```

New text:

```
            merged = dict(answers)
```

### `u103-a.A1_read_serves_only_answers`

Drop the reader's rule that only a match or a miss is served from a cache document

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A1_read_serves_only_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_only_an_answer_is_kept_or_served_in_either_direction`

Old text:

```
            if classify(payload)[0] not in _KEPT_OUTCOMES:
                continue
            answers[offset] = payload
```

New text:

```
            answers[offset] = payload
```

### `u103-a.A2_write_keeps_only_answers`

Drop the writer's rule that only a match or a miss is kept, removed alone so the reader's copy of the rule is not what is measured

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A2_write_keeps_only_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_only_an_answer_is_kept_or_served_in_either_direction`

Old text:

```
                    for offset in sorted(merged)
                    if classify(merged[offset])[0] in _KEPT_OUTCOMES
```

New text:

```
                    for offset in sorted(merged)
```

### `u103-a.A3_document_must_carry_its_plan`

Stop checking that a cache document carries the plan it was asked for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A3_document_must_carry_its_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`

Old text:

```
        if document.get("version") != CACHE_VERSION or document.get("plan") != plan.material():
```

New text:

```
        if document.get("version") != CACHE_VERSION:
```

### `u103-a.A5_offset_must_be_planned`

Serve a kept answer at an offset the plan never asked for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A5_offset_must_be_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_only_an_answer_is_kept_or_served_in_either_direction`

Old text:

```
            if offset not in planned or not isinstance(payload, dict):
```

New text:

```
            if not isinstance(payload, dict):
```

### `u103-a.A6_digest_in_the_key`

Take the recording's content digest out of the key material, so a changed file keeps its old key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A6_digest_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_every_field_of_the_plan_moves_the_key[digest]`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_changed_recording_misses_the_cache_and_is_paid_for`
  - `tests/intake/test_workers.py::test_two_recordings_sharing_a_stem_keep_a_tracklist_each`

Old text:

```
            "digest": self.digest,
            "offsets": list(self.offsets),
```

New text:

```
            "digest": "",
            "offsets": list(self.offsets),
```

### `u103-a.A7_offsets_in_the_key`

Take the offsets out of the key material, so a changed chunk plan keeps its old key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A7_offsets_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_every_field_of_the_plan_moves_the_key[offsets]`

Old text:

```
            "offsets": list(self.offsets),
            "chunk_s": self.chunk_s,
```

New text:

```
            "offsets": [],
            "chunk_s": self.chunk_s,
```

### `u103-a.A9_refresh_reads_nothing_kept`

Let a refreshing pass read the kept answers anyway

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A9_refresh_reads_nothing_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_refresh_reads_nothing_kept_and_lays_the_new_answers_over_the_document`
  - `tests/intake/test_workers.py::test_refresh_pays_for_every_chunk_again_and_the_new_answers_replace_the_kept_ones`

Old text:

```
    kept = kept_in.read(plan) if plan is not None and not refresh else {}
```

New text:

```
    kept = kept_in.read(plan) if plan is not None else {}
```

### `u57-recognition-and-items.M11_unreached_stop_tenfold`

Fifty unanswered calls in a row before the run stops, not five

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M11_unreached_stop_tenfold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_rejecting_host_stops_the_run_the_same_way`
  - `tests/intake/test_recognition.py::test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent`

Old text:

```
UNREACHED_STOP = 5
```

New text:

```
UNREACHED_STOP = 50
```

### `u57-recognition-and-items.M12_quota_reads_as_failure`

The provider's quota answer is raised under the failure slug, not the spend slug

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M12_quota_reads_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_cache_that_cannot_be_written_does_not_replace_the_refusal_on_its_way_out`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
    return refuse(
        "intake-recognition-spend-bound",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
```

New text:

```
    return refuse(
        "intake-recognition-failed",
        f"the recognition service refused to spend: code {code} ({message or 'no message'}) "
```

### `u57-recognition-and-items.M16_grid_off_by_one`

The planned count loses its last chunk

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M16_grid_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 69 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_ledger_that_cannot_record_stops_the_run_before_the_call`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_run_where_no_call_got_an_answer_is_a_failure_and_not_an_empty_set`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - ... and 54 more, see the JSON sidecar

Old text:

```
    return (whole - chunk_s) // interval_s + 1
```

New text:

```
    return (whole - chunk_s) // interval_s
```

### `u57-recognition-and-items.M18_missing_credential_is_unready`

A credential missing after the gate is reported as the gate class, not as credential-missing

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M18_missing_credential_is_unready`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_missing_after_the_gate_is_credential_missing_with_its_own_remedy`

Old text:

```
            "credential-missing" if missing else "intake-recognition-unready",
```

New text:

```
            "intake-recognition-unready",
```

### `u57-recognition-and-items.M1_miss_family_loses_1001`

1001, the service's own no result code, falls out of the miss family

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M1_miss_family_loses_1001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 48 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_from_another_cache_version_is_a_miss`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_pass_that_paid_for_nothing_writes_nothing_and_reports_nothing_unwritten`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_with_the_misses_counted_not_a_refusal`
  - `tests/intake/test_recognition.py::test_a_set_that_fits_one_run_is_one_part`
  - ... and 33 more, see the JSON sidecar

Old text:

```
_MISS_CODES = frozenset({1001, 2004, 3015})
```

New text:

```
_MISS_CODES = frozenset({2004, 3015})
```

### `u57-recognition-and-items.M2_quota_family_empty`

3003 stops being a quota answer, so a spent account reads as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M2_quota_family_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_cache_that_cannot_be_written_does_not_replace_the_refusal_on_its_way_out`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload4-quota]`
  - `tests/intake/test_recognition.py::test_the_two_spend_refusals_and_a_miss_are_three_different_things`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
_QUOTA_CODES = frozenset({3003})
```

New text:

```
_QUOTA_CODES = frozenset()
```

### `u57-recognition-and-items.M3_auth_family_loses_3001`

3001, a missing or invalid access key, stops being a credential answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M3_auth_family_loses_3001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_credential_answer_ends_the_run_as_auth_failed`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload5-auth]`

Old text:

```
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
```

New text:

```
_AUTH_CODES = frozenset({3002, 3006, 3014})
```

### `u57-recognition-and-items.M4_transient_range_dropped`

The 2000s stop being transient, so a recording error ends the run as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M4_transient_range_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_transient_answer_or_a_transport_that_raised_skips_the_chunk_and_is_counted`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload10-transient]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload11-transient]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload9-transient]`

Old text:

```
    if 2000 <= code < 3000 or code in _TRANSIENT_CODES:
```

New text:

```
    if code in _TRANSIENT_CODES:
```

### `u57-recognition-and-items.M5_empty_music_not_none`

A match answer carrying no music entry is indexed rather than read as none

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M5_empty_music_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_with_no_music_and_a_malformed_score_are_handled`

Old text:

```
    if not isinstance(music, list) or not music:
        return None
```

New text:

```
    if not isinstance(music, list):
        return None
```

### `u57-recognition-and-items.M6_score_constant`

Every hit scores zero, so the fold can never prefer a better answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M6_score_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_becomes_a_wanted_row_with_the_version_split_and_the_isrc_kept`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score`

Old text:

```
    try:
        score = int(top.get("score", 0))
    except (TypeError, ValueError):
        score = 0
```

New text:

```
    score = 0
```

### `u57-recognition-and-items.M7_fold_never_takes_best_score`

Adjacent answers fold to the first, whatever the later one scored

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M7_fold_never_takes_best_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_to_the_first_offset_and_best_score`

Old text:

```
            if found.score > last.score:
```

New text:

```
            if False:
```

### `r1056.F1_no_fold`

years_filed: compare the label unfolded, so a decomposed spelling is another label

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F1_no_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_spelled_decomposed_on_either_side_is_the_same_label`

Old text:

```
        if _folded(named) == wanted and tracks > 0:
```

New text:

```
        if named == label and tracks > 0:
```

### `r1056.F2_empty_year_counts`

years_filed: count a year whose entry held no track

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F2_empty_year_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_year_filed_under_another_label_or_holding_no_track_is_not_marked`

Old text:

```
        if _folded(named) == wanted and tracks > 0:
```

New text:

```
        if _folded(named) == wanted and tracks >= 0:
```

### `r1056.F3_any_label_counts`

years_filed: count a year filed under any label

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F3_any_label_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_label_batch_landed_natively_with_a_manifest_is_marked_by_its_pass`
  - `tests/test_label_mark_native.py::test_a_label_is_compared_exactly_otherwise`
  - `tests/test_label_mark_native.py::test_a_pass_whose_landings_filed_none_of_the_built_years_marks_nothing_and_says_so[another-label]`
  - `tests/test_label_mark_native.py::test_a_year_filed_under_another_label_or_holding_no_track_is_not_marked`

Old text:

```
        if _folded(named) == wanted and tracks > 0:
```

New text:

```
        if tracks > 0:
```

### `r1056.F4_non_list_read_as_empty`

years_filed: read a labels value that is not a list as nothing filed

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F4_non_list_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-string]`

Old text:

```
    if not isinstance(filed, list):
        return None
```

New text:

```
    if not isinstance(filed, list):
        return frozenset()
```

### `r1056.F5_non_dict_entry_skipped`

years_filed: skip an entry that is not a mapping rather than refuse the record

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F5_non_dict_entry_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-list-of-strings]`

Old text:

```
        if not isinstance(entry, dict):
            return None
```

New text:

```
        if not isinstance(entry, dict):
            continue
```

### `r1056.F6_text_year_accepted`

years_filed: accept any year value, so a text year is read rather than refused

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F6_text_year_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-year]`
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-text-year]`

Old text:

```
            or not isinstance(year, int)
            or isinstance(year, bool)
```

New text:

```
            or year is None
```

### `r1056.F7_bool_tracks_accepted`

years_filed: accept a boolean track count

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F7_bool_tracks_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_record_naming_its_filing_in_a_form_this_build_cannot_read_is_refused[a-bool-tracks]`

Old text:

```
            or not isinstance(tracks, int)
            or isinstance(tracks, bool)
```

New text:

```
            or not isinstance(tracks, int)
```

### `r1056.F8_no_zero_pad`

years_filed: spell a year unpadded, unlike the ledger

- File: `src/cratekit/intake/label_filing.py`
- Source: `r1056.json`, row `F8_no_zero_pad`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_mark_native.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_mark_native.py::test_a_year_is_four_digits_as_the_ledger_spells_it`

Old text:

```
            years.add(f"{year:04d}")
```

New text:

```
            years.add(str(year))
```

### `u150.F1_blank_ref_claims`

label_filing._refs: let a manifest row with no id claim a file, so a file another row names records no track

- File: `src/cratekit/intake/label_filing.py`
- Source: `u150.json`, row `F1_blank_ref_claims`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_intake_land_labels_native.py`
- Collected: 90 against a baseline of 90
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_row_with_no_id_makes_no_claim_on_a_file_another_row_names`
  - `tests/test_organize_mirror_inbox.py::test_the_label_plans_refs_leave_out_a_target_two_rows_name_two_tracks`

Old text:

```
                if not ref:
                    continue
                for target in targets:
```

New text:

```
                for target in targets:
```

### `u156.L10_staging_dropped`

supported_only: keep the targets a landing leaves in staging, so a year playlist plans members no row answers

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L10_staging_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere`

Old text:

```
        held = tuple(target for target in one.targets if target in kept)
```

New text:

```
        held = one.targets
```

### `u156.L11_unlanded_named`

write: drop the member whose file did not land without naming it

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L11_unlanded_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`

Old text:

```
            if held:
                ids.append(held)
            else:
                left.append(
```

New text:

```
            if held:
                ids.append(held)
            elif False:
                left.append(
```

### `u156.L12_empty_year`

write: make a year playlist even when no member of it landed

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L12_empty_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`

Old text:

```
        if ids:
            wanted.append((one, tuple(dict.fromkeys(ids))))
```

New text:

```
        wanted.append((one, tuple(dict.fromkeys(ids))))
```

### `u156.L13_tree_reused`

write: make a new tree folder even when the plan found one, so Record Labels doubles

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L13_tree_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`

Old text:

```
    if plan.tree_folder:
        tree = _live_row(
```

New text:

```
    if False:
        tree = _live_row(
```

### `u156.L14_folder_reused`

write: make a new label folder even when the plan found one

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L14_folder_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`

Old text:

```
            if planned:
                folder = _live_row(
```

New text:

```
            if False:
                folder = _live_row(
```

### `u156.L15_year_reused`

write: make a new year playlist even when the plan found one, so the year doubles

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L15_year_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_the_same_files_landed_again_add_no_second_membership`
  - `tests/test_intake_land_labels_native.py::test_the_write_refuses_a_planned_node_removed_since_the_plan`

Old text:

```
        if one.playlist_id:
            playlist = _live_row(
```

New text:

```
        if False:
            playlist = _live_row(
```

### `u156.L16_live_at_write`

_live_row: take a planned node removed since the plan, so the write files into a playlist nobody sees

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L16_live_at_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_write_refuses_a_planned_node_removed_since_the_plan`

Old text:

```
    if row is None or rb_writer.node_removed(row) or not _of_kind(row, folder=folder):
```

New text:

```
    if row is None:
```

### `u156.L17_digest_years`

identity: leave the year playlists out of the digest, so an answer survives a playlist made since

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L17_digest_years`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`

Old text:

```
        "years": [one.identity() for one in plan.years],
```

New text:

```
        "years": [],
```

### `u156.L1_year_bound`

_read_year: take any four digits as a release year, so a 0000 placeholder files under year 0

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L1_year_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_with_no_reason_behind_it_is_named_with_why[0000-names 0, which is no release year]`
  - `tests/test_intake_land_labels_native.py::test_a_year_with_no_reason_behind_it_is_named_with_why[1899-01-01-names 1899]`
  - `tests/test_intake_land_labels_native.py::test_a_year_with_no_reason_behind_it_is_named_with_why[2999-names 2999]`

Old text:

```
    if not FIRST_YEAR <= year <= _today().year + 1:
```

New text:

```
    if False:
```

### `u156.L21_read_back`

assert_read_back: accept a year playlist that does not hold what the plan named

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L21_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_an_answer_the_database_does_not_hold_is_refused`

Old text:

```
        missing = [content for content in one.ids if content not in live]
        if missing:
```

New text:

```
        missing = [content for content in one.ids if content not in live]
        if False:
```

### `u156.L2_bridge_guard`

_catalog_node: drop the refusal of a library whose intake tree is on the bridge, so the tree is appended beside an intake file

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L2_bridge_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_plan_refuses_a_library_whose_intake_tree_is_on_the_bridge`

Old text:

```
    if declared is None or not medium.native:
```

New text:

```
    if declared is None:
```

### `u156.L3_wrong_kind`

_sole: drop the refusal of a node of the other kind, so a playlist named for the label stands where its folder belongs

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L3_wrong_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_playlist_where_the_label_folder_belongs_is_refused_before_the_gate`
  - `tests/test_intake_land_labels_native.py::test_a_smart_playlist_where_a_year_playlist_belongs_is_refused_before_the_gate`

Old text:

```
        if not _of_kind(row, folder=folder):
```

New text:

```
        if False:
```

### `u156.L4_two_of_a_name`

_sole: admit two siblings of one name, so the first the query yields is written into

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L4_two_of_a_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_two_record_labels_folders_are_refused_before_the_gate`

Old text:

```
    if len(named) > 1:
```

New text:

```
    if len(named) > 2:
```

### `u156.L5_nfc_fold`

_folded: compare names as stored, so a decomposed label folder is not found and a second is made

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L5_nfc_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_label_tag_spelled_decomposed_files_under_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_one_label_spelled_two_ways_in_a_manifest_is_one_folder`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return name
```

### `u156.L6_removed_nodes`

_live_children: keep removed nodes, so a playlist a person deleted in rekordbox is written into

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L6_removed_nodes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`

Old text:

```
    return [row for row in under if not rb_writer.node_removed(row)]
```

New text:

```
    return under
```

### `u156.L7_year_boundary`

_YEAR: drop the digit boundary, so 20210305 reads as 2021

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L7_year_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits[20210305-None]`

Old text:

```
_YEAR = re.compile(r"^\s*(\d{4})(?!\d)")
```

New text:

```
_YEAR = re.compile(r"^\s*(\d{4})")
```

### `u156.L8_year_anchor`

year_of: search the tag rather than read its head, so a year anywhere in the text is taken

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L8_year_anchor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_the_year_is_the_date_tags_leading_four_digits[March 2021-None]`

Old text:

```
    found = _YEAR.match(stored)
```

New text:

```
    found = re.search(r"(\d{4})(?!\d)", stored)
```

### `u156.L9_no_year_named`

plan_for_label: file a file with no year under a year of none instead of naming it

- File: `src/cratekit/intake/label_filing.py`
- Source: `u156.json`, row `L9_no_year_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_screen_with_nothing_to_file_says_so`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_left_in_staging_is_not_said_to_be_in_the_intake_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_the_move_refused_is_said_not_to_have_landed`

Old text:

```
        year, why = _read_year(source)
        if year is None:
```

New text:

```
        year, why = _read_year(source)
        if False:
```

### `u177.C1_label_fold`

_read_label: drop the NFC fold, so one label spelled two ways makes two folders

- File: `src/cratekit/intake/label_filing.py`
- Source: `u177.json`, row `C1_label_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_label_tag_spelled_decomposed_files_under_the_composed_folder`

Old text:

```
    named = _folded(str(stored or "").strip())

```

New text:

```
    named = str(stored or "").strip()

```

### `u177.C2_no_label_filed`

plan_for_tags: file a file with no label tag under an empty label, not under none

- File: `src/cratekit/intake/label_filing.py`
- Source: `u177.json`, row `C2_no_label_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`

Old text:

```
        if not label or year is None:
            unfiled.append(
                Unfiled(
                    target=str(target),
                    reason=landing.NO_LABEL,
                    sentence=(
                        f"{target.name} was filed under no "

```

New text:

```
        if label and year is None:
            unfiled.append(
                Unfiled(
                    target=str(target),
                    reason=landing.NO_LABEL,
                    sentence=(
                        f"{target.name} was filed under no "

```

### `r1255.R1_rotation_unlisted_from_scan`

landings: never read the listing off the scan, so the classifier's reason counts one record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R1_rotation_unlisted_from_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
    unlisted = session.log_unlisted(unreadable, cfg)
```

New text:

```
    unlisted = False
```

### `r1255.R2_plan_carries_unlisted`

plan_rotation: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R2_plan_carries_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        log_unlisted=found.unlisted,
```

New text:

```
        log_unlisted=False,
```

### `u111-c.C3_inboxed_suffix`

A name ending _inboxed is no longer recognised as a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C3_inboxed_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_each_batch_says_how_it_was_recognised_and_what_it_was_aged_from`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
    if name.endswith(INBOXED_SUFFIX):
```

New text:

```
    if False:
```

### `u111-c.C4_removal_threshold`

A batch in Old is removed after the stale threshold instead of the expired one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C4_removal_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_batch_moved_past_expiry_is_removed_by_the_next_run_and_then_nothing`
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`

Old text:

```
        action = REMOVE if age > expired_days else KEEP
```

New text:

```
        action = REMOVE if age > stale_days else KEEP
```

### `u111-c.C5_move_threshold`

A batch in INBOX moves only after the expired threshold instead of the stale one

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C5_move_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_and_the_second_run_reuses_it`
  - `tests/test_inbox_rotate.py::test_the_forty_and_the_hundred_move_the_old_one_hundred_twenty_goes_and_no_track_moves`

Old text:

```
        action = MOVE if age > stale_days else KEEP
```

New text:

```
        action = MOVE if age > expired_days else KEEP
```

### `u111-c.C6_plan_taken_again`

The write no longer takes the plan again on its own handle and compares digests

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C6_plan_taken_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_the_engine_refuses_a_plan_inbox_no_longer_matches`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u111-c.C7_old_creation_planned`

The folder the write creates for Old is not named to the confinement judge

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-c.json`, row `C7_old_creation_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_second_run_plans_nothing_and_still_asks`
  - `tests/test_inbox_rotate.py::test_old_is_created_once_and_the_second_run_reuses_it`

Old text:

```
                created.append(str(old.ID))
```

New text:

```
                pass
```

### `u111-d.C10_two_olds_refused`

Two live Old folders under INBOX are no longer refused, the first is used

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C10_two_olds_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_two_old_folders_are_refused_rather_than_one_chosen`

Old text:

```
    if len(olds) > 1:
```

New text:

```
    if len(olds) > 99:
```

### `u111-d.C9_committed_records_only`

A landing record dates its batch whether or not its commit landed

- File: `src/cratekit/intake/rotate.py`
- Source: `u111-d.json`, row `C9_committed_records_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_a_landing_record_that_committed_nothing_dates_nothing`

Old text:

```
        if str(session.SourceState.COMMITTED) not in {str(v) for v in record.sources.values()}:
```

New text:

```
        if False:
```

### `u113-c.C7_unproven_import_names`

The rotation reads an intake file's recorded names whether or not its import was proven

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C7_unproven_import_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`, `tests/test_inbox_rotate.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_an_intake_file_nobody_imported_names_nothing`

Old text:

```
        if session.IMPORT_VERIFIED_KEY in record.detail:
```

New text:

```
        if True:
```

### `u113-c.C9_earliest_name_wins`

The earliest landing of a recorded name ages it, not the latest

- File: `src/cratekit/intake/rotate.py`
- Source: `u113-c.json`, row `C9_earliest_name_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate_account_playlists.py`, `tests/test_inbox_rotate.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate_account_playlists.py::test_the_latest_landing_of_a_name_is_the_one_it_is_aged_by`

Old text:

```
                if name not in by_name or landed >= by_name[name][0]:
```

New text:

```
                if name not in by_name or landed <= by_name[name][0]:
```

### `u166.R2_rotate_reserved`

_classify: let the rotation take Analyze for a batch

- File: `src/cratekit/intake/rotate.py`
- Source: `u166.json`, row `R2_rotate_reserved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 74 against a baseline of 74
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_the_rotation_never_takes_analyze_for_a_batch_whatever_a_record_says`

Old text:

```
    if not in_old and name == native.ANALYZE:
```

New text:

```
    if False:
```

### `u175.R1_account_ids_unrecorded`

rotate._named_ids: read no account playlist off a native landing record, so a dated playlist is no batch and is neither rotated nor mirrored

- File: `src/cratekit/intake/rotate.py`
- Source: `u175.json`, row `R1_account_ids_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists_native.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_pass_batch_and_its_dated_playlists_move_together_and_expire_together`
  - `tests/test_intake_land_account_playlists_native.py::test_the_rotation_ages_an_account_playlist_by_its_landing_date`
  - `tests/test_organize_mirror_inbox.py::test_a_passs_dated_account_playlist_is_mirrored_beside_its_batch_under_its_dated_name`

Old text:

```
    accounts = record.detail.get(native.INBOX_PLAYLISTS_KEY)
    if isinstance(accounts, list):
```

New text:

```
    accounts = None
    if isinstance(accounts, list):
```

### `u214.M15_unread_is_not_none`

_classify: say no landing record names an unrecognised playlist even while a session record could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M15_unread_is_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
            if unread
            else
```

New text:

```
            if False
            else
```

### `u214.M16_old_only_under_inbox`

_classify: read a folder named Old inside Old as the Old folder too

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M16_old_only_under_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if old_display is not None and name == old_display:
```

### `u214.M18_folder_unknown`

_batch_folder: read a refused batch folder as absent, so a batch is said to have none

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M18_folder_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
    except OSError:
        return None
```

New text:

```
    except OSError:
        return False
```

### `u214.M19_folder_unread_reason`

_classify: say no batch folder carries the name even while the music folder could not be read

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M19_folder_unread_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`

Old text:

```
            if folder_unread

```

New text:

```
            if False

```

### `u214.M1_old_named_as_old`

_classify: never name the declared Old as Old, so it reads as any folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M1_old_named_as_old`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        if not in_old and old_display is not None and name == old_display:
```

New text:

```
        if False:
```

### `u214.M20_unread_unlisted`

Landings.unread: say nothing of a log that could not be listed

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M20_unread_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        if self.unlisted:
```

New text:

```
        if False:
```

### `u214.M2_left_row_count`

_classify: count no rows for a left playlist, so the unrecognised label playlist is named without its 36 rows

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M2_left_row_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_payload_shows_each_left_node_with_its_row_count`

Old text:

```
        tracks = _track_count(db, row) if counted else None
```

New text:

```
        tracks = None
```

### `u214.M3_live_left_collected`

live_batches: collect no left node, so the mirror drops them unsaid again

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M3_live_left_collected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_a_music_folder_that_cannot_be_read_is_never_read_as_no_batch_folder`
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_inbox_unmirrored.py::test_an_undeclared_old_is_named_as_a_folder`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
        else:
            left.append(classified)
    return Live(
```

New text:

```
        else:
            pass
    return Live(
```

### `u214.M4_digest_without_count`

identity: digest each left node with its row count, so adding a track to a person's playlist stales the rotation gate

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M4_digest_without_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_row_added_to_a_left_playlist_does_not_move_the_rotations_digest`

Old text:

```
        "left": [node.identity() for node in plan.left],
```

New text:

```
        "left": [node.to_json() for node in plan.left],
```

### `u214.M5_rotation_old_display`

plan_rotation: pass no Old display, so the rotation plan names Old as a folder and the mirror as Old

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M5_rotation_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
            old_display=old.display,
```

New text:

```
            old_display=None,
```

### `u214.M6_live_old_display`

live_batches: read no Old display, so the mirror names Old as a plain folder

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M6_live_old_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_inbox_unmirrored.py::test_the_rotation_plan_names_the_same_nodes_the_same_way`

Old text:

```
    old_display = declared.intake_old.display if declared.intake_old is not None else None
```

New text:

```
    old_display = None
```

### `u214.M7_label_rows`

Left.label: leave the row count out of the line a person reads

- File: `src/cratekit/intake/rotate.py`
- Source: `u214.json`, row `M7_label_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`

Old text:

```
        rows = f" ({self.tracks} row(s))" if self.tracks is not None else ""
```

New text:

```
        rows = ""
```

### `r1255.B1_batch_name_clause`

batch_name._records: word the refusal with the old count, not the clause

- File: `src/cratekit/intake/batch_name.py`
- Source: `r1255.json`, row `B1_batch_name_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_intake_shelve.py`, `tests/test_inbox_rotate.py`
- Collected: 105 against a baseline of 105
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_an_unreadable_record_keeps_its_own_refusal`
  - `tests/test_session_log_unlisted.py::test_the_batch_name_rule_refuses_rather_than_call_a_name_free`

Old text:

```
            f"{session.unread_clause(unreadable, cfg)}, so no batch name can be called "
```

New text:

```
            f"the session log holds {len(unreadable)} entries this build cannot read, so no batch name can be called "
```

### `u110-a.A2_favorites_word`

A hearts job says Tidal playlists instead of Favorites

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A2_favorites_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 132 against a baseline of 132
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_job_the_pass_lost_does_not_name_the_batch`
  - `tests/test_intake_land_names.py::test_each_kind_of_pass_job_says_its_own_word`

Old text:

```
        return FAVORITES if source_id == intake_cli.FAVORITES_SOURCE_ID else PLAYLISTS
```

New text:

```
        return PLAYLISTS
```

### `u110-a.A5_several_labels`

A manifest naming several labels is named for its first label, not Labels

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A5_several_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_label_rows_name_one_label_by_its_name_and_several_as_labels`

Old text:

```
else LABELS
```

New text:

```
else next(iter(named.values()))
```

### `u110-a.A6_folder_safe`

A label name's slash and colon reach the folder name unreplaced

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A6_folder_safe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_label_rows_name_one_label_by_its_name_and_several_as_labels`

Old text:

```
_UNSAFE.sub("-", text)
```

New text:

```
text
```

### `u110-a.A7_join_order`

Several pass words are joined alphabetically instead of in the fixed order

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A7_join_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 132 against a baseline of 132
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_job_the_pass_lost_does_not_name_the_batch`
  - `tests/test_intake_land_names.py::test_several_words_are_joined_in_one_order_whatever_order_they_arrive_in`

Old text:

```
    ordered = [word for word in _ORDER if word in present]
```

New text:

```
    ordered = [word for word in sorted(present) if word in _ORDER]
```

### `u110-a.A8_labels_first`

Label rows lose their precedence over the pass's jobs

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A8_labels_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`

Old text:

```
    said = label_words(label_rows)
    if said is not None:
        return said
    if pass_name:
```

New text:

```
    if pass_name:
```

### `u113-a.A4_batch_name_not_taken`

An account playlist may take the batch's own name

- File: `src/cratekit/intake/batch_name.py`
- Source: `u113-a.json`, row `A4_batch_name_not_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`

Old text:

```
    taken = {*held, batch}
```

New text:

```
    taken = {*held}
```

### `u113-a.A5_landing_names_its_own`

Two account playlists of one name in one landing share it

- File: `src/cratekit/intake/batch_name.py`
- Source: `u113-a.json`, row `A5_landing_names_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`

Old text:

```
        taken.add(candidate)
        named.append(candidate)
```

New text:

```
        named.append(candidate)
```

### `u154.R5_unreadable_record_fails_open`

an unreadable session record is dropped and a shelved name reads free

- File: `src/cratekit/intake/batch_name.py`
- Source: `u154.json`, row `R5_unreadable_record_fails_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_an_unreadable_session_record_makes_the_name_rule_refuse_rather_than_read_a_name_free`

Old text:

```
    if unreadable:
        raise refuse(

```

New text:

```
    if False:
        raise refuse(

```

### `u164.B1_taken_recorded`

taken: read the music folder alone, as before U164

- File: `src/cratekit/intake/batch_name.py`
- Source: `u164.json`, row `B1_taken_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_shelve.py`, `tests/test_intake_land_names.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_two_unnamed_landings_on_one_day_are_two_playlists_and_never_one`
  - `tests/test_intake_shelve.py::test_a_shelved_batch_name_stays_taken_so_a_landing_that_day_takes_the_next`
  - `tests/test_intake_shelve.py::test_an_unreadable_session_record_makes_the_name_rule_refuse_rather_than_read_a_name_free`

Old text:

```
    return os.path.lexists(landing.target_dir(cfg, name)) or name in recorded
```

New text:

```
    return os.path.lexists(landing.target_dir(cfg, name))
```

### `u164.B2_native_names`

recorded_names: read shelve records alone and skip native landings

- File: `src/cratekit/intake/batch_name.py`
- Source: `u164.json`, row `B2_native_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_shelve.py`
- Collected: 112 against a baseline of 112
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_filed.py::test_a_second_unnamed_landing_that_day_takes_two_for_its_playlist_and_its_folder`
  - `tests/test_intake_land_native.py::test_two_unnamed_landings_on_one_day_are_two_playlists_and_never_one`

Old text:

```
        elif record.workflow == native.WORKFLOW:
            for key in (native.BATCH_PLAYLIST_KEY, native.FILED_BATCH_KEY):
```

New text:

```
        elif False:
            for key in (native.BATCH_PLAYLIST_KEY, native.FILED_BATCH_KEY):
```

### `u175.N1_date_first`

dated: put the date before the account's name, the order Phillip declined

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N1_date_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 102 against a baseline of 102
- Kills: 54 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_the_job_store_is_read_not_written_by_a_plan`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    return f"{account_name} {day.isoformat()}"
```

New text:

```
    return f"{day.isoformat()} {account_name}"
```

### `u175.N2_no_date`

dated: return the account's name alone, undated as before U175

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N2_no_date`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 102 against a baseline of 102
- Kills: 54 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_the_job_store_is_read_not_written_by_a_plan`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    return f"{account_name} {day.isoformat()}"
```

New text:

```
    return account_name
```

### `u175.N3_date_form`

dated: write the date as the account's own month_day_year form rather than ISO

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N3_date_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 102 against a baseline of 102
- Kills: 54 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_the_job_store_is_read_not_written_by_a_plan`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    return f"{account_name} {day.isoformat()}"
```

New text:

```
    return f"{account_name} {day.month}_{day.day:02d}_{day.year % 100:02d}"
```

### `u175.N4_clock_not_seam`

inbox_names: read the system clock rather than the landing's today seam, so the playlist's date can differ from the batch's

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N4_clock_not_seam`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 102 against a baseline of 102
- Kills: 54 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze`
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read`
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_session_log_that_cannot_be_listed_is_named_as_one_by_the_plan`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_the_job_store_is_read_not_written_by_a_plan`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    on = today()
```

New text:

```
    on = date.today()
```

### `u175.N7_held_not_held`

inbox_names: stop holding what INBOX holds, so a second landing the same day adds into the first's playlist

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N7_held_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 102 against a baseline of 102
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_names_each_playlist_as_the_bridge_does`

Old text:

```
    taken = {*held, batch}
```

New text:

```
    taken = {batch}
```

### `u175.N8_counter_before_date`

inbox_names: count from the undated name, so a held name becomes Sunset Warmup 2 with no date

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N8_counter_before_date`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_refill.py`
- Collected: 102 against a baseline of 102
- Kills: 9 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_an_account_playlist_named_analyze_lands_dated_and_never_as_analyze`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`
  - `tests/test_intake_land_account_playlists.py::test_a_name_at_the_playlist_root_is_not_given_since_an_import_lands_there`
  - `tests/test_intake_land_account_playlists.py::test_an_account_playlist_whose_dated_name_is_the_batchs_takes_two`
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_names_each_playlist_as_the_bridge_does`

Old text:

```
            candidate = f"{base} {count}"
        taken.add(candidate)
```

New text:

```
            candidate = f"{account_name} {count}"
        taken.add(candidate)
```

### `u175.N9_landing_not_held`

inbox_names: do not hold a name an earlier playlist of the same landing took, so two account playlists of one name share one INBOX playlist

- File: `src/cratekit/intake/batch_name.py`
- Source: `u175.json`, row `N9_landing_not_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_inbox_analyzed.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_inbox_names_counts_past_every_name_inbox_holds_and_this_landing_took`

Old text:

```
            candidate = f"{base} {count}"
        taken.add(candidate)
```

New text:

```
            candidate = f"{base} {count}"
        pass
```

### `u179.N1_one_label_only_when_all_named`

bandcamp name: name the batch for its one label even when a file carries none

- File: `src/cratekit/intake/batch_name.py`
- Source: `u179.json`, row `N1_one_label_only_when_all_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_intake_land_names.py`
- Collected: 59 against a baseline of 59
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_batch_of_a_label_and_an_unregistered_seller_files_by_tag_under_a_plain_name`
  - `tests/test_sync_bandcamp.py::test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label`
  - `tests/test_sync_bandcamp.py::test_the_batch_name_is_the_one_label_every_file_names_or_plain[labels3-Bandcamp]`

Old text:

```
    if len(named) == 1 and not unnamed:
```

New text:

```
    if len(named) == 1:
```

### `u179.N2_label_case_folded`

bandcamp name: compare labels with their case, so PULS and puls read as two labels

- File: `src/cratekit/intake/batch_name.py`
- Source: `u179.json`, row `N2_label_case_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_intake_land_names.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_the_batch_name_is_the_one_label_every_file_names_or_plain[labels1-Bandcamp PULS]`

Old text:

```
            named.setdefault(said.casefold(), said)
        else:
            unnamed = True
```

New text:

```
            named.setdefault(said, said)
        else:
            unnamed = True
```

### `u179.N3_name_made_free`

bandcamp name: take the name even when a batch already holds it, so two landings merge

- File: `src/cratekit/intake/batch_name.py`
- Source: `u179.json`, row `N3_name_made_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_intake_land_names.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_taken_batch_name_takes_the_next_number`

Old text:

```
        words = f"{BANDCAMP} {next(iter(named.values()))}"
    return free(cfg, f"{today().isoformat()} {words}")
```

New text:

```
        words = f"{BANDCAMP} {next(iter(named.values()))}"
    return f"{today().isoformat()} {words}"
```

### `u113-a.A2_queue_order`

The account playlists are taken newest job first, the order the store lists them

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A2_queue_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        queued = sorted(
            batch_name.pass_jobs(cfg, pass_name), key=lambda job: (job.created, job.job_id)
        )
```

New text:

```
        queued = batch_name.pass_jobs(cfg, pass_name)
```

### `u113-a.A3_no_pass_splits_nothing`

A landing given no pass still splits, by every named job on the library

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A3_no_pass_splits_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not pass_name or not files:
        return ()
    found = sources(cfg, pass_name)
```

New text:

```
    if not files:
        return ()
    found = sources(cfg, pass_name or "")
```

### `u113-a.A8_pending_any_state`

Names held by intake files are read from records whatever their state, not only those awaiting import

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A8_pending_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_name_an_unimported_intake_file_holds_is_not_given_again`

Old text:

```
        and record.state is session.SessionState.AWAITING_IMPORT
```

New text:

```
        and record.state is not session.SessionState.AWAITING_IMPORT
```

### `u120.B2_first_mention_wins`

prefer_dated: a later mention that knows its date does not replace a first that does not

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u120.json`, row `B2_first_mention_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_two_jobs_carried_is_one_heart_with_the_dated_jobs_date`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_prefers_the_mention_that_knows_its_date`

Old text:

```
    return held is None or (not held.known and row.known)
```

New text:

```
    return held is None
```

### `u128-b.A6b_abandoned_counts`

Rerun of A6 after its test: count every landing record as standing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A6b_abandoned_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_abandoned_landing_is_not_read_as_mirrored`

Old text:

```
        if record.workflow == ingest.INTAKE_WORKFLOW and record.state in standing
```

New text:

```
        if record.workflow == ingest.INTAKE_WORKFLOW
```

### `u128-b.A8b_ambiguous_is_an_answer`

Rerun of A8 after its test: take the first of two active rows as the owned row

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A8b_ambiguous_is_an_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_file_two_active_rows_claim_is_no_owned_row`

Old text:

```
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = ("", AMBIGUOUS_ROWS)
                    continue
```

New text:

```
                if matched.outcome is trees.MatchOutcome.AMBIGUOUS:
                    answer = (str(matched.content_ids[0]), "")
                    break
```

### `u128-b.A9b_emptied_left_lost`

Rerun of A9 after its test: drop the left rows of a claim left holding nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128-b.json`, row `A9b_emptied_left_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_claim_left_holding_nothing_still_answers_its_left_rows`

Old text:

```
            emptied.extend((one.name, row) for row in left)
```

New text:

```
            pass
```

### `u128.A10_no_warning`

Give no left out warning however many rows were left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A10_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`

Old text:

```
    if not left:
        return []
    named_rows
```

New text:

```
    if True:
        return []
    named_rows
```

### `u128.A1_owned_not_mirrored`

Drop every owned member from the claim, U113's new tracks only rule

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A1_owned_not_mirrored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 13 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`
  - `tests/test_intake_land_account_playlists.py::test_an_export_rewritten_after_the_gate_moves_nothing`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists.py::test_an_owned_track_whose_row_the_export_does_not_hold_is_warned`
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`
  - `tests/test_intake_land_account_playlists.py::test_the_gate_screen_counts_the_owned_tracks_beside_the_new`
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_whose_row_cannot_be_found_by_path_is_warned`
  - `tests/test_intake_land_account_playlists_native.py::test_the_gate_screen_counts_the_owned_rows_beside_the_new`

Old text:

```
            if row.paths not in seen:
                seen.add(row.paths)
                members.append(_member(row))
```

New text:

```
            if row.paths not in seen:
                seen.add(row.paths)
```

### `u128.A2_rerun_unseen`

Never read a playlist as already mirrored by this pass, so a rerun mirrors the owned tracks again

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A2_rerun_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
        rerun = source.playlist_id in again
```

New text:

```
        rerun = False
```

### `u128.A3_rerun_keeps_owned`

On a rerun, keep the owned members and the left rows instead of the new files alone

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A3_rerun_keeps_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
            if rerun:
                continue
            if row.state != OWNED:
```

New text:

```
            if row.state != OWNED:
```

### `u128.A4_untied_carried_silent`

A carried row no planned file answers is silently absent rather than left

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A4_untied_carried_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_track_neither_owned_nor_brought_is_named_in_the_warnings`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`

Old text:

```
                if not tied:
                    left.append(_left(row, NOT_BROUGHT))
```

New text:

```
                if not tied:
                    pass
```

### `u128.A7_any_pass_counts`

Read a playlist as mirrored when any pass landed it, not only this one

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u128.json`, row `A7_any_pass_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_a_bridge_landing_is_what_a_rerun_of_its_pass_reads_as_mirrored`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`

Old text:

```
        and entry.get(PASS_KEY) == pass_name
```

New text:

```
        and entry.get(PASS_KEY) is not None
```

### `u145.M3_landing_heart_undated`

Hearted.month: a landed heart whose job dated it goes to Undated

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M3_landing_heart_undated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_hearts_native.py`
- Collected: 19 against a baseline of 19
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land_hearts_native.py::test_a_heart_a_playlist_also_asked_for_is_in_that_playlist_and_in_all_favorites`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_dated_the_twentieth_of_october_joins_its_month_and_no_quarter_is_made`
  - `tests/test_intake_land_hearts_native.py::test_a_heart_whose_job_froze_no_date_key_joins_all_favorites_and_no_month`
  - `tests/test_intake_land_hearts_native.py::test_a_hearted_file_lands_in_its_batch_all_favorites_and_a_month_made_for_it`
  - `tests/test_intake_land_hearts_native.py::test_a_source_at_the_root_takes_its_months_beside_it`
  - `tests/test_intake_land_hearts_native.py::test_the_hearts_are_in_the_digest_so_another_set_is_another_plan`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_jobs_hearts_are_read_from_the_job_and_a_playlist_job_claims_no_heart`
  - `tests/test_intake_land_hearts_native.py::test_the_pass_prefers_the_mention_that_knows_its_date`
  - `tests/test_intake_land_hearts_native.py::test_the_record_carries_the_hearts_placed_under_their_own_key`
  - `tests/test_intake_land_hearts_native.py::test_two_hearts_of_two_months_and_an_existing_month_is_added_to_not_made`
  - `tests/test_intake_land_hearts_native.py::test_with_no_pink_row_the_landing_places_the_heart_and_warns`

Old text:

```
        return placeholders.month_label(self.hearted) if self.known else None
```

New text:

```
        return placeholders.UNDATED if self.known else None
```

### `u145.M4_states_carried_only`

carried_hearts: states=None still reads only the carried states, so an owned row dates nothing

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u145.json`, row `M4_states_carried_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_split.py`, `tests/test_favorites_backfill.py`
- Collected: 64 against a baseline of 64
- Kills: 8 (killed)
- Killed:
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_and_undated_holds_is_not_given_a_month`
  - `tests/test_favorites_backfill.py::test_a_heart_all_favorites_holds_at_the_root_beside_another_playlist_still_takes_its_month`
  - `tests/test_favorites_backfill.py::test_a_heart_its_job_dated_nowhere_stays_undated_though_the_account_dates_it_now`
  - `tests/test_favorites_backfill.py::test_a_heart_put_back_by_hand_after_a_removal_takes_its_month_and_is_not_taken_back`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_in_a_batch_folder_is_placed_beside_a_downloaded_one`
  - `tests/test_favorites_backfill.py::test_an_owned_heart_the_source_system_filed_is_placed_and_one_with_no_row_is_not`
  - `tests/test_favorites_backfill.py::test_owned_hearts_not_in_all_favorites_are_planned_by_month_and_those_taken_back_are_named`
  - `tests/test_favorites_split.py::test_a_job_row_owned_when_its_job_ran_still_dates_the_member`

Old text:

```
        if states is not None and report.get("state") not in states:
```

New text:

```
        if report.get("state") not in (states or CARRIED_STATES):
```

### `u146-b.A1_superseded_ignored`

owned_hearts: an older pass places its owned hearts though a later hearts job ran, putting back a heart dropped since

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A1_superseded_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_landing_an_older_pass_places_no_owned_heart_once_a_later_hearts_job_ran`

Old text:

```
    if superseded:
        return ()
```

New text:

```
    if superseded and False:
        return ()
```

### `u146-b.A2_owned_reads_carried`

owned_hearts: reads the carried states, so the landing finds no owned heart

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A2_owned_reads_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 12 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
    return hearts(cfg, pass_name, states=frozenset({OWNED}))
```

New text:

```
    return hearts(cfg, pass_name)
```

### `u146-b.A3_report_paths_dropped`

carried_hearts: the report's files are not carried on the row, so no owned heart has a row to place

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A3_report_paths_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`

Old text:

```
                known=intake_cli.HEARTED in said,
                paths=tuple(str(path) for path in (report.get("paths") or ())),
```

New text:

```
                known=intake_cli.HEARTED in said,
                paths=(),
```

### `u165.F1_reset_cache`

file_landed: plan over the cached collection without forgetting it (round one's test)

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F1_reset_cache`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_collection_read_before_the_commit_does_not_hide_the_landed_rows`

Old text:

```
    collection.reset_cache()

```

New text:

```
    pass

```

### `u165.F2_compare`

file_landed: never compare the plan after the commit with the prediction

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F2_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`

Old text:

```
        if now != one.place:
```

New text:

```
        if False:
```

### `u165.F3_differing_files`

file_landed: file even when a row differs from its prediction

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F3_differing_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_plan_after_the_commit_that_differs_files_nothing_and_says_so`

Old text:

```
    if differing:
        return Filed(state=FILED_DIFFERENTLY
```

New text:

```
    if False:
        return Filed(state=FILED_DIFFERENTLY
```

### `u165.F4_vox_predicted`

predict: never predict the vocal sub

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F4_vox_predicted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_five_files_land_and_file_under_one_answer`

Old text:

```
vox=row.vox),
```

New text:

```
vox=False),
```

### `u165.F5_report_failed`

file_landed: report a filing whose entries failed as filed

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F5_report_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if report.failed:
        return Filed(
            state=NOT_FILED,
```

New text:

```
    if False:
        return Filed(
            state=NOT_FILED,
```

### `u165.F6_unplaced`

_refuse_unplaced: never refuse a landed row the tree writer could not place

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F6_unplaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 152 against a baseline of 152
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_filing.py::test_a_landed_row_the_tree_could_not_place_refuses_before_the_ledger_is_marked`

Old text:

```
    if not membership.skipped:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} landed row(s)
```

New text:

```
    if True:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
    raise refuse(
        "adopt-entries-failed",
        f"{len(unplaced)} landed row(s)
```

### `r740-b.E2_average_bpm_nonzero`

existing guard sample: the intake row's AverageBpm literal becomes a tempo

- File: `src/cratekit/intake/collection_xml.py`
- Source: `r740-b.json`, row `E2_average_bpm_nonzero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 108 against a baseline of 108
- Kills: 8 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_the_gridless_constant_even_when_bpm_is_present`
  - `tests/intake/test_pipeline.py::test_single_file_ingest_uses_no_network`
  - `tests/test_landing_head.py::test_a_file_headed_in_its_filename_only_carries_that_head`
  - `tests/test_landing_head.py::test_a_file_headed_nowhere_lands_bare_and_nothing_invents_a_tempo`
  - `tests/test_landing_head.py::test_a_lossy_file_keeps_its_marker_on_all_three_surfaces`
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_a_title_headed_file_with_no_tempo_elsewhere_lands_named_as_its_title`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="112.00"
```

### `r770-d.S1_composite_the_splice_takes_a_stub`

COMPOSITE for r770-a's S1, which was a zero: collection_xml.splice_tracks does not refuse a U22 stub listing, with place_files' own refusal left in place. The driver pairs only inside one batch, so the pairing is recorded in r770-notes.md

- File: `src/cratekit/intake/collection_xml.py`
- Source: `r770-d.json`, row `S1_composite_the_splice_takes_a_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_landing.py`, `tests/test_intake_imported.py`, `tests/intake/test_collection_xml.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_a_u22_stub_listing_is_not_a_splice_target`
  - `tests/test_landing.py::test_a_stub_export_is_refused_before_any_move`

Old text:

```
    if is_stub_listing(raw):
```

New text:

```
    if False:
```

### `u37-author-light.G1_stub_listing`

Treat a U22 stub listing as a spliceable Fresh Export

- File: `src/cratekit/intake/collection_xml.py`
- Source: `u37-author-light.json`, row `G1_stub_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_a_u22_stub_listing_is_not_a_splice_target`

Old text:

```
    if is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
```

New text:

```
    if False and is_stub_listing(raw):
        raise refuse(
            "intake-export-is-stub",
```

### `u37-author-light.G3_gridless_bpm`

Write a real AverageBpm instead of the gridless constant

- File: `src/cratekit/intake/collection_xml.py`
- Source: `u37-author-light.json`, row `G3_gridless_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_the_gridless_constant_even_when_bpm_is_present`

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="124.00"
```

### `u166.C12_ack_first`

inbox_analyzed: drop the backup acknowledgment before the plan

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u166.json`, row `C12_ack_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u166.C13_read_back_call`

inbox_analyzed: skip the read back after the commit

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u166.json`, row `C13_read_back_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_cli_contract.py`, `tests/test_inbox_rotate.py`
- Collected: 1066 against a baseline of 1066
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`

Old text:

```
    analyzed.assert_read_back(plan, cleared)
```

New text:

```
    pass
```

### `u173.M21_gate_name`

analyzed_cli: the clear's gate renamed, so the skill's decide line names a gate that does not exist

- File: `src/cratekit/intake/analyzed_cli.py`
- Source: `u173.json`, row `M21_gate_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rekordbox_visit_skill.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/test_rekordbox_visit_skill.py::test_the_clear_s_gate_is_answered_by_its_own_name_and_option`

Old text:

```
APPROVE_GATE = "inbox.analyzed.approve"
```

New text:

```
APPROVE_GATE = "inbox.analyzed.confirm"
```

### `u102-a.D1_keep_is_not_accept`

decided(): read the accepted verdict alone, so an item answered keep is treated as a rename to apply

- File: `src/cratekit/intake/repair.py`
- Source: `u102-a.json`, row `D1_keep_is_not_accept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/intake/test_repair.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_open_or_rejected_or_kept_proposal_is_untouched`

Old text:

```
        elif item.option != ACCEPT:
            kept += 1
```

New text:

```
        elif item.option is None:
            kept += 1
```

### `u102-a.D2_open_is_not_accepted`

decided(): drop the branch that counts an item with no accepted verdict as open

- File: `src/cratekit/intake/repair.py`
- Source: `u102-a.json`, row `D2_open_is_not_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/intake/test_repair.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_open_or_rejected_or_kept_proposal_is_untouched`

Old text:

```
        elif item.verdict is not Verdict.ACCEPTED:
            still_open += 1
```

New text:

```
        elif False:
            still_open += 1
```

### `u37-author-light.G5_path_repair_queue`

Offer path repair into the adoption queue instead

- File: `src/cratekit/intake/repair.py`
- Source: `u37-author-light.json`, row `G5_path_repair_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/intake/test_repair.py`
- Collected: 164 against a baseline of 164
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_repair.py::test_offer_repairs_writes_path_repair_queue_items`
  - `tests/test_review_queue.py::test_every_new_adjudication_surface_is_owed_by_a_registered_unit`
  - `tests/test_review_queue.py::test_the_path_repair_pass_offers_its_proposals_into_the_path_repair_queue`

Old text:

```
            queue=Queue.PATH_REPAIR,
```

New text:

```
            queue=Queue.ADOPTION,
```

