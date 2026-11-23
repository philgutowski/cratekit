# Mutation table: u312-replay-before-5

Measured by `scripts/mutate.py` on 2026-11-23 12:19 UTC, branch `HEAD` at `bece470e`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 124.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `269cecd96b22`, and this tree is at `bece470ea56f`).

Subset baselines: 36, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 113 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1394.P2_counts_not_carried` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1394.P3_begun_answers_no_recorder` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 5 | killed |
| `r1394.P9_finish_not_held_to_the_agreed_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `r1411.W1_finish_passes_no_agreed` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 10 | killed |
| `r1411.W2_finish_passes_agreed_only_with_nothing_else` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 7 | killed |
| `r1411.W3_agreed_is_the_asked_order` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 10 | killed |
| `r1411.W4_agreed_is_the_checks_listing` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M10_moved_unrecorded` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 1 | killed |
| `u231.M11_snapshot_from_the_order_sent` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 15 | killed |
| `u231.M12_settle_takes_any_reading` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 12 | killed |
| `u231.M13_settle_sleeps_the_whole_window` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M14_settle_reading_not_kept` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M23_carried_moving_unread` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 2 | killed |
| `u231.M7_continue_resends` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 6 | killed |
| `u231.M8_no_record_sends_blind` | `src/cratekit/sync/pair_write.py` | user | 20 file(s) | 750 | 1 | killed |
| `r1376.F11_leader_lost` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 4 | killed |
| `r1376.F3_call_site_gone` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 6 | killed |
| `r1376.F4_first_sync_unrecorded_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1376.F5_first_sync_marked_only` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 318 | killed |
| `r1376.F6_every_sync_first` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 4 | killed |
| `u225.M15_fold_despite_skip` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M16_account_base_unfolded` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M17_rekordbox_base_unfolded` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M20_stopped_not_passed` | `src/cratekit/sync/pair_plan.py` | user | 19 file(s) | 662 | 3 | killed |
| `r1372.K6_reader_ignores_carried` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 7 | killed |
| `r1372.K9_carried_unread_unsaid` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 1 | killed |
| `r1376.F13_snapshot_guard_inclusive` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 34 | killed |
| `r1376.F1_first_stop_none` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 7 | killed |
| `u225.M14_superseded_unchecked` | `src/cratekit/sync/pair_read.py` | user | 19 file(s) | 662 | 4 | killed |
| `u225.M24_unread_unsaid` | `src/cratekit/sync/pair_screen.py` | user | 19 file(s) | 662 | 2 | killed |
| `r1372.K17_no_let_go_at_snapshot` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 2 | killed |
| `r1372.K1_no_carry` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 9 | killed |
| `r1372.K4_carry_unwritten_not_refused` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M21_start_from_asked` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M22_written_always` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `u225.M23_links_dropped` | `src/cratekit/sync/pair_write.py` | user | 19 file(s) | 662 | 1 | killed |
| `r227.A2_never_stale` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 13 | killed |
| `u208.M19_adapter_never_records_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 5 | killed |
| `u226.M1_equal_not_agreed` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 785 | 78 | killed |
| `u226.M4_prefix_as_subset` | `src/cratekit/acquire/listing.py` | user | 13 file(s) | 785 | 3 | killed |
| `r1360.J3_prefix_always_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 4 | killed |
| `r1360.J4_prefix_uncounted_lags` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 2 | killed |
| `r1360.W8_overlap_kept` | `src/cratekit/acquire/listing.py` | user | 15 file(s) | 828 | 25 | killed |
| `u12-independent-round-6.C4_darwin_headroom` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 4 | killed |
| `u12-independent-round-6.G3_headroom_can_go_negative` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M1_measurement_below_the_floor` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u12-independent-round-6.M7_parent_keeps_the_write_end` | `src/cratekit/core/pool.py` | user | 1 file(s) | 269 | 1 | killed |
| `u211.D1_refusal_keeps_its_run` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1178 | 2 | killed |
| `u211.D2_continue_step_named` | `src/cratekit/cli/__init__.py` | user | 4 file(s) | 1178 | 2 | killed |
| `u211.P12_careful_pid_refuses` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 8 | killed |
| `u211.P3_recheck_before_refusing` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 9 | killed |
| `u211.P4_zombie_status_reads_zombie` | `src/cratekit/core/processes.py` | user | 2 file(s) | 58 | 8 | killed |
| `u211.P7_unreadable_refuses` | `src/cratekit/core/processes.py` | user | 3 file(s) | 109 | 17 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_probes.py` | user | 3 file(s) | 270 | 15 | killed |
| `u211.D4_only_the_scans_own_refusal_is_kept` | `src/cratekit/cli/__init__.py` | user | 3 file(s) | 137 | 1 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 334 | 20 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 334 | 76 | killed |
| `u278.M9_continue_names_no_hour` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 248 | 3 | killed |
| `u293.L2_night_reset` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 4 | killed |
| `u293.L3_spent_off_by_one` | `src/cratekit/core/night_budget.py` | user | 2 file(s) | 103 | 2 | killed |
| `u326.R8_general_catalogue_refused` | `tests/conftest.py` | maintainer | 1 file(s) | 141 | 1 | killed |
| `r239-a.A1_probe_to_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 122 | killed |
| `r239-a.A2_probe_to_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A3_probe_removed` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 7 | killed |
| `r239-a.A4_open_default_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 121 | killed |
| `r239-a.A7_needed_always_true` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 122 | killed |
| `r239-a.A8_needed_always_false` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 8 | killed |
| `r239-a.A9_header_nearby_value` | `src/cratekit/core/rb_writer.py` | user | 6 file(s) | 706 | 122 | killed |
| `r239-b.S5_converge_key_off` | `src/cratekit/cli/converge.py` | user | 7 file(s) | 723 | 2 | killed |
| `r239-b.S2_unplaced_key_off` | `src/cratekit/write/routing_export.py` | user | 7 file(s) | 723 | 2 | killed |
| `u288.M1_delete_admitted_by_any_name` | `src/cratekit/core/rb_changes.py` | user | 2 file(s) | 286 | 2 | killed |
| `r1830.M2_marked_removed_row_counted` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 3 | killed |
| `r1830.M4_one_place_whatever_removed` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 2 | killed |
| `r1830.M5_any_playlist_counts` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 16 | killed |
| `u288.M10_changed_rows` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 7 | killed |
| `u288.M12_still_names` | `src/cratekit/core/rb_removal.py` | user | 2 file(s) | 286 | 1 | killed |
| `u302.W4_open_tag_never_self_closing` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 17 | killed |
| `r312.E12_check_names_no_file` | `src/cratekit/write/convergence_check.py` | user | 2 file(s) | 307 | 6 | killed |
| `r312.E10_empty_still_warns` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 3 | killed |
| `r312.E13_record_drops_location` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 6 | killed |
| `r312.E14_listed_in_dropped` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 3 | killed |
| `r678-a.A12_retired_file_unnamed` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 3 | killed |
| `r678-a.A2_drop_the_import_proof_case` | `src/cratekit/cli/render.py` | user | 2 file(s) | 89 | 2 | killed |
| `u167.M20_session_state` | `src/cratekit/analysis/rekordbox_check.py` | user | 2 file(s) | 22479 | 0 (promoted) | zero |
| `u27-reports-round-1.S1_limit_floor` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.S2_truncation_row` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S3_summary_total` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.S6_lossy_marker` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 3 | killed |
| `u27-reports-round-2.S5_handler_key_wrong` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-3-fixes.F1_as_of_falsiness` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-3-fixes.F5_gap_row_flood` | `src/cratekit/cli/reports.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.W2_unreadable_reported` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 229 | 2 | killed |
| `u211.D3_kept_set_is_narrow` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 229 | 1 | killed |
| `u48-author.P3_two_codes_collapsed_to_one` | `src/cratekit/modules/tools/backup.py` | user | 1 file(s) | 229 | 2 | killed |
| `u258.M9_population_keeps_the_owners` | `tests/test_reserved_causes.py` | maintainer | 2 file(s) | 239 | 2 | killed |
| `u326.W1_children_reads_lists` | `tests/_source_guards.py` | maintainer | 4 file(s) | 1593 | 150 | killed |
| `u326.W2_cache_by_identity` | `tests/_source_guards.py` | maintainer | 4 file(s) | 1593 | 143 | killed |
| `u125.P2_drop_slug` | `tests/_pinned_reserved_populations.py` | maintainer | 2 file(s) | 2 | 2 | killed |
| `u296.M19_pin_in_the_wrong_file` | `tests/_pinned_reserved_populations.py` | maintainer | 2 file(s) | 235 | 2 | killed |
| `u296.M20_unknown_pin_table` | `tests/_pinned_reserved_populations.py` | maintainer | 2 file(s) | 235 | 1 | killed |
| `r592-a.A1_occupancy_guard_removed` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r592-a.A2_database_dropped_from_fileset` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `r592-a.A4_fileset_not_rebased` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 4 | killed |
| `r592-a.A5_replacing_existing_inverted` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 8 | killed |
| `r592-a.A6_old_suffix_rule_restored` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 2 | killed |
| `r338-c.C4_bare_metal_asks_about_the_share` | `src/cratekit/session/restore_cli.py` | user | 2 file(s) | 22479 | 0 (promoted) | zero |
| `r592-b.B1_step_on_every_failure` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `r592-b.B2_step_on_the_wrong_half` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `r592-b.B4_step_names_the_wrong_directory` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `r592-b.B5_step_names_no_file` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `r592-b.B7_sample_halves_split` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A12_which_half_failed` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u96-a.A13_completed_halves_recorded` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 1 | killed |
| `u96-a.A15_report_names_where_the_database_is` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u96-a.A4_run_inside_the_held_session` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A5_the_mirror_is_pulled` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A6_a_half_at_a_time` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 94 | 2 | killed |
| `u96-a.A8_database_elsewhere_is_skipped` | `src/cratekit/session/restore_cli.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `r592-b.B6_restore_mirror_carries_the_database` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 3 file(s) | 22479 | 0 (promoted) | zero |
| `u96-b.C3_engine_occupied_target` | `src/cratekit/core/restore_recovery.py` | user | 2 file(s) | 253 | 3 | killed |
| `u169.N6_repair_apply_bypasses` | `src/cratekit/intake/repair_cli.py` | user | 2 file(s) | 37 | 1 | killed |
| `u169.N1_relative_read_against_cwd` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N3_missing_folder_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N4_name_apply_bypasses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u89.C1_converge_threshold` | `src/cratekit/cli/converge.py` | user | 1 file(s) | 197 | 2 | killed |
| `u132.W5_rebuild_note` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 21 | killed |
| `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.W4_rebuild_worker` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.W6_rebuild_resume_loads_first` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 3 | killed |
| `u155.R4_genre_sub_named` | `src/cratekit/core/routing.py` | user | 1 file(s) | 197 | 3 | killed |
| `r316.M11_warning_ignores_dimension` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 197 | 8 | killed |
| `r316.M3_inbox_gaps_leak_into_totals` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r691.F2_trees_left_off` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F3_planner_warnings_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F4_gaps_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r691.K2_gaps_not_carried_to_the_apply` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N3_declined_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N4_inbox_empty_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r691.P1_destination_left_off_the_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r691.P2_vocal_left_off_the_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.W1_write_ignores_the_plan` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 22 | killed |
| `u53-routing-and-rebuild-workers.A3_empty_folder_shortcircuit_removed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u53-routing-and-rebuild-workers.A5_applied_always_true` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R1_resort_drives_a_foreign_job` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E22_export_remedy` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E23_export_branch` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 57 | killed |
| `u89.W1_resort_worker` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U14_no_native_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U15_export_branch` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 18 | killed |
| `r686.E1_tracks_counts_every_item` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E2_routed_counts_vocal` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 9 | killed |
| `r686.E4_long_tracks_intake_only` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `r686.E5_warnings_dropped` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `r686.E6_gaps_dropped` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E7_subs_not_named` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.B1_owed_rating_blocks_the_answer` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.C1_rates_flag_ignored` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.C2_no_energy_counted` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.G1_zero_owed_still_warns` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 9 | killed |
| `r688.G2_count_off_by_one` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 7 | killed |
| `r688.N1_long_track_change_not_a_write` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.U1_hand_rated_counted` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `r688.U2_missing_attribute_counted` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 8 | killed |
| `r688.U3_empty_rating_not_unrated` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 3 | killed |
| `r688.V1_applied_envelope_drops_warning` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 6 | killed |
| `r688.V2_gate_drops_warning` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 3 | killed |
| `r688.V3_declined_envelope_drops_warning` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.W1_rating_written_again` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 5 | killed |
| `r691.F1_routed_counts_vocal` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 9 | killed |
| `r691.P4_digest_over_the_file_list` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u302.W5_blocked_sweep_reads_as_filed` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 6 | killed |
| `u302.W6_written_sweep_gets_a_reason` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 11 | killed |
| `u53-routing-and-rebuild-workers.U1_unplaced_constant_empty` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `u53-routing-and-rebuild-workers.U2_compared_true_without_a_tree` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `u53-routing-and-rebuild-workers.U3_held_never_populated` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.U4_tombstones_reported` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I1_native_filter_dropped` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E14_non_creating_writer` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E16_never_in_place` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 32 | killed |
| `u86.E10_unreadable_not_routed` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 3 | killed |
| `u86.E11_is_file` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 5 | killed |
| `u86.E12_prefix_map` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E4_export_absent` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E6_intake_absent` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E9_row_absent` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `u88.D1_zero_is_a_length` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.D2_prefix_digits` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.D3_absent_attribute` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 41 | killed |
| `u88.I1_items_outside_intake` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `u88.I2_item_flag` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 3 | killed |

## Zero rows and what they owe

- `u167.M20_session_state` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r338-c.C4_bare_metal_asks_about_the_share` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B1_step_on_every_failure` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B2_step_on_the_wrong_half` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B4_step_names_the_wrong_directory` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A12_which_half_failed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A15_report_names_where_the_database_is` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u96-a.A8_database_elsewhere_is_skipped` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r592-b.B6_restore_mirror_carries_the_database` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1394.P2_counts_not_carried`

pair write: the recorder's counts are marked in the run's steps but not carried past the run

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1394.json`, row `P2_counts_not_carried`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `u231.M10_moved_unrecorded`

