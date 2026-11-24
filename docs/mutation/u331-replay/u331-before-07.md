# Mutation table: u331-before-07

Measured by `scripts/mutate.py` on 2026-11-23 23:54 UTC, branch `HEAD` at `c0bb16a4`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22808 collected. pytest invocations for this batch: 60.

Full baseline: measured by this driver (the battery's verdict was not read: it was measured on another machine, or before this one last started).

Subset baselines: 36, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 139 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22808 against 22808. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r289-b.C2_fallback_resume_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `r289-b.C3_fallback_queue_call_site` | `src/cratekit/acquire/fallback_cli.py` | user | 2 file(s) | 72 | 1 | killed |
| `r679-b.D2_fallback_gate_on_question_alone` | `src/cratekit/acquire/fallback_cli.py` | user | 3 file(s) | 833 | 1 | killed |
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
| `r395.M9_worker_literal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `r744.B1_window_not_bound` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 238 | 1 | killed |
| `u157.A1_no_level_tag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 213 | 1 | killed |
| `u157.A2_cut_unbound` | `src/cratekit/analysis/cli.py` | user | 3 file(s) | 278 | 3 | killed |
| `u192.A1_run_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 11 | killed |
| `u192.A2_restamp_queue_only_ignored` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 3 | killed |
| `u192.A3_restamp_wrong_resume` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M11_no_fallback` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u223.M12_renamed_to_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M13_resumed_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M14_any_status` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M15_folder_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M17_claim_failure_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M18_refused_rename_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u223.M19_attempt_start_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u223.M20_twin_target_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u241.M13_vocal_model_not_kept_back` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M19_failed_run_does_not_say_its_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 4 | killed |
| `u241.M20_held_job_records_a_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u241.M21_no_check_line_on_the_answer` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 12 | killed |
| `u241.M25_an_idle_resume_overwrites_the_pool` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 272 | 1 | killed |
| `u276.K11_run_binding_names_whole` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 24 | 2 | killed |
| `u306.A1_zero_told_apart` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 1 | killed |
| `u306.A2_zero_state` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 4 | killed |
| `u306.A3_walk_recursive` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 18 | killed |
| `u306.A4_walk_warnings` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 4 | killed |
| `u306.A7_calibrate_handler` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 44 | killed |
| `u58-workers-and-wav.R2_extra_not_required` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u58-workers-and-wav.R4_keyless_finalized` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u58-workers-and-wav.R5_tag_write_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u58-workers-and-wav.R7_absent_energy_stamped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u58-workers-and-wav.R8_title_without_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u58-workers-and-wav.R9_missing_file_analysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 2 | killed |
| `u58-workers-and-wav.S2_unchanged_rewritten` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u58-workers-and-wav.S3_queue_without_calibration` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 3 | killed |
| `u90-a.A7_exclusive_group_gone` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 173 | 1 | killed |
| `u93-recursive-analysis.D21_restamp_flag` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 18 | killed |
| `u93-recursive-analysis.D22_restamp_resume_warning` | `src/cratekit/analysis/cli.py` | user | 2 file(s) | 207 | 2 | killed |
| `u93-recursive-analysis.D24_restamp_join` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 207 | 1 | killed |
| `u94-c.N6_default_sample_halved` | `src/cratekit/analysis/cli.py` | maintainer | 2 file(s) | 207 | 1 | killed |
| `u162.R10_latest_verb` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R1_area_exists` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R2_rekordbox_closed` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R3_clone_is_a_link` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R4_snapshots_copied` | `src/cratekit/core/rehearsal.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u162.R5_locks_copied` | `src/cratekit/core/rehearsal.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u162.R7_witness_database` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 1 | killed |
| `u162.R8_witness_folders` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 3 | killed |
| `u162.R9_latest_key` | `src/cratekit/core/rehearsal.py` | user | 2 file(s) | 69 | 2 | killed |
| `u188.M14_mapped_in_given_order` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M15_mapped_shortest_first` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M16_mapped_by_live_length` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u188.M17_empty_scratch_kept` | `src/cratekit/core/rehearsal.py` | user | 1 file(s) | 25 | 1 | killed |
| `u206.M20_rehearsal_cache_not_kept_live` | `src/cratekit/core/rehearsal.py` | user | 9 file(s) | 1130 | 1 | killed |
| `r1264.M14_check_unread_moved` | `src/cratekit/sync/pair_check.py` | user | 2 file(s) | 49 | 1 | killed |
| `r1264.M15_check_unread_as_tuple` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 20 | 1 | killed |
| `r1385.M12_check_reads_no_job` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 292 | 2 | killed |
| `r1420-b.B2_beyond_tail_unread_pinned` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 1 | killed |
| `r1420.B1_beyond_order_unread` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 8 | killed |
| `r1420.B3_beyond_removals_asked` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 3 | killed |
| `r1420.N1_fix_reverted` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 7 | killed |
| `r1420.N2_moves_begun_ignored` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1420.N3_finish_read_too` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1420.N5_order_always_read` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 6 | killed |
| `r1420.N6_call_site_never_reads_order` | `src/cratekit/sync/pair_check.py` | user | 21 file(s) | 762 | 8 | killed |
| `u209.C10_reverse_recheck` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C11_home_of` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C12_brought_folder` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C13_jobs_queued` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 2 | killed |
| `u209.C3_withheld` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C4_rekordbox_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C5_memberships` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C6_discovered_place` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 5 | killed |
| `u209.C7_made_left_behind` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C8_rows_gone` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.C9_unpaired_back` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u209.H1_offer_mismatch_ignored` | `src/cratekit/sync/pair_check.py` | user | 5 file(s) | 208 | 1 | killed |
| `u210.R10_check_todo` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R11_part_written` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 6 | killed |
| `u210.R12_our_folders` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 5 | killed |
| `u210.R14_asked_before` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 9 | killed |
| `u210.R18_beyond_order` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R19_beyond_gained` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R20_beyond_lost` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R21_check_queued` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R22_landed_read` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 265 | 1 | killed |
| `u226.M20_check_no_lag` | `src/cratekit/sync/pair_check.py` | user | 8 file(s) | 267 | 1 | killed |
| `u246.S12_pair_cli_made_here_empty` | `src/cratekit/sync/pair_check.py` | user | 1 file(s) | 14 | 1 | killed |
| `u246.S13_pair_cli_per_element` | `src/cratekit/sync/pair_check.py` | maintainer | 2 file(s) | 79 | 1 | killed |
| `r1264.M12_record_holds_back` | `src/cratekit/sync/pair_write.py` | user | 2 file(s) | 49 | 5 | killed |
| `r1372.K17_no_let_go_at_snapshot` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 2 | killed |
| `r1372.K1_no_carry` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 9 | killed |
| `r1372.K4_carry_unwritten_not_refused` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1394.P1_counts_never_written` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 4 | killed |
| `r1394.P2_counts_not_carried` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1394.P3_begun_answers_no_recorder` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 5 | killed |
| `r1394.P9_finish_not_held_to_the_agreed_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `r1411.W1_finish_passes_no_agreed` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 10 | killed |
| `r1411.W2_finish_passes_agreed_only_with_nothing_else` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 7 | killed |
| `r1411.W3_agreed_is_the_asked_order` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 10 | killed |
| `r1411.W4_agreed_is_the_checks_listing` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `r1418.F1_agreed_is_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 1 | killed |
| `r1418.F2_agreed_passed_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | maintainer | 10 file(s) | 394 | 1 | killed |
| `r1418.F3_agreed_passed_only_for_an_empty_reading` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 11 | killed |
| `r1418.F4_agreed_only_without_adds_or_removes` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 7 | killed |
| `r1420.C1_continued_ignored` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 4 | killed |
| `r1420.C3_continued_read_after_the_mark` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 1 | killed |
| `r1420.C4_carried_record_unread` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 2 | killed |
| `r1420.E2_finish_agreed_dropped` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 10 | killed |
| `r1434.F7_ordering_start_from_the_readable_tracks` | `src/cratekit/sync/pair_write.py` | user | 10 file(s) | 394 | 3 | killed |
| `u130-c.C1_half_written_snapshot` | `src/cratekit/sync/pair_write.py` | user | 1 file(s) | 76 | 6 | killed |
| `u198.C9_account_only` | `src/cratekit/sync/pair_write.py` | user | 3 file(s) | 168 | 1 | killed |
| `u202.C4_dates_recorded` | `src/cratekit/sync/pair_write.py` | user | 3 file(s) | 160 | 6 | killed |
| `u210.R1_made_step_read` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R2_resumed_move` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R3_made_here_folder` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R4_rekordbox_landed` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 2 | killed |
| `u210.R5_queue_once` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 1 | killed |
| `u210.R8_done_step` | `src/cratekit/sync/pair_write.py` | user | 8 file(s) | 265 | 3 | killed |
| `u216.M20_made_drops_held` | `src/cratekit/sync/pair_write.py` | user | 12 file(s) | 385 | 9 | killed |
| `u225.M21_start_from_asked` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M22_written_always` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M23_links_dropped` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `u231.M10_moved_unrecorded` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M11_snapshot_from_the_order_sent` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 15 | killed |
| `u231.M12_settle_takes_any_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 12 | killed |
| `u231.M13_settle_sleeps_the_whole_window` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M14_settle_reading_not_kept` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M23_carried_moving_unread` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M7_continue_resends` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 6 | killed |
| `u231.M8_no_record_sends_blind` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 1 | killed |
| `u234.S1_sample_finish_held_to_the_plans_reading` | `src/cratekit/sync/pair_write.py` | user | 21 file(s) | 762 | 10 | killed |
| `u304.S5_settle_window_clock` | `src/cratekit/sync/pair_write.py` | user | 2 file(s) | 107 | 1 | killed |
| `u304.S6_settle_moment_clock` | `src/cratekit/sync/pair_write.py` | user | 2 file(s) | 107 | 1 | killed |
| `r263.S2_favorites_reason` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 1 | killed |
| `u109-b.B1_labels_not_guided` | `src/cratekit/sync/sources.py` | user | 3 file(s) | 228 | 13 | killed |
| `u109-b.B2_command_spelling` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 197 | 9 | killed |
| `u109-b.B3_no_cursor_reworded` | `src/cratekit/sync/sources.py` | user | 1 file(s) | 31 | 3 | killed |
| `u74.A1_no_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 26 | killed |
| `u74.A2_wrong_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 14 | killed |

## Considered and dropped

Recorded rows this replay left out and did NOT measure. They are not coverage, and `scripts/killset.py check` fails on one that was killed before and is neither a row nor mapped here.

- `u241-dsp.D4_settings_not_handed_to_the_head`: handle_run: the item's settings are not compared with the workers', so a real run stops its pool at the first head Dropped because: owed to the macOS battery, not measured: every test file its subset names skips whole on a cloud container, which has no audio libraries, so the subset collects nothing and the driver refuses it (U306 left the same row out for the same reason)

## Row definitions

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
- Collected: 833 against a baseline of 833
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

### `r395.M9_worker_literal`

Put the old bare pip literal back in the analysis worker refusal

- File: `src/cratekit/analysis/cli.py`
- Source: `r395.json`, row `M9_worker_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `r744.B1_window_not_bound`

the run binds the shipped window rather than the configured one, so analysis.tempo_floor and tempo_ceiling change nothing

- File: `src/cratekit/analysis/cli.py`
- Source: `r744.json`, row `B1_window_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_head_agreement.py`, `tests/test_analysis_workers.py`
- Collected: 238 against a baseline of 238
- Kills: 1 (killed)
- Killed:
  - `tests/test_head_agreement.py::test_a_raised_window_loads_and_reaches_the_detector_binding`

Old text:

```
            tempo_window=(cfg.analysis.tempo_floor, cfg.analysis.tempo_ceiling),
```

New text:

```
            tempo_window=(80, 160),
```

### `u157.A1_no_level_tag`

_finalize: write no driftlevel tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A1_no_level_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`
- Collected: 213 against a baseline of 213
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_a_measured_drift_is_written_as_its_level_and_verdict`

Old text:

```
        "driftlevel": _drift_level(scored.get("drift")),
```

New text:

```
        "driftlevel": None,
```

### `u157.A2_cut_unbound`

_bind_defaults: bind no drift cut, so the detector reads the shipped default

- File: `src/cratekit/analysis/cli.py`
- Source: `u157.json`, row `A2_cut_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_analysis_workers.py`, `tests/test_head_agreement.py`
- Collected: 278 against a baseline of 278
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

### `u192.A1_run_queue_only_ignored`

analyze_run: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A1_run_queue_only_ignored`
- Moved: Same branch in analyze_run; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
- Kills: 11 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`
  - `tests/test_analysis_workers.py::test_an_item_renamed_before_its_row_moved_resumes_as_finished`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[run]`
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

### `u192.A2_restamp_queue_only_ignored`

analyze_restamp: ignore --queue-only and drive the job

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A2_restamp_queue_only_ignored`
- Moved: Same branch in analyze_restamp; U298 replaced the local _reported with core.jobs.reported
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_resumes_after_a_kill_and_finishes_the_rest`
  - `tests/test_analysis_workers.py::test_queue_only_returns_the_job_queued_with_nothing_driven[restamp]`

Old text:

```
        if foreground.queue_only(ctx.args):
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
```

New text:

```
        if False:
            return ctx.envelope(
                data=jobs.reported(store, job), warnings=(DB_NOT_WRITTEN, *extra)
```

### `u192.A3_restamp_wrong_resume`

analyze_restamp: name the analyze run command as the one that resumes an interrupted restamp

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A3_restamp_wrong_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u223.M11_no_fallback`

_finalized_twin: no staged report fallback when the intent is gone

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M11_no_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
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

### `u223.M12_renamed_to_unchecked`

_staged_twin: accept an analysed report whatever its renamed_to says

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M12_renamed_to_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u223.M13_resumed_unchecked`

_staged_twin: accept any prefixed skip, not only a resume's

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M13_resumed_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u223.M14_any_status`

_staged_twin: accept a report of any status

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M14_any_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u223.M15_folder_unchecked`

_staged_twin: accept a path outside the item's own folder

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M15_folder_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u223.M17_claim_failure_keeps_evidence`

_finalize: keep the intent when the target name is taken

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M17_claim_failure_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_leaves_no_intent_behind`

Old text:

```
        # read that unrelated file as this item's twin (U223).
        artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
        # read that unrelated file as this item's twin (U223).
```

### `u223.M18_refused_rename_keeps_evidence`

_finalize: keep the intent when the rename is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M18_refused_rename_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`

Old text:

```
        target.unlink(missing_ok=True)
        artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
        target.unlink(missing_ok=True)
```

### `u223.M19_attempt_start_keeps_evidence`

handle_run: keep stale evidence when the source is still a file

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M19_attempt_start_keeps_evidence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`

Old text:

```
    # it renames (U223).
    artifacts.discard_rename_evidence(cfg, job, item)
```

New text:

```
    # it renames (U223).
```

### `u223.M20_twin_target_unchecked`

_finalized_twin: an existing guard, accept a target that is not a file

- File: `src/cratekit/analysis/cli.py`
- Source: `u223.json`, row `M20_twin_target_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u241.M13_vocal_model_not_kept_back`

_open_ahead: the driver's vocal model is not kept back from the light pool's budget

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M13_vocal_model_not_kept_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
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

### `u241.M19_failed_run_does_not_say_its_pool`

_resume: a run that failed or was stopped leaves without its pool line

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M19_failed_run_does_not_say_its_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
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

### `u241.M20_held_job_records_a_pool`

_heads_ahead: a call that drove nothing, because another driver holds the job, records a pool anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M20_held_job_records_a_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
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

### `u241.M21_no_check_line_on_the_answer`

_resume: the answer no longer carries the analyze.pool check

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M21_no_check_line_on_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
- Kills: 12 (killed)
- Killed:
  - `tests/test_analysis_ahead.py::test_a_closure_bound_by_a_test_is_never_sent_to_a_worker`
  - `tests/test_analysis_ahead.py::test_a_healthy_machine_says_how_many_workers_and_that_the_ceiling_held_it`
  - `tests/test_analysis_ahead.py::test_a_job_whose_record_is_gone_says_it_does_not_know`
  - `tests/test_analysis_ahead.py::test_a_job_with_nothing_waiting_says_so_and_starts_nothing`
  - `tests/test_analysis_ahead.py::test_a_machine_deep_in_swap_runs_one_worker_and_names_the_swap_gate`
  - `tests/test_analysis_ahead.py::test_a_machine_using_most_of_its_memory_names_the_used_percent_gate`
  - `tests/test_analysis_ahead.py::test_a_pool_record_that_cannot_be_written_is_a_missing_line_and_never_a_failed_job`
  - `tests/test_analysis_ahead.py::test_a_resume_of_a_finished_job_still_says_what_pool_it_ran_with`
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

### `u241.M25_an_idle_resume_overwrites_the_pool`

_worth_recording: a drive that measured nothing overwrites the record of the drive that did

- File: `src/cratekit/analysis/cli.py`
- Source: `u241.json`, row `M25_an_idle_resume_overwrites_the_pool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_ahead.py`
- Collected: 272 against a baseline of 272
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

### `u276.K11_run_binding_names_whole`

analysis/cli.py: the driver's detector binding names the whole method, so analyze run separates whatever the default says

- File: `src/cratekit/analysis/cli.py`
- Source: `u276.json`, row `K11_run_binding_names_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_key_default.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_key_default.py::test_no_shipped_caller_of_the_detector_names_a_key_method`
  - `tests/test_analysis_key_default.py::test_the_runs_shipped_bindings_name_no_method_so_they_take_the_default[cli.py]`

Old text:

```
            drift_cut=cfg.analysis.drift_cut,
        )
        light.bind_detect(_BOUND_DETECT)
```

New text:

```
            drift_cut=cfg.analysis.drift_cut,
            key=detect.KEY_WHOLE,
        )
        light.bind_detect(_BOUND_DETECT)
