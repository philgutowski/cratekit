# Mutation table: u332-replay-after-2

Measured by `scripts/mutate.py` on 2026-11-24 07:31 UTC, branch `HEAD` at `0c43f109`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23212 collected. pytest invocations for this batch: 285.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 07:31 UTC for commit `0c43f10986b6`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 111, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23212 against 23212. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B11_a_changed_schema_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 5 | killed |
| `u297.B8_a_changed_exit_code_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 2 | killed |
| `u122.H7_attended_beats_hold` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 2 | killed |
| `u148.C5_issue_count_dropped` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 2 | killed |
| `u148.W3_issue_whole_dropped` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 3 | killed |
| `u151.O1_owner_filter_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X5_field_count_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u203.M2_span_closer_any_follower` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u291.L1_lanes_back_to_five` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u314.L10_search_names_no_file` | `scripts/board.py` | maintainer | 1 file(s) | 7 | 2 | killed |
| `r83.D2_fetch_defect` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 2 | killed |
| `u176-c5.C5_empty_page_ends` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 92 | 1 | killed |
| `u176.C6_repeated_token` | `src/cratekit/acquire/bandcamp.py` | maintainer | 1 file(s) | 46 | 1 | killed |
| `u176.V1_auth_failed_reason` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 1066 | 5 | killed |
| `u176.V9_collision_refused` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u177.B7_tag_not_written` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 4 | killed |
| `u205.C2_token_never_reused` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 6 | killed |
| `r289-b.B1_reclaim_rmtree` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 367 | 2 | killed |
| `r290-author.S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 195 | 11 | killed |
| `r668-b.M12_home_expansion_raises` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `u42-author-round-2.C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 25 | 1 | killed |
| `u42-author.W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 229 | 2 | killed |
| `u54-acquisition-worker.G19_frozen_config` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 40 | killed |
| `u54-acquisition-worker.G9_failed_invocation` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 5 | killed |
| `u80.F14_single_option_stalls` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F8_mix_not_demoted` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80-b.C4_searcher_eager` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u81-fetch-a.W5_pre_download_exists` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.W2_scheme_half_rerun` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `r1016.M7_send_translation_dropped` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 793 | 2 | killed |
| `r878-a.A13_dedupe_shared` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 141 | 4 | killed |
| `r878-b.B10_folder_dedupe_key` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 141 | 2 | killed |
| `r887-a.K5_filter_before_count` | `src/cratekit/acquire/listing.py` | user | 3 file(s) | 204 | 3 | killed |
| `u65.C1_the_declared_total_is_ignored` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 198 | 3 | killed |
| `u65.E2_the_shape_helper_ignores_the_page_size_table` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 198 | 5 | killed |
| `u305.M4_index_library_not_reexported` | `src/cratekit/acquire/match.py` | maintainer | 3 file(s) | 709 | 301 | killed |
| `r664.E1_stem_head_kept` | `src/cratekit/acquire/match_library.py` | user | 10 file(s) | 1193 | 149 | killed |
| `u261.W5_session_fields_guard_sample` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 188 | 1 | killed |
| `r703-a.V5_escalate_when_ok` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 1 | killed |
| `r703-b.R3_mapping_positional` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 276 | 1 | killed |
| `u47-author.CODEC_none_reads_as_unreadable` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 6 | killed |
| `u47-author.R196_accept_device_flow_session` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 3 | killed |
| `u47-author.R197_event_abort_preset` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 5 | killed |
| `u254.M02_cache_identity_ignored` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 5 | killed |
| `u254.M11_unterminated_tail_whole` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 23 | killed |
| `u254.M19_already_inverted` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 33 | killed |
| `r731-b.M13_gate_without_the_review_list` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 1 | killed |
| `u165.A3_grant_first` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 100 | 1 | killed |
| `u55-collection-reader.R12_apply_item_ids` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 15 | killed |
| `u956.S18_unplaced_inside_passes` | `src/cratekit/adopt/apply_cli.py` | user | 3 file(s) | 72 | 2 | killed |
| `u55-collection-reader.R4_genre_proxy` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 56 | 22 | killed |
| `r780-a.A5_style_doubles_decided` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `u118-c.M1_declarer_settles` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 189 | 5 | killed |
| `r758-b.C1_gate_asked_before_the_acknowledgment` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r797-b.M5_the_writer_can_leave_one` | `src/cratekit/adopt/move_cli.py` | user | 3 file(s) | 172 | 2 | killed |
| `r788-c.L5_renamed_bucket_unseen` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 163 | 3 | killed |
| `r1965.R02_collision_rule` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 5 | killed |
| `r722.P8_tally_folds_unreadable` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 651 | 2 | killed |
| `r731-a.M09_digest_blind_to_the_review_list` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 3 | killed |
| `r788-a.P7_renamed_track_reads_present` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 3 | killed |
| `u340.R10_plan_no_second_entry` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 814 | 10 | killed |
| `u23-round-8-independent.A3_at_risk_drops_the_original_clause` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 2 | killed |
| `u23-round-8-independent.D1_bytes_agree_drops_the_size_gate` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 613 | 1 | killed |
| `r658-c.S4c_dataless_skip_returns` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 613 | 1 | killed |
| `r722.S3_track_drops_flag` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 4 | killed |
| `u340.R09_census_unread_raises` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 669 | 32 | killed |
| `u956.O7_prefix_not_anchored` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 639 | 3 | killed |
| `u956.O22_scan_verb_unconfined` | `src/cratekit/adopt/scan_cli.py` | user | 3 file(s) | 668 | 1 | killed |
| `u223.M21_discard_through_link` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 176 | 1 | killed |
| `u223.M6_discard_keeps_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 176 | 3 | killed |
| `u90-a.A3_range_guard_off` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 7 | killed |
| `u90-b.B5_previous_cut_not_reported` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 2 | killed |
| `u94-a.S3_partial_refusal_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 6 | killed |
| `u94-b.W4_partial_warning_dropped` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 2 | killed |
| `u94-c.N4_vocal_half_sampled` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 1 | killed |
| `u223.M11_no_fallback` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 2 | killed |
| `u241.M20_held_job_records_a_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 271 | 1 | killed |
| `u343.M02_finalize_writes_a_key` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 480 | 6 | killed |
| `u58-workers-and-wav.R2_extra_not_required` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 1 | killed |
| `u263.D11_mono_shape` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 2 | killed |
| `u263.D5_window_offset` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 1 | killed |
| `u344.M2_head_measures_uncalibrated` | `src/cratekit/analysis/detect.py` | user | 5 file(s) | 495 | 1 | killed |
| `u327.A14_plan_taken_again` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u327.A22_read_back_refuses_wrong` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u342.P11_restore_keeps_a_stamp` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 2 | killed |
| `u342.P8_a_stopped_stamp_continues` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 1 | killed |
| `u241.M22_decode_not_costed` | `src/cratekit/analysis/light.py` | user | 1 file(s) | 271 | 29 | killed |
| `u275.M8_analysis_line_scaled` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 553 | 18 | killed |
| `sitting3.G14_unchunked_floor_is_width` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 1 | killed |
| `u25-author-light.G3_unchunked_only` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 4 | killed |
| `u58-workers-and-wav.W5_terminal_decoded` | `src/cratekit/analysis/vocals.py` | maintainer | 1 file(s) | 176 | 1 | killed |
| `u92-author.G6_stat_failure_is_oversize` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 230 | 8 | killed |
| `r221-a.W2_rehearsal_said_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `r222-b.B10_archive_not_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B5_whole_payload_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 9 | killed |
| `r349-a.A2_success_produced` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 6 | killed |
| `u45-round-1.C3_nothing_ran_accepted` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 8 | killed |
| `u45-round-1.Q4_payload_key_not_read` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.W8_engine_refusal_escapes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u50-review-fixes.R2_empty_job_guard_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r924.D3_write_failure_raises` | `src/cratekit/cli/__init__.py` | user | 1 file(s) | 11 | 1 | killed |
| `r349-a.A3_job_show_field` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 89 | 4 | killed |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry_modules.py` | user | 24 file(s) | 4345 | collection error | collect-error |
| `r925.R6_count_line` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 2 | killed |
| `r338-c.C6_only_the_first_root_is_watched` | `src/cratekit/core/analysis_store.py` | user | 1 file(s) | 32 | 1 | killed |
| `u260.E5_key_digest_of_a_prefix` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u83-a.E2_quality_floor` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-a.R2_unreadable_is_not_art_error` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W4_rgb_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `r349-c.C3_unparseable_reported` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 89 | 1 | killed |
| `example-binaries-five-row.B1_broken_override_falls_through` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 17 | 1 | killed |
| `r290-author.R3_the_owner_drops_the_type` | `src/cratekit/core/cause.py` | user | 3 file(s) | 317 | 13 | killed |
| `u254.C4_append_not_append` | `src/cratekit/core/config.py` | user | 4 file(s) | 962 | 54 | killed |
| `r290-author.J4_predicate_narrowed_to_failed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 29 | killed |
| `u331.S16_item_path_reexport_joins_plainly` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 269 | 84 | killed |
| `u342.S6_stamp_reads_back_the_body` | `src/cratekit/core/naming.py` | user | 4 file(s) | 392 | 2 | killed |
| `u205.G5_app_share_unclamped` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 184 | 1 | killed |
| `r758-a.W7_removed_row_marked_again` | `src/cratekit/core/rb_nodes.py` | user | 2 file(s) | 300 | 1 | killed |
| `r731-b.M22_single_sub_does_not_compete` | `src/cratekit/core/routing.py` | maintainer | 2 file(s) | 70 | 1 | killed |
| `r722-b.T6_field_failure_swallowed` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2990 | 1 | killed |
| `u81-fetch-b.S1_strip_does_nothing` | `src/cratekit/core/tags.py` | user | 1 file(s) | 35 | 2 | killed |
| `r301.B2_bound_host_ignored` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 3 | killed |
| `r706-a.A5_run_guard_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 2 | killed |
| `r706-b.B6_grid_not_partitioned` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 5 | killed |
| `u103-a.A10_write_is_a_merge` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 3 | killed |
| `u57-recognition-and-items.M11_unreached_stop_tenfold` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 2 | killed |
| `u57-recognition-and-items.M5_empty_music_not_none` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 1 | killed |
| `r679-b.D1_intake_gate_on_question_alone` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 834 | 2 | killed |
| `r924.C1_set_identify_not_told` | `src/cratekit/intake/cli.py` | user | 3 file(s) | 119 | 4 | killed |
| `u213.M12_absent_rule` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 1 | killed |
| `u70.S2_sentinel_casefold` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 241 | 2 | killed |
| `r925.S4_write_failure_refuses` | `src/cratekit/intake/cli_identify.py` | user | 1 file(s) | 67 | 1 | killed |
| `u104-d.C2_refusal_named_for_the_address` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `r770-d.S1_composite_the_splice_takes_a_stub` | `src/cratekit/intake/collection_xml.py` | user | 4 file(s) | 85 | 2 | killed |
| `u104-a.F1_guard_string_layer` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-b.F9_scratch_prepare_is_its_own_kind` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u37-author-light.G4_staging` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 8 | 1 | killed |
| `u331.S07_check_engine_origin_renamed` | `src/cratekit/intake/rekordbox_check.py` | user | 1 file(s) | 71 | 2 | killed |
| `u102-a.P3_root_filter` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U5_linked_file` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G9_post_gate_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u237.M1_bare_letter_is_a_mark_again` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 33 | killed |
| `u177.A3_account_case` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 5 | killed |
| `r704-a.S6_status_coefficient` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `u237.M8_one_direction_only` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 1 | killed |
| `r356-b.B5_export_plan_hands_on_the_display_title` | `src/cratekit/modules/outbound/export.py` | user | 1 file(s) | 64 | 2 | killed |
| `r229.L12_the_first_of_several_is_adopted` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r229.L3_nothing_shared_is_a_match` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `u309-z.U1_settle_found_refusal` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 9 file(s) | 514 | 1 | killed |
| `u27-reports-round-1.C2_tree_anchored_at_zero` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L4_median_even` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `r154-a.A2_stamp_calendar` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 188 | 1 | killed |
| `r222-a.A1_nothing_held` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 5 | killed |
| `r222-a.A9_rehearsal_purges` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 4 | killed |
| `u45-round-2.E5_outcome_ok_widened` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 1 | killed |
| `r1761.P13_history_record_ignored` | `src/cratekit/modules/tools/backup_proof.py` | user | 5 file(s) | 406 | 77 | killed |
| `r1761.P23_probe_counts_state` | `src/cratekit/modules/tools/backup_record.py` | user | 5 file(s) | 406 | 1 | killed |
| `r154-b.B4_stated_volume_over_unmarked` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r338-a.B6_identity_interpolated_raw` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 3 | killed |
| `r338-b.R9_contained_restore_asks_about_a_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r367.G4_the_inventory_restored_flag_is_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 4 | killed |
| `r388-a.M5_root_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `u311.C1_first_loudness_block` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 247 | 1 | killed |
| `r187-a.A11_no_cutoff` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 4 | killed |
| `u266.M6_size_not_compared` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 324 | 1 | killed |
| `u281.R7_one_count_for_every_catalogue` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 3 | killed |
| `u260.F10_fetch_memory_one` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 2 | killed |
| `u260.F7_fetch_evicts_newest` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u281.W5_run_never_changes` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 4 | killed |
| `u133-b-rerun.T6_former_sub` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 1038 | 1 | killed |
| `r675.G4_could_name_empty` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 7 | killed |
| `r758-a.T3_target_not_proven` | `src/cratekit/write/trees.py` | user | 1 file(s) | 87 | 1 | killed |
| `r685-b.G1_the_guard_forgets_aliases` | `tests/test_active_taxonomy.py` | maintainer | 1 file(s) | 18 | 1 | killed |

## Row definitions

### `u297.B11_a_changed_schema_unseen`

compare_databases: compare no declarations, so a table that lost its key, a constraint or an index compares clean

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B11_a_changed_schema_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 5 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base0-changed0-said0]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base1-changed1-said1]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base2-changed2-said2]`
  - `tests/test_behaviour_compare.py::test_a_database_that_holds_the_same_rows_another_way_is_reported[base3-changed3-said3]`
  - `tests/test_behaviour_compare.py::test_a_table_in_one_dump_only_is_reported`

