# Mutation table: u335-after-12

Measured by `scripts/mutate.py` on 2026-11-24 06:53 UTC, branch `HEAD` at `1a401a39`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 23223 collected. pytest invocations for this batch: 254.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-24 06:52 UTC for commit `1a401a39247d`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 40, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 23223 against 23223. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r1991.E1_doubled_converged` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 1 | killed |
| `r1991.K1_no_unidentified` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 8 | killed |
| `r1991.K2_removed_unidentified` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 1 | killed |
| `r1991.K3_uncompared_dimension_named` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 1 | killed |
| `r1991.K4_unfiled_named` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 1 | killed |
| `r1991.K6_genre_folder_unread` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 1 | killed |
| `r1991.K7_other_buckets_name` | `src/cratekit/write/convergence_check.py` | user | 1 file(s) | 22 | 2 | killed |
| `r312.E12_check_names_no_file` | `src/cratekit/write/convergence_check.py` | user | 2 file(s) | 309 | 6 | killed |
| `r816-e.D1_resolve_once` | `src/cratekit/write/metadata.py` | maintainer | 3 file(s) | 169 | 1 | killed |
| `r816-e.D2_survey_total` | `src/cratekit/write/metadata_cli.py` | user | 3 file(s) | 23223 | 0 (promoted) | zero |
| `u89.L1_absent_is_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 126 | killed |
| `u130-c.C5_no_renumber` | `src/cratekit/write/playlist_pair.py` | user | 1 file(s) | 76 | 3 | killed |
| `u302.W1_intake_replace_bumps_count` | `src/cratekit/write/rbxml.py` | user | 2 file(s) | 86 | 1 | killed |
| `u302.W2_self_closed_node_deepens` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 15 | killed |
| `u302.W3_close_tag_not_counted` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 58 | killed |
| `u302.W4_open_tag_never_self_closing` | `src/cratekit/write/rbxml.py` | user | 3 file(s) | 164 | 17 | killed |
| `u76-a.D3_tree_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.D4_folder_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.D5_playlist_level_lookup` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-a.M1_merge_not_append` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 16 | killed |
| `u76-a.W1_copy_on_write` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.W2_commit_on_success` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.X1_dedupe_against_held` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 6 | killed |
| `u76-b.C1_count_bump` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-b.L1_folder_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L2_anchor_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L3_folder_close_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.L4_playlist_close_own_line` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.O1_anchor_order` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 4 | killed |
| `u76-b.O2_anchor_none` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 4 | killed |
| `u76-b.S1_self_closed_folder` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-b.X2_entries_count` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-b.X3_self_closed_playlist` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 3 | killed |
| `u76-b.X4_track_indent` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-zeros.X5_entries_absent` | `src/cratekit/write/rbxml.py` | maintainer | 4 file(s) | 224 | 3 | killed |
| `u91.R1_crlf_guard` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 343 | 2 | killed |
| `u76-a.D1_duplicate_sibling` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-a.D2_type_collision` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.F1_nfc_fold` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.F2_case_fold` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `u76-a.P2_dedupe_ids` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 2 | killed |
| `u76-zeros.P1_join_pairs` | `src/cratekit/write/rbxml_insert.py` | user | 4 file(s) | 224 | 1 | killed |
| `r1950.C04_second_bucket_files_by_first_word` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 174 | 2 | killed |
| `r2020-composite.C14_favorites_step_reads_no_tree_list` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 2 | killed |
| `r2020.M10_messages_no_unread_warning` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 6 | killed |
| `r2020.M11_owing_no_steps` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 4 | killed |
| `r2020.M12_found_no_after` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 10 | killed |
| `r2020.M13_with_steps_replaces` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 2 | killed |
| `r2020.M1_message_one_unnamed` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 9 | killed |
| `r2020.M4_message_no_advice` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 1 | killed |
| `r2020.M6_warning_code` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 6 | killed |
| `r2020.M7_report_drops_unread` | `src/cratekit/write/rebuild.py` | user | 4 file(s) | 261 | 7 | killed |
| `r312.E10_empty_still_warns` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 3 | killed |
| `r312.E13_record_drops_location` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 6 | killed |
| `r312.E14_listed_in_dropped` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 3 | killed |
| `r316.M10_derivation_restates_no_gap` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 9 | killed |
| `r316.M11_warning_ignores_dimension` | `src/cratekit/write/rebuild.py` | user | 1 file(s) | 197 | 8 | killed |
| `r316.M8_not_derived_ignores_declaration` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 1 | killed |
| `r316.M9_not_derived_ignores_threshold` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 309 | 14 | killed |
| `u132.W4_routing_tree_only` | `src/cratekit/write/rebuild.py` | user | 8 file(s) | 634 | 2 | killed |
| `u219.A4_additions_rows` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 732 | 21 | killed |
| `u340.R05_derive_one_bucket` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 173 | 11 | killed |
| `u340.R06_truth_unread` | `src/cratekit/write/rebuild.py` | user | 3 file(s) | 173 | 4 | killed |
| `u340.R07_vox_first_only` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 168 | 1 | killed |
| `r2020.M15_old_facts_read_as_empty` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 8 | killed |
| `r2020.M16_gate_shows_none` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 2 | killed |
| `r2020.M17_fresh_plan_unrecorded` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 1 | killed |
| `r2020.M18_plan_drops_unread` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 3 | killed |
| `r2020.M19_no_warning_after_gate` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 1 | killed |
| `r2020.M20_resort_report_no_after` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 11 | killed |
| `r2020.M21_resort_resume_no_found` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 10 | killed |
| `r2020.M25_left_behind_count_zero` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 261 | 2 | killed |
| `r316.M3_inbox_gaps_leak_into_totals` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r318-b.N1_no_native_key_dropped` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 231 | 1 | killed |
| `r318.C1_skipped_files_always_empty` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 4 | killed |
| `r318.C2_tombstones_not_consulted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r318.C3_ambiguous_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r318.C4_withdrawn_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r318.C5_withdrawn_single_id_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r318.C6_trees_emptied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 2 | killed |
| `r318.C8_path_reduced_to_name` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r318.C9_warnings_not_emitted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 4 | killed |
| `r318.W5_next_act_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r691.F2_trees_left_off` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F3_planner_warnings_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F4_gaps_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r691.K1_empty_folder_plan_names_no_tree` | `src/cratekit/write/routing_cli.py` | maintainer | 1 file(s) | 197 | 1 | killed |
| `r691.K2_gaps_not_carried_to_the_apply` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N3_declined_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N4_inbox_empty_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r691.P1_destination_left_off_the_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r691.P2_vocal_left_off_the_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.W1_write_ignores_the_plan` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 22 | killed |
| `u155.W6_inbox_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u219.G3_adds_frozen` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 21 | killed |
| `u53-routing-and-rebuild-workers.A3_empty_folder_shortcircuit_removed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u53-routing-and-rebuild-workers.A5_applied_always_true` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R1_resort_drives_a_foreign_job` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R3_resort_drives_an_itemless_job` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 23223 | 0 (promoted) | zero |
| `u86-b.E22_export_remedy` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E23_export_branch` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 57 | killed |
| `u89.W1_resort_worker` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U14_no_native_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U15_export_branch` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 18 | killed |
| `r239-b.S2_unplaced_key_off` | `src/cratekit/write/routing_export.py` | user | 7 file(s) | 724 | 2 | killed |
| `r313.G7_handler_opens_with_write_intent` | `src/cratekit/write/routing_export.py` | user | 3 file(s) | 1634 | 1 | killed |
| `r685-a.V1_route_inbox_export_reads_the_shipped_text` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 215 | 4 | killed |
| `r686.E1_tracks_counts_every_item` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E2_routed_counts_vocal` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 9 | killed |
| `r686.E4_long_tracks_intake_only` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `r686.E5_warnings_dropped` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `r686.E6_gaps_dropped` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E7_subs_not_named` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.B1_owed_rating_blocks_the_answer` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.C1_rates_flag_ignored` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.C2_no_energy_counted` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.C3_files_not_rows` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
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
| `u155.W3_gate_column` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 3 | killed |
| `u155.W4_gate_count` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 3 | killed |
| `u155.W5_owed_once` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 1 | killed |
| `u155.W7_export_item_genre` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 1 | killed |
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
| `u86.E2_governed_tree` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E4_export_absent` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E6_intake_absent` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E9_row_absent` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `u88.D1_zero_is_a_length` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.D2_prefix_digits` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.D3_absent_attribute` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 41 | killed |
| `u88.I1_items_outside_intake` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `u88.I2_item_flag` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 3 | killed |
| `u88.L1_bound_strict` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L2_bound_coefficient` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L3_existing_members_replanned` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L4_folder_warning_dropped` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L5_folder_refusal_bypassed` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.T1_unreadable_count` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89-e6.E6_vox_warnings` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.E1_export_threshold` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.E2_no_vox_subs` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 8 | killed |
| `u89.E3_subs_uncalibrated` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 9 | killed |
| `u89.E4_undeclared_sub` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.E5_unreachable_tree` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91-b.P1_inbox_decide_rows` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91-b.U6_tree_named` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U12_write_warnings` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U17_decide_unreadable` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 3 | killed |
| `u91.U18_unplaced_threshold` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U1_unplaced_rule` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 4 | killed |
| `u91.U3_tree_absent_refusal` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U4_tree_type` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 16 | killed |
| `u91.U5_creating_writer` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 7 | killed |
| `u91.U7_nothing_written` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U8_suffix` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 12 | killed |
| `u91.U9_cut_over_refusal` | `src/cratekit/write/routing_export.py` | user | 1 file(s) | 197 | 2 | killed |
| `r318.P1_withdrawn_branch_removed` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 425 | 5 | killed |
| `r318.P4_ambiguous_reads_not_imported` | `src/cratekit/write/routing_pass.py` | user | 4 file(s) | 425 | 3 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 13 file(s) | 817 | 63 | killed |
| `r1991.T1_removed_node_recorded` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 1 | killed |
| `r1991.T2_first_of_two_recorded` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 1 | killed |
| `r1991.T3_unfiled_pair_recorded` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 1 | killed |
| `r1991.T4_no_record` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 5 | killed |
| `r1991.T5_moves_bound_destinations` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 2 | killed |
| `r1991.T6_filed_untracked` | `src/cratekit/write/trees.py` | user | 21 file(s) | 1590 | 5 | killed |
| `r375-b.T3_a_noop_claims_a_commit` | `src/cratekit/write/trees.py` | user | 3 file(s) | 189 | 1 | killed |
| `r375-b.T4_noop_bound_off_by_one` | `src/cratekit/write/trees.py` | user | 3 file(s) | 189 | 5 | killed |
| `r375-b.T5_witnessed_commit_not_recorded` | `src/cratekit/write/trees.py` | user | 3 file(s) | 189 | 1 | killed |
| `r375-b.T7_commit_recorded_after_the_fingerprint` | `src/cratekit/write/trees.py` | user | 3 file(s) | 189 | 1 | killed |
| `r375-b.T8_counts_filed_as_updates` | `src/cratekit/write/trees.py` | user | 3 file(s) | 189 | 4 | killed |
| `r375-c.T6_every_raise_read_as_a_commit_again` | `src/cratekit/write/trees.py` | user | 3 file(s) | 189 | 1 | killed |
| `u298.H13_capture_verified` | `src/cratekit/write/trees.py` | user | 3 file(s) | 308 | 3 | killed |
| `u298.H14_capture_attached_before_judged` | `src/cratekit/write/trees.py` | user | 3 file(s) | 308 | 2 | killed |
| `u302.W11_landed_commit_recorded_as_zero` | `src/cratekit/write/trees.py` | user | 1 file(s) | 60 | 1 | killed |
| `u302.W14c_root_read_back_unchecked` | `src/cratekit/write/trees.py` | user | 4 file(s) | 393 | 1 | killed |
| `u302.W17_landed_removal_not_recorded` | `src/cratekit/write/trees.py` | user | 3 file(s) | 295 | 1 | killed |
| `u302.W9c_configuration_rules_dropped` | `src/cratekit/write/trees.py` | user | 4 file(s) | 438 | 2 | killed |
| `u77-b.B6_trial_id` | `src/cratekit/write/trees.py` | user | 6 file(s) | 254 | 2 | killed |
| `u77-b.B7_check_empty_catalog` | `src/cratekit/write/trees.py` | user | 6 file(s) | 254 | 3 | killed |
| `u77-b.B8_label_write_order` | `src/cratekit/write/trees.py` | user | 6 file(s) | 254 | 2 | killed |
| `u88-b.W1_replace_not_append` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 2 | killed |
| `u312.E1_exited_ignores_expected` | `tests/_sync_builders.py` | maintainer | 3 file(s) | 196 | 76 | killed |
| `u232.A1_platform_stub` | `tests/conftest.py` | maintainer | 4 file(s) | 90 | 4 | killed |
| `u232.A2_pyrekordbox_stub` | `tests/conftest.py` | maintainer | 4 file(s) | 90 | 26 | killed |
| `u232.A8_opt_in` | `tests/conftest.py` | maintainer | 2 file(s) | 55 | 4 | killed |
| `u312.L1_parser_cache_ignores_membership` | `tests/test_outbound_workers.py` | maintainer | 6 file(s) | 424 | 23 | killed |
| `u232.A10_real_walk_restored` | `tests/test_process_scan.py` | maintainer | 1 file(s) | 46 | 8 | killed |
| `u28-skills-independent.L11_rule_d_scanner` | `tests/test_skills_lint.py` | user | 1 file(s) | 31 | 2 | killed |
| `r658-b.S7_tombstone_full_disk` | `tests/test_uncredited_tombstone.py` | user | 1 file(s) | 35 | 1 | killed |

