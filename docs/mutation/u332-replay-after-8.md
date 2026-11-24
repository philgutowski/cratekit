# Mutation table: u332-replay-after-8

Measured by `scripts/mutate.py` on 2026-11-24 06:23 UTC, branch `HEAD` at `fb09b891`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23212 collected. pytest invocations for this batch: 292.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 06:23 UTC for commit `fb09b891b325`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 114, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23212 against 23212. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B6_any_two_texts_the_same` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 21 | killed |
| `u122.H5_units_only` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 4 | killed |
| `u148.C3_no_count_skips` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 2 | killed |
| `u148.W1_full_page_taken` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 3 | killed |
| `u151.M2_issue_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 2 | killed |
| `u151.X3_status_refusal_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u196.S4_missing_ledger_no_match` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 1 | killed |
| `u203.M8_ellipsis_not_trailing` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u313.B4_withdrawn_held` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `r703-a.A1_classifier_reads_text` | `src/cratekit/acquire/adapter.py` | user | 7 file(s) | 873 | 1 | killed |
| `u246.S1_adapter_asked_empty` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 260 | 70 | killed |
| `u176.C3_page_error_is_rejected` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 92 | 1 | killed |
| `u176.V12_strict_refuses_lossy` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V7_record_version` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u177.B5_registry_unread_empty` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `u205.C11_collection_404_read_as_absence` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C8_availability_ignored` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `r289-c.B2r_reclaim_reports_a_failure_as_a_removal` | `src/cratekit/acquire/cli.py` | maintainer | 6 file(s) | 367 | 1 | killed |
| `r668-a.M6_no_list_check_on_resume` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 3 | killed |
| `u169.A4_no_declined_warning` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 4 | killed |
| `u42-author.P2_relative_path_leaks_the_root` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 25 | 5 | killed |
| `u54-acquisition-worker.G15_no_marker_text` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `u54-acquisition-worker.G2_missing_identifier` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `u80.F12_open_searched_again` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.F6_ignore_errors_back` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `r289-b.C2_fallback_resume_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `u81-fetch-a.W1_strict_not_refused` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Q3_empty_queue` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 4 | killed |
| `r1016.M4_date_added_not_moved` | `src/cratekit/acquire/listing.py` | maintainer | 7 file(s) | 793 | 1 | killed |
| `r878-a.A11_count_alone_is_a_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 141 | 1 | killed |
| `r878-a.A8_no_cursor_ends` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 141 | 16 | killed |
| `r887-a.K2_playlists_kept_unfiltered` | `src/cratekit/acquire/listing.py` | user | 3 file(s) | 204 | 1 | killed |
| `u65.B4_account_playlists_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 198 | 5 | killed |
| `u65.D5_the_favourites_budget_is_tightened_onto_real_data` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 85 | 2 | killed |
| `u70.E3_hearts_declared_total` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 259 | 4 | killed |
| `u213.M1_first_group_is_the_title` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 726 | 13 | killed |
| `u261.H6_app_not_asked_again` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 96 | 3 | killed |
| `r703-a.V3_cause_not_passed` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 4 | killed |
| `r703-b.R1_status_path_dropped` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 1 | killed |
| `u47-author.CODEC_mp3_reads_as_lossless` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 1 | killed |
| `u47-author.R195_verify_skips_the_mapping` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 3 | killed |
| `u47-author.R197_drop_progress` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 3 | killed |
| `u254-m08.M08_never_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 1 | killed |
| `u254.M09_any_line_torn` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 2 | killed |
| `u254.M17_document_at_journal_schema` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 1 | killed |
| `r1991.A4_apply_records_nothing` | `src/cratekit/adopt/apply_cli.py` | user | 15 file(s) | 521 | 1 | killed |
| `u132.W2_coded_note` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 447 | 3 | killed |
| `u27-adopt-apply-author.S4_workflow_is_not_the_verb` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `u55-round-2.R8_census_prefix_map` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 1 | killed |
| `u55-collection-reader.R1_read_only_open` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 56 | 2 | killed |
| `r780-a.A3_verdict_ignored_in_tree_path` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `r797-d.M8_again_an_unread_file_is_no_reading` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 172 | 2 | killed |
| `u133-b-rerun.E2_former_place_only` | `src/cratekit/adopt/move.py` | user | 4 file(s) | 215 | 10 | killed |
| `r780-b.B4_gone_named_once_per_move` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r788-c.L2_removed_tag_files` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 163 | 2 | killed |
| `u118-b.P2_recorded_under_split` | `src/cratekit/adopt/placements.py` | maintainer | 3 file(s) | 143 | 1 | killed |
| `r722.P5_entry_drops_unreadable` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 651 | 4 | killed |
| `r731-a.M07_withheld_entry_loses_its_bucket` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 6 | killed |
| `r788-a.P5_withheld_gains` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 3 | killed |
| `r788-b.P9_unplaced_entry_gains` | `src/cratekit/adopt/plan.py` | maintainer | 4 file(s) | 163 | 1 | killed |
| `u23-round-8-independent.A1_at_risk_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 4 | killed |
| `u23-round-8-independent.C1_shape2_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 3 | killed |
| `u23-round-8-independent.F4_byte_search_reads_before_it_filters` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 613 | 2 | killed |
| `r722.S1_unreadable_folded` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 4 | killed |
| `u23-round-8-independent.X8_classify_drops_the_too_coarse_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 613 | 1 | killed |
| `u956.O3_confine_default_off` | `src/cratekit/adopt/scan.py` | user | 4 file(s) | 685 | 7 | killed |
| `u55-collection-reader.R11_scan_item_ids` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 29 | 4 | killed |
| `u223.M10_report_wrong_name` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 176 | 2 | killed |
| `u223.M4_subdir_unlinked` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 176 | 2 | killed |
| `u90-a.A1_lower_bound_strict` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 1 | killed |
| `u90-b.B3_note_reworded` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 3 | killed |
| `u94-a.S1_floor_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 3 | killed |
| `u94-b.W1_after_walk_refusal_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 1 | killed |
| `u94-c.N2_stride_is_a_fixed_step` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 1 | killed |
| `u192.A1_run_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 212 | 15 | killed |
| `u241.M13_vocal_model_not_kept_back` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 271 | 1 | killed |
| `u306.A7_calibrate_handler` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 44 | killed |
| `u343.M24_twin_recovery_off` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 4 | killed |
| `u94-c.N6_default_sample_halved` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 212 | 1 | killed |
| `u264.M6_any_release_measured` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 8 | killed |
| `u343.M22_record_keeps_key_buckets` | `src/cratekit/analysis/detect.py` | user | 2 file(s) | 92 | 2 | killed |
| `u327.A10_file_missing_named` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u327.A1_key_equal_by_wheel` | `src/cratekit/analysis/head_adopt.py` | user | 2 file(s) | 161 | 1 | killed |
| `u342.E3_stale_plan_refuses` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 1 | killed |
| `u342.P6_stamped_not_left` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 1 | killed |
| `u342.C4_written_says_no_rename` | `src/cratekit/analysis/head_adopt_cli.py` | user | 4 file(s) | 392 | 1 | killed |
| `u275.M6_unknown_length_shorter` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 553 | 2 | killed |
| `sitting3.G11_tail_dropped` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 2 | killed |
| `sitting3.G7_chatter_on_stdout` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 1 | killed |
| `u58-workers-and-wav.W3_undecodable_scored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 176 | 2 | killed |
| `u92-author.G4_cap_doubled` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 230 | 1 | killed |
| `r221-a.S3_flag_reads_a_key_nothing_freezes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 7 | killed |
| `r221-b.M4_steps_replaced_not_joined` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B3_any_library_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r290-author.S04_backup_call_removed` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 215 | 11 | killed |
| `r757-c1.S1_resume_drops_the_full_flag` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 727 | 1 | killed |
| `u45-round-1.A4_state_collapsed_to_known` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.Q2_resume_always_rehearses` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-1.W5_publishing_switched_off` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 8 | killed |
| `u50-author.W5_unknown_portion_unchecked` | `src/cratekit/backup/cli.py` | maintainer | 1 file(s) | 89 | 1 | killed |
| `r924.D1_json_gets_progress` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 52 | 1 | killed |
| `u55-collection-reader.R30_scan_handler_bound` | `src/cratekit/cli/handlers.py` | user | 5 file(s) | 243 | 6 | killed |
| `u27-adopt-apply-author.R1_marker_restored` | `src/cratekit/cli/registry_modules.py` | user | 3 file(s) | 1732 | collection error | collect-error |
| `r925.R3_no_isrc_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 2 | killed |
| `u247.M7_load_keyed_on_path_size_time` | `src/cratekit/core/active_taxonomy.py` | user | 4 file(s) | 293 | 2 | killed |
| `u260.E3_key_drops_cap` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u83-a.E10_reported_dimensions` | `src/cratekit/core/art.py` | maintainer | 1 file(s) | 73 | 1 | killed |
| `u83-a.E9_resize` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-b.W2_format_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `r349-b.B1_absent_is_none` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 89 | 1 | killed |
| `u953.M19_backup_facts_damaged_remedy` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 753 | 9 | killed |
| `u331.S03_yt_dlp_install_step_dropped` | `src/cratekit/core/binaries.py` | user | 3 file(s) | 113 | 2 | killed |
| `u254.C1_append_unsynced` | `src/cratekit/core/config.py` | user | 4 file(s) | 962 | 1 | killed |
| `r290-author.J2_blocked_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 48 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 18 file(s) | 1398 | 122 | killed |
| `u342.S2_stamp_refuses_a_marker_alone` | `src/cratekit/core/naming.py` | user | 4 file(s) | 392 | 3 | killed |
| `u205.G2_app_rate_limit_not_counted` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 184 | 1 | killed |
| `r758-a.W1_marker_not_judged` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 300 | 74 | killed |
| `r679-a.A8_actor_is_not_the_rule` | `src/cratekit/core/review.py` | user | 3 file(s) | 834 | 11 | killed |
| `u329.P6_session_ack_wrong_family` | `src/cratekit/core/session_ack.py` | user | 5 file(s) | 362 | 69 | killed |
| `u23-round-8-independent.X15_save_drops_the_id3v1_trailer` | `src/cratekit/core/tags.py` | user | 3 file(s) | 853 | 1 | killed |
| `u310.G3_recorded_reject_honoured` | `src/cratekit/deletion/cli.py` | user | 4 file(s) | 393 | 3 | killed |
| `r706-a.A3_max_parts_four` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 5 | killed |
| `r706-b.B4_parts_reported_as_one` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 5 | killed |
| `r924.A6_last_call_unsaid` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 2 | killed |
| `u103-a.A7_offsets_in_the_key` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 2 | killed |
| `u57-recognition-and-items.M3_auth_family_loses_3001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 2 | killed |
| `r1295.M16_set_aside_one_word` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 221 | 4 | killed |
| `r682-a.M6_reason_counted_outside_state_guard` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u120.L2_date_added_ignored` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u57-recognition-and-items.C7_foreign_job_driven` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r924.C3_recording_drops_progress` | `src/cratekit/intake/cli_identify.py` | user | 3 file(s) | 119 | 2 | killed |
| `u103-b.C7_unwritten_note` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `r924.F4_sum_not_largest` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 11 | 1 | killed |
| `u104-b.F7_remove_on_exit` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 11 | killed |
| `u104-c.P6_address_is_stripped` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `r924.R1_bound_identifier_not_told` | `src/cratekit/intake/recognize.py` | user | 2 file(s) | 78 | 4 | killed |
| `u102-a.P1_root_boundary` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U3_empty_name` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G7_referenced_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u52-item-derivation.C1_can_list_always_true` | `src/cratekit/label/crawl.py` | user | 1 file(s) | 180 | 1 | killed |
| `r381.M5_migrate_any_identifier` | `src/cratekit/label/registry.py` | user | 5 file(s) | 429 | 4 | killed |
| `r704-a.S4_context_walk_one_level` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `u237.M6_substring_again` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 9 | killed |
| `u192.F7_queue_only_always` | `src/cratekit/modules/foreground.py` | user | 3 file(s) | 342 | 9 | killed |
| `r229.L10_a_name_matches_by_bare_suffix` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L1_a_third_suffices` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r229.L9_an_empty_list_is_a_legacy_record` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `u261.O2_account_drops_the_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 209 | 2 | killed |
| `u27-reports-round-1.L1_distinct_tracks` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u311.D3_tempo_never_read` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 2 | killed |
| `r221-a.E2_outcome_payload_drops_the_key` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 722 | 7 | killed |
| `r222-a.A7_no_record_is_a_late_floor` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 2 | killed |
| `r367.E1_a_failed_transfer_is_unread` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 282 | 15 | killed |
| `u311.A4_logged_takes_any_json` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 897 | 1 | killed |
| `u45-round-1.E2_publish_unconditional` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 7 | killed |
| `u48-author.P7_listing_message_reworded` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 1 | killed |
| `u311.A8_no_directory_matcher` | `src/cratekit/modules/tools/backup_record.py` | user | 4 file(s) | 317 | 1 | killed |
| `r154-b.B2_two_markers` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 2 | killed |
| `r338-a.B4_no_undo_archive` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-b.R7_restore_is_a_sync` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r367.G1_always_copy_the_restored_sidecar` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 6 | killed |
| `r388-a.M3_contents_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r388-b.M9_root_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `u44-author.A2_archive_collision_skips` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 245 | 3 | killed |
| `r187-b.B6_stamp_unchecked` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 1 | killed |
| `u43-author-light.E2_tempo_band_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 1 | killed |
| `u281.R5_no_reset` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 3 | killed |
| `u322.M17_deezer_gate_open_always` | `src/cratekit/tagging/published.py` | user | 6 file(s) | 392 | 3 | killed |
| `u260.F5_binder_builds_per_call` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 8 | killed |
| `u281.W2_searcher_ignores_the_handed_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 10 | killed |
| `u118-d.T1_old_playlist_split_row` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 202 | collection error | collect-error |
| `u133-b.T8_bpm` | `src/cratekit/templates/taxonomy.default.toml` | user | 2 file(s) | 894 | 3 | killed |
| `r675.G2_row_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 14 | killed |
| `r500-c.G14_located_skips_the_decode` | `src/cratekit/write/trees.py` | user | 10 file(s) | 1006 | 9 | killed |
| `u297.S1_a_root_outside_the_scenarios_own_directory` | `tests/behaviour/conftest.py` | user | 1 file(s) | 137 | 1 | killed |

