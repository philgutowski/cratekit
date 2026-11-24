# Mutation table: u332-replay-after-4

Measured by `scripts/mutate.py` on 2026-11-24 07:07 UTC, branch `HEAD` at `d0c7143a`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23212 collected. pytest invocations for this batch: 282.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 07:07 UTC for commit `d0c7143a91b0`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 106, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23212 against 23212. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B2_the_temporary_directory_itself` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u122.H1_no_hold` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 10 | killed |
| `u122.N2_next_offers_busy` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 2 | killed |
| `u148.L2_issue_literal` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 6 | killed |
| `u151.C1_no_cursor_trusted` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.U1_unblocks_always_written` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 4 | killed |
| `u187.A2_answer_counted_as_a_hold` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 5 | killed |
| `u203.M4_sentence_cut_anywhere` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u291.L3_lanes_one_over` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u330.A8_progress_refreshes_nothing` | `scripts/board.py` | maintainer | 9 file(s) | 947 | 1 | killed |
| `r83.D4_drop_type_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 2 | killed |
| `u176.C11_fetch_refuses_untrusted` | `src/cratekit/acquire/bandcamp.py` | user | 1 file(s) | 46 | 4 | killed |
| `u176.C8_member_base_name` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 92 | 2 | killed |
| `u176.V3_seller_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 13 | killed |
| `u177.B1_seller_by_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 5 | killed |
| `u177.B9_untagged_refusal` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u205.C4_rejected_token_kept` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 2 | killed |
| `r289-b.B4_unknown_job_read_as_terminal` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 367 | 1 | killed |
| `r668-a.M2_resume_argv_carries_the_list` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 2 | killed |
| `u108-c.G25_drive_maps_ending` | `src/cratekit/acquire/cli.py` | user | 7 file(s) | 477 | 31 | killed |
| `u42-author.C3_strict_consults_the_marker` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 25 | 3 | killed |
| `u54-acquisition-worker.G10_absent_result` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `u54-acquisition-worker.G20_output_exists` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `r703-a.D1_pool_reads_text` | `src/cratekit/acquire/download.py` | user | 5 file(s) | 448 | 3 | killed |
| `u80.F1_one_platform` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 7 | killed |
| `u81-fetch-b.L2_any_suffix` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u80.C7_offered_not_named` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u81-fetch-a.W7_final_unmarked` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 4 | killed |
| `r1016.M10_wrong_endpoint` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 793 | 6 | killed |
| `r1016.M9_offset_not_sent` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 793 | 10 | killed |
| `r878-a.A2_cursor_refuses_offset_rule` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 141 | 1 | killed |
| `r878-b.B2_client_part_refusal` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 141 | 2 | killed |
| `u65.A2_max_pages_gets_a_default` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 198 | 1 | killed |
| `u65.C3_a_full_page_at_the_declared_end_stops_anyway` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 198 | 1 | killed |
| `u65.E4_the_playlist_total_is_never_wired` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 198 | 1 | killed |
| `r679-b.B5_rule_not_recorded` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 5 | killed |
| `u213.M5_listed_names_artist` | `src/cratekit/acquire/match_list.py` | user | 3 file(s) | 726 | 3 | killed |
| `r703-a.LF1_plain_runtime_error` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 1 | killed |
| `r703-b.L4_error_notes_nothing` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 2 | killed |
| `r703-c.C2_message_outranks_exception` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 1 | killed |
| `u47-author.CODEC_refusal_drops_the_codec_name` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 2 | killed |
| `u47-author.R196_no_stored_session_proceeds` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 1 | killed |
| `u47-author.R197_progress_enabled` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 1 | killed |
| `u254.M04_cache_identity_no_mtime` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 741 | 1 | killed |
| `u254.M13_header_older_version` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 1 | killed |
| `u254.M21_record_needs_actor` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 3 | killed |
| `r731-b.M15_gate_without_the_read_state` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 2 | killed |
| `u27-adopt-apply-author.A2_gate_found_by_position` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 1037 | 1 | killed |
| `u55-collection-reader.R20_membership_locations_key` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 9 | killed |
| `u23-round-8-independent.X2_approval_option_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 613 | 1 | killed |
| `r758-b.M3_renamed_playlist_is_moved_from` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A8_double_listed_beside_a_move` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `u118-c.M4_held_split_none` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 189 | 2 | killed |
| `r758-b.C5_a_sub_nobody_was_shown_is_removed` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r731-b.M16_skewed_registry_raises_at_the_plan` | `src/cratekit/adopt/placements.py` | user | 2 file(s) | 70 | 1 | killed |
| `r788-c.L9_every_library_is_calibrated` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 163 | 2 | killed |
| `r722.P1_level_none` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 651 | 4 | killed |
| `r731-a.M03_same_sub_withheld` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 5 | killed |
| `r731-b.M23_collision_counts_a_listed_track` | `src/cratekit/adopt/plan.py` | maintainer | 2 file(s) | 70 | 1 | killed |
| `r788-b.P14_digest_drops_vocal` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 2 | killed |
| `u956.O14_digest_blind_to_outside` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 685 | 1 | killed |
| `u23-round-8-independent.A5_at_risk_drops_this_call` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 1 | killed |
| `u23-round-8-independent.E1_vacancy_is_mere_absence` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 1 | killed |
| `r759.A2_deadline_a_second_late` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 1 | 1 | killed |
| `u956.O11_no_samefile_walk` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 639 | 2 | killed |
| `u956.O9_path_not_composed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 639 | 1 | killed |
| `u241.M15_identity_without_the_time` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 271 | 1 | killed |
| `u223.M23_intent_link_followed` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 176 | 1 | killed |
| `u223.M8_report_not_mapping` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 176 | 1 | killed |
| `u90-a.A5_min_coefficient` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 2 | killed |
| `u90-b.B7_fit_detail_drops_old_cut` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 2 | killed |
| `u94-a.S5_recursive_not_required` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 2 | killed |
| `u94-b.W6_outcome_energy_only` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 1 | killed |
| `u94-c.N7_root_not_required_first` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 1 | killed |
| `u223.M13_resumed_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 1 | killed |
| `u241.M25_an_idle_resume_overwrites_the_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 271 | 1 | killed |
| `u343.M04_untitled_never_titles` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 323 | 4 | killed |
| `u58-workers-and-wav.R7_absent_energy_stamped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 1 | killed |
| `u263.D13_extensible` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 57 | 11 | killed |
| `u263.D7_stderr_fails` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 2 | killed |
| `u264.M2_leading_zero_dropped` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 1 | killed |
| `u344.M11_centre_read_from_top` | `src/cratekit/analysis/decode.py` | user | 7 file(s) | 552 | 1 | killed |
| `u58-workers-and-wav.E2_uncalibrated_measured` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 176 | 1 | killed |
| `u327.A16_before_values_recorded` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 3 | killed |
| `u327.A7_not_analysed_left` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u342.P2_unanswered_named` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 2 | killed |
| `u327.B3_partial_apply_refuses` | `src/cratekit/analysis/head_adopt_cli.py` | user | 1 file(s) | 114 | 3 | killed |
| `u275.M2_slope_back_to_linux` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 553 | 19 | killed |
| `u343.M09_resume_reads_the_mark_alone` | `src/cratekit/analysis/run.py` | user | 4 file(s) | 501 | 10 | killed |
| `sitting3.G1_columns_by_number` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 4 | killed |
| `sitting3.G12_columns_per_track` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 18 | 1 | killed |
| `u58-zero-row-remeasured.W6_gender_constant` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 176 | 2 | killed |
| `u92-author.G8_refused_file_tagged_zero` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 230 | 2 | killed |
| `r221-a.W4_twin_branch_warning_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B12_warnings_from_the_live_configuration` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B7_unreadable_is_elsewhere` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r757-c2.S6_twin_in_the_other_mode_says_nothing` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 727 | 1 | killed |
| `u45-round-1.C5_first_refusal_taken` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-1.R2_slug_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-2.C7_failed_detail_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u50-zero-rows.W4b_item_ignored_entirely` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 12 | killed |
| `r757-c2.D1_due_a_day_late` | `src/cratekit/cli/doctor_backup.py` | maintainer | 4 file(s) | 727 | 1 | killed |
| `r925.J3_field_not_set` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 5 | killed |
| `r678-a.A1_drop_the_job_state_case` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 9 | killed |
| `r685-a.L3_a_copy_that_does_not_parse_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 2 file(s) | 130 | 5 | killed |
| `u260.E10_encode_memory_unbounded` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u260.E7_encode_bound_off_by_one` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u83-a.E4_cap_inclusive` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.R4_full_decode` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W5b_cap_inclusive` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `r757-b2.F2_first_record_erases_the_implied_date` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 727 | 1 | killed |
| `example-binaries-five-row.B4_unknown_source_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `u27-reports-round-1.R2_governed_tree_code` | `src/cratekit/core/cause.py` | user | 26 file(s) | 5113 | 1 | killed |
| `u197.M2_retired_mapping_empty` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 828 | 4 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/core/jobs.py` | user | 5 file(s) | 349 | 48 | killed |
| `u169.E2_drive_fails_a_decline` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 153 | 11 | killed |
| `u39-author-full.E2_wheel_bound_widened` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1487 | 10 | killed |
| `u205.G7_process_spend_drops_app` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 184 | 1 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 121 | killed |
| `r797-a.T8_competes_in_a_band_bucket` | `src/cratekit/core/routing.py` | user | 4 file(s) | 1097 | 28 | killed |
| `r722.T1_checked_is_lenient` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2990 | 5 | killed |
| `u247.M5_failure_remembered` | `src/cratekit/core/taxonomy.py` | user | 4 file(s) | 293 | 2 | killed |
| `r301.B4_refusal_message_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 3 | killed |
| `r706-a.A7_ceiling_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 227 | 1 | killed |
| `r924.A2_plan_before_the_bounds` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 186 | 1 | killed |
| `u103-a.A2_write_keeps_only_answers` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 1 | killed |
| `u57-recognition-and-items.M16_grid_off_by_one` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 58 | killed |
| `u57-recognition-and-items.M7_fold_never_takes_best_score` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 1 | killed |
| `r682-a.M2_non_string_why_counted` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `r925.S2_out_ignored` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u213.M6_readable_refuses_nameless` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u70.S4_canonical_source` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 241 | 2 | killed |
| `u103-b.C10_open_question_is_pending` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u104-d.C4_scratch_left_said` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u37-author-light.G3_gridless_bpm` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 51 | 1 | killed |
| `u104-a.F3_guard_absent_library_return` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `u104-c.P2_probe_bound` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 41 | 1 | killed |
| `r706-c.C4_pipeline_drops_parts` | `src/cratekit/intake/pipeline.py` | user | 1 file(s) | 67 | 1 | killed |
| `u102-a.D2_open_is_not_accepted` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 23 | 1 | killed |
| `u102-a.P5_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-b.G2_post_gate_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.R2_retryable_after_gate` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u237.M3_one_mark_only` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 12 | killed |
| `r261.S4_existing_can_list` | `src/cratekit/label/sweep.py` | user | 4 file(s) | 521 | 1 | killed |
| `u52-zero-rows.L6_verifier_missing_returns_stub` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `u192.F2_no_retry` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 278 | 4 | killed |
| `r572.E1_export_drop_album` | `src/cratekit/modules/outbound/export.py` | user | 1 file(s) | 64 | 1 | killed |
| `r229.L14_a_recorded_crate_is_a_claimant` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L5_no_crate_side_bound` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `u309-z.U6_pairs_words_only_on_hold` | `src/cratekit/modules/outbound/pairs.py` | user | 5 file(s) | 247 | 1 | killed |
| `u27-reports-round-2.C3_uncovered_order` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.L6_entries_in_no_playlist` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `r154-b.B11_marker_name_safety` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 5 | killed |
| `r222-a.A3_no_floor_holds_nothing` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 2 | killed |
| `r338-b.R2_missing_directory_exit_moved` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 722 | 1 | killed |
| `u48-author.P1_listing_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 4 | killed |
| `u311.A10_paths_keep_the_trailing_empty` | `src/cratekit/modules/tools/backup_record.py` | user | 4 file(s) | 317 | 1 | killed |
| `r154-b.B6_walk_bound` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r338-b.R1_missing_directory_refuses` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-c.C2_carried_share_still_warned` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r367.G7_the_listing_is_of_the_snapshot_root` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 1 | killed |
| `r388-b.M10_named_stamp_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `u311.C3_suffix_case_matters` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 247 | 1 | killed |
| `r187-b.B1_size_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 1 | killed |
| `u311.C7_wider_tier_steps_down` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 339 | 1 | killed |
| `u281.R1_stop_after_four` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 11 | killed |
| `u281.S6_every_title_named_cloudflare` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 205 | 2 | killed |
| `u260.F1_fetch_never_answers_from_memory` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 10 | killed |
| `u260.F9_fetch_memory_unbounded` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u282.P4_refusal_not_unread` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 3 | killed |
| `u133-b.T1_keyword_back` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 946 | collection error | collect-error |
| `u25.G15_barren_watch` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u327.A24_spec_reads_title_head_first` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 213 | 2 | killed |
| `r758-a.T5_dead_track_moved` | `src/cratekit/write/trees.py` | user | 1 file(s) | 87 | 1 | killed |
| `r658-b.S3_adoption_failing_stat` | `tests/test_adoption.py` | user | 1 file(s) | 613 | 1 | killed |