## Zero rows and what they owe

- `r816-e.D2_survey_total` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u53-routing-and-rebuild-workers.R3_resort_drives_an_itemless_job` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r1991.E1_doubled_converged`

existing guard: a report with a doubled row reads converged

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `E1_doubled_converged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_says_differing_over_a_doubled_row_beside_an_unread_folder`

Old text:

```
        return not self.differences and self.derived > 0 and not self.doubled
```

New text:

```
        return not self.differences and self.derived > 0
```

### `r1991.K1_no_unidentified`

check: put every unread playlist in foreign, so converge says matching over a cleared second genre under an unrecorded renamed folder (the residual itself)

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `K1_no_unidentified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_a_leftover_beside_a_folder_a_write_made_again_is_named_as_not_compared`
  - `tests/test_unrecorded_genre_folder.py::test_a_playlist_its_folders_genre_does_not_declare_stays_foreign`
  - `tests/test_unrecorded_genre_folder.py::test_a_rebuild_still_clears_a_restored_flag_over_an_unrecorded_renamed_folder`
  - `tests/test_unrecorded_genre_folder.py::test_a_renamed_folder_a_record_names_for_a_dropped_bucket_is_named_as_not_compared`
  - `tests/test_unrecorded_genre_folder.py::test_a_second_node_a_write_made_under_the_genres_own_name_is_named_as_not_compared`
  - `tests/test_unrecorded_genre_folder.py::test_a_tree_adopted_before_the_record_names_the_renamed_folder_as_not_compared`
  - `tests/test_unrecorded_genre_folder.py::test_a_vocal_playlist_the_run_did_not_compare_stays_foreign_under_an_unrecorded_folder`
  - `tests/test_unrecorded_genre_folder.py::test_the_converge_verb_never_says_matching_over_an_unrecorded_renamed_folder`

Old text:

```
            (not_read if (node.folder_id, node.playlist_id) in unread else foreign).append(shown)
```

New text:

```
            foreign.append(shown)
```

### `r1991.K2_removed_unidentified`

unidentified: name a playlist rekordbox removed

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `K2_removed_unidentified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_a_removed_playlist_under_an_unrecorded_folder_is_not_named`

Old text:

```
        if not node.removed
        and (node.folder_id, node.playlist_id) not in compared
```

New text:

```
        if True
        and (node.folder_id, node.playlist_id) not in compared
```

### `r1991.K3_uncompared_dimension_named`

unidentified: name a playlist whose only reading is a dimension this run did not compare (vocal, Favorites)

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `K3_uncompared_dimension_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_a_vocal_playlist_the_run_did_not_compare_stays_foreign_under_an_unrecorded_folder`

Old text:

```
        and subs(node) - skipped

```

New text:

```
        and subs(node)

```

### `r1991.K4_unfiled_named`

unidentified: name a playlist holding no filed track, so a person's own folder reads not compared

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `K4_unfiled_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_a_persons_folder_holding_no_filed_track_stays_foreign`

Old text:

```
        and node.content_ids & holding

```

New text:

```
        and node.content_ids

```

### `r1991.K6_genre_folder_unread`

unidentified: read a genre named folder only by its record, so its own playlists read by any bucket

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `K6_genre_folder_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_a_playlist_its_folders_genre_does_not_declare_stays_foreign`

Old text:

```
        if folder not in bucket_names:
            folder = recorded_folder.get(node.folder_id, "")
```

New text:

```
        if True:
            folder = recorded_folder.get(node.folder_id, "")
```

### `r1991.K7_other_buckets_name`

unidentified: read a playlist its folder's genre does not declare by any bucket, so a person's playlist in a genre folder reads not compared

- File: `src/cratekit/write/convergence_check.py`
- Source: `r1991.json`, row `K7_other_buckets_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unrecorded_genre_folder.py`
- Collected: 22 against a baseline of 22
- Kills: 2 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_a_playlist_its_folders_genre_does_not_declare_stays_foreign`
  - `tests/test_unrecorded_genre_folder.py::test_a_renamed_recorded_folder_is_read_by_its_recorded_genre_alone`

Old text:

```
        return set() if place is None else {place[1]}
```

New text:

```
        return readings.get(node.playlist_display, set()) if place is None else {place[1]}
```

### `r312.E12_check_names_no_file`

check: an unexpected difference carries no file location, the state before this unit

- File: `src/cratekit/write/convergence_check.py`
- Source: `r312.json`, row `E12_check_names_no_file`
- Moved: Anchored where u302-replay-after-c.json replayed it: the same text, now in src/cratekit/write/convergence_check.py, was in src/cratekit/write/rebuild.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
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

### `r816-e.D1_resolve_once`

plan_genre_retag: ask the database for the lookup row once per row

- File: `src/cratekit/write/metadata.py`
- Source: `r816-e.json`, row `D1_resolve_once`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_metadata_policy.py`, `tests/test_genre_retag.py`
- Collected: 169 against a baseline of 169
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_rows.py::test_each_distinct_file_word_is_resolved_once`

Old text:

```
        if wanted not in resolved:
```

New text:

```
        if True:
```

### `r816-e.D2_survey_total`

_is_a_file: let a refusal to answer raise out of the survey

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r816-e.json`, row `D2_survey_total`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_rows.py`, `tests/test_metadata_cli.py`, `tests/test_paths_resolved.py`
- Collected: 23223 against a baseline of 23223
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    try:
        return path.is_file()
    except (OSError, ValueError):
        return False
```

New text:

```
    return path.is_file()
```

### `u89.L1_absent_is_default`

load_vocal_threshold: an absent calibration returns the default cut instead of None, so routing files from a cut nobody fitted

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L1_absent_is_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 126 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_absent_vocal_calibration_is_the_default_cut`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`
  - `tests/test_routing_workers.py::test_a_25_minute_track_is_a_member_and_a_19_minute_one_is_not`
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_clean_apply_names_no_skipped_file`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - ... and 111 more, see the JSON sidecar

Old text:

```
    if not path.is_file():
        return None
```

New text:

```
    if not path.is_file():
        return DEFAULT_VOCAL_THRESHOLD
```

### `u130-c.C5_no_renumber`

Leave rekordbox's order as the adds and removals left it

- File: `src/cratekit/write/playlist_pair.py`
- Source: `u130-c.json`, row `C5_no_renumber`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair.py::test_a_track_added_on_the_account_only_lands_in_rekordbox_in_place`
  - `tests/test_sync_pair.py::test_the_first_sync_marks_the_pair_and_adds_only`
  - `tests/test_sync_pair.py::test_when_both_sides_reorder_the_account_order_wins`

Old text:

```
            moved = renumber(db, change.playlist_id, change.order)
```

New text:

```
            moved = 0
```

### `u302.W1_intake_replace_bumps_count`

insert_intake_playlist: a replaced playlist bumps its folder's count as if it were new

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W1_intake_replace_bumps_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`
- Collected: 86 against a baseline of 86
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_an_intake_playlist_replaced_leaves_its_folders_count_alone`

Old text:

```
    if existing is None:
        _bump_count(content, parent, +1)
```

New text:

```
    if True:
        _bump_count(content, parent, +1)
```

### `u302.W2_self_closed_node_deepens`

_node_tokens: a self closed node counts as an open one

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W2_self_closed_node_deepens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_registry.py`
- Collected: 164 against a baseline of 164
- Kills: 15 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_insert_genre_folder_byte_exact`
  - `tests/test_rbxml.py::test_insert_genre_folder_is_idempotent`
  - `tests/test_rbxml.py::test_insert_root_playlist_and_idempotent_replace`
  - `tests/test_rbxml.py::test_insert_then_remove_round_trips`
  - `tests/test_rbxml.py::test_remove_folder_node_absent_is_warning_noop`
  - `tests/test_rbxml.py::test_remove_folder_node_self_closed_target_does_not_wipe_siblings`
  - `tests/test_rbxml.py::test_remove_folder_node_with_track_bearing_subs`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_registry.py::test_a_raw_angle_bracket_in_a_display_name_does_not_unanchor_the_document`
  - `tests/test_xml_splice_golden.py::test_add_vocal_playlists_golden`
  - `tests/test_xml_splice_golden.py::test_add_vocal_playlists_is_idempotent`
  - `tests/test_xml_splice_golden.py::test_unplaced_new_sub_golden`

Old text:

```
            yield (0 if self_closing else 1), opening
```

New text:

```
            yield 1, opening
```

### `u302.W3_close_tag_not_counted`

_node_tokens: a close tag no longer ends a level

- File: `src/cratekit/write/rbxml.py`
- Source: `u302.json`, row `W3_close_tag_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_registry.py`
- Collected: 164 against a baseline of 164
- Kills: 58 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_node_whose_kind_is_unreadable_is_never_described_as_a_playlist`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_a_similarly_named_sibling_folder_is_untouched`
  - `tests/test_rbxml.py::test_a_writer_refuses_to_replace_a_node_of_the_other_type`
  - `tests/test_rbxml.py::test_an_intake_playlist_replaced_leaves_its_folders_count_alone`
  - `tests/test_rbxml.py::test_insert_genre_folder_byte_exact`
  - ... and 43 more, see the JSON sidecar

Old text:

```
            yield -1, closing
```

New text:

```
            yield 0, closing
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
  - `tests/test_xml_splice_golden.py::test_rating_write_golden[sort_inbox_rating]`
  - `tests/test_xml_splice_golden.py::test_rating_write_golden[sort_unplaced_rating]`
  - `tests/test_xml_splice_golden.py::test_route_into_energy_sub_golden`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), raw_attrs.endswith(b"/")
```

New text:

```
    return match, dict(_ATTR_PAIR.findall(raw_attrs)), False
```

### `u76-a.D3_tree_level_lookup`

_write_catalog: locate the catalog tree under ROOT with direct_child, so two trees of one name are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D3_tree_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`

Old text:

```
        found = _sole_child(content, root, tree.display, FOLDER_TYPE)
```

New text:

```
        found = direct_child(content, root, tree.display, FOLDER_TYPE)
```

### `u76-a.D4_folder_level_lookup`

_write_catalog: locate the label folder with direct_child, so two folders of the label's name are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D4_folder_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`

Old text:

```
    existing = _sole_child(content, parent, folder_name, FOLDER_TYPE)
```

New text:

```
    existing = direct_child(content, parent, folder_name, FOLDER_TYPE)
```

### `u76-a.D5_playlist_level_lookup`

_merge_catalog: locate a held year playlist with direct_child, so two playlists of one year are written into rather than refused

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `D5_playlist_level_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`

Old text:

```
        playlist = _sole_child(content, here, name, PLAYLIST_TYPE)
```

New text:

```
        playlist = direct_child(content, here, name, PLAYLIST_TYPE)
```

### `u76-a.M1_merge_not_append`

_write_catalog: never take the merge path, so a held folder gets a second folder of its name beside it (the R-129 doubling)

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `M1_merge_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 16 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_a_catalog_rerun_refreshes_the_folder_rather_than_duplicating_it`
  - `tests/test_tree_writer.py::test_one_source_the_writer_refuses_writes_none_of_them`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`
  - ... and 1 more, see the JSON sidecar

Old text:

```
    if existing is not None:
        return _merge_catalog(content, existing, pairs)
```

New text:

```
    if existing is not None and not existing:
        return _merge_catalog(content, existing, pairs)
```

### `u76-a.W1_copy_on_write`

insert_catalog_folder: edit the caller's document directly, so a refusal after an earlier merge leaves that merge behind

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `W1_copy_on_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    work = bytearray(content)
    warning = _write_catalog(
```

New text:

```
    work = content
    warning = _write_catalog(
```

### `u76-a.W2_commit_on_success`

insert_catalog_folder: copy the working bytes back even on a refusal

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `W2_commit_on_success`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    if warning is None:
        content[:] = work
    return warning
```

New text:

```
    if warning is None or warning:
        content[:] = work
    return warning
```

### `u76-a.X1_dedupe_against_held`

_extend_playlist: dedupe the new ids against nothing, so a member the playlist holds is added again

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-a.json`, row `X1_dedupe_against_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 6 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_catalog_written_twice_is_byte_identical_to_written_once`
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_a_playlist_that_gains_nothing_is_left_byte_identical`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`
  - `tests/test_xml_splice_golden.py::test_label_subtree_written_twice_matches_the_single_write_golden`

Old text:

```
    fresh = dedupe_track_ids(track_ids, track_keys(content, playlist))
```

New text:

```
    fresh = dedupe_track_ids(track_ids, ())
```

### `u76-b.C1_count_bump`

_merge_catalog: move the folder's Count by one less than the playlists created

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `C1_count_bump`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
        _bump_count(content, here, created)
```

New text:

```
        _bump_count(content, here, created - 1)
```

### `u76-b.L1_folder_own_line`

_merge_catalog: drop the check that the held folder starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L1_folder_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
    if not _starts_its_line(content, folder.line_start, folder.tag_start):
        return f"the folder {folder.name!r} does not start its own line"
```

New text:

```
    if False:
        return f"the folder {folder.name!r} does not start its own line"
```

### `u76-b.L2_anchor_own_line`

_merge_catalog: drop the check that the playlist a new year goes before starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L2_anchor_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
            if not _starts_its_line(content, at, anchor.tag_start):
```

New text:

```
            if False:
```

### `u76-b.L3_folder_close_own_line`

_merge_catalog: drop the check that the folder's close tag starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L3_folder_close_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
            if not _starts_its_line(content, at, here.close_start):
```

New text:

```
            if False:
```

### `u76-b.L4_playlist_close_own_line`

_extend_playlist: drop the check that a held playlist's close tag starts its own line

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `L4_playlist_close_own_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`

Old text:

```
        if not _starts_its_line(content, at, playlist.close_start):
```

New text:

```
        if False:
```

### `u76-b.O1_anchor_order`

_merge_catalog: place a new year before the first held playlist sorting ABOVE it, reversing newest first

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `O1_anchor_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`

Old text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
```

New text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) > wanted
```

### `u76-b.O2_anchor_none`

_merge_catalog: always append a new year last

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `O2_anchor_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 4 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_a_new_year_is_placed_among_held_years_the_caller_did_not_name`
  - `tests/test_rbxml.py::test_a_new_year_lands_first_or_last_by_the_callers_order`
  - `tests/test_rbxml.py::test_a_second_write_with_one_new_year_adds_that_playlist_and_nothing_else`

Old text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted
```

New text:

```
                if child.node_type == PLAYLIST_TYPE and _folded(child.name) < wanted and False
```

### `u76-b.S1_self_closed_folder`

_merge_catalog: do not open a self closed held folder before merging into it

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `S1_self_closed_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    if folder.self_closing:
        # An empty folder exported self closed
```

New text:

```
    if folder.self_closing and not folder.self_closing:
        # An empty folder exported self closed
```

### `u76-b.X2_entries_count`

_extend_playlist: move Entries by the ids offered rather than the ids added

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X2_entries_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`

Old text:

```
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    total = _read_int(content, entries) + len(track_ids)
```

### `u76-b.X3_self_closed_playlist`

_extend_playlist: treat a self closed playlist as open, writing at the line of a close tag it does not have

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X3_self_closed_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`
  - `tests/test_rbxml.py::test_a_merge_point_sharing_its_line_refuses_and_writes_nothing`
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    if playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
```

New text:

```
    if playlist.self_closing and not playlist.self_closing:
        content[playlist.tag_end - 1 : playlist.tag_end + 1] = bytearray(
            b">" + CRLF + lines + b" " * playlist.indent + _NODE_CLOSE
```

### `u76-b.X4_track_indent`

_extend_playlist: write the added track keys at the playlist's own indent rather than one step in

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-b.json`, row `X4_track_indent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_self_closed_folder_and_playlist_are_merged_into`

Old text:

```
    lines = track_key_lines(fresh, playlist.indent + INDENT_STEP).encode("utf-8")
```

New text:

```
    lines = track_key_lines(fresh, playlist.indent).encode("utf-8")
```

### `u76-zeros.X5_entries_absent`

_extend_playlist: write the ids into a held playlist with no Entries attribute rather than refusing

- File: `src/cratekit/write/rbxml.py`
- Source: `u76-zeros.json`, row `X5_entries_absent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 3 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_held_playlist_with_no_entry_count_refuses_rather_than_guessing_one`
  - `tests/test_tree_writer.py::test_one_source_the_writer_refuses_writes_none_of_them`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
    if entries is None:
        return f"Entries attr not found for playlist {playlist.name!r}"
    total = _read_int(content, entries) + len(fresh)
```

New text:

```
    if entries is None:
        entries = (playlist.tag_end, playlist.tag_end)
    total = _read_int(content, entries) + len(fresh) if entries[0] != entries[1] else len(fresh)
```

### `u91.R1_crlf_guard`

splice_into_subplaylist create branch: restore the old arithmetic, the close line minus two bytes, with no CRLF check

- File: `src/cratekit/write/rbxml.py`
- Source: `u91.json`, row `R1_crlf_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`
- Collected: 343 against a baseline of 343
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_the_creating_writer_refuses_a_document_whose_lines_end_in_lf`

Old text:

```
        at = _break_before(content, line_start(content, folder.close_start))
        if at is None:
```

New text:

```
        at = line_start(content, folder.close_start) - len(CRLF)
        if at is None:
```

### `u76-a.D1_duplicate_sibling`

_sole_child: answer the first of two same named siblings instead of refusing the duplicate (R-129's refusal removed)

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `D1_duplicate_sibling`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_two_siblings_of_one_name_refuse_and_write_nothing`
  - `tests/test_tree_writer.py::test_the_catalog_check_refuses_a_held_year_playlist_that_appears_twice`

Old text:

```
    if len(matches) > 1:
        return (
            f"{len(matches)} {_type_name(node_type)}s named
```

New text:

```
    if len(matches) > 99:
        return (
            f"{len(matches)} {_type_name(node_type)}s named
```

### `u76-a.D2_type_collision`

_sole_child: check the type of every match but the first, so a same named node of the other type standing first is merged into

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `D2_type_collision`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_failure_after_an_earlier_merge_writes_nothing`

Old text:

```
    for child in matches:
        if child.node_type != node_type:
```

New text:

```
    for child in matches[1:]:
        if child.node_type != node_type:
```

### `u76-a.F1_nfc_fold`

_folded: compare names as given, so a composed and a decomposed spelling of one label are two folders

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `F1_nfc_fold`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py; the text also occurs in an intake module, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_name_drawn_two_ways_in_unicode_is_one_folder`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return name
```

### `u76-a.F2_case_fold`

_folded: fold case as well, so a label differing only by case is poured into another label's folder

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `F2_case_fold`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py; the text also occurs in an intake module, so the tool could not pick the file
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_similarly_named_sibling_folder_is_untouched`

Old text:

```
    return unicodedata.normalize("NFC", name)
```

New text:

```
    return unicodedata.normalize("NFC", name).casefold()
```

### `u76-a.P2_dedupe_ids`

_merged_pairs: keep a batch's repeated ids, so a playlist lists one track twice

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-a.json`, row `P2_dedupe_ids`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 2 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`
  - `tests/test_rbxml.py::test_track_ids_are_deduplicated_inside_a_playlist`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(joined[key][0], list(joined[key][1])) for key in order]
```

### `u76-zeros.P1_join_pairs`

_merged_pairs: keep every pair as given, so a caller naming one playlist twice emits two siblings of that name

- File: `src/cratekit/write/rbxml_insert.py`
- Source: `u76-zeros.json`, row `P1_join_pairs`
- Moved: the same text, now in src/cratekit/write/rbxml_insert.py, was in src/cratekit/write/rbxml.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rbxml.py`, `tests/test_xml_splice_golden.py`, `tests/test_tree_writer.py`, `tests/test_tree_registry.py`
- Collected: 224 against a baseline of 224
- Kills: 1 (killed)
- Killed:
  - `tests/test_rbxml.py::test_a_caller_naming_one_playlist_twice_gets_one_on_the_creating_write`

Old text:

```
    return [(joined[key][0], dedupe_track_ids(joined[key][1])) for key in order]
```

New text:

```
    return [(name, dedupe_track_ids(ids)) for name, ids in playlists]
```

### `r1950.C04_second_bucket_files_by_first_word`

rebuild: filed_genres hands the second bucket the first genre's word, so its genre sub is never reached

- File: `src/cratekit/write/rebuild.py`
- Source: `r1950.json`, row `C04_second_bucket_files_by_first_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre_guards_counts.py`, `tests/test_second_genre.py`, `tests/test_rebuild.py`
- Collected: 174 against a baseline of 174
- Kills: 2 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well`
  - `tests/test_second_genre_guards_counts.py::test_the_second_bucket_files_by_the_second_genres_own_word`

Old text:

```
return ((first, entry.genre), (second, entry.second_genre))
```

New text:

```
return ((first, entry.genre), (second, entry.genre))
```

### `r2020-composite.C14_favorites_step_reads_no_tree_list`

M14's composite, the thing it guards: the favorites step skipped warning reads no list of driven trees, so a drive over another tree names the routing tree's skipped step

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020-composite.json`, row `C14_favorites_step_reads_no_tree_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`

Old text:

```
    if declared.tree.id not in {str(tree_id) for tree_id in tree_ids}:
        return ()
```

New text:

```
    if False:
        return ()
```

### `r2020.M10_messages_no_unread_warning`

after_messages: leave the unidentified warning out of what a drive says

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M10_messages_no_unread_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 6 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_that_failed_part_way_names_the_playlist_as_a_step`
  - `tests/test_unread_playlist_warnings.py::test_every_item_report_of_a_job_is_read_back`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`

Old text:

```
        *unidentified_warnings(unread),

```

New text:

```
        *(),

```

### `r2020.M11_owing_no_steps`

ReportedDrive.owing: re-raise the refusal with no steps, so a partial failure says nothing of what the finished trees found

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M11_owing_no_steps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_that_failed_part_way_names_the_playlist_as_a_step`

Old text:

```
            raise with_steps(failed, self._messages()[1]) from failed
```

New text:

```
            raise with_steps(failed, ()) from failed
```

### `r2020.M12_found_no_after`

ReportedDrive.found: leave the after check's sentences off the success envelope

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M12_found_no_after`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 10 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_drive_over_nothing_unread_says_nothing_of_it`
  - `tests/test_unread_playlist_warnings.py::test_the_rebuild_worker_reports_its_after_check`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`

Old text:

```
            *self._messages()[0],

```

New text:

```
            *(),

```

### `r2020.M13_with_steps_replaces`

with_steps: replace the cause's own steps instead of appending to them

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M13_with_steps_replaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps`

Old text:

```
steps=(*cause.remediation.steps, *steps)),
```

New text:

```
steps=(*steps,)),
```

### `r2020.M1_message_one_unnamed`

unidentified_message: answer None for a single playlist, so one unread playlist goes unnamed everywhere

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M1_message_one_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 9 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_that_failed_part_way_names_the_playlist_as_a_step`
  - `tests/test_unread_playlist_warnings.py::test_every_envelope_after_the_gate_names_it`
  - `tests/test_unread_playlist_warnings.py::test_the_message_names_every_playlist_uncapped_and_sorted`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count`
  - `tests/test_unread_playlist_warnings.py::test_the_resumes_gate_shows_the_playlist_the_plan_could_not_read`

Old text:

```
    found = sorted(playlists)
    if not found:
```

New text:

```
    found = sorted(playlists)
    if len(found) < 2:
```

### `r2020.M4_message_no_advice`

unidentified_message: drop the shared wording, so the sentence says nothing of what to do

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M4_message_no_advice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 1 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count`

Old text:

```
        f"{'; '.join(found)}{UNIDENTIFIED}"
```

New text:

```
        f"{'; '.join(found)}"
```

### `r2020.M6_warning_code`

unidentified_warnings: carry the left behind code, so a reader filtering by code finds none

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M6_warning_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 6 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_every_envelope_after_the_gate_names_it`
  - `tests/test_unread_playlist_warnings.py::test_every_item_report_of_a_job_is_read_back`
  - `tests/test_unread_playlist_warnings.py::test_the_message_names_every_playlist_uncapped_and_sorted`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`

Old text:

```
({"code": UNIDENTIFIED_PLAYLISTS, "message": message},)
```

New text:

```
({"code": LEFT_BEHIND, "message": message},)
```

### `r2020.M7_report_drops_unread`

after_report: stage no unidentified playlists, so neither resume can name them

- File: `src/cratekit/write/rebuild.py`
- Source: `r2020.json`, row `M7_report_drops_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 7 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_names_what_it_left_beside_what_it_did_not_compare`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_over_a_restored_tree_clears_its_flag_and_names_the_playlist`
  - `tests/test_unread_playlist_warnings.py::test_a_rebuild_that_failed_part_way_names_what_the_finished_tree_found_as_steps`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_that_failed_part_way_names_the_playlist_as_a_step`
  - `tests/test_unread_playlist_warnings.py::test_the_rebuild_worker_reports_its_after_check`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`

Old text:

```
        "unidentified": list(after.unidentified),
```

New text:

```
        "unidentified": [],
```

### `r312.E10_empty_still_warns`

left_behind_message: a run that left nothing still produces a sentence

- File: `src/cratekit/write/rebuild.py`
- Source: `r312.json`, row `E10_empty_still_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
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
- Collected: 309 against a baseline of 309
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
- Collected: 309 against a baseline of 309
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

### `r316.M10_derivation_restates_no_gap`

derive_from_taxonomy stops calling not_derived and reports no gaps, so the resume and the derivation disagree

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M10_derivation_restates_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 309 against a baseline of 309
- Kills: 9 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_library_with_no_vocal_calibration_reports_what_it_did_not_compare`
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_rebuild.py::test_the_derivation_routes_a_file_through_the_declared_rules`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`
  - `tests/test_routing_workers.py::test_an_uncalibrated_export_creates_no_vocal_sub_and_names_the_gap`
  - `tests/test_routing_workers.py::test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_each_files_destination`
  - `tests/test_routing_workers.py::test_the_export_gate_names_the_vocal_dimension_it_did_not_read`
  - `tests/test_routing_workers.py::test_the_gap_rule_is_the_derivations_own`

Old text:

```
    gaps = not_derived(declared, vocal_threshold=vocal_threshold)
```

New text:

```
    gaps = ()
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

### `r316.M8_not_derived_ignores_declaration`

not_derived names the vocal gap whether or not the taxonomy declares an additive sub-playlist

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M8_not_derived_ignores_declaration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface`

Old text:

```
    return (VOCAL_DIMENSION,) if additive and vocal_threshold is None else ()
```

New text:

```
    return (VOCAL_DIMENSION,) if vocal_threshold is None else ()
```

### `r316.M9_not_derived_ignores_threshold`

not_derived names the vocal gap even when a threshold was handed in and the dimension was derived

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M9_not_derived_ignores_threshold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 309 against a baseline of 309
- Kills: 14 (killed)
- Killed:
  - `tests/test_rebuild.py::test_a_vocal_playlist_nothing_compared_is_not_named_as_left_behind`
  - `tests/test_rebuild.py::test_a_vocal_track_lands_in_its_energy_sub_AND_the_additive_one`
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[above]`
  - `tests/test_routing_workers.py::test_a_calibrated_inbox_files_a_track_over_the_cut_under_with_vox[below]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-rebuild]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_converge_compares_the_vocal_sub_once_calibrated`
  - `tests/test_routing_workers.py::test_the_database_apply_files_the_track_where_the_gate_said`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_gap_rule_is_the_derivations_own`

Old text:

```
    return (VOCAL_DIMENSION,) if additive and vocal_threshold is None else ()
```

New text:

```
    return (VOCAL_DIMENSION,) if additive else ()
```

### `u132.W4_routing_tree_only`

A rebuild of another tree names the routing tree's skipped step

- File: `src/cratekit/write/rebuild.py`
- Source: `u132.json`, row `W4_routing_tree_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 634 against a baseline of 634
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`

Old text:

```
    if declared.tree.id not in {str(tree_id) for tree_id in tree_ids}:

```

New text:

```
    if False:

```

### `u219.A4_additions_rows`

additions: report nothing missing, so the gate shows no add and the resort queues nothing

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A4_additions_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 732 against a baseline of 732
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_corrupt_calibration_refuses_the_resume_before_any_item_runs[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-native]`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        for entry in report.missing
    ]
```

New text:

```
        for entry in report.missing[:0]
    ]
```

### `u340.R05_derive_one_bucket`

filed_genres: answer the genre's bucket alone, so rebuild, converge and resort never file the second folder

- File: `src/cratekit/write/rebuild.py`
- Source: `u340.json`, row `R05_derive_one_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 173 against a baseline of 173
- Kills: 11 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_alone_in_its_folder_is_named_by_the_check`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_leaves_its_genre_sub_named_as_well`
  - `tests/test_second_genre.py::test_a_cleared_second_genre_under_a_folder_renamed_in_rekordbox_is_named`
  - `tests/test_second_genre.py::test_a_recorded_folder_renamed_to_another_genres_name_is_read_by_that_name`
  - `tests/test_second_genre.py::test_a_soul_tracks_cleared_rnb_alone_in_the_rnb_band_is_named_too`
  - `tests/test_second_genre.py::test_a_vocal_track_takes_with_vox_in_both_folders`
  - `tests/test_second_genre.py::test_an_energy_change_moves_the_band_in_both_folders`
  - `tests/test_second_genre.py::test_rebuild_files_both_and_a_cleared_second_genre_reads_as_that_folder_alone`
  - `tests/test_second_genre.py::test_the_converge_verb_says_differing_over_a_cleared_second_genre`
  - `tests/test_second_genre.py::test_the_derivation_places_a_track_in_both_folders_in_the_same_band`

Old text:

```
    return ((first, entry.genre), (second, entry.second_genre))
```

New text:

```
    return ((first, entry.genre),)
```

### `u340.R06_truth_unread`

read_truth: drop the second genre reading, so a file's second genre never reaches the derivation

- File: `src/cratekit/write/rebuild.py`
- Source: `u340.json`, row `R06_truth_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`, `tests/test_organize_mirror_edits_u340.py`
- Collected: 173 against a baseline of 173
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u340.py::test_a_band_move_in_one_folder_moves_the_energy_in_both_and_keeps_the_second_genre`
  - `tests/test_organize_mirror_edits_u340.py::test_a_move_that_would_wake_a_second_genre_naming_its_own_folder_is_not_taken`
  - `tests/test_organize_mirror_edits_u340.py::test_taking_it_off_one_folder_alone_is_listed_and_not_taken`
  - `tests/test_second_genre.py::test_the_truth_reads_the_second_genre_in_the_same_open`

Old text:

```
        second_genre=values["secondgenre"],
```

New text:

```
        second_genre=None,
```

### `u340.R07_vox_first_only`

derive_from_taxonomy: file the with vox sub in the genre's bucket only

- File: `src/cratekit/write/rebuild.py`
- Source: `u340.json`, row `R07_vox_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_second_genre.py`, `tests/test_rebuild.py`
- Collected: 168 against a baseline of 168
- Kills: 1 (killed)
- Killed:
  - `tests/test_second_genre.py::test_a_vocal_track_takes_with_vox_in_both_folders`

Old text:

```
            if vocal_threshold is not None and routing.routes_with_vox(
                entry.voxlevel, vocal_threshold
            ):
                out.extend(
```

New text:

```
            if bucket_id == routing.resolve_bucket(declared, entry.genre).bucket_id and vocal_threshold is not None and routing.routes_with_vox(
                entry.voxlevel, vocal_threshold
            ):
                out.extend(
```

### `r2020.M15_old_facts_read_as_empty`

_resort_facts: read facts with no list as an empty one, round one's blocker

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M15_old_facts_read_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[converged]`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[resort]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_unread_playlist_warnings.py::test_a_job_an_older_build_froze_says_its_plan_did_not_record_them`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_that_failed_part_way_names_the_playlist_as_a_step`

Old text:

```
    if "unidentified" in facts:
```

New text:

```
    if True:
```

### `r2020.M16_gate_shows_none`

_resort_facts: show no playlist not compared even when the plan recorded some

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M16_gate_shows_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count`
  - `tests/test_unread_playlist_warnings.py::test_the_resumes_gate_shows_the_playlist_the_plan_could_not_read`

Old text:

```
        playlists = [] if unread is None else [unread]
```

New text:

```
        playlists = []
```

### `r2020.M17_fresh_plan_unrecorded`

route_resort: freeze no empty list, so a fresh plan over nothing unread reads as an older build's

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M17_fresh_plan_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 1 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_a_fresh_plan_over_no_routed_tree_records_an_empty_list`

Old text:

```
    facts: dict[str, Any] = {"trees": list(routed), "unidentified": []}
```

New text:

```
    facts: dict[str, Any] = {"trees": list(routed)}
```

### `r2020.M18_plan_drops_unread`

route_resort: record no unidentified playlists from the preview

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M18_plan_drops_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 3 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_every_envelope_after_the_gate_names_it`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count`
  - `tests/test_unread_playlist_warnings.py::test_the_resumes_gate_shows_the_playlist_the_plan_could_not_read`

Old text:

```
            entry for report in reports for entry in report.unidentified

```

New text:

```
            entry for report in reports[:0] for entry in report.unidentified

```

### `r2020.M19_no_warning_after_gate`

route_resort: carry no playlist-not-compared warning on the envelopes after the gate

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M19_no_warning_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 1 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_every_envelope_after_the_gate_names_it`

Old text:

```
    warnings = [*warnings, *rebuild.unidentified_warnings(facts.get("unidentified") or ())]
```

New text:

```
    warnings = [*warnings]
```

### `r2020.M20_resort_report_no_after`

handle_resort: stage only the due again count, so the resort's resume names nothing it found

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M20_resort_report_no_after`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 11 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_drive_over_nothing_unread_says_nothing_of_it`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_that_failed_part_way_names_the_playlist_as_a_step`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`

Old text:

```
            **rebuild.after_report(tree_id, report.after, active_taxonomy.load(cfg)),

```

New text:

```
            "tree_id": tree_id,

```

### `r2020.M21_resort_resume_no_found`

the resort's resume: leave the drive's findings off its success envelope

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M21_resort_resume_no_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 10 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resume_that_drove_nothing_carries_no_vocal_warning[resort]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`
  - `tests/test_unread_playlist_warnings.py::test_a_resort_drive_over_nothing_unread_says_nothing_of_it`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_drive_names_the_playlist_beside_what_it_left`

Old text:

```
            *drive.found(threshold, declared),

```

New text:

```
            *(),

```

### `r2020.M25_left_behind_count_zero`

route_resort, an existing guard: show a left behind count of zero over the preview's leftovers

- File: `src/cratekit/write/routing_cli.py`
- Source: `r2020.json`, row `M25_left_behind_count_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_unread_playlist_warnings.py`, `tests/test_routing_workers.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_resort_scope.py`
- Collected: 261 against a baseline of 261
- Kills: 2 (killed)
- Killed:
  - `tests/test_unread_playlist_warnings.py::test_the_resort_gate_names_a_playlist_not_compared_beside_its_left_behind_count`
  - `tests/test_unread_playlist_warnings.py::test_the_resort_gate_over_nothing_unread_says_nothing_of_it`

Old text:

```
        facts["left_behind"] = sum(len(report.unexpected) for report in reports)
```

New text:

```
        facts["left_behind"] = 0
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

### `r318-b.N1_no_native_key_dropped`

apply_inbox: the no-native-tree answer carries no skipped_files key, so the payload shape differs by branch

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `N1_no_native_key_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_on_a_library_with_no_native_tree_says_so`

Old text:

```
            "skipped": 0,
            "skipped_files": [],
        }
```

New text:

```
            "skipped": 0,
        }
```

### `r318.C1_skipped_files_always_empty`

apply_inbox: skipped_files is always empty, the headline defect R-318 measured, a count and no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C1_skipped_files_always_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_human_output_names_the_skipped_file`

Old text:

```
        "skipped_files": _skipped_files(cfg, rows, missed),
```

New text:

```
        "skipped_files": [],
```

### `r318.C2_tombstones_not_consulted`

_skipped_files: match against the live index instead of the tombstoned one, so withdrawn can never be told from not imported

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C2_tombstones_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
        paths, index.by_tombstoned_location, root=cfg.library.root, prefix_map=rules
```

New text:

```
        paths, index.by_active_location, root=cfg.library.root, prefix_map=rules
```

### `r318.C3_ambiguous_ids_dropped`

_skipped_files: an ambiguous file names no rows, so a person cannot see which two rows to choose between

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C3_ambiguous_ids_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`

Old text:

```
            ids = alive.content_ids
        elif
```

New text:

```
            ids = ()
        elif
```

### `r318.C4_withdrawn_ids_dropped`

_skipped_files: a withdrawn file names no tombstoned row

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C4_withdrawn_ids_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
```

New text:

```
            ids = ()
```

### `r318.C5_withdrawn_single_id_dropped`

_skipped_files: a withdrawn file with ONE tombstone names nothing, only the ambiguous-tombstone ids survive

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C5_withdrawn_single_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
            ids = dead.content_ids or ((dead.content_id,) if dead.content_id else ())
```

New text:

```
            ids = dead.content_ids
```

### `r318.C6_trees_emptied`

_skipped_files: the record names no tree it was declared into

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C6_trees_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_skipped_twice_in_one_tree_names_that_tree_once`

Old text:

```
                "trees": sorted(set(tree_ids)),
```

New text:

```
                "trees": [],
```

### `r318.C8_path_reduced_to_name`

_skipped_files: the payload carries the file name instead of the full path

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C8_path_reduced_to_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`

Old text:

```
                "path": path,
```

New text:

```
                "path": Path(path).name,
```

### `r318.C9_warnings_not_emitted`

route_inbox: the skip warnings never reach the envelope, so the human output, which prints warnings and no totals, names no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C9_warnings_not_emitted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_human_output_names_the_skipped_file`

Old text:

```
                *skipped_warnings(result["skipped_files"]),
```

New text:

```
(empty)
```

### `r318.W5_next_act_dropped`

skipped_warnings: the reason sentence and its next act are replaced by a bare phrase

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W5_next_act_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`

Old text:

```
        why = SKIP_NEXT_ACT[routing_pass.Placement(reason)]
```

New text:

```
        why = "of its state"
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

### `r691.K1_empty_folder_plan_names_no_tree`

the plan's placements are keyed only when the folder has files, so the write's index has nothing to find for an empty folder

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `K1_empty_folder_plan_names_no_tree`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_empty_inbox_plan_names_every_native_tree`

Old text:

```
    placements: dict[str, tuple[rebuild.DeclaredPlacement, ...]] = {
        tree_id: () for tree_id in native
    }

```

New text:

```
    placements: dict[str, tuple[rebuild.DeclaredPlacement, ...]] = {}

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

### `u155.W6_inbox_item_genre`

plan_inbox: carry an empty genre column on every item, the database gate hiding the second place

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W6_inbox_item_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
            "genre": genre.get(str(path), ""),
```

New text:

```
            "genre": "",
```

### `u219.G3_adds_frozen`

route resort: freeze an empty plan in the job, so the worker holds its write to nothing the gate showed

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G3_adds_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 297 against a baseline of 297
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[the library moved]`
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing[two files swapped]`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-encrypted]`
  - `tests/test_routing_workers.py::test_a_queued_job_runs_its_item_and_the_tree_holds_the_track[resort-native]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[resort]`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                RESORT_ADDS_KEY: adds,
```

New text:

```
                RESORT_ADDS_KEY: [],
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

### `u53-routing-and-rebuild-workers.R3_resort_drives_an_itemless_job`

A resort queued by an older build drives to succeeded over a library nothing read

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `R3_resort_drives_an_itemless_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 23223 against a baseline of 23223
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

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

### `r239-b.S2_unplaced_key_off`

route unplaced's open, unplaced_items, passes unlock=False again

- File: `src/cratekit/write/routing_export.py`
- Source: `r239-b.json`, row `S2_unplaced_key_off`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 724 against a baseline of 724
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

### `r313.G7_handler_opens_with_write_intent`

the unplaced report opens the database with require_closed, so it refuses with rekordbox open

- File: `src/cratekit/write/routing_export.py`
- Source: `r313.json`, row `G7_handler_opens_with_write_intent`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1634 against a baseline of 1634
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_reports_with_rekordbox_open_and_writes_nothing`

Old text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg)

```

New text:

```
        return [], {"compared": False, "reason": "no-native-tree", "collection": 0}
    handle = rb_writer.open_db(cfg=cfg, require_closed=True)

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

### `r688.C3_files_not_rows`

two rows naming one file are counted as one owed rating, though rekordbox rates each row

- File: `src/cratekit/write/routing_export.py`
- Source: `r688.json`, row `C3_files_not_rows`
- Moved: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_two_rows_naming_one_file_are_both_counted_as_owed`

Old text:

```
        owed += sum(1 for key in files[placement.location] if _unrated(by_id[key]))

```

New text:

```
        owed += 1 if any(_unrated(by_id[key]) for key in files[placement.location]) else 0

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

### `u155.W3_gate_column`

_column: show a genre sub placement in the energy sub column, the round 1 defect

- File: `src/cratekit/write/routing_export.py`
- Source: `u155.json`, row `W3_gate_column`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
    if routing.genre_sub_named(declared, placement.bucket, placement.sub):
        return genre
```

New text:

```
(empty)
```

### `u155.W4_gate_count`

_placed_counts: count no track as filed into a genre sub

- File: `src/cratekit/write/routing_export.py`
- Source: `u155.json`, row `W4_gate_count`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 3 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_gate_counts_tracks_filed_into_a_genre_sub`

Old text:

```
        "genre sub": sum(1 for item in tracks if item.get("genre")),
```

New text:

```
        "genre sub": 0,
```

### `u155.W5_owed_once`

_owed_ratings: count a row once per placement again, two for a vocal track

- File: `src/cratekit/write/routing_export.py`
- Source: `u155.json`, row `W5_owed_once`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_vocal_track_unrated_is_owed_one_rating_not_one_per_place`

Old text:

```
        if placement.location in counted:
            continue
```

New text:

```
(empty)
```

### `u155.W7_export_item_genre`

plan_export: carry an empty genre column on every item, the export gate hiding the second place

- File: `src/cratekit/write/routing_export.py`
- Source: `u155.json`, row `W7_export_item_genre`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
            "vocal": vocal.get(key, ""),
            "genre": decision.genre.get(key, ""),
```

New text:

```
            "vocal": vocal.get(key, ""),
            "genre": "",
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

### `u86.E2_governed_tree`

Hand the export writer an ungoverned tree, so the emitter guard is never armed

- File: `src/cratekit/write/routing_export.py`
- Source: `u86.json`, row `E2_governed_tree`
- Moved: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_export_writer_itself_refuses_a_routing_tree_that_has_cut_over`

Old text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
```

New text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=rbxml.Tree(display=tree.display))
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

