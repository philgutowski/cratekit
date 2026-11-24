# Mutation table: u332-replay-after-1

Measured by `scripts/mutate.py` on 2026-11-24 07:05 UTC, branch `HEAD` at `6482067c`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23212 collected. pytest invocations for this batch: 286.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 07:05 UTC for commit `6482067c55e5`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 111, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23212 against 23212. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B10_a_changed_mode_unseen` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u297.B7_a_word_read_inside_a_longer_one` | `scripts/behaviour_compare.py` | maintainer | 1 file(s) | 137 | 3 | killed |
| `u122.H6_hold_beats_closure` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 4 | killed |
| `u148.C4_only_none_refused` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 1 | killed |
| `u148.W2_whole_off` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 3 | killed |
| `u151.N1_number_filter_dropped` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X4_unseen_project_trusted` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 2 | killed |
| `u203.M1_no_opening_span` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 6 | killed |
| `u203.M9_no_comma_cut` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u313.B6_refusal_exit_code` | `scripts/board.py` | maintainer | 2 file(s) | 55 | 4 | killed |
| `r83.D1_offer_defect` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 8 | killed |
| `u47-author.CODEC_refused_track_sinks_the_run` | `src/cratekit/acquire/adapter.py` | user | 2 file(s) | 202 | 2 | killed |
| `u176.C4_page_without_items_list` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 92 | 4 | killed |
| `u176.V13_number_after_prefix` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V8_recorded_item_done` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u177.B6_frozen_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 8 | killed |
| `u205.C1_park_wrapped_as_outage` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 2 | killed |
| `u205.C9_names_not_included` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `r668-a.M9_other_verbs_job_read` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `u169.A5_warning_names_failed_items` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u54-acquisition-worker.G17_paced_sleep_bound` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 2 | killed |
| `u54-acquisition-worker.G8_park_on_block` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 94 | 1 | killed |
| `u80.F13_rejected_searched_again` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F7_mix_boundary` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `r289-b.C3_fallback_queue_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `u81-fetch-a.W3_host_half` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Q5_owned_row_fetched` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 3 | killed |
| `r1016.M5_not_a_page_check_dropped` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 793 | 3 | killed |
| `r878-a.A12_parse_retried` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 141 | 1 | killed |
| `r878-a.A9_cursor_advances` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 141 | 14 | killed |
| `r887-a.K3_count_kept_not_served` | `src/cratekit/acquire/listing.py` | user | 3 file(s) | 204 | 3 | killed |
| `u65.B5_artist_releases_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 265 | 3 | killed |
| `u65.E1_the_shape_helper_ignores_the_rule_table` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 198 | 28 | killed |
| `u265.M8_other_scorer` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2712 | 25 | killed |
| `u213.M4_first_group_keeps_brackets` | `src/cratekit/acquire/match_identity.py` | user | 3 file(s) | 726 | 15 | killed |
| `u261.W2_changed_session_skipped` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 485 | 5 | killed |
| `r703-a.V4_no_escalation` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 2 | killed |
| `r703-b.R2_everything_is_the_provider` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 276 | 1 | killed |
| `u47-author.CODEC_no_refusal` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 4 | killed |
| `u47-author.R196_absent_marker_reads_as_pkce` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 1 | killed |
| `u47-author.R197_drop_progress_overall` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 202 | 3 | killed |
| `u254.M01_mark_validates_record` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 4 | killed |
| `u254.M10_torn_needs_terminated_tail` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 1 | killed |
| `u254.M18_remark_first_wins` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 1 | killed |
| `r722.A1_gate_drops_tally` | `src/cratekit/adopt/apply_cli.py` | user | 3 file(s) | 63 | 1 | killed |
| `u165.A2_refuse_unplaced_called` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 100 | 1 | killed |
| `u55-collection-reader.R10_apply_zero_item_refusal` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 1 | killed |
| `u956.O17_gate_hides_outside` | `src/cratekit/adopt/apply_cli.py` | user | 3 file(s) | 72 | 1 | killed |
| `u55-collection-reader.R3_soft_delete_marker` | `src/cratekit/adopt/collection.py` | user | 3 file(s) | 56 | 1 | killed |
| `r780-a.A4_excluded_track_moved` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `u118-c.M10_no_reading_leaves_split` | `src/cratekit/adopt/move.py` | user | 2 file(s) | 102 | 3 | killed |
| `u340.R27_move_split_kept` | `src/cratekit/adopt/move.py` | user | 4 file(s) | 814 | 6 | killed |
| `r780-b.B5_verdicts_not_handed_to_the_worker` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r788-c.L4_renamed_membership_unseen` | `src/cratekit/adopt/placements.py` | user | 4 file(s) | 163 | 3 | killed |
| `r1965.R01_manual_class_beside` | `src/cratekit/adopt/plan.py` | user | 9 file(s) | 432 | 7 | killed |
| `r722.P7_tally_counts_excluded` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 651 | 1 | killed |
| `r731-a.M08_digest_blind_to_unread` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 1 | killed |
| `r788-a.P6_present_is_added` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 8 | killed |
| `u23-round-8-independent.X10_entry_id_drops_the_sub` | `src/cratekit/adopt/plan.py` | user | 1 file(s) | 613 | 1 | killed |
| `u23-round-8-independent.A2_at_risk_always_false` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 6 | killed |
| `u23-round-8-independent.C2_shape3_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 613 | 1 | killed |
| `u23-round-8-independent.G1_locked_passes_no_size` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 613 | 2 | killed |
| `r722.S2_track_drops_energy` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 7 | killed |
| `u339-composites.C6_census_tombstone` | `src/cratekit/adopt/scan.py` | user | 7 file(s) | 1016 | 49 | killed |
| `u956.O4_outside_reads_missing` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 639 | 6 | killed |
| `u55-collection-reader.R9_scan_zero_item_refusal` | `src/cratekit/adopt/scan_cli.py` | user | 1 file(s) | 29 | 2 | killed |
| `u223.M1_keep_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 176 | 1 | killed |
| `u223.M5_discard_keeps_report` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 176 | 1 | killed |
| `u90-a.A2_upper_bound_strict` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 1 | killed |
| `u90-b.B4_date_field_dropped` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 176 | 1 | killed |
| `u94-a.S2_floor_off_by_one` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 2 | killed |
| `u94-b.W3_accepted_reads_ok` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 2 | killed |
| `u94-c.N3_sample_ignored` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 212 | 3 | killed |
| `u192.A3_restamp_wrong_resume` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 176 | 1 | killed |
| `u241.M19_failed_run_does_not_say_its_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 271 | 4 | killed |
| `u343.M01_finalize_no_mark` | `src/cratekit/analysis/cli.py` | user | 5 file(s) | 534 | 9 | killed |
| `u343.M25_report_renamed_to_back` | `src/cratekit/analysis/cli.py` | maintainer | 1 file(s) | 176 | 1 | killed |
| `u263.D10_first_stream` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 1 | killed |
| `u264.M13_float64_halving` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 4 | killed |
| `u344.M1_head_bypasses_restamp_measure` | `src/cratekit/analysis/detect.py` | user | 5 file(s) | 495 | 1 | killed |
| `u327.A12_agreeing_title_left_whole` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 7 | killed |
| `u327.A20_judge_title` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u342.P10_leave_holds_a_stamp` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 1 | killed |
| `u342.P7_tag_must_be_the_title` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 2 | killed |
| `u241.M11_cost_from_the_cheapest_track` | `src/cratekit/analysis/light.py` | user | 1 file(s) | 271 | 13 | killed |
| `u275.M7_cheapest_track_sets_the_cost` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 553 | 13 | killed |
| `sitting3.G13_padded_frames_kept` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 1 | killed |
| `sitting3.G9_tail_sent_alone` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 5 | killed |
| `u58-workers-and-wav.W4_model_guard` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 176 | 2 | killed |
| `u92-author.G5_guard_after_the_load` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 230 | 1 | killed |
| `r221-a.W1_rehearsal_never_said` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `r221-b.R1_refusal_is_its_own_cause` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B4_rehearsal_is_a_twin` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `r349-a.A1_failure_write` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.C2_refusal_read_as_failure` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 6 | killed |
| `u45-round-1.Q3_resume_loses_the_job` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 2 | killed |
| `u45-round-1.W6_rehearsal_becomes_a_real_run` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 6 | killed |
| `u50-author.W6_fresh_config_in_the_handler` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 19 | killed |
| `r924.D2_human_gets_none` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 52 | 5 | killed |
| `u58-workers-and-wav.H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 8 file(s) | 603 | 36 | killed |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry_modules.py` | user | 24 file(s) | 4342 | collection error | collect-error |
| `r925.R4_version_unsaid` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 1 | killed |
| `u247.M9_unmounted_guard_sample` | `src/cratekit/core/active_taxonomy.py` | user | 4 file(s) | 293 | 2 | killed |
| `u260.E4_key_by_length_only` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 2 | killed |
| `u83-a.E1_baseline_flag` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 3 | killed |
| `u83-a.R1_flac_declared_dimensions` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W3_progressive_guard` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u953.M20_held_key_not_moved` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 33 | 4 | killed |
| `r1313.N4_not_found_status_moved` | `src/cratekit/core/cause.py` | user | 5 file(s) | 561 | 19 | killed |
| `u254.C2_append_one_write` | `src/cratekit/core/config.py` | user | 4 file(s) | 962 | 1 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2532 | 109 | killed |
| `u298.H21_advance_refuses_empty` | `src/cratekit/core/jobs.py` | user | 2 file(s) | 131 | 3 | killed |
| `u342.S3_stamp_refuses_a_trailing_head` | `src/cratekit/core/naming.py` | user | 4 file(s) | 392 | 1 | killed |
| `u205.G3_attach_drops_identity` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 184 | 6 | killed |
| `u329.P1_rb_changes_wrong_family` | `src/cratekit/core/rb_changes.py` | user | 5 file(s) | 449 | 201 | killed |
| `r731-b.M21_sink_does_not_compete` | `src/cratekit/core/routing.py` | user | 2 file(s) | 70 | 7 | killed |
| `u329.P7_session_holders_wrong_family` | `src/cratekit/core/session_holders.py` | user | 5 file(s) | 708 | 81 | killed |
| `u250.M7_energy_word_reads_absent` | `src/cratekit/core/tags.py` | user | 4 file(s) | 126 | 2 | killed |
| `r301.B1_shipped_month_unbounded` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 5 | killed |
| `r706-a.A4_month_asked_of_one_run` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 1 | killed |
| `r706-b.B5_chunks_count_the_first_part` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 4 | killed |
| `r924.A7_kept_chunks_counted` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 78 | 1 | killed |
| `u103-a.A9_refresh_reads_nothing_kept` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 4 | killed |
| `u57-recognition-and-items.M4_transient_range_dropped` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 4 | killed |
| `r431-b.B9_the_freeze_drops_the_field` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 596 | 3 | killed |
| `r706-c.C3_summary_ignores_the_payload` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u213.M11_unreadable_said_isrc` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u70.E1_missing_id_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 2 | killed |
| `r925.S3_no_write` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 3 | killed |
| `u103-b.C9_refusal_counts_the_gap` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `r740-b.E2_average_bpm_nonzero` | `src/cratekit/intake/collection_xml.py` | user | 5 file(s) | 113 | 16 | killed |
| `r924.F5_watcher_not_joined` | `src/cratekit/intake/fetch.py` | maintainer | 1 file(s) | 11 | 1 | killed |
| `u104-b.F8_leftover_recorded` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u121.S18_info_json_flag` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u37-author-light.G2_recognition_gate` | `src/cratekit/intake/recognize.py` | user | 1 file(s) | 8 | 1 | killed |
| `u102-a.P2_root_casefold` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-a.U4_same_suffix` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G8_collision_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u52-item-derivation.C2_can_list_requires_all` | `src/cratekit/label/crawl.py` | user | 1 file(s) | 180 | 3 | killed |
| `u177.A1_account_suffix` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 23 | killed |
| `r704-a.S5_context_read_by_type` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `u237.M7_left_word_boundary_only` | `src/cratekit/label/verify.py` | user | 3 file(s) | 392 | 7 | killed |
| `u192.F8_not_exclusive` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 278 | 3 | killed |
| `r229.L11_an_empty_name_matches` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L2_exactly_half_is_not_enough` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `u309.U5_reserve_written` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 9 file(s) | 514 | 136 | killed |
| `u27-reports-round-1.C1_tree_absent_refusal` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L3_empty_tempo_is_zero` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `r154-a.A1_stamp_pattern` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 188 | 1 | killed |
| `r222-a.A10_plan_text_at_keep_zero` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 188 | 1 | killed |
| `r222-a.A8_floor_read_by_a_rehearsal` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 3 | killed |
| `r388-c.M17_slug_respelled` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 722 | 4 | killed |
| `u317.Q10_token_not_struck` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 23212 | 0 (promoted) | zero |
| `u45-round-1.E4_return_codes_unread` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 16 | killed |
| `u311.A9_uncomposed_reads_nfd` | `src/cratekit/modules/tools/backup_record.py` | user | 4 file(s) | 317 | 1 | killed |
| `r154-b.B3_handed_down_stamp` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 188 | 1 | killed |
| `r338-a.B5_one_mirror_for_every_library` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 4 | killed |
| `r338-b.R8_unmarked_snapshot_orphans_the_share` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r367.G3_membership_is_inverted` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 4 | killed |
| `r388-a.M4_contents_listing_message_reworded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 430 | 3 | killed |
| `u44-author.A3_archive_after_the_first_pass` | `src/cratekit/modules/tools/mastering.py` | user | 2 file(s) | 245 | 1 | killed |
| `r187-b.B8_bool_is_a_number` | `src/cratekit/modules/tools/setbuilder.py` | maintainer | 2 file(s) | 268 | 1 | killed |
| `u43-author-light.E3_tempo_serialized_as_bpm` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 4 | killed |
| `u281.R6_outage_keeps_the_count` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 1 | killed |
| `u956.O5_tagging_walk_confined` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 88 | 1 | killed |
| `u260.F6_fetch_bound_off_by_one` | `src/cratekit/tagging/searchers.py` | maintainer | 4 file(s) | 263 | 1 | killed |
| `u281.W4_binder_drops_the_count` | `src/cratekit/tagging/searchers.py` | user | 2 file(s) | 138 | 1 | killed |
| `u118-d.T2_named_word` | `src/cratekit/templates/taxonomy.default.toml` | user | 2 file(s) | 928 | collection error | collect-error |
| `u133-b.T9_energy_off` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 1038 | 13 | killed |
| `r675.G3_candidate_leaf_not_keyed` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 121 | 14 | killed |
| `r758-a.T2_first_commit_admits_a_removal` | `src/cratekit/write/trees.py` | user | 1 file(s) | 87 | 1 | killed |
| `r658-b.S12_repair_real_read` | `tests/intake/test_repair_apply.py` | user | 1 file(s) | 22 | 1 | killed |

