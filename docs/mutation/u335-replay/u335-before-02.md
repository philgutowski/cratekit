# Mutation table: u335-before-02

Measured by `scripts/mutate.py` on 2026-11-24 05:09 UTC, branch `HEAD` at `b41c698d`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23216 collected. pytest invocations for this batch: 271.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 05:09 UTC for commit `b41c698da363`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 55, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23216 against 23216. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u239.L02_remember_owner` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 2 | killed |
| `u239.L03_remember_called` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 6 | killed |
| `u239.L05_commands_added` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 3 | killed |
| `u239.L06_unrecorded_warning` | `src/cratekit/cli/label_sync.py` | user | 3 file(s) | 276 | 1 | killed |
| `u303.L1_land_key_wrong` | `src/cratekit/cli/label_sync.py` | user | 2 file(s) | 134 | 60 | killed |
| `u303.L2_tail_not_kept` | `src/cratekit/cli/label_sync.py` | user | 2 file(s) | 134 | 4 | killed |
| `r1394.S3_bool_count_read` | `src/cratekit/cli/output.py` | maintainer | 2 file(s) | 177 | 1 | killed |
| `r1394.S4_negative_count_read` | `src/cratekit/cli/output.py` | maintainer | 2 file(s) | 177 | 1 | killed |
| `u298.H5_approving_actor_default` | `src/cratekit/cli/output.py` | user | 1 file(s) | 100 | 1 | killed |
| `r2020.M22_rebuild_returns_none` | `src/cratekit/cli/rebuild.py` | user | 4 file(s) | 261 | 6 | killed |
| `r2020.M23_rebuild_resume_no_found` | `src/cratekit/cli/rebuild.py` | user | 4 file(s) | 261 | 6 | killed |
| `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 21 | killed |
| `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.W4_rebuild_worker` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.W6_rebuild_resume_loads_first` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 3 | killed |
| `u328.S1_a_part_left_out_of_the_table` | `src/cratekit/cli/registry.py` | user | 92 file(s) | 8498 | collection error | collect-error |
| `r773-b.R1_doctor_check_not_declared` | `src/cratekit/cli/registry_later.py` | maintainer | 1 file(s) | 94 | 1 | killed |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry_modules.py` | maintainer | 21 file(s) | 4172 | collection error | collect-error |
| `r770-d.C8_native_gate_answered_inline` | `src/cratekit/cli/registry_pipeline.py` | user | 2 file(s) | 1053 | 6 | killed |
| `u91.G1_registry_xml` | `src/cratekit/cli/registry_pipeline.py` | user | 2 file(s) | 1217 | 1 | killed |
| `r678-a.A1_drop_the_job_state_case` | `src/cratekit/cli/render.py` | user | 5 file(s) | 327 | 9 | killed |
| `r686.R1_empty_list_bare_header` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1217 | 3 | killed |
| `u295.S10_stuck_accepted` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 4 | killed |
| `u295.S11_no_read_back` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S12_cleanup_ignores_launchd` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S13_cleanup_keeps_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 3 | killed |
| `u295.S14_dirs_not_resolved` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 11 | killed |
| `u295.S15_override_relative` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S16_any_bin_prefix` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S17_plist_mode` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S18_crate_exec_bit` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S19_keys_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S1_platform_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 6 | killed |
| `u295.S20_gone_crate_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S21_run_at_load_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S22_env_names_unchecked` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 2 | killed |
| `u295.S23_show_always_clean` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 26 | killed |
| `u295.S24_loaded_without_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u295.S25_install_lockless` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 2 | killed |
| `u295.S2_root_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 3 | killed |
| `u295.S3_argv_widened` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 7 | killed |
| `u295.S4_run_at_load` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 7 | killed |
| `u295.S5_read_words_after_night` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 2 | killed |
| `u295.S7_user_domain` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 63 | killed |
| `u295.S8_unknown_read_absent` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 2 | killed |
| `u295.S9_skip_bootout_on_unknown` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1116 | 1 | killed |
| `u154.G16_wizard_default_dropped` | `src/cratekit/cli/setup.py` | user | 1 file(s) | 6 | 1 | killed |
| `u283.S10_any_raise_escapes` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 2 | killed |
| `u283.S11_vocabulary_never_noted` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 2 | killed |
| `u283.S12_vocabulary_always_noted` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S13_linked_copy_not_checked` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 1 | killed |
| `u283.S17_verb_skips_step` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 4 | killed |
| `u283.S4_recorded_never_acknowledged` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 3 | killed |
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
| `r1115.S1_sync_land_stops_on_unsettled` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1115.S2_sync_land_names_the_refused` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1499.S01_download_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 12 | killed |
| `r1499.S02_tail_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S03_arrival_after_tail` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1499.S04_arrival_after_plan` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S05_keep_after_arrival` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1499.S06_keep_called` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 7 | killed |
| `r1499.S07_kept_read` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 4 | killed |
| `r1499.S08_own_pass_proof` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 2 | killed |
| `r1499.S09_own_library` | `src/cratekit/cli/sync_land.py` | maintainer | 6 file(s) | 325 | 1 | killed |
| `r1499.S10_own_by_list` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 66 | killed |
| `r1499.S11_unreadable_refuses` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S12_warnings_in_refusal` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `r1499.S13_own_unnamed_step` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 325 | 1 | killed |
| `u152.R13_missing_lift` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R14_download_list_match` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R15_download_newest` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R16_download_cancelled` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R17_download_retry` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R20_nothing_downloaded` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 2 | killed |
| `u152.R2_preflight_backup` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R6_lift_failed_checks` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 2 | killed |
| `u152.R7_outbound_held` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 2 | killed |
| `u152.R8_continue_open_pass` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u152.R9_open_passes_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1207 | 1 | killed |
| `u179.P1_shared_preflight` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 104 | 3 | killed |
| `u181.S1_profile_off_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1091 | 1 | killed |
| `u181.S2_gate_never_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1091 | 6 | killed |
| `u181.S3_stop_goes_on` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M18_left_open_taken` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M19_left_open_identity` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M20_cancelled_driven` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u182.M21_all_cancelled_done` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u182.M22_skip_failed` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M11_land_runs_named` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 2 | killed |
| `u183.M12_preflight_way_back` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M14_retryable_intake_continues` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M15_continue_command_words` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 9 | killed |
| `u183.M1_pass_run_as_given` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 16 | killed |
| `u183.M2_land_record_resolves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 3 | killed |
| `u183.M3_recorded_pass_needs_a_job` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M6_unreadable_record` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M7_remember_saves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M8_remember_called` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 5 | killed |
| `u212.S1_missing_ends` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 330 | 1 | killed |
| `u212.S4_staged_said` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 330 | 1 | killed |
| `u227.R15_way_on_wording` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R19_take_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R20_take_source` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 2 | killed |
| `u227.R21_take_continued` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R22_take_not_driven` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R25_way_on_state` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u293.S3_sync_land_holds` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 144 | 1 | killed |
| `u293.N1_no_answer` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 4 | killed |
| `u293.N2_rekordbox_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 3 | killed |
| `u293.N3_live_job_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 1 | killed |
| `u293.N4_occupied_refused` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 4 | killed |
| `u293.N5_owed_kept` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 3 | killed |
| `u293.N6_settled_by_landing` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 1 | killed |
| `u293.N7_unread_landing_is_not_settled` | `src/cratekit/cli/sync_night.py` | user | 3 file(s) | 1091 | 1 | killed |
| `u172-b.C3_left_miscounted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 1 | killed |
| `u172.C1_tail_skips_guess` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 5 | killed |
| `u172.C2_guess_without_pass` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 333 | 2 | killed |
| `u179.T2_rehearsal_ack_attends` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T3_rehearsal_stop_wording` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T4_commands_quoted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 215 | 3 | killed |
| `u181.T1_rescore_ignores_unable` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 217 | 4 | killed |
| `u181.T2_rescore_ignores_profile` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 217 | 30 | killed |
| `u181.T3_rescore_keeps_stale` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 36 | 1 | killed |
| `u181.T4_rescore_failure_ignored` | `src/cratekit/cli/tail.py` | user | 1 file(s) | 36 | 1 | killed |
| `u181.T5_rescore_never_run` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 4 | killed |
| `u181.T6_plan_warnings_not_lifted` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 1 | killed |
| `u190.T1_run_folder_absolute` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 1 | killed |
| `u190.T3_stale_matches_folder` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 1 | killed |
| `u190.T4_name_answers_inline` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 2 | killed |
| `u190.T6_chain_namespace` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 276 | 3 | killed |
| `u212.T1_reason_guard` | `src/cratekit/cli/tail.py` | maintainer | 11 file(s) | 1638 | 1 | killed |
| `u212.T2_done_only` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1638 | 1 | killed |
| `u212.T3_library` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1638 | 1 | killed |
| `u212.T4_earliest_first` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1638 | 1 | killed |
| `u212.T5_name_wraps` | `src/cratekit/cli/tail.py` | user | 11 file(s) | 1638 | 2 | killed |
| `u284.T1_pass_names_nothing` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u284.T2_pass_stop_unsaid` | `src/cratekit/cli/tail.py` | user | 5 file(s) | 385 | 1 | killed |
| `u168.C3_default_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 3 | killed |
| `u168.C4_default_actor_session` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C5_given_actor_ignored` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C6_no_argv_continues` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C7_continue_without_run` | `src/cratekit/cli/verbs/runs.py` | user | 2 file(s) | 1028 | 2 | killed |
| `u170.R10_moved_guard` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R11_digest_ids_only` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R12_default_week` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R1_zero_days` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R2_ceiling` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R3_own_run` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R4_unreadable_dropped` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R5_answers_apply` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 2 | killed |
| `u170.R6_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 2 | killed |
| `u170.R7_declined_applies` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u170.R8_empty_asks` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 2 | killed |
| `u170.R9_kept_planned` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1739 | 1 | killed |
| `u294.M05_suggest_step_band` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M06_served_is_every_row` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 9 | killed |
| `u294.M08_alias_files_stale_check` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M09_digest_drops_words` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M15_text_not_threaded` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u294.M16_settled_unreached` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 3 | killed |
| `u294.M24_notes_dropped` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 2 | killed |
| `u294.M25_folder_stale_check` | `src/cratekit/cli/verbs/tag_campaign.py` | user | 1 file(s) | 56 | 1 | killed |
| `u132.V5_nothing` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 51 | 2 | killed |
| `u133-a.P12_verb_warning` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 51 | 1 | killed |
| `u194.W24_write_copy_bytes_stale` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 119 | 1 | killed |
| `u194.W25_write_copy_read_back` | `src/cratekit/cli/verbs/taxonomy.py` | user | 2 file(s) | 119 | 2 | killed |
| `r1184.M17_verb_takes_step` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 3 | killed |
| `r1184.M18_verb_nothing_to_do` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W18_carrying_several_genres` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W19_carrying_unread` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 2 | killed |
| `u194.W20_retag_reread` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W21_retag_read_back` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W22_unwritten_refusal` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u194.W23_root_missing` | `src/cratekit/cli/verbs/taxonomy_word.py` | user | 1 file(s) | 68 | 1 | killed |
| `u331.S15_foreign_reexport_keeps_every_row` | `src/cratekit/core/active_taxonomy.py` | user | 3 file(s) | 170 | 2 | killed |
| `u260.E11_reset_forgets_nothing` | `src/cratekit/core/art.py` | maintainer | 4 file(s) | 269 | 13 | killed |
| `u260.E6_encode_never_remembered` | `src/cratekit/core/art.py` | user | 4 file(s) | 269 | 11 | killed |
| `u84-a.A10_native_resolution` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 12 | killed |
| `u84-a.A11_dimensions_from_new_bytes` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 10 | killed |
| `u84-a.A12_all_or_nothing` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 6 | killed |
| `u84-a.A8_no_picture_is_none` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 2 | killed |
| `u84-b.A16_shrink_fallback` | `src/cratekit/core/art.py` | user | 3 file(s) | 245 | 2 | killed |
| `u84-b.A17_too_small_to_shrink` | `src/cratekit/core/art.py` | maintainer | 3 file(s) | 245 | 1 | killed |
| `r1103.C1_exit_code` | `src/cratekit/core/cause.py` | user | 3 file(s) | 381 | 2 | killed |
| `r290-author.R3_the_owner_drops_the_type` | `src/cratekit/core/cause.py` | user | 3 file(s) | 317 | 13 | killed |
| `r388-c.M14_status_registration_dropped` | `src/cratekit/core/cause.py` | maintainer | 70 file(s) | 8192 | 2 | killed |
| `r388-c.M15_status_code_disagrees` | `src/cratekit/core/cause.py` | maintainer | 70 file(s) | 8192 | 2 | killed |
| `u138.E2_reason_exit_code` | `src/cratekit/core/cause.py` | user | 1 file(s) | 26 | 9 | killed |
| `u27-restore-cli-author.R3_a_backup_slug_leaves_the_cause_vocabulary` | `src/cratekit/core/cause.py` | user | 2 file(s) | 242 | 3 | killed |
| `u27-restore-cli-author.R4_a_backup_slug_takes_the_wrong_status` | `src/cratekit/core/cause.py` | maintainer | 1 file(s) | 148 | 1 | killed |
| `u27-restore-cli-independent.I_G1_a_second_backup_slug_takes_the_wrong_status` | `src/cratekit/core/cause.py` | maintainer | 3 file(s) | 471 | 2 | killed |
| `u43-author-light.R2_undeclared_refusal_slug` | `src/cratekit/core/cause.py` | user | 31 file(s) | 5370 | 6 | killed |
| `u272.C1_no_flush` | `src/cratekit/core/config.py` | user | 7 file(s) | 642 | 14 | killed |
| `u272.C3_full_flush_then_sync` | `src/cratekit/core/config.py` | maintainer | 7 file(s) | 642 | 1 | killed |

## Row definitions

### `u239.L02_remember_owner`

_remember: record on whichever run ran the tail, the round one blocking shape

- File: `src/cratekit/cli/label_sync.py`
- Source: `u239.json`, row `L02_remember_owner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land.py`
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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

### `u303.L1_land_key_wrong`

label_sync: the go's landing is read under the wrong key, so no tail is found

- File: `src/cratekit/cli/label_sync.py`
- Source: `u303.json`, row `L1_land_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land_beside.py`
- Collected: 134 against a baseline of 134
- Kills: 60 (killed)
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
  - ... and 45 more, see the JSON sidecar

Old text:

```
    land = report.get(go.LAND_KEY) if isinstance(report, Mapping) else None
