# Mutation table: u305-replay-before

Measured by `scripts/mutate.py` on 2026-11-22 14:44 UTC, branch `HEAD` at `21155f99`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 665.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 78, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/b482b633-b7dc-5187-8c0a-c70b2c5040ef/scratchpad/known-failures-u305.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u197.M3_registry_load_fold` | `src/cratekit/acquire/__init__.py` | user | 2 file(s) | 574 | 1 | killed |
| `u197.M4_registry_alternatives_fold` | `src/cratekit/acquire/__init__.py` | user | 2 file(s) | 574 | 1 | killed |
| `r1313.A1_classifier_failure_alone` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 368 | 7 | killed |
| `r1313.A2_status_before_no_file_landed` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 368 | 2 | killed |
| `r1313.A3_classifier_name_on_any_link` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 368 | 1 | killed |
| `r703-a.A1_classifier_reads_text` | `src/cratekit/acquire/adapter.py` | user | 7 file(s) | 872 | 1 | killed |
| `r705-b.S7_acquire_one_softens_the_park_at_the_lookup` | `src/cratekit/acquire/adapter.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-b.S8_acquire_one_softens_the_park_at_the_fetch` | `src/cratekit/acquire/adapter.py` | user | 1 file(s) | 117 | 1 | killed |
| `r83.D1_offer_defect` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 8 | killed |
| `r83.D2_fetch_defect` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 2 | killed |
| `r83.D3_drop_attribute_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 6 | killed |
| `r83.D4_drop_type_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 2 | killed |
| `r83.D5_drop_name_error` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 4 | killed |
| `r83.D6_remedy` | `src/cratekit/acquire/adapter.py` | user | 6 file(s) | 755 | 11 | killed |
| `r83.D7_detail_names_class` | `src/cratekit/acquire/adapter.py` | maintainer | 6 file(s) | 755 | 9 | killed |
| `u246.S1_adapter_asked_empty` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 260 | 70 | killed |
| `u246.S2_adapter_per_element` | `src/cratekit/acquire/adapter.py` | maintainer | 2 file(s) | 190 | 1 | killed |
| `u47-author.CODEC_refused_track_sinks_the_run` | `src/cratekit/acquire/adapter.py` | user | 2 file(s) | 201 | 2 | killed |
| `u176-c5.C5_empty_page_ends` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 1 | killed |
| `u176.C10_trusted_https` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 2 | killed |
| `u176.C11_fetch_refuses_untrusted` | `src/cratekit/acquire/bandcamp.py` | user | 1 file(s) | 47 | 4 | killed |
| `u176.C12_transport_hides_text` | `src/cratekit/acquire/bandcamp.py` | user | 1 file(s) | 47 | 1 | killed |
| `u176.C1_rejected_status_is_session` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 1 | killed |
| `u176.C2_summary_names_a_fan` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 1 | killed |
| `u176.C3_page_error_is_rejected` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 1 | killed |
| `u176.C4_page_without_items_list` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 4 | killed |
| `u176.C6_repeated_token` | `src/cratekit/acquire/bandcamp.py` | maintainer | 1 file(s) | 47 | 1 | killed |
| `u176.C7_preorder_not_downloadable` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 7 | killed |
| `u176.C8_member_base_name` | `src/cratekit/acquire/bandcamp.py` | user | 2 file(s) | 93 | 2 | killed |
| `u176.C9_stat_not_ready` | `src/cratekit/acquire/bandcamp.py` | user | 1 file(s) | 47 | 1 | killed |
| `u269.M3_only_import_hidden_from_the_tree` | `src/cratekit/acquire/bandcamp.py` | maintainer | 1 file(s) | 18 | 1 | killed |
| `u176.V10_same_bytes_staged` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V11_marked_by_file` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V12_strict_refuses_lossy` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V13_number_after_prefix` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V1_auth_failed_reason` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 1043 | 5 | killed |
| `u176.V2_hidden` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V3_seller_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 13 | killed |
| `u176.V4_record_planned_fetched` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u176.V5_suppressed_is_held` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V6_music_folder_present` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u176.V7_record_version` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V8_recorded_item_done` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 1 | killed |
| `u176.V9_collision_refused` | `src/cratekit/acquire/bandcamp_cli.py` | user | 1 file(s) | 46 | 2 | killed |
| `u177.B10_land_command` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 3 | killed |
| `u177.B1_seller_by_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 5 | killed |
| `u177.B2_plan_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 12 | killed |
| `u177.B3_unregistered_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `u177.B4_labels_of_filter` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u177.B5_registry_unread_empty` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 2 | killed |
| `u177.B6_frozen_label` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 8 | killed |
| `u177.B7_tag_not_written` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 4 | killed |
| `u177.B8_write_false_ignored` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u177.B9_untagged_refusal` | `src/cratekit/acquire/bandcamp_cli.py` | user | 2 file(s) | 67 | 1 | killed |
| `u205.C10_country_not_sent` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C11_collection_404_read_as_absence` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C1_park_wrapped_as_outage` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 2 | killed |
| `u205.C2_token_never_reused` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 6 | killed |
| `u205.C3_no_expiry_margin` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 3 | killed |
| `u205.C4_rejected_token_kept` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 2 | killed |
| `u205.C5_server_error_read_as_absence` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C6_message_spells_404` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 2 | killed |
| `u205.C7_transport_text_in_message` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C8_availability_ignored` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u205.C9_names_not_included` | `src/cratekit/acquire/catalogue_api.py` | user | 1 file(s) | 66 | 1 | killed |
| `u207.C1_no_isrc_track_skipped` | `src/cratekit/acquire/catalogue_api.py` | user | 2 file(s) | 98 | 2 | killed |
| `u207.C2_code_not_asked_accepted` | `src/cratekit/acquire/catalogue_api.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.C3_paged_answer_accepted` | `src/cratekit/acquire/catalogue_api.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.C4_non_resource_skipped` | `src/cratekit/acquire/catalogue_api.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.C5_batch_ceiling_raised` | `src/cratekit/acquire/catalogue_api.py` | user | 2 file(s) | 98 | 4 | killed |
| `u207.C6_batch_shape_unchecked` | `src/cratekit/acquire/catalogue_api.py` | user | 2 file(s) | 98 | 1 | killed |
| `r1115.M1_failed_needs_a_failure` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 1 | killed |
| `r1115.M2_every_failure_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 5 | killed |
| `r1115.M3_nothing_left_to_run` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 1 | killed |
| `r1115.M4_retryable_is_not_for_good` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 4 | killed |
| `r1115.M5_declined_is_refused` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 8 | killed |
| `r1115.M6_landed_needs_a_track` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 3 | killed |
| `r1115.M7_done_counts_done` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 8 | killed |
| `r1115.M8_failed_names_the_failures` | `src/cratekit/acquire/cli.py` | user | 5 file(s) | 368 | 2 | killed |
| `r289-b.B1_reclaim_rmtree` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.B3_terminal_filter_gone` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.B4_unknown_job_read_as_terminal` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 1 | killed |
| `r289-b.B5_job_directory_before_its_items` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.B6_job_directory_never_reclaimed` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 2 | killed |
| `r289-b.C1_download_call_site` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 398 | 1 | killed |
| `r289-c.B2r_reclaim_reports_a_failure_as_a_removal` | `src/cratekit/acquire/cli.py` | maintainer | 6 file(s) | 398 | 1 | killed |
| `r289-c.B9r_children_unreadable_raises` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 22933 | 0 (promoted) | zero |
| `r290-author.S02_acquire_download_call_removed` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 195 | 11 | killed |
| `r668-a.M11_no_frozen_list_skip` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 22933 | 0 (promoted) | zero |
| `r668-a.M1_list_required_again` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 39 | killed |
| `r668-a.M2_resume_argv_carries_the_list` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `r668-a.M3_no_empty_job_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-a.M4_no_missing_list_guard` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `r668-a.M6_no_list_check_on_resume` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `r668-a.M9_other_verbs_job_read` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-b.M12_home_expansion_raises` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r668-b.M8_named_not_absolutised` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u108-c.G25_drive_maps_ending` | `src/cratekit/acquire/cli.py` | user | 7 file(s) | 508 | 31 | killed |
| `u169.A1_retryable_policy_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u169.A2_any_permanent_declined` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 7 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `u169.A4_no_declined_warning` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 4 | killed |
| `u169.A5_warning_names_failed_items` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 1 | killed |
| `u274.C1_worker_names_no_drive` | `src/cratekit/acquire/cli.py` | user | 6 file(s) | 449 | 17 | killed |
| `u42-author-round-2.C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C1_undecided_derived` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C3_strict_consults_the_marker` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C4_marked_lossless_dropped` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C5_empty_marker_matches_everything` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P1_unresolved_from_the_page` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P2_relative_path_leaks_the_root` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 24 | 5 | killed |
| `u42-author.W1_onerror_hook` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u42-author.W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 22933 | 2 (promoted) | killed |
| `u42-author.W3_onerror_silent` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u54-acquisition-worker.G10_absent_result` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G11_not_acquired` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 8 | killed |
| `u54-acquisition-worker.G12_landing_check` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-acquisition-worker.G14_marker_applied` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G15_no_marker_text` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G17_paced_sleep_bound` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `u54-acquisition-worker.G19_frozen_config` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 40 | killed |
| `u54-acquisition-worker.G1_origin_refusal` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G20_output_exists` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G27_remedy_absent_stays_absent` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G28_marker_decided_by_the_file` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G29_auth_failure_parks` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G2_missing_identifier` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G8_park_on_block` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G9_failed_invocation` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-zero-row-remeasured.G7_staging_cleared` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r703-a.D1_pool_reads_text` | `src/cratekit/acquire/download.py` | user | 5 file(s) | 445 | 3 | killed |
| `u80-b.F9_coverage_weight` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F10_no_url_dedupe` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F11_tie_ignores_platform` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F12_open_searched_again` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.F13_rejected_searched_again` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F14_single_option_stalls` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F15_empty_offered` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 4 | killed |
| `u80.F1_one_platform` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 7 | killed |
| `u80.F2_order_reversed` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 2 | killed |
| `u80.F4_timeout_is_empty` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F5_api_url_kept` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F6_ignore_errors_back` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F7_mix_boundary` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.F8_mix_not_demoted` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 37 | 1 | killed |
| `u81-fetch-b.L1_two_files_first_wins` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.L2_any_suffix` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Y1_no_option_terminator` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Y2_metadata_kept_on_convert` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Y3_failed_exit_is_a_file` | `src/cratekit/acquire/fallback.py` | user | 1 file(s) | 35 | 1 | killed |
| `r289-b.C2_fallback_resume_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `r289-b.C3_fallback_queue_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `r679-b.D2_fallback_gate_on_question_alone` | `src/cratekit/acquire/fallback_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `u80-b.C4_searcher_eager` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.C3_dedupe_on_match_id` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u80.C7_offered_not_named` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 3 | killed |
| `u80.C8_outage_narrowed` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u81-fetch-a.W10_untaggable_committed` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W12_download_failure_not_retryable` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W1_strict_not_refused` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W3_host_half` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W5_pre_download_exists` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W6_post_landing_exists` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W7_final_unmarked` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 4 | killed |
| `u81-fetch-a.W8_upload_tags_kept` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-a.W9_row_tags_not_written` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `u81-fetch-b.Q1_provider_route_fetched_lossy` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `u81-fetch-b.Q3_empty_queue` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 4 | killed |
| `u81-fetch-b.Q5_owned_row_fetched` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 3 | killed |
| `u81-fetch-b.W2_scheme_half_rerun` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 2 | killed |
| `u81-fetch-b.W4_empty_stem_rerun` | `src/cratekit/acquire/fallback_cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r1313.I1_cache_failure_alone` | `src/cratekit/acquire/isrc_cache.py` | user | 4 file(s) | 401 | 5 | killed |
| `r1313.I2_cache_keeps_any_status` | `src/cratekit/acquire/isrc_cache.py` | user | 4 file(s) | 401 | 3 | killed |
| `u206-b.M10b_day_coefficient_halved` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u206-b.M2b_disabled_recall_composite` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 8 | killed |
| `u206.M11_unreadable_answer_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 4 | killed |
| `u206.M12_corrupt_file_not_set_aside` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u206.M13_write_without_merge` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 5 | killed |
| `u206.M16_said_not_found_widened` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 3 | killed |
| `u206.M1_recall_never_hits` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 19 | killed |
| `u206.M21_override_ignored` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M3_disabled_still_remembers` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M4_unfolded_spelling_kept` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M5_country_ignored` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 5 | killed |
| `u206.M6_not_found_lives_as_found` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M7_not_found_ignores_shorter_setting` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u206.M8_expiry_off_by_one` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 5 | killed |
| `u206.M9_future_stamp_trusted` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1135 | 1 | killed |
| `u207.S1_any_client_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.S2_lone_code_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.S3_unfolded_spelling_screened` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 1 | killed |
| `u207.S4_rate_limit_keeps_screening` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 2 | killed |
| `u207.S5_refused_form_keeps_screening` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 3 | killed |
| `u207.S6_failed_batch_read_as_empty` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 8 | killed |
| `u207.S7_failed_batch_sent_again` | `src/cratekit/acquire/isrc_screen.py` | user | 2 file(s) | 98 | 2 | killed |
| `u68.D1_unlisted_on_blank_ref` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `u68.D2_first_id_wins` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u68.D3_ref_stripped` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u68.D4_reader_check` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `u68.F1_different_file_refused` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `u68.M1_manifest_version` | `src/cratekit/acquire/listdoc.py` | maintainer | 1 file(s) | 61 | 2 | killed |
| `u68.N1_slash` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.N2_surrounding_space` | `src/cratekit/acquire/listdoc.py` | maintainer | 1 file(s) | 61 | 1 | killed |
| `u68.N3_dot_names` | `src/cratekit/acquire/listdoc.py` | maintainer | 1 file(s) | 61 | 2 | killed |
| `u68.P1_missing_provenance` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.P2_blank_source` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.T1_version_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 6 | killed |
| `u68.T2_isrc_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 4 | killed |
| `u68.T3_key_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.W1_other_service_unlisted` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u68.W2_raw_title_candidate` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u73-b.C1_refs_only_when_several` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 1 | killed |
| `u73-b.C2_refs_written` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 2 | killed |
| `u77-c.C1_manifest_version` | `src/cratekit/acquire/listdoc.py` | user | 6 file(s) | 285 | 2 | killed |
| `u77-c.C2_manifest_version_bool` | `src/cratekit/acquire/listdoc.py` | maintainer | 6 file(s) | 285 | 1 | killed |
| `u77-c.C3_not_a_manifest` | `src/cratekit/acquire/listdoc.py` | user | 6 file(s) | 285 | 3 | killed |
| `u77-c.C4_year_bool` | `src/cratekit/acquire/listdoc.py` | maintainer | 6 file(s) | 285 | 1 | killed |
| `u77-c.C5_source_refs_kept` | `src/cratekit/acquire/listdoc.py` | maintainer | 6 file(s) | 285 | 1 | killed |
| `u78-c.C1_readback_identity` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 149 | 4 | killed |
| `u78-c.C2_readback_count` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 149 | 1 | killed |
| `u78-c.C3_dedupe_lines` | `src/cratekit/acquire/listdoc.py` | maintainer | 3 file(s) | 149 | 1 | killed |
| `u78-c.C4_reason_one_row` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 149 | 1 | killed |
| `u78-c.C5_unlisted_checked_first` | `src/cratekit/acquire/listdoc.py` | user | 3 file(s) | 149 | 5 | killed |
| `u78-c.E2_emitter_checks_rows` | `src/cratekit/acquire/listdoc.py` | user | 1 file(s) | 61 | 3 | killed |
| `r1016.M10_wrong_endpoint` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 6 | killed |
| `r1016.M1_account_walk_back_on_the_clients_method` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 14 | killed |
| `r1016.M2_account_parse_through_the_factory` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 12 | killed |
| `r1016.M3_folder_parse_through_the_factory` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 3 | killed |
| `r1016.M4_date_added_not_moved` | `src/cratekit/acquire/listing.py` | maintainer | 7 file(s) | 832 | 1 | killed |
| `r1016.M5_not_a_page_check_dropped` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 3 | killed |
| `r1016.M7_send_translation_dropped` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 2 | killed |
| `r1016.M8_walk_name_ignored` | `src/cratekit/acquire/listing.py` | maintainer | 7 file(s) | 832 | 1 | killed |
| `r1016.M9_offset_not_sent` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 10 | killed |
| `r1016.S1_account_dedup_dropped` | `src/cratekit/acquire/listing.py` | user | 7 file(s) | 832 | 1 | killed |
| `r1360.J1_prefix_agrees` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 5 | killed |
| `r1360.J2_prefix_equal_only` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 1 | killed |
| `r1360.J3_prefix_always_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 4 | killed |
| `r1360.J4_prefix_uncounted_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 2 | killed |
| `r1360.W10_walk_past_count` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 1 | killed |
| `r1360.W11_offset_dropped` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 19 | killed |
| `r1360.W12_tag_unread` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 13 | killed |
| `r1360.W13_declared_unread` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 24 | killed |
| `r1360.W14_cap_of_one_walked` | `src/cratekit/acquire/listing.py` | maintainer | 15 file(s) | 826 | 1 | killed |
| `r1360.W15_short_page_walked_past` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 1 | killed |
| `r1360.W1_no_walk` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 24 | killed |
| `r1360.W2_walk_no_overlap` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 19 | killed |
| `r1360.W3_no_start_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 1 | killed |
| `r1360.W4_no_tag_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 4 | killed |
| `r1360.W5_no_length_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 1 | killed |
| `r1360.W6_no_empty_check` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 1 | killed |
| `r1360.W7_full_page_ends` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 10 | killed |
| `r1360.W8_overlap_kept` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 826 | 25 | killed |
| `r261.L1_skip_record` | `src/cratekit/acquire/listing.py` | user | 4 file(s) | 522 | 4 | killed |
| `r504-a.A5_listing_no_count` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 659 | 4 | killed |
| `r504-a.A6_listing_unrecorded` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 659 | 4 | killed |
| `r504-a.A7_listing_nonpositive` | `src/cratekit/acquire/listing.py` | maintainer | 5 file(s) | 659 | 2 | killed |
| `r878-a.A10_non_page_refused` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 4 | killed |
| `r878-a.A11_count_alone_is_a_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-a.A12_parse_retried` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-a.A13_dedupe_shared` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 4 | killed |
| `r878-a.A1_paginate_refuses_cursor` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `r878-a.A2_cursor_refuses_offset_rule` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `r878-a.A3_budget_off_by_one` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-a.A6_latest_count_wins` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-a.A7_empty_page_ends` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 1 | killed |
| `r878-a.A8_no_cursor_ends` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 16 | killed |
| `r878-a.A9_cursor_advances` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 14 | killed |
| `r878-b.B10_folder_dedupe_key` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 2 | killed |
| `r878-b.B11_folder_rule_in_table` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 142 | 20 | killed |
| `r878-b.B2_client_part_refusal` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 2 | killed |
| `r878-b.B6_order_by_name` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `r878-b.B7_no_offset_sent` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 2 | killed |
| `r878-b.B8_first_request_no_cursor` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 142 | 1 | killed |
| `r887-a.K2_playlists_kept_unfiltered` | `src/cratekit/acquire/listing.py` | user | 3 file(s) | 198 | 1 | killed |
| `r887-a.K3_count_kept_not_served` | `src/cratekit/acquire/listing.py` | user | 3 file(s) | 198 | 3 | killed |
| `r887-a.K5_filter_before_count` | `src/cratekit/acquire/listing.py` | user | 3 file(s) | 198 | 3 | killed |
| `r888.H1_held_is_paged` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 11 | killed |
| `r888.H2_held_not_deduplicated` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 1 | killed |
| `r888.H3_unheld_listing_not_recorded` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 1 | killed |
| `r888.H4_provider_budget_halved` | `src/cratekit/acquire/listing.py` | user | 5 file(s) | 578 | 1 | killed |
| `r888.H5_abstract_held` | `src/cratekit/acquire/listing.py` | maintainer | 5 file(s) | 578 | 1 | killed |
| `u226.M1_equal_not_agreed` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 783 | 78 | killed |
| `u226.M4_prefix_as_subset` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 783 | 3 | killed |
| `u252.L1_ladder_exponent` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L2_ladder_rungs` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L3_ladder_ceiling_off_by_one` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L4_ladder_cap` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L5_ladder_base` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u252.L6_no_ladder` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 46 | 3 | killed |
| `u65.A2_max_pages_gets_a_default` | `src/cratekit/acquire/listing.py` | maintainer | 2 file(s) | 197 | 1 | killed |
| `u65.B1_favourites_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 9 | killed |
| `u65.B2_favourites_back_to_the_empty_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 5 | killed |
| `u65.B3_playlist_tracks_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 6 | killed |
| `u65.B4_account_playlists_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 5 | killed |
| `u65.B5_artist_releases_back_to_the_short_page` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 266 | 3 | killed |
| `u65.C1_the_declared_total_is_ignored` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 3 | killed |
| `u65.C2_an_empty_page_ends_a_declared_total_walk` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 1 | killed |
| `u65.C3_a_full_page_at_the_declared_end_stops_anyway` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 1 | killed |
| `u65.C4_the_short_page_rule_stops_every_walk` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 13 | killed |
| `u65.C6_offset_advances_by_what_was_served` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 10 | killed |
| `u65.C7_a_zero_total_is_trusted_as_an_end` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 1 | killed |
| `u65.D5_the_favourites_budget_is_tightened_onto_real_data` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 86 | 2 | killed |
| `u65.E1_the_shape_helper_ignores_the_rule_table` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 28 | killed |
| `u65.E2_the_shape_helper_ignores_the_page_size_table` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 5 | killed |
| `u65.E3_the_favourites_total_is_never_wired` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 4 | killed |
| `u65.E4_the_playlist_total_is_never_wired` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 1 | killed |
| `u65.F1_an_unpageable_listing_takes_its_single_page` | `src/cratekit/acquire/listing.py` | user | 1 file(s) | 86 | 2 | killed |
| `u65.F3_the_retry_ceiling_is_raised` | `src/cratekit/acquire/listing.py` | maintainer | 1 file(s) | 86 | 11 | killed |
| `u65.F4_the_favourites_dedup_goes` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 197 | 1 | killed |
| `u70.E3_hearts_declared_total` | `src/cratekit/acquire/listing.py` | user | 2 file(s) | 260 | 4 | killed |
| `r1705.M10_holds_always` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1705.M11_holds_reads_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 38 | killed |
| `r1705.M12_lookup_ignores_wanted_side` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 28 | killed |
| `r1705.M13_lookup_ignores_held_side` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 25 | killed |
| `r1705.M14_lookup_key_drops_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `r1705.M15_lookup_key_spells_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 1 | killed |
| `r1705.M16_lookup_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 38 | killed |
| `r1705.M17_lookup_repeats_the_five` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1705.M18_lookup_skips_every_scored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1705.M19_lookup_after_the_scored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `r1705.M1_luv_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 15 | killed |
| `r1705.M20_lookup_counts_in_the_five` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 38 | killed |
| `r1705.M2_four_numeral_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 14 | killed |
| `r1705.M3_too_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `r1705.M4_2nite_unlisted` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 2 | killed |
| `r1705.M5_spelled_test_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 5 | killed |
| `r1705.M6_spelled_test_a_ratio` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 12 | killed |
| `r1705.M7_spelled_replaces_written` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 2 | killed |
| `r1705.M8_spelled_keeps_spaces` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 7 | killed |
| `r1705.M9_spelled_spells_nothing` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 52 | killed |
| `r1705.S1_discovery_floor_raised` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 28 | killed |
| `r1705.S2_unreadable_title_dropped` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 15 | killed |
| `r1709.M10_title_identity_no_separator` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M11_recording_identity_is_the_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 24 | killed |
| `r1709.M12_held_exact_unfiltered` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 14 | killed |
| `r1709.M13_held_credited_by_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 9 | killed |
| `r1709.M14_isrc_settled_by_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M15_same_recording_title_guard` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M16_candidates_grouped_by_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 5 | killed |
| `r1709.M17_question_identity_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M18_match_id_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M19_search_option_token` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M1_bare_no_nfkc` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M20_current_option_no_title` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M21_current_option_never_carries` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M3_bare_keeps_spaces` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M4_bare_keeps_invisible` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 5 | killed |
| `r1709.M5_no_variation_selectors` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 3 | killed |
| `r1709.M6_no_format_characters` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 2 | killed |
| `r1709.M7_tag_characters_dropped` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M8_bare_for_every_title` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M9_title_identity_is_the_fold` | `src/cratekit/acquire/match.py` | user | 29 file(s) | 3983 | 30 | killed |
| `r431-b.B1_a_wanted_built_by_hand_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r431-b.B2_a_row_billing_a_guest_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r431-b.B3_a_listing_that_spelled_a_credit_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 7 | killed |
| `r431-b.B4_the_engine_never_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 7 | killed |
| `r431-b.B5_the_engine_ignores_companions_false` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 1 | killed |
| `r431-b.B7_the_engine_asks_under_the_tombstones_kind` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 8 | killed |
| `r431-b.B8_the_reader_never_counts_the_artists` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r664.E1_stem_head_kept` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 149 | killed |
| `r664.E2_pair_rule_field_by_field` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 1 | killed |
| `r664.E4_title_not_split` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 120 | killed |
| `r664.G5_key_not_read_from_the_tag_head` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 2 | killed |
| `r664.G6_tag_head_outranks_stem_head` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1298 | 1 | killed |
| `r667-b.B1_same_recording_no_isrc` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667-b.B2_reader_isrc_unfolded` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 2 | killed |
| `r667.E1_title_head_kept` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 33 | killed |
| `r667.E2_first_copy_only` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 2 | killed |
| `r667.F1_credited_reason_is_exact` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 3 | killed |
| `r667.F2_isrc_version_not_settled` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.F3_doubtful_not_offered` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 3 | killed |
| `r667.F4_text_copy_joins_isrc_paths` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.G12_same_recording_no_credit` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.G13_isrc_not_consulted` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 16 | killed |
| `r667.G15_isrc_hit_skips_key` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 3 | killed |
| `r667.G16_isrc_reason_is_exact` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 11 | killed |
| `r667.G17_reader_drops_isrc` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 17 | killed |
| `r667.G3_members_not_split` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 6 | killed |
| `r667.G4_members_not_folded` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 5 | killed |
| `r667.G5_empty_isrc_asks` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 1 | killed |
| `r667.G8_no_credited_rule` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 729 | 6 | killed |
| `r679-b.C1_credited_rule_not_owning` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 879 | 2 | killed |
| `r679-b.C2_reading_shape_missing` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 879 | 1 | killed |
| `u16-round-8-independent-composites.V24_approximate_limit_raised` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 10 | killed |
| `u16-round-8-independent.V11_candidate_order_sorted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 3 | killed |
| `u16-round-8-independent.V12_approximate_floor_halved` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 13 | killed |
| `u16-round-8-independent.V13_withheld_not_reported` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 4 | killed |
| `u16-round-8-independent.V14_tombstone_fold_nfd` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 4 | killed |
| `u16-round-8-independent.V15_empty_identity_accepted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 1 | killed |
| `u16-round-8-independent.V16_key_leaves_item_identity` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 3 | killed |
| `u16-round-8-independent.V18_rejection_skips_tombstones` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V19_unbound_yes_takes_todays_candidate` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V1_key_check_first_copy_only` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 2 | killed |
| `u16-round-8-independent.V20_digest_width_halved` | `src/cratekit/acquire/match.py` | maintainer | 1 file(s) | 609 | 3 | killed |
| `u16-round-8-independent.V21_suppression_asked_one_spelling` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 9 | killed |
| `u16-round-8-independent.V3_version_differs_silently_joins` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 41 | killed |
| `u16-round-8-independent.V5_ambiguous_reading_promoted` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 28 | killed |
| `u16-round-8-independent.V6_reading_question_never_asked` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 28 | killed |
| `u16-round-8-independent.V7_tombstoned_counted_missing` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 28 | killed |
| `u16-round-8-independent.V8_missing_without_options` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 9 | killed |
| `u16-round-8-independent.V9_relative_key_by_letter` | `src/cratekit/acquire/match.py` | user | 1 file(s) | 609 | 11 | killed |
| `u213.M1_first_group_is_the_title` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 13 | killed |
| `u213.M21_first_group_version_check` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 778 | 6 | killed |
| `u213.M22_names_a_version_last_word` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 778 | 2 | killed |
| `u213.M3_first_group_position` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 16 | killed |
| `u213.M4_first_group_keeps_brackets` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 15 | killed |
| `u213.M5_listed_names_artist` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 3 | killed |
| `u249.M01_path_alone` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 7 | killed |
| `u249.M02_size_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 2 | killed |
| `u249.M03_mtime_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M04_ctime_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M05_inode_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M06_device_out_of_stamp` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M07_size_not_stat` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 2 | killed |
| `u249.M08_template_out_of_key` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M09_no_window` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 4 | killed |
| `u249.M10_window_halved` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 3 | killed |
| `u249.M11_window_boundary` | `src/cratekit/acquire/match.py` | maintainer | 4 file(s) | 817 | 1 | killed |
| `u249.M12_moment_after_read` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u249.M13_failed_read_remembered` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 3 | killed |
| `u249.M14_unstated_remembered_never` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 11 | killed |
| `u249.M20_reset_forgets_nothing` | `src/cratekit/acquire/match.py` | maintainer | 4 file(s) | 817 | 6 | killed |
| `u249.M20a_failed_read_keeps_old_entry` | `src/cratekit/acquire/match.py` | user | 4 file(s) | 817 | 1 | killed |
| `u262.C1_letters_rule_back` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 15 | killed |
| `u262.C2_any_word` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 1 | killed |
| `u262.C3_last_word` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 32 | killed |
| `u262.C4_unfolded_words` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 26 | killed |
| `u262.C5_no_with` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 7 | killed |
| `u262.C6_no_ft` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 9 | killed |
| `u262.C7_no_featuring` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 4 | killed |
| `u262.C8_no_feat` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 681 | 19 | killed |
| `u265.M10_empty_index_scored` | `src/cratekit/acquire/match.py` | maintainer | 24 file(s) | 2835 | 1 | killed |
| `u265.M1_narrow_split_everywhere` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 2 | killed |
| `u265.M2_python_split_everywhere` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 2 | killed |
| `u265.M2b_width_off_by_one` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 1 | killed |
| `u265.M3_words_not_sorted` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 18 | killed |
| `u265.M4_query_not_sorted` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 42 | killed |
| `u265.M5_hit_named_by_its_sorted_form` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 61 | killed |
| `u265.M6_cache_misaligned` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 15 | killed |
| `u265.M7_cache_never_kept` | `src/cratekit/acquire/match.py` | maintainer | 24 file(s) | 2835 | 1 | killed |
| `u265.M8_other_scorer` | `src/cratekit/acquire/match.py` | user | 24 file(s) | 2835 | 39 | killed |
| `u269.M7_match_engine_binds_lxml` | `src/cratekit/acquire/match.py` | maintainer | 1 file(s) | 609 | 2 | killed |
| `u286.M10_swap_either_half` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `u286.M11_swap_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 8 | killed |
| `u286.M12_swap_second_half_artist` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 8 | killed |
| `u286.M13_filter_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 20 | killed |
| `u286.M14_filter_after_cap` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `u286.M15_cap_removed` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `u286.M16_cap_off_by_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `u286.M17_cap_counts_files` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `u286.M18_resolver_back_to_base` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 51 | killed |
| `u286.M19_limit_ignored` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 9 | killed |
| `u286.M1_title_floor_up_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `u286.M2_title_floor_down_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 1 | killed |
| `u286.M3_title_floor_to_sixty` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 3 | killed |
| `u286.M4_plain_ratio` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 6 | killed |
| `u286.M6_unreadable_title_not_asked` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 15 | killed |
| `u286.S1_discovery_floor_up_one` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 10 | killed |
| `u286.S2_offer_not_truncated` | `src/cratekit/acquire/match.py` | user | 27 file(s) | 3906 | 4 | killed |
| `r1709.M22_adjudicate_not_carried` | `src/cratekit/acquire/match_cli.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r1709.M2_adjudicate_offered_not_carried` | `src/cratekit/acquire/match_cli.py` | user | 29 file(s) | 3983 | 1 | killed |
| `r431-b.B6_the_verb_calls_a_companion_stale` | `src/cratekit/acquire/match_cli.py` | user | 7 file(s) | 1005 | 1 | killed |
| `r679-b.B1_no_retirement` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 7 | killed |
| `r679-b.B2_any_matched_row_is_owned_by_a_rule` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.B3_no_reopen` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r679-b.B5_rule_not_recorded` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 5 | killed |
| `r679-b.B6_one_shape_only` | `src/cratekit/acquire/match_cli.py` | user | 3 file(s) | 879 | 7 | killed |
| `u16-round-8-independent.V22_suppressed_warning_omitted` | `src/cratekit/acquire/match_cli.py` | user | 1 file(s) | 609 | 26 | killed |
| `r1305.L1_login_name_on_any_link` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 1 | killed |
| `r1305.L2_login_status_declared_only` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 5 | killed |
| `r1305.L3_login_name_dropped` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 207 | 1 | killed |
| `r1694.L1_login_no_tolerance` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 7 | killed |
| `r1694.L2_token_file_uncaught` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 1 | killed |
| `r1694.L3_token_file_catches_defect` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 1 | killed |
| `r1694.L4_rewrite_unchanged` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 2 | killed |
| `r1694.L5_hold_the_refresh` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 2 | killed |
| `r1694.L6_no_note` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 8 | killed |
| `r1694.L7_note_the_words` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 164 | 7 | killed |
| `r1694.S1_tolerance_reraises` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 7 | killed |
| `r1694.S2_tolerance_always` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 3 | killed |
| `r1694.S3_catch_everything` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 1 | killed |
| `r1694.S4_failures_no_credential` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 8 | killed |
| `r1694.S5_failures_no_cratekit` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 2 | killed |
| `r1694.S6_failures_no_oserror` | `src/cratekit/acquire/provider_session.py` | user | 4 file(s) | 208 | 1 | killed |
| `r705-b.S2_client_session_never_attaches` | `src/cratekit/acquire/provider_session.py` | user | 1 file(s) | 117 | 16 | killed |
| `u205.O2_no_country_still_opens` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 351 | 1 | killed |
| `u205.O3_unreadable_values_read_as_absent` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 351 | 1 | killed |
| `u205.O4_app_attached_as_account` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 351 | 6 | killed |
| `u261.H1_reuse_skips_the_gate` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 213 | 1 | killed |
| `u261.H2_reuse_ignores_a_replaced_session` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 4 | killed |
| `u261.H3_reuse_swallows_a_missing_session` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 141 | 2 | killed |
| `u261.H4_failed_read_keeps_the_hold` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 141 | 1 | killed |
| `u261.H5_settings_not_in_the_key` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 147 | 1 | killed |
| `u261.H6_app_not_asked_again` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 96 | 3 | killed |
| `u261.H7_nothing_held` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 12 | killed |
| `u261.H8_blob_is_the_stored_not_the_refresh` | `src/cratekit/acquire/provider_session.py` | maintainer | 1 file(s) | 30 | 1 | killed |
| `u261.H9_no_forget_before_a_new_login` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 141 | 1 | killed |
| `u261.R1_watch_not_installed` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 3 | killed |
| `u261.R2_answered_refusal_ignored` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 207 | 2 | killed |
| `u261.R3_raised_refusal_ignored` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 141 | 1 | killed |
| `u261.R4_forbidden_not_a_refusal` | `src/cratekit/acquire/provider_session.py` | user | 3 file(s) | 174 | 4 | killed |
| `u261.R5_drop_not_by_identity` | `src/cratekit/acquire/provider_session.py` | maintainer | 1 file(s) | 30 | 2 | killed |
| `u261.W1_unchanged_skip_removed` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 481 | 5 | killed |
| `u261.W2_changed_session_skipped` | `src/cratekit/acquire/provider_session.py` | user | 5 file(s) | 481 | 5 | killed |
| `u261.W3_compare_by_value_not_bytes` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 187 | 1 | killed |
| `u261.W5_session_fields_guard_sample` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 187 | 1 | killed |
| `u274.P1_gone_never` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P2_gone_overflow` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P3_gone_permission` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 2 | killed |
| `u274.P4_sweep_live` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 6 | killed |
| `u274.P5_sweep_not_dir` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 2 | killed |
| `u274.P6_sweep_other_account` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P7_no_sweep` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.P8_captured_always` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 3 | killed |
| `u274.P9_captured_nothing` | `src/cratekit/acquire/provider_session.py` | user | 6 file(s) | 449 | 6 | killed |
| `u62.S1_device_flow_login` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S2_401_not_rejected` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 2 | killed |
| `u62.S4_every_failure_rejected` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 4 | killed |
| `u62.S5_blob_without_token_logged_in` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S6_refresh_not_written_back` | `src/cratekit/acquire/provider_session.py` | user | 2 file(s) | 331 | 1 | killed |
| `u62.S7_naive_expiry_as_local` | `src/cratekit/acquire/provider_session.py` | maintainer | 2 file(s) | 22933 | 0 (promoted) | zero |
| `r1694.V1_drive_failures_narrowed` | `src/cratekit/acquire/vendored.py` | user | 3 file(s) | 130 | 2 | killed |
| `r703-a.LF1_plain_runtime_error` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r703-a.LF2_cause_not_worded` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 4 | killed |
| `r703-a.V1_no_observed_session` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 4 | killed |
| `r703-a.V2_no_forget` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 2 | killed |
| `r703-a.V3_cause_not_passed` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 4 | killed |
| `r703-a.V4_no_escalation` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 2 | killed |
| `r703-a.V5_escalate_when_ok` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r703-a.V6_sample_no_park_check` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 2 | killed |
| `r703-b.L1_no_active_exception` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 3 | killed |
| `r703-b.L4_error_notes_nothing` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 2 | killed |
| `r703-b.O1_proxy_notes_nothing` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 5 | killed |
| `r703-b.O3_writes_land_on_proxy` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r703-b.O4_wraps_twice` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 274 | 1 | killed |
| `r703-b.R1_status_path_dropped` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r703-b.R2_everything_is_the_provider` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r703-b.R3_mapping_positional` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 274 | 1 | killed |
| `r703-c.C1_last_exception_wins` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r703-c.C2_message_outranks_exception` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 274 | 1 | killed |
| `r705-b.S3_vendored_never_asks_before_login` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-b.S4_vendored_never_attaches_to_the_tool` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 117 | 1 | killed |
| `r705-b.S5_vendored_never_asks_after_login` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 117 | 1 | killed |
| `r83.D8_vendored_defect_first` | `src/cratekit/acquire/vendored.py` | user | 1 file(s) | 157 | 2 | killed |
| `u197.M5_adapter_name` | `src/cratekit/acquire/vendored.py` | user | 3 file(s) | 643 | 11 | killed |
| `u274.V11_defect_swallowed` | `src/cratekit/acquire/vendored.py` | maintainer | 6 file(s) | 449 | 1 | killed |
| `u274.V12_scope_per_invocation` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 16 | killed |
| `u274.V1_refusal_forgotten` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 4 | killed |
| `u274.V2_login_refusal_unrecorded` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 2 | killed |
| `u274.V3_offer_refusal_unrecorded` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.V4_fetch_refusal_unrecorded` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.V5_source_per_track` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 14 | killed |
| `u274.V6_no_rebind` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.V8_atmos_stored` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 1 | killed |
| `u274.V9_no_capture` | `src/cratekit/acquire/vendored.py` | user | 6 file(s) | 449 | 7 | killed |
| `u47-author.CODEC_alac_reads_as_lossy` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.CODEC_mp3_reads_as_lossless` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.CODEC_no_refusal` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 4 | killed |
| `u47-author.CODEC_none_reads_as_unreadable` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 6 | killed |
| `u47-author.CODEC_policy_ignored` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.CODEC_refusal_drops_the_codec_name` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 2 | killed |
| `u47-author.CODEC_suffix_instead_of_container` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R195_drop_ffmpeg_key` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 4 | killed |
| `u47-author.R195_push_empty_instead` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 4 | killed |
| `u47-author.R195_verify_skips_the_mapping` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 3 | killed |
| `u47-author.R196_absent_marker_reads_as_pkce` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R196_accept_device_flow_session` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 3 | killed |
| `u47-author.R196_login_without_pkce` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R196_no_stored_session_proceeds` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R197_argument_set_shrinks` | `src/cratekit/acquire/vendored.py` | maintainer | 2 file(s) | 201 | 3 | killed |
| `u47-author.R197_drop_event_abort` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 6 | killed |
| `u47-author.R197_drop_event_run` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 3 | killed |
| `u47-author.R197_drop_progress` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 3 | killed |
| `u47-author.R197_drop_progress_overall` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 3 | killed |
| `u47-author.R197_event_abort_preset` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 5 | killed |
| `u47-author.R197_event_run_left_clear` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.R197_progress_enabled` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.SAMPLE_permanence_asked_second` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |
| `u47-author.SAMPLE_quality_equality` | `src/cratekit/acquire/vendored.py` | user | 2 file(s) | 201 | 1 | killed |