Old text:

```
            one.get("schema", []), other.get("schema", []), words, limit,
```

New text:

```
            [], [], words, limit,
```

### `u297.B8_a_changed_exit_code_unseen`

compare_commands: stop comparing exit codes

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B8_a_changed_exit_code_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_one_changed_exit_code_is_reported`
  - `tests/test_behaviour_compare.py::test_one_command_more_is_reported_once_and_the_rest_are_still_compared`

Old text:

```
            if one["exit"] != other["exit"]:
```

New text:

```
            if False:
```

### `u122.H7_attended_beats_hold`

Attended is checked before the hold, the order the review moved

- File: `scripts/board.py`
- Source: `u122.json`, row `H7_attended_beats_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`

Old text:

```
    if current in UNDERWAY:
```

New text:

```
    if node["attended"]:
        return "Attended"
    if current in UNDERWAY:
```

### `u148.C5_issue_count_dropped`

load_issues never checks its read against the repository's count

- File: `scripts/board.py`
- Source: `u148.json`, row `C5_issue_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options2-load_issues-returned 316 of the 317 GitHub]`
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`

Old text:

```
    short_of_count(issues, int(total) if total.isdigit() else total, "issue")
```

New text:

```
    pass
```

### `u148.W3_issue_whole_dropped`

load_issues no longer passes its read through whole

- File: `scripts/board.py`
- Source: `u148.json`, row `W3_issue_whole_dropped`
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
    whole(issues, "issue")

```

New text:

```
    pass

```

### `u151.O1_owner_filter_dropped`

a card on this project number under another owner counts as this board's

- File: `scripts/board.py`
- Source: `u151.json`, row `O1_owner_filter_dropped`
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
                    continue

```

New text:

```
                pass

```

### `u151.X5_field_count_dropped`

a project whose fields come back short is trusted

- File: `scripts/board.py`
- Source: `u151.json`, row `X5_field_count_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_read_whole_is_refused_by_name[<lambda>-Truncated-project field read returned 1 of the 101]`

Old text:

```
    short_of_count(fields["nodes"], fields.get("totalCount"), "project field")

```

New text:

```
(empty)
```

### `u203.M2_span_closer_any_follower`

_OPENING_EMPHASIS: accept a closer followed by a letter, so **Brainstorm**s reads as a brainstorm