## Zero rows and what they owe

- `u317.Q10_token_not_struck` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u297.B10_a_changed_mode_unseen`

compare_files: stop comparing permission bits, so a private file written world readable compares clean

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B10_a_changed_mode_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_private_file_written_world_readable_is_reported`

Old text:

```
        if one.get("mode") != other.get("mode"):
```

New text:

```
        if False:
```

### `u297.B7_a_word_read_inside_a_longer_one`

same_but_for: drop the leading end of the whole word rule, so a process id is read inside a longer number

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B7_a_word_read_inside_a_longer_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[lock_3409-lock_3467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid 13409-pid 13467-False]`
  - `tests/test_behaviour_compare.py::test_two_texts_are_the_same_only_where_each_holds_its_own_word[pid x3409-pid x3467-False]`

Old text:

```
        r"(?<![0-9A-Za-z_])(?:" + "|".join(re.escape(one) for one in longest_first) + r")(?![0-9A-Za-z_])"
```

New text:

```
        r"(?:" + "|".join(re.escape(one) for one in longest_first) + r")(?![0-9A-Za-z_])"
```

### `u122.H6_hold_beats_closure`

The hold is checked before closure, so a closed held card is not Done

- File: `scripts/board.py`
- Source: `u122.json`, row `H6_hold_beats_closure`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[3-In Progress]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[3-In review]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[6-In Progress]`
  - `tests/test_board_status.py::test_a_closed_card_is_done_whatever_it_held[6-In review]`

Old text:

```
    if node["closed"]:
        return "Done"
    if current in UNDERWAY:
```

New text:

```
    if current in UNDERWAY:
        return current
    if node["closed"]:
        return "Done"
    if False:
```

### `u148.C4_only_none_refused`

only a missing count is refused, a count that is not a number falls through

- File: `scripts/board.py`
- Source: `u148.json`, row `C4_only_none_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_a_read_short_of_its_count_or_with_none_is_refused[options3-load_issues-no count to check it against]`

Old text:

```
    if not isinstance(total, int):
```

New text:

```
    if total is None:
```

### `u148.W2_whole_off`

whole checks nothing

- File: `scripts/board.py`
- Source: `u148.json`, row `W2_whole_off`
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
    if False:
```

### `u151.N1_number_filter_dropped`

a card on another project of the same owner counts as this board's

- File: `scripts/board.py`
- Source: `u151.json`, row `N1_number_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_only_this_owners_project_is_the_board_whatever_the_case`

Old text:

```
                if str(project.get("number")) != PROJECT_NUMBER:
                    continue

```

New text:

```
                pass