## Row definitions

### `u297.B6_any_two_texts_the_same`

same_but_for: read any two texts as the same once a capture has a word of its own, so no difference in output, a file or a row is seen

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B6_any_two_texts_the_same`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 21 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_changed_cell_is_a_row_gone_and_a_row_come`
  - `tests/test_behaviour_compare.py::test_a_changed_line_of_standard_error_is_reported`
  - `tests/test_behaviour_compare.py::test_a_changed_text_file_shows_the_line_that_changed`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base0-changed0-said0]`
  - `tests/test_behaviour_compare.py::test_a_file_that_only_ends_like_a_sidecar_is_compared_as_a_file`
  - `tests/test_behaviour_compare.py::test_a_long_difference_is_cut_unless_asked_for_whole`
  - `tests/test_behaviour_compare.py::test_a_missing_final_newline_is_a_difference_and_says_how_the_texts_end`
  - `tests/test_behaviour_compare.py::test_a_word_that_stands_for_two_things_keeps_both_counterparts`
  - `tests/test_behaviour_compare.py::test_another_files_inode_in_that_row_is_a_difference`
  - `tests/test_behaviour_compare.py::test_one_changed_character_of_help_is_reported`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[8430 bytes, pid 3409-8431 bytes, pid 3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[lock_3409-lock_3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 13409-pid 13467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 34091-pid 34671-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 3409\n-pid 3467-False]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return re.fullmatch("".join(pattern), second, flags=re.DOTALL) is not None
```

New text:

```
    return True
```

### `u122.H5_units_only`

The hold applies to units only, the behaviour before the 2026-10-09 amendment

- File: `scripts/board.py`
- Source: `u122.json`, row `H5_units_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if current in UNDERWAY and node["unit"]:
```

### `u148.C3_no_count_skips`

a read with no count skips the check, the shape before the review

