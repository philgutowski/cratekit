# Mutation table: u332-replay-before-3

Measured by `scripts/mutate.py` on 2026-11-24 06:15 UTC, branch `HEAD` at `324cafa5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 144.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:15 UTC for commit `324cafa562b9`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 112, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 161 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B1_a_root_outside_the_temporary_directory` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 3 | killed |
| `u297.B9_a_file_in_one_capture_only_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 2 | killed |
| `u122.N1_next_busy_progress_only` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 1 | killed |
| `u148.L1_old_limit` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 4 | killed |
| `u151.A1_archived_read` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.O2_owner_case_sensitive` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u187.A1_relayed_answer_never_matches` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 5 | killed |
| `u203.M3_no_sentence_cut` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 4 | killed |
| `u291.L2_lanes_one_short` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u314.L1_archives_unread` | `scripts/board.py` | maintainer | 3 file(s) | 157 | 7 | killed |
| `r83.D3_drop_attribute_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 753 | 6 | killed |
| `u176.C10_trusted_https` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 2 | killed |
| `u176.C7_preorder_not_downloadable` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 7 | killed |
| `u176.V2_hidden` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u177.B10_land_command` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 3 | killed |
| `u177.B8_write_false_ignored` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u205.C3_no_expiry_margin` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 3 | killed |
| `r289-b.B3_terminal_filter_gone` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r668-a.M1_list_required_again` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 39 | killed |
| `r668-b.M8_named_not_absolutised` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u42-author.C1_undecided_derived` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.W3_onerror_silent` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u54-acquisition-worker.G1_origin_refusal` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-zero-row-remeasured.G7_staging_cleared` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u80.F15_empty_offered` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 4 | killed |
| `u81-fetch-b.L1_two_files_first_wins` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u80.C3_dedupe_on_match_id` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u81-fetch-a.W6_post_landing_exists` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.W4_empty_stem_rerun` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r1016.M8_walk_name_ignored` | `src/cratekit/acquire/listing.py` | maintainer | 7 file(s) | 794 | 1 | killed |
| `r878-a.A1_paginate_refuses_cursor` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `r878-b.B11_folder_rule_in_table` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 20 | killed |
| `u65.A1_stop_gets_a_default` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 199 | 1 | killed |
| `u65.C2_an_empty_page_ends_a_declared_total_walk` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 1 | killed |
| `u65.E3_the_favourites_total_is_never_wired` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 4 | killed |
| `r679-b.B1_no_retirement` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 7 | killed |
| `r664.E4_title_not_split` | `src/cratekit/acquire/match_library.py` | user | 10 file(s) | 1193 | 106 | killed |
| `u274.P4_sweep_live` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 450 | 6 | killed |
| `r703-b.L1_no_active_exception` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 3 | killed |
| `r703-c.C1_last_exception_wins` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 1 | killed |
| `u47-author.CODEC_policy_ignored` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R196_login_without_pkce` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R197_event_run_left_clear` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u254.M03_cache_identity_no_size` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M12_header_upgrade` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `u254.M20_mark_unlocked` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `r731-b.M14_gate_without_the_count` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 1 | killed |
| `u27-adopt-apply-author.A1_approval_actor_is_the_process` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 632 | 1 | killed |
| `u55-collection-reader.R19_collector_groups_locations` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 1 | killed |
| `u23-round-8-independent.X1_approval_type_check_never_fires` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 7 | killed |
| `r758-b.M2_unnamed_genre_is_moved` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `r780-a.A6_every_entry_claims_its_bucket` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `u118-c.M2_holder_genre_leg` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 189 | 1 | killed |
| `r758-b.C3_rows_not_proven_against_the_digest` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `u340.R28_worker_no_elsewhere` | `src/cratekit/adopt/move_cli.py` | user | 4 file(s) | 816 | 2 | killed |
| `r788-c.L6_removed_node_is_a_place` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 163 | 1 | killed |
| `r1965.R25_sample_vocal_sub` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 9 | killed |
| `r731-a.M01_unread_tree_withholds` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 1 | killed |
| `r731-a.M11_verdict_withheld_on_the_review_list` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 1 | killed |
| `r788-a.P8_renamed_bucket_doubles` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 2 | killed |
| `u956.O13_outside_list_every_excluded` | `src/cratekit/adopt/plan.py` | user | 3 file(s) | 658 | 2 | killed |
| `u23-round-8-independent.A4_at_risk_drops_the_record_value` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.D2_bytes_agree_size_gate_inverted` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 6 | killed |
| `r759.A1_deadline_asked_only_at_the_end` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 1 | 1 | killed |
| `r722.S4_default_reader_lenient` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 692 | 4 | killed |
| `u956.O10_root_not_composed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 641 | 1 | killed |
| `u956.O8_dots_not_read` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 641 | 1 | killed |
| `u241.M14_a_changed_file_keeps_its_old_head` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 4 | killed |
| `u223.M22_discard_unlinks_directory` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 177 | 1 | killed |
| `u223.M7_report_any_item` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 177 | 2 | killed |
| `u90-a.A4_max_coefficient` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 2 | killed |
| `u90-b.B6_hand_detail_drops_old_cut` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 4 | killed |
| `u94-a.S4_accept_flag_dead` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 11 | killed |
| `u94-b.W5_warning_without_a_write` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N5_note_m_is_the_sample` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u223.M12_renamed_to_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 1 | killed |
| `u241.M21_no_check_line_on_the_answer` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 13 | killed |
| `u343.M03_untitled_overwrites_a_title` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 324 | 3 | killed |
| `u58-workers-and-wav.R4_keyless_finalized` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 2 | killed |
| `u263.D12_channels_first` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 7 | killed |
| `u263.D6_window_round` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u264.M1_fast_path_never` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u264.M9_read_at_target_rate` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u157.D8_percentile` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u344.M3_head_unavailable_reads_calibrated` | `src/cratekit/analysis/detect.py` | user | 5 file(s) | 497 | 1 | killed |
| `u327.A15_digest_covers_items` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 2 | killed |
| `u327.A6_key_id_empty` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 3 | killed |
| `u342.P1_never_stamped_half` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 2 | killed |
| `u342.P9_stamped_key_tag` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 3 | killed |
| `u275.M1_base_back_to_linux` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 555 | 6 | killed |
| `u343.M08_resume_reads_the_name_alone` | `src/cratekit/analysis/run.py` | user | 4 file(s) | 503 | 7 | killed |
| `sitting3.G15_fold_any_ragged_tail` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 3 | killed |
| `u263.D17_vocal_reraise` | `src/cratekit/analysis/vocal.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u58-workers-and-wav.W7_undecodable_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 177 | 1 | killed |
| `u92-author.G7_reason_reworded` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 1 | killed |
| `r221-a.W3_queue_branch_warning_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B11_finished_jobs_are_twins` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `r222-b.B6_itemless_job_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r349-a.A4_envelope_field` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r757-c2.S5_unread_number_printed_as_zero` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 728 | 1 | killed |
| `u45-round-1.C4_uniform_refusal_flattened` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `u45-round-1.R1_reserved_remediation_discarded` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `u45-round-2.A3_age_seconds_always_none` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u50-zero-rows.B2_items_hardcoded_pair` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u248.L4_listing_drops_the_stub_line` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1235 | 4 | killed |
| `r925.J2_playlist_excluded` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 4 | killed |
| `u42-author.R1_planned_marker_returns` | `src/cratekit/cli/registry_pipeline.py` | user | 3 file(s) | 1049 | collection error | collect-error |
| `r685-a.L2_an_unmounted_library_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 4 file(s) | 350 | 2 | killed |
| `u260.D1_decodes_always` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 2 | killed |
| `u260.E6_encode_never_remembered` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 11 | killed |
| `u83-a.E3_ladder_ends_on_floor` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.R3_unknown_depth_default` | `src/cratekit/core/art.py` | maintainer | 1 file(s) | 73 | 1 | killed |
| `u83-b.W5_cap_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `r757-b2.F1_absent_key_reads_as_never` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 728 | 1 | killed |
| `example-binaries-five-row.B3_platform_binary_remedy` | `src/cratekit/core/binaries.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u27-r80-write-probe-replacement.W8_read_probe_flags` | `src/cratekit/core/cause.py` | user | 1 file(s) | 358 | 1 | killed |
| `u197-m6.M6_composite` | `src/cratekit/core/config_schema.py` | user | 3 file(s) | 827 | 2 | killed |
| `r290-author.J7_cancelled_raises_the_plain_type` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 25 | killed |
| `u57-recognition-and-items.C12_stray_file_sorted` | `src/cratekit/core/jobs.py` | user | 1 file(s) | 67 | 1 | killed |
| `u342.S7_stamp_pads_the_key` | `src/cratekit/core/naming.py` | user | 4 file(s) | 392 | 1 | killed |
| `u205.G6_file_account_share_is_the_total` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 184 | 2 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `r797-a.T7_competes_in_a_style_bucket` | `src/cratekit/core/routing.py` | user | 4 file(s) | 1097 | 13 | killed |
| `r722-b.T7_lenient_field_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 1 | killed |
| `u247.M1_memo_removed` | `src/cratekit/core/taxonomy.py` | user | 4 file(s) | 293 | 10 | killed |
| `r301.B3_refusal_detail_no_key` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 4 | killed |
| `r706-a.A6_run_message_reworded` | `src/cratekit/intake/acrcloud.py` | maintainer | 5 file(s) | 227 | 2 | killed |
| `r924.A1_no_plan_line` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 186 | 4 | killed |
| `u103-a.A1_read_serves_only_answers` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 1 | killed |
| `u57-recognition-and-items.M12_quota_reads_as_failure` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 4 | killed |
| `u57-recognition-and-items.M6_score_constant` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 6 | killed |
| `r682-a.M1_no_by_reason_in_summary` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 122 | 4 | killed |
| `r925.S1_no_folder_check` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 108 | 40 | killed |
| `u213.M13_unidentified_any` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u70.S3_sentinel_strip` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 241 | 1 | killed |
| `r925.S5_unwritten_note_names_no_job_show` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u104-d.C3_detail_renamed` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `u37-author-light.G1_stub_listing` | `src/cratekit/intake/collection_xml.py` | user | 2 file(s) | 12 | 1 | killed |
| `u104-a.F2_guard_samefile_layer` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P1_numbered_output` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `r685-a.V2_landing_preflight_reads_the_shipped_text` | `src/cratekit/intake/landing.py` | user | 2 file(s) | 41 | 2 | killed |
| `u102-a.D1_keep_is_not_accept` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 23 | 1 | killed |
| `u102-a.P4_unchanged` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G1_plan_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.R1_retryable_seed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u237.M2_symbol_marks_dropped` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 36 | killed |
| `u177.A6_first_of_two` | `src/cratekit/label/registry.py` | user | 6 file(s) | 190 | 2 | killed |
| `u52-zero-rows.L5_artist_for_missing_returns_none` | `src/cratekit/label/sweep.py` | user | 3 file(s) | 293 | 1 | killed |
| `u192.F1_no_rearm_catch` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 4 | killed |
| `r356-b.B6_export_plan_drops_the_reason` | `src/cratekit/modules/outbound/export.py` | user | 1 file(s) | 64 | 1 | killed |
| `r229.L13_a_mismatch_is_never_said` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r229.L4_an_eighth_of_the_crate` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `u309-z.U2_settle_extend_dedupes` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 9 file(s) | 514 | 1 | killed |
| `u27-reports-round-1.C4_placement_count` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L5_unused_buckets` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `r154-a.A4_legacy_spelling` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 189 | 1 | killed |
| `r1761.P25_max_delete_sentence_on_any_failure` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r222-a.A2_boundary_not_strict` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 3 | killed |
| `r338-a.B7_rehearsal_transfers_the_share` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 1 | killed |
| `r757-a.E2_fast_mode_lists_folder_by_folder` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 23216 | 0 (promoted) | zero |
| `r757-b1.E12_plain_line_dropped` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 23216 | 0 (promoted) | zero |
| `u317.Q15_archive_not_rechecked` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u323.I1_unread_identity_refuses` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u48-author.E1_listing_return_code_inverted` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 17 | killed |
| `r1761.P5_empty_root_passes` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r1761.P7_floor_coefficient_halved` | `src/cratekit/modules/tools/backup_record.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `u317.Q12_root_volume_not_rechecked` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u317.Q8_settled_trusts_the_first_walk` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r154-b.B5_veto_not_select` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 189 | 3 | killed |
| `r338-a.B8_contained_share_copied_twice` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 8 | killed |
| `r338-c.C1_absent_share_never_said` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 4 | killed |
| `r367.G5_absent_sidecars_are_not_recorded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 2 | killed |
| `r388-a.M6_root_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `u311.C2_any_block_is_the_report` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `r187-b.B10_bad_track_is_current` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 7 | killed |
| `u311.C6_relative_key_dropped` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 3 | killed |
| `r704-a.R5_flag_not_stored` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 2 | killed |
| `u281.S5_title_not_named_cloudflare` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 205 | 1 | killed |
| `u260.F11_reset_images_forgets_nothing` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 9 | killed |
| `u260.F8_fetch_hit_not_refreshed` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u282.P1_no_picture_question` | `src/cratekit/tagging/searchers.py` | user | 9 file(s) | 1470 | 8 | killed |
| `u133-b.T10_family` | `src/cratekit/templates/taxonomy.default.toml` | user | 2 file(s) | 894 | 3 | killed |
| `u132.G1_undeclared_cause` | `src/cratekit/write/genre_favorites.py` | user | 5 file(s) | 288 | 2 | killed |
| `r675.G5_leaf_compared_as_whole_path` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 15 | killed |
| `r758-a.T4_target_can_be_removed_from` | `src/cratekit/write/trees.py` | user | 1 file(s) | 87 | 1 | killed |
| `r685-b.G2_the_guard_forgets_attributes` | `tests/test_active_taxonomy.py` | maintainer | 1 file(s) | 18 | 1 | killed |