```

New text:

```
    land = report.get("landing") if isinstance(report, Mapping) else None
```

### `u303.L2_tail_not_kept`

label_sync: the downloads the go's tail leaves are no longer kept under the job

- File: `src/cratekit/cli/label_sync.py`
- Source: `u303.json`, row `L2_tail_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_sync_go.py`, `tests/test_sync_land_beside.py`
- Collected: 134 against a baseline of 134
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_file_under_a_name_the_tail_left_but_not_the_same_file_is_not_the_gos`
  - `tests/test_label_sync_go.py::test_a_go_whose_tail_renamed_its_tracks_and_stopped_runs_its_tail_again_under_its_run`
  - `tests/test_label_sync_go.py::test_a_tails_record_that_cannot_be_read_reads_nothing_as_the_gos_own`
  - `tests/test_label_sync_go.py::test_the_tail_keeps_what_it_left_whichever_way_it_ends`

Old text:

```
            go.keep_tail(cfg, store, job, folder)
```

New text:

```
            pass
```

### `r1394.S3_bool_count_read`

stopped write: a count written as true or false is read as a number

- File: `src/cratekit/cli/output.py`
- Source: `r1394.json`, row `S3_bool_count_read`
- Moved: U298 replaced pair_stopped's _count with cli.output.count_of, the same three part check, which _moving now calls for both counts
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
```

New text:

```
    if not isinstance(value, int) or value < 0:
```

### `r1394.S4_negative_count_read`

stopped write: a negative count is read as one

- File: `src/cratekit/cli/output.py`
- Source: `r1394.json`, row `S4_negative_count_read`
- Moved: U298 replaced pair_stopped's _count with cli.output.count_of, the same three part check, which _moving now calls for both counts
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`

Old text:

```
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
```

New text:

```
    if isinstance(value, bool) or not isinstance(value, int):
```

### `u298.H5_approving_actor_default`

approving_actor: a run nobody decided reads as the cli actor

- File: `src/cratekit/cli/output.py`
- Source: `u298.json`, row `H5_approving_actor_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_shared_homes.py::test_the_approving_actor_is_read_off_the_recorded_decision`

Old text:

```
    return decision.actor if decision is not None else ""
```

New text:

```
    return decision.actor if decision is not None else "cli"
```

