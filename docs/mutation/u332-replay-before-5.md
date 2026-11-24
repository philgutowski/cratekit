# Mutation table: u332-replay-before-5

Measured by `scripts/mutate.py` on 2026-11-24 06:14 UTC, branch `HEAD` at `324cafa5`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 122.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 04:14 UTC for commit `324cafa562b9`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 119, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 185 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u297.B3_somebodys_directory_emptied` | `scripts/behaviour_compare.py` | user | 1 file(s) | 137 | 3 | killed |
| `u122.H2_review_not_held` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 6 | killed |
| `u122.N3_next_no_status` | `scripts/board.py` | maintainer | 2 file(s) | 126 | 2 | killed |
| `u148.N1_truncation_blamed_on_token` | `scripts/board.py` | maintainer | 4 file(s) | 186 | 1 | killed |
| `u151.C2_page_bound_short` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u151.U2_added_card_zero` | `scripts/board.py` | maintainer | 3 file(s) | 50 | 1 | killed |
| `u187.A3_answer_not_read_as_reply` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 3 | killed |
| `u203.M5_no_trailing_strip` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 27 | killed |
| `u291.L4_help_names_a_literal` | `scripts/board.py` | maintainer | 1 file(s) | 91 | 1 | killed |
| `u197.M3_registry_load_fold` | `src/cratekit/acquire/__init__.py` | user | 2 file(s) | 574 | 1 | killed |
| `r83.D5_drop_name_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 753 | 4 | killed |
| `u176.C12_transport_hides_text` | `src/cratekit/acquire/bandcamp.py` | user | 1 file(s) | 47 | 1 | killed |
| `u176.C9_stat_not_ready` | `src/cratekit/acquire/bandcamp.py` | user | 1 file(s) | 47 | 1 | killed |
| `u176.V4_record_planned_fetched` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u177.B2_plan_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 12 | killed |
| `u305.M6_registry_import_dropped` | `src/cratekit/acquire/bandcamp_cli.py` | user | 3 file(s) | 114 | 55 | killed |
| `u205.C5_server_error_read_as_absence` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `r289-b.B5_job_directory_before_its_items` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 366 | 2 | killed |
| `r668-a.M3_no_empty_job_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u169.A1_retryable_policy_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u42-author.C4_marked_lossless_dropped` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u54-acquisition-worker.G11_not_acquired` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 8 | killed |
| `u54-acquisition-worker.G27_remedy_absent_stays_absent` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u80-b.F9_coverage_weight` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F2_order_reversed` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 2 | killed |
| `u81-fetch-b.Y1_no_option_terminator` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u80.C8_outage_narrowed` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u81-fetch-a.W8_upload_tags_kept` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r1016.M1_account_walk_back_on_the_clients_method` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 14 | killed |
| `r1016.S1_account_dedup_dropped` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 794 | 1 | killed |
| `r878-a.A3_budget_off_by_one` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-b.B6_order_by_name` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `u65.B1_favourites_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 9 | killed |
| `u65.C4_the_short_page_rule_stops_every_walk` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 199 | 13 | killed |
| `u65.F1_an_unpageable_listing_takes_its_single_page` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 86 | 2 | killed |
| `r679-b.B6_one_shape_only` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 834 | 7 | killed |
| `u205.O2_no_country_still_opens` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 353 | 1 | killed |
| `r703-a.LF2_cause_not_worded` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 4 | killed |
| `r703-b.O1_proxy_notes_nothing` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 275 | 5 | killed |
| `r83.D8_vendored_defect_first` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 157 | 2 | killed |
| `u47-author.CODEC_suffix_instead_of_container` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R197_argument_set_shrinks` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 201 | 3 | killed |
| `u47-author.SAMPLE_permanence_asked_second` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u254.M05_cache_identity_no_inode` | `src/cratekit/adopt/apply.py` | maintainer | 6 file(s) | 743 | 1 | killed |
| `u254.M14_header_unterminated` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 743 | 1 | killed |
| `r1991.A1_vocal_unrecorded` | `src/cratekit/adopt/apply_cli.py` | user | 15 file(s) | 521 | 1 | killed |
| `r788-d.A2_vocal_rows_never_written` | `src/cratekit/adopt/apply_cli.py` | user | 4 file(s) | 163 | 3 | killed |
| `u27-adopt-apply-author.A3_missing_gate_refuses_under_the_wrong_reason` | `src/cratekit/adopt/apply_cli.py` | maintainer | 1 file(s) | 17 | 1 | killed |
| `u55-collection-reader.R24_worker_digest_check` | `src/cratekit/adopt/apply_cli.py` | user | 2 file(s) | 46 | 3 | killed |
| `u23-round-8-independent.X3_approval_actor_unchecked` | `src/cratekit/adopt/approval.py` | user | 1 file(s) | 615 | 1 | killed |
| `r780-a.A11_tree_reading_from_entry_sub` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 1 | killed |
| `r780-a.A9_refused_buckets_empty` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 87 | 2 | killed |
| `u118-c.M6_verdict_reason` | `src/cratekit/adopt/move.py` | user | 1 file(s) | 58 | 1 | killed |
| `r758-b.C6_left_target_is_added_back` | `src/cratekit/adopt/move_cli.py` | user | 1 file(s) | 87 | 1 | killed |
| `r731-b.M17_bridge_tree_raises_at_the_plan` | `src/cratekit/adopt/placements.py` | user | 2 file(s) | 70 | 6 | killed |
| `r797-b.M1_found_in_the_holding_folder` | `src/cratekit/adopt/placements.py` | user | 3 file(s) | 172 | 5 | killed |
| `r722.P2_build_drops_level` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 653 | 3 | killed |
| `r731-a.M04_renamed_sub_not_withheld` | `src/cratekit/adopt/plan.py` | user | 2 file(s) | 70 | 2 | killed |
| `r788-a.P1_untagged_is_added` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 11 | killed |
| `r788-b.P16_digest_moves_under_its_own_apply` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 163 | 3 | killed |
| `u956.O15_document_blind_to_outside` | `src/cratekit/adopt/plan.py` | user | 4 file(s) | 687 | 2 | killed |
| `u23-round-8-independent.A6_at_risk_original_by_identity` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.E2_vacancy_parent_check_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.S1_size_of_always_none` | `src/cratekit/adopt/revert_changed.py` | maintainer | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 619 | 5 | killed |
| `u956.O12_unaskable_parent_answers` | `src/cratekit/adopt/scan.py` | user | 2 file(s) | 641 | 2 | killed |
| `u956.S19_unadoptable_routes` | `src/cratekit/adopt/scan.py` | user | 4 file(s) | 687 | 14 | killed |
| `u241.M16_changed_settings_keep_old_heads` | `src/cratekit/analysis/ahead.py` | user | 1 file(s) | 272 | 3 | killed |
| `u223.M24_report_link_followed` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 177 | 1 | killed |
| `u223.M9_report_unparsed` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 177 | 1 | killed |
| `u90-a.A6_dispatch_truthiness` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 1 | killed |
| `u90-b.B8_hand_reads_old_after_write` | `src/cratekit/analysis/calibrate.py` | user | 1 file(s) | 177 | 4 | killed |
| `u94-a.S6_music_folder_not_wide` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-b.W7_omissions_dropped_from_the_fit` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 1 | killed |
| `u94-c.N8_absent_folder_not_told_apart` | `src/cratekit/analysis/calibrate.py` | user | 2 file(s) | 213 | 2 | killed |
| `u223.M14_any_status` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 1 | killed |
| `u306.A1_zero_told_apart` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 213 | 1 | killed |
| `u343.M05_untitled_title_with_a_head` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 324 | 4 | killed |
| `u58-workers-and-wav.R9_missing_file_analysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 177 | 2 | killed |
| `u263.D14_whole_frames` | `src/cratekit/analysis/decode.py` | maintainer | 2 file(s) | 57 | 1 | killed |
| `u263.D9_file_protocol` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 1 | killed |
| `u264.M3_trailing_zero_dropped` | `src/cratekit/analysis/decode.py` | user | 2 file(s) | 57 | 2 | killed |
| `u157.D10_verdict_cut` | `src/cratekit/analysis/detect.py` | user | 3 file(s) | 23216 | 0 (promoted) | zero |
| `u241.M27_no_warm_up_before_the_first_head` | `src/cratekit/analysis/detect.py` | user | 1 file(s) | 15 | 1 | killed |
| `u344.M5_measure_not_warmed` | `src/cratekit/analysis/energy.py` | maintainer | 5 file(s) | 497 | 1 | killed |
| `u327.A17_policy_before_files` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u327.A8_no_reference_left` | `src/cratekit/analysis/head_adopt.py` | user | 1 file(s) | 114 | 1 | killed |
| `u342.P3_headless_is_stamped` | `src/cratekit/analysis/head_adopt.py` | user | 4 file(s) | 392 | 12 | killed |
| `u342.C1_unanswered_names_the_half` | `src/cratekit/analysis/head_adopt_cli.py` | user | 4 file(s) | 392 | 1 | killed |
| `u275.M3_slope_rounded_down` | `src/cratekit/analysis/light.py` | user | 5 file(s) | 555 | 6 | killed |
| `u343.M10_mark_reads_the_wrong_field` | `src/cratekit/analysis/run.py` | user | 3 file(s) | 231 | 6 | killed |
| `sitting3.G2_missing_target_read_as_fixture` | `src/cratekit/analysis/vocal.py` | user | 1 file(s) | 18 | 2 | killed |
| `u263.D18_vocal_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 234 | 1 | killed |
| `u92-author.G1_guard_deleted` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 4 | killed |
| `u92-author.G9_warning_counts_the_wrong_reason` | `src/cratekit/analysis/vocals.py` | user | 3 file(s) | 231 | 5 | killed |
| `r221-a.W6_twin_branch_says_it_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B14_destination_claimed_unread` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r222-b.B8_every_exception_is_unreadable` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 1 | killed |
| `r349-b.B4_stage_error_completes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r757-c2.S7_verb_says_nothing_of_the_comparison` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 23216 | 0 (promoted) | zero |
| `u45-round-1.C6_partial_run_refused` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 3 | killed |
| `u45-round-1.W2_report_from_the_plan` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 10 | killed |
| `u50-author.B1_no_items_enqueued` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 89 | 30 | killed |
| `r290-author.D1_dispatcher_ignores_the_type` | `src/cratekit/cli/__init__.py` | user | 57 file(s) | 7231 | 47 | killed |
| `r388-b.M12_listing_steps_say_take_a_backup` | `src/cratekit/cli/exit_codes.py` | user | 4 file(s) | 660 | 2 | killed |
| `r925.J4_isrc_dropped` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 67 | 2 | killed |
| `r678-a.A4_empty_job_id_renders_a_job` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 4 | killed |
| `r685-a.L4_an_unreadable_copy_falls_back` | `src/cratekit/core/active_taxonomy.py` | user | 1 file(s) | 18 | 1 | killed |
| `u260.E11_reset_forgets_nothing` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 13 | killed |
| `u260.E8_encode_hit_not_refreshed` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 1 | killed |
| `u83-a.E5_over_cap_refusal` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `u83-b.W10_id3_add_tags` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 9 | killed |
| `u83-b.W6_flac_block_width` | `src/cratekit/core/art.py` | user | 1 file(s) | 73 | 2 | killed |
| `r757-b2.F3_full_record_does_not_move_the_date` | `src/cratekit/core/backup_facts.py` | user | 4 file(s) | 728 | 4 | killed |
| `example-binaries-five-row.B5_credential_strip` | `src/cratekit/core/binaries.py` | user | 1 file(s) | 18 | 1 | killed |
| `u45-round-1.V1_transfer_failure_is_a_defect` | `src/cratekit/core/cause.py` | user | 33 file(s) | 5516 | 1 | killed |
| `u241.M09_ceiling_ignores_the_reserve` | `src/cratekit/core/cores.py` | user | 2 file(s) | 314 | 14 | killed |
| `r390-a.A1_retry_re_arms_unconditionally` | `src/cratekit/core/jobs.py` | user | 3 file(s) | 210 | 5 | killed |
| `u169.E3_decline_writes_failed` | `src/cratekit/core/jobs_drive.py` | user | 2 file(s) | 153 | 10 | killed |
| `u39-naming-independent.E2_wheel_letter_widened` | `src/cratekit/core/naming.py` | user | 9 file(s) | 1486 | 1 | killed |
| `u205.G8_since_keeps_earlier_app_calls` | `src/cratekit/core/provider_gate.py` | user | 2 file(s) | 23216 | 6 (promoted) | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 707 | 122 | killed |
| `u118-b.R1_split_competes` | `src/cratekit/core/routing.py` | user | 2 file(s) | 102 | 20 | killed |
| `r722.T3_open_failure_is_absent` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2994 | 3 | killed |
| `u247.M6_key_is_the_size` | `src/cratekit/core/taxonomy.py` | user | 4 file(s) | 293 | 9 | killed |
| `r301.S1_month_ignores_ledger` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 5 | killed |
| `r706-b.B1_partition_front_loads_the_remainder` | `src/cratekit/intake/acrcloud.py` | user | 5 file(s) | 227 | 1 | killed |
| `r924.A3_cached_count_zero` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 78 | 1 | killed |
| `u103-a.A3_document_must_carry_its_plan` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 183 | 1 | killed |
| `u57-recognition-and-items.M18_missing_credential_is_unready` | `src/cratekit/intake/acrcloud.py` | user | 2 file(s) | 175 | 1 | killed |
| `u259.M1_judge_no_row` | `src/cratekit/intake/analyzed.py` | user | 2 file(s) | 85 | 6 | killed |
| `r682-a.M3_empty_why_counted` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 67 | 1 | killed |
| `u103-b.C8_set_no_op_carries_warnings` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 596 | 2 | killed |
| `u213.M8_readable_unread_excludes_read` | `src/cratekit/intake/cli.py` | user | 2 file(s) | 113 | 1 | killed |
| `u70.S5_source_id_recorded` | `src/cratekit/intake/cli.py` | maintainer | 2 file(s) | 241 | 1 | killed |
| `u103-b.C14_offered_under_its_own_key` | `src/cratekit/intake/cli_identify.py` | user | 9 file(s) | 596 | 1 | killed |
| `u104-d.C5_no_digest_token_is_the_address` | `src/cratekit/intake/cli_identify.py` | user | 2 file(s) | 108 | 1 | killed |
| `r924.F1_no_start_line` | `src/cratekit/intake/fetch.py` | user | 2 file(s) | 52 | 3 | killed |
| `u104-a.F4_landing_inside_scratch` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u104-c.P3_several_threshold` | `src/cratekit/intake/fetch.py` | user | 1 file(s) | 41 | 1 | killed |
| `u103-b.P2_digest_reaches_the_verb` | `src/cratekit/intake/pipeline.py` | user | 1 file(s) | 67 | 1 | killed |
| `u37-author-light.G5_path_repair_queue` | `src/cratekit/intake/repair.py` | user | 2 file(s) | 155 | 3 | killed |
| `u102-a.P6_missing_says_what_exists` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u102-b.G4_plan_collisions` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 2 | killed |
| `u102-b.S1_stub_removed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `u237.M4_case_sensitive_mark` | `src/cratekit/label/harvest.py` | user | 2 file(s) | 354 | 12 | killed |
| `r704-a.S1_no_cause_chain_check` | `src/cratekit/label/sweep.py` | user | 5 file(s) | 524 | 6 | killed |
| `u205.S3_catalogue_lookup_ignores_app` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 248 | 15 | killed |
| `u192.F3_keep_remedy_token` | `src/cratekit/modules/foreground.py` | user | 2 file(s) | 279 | 1 | killed |
| `r356-b.B7_heart_back_hands_on_no_title` | `src/cratekit/modules/outbound/hearts.py` | user | 1 file(s) | 64 | 1 | killed |
| `r229.L16_a_moved_record_is_not_followed` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 3 | killed |
| `r229.L6_a_living_crate_is_a_candidate` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 3 | killed |
| `u309-z.U13_shell_config_origin` | `src/cratekit/modules/outbound/shell.py` | user | 5 file(s) | 1320 | 1 | killed |
| `u27-reports-round-2.C3b_tie_break` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L7_shape_governed_filter` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 2 | killed |
| `r154-b.B9_marker_failure_fails_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 1 | killed |
| `r1761.P3_identity_raise_refuses` | `src/cratekit/modules/tools/backup.py` | user | 5 file(s) | 23216 | 0 (promoted) | zero |
| `r222-a.A4_keep_zero_holds` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 278 | 1 | killed |
| `r338-c.C3_rehearsed_restore_pulls_the_share` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 723 | 1 | killed |
| `r757-a.E6_unread_total_is_zero` | `src/cratekit/modules/tools/backup.py` | user | 4 file(s) | 23216 | 0 (promoted) | zero |
| `u311.A1_warning_key_order` | `src/cratekit/modules/tools/backup.py` | user | 11 file(s) | 898 | 1 | killed |
| `u317.Q19_self_written_empty` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u323.I5_provider_dropped_by_the_plan` | `src/cratekit/modules/tools/backup.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |
| `u48-author.P2_purge_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 691 | 1 | killed |
| `r1761.P9_emptied_passes_on_the_fact_file` | `src/cratekit/modules/tools/backup_proof.py` | user | 2 file(s) | 246 | 2 | killed |
| `u311.A5_agrees_ignores_the_hash` | `src/cratekit/modules/tools/backup_record.py` | user | 4 file(s) | 318 | 1 | killed |
| `u317.Q1_unlisted_folder_is_absence` | `src/cratekit/modules/tools/backup_record.py` | user | 1 file(s) | 23216 | 0 (promoted) | zero |
| `r154-a.A3_named_shape_check` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 9 | killed |
| `r154-b.B7_walk_order` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 5 | killed |
| `r338-b.R4_empty_listing_read_as_held` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `r367.E2_an_unconfirmed_restore_is_allowed` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 283 | 1 | killed |
| `r367.G8_files_only_is_dropped` | `src/cratekit/modules/tools/backup_snapshot.py` | maintainer | 1 file(s) | 189 | 1 | killed |
| `r388-b.M11_db_folder_absent_read_as_failure` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 723 | 1 | killed |
| `u311.C4_24_bit_loses_its_depth` | `src/cratekit/modules/tools/mastering.py` | user | 3 file(s) | 248 | 1 | killed |
| `r187-b.B3_entry_not_a_mapping` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 269 | 2 | killed |
| `u311.C8_unreadable_number_raises` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 340 | 44 | killed |
| `u281.R2_limit_two` | `src/cratekit/tagging/catalogues.py` | user | 2 file(s) | 138 | 12 | killed |
| `u281.S7_body_note_reworded` | `src/cratekit/tagging/catalogues.py` | user | 3 file(s) | 205 | 1 | killed |
| `u260.F2_empty_answer_remembered` | `src/cratekit/tagging/searchers.py` | user | 4 file(s) | 263 | 1 | killed |
| `u281.S2_challenge_header_unread` | `src/cratekit/tagging/searchers.py` | user | 5 file(s) | 447 | 3 | killed |
| `u281.S1_beatport_reads_no_refusal` | `src/cratekit/tagging/shops.py` | user | 5 file(s) | 447 | 22 | killed |
| `u133-b.T2_alias_gone` | `src/cratekit/templates/taxonomy.default.toml` | user | 4 file(s) | 1222 | 2 | killed |
| `u90-c.C6_wrapper_reads_nothing` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 203 | 8 | killed |
| `r685-a.V1_route_inbox_export_reads_the_shipped_text` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 215 | 4 | killed |
| `r758-a.T6_removed_playlist_is_a_destination` | `src/cratekit/write/trees.py` | user | 1 file(s) | 87 | 2 | killed |
| `u125.D1_derive_test_tautology` | `tests/test_reserved_causes.py` | maintainer | 1 file(s) | 23216 | 0 (promoted) | zero |

## Zero rows and what they owe

- `u157.D10_verdict_cut` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r349-b.B4_stage_error_completes` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-c2.S7_verb_says_nothing_of_the_comparison` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r1761.P3_identity_raise_refuses` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-a.E6_unread_total_is_zero` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u317.Q19_self_written_empty` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u323.I5_provider_dropped_by_the_plan` (maintainer facing): maintainer facing, composite not required
- `u317.Q1_unlisted_folder_is_absence` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u125.D1_derive_test_tautology` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u297.B3_somebodys_directory_emptied`

take_root: take a root, or the source directory beside it, that holds files no capture left

- File: `scripts/behaviour_compare.py`
- Source: `u297.json`, row `B3_somebodys_directory_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_behaviour_compare.py`
- Collected: 137 against a baseline of 137
- Kills: 3 (killed)
- Killed:
  - `tests/test_behaviour_compare.py::test_a_file_that_is_only_named_like_a_holder_vouches_for_nothing`
  - `tests/test_behaviour_compare.py::test_a_root_that_holds_somebodys_files_is_refused_and_left_alone`
  - `tests/test_behaviour_compare.py::test_the_directory_beside_the_root_is_not_emptied_either`

Old text:

```
        if not left_by_a_capture(folder, holder):