### `u88.L1_bound_strict`

_long_tracks: a track of exactly the bound becomes a member

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `L1_bound_strict`
- Moved: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`

Old text:

```
        elif seconds > long_tracks.over_seconds and key not in members:
```

New text:

```
        elif seconds >= long_tracks.over_seconds and key not in members:
```

### `u88.L2_bound_coefficient`

_long_tracks: raise the bound by a minute over the declared value

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `L2_bound_coefficient`
- Moved: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`

Old text:

```
        elif seconds > long_tracks.over_seconds and key not in members:
```

New text:

```
        elif seconds > long_tracks.over_seconds + 60 and key not in members:
```

### `u88.L3_existing_members_replanned`

_long_tracks: drop the member exclusion, so the offered plan names tracks the playlist already holds

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `L3_existing_members_replanned`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`

Old text:

```
        elif seconds > long_tracks.over_seconds and key not in members:
```

New text:

```
        elif seconds > long_tracks.over_seconds:
```

### `u88.L4_folder_warning_dropped`

_long_tracks: a root FOLDER of the playlist's name plans nothing and warns nothing

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `L4_folder_warning_dropped`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced`

Old text:

```
        warnings.append({
            "code": "route-write-skipped",
            "message": f"the {long_tracks.display!r} playlist was not built: {held}",
        })

```