## Zero rows and what they owe

- `r289-c.B9r_children_unreadable_raises` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r668-a.M11_no_frozen_list_skip` (maintainer facing): maintainer facing, composite not required
- `u42-author.W1_onerror_hook` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u42-author.W3_onerror_silent` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u62.S7_naive_expiry_as_local` (maintainer facing): maintainer facing, composite not required

## Row definitions

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

### `r1313.A1_classifier_failure_alone`

classify_unavailable: read the 404 off the failure alone, as before R-1313, so a track answered with a 404 page is retried for ever

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A1_classifier_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 368 against a baseline of 368
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[classify_unavailable]`
  - `tests/test_provider_not_found_bodies.py::test_a_track_the_provider_answers_with_a_404_page_is_permanent_with_no_retry`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if answered_not_found(exc):
        return TrackOutcome.UNAVAILABLE_PERMANENT
```

New text:

```
    if getattr(getattr(exc, "response", None), "status_code", None) == 404:
        return TrackOutcome.UNAVAILABLE_PERMANENT
```

### `r1313.A2_status_before_no_file_landed`

classify_unavailable: ask the nearest status before NoFileLanded, so a download whose swallowed cause was a 404 page quarantines a live track

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A2_status_before_no_file_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 368 against a baseline of 368
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

### `r1313.A3_classifier_name_on_any_link`

classify_unavailable: read a not found class name on any link the walk reaches, so a name met only as context is read as the provider's answer

- File: `src/cratekit/acquire/adapter.py`
- Source: `r1313.json`, row `A3_classifier_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_vendor_import.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
```

New text:

```
    from cratekit.core.cause import failure_links  # noqa: PLC0415

    if any("notfound" in type(one).__name__.lower() for one, _ in failure_links(exc)):
        return TrackOutcome.UNAVAILABLE_PERMANENT
    if answered_not_found(exc):
```

### `r703-a.A1_classifier_reads_text`

classify_unavailable no longer holds NoFileLanded transient by type

- File: `src/cratekit/acquire/adapter.py`
- Source: `r703-a.json`, row `A1_classifier_reads_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`, `tests/test_provider_gate.py`
- Collected: 872 against a baseline of 872
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

### `r705-b.S7_acquire_one_softens_the_park_at_the_lookup`

a park raised at the offer is one unavailable track and the driver claims the next

- File: `src/cratekit/acquire/adapter.py`
- Source: `r705-b.json`, row `S7_acquire_one_softens_the_park_at_the_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_acquire_one_lets_the_park_through_rather_than_failing_the_track[offer]`

Old text:

```
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken, Parked):

```

New text:

```
        offer = source.offer(request)
    except (AdapterAuthFailed, AdapterBroken):

```

### `r705-b.S8_acquire_one_softens_the_park_at_the_fetch`

a park raised at the fetch is one unavailable track and the driver claims the next

- File: `src/cratekit/acquire/adapter.py`
- Source: `r705-b.json`, row `S8_acquire_one_softens_the_park_at_the_fetch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_acquire_one_lets_the_park_through_rather_than_failing_the_track[fetch]`

Old text:

```
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken, Parked):

```

New text:

```
        path = source.fetch(request, settings.download_staging)
    except (AdapterAuthFailed, AdapterBroken):

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

### `r83.D3_drop_attribute_error`

R-348: AttributeError leaves the defect classes, the class the sitting found

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D3_drop_attribute_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
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

### `r83.D5_drop_name_error`

R-348: NameError, and with it UnboundLocalError, leaves the defect classes

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D5_drop_name_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
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

### `r83.D6_remedy`

R-348: the defect carries switch-adapter instead of report-defect

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D6_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
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

### `r83.D7_detail_names_class`

R-348: the detail no longer names the exception class

- File: `src/cratekit/acquire/adapter.py`
- Source: `r83.json`, row `D7_detail_names_class`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_doctor.py`, `tests/test_pacing.py`
- Collected: 755 against a baseline of 755
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
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`
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

### `u246.S2_adapter_per_element`

InvocationResult: build the requested set once per result again (the shape on main)

- File: `src/cratekit/acquire/adapter.py`
- Source: `u246.json`, row `S2_adapter_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_adapter_contract.py`
- Collected: 190 against a baseline of 190
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
            stray = [r.key for r in self.results if r.key not in asked]
```

New text:

```
            stray = [r.key for r in self.results if r.key not in set(self.requested)]
```

### `u47-author.CODEC_refused_track_sinks_the_run`

Escalate a lossy landing to an adapter failure, the shape that raises an uncaught ValueError when a delisted track landed earlier in the same batch

- File: `src/cratekit/acquire/adapter.py`
- Source: `u47-author.json`, row `CODEC_refused_track_sinks_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u176-c5.C5_empty_page_ends`

_pages: an empty page does not end the listing, so the listing walks past the end and refuses

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176-c5.json`, row `C5_empty_page_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
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

### `u176.C11_fetch_refuses_untrusted`

fetch: a link outside Bandcamp is requested with the session

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C11_fetch_refuses_untrusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`
- Collected: 47 against a baseline of 47
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

### `u176.C3_page_error_is_rejected`

_pages: a page answering with an error is not read as a refused session

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C3_page_error_is_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_bandcamp.py::test_a_page_answering_with_an_error_is_rejected`

Old text:

```
        if page.get("error"):
```

New text:

```
        if False:
```

### `u176.C4_page_without_items_list`

_pages: a page holding no list of items ends the listing, so an unreadable page reads as an account holding nothing older

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C4_page_without_items_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
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

### `u176.C6_repeated_token`

_pages: a token already seen is followed again, so a stuck listing asks up to the page cap before it refuses

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C6_repeated_token`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`
- Collected: 47 against a baseline of 47
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

### `u176.C8_member_base_name`

unpack: a member's path is kept rather than reduced to its base name, so an archive member reaches outside the holding folder

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u176.json`, row `C8_member_base_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp.py`, `tests/test_bandcamp_cli.py`
- Collected: 93 against a baseline of 93
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

### `u269.M3_only_import_hidden_from_the_tree`

acquire/bandcamp.py: the one import of curl_cffi becomes a computed name, so no import under src names it

- File: `src/cratekit/acquire/bandcamp.py`
- Source: `u269.json`, row `M3_only_import_hidden_from_the_tree`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_packaging.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_packaging.py::test_every_core_dependency_is_imported_by_the_package`

Old text:

```
        from curl_cffi import requests as curl_requests  # noqa: PLC0415 - the network seam

```

New text:

```
        curl_requests = __import__("".join(["curl", "_cffi.requests"])).requests

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

### `u176.V1_auth_failed_reason`

_auth_failed: a missing or refused session is credential-missing, a precondition, rather than auth-failed

- File: `src/cratekit/acquire/bandcamp_cli.py`
- Source: `u176.json`, row `V1_auth_failed_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_bandcamp_cli.py`, `tests/test_cli_contract.py`
- Collected: 1043 against a baseline of 1043
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_cli.py::test_a_listing_the_session_is_refused_at_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues`
  - `tests/test_bandcamp_cli.py::test_a_session_removed_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_an_expired_session_is_auth_failed_naming_the_login_step`
  - `tests/test_bandcamp_cli.py::test_no_recorded_session_is_auth_failed_before_any_request`

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
  - `tests/test_bandcamp_cli.py::test_a_library_unmounted_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_listing_bandcamp_cannot_answer_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_listing_the_session_is_refused_at_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_a_lossy_file_under_a_lossless_offer_is_marked_by_what_it_is`
  - `tests/test_bandcamp_cli.py::test_a_permissive_policy_takes_the_lossy_release_marked`
  - `tests/test_bandcamp_cli.py::test_a_purchase_already_recorded_is_done_when_its_item_runs_again`
  - `tests/test_bandcamp_cli.py::test_a_purchase_filtered_out_is_offered_on_the_next_run_without_the_filter`
  - `tests/test_bandcamp_cli.py::test_a_purchase_no_longer_downloadable_fails_permanently`
  - `tests/test_bandcamp_cli.py::test_a_seller_filter_plans_only_that_seller`
  - `tests/test_bandcamp_cli.py::test_a_seller_matching_nothing_is_warned_about`
  - `tests/test_bandcamp_cli.py::test_a_session_refused_in_the_worker_parks_the_job_and_a_resume_continues`
  - `tests/test_bandcamp_cli.py::test_a_session_removed_since_the_queue_parks_the_resumed_job`
  - `tests/test_bandcamp_cli.py::test_strict_refuses_a_release_offered_only_lossy`

Old text:

```
        if sellers and purchase.seller.casefold() not in sellers:
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
  - `tests/test_catalogue_app.py::test_a_lifetime_that_is_a_flag_is_not_read_as_one_second`
  - `tests/test_catalogue_app.py::test_a_rate_limit_on_the_app_trips_the_shared_gate_and_refuses_the_account_too`
  - `tests/test_catalogue_app.py::test_a_short_lived_token_keeps_half_its_life_rather_than_none[30]`
  - `tests/test_catalogue_app.py::test_a_short_lived_token_keeps_half_its_life_rather_than_none[60]`
  - `tests/test_catalogue_app.py::test_a_token_with_no_readable_lifetime_serves_one_margin_and_is_asked_again`
  - `tests/test_catalogue_app.py::test_the_token_is_fetched_once_and_reused_until_it_nears_expiry`

Old text:

```
        if self._token is not None and now < self._expires_at:
```

New text:

```
        if False:
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

### `u207.C1_no_isrc_track_skipped`

isrcs_held: a track with no readable ISRC is skipped rather than refusing the answer, so the code it answered is read as absent

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C1_no_isrc_track_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-isrc]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[unreadable-isrc]`

Old text:

```
            if not code:
                raise CatalogueUnavailable(
                    f"the catalogue API's answer to this {what} holds a track with no "
```

New text:

```
            if not code:
                continue
                raise CatalogueUnavailable(
                    f"the catalogue API's answer to this {what} holds a track with no "
```

### `u207.C2_code_not_asked_accepted`

isrcs_held: an answer naming a code nobody asked is accepted, so the code asked is read as absent

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C2_code_not_asked_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[a-code-not-asked]`

Old text:

```
        if not named <= set(asked):
```

New text:

```
        if False:
```

### `u207.C3_paged_answer_accepted`

isrcs_held: an answer with a next link is read whole, so a code on the page not read is absent

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C3_paged_answer_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[paged]`

Old text:

```
        if isinstance(links, Mapping) and _text(links.get("next")):
```

New text:

```
        if False:
```

### `u207.C4_non_resource_skipped`

isrcs_held: an entry that is not a resource is skipped rather than refusing the answer

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C4_non_resource_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[not-a-resource]`

Old text:

```
            if not isinstance(resource, Mapping):
                raise CatalogueUnavailable(
```

New text:

```
            if not isinstance(resource, Mapping):
                continue
                raise CatalogueUnavailable(
```

### `u207.C5_batch_ceiling_raised`

catalogue: the batch ceiling is fifty, past the API's documented twenty

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C5_batch_ceiling_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 4 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_failed_batch_does_not_stop_the_next_one`
  - `tests/test_isrc_screen.py::test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same`
  - `tests/test_isrc_screen.py::test_fifty_codes_the_catalogue_files_nothing_under_cost_three_requests_not_fifty`
  - `tests/test_isrc_screen.py::test_the_app_client_refuses_a_batch_it_was_not_built_to_ask`

Old text:

```
ISRC_BATCH = 20
```

New text:

```
ISRC_BATCH = 50
```

### `u207.C6_batch_shape_unchecked`

isrcs_held: a batch of duplicate, unfolded or malformed codes is sent as given

- File: `src/cratekit/acquire/catalogue_api.py`
- Source: `u207.json`, row `C6_batch_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_app_client_refuses_a_batch_it_was_not_built_to_ask`

Old text:

```
        if len(set(asked)) != len(asked) or any(code != match.isrc_token(code) for code in asked):
```

New text:

```
        if False:
```

### `r1115.M1_failed_needs_a_failure`

read_download: drop the rule that a FAILED job settles only with a failed track, so a FAILED job holding none reads as settled

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M1_failed_needs_a_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`

Old text:

```
        and bool(failed)

```

New text:

```
        and True

```

### `r1115.M2_every_failure_for_good`

read_download: drop the rule that every failed track is refused for good, so a transient failure settles and the go lands over it

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M2_every_failure_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-recording-no-cause]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        and len(for_good) == len(failed)

```

New text:

```
        and len(for_good) >= 0

```

### `r1115.M3_nothing_left_to_run`

read_download: drop the rule that no track is still to run, so a FAILED job with a track never attempted settles

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M3_nothing_left_to_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-track-never-attempted]`

Old text:

```
        and all(item.state in finished for item in held)

```

New text:

```
        and any(item.state in finished for item in held)

```

### `r1115.M4_retryable_is_not_for_good`

read_download: read every failure with a cause as refused for good, retryable or not

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M4_retryable_is_not_for_good`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[a-failure-a-retry-could-clear]`
  - `tests/test_label_sync_go.py::test_a_transient_failure_still_ends_the_go_on_its_refusal_with_no_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
        item.item_id for item in failed if item.cause is not None and not item.cause.retryable

```

New text:

```
        item.item_id for item in failed if item.cause is not None

```

### `r1115.M5_declined_is_refused`

read_download: leave a declined track out of the refused rows, so a lossy only track is named nowhere on the go's check

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M5_declined_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_runs_own_tail_refused_beside_a_download_names_its_tracks_refused_for_good`
  - `tests/test_label_sync_go.py::test_a_tail_refused_beside_a_download_still_names_the_tracks_refused_for_good`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
        and (item.item_id in for_good or item.state is jobs.ItemState.SKIPPED)

```

New text:

```
        and (item.item_id in for_good)

```

### `r1115.M6_landed_needs_a_track`

DownloadRead.landed: read a settled download with no track done as landed, so a tail is set over an empty folder

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M6_landed_needs_a_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_whose_every_track_failed_for_good_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`

Old text:

```
        return self.settled and self.done > 0

```

New text:

```
        return self.settled

```

### `r1115.M7_done_counts_done`

read_download: count a skipped track as done too

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M7_done_counts_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 8 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[failed-with-no-failed-track]`
  - `tests/test_label_sync_go.py::test_a_download_settles_only_when_nothing_it_did_not_land_could_land_on_a_retry[succeeded-with-a-declined-track]`
  - `tests/test_label_sync_go.py::test_a_go_under_its_run_over_a_download_that_refused_every_track_runs_no_tail`
  - `tests/test_label_sync_go.py::test_a_go_whose_every_track_was_refused_runs_no_tail_and_says_so`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
        done=sum(1 for item in held if item.state is jobs.ItemState.DONE),

```

New text:

```
        done=sum(1 for item in held if item.state in (jobs.ItemState.DONE, jobs.ItemState.SKIPPED)),

```

### `r1115.M8_failed_names_the_failures`

read_download: name no failed track, so the go's own warning for one is never raised

- File: `src/cratekit/acquire/cli.py`
- Source: `r1115.json`, row `M8_failed_names_the_failures`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 368 against a baseline of 368
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`

Old text:

```
        failed=tuple(item.item_id for item in failed if item.item_id in for_good),

```

New text:

```
        failed=(),

```

### `r289-b.B1_reclaim_rmtree`

Reclaim with rmtree, so a refused landing kept as evidence is deleted

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B1_reclaim_rmtree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-b.B3_terminal_filter_gone`

Sweep every job's staging, open ones included

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B3_terminal_filter_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-b.B4_unknown_job_read_as_terminal`

Read a directory naming a job this queue does not hold as finished

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B4_unknown_job_read_as_terminal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-b.B5_job_directory_before_its_items`

Reclaim the job directory first, so its item directories never go

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B5_job_directory_before_its_items`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-b.B6_job_directory_never_reclaimed`

Reclaim the item directories and leave the job directory behind

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `B6_job_directory_never_reclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-b.C1_download_call_site`

Drop the sweep at the head of acquire download

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-b.json`, row `C1_download_call_site`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-c.B2r_reclaim_reports_a_failure_as_a_removal`

Report a directory that could not be removed as one that was

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B2r_reclaim_reports_a_failure_as_a_removal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 398 against a baseline of 398
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

### `r289-c.B9r_children_unreadable_raises`

Let an unlistable directory raise out of the sweep and fail the verb

- File: `src/cratekit/acquire/cli.py`
- Source: `r289-c.json`, row `B9r_children_unreadable_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return tuple(sorted(directory.iterdir()))
    except OSError:
        return ()
```

New text:

```
    return tuple(sorted(directory.iterdir()))
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

### `r668-a.M11_no_frozen_list_skip`

a job whose payload names no list is compared against an empty path and refuses any list named beside it

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M11_no_frozen_list_skip`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not frozen:
        return
    try:
```

New text:

```
    try:
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

### `r668-a.M2_resume_argv_carries_the_list`

the resume argv and the drive it with line name the frozen list again

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M2_resume_argv_carries_the_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
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

### `r668-a.M6_no_list_check_on_resume`

a list named beside --job is never compared with the frozen one, so a different list is silently ignored and the job driven

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M6_no_list_check_on_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
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

### `r668-a.M9_other_verbs_job_read`

another verb's job payload is read as a frozen download list

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-a.json`, row `M9_other_verbs_job_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
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

### `r668-b.M12_home_expansion_raises`

a named list under a home directory that cannot be expanded raises instead of being compared as typed

- File: `src/cratekit/acquire/cli.py`
- Source: `r668-b.json`, row `M12_home_expansion_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`
- Collected: 93 against a baseline of 93
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

### `u108-c.G25_drive_maps_ending`

acquire_cli.drive_queued: a parked or half failed job is returned as if it ended clean

- File: `src/cratekit/acquire/cli.py`
- Source: `u108-c.json`, row `G25_drive_maps_ending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_intake_missing.py`, `tests/test_label_sync_go.py`, `tests/test_listdoc.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 508 against a baseline of 508
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

### `u274.C1_worker_names_no_drive`

acquire.cli: the download worker names no per drive holder, so a download logs in once a track

- File: `src/cratekit/acquire/cli.py`
- Source: `u274.json`, row `C1_worker_names_no_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 17 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_download_worker_names_the_vendored_drive`
  - ... and 2 more, see the JSON sidecar

Old text:

```
handle.per_drive = vendored.drive  # type: ignore[attr-defined]

```

New text:

```
(empty)
```

### `u42-author-round-2.C2_unknown_defaults_lossless`

Classify an unrecognised suffix as lossless instead of 'other'

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author-round-2.json`, row `C2_unknown_defaults_lossless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_non_audio_files_are_not_reported`

Old text:

```
    return "other"
```

New text:

```
    return "lossless"
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

### `u42-author.C3_strict_consults_the_marker`

Make strict behave like the permissive policy, admitting a marked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `C3_strict_consults_the_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`
  - `tests/test_acquire_cli.py::test_the_audit_reads_the_policy_the_configuration_actually_holds`

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

### `u42-author.P2_relative_path_leaks_the_root`

Report the absolute path, putting a real directory layout in the payload (R1)

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `P2_relative_path_leaks_the_root`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_cli.py::test_a_configuration_with_no_marker_text_decides_no_marker_question`
  - `tests/test_acquire_cli.py::test_a_lossless_file_wearing_the_marker_is_reported`
  - `tests/test_acquire_cli.py::test_an_mp4_container_is_reported_undecided_rather_than_assumed`
  - `tests/test_acquire_cli.py::test_permissive_policy_reports_only_the_unmarked_lossy_file`
  - `tests/test_acquire_cli.py::test_strict_policy_reports_every_lossy_file_marked_or_not`

Old text:

```
        where = str(path.relative_to(root))
```

New text:

```
        where = str(path)
```

### `u42-author.W1_onerror_hook`

Revert the walk to Path.rglob, which swallows the PermissionError

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W1_onerror_hook`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    for dirpath, _dirnames, filenames in os.walk(root, onerror=note):
        here = Path(dirpath)
        for name in filenames:
            path = here / name
```

New text:

```
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if True:
```

### `u42-author.W2_unreadable_reported`

Collect the unreadable directories and then never report them

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W2_unreadable_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 22933 against a baseline of 22933
- Kills: 2 (killed)
- Promoted: subset killed 0, full suite killed 2
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

### `u42-author.W3_onerror_silent`

Keep os.walk but make the error hook a no-op, the half-fix

- File: `src/cratekit/acquire/cli.py`
- Source: `u42-author.json`, row `W3_onerror_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`
- Collected: 22933 against a baseline of 22933
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

### `u54-acquisition-worker.G10_absent_result`

Drop the refusal for a run that reported OK with no result for this key

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G10_absent_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `u54-acquisition-worker.G15_no_marker_text`

Commit a lossy landing unmarked when the configuration names no marker text

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G15_no_marker_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `u54-acquisition-worker.G17_paced_sleep_bound`

Let the pool bind its own definition time sleep instead of the one the frozen configuration paces

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G17_paced_sleep_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `u54-acquisition-worker.G19_frozen_config`

Build the adapter settings from a fresh load rather than the configuration the job was frozen against

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G19_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 40 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_deleted_frozen_list_named_relative_from_where_it_was_queued_still_drives`
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
  - ... and 25 more, see the JSON sidecar

Old text:

```
    settings = AdapterSettings.from_config(cfg)
```

New text:

```
    settings = AdapterSettings.from_config(_load())
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

### `u54-acquisition-worker.G20_output_exists`

Replace a file already at the destination instead of refusing

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G20_output_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `u54-acquisition-worker.G2_missing_identifier`

Queue a provider list whose rows carry no identifier, dropping the by-position refusal

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G2_missing_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `u54-acquisition-worker.G8_park_on_block`

Read a parked run as an ordinary result, so the driver claims the next item into a provider block

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G8_park_on_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `u54-acquisition-worker.G9_failed_invocation`

Ignore an invocation the adapter could not run at all

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G9_failed_invocation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
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

### `r703-a.D1_pool_reads_text`

classify_signal reads a NoFileLanded's carried words for block and rate limit markers

- File: `src/cratekit/acquire/download.py`
- Source: `r703-a.json`, row `D1_pool_reads_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_pacing.py`, `tests/test_provider_gate.py`
- Collected: 445 against a baseline of 445
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
  - `tests/test_acquire_fallback.py::test_an_acceptance_over_one_option_is_that_option`

Old text:

```
    if chosen is None and count == 1:
```

New text:

```
    if chosen is None and count == 0:
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

### `r679-b.D2_fallback_gate_on_question_alone`

fallback pass: gate the store on the needs-review state alone

- File: `src/cratekit/acquire/fallback_cli.py`
- Source: `r679-b.json`, row `D2_fallback_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
    if any(match_cli.touches_the_queue(one) for one in resolved.matches):
```

New text:

```
    if any(one.state is match.MatchState.NEEDS_REVIEW for one in resolved.matches):
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

### `r1313.I1_cache_failure_alone`

said_not_found: read the 404 off the failure alone, as before R-1313, so an ISRC answered with a 404 page is never kept

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I1_cache_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 401 against a baseline of 401
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.I2_cache_keeps_any_status`

said_not_found: keep any failure carrying a status, so an outage is remembered for a week as filed under nothing

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `r1313.json`, row `I2_cache_keeps_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 401 against a baseline of 401
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[500]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[500-json-isrc_cache]`
  - `tests/test_provider_not_found_bodies.py::test_a_server_error_is_never_a_not_found_whatever_its_body[503-empty-isrc_cache]`

Old text:

```
    return answered_not_found(exc)
```

New text:

```
    return answered_not_found(exc) or getattr(getattr(exc, "response", None), "status_code", None) is not None
```

### `u206-b.M10b_day_coefficient_halved`

DAY_S halved, measured again once the tests write a day out as 86 400 seconds

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M10b_day_coefficient_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`

Old text:

```
DAY_S = 86_400
```

New text:

```
DAY_S = 43_200
```

### `u206-b.M2b_disabled_recall_composite`

Composite: drop recall's days 0 guard AND give every entry at least a day's life, so answers kept before the cache was turned off still answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M2b_disabled_recall_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_answers_kept_before_the_cache_was_turned_off_answer_nothing`
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`

Old text:

```
        global _PROCESS_HITS
        if not self.enabled:
            return None
```

New text:

```
        global _PROCESS_HITS
        self.days = max(self.days, 1)
```

### `u206.M11_unreadable_answer_kept`

Cache.remember: keep an answer holding a track that cannot be read

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M11_unreadable_answer_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 4 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-artist]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-identifier]`
  - `tests/test_isrc_cache.py::test_an_answer_holding_a_track_that_cannot_be_read_is_asked_again[no-title]`
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`

Old text:

```
        if not all(_readable(track) for track in tracks):
            return False
```

New text:

```
        if False:
            return False
```

### `u206.M12_corrupt_file_not_set_aside`

Cache._entries: a file that does not parse is read as empty and overwritten, never set aside

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M12_corrupt_file_not_set_aside`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds`
  - `tests/test_isrc_cache.py::test_a_file_of_another_shape_is_set_aside_too`
  - `tests/test_isrc_cache.py::test_doctor_names_a_set_aside_file_and_never_fails`

Old text:

```
        if entries is None:
            if locked:
                self._set_aside_held()
            else:
                self._set_aside()
            return {}
```

New text:

```
        if entries is None:
            return {}
```

### `u206.M13_write_without_merge`

Cache.remember: write only this entry, dropping what another process wrote since

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M13_write_without_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_second_run_over_the_same_set_asks_the_provider_no_isrc_again`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
            merged = {
                name: entry for name, entry in entries.items() if self._fresh(entry, now) is not None
            }
```

New text:

```
            merged = {}
```

### `u206.M16_said_not_found_widened`

said_not_found: read InvalidISRC as a said not found too

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M16_said_not_found_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`
  - `tests/test_isrc_cache.py::test_said_not_found_is_the_clients_own_class_or_a_404_and_nothing_else[invalid-isrc]`

Old text:

```
    if type(exc).__name__ == "ObjectNotFound":
```

New text:

```
    if type(exc).__name__ in ("ObjectNotFound", "InvalidISRC"):
```

### `u206.M1_recall_never_hits`

Cache.recall: never answer from the file, so every lookup asks the provider again

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M1_recall_never_hits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_second_run_over_the_same_set_asks_the_provider_no_isrc_again`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[streamable]`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[withdrawn]`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        held = self._fresh(entries.get(key), self.clock())
```

New text:

```
        held = None
```

### `u206.M21_override_ignored`

_resolved: ignore CRATEKIT_ISRC_CACHE_DIR, so a hand copy run cannot share the live answers

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M21_override_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`

Old text:

```
    if override:
        return Path(override) / config.state_file(key).relative
```

New text:

```
    if False:
        return Path(override) / config.state_file(key).relative
```

### `u206.M3_disabled_still_remembers`

Cache.remember: drop the days 0 guard, so a cache turned off still writes the file

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M3_disabled_still_remembers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`

Old text:

```
        if not self.enabled:
            return False
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
```

New text:

```
        key = _key(isrc, country)
        if key is None:
            return False
        tracks = list(tracks)
```

### `u206.M4_unfolded_spelling_kept`

_key: keep a spelling that is not its own fold under the folded key

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M4_unfolded_spelling_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_spelling_that_is_not_its_own_fold_is_asked_and_never_kept`

Old text:

```
    if not folded or folded != isrc:
```

New text:

```
    if not folded:
```

### `u206.M5_country_ignored`

_key: leave the country out, so an answer in one country answers another

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M5_country_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_corrupt_file_is_set_aside_and_the_lookup_succeeds`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`

Old text:

```
    return f"{folded}|{country}"
```

New text:

```
    return f"{folded}|"
```

### `u206.M6_not_found_lives_as_found`

_fresh: a not found lives as long as a found answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M6_not_found_lives_as_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`

Old text:

```
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
```

New text:

```
        days = self.days
```

### `u206.M7_not_found_ignores_shorter_setting`

_fresh: a not found lives a week even when the setting is shorter

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M7_not_found_ignores_shorter_setting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_not_found_lives_no_longer_than_a_shorter_setting`

Old text:

```
        days = self.days if tracks else min(NOT_FOUND_DAYS, self.days)
```

New text:

```
        days = self.days if tracks else NOT_FOUND_DAYS
```

### `u206.M8_expiry_off_by_one`

_fresh: an entry exactly its lifetime old is still used

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M8_expiry_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_not_found_lives_no_longer_than_a_shorter_setting`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`

Old text:

```
        if age < 0 or age >= days * DAY_S:
```

New text:

```
        if age < 0 or age > days * DAY_S:
```

### `u206.M9_future_stamp_trusted`

_fresh: an entry stamped later than now is used

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M9_future_stamp_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1135 against a baseline of 1135
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_answer_stamped_later_than_now_is_asked_again`

Old text:

```
        if age < 0 or age >= days * DAY_S:
```

New text:

```
        if age >= days * DAY_S:
```

### `u207.S1_any_client_screened`

screen: ask any client with an isrcs_held member, not only the app catalogue, so a stand in that answers an empty set marks every code absent

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S1_any_client_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_stand_in_for_the_client_is_never_screened_whatever_it_answers`

Old text:

```
        if self._stopped or not isinstance(client, catalogue_api.AppCatalogue):
            return 0
```

New text:

```
        if self._stopped or not callable(getattr(client, "isrcs_held", None)):
            return 0
```

### `u207.S2_lone_code_screened`

screen: a batch of one code is screened, paying a request its own lookup would have answered

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S2_lone_code_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_lone_code_is_never_screened_since_its_own_lookup_costs_the_same`

Old text:

```
MIN_BATCH = 2
```

New text:

```
MIN_BATCH = 1
```

### `u207.S3_unfolded_spelling_screened`

screen: a spelling that is not its own fold enters a batch, so a lowercase code is screened under its fold

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S3_unfolded_spelling_screened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_malformed_code_or_a_spelling_not_its_own_fold_never_enters_a_batch`

Old text:

```
            if code and code == match.isrc_token(code) and code not in self._asked
```

New text:

```
            if code and match.isrc_token(code) and code not in self._asked
```

### `u207.S4_rate_limit_keeps_screening`

screen: a rate limit or a rejected app credential on a batch leaves the screening running, so every later batch is sent into it

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S4_rate_limit_keeps_screening`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_rate_limit_on_a_batch_is_counted_marks_nothing_and_stops_the_screening`
  - `tests/test_isrc_screen.py::test_a_rejected_app_credential_on_a_batch_marks_nothing_and_stops_the_screening`

Old text:

```
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                self._stopped = True
                break
```

New text:

```
            except (catalogue_api.CatalogueRateLimited, catalogue_api.AppCredentialsRejected):
                continue
```

### `u207.S5_refused_form_keeps_screening`

screen: a 4xx refusal of the request form does not stop the screening

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S5_refused_form_keeps_screening`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 3 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[400]`
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[404]`
  - `tests/test_isrc_screen.py::test_a_refused_request_form_stops_the_screening_and_marks_nothing[422]`

Old text:

```
                if exc.status is not None and 400 <= exc.status < 500:
```

New text:

```
                if exc.status is not None and 400 <= exc.status < 400:
```

### `u207.S6_failed_batch_read_as_empty`

screen: a batch the API could not answer is read as an empty answer, so every code in it is answered not found

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S6_failed_batch_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_failed_batch_does_not_stop_the_next_one`
  - `tests/test_isrc_screen.py::test_a_server_error_on_a_batch_falls_back_to_singles_and_finds_the_one_bad_answer`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[a-code-not-asked]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-isrc]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[no-list]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[not-a-resource]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[paged]`
  - `tests/test_isrc_screen.py::test_an_answer_that_cannot_be_attributed_whole_marks_nothing_absent[unreadable-isrc]`

Old text:

```
                continue
            self._absent.update(code for code in batch if code not in held)
```

New text:

```
                held = frozenset()
            self._absent.update(code for code in batch if code not in held)
```

### `u207.S7_failed_batch_sent_again`

screen: a batch's codes are marked asked only once it answered, so a failed batch is sent again by the next plan

- File: `src/cratekit/acquire/isrc_screen.py`
- Source: `u207.json`, row `S7_failed_batch_sent_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_catalogue_app.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_a_batch_that_failed_is_not_sent_again_by_the_next_plan`
  - `tests/test_isrc_screen.py::test_a_code_already_screened_is_not_sent_again`

Old text:

```
            self._asked.update(batch)
            made += 1
```

New text:

```
            made += 1
```

### `u68.D1_unlisted_on_blank_ref`

A row with no provider id is written to the document instead of being returned unlisted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D1_unlisted_on_blank_ref`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_with_no_provider_id_is_unlisted_and_the_document_still_reads`
  - `tests/test_listdoc.py::test_a_track_from_another_service_is_unlisted_not_written_as_a_provider_id`
  - `tests/test_listdoc.py::test_no_listable_row_writes_nothing_and_says_so`

Old text:

```
        if not ref:
            unlisted.append(row)
            continue
```

New text:

```
        if False:
            unlisted.append(row)
            continue
```

### `u68.D2_first_id_wins`

A repeated id is written again instead of being folded into its first occurrence

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D2_first_id_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_duplicate_id_is_written_once_and_the_first_occurrence_wins`
  - `tests/test_listdoc.py::test_an_id_is_compared_stripped_because_the_reader_strips_it`

Old text:

```
        if ref in seen:
            continue
```

New text:

```
        if False:
            continue
```

### `u68.D3_ref_stripped`

An id is compared as given rather than stripped, as the reader strips it

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D3_ref_stripped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_with_no_provider_id_is_unlisted_and_the_document_still_reads`
  - `tests/test_listdoc.py::test_an_id_is_compared_stripped_because_the_reader_strips_it`

Old text:

```
        ref = str(row.ref or "").strip()
```

New text:

```
        ref = str(row.ref or "")
```

### `u68.D4_reader_check`

Drop the read back through the reader's own row recognition, so a row the reader refuses is written

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `D4_reader_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-artist]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-title]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`

Old text:

```
        track = _track(row, ref)
        _checked(track, position)
```

New text:

```
        track = _track(row, ref)
```

### `u68.F1_different_file_refused`

An existing file holding different bytes is overwritten instead of refused

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `F1_different_file_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_an_existing_different_list_is_refused_and_left_alone`
  - `tests/test_listdoc.py::test_an_existing_different_manifest_is_refused_before_the_list_is_written`
  - `tests/test_listdoc.py::test_an_existing_different_unlisted_file_refuses_before_either_half_is_written`

Old text:

```
    if present != payload:
```

New text:

```
    if False:
```

### `u68.M1_manifest_version`

The manifest records the declared version of a row as empty

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `M1_manifest_version`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_the_manifest_records_each_ids_provenance`

Old text:

```
            "version": track.get("version", ""),
```

New text:

```
            "version": "",
```

### `u68.N1_slash`

A name holding a slash is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `N1_slash`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[a/b]`

Old text:

```
        or "/" in name

```

New text:

```
(empty)
```

### `u68.N2_surrounding_space`

A name with leading or trailing space is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `N2_surrounding_space`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[ set]`

Old text:

```
        or name != name.strip()

```

New text:

```
(empty)
```

### `u68.N3_dot_names`

A name of one or two dots is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `N3_dot_names`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[..]`
  - `tests/test_listdoc.py::test_a_name_that_is_not_one_plain_file_name_is_refused[.]`

Old text:

```
        or name in {".", ".."}

```

New text:

```
(empty)
```

### `u68.P1_missing_provenance`

A listed id with no provenance is not refused by name

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `P1_missing_provenance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_listed_id_with_no_provenance_refuses_and_writes_nothing`

Old text:

```
    if found is None:
        raise ListDocRefused
```

New text:

```
    if False:
        raise ListDocRefused
```

### `u68.P2_blank_source`

A provenance naming no source is accepted

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `P2_blank_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_provenance_naming_no_source_refuses`

Old text:

```
    if not isinstance(found.source, str) or not found.source.strip():
```

New text:

```
    if False:
```

### `u68.T1_version_written`

A declared version is not written to the track

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `T1_version_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 6 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (Extended)]`
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (feat. Mira) (Extended)]`
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_a_version_re_reads_to_the_same_token[Tide Line-Dub-dub]`
  - `tests/test_listdoc.py::test_the_list_round_trips_through_the_real_reader_and_the_download_freeze`
  - `tests/test_listdoc.py::test_the_manifest_records_each_ids_provenance`

Old text:

```
    if row.version.strip():
        track["version"]
```

New text:

```
    if False:
        track["version"]
```

### `u68.T2_isrc_written`

An isrc is not written to the track

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `T2_isrc_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 4 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_row_reads_as_the_wanted_track_its_list_row_reads_as`
  - `tests/test_listdoc.py::test_frozen_tracks_become_rows_that_freeze_back_identically`
  - `tests/test_listdoc.py::test_the_list_round_trips_through_the_real_reader_and_the_download_freeze`
  - `tests/test_listdoc.py::test_the_manifest_records_each_ids_provenance`

Old text:

```
    if row.isrc and row.isrc.strip():
```

New text:

```
    if False:
```

### `u68.T3_key_written`

A key is not written to the track

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `T3_key_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_the_list_round_trips_through_the_real_reader_and_the_download_freeze`

Old text:

```
    if row.key and row.key.strip():
```

New text:

```
    if False:
```

### `u68.W1_other_service_unlisted`

A track from another service keeps its id and is written as a provider id

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `W1_other_service_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_track_from_another_service_is_unlisted_not_written_as_a_provider_id`

Old text:

```
    ref = wanted.ref if wanted.origin == match.TIDAL else ""
```

New text:

```
    ref = wanted.ref
```

### `u68.W2_raw_title_candidate`

Drop the raw title plus declared version spelling, so the split title is the fallback

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u68.json`, row `W2_raw_title_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (Extended)]`
  - `tests/test_listdoc.py::test_a_declared_version_beside_an_embedded_one_round_trips_whole[Sun Path (feat. Mira) (Extended)]`

Old text:

```
        if wanted.version and wanted.spelled.endswith(suffix):
```

New text:

```
        if False:
```

### `u73-b.C1_refs_only_when_several`

Write source_refs for a single reference too, changing the bytes of a manifest an earlier build wrote

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u73-b.json`, row `C1_refs_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_one_reference_writes_the_bytes_a_manifest_had_before_the_field`

Old text:

```
        if len(origin.source_refs) > 1:
```

New text:

```
        if len(origin.source_refs) >= 1:
```

### `u73-b.C2_refs_written`

Never write source_refs into the manifest

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u73-b.json`, row `C2_refs_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 2 (killed)
- Killed:
  - `tests/test_listdoc.py::test_every_source_that_asked_for_an_id_reads_back`
  - `tests/test_listdoc.py::test_the_manifest_keeps_every_reference_an_id_came_from`

Old text:

```
            entry["source_refs"] = list(origin.source_refs)
```

New text:

```
            pass
```

### `u77-c.C1_manifest_version`

manifest_rows: refuse only a version below this build's, so a manifest of a later version is read on the hope its keys still mean what they meant

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C1_manifest_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves[{"manifest": 2, "rows": {}}-version 2]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 2, "rows": {}}-version 2]`

Old text:

```
if isinstance(version, bool) or version != MANIFEST_VERSION:
```

New text:

```
if isinstance(version, bool) or version < MANIFEST_VERSION:
```

### `u77-c.C2_manifest_version_bool`

manifest_rows: drop the boolean test on the version, so true, which Python holds equal to 1, reads as version 1

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C2_manifest_version_bool`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": true, "rows": {}}-version True]`

Old text:

```
if isinstance(version, bool) or version != MANIFEST_VERSION:
```

New text:

```
if version != MANIFEST_VERSION:
```

### `u77-c.C3_not_a_manifest`

manifest_rows: stop asking whether the document names a manifest version at all, so a list document passed by mistake is not refused by name

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C3_not_a_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_list_passed_where_the_manifest_belongs_is_refused_before_the_gate`
  - `tests/test_landing_labels.py::test_a_manifest_that_cannot_be_read_refuses_before_any_file_moves[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"list": 1, "origin": "tidal", "tracks": []}-not a manifest]`

Old text:

```
if not isinstance(body, Mapping) or "manifest" not in body:
```

New text:

```
if not isinstance(body, Mapping):
```

### `u77-c.C4_year_bool`

_manifest_row: drop the boolean test on the year, so a year of true is read as the year 1

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C4_year_bool`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_manifest_this_build_did_not_write_is_refused_whole[{"manifest": 1, "rows": {"1": {"source": "label", "year": true}}}-year]`

Old text:

```
if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
```

New text:

```
if year is not None and not isinstance(year, int):
```

### `u77-c.C5_source_refs_kept`

_manifest_row: read every entry's source_refs as empty, so the other sources that asked for an id are lost on the way back

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u77-c.json`, row `C5_source_refs_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 285 against a baseline of 285
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_every_source_that_asked_for_an_id_reads_back`

Old text:

```
            source_refs=tuple(asked),

```

New text:

```
            source_refs=(),

```

### `u78-c.C1_readback_identity`

The text line read back compares only that one track came back, not which

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C1_readback_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 149 against a baseline of 149
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[leading-ordinal]`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[separator-in-artist]`

Old text:

```
    if len(again) != 1 or (again[0].recording, again[0].version_key) != (
        wanted.recording,
        wanted.version_key,
    ):
```

New text:

```
    if len(again) != 1:
```

### `u78-c.C2_readback_count`

The text line read back no longer requires exactly one track, so a line read as a comment passes

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C2_readback_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[read-as-a-comment]`

Old text:

```
    if len(again) != 1 or (again[0].recording, again[0].version_key) != (
```

New text:

```
    if again and (again[0].recording, again[0].version_key) != (
```

### `u78-c.C3_dedupe_lines`

The same line twice is written twice

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C3_dedupe_lines`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_the_same_line_twice_is_written_once_under_its_first_reason`

Old text:

```
        if line in seen:
            continue
        seen.add(line)
```

New text:

```
        seen.add(line)
```

### `u78-c.C4_reason_one_row`

A reason carrying a line break is written as it stands, so the text reader refuses the whole file

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C4_reason_one_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_reason_carrying_a_line_break_stays_one_row`

Old text:

```
        tracks.extend((f"# {' '.join(str(entry.reason).split())}", line))
```

New text:

```
        tracks.extend((f"# {entry.reason}", line))
```

### `u78-c.C5_unlisted_checked_first`

The unlisted file is written over whatever is there, after the list, rather than checked with the other two

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `C5_unlisted_checked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 149 against a baseline of 149
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_different_file_at_the_unlisted_path_refuses_before_the_list_is_written`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[leading-ordinal]`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[read-as-a-comment]`
  - `tests/test_listdoc.py::test_a_row_that_would_read_back_as_another_track_is_refused_by_position[separator-in-artist]`
  - `tests/test_listdoc.py::test_an_existing_different_unlisted_file_refuses_before_either_half_is_written`

Old text:

```
        files.append((unlisted_path, _encoded(text_document(handed))))
    pending = [(path, payload) for path, payload in files if not _unchanged(path, payload)]
    for path, payload in pending:
        config.atomic_write_bytes(payload, path)
```

New text:

```
    pending = [(path, payload) for path, payload in files if not _unchanged(path, payload)]
    for path, payload in pending:
        config.atomic_write_bytes(payload, path)
    if handed:
        config.atomic_write_bytes(_encoded(text_document(handed)), unlisted_path)
```

### `u78-c.E2_emitter_checks_rows`

Existing guard sample: the emitter no longer reads each listed row back through the reader

- File: `src/cratekit/acquire/listdoc.py`
- Source: `u78-c.json`, row `E2_emitter_checks_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_listdoc.py`
- Collected: 61 against a baseline of 61
- Kills: 3 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-artist]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[no-title]`
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`

Old text:

```
        _checked(track, position)
```

New text:

```
(empty)
```

### `r1016.M10_wrong_endpoint`

The account walk asks the account's own created playlists endpoint, which leaves out the followed ones the listing has always served

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M10_wrong_endpoint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M1_account_walk_back_on_the_clients_method`

The account walk calls the client's playlist_and_favorite_playlists again, which parses through parse_factory and fetches every owned playlist, the defect itself

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M1_account_walk_back_on_the_clients_method`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M2_account_parse_through_the_factory`

The account walk keeps its own request but parses with parse_factory, so every owned playlist is fetched again

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M2_account_parse_through_the_factory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M3_folder_parse_through_the_factory`

The folder walk parses with parse_factory again, so every owned playlist in a folder is fetched again

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M3_folder_parse_through_the_factory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M4_date_added_not_moved`

The listing's created is no longer moved onto the playlist as dateAdded, so user_date_added is lost where the client's method kept it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M4_date_added_not_moved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M5_not_a_page_check_dropped`

An answer that is not a page is no longer refused by name and escapes as a bare KeyError or TypeError

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M5_not_a_page_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M7_send_translation_dropped`

_send no longer translates a rejected signature, so a client whose request moved is retried through the whole ladder as a raw TypeError

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M7_send_translation_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M8_walk_name_ignored`

_client_part's refusal names the folder listing whatever walk it was called for, so the account walk blames the wrong listing

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M8_walk_name_ignored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.M9_offset_not_sent`

The account request always asks for offset 0, so the walk reads its first page until the budget raises

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `M9_offset_not_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1016.S1_account_dedup_dropped`

Sample of an existing guard: the account listing loses its dedup by identifier, so a playlist re-served across a page boundary is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r1016.json`, row `S1_account_dedup_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/modules/test_labels.py`, `tests/test_provider_gate.py`, `tests/intake/test_workers.py`
- Collected: 832 against a baseline of 832
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

### `r1360.J1_prefix_agrees`

judge_window: a first part beside a whole window agrees, as U226 left it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J1_prefix_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged6-unpaged6-4-lags]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged7-unpaged7-4-lags]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged8-unpaged8-4-lags]`

Old text:

```
        return WINDOW_LAGS if counted and len(paged) >= declared else WINDOW_AGREES
```

New text:

```
        return WINDOW_AGREES
```

### `r1360.J2_prefix_equal_only`

judge_window: a first part lags only beside a window of exactly the count

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J2_prefix_equal_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged8-unpaged8-4-lags]`

Old text:

```
counted and len(paged) >= declared else
```

New text:

```
counted and len(paged) == declared else
```

### `r1360.J3_prefix_always_lags`

judge_window: a first part beside a window short of the count lags too

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J3_prefix_always_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged4-unpaged4-4-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged5-unpaged5-4-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged9-unpaged9-None-agrees]`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
        return WINDOW_LAGS if counted and len(paged) >= declared else WINDOW_AGREES
```

New text:

```
        return WINDOW_LAGS
```

### `r1360.J4_prefix_uncounted_lags`

judge_window: a first part beside a playlist declaring no count lags

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J4_prefix_uncounted_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged9-unpaged9-None-agrees]`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
WINDOW_LAGS if counted and len(paged) >= declared else
```

New text:

```
WINDOW_LAGS if not counted or len(paged) >= declared else
```

### `r1360.W10_walk_past_count`

playlist_tracks_unpaged: the walk asks again at the declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W10_walk_past_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[199-2]`

Old text:

```
        if len(rows) >= declared:
            break
```

New text:

```
        if len(rows) > declared:
            break
```

### `r1360.W11_offset_dropped`

playlist_tracks_unpaged: a later request is asked with no offset

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W11_offset_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 19 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
                return playlist.tracks(offset=offset) if offset else playlist.tracks()
```

New text:

```
                return playlist.tracks()
```

### `r1360.W12_tag_unread`

playlist_tracks_unpaged: the first page's tag is not read, so no walk holds together where a client keeps one

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W12_tag_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`

Old text:

```
    tag = getattr(playlist, "_etag", None)
    for _ask
```

New text:

```
    tag = None
    for _ask
```

### `r1360.W13_declared_unread`

playlist_tracks_unpaged: the walk reads no declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W13_declared_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 24 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_page_carrying_another_version_tag_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_empty_later_page_ends_the_walk`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    declared = getattr(playlist, "num_tracks", None)
    if not _is_count
```

New text:

```
    declared = None
    if not _is_count
```

### `r1360.W14_cap_of_one_walked`

playlist_tracks_unpaged: a first page of one track is walked, which reads no new track a request

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W14_cap_of_one_walked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_cap_of_one_track_is_read_once_rather_than_walked_forever`

Old text:

```
or len(rows) >= declared or len(rows) < 2:
```

New text:

```
or len(rows) >= declared or len(rows) < 1:
```

### `r1360.W15_short_page_walked_past`

playlist_tracks_unpaged: a page shorter than the first does not end the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W15_short_page_walked_past`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`

Old text:

```
        rows.extend(page[1:])
        if len(page) < step:
            break

```

New text:

```
        rows.extend(page[1:])

```

### `r1360.W1_no_walk`

playlist_tracks_unpaged: a first page short of the declared count is not walked past, as U226 left it

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W1_no_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 24 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_page_carrying_another_version_tag_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_empty_later_page_ends_the_walk`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - ... and 9 more, see the JSON sidecar

Old text:

```
    if not _is_count(declared) or len(rows) >= declared or len(rows) < 2:
        return rows
```

New text:

```
    if True:
        return rows
```

### `r1360.W2_walk_no_overlap`

playlist_tracks_unpaged: each later request starts where the last ended, not one track back

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W2_walk_no_overlap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 19 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_outbound_window_lag.py::test_the_walk_stops_once_it_holds_the_declared_count`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[120-51-0]`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        offset = len(rows) - 1

```

New text:

```
        offset = len(rows)

```

### `r1360.W3_no_start_check`

playlist_tracks_unpaged: a page is taken without starting on the last track read

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W3_no_start_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_page_that_does_not_start_where_the_last_ended_ends_the_walk_before_it`

Old text:

```
            or row_id(page[0]) != row_id(rows[-1])

```

New text:

```
(empty)
```

### `r1360.W4_no_tag_check`

playlist_tracks_unpaged: a page carrying another version tag is taken

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W4_no_tag_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_page_carrying_another_version_tag_ends_the_walk_before_it`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
            or getattr(playlist, "_etag", None) != tag

```

New text:

```
(empty)
```

### `r1360.W5_no_length_check`

playlist_tracks_unpaged: a page longer than the first is taken

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W5_no_length_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_page_longer_than_the_first_ends_the_walk_before_it`

Old text:

```
            or len(page) > step

```

New text:

```
(empty)
```

### `r1360.W6_no_empty_check`

playlist_tracks_unpaged: an empty later page is not read as the end of the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W6_no_empty_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_an_empty_later_page_ends_the_walk`

Old text:

```
            not page
            or len(page) > step
```

New text:

```
            len(page) > step
```

### `r1360.W7_full_page_ends`

playlist_tracks_unpaged: a full later page ends the walk as a short one does

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W7_full_page_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_unpaged_read_walks_past_a_capped_first_page_one_track_back`
  - `tests/test_sync_pair_calls.py::test_a_300_track_order_with_adds_and_removals_stays_inside_its_forecast`
  - `tests/test_sync_pair_calls.py::test_an_existing_playlists_removals_and_additions_cost_what_is_expected[250-60-120]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[200-3]`
  - `tests/test_sync_pair_calls.py::test_an_unpaged_reads_requests_are_what_its_walk_asks[250-3]`

Old text:

```
        if len(page) < step:
            break
```

New text:

```
        if len(page) <= step:
            break
```

### `r1360.W8_overlap_kept`

playlist_tracks_unpaged: the overlapping track is read twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W8_overlap_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 826 against a baseline of 826
- Kills: 25 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_long_playlist_nothing_changed_is_read_whole_and_written_once`
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_short_later_page_is_the_last_one_asked_for`
  - `tests/test_outbound_window_lag.py::test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_each_later_page_goes_through_the_retry_ladder`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - ... and 10 more, see the JSON sidecar

Old text:

```
        rows.extend(page[1:])
```

New text:

```
        rows.extend(page)
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

### `r504-a.A5_listing_no_count`

The listing hands back no count at all

- File: `src/cratekit/acquire/listing.py`
- Source: `r504-a.json`, row `A5_listing_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 659 against a baseline of 659
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_listing_hands_back_the_count_the_walk_ended_on`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
    return rows, total if isinstance(total, int) and total > 0 else None
```

New text:

```
    return rows, None
```

### `r504-a.A6_listing_unrecorded`

The listing walks on the unrecorded count, so the one it ended on is never kept

- File: `src/cratekit/acquire/listing.py`
- Source: `r504-a.json`, row `A6_listing_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 659 against a baseline of 659
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_listing_hands_back_the_count_the_walk_ended_on`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`

Old text:

```
    rows = favorite_tracks(session, declared_total=declared, **kwargs)
```

New text:

```
    rows = favorite_tracks(session, declared_total=count, **kwargs)
```

### `r504-a.A7_listing_nonpositive`

The listing trusts a zero or sentinel count and hands it back as a count

- File: `src/cratekit/acquire/listing.py`
- Source: `r504-a.json`, row `A7_listing_nonpositive`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`
- Collected: 659 against a baseline of 659
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[-1]`
  - `tests/test_label_tidal_catalogue.py::test_a_count_the_provider_did_not_publish_leaves_nothing_to_compare[0]`

Old text:

```
    return rows, total if isinstance(total, int) and total > 0 else None
```

New text:

```
    return rows, total if isinstance(total, int) else None
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

### `r878-a.A11_count_alone_is_a_page`

paginate_cursor: refuse a response that declares a count but carries no items, so an empty folder refuses

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A11_count_alone_is_a_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-a.A12_parse_retried`

paginate_cursor: parse each item once with no retry, so a rate limited playlist read refuses the verb

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A12_parse_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-a.A13_dedupe_shared`

_take: never skip an identifier already taken, in both walks

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A13_dedupe_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-a.A2_cursor_refuses_offset_rule`

paginate_cursor: drop the refusal of a shape that declares an offset rule

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A2_cursor_refuses_offset_rule`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-a.A8_no_cursor_ends`

paginate_cursor: a response with no cursor no longer ends the walk

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A8_no_cursor_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-a.A9_cursor_advances`

paginate_cursor: never send the cursor the last response carried, so every request reads the first page

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-a.json`, row `A9_cursor_advances`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-b.B10_folder_dedupe_key`

account_folders: no dedupe key, so a folder served on two windows is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B10_folder_dedupe_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r878-b.B2_client_part_refusal`

_client_part: drop the refusal of a missing client part, so a moved request object is retried and slept on

- File: `src/cratekit/acquire/listing.py`
- Source: `r878-b.json`, row `B2_client_part_refusal`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 142 against a baseline of 142
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

### `r887-a.K2_playlists_kept_unfiltered`

listing.folder_playlists: keep nothing out, so a nested folder is parsed as a playlist

- File: `src/cratekit/acquire/listing.py`
- Source: `r887-a.json`, row `K2_playlists_kept_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 198 against a baseline of 198
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

### `r887-a.K3_count_kept_not_served`

paginate_cursor: compare the kept items, not every served item, with the declared total, which is R-878's refusal on every real account

- File: `src/cratekit/acquire/listing.py`
- Source: `r887-a.json`, row `K3_count_kept_not_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 198 against a baseline of 198
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

### `r887-a.K5_filter_before_count`

paginate_cursor: skip a raw item before counting it, so kept items alone are counted

- File: `src/cratekit/acquire/listing.py`
- Source: `r887-a.json`, row `K5_filter_before_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`, `tests/test_export_set.py`
- Collected: 198 against a baseline of 198
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

### `r888.H1_held_is_paged`

listing.artist_releases: a HeldReleases roster is treated as a provider artist, probed for paging methods it lacks, and read as empty

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H1_held_is_paged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_crawl_that_read_everything_still_succeeds`
  - `tests/test_label_tidal_catalogue.py::test_a_held_artist_rate_limited_during_discovery_is_not_recorded_as_unread`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_a_rate_limit_during_discovery_fails_the_sweep_and_names_the_artist`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_larger_than_one_artists_budget_is_read_in_full_once_each`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_member_missing_one_listing_fails_the_sweep_and_names_it`
  - `tests/test_label_tidal_catalogue.py::test_a_roster_release_credited_under_two_artists_is_returned_once`
  - `tests/test_label_tidal_catalogue.py::test_a_various_compilation_the_credited_artists_do_not_list_is_not_offered`
  - `tests/test_label_tidal_catalogue.py::test_discovery_from_a_copyright_matching_compilation_offers_the_credited_artist`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory`

Old text:

```
    held = isinstance(artist, HeldReleases)
```

New text:

```
    held = False
```

### `r888.H2_held_not_deduplicated`

listing.artist_releases: a release a held roster lists under two artists is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H2_held_not_deduplicated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_roster_release_credited_under_two_artists_is_returned_once`

Old text:

```
            if identity in seen:
```

New text:

```
            if identity in seen and not held:
```

### `r888.H3_unheld_listing_not_recorded`

listing.artist_releases: a listing a held roster does not hold reads as an empty listing and is not recorded as skipped

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H3_unheld_listing_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`

Old text:

```
        listed = artist.held(method) if held else getattr(artist, method, None)
```

New text:

```
        listed = (artist.held(method) or []) if held else getattr(artist, method, None)
```

### `r888.H4_provider_budget_halved`

listing.PAGE_CAPS: a real provider artist's release walk gets a budget of 50 requests rather than 100

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H4_provider_budget_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_listing_that_never_ends_still_spends_its_budget_and_blames_the_offset`

Old text:

```
    # A label roster held in memory spends none of it (R-888, ``HeldReleases``).
    "artist_releases": 100,
```

New text:

```
    # A label roster held in memory spends none of it (R-888, ``HeldReleases``).
    "artist_releases": 50,
```

### `r888.H5_abstract_held`

listing.HeldReleases: held is not abstract, so a subclass without it is built and fails mid crawl

- File: `src/cratekit/acquire/listing.py`
- Source: `r888.json`, row `H5_abstract_held`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_held_object_that_forgets_its_lists_fails_when_built`

Old text:

```
    @abstractmethod
    def held(
```

New text:

```
    def held(
```

### `u226.M1_equal_not_agreed`

judge_window: two equal reads are not read as agreeing first

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M1_equal_not_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 783 against a baseline of 783
- Kills: 78 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_outbound_window_lag.py::test_a_window_short_of_the_declared_total_still_refuses_with_nothing_sent`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged0-unpaged0-2-agrees]`
  - `tests/test_outbound_window_lag.py::test_the_judge_reads_the_two_reads_against_the_declared_count[paged1-unpaged1-3-agrees]`
  - `tests/test_prune.py::test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent`
  - `tests/test_prune.py::test_a_settled_track_the_listing_hides_is_not_recorded_as_off`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - ... and 63 more, see the JSON sidecar

Old text:

```
    if unpaged == paged:
        return WINDOW_AGREES
```

New text:

```
    if False:
        return WINDOW_AGREES
```

### `u226.M4_prefix_as_subset`

judge_window: any unpaged read whose tracks the window holds agrees, wherever they stand

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M4_prefix_as_subset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 783 against a baseline of 783
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_named_pair_whose_window_lags_refuses_as_itself`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_lags_beside_a_partial_unpaged_read_holds_the_pair_and_says_why`
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
paged[: len(unpaged)] == unpaged
```

New text:

```
set(unpaged) <= set(paged)
```

### `u252.L1_ladder_exponent`

fetch_with_retry: double every wait, 2, 4, 8, 16 and 16 in place of 1, 2, 4, 8 and 16

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L1_ladder_exponent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
            sleep(min(max_delay, base_delay * (2 ** (attempt - 1))))
```

New text:

```
            sleep(min(max_delay, base_delay * (2 ** attempt)))
```

### `u252.L2_ladder_rungs`

DEFAULT_MAX_RETRIES: four rungs in place of five, so a reading waits 15 seconds and asks four times

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L2_ladder_rungs`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
DEFAULT_MAX_RETRIES = 5
```

New text:

```
DEFAULT_MAX_RETRIES = 4
```

### `u252.L3_ladder_ceiling_off_by_one`

fetch_with_retry: re-raise at the ceiling one attempt early

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L3_ladder_ceiling_off_by_one`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
            if attempt > max_retries:
```

New text:

```
            if attempt >= max_retries:
```

### `u252.L4_ladder_cap`

DEFAULT_MAX_DELAY_S: cap a wait at 8 seconds in place of 30, so the last rung waits 8 not 16

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L4_ladder_cap`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
DEFAULT_MAX_DELAY_S = 30.0
```

New text:

```
DEFAULT_MAX_DELAY_S = 8.0
```

### `u252.L5_ladder_base`

DEFAULT_BASE_DELAY_S: halve the first wait, the coefficient of every rung

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L5_ladder_base`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
DEFAULT_BASE_DELAY_S = 1.0
```

New text:

```
DEFAULT_BASE_DELAY_S = 0.5
```

### `u252.L6_no_ladder`

fetch_with_retry: take every failure as not retryable, so a timeout is re-raised at the first attempt with no wait

- File: `src/cratekit/acquire/listing.py`
- Source: `u252.json`, row `L6_no_ladder`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`
- Collected: 46 against a baseline of 46
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
            if isinstance(exc, CratekitError) and not exc.cause.retryable:
```

New text:

```
            if True:
```

### `u65.A2_max_pages_gets_a_default`

the request budget becomes optional and effectively unbounded

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `A2_max_pages_gets_a_default`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.B1_favourites_back_to_the_short_page`

R-383 reintroduced exactly: the favourites walk ends on a short page again

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B1_favourites_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.B2_favourites_back_to_the_empty_page`