## Zero rows and what they owe

- `u42-author.W3_onerror_silent` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u263.D6_window_round` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u264.M1_fast_path_never` (maintainer facing): maintainer facing, composite not required
- `u264.M9_read_at_target_rate` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u157.D8_percentile` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u263.D17_vocal_reraise` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P25_max_delete_sentence_on_any_failure` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-a.E2_fast_mode_lists_folder_by_folder` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-b1.E12_plain_line_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q15_archive_not_rechecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u323.I1_unread_identity_refuses` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P5_empty_root_passes` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P7_floor_coefficient_halved` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q12_root_volume_not_rechecked` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q8_settled_trusts_the_first_walk` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u297.B1_a_root_outside_the_temporary_directory`

refuse_outside_temporary: accept any root, so a capture can be pointed at a directory somebody keeps

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B1_a_root_outside_the_temporary_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_link_inside_the_temporary_directory_that_leads_out_of_it_is_refused`
  - `tests/test_behaviour_compare.py::test_a_root_outside_the_temporary_directory_is_refused_before_anything_runs`
  - `tests/test_behaviour_compare.py::test_the_temporary_directory_itself_is_no_root`

Old text:

```
    if not is_inside(path, temporary_directory()):
```

New text:

```
    if False:
```

### `u297.B9_a_file_in_one_capture_only_unseen`

compare_files: walk only the paths both captures hold, so an extra file and a missing one are never reported

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B9_a_file_in_one_capture_only_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_an_empty_directory_a_verb_made_is_an_entry_of_its_own`
  - `tests/test_behaviour_compare.py::test_one_extra_file_is_reported_and_so_is_one_that_is_gone`

Old text:

```
    for relative in sorted(set(before) | set(after)):
```

New text:

```
    for relative in sorted(set(before) & set(after)):
```

### `u122.N1_next_busy_progress_only`

next counts only In Progress as busy, so an In review card is offered again

- File: `scripts/board.py`
- Source: `u122.json`, row `N1_next_busy_progress_only`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
.get("status") in UNDERWAY
```

New text:

```
.get("status") == "In Progress"
```

### `u148.L1_old_limit`

READ_LIMIT back to 300, the ceiling the board passed

- File: `scripts/board.py`
- Source: `u148.json`, row `L1_old_limit`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`
  - `tests/test_board_reads.py::test_every_issue_and_project_item_is_read_past_three_hundred`
  - `tests/test_board_reads.py::test_issues_filed_after_the_count_are_read_and_not_refused`

Old text:

```
READ_LIMIT = 5000
```

New text:

```
READ_LIMIT = 300
```

### `u151.A1_archived_read`

archived cards are read as on the board

- File: `scripts/board.py`
- Source: `u151.json`, row `A1_archived_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card`

Old text:

```
includeArchived: false
```

New text:

```
includeArchived: true
```

### `u151.O2_owner_case_sensitive`

the owner match becomes case sensitive

- File: `scripts/board.py`
- Source: `u151.json`, row `O2_owner_case_sensitive`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_only_this_owners_project_is_the_board_whatever_the_case`

Old text:

```
                if login.lower() != owner.lower():
```

New text:

```
                if login != owner:
```

### `u187.A1_relayed_answer_never_matches`

_relayed_answer: never match, so the relay thread's Answer from Phillip is read as a session hold and never as his reply

- File: `scripts/board.py`
- Source: `u187.json`, row `A1_relayed_answer_never_matches`
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
    return comment_heading(comment.get("body") or "") == HEAD_ANSWER
```

New text:

```
    return False
```

### `u203.M3_no_sentence_cut`

_HEADING_END: cut only at a colon or comma, so Needs the machine. The card needs rekordbox is a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M3_no_sentence_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Landed; merge 5c8b26a-landed]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Needs the machine. The card needs rekordbox-needs the machine]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Question for Phillip? Which one-question for phillip]`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:,]")
```

### `u291.L2_lanes_one_short`

CLOUD_LANES: nine lanes, one short of the cap

- File: `scripts/board.py`
- Source: `u291.json`, row `L2_lanes_one_short`
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
CLOUD_LANES = 9
```

### `u314.L1_archives_unread`

ledger_files: read the working file alone, so search, the highest number and the title check never see an archive

- File: `scripts/board.py`
- Source: `u314.json`, row `L1_archives_unread`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`, `tests/test_restart_and_residual_files.py`, `tests/test_pending_units.py`
- Collected: 157 against a baseline of 157
- Kills: 7 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_search_reads_every_archive_and_says_where_each_hit_is`
  - `tests/test_pending_units.py::test_the_residual_heading_reader_reads_the_document_as_it_is_written`
  - `tests/test_restart_and_residual_files.py::test_a_landing_numbers_past_the_highest_in_any_file_and_archives_when_over`
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_file_over_the_limit_and_archives_that_overlap`
  - `tests/test_restart_and_residual_files.py::test_check_refuses_a_heading_in_two_archives_and_a_misnamed_one`
  - `tests/test_restart_and_residual_files.py::test_the_archive_moves_every_entry_byte_for_byte_and_a_rerun_changes_nothing`

Old text:

```
    return sorted((ledger.parent / "ledger").glob("*.md"), key=first) + [ledger]
```

New text:

```
    return [ledger]
```

### `r83.D3_drop_attribute_error`

R-348: AttributeError leaves the defect classes, the class the sitting found

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D3_drop_attribute_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 753 against a baseline of 753
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_stops_the_paced_pool_rather_than_being_retried`
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_a_defect_naming_a_token_as_a_defect`

Old text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)
```

New text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (TypeError, NameError)
```

### `u176.C10_trusted_https`

trusted: plain http is trusted, so the session is sent over an unencrypted link

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C10_trusted_https`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_the_download_page_itself_is_never_asked_outside_bandcamp[plain-http]`
  - `tests/test_bandcamp.py::test_the_session_is_never_sent_to_a_link_outside_bandcamp[plain-http]`

Old text:

```
    return parts.scheme == "https" and any(
```

New text:

```
    return parts.scheme in ("http", "https") and any(
```

### `u176.C7_preorder_not_downloadable`

Purchase.downloadable: a preorder with a link reads downloadable, so the plan offers a release that cannot be fetched

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C7_preorder_not_downloadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 7 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_preorder_and_a_purchase_with_no_link_are_not_downloadable`
  - `tests/test_bandcamp_cli.py::test_a_compilation_with_one_owned_track_stages_the_rest_and_names_the_one`
  - `tests/test_bandcamp_cli.py::test_a_preorder_is_not_downloadable`
  - `tests/test_bandcamp_cli.py::test_a_second_run_plans_nothing`
  - `tests/test_bandcamp_cli.py::test_an_owned_release_names_the_owned_file_and_is_not_fetched`
  - `tests/test_bandcamp_cli.py::test_the_fetch_stages_flat_into_its_batch_folder_and_records_each`
  - `tests/test_bandcamp_cli.py::test_the_plan_gives_every_purchase_newest_first_one_disposition`

Old text:

```
        return bool(self.download_page) and not self.preorder
```

New text:

```
        return bool(self.download_page)
```

### `u176.V2_hidden`

plan: a hidden purchase is not planned hidden, so a purchase the account hid is fetched

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V2_hidden`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_hidden_purchase_is_planned_hidden`

Old text:

```
        if purchase.hidden:
```

New text:

```
        if False:
```

### `u177.B10_land_command`

land_command: name no landing, so the fetch never says how to file the batch by label

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B10_land_command`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`

Old text:

```
    if not any(isinstance(one, Mapping) and one.get("label") for one in releases.values()):
        return None

```

New text:

```
    if True:
        return None

```

### `u177.B8_write_false_ignored`

handle_fetch: ignore the writer's False, so a file that would not take the tag is reported tagged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B8_write_false_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`

Old text:

```
        if label and not tags.write_tags(path, {"label": label}):
            untagged.append(final.name)

```

New text:

```
        if label:
            tags.write_tags(path, {"label": label})

```

### `u205.C3_no_expiry_margin`

app client: a token is kept to the last second of its life and refused on the way

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C3_no_expiry_margin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_short_lived_token_keeps_half_its_life_rather_than_none[30]`
  - `tests/test_catalogue_app.py::test_a_short_lived_token_keeps_half_its_life_rather_than_none[60]`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_reused_until_it_nears_expiry`

Old text:

```
max(seconds - TOKEN_MARGIN_S, seconds / 2)
```

New text:

```
max(seconds, seconds / 2)
```

### `r289-b.B3_terminal_filter_gone`

Sweep every job's staging, open ones included

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B3_terminal_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_directory_naming_a_job_this_queue_does_not_hold_is_left_alone`
  - `tests/test_acquire_workers.py::test_an_open_jobs_staging_survives_the_sweep`

Old text:

```
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
```

New text:

```
        if False:
```

### `r668-a.M1_list_required_again`

the list positional is required again, so --job alone is argparse's usage error, the defect sitting 7 hit

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M1_list_required_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 39 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_download_job_runs_pending_to_done_through_the_resume_path`
  - `tests/test_acquire_workers.py::test_a_lossless_landing_under_the_permissive_policy_is_not_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_rate_limit_is_retried_under_backoff_and_then_lands`
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - ... and 24 more, see the JSON sidecar