### `r2020.M22_rebuild_returns_none`

the rebuild worker: stage no report, as before R-2020

- File: `src/cratekit/cli/rebuild.py`
- Source: `r2020.json`, row `M22_rebuild_returns_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`
  - `tests/test_routing_workers.py::test_the_rebuild_worker_stages_its_after_check_as_its_report`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps`
  - `tests/test_unread_playlist_warnings.py::test_the_rebuild_worker_reports_its_after_check`

Old text:

```
    return REBUILD_ARTIFACTS.produced(
        cfg, job, item, engine.after_report(tree_id, report.after, active_taxonomy.load(cfg))
    )
```

New text:

```
    return None
```

### `r2020.M23_rebuild_resume_no_found`

the rebuild's resume: leave the drive's findings off its success envelope

- File: `src/cratekit/cli/rebuild.py`
- Source: `r2020.json`, row `M23_rebuild_resume_no_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_resume_that_drove_nothing_carries_no_vocal_warning[rebuild]`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_the_rebuild_worker_reports_its_after_check`

Old text:

```
        warnings = (*warnings, *drive.found(threshold, declared))
```

New text:

```
        warnings = (*warnings,)
```

### `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped`

The rebuild files a job with no items, the state every rebuild was in before this unit

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `I3_rebuild_items_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 21 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_over_an_absent_music_directory_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-native]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`
  - `tests/test_routing_workers.py::test_a_resume_reads_no_registry_of_its_own`
  - `tests/test_routing_workers.py::test_a_resume_that_drove_nothing_carries_no_vocal_warning[rebuild]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
            payload={"tree": tree_id, "actor": actor},
            item_ids=items,
```

New text:

```
            payload={"tree": tree_id, "actor": actor},
```

### `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job`