New text:

```
(empty)
```

### `u88.L5_folder_refusal_bypassed`

_long_tracks: never take the refusal branch, so a root FOLDER is planned over and only the writer refuses

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `L5_folder_refusal_bypassed`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_root_folder_of_that_name_is_a_warning_and_is_not_replaced`

Old text:

```
    if isinstance(held, str):
        warnings.append({
```

New text:

```
    if False:
        warnings.append({
```

### `u88.T1_unreadable_count`

route_inbox_export: the unreadable length count is reported as zero

- File: `src/cratekit/write/routing_export.py`
- Source: `u88.json`, row `T1_unreadable_count`
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
        duration_unreadable=long_plan.unreadable,
```

New text:

```
        duration_unreadable=0,
```

### `u89-e6.E6_vox_warnings`

_vox_subs: drop the vocal writer's per folder warnings

- File: `src/cratekit/write/routing_export.py`
- Source: `u89-e6.json`, row `E6_vox_warnings`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served`

Old text:

```
    warnings.extend(
        {"code": "route-write-skipped", "message": text} for text in report.warnings
    )
```

New text:

```
(empty)
```

### `u89.E1_export_threshold`

plan_export: derive with None instead of the loaded cut

- File: `src/cratekit/write/routing_export.py`
- Source: `u89.json`, row `E1_export_threshold`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
        declared, readings, vocal_threshold=threshold
    )
```

New text:

```
        declared, readings, vocal_threshold=None
    )
```

### `u89.E2_no_vox_subs`

_vox_subs: skip the vocal writer, so no sub exists for the router to splice into

- File: `src/cratekit/write/routing_export.py`
- Source: `u89.json`, row `E2_no_vox_subs`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_files_over_the_cut_and_not_under_it`
  - `tests/test_routing_workers.py::test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing`
  - `tests/test_routing_workers.py::test_a_folder_the_vocal_writer_cannot_serve_is_a_warning_and_the_rest_are_served`
  - `tests/test_routing_workers.py::test_the_export_gate_names_each_track_by_artist_and_title`
  - `tests/test_routing_workers.py::test_the_export_gate_prints_the_plan_in_the_default_mode`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_every_item_the_digest_was_taken_over`
  - `tests/test_routing_workers.py::test_the_export_vocal_subs_are_created_once`
  - `tests/test_routing_workers.py::test_vocal_subs_alone_are_a_change_and_write_a_file`

Old text:

```
        written, report = trees.add_vox_playlists(content, declared, tree=tree)
```

New text:

```
        written, report = content, trees.VoxReport()
```

### `u89.E3_subs_uncalibrated`

_vox_subs: drop the calibration condition, so an uncalibrated export gains empty vocal subs

- File: `src/cratekit/write/routing_export.py`
- Source: `u89.json`, row `E3_subs_uncalibrated`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_long_track_alone_is_a_change_and_writes_a_file`
  - `tests/test_routing_workers.py::test_an_export_inbox_lands_each_track_in_its_declared_sub`
  - `tests/test_routing_workers.py::test_an_export_run_owes_the_import_of_the_root_playlist_it_added_to_alone`
  - `tests/test_routing_workers.py::test_an_export_whose_every_file_is_unreadable_is_blocked_not_already_filed`
  - `tests/test_routing_workers.py::test_an_uncalibrated_export_creates_no_vocal_sub_and_names_the_gap`
  - `tests/test_routing_workers.py::test_the_check_run_after_the_playlist_import_owes_no_import`
  - `tests/test_routing_workers.py::test_the_export_gate_leaves_an_unread_track_unnamed`
  - `tests/test_routing_workers.py::test_the_export_gate_says_why_an_intake_track_goes_nowhere`
  - `tests/test_routing_workers.py::test_the_offered_plan_names_each_long_track_before_anything_is_written`

Old text:

```
    if threshold is None or not any(
```

New text:

```
    if not any(
```

### `u89.E4_undeclared_sub`

_vox_subs: drop the declared vocal sub condition, so a taxonomy without one is asked for its display

- File: `src/cratekit/write/routing_export.py`
- Source: `u89.json`, row `E4_undeclared_sub`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_over_a_taxonomy_with_no_vocal_sub_creates_none`

Old text:

```
    if threshold is None or not any(
        entry.additive and entry.id == trees.VOX_SUB_CLASS for entry in declared.sub_classes
    ):
```

New text:

```
    if threshold is None:
```

### `u89.E5_unreachable_tree`

_vox_subs: narrow the except to DuplicateFolders, so an export with no routing tree raises

- File: `src/cratekit/write/routing_export.py`
- Source: `u89.json`, row `E5_unreachable_tree`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_export_with_no_routing_tree_warns_rather_than_crashing`

Old text:

```
    except (trees.TreeUnreachable, trees.DuplicateFolders) as exc:
```

New text:

```
    except trees.DuplicateFolders as exc:
```

### `u91-b.P1_inbox_decide_rows`

plan_export, existing guard sample: hand an intake key with no collection row to _decide anyway

- File: `src/cratekit/write/routing_export.py`
- Source: `u91-b.json`, row `P1_inbox_decide_rows`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_intake_key_with_no_row_warns_once_and_only_as_row_absent`

Old text:

```
                f"row in {export.name}, so it was not routed",
            })
            continue
        rows.append((key, row))
```

New text:

```
                f"row in {export.name}, so it was not routed",
            })
        rows.append((key, row or {}))
```

### `u91-b.U6_tree_named`

apply_unplaced_export: stop naming the tree, so the emitter guard is unarmed and the genre folder is searched for across the whole playlist section

- File: `src/cratekit/write/routing_export.py`
- Source: `u91-b.json`, row `U6_tree_named`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing`

Old text:

```
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
```

New text:

```
    report = trees.apply_unplaced_changes(plan, buffer, tree=None)
```

### `u91.U12_write_warnings`

route_unplaced_export: drop the writer's skipped writes from the warnings

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U12_write_warnings`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_missing_genre_folder_is_a_skipped_write_and_no_folder_is_invented`

Old text:

```
        *({"code": "route-write-skipped", "message": text} for text in report.warnings),
    ]
    # "NOTHING TO ROUTE" ONLY WHEN NOTHING WAS LEFT BEHIND, the inbox sweep's
```

New text:

```
    ]
    # "NOTHING TO ROUTE" ONLY WHEN NOTHING WAS LEFT BEHIND, the inbox sweep's
```

### `u91.U17_decide_unreadable`

_decide: route a row whose Location names no file here, by absent tags, instead of warning and skipping it

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U17_decide_unreadable`
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
                f"not routed",
            })
            continue
        files.setdefault(str(path), []).append(key)
```

New text:

```
                f"not routed",
            })
        files.setdefault(str(path), []).append(key)