- File: `scripts/board.py`
- Source: `u148.json`, row `C3_no_count_skips`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options1-project_items-no count to check it against]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`

Old text:

```
    if not isinstance(total, int):
        # No count means no check, and a read nobody could check is not whole.
        raise Truncated(
```

New text:

```
    if not isinstance(total, int):
        return
        raise Truncated(
```

### `u148.W1_full_page_taken`

whole accepts a read of exactly the limit, a full page read as complete

- File: `scripts/board.py`
- Source: `u148.json`, row `W1_full_page_taken`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[300-330-issue read returned 300 rows]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315-316-the whole limit of 315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316-316-the whole limit of 316]`

Old text:

```
    if len(rows) >= READ_LIMIT:
```

New text:

```
    if len(rows) > READ_LIMIT:
```

### `u151.M2_issue_count_dropped`

an issue read shorter than the repository count is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `M2_issue_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options0-project_items-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options1-project_items-no count to check it against]`

Old text:

```
    short_of_count(seen, total, "project membership")

```

New text:

```
(empty)
```

### `u151.X3_status_refusal_dropped`

a project with no Status field is not refused

- File: `scripts/board.py`
- Source: `u151.json`, row `X3_status_refusal_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_read_whole_is_refused_by_name[<lambda>-Fail-no single select Status field]`

Old text:

```
    if not status or "options" not in status:
        raise Fail(
```

New text:

```
    if False:
        raise Fail(
```

### `u196.S4_missing_ledger_no_match`

search_residuals: drop the refusal of a missing ledger, so a search over a file never read says no match

- File: `scripts/board.py`
- Source: `u196.json`, row `S4_missing_ledger_no_match`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_missing_ledger_is_refused_never_read_as_no_match`

Old text:

```
    if not source.is_file():
        # A missing
```

New text:

```
    if False:
        # A missing
```

### `u203.M8_ellipsis_not_trailing`

_TRAILING: leave the ellipsis character out, so Brainstorm followed by one reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M8_ellipsis_not_trailing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`

Old text:

```
_TRAILING = ".?!;\u2026# \t"
```

New text:

```
_TRAILING = ".?!;# \t"
```

### `u313.B4_withdrawn_held`

cloud_state: read a Withdrawn card as held, so a released card is never offered

- File: `scripts/board.py`
- Source: `u313.json`, row `B4_withdrawn_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Started@2; ## Withdrawn@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Started@s+4; Withdrawn.@s+2]`

Old text:

```
    if heading == HEAD_WITHDRAWN:
```

New text:

```
    if heading == HEAD_WITHDRAWN and False:
```

### `r703-a.A1_classifier_reads_text`

classify_unavailable no longer holds NoFileLanded transient by type

- File: `src/cratekit/acquire/adapter.py`
- Source: `r703-a.json`, row `A1_classifier_reads_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`, `tests/test_provider_gate.py`
- Collected: 873 against a baseline of 873
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`

Old text:

```
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT

```

New text:

```
(empty)
```

### `u246.S1_adapter_asked_empty`

InvocationResult: an empty set of requested keys, so every result reads as a track nobody asked for

- File: `src/cratekit/acquire/adapter.py`
- Source: `u246.json`, row `S1_adapter_asked_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`, `tests/intake/test_pipeline.py`
- Collected: 260 against a baseline of 260
- Kills: 70 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`
  - `tests/test_acquire_workers.py::test_a_download_job_runs_pending_to_done_through_the_resume_path`
  - `tests/test_acquire_workers.py::test_a_lossless_landing_under_the_permissive_policy_is_not_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked[lossy-offer]`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked[lying-offer]`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_rate_limit_is_retried_under_backoff_and_then_lands`
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - ... and 55 more, see the JSON sidecar

Old text:

```
            asked = set(self.requested)
```

New text:

```
            asked = set()
```

### `u176.C3_page_error_is_rejected`

_pages: a page answering with an error is not read as a refused session

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C3_page_error_is_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 92 against a baseline of 92
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_page_refusing_the_session_or_answering_an_error_is_rejected[a-page-answering-with-an-error]`

Old text:

```
        if page.get("error"):
```

New text:

```
        if False:
```

### `u176.V12_strict_refuses_lossy`

_encoding: the strict policy takes a lossy format when no lossless one is offered

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V12_strict_refuses_lossy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_strict_refuses_a_release_offered_only_lossy`

Old text:

```
    if not decision.permitted:
```

New text:

```
    if False:
```

### `u176.V7_record_version`

fetched: a record of another version is read, so its purchases are trusted under a shape this build does not know

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V7_record_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_an_unreadable_record_refuses_rather_than_offering_everything_again[newer-version]`

Old text:

```
    if raw.get("version") != RECORD_VERSION:
```

New text:

```
    if False:
```

### `u177.B5_registry_unread_empty`

registry: read an unreadable registry as empty, so every purchase stages untagged with a clean plan

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B5_registry_unread_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_an_unreadable_registry_refuses_the_plan_rather_than_staging_untagged[{"version": 99, "labels": {}}]`
  - `tests/test_bandcamp_labels.py::test_an_unreadable_registry_refuses_the_plan_rather_than_staging_untagged[{not json]`

Old text:

```
    del origin
    return labels.RegistryStore().load()

```

New text:

```
    del origin
    try:
        return labels.RegistryStore().load()
    except CratekitError:
        return labels.empty()

```

### `u205.C11_collection_404_read_as_absence`

app client: a 404 on the ISRC collection, which says the address moved, is read as no track and remembered by sync pair as a miss

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C11_collection_404_read_as_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`

Old text:

```
            "tracks", {"filter[isrc]": str(isrc), "include": INCLUDE}, what, absence=False
```

New text:

```
            "tracks", {"filter[isrc]": str(isrc), "include": INCLUDE}, what, absence=True
```

### `u205.C8_availability_ignored`

app client: a track the answer says does not stream is read as streaming, so _among offers it as a candidate

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C8_availability_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_the_answer_is_read_into_the_shape_the_choosing_logic_reads`

Old text:

```
    return any(str(mode).strip().upper() == "STREAM" for mode in said)
```

New text:

```
    return True
```

### `r289-c.B2r_reclaim_reports_a_failure_as_a_removal`

Report a directory that could not be removed as one that was

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B2r_reclaim_reports_a_failure_as_a_removal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 367 against a baseline of 367
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)
```

New text:

```
    try:
        directory.rmdir()
    except OSError:
        pass
    removed.append(directory)
```

### `r668-a.M6_no_list_check_on_resume`

a list named beside --job is never compared with the frozen one, so a different list is silently ignored and the job driven

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M6_no_list_check_on_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_different_list_named_beside_the_job_is_refused_and_nothing_is_fetched`
  - `tests/test_acquire_workers.py::test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name`
  - `tests/test_acquire_workers.py::test_a_refused_list_leaves_a_dead_drivers_claim_for_the_resume_to_reconcile`

Old text:

```
            _same_list_or_refuse(
                ctx.args.list, jobs.get(store, ctx.args.job), ctx.entry.handler_key
            )

```

New text:

```
            pass

```

### `u169.A4_no_declined_warning`

drive_queued: add no warning for the skipped tracks

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A4_no_declined_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`

Old text:

```
    warnings = (*warnings, *declined_warnings(store, job))
```

New text:

```
    warnings = tuple(warnings)
```

### `u42-author.P2_relative_path_leaks_the_root`

Report the absolute path, putting a real directory layout in the payload (R1)

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P2_relative_path_leaks_the_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 25 against a baseline of 25
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[a-lossless-file-wearing-the-marker]`
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[an-mp4-container-is-undecided]`
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[no-marker-text-strict-still-fires]`
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[permissive-reports-only-the-unmarked]`
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[strict-reports-every-lossy-file-marked-or-not]`

Old text:

```
        where = str(path.relative_to(root))
```

New text:

```
        where = str(path)
```

### `u54-acquisition-worker.G15_no_marker_text`

Commit a lossy landing unmarked when the configuration names no marker text

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G15_no_marker_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`

Old text:

```
    if not text:
        raise refuse(
            "lossy-refused",
            f"{landed.name} landed lossy under a policy that permits lossy only "
            f"when marked, and the configuration names no marker text, so it "
            f"cannot be marked and is not kept",
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=("acquire.cli",),
            detail={"path": str(landed)},
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G2_missing_identifier`

Queue a provider list whose rows carry no identifier, dropping the by-position refusal

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G2_missing_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this list carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing can ask the "
            f"provider for them",
            "fetch the list from the provider again so every row carries its id",
            positions=missing,
        )

```

New text:

```
(empty)
```

### `u80.F12_open_searched_again`

An open question is not read from the queue, so it is searched again

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F12_open_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_list_whose_rows_are_all_settled_needs_no_binary`
  - `tests/test_acquire_fallback.py::test_a_second_run_searches_nothing_and_offers_nothing_twice`
  - `tests/test_acquire_fallback.py::test_an_outage_names_every_row_already_offered`

Old text:

```
    if held.verdict is None:
        return Proposal(
            wanted,
            WAITING,
```

New text:

```
    if held.verdict is None:
        return None
        return Proposal(
            wanted,
            WAITING,
```

### `u80.F6_ignore_errors_back`

The subprocess is run with the source system's ignore errors flag again

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F6_ignore_errors_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_the_argv_searches_flat_with_the_platform_prefix_and_no_ignore_errors`

Old text:

```
            "--no-warnings",
            "--print",
```

New text:

```
            "--no-warnings",
            "--ignore-errors",
            "--print",
```

### `r289-b.C2_fallback_resume_call_site`

Drop the sweep on the fallback fetch resume path

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r289-b.json`, row `C2_fallback_resume_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_this_verb_sweeps_the_staging_tree_it_shares_with_the_download_verb`

Old text:

```
            acquire_cli.sweep_staging(
                Path(jobs.frozen_config(job).paths.download_staging), store
            )

```

New text:

```
(empty)
```

### `u81-fetch-a.W1_strict_not_refused`

The strict policy refusal before the download is removed, so a lossy upload is fetched under strict

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W1_strict_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_strict_policy_refuses_that_item_before_anything_downloads`

Old text:

```
    if not decision.permitted:
        raise refuse(
            "lossy-refused",
```

New text:

```
    if False:
        raise refuse(
            "lossy-refused",
```

### `u81-fetch-b.Q3_empty_queue`

A list with nothing accepted queues a job anyway instead of reporting a no-op

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `Q3_empty_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_acquire_fallback_fetch.py::test_a_row_with_a_provider_route_is_not_fetched_lossy`
  - `tests/test_acquire_fallback_fetch.py::test_an_acceptance_naming_no_upload_of_several_is_not_queued`
  - `tests/test_acquire_fallback_fetch.py::test_nothing_accepted_queues_nothing_and_says_so`

Old text:

```
    if not rows:
        return ctx.envelope(
```

New text:

```
    if False:
        return ctx.envelope(
```

### `r1016.M4_date_added_not_moved`

The listing's created is no longer moved onto the playlist as dateAdded, so user_date_added is lost where the client's method kept it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M4_date_added_not_moved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 793 against a baseline of 793
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`

Old text:

```
            playlist["dateAdded"] = item["created"]

```

New text:

```
            item["created"]

```

### `r878-a.A11_count_alone_is_a_page`

paginate_cursor: refuse a response that declares a count but carries no items, so an empty folder refuses

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A11_count_alone_is_a_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_response_with_a_count_and_no_items_is_an_empty_listing`

Old text:

```
                not isinstance(response.get("items"), list) and _declared(response) is None
```

New text:

```
                not isinstance(response.get("items"), list)
```

### `r878-a.A8_no_cursor_ends`

paginate_cursor: a response with no cursor no longer ends the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A8_no_cursor_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 16 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_folder_holding_a_folder_keeps_only_its_playlists`
  - `tests/test_adapter_listing.py::test_a_folder_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_a_folder_served_on_two_pages_is_returned_once`
  - `tests/test_adapter_listing.py::test_a_folders_playlists_are_walked_by_cursor_through_the_folders_own_parser`
  - `tests/test_adapter_listing.py::test_a_parse_that_fails_transiently_is_retried_alone_without_refetching_the_page`
  - `tests/test_adapter_listing.py::test_a_response_with_no_cursor_ends_the_walk`
  - `tests/test_adapter_listing.py::test_a_short_walk_over_a_mixed_root_still_refuses`
  - `tests/test_adapter_listing.py::test_a_transient_failure_retries_the_same_cursor_and_not_the_first_page`
  - `tests/test_adapter_listing.py::test_a_walk_that_collects_fewer_than_the_declared_count_refuses`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_adapter_listing.py::test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset`
  - `tests/test_adapter_listing.py::test_the_latest_declared_count_is_the_one_checked`
  - `tests/test_adapter_listing.py::test_the_root_count_covers_playlists_too_so_folders_are_kept_after_counting`
  - `tests/test_adapter_listing.py::test_the_root_folders_are_walked_by_cursor_past_an_endpoint_that_ignores_offset`
  - `tests/test_label_playlists.py::test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if not page or not following:
```

New text:

```
        if not page:
```

### `r887-a.K2_playlists_kept_unfiltered`

listing.folder_playlists: keep nothing out, so a nested folder is parsed as a playlist

- File: `src/cratekit/acquire/listing.py`
- Source: `r887-a.json`, row `K2_playlists_kept_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_folder_holding_a_folder_keeps_only_its_playlists`

Old text:

```
        keep=_item_type("PLAYLIST"),
```

New text:

```
        keep=None,
```

### `u65.B4_account_playlists_back_to_the_short_page`

the sync all listing ends on a short page, silently skipping playlists

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B4_account_playlists_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`

Old text:

```
    "account_playlists": StopRule.EMPTY_PAGE,
```

New text:

```
    "account_playlists": StopRule.SHORT_PAGE,
```

### `u65.D5_the_favourites_budget_is_tightened_onto_real_data`

a budget that can fire on a real account, which turns a correctness fix into an outage

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `D5_the_favourites_budget_is_tightened_onto_real_data`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`
- Collected: 85 against a baseline of 85
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_every_budget_clears_the_largest_collection_this_project_has_measured`

Old text:

```
    "favorite_tracks": 200,  # reaches 19,900 tracks. Largest measured: 197.
```

New text:

```
    "favorite_tracks": 3,  # reaches 19,900 tracks. Largest measured: 197.
```

### `u70.E3_hearts_declared_total`

Existing: the favourites walk ends on a page shape instead of the declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `u70.json`, row `E3_hearts_declared_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_listing.py`
- Collected: 259 against a baseline of 259
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_the_declared_count_is_retried_on_the_same_ladder_every_page_is`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`

Old text:

```
    kwargs.setdefault("declared_total", _declared_count(favorites, "get_tracks_count"))
```

New text:

```
    kwargs.setdefault("declared_total", None)
```

### `u213.M1_first_group_is_the_title`

split_version: drop the first group rule, so a title written wholly in brackets walks off whole and the row names no title

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M1_first_group_is_the_title`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 13 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[  [Premade Sandwiches]  -expected2]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Premade Sandwiches)-expected1]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Love) (Remix)-expected12]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Or Without You)-expected9]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You)-expected10]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(feat. Mira)-expected13]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (Live)-expected3]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches]-expected0]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[With You]-expected8]`

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
            remaining = inside
            break
```

New text:

```
        if False:
            remaining = inside
            break
```

### `u261.H6_app_not_asked_again`

session_for: hand a reuse the held absence of an app client, so app values recorded or lost since the open are not seen and no lost value is noted

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H6_app_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`
- Collected: 96 against a baseline of 96
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_a_lost_app_value_is_noted_on_every_resolve_that_falls_back`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`

Old text:

```
            if current.app is None:
```

New text:

```
            if False:
```

### `r703-a.V3_cause_not_passed`

fetch hands landed_file no cause, the eleventh sitting's plain no file answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V3_cause_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_failure_message_with_no_exception_is_the_cause`
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`
  - `tests/test_adapter_contract.py::test_a_rate_limited_album_read_reaches_the_item_cause_by_name`
  - `tests/test_adapter_contract.py::test_an_error_the_tool_logs_from_its_except_is_the_cause`

Old text:

```
            cause=cause,
        )
```

New text:

```
            cause=None,
        )
```

### `r703-b.R1_status_path_dropped`

is_rate_limit reads the client's class only, so a bare 429 reads as an ordinary answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `R1_status_path_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_bare_http_429_reads_as_a_rate_limit`

Old text:

```
    return isinstance(exc, TooManyRequests) or status_of(exc) in RATE_LIMIT_STATUSES
```

New text:

```
    return isinstance(exc, TooManyRequests)
```

### `u47-author.CODEC_mp3_reads_as_lossless`

Flip MP3 to lossless in the container table, a realistic nearby value rather than a deletion

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_mp3_reads_as_lossless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_codec_table_answers_for_every_container_it_declares`

Old text:

```
    "MP3": False,
```

New text:

```
    "MP3": True,
```

### `u47-author.R195_verify_skips_the_mapping`

Verify a hand-named pair rather than everything pushed, which is the source system's guard that watched two keys while the tool had more

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R195_verify_skips_the_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_an_injected_session_still_has_this_runs_settings_pushed_and_verified`
  - `tests/test_adapter_contract.py::test_applying_settings_writes_them_in_memory_and_saves_nothing`
  - `tests/test_adapter_contract.py::test_verification_covers_the_ffmpeg_key_by_it_being_pushed`

Old text:

```
    applied = {key: getattr(target, key, _ABSENT) for key in expected}
```

New text:

```
    applied = {key: getattr(target, key, _ABSENT) for key in ("quality_audio",)}
```

### `u47-author.R197_drop_progress`

Drop progress from the downloader construction, half of the pair whose absence swallowed the failure

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_drop_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`

Old text:

```
            progress=progress,

```

New text:

```
(empty)
```

### `u254-m08.M08_never_append`

