# Mutation table: u303-replay-before-d

Measured by `scripts/mutate.py` on 2026-11-22 18:45 UTC, branch `HEAD` at `fd8173d3`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 198.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 30, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `/tmp/claude-0/-home-user-cratekit/ce20fa78-0ba8-5393-bea1-e47f9b749a43/scratchpad/known-replay.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r745-b.C1_pending_name_accepted` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 3 | killed |
| `r745-b.C3_create_not_exclusive` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 2 | killed |
| `r745-b.C4_torn_file_left` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r745-b.C5_made_folders_left` | `src/cratekit/cli/export_collection.py` | maintainer | 1 file(s) | 97 | 1 | killed |
| `r745-b.C6_folder_not_asked_before_the_copy` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r745-b.C8_live_database_opened` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 4 | killed |
| `r745-c.C2_existing_file_not_checked_first` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r745-c.C7_a_file_taken_for_a_folder` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r773-b.C10_summary_remapped_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r773-b.C1_no_rule_handed_to_the_emitter` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 3 | killed |
| `r773-b.C2_root_not_the_library_root` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 5 | killed |
| `r773-b.C3_warning_not_given` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 5 | killed |
| `r773-b.C4_warning_counts_prefixes_as_rows` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 5 | killed |
| `r773-b.C5_prefix_cap_two` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 3 | killed |
| `r773-b.C6_rest_of_the_prefixes_not_counted` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 2 | killed |
| `r773-b.C7_check_always_ok` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r773-b.C8_summary_unmapped_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 3 | killed |
| `r773-b.C9_summary_left_zero` | `src/cratekit/cli/export_collection.py` | user | 1 file(s) | 97 | 1 | killed |
| `r349-a.A3_job_show_field` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 99 | 4 | killed |
| `r925.J2_playlist_excluded` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 108 | 3 | killed |
| `r925.J3_field_not_set` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 108 | 4 | killed |
| `r925.J4_isrc_dropped` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 108 | 2 | killed |
| `r925.J5_version_dropped` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 108 | 1 | killed |
| `u182.M10_dry_run_writes` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M12_empty_set_copies` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M13_identity_parse` | `src/cratekit/cli/jobs.py` | user | 2 file(s) | 153 | 3 | killed |
| `u182.M13b_sweep_verbatim` | `src/cratekit/cli/jobs.py` | maintainer | 1 file(s) | 82 | 1 | killed |
| `u182.M14c_frees_set_composite` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M15_name_fallback` | `src/cratekit/cli/jobs.py` | user | 2 file(s) | 137 | 2 | killed |
| `u182.M16_naive_instant` | `src/cratekit/cli/jobs.py` | maintainer | 1 file(s) | 82 | 1 | killed |
| `u182.M17_summary_playlist` | `src/cratekit/cli/jobs.py` | user | 3 file(s) | 245 | 3 | killed |
| `u182.M1_days_floor` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M2c_running_composite` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 4 | killed |
| `u182.M3_blocked_offered` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M4_unknown_age_stale` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M5_cutoff` | `src/cratekit/cli/jobs.py` | user | 2 file(s) | 153 | 3 | killed |
| `u182.M6_listing_lock_check` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 1 | killed |
| `u182.M7_frees_identity` | `src/cratekit/cli/jobs.py` | user | 2 file(s) | 153 | 1 | killed |
| `u182.M8_keeper_kept` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 2 | killed |
| `u182.M9_keeper_newest` | `src/cratekit/cli/jobs.py` | user | 1 file(s) | 82 | 2 | killed |
| `r1499.L01_go_arrival_after_tail` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 324 | 1 | killed |
| `u190.L10_rest_of_tail_after_a_step_gate` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L11_done_keeps_the_go_outcome` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L1_no_tail_returns_untouched` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 146 | killed |
| `u190.L2_land_of_needs_a_mapping` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 56 | killed |
| `u190.L3_landing_carries_manifest` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 19 | killed |
| `u190.L4_landing_carries_pass` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 19 | killed |
| `u190.L5_land_stop_rekordbox_visit` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L6_way_on_from_the_stopped_step` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L7_pending_id_names_the_go` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u190.L9_verify_verb_by_step` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 1201 | 1 | killed |
| `u239.L01_remember_land_only` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 1 | killed |
| `u239.L02_remember_owner` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 2 | killed |
| `u239.L03_remember_called` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 6 | killed |
| `u239.L05_commands_added` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 3 | killed |
| `u239.L06_unrecorded_warning` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 275 | 1 | killed |
| `u293.S4_label_go_holds` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 253 | 2 | killed |
| `u295.S10_stuck_accepted` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 4 | killed |
| `u295.S11_no_read_back` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S12_cleanup_ignores_launchd` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S13_cleanup_keeps_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 3 | killed |
| `u295.S14_dirs_not_resolved` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 11 | killed |
| `u295.S15_override_relative` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S16_any_bin_prefix` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S17_plist_mode` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S18_crate_exec_bit` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S19_keys_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S1_platform_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 6 | killed |
| `u295.S20_gone_crate_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S21_run_at_load_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S22_env_names_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S23_show_always_clean` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 26 | killed |
| `u295.S24_loaded_without_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u295.S25_install_lockless` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S2_root_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 3 | killed |
| `u295.S3_argv_widened` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 7 | killed |
| `u295.S4_run_at_load` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 7 | killed |
| `u295.S5_read_words_after_night` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S6_daemons_directory` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S7_user_domain` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 63 | killed |
| `u295.S8_unknown_read_absent` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 2 | killed |
| `u295.S9_skip_bootout_on_unknown` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1093 | 1 | killed |
| `u179-z.S4_to_fetch_counts_held` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179-z.S9_refusals_need_permanence` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.D1_fetched_once` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.D2_refused_once` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S10_open_fetch_stops` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 2 | killed |
| `u179.S13_nothing_staged_ends` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 4 | killed |
| `u179.S14_relist_after_name` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S15_unread_apart` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S16_no_genre_named` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S17_label_flag_needs_a_label` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S1_fetch_only_when_planned` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 3 | killed |
| `u179.S2_owned_recorded` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 4 | killed |
| `u179.S3_held_recorded` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 3 | killed |
| `u179.S5_open_fetch_elsewhere` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S6_open_fetches_all` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S7_open_fetch_order` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 1 | killed |
| `u179.S8_refusals_settle` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 2 | killed |
| `u179.T1_rehearsal_runs` | `src/cratekit/cli/sync_bandcamp.py` | user | 2 file(s) | 34 | 5 | killed |
| `u172-b.C3_left_miscounted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 1 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u172.C2_guess_without_pass` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 2 | killed |
| `u179.T2_rehearsal_ack_attends` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T3_rehearsal_stop_wording` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T4_commands_quoted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 215 | 3 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 4 | killed |
| `u181.T2_rescore_ignores_profile` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 30 | killed |
| `u181.T3_rescore_keeps_stale` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u181.T4_rescore_failure_ignored` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 34 | 1 | killed |
| `u181.T5_rescore_never_run` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 4 | killed |
| `u181.T6_plan_warnings_not_lifted` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 1 | killed |
| `u190.T1_run_folder_absolute` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 1 | killed |
| `u190.T3_stale_matches_folder` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 1 | killed |
| `u190.T4_name_answers_inline` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 2 | killed |
| `u190.T6_chain_namespace` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 275 | 3 | killed |
| `u212.T1_reason_guard` | `src/cratekit/cli/tail.py` | maintainer | 11 file(s) | 1607 | 1 | killed |
| `u212.T2_done_only` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 1 | killed |
| `u212.T3_library` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 1 | killed |
| `u212.T4_earliest_first` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 1 | killed |
| `u212.T5_name_wraps` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1607 | 2 | killed |
| `u284.T1_pass_names_nothing` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u284.T2_pass_stop_unsaid` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u319.M10_sync_stop_drops_the_short_path` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 183 | 1 | killed |
| `u168.C3_default_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 3 | killed |
| `u168.C4_default_actor_session` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C5_given_actor_ignored` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C6_no_argv_continues` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C7_continue_without_run` | `src/cratekit/cli/verbs/runs.py` | user | 2 file(s) | 1005 | 2 | killed |
| `u170.R10_moved_guard` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R11_digest_ids_only` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R12_default_week` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R1_zero_days` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R2_ceiling` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R3_own_run` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R4_unreadable_dropped` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R5_answers_apply` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 2 | killed |
| `u170.R6_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 2 | killed |
| `u170.R7_declined_applies` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u170.R8_empty_asks` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 2 | killed |
| `u170.R9_kept_planned` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1704 | 1 | killed |
| `u186.R1_decide_abort` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R2_decide_no_digest` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R3_decide_any_gate` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R4_decide_any_option` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R5_decide_any_digest` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R6_decide_unwired` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 3 | killed |
| `u186.R7_continue_dedupe` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u186.R8_continue_drops_repeat` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 34 | 1 | killed |
| `u294.M05_suggest_step_band` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M06_served_is_every_row` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 9 | killed |
| `u294.M07_followers_another_spelling` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M08_alias_files_stale_check` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M09_digest_drops_words` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M10_digest_drops_answers` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M11_unknown_word_accepted` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 4 | killed |
| `u294.M12_settled_answer_taken` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M13_unanswerable_accepted` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M14_answered_twice` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 2 | killed |
| `u294.M15_text_not_threaded` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M16_settled_unreached` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 3 | killed |
| `u294.M18_no_reload_after_words` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M19_ack_skipped` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 2 file(s) | 1053 | 1 | killed |
| `u294.M20_abort_applies` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M24_notes_dropped` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 2 | killed |
| `u294.M25_folder_stale_check` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |

## Row definitions

### `r745-b.C1_pending_name_accepted`

_refuse_destination: accept a name the pending scan reads as an intake file

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C1_pending_name_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_favorites.xml]`
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_inboxed.xml]`
  - `tests/test_export_collection.py::test_a_name_the_pending_scan_reads_as_an_intake_file_is_refused[_synced.xml]`