```

### `u306.A1_zero_told_apart`

analysis.cli.nothing_to_queue: read every zero as an empty folder, so a mistyped or unmounted folder says nothing new to do for analyze, restamp and vocals

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A1_zero_told_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
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

### `u306.A2_zero_state`

analysis.cli.nothing_to_queue: the default state of an empty folder reworded, so the no job payload names another state

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A2_zero_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
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

### `u306.A3_walk_recursive`

analysis.cli.walk_folder: ignore --recursive, so a nested file is never queued by restamp or vocals

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A3_walk_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
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

### `u306.A4_walk_warnings`

analysis.cli.walk_folder: drop the walk's warnings, so a folder it could not list or a link it declined is never told

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A4_walk_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_recursive_restamp_says_which_linked_folders_it_did_not_walk`
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_a_tree_whose_only_folders_are_links_says_so_on_the_zero`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`

Old text:

```
    return folder, recursive, scan, discovery.walk_warnings(scan.skipped_links, scan.unreadable)
```

New text:

```
    return folder, recursive, scan, ()
```

### `u306.A7_calibrate_handler`

analysis.cli.analyze_calibrate: the handler answers the validate verb's envelope instead of running the calibrate body

- File: `src/cratekit/analysis/cli.py`
- Source: `u306.json`, row `A7_calibrate_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u58-workers-and-wav.R2_extra_not_required`