```

### `u91.U18_unplaced_threshold`

plan_unplaced_export: route with no vocal cut instead of the calibrated one

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U18_unplaced_threshold`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates`

Old text:

```
    decision = _decide(cfg, declared, [(key, by_id[key]) for key in keys], threshold, warnings)
```

New text:

```
    decision = _decide(cfg, declared, [(key, by_id[key]) for key in keys], None, warnings)
```

### `u91.U1_unplaced_rule`

unplaced_keys: return every collection key, so a track already under the routing tree is planned again

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U1_unplaced_rule`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it`
  - `tests/test_routing_workers.py::test_a_track_held_only_in_a_vocal_sub_is_placed`
  - `tests/test_routing_workers.py::test_a_track_held_only_outside_the_tree_is_unplaced`
  - `tests/test_routing_workers.py::test_the_unplaced_check_run_owes_no_import_before_the_tracks_are_filed`

Old text:

```
    return [key for key in by_id if key not in held]
```

New text:

```
    return list(by_id)
```

### `u91.U3_tree_absent_refusal`

_routing_tree_node: answer the playlist root when the tree is absent or wrong typed, instead of refusing governed-tree-absent

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U3_tree_absent_refusal`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_refuses[a-playlist-of-that-name]`
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_refuses[absent]`

Old text:

```
    if isinstance(node, rbxml.NodeSpan):
        return node
    why = node if isinstance(node, str) else f"no folder named {display!r} sits under ROOT"
```

New text:

```
    if root is not None:
        return node if isinstance(node, rbxml.NodeSpan) else root
    why = node if isinstance(node, str) else f"no folder named {display!r} sits under ROOT"
```

### `u91.U4_tree_type`

_routing_tree_node: look the tree up as a PLAYLIST rather than a folder

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U4_tree_type`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 16 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates`
  - `tests/test_routing_workers.py::test_a_missing_genre_folder_is_a_skipped_write_and_no_folder_is_invented`
  - `tests/test_routing_workers.py::test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing`
  - `tests/test_routing_workers.py::test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it`
  - `tests/test_routing_workers.py::test_a_second_sweep_over_its_own_output_places_nothing`
  - `tests/test_routing_workers.py::test_a_sweep_that_could_place_nothing_is_blocked_not_done`
  - `tests/test_routing_workers.py::test_a_track_held_only_in_a_vocal_sub_is_placed`
  - `tests/test_routing_workers.py::test_a_track_held_only_outside_the_tree_is_unplaced`
  - `tests/test_routing_workers.py::test_an_export_with_no_routing_tree_refuses[a-playlist-of-that-name]`
  - `tests/test_routing_workers.py::test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created`
  - `tests/test_routing_workers.py::test_an_unreadable_track_is_a_warning_and_the_rest_are_placed`
  - `tests/test_routing_workers.py::test_no_tempo_or_bpm_attribute_differs_after_the_sweep`
  - `tests/test_routing_workers.py::test_the_sweep_runs_with_rekordbox_open_and_opens_no_database`
  - `tests/test_routing_workers.py::test_the_unplaced_check_run_owes_no_import_before_the_tracks_are_filed`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        else rbxml.direct_child(content, root, display, rbxml.FOLDER_TYPE)
```

New text:

```
        else rbxml.direct_child(content, root, display, rbxml.PLAYLIST_TYPE)
```

### `u91.U5_creating_writer`

apply_unplaced_export: call the NON creating writer, so a bucket with no sub leaves its tracks unplaced

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U5_creating_writer`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 7 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates`
  - `tests/test_routing_workers.py::test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing`
  - `tests/test_routing_workers.py::test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it`
  - `tests/test_routing_workers.py::test_a_second_sweep_over_its_own_output_places_nothing`
  - `tests/test_routing_workers.py::test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created`
  - `tests/test_routing_workers.py::test_the_unplaced_check_run_owes_no_import_before_the_tracks_are_filed`

Old text:

```
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
```

New text:

```
    report = trees.apply_playlist_changes(plan, buffer, tree=tree)
```

### `u91.U7_nothing_written`

apply_unplaced_export: write the file even when nothing was inserted

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U7_nothing_written`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_second_sweep_over_its_own_output_places_nothing`
  - `tests/test_routing_workers.py::test_a_sweep_that_could_place_nothing_is_blocked_not_done`

Old text:

```
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
    if not report.inserted:
```

New text:

```
    report = trees.apply_unplaced_changes(plan, buffer, tree=tree)
    if False:
```

### `u91.U8_suffix`

PLACED_SUFFIX: write _routed.xml, the inbox sweep's name, so an unimported inbox routing is replaced

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U8_suffix`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 12 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_bare_lf_before_a_folder_close_is_a_skipped_create_and_the_file_parses`
  - `tests/test_routing_workers.py::test_a_calibrated_vocal_track_lands_in_a_vocal_sub_the_sweep_creates`
  - `tests/test_routing_workers.py::test_a_missing_genre_folder_is_a_skipped_write_and_no_folder_is_invented`
  - `tests/test_routing_workers.py::test_a_namesake_genre_folder_outside_the_routing_tree_takes_nothing`
  - `tests/test_routing_workers.py::test_a_placed_track_is_untouched_even_where_the_declaration_would_not_put_it`
  - `tests/test_routing_workers.py::test_a_second_sweep_over_its_own_output_places_nothing`
  - `tests/test_routing_workers.py::test_a_track_held_only_in_a_vocal_sub_is_placed`
  - `tests/test_routing_workers.py::test_a_track_held_only_outside_the_tree_is_unplaced`
  - `tests/test_routing_workers.py::test_an_unplaced_track_lands_in_its_sub_and_an_absent_sub_is_created`
  - `tests/test_routing_workers.py::test_an_unreadable_track_is_a_warning_and_the_rest_are_placed`
  - `tests/test_routing_workers.py::test_no_tempo_or_bpm_attribute_differs_after_the_sweep`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
PLACED_SUFFIX = "_placed.xml"
```

New text:

```
PLACED_SUFFIX = "_routed.xml"
```

### `u91.U9_cut_over_refusal`

_refuse_off_the_bridge: never refuse a tree that has cut over (shared with route inbox --export)

- File: `src/cratekit/write/routing_export.py`
- Source: `u91.json`, row `U9_cut_over_refusal`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_cut_over_tree_refuses_the_sweep_and_writes_nothing`
  - `tests/test_routing_workers.py::test_a_native_routing_tree_refuses_before_the_plan_is_offered`

Old text:

```
    if tree_registry.read(cfg).is_database_native(declared.tree.id):
```

New text:

```
    if False:
```

### `r318.P1_withdrawn_branch_removed`

row_placement: never answer withdrawn, so a track imported then removed in rekordbox is reported as never imported and the person is sent to import it again

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P1_withdrawn_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 425 against a baseline of 425
- Kills: 5 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_a_location_reaching_only_soft_deleted_rows_is_withdrawn`
  - `tests/test_deferred_routing.py::test_a_track_deleted_after_import_is_surfaced`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn-twice]`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[withdrawn]`