Old text:

```
        "list",
        nargs="?",
        default=None,

```

New text:

```
        "list",

```

### `r668-b.M8_named_not_absolutised`

the named list is compared without the freeze's absolutising, so a relative spelling from the queueing directory is refused

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M8_named_not_absolutised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`

Old text:

```
        given = Path(named).expanduser().absolute()
    except RuntimeError:
```

New text:

```
        given = Path(named).expanduser()
    except RuntimeError:
```

### `u42-author.C1_undecided_derived`

Empty the undecided remainder, so an MP4 container falls out as 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C1_undecided_derived`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_every_audio_container_the_renamer_knows_has_a_classification`
  - `tests/test_acquire_cli.py::test_the_undecided_remainder_is_the_mp4_container_today`

Old text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS
```

New text:

```
UNDECIDED_EXTS: frozenset[str] = frozenset()
```

### `u42-author.W3_onerror_silent`

Keep os.walk but make the error hook a no-op, the half-fix

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W3_onerror_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        unreadable.append(Path(exc.filename) if exc.filename else root)
```

New text:

```
        return None
```

### `u54-acquisition-worker.G1_origin_refusal`

Queue a list from any provider, dropping the refusal that only the provider's own list carries acquirable identifiers

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G1_origin_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_pasted_tracklist_is_refused_at_the_queue_rather_than_queued_unacquirable`

Old text:

```
    if origin != match.TIDAL:
        raise _unusable(
            f"this is a {origin} list, and acquiring needs the provider's own track "
            f"identifiers, which only a list fetched from the provider carries",
            "fetch the playlist from the provider into a list document first, "
            "then acquire that",
            "a pasted tracklist is matched against the library with match.run; "
            "its missing rows carry acquisition options, not identifiers",
            origin=origin,
        )

```

New text:

```
(empty)
```

### `u54-zero-row-remeasured.G7_staging_cleared`

Keep whatever a killed attempt left in the item's staging directory, re-measured after the fake was taught to skip

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-zero-row-remeasured.json`, row `G7_staging_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)

```

New text:

```
(empty)
```

### `u80.F15_empty_offered`

A row with no candidate is offered as an empty item rather than reported

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F15_empty_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_provider_route_beside_an_unfound_row_is_reported_not_refused`
  - `tests/test_acquire_fallback.py::test_a_row_with_none_beside_a_row_offered_is_a_failing_check`
  - `tests/test_acquire_fallback.py::test_no_candidate_anywhere_refuses_and_names_the_row`
  - `tests/test_acquire_fallback.py::test_unreadable_lines_are_counted_on_a_row_with_none`

Old text:

```
    on_screen = ranked(wanted, answer)
    if not on_screen:
```

New text:

```
    on_screen = ranked(wanted, answer)
    if False:
```

### `u81-fetch-b.L1_two_files_first_wins`

A download that left two MP3 files hands the first one on as the track

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `L1_two_files_first_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_never_reads_a_failure_as_a_file[two]`

Old text:

```
    if len(found) != 1:
```

New text:

```
    if len(found) == 0:
```

### `u80.C3_dedupe_on_match_id`

Rows are deduplicated on the match id, which carries the key

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80.json`, row `C3_dedupe_on_match_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_one_track_with_and_without_a_key_is_searched_once`

Old text:

```
            asked = fallback.item_id(one.wanted)
```

New text:

```
            asked = one.match_id
```

### `u81-fetch-a.W6_post_landing_exists`

A file that appeared during the download is no longer checked, so the engine commits over it

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W6_post_landing_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_output_that_appears_during_the_download_is_refused_not_replaced`

Old text:

```
    if final.exists():
        raise _exists(final, detail)
```

New text:

```
    if False:
        raise _exists(final, detail)
```

### `u81-fetch-b.W4_empty_stem_rerun`

Re-run of W4: a row naming no artist and no title is fetched and committed

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `W4_empty_stem_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_naming_no_artist_and_no_title_is_refused_before_a_download`

Old text:

```
    if not stem:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r1016.M8_walk_name_ignored`

_client_part's refusal names the folder listing whatever walk it was called for, so the account walk blames the wrong listing

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M8_walk_name_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_user_without_the_parts_the_account_walk_reaches_is_refused_by_name`

Old text:

```
                f"changed shape and the {walk} needs updating with it"
            )
    return value
```

New text:

```
                f"changed shape and the folder listing needs updating with it"
            )
    return value
```

### `r878-a.A1_paginate_refuses_cursor`

paginate: drop the refusal of a cursor shape, so an offset walk can run over the folder endpoint again

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A1_paginate_refuses_cursor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_paginate_refuses_a_shape_that_walks_by_cursor`

Old text:

```
    if stop is StopRule.CURSOR:
```

New text:

```
    if False:
```

### `r878-b.B11_folder_rule_in_table`

STOP_RULES: put account_folders back on the empty page rule, the offset walk R-878 found

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B11_folder_rule_in_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 20 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_client_whose_request_rejects_the_arguments_refuses_by_name_unslept`
  - `tests/test_adapter_listing.py::test_a_cursor_that_never_changes_spends_the_budget_and_refuses`
  - `tests/test_adapter_listing.py::test_a_folder_served_on_two_pages_is_returned_once`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[a-list]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[items-null]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[no-items-no-count]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[nothing]`
  - `tests/test_adapter_listing.py::test_a_response_with_no_cursor_ends_the_walk`
  - `tests/test_adapter_listing.py::test_a_short_walk_over_a_mixed_root_still_refuses`
  - `tests/test_adapter_listing.py::test_a_transient_failure_retries_the_same_cursor_and_not_the_first_page`
  - `tests/test_adapter_listing.py::test_a_walk_that_collects_fewer_than_the_declared_count_refuses`
  - `tests/test_adapter_listing.py::test_an_empty_page_ends_the_walk_even_when_it_carries_a_cursor`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_adapter_listing.py::test_paginate_refuses_a_shape_that_walks_by_cursor`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    "account_folders": StopRule.CURSOR,
```

New text:

```
    "account_folders": StopRule.EMPTY_PAGE,
```

### `u65.A1_stop_gets_a_default`

stop becomes optional, so a new wrapper inherits an assumption instead of choosing

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `A1_stop_gets_a_default`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_paginate_refuses_to_be_called_without_a_declared_rule_or_budget[stop]`

Old text:

```
    stop: StopRule,
    max_pages: int,
```

New text:

```
    stop: StopRule = StopRule.SHORT_PAGE,
    max_pages: int,
```

### `u65.C2_an_empty_page_ends_a_declared_total_walk`

the empty middle window ends the walk again, the exact defect the review found

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C2_an_empty_page_ends_a_declared_total_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`

Old text:

```
            if offset >= total and len(page) < page_size:
                break
        elif not page:
            break
```

New text:

```
            if offset >= total and len(page) < page_size:
                break
        if not page:
            break
```

### `u65.E3_the_favourites_total_is_never_wired`

the shape declares the total rule and is handed no total, so it degrades silently

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E3_the_favourites_total_is_never_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
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
    kwargs.setdefault("declared_total", lambda: None)
```

### `r679-b.B1_no_retirement`

adjudicate: never retire, so an owned row leaves its question open

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B1_no_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        if owned_by_a_rule(found):
```

New text:

```
        if False:
```

### `r664.E4_title_not_split`

Skip split_title on the chosen title, so a version stays inside the recording token

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E4_title_not_split`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 106 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - ... and 91 more, see the JSON sidecar

Old text:

```
    title, version = split_title(spelled)

```

New text:

```
    title, version = spelled, ""

```

### `u274.P4_sweep_live`

sweep_orphans: drop the process check, so every directory of the form is removed, a live drive's token included

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P4_sweep_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 450 against a baseline of 450
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_an_answer_that_judges_no_session_keeps_the_client`
  - `tests/test_provider_session_hold.py::test_the_surveys_drive_logs_in_once_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_a_directory_whose_process_it_cannot_see`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_alone_what_it_cannot_prove_is_an_orphan[own-process]`

Old text:

```
        if owned is None or not _gone(int(owned.group(1))):

```

New text:

```
        if owned is None:

```

### `r703-b.L1_no_active_exception`

the tool's log ignores the exception being handled and keeps only the message

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `L1_no_active_exception`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_an_error_the_tool_logs_from_its_except_is_the_cause`
  - `tests/test_adapter_contract.py::test_the_first_exception_the_tool_logs_is_the_cause_not_its_consequence`
  - `tests/test_adapter_contract.py::test_the_providers_exception_outranks_a_message_the_tool_logged_first`

Old text:

```
        active = sys.exc_info()[1]
```

New text:

```
        active = None
```

### `r703-c.C1_last_exception_wins`

Batch B's L2 again after its test: a later exception overwrites the first

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-c.json`, row `C1_last_exception_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_first_exception_the_tool_logs_is_the_cause_not_its_consequence`

Old text:

```
        if self._exception is None:
            self._exception = exc
```

New text:

```
        self._exception = exc
```

### `u47-author.CODEC_policy_ignored`

Run the check under every policy, so a permitted lossy acquisition is refused too

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_policy_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_permitted_lossy_policy_does_not_refuse_the_landing`

Old text:

```
    if policy is not LosslessPolicy.STRICT:
        return path
```

New text:

```
(empty)
```

### `u47-author.R196_login_without_pkce`

Authenticate with PKCE off, which is the call that produced lossy audio for every download since July

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_login_without_pkce`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_adapter_authenticates_with_pkce_on`

Old text:

```
            authorised = tidal.login_token(do_pkce=True)
```

New text:

```
            authorised = tidal.login_token()
```

### `u47-author.R197_event_run_left_clear`

Pass event_run unset, the realistic nearby value: every segment worker then waits on something nothing wakes, so the failure is a hang rather than an error

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_event_run_left_clear`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
    event_run = Event()
    event_run.set()
    return Event(), event_run
```

New text:

```
    event_run = Event()
    return Event(), event_run
```

### `u254.M03_cache_identity_no_size`

_as_left: leave the size out of the identity, so a same inode file another hand changed reads as left

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M03_cache_identity_no_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)
```

New text:

```
    return (found.st_dev, found.st_ino, 0, found.st_mtime_ns)
```

### `u254.M12_header_upgrade`

_read_journal: drop the upgrade refusal of a newer journal header

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M12_header_upgrade`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header from a newer build]`

Old text:

```
            f"{SCHEMA_VERSION}",
            Remedy.UPGRADE_CRATEKIT,
        )
    if version != SCHEMA_VERSION:
```

New text:

```
            f"{SCHEMA_VERSION}",
            Remedy.RUN_DOCTOR,
        )
    if version != SCHEMA_VERSION:
```

### `u254.M20_mark_unlocked`

mark_applied: take no lock around the read, the choice and the write

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M20_mark_unlocked`
- Moved: Same with statement in mark_applied; U298 renamed config._exclusive_lock to exclusive_lock
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_every_ledger_write_happens_under_the_exclusive_lock`

Old text:

```
    with config.exclusive_lock(lock_path(cfg)):
        known = _LEFT.pop(key, None)
```

New text:

```
    if True:
        known = _LEFT.pop(key, None)
```

### `r731-b.M14_gate_without_the_count`

the gate's facts no longer carry the withheld count split by kind

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M14_gate_without_the_count`
- Moved: the gate's facts are now read through the _FACTS key list; dropping withheld_by_placement from it is the same omission
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    "placements",
    "withheld_by_placement",