- File: `scripts/board.py`
- Source: `u203.json`, row `M2_span_closer_any_follower`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[resume-**Brainstorm**s@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[underway-**Brainstorm**s@1]`

Old text:

```
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1(?=$|[\s.,:;?!\u2026])")
```

New text:

```
_OPENING_EMPHASIS = re.compile(r"([*_]+)(.+?)\1")
```

### `u291.L1_lanes_back_to_five`

CLOUD_LANES: put the cap back at five, the count before 2026-11-21

- File: `scripts/board.py`
- Source: `u291.json`, row `L1_lanes_back_to_five`
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
CLOUD_LANES = 5
```

### `u314.L10_search_names_no_file`

cmd_residuals: print a search hit without the file it is in

- File: `scripts/board.py`
- Source: `u314.json`, row `L10_search_names_no_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_residual_search.py`
- Collected: 7 against a baseline of 7
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_search_reads_every_archive_and_says_where_each_hit_is`
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`

Old text:

```
            print(f"R-{number}. {title}  ({path.relative_to(LEDGER.parent.parent)})")
```

New text:

```
            print(f"R-{number}. {title}")
```

### `r83.D2_fetch_defect`

R-348: acquire_one no longer asks the defect question after a failed fetch

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D2_fetch_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way`
  - `tests/test_adapter_contract.py::test_a_defect_stops_the_paced_pool_rather_than_being_retried`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - same rule as the lookup above
        raise_if_defect(exc)

```

New text:

```
    except Exception as exc:  # noqa: BLE001 - same rule as the lookup above

```

### `u176-c5.C5_empty_page_ends`

_pages: an empty page does not end the listing, so the listing walks past the end and refuses

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176-c5.json`, row `C5_empty_page_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 92 against a baseline of 92
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_an_empty_page_ends_the_listing_even_when_it_says_more_is_available`

Old text:

```
        if not items:
            return
```

New text:

```
        if not items and False:
            return
```

### `u176.C6_repeated_token`

_pages: a token already seen is followed again, so a stuck listing asks up to the page cap before it refuses

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C6_repeated_token`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_repeated_token_is_refused_at_once_not_after_every_page_allowed`

Old text:

```
        if not token or token in seen:
```

New text:

```
        if not token:
```

### `u176.V1_auth_failed_reason`

_auth_failed: a missing or refused session is credential-missing, a precondition, rather than auth-failed

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V1_auth_failed_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`, `tests/test_cli_contract.py`
- Collected: 1066 against a baseline of 1066
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues`
  - `tests/test_bandcamp_cli.py::test_an_expired_session_is_auth_failed_naming_the_login_step`
  - `tests/test_bandcamp_cli.py::test_no_recorded_session_is_auth_failed_before_any_request`
  - `tests/test_bandcamp_cli.py::test_what_went_wrong_since_the_queue_parks_the_resumed_job[a-listing-the-session-is-refused-at]`
  - `tests/test_bandcamp_cli.py::test_what_went_wrong_since_the_queue_parks_the_resumed_job[a-session-removed-since-the-queue]`

Old text:

```
        "auth-failed",
        f"{message}, so the account's purchases could not be read",
```

New text:

```
        "credential-missing",
        f"{message}, so the account's purchases could not be read",
```

### `u176.V9_collision_refused`

handle_fetch: a name already in the batch is overwritten rather than refused

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V9_collision_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_name_already_in_the_batch_refuses_that_file_alone`
  - `tests/test_bandcamp_cli.py::test_a_refused_copy_is_kept_and_named_never_deleted`

Old text:

```
        if final.exists():
            if final.is_file()
```

New text:

```
        if False:
            if final.is_file()
```

### `u177.B7_tag_not_written`

handle_fetch: skip the label write, so a registered seller's files stage untagged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B7_tag_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 4 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`

Old text:

```
        if label and not tags.write_tags(path, {"label": label}):

```

New text:

```
        if False:

```

### `u205.C2_token_never_reused`

app client: a token is asked for before every read, doubling the app's calls

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C2_token_never_reused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 6 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_asked_again_only_as_its_life_runs_out[a-flag-is-no-lifetime-of-one-second]`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_asked_again_only_as_its_life_runs_out[no-readable-lifetime-serves-one-margin]`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_asked_again_only_as_its_life_runs_out[reused-until-it-nears-expiry]`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_asked_again_only_as_its_life_runs_out[short-lived-30]`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_asked_again_only_as_its_life_runs_out[short-lived-60]`

Old text:

```
        if self._token is not None and now < self._expires_at:
```

New text:

```
        if False:
```

### `r289-b.B1_reclaim_rmtree`

Reclaim with rmtree, so a refused landing kept as evidence is deleted

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B1_reclaim_rmtree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 367 against a baseline of 367
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_refused_landing_left_as_evidence_survives_the_sweep`
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
        shutil.rmtree(directory)
    except OSError:
        return
    removed.append(directory)
```

### `r290-author.S02_acquire_download_call_removed`

Remove the one jobs.raise_for_state call from acquire/cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/acquire/cli.py`
- Source: `r290-author.json`, row `S02_acquire_download_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_acquire_workers.py`
- Collected: 195 against a baseline of 195
- Kills: 11 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[acquire.download]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[acquire.download]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r668-b.M12_home_expansion_raises`

a named list under a home directory that cannot be expanded raises instead of being compared as typed

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M12_home_expansion_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_list_under_a_home_that_cannot_be_expanded_is_refused_by_name`

Old text:

```
    except RuntimeError:
        given = Path(named).absolute()
```

New text:

```
    except RuntimeError:
        raise
```

### `u42-author-round-2.C2_unknown_defaults_lossless`

Classify an unrecognised suffix as lossless instead of 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author-round-2.json`, row `C2_unknown_defaults_lossless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_the_audit_reports_each_file_by_its_kind_under_each_policy[non-audio-files-are-not-reported]`

Old text:

```
    return "other"
```

New text:

```
    return "lossless"
```

### `u42-author.W2_unreadable_reported`

Collect the unreadable directories and then never report them

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W2_unreadable_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    found += [_item(path, root, "path-unreadable") for path in unreadable]
```

New text:

```
(empty)
```

### `u54-acquisition-worker.G19_frozen_config`

Build the adapter settings from a fresh load rather than the configuration the job was frozen against

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G19_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 40 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
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
  - ... and 25 more, see the JSON sidecar

Old text:

```
    settings = AdapterSettings.from_config(cfg)
```

New text:

```
    settings = AdapterSettings.from_config(_load())
```

### `u54-acquisition-worker.G9_failed_invocation`

Ignore an invocation the adapter could not run at all

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G9_failed_invocation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
    if invocation.outcome in FAILED_INVOCATIONS:
```

New text:

```
    if False:
```

### `u80.F14_single_option_stalls`

An acceptance over one option without naming it stalls instead of choosing it

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F14_single_option_stalls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_acceptance_settles_on_an_upload_only_when_it_names_one[over-one-option-is-that-option]`

Old text:

```
    if chosen is None and count == 1:
```

New text:

```
    if chosen is None and count == 0:
```

### `u80.F8_mix_not_demoted`

A long mix is no longer demoted below the track it names

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F8_mix_not_demoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_long_mix_is_demoted_below_the_track_it_names`

Old text:

```
        said *= MIX_FACTOR
```

New text:

```
        said *= 1.0
```

### `u80-b.C4_searcher_eager`

The searcher is built before any row needs a search, so a settled list needs yt-dlp

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80-b.json`, row `C4_searcher_eager`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_broken_override_is_its_own_refusal`
  - `tests/test_acquire_fallback.py::test_a_list_whose_rows_are_all_settled_needs_no_binary`
  - `tests/test_acquire_fallback.py::test_a_missing_binary_refuses_with_the_install_hint`

Old text:

```
            found: fallback.FallbackSearcher | None = None
```

New text:

```
            try:
                found: fallback.FallbackSearcher | None = searcher()
            except binaries.BinaryNotFound as exc:
                raise _binary_refusal(exc, subject) from exc
```

### `u81-fetch-a.W5_pre_download_exists`

The name already taken is no longer checked before the download, so one is spent on it

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W5_pre_download_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_existing_output_is_refused_without_a_download`

Old text:

```
    if expected.exists():
        raise _exists(expected, detail)
```

New text:

```
    if False:
        raise _exists(expected, detail)
```

### `u81-fetch-b.W2_scheme_half_rerun`

Re-run of W2: the web address check keeps only its host half

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `W2_scheme_half_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool[file://localhost/etc/hosts]`
  - `tests/test_acquire_fallback_fetch.py::test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool[ftp://uploads.example/track.mp3]`

Old text:

```
    if where.scheme not in ("http", "https") or not where.netloc:
```

New text:

```
    if not where.netloc:
```

### `r1016.M7_send_translation_dropped`

_send no longer translates a rejected signature, so a client whose request moved is retried through the whole ladder as a raw TypeError

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M7_send_translation_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 793 against a baseline of 793
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_client_whose_request_rejects_the_arguments_refuses_by_name_unslept`
  - `tests/test_adapter_listing.py::test_an_account_request_that_rejects_the_arguments_refuses_by_name_unslept`

Old text:

```
    try:
        return request.request(*args, **kwargs)
    except TypeError as exc:
```

New text:

```
    try:
        return request.request(*args, **kwargs)
    except KeyboardInterrupt as exc:
```

### `r878-a.A13_dedupe_shared`

_take: never skip an identifier already taken, in both walks

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A13_dedupe_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_cursor_that_never_changes_spends_the_budget_and_refuses`
  - `tests/test_adapter_listing.py::test_a_favourite_repeated_across_a_page_boundary_is_returned_once`
  - `tests/test_adapter_listing.py::test_a_folder_served_on_two_pages_is_returned_once`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`

Old text:

```
        if identity in seen:
            return
```

New text:

```
        if False:
            return
```

### `r878-b.B10_folder_dedupe_key`

account_folders: no dedupe key, so a folder served on two windows is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B10_folder_dedupe_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_cursor_that_never_changes_spends_the_budget_and_refuses`
  - `tests/test_adapter_listing.py::test_a_folder_served_on_two_pages_is_returned_once`

Old text:

```
    kwargs.setdefault("key", lambda folder: str(getattr(folder, "id", "")))
```

New text:

```
    kwargs.setdefault("key", None)
```

### `r887-a.K5_filter_before_count`

paginate_cursor: skip a raw item before counting it, so kept items alone are counted

- File: `src/cratekit/acquire/listing.py`
- Source: `r887-a.json`, row `K5_filter_before_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 204 against a baseline of 204
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_folder_holding_a_folder_keeps_only_its_playlists`
  - `tests/test_adapter_listing.py::test_a_short_walk_over_a_mixed_root_still_refuses`
  - `tests/test_adapter_listing.py::test_the_root_count_covers_playlists_too_so_folders_are_kept_after_counting`

Old text:

```
            identity = _raw_identity(raw)
            if identity is None:
```

New text:

```
            if keep is not None and not keep(raw):
                continue
            identity = _raw_identity(raw)
            if identity is None:
```

### `u65.C1_the_declared_total_is_ignored`

the total is read and then never consulted, so every walk falls back to a page shape

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C1_the_declared_total_is_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`

Old text:

```
        if total is not None:
```

New text:

```
        if False and total is not None:
```

### `u65.E2_the_shape_helper_ignores_the_page_size_table`

one shared page size, so account playlists is paged at the wrong window width

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E2_the_shape_helper_ignores_the_page_size_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_adapter_listing.py::test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset`

Old text:

```
        "page_size": PAGE_SIZES[name],
```

New text:

```
        "page_size": 100,
```

### `u305.M4_index_library_not_reexported`

match: stop re-exporting index_library, so every caller of match.index_library and the intake suite's patch of it lose their target

- File: `src/cratekit/acquire/match.py`
- Source: `u305.json`, row `M4_index_library_not_reexported`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_library_reads_remembered.py`, `tests/intake/test_workers.py`
- Collected: 709 against a baseline of 709
- Kills: 301 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_answers_that_could_not_be_kept_are_said_on_both_verbs`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_reports_the_coverage_rule_and_a_gap_is_paid_for_again_and_nothing_else_is`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - ... and 286 more, see the JSON sidecar

Old text:

```
    index_library,

```

New text:

```
(empty)
```

### `r664.E1_stem_head_kept`

Stop stripping the head from the stem, the filename half of the same rule

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E1_stem_head_kept`
- Moved: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1193 against a baseline of 1193
- Kills: 149 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - ... and 134 more, see the JSON sidecar

Old text:

```
    body = naming.strip_heads(stem, template=template)

```

New text:

```
    body = stem

```

### `u261.W5_session_fields_guard_sample`

write_back (existing guard, sampled): accept a blob carrying no session field, so a file that is not a session replaces the stored one

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W5_session_fields_guard_sample`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`
- Collected: 188 against a baseline of 188
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

### `r703-a.V5_escalate_when_ok`

the escalation is asked on a landed item too, so an error the tool survived could abort a good download

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V5_escalate_when_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_an_error_the_tool_survived_does_not_fail_a_landed_item`

Old text:

```
        if not ok and isinstance(cause, BaseException):
```

New text:

```
        if isinstance(cause, BaseException):
```

### `r703-b.R3_mapping_positional`

a single mapping argument is formatted positionally, not by name

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `R3_mapping_positional`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_mapping_argument_renders_the_way_logging_would`

Old text:

```
        values = rest[0] if len(rest) == 1 and isinstance(rest[0], Mapping) else tuple(rest)
```

New text:

```
        values = tuple(rest)
```

### `u47-author.CODEC_none_reads_as_unreadable`

Treat a None codec as unreadable rather than as container-decided, which refuses every genuine FLAC because mutagen exposes info.codec on MP4 alone

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_none_reads_as_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_real_flac_is_accepted_even_though_mutagen_reports_no_codec`
  - `tests/test_adapter_contract.py::test_an_error_the_tool_survived_does_not_fail_a_landed_item`
  - `tests/test_adapter_contract.py::test_the_classifier_reads_mutagens_container_and_not_the_file_extension`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_progress_pair_is_disabled_so_no_rendering_reaches_a_stream`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
    known = LOSSLESS_BY_CONTAINER.get(container)
    if known is None:
        return container, None
    return container, known
```

New text:

```
    return container, None
```

### `u47-author.R196_accept_device_flow_session`

Stop refusing a stored device-flow session, so the product silently downloads lossy audio with it

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_accept_device_flow_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_device_flow_session_is_refused_with_a_remedy_that_has_a_procedure`
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored1-True-True]`
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored2-True-True]`

Old text:

```
    if not bool(getattr(stored, "is_pkce", False)):
```

New text:

```
    if False:
```

### `u47-author.R197_event_abort_preset`