Drop the missing extra refusal in the run worker

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R2_extra_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u58-workers-and-wav.R4_keyless_finalized`

Finalize a track whose head found no key

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R4_keyless_finalized`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u58-workers-and-wav.R5_tag_write_unchecked`

Ignore a failed tag write and rename anyway

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R5_tag_write_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`

Old text:

```
    _write_or_refuse(path, fields, untouched="The file is untouched and was not renamed")
```

New text:

```
    tags.write_tags(path, fields)
```

### `u58-workers-and-wav.R7_absent_energy_stamped`

Write a level for an absent energy

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R7_absent_energy_stamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u58-workers-and-wav.R8_title_without_head`

Write the bare stem as the title tag

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R8_title_without_head`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_analyze_job_runs_pending_to_done_and_the_files_carry_the_result`

Old text:

```
        "title": rendered.title_tag,
```

New text:

```
        "title": path.stem,
```

### `u58-workers-and-wav.R9_missing_file_analysed`

Drop the source-missing refusal for a file that vanished

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R9_missing_file_analysed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u58-workers-and-wav.S2_unchanged_rewritten`

Rewrite a file whose level did not move

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S2_unchanged_rewritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u58-workers-and-wav.S3_queue_without_calibration`

Queue a restamp over a library that has no calibration

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `S3_queue_without_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_restamp_with_no_calibration_refuses_at_the_queue`
  - `tests/test_analysis_workers.py::test_the_restamp_refusal_names_the_library_wide_calibrate`

Old text:

```
    # REFUSED AT THE QUEUE, not only in the worker: a job whose every item
    # would fail on the same absence is a report over work nothing could do.
    _calibration_or_refuse(cfg)

```

New text:

```
(empty)
```

### `u90-a.A7_exclusive_group_gone`

The folder and the flag no longer mutually exclusive in the parser

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A7_exclusive_group_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 173 against a baseline of 173
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

### `u93-recursive-analysis.D21_restamp_flag`

The restamp queue ignores the flag and always scans one level

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D21_restamp_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
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
    scan = discovery.scan_audio(folder, recursive=recursive)
```

New text:

```
    recursive = bool(getattr(ctx.args, "recursive", False))
    scan = discovery.scan_audio(folder, recursive=False)
```

### `u93-recursive-analysis.D22_restamp_resume_warning`

The restamp resume drops the walk's omissions, leaving them on the queue envelope only

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D22_restamp_resume_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_driven_at_its_queue_names_a_linked_folder_once`
  - `tests/test_analysis_workers.py::test_the_resume_repeats_what_the_walk_left_out_rather_than_only_the_queue`

Old text:

```
        warnings = (*warnings, *discovery.warnings_of(job.payload))
        if job.handler_key == "analyze.restamp":
```

New text:

```
        if job.handler_key == "analyze.restamp":
```

### `u93-recursive-analysis.D24_restamp_join`

The restamp worker joins the item id with the operator instead of the checked rule

- File: `src/cratekit/analysis/cli.py`
- Source: `u93-recursive-analysis.json`, row `D24_restamp_join`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_restamp_item_that_would_leave_the_frozen_folder_is_refused`

Old text:

```
    return folder, discovery.item_path(folder, str(item.item_id))
```

New text:

```
    return folder, folder / item.item_id
```

### `u94-c.N6_default_sample_halved`

DEFAULT_CALIBRATION_SAMPLE: halve the coefficient, 500 to 250