write: every move accepted is not recorded, so a later lag on the path is finished from

- File: `src/cratekit/sync/pair_write.py`
- Source: `u231.json`, row `M10_moved_unrecorded`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: moved by hand: the same guard, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py; the clock is read through pair_model._now, its home since the split, so one patch of it reaches every caller
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `r1376.F11_leader_lost`

plan_pair: the stop is read as led by the account whatever side led it

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F11_leader_lost`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
            leader=stopped_write.leader,
```

New text:

```
            leader=pair_merge.ACCOUNT,
```

### `r1376.F3_call_site_gone`

plan_pair: a first sync never asks for the stop on its account playlist

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F3_call_site_gone`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
    if stopped_write is None and first_sync:
        stopped_write = reader.first_stop(target.account_id)
```

New text:

```
    if False:
        stopped_write = reader.first_stop(target.account_id)
```

### `r1376.F4_first_sync_unrecorded_only`

plan_pair: a pair marked with no snapshot is not read as a first sync, so its earlier stop is kept out by the mark

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F4_first_sync_unrecorded_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is None
```

### `r1376.F5_first_sync_marked_only`

plan_pair: a pair with no record at all, a hand pairing before its mark, is not read as a first sync

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F5_first_sync_marked_only`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 318 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - `tests/test_sync_pair.py::test_a_row_with_no_isrc_anywhere_is_named_and_the_provider_is_not_asked`
  - `tests/test_sync_pair.py::test_a_second_rekordbox_playlist_for_a_paired_account_playlist_is_refused`
  - `tests/test_sync_pair.py::test_a_session_log_that_cannot_be_listed_holds_the_track`
  - ... and 303 more, see the JSON sidecar

Old text:

```
    first_sync = held is None or held.first
```

New text:

```
    first_sync = held is not None and held.first
```

### `r1376.F6_every_sync_first`

plan_pair: every sync reads the stop whatever its snapshot, so a stop the snapshot passed is finished again

- File: `src/cratekit/sync/pair_plan.py`
- Source: `r1376.json`, row `F6_every_sync_first`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
    if stopped_write is None and first_sync:
```

New text:

```
    if stopped_write is None:
```

### `u225.M15_fold_despite_skip`

plan_pair: both bases move to the stopped write's though it skipped rekordbox

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M15_fold_despite_skip`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_that_skipped_rekordbox_leaves_the_accounts_removal_to_be_made`

Old text:

```
    folded = stopped_write is not None and stopped_write.written
```

New text:

```
    folded = stopped_write is not None
```

### `u225.M16_account_base_unfolded`

plan_pair: the account base is the snapshot's, not what the stopped write left

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M16_account_base_unfolded`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
                if folded
                else held.account or ()
```

New text:

```
                if False
                else held.account or ()
```

### `u225.M17_rekordbox_base_unfolded`

plan_pair: the rekordbox base is the snapshot's, not what the stopped write left

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M17_rekordbox_base_unfolded`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_track_the_stopped_write_added_then_taken_off_in_rekordbox_comes_off_the_account`

Old text:

```
            if folded
            else tuple(held.rekordbox or ())
```

New text:

```
            if False
            else tuple(held.rekordbox or ())
```

### `u225.M20_stopped_not_passed`

plan_pair: the stopped write is not handed to the merge

- File: `src/cratekit/sync/pair_plan.py`
- Source: `u225.json`, row `M20_stopped_not_passed`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_plan.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_names_the_pair_as_finishing_the_stopped_run`
  - `tests/test_sync_pair_stopped_order.py::test_the_gate_says_the_account_was_read_off_the_moves_path`

Old text:

```
        stopped=stopped,
```

New text:

```
        stopped=None,
```

### `r1372.K6_reader_ignores_carried`

reader: the carried records are not read, only the kept steps

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K6_reader_ignores_carried`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        records = [*records, *(one for one in kept if (one.run_id, one.digest) not in current)]
```

New text:

```
        records = [*records]
```

### `r1372.K9_carried_unread_unsaid`

reader: a carried record that cannot be read is not named

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1372.json`, row `K9_carried_unread_unsaid`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
        problems = [*problems, *unread]
```

New text:

```
        problems = [*problems]
```

### `r1376.F13_snapshot_guard_inclusive`

stopped_write (sample, U225): a stop that began after the snapshot by a hair is read as passed

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F13_snapshot_guard_inclusive`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 34 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_fresh_sync_orders_the_account_to_rekordbox_and_plans_no_rekordbox_order`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_reading_that_never_settled_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_reading_still_on_the_moves_path_is_finished_never_read_as_a_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_later_run_that_failed_before_its_order_began_does_not_hide_the_stopped_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_before_the_stop_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_kept_for_another_run_shows_no_reorder`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_on_the_path_is_never_the_baseline_so_the_partial_state_after_it_finishes`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None or True:
```

### `r1376.F1_first_stop_none`

first_stop: a first sync is never handed the stop on its account playlist

- File: `src/cratekit/sync/pair_read.py`
- Source: `r1376.json`, row `F1_first_stop_none`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_first_sync_reads_the_stop_on_its_account_playlist_whatever_the_mark`
  - `tests/test_sync_pair_stopped_order.py::test_a_first_sync_whose_account_side_was_skipped_still_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_pair_released_after_a_stop_and_paired_again_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_at_the_root_never_takes_the_scramble_on_its_first_sync`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`

Old text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return write
```

New text:

```
        _began, write = self.stopped[0].get(account_id, (None, None))
        return None
```

### `u225.M14_superseded_unchecked`

stopped_write: a write the pair's snapshot came after is still finished

- File: `src/cratekit/sync/pair_read.py`
- Source: `u225.json`, row `M14_superseded_unchecked`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_read.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_stop_from_before_the_pair_was_marked_again_is_not_its_stop`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_a_fresh_sync_finished_is_left_behind_by_the_snapshot`
  - `tests/test_sync_pair_stopped_order.py::test_a_stopped_write_its_continue_holds_is_finished_by_the_next_sync_and_leaves_nothing`

Old text:

```
            if synced is None or not began > synced:
```

New text:

```
            if synced is None:
```

### `u225.M24_unread_unsaid`

_warnings: runs' steps that could not be read are not named

- File: `src/cratekit/sync/pair_screen.py`
- Source: `u225.json`, row `M24_unread_unsaid`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_screen.py, was in src/cratekit/sync/pair_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 662 against a baseline of 662
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write`

Old text:

```
    if planned.stopped_unread:
```

New text:

```
    if False:
```

### `r1372.K17_no_let_go_at_snapshot`

_record: a snapshot recorded whole lets go of no carried record of its pair

- File: `src/cratekit/sync/pair_write.py`
- Source: `r1372.json`, row `K17_no_let_go_at_snapshot`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `u225.M21_start_from_asked`

_write_account: the start is built from the asked removals and additions, not the adapter's answer

- File: `src/cratekit/sync/pair_write.py`
- Source: `u225.json`, row `M21_start_from_asked`
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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
- Moved: Anchored where u304-replay-after.json replayed it: the same text, now in src/cratekit/sync/pair_write.py, was in src/cratekit/sync/pair_cli.py
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

### `r227.A2_never_stale`

No export is ever stale, which is the tree before this unit

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A2_never_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return False
```

### `u208.M19_adapter_never_records_tie`

match_track: never record a broken tie

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M19_adapter_never_records_tie`
- Moved: Anchored where u309-replay-after-c.json replayed it: match_track moved from tidal_account.py into the Reads mixin in tidal_reads.py and its ISRC lookup lost a level of nesting; same branch reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
                elif tied:
                    self._ties.add(key)
```

New text:

```
                elif False:
                    self._ties.add(key)
```

### `u226.M1_equal_not_agreed`

judge_window: two equal reads are not read as agreeing first

- File: `src/cratekit/acquire/listing.py`
- Source: `u226.json`, row `M1_equal_not_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`
- Collected: 785 against a baseline of 785
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
- Collected: 785 against a baseline of 785
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

### `r1360.J3_prefix_always_lags`

judge_window: a first part beside a window short of the count lags too

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `J3_prefix_always_lags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
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
- Collected: 828 against a baseline of 828
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

### `r1360.W8_overlap_kept`

playlist_tracks_unpaged: the overlapping track is read twice

- File: `src/cratekit/acquire/listing.py`
- Source: `r1360.json`, row `W8_overlap_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_adapter_listing.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_hold.py`
- Collected: 828 against a baseline of 828
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

### `u12-independent-round-6.C4_darwin_headroom`

Raise the darwin headroom share from half to three quarters, which is the value the measured inactive-queue split says is too optimistic.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `C4_darwin_headroom`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 4 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_darwin_headroom_claims_half_because_half_is_what_was_measured`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[darwin-50]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[linux-75]`
  - `tests/test_pool_sizing.py::test_the_headroom_share_is_lower_where_the_reading_is_measurably_worse[win32-75]`

Old text:

```
DARWIN_HEADROOM_PERCENT = 50
```

New text:

```
DARWIN_HEADROOM_PERCENT = 75
```

### `u12-independent-round-6.G3_headroom_can_go_negative`

Report a negative headroom for a cgroup already over its cap.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `G3_headroom_can_go_negative`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_cgroup_already_over_its_cap_has_no_headroom_rather_than_negative`

Old text:

```
    return max(0, limit - used)

```

New text:

```
    return limit - used

```

### `u12-independent-round-6.M1_measurement_below_the_floor`