Old text:

```
    if removed.outcome in (trees.MatchOutcome.MATCHED, trees.MatchOutcome.AMBIGUOUS):
        # A row exists and every one of them is a tombstone: imported once, then
```

New text:

```
    if False:
        # A row exists and every one of them is a tombstone: imported once, then
```

### `r318.P4_ambiguous_reads_not_imported`

row_placement: two live rows claiming a location answer not imported instead of ambiguous

- File: `src/cratekit/write/routing_pass.py`
- Source: `r318.json`, row `P4_ambiguous_reads_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_intake_imported.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 425 against a baseline of 425
- Kills: 3 (killed)
- Killed:
  - `tests/test_deferred_routing.py::test_two_active_rows_on_one_location_are_ambiguous_and_never_written`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_the_placement_of_a_row_answer_is_one_rule[ambiguous]`

Old text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.AMBIGUOUS
```

New text:

```
    if alive.outcome is trees.MatchOutcome.AMBIGUOUS:
        return Placement.NOT_IMPORTED
```

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_sub.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_filing.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 817 against a baseline of 817
- Kills: 63 (killed)
- Killed:
  - `tests/test_adopt_former_place.py::test_a_library_whose_own_taxonomy_still_has_the_sub_moves_no_track_of_that_sub`
  - `tests/test_adopt_former_place.py::test_a_renamed_old_playlist_is_found_through_the_node_recorded_under_the_old_sub`
  - `tests/test_adopt_former_place.py::test_a_track_in_the_old_playlist_holds_the_former_place_in_both_buckets`
  - `tests/test_adopt_former_place.py::test_an_approved_move_files_each_track_in_its_band_and_a_second_plans_nothing`
  - `tests/test_adopt_former_place.py::test_the_gate_shows_every_track_leaving_the_old_playlist_and_every_one_left`
  - `tests/test_adopt_jazz_folder.py::test_a_track_in_the_old_jazz_playlist_holds_its_former_place_in_both_buckets`
  - `tests/test_adopt_jazz_folder.py::test_an_approved_move_files_jazz_in_its_bands_and_keeps_every_other_membership`
  - `tests/test_adopt_jazz_folder.py::test_the_gate_shows_every_jazz_track_moving_and_no_other_track`
  - `tests/test_adopt_move.py::test_a_cancelled_move_exits_with_its_own_cause_and_not_ok`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - `tests/test_adopt_move.py::test_a_failure_in_the_additions_writes_nothing_at_all`
  - `tests/test_adopt_move.py::test_a_job_another_verb_queued_is_never_driven_through_this_gate`
  - `tests/test_adopt_move.py::test_a_parked_move_leaves_blocked_and_non_zero`
  - `tests/test_adopt_move.py::test_a_reading_that_changed_after_the_approval_is_a_stale_decision`
  - `tests/test_adopt_move.py::test_a_refusal_at_the_second_commit_keeps_its_own_cause_and_the_job_says_in_both`
  - ... and 48 more, see the JSON sidecar

Old text:

```
    for genre in bucket.genre_subs:
        if genre.id == sub_id:
            return bucket.display, genre.display
```

New text:

```
(empty)
```

### `r1991.T1_removed_node_recorded`

writer: count a node rekordbox removed among the nodes at a pair, so the removed row the writer found by name is recorded as the destination

- File: `src/cratekit/write/trees.py`
- Source: `r1991.json`, row `T1_removed_node_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_genre_favorites.py`, `tests/test_genre_retag.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_rebuild_growth.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_shared_homes.py`, `tests/test_tag_set_move.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_write_session.py`, `tests/test_xml_splice_golden.py`
- Collected: 1590 against a baseline of 1590
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_records_no_node_rekordbox_removed`

Old text:

```
        if not node.removed:
            standing.setdefault
```

New text:

```
        if True:
            standing.setdefault
```

### `r1991.T2_first_of_two_recorded`

writer: record the first of two live nodes at one pair, so the record binds a destination to a folder chosen by position

- File: `src/cratekit/write/trees.py`
- Source: `r1991.json`, row `T2_first_of_two_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_genre_favorites.py`, `tests/test_genre_retag.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_rebuild_growth.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_shared_homes.py`, `tests/test_tag_set_move.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_write_session.py`, `tests/test_xml_splice_golden.py`
- Collected: 1590 against a baseline of 1590
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_never_chooses_between_two_live_nodes_at_one_pair`

Old text:

```
        if place is None or len(nodes) != 1:
```

New text:

```
        if place is None or not nodes:
```

### `r1991.T3_unfiled_pair_recorded`

writer: record every pair of record_as, not only those it filed into, so a standing playlist it did not fill becomes a destination

- File: `src/cratekit/write/trees.py`
- Source: `r1991.json`, row `T3_unfiled_pair_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_genre_favorites.py`, `tests/test_genre_retag.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_rebuild_growth.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_shared_homes.py`, `tests/test_tag_set_move.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_write_session.py`, `tests/test_xml_splice_golden.py`
- Collected: 1590 against a baseline of 1590
- Kills: 1 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_records_only_a_pair_it_filed_into`

Old text:

```
    for pair in sorted(set(filed)):
```

New text:

```
    for pair in sorted(record_as):
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

### `r1991.T5_moves_bound_destinations`

writer: record without keep_recorded, so adoption moves a destination a rebuild bound and can raise after the landed write

- File: `src/cratekit/write/trees.py`
- Source: `r1991.json`, row `T5_moves_bound_destinations`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_move.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_deletion_streaming.py`, `tests/test_genre_favorites.py`, `tests/test_genre_retag.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_landing_labels.py`, `tests/test_rebuild.py`, `tests/test_rebuild_growth.py`, `tests/test_routing_workers.py`, `tests/test_second_genre.py`, `tests/test_shared_homes.py`, `tests/test_tag_set_move.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_unrecorded_genre_folder.py`, `tests/test_write_session.py`, `tests/test_xml_splice_golden.py`
- Collected: 1590 against a baseline of 1590
- Kills: 2 (killed)
- Killed:
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_gives_no_node_a_second_destination`
  - `tests/test_unrecorded_genre_folder.py::test_the_writer_never_moves_a_destination_the_record_already_binds`

Old text:

```
        convergence.record_nodes(cfg, tree_id, found, keep_recorded=True)
```

New text:

```
        convergence.record_nodes(cfg, tree_id, found, keep_recorded=False)
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

### `r375-b.T3_a_noop_claims_a_commit`