Pass event_abort already set, which makes item() return (False, '') before it looks at anything

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_event_abort_preset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`
  - `tests/test_adapter_contract.py::test_a_rate_limited_album_read_reaches_the_item_cause_by_name`
  - `tests/test_adapter_contract.py::test_a_session_the_tool_saw_rejected_is_an_invocation_auth_failure`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
    return Event(), event_run
```

New text:

```
    aborted = Event()
    aborted.set()
    return aborted, event_run
```

### `u254.M02_cache_identity_ignored`

mark_applied: append whenever this process has marked the path before, whatever happened to the file since

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M02_cache_identity_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_record_another_process_left_is_cut_before_the_next_append`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`

Old text:

```
        if known is not None and known == _as_left(path):
```

New text:

```
        if known is not None:
```

### `u254.M11_unterminated_tail_whole`

_read_journal: call a journal with an unterminated last line appendable

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M11_unterminated_tail_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 23 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_record_another_process_left_is_cut_before_the_next_append`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[two torn lines at the end]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[one-4]`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    whole = not tail
```

New text:

```
    whole = True
```

### `u254.M19_already_inverted`

apply_plan: report as already applied the entries the ledger does not hold

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M19_already_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 33 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-3]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id in done
```

New text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id not in done
```

### `r731-b.M13_gate_without_the_review_list`

the gate's facts no longer carry the list of withheld entries

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r731-b.json`, row `M13_gate_without_the_review_list`
- Moved: the gate's facts are now read through the _FACTS key list; dropping held_elsewhere from it is the same omission
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    "withheld_by_placement",
    "held_elsewhere",

```

New text:

```
    "withheld_by_placement",

```

### `u165.A3_grant_first`

file_plan: mint no approval before the memberships are written

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A3_grant_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`

Old text:

```
    grant(plan, actor=actor)

    membership = _write_memberships
```

New text:

```
    membership = _write_memberships
```

### `u55-collection-reader.R12_apply_item_ids`

The apply enqueues with no items at all

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R12_apply_item_ids`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 15 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`
  - `tests/test_adopt_workers.py::test_an_uncalibrated_library_files_no_vocal_sub_from_its_tags`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[None]`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[no-such-root]`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`

Old text:

```
            item_ids=(plan.digest(),),
```

New text:

```
            item_ids=(),
```

### `u956.S18_unplaced_inside_passes`

existing, _refuse_unplaced: never refuse, so a row inside the root with two live rows is marked adopted and the pass is not all or nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u956.json`, row `S18_unplaced_inside_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_apply_cli.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_a_row_inside_the_root_that_cannot_be_placed_still_fails_the_pass`
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`

Old text:

```
    if not membership.skipped:
        return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
```

New text:

```
    return
    unplaced = sorted({str(match.requested) for match in membership.skipped})
```

### `u55-collection-reader.R4_genre_proxy`

Read the raw GenreID rather than the binding's own display proxy

- File: `src/cratekit/adopt/collection.py`
- Source: `u55-collection-reader.json`, row `R4_genre_proxy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 56 against a baseline of 56
- Kills: 22 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`
  - `tests/test_adopt_workers.py::test_an_apply_whose_entries_failed_raises_rather_than_reporting_success`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    return str(getattr(row, "GenreName", "") or "")
```

New text:

```
    return str(getattr(row, "GenreID", "") or "")
```

### `r780-a.A5_style_doubles_decided`

the tree path decides in style buckets too, by the genre's resolver answer, which the brief puts out of scope; the one predicate the selection, the decision and the doubled listing share

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A5_style_doubles_decided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_what_the_tree_path_never_asks_about`

Old text:

```
    return kind is routing.Competing.BAND

```

New text:

```
    return True

```

### `u118-c.M1_declarer_settles`

The declaring bucket's tree path decides on split places, so R&B tracks in two R&B bands are listed under Soul

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M1_declarer_settles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`
- Collected: 189 against a baseline of 189
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_held_twice_is_not_listed_beside_the_move_that_leaves_it`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_split_place.py::test_a_track_in_two_r_and_b_bands_whose_genre_names_neither_is_not_listed_under_soul[another-folder]`
  - `tests/test_adopt_split_place.py::test_a_track_in_two_r_and_b_bands_whose_genre_names_neither_is_not_listed_under_soul[no-genre]`
  - `tests/test_adopt_split_place.py::test_an_r_and_b_track_in_two_r_and_b_bands_is_still_r_and_bs_to_settle`

Old text:

```
        if declarer == bucket:
            settled.add(place.id)
```

New text:

```
        if declarer == bucket:
            pass
```

### `r758-b.C1_gate_asked_before_the_acknowledgment`

the verb asks its gate without reading the backup acknowledgment first

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C1_gate_asked_before_the_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).

```

### `r797-b.M5_the_writer_can_leave_one`

membership_moves: resolve a place left through destination, which knows no former place, so every move out of the old playlist refuses

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r797-b.json`, row `M5_the_writer_can_leave_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`

Old text:

```
                placements.named_place(declared, move.bucket, sub) for sub in move.remove
```

New text:

```
                destination(declared, move.bucket, sub) for sub in move.remove
```

### `r788-c.L5_renamed_bucket_unseen`

vocals_from: no bucket is named as having its vocal sub under another name only

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L5_renamed_bucket_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_renamed_vocal_playlist_is_found_through_its_recorded_node_and_says_so`
  - `tests/test_adopt_vocals.py::test_an_empty_renamed_vocal_playlist_still_names_its_bucket`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
        if answering and not by_display.get(names):
            renamed.add(bucket.id)
```

New text:

```
        if False:
            renamed.add(bucket.id)
```

### `r1965.R02_collision_rule`

derived_classes: drop the rule that a class whose name a bucket's own place takes is not that bucket's

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R02_collision_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_bucket_declaring_a_sub_of_the_vocal_identifier_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_that_has_no_vocal_sub_is_not_read_for_one`
  - `tests/test_adopt_vocals.py::test_a_bucket_whose_band_is_labelled_with_the_vocal_name_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_whose_own_sub_carries_the_vocal_name_has_no_vocal_sub`
  - `tests/test_adopt_vocals.py::test_a_bucket_with_no_vocal_sub_plans_nothing_for_its_tagged_tracks`

Old text:

```
        if entry.id not in ids and entry.display not in displays:
            found.append(entry.id)
```

New text:

```
        if True:
            found.append(entry.id)
```

### `r722.P8_tally_folds_unreadable`

The tally counts an unreadable file as absent

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P8_tally_folds_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 651 against a baseline of 651
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`

Old text:

```
            if entry.energy_unreadable:
                readings["unreadable"] += 1
            elif entry.energy is None:
```

New text:

```
            if entry.energy is None:
```

### `r731-a.M09_digest_blind_to_the_review_list`

the digest no longer covers the rows of the review list

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M09_digest_blind_to_the_review_list`
- Moved: the digest's review list comprehension was joined onto one line by the formatter; it is emptied as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_the_digest_covers_every_field_the_review_list_shows`
  - `tests/test_adopt_placements.py::test_the_digest_moves_when_a_withheld_track_is_moved_to_another_band`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
                    {"id": entry.entry_id, **review_row(entry)} for entry in self.held_elsewhere()
```

New text:

```
                    {"id": entry.entry_id, **review_row(entry)} for entry in ()
```

### `r788-a.P7_renamed_track_reads_present`

vocal_place: a track in the sub under another name only reads present, so it joins the digest as a membership the writer may be handed

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P7_renamed_track_reads_present`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_track_in_the_sub_under_another_name_only_is_not_added`
  - `tests/test_adopt_vocals.py::test_a_track_whose_bucket_has_its_vocal_sub_under_another_name_only_is_not_added`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if vocals.sits_unnamed(bucket, content_id):
        return VOCAL_RENAMED, sub
```

New text:

```
    if False:
        return VOCAL_RENAMED, sub
```

### `u340.R10_plan_no_second_entry`

build_adoption_plan: drop the second entry, so adoption never files the second folder

- File: `src/cratekit/adopt/plan.py`
- Source: `u340.json`, row `R10_plan_no_second_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 814 against a baseline of 814
- Kills: 10 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[rnb]`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[rnb-soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[soul-rnb]`
  - `tests/test_second_genre.py::test_a_track_in_its_second_folder_is_no_stranger_there`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[rnb-soul]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[soul-rnb]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_the_track_in_both_folders`
  - `tests/test_second_genre.py::test_the_plan_gives_a_second_entry_and_counts_the_track_once`
  - `tests/test_second_genre.py::test_the_worker_checks_a_move_against_the_entry_that_planned_it`

Old text:

```
        if second_sub:
            entry = replace(unplaced, genre=track.second_genre, second=True)
```

New text:

```
        if second_sub and False:
            entry = replace(unplaced, genre=track.second_genre, second=True)
```

### `u23-round-8-independent.A3_at_risk_drops_the_original_clause`

A field holding this record's own original is no longer accounted for

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A3_at_risk_drops_the_original_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`

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
    return held in ((record.written,), (written,))

```

### `u23-round-8-independent.D1_bytes_agree_drops_the_size_gate`

The size shortcut round 8 restored is removed again

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `D1_bytes_agree_drops_the_size_gate`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
        return False

```

New text:

```
(empty)
```

### `r658-c.S4c_dataless_skip_returns`

Composite for S4, run as its own table: put back a skip that refuses to read a dataless file, which only the scoped evicted stat can reach

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `r658-c.json`, row `S4c_dataless_skip_returns`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_cloud_EVICTED_file_IS_read_because_the_restore_fetches_it_anyway`

Old text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    try:
        found = digest_of(target)

```

New text:

```
    if recorded_size is not None and info.st_size != recorded_size:
        return _Looked(ByteRead.A_DIFFERENT_SIZE)
    if getattr(info, "st_flags", 0) & 0x40000000:
        return _Looked(ByteRead.UNREADABLE)
    try:
        found = digest_of(target)

```

### `r722.S3_track_drops_flag`

The scanned track does not carry the unreadable flag

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S3_track_drops_flag`
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
            energy=energy,
            energy_unreadable=unreadable,
```

New text:

```
            energy=energy,
```

### `u340.R09_census_unread_raises`

_second_of: let an unreadable file's failure end the census walk

- File: `src/cratekit/adopt/scan.py`
- Source: `u340.json`, row `R09_census_unread_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`
- Collected: 669 against a baseline of 669
- Kills: 32 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_collision_is_addressed_by_the_node_and_survives_a_rename`
  - `tests/test_adoption.py::test_a_container_this_build_cannot_write_costs_one_entry_not_the_run`
  - `tests/test_adoption.py::test_a_declared_folder_that_already_exists_is_surfaced`
  - `tests/test_adoption.py::test_a_failed_write_leaves_the_entry_outstanding`
  - `tests/test_adoption.py::test_a_folder_holding_only_what_the_plan_names_is_not_a_collision`
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_plan_applied_thirty_percent_through_resumes_from_item_thirty_one`
  - `tests/test_adoption.py::test_a_recorded_answer_that_is_not_an_approval_applies_nothing`
  - `tests/test_adoption.py::test_a_recorded_location_handed_over_as_a_Path_still_resolves`
  - `tests/test_adoption.py::test_a_row_recorded_THE_WAY_REKORDBOX_RECORDS_ONE_is_adoptable[empty-authority]`
  - `tests/test_adoption.py::test_a_row_recorded_THE_WAY_REKORDBOX_RECORDS_ONE_is_adoptable[localhost]`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_a_second_run_over_a_finished_plan_writes_nothing`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`
  - `tests/test_adoption.py::test_an_approval_for_a_different_plan_is_refused`
  - ... and 17 more, see the JSON sidecar

Old text:

```
        return (reader(path) or "").strip()
    except (tags.TagReadFailed, OSError):
        return ""
```

New text:

```
        return (reader(path) or "").strip()
    except OSError:
        return ""
```

### `u956.O7_prefix_not_anchored`

within_root: match the root as a bare text prefix, so a sibling folder sharing the root's name reads inside it

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O7_prefix_not_anchored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 639 against a baseline of 639
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_a_row_mapped_outside_the_root_is_excluded_and_keeps_its_path`
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/vol/libArchive/a.flac-/vol/lib-False]`
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/vol/library/a.flac-/vol/lib-False]`

