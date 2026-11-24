# Mutation table: u332-replay-before-6

Measured by `scripts/mutate.py` on 2026-11-24 06:16 UTC, branch `HEAD` at `324cafa5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 153.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:16 UTC for commit `324cafa562b9`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 121, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 159 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B4_a_failed_run_closed_as_a_capture` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 1 | killed |
| `u122.H3_progress_not_held` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 6 | killed |
| `u148.C1_one_short_allowed` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 2 | killed |
| `u148.S1_branch_before_read` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 1 | killed |
| `u151.F1_cursor_typed` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.X1_next_skips_context` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u187.A4_heading_drifts` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 5 | killed |
| `u203.M6_one_pass` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u291.L5_default_ignores_the_constant` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 2 | killed |
| `u197.M4_registry_alternatives_fold` | `src/cratekit/acquire/__init__.py` | user | 2 file(s) | 574 | 1 | killed |
| `r83.D6_remedy` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 753 | 11 | killed |
| `u176.C1_rejected_status_is_session` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 1 | killed |
| `u176.V10_same_bytes_staged` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V5_suppressed_is_held` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u177.B3_unregistered_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `u305.M7_registration_warnings_import_dropped` | `src/cratekit/acquire/bandcamp_cli.py` | user | 3 file(s) | 114 | 1 | killed |
| `u205.C6_message_spells_404` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 2 | killed |
| `r289-b.B6_job_directory_never_reclaimed` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r668-a.M4_no_missing_list_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `u169.A2_any_permanent_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 7 | killed |
| `u42-author.C5_empty_marker_matches_everything` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u54-acquisition-worker.G12_landing_check` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-acquisition-worker.G28_marker_decided_by_the_file` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u80.F10_no_url_dedupe` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F4_timeout_is_empty` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u81-fetch-b.Y2_metadata_kept_on_convert` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W10_untaggable_committed` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W9_row_tags_not_written` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `r1016.M2_account_parse_through_the_factory` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 12 | killed |
| `r261.L1_skip_record` | `src/cratekit/acquire/listing.py` | user | 4 file(s) | 522 | 4 | killed |
| `r878-a.A6_latest_count_wins` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-b.B7_no_offset_sent` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 2 | killed |
| `u65.B2_favourites_back_to_the_empty_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 6 | killed |
| `u65.C6_offset_advances_by_what_was_served` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 10 | killed |
| `u65.F3_the_retry_ceiling_is_raised` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 86 | 11 | killed |
| `r1709.M11_recording_identity_is_the_token` | `src/cratekit/acquire/match_identity.py` | user | 29 file(s) | 3858 | 24 | killed |
| `u205.O3_unreadable_values_read_as_absent` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 353 | 1 | killed |
| `r703-a.V1_no_observed_session` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 4 | killed |
| `r703-b.O3_writes_land_on_proxy` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 1 | killed |
| `u197.M5_adapter_name` | `src/cratekit/acquire/vendored.py` | user | 3 file(s) | 643 | 11 | killed |
| `u47-author.R195_drop_ffmpeg_key` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 4 | killed |
| `u47-author.R197_drop_event_abort` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 6 | killed |
| `u47-author.SAMPLE_quality_equality` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u254.M06_never_cache` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 743 | 1 | killed |
| `u254.M15_header_string_version` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `r1991.A2_shared_pair_recorded` | `src/cratekit/adopt/apply_cli.py` | user | 15 file(s) | 521 | 1 | killed |
| `r788-d.A3_present_rows_handed_over` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 163 | 2 | killed |
| `u27-adopt-apply-author.S1_no_session_at_all` | `src/cratekit/adopt/apply_cli.py` | user | 1 file(s) | 17 | 6 | killed |
| `u55-collection-reader.R27_apply_no_tag_value` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 2 | killed |
| `u23-round-8-independent.X4_approval_digest_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `r780-a.A12_unnamed_not_left_in_tree_path` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r797-b.M7_a_track_still_there_is_listed` | `src/cratekit/adopt/move.py` | user | 3 file(s) | 172 | 10 | killed |
| `u118-c.M7_unnamed_reason` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 58 | 1 | killed |
| `r758-b.C9_read_back_is_not_the_verdict` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A7_doubled_rows_not_carried` | `src/cratekit/adopt/placements.py` | user | 2 file(s) | 128 | 4 | killed |
| `r797-b.M2_recorded_under_the_old_sub` | `src/cratekit/adopt/placements.py` | user | 3 file(s) | 172 | 2 | killed |
| `r722.P3_verdict_drops_level` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 1 | killed |
| `r731-a.M05_unnamed_without_held` | `src/cratekit/adopt/plan.py` | maintainer | 2 file(s) | 70 | 1 | killed |
| `r788-a.P2_blind_plan_files` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 3 | killed |
| `r788-b.P17_withheld_presence_is_planned` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 1 | killed |
| `u956.O16_row_names_no_location` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 43 | 2 | killed |
| `u23-round-8-independent.B1_settled_never_refuses` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.E4_vacancy_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.X12_look_at_drops_the_regular_file_test` | `src/cratekit/adopt/revert_changed.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.X14_probe_drops_the_dataless_test` | `src/cratekit/adopt/scan.py` | user | 1 file(s) | 615 | 1 | killed |
| `u956.O1_confine_guard_gone` | `src/cratekit/adopt/scan.py` | user | 4 file(s) | 687 | 7 | killed |
| `u956.S20_tombstone_scanned` | `src/cratekit/adopt/scan.py` | user | 4 file(s) | 687 | 3 | killed |
| `u241.M23_identity_without_the_size` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 1 | killed |
| `u223.M2_keep_linked_intent` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 177 | 1 | killed |
| `u306.A5_item_record_owner` | `src/cratekit/analysis/artifacts.py` | user | 3 file(s) | 318 | 2 | killed |
| `u90-b.B1_library_root_unchecked` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-c.C2_unreadable_refuses` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u94-a.S7_samefile_to_spelling` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W8_note_forgets_the_omission` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `r395.M9_worker_literal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 1 | killed |
| `u223.M15_folder_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 1 | killed |
| `u306.A2_zero_state` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 213 | 4 | killed |
| `u343.M06_handle_run_no_resume_skip` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 482 | 10 | killed |
| `u58-workers-and-wav.S2_unchanged_rewritten` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 1 | killed |
| `u263.D15_chunk_padding` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 57 | 1 | killed |
| `u264.M10_window_dropped` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 23216 | 0 (promoted) | zero |
| `u264.M4_table_rule_1_0` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 1 | killed |
| `u157.D1_band_narrow` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u263.D16_head_no_decoder` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u58-workers-and-wav.E1_beatless_cap` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 177 | 1 | killed |
| `u327.A18_file_read_back` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u327.A9_tag_body_compared` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u342.P4_stamped_apart` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 10 | killed |
| `u342.C2_written_counts_what_took` | `src/cratekit/analysis/head_adopt_cli.py` | user | 4 file(s) | 392 | 1 | killed |
| `u275.M4_base_rounded_down` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 555 | 5 | killed |
| `u343.M11_mark_value_empty` | `src/cratekit/analysis/run.py` | user | 4 file(s) | 264 | 9 | killed |
| `sitting3.G4_clip_wrapper` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 1 | killed |
| `u58-workers-and-wav.W1_voxlevel_zero` | `src/cratekit/analysis/vocals.py` | user | 1 file(s) | 177 | 4 | killed |
| `u92-author.G2_cap_is_inclusive` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 1 | killed |
| `u241.M26_warm_up_takes_no_lock` | `src/cratekit/analysis/warm.py` | user | 1 file(s) | 15 | 1 | killed |
| `r221-b.M1_refusal_step_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `r222-b.B1_always_enqueue` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 8 | killed |
| `r222-b.B9_mirror_not_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r349-c.C2_write_failure_step` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u311.B3_iso_drops_a_present_moment` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 218 | 1 | killed |
| `u45-round-1.H2_queueing_plans_first` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `u45-round-1.W3_ages_not_read_back` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 4 | killed |
| `u50-author.B3_items_one_portion_only` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 14 | killed |
| `r290-author.D4_cancelled_reads_failed` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7231 | 22 | killed |
| `r388-c.M13_credential_step_dropped` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 660 | 2 | killed |
| `r925.J5_version_dropped` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 1 | killed |
| `r682-a.M11_unstated_bound_inclusive` | `src/cratekit/cli/render.py` | user | 2 file(s) | 122 | 3 | killed |
| `r685-a.L6_a_permission_is_a_defect_to_report` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u260.E12_key_digest_of_64_kb` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 1 | killed |
| `u260.E9_encode_evicts_newest` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u83-a.E6_exif_orientation` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 1 | killed |
| `u83-b.W12_container_refusal` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 5 | killed |
| `u83-b.W8_flac_clear_pictures` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u317.Q18_week_doubled` | `src/cratekit/core/backup_facts.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u331.S01_yt_dlp_subject_dropped` | `src/cratekit/core/binaries.py` | user | 3 file(s) | 113 | 1 | killed |
| `u45-round-1.V2_summary_slug_undeclared` | `src/cratekit/core/cause.py` | user | 33 file(s) | 5516 | 4 | killed |
| `u94-b.W9_walk_warning_says_queued` | `src/cratekit/core/discovery.py` | user | 1 file(s) | 177 | 1 | killed |
| `r390-a.A2_retry_refuses_any_closed_job_with_a_cause` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 296 | 9 | killed |
| `u169.E4_decline_drops_cause` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 153 | 10 | killed |
| `u241.M08_plan_forgets_which_gate` | `src/cratekit/core/pool.py` | user | 2 file(s) | 298 | 6 | killed |
| `u301.G5_report_state_reads_garbage_as_fresh` | `src/cratekit/core/provider_gate.py` | user | 1 file(s) | 66 | 1 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `u118-b.R2_split_lookup` | `src/cratekit/core/routing.py` | user | 2 file(s) | 102 | 14 | killed |
| `r722.T8_lenient_energy_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 1 | killed |
| `u118-b.A1_tag_beats_route` | `src/cratekit/core/taxonomy_build.py` | user | 3 file(s) | 1070 | 4 | killed |
| `r706-a.A1_ceiling_dropped` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 6 | killed |
| `r706-b.B2_parts_needed_floors` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 7 | killed |
| `r924.A4_split_on_one_part` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `u103-a.A5_offset_must_be_planned` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 1 | killed |
| `u57-recognition-and-items.M1_miss_family_loses_1001` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 39 | killed |
| `u259.M5_member_reads_nothing` | `src/cratekit/intake/analyzed.py` | user | 2 file(s) | 85 | 16 | killed |
| `r682-a.M4_state_keys_not_seeded` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 3 | killed |
| `u104-e.E3_honest_zero_names_the_address` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 108 | 1 | killed |
| `u213.M9_readable_order_holds_unread` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 3 | killed |
| `u70.S6_source_id_only_for_hearts` | `src/cratekit/intake/cli.py` | maintainer | 2 file(s) | 241 | 1 | killed |
| `u103-b.C3_out_must_be_a_folder` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u104-e.E2_timeout_is_retryable` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `r924.F2_no_landed_line` | `src/cratekit/intake/fetch.py` | user | 2 file(s) | 52 | 2 | killed |
| `u104-b.F5_landing_is_a_file` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P4_timeout_is_its_own_kind` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u307.R16_identify_only_drops_a_field` | `src/cratekit/intake/pipeline.py` | user | 2 file(s) | 75 | 1 | killed |
| `r675.G10_repair_apply_asks_with_no_candidates` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 121 | 1 | killed |
| `u102-a.U1_no_stored_path` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G5_claim` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u308.L4_translated_swallows_refusal` | `src/cratekit/label/catalogue.py` | user | 4 file(s) | 467 | 8 | killed |
| `u237.M5_bare_year_is_a_label` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 4 | killed |
| `r704-a.S2_cause_walk_reads_only_the_error` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 1 | killed |
| `u261.O1_catalogue_drops_the_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 270 | 3 | killed |
| `u192.F4_command_dropped` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 4 | killed |
| `r356-b.B8_heart_back_drops_the_reason` | `src/cratekit/modules/outbound/hearts.py` | user | 1 file(s) | 64 | 1 | killed |
| `r229.L18_contents_grow` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 5 | killed |
| `r229.L7_a_reused_path_keeps_its_record` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `u205.S1_account_lookup_ignores_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 179 | 17 | killed |
| `u27-reports-round-3-fixes.F6_folder_count_overwrite` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-2.L2_genre_parent` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 2 | killed |
| `r1761.P10_move_nothing_only_when_new` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r1761.P4_content_proof_skipped` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r222-a.A5_held_run_takes_no_slot` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 5 | killed |
| `r349-c.C1_prune_recorded` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 29 | killed |
| `r757-a.E7_first_totals_win` | `src/cratekit/modules/tools/backup.py` | maintainer | 4 file(s) | 23216 | 0 (promoted) | zero |
| `u311.A2_refused_portion_runs` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u317.Q20_resend_keeps_times` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u323.I6_provider_dropped_at_the_gate` | `src/cratekit/modules/tools/backup.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u48-author.P4_warning_not_recorded_on_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 5 | killed |
| `r1761.P17_census_damaged_is_none` | `src/cratekit/modules/tools/backup_record.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `u311.A6_double_star_stays_in_a_segment` | `src/cratekit/modules/tools/backup_record.py` | user | 4 file(s) | 318 | 1 | killed |
| `u317.Q2_unreadable_folder_is_absence` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 23216 | 1 (promoted) | killed |
| `r154-a.A5_listing_filter` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 189 | 1 | killed |
| `r154-b.B8_walk_match` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 189 | 3 | killed |
| `r338-b.R5_pulled_under_the_watch` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r367.E3_a_live_rekordbox_is_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 1 file(s) | 189 | 1 | killed |
| `r388-a.M1_named_identity_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 2 | killed |
| `r388-b.M7_share_listing_back_to_absence` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `u311.C5_binaries_out_of_order` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 30 | killed |
| `r187-b.B4_empty_read_cached` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 1 | killed |
| `u311.C9_anchor_comes_back` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 13 | killed |
| `u281.R3_stopped_reads_miss` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 8 | killed |
| `u282.W1_walk_beatport_first` | `src/cratekit/tagging/catalogues.py` | user | 9 file(s) | 1470 | 43 | killed |
| `u260.F3_admission_ignored` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 2 | killed |
| `u281.S3_challenge_header_case` | `src/cratekit/tagging/searchers.py` | user | 3 file(s) | 204 | 1 | killed |
| `u281.S8_refusal_check_before_the_payload` | `src/cratekit/tagging/shops.py` | user | 3 file(s) | 205 | 1 | killed |
| `u133-b.T4_rates` | `src/cratekit/templates/taxonomy.default.toml` | user | 3 file(s) | 945 | 1 | killed |
| `u90-c5.C5_record_threshold_unconverted` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 203 | 1 | killed |
| `r1991.T4_no_record` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 5 | killed |
| `r758-b.T7_refusal_read_as_an_interruption` | `src/cratekit/write/trees.py` | user | 1 file(s) | 87 | 1 | killed |

## Zero rows and what they owe

- `u264.M10_window_dropped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u157.D1_band_narrow` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u263.D16_head_no_decoder` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-c.C2_write_failure_step` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r685-a.L6_a_permission_is_a_defect_to_report` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q18_week_doubled` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P10_move_nothing_only_when_new` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P4_content_proof_skipped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-a.E7_first_totals_win` (maintainer facing): maintainer facing, composite not required
- `u317.Q20_resend_keeps_times` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u323.I6_provider_dropped_at_the_gate` (maintainer facing): maintainer facing, composite not required
- `r1761.P17_census_damaged_is_none` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u297.B4_a_failed_run_closed_as_a_capture`

run_capture: write the manifest though the scenario run failed, so a capture missing scenarios reads as finished

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B4_a_failed_run_closed_as_a_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_run_that_failed_with_every_record_written_is_not_a_capture`