Return the measurement even when it is below the declared floor, so the floor becomes a fallback rather than a floor.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M1_measurement_below_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_the_probe_never_reports_below_the_declared_floor`

Old text:

```
    return max(measured, floor_bytes)

```

New text:

```
    return measured

```

### `u12-independent-round-6.M7_parent_keeps_the_write_end`

Leave the parent's copy of the pipe write end open, so a child that dies without answering is indistinguishable from a slow one.

- File: `src/cratekit/core/pool.py`
- Source: `u12-independent-round-6.json`, row `M7_parent_keeps_the_write_end`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_pool_sizing.py`
- Collected: 269 against a baseline of 269
- Kills: 1 (killed)
- Killed:
  - `tests/test_pool_sizing.py::test_a_probe_child_that_dies_without_answering_gives_up_at_once`

Old text:

```
    # exactly like a slow one until the timeout expired.
    writer.close()

```

New text:

```
    # exactly like a slow one until the timeout expired.

```

### `u211.D1_refusal_keeps_its_run`

dispatcher: a refusal under the unconfirmed cause is not kept, so the run fails and is not resumable

- File: `src/cratekit/cli/__init__.py`
- Source: `u211.json`, row `D1_refusal_keeps_its_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_cli_contract.py`, `tests/test_job_outcome.py`, `tests/test_run_decide_continue.py`
- Collected: 1178 against a baseline of 1178
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
            isinstance(exc, processes.AbsenceUnconfirmed)
            and cause.reason in gates.KEPT_RUN_REASONS
```

New text:

```
            False
            and cause.reason in gates.KEPT_RUN_REASONS
```

### `u211.D2_continue_step_named`

dispatcher: a kept refusal carries no step naming the command that continues it

- File: `src/cratekit/cli/__init__.py`
- Source: `u211.json`, row `D2_continue_step_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_cli_contract.py`, `tests/test_job_outcome.py`, `tests/test_run_decide_continue.py`
- Collected: 1178 against a baseline of 1178
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        if kept and state is not None:
            cause = _with_run_continue(cause, state)
```

New text:

```
        if False:
            cause = _with_run_continue(cause, state)
```

### `u211.P12_careful_pid_refuses`

rekordbox_pid: answer zero over an unreadable live process when the name was not read

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P12_careful_pid_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_careful_pid_refuses_over_an_unreadable_live_process`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`

Old text:

```
        if not any(executable_stem(found) == name for _pid, found in listed):
            raise
```

New text:

```
        if False:
            raise
```

### `u211.P3_recheck_before_refusing`

running_processes: refuse every process whose read raised, without asking whether it is now gone or a zombie

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P3_recheck_before_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 9 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[fails-to-build-then-gone]`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[system-error-then-status-zombie]`
  - `tests/test_process_scan.py::test_doctor_reads_a_skipped_zombie_as_nothing`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_answers_as_pyrekordbox_does`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`

Old text:

```
            if _gone_or_zombie(table, pid, process):
                continue
```

New text:

```
            if False:
                continue
```

### `u211.P4_zombie_status_reads_zombie`

_gone_or_zombie: never read the status as zombie, so the sitting's dying daemon refuses

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P4_zombie_status_reads_zombie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`
- Collected: 58 against a baseline of 58
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_process_that_is_dead_or_dying_is_skipped[system-error-then-status-zombie]`
  - `tests/test_process_scan.py::test_doctor_reads_a_skipped_zombie_as_nothing`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_answers_as_pyrekordbox_does`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_whole_list_is_walked_and_every_unreadable_pid_is_named`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`

Old text:

```
        return target.status() == platform.STATUS_ZOMBIE
```

New text:

```
        return target.status() == platform.STATUS_DEAD
```

### `u211.P7_unreadable_refuses`

running_processes: answer the processes it read and drop the refusal, so an unreadable live process reads as absent

- File: `src/cratekit/core/processes.py`
- Source: `u211.json`, row `P7_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_paths_resolved.py`
- Collected: 109 against a baseline of 109
- Kills: 17 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_backup_refuses_the_database_portion_alone_and_still_mirrors`
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_system_error_on_a_live_process_refuses_naming_the_pid`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[cannot-even-be-built]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[os-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[runtime-error]`
  - `tests/test_process_scan.py::test_any_error_on_a_live_process_refuses_rather_than_reading_absent[status-unreadable-too]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_doctor_names_an_unreadable_live_process_as_a_note`
  - `tests/test_process_scan.py::test_many_unreadable_pids_are_counted_past_the_named_ones`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_careful_pid_names_a_rekordbox_it_read_beside_an_unreadable_process`
  - `tests/test_process_scan.py::test_the_careful_pid_refuses_over_an_unreadable_live_process`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    if unreadable:
        raise _unconfirmed(unreadable, found) from first
```

New text:

```
    if False:
        raise _unconfirmed(unreadable, found) from first
```

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_probes.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_probes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 270 against a baseline of 270
- Kills: 15 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_the_binding_probe_at_open_only_loses_a_warning`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_names_rekordbox_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`

Old text:

```
        return processes.rekordbox_pid(name)
```

New text:

```
        raise
```

### `u211.D4_only_the_scans_own_refusal_is_kept`

dispatcher: keep the run of any refusal carrying the reason, a backup job's summary included, so its printed continue command refuses forever

- File: `src/cratekit/cli/__init__.py`
- Source: `u211.json`, row `D4_only_the_scans_own_refusal_is_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_scan_jobs.py`, `tests/test_backup_cli.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_process_scan_jobs.py::test_a_backup_job_refused_by_the_scan_is_not_offered_as_a_run_to_continue`

Old text:

```
            isinstance(exc, processes.AbsenceUnconfirmed)
            and cause.reason in gates.KEPT_RUN_REASONS
```

New text:

```
            True
            and cause.reason in gates.KEPT_RUN_REASONS
```

### `u211.W4_probe_wrapped_at_commit`

commit: run the binding's commit without the careful probe, so its own walk meets the dying process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W4_probe_wrapped_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 334 against a baseline of 334
- Kills: 20 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_skipped_rekordbox_side_is_finished_by_the_next_sync`
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_is_added_and_never_queued`
  - `tests/test_sync_pair.py::test_a_track_another_account_playlist_landed_with_its_isrc_in_the_row_is_added`
  - `tests/test_sync_pair.py::test_a_track_another_pairs_intake_job_found_owned_is_added`
  - `tests/test_sync_pair.py::test_a_track_held_twice_that_lost_one_copy_is_not_read_as_put_back`
  - `tests/test_sync_pair.py::test_a_track_removed_on_the_account_leaves_the_playlist_and_stays_in_the_collection`
  - `tests/test_sync_pair.py::test_an_account_track_found_by_isrc_is_linked_and_the_link_is_kept`
  - `tests/test_sync_pair.py::test_one_row_landed_in_two_inbox_playlists_is_one_row`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_the_first_sync_removes_nothing_on_either_side`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        with _binding_probe(strict=True):
            db.commit()
```

New text:

```
        with nullcontext():
            db.commit()
```

### `u211.W5_probe_wrapped_at_open`

open_db: construct the binding without the careful probe, so the dying process reads as a damaged library

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W5_probe_wrapped_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 334 against a baseline of 334
- Kills: 76 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_a_rekordbox_running_refusal_still_ends_the_run_as_failed`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_sync_pair.py::test_a_first_sync_with_a_side_skipped_records_no_snapshot_and_stays_first`
  - `tests/test_sync_pair.py::test_a_folder_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_job_naming_no_playlist_is_named_by_its_account_playlist`
  - `tests/test_sync_pair.py::test_a_label_playlist_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_landed_track_is_found_in_the_inbox_playlist_landed_for_the_account`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`
  - `tests/test_sync_pair.py::test_a_pair_whose_playlist_is_gone_does_not_hold_every_other_pair`
  - `tests/test_sync_pair.py::test_a_plan_with_every_landing_record_readable_warns_nothing_of_them`
  - `tests/test_sync_pair.py::test_a_playlist_under_one_of_cratekits_trees_is_not_a_pair`
  - `tests/test_sync_pair.py::test_a_rekordbox_change_between_the_gates_and_the_write_refuses_as_stale`
  - `tests/test_sync_pair.py::test_a_rekordbox_row_with_no_isrc_column_is_matched_on_its_files_isrc`
  - ... and 61 more, see the JSON sidecar

Old text:

```
        with _binding_probe(strict=False):
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

New text:

```
        with nullcontext():
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

### `u278.M9_continue_names_no_hour`

hour_to_name: never name the hour, so a continue above the budget is refused as printed

- File: `src/cratekit/core/provider_gate.py`
- Source: `u278.json`, row `M9_continue_names_no_hour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_sync_pair_resume.py`, `tests/test_label_playlists.py`
- Collected: 248 against a baseline of 248
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_parked_jobs_continue_carries_the_hour_its_ceiling_needs`
  - `tests/test_sync_pair_resume.py::test_a_ceiling_continue_above_the_hour_names_the_hour_and_finishes_the_run`
  - `tests/test_sync_pair_resume.py::test_a_gate_forecast_above_the_hour_names_the_hour_and_its_command_runs`

Old text:

```
    return wanted if wanted > settings.calls_per_hour else None
```

New text:

```
    return None
```

### `u293.L2_night_reset`

open_night: every firing starts from nothing, whatever the night spent

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L2_night_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 4 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_second_firing_of_the_night_has_only_what_is_left`
  - `tests/test_provider_gate_night.py::test_a_spent_night_refuses_and_names_when_it_frees`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`
  - `tests/test_sync_night.py::test_a_night_already_spent_refuses_before_any_call`

Old text:

```
    spent = ledger.spent if ledger.night == night else 0
    if ledger.open_start is not None:
        # A DEAD
```

New text:

```
    spent = 0
    if ledger.open_start is not None:
        # A DEAD
```

### `u293.L3_spent_off_by_one`

open_night: a night with exactly its budget spent is not refused

- File: `src/cratekit/core/night_budget.py`
- Source: `u293.json`, row `L3_spent_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_sync_night.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_spent_night_refuses_and_names_when_it_frees`
  - `tests/test_sync_night.py::test_a_night_already_spent_refuses_before_any_call`

Old text:

```
    if spent >= budget:
```

New text:

```
    if spent > budget:
```

### `u326.R8_general_catalogue_refused`

_no_live_general_catalogue: leave the process wide genre lookup as shipped, so an ISRC asks the real catalogue

- File: `tests/conftest.py`
- Source: `u326.json`, row `R8_general_catalogue_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_published_genre.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_published_genre.py::test_the_suite_cannot_reach_the_live_catalogue_through_the_shared_lookup`

Old text:

```
        monkeypatch.setattr(published, "_shared", [guarded])
```

New text:

```
        pass
```

### `r239-a.A1_probe_to_true`

open_db answers every unnamed open with the key on, the old default, instead of asking the file

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A1_probe_to_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
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

### `r239-a.A2_probe_to_false`

open_db answers every unnamed open with the key off, the constant the five verb sites used to pass

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A2_probe_to_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
    if unlock is None:
        unlock = False

```

### `r239-a.A3_probe_removed`

Delete the probe block, so None reaches the binding, which reads it as no key

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A3_probe_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
    if unlock is None:
        unlock = unlock_needed(target)

```

New text:

```
(empty)
```

### `r239-a.A4_open_default_true`

open_db's unlock default back to True, so the probe branch never fires for an unnamed open

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A4_open_default_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 121 (killed)
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
  - ... and 106 more, see the JSON sidecar

Old text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = None,

```

New text:

```
    force_cloud_canary: bool = False,
    unlock: bool | None = True,