```

### `u151.X4_unseen_project_trusted`

a project the token cannot see is not refused

- File: `scripts/board.py`
- Source: `u151.json`, row `X4_unseen_project_trusted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cost.py::test_a_project_the_token_cannot_read_whole_is_refused_by_name[gh-Fail-cannot be read with this token]`
  - `tests/test_board_cost.py::test_next_asks_for_the_project_before_trusting_an_empty_card_read`

Old text:

```
    if not project:
        raise Fail(
```

New text:

```
    if False:
        raise Fail(
```

### `u203.M1_no_opening_span`

comment_heading: never take an opening emphasised span, so **Brainstorm.** One question waits reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M1_no_opening_span`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[set-aside-## Started@s+4; **Needs the machine.** It reads the live library.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[waiting-on-phillip-comments21]`
  - `tests/test_board_cloud.py::test_a_known_heading_reads_through_trailing_punctuation_and_emphasis`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[**Brainstorm**.One question waits-brainstorm]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[**Question for Phillip**?Which-question for phillip]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[text5-brainstorm]`

Old text:

```
        span = _OPENING_EMPHASIS.match(text)
```

New text:

```
        span = None
```

### `u203.M9_no_comma_cut`

_HEADING_END: drop the comma cut, so Started, 2026-10-13. reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M9_no_comma_cut`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[**Brainstorm, round 2.**-brainstorm]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Started, 2026-10-13.-started]`

Old text:

```
_HEADING_END = re.compile(r"[:,]|[.?!;\u2026](?=\s)")
```

New text:

```
_HEADING_END = re.compile(r"[:]|[.?!;\u2026](?=\s)")
```

### `u313.B6_refusal_exit_code`

_refuse: print the refusal and return 0, so a refused residuals command reads as done

- File: `scripts/board.py`
- Source: `u313.json`, row `B6_refusal_exit_code`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restart_and_residual_files.py`, `tests/test_board_residual_search.py`
- Collected: 55 against a baseline of 55
- Kills: 4 (killed)
- Killed:
  - `tests/test_board_residual_search.py::test_a_missing_ledger_is_refused_never_read_as_no_match`
  - `tests/test_board_residual_search.py::test_the_command_prints_hits_and_refuses_an_empty_search`
  - `tests/test_restart_and_residual_files.py::test_check_against_a_revision_refuses_a_removed_heading_and_a_changed_entry`
  - `tests/test_restart_and_residual_files.py::test_the_landing_refuses_off_main_and_behind_origin`

Old text:

```
    print(f"board: {message}", file=sys.stderr)
    return code
```

New text:

```
    print(f"board: {message}", file=sys.stderr)
    return 0
```

### `r83.D1_offer_defect`

R-348: acquire_one no longer asks the defect question after a failed offer

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D1_offer_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
- Kills: 8 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - one dead track never sinks the run
        raise_if_defect(exc)

```

New text:

```
    except Exception as exc:  # noqa: BLE001 - one dead track never sinks the run

```

### `u47-author.CODEC_refused_track_sinks_the_run`

Escalate a lossy landing to an adapter failure, the shape that raises an uncaught ValueError when a delisted track landed earlier in the same batch

- File: `src/cratekit/acquire/adapter.py`
- Source: `u47-author.json`, row `CODEC_refused_track_sinks_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_after_a_delisted_track_still_returns_a_contract_result`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`

Old text:

```
        return TrackResult(
            key=request.key,
            outcome=TrackOutcome.REFUSED_BY_POLICY,
            detail=str(exc),
            remedy=exc.remedy,
        )
```

New text:

```
        raise AdapterBroken(str(exc)) from exc
```

### `u176.C4_page_without_items_list`

_pages: a page holding no list of items ends the listing, so an unreadable page reads as an account holding nothing older

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C4_page_without_items_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 92 against a baseline of 92
- Kills: 4 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_page_holding_no_list_of_items_is_unavailable_never_the_end[empty]`
  - `tests/test_bandcamp.py::test_a_page_holding_no_list_of_items_is_unavailable_never_the_end[no-items]`
  - `tests/test_bandcamp.py::test_a_page_holding_no_list_of_items_is_unavailable_never_the_end[not-a-list]`
  - `tests/test_bandcamp.py::test_a_page_holding_no_list_of_items_is_unavailable_never_the_end[null]`

Old text:

```
        if not isinstance(items, list):
            # A page with no list at all is not the empty page that ends a
            # listing; read as one it would call every purchase absent.
            raise BandcampUnavailable(f"a page of {what} holds no list of items")
```

New text:

```
        if not isinstance(items, list):
            return
```

### `u176.V13_number_after_prefix`

number_in: the prefix is not required, so a number in the album title holds the wrong track

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V13_number_after_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_number_in_reads_after_the_release_prefix_only`

Old text:

```
    if not artist or not title or not name.startswith(prefix):
        return None
```

New text:

```
    if not artist or not title:
        return None
```

### `u176.V8_recorded_item_done`

handle_fetch: a purchase the record holds is fetched again when its item runs again

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V8_recorded_item_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_purchase_already_recorded_is_done_when_its_item_runs_again`

Old text:

```
    if item.item_id in fetched(cfg):
```

New text:

```
    if False:
```

### `u177.B6_frozen_label`

frozen_release: freeze no label, so the worker tags nothing

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B6_frozen_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 8 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`

Old text:

```
        "label": planned.label.name if planned.label is not None else None,

```

New text:

```
        "label": None,

```

### `u205.C1_park_wrapped_as_outage`

app client: the gate's park raised inside the transport is wrapped as an outage and retried into the cooldown

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C1_park_wrapped_as_outage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_the_gates_park_raised_inside_the_app_transport_passes_through_as_itself`

Old text:

```
        except CratekitError:
            raise
        except Exception as exc:  # noqa: BLE001 - classified, never swallowed
```

New text:

```
        except Exception as exc:  # noqa: BLE001 - classified, never swallowed
```

### `u205.C9_names_not_included`

app client: the reads do not ask for the names, so every release of several reads as unreadable

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C9_names_not_included`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_the_lookup_asks_the_isrc_in_the_accounts_own_country_with_the_names_included`

Old text:

```
INCLUDE = "artists,albums"
```

New text:

```
INCLUDE = "albums"
```

### `r668-a.M9_other_verbs_job_read`

another verb's job payload is read as a frozen download list

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M9_other_verbs_job_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_another_verbs_job_is_not_read_as_a_frozen_download_list`

Old text:

```
    if named is None or job.handler_key != handler_key:
```

New text:

```
    if named is None:
```

### `u169.A5_warning_names_failed_items`

declined_warnings: name every item with a cause, failed ones included (unreachable through the verb, which refuses a failed job before its warnings; killed at the function)

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A5_warning_names_failed_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`

Old text:

```
        if item.state is not jobs.ItemState.SKIPPED or item.cause is None:
```

New text:

```
        if item.cause is None:
```

### `u54-acquisition-worker.G17_paced_sleep_bound`

Let the pool bind its own definition time sleep instead of the one the frozen configuration paces

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G17_paced_sleep_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load`

Old text:

```
    run = download.acquire_paced(adapter, (request,), sleep=_SLEEP)
```

New text:

```
    run = download.acquire_paced(adapter, (request,))
```

### `u54-acquisition-worker.G8_park_on_block`

Read a parked run as an ordinary result, so the driver claims the next item into a provider block

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G8_park_on_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`

Old text:

```
    if run.parked is not None:
        raise jobs.Parked(run.parked)

```

New text:

```
(empty)
```

### `u80.F13_rejected_searched_again`

A rejected row is searched and offered again

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F13_rejected_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_rejected_row_is_not_searched_again_and_says_so`

Old text:

```
    if held.verdict is review.Verdict.REJECTED:
        return Proposal(
```

New text:

```
    if held.verdict is review.Verdict.REJECTED:
        return None
        return Proposal(
```

### `u80.F7_mix_boundary`

An upload exactly at the mix length is demoted as a mix

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F7_mix_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_long_mix_is_demoted_below_the_track_it_names`

Old text:

```
    if hit.duration is not None and hit.duration > LIKELY_MIX_SECONDS:
```

New text:

```
    if hit.duration is not None and hit.duration >= LIKELY_MIX_SECONDS:
```

### `r289-b.C3_fallback_queue_call_site`

Drop the sweep on the fallback fetch queue path

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r289-b.json`, row `C3_fallback_queue_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_this_verb_sweeps_the_staging_tree_it_shares_with_the_download_verb`

Old text:

```
        acquire_cli.sweep_staging(Path(cfg.paths.download_staging), store)

```

New text:

```
(empty)
```

### `u81-fetch-a.W3_host_half`

The web address check keeps only its scheme half, so an address with no host is handed to the tool

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W3_host_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_an_accepted_option_that_is_not_a_web_address_is_never_handed_to_the_tool[https://]`

Old text:

```
    if where.scheme not in ("http", "https") or not where.netloc:
```

New text:

```
    if where.scheme not in ("http", "https"):
```

### `u81-fetch-b.Q5_owned_row_fetched`

Existing guard, moved into missing_rows: a row the library holds is not counted owned and is fetched

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-b.json`, row `Q5_owned_row_fetched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_fallback.py`
- Collected: 72 against a baseline of 72
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_an_owned_row_is_never_searched`
  - `tests/test_acquire_fallback.py::test_no_binary_is_needed_when_nothing_is_searched`
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`

Old text:

```
        if one.state is match.MatchState.MATCHED:
            counts["owned"] += 1
```

New text:

```
        if False:
            counts["owned"] += 1
```

### `r1016.M5_not_a_page_check_dropped`

An answer that is not a page is no longer refused by name and escapes as a bare KeyError or TypeError

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M5_not_a_page_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 793 against a baseline of 793
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[a-list]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[an-error-body]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[items-null]`

Old text:

```
        if not isinstance(page, dict) or not isinstance(page.get("items"), list):
```

New text:

```
        if False:
```

### `r878-a.A12_parse_retried`

paginate_cursor: parse each item once with no retry, so a rate limited playlist read refuses the verb

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A12_parse_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_parse_that_fails_transiently_is_retried_alone_without_refetching_the_page`

Old text:

```
            item = fetch_with_retry(lambda _l, _o, raw=raw: parse(raw), limit=0, offset=0, **retry)
```

New text:

```
            item = parse(raw)
```

### `r878-a.A9_cursor_advances`

paginate_cursor: never send the cursor the last response carried, so every request reads the first page

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A9_cursor_advances`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 141 against a baseline of 141
- Kills: 14 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_cursor_that_never_changes_spends_the_budget_and_refuses`
  - `tests/test_adapter_listing.py::test_a_folder_holding_a_folder_keeps_only_its_playlists`
  - `tests/test_adapter_listing.py::test_a_folder_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_a_folder_served_on_two_pages_is_returned_once`
  - `tests/test_adapter_listing.py::test_a_folders_playlists_are_walked_by_cursor_through_the_folders_own_parser`
  - `tests/test_adapter_listing.py::test_a_transient_failure_retries_the_same_cursor_and_not_the_first_page`
  - `tests/test_adapter_listing.py::test_a_walk_that_collects_fewer_than_the_declared_count_refuses`
  - `tests/test_adapter_listing.py::test_an_empty_page_ends_the_walk_even_when_it_carries_a_cursor`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_adapter_listing.py::test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset`
  - `tests/test_adapter_listing.py::test_the_root_count_covers_playlists_too_so_folders_are_kept_after_counting`
  - `tests/test_adapter_listing.py::test_the_root_folders_are_walked_by_cursor_past_an_endpoint_that_ignores_offset`
  - `tests/test_label_playlists.py::test_a_folders_playlists_are_read_past_one_page_without_the_clients_lookup`
  - `tests/test_label_playlists.py::test_the_root_folders_are_read_past_one_page`

Old text:

```
        cursor = str(following)
```

New text:

```
        pass
```

### `r887-a.K3_count_kept_not_served`

paginate_cursor: compare the kept items, not every served item, with the declared total, which is R-878's refusal on every real account

- File: `src/cratekit/acquire/listing.py`
- Source: `r887-a.json`, row `K3_count_kept_not_served`
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
    counted = len(served) + unkeyed
```

New text:

```
    counted = len(items)
```

### `u65.B5_artist_releases_back_to_the_short_page`

a label catalogue ends at the first short page, which is the core job done wrong

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B5_artist_releases_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/modules/test_labels.py`
- Collected: 265 against a baseline of 265
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_an_artist_release_listing_reads_to_the_end_across_both_methods`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`

Old text:

```
    "artist_releases": StopRule.EMPTY_PAGE,
```

New text:

```
    "artist_releases": StopRule.SHORT_PAGE,
```

### `u65.E1_the_shape_helper_ignores_the_rule_table`

every shape gets one hard coded rule again, which is R-383's own shape

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E1_the_shape_helper_ignores_the_rule_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 198 against a baseline of 198
- Kills: 28 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_client_whose_request_rejects_the_arguments_refuses_by_name_unslept`
  - `tests/test_adapter_listing.py::test_a_cursor_that_never_changes_spends_the_budget_and_refuses`
  - `tests/test_adapter_listing.py::test_a_folder_holding_a_folder_keeps_only_its_playlists`
  - `tests/test_adapter_listing.py::test_a_folder_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_a_folder_served_on_two_pages_is_returned_once`
  - `tests/test_adapter_listing.py::test_a_folders_playlists_are_walked_by_cursor_through_the_folders_own_parser`
  - `tests/test_adapter_listing.py::test_a_parse_that_fails_transiently_is_retried_alone_without_refetching_the_page`
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[a-list]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[items-null]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[no-items-no-count]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[nothing]`
  - `tests/test_adapter_listing.py::test_a_response_with_a_count_and_no_items_is_an_empty_listing`
  - `tests/test_adapter_listing.py::test_a_response_with_no_cursor_ends_the_walk`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        "stop": STOP_RULES[name],
```

New text:

```
        "stop": StopRule.EMPTY_PAGE,
```

### `u265.M8_other_scorer`

_approximate: score the sorted forms with WRatio instead of ratio, so scores and the floor's cut move

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M8_other_scorer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2712 against a baseline of 2712
- Kills: 25 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        scorer=fuzz.ratio,
```

New text:

```
        scorer=fuzz.WRatio,
```

### `u213.M4_first_group_keeps_brackets`

split_version: keep the brackets on a title written wholly in them

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u213.json`, row `M4_first_group_keeps_brackets`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 726 against a baseline of 726
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_a_set_aside_track_names_the_half_the_reader_names`
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
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[]-expected7]`

Old text:

```
            remaining = inside
            break
```

New text:

```
            remaining = found.group(0).strip()
            break
```

### `u261.W2_changed_session_skipped`

write_back: read any encodable session as unchanged, so a refreshed token is never stored (the merge blocker the card names)

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W2_changed_session_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 485 against a baseline of 485
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_refreshed_session_goes_back_to_the_keychain`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refreshed_session_is_written_once_through_the_index`
  - `tests/test_provider_session_hold.py::test_a_session_the_tool_changed_is_written_back_from_the_scope`
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        if unchanged is not None and unchanged == _canonical(stored):
```

New text:

```
        if unchanged is not None:
```

### `r703-a.V4_no_escalation`

a carried exception is no longer judged for a dead session or a defect

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V4_no_escalation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_a_session_the_tool_saw_rejected_is_an_invocation_auth_failure`

Old text:

```
        if not ok and isinstance(cause, BaseException):
            raise_if_session_dead(cause)

```

New text:

```
(empty)
```

### `r703-b.R2_everything_is_the_provider`

describe_cause calls the tool's own control flow the provider's answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `R2_everything_is_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 276 against a baseline of 276
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_tools_own_control_flow_is_not_called_the_providers_answer`

Old text:

```
    if isinstance(cause, _provider_errors()):
```

New text:

```
    if True:
```

### `u47-author.CODEC_no_refusal`

Accept whatever landed, which is the state the product shipped in from July: the rule enforced at the setting and never at the file

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_lossy_landing_after_a_delisted_track_still_returns_a_contract_result`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_is_refused_and_the_refusal_names_the_codec`
  - `tests/test_adapter_contract.py::test_a_lossy_landing_refuses_the_track_and_lets_the_run_continue`
  - `tests/test_adapter_contract.py::test_a_refused_file_is_left_where_it_landed`

Old text:

```
    if not lossless:
        raise LosslessRefused(
            f"the provider was asked for lossless audio and the file that landed "
            f"for {key} is {name}; it is at {path}"
        )
```

New text:

```
(empty)
```

### `u47-author.R196_absent_marker_reads_as_pkce`

Default a missing is_pkce to True, so a legacy device-flow token is read as a PKCE one

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_absent_marker_reads_as_pkce`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 202 against a baseline of 202
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_only_a_stored_pkce_session_is_used[stored2-True-True]`

Old text:

```
    if not bool(getattr(stored, "is_pkce", False)):
```

New text:

```
    if not bool(getattr(stored, "is_pkce", True)):
```

### `u47-author.R197_drop_progress_overall`

Drop progress_overall from the downloader construction

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_drop_progress_overall`
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
            progress_overall=progress_overall,

```

New text:

```
(empty)
```

### `u254.M01_mark_validates_record`

mark_applied: drop the reader's field rules on the record before it is written, so a record the reader refuses lands

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M01_mark_validates_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`

Old text:

```
    _record_from(
        entry.to_json(),
        path=path,
        where=f"was refused a record for the entry {entry.entry_id!r}, one",
    )
```

New text:

```
    pass
```

### `u254.M10_torn_needs_terminated_tail`

_read_journal: read a damaged last whole line as torn even when an unterminated line follows it

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M10_torn_needs_terminated_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[two torn lines at the end]`

Old text:

```
            if index == len(body) - 1 and whole:
```

New text:

```
            if index == len(body) - 1:
```

### `u254.M18_remark_first_wins`

_read_journal: fold a re-mark first one wins, unlike the document's writer

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M18_remark_first_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`

Old text:

```
        folded[record.entry_id] = record
```

New text:

```
        folded.setdefault(record.entry_id, record)
```

### `r722.A1_gate_drops_tally`

The approval gate's facts omit the reading tally

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r722.json`, row `A1_gate_drops_tally`
- Moved: the gate's facts are now read through the _FACTS key list; dropping energy from it is dropping the energy line from the gate document
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`

Old text:

```
    "counts",
    "energy",

```

New text:

```
    "counts",

```

### `u165.A2_refuse_unplaced_called`

file_plan: skip the unplaced refusal before the ledger is marked

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u165.json`, row `A2_refuse_unplaced_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_filing.py`, `tests/test_intake_land_native.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_track_the_tree_write_could_not_place_is_never_marked_applied`

Old text:

```
    refuse_unplaced(membership)

```

New text:

```
    pass

```

### `u55-collection-reader.R10_apply_zero_item_refusal`

The apply queues a job with one item over a plan that can place nothing

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R10_apply_zero_item_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`

Old text:

```
    if not applicable:
```

New text:

```
    if False:
```

### `u956.O17_gate_hides_outside`

apply_cli _FACTS: leave outside_root off the gate, so adopt.apply.approve never names the rows left out

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u956.json`, row `O17_gate_hides_outside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 72 against a baseline of 72
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`

Old text:

```
    "outside_root",

```

New text:

```
(empty)
```

### `u55-collection-reader.R3_soft_delete_marker`

R-186's exact defect: default the tombstone marker instead of reading it

- File: `src/cratekit/adopt/collection.py`
- Source: `u55-collection-reader.json`, row `R3_soft_delete_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_collection.py::test_a_row_that_cannot_report_the_marker_refuses_rather_than_defaulting`

Old text:

```
            deleted=trees.soft_delete_marker(row),
```

New text:

```
            deleted=bool(getattr(row, "rb_local_deleted", False)),
```

### `r780-a.A4_excluded_track_moved`

a track whose file the census could not read is moved on the reading its row happens to carry

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A4_excluded_track_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[excluded-in-two-bands]`

Old text:

```
    elif entry.disposition is Disposition.EXCLUDED or entry.energy is None or not target:
```

New text:

```
    elif entry.energy is None or not target:
```

### `u118-c.M10_no_reading_leaves_split`

A Soul track with no reading is left in R&B rather than moved to Soul Unsorted

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M10_no_reading_leaves_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`
- Collected: 102 against a baseline of 102
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_with_no_reading_leaves_r_and_b_for_soul_unsorted`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`

Old text:

```
        return "" if set(stale) <= routing.left_only(declared, entry.bucket) else LEFT_NO_READING
```

New text:

```
        former = {place.id for _declarer, place in routing.former_places(declared, entry.bucket)}
        return "" if set(stale) <= former else LEFT_NO_READING
```

### `u340.R27_move_split_kept`

held_in: keep no split place for the other entry, so adopt move takes Soul with R&B out of R&B and the worker reads the band as left (B1, round two)

- File: `src/cratekit/adopt/move.py`
- Source: `u340.json`, row `R27_move_split_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_adoption.py`, `tests/test_adopt_move.py`, `tests/test_adopt_split_place.py`
- Collected: 814 against a baseline of 814
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[rnb]`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[rnb-soul]`
  - `tests/test_second_genre.py::test_a_split_pair_is_filed_into_both_and_never_moved_out_of_either[soul-rnb]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[rnb-soul]`
  - `tests/test_second_genre.py::test_an_energy_change_moves_a_split_pair_in_both_and_the_worker_agrees[soul-rnb]`

Old text:

```
    return frozenset(held - kept_beside(declared, bucket, elsewhere))
```

New text:

```
    return frozenset(held)
```

### `r780-b.B5_verdicts_not_handed_to_the_worker`

the worker asks the plan's rule with no refused bucket, so a move approved before a verdict landed is performed into the refused folder

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r780-b.json`, row `B5_verdicts_not_handed_to_the_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_verdict_on_another_bucket_keeps_the_tree_path_out_of_its_folder`

Old text:

```
    refused = move_engine.refused_buckets(current.entries)
```

New text:

```
    refused = frozenset()
```

### `r788-c.L4_renamed_membership_unseen`

vocals_from: nobody is held under another name only, so a track in a renamed vocal playlist with a named one beside it is added to the named one too

- File: `src/cratekit/adopt/placements.py`
- Source: `r788-c.json`, row `L4_renamed_membership_unseen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_renamed_vocal_playlist_is_found_through_its_recorded_node_and_says_so`
  - `tests/test_adopt_vocals.py::test_a_track_held_under_both_names_is_not_held_under_another_name_only`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
        if under_another:
            unnamed[bucket.id] = frozenset(under_another)
```

New text:

```
        if False:
            unnamed[bucket.id] = frozenset(under_another)
```

### `r1965.R01_manual_class_beside`

derived_classes: admit a manual class (Candy), so the move removes it

- File: `src/cratekit/adopt/plan.py`
- Source: `r1965.json`, row `R01_manual_class_beside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_set_move.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`, `tests/test_tag_set.py`, `tests/test_genre_favorites.py`
- Collected: 432 against a baseline of 432
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_no_additive_class_of_the_vocal_identifier_is_no_vocal_sub`
  - `tests/test_tag_set_move.py::test_a_candy_membership_added_after_the_approval_keeps_the_favorites_and_the_job_finishes`
  - `tests/test_tag_set_move.py::test_a_folder_holding_the_track_only_beside_the_band_still_reads_its_other_playlists`
  - `tests/test_tag_set_move.py::test_a_manual_sub_is_never_removed_and_keeps_the_old_folders_favorites`
  - `tests/test_tag_set_move.py::test_a_place_another_bucket_declares_names_no_folder_of_the_declarer`
  - `tests/test_tag_set_move.py::test_the_reader_files_each_place_beside_the_band_and_the_folders_other_playlists_apart`
  - `tests/test_tag_set_move.py::test_the_shipped_places_beside_a_band_are_the_two_derived_classes_and_the_genre_subs`

Old text:

```
        if not entry.additive:
            continue
        others = tuple(other for other in declared.sub_classes if other is not entry)
        # The loader's own list of what a bucket's folder holds, without this class.
        ids, displays = taxonomy.live_places(declared.bucket(bucket_id), declared.energy, others)
        if entry.id not in ids
```

New text:

```
        others = tuple(other for other in declared.sub_classes if other is not entry)
        # The loader's own list of what a bucket's folder holds, without this class.
        ids, displays = taxonomy.live_places(declared.bucket(bucket_id), declared.energy, others)
        if entry.id not in ids
```

### `r722.P7_tally_counts_excluded`

The tally counts entries the census never opened

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P7_tally_counts_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 651 against a baseline of 651
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_an_excluded_file_is_never_opened_for_its_reading`

Old text:

```
            if entry.category is not Readability.READABLE:
                continue
            if entry.energy_unreadable:
```

New text:

```
            if entry.energy_unreadable:
```

### `r731-a.M08_digest_blind_to_unread`

the digest no longer covers whether the tree was read

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M08_digest_blind_to_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_tree_nobody_read_is_a_different_plan_from_a_tree_holding_nothing`

Old text:

```
                "placements": self.placements.state,
                "held_elsewhere": [
```

New text:

```
                "held_elsewhere": [
```

### `r788-a.P6_present_is_added`

vocal_place: a track already in the sub is planned as an addition and handed to the writer

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P6_present_is_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 8 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_keep_separate_verdict_withholds_the_vocal_addition_with_the_entry`
  - `tests/test_adopt_vocals.py::test_a_track_already_in_the_sub_is_counted_present_and_not_added`
  - `tests/test_adopt_vocals.py::test_a_withheld_track_already_in_its_vocal_sub_reads_present_and_is_not_digested`
  - `tests/test_adopt_vocals.py::test_only_the_additions_reach_the_writer_under_the_declared_names`
  - `tests/test_adopt_vocals.py::test_the_counts_add_up_to_the_tagged_tracks_of_the_census`
  - `tests/test_adopt_vocals.py::test_the_digest_does_not_move_when_the_membership_it_approved_lands`
  - `tests/test_adopt_vocals.py::test_the_document_names_the_count_and_lists_every_membership_it_may_write`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
    if vocals.sits(bucket, content_id):
        return VOCAL_PRESENT, sub
```

New text:

```
    if False:
        return VOCAL_PRESENT, sub
```

### `u23-round-8-independent.X10_entry_id_drops_the_sub`

Two pieces of work differing only by sub-folder share one identifier

- File: `src/cratekit/adopt/plan.py`
- Source: `u23-round-8-independent.json`, row `X10_entry_id_drops_the_sub`
- Moved: the identifier's document was joined onto one line by the formatter; the sub is dropped from it as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_entry_identifier_moves_when_the_destination_moves`

Old text:

```
        canonical_json({"tree": tree, "content": content_id, "bucket": bucket, "sub": sub}).encode()
```

New text:

```
        canonical_json({"tree": tree, "content": content_id, "bucket": bucket}).encode()
```

### `u23-round-8-independent.A2_at_risk_always_false`

Everything is at risk, so every re-run falls through to the digest

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A2_at_risk_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 6 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`
  - `tests/test_adoption.py::test_a_TAG_EDITED_IN_PLACE_is_still_accepted_because_nothing_is_at_risk`
  - `tests/test_adoption.py::test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    return False

```

### `u23-round-8-independent.C2_shape3_bypasses_the_check`

Shape 3, one file under two names, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `C2_shape3_bypasses_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`

Old text:

```
            # a different question and the shape below is where it is asked.
            return _settled_or_refused(

```

New text:

```
            # a different question and the shape below is where it is asked.
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=True
            )
            return _settled_or_refused(

```

### `u23-round-8-independent.G1_locked_passes_no_size`

_record_locked hands size_here=None, disabling every size gate below it

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `G1_locked_passes_no_size`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 613 against a baseline of 613
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
        size_here=_size_of(resolved),
```

New text:

```
        size_here=None,
```

### `r722.S2_track_drops_energy`

The scanned track does not carry the level it read

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S2_track_drops_energy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_changed_reading_moves_the_digest`
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_adoption_lands_a_track_where_the_routing_pass_would`
  - `tests/test_adopt_energy.py::test_the_approval_gate_shows_the_reading_tally`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
            energy=energy,
            energy_unreadable=unreadable,
```

New text:

```
            energy_unreadable=unreadable,
```

### `u339-composites.C6_census_tombstone`

scan_rows: a tombstoned row is read as live by the census, the layer M6_tombstone_row's guard sits on (its composite)

- File: `src/cratekit/adopt/scan.py`
- Source: `u339-composites.json`, row `C6_census_tombstone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_behaviour_compare.py`, `tests/test_tag_backlog.py`, `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`
- Collected: 1016 against a baseline of 1016
- Kills: 49 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`
  - `tests/test_behaviour_compare.py::test_two_captures_of_one_commit_are_equal`
  - `tests/test_tag_backlog.py::test_a_catch_all_is_left_to_tag_retag`
  - `tests/test_tag_backlog.py::test_a_person_reads_the_backlog`
  - `tests/test_tag_backlog.py::test_a_row_lagging_its_file_is_served_exactly_when_tag_rows_would_write_it`
  - `tests/test_tag_backlog.py::test_a_row_with_no_genre_and_agreeing_neighbours_is_proposed_from_the_neighbours`
  - `tests/test_tag_backlog.py::test_a_row_with_nothing_beside_it_is_left_with_no_votes`
  - `tests/test_tag_backlog.py::test_a_word_neither_answer_takes_leaves_its_rows_with_the_refusal`
  - `tests/test_tag_backlog.py::test_a_word_with_one_answer_moves_only_the_rows_it_reaches`
  - `tests/test_tag_backlog.py::test_every_needs_genre_row_lands_in_exactly_one_cause_and_a_routed_row_in_none`
  - `tests/test_tag_backlog.py::test_off_taxonomy_words_are_grouped_across_spellings_and_ranked_by_rows`
  - `tests/test_tag_backlog.py::test_only_a_row_with_no_genre_is_asked_of_the_catalogue`
  - `tests/test_tag_backlog.py::test_the_campaign_lists_the_existing_verbs_in_order_and_the_projection`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        if row.deleted:
            continue
```

New text:

```
(empty)
```

### `u956.O4_outside_reads_missing`

scan_rows: name an outside row missing rather than outside-root, so the count and the gate say the file is gone when it is there

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O4_outside_reads_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 639 against a baseline of 639
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_a_row_mapped_outside_the_root_is_excluded_and_keeps_its_path`
  - `tests/test_adopt_outside_root.py::test_adopt_move_reads_the_same_disposition`
  - `tests/test_adopt_outside_root.py::test_adopt_scan_counts_each_sampler_row_outside_the_root`
  - `tests/test_adopt_outside_root.py::test_the_digest_moves_when_a_different_row_is_left_outside`
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`
  - `tests/test_adopt_outside_root.py::test_the_plan_counts_and_names_every_row_it_leaves_outside`

Old text:

```
            readability = Readability.OUTSIDE_ROOT
```

New text:

```
            readability = Readability.MISSING
```

### `u55-collection-reader.R9_scan_zero_item_refusal`

The scan queues a job over an empty library, which drives to SUCCEEDED having read nothing

- File: `src/cratekit/adopt/scan_cli.py`
- Source: `u55-collection-reader.json`, row `R9_scan_zero_item_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[False]`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[True]`

Old text:

```
    if not live:
```

New text:

```
    if False:
```

### `u223.M1_keep_intent`

staged_path: clear the rename intent with everything else, the shipped behaviour

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M1_keep_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
```

New text:

```
                entry.name == "never-kept.json"
                and entry.is_file()
```

### `u223.M5_discard_keeps_report`

discard_rename_evidence: drop the intent only, round one's residual

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M5_discard_keeps_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (RENAME_INTENT_FILENAME,):
```

### `u90-a.A2_upper_bound_strict`

The range guard's upper bound made strict, so a cut of 100 is refused

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A2_upper_bound_strict`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if not VOCAL_SCORE_MIN <= cut < VOCAL_SCORE_MAX:
```

### `u90-b.B4_date_field_dropped`

The hand cut's set_on date field no longer written

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B4_date_field_dropped`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`

Old text:

```
note=f"set by hand on {today}", set_on=today
```

New text:

```
note=f"set by hand on {today}"
```

### `u94-a.S2_floor_off_by_one`

analyze_calibrate: move the floor one below MIN_CALIBRATION_TRACKS, a nearby value, so a sample of nine is accepted

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S2_floor_off_by_one`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra0]`
  - `tests/test_analysis_workers.py::test_a_sample_below_the_fit_floor_is_refused_before_measuring[extra1]`

Old text:

```
    if sample < MIN_CALIBRATION_TRACKS:
        return _calibrate_refusal(
```

New text:

```
    if sample < MIN_CALIBRATION_TRACKS - 1:
        return _calibrate_refusal(
```

### `u94-b.W3_accepted_reads_ok`

_partial_accepted: report an accepted partial as ok, so it reads as the library wide fit on the check row

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W3_accepted_reads_ok`
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
        "skipped",
        f"{what}; fitted anyway
```

New text:

```
        "ok",
        f"{what}; fitted anyway
```

### `u94-c.N3_sample_ignored`

analyze_calibrate: measure every walked track whatever --sample says, the unbounded run the brief rules out

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N3_sample_ignored`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 212 against a baseline of 212
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_sample_at_the_fit_floor_is_accepted`
  - `tests/test_analysis_workers.py::test_the_same_tree_gives_the_same_sample_twice`
  - `tests/test_analysis_workers.py::test_the_vocal_cut_reads_every_tagged_file_while_energy_reads_the_sample`

Old text:

```
    sampled = stride_sample(paths, sample)
```

New text:

```
    sampled = list(paths)
```

### `u192.A3_restamp_wrong_resume`

analyze_restamp: name the analyze run command as the one that resumes an interrupted restamp

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A3_restamp_wrong_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    return _settle(ctx, cfg, job, restamp_argv(job))
```

New text:

```
    return _settle(ctx, cfg, job, analyze_argv(job))
```

### `u241.M19_failed_run_does_not_say_its_pool`

_resume: a run that failed or was stopped leaves without its pool line

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M19_failed_run_does_not_say_its_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_analysis_ahead.py::test_an_interrupt_during_a_run_ahead_ends_the_workers_and_the_resume_finishes`
  - `tests/test_analysis_ahead.py::test_an_unreadable_calibration_is_each_items_refusal_and_opens_no_pool`

Old text:

```
                if pooled is None:
                    raise
                raise _with_pool(failed, pooled) from failed

```

New text:

```
                raise

```

### `u343.M01_finalize_no_mark`

_finalize: drop the mark from the write, so a measured file reads as unmeasured and every resume measures it again

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M01_finalize_no_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analysis.py`, `tests/test_vocals_cli.py`, `tests/test_restamp_scored_by.py`, `tests/test_analysis_ahead.py`
- Collected: 534 against a baseline of 534
- Kills: 9 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_pooled_run_leaves_exactly_what_the_serial_run_leaves`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_analysis_workers.py::test_an_uncalibrated_library_writes_no_energy_tag_and_routes_to_the_sink`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_the_tail_over_the_real_verbs_leaves_every_title_headless_for_the_landing`

Old text:

```
        run.MARK_FIELD: run.MARK_VALUE,
    }
```

New text:

```
    }
```

### `u343.M25_report_renamed_to_back`

handle_run: report a renamed_to again, a rename the run never makes

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M25_report_renamed_to_back`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
            "path": str(path),
            "status": "analyzed",
```

New text:

```
            "path": str(path),
            "renamed_to": path.name,
            "status": "analyzed",
```

### `u263.D10_first_stream`

_ffmpeg_samples: drop the map to the first audio stream

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D10_first_stream`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_first_audio_stream_is_taken_even_when_another_is_the_default`

Old text:

```
        "-map", "0:a:0",

```

New text:

```
(empty)
```

### `u264.M13_float64_halving`

_mean_of_two: add and halve in float64 and round once, so a finite pair whose float32 sum overflows mixes to a finite value

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M13_float64_halving`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0-right5-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-3e+38--3e+38-ff800000-ff800000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[3e+38-3e+38-7f800000-7f800000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left4-0.0-80000000-00000000]`

Old text:

```
    out = np.add(stereo[0], stereo[1])
    # numpy's reduction starts from plus zero: minus zero plus minus zero is
    # minus zero here and plus zero in the mean, and no other sum changes.
    out += out.dtype.type(0)
    out /= out.dtype.type(2)
```

New text:

```
    out = ((stereo[0].astype(np.float64) + stereo[1]) / 2).astype(stereo.dtype)
    out += out.dtype.type(0)
```

### `u344.M1_head_bypasses_restamp_measure`

energy_from_path: measure through features_from_path directly, not the restamp's energy.measure, so a bound extractor is not the head's

- File: `src/cratekit/analysis/detect.py`
- Source: `u344.json`, row `M1_head_bypasses_restamp_measure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_warm.py`, `tests/test_energy_one_measure_librosa.py`, `tests/test_analysis_ahead.py`
- Collected: 495 against a baseline of 495
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_detector_names_why_energy_is_what_it_is`

Old text:

```
    features = energy.measure(Path(path))

```

New text:

```
    features = energy.features_from_path(Path(path))

```

### `u327.A12_agreeing_title_left_whole`

plan_row: drop the agreeing title return, so a blank key tag beside an agreeing head is filled

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A12_agreeing_title_left_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 7 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_a_missing_key_never_stops_the_tempo_nor_a_missing_tempo_the_key`
  - `tests/test_analyze_adopt.py::test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_a_second_run_plans_nothing_still_asks_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_the_old_values_are_on_disk_before_the_first_file_is_written`
  - `tests/test_analyze_adopt.py::test_the_plan_shows_each_row_before_and_after_with_its_key_relation_and_tempo`
  - `tests/test_analyze_adopt.py::test_the_record_keeps_every_surface_s_old_value_for_a_restore`

Old text:

```
    if new_title == title and new_tag == tag_title:
```

New text:

```
    if False:
```

### `u327.A20_judge_title`

judge: never read the title back, so a row that does not carry its new title passes

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A20_judge_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_the_read_back_names_a_title_not_carried_and_a_column_moved`

Old text:

```
        if str(now.get("Title") or "") != item.new_title:
```

New text:

```
        if False:
```

### `u342.P10_leave_holds_a_stamp`

plan_adopt: let --leave hold out only a corrected row, so a stamped row named by it is written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P10_leave_holds_a_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`

Old text:

```
        if item.action in WRITING and content_id in held:
```

New text:

```
        if item.action == ADOPT and content_id in held:
```

### `u342.P7_tag_must_be_the_title`

_tag_after: stamp a headless row's file whatever its title tag says

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P7_tag_must_be_the_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_row_whose_tag_carries_another_title_is_left`
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`

Old text:

```
        return new_title if tag_title in (title, new_title) else None
```

New text:

```
        return new_title
```

### `u241.M11_cost_from_the_cheapest_track`

light.costliest: the cheapest track sets the worker's cost

- File: `src/cratekit/analysis/light.py`
- Source: `u241.json`, row `M11_cost_from_the_cheapest_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 271 against a baseline of 271
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[64]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[6]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[8]`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[12]`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[8]`

Old text:

```
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)

```

New text:

```
    return min((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)

```

### `u275.M7_cheapest_track_sets_the_cost`

costliest: take the cheapest track's cost, so a folder's longest track no longer sets the plan

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M7_cheapest_track_sets_the_cost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 553 against a baseline of 553
- Kills: 13 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_eight_gigabytes_free_over_the_six_mac_tracks_is_one_worker`
  - `tests/test_analysis_ahead.py::test_one_high_rate_file_sets_the_batchs_cost_though_it_is_not_the_longest`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[12]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[18]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[24]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[32]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[4]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[64]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[6]`
  - `tests/test_analysis_ahead.py::test_six_mac_tracks_plan_no_more_workers_than_memory_holds[8]`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[12]`
  - `tests/test_analysis_ahead.py::test_the_light_plan_is_never_wider_than_before_u275[8]`

Old text:

```
    return max((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)
```

New text:

```
    return min((cost_of(path) for path in paths), default=LIGHT_BASE_BYTES)
```

### `sitting3.G13_padded_frames_kept`

Count the frames the padding added, so a short clip's presence is diluted

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G13_padded_frames_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`

Old text:

```
    if padded > width and vocals.size:

```

New text:

```
    if False:

```

### `sitting3.G9_tail_sent_alone`

Send a short tail to the network as its own piece, the R-371 defect

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G9_tail_sent_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_at_the_real_chunk_size_only_a_tail_under_the_floor_is_folded`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces[a-lone-short-clip-is-padded-to-the-floor]`
  - `tests/test_analysis.py::test_chunked_inference_walks_the_signal_in_pieces[a-short-tail-is-folded]`
  - `tests/test_analysis.py::test_padded_frames_are_trimmed_so_a_short_clip_scores_on_its_own_length`
  - `tests/test_analysis.py::test_the_unchunked_path_pads_a_short_signal_too`

Old text:

```
    slices = _without_a_short_tail(slices, floor=floor)

```

New text:

```
    slices = list(slices)

```

### `u58-workers-and-wav.W4_model_guard`

Drop the guard for a model that did not load

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W4_model_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 176 against a baseline of 176
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_model_that_did_not_load_is_a_named_absence`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`

Old text:

```
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
(empty)
```

### `u92-author.G5_guard_after_the_load`

Move the guard behind the model load, the brief's literal reading, which this unit did not take

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G5_guard_after_the_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 230 against a baseline of 230
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)

```

New text:

```
    model = _load()
    if model is None:
        return _inactive(result, REASON_MODEL_UNAVAILABLE)
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

### `r221-a.W1_rehearsal_never_said`

The warning is never carried, which is the exact state the ledger entry describes

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W1_rehearsal_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return ()
```

### `r221-b.R1_refusal_is_its_own_cause`

Raise the result from the original unconditionally, which is `raise exc from exc` on a real run and truncates the chain cause.classified walks. This is the defect the code review found

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `R1_refusal_is_its_own_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`

Old text:

```
    extended = _with_rehearsal_step(error, job)
    if extended is error:
        raise error
    raise extended from error
```

New text:

```
    raise _with_rehearsal_step(error, job) from error
```

### `r222-b.B4_rehearsal_is_a_twin`

Drop the rehearsal flag comparison, so an open rehearsal answers a request for a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B4_rehearsal_is_a_twin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_and_a_real_run_are_two_jobs`
  - `tests/test_backup_cli.py::test_the_emptied_flag_is_frozen_by_the_parser_and_rebuilt_by_the_resume`
  - `tests/test_backup_cli.py::test_the_frozen_payload_and_the_parser_agree_about_the_flag`

Old text:

```
        if bool((job.payload or {}).get(DRY_RUN)) != dry_run:
            continue
```

New text:

```
        if False:
            continue
```

### `r349-a.A1_failure_write`

Drop the failure path JSON write: raise the refusal without writing the outcome

- File: `src/cratekit/backup/cli.py`
- Source: `r349-a.json`, row `A1_failure_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
            raise _with_outcome_recorded(refusal, outcome, outcome_to)
```

New text:

```
            raise refusal
```

### `u45-round-1.C2_refusal_read_as_failure`

Widen the failed predicate to any portion that did not run, so a refused database portion reads as a failed transfer

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C2_refusal_read_as_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_fails_every_portion_by_name`
  - `tests/test_backup_cli.py::test_a_machine_with_no_rclone_refuses_by_name`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_portion_the_engine_refused_fails_rather_than_reporting_a_copy`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`

Old text:

```
        entry for entry in outcome.portions if not entry.ran and entry.refusal is None
```

New text:

```
        entry for entry in outcome.portions if not entry.ran
```

### `u45-round-1.Q3_resume_loses_the_job`

Drop --job from the resume argv, so the child queues a second backup instead of continuing the first

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `Q3_resume_loses_the_job`
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
    return [*argv, "--job", job.job_id]
```

New text:

```
    return list(argv)
```

### `u45-round-1.W6_rehearsal_becomes_a_real_run`

Ignore the frozen dry-run key, so a rehearsal transfers for real and publishes an age

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W6_rehearsal_becomes_a_real_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 6 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    dry_run = bool(payload.get(DRY_RUN))
```

New text:

```
    dry_run = False
```

### `u50-author.W6_fresh_config_in_the_handler`

Load the configuration in the handler rather than using the one frozen on the job (KTD9)

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `W6_fresh_config_in_the_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 19 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_says_which_kind_of_run_it_was[under-a-real-run-gains-no-rehearsal-step]`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_says_which_kind_of_run_it_was[under-a-rehearsal-says-so]`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_configuration_the_worker_runs_against_is_the_frozen_one`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        cfg=cfg,
        # RESOLVED AT CALL TIME, not left to the default, so a test can put a
        # stand-in in front of it. ``perform_backup``'s own default is bound when
        # this module is imported and cannot be reached any other way.
        runner=backup.subprocess_runner,
```

New text:

```
        cfg=_load(),
        runner=backup.subprocess_runner,
```

### `r924.D2_human_gets_none`

The dispatcher never hands a writer, so human output is silent again

- File: `src/cratekit/cli/__init__.py`
- Source: `r924.json`, row `D2_human_gets_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_human_fetch_runs_its_watcher`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
        if not as_json:
            context.progress = _progress_to(stderr)
```

New text:

```
        if False:
            context.progress = _progress_to(stderr)
```

### `u58-workers-and-wav.H1_run_unbound`

Drop the analyze.run binding from the handler table

- File: `src/cratekit/cli/handlers.py`
- Source: `u58-workers-and-wav.json`, row `H1_run_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 603 against a baseline of 603
- Kills: 36 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_calibrated_level_is_written_and_routes_to_a_band`
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_job_an_older_build_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - ... and 21 more, see the JSON sidecar

Old text:

```
    "analyze.run": "cratekit.analysis.cli:handle_run",

```

New text:

```
(empty)
```

### `u45-round-1.V3_marker_restored`

Put planned_in back, so the verb reads as unlanded and every conformance property stops arming against it

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u45-round-1.json`, row `V3_marker_restored`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4342 against a baseline of 4346
- Kills: 49 (collect-error)
- Note: collection changed: 4342 collected against a baseline of 4346. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`
  - `tests/test_backup_cli.py::test_a_backup_to_a_destination_nobody_is_backing_up_to_is_its_own_job`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        # Landed (U45).
```

New text:

```
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        planned_in="U35",
        # Landed (U45).
```

### `r925.R4_version_unsaid`

The human line drops a track's version

- File: `src/cratekit/cli/render.py`
- Source: `r925.json`, row `R4_version_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`

Old text:

```
        if row.get("version"):
            named += f" ({_one_line(row['version'])})"
```

New text:

```
        if False:
            named += f" ({_one_line(row['version'])})"
```

### `u247.M9_unmounted_guard_sample`

active_taxonomy.read_text: drop the unmounted volume refusal, a sample of the existing guard the memo sits behind

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `u247.json`, row `M9_unmounted_guard_sample`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
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

### `u260.E4_key_by_length_only`

to_cdj_jpeg_remembered: key on the length without the digest, so two pictures of one length share an encode

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E4_key_by_length_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_two_covers_sharing_a_long_header_are_encoded_apart`
  - `tests/test_album_cover_once.py::test_two_pictures_of_one_length_are_encoded_apart`

Old text:

```
    key = (hashlib.sha256(data).digest(), len(data), size, max_bytes)
```

New text:

```
    key = (b"", len(data), size, max_bytes)
```

### `u83-a.E1_baseline_flag`

The encoder emits a progressive JPEG, the kind a Pioneer player renders blank

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E1_baseline_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 3 (killed)
- Killed:
  - `tests/test_art.py::test_a_progressive_jpeg_input_comes_out_baseline`
  - `tests/test_art.py::test_a_progressive_rgba_png_comes_out_a_baseline_rgb_jpeg_under_the_cap`
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
quality=quality, optimize=True, progressive=False)
```

New text:

```
quality=quality, optimize=True, progressive=True)
```

### `u83-a.R1_flac_declared_dimensions`

The reader reports a FLAC picture's decoded size instead of what the block declares, hiding a zeroed block

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `R1_flac_declared_dimensions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_zeroed_flac_block_reads_as_zeroes_not_as_the_decoded_size`

Old text:

```
_picture(pic.mime, bytes(pic.data), (pic.width, pic.height, pic.depth))
```

New text:

```
_picture(pic.mime, bytes(pic.data), None)
```

### `u83-b.W3_progressive_guard`

The writer accepts a progressive JPEG

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W3_progressive_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_a_refused_picture_fails_and_leaves_the_file_untouched[progressive]`

Old text:

```
    if measured.progressive:
```

New text:

```
    if False:
```

### `u953.M20_held_key_not_moved`

record carries the held keys but never moves one to the new fact, so a full comparison is never recorded

- File: `src/cratekit/core/backup_facts.py`
- Source: `u953.json`, row `M20_held_key_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`
- Collected: 33 against a baseline of 33
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_damaged_full_comparison_entry_refuses_its_own_reader_and_no_other`
  - `tests/test_backup_comparison.py::test_a_record_a_few_minutes_ahead_is_zero_days_old_and_not_minus_one`
  - `tests/test_backup_comparison.py::test_doctor_refuses_a_full_comparison_recorded_ahead_of_now`
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
        if moved:
```

New text:

```
        if False:
```

### `r1313.N4_not_found_status_moved`

NOT_FOUND_STATUS: 410 rather than 404, so no 404 is a not found through the nearest status

- File: `src/cratekit/core/cause.py`
- Source: `r1313.json`, row `N4_not_found_status_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`
- Collected: 561 against a baseline of 561
- Kills: 19 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_transient_marker_wins_over_a_status_code`
  - `tests/test_adapter_contract.py::test_only_an_explicit_not_found_classifies_permanent[exc3]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[404]`
  - `tests/test_label_tidal_catalogue.py::test_a_404_status_is_gone_whatever_the_class_is_called`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
NOT_FOUND_STATUS = 404
```

New text:

```
NOT_FOUND_STATUS = 410
```

### `u254.C2_append_one_write`

append_durable_bytes: make one write call and drop what it did not take

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C2_append_one_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 962 against a baseline of 962
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

### `r290-author.J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J3_closed_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2532 against a baseline of 2532
- Kills: 109 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - ... and 94 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if False and not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `u298.H21_advance_refuses_empty`

advance: a job with no items is driven straight to succeeded

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H21_advance_refuses_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 131 against a baseline of 131
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.apply]`
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.scan]`
  - `tests/test_tag_workers.py::test_a_job_with_no_items_is_refused_rather_than_driven`

Old text:

```
    if job.is_open() and not items(store, job.job_id):
```

New text:

```
    if False:
```

### `u342.S3_stamp_refuses_a_trailing_head`

stamp_head: drop the refusal of a title carrying a head at its end, so it gets a second

- File: `src/cratekit/core/naming.py`
- Source: `u342.json`, row `S3_stamp_refuses_a_trailing_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_title_with_no_head_is_stamped_and_keeps_every_byte[a-head-at-the-end]`

Old text:

```
        or strip_trailing_head(name, template=template) != name

```

New text:

```
        or False

```

### `u205.G3_attach_drops_identity`

gate attach: the wrapped transport counts every call under the account whatever identity it was attached under

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G3_attach_drops_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 184 against a baseline of 184
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
            return self.call(lambda: original(method, url, *args, **kwargs), identity=identity)
```

New text:

```
            return self.call(lambda: original(method, url, *args, **kwargs), identity=ACCOUNT)
```

### `u329.P1_rb_changes_wrong_family`

rb_changes binds _writer to the session's accessor, so every _writer().name reads the wrong module

- File: `src/cratekit/core/rb_changes.py`
- Source: `u329.json`, row `P1_rb_changes_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_write_guard_completeness.py`, `tests/test_sync_removed.py`, `tests/test_adopt_move.py`, `tests/test_intake_land_native.py`
- Collected: 449 against a baseline of 449
- Kills: 201 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_doubled_membership_leaves_in_one_move`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_person_stopping_the_removals_is_an_interrupt_and_not_a_failure`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - `tests/test_adopt_move.py::test_a_removal_from_a_playlist_that_is_not_there_creates_none`
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`
  - `tests/test_adopt_move.py::test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal`
  - `tests/test_adopt_move.py::test_a_track_not_in_its_target_has_nothing_removed`
  - `tests/test_adopt_move.py::test_a_track_with_no_live_collection_row_is_skipped_whole`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`
  - `tests/test_adopt_move.py::test_an_admitted_commit_refuses_a_removed_collection_row_or_a_hard_delete`
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_an_ordinary_guarded_commit_refuses_a_removal_and_rolls_it_back`
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`
  - `tests/test_adopt_move.py::test_the_fingerprint_is_taken_after_each_commit_that_landed`
  - ... and 186 more, see the JSON sidecar

Old text:

```
from cratekit.core.rb_call_time import writer as _writer
```

New text:

```
from cratekit.core.session_call_time import session as _writer
```

### `r731-b.M21_sink_does_not_compete`

the no reading sub no longer competes with a band

- File: `src/cratekit/core/routing.py`
- Source: `r731-b.json`, row `M21_sink_does_not_compete`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 7 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_sub_class_is_removed_from_the_bands_by_identifier`
  - `tests/test_adopt_placements.py::test_a_track_holding_a_place_is_withheld_only_where_it_competes[band-whose-file-has-no-reading]`
  - `tests/test_adopt_placements.py::test_a_track_holding_a_place_is_withheld_only_where_it_competes[sink-whose-file-now-reads]`
  - `tests/test_adopt_placements.py::test_every_sub_routing_can_name_is_one_of_its_buckets_competing_subs`
  - `tests/test_adopt_placements.py::test_the_bands_and_the_no_reading_sub_compete_in_an_energy_bucket`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if taxonomy.energy.no_energy_sub is not None:
        found.add(taxonomy.energy.no_energy_sub.id)
    return Competing.BAND
```

New text:

```
    return Competing.BAND
```

### `u329.P7_session_holders_wrong_family`

session_holders binds _session to the writer's accessor, so every _session().name reads the wrong module

- File: `src/cratekit/core/session_holders.py`
- Source: `u329.json`, row `P7_session_holders_wrong_family`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`, `tests/test_doctor.py`, `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`
- Collected: 708 against a baseline of 708
- Kills: 81 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_nested_session_is_refused_rather_than_deadlocking`
  - `tests/test_adopt_apply_cli.py::test_a_second_run_holding_the_lock_rewrites_no_file`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_is_armed_on_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_analysis_watch_reaches_a_share_outside_the_library_root`
  - `tests/test_adopt_apply_cli.py::test_the_whole_loop_runs_with_the_library_lock_actually_held`
  - `tests/test_doctor.py::test_an_open_session_whose_process_is_gone_names_the_verb_that_ends_it`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_dead_holders_claim_is_cleared_and_the_refusal_named_it_first`
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[abort]`
  - ... and 66 more, see the JSON sidecar

Old text:

```
from cratekit.core.session_call_time import session as _session
```

New text:

```
from cratekit.core.rb_call_time import writer as _session
```

### `u250.M7_energy_word_reads_absent`

read_energy_checked: answer None for a stored energy that is not a number instead of raising, so a damaged file reads as untagged

- File: `src/cratekit/core/tags.py`
- Source: `u250.json`, row `M7_energy_word_reads_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_energy.py`, `tests/test_tags.py`, `tests/test_rebuild_one_open.py`, `tests/test_organize_mirror_edits_u227.py`
- Collected: 126 against a baseline of 126
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    if number is None:
        raise TagReadFailed(f"energylevel is not a number: {value!r}")
```

New text:

```
    if number is None:
        return None
```

### `r301.B1_shipped_month_unbounded`

The shipped budget carries no monthly bound, which is the tree before this unit

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `B1_shipped_month_unbounded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_hand_built_budget_bounds_the_run_and_the_shipped_one_bounds_the_month_too`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[identify]`
  - `tests/intake/test_workers.py::test_an_unconfigured_machine_meets_a_monthly_bound_before_the_first_call[set]`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[identify]`
  - `tests/intake/test_workers.py::test_the_configured_host_and_month_are_the_ones_every_paid_call_meets[set]`

Old text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=recognition.monthly_calls)
```

New text:

```
        return cls(per_run=MAX_CALLS_PER_RUN, monthly=None)
```

### `r706-a.A4_month_asked_of_one_run`

The month is asked about one run's worth rather than the whole set, so a set the month cannot afford spends its first part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A4_month_asked_of_one_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
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

### `r706-b.B5_chunks_count_the_first_part`

The walked grid is rebuilt from the first part only, so chunks and cached count one part

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B5_chunks_count_the_first_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_split_set_is_one_cached_plan_and_a_gap_meets_the_bound_on_what_is_owed`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
    offsets = tuple(offset for part in parts for offset in part)
```

New text:

```
    offsets = tuple(parts[0]) if parts else ()
```

### `r924.A7_kept_chunks_counted`

A chunk the cache answered speaks the counter as if it were paid

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A7_kept_chunks_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 78 against a baseline of 78
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

### `u103-a.A9_refresh_reads_nothing_kept`

Let a refreshing pass read the kept answers anyway

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A9_refresh_reads_nothing_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_refresh_reads_nothing_kept_and_lays_the_new_answers_over_the_document`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_nobody_recognised_is_an_honest_zero_that_says_what_it_cost`
  - `tests/intake/test_workers.py::test_refresh_pays_for_every_chunk_again_and_the_new_answers_replace_the_kept_ones`

Old text:

```
    kept = kept_in.read(plan) if plan is not None and not refresh else {}
```

New text:

```
    kept = kept_in.read(plan) if plan is not None else {}
```

### `u57-recognition-and-items.M4_transient_range_dropped`

The 2000s stop being transient, so a recording error ends the run as unclassified

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M4_transient_range_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
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

### `r431-b.B9_the_freeze_drops_the_field`

The intake freeze stops carrying several_artists, so the worker resolves from a track that never looked

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B9_the_freeze_drops_the_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
        "several_artists": row.several_artists,
```

New text:

```
(empty)
```

### `r706-c.C3_summary_ignores_the_payload`

The resume summary reports one part rather than reading the frozen count

- File: `src/cratekit/intake/cli.py`
- Source: `r706-c.json`, row `C3_summary_ignores_the_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
        "parts": int(payload.get(PARTS) or 1),
```

New text:

```
        "parts": 1,
```

### `u213.M11_unreadable_said_isrc`

Unreadable.said: name the track with no ISRC, so the backfill cannot find it by its code

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M11_unreadable_said_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
        return {"artist": self.artist, "title": self.title, "isrc": self.isrc}
```

New text:

```
        return {"artist": self.artist, "title": self.title, "isrc": ""}
```

### `u70.E1_missing_id_refused`

Existing: a provider row with no id is not refused by position, so a heart without one is queued under a blank key

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `E1_missing_id_refused`
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
        if row.origin != match.TEXT and False
```

### `r925.S3_no_write`

intake set writes no tracklist and says it wrote one

- File: `src/cratekit/intake/cli_identify.py`
- Source: `r925.json`, row `S3_no_write`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/intake/test_set_fetch.py`
- Collected: 108 against a baseline of 108
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`

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

### `u103-b.C9_refusal_counts_the_gap`

Let the unwritable tracklist refusal promise a free rerun over chunks that got no answer

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C9_refusal_counts_the_gap`
- Moved: the text moved whole from intake/cli.py to intake/cli_identify.py with its function (U307); the tests that killed it, test_the_unwritable_tracklist_refusal_does_not_promise_a_free_rerun_over_a_gap, were folded by the trim into test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept, both of its checks, carried whole
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_tracklist_that_cannot_be_written_refuses_and_says_the_answers_were_kept`

Old text:

```
        elif result.unreached:
```

New text:

```
        elif False:
```

### `r740-b.E2_average_bpm_nonzero`

existing guard sample: the intake row's AverageBpm literal becomes a tempo

- File: `src/cratekit/intake/collection_xml.py`
- Source: `r740-b.json`, row `E2_average_bpm_nonzero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_head.py`, `tests/test_landing.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_collection_xml.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 113 against a baseline of 113
- Kills: 16 (killed)
- Killed:
  - `tests/intake/test_collection_xml.py::test_average_bpm_is_gridless_inizio_no_tempo_child_and_the_bytes_crlf`
  - `tests/intake/test_pipeline.py::test_single_file_ingest_uses_no_network`
  - `tests/test_landing_head.py::test_a_second_landing_of_the_same_file_renders_the_same_name`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[a-provider-key-tag]`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[no-title-tag]`
  - `tests/test_landing_head.py::test_a_title_analyze_run_measured_lands_as_its_title_tag_gives_it_with_no_head[titled]`
  - `tests/test_landing_head.py::test_intake_file_names_its_track_from_the_same_head`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[01A - 112 - Ain't Gonna Hurt Nobody.flac-fields0-01A - 112 - Ain't Gonna Hurt Nobody-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields4-05B - 98 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[05B - 98 - Probe - Body.flac-fields5-05B - 98 - Body-8A]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[08A - 124 - [MP3] Body.flac-fields8-08A - 124 - [MP3] Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body [MP3].flac-fields7-Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields1-08A - 124 - Body-None]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields2-08A - 124 - Body-3B]`
  - `tests/test_landing_head.py::test_the_name_carries_the_head_and_nothing_invents_a_tempo[Body.flac-fields3-08A - 124 - Body-Am]`
  - ... and 1 more, see the JSON sidecar

Old text:

```
Year="0" AverageBpm="0.00"
```

New text:

```
Year="0" AverageBpm="112.00"
```

### `r924.F5_watcher_not_joined`

The watcher is told to stop and not waited for, so it can outlive the fetch

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F5_watcher_not_joined`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_fetch_that_raises_still_stops_the_watcher`

Old text:

```
        stop.set()
        watcher.join()
```

New text:

```
        stop.set()
```

### `u104-b.F8_leftover_recorded`

Drop the record of a scratch folder that could not be removed, so the envelope says nothing about it

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F8_leftover_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_scratch_folder_that_cannot_be_removed_is_said_on_the_envelope`

Old text:

```
        if scratch.exists():
            held.leftover = str(scratch)
```

New text:

```
        if scratch.exists():
            pass
```

### `u121.S18_info_json_flag`

_MixDownload.argv: do not ask yt-dlp for the info document

- File: `src/cratekit/intake/fetch.py`
- Source: `u121.json`, row `S18_info_json_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_runs_u80s_download_under_a_mix_sized_bound`

Old text:

```
        argv[1:1] = ["--playlist-end", str(PLAYLIST_PROBE), "--write-info-json"]
```

New text:

```
        argv[1:1] = ["--playlist-end", str(PLAYLIST_PROBE)]
```

### `u37-author-light.G2_recognition_gate`

Skip the recognition presence gate

- File: `src/cratekit/intake/recognize.py`
- Source: `u37-author-light.json`, row `G2_recognition_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_pipeline.py::test_identification_only_downloads_nothing_and_writes_a_tracklist`

Old text:

```
    missing = recognition_ready()
    if not missing:
        return
    raise refuse(
```

New text:

```
    missing = recognition_ready()
    if True:
        return
    raise refuse(
```

### `u102-a.P2_root_casefold`

_key: compare the root exactly instead of casefolded

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P2_root_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_in_any_case_and_a_shared_prefix_is_not_the_folder`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return locations.norm_for_compare(path)
```

### `u102-a.U4_same_suffix`

_unusable_why: drop the check that the proposed name keeps the file's extension

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U4_same_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[04A - 124 - Song - Artist.txt-change the file's extension]`

Old text:

```
    if Path(proposed).suffix.lower() != Path(accepted.path).suffix.lower():
```

New text:

```
    if False:
```

### `u102-b.G8_collision_is_owed`

_HELD: stop counting a collision as owed, which is R-172 itself, a skipped collision reported as ok

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G8_collision_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (REFERENCED, UNUSABLE)
```

### `u52-item-derivation.C2_can_list_requires_all`

Require EVERY listing method rather than any, so a client exposing one of two is refused instead of half read

- File: `src/cratekit/label/crawl.py`
- Source: `u52-item-derivation.json`, row `C2_can_list_requires_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`
- Collected: 180 against a baseline of 180
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_listing_that_cannot_be_paged_raises_instead_of_reporting_empty`
  - `tests/modules/test_labels.py::test_a_provider_error_out_of_the_crawl_is_not_an_empty_catalogue`
  - `tests/modules/test_labels.py::test_one_working_listing_with_no_releases_still_reports_empty`

Old text:

```
    return any(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

New text:

```
    return all(getattr(artist, method, None) is not None for method in LISTING_METHODS)
```

### `u177.A1_account_suffix`

bandcamp_account: keep .bandcamp.com on the host, so an address is stored as a host no purchase's seller equals

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A1_account_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 23 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_fetch_of_no_labels_release_names_no_label_landing`
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_label_whose_purchases_are_all_filtered_is_not_said_to_stage`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_seller_is_named_with_the_command_that_registers_it`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_sellers_files_stage_with_no_label_tag`
  - `tests/test_bandcamp_labels.py::test_seller_by_label_name_fetches_only_that_labels_releases`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`
  - `tests/test_bandcamp_labels.py::test_the_plan_names_each_rows_label_and_none_for_a_seller_no_label_names`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    if host.endswith(_ACCOUNT_HOST):
        host = host[: -len(_ACCOUNT_HOST)]
    if not host or not _ACCOUNT.fullmatch(host):

```

New text:

```
    if not host or not _ACCOUNT.fullmatch(host):

```

### `r704-a.S5_context_read_by_type`

an implicit context is read by its type as well as its status, so an unrelated error raised while handling a rate limit is called one

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S5_context_read_by_type`
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
    if any(is_rate_limit(link) for link in _linked(exc, "__context__")):
```

### `u237.M7_left_word_boundary_only`

_words_within: pad only the front, so a needle that is a word's prefix still confirms

- File: `src/cratekit/label/verify.py`
- Source: `u237.json`, row `M7_left_word_boundary_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_kept_listing.py`
- Collected: 392 against a baseline of 392
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Puls-Pulse]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[RAWAXXX-Rawax]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-RAWAXXX]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[Rawax-Rawaxxx Records]`
  - `tests/modules/test_labels.py::test_a_needle_inside_a_longer_word_confirms_nothing[tide-Tidewater]`
  - `tests/modules/test_labels.py::test_a_release_credited_to_a_longer_act_name_is_a_mismatch_not_a_confirmation`
  - `tests/test_label_tidal_catalogue.py::test_a_longer_act_name_holding_the_needle_neither_confirms_nor_discovers`

Old text:

```
    return f" {needle} " in f" {credit} "
```

New text:

```
    return f" {needle}" in f" {credit} "
```

### `u192.F8_not_exclusive`

add_job_options: declare the two flags on the parser rather than in one exclusive group

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F8_not_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 278 against a baseline of 278
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_queue_only_beside_job_is_refused_before_anything_is_queued[restamp]`
  - `tests/test_analysis_workers.py::test_queue_only_beside_job_is_refused_before_anything_is_queued[run]`
  - `tests/test_tag_workers.py::test_tag_folder_queue_only_beside_job_is_refused_before_anything_is_queued`

Old text:

```
    chosen = parser.add_mutually_exclusive_group()
```

New text:

```
    chosen = parser
```

### `r229.L11_an_empty_name_matches`

The empty name guard is removed, so a nameless playlist matches any key ending in the separator

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L11_an_empty_name_matches`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_written_before_tracks_were_kept_is_recognised_by_name[2024/--False]`

Old text:

```
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))
```

New text:

```
    return recorded_key == name or recorded_key.endswith("/" + name)
```

### `r229.L2_exactly_half_is_not_enough`

Exactly half no longer qualifies, the boundary moved from at least to more than

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L2_exactly_half_is_not_enough`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_is_recognised_when_the_crate_still_carries_half_its_tracks[exactly-half]`

Old text:

```
    return shared >= 1 and shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR
```

New text:

```
    return shared >= 1 and shared * SHARED_DENOMINATOR > len(written) * SHARED_NUMERATOR
```

### `u309.U5_reserve_written`

A reservation's new identifier is never written to the ledger

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U5_reserve_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 136 (killed)
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
  - ... and 121 more, see the JSON sidecar

Old text:

```
        held[key] = record(remote_id)
        ledger._write(cfg, document)
        return remote_id, True
```

New text:

```
        held[key] = record(remote_id)
        return remote_id, True
```

### `u27-reports-round-1.C1_tree_absent_refusal`

Drop the refusal for a governed tree the export does not hold, so every entry reports uncovered

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C1_tree_absent_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
    if not view.has_folder(tree.display):
        raise _refuse_absent(tree)

```

New text:

```
(empty)
```

### `u27-reports-round-1.L3_empty_tempo_is_zero`

Report an unreadable library as a tempo range of zero rather than as unknown

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L3_empty_tempo_is_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_library_with_no_readable_head_reports_none_rather_than_zero`

Old text:

```
    if not found:
        return TempoSpread(readable=0, unreadable=unreadable)

```

New text:

```
    if not found:
        return TempoSpread(
            readable=0, unreadable=unreadable, lowest=0.0, highest=0.0, median=0.0
        )

```

### `r154-a.A1_stamp_pattern`

Drop the pattern half of is_stamp, so the calendar parse alone decides and its lenient padding admits 2026-8-01T000000Z

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-a.json`, row `A1_stamp_pattern`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-8-01T000000Z]`

Old text:

```
    if not _STAMP_SHAPE.fullmatch(value):
        return False
    try:
        datetime.strptime(value, _STAMP_FORMAT)