Old text:

```
        if name.endswith(suffix):
```

New text:

```
        if False:
```

### `r745-b.C3_create_not_exclusive`

_write_new: open for writing, replacing what is there. The composite for C2

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C3_create_not_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_file_that_appears_after_the_check_is_refused_by_the_write`
  - `tests/test_export_collection.py::test_a_file_that_came_and_went_is_still_refused_as_taken`

Old text:

```
open(destination, "xb")
```

New text:

```
open(destination, "wb")
```

### `r745-b.C4_torn_file_left`

_write_new: leave the file a failed write created

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C4_torn_file_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made`

Old text:

```
                destination.unlink()
```

New text:

```
                pass
```

### `r745-b.C5_made_folders_left`

_write_new: leave the folders a failed write made

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C5_made_folders_left`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_write_that_fails_part_way_leaves_no_file_and_no_folder_it_made`

Old text:

```
                path.rmdir()
```

New text:

```
                pass
```

### `r745-b.C6_folder_not_asked_before_the_copy`

_refuse_destination: do not ask the folder before the database is copied

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C6_folder_not_asked_before_the_copy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied`

Old text:

```
    _refuse_unwritable_folder(destination)
```

New text:

```
    pass
```

### `r745-b.C8_live_database_opened`

_read: open the configured database itself, with no copy and no check that rekordbox is closed

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-b.json`, row `C8_live_database_opened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_refused_read_leaves_no_folder_behind`
  - `tests/test_export_collection.py::test_rekordbox_running_is_refused_and_nothing_is_written`
  - `tests/test_export_collection.py::test_the_agent_running_is_refused_under_the_same_slug`
  - `tests/test_export_collection.py::test_the_configured_database_is_never_opened_and_is_left_byte_for_byte`

Old text:

```
    with rb_writer.read_only_copy(database, cfg=cfg) as db:
```

New text:

```
    with __import__("contextlib").closing(
        rb_writer.open_db(database, require_closed=False, check_app_version=False, cfg=cfg)
    ) as db:
```

### `r745-c.C2_existing_file_not_checked_first`

_refuse_destination: drop the check ahead of the copy. Measured again after the test its zero bought

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-c.json`, row `C2_existing_file_not_checked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_an_existing_file_is_refused_before_the_database_is_copied`

Old text:

```
    if os.path.lexists(destination):
        raise _taken(destination)
```

New text:

```
    if False:
        raise _taken(destination)
```

### `r745-c.C7_a_file_taken_for_a_folder`

_refuse_unwritable_folder: do not ask whether the nearest ancestor is a folder. Measured again after the assertion its zero bought

- File: `src/cratekit/cli/export_collection.py`
- Source: `r745-c.json`, row `C7_a_file_taken_for_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_folder_that_is_a_file_is_refused_before_the_database_is_copied`

Old text:

```
    if not nearest.is_dir():
```

New text:

```
    if False:
```

### `r773-b.C10_summary_remapped_zero`

summary: report no location placed by a rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C10_summary_remapped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`

Old text:

```
                "locations_remapped": document.remapped,
```

New text:

```
                "locations_remapped": 0,
```

### `r773-b.C1_no_rule_handed_to_the_emitter`

_read: hand the emitter an empty prefix map, which is the export sitting 19 measured

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C1_no_rule_handed_to_the_emitter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
        prefix_map=[
            locations.PrefixRule(source, target) for source, target in cfg.resolved_prefix_map()
        ],
```

New text:

```
        prefix_map=[],
```

### `r773-b.C2_root_not_the_library_root`

_read: hand the emitter the filesystem root as the library root

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C2_root_not_the_library_root`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_a_landing_splices_into_the_file_and_the_import_is_proved_against_a_second[recorded-under-a-base-drive]`
  - `tests/test_export_collection.py::test_a_library_recorded_where_it_is_mounted_has_nothing_to_place`
  - `tests/test_export_collection.py::test_every_location_is_written_under_the_mounted_root_when_a_rule_places_it`
  - `tests/test_export_collection.py::test_the_envelope_counts_what_the_file_holds_and_names_what_it_left_out`
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`

Old text:

```
        root=cfg.library.root,
```

New text:

```
        root="/",
```

### `r773-b.C3_warning_not_given`

_warnings: give no warning over rows under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C3_warning_not_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes0-rule (3 under /a/b), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
    if omitted.unmapped_paths:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
```

New text:

```
    if False:
        shown = omitted.unmapped_prefixes[:_NAMED_PREFIXES]
```

### `r773-b.C4_warning_counts_prefixes_as_rows`

_warnings: open the warning with the number of prefixes where the number of rows goes

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C4_warning_counts_prefixes_as_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes0-rule (3 under /a/b), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
                    f"{len(omitted.unmapped_paths)} track(s) record a path under "
```

New text:

```
                    f"{len(omitted.unmapped_prefixes)} track(s) record a path under "
```

### `r773-b.C5_prefix_cap_two`

_NAMED_PREFIXES: name two prefixes where three are named

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C5_prefix_cap_two`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes1-rule (3 under /a/b, 2 under /c/d, 1 under /e/f), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`

Old text:

```
_NAMED_PREFIXES = 3
```

New text:

```
_NAMED_PREFIXES = 2
```

### `r773-b.C6_rest_of_the_prefixes_not_counted`

_warnings: never say how many prefixes were not named

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C6_rest_of_the_prefixes_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes2-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 1 other prefix), and]`
  - `tests/test_export_collection.py::test_the_warning_names_three_prefixes_and_counts_the_rest[prefixes3-rule (3 under /a/b, 2 under /c/d, 1 under /e/f, and 2 other prefixes), and]`

Old text:

```
        if more > 0:
            listed +=
```

New text:

```
        if False:
            listed +=
```

### `r773-b.C7_check_always_ok`

export.locations: report ok whatever is under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C7_check_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
            status="ok" if not omitted.unmapped_paths else "info",
        ),
        _check(
            "export.tempo",
```

New text:

```
            status="ok",
        ),
        _check(
            "export.tempo",
```

### `r773-b.C8_summary_unmapped_zero`

summary: report no track under no rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C8_summary_unmapped_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_export_and_doctor_count_the_same_rows_as_under_no_rule`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_export_collection.py::test_with_no_rule_each_location_is_written_as_the_database_holds_it_and_counted`

Old text:

```
                "tracks_under_no_rule": len(omitted.unmapped_paths),
```

New text:

```
                "tracks_under_no_rule": 0,
```

### `r773-b.C9_summary_left_zero`

summary: report no location left to a rule

- File: `src/cratekit/cli/export_collection.py`
- Source: `r773-b.json`, row `C9_summary_left_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 97 against a baseline of 97
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_envelope_counts_a_row_left_to_its_rule`

Old text:

```
                "locations_left_to_a_rule": len(omitted.left_to_rule),
```

New text:

```
                "locations_left_to_a_rule": 0,
```

### `r349-a.A3_job_show_field`

job show stops attaching the outcomes field

- File: `src/cratekit/cli/jobs.py`
- Source: `r349-a.json`, row `A3_job_show_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_queued_backup_names_every_command_it_ran_in_job_show`
  - `tests/test_backup_cli.py::test_a_rehearsal_s_outcome_is_recorded_and_says_it_was_one`

Old text:

```
        summary[backup_facts.OUTCOMES_FIELD] = outcomes
```

New text:

```
        pass
```

### `r925.J2_playlist_excluded`

job show lists tracks for a set job only, not a playlist job

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J2_playlist_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_job_show_lists_a_playlist_jobs_tracks_too`
  - `tests/intake/test_workers.py::test_the_job_verbs_spell_the_intake_keys_the_intake_module_spells`

Old text:

```
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set", "intake.playlist"})
```

New text:

```
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set"})
```

### `r925.J3_field_not_set`

job show computes the tracks and never puts them on the envelope

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J3_field_not_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_job_show_lists_a_playlist_jobs_tracks_too`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`
  - `tests/intake/test_workers.py::test_job_show_on_a_job_of_another_handler_lists_no_tracks`

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

### `r925.J4_isrc_dropped`

job show lists every track without its ISRC

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J4_isrc_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_job_show_lists_a_playlist_jobs_tracks_too`
  - `tests/intake/test_workers.py::test_job_show_lists_every_track_an_intake_set_froze_in_set_order`

Old text:

```
                "isrc": str(said["isrc"]) if said.get("isrc") else None,
```

New text:

```
                "isrc": None,
```

### `r925.J5_version_dropped`

job show lists every track without its version

- File: `src/cratekit/cli/jobs.py`
- Source: `r925.json`, row `J5_version_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
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

### `u182.M10_dry_run_writes`

_cancel_stale: cancel in a dry run too

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M10_dry_run_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`

Old text:

```
            if not dry_run:
                outcome = _cancel_queued(store, hold.job.job_id)
```

New text:

```
            if True:
                outcome = _cancel_queued(store, hold.job.job_id)
```

### `u182.M12_empty_set_copies`

intake_holds: count two jobs with no item as copies of each other

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M12_empty_set_copies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_two_jobs_with_no_item_are_nobodys_copies`

Old text:

```
                    if mine and other.job_id != job.job_id and sets[other.job_id] == mine
```

New text:

```
                    if other.job_id != job.job_id and sets[other.job_id] == mine
```

### `u182.M13_identity_parse`

playlist_identity: key on the raw source instead of the pass's reading

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M13_identity_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_sync_land.py`
- Collected: 153 against a baseline of 153
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_url_typed_by_hand_holds_the_same_playlist_a_sweeps_id_does`
  - `tests/test_jobs.py::test_the_job_verbs_read_a_playlist_as_the_sweep_records_it`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        return catalogue.playlist_id(source)
```

New text:

```
        return source
```