The rebuild drives another verb's job, without that verb's own resume checks

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R2_rebuild_drives_a_foreign_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_another_verbs_job[rebuild]`

Old text:

```
    if job.handler_key != ctx.entry.handler_key:
        raise refuse(
            "job-unknown",
```

New text:

```
    if False:
        raise refuse(
            "job-unknown",
```

### `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job`

A rebuild queued by an older build drives to succeeded having rebuilt nothing

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R4_rebuild_drives_an_itemless_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_a_job_an_older_build_queued_with_no_items[rebuild]`

Old text:

```
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
```

New text:

```
        if False:
            raise refuse(
                "internal-error",
```

### `u53-zero-rows-remeasured.I6_tree_items_ignores_native`

The rebuild's items include trees the registry says are still on the bridge

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-zero-rows-remeasured.json`, row `I6_tree_items_ignores_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge[rebuild]`

Old text:

```
    native = tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    native = tuple(sorted(entries.tree_ids()))
```

### `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree`

A rebuild of one named tree quietly rebuilds every tree in the library

- File: `src/cratekit/cli/rebuild.py`
- Source: `u53-zero-rows-remeasured.json`, row `I7_tree_items_ignores_the_named_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`

Old text:

```
    if tree_id is None:
        return native
    return tuple(t for t in native if t == tree_id)
```

New text:

```
    return native
```

### `u89.W4_rebuild_worker`

cli/rebuild handle: hand the engine None instead of the loaded cut

- File: `src/cratekit/cli/rebuild.py`
- Source: `u89.json`, row `W4_rebuild_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_worker_driven_without_the_resume_refuses_a_corrupt_calibration`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
        vocal_threshold=None,
```

### `u89.W6_rebuild_resume_loads_first`

cli/rebuild _resume: do not read the cut before driving, so a corrupt calibration fails items instead of refusing

- File: `src/cratekit/cli/rebuild.py`
- Source: `u89.json`, row `W6_rebuild_resume_loads_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_resume_that_drove_nothing_carries_no_vocal_warning[rebuild]`

Old text:

```
        threshold = metadata_cli.load_vocal_threshold(jobs.frozen_config(job))
```

New text:

```
        threshold = 0.0
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

### `r773-b.R1_doctor_check_not_declared`

registry: the verb no longer declares library.paths_resolved

- File: `src/cratekit/cli/registry_later.py`
- Source: `r773-b.json`, row `R1_doctor_check_not_declared`
- Moved: the same text, now in src/cratekit/cli/registry_later.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_verb_declares_one_xml_no_database_surface_and_asks_nothing`

Old text:

```
        doctor_checks=("library.mounted", "rekordbox.closed", "library.paths_resolved"),
```

New text:

```
        doctor_checks=("library.mounted", "rekordbox.closed"),
```

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry_modules.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Moved: the same text, now in src/cratekit/cli/registry_modules.py, was in src/cratekit/cli/registry.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4172 against a baseline of 4176
- Kills: 33 (collect-error)
- Note: collection changed: 4172 collected against a baseline of 4176. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_cli_contract.py::test_a_planned_verb_whose_module_has_landed_must_lose_its_marker`
  - `tests/test_cutover_parity.py::test_the_cutover_is_mechanically_possible_and_says_what_is_left`
  - `tests/test_cutover_parity.py::test_the_parity_table_renders_for_a_person`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_lossy_marked_companion_comes_back_with_a_clean_title`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[empty-anchor]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-name]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-path]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[path-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[tempo-beside-path]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[unowned-no-key]`
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        emits=frozenset({"plan"}), output_schema="plan/1",
        # Landed (U43).
```

New text:

```
        emits=frozenset({"plan"}), output_schema="plan/1",
        planned_in="U35",
        # Landed (U43).
```

### `r770-d.C8_native_gate_answered_inline`

registry: declare intake.file.native as an ordinary gate, answerable on the run that found it

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `r770-d.json`, row `C8_native_gate_answered_inline`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_cli_contract.py`
- Collected: 1053 against a baseline of 1053
- Kills: 6 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_a_failure_past_the_gate_says_what_it_leaves_and_keeps_its_reason_and_remedy`
  - `tests/test_intake_writers_native.py::test_a_file_already_in_the_collection_gains_a_membership_and_no_second_row`
  - `tests/test_intake_writers_native.py::test_a_file_named_through_a_link_is_stored_under_the_configured_root`
  - `tests/test_intake_writers_native.py::test_intake_file_tags_its_row_vox_from_the_files_score`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_the_gate_screen_names_the_row_its_columns_the_playlist_and_the_database`

Old text:

```
                prompt="Add this file to the collection?", explicit=True, digest_source="plan",
```

New text:

```
                prompt="Add this file to the collection?", explicit=False, digest_source="plan",
```

### `u91.G1_registry_xml`

registry route.unplaced: declare no write surface, so doctor and conformance 8 no longer see the xml write

- File: `src/cratekit/cli/registry_pipeline.py`
- Source: `u91.json`, row `G1_registry_xml`
- Moved: the same text, now in src/cratekit/cli/registry_pipeline.py, was in src/cratekit/cli/registry.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`
- Collected: 1217 against a baseline of 1217
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_declares_no_write_and_needs_only_what_a_read_needs`

Old text:

```
        writes=frozenset({"xml"}), taxonomy_terms=("genre_energy",),
```

New text:

```
        taxonomy_terms=("genre_energy",),
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

### `r686.R1_empty_list_bare_header`

An empty collection in a gate's context renders as a bare header again

- File: `src/cratekit/cli/render.py`
- Source: `r686.json`, row `R1_empty_list_bare_header`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`
- Collected: 1217 against a baseline of 1217
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_screen_says_none_for_an_empty_warning_list`

Old text:

```
        if isinstance(value, (Mapping, list, tuple)) and not value:

```

New text:

```
        if False:

```

### `u295.S10_stuck_accepted`

_boot_out: accept an agent still loaded after its bootout

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S10_stuck_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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

### `u295.S7_user_domain`

_domain: load into user/<uid> instead of the person's GUI login

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S7_user_domain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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
- Collected: 1116 against a baseline of 1116
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

### `u154.G16_wizard_default_dropped`

setup records no processed_dir when nothing answers

- File: `src/cratekit/cli/setup.py`
- Source: `u154.json`, row `G16_wizard_default_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_processed_dir.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_processed_dir.py::test_a_clean_machine_records_the_default_when_no_flag_names_one`

Old text:

```
            question="Which folder under the music folder holds filed batches",
            default=config.DEFAULT_PROCESSED_DIR,

```

New text:

```
            question="Which folder under the music folder holds filed batches",
            default="Filed_Elsewhere",

```

### `u283.S10_any_raise_escapes`

_link_discogs: the bare except catches only arithmetic errors, so a check raising anything else escapes setup after the configuration is saved

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S10_any_raise_escapes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 2 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_check_that_raises_anything_else_stores_nothing_and_is_a_note`
  - `tests/test_setup_discogs.py::test_an_exception_carrying_the_token_never_reaches_the_note`

Old text:

```
        except Exception as exc:  # noqa: BLE001
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"the token could not be checked ({type(exc).__name__}), so it was "
```

New text:

```
        except ArithmeticError as exc:  # noqa: BLE001
            wizard.note(
                key,
                title,
                doctor.Status.FAIL,
                f"the token could not be checked ({type(exc).__name__}), so it was "
```

### `u283.S11_vocabulary_never_noted`

_discogs_vocabulary: never notes a copy without the Discogs table

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S11_vocabulary_never_noted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 2 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_copy_without_the_discogs_table_is_pointed_to_taxonomy_upgrade`
  - `tests/test_setup_discogs.py::test_an_already_linked_copy_without_the_table_is_pointed_there_too`

Old text:

```
    if searchers.DISCOGS not in found.missing_vocabularies:
        return
```

New text:

```
    if True:
        return
```

### `u283.S12_vocabulary_always_noted`

_discogs_vocabulary: notes every copy, the table present or not

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S12_vocabulary_always_noted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_copy_with_the_table_or_no_copy_gets_no_such_note`

Old text:

```
    if searchers.DISCOGS not in found.missing_vocabularies:
        return
```

New text:

```
    if False:
        return
```

### `u283.S13_linked_copy_not_checked`

_link_discogs: a token already recorded does not look at the copy's Discogs table

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S13_linked_copy_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 1 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_an_already_linked_copy_without_the_table_is_pointed_there_too`

Old text:

```
                f"as it is; crate setup {RELINK_FLAG} offers to replace it"
            ),
        )
        _discogs_vocabulary(wizard, cfg)
```

New text:

```
                f"as it is; crate setup {RELINK_FLAG} offers to replace it"
            ),
        )
```

### `u283.S17_verb_skips_step`

setup: the verb no longer runs the Discogs step

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S17_verb_skips_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 4 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_the_verb_hands_the_flag_to_the_step`
  - `tests/test_setup_discogs.py::test_the_verb_links_discogs_through_the_shipped_client`
  - `tests/test_setup_discogs.py::test_the_verb_refuses_a_rejected_token_and_stores_nothing`
  - `tests/test_setup_discogs.py::test_the_verb_without_the_flag_leaves_a_recorded_token`

Old text:

```
    _link_discogs(wizard, cfg, relink=bool(args.relink_discogs))
```

New text:

```
    pass
```

### `u283.S4_recorded_never_acknowledged`

_link_discogs: a recorded token is not acknowledged, so every run asks for it again and may replace it

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S4_recorded_never_acknowledged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 3 (killed)
- Killed:
  - `tests/test_setup_discogs.py::test_a_recorded_token_is_acknowledged_with_no_question_and_no_request`
  - `tests/test_setup_discogs.py::test_an_already_linked_copy_without_the_table_is_pointed_there_too`
  - `tests/test_setup_discogs.py::test_the_verb_without_the_flag_leaves_a_recorded_token`

Old text:

```
    if already and not relink:
```

New text:

```
    if False:
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

### `r1115.S1_sync_land_stops_on_unsettled`

sync land _download: carry on over a download that did not settle, so a transient failure lands the rest

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1115.json`, row `S1_sync_land_stops_on_unsettled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_crate_sync_skill.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_parked_download_ends_the_pass_blocked_before_the_tail`
  - `tests/test_sync_land.py::test_a_transient_download_failure_ends_the_pass_and_lands_nothing`

Old text:

```
    if not read.settled:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
```

New text:

```
    if False:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
```

### `r1115.S2_sync_land_names_the_refused`

sync land _download: report no refused track

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1115.json`, row `S2_sync_land_names_the_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_crate_sync_skill.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_one_lossy_refusal_among_eight_downloads_lands_seven_and_reports_one`

Old text:

```
    refused = [dict(row) for row in read.refused]
```

New text:

```
    refused = []
```

### `r1499.S01_download_reading`

sync land: the reading before the download never refuses, so a pass downloads beside a go's download at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S01_download_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`
  - `tests/test_sync_land_beside.py::test_a_label_gos_download_at_its_landings_gate_renamed_refuses_the_pass_before_it_downloads`
  - `tests/test_sync_land_beside.py::test_a_pass_whose_landing_is_proven_is_not_named`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == DOWNLOAD:
        return settled

```

### `r1499.S02_tail_reading`

sync land: the reading before the tail never refuses, so a download finished during the pass's download is tailed and landed with it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S02_tail_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_gos_download_arriving_while_the_pass_downloads_refuses_its_tail`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == TAG:
        return settled

```

### `r1499.S03_arrival_after_tail`

sync land: no check after name apply, so a download finished during the tail is renamed and planned into the landing

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S03_arrival_after_tail`
- Moved: Anchored where u303-replay-after-c.json replayed it: U303 shortened the comment under the check to a sentence; the arrival check after the name apply, the guard this row disables, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
            if changed is not None:
                # Not continued, since no record was kept; the steps name the landing.
```

New text:

```
            if False:
                # Not continued, since no record was kept; the steps name the landing.
```

### `r1499.S04_arrival_after_plan`

sync land: a landing planned over an arrival is handed on at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S04_arrival_after_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`

Old text:

```
                changed = _arrived(cfg, staging, name, before)
                if changed is None:
                    raise

```

New text:

```
                changed = None
                if changed is None:
                    raise

```

### `r1499.S05_keep_after_arrival`

_keep: keep the record although something arrived, so the arrival reads as the pass's own on its next run

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S05_keep_after_arrival`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if why is not None:
        report.warnings.append(
```

New text:

```
    if False:
        report.warnings.append(
```

### `r1499.S06_keep_called`

sync land: keep no record at the tail's stop, so the pass continued refuses beside its own renamed tracks

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S06_keep_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`
  - `tests/test_sync_land_beside.py::test_the_record_is_kept_under_the_pass_at_each_tail_stop`

Old text:

```
            _keep(report, cfg, staging, name, before)
```

New text:

```
            pass
```

### `r1499.S07_kept_read`

_alone: read no kept record, so the pass's own renamed tracks are beside it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S07_kept_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`

Old text:

```
                kept=staged.kept(staged.pass_record(cfg, name)),
```

New text:

```
                kept=frozenset(),
```

### `r1499.S08_own_pass_proof`

_alone: never read the pass's landing proof, so a landed pass's record still reads files as its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S08_own_pass_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`

Old text:

```
                own_pass=name,
                origin=_ORIGIN,
```

New text:

```
                own_pass=None,
                origin=_ORIGIN,
```

### `r1499.S09_own_library`

_own_downloads: a download of another library over the pass's list is its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S09_own_library`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name`

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name
```

### `r1499.S10_own_by_list`

_own_downloads: no download is the pass's own, so its own fresh tracks refuse it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S10_own_by_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 66 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_job_command_that_stops_at_a_gate_is_that_commands_gate`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - ... and 51 more, see the JSON sidecar

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name + '-' and job.library_id == cfg.library.volume_id
```

### `r1499.S11_unreadable_refuses`

_alone: a refusal of the reading (an unlistable folder, an unreadable root) reads as nothing beside

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S11_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`

Old text:

```
    except CratekitError as exc:
        raise _Stop(step, exc) from None
    except OSError
```

New text:

```
    except CratekitError:
        return staged.Settled(frozenset(), 0)
    except OSError
```

### `r1499.S12_warnings_in_refusal`

_with_warnings: a refusal drops the pass's warnings

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S12_warnings_in_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if report.warnings:
        data["warnings"]
```

New text:

```
    if False:
        data["warnings"]
```

### `r1499.S13_own_unnamed_step`

_own_unnamed: never name the landing under the pass for files no download names

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S13_own_unnamed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 325 against a baseline of 325
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`

Old text:

```
    if not (found.unnamed and own):
        return ()
```

New text:

```
    if True:
        return ()
```

### `u152.R13_missing_lift`

_missing: carry none of the listing's failing rows

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R13_missing_lift`
- Moved: Anchored where u303-replay-merged5.json replayed it: U303 shortened the comment above the call to one line; the lift of the listing's failing rows in _missing, the guard this row removes, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`

Old text:

```
    # The listing's failing rows ride through, so an unnameable track is said.
    _lift_failed_checks(report, envelope)

```

New text:

```
    # The listing's failing rows ride through, so an unnameable track is said.

```

### `u152.R14_download_list_match`

_download_job: drop the list match, so another list's download job is read as the pass's

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R14_download_list_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`

Old text:

```
            and str((job.payload or {}).get(acquire_cli.LIST) or "") == wanted

```

New text:

```
(empty)
```

### `u152.R15_download_newest`

_download_job: read the oldest job over the list, the round two defect

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R15_download_newest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
    for job in jobs.list_jobs(store):
        if (
            job.handler_key == key
```

New text:

```
    for job in reversed(jobs.list_jobs(store)):
        if (
            job.handler_key == key
```

### `u152.R16_download_cancelled`

_download_job: read a cancelled download as the pass's claim on the list

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R16_download_cancelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`

Old text:

```
            and job.state is not jobs.JobState.CANCELLED

```

New text:

```
(empty)
```

### `u152.R17_download_retry`

_download: never retry a download that failed transiently, so a continued pass reads it as settled

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R17_download_retry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`

Old text:

```
            job = jobs.retry(store, job.job_id)
```

New text:

```
            pass
```

### `u152.R20_nothing_downloaded`

_download: go on to the tail when the download landed nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R20_nothing_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_every_download_refused_lands_nothing_on_a_failing_row`
  - `tests/test_sync_land.py::test_the_newest_download_over_the_list_is_the_one_the_pass_reads`

Old text:

```
    if not done:
        report.check(
```

New text:

```
    if False:
        report.check(
```

### `u152.R2_preflight_backup`

_preflight: drop the backup driver check, so a pass runs beside a live backup

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R2_preflight_backup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_running_backup_refuses_before_any_write`

Old text:

```
        try:
            jobs.assert_free(job.job_id)
        except jobs.DriverHeld as exc:
```

New text:

```
        try:
            pass
        except jobs.DriverHeld as exc:
```

### `u152.R6_lift_failed_checks`

_lift_failed_checks: carry no step's failing row, so the withheld hearts and the unnameable tracks are said nowhere

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R6_lift_failed_checks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_listing_with_nothing_nameable_says_so_and_carries_its_failing_row`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
        if check.get("key") in held:
            continue
        report.checks.append(dict(check))
```

New text:

```
        if check.get("key") in held:
            continue
```

### `u152.R7_outbound_held`

_lift_failed_checks: lift the unasked outbound write's refusal as a FAIL row on every pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R7_outbound_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`
  - `tests/test_sync_land.py::test_the_outbound_hearts_write_stays_behind_its_own_gate`

Old text:

```
        if check.get("key") in held:
            continue

```

New text:

```
(empty)
```

### `u152.R8_continue_open_pass`

_sync: never continue the one earlier pass sync all left out, so a hand typed pass ends no_op

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R8_continue_open_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`

Old text:

```
        if len(earlier) == 1:
```

New text:

```
        if False:
```

### `u152.R9_open_passes_library`

_open_intake: drop the library filter, so another library's open pass is continued

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R9_open_passes_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1207 against a baseline of 1207
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_that_ended_or_belongs_to_another_library_is_not_continued`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
            and job.library_id == cfg.library.volume_id
        ]


def _run_of
```

New text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
        ]


def _run_of
```

### `u179.P1_shared_preflight`

preflight: drop the rekordbox check, so sync bandcamp plans and fetches with rekordbox open

- File: `src/cratekit/cli/sync_land.py`
- Source: `u179.json`, row `P1_shared_preflight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_land.py`
- Collected: 104 against a baseline of 104
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_rekordbox_running_refuses_before_the_plan`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_rekordbox_running_refuses_before_any_write`

Old text:

```
    rb_writer.assert_rekordbox_closed(verb)
```

New text:

```
    pass
```

### `u181.S1_profile_off_asked`

sync land _vocals: ask the model on a profile with the vocals module off

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S1_profile_off_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_profile_with_the_vocals_module_off_is_not_asked`

Old text:

```
    if not tail.vocals_on(cfg):
        report.summary["vocal_scoring"] = "off"
```

New text:

```
    if False:
        report.summary["vocal_scoring"] = "off"
```

### `u181.S2_gate_never_asked`

sync land _vocals: never stop at the gate, so a pass lands rows with no score unasked

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S2_gate_never_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 6 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.land]`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_cannot_score_stops_at_its_gate_before_queueing_anything`
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`
  - `tests/test_sync_land.py::test_the_answered_gate_takes_the_pass_on_and_the_summary_says_vocals_were_skipped`
  - `tests/test_sync_land.py::test_the_gate_recorded_by_a_separate_act_continues_the_same_run`

Old text:

```
    unable = tail.vocals_unavailable()
    if unable is None:
```

New text:

```
    unable = tail.vocals_unavailable()
    if True:
```

### `u181.S3_stop_goes_on`

sync land _vocals: an answer of stop takes the pass on

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S3_stop_goes_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_answering_stop_refuses_with_the_command_that_mends_it`

Old text:

```
    if option != WITHOUT_VOCALS_GO:
```

New text:

```
    if option is None:
```

### `u182.M18_left_open_taken`

_left_behind: name the pass's own jobs on the left open row too

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M18_left_open_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_the_hearts_the_provider_withholds_are_reported_once_and_not_retried`

Old text:

```
    left = [hold for hold in holds if not taken or _run_of(hold.job) != taken]
```

New text:

```
    left = list(holds)
```

### `u182.M19_left_open_identity`

_left_behind: group by the label alone, so a typed URL and a sweep's id are two playlists

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M19_left_open_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`

Old text:

```
        grouped.setdefault(hold.identity or hold.label(), []).append(hold)
```

New text:

```
        grouped.setdefault(hold.label(), []).append(hold)
```

### `u182.M20_cancelled_driven`

_intake: drive cancelled jobs with the rest, so a continued pass stops on a cancelled job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M20_cancelled_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
    live = [job for job in found if job.state is not jobs.JobState.CANCELLED]
```

New text:

```
    live = list(found)
```

### `u182.M21_all_cancelled_done`

_intake: go on when every job was cancelled, so the listing refuses a pass with nothing resolved

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M21_all_cancelled_done`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`

Old text:

```
        if not live:
            report.check(
```

New text:

```
        if False:
            report.check(
```

### `u182.M22_skip_failed`

_missing: list without --skip-failed, so a pass with a cancelled copy stops at the listing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u182.json`, row `M22_skip_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`

Old text:

```
        argv.append("--skip-failed")
```

New text:

```
        pass
```

### `u183.M11_land_runs_named`

_unknown_pass: name no land run beside a recent pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M11_land_runs_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    lands = _land_runs_of(passes)
```

New text:

```
    lands: dict[str, str] = {}
```

### `u183.M12_preflight_way_back`

_preflight: a rekordbox or backup refusal no longer ends with the command that comes back

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M12_preflight_way_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`

Old text:

```
        raise tail.with_steps(exc, f"then run it again: {again}") from None
```

New text:

```
        raise
```

### `u183.M14_retryable_intake_continues`

_intake: a retryable ended intake job stops as one that cannot continue, so its way on ends at the resume

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M14_retryable_intake_continues`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`

Old text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry))
```

New text:

```
                raise _Stop(INTAKE, tail.with_steps(error, retry), continues=False)
```

### `u183.M15_continue_command_words`

_continue_command: drop the flag, so every printed continuation starts a new pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M15_continue_command_words`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_an_earlier_pass_left_open_beside_a_new_one_is_named_with_its_way_on`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_an_unknown_id_refuses_before_any_step_and_names_the_recent_passes`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_two_earlier_passes_holding_open_jobs_are_a_choice_named_not_made`

Old text:

```
    return f"crate sync land --pass-run {pass_run}"
```

New text:

```
    return f"crate sync land {pass_run}"
```

### `u183.M1_pass_run_as_given`

_resolve: never take the given id as a pass run, so a pass id is looked up as a land record and refused

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M1_pass_run_as_given`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_is_told_the_answer_that_continues_it`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_continued_pass_whose_every_job_was_cancelled_names_a_new_pass_not_a_resume`
  - `tests/test_sync_land.py::test_a_job_another_driver_holds_ends_the_pass_with_that_drivers_refusal`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_url_typed_by_hand_and_a_sweeps_id_are_one_playlist_on_the_left_open_row`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_failed_names_its_retry_not_a_continuation`
  - `tests/test_sync_land.py::test_an_intake_job_that_ended_retryable_ends_its_way_on_with_the_continuation`
  - `tests/test_sync_land.py::test_the_continue_command_a_failed_step_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_continue_command_a_pending_stop_prints_works_when_pasted`
  - `tests/test_sync_land.py::test_the_left_open_row_names_each_playlist_its_age_size_and_copies`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if _pass_jobs(store, given, cfg):
            return given
```

New text:

```
        if False:
            return given
```

### `u183.M2_land_record_resolves`

_resolve: ignore the land run's recorded pass, so the land run's own id is refused as it was before U183

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M2_land_record_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if recorded:
```

New text:

```
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if False:
```

### `u183.M3_recorded_pass_needs_a_job`

_resolve: take a land run's recorded pass with no intake job of this library, so the pass fails at the fourth step again

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M3_recorded_pass_needs_a_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_land_run_whose_pass_no_intake_job_carries_is_refused_not_continued`

Old text:

```
            if _pass_jobs(store, recorded, cfg):
                report.check(
```

New text:

```
            if True:
                report.check(
```

### `u183.M6_unreadable_record`

_land_record: let a record that cannot be read raise out of the resolver

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M6_unreadable_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
    except (CratekitError, AttributeError, KeyError, TypeError, ValueError, OSError):
        return None
    return state if
```

New text:

```
    except KeyError:
        return None
    return state if
```

### `u183.M7_remember_saves`

_remember: record the pass on the run without saving, so a run that stops before the dispatcher saves keeps nothing

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M7_remember_saves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`

Old text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
    gates.save(ctx.run)
```

New text:

```
    ctx.run.related_runs[PASS_ROLE] = pass_run
```

### `u183.M8_remember_called`

sync_land: never record the pass on the land run

- File: `src/cratekit/cli/sync_land.py`
- Source: `u183.json`, row `M8_remember_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
        if run_id:
            _remember(ctx, report, run_id)
```

New text:

```
        if False:
            _remember(ctx, report, run_id)
```

### `u212.S1_missing_ends`

sync_land._missing: nothing listed ends the pass whatever is staged

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S1_missing_ends`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 330 against a baseline of 330
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`

Old text:

```
    if (envelope.get("outcome") == str(Outcome.NO_OP) or not listed) and not staged:
```

New text:

```
    if envelope.get("outcome") == str(Outcome.NO_OP) or not listed:
```

### `u212.S4_staged_said`

sync_land._missing: the missing row drops the staged clause, so the pass does not say how many it skipped

- File: `src/cratekit/cli/sync_land.py`
- Source: `u212.json`, row `S4_staged_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_crate_sync_skill.py`, `tests/test_inbox_analyzed.py`, `tests/test_rekordbox_visit_skill.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`
- Collected: 330 against a baseline of 330
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
        + (f"; {staged} more {held}" if staged else ""),
```

New text:

```
        + "",
```

### `u227.R15_way_on_wording`

_way_on: name a mirror download as queued by hand, to be driven outside a pass (round one's S12)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R15_way_on_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif False:
```

### `u227.R19_take_library`

_take_mirror_downloads: take another library's mirror job

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R19_take_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_another_library_queued_is_not_taken`

Old text:

```
                or job.library_id != cfg.library.volume_id

```

New text:

```
(empty)
```

### `u227.R20_take_source`

_mirror_download: any intake.playlist job is a mirror download, a hand queued one included

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R20_take_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land.py::test_an_intake_job_queued_by_hand_with_no_pass_is_named_not_passed_over`
  - `tests/test_sync_land_mirror_downloads.py::test_a_hand_queued_playlist_job_and_a_cancelled_mirror_job_are_not_taken`

Old text:

```
        and (job.payload or {}).get("source_id") == mirror_downloads.SOURCE_ID

```

New text:

```
(empty)
```

### `u227.R21_take_continued`

sync_land: take mirror jobs into a continued earlier pass

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R21_take_continued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_continuing_an_earlier_one_over_nothing_new_takes_none`

Old text:

```
            if fresh and run_id in (None, fresh) and _take_mirror_downloads(report, cfg, fresh):
```

New text:

```
            if fresh and _take_mirror_downloads(report, cfg, run_id or fresh):
```

### `u227.R22_take_not_driven`

sync_land: give the jobs the run but keep driving the pass sync all named nothing for

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R22_take_not_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_pass_whose_sync_all_queued_nothing_takes_the_mirror_download`

Old text:

```
                run_id = fresh
                report.summary["pass_run"] = fresh
```

New text:

```
                pass
```

### `u227.R25_way_on_state`

_way_on: name a blocked mirror download as the next pass's, which takes queued jobs only (round two's R3)

- File: `src/cratekit/cli/sync_land.py`
- Source: `u227.json`, row `R25_way_on_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_land_mirror_downloads.py`, `tests/test_sync_land_staged.py`
- Collected: 96 against a baseline of 96
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_mirror_downloads.py::test_a_mirror_download_a_pass_cannot_take_keeps_the_command_that_settles_it`

Old text:

```
    elif _mirror_download(job) and job.state is jobs.JobState.QUEUED:
```

New text:

```
    elif _mirror_download(job):
```

### `u293.S3_sync_land_holds`

sync_land: a pass by hand takes no staging lock

- File: `src/cratekit/cli/sync_land.py`
- Source: `u293.json`, row `S3_sync_land_holds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_sync_land_beside.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`

Old text:

```
    with staging_lock.held("crate sync land", run_id=ctx.run.run_id):
```

New text:

```
    if True:
```

### `u293.N1_no_answer`

_no_answer: an answer or a raised line given to the night is taken

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N1_no_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv0]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv1]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv2]`
  - `tests/test_sync_night.py::test_an_answer_or_a_raised_line_given_to_the_night_refuses_before_anything[argv3]`

Old text:

```
    if given:
```

New text:

```
    if False:
```

### `u293.N2_rekordbox_refused`

sync_night: the night runs beside rekordbox or its agent

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N2_rekordbox_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_night_writes_its_record_even_when_its_line_cannot_be_kept`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running0]`
  - `tests/test_sync_night.py::test_rekordbox_or_its_agent_up_refuses_before_any_call[running1]`

Old text:

```
            rb_writer.assert_rekordbox_closed("crate sync night")