Old text:

```
    if done.returncode != 0 or not recorded or missing:
```

New text:

```
    if not recorded or missing:
```

### `u122.H3_progress_not_held`

UNDERWAY loses In Progress, a session's and a lane's status

- File: `scripts/board.py`
- Source: `u122.json`, row `H3_progress_not_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In Progress]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In Progress]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In Progress]`

Old text:

```
UNDERWAY = ("In Progress", "In review")
```

New text:

```
UNDERWAY = ("In review",)
```

### `u148.C1_one_short_allowed`

short_of_count lets a read one row short of the count through

- File: `scripts/board.py`
- Source: `u148.json`, row `C1_one_short_allowed`
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
    if len(rows) < total - 1:
```

### `u148.S1_branch_before_read`

start creates the branch before it reads the board, the shape before the review

- File: `scripts/board.py`
- Source: `u148.json`, row `S1_branch_before_read`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_start_reads_the_board_before_it_branches`

Old text:

```
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

    subprocess.run(["git", "checkout", "-b", branch], check=True)

```

New text:

```
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    ctx = project_context(owner)
    items = project_items(owner)
    item = items.get(node["number"])

```

### `u151.F1_cursor_typed`

the cursor goes as -F, which gh would type

- File: `scripts/board.py`
- Source: `u151.json`, row `F1_cursor_typed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_the_card_read_is_a_page_per_hundred_issues_not_a_call_per_card`

Old text:

```
            args += ["-f", f"after={after}"]
```

New text:

```
            args += ["-F", f"after={after}"]
```

### `u151.X1_next_skips_context`

next trusts the card read without asking for the project first

- File: `scripts/board.py`
- Source: `u151.json`, row `X1_next_skips_context`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_next_asks_for_the_project_before_trusting_an_empty_card_read`

Old text:

```
        project_context(owner)
        items = project_items(owner)
```

New text:

```
        items = project_items(owner)
```

### `u187.A4_heading_drifts`

HEAD_ANSWER: a nearby heading, answer from phil, so the documented heading no longer matches

- File: `scripts/board.py`
- Source: `u187.json`, row `A4_heading_drifts`
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
HEAD_ANSWER = "answer from phillip"
```

New text:

```
HEAD_ANSWER = "answer from phil"
```

### `u203.M6_one_pass`

comment_heading: strip once instead of to a fixed point, so emphasis left behind a full stop survives

- File: `scripts/board.py`
- Source: `u203.json`, row `M6_one_pass`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Brainstorm**.-brainstorm]`
  - `tests/test_board_cloud.py::test_headings_are_read_through_markdown_emphasis_and_punctuation[Landed_!-landed]`

Old text:

```
        while text != settled:
```

New text:

```
        for _ in (1,):
```

### `u291.L5_default_ignores_the_constant`

cmd_cloud: with no --lanes, count four lanes rather than CLOUD_LANES

- File: `scripts/board.py`
- Source: `u291.json`, row `L5_default_ignores_the_constant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments2-0-said2-unsaid2]`
  - `tests/test_board_cloud.py::test_the_lanes_bound_what_is_offered[None-12-comments3-0-said3-unsaid3]`

Old text:

```
    lanes = max(1, getattr(args, "lanes", None) or CLOUD_LANES)
```

New text:

```
    lanes = max(1, getattr(args, "lanes", None) or 4)
```

### `u197.M4_registry_alternatives_fold`

alternatives_to: compare the name as given, so the retired key is offered its own adapter as the replacement

- File: `src/cratekit/acquire/__init__.py`
- Source: `u197.json`, row `M4_registry_alternatives_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_doctor.py`
- Collected: 574 against a baseline of 574
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_retired_vendored_key_resolves_to_the_same_adapter`

Old text:

```
    return tuple(other for other in ADAPTERS if other != current)
```

New text:

```
    return tuple(other for other in ADAPTERS if other != name)
```

### `r83.D6_remedy`

R-348: the defect carries switch-adapter instead of report-defect

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D6_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 753 against a baseline of 753
- Kills: 11 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_download_breaks_the_adapter_the_same_way`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-AttributeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-TypeError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_stops_the_paced_pool_rather_than_being_retried`
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_a_defect_naming_a_token_as_a_defect`

Old text:

```
            remedy=Remedy.REPORT_DEFECT,
        ) from exc
```

New text:

```
            remedy=Remedy.SWITCH_ADAPTER,
        ) from exc
```

### `u176.C1_rejected_status_is_session`

_json: a 401 or 403 is read as an outage rather than a refused session, so an expired cookie is retried rather than sent to the login step

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C1_rejected_status_is_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_session_the_summary_names_but_the_pages_refuse_is_rejected`

Old text:

```
    if response.status in REJECTED_STATUSES:
        raise SessionRejected(f"Bandcamp refused the session when asked for {what}")
```

New text:

```
    if False:
        raise SessionRejected(f"Bandcamp refused the session when asked for {what}")
```

### `u176.V10_same_bytes_staged`

handle_fetch: the same bytes already in the batch are refused rather than counted staged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V10_same_bytes_staged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_the_same_bytes_already_in_the_batch_count_as_staged`

Old text:

```
            if final.is_file() and filecmp.cmp(path, final, shallow=False):
```

New text:

```
            if False:
```

### `u176.V5_suppressed_is_held`

holding: a track a tombstone suppresses is not held, so a deletion made on purpose is fetched back

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V5_suppressed_is_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_track_the_library_deleted_on_purpose_is_held`

Old text:

```
        return str(found.why), ()
```

New text:

```
        return None
```

### `u177.B3_unregistered_filter`

unregistered: name sellers with nothing to fetch too, so a filtered seller is asked to register

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B3_unregistered_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`

Old text:

```
            if one.disposition in TO_FETCH and one.label is None and one.purchase.seller

```

New text:

```
            if one.label is None and one.purchase.seller

```

### `u305.M7_registration_warnings_import_dropped`

_registration_warnings: drop the local import of the label registry, so a tied seller's warning raises NameError

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u305.json`, row `M7_registration_warnings_import_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`, `tests/test_bandcamp_labels.py`, `tests/test_bandcamp.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_two_labels_naming_one_account_by_hand_stage_it_under_neither`

Old text:

```
    from cratekit.label import registry as labels

    warned: list[dict[str, str]] = []
```

New text:

```
    warned: list[dict[str, str]] = []
```

### `u205.C6_message_spells_404`

app client: a token service 404 is spelled with its digits, which the classifier reads as an absence

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C6_message_spells_404`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`
  - `tests/test_catalogue_app.py::test_a_token_service_that_did_not_answer_is_an_outage_never_an_absence[no-such-address]`

Old text:

```
        return "a status saying the address does not exist"
```

New text:

```
        return "status 404"
```

### `r289-b.B6_job_directory_never_reclaimed`

Reclaim the item directories and leave the job directory behind

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B6_job_directory_never_reclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 366 against a baseline of 366
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_the_emptied_staging_of_a_finished_job_is_reclaimed_by_the_next_run`
  - `tests/test_acquire_workers.py::test_the_sweep_reports_what_it_removed_deepest_first`

Old text:

```
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
```

New text:

```
                _reclaim(item_dir, removed)
```

### `r668-a.M4_no_missing_list_guard`

a command naming neither a list nor a job is not refused by the verb, and reads a list called None

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M4_no_missing_list_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_command_naming_nothing_is_refused_before_the_configuration_is_read`
  - `tests/test_acquire_workers.py::test_neither_a_list_nor_a_job_is_refused_by_the_verb_and_queues_nothing`

Old text:

```
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
```

New text:

```
    if False:
        raise _unusable(
```

### `u169.A2_any_permanent_declined`

refused_for_good: drop the policy class, so any permanent failure (output-exists) is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A2_any_permanent_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 7 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return not cause.retryable
```

### `u42-author.C5_empty_marker_matches_everything`

Drop the empty-marker guard, so '' in stem marks every file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C5_empty_marker_matches_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`

Old text:

```
            marked = bool(marker) and marker in path.stem
```

New text:

```
            marked = marker in path.stem
```

### `u54-acquisition-worker.G12_landing_check`