```

### `r239-a.A7_needed_always_true`

unlock_needed answers encrypted for every readable file, the U55 row that read zero with no encrypted input

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A7_needed_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
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

### `r239-a.A8_needed_always_false`

unlock_needed answers plain for every readable file, the other U55 zero row, now with an encrypted input to fail on

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A8_needed_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
- Kills: 8 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_a_snapshot_check_that_names_no_key_verifies_either_kind[encrypted]`
  - `tests/test_rb_writer_db.py::test_an_encrypted_database_does_not_open_with_the_key_withheld`
  - `tests/test_rb_writer_db.py::test_an_open_that_names_no_key_opens_either_kind_of_database[encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[rebuild-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_the_confirmed_inbox_applies_and_the_declined_one_does_not[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
            return not handle.read(len(SQLITE_HEADER)).startswith(SQLITE_HEADER)
```

New text:

```
            return False
```

### `r239-a.A9_header_nearby_value`

The plain header constant to a realistic nearby value, SQLite format 4, so no plain file matches it

- File: `src/cratekit/core/rb_writer.py`
- Source: `r239-a.json`, row `A9_header_nearby_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`
- Collected: 706 against a baseline of 706
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

### `r239-b.S5_converge_key_off`

converge passes unlock=False again, so every native tree reads not compared on a real library

- File: `src/cratekit/cli/converge.py`
- Source: `r239-b.json`, row `S5_converge_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 723 against a baseline of 723
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`
  - `tests/test_routing_workers.py::test_converge_compares_a_native_tree_on_an_encrypted_library`

Old text:

```
            handle = rb_writer.open_db(cfg=cfg)
```

New text:

```
            handle = rb_writer.open_db(cfg=cfg, unlock=False)
```

### `r239-b.S2_unplaced_key_off`

route unplaced's open, unplaced_items, passes unlock=False again

- File: `src/cratekit/write/routing_export.py`
- Source: `r239-b.json`, row `S2_unplaced_key_off`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 723 against a baseline of 723
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`

Old text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg, unlock=False)

```

### `u288.M1_delete_admitted_by_any_name`

guard_violations: admit a delete in any table once any table is named, not only the named one

- File: `src/cratekit/core/rb_changes.py`
- Source: `u288.json`, row `M1_delete_admitted_by_any_name`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_changes.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_delete_is_admitted_only_in_a_table_the_commit_names`
  - `tests/test_sync_removed.py::test_another_writer_deleting_a_content_row_through_the_binding_is_refused_at_its_commit`

Old text:

```
        if table in deletable:
            continue
```

New text:

```
        if deletable:
            continue
```

### `r1830.M2_marked_removed_row_counted`

renumbered_positions: a removed row marked removed counts, review round one's B1

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M2_marked_removed_row_counted`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 3 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_marked_row_is_neither_counted_nor_moved_so_live_numbers_stay_distinct`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`

Old text:

```
        if content in gone and live and number is not None:
```

New text:

```
        if content in gone and number is not None:
```

### `r1830.M4_one_place_whatever_removed`

renumbered_positions: a row moves one place however many removed rows sit below it

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M4_one_place_whatever_removed`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_two_removed_members_of_one_playlist_lower_each_row_by_those_below_it`
  - `tests/test_sync_removed.py::test_two_removed_members_of_one_playlist_and_a_member_on_two_playlists`

Old text:

```
            moved[key] = (playlist, int(number), int(number) - below)
```

New text:

```
            moved[key] = (playlist, int(number), int(number) - 1)
```

### `r1830.M5_any_playlist_counts`

renumbered_positions: a removed row in any playlist lowers rows in every playlist

- File: `src/cratekit/core/rb_removal.py`
- Source: `r1830.json`, row `M5_any_playlist_counts`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 16 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_member_on_two_playlists_renumbers_each_by_its_own_place_and_no_other`
  - `tests/test_sync_removed.py::test_a_commit_that_lands_and_then_raises_still_records_every_row`
  - `tests/test_sync_removed.py::test_a_history_list_holding_others_keeps_its_numbers`
  - `tests/test_sync_removed.py::test_a_position_the_pass_holds_is_kept_and_the_collection_not_walked`
  - `tests/test_sync_removed.py::test_a_read_back_that_disagrees_refuses_as_unverified`
  - `tests/test_sync_removed.py::test_a_removed_member_in_the_middle_of_three_leaves_one_and_two_and_nothing_else_moved`
  - `tests/test_sync_removed.py::test_a_removed_row_the_database_holds_again_is_not_offered_by_delete_review`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moved_between_the_gate_and_the_write_refuses_as_stale`
  - `tests/test_sync_removed.py::test_a_track_only_marked_out_of_a_playlist_renumbers_none_of_its_live_members`
  - `tests/test_sync_removed.py::test_an_append_after_a_renumbering_takes_the_next_position`
  - `tests/test_sync_removed.py::test_apply_takes_out_exactly_the_offered_rows_and_every_row_naming_them`
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_sync_removed.py::test_the_last_member_removed_renumbers_nothing_in_its_playlist`
  - `tests/test_sync_removed.py::test_the_removal_writes_no_beat_grid_and_no_tempo`
  - `tests/test_sync_removed.py::test_the_session_record_names_every_row_removed_and_restore_list_reads_it`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        below = sum(1 for one in deleted.get(playlist, ()) if one < int(number))
```

New text:

```
        below = sum(1 for numbers in deleted.values() for one in numbers if one < int(number))
```

### `u288.M10_changed_rows`

collection_removal_violations: read a changed row as unchanged

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M10_changed_rows`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 7 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_confined_removal_reads_clean_and_every_stray_difference_is_named`
  - `tests/test_rb_writer_guard.py::test_a_reading_with_no_positions_admits_no_membership_change`
  - `tests/test_rb_writer_guard.py::test_the_confinement_admits_the_planned_renumbering_and_nothing_beside_it`
  - `tests/test_rb_writer_guard.py::test_the_confinement_refuses_a_marked_row_renumbered`
  - `tests/test_rb_writer_guard.py::test_the_read_back_after_the_commit_admits_only_the_counter_moving_forward`
  - `tests/test_sync_removed.py::test_a_renumbering_that_moves_any_other_membership_is_refused_with_nothing_written`
  - `tests/test_sync_removed.py::test_commit_proves_the_removal_confined_before_it_commits`

Old text:

```
            if old[key] == new[key]:
                continue
```

New text:

```
            if True:
                continue
```

### `u288.M12_still_names`

collection_removal_violations: drop the check that every row naming a removed track is gone

- File: `src/cratekit/core/rb_removal.py`
- Source: `u288.json`, row `M12_still_names`
- Moved: Anchored where u300-replay-after-a.json replayed it: the same text, now in src/cratekit/core/rb_removal.py, was in src/cratekit/core/rb_writer.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_guard.py`, `tests/test_sync_removed.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_guard.py::test_a_planned_removal_that_was_not_made_is_refused`

Old text:

```
            if names in gone and key in new:
```

New text:

```
            if False:
```

### `u302.W4_open_tag_never_self_closing`

_open_tag: every open tag is read as one that has children

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W4_open_tag_never_self_closing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_registry.py`
- Collected: 164 against a baseline of 164
- Kills: 17 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_rating_patch_is_exact_id_match`
  - `tests/test_rbxml.py::test_remove_folder_node_self_closed_target_does_not_wipe_siblings`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_splice_digit_growth_into_self_closing_sub`
  - `tests/test_rbxml.py::test_splice_is_playlists_scoped`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_registry.py::test_a_track_id_never_matches_a_longer_one`
  - `tests/test_tree_registry.py::test_the_locates_read_attributes_in_either_order`
  - `tests/test_xml_splice_golden.py::test_add_vocal_playlists_is_idempotent`
  - `tests/test_xml_splice_golden.py::test_name_collision_current_behaviour`
  - `tests/test_xml_splice_golden.py::test_rating_write_golden`
  - `tests/test_xml_splice_golden.py::test_route_into_energy_sub_golden`
  - `tests/test_xml_splice_golden.py::test_second_rating_writer_golden`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), raw_attrs.endswith(b"/")
```

New text:

```
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), False
```

### `r312.E12_check_names_no_file`

check: an unexpected difference carries no file location, the state before this unit

- File: `src/cratekit/write/convergence_check.py`
- Source: `r312.json`, row `E12_check_names_no_file`
- Moved: Anchored where u302-replay-after-c.json replayed it: the same text, now in src/cratekit/write/convergence_check.py, was in src/cratekit/write/rebuild.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 6 (killed)
- Killed:
  - `tests/test_rebuild.py::test_the_check_reports_a_difference_in_both_directions`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
            replace(entry, location=located_at.get(entry.content_id or ""))
```

New text:

```
            replace(entry, location=None)
```

### `r312.E10_empty_still_warns`

left_behind_message: a run that left nothing still produces a sentence

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E10_empty_still_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[converged]`
  - `tests/test_routing_workers.py::test_a_resort_that_left_nothing_behind_says_nothing_about_it`
  - `tests/test_routing_workers.py::test_the_leftover_code_is_the_locked_spelling`

Old text:

```
    if not found:
        return None
    named
```

New text:

```
    named
```

### `r312.E13_record_drops_location`

left_behind_record: the written record carries no location, so the message falls back to a row number

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E13_record_drops_location`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_the_record_a_worker_writes_is_the_one_the_message_reads`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
        "location": entry.location,
    }
```

New text:

```
        "location": None,
    }
```

### `r312.E14_listed_in_dropped`

left_behind_message: reword the closing sentence so it no longer says where the whole list is

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E14_listed_in_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 307 against a baseline of 307
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_leftover_warning_is_capped_and_still_counts_every_one`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
        f"Every one is listed in {listed_in}"
```

New text:

```
        "Every one was recorded"
```

### `r678-a.A12_retired_file_unnamed`

the retired intake file's name is dropped from the proof line

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A12_retired_file_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_render_payloads.py::test_each_proof_action_is_worded_and_an_unknown_one_keeps_its_fields[item2-  run s: proven earlier; intake file retired to g.xml.imported; run closed]`
  - `tests/test_render_payloads.py::test_the_import_proof_is_gated_on_the_verb_as_well_as_the_schema`

Old text:

```
    filed = f"intake file retired to {PurePath(str(retired)).name}" if retired else None
```

New text:

```
    filed = None
```

### `r678-a.A2_drop_the_import_proof_case`

the original defect for intake imported: render never asks for the proof

- File: `src/cratekit/cli/render.py`
- Source: `r678-a.json`, row `A2_drop_the_import_proof_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_render_payloads.py`, `tests/test_intake_imported.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`

Old text:

```
    lines += render_import_proof(envelope)

```

New text:

```
(empty)
```

### `u167.M20_session_state`

_landed: a session is taken whatever its state, open or refused

- File: `src/cratekit/analysis/rekordbox_check.py`
- Source: `u167.json`, row `M20_session_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`, `tests/test_sync_land.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            and record.state is session.SessionState.CLOSED
            and str(session.SourceState.COMMITTED) in record.sources.values()
        }
```

New text:

```
        }
```

### `u27-reports-round-1.S1_limit_floor`

Pass the limit through unfloored, so a negative one becomes a slice from the end

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S1_limit_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_negative_limit_is_read_as_zero_rather_than_as_a_slice_from_the_end`

Old text:

```
    limit = max(0, int(ctx.args.limit))
```

New text:

```
    limit = int(ctx.args.limit)
```

### `u27-reports-round-1.S2_truncation_row`

Drop the row that says the list was capped

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S2_truncation_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
    if len(listed) < len(report.uncovered):
        findings.append(
            Finding(
                key="coverage.truncated",
                title="the list above is not the whole answer",
                status=Status.INFO,
                detail=(
                    f"{len(listed)} of {len(report.uncovered)} uncovered tracks "
                    f"are listed; raise the limit to see the rest"
                ),
            )
        )

```

New text:

```
(empty)
```

### `u27-reports-round-1.S3_summary_total`

Derive the summary total from the truncated list, the arithmetic that hides the cap

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S3_summary_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_limit_of_zero_lists_nothing_and_still_counts_everything`
  - `tests/test_reports_cli.py::test_a_limit_that_drops_rows_says_so_and_still_reports_the_true_total`

Old text:

```
            "uncovered": len(report.uncovered),