the fix as first written: the empty middle window ends the favourites walk

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B2_favourites_back_to_the_empty_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_adapter_listing.py::test_a_permanent_count_failure_still_surfaces_at_the_ceiling`
  - `tests/test_adapter_listing.py::test_a_whole_window_of_unservable_items_does_not_end_the_favourites_walk`
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

### `u65.B3_playlist_tracks_back_to_the_short_page`

the placeholder acquire read ends on a short page, dropping the rest of a playlist

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B3_playlist_tracks_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.B4_account_playlists_back_to_the_short_page`

the sync all listing ends on a short page, silently skipping playlists

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B4_account_playlists_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.B5_artist_releases_back_to_the_short_page`

a label catalogue ends at the first short page, which is the core job done wrong

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `B5_artist_releases_back_to_the_short_page`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/modules/test_labels.py`
- Collected: 266 against a baseline of 266
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

### `u65.C1_the_declared_total_is_ignored`

the total is read and then never consulted, so every walk falls back to a page shape

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C1_the_declared_total_is_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.C2_an_empty_page_ends_a_declared_total_walk`

the empty middle window ends the walk again, the exact defect the review found

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C2_an_empty_page_ends_a_declared_total_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.C3_a_full_page_at_the_declared_end_stops_anyway`

a total that under reports now truncates, because the walk trusts it over what it sees

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C3_a_full_page_at_the_declared_end_stops_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.C4_the_short_page_rule_stops_every_walk`

the rule argument is dropped from the short page test, so every shape stops short

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C4_the_short_page_rule_stops_every_walk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.C6_offset_advances_by_what_was_served`

the plausible wrong fix: advance by the page's length, not the window width, re-serving items

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C6_offset_advances_by_what_was_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.C7_a_zero_total_is_trusted_as_an_end`

the sentinel check goes, so an unparsed num_tracks of -1 ends the walk at once

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `C7_a_zero_total_is_trusted_as_an_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.D5_the_favourites_budget_is_tightened_onto_real_data`

a budget that can fire on a real account, which turns a correctness fix into an outage

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `D5_the_favourites_budget_is_tightened_onto_real_data`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`
- Collected: 86 against a baseline of 86
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

### `u65.E1_the_shape_helper_ignores_the_rule_table`

every shape gets one hard coded rule again, which is R-383's own shape

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E1_the_shape_helper_ignores_the_rule_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.E2_the_shape_helper_ignores_the_page_size_table`

one shared page size, so account playlists is paged at the wrong window width

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E2_the_shape_helper_ignores_the_page_size_table`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.E3_the_favourites_total_is_never_wired`

the shape declares the total rule and is handed no total, so it degrades silently

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E3_the_favourites_total_is_never_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.E4_the_playlist_total_is_never_wired`

the playlist count on the object is ignored, so that shape degrades too

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `E4_the_playlist_total_is_never_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u65.F4_the_favourites_dedup_goes`

U14's dedup: a favourite re-served on a shifted page boundary is returned twice

- File: `src/cratekit/acquire/listing.py`
- Source: `u65.json`, row `F4_the_favourites_dedup_goes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_outbound_tidal_account.py`
- Collected: 197 against a baseline of 197
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

### `u70.E3_hearts_declared_total`

Existing: the favourites walk ends on a page shape instead of the declared count

- File: `src/cratekit/acquire/listing.py`
- Source: `u70.json`, row `E3_hearts_declared_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_listing.py`
- Collected: 260 against a baseline of 260
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

### `r1705.M10_holds_always`

_holds_spelling answers yes for every title, so the lookup offers OK against O.K., U286's split class, where the score did not

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M10_holds_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_lookup_does_not_widen_a_title_split_differently`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return any(word in _SPELLED_OUT for word in title.split())

```

New text:

```
    return True

```

### `r1705.M11_holds_reads_artist`

_holds_spelling reads the artist half of the token rather than the title

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M11_holds_reads_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 38 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    _artist, _separator, title = recording.partition("\x1f")

```

New text:

```
    title, _separator, _artist = recording.partition("\x1f")

```

### `r1705.M12_lookup_ignores_wanted_side`

spelled_alike ignores a listed word in the WANTED title, so 4 U against a held For You for a short artist reads missing

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M12_lookup_ignores_wanted_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-wanted]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2-to]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2day-today]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2morrow-tomorrow]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2nite-tonight]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4-for]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        asks = _holds_spelling(recording)

```

New text:

```
        asks = False

```

### `r1705.M13_lookup_ignores_held_side`

spelled_alike ignores a listed word in the HELD title, so For You against a held 4 U for a short artist reads missing

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M13_lookup_ignores_held_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 25 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-held]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2-to]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2day-today]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2morrow-tomorrow]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2nite-tonight]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4-for]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4ever-forever]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[b4-before]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
            if asks or _holds_spelling(token)

```

New text:

```
            if asks

```

### `r1705.M14_lookup_key_drops_artist`

_spelled_key drops the artist, so a spelled out copy by another artist is offered

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M14_lookup_key_drops_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_out_copy_by_another_artist_is_not_offered`
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return f"{artist}{separator}{_spelled_out(title)}"

```

New text:

```
    return f"{separator}{_spelled_out(title)}"

```

### `r1705.M15_lookup_key_spells_artist`

_spelled_key spells the artist out too, so Lil Kid and Little Kid read as one artist

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M15_lookup_key_spells_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`

Old text:

```
    return f"{artist}{separator}{_spelled_out(title)}"

```

New text:

```
    return f"{_spelled_out(artist)}{separator}{_spelled_out(title)}"

```

### `r1705.M16_lookup_removed`

_resembling never reads the lookup, so a pair the discovery score misses (Prince, 4 U against For You) reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M16_lookup_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 38 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
        for recording in index.spelled_alike(wanted.recording)

```

New text:

```
        for recording in ()

```

### `r1705.M17_lookup_repeats_the_five`

the lookup's hits are not checked against the five scored recordings, so a recording both hold is offered twice

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M17_lookup_repeats_the_five`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
        if recording not in offered

```

New text:

```
(empty)
```

### `r1705.M18_lookup_skips_every_scored`

the lookup skips every recording discovery scored, round two's shape, so a lookup hit ranked sixth is cut by the cap, never offered and never counted withheld

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M18_lookup_skips_every_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    offered = {held.recording for held in scored}

```

New text:

```
    offered = {held.recording for held in _approximate(wanted, index, limit=None)}

```

### `r1705.M19_lookup_after_the_scored`

the lookup's hits follow the scored five rather than leading, so the same title under the reading sits behind fuzzy hits and is truncated

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M19_lookup_after_the_scored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return tuple(looked_up + scored)

```

New text:

```
    return tuple(scored + looked_up)

```

### `r1705.M1_luv_unlisted`

_SPELLED_OUT loses luv, so Luv U against a held Love You reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M1_luv_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-Luv U-Love You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-Luv U-Love You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-Luv U-Love You-slang-wanted]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[luv-love]`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "luv": "love",

```

New text:

```
(empty)
```

### `r1705.M20_lookup_counts_in_the_five`

the lookup's hits are cut to the five with the scored ones, round one's shape, so a scored recording is pushed out with nothing withheld

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M20_lookup_counts_in_the_five`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 38 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
    return tuple(looked_up + scored)

```

New text:

```
    return tuple((looked_up + scored)[: len(scored)])

```

### `r1705.M2_four_numeral_unlisted`

_SPELLED_OUT loses 4, so 4 U against a held For You reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M2_four_numeral_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 14 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Prince-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[4-for]`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "4": "for",

```

New text:

```
(empty)
```

### `r1705.M3_too_unlisted`

_SPELLED_OUT loses too, so Luv U 2 against a held Love You Too reads missing

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M3_too_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-wanted]`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "too": "to",

```

New text:

```
(empty)
```

### `r1705.M4_2nite_unlisted`

_SPELLED_OUT loses 2nite, so 2Nite against Tonight reads missing

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M4_2nite_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_listed_spelling_offers_its_spelled_out_title[2nite-tonight]`
  - `tests/test_match_states.py::test_the_word_list_is_the_curated_one`

Old text:

```
        "2nite": "tonight",

```

New text:

```
(empty)
```

### `r1705.M5_spelled_test_removed`

_agree loses the spelled out equality, so a scored slang pair (Monkey Safari, Luv U against Love You) is dropped by the title test

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M5_spelled_test_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`

Old text:

```
        one.replace(" ", "") == other.replace(" ", "")
        or _spelled_out(one) == _spelled_out(other)

```

New text:

```
        one.replace(" ", "") == other.replace(" ", "")

```

### `r1705.M6_spelled_test_a_ratio`

_agree compares the spelled out forms by fuzz.ratio at the title floor rather than equality, so 2 against Tom (80) and N against Ant are offered

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M6_spelled_test_a_ratio`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 12 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`
  - `tests/test_match_states.py::test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio`

Old text:

```
        or _spelled_out(one) == _spelled_out(other)

```

New text:

```
        or fuzz.ratio(_spelled_out(one), _spelled_out(other)) >= APPROXIMATE_TITLE_FLOOR

```

### `r1705.M7_spelled_replaces_written`

_agree reads only the spelled out form, dropping U286's equality as written, so U Turn against UTurn no longer agrees

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M7_spelled_replaces_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`

Old text:

```
        one.replace(" ", "") == other.replace(" ", "")
        or _spelled_out(one) == _spelled_out(other)

```

New text:

```
        _spelled_out(one) == _spelled_out(other)

```

### `r1705.M8_spelled_keeps_spaces`

_spelled_out joins the words with a space, so 2 Nite against Tonight is no longer one string

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M8_spelled_keeps_spaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Monkey Safari-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return "".join(_SPELLED_OUT.get(word, word) for word in folded.split())

```

New text:

```
    return " ".join(_SPELLED_OUT.get(word, word) for word in folded.split())

```

### `r1705.M9_spelled_spells_nothing`

_spelled_out spells no word out, so the reading and the lookup join nothing the written form does not

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `M9_spelled_spells_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 52 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_slang_title_through_the_real_verb_is_asked_and_not_downloaded`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-2 Nite-Tonight-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4 U-For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-4Ever-Forever-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-B4 U Go-Before You Go-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-B4 U Go-Before You Go-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-held]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-I Would Die 4 U-I Would Die For You-slang-wanted]`
  - `tests/test_match_states.py::test_a_title_in_slang_or_numerals_is_offered_its_spelled_out_copy[Aurora Bloom-Luv U 2-Love You Too-slang-held]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    return "".join(_SPELLED_OUT.get(word, word) for word in folded.split())

```

New text:

```
    return "".join(word for word in folded.split())

```

### `r1705.S1_discovery_floor_raised`

SAMPLED existing guard: APPROXIMATE_FLOOR raised from 82 to 90, so fewer near hits are discovered

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `S1_discovery_floor_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Every Day-Everyday]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Good Bye-Goodbye]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Hi Fi-HiFi]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 90

```

### `r1705.S2_unreadable_title_dropped`

SAMPLED existing guard: _title_resembles answers no for a title that folds to nothing, so a hit discovery found reads missing

- File: `src/cratekit/acquire/match.py`
- Source: `r1705.json`, row `S2_unreadable_title_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[!!!-Sun]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[Sun-!!!]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
    if not asked or not found:
        return True

```

New text:

```
    if not asked or not found:
        return False

```

### `r1709.M10_title_identity_no_separator`

title_identity returns the bare text with no separator, so it can equal another title's fold

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M10_title_identity_no_separator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`

Old text:

```
    return f"\x1f{bare}" if bare else ""

```

New text:

```
    return bare

```

### `r1709.M11_recording_identity_is_the_token`

recording_identity reads the title by fold, the base's token, so every identity collapses again

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M11_recording_identity_is_the_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 24 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_two_emoji_titles_by_one_artist_played_back_to_back_stay_two_rows`
  - `tests/intake/test_workers.py::test_two_recognised_emoji_titles_by_one_artist_are_two_items`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact`
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

### `r1709.M12_held_exact_unfiltered`

LibraryIndex.held keeps every file under the token, so a held fire emoji owns a wanted drop

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M12_held_exact_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 14 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[!!!-!!]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[!!!-???]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\U0001f44d-\U0001f44d\U0001f3fd]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\U0001f4a7-\U0001f525]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\U0001f525-]`
  - `tests/test_match_states.py::test_two_titles_that_fold_to_nothing_and_differ_are_not_one_title[\u2764-\u2665]`

Old text:

```
            if one.distinct == distinct

```

New text:

```
            if True

```

### `r1709.M13_held_credited_by_fold`

the credited list rule compares the fold alone again

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M13_held_credited_by_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`
  - `tests/test_match_states.py::test_the_wanted_emoji_title_is_owned_beside_another_one_the_library_holds`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
            if same_title(one.title, title) and member in one.members

```

New text:

```
            if member in one.members

```

### `r1709.M14_isrc_settled_by_fold`

the ISRC branch settles a file under another emoji title by the fold

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M14_isrc_settled_by_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`

Old text:

```
    settled = [held for held in carrying if same_title(held.title, wanted.title)]
    doubtful = [held for held in carrying if not same_title(held.title, wanted.title)]

```

New text:

```
    settled = [held for held in carrying if fold(held.title) == fold(wanted.title)]
    doubtful = [held for held in carrying if fold(held.title) != fold(wanted.title)]

```

### `r1709.M15_same_recording_title_guard`

_same_recording no longer reads the title, so an emoji candidate offered for another reads exact

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M15_same_recording_title_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_approximate_hit_is_a_question_and_never_a_match`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`

Old text:

```
    if not same_title(held.title, wanted.title):
        return False
    if held.distinct
```

New text:

```
    if False:
        return False
    if held.recording
```

### `r1709.M16_candidates_grouped_by_token`

_candidates_for groups by the token, so two held emoji files are one candidate carrying both paths

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M16_candidates_grouped_by_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
        grouped.setdefault((held.distinct, held.version_key, held.key_key), []).append(held)

```

New text:

```
        grouped.setdefault((held.recording, held.version_key, held.key_key), []).append(held)

```

### `r1709.M17_question_identity_token`

the review item hashes the token, so a held emoji row retires another's question and one answer settles both

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M17_question_identity_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`

Old text:

```
        "recording": recording_identity(artist, title),

```

New text:

```
        "recording": recording_token(artist, title),

```

### `r1709.M18_match_id_token`

match_id hashes the token, so intake missing drops a second emoji row as a line listed twice

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M18_match_id_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_two_emoji_rows_are_each_searched_and_listed`
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`
  - `tests/test_match_states.py::test_two_emoji_rows_in_one_list_carry_two_match_identifiers`

Old text:

```
            f"mt_{_digest(self.wanted.distinct, self.wanted.version_key, self.wanted.key_key)}"

```

New text:

```
            f"mt_{_digest(self.wanted.recording, self.wanted.version_key, self.wanted.key_key)}"

```

### `r1709.M19_search_option_token`

the search acquisition option hashes the token

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M19_search_option_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_emoji_titles_identities_are_its_own`

Old text:

```
option_id=f"aq_{_digest(BY_SEARCH, wanted.distinct, wanted.version_key)}",
```

New text:

```
option_id=f"aq_{_digest(BY_SEARCH, wanted.recording, wanted.version_key)}",
```

### `r1709.M1_bare_no_nfkc`

bare_title composes with NFC rather than NFKC, so a title of fullwidth marks or an ellipsis is a different title and a real duplicate is offered rather than owned

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M1_bare_no_nfkc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[ellipsis]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[width]`

Old text:

```
    composed = unicodedata.normalize("NFKC", str(title))

```

New text:

```
    composed = unicodedata.normalize("NFC", str(title))

```

### `r1709.M20_current_option_no_title`

current_option carries a former identifier without its title, so an answer about a fire emoji answers for a snow emoji held in its place

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M20_current_option_no_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`

Old text:

```
        if _former_candidate_id(one) == option and same_title(one.title, title)

```

New text:

```
        if _former_candidate_id(one) == option

```

### `r1709.M21_current_option_never_carries`

current_option never carries, so every answer recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M21_current_option_never_carries`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`

Old text:

```
    return carried[0].candidate_id if carried else option

```

New text:

```
    return option

```

### `r1709.M3_bare_keeps_spaces`

bare_title keeps spacing, so ? ? and ?? are two titles and a real duplicate is not owned

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M3_bare_keeps_spaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[spacing]`

Old text:

```
    return "".join(ch for ch in composed if not ch.isspace() and not _invisible(ch))

```

New text:

```
    return "".join(ch for ch in composed if not _invisible(ch))

```

### `r1709.M4_bare_keeps_invisible`

bare_title keeps every invisible character, so a variation selector or a joiner makes one title two

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M4_bare_keeps_invisible`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_the_same_emoji_title_is_exact`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[joiner]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[selector]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[text-and-emoji]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[zero-width-space]`

Old text:

```
    return "".join(ch for ch in composed if not ch.isspace() and not _invisible(ch))

```

New text:

```
    return "".join(ch for ch in composed if not ch.isspace())

```

### `r1709.M5_no_variation_selectors`

_invisible no longer drops the variation selectors, so the heart with and without its emoji presentation are two titles

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M5_no_variation_selectors`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_the_same_emoji_title_is_exact`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[selector]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[text-and-emoji]`

Old text:

```
    if any(point in selectors for selectors in _VARIATION_SELECTORS):
        return True

```

New text:

```
    if False:
        return True

```

### `r1709.M6_no_format_characters`

_invisible no longer drops format characters, so a zero width joiner or space makes one title two

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M6_no_format_characters`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[joiner]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_spelled_another_way_is_still_owned[zero-width-space]`

Old text:

```
    return unicodedata.category(ch) == "Cf" and point not in _TAG_CHARACTERS

```

New text:

```
    return False

```

### `r1709.M7_tag_characters_dropped`

_invisible drops the tag characters too, so England and Scotland flags are one title

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M7_tag_characters_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_two_flags_are_two_titles`

Old text:

```
    return unicodedata.category(ch) == "Cf" and point not in _TAG_CHARACTERS

```

New text:

```
    return unicodedata.category(ch) == "Cf"

```

### `r1709.M8_bare_for_every_title`

bare_title returns text for a title that folds to something too

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M8_bare_for_every_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_that_folds_to_something_compares_exactly_as_it_did`

Old text:

```
    if fold(title):
        return ""
    composed
```

New text:

```
    if False:
        return ""
    composed
```

### `r1709.M9_title_identity_is_the_fold`

title_identity returns the fold alone, the base's reading, so an emoji title is every other one by the artist

- File: `src/cratekit/acquire/match.py`
- Source: `r1709.json`, row `M9_title_identity_is_the_fold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 30 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_two_emoji_titles_by_one_artist_played_back_to_back_stay_two_rows`
  - `tests/intake/test_workers.py::test_two_recognised_emoji_titles_by_one_artist_are_two_items`
  - `tests/test_acquire_fallback.py::test_an_upload_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_a_search_answered_by_another_emoji_title_is_not_exact`
  - `tests/test_intake_missing_search.py::test_a_search_question_about_one_emoji_title_is_not_another_ones`
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

### `r431-b.B1_a_wanted_built_by_hand_asks`

uncredited_spellings no longer requires a spelled title, so a Wanted built from a held file asks for a companion

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B1_a_wanted_built_by_hand_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_wanted_nobody_read_from_a_listing_never_asks_for_a_companion`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if self.several_artists or _credits_in(self.listed):
```

### `r431-b.B2_a_row_billing_a_guest_asks`

uncredited_spellings ignores several_artists, so a row crediting a guest in its artists list asks

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B2_a_row_billing_a_guest_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_match_states.py::test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or _credits_in(self.spelled):
```

### `r431-b.B3_a_listing_that_spelled_a_credit_asks`

uncredited_spellings ignores a bracketed credit, so a listing crediting Zed reaches Mira's companion

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B3_a_listing_that_spelled_a_credit_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (with Zed) - Nightwave Remix]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path [ft. Zed] [Nightwave Remix]]`

Old text:

```
        if not self.spelled or self.several_artists or _credits_in(self.spelled):
```

New text:

```
        if not self.spelled or self.several_artists:
```

### `r431-b.B4_the_engine_never_asks`

standing_tombstone asks under the companion kind for nothing, which is the defect the unit closes

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B4_the_engine_never_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_provider_row_crediting_somebody_else_is_not_withheld`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`

Old text:

```
    for identity in wanted.uncredited_spellings:
        if suppresses(UNCREDITED_KIND, identity):
```

New text:

```
    for identity in ():
        if suppresses(UNCREDITED_KIND, identity):
```

### `r431-b.B5_the_engine_ignores_companions_false`

standing_tombstone asks for a companion even when the caller said not to

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B5_the_engine_ignores_companions_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`

Old text:

```
    if not companions:
        return None
    for identity in wanted.uncredited_spellings:
```

New text:

```
    for identity in wanted.uncredited_spellings:
```

### `r431-b.B7_the_engine_asks_under_the_tombstones_kind`

The engine's copy of the companion kind drifts onto the tombstone's own

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B7_the_engine_asks_under_the_tombstones_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_provider_row_crediting_somebody_else_is_not_withheld`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`

Old text:

```
UNCREDITED_KIND = "version-uncredited"
```

New text:

```
UNCREDITED_KIND = "version"
```

### `r431-b.B8_the_reader_never_counts_the_artists`

_from_row stops setting several_artists, so every provider row reads as billing one

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B8_the_reader_never_counts_the_artists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_match_states.py::test_a_provider_row_billing_a_guest_in_its_artists_never_asks_for_a_companion`

Old text:

```
        several_artists=_bills_several(row),
```

New text:

```
        several_artists=False,
```

### `r664.E1_stem_head_kept`

Stop stripping the head from the stem, the filename half of the same rule

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `E1_stem_head_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
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

### `r664.E2_pair_rule_field_by_field`

Collapse the pair rule to field by field fallback, the shape that assembled an identity matching neither source

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `E2_pair_rule_field_by_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_half_tagged_file_does_not_get_an_identity_matching_neither_source`

Old text:

```
    if tagged_artist and tagged_title:
        artist, spelled = tagged_artist, tagged_title
    elif named_artist and named_title:
        artist, spelled = named_artist, named_title
    else:
        artist, spelled = tagged_artist or named_artist, tagged_title or named_title

```

New text:

```
    artist, spelled = tagged_artist or named_artist, tagged_title or named_title

```

### `r664.E4_title_not_split`

Skip split_title on the chosen title, so a version stays inside the recording token

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `E4_title_not_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 120 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_resume_that_redoes_an_offered_item_asks_nothing_twice`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_and_no_intake_file_is_written`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_favorites_resolves_each_heart_owned_offered_or_missing`
  - `tests/intake/test_workers.py::test_identify_reports_an_owned_track_owned_an_offered_one_offered_and_the_rest_missing`
  - `tests/intake/test_workers.py::test_the_missing_hearts_carry_the_provider_id_acquisition_reads`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`
  - `tests/intake/test_workers.py::test_the_resolution_names_owned_offered_and_missing_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - ... and 105 more, see the JSON sidecar

Old text:

```
    title, version = split_title(spelled)

```

New text:

```
    title, version = spelled, ""

```

### `r664.G5_key_not_read_from_the_tag_head`

Stop reading the key off a head found only inside the title tag, the first draft's precedence the review reversed

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `G5_key_not_read_from_the_tag_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none`
  - `tests/test_match_states.py::test_the_stem_head_outranks_the_tag_head_and_both_outrank_the_initialkey_tag`

Old text:

```
    written_key = head.get("key") or tag_head.get("key")

```

New text:

```
    written_key = head.get("key")

```

### `r664.G6_tag_head_outranks_stem_head`

Let the head inside the tag outrank the head in the filename

- File: `src/cratekit/acquire/match.py`
- Source: `r664.json`, row `G6_tag_head_outranks_stem_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1298 against a baseline of 1298
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_stem_head_outranks_the_tag_head_and_both_outrank_the_initialkey_tag`

Old text:

```
    written_key = head.get("key") or tag_head.get("key")

```

New text:

```
    written_key = tag_head.get("key") or head.get("key")

```

### `r667-b.B1_same_recording_no_isrc`

_same_recording: the ISRC clause removed, r667's G11 after its direct test

- File: `src/cratekit/acquire/match.py`
- Source: `r667-b.json`, row `B1_same_recording_no_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`

Old text:

```
    return fold(wanted.artist) in held.members or _carries(held, token)
```

New text:

```
    return fold(wanted.artist) in held.members
```

### `r667-b.B2_reader_isrc_unfolded`

_read_from_disk: the ISRC tag carried verbatim, r667's G18 after its direct tests

- File: `src/cratekit/acquire/match.py`
- Source: `r667-b.json`, row `B2_reader_isrc_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_malformed_isrc_tag_is_not_an_identity`

Old text:

```
        isrc=isrc_token(read["isrc"]),
```

New text:

```
        isrc=str(read["isrc"] or ""),
```

### `r667.E1_title_head_kept`

Existing: _read_from_disk takes the title tag verbatim, the R-664 defect

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `E1_title_head_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 33 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_track_held_under_a_headed_title_tag_is_owned_and_nothing_is_listed`
  - `tests/test_intake_missing.py::test_a_track_held_under_the_rows_isrc_is_owned_and_nothing_is_listed`
  - `tests/test_intake_missing.py::test_a_track_held_with_no_isrc_under_a_credited_list_is_owned_and_nothing_is_listed`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_head_found_only_in_the_tag_carries_the_key_when_the_stem_has_none`
  - `tests/test_match_states.py::test_a_head_inside_the_title_tag_is_stripped_so_a_plain_provider_row_matches`
  - `tests/test_match_states.py::test_a_head_written_as_a_suffix_inside_the_tag_comes_off_as_it_does_from_the_stem`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_headed_tag_with_a_lossy_marker_strips_under_the_librarys_template`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    tagged_title = naming.strip_heads(spelled_tag, template=template)
```

New text:

```
    tagged_title = spelled_tag
```

### `r667.E2_first_copy_only`

Existing: resolve_one reads the key off the first held copy only

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `E2_first_copy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}
```

### `r667.F1_credited_reason_is_exact`

resolve_one: a credited list hit reports exact, so the report claims a token agreement that did not happen

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F1_credited_reason_is_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`