- File: `src/cratekit/analysis/cli.py`
- Source: `u94-c.json`, row `N6_default_sample_halved`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_vocals_cli.py`
- Collected: 207 against a baseline of 207
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

### `u162.R10_latest_verb`

latest: match a record by key alone, so another verb's rehearsal is compared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R10_latest_verb`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
            and body.get("verb") == verb

```

New text:

```
(empty)
```

### `u162.R1_area_exists`

open_area: drop the refusal of an area that already exists, so one area is shared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R1_area_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
        if path.exists():
```

New text:

```
        if False:
```

### `u162.R2_rekordbox_closed`

open_area: drop the closed rekordbox check before the copy

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R2_rekordbox_closed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_empty_staging_rehearses_nothing_and_rekordbox_refuses`

Old text:

```
    rb_writer.assert_rekordbox_closed("copying the database for a rehearsal")

```

New text:

```
(empty)
```

### `u162.R3_clone_is_a_link`

clone: a hard link where the volume does not clone

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R3_clone_is_a_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_clone_is_never_a_hard_link_and_the_plan_lines_name_every_leaf`

Old text:

```
    shutil.copy2(source, destination)
```

New text:

```
    os.link(source, destination)
```

### `u162.R4_snapshots_copied`

_NOT_COPIED: copy the snapshots directory into the area

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R4_snapshots_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
        "snapshots",

```

New text:

```
(empty)
```

### `u162.R5_locks_copied`

_copy_library_state: copy lock files into the area

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R5_locks_copied`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
        if entry.key in _NOT_COPIED or entry.key.endswith("_lock"):
```

New text:

```
        if entry.key in _NOT_COPIED:
```

### `u162.R7_witness_database`

assert_untouched: drop the live database hash comparison

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R7_witness_database`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_the_witness_refuses_a_live_change`

Old text:

```
    if _hashes(before.database) != before.hashes:
```

New text:

```
    if False:
```

### `u162.R8_witness_folders`

assert_untouched: drop the live folder listing comparison

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R8_witness_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_another_year_s_batch_is_refused`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_that_touched_the_live_library_is_refused`
  - `tests/test_intake_land_rehearse.py::test_the_witness_refuses_a_live_change`

Old text:

```
        if _listed(Path(folder)) != listing:
```

New text:

```
        if False:
```

### `u162.R9_latest_key`

latest: match a record by verb alone, so another batch's rehearsal is compared

- File: `src/cratekit/core/rehearsal.py`
- Source: `u162.json`, row `R9_latest_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`, `tests/test_intake_land_native.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_a_live_plan_names_its_own_batch_s_rehearsal_and_the_lines`
  - `tests/test_intake_land_rehearse.py::test_two_areas_are_apart_and_copy_library_state_only`

Old text:

```
            and body.get("key") == dict(key)

```

New text:

```
(empty)
```

### `u188.M14_mapped_in_given_order`

rehearsal.mapped: apply the pairs in the order given, so a scratch spelling holding another's is half mapped

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M14_mapped_in_given_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            key=lambda pair: len(pair[0]),
            reverse=True,
```

New text:

```
            key=lambda pair: 0,
            reverse=True,
```

### `u188.M15_mapped_shortest_first`

rehearsal.mapped: shortest scratch spelling first

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M15_mapped_shortest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            key=lambda pair: len(pair[0]),
            reverse=True,
```

New text:

```
            key=lambda pair: len(pair[0]),
            reverse=False,
```

### `u188.M16_mapped_by_live_length`

rehearsal.mapped: order by the live spelling's length rather than the scratch one's

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M16_mapped_by_live_length`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            key=lambda pair: len(pair[0]),
```

New text:

```
            key=lambda pair: len(pair[1]),
```

### `u188.M17_empty_scratch_kept`

rehearsal.mapped: keep an empty scratch spelling, which inserts the live one between every character

- File: `src/cratekit/core/rehearsal.py`
- Source: `u188.json`, row `M17_empty_scratch_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_rehearse.py`
- Collected: 25 against a baseline of 25
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_rehearse.py::test_mapped_applies_the_longest_spelling_first_and_the_refusal_names_each_field_once`

Old text:

```
            ((scratch, live) for scratch, live in replacements if scratch),
```

New text:

```
            ((scratch, live) for scratch, live in replacements),
```

### `u206.M20_rehearsal_cache_not_kept_live`

rehearsal.redirected: do not point the ISRC cache at the live directory, so a rehearsal's answers are thrown away

- File: `src/cratekit/core/rehearsal.py`
- Source: `u206.json`, row `M20_rehearsal_cache_not_kept_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 1 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_rehearsal_keeps_the_live_isrc_cache_and_restores_the_environment`

Old text:

```
    os.environ[config.ENV_ISRC_CACHE_DIR] = saved[config.ENV_ISRC_CACHE_DIR] or str(
        config.state_path("isrc_cache").parent
    )
```

New text:

```
    os.environ.pop(config.ENV_ISRC_CACHE_DIR, None)
```

### `r1264.M14_check_unread_moved`

check: never read the unread tracks as moved, so a new unread track after the plan is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1264.json`, row `M14_check_unread_moved`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_track_turning_unreadable_between_the_plan_and_the_write_refuses_stale`

Old text:

```
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
```

New text:

```
            unread_moved = False
```

### `r1264.M15_check_unread_as_tuple`

check: compare the unread tracks by place, so tracks trading places refuses stale

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1264.json`, row `M15_check_unread_as_tuple`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`
- Collected: 20 against a baseline of 20
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`

Old text:

```
            unread_moved = set(listing.unread) != {named.remote_id for named in one.unread}
```

New text:

```
            unread_moved = tuple(listing.unread) != tuple(named.remote_id for named in one.unread)
```

### `r1385.M12_check_reads_no_job`

check: read no job at apply time, so a job another sync queued since the plan is queued again beside it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1385.json`, row `M12_check_reads_no_job`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_unread.py`, `tests/test_intake_land_twins.py`
- Collected: 292 against a baseline of 292
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            for job in pair_jobs(cfg, store)
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

New text:

```
            for job in ()
            for item in (job.payload or {}).get(intake_cli.TRACKS) or {}
        }
```

### `r1420-b.B2_beyond_tail_unread_pinned`

sample: the part written check reads the kept tracks' order but not that this write's additions stand after them, measured again once a test pins it

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420-b.json`, row `B2_beyond_tail_unread_pinned`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != kept + tail
        ):
```

New text:

```
        if kept != [track for track in one.account_now if track in held] or (
            list(now) != list(now)
        ):
```

### `r1420.B1_beyond_order_unread`

sample: the part written check never reads the order, whatever ordering says

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B1_beyond_order_unread`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if not parts and ordering is None:
```

### `r1420.B3_beyond_removals_asked`

sample: the kept order is compared to the whole plan's reading, so a track this write took off reads as a reorder

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `B3_beyond_removals_asked`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
        if kept != [track for track in one.account_now if track in held] or (
```

New text:

```
        if kept != [track for track in one.account_now] or (
```

### `r1420.N1_fix_reverted`

the check leaves the order unread once ordering is marked, as before R-1420, so a person's reorder after an order that moved nothing is written over

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N1_fix_reverted`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING)
```

### `r1420.N2_moves_begun_ignored`

a pair whose moves began has its order read, so a continue of a stop part way through the moves refuses the moves' own order as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N2_moves_begun_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and one.finishing_order
```

### `r1420.N3_finish_read_too`

a finish of a stopped order has its order read by the check, so a continue of a refused finish whose check lists the lag is held as moved rather than refused at the adapter

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N3_finish_read_too`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return steps.has(STEP_ORDERING) and steps.has(STEP_MOVING)
```

### `r1420.N5_order_always_read`

every part written pair has its order read, the moves' own included

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N5_order_always_read`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
    return steps.has(STEP_ORDERING) and (steps.has(STEP_MOVING) or one.finishing_order)