```

New text:

```
            "uncovered": len(listed),
```

### `u27-reports-round-1.S6_lossy_marker`

Build the naming template without the configured lossy marker

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-1.json`, row `S6_lossy_marker`
- Moved: Anchored where u325-replay-after.json replayed it: U298 folded this template's strip, empty check and marker rule into naming.NameTemplate.lossy_if_marked, which it now returns; the plain template here drops the configured marker as before, local to this verb
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_rejected_pair_comes_back_suppressed_rather_than_as_a_question`
  - `tests/test_reports_cli.py::test_a_second_run_re_offers_the_same_item_rather_than_a_second_one`
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`

Old text:

```
    return NameTemplate.lossy_if_marked(cfg.naming.lossy_marker)
```

New text:

```
    return NameTemplate()
```

### `u27-reports-round-2.S5_handler_key_wrong`

Round 1's S5 was inert because the engine default matched; pass a WRONG key instead

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-2.json`, row `S5_handler_key_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_duplicates_offers_the_pair_into_the_queue_under_its_own_handler_key`
  - `tests/test_reports_cli.py::test_the_shell_passes_the_REGISTRY_key_rather_than_letting_the_engine_default`

Old text:

```
            view, store, template=_template(cfg), handler_key=ctx.entry.handler_key
```

New text:

```
            view, store, template=_template(cfg), handler_key="duplicates"
```

### `u27-reports-round-3-fixes.F1_as_of_falsiness`

Restore the falsiness test, so an explicitly empty as-of is read as an absent flag

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F1_as_of_falsiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_an_as_of_that_is_not_a_date_refuses_rather_than_answering_for_today[empty]`

Old text:

```
    if written is None:
```

New text:

```
    if not written:
```

### `u27-reports-round-3-fixes.F5_gap_row_flood`

Render one gap row per declared bucket again when the governed tree is absent

- File: `src/cratekit/cli/reports.py`
- Source: `u27-reports-round-3-fixes.json`, row `F5_gap_row_flood`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reports_cli.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_reports_cli.py::test_a_missing_tree_is_named_once_rather_than_as_a_row_per_bucket`

Old text:

```
    if stats.shape.folders == 0:
```

New text:

```
    if False:
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

### `u211.D3_kept_set_is_narrow`

KEPT_RUN_REASONS: rekordbox-running keeps its run as well

- File: `src/cratekit/cli/gates.py`
- Source: `u211.json`, row `D3_kept_set_is_narrow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`
- Collected: 229 against a baseline of 229
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
KEPT_RUN_REASONS: tuple[str, ...] = (processes.UNCONFIRMED,)
```

New text:

```
KEPT_RUN_REASONS: tuple[str, ...] = (processes.UNCONFIRMED, "rekordbox-running")
```

### `u48-author.P3_two_codes_collapsed_to_one`

One code over both conditions, which is the discriminator this unit split

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P3_two_codes_collapsed_to_one`
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
ARCHIVE_PURGE_FAILED = "archive-purge-failed"
```

New text:

```
ARCHIVE_PURGE_FAILED = "archive-listing-failed"
```

### `u258.M9_population_keeps_the_owners`

population_under_measurement: keep the two table owners, so every count in the at risk section is over a wider basis than its pins

- File: `tests/test_reserved_causes.py`
- Source: `u258.json`, row `M9_population_keeps_the_owners`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_parse_memo.py`
- Collected: 239 against a baseline of 239
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        for relative, source in sources
        if relative not in TABLE_OWNERS
    ]
```

New text:

```
        for relative, source in sources
    ]
```

### `u326.W1_children_reads_lists`

_children: skip a list field's nodes, so a walk never enters a body, an argument list or a target list

- File: `tests/_source_guards.py`
- Source: `u326.json`, row `W1_children_reads_lists`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 1593 against a baseline of 1593
- Kills: 150 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_the_csv_writer_guard_bites_and_stays_quiet_on_correct_code`
  - `tests/test_rb_writer_guard.py::test_a_conditional_defaulting_the_marker_fires_and_a_summary_string_does_not`
  - `tests/test_rb_writer_guard.py::test_a_presence_flag_is_not_a_marker_holder`
  - `tests/test_rb_writer_guard.py::test_defining_the_marker_on_a_row_double_is_not_reading_it`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[except as-    try:\n        pass\n    except ValueError as TABLE:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[for target-    for TABLE, _ in rows:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[nested unpacking-    (a, [TABLE, b]) = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[plain assignment-    TABLE = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[tuple unpacking-    TABLE, meta = rows[0]\n    return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_every_way_of_shadowing_a_lookup_table_still_fires[with as-    with rows as TABLE:\n        return TABLE.get(COLUMN, 0)\n]`
  - `tests/test_rb_writer_guard.py::test_only_the_declared_modules_read_the_soft_delete_marker_at_all`
  - `tests/test_rb_writer_guard.py::test_the_launder_rules_reach_a_class_body_and_a_nonlocal_rebinding`
  - `tests/test_rb_writer_guard.py::test_the_lookup_table_exclusion_is_not_an_evasion_route`
  - `tests/test_rb_writer_guard.py::test_the_lookup_table_exclusion_is_scope_aware_not_just_name_keyed`
  - `tests/test_rb_writer_guard.py::test_the_soft_delete_guard_catches_a_read_laundered_one_line_later`
  - ... and 135 more, see the JSON sidecar

Old text:

```
            found.extend([item for item in value if isinstance(item, _AST)])
```

New text:

```
            pass
```

### `u326.W2_cache_by_identity`

_walk: hand back the held walk for any module once one is held, so a second module is answered from the first

- File: `tests/_source_guards.py`
- Source: `u326.json`, row `W2_cache_by_identity`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py`, `tests/test_rb_writer_guard.py`, `tests/test_review_queue.py`, `tests/test_cli_contract.py`
- Collected: 1593 against a baseline of 1593
- Kills: 143 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[acquire.fallback-fetch]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[acquire.fallback]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[audit.duplicates]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[delete.review]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.identify]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.missing]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.playlist]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[intake.set]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.approved]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.harvest]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.held]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.import]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.judge]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[label.sync]`
  - `tests/test_cli_contract.py::test_conformance_4_adjudication_goes_through_the_review_queue[match.run]`
  - ... and 128 more, see the JSON sidecar

Old text:

```
    if not (_LAST_MODULE_WALK and _LAST_MODULE_WALK[0] is node):
```

New text:

```
    if not _LAST_MODULE_WALK:
```

### `u125.P2_drop_slug`

Remove cancelled from PINNED_NON_RESERVED_CAUSES while the tree still declares it

- File: `tests/_pinned_reserved_populations.py`
- Source: `u125.json`, row `P2_drop_slug`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`, `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
- Collected: 2 against a baseline of 2
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
    'canary-read-failed',
    'cancelled',
    'catalog-tree-undeclared',

```

New text:

```
    'canary-read-failed',
    'catalog-tree-undeclared',

```

### `u296.M19_pin_in_the_wrong_file`

read_package_pins: accept a module pinned in another package's file, so a pin can sit where nobody looks for it

- File: `tests/_pinned_reserved_populations.py`
- Source: `u296.json`, row `M19_pin_in_the_wrong_file`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_pins_reader.py`, `tests/test_reserved_causes.py`
- Collected: 235 against a baseline of 235
- Kills: 2 (killed)
- Killed:
  - `tests/test_reserved_pins_reader.py::test_a_frozenset_table_is_read_by_its_members`
  - `tests/test_reserved_pins_reader.py::test_a_module_pinned_in_another_packages_file_is_refused`

Old text:

```
                if owner != package:
```

New text:

```
                if False:
```

### `u296.M20_unknown_pin_table`

read_package_pins: ignore a table it does not know, so a misspelt table silently stops pinning

- File: `tests/_pinned_reserved_populations.py`
- Source: `u296.json`, row `M20_unknown_pin_table`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_reserved_pins_reader.py`, `tests/test_reserved_causes.py`
- Collected: 235 against a baseline of 235
- Kills: 1 (killed)
- Killed:
  - `tests/test_reserved_pins_reader.py::test_a_table_the_reader_does_not_know_is_refused_rather_than_ignored`

Old text:

```
        if unknown:
            raise ValueError
```

New text:

```
        if False:
            raise ValueError
```

### `r592-a.A1_occupancy_guard_removed`

assert_recovery_target: find nothing occupied whatever the target holds, so a library whose database sits where this one lands is replaced unasked

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A1_occupancy_guard_removed`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = []
```

### `r592-a.A2_database_dropped_from_fileset`

recovered_database_fileset: return the companions only, so a database already at the landing path is not an occupied target

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A2_database_dropped_from_fileset`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return companions
```

### `r592-a.A4_fileset_not_rebased`

recovered_database_fileset: land the database at its bare name at the top of the target for every layout, so the guard tests a path the transfer never writes

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A4_fileset_not_rebased`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 4 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
        landing = target / database.relative_to(cfg.library.root)
    except ValueError:
```

New text:

```
        landing = target / database.name
    except ValueError:
```

### `r592-a.A5_replacing_existing_inverted`

assert_recovery_target: refuse an occupied target only when it WAS named for replacement

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A5_replacing_existing_inverted`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 8 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_is_the_library_plan_moved_and_nothing_else`
  - `tests/test_restore.py::test_u95_a_bare_metal_plan_never_reads_the_capture_the_refused_library_holds`
  - `tests/test_restore.py::test_u95_a_bare_metal_session_plans_and_runs_entirely_under_its_target`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_library_is_refused_under_a_bare_metal_session`
  - `tests/test_restore.py::test_u95_a_plan_built_for_the_target_is_refused_under_a_library_session`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if existing and replacing_existing:
```

### `r592-a.A6_old_suffix_rule_restored`

assert_recovery_target: put the recursive any-database rule back, the behaviour R-592 records, so every interrupted recovery is refused on rerun

- File: `src/cratekit/core/restore_recovery.py`
- Source: `r592-a.json`, row `A6_old_suffix_rule_restored`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 253 against a baseline of 253
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_opens_over_databases_it_would_not_replace`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`

Old text:

```
    existing = [entry for entry in recovered_database_fileset(cfg, where) if entry.exists()]
```

New text:

```
    existing = sorted(entry for entry in where.rglob("*.db") if entry.is_file())
```

### `r338-c.C4_bare_metal_asks_about_the_share`

recover_under_bare_metal_session: let the plan ask the remote about a share the skipped database half will never pull

- File: `src/cratekit/session/restore_cli.py`
- Source: `r338-c.json`, row `C4_bare_metal_asks_about_the_share`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                pull_share=False,
```

New text:

```
                pull_share=True,
```

### `r592-b.B1_step_on_every_failure`

_half_failed: give the removal step to a mirror failure too, sending a person to delete files the mirror never lands

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B1_step_on_every_failure`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not dry_run and half == DATABASE_HALF:
```

New text:

```
    if not dry_run:
```

### `r592-b.B2_step_on_the_wrong_half`

_half_failed: give the removal step to the mirror half and not the database half, so a database half that landed part of the fileset says nothing about it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B2_step_on_the_wrong_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not dry_run and half == DATABASE_HALF:
```

New text:

```
    if not dry_run and half == MIRROR_HALF:
```

### `r592-b.B4_step_names_the_wrong_directory`

rerun_step: name the target rather than the directory the database lands in, so the person looks for it in the wrong place

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B4_step_names_the_wrong_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        f"companion of it in {database_target.parent} if one is there, because a "
```

New text:

```
        f"companion of it in {database_target.parent.parent} if one is there, because a "
```

### `r592-b.B5_step_names_no_file`

rerun_step: say the database rather than its file name, so the step does not say which file to remove

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B5_step_names_no_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
        f"before running the recovery again, remove {database_target.name} and any "
```

New text:

```
        f"before running the recovery again, remove the database and any "
```