```

New text:

```
    "placements",

```

### `u27-adopt-apply-author.A1_approval_actor_is_the_process`

Mint the approval under a fixed actor, so the record cannot say who asserted it

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A1_approval_actor_is_the_process`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`
- Collected: 632 against a baseline of 632
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
            approval=grant(plan, actor=actor),
```

New text:

```
            approval=grant(plan, actor="cli"),
```

### `u55-collection-reader.R19_collector_groups_locations`

The collector groups content identifiers again, which is the seam defect U55 found

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R19_collector_groups_locations`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`

Old text:

```
            into.setdefault((folder, sub), []).append(entry.path)
```

New text:

```
            into.setdefault((folder, sub), []).append(entry.content_id)
```

### `u23-round-8-independent.X1_approval_type_check_never_fires`

R34: a blanket affirmative is no longer refused by type

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X1_approval_type_check_never_fires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 7 (killed)
- Killed:
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[NoneTypeNone]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[boolTrue]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[dict{'approved':]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[dict{'digest': ']`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[int1]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[strapprove]`
  - `tests/test_adoption.py::test_no_blanket_affirmative_applies_a_plan[stryes]`

Old text:

```
    if not isinstance(approval, Approval):
```

New text:

```
    if not isinstance(approval, object):
```

### `r758-b.M2_unnamed_genre_is_moved`

a track whose genre names no style is moved to the resolver's default

- File: `src/cratekit/adopt/move.py`
- Source: `r758-b.json`, row `M2_unnamed_genre_is_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_genre_that_stopped_naming_the_style_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_the_genre_decides_a_style_move_and_a_genre_naming_no_style_is_left`

Old text:

```
    return "" if entry.genre in by_source.map else LEFT_NO_STYLE
```

New text:

```
    return ""
```

### `r780-a.A6_every_entry_claims_its_bucket`

a verdict withheld entry claims its bucket, so it goes to the R-758 path, which returns nothing for it, and the double is neither moved nor listed

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A6_every_entry_claims_its_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_a_verdict_withheld_since_the_approval_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_verdict_withheld_double_is_left_and_listed_under_its_own_reason`

Old text:

```
    if entry.disposition is Disposition.ROUTE:
        return True
    return entry.disposition is Disposition.WITHHELD and entry.held_elsewhere
```

New text:

```
    return True
```

### `u118-c.M2_holder_genre_leg`

The holder settles its places only for an entry claiming Soul, not for one whose genre names it

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M2_holder_genre_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`

Old text:

```
        elif claims(entry, declarer) or genre_names(entry, declarer, declared):
```

New text:

```
        elif claims(entry, declarer):
```

### `r758-b.C3_rows_not_proven_against_the_digest`

the digest of the frozen rows is not taken again, so edited rows are shown and performed under the approved digest

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C3_rows_not_proven_against_the_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`

Old text:

```
    if not (taken == stated == queued_under):
```

New text:

```
    if not (stated == queued_under):
```

### `u340.R28_worker_no_elsewhere`

handle: read the moves back with no other entry's buckets, so a written split pair move is reported in both (round two)

- File: `src/cratekit/adopt/move_cli.py`
- Source: `u340.json`, row `R28_worker_no_elsewhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 816 against a baseline of 816
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[rnb]`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[soul]`

Old text:

```
        cfg, declared, approved, gone, move_engine.claimed_buckets(current.entries)
```

New text:

```
        cfg, declared, approved, gone, {}
```

### `r788-c.L6_removed_node_is_a_place`

_indexed: a playlist rekordbox removed is indexed with the live ones, for both readers. The existing guard this unit moved into a shared body

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L6_removed_node_is_a_place`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_removed_vocal_playlist_is_not_a_place`

Old text:

```
    live = [node for node in nodes if not node.removed]
```

New text:

```
    live = list(nodes)
```

### `r1965.R25_sample_vocal_sub`

sample: vocal_sub answers the vocal class in every bucket, colliding ones included

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R25_sample_vocal_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 9 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_bucket_declaring_a_sub_of_the_vocal_identifier_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_that_has_no_vocal_sub_is_not_read_for_one`
  - `tests/test_adopt_vocals.py::test_a_bucket_whose_band_is_labelled_with_the_vocal_name_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_whose_own_sub_carries_the_vocal_name_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_with_no_vocal_sub_plans_nothing_for_its_tagged_tracks`
  - `tests/test_adopt_vocals.py::test_a_taxonomy_with_no_vocal_class_plans_nothing_for_any_tagged_track`
  - `tests/test_adopt_vocals.py::test_a_taxonomy_with_no_vocal_sub_says_so_whatever_else_is_true`
  - `tests/test_adopt_vocals.py::test_no_additive_class_of_the_vocal_identifier_is_no_vocal_sub`
  - `tests/test_adopt_workers.py::test_a_calibration_that_cannot_be_read_refuses_before_the_library_is_walked`

Old text:

```
    return VOX_SUB_CLASS if VOX_SUB_CLASS in derived_classes(declared, bucket_id) else None
```

New text:

```
    return VOX_SUB_CLASS
```

### `r731-a.M01_unread_tree_withholds`

a tree nobody read is treated as read, so held subs a caller carried withhold

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M01_unread_tree_withholds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_an_unread_tree_withholds_nothing_even_when_it_carries_held_subs`

Old text:

```
    if not placements.read:
        return NO_COMPETING_PLACE
    kind, competing
```

New text:

```
    kind, competing
```

### `r731-a.M11_verdict_withheld_on_the_review_list`

an entry a collision verdict withheld is listed as holding a place

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M11_verdict_withheld_on_the_review_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_collision_verdict_withholds_under_its_own_reason_and_own_count`

Old text:

```
        return self.disposition is Disposition.WITHHELD and bool(self.holds)
```

New text:

```
        return self.disposition is Disposition.WITHHELD
```

### `r788-a.P8_renamed_bucket_doubles`

vocal_place: a bucket whose vocal sub answers under another name only is added to, so the writer makes a second playlist beside it

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P8_renamed_bucket_doubles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_track_whose_bucket_has_its_vocal_sub_under_another_name_only_is_not_added`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if bucket in vocals.renamed:
        return VOCAL_RENAMED, sub
```

New text:

```
    if False:
        return VOCAL_RENAMED, sub
```

### `u956.O13_outside_list_every_excluded`

AdoptionPlan.outside_root: list every excluded row, so the gate names a missing or unmapped row as outside the root

- File: `src/cratekit/adopt/plan.py`
- Source: `u956.json`, row `O13_outside_list_every_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`
- Collected: 658 against a baseline of 658
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`
  - `tests/test_adopt_outside_root.py::test_the_plan_counts_and_names_every_row_it_leaves_outside`

Old text:

```
            entry for entry in self.firsts() if entry.category is Readability.OUTSIDE_ROOT
```

New text:

```
            entry for entry in self.firsts() if entry.disposition is Disposition.EXCLUDED
```

### `u23-round-8-independent.A4_at_risk_drops_the_record_value`

The value the record says adoption wrote no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A4_at_risk_drops_the_record_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`

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
    return held in ((written,),)

```

### `u23-round-8-independent.D2_bytes_agree_size_gate_inverted`

The size shortcut refuses on AGREEING sizes

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `D2_bytes_agree_size_gate_inverted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 6 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[both]`
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[inode-renumbered]`
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[mounted-in-another-order]`
  - `tests/test_adoption.py::test_a_file_RENAMED_between_two_adoptions_is_still_one_record`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
```

New text:

```
    if record.size is not None and size_here is not None and record.size == size_here:
```

### `r759.A1_deadline_asked_only_at_the_end`

the read deadline is asked only after the stream has ended, so a trickling file is read to its end before the timeout is raised

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r759.json`, row `A1_deadline_asked_only_at_the_end`
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
                if not block:
                    break
                hasher.update(block)
                if time.monotonic() > give_up_at:
                    raise TimeoutError(
                        f"{path} did not finish arriving within "
                        f"{deadline_seconds} seconds"
                    )

```

New text:

```
                if not block:
                    if time.monotonic() > give_up_at:
                        raise TimeoutError(
                            f"{path} did not finish arriving within "
                            f"{deadline_seconds} seconds"
                        )
                    break
                hasher.update(block)

```

### `r722.S4_default_reader_lenient`

The census's default reader is the lenient one, which folds failures into None

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S4_default_reader_lenient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 692 against a baseline of 692
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
    energy_reader: Callable[[Path], int | None] = tags.read_energy_checked,
```

New text:

```
    energy_reader: Callable[[Path], int | None] = tags.read_energy_from_file,
```

### `u956.O10_root_not_composed`

within_root: compare the root's own composition form, so a root spelled decomposed reads every row outside it

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O10_root_not_composed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/vol/lib/Caf\xe9/a.flac-/vol/lib/Cafe\u0301-True]`

Old text:

```
    anchor = posixpath.normpath(locations.norm_for_compare(str(root)))
```

New text:

```
    anchor = posixpath.normpath(str(root))
```

### `u956.O8_dots_not_read`

within_root: compare the path without reading its dots, so a path that climbs out of the root by .. reads inside it

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O8_dots_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 641 against a baseline of 641
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/vol/lib/../srv/Sampler/a.wav-/vol/lib-False]`

Old text:

```
    wanted = posixpath.normpath(locations.norm_for_compare(str(path)))
```

New text:

```
    wanted = locations.norm_for_compare(str(path))
```

### `u241.M14_a_changed_file_keeps_its_old_head`

ahead: a head measured ahead is used whatever file now sits at the path

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M14_a_changed_file_keeps_its_old_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_replaced_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_at_the_same_length_is_measured_again_by_its_time_alone`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_in_place_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`

Old text:

```
    if measured_identity is None or measured_identity != identity_of(path):

```

New text:

```
    if False:

```

### `u223.M22_discard_unlinks_directory`

discard_rename_evidence: unlink a directory at the report name, failing the item for good

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M22_discard_unlinks_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`

Old text:

```
        if entry.is_symlink() or not entry.is_dir():
            entry.unlink(missing_ok=True)
```

New text:

```
        if True:
            entry.unlink(missing_ok=True)
```

### `u223.M7_report_any_item`

staged_report: accept a report for another item

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M7_report_any_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_rename_intent_for_another_item_or_a_gone_target_is_not_a_twin`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    if not isinstance(loaded, dict):
        return None
    return loaded
```

### `u90-a.A4_max_coefficient`

The score range's top moved from 100 to 1000

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A4_max_coefficient`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte`

Old text:

```
VOCAL_SCORE_MAX = 100.0
```

New text:

```
VOCAL_SCORE_MAX = 1000.0
```

### `u90-b.B6_hand_detail_drops_old_cut`

The hand path's check detail stops naming the cut it replaced

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B6_hand_detail_drops_old_cut`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
f"cut set by hand at {cut:g}, written to {target}; {before}; "
```

New text:

```
f"cut set by hand at {cut:g}, written to {target}; "
```

### `u94-a.S4_accept_flag_dead`

analyze_calibrate: read --accept-partial as always false, so the flag the refusal names does nothing

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S4_accept_flag_dead`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`
  - `tests/test_analysis_workers.py::test_a_single_cluster_is_not_cut_down_the_middle`
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`
  - `tests/test_analysis_workers.py::test_calibrate_cuts_the_vocal_threshold_between_the_two_clusters`
  - `tests/test_analysis_workers.py::test_calibrate_fits_the_energy_reference_over_a_folder_and_writes_it`
  - `tests/test_analysis_workers.py::test_calibrate_over_an_empty_folder_is_a_failed_check_not_a_traceback`
  - `tests/test_analysis_workers.py::test_calibrate_over_too_few_tracks_writes_nothing_and_says_so`
  - `tests/test_analysis_workers.py::test_calibrate_without_the_extra_refuses_rather_than_fitting_over_nothing`

Old text:

```
    accepted = bool(ctx.args.accept_partial)
```

New text:

```
    accepted = False
```

### `u94-b.W5_warning_without_a_write`

analyze_calibrate: warn about what was written when neither half wrote anything

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W5_warning_without_a_write`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_partial_fit_that_wrote_nothing_does_not_warn_about_a_calibration`

Old text:

```
if partial is not None and wrote else ())
```

New text:

```
if partial is not None else ())
```

### `u94-c.N5_note_m_is_the_sample`

analyze_calibrate: record the sample size as M, so the note reads N of N and hides how much of the library was fitted

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N5_note_m_is_the_sample`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`

Old text:

```
        _calibrate_energy(cfg, folder, sampled, len(paths), left_out),
```

New text:

```
        _calibrate_energy(cfg, folder, sampled, len(sampled), left_out),
```

### `u223.M12_renamed_to_unchecked`

_staged_twin: accept an analysed report whatever its renamed_to says

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M12_renamed_to_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
        if report.get("renamed_to") != target.name:
            return None
```

New text:

```
        pass
```

### `u241.M21_no_check_line_on_the_answer`

_resume: the answer no longer carries the analyze.pool check

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M21_no_check_line_on_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_closure_bound_by_a_test_is_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it`
  - `tests/test_analysis_ahead.py::test_a_job_whose_record_is_gone_says_it_does_not_know`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_pool_record_that_cannot_be_written_is_a_missing_line_and_never_a_failed_job`
  - `tests/test_analysis_ahead.py::test_a_resume_of_a_finished_job_still_says_what_pool_it_ran_with`
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`
  - `tests/test_analysis_ahead.py::test_a_worker_that_dies_costs_the_run_nothing_but_its_pool`
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`
  - `tests/test_analysis_ahead.py::test_the_person_reads_the_check_line_without_asking_for_json`
  - `tests/test_analysis_ahead.py::test_two_cores_leave_no_ceiling_for_a_pool`

Old text:

```
            summary["checks"] = [_pool_check(artifacts.pool_record(cfg, job.job_id))]

```

New text:

```
(empty)
```

### `u343.M03_untitled_overwrites_a_title`

_untitled: answer the stem for a file that has a title too, so the run overwrites a title tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M03_untitled_overwrites_a_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_restamp_scored_by.py`
- Collected: 324 against a baseline of 324
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[a-title-kept]`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
    if (tags.read_tag(path, "title") or "").strip():
        return None
```

New text:

```
    if False:
        return None
```

### `u58-workers-and-wav.R4_keyless_finalized`

Finalize a track whose head found no key

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R4_keyless_finalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_an_undecodable_file_is_its_own_terminal_and_not_a_keyless_track`

Old text:

```
    if partial.get("terminal") is not None:
        return artifacts.produced(
            cfg, job, item, {"item": item.item_id, "path": str(path), "status": partial["terminal"]}
        )

```

New text:

```
(empty)
```

### `u263.D12_channels_first`

_ffmpeg_samples: leave the samples frames first, not librosa's channels first

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D12_channels_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[broken-png]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[gif-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[webp-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[2]`
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[6]`
  - `tests/test_analysis_decode.py::test_an_ffmpeg_that_exits_non_zero_saying_nothing_fails`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_the_one_decoded`

Old text:

```
    native = frames.reshape(-1, channels).T
```

New text:

```
    native = frames.reshape(channels, -1)
```

### `u263.D6_window_round`

_window: round the frame count rather than truncate it as libsndfile does

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D6_window_round`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return native[..., start : start + int(duration * native_rate)]
```

New text:

```
    return native[..., start : start + round(duration * native_rate)]
```

### `u264.M1_fast_path_never`

mono: never take the one add, so every mix is librosa.to_mono (the speed is lost, the samples are not)

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M1_fast_path_never`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        and samples.shape[0] == 2
        and samples.dtype == np.float32
    )
```

New text:

```
        and samples.shape[0] == 2
        and samples.dtype == np.float32
        and False
    )
```

### `u264.M9_read_at_target_rate`

decode.load: read through librosa.load at the target rate, so the channels are resampled before the mix rather than after

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M9_read_at_target_rate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        native, native_rate = librosa.load(str(path), sr=None, mono=False, **window)
```

New text:

```
        native, native_rate = librosa.load(str(path), sr=rate, mono=False, **window)
```

### `u157.D8_percentile`

DRIFT_PERCENTILE: the whole range instead of the tenth to ninetieth

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D8_percentile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
DRIFT_PERCENTILE = 10.0
```

New text:

```
DRIFT_PERCENTILE = 0.0
```

### `u344.M3_head_unavailable_reads_calibrated`

energy_from_path: name a level the features could not give as calibrated

- File: `src/cratekit/analysis/detect.py`
- Source: `u344.json`, row `M3_head_unavailable_reads_calibrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_warm.py`, `tests/test_energy_one_measure_librosa.py`, `tests/test_analysis_ahead.py`
- Collected: 497 against a baseline of 497
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_detector_names_why_energy_is_what_it_is`

Old text:

```
    if features is None:
        return None, energy.STATUS_FEATURES_UNAVAILABLE
    return energy.level_for
```

New text:

```
    if features is None:
        return None, energy.STATUS_CALIBRATED
    return energy.level_for
```

### `u327.A15_digest_covers_items`

AdoptPlan.digest: digest the counts and not the items, so a changed answer with the same counts is approved

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A15_digest_covers_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_stamped_row_moved_between_plan_and_apply_refuses_and_writes_nothing`
  - `tests/test_analyze_adopt.py::test_a_title_changed_between_plan_and_apply_refuses_and_writes_nothing`

Old text:

```
                "items": [item.digested() for item in self.items],
                "counts": dict(self.counts),
```

New text:

```
                "counts": dict(self.counts),
```

### `u327.A6_key_id_empty`

reference_key: drop the empty KeyID check, so a KeyID of zero beside a named key row is read as a key

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A6_key_id_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_key_column_reads_in_either_notation_or_says_why_it_does_not[0-8A-expected10]`
  - `tests/test_analyze_adopt.py::test_the_key_column_reads_in_either_notation_or_says_why_it_does_not[0-8A-expected9]`
  - `tests/test_analyze_adopt.py::test_the_key_column_reads_in_either_notation_or_says_why_it_does_not[None-8A-expected8]`

Old text:

```
    if key_id in rb_writer.FIELD_EMPTIES["KeyID"] or not str(scale_name or "").strip():
```

New text:

```
    if not str(scale_name or "").strip():
```

### `u342.P1_never_stamped_half`

plan_row: stamp a headless row whose key or tempo is missing, as long as one half is there

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P1_never_stamped_half`
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
        if key is None or tempo is None:
            return Item(content_id, LEAVE_ACTION, reason=NO_HEAD_UNANSWERED, **common)
```

New text:

```
        if key is None and tempo is None:
            return Item(content_id, LEAVE_ACTION, reason=NO_HEAD_UNANSWERED, **common)
```

### `u342.P9_stamped_key_tag`

plan_row: give only a corrected row rekordbox's key tag, never a stamped one

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P9_stamped_key_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
    if key is not None and parse_camelot(initialkey) != parse_camelot(key):
```

New text:

```
    if action == ADOPT and key is not None and parse_camelot(initialkey) != parse_camelot(key):
```

### `u275.M1_base_back_to_linux`

LIGHT_BASE_BYTES back to U241's 320 megabytes, the figure before the Mac was measured

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M1_base_back_to_linux`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 555 against a baseline of 555
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[729-2346]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BASE_BYTES = 384 * 1024 * 1024
```

New text:

```
LIGHT_BASE_BYTES = 320 * 1024 * 1024
```

### `u343.M08_resume_reads_the_name_alone`

already_analyzed: read only the head on the name, so a file marked since U343 is measured again

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M08_resume_reads_the_name_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`, `tests/test_analysis_ahead.py`
- Collected: 503 against a baseline of 503
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_batch_resume_skips_a_file_carrying_the_mark_and_reads_the_rest`
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_reads_the_head_by_the_rule_analyze_run_skips_by`

Old text:

```
    return has_head(path.name, template=template) or marked(path)
```

New text:

```
    return has_head(path.name, template=template)
```

### `sitting3.G15_fold_any_ragged_tail`

Fold every tail shorter than the chunk, not only one under the floor

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G15_fold_any_ragged_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`

Old text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)

```

New text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else chunk_samples

```

### `u263.D17_vocal_reraise`

vocal.decode: swallow a missing decoder as an undecodable file

- File: `src/cratekit/analysis/vocal.py`
- Source: `u263.json`, row `D17_vocal_reraise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except decoder.DecoderMissing:
        raise

```

New text:

```
(empty)
```

### `u58-workers-and-wav.W7_undecodable_reason_reworded`

Reword the undecodable reason, do not append

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W7_undecodable_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`

Old text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-undecodable"
```

New text:

```
REASON_AUDIO_UNDECODABLE = "vocal-audio-unreadable"
```

### `u92-author.G7_reason_reworded`

Reword the reason slug, never append, since the suite asserts with equality and with in

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G7_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`

Old text:

```
REASON_AUDIO_TOO_LARGE = "vocal-audio-too-large"
```

New text:

```
REASON_AUDIO_TOO_LARGE = "vocal-file-oversize"
```

### `r221-a.W3_queue_branch_warning_dropped`

The identifier is handed back with no word about what it will do, and the detached child a resume spawns writes to a log nobody is watching

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W3_queue_branch_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
                *map(dict, backup.snapshot_identity_warning(cfg)),
                *_rehearsal(job),
            ),
        )
```

New text:

```
                *map(dict, backup.snapshot_identity_warning(cfg)),
            ),
        )
```

### `r222-b.B11_finished_jobs_are_twins`

Read every state from the queue, so a backup that is over stands in for a new one for ever

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B11_finished_jobs_are_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`

Old text:

```
    for job in jobs.list_jobs(store, states=open_states):
```

New text:

```
    for job in jobs.list_jobs(store):
```

### `r222-b.B6_itemless_job_is_a_twin`

Report a job with no items, which refuses when driven, as the backup asked for

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B6_itemless_job_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_job_that_is_not_this_backup_does_not_stand_in_for_it[itemless]`

Old text:

```
        if not jobs.items(store, job.job_id):
            continue
        try:
```

New text:

```
        if False:
            continue
        try:
```

### `r349-a.A4_envelope_field`

The backup run --job envelope stops attaching the outcomes field

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A4_envelope_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`

Old text:

```
        progress[OUTCOMES] = outcomes
```

New text:

```
        pass
```

### `r757-c2.S5_unread_number_printed_as_zero`

comparison_warning: print a total that was not read as 0

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S5_unread_number_printed_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 728 against a baseline of 728
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

### `u45-round-1.C4_uniform_refusal_flattened`

Drop the uniform pass-through so every no-run refusal becomes the summary slug and rclone-missing loses install-binary

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C4_uniform_refusal_flattened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`

Old text:

```
    if len(refusals) == 1:
        only = next(iter(refusals))
```

New text:

```
    if False:
        only = next(iter(refusals))
```

### `u45-round-1.R1_reserved_remediation_discarded`

Replace the reservation table's per-slug remediation with the class default, which is what the first draft did

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `R1_reserved_remediation_discarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
            remediation=reservations.remediation_for(slug),
```

New text:

```
            remediation=Remediation(),
```

### `u45-round-2.A3_age_seconds_always_none`

Report no age number even for a known portion, so the value R15's warning quotes never reaches the report

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-2.json`, row `A3_age_seconds_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
            "age_seconds": entry.age.total_seconds() if entry.age is not None else None,
```

New text:

```
            "age_seconds": None,
```

### `u50-zero-rows.B2_items_hardcoded_pair`

Name the two portions instead of deriving them, so a third portion is queued by nobody

- File: `src/cratekit/backup/cli.py`
- Source: `u50-zero-rows.json`, row `B2_items_hardcoded_pair`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return ("files", "database")
```

### `u248.L4_listing_drops_the_stub_line`

ask_for_listing: a missing extra no longer makes the stub, so the listing omits (requires the extra)

- File: `src/cratekit/cli/__init__.py`
- Source: `u248.json`, row `L4_listing_drops_the_stub_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_lazy.py`, `tests/test_cli_contract.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`
- Collected: 1235 against a baseline of 1235
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_missing_analysis_extra_names_the_install_command`
  - `tests/test_cli_contract.py::test_a_module_with_missing_extras_becomes_a_stub_that_names_the_install_command`
  - `tests/test_cli_lazy.py::test_a_blocked_extra_still_lists_the_stub_line_and_refuses_with_the_install_command`
  - `tests/test_vocals_cli.py::test_a_missing_vocals_extra_names_the_install_command`

Old text:

```
            if _is_missing_extra(exc, self.entry):
                self._stub(exc)
```

New text:

```
            if _is_missing_extra(exc, self.entry):
                pass
```

### `r925.J2_playlist_excluded`

job show lists tracks for a set job only, not a playlist job

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J2_playlist_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`
  - `tests/intake/test_workers.py::test_the_intake_keys_resolve_to_the_one_worker_and_the_job_verbs_spell_them_alike`

Old text:

```
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set", "intake.playlist"})
```

New text:

```
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set"})
```

### `u42-author.R1_planned_marker_returns`

Restore planned_in on acquire.download, which is the state that hid rows 6 and 7

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u42-author.json`, row `R1_planned_marker_returns`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_cutover_parity.py`, `tests/test_cli_contract.py`
- Collected: 1049 against a baseline of 1052
- Kills: 7 (collect-error)
- Note: collection changed: 1049 collected against a baseline of 1052. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_acquire_cli.py::test_download_argv_round_trips_the_frozen_payload_and_carries_no_run`
  - `tests/test_acquire_cli.py::test_download_on_an_absent_job_refuses_with_a_vocabulary_code`
  - `tests/test_acquire_cli.py::test_download_over_an_absent_list_refuses_by_name`
  - `tests/test_acquire_cli.py::test_download_reaches_no_provider_and_no_network`
  - `tests/test_acquire_cli.py::test_the_verb_appears_in_help_and_dispatches[acquire.download]`
  - `tests/test_acquire_cli.py::test_the_verb_is_landed_rather_than_planned[acquire.download]`
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`

Old text:

```
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        # Landed (U42).
```

New text:

```
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        planned_in="U15",
        # Landed (U42).
```

### `r685-a.L2_an_unmounted_library_falls_back`

Drop the library root check, so an absent volume reads as no active copy and routes by the shipped template

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L2_an_unmounted_library_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_routing_workers.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`
- Collected: 350 against a baseline of 350
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[library-root-absent]`
  - `tests/test_active_taxonomy.py::test_a_library_unmounted_after_a_good_load_still_refuses`

Old text:

```
        if not cfg.library.root.is_dir():

```

New text:

```
        if False:

```

### `u260.D1_decodes_always`

decodes: answer True for any bytes, so the shipped admission admits what is not a picture

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `D1_decodes_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_an_answer_the_admission_refuses_is_handed_on_and_not_remembered`
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`

Old text:

```
    return _measure(data) is not None
```

New text:

```
    return True
```

### `u260.E6_encode_never_remembered`

to_cdj_jpeg_remembered: never answer from memory

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E6_encode_never_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 11 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_different_bytes_are_encoded_apart`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_encode_memory_drops_the_least_recently_used`
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
        made = _remembered.get(key)
        if made is not None:
```

New text:

```
        made = None
        if made is not None:
```

### `u83-a.E3_ladder_ends_on_floor`

The ladder loses its last rung, so quality 50 is never tried, the defect the suite caught while building

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E3_ladder_ends_on_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
    return [*rungs, ART_MIN_QUALITY]
```

New text:

```
    return rungs
```

### `u83-a.R3_unknown_depth_default`

An unlisted Pillow mode measures as a guessed 24 again instead of 0

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R3_unknown_depth_default`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_mode_with_no_known_depth_reads_as_zero_not_as_a_guess`

Old text:

```
depth=_DEPTH_BY_MODE.get(img.mode, 0),
```

New text:

```
depth=_DEPTH_BY_MODE.get(img.mode, 24),
```

### `u83-b.W5_cap_guard`

The writer accepts a picture over the byte cap

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W5_cap_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_picture_over_the_cap_is_refused_and_the_file_untouched`
  - `tests/test_art.py::test_the_writer_default_cap_is_the_encoder_default_cap`

Old text:

```
    if len(jpeg) > max_bytes:
```

New text:

```
    if False:
```

### `r757-b2.F1_absent_key_reads_as_never`

_full_comparison: a file from a build with one mode answers never, over a library whose every backup was a full one

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F1_absent_key_reads_as_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 728 against a baseline of 728
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_fact_file_from_a_build_with_one_mode_reads_as_a_full_comparison`

Old text:

```
    if held is _ABSENT:
        return facts.get(Portion.FILES)
```

New text:

```
    if held is _ABSENT:
        return None
```

### `example-binaries-five-row.B3_platform_binary_remedy`

A platform-provided binary reports INSTALL_BINARY instead of UNSUPPORTED_PLATFORM, so the CLI would tell a user to install something the operating system ships.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B3_platform_binary_remedy`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_the_binary_failures_carry_four_different_remedies`

Old text:

```
            remedy=Remedy.UNSUPPORTED_PLATFORM,

```

New text:

```
            remedy=Remedy.INSTALL_BINARY,

```

### `u27-r80-write-probe-replacement.W8_read_probe_flags`

Make the read probe write capable, the shape the reports allowlist forbids

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W8_read_probe_flags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`
- Collected: 358 against a baseline of 358
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_the_allowlist_admits_no_writer_this_guard_cannot_name`

Old text:

```
        handle = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
```

New text:

```
        handle = os.open(path, os.O_RDWR | os.O_NONBLOCK)
```

### `u197-m6.M6_composite`

What the default does hold: default to the alternative, a name the fold leaves alone, so a fresh configuration selects streamrip

- File: `src/cratekit/core/config_schema.py`
- Source: `u197-m6.json`, row `M6_composite`
- Moved: the same text, now in src/cratekit/core/config_schema.py, was in src/cratekit/core/config.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`
- Collected: 827 against a baseline of 827
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_configured_adapter_name_resolves_through_the_registry`
  - `tests/test_config.py::test_the_vendored_adapter_is_the_default_under_its_neutral_name`

Old text:

```
    adapter: str = "vendored"
```

New text:

```
    adapter: str = "streamrip"
```

### `r290-author.J7_cancelled_raises_the_plain_type`

Raise a plain CratekitError for a cancelled job, so a person who stopped a run is told it failed

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J7_cancelled_raises_the_plain_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 25 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[backup.run]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[export.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.playlist]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[intake.set]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.import]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
            raise JobCancelled(job.cause)
```

New text:

```
            raise CratekitError(job.cause)
```

### `u57-recognition-and-items.C12_stray_file_sorted`

The report reader sorts every json file by its stem as a number again

- File: `src/cratekit/core/jobs.py`
- Source: `u57-recognition-and-items.json`, row `C12_stray_file_sorted`
- Moved: U298 deleted core/artifacts.py and folded its committed reader into core.jobs.Artifacts.committed, whose default order is by_ordinal; the filter to ordinal named files before the numeric sort is that function's, and dropping it lets a stray json file reach int() as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
    return sorted((path for path in paths if path.stem.isdigit()), key=lambda item: int(item.stem))
```

New text:

```
    return sorted(paths, key=lambda item: int(item.stem))
```

### `u342.S7_stamp_pads_the_key`

stamp_head: render the head's key unpadded, so 6A is written where the library writes 06A

- File: `src/cratekit/core/naming.py`
- Source: `u342.json`, row `S7_stamp_pads_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_title_with_no_head_is_stamped_and_keeps_every_byte[the-key-padded]`

Old text:

```
        head = _render_head(spec, template, template.key_pad)
        rendered
```

New text:

```
        head = _render_head(spec, template, "none")
        rendered
```

### `u205.G6_file_account_share_is_the_total`

gate state write: the account's entry under identities is written as the total, the app's calls in it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G6_file_account_share_is_the_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`

Old text:

```
                    "calls": max(0, self.calls - self.app_calls),
```

New text:

```
                    "calls": self.calls,
```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 707 against a baseline of 707
- Kills: 122 (killed)
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
  - ... and 107 more, see the JSON sidecar

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = True

```

### `r797-a.T7_competes_in_a_style_bucket`

competing_subs: leave former places out of a bucket split by style, so the folder holding the old playlist no longer sees it

- File: `src/cratekit/core/routing.py`
- Source: `r797-a.json`, row `T7_competes_in_a_style_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`, `tests/test_routing_parity.py`
- Collected: 1097 against a baseline of 1097
- Kills: 13 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_competes_where_it_is_declared_and_where_it_sits_and_nowhere_else`
  - `tests/test_adopt_former_place.py::test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[another-band]`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[its-reading]`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_whose_genre_names_another_style_moves_to_that_style`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[defaulted-genre]`
  - `tests/test_adopt_former_place.py::test_a_track_whose_genre_lands_in_the_old_folders_default_is_withheld`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`
  - `tests/test_adopt_placements.py::test_the_style_subs_compete_where_a_bucket_has_no_energy_dimension`

Old text:

```
        return Competing.STYLE, frozenset((found | former) - classes)
```

New text:

```
        return Competing.STYLE, frozenset(found - classes)
```

### `r722-b.T7_lenient_field_raises`

The lenient reader raises on one undecodable field instead of reading it as None, rerun after the fix round

- File: `src/cratekit/core/tags.py`
- Source: `r722-b.json`, row `T7_lenient_field_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2994 against a baseline of 2994
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_undecodable_field_fails_the_checked_read_and_reads_as_none_beside_its_neighbours`

Old text:

```
            if strict:
                raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

New text:

```
            raise TagReadFailed(f"{key}: {type(exc).__name__}: {exc}") from exc
```

### `u247.M1_memo_removed`

load_taxonomy: call the unremembered parse, so every load parses its text again, as main did

- File: `src/cratekit/core/taxonomy.py`
- Source: `u247.json`, row `M1_memo_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 10 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_read_again_with_the_same_text_is_not_parsed_again`
  - `tests/test_active_taxonomy.py::test_a_copy_rewritten_between_two_loads_is_read_and_judged_again`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_sweep_parses_the_active_taxonomy_once_however_many_files_it_tags`
  - `tests/test_taxonomy.py::test_an_edit_that_keeps_the_length_is_a_different_text_and_is_parsed_again`
  - `tests/test_taxonomy.py::test_the_memo_holds_eight_texts_and_parses_the_first_again_after_a_ninth`
  - `tests/test_taxonomy.py::test_the_same_text_is_parsed_once_and_answers_what_a_fresh_parse_builds`
  - `tests/test_taxonomy.py::test_the_three_texts_an_upgrade_reads_are_each_parsed_once`
  - `tests/test_taxonomy.py::test_two_texts_are_each_parsed_once_and_each_answers_its_own`

Old text:

```
    return _parsed(text)

```

New text:

```
    return _parsed.__wrapped__(text)

```

### `r301.B3_refusal_detail_no_key`

The monthly refusal's detail no longer names the key that raises the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B3_refusal_detail_no_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
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

### `r706-a.A6_run_message_reworded`

Reword the per part run refusal, do not append to it

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A6_run_message_reworded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
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

### `r924.A1_no_plan_line`

Identification never states its plan before the first call

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A1_no_plan_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 186 against a baseline of 186
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

### `u103-a.A1_read_serves_only_answers`

Drop the reader's rule that only a match or a miss is served from a cache document

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A1_read_serves_only_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
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

### `u57-recognition-and-items.M12_quota_reads_as_failure`

The provider's quota answer is raised under the failure slug, not the spend slug

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M12_quota_reads_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_and_neither_spend_refusal_is_a_miss`
  - `tests/intake/test_recognition.py::test_answers_that_cannot_be_kept_neither_fail_the_pass_nor_replace_its_refusal`
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

### `u57-recognition-and-items.M6_score_constant`

Every hit scores zero, so the fold can never prefer a better answer

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M6_score_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_becomes_a_wanted_row_with_the_version_split_and_the_isrc_kept`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[adjacent-fold-to-first-offset-and-best-score]`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[no-isrc-the-token-decides-and-a-version-differs]`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[played-twice-stays-twice]`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[two-emoji-titles-stay-two-rows]`
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[two-isrcs-that-differ-do-not-fold]`

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

### `r682-a.M1_no_by_reason_in_summary`

the intake summary no longer carries by_reason, so the json and the rendering both lose the breakdown

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M1_no_by_reason_in_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_render_payloads.py`
- Collected: 122 against a baseline of 122
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`

Old text:

```
        "by_reason": by_reason,

```

New text:

```
(empty)
```

### `r925.S1_no_folder_check`

intake set skips the free tracklist folder check, so a folder that is a file is found only after the spend

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S1_no_folder_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/intake/test_set_fetch.py`
- Collected: 108 against a baseline of 108
- Kills: 40 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[failed]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[several]`
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[timed-out]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[not-there]`
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[outside]`
  - `tests/intake/test_set_fetch.py::test_a_local_path_never_consults_the_fetch_seam`
  - `tests/intake/test_set_fetch.py::test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint`
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_made_is_a_fact_about_this_machine`
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`
  - `tests/intake/test_set_fetch.py::test_a_scratch_root_inside_the_library_refuses_before_anything_is_fetched`
  - `tests/intake/test_set_fetch.py::test_identification_that_raises_still_removes_the_fetched_mix`
  - `tests/intake/test_set_fetch.py::test_the_page_a_mix_came_from_is_frozen_on_the_set_job`
  - ... and 25 more, see the JSON sidecar

Old text:

```
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
```

New text:

```
        out = Path(ctx.args.out or cfg.paths.download_staging / TRACKLISTS_DIR)
```

### `u213.M13_unidentified_any`

_refuse_unidentified: refuse only when more than one row carries no id

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M13_unidentified_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_listing_that_fails_refuses_and_queues_nothing[no-id-by-position]`
  - `tests/intake/test_workers.py::test_a_row_the_reader_refuses_refuses_the_playlist_and_queues_nothing[no-identifier-by-position]`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`

Old text:

```
    if missing:
        raise _unusable(
```

New text:

```
    if len(missing) > 1:
        raise _unusable(
```

### `u70.S3_sentinel_strip`

The sentinel is compared unstripped, so a padded favorites is read as a playlist reference

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S3_sentinel_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_reserved_reference_is_read_however_it_is_cased[ FAVORITES ]`

Old text:

```
    return str(reference or "").strip().casefold() == FAVORITES
```

New text:

```
    return str(reference or "").casefold() == FAVORITES
```

### `r925.S5_unwritten_note_names_no_job_show`

The unwritten note no longer names the verb that lists the tracks

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r925.json`, row `S5_unwritten_note_names_no_job_show`
- Moved: the same unwritten tracklist note of _set_tracklist, which U307 moved from cli.py to cli_identify.py, one level less indented
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`

Old text:

```
f"{exc.strerror or exc}); the job is queued, and its tracks are listed "
            f"by: crate job show {job_id}"
```

New text:

```
f"{exc.strerror or exc}); the job is queued"
```

### `u104-d.C3_detail_renamed`

Rename the message only and leave the scratch path in the refusal's detail

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C3_detail_renamed`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_refusal_from_inside_the_identifier_names_the_address_and_not_the_scratch_file`

Old text:

```
        key: held.ref if value == str(held.path) else value
```

New text:

```
        key: value
```

### `u37-author-light.G1_stub_listing`

Treat a U22 stub listing as a spliceable Fresh Export

- File: `src/cratekit/intake/collection_xml.py`
- Source: `u37-author-light.json`, row `G1_stub_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`
- Collected: 12 against a baseline of 12
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

### `u104-a.F2_guard_samefile_layer`

Drop the filesystem half of the library guard: two spellings of one folder that resolve does not settle are no longer compared with samefile

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F2_guard_samefile_layer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_library_guard_asks_the_filesystem_and_not_only_the_strings`

Old text:

```
        if ancestor.exists() and ancestor.samefile(library):
            raise ScratchUnderLibrary(here, library)
```

New text:

```
        if ancestor.exists() and ancestor.samefile(library):
            pass
```

### `u104-c.P1_numbered_output`

Put the fixed output name back, so every entry of a playlist address lands on one file name and a set page reads as one recording

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P1_numbered_output`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound`

Old text:

```
        argv[template] = str(directory / f"{fallback.FETCH_STEM}-%(autonumber)s.%(ext)s")
```

New text:

```
        argv[template] = str(directory / f"{fallback.FETCH_STEM}.%(ext)s")
```

### `r685-a.V2_landing_preflight_reads_the_shipped_text`

The landing's preflight parses the shipped text, so an undeclared catalog tree is not seen

- File: `src/cratekit/intake/landing.py`
- Source: `r685-a.json`, row `V2_landing_preflight_reads_the_shipped_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_landing_labels.py`
- Collected: 41 against a baseline of 41
- Kills: 2 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_no_module_but_the_loader_reads_the_shipped_template`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_refuses_before_any_file_moves`

Old text:

```
    checked = Checked(registry=tree_registry.read(cfg), declared=active_taxonomy.load(cfg))

```

New text:

```
    checked = Checked(
        registry=tree_registry.read(cfg),
        declared=taxonomy.load_taxonomy(taxonomy.shipped_template_text("default")),
    )

```

### `u102-a.D1_keep_is_not_accept`

decided(): read the accepted verdict alone, so an item answered keep is treated as a rename to apply

- File: `src/cratekit/intake/repair.py`
- Source: `u102-a.json`, row `D1_keep_is_not_accept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`, `tests/intake/test_repair.py`
- Collected: 23 against a baseline of 23
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

### `u102-a.P4_unchanged`

_plan_for: stop setting aside a proposal that names the file's own name, so it is planned as a rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P4_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_that_asked_for_no_change_is_listed_with_its_reason`

Old text:

```
        if path.name == accepted.proposed:
```

New text:

```
        if False:
```

### `u102-b.G1_plan_referenced`

_plan_for: treat no candidate as referenced, leaving only the post gate check to hold the file

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G1_plan_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
        if not naming_cli.is_referenced(path, referenced)
    ]
```

New text:

```
        if True
    ]
```

### `u102-b.R1_retryable_seed`

_apply: call a run retryable when all it holds is a file only a person can release

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R1_retryable_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
        item["action"] in _HELD and item["action"] not in _NEEDS_A_PERSON
```

New text:

```
        item["action"] in _HELD
```

### `u237.M2_symbol_marks_dropped`

_YEAR: forget the sound recording and copyright symbols, so a line starting with one keeps its mark and year

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M2_symbol_marks_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 36 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117 \xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\xa9 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\xa9 ]`
  - ... and 21 more, see the JSON sidecar

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\))\s*)+", re.IGNORECASE)
```