Old text:

```
            else Why.CREDITED_EXACT
```

New text:

```
            else Why.EXACT
```

### `r667.F2_isrc_version_not_settled`

_candidates_for: an ISRC hit at another version spelling is a version question on the candidate beside a key question on the match

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F2_isrc_version_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`

Old text:

```
        elif version_key != wanted.version_key and not _carries(first, token):
```

New text:

```
        elif version_key != wanted.version_key:
```

### `r667.F3_doubtful_not_offered`

resolve_one: an ISRC hit whose title disagrees is not offered, so it falls through to missing or a scored hit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F3_doubtful_not_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`

Old text:

```
    if doubtful:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
```

New text:

```
    if False:
        # The ISRC agrees and the title does not, see above. Asked, not assumed.
```

### `r667.F4_text_copy_joins_isrc_paths`

resolve_one: a text matched copy at the wanted version joins an ISRC settled row's paths and key check

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `F4_text_copy_joins_isrc_paths`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`

Old text:

```
    if settled:
        exact, agreed = settled, Why.ISRC_EXACT
```

New text:

```
    if settled:
        exact = settled + [held for held in owned if held.version_key == wanted.version_key and held.path not in {one.path for one in settled}]
        agreed = Why.ISRC_EXACT
```

### `r667.G12_same_recording_no_credit`

_same_recording: a credited hit at another version is title-approximate, not version-differs

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G12_same_recording_no_credit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`

Old text:

```
    return fold(wanted.artist) in held.members or _carries(held, token)
```

New text:

```
    return _carries(held, token)
```

### `r667.G13_isrc_not_consulted`

resolve_one: never ask the index by ISRC, the engine before this unit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G13_isrc_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 16 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - `tests/test_match_states.py::test_an_isrc_under_another_artist_and_another_emoji_title_is_asked`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    carrying = index.held_by_isrc(isrc_token(wanted.isrc))
```

New text:

```
    carrying = ()
```

### `r667.G15_isrc_hit_skips_key`

resolve_one: an ISRC hit is matched before the key check runs

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G15_isrc_hit_skips_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None}:
```

New text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}
        if disagreements == {None} or settled:
```

### `r667.G16_isrc_reason_is_exact`

resolve_one: an ISRC hit reports the text reason, so the report claims an agreement that did not happen

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G16_isrc_reason_is_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 11 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - `tests/test_match_states.py::test_the_verb_lists_a_retired_question_only_when_asked_for_everything`

Old text:

```
        exact, agreed = settled, Why.ISRC_EXACT
```

New text:

```
        exact, agreed = settled, Why.EXACT
```

### `r667.G17_reader_drops_isrc`

_read_from_disk: the ISRC tag is read and not carried, so the index has nothing to be asked by

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G17_reader_drops_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 17 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_held_under_the_rows_isrc_is_owned_whatever_its_artist_tag_says`
  - `tests/test_match_states.py::test_a_files_isrc_tag_is_folded_before_it_is_indexed`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_retired_question_offered_again_is_neither_reopened_nor_duplicated`
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`
  - `tests/test_match_states.py::test_a_retired_question_whose_row_goes_missing_keeps_the_verdict`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[isrc-exact]`
  - `tests/test_match_states.py::test_a_rows_isrc_is_folded_before_it_is_asked`
  - `tests/test_match_states.py::test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing`
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_title_disagrees_is_a_question_not_a_match`
  - `tests/test_match_states.py::test_an_isrc_on_a_file_under_another_emoji_title_is_asked_not_settled`
  - `tests/test_match_states.py::test_an_isrc_settled_row_lists_the_files_carrying_the_isrc_and_no_other`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        isrc=isrc_token(read["isrc"]),
```

New text:

```
        isrc="",
```

### `r667.G3_members_not_split`

credited_members: a comma separated tag is one name, so nobody is a member

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G3_members_not_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_track_held_with_no_isrc_under_a_credited_list_is_owned_and_nothing_is_listed`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`
  - `tests/test_match_states.py::test_the_primary_artist_need_not_be_first_in_the_credited_list`

Old text:

```
    return tuple(part for part in (piece.strip() for piece in str(artist).split(",")) if part)
```

New text:

```
    return (str(artist).strip(),) if str(artist).strip() else ()
```

### `r667.G4_members_not_folded`

Owned.members: the credited names unfolded, so case and marks decide membership

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G4_members_not_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 5 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_a_single_artist_file_is_indexed_once_and_the_rule_moves_nothing`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`

Old text:

```
            self, "members", frozenset(fold(name) for name in credited_members(self.artist))
```

New text:

```
            self, "members", frozenset(credited_members(self.artist))
```

### `r667.G5_empty_isrc_asks`

held_by_isrc: an empty token asks the map instead of answering nothing

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G5_empty_isrc_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_empty_isrc_token_asks_the_index_nothing`

Old text:

```
        return self.by_isrc.get(isrc, ()) if isrc else ()
```

New text:

```
        return self.by_isrc.get(isrc, ())
```

### `r667.G8_no_credited_rule`

held: the recording token alone, the rule every caller had before this unit

- File: `src/cratekit/acquire/match.py`
- Source: `r667.json`, row `G8_no_credited_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_intake_missing.py`, `tests/test_tags.py`
- Collected: 729 against a baseline of 729
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_track_held_with_no_isrc_under_a_credited_list_is_owned_and_nothing_is_listed`
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_file_with_no_isrc_tag_is_owned_when_the_primary_artist_is_a_credited_member`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`
  - `tests/test_match_states.py::test_the_credited_list_rule_tells_two_emoji_titles_apart`
  - `tests/test_match_states.py::test_the_primary_artist_need_not_be_first_in_the_credited_list`

Old text:

```
        return exact + credited
```

New text:

```
        return exact
```

### `r679-b.C1_credited_rule_not_owning`

OWNING_RULES: leave the credited rule out, so its 4 items stay open

- File: `src/cratekit/acquire/match.py`
- Source: `r679-b.json`, row `C1_credited_rule_not_owning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_persons_acceptance_being_applied_retires_nothing`
  - `tests/test_match_states.py::test_a_row_owned_by_a_later_resolution_retires_its_open_question_naming_the_rule[credited-exact]`

Old text:

```
OWNING_RULES: frozenset[Why] = frozenset({Why.EXACT, Why.ISRC_EXACT, Why.CREDITED_EXACT})
```

New text:

```
OWNING_RULES: frozenset[Why] = frozenset({Why.EXACT, Why.ISRC_EXACT})
```

### `r679-b.C2_reading_shape_missing`

QUESTION_SHAPES: leave the reading shape out, so a reading question is never retired

- File: `src/cratekit/acquire/match.py`
- Source: `r679-b.json`, row `C2_reading_shape_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_question_identity_is_one_per_shape_and_agrees_with_the_asked_one`

Old text:

```
    ASKS_ABOUT_RECORDING,
    ASKS_ABOUT_READING,
)
```

New text:

```
    ASKS_ABOUT_RECORDING,
)
```

### `u16-round-8-independent-composites.V24_approximate_limit_raised`

APPROXIMATE_LIMIT coefficient raised from 5 to 10; every test referencing it compares against match.APPROXIMATE_LIMIT itself, so the hunt predicts the value can drift green

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent-composites.json`, row `V24_approximate_limit_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 10 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_at_most_the_declared_number_of_approximate_candidates_is_offered`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
APPROXIMATE_LIMIT = 5

```

New text:

```
APPROXIMATE_LIMIT = 10

```

### `u16-round-8-independent.V11_candidate_order_sorted`

Candidate groups iterate sorted instead of insertion order, so the approximate offer truncates the best hit instead of the worst

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V11_candidate_order_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
    for recording, version_key, key in grouped:

```

New text:

```
    for recording, version_key, key in sorted(grouped):

```

### `u16-round-8-independent.V12_approximate_floor_halved`

APPROXIMATE_FLOOR coefficient halved from 82 to 41, admitting resemblances the unit exists to keep out of the offer

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V12_approximate_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 13 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_resemblance_below_the_floor_is_missing_rather_than_a_question`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - `tests/test_match_states.py::test_an_isrc_hit_on_an_abbreviated_title_is_still_asked_about`
  - `tests/test_match_states.py::test_an_unrelated_title_by_another_artist_is_still_not_offered`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_lookup_is_what_reaches_a_pair_discovery_cannot_score`
  - `tests/test_match_states.py::test_the_lookup_reads_the_artist_as_it_folds_and_never_spelled_out`

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 41

```

### `u16-round-8-independent.V13_withheld_not_reported`

The truncated approximate offer stops saying how many candidates were withheld, so a rejection rejects answers never shown

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V13_withheld_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - `tests/test_match_states.py::test_the_withheld_warning_survives_onto_the_run_that_actually_acquires`

Old text:

```
            withheld=max(len(offered) - APPROXIMATE_LIMIT, 0),

```

New text:

```
            withheld=0,

```

### `u16-round-8-independent.V14_tombstone_fold_nfd`

tombstone_fold normalizes NFD instead of NFC, drifting from U24's byte-for-byte algorithm so a recorded suppression can never be found

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V14_tombstone_fold_nfd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_composed_address_still_matches_a_row_spelled_that_way[Caf\xe9 del Mar-Track-Live]`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Caf\xe9 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_tombstone_fold_is_pinned_where_two_normalizations_disagree['Cafe\u0301 del Mar'-'caf\xe9 del mar']`
  - `tests/test_match_states.py::test_the_two_copies_of_the_tombstone_identity_agree_once_both_exist`

Old text:

```
        " ", unicodedata.normalize("NFC", str(value)).casefold()

```

New text:

```
        " ", unicodedata.normalize("NFD", str(value)).casefold()

```

### `u16-round-8-independent.V15_empty_identity_accepted`

The empty tombstone identity refusal removed alone, so every unnamed candidate collides onto one suppression

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V15_empty_identity_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_identity_with_neither_an_artist_nor_a_title_is_refused`

Old text:

```
    if not folded_artist and not folded_title:

```

New text:

```
    if False:

```

### `u16-round-8-independent.V16_key_leaves_item_identity`

The list's key leaves the review item identity, so one answer settles the key question and the version question both

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V16_key_leaves_item_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_review_item_identity_is_not_the_tombstone_identity`

Old text:

```
        "key": key_token(key),

```

New text:

```
        "key": "",

```

### `u16-round-8-independent.V18_rejection_skips_tombstones`

A rejection stops consulting the tombstones, so a rejected question hands acquisition a version standing under a tombstone (R36)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V18_rejection_skips_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_rejecting_a_question_about_a_tombstoned_version_does_not_hand_it_to_acquisition`
  - `tests/test_match_states.py::test_rejecting_an_ambiguous_reading_can_skip_rather_than_acquire`

Old text:

```
        standing = standing_tombstone(
            found.wanted, suppresses=suppresses, suppression_id=suppression_id
        )

```

New text:

```
        standing = None

```

### `u16-round-8-independent.V19_unbound_yes_takes_todays_candidate`

An unspecific yes stops being bound to the candidate it was given about and accepts whatever the library holds today

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V19_unbound_yes_takes_todays_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`

Old text:

```
            chosen = [c for c in found.candidates if c.candidate_id == about]

```

New text:

```
            chosen = list(found.candidates)

```

### `u16-round-8-independent.V1_key_check_first_copy_only`

Exact branch reads only the first held copy's key, so an unkeyed copy that sorts first answers the key question for a keyed one

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V1_key_check_first_copy_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_relative_key_wins_the_reporting_when_both_disagreements_are_present`

Old text:

```
        disagreements = {key_disagreement(wanted.key, held.key) for held in exact}

```

New text:

```
        disagreements = {key_disagreement(wanted.key, exact[0].key)}

```

### `u16-round-8-independent.V20_digest_width_halved`

DIGEST_WIDTH coefficient halved from 16 to 8 hex characters, dropping identifier collision resistance from 64 to 32 bits

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V20_digest_width_halved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_declared_width_survives_a_population_a_narrower_one_does_not`
  - `tests/test_match_states.py::test_the_digest_width_is_the_narrowest_one_that_meets_the_requirement`

Old text:

```
DIGEST_WIDTH = 16

```

New text:

```
DIGEST_WIDTH = 8

```

### `u16-round-8-independent.V21_suppression_asked_one_spelling`

The tombstone store is asked under one spelling instead of every spelling a version could be recorded under, re-acquiring deletions recorded from another spelling

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V21_suppression_asked_one_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_stale_tombstone_is_reported_under_every_spelling_the_match_consults`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path - nightwave remix]`
  - `tests/test_match_states.py::test_a_tombstone_under_a_spelling_the_composition_never_produces_is_found[sun path [nightwave remix]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path [Original Version]]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path (Original Mix)-Sun Path]`
  - `tests/test_match_states.py::test_the_two_spellings_of_no_qualifier_at_all_reach_each_other[Sun Path-Sun Path (Original Mix)]`

Old text:

```
    for identity in wanted.suppression_spellings:

```

New text:

```
    for identity in (wanted.identity,):

```

### `u16-round-8-independent.V3_version_differs_silently_joins`

A recording owned only at another version resolves MATCHED instead of needs review, the silent join R11 forbids

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V3_version_differs_silently_joins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 41 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_hit_at_another_version_is_a_version_question_not_an_approximate_one`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Feature Edit]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Featureless Dub]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Withdrawn Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Within Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Without You Remix]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_persons_acceptance_being_applied_retires_nothing`
  - `tests/test_match_states.py::test_a_persons_answer_is_never_overwritten_by_a_later_resolution`
  - `tests/test_match_states.py::test_a_question_answered_from_one_source_is_never_asked_again_from_another`
  - `tests/test_match_states.py::test_a_rejected_question_makes_the_track_missing_rather_than_matched`
  - `tests/test_match_states.py::test_a_rejected_verdict_leaves_a_missing_row_that_says_what_to_go_and_get`
  - ... and 26 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.VERSION_DIFFERS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.VERSION_DIFFERS,

```

### `u16-round-8-independent.V5_ambiguous_reading_promoted`

The other-reading question resolves MATCHED, reporting ownership of a record nobody checked

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V5_ambiguous_reading_promoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
            state=MatchState.NEEDS_REVIEW,
            why=Why.READING_AMBIGUOUS,

```

New text:

```
            state=MatchState.MATCHED,
            why=Why.READING_AMBIGUOUS,

```

### `u16-round-8-independent.V6_reading_question_never_asked`

The other-reading guard layer removed alone: the question is never asked and the row falls through to approximate or missing

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V6_reading_question_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Dub]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Extended]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Instrumental]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Live]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Remix]`
  - `tests/test_match_states.py::test_a_tombstone_over_the_file_being_offered_as_the_answer_is_reported`
  - `tests/test_match_states.py::test_a_verdict_survives_the_rename_that_flips_the_reading`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[acapella]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[alternate]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[club]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[cut]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[flip]`
  - `tests/test_match_states.py::test_a_word_only_the_domain_vocabulary_knew_no_longer_re_acquires_a_held_file[interlude]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    confirming = _other_reading_the_library_holds(wanted, index)

```

New text:

```
    confirming = None

```

### `u16-round-8-independent.V7_tombstoned_counted_missing`

Resolution never consults the tombstones, so a suppressed version reports MISSING with acquisition options and the deletion is undone (R36)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V7_tombstoned_counted_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 28 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_suppressed_track_is_in_none_of_the_three_arrays`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    standing = standing_tombstone(
        wanted, suppresses=suppresses, suppression_id=suppression_id
    )

```

New text:

```
    standing = None

```

### `u16-round-8-independent.V8_missing_without_options`

A missing row carries no acquisition options, so the review queue item has nothing to offer (R12)

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V8_missing_without_options`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_missing_track_carries_its_options_as_data_rather_than_as_a_question`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[ambiguous-dash]`
  - `tests/test_match_states.py::test_every_identifier_this_module_generates_is_the_declared_width`
  - `tests/test_match_states.py::test_the_dash_spelling_re_acquires_a_deleted_version_and_says_nothing_about_it`

Old text:

```
        acquisitions=acquisition_options(wanted),

```

New text:

```
        acquisitions=(),

```

### `u16-round-8-independent.V9_relative_key_by_letter`

Relative major or minor detected by matching letter instead of matching wheel number, so 8A vs 8B reads as outright disagreement and 8A vs 9A as relative

- File: `src/cratekit/acquire/match.py`
- Source: `u16-round-8-independent.json`, row `V9_relative_key_by_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 11 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_relative_key_disagreement_surfaces_rather_than_picking_one`
  - `tests/test_match_states.py::test_a_version_answer_never_settles_a_key_question_about_the_same_line`
  - `tests/test_match_states.py::test_an_isrc_hit_at_another_version_spelling_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_isrc_hit_still_asks_about_the_key`
  - `tests/test_match_states.py::test_an_isrc_hit_whose_artist_tag_credits_nobody_the_row_names_still_asks_about_the_key_alone`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[differs-then-relative]`
  - `tests/test_match_states.py::test_an_unspecific_yes_about_one_copy_does_not_settle_a_question_about_another[relative-then-differs]`
  - `tests/test_match_states.py::test_one_answered_key_question_never_settles_another_one`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-first]`
  - `tests/test_match_states.py::test_the_key_check_reads_every_held_copy_rather_than_whichever_sorted_first[sorts-last]`

Old text:

```
    return Why.KEY_RELATIVE if left[0] == right[0] else Why.KEY_DIFFERS

```

New text:

```
    return Why.KEY_RELATIVE if left[1] == right[1] else Why.KEY_DIFFERS

```

### `u213.M1_first_group_is_the_title`

split_version: drop the first group rule, so a title written wholly in brackets walks off whole and the row names no title

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M1_first_group_is_the_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
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

### `u213.M21_first_group_version_check`

split_version: drop the version check from the first group rule, so a row titled only (Extended) reads as the title Extended and the emitter writes it

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M21_first_group_version_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/intake/test_workers.py`
- Collected: 778 against a baseline of 778
- Kills: 6 (killed)
- Killed:
  - `tests/test_listdoc.py::test_a_row_the_reader_would_refuse_is_refused_by_the_emitter[only-a-version]`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Extended)-expected14]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Original Mix] (Remastered)-expected15]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches Live]-expected16]`

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
```

New text:

```
        if found.start() == 0:
```

### `u213.M22_names_a_version_last_word`

_names_a_version: read the group's first word rather than its last

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M22_names_a_version_last_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_listdoc.py`, `tests/intake/test_workers.py`
- Collected: 778 against a baseline of 778
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches Live]-expected16]`

Old text:

```
    return bool(words) and words[-1] in _DASH_VERSIONS
```

New text:

```
    return bool(words) and words[0] in _DASH_VERSIONS
```

### `u213.M3_first_group_position`

split_version: take any group as the title, not only the one standing first, so Song (Remix) reads as Remix

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M3_first_group_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
- Kills: 16 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_of_two_near_hits_only_the_one_whose_title_resembles_is_offered`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
```

New text:

```
        if found.start() >= 0 and not _names_a_version(inside):
```

### `u213.M4_first_group_keeps_brackets`

split_version: keep the brackets on a title written wholly in them

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M4_first_group_keeps_brackets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
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

### `u213.M5_listed_names_artist`

listed_names: read no artist off a refused row

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M5_listed_names_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
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

### `u249.M01_path_alone`

_read_from_disk: answer any remembered path whatever its stamp, the path alone as identity

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M01_path_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 7 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and True

```

### `u249.M02_size_out_of_stamp`

_read_from_disk: compare the stamp without its size

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M02_size_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[1:] == stamp[1:]

```

### `u249.M03_mtime_out_of_stamp`

_read_from_disk: compare the stamp without its modification time

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M03_mtime_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_modification_time_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:1] + entry.stamp[2:] == stamp[:1] + stamp[2:]

```

### `u249.M04_ctime_out_of_stamp`

_read_from_disk: compare the stamp without its change time, so a restore tool's old time over new bytes is answered from memory

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M04_ctime_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_restore_that_puts_the_old_size_and_time_back_is_read_again_on_its_change_time`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:2] + entry.stamp[3:] == stamp[:2] + stamp[3:]

```

### `u249.M05_inode_out_of_stamp`

_read_from_disk: compare the stamp without its inode

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M05_inode_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_swapped_in_under_the_same_name_size_and_times_is_read_again_on_its_inode`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:3] + entry.stamp[4:] == stamp[:3] + stamp[4:]

```

### `u249.M06_device_out_of_stamp`

_read_from_disk: compare the stamp without its device

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M06_device_out_of_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`

Old text:

```
            and entry.stamp == stamp

```

New text:

```
            and entry.stamp[:4] == stamp[:4]

```

### `u249.M07_size_not_stat`

_stamp_of: stamp a constant in place of the file's size

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M07_size_not_stat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 2 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_with_a_new_size_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return (0, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

### `u249.M08_template_out_of_key`

_read_from_disk: key the memory on the path alone, so an entry parsed under one name template answers another

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M08_template_out_of_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_name_template_is_part_of_the_key`

Old text:

```
    key = (path, template)
```

New text:

```
    key = (path, None)
```

### `u249.M09_no_window`

_read_from_disk: answer an equal stamp from memory however recent the file's modification time

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M09_no_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 4 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_to_the_same_size_inside_the_window_is_read_again`
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and True

```

### `u249.M10_window_halved`

REMEMBER_WINDOW_NS: one second in place of two, under a FAT volume's step

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M10_window_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[1.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[just-under-2s]`

Old text:

```
REMEMBER_WINDOW_NS = 2_000_000_000
```

New text:

```
REMEMBER_WINDOW_NS = 1_000_000_000
```

### `u249.M11_window_boundary`

_read_from_disk: a file exactly two seconds older than its entry is read again rather than answered

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M11_window_boundary`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
            and stamp[1] <= entry.made_ns - REMEMBER_WINDOW_NS

```

New text:

```
            and stamp[1] < entry.made_ns - REMEMBER_WINDOW_NS

```

### `u249.M12_moment_after_read`

_read_from_disk: take the entry's moment after the read, so a write during the read can be answered from memory

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M12_moment_after_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_the_entrys_moment_is_taken_before_the_read`

Old text:

```
    owned, whole = _read_fresh(path, template)
    if stamp is not None and whole:
```

New text:

```
    owned, whole = _read_fresh(path, template)
    made_ns = _now_ns()
    if stamp is not None and whole:
```

### `u249.M13_failed_read_remembered`

_read_from_disk: remember a read that failed, so a moment's I/O error on a USB volume answers every later job

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M13_failed_read_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 3 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_failed_is_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`

Old text:

```
    if stamp is not None and whole:
```

New text:

```
    if stamp is not None:
```

### `u249.M14_unstated_remembered_never`

_stamp_of: answer None for every file, so nothing is ever remembered and every walk opens every file

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M14_unstated_remembered_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 11 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_on_another_device_under_the_same_name_and_stamp_is_read_again`
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_library_reads_remembered.py::test_a_pass_of_three_playlists_opens_each_library_file_once`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_removed_file_is_absent_a_new_one_is_read_and_a_renamed_one_is_read_under_its_name`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_an_unchanged_old_file_is_answered_from_memory_on_the_second_index`
  - `tests/test_library_reads_remembered.py::test_the_stamp_is_the_files_stat_and_none_for_a_file_that_is_gone`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2.5s]`
  - `tests/test_library_reads_remembered.py::test_the_window_is_two_seconds_to_the_nanosecond[2s]`

Old text:

```
    return (seen.st_size, seen.st_mtime_ns, seen.st_ctime_ns, seen.st_ino, seen.st_dev)
```

New text:

```
    return None
```

### `u249.M20_reset_forgets_nothing`

match.reset_cache: forget nothing

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M20_reset_forgets_nothing`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 6 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_that_cannot_be_stated_is_read_as_before_and_never_remembered`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_is_indexed_as_read_and_not_remembered`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[intake]`
  - `tests/test_library_reads_remembered.py::test_a_reset_forgets_every_file[match]`
  - `tests/test_library_reads_remembered.py::test_a_test_starts_with_nothing_remembered`

Old text:

```
    test can clear is a memory that leaks one test's library into the next."""
    _REMEMBERED.clear()
```

New text:

```
    test can clear is a memory that leaks one test's library into the next."""
```

### `u249.M20a_failed_read_keeps_old_entry`

_read_from_disk: keep an earlier whole read's entry when a later read is not whole, so a stamp that comes back brings the old tags back

- File: `src/cratekit/acquire/match.py`
- Source: `u249.json`, row `M20a_failed_read_keeps_old_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_library_reads_remembered.py`, `tests/test_match_states.py`, `tests/test_sync_land.py`, `tests/intake/test_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 1 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_read_that_is_not_whole_forgets_what_an_earlier_whole_read_left`

Old text:

```
    else:
        # A read that was not whole, or a file with no stamp, forgets what an
        # earlier whole read left: the file has been seen changing, and a stamp
        # that came back later must not bring the older answer back with it.
        _REMEMBERED.pop(key, None)
    return owned
```

New text:

```
    return owned
```

### `u262.C1_letters_rule_back`

_is_a_credit: answer by the folded group's first letters again, the defect, so (Without You Remix) is a credit

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C1_letters_rule_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_defect_title_keeps_the_tombstone_identity_its_spelling_always_had`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Feature Edit]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Featureless Dub]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Withdrawn Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Within Mix]`
  - `tests/test_match_states.py::test_a_group_that_only_begins_with_a_credits_letters_is_a_version[Without You Remix]`
  - `tests/test_match_states.py::test_a_library_file_whose_group_only_begins_with_a_credits_letters_is_that_version`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You Remix)-expected11]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Feature Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featureless Dub]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featurette]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Ftw Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Withdrawn Mix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Within Mix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Without You Remix]`

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return any(" ".join(words).startswith(marker) for marker in _CREDIT_MARKERS)
```