### `u182.M13b_sweep_verbatim`

playlist_identity: parse a sweep's own id as if typed, so it no longer agrees with the cursor

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M13b_sweep_verbatim`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_the_job_verbs_read_a_playlist_as_the_sweep_records_it`

Old text:

```
    if (job.payload or {}).get(INTAKE_SWEEP_KEY) == INTAKE_SWEEP_ID:
```

New text:

```
    if False:
```

### `u182.M14c_frees_set_composite`

composite for M14: drop _frees's own set check, the layer that holds when the identity's set branch is gone

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M14c_frees_set_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_stale_set_job_says_it_frees_no_playlist_and_names_no_file_as_one`

Old text:

```
    if hold.job.handler_key != "intake.playlist":
        return "frees no account playlist: a set job holds none out of a pass"
```

New text:

```
    if False:
        return "frees no account playlist: a set job holds none out of a pass"
```

### `u182.M15_name_fallback`

intake_playlist: name a job queued by hand by nothing rather than by its source

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M15_name_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_render_payloads.py`
- Collected: 137 against a baseline of 137
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_reference_the_url_parser_cannot_read_is_kept_as_typed_not_a_crash`
  - `tests/test_jobs.py::test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for`

Old text:

```
    return source, source


def playlist_identity
```

New text:

```
    return "", source


def playlist_identity
```

### `u182.M16_naive_instant`

_instant: accept a stamp with no offset, read as if it were UTC

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M16_naive_instant`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`

Old text:

```
    return moment if moment.tzinfo is not None else None
```

New text:

```
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)
```

### `u182.M17_summary_playlist`

_summary: carry no playlist field, so job show and job list say nothing of it

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M17_summary_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_render_payloads.py`, `tests/intake/test_workers.py`
- Collected: 245 against a baseline of 245
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_hearts_job_names_no_playlist_and_frees_the_hearts`
  - `tests/test_jobs.py::test_a_stale_set_job_says_it_frees_no_playlist_and_names_no_file_as_one`
  - `tests/test_jobs.py::test_job_show_and_list_name_the_playlist_an_intake_job_was_made_for`

Old text:

```
    named = intake_playlist(job)
    if named is not None:
```

New text:

```
    named = None
    if named is not None:
```

### `u182.M1_days_floor`

_days: accept zero, so --stale-days 0 offers a job queued a second ago as stale

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M1_days_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_zero_or_negative_day_count_is_the_parsers_usage_error_and_cancels_nothing`

Old text:

```
    if value < 1:
        raise ValueError(f"{text!r} is not a number of days")
```

New text:

```
    if value < 0:
        raise ValueError(f"{text!r} is not a number of days")
```

### `u182.M2c_running_composite`

composite for M2: drop the running check, the queued check and the listing's lock check together, so a job a live driver runs is offered

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M2c_running_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 4 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
    state = hold.job.state
    if state is jobs.JobState.RUNNING:
        return "running; a stale cancel never touches a running job"
    if state is not jobs.JobState.QUEUED:
        return (
            f"{state}, not queued; if it is stale, cancel it by its id: "
            f"crate job cancel {hold.job.job_id}"
        )
    created = _instant(hold.job.created)
    if created is None:
        return f"its queued time {hold.job.created!r} cannot be read, so its age is unknown"
    if created >= cutoff:
        return f"queued {hold.age_days} day(s) ago, within the {days} day(s) asked"
    try:
        jobs.assert_free(hold.job.job_id)
    except jobs.DriverHeld:
        return "a live driver holds it; a stale cancel never touches a running job"
```

New text:

```
    created = _instant(hold.job.created)
    if created is None:
        return "unknown"
    if created >= cutoff:
        return "young"
```

### `u182.M3_blocked_offered`

_left_reason: offer a blocked job as stale, so a parked job is cancelled

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M3_blocked_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_blocked_job_or_another_librarys_is_left_by_the_stale_cancel`

Old text:

```
    if state is not jobs.JobState.QUEUED:
        return (
```

New text:

```
    if state not in (jobs.JobState.QUEUED, jobs.JobState.BLOCKED):
        return (
```

### `u182.M4_unknown_age_stale`

_left_reason: read an unreadable queued time as stale rather than of unknown age

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M4_unknown_age_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_job_whose_queued_time_cannot_be_read_is_never_stale`

Old text:

```
    if created is None:
        return f"its queued time {hold.job.created!r} cannot be read, so its age is unknown"
```

New text:

```
    if created is None:
        return None
```

### `u182.M5_cutoff`

_left_reason: never leave a younger job, so every queued job is stale whatever its age

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M5_cutoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_sync_land.py`
- Collected: 153 against a baseline of 153
- Kills: 3 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_cancel_whose_playlist_another_open_job_holds_says_it_frees_nothing_yet`
  - `tests/test_jobs.py::test_a_url_typed_by_hand_holds_the_same_playlist_a_sweeps_id_does`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
    if created >= cutoff:
```

New text:

```
    if False:
```

### `u182.M6_listing_lock_check`

_left_reason: drop the live driver check, so a dry run lists a held job for cancel

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M6_listing_lock_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_a_queued_job_a_live_driver_holds_as_left`

Old text:

```
        jobs.assert_free(hold.job.job_id)
    except jobs.DriverHeld:
```

New text:

```
        pass
    except jobs.DriverHeld:
```

### `u182.M7_frees_identity`

_frees: match the holder by the raw source again, so a typed URL and a sweep's id read as two playlists

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M7_frees_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`, `tests/test_sync_land.py`
- Collected: 153 against a baseline of 153
- Kills: 1 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_url_typed_by_hand_holds_the_same_playlist_a_sweeps_id_does`

Old text:

```
            and hold.identity
            and other.identity == hold.identity
```

New text:

```
            and hold.source
            and other.source == hold.source
```

### `u182.M8_keeper_kept`

_cancel_stale: never keep the newest copy, so every stale copy of a track set is cancelled

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M8_keeper_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
            if hold.same_tracks and keeper.job_id == hold.job.job_id:
```

New text:

```
            if False:
```

### `u182.M9_keeper_newest`

_cancel_stale: keep the oldest copy of a track set rather than the newest

- File: `src/cratekit/cli/jobs.py`
- Source: `u182.json`, row `M9_keeper_newest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_jobs.py`
- Collected: 82 against a baseline of 82
- Kills: 2 (killed)
- Killed:
  - `tests/test_jobs.py::test_a_dry_run_lists_three_stale_jobs_and_names_the_keeper_of_the_identical_two`
  - `tests/test_jobs.py::test_the_stale_cancel_cancels_the_stale_keeps_the_newest_copy_and_leaves_the_younger`

Old text:

```
                (by_id[other].job for other in (hold.job.job_id, *hold.same_tracks)),
                key=_newest,
```

New text:

```
                (by_id[other].job for other in (hold.job.job_id, *hold.same_tracks)),
                key=lambda held: tuple(-ord(c) for c in held.created),
```

### `r1499.L01_go_arrival_after_tail`

label sync: no check after the go's name apply, so an arrival is planned into the go's landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L01_go_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`

Old text:

```
        if changed is not None:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

New text:

```
        if False:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

### `u190.L10_rest_of_tail_after_a_step_gate`

_attended: name nothing after a tail step's own gate, so the rest of the tail is left unsaid

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L10_rest_of_tail_after_a_step_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
        after = tuple(f"then: {one}" for one in _commands(folder, landing, stop.step)[1:])
```

New text:

```
        after = ()
```

### `u190.L11_done_keeps_the_go_outcome`

label_sync: end a landing that planned nothing as NO_OP, hiding the download the go made

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L11_done_keeps_the_go_outcome`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
        outcome=envelope.outcome,
```

New text:

```
        outcome=Outcome.NO_OP,
```

### `u190.L1_no_tail_returns_untouched`

label_sync: run the chain over a go that names no tail

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L1_no_tail_returns_untouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 146 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[label.sync]`
  - `tests/test_label_sync.py::test_a_catalogue_that_confirms_nothing_is_not_a_label_with_nothing_new`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv3-go with --answer]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv5-goes with --answer pick]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv6---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_half_shaped_invocation_is_refused_and_records_nothing[argv7---next would ignore the releases]`
  - `tests/test_label_sync.py::test_a_label_with_nothing_new_is_not_asked_and_a_run_with_nothing_to_ask_says_so`
  - `tests/test_label_sync.py::test_a_label_with_three_new_releases_is_asked_once`
  - `tests/test_label_sync.py::test_a_labels_own_offer_bounds_a_first_question`
  - `tests/test_label_sync.py::test_a_later_answer_files_its_releases_under_the_run_that_asked`
  - `tests/test_label_sync.py::test_a_newly_followed_label_is_offered_at_most_its_offer_per_sweep_newest`
  - `tests/test_label_sync.py::test_a_pick_naming_a_release_the_question_did_not_offer_is_refused`
  - `tests/test_label_sync.py::test_a_question_counts_only_the_labels_own_releases_past_its_window`
  - `tests/test_label_sync.py::test_a_release_answered_not_now_is_not_filed_by_the_labels_sweep`
  - `tests/test_label_sync.py::test_a_release_the_genre_gate_holds_never_appears_in_a_question`
  - ... and 131 more, see the JSON sidecar

Old text:

```
    if land is None:
        return envelope
    cfg
```

New text:

```
    if land is None:
        land = {"folder": "/nowhere", "pass": "none"}
    cfg
```

### `u190.L2_land_of_needs_a_mapping`

_land_of: read the go's report without its key, so no tail is ever run

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L2_land_of_needs_a_mapping`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 56 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_failed_only_by_a_track_refused_for_good_runs_the_tail_on_the_rest`
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_download_queued_by_hand_is_not_resumed_or_held_by_a_go`
  - `tests/test_label_sync_go.py::test_a_download_that_ended_half_failed_is_retried_by_the_next_go_and_only_its_failures`
  - `tests/test_label_sync_go.py::test_a_download_that_finished_during_the_tail_is_not_kept_as_the_gos`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_fresh_go_with_nothing_new_names_an_unlanded_download_rather_than_end_quietly`
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - ... and 41 more, see the JSON sidecar