```

New text:

```
            pass
```

### `u293.N3_live_job_refused`

sync_night: the night runs beside a job with a live driver

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N3_live_job_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_job_with_a_live_driver_refuses_before_any_call`

Old text:

```
            _no_live_job()
            pass_run
```

New text:

```
            pass_run
```

### `u293.N4_occupied_refused`

sync_night: a new pass runs beside what the staging folder holds

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N4_occupied_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_staging_folder_holding_what_a_landing_takes_refuses_a_new_pass`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
                _nothing_waits(cfg, last)
```

New text:

```
                pass
```

### `u293.N5_owed_kept`

_refused: a refusal writes a fresh record over a pass still owed

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N5_owed_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_the_next_night_continues`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_an_answered_gate_over_tracks_still_staged_stays_owed`

Old text:

```
    if _owed(last) and last is not None:
```

New text:

```
    if False:
```

### `u293.N6_settled_by_landing`

settle: the pass's own landing never ends a wait, so a landed pass reads as waiting

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N6_settled_by_landing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landed_pass_reads_settled_everywhere_whatever_is_staged_since`

Old text:

```
    if _landed(cfg, record.get("land_name")):
```

New text:

```
    if False:
```

### `u293.N7_unread_landing_is_not_settled`

_landed: a landing log that cannot be read is read as landed, so a waiting pass reads settled

- File: `src/cratekit/cli/sync_night.py`
- Source: `u293.json`, row `N7_unread_landing_is_not_settled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_night.py`, `tests/test_crate_sync_skill.py`, `tests/test_cli_contract.py`
- Collected: 1091 against a baseline of 1091
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_night.py::test_a_landing_that_cannot_be_read_settles_nothing`