## Row definitions

### `u297.B2_the_temporary_directory_itself`

is_inside: read a directory as inside itself, so the whole temporary directory can be a capture's root and be emptied

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B2_the_temporary_directory_itself`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_the_temporary_directory_itself_is_no_root`

Old text:

```
    return relative != Path(".")
```

New text:

```
    return True
```

### `u122.H1_no_hold`

Remove the hold: derive_status ignores a held status and derives from the graph

- File: `scripts/board.py`
- Source: `u122.json`, row `H1_no_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 10 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if False:
```

### `u122.N2_next_offers_busy`

next lists a busy card under underway but leaves it in the ready list

- File: `scripts/board.py`
- Source: `u122.json`, row `N2_next_offers_busy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
    ready = [n for n in ready if n["number"] not in busy]
```

New text:

```
    ready = list(ready)
```

### `u148.L2_issue_literal`

load_issues asks gh for a literal 300 instead of READ_LIMIT

- File: `scripts/board.py`
- Source: `u148.json`, row `L2_issue_literal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[315-316-the whole limit of 315]`
  - `tests/test_board_reads.py::test_a_read_that_fills_the_limit_is_refused_by_name[316-316-the whole limit of 316]`
  - `tests/test_board_reads.py::test_every_issue_and_project_item_is_read_past_three_hundred`
  - `tests/test_board_reads.py::test_issues_filed_after_the_count_are_read_and_not_refused`
  - `tests/test_board_reads.py::test_one_row_under_the_limit_is_taken_as_whole`

Old text:

```
        "all",
        "--limit",
        str(READ_LIMIT),
```

New text:

```
        "all",
        "--limit",
        "300",
```

### `u151.C1_no_cursor_trusted`

a page that says more and gives no cursor is followed from the start again

- File: `scripts/board.py`
- Source: `u151.json`, row `C1_no_cursor_trusted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_read_that_is_short_or_never_ends_is_refused[150-<lambda>-gave no cursor]`

Old text:

```
        if not after:
            raise Truncated("the project membership read said there was more and gave no cursor")

```

New text:

```
(empty)
```

### `u151.U1_unblocks_always_written`

Unblocks is rewritten on every card again, the U151 cost

- File: `scripts/board.py`
- Source: `u151.json`, row `U1_unblocks_always_written`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_changed_or_missing_unblocks_number_is_written_once[0-7-written0]`
  - `tests/test_board_cost.py::test_a_changed_or_missing_unblocks_number_is_written_once[2-None-written1]`
  - `tests/test_board_cost.py::test_a_sync_with_no_drift_lists_nothing_and_writes_nothing`
  - `tests/test_board_cost.py::test_an_issue_off_the_board_is_added_then_given_its_status_and_number`

Old text:

```
 and apply and item.get("unblocks") != unblocks:
```

New text:

```
 and apply:
```

### `u187.A2_answer_counted_as_a_hold`

cloud_state: count a relayed answer among the session's own comments, so an answer alone holds the card

- File: `scripts/board.py`
- Source: `u187.json`, row `A2_answer_counted_as_a_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Question for Phillip@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-**Answer from Phillip.**@s+6]`

Old text:

```
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "") and not _relayed_answer(c)]
```

New text:

```
    mine = [c for c in ordered if SESSION_MARK in (c.get("body") or "")]
```

### `u203.M4_sentence_cut_anywhere`

_HEADING_END: cut at any stop, whitespace after it or not, so Landed v0.6.0 today is cut inside the version

- File: `scripts/board.py`
- Source: `u203.json`, row `M4_sentence_cut_anywhere`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Landed v0.6.0 today-landed v0.6.0 today]`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026]")
```

### `u291.L3_lanes_one_over`

CLOUD_LANES: eleven lanes, one over the cap

- File: `scripts/board.py`
- Source: `u291.json`, row `L3_lanes_one_over`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes_and_its_help_says_so`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments2-0-said2-unsaid2]`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments3-0-said3-unsaid3]`

Old text:

```
CLOUD_LANES = 10
```

New text:

```
CLOUD_LANES = 11
```

### `u330.A8_progress_refreshes_nothing`

cloud_state: age the hold from the last stated heading, so a Progress note no longer refreshes it and a live session reads as dead

- File: `scripts/board.py`
- Source: `u330.json`, row `A8_progress_refreshes_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`, `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_residual_search.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`, `tests/test_vocals_cli.py`, `tests/test_adoption.py`
- Collected: 947 against a baseline of 947
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[underway-## Started@s+4; ## Plan@s+3; ## Progress@1]`

Old text:

```
    age = _hours_since(_when(mine[-1]))
```

New text:

```
    age = _hours_since(_when(last))
```

### `r83.D4_drop_type_error`

R-348: TypeError leaves the defect classes

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D4_drop_type_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`

Old text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)
```

New text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, NameError)
```

### `u176.C11_fetch_refuses_untrusted`

fetch: a link outside Bandcamp is requested with the session

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C11_fetch_refuses_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`
- Collected: 46 against a baseline of 46
- Kills: 4 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_the_session_is_never_sent_to_a_link_outside_bandcamp[lookalike-host]`
  - `tests/test_bandcamp.py::test_the_session_is_never_sent_to_a_link_outside_bandcamp[other-host]`
  - `tests/test_bandcamp.py::test_the_session_is_never_sent_to_a_link_outside_bandcamp[plain-http]`
  - `tests/test_bandcamp.py::test_the_session_is_never_sent_to_a_link_outside_bandcamp[suffix-host]`

Old text:

```
    if not trusted(link):
        raise BandcampUnavailable
```

New text:

```
    if False:
        raise BandcampUnavailable
```

### `u176.C8_member_base_name`

unpack: a member's path is kept rather than reduced to its base name, so an archive member reaches outside the holding folder

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C8_member_base_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 92 against a baseline of 92
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_unpack_flattens_audio_and_leaves_the_rest`
  - `tests/test_bandcamp.py::test_unpack_refuses_a_name_the_archive_holds_twice`

Old text:

```
                name = PurePosixPath(member.filename.replace("\\", "/")).name
```

New text:

```
                name = member.filename
```

### `u176.V3_seller_filter`

plan: --seller filters nothing

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V3_seller_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 13 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_permissive_policy_marks_a_lossy_file_by_what_it_is[a-lossy-file-under-a-lossless-offer]`
  - `tests/test_bandcamp_cli.py::test_a_permissive_policy_marks_a_lossy_file_by_what_it_is[a-lossy-release]`
  - `tests/test_bandcamp_cli.py::test_a_purchase_already_recorded_is_done_when_its_item_runs_again`
  - `tests/test_bandcamp_cli.py::test_a_purchase_filtered_out_is_offered_on_the_next_run_without_the_filter`
  - `tests/test_bandcamp_cli.py::test_a_purchase_no_longer_downloadable_fails_permanently`
  - `tests/test_bandcamp_cli.py::test_a_seller_filter_plans_only_that_seller`
  - `tests/test_bandcamp_cli.py::test_a_seller_matching_nothing_is_warned_about`
  - `tests/test_bandcamp_cli.py::test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues`
  - `tests/test_bandcamp_cli.py::test_strict_refuses_a_release_offered_only_lossy`
  - `tests/test_bandcamp_cli.py::test_what_went_wrong_since_the_queue_parks_the_resumed_job[a-library-unmounted-since-the-queue]`
  - `tests/test_bandcamp_cli.py::test_what_went_wrong_since_the_queue_parks_the_resumed_job[a-listing-bandcamp-cannot-answer]`
  - `tests/test_bandcamp_cli.py::test_what_went_wrong_since_the_queue_parks_the_resumed_job[a-listing-the-session-is-refused-at]`
  - `tests/test_bandcamp_cli.py::test_what_went_wrong_since_the_queue_parks_the_resumed_job[a-session-removed-since-the-queue]`

Old text:

```
        if sellers and purchase.seller.casefold() not in sellers:
```

New text:

```
        if False:
```

### `u177.B1_seller_by_label`

_sellers: take every name as an account, so --seller PULS plans nothing of pulsromania

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B1_seller_by_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_seller_by_label_name_fetches_only_that_labels_releases`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`

Old text:

```
        found.add(entry.bandcamp if entry is not None and entry.bandcamp else name.casefold())

```

New text:

```
        found.add(name.casefold())

```

### `u177.B9_untagged_refusal`

handle_fetch: drop the refusal naming the untagged files, so the item succeeds over them

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B9_untagged_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`

Old text:

```
    if untagged:
        raise refuse(

```

New text:

```
    if False:
        raise refuse(

```

### `u205.C4_rejected_token_kept`