```

New text:

```
        if False:
```

### `u122.H2_review_not_held`

UNDERWAY loses In review, the runner's status, so it reads as drift again

- File: `scripts/board.py`
- Source: `u122.json`, row `H2_review_not_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_status.py`, `tests/test_pending_units.py`
- Collected: 126 against a baseline of 126
- Kills: 6 (killed)
- Killed:
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[1-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[2-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[4-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[5-In review]`
  - `tests/test_board_status.py::test_an_open_card_somebody_holds_keeps_the_status_it_holds[7-In review]`
  - `tests/test_board_status.py::test_next_lists_a_held_card_as_busy_and_never_offers_it[In review]`

Old text:

```
UNDERWAY = ("In Progress", "In review")
```

New text:

```
UNDERWAY = ("In Progress",)
```

### `u122.N3_next_no_status`

next drops the status column, so a reader cannot tell the runner's hold from a session's

- File: `scripts/board.py`
- Source: `u122.json`, row `N3_next_no_status`
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
            print(f"  #{node['number']:<3} {status:<11} {node['title']}")
```

New text:

```
            print(f"  #{node['number']:<3} {node['title']}")
```

### `u148.N1_truncation_blamed_on_token`

next catches a truncation as a token that cannot read the board

- File: `scripts/board.py`
- Source: `u148.json`, row `N1_truncation_blamed_on_token`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_reads.py`, `tests/test_board_status.py`, `tests/test_pending_units.py`, `tests/test_restart_and_residual_files.py`
- Collected: 186 against a baseline of 186
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_next_refuses_a_truncated_item_read_and_names_a_blind_token`

Old text:

```
    except Truncated:
        # A cut short read is not a token that cannot see the board, and the
        # queue below would offer a held card the read missed.
        raise

```

New text:

```
(empty)
```

### `u151.C2_page_bound_short`

the page bound drops its last page, a read of 317 issues refused

- File: `scripts/board.py`
- Source: `u151.json`, row `C2_page_bound_short`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_reads.py::test_one_row_under_the_limit_is_taken_as_whole`

Old text:

```
    for _ in range(READ_LIMIT // 100 + 1):
```

New text:

```
    for _ in range(READ_LIMIT // 100):
```

### `u151.U2_added_card_zero`

a card sync just added reads as holding 0, so a derived 0 is never written

- File: `scripts/board.py`
- Source: `u151.json`, row `U2_added_card_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cost.py`, `tests/test_board_reads.py`, `tests/test_board_status.py`
- Collected: 50 against a baseline of 50
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cost.py::test_an_issue_off_the_board_is_added_then_given_its_status_and_number`

Old text:

```
"status": None, "unblocks": None}
```

New text:

```
"status": None, "unblocks": 0}
```

### `u187.A3_answer_not_read_as_reply`

cloud_state: drop the relayed answer from the replies after a question, so the card is never offered as answered

- File: `scripts/board.py`
- Source: `u187.json`, row `A3_answer_not_read_as_reply`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 3 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Question for Phillip@3; ## Answer from Phillip@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`

Old text:

```
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or "") or _relayed_answer(c))
```

New text:

```
        if _when(c) > since and (SESSION_MARK not in (c.get("body") or ""))
```

### `u203.M5_no_trailing_strip`

comment_heading: strip emphasis but no trailing punctuation, so ## Brainstorm. reads as a hold

- File: `scripts/board.py`
- Source: `u203.json`, row `M5_no_trailing_strip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 27 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm?@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-## Brainstorm?@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Brainstorm.**@s+6; **Answer from Phillip.**@s+5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Question for Phillip.**@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-**Question for Phillip.**@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-Brainstorm!@1; !B@0.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[answered-Brainstorm!@s+6; !B@s+5.5]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[landed-open-## Started@s+4; **Landed.**@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-## Started@s+4; Withdrawn.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[ready-**Answer from Phillip.**@s+6]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[set-aside-## Started@s+4; **Needs the machine.** It reads the live library.@s+2]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[waiting-on-phillip-## Brainstorm?@1]`
  - `tests/test_board_cloud.py::test_a_cards_comments_give_its_state[waiting-on-phillip-## Brainstorm?@s+6]`
  - ... and 12 more, see the JSON sidecar

Old text:

```
            text = text.strip().strip("*_").rstrip(_TRAILING)
```

New text:

```
            text = text.strip().strip("*_")
```

### `u291.L4_help_names_a_literal`

--lanes help: name a literal five rather than read the constant

- File: `scripts/board.py`
- Source: `u291.json`, row `L4_help_names_a_literal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_board_cloud.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_board_cloud.py::test_the_cloud_runs_ten_lanes_and_its_help_says_so`

Old text:

```
        help=f"how many cards the cloud builds at once (default {CLOUD_LANES})",
```

New text:

```
        help="how many cards the cloud builds at once (default 5)",
```

### `u197.M3_registry_load_fold`

registry load: look the name up as given, so a caller holding the retired key is refused

- File: `src/cratekit/acquire/__init__.py`
- Source: `u197.json`, row `M3_registry_load_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_doctor.py`
- Collected: 574 against a baseline of 574
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_retired_vendored_key_resolves_to_the_same_adapter`

Old text:

```
        target = ADAPTERS[current_adapter_name(name)]
```

New text:

```
        target = ADAPTERS[name]
```

### `r83.D5_drop_name_error`

R-348: NameError, and with it UnboundLocalError, leaves the defect classes

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D5_drop_name_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 753 against a baseline of 753
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[streamrip-UnboundLocalError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-NameError]`
  - `tests/test_adapter_contract.py::test_a_defect_raised_during_a_lookup_breaks_the_adapter_and_asks_for_a_report[vendored-UnboundLocalError]`

Old text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError, NameError)
```

New text:

```
DEFECT_ERRORS: tuple[type[BaseException], ...] = (AttributeError, TypeError)
```

### `u176.C12_transport_hides_text`

CurlTransport.get: the failure carries the exception's text, which names the signed link

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C12_transport_hides_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_the_real_transport_replaces_an_exception_whose_text_names_the_link`

Old text:

```
            answer = self._session.get(url, headers=self._headers(cookie), timeout=TIMEOUT_S)
            return Response(answer.status_code, answer.text, dict(answer.headers))
        except Exception as exc:  # noqa: BLE001 - replaced so its text cannot leak a link
            failure = type(exc).__name__
```

New text:

```
            answer = self._session.get(url, headers=self._headers(cookie), timeout=TIMEOUT_S)
            return Response(answer.status_code, answer.text, dict(answer.headers))
        except Exception as exc:  # noqa: BLE001 - replaced so its text cannot leak a link
            failure = str(exc)
```

### `u176.C9_stat_not_ready`

_prepared: a stat answer that is not ok is downloaded anyway

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C9_stat_not_ready`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`
- Collected: 47 against a baseline of 47
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_stat_answer_that_is_not_ready_is_unavailable`

Old text:

```
    if answer.get("result") != "ok":
```

New text:

```
    if False:
```

### `u176.V4_record_planned_fetched`

plan: a purchase the record holds is planned again, so a second run fetches it again

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V4_record_planned_fetched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`
- Collected: 46 against a baseline of 46
- Kills: 2 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_purchase_the_record_holds_is_done_on_a_resume_and_fetched_nothing_twice`
  - `tests/test_bandcamp_cli.py::test_a_second_run_plans_nothing`

Old text:

```
        if purchase.item_id in record:
```

New text:

```
        if False:
```

### `u177.B2_plan_label`

plan: never ask the registry, so no row names a label and nothing is tagged

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u177.json`, row `B2_plan_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_labels.py`, `tests/test_bandcamp_cli.py`
- Collected: 67 against a baseline of 67
- Kills: 12 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_seller_is_named_with_the_command_that_registers_it`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`
  - `tests/test_bandcamp_labels.py::test_the_plan_names_each_rows_label_and_none_for_a_seller_no_label_names`

Old text:

```
        label = known.by_bandcamp(purchase.seller) if purchase.seller else None

```

New text:

```
        label = None

```

### `u305.M6_registry_import_dropped`

registry: drop the local import of the label registry, so reading it raises NameError now that bandcamp_cli imports it only for type checking

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u305.json`, row `M6_registry_import_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`, `tests/test_bandcamp_labels.py`, `tests/test_bandcamp.py`
- Collected: 114 against a baseline of 114
- Kills: 55 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_compilation_listing_artist_and_title_together_is_read_as_both`
  - `tests/test_bandcamp_cli.py::test_a_compilation_with_one_owned_track_stages_the_rest_and_names_the_one`
  - `tests/test_bandcamp_cli.py::test_a_file_the_track_list_did_not_name_is_held_by_its_own_tags`
  - `tests/test_bandcamp_cli.py::test_a_hidden_purchase_is_planned_hidden`
  - `tests/test_bandcamp_cli.py::test_a_library_unmounted_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_listing_bandcamp_cannot_answer_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_listing_the_session_is_refused_at_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_lossy_file_under_a_lossless_offer_is_marked_by_what_it_is`
  - `tests/test_bandcamp_cli.py::test_a_name_already_in_the_batch_refuses_that_file_alone`
  - `tests/test_bandcamp_cli.py::test_a_permissive_policy_takes_the_lossy_release_marked`
  - `tests/test_bandcamp_cli.py::test_a_preorder_is_not_downloadable`
  - `tests/test_bandcamp_cli.py::test_a_purchase_already_recorded_is_done_when_its_item_runs_again`
  - `tests/test_bandcamp_cli.py::test_a_purchase_filtered_out_is_offered_on_the_next_run_without_the_filter`
  - `tests/test_bandcamp_cli.py::test_a_purchase_no_longer_downloadable_fails_permanently`
  - `tests/test_bandcamp_cli.py::test_a_purchase_the_record_holds_is_done_on_a_resume_and_fetched_nothing_twice`
  - ... and 40 more, see the JSON sidecar

Old text:

```
    from cratekit.label import registry as labels

    del origin
```

New text:

```
    del origin
```

### `u205.C5_server_error_read_as_absence`

app client: a 500 is raised as the not found, so an outage reads as no track and sync pair remembers a miss

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u205.json`, row `C5_server_error_read_as_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[500]`

Old text:

```
        if status == NOT_FOUND_STATUS and absence:
```

New text:

```
        if (status == NOT_FOUND_STATUS and absence) or status == 500:
```

### `r289-b.B5_job_directory_before_its_items`

Reclaim the job directory first, so its item directories never go

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B5_job_directory_before_its_items`
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
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
```

New text:

```
        _reclaim(job_dir, removed)
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
```

### `r668-a.M3_no_empty_job_guard`

an empty --job identifier is not refused, so it falls through to the queueing path and queues the list a second time

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M3_no_empty_job_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_empty_job_identifier_is_refused_rather_than_queueing_the_list_again`

Old text:

```
    if ctx.args.job is not None and not ctx.args.job.strip():
        raise _unusable(
```

New text:

```
    if False:
        raise _unusable(
```

### `u169.A1_retryable_policy_declined`

refused_for_good: drop the retryable clause, so a retryable policy refusal is skipped