mark_applied: rewrite the whole ledger on every mark that misses the cache, the square this card ends

- File: `src/cratekit/adopt/apply.py`
- Source: `u254-m08.json`, row `M08_never_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_journal_this_process_never_wrote_appends`

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if False:
                config.append_durable_bytes(line, path)
```

### `u254.M09_any_line_torn`

_read_journal: read a damaged line anywhere as torn and stop, so the records after it are lost

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M09_any_line_torn`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a damaged line before the last]`

Old text:

```
            if index == len(body) - 1 and whole:
```

New text:

```
            if whole:
```

### `u254.M17_document_at_journal_schema`

_read_document: read a whole document that claims schema 2

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M17_document_at_journal_schema`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_document_at_a_schema_no_build_wrote_whole_refuses[at-the-journal-schema]`

Old text:

```
    if version > DOCUMENT_SCHEMA_VERSION:
```

New text:

```
    if version > SCHEMA_VERSION:
```

### `r1991.A4_apply_records_nothing`

adopt apply: hand the writer no record_as, so adoption records nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r1991.json`, row `A4_apply_records_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_outside_root.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_filing.py`, `tests/test_organize.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_second_genre_guards_counts.py`
- Collected: 521 against a baseline of 521
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`

Old text:

```
            record_as=planned_destinations(plan, declared),

```

New text:

```
(empty)
```

### `u132.W2_coded_note`

A skip over an undeclared class carries favorites-skipped, not its cause code

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W2_coded_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 447 against a baseline of 447
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_genre_favorites.py::test_the_undeclared_note_states_the_version_the_skip_saw`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
    if skipped and cause == genre_favorites.CLASS_UNDECLARED:

```

New text:

```
    if False:

```

### `u27-adopt-apply-author.S4_workflow_is_not_the_verb`

Record the session under a name that is not this verb's

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S4_workflow_is_not_the_verb`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 17 against a baseline of 17
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

### `u55-round-2.R8_census_prefix_map`

The census drops the configured volume rewrites, so an older volume name resolves nowhere

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-round-2.json`, row `R8_census_prefix_map`
- Moved: the census's scan_rows arguments were joined onto one line by the formatter; the prefix map is emptied as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`

Old text:

```
            rows, declared, root=cfg.library.root, prefix_map=collection.prefix_rules(cfg)
```

New text:

```
            rows, declared, root=cfg.library.root, prefix_map=()
```

### `u55-collection-reader.R1_read_only_open`

The reader asks for a WRITE intent open. The single most important row in this table.

- File: `src/cratekit/adopt/collection.py`
- Source: `u55-collection-reader.json`, row `R1_read_only_open`
- Moved: the read only open's arguments were joined onto one line by the formatter; require_closed is flipped as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_this_module_holds_no_write_path_at_all`

Old text:

```
rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
```

New text:

```
rb_writer.live_db_path(cfg), require_closed=True, check_app_version=False, cfg=cfg
```

### `r780-a.A3_verdict_ignored_in_tree_path`

a keep-separate verdict on the bucket asked is ignored, so a removal is planned inside a folder a person refused

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A3_verdict_ignored_in_tree_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`
  - `tests/test_adopt_move.py::test_a_verdict_withheld_double_is_left_and_listed_under_its_own_reason`

Old text:

```
    elif bucket in refused:
        reason = LEFT_VERDICT

```

New text:

```
(empty)
```

### `r797-d.M8_again_an_unread_file_is_no_reading`

M8 measured again after the second review moved its condition: say a file the census could not read is left because its genre names another bucket

- File: `src/cratekit/adopt/move.py`
- Source: `r797-d.json`, row `M8_again_an_unread_file_is_no_reading`
- Moved: the former place listing now hands its fallback reason to the shared ladder _listed; an unread file never reads as no reading, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread-genre-names-the-old-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread]`

Old text:

```
    otherwise = LEFT_NO_READING if genre_names_it else LEFT_FORMER
```

New text:

```
    otherwise = LEFT_NO_READING if False else LEFT_FORMER
```

### `u133-b-rerun.E2_former_place_only`

Existing guard sample: a track sitting only in a former place is never recognised as one

- File: `src/cratekit/adopt/move.py`
- Source: `u133-b-rerun.json`, row `E2_former_place_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 215 against a baseline of 215
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[another-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[no-genre]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread-genre-names-the-old-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[unread]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left[holder]`
  - `tests/test_adopt_former_place.py::test_a_verdict_on_the_bucket_the_genre_names_is_the_reason_a_track_there_is_left[promoted]`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_digest_moves_when_a_track_turns_up_in_the_old_playlist`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`

Old text:

```
    return bool(held) and set(held) <= former

```

New text:

```
    return False

```

### `r780-b.B4_gone_named_once_per_move`

a track gone from the collection is named once per move it carried, so the report lists it twice

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B4_gone_named_once_per_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_one_track_carries_a_move_in_each_bucket_it_doubles_in`

Old text:

```
    return tuple(todo), tuple(sorted(gone))
```

New text:

```
    return tuple(todo), tuple(
        sorted(move.content_id for move in approved if move.content_id in gone)
    )
```

### `r788-c.L2_removed_tag_files`

vox_tagged: an association rekordbox removed is read as a tag, so a track a person untagged is filed

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L2_removed_tag_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_tag_a_person_took_off_is_not_a_tag`
  - `tests/test_adopt_vocals.py::test_an_association_that_cannot_say_whether_it_was_removed_refuses`

Old text:

```
        if not _removed(song, "My Tag association")
```

New text:

```
        if True
```

### `u118-b.P2_recorded_under_split`

recorded_under answers a split place under the declaring bucket, so a renamed holder playlist is not recognised

- File: `src/cratekit/adopt/placements.py`
- Source: `u118-b.json`, row `P2_recorded_under_split`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_place_is_found_as_the_r_and_b_place_it_is`

Old text:

```
        return recorded_under(declared, split.bucket, split.sub)
```

New text:

```
        return bucket_id, sub_id
```

### `r722.P5_entry_drops_unreadable`

The plan entry does not carry the unreadable flag

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P5_entry_drops_unreadable`
- Moved: the PlanEntry is now built before _destined routes it, four spaces less indented; the unreadable flag is dropped from it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 651 against a baseline of 651
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
            energy=track.energy,
            energy_unreadable=track.energy_unreadable,
```

New text:

```
            energy=track.energy,
```

### `r731-a.M07_withheld_entry_loses_its_bucket`

a withheld entry's bucket is blanked, so its identifier and its review row lose it

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M07_withheld_entry_loses_its_bucket`
- Moved: the entry a competing place withholds now keeps its bucket in _destined; the mutation blanks it there, as the old condition did for every withheld entry
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_genre_answered_later_is_withheld_over_the_place_the_track_holds`
  - `tests/test_adopt_placements.py::test_a_track_holding_a_place_is_withheld_only_where_it_competes[withheld-keeps-its-identifier]`
  - `tests/test_adopt_placements.py::test_a_track_in_one_band_whose_file_reads_another_is_withheld_and_listed`
  - `tests/test_adopt_placements.py::test_a_track_the_plan_withheld_is_not_a_stranger_in_its_own_folder`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE

```

New text:

```
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE
        bucket = "" if withheld_by else bucket

```

### `r788-a.P5_withheld_gains`

vocal_place: a withheld track is added to its vocal sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P5_withheld_gains`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_track_withheld_over_another_band_stays_withheld_and_gains_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_the_counts_add_up_to_the_tagged_tracks_of_the_census`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if disposition is Disposition.WITHHELD:
        return VOCAL_WITHHELD, sub
```

New text:

```
    if False:
        return VOCAL_WITHHELD, sub
```

### `r788-b.P9_unplaced_entry_gains`

vocal_place: only an empty bucket is no bucket, so an entry the plan does not place gains a vocal sub when a caller hands its bucket in

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P9_unplaced_entry_gains`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_an_entry_the_plan_does_not_place_has_no_bucket_whatever_bucket_it_is_handed`

Old text:

```
    if not bucket or disposition not in (Disposition.ROUTE, Disposition.WITHHELD):
        return VOCAL_NO_BUCKET, ""
```

New text:

```
    if not bucket:
        return VOCAL_NO_BUCKET, ""
```

### `u23-round-8-independent.A1_at_risk_always_true`

Nothing is ever at risk, so _settled_or_refused can never refuse

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A1_at_risk_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    return True

```

### `u23-round-8-independent.C1_shape2_bypasses_the_check`

Shape 2, both addresses agreeing, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `C1_shape2_bypasses_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
        if by_identity is by_path:
            return _settled_or_refused(
                by_identity,
                resolved,
                identity=identity,
                path_text=path_text,
                keep_path=True,
                written=written,
                look=look,
                current=current,
                size_here=size_here,
            )

```

New text:

```
        if by_identity is by_path:
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=True
            )

```

### `u23-round-8-independent.F4_byte_search_reads_before_it_filters`

Round 7 order restored: the whole-file read runs before the filters that empty the list

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `F4_byte_search_reads_before_it_filters`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None

```

New text:

```
    looked = look()
    if looked.outcome is not ByteRead.ANSWERED:
        return None
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
    if not vacant or size_here is None:
        return None
    same_size = [record for record in vacant if record.size == size_here]
    if not same_size:
        return None

```

### `r722.S1_unreadable_folded`

The census reads a failed read as a file with no reading

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S1_unreadable_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
    except (tags.TagReadFailed, OSError):
        return None, True
```

New text:

```
    except (tags.TagReadFailed, OSError):
        return None, False
```

### `u23-round-8-independent.X8_classify_drops_the_too_coarse_test`

A generic genre is routed rather than asked about

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X8_classify_drops_the_too_coarse_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_genre_the_taxonomy_calls_too_coarse_gets_a_disposition`

Old text:

```
    if not value or declared.is_too_coarse_as_source(value):
```

New text:

```
    if not value:
```

### `u956.O3_confine_default_off`

scan_rows: confine only when asked, so every adoption caller routes a row outside the root

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O3_confine_default_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 685 against a baseline of 685
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_a_row_mapped_outside_the_root_is_excluded_and_keeps_its_path`
  - `tests/test_adopt_outside_root.py::test_adopt_move_reads_the_same_disposition`
  - `tests/test_adopt_outside_root.py::test_adopt_scan_counts_each_sampler_row_outside_the_root`
  - `tests/test_adopt_outside_root.py::test_an_apply_over_sampler_rows_files_the_rest_and_records_no_sampler_row`
  - `tests/test_adopt_outside_root.py::test_an_outside_row_is_never_probed`
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`
  - `tests/test_adopt_outside_root.py::test_the_plan_counts_and_names_every_row_it_leaves_outside`

Old text:

```
    confine_to_root: bool = True,
```

New text:

```
    confine_to_root: bool = False,
```

### `u55-collection-reader.R11_scan_item_ids`

The scan enqueues with no items at all, which is the R-203 shape

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u55-collection-reader.json`, row `R11_scan_item_ids`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`

Old text:

```
            item_ids=live,
```

New text:

```
            item_ids=(),
```

### `u223.M10_report_wrong_name`

staged_report: read the report under a name staged_path never writes

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M10_report_wrong_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
```

New text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / f"{item.ordinal}.json"
```

### `u223.M4_subdir_unlinked`

staged_path: unlink a subdirectory entry instead of removing its tree

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M4_subdir_unlinked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
```

New text:

```
            if False:
                shutil.rmtree(entry)
```