Old text:

```
    if wanted == anchor or wanted.startswith(anchor + "/"):
```

New text:

```
    if wanted == anchor or wanted.startswith(anchor):
```

### `u956.O22_scan_verb_unconfined`

adopt scan: census without confining to the root, so the scan counts a sampler row readable and routed that adopt apply excludes

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u956.json`, row `O22_scan_verb_unconfined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`
- Collected: 668 against a baseline of 668
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_adopt_scan_counts_each_sampler_row_outside_the_root`

Old text:

```
        [row], declared, root=cfg.library.root, prefix_map=collection.prefix_rules(cfg)
    )
```

New text:

```
        [row], declared, root=cfg.library.root, prefix_map=collection.prefix_rules(cfg),
        confine_to_root=False,
    )
```

### `u223.M21_discard_through_link`

discard_rename_evidence: reach through a linked staging directory

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M21_discard_through_link`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_discard_never_reaches_through_a_linked_staging_directory`

Old text:

```
    if directory.is_symlink() or not directory.is_dir():
        # NOT THROUGH A LINK
```

New text:

```
    if not directory.exists():
        # NOT THROUGH A LINK
```

### `u223.M6_discard_keeps_intent`

discard_rename_evidence: drop the report only, keeping the intent

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M6_discard_keeps_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (_report_name(item.ordinal),):
```

### `u90-a.A3_range_guard_off`

The whole range guard switched off, so any float is written as the cut

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A3_range_guard_off`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[nan]`
  - `tests/test_analysis_workers.py::test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if False:
```

### `u90-b.B5_previous_cut_not_reported`

The summary reports no previous cut whatever was on record

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B5_previous_cut_not_reported`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
"previous_vocal_cut": previous}
```

New text:

```
"previous_vocal_cut": None}
```

### `u94-a.S3_partial_refusal_dropped`

analyze_calibrate: never refuse a walk known to be partial before it is made, which is R-409 itself: one genre folder fits and writes

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S3_partial_refusal_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_recursive_walk_of_one_genre_is_still_one_genre`
  - `tests/test_analysis_workers.py::test_a_refusal_known_before_the_walk_does_not_make_the_walk`
  - `tests/test_analysis_workers.py::test_a_single_genre_folder_without_the_flag_writes_nothing_and_says_why`
  - `tests/test_analysis_workers.py::test_the_root_read_one_level_deep_is_partial_and_names_the_flag`
  - `tests/test_analysis_workers.py::test_the_root_with_no_loose_tracks_and_no_flag_is_told_about_the_flag`
  - `tests/test_analysis_workers.py::test_the_wrong_folder_is_said_before_the_missing_extra`

Old text:

```
    if partial is not None and not accepted:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

```

New text:

```
    if False:
        return _calibrate_refusal(ctx, _partial_refused(partial), summary)

```

### `u94-b.W4_partial_warning_dropped`

analyze_calibrate: never put calibration-partial-sample on the envelope

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W4_partial_warning_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`
  - `tests/test_analysis_workers.py::test_accept_partial_writes_and_warns`

Old text:

```
if partial is not None and wrote else ())
```

New text:

```
if False else ())
```

### `u94-c.N4_vocal_half_sampled`

analyze_calibrate: hand the vocal half the sample instead of every file under the walk

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N4_vocal_half_sampled`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample`

Old text:

```
        _calibrate_vocals(cfg, folder, paths, left_out),
```

New text:

```
        _calibrate_vocals(cfg, folder, sampled, left_out),
```

### `u223.M11_no_fallback`

_finalized_twin: no staged report fallback when the intent is gone

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M11_no_fallback`
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
    if target is None:
        target = _staged_twin(cfg, job, item)
```

New text:

```
(empty)
```

### `u241.M20_held_job_records_a_pool`

_heads_ahead: a call that drove nothing, because another driver holds the job, records a pool anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M20_held_job_records_a_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_job_another_driver_holds_records_no_pool_and_adds_none_to_the_refusal`

Old text:

```
        drove = False
        raise

```

New text:

```
        raise

```

### `u343.M02_finalize_writes_a_key`

_finalize: write a detector's camelot as initialkey, the key the run no longer measures

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M02_finalize_writes_a_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_restamp_scored_by.py`, `tests/test_analysis_ahead.py`
- Collected: 480 against a baseline of 480
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[a-title-kept]`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-lossy-marked-first]`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-the-stem]`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
        "drift": scored.get("drift_verdict"),
        run.MARK_FIELD: run.MARK_VALUE,
```

New text:

```
        "drift": scored.get("drift_verdict"),
        "initialkey": scored.get("camelot"),
        run.MARK_FIELD: run.MARK_VALUE,
```

### `u58-workers-and-wav.R2_extra_not_required`

Drop the missing extra refusal in the run worker

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R2_extra_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
    _require_heavy(_fake_detect_bound(), "analysing a track")

```

New text:

```
(empty)
```

### `u263.D11_mono_shape`

_ffmpeg_samples: keep a mono file two dimensional

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D11_mono_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_lossless_m4a_decodes_to_the_pcm_it_was_made_from[1]`
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_taken_even_when_another_is_the_default`

Old text:

```
    if channels == 1:
        native = native[0]
```

New text:

```
(empty)
```

### `u263.D5_window_offset`

_window: ignore the offset, so the slice starts at the top of the track

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D5_window_offset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_file_only_ffmpeg_reads_is_decoded_once_and_its_centre_cut`

Old text:

```
    start = int(offset * native_rate) if offset > 0 else 0
```

New text:

```
    start = 0
```

### `u344.M2_head_measures_uncalibrated`

energy_from_path: drop the no calibration answer, so an uncalibrated head measures and raises

- File: `src/cratekit/analysis/detect.py`
- Source: `u344.json`, row `M2_head_measures_uncalibrated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_warm.py`, `tests/test_energy_one_measure_librosa.py`, `tests/test_analysis_ahead.py`
- Collected: 495 against a baseline of 495
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_detector_names_why_energy_is_what_it_is`

Old text:

```
    if calibration is None:
        return None, energy.STATUS_UNCALIBRATED
    features = energy.measure(Path(path))
```

New text:

```
    features = energy.measure(Path(path))
```

### `u327.A14_plan_taken_again`

assert_plan_unchanged: never refuse, so a plan that moved after the gate is written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A14_plan_taken_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_plan_that_moves_on_the_write_handle_refuses_before_any_file`

Old text:

```
    if again.digest == approved.digest:
        return
```

New text:

```
    if True:
        return
```

### `u327.A22_read_back_refuses_wrong`

assert_read_back: refuse only a moved column, so a title that does not read back ends ok

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A22_read_back_refuses_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_read_back_wrong_or_moved_refuses_naming_the_session_that_undoes_it`

Old text:

```
    elif written.wrong:
```

New text:

```
    elif False:
```

### `u342.P11_restore_keeps_a_stamp`

apply_adopt: keep only the corrected rows' surfaces in the record, so a restore leaves a stamped file's title tag

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P11_restore_keeps_a_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes]
```

New text:

```
        gates.record.detail[RECORD_KEY] = [item.before() for item in writes if item.action == ADOPT]
```

### `u342.P8_a_stopped_stamp_continues`

_tag_after: refuse a tag already carrying the stamped title, so a run stopped after the files is never continued

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P8_a_stopped_stamp_continues`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`

Old text:

```
        return new_title if tag_title in (title, new_title) else None
```

New text:

```
        return new_title if tag_title in (title,) else None
```

### `u241.M22_decode_not_costed`

light.worker_bytes: the decode's line is dropped, so a 192 kilohertz file is declared at its length alone, 1310 MB where 2180 was measured

- File: `src/cratekit/analysis/light.py`
- Source: `u241.json`, row `M22_decode_not_costed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
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

### `u275.M8_analysis_line_scaled`

worker_bytes: the analysis line at three quarters of the declared slope, a coefficient mutation

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M8_analysis_line_scaled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 553 against a baseline of 553
- Kills: 18 (killed)
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
  - ... and 3 more, see the JSON sidecar

Old text:

```
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND)
```

New text:

```
    analysis = int(seconds * LIGHT_BYTES_PER_SECOND * 3 // 4)
```

### `sitting3.G14_unchunked_floor_is_width`

Let the unchunked path's floor collapse to the signal's own width

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G14_unchunked_floor_is_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    floor = MIN_CHUNK_SAMPLES if chunk_samples is None else min(MIN_CHUNK_SAMPLES, chunk_samples)

```

New text:

```
    floor = min(MIN_CHUNK_SAMPLES, chunk_samples or width)

```

### `u25-author-light.G3_unchunked_only`

Ignore chunk_samples and always run one whole-track pass

- File: `src/cratekit/analysis/vocal.py`
- Source: `u25-author-light.json`, row `G3_unchunked_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces[a-short-tail-is-folded]`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces[an-exact-multiple-is-equal-pieces]`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces[walks-the-signal-in-pieces]`

Old text:

```
    if chunk_samples is None or width <= chunk_samples:
        slices = [batch]
    else:
        slices = [
            batch[:, start : start + chunk_samples]
            for start in range(0, width, chunk_samples)
        ]