- File: `src/cratekit/acquire/cli.py`
- Source: `u169.json`, row `A1_retryable_policy_declined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 250 against a baseline of 250
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_only_a_permanent_cause_in_the_policy_class_is_refused_for_good`

Old text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable
```

New text:

```
    return cause.code is ExitCode.REFUSED_BY_POLICY
```

### `u42-author.C4_marked_lossless_dropped`

Stop reporting a lossless file that wears the lossy marker

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C4_marked_lossless_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`

Old text:

```
            elif marked:
                found.append(_item(path, root, "marked-lossless"))
```

New text:

```
            elif False:
                found.append(_item(path, root, "marked-lossless"))
```

### `u54-acquisition-worker.G11_not_acquired`

Commit a per-track result that is not an acquisition

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G11_not_acquired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 8 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`

Old text:

```
    if result.outcome is not TrackOutcome.ACQUIRED:
        raise _refused_track(result, invocation.adapter)

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G27_remedy_absent_stays_absent`

Restore the non-transient remedy fallback, so a delisted track is told to relax the lossless policy

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G27_remedy_absent_stays_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`

Old text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else None),
```

New text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else Remedy.RELAX_LOSSLESS_POLICY),
```

### `u80-b.F9_coverage_weight`

The score weights similarity 60 and word coverage 40, not half and half

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80-b.json`, row `F9_coverage_weight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_the_score_is_half_similarity_half_word_coverage`

Old text:

```
    said = 50.0 * ratio + 50.0 * coverage
```

New text:

```
    said = 60.0 * ratio + 40.0 * coverage
```

### `u80.F2_order_reversed`

YouTube is searched before SoundCloud, against the source system's order

- File: `src/cratekit/acquire/fallback.py`
- Source: `u80.json`, row `F2_order_reversed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_ranked_candidates_are_offered_on_one_item`
  - `tests/test_acquire_fallback.py::test_ranking_breaks_a_tie_by_platform_then_order_and_dedupes_urls`

Old text:

```
PLATFORMS: tuple[str, ...] = (SOUNDCLOUD, YOUTUBE)
```

New text:

```
PLATFORMS: tuple[str, ...] = (YOUTUBE, SOUNDCLOUD)
```

### `u81-fetch-b.Y1_no_option_terminator`

The address is passed without the option terminator in front of it

- File: `src/cratekit/acquire/fallback.py`
- Source: `u81-fetch-b.json`, row `Y1_no_option_terminator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_the_shipped_fetcher_extracts_mp3_drops_upload_metadata_and_ends_on_the_address`

Old text:

```
            "--",
            url,
```

New text:

```
            url,
```

### `u80.C8_outage_narrowed`

Only FallbackUnavailable is an outage, so any other searcher failure crashes

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u80.json`, row `C8_outage_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback.py::test_any_searcher_failure_is_an_outage_not_a_crash`

Old text:

```
                except Exception as exc:  # noqa: BLE001 - refused whole, never swallowed
```

New text:

```
                except fallback.FallbackUnavailable as exc:
```

### `u81-fetch-a.W8_upload_tags_kept`

The upload's own tag block is not stripped before the row's artist and title are written

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `u81-fetch-a.json`, row `W8_upload_tags_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_fallback_fetch.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_tempo_the_upload_carried_is_never_committed`

Old text:

```
        written = tags.strip_tags(landed) and tags.write_tags(
```

New text:

```
        written = tags.write_tags(
```

### `r1016.M1_account_walk_back_on_the_clients_method`

The account walk calls the client's playlist_and_favorite_playlists again, which parses through parse_factory and fetches every owned playlist, the defect itself

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M1_account_walk_back_on_the_clients_method`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 14 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listed_playlist_carries_the_fields_the_callers_read`
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_a_user_without_the_parts_the_account_walk_reaches_is_refused_by_name`
  - `tests/test_adapter_listing.py::test_account_playlists_are_returned_unfiltered`
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[a-list]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[an-error-body]`
  - `tests/test_adapter_listing.py::test_an_account_answer_that_is_not_a_page_is_refused_not_read_as_the_end[items-null]`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_an_account_request_that_rejects_the_arguments_refuses_by_name_unslept`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_catalogue_and_the_folder_reads_hand_the_plans_what_the_pages_said`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_keeps_the_playlists_the_account_created`
  - `tests/test_label_tidal_catalogue.py::test_the_account_listing_pages_past_the_first_page`

Old text:

```
    return paginate(
        _account_playlists_endpoint(session.user),
        **_shape("account_playlists", **kwargs),
    )
```

New text:

```
    return paginate(
        _paged_caller(session.user, "playlist_and_favorite_playlists"),
        **_shape("account_playlists", **kwargs),
    )
```

### `r1016.S1_account_dedup_dropped`

Sample of an existing guard: the account listing loses its dedup by identifier, so a playlist re-served across a page boundary is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `S1_account_dedup_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 794 against a baseline of 794
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_account_playlists_page_and_deduplicate`

Old text:

```
    kwargs.setdefault("key", lambda playlist: str(getattr(playlist, "id", "")))
    return paginate(
        _account_playlists_endpoint(session.user),
```

New text:

```
    return paginate(
        _account_playlists_endpoint(session.user),
```

### `r878-a.A3_budget_off_by_one`

paginate_cursor: let the budget guard allow one request past the cap, so a cursor that never changes spends more than its budget

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A3_budget_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_cursor_that_never_changes_spends_the_budget_and_refuses`

Old text:

```
        if pages >= max_pages:
            raise ListingTruncated(
                f"{shape or 'listing'} spent its whole budget of {max_pages} requests "
                f"at {page_size} per page without reaching the end, having collected "
                f"{len(items)} item(s). The budget is sized far above any real "
                f"collection, so reaching it means the provider is not advancing its "
                f"cursor. Returning
```

New text:

```
        if pages > max_pages:
            raise ListingTruncated(
                f"{shape or 'listing'} spent its whole budget of {max_pages} requests "
                f"at {page_size} per page without reaching the end, having collected "
                f"{len(items)} item(s). The budget is sized far above any real "
                f"collection, so reaching it means the provider is not advancing its "
                f"cursor. Returning
```

### `r878-b.B6_order_by_name`

FOLDER_ORDER: order by date rather than the name the client asks for

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B6_order_by_name`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_the_folder_request_is_the_one_the_client_sends_with_a_cursor_and_no_offset`

Old text:

```
FOLDER_ORDER = "NAME"
```

New text:

```
FOLDER_ORDER = "DATE"
```

### `u65.B1_favourites_back_to_the_short_page`

R-383 reintroduced exactly: the favourites walk ends on a short page again

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B1_favourites_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 9 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_each_wrapper_docstring_names_the_rule_its_table_declares`
  - `tests/test_adapter_listing.py::test_every_shape_declares_the_rule_its_provider_can_actually_support`
  - `tests/test_adapter_listing.py::test_the_declared_count_is_retried_on_the_same_ladder_every_page_is`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`
  - `tests/test_outbound_tidal_account.py::test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one`
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_has_heart_answers_a_whole_sweep_from_one_paged_read`

Old text:

```
    "favorite_tracks": StopRule.DECLARED_TOTAL,
```

New text:

```
    "favorite_tracks": StopRule.SHORT_PAGE,
```

### `u65.C4_the_short_page_rule_stops_every_walk`

the rule argument is dropped from the short page test, so every shape stops short

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C4_the_short_page_rule_stops_every_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 199 against a baseline of 199
- Kills: 13 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_of_624_playlists_is_paced_in_seconds_not_minutes`
  - `tests/test_adapter_listing.py::test_a_listing_with_no_declared_total_walks_to_an_empty_page`
  - `tests/test_adapter_listing.py::test_a_playlist_that_publishes_no_count_degrades_rather_than_refusing`
  - `tests/test_adapter_listing.py::test_a_playlist_whose_provider_omits_a_track_reads_to_the_end`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
  - `tests/test_adapter_listing.py::test_an_account_listing_of_owned_playlists_costs_its_pages_and_no_single_fetch`
  - `tests/test_adapter_listing.py::test_an_artist_release_listing_reads_to_the_end_across_both_methods`
  - `tests/test_adapter_listing.py::test_the_account_playlists_listing_reads_to_the_end_at_its_own_page_size`
  - `tests/test_adapter_listing.py::test_the_favourites_listing_reads_the_whole_account_and_not_its_newest_fraction`
  - `tests/test_outbound_tidal_account.py::test_a_heart_already_held_makes_no_write_and_a_new_one_makes_exactly_one`
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`
  - `tests/test_outbound_tidal_account.py::test_has_heart_answers_a_whole_sweep_from_one_paged_read`

Old text:

```
        if stop is StopRule.SHORT_PAGE and len(page) < page_size:
```

New text:

```
        if len(page) < page_size:
```

### `u65.F1_an_unpageable_listing_takes_its_single_page`

U14's guard: a listing that cannot page truncates silently instead of refusing

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `F1_an_unpageable_listing_takes_its_single_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`
- Collected: 86 against a baseline of 86
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_listing_that_rejects_pagination_arguments_refuses`
  - `tests/test_adapter_listing.py::test_the_refusal_is_immediate_and_is_not_slept_on`

Old text:

```
        except TypeError as exc:
            raise ListingNotPaginated(
```

New text:

```
        except TypeError as exc:
            del exc
            return fn()
        except RuntimeError as exc:
            raise ListingNotPaginated(
```

### `r679-b.B6_one_shape_only`

retire_questions: ask about the first shape only, so a version question is never retired

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B6_one_shape_only`
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
            for identity in found.wanted.questions()
```

New text:

```
            for identity in found.wanted.questions()[:1]
```

### `u205.O2_no_country_still_opens`

opener: an account naming no country still gets an app client, asked in no country

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O2_no_country_still_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 353 against a baseline of 353
- Kills: 1 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_an_account_that_names_no_country_gets_no_app_client`

Old text:

```
    if country is None:
        return None
```

New text:

```
    if False:
        return None
```

### `r703-a.LF2_cause_not_worded`

landed_file drops the cause from the message

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `LF2_cause_not_worded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 4 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_failure_message_with_no_exception_is_the_cause`
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`
  - `tests/test_adapter_contract.py::test_a_rate_limited_album_read_reaches_the_item_cause_by_name`
  - `tests/test_adapter_contract.py::test_an_error_the_tool_logs_from_its_except_is_the_cause`

Old text:

```
            message = f"{message}; {describe_cause(cause)}"
```

New text:

```
            message = f"{message}"
```

### `r703-b.O1_proxy_notes_nothing`

the observed session re-raises without noting, so the unlogged lookup error is lost

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `O1_proxy_notes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 275 against a baseline of 275
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_a_not_found_album_read_is_named_and_stays_transient`
  - `tests/test_adapter_contract.py::test_a_rate_limited_album_read_reaches_the_item_cause_by_name`
  - `tests/test_adapter_contract.py::test_a_session_the_tool_saw_rejected_is_an_invocation_auth_failure`
  - `tests/test_adapter_contract.py::test_the_observed_session_writes_through_and_raises_what_it_notes`

Old text:

```
                log.note(exc)
                raise
```

New text:

```
                raise
```

### `r83.D8_vendored_defect_first`

R-348: the vendored source no longer asks the defect question before the token heuristic

- File: `src/cratekit/acquire/vendored.py`
- Source: `r83.json`, row `D8_vendored_defect_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`
- Collected: 157 against a baseline of 157
- Kills: 2 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_defect_the_tool_swallowed_breaks_the_adapter`
  - `tests/test_adapter_contract.py::test_the_vendored_source_reads_a_defect_naming_a_token_as_a_defect`

Old text:

```
    raise_if_defect(exc)
    if classify_unavailable(exc)
```

New text:

```
    if classify_unavailable(exc)
```

### `u47-author.CODEC_suffix_instead_of_container`

Classify by file suffix rather than by mutagen's container class, which gives the wrong answer for the .m4a this defect produced

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_suffix_instead_of_container`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_classifier_reads_mutagens_container_and_not_the_file_extension`

Old text:

```
    container = type(handle).__name__
```

New text:

```
    container = str(path.suffix).lstrip(".").upper()
```

### `u47-author.R197_argument_set_shrinks`

Remove event_abort from the declared argument set, so the set no longer describes what fetch passes

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_argument_set_shrinks`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 3 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_every_keyword_fetch_passes_exists_on_the_real_downloader`
  - `tests/test_adapter_contract.py::test_the_downloader_construction_in_the_source_names_every_argument`
  - `tests/test_adapter_contract.py::test_the_downloader_gets_every_argument_the_vendored_cli_passes`

Old text:

```
        "event_abort",

```

New text:

```
(empty)
```

### `u47-author.SAMPLE_permanence_asked_second`

Existing guard: ask the authentication heuristic before the permanence question, so a track whose stream token is missing aborts the whole run

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `SAMPLE_permanence_asked_second`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_the_vendored_source_escalates_a_dead_session_but_not_a_dead_track`

Old text:

```
    if classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT:
        return
    if is_authentication_failure(exc):
```

New text:

```
    if is_authentication_failure(exc):
```

### `u254.M05_cache_identity_no_inode`

_as_left: leave the inode out of the identity, so a replaced file of the same size reads as left

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M05_cache_identity_no_inode`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`

Old text:

```
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)
```

New text:

```
    return (found.st_dev, 0, found.st_size, found.st_mtime_ns)
```

### `u254.M14_header_unterminated`

_read_journal: accept a header with no line ending after it

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M14_header_unterminated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 743 against a baseline of 743
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_wrong_journal_refuses_rather_than_reading_as_empty[a header alone with no newline]`

Old text:

```
    if len(lines) < 2:
```

New text:

```
    if len(lines) < 1:
```

### `r1991.A1_vocal_unrecorded`

planned_destinations: leave out the vocal additions, so a with vox playlist adoption filed is never recorded

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r1991.json`, row `A1_vocal_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_outside_root.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_land_filing.py`, `tests/test_organize.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_second_genre_guards_counts.py`
- Collected: 521 against a baseline of 521
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_planned_destinations_name_each_pair_once_and_skip_what_names_none`

Old text:

```
    places += [(entry.bucket, entry.vocal_sub) for entry in plan.vocal_additions()]

```

New text:

```
(empty)
```

### `r788-d.A2_vocal_rows_never_written`

planned_memberships: the vocal additions are left out of the write, so the gate lists memberships the apply never performs

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r788-d.json`, row `A2_vocal_rows_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
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

### `u27-adopt-apply-author.A3_missing_gate_refuses_under_the_wrong_reason`

Report a verb declaring no approval gate as a configuration problem

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u27-adopt-apply-author.json`, row `A3_missing_gate_refuses_under_the_wrong_reason`
- Moved: the refusal is now built through core.cause.refuse, whose first argument is the reason; the same reason is swapped
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`
- Collected: 17 against a baseline of 17
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_is_found_by_digest_source_not_by_position`

Old text:

```
        "internal-error",
        f"{entry.name} declares no gate digested against the plan, so "
```

New text:

```
        "config-unusable",
        f"{entry.name} declares no gate digested against the plan, so "
```

### `u55-collection-reader.R24_worker_digest_check`

The worker applies a plan nobody approved, because the frozen digest is not compared

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `u55-collection-reader.json`, row `R24_worker_digest_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if plan.digest() != frozen_digest:
```

New text:

```
    if False:
```

### `u23-round-8-independent.X3_approval_actor_unchecked`

An approval naming nobody is accepted at apply time

- File: `src/cratekit/adopt/approval.py`
- Source: `u23-round-8-independent.json`, row `X3_approval_actor_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_an_approval_with_no_actor_is_refused`

Old text:

```
    if not str(approval.actor).strip():
```

New text:

```
    if approval.actor is None:
```

### `r780-a.A11_tree_reading_from_entry_sub`

the tree path takes adoption's sub as the reading in every bucket, so a track with no entry sub has no target and a double is left rather than moved

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A11_tree_reading_from_entry_sub`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_the_reading_is_asked_of_the_one_resolver_in_either_bucket`

Old text:

```
    if claims(entry, bucket):
        return entry.sub
    try:
```

New text:

```
    if entry.sub:
        return entry.sub
    try:
```

### `r780-a.A9_refused_buckets_empty`

no bucket is ever read as refused, so a verdict is honoured nowhere in the tree path

- File: `src/cratekit/adopt/move.py`
- Source: `r780-a.json`, row `A9_refused_buckets_empty`
- Moved: the same expression joined onto one line by the formatter; it is emptied as before
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
    return frozenset(entry.bucket for entry in entries if entry.withheld_by == WITHHELD_BY_VERDICT)
```

New text:

```
    return frozenset()
```

### `u118-c.M6_verdict_reason`

A Soul track a verdict refused is listed as no reading

- File: `src/cratekit/adopt/move.py`
- Source: `u118-c.json`, row `M6_verdict_reason`
- Moved: the split place reasons are now the ladder _listed, which the former place listing shares; a refused bucket loses its verdict reason, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`
- Collected: 58 against a baseline of 58
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_split_place.py::test_a_soul_track_whose_folder_a_verdict_refused_is_listed_and_r_and_b_moves_nothing`

Old text:

```
    elif refused:
        reason = LEFT_VERDICT
    else:
        reason = otherwise
```

New text:

```
    elif refused:
        reason = otherwise
    else:
        reason = otherwise
```

### `r758-b.C6_left_target_is_added_back`

a track approved as already in its target that has left it is added back and its other sub removed

- File: `src/cratekit/adopt/move_cli.py`
- Source: `r758-b.json`, row `C6_left_target_is_added_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_track_approved_as_in_its_target_that_left_it_is_a_stale_decision`

Old text:

```
        if now.add and not move.add:
            stale[move.content_id] = "it has left the sub it was approved as holding"
            continue

```

New text:

```
(empty)
```

### `r731-b.M17_bridge_tree_raises_at_the_plan`

a tree on the bridge raises out of the reader instead of answering unread

- File: `src/cratekit/adopt/placements.py`
- Source: `r731-b.json`, row `M17_bridge_tree_raises_at_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 6 (killed)
- Killed:
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.apply]`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_workers.py::test_an_uncut_library_marks_nothing_and_the_job_stays_resumable[None]`
  - `tests/test_adopt_workers.py::test_an_uncut_library_reads_neither_its_tree_nor_its_vocals`

Old text:

```
        except (tree_registry.TreeModeRefused, tree_registry.RegistrySkew):
```

New text:

```
        except tree_registry.RegistrySkew:
```

### `r797-b.M1_found_in_the_holding_folder`

named_place: look for a former place in the declaring bucket's folder, where the old playlist never was

- File: `src/cratekit/adopt/placements.py`
- Source: `r797-b.json`, row `M1_found_in_the_holding_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`
- Collected: 172 against a baseline of 172
- Kills: 5 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_former_place_is_found_in_the_folder_of_the_bucket_that_held_it`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_former_place.py::test_the_writer_is_told_to_leave_the_old_playlist_by_its_own_names`

Old text:

```
    return declared.bucket(former.bucket).display, former.display
```

New text:

```
    return declared.bucket(bucket_id).display, former.display
```

### `r722.P2_build_drops_level`

build_adoption_plan passes None instead of the scanned track's reading

- File: `src/cratekit/adopt/plan.py`
- Source: `r722.json`, row `P2_build_drops_level`
- Moved: the resolved sub is now named sub and handed to _destined; the energy level is dropped from the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 653 against a baseline of 653
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_changed_reading_moves_the_digest`
  - `tests/test_adopt_energy.py::test_a_tagged_file_lands_in_the_band_its_energy_falls_in`
  - `tests/test_adopt_energy.py::test_adoption_lands_a_track_where_the_routing_pass_would`

Old text:

```
            sub = _sub_for(declared, bucket, track.genre, track.energy)
```

New text:

```
            sub = _sub_for(declared, bucket, track.genre, None)
```

### `r731-a.M04_renamed_sub_not_withheld`

a track in the planned sub under another name only is routed, so the writer doubles it

- File: `src/cratekit/adopt/plan.py`
- Source: `r731-a.json`, row `M04_renamed_sub_not_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_placements.py`, `tests/test_adopt_workers.py`
- Collected: 70 against a baseline of 70
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_placements.py::test_a_track_in_the_planned_sub_under_another_name_only_is_withheld`
  - `tests/test_adopt_workers.py::test_an_approved_apply_leaves_a_withheld_track_where_it_sat`

Old text:

```
    if not held or (sub in held and sub not in unnamed):
```

New text:

```
    if not held or sub in held:
```

### `r788-a.P1_untagged_is_added`

vocal_place: drop the tag check, so every routed track of a calibrated library is filed under the vocal sub

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-a.json`, row `P1_untagged_is_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 11 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_a_plan_with_no_vocal_addition_hands_the_writer_what_it_always_did`
  - `tests/test_adopt_vocals.py::test_a_tagged_track_with_no_bucket_is_counted_as_one_and_not_passed_over`
  - `tests/test_adopt_vocals.py::test_a_track_without_the_tag_is_never_added`
  - `tests/test_adopt_vocals.py::test_an_untagged_track_sitting_in_a_vocal_sub_is_left_out_of_the_plan_entirely`
  - `tests/test_adopt_vocals.py::test_one_apply_writes_the_entries_and_the_vocal_subs_in_one_mapping`
  - `tests/test_adopt_vocals.py::test_the_counts_add_up_to_the_tagged_tracks_of_the_census`
  - `tests/test_adopt_vocals.py::test_the_digest_changes_when_a_vocal_membership_is_added_to_the_plan`
  - `tests/test_adopt_vocals.py::test_the_document_names_the_count_and_lists_every_membership_it_may_write`
  - `tests/test_adopt_vocals.py::test_the_gate_shows_what_the_document_says_about_vocals`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`
  - `tests/test_adopt_workers.py::test_an_untagged_membership_of_a_vocal_sub_is_never_removed`

Old text:

```
    if not vocals.filing or not vocals.carries(content_id):
```

New text:

```
    if not vocals.filing:
```

### `r788-b.P16_digest_moves_under_its_own_apply`

digest: cover the additions only, so the apply's own write moves the digest and a stopped run refuses its own work

- File: `src/cratekit/adopt/plan.py`
- Source: `r788-b.json`, row `P16_digest_moves_under_its_own_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_vocals.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_workers.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_vocals.py::test_every_row_the_writer_may_be_handed_is_on_the_gate_whatever_the_tree_holds_now`
  - `tests/test_adopt_vocals.py::test_the_digest_does_not_move_when_the_membership_it_approved_lands`
  - `tests/test_adopt_workers.py::test_an_approved_apply_files_the_tagged_tracks_and_touches_nothing_else`

Old text:

```
                "vocal": [vocal_id(entry) for entry in self.vocal_memberships()],
```

New text:

```
                "vocal": [vocal_id(entry) for entry in self.vocal_additions()],
```

### `u956.O15_document_blind_to_outside`

to_json: an empty outside_root list, so the gate shows none of the rows the plan leaves out

- File: `src/cratekit/adopt/plan.py`
- Source: `u956.json`, row `O15_document_blind_to_outside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 687 against a baseline of 687
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`
  - `tests/test_adopt_outside_root.py::test_the_plan_counts_and_names_every_row_it_leaves_outside`

Old text:

```
        "outside_root": [outside_row(entry) for entry in plan.outside_root()],
```

New text:

```
        "outside_root": [],
```

### `u23-round-8-independent.A6_at_risk_original_by_identity`

The original clause compares by object identity rather than by value

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A6_at_risk_original_by_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
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
    if held is record.original:
        return True
    return held in ((record.written,), (written,))

```

### `u23-round-8-independent.E2_vacancy_parent_check_inverted`

Vacancy requires the containing directory to be ABSENT

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `E2_vacancy_parent_check_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
        if not recorded.parent.is_dir():
            return False
        return not recorded.exists()
```

New text:

```
        if recorded.parent.is_dir():
            return False
        return not recorded.exists()
```

### `u23-round-8-independent.S1_size_of_always_none`

_size_of never answers, so every size shortcut on every path is disabled

- File: `src/cratekit/adopt/revert_changed.py`
- Source: `u23-round-8-independent.json`, row `S1_size_of_always_none`
- Moved: Anchored where u310-replay-after-b.json replayed it: the same text, now in src/cratekit/adopt/revert_changed.py, was in src/cratekit/adopt/revert.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_LEGACY_record_SURVIVES_A_RENAME_rather_than_being_doubled`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
    try:
        return target.stat().st_size
    except OSError:
        return None

```

New text:

```
    return None

```

### `u23-round-8-independent-composites.X6_composite_excluded_becomes_routed`

What X6 holds: the EXCLUDED disposition itself, forced to ROUTE

- File: `src/cratekit/adopt/scan.py`
- Source: `u23-round-8-independent-composites.json`, row `X6_composite_excluded_becomes_routed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 619 against a baseline of 619
- Kills: 5 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped`
  - `tests/test_adoption.py::test_every_plan_entry_identifier_is_derivable_from_the_record_it_names`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`

Old text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.EXCLUDED,
                genre=row.genre,
            )
            continue