Old text:

```
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
```

New text:

```
    land = report.get("tail") if isinstance(report, Mapping) else None
```

### `u190.L3_landing_carries_manifest`

_landing_args: drop the manifest, so the landing files the label's rows under no label

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L3_landing_carries_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        *(["--manifest", str(manifest)] if isinstance(manifest, str) and manifest else []),
```

New text:

```
        *([] if isinstance(manifest, str) and manifest else []),
```

### `u190.L4_landing_carries_pass`

_landing_args: drop the pass, so the landing's intake file is named for nothing the go named

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L4_landing_carries_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 19 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_half_failed_by_a_track_a_retry_may_clear_is_retried_under_its_run`
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_go_resuming_an_earlier_download_lands_it_under_that_gos_manifest_and_pass`
  - `tests/test_label_sync_go.py::test_a_go_stopped_at_the_ceiling_finishes_and_lands_on_the_next_go_under_its_run`
  - `tests/test_label_sync_go.py::test_a_go_whose_job_was_finished_by_hand_lands_on_the_next_go_with_no_new_decision`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_landing_recorded_for_one_download_never_answers_for_the_runs_next_one`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_already_landed_refuses_nothing`
  - `tests/test_label_sync_go.py::test_a_release_whose_second_track_lands_lossy_runs_the_tail_on_the_first_and_names_it`
  - `tests/test_label_sync_go.py::test_a_resumed_download_failed_only_by_a_refusal_lands_under_the_first_gos_manifest`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        "--pass",
        str(land["pass"]),
    ]
```

New text:

```
    ]
```

### `u190.L5_land_stop_rekordbox_visit`

_attended: follow the landing's gate with the next tail command rather than the rekordbox visit

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L5_land_stop_rekordbox_visit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it`

Old text:

```
    if stop.step == tail.LAND:
        after: Sequence[str] = tail.REKORDBOX_STEPS
```

New text:

```
    if False:
        after: Sequence[str] = tail.REKORDBOX_STEPS
```

### `u190.L6_way_on_from_the_stopped_step`

_commands: name the whole tail from its first step, so a person reruns steps that succeeded

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L6_way_on_from_the_stopped_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
tail.STEPS[tail.STEPS.index(step):]
```

New text:

```
tail.STEPS[0:]
```

### `u190.L7_pending_id_names_the_go`

_attended: name the pending action for the landing's run rather than the go's

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L7_pending_id_names_the_go`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_landing_gates_run_is_named_in_the_envelope_with_the_commands_that_answer_it`

Old text:

```
        id=f"label-sync-{ctx.run.run_id}",
```

New text:

```
        id=f"label-sync-{chain.summary.get('gate_run')}",
```

### `u190.L9_verify_verb_by_step`

_attended: name the landing as the verb to verify whatever step stopped

- File: `src/cratekit/cli/label_sync.py`
- Source: `u190.json`, row `L9_verify_verb_by_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_cli_contract.py`
- Collected: 1201 against a baseline of 1201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_tail_step_stopped_at_a_gate_names_its_answer_and_the_rest_of_the_tail`

Old text:

```
        verify_verb=tail.LAND_VERB if stop.step == tail.LAND else ctx.entry.name,
```

New text:

```
        verify_verb=tail.LAND_VERB,
```

### `u239.L01_remember_land_only`

_remember: record a gate stop at any step as the landing, so a restamp gate is taken for it

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L01_remember_land_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`

Old text:

```
    if not (stop.step == tail.LAND and stop.cause.reason == tail.GATE_STOP and landed):
```

New text:

```
    if not (stop.cause.reason == tail.GATE_STOP and landed):
```

### `u239.L02_remember_owner`

_remember: record on whichever run ran the tail, the round one blocking shape

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L02_remember_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    if owner == ctx.run.run_id:
```

New text:

```
    if True:
```

### `u239.L03_remember_called`

label_sync: never record the landing, so a later go runs the tail again

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L03_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_fresh_go_that_landed_another_runs_download_records_it_on_that_run`
  - `tests/test_label_sync_go.py::test_a_go_that_ran_its_tail_once_names_its_landing_when_run_again`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_reached_its_landing_names_that_landing_and_runs_nothing_again`
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`
  - `tests/test_label_sync_go.py::test_a_stop_at_a_gate_before_the_landing_records_no_landing_and_the_next_go_runs_the_tail`
  - `tests/test_label_sync_go.py::test_a_walk_under_a_landed_run_that_records_an_answer_is_not_a_no_op`

Old text:

```
        warnings.extend(_remember(ctx, stop, land))
```

New text:

```
        pass
```

### `u239.L05_commands_added`

_with_commands: never name the tail commands on the go's refusal

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L05_commands_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_download_landed_while_the_fresh_go_downloaded_refuses_its_tail`
  - `tests/test_label_sync_go.py::test_a_later_gos_download_in_the_same_folder_refuses_the_tail_and_names_its_commands`
  - `tests/test_label_sync_go.py::test_a_plain_download_into_the_folder_refuses_the_runs_own_tail`

Old text:

```
    land = _land_in(cause.detail) if _GO_ORIGIN in cause.origin else None
```

New text:

```
    land = None
```

### `u239.L06_unrecorded_warning`

_remember: drop the warning when another run's record cannot keep the landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L06_unrecorded_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_landing_another_runs_record_cannot_keep_is_a_warning_and_the_go_still_ends_at_it`

Old text:

```
    except Exception as exc:  # noqa: BLE001 - see below
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001 - see below
```

### `u293.S4_label_go_holds`

label_sync: a label go takes no staging lock

- File: `src/cratekit/cli/label_sync.py`
- Source: `u293.json`, row `S4_label_go_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_label_go_holds_the_lock_and_a_walk_does_not`
  - `tests/test_sync_night.py::test_a_label_go_refuses_while_another_pass_holds_the_lock`

Old text:

```
    with staging_lock.held("crate label sync --go", run_id=ctx.run.run_id):
```

New text:

```
    if True:
```

### `u295.S10_stuck_accepted`

_boot_out: accept an agent still loaded after its bootout

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S10_stuck_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 4 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_bootout_launchd_ignores_is_said_in_words_a_person_reads`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[bootout fails]`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[stuck]`
  - `tests/test_schedule.py::test_an_agent_launchd_will_not_let_go_of_is_not_replaced`

Old text:

```
    after, check = loaded()
    if after != NOT_LOADED:
        if not out.ok:
```

New text:

```
    after, check = loaded()
    if after == UNKNOWN:
        if not out.ok:
```

### `u295.S11_no_read_back`

_install: trust bootstrap's exit and never read launchd back

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S11_no_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing`

Old text:

```
    state, check = loaded() if answer.ok else (UNKNOWN, answer)
```

New text:

```
    state, check = (LOADED, answer) if answer.ok else (UNKNOWN, answer)
```

### `u295.S12_cleanup_ignores_launchd`

_install: delete the plist on a failed load whatever launchd still holds

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S12_cleanup_ignores_launchd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_failed_load_launchd_may_still_hold_keeps_its_plist`

Old text:

```
        failed = answer if not answer.ok else check
        if after != NOT_LOADED:
```

New text:

```
        failed = answer if not answer.ok else check
        if False:
```

### `u295.S13_cleanup_keeps_plist`

_install: keep the plist written for a failed load, leaving an agent half installed

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S13_cleanup_keeps_plist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 3 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_bootstrap_that_fails_is_refused_in_its_words_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_failed_replace_says_the_earlier_schedule_is_gone_too`

Old text:

```
        _remove_plist(target)
        earlier = 
```

New text:

```
        pass
        earlier = 
```

### `u295.S14_dirs_not_resolved`

environment: carry no resolved directory, so an XDG install's night reads another installation

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S14_dirs_not_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 11 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_relative_override_is_carried_absolute`
  - `tests/test_schedule.py::test_an_installation_found_through_xdg_alone_is_the_one_the_agent_reads`
  - `tests/test_schedule.py::test_install_and_show_agree_on_the_environment_shape`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[no config]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[no state]`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`
  - `tests/test_schedule.py::test_show_reads_an_installed_agent_launchd_does_not_hold`
  - `tests/test_schedule.py::test_show_reads_an_installed_loaded_agent`
  - `tests/test_schedule.py::test_show_reads_the_night_line_from_the_state_the_agent_carries`
  - `tests/test_schedule.py::test_show_writes_nothing_and_asks_launchd_only_to_print`
  - `tests/test_schedule.py::test_the_agent_carries_a_fixed_path_the_resolved_directories_and_nothing_else`

Old text:

```
        carried[name] = str(_absolute(directory))
```

New text:

```
        pass
```

### `u295.S15_override_relative`

environment: carry an override as set, so a relative one names another place for launchd

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S15_override_relative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_relative_override_is_carried_absolute`

Old text:

```
            carried[name] = str(_absolute(value))
```

New text:

```
            carried[name] = value
```

### `u295.S16_any_bin_prefix`

environment: carry every CRATEKIT_BIN_ name set, not only the binaries this build runs

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S16_any_bin_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_the_agent_carries_a_fixed_path_the_resolved_directories_and_nothing_else`

Old text:

```
    for name in (*override_names(), *binary_names()):
```

New text:

```
    for name in (*override_names(), *(n for n in source if n.startswith(binaries.ENV_PREFIX))):
```

### `u295.S17_plist_mode`

PLIST_MODE: the plist readable by everyone on the Mac

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S17_plist_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it`

Old text:

```
PLIST_MODE = 0o600
```

New text:

```
PLIST_MODE = 0o644
```

### `u295.S18_crate_exec_bit`