app client: a token the API refused is sent again on every rung of the ladder, so an expired token refuses the run

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C4_rejected_token_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`

Old text:

```
            self._token = None
            raise AppCredentialsRejected(
```

New text:

```
            raise AppCredentialsRejected(
```

### `r289-b.B4_unknown_job_read_as_terminal`

Read a directory naming a job this queue does not hold as finished

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B4_unknown_job_read_as_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 367 against a baseline of 367
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone`

Old text:

```
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
```

New text:

```
        if states.get(job_dir.name, jobs.JobState.SUCCEEDED) not in jobs.TERMINAL_STATES:
```

### `r668-a.M2_resume_argv_carries_the_list`

the resume argv and the drive it with line name the frozen list again

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M2_resume_argv_carries_the_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`

Old text:

```
    return ["acquire", "download", "--job", job.job_id]
```

New text:

```
    return ["acquire", "download", str((job.payload or {}).get(LIST) or ""), "--job", job.job_id]
```

### `u108-c.G25_drive_maps_ending`

acquire_cli.drive_queued: a parked or half failed job is returned as if it ended clean

- File: `src/cratekit/acquire/cli.py`
- Source: `u108-c.json`, row `G25_drive_maps_ending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_label_sync_go.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 477 against a baseline of 477
- Kills: 31 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_while_a_go_resumed_another_refuses_the_resumes_tail`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_parked_by_a_rate_limit_names_its_own_go_for_after_the_park`
  - `tests/test_label_sync_go.py::test_a_go_resumed_under_another_run_names_the_run_that_queued_it_to_continue`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_names_its_own_go_to_continue_not_the_job`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_cancelled_still_refuses_and_lands_nothing`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - ... and 16 more, see the JSON sidecar

Old text:

```
    jobs.raise_for_state(job)
    return job, warnings
```

New text:

```
    return job, warnings
```

### `u42-author.C3_strict_consults_the_marker`

Make strict behave like the permissive policy, admitting a marked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C3_strict_consults_the_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 25 against a baseline of 25
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[no-marker-text-strict-still-fires]`
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[strict-reports-every-lossy-file-marked-or-not]`

Old text:

```
                if policy is LosslessPolicy.STRICT:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

New text:

```
                if policy is LosslessPolicy.STRICT and marker and not marked:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
```

### `u54-acquisition-worker.G10_absent_result`

Drop the refusal for a run that reported OK with no result for this key

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G10_absent_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_run_reporting_nothing_for_the_key_is_refused_rather_than_read_as_success`

Old text:

```
    if result is None:
        raise refuse(
            "unavailable-transient",
            f"{invocation.adapter} finished without reporting on {request.key}, "
            f"so nothing is known about it and it stays queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=("acquire.cli",),
            detail={"adapter": invocation.adapter, "key": request.key},
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G20_output_exists`

Replace a file already at the destination instead of refusing

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G20_output_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`

Old text:

```
    if final.exists():
```

New text:

```
    if False:
```

### `r703-a.D1_pool_reads_text`

classify_signal reads a NoFileLanded's carried words for block and rate limit markers

- File: `src/cratekit/acquire/download.py`
- Source: `r703-a.json`, row `D1_pool_reads_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_pacing.py`, `tests/test_provider_gate.py`
- Collected: 448 against a baseline of 448
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_paced_pool_reads_no_pacing_signal_off_the_carried_words[403 Client Error]`
  - `tests/test_adapter_contract.py::test_the_paced_pool_reads_no_pacing_signal_off_the_carried_words[429]`
  - `tests/test_adapter_contract.py::test_the_paced_pool_reads_no_pacing_signal_off_the_carried_words[Forbidden Fruit. File is corrupt!]`

Old text:

```
    if isinstance(exc, NoFileLanded):
        return ProviderSignal.NONE

```

New text:

```
(empty)
```

### `u80.F1_one_platform`

Only the first platform is searched, so YouTube is never asked

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F1_one_platform`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 7 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_accepted_upload_is_reported_with_its_url_and_not_searched`
  - `tests/test_acquire_fallback.py::test_an_outage_names_every_row_already_offered`
  - `tests/test_acquire_fallback.py::test_an_outage_on_the_first_row_says_nothing_was_offered`
  - `tests/test_acquire_fallback.py::test_no_candidate_anywhere_refuses_and_names_the_row`
  - `tests/test_acquire_fallback.py::test_one_track_with_and_without_a_key_is_searched_once`
  - `tests/test_acquire_fallback.py::test_ranked_candidates_are_offered_on_one_item`
  - `tests/test_acquire_fallback.py::test_the_same_line_twice_is_one_question`

Old text:

```
    for platform in PLATFORMS:
        answer = searcher.search(platform, query(wanted), SEARCH_LIMIT)
```

New text:

```
    for platform in PLATFORMS[:1]:
        answer = searcher.search(platform, query(wanted), SEARCH_LIMIT)
```

### `u81-fetch-b.L2_any_suffix`

The landing is not required to be MP3, so an unconverted upload is handed on

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `L2_any_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_never_reads_a_failure_as_a_file[not-mp3]`

Old text:

```
            if one.is_file() and one.suffix.lower() == FETCH_SUFFIX
```

New text:

```
            if one.is_file()
```

### `u80.C7_offered_not_named`

An outage no longer names the rows this run already offered

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80.json`, row `C7_offered_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_outage_names_every_row_already_offered`
  - `tests/test_acquire_fallback.py::test_one_track_with_and_without_a_key_is_searched_once`
  - `tests/test_acquire_fallback.py::test_ranked_candidates_are_offered_on_one_item`

Old text:

```
                if made.state == fallback.OFFERED:
                    offered_now.append(made)
```

New text:

```
                if made.state == fallback.OFFERED:
                    pass
```

### `u81-fetch-a.W7_final_unmarked`

The committed name ignores the policy decision and is never marked

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W7_final_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_lossy_file_lands_marked`
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_an_output_that_appears_during_the_download_is_refused_not_replaced`
  - `tests/test_acquire_fallback_fetch.py::test_artist_and_title_tags_come_from_the_row_not_the_upload_page`

Old text:

```
        Path(stem + landed.suffix), marker, required=decision.marker_required
```

New text:

```
        Path(stem + landed.suffix), marker, required=False
```

### `r1016.M10_wrong_endpoint`

The account walk asks the account's own created playlists endpoint, which leaves out the followed ones the listing has always served

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M10_wrong_endpoint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 793 against a baseline of 793
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listed_playlist_still_reads_its_tracks_through_the_playlist`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_adapter_listing.py::test_the_clients_own_account_listing_fetches_every_owned_playlist_again`

Old text:

```
ACCOUNT_PLAYLISTS_ENDPOINT = "users/%s/playlistsAndFavoritePlaylists"
```

New text:

```
ACCOUNT_PLAYLISTS_ENDPOINT = "users/%s/playlists"
```

### `r1016.M9_offset_not_sent`

The account request always asks for offset 0, so the walk reads its first page until the budget raises

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M9_offset_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 793 against a baseline of 793
- Kills: 10 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listed_playlist_still_reads_its_tracks_through_the_playlist`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_account_playlists_are_returned_unfiltered`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_keeps_the_playlists_the_account_created`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_pages_past_the_first_page`

Old text:

```
params={"limit": limit, "offset": offset})
```

New text:

```
params={"limit": limit, "offset": 0})
```

### `r878-a.A2_cursor_refuses_offset_rule`

paginate_cursor: drop the refusal of a shape that declares an offset rule

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A2_cursor_refuses_offset_rule`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_paginate_cursor_refuses_a_shape_that_walks_by_offset`

Old text:

```
    if stop is not StopRule.CURSOR:
```

New text:

```
    if False:
```

### `r878-b.B2_client_part_refusal`

_client_part: drop the refusal of a missing client part, so a moved request object is retried and slept on

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B2_client_part_refusal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_client_without_the_request_object_refuses_by_name_and_is_not_retried`
  - `tests/test_adapter_listing.py::test_a_user_without_the_parts_the_account_walk_reaches_is_refused_by_name`

Old text:

```
        if value is None:
            raise ListingNotPaginated(
                f"{type(owner).__name__} has no
```

New text:

```
        if False:
            raise ListingNotPaginated(
                f"{type(owner).__name__} has no
```

### `u65.A2_max_pages_gets_a_default`

the request budget becomes optional and effectively unbounded

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `A2_max_pages_gets_a_default`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_paginate_refuses_to_be_called_without_a_declared_rule_or_budget[max_pages]`

Old text:

```
    stop: StopRule,
    max_pages: int,
    declared_total
```

New text:

```
    stop: StopRule,
    max_pages: int = 1_000_000,
    declared_total
```

### `u65.C3_a_full_page_at_the_declared_end_stops_anyway`

a total that under reports now truncates, because the walk trusts it over what it sees

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C3_a_full_page_at_the_declared_end_stops_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_favourites_total_that_under_reports_does_not_truncate_the_walk`

Old text:

```
            if offset >= total and len(page) < page_size:
```

New text:

```
            if offset >= total:
```

### `u65.E4_the_playlist_total_is_never_wired`

the playlist count on the object is ignored, so that shape degrades too

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E4_the_playlist_total_is_never_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`

Old text:

```
    kwargs.setdefault("declared_total", _declared_attribute(playlist, "num_tracks"))
```

New text:

```
    kwargs.setdefault("declared_total", lambda: None)
```

### `r679-b.B5_rule_not_recorded`

retire_questions: record a fixed rule instead of the why that owned the row

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B5_rule_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        rule=str(found.why),
```

New text:

```
        rule="exact",
```

### `u213.M5_listed_names_artist`

listed_names: read no artist off a refused row

- File: `src/cratekit/acquire/match_list.py`
- Source: `u213.json`, row `M5_listed_names_artist`
- Moved: the same text, now in src/cratekit/acquire/match_list.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_match_states.py::test_listed_names_reads_a_row_the_reader_refuses`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)
```

New text:

```
    return str(_field(row, "id", "")).strip(), "", _raw_title(row)
```

### `r703-a.LF1_plain_runtime_error`

landed_file raises a plain RuntimeError, so the classifier reads the carried words

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `LF1_plain_runtime_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`

Old text:

```
        raise NoFileLanded(message, cause=cause) from (
```

New text:

```
        raise RuntimeError(message) from (
```

### `r703-b.L4_error_notes_nothing`

error() goes back to discarding, so a message only failure has no cause

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `L4_error_notes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_failure_message_with_no_exception_is_the_cause`
  - `tests/test_adapter_contract.py::test_a_mapping_argument_renders_the_way_logging_would`

Old text:

```
    def error(self, *args: object, **_kwargs: object) -> None:
        self._failure(args)
```

New text:

```
    def error(self, *args: object, **_kwargs: object) -> None:
        return None
```

### `r703-c.C2_message_outranks_exception`

Batch B's L3 again after its test: the cause prefers the tool's message over the provider's exception

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-c.json`, row `C2_message_outranks_exception`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_providers_exception_outranks_a_message_the_tool_logged_first`

Old text:

```
        return self._exception if self._exception is not None else self._message
```

New text:

```
        return self._message if self._message is not None else self._exception
```

### `u47-author.CODEC_refusal_drops_the_codec_name`

Reword the refusal so it no longer names the codec that actually arrived, leaving the reader with a refusal and no fact

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_refusal_drops_the_codec_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_is_refused_and_the_refusal_names_the_codec`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`

Old text:

```
            f"the provider was asked for lossless audio and the file that landed "
            f"for {key} is {name}; it is at {path}"
```