### `u177.A6_first_of_two`

by_bandcamp: answer the first of two claimants, so a hand edited tie stages under a guessed label

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A6_first_of_two`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`, `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 190 against a baseline of 190
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_two_labels_naming_one_account_by_hand_stage_it_under_neither`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
        return found[0] if len(found) == 1 else None

```

New text:

```
        return found[0] if found else None

```

### `u52-zero-rows.L5_artist_for_missing_returns_none`

The bare skip R-135 named in miniature: a label with no catalogue object at all returns None rather than refusing

- File: `src/cratekit/label/sweep.py`
- Source: `u52-zero-rows.json`, row `L5_artist_for_missing_returns_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_missing_artist_refusal_names_the_missing_object_not_the_listing`

Old text:

```
        raise run.LookupFailure(
            f"no catalogue object was available for the registered label "
            f"{entry.name!r}, so its releases were never listed; that is not "
            f"a label with nothing new"
        )
```

New text:

```
        return None
```

### `u192.F1_no_rearm_catch`

settle: let the cancelled refusal through untouched, so an interrupted drive leaves the job closed and names job resume

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F1_no_rearm_catch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    except JobCancelled as exc:
        raise _resumable(exc, job_id, argv, origin) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _resumable(exc, job_id, argv, origin) from exc
```