crate_runs: never ask whether the crate is executable

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S18_crate_exec_bit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_crate_that_cannot_run_is_refused_and_nothing_is_written[not executable]`

Old text:

```
    return found.is_absolute() and found.is_file() and os.access(found, os.X_OK)
```

New text:

```
    return found.is_absolute() and found.is_file()
```

### `u295.S19_keys_unchecked`

read_agent: never compare the plist's keys, so a Program key passes

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S19_keys_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a program key]`

Old text:

```
    if keys != PLIST_KEYS:

```

New text:

```
    if False:

```

### `u295.S1_platform_guard`

_macos_only: never refuse another platform, so a schedule is attempted where there is no launchd

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S1_platform_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 6 (killed)
- Killed:
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[linux-install]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[linux-remove]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[linux-show]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[win32-install]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[win32-remove]`
  - `tests/test_schedule.py::test_any_platform_but_macos_refuses_naming_it[win32-show]`

Old text:

```
    if running != MACOS:

```

New text:

```
    if False:

```

### `u295.S20_gone_crate_unchecked`

read_agent: never ask whether the crate it runs can run

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S20_gone_crate_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_whose_crate_is_gone`

Old text:

```
    if crate is not None and not crate_runs(crate):

```

New text:

```
    if False:

```

### `u295.S21_run_at_load_unchecked`

read_agent: accept an agent that runs at load

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S21_run_at_load_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[run at load]`

Old text:

```
    if document.get("RunAtLoad") is not False:

```

New text:

```
    if False:

```

### `u295.S22_env_names_unchecked`

read_agent: accept an environment name this build never carries

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S22_env_names_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a raised limit]`
  - `tests/test_schedule.py::test_show_never_prints_a_value_this_build_would_not_carry`

Old text:

```
    unknown = sorted(set(env) - allowed_names())
```

New text:

```
    unknown = []
```

### `u295.S23_show_always_clean`

show: exit clean whatever problems were read

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S23_show_always_clean`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 26 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a program key]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[a raised limit]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[another program]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[every hour]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[hour 99]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[no calendar]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[one weekday]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[run at load]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[split log]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_edited_to_be_anything_but_the_nights[two times]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_launchd_holds_with_no_plist`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[a true hour]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an answer]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an empty word]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[log outside its state]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
    if not problems:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
```

New text:

```
    if True:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP)
```

### `u295.S24_loaded_without_plist`

show: a loaded agent with no plist reads as a clean report

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S24_loaded_without_plist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_launchd_holds_with_no_plist`

Old text:

```
        if found is None and unreadable is None:

```

New text:

```
        if False:

```

### `u295.S25_install_lockless`

install: boot the agent out without the staging lock, so a night in progress is ended

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S25_install_lockless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_night_in_progress_is_never_booted_out[install]`
  - `tests/test_schedule.py::test_only_the_one_seam_starts_a_process`

Old text:

```
    with staging_lock.held("crate schedule install", run_id=ctx.run.run_id):
```

New text:

```
    with open(os.devnull):
```

### `u295.S2_root_guard`

_as_the_person: never refuse root, so the agent is bootstrapped into gui/0

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S2_root_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 3 (killed)
- Killed:
  - `tests/test_schedule.py::test_root_is_refused_and_launchd_is_never_asked[install]`
  - `tests/test_schedule.py::test_root_is_refused_and_launchd_is_never_asked[remove]`
  - `tests/test_schedule.py::test_root_is_refused_and_launchd_is_never_asked[show]`

Old text:

```
    if uid() == 0:

```

New text:

```
    if False:

```

### `u295.S3_argv_widened`

agent: the plist's program arguments carry an answer after sync night

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S3_argv_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 7 (killed)
- Killed:
  - `tests/test_schedule.py::test_install_and_show_agree_on_the_environment_shape`
  - `tests/test_schedule.py::test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`
  - `tests/test_schedule.py::test_show_reads_an_installed_agent_launchd_does_not_hold`
  - `tests/test_schedule.py::test_show_reads_an_installed_loaded_agent`
  - `tests/test_schedule.py::test_show_reads_the_night_line_from_the_state_the_agent_carries`
  - `tests/test_schedule.py::test_show_writes_nothing_and_asks_launchd_only_to_print`

Old text:

```
        "ProgramArguments": [str(crate), *NIGHT_ARGV],
```

New text:

```
        "ProgramArguments": [str(crate), *NIGHT_ARGV, "-d", "intake.land.native=go"],
```

### `u295.S4_run_at_load`

agent: the plist runs the night at load, so an install starts a pass at once

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S4_run_at_load`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 7 (killed)
- Killed:
  - `tests/test_schedule.py::test_install_and_show_agree_on_the_environment_shape`
  - `tests/test_schedule.py::test_install_writes_one_agent_that_runs_the_night_alone_and_loads_it`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`
  - `tests/test_schedule.py::test_show_reads_an_installed_agent_launchd_does_not_hold`
  - `tests/test_schedule.py::test_show_reads_an_installed_loaded_agent`
  - `tests/test_schedule.py::test_show_reads_the_night_line_from_the_state_the_agent_carries`
  - `tests/test_schedule.py::test_show_writes_nothing_and_asks_launchd_only_to_print`

Old text:

```
        "RunAtLoad": False,
    }
```

New text:

```
        "RunAtLoad": True,
    }
```

### `u295.S5_read_words_after_night`

read_agent: accept words after sync night, so show reads clean over an agent given an answer

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S5_read_words_after_night`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an answer]`
  - `tests/test_schedule.py::test_show_fails_over_an_agent_that_reads_another_installation_or_more_words[an empty word]`

Old text:

```
        and program[1:] == NIGHT_ARGV

```

New text:

```
        and program[1:3] == NIGHT_ARGV

```

### `u295.S6_daemons_directory`

launch_agents_dir: the plist goes beside the system's daemons instead of the person's agents

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S6_daemons_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_the_default_directory_is_the_persons_own_launch_agents`
  - `tests/test_schedule.py::test_the_module_names_no_system_domain_and_no_system_directory`

Old text:

```
    return Path.home() / "Library" / "LaunchAgents"
```

New text:

```
    return Path.home() / "Library" / "LaunchDaemons"
```

### `u295.S7_user_domain`

_domain: load into user/<uid> instead of the person's GUI login

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S7_user_domain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 63 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_binary_the_install_finds_on_its_path_alone_is_on_the_agents_path`
  - `tests/test_schedule.py::test_a_bootout_launchd_ignores_is_said_in_words_a_person_reads`
  - `tests/test_schedule.py::test_a_bootout_refused_over_an_agent_then_absent_boots_out_nothing`
  - `tests/test_schedule.py::test_a_bootstrap_launchd_does_not_then_hold_is_refused_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_bootstrap_that_fails_is_refused_in_its_words_and_leaves_nothing`
  - `tests/test_schedule.py::test_a_failed_load_launchd_may_still_hold_keeps_its_plist`
  - `tests/test_schedule.py::test_a_failed_replace_says_the_earlier_schedule_is_gone_too`
  - `tests/test_schedule.py::test_a_night_in_progress_is_never_booted_out[install]`
  - `tests/test_schedule.py::test_a_night_in_progress_is_never_booted_out[remove]`
  - `tests/test_schedule.py::test_a_plist_left_without_launchd_holding_it_is_replaced`
  - `tests/test_schedule.py::test_a_relative_override_is_carried_absolute`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[bootout fails]`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[print unreadable]`
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[stuck]`
  - `tests/test_schedule.py::test_a_replace_whose_write_fails_says_the_earlier_schedule_is_off`
  - ... and 48 more, see the JSON sidecar

Old text:

```
    return f"gui/{uid()}"
```

New text:

```
    return f"user/{uid()}"
```

### `u295.S8_unknown_read_absent`

loaded: any print failure reads as not loaded, absence read as evidence of absence

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S8_unknown_read_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 2 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[print unreadable]`
  - `tests/test_schedule.py::test_show_never_reads_launchd_it_cannot_read_as_not_loaded`

Old text:

```
    if answer.code == NOT_LOADED_CODE:

```

New text:

```
    if True:

```

### `u295.S9_skip_bootout_on_unknown`

_boot_out: skip the bootout when launchd cannot be read

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S9_skip_bootout_on_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1093 against a baseline of 1093
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_a_remove_launchd_does_not_confirm_keeps_the_plist[print unreadable]`

Old text:

```
    if state == NOT_LOADED:
        return False
    out = launchctl(
```

New text:

```
    if state != LOADED:
        return False
    out = launchctl(
```

### `u179-z.S4_to_fetch_counts_held`

_plan: count only new purchases, so a plan holding only part owned releases reads as nothing new

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179-z.json`, row `S4_to_fetch_counts_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_plan_holding_only_part_owned_releases_still_fetches_the_rest`

Old text:

```
    to_fetch = int(summary.get("new") or 0) + int(summary.get("held") or 0)
```

New text:

```
    to_fetch = int(summary.get("new") or 0)
```

### `u179-z.S9_refusals_need_permanence`

_fetched: read a fetch failed by a retryable item as settled too, so a transient failure lands the rest

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179-z.json`, row `S9_refusals_need_permanence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_fetch_failed_by_a_transient_answer_ends_the_verb_and_lands_nothing`

Old text:

```
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
```

New text:

```
    settled_with_refusals = job.state is jobs.JobState.FAILED
```

### `u179.D1_fetched_once`

_fetched: count every done item as staged, so a release two fetches held is named twice

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `D1_fetched_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first`

Old text:

```
    staged = [item for item in done if item.item_id not in seen]
```

New text:

```
    staged = list(done)
```

### `u179.D2_refused_once`

_fetched: name a release each time a fetch refuses it, the second round's same shape one list over

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `D2_refused_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`

Old text:

```
        if item.item_id not in taken and item.item_id not in already
```

New text:

```
        if item.item_id not in taken
```