```

New text:

```
    return False and steps.has(STEP_ORDERING)
```

### `r1420.N6_call_site_never_reads_order`

the check passes ordering as true for every part written pair, so no order is read once an account write began

- File: `src/cratekit/sync/pair_check.py`
- Source: `r1420.json`, row `N6_call_site_never_reads_order`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_after_a_change_no_move_of_the_run_recorded_holds_it_as_moved`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_a_reorder_made_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_that_also_added_holds_the_added_track_moved_since`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_stopped_before_any_move_holds_a_reorder_made_since[parked]`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
                why = _beyond(one, now, ordering=_ordered_by_this_run(one, of(one)))
```

New text:

```
                why = _beyond(one, now, ordering=True)
```

### `u209.C10_reverse_recheck`

check: run no recheck of a made rekordbox side's home before the write

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C10_reverse_recheck`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlists_folder_gone_reads_as_one_sentence`
  - `tests/test_sync_pair_hold_every.py::test_a_rekordbox_name_taken_before_the_write_stops_every_pair_before_any_is_written`

Old text:

```
                    pair_reverse.recheck(db, one.home, one.change.order)
```

New text:

```
                    pass
```

### `u209.C11_home_of`

check: compare no home a made rekordbox side goes to with the plan's

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C11_home_of`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlists_rekordbox_folder_archived_before_the_write_refuses_stale`

Old text:

```
                if now != one.home:
```

New text:

```
                if False:
```

### `u209.C12_brought_folder`

check: read no brought playlist taken out of its account folder

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C12_brought_folder`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_brought_playlist_taken_out_of_its_account_folder_before_the_write_refuses_stale`

Old text:

```
            if listing.get(one.target.account_id) != one.target.title:
```

New text:

```
            if False:
```

### `u209.C13_jobs_queued`

check: read no acquisitions another sync queued since the plan

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C13_jobs_queued`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_another_pairs_job_queued_since_the_plan_refuses_the_write_as_stale`
  - `tests/test_sync_pair_hold.py::test_tracks_another_sync_queued_before_the_write_refuse_stale_not_twice`

Old text:

```
            again = sorted(set(one.acquire) & now)
```

New text:

```
            again = []
```

### `u209.C3_withheld`

check: read no change in the account's withheld count

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C3_withheld`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_withheld_count_changed_before_the_write_refuses_stale`

Old text:

```
            elif withheld != one.withheld:
```

New text:

```
            elif False:
```

### `u209.C4_rekordbox_gone`

check: read no rekordbox playlist deleted or turned into a folder

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C4_rekordbox_gone`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_rekordbox_playlist_deleted_before_the_write_refuses_stale`

Old text:

```
            if there is None or there.removed or not there.plain:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