```

New text:

```
        if readability not in ADOPTABLE:
            yield ScannedTrack(
                content_id=row.content_id,
                recorded=row.recorded,
                path=path,
                readability=readability,
                disposition=Disposition.ROUTE,
                genre=row.genre,
            )
            continue

```

### `u956.O12_unaskable_parent_answers`

within_root: a parent that cannot be asked ends the walk, so a row under a gone folder of an aliased root reads outside it

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `O12_unaskable_parent_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`
- Collected: 641 against a baseline of 641
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_outside_root.py::test_within_root_is_anchored_on_whole_components_and_reads_no_dots[/anything/at/all.flac-/-True]`
  - `tests/test_adopt_outside_root.py::test_within_root_reaches_the_root_through_a_name_that_is_the_same_directory`

Old text:

```
        except (OSError, ValueError):
            continue
    return False
```

New text:

```
        except (OSError, ValueError):
            return False
    return False
```

### `u956.S19_unadoptable_routes`

existing, scan_rows: route an unadoptable row, so a missing file is planned for a playlist

- File: `src/cratekit/adopt/scan.py`
- Source: `u956.json`, row `S19_unadoptable_routes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_outside_root.py`, `tests/test_adoption.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`
- Collected: 687 against a baseline of 687
- Kills: 14 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_outside_root.py::test_a_row_mapped_outside_the_root_is_excluded_and_keeps_its_path`
  - `tests/test_adopt_outside_root.py::test_adopt_move_reads_the_same_disposition`
  - `tests/test_adopt_outside_root.py::test_adopt_scan_counts_each_sampler_row_outside_the_root`
  - `tests/test_adopt_outside_root.py::test_an_apply_over_sampler_rows_files_the_rest_and_records_no_sampler_row`
  - `tests/test_adopt_outside_root.py::test_the_gate_names_each_sampler_row_it_leaves_out`
  - `tests/test_adopt_outside_root.py::test_the_plan_counts_and_names_every_row_it_leaves_outside`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_adopt_workers.py::test_an_apply_over_a_cut_over_library_writes_the_memberships`
  - `tests/test_adopt_workers.py::test_the_membership_write_is_derived_from_the_plan_and_not_from_the_run`
  - `tests/test_adoption.py::test_a_location_naming_another_host_is_reported_rather_than_guessed`
  - `tests/test_adoption.py::test_a_row_whose_location_column_is_NULL_does_not_end_the_census`
  - `tests/test_adoption.py::test_an_excluded_track_is_carried_in_the_plan_rather_than_dropped`
  - `tests/test_adoption.py::test_the_plan_carries_every_scanned_row_whatever_happened_to_it`

Old text:

```
        if readability not in ADOPTABLE:
```

New text:

```
        if False:
```

### `u241.M16_changed_settings_keep_old_heads`

ahead: heads measured under the old calibration are used after it changes

- File: `src/cratekit/analysis/ahead.py`
- Source: `u241.json`, row `M16_changed_settings_keep_old_heads`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_each_setting_a_head_is_measured_under_is_compared[drift-cut]`
  - `tests/test_analysis_ahead.py::test_each_setting_a_head_is_measured_under_is_compared[tempo-window]`
  - `tests/test_analysis_ahead.py::test_settings_that_changed_mid_run_stop_the_pool_and_the_rest_is_measured_here`

Old text:

```
    if settings != session.settings:
        session.stop(STOPPED_SETTINGS)
        return None

```

New text:

```
(empty)
```

### `u223.M24_report_link_followed`

staged_report: read a report that is a link

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M24_report_link_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_or_report_is_never_read_as_the_twin`

Old text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
    if path.is_symlink() or not path.is_file():
        return None
```

New text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
    if not path.is_file():
        return None
```

### `u223.M9_report_unparsed`

staged_report: let a report that is not JSON raise

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M9_report_unparsed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin`

Old text:

```
    except (OSError, ValueError):
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    except OSError:
        return None
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

### `u90-a.A6_dispatch_truthiness`

The hand path dispatched on truthiness, so a cut of 0 falls through to the fit

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-a.json`, row `A6_dispatch_truthiness`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`

Old text:

```
    if ctx.args.vocal_cut is not None:
```

New text:

```
    if ctx.args.vocal_cut:
```

### `u90-b.B8_hand_reads_old_after_write`

The hand path reads the previous cut after its own write, so it reports itself

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u90-b.json`, row `B8_hand_reads_old_after_write`
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
    previous, before = _previous_vocal_cut(cfg)
    today = _today()
    target = _write_vocal_calibration(
        cfg, cut, method=VOCAL_METHOD_HAND, note=f"set by hand on {today}", set_on=today
    )
```

New text:

```
    today = _today()
    target = _write_vocal_calibration(
        cfg, cut, method=VOCAL_METHOD_HAND, note=f"set by hand on {today}", set_on=today
    )
    previous, before = _previous_vocal_cut(cfg)
```

### `u94-a.S6_music_folder_not_wide`

_is_library_wide: accept the root alone, so the music folder every module places tracks under is refused as not the library

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-a.json`, row `S6_music_folder_not_wide`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_music_folder_walked_recursively_is_the_library_too`

Old text:

```
    for candidate in (root, root / cfg.library.music_dir):
```

New text:

```
    for candidate in (root,):
```

### `u94-b.W7_omissions_dropped_from_the_fit`

analyze_calibrate: leave the walk's omissions off the envelope of a fit that went ahead

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-b.json`, row `W7_omissions_dropped_from_the_fit`
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
        + tuple(omitted),
```

New text:

```
        + tuple(()),
```

### `u94-c.N8_absent_folder_not_told_apart`

analyze_calibrate: drop the not a folder answer, so a mistyped path is told it is not the library root

- File: `src/cratekit/analysis/calibrate.py`
- Source: `u94-c.json`, row `N8_absent_folder_not_told_apart`
- Moved: the same text, now in src/cratekit/analysis/calibrate.py, was in src/cratekit/analysis/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`
  - `tests/test_analysis_workers.py::test_calibrate_over_a_folder_that_is_not_there_says_that_and_not_empty`

Old text:

```
    if not folder.is_dir():
        return _calibrate_refusal(
```

New text:

```
    if False:
        return _calibrate_refusal(
```

### `u223.M14_any_status`

_staged_twin: accept a report of any status

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M14_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    elif status != "skipped-prefixed" or report.get("resumed_after_rename") is not True:
        return None
```

New text:

```
    elif False:
        return None
```

### `u306.A1_zero_told_apart`

analysis.cli.nothing_to_queue: read every zero as an empty folder, so a mistyped or unmounted folder says nothing new to do for analyze, restamp and vocals

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A1_zero_told_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_folder_that_is_not_there_is_a_different_zero_from_an_empty_one`

Old text:

```
    if folder.is_dir():
        return ctx.envelope(data=no_job(state), outcome=Outcome.NO_OP, warnings=extra)
```

New text:

```
    if True:
        return ctx.envelope(data=no_job(state), outcome=Outcome.NO_OP, warnings=extra)
```

### `u343.M05_untitled_title_with_a_head`

_untitled: render the title with a key and tempo head, the head the run no longer writes

- File: `src/cratekit/analysis/cli.py`
- Source: `u343.json`, row `M05_untitled_title_with_a_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_analyze_adopt.py`, `tests/test_restamp_scored_by.py`
- Collected: 324 against a baseline of 324
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-lossy-marked-first]`
  - `tests/test_analysis_workers.py::test_the_run_titles_only_a_file_with_no_title_and_never_with_a_head[untitled-the-stem]`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`

Old text:

```
        stem=path.stem, suffix=path.suffix, lossy=bool(marker) and marker in path.stem
    )
```

New text:

```
        stem=path.stem, suffix=path.suffix, lossy=bool(marker) and marker in path.stem,
        key="08A", bpm=124,
    )