```

New text:

```
    slices = [batch]

```

### `u58-workers-and-wav.W5_terminal_decoded`

Decode a track whose head was terminal anyway

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W5_terminal_decoded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_terminal_head_is_not_decoded_at_all`

Old text:

```
    if result.get("terminal") is not None:
        return _inactive(result, REASON_HEAD_TERMINAL)

```

New text:

```
(empty)
```

### `u92-author.G6_stat_failure_is_oversize`

A size that cannot be read answers oversize, so a missing file names the wrong remedy

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G6_stat_failure_is_oversize`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 230 against a baseline of 230
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_analyse_scores_the_singing_columns_not_the_first_three`
  - `tests/test_analysis_workers.py::test_a_decode_that_fails_is_reported_as_inactive_and_never_as_zero`
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_model_whose_inference_raises_is_a_named_absence_with_the_head_intact`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_a_size_that_cannot_be_read_is_not_oversize_and_the_decode_path_reports`
  - `tests/test_analysis_workers.py::test_the_decoder_receives_the_partials_path`

Old text:

```
    except (OSError, TypeError, ValueError):
        return False

```

New text:

```
    except (OSError, TypeError, ValueError):
        return True

```

### `r221-a.W2_rehearsal_said_unconditionally`

Every run is told it copied nothing, including the real one that copied and published, which is the same defect pointing the other way

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W2_rehearsal_said_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_the_flag_on_the_envelope_is_the_jobs_own_and_not_the_command_lines`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return (rehearsal_warning(),)
```

### `r222-b.B10_archive_not_compared`

Compare only the mirror, so two jobs rotating one archive root from different mirrors are strangers

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B10_archive_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`

Old text:

```
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
```

New text:

```
            frozen.backup.dest == cfg.backup.dest
```

### `r222-b.B5_whole_payload_compared`

Compare the whole payload, so a job frozen with one more key is a stranger and a second backup is filed beside it

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B5_whole_payload_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
```

New text:

```
        if dict(job.payload or {}) != {DRY_RUN: dry_run}:
```

### `r349-a.A2_success_produced`

The handler returns nothing on success instead of the staged record

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A2_success_produced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_handler_uses_the_configuration_it_was_handed`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    return jobs.Produced(staged=staged, final=final)
```

New text:

```
    return None
```

### `u45-round-1.C3_nothing_ran_accepted`

Return None when no portion ran, so a machine with no rclone exits OK over a backup that did not happen

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C3_nothing_ran_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 8 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
    refusals
```

New text:

```
    return None
    refusals
```

### `u45-round-1.Q4_payload_key_not_read`

Read a key the handler does not freeze, which is the drift the named constant exists to prevent

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q4_payload_key_not_read`
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
```

New text:

```
    if payload.get("dryrun"):
```

### `u45-round-1.W8_engine_refusal_escapes`

Let BackupRefused escape, so an unconfigured remote reaches the dispatcher as internal-error with report-defect

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W8_engine_refusal_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_unconfigured_remote_refuses_in_the_backup_vocabulary`

Old text:

```
    except backup.BackupRefused as exc:
        raise _engine_refusal(
            exc.refusal, exc.detail, library=str(cfg.library.root)
        ) from exc
```

New text:

```
    except backup.BackupRefused:
        raise
```

### `u50-review-fixes.R2_empty_job_guard_dropped`

Drive a job with no items, so a job queued by the previous build reports SUCCEEDED over a library nothing copied

- File: `src/cratekit/backup/cli.py`
- Source: `u50-review-fixes.json`, row `R2_empty_job_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`

Old text:

```
                _refuse_an_empty_job(store, job)
```

New text:

```
(empty)
```

### `r924.D3_write_failure_raises`

A progress line that cannot be written raises out of the paid pass

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D3_write_failure_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_closed_standard_error_does_not_end_a_paid_pass`

Old text:

```
        except (OSError, ValueError):
            pass
```

New text:

```
        except ValueError:
            pass
```

### `r349-a.A3_job_show_field`

job show stops attaching the outcomes field

- File: `src/cratekit/cli/jobs.py`
- Source: `r349-a.json`, row `A3_job_show_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`

Old text:

```
        summary[backup_facts.OUTCOMES_FIELD] = outcomes
```

New text:

```
        pass
```

### `u45-round-1.V5_module_toggle_dropped`

Drop the module toggle, so the verb is offered on a slim install that has no backup module

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u45-round-1.json`, row `V5_module_toggle_dropped`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4345 against a baseline of 4346
- Kills: 6 (collect-error)
- Note: collection changed: 4345 collected against a baseline of 4346. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_the_verb_is_declared_landed_and_names_this_module`
  - `tests/test_backup_cli.py::test_the_verb_is_offered_on_the_full_profile_and_withheld_on_the_slim_one`
  - `tests/test_cli_contract.py::test_every_declared_module_toggle_is_used_by_at_least_one_verb`
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cli_contract.py::test_every_live_toggle_is_driven_by_the_toggle_test_below`
  - `tests/test_doctor.py::test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure`

Old text:

```
source_scripts=("backup.sh",), module_id="backup",
```

New text:

```
source_scripts=("backup.sh",),
```

### `r925.R6_count_line`

The heading line counts one fewer track than it lists

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R6_count_line`
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
    lines = [f"  tracks: {len(rows)}"]
```

New text:

```
    lines = [f"  tracks: {len(rows) - 1}"]
```

### `r338-c.C6_only_the_first_root_is_watched`

is_watched: ask the library root alone, so a share aimed at the live share's own parent is pulled under the watch that refuses it

- File: `src/cratekit/core/analysis_store.py`
- Source: `r338-c.json`, row `C6_only_the_first_root_is_watched`
- Moved: Same is_watched line; U298 replaced the module's own _is_within with config.is_inside, the same textual containment test, so asking only the first root is the same mutation
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_store.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_that_would_land_under_the_analysis_watch_is_withheld_and_not_asked_about`

Old text:

```
    return any(config.is_inside(Path(path), root) for root in watch_roots(cfg))
```

New text:

```
    return config.is_inside(Path(path), watch_roots(cfg)[0])
```

### `u260.E5_key_digest_of_a_prefix`

to_cdj_jpeg_remembered: digest only the first kilobyte, so two pictures sharing a header share an encode

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E5_key_digest_of_a_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_two_covers_sharing_a_long_header_are_encoded_apart`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (hashlib.sha256(data[:1024]).digest(), len(data), size, max_bytes)
```

### `u83-a.E2_quality_floor`

Lower the quality floor from 50 to 45, a realistic nearby value

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E2_quality_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
ART_MIN_QUALITY = 50
```

New text:

```
ART_MIN_QUALITY = 45
```

### `u83-a.R2_unreadable_is_not_art_error`