### `r356-b.B6_export_plan_drops_the_reason`

An unmatched export row never carries what the account said about it

- File: `src/cratekit/modules/outbound/export.py`
- Source: `r356-b.json`, row `B6_export_plan_drops_the_reason`
- Moved: the reason export.plan gives an unmatched row moved out of the Unmatched constructor's keyword arguments into a local reason the row is built from on the next line; the same account reason is dropped for the bare word
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_an_unmatched_export_row_carries_what_the_account_said_about_it`

Old text:

```
            reason = account.unmatched_reason(track.identity) or "unmatched"

```

New text:

```
            reason = "unmatched"

```

### `r229.L13_a_mismatch_is_never_said`

A record under the crate's own path written from other music is reported as an ordinary update

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L13_a_mismatch_is_never_said`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`
  - `tests/test_outbound_workers.py::test_a_path_reused_for_a_different_crate_is_said_at_the_gate`

Old text:

```
        mismatched = bool(written) and not _still_carries(written, wanted)
```

New text:

```
        mismatched = False
```

### `r229.L4_an_eighth_of_the_crate`

The crate side bound loosens from a quarter to an eighth, so a crate one past quadrupled is recognised

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L4_an_eighth_of_the_crate`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_crate_the_record_is_a_sliver_of_is_not_that_crate[one-past-quadrupled]`

Old text:

```
GROWN_DENOMINATOR = 4
```

New text:

```
GROWN_DENOMINATOR = 8
```

### `u309-z.U2_settle_extend_dedupes`

The shared extend adds a value the record already holds a second time

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u309-z.json`, row `U2_settle_extend_dedupes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_track_settled_twice_on_a_set_playlist_is_recorded_once`