```

### `u58-workers-and-wav.R9_missing_file_analysed`

Drop the source-missing refusal for a file that vanished

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R9_missing_file_analysed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`

Old text:

```
        if twin is None:
            raise _refuse_missing(item, folder, path, "analyse")

```

New text:

```
(empty)
```

### `u263.D14_whole_frames`

_parse_float_wav: keep a stray sample past the last whole frame

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D14_whole_frames`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_float_wav_on_a_pipe_is_read_to_its_end_in_whole_frames`

Old text:

```
            whole = available - available % (4 * channels)
```

New text:

```
            whole = available - available % 4
```

### `u263.D9_file_protocol`

_ffmpeg_samples: pass the path bare, so a name with a colon is read as a protocol

- File: `src/cratekit/analysis/decode.py`
- Source: `u263.json`, row `D9_file_protocol`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_path_with_a_colon_is_read_as_a_file`

Old text:

```
        "-i", f"file:{path}",
```

New text:

```
        "-i", f"{path}",
```

### `u264.M3_trailing_zero_dropped`

_mean_of_two: drop librosa 1.0's buffer of zeros, so a half sum that rounds to minus zero stays minus zero on 1.0

- File: `src/cratekit/analysis/decode.py`
- Source: `u264.json`, row `M3_trailing_zero_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[-0.0-right5-80000000-00000000]`
  - `tests/test_analysis_decode.py::test_a_zero_takes_the_sign_each_measured_release_gives_it[left4-0.0-80000000-00000000]`

Old text:

```
    if zero_after:
        # librosa 1.0 adds the mean into zeros: a half sum that rounds to
        # minus zero, minus the smallest subnormal and zero, is plus zero.
        out += out.dtype.type(0)
```

New text:

```
    if zero_after:
        pass
```

### `u157.D10_verdict_cut`

analyse_file: read the verdict against the shipped default, not the bound cut

- File: `src/cratekit/analysis/detect.py`
- Source: `u157.json`, row `D10_verdict_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_drift.py`, `tests/test_analysis_tempo.py`, `tests/test_drift.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
drift_words.verdict(drift, drift_cut)
```

New text:

```
drift_words.verdict(drift, DEFAULT_DRIFT_CUT)
```

### `u241.M27_no_warm_up_before_the_first_head`

analyse_file: no warm up, so two workers on a cold cache compile into it together, crash, and leave it damaged

- File: `src/cratekit/analysis/detect.py`
- Source: `u241.json`, row `M27_no_warm_up_before_the_first_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_warm.py`
- Collected: 15 against a baseline of 15
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_warm.py::test_the_detector_asks_for_the_warm_up_before_it_decodes`

Old text:

```
    warm.kernels()

```

New text:

```
    warm.kernels  # not called

```

### `u344.M5_measure_not_warmed`

features_from_path: drop the warm up, so a process measuring energy first compiles differently from one that ran a head

- File: `src/cratekit/analysis/energy.py`
- Source: `u344.json`, row `M5_measure_not_warmed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_restamp_scored_by.py`, `tests/test_analysis_workers.py`, `tests/test_analysis_warm.py`, `tests/test_energy_one_measure_librosa.py`, `tests/test_analysis_ahead.py`
- Collected: 497 against a baseline of 497
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_warm.py::test_the_energy_measure_asks_for_the_warm_up_before_it_decodes`

Old text:

```
    warm.kernels()
    # THROUGH THE ONE DECODER (U263), which
```

New text:

```
    # THROUGH THE ONE DECODER (U263), which
```

### `u327.A17_policy_before_files`

apply_adopt: drop the policy check before the first file, so a plan naming another column writes the files and the title

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A17_policy_before_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_plan_that_would_write_the_tempo_column_is_refused_by_policy`

Old text:

```
    metadata.assert_within_policy(row_changes(writes))

```

New text:

```
(empty)
```

### `u327.A8_no_reference_left`

plan_row: drop the no answer guard, so a row with neither key nor tempo reads as agreeing

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u327.json`, row `A8_no_reference_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_missing_key_never_stops_the_tempo_nor_a_missing_tempo_the_key`

Old text:

```
    if key is None and tempo is None:
```

New text:

```
    if False:
```

### `u342.P3_headless_is_stamped`

plan_row: never take the stamp path, so a headless title is left no-head as before U342

- File: `src/cratekit/analysis/head_adopt.py`
- Source: `u342.json`, row `P3_headless_is_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 12 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_file_already_stamped_is_continued_by_planning_again`
  - `tests/test_analyze_adopt.py::test_a_file_with_no_title_tag_is_titled_by_the_run_so_adopt_stamps_it_after_the_visit`
  - `tests/test_analyze_adopt.py::test_a_headless_row_rekordbox_did_not_key_or_time_is_left_and_named`
  - `tests/test_analyze_adopt.py::test_a_headless_row_whose_tag_carries_another_title_is_left`
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
    if parsed is None:
        # NO HEAD
```

New text:

```
    if False:
        # NO HEAD
```

### `u342.C1_unanswered_names_the_half`

_why_left: drop the missing half from a headless row's reason

- File: `src/cratekit/analysis/head_adopt_cli.py`
- Source: `u342.json`, row `C1_unanswered_names_the_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_adopt.py`, `tests/test_restore_tags.py`, `tests/test_naming.py`, `tests/test_no_beatgrid_ever.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_analyze_adopt.py::test_a_headless_row_rekordbox_did_not_key_or_time_is_left_and_named`

Old text:

```
    if item.reason == ha.NO_HEAD_UNANSWERED and item.notes:
```

New text:

```
    if False:
```

### `u275.M3_slope_rounded_down`

LIGHT_BYTES_PER_SECOND rounded down to 3.0 megabytes a second, over every peak but under a ninth above the measured slope

- File: `src/cratekit/analysis/light.py`
- Source: `u275.json`, row `M3_slope_rounded_down`
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
LIGHT_BYTES_PER_SECOND = 25 * 1024 * 1024 // 8
```

New text:

```
LIGHT_BYTES_PER_SECOND = 3 * 1024 * 1024
```

### `u343.M10_mark_reads_the_wrong_field`

marked: read the drift tag in place of the mark, an identity not unique to the run's measure

- File: `src/cratekit/analysis/run.py`
- Source: `u343.json`, row `M10_mark_reads_the_wrong_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 6 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_batch_resume_skips_a_file_carrying_the_mark_and_reads_the_rest`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_an_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_item_written_before_its_row_moved_resumes_by_its_mark_and_is_measured_once`
  - `tests/test_vocals_cli.py::test_unscored_queues_a_file_the_run_marked_with_no_score_and_leaves_the_rest`
  - `tests/test_vocals_cli.py::test_unscored_reads_the_head_by_the_rule_analyze_run_skips_by`

Old text:

```
    return tags.read_tag(path, MARK_FIELD) is not None
```

New text:

```
    return tags.read_tag(path, "drift") is not None
```

### `sitting3.G2_missing_target_read_as_fixture`

A label table lacking a target falls back to the first three columns instead of raising

- File: `src/cratekit/analysis/vocal.py`
- Source: `sitting3.json`, row `G2_missing_target_read_as_fixture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis.py::test_class_indices_resolve_the_singing_columns_by_name`

Old text:

```
    except ValueError as exc:
        raise ValueError(
            f"the vocal model's label table does not name all of {TARGET_LABELS}"
        ) from exc
    return (first, second, third)

```

New text:

```
    except ValueError:
        return (0, 1, 2)
    return (first, second, third)

```

### `u263.D18_vocal_reason`

vocals.analyse: let a missing decoder fail the item rather than name it

- File: `src/cratekit/analysis/vocals.py`
- Source: `u263.json`, row `D18_vocal_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_decode.py`, `tests/test_analysis_decode_librosa.py`, `tests/test_analysis_workers.py`
- Collected: 234 against a baseline of 234
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_decode.py::test_the_vocal_pass_names_the_missing_decoder`

Old text:

```
    except DecoderMissing:
        return _inactive(result, REASON_NO_DECODER)
```

New text:

```
    except DecoderMissing:
        raise
```

### `u92-author.G1_guard_deleted`

Delete the oversize guard from analyse entirely, which is main's state

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G1_guard_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_file_over_the_cap_never_reaches_the_decoder`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_an_oversize_file_is_refused_without_loading_the_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    if is_oversize(result.get("path")):
        return _inactive(result, REASON_AUDIO_TOO_LARGE)

```

New text:

```
(empty)
```

### `u92-author.G9_warning_counts_the_wrong_reason`

unscored_warning counts size refusals, so an oversize file is reported as a missing model

- File: `src/cratekit/analysis/vocals.py`
- Source: `u92-author.json`, row `G9_warning_counts_the_wrong_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 231 against a baseline of 231
- Kills: 5 (killed)
- Killed:
  - `tests/test_analysis.py::test_a_model_whose_table_lacks_the_targets_fails_at_load_not_per_track`
  - `tests/test_analysis_workers.py::test_a_run_over_an_oversize_track_reports_it_and_writes_no_vox_tag`
  - `tests/test_analysis_workers.py::test_a_run_with_no_model_loaded_warns_on_the_envelope`
  - `tests/test_analysis_workers.py::test_an_oversize_track_is_never_warned_about_as_a_missing_model`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`

Old text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_MODEL_UNAVAILABLE, 0))
```

New text:

```
    count = int(summary.get("by_vocal_reason", {}).get(REASON_AUDIO_TOO_LARGE, 0))
```

### `r221-a.W6_twin_branch_says_it_unconditionally`

The reported twin always carries the word, so a person asking twice for a REAL backup is told the open job copies nothing. Removing the helper's own guard is W2; this is the branch's own reading of the job it hands back

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W6_twin_branch_says_it_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_asking_for_a_backup_twice_reports_the_open_job_rather_than_a_second`

Old text:

```
                    *_rehearsal(twin),
```

New text:

```
                    rehearsal_warning(),
```

### `r222-b.B14_destination_claimed_unread`

Reword the unreadable case to the ordinary sentence's opening, so the warning no longer says the configuration was not rebuilt

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B14_destination_claimed_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`

Old text:

```
        "its frozen configuration could not be rebuilt, so where it writes is "
```

New text:

```
        "its frozen configuration was not consulted, so where it writes is "
```

### `r222-b.B8_every_exception_is_unreadable`

Catch every exception from the rebuild, so a defect in it is reported as an open backup with exit zero

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B8_every_exception_is_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`

Old text:

```
        except (config.ConfigError, ValueError):
            return job, None
```

New text:

```
        except Exception:
            return job, None
```

### `r349-b.B4_stage_error_completes`

A staging write error escapes the handler instead of completing the item

- File: `src/cratekit/backup/cli.py`
- Source: `r349-b.json`, row `B4_stage_error_completes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except OSError:
        return None
    return jobs.Produced
```

New text:

```
    except KeyError:
        return None
    return jobs.Produced
```

### `r757-c2.S7_verb_says_nothing_of_the_comparison`

backup_library: leave the comparison sentence off the resumed envelope

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S7_verb_says_nothing_of_the_comparison`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                *comparison_warning(reported["progress"].get(OUTCOMES)),
```

New text:

```
                *(),
```

### `u45-round-1.C6_partial_run_refused`

Refuse whenever any portion did not run, so a mirror that completed while the database was skipped is reported as a failure

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `C6_partial_run_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_nothing_that_ran_is_never_reported_as_a_refusal`

Old text:

```
    if any(entry.ran for entry in outcome.portions):
        return None
```

New text:

```
    if all(entry.ran for entry in outcome.portions):
        return None
```

### `u45-round-1.W2_report_from_the_plan`

Report the PLAN rather than the OUTCOME, which is the shell half of the first-caller defect

- File: `src/cratekit/backup/cli.py`
- Source: `u45-round-1.json`, row `W2_report_from_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 10 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_partial_run_succeeds_and_publishes_only_the_half_that_ran`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_every_command_the_engine_ran_is_paired_with_its_own_return_code`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    report = backup.outcome_payload(outcome)
```

New text:

```
    report = backup.plan_payload(plan)
```

### `u50-author.B1_no_items_enqueued`

Queue the backup with no items, so the driver has nothing to claim and reports an empty success

- File: `src/cratekit/backup/cli.py`
- Source: `u50-author.json`, row `B1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 89 against a baseline of 89
- Kills: 30 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_a_resume_reports_the_queued_job_rather_than_filing_a_second`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_an_open_backup_whose_destinations_cannot_be_read_is_not_read_as_elsewhere`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`
  - ... and 15 more, see the JSON sidecar

Old text:

```
            item_ids=backup_items(),
```

New text:

```
(empty)
```

### `r290-author.D1_dispatcher_ignores_the_type`

Make the dispatcher blind to JobBlocked, so a parked job exits non zero and says failed

- File: `src/cratekit/cli/__init__.py`
- Source: `r290-author.json`, row `D1_dispatcher_ignores_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_parity.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_adopt.py`, `tests/test_label_workers.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_packaging.py`, `tests/test_pending_units.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_skills_lint.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 7231 against a baseline of 7231
- Kills: 47 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
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
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[intake.playlist]`
  - ... and 32 more, see the JSON sidecar

Old text:

```
        parked = isinstance(exc, JobBlocked)
```

New text:

```
        parked = False
```

### `r388-b.M12_listing_steps_say_take_a_backup`

Replace the listing failure's first reserved step with the take a backup step it replaced

- File: `src/cratekit/cli/exit_codes.py`
- Source: `r388-b.json`, row `M12_listing_steps_say_take_a_backup`
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
            "check the backup remote is reachable from this machine; the snapshot "
            "is not known to be missing, a listing of it failed",
```

New text:

```
            "no dated database snapshot exists for this library yet; take a "
            "backup before a restore can be planned",
```

### `r925.J4_isrc_dropped`

job show lists every track without its ISRC

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J4_isrc_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`

Old text:

```
                "isrc": str(said["isrc"]) if said.get("isrc") else None,
```

New text:

```
                "isrc": None,
```

### `r678-a.A4_empty_job_id_renders_a_job`

a queue that held nothing prints a job line with an empty identifier

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A4_empty_job_id_renders_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/intake/test_workers.py`, `tests/test_acquire_workers.py`, `tests/test_tag_workers.py`, `tests/test_intake_imported.py`
- Collected: 327 against a baseline of 327
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_empty_playlist_queues_nothing_and_says_so`
  - `tests/test_render_payloads.py::test_an_empty_job_id_is_a_queue_that_held_nothing_and_renders_nothing`
  - `tests/test_render_payloads.py::test_the_job_list_case_belongs_to_the_listing_alone`
  - `tests/test_tag_workers.py::test_a_folder_with_nothing_to_tag_names_no_job`

Old text:

```
    if not isinstance(job_id, str) or not job_id:
        return []
```

New text:

```
    if not isinstance(job_id, str):
        return []