New text:

```
            f"the file that landed for {key} was refused by the lossless policy"
```

### `u47-author.R196_no_stored_session_proceeds`

Proceed when there is no stored session at all

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_no_stored_session_proceeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored3-False-True]`

Old text:

```
    if not had_stored_session:
        return "there is no stored provider session to authenticate with"
```

New text:

```
(empty)
```

### `u47-author.R197_progress_enabled`

Render the progress bars, so tool chatter reaches a stream a caller may be parsing (R32)

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_progress_enabled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`

Old text:

```
    return Progress(disable=True), Progress(disable=True)
```

New text:

```
    return Progress(disable=False), Progress(disable=False)
```

### `u254.M04_cache_identity_no_mtime`

_as_left: leave the modification time out of the identity

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M04_cache_identity_no_mtime`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)
```

New text:

```
    return (found.st_dev, found.st_ino, found.st_size, 0)
```

### `u254.M13_header_older_version`

_read_journal: accept a journal header at a schema no build wrote as a journal

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M13_header_older_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header with an older version]`

Old text:

```
    if version != SCHEMA_VERSION:
```

New text:

```
    if version > SCHEMA_VERSION:
```

### `u254.M21_record_needs_actor`

_record_from: drop actor from the fields every record must carry

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M21_record_needs_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a record missing its actor, last]`
  - `tests/test_adoption.py::test_a_wrong_applied_ledger_refuses_rather_than_reading_as_empty[11]`

Old text:

```
    for name in ("entry", "tree", "content", "actor"):
```

New text:

```
    for name in ("entry", "tree", "content"):
```

### `r731-b.M15_gate_without_the_read_state`

the gate's facts no longer say whether the tree was read

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M15_gate_without_the_read_state`
- Moved: the gate's facts are now read through the _FACTS key list; dropping placements from it is the same omission
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncut_library_reads_neither_its_tree_nor_its_vocals`

Old text:

```
    "collisions",
    "placements",

```

New text:

```
    "collisions",

```

### `u27-adopt-apply-author.A2_gate_found_by_position`

Take the first declared gate rather than the one digested against the plan

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A2_gate_found_by_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_cli_contract.py`
- Collected: 1037 against a baseline of 1037
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`

Old text:

```
    for spec in entry.gates:
        if spec.digest_source == "plan":
            return spec
```

New text:

```
    for spec in entry.gates:
        if True:
            return spec
```

### `u55-collection-reader.R20_membership_locations_key`

The written mapping groups content identifiers, so the write matches nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R20_membership_locations_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 9 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`

Old text:

```
        grouped.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
        grouped.setdefault((folder, sub), []).append(entry.content_id)
```

### `u23-round-8-independent.X2_approval_option_unchecked`

A recorded answer that is not the approve option is accepted

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X2_approval_option_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_recorded_answer_that_is_not_an_approval_applies_nothing`

Old text:

```
    if approval.option != APPROVE:
```

New text:

```
    if approval.option is None:
```

### `r758-b.M3_renamed_playlist_is_moved_from`

a sub held through a renamed playlist only is planned for a move the writer cannot make

- File: `src/cratekit/adopt/move.py`
- Source: `r758-b.json`, row `M3_renamed_playlist_is_moved_from`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[under-another-name]`

Old text:

```
    if unnamed:
        return LEFT_UNNAMED

```

New text:

```
(empty)
```

### `r780-a.A8_double_listed_beside_a_move`

a doubled target is listed as left beside the move that keeps it, so one track reads as both moved and left in one bucket

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A8_double_listed_beside_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_doubled_target_beside_a_stale_sub_is_a_move_and_the_double_is_listed_after`

Old text:

```
                if isinstance(found, Move):
                    moves.append(found)
                    continue

```

New text:

```
                if isinstance(found, Move):
                    moves.append(found)

```

### `u118-c.M4_held_split_none`

No unclaimed Soul track in a split place is listed

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M4_held_split_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 189 against a baseline of 189
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`
  - `tests/test_adopt_split_place.py::test_an_unreadable_soul_file_in_r_and_b_is_listed_under_soul_and_not_moved`

Old text:

```
    if not split or claims(entry, bucket) or not genre_names(entry, bucket, declared):
        return ()
```

New text:

```
    if True:
        return ()
```

### `r758-b.C5_a_sub_nobody_was_shown_is_removed`

a track filed in a further sub since the approval has that sub removed as well

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C5_a_sub_nobody_was_shown_is_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_filed_somewhere_nobody_was_shown_is_a_stale_decision`

Old text:

```
        if set(now.remove) - set(move.remove):
            stale[move.content_id] = "it holds a sub nobody was shown"
            continue

```

New text:

```
(empty)
```

### `r731-b.M16_skewed_registry_raises_at_the_plan`

a registry naming a root the library lacks raises out of the reader instead of answering unread

- File: `src/cratekit/adopt/placements.py`
- Source: `r731-b.json`, row `M16_skewed_registry_raises_at_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[no-such-root]`

Old text:

```
        except (tree_registry.TreeModeRefused, tree_registry.RegistrySkew):
```

New text:

```
        except tree_registry.TreeModeRefused:
```

### `r788-c.L9_every_library_is_calibrated`

vocal_standing: any library with a vocal sub stands, so an uncalibrated one files from its tags

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L9_every_library_is_calibrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_calibration_that_cannot_be_read_refuses_before_the_library_is_walked`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`

Old text:

```
    return metadata_cli.load_vocal_threshold(cfg) is not None
```

New text:

```
    return True
```

### `r722.P1_level_none`

The original defect: _sub_for resolves with a level of None for every track

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P1_level_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 651 against a baseline of 651
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_changed_reading_moves_the_digest`
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_adoption_lands_a_track_where_the_routing_pass_would`

Old text:

```
    sub = routing.energy_sub(declared, bucket_id, level, source_genre=genre)
```

New text:

```
    sub = routing.energy_sub(declared, bucket_id, None, source_genre=genre)
```

### `r731-a.M03_same_sub_withheld`

a track already in the sub the plan names is withheld instead of left to the writer

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M03_same_sub_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_already_in_the_sub_the_plan_names_is_not_withheld`
  - `tests/test_adopt_placements.py::test_a_track_holding_a_place_is_withheld_only_where_it_competes[two-bands-one-the-plan-names]`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if not held or (sub in held and sub not in unnamed):
```

New text:

```
    if not held:
```

### `r731-b.M23_collision_counts_a_listed_track`

a track the plan withheld and listed is counted a stranger in its own folder

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-b.json`, row `M23_collision_counts_a_listed_track`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_the_plan_withheld_is_not_a_stranger_in_its_own_folder`

Old text:

```
            - planned_by_bucket[bucket_id]
            - named_by_bucket.get(bucket_id, set())
```

New text:

```
            - planned_by_bucket[bucket_id]
```

### `r788-b.P14_digest_drops_vocal`

digest: no vocal membership is covered, so a plan that gained vocal additions after the approval is applied under it

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P14_digest_drops_vocal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_the_digest_changes_when_a_vocal_membership_is_added_to_the_plan`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
                "vocal": [vocal_id(entry) for entry in self.vocal_memberships()],
```

New text:

```
                "vocal": [],
```

### `u956.O14_digest_blind_to_outside`

AdoptionPlan.digest: leave the outside rows out, so an approval stands over a screen that names other rows

- File: `src/cratekit/adopt/plan.py`
- Source: `u956.json`, row `O14_digest_blind_to_outside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 685 against a baseline of 685
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_digest_moves_when_a_different_row_is_left_outside`

Old text:

```
                "outside_root": [outside_row(entry) for entry in self.outside_root()],
            }
```

New text:

```
            }
```

### `u23-round-8-independent.A5_at_risk_drops_this_call`

The value THIS call is about to write no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A5_at_risk_drops_this_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,),)

```

### `u23-round-8-independent.E1_vacancy_is_mere_absence`

Round 7 restored: an unmounted volume reads as a deleted file

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E1_vacancy_is_mere_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
    recorded = Path(record.path)
    try:
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
    except OSError:
        return False

```

New text:

```
    recorded = Path(record.path)
    try:
        return not recorded.exists()
    except OSError:
        return False

```

### `r759.A2_deadline_a_second_late`

the read deadline is honoured a second after it passes, so a trickling file is read fifty blocks further than the caller allowed

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r759.json`, row `A2_deadline_a_second_late`
- Moved: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`
- Collected: 1 against a baseline of 1
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_deadline_ends_a_read_that_keeps_arriving_forever`

Old text:

```
                if time.monotonic() > give_up_at:
                    raise TimeoutError(

```

New text:

```
                if time.monotonic() > give_up_at + 1.0:
                    raise TimeoutError(

```

### `u956.O11_no_samefile_walk`

within_root: ask by name only, so a volume that folds case or a name linked to the root reads every row outside it

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O11_no_samefile_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 639 against a baseline of 639
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/anything/at/all.flac-/-True]`
  - `tests/test_adopt_outside_root.py::test_within_root_reaches_the_root_through_a_name_that_is_the_same_directory`

Old text:

```
            if os.path.samefile(parent, anchor):
```

New text:

```
            if False:
```

### `u956.O9_path_not_composed`

within_root: compare the path's own composition form, so a decomposed accent reads outside an accented root

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O9_path_not_composed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 639 against a baseline of 639
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/vol/lib/Cafe\u0301/a.flac-/vol/lib/Caf\xe9-True]`

Old text:

```
    wanted = posixpath.normpath(locations.norm_for_compare(str(path)))
```

New text:

```
    wanted = posixpath.normpath(str(path))
```

### `u241.M15_identity_without_the_time`

ahead.identity_of: no modification time, so a file rewritten at the same length keeps its old head

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M15_identity_without_the_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_changed_after_its_head_was_measured_is_measured_again[same-length-by-its-time]`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)

```

New text:

```
    return (found.st_dev, found.st_ino, found.st_size, 0)

```

### `u223.M23_intent_link_followed`

rename_intent: read an intent that is a link

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M23_intent_link_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_or_report_is_never_read_as_the_twin`

Old text:

```
    path = intent_path(cfg, job.job_id, item.ordinal)
    if path.is_symlink() or not path.is_file():
```

New text:

```
    path = intent_path(cfg, job.job_id, item.ordinal)
    if not path.is_file():
```

### `u223.M8_report_not_mapping`

staged_report: drop the mapping check, so a list report raises

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M8_report_not_mapping`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    if loaded.get("item") != item.item_id:
        return None
    return loaded
```

### `u90-a.A5_min_coefficient`

The score range's bottom moved from 0 to minus 1

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A5_min_coefficient`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`

Old text:

```
VOCAL_SCORE_MIN = 0.0
```

New text:

```
VOCAL_SCORE_MIN = -1.0
```

### `u90-b.B7_fit_detail_drops_old_cut`

The fit's check detail stops naming the cut it replaced

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B7_fit_detail_drops_old_cut`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`

Old text:

```
        f"written to {target}; {before}",
```

New text:

```
        f"written to {target}",
```

### `u94-a.S5_recursive_not_required`

_partial_before_walk: treat the root read one level deep as the whole library, so only its loose files are fitted and the check says ok

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S5_recursive_not_required`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_root_read_one_level_deep_is_partial_and_names_the_flag`
  - `tests/test_analysis_workers.py::test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag`