Old text:

```
        held += [str(one) for one in more if str(one) not in held]
```

New text:

```
        held += [str(one) for one in more]
```

### `u27-reports-round-1.C4_placement_count`

Keep only the first placement per track, so a track filed twice reports one

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C4_placement_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_covered_track_names_every_path_under_the_tree_that_holds_it`

Old text:

```
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
            held.setdefault(track_id, [playlist.path])
```

### `u27-reports-round-1.L5_unused_buckets`

Report no unused buckets at all

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L5_unused_buckets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_declared_bucket_with_no_folder_is_a_gap`

Old text:

```
            unused_buckets=tuple(sorted(declared_ids - present_ids)),
```

New text:

```
            unused_buckets=(),
```

### `r154-a.A4_legacy_spelling`

Accept only this product's stamp as a snapshot name, so every snapshot the source system wrote is refused by name and hidden from the listing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A4_legacy_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_the_source_system_wrote_is_still_a_name_and_still_pulled`

Old text:

```
    if is_stamp(value):
        return True
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
```

New text:

```
    if is_stamp(value):
        return True
    return False
    if not _LEGACY_SHAPE.fullmatch(value):
        return False
```

### `r1761.P25_max_delete_sentence_on_any_failure`

run_backup: the remote holds files sentence is said for any failure of a move nothing mirror, round one's B2

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P25_max_delete_sentence_on_any_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                and MOVE_NOTHING[0].lstrip("-") in failed.stderr
```

New text:

```
                and True