Take the adapter's word for the landed file, skipping the policy check at the file

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G12_landing_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_an_unreadable_landing_is_transient_and_not_a_policy_refusal`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_refused_landing_left_as_evidence_survives_the_sweep`
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    landed = checked_landing(Path(str(result.path)), request.key, policy=per_item.lossless_policy)
```

New text:

```
    landed = Path(str(result.path))
```

### `u54-acquisition-worker.G28_marker_decided_by_the_file`

Take the marker requirement from the offer's claim alone, so a lying offer commits an unmarked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G28_marker_decided_by_the_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    required = result.requires_lossy_marker or lossy_landing(
        landed, policy=per_item.lossless_policy
    )
```

New text:

```
    required = result.requires_lossy_marker
```

### `u80.F10_no_url_dedupe`

The same upload returned twice is offered as two options

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F10_no_url_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls`

Old text:

```
        if hit.url in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u80.F4_timeout_is_empty`

A search that timed out reads as an empty answer rather than an outage

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F4_timeout_is_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_a_timeout_or_a_program_that_cannot_start_is_unavailable[raised0]`

Old text:

```
        except subprocess.TimeoutExpired as exc:
            raise FallbackUnavailable(
                f"the {platform} search did not answer within {self._timeout:g} seconds"
            ) from exc
```

New text:

```
        except subprocess.TimeoutExpired:
            return Answer(hits=())
```

### `u81-fetch-b.Y2_metadata_kept_on_convert`

The metadata drop is not passed to the conversion step

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `Y2_metadata_kept_on_convert`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_extracts_mp3_drops_upload_metadata_and_ends_on_the_address`

Old text:

```
            "--postprocessor-args",
            "ExtractAudio:-map_metadata -1",

```

New text:

```
(empty)
```

### `u81-fetch-a.W10_untaggable_committed`

A landing that could not be tagged from its row is committed anyway

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W10_untaggable_committed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_file_that_cannot_be_tagged_from_its_row_is_not_committed`

Old text:

```
    if not written:
        raise refuse(
            "unavailable-transient",
            untagged,
```

New text:

```
    if False:
        raise refuse(
            "unavailable-transient",
            untagged,
```

### `u81-fetch-a.W9_row_tags_not_written`

The row's artist and title are never written, so the file carries no name at all

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W9_row_tags_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`
  - `tests/test_acquire_fallback_fetch.py::test_artist_and_title_tags_come_from_the_row_not_the_upload_page`

Old text:

```
            landed, {"artist": artist or None, "title": title or None}
```

New text:

```
            landed, {"artist": None, "title": None}
```

### `r1016.M2_account_parse_through_the_factory`

The account walk keeps its own request but parses with parse_factory, so every owned playlist is fetched again

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M2_account_parse_through_the_factory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 12 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_account_playlists_are_returned_unfiltered`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[a-list]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[an-error-body]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[items-null]`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_keeps_the_playlists_the_account_created`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_pages_past_the_first_page`

Old text:

```
    parse = _client_part(user, "playlist", "parse", walk=walk)
```

New text:

```
    parse = _client_part(user, "playlist", "parse_factory", walk=walk)
```

### `r261.L1_skip_record`

listing.artist_releases stops appending a skipped method to the caller's collector

- File: `src/cratekit/acquire/listing.py`
- Source: `r261.json`, row `L1_skip_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/modules/test_labels.py`
- Collected: 522 against a baseline of 522
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_skipped_release_listing_is_named_to_a_caller_that_asks`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_plain_artist_object_missing_one_listing_is_recorded_by_the_source`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`

Old text:

```
                skipped.append(method)
```

New text:

```
                pass
```

### `r878-a.A6_latest_count_wins`

paginate_cursor: keep the first declared count rather than the latest, so a folder removed mid walk refuses a whole listing

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A6_latest_count_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_the_latest_declared_count_is_the_one_checked`

Old text:

```
        if _declared(response) is not None:
            total = _declared(response)
```

New text:

```
        if total is None and _declared(response) is not None:
            total = _declared(response)
```

### `r878-b.B7_no_offset_sent`

_folder_endpoint: send an offset of zero beside the cursor, as the client does

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B7_no_offset_sent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_folders_playlists_are_walked_by_cursor_through_the_folders_own_parser`
  - `tests/test_adapter_listing.py::test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset`

Old text:

```
            "folderId": folder_id,
            "limit": limit,
```

New text:

```
            "folderId": folder_id,
            "offset": 0,
            "limit": limit,
```

### `u65.B2_favourites_back_to_the_empty_page`

the fix as first written: the empty middle window ends the favourites walk

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B2_favourites_back_to_the_empty_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_adapter_listing.py::test_the_declared_count_is_retried_on_the_same_ladder_every_page_is`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`

Old text:

```
    "favorite_tracks": StopRule.DECLARED_TOTAL,
```

New text:

```
    "favorite_tracks": StopRule.EMPTY_PAGE,
```

### `u65.C6_offset_advances_by_what_was_served`

the plausible wrong fix: advance by the page's length, not the window width, re-serving items

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C6_offset_advances_by_what_was_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 10 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_with_no_declared_total_walks_to_an_empty_page`
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`
  - `tests/test_outbound_tidal_account.py::test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one`
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`
  - `tests/test_outbound_tidal_account.py::test_has_heart_answers_a_whole_sweep_from_one_paged_read`

Old text:

```
        offset += page_size

        if total is not None:
```

New text:

```
        offset += len(page)

        if total is not None:
```

### `u65.F3_the_retry_ceiling_is_raised`

U14's bound, mutated to a realistic nearby value rather than removed

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `F3_the_retry_ceiling_is_raised`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`
- Collected: 86 against a baseline of 86
- Kills: 11 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_failure_surfaces_after_the_retry_ceiling`
  - `tests/test_adapter_listing.py::test_a_refusal_that_declares_itself_retryable_still_climbs_the_ladder`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[a-list]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[items-null]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[no-items-no-count]`
  - `tests/test_adapter_listing.py::test_a_response_that_is_not_a_page_is_refused_not_read_as_an_empty_listing[nothing]`
  - `tests/test_adapter_listing.py::test_a_transient_failure_is_still_slept_on_the_full_ladder`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[a-list]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[an-error-body]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[items-null]`
  - `tests/test_adapter_listing.py::test_the_backoff_is_capped_rather_than_doubling_forever`

Old text:

```
            if attempt > max_retries:
```

New text:

```
            if attempt > max_retries + 3:
```

### `r1709.M11_recording_identity_is_the_token`

recording_identity reads the title by fold, the base's token, so every identity collapses again

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r1709.json`, row `M11_recording_identity_is_the_token`
- Moved: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3858 against a baseline of 3858
- Kills: 24 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_adjacent_answers_for_one_recording_fold_and_nothing_else_does[two-emoji-titles-stay-two-rows]`
  - `tests/intake/test_workers.py::test_a_recognised_track_is_keyed_by_recording_version_and_isrc_and_a_provider_row_by_its_id`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact[another-emoji]`
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    return f"{fold(artist)}\x1f{title_identity(title)}"

```

New text:

```
    return f"{fold(artist)}\x1f{fold(title)}"

```

### `u205.O3_unreadable_values_read_as_absent`

opener: recorded app values the keychain will not give are read as absent, putting every lookup back on the account without a word

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O3_unreadable_values_read_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 353 against a baseline of 353
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_keychain_that_could_not_be_read_for_the_app_is_refused_not_read_as_absent`

Old text:

```
        raise catalogue_api.unreadable(exc) from exc
```

New text:

```
        return None
```

### `r703-a.V1_no_observed_session`

fetch no longer stands the observed session in the downloader, so the unlogged lookup error is lost again

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V1_no_observed_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`
  - `tests/test_adapter_contract.py::test_a_rate_limited_album_read_reaches_the_item_cause_by_name`
  - `tests/test_adapter_contract.py::test_a_session_the_tool_saw_rejected_is_an_invocation_auth_failure`

Old text:

```
        observe_session(downloader, tool_log)

```

New text:

```
(empty)
```

### `r703-b.O3_writes_land_on_proxy`

attribute writes land on the proxy, so the tool's audio_quality write never reaches the real session

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `O3_writes_land_on_proxy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_observed_session_writes_through_and_raises_what_it_notes`

Old text:

```
    def __setattr__(self, name: str, value: object) -> None:
        setattr(self._session, name, value)
```

New text:

```
    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)
```

### `u197.M5_adapter_name`

VendoredAdapter.name: keep the retired key, so the class disagrees with the registry and the configuration

- File: `src/cratekit/acquire/vendored.py`
- Source: `u197.json`, row `M5_adapter_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_acquire_workers.py`
- Collected: 643 against a baseline of 643
- Kills: 11 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_every_registered_adapter_loads_with_no_third_party_tool_installed`
  - `tests/test_adapter_contract.py::test_the_retired_vendored_key_resolves_to_the_same_adapter`
  - `tests/test_doctor.py::test_a_configuration_naming_the_retired_vendored_key_passes_the_adapter_check`
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`

Old text:

```
    name = "vendored"
```

New text:

```
    name = "tidal_dl_ng"
```

### `u47-author.R195_drop_ffmpeg_key`

Drop path_binary_ffmpeg from the settings mapping, which is exactly the state that landed a 320k AAC file with doctor reporting green

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R195_drop_ffmpeg_key`
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
(empty)
```

### `u47-author.R197_drop_event_abort`

Drop event_abort from the downloader construction, the argument whose absence killed item() on its first line

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_drop_event_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`
  - `tests/test_adapter_contract.py::test_a_rate_limited_album_read_reaches_the_item_cause_by_name`
  - `tests/test_adapter_contract.py::test_a_session_the_tool_saw_rejected_is_an_invocation_auth_failure`
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`
  - `tests/test_adapter_contract.py::test_the_run_event_is_set_and_the_abort_event_is_clear`

Old text:

```
            event_abort=event_abort,

```

New text:

```
(empty)
```

### `u47-author.SAMPLE_quality_equality`

Existing guard: compare the quality string for equality rather than matching, so a new lossless tier upstream starts being refused

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `SAMPLE_quality_equality`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_the_clients_quality_vocabulary[HI_RES_LOSSLESS-True]`

Old text:

```
        return Offer(lossless="LOSSLESS" in quality.upper(), detail=quality)
```

New text:

```
        return Offer(lossless=quality.upper() == "LOSSLESS", detail=quality)
```

### `u254.M06_never_cache`

mark_applied: never remember what this process left, so every mark reads the whole ledger again

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M06_never_cache`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`

Old text:

```
        if left is not None:
            _LEFT[key] = left
```

New text:

```
        if left is not None:
            pass
```

### `u254.M15_header_string_version`

_read_journal: drop the integer check on the header's schema_version

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M15_header_string_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header with a string version]`

Old text:

```
    header = json.loads(lines[0].decode("utf-8"))
    version = header.get("schema_version")
    if not isinstance(version, int):
```

New text:

```
    header = json.loads(lines[0].decode("utf-8"))
    version = int(header.get("schema_version"))
    if not isinstance(version, int):
```

### `r1991.A2_shared_pair_recorded`

planned_destinations: record a pair two destinations share as one of them

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r1991.json`, row `A2_shared_pair_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_outside_root.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_filing.py`, `tests/test_organize.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_second_genre_guards_counts.py`
- Collected: 521 against a baseline of 521
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_planned_destinations_name_each_pair_once_and_skip_what_names_none`

Old text:

```
if len(found) == 1}
```

New text:

```
if found}
```

### `r788-d.A3_present_rows_handed_over`

vocal_locations: every planned membership is handed to the writer, the present ones too

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r788-d.json`, row `A3_present_rows_handed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
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

### `u27-adopt-apply-author.S1_no_session_at_all`

Run the apply loop with no destructive session around it (the residual's condition, unchanged)

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `S1_no_session_at_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 17 against a baseline of 17
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

### `u55-collection-reader.R27_apply_no_tag_value`