Old text:

```
    if wide and recursive:
        return None
```

New text:

```
    if wide:
        return None
```

### `u94-b.W6_outcome_energy_only`

analyze_calibrate: derive the outcome from the energy half alone, so a run that replaced only the vocal cut answers no_op

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W6_outcome_energy_only`
- Moved: the calibrate verb's body moved from analysis/cli.py to analysis/calibrate.py, a file the base did not hold, and the text occurs once there
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_run_where_only_the_vocal_half_wrote_does_not_answer_no_op`

Old text:

```
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK if calibrated else Outcome.NO_OP,
```

### `u94-c.N7_root_not_required_first`

analyze_calibrate: ask the folder's standing with the library away, so an unmounted volume is blamed on the folder

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N7_root_not_required_first`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_calibrate_refuses_with_the_library_away_rather_than_writing_beside_the_mount`

Old text:

```
    _require_library_root(cfg)
    partial = _partial_before_walk
```

New text:

```
    partial = _partial_before_walk
```

### `u223.M13_resumed_unchecked`

_staged_twin: accept any prefixed skip, not only a resume's

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M13_resumed_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    elif status != "skipped-prefixed" or report.get("resumed_after_rename") is not True:
```

New text:

```
    elif status != "skipped-prefixed":
```

### `u241.M25_an_idle_resume_overwrites_the_pool`

_worth_recording: a drive that measured nothing overwrites the record of the drive that did

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M25_an_idle_resume_overwrites_the_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`

Old text:

```
        return True
    return artifacts.pool_record(cfg, job_id) is None

```

New text:

```
        return True
    return True

```

### `u343.M04_untitled_never_titles`

_untitled: answer None for every file, so a file with no title tag lands with nothing adopt can stamp (round one's blocking finding)

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M04_untitled_never_titles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_restamp_scored_by.py`
- Collected: 323 against a baseline of 323
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-lossy-marked-first]`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-the-stem]`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`

Old text:

```
    return naming.render_all(spec, template=template).title_tag or None
```

New text:

```
    return None
```

### `u58-workers-and-wav.R7_absent_energy_stamped`

Write a level for an absent energy

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R7_absent_energy_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`

Old text:

```
        "energylevel": scored.get("energy"),
```

New text:

```
        "energylevel": scored.get("energy") or 5,
```

### `u263.D13_extensible`

_parse_float_wav: read the extensible tag without its sub format

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D13_extensible`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[broken-png]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[gif-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[webp-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[1]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[2]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[6]`
  - `tests/test_analysis_decode.py::test_a_path_with_a_colon_is_read_as_a_file`
  - `tests/test_analysis_decode.py::test_the_decode_writes_no_file`
  - `tests/test_analysis_decode.py::test_the_extensible_header_and_a_chunk_before_the_data_are_read`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_taken_even_when_another_is_the_default`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_the_one_decoded`

Old text:

```
            if fmt_tag == _WAVE_FORMAT_EXTENSIBLE:
                (fmt_tag,) = struct.unpack("<H", blob[body + 24 : body + 26])
```

New text:

```
(empty)
```

### `u263.D7_stderr_fails`

_ffmpeg_samples: trust the exit code alone, so a mid file error yields the first half

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D7_stderr_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_an_m4a_damaged_in_the_middle_fails_rather_than_yielding_its_first_half[aac]`
  - `tests/test_analysis_decode.py::test_an_m4a_damaged_in_the_middle_fails_rather_than_yielding_its_first_half[alac]`

Old text:

```
    if proc.returncode != 0 or said:
```

New text:

```
    if proc.returncode != 0:
```

### `u264.M2_leading_zero_dropped`

_mean_of_two: drop the plus zero numpy's reduction starts from, so two minus zero channels mix to minus zero

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M2_leading_zero_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0--0.0-00000000-00000000]`

Old text:

```
    out = np.add(stereo[0], stereo[1])
    # numpy's reduction starts from plus zero: minus zero plus minus zero is
    # minus zero here and plus zero in the mean, and no other sum changes.
    out += out.dtype.type(0)
```

New text:

```
    out = np.add(stereo[0], stereo[1])
```

### `u344.M11_centre_read_from_top`

centred: read a file libsndfile opens from its top, not its centre, so run and restamp measure different audio than they did

- File: `src/cratekit/analysis/decode.py`
- Source: `u344.json`, row `M11_centre_read_from_top`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_warm.py`, `tests/test_energy_one_measure_librosa.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 552 against a baseline of 552
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_file_libsndfile_reads_is_one_windowed_load[the-centre-of-a-file-is-one-windowed-load]`

Old text:

```
    return load(path, rate, offset=_centre(length, seconds), duration=seconds)
```

New text:

```
    return load(path, rate, offset=0.0, duration=seconds)
```

### `u58-workers-and-wav.E2_uncalibrated_measured`

Measure energy with no calibration instead of reporting uncalibrated

- File: `src/cratekit/analysis/detect.py`
- Source: `u58-workers-and-wav.json`, row `E2_uncalibrated_measured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_detector_names_why_energy_is_what_it_is`

Old text:

```
    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED

```

New text:

```
(empty)
```

### `u327.A16_before_values_recorded`

apply_adopt: keep no surface's old value in the session record

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A16_before_values_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_old_values_are_on_disk_before_the_first_file_is_written`
  - `tests/test_analyze_adopt.py::test_the_record_keeps_every_surface_s_old_value_for_a_restore`

Old text:

```
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes]

```

New text:

```
(empty)
```

### `u327.A7_not_analysed_left`

plan_row: drop the not analysed guard, so a row rekordbox has not analysed is planned off its unread columns

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A7_not_analysed_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`

Old text:

```
    if judged.action != analyzed.CLEAR:
```

New text:

```
    if False:
```

### `u342.P2_unanswered_named`

plan_row: name a headless row rekordbox did not fully answer as no-head, losing why

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P2_unanswered_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_row_rekordbox_did_not_key_or_time_is_left_and_named`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`

Old text:

```
            return Item(content_id, LEAVE_ACTION, reason=NO_HEAD_UNANSWERED, **common)
```

New text:

```
            return Item(content_id, LEAVE_ACTION, reason=NO_HEAD, **common)
```

### `u327.B3_partial_apply_refuses`

analyze_adopt: end a run whose files did not all take as ok

- File: `src/cratekit/analysis/head_adopt_cli.py`
- Source: `u327.json`, row `B3_partial_apply_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_that_cannot_be_written_keeps_its_row_s_title_and_is_named`
  - `tests/test_analyze_adopt.py::test_a_file_that_does_not_read_back_keeps_its_row_s_title_and_is_named`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`

Old text:

```
    if written is None or not (written.files.failed or written.files.wrong):
```

New text:

```
    if True:
```

### `u275.M2_slope_back_to_linux`

LIGHT_BYTES_PER_SECOND back to U241's 1.5 megabytes a second, under every Mac peak

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M2_slope_back_to_linux`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 553 against a baseline of 553
- Kills: 19 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[376-1281]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[576-1805]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[668-2105]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[690-2162]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
```

New text:

```
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024 // 2
```

### `u343.M09_resume_reads_the_mark_alone`

already_analyzed: read only the mark, so a file a run before U343 named is measured again

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M09_resume_reads_the_mark_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`, `tests/test_analysis_ahead.py`
- Collected: 501 against a baseline of 501
- Kills: 10 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_killed_batch_resumes_skipping_completed_tracks`
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_vocals_cli.py::test_a_rescore_job_that_does_not_succeed_ends_the_chain_at_the_analyze_step`
  - `tests/test_vocals_cli.py::test_analyze_run_still_skips_a_prefixed_file`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_scores_a_headed_file_with_no_score_and_leaves_a_scored_one`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_headed_file_with_no_score_and_leaves_the_rest_alone`
  - `tests/test_vocals_cli.py::test_unscored_reads_the_head_by_the_rule_analyze_run_skips_by`

Old text:

```
    return has_head(path.name, template=template) or marked(path)
```

New text:

```
    return marked(path)
```

### `sitting3.G1_columns_by_number`