```

### `r222-a.A2_boundary_not_strict`

Hold a folder named exactly at the floor, so the last completed run's own folder is never settled and survives every later run

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A2_boundary_not_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`

Old text:

```
(floor is None or name > floor)]
```

New text:

```
(floor is None or name >= floor)]
```

### `r338-a.B7_rehearsal_transfers_the_share`

TRANSFERRING_LABELS: leave the share's capture out, so a dry run really syncs gigabytes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-a.json`, row `B7_rehearsal_transfers_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r757-a.E2_fast_mode_lists_folder_by_folder`

_plan_files: the ordinary run drops the recursive listing option, which is the whole of the speed fix

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E2_fast_mode_lists_folder_by_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                *(() if full else (FAST_LIST,)),
```

New text:

```
                *(() if True else (FAST_LIST,)),
```

### `r757-b1.E12_plain_line_dropped`

_said: drop a line that is not a logged object, the review's fix

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-b1.json`, row `E12_plain_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if not isinstance(entry, dict):
            lines.append(line)
```

New text:

```
        if not isinstance(entry, dict):
            pass
```

### `u317.Q15_archive_not_rechecked`

run_backup: the quick archive runs without asking still_removed first

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q15_archive_not_rechecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                if stale:
                    failed = CommandResult(
```

New text:

```
                if False:
                    failed = CommandResult(
```

### `u323.I1_unread_identity_refuses`

_not_the_recorded_volume: an identity the platform cannot read (observed None) refuses as foreign instead of being left to the census

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I1_unread_identity_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if recorded is None or observed is None:
            return ""
```

New text:

```
        if recorded is None:
            return ""
```

### `u48-author.E1_listing_return_code_inverted`

Existing guard: purge on a failed listing and report a good one as failed

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `E1_listing_return_code_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 17 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_folder_the_last_completed_run_wrote_is_settled_not_held`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing`
  - `tests/modules/test_tools.py::test_the_retention_the_plan_declared_is_the_retention_the_run_applies`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
```

New text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode == 0:
```

### `r1761.P5_empty_root_passes`

_unproven: a root holding nothing at all is not refused, so with no history it runs as a new library

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P5_empty_root_passes`
- Moved: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not anything:
        held_before = ""
```

New text:

```
    if False:
        held_before = ""
```

### `r1761.P7_floor_coefficient_halved`

LIBRARY_FLOOR: a twentieth rather than a tenth, so one file where twelve were passes

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `r1761.json`, row `P7_floor_coefficient_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
LIBRARY_FLOOR = 10
```

New text:

```
LIBRARY_FLOOR = 20
```

### `u317.Q12_root_volume_not_rechecked`

still_removed: a quick run's archive runs over a root that went away or changed volume (round one's B2)

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q12_root_volume_not_rechecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if os.stat(root).st_dev != root_dev:
            return f"the library root {root} is on another volume than the one walked"
    except OSError as exc:
        return f"the library root {root} could not be read before the archive: {exc}"
```

New text:

```
        pass
    except OSError:
        pass
```

### `u317.Q8_settled_trusts_the_first_walk`

settled: every entry of the walk before the transfer is trusted, so a file changed mid run is never sent again

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q8_settled_trusts_the_first_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        out[rel] = was if now is not None and was.agrees(now) else DOUBT
```

New text:

```
        out[rel] = was
```

### `r154-b.B5_veto_not_select`

Read only the newest folder, which is the first cut: a shared root refuses whenever the other library backed up last

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B5_veto_not_select`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`

Old text:

```
    newest = names[::-1][:NEWEST_WALK]
```

New text:

```
    newest = names[::-1][:1]
```

### `r338-a.B8_contained_share_copied_twice`

_outside_share: read every layout as the outside one, so a share the mirror already carries is synced a second time

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B8_contained_share_copied_twice`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r338-c.C1_absent_share_never_said`

absent_analysis_share: never warn, so an outside share that is not a directory reads as a share that was carried

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C1_absent_share_never_said`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r367.G5_absent_sidecars_are_not_recorded`

the plan copies nothing extra and also does not name what it skipped

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G5_absent_sidecars_are_not_recorded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
            absent.append(sidecar.suffix)

```

New text:

```
(empty)
```

### `r388-a.M6_root_listing_message_reworded`

Reword could not be listed to could not be read in the root listing refusal

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M6_root_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `u311.C2_any_block_is_the_report`

The loudness reader takes any JSON object, not one carrying its marker

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C2_any_block_is_the_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_loudness_report_is_parsed_as_json_not_grepped`

Old text:

```
        if isinstance(data, dict) and marker in data:
```

New text:

```
        if isinstance(data, dict):
```

### `r187-b.B10_bad_track_is_current`

_entry_is_current: a cached track that cannot be rebuilt still counts as current, so it is served as a keyless file

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B10_bad_track_is_current`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-missing-fields]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-not-a-mapping]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[bpm-124]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[title-None]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[vox-value2]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[voxgender-4]`

Old text:

```
        and (entry.get("track") is None or _track_from_cache(entry.get("track")) is not None)

```

New text:

```
(empty)
```

### `u311.C6_relative_key_dropped`

The relative key (same number, other letter) leaves the perfect tier

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C6_relative_key_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 340 against a baseline of 340
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_camelot_tiers_are_the_ported_ones[8B-perfect]`
  - `tests/test_setbuilder_cli.py::test_a_count_caps_the_companions`
  - `tests/test_setbuilder_cli.py::test_an_unowned_sequence_places_each_companion_once`

Old text:

```
    perfect = ((0, letter), (1, letter), (-1, letter), (0, other))
```

New text:

```
    perfect = ((0, letter), (1, letter), (-1, letter))
```

### `r704-a.R5_flag_not_stored`

LookupFailure drops the flag it was handed

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R5_flag_not_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
        self.rate_limited = rate_limited
```

New text:

```
        self.rate_limited = False
```

### `u281.S5_title_not_named_cloudflare`

unread_outcome: never name a Cloudflare title page a Cloudflare challenge

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `S5_title_not_named_cloudflare`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_just_a_moment_page_is_blocked_not_a_parse_break`

Old text:

```
        named = f", a {CLOUDFLARE_CHALLENGE}" if _CLOUDFLARE_TITLE.match(title) else ""
```

New text:

```
        named = ""
```

### `u260.F11_reset_images_forgets_nothing`

reset_images: drop nothing, so a shared fetch built in one test outlives it

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F11_reset_images_forgets_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 9 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_binder_hands_back_one_fetch_per_process_and_the_reset_drops_it`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    """Forget the shared image fetch and every picture it remembered."""
    _images.clear()
```

New text:

```
    """Forget the shared image fetch and every picture it remembered."""
```

### `u260.F8_fetch_hit_not_refreshed`

remembering: a hit no longer refreshes its entry, so the memory is first in first out

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F8_fetch_hit_not_refreshed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`

Old text:

```
            if data is not None:
                held.move_to_end(url)
                return data
```

New text:

```
            if data is not None:
                return data
```

### `u282.P1_no_picture_question`

_pictured: no picture question is carried, so a file Discogs tagged gets no cover (merge blocker 5)

- File: `src/cratekit/tagging/searchers.py`
- Source: `u282.json`, row `P1_no_picture_question`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 8 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_file_discogs_tagged_with_no_picture_gets_beatport_s_cover`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_misses_names_no_picture_and_no_unread`
  - `tests/test_discogs_first.py::test_a_picture_ask_beatport_refuses_is_unread_and_counts_toward_the_stop`
  - `tests/test_discogs_first.py::test_a_refused_picture_ask_keeps_the_genre_and_says_beatport_went_unread`
  - `tests/test_discogs_first.py::test_a_tagged_file_with_no_picture_keeps_its_genre_and_gets_the_cover`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`

Old text:

```
    if not later:
        return lent
```

New text:

```
    if True:
        return lent
```

### `u133-b.T10_family`

Jazz reads as the downtempo family to the set builder

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T10_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`
- Collected: 894 against a baseline of 894
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_jazz_is_shaped_as_hip_hop_is`
  - `tests/test_routing_parity.py::test_the_family_projection_matches_the_old_rules_applied_to_the_folder[Jazz]`
  - `tests/test_routing_parity.py::test_the_family_projection_matches_the_old_rules_applied_to_the_folder[jazz]`

Old text:

```
display = "Jazz"
family = "other"

```

New text:

```
display = "Jazz"
family = "downtempo"

```

### `u132.G1_undeclared_cause`

The additive half's skip over an undeclared class carries no cause

- File: `src/cratekit/write/genre_favorites.py`
- Source: `u132.json`, row `G1_undeclared_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_routing_workers.py`
- Collected: 288 against a baseline of 288
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_genre_favorites_adoption.py::test_an_adoption_over_a_taxonomy_without_the_class_names_the_skipped_step`

Old text:

```
            cause=CLASS_UNDECLARED,

```

New text:

```
            cause="",

```

### `r675.G5_leaf_compared_as_whole_path`

_referenced: the dark row is looked up by its whole decoded path rather than its leaf, so no row under another volume ever matches

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G5_leaf_compared_as_whole_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 15 (killed)
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
  - `tests/test_naming_apply_cli.py::test_the_refusal_counts_every_row_and_lists_no_more_than_twenty`
  - `tests/test_naming_apply_cli.py::test_the_refusal_names_the_decoded_location_a_rule_is_matched_against`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(_key(decoded)))
```

### `r758-a.T4_target_can_be_removed_from`

a move that names its own target among its removals takes the track out of the target

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T4_target_can_be_removed_from`
- Moved: the leavers are now gathered in the step _proven_leavers, one level less indented, the same test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removal_from_a_playlist_that_is_not_there_creates_none`

Old text:

```
            if destination != move.target:
                leaving.setdefault(destination, []).append(move.content_id)
```

New text:

```
            leaving.setdefault(destination, []).append(move.content_id)
```

### `r685-b.G2_the_guard_forgets_attributes`

The guard stops matching module attribute calls, the spelling every verb used

- File: `tests/test_active_taxonomy.py`
- Source: `r685-b.json`, row `G2_the_guard_forgets_attributes`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_the_guard_sees_every_spelling_it_should_refuse`

Old text:

```
        if isinstance(func, ast.Attribute) and func.attr in READERS:

```

New text:

```
        if isinstance(func, ast.Attribute) and func.attr in ():

```