Old text:

```
    except (CratekitError, OSError):
        return None
```

New text:

```
    except (CratekitError, OSError):
        return True
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
- Collected: 217 against a baseline of 217
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
- Collected: 217 against a baseline of 217
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
- Collected: 36 against a baseline of 36
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
- Collected: 36 against a baseline of 36
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 276 against a baseline of 276
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
- Collected: 1638 against a baseline of 1638
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
- Collected: 1638 against a baseline of 1638
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
- Collected: 1638 against a baseline of 1638
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
- Collected: 1638 against a baseline of 1638
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
- Collected: 1638 against a baseline of 1638
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
- Collected: 1028 against a baseline of 1028
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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
- Collected: 1739 against a baseline of 1739
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

### `u132.V5_nothing`

A plan that writes nothing still asks the gate

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V5_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_what_is_held_is_said_and_written_around`

Old text:

```
    if not found.writes:

```

New text:

```
    if False:

```

### `u133-a.P12_verb_warning`

The verb drops the keyword rule warning

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u133-a.json`, row `P12_verb_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
    ] + [{"code": KEYWORD_RULE, "message": sentence} for sentence in found.keywords]

```

New text:

```
    ]

```

### `u194.W24_write_copy_bytes_stale`

write_copy: drop the byte check after the second plan, so an edit made since is written over

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W24_write_copy_bytes_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 119 against a baseline of 119
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_an_edit_after_the_second_plan_is_refused_as_stale`