Read the first three columns whatever the label table says, the R-370 defect

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G1_columns_by_number`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis.py::test_class_indices_resolve_the_singing_columns_by_name`
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    labels = getattr(model, "labels", None)
    if labels is None:
        raise ValueError(

```

New text:

```
    labels = getattr(model, "labels", None)
    if True:
        return (0, 1, 2)
        raise ValueError(

```

### `sitting3.G12_columns_per_track`

Resolve the columns per track after the decode instead of once at load

- File: `src/cratekit/analysis/vocals.py`
- Source: `sitting3.json`, row `G12_columns_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`

Old text:

```
        _VOCAL_COLUMNS = class_indices(model)
        _VOCAL_MODEL = model

```

New text:

```
        _VOCAL_COLUMNS = None
        _VOCAL_MODEL = model

```

### `u58-zero-row-remeasured.W6_gender_constant`

Report every scored track's gender as U

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-zero-row-remeasured.json`, row `W6_gender_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
    result["voxgender"] = score.gender
```

New text:

```
    result["voxgender"] = "U"
```

### `u92-author.G8_refused_file_tagged_zero`

Tag the refused file voxlevel 0 the way the source system did, instead of leaving an absence

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G8_refused_file_tagged_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 230 against a baseline of 230
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
    if is_oversize(result.get("path")):
        result = _inactive(result, REASON_AUDIO_TOO_LARGE)
        result["voxlevel"] = 0
        result["voxgender"] = "U"
        result["voxgenderconf"] = 0
        return result

```

### `r221-a.W4_twin_branch_warning_dropped`

A second ask reports the open rehearsal as the backup the person asked for, with nothing saying it is one

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W4_twin_branch_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
                    *_rehearsal(twin),
                ),
            )
```

New text:

```
                ),
            )
```

### `r222-b.B12_warnings_from_the_live_configuration`

Describe the reported job from the configuration on disk rather than the one it was frozen against

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B12_warnings_from_the_live_configuration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
            described = cfg if frozen is None else frozen
```

New text:

```
            described = cfg
```

### `r222-b.B7_unreadable_is_elsewhere`

Read a frozen configuration that cannot be rebuilt as somewhere else, and file a second job beside it

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B7_unreadable_is_elsewhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`

Old text:

```
        except (config.ConfigError, ValueError):
            return job, None
```

New text:

```
        except (config.ConfigError, ValueError):
            continue
```

### `r757-c2.S6_twin_in_the_other_mode_says_nothing`

_already_queued: drop the sentence saying the open job runs the other comparison, the review's fix

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S6_twin_in_the_other_mode_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
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

### `u45-round-1.C5_first_refusal_taken`

Take the first portion's refusal when the reasons differ, rather than naming all of them

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C5_first_refusal_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if len(refusals) == 1:
```

New text:

```
    if refusals:
```

### `u45-round-1.R2_slug_flattened`

Fold every engine refusal into one slug, so nine diagnoses arrive as one and each loses its own fix

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R2_slug_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    slug = str(refusal)
    return CratekitError(
```

New text:

```
    slug = str(backup.Refusal.RCLONE_MISSING)
    return CratekitError(
```

### `u45-round-2.C7_failed_detail_dropped`

Reword the transfer-failed message so it no longer says a destructive session still sees the previous age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-2.json`, row `C7_failed_detail_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_transfer_failure_says_no_age_was_published`

Old text:

```
            + ". No backup age was published for that portion, so a destructive "
            "session still sees whatever the last successful run left",
```

New text:

```
            + ". The run stopped there.",
```

### `u50-zero-rows.W4b_item_ignored_entirely`

Back up the mirror whatever the item says, so every item of the job does the same half

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `W4b_item_ignored_entirely`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 12 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    named = str(item.item_id or "")
```

New text:

```
    named = str(backup_facts.Portion.FILES)
```

### `r757-c2.D1_due_a_day_late`

_check_full_comparison: say to run one only past the bound and not at it

- File: `src/cratekit/cli/doctor_backup.py`
- Source: `r757-c2.json`, row `D1_due_a_day_late`
- Moved: the same text, now in src/cratekit/cli/doctor_backup.py, was in src/cratekit/cli/doctor.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
    due = f". {run_one}" if days >= FULL_COMPARISON_DUE_DAYS else ""
```

New text:

```
    due = f". {run_one}" if days > FULL_COMPARISON_DUE_DAYS else ""
```

### `r925.J3_field_not_set`

job show computes the tracks and never puts them on the envelope

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J3_field_not_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_job_of_another_handler_lists_no_tracks_and_is_not_driven_under_this_envelope`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`

Old text:

```
    if tracks is not None:
        summary[TRACKS_FIELD] = tracks
```

New text:

```
    if tracks is None:
        summary[TRACKS_FIELD] = tracks
```

### `r678-a.A1_drop_the_job_state_case`

the original defect for the three queueing verbs: render never asks for the job

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A1_drop_the_job_state_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 9 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_render_payloads.py::test_a_builder_that_raises_leaves_the_queued_verb_a_success`
  - `tests/test_render_payloads.py::test_a_verb_showing_a_queued_job_it_did_not_queue_names_no_drive`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_prints_the_settled_job_and_no_drive_command`

Old text:

```
    lines += render_job_state(envelope, drive=drive)

```

New text:

```
(empty)
```

### `r685-a.L3_a_copy_that_does_not_parse_falls_back`

An active copy that fails validation is replaced by the shipped template instead of refused

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L3_a_copy_that_does_not_parse_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_rebuild.py`
- Collected: 130 against a baseline of 130
- Kills: 5 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_breaks_after_a_good_load_refuses`
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-a-taxonomy]`
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-toml]`
  - `tests/test_active_taxonomy.py::test_a_copy_that_does_not_parse_refuses_on_every_load`
  - `tests/test_rebuild.py::test_an_active_taxonomy_that_cannot_be_read_is_not_compared_and_opens_nothing`

Old text:

```
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        raise refuse(

```

New text:

```
    try:
        return taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return _shipped(cfg.taxonomy.template)
        raise refuse(

```

### `u260.E10_encode_memory_unbounded`

COVER_MEMORY: a hundred entries

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E10_encode_memory_unbounded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_shipped_encode_memory_is_bounded`

Old text:

```
COVER_MEMORY = 4
```

New text:

```
COVER_MEMORY = 100
```

### `u260.E7_encode_bound_off_by_one`

to_cdj_jpeg_remembered: keep one entry more than the bound

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E7_encode_bound_off_by_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest`

Old text:

```
        while len(_remembered) > COVER_MEMORY:
```

New text:

```
        while len(_remembered) > COVER_MEMORY + 1:
```

### `u83-a.E4_cap_inclusive`

The encoder's cap comparison becomes exclusive

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E4_cap_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
        if len(encoded) <= max_bytes:
```

New text:

```
        if len(encoded) < max_bytes:
```

### `u83-a.R4_full_decode`

The measure drops its full decode, so a truncated picture that opens cleanly reads as decoded

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R4_full_decode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_truncated_picture_does_not_read_as_decoded`

Old text:

```
            img.load()

```

New text:

```
(empty)
```

### `u83-b.W5b_cap_inclusive`

The writer's cap becomes exclusive while the encoder's stays inclusive, so a picture encoded exactly to the cap is refused

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W5b_cap_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_picture_over_the_cap_is_refused_and_the_file_untouched`

Old text:

```
    if len(jpeg) > max_bytes:
```

New text:

```
    if len(jpeg) >= max_bytes:
```

### `r757-b2.F2_first_record_erases_the_implied_date`

record: write null where an earlier build's file implied a full comparison

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F2_first_record_erases_the_implied_date`
- Moved: U953 folded the two implied date readings of record into one loop over the held keys, so writing null for the full comparison key alone is the same erased date as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 727 against a baseline of 727
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison`

Old text:

```
            held[key] = _as_held(read.get(Portion.FILES))
```

New text:

```
            held[key] = None if key == FULL_COMPARISON_KEY else _as_held(read.get(Portion.FILES))
```

### `example-binaries-five-row.B4_unknown_source_remedy`

Collapse the two None-hint cases onto one remedy token, which is the exact distinction the docstring says must not live in a None-check on a second attribute.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B4_unknown_source_remedy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
        remedy=Remedy.INSTALL_BINARY if hint is not None else Remedy.INSTALL_BINARY_SOURCE_UNKNOWN,

```

New text:

```
        remedy=Remedy.INSTALL_BINARY,

```

### `u27-reports-round-1.R2_governed_tree_code`

Move the governed-tree refusal off the library-prerequisite code

- File: `src/cratekit/core/cause.py`
- Source: `u27-reports-round-1.json`, row `R2_governed_tree_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5113 against a baseline of 5113
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
        "governed-tree-absent": ExitCode.LIBRARY_PREREQUISITE,
```

New text:

```
        "governed-tree-absent": ExitCode.PRECONDITION,
```

### `u197.M2_retired_mapping_empty`

RETIRED_ADAPTER_NAMES: forget the vendored downloader's old key, so an older configuration names an unknown adapter

- File: `src/cratekit/core/config_schema.py`
- Source: `u197.json`, row `M2_retired_mapping_empty`
- Moved: Anchored where u299-replay-after-10.json replayed it: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_adapter_contract.py`
- Collected: 828 against a baseline of 828
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_retired_vendored_key_resolves_to_the_same_adapter`
  - `tests/test_config.py::test_a_file_naming_the_retired_adapter_key_reads_back_as_the_current_one`
  - `tests/test_config.py::test_only_a_retired_adapter_key_is_folded`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`

Old text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({"tidal_dl_ng": "vendored"})
```

New text:

```
RETIRED_ADAPTER_NAMES: Mapping[str, str] = MappingProxyType({})
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Moved: Anchored where u325-replay-after.json replayed it: U298 replaced the resume tails of tagging.shell.advance, adopt.shell.advance, acquire fallback-fetch and master with core.jobs.resumed, which advance calls; its one raise_for_state call is the mapping each of those four shells made, and tests/test_job_outcome.py names that function as the shared tail. The tests are this row's own plus those of the three rows mapped to it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_adopt_workers.py`, `tests/test_master_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 349 against a baseline of 349
- Kills: 48 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[master]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.folder]`
  - ... and 33 more, see the JSON sidecar

Old text:

```
    raise_for_state(job)
    return job, warnings
```

New text:

```
    get  # the mapping call, removed
    return job, warnings
```

### `u169.E2_drive_fails_a_decline`

drive: no Declined clause, so a declined item falls to the failure boundary and fails the job

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E2_drive_fails_a_decline`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 153 against a baseline of 153
- Kills: 11 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_job_every_item_of_which_was_declined_succeeds_rather_than_failing`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
                except Declined as exc:
```

New text:

```
                except Parked as exc:
```

### `u39-author-full.E2_wheel_bound_widened`

Existing guard sample: the Camelot number bound admits 13 through 19

- File: `src/cratekit/core/naming.py`
- Source: `u39-author-full.json`, row `E2_wheel_bound_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1487 against a baseline of 1487
- Kills: 10 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_off_wheel_key_is_rejected_rather_than_normalized[13A]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[bare]`
  - `tests/test_naming.py::TestRender::test_an_unwritable_key_is_refused_rather_than_emitted[default]`
  - `tests/test_naming.py::TestSplitAndPadHead::test_split[refuses-unwritable-head]`
  - `tests/test_naming.py::TestTheDeletedDuplicate::test_it_accepted_off_wheel_and_lowercase_keys[off-wheel-13]`
  - `tests/test_naming.py::TestTrailingHead::test_strip_trailing_head[same-wheel-bound]`
  - `tests/test_naming.py::test_is_camelot_agrees_with_parse_camelot`
  - `tests/test_naming.py::test_pad_camelot_normalizes_and_refuses`
  - `tests/test_naming.py::test_parse_and_strip_head[13 is off the wheel]`
  - `tests/test_naming.py::test_parse_camelot[13A]`

Old text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-2])"

```

New text:

```
_CAMELOT_NUMBER = r"(?:[1-9]|1[0-9])"

```

### `u205.G7_process_spend_drops_app`

process spend: the app's share of this process's calls is not reported, so the spend line says every call was the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G7_process_spend_drops_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`

Old text:

```
        app_calls=_PROCESS_APP_CALLS,
```

New text:

```
        app_calls=0,
```

### `r239-a.A4_open_default_true`

open_db's unlock default back to True, so the probe branch never fires for an unnamed open

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A4_open_default_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 121 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_the_database_file_is_byte_identical_after_a_full_read`
  - `tests/test_adopt_collection.py::test_the_reader_never_opens_the_database_for_writing`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_collection.py::test_two_reads_in_one_process_open_the_database_once`
  - `tests/test_deletion.py::test_delete_review_abort_moves_nothing`
  - `tests/test_deletion.py::test_delete_review_exits_ok_after_the_recorded_decision`
  - `tests/test_deletion.py::test_delete_review_first_run_confirmed_reports_ok_and_trashes_nothing`
  - `tests/test_deletion.py::test_delete_review_honours_a_reject_recorded_before_the_gate`
  - `tests/test_deletion.py::test_delete_review_prints_the_baseline_to_a_person_not_only_to_json`
  - `tests/test_deletion.py::test_delete_review_refuses_an_inline_answer_and_does_not_record_it`
  - `tests/test_deletion.py::test_delete_review_refuses_at_its_explicit_gate`
  - `tests/test_deletion.py::test_delete_review_says_on_the_refusal_that_a_first_run_accepted_history`
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - ... and 106 more, see the JSON sidecar

Old text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = None,

```

New text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = True,

```

### `r797-a.T8_competes_in_a_band_bucket`

competing_subs: leave former places out of a bucket split by energy, so adoption files a band beside the old playlist