### `u179.S10_open_fetch_stops`

_fetched: drop the stop on a fetch that did not settle, so a parked fetch goes on to the tail

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S10_open_fetch_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_fetch_failed_by_a_transient_answer_ends_the_verb_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_a_fetch_parked_by_the_session_ends_blocked_and_the_next_run_drives_it_on`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED and not settled_with_refusals:
        raise tail.Stop(FETCH, tail.job_error(report, job))
```

New text:

```
    if False:
        raise tail.Stop(FETCH, tail.job_error(report, job))
```

### `u179.S13_nothing_staged_ends`

sync_bandcamp: drop the empty folder end, so the tail is run over a folder holding nothing

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S13_nothing_staged_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`
  - `tests/test_sync_bandcamp.py::test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none`
  - `tests/test_sync_bandcamp.py::test_a_second_run_after_a_landing_finds_nothing_new_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing`

Old text:

```
        if not files:
            report.check(
```

New text:

```
        if False:
            report.check(
```

### `u179.S14_relist_after_name`

sync_bandcamp: read the tags of the files as staged before name apply renamed them

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S14_relist_after_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_the_tags_are_read_from_the_files_the_name_step_renamed`

Old text:

```
        folder = tail.through_name(report, folder, cfg)
        files = _staged(folder)
```

New text:

```
        folder = tail.through_name(report, folder, cfg)
```

### `u179.S15_unread_apart`

_read_tags: count a file whose tags could not be read as a file with no genre

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S15_unread_apart`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label`

Old text:

```
            report.summary["tags_unread"].append(path.name)
```

New text:

```
            report.summary["no_genre"].append(path.name)
```

### `u179.S16_no_genre_named`

_read_tags: never name a file with no genre

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S16_no_genre_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_files_left_without_a_genre_are_named_in_the_report`

Old text:

```
        if not (read.get("genre") or "").strip():
```

New text:

```
        if False:
```

### `u179.S17_label_flag_needs_a_label`

_landing: pass --label-from-tags whether or not any file carries a label tag

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S17_label_flag_needs_a_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_seller_no_label_names_lands_unlabelled_and_is_named`

Old text:

```
    if any(read.labels):
```

New text:

```
    if True:
```

### `u179.S1_fetch_only_when_planned`

sync_bandcamp: fetch whatever the plan said, so a plan with nothing new still queues a fetch

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S1_fetch_only_when_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_second_run_after_a_landing_finds_nothing_new_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing`
  - `tests/test_sync_bandcamp.py::test_the_same_batch_again_takes_the_staged_files_on_and_fetches_nothing_twice`

Old text:

```
        if planned:
            _fetch(report, cfg, batch, sellers)
```

New text:

```
        if True:
            _fetch(report, cfg, batch, sellers)
```

### `u179.S2_owned_recorded`

_plan: never record an owned purchase, so the report names nothing held as owned

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S2_owned_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_nothing_new_ends_with_no_fetch_no_tail_and_no_landing`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
        if row.get("disposition") == OWNED:
```

New text:

```
        if row.get("disposition") == "none":
```

### `u179.S3_held_recorded`

_plan: never record a purchase with tracks held back, so those owned tracks go unnamed

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S3_held_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_a_plan_holding_only_part_owned_releases_still_fetches_the_rest`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`

Old text:

```
        elif row.get("disposition") == HELD:
```

New text:

```
        elif row.get("disposition") == "none":
```

### `u179.S5_open_fetch_elsewhere`

_open_fetch: drop the other batch test, so an open fetch into another batch is driven into this one

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S5_open_fetch_elsewhere`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_an_open_fetch_into_another_batch_is_named_and_nothing_is_fetched`

Old text:

```
        if _batch_of(job) != batch:
            raise _Elsewhere(job, _batch_of(job))
```

New text:

```
        if False:
            raise _Elsewhere(job, _batch_of(job))
```

### `u179.S6_open_fetches_all`

_open_fetch: drive only the newest open fetch, the round one residual

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S6_open_fetches_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first`

Old text:

```
    return list(reversed(held))
```

New text:

```
    return held[:1]
```

### `u179.S7_open_fetch_order`

_open_fetch: drive the open fetches newest first rather than oldest first

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S7_open_fetch_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_two_fetches_left_open_in_the_batch_are_both_driven_on_oldest_first`

Old text:

```
    return list(reversed(held))
```

New text:

```
    return list(held)
```

### `u179.S8_refusals_settle`

_fetched: never read a fetch failed only by refusals as settled, so one lossy release ends the verb

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `S8_refusals_settle`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`
  - `tests/test_sync_bandcamp.py::test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none`

Old text:

```
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
```

New text:

```
    settled_with_refusals = False
```

### `u179.T1_rehearsal_runs`

sync_bandcamp: skip the rehearsal, so the landing is planned with none behind it

- File: `src/cratekit/cli/sync_bandcamp.py`
- Source: `u179.json`, row `T1_rehearsal_runs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`
- Collected: 34 against a baseline of 34
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_failed_rehearsal_plans_no_live_landing`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
        tail.rehearse(report, folder, landing)
```

New text:

```
        pass
```

### `u172-b.C3_left_miscounted`

guess: count the files left as the candidates written rather than the files still without a genre

- File: `src/cratekit/cli/tail.py`
- Source: `u172-b.json`, row `C3_left_miscounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_guess.py::test_the_files_left_are_the_files_still_without_a_genre`

Old text:

```
    left = count - after - unread
```

New text:

```
    left = count - before - written - unread
```

### `u172.C1_tail_skips_guess`

through_name: never run the guess after tag folder

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C1_tail_skips_guess`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_the_labels_release_reaches_the_same_gate_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp.py::test_the_tail_runs_on_the_absolute_batch_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
        if step == TAG:
            guess(chain, folder, pass_name)
```

New text:

```
        if False:
            guess(chain, folder, pass_name)
```

### `u172.C2_guess_without_pass`

guess_argv: never name the pass, so no playlist votes in a pass

- File: `src/cratekit/cli/tail.py`
- Source: `u172.json`, row `C2_guess_without_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_guess.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`
- Collected: 333 against a baseline of 333
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`
  - `tests/test_tag_guess.py::test_the_guess_is_named_with_a_pass_only_when_one_is_given`

Old text:

```
*([PASS_FLAG, pass_name] if pass_name else [])
```

New text:

```
*([])
```

### `u179.T2_rehearsal_ack_attends`

rehearse: a missing acknowledgment at the rehearsal ends the verb as a failure, not for a person

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T2_rehearsal_ack_attends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`

Old text:

```
        if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
```

New text:

```
        if cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
```

### `u179.T3_rehearsal_stop_wording`

attended: word a rehearsal's acknowledgment stop as a landing's, naming no rehearsal

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T3_rehearsal_stop_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 214 against a baseline of 214
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`

Old text:

```
            if stop.step == REHEARSE
            else (f"then plan the landing again: crate {command}",)
```

New text:

```
            if False
            else (f"then plan the landing again: crate {command}",)
```

### `u179.T4_commands_quoted`

attended: join the step's command with plain spaces, so a batch folder with a space cannot be pasted

- File: `src/cratekit/cli/tail.py`
- Source: `u179.json`, row `T4_commands_quoted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_failed_rehearsal_plans_no_live_landing`
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`
  - `tests/test_sync_bandcamp_native.py::test_one_new_puls_release_and_one_owned_land_one_batch_filed_under_its_label`

Old text:

```
    command = shlex.join(stop.argv)
```

New text:

```
    command = " ".join(stop.argv)
```

### `u181.T1_rescore_ignores_unable`

tail.rescore: queue the rescore although the model cannot score here

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T1_rescore_ignores_unable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`
  - `tests/test_vocals_cli.py::test_the_tails_rescore_asks_nothing_of_a_model_that_cannot_score`

Old text:

```
    if unable is not None:
        chain.summary["vocal_rescore"] = "skipped"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "skipped"
```

### `u181.T2_rescore_ignores_profile`

tail.rescore: run the vocals verb on a profile with the vocals module off

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T2_rescore_ignores_profile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_vocals_cli.py`
- Collected: 215 against a baseline of 215
- Kills: 30 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - ... and 15 more, see the JSON sidecar

Old text:

```
    if not vocals_on(cfg):
        chain.summary["vocal_rescore"] = "off"
```

New text:

```
    if False:
        chain.summary["vocal_rescore"] = "off"
```

### `u181.T3_rescore_keeps_stale`

tail.rescore: leave a stale vocals job over the folder open

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T3_rescore_keeps_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_the_tails_rescore_replaces_a_stale_vocals_job_over_the_folder`

Old text:

```
        replace_stale(chain, ANALYZE, VOCALS_VERB, folder, cfg)
```

New text:

```
        pass
```

### `u181.T4_rescore_failure_ignored`

tail.rescore: a vocals job that did not succeed is reported scored and the chain goes on

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T4_rescore_failure_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_vocals_cli.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_vocals_cli.py::test_a_rescore_job_that_does_not_succeed_ends_the_chain_at_the_analyze_step`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
        raise Stop(ANALYZE, job_error(chain, job))
    chain.summary["vocal_rescore"] = count
```

New text:

```
    chain.summary["vocal_rescore"] = count
```

### `u181.T5_rescore_never_run`

tail.run: the analyze step never rescores

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T5_rescore_never_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`
  - `tests/test_sync_land.py::test_the_analyze_step_rescores_after_analyze_run_and_before_the_restamp`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_tail_asks_the_vocal_model_before_analyze_run_binds_its_loader`

Old text:

```
        if step == ANALYZE:
            rescore(chain, folder, cfg, unable=unable)
```

New text:

```
        if False:
            rescore(chain, folder, cfg, unable=unable)
```

### `u181.T6_plan_warnings_not_lifted`

tail.land: the landing gate screen's warnings are not lifted onto the chain

- File: `src/cratekit/cli/tail.py`
- Source: `u181.json`, row `T6_plan_warnings_not_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 181 against a baseline of 181
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_warning_the_landing_plan_carries_rides_the_passes_own_warnings`

Old text:

```
        lift_plan_warnings(chain, cause)
```

New text:

```
        pass
```

### `u190.T1_run_folder_absolute`

run: trust the folder handed in as absolute

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T1_run_folder_absolute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_the_chain_runs_on_the_absolute_folder_whatever_it_is_handed`

Old text:

```
    folder = folder.expanduser().absolute()
    chain.summary["staging"] = str(folder)
```

New text:

```
    chain.summary["staging"] = str(folder)
```

### `u190.T3_stale_matches_folder`

replace_stale: cancel open tail jobs over any folder, so another folder's work is lost

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T3_stale_matches_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_stale_job_over_another_folder_or_library_is_left_alone`

Old text:

```
            and str((job.payload or {}).get("folder") or "") == str(folder)
```

New text:

```
            and True
```

### `u190.T4_name_answers_inline`

name_argv: leave name apply's confirm unanswered, so the chain stops at a gate a person running the tail answers on the command line

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T4_name_answers_inline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_name_apply_has_its_confirm_answered_inline_over_the_absolute_staging_folder`
  - `tests/test_sync_land.py::test_the_pass_runs_every_step_in_its_order_and_the_tail_on_the_absolute_staging_path`

Old text:

```
    return ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]
```

New text:

```
    return ["name", "apply", "--root", str(folder)]
```

### `u190.T6_chain_namespace`

Chain.check: key every check sync.land whatever the chain, so the go's checks read as a sync pass's

- File: `src/cratekit/cli/tail.py`
- Source: `u190.json`, row `T6_chain_namespace`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land.py`, `tests/test_label_sync.py`
- Collected: 275 against a baseline of 275
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_failing_analyze_run_stops_the_go_and_plans_no_landing`
  - `tests/test_label_sync_go.py::test_a_go_over_two_answered_releases_runs_the_tail_in_order_and_stops_at_the_landing_gate`
  - `tests/test_label_sync_go.py::test_a_landing_that_planned_nothing_ends_the_go_with_its_own_outcome`

Old text:

```
                "key": f"{self.namespace}.{step}",
```

New text:

```
                "key": f"sync.land.{step}",
```

### `u212.T1_reason_guard`

tail.second_copies: read any refusal's outstanding files, not only rename-incomplete's

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T1_reason_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_stop_that_is_not_rename_incomplete_or_cannot_read_the_queue_is_unchanged`

Old text:

```
    if cause.reason != RENAME_INCOMPLETE:
        return stop
```

New text:

```
(empty)
```

### `u212.T2_done_only`

tail._downloaded_by: a job that froze the track and never acquired it is named as its source

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T2_done_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if refs & done:
```

New text:

```
            if refs:
```

### `u212.T3_library`

tail._downloaded_by: another library's download job is named

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T3_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
            if cfg is not None and job.library_id != cfg.library.volume_id:
                continue
```

New text:

```
(empty)
```

### `u212.T4_earliest_first`

tail._downloaded_by: the passes named newest first, though the step says earliest first

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T4_earliest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_the_passes_named_are_this_librarys_finished_downloads_earliest_first`

Old text:

```
        for job in reversed(jobs.list_jobs(store)):
```

New text:

```
        for job in jobs.list_jobs(store):
```

### `u212.T5_name_wraps`

tail.name: the name step's stop passed on without the passes that downloaded the copy

- File: `src/cratekit/cli/tail.py`
- Source: `u212.json`, row `T5_name_wraps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_cli_contract.py`, `tests/test_crate_sync_skill.py`, `tests/test_drift.py`, `tests/test_label_sync_go.py`, `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_tag_guess.py`, `tests/test_vocals_cli.py`
- Collected: 1607 against a baseline of 1607
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_name_stop_over_a_second_copy_names_the_pass_that_downloaded_it`
  - `tests/test_sync_land_staged.py::test_a_second_copy_no_download_job_records_is_said_so`

Old text:

```
        raise second_copies(stop, cfg) from None
```

New text:

```
        raise stop from None
```

### `u284.T1_pass_names_nothing`

tail.tail_step: the pass never names the files the catalogues refused

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T1_pass_names_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_a_token_the_pass_reaches_its_landing_and_names_the_refused_files`

Old text:

```
    if step == TAG:
        refused_files(chain, chain.settled.get(step))
```

New text:

```
    if False:
        refused_files(chain, chain.settled.get(step))
```

### `u284.T2_pass_stop_unsaid`

tail.tail_step: the pass's stop at its tag step says nothing of who refused or the token

- File: `src/cratekit/cli/tail.py`
- Source: `u284.json`, row `T2_pass_stop_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_refused.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`, `tests/test_tag_guess.py`, `tests/test_tag_folder_copyright.py`
- Collected: 385 against a baseline of 385
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_refused.py::test_with_no_token_the_pass_stops_at_its_tag_step_saying_who_refused_and_the_token`

Old text:

```
        raise Stop(step, refused_stop(error, chain.settled.get(step)) if step == TAG else error)
```

New text:

```
        raise Stop(step, error)
```

### `u319.M10_sync_stop_drops_the_short_path`

tail: the step crate sync land prints names one path again

- File: `src/cratekit/cli/tail.py`
- Source: `u319.json`, row `M10_sync_stop_drops_the_short_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_drift.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_label_sync_go.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_drift.py::test_the_sync_stop_offers_the_auto_analysis_path_after_the_selections_it_stands_in_for`

Old text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}; "
    f"{AUTO_ANALYSIS_STEP}",
```

New text:

```
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS}",
```

### `u168.C3_default_actor_cli`

_actor: default to cli whatever the terminal

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C3_default_actor_cli`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`
- Collected: 8 against a baseline of 8
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_decide_continue.py::test_a_continuation_that_refuses_answers_with_its_refusal_and_keeps_the_answer`
  - `tests/test_run_decide_continue.py::test_a_session_answers_and_mints_in_one_command_with_no_actor_given`
  - `tests/test_run_decide_continue.py::test_with_no_terminal_and_no_actor_the_answer_is_the_sessions`

Old text:

```
    if session.has_controlling_terminal():
        return TERMINAL_ACTOR, "a terminal, and no --actor"
```

New text:

```
    if True:
        return TERMINAL_ACTOR, "a terminal, and no --actor"
```

### `u168.C4_default_actor_session`

_actor: default to session even at a terminal

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C4_default_actor_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_decide_continue.py::test_at_a_terminal_and_no_actor_the_answer_is_the_command_lines`

Old text:

```
    if session.has_controlling_terminal():
        return TERMINAL_ACTOR, "a terminal, and no --actor"
```

New text:

```
    if False:
        return TERMINAL_ACTOR, "a terminal, and no --actor"
```

### `u168.C5_given_actor_ignored`

_actor: ignore an actor given with --actor

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C5_given_actor_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_decide_continue.py::test_an_actor_given_is_recorded_whatever_the_terminal`

Old text:

```
    if given is not None:
        return given, "given with --actor"
```

New text:

```
    if False:
        return given, "given with --actor"
```

### `u168.C6_no_argv_continues`

_continued: skip the refusal for a run that keeps no command line

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C6_no_argv_continues`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`
- Collected: 8 against a baseline of 8
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_decide_continue.py::test_a_run_that_keeps_no_command_line_is_refused_with_the_answer_recorded`

Old text:

```
    if state.argv is None:
        raise CratekitError(
```

New text:

```
    if state.argv is None and False:
        raise CratekitError(
```

### `u168.C7_continue_without_run`

_continued: dispatch the verb again without --run, as a new run

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C7_continue_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1005 against a baseline of 1005
- Kills: 2 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_a_session_answers_and_mints_in_one_command_with_no_actor_given`

Old text:

```
    envelope = cli.dispatch(["--run", state.run_id, *state.argv], stderr=sys.stderr)
```

New text:

```
    envelope = cli.dispatch([*state.argv], stderr=sys.stderr)
```

### `u170.R10_moved_guard`

_retire_one: record on a gate that moved since the plan

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R10_moved_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again`

Old text:

```
    if state.open_gate != one.gate:
```

New text:

```
    if False:
```

### `u170.R11_digest_ids_only`

retire: digest the planned run ids alone, not when each went idle

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R11_digest_ids_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_answer_is_stale_once_a_planned_run_is_resumed_even_if_it_stays_old`

Old text:

```
    plan = {"digest": digest_of(items), "count": len(items), "items": items}
```

New text:

```
    plan = {"digest": digest_of([one["run_id"] for one in items]), "count": len(items), "items": items}
```

### `u170.R12_default_week`

retire: default threshold fixed at seven days, not the file's

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R12_default_week`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_reads_its_default_threshold_from_the_file`

Old text:

```
        age = timedelta(days=config.load().reports.open_gate_stale_days)
```

New text:

```
        age = timedelta(days=7)
```

### `u170.R1_zero_days`

older_than: accept 0d

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R1_zero_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_age_that_is_not_a_whole_number_of_days_is_a_usage_error[0d]`

Old text:

```
_AGE = re.compile(r"^([1-9][0-9]*)d$")
```

New text:

```
_AGE = re.compile(r"^([0-9]+)d$")
```

### `u170.R2_ceiling`

older_than: the ceiling one day higher

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R2_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_age_that_is_not_a_whole_number_of_days_is_a_usage_error[3651d]`

Old text:

```
    if not match or days > config.MAX_OPEN_GATE_STALE_DAYS:
```

New text:

```
    if not match or days > config.MAX_OPEN_GATE_STALE_DAYS + 1:
```

### `u170.R3_own_run`

old_gates: plan the asking run too

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R3_own_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_never_retires_its_own_run`

Old text:

```
        if path.stem == skip:
```

New text:

```
        if False:
```

### `u170.R4_unreadable_dropped`

old_gates: drop an unreadable record without saying so

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R4_unreadable_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_record_retire_cannot_read_is_said_and_not_dropped`

Old text:

```
            unreadable.append(path.stem)
```

New text:

```
            pass
```

### `u170.R5_answers_apply`

_retire_one: record the gate's first option, apply, instead of abort

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R5_answers_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`

Old text:

```
    gates.record(state, spec, gates.RETIRE_OPTION, actor=SESSION_ACTOR)
```

New text:

```
    gates.record(state, spec, spec.options[0], actor=SESSION_ACTOR)
```

### `u170.R6_actor_cli`

_retire_one: record the abort as cli instead of session

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R6_actor_cli`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`

Old text:

```
    gates.record(state, spec, gates.RETIRE_OPTION, actor=SESSION_ACTOR)
```

New text:

```
    gates.record(state, spec, gates.RETIRE_OPTION, actor=TERMINAL_ACTOR)
```

### `u170.R7_declined_applies`

retire: an abort on the confirm still retires

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R7_declined_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_declined_retirement_answers_nothing`

Old text:

```
    if option != "apply":
```

New text:

```
    if False:
```

### `u170.R8_empty_asks`

retire: an empty plan is asked over instead of ending with no change

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R8_empty_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_says_nothing_about_an_old_run_already_answered`
  - `tests/test_run_retire.py::test_retire_with_nothing_old_asks_nothing_and_changes_nothing`

Old text:

```
    if not planned:
```

New text:

```
    if False:
```

### `u170.R9_kept_planned`

retire: plan every old gate, the kept ones too

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R9_kept_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1704 against a baseline of 1704
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`

Old text:

```
    planned = [one for one in found if one.retirable]
```

New text:

```
    planned = list(found)
```

### `u186.R1_decide_abort`

same_plan_answered: drop the abort refusal, so two aborts over one plan warn

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R1_decide_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_both_answers_are_abort`

Old text:

```
    if option == gates.RETIRE_OPTION or offered is None:
```

New text:

```
    if offered is None:
```

### `u186.R2_decide_no_digest`

same_plan_answered: drop the no digest refusal, so a run offered nothing matches a sibling that recorded none

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R2_decide_no_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_this_run_was_offered_no_digest`

Old text:

```
    if option == gates.RETIRE_OPTION or offered is None:
```

New text:

```
    if option == gates.RETIRE_OPTION:
```

### `u186.R3_decide_any_gate`

same_plan_answered: match an answer on any gate, not the one being answered

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R3_decide_any_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_answered_another_gate`

Old text:

```
            name == gate and held.option == option and held.digest == offered
```

New text:

```
            held.option == option and held.digest == offered
```

### `u186.R4_decide_any_option`

same_plan_answered: match an answer of any option, so a sibling's abort warns over an apply

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R4_decide_any_option`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_aborted`

Old text:

```
            name == gate and held.option == option and held.digest == offered
```

New text:

```
            name == gate and held.digest == offered
```

### `u186.R5_decide_any_digest`

same_plan_answered: match an answer over any digest, so another plan's approval warns

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R5_decide_any_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_the_sibling_answered_another_plan`

Old text:

```
            name == gate and held.option == option and held.digest == offered
```

New text:

```
            name == gate and held.option == option
```

### `u186.R6_decide_unwired`

decide: never compute the repeat, so run decide says nothing over a sibling that approved the same plan

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R6_decide_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 3 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`

Old text:

```
    said = same_plan_answered(state, spec.name, ctx.args.option)
```

New text:

```
    said = []
```

### `u186.R7_continue_dedupe`

_continued: drop the dedupe, so a sibling named by decide and by the stale gate is said twice

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R7_continue_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_continue_says_a_sibling_once_when_the_verb_stops_at_its_gate_again`

Old text:

```
    repeated = [one for one in said if one not in envelope.warnings]
```

New text:

```
    repeated = list(said)
```

### `u186.R8_continue_drops_repeat`

_continued: drop the repeat on a continued run's envelope

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u186.json`, row `R8_continue_drops_repeat`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_siblings.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`

Old text:

```
    repeated = [one for one in said if one not in envelope.warnings]
```

New text:

```
    repeated = []
```

### `u294.M05_suggest_step_band`

the suggest step plans at medium rather than the backlog's floor

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M05_suggest_step_band`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_the_suggest_step_plans_at_the_backlogs_floor`

Old text:

```
        band=backlog.FLOOR,
```

New text:

```
        band=suggest.MEDIUM,
```

### `u294.M06_served_is_every_row`

the rows step keeps every backlog row rather than the served ones

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M06_served_is_every_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 9 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_the_fourth_step_refusing_stops_the_campaign_after_the_words`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    served = frozenset(row.content_id for row in plan.rows if row.status == backlog.SERVED)
```

New text:

```
    served = frozenset(row.content_id for row in plan.rows)
```

### `u294.M07_followers_another_spelling`

the follow step writes a row whose file carries another spelling than the answer filed

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M07_followers_another_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`

Old text:

```
    narrowed = rows.narrowed(whole, keep - other)
```

New text:

```
    narrowed = rows.narrowed(whole, keep)
```

### `u294.M08_alias_files_stale_check`

the words step drops its check that the alias would retag the files the gate listed

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M08_alias_files_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`

Old text:

```
        if (planned.edit.display, files) != (shown.genre, shown.files):
```

New text:

```
        if planned.edit.display != shown.genre:
```

### `u294.M09_digest_drops_words`

the digest leaves out the words and their files, so a file that came to carry a word moves nothing

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M09_digest_drops_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`

Old text:

```
            "words": [word.to_json() for word in words],
```

New text:

```
            "words": [],
```

### `u294.M10_digest_drops_answers`

the digest leaves out the answers, so an answer changed between the gate and the apply is not stale

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M10_digest_drops_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_the_digest_moves_with_an_answer_a_proposal_or_a_row`

Old text:

```
            "answers": [answer.to_json() for answer in given],
            "words": [word.to_json() for word in words],
```

New text:

```
            "answers": [],
            "words": [word.to_json() for word in words],
```

### `u294.M11_unknown_word_accepted`

an answer naming no word the backlog holds is dropped rather than refused

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M11_unknown_word_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias0-folder0-leave_word0-names no word]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias1-folder1-leave_word1-names no word]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias2-folder2-leave_word2-names no word]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses_before_anything_is_written`

Old text:

```
            if _held_by_copy(declared, spelling, kind, genre):
```

New text:

```
            if True:
```

### `u294.M12_settled_answer_taken`

an answer to a settled word is dropped whatever it says, rather than refused

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M12_settled_answer_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias7-folder7-leave_word7-already has its one answer]`

Old text:

```
            if _same_as_settled(word, kind, genre):
```

New text:

```
            if True:
```

### `u294.M13_unanswerable_accepted`

an answer to a word neither verb takes is not refused

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M13_unanswerable_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias8-folder8-leave_word8-cannot be answered]`

Old text:

```
        if word.unanswerable is not None:
            raise _invalid(
```

New text:

```
        if False:
            raise _invalid(
```

### `u294.M14_answered_twice`

a word answered twice takes the last answer rather than refusing

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M14_answered_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias5-folder5-leave_word5-answered twice]`
  - `tests/test_tag_campaign.py::test_an_answer_the_plan_does_not_hold_refuses[alias6-folder6-leave_word6-answered twice]`

Old text:

```
        if word.spelling in found:
```

New text:

```
        if False:
```

### `u294.M15_text_not_threaded`

each word's edit is planned on the copy as it stands, not on the text the words before it leave

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M15_text_not_threaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_an_alias_to_the_folder_another_answer_makes_is_planned_on_that_folder`

Old text:

```
        text = edit.after
```

New text:

```
        text = text
```

### `u294.M16_settled_unreached`

the campaign runs a settled word's answer even when it moves no row

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M16_settled_unreached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    return [word for word in plan.words if word.settled and word.reached]
```

New text:

```
    return [word for word in plan.words if word.settled]
```

### `u294.M18_no_reload_after_words`

the rows that follow are planned on the taxonomy as it was before the words step wrote the copy

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M18_no_reload_after_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`

Old text:

```
            # THE COPY MOVED, so the rows that follow are planned on it.
            declared = active_taxonomy.load(cfg)
```

New text:

```
            # THE COPY MOVED, so the rows that follow are planned on it.
            pass
```

### `u294.M19_ack_skipped`

the backup acknowledgment is not read before the plan and the gate

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M19_ack_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_cli_contract.py`
- Collected: 1053 against a baseline of 1053
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).
    session.assert_backup_acknowledged(cfg)

    args = ctx.args
```

New text:

```
    # BEFORE THE PLAN IS BUILT AND BEFORE THE GATE (R-733).

    args = ctx.args
```

### `u294.M20_abort_applies`

an aborted gate goes on to the steps as if applied

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M20_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_declined_campaign_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=facts) != APPLY:
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=facts) not in (APPLY, "abort"):
```

### `u294.M24_notes_dropped`

the gate and the report carry none of the backlog's own notes

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M24_notes_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_catalogue_nobody_could_read_is_said_at_the_gate`
  - `tests/test_tag_campaign.py::test_the_gate_and_the_report_say_what_the_verbs_could_not_read`

Old text:

```
        if note["code"] in _CARRIED and note["code"] != backlog_cli.ROWS_JOINING
```

New text:

```
        if False
```

### `u294.M25_folder_stale_check`

the words step drops its check that the folder edit is the one the gate listed

- File: `src/cratekit/cli/verbs/tag_campaign.py`
- Source: `u294.json`, row `M25_folder_stale_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_folder_that_would_copy_another_bucket_after_the_gate_stops_the_words_as_stale`

Old text:

```
            if fresh != (shown.genre, shown.bucket, shown.like, shown.copy):
```

New text:

```
            if False:
```