### `u262.C2_any_word`

_is_a_credit: a marker anywhere in the group makes a credit, so (Live with Strings) loses its version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C2_any_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Live with Strings]`

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return any(word in _CREDIT_MARKERS for word in words)
```

### `u262.C3_last_word`

_is_a_credit: ask the group's last word rather than its first

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C3_last_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 32 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    return bool(words) and words[-1] in _CREDIT_MARKERS
```

### `u262.C4_unfolded_words`

_is_a_credit: split the raw group on spaces without folding, so feat. and Featuring are not markers

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C4_unfolded_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 26 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    words = fold(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS
```

New text:

```
    words = str(inside).split()
    return bool(words) and words[0] in _CREDIT_MARKERS
```

### `u262.C5_no_with`

_CREDIT_MARKERS: drop with, so (with Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C5_no_with`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 7 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (with Mira)-addresses2]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (with Zed) - Nightwave Remix]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[With You]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[With]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[with Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring"})
```

### `u262.C6_no_ft`

_CREDIT_MARKERS: drop ft, so (ft Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C6_no_ft`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_the_abbreviation_ft_stays_a_credit`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path [ft. Zed] [Nightwave Remix]]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[FT. Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Ft Worth Edit]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[ft Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[ft.anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "featuring", "with"})
```

### `u262.C7_no_featuring`

_CREDIT_MARKERS: drop featuring, so (Featuring Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C7_no_featuring`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[Featuring Anna]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_agree_on_what_a_credit_is[featuring]`
  - `tests/test_match_states.py::test_the_matcher_and_the_tombstone_share_one_credit_vocabulary`

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "with"})
```

### `u262.C8_no_feat`

_CREDIT_MARKERS: drop feat, so (feat. Anna) becomes a version

- File: `src/cratekit/acquire/match.py`
- Source: `u262.json`, row `C8_no_feat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/test_uncredited_tombstone.py`, `tests/test_tombstones.py`
- Collected: 681 against a baseline of 681
- Kills: 19 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (feat. Mira) (Extended) (Remastered)-provider2-spelled_addresses2-provider_addresses2]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (feat. Mira) (Nightwave Remix)-addresses0]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (Nightwave Remix) (feat. Zed)]`
  - `tests/test_match_states.py::test_a_listing_that_spelled_a_credit_never_asks_for_a_companion[Sun Path (feat. Zed) (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - ... and 4 more, see the JSON sidecar

Old text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"feat", "ft", "featuring", "with"})
```

New text:

```
_CREDIT_MARKERS: frozenset[str] = frozenset({"ft", "featuring", "with"})
```

### `u265.M10_empty_index_scored`

_approximate: drop the early return on an empty index (an existing guard, sampled), so an empty library sorts the wanted token and asks the scorer

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M10_empty_index_scored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call`

Old text:

```
    if not index.by_recording:
        return ()
    from rapidfuzz import fuzz, process

    recordings, sorted_choices
```

New text:

```
    from rapidfuzz import fuzz, process

    recordings, sorted_choices
```

### `u265.M1_narrow_split_everywhere`

_sorted_words: split every string on the narrow set, so a wide string keeps U+0085 and U+00A0 inside a word where the scorer splits

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M1_narrow_split_everywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
        words = token.split()
```

New text:

```
    if False:
        words = token.split()
```

### `u265.M2_python_split_everywhere`

_sorted_words: split every string on Python whitespace, so a narrow string splits on U+0085 and U+00A0 where the scorer does not

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M2_python_split_everywhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
        words = token.split()
```

New text:

```
    if True:
        words = token.split()
```

### `u265.M2b_width_off_by_one`

_sorted_words: read a string as wide from U+00FF rather than U+0100, so a narrow name ending in y with a diaeresis splits on U+00A0 where the scorer does not (review round one's finding)

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M2b_width_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_word_sort_splits_on_exactly_the_whitespace_the_scorer_splits_on`

Old text:

```
    if token and max(token) > "\xff":
```

New text:

```
    if token and max(token) >= "\xff":
```

### `u265.M3_words_not_sorted`

_sorted_words: join the words in their own order, so the pass scores plain ratio and an artist and title swap no longer matches

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M3_words_not_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 18 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Lights Midnight-Midnight Lights]`
  - `tests/test_match_states.py::test_a_spelled_number_is_not_read_as_a_numeral[Four Tune-Fortune]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_every_pair_scores_the_same_through_the_sorted_form`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    return " ".join(sorted(words))
```

New text:

```
    return " ".join(words)
```

### `u265.M4_query_not_sorted`

_approximate: score the wanted token unsorted against the sorted library names

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M4_query_not_sorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 42 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbor Lights]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Light]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Harbour Lighte]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Midnight Harbour Lights-Midnight Lights]`
  - ... and 27 more, see the JSON sidecar

Old text:

```
        _sorted_words(wanted.recording),
        sorted_choices,
```

New text:

```
        wanted.recording,
        sorted_choices,
```

### `u265.M5_hit_named_by_its_sorted_form`

_approximate: look a hit up by its sorted string rather than its position, so any recording whose words were not already in order loses its files

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M5_hit_named_by_its_sorted_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 61 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[DNA-D.N.A.]`
  - ... and 46 more, see the JSON sidecar

Old text:

```
        held for _sorted, _score, position in found for held in index.versions(recordings[position])
```

New text:

```
        held for _sorted, _score, position in found for held in index.versions(_sorted)
```

### `u265.M6_cache_misaligned`

sorted_recordings: build the sorted names in reverse, so a position the scorer returns names a different recording

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M6_cache_misaligned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 15 (killed)
- Killed:
  - `tests/test_library_reads_remembered.py::test_a_file_rewritten_between_two_jobs_is_read_again_and_the_second_job_matches_its_new_tags`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-5]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in recordings))
```

New text:

```
            cached = (recordings, tuple(_sorted_words(token) for token in reversed(recordings)))
```

### `u265.M7_cache_never_kept`

sorted_recordings: never store the sorted names, so every wanted row sorts the whole library again (answers unchanged, cost back to per pair)

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M7_cache_never_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_each_name_is_sorted_once_for_the_index_and_each_row_once_a_call`

Old text:

```
            object.__setattr__(self, "_sorted", cached)
```

New text:

```
            pass
```

### `u265.M8_other_scorer`

_approximate: score the sorted forms with WRatio instead of ratio, so scores and the floor's cut move

- File: `src/cratekit/acquire/match.py`
- Source: `u265.json`, row `M8_other_scorer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`
- Collected: 2835 against a baseline of 2835
- Kills: 39 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_rerun_after_acquiring_reports_the_heart_owned_with_no_cursor`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_favorites_resolves_each_heart_owned_offered_or_missing`
  - `tests/intake/test_workers.py::test_the_missing_hearts_carry_the_provider_id_acquisition_reads`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`
  - `tests/intake/test_workers.py::test_the_resolution_names_owned_offered_and_missing_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_rejected_row_under_a_tombstone_is_suppressed_not_listed`
  - `tests/test_intake_missing.py::test_a_rejection_after_a_listing_refuses_over_the_earlier_list_and_says_why`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_row_tombstoned_since_the_job_is_not_listed_and_counted_suppressed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_second_run_is_the_same_list_and_not_a_refusal`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_shorter_rerun_over_the_jobs_earlier_list_refuses_and_says_why`
  - ... and 24 more, see the JSON sidecar

Old text:

```
        scorer=fuzz.ratio,
```

New text:

```
        scorer=fuzz.WRatio,
```

### `u269.M7_match_engine_binds_lxml`

acquire/match.py: bind lxml.etree under a branch that never runs, the export reader guard's lxml case, which stays as it is

- File: `src/cratekit/acquire/match.py`
- Source: `u269.json`, row `M7_match_engine_binds_lxml`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 2 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_export_guard_stays_quiet_on_correct_code[from . import match\n]`
  - `tests/test_match_states.py::test_the_match_engine_never_reaches_a_rekordbox_export`

Old text:

```
import hashlib

```

New text:

```
import hashlib

if False:
    import lxml.etree  # noqa: F401

```

### `u286.M10_swap_either_half`

the swap allowance takes either crossed half rather than both, so an unrelated title by an artist sharing one word is offered

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M10_swap_either_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_swap_is_offered_only_when_both_halves_cross`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)

```

New text:

```
    return _agree(asked, fold(held.artist)) or _agree(fold(wanted.artist), found)

```

### `u286.M11_swap_removed`

the swap allowance removed, so a listing pasted title first reads missing and downloads the record the library holds

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M11_swap_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 8 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)

```

New text:

```
    return False

```

### `u286.M12_swap_second_half_artist`

the swap's second half compares artist with artist, which the shared artist always passes, so one crossed half is enough

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M12_swap_second_half_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 8 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Every Day-Everyday - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - OK-O.K. - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), found)

```

New text:

```
    return _agree(asked, fold(held.artist)) and _agree(fold(wanted.artist), fold(held.artist))

```

### `u286.M13_filter_removed`

_resembling keeps every recording discovery finds, the base's behaviour, so Joy is offered Goodbye again

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M13_filter_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 20 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_joy_against_goodbye_is_downloaded_through_the_real_verb`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if not _title_resembles(wanted, held[0]):
            continue

```

New text:

```
        if False:
            continue

```

### `u286.M14_filter_after_cap`

_resembling asks discovery for the best five only and filters those, so unrelated titles outscoring a real near match push it out and the row downloads

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M14_filter_after_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
        _approximate(wanted, index, limit=None), key=attrgetter("recording")

```

New text:

```
        _approximate(wanted, index, limit=APPROXIMATE_LIMIT), key=attrgetter("recording")

```

### `u286.M15_cap_removed`

_resembling keeps every recording that passes, so more than five reach the candidate builder and the withheld count reports recordings the cap should not have built

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M15_cap_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`

Old text:

```
        if recordings == APPROXIMATE_LIMIT:
            break

```

New text:

```
        if False:
            break

```

### `u286.M16_cap_off_by_one`

_resembling keeps six recordings rather than five

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M16_cap_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_scorer_is_capped_at_the_same_number_the_offer_is`

Old text:

```
        if recordings == APPROXIMATE_LIMIT:

```

New text:

```
        if recordings == APPROXIMATE_LIMIT + 1:

```

### `u286.M17_cap_counts_files`

_resembling counts files rather than recordings toward the cap, so a recording held as several versions takes several places

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M17_cap_counts_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`

Old text:

```
        recordings += 1

```

New text:

```
        recordings += len(held)

```

### `u286.M18_resolver_back_to_base`

resolve_one calls the shipped discovery at the offer limit, the base, so the whole title test is bypassed

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M18_resolver_back_to_base`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 51 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[2-Tom]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[4-Fort]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[B-Bee]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Cos-Because]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Luv-Lover]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[N-Ant]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[U-Yo]`
  - `tests/test_match_states.py::test_a_pair_the_spelled_out_reading_does_not_join_still_settles_missing[Wot-What]`
  - `tests/test_match_states.py::test_a_scored_hit_keeps_its_place_and_a_lookup_hit_only_discovery_missed_leads`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Alex Kaminski-Mana-Nebula]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Hot Since 82-Wow-Wild]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Monkey Safari-Joy-Goodbye]`
  - ... and 36 more, see the JSON sidecar

Old text:

```
    near = _resembling(wanted, index)

```

New text:

```
    near = _approximate(wanted, index, limit=APPROXIMATE_LIMIT)

```

### `u286.M19_limit_ignored`

_approximate ignores its limit and always caps at five, so the resolver's ask for every hit is cut before the title test

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M19_limit_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 9 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[265-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[2650-None]`
  - `tests/test_match_states.py::test_the_approximate_pass_answers_exactly_as_the_shipped_scorer[26500-None]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_unrelated_titles_scoring_higher_do_not_push_a_real_near_match_out`

Old text:

```
        score_cutoff=APPROXIMATE_FLOOR,
        limit=limit,

```

New text:

```
        score_cutoff=APPROXIMATE_FLOOR,
        limit=APPROXIMATE_LIMIT,

```

### `u286.M1_title_floor_up_one`

APPROXIMATE_TITLE_FLOOR raised from 66 to 67, so one letter changed in a three letter title (Joy against Jay) reads missing and downloads

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M1_title_floor_up_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Joy-Jay]`
  - `tests/test_match_states.py::test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio`

Old text:

```
APPROXIMATE_TITLE_FLOOR = 66

```

New text:

```
APPROXIMATE_TITLE_FLOOR = 67

```

### `u286.M2_title_floor_down_one`

APPROXIMATE_TITLE_FLOOR lowered from 66 to 65, so the nearest pair under it (Burning Sunlight against Morning Starlight Rising, 65.0) is offered

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M2_title_floor_down_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`

Old text:

```
APPROXIMATE_TITLE_FLOOR = 66

```

New text:

```
APPROXIMATE_TITLE_FLOOR = 65

```

### `u286.M3_title_floor_to_sixty`

APPROXIMATE_TITLE_FLOOR lowered to 60, so the card's Traumer pair, Get Out against Agenou at 61.5, is offered again

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M3_title_floor_to_sixty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 3 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_the_title_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_titles_split_differently_are_kept_by_equality_and_not_by_a_ratio`

Old text:

```
APPROXIMATE_TITLE_FLOOR = 66

```

New text:

```
APPROXIMATE_TITLE_FLOOR = 60

```

### `u286.M4_plain_ratio`

_agree scores fuzz.ratio rather than token_set_ratio, so a dropped or reordered word scores on its letters and can read missing

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M4_plain_ratio`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 6 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Lights Midnight-Midnight Lights]`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_the_title_test_only_adds_agreement_and_only_for_a_spelled_out_equal_pair`

Old text:

```
    return fuzz.token_set_ratio(one, other) >= APPROXIMATE_TITLE_FLOOR

```

New text:

```
    return fuzz.ratio(one, other) >= APPROXIMATE_TITLE_FLOOR

```

### `u286.M6_unreadable_title_not_asked`

_title_resembles no longer asks whether a title folds to nothing, so the empty title is scored and agrees with nothing

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `M6_unreadable_title_not_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 15 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[!!!-Sun]`
  - `tests/test_match_states.py::test_a_title_that_folds_to_nothing_is_offered_as_before[Sun-!!!]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_about_one_emoji_title_does_not_settle_another`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_an_emoji_candidate_offered_for_another_is_named_a_resemblance`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[26500]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[2650]`
  - `tests/test_match_states.py::test_the_offer_is_the_shipped_hits_filtered_by_title_then_capped[265]`
  - `tests/test_match_states.py::test_two_different_emoji_titles_by_one_artist_are_not_one_recording`
  - `tests/test_match_states.py::test_two_different_emoji_titles_through_the_real_verb_are_not_owned`
  - `tests/test_match_states.py::test_two_held_emoji_titles_are_offered_as_two_candidates`

Old text:

```
    if not asked or not found:
        return True

```

New text:

```
    if False:
        return True

```

### `u286.S1_discovery_floor_up_one`

sampled existing guard: APPROXIMATE_FLOOR raised from 82 to 83

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `S1_discovery_floor_up_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 10 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_former_identifier_is_carried_only_with_one_fit_and_its_title`
  - `tests/test_match_states.py::test_a_real_near_match_is_still_offered[Good Bye-Goodbye]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Paul Deep (AR)-Rea-Tique]`
  - `tests/test_match_states.py::test_a_short_title_sharing_nothing_with_the_held_one_settles_missing[Traumer-Get Out-Agenou]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[Aurora Bloom - Goodbye-Good Bye - Aurora Bloom]`
  - `tests/test_match_states.py::test_a_swapped_listing_split_differently_is_still_offered[M.I.A. - Paper Planes-Paper Planes - MIA]`
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`
  - `tests/test_match_states.py::test_an_answer_recorded_before_is_not_carried_to_another_emoji_file`
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`
  - `tests/test_match_states.py::test_the_floor_is_pinned_from_both_sides_by_the_nearest_score_either_way`

Old text:

```
APPROXIMATE_FLOOR = 82

```

New text:

```
APPROXIMATE_FLOOR = 83

```

### `u286.S2_offer_not_truncated`

sampled existing guard: the approximate offer is not truncated to the limit

- File: `src/cratekit/acquire/match.py`
- Source: `u286.json`, row `S2_offer_not_truncated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`
- Collected: 3906 against a baseline of 3906
- Kills: 4 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_at_most_the_declared_number_of_approximate_candidates_is_offered`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`

Old text:

```
            candidates=offered[:APPROXIMATE_LIMIT],

```

New text:

```
            candidates=offered,

```

### `r1709.M22_adjudicate_not_carried`

adjudicate passes the stored option unchanged, so an answer recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r1709.json`, row `M22_adjudicate_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_an_answer_recorded_before_naming_an_emoji_file_still_applies`

Old text:

```
                    else match.current_option(found, held.option, titles.get(held.option))

```

New text:

```
                    else held.option

```

### `r1709.M2_adjudicate_offered_not_carried`

adjudicate binds an unspecific yes to the stored option unchanged, so a yes recorded before about an emoji file reads as a candidate gone

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r1709.json`, row `M2_adjudicate_offered_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_catalogue_app.py`, `tests/test_cli_contract.py`, `tests/test_export_set.py`, `tests/test_export_set_rename.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_library_reads_remembered.py`, `tests/test_listdoc.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_setbuilder_cli.py`, `tests/test_title_matcher.py`, `tests/test_review_queue.py`, `tests/test_render_payloads.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`
- Collected: 3983 against a baseline of 3983
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_yes_recorded_before_naming_no_option_still_applies`

Old text:

```
                    match.current_option(found, one.option_id, titles.get(one.option_id))

```

New text:

```
                    one.option_id

```

### `r431-b.B6_the_verb_calls_a_companion_stale`

The verb's report over a matched row asks for companions, so a held file crediting somebody else calls one stale

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r431-b.json`, row `B6_the_verb_calls_a_companion_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_label_approved.py`, `tests/test_label_workers.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1005 against a baseline of 1005
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`

Old text:

```
                companions=not held,
```

New text:

```
                companions=True,
```

### `r679-b.B1_no_retirement`

adjudicate: never retire, so an owned row leaves its question open

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B1_no_retirement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
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

### `r679-b.B2_any_matched_row_is_owned_by_a_rule`

owned_by_a_rule: any matched row counts, a person's applied acceptance included

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B2_any_matched_row_is_owned_by_a_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_the_gate_predicate_admits_a_question_and_a_rule_owned_row_and_nothing_else`

Old text:

```
    return found.state is match.MatchState.MATCHED and found.why in match.OWNING_RULES
```

New text:

```
    return found.state is match.MatchState.MATCHED
```

### `r679-b.B3_no_reopen`

adjudicate: leave a superseded item standing when its row asks again

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B3_no_reopen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_retired_question_the_row_asks_again_is_reopened_not_read_as_a_rejection`

Old text:

```
        if held is not None and held.verdict is review.Verdict.SUPERSEDED:
```

New text:

```
        if False:
```

### `r679-b.B5_rule_not_recorded`

retire_questions: record a fixed rule instead of the why that owned the row

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B5_rule_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
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

### `r679-b.B6_one_shape_only`

retire_questions: ask about the first shape only, so a version question is never retired

- File: `src/cratekit/acquire/match_cli.py`
- Source: `r679-b.json`, row `B6_one_shape_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
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

### `u16-round-8-independent.V22_suppressed_warning_omitted`

The suppressed rows stop being reported on the warning channel, so a suppression is omitted silently (R36)

- File: `src/cratekit/acquire/match_cli.py`
- Source: `u16-round-8-independent.json`, row `V22_suppressed_warning_omitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`
- Collected: 609 against a baseline of 609
- Kills: 26 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (Nightwave Remix) (feat. Mira)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira) (Nightwave Remix)-]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path (feat. Mira)-Nightwave Remix]`
  - `tests/test_match_states.py::test_a_credited_deletion_suppresses_the_listing_that_never_spelled_the_credit[Sun Path [ft. Mira] [Nightwave Remix]-]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[round-listed]`
  - `tests/test_match_states.py::test_a_credited_listing_reaches_the_other_bracket_shape_of_its_own_version[square-listed]`
  - `tests/test_match_states.py::test_a_deletion_of_the_plain_record_never_withholds_the_credited_one`
  - `tests/test_match_states.py::test_a_listing_both_records_answer_is_reported_under_the_tombstone`
  - `tests/test_match_states.py::test_a_suppressed_version_is_reported_as_a_warning_carrying_its_identifier`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[round]`
  - `tests/test_match_states.py::test_a_tombstone_is_addressed_by_every_reading_except_the_undecidable_one[square]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Extended) (Remastered)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Nightwave Remix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (Original Mix)]`
  - `tests/test_match_states.py::test_a_tombstone_recorded_from_any_row_spelling_suppresses_the_list_that_names_it[Sun Path (feat. Mira) (Nightwave Remix)]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    for track in result.suppressed:

```

New text:

```
    for track in ():

```

### `r1305.L1_login_name_on_any_link`

_rejected: read the client's authentication error by name on any link, so a reset met while handling one asks for a login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L1_login_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_authentication_error_reached_only_as_context_is_a_wait`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False

```

New text:

```
        if type(link).__name__ == "AuthenticationError":
            return True
    return False

```

### `r1305.L2_login_status_declared_only`

_rejected: read a status on the declared chain only, so a login answered 401 or 403 with a page is told to wait

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L2_login_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[400-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_whatever_the_body_asks_for_a_login[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_login_rejected_with_a_page_tells_the_person_to_log_in_again`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login[401-html]`

Old text:

```
        if answered_status(link) in REJECTED_STATUSES:
```

New text:

```
        if declared and answered_status(link) in REJECTED_STATUSES:
```

### `r1305.L3_login_name_dropped`

_rejected: drop the client's authentication error by name, a sample of the guard as it stood before R-1305

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1305.json`, row `L3_login_name_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[client-auth-error]`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
            return True
    return False

```

New text:

```
        if False:
            return True
    return False

```

### `r1694.L1_login_no_tolerance`

_login: open the scope with no tolerance, so the login fails as it did before R-1694

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L1_login_no_tolerance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
    with materialised_session(name, unstored=failed.append) as scope:
```

New text:

```
    with materialised_session(name) as scope:
```

### `r1694.L2_token_file_uncaught`

_login: let a token file the refresh cannot be written to raise, so a full temporary disk fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L2_token_file_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`

Old text:

```
            except OSError as exc:
                failed.append(exc)
    if failed:
```

New text:

```
            except ArithmeticError as exc:
                failed.append(exc)
    if failed:
```

### `r1694.L3_token_file_catches_defect`

_login: catch every exception at the token file write, so a field the file cannot encode is a warning rather than a defect

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L3_token_file_catches_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_capture_still_raises`

Old text:

```
            except OSError as exc:
                failed.append(exc)
    if failed:
```

New text:

```
            except Exception as exc:
                failed.append(exc)
    if failed:
```

### `r1694.L4_rewrite_unchanged`

_login: rewrite the token file for an unchanged session too, so a file that cannot be written is reported over a session with nothing to store

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L4_rewrite_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_capture_still_raises`
  - `tests/test_provider_session_unstored.py::test_an_unchanged_session_never_rewrites_the_token_file`

Old text:

```
        if _canonical(refreshed) != _canonical(stored):
```

New text:

```
        if _canonical(refreshed) is not None:
```

### `r1694.L5_hold_the_refresh`

_login: return the refresh as what the keychain holds after a store failure, so every later resolve logs in again and fails to store again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L5_hold_the_refresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`

Old text:

```
        return client, stored
    return client, refreshed
```

New text:

```
        return client, refreshed
    return client, refreshed
```

### `r1694.L6_no_note`

_login: note nothing on a store failure, so the verb never says the session was not stored

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L6_no_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
```

New text:

```
        pass
```

### `r1694.L7_note_the_words`

_login: note the failure's words rather than its class, so a credential refusal's setup advice reaches the warning

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `L7_note_the_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 164 against a baseline of 164
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_token_file_that_cannot_take_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
        _UNSTORED.extend(type(exc).__name__ for exc in failed)
```

New text:

```
        _UNSTORED.extend(str(exc) for exc in failed)
```

### `r1694.S1_tolerance_reraises`

materialised_session: re-raise a store failure handed to the tolerance, so a refreshed login on the opt in fails the verb again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S1_tolerance_reraises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 7 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`

Old text:

```
            except STORE_FAILURES as exc:
                unstored(exc)

```

New text:

```
            except STORE_FAILURES as exc:
                raise

```

### `r1694.S2_tolerance_always`

materialised_session: tolerate a store failure even when no callback was given, so the drive's own catch and streamrip's scope lose their failure

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S2_tolerance_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_scope_that_asked_for_no_tolerance_still_raises_its_write_back_failure`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if unstored is None:
            write_back(name, path, codec=codec, stored=payload)
        else:

```

New text:

```
        if False:
            write_back(name, path, codec=codec, stored=payload)
        else:
            unstored = unstored or (lambda exc: None)

```

### `r1694.S3_catch_everything`

materialised_session: catch every exception at the write back, so a defect in the write is a warning rather than a raise

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S3_catch_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_defect_in_the_write_back_still_raises`

Old text:

```
            except STORE_FAILURES as exc:
                unstored(exc)

```

New text:

```
            except Exception as exc:
                unstored(exc)