- File: `src/cratekit/core/routing.py`
- Source: `r797-a.json`, row `T8_competes_in_a_band_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`, `tests/test_routing_parity.py`
- Collected: 1097 against a baseline of 1097
- Kills: 28 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_competes_where_it_is_declared_and_where_it_sits_and_nowhere_else`
  - `tests/test_adopt_former_place.py::test_a_genre_only_the_fallback_tier_lands_is_not_read_as_naming_the_bucket`
  - `tests/test_adopt_former_place.py::test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision[Afrobeat]`
  - `tests/test_adopt_former_place.py::test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision[Deep House]`
  - `tests/test_adopt_former_place.py::test_a_genre_that_left_the_promoted_bucket_since_the_approval_is_a_stale_decision[]`
  - `tests/test_adopt_former_place.py::test_a_move_whose_target_is_a_former_place_is_refused_and_nothing_is_written`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_leaves_it_for_the_band_its_reading_names[already-in-it]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_leaves_it_for_the_band_its_reading_names[and-a-stale-band]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_leaves_it_for_the_band_its_reading_names[its-band]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_leaves_it_for_the_band_its_reading_names[no-reading-in-the-sink]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_leaves_it_for_the_band_its_reading_names[no-reading]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[another-folder]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[no-genre]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    return Competing.BAND, frozenset((found | former) - classes)
```

New text:

```
    return Competing.BAND, frozenset(found - classes)
```

### `r722.T1_checked_is_lenient`

read_tags_checked runs the lenient body

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T1_checked_is_lenient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2990 against a baseline of 2990
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read_and_reads_as_none_beside_its_neighbours`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    return _read_tags(path, fields, strict=True)
```

New text:

```
    return _read_tags(path, fields, strict=False)
```

### `u247.M5_failure_remembered`

_parsed: remember a text that is not TOML as its refusal, raised again from the memo without a parse

- File: `src/cratekit/core/taxonomy.py`
- Source: `u247.json`, row `M5_failure_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_does_not_parse_refuses_on_every_load`
  - `tests/test_taxonomy.py::test_a_text_that_does_not_load_raises_on_every_call[not-toml]`

Old text:

```
    return _parsed(text)


@lru_cache(maxsize=_PARSED_LIMIT)
def _parsed(text: str) -> Taxonomy:
    """The parse :func:`load_taxonomy` remembers, keyed on the whole text."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise TaxonomyError([f"template is not valid TOML: {exc}"]) from exc
    return build_taxonomy(data)
```

New text:

```
    got = _parsed(text)
    if isinstance(got, TaxonomyError):
        raise got
    return got


@lru_cache(maxsize=_PARSED_LIMIT)
def _parsed(text: str) -> Taxonomy:
    """The parse :func:`load_taxonomy` remembers, keyed on the whole text."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return TaxonomyError([f"template is not valid TOML: {exc}"])
    return build_taxonomy(data)
```

### `r301.B4_refusal_message_no_key`

The monthly refusal's message is reworded so it no longer names the key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B4_refusal_message_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
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

### `r706-a.A7_ceiling_message_reworded`

Reword the ceiling refusal so it no longer says the file is not one set

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A7_ceiling_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
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

### `r924.A2_plan_before_the_bounds`

The plan line is said before the month bound and the credential read, so a refused run is told it will pay

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A2_plan_before_the_bounds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 186 against a baseline of 186
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

### `u103-a.A2_write_keeps_only_answers`

Drop the writer's rule that only a match or a miss is kept, removed alone so the reader's copy of the rule is not what is measured

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A2_write_keeps_only_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
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

### `u57-recognition-and-items.M16_grid_off_by_one`

The planned count loses its last chunk

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M16_grid_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 58 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[chunk-plan]`
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[file]`
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[host]`
  - `tests/intake/test_recognition.py::test_a_chunk_that_got_no_answer_is_never_kept_so_only_the_gap_is_paid_again`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[another-plan]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[corrupt]`
  - `tests/intake/test_recognition.py::test_a_document_that_cannot_be_trusted_is_a_miss_and_never_a_tracklist[not-an-object]`
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_ledger_that_cannot_record_stops_the_run_before_the_call`
  - `tests/intake/test_recognition.py::test_a_partition_that_hands_back_an_oversize_part_is_refused_before_any_call[oversize-second-part]`
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_digested_is_identified_without_the_cache_and_says_so`
  - `tests/intake/test_recognition.py::test_a_recording_that_cannot_be_measured_or_carved_fails_without_a_call`
  - `tests/intake/test_recognition.py::test_a_run_where_no_call_got_an_answer_is_a_failure_and_not_an_empty_set`
  - `tests/intake/test_recognition.py::test_a_second_pass_over_an_unchanged_recording_spends_nothing`
  - ... and 43 more, see the JSON sidecar

Old text:

```
    return (whole - chunk_s) // interval_s + 1
```

New text:

```
    return (whole - chunk_s) // interval_s
```

### `u57-recognition-and-items.M7_fold_never_takes_best_score`

Adjacent answers fold to the first, whatever the later one scored

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M7_fold_never_takes_best_score`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[adjacent-fold-to-first-offset-and-best-score]`

Old text:

```
            if found.score > last.score:
```

New text:

```
            if False:
```

### `r682-a.M2_non_string_why_counted`

a why that is not a string is counted under its own value as a slug

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M2_non_string_why_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
            if isinstance(why, str) and why:
```

New text:

```
            if why:
```

### `r925.S2_out_ignored`

intake set ignores --out and always writes under download staging

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S2_out_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`

Old text:

```
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
```

New text:

```
        out = _tracklist_dir(cfg, None, local if local is not None else source.strip())
```

### `u213.M6_readable_refuses_nameless`

list_playlist_readable: drop the refusal of a row carrying no provider id, so it is silently dropped from the listing

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M6_readable_refuses_nameless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    _refuse_unidentified(nameless)
    tracks = frozen_rows(tuple(read))
```

New text:

```
    tracks = frozen_rows(tuple(read))
```

### `u70.S4_canonical_source`

The job records the reference as typed rather than the canonical favorites, so the resume argv carries the typed spelling

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S4_canonical_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[Favorites]`

Old text:

```
        if hearts:
            reference = FAVORITES
        found = catalogue.resolve(cfg)
```

New text:

```
        found = catalogue.resolve(cfg)
```

### `u103-b.C10_open_question_is_pending`

Exit OK from identify while a version question is open

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C10_open_question_is_pending`
- Moved: the same envelope of intake identify, which U307 moved from cli.py to cli_identify.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK,
        pending=pending,
```

New text:

```
        outcome=Outcome.OK,
        code=ExitCode.OK,
        pending=None,
```

### `u104-d.C4_scratch_left_said`

Never say that a scratch folder outlived its pass

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C4_scratch_left_said`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`

Old text:

```
    if held.leftover is None:
        return ()
```

New text:

```
    if held.leftover is None or True:
        return ()
```

### `u37-author-light.G3_gridless_bpm`

Write a real AverageBpm instead of the gridless constant

- File: `src/cratekit/intake/collection_xml.py`
- Source: `u37-author-light.json`, row `G3_gridless_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_gridless_inizio_no_tempo_child_and_the_bytes_crlf`

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="124.00"
```

### `u104-a.F3_guard_absent_library_return`

Drop the early return for a library root that is not there, so samefile is asked about a folder that does not exist

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F3_guard_absent_library_return`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_library_that_is_not_there_has_nothing_to_be_inside`

Old text:

```
    if not library.exists():
        return

```

New text:

```
(empty)
```

### `u104-c.P2_probe_bound`

Raise the playlist probe from two entries to twenty, a realistic nearby value that downloads most of a set page to learn it is one

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P2_probe_bound`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound`

Old text:

```
PLAYLIST_PROBE = 2
```

New text:

```
PLAYLIST_PROBE = 20
```

### `r706-c.C4_pipeline_drops_parts`

identify_only does not carry parts through, so every verb sees one

- File: `src/cratekit/intake/pipeline.py`
- Source: `r706-c.json`, row `C4_pipeline_drops_parts`
- Moved: the same copy of parts into the verb's result, which U307 made one comprehension over the fields; leaving parts out gives its default of one, as the dropped argument did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified)}
```

New text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified) if one.name != "parts"}
```

### `u102-a.D2_open_is_not_accepted`

decided(): drop the branch that counts an item with no accepted verdict as open

- File: `src/cratekit/intake/repair.py`
- Source: `u102-a.json`, row `D2_open_is_not_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/intake/test_repair.py`
- Collected: 23 against a baseline of 23
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

### `u102-a.P5_missing`

_plan_for: stop setting aside an accepted item whose file is gone, so the run after an apply plans it again

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P5_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`
  - `tests/intake/test_repair_apply.py::test_an_accepted_proposal_is_shown_asked_renamed_and_then_converges`

Old text:

```
        if not path.is_file():
            # ONE CLASS
```

New text:

```
        if False:
            # ONE CLASS
```

### `u102-b.G2_post_gate_referenced`