```

New text:

```
            if there is None:
                moved.append(
                    Moved(
                        REKORDBOX_SIDE,
                        one.target.rekordbox_id,
```

### `u209.C5_memberships`

check: read no moved rekordbox membership

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C5_memberships`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair_hold.py::test_a_moved_list_is_checked_whichever_side_was_skipped`
  - `tests/test_sync_pair_hold.py::test_a_rekordbox_membership_changed_before_the_write_refuses_stale_and_names_it`
  - `tests/test_sync_pair_hold.py::test_both_sides_moved_are_both_named`
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_whose_rekordbox_side_moved_before_the_write_refuses_stale`

Old text:

```
            if there.memberships() != tuple(tuple(row) for row in one.rekordbox_before):
```

New text:

```
            if False:
```

### `u209.C6_discovered_place`

check: read no move of a discovered playlist's place

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C6_discovered_place`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_dragged_into_archive_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_into_a_subfolder_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_to_another_folder_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_to_the_root_before_the_write_refuses_stale`
  - `tests/test_sync_pair_hold_every.py::test_a_discovered_playlist_moved_where_discovery_never_pairs_refuses_stale`

Old text:

```
                if now_found is None or (now_found.folder, now_found.title) != (
```

New text:

```
                if False and (now_found.folder, now_found.title) != (
```

### `u209.C7_made_left_behind`

check: read no made pair dragged where no pair is kept

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C7_made_left_behind`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_dragged_into_archive_before_the_write_refuses_stale`

Old text:

```
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if why:
```

New text:

```
                why = pair_discover.left_behind(db, there, favorites=favorites, skip=skip)
                if False:
```

### `u209.C8_rows_gone`

check: read no row the plan adds gone from the collection

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C8_rows_gone`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_row_the_plan_adds_gone_before_the_write_stops_every_pair`

Old text:

```
            gone = sorted(set(one.change.adds) - set(playlist_pair.content(db, one.change.adds)))
```

New text:

```
            gone = []
```

### `u209.C9_unpaired_back`

check: read no let go playlist back where its pair is kept

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `C9_unpaired_back`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold_every.py::test_a_made_pair_let_go_in_archive_and_dragged_back_before_the_write_refuses_stale`

Old text:

```
            if not pair_discover.left_behind(db, there, favorites=favorites, skip=skip):
```

New text:

```
            if False:
```

### `u209.H1_offer_mismatch_ignored`

_held_plan: read back a held plan whatever offer the run recorded

- File: `src/cratekit/sync/pair_check.py`
- Source: `u209.json`, row `H1_offer_mismatch_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`
- Collected: 208 against a baseline of 208
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_hold.py::test_a_held_plan_other_than_the_offer_is_planned_again`

Old text:

```
    if moved:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
```

New text:

```
    if False:
        return None, 0, f"the held plan is not the plan {', '.join(moved)} showed"
```

### `u210.R10_check_todo`

check: read every pair, a finished one included

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R10_check_todo`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`

Old text:

```
    todo = [one for one in planned.pairs if not of(one).has(STEP_DONE)]
```

New text:

```
    todo = list(planned.pairs)
```

### `u210.R11_part_written`

check: read a part written existing pair exactly, as one not started

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R11_part_written`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`
  - `tests/test_sync_pair_resume_one.py::test_a_track_lost_from_the_part_written_account_playlist_refuses_stale`
  - `tests/test_sync_pair_resume_one.py::test_a_track_withheld_on_the_part_written_playlist_refuses_stale`

Old text:

```
            if one.target.new or of(one).has(STEP_ACCOUNT):
```

New text:

```
            if one.target.new:
```

### `u210.R12_our_folders`

check: read a folder this run made as not there for the pairs still to make in it

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R12_our_folders`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`

Old text:

```
            folder_id = place.folder_id or our_folders.get(place.folder, "")
```

New text:

```
            folder_id = place.folder_id
```

### `u210.R14_asked_before`

_asked_before: compare what is asked now unchanged, so a continue after the run's own marks plans again

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R14_asked_before`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[3-the move and the fill]`
  - `tests/test_sync_pair_resume.py::test_a_title_taken_in_the_folder_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`
  - `tests/test_sync_pair_resume_one.py::test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan`

Old text:

```
    return {**dict(asked), "targets": targets}
```

New text:

```
    return dict(asked)
```

### `u210.R18_beyond_order`

_beyond: read no order on a part written playlist

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R18_beyond_order`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_reorder_by_hand_on_the_part_written_playlist_refuses_stale`

Old text:

```
    if not parts and not ordering:
```

New text:

```
    if False:
```

### `u210.R19_beyond_gained`

_beyond: read no track gained

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R19_beyond_gained`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_track_put_on_a_part_made_playlist_before_the_continue_refuses_stale_naming_it`

Old text:

```
    gained = held - before - added
```

New text:

```
    gained = set()
```

### `u210.R20_beyond_lost`

_beyond: read no track lost

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R20_beyond_lost`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_track_lost_from_the_part_written_account_playlist_refuses_stale`

Old text:

```
    lost = (before - set(one.account_removes)) - held
```

New text:

```
    lost = set()
```

### `u210.R21_check_queued`

check: read the run's own queued job as another sync's

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R21_check_queued`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue`

Old text:

```
    asking = [one for one in todo if one.acquire and not of(one).has(STEP_QUEUED)]
```

New text:

```
    asking = [one for one in todo if one.acquire]
```

### `u210.R22_landed_read`

check: read no rekordbox playlist this run's commit landed

- File: `src/cratekit/sync/pair_check.py`
- Source: `u210.json`, row `R22_landed_read`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_rekordbox_playlist_changed_after_this_run_wrote_it_refuses_stale`

Old text:

```
                _landed_moved(db, one, landed, moved)
```

New text:

```
                pass
```

### `u226.M20_check_no_lag`

check: a lagging listing is compared as read rather than named as moved

- File: `src/cratekit/sync/pair_check.py`
- Source: `u226.json`, row `M20_check_no_lag`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_account.py`
- Collected: 267 against a baseline of 267
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_window_lag.py::test_a_window_that_starts_lagging_after_the_plan_stops_the_write_as_moved`

Old text:

```
            if listing.window == provider_listing.WINDOW_LAGS:
                # U226. Neither read
```

New text:

```
            if False:
                # U226. Neither read
```

### `u246.S12_pair_cli_made_here_empty`

pair: no account ids made this run, so discovery is told every pair, the ones this run made included, is already paired

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S12_pair_cli_made_here_empty`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`

Old text:

```
            made_here = set(ours.values())
```

New text:

```
            made_here = set()
```

### `u246.S13_pair_cli_per_element`

pair: build the made here set once per pair again (the shape on main)

- File: `src/cratekit/sync/pair_check.py`
- Source: `u246.json`, row `S13_pair_cli_per_element`
- Moved: the same text, now in src/cratekit/sync/pair_check.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_sync_pair_discover.py`
- Collected: 79 against a baseline of 79
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
                        if pair.account_id not in made_here
```

New text:

```
                        if pair.account_id not in set(ours.values())
```

### `r1264.M12_record_holds_back`

_record: hold the snapshot back while a track is unread, the round one defect

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1264.json`, row `M12_record_holds_back`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_hold.py`
- Collected: 49 against a baseline of 49
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_unread.py::test_a_row_read_through_its_second_release_moves_on_the_account_with_rekordbox`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_in_rekordbox_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_a_track_synced_across_and_then_removed_on_the_account_is_not_put_back`
  - `tests/test_sync_pair_unread.py::test_an_untitled_track_never_stops_its_pair_and_the_rest_syncs_both_ways`
  - `tests/test_sync_pair_unread.py::test_unread_tracks_trading_places_after_the_plan_is_not_stale`

Old text:

```
    whole = rekordbox_after is not None and account_after is not None and not one.withheld
```

New text:

```
    whole = (
        rekordbox_after is not None
        and account_after is not None
        and not one.withheld
        and not one.unread
    )
```

### `r1372.K17_no_let_go_at_snapshot`

_record: a snapshot recorded whole lets go of no carried record of its pair

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K17_no_let_go_at_snapshot`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`

Old text:

```
    if whole:
        _let_go_passed(one.target.account_id, recorded.synced)
```

New text:

```
    if False:
        _let_go_passed(one.target.account_id, recorded.synced)
```

### `r1372.K1_no_carry`

write: the pair's steps are not carried past the run as its order begins

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K1_no_carry`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        # whatever its age until the pair's snapshot passes it.
        steps.carry()
```

New text:

```
        # whatever its age until the pair's snapshot passes it.
        pass
```

### `r1372.K4_carry_unwritten_not_refused`

PairSteps.carry: a carry that cannot be written is swallowed and the moves go on

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K4_carry_unwritten_not_refused`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_that_cannot_be_kept_past_its_run_moves_nothing`

Old text:

```
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            raise steps_unwritten(self.steps.run_id, exc) from None
```

New text:

```
            held_plan.carry(self.steps, self.key)
        except OSError as exc:
            exc = exc
```

### `r1394.P1_counts_never_written`

pair write: the recorder writes the moving step with no progress, sent and landed always 0

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P1_counts_never_written`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
                        at=at, start=start, end=end, sent=sent, landed=landed
```

New text:

```
                        at=at, start=start, end=end, sent=0, landed=0
```

### `r1394.P2_counts_not_carried`

pair write: the recorder's counts are marked in the run's steps but not carried past the run

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P2_counts_not_carried`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
                steps.carry()

            return sending
```

New text:

```
                pass

            return sending
```

### `r1394.P3_begun_answers_no_recorder`

pair write: begun answers no recorder, so the adapter tells the record nothing between moves

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P3_begun_answers_no_recorder`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`

Old text:

```
            return sending
```

New text:

```
            return None
```

### `r1394.P9_finish_not_held_to_the_agreed_reading`

pair write: a write that finishes a stopped order lets the adapter plan its moves from any reading holding the same tracks, round one's row 1

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P9_finish_not_held_to_the_agreed_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`

Old text:

```
                or (one.finishing_order and not (one.account_removes or one.account_adds))
```

New text:

```
                or False
```

### `r1411.W1_finish_passes_no_agreed`

the pair write passes no agreed reading at a finish, the measured cost R-1411 names

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W1_finish_passes_no_agreed`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if False
```

### `r1411.W2_finish_passes_agreed_only_with_nothing_else`

the pair write passes agreed only at a finish that adds and removes nothing, as before this card

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W2_finish_passes_agreed_only_with_nothing_else`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if one.finishing_order
            and one.account_before
            and not (one.account_removes or one.account_adds)
```

### `r1411.W3_agreed_is_the_asked_order`

the pair write passes the order it asks as the agreed reading rather than the plan's reading

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W3_agreed_is_the_asked_order`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(one.account_order)}
```

### `r1411.W4_agreed_is_the_checks_listing`

round one's BLOCKING shape: the pair write passes the check's listing as the agreed reading when there is one

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1411.json`, row `W4_agreed_is_the_checks_listing`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(account_listed or one.account_before)}
```

### `r1418.F1_agreed_is_the_readable_tracks`

the brief's row: a finish is held to the tracks the provider could read, so a lag differing only by where an unread track stands is planned from

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F1_agreed_is_the_readable_tracks`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            {"agreed": tuple(one.account_before)}
```

New text:

```
            {"agreed": tuple(one.account_now)}
```

### `r1418.F2_agreed_passed_for_an_empty_reading`

the clause for an empty plan reading dropped, so a finish whose plan read no account passes an empty agreed order to an adapter that may not take it

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F2_agreed_passed_for_an_empty_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order
            else {}
```

### `r1418.F3_agreed_passed_only_for_an_empty_reading`

the clause inverted, so a finish whose plan read the account passes no agreed order and is held to membership alone

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F3_agreed_passed_only_for_an_empty_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 11 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_plan_read_no_account_passes_no_agreed_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order and not one.account_before
            else {}
```

### `r1418.F4_agreed_only_without_adds_or_removes`

existing guard, R-1411: a finish that also adds or removes passes no agreed order, as before R-1411

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1418.json`, row `F4_agreed_only_without_adds_or_removes`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if one.finishing_order
            and one.account_before
            and not (one.account_removes or one.account_adds)
            else {}
```

### `r1420.C1_continued_ignored`

a continue of an order parked or stopped with the whole write before any move passes the adapter no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C1_continued_ignored`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[credential-missing]`
  - `tests/test_sync_pair_order.py::test_a_continue_of_an_order_that_moved_nothing_hands_the_adapter_the_checks_listing[parked]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`

Old text:

```
                or (continued and not one.finishing_order)
```

New text:

```
                or (continued and one.finishing_order and False)
```

### `r1420.C3_continued_read_after_the_mark`

whether an earlier command began the order is read as always yes, so a first order is asked to agree with the check's listing

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C3_continued_read_after_the_mark`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_first_order_is_asked_with_nothing_to_agree_with_but_what_the_adapter_wrote`

Old text:

```
        continued = steps.has(STEP_ORDERING)
```

New text:

```
        continued = steps.has(STEP_ORDERING) or True
```

### `r1420.C4_carried_record_unread`

a continue whose run's steps cannot be read does not read the carried record, so its order of a pair that moved nothing is asked with no listing to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `C4_carried_record_unread`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[gone]`
  - `tests/test_sync_pair_order.py::test_a_continue_whose_steps_cannot_be_read_still_agrees_with_the_checks_listing_first[unreadable]`

Old text:

```
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is not None
```

New text:

```
        continued = steps.has(STEP_ORDERING) or steps.carried(STEP_ORDERING) is None and False
```

### `r1420.E2_finish_agreed_dropped`

sample: a finish of a stopped order is not held to the plan's reading at the adapter

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1420.json`, row `E2_finish_agreed_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
            else {}
```

New text:

```
            if False and one.finishing_order and one.account_before
            else {}
```

### `r1434.F7_ordering_start_from_the_readable_tracks`

R-1418's zero row, now the card's pin: the ordering step records its start from the readable tracks, so a track unread at the stop and read since is left out of the path read and its move by the person is put back

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1434.json`, row `F7_ordering_start_from_the_readable_tracks`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`

Old text:

```
                    one.account_before or one.account_now, removed, added
```

New text:

```
                    one.account_now, removed, added
```

### `u130-c.C1_half_written_snapshot`

Record the snapshot when either side was written, not both

- File: `src/cratekit/sync/pair_write.py`
- Source: `u130-c.json`, row `C1_half_written_snapshot`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_skipped_account_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_skipped_rekordbox_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_whole_sync_after_a_skipped_one_finishes_both_sides_from_the_old_base`
  - `tests/test_sync_pair.py::test_skipping_the_first_pairs_rekordbox_side_says_nothing_was_queued`
  - `tests/test_sync_pair.py::test_skipping_the_only_side_with_changes_answers_no_op`

Old text:

```
    whole = rekordbox_after is not None and account_after is not None and not one.withheld
```

New text:

```
    whole = (rekordbox_after is not None or account_after is not None) and not one.withheld
```

### `u198.C9_account_only`

apply_pair: a new pair is made when only rekordbox was approved

- File: `src/cratekit/sync/pair_write.py`
- Source: `u198.json`, row `C9_account_only`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_skipping_the_account_gate_makes_and_marks_nothing`

Old text:

```
        if not account:
            return done
```

New text:

```
        if False:
            return done
```

### `u202.C4_dates_recorded`

_record: the account's added dates are never recorded with the snapshot

- File: `src/cratekit/sync/pair_write.py`
- Source: `u202.json`, row `C4_dates_recorded`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_discover.py`
- Collected: 160 against a baseline of 160
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_rekordbox_removal_later_than_the_account_putting_it_back_takes_it_off_both`
  - `tests/test_sync_pair_back.py::test_a_removal_rekordbox_kept_no_moment_for_keeps_the_track_and_names_the_call`
  - `tests/test_sync_pair_back.py::test_a_removal_whose_row_time_predates_the_last_sync_is_no_moment`
  - `tests/test_sync_pair_back.py::test_a_row_held_as_two_releases_is_put_back_when_its_later_release_was`
  - `tests/test_sync_pair_back.py::test_a_track_put_back_on_the_account_after_rekordbox_took_it_out_stays_on_both`
  - `tests/test_sync_pair_back.py::test_the_snapshot_records_each_account_tracks_added_date`

Old text:

```
            if whole
            else None
        ),
        rekordbox=(
```

New text:

```
            if False
            else None
        ),
        rekordbox=(
```

### `u210.R1_made_step_read`

apply_pair: never read a made side recorded by an earlier command, so a continue makes it again

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R1_made_step_read`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[3-the move and the fill]`

Old text:

```
        if isinstance(made, str) and made:
```

New text:

```
        if False:
```

### `u210.R2_resumed_move`

_made: move only a playlist this call made, so a stop between the make and the move leaves it at the root

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R2_resumed_move`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_stop_between_making_a_playlist_and_filling_it_fills_it_and_makes_no_second[2-the make and the move]`

Old text:

```
    if made or (resumed and _made_here(store.get(account_id), one)):
```

New text:

```
    if made:
```

### `u210.R3_made_here_folder`

_made_here: read a reservation in any folder as made here

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R3_made_here_folder`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_made_here_reads_only_a_pair_made_for_this_playlist_in_this_folder`

Old text:

```
        and held.folder == place.folder
```

New text:

```
        and True
```

### `u210.R4_rekordbox_landed`

apply_pair: write rekordbox again on a continue whose commit already landed

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R4_rekordbox_landed`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_first_sync_named_by_hand_that_failed_after_its_mark_is_continued_on_its_plan`
  - `tests/test_sync_pair_resume_one.py::test_a_stop_inside_the_account_write_is_finished_without_writing_rekordbox_twice`

Old text:

```
        if isinstance(landed, dict):
```

New text:

```
        if False:
```

### `u210.R5_queue_once`

_queue_once: queue again a job an earlier command of the run queued

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R5_queue_once`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_job_queued_before_a_stop_is_not_queued_again_by_the_continue`

Old text:

```
    if steps.has(STEP_QUEUED):
```

New text:

```
    if False:
```

### `u210.R8_done_step`

apply_pair: record no done step, so a continue redoes a finished pair

- File: `src/cratekit/sync/pair_write.py`
- Source: `u210.json`, row `R8_done_step`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`
- Collected: 265 against a baseline of 265
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_resume.py::test_a_ceiling_stop_after_three_of_five_pairs_is_finished_by_a_continue_of_the_run`
  - `tests/test_sync_pair_resume.py::test_a_pair_the_stopped_command_finished_is_not_read_again_by_the_continue`
  - `tests/test_sync_pair_resume.py::test_the_stop_names_the_run_and_the_calls_its_continue_needs`

Old text:

```
    steps.mark(STEP_DONE, done.account_id or one.target.key)
```

New text:

```
    pass
```

### `u216.M20_made_drops_held`

_made: the plan's listing is not passed to the folder's reservation

- File: `src/cratekit/sync/pair_write.py`
- Source: `u216.json`, row `M20_made_drops_held`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 385 against a baseline of 385
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
        stale=place.stale,
        held=place.held,
    )
```

New text:

```
        stale=place.stale,
    )
```

### `u225.M21_start_from_asked`

_write_account: the start is built from the asked removals and additions, not the adapter's answer

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M21_start_from_asked`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_an_addition_the_provider_left_out_is_never_read_as_taken_off`

Old text:

```
                    one.account_before or one.account_now, removed, added
```

New text:

```
                    one.account_before or one.account_now, one.account_removes, one.account_adds
```

### `u225.M22_written_always`

_write_account: the step says rekordbox was committed though its gate was skipped

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M22_written_always`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made`

Old text:

```
                written=rekordbox_after is not None,
```

New text:

```
                written=True,
```

### `u225.M23_links_dropped`

_write_account: the step records none of the write's links

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M23_links_dropped`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
                written=rekordbox_after is not None,
                links=one.links,
```

New text:

```
                written=rekordbox_after is not None,
                links={},
```

### `u231.M10_moved_unrecorded`

write: every move accepted is not recorded, so a later lag on the path is finished from

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M10_moved_unrecorded`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`

Old text:

```
        steps.mark(STEP_MOVED, timestamp())
```

New text:

```
        pass
```

### `u231.M11_snapshot_from_the_order_sent`

write: the order as sent is recorded as the snapshot, with no settle reading

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M11_snapshot_from_the_order_sent`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_settle_reading_refused_for_another_reason_stops_the_write`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_at_once_finishes_in_the_one_run`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        done.settle = Settle(
            one=one, steps=steps, end=sent, moved_at=pair_model._now(), rekordbox_after=None
        )
        return None
```

New text:

```
        return sent
```

### `u231.M12_settle_takes_any_reading`

settle: any reading finishes the pair, the order the moves leave or not

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M12_settle_takes_any_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_pair_that_never_settles_stays_pending_past_the_age_a_plan_is_kept`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_agreed_once_off_the_path_keeps_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_is_held_whole_until_a_later_reading_agrees`
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_pending_run_does_not_count_its_pending_pair_as_synced`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`
  - `tests/test_sync_pair_settle.py::test_an_agreeing_reading_too_soon_after_the_last_is_not_agreement`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`

Old text:

```
        if reading is not None and tuple(reading) == tuple(settle.end):
```

New text:

```
        if reading is not None:
```

### `u231.M13_settle_sleeps_the_whole_window`

settle: the whole window is waited, the time spent on other pairs' writes not counted

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M13_settle_sleeps_the_whole_window`
- Moved: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`

Old text:

```
        left = SETTLE_SECONDS - (pair_model._now() - settle.moved_at).total_seconds()
```

New text:

```
        left = SETTLE_SECONDS
```

### `u231.M14_settle_reading_not_kept`

settle: a reading short of the order is not kept on the pair for the next plan to agree with

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M14_settle_reading_not_kept`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_an_order_the_provider_serves_late_is_left_pending_and_the_run_ends_ok`

Old text:

```
        if reading is not None:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
```

New text:

```
        if False:
            pairs.PairStore(cfg).see(settle.one.target.account_id, reading, at=timestamp())
```

### `u231.M23_carried_moving_unread`

continue: the carried record is not read when the run's steps cannot show the moves (round two's row 4)

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M23_carried_moving_unread`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`

Old text:

```
            moving = steps.carried(STEP_MOVING)
```

New text:

```
            moving = None
```

### `u231.M7_continue_resends`

write: a continue whose pair's moves began sends the order again rather than only reading it

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M7_continue_resends`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[gone]`
  - `tests/test_sync_pair_settle.py::test_a_continue_whose_steps_cannot_be_read_still_sends_no_move_again[unreadable]`
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_then_a_continue_sends_no_move_again`
  - `tests/test_sync_pair_settle.py::test_a_stop_part_way_whose_moves_all_landed_finishes_on_the_continue`

Old text:

```
        if isinstance(moving, Mapping):
```

New text:

```
        if False:
```

### `u231.M8_no_record_sends_blind`

write: a write that keeps no record sends its order's moves anyway (round one's BLOCKING row)

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M8_no_record_sends_blind`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 750 against a baseline of 750
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_write_that_keeps_no_record_sends_no_order`

Old text:

```
        if steps.steps is None:
            # U231, ROUND ONE'S REVIEW.
```

New text:

```
        if False:
            # U231, ROUND ONE'S REVIEW.
```

### `u234.S1_sample_finish_held_to_the_plans_reading`

sample, R-1411: the finish is not held to the plan's reading, so the rest of an off path order is moved from whatever the adapter reads

- File: `src/cratekit/sync/pair_write.py`
- Source: `u234.json`, row `S1_sample_finish_held_to_the_plans_reading`
- Moved: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 762 against a baseline of 762
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_pending_stop_agreed_off_its_path_is_finished_from_rekordbox`
  - `tests/test_sync_pair_stopped_order.py::test_an_account_the_stop_left_off_its_path_is_never_written_into_rekordbox`

Old text:

```
            if one.finishing_order and one.account_before
```

New text:

```
            if False and one.finishing_order and one.account_before
```

### `u304.S5_settle_window_clock`

pair_write._settle: the settle window counted off the wall clock, not pair_model._now

- File: `src/cratekit/sync/pair_write.py`
- Source: `u304.json`, row `S5_settle_window_clock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_account.py`
- Collected: 107 against a baseline of 107
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continues_settle_window_is_counted_from_when_the_moves_began`

Old text:

```
        left = SETTLE_SECONDS - (pair_model._now() - settle.moved_at).total_seconds()
```

New text:

```
        left = SETTLE_SECONDS - (datetime.now(settle.moved_at.tzinfo) - settle.moved_at).total_seconds()
```

### `u304.S6_settle_moment_clock`

pair_write._write_account: when the moves were sent is stamped off the wall clock, not pair_model._now

- File: `src/cratekit/sync/pair_write.py`
- Source: `u304.json`, row `S6_settle_moment_clock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_account.py`
- Collected: 107 against a baseline of 107
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_the_settle_window_counts_the_time_spent_on_other_writes`

Old text:

```
            one=one, steps=steps, end=sent, moved_at=pair_model._now(), rekordbox_after=None
```

New text:

```
            one=one, steps=steps, end=sent, moved_at=datetime.now(__import__("datetime").UTC), rekordbox_after=None
```

### `r263.S2_favorites_reason`

Favorites declares no reason, so its absent record reads as never again

- File: `src/cratekit/sync/sources.py`
- Source: `r263.json`, row `S2_favorites_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        no_cursor="no favorites worker records a cursor, so a completed sync "
```

New text:

```
        no_cursor="" and "no favorites worker records a cursor, so a completed sync "
```

### `u109-b.B1_labels_not_guided`

Drop guided_by from the labels spec, so labels is an ordinary source with no worker

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B1_labels_not_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        guided_by="label.sync",
```

New text:

```
(empty)
```

### `u109-b.B2_command_spelling`

Spell the guided command with the registry's dotted name, crate label.sync

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B2_command_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_label_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        return "crate " + self.guided_by.replace(".", " ")
```

New text:

```
        return "crate " + self.guided_by
```

### `u109-b.B3_no_cursor_reworded`

Reword the labels no_cursor sentence so it no longer names the guided verb

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B3_no_cursor_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`

Old text:

```
        no_cursor="label releases are taken by crate label sync, which keeps "
```

New text:

```
        no_cursor="label releases are taken by the guided verb, which keeps "
```

### `u74.A1_no_inbound_key`

The favourites spec declares no read half, so sync all never lists the hearts

- File: `src/cratekit/sync/sources.py`
- Source: `u74.json`, row `A1_no_inbound_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 26 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - ... and 11 more, see the JSON sidecar

Old text:

```
        inbound_key="intake.playlist",
```

New text:

```
        inbound_key=None,
```

### `u74.A2_wrong_inbound_key`

The read half is queued under intake.set, a key whose worker reads a tracklist, not a listing

- File: `src/cratekit/sync/sources.py`
- Source: `u74.json`, row `A2_wrong_inbound_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_only_favourites_declares_a_read_half_and_its_key_is_a_bound_intake_key`

Old text:

```
        inbound_key="intake.playlist",
```

New text:

```
        inbound_key="intake.set",
```