```

New text:

```
    try:
        datetime.strptime(value, _STAMP_FORMAT)
```

### `r222-a.A10_plan_text_at_keep_zero`

Describe the held run at a keep of zero, so the preview promises a retention the run does not apply

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A10_plan_text_at_keep_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_plan_describes_the_rotation_the_run_applies[0-keeping no-last completed mirror]`

Old text:

```
    if archive_keep == 0:
        return "keeping no dated archive folder"
```

New text:

```
    if False:
        return "keeping no dated archive folder"
```

### `r222-a.A8_floor_read_by_a_rehearsal`

Read the record above the rehearsal's return, so a preview fails over a file it never touches

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A8_floor_read_by_a_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if keep < 0 or not purge:
        return out, None
    floor = _rotation_floor(cfg)
```

New text:

```
    floor = _rotation_floor(cfg)
    if keep < 0 or not purge:
        return out, None
```

### `r388-c.M17_slug_respelled`

Respell the enum value, so the engine raises a slug nothing reserved

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r388-c.json`, row `M17_slug_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `u317.Q10_token_not_struck`

run_backup: the record's token stays in the library's fact while a run sends, so a failed run of another installation leaves its record trusted (round two's finding)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q10_token_not_struck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 23212 against a baseline of 23212
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    _strike_token(cfg)
```