_apply: drop the referenced check made after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G2_post_gate_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_row_after_the_gate_holds_the_file_and_an_unreadable_collection_refuses`

Old text:

```
        if naming_cli.is_referenced(path, referenced):
            _owed(
```

New text:

```
        if False:
            _owed(
```

### `u102-b.R2_retryable_after_gate`

_owed: stop marking the run retryable when a rename fails after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R2_retryable_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_interrupt_or_a_refused_rename_after_the_claim_leaves_no_stub`

Old text:

```
        nonlocal retryable
        retryable = True
```

New text:

```
        nonlocal retryable
```

### `u237.M3_one_mark_only`

_YEAR: strip one mark only, so (P)(C) 2021 Cadenza keeps the second mark and the year

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M3_one_mark_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 12 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-(P)(C) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-\u2117 \xa9 2021 ]`

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)", re.IGNORECASE)
```

### `r261.S4_existing_can_list`

Sample of an existing guard: _crawl_or_refuse accepts an object exposing no listing at all

- File: `src/cratekit/label/sweep.py`
- Source: `r261.json`, row `S4_existing_can_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 521 against a baseline of 521
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_an_artist_exposing_no_listing_method_raises_rather_than_crawling_nothing`

Old text:

```
    if not listable:
```

New text:

```
    if False:
```

### `u52-zero-rows.L6_verifier_missing_returns_stub`

A source built with neither verifier nor catalogue confirms nothing instead of refusing, so every release is dropped as unconfirmed

- File: `src/cratekit/label/sweep.py`
- Source: `u52-zero-rows.json`, row `L6_verifier_missing_returns_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_source_with_neither_verifier_nor_catalogue_refuses_rather_than_confirming_nothing`

Old text:

```
        raise run.LookupFailure(
            "this labels source was built with neither a verification callable "
            "nor a catalogue, so no release it listed could be confirmed"
        )
```

New text:

```
        def unconfirmed(claimed: str, release: Any) -> Mapping[str, Any]:
            return {}

        return unconfirmed
```

### `u192.F2_no_retry`

_resumable: read the job instead of re-arming it, so the named --job command meets a closed job

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F2_no_retry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 278 against a baseline of 278
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
        job = jobs.retry(store, job_id)
```

New text:

```
        job = jobs.get(store, job_id)
```

### `r572.E1_export_drop_album`

The export engine stops passing the album to match_track

- File: `src/cratekit/modules/outbound/export.py`
- Source: `r572.json`, row `E1_export_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_the_export_plan_hands_the_account_the_release_title_and_album[the-files-album-tag]`

Old text:

```
            album=track.album,
```

New text:

```
(empty)
```

### `r229.L14_a_recorded_crate_is_a_claimant`

A living crate with its own remote playlist is named as the one a mismatched record belongs to

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L14_a_recorded_crate_is_a_claimant`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`

Old text:

```
                and not (playlists.get(key) or {}).get("remote_id")

```

New text:

```
(empty)
```

### `r229.L5_no_crate_side_bound`

A candidate is judged on the record's side alone, so a three thousand track crate is offered an eight track orphan

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L5_no_crate_side_bound`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_crate_the_record_is_a_sliver_of_is_not_that_crate[a-crate-that-merely-contains-it]`
  - `tests/modules/test_outbound.py::test_a_crate_the_record_is_a_sliver_of_is_not_that_crate[one-past-quadrupled]`

Old text:

```
            if _still_carries(written, wanted) and _grown_within(written, wanted):
```

New text:

```
            if _still_carries(written, wanted):
```

### `u309-z.U6_pairs_words_only_on_hold`

A pairs record whose links hold empty text reads as well formed, the empty allowance spread past the held map

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u309-z.json`, row `U6_pairs_words_only_on_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_pair_discover.py`, `tests/modules/test_outbound.py`
- Collected: 247 against a baseline of 247
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_pairs_record_whose_links_hold_empty_text_is_unusable`

Old text:

```
isinstance(k, str) and k and isinstance(v, str) and (words or v) for k, v in value.items()
```

New text:

```
isinstance(k, str) and k and isinstance(v, str) for k, v in value.items()
```

### `u27-reports-round-2.C3_uncovered_order`

Round 1 zero, re-run against the replacement guard: drop the deterministic order

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-2.json`, row `C3_uncovered_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_uncovered_list_is_ordered_BY_ARTIST_AND_NOT_BY_THE_WALK`
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
        uncovered=tuple(sorted(uncovered, key=_by_name)),
```

New text:

```
        uncovered=tuple(uncovered),
```

### `u27-reports-round-1.L6_entries_in_no_playlist`

Count every entry as in no playlist

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L6_entries_in_no_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_gaps_count_entries_with_no_head_and_entries_in_no_playlist`

Old text:

```
            entries_in_no_playlist=sum(1 for entry in view.entries if not entry.playlists),
```

New text:

```
            entries_in_no_playlist=len(view.entries),
```

### `r154-b.B11_marker_name_safety`

Write a marker for any identity at all, so one carrying a separator or a dot segment is interpolated into a remote path

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B11_marker_name_safety`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[..]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[.hidden]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has space]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has/slash]`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`

Old text:

```
    if not _MARKER_IDENTITY.fullmatch(folded):
        return None
```

New text:

```
    if False:
        return None
```

### `r222-a.A3_no_floor_holds_nothing`

Read no floor as nothing to hold, so a remote with no completed mirror on record is rotated as though every folder were settled

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A3_no_floor_holds_nothing`
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
(floor is None or name > floor)]
```

New text:

```
(floor is not None and name > floor)]
```

### `r338-b.R2_missing_directory_exit_moved`

RCLONE_DIRECTORY_NOT_FOUND: move the exit to 4, rclone's file not found, a nearby value, so a missing mirror refuses

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-b.json`, row `R2_missing_directory_exit_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `u48-author.P1_listing_classification_dropped`

A failed listing returns no warning, so the rotation stops silently again

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P1_listing_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

New text:

```
    if result.returncode != 0:
        return out, None
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

### `u311.A10_paths_keep_the_trailing_empty`

Reading a path list keeps the empty name after the last line feed

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u311.json`, row `A10_paths_keep_the_trailing_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 317 against a baseline of 317
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_quick.py::test_a_name_holding_a_line_separator_is_one_path_to_the_archive_check`

Old text:

```
    return tuple(feed.split("\n")[:-1]) if feed else ()
```

New text:

```
    return tuple(feed.split("\n")) if feed else ()
```

### `r154-b.B6_walk_bound`

Multiply the walk bound by ten, so a remote of foreign snapshots is read far past what the refusal says it looked at

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B6_walk_bound`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`

Old text:

```
NEWEST_WALK = 8
```

New text:

```
NEWEST_WALK = 80
```

### `r338-b.R1_missing_directory_refuses`

share_is_held: stop reading rclone's missing directory exit as no mirror, so every backup older than this fix refuses its restore

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R1_missing_directory_refuses`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r338-c.C2_carried_share_still_warned`

absent_analysis_share: warn whenever the share is outside the root, carried or not, which is the retired warning back under a new code

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C2_carried_share_still_warned`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r367.G7_the_listing_is_of_the_snapshot_root`

list the dated folder, not the db folder inside it, so the log is never seen

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G7_the_listing_is_of_the_snapshot_root`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`

Old text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
```

New text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/",
```

### `r388-b.M10_named_stamp_absent_read_as_failure`

Drop the exit 3 branch on the identity listing, so a mistyped stamp sends the person to the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M10_named_stamp_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `u311.C3_suffix_case_matters`

A recording whose suffix is upper case is refused as unsupported

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C3_suffix_case_matters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 247 against a baseline of 247
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_recording_is_read_whatever_the_case_of_its_suffix`

Old text:

```
    if path.suffix.lower() not in SOURCE_SUFFIXES:
```

New text:

```
    if path.suffix not in SOURCE_SUFFIXES:
```

### `r187-b.B1_size_dropped`

_entry_is_current: drop the size, so new bytes restored under an old modification time serve the old track

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B1_size_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_new_bytes_under_an_old_modification_time_are_re_read`

Old text:

```
        and entry.get("size") == identity["size"]

```

New text:

```
(empty)
```

### `u311.C7_wider_tier_steps_down`

The wider tier's plus three step becomes minus three

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C7_wider_tier_steps_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 339 against a baseline of 339
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_camelot_tiers_are_the_ported_ones[11A-wider]`

Old text:

```
    wider = ((-2, letter), (3, letter), (-1, other), (1, other))
```

New text:

```
    wider = ((-2, letter), (-3, letter), (-1, other), (1, other))
```

### `u281.R1_stop_after_four`

Refusals.stopped: stop only once the count passes the limit, so four refusals are sent, not three

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R1_stop_after_four`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 11 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
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
        if self.running.get(source, 0) < self.limit:
```

New text:

```
        if self.running.get(source, 0) <= self.limit:
```

### `u281.S6_every_title_named_cloudflare`

unread_outcome: name every challenge title Cloudflare's, Bandcamp's own Client Challenge included

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `S6_every_title_named_cloudflare`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 2 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_bandcamp_client_challenge_title_is_blocked_and_not_called_cloudflare`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
        named = f", a {CLOUDFLARE_CHALLENGE}" if _CLOUDFLARE_TITLE.match(title) else ""
```

New text:

```
        named = f", a {CLOUDFLARE_CHALLENGE}"
```

### `u260.F1_fetch_never_answers_from_memory`

remembering: never look the address up, so every file asks the host again, the behaviour before the unit

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F1_fetch_never_answers_from_memory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 10 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_raises_is_not_remembered`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_an_empty_answer_handed_straight_in_is_not_remembered`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
            data = held.get(url)
            if data is not None:
                held.move_to_end(url)
                return data
        data = fetch_image(url)
```

New text:

```
            data = None
            if data is not None:
                held.move_to_end(url)
                return data
        data = fetch_image(url)
```

### `u260.F9_fetch_memory_unbounded`

IMAGE_MEMORY: a hundred entries, near enough unbounded for a sweep

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F9_fetch_memory_unbounded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_shipped_fetch_memory_is_bounded`

Old text:

```
IMAGE_MEMORY = 4
```

New text:

```
IMAGE_MEMORY = 100
```

### `u282.P4_refusal_not_unread`

_pictured: a refused or unread picture ask does not join unread

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P4_refusal_not_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`

Old text:

```
            if outcome.answer.value in UNREAD_ANSWERS and source not in unread:
```

New text:

```
            if False:
```

### `u133-b.T1_keyword_back`

The jazz keyword rule sends a partial match to NonElectronic again, as before U133

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T1_keyword_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 946 against a baseline of 945
- Kills: 13 (collect-error)
- Note: collection changed: 946 collected against a baseline of 945. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_already_in_rock_is_filed_in_jazz_and_stays_in_rock`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved[Acid Jazz]`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved[Jazz Funk]`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_routes_to_jazz_by_the_keyword_rule_the_author_moved[jazz]`
  - `tests/test_routing_parity.py::test_the_one_keyword_rule_the_author_moved_takes_only_what_the_old_code_filed_by_it`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_made_before_u133_takes_the_discogs_table_and_loads_after_the_holds_edits`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_with_no_jazz_keyword_rule_is_told_it_has_none`
  - `tests/test_taxonomy_upgrade.py::test_a_copy_with_the_words_out_and_the_row_left_does_not_load`
  - `tests/test_taxonomy_upgrade.py::test_every_bucket_of_the_copy_filing_a_word_is_named_not_the_first`
  - `tests/test_taxonomy_upgrade.py::test_jazz_is_held_while_non_electronic_still_files_its_words_and_every_place_is_named`
  - `tests/test_taxonomy_upgrade.py::test_one_place_filing_a_word_under_two_spellings_names_both_in_one_sentence`
  - `tests/test_taxonomy_upgrade.py::test_the_hand_edit_the_hold_names_lets_jazz_in_on_the_next_run`
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
keyword = "jazz"
bucket = "jazz"

```

New text:

```
keyword = "jazz"
bucket = "non_electronic"

```

### `u25.G15_barren_watch`

Watch Music, which holds no ANLZ file, instead of watch_roots

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G15_barren_watch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_store.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_no_call_site_hand_lists_the_roots_an_analysis_watch_covers`

Old text:

```
            analysis_roots=analysis_store.watch_roots(cfg),

```

New text:

```
            analysis_roots=(Path(cfg.library.root) / "Music",),

```

### `u327.A24_spec_reads_title_head_first`

_spec_for: read the file name's head first again, so name apply writes the old tempo back over a corrected title

- File: `src/cratekit/write/naming_cli.py`
- Source: `u327.json`, row `A24_spec_reads_title_head_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_analyze_adopt.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_full_library_name_apply_after_the_adopt_brings_nothing_back`
  - `tests/test_naming_apply_cli.py::test_one_file_is_planned_its_one_rename[the-title-head-wins-over-the-filename-head]`

Old text:

```
        naming.parse_head(title, template=template)
        or naming.parse_head(path.name, template=template)
        or {}
```

New text:

```
        naming.parse_head(path.name, template=template)
        or naming.parse_head(title, template=template)
        or {}
```

### `r758-a.T5_dead_track_moved`

a track with no live collection row is moved like any other

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T5_dead_track_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_no_live_collection_row_is_skipped_whole`

Old text:

```
        live = [move for move in moves if _live_content(db, move.content_id)]
```

New text:

```
        live = list(moves)
```

### `r658-b.S3_adoption_failing_stat`

Drop the scoped failing stat around the stamping write

- File: `tests/test_adoption.py`
- Source: `r658-b.json`, row `S3_adoption_failing_stat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_stamping_STAT_that_fails_records_the_state_rather_than_asserting_it_cannot`

Old text:

```
        failing.setattr(Path, "stat", stat_fails_after_the_write)

```

New text:

```
(empty)
```