### `u90-a.A1_lower_bound_strict`

The range guard's lower bound made strict, so a cut of 0 is refused

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A1_lower_bound_strict`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if not VOCAL_SCORE_MIN < cut <= VOCAL_SCORE_MAX:
```

### `u90-b.B3_note_reworded`

The hand cut's note stops saying set by hand

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B3_note_reworded`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`

Old text:

```
note=f"set by hand on {today}"
```

New text:

```
note=f"entered on {today}"
```

### `u94-a.S1_floor_dropped`

analyze_calibrate: never refuse a sample below the fit floor, so --sample 3 measures three tracks and fails after the walk instead of before it

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S1_floor_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_refusal_known_before_the_walk_does_not_make_the_walk`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra0]`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra1]`

Old text:

```
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
```

New text:

```
    if sample < 0:
        return _calibrate_refusal(
```

### `u94-b.W1_after_walk_refusal_dropped`

analyze_calibrate: ask what the walk left out and fit anyway without the flag, so the omission is known and ignored

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W1_after_walk_refusal_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        if partial is not None and not accepted:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
```

New text:

```
        if False:
            return _calibrate_refusal(ctx, _partial_refused(partial), summary, omitted)
```

### `u94-c.N2_stride_is_a_fixed_step`

stride_sample: a fixed step of len // count, which stops short of the tail whenever the division has a remainder

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N2_stride_is_a_fixed_step`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_stride_sample_is_even_ordered_and_reaches_the_tail`

Old text:

```
    return [items[index * total // count] for index in range(count)]
```

New text:

```
    return [items[index * (total // count)] for index in range(count)]
```

### `u192.A1_run_queue_only_ignored`

analyze_run: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A1_run_queue_only_ignored`
- Moved: Anchored where u325-replay-after.json replayed it: Same branch in analyze_run; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 15 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_an_older_build_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`

Old text:

```
        if foreground.queue_only(ctx.args):
            return ctx.envelope(data=jobs.reported(store, job))
```

New text:

```
        if False:
            return ctx.envelope(data=jobs.reported(store, job))
```

### `u241.M13_vocal_model_not_kept_back`

_open_ahead: the driver's vocal model is not kept back from the light pool's budget

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M13_vocal_model_not_kept_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`

Old text:

```
        reserve += vocals.VOCAL_WORKER_BYTES
    return ahead.open_session(
```

New text:

```
        pass
    return ahead.open_session(
```

### `u306.A7_calibrate_handler`

analysis.cli.analyze_calibrate: the handler answers the validate verb's envelope instead of running the calibrate body

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A7_calibrate_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 44 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[nan]`
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_refuses_with_the_library_away`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`
  - `tests/test_analysis_workers.py::test_a_recursive_run_at_the_root_writes_a_calibration_with_the_sample_note`
  - `tests/test_analysis_workers.py::test_a_recursive_walk_of_one_genre_is_still_one_genre`
  - ... and 29 more, see the JSON sidecar

Old text:

```
    return calibrate.analyze_calibrate(ctx)
```

New text:

```
    return analyze_validate(ctx)
```

### `u343.M24_twin_recovery_off`

_finalized_twin: never find the renamed twin, so a job an older build left half renamed refuses its finished item as missing

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M24_twin_recovery_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_rename_intent_for_another_item_or_a_gone_target_is_not_a_twin`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`
  - `tests/test_analysis_workers.py::test_an_item_an_older_build_renamed_before_its_row_moved_resumes_as_finished`

Old text:

```
    if target is None or not target.is_file():
        return None
    return target
```

New text:

```
    return None
```

### `u94-c.N6_default_sample_halved`

DEFAULT_CALIBRATION_SAMPLE: halve the coefficient, 500 to 250

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N6_default_sample_halved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_default_sample_is_what_the_parser_hands_the_verb`

Old text:

```
DEFAULT_CALIBRATION_SAMPLE = 500
```

New text:

```
DEFAULT_CALIBRATION_SAMPLE = 250
```

### `u264.M6_any_release_measured`

_measured_zero_rule: treat a release not measured as measured, with the 1.0 rule

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M6_any_release_measured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[0.11.0rc1-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[0.12.0.dev0-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[0.9.2-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.0.0rc0-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.0.1-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.1.0-None]`
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[2.0.0-None]`

Old text:

```
    return _MEASURED_MIX.get(version)
```

New text:

```
    return _MEASURED_MIX.get(version, True)
```

### `u343.M22_record_keeps_key_buckets`

_HEAD_AGREEMENT: carry the detector's key buckets in the run's answer again

- File: `src/cratekit/analysis/detect.py`
- Source: `u343.json`, row `M22_record_keeps_key_buckets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_stages.py`, `tests/test_head_agreement.py`
- Collected: 92 against a baseline of 92
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_stages.py::test_the_recorded_agreement_carries_the_tempo_and_no_key`
  - `tests/test_head_agreement.py::test_the_recorded_shape_is_the_shape_the_measurement_prints`

Old text:

```
    "within_one": 226,
}
```

New text:

```
    "within_one": 226,
    "key": {"equal": 158, "differs": 141},
}
```

### `u327.A10_file_missing_named`

_resolved: answer a missing file as present, so it is named unreadable rather than missing

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A10_file_missing_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_gone_before_the_plan_is_left_and_named`

Old text:

```
    return (path, "") if present else (path, FILE_MISSING)
```

New text:

```
    return (path, "")
```

### `u327.A1_key_equal_by_wheel`

adopted: compare the written key to rekordbox's as text, so an unpadded spelling of the same key is rewritten

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A1_key_equal_by_wheel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 161 against a baseline of 161
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_head_takes_rekordbox_s_key_and_tempo_and_no_other_byte[unpadded-equal-stands]`

Old text:

```
    if key is not None and parse_camelot(written_key) != parse_camelot(key):
```

New text:

```
    if key is not None and written_key != key:
```

### `u342.E3_stale_plan_refuses`

assert_plan_unchanged (existing, sample): take any plan on the write handle as the approved one

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `E3_stale_plan_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_plan_that_moves_on_the_write_handle_refuses_before_any_file`

Old text:

```
    if again.digest == approved.digest:
```

New text:

```
    if True:
```

### `u342.P6_stamped_not_left`

LEFT: count stamped among the rows left alone

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P6_stamped_not_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`

Old text:

```
    outcome for outcome in OUTCOMES if outcome not in (*WRITING, AGREE)
```

New text:

```
    outcome for outcome in OUTCOMES if outcome not in (ADOPT, AGREE)
```

### `u342.C4_written_says_no_rename`

_written: say the file names keep their old head again

- File: `src/cratekit/analysis/head_adopt_cli.py`
- Source: `u342.json`, row `C4_written_says_no_rename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`

Old text:

```
f"other column; no file is renamed; a restore of session "
```

New text:

```
f"other column; the file names keep their old head; a restore of session "
```

### `u275.M6_unknown_length_shorter`

_shape_of: bound an unknown length at fifty times the slowest rate, so not knowing plans wider than knowing

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M6_unknown_length_shorter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 553 against a baseline of 553
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_whose_length_is_unknown_is_still_planned_narrower`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`

Old text:

```
            seconds = target.stat().st_size / SLOWEST_BYTES_PER_SECOND
```

New text:

```
            seconds = target.stat().st_size / (SLOWEST_BYTES_PER_SECOND * 50)
```

### `sitting3.G11_tail_dropped`

Drop a short tail instead of folding it, so its frames are never scored

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G11_tail_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces[a-short-tail-is-folded]`

Old text:

```
    merged = np.concatenate([slices[-2], last], axis=-1)
    return [*slices[:-2], merged]

```

New text:

```
    return slices[:-1]

```

### `sitting3.G7_chatter_on_stdout`

Let the wrapper print onto the JSON envelope's stream

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G7_chatter_on_stdout`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

New text:

```
    with contextlib.nullcontext():
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

### `u58-workers-and-wav.W3_undecodable_scored`

Drop the guard that reports a failed decode instead of scoring it

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W3_undecodable_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`

Old text:

```
    if samples is None:
        return _inactive(result, REASON_AUDIO_UNDECODABLE)

```

New text:

```
(empty)
```

### `u92-author.G4_cap_doubled`

Double the cap to 500 mebibytes, which still refuses something and refuses it late

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G4_cap_doubled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 230 against a baseline of 230
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 500 * 1024 * 1024
```

### `r221-a.S3_flag_reads_a_key_nothing_freezes`

Read the rehearsal flag under a name the build does not freeze, so every job reads as a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `S3_flag_reads_a_key_nothing_freezes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_says_which_kind_of_run_it_was[under-a-rehearsal-says-so]`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return bool((job.payload or {}).get(DRY_RUN))
```

New text:

```
    return bool((job.payload or {}).get("rehearsal"))
```

### `r221-b.M4_steps_replaced_not_joined`

The sentence replaces the failure's own steps rather than joining them, so the thing a person has to do to fix it is gone

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M4_steps_replaced_not_joined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`

Old text:

```
                steps=(*cause.remediation.steps, rehearsal_warning()["message"]),
```

New text:

```
                steps=(rehearsal_warning()["message"],),
```

### `r222-b.B3_any_library_is_a_twin`

Drop the library comparison, so a job copying another library is reported as this one's backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B3_any_library_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_job_that_is_not_this_backup_does_not_stand_in_for_it[another-library]`

Old text:

```
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
```

New text:

```
        if job.handler_key != handler_key:
```

### `r290-author.S04_backup_call_removed`

Remove the one jobs.raise_for_state call from backup/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `S04_backup_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 11 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r757-c1.S1_resume_drops_the_full_flag`

backup_argv: never emit --full, so a resumed full job's command line is a fast one

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S1_resume_drops_the_full_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
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

### `u45-round-1.A4_state_collapsed_to_known`

Report every portion as known, so never-recorded and recorded-in-the-future both read as a current backup

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `A4_state_collapsed_to_known`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
            "state": str(entry.state),
            "age_seconds"
```

New text:

```
            "state": "known",
            "age_seconds"
```

### `u45-round-1.Q2_resume_always_rehearses`

Always emit --dry-run, the other direction, so a real backup respawns as a rehearsal that copies nothing

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q2_resume_always_rehearses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    argv.append("--dry-run")
```

### `u45-round-1.W5_publishing_switched_off`

Pass publish=False, so a successful backup records no age and the write session still sees never-recorded

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W5_publishing_switched_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 8 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
    outcome = backup.run_backup(cfg, plan, runner=runner, now=now, dry_run=dry_run)
```

New text:

```
    outcome = backup.run_backup(
        cfg, plan, runner=runner, now=now, dry_run=dry_run, publish=False
    )
```

### `u50-author.W5_unknown_portion_unchecked`

Let an undeclared item name raise out of the coercion rather than refusing by name

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W5_unknown_portion_unchecked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`

Old text:

```
        raise refuse(
            "internal-error",
            f"this job's item is {named!r}, which is not a backup portion this "
            f"build declares. The portions are {', '.join(declared)}",
```

New text:

```
        raise refuse(
            "internal-error",
            "the item could not be read",
```

### `r924.D1_json_gets_progress`

The dispatcher hands the progress writer to JSON output too, so standard error carries progress under --output json

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D1_json_gets_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`

Old text:

```
        if not as_json:
            context.progress = _progress_to(stderr)
```

New text:

```
        if True:
            context.progress = _progress_to(stderr)
```

### `u55-collection-reader.R30_scan_handler_bound`

adopt.scan loses its worker, which is the state R-203 records

- File: `src/cratekit/cli/handlers.py`
- Source: `u55-collection-reader.json`, row `R30_scan_handler_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`
- Collected: 243 against a baseline of 243
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_both_adopt_keys_resolve_to_a_worker`
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`

Old text:

```
    "adopt.scan": "cratekit.adopt.scan_cli:handle",
```

New text:

```
(empty)
```

### `u27-adopt-apply-author.R1_marker_restored`

Put planned_in back on the entry, so the conformance suite stops driving the landed verb

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u27-adopt-apply-author.json`, row `R1_marker_restored`
- Moved: U328 moved adopt.move's entry to the modules part, which does not import ADOPT_APPLY_CLI_UNIT, so the row as written ended in a NameError and broke collection for another reason; the same marker is put back on the same entry, by the constant's value, U27
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_adoption.py`, `tests/test_pending_units.py`
- Collected: 1732 against a baseline of 1735
- Kills: 3 (collect-error)
- Note: collection changed: 1732 collected against a baseline of 1735. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adoption.py::test_no_landed_adoption_verb_still_owes_the_file_the_board_reads`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cli_contract.py::test_every_verb_acknowledged_for_conformance_is_refused_without_one_elsewhere`

Old text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, two modules
```

New text:

```
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        planned_in="U27",
    ),
    # ── Deletion: one surface, two modules
```

### `r925.R3_no_isrc_unsaid`

A track with no ISRC prints nothing where the ISRC goes

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R3_no_isrc_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/test_render_payloads.py::test_job_show_lists_the_frozen_tracks_and_a_payload_without_them_prints_none`

Old text:

```
        isrc = f"isrc {_one_line(row['isrc'])}" if row.get("isrc") else "no isrc"
```

New text:

```
        isrc = f"isrc {_one_line(row['isrc'])}" if row.get("isrc") else ""
```

### `u247.M7_load_keyed_on_path_size_time`

active_taxonomy.load: remember the answer by the copy's path, size and modification time, the identity METHOD's second pattern warns of

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `u247.json`, row `M7_load_keyed_on_path_size_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_rewritten_between_two_loads_is_read_and_judged_again`
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`

Old text:

```
    path, text = read_text(cfg)
    if text is None:
        return _shipped(cfg.taxonomy.template)
    try:
        return taxonomy.load_taxonomy(text)
```

New text:

```
    memo = load.__dict__.setdefault("by_file", {})
    where = config.state_path("taxonomy_active", cfg)
    try:
        held = where.stat()
        key = (str(where), held.st_size, held.st_mtime_ns)
    except OSError:
        key = None
    if key is not None and key in memo:
        return memo[key]
    path, text = read_text(cfg)
    if text is None:
        return _shipped(cfg.taxonomy.template)
    try:
        if key is not None:
            memo[key] = taxonomy.load_taxonomy(text)
        return taxonomy.load_taxonomy(text)
```

### `u260.E3_key_drops_cap`

to_cdj_jpeg_remembered: key without the byte cap

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E3_key_drops_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, 0)
```

### `u83-a.E10_reported_dimensions`

The encoder reports width and height transposed

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E10_reported_dimensions`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_size_none_keeps_the_native_resolution`

Old text:

```
return CdjJpeg(encoded, measured.width, measured.height, measured.depth)
```

New text:

```
return CdjJpeg(encoded, measured.height, measured.width, measured.depth)
```

### `u83-a.E9_resize`

New art is no longer resized to the 800 pixel square

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E9_resize`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_progressive_rgba_png_comes_out_a_baseline_rgb_jpeg_under_the_cap`
  - `tests/test_art.py::test_the_reported_dimensions_match_what_pillow_reads_back`

Old text:

```
    if size is not None and img.size != (size, size):
```

New text:

```
    if False:
```

### `u83-b.W2_format_guard`

The writer accepts a picture that is not a JPEG

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W2_format_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[png]`

Old text:

```
    if measured.format != "JPEG":
```

New text:

```
    if False:
```

### `r349-b.B1_absent_is_none`

A job with no outcome directory reports an empty mapping rather than no field

- File: `src/cratekit/core/backup_facts.py`
- Source: `r349-b.json`, row `B1_absent_is_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_of_another_verb_grows_no_outcomes_field`

Old text:

```
    if not directory.is_dir():
        return None
```

New text:

```
    if not directory.is_dir():
        return {}
```

### `u953.M19_backup_facts_damaged_remedy`

_damaged answers a damaged fact file with run doctor instead of the repair

- File: `src/cratekit/core/backup_facts.py`
- Source: `u953.json`, row `M19_backup_facts_damaged_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_backup_quick.py`, `tests/test_doctor.py`
- Collected: 753 against a baseline of 753
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_no_backup[unreadable]`
  - `tests/modules/test_tools.py::test_a_record_that_cannot_be_read_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_says_which_kind_of_run_it_was[under-a-real-run-gains-no-rehearsal-step]`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_says_which_kind_of_run_it_was[under-a-rehearsal-says-so]`
  - `tests/test_backup_cli.py::test_an_unwritable_fact_file_says_which_file_rather_than_report_defect`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    return BackupFactsUnreadable(message, path=path, remedy=Remedy.REPAIR_BACKUP_FACTS)
```

New text:

```
    return BackupFactsUnreadable(message, path=path, remedy=Remedy.RUN_DOCTOR)
```

### `u331.S03_yt_dlp_install_step_dropped`

binaries.yt_dlp_missing: give no install step even when the platform's package manager is known

- File: `src/cratekit/core/binaries.py`
- Source: `u331.json`, row `S03_yt_dlp_install_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/intake/test_set_fetch.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint`
  - `tests/test_acquire_fallback.py::test_a_missing_binary_refuses_with_the_install_hint`

Old text:

```
            (f"install {', '.join(hint.packages)} with {hint.manager}, then run it again",)
            if hint is not None
            else ()
```

New text:

```
            ()
```

### `u254.C1_append_unsynced`

append_durable_bytes: return without syncing the appended record

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C1_append_unsynced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 962 against a baseline of 962
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

### `r290-author.J2_blocked_raises_the_plain_type`

Raise a plain CratekitError for a parked job, so the verb exits non zero and the outcome word says failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J2_blocked_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 48 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[export.playlist]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
        raise JobBlocked(job.cause)
```

New text:

```
        raise CratekitError(job.cause)
```

### `u298.H16_reported_extra_under_progress`

reported: a verb's own detail is dropped from progress

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H16_reported_extra_under_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_refused.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_vocals_cli.py`
- Collected: 1398 against a baseline of 1398
- Kills: 122 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - `tests/intake/test_workers.py::test_queueing_a_set_identifies_it_and_gives_the_driver_one_item_per_track`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - ... and 107 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `u342.S2_stamp_refuses_a_marker_alone`

stamp_head: drop the refusal of a name with nothing but a marker after the head

- File: `src/cratekit/core/naming.py`
- Source: `u342.json`, row `S2_stamp_refuses_a_marker_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_title_with_no_head_is_stamped_and_keeps_every_byte[a-marker-and-blanks]`
  - `tests/test_analyze_adopt.py::test_a_title_with_no_head_is_stamped_and_keeps_every_byte[a-marker-and-nothing-after]`
  - `tests/test_analyze_adopt.py::test_a_title_with_no_head_is_stamped_and_keeps_every_byte[nothing-to-follow-the-head]`

Old text:

```
        or not strip_head(name, template=template).strip()

```

New text:

```
        or False

```

### `u205.G2_app_rate_limit_not_counted`

gate: a rate limit answer to the app is counted as the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G2_app_rate_limit_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`

Old text:

```
            if app:
                state.app_rate_limited += 1
```

New text:

```
            if False:
                state.app_rate_limited += 1
```

### `r758-a.W1_marker_not_judged`

the guard stops judging a changed soft delete marker, so any writer removes a row in any table with the guard saying nothing

- File: `src/cratekit/core/rb_changes.py`
- Source: `r758-a.json`, row `W1_marker_not_judged`
- Moved: U953 replaced the local rb_writer name with a _writer() call on the marker line, so the same impossible extra condition silences the same marker judgment
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 300 against a baseline of 300
- Kills: 74 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row_or_a_hard_delete`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[cloudAgentRegistry]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentCue]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[contentFile]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdActiveCensor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdAlbum]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdArtist]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCategory]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdColor]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdContent]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdCue]`
  - `tests/test_rb_writer_guard.py::test_a_changed_marker_is_a_removal_and_no_ordinary_commit_admits_one[djmdDevice]`
  - ... and 59 more, see the JSON sidecar

Old text:

```
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted:
```

New text:

```
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted and table == "":
```

### `r679-a.A8_actor_is_not_the_rule`

supersede: write a fixed word as the actor instead of the rule that owned the row

- File: `src/cratekit/core/review.py`
- Source: `r679-a.json`, row `A8_actor_is_not_the_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/test_match_states.py`, `tests/intake/test_workers.py`
- Collected: 834 against a baseline of 834
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`
  - `tests/test_review_queue.py::test_a_batch_resolution_does_not_touch_items_a_resolution_superseded`
  - `tests/test_review_queue.py::test_a_superseded_item_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_review_queue.py::test_an_export_carrying_the_third_verdict_imports_without_conflict`
  - `tests/test_review_queue.py::test_an_import_carries_the_machines_verdict_under_the_machines_rules`
  - `tests/test_review_queue.py::test_supersede_retires_an_open_item_naming_the_rule_and_it_leaves_the_open_list`
  - `tests/test_review_queue.py::test_supersede_takes_several_identifiers_and_retires_only_the_open_ones_among_them`

Old text:

```
            (str(Verdict.SUPERSEDED), rule, now, now, *open_ids),
```

New text:

```
            (str(Verdict.SUPERSEDED), "resolution", now, now, *open_ids),
```

### `u329.P6_session_ack_wrong_family`

session_ack binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_ack.py`
- Source: `u329.json`, row `P6_session_ack_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`
- Collected: 362 against a baseline of 362
- Kills: 69 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_nested_session_is_refused_rather_than_deadlocking`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_a_volume_whose_identity_moved_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_deferred_routing.py::test_a_bucket_folder_that_does_not_exist_yet_is_not_mistaken_for_a_rename`
  - `tests/test_deferred_routing.py::test_a_crash_between_the_commit_and_the_mark_converges`
  - ... and 54 more, see the JSON sidecar

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `u23-round-8-independent.X15_save_drops_the_id3v1_trailer`

A tag write destroys an mp3's legacy ID3v1 trailer

- File: `src/cratekit/core/tags.py`
- Source: `u23-round-8-independent.json`, row `X15_save_drops_the_id3v1_trailer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_tags.py`
- Collected: 853 against a baseline of 853
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_mp3s_legacy_id3v1_genre_survives_a_write_and_a_revert[.mp3]`

Old text:

```
    trailer = _id3v1_trailer(path)
    handle.save()
    if trailer is not None:
        _restore_id3v1_trailer(path, trailer)

```

New text:

```
    handle.save()

```

### `u310.G3_recorded_reject_honoured`

review: the gate accepts every offered item, a recorded reject included

- File: `src/cratekit/deletion/cli.py`
- Source: `u310.json`, row `G3_recorded_reject_honoured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`, `tests/behaviour/deletion.py`
- Collected: 393 against a baseline of 393
- Kills: 3 (killed)
- Killed:
  - `tests/behaviour/deletion.py::test_review_offers_declines_trashes_and_lists_tombstones`
  - `tests/behaviour/deletion.py::test_review_puts_the_file_back_when_its_tombstone_cannot_be_written`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`

Old text:

```
                if item.verdict is None:
```

New text:

```
                if True:
```

### `r706-a.A3_max_parts_four`

MAX_PARTS moves from three to four, the decision's Part A, B and C plus one

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A3_max_parts_four`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_and_neither_spend_refusal_is_a_miss`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
MAX_PARTS = 3
```

New text:

```
MAX_PARTS = 4
```

### `r706-b.B4_parts_reported_as_one`

The result says one part whatever the cut

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B4_parts_reported_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_one_cached_plan_and_a_gap_meets_the_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
        parts=len(parts),
```

New text:

```
        parts=1,
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

### `u103-a.A7_offsets_in_the_key`

Take the offsets out of the key material, so a changed chunk plan keeps its old key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A7_offsets_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[chunk-plan]`
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

### `u57-recognition-and-items.M3_auth_family_loses_3001`

3001, a missing or invalid access key, stops being a credential answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M3_auth_family_loses_3001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_an_answer_that_ends_the_run_stops_it_at_that_call[credential-is-auth-failed]`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload5-auth]`

Old text:

```
_AUTH_CODES = frozenset({3001, 3002, 3006, 3014})
```

New text:

```
_AUTH_CODES = frozenset({3002, 3006, 3014})
```

### `r1295.M16_set_aside_one_word`

set_aside: always names the title as the absent half, so an artistless track is misnamed

- File: `src/cratekit/intake/cli.py`
- Source: `r1295.json`, row `M16_set_aside_one_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/intake/test_workers.py`, `tests/test_sync_all.py`
- Collected: 221 against a baseline of 221
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
why=f"the account lists it with no {_absent(title)}"
```

New text:

```
why="the account lists it with no title"
```

### `r682-a.M6_reason_counted_outside_state_guard`

a reason is counted before the state word is checked, so a row in a state the counts do not know is counted under it

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M6_reason_counted_outside_state_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
        if word in counts:
            counts[word] += 1
            why = report.get("why")
            if isinstance(why, str) and why:
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
```

New text:

```
        why = report.get("why")
        if isinstance(why, str) and why:
            by_reason.setdefault(word, {})[why] = by_reason.get(word, {}).get(why, 0) + 1
        if word in counts:
            counts[word] += 1
```

### `u120.L2_date_added_ignored`

hearted_on: the older client's date_added is not read

- File: `src/cratekit/intake/cli.py`
- Source: `u120.json`, row `L2_date_added_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`

Old text:

```
    for name in ("user_date_added", "date_added"):
```

New text:

```
    for name in ("user_date_added",):
```

### `u57-recognition-and-items.C7_foreign_job_driven`

A job of another verb is driven under this verb's envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C7_foreign_job_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_job_of_another_handler_lists_no_tracks_and_is_not_driven_under_this_envelope`

Old text:

```
    if job.handler_key not in INTAKE_KEYS:
```

New text:

```
    if False:
```

### `r924.C3_recording_drops_progress`

_recording does not pass its progress to the fetch

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r924.json`, row `C3_recording_drops_progress`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
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

### `u103-b.C7_unwritten_note`

Never say that the answers a pass paid for could not be kept

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C7_unwritten_note`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_answers_that_could_not_be_kept_are_said_on_both_verbs`

Old text:

```
    if result.cache_unwritten:
        notes.append(
```

New text:

```
    if False:
        notes.append(
```

### `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero`

A set where chunks got no answer and the rest named nothing is reported as nothing identified

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u57-recognition-and-items.json`, row `C6_unanswered_zero_reads_as_zero`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`

Old text:

```
    if not result.unreached:
        return ()
    if not result.rows:
        raise refuse(
```

New text:

```
    if not result.unreached or not result.rows:
        return ()
    if False:
        raise refuse(
```

### `r924.F4_sum_not_largest`

The bytes said are the sum of every file in the folder rather than the largest

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F4_sum_not_largest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_the_bytes_said_are_the_largest_file_and_not_the_sum`

Old text:

```
                largest = max(largest, one.stat().st_size)
```

New text:

```
                largest += one.stat().st_size
```

### `u104-b.F7_remove_on_exit`

Drop the removal of the scratch folder when the pass ends, so a fetched mix stays on disk

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F7_remove_on_exit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 11 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[failed]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[several]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[timed-out]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[not-there]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[outside]`
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`
  - `tests/intake/test_set_fetch.py::test_identification_that_raises_still_removes_the_fetched_mix`
  - `tests/intake/test_set_fetch.py::test_identify_over_a_url_writes_a_tracklist_named_for_the_address`
  - `tests/intake/test_set_fetch.py::test_the_page_a_mix_came_from_is_frozen_on_the_set_job`

Old text:

```
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
        if scratch.exists():
```

New text:

```
    finally:
        if scratch.exists():
```

### `u104-c.P6_address_is_stripped`

Stop stripping the address before it is digested, so a stray space names a second scratch folder for one mix

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P6_address_is_stripped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_scratch_entry_is_declared_under_the_installation_root`

Old text:

```
    token = hashlib.sha256(url.strip().encode("utf-8")).hexdigest()[:SCRATCH_DIGEST_CHARS]
```

New text:

```
    token = hashlib.sha256(url.encode("utf-8")).hexdigest()[:SCRATCH_DIGEST_CHARS]
```

### `r924.R1_bound_identifier_not_told`

recognize does not hand progress to the bound identifier

- File: `src/cratekit/intake/recognize.py`
- Source: `r924.json`, row `R1_bound_identifier_not_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 78 against a baseline of 78
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
            recognition, refresh=refresh, progress=progress
```

New text:

```
            recognition, refresh=refresh
```

### `u102-a.P1_root_boundary`

_under: match the root as a bare prefix, without the separator, so a sibling folder sharing the prefix is inside it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P1_root_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder`

Old text:

```
    return held == wanted or held.startswith(wanted + "/")
```

New text:

```
    return held == wanted or held.startswith(wanted)
```

### `u102-a.U3_empty_name`

_unusable_why: stop refusing an empty proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U3_empty_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if proposed in {".", ".."} or Path(proposed).name != proposed:
```

### `u102-b.G7_referenced_is_owed`

_HELD: stop counting a referenced file as an accepted rename that did not happen, so the run answers ok over it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G7_referenced_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (COLLIDES, UNUSABLE)
```

### `u52-item-derivation.C1_can_list_always_true`

Answer yes for every object, which is what makes the refusal above unreachable from the other side

- File: `src/cratekit/label/crawl.py`
- Source: `u52-item-derivation.json`, row `C1_can_list_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`
- Collected: 180 against a baseline of 180
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing`

Old text:

```
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

New text:

```
    return True
```

### `r381.M5_migrate_any_identifier`

migrate moves any entry whose slug differs, not only one the old fold produced

- File: `src/cratekit/label/registry.py`
- Source: `r381.json`, row `M5_migrate_any_identifier`
- Moved: The _legacy_slug alias was the fold of the name and is now called as _fold; the mutation drops the old fold test as before.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 429 against a baseline of 429
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_registry_survives_a_label_rename_without_orphaning_its_state`
  - `tests/test_label_slug.py::test_a_renamed_entry_under_the_old_fold_is_not_taken_by_its_old_name`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries0]`
  - `tests/test_label_slug.py::test_an_identifier_the_old_fold_did_not_produce_is_left_alone[entries1]`

Old text:

```
    if new == entry.label_id or entry.label_id != _fold(entry.name):

```

New text:

```
    if new == entry.label_id:

```

### `r704-a.S4_context_walk_one_level`

the context walk stops one level down, above the 429 the client's translation leaves two contexts deep

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S4_context_walk_one_level`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in _linked(exc, "__context__")):
```

New text:

```
    if any(status_of(link) in RATE_LIMIT_STATUSES for link in (exc, exc.__context__)):
```

### `u237.M6_substring_again`

_words_within: back to a raw substring, so the Rawax needle confirms RAWAXXX

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M6_substring_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Puls-Pulse]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[RAWAXXX-Rawax]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-RAWAXXX]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-Rawaxxx Records]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[adenza-Cadenza]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[ronos-Cronos]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[tide-Tidewater]`
  - `tests/modules/test_labels.py::test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
    return f" {needle} " in f" {credit} "
```

New text:

```
    return needle in credit
```

### `u192.F7_queue_only_always`

queue_only: always True, so a verb run by hand queues and returns as before U192

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F7_queue_only_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`
- Collected: 342 against a baseline of 342
- Kills: 9 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_analysis_workers.py::test_analyze_restamp_by_hand_drives_its_job_and_says_the_database_note_once`
  - `tests/test_analysis_workers.py::test_analyze_run_by_hand_queues_and_drives_its_job_to_succeeded_in_one_call`
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_prints_the_settled_job_and_no_drive_command`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call`

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return True
```

### `r229.L10_a_name_matches_by_bare_suffix`

The name rule drops the separator, so Big Crate is recognised as Crate

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L10_a_name_matches_by_bare_suffix`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_written_before_tracks_were_kept_is_recognised_by_name[2024/Big Crate-Crate-False]`

Old text:

```
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))
```

New text:

```
    return bool(name) and (recorded_key == name or recorded_key.endswith(name))
```

### `r229.L1_a_third_suffices`

The share of a record's tracks a crate must still carry drops from a half to a third, so two of five is recognised

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L1_a_third_suffices`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_is_recognised_when_the_crate_still_carries_half_its_tracks[two-of-five]`
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`

Old text:

```
SHARED_DENOMINATOR = 2
```

New text:

```
SHARED_DENOMINATOR = 3
```

### `r229.L9_an_empty_list_is_a_legacy_record`

A record this build wrote with no contents qualifies by name, as a record from before the field existed does

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L9_an_empty_list_is_a_legacy_record`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_this_build_wrote_with_no_tracks_is_not_a_legacy_record`

Old text:

```
        elif _legacy(record) and _same_name(key, name):
```

New text:

```
        elif _same_name(key, name):
```

### `u261.O2_account_drops_the_app`

open_account: build the account without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u261.json`, row `O2_account_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=held.app)
```

New text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=None)
```

### `u27-reports-round-1.L1_distinct_tracks`

Sum the sub-playlists instead of counting distinct tracks, the double count the docstring names

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L1_distinct_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_genre_counts_distinct_tracks_rather_than_summing_its_playlists`

Old text:

```
                tracks=len(tracks),
```

New text:

```
                tracks=playlists and sum(len(p.track_ids) for p in view.playlists if p.path[: len(folder)] == folder and len(p.path) > len(folder)),
```

### `u311.D3_tempo_never_read`

The library report reads a field the name head never carries, so no track has a tempo

- File: `src/cratekit/modules/reports/library.py`
- Source: `u311.json`, row `D3_tempo_never_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tempo_median_over_an_even_population_averages_the_middle_pair`
  - `tests/modules/test_reports_engines.py::test_the_tempo_spread_reads_a_marked_head_and_counts_what_it_could_not_read`

Old text:

```
    written = (parse_head(name, template=template) or {}).get("bpm")
```

New text:

```
    written = (parse_head(name, template=template) or {}).get("tempo")
```

### `r221-a.E2_outcome_payload_drops_the_key`

The renderer stops carrying the flag, so every reader of a rendered run is back to guessing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E2_outcome_payload_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r222-a.A7_no_record_is_a_late_floor`

Answer a missing record with a floor after every date, so nothing is held and the old rotation runs on a remote with no completed mirror

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A7_no_record_is_a_late_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`

Old text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
```

New text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return "9999"
```

### `r367.E1_a_failed_transfer_is_unread`

existing guard sample: run_restore returns results without reading return codes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E1_a_failed_transfer_is_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 15 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent`
  - `tests/modules/test_tools.py::test_a_rehearsed_restore_does_not_clear_the_live_sidecars`
  - `tests/modules/test_tools.py::test_a_restore_copies_the_log_only_when_the_snapshot_holds_it[holding-the-log-copies-it]`
  - `tests/modules/test_tools.py::test_a_restore_copies_the_log_only_when_the_snapshot_holds_it[only-the-database-skips-the-absent-sidecar]`
  - `tests/modules/test_tools.py::test_restore_removes_stale_sidecars_before_copying`
  - `tests/modules/test_tools.py::test_the_sidecars_are_cleared_before_the_mirror_too`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

New text:

```
        if result.returncode == 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

### `u311.A4_logged_takes_any_json`

The comparison log reader keeps any JSON value, not only objects

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A4_logged_takes_any_json`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 897 against a baseline of 897
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
    return [entry for entry in map(_parsed, stderr.splitlines()) if isinstance(entry, dict)]
```

New text:

```
    return [entry for entry in map(_parsed, stderr.splitlines()) if entry is not None]
```

### `u45-round-1.E2_publish_unconditional`

Publish regardless of the flag, the same hole reached from the other side

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E2_publish_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        if publish:
            backup_facts.record(
```

New text:

```
        if True:
            backup_facts.record(
```

### `u48-author.P7_listing_message_reworded`

Reword the listing message, not append: the suite asserts with `in`

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P7_listing_message_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`

Old text:

```
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
```

New text:

```
                f"nothing was removed and the rotation will stay stopped "
                f"until it succeeds. The backup itself completed"
```

### `u311.A8_no_directory_matcher`

A dir/** exclude gets no directory matcher, so the walk descends into the excluded folder

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u311.json`, row `A8_no_directory_matcher`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 317 against a baseline of 317
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_quick_walk_reads_hashes_globs_and_names_as_rclone_does`

Old text:

```
directories=tuple(d for _, d in pairs if d is not None)
```

New text:

```
directories=()
```

### `r154-b.B2_two_markers`

Accept a named snapshot when the expected identity is AMONG its markers, so a folder two libraries wrote passes on either one

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B2_two_markers`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_two_identities_or_an_empty_marker_refuse_as_another_librarys`
  - `tests/modules/test_tools.py::test_two_markers_are_refused_without_offering_an_identity_to_pass`

Old text:

```
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

New text:

```
        if expected in recorded:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

### `r338-a.B4_no_undo_archive`

_plan_database: drop the backup-dir, so a share emptied by a reinstall empties its only copy with nothing to undo it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B4_no_undo_archive`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r338-b.R7_restore_is_a_sync`

_plan_restore_inside_the_gates: pull the share with sync, which deletes every analysis file beside the restored database that the mirror never saw

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R7_restore_is_a_sync`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r367.G1_always_copy_the_restored_sidecar`

the original defect: copy every restored sidecar whether the snapshot holds it or not

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G1_always_copy_the_restored_sidecar`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_restore_copies_the_log_only_when_the_snapshot_holds_it[only-the-database-skips-the-absent-sidecar]`
  - `tests/modules/test_tools.py::test_a_snapshot_that_cannot_be_listed_refuses_before_clearing`
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        if name not in held:
            absent.append(sidecar.suffix)
            continue
        commands.append(

```

New text:

```
    absent: list[str] = []
    for sidecar in config.state_file("rekordbox_db").sidecars:
        if not sidecar.restored:
            continue
        name = f"{database_target.name}{sidecar.suffix}"
        commands.append(

```

### `r388-a.M3_contents_listing_back_to_absence`

A named snapshot whose db folder listing exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M3_contents_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r388-b.M9_root_absent_read_as_failure`

Drop the exit 3 branch on the root listing, so a root no backup wrote is a listing failure

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M9_root_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `u44-author.A2_archive_collision_skips`

Restore the source system's behaviour: an existing archive entry is skipped rather than verified

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `A2_archive_collision_skips`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 245 against a baseline of 245
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_archive_entry_with_the_same_name_and_different_content_refuses`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_impostor_matching_the_first_chunk_is_still_a_different_recording`

Old text:

```
    if destination.exists():
        if digest(destination) == source_digest:
            return destination
```

New text:

```
    if destination.exists():
        return destination
```

### `r187-b.B6_stamp_unchecked`

_load_cache: trust a cache parsed under another template, so a changed lossy marker serves the old titles

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B6_stamp_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_parsed_under_another_template_is_discarded`

Old text:

```
    if data.get("template") != stamp:
        return {}

```

New text:

```
(empty)
```

### `u43-author-light.E2_tempo_band_dropped`

in_band returns True for everything, so a track a hundred BPM away enters the pool on its key alone

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E2_tempo_band_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_band_holds_half_and_double_time_and_drops_when_the_anchor_has_no_tempo`

Old text:

```
    if anchor_bpm is None:
        return True
    if candidate_bpm is None:
        return False
```

New text:

```
    if anchor_bpm is None or candidate_bpm is None:
        return True
```

### `u281.R5_no_reset`

Refusals.heard: an answer that is not a refusal never ends the run of them, so a catalogue that answered can be stopped

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R5_no_reset`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_an_answer_between_refusals_ends_the_run_of_them[a-match-between]`
  - `tests/test_beatport_refusal.py::test_an_answer_between_refusals_ends_the_run_of_them[a-miss-between]`
  - `tests/test_beatport_refusal.py::test_an_answer_between_refusals_ends_the_run_of_them[an-outage-between]`

Old text:

```
        else:
            self.running.pop(outcome.source, None)
            self.last.pop(outcome.source, None)
```

New text:

```
        else:
            pass
```

### `u322.M17_deezer_gate_open_always`

second_opinion: the flag is ignored, so tag folder asks Deezer past a refusing Beatport too

- File: `src/cratekit/tagging/published.py`
- Source: `u322.json`, row `M17_deezer_gate_open_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_walk_refusal.py`, `tests/test_tag_suggest.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_published_genre.py`, `tests/test_beatport_refusal.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[refused]`
  - `tests/test_catalogue_walk_refusal.py::test_tag_folders_gate_is_unchanged`

Old text:

```
            and not (past_a_refusing_shop and _refused_beside_discogs(first, hit))
```

New text:

```
            and not _refused_beside_discogs(first, hit)
```

### `u260.F5_binder_builds_per_call`

for_images: build a fresh remembering fetch on every call, so the worker's per item binder call forgets every picture

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F5_binder_builds_per_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 8 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_binder_hands_back_one_fetch_per_process_and_the_reset_drops_it`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    if not _images:
        _images.append(remembering(default_image_fetch(), admit=art.decodes))
    return _images[0]
```

New text:

```
    return remembering(default_image_fetch(), admit=art.decodes)
```

### `u281.W2_searcher_ignores_the_handed_count`

catalogue_searcher: build its own count whatever it is handed, so a worker's per file searcher starts again every file

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W2_searcher_ignores_the_handed_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 10 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
    counted = Refusals() if refusals is None else refusals
```

New text:

```
    counted = Refusals()
```

### `u118-d.T1_old_playlist_split_row`

Soul no longer splits R&B's former place, so a Soul track in the old Soul / R&B playlist is not moved

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u118-d.json`, row `T1_old_playlist_split_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_taxonomy.py`, `tests/test_adopt_former_place.py`
- Collected: 202 against a baseline of 246
- Kills: 8 (collect-error)
- Note: collection changed: 202 collected against a baseline of 246. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_the_old_soul_r_and_b_playlist_moves_to_soul_and_is_withheld_until`
  - `tests/test_adopt_split_place.py::test_a_split_place_is_found_as_the_r_and_b_place_it_is`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_an_r_and_b_track_in_the_old_soul_r_and_b_playlist_still_moves_to_r_and_b`
  - `tests/test_adopt_split_place.py::test_soul_is_split_out_of_every_r_and_b_band_and_r_and_bs_old_playlist`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`
  - `tests/test_taxonomy.py::test_a_template_breaking_a_rule_is_refused_by_name[split-of-holders-former-place-renamed]`
  - `tests/test_taxonomy.py::test_the_shipped_template_splits_one_bucket_out_of_every_place_of_another`
- Collection errors: `tests/test_adopt_former_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_former_place.py`

Old text:

```
[[bucket.split_from]]
id = "rnb_soul_rnb"
bucket = "rnb"
sub = "non_electronic_soul_rnb"
display = "Soul / R&B"

```

New text:

```
(empty)
```

### `u133-b.T8_bpm`

Jazz's tempo window starts at 120, off the non electronic window

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T8_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`
- Collected: 894 against a baseline of 894
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_jazz_is_shaped_as_hip_hop_is`
  - `tests/test_routing_parity.py::test_the_tempo_window_is_unchanged_for_every_source_string[Jazz]`
  - `tests/test_routing_parity.py::test_the_tempo_window_is_unchanged_for_every_source_string[jazz]`

Old text:

```
display = "Jazz"
family = "other"
bpm = { start = 110,
```

New text:

```
display = "Jazz"
family = "other"
bpm = { start = 120,
```

### `r675.G2_row_leaf_not_keyed`

_referenced: the dark row's leaf is looked up as spelled, so a case or composition variant of a candidate's name is another name

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G2_row_leaf_not_keyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 14 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_to_a_candidate_by_name_ignoring_case`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_a_row_recording_a_link_to_nothing_is_dark`
  - `tests/test_naming_apply_cli.py::test_a_row_that_goes_unmapped_after_the_gate_refuses_before_any_rename`
  - `tests/test_naming_apply_cli.py::test_a_row_under_an_unmapped_volume_refuses_and_renames_nothing`
  - `tests/test_naming_apply_cli.py::test_a_rule_differing_from_the_recorded_volume_only_in_case_refuses[prefix_map0]`
  - `tests/test_naming_apply_cli.py::test_an_unmapped_row_refuses_the_plan_too`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(Path(decoded).name))
```

### `r500-c.G14_located_skips_the_decode`

trees.located resolves the raw recorded value without decoding it, the shared locate step both writers and this verb now call

- File: `src/cratekit/write/trees.py`
- Source: `r500-c.json`, row `G14_located_skips_the_decode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 1006 against a baseline of 1006
- Kills: 9 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`
  - `tests/test_tree_writer.py::test_normalization_resolves_each_spelling_to_the_right_row[a-location-url]`

Old text:

```
    decoded = locations.location_to_path(str(recorded))
    return decoded,
```

New text:

```
    decoded = str(recorded)
    return decoded,
```

### `u297.S1_a_root_outside_the_scenarios_own_directory`

refuse_a_root_outside: accept a configuration or state directory anywhere in the temporary directory, another test's included

- File: `tests/behaviour/conftest.py`
- Source: `u297.json`, row `S1_a_root_outside_the_scenarios_own_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_root_outside_the_scenarios_own_directory_is_refused[in-another-tests-directory]`

Old text:

```
        if not compare.is_inside(path, scenario_root):
```

New text:

```
        if False:
```