New text:

```
                    pass
```

### `u45-round-1.E4_return_codes_unread`

Stop reading return codes in run_backup, which is exactly the defect its sibling run_restore shipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E4_return_codes_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 16 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_capture_marks_the_snapshot_after_the_database_and_never_before_it`
  - `tests/modules/test_tools.py::test_the_prune_runs_only_after_the_mirror_succeeded`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_narrowed_portion_whose_transfer_failed_refuses_by_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`
  - ... and 1 more, see the JSON sidecar

Old text:

```
            if result.returncode != 0:
                failed = result
                break
```

New text:

```
            pass
```

### `u311.A9_uncomposed_reads_nfd`

The decomposed name check asks for NFD instead of NFC, flagging composed names and missing decomposed ones

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u311.json`, row `A9_uncomposed_reads_nfd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 317 against a baseline of 317
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_quick_walk_reads_hashes_globs_and_names_as_rclone_does`

Old text:

```
unicodedata.is_normalized("NFC", path)
```

New text:

```
unicodedata.is_normalized("NFD", path)
```

### `r154-b.B3_handed_down_stamp`

Ignore accept_unrecorded, so a stamp the verb resolved and handed down arrives looking typed and an unmarked one is pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B3_handed_down_stamp`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 188 against a baseline of 188
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_resolved_stamp_handed_down_is_not_mistaken_for_one_a_person_named`

Old text:

```
        accepted = True if accept_unrecorded is None else accept_unrecorded