_record_membership_commit: record a commit for a pass that added nothing, so a restore refuses over sessions that created nothing

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T3_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    session.record_commit(
```

### `r375-b.T4_noop_bound_off_by_one`

_record_membership_commit: move the no-op bound by one, so a pass that added exactly one membership claims no commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T4_noop_bound_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 189 against a baseline of 189
- Kills: 5 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`
  - `tests/test_tree_writer.py::test_a_pass_that_added_nothing_claims_no_commit`

Old text:

```
    if added <= 0:
        return
    session.record_commit(
```

New text:

```
    if added <= 1:
        return
    session.record_commit(
```

### `r375-b.T5_witnessed_commit_not_recorded`

write_tree_membership: ignore the witness, so a commit that landed and then raised closes as though nothing landed

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T5_witnessed_commit_not_recorded`
- Moved: U298 moved write_tree_membership's failure path, the quiet rollback and the witnessed commit record, into trees._undo_unless_landed, which its except branch now calls; the same witness check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`

Old text:

```
    if witness.landed:
        _record_membership_commit(record, tree_id, added, cfg)
```

New text:

```
    if False:
        _record_membership_commit(record, tree_id, added, cfg)
```

### `r375-b.T7_commit_recorded_after_the_fingerprint`

write_tree_membership: record the commit AFTER the fingerprint write, so a failure there closes a committed write as empty

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T7_commit_recorded_after_the_fingerprint`
- Moved: write_tree_membership's commit record and fingerprint now read from the _Run record and their comment is shortened; the same two calls swapped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`

Old text:

```
        _record_membership_commit(record, tree_id, run.added, cfg)

        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT, or the next run
        # would read this session's own write as an out of band restore. Outside
        # the try, since the commit has landed and nothing is pending.
        convergence.record_fingerprint(cfg, db)

```

New text:

```
        # THE FINGERPRINT IS TAKEN AT THE CLOSE, AFTER THE COMMIT, or the next run
        # would read this session's own write as an out of band restore. Outside
        # the try, since the commit has landed and nothing is pending.
        convergence.record_fingerprint(cfg, db)
        _record_membership_commit(record, tree_id, run.added, cfg)

```

### `r375-b.T8_counts_filed_as_updates`

_record_membership_commit: file the added memberships as updated rather than created

- File: `src/cratekit/write/trees.py`
- Source: `r375-b.json`, row `T8_counts_filed_as_updates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 189 against a baseline of 189
- Kills: 4 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`

Old text:

```
session.TreeChange(tree=tree_id, created=added)
```

New text:

```
session.TreeChange(tree=tree_id, updated=added)
```

### `r375-c.T6_every_raise_read_as_a_commit_again`

write_tree_membership: record a commit on every raise. Batch B read this as ZERO; measured again after test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit

- File: `src/cratekit/write/trees.py`
- Source: `r375-c.json`, row `T6_every_raise_read_as_a_commit_again`
- Moved: U298 moved write_tree_membership's failure path, the quiet rollback and the witnessed commit record, into trees._undo_unless_landed, which its except branch now calls; the same witness check
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_rebuild.py`, `tests/test_adopt_apply_cli.py`
- Collected: 189 against a baseline of 189
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`

Old text:

```
    if witness.landed:
        _record_membership_commit(record, tree_id, added, cfg)
```

New text:

```
    if True:
        _record_membership_commit(record, tree_id, added, cfg)
```

### `u298.H13_capture_verified`

attached_capture: a capture that fails its check is written past

- File: `src/cratekit/write/trees.py`
- Source: `u298.json`, row `H13_capture_verified`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 308 against a baseline of 308
- Kills: 3 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_write_commits_behind_a_verified_capture`
  - `tests/test_write_session.py::test_the_shared_capture_attaches_before_it_judges`
  - `tests/test_write_session.py::test_the_tree_writers_reach_for_the_session_spine`

Old text:

```
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture
```

New text:

```
    session.attach_capture(record, capture.root, cfg)
    return record, capture
```

### `u298.H14_capture_attached_before_judged`

attached_capture: a capture that fails its check is never attached to the session record

- File: `src/cratekit/write/trees.py`
- Source: `u298.json`, row `H14_capture_attached_before_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_shared_homes.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 308 against a baseline of 308
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_the_write_commits_behind_a_verified_capture`
  - `tests/test_write_session.py::test_the_shared_capture_attaches_before_it_judges`

Old text:

```
    session.attach_capture(record, capture.root, cfg)
    snapshot.assert_verified(capture)
    return record, capture
```

New text:

```
    snapshot.assert_verified(capture)
    session.attach_capture(record, capture.root, cfg)
    return record, capture
```

### `u302.W11_landed_commit_recorded_as_zero`

_Run.undo_unless_landed: a commit that landed and raised records no additions

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W11_landed_commit_recorded_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`

Old text:

```
        _undo_unless_landed(self.db, witness, self.record, self.tree_id, self.added, self.cfg)
```

New text:

```
        _undo_unless_landed(self.db, witness, self.record, self.tree_id, 0, self.cfg)
```

### `u302.W14c_root_read_back_unchecked`

what W14 holds: _root_row hands an absent adopted root on as None instead of refusing it, the layer that refuses a root W14 reads as present

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W14c_root_read_back_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`, `tests/test_tree_writer.py`
- Collected: 393 against a baseline of 393
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_root_the_probe_vouched_for_but_the_database_lacks_is_refused`

Old text:

```
    row = db.get_playlist(ID=str(root_id))
    if row is None:
```

New text:

```
    row = db.get_playlist(ID=str(root_id))
    if False:
```

### `u302.W17_landed_removal_not_recorded`

_remove_leavers: a removal commit that landed and then raised is not recorded

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W17_landed_removal_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_write_session.py`, `tests/test_adopt_move.py`
- Collected: 295 against a baseline of 295
- Kills: 1 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_moves_removal_commit_that_lands_and_then_raises_is_still_recorded`

Old text:

```
                _record_removal_commit(run.record, run.tree_id, run.removed, run.cfg)
```

New text:

```
                pass
```

### `u302.W9c_configuration_rules_dropped`

what W9 holds: prefix_rules with no caller map returns no rules, so a recorded path is never resolved through the configuration

- File: `src/cratekit/write/trees.py`
- Source: `u302.json`, row `W9c_configuration_rules_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tree_writer.py`, `tests/test_naming_apply_cli.py`, `tests/test_routing_workers.py`, `tests/test_deferred_routing.py`
- Collected: 438 against a baseline of 438
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_apply_cli.py::test_a_row_under_a_remapped_volume_still_protects_its_file[prefix_map0]`
  - `tests/test_routing_workers.py::test_an_export_location_under_a_retired_volume_name_resolves_through_the_prefix_map`

Old text:

```
        return list(locations.prefix_rules(cfg.resolved_prefix_map()))
```

New text:

```
        return []
```

### `u77-b.B6_trial_id`

check_record_labels_tree: trial every year with no id, so the writer returns from a held playlist before its three layout refusals and the check passes what the write refuses

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B6_trial_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_a_held_year_playlist_the_writer_cannot_extend_refuses_before_any_move`
  - `tests/test_tree_writer.py::test_the_catalog_check_reaches_a_held_playlist_the_writer_cannot_extend`

Old text:

```
trial, label, [(f"{label} {year}", [_TRIAL_ID]) for year in years], target
```

New text:

```
trial, label, [(f"{label} {year}", []) for year in years], target
```

### `u77-b.B7_check_empty_catalog`

check_record_labels_tree: resolve the catalog tree even when nothing would be written, so an undeclared tree refuses a landing that has no label row

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B7_check_empty_catalog`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing[favourites]`
  - `tests/test_landing_labels.py::test_an_undeclared_catalog_tree_costs_a_landing_with_no_label_row_nothing[no-manifest]`
  - `tests/test_tree_writer.py::test_the_catalog_check_asks_nothing_when_there_is_nothing_to_write`

Old text:

```
    if not catalog:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

New text:

```
    if catalog is None:
        return
    target = _catalog_tree(declared, registry, tree)
    trial
```

### `u77-b.B8_label_write_order`

insert_record_labels_trees: write the sources first name first, so a new tree reads Z to A

- File: `src/cratekit/write/trees.py`
- Source: `u77-b.json`, row `B8_label_write_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing_labels.py`, `tests/test_landing.py`, `tests/test_intake_land.py`, `tests/test_tree_writer.py`, `tests/test_listdoc.py`, `tests/test_xml_splice_golden.py`
- Collected: 254 against a baseline of 254
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`
  - `tests/test_tree_writer.py::test_several_sources_are_one_write_and_a_new_tree_reads_a_to_z`

Old text:

```
    for label in sorted(catalog, reverse=True):
        _insert_catalog(content,
```

New text:

```
    for label in sorted(catalog):
        _insert_catalog(content,
```

### `u88-b.W1_replace_not_append`

add_to_root_playlist: write the new tracks alone, so the playlist's members are replaced

- File: `src/cratekit/write/trees.py`
- Source: `u88-b.json`, row `W1_replace_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_track_is_never_removed_from_the_playlist`
  - `tests/test_routing_workers.py::test_the_add_only_writer_counts_each_new_track_once`

Old text:

```
    warning = rbxml.insert_root_playlist(name, [*existing, *new], content)
```

New text:

```
    warning = rbxml.insert_root_playlist(name, new, content)
```

### `u312.E1_exited_ignores_expected`

exited: hold every drive to exit OK whatever code the test expects, so a refusal the test expects reads as a failure and an OK the test forbids passes

- File: `tests/_sync_builders.py`
- Source: `u312.json`, row `E1_exited_ignores_expected`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_resume_one.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 196 against a baseline of 196
- Kills: 76 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_over_a_recent_export_carries_no_age_warning`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`
  - `tests/test_sync_all.py::test_the_composed_gate_shows_the_tracks_the_sweeps_digest_covers`
  - `tests/test_sync_all.py::test_the_composed_pass_carries_the_favourites_verb_standing_warning`
  - ... and 61 more, see the JSON sidecar

Old text:

```
    assert code == int(expected), f"exited {code}, expected {int(expected)}: {envelope!r}"
```

New text:

```
    assert code == int(ExitCode.OK), f"exited {code}, expected {int(expected)}: {envelope!r}"
```

### `u232.A1_platform_stub`

_no_host_process_table: leave core.processes._platform as psutil, so the careful scan reads the host

- File: `tests/conftest.py`
- Source: `u232.json`, row `A1_platform_stub`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`, `tests/test_process_scan.py`, `tests/test_sync_bandcamp.py`, `tests/test_process_scan_jobs.py`
- Collected: 90 against a baseline of 90
- Kills: 4 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_the_careful_scan_reads_no_rekordbox_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        monkeypatch.setattr(processes, "_platform", lambda: empty)
```

New text:

```
        pass
```

### `u232.A2_pyrekordbox_stub`

_no_host_process_table: leave pyrekordbox's get_process_id walking the host, the refused cut's own route

- File: `tests/conftest.py`
- Source: `u232.json`, row `A2_pyrekordbox_stub`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`, `tests/test_process_scan.py`, `tests/test_sync_bandcamp.py`, `tests/test_process_scan_jobs.py`
- Collected: 90 against a baseline of 90
- Kills: 26 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_pyrekordbox_reads_no_rekordbox_with_rekordbox_open_on_the_host`
  - `tests/test_host_process_table.py::test_the_writers_guard_reads_clear_with_rekordbox_open_on_the_host`
  - `tests/test_sync_bandcamp.py::test_a_batch_of_a_label_and_an_unregistered_seller_files_by_tag_under_a_plain_name`
  - `tests/test_sync_bandcamp.py::test_a_failed_rehearsal_plans_no_live_landing`
  - `tests/test_sync_bandcamp.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_bandcamp.py::test_a_fetch_failed_by_a_transient_answer_ends_the_verb_and_lands_nothing`
  - `tests/test_sync_bandcamp.py::test_a_fetch_parked_by_the_session_ends_blocked_and_the_next_run_drives_it_on`
  - `tests/test_sync_bandcamp.py::test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label`
  - `tests/test_sync_bandcamp.py::test_a_labels_new_release_and_its_owned_one_reach_the_gate_named_for_the_label`
  - `tests/test_sync_bandcamp.py::test_a_plan_holding_only_part_owned_releases_still_fetches_the_rest`
  - `tests/test_sync_bandcamp.py::test_a_rehearsal_that_needs_the_acknowledgment_names_the_rehearsal_then_the_landing`
  - `tests/test_sync_bandcamp.py::test_a_release_refused_by_two_fetches_is_named_once`
  - `tests/test_sync_bandcamp.py::test_a_release_refused_for_good_is_recorded_and_nothing_is_landed_over_none`
  - `tests/test_sync_bandcamp.py::test_a_second_run_after_a_landing_finds_nothing_new_and_lands_nothing`
  - ... and 11 more, see the JSON sidecar

Old text:

```
            monkeypatch.setattr(utils, "get_process_id", no_process)
```

New text:

```
            pass
```

### `u232.A8_opt_in`

_no_host_process_table: ignore the real_process_table marker, so no test can reach the real table

- File: `tests/conftest.py`
- Source: `u232.json`, row `A8_opt_in`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`, `tests/test_process_scan.py`
- Collected: 55 against a baseline of 55
- Kills: 4 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_opted_in_reads_the_real_host`
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`
  - `tests/test_host_process_table.py::test_the_fake_host_is_what_the_real_scan_reads`
  - `tests/test_process_scan.py::test_the_seam_is_psutil_when_nothing_replaces_it`

Old text:

```
    if request.node.get_closest_marker(REAL_PROCESS_TABLE) is not None:
        yield
        return
    import psutil
```

New text:

```
    import psutil
```

### `u312.L1_parser_cache_ignores_membership`

_less_work: key the cached command tree on nothing, so a tree built with one set of modules answers a test run under another

- File: `tests/test_outbound_workers.py`
- Source: `u312.json`, row `L1_parser_cache_ignores_membership`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_export_set_rename.py`, `tests/test_sync_removed.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`, `tests/test_taxonomy_upgrade.py`
- Collected: 424 against a baseline of 424
- Kills: 23 (killed)
- Killed:
  - `tests/test_sync_removed.py::test_delete_review_after_the_apply_offers_the_removed_file_and_none_other`
  - `tests/test_vocals_cli.py::test_a_file_finalized_with_no_voxlevel_is_scored_once_the_model_is_bound`
  - `tests/test_vocals_cli.py::test_a_folder_with_no_audio_queues_nothing`
  - `tests/test_vocals_cli.py::test_a_missing_checkpoint_is_refused_at_the_queue_and_named`
  - `tests/test_vocals_cli.py::test_a_nested_file_deleted_after_the_vocals_queue_refuses_that_item_only`
  - `tests/test_vocals_cli.py::test_a_one_level_vocals_resume_says_nothing_about_a_walk_it_never_did`
  - `tests/test_vocals_cli.py::test_a_prefixed_file_is_scored_by_analyze_vocals_and_not_skipped`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_says_which_linked_folders_it_did_not_walk`
  - `tests/test_vocals_cli.py::test_a_recursive_vocals_pass_scores_the_nested_file_the_item_names`
  - `tests/test_vocals_cli.py::test_a_slim_worker_refuses_at_the_queue_rather_than_reporting_done`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[no-sidecar-or-dot-directory]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[one-level-by-default]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[one-name-in-two-folders]`
  - `tests/test_vocals_cli.py::test_a_vocals_pass_queues_each_file_its_walk_finds_in_sorted_order[recursive-every-file-once]`
  - `tests/test_vocals_cli.py::test_an_oversize_track_is_refused_by_the_restamp_verb_and_keeps_its_tags`
  - ... and 8 more, see the JSON sidecar

Old text:

```
        membership = cli._membership()
```

New text:

```
        membership = ()
```

### `u232.A10_real_walk_restored`

real_probes: leave pyrekordbox's walk stubbed, so the U211 tests over a dying process_iter read nothing

- File: `tests/test_process_scan.py`
- Source: `u232.json`, row `A10_real_walk_restored`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`
- Collected: 46 against a baseline of 46
- Kills: 8 (killed)
- Killed:
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_pyrekordbox_alone_lets_the_dying_process_escape`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`

Old text:

```
    monkeypatch.setattr(pyrekordbox.utils, "get_process_id", REAL_WALK)
```

New text:

```
    pass
```

### `u28-skills-independent.L11_rule_d_scanner`

rule (d) stops delegating to the portability scanner, so no personal literal in a shipped skill is found

- File: `tests/test_skills_lint.py`
- Source: `u28-skills-independent.json`, row `L11_rule_d_scanner`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_lint.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_skills_lint.py::test_a_rule_reports_what_it_finds[home literal]`
  - `tests/test_skills_lint.py::test_a_volume_literal_in_any_skill_fails`

Old text:

```
        for violation in scan.portability_violations(
            text, identity_tokens=scan.machine_identity_tokens()
        ):
```

New text:

```
        for violation in []:
```

### `r658-b.S7_tombstone_full_disk`

Drop the scoped refusing store write

- File: `tests/test_uncredited_tombstone.py`
- Source: `r658-b.json`, row `S7_tombstone_full_disk`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_uncredited_tombstone.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_uncredited_tombstone.py::test_a_record_that_cannot_be_written_leaves_neither_half`

Old text:

```
        full_disk.setattr(review.DecisionStore, "_write", refuses)

```

New text:

```
(empty)
```