```

### `r685-a.L4_an_unreadable_copy_falls_back`

An active copy that cannot be read is replaced by the shipped template instead of refused

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `r685-a.json`, row `L4_an_unreadable_copy_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_that_cannot_be_read_refuses_rather_than_falling_back[copy-not-text]`

Old text:

```
    except (OSError, UnicodeDecodeError) as exc:
        raise refuse(

```

New text:

```
    except (OSError, UnicodeDecodeError) as exc:
        return _shipped(cfg.taxonomy.template)
        raise refuse(

```

### `u260.E11_reset_forgets_nothing`

reset_cache: clear nothing, so one test's encode answers the next test's

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E11_reset_forgets_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 13 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a refusal]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[a transport failure]`
  - `tests/test_album_cover_once.py::test_a_fetch_that_failed_for_one_file_is_asked_again_for_the_next[an empty answer]`
  - `tests/test_album_cover_once.py::test_different_bytes_are_encoded_apart`
  - `tests/test_album_cover_once.py::test_every_file_carries_byte_for_byte_what_it_carried_before`
  - `tests/test_album_cover_once.py::test_the_encode_memory_drops_the_least_recently_used`
  - `tests/test_album_cover_once.py::test_the_encode_memory_keeps_a_few_pictures_and_forgets_the_oldest`
  - `tests/test_album_cover_once.py::test_the_encode_reset_forgets`
  - `tests/test_album_cover_once.py::test_the_same_bytes_at_another_size_or_cap_are_encoded_again`
  - `tests/test_album_cover_once.py::test_two_addresses_serving_the_same_bytes_make_two_requests_and_one_encode`
  - `tests/test_album_cover_once.py::test_two_albums_in_one_folder_make_two_requests_and_two_encodes`
  - `tests/test_album_cover_once.py::test_two_pictures_of_one_length_are_encoded_apart`
  - `tests/test_tag_workers.py::test_an_albums_cover_is_asked_for_and_encoded_once_across_the_queued_sweep`

Old text:

```
    with _remembered_lock:
        _remembered.clear()
```

New text:

```
    with _remembered_lock:
        pass
```

### `u260.E8_encode_hit_not_refreshed`

to_cdj_jpeg_remembered: a hit no longer refreshes its entry, so the memory is first in first out

- File: `src/cratekit/core/art.py`
- Source: `u260.json`, row `E8_encode_hit_not_refreshed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_art.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_the_encode_memory_drops_the_least_recently_used`

Old text:

```
        if made is not None:
            _remembered.move_to_end(key)
            return made
```

New text:

```
        if made is not None:
            return made
```

### `u83-a.E5_over_cap_refusal`

A picture that cannot fit comes back over the cap, as the source system returned it, instead of raising

- File: `src/cratekit/core/art.py`
- Source: `u83-a.json`, row `E5_over_cap_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_picture_that_cannot_fit_raises_rather_than_exceeding_the_cap`
  - `tests/test_art.py::test_the_encoder_never_goes_below_the_quality_floor`

Old text:

```
    raise ArtError(
        f"the image does not fit
```

New text:

```
    return CdjJpeg(encoded, img.size[0], img.size[1], 24)
    raise ArtError(
        f"the image does not fit
```

### `u83-b.W10_id3_add_tags`

The ID3 branch skips add_tags on a file with no tag yet, the step whose absence pushes a caller toward a bare ID3 object

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W10_id3_add_tags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 9 (killed)
- Killed:
  - `tests/test_art.py::test_a_chunk_container_never_receives_a_bare_id3_stream[.aiff-FORM]`
  - `tests/test_art.py::test_a_chunk_container_never_receives_a_bare_id3_stream[.wav-RIFF]`
  - `tests/test_art.py::test_a_picture_over_the_cap_is_refused_and_the_file_untouched`
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.aiff]`
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.wav]`
  - `tests/test_art.py::test_an_art_write_leaves_the_decoded_audio_unchanged[.aiff]`
  - `tests/test_art.py::test_an_art_write_leaves_the_decoded_audio_unchanged[.wav]`
  - `tests/test_art.py::test_the_id3_frame_is_a_front_cover_jpeg[.aiff]`
  - `tests/test_art.py::test_the_id3_frame_is_a_front_cover_jpeg[.wav]`

Old text:

```
                # and saved against them. add_tags() is the container's own way.
                handle.add_tags()
```

New text:

```
                # and saved against them. add_tags() is the container's own way.
                pass
```

### `u83-b.W6_flac_block_width`

The FLAC block declares width zero, the vendored downloader's defect

- File: `src/cratekit/core/art.py`
- Source: `u83-b.json`, row `W6_flac_block_width`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_art.py`
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_art.py::test_a_written_cover_is_the_bytes_given_reads_back_measured_and_is_replaced_by_the_next[.flac]`
  - `tests/test_art.py::test_the_flac_block_carries_nonzero_width_height_and_depth`

Old text:

```
            block.width = measured.width
```

New text:

```
            block.width = 0
```

### `r757-b2.F3_full_record_does_not_move_the_date`

record: ignore full_comparison=True

- File: `src/cratekit/core/backup_facts.py`
- Source: `r757-b2.json`, row `F3_full_record_does_not_move_the_date`
- Moved: U953 folded the two date moves of record into one loop over pairs, so pairing the full comparison key with False ignores full_comparison=True exactly as the old if False did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 728 against a baseline of 728
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_damaged_full_comparison_entry_refuses_its_own_reader_and_no_other`
  - `tests/test_backup_comparison.py::test_a_record_a_few_minutes_ahead_is_zero_days_old_and_not_minus_one`
  - `tests/test_backup_comparison.py::test_doctor_refuses_a_full_comparison_recorded_ahead_of_now`
  - `tests/test_backup_comparison.py::test_doctor_says_how_long_ago_a_full_comparison_last_ran`

Old text:

```
    for key, moved in ((FULL_COMPARISON_KEY, full_comparison), (FULL_CHECK_KEY, full_check)):
```

New text:

```
    for key, moved in ((FULL_COMPARISON_KEY, False), (FULL_CHECK_KEY, full_check)):
```

### `example-binaries-five-row.B5_credential_strip`

subprocess_env() stops stripping Cratekit credentials, so every spawned third-party binary receives a copy and the credential reaches a process listing.

- File: `src/cratekit/core/binaries.py`
- Source: `example-binaries-five-row.json`, row `B5_credential_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_binaries.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_binaries.py::test_a_spawned_process_does_not_inherit_an_opted_in_credential`

Old text:

```
        if not key.startswith(secrets.ENV_CREDENTIAL_PREFIX)

```

New text:

```
        if True

```

### `u45-round-1.V1_transfer_failure_is_a_defect`

Classify a failed transfer as INTERNAL, so an unreachable remote tells a person to report a bug

- File: `src/cratekit/core/cause.py`
- Source: `u45-round-1.json`, row `V1_transfer_failure_is_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5516 against a baseline of 5516
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`

Old text:

```
        "backup-transfer-failed": ExitCode.PRECONDITION,
```

New text:

```
        "backup-transfer-failed": ExitCode.INTERNAL,
```

### `u241.M09_ceiling_ignores_the_reserve`

worker_ceiling: every core, nothing kept back for the driver

- File: `src/cratekit/core/cores.py`
- Source: `u241.json`, row `M09_ceiling_ignores_the_reserve`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cores.py`, `tests/test_analysis_ahead.py`
- Collected: 314 against a baseline of 314
- Kills: 14 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it`
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_memory_overrules_a_wide_core_count`
  - `tests/test_analysis_ahead.py::test_the_cost_is_set_by_the_costliest_track_in_the_batch`
  - `tests/test_analysis_ahead.py::test_the_light_pool_is_refused_by_the_gates_whatever_the_cores_say`
  - `tests/test_analysis_ahead.py::test_two_cores_leave_no_ceiling_for_a_pool`
  - `tests/test_cores.py::test_a_ceiling_from_many_cores_never_widens_what_memory_affords`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[11-2-9]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[2-2-1]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[3-2-1]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[4-2-2]`
  - `tests/test_cores.py::test_the_ceiling_is_the_cores_less_what_is_kept_back_and_never_under_one[8-1-7]`
  - `tests/test_cores.py::test_the_reader_is_looked_up_when_called_so_a_test_can_stand_in`

Old text:

```
    return max(1, cores - reserved)

```

New text:

```
    return max(1, cores)

```

### `r390-a.A1_retry_re_arms_unconditionally`

the original defect: retry re-arms every failed item whatever the job cause says

- File: `src/cratekit/core/jobs.py`
- Source: `r390-a.json`, row `A1_retry_re_arms_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_acquire_workers.py`
- Collected: 210 against a baseline of 210
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_jobs.py::test_a_partial_failure_whose_failures_are_permanent_is_not_resumable`
  - `tests/test_jobs.py::test_resuming_a_job_of_permanent_failures_through_the_verb_refuses`
  - `tests/test_jobs.py::test_two_distinct_permanent_reasons_name_both_whichever_failed_last`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`

Old text:

```
    if current.cause is not None and not current.cause.retryable:
        raise refuse(
            "job-not-retryable",
            f"job {job_id} {current.state} with a cause that is not retryable, "
            f"so resuming it cannot succeed and its items were left as they are",
            steps=(
                "inspect each failed item's cause on the job's own record",
                "queue the work again the way it was queued the first time, "
                "once the reason is addressed",
            ),
            origin=("jobs",),
            detail={
                "job_id": job_id,
                "state": str(current.state),
                # Named on the refusal as the job cause names them (R-391), so
                # a person is not sent into the nested cause to learn which.
                **_permanent_reasons_of(current.cause),
            },
            inner=current.cause,
        )

```

New text:

```
(empty)
```

### `u169.E3_decline_writes_failed`

decline_item: record the item failed rather than skipped

- File: `src/cratekit/core/jobs_drive.py`
- Source: `u169.json`, row `E3_decline_writes_failed`
- Moved: the same text, now in src/cratekit/core/jobs_drive.py, was in src/cratekit/core/jobs.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_acquire_workers.py`
- Collected: 153 against a baseline of 153
- Kills: 10 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`
  - `tests/test_jobs.py::test_a_declined_item_is_skipped_with_its_cause_and_the_job_succeeds`
  - `tests/test_jobs.py::test_a_real_failure_beside_a_declined_item_still_fails_the_job_and_names_both`
  - `tests/test_jobs.py::test_a_retry_re_arms_the_failure_and_leaves_the_declined_item_settled`

Old text:

```
            (str(ItemState.SKIPPED), json.dumps(cause.to_json()), job_id, item_id),
```

New text:

```
            (str(ItemState.FAILED), json.dumps(cause.to_json()), job_id, item_id),
```

### `u39-naming-independent.E2_wheel_letter_widened`

Existing guard sample: the Camelot letter class admits C, not just A/B

- File: `src/cratekit/core/naming.py`
- Source: `u39-naming-independent.json`, row `E2_wheel_letter_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_naming.py`, `tests/test_naming_budget.py`, `tests/test_reports_cli.py`
- Collected: 1486 against a baseline of 1486
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_off_wheel_key_is_rejected_rather_than_normalized[8C]`

Old text:

```
_CAMELOT_LETTER = r"[AB]"

```

New text:

```
_CAMELOT_LETTER = r"[ABC]"

```

### `u205.G8_since_keeps_earlier_app_calls`

spend since: the app's share is not differenced, so a run is charged the app calls made before it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u205.json`, row `G8_since_keeps_earlier_app_calls`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 23216 against a baseline of 23216
- Kills: 6 (killed)
- Promoted: subset killed 0, full suite killed 6
- Killed:
  - `tests/test_catalogue_app.py::test_process_spend_carries_the_apps_share`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[excludes-another-processs-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[names-rate-limit-answers]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[reports-its-calls]`
  - `tests/test_provider_gate.py::test_a_run_that_reached_the_provider_reports_its_calls[survives-a-refusal]`
  - `tests/test_provider_gate.py::test_process_spend_is_this_process_alone`

Old text:

```
            app_calls=max(0, self.app_calls - earlier.app_calls),
```

New text:

```
            app_calls=self.app_calls,
```

### `r239-a.A7_needed_always_true`

unlock_needed answers encrypted for every readable file, the U55 row that read zero with no encrypted input

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A7_needed_always_true`
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
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return True
```

### `u118-b.R1_split_competes`

A split place no longer competes in the bucket that declares it

- File: `src/cratekit/core/routing.py`
- Source: `u118-b.json`, row `R1_split_competes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_split_place.py`, `tests/test_adopt_former_place.py`
- Collected: 102 against a baseline of 102
- Kills: 20 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_split_place.py::test_a_soul_track_already_in_its_soul_band_only_leaves_r_and_b`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_a_renamed_r_and_b_band_is_left_since_the_writer_cannot_see_it`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names[another-band]`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names[low]`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_r_and_b_med_moves_to_the_soul_band_its_reading_names[same-band]`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_the_old_soul_r_and_b_playlist_moves_to_soul_and_is_withheld_until`
  - `tests/test_adopt_split_place.py::test_a_soul_track_in_two_r_and_b_bands_leaves_both_in_one_move_and_r_and_b_plans_none`
  - `tests/test_adopt_split_place.py::test_a_soul_track_with_no_reading_leaves_r_and_b_for_soul_unsorted`
  - `tests/test_adopt_split_place.py::test_a_split_place_competes_in_soul_and_nowhere_else`
  - `tests/test_adopt_split_place.py::test_a_track_in_an_r_and_b_band_holds_it_in_r_and_b_and_the_split_place_in_soul`
  - `tests/test_adopt_split_place.py::test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision[Deep House]`
  - `tests/test_adopt_split_place.py::test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision[R&B]`
  - `tests/test_adopt_split_place.py::test_a_track_retagged_out_of_soul_since_the_approval_is_a_stale_decision[]`
  - `tests/test_adopt_split_place.py::test_adoption_withholds_a_soul_track_still_in_an_r_and_b_band`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        | {place.id for place in taxonomy.bucket(bucket_id).split_from}

```

New text:

```
(empty)
```

### `r722.T3_open_failure_is_absent`

A mutagen open failure reads as absent in the checked reader

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T3_open_failure_is_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2994 against a baseline of 2994
- Kills: 3 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        log.debug("tag read failed for %s: %s", path, exc)
```

### `u247.M6_key_is_the_size`

load_taxonomy: key the memo on the text's length, so an edit that keeps the length is answered with the old declaration

- File: `src/cratekit/core/taxonomy.py`
- Source: `u247.json`, row `M6_key_is_the_size`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_workers.py`, `tests/test_tag_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 9 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_a_copy_rewritten_between_two_loads_is_read_and_judged_again`
  - `tests/test_active_taxonomy.py::test_two_libraries_each_answer_their_own_copy`
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_scan_queues_one_item_per_live_row_and_drives_them_all`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_taxonomy.py::test_an_edit_that_keeps_the_length_is_a_different_text_and_is_parsed_again`
  - `tests/test_taxonomy.py::test_the_memo_holds_eight_texts_and_parses_the_first_again_after_a_ninth`
  - `tests/test_taxonomy.py::test_the_three_texts_an_upgrade_reads_are_each_parsed_once`
  - `tests/test_taxonomy.py::test_two_texts_are_each_parsed_once_and_each_answers_its_own`

Old text:

```
    return _parsed(text)

```

New text:

```
    by_size = load_taxonomy.__dict__.setdefault("by_size", {})
    if len(text) not in by_size:
        by_size[len(text)] = _parsed(text)
    return by_size[len(text)]

```

### `r301.S1_month_ignores_ledger`

Sample of an existing guard: the monthly check ignores what the month already spent

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r301.json`, row `S1_month_ignores_ledger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_month_is_asked_once_over_the_whole_set_before_the_first_part`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_counts_what_the_ledger_already_holds`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
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

### `r706-b.B1_partition_front_loads_the_remainder`

The remainder goes to the first part whole instead of one chunk to each of the first parts, so a cut is uneven and can exceed the bound

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r706-b.json`, row `B1_partition_front_loads_the_remainder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`, `tests/test_isolation_survives_undo.py`
- Collected: 227 against a baseline of 227
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

### `r924.A3_cached_count_zero`

The plan line is told nothing was cached

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A3_cached_count_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`
- Collected: 78 against a baseline of 78
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

### `u103-a.A3_document_must_carry_its_plan`

Stop checking that a cache document carries the plan it was asked for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A3_document_must_carry_its_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 183 against a baseline of 183
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

### `u57-recognition-and-items.M18_missing_credential_is_unready`

A credential missing after the gate is reported as the gate class, not as credential-missing

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u57-recognition-and-items.json`, row `M18_missing_credential_is_unready`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`
- Collected: 175 against a baseline of 175
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_keychain_credentials_are_read_by_name_and_a_missing_one_is_credential_missing`

Old text:

```
            "credential-missing" if missing else "intake-recognition-unready",
```

New text:

```
            "intake-recognition-unready",
```

### `u259.M1_judge_no_row`

analyzed.judge: drop the answer for a row the collection lacks, so None reaches the removal marker read

- File: `src/cratekit/intake/analyzed.py`
- Source: `u259.json`, row `M1_judge_no_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analyze_check.py`, `tests/test_inbox_analyzed.py`
- Collected: 85 against a baseline of 85
- Kills: 6 (killed)
- Killed:
  - `tests/test_analyze_check.py::test_a_row_whose_id_is_not_text_stays_out_of_every_row_as_it_did`
  - `tests/test_analyze_check.py::test_a_scope_past_one_chunk_is_read_a_statement_a_500_and_answers_as_the_per_row_reads`
  - `tests/test_analyze_check.py::test_read_row_handed_no_row_reads_it_and_answers_as_handed_one`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_for_a_named_landing`
  - `tests/test_analyze_check.py::test_the_mixed_library_reads_as_the_per_row_reads_read_it_in_inbox_analyze`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`

Old text:

```
    if row is None:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

New text:

```
    if False:
        return Member(content_id=content_id, title="", action=WAIT, why=NO_ROW)
```

### `r682-a.M3_empty_why_counted`

an empty why is counted under the empty string as a reason

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M3_empty_why_counted`
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
            if isinstance(why, str):
```

### `u103-b.C8_set_no_op_carries_warnings`

Drop the warnings from intake set's nothing identified envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u103-b.json`, row `C8_set_no_op_carries_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                outcome=Outcome.NO_OP,
            )
```

### `u213.M8_readable_unread_excludes_read`

list_playlist_readable: keep a track as unread even when another row of it read

- File: `src/cratekit/intake/cli.py`
- Source: `u213.json`, row `M8_readable_unread_excludes_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`

Old text:

```
    unread = {ref: one for ref, one in refused.items() if ref not in tracks}
```

New text:

```
    unread = dict(refused)
```

### `u70.S5_source_id_recorded`

A hearts job is queued with no source_id, so nothing can tell it from a playlist job

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `S5_source_id_recorded`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`

Old text:

```
            source_id=FAVORITES_SOURCE_ID if hearts else None,
```

New text:

```
            source_id=None,
```

### `u103-b.C14_offered_under_its_own_key`

Offer identify's version questions under the match verb's key instead of its own

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u103-b.json`, row `C14_offered_under_its_own_key`
- Moved: the text moved whole from intake/cli.py to intake/cli_identify.py with its function (U307); the tests that killed it, test_identify_reports_an_owned_track_owned_an_offered_one_offered_and_the_rest_missing, were folded by the trim into test_identify_and_a_set_job_report_owned_offered_and_missing, every one of its eight checks, carried whole beside the set job's
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 596 against a baseline of 596
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`

Old text:

```
        cfg, result.rows, handler_key=ctx.entry.handler_key, run_id=ctx.run.run_id
```

New text:

```
        cfg, result.rows, handler_key="match.run", run_id=ctx.run.run_id
```

### `u104-d.C5_no_digest_token_is_the_address`

Take a digestless tracklist's token from the scratch path, which every fetched mix shares, instead of from the address

- File: `src/cratekit/intake/cli_identify.py`
- Source: `u104-d.json`, row `C5_no_digest_token_is_the_address`
- Moved: the same text, now in src/cratekit/intake/cli_identify.py, was in src/cratekit/intake/cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetched_mix_with_no_digest_is_named_by_its_address_and_not_its_scratch_file`

Old text:

```
    token = digest or digest_of({"path": held.ref})
```

New text:

```
    token = digest or digest_of({"path": str(held.path)})
```

### `r924.F1_no_start_line`

The fetch never says it started

- File: `src/cratekit/intake/fetch.py`
- Source: `r924.json`, row `F1_no_start_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_set_fetch.py`
- Collected: 52 against a baseline of 52
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_fetch_that_raises_still_stops_the_watcher`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_watcher_reports_the_bytes_written_while_the_download_runs`

Old text:

```
            progress(f"fetching: {address}")
```

New text:

```
            pass
```

### `u104-a.F4_landing_inside_scratch`

Drop the half of the landing check that requires the fetched file to be inside the scratch folder it was handed

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-a.json`, row `F4_landing_inside_scratch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_fetcher_that_lands_outside_its_folder_is_a_failed_fetch[outside]`

Old text:

```
        if not landed.is_file() or scratch.resolve() not in landed.resolve().parents:
```

New text:

```
        if not landed.is_file():
```

### `u104-c.P3_several_threshold`

Move the several recordings threshold from more than one to more than two, so exactly two landed recordings read as an ordinary failure

- File: `src/cratekit/intake/fetch.py`
- Source: `u104-c.json`, row `P3_several_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`
- Collected: 41 against a baseline of 41
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_the_shipped_fetcher_refuses_a_playlist_that_landed_two_recordings`

Old text:

```
            if len(landed) > 1:
```

New text:

```
            if len(landed) > 2:
```

### `u103-b.P2_digest_reaches_the_verb`

Drop the recording's digest between the identifier and the verb, so the tracklist falls back to a path name

- File: `src/cratekit/intake/pipeline.py`
- Source: `u103-b.json`, row `P2_digest_reaches_the_verb`
- Moved: the same copy of the digest into the verb's result, which U307 made one comprehension over the fields; leaving digest out gives its empty default, as the dropped argument did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 67 against a baseline of 67
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`

Old text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified)}
```

New text:

```
    copied = {one.name: getattr(found, one.name) for one in fields(recognize.Identified) if one.name != "digest"}