Old text:

```
    if as_read(raw) != before:
```

New text:

```
    if False:
```

### `u194.W25_write_copy_read_back`

write_copy: drop the read back, so a copy that does not load is left as every verb's declaration

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u194.json`, row `W25_write_copy_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 119 against a baseline of 119
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_copy_that_does_not_read_back_is_replaced_by_the_one_it_replaced`
  - `tests/test_taxonomy_upgrade.py::test_a_restore_that_fails_says_so_and_names_the_backup`

Old text:

```
    problem = _read_back(cfg, path, written)
    if problem is not None:
```

New text:

```
    problem = _read_back(cfg, path, written)
    if False:
```

### `r1184.M17_verb_takes_step`

taxonomy alias verb: ignore the refusal's own step, so the bare folder and own name refusals say leave the word

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M17_verb_takes_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 3 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_carrying_a_folders_own_name_is_never_retagged`
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_its_folder_cannot_take_is_refused_with_its_step`
  - `tests/test_taxonomy_word.py::test_the_bare_folder_refusal_names_the_folder_verb_as_its_step`

Old text:

```
    if exc.step:

```

New text:

```
    if False:

```

### `r1184.M18_verb_nothing_to_do`

taxonomy alias verb: the no change sentence for an own name claims a tagging alias

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `r1184.json`, row `M18_verb_nothing_to_do`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folders_own_name_in_another_case_is_retagged_to_the_exact_name`

Old text:

```
                        if edit.own_name

```

New text:

```
                        if False

```

### `u194.W18_carrying_several_genres`

carrying: plan a write for a file carrying the word beside another genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W18_carrying_several_genres`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_with_two_genres_is_left_and_named`

Old text:

```
        current = _JOINED.join(values)
        if len(values) == 1:
```

New text:

```
        current = _JOINED.join(values)
        if True:
```

### `u194.W19_carrying_unread`

carrying: read a file whose genre could not be read as one carrying no genre

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W19_carrying_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_whose_genre_cannot_be_read_is_named_and_never_called_clean`
  - `tests/test_taxonomy_word.py::test_nothing_to_do_does_not_claim_a_file_it_could_not_read`

Old text:

```
        if values is None:
            items.append(FileItem(path=path, relative=relative, change=UNREAD))
            continue
```

New text:

```
        if values is None:
            continue
```

### `u194.W20_retag_reread`

_retag: drop the read before the write, so a file changed since the second plan is written over

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W20_retag_reread`
- Moved: Same read before the write in _retag; U298 replaced the local _genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_changed_after_the_second_plan_is_left_and_named`

Old text:

```
        if file_genres(item.path) != (item.current,):
            done.moved.append(item)
```

New text:

```
        if False:
            done.moved.append(item)
```

### `u194.W21_retag_read_back`

_retag: drop the read back, so a write that did not take is counted as retagged

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W21_retag_read_back`
- Moved: Same read back in _retag; U298 replaced the local _genres with tagging.tag.file_genres, the identical exact reader
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_write_that_does_not_read_back_is_named_apart_from_one_never_made`

Old text:

```
        if file_genres(item.path) != (display,):
            done.wrong.append(item)
```

New text:

```
        if False:
            done.wrong.append(item)
```

### `u194.W22_unwritten_refusal`

alias verb: leave a file the writer could not write out of the refusal, so the run reports success

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W22_unwritten_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_file_that_will_not_take_the_genre_is_named_and_the_rerun_finishes`

Old text:

```
    if done.moved or done.failed or done.wrong:
```

New text:

```
    if done.moved or done.wrong:
```

### `u194.W23_root_missing`

_root: drop the refusal of a folder that is not there, so the walk plans nothing and reads clean

- File: `src/cratekit/cli/verbs/taxonomy_word.py`
- Source: `u194.json`, row `W23_root_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_word.py`
- Collected: 68 against a baseline of 68
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_word.py::test_a_folder_that_is_not_there_is_refused_with_nothing_written`

Old text:

```
    if not root.is_dir():
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

New text:

```
    if False:
        raise refuse(
            "source-missing",
            f"{root} is not a folder, so there are no files to retag; nothing was written",
```

### `u331.S15_foreign_reexport_keeps_every_row`

active_taxonomy.outside_foreign: the re-export the favourites home and the pair discovery call is replaced by one that keeps every row, so a playlist inside another app's folder counts as the Favorites home

- File: `src/cratekit/core/active_taxonomy.py`
- Source: `u331.json`, row `S15_foreign_reexport_keeps_every_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_placement.py`, `tests/test_sync_pair_discover.py`, `tests/test_import_rules.py`
- Collected: 170 against a baseline of 170
- Kills: 2 (killed)
- Killed:
  - `tests/test_favorites_placement.py::test_a_playlist_of_the_sources_name_inside_deadca7s_folder_is_not_a_second_source`
  - `tests/test_sync_pair_discover.py::test_a_favourites_name_inside_another_apps_folder_does_not_unsettle_the_home`

Old text:

```
from cratekit.core.foreign_tree import outside as outside_foreign

```

New text:

```

def outside_foreign(rows, _every):
    return list(rows)


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

### `u84-a.A10_native_resolution`

The repair re-encodes to the 800 square new art edge, which upscales a 320 by 200 cover and stretches it

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A10_native_resolution`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`
  - `tests/test_tagging_engine.py::test_a_png_in_a_filled_block_is_re_encoded_as_a_baseline_jpeg`
  - `tests/test_tagging_engine.py::test_a_progressive_jpeg_with_sound_dimensions_becomes_baseline`
  - `tests/test_tagging_engine.py::test_a_sound_block_beside_a_broken_one_is_kept_as_it_was_and_in_order`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_a_vendored_zeroed_block_ends_with_real_dimensions_and_the_same_image`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims0]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims1]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims2]`

Old text:

```
        return to_cdj_jpeg(data, size=None), False
```

New text:

```
        return to_cdj_jpeg(data, size=ART_SIZE), False
```

### `u84-a.A11_dimensions_from_new_bytes`

The repaired block's width, height and depth are not written, so the zeroes stay

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A11_dimensions_from_new_bytes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 10 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`
  - `tests/test_tagging_engine.py::test_a_sound_block_beside_a_broken_one_is_kept_as_it_was_and_in_order`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_a_vendored_zeroed_block_ends_with_real_dimensions_and_the_same_image`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims0]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims1]`
  - `tests/test_tagging_engine.py::test_any_one_zeroed_dimension_is_broken[dims2]`

Old text:

```
            block.width, block.height, block.depth = cdj.width, cdj.height, cdj.depth
```

New text:

```
            pass
```

### `u84-a.A12_all_or_nothing`

A block that cannot be repaired is passed over and the rest are saved and reported fixed

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A12_all_or_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 6 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_corrupt_image_reports_an_error_and_the_genre_flow_still_proceeds`
  - `tests/test_tagging_engine.py::test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged`
  - `tests/test_tagging_engine.py::test_an_encoder_failure_that_is_not_an_art_error_is_still_an_error`
  - `tests/test_tagging_engine.py::test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok[not-an-image]`
  - `tests/test_tagging_engine.py::test_an_undecodable_image_in_a_filled_block_is_an_error_not_ok[truncated-jpeg]`
  - `tests/test_tagging_engine.py::test_one_unrepairable_block_leaves_every_block_as_it_was`

Old text:

```
        return ArtRepair(REPAIR_ERROR, f"a picture could not be repaired: {exc}")
```

New text:

```
        log.debug("a picture could not be repaired: %s", exc)