### `r592-b.B7_sample_halves_split`

SAMPLE, existing guard: _halves hands the whole plan to the mirror half, so a failed mirror lands the database behind it

- File: `src/cratekit/session/restore_cli.py`
- Source: `r592-b.json`, row `B7_sample_halves_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    mirror = tuple(c for c in decided.commands if c.label == backup.RESTORE_MIRROR)
```

New text:

```
    mirror = tuple(decided.commands)
```

### `u96-a.A12_which_half_failed`

_half_failed: swap the two failure sentences, so a failed mirror is reported as a failed database half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A12_which_half_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    elif half == MIRROR_HALF:
        message = (
```

New text:

```
    elif half == DATABASE_HALF:
        message = (
```

### `u96-a.A13_completed_halves_recorded`

Never record a completed half, so a database failure does not say the mirror arrived

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A13_completed_halves_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 1 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`

Old text:

```
            completed.append(half)
```

New text:

```
            pass
```

### `u96-a.A15_report_names_where_the_database_is`

_recovered: always report the rebased database path, so a database that was never recovered is reported at the top of the target

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A15_report_names_where_the_database_is`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            "database_target": str(report.database_elsewhere or report.database_target),
```

New text:

```
            "database_target": str(report.database_target),
```

### `u96-a.A16_no_absent_companion_for_a_half_that_did_not_run`

Report the plan's absent companions even when the database half was skipped

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A16_no_absent_companion_for_a_half_that_did_not_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            absent=decided.absent_sidecars if elsewhere is None else (),
```

New text:

```
            absent=decided.absent_sidecars,
```

### `u96-a.A4_run_inside_the_held_session`

Drop gates=held.guard from the run_restore call of each half

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A4_run_inside_the_held_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
                    portion,
                    cfg,
                    dry_run=dry_run,
                    gates=held.guard,
```

New text:

```
                    portion,
                    cfg,
                    dry_run=dry_run,
```

### `u96-a.A5_the_mirror_is_pulled`

Plan with include_mirror=False, so a recovery onto an empty drive brings a database and no music

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A5_the_mirror_is_pulled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
                include_mirror=True,
```

New text:

```
                include_mirror=False,
```

### `u96-a.A6_a_half_at_a_time`

_halves: put every command in the mirror half, which is spending the plan whole, so a failed mirror still lands the database

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A6_a_half_at_a_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 94 against a baseline of 94
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
    mirror = tuple(c for c in decided.commands if c.label == backup.RESTORE_MIRROR)
```

New text:

```
    mirror = decided.commands
```

### `u96-a.A8_database_elsewhere_is_skipped`

Run the database half even when the configured database was never on the lost volume

- File: `src/cratekit/session/restore_cli.py`
- Source: `u96-a.json`, row `A8_database_elsewhere_is_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            if half == DATABASE_HALF and elsewhere is not None:
```

New text:

```
            if False:
```

### `r592-b.B6_restore_mirror_carries_the_database`

_plan_restore_inside_the_gates: exclude volume clutter only from the restore mirror, so a mirror still holding the database lands it where the database half writes

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r592-b.json`, row `B6_restore_mirror_carries_the_database`
- Moved: Anchored where u311-replay-after-b.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_backup_cli.py`, `tests/test_restore.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(_mirror_excludes(cfg)),
```

New text:

```
                    rclone, "copy", str(cfg.backup.dest), str(target),
                    *_exclude_args(VOLUME_EXCLUDES),
```

### `u96-b.C3_engine_occupied_target`

SAMPLE. assert_recovery_target: disarm the refusal of a target that already holds a database

- File: `src/cratekit/core/restore_recovery.py`
- Source: `u96-b.json`, row `C3_engine_occupied_target`
- Moved: Anchored where u300-replay-after-c.json replayed it: the same text, now in src/cratekit/core/restore_recovery.py, was in src/cratekit/core/restore.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore_cli.py`, `tests/test_restore.py`
- Collected: 253 against a baseline of 253
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_holding_a_library_in_a_subdirectory`
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore_cli.py::test_a_target_that_already_holds_a_database_is_refused_with_no_way_to_name_it`

Old text:

```
    if existing and not replacing_existing:
```

New text:

```
    if False:
```

### `u169.N6_repair_apply_bypasses`

repair paths --apply: take a relative root as it is

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u169.json`, row `N6_repair_apply_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/intake/test_repair_apply.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_root_option.py::test_repair_apply_reads_a_relative_root_against_the_library_root`

Old text:

```
        naming_cli.root_path(ctx.args.root, cfg, verb="repair paths --apply")
```

New text:

```
        Path(ctx.args.root)
```

### `u169.N1_relative_read_against_cwd`

root_path: take a relative root as it is, read under the working directory, the base's reading

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N1_relative_read_against_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_root_option.py::test_a_missing_relative_root_refuses_naming_the_path_it_tried`
  - `tests/test_root_option.py::test_a_relative_root_is_read_against_the_library_root`
  - `tests/test_root_option.py::test_name_apply_reads_a_relative_root_inside_the_library`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`
  - `tests/test_root_option.py::test_repair_apply_reads_a_relative_root_against_the_library_root`
  - `tests/test_root_option.py::test_repair_paths_scans_a_relative_root_inside_the_library`

Old text:

```
    return named if named.is_absolute() else library / named
```

New text:

```
    return named
```

### `u169.N3_missing_folder_accepted`

root_folder: accept a folder that is not there

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N3_missing_folder_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_root_option.py::test_a_file_where_the_folder_should_be_is_refused`
  - `tests/test_root_option.py::test_a_missing_absolute_root_refuses_naming_it`
  - `tests/test_root_option.py::test_a_missing_library_root_is_refused_when_no_root_was_given`
  - `tests/test_root_option.py::test_a_missing_relative_root_refuses_naming_the_path_it_tried`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`
  - `tests/test_root_option.py::test_repair_paths_refuses_a_root_with_no_folder`

Old text:

```
    if tried.is_dir():
        return tried
```

New text:

```
    if True:
        return tried
```

### `u169.N4_name_apply_bypasses`

name apply: read --root as the base did, bypassing the helper

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N4_name_apply_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_name_apply_reads_a_relative_root_inside_the_library`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`

Old text:

```
    root = root_folder(ctx.args.root, cfg, verb="name apply")
```

New text:

```
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
```

### `u89.C1_converge_threshold`

converge _compare: pass None instead of the loaded cut

- File: `src/cratekit/cli/converge.py`
- Source: `u89.json`, row `C1_converge_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_is_converge_not_comparing_rather_than_a_match`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`

Old text:

```
            vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
            vocal_threshold=None,
```

### `u132.W5_rebuild_note`

The rebuild resume carries no skipped step note

- File: `src/cratekit/cli/rebuild.py`
- Source: `u132.json`, row `W5_rebuild_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`

Old text:

```
            *engine.favorites_skipped_warnings(declared, driven),

```

New text:

```
(empty)
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

### `u155.R4_genre_sub_named`

genre_sub_named: answer False, so a gate shows the genre sub as the energy sub

- File: `src/cratekit/core/routing.py`
- Source: `u155.json`, row `R4_genre_sub_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    return _genre_sub_by_id(taxonomy.bucket(bucket_id), sub_id) is not None
```

New text:

```
    return False
```

### `r316.M11_warning_ignores_dimension`

not_compared_warnings warns whatever the gaps say, so a taxonomy with no vocal dimension is warned about

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M11_warning_ignores_dimension`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[above]`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[below]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface`
  - `tests/test_routing_workers.py::test_the_warning_code_is_the_locked_spelling`

Old text:

```
    if VOCAL_DIMENSION not in tuple(not_compared):
        return ()

```

New text:

```
(empty)
```

### `r316.M3_inbox_gaps_leak_into_totals`

route_inbox reads the gaps without taking them out of the result, so they ride in the plan totals

- File: `src/cratekit/write/routing_cli.py`
- Source: `r316.json`, row `M3_inbox_gaps_leak_into_totals`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`

Old text:

```
    not_compared = result.pop("not_compared", ())
```

New text:

```
    not_compared = result.get("not_compared", ())
```

### `r691.F2_trees_left_off`

the trees the write goes into are left off the screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F2_trees_left_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`

Old text:

```
        "trees": list(plan.native),

```

New text:

```
        "trees": [],

```

### `r691.F3_planner_warnings_dropped_from_facts`

the planner's warnings stay off the screen, so a library with nothing native shows empty destinations and no reason

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F3_planner_warnings_dropped_from_facts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_empty_inbox_with_no_native_tree_answers_inbox_empty_with_the_remedy`
  - `tests/test_routing_workers.py::test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer`

Old text:

```
        "not derived": list(plan.gaps),
        "warnings": [warning["message"] for warning in plan.warnings],

```

New text:

```
        "not derived": list(plan.gaps),
        "warnings": [],

```

### `r691.F4_gaps_dropped_from_facts`

the dimensions not derived stay off the database gate's screen

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F4_gaps_dropped_from_facts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`

Old text:

```
        "not derived": list(plan.gaps),
        "warnings": [warning["message"] for warning in plan.warnings],

```

New text:

```
        "not derived": [],
        "warnings": [warning["message"] for warning in plan.warnings],

```

### `r691.K2_gaps_not_carried_to_the_apply`

the apply reports nothing as not compared, the R-316 shape, now that the derivation happened on the plan

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `K2_gaps_not_carried_to_the_apply`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`
  - `tests/test_routing_workers.py::test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox`

Old text:

```
        "not_compared": planned.gaps,

```

New text:

```
        "not_compared": (),

```

### `r691.N3_declined_envelope_drops_the_warning`

the declined answer drops the planner's warning, so a reader of the JSON after an abort cannot learn why every destination is empty

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `N3_declined_envelope_drops_the_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_long_track_playlist_gets_the_review_alone_as_its_remedy`
  - `tests/test_routing_workers.py::test_the_database_gate_on_a_library_with_no_native_tree_says_so_before_the_answer`

Old text:

```
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,
        )

```

New text:

```
        return ctx.envelope(
            data=_plan(items, kind="inbox", applied=False),
            outcome=Outcome.NO_OP,
        )

```

### `r691.N4_inbox_empty_envelope_drops_the_warning`

the inbox-empty answer drops the planner's warning, so the screen and the answer name different reasons for one state

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `N4_inbox_empty_envelope_drops_the_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_long_track_playlist_gets_the_review_alone_as_its_remedy`
  - `tests/test_routing_workers.py::test_an_empty_inbox_with_no_native_tree_answers_inbox_empty_with_the_remedy`
  - `tests/test_routing_workers.py::test_the_remedy_names_the_long_track_playlist_the_active_copy_declares`

Old text:

```
            data=_plan(items, kind="inbox", applied=False, reason="inbox-empty"),
            outcome=Outcome.NO_OP,
            warnings=planned.warnings,

```

New text:

```
            data=_plan(items, kind="inbox", applied=False, reason="inbox-empty"),
            outcome=Outcome.NO_OP,

```

### `r691.P1_destination_left_off_the_item`

each item is listed with no destination, the defect R-691 recorded: a person answers a placement they cannot read

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `P1_destination_left_off_the_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_apply_files_the_track_where_the_gate_said`
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`

Old text:

```
            "destination": destined.get(str(path), ""),
            "vocal": vocal.get(str(path), ""),

```

New text:

```
            "destination": "",
            "vocal": vocal.get(str(path), ""),

```

### `r691.P2_vocal_left_off_the_item`

the vocal sub a track also files into is left off the item

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `P2_vocal_left_off_the_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_apply_files_the_track_where_the_gate_said`
  - `tests/test_routing_workers.py::test_the_database_digest_binds_the_destinations_not_the_file_list`

Old text:

```
            "destination": destined.get(str(path), ""),
            "vocal": vocal.get(str(path), ""),

```

New text:

```
            "destination": destined.get(str(path), ""),
            "vocal": "",

```

### `r691.W1_write_ignores_the_plan`

the write takes no placement from the plan, so the confirmed apply files nothing where the screen said it would

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `W1_write_ignores_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 22 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[above]`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[below]`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_a_second_calibrated_inbox_creates_no_second_vocal_sub`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface`
  - `tests/test_routing_workers.py::test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            placements = planned.placements[tree_id]

```

New text:

```
            placements = ()

```

### `u53-routing-and-rebuild-workers.A3_empty_folder_shortcircuit_removed`

A confirmed apply over an empty intake folder derives and opens a database rather than stopping

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `A3_empty_folder_shortcircuit_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_an_empty_folder_opens_nothing`
  - `tests/test_routing_workers.py::test_an_empty_inbox_with_no_native_tree_answers_inbox_empty_with_the_remedy`

Old text:

```
    if not items:
        # AN EMPTY FOLDER IS NOT A WRITE.
```

New text:

```
    if False:
        # AN EMPTY FOLDER IS NOT A WRITE.
```

### `u53-routing-and-rebuild-workers.A5_applied_always_true`

Every apply reports itself as having applied, whatever it did

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `A5_applied_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`

Old text:

```
        outcome=Outcome.OK if result["applied"] else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u53-routing-and-rebuild-workers.R1_resort_drives_a_foreign_job`

The resort drives any queued job of any verb under its own envelope

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R1_resort_drives_a_foreign_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_resume_drives_another_verbs_job[resort]`

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

### `u86-b.E22_export_remedy`

Drop the warning that names --export on the database path

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86-b.json`, row `E22_export_remedy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_without_export_a_library_with_no_native_tree_names_the_export_remedy`

Old text:

```
            if result["reason"] == "no-native-tree"
```

New text:

```
            if False
```

### `u86-b.E23_export_branch`

Ignore --export and take the disk folder path

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86-b.json`, row `E23_export_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 57 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not`
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none`
  - `tests/test_routing_workers.py::test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_export_before_the_plan`
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served`
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_lone_unrated_track_with_energy_is_owed_one_rating`
  - `tests/test_routing_workers.py::test_a_long_track_alone_is_a_change_and_writes_a_file`
  - `tests/test_routing_workers.py::test_a_missing_duration_is_counted_not_guessed`
  - `tests/test_routing_workers.py::test_a_native_routing_tree_refuses_before_the_plan_is_offered`
  - `tests/test_routing_workers.py::test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced`
  - `tests/test_routing_workers.py::test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated`
  - `tests/test_routing_workers.py::test_a_same_named_playlist_inside_a_folder_is_not_hijacked`
  - ... and 42 more, see the JSON sidecar

Old text:

```
    if ctx.args.export:
        return route_inbox_export(ctx, cfg, Path(ctx.args.export))
```

New text:

```
(empty)
```

### `u89.W1_resort_worker`

handle_resort: hand the engine None instead of the loaded cut

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89.json`, row `W1_resort_worker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
        workflow=RESORT_WORKFLOW,
        # THE CALIBRATED CUT, through the one loader, at the path the frozen
        # configuration names. None on a library never calibrated (U89, D7).
        vocal_threshold=metadata_cli.load_vocal_threshold(cfg),
```

New text:

```
        workflow=RESORT_WORKFLOW,
        vocal_threshold=None,
```

### `u91.U14_no_native_warning`

route_unplaced: drop the warning that names --export on a library with nothing native

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U14_no_native_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_without_the_flag_nothing_is_written_and_the_answer_names_the_flag`

Old text:

```
            if totals["reason"] == "no-native-tree"
            else []
```

New text:

```
            if False
            else []
```

### `u91.U15_export_branch`

route_unplaced: ignore --export and answer the report

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U15_export_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 18 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates`
  - `tests/test_routing_workers.py::test_a_cut_over_tree_refuses_the_sweep_and_writes_nothing`
  - `tests/test_routing_workers.py::test_a_missing_genre_folder_is_a_skipped_write_and_no_folder_is_invented`
  - `tests/test_routing_workers.py::test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing`
  - `tests/test_routing_workers.py::test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it`
  - `tests/test_routing_workers.py::test_a_second_sweep_over_its_own_output_places_nothing`
  - `tests/test_routing_workers.py::test_a_sweep_that_could_place_nothing_is_blocked_not_done`
  - `tests/test_routing_workers.py::test_a_track_held_only_in_a_vocal_sub_is_placed`
  - `tests/test_routing_workers.py::test_a_track_held_only_outside_the_tree_is_unplaced`
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_refuses[a-playlist-of-that-name]`
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_refuses[absent]`
  - `tests/test_routing_workers.py::test_an_unmounted_library_refuses_the_sweep`
  - `tests/test_routing_workers.py::test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created`
  - `tests/test_routing_workers.py::test_an_unreadable_track_is_a_warning_and_the_rest_are_placed`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    if ctx.args.export:
        return route_unplaced_export(ctx, cfg, Path(ctx.args.export))
```

New text:

```
    if False:
        return route_unplaced_export(ctx, cfg, Path(ctx.args.export))
```

### `r686.E1_tracks_counts_every_item`

tracks counts created playlists as tracks

- File: `src/cratekit/write/routing_export.py`
- Source: `r686.json`, row `E1_tracks_counts_every_item`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        "tracks": len(tracks),

```

New text:

```
        "tracks": len(items),

```

### `r686.E2_routed_counts_vocal`

routed is counted off the vocal column instead of the destination

- File: `src/cratekit/write/routing_export.py`
- Source: `r686.json`, row `E2_routed_counts_vocal`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_gate_counts_tracks_filed_into_a_genre_sub`

Old text:

```
        "routed": sum(1 for item in tracks if item["destination"]),

```

New text:

```
        "routed": sum(1 for item in tracks if item["vocal"]),

```

### `r686.E4_long_tracks_intake_only`

long tracks counts only the first track's membership

- File: `src/cratekit/write/routing_export.py`
- Source: `r686.json`, row `E4_long_tracks_intake_only`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        "long tracks": sum(1 for item in tracks if item["long_track"]),

```

New text:

```
        "long tracks": sum(1 for item in tracks[:1] if item["long_track"]),

```

### `r686.E5_warnings_dropped`

The planner's warnings stay off the screen

- File: `src/cratekit/write/routing_export.py`
- Source: `r686.json`, row `E5_warnings_dropped`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
        "warnings": [warning["message"] for warning in warnings],

```

New text:

```
        "warnings": [],

```

### `r686.E6_gaps_dropped`

The dimensions not derived stay off the screen

- File: `src/cratekit/write/routing_export.py`
- Source: `r686.json`, row `E6_gaps_dropped`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`

Old text:

```
        "not derived": list(gaps),

```

New text:

```
        "not derived": [],

```

### `r686.E7_subs_not_named`

The created vocal subs are left off the screen

- File: `src/cratekit/write/routing_export.py`
- Source: `r686.json`, row `E7_subs_not_named`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        "vocal subs created": list(vox_created),

```

New text:

```
        "vocal subs created": [],

```

### `r688.B1_owed_rating_blocks_the_answer`

an owed rating turns a run with nothing to route into route-blocked, which no run of this medium can ever clear

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `B1_owed_rating_blocks_the_answer`
- Moved: Anchored where u302-replay-after-a.json replayed it: the inbox export route now sits in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py, and names its answer through the shared _route_reason helper
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`

Old text:

```
    reason = _route_reason(destination, warnings)
    warnings += unrated

```

New text:

```
    reason = _route_reason(destination, warnings)
    warnings += unrated
    if unrated and reason == "nothing-to-route":
        reason = "route-blocked"

```

### `r688.C1_rates_flag_ignored`

a bucket declared rates = false is counted as owed a rating

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `C1_rates_flag_ignored`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_the_rating_rule_skips_is_filed_and_not_owed[bucket-does-not-rate]`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        if not routing.rates(declared, placement.bucket):
            continue

```

New text:

```
        pass

```

### `r688.C2_no_energy_counted`

a track with no energy reading is counted as owed a rating it has no value for

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `C2_no_energy_counted`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_the_rating_rule_skips_is_filed_and_not_owed[no-energy-reading]`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        if routing.energy_rating(declared, energy.get(placement.location)) is None:

```

New text:

```
        if routing.energy_rating(declared, energy.get(placement.location)) == -1:

```

### `r688.G1_zero_owed_still_warns`

a run that owes no rating still carries the owed rating warning, so every export run warns

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `G1_zero_owed_still_warns`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_row_with_no_rating_attribute_is_not_counted_as_owed`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_track_the_rating_rule_skips_is_filed_and_not_owed[bucket-does-not-rate]`
  - `tests/test_routing_workers.py::test_a_track_the_rating_rule_skips_is_filed_and_not_owed[no-energy-reading]`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`
  - `tests/test_routing_workers.py::test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_screen_says_none_for_an_empty_warning_list`

Old text:

```
    if not owed:
        return []

```

New text:

```
    if owed < 0:
        return []

```

### `r688.G2_count_off_by_one`

the warning names one row more than the count the planner returned

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `G2_count_off_by_one`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 7 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_lone_unrated_track_with_energy_is_owed_one_rating`
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        "message": f"{owed} intake row(s) are owed a star rating from energy and "

```

New text:

```
        "message": f"{owed + 1} intake row(s) are owed a star rating from energy and "

```

### `r688.N1_long_track_change_not_a_write`

a run whose only change is the long track playlist writes no file, existing guard sampled

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `N1_long_track_change_not_a_write`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_long_track_alone_is_a_change_and_writes_a_file`

Old text:

```
    if not report.inserted and not lengthened and not vox_created:

```

New text:

```
    if not report.inserted and not vox_created:

```

### `r688.U1_hand_rated_counted`

a rating a person set is counted as owed, existing guard sampled

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `U1_hand_rated_counted`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
    return value is not None and value.strip() in ("", "0")

```

New text:

```
    return value is not None

```

### `r688.U2_missing_attribute_counted`

a row with no Rating attribute is counted as owed, existing guard sampled

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `U2_missing_attribute_counted`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_with_no_rating_attribute_is_not_counted_as_owed`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`
  - `tests/test_routing_workers.py::test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_screen_says_none_for_an_empty_warning_list`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
    return value is not None and value.strip() in ("", "0")

```

New text:

```
    return value is None or value.strip() in ("", "0")

```

### `r688.U3_empty_rating_not_unrated`

an empty Rating stops reading as nobody rated this, existing guard sampled

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `U3_empty_rating_not_unrated`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
    return value is not None and value.strip() in ("", "0")

```

New text:

```
    return value is not None and value.strip() in ("0",)

```

### `r688.V1_applied_envelope_drops_warning`

the applied run's envelope loses the owed rating warning, so the ratings nobody wrote go unsaid

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `V1_applied_envelope_drops_warning`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_lone_unrated_track_with_energy_is_owed_one_rating`
  - `tests/test_routing_workers.py::test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
    warnings += unrated

```

New text:

```
    warnings += []

```

### `r688.V2_gate_drops_warning`

the gate's screen loses the owed rating warning, so a person answers without reading it

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `V2_gate_drops_warning`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_no_rating_and_says_which_are_owed`

Old text:

```
    facts = _export_facts(items, export, gaps, vox_created, [*warnings, *unrated])

```

New text:

```
    facts = _export_facts(items, export, gaps, vox_created, warnings)

```

### `r688.V3_declined_envelope_drops_warning`

the declined run's envelope loses the owed rating warning

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `V3_declined_envelope_drops_warning`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`

Old text:

```
            warnings=[*warnings, *unrated],

```

New text:

```
            warnings=warnings,

```

### `r688.W1_rating_written_again`

the export writer patches a rating onto every routed row again, the defect R-688 recorded: a write the import never lands

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `W1_rating_written_again`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_an_analysed_track_keeps_its_rating_and_its_grid`
  - `tests/test_routing_workers.py::test_an_owed_star_rating_is_not_written_into_the_export`
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
    lengthened, long_warning = 0, None

```

New text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
    trees.apply_rating_changes({key: 255 for keys in plan.values() for key in keys}, buffer)
    lengthened, long_warning = 0, None

```

### `r691.F1_routed_counts_vocal`

routed is counted off the vocal column instead of the destination, on both gates

- File: `src/cratekit/write/routing_export.py`
- Source: `r691.json`, row `F1_routed_counts_vocal`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_gate_prints_the_destination_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_gate_counts_tracks_filed_into_a_genre_sub`

Old text:

```
        "routed": sum(1 for item in tracks if item["destination"]),
        "vocal": sum(1 for item in tracks if item["vocal"]),

```

New text:

```
        "routed": sum(1 for item in tracks if item["vocal"]),
        "vocal": sum(1 for item in tracks if item["vocal"]),

```

### `r691.P4_digest_over_the_file_list`

the digest is taken over the file list alone, the other half of the defect: a decision recorded against it stays valid while the routing under it changes

- File: `src/cratekit/write/routing_export.py`
- Source: `r691.json`, row `P4_digest_over_the_file_list`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_digest_binds_the_destinations_not_the_file_list`

Old text:

```
    digest = digest_of({"kind": kind, "items": items})

```

New text:

```
    digest = digest_of({
        "kind": kind,
        "items": [
            {k: v for k, v in item.items() if k in ("path", "name", "track_id")}
            for item in items
        ],
    })

```

### `u302.W5_blocked_sweep_reads_as_filed`

_route_reason: a sweep that skipped a write answers nothing-to-route

- File: `src/cratekit/write/routing_export.py`
- Source: `u302.json`, row `W5_blocked_sweep_reads_as_filed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 6 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing`
  - `tests/test_routing_workers.py::test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced`
  - `tests/test_routing_workers.py::test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated`
  - `tests/test_routing_workers.py::test_a_sweep_that_could_place_nothing_is_blocked_not_done`
  - `tests/test_routing_workers.py::test_an_export_whose_every_file_is_unreadable_is_blocked_not_already_filed`
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_is_blocked_not_already_filed`

Old text:

```
    if warnings:
        return "route-blocked"
```

New text:

```
    if False:
        return "route-blocked"
```

### `u302.W6_written_sweep_gets_a_reason`

_route_reason: a sweep that wrote its file is still given a reason it wrote none

- File: `src/cratekit/write/routing_export.py`
- Source: `u302.json`, row `W6_written_sweep_gets_a_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 11 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing`
  - `tests/test_routing_workers.py::test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced`
  - `tests/test_routing_workers.py::test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated`
  - `tests/test_routing_workers.py::test_a_second_export_run_over_its_own_output_inserts_nothing`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_a_second_sweep_over_its_own_output_places_nothing`
  - `tests/test_routing_workers.py::test_a_sweep_that_could_place_nothing_is_blocked_not_done`
  - `tests/test_routing_workers.py::test_an_export_whose_every_file_is_unreadable_is_blocked_not_already_filed`
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_is_blocked_not_already_filed`
  - `tests/test_routing_workers.py::test_the_export_vocal_subs_are_created_once`

Old text:

```
    if destination is not None:
        return None
    if warnings:
```

New text:

```
    if destination is None:
        return None
    if warnings:
```

### `u53-routing-and-rebuild-workers.U1_unplaced_constant_empty`

Unplaced reports nothing whatever the library holds, which is the defect verbatim

- File: `src/cratekit/write/routing_export.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U1_unplaced_constant_empty`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_does_not_report_a_row_rekordbox_removed`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[encrypted]`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds[native]`
  - `tests/test_routing_workers.py::test_unplaced_reports_with_rekordbox_open_and_writes_nothing`

Old text:

```
    items = [
        {"content_id": row.content_id, "path": row.recorded}
        for row in active
        if row.content_id not in held
    ]
```

New text:

```
    items = []
```

### `u53-routing-and-rebuild-workers.U2_compared_true_without_a_tree`

A library with nothing native reports an empty answer as a comparison it made

- File: `src/cratekit/write/routing_export.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U2_compared_true_without_a_tree`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_says_when_it_could_not_compare`
  - `tests/test_routing_workers.py::test_without_the_flag_nothing_is_written_and_the_answer_names_the_flag`

Old text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
```

New text:

```
        return [], {"compared": True, "reason": None, "collection": 0}
```

### `u53-routing-and-rebuild-workers.U3_held_never_populated`

Nothing is read out of the tree, so every row in the library reports as unplaced

- File: `src/cratekit/write/routing_export.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U3_held_never_populated`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_over_a_fully_placed_library_reports_none`

Old text:

```
            for node in rebuild.read_tree(handle, root_id):
                held |= set(node.content_ids)
```

New text:

```
            rebuild.read_tree(handle, root_id)
```

### `u53-routing-and-rebuild-workers.U4_tombstones_reported`

A row rekordbox removed is reported as a track still waiting to be filed

- File: `src/cratekit/write/routing_export.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U4_tombstones_reported`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_does_not_report_a_row_rekordbox_removed`

Old text:

```
    active = [row for row in rows if not row.deleted]
```

New text:

```
    active = list(rows)
```

### `u53-zero-rows-remeasured.I1_native_filter_dropped`

A resort queues an item for a tree still on the bridge, which no rebuild can write

- File: `src/cratekit/write/routing_export.py`
- Source: `u53-zero-rows-remeasured.json`, row `I1_native_filter_dropped`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_neither_queued_verb_takes_an_item_for_a_tree_still_on_the_bridge[resort]`

Old text:

```
    return tuple(sorted(t for t in entries.tree_ids() if entries.is_database_native(t)))
```

New text:

```
    return tuple(sorted(entries.tree_ids()))
```

### `u86-b.E14_non_creating_writer`

Use the creating writer, so a sub the curated tree lacks is invented

- File: `src/cratekit/write/routing_export.py`
- Source: `u86-b.json`, row `E14_non_creating_writer`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_export_sub_that_does_not_exist_is_a_warning_and_nothing_is_created`

Old text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
```

New text:

```
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
```

### `u86-b.E16_never_in_place`

Write the output over the export it read

- File: `src/cratekit/write/routing_export.py`
- Source: `u86-b.json`, row `E16_never_in_place`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 32 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not`
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none`
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_long_track_alone_is_a_change_and_writes_a_file`
  - `tests/test_routing_workers.py::test_a_missing_duration_is_counted_not_guessed`
  - `tests/test_routing_workers.py::test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced`
  - `tests/test_routing_workers.py::test_a_same_named_playlist_inside_a_folder_is_not_hijacked`
  - `tests/test_routing_workers.py::test_a_second_export_run_over_its_own_output_inserts_nothing`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_a_template_declaring_no_long_track_playlist_builds_none`
  - `tests/test_routing_workers.py::test_a_track_is_never_removed_from_the_playlist`
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`
  - `tests/test_routing_workers.py::test_a_track_the_rating_rule_skips_is_filed_and_not_owed[bucket-does-not-rate]`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    destination = export.with_name(export.stem + ROUTED_SUFFIX)
```

New text:

```
    destination = export
```

### `u86.E10_unreadable_not_routed`

Route a track whose file could not be found, through the fallback

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E10_unreadable_not_routed`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_export_track_whose_file_is_not_there_is_a_warning_and_not_routed`
  - `tests/test_routing_workers.py::test_an_unreadable_track_is_a_warning_and_the_rest_are_placed`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`

Old text:

```
        if path is None:
            warnings.append({
```

New text:

```
        if False:
            warnings.append({
```

### `u86.E11_is_file`

Accept a candidate path without asking whether it is a file

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E11_is_file`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_sweep_that_could_place_nothing_is_blocked_not_done`
  - `tests/test_routing_workers.py::test_an_export_track_whose_file_is_not_there_is_a_warning_and_not_routed`
  - `tests/test_routing_workers.py::test_an_export_whose_every_file_is_unreadable_is_blocked_not_already_filed`
  - `tests/test_routing_workers.py::test_an_unreadable_track_is_a_warning_and_the_rest_are_placed`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`

Old text:

```
        if candidate and candidate.startswith("/") and Path(candidate).is_file():
```

New text:

```
        if candidate and candidate.startswith("/"):
```

### `u86.E12_prefix_map`

Ignore the prefix map and try the recorded path alone

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E12_prefix_map`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`

Old text:

```
    for candidate in (resolved.path, decoded):
```

New text:

```
    for candidate in (decoded,):
```

### `u86.E4_export_absent`

Drop the refusal of an export path that is not a file

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E4_export_absent`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py; the text also occurs in three intake modules, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_absent_export_refuses`

Old text:

```
    if not export.is_file():
```

New text:

```
    if False:
```

### `u86.E6_intake_absent`

Read an absent intake folder as an empty one instead of refusing

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E6_intake_absent`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_export_without_an_intake_folder_refuses`

Old text:

```
    if not isinstance(node, rbxml.NodeSpan):
        why = node if isinstance(node, str) else f"no folder named {display!r} sits under ROOT"
```

New text:

```
    if not isinstance(node, rbxml.NodeSpan):
        return []
        why = node if isinstance(node, str) else f"no folder named {display!r} sits under ROOT"
```

### `u86.E9_row_absent`

Treat an intake key with no collection row as a row with no Location

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E9_row_absent`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_export_intake_key_with_no_collection_row_is_a_warning`
  - `tests/test_routing_workers.py::test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`

Old text:

```
        row = by_id.get(key)
```

New text:

```
        row = by_id.get(key, {})
```

### `u88.D1_zero_is_a_length`

_duration: a TotalTime of zero reads as a length rather than as unknown

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `D1_zero_is_a_length`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_missing_duration_is_counted_not_guessed`

Old text:

```
    return seconds if seconds > 0 else None
```

New text:

```
    return seconds if seconds >= 0 else None
```

### `u88.D2_prefix_digits`

_duration: match a leading run of digits instead of the whole value, so a fraction reaches int()

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `D2_prefix_digits`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_missing_duration_is_counted_not_guessed`

Old text:

```
not _SECONDS.fullmatch(value.strip())
```

New text:

```
not _SECONDS.match(value.strip())
```

### `u88.D3_absent_attribute`

_duration: drop the absent attribute check, so a row with no TotalTime is read

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `D3_absent_attribute`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 41 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none`
  - `tests/test_routing_workers.py::test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing`
  - `tests/test_routing_workers.py::test_a_declined_export_route_writes_nothing`
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served`
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_lone_unrated_track_with_energy_is_owed_one_rating`
  - `tests/test_routing_workers.py::test_a_missing_duration_is_counted_not_guessed`
  - `tests/test_routing_workers.py::test_a_row_with_no_rating_attribute_is_not_counted_as_owed`
  - `tests/test_routing_workers.py::test_a_run_whose_every_filing_was_skipped_is_blocked_and_not_rated`
  - `tests/test_routing_workers.py::test_a_second_export_run_over_its_own_output_inserts_nothing`
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`
  - `tests/test_routing_workers.py::test_a_track_the_rating_rule_skips_is_filed_and_not_owed[bucket-does-not-rate]`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    if value is None or not _SECONDS.fullmatch(value.strip()):
```

New text:

```
    if not _SECONDS.fullmatch(value.strip()):
```

### `u88.I1_items_outside_intake`

plan_export: a long track outside the intake gets no item, so the digest omits its addition

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `I1_items_outside_intake`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_names_each_track_by_artist_and_title`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_each_long_track_before_anything_is_written`

Old text:

```
        for key in long_plan.keys
        if key not in intake

```

New text:

```
        for key in ()

```

### `u88.I2_item_flag`

plan_export: an intake item never names the long track playlist

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `I2_item_flag`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_each_long_track_before_anything_is_written`

Old text:

```
            "long_track": playlist if key in lengthy else "",
```

New text:

```
            "long_track": "",
```