A tag_value supplier is installed, so the apply writes a genre onto the person's files

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R27_apply_no_tag_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_an_apply_records_the_node_of_each_destination_it_filed_into`

Old text:

```
    report, gathered = apply_outstanding(cfg, plan, declared, actor=actor)
```

New text:

```
    report, gathered = apply_outstanding(
        cfg, plan, declared, actor=actor, tag_value=lambda entry, _d: entry.bucket or None
    )
```

### `u23-round-8-independent.X4_approval_digest_unchecked`

An approval given for a different plan is accepted

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X4_approval_digest_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_for_a_different_plan_is_refused`

Old text:

```
    if approval.digest != current:
```

New text:

```
    if approval.digest is None:
```

### `r780-a.A12_unnamed_not_left_in_tree_path`

a double held through a renamed playlist in a bucket the genre does not name is planned for a removal the writer cannot make

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A12_unnamed_not_left_in_tree_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_with_nothing_to_move_on_is_left_and_listed_under_its_reason[under-another-name-elsewhere]`

Old text:

```
    if unnamed:
        reason = LEFT_UNNAMED
    elif bucket in refused:
```

New text:

```
    if bucket in refused:
```

### `r797-b.M7_a_track_still_there_is_listed`

buckets_asked: never ask a bucket about a track that holds nothing there but a former place, so the old playlist reads as empty while it holds tracks

- File: `src/cratekit/adopt/move.py`
- Source: `r797-b.json`, row `M7_a_track_still_there_is_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
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
        if bucket.formerly and in_former_place_only(
```

New text:

```
        if False and in_former_place_only(
```

### `u118-c.M7_unnamed_reason`

An unclaimed Soul track in a renamed R&B band is listed as no reading

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M7_unnamed_reason`
- Moved: the split place reasons are now the ladder _listed; the unnamed reason is never given, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_an_unreadable_soul_file_in_r_and_b_is_listed_under_soul_and_not_moved`

Old text:

```
    if unnamed:
        reason = LEFT_UNNAMED
    elif refused:
```

New text:

```
    if False:
        reason = LEFT_UNNAMED
    elif refused:
```

### `r758-b.C9_read_back_is_not_the_verdict`

the job fails only when the writer raised, so tracks still in both subs drive it to succeeded

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C9_read_back_is_not_the_verdict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_removal_that_did_not_take_fails_the_job_though_nothing_raised`

Old text:

```
    if interrupted is not None or unfinished:
```

New text:

```
    if interrupted is not None:
```

### `r780-a.A7_doubled_rows_not_carried`

the placement reader drops the multiplicity the tree walk counted, so a pair held by two rows is never listed

- File: `src/cratekit/adopt/placements.py`
- Source: `r780-a.json`, row `A7_doubled_rows_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 128 against a baseline of 128
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_an_approved_move_adds_the_new_sub_and_removes_the_old`
  - `tests/test_adopt_move.py::test_the_gate_shows_every_move_with_what_it_adds_removes_and_reads`
  - `tests/test_adopt_placements.py::test_a_double_in_a_renamed_recorded_node_is_still_a_double`
  - `tests/test_adopt_placements.py::test_a_pair_held_by_two_rows_is_held_once_and_doubled`

Old text:

```
            for content_id in {cid for node in answering for cid in node.doubled}:
```

New text:

```
            for content_id in ():
```

### `r797-b.M2_recorded_under_the_old_sub`

recorded_under: ask for a former place's node under the bucket that now declares it, so a renamed old playlist reads as absent

- File: `src/cratekit/adopt/placements.py`
- Source: `r797-b.json`, row `M2_recorded_under_the_old_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_is_found_in_the_folder_of_the_bucket_that_held_it`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`

Old text:

```
    return former.bucket, former.sub
```

New text:

```
    return bucket_id, sub_id
```

### `r722.P3_verdict_drops_level`

with_verdicts resolves an answered genre with no reading

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P3_verdict_drops_level`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_genre_verdict_lands_in_the_band_the_census_read`

Old text:

```
        sub = _sub_for(declared, chosen, entry.genre, entry.energy)
```

New text:

```
        sub = _sub_for(declared, chosen, entry.genre, None)
```

### `r731-a.M05_unnamed_without_held`

an unnamed sub is no longer required to be one the track holds

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M05_unnamed_without_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_an_unnamed_sub_the_track_does_not_hold_changes_nothing`

Old text:

```
    unnamed = tuple(sorted(set(placements.holds_unnamed(bucket, content_id)) & set(held)))
    if not held or (sub in held and sub not in unnamed):
```

New text:

```
    unnamed = tuple(sorted(set(placements.holds_unnamed(bucket, content_id))))
    if (not held and not unnamed) or (sub in held and sub not in unnamed):
```

### `r788-a.P2_blind_plan_files`

vocal_place: drop the filing check, so a tree nobody read, a taxonomy with no vocal sub and an uncalibrated library all file from the tag

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P2_blind_plan_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_library_with_no_calibrated_cut_plans_no_vocal_membership`
  - `tests/test_adopt_vocals.py::test_a_tree_nobody_read_plans_no_vocal_membership`
  - `tests/test_adopt_vocals.py::test_each_reason_nothing_can_be_filed_plans_nothing_for_a_tagged_track`

Old text:

```
    if not vocals.filing or not vocals.carries(content_id):
```

New text:

```
    if not vocals.carries(content_id):
```

### `r788-b.P17_withheld_presence_is_planned`

PlanEntry.vocal_planned: drop applicable, so a withheld track's vocal membership is one an apply may write

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P17_withheld_presence_is_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_withheld_track_already_in_its_vocal_sub_reads_present_and_is_not_digested`

Old text:

```
        return self.applicable and self.vocal in VOCAL_PLANNED
```

New text:

```
        return self.vocal in VOCAL_PLANNED
```

### `u956.O16_row_names_no_location`

outside_row: name the row by its resolved path in the location field, so the gate shows a place rekordbox never recorded

- File: `src/cratekit/adopt/plan.py`
- Source: `u956.json`, row `O16_row_names_no_location`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adopt_apply_cli.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`
  - `tests/test_adopt_outside_root.py::test_the_plan_counts_and_names_every_row_it_leaves_outside`

Old text:

```
    return {"content_id": entry.content_id, "location": entry.recorded, "path": entry.path}
```

New text:

```
    return {"content_id": entry.content_id, "location": entry.path, "path": entry.path}
```

### `u23-round-8-independent.B1_settled_never_refuses`

Round 7 restored: the two converging-address shapes accept unconditionally

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `B1_settled_never_refuses`
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
    if _nothing_unrecorded_is_at_risk(record, written=written, current=current):
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):

```

New text:

```
    if True:
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):

```

### `u23-round-8-independent.E4_vacancy_always_true`

Every record is stranded, so every record is a byte-search candidate

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E4_vacancy_always_true`
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
    return True

```

### `u23-round-8-independent.X12_look_at_drops_the_regular_file_test`

A directory or a fifo at the recorded path reaches the hash

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `X12_look_at_drops_the_regular_file_test`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIRECTORY_at_the_recorded_path_refuses_as_ITS_OWN_reason`
  - `tests/test_adoption.py::test_a_FIFO_at_the_recorded_path_refuses_instead_of_blocking_forever`

Old text:

```
    if not stat_module.S_ISREG(info.st_mode):
        return _Looked(ByteRead.NOT_A_REGULAR_FILE)

```

New text:

```
(empty)
```

### `u23-round-8-independent.X14_probe_drops_the_dataless_test`

A cloud-evicted file is probed by reading it, so the census downloads

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent.json`, row `X14_probe_drops_the_dataless_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_online_only_file_is_never_opened_by_the_probe`

Old text:

```
    if _is_dataless(info):
        return Readability.ONLINE_ONLY

```

New text:

```
(empty)
```

### `u956.O1_confine_guard_gone`

scan_rows: never read a row as outside the root, so a sampler preset mapped outside it routes and the apply fails the pass again (the card itself)

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O1_confine_guard_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 687 against a baseline of 687
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
        if readability is None and confine_to_root and not within_root(path or "", root):
```

New text:

```
        if False:
```

### `u956.S20_tombstone_scanned`

existing, scan_rows: census a tombstone, so adopting a removed track would put it back

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `S20_tombstone_scanned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 687 against a baseline of 687
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adoption.py::test_a_soft_deleted_row_is_not_proposed_for_adoption`

Old text:

```
        if row.deleted:
            continue
        path, readability = _resolved_path(
```

New text:

```
        path, readability = _resolved_path(
```

### `u241.M23_identity_without_the_size`

ahead.identity_of: no size, so a file rewritten with its time put back keeps its old head

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M23_identity_without_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_rewritten_with_its_time_put_back_is_measured_again_by_its_size_alone`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)

```

New text:

```
    return (found.st_dev, found.st_ino, 0, found.st_mtime_ns)

```

### `u223.M2_keep_linked_intent`

staged_path: keep an intent that is a link, so the clear keeps it and rename_intent follows it

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M2_keep_linked_intent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_is_cleared_rather_than_kept_and_followed`

Old text:

```
                and entry.is_file()
                and not entry.is_symlink()
            ):
```

New text:

```
                and entry.is_file()
            ):
```

### `u306.A5_item_record_owner`

analysis.artifacts._item_record: take a record written for another item as this one's, so a resume renames or reports by a neighbour's record

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u306.json`, row `A5_item_record_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_drift.py`, `tests/test_shared_homes.py`
- Collected: 318 against a baseline of 318
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_rename_intent_for_another_item_or_a_gone_target_is_not_a_twin`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
```

New text:

```
    if not isinstance(loaded, dict):
```

### `u90-b.B1_library_root_unchecked`

The hand path stops requiring the library root before it writes

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B1_library_root_unchecked`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_refuses_with_the_library_away`

Old text:

```
    _require_library_root(cfg)
    previous, before = _previous_vocal_cut(cfg)
```

New text:

```
    previous, before = _previous_vocal_cut(cfg)
```

### `u90-c.C2_unreadable_refuses`

An unreadable calibration refuses the hand cut instead of being replaced by it

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-c.json`, row `C2_unreadable_refuses`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`

Old text:

```
        return None, "the calibration on record before could not be read, and this replaces it"
```

New text:

```
        raise
```

### `u94-a.S7_samefile_to_spelling`

_is_library_wide: compare two spellings instead of asking the filesystem, so the root reached through a link is not the root

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S7_samefile_to_spelling`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_root_reached_through_a_link_is_still_the_root`

Old text:

```
            if os.path.samefile(folder, candidate):
```

New text:

```
            if str(folder) == str(candidate):
```

### `u94-b.W8_note_forgets_the_omission`

fitted_note: never record how many folders were not walked, so the file a later restamp trusts reads as a whole fit

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W8_note_forgets_the_omission`
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
    if left_out:
        note +=
```

New text:

```
    if False:
        note +=
```

### `r395.M9_worker_literal`

Put the old bare pip literal back in the analysis worker refusal

- File: `src/cratekit/analysis/cli.py`
- Source: `r395.json`, row `M9_worker_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_missing_extra_refuses_the_item_rather_than_skipping_it_as_keyless`

Old text:

```
"install": extras.install_command("analysis")
```

New text:

```
"install": "pip install 'cratekit[analysis]'"
```

### `u223.M15_folder_unchecked`

_staged_twin: accept a path outside the item's own folder

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M15_folder_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if target.parent != source.parent:
        return None
    return target
```

New text:

```
    return target
```

### `u306.A2_zero_state`

analysis.cli.nothing_to_queue: the default state of an empty folder reworded, so the no job payload names another state

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A2_zero_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_with_no_audio_queues_nothing_and_says_so`
  - `tests/test_analysis_workers.py::test_a_restamp_over_an_empty_folder_is_the_honest_zero_whatever_the_calibration`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_vocals_cli.py::test_a_folder_with_no_audio_queues_nothing`

Old text:

```
    ctx, folder: Path, extra: tuple[dict[str, str], ...] = (), *, state: str = "no-audio"
```

New text:

```
    ctx, folder: Path, extra: tuple[dict[str, str], ...] = (), *, state: str = "no-audio-found"
```

### `u343.M06_handle_run_no_resume_skip`

handle_run: never skip a measured file, so a resume measures and writes every file again

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M06_handle_run_no_resume_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_restamp_scored_by.py`
- Collected: 482 against a baseline of 482
- Kills: 10 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_carrying_its_head_and_a_file_that_is_gone_are_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_workers.py::test_a_file_beside_its_headed_twin_is_measured_where_it_is_and_named_nothing`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_restamp_scored_by.py::test_a_file_the_run_did_not_score_is_restamped_and_the_rest_left_out`
  - `tests/test_restamp_scored_by.py::test_a_resumed_tail_restamps_every_file_since_its_run_scored_none`
  - `tests/test_restamp_scored_by.py::test_a_tail_pass_restamps_the_file_the_run_did_not_score_and_counts_the_rest`

Old text:

```
    artifacts.discard_rename_evidence(cfg, job, item)
    if already_measured(path, cfg):
```

New text:

```
    artifacts.discard_rename_evidence(cfg, job, item)
    if False:
```

### `u58-workers-and-wav.S2_unchanged_rewritten`

Rewrite a file whose level did not move

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S2_unchanged_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_whose_level_did_not_move_is_reported_unchanged_and_not_rewritten`

Old text:

```
    if previous != level:
```

New text:

```
    if True:
```

### `u263.D15_chunk_padding`

_parse_float_wav: skip an odd sized chunk without its pad byte

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D15_chunk_padding`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_extensible_header_and_a_chunk_before_the_data_are_read`

Old text:

```
        position = body + size + (size & 1)
```

New text:

```
        position = body + size
```

### `u264.M10_window_dropped`

decode.load: read the whole file through librosa, dropping the offset and duration

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M10_window_dropped`
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
        native, native_rate = librosa.load(str(path), sr=None, mono=False)
```

### `u264.M4_table_rule_1_0`

_MEASURED_MIX: give 1.0.0 the rule of the releases before it

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M4_table_rule_1_0`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_only_a_measured_release_takes_the_one_add[1.0.0-True]`

Old text:

```
    "1.0.0": True,
```

New text:

```
    "1.0.0": False,
```

### `u157.D1_band_narrow`

DRIFT_BAND: back to the first band of 0.12, so the other section of a two tempo track falls outside it

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D1_band_narrow`
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
DRIFT_BAND = 0.12
```

### `u263.D16_head_no_decoder`

detect.analyse_file: report a missing decoder as undecodable, blaming the file

- File: `src/cratekit/analysis/detect.py`
- Source: `u263.json`, row `D16_head_no_decoder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except decode.DecoderMissing:
        return {"path": path, "terminal": TERMINAL_NO_DECODER}

```

New text:

```
(empty)
```

### `u58-workers-and-wav.E1_beatless_cap`

Drop the beatless cap in the energy scorer

- File: `src/cratekit/analysis/energy.py`
- Source: `u58-workers-and-wav.json`, row `E1_beatless_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_beatless_guard_caps_a_loud_track_with_no_onsets`

Old text:

```
    if calibration.onset_floor is not None:
        density = float(features.get("onset_density", math.inf))
        if not math.isnan(density) and density < calibration.onset_floor:
            level = min(level, BEATLESS_CAP)

```

New text:

```
(empty)
```

### `u327.A18_file_read_back`

write_files: trust the write, so a file that does not read back as planned has its row written

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A18_file_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_that_does_not_read_back_keeps_its_row_s_title_and_is_named`

Old text:

```
        if unreadable or title != item.new_tag_title or initialkey != item.new_initialkey:
```

New text:

```
        if unreadable:
```

### `u327.A9_tag_body_compared`

plan_row: drop the title tag body comparison, so a file whose tag names another title is rewritten

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A9_tag_body_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`

Old text:

```
    if new_tag is None or split_head(tag_title, template=template)[1] != split_head(
        title, template=template
    )[1]:
```

New text:

```
    if new_tag is None:
```

### `u342.P4_stamped_apart`

plan_row: plan a stamped row as adopt, so the plan does not show it apart

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P4_stamped_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 10 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`
  - `tests/test_analyze_adopt.py::test_a_headless_title_is_planned_stamped_apart_from_the_corrected_rows`
  - `tests/test_analyze_adopt.py::test_a_second_run_after_a_stamp_plans_nothing_and_ends_no_op`
  - `tests/test_analyze_adopt.py::test_a_stamped_row_is_counted_written_and_never_as_left`
  - `tests/test_analyze_adopt.py::test_leave_holds_a_stamped_row_out_in_the_plan_and_on_the_apply`
  - `tests/test_analyze_adopt.py::test_rows_not_analysed_with_no_head_or_a_differing_tag_are_left_and_named`
  - `tests/test_analyze_adopt.py::test_the_apply_stamps_title_title_tag_and_key_tag_and_nothing_else`
  - `tests/test_analyze_adopt.py::test_the_check_names_adopt_for_the_bare_titles_a_landing_since_u343_leaves`
  - `tests/test_restore_tags.py::test_a_restore_puts_a_stamped_row_and_its_file_back_with_no_head`

Old text:

```
        action = STAMPED

```

New text:

```
        action = ADOPT

```

### `u342.C2_written_counts_what_took`

_written: count every stamped row planned as written, whether its file took it or not

- File: `src/cratekit/analysis/head_adopt_cli.py`
- Source: `u342.json`, row `C2_written_counts_what_took`
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
item.action == ha.STAMPED)
```

### `u275.M4_base_rounded_down`

LIGHT_BASE_BYTES rounded down to 352 megabytes, over the measured intercept but under an eighth above it

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M4_base_rounded_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_ahead_real.py`, `tests/test_head_agreement.py`, `tests/test_drift.py`
- Collected: 555 against a baseline of 555
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_file_stored_at_a_high_rate_costs_its_decode_and_not_only_its_length`
  - `tests/test_analysis_ahead.py::test_a_length_the_header_will_not_give_is_bounded_by_the_files_size`
  - `tests/test_analysis_ahead.py::test_a_light_workers_cost_is_the_measured_line_in_the_tracks_length`
  - `tests/test_analysis_ahead.py::test_each_measured_mac_peak_is_under_what_its_length_declares[236-987]`
  - `tests/test_analysis_ahead.py::test_the_declared_line_keeps_the_linux_margin_over_the_macs_measured_line`

Old text:

```
LIGHT_BASE_BYTES = 384 * 1024 * 1024
```

New text:

```
LIGHT_BASE_BYTES = 352 * 1024 * 1024
```

### `u343.M11_mark_value_empty`

MARK_VALUE: an empty mark, which the writer skips, so no file is ever marked

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M11_mark_value_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`, `tests/test_restamp_scored_by.py`
- Collected: 264 against a baseline of 264
- Kills: 9 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_batch_resume_skips_a_file_carrying_the_mark_and_reads_the_rest`
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
MARK_VALUE = "1"
```

New text:

```
MARK_VALUE = ""
```

### `sitting3.G4_clip_wrapper`

Build the clip level wrapper again

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G4_clip_wrapper`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis.py::test_default_loader_builds_the_frame_wrapper_from_the_checkpoint_on_disk`

Old text:

```
    from panns_inference import SoundEventDetection

    # The wrapper prints its checkpoint path and device to stdout on
    # construction, and stdout is where the JSON envelope goes.
    with contextlib.redirect_stdout(io.StringIO()):
        return SoundEventDetection(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

New text:

```
    from panns_inference import AudioTagging

    with contextlib.redirect_stdout(io.StringIO()):
        return AudioTagging(checkpoint_path=str(scoring.CHECKPOINT), device="cpu")

```

### `u58-workers-and-wav.W1_voxlevel_zero`

The original defect: score every track voxlevel 0 with a model loaded

- File: `src/cratekit/analysis/vocals.py`
- Source: `u58-workers-and-wav.json`, row `W1_voxlevel_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`
  - `tests/test_analysis_workers.py::test_a_partial_carrying_only_a_path_scores_nonzero_through_the_fixed_path`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_run_batch_threads_the_decoder_through_to_the_vocal_pass`

Old text:

```
    result["voxlevel"] = int(round(score.presence))
```

New text:

```
    result["voxlevel"] = 0
```

### `u92-author.G2_cap_is_inclusive`

Refuse a file exactly AT the cap, strictly greater becomes greater or equal

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G2_cap_is_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_exactly_at_the_cap_is_still_decoded`

Old text:

```
        return Path(path).stat().st_size > VOCAL_MAX_BYTES
```

New text:

```
        return Path(path).stat().st_size >= VOCAL_MAX_BYTES
```

### `u241.M26_warm_up_takes_no_lock`

warm.exclusive: the lock is opened and never taken, so two processes fill the kernel cache together

- File: `src/cratekit/analysis/warm.py`
- Source: `u241.json`, row `M26_warm_up_takes_no_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_warm.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_warm.py::test_two_processes_are_never_inside_the_lock_together`

Old text:

```
        fcntl.flock(handle, fcntl.LOCK_EX)

```

New text:

```
        pass

```

### `r221-b.M1_refusal_step_dropped`

No refusal carries the sentence, so a rehearsal that failed reads as a real backup attempt that fell over

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M1_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    return error
    cause = error.cause
```

### `r222-b.B1_always_enqueue`

Never report a twin, which is the finding itself: every ask files another job

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B1_always_enqueue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 8 (killed)
- Killed:
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
        if found is not None:
            twin, frozen = found
```

New text:

```
        if False:
            twin, frozen = found
```

### `r222-b.B9_mirror_not_compared`

Compare only the archive root, so two jobs syncing into one mirror with different archives are strangers

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B9_mirror_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[dest]`

Old text:

```
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
```

New text:

```
            frozen.backup.archive_root == cfg.backup.archive_root
```

### `r349-c.C2_write_failure_step`

A failed record write returns the refusal without the step saying the record is missing

- File: `src/cratekit/backup/cli.py`
- Source: `r349-c.json`, row `C2_write_failure_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except OSError as exc:
        cause = refusal.cause
```

New text:

```
    except OSError as exc:
        return refusal
        cause = refusal.cause
```

### `u311.B3_iso_drops_a_present_moment`

The backup ages report a recorded moment as none

- File: `src/cratekit/backup/cli.py`
- Source: `u311.json`, row `B3_iso_drops_a_present_moment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 218 against a baseline of 218
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_report_carries_the_age_number_and_not_only_the_state`

Old text:

```
    return moment.isoformat() if moment is not None else None
```

New text:

```
    return None
```

### `u45-round-1.H2_queueing_plans_first`

Plan inside the handler, so queueing refuses on a machine with no rclone where the work would have run fine

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `H2_queueing_plans_first`
- Moved: Anchored where u325-replay-after.json replayed it: Same handler, backup_library; U298 replaced its private _load with cli.output.load_config, so the line the plan is inserted after is reworded and the insertion point is the same
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_queueing_needs_no_rclone_no_remote_and_no_volume`

Old text:

```
    cfg = load_config(("backup.cli",))
    with jobs.open_store() as store:
        if ctx.args.job:
```

New text:

```
    cfg = load_config(("backup.cli",))
    backup.plan_backup(cfg)
    with jobs.open_store() as store:
        if ctx.args.job:
```

### `u45-round-1.W3_ages_not_read_back`

Drop the age read-back, so the verb never reports what a destructive session would see

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W3_ages_not_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report["ages"] = published_ages(cfg, now=now)
```

New text:

```
    report["ages"] = []
```

### `u50-author.B3_items_one_portion_only`

Queue only the mirror, so the database half of every backup is never claimed

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `B3_items_one_portion_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 14 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_an_item_naming_something_that_is_not_a_portion_refuses_by_name`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_queueing_still_needs_nothing_from_the_machine`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_ages_reported_are_the_ones_this_job_published`
  - `tests/test_backup_cli.py::test_the_item_list_is_derived_from_the_portions_rather_than_written_out`
  - `tests/test_backup_cli.py::test_the_outcome_record_is_private_under_a_permissive_umask`

Old text:

```
    return tuple(str(portion) for portion in backup_facts.Portion)
```

New text:

```
    return (str(backup_facts.Portion.FILES),)
```

### `r290-author.D4_cancelled_reads_failed`

Read the cancelled type as the failed outcome, which is what the dispatcher said before Outcome.CANCELLED had a producer

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D4_cancelled_reads_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7231 against a baseline of 7231
- Kills: 22 (killed)
- Killed:
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
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[master]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            outcome = Outcome.CANCELLED
```

New text:

```
            outcome = Outcome.FAILED
```

### `r388-c.M13_credential_step_dropped`

Drop the credential step from the listing failure's reservation

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-c.json`, row `M13_credential_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 660 against a baseline of 660
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-contents]`
  - `tests/modules/test_tools.py::test_a_named_snapshot_whose_listing_fails_sends_the_person_to_the_remote[list-snapshot-identity]`

Old text:

```
            "check the remote's credential has not expired or been revoked, and "
            "reconnect it in rclone if it has",

```

New text:

```
(empty)
```

### `r925.J5_version_dropped`

job show lists every track without its version

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J5_version_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`

Old text:

```
                "version": str(said.get("version") or ""),
```

New text:

```
                "version": "",
```

### `r682-a.M11_unstated_bound_inclusive`

a complete breakdown prints unstated 0

- File: `src/cratekit/cli/render.py`
- Source: `r682-a.json`, row `M11_unstated_bound_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 122 against a baseline of 122
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_render_payloads.py::test_rows_no_reason_explains_are_said_rather_than_read_as_complete[complete]`
  - `tests/test_render_payloads.py::test_the_reasons_follow_their_count_most_rows_first_and_ties_by_slug`

Old text:

```
    if unstated > 0:
```

New text:

```
    if unstated >= 0:
```

### `r685-a.L6_a_permission_is_a_defect_to_report`

The unreadable branch always says report a defect, never grant access

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L6_a_permission_is_a_defect_to_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),

```

New text:

```
            remedy=Remedy.REPORT_DEFECT,

```

### `u260.E12_key_digest_of_64_kb`

to_cdj_jpeg_remembered: digest only the first 64 KB, the prefix round two found surviving the first header test

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E12_key_digest_of_64_kb`
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
    key = (hashlib.sha256(data[:65536]).digest(), len(data), size, max_bytes)
```

### `u260.E9_encode_evicts_newest`

to_cdj_jpeg_remembered: evict the newest entry instead of the least recently used

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E9_encode_evicts_newest`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest`

Old text:

```
            _remembered.popitem(last=False)
```

New text:

```
            _remembered.popitem(last=True)
```

### `u83-a.E6_exif_orientation`

The encoder stops applying the EXIF orientation before the re-encode drops the tag

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E6_exif_orientation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_art.py::test_an_exif_orientation_is_baked_into_the_pixels`

Old text:

```
_flatten_to_rgb(ImageOps.exif_transpose(source))
```

New text:

```
_flatten_to_rgb(source)
```

### `u83-b.W12_container_refusal`

A container with no verified picture handling is no longer refused

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W12_container_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[.ogg]`
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[.opus]`
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[.xyz]`
  - `tests/test_art.py::test_a_container_without_verified_picture_handling_raises[]`
  - `tests/test_art.py::test_the_container_check_comes_before_the_image_check`

Old text:

```
    if suffix not in ART_SUFFIXES:
```

New text:

```
    if False:
```

### `u83-b.W8_flac_clear_pictures`

The FLAC writer appends instead of replacing

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W8_flac_clear_pictures`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_flac_picture_of_another_type_is_replaced_too`
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.flac]`

Old text:

```
            handle.clear_pictures()

```

New text:

```
(empty)
```

### `u317.Q18_week_doubled`

_full_check_schedule: a full check is due at twice the week, so an eight day old one is not run

- File: `src/cratekit/core/backup_facts.py`
- Source: `u317.json`, row `Q18_week_doubled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if answer.age is None or answer.age >= timedelta(days=FULL_CHECK_DAYS):
```

New text:

```
    if answer.age is None or answer.age >= timedelta(days=2 * FULL_CHECK_DAYS):
```

### `u331.S01_yt_dlp_subject_dropped`

binaries.yt_dlp_missing: drop the caller's subject from the refusal's detail, so acquire fallback and intake set no longer name the track or set it was for

- File: `src/cratekit/core/binaries.py`
- Source: `u331.json`, row `S01_yt_dlp_subject_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/intake/test_set_fetch.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_missing_yt_dlp_refuses_a_url_with_the_install_hint`

Old text:

```
            "packages": list(hint.packages) if hint is not None else [],
            **subject,
```

New text:

```
            "packages": list(hint.packages) if hint is not None else [],
```

### `u45-round-1.V2_summary_slug_undeclared`

Remove backup-nothing-ran from the registry, so its raise site raises UnknownReason at the boundary

- File: `src/cratekit/core/cause.py`
- Source: `u45-round-1.json`, row `V2_summary_slug_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5516 against a baseline of 5516
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        "backup-nothing-ran": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u94-b.W9_walk_warning_says_queued`

discovery.walk_warnings: ignore the verb for a declined link, so calibrate tells a person about a queue it does not have

- File: `src/cratekit/core/discovery.py`
- Source: `u94-b.json`, row `W9_walk_warning_says_queued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_walk_that_left_a_folder_out_is_not_the_library`

Old text:

```
        link_warning(tuple(skipped_links), verb),
```

New text:

```
        link_warning(tuple(skipped_links)),
```

### `r390-a.A2_retry_refuses_any_closed_job_with_a_cause`

the flag is not read: a cancelled job and a retryable failure are refused too

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A2_retry_refuses_any_closed_job_with_a_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_backup_cli.py`, `tests/test_outbound_workers.py`
- Collected: 296 against a baseline of 296
- Kills: 9 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_jobs.py::test_a_cancelled_job_can_be_resumed_and_a_succeeded_one_cannot`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
```

New text:

```
    if current.cause is not None:
        raise refuse(
            "job-not-retryable",
```

### `u169.E4_decline_drops_cause`

decline_item: keep no cause on the skipped item, so nothing can name why

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E4_decline_drops_cause`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 153 against a baseline of 153
- Kills: 10 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.SKIPPED), None, job_id, item_id),
```

### `u241.M08_plan_forgets_which_gate`

plan_pool: a plan refused by pressure no longer carries which gate refused it

- File: `src/cratekit/core/pool.py`
- Source: `u241.json`, row `M08_plan_forgets_which_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_stream.py`, `tests/test_analysis_ahead.py`
- Collected: 298 against a baseline of 298
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_run_that_fails_part_way_says_its_pool_on_the_refusal_and_matches_the_serial_run`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_both_gates_names_both_swap_first`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_swap_names_the_gate_the_reading_and_the_limit`
  - `tests/test_pool_stream.py::test_a_plan_refused_by_the_used_percent_names_that_gate`

Old text:

```
            ceiling=ceiling,
            refused_by=refused,

```

New text:

```
            ceiling=ceiling,

```

### `u301.G5_report_state_reads_garbage_as_fresh`

_report_state: read a state file that is not a JSON object as a fresh one, so a report shows nothing spent over a file it never read

- File: `src/cratekit/core/provider_gate.py`
- Source: `u301.json`, row `G5_report_state_reads_garbage_as_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_the_report_reader_says_when_it_could_not_read_the_file`

Old text:

```
    return _State.from_json(data) if isinstance(data, dict) else None
```

New text:

```
    return _State.from_json(data if isinstance(data, dict) else {})
```

### `r239-a.A9_header_nearby_value`

The plain header constant to a realistic nearby value, SQLite format 4, so no plain file matches it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A9_header_nearby_value`
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
SQLITE_HEADER = b"SQLite format 3"
```

New text:

```
SQLITE_HEADER = b"SQLite format 4"
```

### `u118-b.R2_split_lookup`

split_place finds nothing, so a split place resolves as an ordinary sub

- File: `src/cratekit/core/routing.py`
- Source: `u118-b.json`, row `R2_split_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`
- Collected: 102 against a baseline of 102
- Kills: 14 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_the_old_soul_r_and_b_playlist_moves_to_soul_and_is_withheld_until`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[rnb]`
  - `tests/test_adopt_split_place.py::test_a_split_pairs_soul_band_move_is_written_read_back_and_keeps_its_r_and_b_band[soul]`
  - `tests/test_adopt_split_place.py::test_a_split_place_competes_in_soul_and_nowhere_else`
  - `tests/test_adopt_split_place.py::test_a_split_place_is_found_as_the_r_and_b_place_it_is`
  - `tests/test_adopt_split_place.py::test_a_track_in_an_r_and_b_band_holds_it_in_r_and_b_and_the_split_place_in_soul`
  - `tests/test_adopt_split_place.py::test_a_track_in_the_old_hip_hop_playlist_holds_its_former_place_in_both_buckets`
  - `tests/test_adopt_split_place.py::test_an_approved_move_files_soul_and_hip_hop_in_their_folders_and_keeps_r_and_b`
  - `tests/test_adopt_split_place.py::test_the_gate_shows_every_soul_and_hip_hop_track_moving_and_no_r_and_b_track`
  - `tests/test_adopt_split_place.py::test_the_writer_is_told_to_add_the_soul_band_and_leave_the_r_and_b_band_by_name`

Old text:

```
    for place in taxonomy.bucket(bucket_id).split_from:
```

New text:

```
    for place in ():
```

### `r722.T8_lenient_energy_raises`

read_energy_from_file stops folding a failed read into None

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T8_lenient_energy_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2994 against a baseline of 2994
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None
```

New text:

```
    return read_energy_checked(path)
```

### `u118-b.A1_tag_beats_route`

A bucket's tagging only word no longer wins over another bucket's routing alias, so Trap / Wave tags as the breaks bucket

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u118-b.json`, row `A1_tag_beats_route`
- Moved: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_adopt_split_place.py`, `tests/test_routing_parity.py`
- Collected: 1070 against a baseline of 1070
- Kills: 4 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_each_word_tags_as_the_folder_the_author_gave_it_and_the_tag_routes_there[Trap / Wave-Hip-Hop]`
  - `tests/test_routing_parity.py::test_tagging_matches_the_old_tagger_except_on_a_declared_refusal[trap / wave]`
  - `tests/test_routing_parity.py::test_the_three_strings_the_two_old_tables_flatly_contradicted[Trap / Wave-Hip-Hop]`
  - `tests/test_taxonomy.py::test_a_tagging_only_word_wins_over_another_buckets_routing_alias`

Old text:

```
            tagged[key] = bucket.id
            tagging[key] = (bucket.id, None)
```

New text:

```
            tagged[key] = bucket.id
            tagging.setdefault(key, (bucket.id, None))
```

### `r706-a.A1_ceiling_dropped`

Drop the parts ceiling, so a file of any length is cut into as many parts as it takes

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-a.json`, row `A1_ceiling_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 6 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_nonsense_duration_is_refused_by_the_bound_before_any_grid_exists`
  - `tests/intake/test_recognition.py::test_a_recording_over_the_parts_ceiling_is_refused_before_any_carve_call_or_credential`
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_and_neither_spend_refusal_is_a_miss`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_recognition.py::test_the_per_run_bound_refuses_before_any_carve_call_or_credential`
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

### `r706-b.B2_parts_needed_floors`

parts_needed floors instead of ceiling, so 732 chunks is one part of 732

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B2_parts_needed_floors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
- Kills: 7 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_five_hour_mix_is_identified_in_two_even_parts_as_one_set`
  - `tests/intake/test_recognition.py::test_a_two_hour_set_is_one_run_a_five_hour_mix_is_two_parts_and_nine_hours_is_over_the_ceiling`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[401-400-sizes3]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[5-2-sizes6]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[7-3-sizes7]`
  - `tests/intake/test_recognition.py::test_partition_cuts_the_grid_into_the_fewest_even_parts_under_the_bound[732-400-sizes4]`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
    return -(-planned // per_run)
```

New text:

```
    return max(1, planned // per_run)
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

### `u103-a.A5_offset_must_be_planned`

Serve a kept answer at an offset the plan never asked for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A5_offset_must_be_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
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

### `u57-recognition-and-items.M1_miss_family_loses_1001`

1001, the service's own no result code, falls out of the miss family

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M1_miss_family_loses_1001`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 39 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[chunk-plan]`
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[file]`
  - `tests/intake/test_recognition.py::test_a_changed_file_plan_or_host_misses_the_cache[host]`
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
  - `tests/intake/test_recognition.py::test_a_set_nobody_recognised_is_zero_rows_and_neither_spend_refusal_is_a_miss`
  - ... and 24 more, see the JSON sidecar

Old text:

```
_MISS_CODES = frozenset({1001, 2004, 3015})
```

New text:

```
_MISS_CODES = frozenset({2004, 3015})
```

### `u259.M5_member_reads_nothing`

analyzed.member: judge no row instead of the row read by ID, so the clear reads every member as missing

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M5_member_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_inbox_analyzed.py`
- Collected: 85 against a baseline of 85
- Kills: 16 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_collection_whose_ids_are_stored_as_integers_reads_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_row_the_binding_cannot_load_after_one_that_refuses_still_refuses_as_it_did`
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_row_whose_removal_marker_cannot_be_read_refuses_as_it_did[analyze]`
  - `tests/test_analyze_check.py::test_a_row_whose_removal_marker_cannot_be_read_refuses_as_it_did[unanalysed]`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_over_every_row`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    return judge(content_id, db.get_content(ID=content_id))
```

New text:

```
    return judge(content_id, None)
```

### `r682-a.M4_state_keys_not_seeded`

by_reason carries only the states some row reached, so suppressed with no rows is absent rather than an empty mapping

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M4_state_keys_not_seeded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
        "by_reason": by_reason,

```

New text:

```
        "by_reason": {word: reasons for word, reasons in by_reason.items() if reasons},

```

### `u104-e.E3_honest_zero_names_the_address`

Report the scratch file's path as the source of a mix nobody recognised

- File: `src/cratekit/intake/cli.py`
- Source: `u104-e.json`, row `E3_honest_zero_names_the_address`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_nobody_recognised_is_an_honest_zero_that_names_the_address`

Old text:

```
                    chunks=result.chunks,
                    source=held.ref,
```

New text:

```
                    chunks=result.chunks,
                    source=str(held.path),
```

### `u213.M9_readable_order_holds_unread`

list_playlist_readable: order only the tracks that read, so a twin's snapshot drops the unread track

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M9_readable_order_holds_unread`
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
        order.setdefault(ref, None)
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
```

New text:

```
        try:
            read.append(match.read_row(row, origin=match.TIDAL, position=position))
            order.setdefault(ref, None)
```

### `u70.S6_source_id_only_for_hearts`

Every playlist job is stamped source_id favorites, so a playlist reads as the hearts listing

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S6_source_id_only_for_hearts`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_playlist_reference_still_reaches_the_playlist_and_not_the_hearts`

Old text:

```
            source_id=FAVORITES_SOURCE_ID if hearts else None,
```

New text:

```
            source_id=FAVORITES_SOURCE_ID,
```

### `u103-b.C3_out_must_be_a_folder`

Drop the check, made before the spend, that --out is not a file

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C3_out_must_be_a_folder`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_tracklist_folder_that_is_a_file_is_refused_before_any_spend`

Old text:

```
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no tracklist can be written into "
```

New text:

```
    if False:
        raise _unusable(
            f"{out} exists and is not a folder, so no tracklist can be written into "
```

### `u104-e.E2_timeout_is_retryable`

Stop calling a timed out download retryable, the one fetch failure known to be worth running again

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-e.json`, row `E2_timeout_is_retryable`
- Moved: the text moved whole from intake/cli.py to intake/cli_identify.py with its function (U307); the tests that killed it, test_a_download_that_timed_out_is_the_one_fetch_failure_called_retryable, were folded by the trim into test_a_fetch_failure_refuses_and_leaves_no_scratch_file, the timeout case of the parametrized fetch failure test, which asserts retryable only for the timeout
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetch_failure_refuses_and_leaves_no_scratch_file[timed-out]`

Old text:

```
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            steps=(
                "run it again later",
```

New text:

```
            remedy=Remedy.RETRY_LATER,
            retryable=False,
            steps=(
                "run it again later",
```

### `r924.F2_no_landed_line`

The fetch never says what landed

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F2_no_landed_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`

Old text:

```
            progress(f"fetched: {megabytes(landed.stat().st_size)} in {elapsed}s")
```

New text:

```
            pass
```

### `u104-b.F5_landing_is_a_file`

Drop the half of the landing check that requires the fetcher's answer to be a file that exists

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-b.json`, row `F5_landing_is_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[not-there]`

Old text:

```
        if not landed.is_file() or scratch.resolve() not in landed.resolve().parents:
```

New text:

```
        if scratch.resolve() not in landed.resolve().parents:
```

### `u104-c.P4_timeout_is_its_own_kind`

Drop the branch that tells a timed out download from every other failed one, so nothing is ever called retryable

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P4_timeout_is_its_own_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_says_a_timeout_as_the_one_retryable_kind`

Old text:

```
            if isinstance(exc.__cause__, subprocess.TimeoutExpired):
                raise SetFetchTimedOut(str(exc)) from exc

```

New text:

```
(empty)
```

### `u307.R16_identify_only_drops_a_field`

pipeline.identify_only: copy every field of recognize.Identified but the last, so the parts count falls to its default

- File: `src/cratekit/intake/pipeline.py`
- Source: `u307.json`, row `R16_identify_only_drops_a_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_workers.py`
- Collected: 75 against a baseline of 75
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
for one in fields(recognize.Identified)}
```

New text:

```
for one in fields(recognize.Identified)[:-1]}
```

### `r675.G10_repair_apply_asks_with_no_candidates`

repair_cli apply: the repair verb's read after the gate hands the guard no candidates

- File: `src/cratekit/intake/repair_cli.py`
- Source: `r675.json`, row `G10_repair_apply_asks_with_no_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_apply_cli.py`, `tests/intake/test_repair_apply.py`
- Collected: 121 against a baseline of 121
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_dark_row_recorded_after_the_gate_refuses_the_repair_before_any_rename`

Old text:

```
        naming_cli.referenced_keys(cfg, renaming=[Path(item["path"]) for item in renames])
```

New text:

```
        naming_cli.referenced_keys(cfg, renaming=[])
```

### `u102-a.U1_no_stored_path`

_unusable_why: drop the refusal over an item the queue holds no path for

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U1_no_stored_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
    if accepted.path is None:
        return (
```

New text:

```
    if False:
        return (
```

### `u102-b.G5_claim`

_apply: skip the atomic claim, so a name taken after the gate is overwritten by the rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G5_claim`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_name_refused_or_taken_after_the_gate_is_named_and_never_overwritten`

Old text:

```
            claimed = naming.claim_target(target)
```

New text:

```
            claimed = True
```

### `u308.L4_translated_swallows_refusal`

catalogue.translated: an adapter's own refusal is translated into the boundary's failure

- File: `src/cratekit/label/catalogue.py`
- Source: `u308.json`, row `L4_translated_swallows_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_workers.py`, `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_favorites_backfill.py`
- Collected: 467 against a baseline of 467
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_refusal_raised_mid_crawl_passes_through_the_listing_boundary_unchanged`
  - `tests/test_favorites_backfill.py::test_a_heart_a_short_listing_did_not_date_is_held_back_not_filed_undated`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`
  - `tests/test_label_workers.py::test_a_refusal_the_artist_lookup_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`
  - `tests/test_label_workers.py::test_a_refusal_the_sweep_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
    except passing:
        raise
    except Exception as exc:
```

New text:

```
    except Exception as exc:
```

### `u237.M5_bare_year_is_a_label`

_YEAR_NUM: strip a year only when a name follows, so a line of a mark and a year offers the year as a label

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M5_bare_year_is_a_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[(P) 2021-expected10]`
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[(P) 2021.-expected11]`
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[2021-expected14]`
  - `tests/modules/test_labels.py::test_only_the_parenthesised_or_symbol_mark_and_the_year_are_stripped[\u2117 2021-expected13]`

Old text:

```
_YEAR_NUM = re.compile(r"^\d{4}(?:\s+|\.?$)")
```

New text:

```
_YEAR_NUM = re.compile(r"^\d{4}\s+")
```

### `r704-a.S2_cause_walk_reads_only_the_error`

the declared cause chain is not walked, so a client error raised from a TooManyRequests reads as permanent

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S2_cause_walk_reads_only_the_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`

Old text:

```
    if any(is_rate_limit(link) for link in _linked(exc, "__cause__")):
```

New text:

```
    if any(is_rate_limit(link) for link in (exc,)):
```

### `u261.O1_catalogue_drops_the_app`

open_catalogue: build the catalogue without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u261.json`, row `O1_catalogue_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 270 against a baseline of 270
- Kills: 3 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_an_app_recorded_after_the_open_is_picked_up_by_the_next_resolve`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
        catalogue=held.app,
```

New text:

```
        catalogue=None,
```

### `u192.F4_command_dropped`

_resumable: the first step says to resume the job without naming the command

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F4_command_dropped`
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
        f"resume it with: {command}",
```

New text:

```
        "resume it with its --job command",
```

### `r356-b.B8_heart_back_drops_the_reason`

An unmatched favourite never carries what the account said about it

- File: `src/cratekit/modules/outbound/hearts.py`
- Source: `r356-b.json`, row `B8_heart_back_drops_the_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_heart_back_hands_the_account_the_names_and_reports_its_reasons`

Old text:

```
            if reason:
                reasons.append((item.row_id, reason))
```

New text:

```
            if False:
                reasons.append((item.row_id, reason))
```

### `r229.L18_contents_grow`

The recorded contents are appended to rather than replaced, which is the ever growing log the review found

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L18_contents_grow`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_an_adopted_record_moves_and_no_playlist_is_created`
  - `tests/modules/test_outbound.py::test_the_move_is_reported_once_under_the_per_item_shape`
  - `tests/modules/test_outbound.py::test_the_recorded_contents_are_replaced_and_not_grown`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`

Old text:

```
        record["tracks"] = contents
        dirty = True
```

New text:

```
        record["tracks"] = [*_listed(record, "tracks"), *contents]
        dirty = True
```

### `r229.L7_a_reused_path_keeps_its_record`

A displaced record is never freed, so a crate renamed away from a reused path forks as it did before

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L7_a_reused_path_keeps_its_record`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_path_reused_for_a_different_crate_frees_its_record`
  - `tests/test_outbound_workers.py::test_a_path_reused_for_a_different_crate_is_said_at_the_gate`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if key in living:
```

### `u205.S1_account_lookup_ignores_app`

outbound account: ISRC lookups go to the account session whatever the opener built

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S1_account_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 179 against a baseline of 179
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

### `u27-reports-round-3-fixes.F6_folder_count_overwrite`

Count a playlist's raw length again, so folder rows stop reconciling with placements

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-3-fixes.json`, row `F6_folder_count_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_count_never_exceeds_what_the_collection_can_account_for`
  - `tests/modules/test_reports_engines.py::test_two_playlists_sharing_a_display_path_add_up_rather_than_overwrite`

Old text:

```
        counts.setdefault(playlist.path, 0)
        for track_id in playlist.track_ids:
            if track_id not in known:
                continue
            counts[playlist.path] += 1
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
        counts[playlist.path] = len(playlist.track_ids)
        for track_id in playlist.track_ids:
            held.setdefault(track_id, []).append(playlist.path)
```

### `u27-reports-round-2.L2_genre_parent`

Round 1 zero, re-run against the replacement guards: loosen the genre filter

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-2.json`, row `L2_genre_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_below_a_genre_is_not_itself_a_genre`
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
        if len(folder) < 2 or folder[-2] != tree_display:
```

New text:

```
        if len(folder) < 2 or tree_display not in folder:
```

### `r1761.P10_move_nothing_only_when_new`

_plan_files: delete nothing only for a new library, so a census of none mirrors a lost volume's mount point (round two's B3)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P10_move_nothing_only_when_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    move_nothing = held == 0 and not emptied
```

New text:

```
    move_nothing = new_library
```

### `r1761.P4_content_proof_skipped`

_plan_files: ignore the content proof's refusal, so an empty root is mirrored (the defect)

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P4_content_proof_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if unproven:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_UNPROVEN,
```

New text:

```
    if False:
        return PortionPlan(
            portion=backup_facts.Portion.FILES,
            refusal=Refusal.LIBRARY_ROOT_UNPROVEN,
```

### `r222-a.A5_held_run_takes_no_slot`

Spend the whole keep on settled folders, so the held run is kept on top of the keep rather than as one slot of it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A5_held_run_takes_no_slot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    slots = keep - 1 if held else keep
```

New text:

```
    slots = keep
```

### `r349-c.C1_prune_recorded`

The prune calls the bare runner, so its commands are not recorded beside its results

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r349-c.json`, row `C1_prune_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`, `tests/modules/test_tools.py`
- Collected: 278 against a baseline of 278
- Kills: 29 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_backup_payload_carries_a_version`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_a_supplied_configuration_is_used_rather_than_the_one_on_disk`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - ... and 14 more, see the JSON sidecar

Old text:

```
                    runner=recorded,
```

New text:

```
                    runner=runner,
```

### `r757-a.E7_first_totals_win`

comparison_report: keep the first totals logged and not the last

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E7_first_totals_win`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if isinstance(found, dict):
            stats = found
```

New text:

```
        if isinstance(found, dict) and not stats:
            stats = found
```

### `u311.A2_refused_portion_runs`

A portion with a refusal still reads as one that will run

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A2_refused_portion_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
        return self.refusal is None and (bool(self.commands) or self.kind in _NOTHING_TO_SEND)
```

New text:

```
        return bool(self.commands) or self.kind in _NOTHING_TO_SEND
```

### `u317.Q20_resend_keeps_times`

_quick_commands: the resend loses --ignore-times, so a rewrite with its size and time kept is never sent

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q20_resend_keeps_times`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    rclone, "copy", root, dest, *listed, "--ignore-times",
```

New text:

```
                    rclone, "copy", root, dest, *listed,
```

### `u323.I6_provider_dropped_at_the_gate`

_not_the_recorded_volume: the volume gate is asked with no provider, so the platform's own identity read answers

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I6_provider_dropped_at_the_gate`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        session.assert_volume_identity(
            cfg, identity_provider=identity_provider, mount_enumerator=mount_enumerator
        )
```

New text:

```
        session.assert_volume_identity(
            cfg, identity_provider=None, mount_enumerator=mount_enumerator
        )
```

### `u48-author.P4_warning_not_recorded_on_the_portion`

run_backup reads the classification and drops it instead of carrying it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P4_warning_not_recorded_on_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
```

New text:

```
                results += pruned
                continue
```

### `r1761.P17_census_damaged_is_none`

read_census: a census that cannot be parsed is no census, so it is not history

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `r1761.json`, row `P17_census_damaged_is_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        return Census(files=None)
```

New text:

```
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        return None
```

### `u311.A6_double_star_stays_in_a_segment`

The glob reader no longer reads a double star as one token, so it stops crossing separators

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u311.json`, row `A6_double_star_stays_in_a_segment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 318 against a baseline of 318
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_quick_walk_reads_hashes_globs_and_names_as_rclone_does`

Old text:

```
re.findall(r"\*\*|.", text, re.S)
```

New text:

```
re.findall(r".", text, re.S)
```

### `u317.Q2_unreadable_folder_is_absence`

walk: a folder that cannot be listed is skipped, so its files read as removed

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q2_unreadable_folder_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_duplication.py::test_no_package_holds_a_copied_block_beyond_its_allowance`

Old text:

```
            raise WalkRefused(f"{directory} could not be listed: {exc}") from exc
```

New text:

```
            continue
```

### `r154-a.A5_listing_filter`

List every folder under the snapshot root as a snapshot, so a stray folder sorting last is the newest

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A5_listing_filter`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_newest_snapshot_ignores_folders_that_are_not_stamps`

Old text:

```
            if is_snapshot_name(name)
```

New text:

```
            if name
```

### `r154-b.B8_walk_match`

Stop the walk at the first folder carrying ANY marker, so the default pulls another library's snapshot under a shared root

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B8_walk_match`
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
        if seen[name] == (expected,):
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
```

New text:

```
        if seen[name]:
            return ResolvedSnapshot(stamp=name, recorded_volume=expected, named=False)
```

### `r338-b.R5_pulled_under_the_watch`

_plan_restore_inside_the_gates: stop withholding a landing place the analysis watch covers, the defect the built in review found: a live restore ends refused after the database is replaced

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R5_pulled_under_the_watch`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_that_would_land_under_the_analysis_watch_is_withheld_and_not_asked_about`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if not pull_share:
```

### `r367.E3_a_live_rekordbox_is_ignored`

existing guard sample: a restore proceeds while rekordbox holds the database

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `E3_a_live_rekordbox_is_ignored`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_refuses_while_rekordbox_holds_the_database`

Old text:

```
    if running:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
```

New text:

```
    if running and False:
        raise BackupRefused(
            Refusal.REKORDBOX_RUNNING,
```

### `r388-a.M1_named_identity_listing_back_to_absence`

A named snapshot whose identity marker listing exits 1 raises no-snapshot-available again, the defect the unit fixes

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-a.json`, row `M1_named_identity_listing_back_to_absence`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
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

### `r388-b.M7_share_listing_back_to_absence`

An analysis share listing that exits 1 raises no-snapshot-available again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M7_share_listing_back_to_absence`
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
            Refusal.SNAPSHOT_LISTING_FAILED,
            f"the analysis share mirror
```

New text:

```
            Refusal.NO_SNAPSHOT_AVAILABLE,
            f"the analysis share mirror
```

### `u311.C5_binaries_out_of_order`

The shared binary lookup answers its names in reverse, swapping ffmpeg and ffprobe

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C5_binaries_out_of_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 30 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_mastering_leaves_no_intermediate_behind`
  - `tests/modules/test_tools.py::test_mastering_leaves_the_source_byte_identical_and_archived`
  - `tests/modules/test_tools.py::test_mastering_reports_before_and_after_loudness`
  - `tests/modules/test_tools.py::test_the_mastering_payload_carries_a_version`
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_joined_wav_is_written_as_rf64_when_it_needs_to_be`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - ... and 15 more, see the JSON sidecar

Old text:

```
        return [binaries.resolve(name) for name in names]
```

New text:

```
        return [binaries.resolve(name) for name in reversed(names)]
```

### `r187-b.B4_empty_read_cached`

build_index: cache a read that returned no field at all, so one failed read drops the track until the file is touched

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B4_empty_read_cached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer`

Old text:

```
            if identity is not None and any(value is not None for value in raw.values()):
```

New text:

```
            if identity is not None:
```

### `u311.C9_anchor_comes_back`

The anchor is no longer excluded from its own pool by match key

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C9_anchor_comes_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 340 against a baseline of 340
- Kills: 13 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        if anchor_match and track.match == anchor_match:
```

New text:

```
        if False:
```

### `u281.R3_stopped_reads_miss`

Refusals.stopped: answer a stopped catalogue MISS, the card's merge blocker, a refused file recorded as one no catalogue carries

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R3_stopped_reads_miss`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 8 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_never_reads_as_a_miss_or_a_clean_no_hit`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`

Old text:

```
        return SourceOutcome(
            source,
            Answer.BLOCKED,
            note=(
                f"{NOT_SENT}{source} refused
```

New text:

```
        return SourceOutcome(
            source,
            Answer.MISS,
            note=(
                f"{NOT_SENT}{source} refused
```

### `u282.W1_walk_beatport_first`

WALK: Beatport first again, the order before the card

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u282.json`, row `W1_walk_beatport_first`
- Moved: Anchored where u306-replay-after-d.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_discogs_first.py`, `tests/test_discogs_searcher.py`, `tests/test_catalogue_searcher.py`, `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`, `tests/test_tagging_engine.py`, `tests/test_title_matcher.py`, `tests/test_tag_suggest.py`
- Collected: 1470 against a baseline of 1470
- Kills: 43 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken`
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_discogs_first.py::test_a_401_is_sent_once_and_beatport_decides_every_file`
  - `tests/test_discogs_first.py::test_a_beatport_decline_beside_a_refused_token_is_a_decline_and_never_raises`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_a_beatport_miss_keeps_discogs_word_and_is_not_no_hit`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[outage]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[refused]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_beside_an_unread_beatport_is_a_decline_never_an_outage[reshaped]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[both]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[fallback-only]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[styleless]`
  - `tests/test_discogs_first.py::test_a_discogs_decline_goes_on_to_beatport_which_decides[unmapped]`
  - `tests/test_discogs_first.py::test_a_discogs_match_carries_a_picture_ask_and_spends_nothing_until_asked`
  - `tests/test_discogs_first.py::test_a_discogs_match_decides_and_beatport_is_not_asked`
  - `tests/test_discogs_first.py::test_a_discogs_miss_asks_beatport_and_beatport_decides`
  - ... and 28 more, see the JSON sidecar

Old text:

```
WALK: tuple[str, ...] = (DISCOGS, BEATPORT)
```

New text:

```
WALK: tuple[str, ...] = (BEATPORT, DISCOGS)
```

### `u260.F3_admission_ignored`

remembering: drop the admission, so bytes that are not a picture are remembered and never asked for again

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F3_admission_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 2 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_an_answer_the_admission_refuses_is_handed_on_and_not_remembered`
  - `tests/test_album_cover_once.py::test_bytes_that_are_not_a_picture_are_asked_again_and_fail_as_they_did`

Old text:

```
        if not data or (admit is not None and not admit(data)):
```

New text:

```
        if not data:
```

### `u281.S3_challenge_header_case`

_refusal_note: compare the header's value as sent, so ' Challenge ' is not named one

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S3_challenge_header_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`
- Collected: 204 against a baseline of 204
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_the_challenge_header_is_read_whatever_case_its_name_and_value_arrive_in`

Old text:

```
    if mitigated.strip().lower() == _CF_CHALLENGE:
```

New text:

```
    if mitigated == _CF_CHALLENGE:
```

### `u281.S8_refusal_check_before_the_payload`

_search_beatport: run the refusal check before the parse again, round one's order, so a results page carrying Cloudflare's script reads as a refusal

- File: `src/cratekit/tagging/shops.py`
- Source: `u281.json`, row `S8_refusal_check_before_the_payload`
- Moved: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_results_page_carrying_cloudflares_script_is_read_as_results`

Old text:

```
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
```

New text:

```
    refused = unread_outcome(BEATPORT, page)
    if refused is not None:
        return refused
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
```

### `u133-b.T4_rates`

Jazz gets a star rating derived from energy

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T4_rates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 945 against a baseline of 945
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_jazz_is_shaped_as_hip_hop_is`

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

```

### `u90-c5.C5_record_threshold_unconverted`

The one reader returns the stored threshold as written rather than the checked float

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c5.json`, row `C5_record_threshold_unconverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 203 against a baseline of 203
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

### `r1991.T4_no_record`

writer: record nothing after the commit, so adoption leaves no node and a renamed folder is read as no genre's (the residual's first half)

- File: `src/cratekit/write/trees.py`
- Source: `r1991.json`, row `T4_no_record`
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
    if record_as:
        _record_filed_nodes(cfg, db, tree_id, root_id, record_as, run.filed)

```

New text:

```
(empty)
```

### `r758-b.T7_refusal_read_as_an_interruption`

a refusal in the removals is raised as an interrupted move and loses its own cause and remedy

- File: `src/cratekit/write/trees.py`
- Source: `r758-b.json`, row `T7_refusal_read_as_an_interruption`
- Moved: the removals are now the step _remove_leavers, one level less indented, the same clause
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`

Old text:

```
            if isinstance(exc, cause.CratekitError):
                raise

```

New text:

```
(empty)
```