```

### `u84-a.A8_no_picture_is_none`

A file with no picture reports ok rather than none

- File: `src/cratekit/core/art.py`
- Source: `u84-a.json`, row `A8_no_picture_is_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_art_repair_reaches_the_artifact_and_the_summary_counts_every_status`
  - `tests/test_tagging_engine.py::test_a_file_with_no_picture_reports_none_and_is_not_written`

Old text:

```
    if not blocks:
        return ArtRepair(REPAIR_NONE)
```

New text:

```
    if False:
        return ArtRepair(REPAIR_NONE)
```

### `u84-b.A16_shrink_fallback`

A picture over the cap at native size is refused again, the review's finding, leaving it blank

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A16_shrink_fallback`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged`
  - `tests/test_tagging_engine.py::test_a_picture_too_large_for_the_cap_at_native_size_is_shrunk_not_left_blank`

Old text:

```
        if _measure(data) is None:
            raise
```

New text:

```
        raise
```

### `u84-b.A17_too_small_to_shrink`

The guard that refuses to shrink a picture already inside the box is removed

- File: `src/cratekit/core/art.py`
- Source: `u84-b.json`, row `A17_too_small_to_shrink`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_art.py`
- Collected: 245 against a baseline of 245
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_inside_the_box_that_cannot_fit_is_an_error_and_is_never_enlarged`

Old text:

```
    if max(img.size) <= ART_SIZE:
```

New text:

```
    if max(img.size) < 0:
```

### `r1103.C1_exit_code`

cause.REASONS: tag-retag-unwritten exits USAGE, the parser's status, rather than PRECONDITION

- File: `src/cratekit/core/cause.py`
- Source: `r1103.json`, row `C1_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_reserved_causes.py`, `tests/test_genre_retag.py`
- Collected: 381 against a baseline of 381
- Kills: 2 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`

Old text:

```
        "tag-retag-unwritten": ExitCode.PRECONDITION,
```

New text:

```
        "tag-retag-unwritten": ExitCode.USAGE,
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

### `r388-c.M14_status_registration_dropped`

Remove the slug from core.cause REASONS, the P5 registration beside the reservation

- File: `src/cratekit/core/cause.py`
- Source: `r388-c.json`, row `M14_status_registration_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_listing.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_discovery.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_listdoc.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_uncredited_tombstone.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8192 against a baseline of 8192
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "snapshot-listing-failed": ExitCode.PRECONDITION,

```

New text:

```
(empty)
```

### `r388-c.M15_status_code_disagrees`

Register the slug in core.cause at a code the reservation does not hold

- File: `src/cratekit/core/cause.py`
- Source: `r388-c.json`, row `M15_status_code_disagrees`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_listing.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_discovery.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_listdoc.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_uncredited_tombstone.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8192 against a baseline of 8192
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_where_this_table_and_the_closed_reason_registry_overlap_they_agree`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "snapshot-listing-failed": ExitCode.PRECONDITION,
```

New text:

```
        "snapshot-listing-failed": ExitCode.LIBRARY_UNAVAILABLE,
```

### `u138.E2_reason_exit_code`

The new refusal maps to another exit code than the acknowledgment's

- File: `src/cratekit/core/cause.py`
- Source: `u138.json`, row `E2_reason_exit_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
        "backup-acknowledgment-backup-too-old": ExitCode.ACK_REQUIRED,

```

New text:

```
        "backup-acknowledgment-backup-too-old": ExitCode.DECISION_REQUIRED,

```

### `u27-restore-cli-author.R3_a_backup_slug_leaves_the_cause_vocabulary`

Remove one refusal from cause.REASONS, so building its cause raises

- File: `src/cratekit/core/cause.py`
- Source: `u27-restore-cli-author.json`, row `R3_a_backup_slug_leaves_the_cause_vocabulary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 242 against a baseline of 242
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_arrives_as_a_cause_and_not_as_a_bare_exception`
  - `tests/test_restore_cli.py::test_an_off_machine_refusal_carries_the_reserved_remediation_and_not_the_class_default`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "remote-not-configured": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u27-restore-cli-author.R4_a_backup_slug_takes_the_wrong_status`

Give one refusal a status the reservation table does not give it

- File: `src/cratekit/core/cause.py`
- Source: `u27-restore-cli-author.json`, row `R4_a_backup_slug_takes_the_wrong_status`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 148 against a baseline of 148
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "no-snapshot-available": ExitCode.PRECONDITION,
```

New text:

```
        "no-snapshot-available": ExitCode.INTERNAL,
```

### `u27-restore-cli-independent.I_G1_a_second_backup_slug_takes_the_wrong_status`

Give an unconfirmed restore a hard failure status the reservation table does not give it, a different member from the author's row so the derived guard is shown to cover the enum rather than one entry

- File: `src/cratekit/core/cause.py`
- Source: `u27-restore-cli-independent.json`, row `I_G1_a_second_backup_slug_takes_the_wrong_status`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_reserved_causes.py`, `tests/test_restore_cli.py`
- Collected: 471 against a baseline of 471
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_where_this_table_and_the_closed_reason_registry_overlap_they_agree`
  - `tests/test_write_session.py::test_every_backup_refusal_carries_one_code_in_both_cause_tables`

Old text:

```
        "restore-not-confirmed": ExitCode.DECISION_REQUIRED,
```

New text:

```
        "restore-not-confirmed": ExitCode.PRECONDITION,
```

### `u43-author-light.R2_undeclared_refusal_slug`

setbuild-anchor-not-indexed leaves cause.REASONS, so refuse raises UnknownReason at the boundary instead of refusing

- File: `src/cratekit/core/cause.py`
- Source: `u43-author-light.json`, row `R2_undeclared_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5370 against a baseline of 5370
- Kills: 6 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`
  - `tests/test_setbuilder_cli.py::test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[path-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_an_anchor_with_no_camelot_key_is_not_indexed`

Old text:

```
        "setbuild-anchor-not-indexed": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u272.C1_no_flush`

flush_to_disk: open and close the path and flush nothing

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C1_no_flush`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 642 against a baseline of 642
- Kills: 14 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_a_capture_outside_the_configured_store_is_flushed_too`
  - `tests/test_snapshot_flush_u272.py::test_a_directory_is_flushed_through_the_same_call`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[EINVAL]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTSUP]`
  - `tests/test_snapshot_flush_u272.py::test_a_filesystem_without_the_full_flush_gets_the_plain_sync[ENOTTY]`
  - `tests/test_snapshot_flush_u272.py::test_a_full_flush_that_fails_on_the_device_raises_rather_than_falling_back`
  - `tests/test_snapshot_flush_u272.py::test_a_plain_sync_that_fails_raises`
  - `tests/test_snapshot_flush_u272.py::test_an_unverified_capture_is_flushed_in_the_same_order`
  - `tests/test_snapshot_flush_u272.py::test_every_file_a_capture_holds_is_flushed_before_its_manifest_by_walking`
  - `tests/test_snapshot_flush_u272.py::test_the_copy_its_companions_and_its_directories_reach_the_disk_before_the_manifest`
  - `tests/test_snapshot_flush_u272.py::test_the_flush_follows_the_check_so_what_the_check_leaves_is_flushed`
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`
  - `tests/test_snapshot_flush_u272.py::test_the_manifest_is_followed_by_a_flush_of_the_directory_that_holds_it`
  - `tests/test_snapshot_flush_u272.py::test_where_no_full_flush_exists_the_plain_sync_is_the_flush`

Old text:

```
    try:
        _flush_descriptor(fd)
    except OSError as exc:
```

New text:

```
    try:
        pass
    except OSError as exc:
```

### `u272.C3_full_flush_then_sync`

_flush_descriptor: drop the return after a full flush, so the plain sync runs as well

- File: `src/cratekit/core/config.py`
- Source: `u272.json`, row `C3_full_flush_then_sync`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_snapshot_flush_u272.py`, `tests/test_snapshot.py`, `tests/test_config.py`, `tests/test_config_test_root.py`, `tests/test_write_session.py`, `tests/test_restore.py`, `tests/test_rb_snapshot.py`
- Collected: 642 against a baseline of 642
- Kills: 1 (killed)
- Killed:
  - `tests/test_snapshot_flush_u272.py::test_the_full_flush_is_asked_for_where_the_platform_offers_one`

Old text:

```
            _full_flush(fd, _FULL_FLUSH)
            return
```

New text:

```
            _full_flush(fd, _FULL_FLUSH)
```