```

New text:

```
        accepted = True
```

### `r338-a.B5_one_mirror_for_every_library`

share_destination: key every library's share under the one unrecorded folder, so two libraries under one snapshot root archive each other's grids

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B5_one_mirror_for_every_library`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r338-b.R8_unmarked_snapshot_orphans_the_share`

_plan_restore_inside_the_gates: drop the fallback to this library's identity, so a snapshot whose marker failed to write looks for its share under the unrecorded folder

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R8_unmarked_snapshot_orphans_the_share`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `r367.G3_membership_is_inverted`

copy the sidecar when it is absent and skip it when it is present

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G3_membership_is_inverted`
- Moved: Anchored where u311-replay-after-a.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
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
        if name not in held:
```

New text:

```
        if name in held:
```

### `r388-a.M4_contents_listing_message_reworded`

Reword could not be listed to could not be read in the contents listing refusal, the sidecar row R-387 recorded as G9

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M4_contents_listing_message_reworded`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
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

### `u27-restore-cli-independent.X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`

What the from-backup zeros DO leave held: remove the refusal that stops a restore with no recorded decision, in the backup module the verb calls. Paired with I_A1 and with the whole from-backup family of zeros, which are one hole rather than eleven

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `u27-restore-cli-independent.json`, row `X1_the_off_machine_engine_stops_refusing_an_unconfirmed_restore`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 430 against a baseline of 430
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`
  - `tests/test_write_session.py::test_the_restore_is_the_recovery_and_reaches_its_own_refusals`
  - `tests/test_write_session.py::test_the_restores_own_refusals_survive_the_gates_being_added`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
            "a restore replaces the live database and is not performed without an "
            "explicit decision naming this library and this snapshot.",
        )