```

### `r1694.S4_failures_no_credential`

STORE_FAILURES: drop the credential errors, so the keychain's own refusal on the opt in fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S4_failures_no_credential`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 8 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_a_refreshed_login_the_keychain_cannot_take_returns_the_client`
  - `tests/test_provider_session_unstored.py::test_a_verb_whose_login_refreshed_on_the_opt_in_answers_as_before_and_warns`
  - `tests/test_provider_session_unstored.py::test_an_index_that_cannot_be_locked_is_noted_and_the_keychain_is_untouched`
  - `tests/test_provider_session_unstored.py::test_the_held_session_is_the_stored_one_so_a_reuse_neither_logs_in_nor_warns_again`
  - `tests/test_provider_session_unstored.py::test_the_warning_is_this_verbs_alone`
  - `tests/test_provider_session_unstored.py::test_two_failed_stores_in_one_verb_make_one_warning_naming_the_class_once`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_leaves_a_park_its_own_cause`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    CratekitError,
    OSError,
)
```

### `r1694.S5_failures_no_cratekit`

STORE_FAILURES: drop CratekitError, so an index the write could not read fails the login

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S5_failures_no_cratekit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_unstored.py::test_an_index_that_refuses_after_the_keychain_took_the_refresh_is_noted`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    OSError,
)
```

### `r1694.S6_failures_no_oserror`

STORE_FAILURES: drop OSError, so an index file the write could not make fails the login and the drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r1694.json`, row `S6_failures_no_oserror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_unstored.py`, `tests/test_provider_session_hold.py`, `tests/test_vendored_drive.py`, `tests/test_provider_gate.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`

Old text:

```
    secrets.CredentialError,
    CratekitError,
    OSError,
)
```

New text:

```
    secrets.CredentialError,
    CratekitError,
)
```

### `r705-b.S2_client_session_never_attaches`

the catalogue and account client's transport is not gated, so nothing it does is paced or counted

- File: `src/cratekit/acquire/provider_session.py`
- Source: `r705-b.json`, row `S2_client_session_never_attaches`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 16 (killed)
- Killed:
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
  - `tests/test_provider_gate.py::test_the_spend_line_reaches_a_person_on_the_human_output`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        client = CLIENT_FACTORY()
        gate.attach(client)

```

New text:

```
        client = CLIENT_FACTORY()

```

### `u205.O2_no_country_still_opens`

opener: an account naming no country still gets an app client, asked in no country

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O2_no_country_still_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 351 against a baseline of 351
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

### `u205.O3_unreadable_values_read_as_absent`

opener: recorded app values the keychain will not give are read as absent, putting every lookup back on the account without a word

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O3_unreadable_values_read_as_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 351 against a baseline of 351
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

### `u205.O4_app_attached_as_account`

opener: the app client is attached under the account identity, so its calls are reported as the account's

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u205.json`, row `O4_app_attached_as_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 351 against a baseline of 351
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

### `u261.H1_reuse_skips_the_gate`

session_for: reuse the held session without asking the gate, so a verb started inside a cooldown gets a client

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H1_reuse_skips_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_catalogue_app.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_reuse_inside_a_cooldown_refuses_without_a_call`

Old text:

```
        current.gate.assert_open()
        try:
            stored = secrets.get_json(name)
```

New text:

```
        try:
            stored = secrets.get_json(name)
```

### `u261.H2_reuse_ignores_a_replaced_session`

session_for: reuse the held client whatever the keychain now holds, so a session replaced or refreshed elsewhere is never picked up

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H2_reuse_ignores_a_replaced_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_a_session_replaced_after_an_open_is_logged_in_afresh_from_the_new_value`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
        if _canonical(stored) == current.blob:
```

New text:

```
        if True:
```

### `u261.H3_reuse_swallows_a_missing_session`

session_for: answer a keychain that no longer holds the session with the held client, so a withdrawn session is reused

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H3_reuse_swallows_a_missing_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_keychain_that_cannot_be_read_on_a_reuse_says_repair_it`
  - `tests/test_provider_session_hold.py::test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused`

Old text:

```
            drop(current)
            raise _to_auth_failure(exc) from exc
```

New text:

```
            return current
```

### `u261.H4_failed_read_keeps_the_hold`

session_for: refuse a keychain that cannot be read on a reuse but keep the hold, so the account's held adapter goes on over it

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H4_failed_read_keeps_the_hold`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_session_gone_from_the_keychain_after_an_open_is_refused_not_reused`

Old text:

```
            drop(current)
            raise _to_auth_failure(exc) from exc
```

New text:

```
            raise _to_auth_failure(exc) from exc
```

### `u261.H5_settings_not_in_the_key`

session_for: reuse a session opened under other gate settings, so a job's frozen interval and cooldown are not the ones its calls run under

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H5_settings_not_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`
- Collected: 147 against a baseline of 147
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_other_gate_settings_open_a_session_of_their_own`

Old text:

```
    if current is not None and current.name == str(name) and current.settings == settings:
```

New text:

```
    if current is not None and current.name == str(name):
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

### `u261.H7_nothing_held`

session_for: hold nothing after a login, so every opener logs in again as before the unit

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H7_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 12 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again`
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_a_session_the_index_no_longer_records_is_refused_by_both_seams`
  - `tests/test_provider_session_hold.py::test_an_answer_that_judges_no_session_keeps_the_client`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`
  - `tests/test_provider_session_hold.py::test_the_surveys_drive_logs_in_once_and_writes_nothing`

Old text:

```
    _watch(opened)
    _HELD = opened
    return opened
```

New text:

```
    _watch(opened)
    return opened
```

### `u261.H8_blob_is_the_stored_not_the_refresh`

_login: report the session read rather than the refresh written back, so a refreshed login reads as replaced on every reuse and logs in again

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H8_blob_is_the_stored_not_the_refresh`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`
- Collected: 30 against a baseline of 30
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`

Old text:

```
    return client, refreshed
```

New text:

```
    return client, stored
```

### `u261.H9_no_forget_before_a_new_login`

session_for: keep the old hold while a replaced session is logged in afresh, so a login that fails leaves the account's adapter over the replaced session

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `H9_no_forget_before_a_new_login`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`

Old text:

```
    forget()
    gate = provider_gate.Gate(settings)
```

New text:

```
    gate = provider_gate.Gate(settings)
```

### `u261.R1_watch_not_installed`

session_for: install no watch on the shared client, so a 401 or 403 the catalogue meets leaves the refused client held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R1_watch_not_installed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`

Old text:

```
    _watch(opened)
    _HELD = opened
```

New text:

```
    _HELD = opened
```

### `u261.R2_answered_refusal_ignored`

_watch: ignore a 401 or 403 the transport answers, so a refused client stays held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R2_answered_refusal_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`
- Collected: 207 against a baseline of 207
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`

Old text:

```
        if getattr(response, "status_code", None) in SESSION_REFUSED_STATUSES:
            drop(session)
```

New text:

```
        if False:
            drop(session)
```

### `u261.R3_raised_refusal_ignored`

_watch: ignore a 401 or 403 the transport raises, so a refusal that arrives as an exception leaves the client held

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R3_raised_refusal_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_the_transport_raises_drops_the_client_too`

Old text:

```
            if answered_status(exc) in SESSION_REFUSED_STATUSES:
```

New text:

```
            if False:
```

### `u261.R4_forbidden_not_a_refusal`

SESSION_REFUSED_STATUSES: read only 401 as judging the session, so a 403 neither drops the shared client nor forgets the account

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R4_forbidden_not_a_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_rejection_bodies.py`
- Collected: 174 against a baseline of 174
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-empty]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-json]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`

Old text:

```
SESSION_REFUSED_STATUSES = frozenset({401, 403})
```

New text:

```
SESSION_REFUSED_STATUSES = frozenset({401})
```

### `u261.R5_drop_not_by_identity`

drop: drop whatever is held, so a stale client's refusal throws away the newer session logged in since

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `R5_drop_not_by_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`
- Collected: 30 against a baseline of 30
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_to_a_client_no_longer_held_keeps_the_newer_one`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
    if _HELD is session:
        _HELD = None
```

New text:

```
    if True:
        _HELD = None
```

### `u261.W1_unchanged_skip_removed`

write_back: drop the unchanged comparison, so every login writes the value already stored back to the keychain

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W1_unchanged_skip_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 481 against a baseline of 481
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_an_unchanged_session_makes_no_keychain_write`
  - `tests/test_provider_session_hold.py::test_an_unchanged_toml_session_is_not_written_back`
  - `tests/test_provider_session_hold.py::test_the_surveys_drive_logs_in_once_and_writes_nothing`
  - `tests/test_provider_session_hold.py::test_write_back_compares_the_value_and_not_the_spelling`

Old text:

```
        if unchanged is not None and unchanged == _canonical(stored):
            return False
```

New text:

```
        if False:
            return False
```

### `u261.W2_changed_session_skipped`

write_back: read any encodable session as unchanged, so a refreshed token is never stored (the merge blocker the card names)

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u261.json`, row `W2_changed_session_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_adapter_contract.py`, `tests/test_outbound_tidal_account.py`, `tests/test_catalogue_app.py`, `tests/test_provider_gate.py`
- Collected: 481 against a baseline of 481
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

### `u274.P1_gone_never`

_gone: read a process that is gone as alive, so a hard killed drive's token directory is never swept

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P1_gone_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`

Old text:

```
    except ProcessLookupError:
        return True

```

New text:

```
    except ProcessLookupError:
        return False

```

### `u274.P2_gone_overflow`

_gone: let OverflowError and ValueError escape, so a directory named for an impossible process id fails every materialise

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P2_gone_overflow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`

Old text:

```
    except (OSError, OverflowError, ValueError):

```

New text:

```
    except OSError:

```

### `u274.P3_gone_permission`

_gone: read another account's process (a permission refusal) as gone, so its live directory is swept

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P3_gone_permission`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_process_id_no_process_can_have_is_left_and_does_not_raise`
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_a_directory_whose_process_it_cannot_see`

Old text:

```
    except (OSError, OverflowError, ValueError):
        # Another account's process, or an id no process can have, which only
        # a directory someone else named could carry: never proven gone.
        return False

```

New text:

```
    except (OSError, OverflowError, ValueError):
        # Another account's process, or an id no process can have, which only
        # a directory someone else named could carry: never proven gone.
        return True

```

### `u274.P4_sweep_live`

sweep_orphans: drop the process check, so every directory of the form is removed, a live drive's token included

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P4_sweep_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 6 (killed)
- Killed:
  - `tests/test_adapter_contract.py::test_a_transient_track_is_requeueable_and_a_permanent_one_is_quarantined[vendored]`
  - `tests/test_provider_gate.py::test_a_verb_at_the_hours_line_is_blocked_and_keeps_what_it_did`
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

### `u274.P5_sweep_not_dir`

sweep_orphans: drop the directory check, so a file or a link of the name is reported removed

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P5_sweep_not_dir`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_the_sweep_reports_only_what_it_removed[file]`
  - `tests/test_vendored_drive.py::test_the_sweep_reports_only_what_it_removed[symlink]`

Old text:

```
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:

```

New text:

```
        if info.st_uid != account:

```

### `u274.P6_sweep_other_account`

sweep_orphans: drop the owner check, so another account's directory is removed

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P6_sweep_other_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_the_sweep_leaves_another_accounts_directory_alone`

Old text:

```
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != account:

```

New text:

```
        if not stat.S_ISDIR(info.st_mode):

```

### `u274.P7_no_sweep`

materialised_session: never sweep, so a hard killed drive's token file stays in the temporary directory

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P7_no_sweep`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_killed_outright_leaves_a_directory_the_next_one_sweeps`

Old text:

```
    sweep_orphans()
    # mkdtemp
```

New text:

```
    # mkdtemp
```

### `u274.P8_captured_always`

captured: take every field the client holds, so a float expiry read back from an int one writes the keychain on every drive

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P8_captured_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 3 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_an_unchanged_session_needs_no_keychain_write_at_all`

Old text:

```
        if value != stored.get(name):
            refreshed[name] = value

```

New text:

```
        refreshed[name] = value

```

### `u274.P9_captured_nothing`

captured: take no field, so a token the provider refreshed during the drive never reaches the keychain

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u274.json`, row `P9_captured_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 6 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        if value != stored.get(name):
            refreshed[name] = value

```

New text:

```
        if False:
            refreshed[name] = value

```

### `u62.S1_device_flow_login`

Log in as a device flow session rather than PKCE

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S1_device_flow_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_recorded_session_resolves_the_adapter_over_a_pkce_login`

Old text:

```
                is_pkce=True,
```

New text:

```
                is_pkce=False,
```

### `u62.S2_401_not_rejected`

Drop 401 from the statuses read as a rejected session

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S2_401_not_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[401]`
  - `tests/test_label_tidal_catalogue.py::test_a_session_the_provider_rejects_asks_for_a_new_login_not_a_first_one[chained-401]`

Old text:

```
REJECTED_STATUSES = frozenset({400, 401, 403})
```

New text:

```
REJECTED_STATUSES = frozenset({400, 403})
```

### `u62.S4_every_failure_rejected`

Read every login failure as a rejected session, the pre review behaviour

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S4_every_failure_rejected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[connection]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[server-error]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[timeout]`
  - `tests/test_label_tidal_catalogue.py::test_a_provider_that_cannot_be_reached_is_a_wait_not_a_new_login[unparseable-page]`

Old text:

```
            if _rejected(exc):
```

New text:

```
            if True:
```

### `u62.S5_blob_without_token_logged_in`

Hand a blob with no access token to the provider

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S5_blob_without_token_logged_in`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_stored_blob_with_no_access_token_never_reaches_the_provider`

Old text:

```
        if not isinstance(stored, dict) or not stored.get("access_token"):
```

New text:

```
        if not isinstance(stored, dict):
```

### `u62.S6_refresh_not_written_back`

Write the stored blob back unchanged instead of the refreshed tokens

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S6_refresh_not_written_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_refresh_during_login_is_written_back_to_the_keychain`

Old text:

```
            if value is not None:
                refreshed[field] = _epoch(value)
```

New text:

```
            if value is not None and False:
                refreshed[field] = _epoch(value)
```

### `u62.S7_naive_expiry_as_local`

Read the client's naive expiry as local time

- File: `src/cratekit/acquire/provider_session.py`
- Source: `u62.json`, row `S7_naive_expiry_as_local`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/test_adapter_contract.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if value.tzinfo is None:
```

New text:

```
        if value.tzinfo is None and False:
```

### `r1694.V1_drive_failures_narrowed`

vendored.drive: catch only credential errors at the close, so an index or file failure at a finished drive's close replaces its answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r1694.json`, row `V1_drive_failures_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_provider_session_unstored.py`, `tests/test_acquire_workers.py`
- Collected: 130 against a baseline of 130
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
        except provider_session.STORE_FAILURES as exc:
```

New text:

```
        except provider_session.STORE_FAILURES[:1] as exc:
```

### `r703-a.LF1_plain_runtime_error`

landed_file raises a plain RuntimeError, so the classifier reads the carried words

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `LF1_plain_runtime_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.LF2_cause_not_worded`

landed_file drops the cause from the message

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `LF2_cause_not_worded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.V1_no_observed_session`

fetch no longer stands the observed session in the downloader, so the unlogged lookup error is lost again

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V1_no_observed_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.V2_no_forget`

fetch keeps what the constructor logged, so the ffmpeg warning can stand as the item's cause

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V2_no_forget`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.V3_cause_not_passed`

fetch hands landed_file no cause, the eleventh sitting's plain no file answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V3_cause_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.V4_no_escalation`

a carried exception is no longer judged for a dead session or a defect

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V4_no_escalation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.V5_escalate_when_ok`

the escalation is asked on a landed item too, so an error the tool survived could abort a good download

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V5_escalate_when_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-a.V6_sample_no_park_check`

Sample of an existing guard: fetch no longer asks the gate for a park it raised inside the tool (R-705)

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-a.json`, row `V6_sample_no_park_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_held_lock_the_tool_swallowed_during_a_download_comes_out_of_fetch`
  - `tests/test_provider_gate.py::test_a_trip_the_tool_swallowed_during_a_download_comes_out_of_fetch_as_the_park`

Old text:

```
        self._gate.raise_if_parked()
        # THE SWALLOWED ERROR
```

New text:

```
        # THE SWALLOWED ERROR
```

### `r703-b.L1_no_active_exception`

the tool's log ignores the exception being handled and keeps only the message

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `L1_no_active_exception`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.L4_error_notes_nothing`

error() goes back to discarding, so a message only failure has no cause

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `L4_error_notes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.O1_proxy_notes_nothing`

the observed session re-raises without noting, so the unlogged lookup error is lost

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `O1_proxy_notes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.O3_writes_land_on_proxy`

attribute writes land on the proxy, so the tool's audio_quality write never reaches the real session

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `O3_writes_land_on_proxy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.O4_wraps_twice`

observe_session wraps an already observed session again

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `O4_wraps_twice`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.R1_status_path_dropped`

is_rate_limit reads the client's class only, so a bare 429 reads as an ordinary answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `R1_status_path_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.R2_everything_is_the_provider`

describe_cause calls the tool's own control flow the provider's answer

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `R2_everything_is_the_provider`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-b.R3_mapping_positional`

a single mapping argument is formatted positionally, not by name

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-b.json`, row `R3_mapping_positional`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-c.C1_last_exception_wins`

Batch B's L2 again after its test: a later exception overwrites the first

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-c.json`, row `C1_last_exception_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r703-c.C2_message_outranks_exception`

Batch B's L3 again after its test: the cause prefers the tool's message over the provider's exception

- File: `src/cratekit/acquire/vendored.py`
- Source: `r703-c.json`, row `C2_message_outranks_exception`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_provider_gate.py`
- Collected: 274 against a baseline of 274
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

### `r705-b.S3_vendored_never_asks_before_login`

a download started inside the cooldown builds the tool and logs in

- File: `src/cratekit/acquire/vendored.py`
- Source: `r705-b.json`, row `S3_vendored_never_asks_before_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_the_vendored_adapter_refuses_inside_the_cooldown_before_touching_the_tool`

Old text:

```
        self._gate.assert_open()
        if self._session is not None:

```

New text:

```
        if self._session is not None:

```

### `r705-b.S4_vendored_never_attaches_to_the_tool`

the tool's own session is not gated, so its login and every download lookup go out unpaced

- File: `src/cratekit/acquire/vendored.py`
- Source: `r705-b.json`, row `S4_vendored_never_attaches_to_the_tool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park`

Old text:

```
        self._gate.attach(tidal.session)

```

New text:

```
        pass

```

### `r705-b.S5_vendored_never_asks_after_login`

a park the tool swallowed inside its login reads as a rejected session

- File: `src/cratekit/acquire/vendored.py`
- Source: `r705-b.json`, row `S5_vendored_never_asks_after_login`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate.py::test_a_rate_limited_login_comes_out_of_the_vendored_adapter_as_the_park`

Old text:

```
        self._gate.raise_if_parked()
        if not authorised:

```

New text:

```
        if not authorised:

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

### `u274.V11_defect_swallowed`

drive: swallow a defect at the close of a drive that returned

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V11_defect_swallowed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`

Old text:

```
        except Exception:
            if finished:
                raise

```

New text:

```
        except Exception:
            pass

```

### `u274.V12_scope_per_invocation`

VendoredAdapter._session_scope: ignore the drive, so every track materialises and logs in again

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V12_scope_per_invocation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 16 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_drive_reads_the_keychain_as_a_one_track_drive_does_and_writes_nothing`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_tool_is_built_and_pointed_at_one_token_file_for_the_whole_drive`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        held = _DRIVE.get()
        if held is not None:
            return nullcontext(held)

```

New text:

```
(empty)
```

### `u274.V1_refusal_forgotten`

_refuse_if_refused: ask nothing, so a source that met a refusal logs in or asks again

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V1_refusal_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 4 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_fetch_that_meets_a_dead_session_is_remembered`
  - `tests/test_vendored_drive.py::test_a_refusal_outlives_the_source_it_was_met_on`
  - `tests/test_vendored_drive.py::test_a_refused_source_raises_again_with_no_call`
  - `tests/test_vendored_drive.py::test_a_session_refused_mid_track_is_never_asked_again`

Old text:

```
        if self._refused is not None:
            raise AdapterAuthFailed(str(self._refused), remedy=self._refused.remedy)

```

New text:

```
        pass

```

### `u274.V2_login_refusal_unrecorded`

authenticate: do not record a refused login, so a later track of the drive logs in again into the refused session

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V2_login_refusal_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 2 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_refusal_outlives_the_source_it_was_met_on`
  - `tests/test_vendored_drive.py::test_a_refused_source_raises_again_with_no_call`

Old text:

```
        except AdapterAuthFailed as refused:
            self._refused = refused
            raise

```

New text:

```
        except AdapterAuthFailed as refused:
            raise

```

### `u274.V3_offer_refusal_unrecorded`

offer: do not record a dead session met on a lookup

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V3_offer_refusal_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_session_refused_mid_track_is_never_asked_again`

Old text:

```
            except AdapterAuthFailed as dead:
                self._refused = dead
                raise
            raise

```

New text:

```
            except AdapterAuthFailed as dead:
                raise
            raise

```

### `u274.V4_fetch_refusal_unrecorded`

fetch: do not record a dead session met in a download

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V4_fetch_refusal_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_fetch_that_meets_a_dead_session_is_remembered`

Old text:

```
        except AdapterAuthFailed as dead:
            self._refused = dead
            raise

    def _fetch
```

New text:

```
        except AdapterAuthFailed as dead:
            raise

    def _fetch
```

### `u274.V5_source_per_track`

_Drive.source: never reuse the held source, so every track logs in again (the card's six calls a track)

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V5_source_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 14 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_broken_item_fails_alone_and_the_job_stays_resumable`
  - `tests/test_vendored_drive.py::test_a_drive_signalled_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_drive_torn_down_mid_track_leaves_no_token_file`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_session_withdrawn_mid_drive_parks_and_a_resume_lands_the_rest`
  - `tests/test_vendored_drive.py::test_a_ten_track_job_logs_in_once_and_spends_four_calls_a_track`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`
  - `tests/test_vendored_drive.py::test_every_call_of_the_drive_goes_through_the_gate`
  - `tests/test_vendored_drive.py::test_the_tool_is_built_and_pointed_at_one_token_file_for_the_whole_drive`
  - `tests/test_vendored_drive.py::test_two_drives_log_in_twice`

Old text:

```
        if held is not None and held.settings.gate == settings.gate:

```

New text:

```
        if False:

```

### `u274.V6_no_rebind`

_Drive.source: reuse the held source without this track's settings, so every track is told the first track's staging directory

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V6_no_rebind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_each_item_still_lands_in_its_own_staging_directory`

Old text:

```
            held.rebind(settings)
            return held

```

New text:

```
            return held

```

### `u274.V8_atmos_stored`

capture: store whatever the tool holds, a session left in its Atmos client included

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V8_atmos_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 1 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_session_left_in_the_atmos_client_is_not_stored`

Old text:

```
        if getattr(self._tidal, "is_atmos_session", False):
            return

```

New text:

```
(empty)
```

### `u274.V9_no_capture`

_Drive.close: skip the capture, so a refresh during the drive never reaches the keychain

- File: `src/cratekit/acquire/vendored.py`
- Source: `u274.json`, row `V9_no_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vendored_drive.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_contract.py`, `tests/test_provider_session_hold.py`, `tests/test_provider_gate.py`, `tests/test_handlers.py`
- Collected: 449 against a baseline of 449
- Kills: 7 (killed)
- Killed:
  - `tests/test_vendored_drive.py::test_a_defect_at_the_close_of_a_finished_drive_is_raised`
  - `tests/test_vendored_drive.py::test_a_refresh_before_a_withdrawal_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_in_a_drive_where_every_item_failed_still_reaches_the_keychain`
  - `tests/test_vendored_drive.py::test_a_refresh_the_keychain_cannot_take_is_a_warning_on_a_finished_download`
  - `tests/test_vendored_drive.py::test_a_token_file_that_cannot_be_written_at_the_close_is_a_warning`
  - `tests/test_vendored_drive.py::test_a_token_refreshed_during_the_drive_is_stored_once`
  - `tests/test_vendored_drive.py::test_an_index_that_refuses_after_the_keychain_took_the_session_is_a_warning`

Old text:

```
            if self._scope is not None and self._source is not None:
                self._source.capture(self._scope)

```

New text:

```
            pass

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

### `u47-author.CODEC_mp3_reads_as_lossless`

Flip MP3 to lossless in the container table, a realistic nearby value rather than a deletion

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_mp3_reads_as_lossless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.CODEC_no_refusal`

Accept whatever landed, which is the state the product shipped in from July: the rule enforced at the setting and never at the file

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_no_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.CODEC_none_reads_as_unreadable`

Treat a None codec as unreadable rather than as container-decided, which refuses every genuine FLAC because mutagen exposes info.codec on MP4 alone

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_none_reads_as_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.CODEC_refusal_drops_the_codec_name`

Reword the refusal so it no longer names the codec that actually arrived, leaving the reader with a refusal and no fact

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `CODEC_refusal_drops_the_codec_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R195_verify_skips_the_mapping`

Verify a hand-named pair rather than everything pushed, which is the source system's guard that watched two keys while the tool had more

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R195_verify_skips_the_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R196_absent_marker_reads_as_pkce`

Default a missing is_pkce to True, so a legacy device-flow token is read as a PKCE one

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_absent_marker_reads_as_pkce`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R196_accept_device_flow_session`

Stop refusing a stored device-flow session, so the product silently downloads lossy audio with it

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_accept_device_flow_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R196_no_stored_session_proceeds`

Proceed when there is no stored session at all

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R196_no_stored_session_proceeds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R197_drop_progress`

Drop progress from the downloader construction, half of the pair whose absence swallowed the failure

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_drop_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R197_drop_progress_overall`

Drop progress_overall from the downloader construction

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_drop_progress_overall`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R197_event_abort_preset`

Pass event_abort already set, which makes item() return (False, '') before it looks at anything

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_event_abort_preset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

### `u47-author.R197_progress_enabled`

Render the progress bars, so tool chatter reaches a stream a caller may be parsing (R32)

- File: `src/cratekit/acquire/vendored.py`
- Source: `u47-author.json`, row `R197_progress_enabled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_vendor_import.py`
- Collected: 201 against a baseline of 201
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

