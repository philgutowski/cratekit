# Mutation table: u332-replay-before-7

Measured by `scripts/mutate.py` on 2026-11-24 04:13 UTC, branch `HEAD` at `324cafa5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 317.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:13 UTC for commit `324cafa562b9`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 122, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B5_a_scenario_with_no_record_closed_over` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 4 | killed |
| `u122.H4_hold_flattened` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 5 | killed |
| `u148.C2_count_off` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 2 | killed |
| `u148.S2_claims_in_progress` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 1 | killed |
| `u151.M1_membership_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X2_no_org_fallback` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u196.S3_empty_search` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 1 | killed |
| `u203.M7_rule_line_is_a_heading` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u313.B3_stale_window_doubled` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 10 | killed |
| `r1313.A2_status_before_no_file_landed` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 370 | 2 | killed |
| `r83.D7_detail_names_class` | `src/cratekit/acquire/adapter.py` | maintainer | 6 file(s) | 753 | 9 | killed |
| `u176.C2_summary_names_a_fan` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 1 | killed |
| `u176.V11_marked_by_file` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V6_music_folder_present` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u177.B4_labels_of_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u205.C10_country_not_sent` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C7_transport_text_in_message` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `r289-b.C1_download_call_site` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 1 | killed |
| `r668-a.M5_missing_list_guard_after_load` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `u42-author.P1_unresolved_from_the_page` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u54-acquisition-worker.G14_marker_applied` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G29_auth_failure_parks` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u80.F11_tie_ignores_platform` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F5_api_url_kept` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u81-fetch-b.Y3_failed_exit_is_a_file` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W12_download_failure_not_retryable` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Q1_provider_route_fetched_lossy` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r1016.M3_folder_parse_through_the_factory` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 3 | killed |
| `r878-a.A10_non_page_refused` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 4 | killed |
| `r878-a.A7_empty_page_ends` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-b.B8_first_request_no_cursor` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `u65.B3_playlist_tracks_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 6 | killed |
| `u65.C7_a_zero_total_is_trusted_as_an_end` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 1 | killed |
| `u65.F4_the_favourites_dedup_goes` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 1 | killed |
| `r1709.M9_title_identity_is_the_fold` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 30 | killed |
| `u205.O4_app_attached_as_account` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 353 | 6 | killed |
| `r703-a.V2_no_forget` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 2 | killed |
| `r703-b.O4_wraps_twice` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 275 | 1 | killed |
| `u47-author.CODEC_alac_reads_as_lossy` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R195_push_empty_instead` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 4 | killed |
| `u47-author.R197_drop_event_run` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 3 | killed |
| `u23-round-8-independent.X9_outstanding_returns_everything` | `src/cratekit/adopt/apply.py` | user | 1 file(s) | 615 | 2 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 86 | killed |
| `u254.M16_journal_needs_format` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `r1991.A3_undeclared_raises` | `src/cratekit/adopt/apply_cli.py` | user | 15 file(s) | 521 | 1 | killed |
| `u132.W1_every_apply` | `src/cratekit/adopt/apply_cli.py` | user | 10 file(s) | 447 | 1 | killed |
| `u27-adopt-apply-author.S2_analysis_watch_watches_nothing` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 165 | 2 | killed |
| `u55-round-2.R23_worker_raises_on_failure` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 1 | killed |
| `u23-round-8-independent.X5_grant_accepts_a_blank_actor` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `r780-a.A2_tree_path_adds_a_sub` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 8 | killed |
| `r797-d.M6_again_settled_in_one_bucket` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 172 | 6 | killed |
| `u118-c.M8_asked_split` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 189 | 2 | killed |
| `r780-b.B3_renamed_target_reads_as_done` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r788-c.L1_any_vox_value_is_the_tag` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 163 | 2 | killed |
| `u118-b.P1_named_place_split` | `src/cratekit/adopt/placements.py` | user | 3 file(s) | 143 | 25 | killed |
| `r722.P4_entry_drops_energy` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 3 | killed |
| `r731-a.M06_competing_place_never_withholds` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 13 | killed |
| `r788-a.P3_uncalibrated_files` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 4 | killed |
| `r788-b.P19_answered_genre_files_nothing` | `src/cratekit/adopt/plan.py` | maintainer | 4 file(s) | 163 | 1 | killed |
| `u956.S21_excluded_applicable` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 687 | 10 | killed |
| `u23-round-8-independent.B3_settled_bytes_clause_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.F1_byte_search_drops_the_vacancy_filter` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut` | `src/cratekit/adopt/revert_changed.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.X7_classify_accepts_the_fallback_tier` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `u956.O2_confine_flag_ignored` | `src/cratekit/adopt/scan.py` | user | 3 file(s) | 703 | 1 | killed |
| `u247.M8_scan_freezes_its_declaration` | `src/cratekit/adopt/scan_cli.py` | user | 2 file(s) | 47 | 1 | killed |
| `u241.M24_identity_after_the_read` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 3 | killed |
| `u223.M3_no_clear` | `src/cratekit/analysis/artifacts.py` | user | 2 file(s) | 279 | 3 | killed |
| `u306.A6_item_record_unreadable` | `src/cratekit/analysis/artifacts.py` | user | 3 file(s) | 318 | 1 | killed |
| `u90-b.B2_method_not_hand` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 3 | killed |
| `u90-c.C3_hand_branch_wrong_method` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 4 | killed |
| `u94-a.S8_after_walk_never_asked` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N1_stride_is_the_first_n` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u157.A2_cut_unbound` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 283 | 3 | killed |
| `u223.M20_twin_target_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 2 | killed |
| `u306.A3_walk_recursive` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 213 | 18 | killed |
| `u343.M07_waiting_takes_measured_files` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 449 | 3 | killed |
| `u90-a.A7_exclusive_group_gone` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 1 | killed |
| `u263.D23_cover_lines` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 4 | killed |
| `u264.M11_ffmpeg_left_channel` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u264.M5_halving` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 7 | killed |
| `u157.D2_band_wide` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u343.M21_stages_keep_the_key_stage` | `src/cratekit/analysis/detect.py` | maintainer | 2 file(s) | 204 | 2 | killed |
| `u58-workers-and-wav.S4_undo_overwritten` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 177 | 1 | killed |
| `u327.A19_row_follows_file` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 3 | killed |
| `u342.E2_policy_before_files` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 1 | killed |
| `u342.P5_stamped_writes` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 8 | killed |
| `u342.C3_written_counts_stamps` | `src/cratekit/analysis/head_adopt_cli.py` | user | 4 file(s) | 392 | 1 | killed |
| `u275.M5_decode_line_dropped` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 555 | 29 | killed |
| `sitting3.G10_lone_clip_not_padded` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 3 | killed |
| `sitting3.G5_loader_skips_readiness` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 1 | killed |
| `u58-workers-and-wav.W2_decoder_seam_ignored` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 177 | 7 | killed |
| `u92-author.G3_cap_coefficient` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 1 | killed |
| `r1761.P24_flag_lost_in_the_worker` | `src/cratekit/backup/cli.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r221-b.M2_refusal_step_unconditional` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `r222-b.B2_any_verb_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r290-author.R2_backup_rebuild_drops_the_type` | `src/cratekit/backup/cli.py` | user | 2 file(s) | 215 | 2 | killed |
| `r390-a.A6_backup_transfer_exit_is_permanent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `u45-round-1.A1_unreadable_reported_as_absent` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 5 | killed |
| `u45-round-1.Q1_resume_drops_the_rehearsal` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.W4_ages_derived_from_the_outcome` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `u50-author.W1_no_narrowing` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r678-b.B1_emit_hands_in_no_drive` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 293 | 3 | killed |
| `r388-d.M16_named_stamp_step_dropped_remeasured` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 660 | 2 | killed |
| `u328.S1_a_part_left_out_of_the_table` | `src/cratekit/cli/registry.py` | user | 92 file(s) | 8498 | collection error | collect-error |
| `r682-a.M7_reason_line_not_printed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 6 | killed |
| `r685-a.L7_a_parse_failure_names_a_defect` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 18 | 1 | killed |
| `u260.E2_key_drops_size` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u301.A1_decoded_rgb_skips_the_orientation` | `src/cratekit/core/art.py` | user | 3 file(s) | 167 | 1 | killed |
| `u83-a.E7_flatten_transparency` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 3 | killed |
| `u83-b.W1_undecodable_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 5 | killed |
| `u83-b.W9_id3_delall` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 3 | killed |
| `u45-round-1.E8_naive_timestamp_stored` | `src/cratekit/core/backup_facts.py` | user | 5 file(s) | 1072 | 1 | killed |
| `u331.S02_yt_dlp_said_dropped` | `src/cratekit/core/binaries.py` | user | 3 file(s) | 113 | 2 | killed |
| `r301.F1_section_not_built` | `src/cratekit/core/config.py` | user | 2 file(s) | 320 | 5 | killed |
| `r290-author.J1_blocked_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 49 | killed |
| `r390-a.A5_refusal_drops_the_inner_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 210 | 4 | killed |
| `r669-b.B1_composer_not_sanitized` | `src/cratekit/core/naming.py` | user | 2 file(s) | 134 | 2 | killed |
| `u205.G1_app_call_not_counted` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 184 | 5 | killed |
| `u301.G6_totals_drop_the_app` | `src/cratekit/core/provider_gate.py` | user | 3 file(s) | 246 | 5 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2744 | 176 | killed |
| `r118-a.A2_enoent_refuses_too` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1592 | 169 | killed |
| `r722.T9_lenient_open_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 306 | killed |
| `u310.G2_gate_digest_is_the_plan` | `src/cratekit/deletion/cli.py` | user | 4 file(s) | 393 | 1 | killed |
| `r706-a.A2_ceiling_one_part_wider` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 4 | killed |
| `r706-b.B3_partition_drops_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 4 | killed |
| `r924.A5_cadence_halved` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `u103-a.A6_digest_in_the_key` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 5 | killed |
| `u57-recognition-and-items.M2_quota_family_empty` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 6 | killed |
| `u331.S08_check_verb_origin_renamed` | `src/cratekit/intake/check_cli.py` | user | 1 file(s) | 71 | 1 | killed |
| `r682-a.M5_reason_counted_twice` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 4 | killed |
| `u120.L1_date_frozen_when_none` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u57-recognition-and-items.C3_missing_ref_not_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 2 | killed |
| `r706-c.C1_parts_note_never_said` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u103-b.C6_served_note` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u104-e.E4_identify_library_before_fetch` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 2 | killed |
| `r924.F3_watcher_silent` | `src/cratekit/intake/fetch.py` | user | 2 file(s) | 52 | 2 | killed |
| `u104-b.F6_clear_before_attempt` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P5_stem_bound` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `r301.R1_seam_falls_back_to_defaults` | `src/cratekit/intake/recognize.py` | user | 3 file(s) | 183 | 1 | killed |
| `r675.G9_repair_plan_asks_with_no_candidates` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `u102-a.U2_bare_filename` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-b.G6_abort` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u62.C1_bound_constant_true` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 503 | 1 | killed |
| `u237.M9_year_eats_the_next_digit` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 1 | killed |
| `r704-a.S3_no_context_status_check` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `u237.M10_empty_sides_match` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 2 | killed |
| `u192.F6_queue_only_never` | `src/cratekit/modules/foreground.py` | user | 4 file(s) | 414 | 21 | killed |
| `r837-a.A8_load_carries_sets` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 419 | 23 | killed |
| `r229.L19_a_copy_not_a_move` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 6 | killed |
| `r229.L8_a_living_legacy_record_is_freed` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `u205.S2_account_rejection_read_as_wait` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 179 | 2 | killed |
| `u27-reports-round-2.S5b_engine_default_drift` | `src/cratekit/modules/reports/duplicates.py` | user | 2 file(s) | 382 | 3 | killed |
| `u27-reports-round-3-fixes.F2_depth_origin` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `r1761.P11_move_nothing_dropped` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r221-a.E1_outcome_forgets_the_run` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 5 | killed |
| `r222-a.A6_any_destination_is_a_floor` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 1 | killed |
| `r349-c.C4_argv_rendered` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 4 | killed |
| `r757-a.E8_failed_mirror_reports_nothing` | `src/cratekit/modules/tools/backup.py` | maintainer | 4 file(s) | 23216 | 0 (promoted) | zero |
| `u311.A3_database_destination_not_required` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u317.Q21_send_without_archive` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u45-round-1.E1_rehearsal_publishes` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 7 | killed |
| `u48-author.P6_purge_count_not_named` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 1 | killed |
| `r1761.P18_census_any_root` | `src/cratekit/modules/tools/backup_record.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `u311.A7_unanchored_exclude_anchors` | `src/cratekit/modules/tools/backup_record.py` | user | 4 file(s) | 318 | 1 | killed |
| `u317.Q4_racy_file_not_hashed` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r154-b.B1_named_mismatch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 8 | killed |
| `r338-a.B3_capture_is_a_copy` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 2 | killed |
| `r338-b.R6_switch_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r367.G12_listing_results_are_discarded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 2 | killed |
| `r388-a.M2_identity_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r388-b.M8_share_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `u44-author-round-2.B3_concat_output_unread` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 246 | 1 | killed |
| `r187-b.B5_empty_walk_writes` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `u43-author-light.E1_anchor_is_its_own_companion` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 8 | killed |
| `u281.R4_stopped_note_unmarked` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 3 | killed |
| `u956.O6_tag_set_promises_outside` | `src/cratekit/tagging/genre_set_cli.py` | user | 3 file(s) | 104 | 3 | killed |
| `u260.F4_binder_admits_everything` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 1 | killed |
| `u281.S4_any_mitigation_is_a_challenge` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 204 | 1 | killed |
| `u260.E1_engine_encodes_per_file` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 196 | 8 | killed |
| `u133-b.T5_former_display` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 1038 | 2 | killed |
| `r675.G1_every_dark_row_refuses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 6 | killed |
| `r1991.T6_filed_untracked` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 5 | killed |
| `u302.W16_move_removes_without_proof_of_the_target` | `src/cratekit/write/trees.py` | user | 2 file(s) | 147 | 1 | killed |

## Zero rows and what they owe

- `u264.M11_ffmpeg_left_channel` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u157.D2_band_wide` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P24_flag_lost_in_the_worker` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u50-author.W1_no_narrowing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P11_move_nothing_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-a.E8_failed_mirror_reports_nothing` (maintainer facing): maintainer facing, composite not required
- `u317.Q21_send_without_archive` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P18_census_any_root` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q4_racy_file_not_hashed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u297.B5_a_scenario_with_no_record_closed_over`