```

New text:

```
(empty)
```

### `u44-author.A3_archive_after_the_first_pass`

Move the archive AFTER the probe, so a crash between them leaves no verified copy

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u44-author.json`, row `A3_archive_after_the_first_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_master_cli.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_archive_is_taken_before_any_encoding_stage`

Old text:

```
    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )

    probe = probe_source(source, runner=runner, ffprobe=ffprobe)
```

New text:

```
    probe = probe_source(source, runner=runner, ffprobe=ffprobe)

    archived_to = None
    if archive:
        archived_to = archive_source(
            source, archive_dir or (source.parent / ARCHIVE_DIRNAME)
        )
```

### `r187-b.B8_bool_is_a_number`

_is_number: let a bool through as an int, so a cached energy of true is served

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B8_bool_is_a_number`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`

Old text:

```
    return value is None or (isinstance(value, int | float) and not isinstance(value, bool))
```

New text:

```
    return value is None or isinstance(value, int | float)
```

### `u43-author-light.E3_tempo_serialized_as_bpm`

as_payload spells the tempo key the way the Vorbis tag dialect does, which is one splat from handing a tempo to a tag writer and seeding a grid at half or double time (R17)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E3_tempo_serialized_as_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_structured_payload_carries_a_version`
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
            "tempo": plan.anchor.bpm,
```