```

### `u37-author-light.G5_path_repair_queue`

Offer path repair into the adoption queue instead

- File: `src/cratekit/intake/repair.py`
- Source: `u37-author-light.json`, row `G5_path_repair_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_review_queue.py`, `tests/intake/test_repair.py`
- Collected: 155 against a baseline of 155
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_repair.py::test_propose_name_is_idempotent_and_offering_twice_offers_one_item`
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

### `u102-a.P6_missing_says_what_exists`

_plan_for: always word a missing file as a rename already carried out, whether or not any file carries the proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P6_missing_says_what_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`

Old text:

```
            if target.is_file():
                why = (
```

New text:

```
            if True:
                why = (
```

### `u102-b.G4_plan_collisions`

_plan_for: detect no collision while the plan is built, leaving it to the claim

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G4_plan_collisions`
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
    collides = naming_cli.held_collisions([(path, acc.proposed) for acc, path in free])
```

New text:

```
    collides: dict[str, str] = {}
```

### `u102-b.S1_stub_removed`

_apply: leave the zero byte claim behind when the rename did not happen

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `S1_stub_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_interrupt_or_a_refused_rename_after_the_claim_leaves_no_stub`

Old text:

```
            if not moved:
                target.unlink(missing_ok=True)
```

New text:

```
            if not moved:
                pass
```

### `u237.M4_case_sensitive_mark`

_YEAR: drop the case fold, so a lower case (p) mark is kept as part of the name

- File: `src/cratekit/label/harvest.py`
- Source: `u237.json`, row `M4_case_sensitive_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 354 against a baseline of 354
- Kills: 12 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cadenza-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos Barac-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Cronos-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Gettraum, LaMez-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Pressure Traxx-(p) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-(c) 2021 ]`
  - `tests/modules/test_labels.py::test_a_copyright_line_keeps_the_label_name_whole_under_every_prefix[Puls-(p) 2021 ]`

Old text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+", re.IGNORECASE)
```

New text:

```
_YEAR = re.compile(r"^(?:(?:\([PC]\)|[\u2117\u00a9])\s*)+")
```

### `r704-a.S1_no_cause_chain_check`

the sweep never asks whether the error or its declared causes are a rate limit, so the sitting's TooManyRequests is permanent again

- File: `src/cratekit/label/sweep.py`
- Source: `r704-a.json`, row `S1_no_cause_chain_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 524 against a baseline of 524
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[artist-resolve]`
  - `tests/test_label_workers.py::test_a_rate_limit_at_every_other_sweep_boundary_is_retryable[listing-probe]`
  - `tests/test_label_workers.py::test_a_rate_limited_listing_fails_its_item_as_retryable_and_the_job_says_resume`
  - `tests/test_label_workers.py::test_a_rate_limited_verification_is_retryable_too`
  - `tests/test_label_workers.py::test_a_resumed_job_rearms_the_rate_limited_label_and_not_the_settled_one`

Old text:

```
    if any(is_rate_limit(link) for link in _linked(exc, "__cause__")):
        return run.LookupFailure(message, rate_limited=True)

```

New text:

```
(empty)
```

### `u205.S3_catalogue_lookup_ignores_app`

label catalogue: tracks_for_isrc goes to the account session whatever the opener built, and intake missing with it

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `u205.json`, row `S3_catalogue_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_intake_missing_isrc.py`
- Collected: 248 against a baseline of 248
- Kills: 15 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[400]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[500]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[503]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[data-not-a-list]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-an-object]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-json]`
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[400]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[401]`
  - `tests/test_catalogue_app.py::test_a_token_service_refusing_the_app_is_a_rejected_app_credential[403]`
  - `tests/test_catalogue_app.py::test_an_isrc_catalogue_lookup_goes_to_the_app_and_intake_missing_with_it`
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`

Old text:

```
        self._lookups = catalogue if catalogue is not None else session
```

New text:

```
        self._lookups = session
```

### `u192.F3_keep_remedy_token`

_resumable: keep the job resume token, so the fix line names the detached worker ahead of the --job command

- File: `src/cratekit/modules/foreground.py`
- Source: `u192.json`, row `F3_keep_remedy_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_analysis_workers.py`
- Collected: 279 against a baseline of 279
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`

Old text:

```
    remediation = dataclasses.replace(cause.remediation, remedy=None, steps=steps)
```

New text:

```
    remediation = dataclasses.replace(cause.remediation, steps=steps)
```

### `r356-b.B7_heart_back_hands_on_no_title`

The hearts engine hands the account no title

- File: `src/cratekit/modules/outbound/hearts.py`
- Source: `r356-b.json`, row `B7_heart_back_hands_on_no_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_heart_back_hands_the_account_the_names_and_reports_its_reasons`

Old text:

```
            title=item.release_title,
```

New text:

```
            title="",
```

### `r229.L16_a_moved_record_is_not_followed`

The confirmed remote id is ignored, so a half driven job whose record moved creates a second playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L16_a_moved_record_is_not_followed`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_a_job_whose_confirmed_remote_playlist_nothing_records_refuses`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`

Old text:

```
        if expected and own != expected:
```

New text:

```
        if False:
```

### `r229.L6_a_living_crate_is_a_candidate`

A recorded key the export still carries is offered, so two crates sharing their tracks adopt each other

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L6_a_living_crate_is_a_candidate`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_key_the_export_still_carries_is_not_a_candidate`
  - `tests/modules/test_outbound.py::test_a_legacy_record_under_a_living_path_is_never_freed`
  - `tests/test_outbound_workers.py::test_a_crate_the_export_still_carries_is_never_adopted_from`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if False and (not written or _still_carries(written, living[key])):
```

### `u309-z.U13_shell_config_origin`

The outbound verbs' config refusal no longer names the verb that met it

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `u309-z.json`, row `U13_shell_config_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`, `tests/test_cli_contract.py`, `tests/test_favorites_pink.py`, `tests/test_shared_homes.py`
- Collected: 1320 against a baseline of 1320
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_an_unusable_config_is_refused_as_the_verb_that_met_it`

Old text:

```
    return output.load_config((origin,))
```

New text:

```
    return output.load_config(())
```

### `u27-reports-round-2.C3b_tie_break`

Sort on artist and name alone, leaving the tie to the walk

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-2.json`, row `C3b_tie_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
    return (placement.entry.artist, placement.entry.name, placement.entry.track_id)
```

New text:

```
    return (placement.entry.artist, placement.entry.name, "")
```

### `u27-reports-round-1.L7_shape_governed_filter`

Measure the tree shape over every folder in the export rather than the governed tree

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L7_shape_governed_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_taxonomy_whose_tree_this_library_does_not_use_reports_no_genres`
  - `tests/modules/test_reports_engines.py::test_the_shape_measures_the_governed_tree_from_its_own_node`

Old text:

```
    governed_folders = [
        path for path in view.folders if tree_display == path[-1] or tree_display in path[:-1]
    ]

```

New text:

```
    governed_folders = list(view.folders)

```

### `r154-b.B9_marker_failure_fails_the_portion`

Let a marker that cannot be written fail the database portion, which skips the settings and publishes no age over a good copy

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B9_marker_failure_fails_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_marker_that_cannot_be_written_warns_and_does_not_fail_the_backup`

Old text:

```
            if result.returncode != 0 and command.label == SNAPSHOT_IDENTITY:
```

New text:

```
            if False and command.label == SNAPSHOT_IDENTITY:
```

### `r1761.P3_identity_raise_refuses`

_not_the_recorded_volume: an identity read that raises is a refusal, so a flaky probe stops every backup

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r1761.json`, row `P3_identity_raise_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`, `tests/test_backup_quick.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/modules/test_tools.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    except Exception:  # noqa: BLE001 - an unread identity is left to the census
        return ""
```

New text:

```
    except Exception:  # noqa: BLE001 - an unread identity is left to the census
        return "the identity could not be read"
```

### `r222-a.A4_keep_zero_holds`

Hold the run's folders at a keep of zero, overruling a request to keep no archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A4_keep_zero_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 278 against a baseline of 278
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = [name for name in names if (floor is None or name > floor)]
```

### `r338-c.C3_rehearsed_restore_pulls_the_share`

TRANSFERRING_LABELS: leave the share's restore out, so a rehearsed restore really downloads it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r338-c.json`, row `C3_rehearsed_restore_pulls_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_rehearsed_restore_transfers_no_share`

Old text:

```
        RESTORE_DATABASE,
        RESTORE_SHARE,
    }
```

New text:

```
        RESTORE_DATABASE,
    }
```

### `r757-a.E6_unread_total_is_zero`

_count: answer zero for a total rclone did not give, so an unread run says it sent nothing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r757-a.json`, row `E6_unread_total_is_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value
```

New text:

```
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    return value
```

### `u311.A1_warning_key_order`

The shared warning builder writes message before code, changing every warning's key order in the envelope

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u311.json`, row `A1_warning_key_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`, `tests/test_process_guard.py`, `tests/test_process_scan.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 898 against a baseline of 898
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_engine_helpers_keep_their_shapes`

Old text:

```
    return {"code": code, "message": message}
```

New text:

```
    return {"message": message, "code": code}
```

### `u317.Q19_self_written_empty`

_self_written: the fact file counts as a change, so no run after a backup is ever skipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u317.json`, row `Q19_self_written_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return frozenset({rel.as_posix()})
```

New text:

```
    return frozenset()
```

### `u323.I5_provider_dropped_by_the_plan`

plan_backup: the caller's identity provider is not handed to the files portion, so the platform's own is read

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u323.json`, row `I5_provider_dropped_by_the_plan`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_backup_unproven_root.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                emptied=emptied,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
        )
    if backup_facts.Portion.DATABASE in wanted:
```

New text:

```
                emptied=emptied,
                identity_provider=None,
                mount_enumerator=mount_enumerator,
            )
        )
    if backup_facts.Portion.DATABASE in wanted:
```

### `u48-author.P2_purge_classification_dropped`

Failed purges return no warning, so folders survive with nothing saying so

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P2_purge_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 691 against a baseline of 691
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

New text:

```
    if False:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

### `r1761.P9_emptied_passes_on_the_fact_file`