A file that could not be read raises the image verdict again instead of its own class

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R2_unreadable_is_not_art_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_file_that_cannot_be_read_raises_rather_than_reading_as_no_art`

Old text:

```
        raise UnreadableFile(f"could not read
```

New text:

```
        raise ArtError(f"could not read
```

### `u83-b.W4_rgb_guard`

The writer accepts a greyscale or CMYK JPEG

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W4_rgb_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[jpeg-CMYK]`
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[jpeg-L]`

Old text:

```
    if measured.mode != "RGB":
```

New text:

```
    if False:
```

### `r349-c.C3_unparseable_reported`

An unparseable record is skipped rather than reported unreadable

- File: `src/cratekit/core/backup_facts.py`
- Source: `r349-c.json`, row `C3_unparseable_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_record_that_cannot_be_parsed_is_reported_rather_than_skipped`

Old text:

```
            found[path.stem] = {"unreadable": f"{path}: {exc}"}
```

New text:

```
            continue
```

### `example-binaries-five-row.B1_broken_override_falls_through`

find() returns a broken per-binary override as if it worked, instead of None. The guard exists so a set-but-broken override never falls through to a different binary.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B1_broken_override_falls_through`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_find_never_raises_because_doctor_reports_on_all_of_them`

Old text:

```
        return override if _executable(Path(override)) else None

```

New text:

```
        return override

```

### `r290-author.R3_the_owner_drops_the_type`

Make cause.rebuilt return the plain type for every input, so both hops drop the blocked bit at once with no hand written rebuild for the static guard to find

- File: `src/cratekit/core/cause.py`
- Source: `r290-author.json`, row `R3_the_owner_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`, `tests/test_backup_cli.py`
- Collected: 317 against a baseline of 317
- Kills: 13 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[analyze.run]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause[JobBlocked]`
  - `tests/test_job_outcome.py::test_a_rebuilt_refusal_keeps_a_carried_type_and_takes_the_new_cause[JobCancelled]`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`

Old text:

```
            return kind(cause)
```

New text:

```
            return CratekitError(cause)
```

### `u254.C4_append_not_append`

append_durable_bytes: open for writing at the start of the file rather than its end

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C4_append_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 962 against a baseline of 962
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

### `r290-author.J4_predicate_narrowed_to_failed`

Narrow the closed predicate to FAILED alone, so a run stopped by a signal is reported through a normal envelope

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J4_predicate_narrowed_to_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 29 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
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
  - ... and 14 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if job.state is JobState.FAILED and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `u331.S16_item_path_reexport_joins_plainly`

jobs: drop the item_path re-export analysis and vocals resolve an item through, so a feature package reaching it through the listed module finds nothing

- File: `src/cratekit/core/jobs.py`
- Source: `u331.json`, row `S16_item_path_reexport_joins_plainly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_import_rules.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 84 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_calibrated_level_is_written_and_routes_to_a_band`
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_corrupt_undo_log_refuses_by_name_rather_than_failing_every_item_as_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - ... and 69 more, see the JSON sidecar

Old text:

```
    frozen_walk,
    item_path,
    scan_audio,
```

New text:

```
    frozen_walk,
    scan_audio,
```

### `u342.S6_stamp_reads_back_the_body`

stamp_head: drop the read back that the body after the head is the name's own

- File: `src/cratekit/core/naming.py`
- Source: `u342.json`, row `S6_stamp_reads_back_the_body`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_title_with_no_head_is_stamped_and_keeps_every_byte[a-body-that-would-not-read-back]`
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`

Old text:

```
        or strip_head(stamped, template=template) != strip_head(name, template=template)

```

New text:

```
        or False

```

### `u205.G5_app_share_unclamped`

gate state load: an app share above the total is kept, so the account's share reads negative and is shown as zero

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G5_app_share_unclamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_an_app_share_larger_than_the_total_is_clamped_to_it`

Old text:

```
            state.app_calls = min(_as_int(app.get("calls")), state.calls)
```

New text:

```
            state.app_calls = _as_int(app.get("calls"))
```

### `r758-a.W7_removed_row_marked_again`

remove_memberships marks a row that is already removed and reports it, so a second removal counts a row it did not remove

- File: `src/cratekit/core/rb_nodes.py`
- Source: `r758-a.json`, row `W7_removed_row_marked_again`
- Moved: moved by U300's split from src/cratekit/core/rb_writer.py to rb_nodes.py, the same guard in remove_memberships, the module's names now read through the module
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_adopt_move.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removed_membership_is_not_held_and_not_present`

Old text:

```
        if key not in wanted or _writer().membership_removed(song):
```

New text:

```
        if key not in wanted:
```

### `r731-b.M22_single_sub_does_not_compete`

a bucket's single sub is left out of its competing subs

- File: `src/cratekit/core/routing.py`
- Source: `r731-b.json`, row `M22_single_sub_does_not_compete`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_every_sub_routing_can_name_is_one_of_its_buckets_competing_subs`

Old text:

```
        if bucket.single_sub is not None:
            found.add(bucket.single_sub.id)
        return Competing.STYLE
```

New text:

```
        return Competing.STYLE
```

### `r722-b.T6_field_failure_swallowed`

An undecodable field reads as absent in the checked reader, rerun after the fix round

- File: `src/cratekit/core/tags.py`
- Source: `r722-b.json`, row `T6_field_failure_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2990 against a baseline of 2990
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
            log.debug("tag read failed for %s %s: %s", path, key, exc)
```

### `u81-fetch-b.S1_strip_does_nothing`

strip_tags reports success and removes nothing, so an upload's tempo frame survives

- File: `src/cratekit/core/tags.py`
- Source: `u81-fetch-b.json`, row `S1_strip_does_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_strip_tags_empties_an_id3_chunk_inside_a_container_and_keeps_the_audio`

Old text:

```
        handle.delete()
        return True
```

New text:

```
        return True
```

### `r301.B2_bound_host_ignored`

The bound identifier asks the default region whatever the section names

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B2_bound_host_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[set]`

Old text:

```
            host=recognition.host,
```

New text:

```
            host=config.DEFAULT_RECOGNITION_HOST,
```

### `r706-a.A5_run_guard_dropped`

Drop the per part run guard, so an oversize part is paid for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A5_run_guard_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
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

### `r706-b.B6_grid_not_partitioned`

identify hands the whole grid over as one part, so the run guard meets a 5 hour mix

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B6_grid_not_partitioned`
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
    parts = partition(offsets, per_run=spend.per_run)
```

New text:

```
    parts = (offsets,)
```

### `u103-a.A10_write_is_a_merge`

Replace the cache document with this pass's answers instead of laying them over what is kept

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A10_write_is_a_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_split_set_is_one_cached_plan_and_a_gap_meets_the_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_write_is_a_merge_so_an_overlapping_pass_does_not_drop_what_another_paid_for`
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`

Old text:

```
            merged = {**self.read(plan), **answers}
```

New text:

```
            merged = dict(answers)
```

### `u57-recognition-and-items.M11_unreached_stop_tenfold`

Fifty unanswered calls in a row before the run stops, not five

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M11_unreached_stop_tenfold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent[rejected]`
  - `tests/intake/test_recognition.py::test_five_unanswered_calls_in_a_row_stop_the_run_and_count_what_was_spent[unreached]`

Old text:

```
UNREACHED_STOP = 5
```

New text:

```
UNREACHED_STOP = 50
```

### `u57-recognition-and-items.M5_empty_music_not_none`

A match answer carrying no music entry is indexed rather than read as none

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M5_empty_music_not_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_match_naming_no_artist_or_no_title_or_no_music_is_none_and_a_bad_score_is_zero`

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

### `r679-b.D1_intake_gate_on_question_alone`

intake worker: gate the store on the needs-review state alone, the code before the fix round

- File: `src/cratekit/intake/cli.py`
- Source: `r679-b.json`, row `D1_intake_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 834 against a baseline of 834
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if not match_cli.touches_the_queue(found):
```

New text:

```
    if found.state is not match.MatchState.NEEDS_REVIEW:
```

### `r924.C1_set_identify_not_told`

intake set does not hand its progress to identification

- File: `src/cratekit/intake/cli.py`
- Source: `r924.json`, row `C1_set_identify_not_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 119 against a baseline of 119
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

### `u213.M12_absent_rule`

_absent: name the missing half by the artist alone, the rule the review replaced, so a row with neither says no artist

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M12_absent_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_aside_track_names_the_half_the_reader_names`

Old text:

```
    return "artist" if match.split_title(title)[0] else "title"
```

New text:

```
    return "artist" if title else "title"
```

### `u70.S2_sentinel_casefold`

The sentinel is compared case sensitively, so Favorites is read as a playlist reference

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S2_sentinel_casefold`
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
    return str(reference or "").strip().casefold() == FAVORITES
```

New text:

```
    return str(reference or "").strip() == FAVORITES
```

### `r925.S4_write_failure_refuses`

A tracklist that cannot be written raises out of intake set after the job is queued

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r925.json`, row `S4_write_failure_refuses`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`

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
        path = _write_tracklist(out, held, result)
    except ValueError as exc:
        failed = _tracklist_path(out, held, result)
```

### `u104-d.C2_refusal_named_for_the_address`

Let a refusal raised inside the identifier through as it is, naming the scratch file in its message and detail

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C2_refusal_named_for_the_address`
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
                raise _named_for_the_address(exc, held) from exc.__cause__
```

New text:

```
                raise
```

### `r770-d.S1_composite_the_splice_takes_a_stub`

COMPOSITE for r770-a's S1, which was a zero: collection_xml.splice_tracks does not refuse a U22 stub listing, with place_files' own refusal left in place. The driver pairs only inside one batch, so the pairing is recorded in r770-notes.md

- File: `src/cratekit/intake/collection_xml.py`
- Source: `r770-d.json`, row `S1_composite_the_splice_takes_a_stub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_landing.py`, `tests/test_intake_imported.py`, `tests/intake/test_collection_xml.py`
- Collected: 85 against a baseline of 85
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_a_u22_stub_listing_is_not_a_splice_target`
  - `tests/test_landing.py::test_an_export_that_cannot_be_spliced_is_refused_before_any_move[stub]`

Old text:

```
    if is_stub_listing(raw):
```

New text:

```
    if False:
```

### `u104-a.F1_guard_string_layer`

Drop the textual half of the library guard: a scratch folder that resolves to the library or to a path under it is no longer refused by name

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F1_guard_string_layer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_library_that_is_not_there_is_still_refused_by_name`

Old text:

```
    if here == library or library in here.parents:
        raise ScratchUnderLibrary(here, library)
    if not library.exists():
```

New text:

```
    if not library.exists():
```

### `u104-b.F9_scratch_prepare_is_its_own_kind`

Report a scratch folder that cannot be made as an ordinary failed fetch rather than as a fact about this machine

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F9_scratch_prepare_is_its_own_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_made_is_a_fact_about_this_machine`

Old text:

```
            raise ScratchUnusable(
                f"the scratch folder {scratch} could not be prepared "
```

New text:

```
            raise SetFetchFailed(
                f"the scratch folder {scratch} could not be prepared "
```

### `u37-author-light.G4_staging`

Allow inbox of files still under download staging

- File: `src/cratekit/intake/ingest.py`
- Source: `u37-author-light.json`, row `G4_staging`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_staging_files_are_refused`

Old text:

```
    if resolved == staging or staging in resolved.parents:
```

New text:

```
    if False and (resolved == staging or staging in resolved.parents):
```

### `u331.S07_check_engine_origin_renamed`

intake/rekordbox_check: print the module's new place as the envelope's origin, so analyze check's refusals change the origin they have always printed

- File: `src/cratekit/intake/rekordbox_check.py`
- Source: `u331.json`, row `S07_check_engine_origin_renamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_landing_nothing_recorded_refuses_rather_than_reading_empty[--pass]`
  - `tests/test_analyze_check.py::test_a_landing_nothing_recorded_refuses_rather_than_reading_empty[--session]`

Old text:

```
_ORIGIN = ("analysis.rekordbox_check",)
```

New text:

```
_ORIGIN = ("intake.rekordbox_check",)
```

### `u102-a.P3_root_filter`

_plan_for: ignore the root, so an accepted item outside it is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P3_root_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder`

Old text:

```
        if accepted.path is not None and not _under(accepted.path, root):
```

New text:

```
        if False:
```

### `u102-a.U5_linked_file`

_unusable_why: drop the check that the stored path names the file the proposal was shown for, so a link's target is renamed

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U5_linked_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_linked_file_is_never_renamed_through_its_link`

Old text:

```
    if accepted.recorded and Path(accepted.path).name != accepted.recorded:
```

New text:

```
    if False:
```

### `u102-b.G9_post_gate_missing`

_apply: drop the check that the file is still there after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G9_post_gate_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_file_deleted_after_the_gate_is_named_and_not_called_renamed`

Old text:

```
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
```

New text:

```
(empty)
```

### `u237.M1_bare_letter_is_a_mark_again`

_YEAR: make the parentheses optional again, so a bare leading P or C is stripped as a mark (Cadenza reads adenza)

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M1_bare_letter_is_a_mark_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 33 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(C) ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(P)]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(C) ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(P)]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(C) ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(P)]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\u2117]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-\xa9 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\(?[PC]\)?|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

### `u177.A3_account_case`

bandcamp_account: keep the case typed, so PulsRomania never equals the purchase's pulsromania

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A3_account_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_an_account_is_looked_up_in_any_form_a_purchase_could_name_it`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[PulsRomania]`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
    text = account.strip().lower() if isinstance(account, str) else ""

```

New text:

```
    text = account.strip() if isinstance(account, str) else ""

```

### `r704-a.S6_status_coefficient`

the context check asks for a 503 rather than the rate limit statuses

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S6_status_coefficient`
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
    if any(status_of(link) in {503} for link in _linked(exc, "__context__")):
```

### `u237.M8_one_direction_only`

labels_match: drop the credit inside the needle direction, so a needle Rawax Records no longer confirms a credit Rawax

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M8_one_direction_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_confirms_its_label_on_whole_words[Rawax Records-Rawax]`

Old text:

```
(_words_within(left, right) or _words_within(right, left))
```

New text:

```
_words_within(left, right)
```

### `r356-b.B5_export_plan_hands_on_the_display_title`

The export engine hands the account the title with its naming head on

- File: `src/cratekit/modules/outbound/export.py`
- Source: `r356-b.json`, row `B5_export_plan_hands_on_the_display_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_the_export_plan_hands_the_account_the_release_title_and_album[release-title-not-display-title]`
  - `tests/modules/test_outbound.py::test_the_export_plan_hands_the_account_the_release_title_and_album[the-files-album-tag]`

Old text:

```
            title=track.release_title,
```

New text:

```
            title=track.title,
```

### `r229.L12_the_first_of_several_is_adopted`

Two candidates are settled by taking the first rather than reported and left

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L12_the_first_of_several_is_adopted`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_two_candidates_are_both_named_and_neither_is_adopted`
  - `tests/test_outbound_workers.py::test_two_orphaned_records_that_could_each_be_it_adopt_neither`

Old text:

```
    if len(found) != 1:
        return Recognition(crate=len(wanted), candidates=candidates)
```

New text:

```
    if not found:
        return Recognition(crate=len(wanted), candidates=candidates)
```

### `r229.L3_nothing_shared_is_a_match`

The at least one shared track guard is removed, so an empty record is carried by anything

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L3_nothing_shared_is_a_match`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_that_holds_nothing_is_carried_by_nothing`

Old text:

```
    return shared >= 1 and shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR
```

New text:

```
    return shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR
```

### `u309-z.U1_settle_found_refusal`

A settled write whose record is gone no longer refuses: the shared check of five settles passes an empty entry

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u309-z.json`, row `U1_settle_found_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_settled_write_whose_record_is_gone_refuses`

Old text:

```
    if not entry:
        raise _refused(cfg, f"it holds no {what}, whose tracks were just {done}")
```

New text:

```
    if False:
        raise _refused(cfg, f"it holds no {what}, whose tracks were just {done}")
```

### `u27-reports-round-1.C2_tree_anchored_at_zero`

Anchor the governed-path filter at position zero, the shape that reported nothing for a nested tree

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C2_tree_anchored_at_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_inside_another_folder_is_still_the_governed_tree`

Old text:

```
        playlist.path for playlist in view.playlists if wanted in playlist.path[:-1]
```

New text:

```
        playlist.path for playlist in view.playlists if playlist.path[:1] == (wanted,)
```

### `u27-reports-round-1.L4_median_even`

Take the upper middle instead of averaging the pair on an even population

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L4_median_even`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tempo_median_over_an_even_population_averages_the_middle_pair`

Old text:

```
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2

```

New text:

```
    return ordered[middle]

```

### `r154-a.A2_stamp_calendar`

Drop the calendar half of is_stamp, so the pattern alone decides and a thirteenth month is a stamp

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A2_stamp_calendar`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-13-01T000000Z]`

Old text:

```
    try:
        datetime.strptime(value, _STAMP_FORMAT)
    except ValueError:
        return False
    return True
```

New text:

```
    return True
```

### `r222-a.A1_nothing_held`

Hold nothing, which is the finding itself: the rotation counts attempts again and a retry that succeeds purges the failed attempt's archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A1_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = []
```

### `r222-a.A9_rehearsal_purges`

EXISTING GUARD, sampled because this round re-armed its tests: a rehearsal runs the real purge

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A9_rehearsal_purges`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
                    purge=not dry_run,
```

New text:

```
                    purge=True,
```

### `u45-round-2.E5_outcome_ok_widened`

Answer ok when ANY portion is fine rather than all of them

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-2.json`, row `E5_outcome_ok_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`

Old text:

```
        return all(p.refusal is not None or p.ran for p in self.portions)
```

New text:

```
        return any(p.refusal is not None or p.ran for p in self.portions)
```

### `r1761.P13_history_record_ignored`

_history: the record is not read, so an upgrade from a record with no census has no history

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P13_history_record_ignored`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_proof.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 77 (killed)
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
  - ... and 62 more, see the JSON sidecar

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

### `r1761.P23_probe_counts_state`

probe: a file in the state folder is counted as the library's, so a stray state folder proves the root

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `r1761.json`, row `P23_probe_counts_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_unproven_root.py::test_the_probe_reads_past_an_exclude_the_walk_cannot_translate`

Old text:

```
            anything = True
            if held(rel, state_dirname):
```

New text:

```
            anything = True
            if True:
```

### `r154-b.B4_stated_volume_over_unmarked`

Pull an unmarked named snapshot even when a person stated the volume it should record, so the statement is checked against nothing

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B4_stated_volume_over_unmarked`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_replaced_drive_restores_the_old_volumes_snapshot_by_naming_it`

Old text:

```
        if not recorded and snapshot_volume is None and accepted:
```

New text:

```
        if not recorded and accepted:
```

### `r338-a.B6_identity_interpolated_raw`

share_destination: interpolate the configured identity as typed and unvalidated, so a value with a separator writes the share somewhere else on the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B6_identity_interpolated_raw`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r338-b.R9_contained_restore_asks_about_a_share`

_plan_restore_inside_the_gates: treat every layout as the outside one on restore, so a contained library lists and pulls a share mirror it never wrote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R9_contained_restore_asks_about_a_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r367.G4_the_inventory_restored_flag_is_ignored`

a listed shared memory index is written back beside a fresh log

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G4_the_inventory_restored_flag_is_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_copies_the_log_only_when_the_snapshot_holds_it[holding-the-log-copies-it]`
  - `tests/modules/test_tools.py::test_a_restore_copies_the_log_only_when_the_snapshot_holds_it[only-the-database-skips-the-absent-sidecar]`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
        if not sidecar.restored:
            continue

```

New text:

```
(empty)
```

### `r388-a.M5_root_listing_back_to_absence`

A snapshot root listing that exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M5_root_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `u311.C1_first_loudness_block`

The loudness reader takes the first JSON block in ffmpeg's stderr instead of the last

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C1_first_loudness_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 247 against a baseline of 247
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_loudness_report_is_parsed_as_json_not_grepped`

Old text:

```
    for raw in reversed(_JSON_BLOCK.findall(stderr_text or "")):
```

New text:

```
    for raw in _JSON_BLOCK.findall(stderr_text or ""):
```

### `r187-a.A11_no_cutoff`

match_in_index: score cutoff to zero, so a name nothing answers to reaches the whole index

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A11_no_cutoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_web_lookup_is_a_seam_that_is_absent_by_default`
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`

Old text:

```
        score_cutoff=threshold,
```

New text:

```
        score_cutoff=0,
```

### `u266.M6_size_not_compared`

_entry_is_current: trust a cached entry without comparing the size, the sample guard on when the warm index is trusted

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M6_size_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 324 against a baseline of 324
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

### `u281.R7_one_count_for_every_catalogue`

Refusals.heard: count every catalogue's refusals under one key, so a refusing fallback stops Beatport too

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R7_one_count_for_every_catalogue`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_discogs_is_never_under_the_count`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
        if self.running.get(source, 0) < self.limit:
```

New text:

```
        if sum(self.running.values()) < self.limit:
```

### `u260.F10_fetch_memory_one`

IMAGE_MEMORY: one entry, so two interleaved albums ask on every file

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F10_fetch_memory_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_shipped_fetch_memory_is_bounded`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`

Old text:

```
IMAGE_MEMORY = 4
```

New text:

```
IMAGE_MEMORY = 1
```

### `u260.F7_fetch_evicts_newest`

remembering: evict the newest entry instead of the least recently used

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F7_fetch_evicts_newest`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`

Old text:

```
                held.popitem(last=False)
```

New text:

```
                held.popitem(last=True)
```

### `u281.W5_run_never_changes`

for_run: keep the first run's count for every later run, so the next sweep never asks a stopped catalogue

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W5_run_never_changes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 4 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_run_met_again_after_another_starts_afresh`
  - `tests/test_beatport_refusal.py::test_one_run_name_is_one_count_and_another_name_a_fresh_one`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
    if not _run_refusals or _run_refusals[0][0] != run:
```

New text:

```
    if not _run_refusals:
```

### `u133-b-rerun.T6_former_sub`

The former place records the old playlist under another sub identifier

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b-rerun.json`, row `T6_former_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1038 against a baseline of 1038
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_the_old_playlist_is_found_under_the_identifier_it_was_recorded_by`

Old text:

```
bucket = "non_electronic"
sub = "jazz"

```

New text:

```
bucket = "non_electronic"
sub = "jazz_style"

```

### `r675.G4_could_name_empty`

_referenced: the candidates in doubt are never collected, so the refusal names rows and no files

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G4_could_name_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`
  - `tests/intake/test_repair_apply.py::test_a_dark_row_under_a_proposal_name_refuses_the_repair_and_its_plan`
  - `tests/test_naming_apply_cli.py::test_a_dark_row_is_matched_across_folders_by_leaf_alone`
  - `tests/test_naming_apply_cli.py::test_a_dark_tombstone_under_a_candidate_name_still_refuses`
  - `tests/test_naming_apply_cli.py::test_a_gone_file_under_a_folder_on_this_machine_refuses_under_a_candidate_name`
  - `tests/test_naming_apply_cli.py::test_every_unmapped_row_is_counted_and_the_first_is_named`
  - `tests/test_naming_apply_cli.py::test_two_dark_rows_under_one_candidate_name_each_name_it`

Old text:

```
            "could_name": [{"row": decoded, "files": named} for decoded, named in dark[:20]],
```

New text:

```
            "could_name": [{"row": decoded, "files": []} for decoded, named in dark[:20]],
```

### `r758-a.T3_target_not_proven`

a removal is made whether or not the track sits in its target, so a track can end in neither

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T3_target_not_proven`
- Moved: the proof of the target is now the step _proven_leavers, one level less indented, the same test
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`

Old text:

```
        if not places.holds(move.target, move.content_id):
            held_back.append(move.content_id)
            continue
```

New text:

```
(empty)
```

### `r685-b.G1_the_guard_forgets_aliases`

The guard stops binding aliased imports, so an import as another name hides the call

- File: `tests/test_active_taxonomy.py`
- Source: `r685-b.json`, row `G1_the_guard_forgets_aliases`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_the_guard_sees_every_spelling_it_should_refuse`

Old text:

```
                    bound[alias.asname or alias.name] = alias.name

```

New text:

```
                    pass

```