run_capture: close the capture though a scenario the run collected, or a whole scenario file, left no record

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B5_a_scenario_with_no_record_closed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_run_that_did_not_list_what_it_collected_is_not_a_capture[None]`
  - `tests/test_behaviour_compare.py::test_a_run_that_did_not_list_what_it_collected_is_not_a_capture[expected1]`
  - `tests/test_behaviour_compare.py::test_a_scenario_file_that_collected_nothing_keeps_the_capture_open`
  - `tests/test_behaviour_compare.py::test_a_scenario_that_ran_and_left_no_record_keeps_the_capture_open`

Old text:

```
    if done.returncode != 0 or not recorded or missing:
```

New text:

```
    if done.returncode != 0 or not recorded:
```

### `u122.H4_hold_flattened`

A held card derives In Progress whatever it held, so In review becomes drift

- File: `scripts/board.py`
- Source: `u122.json`, row `H4_hold_flattened`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 5 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`

Old text:

```
        return current

```

New text:

```
        return "In Progress"

```

### `u148.C2_count_off`

short_of_count never compares rows to the count

- File: `scripts/board.py`
- Source: `u148.json`, row `C2_count_off`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options0-project_items-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`

Old text:

```
    if len(rows) < total:
```

New text:

```
    if False:
```

### `u148.S2_claims_in_progress`

start says a card not on the board is In Progress

- File: `scripts/board.py`
- Source: `u148.json`, row `S2_claims_in_progress`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_start_reads_the_board_before_it_branches`

Old text:

```
        print(f"Branch {branch} is checked out, but #{node['number']} is NOT on the")
```

New text:

```
        print(f"Branch {branch} is checked out and #{node['number']} is In Progress.")
```

### `u151.M1_membership_count_dropped`

an issue whose memberships come back short is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `M1_membership_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_card_read_that_is_short_or_never_ends_is_refused[5-<lambda>-#1 project membership read returned 1 of the 21]`

Old text:

```
            short_of_count(
                memberships["nodes"], memberships.get("totalCount"),
                f"#{issue['number']} project membership",
            )

```

New text:

```
(empty)
```

### `u151.X2_no_org_fallback`

the context never asks for an organization project

- File: `scripts/board.py`
- Source: `u151.json`, row `X2_no_org_fallback`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_context_is_one_query_for_the_project_its_status_and_unblocks`

Old text:

```
    for kind in ("user", "organization"):
```

New text:

```
    for kind in ("user",):
```

### `u196.S3_empty_search`

cmd_residuals: drop the refusal of an empty search, which matches every heading

- File: `scripts/board.py`
- Source: `u196.json`, row `S3_empty_search`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`

Old text:

```
        if args.land or not words:
```

New text:

```
        if args.land:
```

### `u203.M7_rule_line_is_a_heading`

comment_heading: read a line of emphasis markers alone as the heading, so a rule above Started reads as empty

- File: `scripts/board.py`
- Source: `u203.json`, row `M7_rule_line_is_a_heading`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[\n***\n\nStarted\n-started]`

Old text:

```
        if not text.strip("*_").strip():
            continue
```

New text:

```
        if not text:
            continue
```

### `u313.B3_stale_window_doubled`

cloud_state: read a hold as dead only after twice the stale window, so a dead session's card is not offered to resume

- File: `scripts/board.py`
- Source: `u313.json`, row `B3_stale_window_doubled`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 10 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-## Started@s+1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorm notes**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorm**s@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorms**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorms.**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Pre brainstorm.**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-Brainstorm notes.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-Not **Withdrawn**, held@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-Question.@s+2]`
  - `tests/test_board_cloud.py::test_cloud_offers_answered_before_resumable_before_fresh`

Old text:

```
    if age is not None and age > STALE_HOURS:
```

New text:

```
    if age is not None and age > STALE_HOURS * 2:
```

### `r1313.A2_status_before_no_file_landed`

classify_unavailable: ask the nearest status before NoFileLanded, so a download whose swallowed cause was a 404 page quarantines a live track

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A2_status_before_no_file_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 370 against a baseline of 370
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_transient_marker_wins_over_a_status_code`
  - `tests/test_provider_not_found_bodies.py::test_no_file_landed_carrying_a_404_page_stays_transient`

Old text:

```
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
```

New text:

```
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if isinstance(exc, NoFileLanded):
        return TrackOutcome.UNAVAILABLE_TRANSIENT
    text = str(exc).lower()
```

### `r83.D7_detail_names_class`

R-348: the detail no longer names the exception class

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D7_detail_names_class`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 753 against a baseline of 753
- Kills: 9 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`

Old text:

```
            f"({type(exc).__name__}: {exc})",
```

New text:

```
            f"({exc})",
```

### `u176.C2_summary_names_a_fan`

read_collection: a summary naming no fan is read as signed in, so a logged out cookie lists pages under an empty fan

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C2_summary_names_a_fan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_summary_naming_no_fan_is_rejected_even_when_the_pages_would_answer`

Old text:

```
    if not fan_id:
        raise SessionRejected
```

New text:

```
    if False:
        raise SessionRejected
```

### `u176.V11_marked_by_file`

handle_fetch: a file is marked by the offer alone, so lossy bytes under a lossless offer stage unmarked

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V11_marked_by_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_lossy_file_under_a_lossless_offer_is_marked_by_what_it_is`

Old text:

```
        marked = lossy or acquire_cli.lossy_landing(path, policy=policy)
```

New text:

```
        marked = lossy
```

### `u176.V6_music_folder_present`

Library: an absent music folder is read as an empty library, so every purchase plans new

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V6_music_folder_present`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_library_unmounted_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_an_absent_music_folder_refuses_rather_than_planning_everything_new`

Old text:

```
        if not music.is_dir():
```

New text:

```
        if False:
```

### `u177.B4_labels_of_filter`

labels_of: name a label whose purchases are all filtered, so the check says it stages

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B4_labels_of_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_label_whose_purchases_are_all_filtered_is_not_said_to_stage`

Old text:

```
        if one.disposition in TO_FETCH and one.label is not None
    }

```

New text:

```
        if one.label is not None
    }

```

### `u205.C10_country_not_sent`

app client: reads are asked in no country, so availability answers are not the account's

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C10_country_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_the_lookup_asks_the_isrc_in_the_accounts_own_country_with_the_names_included`

Old text:

```
            params={**params, "countryCode": self.country_code},
```

New text:

```
            params={**params},
```

### `u205.C7_transport_text_in_message`

app client: a transport failure's text, which quotes the URL and the ISRC, is put in the message, so an ISRC holding 404 reads as no track

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C7_transport_text_in_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_transport_failure_whose_text_holds_404_is_not_read_as_no_track`

Old text:

```
                f"the catalogue API could not be reached ({type(exc).__name__})"
```

New text:

```
                f"the catalogue API could not be reached ({exc})"
```

### `r289-b.C1_download_call_site`

Drop the sweep at the head of acquire download

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `C1_download_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`

Old text:

```
        sweep_staging(Path(cfg.paths.download_staging), store)

```

New text:

```
(empty)
```

### `r668-a.M5_missing_list_guard_after_load`

the missing list refusal runs after the configuration is read, so a command naming nothing has side effects first

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M5_missing_list_guard_after_load`
- Moved: Same order in acquire_download; U298 replaced the private _load with cli.output.load_config, so the configuration read the guard is moved after is reworded
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`

Old text:

```
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )
    cfg = load_config(("acquire.cli",))

```

New text:

```
    cfg = load_config(("acquire.cli",))
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )

```

### `u169.A3_worker_never_declines`

handle: re-raise a policy refusal instead of declining it, the base's behaviour

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A3_worker_never_declines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 9 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_label_sync_go.py::test_a_go_job_whose_track_was_refused_for_good_is_not_resumed`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
            raise jobs.Declined(exc.cause) from exc
```

New text:

```
            raise
```

### `u42-author.P1_unresolved_from_the_page`

Report zero outstanding regardless of what the walk found

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P1_unresolved_from_the_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

Old text:

```
            "unresolved": len(found),
```

New text:

```
            "unresolved": 0,
```

### `u54-acquisition-worker.G14_marker_applied`

Commit a lossy landing under its unmarked name whatever the policy required

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G14_marker_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    if not required:
        return landed.name

```

New text:

```
    return landed.name

```

### `u54-acquisition-worker.G29_auth_failure_parks`

Fail the item on a dead credential instead of parking, so the driver re-authenticates once per remaining track

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G29_auth_failure_parks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
        if invocation.outcome is InvocationOutcome.AUTH_FAILED:
```

New text:

```
        if False:
```

### `u80.F11_tie_ignores_platform`

Two equal scores are ordered by position alone, not SoundCloud first

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F11_tie_ignores_platform`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls`

Old text:

```
        key=lambda entry: entry[:3],
    )
    seen: set[str] = set()
    kept: list[Candidate] = []
```

New text:

```
        key=lambda entry: (entry[0], entry[2]),
    )
    seen: set[str] = set()
    kept: list[Candidate] = []
```

### `u80.F5_api_url_kept`

An unresolvable api.soundcloud.com URL is offered instead of the page URL

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F5_api_url_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_printed_lines_are_read_as_hits_and_bad_lines_are_counted`

Old text:

```
    if "api.soundcloud.com" in str(url):
        url = said.get("webpage_url") or ""
```

New text:

```
    if "api.soundcloud.com" in str(url) and False:
        url = said.get("webpage_url") or ""
```

### `u81-fetch-b.Y3_failed_exit_is_a_file`

A download exiting nonzero is read as a landing whenever it left a file

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `Y3_failed_exit_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_never_reads_a_failure_as_a_file[nonzero]`

Old text:

```
        if done.returncode != 0:
            said = (done.stderr or "").strip().splitlines()
            raise FallbackUnavailable(
                f"the download failed
```

New text:

```
        if False:
            said = (done.stderr or "").strip().splitlines()
            raise FallbackUnavailable(
                f"the download failed
```

### `u81-fetch-a.W12_download_failure_not_retryable`

A failed download is refused as final rather than retryable

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W12_download_failure_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_failed_download_is_transient_and_stays_retryable`

Old text:

```
            f"queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
```

New text:

```
            f"queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=False,
```

### `u81-fetch-b.Q1_provider_route_fetched_lossy`

A row with a provider route is queued for a lossy second source download anyway

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `Q1_provider_route_fetched_lossy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_with_a_provider_route_is_not_fetched_lossy`

Old text:

```
        if provider_routed(items, one):
            continue
        said = fallback.settled(items, one)
```

New text:

```
        said = fallback.settled(items, one)
```

### `r1016.M3_folder_parse_through_the_factory`

The folder walk parses with parse_factory again, so every owned playlist in a folder is fetched again

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M3_folder_parse_through_the_factory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_folder_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_playlists.py::test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup`

Old text:

```
    parse_playlist = _client_part(folder, "playlist", "parse", walk=FOLDER_WALK)
```

New text:

```
    parse_playlist = _client_part(folder, "playlist", "parse_factory", walk=FOLDER_WALK)
```

### `r878-a.A10_non_page_refused`

paginate_cursor: drop the refusal of a response with neither items nor a count, so it reads as an empty listing

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A10_non_page_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[a-list]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[items-null]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[no-items-no-count]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[nothing]`

Old text:

```
            if not isinstance(response, dict) or (
```

New text:

```
            if False and (
```

### `r878-a.A7_empty_page_ends`

paginate_cursor: an empty page carrying a cursor no longer ends the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A7_empty_page_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_an_empty_page_ends_the_walk_even_when_it_carries_a_cursor`

Old text:

```
        if not page or not following:
```

New text:

```
        if not following:
```

### `r878-b.B8_first_request_no_cursor`

_folder_endpoint: always send the cursor key, so the first request carries a cursor of None

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B8_first_request_no_cursor`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset`

Old text:

```
        if cursor is not None:
            params["cursor"] = cursor
```

New text:

```
        params["cursor"] = cursor
```

### `u65.B3_playlist_tracks_back_to_the_short_page`

the placeholder acquire read ends on a short page, dropping the rest of a playlist

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B3_playlist_tracks_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_with_no_declared_total_walks_to_an_empty_page`
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
    "playlist_tracks": StopRule.DECLARED_TOTAL,
```

New text:

```
    "playlist_tracks": StopRule.SHORT_PAGE,
```

### `u65.C7_a_zero_total_is_trusted_as_an_end`

the sentinel check goes, so an unparsed num_tracks of -1 ends the walk at once

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C7_a_zero_total_is_trusted_as_an_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`

Old text:

```
        if total is not None and total <= 0:
            total = None
```

New text:

```
        if total is not None and total < -1:
            total = None
```

### `u65.F4_the_favourites_dedup_goes`

U14's dedup: a favourite re-served on a shifted page boundary is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `F4_the_favourites_dedup_goes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_favourite_repeated_across_a_page_boundary_is_returned_once`

Old text:

```
    kwargs.setdefault("key", lambda track: str(getattr(track, "id", "")))
```

New text:

```
    kwargs.setdefault("key", None)
```

### `r1709.M9_title_identity_is_the_fold`

title_identity returns the fold alone, the base's reading, so an emoji title is every other one by the artist

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M9_title_identity_is_the_fold`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 30 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[two-emoji-titles-stay-two-rows]`
  - `tests/intake/test_workers.py::test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id`
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[another-emoji]`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_isrc_screen.py::test_a_provider_track_under_another_emoji_title_does_not_agree`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    bare = bare_title(title)
    return f"\x1f{bare}" if bare else ""

```

New text:

```
    return ""

```

### `u205.O4_app_attached_as_account`

opener: the app client is attached under the account identity, so its calls are reported as the account's

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O4_app_attached_as_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 353 against a baseline of 353
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
    if not gate.attach(client, identity=provider_gate.APP):
```

New text:

```
    if not gate.attach(client, identity=provider_gate.ACCOUNT):
```

### `r703-a.V2_no_forget`

fetch keeps what the constructor logged, so the ffmpeg warning can stand as the item's cause

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V2_no_forget`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_failure_message_with_no_exception_is_the_cause`
  - `tests/test_adapter_contract.py::test_what_the_constructor_logged_is_never_the_items_cause`

Old text:

```
        tool_log.forget()

```

New text:

```
(empty)
```

### `r703-b.O4_wraps_twice`

observe_session wraps an already observed session again

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `O4_wraps_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_observed_session_writes_through_and_raises_what_it_notes`

Old text:

```
    if session is not None and not isinstance(session, _ObservedSession):
```

New text:

```
    if session is not None:
```

### `u47-author.CODEC_alac_reads_as_lossy`

Drop alac from the lossless MP4 codecs, so a genuine ALAC landing is refused

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_alac_reads_as_lossy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_codec_table_answers_for_every_container_it_declares`

Old text:

```
MP4_LOSSLESS_CODECS: frozenset[str] = frozenset({"alac"})
```

New text:

```
MP4_LOSSLESS_CODECS: frozenset[str] = frozenset()
```

### `u47-author.R195_push_empty_instead`

Push the empty string rather than the resolved path, the tool's factory default and the value it reads as do-not-extract-FLAC

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R195_push_empty_instead`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_applying_settings_writes_them_in_memory_and_saves_nothing`
  - `tests/test_adapter_contract.py::test_the_ffmpeg_path_is_the_one_the_binaries_module_resolves`
  - `tests/test_adapter_contract.py::test_the_vendored_settings_translation_names_every_key_that_reverted`
  - `tests/test_adapter_contract.py::test_verification_covers_the_ffmpeg_key_by_it_being_pushed`

Old text:

```
        "path_binary_ffmpeg": ffmpeg,
```

New text:

```
        "path_binary_ffmpeg": "",
```

### `u47-author.R197_drop_event_run`

Drop event_run from the downloader construction

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_drop_event_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
            event_run=event_run,

```

New text:

```
(empty)
```

### `u23-round-8-independent.X9_outstanding_returns_everything`

A resume re-applies every entry from the top

- File: `src/cratekit/adopt/apply.py`
- Source: `u23-round-8-independent.json`, row `X9_outstanding_returns_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one`
  - `tests/test_adoption.py::test_a_second_run_over_a_finished_plan_writes_nothing`

Old text:

```
    return tuple(entry for entry in plan.applicable() if entry.entry_id not in done)
```

New text:

```
    return tuple(plan.applicable())
```

### `u254.M07_always_append`

mark_applied: append even to a torn, absent or schema 1 ledger

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M07_always_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 86 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`
  - ... and 71 more, see the JSON sidecar

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if True:
                config.append_durable_bytes(line, path)
```

### `u254.M16_journal_needs_format`

_is_journal: take any object on the first line as a journal header

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M16_journal_needs_format`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_newer_document_still_asks_for_an_upgrade`

Old text:

```
    return isinstance(header, dict) and header.get("format") == JOURNAL_FORMAT
```

New text:

```
    return isinstance(header, dict)
```

### `r1991.A3_undeclared_raises`

planned_destinations: raise on a destination the taxonomy no longer declares, before the write

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r1991.json`, row `A3_undeclared_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_outside_root.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_filing.py`, `tests/test_organize.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_second_genre_guards_counts.py`
- Collected: 521 against a baseline of 521
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_planned_destinations_name_each_pair_once_and_skip_what_names_none`

Old text:

```
        except KeyError:
            continue
        named.setdefault
```

New text:

```
        except KeyError:
            raise
        named.setdefault
```

### `u132.W1_every_apply`

The adoption runs the Favorites step only when it filed a track

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u132.json`, row `W1_every_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_organize.py`
- Collected: 447 against a baseline of 447
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`

Old text:

```
 or genre_favorites.favorites_class(declared) is None
```

New text:

```
(empty)
```

### `u27-adopt-apply-author.S2_analysis_watch_watches_nothing`

Arm the analysis watch on no roots, so it reports a clean session either way

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S2_analysis_watch_watches_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_write_session.py`
- Collected: 165 against a baseline of 165
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`

Old text:

```
        analysis_roots=watched,
```

New text:

```
        analysis_roots=(),
```

### `u55-round-2.R23_worker_raises_on_failure`

A failed apply returns rather than raising, so the job reaches SUCCEEDED over nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-round-2.json`, row `R23_worker_raises_on_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`

Old text:

```
    if report.failed:
        _commit(produced)
        raise refuse(
```

New text:

```
    if False:
        _commit(produced)
        raise refuse(
```

### `u23-round-8-independent.X5_grant_accepts_a_blank_actor`

grant records an approval attributed to nobody

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X5_grant_accepts_a_blank_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_with_no_actor_is_refused`

Old text:

```
    if not str(actor).strip():
```

New text:

```
    if actor is None:
```

### `r780-a.A2_tree_path_adds_a_sub`

in a bucket the genre does not name, a reading naming none of the held subs plans a move that adds that sub and removes the rest, filing the track by a rule adoption does not use

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A2_tree_path_adds_a_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_double_beside_a_track_left_for_another_reason_is_still_listed`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_track_with_no_genre_is_asked_in_every_bucket_it_doubles_in`
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[names-neither-elsewhere]`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_the_gate_shows_every_move_with_what_it_adds_removes_and_reads`

Old text:

```
    elif target not in held:
        reason = LEFT_NAMES_NEITHER

```

New text:

```
(empty)
```

### `r797-d.M6_again_settled_in_one_bucket`

M6 measured again after the second review replaced its guard: read a former place the entry's own bucket settles as still held in the other, so one membership is planned twice or a track is listed beside its move

- File: `src/cratekit/adopt/move.py`
- Source: `r797-d.json`, row `M6_again_settled_in_one_bucket`
- Moved: the same expression in held_in_tree, now one line; the settled places are no longer taken away, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[another-band]`
  - `tests/test_adopt_former_place.py::test_a_place_the_holding_bucket_settles_is_not_asked_about_in_the_declaring_one[its-reading]`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_whose_genre_names_another_style_moves_to_that_style`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_with_nothing_to_move_on_is_listed_under_its_reason[defaulted-genre]`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`

Old text:

```
    return tuple(sorted((set(placements.holds(bucket, entry.content_id)) & competing) - settled))
```

New text:

```
    return tuple(sorted(set(placements.holds(bucket, entry.content_id)) & competing))
```

### `u118-c.M8_asked_split`

The plan never asks about a bucket where the track is only in a split place nobody claims

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M8_asked_split`
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
        if held_in_split_place(entry, bucket.id, placements, declared):
            asked.append(bucket.id)
            continue

```

New text:

```
(empty)
```

### `r780-b.B3_renamed_target_reads_as_done`

a track whose one place is its target through a renamed playlist reads as finished, which nobody was shown

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B3_renamed_target_reads_as_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_target_held_only_under_another_name_is_not_done`

Old text:

```
            if held == {move.target} and not unnamed & held:
                continue
```

New text:

```
            if held == {move.target}:
                continue
```

### `r788-c.L1_any_vox_value_is_the_tag`

vox_tagged: a value named vox under any category is the tag

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L1_any_vox_value_is_the_tag`
- Moved: the same condition joined onto one line by the formatter; the category test is dropped, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_removed_value_or_category_is_no_tag_at_all`
  - `tests/test_adopt_vocals.py::test_a_value_of_that_name_under_another_category_is_another_tag`

Old text:

```
        if str(getattr(tag, "ParentID", "") or "") in categories and not _removed(tag, "My Tag")
```

New text:

```
        if not _removed(tag, "My Tag")
```

### `u118-b.P1_named_place_split`

named_place resolves a split place as a sub of the declaring bucket

- File: `src/cratekit/adopt/placements.py`
- Source: `u118-b.json`, row `P1_named_place_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_placements.py`
- Collected: 143 against a baseline of 143
- Kills: 25 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_placements.py::test_a_band_label_a_bucket_overrides_still_resolves_to_the_band`
  - `tests/test_adopt_placements.py::test_a_double_in_a_playlist_that_is_not_a_place_is_not_carried`
  - `tests/test_adopt_placements.py::test_a_double_in_a_renamed_recorded_node_is_still_a_double`
  - `tests/test_adopt_placements.py::test_a_node_carrying_the_declared_names_is_the_sub_it_names`
  - `tests/test_adopt_placements.py::test_a_pair_held_by_two_rows_is_held_once_and_doubled`
  - `tests/test_adopt_placements.py::test_a_recorded_node_that_carries_the_declared_names_is_not_unnamed`
  - `tests/test_adopt_placements.py::test_a_renamed_node_is_resolved_through_its_recorded_identifier`
  - `tests/test_adopt_placements.py::test_a_sub_class_playlist_and_a_hand_made_one_are_not_places`
  - `tests/test_adopt_placements.py::test_a_sub_held_under_both_names_is_one_the_writer_can_see`
  - `tests/test_adopt_placements.py::test_a_track_in_two_bands_holds_both`
  - `tests/test_adopt_placements.py::test_two_nodes_answering_for_one_destination_both_count`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        return named_place(declared, split.bucket, split.sub)
```

New text:

```
        return destination(declared, bucket_id, sub_id)
```

### `r722.P4_entry_drops_energy`

The plan entry does not carry the census's level

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P4_entry_drops_energy`
- Moved: the PlanEntry is now built before _destined routes it, four spaces less indented; the energy field is dropped from it
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`

Old text:

```
            energy=track.energy,
            energy_unreadable=track.energy_unreadable,
```

New text:

```
            energy_unreadable=track.energy_unreadable,
```

### `r731-a.M06_competing_place_never_withholds`

the plan reads the competing place and routes the entry anyway

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M06_competing_place_never_withholds`
- Moved: a competing place now withholds in _destined, which build_adoption_plan and with_verdicts share; the competing place is ignored as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 13 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_collision_verdict_withholds_under_its_own_reason_and_own_count`
  - `tests/test_adopt_placements.py::test_a_genre_answered_later_is_withheld_over_the_place_the_track_holds`
  - `tests/test_adopt_placements.py::test_a_track_in_a_band_whose_file_has_no_reading_is_withheld_from_the_sink`
  - `tests/test_adopt_placements.py::test_a_track_in_one_band_whose_file_reads_another_is_withheld_and_listed`
  - `tests/test_adopt_placements.py::test_a_track_in_one_style_sub_is_withheld_from_another`
  - `tests/test_adopt_placements.py::test_a_track_in_the_no_reading_sub_whose_file_now_reads_is_withheld`
  - `tests/test_adopt_placements.py::test_a_track_in_the_planned_sub_under_another_name_only_is_withheld`
  - `tests/test_adopt_placements.py::test_a_track_in_two_bands_is_withheld_from_a_third_and_both_are_listed`
  - `tests/test_adopt_placements.py::test_the_digest_covers_every_field_the_review_list_shows`
  - `tests/test_adopt_placements.py::test_the_digest_differs_between_a_plan_with_a_withheld_entry_and_one_without`
  - `tests/test_adopt_placements.py::test_the_digest_moves_when_a_withheld_track_is_moved_to_another_band`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
        disposition = Disposition.WITHHELD if withheld_by else Disposition.ROUTE
```

New text:

```
        disposition = Disposition.WITHHELD if False else Disposition.ROUTE
```

### `r788-a.P3_uncalibrated_files`

Vocals.filing: drop the calibration, so tags written from the default cut file a back catalogue

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P3_uncalibrated_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_library_with_no_calibrated_cut_plans_no_vocal_membership`
  - `tests/test_adopt_vocals.py::test_each_reason_nothing_can_be_filed_plans_nothing_for_a_tagged_track`
  - `tests/test_adopt_vocals.py::test_the_digest_says_whether_the_tag_and_the_tree_were_read`
  - `tests/test_adopt_vocals.py::test_whether_the_library_is_calibrated_is_carried_and_not_assumed`

Old text:

```
        return self.read and self.has_sub and self.calibrated
```

New text:

```
        return self.read and self.has_sub
```

### `r788-b.P19_answered_genre_files_nothing`

with_verdicts: an answered genre is asked of no vocals, so a tagged track given a bucket is never filed under its vocal sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P19_answered_genre_files_nothing`
- Moved: with_verdicts now routes an answered entry through _destined; the plan's vocals are replaced with none as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_an_answered_genre_is_filed_under_the_vocal_sub_of_the_bucket_it_was_given`

Old text:

```
            _destined(declared, plan.placements, plan.vocals, sub_of, entry, chosen, sub)
```

New text:

```
            _destined(declared, plan.placements, NO_VOCALS, sub_of, entry, chosen, sub)
```

### `u956.S21_excluded_applicable`

existing, PlanEntry.applicable: any entry not excluded is applicable, so a needs-genre or withheld track is written

- File: `src/cratekit/adopt/plan.py`
- Source: `u956.json`, row `S21_excluded_applicable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 687 against a baseline of 687
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adoption.py::test_a_track_needing_a_genre_becomes_a_review_item_not_a_file`
  - `tests/test_adoption.py::test_a_withheld_entry_is_never_written_by_an_apply`
  - `tests/test_adoption.py::test_an_answer_naming_an_undeclared_bucket_is_ignored`
  - `tests/test_adoption.py::test_an_answered_genre_question_turns_the_track_into_work`
  - `tests/test_adoption.py::test_answering_keep_separate_actually_leaves_that_folder_alone`
  - `tests/test_adoption.py::test_every_plan_entry_identifier_is_derivable_from_the_record_it_names`
  - `tests/test_adoption.py::test_re_offering_a_settled_question_does_not_reopen_it`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`

Old text:

```
        return self.disposition is Disposition.ROUTE
```

New text:

```
        return self.disposition is not Disposition.EXCLUDED
```

### `u23-round-8-independent.B3_settled_bytes_clause_inverted`

The bytes acceptance fires when the bytes DISAGREE

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `B3_settled_bytes_clause_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    if _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT
```

New text:

```
    if not _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT
```

### `u23-round-8-independent.F1_byte_search_drops_the_vacancy_filter`

A record whose path still holds its file is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `F1_byte_search_drops_the_vacancy_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_first_adoption_of_EIGHT_files_reads_EIGHT_times_and_not_FIFTEEN`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    vacant = [record for record in possible if _the_recorded_path_is_vacant(record)]
```

New text:

```
    vacant = list(possible)
```

### `u23-round-8-independent.X13_look_at_drops_the_recorded_size_shortcut`

The prefetch reads a file whose size already rules the record out

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `X13_look_at_drops_the_recorded_size_shortcut`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_file_of_a_DIFFERENT_SIZE_is_refused_without_reading_it`

Old text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)

```

New text:

```
(empty)
```

### `u23-round-8-independent.X7_classify_accepts_the_fallback_tier`

An unrecognised genre is routed in bulk by the router's fallback

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X7_classify_accepts_the_fallback_tier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_the_fallback_tier_is_never_accepted_as_an_adoption_answer`

Old text:

```
    if resolution.match is routing.Match.FALLBACK:
        return Disposition.NEEDS_GENRE, "", str(resolution.match)

```

New text:

```
(empty)
```

### `u956.O2_confine_flag_ignored`

scan_rows: confine whatever the flag says, so the tag verbs' walk stops reading a row outside the root

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O2_confine_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_tag_backlog.py`, `tests/test_adoption.py`
- Collected: 703 against a baseline of 703
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_tagging_walk_still_reads_a_row_outside_the_root`

Old text:

```
        if readability is None and confine_to_root and not within_root(path or "", root):
```

New text:

```
        if readability is None and not within_root(path or "", root):
```

### `u247.M8_scan_freezes_its_declaration`

adopt scan handle: judge every row of a job by the declaration its first row read, R-690's open question decided by accident

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u247.json`, row `M8_scan_freezes_its_declaration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_active_taxonomy.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`

Old text:

```
    declared = active_taxonomy.load(cfg)
    (classified,) = scan_engine.scan_rows(
```

New text:

```
    declared = scan_engine.__dict__.setdefault(("u247", job.job_id), active_taxonomy.load(cfg))
    (classified,) = scan_engine.scan_rows(
```

### `u241.M24_identity_after_the_read`

ahead.measure: the identity is taken after the read, so a file written while it was read carries the written file's identity

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M24_identity_after_the_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_replaced_after_its_head_was_measured_is_measured_again`
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`
  - `tests/test_analysis_ahead.py::test_the_identity_a_worker_returns_is_the_files_before_the_read`

Old text:

```
    found = identity_of(path)
    return found, light.analyse(path)

```

New text:

```
    head = light.analyse(path)
    return identity_of(path), head

```

### `u223.M3_no_clear`

staged_path: clear nothing, so a stale report and scratch leak into the next attempt

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M3_no_clear`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_tag_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_linked_intent_is_cleared_rather_than_kept_and_followed`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
            else:
                entry.unlink()
```

New text:

```
            continue
```

### `u306.A6_item_record_unreadable`

analysis.artifacts._item_record: a record that does not parse raises rather than reading as none

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u306.json`, row `A6_item_record_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_drift.py`, `tests/test_shared_homes.py`
- Collected: 318 against a baseline of 318
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin`

Old text:

```
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
```

New text:

```
    except OSError:
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
```

### `u90-b.B2_method_not_hand`

A hand cut recorded under the fit's method, otsu

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B2_method_not_hand`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`

Old text:

```
method=VOCAL_METHOD_HAND, note=
```

New text:

```
method="otsu", note=
```

### `u90-c.C3_hand_branch_wrong_method`

The replaced cut is named as set by hand only when its method is otsu

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-c.json`, row `C3_hand_branch_wrong_method`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    if record.get("method") == VOCAL_METHOD_HAND:
```

New text:

```
    if record.get("method") == "otsu":
```

### `u94-a.S8_after_walk_never_asked`

analyze_calibrate: never ask what the walk left out, so a root missing a linked or unreadable genre reads ok

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S8_after_walk_never_asked`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        partial = _partial_after_walk(scan)
```

New text:

```
        partial = None
```

### `u94-c.N1_stride_is_the_first_n`

stride_sample: take the first N of the sorted walk, which is the first few folders of the alphabet

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N1_stride_is_the_first_n`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`
  - `tests/test_analysis_workers.py::test_the_stride_sample_is_even_ordered_and_reaches_the_tail`

Old text:

```
    return [items[index * total // count] for index in range(count)]
```

New text:

```
    return list(items[:count])
```

### `u157.A2_cut_unbound`

_bind_defaults: bind no drift cut, so the detector reads the shipped default

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A2_cut_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`, `tests/test_head_agreement.py`
- Collected: 283 against a baseline of 283
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_worker_process_with_nothing_bound_binds_the_shipped_defaults`
  - `tests/test_analysis_workers.py::test_the_default_detector_is_rebound_with_a_fresh_calibration_per_item`
  - `tests/test_drift.py::test_a_whole_number_cut_loads_and_reaches_the_detector_binding`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,

```

New text:

```
(empty)
```

### `u223.M20_twin_target_unchecked`

_finalized_twin: an existing guard, accept a target that is not a file

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M20_twin_target_unchecked`
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
    if target is None or not target.is_file():
        return None
    return target
```

New text:

```
    if target is None:
        return None
    return target
```

### `u306.A3_walk_recursive`

analysis.cli.walk_folder: ignore --recursive, so a nested file is never queued by restamp or vocals

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A3_walk_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 18 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_appledouble_sidecar_and_a_dot_directory_are_not_items`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_freezes_the_flag_in_the_payload`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_runs_every_nested_item_to_done_and_writes_the_right_file`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`
  - `tests/test_analysis_workers.py::test_two_nested_folders_holding_the_same_filename_are_two_items`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_nested_sidecar_and_a_dot_directory_are_not_vocals_items`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_queues_every_nested_file_once_in_sorted_order`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
```

New text:

```
    recursive = False
```

### `u343.M07_waiting_takes_measured_files`

_waiting: hand the pool files already measured, so workers read files the driver skips

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M07_waiting_takes_measured_files`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`
- Collected: 449 against a baseline of 449
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_ahead.py::test_a_resume_with_nothing_left_to_measure_keeps_the_pool_that_measured_the_job`

Old text:

```
        if path.is_file() and not already_measured(path, cfg):
```

New text:

```
        if path.is_file():
```

### `u90-a.A7_exclusive_group_gone`

The folder and the flag no longer mutually exclusive in the parser

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A7_exclusive_group_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_and_a_hand_cut_together_are_refused_by_the_parser`

Old text:

```
    chosen = parser.add_mutually_exclusive_group()
```

New text:

```
    chosen = parser
```

### `u263.D23_cover_lines`

_audio_faults: keep the cover decoders' lines, so a cover ffmpeg cannot read fails a whole track

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D23_cover_lines`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_cover_complaint_is_dropped_and_an_audio_complaint_is_kept`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[broken-png]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[gif-as-jpeg]`
  - `tests/test_analysis_decode.py::test_a_cover_ffmpeg_cannot_read_leaves_a_whole_track_decodable[webp-as-jpeg]`

Old text:

```
        if line.strip() and not line.startswith(tuple(f"[{name} @ " for name in _COVER_DECODERS))
```

New text:

```
        if line.strip()
```

### `u264.M11_ffmpeg_left_channel`

decode.load: mix the ffmpeg path's samples by keeping the left channel

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M11_ffmpeg_left_channel`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    native = _window(native, native_rate, offset=offset, duration=duration)
    return _mono_at(librosa, native, native_rate, rate), rate
```

New text:

```
    native = _window(native, native_rate, offset=offset, duration=duration)
    native = native[0] if native.ndim == 2 else native
    return _mono_at(librosa, native, native_rate, rate), rate
```

### `u264.M5_halving`

_mean_of_two: return the sum of the two channels, not its half

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M5_halving`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0-right5-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left4-0.0-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left6--0.0-00000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left7-0.0-00000002-00000002]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left8--0.0-80000002-80000002]`
  - `tests/test_analysis_decode.py::test_the_half_sum_of_two_channels_rounds_once_like_float64[0.10-0.11]`
  - `tests/test_analysis_decode.py::test_the_half_sum_of_two_channels_rounds_once_like_float64[1.0]`

Old text:

```
    out /= out.dtype.type(2)
```

New text:

```
    out /= out.dtype.type(1)
```

### `u157.D2_band_wide`

DRIFT_BAND: widened to 0.5, so a window reaches a related metrical level

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D2_band_wide`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
DRIFT_BAND = 0.25
```

New text:

```
DRIFT_BAND = 0.5
```

### `u343.M21_stages_keep_the_key_stage`

detect.STAGES: name the chroma and key stage again, which no run meets

- File: `src/cratekit/analysis/detect.py`
- Source: `u343.json`, row `M21_stages_keep_the_key_stage`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_stages.py`, `tests/test_analysis_workers.py`
- Collected: 204 against a baseline of 204
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_stages.py::test_the_scripts_stage_names_are_the_detectors_and_the_vocal_passs`
  - `tests/test_analysis_stages.py::test_the_stages_are_decode_tempo_and_drift_and_energy`

Old text:

```
STAGES = ("decode", "tempo_drift", "energy")
```

New text:

```
STAGES = ("decode", "tempo_drift", "chroma_key", "energy")
```

### `u58-workers-and-wav.S4_undo_overwritten`

Let a second restamp overwrite the first previous value

- File: `src/cratekit/analysis/energy.py`
- Source: `u58-workers-and-wav.json`, row `S4_undo_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_undo_log_keeps_the_first_previous_value_across_a_second_restamp`

Old text:

```
        if key in log:
            return False

```

New text:

```
(empty)
```

### `u327.A19_row_follows_file`

apply_adopt: write a row whose file did not take, so the title and the tag disagree

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A19_row_follows_file`
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
        rowed = [item for item in writes if item.content_id in landed and item.writes_title]
```

New text:

```
        rowed = [item for item in writes if item.writes_title]
```

### `u342.E2_policy_before_files`

apply_adopt (existing, sample): skip asking the policy of the whole plan before the first file

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `E2_policy_before_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_plan_that_would_write_the_tempo_column_is_refused_by_policy`

Old text:

```
    metadata.assert_within_policy(row_changes(writes))
```

New text:

```
    pass
```

### `u342.P5_stamped_writes`

WRITING: drop stamped, so a stamped row is planned and never written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P5_stamped_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 8 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_written_message_counts_only_stamped_files_that_took_it`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
WRITING: tuple[str, ...] = (ADOPT, STAMPED)
```

New text:

```
WRITING: tuple[str, ...] = (ADOPT,)
```

### `u342.C3_written_counts_stamps`

_written: count every row that took its title as stamped

- File: `src/cratekit/analysis/head_adopt_cli.py`
- Source: `u342.json`, row `C3_written_counts_stamps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_written_message_counts_only_stamped_files_that_took_it`

Old text:

```
item.action == ha.STAMPED and item.content_id in landed)
```

New text:

```
item.content_id in landed)
```

### `u275.M5_decode_line_dropped`

worker_bytes: drop the decode line, so a 192 kHz file costs only its length's analysis line

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M5_decode_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 555 against a baseline of 555
- Kills: 29 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[1-384000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-192000-86400.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-236.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-3600.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-45.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-660.0]`
  - `tests/test_analysis_ahead.py::test_no_shape_of_file_costs_less_than_it_did_before_u275[2-384000-86400.0]`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    return LIGHT_BASE_BYTES + max(analysis, decode)
```

New text:

```
    return LIGHT_BASE_BYTES + analysis
```

### `sitting3.G10_lone_clip_not_padded`

A lone clip shorter than the floor goes to the network unpadded

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G10_lone_clip_not_padded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_lone_short_clip_is_padded_to_the_floor`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    if len(slices) == 1:
        pad = floor - int(last.shape[-1])
        return [np.concatenate([last, np.zeros((last.shape[0], pad), last.dtype)], axis=-1)]

```

New text:

```
    if len(slices) == 1:
        return slices

```

### `sitting3.G5_loader_skips_readiness`

Ask the library for files that are not there, which is the wget shell out

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G5_loader_skips_readiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_refuses_before_the_extra_is_asked_for_a_missing_checkpoint`

Old text:

```
    missing = scoring.missing_requirement()
    if missing is not None:
        raise FileNotFoundError(missing)

```

New text:

```
    missing = None
    if missing is not None:
        raise FileNotFoundError(missing)

```

### `u58-workers-and-wav.W2_decoder_seam_ignored`

Ignore the bound decoder and always use the shipped one

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W2_decoder_seam_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_run_with_the_model_loaded_carries_no_vocal_warning`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    decoder = _DECODER
    if decoder is None:
        from cratekit.analysis.vocal import decode

        decoder = decode
    return decoder(path)
```

New text:

```
    from cratekit.analysis.vocal import decode

    return decode(path)
```

### `u92-author.G3_cap_coefficient`

Megabytes instead of mebibytes, a realistic nearby value off by 4.9 percent

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G3_cap_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_shipped_oversize_cap_is_two_hundred_and_fifty_mebibytes`

Old text:

```
VOCAL_MAX_BYTES = 250 * 1024 * 1024
```

New text:

```
VOCAL_MAX_BYTES = 250 * 1000 * 1000
```

### `r1761.P24_flag_lost_in_the_worker`

perform_backup: the frozen flag is not handed to the plan, so a queued emptied backup refuses

- File: `src/cratekit/backup/cli.py`
- Source: `r1761.json`, row `P24_flag_lost_in_the_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            emptied=bool(payload.get(EMPTIED)),
```

New text:

```
            emptied=False,
```

### `r221-b.M2_refusal_step_unconditional`

Every refusal gains the sentence, so a person whose REAL backup failed is told nothing was copied and stops looking for the half that was

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M2_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    cause = error.cause
```

### `r222-b.B2_any_verb_is_a_twin`

Drop the handler key comparison, so another verb's open job is reported as the backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B2_any_verb_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_job_that_is_not_this_backup_does_not_stand_in_for_it[another-verb]`

Old text:

```
        if job.handler_key != handler_key or job.library_id != cfg.library.volume_id:
```

New text:

```
        if job.library_id != cfg.library.volume_id:
```

### `r290-author.R2_backup_rebuild_drops_the_type`

Rebuild the backup rehearsal refusal as a plain CratekitError again, so a rehearsal the worker parked says failed

- File: `src/cratekit/backup/cli.py`
- Source: `r290-author.json`, row `R2_backup_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_backup_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r390-a.A6_backup_transfer_exit_is_permanent`

the flag the review round added: a transfer exit recorded with no retryable flag

- File: `src/cratekit/backup/cli.py`
- Source: `r390-a.json`, row `A6_backup_transfer_exit_is_permanent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_decides_the_run_even_when_the_other_completed`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
            retryable=True,
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
```

New text:

```
            origin=("backup", "cli"),
            detail={"portions": [entry.portion.value for entry in failed]},
```

### `u45-round-1.A1_unreadable_reported_as_absent`

Return an empty list for an unreadable fact file, so a library with a good backup reads as never backed up

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `A1_unreadable_reported_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_fact_file_that_cannot_be_read_refuses_rather_than_reporting_nothing`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`
  - `tests/test_backup_cli.py::test_the_remedy_for_an_unreadable_fact_file_travels_from_the_exception`

Old text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        raise refuse(
            "backup-facts-unreadable",
```

New text:

```
    except backup_facts.BackupFactsUnreadable as exc:
        del exc
        return []
        raise refuse(
            "backup-facts-unreadable",
```

### `u45-round-1.Q1_resume_drops_the_rehearsal`

Drop --dry-run from the resume argv, so a queued rehearsal respawns as a real transfer that publishes an age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q1_resume_drops_the_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_resume_rebuilds_the_rehearsal_flag_and_never_carries_a_run`

Old text:

```
    if payload.get(DRY_RUN):
        argv.append("--dry-run")
```

New text:

```
    pass
```

### `u45-round-1.W4_ages_derived_from_the_outcome`

Derive the published ages from the outcome instead of reading the fact file, the duplicate rule the module argues against

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W4_ages_derived_from_the_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = [
        {"portion": p.portion.value, "state": "known" if p.ran else "never-recorded"}
        for p in outcome.portions
    ]
```

### `u50-author.W1_no_narrowing`

Ignore the portion and run the whole plan for every item, so each item does the whole backup

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W1_no_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if portion is not None:
```

New text:

```
    if False:
```

### `r678-b.B1_emit_hands_in_no_drive`

the dispatcher never looks the drive up, so no queueing verb names its command

- File: `src/cratekit/cli/__init__.py`
- Source: `r678-b.json`, row `B1_emit_hands_in_no_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_acquire_workers.py::test_queueing_a_download_names_the_job_and_the_command_that_drives_it`
  - `tests/test_tag_workers.py::test_queueing_a_folder_names_the_job_and_the_command_that_drives_it`

Old text:

```
    print(render.render(envelope, drive=_drive_argv(envelope)), end="", file=stream)
```

New text:

```
    print(render.render(envelope), end="", file=stream)
```

### `r388-d.M16_named_stamp_step_dropped_remeasured`

Re-measure of M16 after the pin: drop the named stamp step added to no-snapshot-available

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-d.json`, row `M16_named_stamp_step_dropped_remeasured`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 660 against a baseline of 660
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-identity-2026-08-01T000000Z-the snapshot 2026-08-01T000000Z was not found]`

Old text:

```
            "when --snapshot named a stamp, that snapshot or its database "
            "folder is not on the remote; check the stamp, or leave the flag "
            "off to take the newest",

```

New text:

```
(empty)
```

### `u328.S1_a_part_left_out_of_the_table`

ENTRIES: leave the modules part out of the assembly, so adoption, deletion, export and the utilities are not registered

- File: `src/cratekit/cli/registry.py`
- Source: `u328.json`, row `S1_a_part_left_out_of_the_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cli_lazy.py`, `tests/test_crate_sync_skill.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_docs_current.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_gate_not_reached.py`, `tests/test_gate_siblings.py`, `tests/test_gate_stale_screen.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_import_rules.py`, `tests/test_install_command.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_artists.py`, `tests/test_label_heard.py`, `tests/test_label_judge.py`, `tests/test_label_playlists.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_paths_resolved.py`, `tests/test_pending_units.py`, `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_report_genres.py`, `tests/test_reports_cli.py`, `tests/test_restamp_scored_by.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_run_retire.py`, `tests/test_schedule.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_setup_discogs.py`, `tests/test_sync_all.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_sync_mark.py`, `tests/test_sync_night.py`, `tests/test_sync_removed.py`, `tests/test_sync_removed_gone.py`, `tests/test_sync_unmark.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_tag_guess.py`, `tests/test_tag_remap.py`, `tests/test_tag_rows.py`, `tests/test_tag_second.py`, `tests/test_tag_set.py`, `tests/test_tag_suggest.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_u242_taken.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8498 against a baseline of 8614
- Kills: 499 (collect-error)
- Note: collection changed: 8498 collected against a baseline of 8614. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/modules/test_tools.py::test_every_declared_verb_is_in_the_static_registry`
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_workflow_name_and_the_registry_verb_name_cannot_drift`
  - `tests/test_adopt_move.py::test_a_cancelled_move_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_failure_in_the_additions_writes_nothing_at_all`
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`
  - `tests/test_adopt_move.py::test_a_job_carrying_no_plan_is_refused_rather_than_driven`
  - `tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero`
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - ... and 484 more, see the JSON sidecar

Old text:

```
    *MODULE_VERBS,

```

New text:

```
(empty)
```

### `r682-a.M7_reason_line_not_printed`

the rendering computes the reasons and never prints the line

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M7_reason_line_not_printed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[complete]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[empty]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[no-whole-count]`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[partial]`
  - `tests/test_render_payloads.py::test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug`

Old text:

```
        if reasons:
            lines.append(f"    by reason: {reasons}")
```

New text:

```
        if False:
            lines.append(f"    by reason: {reasons}")
```

### `r685-a.L7_a_parse_failure_names_a_defect`

The parse refusal's remedy moves from run setup to report a defect, disagreeing with doctor

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L7_a_parse_failure_names_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-toml]`

Old text:

```
            f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.RUN_SETUP,

```

New text:

```
            f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.REPORT_DEFECT,

```

### `u260.E2_key_drops_size`

to_cdj_jpeg_remembered: key without the edge, so a picture asked for at another size is the first size's

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E2_key_drops_size`
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
    key = (hashlib.sha256(data).digest(), len(data), None, max_bytes)
```

### `u301.A1_decoded_rgb_skips_the_orientation`

_decoded_rgb: drop the EXIF transpose, so a rotated photo is encoded on its side

- File: `src/cratekit/core/art.py`
- Source: `u301.json`, row `A1_decoded_rgb_skips_the_orientation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`, `tests/test_album_cover_once.py`, `tests/test_tagging_engine.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_an_exif_orientation_is_baked_into_the_pixels`

Old text:

```
            return _flatten_to_rgb(ImageOps.exif_transpose(source))
```

New text:

```
            return _flatten_to_rgb(source)
```

### `u83-a.E7_flatten_transparency`

Transparency is no longer composited, a plain mode conversion exposes what lies under it

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E7_flatten_transparency`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_art.py::test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it[LA]`
  - `tests/test_art.py::test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it[P]`
  - `tests/test_art.py::test_transparency_is_flattened_onto_white_not_onto_what_lies_under_it[RGBA]`

Old text:

```
    if not has_alpha:
```

New text:

```
    if True:
```

### `u83-b.W1_undecodable_guard`

The writer's refusal of undecodable bytes is dropped, so they go on toward the file

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W1_undecodable_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.aiff]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.flac]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.m4a]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.mp3]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[unreadable.wav]`

Old text:

```
    if measured is None:
        raise ArtError("the picture bytes could not be decoded, so nothing was written")

```

New text:

```
(empty)
```

### `u83-b.W9_id3_delall`

The ID3 writer stops clearing pictures other tools embedded under another description

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W9_id3_delall`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_art.py::test_an_id3_picture_another_tool_embedded_is_replaced_too[.aiff]`
  - `tests/test_art.py::test_an_id3_picture_another_tool_embedded_is_replaced_too[.mp3]`
  - `tests/test_art.py::test_an_id3_picture_another_tool_embedded_is_replaced_too[.wav]`

Old text:

```
            handle.tags.delall("APIC")

```

New text:

```
(empty)
```

### `u45-round-1.E8_naive_timestamp_stored`

Accept a naive completion timestamp at the boundary, so the instant recorded depends on who reads it

- File: `src/cratekit/core/backup_facts.py`
- Source: `u45-round-1.json`, row `E8_naive_timestamp_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_reserved_causes.py`, `tests/test_write_session.py`
- Collected: 1072 against a baseline of 1072
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_naive_timestamp_is_refused_where_it_is_produced`

Old text:

```
    if completed_at.tzinfo is None:
        raise ValueError(
```

New text:

```
    if False:
        raise ValueError(
```

### `u331.S02_yt_dlp_said_dropped`

binaries.yt_dlp_missing: print the exception alone, so the caller's own sentence of what was not done is gone from the message

- File: `src/cratekit/core/binaries.py`
- Source: `u331.json`, row `S02_yt_dlp_said_dropped`
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
        f"{exc} {said}",
```

New text:

```
        f"{exc}",
```

### `r301.F1_section_not_built`

The recognition section is never read from the file, so every install gets the default

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `F1_section_not_built`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`, `tests/intake/test_workers.py`
- Collected: 320 against a baseline of 320
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[set]`
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

### `r290-author.J1_blocked_branch_removed`

Skip the blocked branch of raise_for_state, so a parked job falls through to the closed predicate that cannot see it, which is R-290 itself

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J1_blocked_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 49 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_blocked_job_raises_the_blocked_type_carrying_the_jobs_own_cause`
  - `tests/test_job_outcome.py::test_a_blocked_job_recording_no_reason_is_still_not_a_success`
  - `tests/test_job_outcome.py::test_a_park_on_a_gate_coded_cause_is_still_not_resumable_through_the_run`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.bandcamp-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.fallback-fetch]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[adopt.scan]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.restamp]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.vocals]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[backup.run]`
  - ... and 34 more, see the JSON sidecar

Old text:

```
    if job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

New text:

```
    if False and job.state is JobState.BLOCKED:
        # ``transition`` refuses
```

### `r390-a.A5_refusal_drops_the_inner_cause`

the refusal no longer nests the job's own cause, so the item's reason is unreachable

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A5_refusal_drops_the_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 210 against a baseline of 210
- Kills: 4 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )
```

New text:

```
                **_permanent_reasons_of(current.cause),
            },
        )
```

### `r669-b.B1_composer_not_sanitized`

G14's composite: drop the one sanitizer, the composer's, now that the copy in _artist is gone, so a slash in a credit reaches the filename

- File: `src/cratekit/core/naming.py`
- Source: `r669-b.json`, row `B1_composer_not_sanitized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 134 against a baseline of 134
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_stem_is_the_rows_and_carries_no_path_separator`
  - `tests/test_naming_apply_cli.py::test_an_identifier_stem_composes_its_one_name[a-slash-takes-the-body-form-of-a-segment]`

Old text:

```
        part for part in (sanitize_segment(artist or ""), sanitize_segment(title or "")) if part
```

New text:

```
        part for part in (artist or "", title or "") if part
```

### `u205.G1_app_call_not_counted`

gate: a call under the app identity is counted in the totals and not under the app, so every report reads it as the account's

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G1_app_call_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 184 against a baseline of 184
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_state_file_written_before_the_identities_loads_with_every_call_the_accounts`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
        if app:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
```

New text:

```
        if False:
            state.app_calls += 1
            _PROCESS_APP_CALLS += 1
```

### `u301.G6_totals_drop_the_app`

_State.totals: report no app calls, so the spend a report and the gate read loses the app's share

- File: `src/cratekit/core/provider_gate.py`
- Source: `u301.json`, row `G6_totals_drop_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_catalogue_app.py`
- Collected: 246 against a baseline of 246
- Kills: 5 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_an_app_share_larger_than_the_total_is_clamped_to_it`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - `tests/test_catalogue_app.py::test_the_opener_attaches_the_app_client_under_the_app_identity`

Old text:

```
        return Spend(self.calls, self.rate_limited, self.app_calls, self.app_rate_limited)
```

New text:

```
        return Spend(self.calls, self.rate_limited, 0, 0)
```

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2744 against a baseline of 2744
- Kills: 176 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[True]`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - ... and 161 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `r118-a.A2_enoent_refuses_too`

A fresh installation with no index refuses instead of answering nothing recorded, so the product cannot be set up

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A2_enoent_refuses_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1592 against a baseline of 1592
- Kills: 169 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_bound_identifier_resolves_its_seams_at_call_time`
  - `tests/intake/test_recognition.py::test_the_keychain_credentials_are_read_by_name_and_a_missing_one_is_credential_missing`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-credentials]`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-section]`
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_missing_recording_is_refused_by_name_and_a_tilde_is_expanded_before_the_look`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`
  - `tests/intake/test_workers.py::test_a_repeated_recording_in_one_set_is_one_item_per_play_and_one_per_fold`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_nobody_recognised_is_an_honest_zero_that_says_what_it_cost`
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - ... and 154 more, see the JSON sidecar

Old text:

```
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
```

New text:

```
    except OSError as exc:
```

### `r722.T9_lenient_open_raises`

The lenient reader raises when mutagen cannot open a file

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T9_lenient_open_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2994 against a baseline of 2994
- Kills: 306 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`
  - `tests/test_match_states.py::test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - ... and 291 more, see the JSON sidecar

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
```

### `u310.G2_gate_digest_is_the_plan`

review: the gate digests a constant, so a confirmation of another plan is honoured

- File: `src/cratekit/deletion/cli.py`
- Source: `u310.json`, row `G2_gate_digest_is_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_uncredited_tombstone.py`, `tests/behaviour/deletion.py`
- Collected: 393 against a baseline of 393
- Kills: 1 (killed)
- Killed:
  - `tests/behaviour/deletion.py::test_review_refuses_a_decision_whose_digest_moved`

Old text:

```
        option = ctx.gate.require(spec, digest=_plan_digest(found), context=_shown(found))
```

New text:

```
        option = ctx.gate.require(spec, digest="constant", context=_shown(found))
```

### `r706-a.A2_ceiling_one_part_wider`

The ceiling admits one part more than MAX_PARTS, a coefficient row on the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A2_ceiling_one_part_wider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_and_neither_spend_refusal_is_a_miss`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`

Old text:

```
    ceiling = budget.per_run * MAX_PARTS
```

New text:

```
    ceiling = budget.per_run * (MAX_PARTS + 1)
```

### `r706-b.B3_partition_drops_the_remainder`

Every part is cut to the base size, so the remainder chunks fall out of the grid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B3_partition_drops_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
        parts.append(tuple(offsets[start : start + size]))
```

New text:

```
        parts.append(tuple(offsets[start : start + base]))
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

### `u103-a.A6_digest_in_the_key`

Take the recording's content digest out of the key material, so a changed file keeps its old key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A6_digest_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[file]`
  - `tests/intake/test_recognition.py::test_every_field_of_the_plan_moves_the_key[digest]`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
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

### `u57-recognition-and-items.M2_quota_family_empty`

3003 stops being a quota answer, so a spent account reads as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M2_quota_family_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_pass_that_raised_keeps_what_it_had_already_paid_for`
  - `tests/intake/test_recognition.py::test_a_provider_quota_answer_is_a_spend_refusal_and_never_a_miss`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_and_neither_spend_refusal_is_a_miss`
  - `tests/intake/test_recognition.py::test_answers_that_cannot_be_kept_neither_fail_the_pass_nor_replace_its_refusal`
  - `tests/intake/test_recognition.py::test_every_status_code_lands_in_exactly_one_family[payload4-quota]`
  - `tests/intake/test_workers.py::test_a_spend_refusal_at_the_queue_is_reported_as_policy_and_queues_nothing`

Old text:

```
_QUOTA_CODES = frozenset({3003})
```

New text:

```
_QUOTA_CODES = frozenset()
```

### `u331.S08_check_verb_origin_renamed`

intake/check_cli: print the module's new place as the envelope's origin

- File: `src/cratekit/intake/check_cli.py`
- Source: `u331.json`, row `S08_check_verb_origin_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_variable_grid_on_a_row_not_marked_dyn_is_suspect_and_exits_27`

Old text:

```
_ORIGIN = ("analysis.check_cli",)
```

New text:

```
_ORIGIN = ("intake.check_cli",)
```

### `r682-a.M5_reason_counted_twice`

each row adds two to its reason, a realistic nearby coefficient

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M5_reason_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`

Old text:

```
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
```

New text:

```
                by_reason[word][why] = by_reason[word].get(why, 0) + 2
```

### `u120.L1_date_frozen_when_none`

list_favorites: a heart with no date is frozen with no key, as an older build did

- File: `src/cratekit/intake/cli.py`
- Source: `u120.json`, row `L1_date_frozen_when_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`

Old text:

```
        if key in frozen and HEARTED not in frozen[key]:
            frozen[key][HEARTED] = hearted_on(row)
```

New text:

```
        if key in frozen and HEARTED not in frozen[key] and hearted_on(row):
            frozen[key][HEARTED] = hearted_on(row)
```

### `u57-recognition-and-items.C3_missing_ref_not_refused`

A provider row without an identifier is queued rather than refused by position

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C3_missing_ref_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_listing_that_fails_refuses_and_queues_nothing[no-id-by-position]`
  - `tests/intake/test_workers.py::test_a_row_the_reader_refuses_refuses_the_playlist_and_queues_nothing[no-identifier-by-position]`

Old text:

```
        if row.origin != match.TEXT and not row.ref
```

New text:

```
        if False
```

### `r706-c.C1_parts_note_never_said`

The recognition-in-parts note is never added

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r706-c.json`, row `C1_parts_note_never_said`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
    if result.parts <= 1:
        return ()
    still = (
```

New text:

```
    if result.parts >= 1:
        return ()
    still = (
```

### `u103-b.C6_served_note`

Never say that chunks were answered from the cache

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C6_served_note`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`

Old text:

```
    if result.cached:
        notes.append(
```

New text:

```
    if False:
        notes.append(
```

### `u104-e.E4_identify_library_before_fetch`

Drop intake identify's check that the library is there to be asked, which runs before anything is fetched or sent

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-e.json`, row `E4_identify_library_before_fetch`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_identify_over_a_url_refuses_an_absent_library_before_anything_is_fetched`
  - `tests/intake/test_workers.py::test_an_absent_library_is_refused_before_the_spend_and_never_read_as_an_empty_one`

Old text:

```
    _library_or_refuse(cfg, shown)

```

New text:

```
(empty)
```

### `r924.F3_watcher_silent`

The watcher runs and never reports the bytes

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F3_watcher_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_fetch_that_raises_still_stops_the_watcher`
  - `tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`

Old text:

```
            progress(f"fetching: {megabytes(_bytes_in(directory))} so far, {elapsed}s")
```

New text:

```
            pass
```

### `u104-b.F6_clear_before_attempt`

Stop clearing the scratch folder before an attempt: reuse whatever a killed process left in it

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F6_clear_before_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`

Old text:

```
            if scratch.exists():
                shutil.rmtree(scratch)
            scratch.mkdir(parents=True)
```

New text:

```
            scratch.mkdir(parents=True, exist_ok=True)
```

### `u104-c.P5_stem_bound`

Multiply the tracklist stem bound by ten, 80 to 800, past what a file name may hold

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P5_stem_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_tracklist_stem_is_the_last_segment_reduced_to_a_safe_name[url6-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82-E3-81-82]`

Old text:

```
STEM_MAX_CHARS = 80
```

New text:

```
STEM_MAX_CHARS = 800
```

### `r301.R1_seam_falls_back_to_defaults`

The seam builds a default section when none is handed over instead of refusing

- File: `src/cratekit/intake/recognize.py`
- Source: `r301.json`, row `R1_seam_falls_back_to_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_workers.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-section]`

Old text:

```
            raise TypeError(
                "the bound identifier needs the configuration's recognition "
                "section, which names the host and the month's bound"
            )
```

New text:

```
            recognition = config.RecognitionConfig()
```

### `r675.G9_repair_plan_asks_with_no_candidates`

repair_cli plan: the repair verb's plan read hands the guard no candidates

- File: `src/cratekit/intake/repair_cli.py`
- Source: `r675.json`, row `G9_repair_plan_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`

Old text:

```
        naming_cli.referenced_keys(cfg, renaming=[path for _, path in candidates])
```

New text:

```
        naming_cli.referenced_keys(cfg, renaming=[])
```

### `u102-a.U2_bare_filename`

_unusable_why: stop requiring the proposed name to be a bare filename, so a path with a separator is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U2_bare_filename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[../escaped.flac-not a bare filename]`
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[nested/inside.flac-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if not proposed or proposed in {".", ".."}:
```

### `u102-b.G6_abort`

_apply: carry on past an abort answer

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G6_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_proposal_is_shown_asked_renamed_and_then_converges`

Old text:

```
    if option == "abort":
```

New text:

```
    if False:
```

### `u62.C1_bound_constant_true`

Answer bound() True without asking whether the adapter imports

- File: `src/cratekit/label/catalogue.py`
- Source: `u62.json`, row `C1_bound_constant_true`
- Moved: Same bound(); U298 replaced its try import with provider_session.importable, the same question, so answering True here skips it as before, local to this function
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/intake/test_workers.py`
- Collected: 503 against a baseline of 503
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_the_catalogue_seam_answers_bound_without_reading_a_credential`

Old text:

```
    return provider_session.importable(ADAPTER_MODULE)
```

New text:

```
    return True
```

### `u237.M9_year_eats_the_next_digit`

_YEAR_NUM: drop the boundary after the year, so 20211 Label reads 1 Label

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M9_year_eats_the_next_digit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[20211 Label-expected12]`

Old text:

```
_YEAR_NUM = re.compile(r"^\d{4}(?:\s+|\.?$)")
```

New text:

```
_YEAR_NUM = re.compile(r"^\d{4}\s*")
```

### `r704-a.S3_no_context_status_check`

a non JSON 429 whose status sits only in the implicit context is read as permanent

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S3_no_context_status_check`
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
        return run.LookupFailure(message, rate_limited=True)

```

New text:

```
(empty)
```

### `u237.M10_empty_sides_match`

labels_match: drop the guard on empty folds, so two names that both fold to nothing confirm each other

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M10_empty_sides_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[***----]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[\u65e5\u672c-\u041f\u043b\u0430\u0441\u0442\u0438\u043d\u043a\u0430]`

Old text:

```
    return bool(left) and bool(right) and (_words_within(left, right) or _words_within(right, left))
```

New text:

```
    return _words_within(left, right) or _words_within(right, left)
```

### `u192.F6_queue_only_never`

queue_only: always False, so --queue-only drives the job anyway

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F6_queue_only_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`, `tests/test_label_genre.py`, `tests/test_sync_land.py`
- Collected: 414 against a baseline of 414
- Kills: 21 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_an_older_build_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
  - `tests/test_analysis_workers.py::test_the_shared_tail_step_queues_only_and_drives_its_job_once`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return bool(getattr(args, "queue_only", False))
```

New text:

```
    return False
```

### `r837-a.A8_load_carries_sets`

ledger._load: the sets map is dropped on read, so every later write forgets each set playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A8_load_carries_sets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 419 against a baseline of 419
- Kills: 23 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_track_settled_twice_on_a_set_playlist_is_recorded_once`
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            for key, value in sets.items()
```

New text:

```
            for key, value in ()
```

### `r229.L19_a_copy_not_a_move`

The adopted record is copied to the new key and left under the old one, so two keys name one remote playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L19_a_copy_not_a_move`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_an_adopted_record_moves_and_no_playlist_is_created`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - `tests/test_outbound_workers.py::test_a_renamed_crate_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_two_crates_offered_one_orphan_do_not_both_get_it`

Old text:

```
    record = playlists.pop(recorded_key)
```

New text:

```
    record = dict(playlists[recorded_key])
```

### `r229.L8_a_living_legacy_record_is_freed`

A legacy record under a living path is freed with no contents to say the path was reused

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L8_a_living_legacy_record_is_freed`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_legacy_record_under_a_living_path_is_never_freed`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if key in living and _still_carries(written, living[key]):
```

### `u205.S2_account_rejection_read_as_wait`

outbound account: a rejected app credential is translated as the account's failure, a wait, never naming the app

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S2_account_rejection_read_as_wait`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 179 against a baseline of 179
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

### `u27-reports-round-2.S5b_engine_default_drift`

Drift the engine's own copy of the handler key away from the registry's

- File: `src/cratekit/modules/reports/duplicates.py`
- Source: `u27-reports-round-2.json`, row `S5b_engine_default_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/test_reports_cli.py`
- Collected: 382 against a baseline of 382
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_every_item_carries_the_handler_key_the_registry_declares`
  - `tests/modules/test_reports.py::test_the_declared_handler_key_is_the_one_the_registry_carries`
  - `tests/test_reports_cli.py::test_the_two_copies_of_the_duplicate_handler_key_cannot_drift`

Old text:

```
HANDLER_KEY = "audit.duplicates"
```

New text:

```
HANDLER_KEY = "duplicates.audit"
```

### `u27-reports-round-3-fixes.F2_depth_origin`

Measure the tree depth from the export root again rather than from the tree's own node

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-3-fixes.json`, row `F2_depth_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
    try:
        return len(path) - path.index(tree_display)
    except ValueError:  # pragma: no cover - callers filter to governed paths
        return 0
```

New text:

```
    return len(path)
```

### `r1761.P11_move_nothing_dropped`

_full_commands: a new library's mirror is not told to delete nothing, so a stray state folder archives the mirror

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P11_move_nothing_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                *(MOVE_NOTHING if move_nothing else ()),
```

New text:

```
                *(()),
```

### `r221-a.E1_outcome_forgets_the_run`

The outcome records False whatever the run was, which is the state before this unit: a rehearsal and a real run render identically

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E1_outcome_forgets_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r222-a.A6_any_destination_is_a_floor`

Take the floor from a completed mirror to ANOTHER destination, which says nothing about which folders here are finished

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A6_any_destination_is_a_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`

Old text:

```
    if fact is None or fact.destination != _destination_for(cfg, backup_facts.Portion.FILES):
        return None
```

New text:

```
    if fact is None:
        return None
```

### `r349-c.C4_argv_rendered`

outcome_payload renders the label where the argv belongs

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C4_argv_rendered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 278 against a baseline of 278
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`

Old text:

```
                        "argv": list(command.argv),
```

New text:

```
                        "argv": [command.label],
```

### `r757-a.E8_failed_mirror_reports_nothing`

run_backup: read the comparison only when the mirror returned zero

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E8_failed_mirror_reports_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if command.label == MIRROR:
```

New text:

```
            if command.label == MIRROR and result.returncode == 0:
```

### `u311.A3_database_destination_not_required`

The destination check forgets the database snapshot root, so a run without it is not refused up front

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A3_database_destination_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
    keys = ("dest", "archive_root", "db_dest_root")
```

New text:

```
    keys = ("dest", "archive_root")
```

### `u317.Q21_send_without_archive`

_quick_commands: the send loses --backup-dir, so an overwritten version is not archived

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q21_send_without_archive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    rclone, "copy", root, dest, *listed, "--backup-dir", archive,
```

New text:

```
                    rclone, "copy", root, dest, *listed,
```

### `u45-round-1.E1_rehearsal_publishes`

Let a dry run publish, so a preview records a backup age for a run that copied not one byte

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E1_rehearsal_publishes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
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
    if dry_run:
        publish = False
```

New text:

```
    pass
```

### `u48-author.P6_purge_count_not_named`

The purge message drops how many folders survived it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P6_purge_count_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
```

New text:

```
                f"the archive rotation did not finish: some dated folder(s) "
```

### `r1761.P18_census_any_root`

read_census: a census kept for another library root answers for this one

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `r1761.json`, row `P18_census_any_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if data["library_root"] != str(cfg.library.root) or data["dest"] != str(cfg.backup.dest):
```

New text:

```
        if data["dest"] != str(cfg.backup.dest):
```

### `u311.A7_unanchored_exclude_anchors`

An exclude without a leading slash is matched only at the root, not at any path's end

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u311.json`, row `A7_unanchored_exclude_anchors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 318 against a baseline of 318
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_quick_walk_reads_hashes_globs_and_names_as_rclone_does`

Old text:

```
    head = "^" if anchored else "(?:^|/)"
```

New text:

```
    head = "^"
```

### `u317.Q4_racy_file_not_hashed`

walk: a file inside the racy window is not hashed, so a rewrite keeping size and time is skipped

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q4_racy_file_not_hashed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if rel in must_hash or status.st_mtime_ns >= racy_after_ns:
```

New text:

```
            if rel in must_hash:
```

### `r154-b.B1_named_mismatch`

Accept a named snapshot carrying ANY marker, which is the finding's real half: a well formed stamp from another library is pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B1_named_mismatch`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it`
  - `tests/modules/test_tools.py::test_a_snapshot_marked_for_another_library_is_refused`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[   ]`
  - `tests/modules/test_tools.py::test_an_empty_expected_identity_never_matches_an_empty_marker[]`
  - `tests/modules/test_tools.py::test_two_identities_or_an_empty_marker_refuse_as_another_librarys`
  - `tests/modules/test_tools.py::test_two_markers_are_refused_without_offering_an_identity_to_pass`
  - `tests/test_restore_cli.py::test_another_librarys_snapshot_is_refused_at_the_verb_and_names_both_volumes`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`

Old text:

```
        if recorded == (expected,):
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

New text:

```
        if recorded:
            return ResolvedSnapshot(stamp=snapshot, recorded_volume=expected, named=True)
```

### `r338-a.B3_capture_is_a_copy`

_plan_database: capture the share with copy and not sync, so a grid rekordbox deleted stays in the mirror for ever and the mirror stops being the share

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B3_capture_is_a_copy`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r338-b.R6_switch_ignored`

_plan_restore_inside_the_gates: ignore pull_share, so the bare metal recovery asks the remote about a share it will not pull and can be refused over it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R6_switch_ignored`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_caller_that_will_not_spend_the_database_half_is_not_refused_over_the_share`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if analysis_store.is_watched(cfg, landing):
```

### `r367.G12_listing_results_are_discarded`

the listing runs and its names are thrown away, so every sidecar is treated as absent

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G12_listing_results_are_discarded`
- Moved: Anchored where u311-replay-after-a.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
```

New text:

```
    snapshot_filenames(cfg, chosen, runner=runner)
    held = frozenset()
```

### `r388-a.M2_identity_listing_message_reworded`

Reword could not be listed to could not be read in the identity listing refusal (R-387's row)

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M2_identity_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r388-b.M8_share_listing_message_reworded`

Reword could not be listed to could not be read in the share listing refusal

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M8_share_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `u44-author-round-2.B3_concat_output_unread`

Drop the same check from the join, one function over

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author-round-2.json`, row `B3_concat_output_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 246 against a baseline of 246
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_join_that_exits_zero_and_writes_nothing_refuses_rather_than_returning`

Old text:

```
    _wrote_or_refuse(destination, "join")
    return destination
```

New text:

```
    return destination
```

### `r187-b.B5_empty_walk_writes`

build_index: write the cache after an empty walk, creating a state directory inside a leftover mountpoint

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B5_empty_walk_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_empty_walk_writes_no_cache`

Old text:

```
    if files:
        _save_cache(cache_path, fresh, stamp)
```

New text:

```
    if True:
        _save_cache(cache_path, fresh, stamp)
```

### `u43-author-light.E1_anchor_is_its_own_companion`

build_pool stops excluding the anchor by match key, so the best companion for a track is itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E1_anchor_is_its_own_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
        if anchor_match and track.match == anchor_match:
            continue
```

New text:

```
        if anchor_match and track.match != anchor_match:
            pass
```

### `u281.R4_stopped_note_unmarked`

Refusals.stopped: the note loses its not sent head, so the summary counts the unsent files as sent

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R4_stopped_note_unmarked`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
                f"{NOT_SENT}{source} refused this client on its last {self.limit} "
```

New text:

```
                f"{source} refused this client on its last {self.limit} "
```

### `u956.O6_tag_set_promises_outside`

tag set _written: name no row as outside the root, so tag set promises adopt apply and adopt move for a sampler row neither touches

- File: `src/cratekit/tagging/genre_set_cli.py`
- Source: `u956.json`, row `O6_tag_set_promises_outside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_tag_set.py`, `tests/test_tag_set_move.py`
- Collected: 104 against a baseline of 104
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_tag_set_names_only_rows_whose_file_took_the_genre`
  - `tests/test_adopt_outside_root.py::test_tag_set_promises_adoption_only_for_rows_inside_the_root`
  - `tests/test_adopt_outside_root.py::test_tag_set_promises_no_adoption_when_every_written_row_is_outside`

Old text:

```
            if item.path and not adopt_scan.within_root(item.path, root)
```

New text:

```
            if False
```

### `u260.F4_binder_admits_everything`

for_images: build the shared fetch with no admission, so the shipped worker remembers undecodable bytes

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F4_binder_admits_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`

Old text:

```
        _images.append(remembering(default_image_fetch(), admit=art.decodes))
```

New text:

```
        _images.append(remembering(default_image_fetch()))
```

### `u281.S4_any_mitigation_is_a_challenge`

_refusal_note: name any Cf-Mitigated value a challenge, so a block is called a challenge

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S4_any_mitigation_is_a_challenge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_another_mitigation_is_not_called_a_challenge`

Old text:

```
    if mitigated.strip().lower() == _CF_CHALLENGE:
```

New text:

```
    if mitigated:
```

### `u260.E1_engine_encodes_per_file`

_art_embedded: call the plain encoder again, so every file encodes the same bytes

- File: `src/cratekit/tagging/tag.py`
- Source: `u260.json`, row `E1_engine_encodes_per_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 196 against a baseline of 196
- Kills: 8 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_an_albums_files_naming_one_address_make_one_request_one_wait_and_one_encode`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
        cdj = art.to_cdj_jpeg_remembered(data)
```

New text:

```
        cdj = art.to_cdj_jpeg(data)
```

### `u133-b.T5_former_display`

The former place names a playlist the library does not hold, so the move finds nothing to leave

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T5_former_display`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1038 against a baseline of 1038
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_jazz_left_the_non_electronic_folder_and_declares_the_playlist_it_left`
  - `tests/test_routing_parity.py::test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left`

Old text:

```
sub = "jazz"
display = "Jazz"

```

New text:

```
sub = "jazz"
display = "Jazz Archive"

```

### `r675.G1_every_dark_row_refuses`

_referenced: the leaf test dropped, so every dark row refuses, which is the behaviour R-675 measured at 582 rows

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G1_every_dark_row_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_another_name_lets_the_repair_run`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_only_asked_about_the_files_being_renamed`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_under_a_held_candidate_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_another_name_refuses_nothing`
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-dark-tombstone-under-another-name-R-524]`
  - `tests/test_naming_apply_cli.py::test_a_row_that_can_name_no_candidate_neither_blocks_nor_protects[a-streamed-catalogue-path]`

Old text:

```
        if (named := leaves.get(_key(Path(decoded).name)))
```

New text:

```
        if (named := leaves.get(_key(Path(decoded).name)) or [decoded])
```

### `r1991.T6_filed_untracked`

writer: never note a filed pair, so nothing is recorded

- File: `src/cratekit/write/trees.py`
- Source: `r1991.json`, row `T6_filed_untracked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_genre_favorites.py`, `tests/test_genre_retag.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_rebuild_growth.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_shared_homes.py`, `tests/test_tag_set_move.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_write_session.py`, `tests/test_xml_splice_golden.py`
- Collected: 1590 against a baseline of 1590
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`
  - `tests/test_unrecorded_genre_folder.py::test_a_second_node_a_write_made_under_the_genres_own_name_is_named_as_not_compared`
  - `tests/test_unrecorded_genre_folder.py::test_a_tree_filed_by_adoption_names_its_leftover_under_a_renamed_folder`
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_never_moves_a_destination_the_record_already_binds`
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_records_only_a_pair_it_filed_into`

Old text:

```
        self.filed.add(destination)

```

New text:

```
(empty)
```

### `u302.W16_move_removes_without_proof_of_the_target`

_proven_leavers: a track not proven in its target is removed from where it was

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W16_move_removes_without_proof_of_the_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_adopt_move.py`
- Collected: 147 against a baseline of 147
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`

Old text:

```
        if not places.holds(move.target, move.content_id):
```

New text:

```
        if False:
```