_unproven: the emptied flag passes on the fact file alone, which a database item writes at a mount point (round two's N2)

- File: `src/cratekit/modules/tools/backup_proof.py`
- Source: `r1761.json`, row `P9_emptied_passes_on_the_fact_file`
- Moved: U311 moved the census proof out of backup.py into backup_proof.py with this line unchanged. On the base the row was killed only by the seam allowance test, which the mutant tripped by an incidental reach into the facts module from backup.py, and the guard's own tests need rclone and are this container's failures; from backup_proof.py the same reach crosses no seam, so U311 added test_the_emptied_flag_passes_on_the_files_record_and_not_on_the_fact_file_alone in tests/modules/test_tools.py, which writes a database record alone and asserts the emptied flag is still refused, the guard round two's N2 named
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_import_rules.py`
- Collected: 246 against a baseline of 246
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_emptied_flag_passes_on_the_files_record_and_not_on_the_fact_file_alone`
  - `tests/test_import_rules.py::test_no_package_crosses_a_seam_beyond_its_allowance`

Old text:

```
        if carried is not None:
            return "", False
```

New text:

```
        if backup_facts.path_for(cfg).is_file():
            return "", False
```

### `u311.A5_agrees_ignores_the_hash`

Two readings of a file agree whatever their hashes say

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u311.json`, row `A5_agrees_ignores_the_hash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_comparison.py`, `tests/test_backup_quick.py`, `tests/test_backup_unproven_root.py`
- Collected: 318 against a baseline of 318
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_quick_walk_reads_hashes_globs_and_names_as_rclone_does`

Old text:

```
        return (self.size, self.mtime_ns, self.sha256) == (other.size, other.mtime_ns, other.sha256)
```

New text:

```
        return (self.size, self.mtime_ns) == (other.size, other.mtime_ns)
```

### `u317.Q1_unlisted_folder_is_absence`

walk: a listed folder that is gone is skipped as absent, so its files read as removed (round one's B2)

- File: `src/cratekit/modules/tools/backup_record.py`
- Source: `u317.json`, row `Q1_unlisted_folder_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_quick.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            raise WalkRefused(
                f"{directory} was listed and then was not there, so the walk did "
                f"not see the whole library"
            ) from None
```

New text:

```
            continue
```

### `r154-a.A3_named_shape_check`

Never refuse a named snapshot on shape, which is the finding itself: the traversal value reaches the remote path again

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-a.json`, row `A3_named_shape_check`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 9 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[../another-library-snapshots/2020-01-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01T000000Z ]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01T000000Z/../../elsewhere]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-08-01]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-13-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[2026-8-01T000000Z]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[]`
  - `tests/modules/test_tools.py::test_a_snapshot_value_that_is_not_a_stamp_is_refused_before_the_remote_is_asked[newest]`
  - `tests/test_restore_cli.py::test_the_ledgers_traversal_value_is_refused_at_the_verb`

Old text:

```
        if not is_snapshot_name(snapshot):
```

New text:

```
        if False:
```

### `r154-b.B7_walk_order`

Walk oldest first, so the default pulls the OLDEST snapshot that is this library's

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r154-b.json`, row `B7_walk_order`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_default_takes_the_newest_snapshot_that_is_this_librarys`
  - `tests/modules/test_tools.py::test_the_default_walk_is_bounded_and_the_refusal_says_how_far_it_looked`
  - `tests/modules/test_tools.py::test_the_replaced_drive_identity_selects_the_newest_of_the_old_volumes`
  - `tests/test_restore_cli.py::test_a_backup_landing_between_the_two_acts_moves_the_digest`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
    newest = names[::-1][:NEWEST_WALK]
```

New text:

```
    newest = names[:NEWEST_WALK]
```

### `r338-b.R4_empty_listing_read_as_held`

share_is_held: read a listing that names nothing as a mirror, so a copy from an empty folder is planned and reported as pulled

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R4_empty_listing_read_as_held`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_share_mirror_that_lists_empty_is_absent_too`

Old text:

```
    return bool(result.stdout.strip())
```

New text:

```
    return True
```

### `r367.E2_an_unconfirmed_restore_is_allowed`

existing guard sample: a restore proceeds without the named decision

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `E2_an_unconfirmed_restore_is_allowed`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 283 against a baseline of 283
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_restore_is_a_named_decision_and_never_a_prompt`

Old text:

```
    if not confirmed:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
```

New text:

```
    if confirmed and False:
        raise BackupRefused(
            Refusal.RESTORE_NOT_CONFIRMED,
```

### `r367.G8_files_only_is_dropped`

directories in the snapshot folder can be read as sidecar names

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G8_files_only_is_dropped`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_snapshot_listing_is_of_the_database_folder`

Old text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
                "--files-only",
```

New text:

```
                f"{cfg.backup.db_dest_root}/{snapshot}/db/",
```

### `r388-b.M11_db_folder_absent_read_as_failure`

Drop the exit 3 branch on the contents listing, so a cut off backup sends the person to the remote

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r388-b.json`, row `M11_db_folder_absent_read_as_failure`
- Moved: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 723 against a baseline of 723
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_folder_rclone_says_is_absent_is_not_a_listing_failure[list-snapshot-contents-2026-08-01T000000Z-holds no database folder]`

Old text:

```
    if result.returncode == RCLONE_DIRECTORY_NOT_FOUND:
        # A backup cut off before its database folder was written.
```

New text:

```
    if False:
        # A backup cut off before its database folder was written.
```

### `u311.C4_24_bit_loses_its_depth`

A 24 bit source's encode no longer asks for 24 bits per sample

- File: `src/cratekit/modules/tools/mastering.py`
- Source: `u311.json`, row `C4_24_bit_loses_its_depth`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 248 against a baseline of 248
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_sixteen_bit_source_is_dithered_and_a_deeper_one_is_not`

Old text:

```
    return (*flac, "-sample_fmt", "s32", "-bits_per_raw_sample", "24"), "", "24-bit"
```

New text:

```
    return (*flac, "-sample_fmt", "s32"), "", "24-bit"
```

### `r187-b.B3_entry_not_a_mapping`

_entry_is_current: accept any entry that is present, so a list where a mapping belongs raises mid scan

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-b.json`, row `B3_entry_not_a_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 269 against a baseline of 269
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[list]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[text]`

Old text:

```
        isinstance(entry, dict)
        and entry.get("mtime_ns")
```

New text:

```
        entry is not None
        and entry.get("mtime_ns")
```

### `u311.C8_unreadable_number_raises`

A tag that is not a number raises instead of reading as absent

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C8_unreadable_number_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 340 against a baseline of 340
- Kills: 44 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[list]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[text]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-missing-fields]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-not-a-mapping]`
  - `tests/modules/test_tools.py::test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded[other-build]`
  - `tests/modules/test_tools.py::test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded[unstamped]`
  - `tests/modules/test_tools.py::test_a_cache_parsed_under_another_template_is_discarded`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[bpm-124]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[title-None]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[vox-value2]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[voxgender-4]`
  - `tests/modules/test_tools.py::test_a_headless_title_takes_the_key_adopt_writes_and_no_tempo`
  - `tests/modules/test_tools.py::test_a_marked_lossy_title_loses_its_marker_along_with_the_head`
  - `tests/modules/test_tools.py::test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer`
  - ... and 29 more, see the JSON sidecar

Old text:

```
    except (TypeError, ValueError):
        return None
```

New text:

```
    except TypeError:
        return None
```

### `u281.R2_limit_two`

REFUSALS_BEFORE_STOP: two rather than three, a moment's challenge stops the run

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `R2_limit_two`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_tag_workers.py`
- Collected: 138 against a baseline of 138
- Kills: 12 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_match_resets_the_count_as_a_miss_does`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_an_outage_between_refusals_ends_the_run_of_them`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`
  - `tests/test_beatport_refusal.py::test_the_binder_hands_the_run_count_to_the_searcher`
  - `tests/test_beatport_refusal.py::test_the_count_is_per_catalogue_so_a_refusing_one_never_stops_an_answering_one`
  - `tests/test_beatport_refusal.py::test_the_limit_is_three`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_the_next_sweep_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
REFUSALS_BEFORE_STOP = 3
```

New text:

```
REFUSALS_BEFORE_STOP = 2
```

### `u281.S7_body_note_reworded`

unread_outcome: the challenge script's note loses the Cloudflare challenge words the summary counts by

- File: `src/cratekit/tagging/catalogues.py`
- Source: `u281.json`, row `S7_body_note_reworded`
- Moved: the same text, now in src/cratekit/tagging/catalogues.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_tag_workers.py`
- Collected: 205 against a baseline of 205
- Kills: 1 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_page_carrying_only_cloudflares_script_is_blocked`

Old text:

```
            note=f"the catalogue answered with a {CLOUDFLARE_CHALLENGE} page",
```

New text:

```
            note="the catalogue answered with Cloudflare's challenge page",
```

### `u260.F2_empty_answer_remembered`

remembering: drop the empty answer check, so an empty answer is kept and handed to the next file without a request

- File: `src/cratekit/tagging/searchers.py`
- Source: `u260.json`, row `F2_empty_answer_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_album_cover_once.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_tagging_engine.py`
- Collected: 263 against a baseline of 263
- Kills: 1 (killed)
- Killed:
  - `tests/test_album_cover_once.py::test_an_empty_answer_handed_straight_in_is_not_remembered`

Old text:

```
        if not data or (admit is not None and not admit(data)):
```

New text:

```
        if data is None or (admit is not None and not admit(data)):
```

### `u281.S2_challenge_header_unread`

_refusal_note: never read Cf-Mitigated, so a Cloudflare 403 is only HTTP 403 and the warning cannot name the challenge

- File: `src/cratekit/tagging/searchers.py`
- Source: `u281.json`, row `S2_challenge_header_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`
- Collected: 447 against a baseline of 447
- Kills: 3 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_403_carrying_cloudflares_challenge_header_is_blocked_and_named`
  - `tests/test_beatport_refusal.py::test_the_challenge_header_is_read_whatever_case_its_name_and_value_arrive_in`
  - `tests/test_beatport_refusal.py::test_three_refusals_then_the_fourth_file_is_not_sent_and_records_blocked`

Old text:

```
    if mitigated.strip().lower() == _CF_CHALLENGE:
```

New text:

```
    if False:
```

### `u281.S1_beatport_reads_no_refusal`

_search_beatport: drop the shared refusal check, so a 403 is unreachable and a 200 challenge a parse break, as before the card

- File: `src/cratekit/tagging/shops.py`
- Source: `u281.json`, row `S1_beatport_reads_no_refusal`
- Moved: Anchored where u306-replay-after-a.json replayed it: the same text, now in src/cratekit/tagging/shops.py, was in src/cratekit/tagging/searchers.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_beatport_refusal.py`, `tests/test_catalogue_searcher.py`, `tests/test_discogs_searcher.py`, `tests/test_tag_workers.py`, `tests/test_published_genre.py`
- Collected: 447 against a baseline of 447
- Kills: 22 (killed)
- Killed:
  - `tests/test_beatport_refusal.py::test_a_200_challenge_beside_an_unread_discogs_refuses_as_unreachable_not_parse_broken`
  - `tests/test_beatport_refusal.py::test_a_200_just_a_moment_page_is_blocked_not_a_parse_break`
  - `tests/test_beatport_refusal.py::test_a_200_page_carrying_only_cloudflares_script_is_blocked`
  - `tests/test_beatport_refusal.py::test_a_403_carrying_cloudflares_challenge_header_is_blocked_and_named`
  - `tests/test_beatport_refusal.py::test_a_403_without_the_header_is_blocked_and_says_only_the_status`
  - `tests/test_beatport_refusal.py::test_a_429_that_outlasts_the_backoff_is_blocked_as_the_fallbacks_read_it`
  - `tests/test_beatport_refusal.py::test_a_discogs_match_after_a_stopped_beatport_is_written_and_names_beatport_unread`
  - `tests/test_beatport_refusal.py::test_a_new_run_asks_again_from_its_first_file`
  - `tests/test_beatport_refusal.py::test_a_searcher_given_no_count_keeps_its_own_for_its_life`
  - `tests/test_beatport_refusal.py::test_a_stopped_beatport_and_a_discogs_with_no_token_refuse_rather_than_decline`
  - `tests/test_beatport_refusal.py::test_a_stopped_catalogue_is_answered_without_a_wait`
  - `tests/test_beatport_refusal.py::test_another_mitigation_is_not_called_a_challenge`
  - `tests/test_beatport_refusal.py::test_blocked_miss_blocked_blocked_does_not_stop_the_run`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[not-sent]`
  - `tests/test_beatport_refusal.py::test_deezer_is_still_not_asked_beside_a_blocked_beatport[refused]`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    tracks = None if page.text is None else _beatport_tracks(page.text)
    if tracks is None:
        refused = unread_outcome(BEATPORT, page)
        if refused is not None:
            return refused
        return SourceOutcome(
```

New text:

```
    if page.text is None:
        return SourceOutcome(BEATPORT, Answer.UNREACHABLE, note=page.note)
    tracks = _beatport_tracks(page.text)
    if tracks is None:
        return SourceOutcome(
```

### `u133-b.T2_alias_gone`

Jazz loses its routing alias, so a track tagged Jazz reaches it only by the keyword

- File: `src/cratekit/templates/taxonomy.default.toml`
- Source: `u133-b.json`, row `T2_alias_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_jazz_folder.py`, `tests/test_routing_parity.py`, `tests/test_vocabulary.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 1222 against a baseline of 1222
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_jazz_folder.py::test_a_track_tagged_jazz_routes_to_the_jazz_folder_by_its_alias`
  - `tests/test_routing_parity.py::test_the_promoted_buckets_take_exactly_what_the_old_code_filed_in_the_playlists_they_left`

Old text:

```
aliases = [
  "Jazz",
]

```

New text:

```
aliases = []

```

### `u90-c.C6_wrapper_reads_nothing`

load_vocal_threshold stops delegating, so every caller sees an uncalibrated library

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c.json`, row `C6_wrapper_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 203 against a baseline of 203
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

### `r685-a.V1_route_inbox_export_reads_the_shipped_text`

The export routing verb parses the shipped text instead of loading the library's copy

- File: `src/cratekit/write/routing_export.py`
- Source: `r685-a.json`, row `V1_route_inbox_export_reads_the_shipped_text`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_active_taxonomy.py`, `tests/test_routing_workers.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_active_taxonomy.py::test_no_module_but_the_loader_reads_the_shipped_template`
  - `tests/test_routing_workers.py::test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none`
  - `tests/test_routing_workers.py::test_a_template_declaring_no_long_track_playlist_builds_none`
  - `tests/test_routing_workers.py::test_an_edit_to_the_active_copy_is_the_playlist_the_routing_plan_names`

Old text:

```
    declared = active_taxonomy.load(cfg)
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route inbox without --export, which "

```

New text:

```
    declared = taxonomy.load_taxonomy(taxonomy.shipped_template_text("default"))
    _refuse_off_the_bridge(
        cfg, declared, export, instead="run route inbox without --export, which "

```

### `r758-a.T6_removed_playlist_is_a_destination`

a playlist rekordbox removed answers for a destination, so an addition lands where nobody can see it

- File: `src/cratekit/write/trees.py`
- Source: `r758-a.json`, row `T6_removed_playlist_is_a_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`
- Collected: 87 against a baseline of 87
- Kills: 2 (killed)
- Killed:
  - `tests/test_adopt_move.py::test_a_sub_held_only_through_a_removed_playlist_is_not_planned_for_removal`
  - `tests/test_adopt_move.py::test_an_addition_never_lands_in_a_playlist_rekordbox_removed`

Old text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
        and not rb_writer.node_removed(playlist)
```

New text:

```
        and str(getattr(playlist, "ParentID", "")) in parents
```

### `u125.D1_derive_test_tautology`

Restore the derive test's cause-total assert to x == x so a broken reserved count stays green there

- File: `tests/test_reserved_causes.py`
- Source: `u125.json`, row `D1_derive_test_tautology`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 23216 against a baseline of 23216
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    assert (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ) == (len(causes), len(non_reserved), len(CAUSES)), (
        "derived cause totals from the pins disagree with the tree"
    )

```

New text:

```
    assert (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ) == (
        PINNED_RESERVED_CAUSE_COUNT + len(PINNED_NON_RESERVED_CAUSES),
        len(PINNED_NON_RESERVED_CAUSES),
        PINNED_RESERVED_CAUSE_COUNT,
    ), (
        "derived cause totals from the pins disagree with the tree"
    )

```