New text:

```
            "bpm": plan.anchor.bpm,
```

### `u281.R6_outage_keeps_the_count`

Refusals.heard: only a match or a miss resets, so refused, refused, down, refused stops the run

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R6_outage_keeps_the_count`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_an_answer_between_refusals_ends_the_run_of_them[an-outage-between]`

Old text:

```
        else:
            self.running.pop(outcome.source, None)
```

New text:

```
        elif outcome.answer in (Answer.MISS, Answer.MATCHED):
            self.running.pop(outcome.source, None)
```

### `u956.O5_tagging_walk_confined`

tagging rows.scanned: confine the tag verbs' walk, so tag rows counts a sampler row as unreadable

- File: `src/cratekit/tagging/rows.py`
- Source: `u956.json`, row `O5_tagging_walk_confined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_tag_backlog.py`
- Collected: 88 against a baseline of 88
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_tagging_walk_still_reads_a_row_outside_the_root`

Old text:

```
        confine_to_root=False,
```

New text:

```
        confine_to_root=True,
```

### `u260.F6_fetch_bound_off_by_one`

remembering: keep one entry more than the bound

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F6_fetch_bound_off_by_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_fetch_memory_keeps_a_few_addresses_and_forgets_the_oldest`

Old text:

```
            while len(held) > bound:
```

New text:

```
            while len(held) > bound + 1:
```

### `u281.W4_binder_drops_the_count`

for_taxonomy: hand the searcher no count, so the worker's run count never reaches it

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `W4_binder_drops_the_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`

Old text:

```
    return catalogue_searcher(declared, discogs=for_discogs(), refusals=refusals)
```

New text:

```
    return catalogue_searcher(declared, discogs=for_discogs(), refusals=None)
```

### `u118-d.T2_named_word`

Hip-hop & Rap is no longer a Hip-Hop word

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u118-d.json`, row `T2_named_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_routing_parity.py`
- Collected: 928 against a baseline of 926
- Kills: 5 (collect-error)
- Note: collection changed: 928 collected against a baseline of 926. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_adopt_split_place.py::test_a_hip_hop_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[Hip-hop & Rap]`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_each_word_routes_to_the_folder_the_author_gave_it[Hip-hop & Rap-Hip-Hop]`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`
  - `tests/test_routing_parity.py::test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left`

Old text:

```
  "Hip-hop & Rap",

```

New text:

```
(empty)
```

### `u133-b.T9_energy_off`

Jazz has no energy split

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T9_energy_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy.py`
- Collected: 1038 against a baseline of 1038
- Kills: 13 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[2-low]`
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[5-med]`
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[9-high]`
  - `tests/test_adopt_jazz_folder.py::test_a_jazz_track_in_the_old_playlist_moves_into_its_band_and_leaves_it[None-unsorted]`
  - `tests/test_adopt_jazz_folder.py::test_a_partial_jazz_match_already_in_rock_is_filed_in_jazz_and_stays_in_rock`
  - `tests/test_adopt_jazz_folder.py::test_adoption_withholds_a_jazz_track_still_in_the_old_playlist`
  - `tests/test_adopt_jazz_folder.py::test_an_approved_move_files_jazz_in_its_bands_and_keeps_every_other_membership`
  - `tests/test_adopt_jazz_folder.py::test_jazz_is_shaped_as_hip_hop_is`
  - `tests/test_adopt_jazz_folder.py::test_the_gate_shows_every_jazz_track_moving_and_no_other_track`
  - `tests/test_adopt_jazz_folder.py::test_the_old_jazz_playlist_competes_in_both_buckets_and_is_never_a_destination`
  - `tests/test_routing_parity.py::test_every_bucket_and_level_lands_in_the_same_sub`
  - `tests/test_routing_parity.py::test_the_reserved_and_derived_subs_are_never_returned_by_routing[derived]`
  - `tests/test_routing_parity.py::test_the_reserved_and_derived_subs_are_never_returned_by_routing[reserved]`

Old text:

```
  "jazz",
]
rates = false

```

New text:

```
  "jazz",
]
rates = false
energy = { enabled = false }

```

### `r675.G3_candidate_leaf_not_keyed`

_referenced: the candidates are indexed by their name as spelled, so a keyed lookup never finds one

- File: `src/cratekit/write/naming_cli.py`
- Source: `r675.json`, row `G3_candidate_leaf_not_keyed`
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
        leaves.setdefault(_key(path.name), []).append(str(path))
```

New text:

```
        leaves.setdefault(path.name, []).append(str(path))
```

### `r758-a.T2_first_commit_admits_a_removal`

the move's first commit admits a removal, so one slipped into the additions lands

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T2_first_commit_admits_a_removal`
- Moved: the move's additions and their commit are now the step _add_targets, writing through the _Run record
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_additive_membership_writer_refuses_a_removal_in_its_session`

Old text:

```
                run.add(places.for_adding(destination), destination, content_ids)
            rb_writer.commit_guarded(run.db)
```

New text:

```
                run.add(places.for_adding(destination), destination, content_ids)
            rb_writer.commit_guarded(run.db, removals=rb_writer.REMOVABLE_TABLES)
```

### `r658-b.S12_repair_real_read`

Drop the one patch the repair test puts back, so the configured fixture's empty collection read stands

- File: `tests/intake/test_repair_apply.py`
- Source: `r658-b.json`, row `S12_repair_real_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_row_after_the_gate_holds_the_file_and_an_unreadable_collection_refuses`

Old text:

```
    monkeypatch.setattr(naming_cli, "_recorded", _REAL_RECORDED)

```

New text:

```
(empty)
```

