# Mutation table: u302-replay-before-a

Measured by `scripts/mutate.py` on 2026-11-22 20:42 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 26.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 10, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `/home/user/cratekit/.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 121 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r239-b.S2_unplaced_key_off` | `src/cratekit/write/routing_cli.py` | user | 7 file(s) | 733 | 2 | killed |
| `r290-author.S08_route_resort_call_removed` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 323 | 11 | killed |
| `r312.W2_worker_writes_nothing` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 8 | killed |
| `r312.W3_success_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 5 | killed |
| `r312.W4_failure_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r312.W5_cause_steps_replaced` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r312.W6_type_not_carried` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 126 | 1 | killed |
| `r312.W7b_pre_drive_refusal_extended` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `r312.W8_list_not_by_job` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r313.G7_handler_opens_with_write_intent` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 1611 | 1 | killed |
| `r316.M3_inbox_gaps_leak_into_totals` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r318-b.C7_trees_not_deduplicated` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318-b.N1_no_native_key_dropped` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 244 | 1 | killed |
| `r318-b.W2_cap_halved` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C1_skipped_files_always_empty` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 4 | killed |
| `r318.C2_tombstones_not_consulted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C3_ambiguous_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C4_withdrawn_ids_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C5_withdrawn_single_id_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C6_trees_emptied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 2 | killed |
| `r318.C8_path_reduced_to_name` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.C9_warnings_not_emitted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 4 | killed |
| `r318.W1_cap_not_applied` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W3_count_is_named_not_whole` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W4_reasons_unsorted` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r318.W5_next_act_dropped` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `r501-d.R2_settled_is_not_imported` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 329 | 1 | killed |
| `r501-d.R3_pass_is_proof` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 329 | 1 | killed |
| `r685-a.V1_route_inbox_export_reads_the_shipped_text` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 215 | 4 | killed |
| `r686.E1_tracks_counts_every_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E2_routed_counts_vocal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `r686.E4_long_tracks_intake_only` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r686.E5_warnings_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r686.E6_gaps_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r686.E7_subs_not_named` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.B1_owed_rating_blocks_the_answer` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.C1_rates_flag_ignored` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.C2_no_energy_counted` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `r688.C3_files_not_rows` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.G1_zero_owed_still_warns` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `r688.G2_count_off_by_one` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 7 | killed |
| `r688.N1_long_track_change_not_a_write` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.U1_hand_rated_counted` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r688.U2_missing_attribute_counted` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 8 | killed |
| `r688.U3_empty_rating_not_unrated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r688.V1_applied_envelope_drops_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 6 | killed |
| `r688.V2_gate_drops_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r688.V3_declined_envelope_drops_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r688.W1_rating_written_again` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `r691.F1_routed_counts_vocal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `r691.F2_trees_left_off` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F3_planner_warnings_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.F4_gaps_dropped_from_facts` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r691.K1_empty_folder_plan_names_no_tree` | `src/cratekit/write/routing_cli.py` | maintainer | 1 file(s) | 197 | 1 | killed |
| `r691.K2_gaps_not_carried_to_the_apply` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N3_declined_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.N4_inbox_empty_envelope_drops_the_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `r691.P1_destination_left_off_the_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `r691.P2_vocal_left_off_the_item` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `r691.P4_digest_over_the_file_list` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `r691.W1_write_ignores_the_plan` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 22 | killed |
| `u132.W6_resort_note` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W3_gate_column` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 3 | killed |
| `u155.W4_gate_count` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 3 | killed |
| `u155.W5_owed_once` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W6_inbox_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u155.W7_export_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 244 | 1 | killed |
| `u219-composites.G6_answer_pinned` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 221 | 1 | killed |
| `u219.G2_nothing_to_add` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G3_adds_frozen` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 21 | killed |
| `u219.G4_worker_own_tree` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.G5_resume_run` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.M3_due_again_said` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.R1_routed_trees` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 12 | killed |
| `u219.R2_inbox_routed_only` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.R3_left_alone_named` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u53-routing-and-rebuild-workers.A3_empty_folder_shortcircuit_removed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u53-routing-and-rebuild-workers.A5_applied_always_true` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R1_resort_drives_a_foreign_job` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.U1_unplaced_constant_empty` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `u53-routing-and-rebuild-workers.U2_compared_true_without_a_tree` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u53-routing-and-rebuild-workers.U3_held_never_populated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.U4_tombstones_reported` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I1_native_filter_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E14_non_creating_writer` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E15_nothing_inserted_nothing_written` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u86-b.E16_never_in_place` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 32 | killed |
| `u86-b.E22_export_remedy` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86-b.E23_export_branch` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 57 | killed |
| `u86.E10_unreadable_not_routed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `u86.E11_is_file` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `u86.E12_prefix_map` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E2_governed_tree` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E3_mount_guard` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u86.E4_export_absent` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E6_intake_absent` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u86.E9_row_absent` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u87.G1a_empty_not_unrated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `u87.G1b_any_value_unrated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `u87.G1c_absent_attribute_unrated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 8 | killed |
| `u87.G2_rates_flag` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 5 | killed |
| `u88.D1_zero_is_a_length` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.D2_prefix_digits` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.D3_absent_attribute` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 41 | killed |
| `u88.I1_items_outside_intake` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `u88.I2_item_flag` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `u88.L1_bound_strict` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L2_bound_coefficient` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L3_existing_members_replanned` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L4_folder_warning_dropped` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.L5_folder_refusal_bypassed` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u88.T1_unreadable_count` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89-e6.E6_vox_warnings` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.E1_export_threshold` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.E2_no_vox_subs` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 8 | killed |
| `u89.E3_subs_uncalibrated` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 9 | killed |
| `u89.E4_undeclared_sub` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.E5_unreachable_tree` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.W1_resort_worker` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91-b.P1_inbox_decide_rows` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91-b.U6_tree_named` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U10_unmounted_refusal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u91.U12_write_warnings` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U14_no_native_warning` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U15_export_branch` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 18 | killed |
| `u91.U17_decide_unreadable` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 3 | killed |
| `u91.U18_unplaced_threshold` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
| `u91.U1_unplaced_rule` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 4 | killed |
| `u91.U3_tree_absent_refusal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U4_tree_type` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 16 | killed |
| `u91.U5_creating_writer` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 7 | killed |
| `u91.U7_nothing_written` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |
| `u91.U8_suffix` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 12 | killed |
| `u91.U9_cut_over_refusal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 2 | killed |

## Zero rows and what they owe

- `u86.E3_mount_guard` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u91.U10_unmounted_refusal` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r239-b.S2_unplaced_key_off`

route unplaced's open, unplaced_items, passes unlock=False again

- File: `src/cratekit/write/routing_cli.py`
- Source: `r239-b.json`, row `S2_unplaced_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 2 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`

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

### `r290-author.S08_route_resort_call_removed`

Remove the one jobs.raise_for_state call from write/routing_cli.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/write/routing_cli.py`
- Source: `r290-author.json`, row `S08_route_resort_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_routing_workers.py`
- Collected: 323 against a baseline of 323
- Kills: 11 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[route.resort]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[route.resort]`
  - `tests/test_job_outcome.py::test_every_function_that_drives_a_job_maps_its_ending_afterwards`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_with_nothing_left_behind_adds_no_step`
  - `tests/test_routing_workers.py::test_a_resume_whose_items_did_not_all_succeed_is_not_an_ok_exit[resort]`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
```

### `r312.W2_worker_writes_nothing`

handle_resort: the item report always says nothing was left

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W2_worker_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
            "left_behind": [rebuild.left_behind_record(entry) for entry in left],
```

New text:

```
            "left_behind": [],
```

### `r312.W3_success_exit_silent`

_resume: the success envelope carries no leftover warning

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W3_success_exit_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
                *rebuild.left_behind_warnings(records, listed_in=listed_in),

```

New text:

```
(empty)
```

### `r312.W4_failure_exit_silent`

_resume: a refusal is re-raised as it came, the leftovers never added to it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W4_failure_exit_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`

Old text:

```
        raise _with_left_behind(failed, frozen, job.job_id) from failed
```

New text:

```
        raise
```

### `r312.W5_cause_steps_replaced`

_with_left_behind: replace the recorded steps with the leftover step, not append to them

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W5_cause_steps_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`

Old text:

```
                cause.remediation, steps=(*cause.remediation.steps, message)
```

New text:

```
                cause.remediation, steps=(message,)
```

### `r312.W6_type_not_carried`

_with_left_behind: rebuild as a plain CratekitError, dropping the blocked or cancelled type

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W6_type_not_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`
- Collected: 126 against a baseline of 126
- Kills: 1 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`

Old text:

```
    return rebuilt(
        error,
        replace(
            cause,
```

New text:

```
    return CratekitError(
        replace(
            cause,
```

### `r312.W7b_pre_drive_refusal_extended`

_resume: drop the guard that re-raises a refusal raised before the drive. Measured ZERO on the first pass over a full run of 9679, then re-measured after test_a_refusal_raised_before_the_drive_carries_no_leftover_step was written against it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W7b_pre_drive_refusal_extended`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`

Old text:

```
        if frozen is None:
            raise
        raise _with_left_behind
```

New text:

```
        raise _with_left_behind
```

### `r312.W8_list_not_by_job`

_left_behind: point at the shared reports directory, not this job's

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W8_list_not_by_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_one_jobs_leftovers_are_not_counted_under_another`
  - `tests/test_routing_workers.py::test_the_whole_list_is_written_where_the_warning_says_it_is`

Old text:

```
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final / job_id)
```

New text:

```
    return records, str(jobs.store_dir(cfg) / RESORT_ARTIFACTS.final)
```

### `r313.G7_handler_opens_with_write_intent`

the unplaced report opens the database with require_closed, so it refuses with rekordbox open

- File: `src/cratekit/write/routing_cli.py`
- Source: `r313.json`, row `G7_handler_opens_with_write_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1611 against a baseline of 1611
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

### `r318-b.C7_trees_not_deduplicated`

_skipped_files: a tree the writer skipped a file in twice is listed twice

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `C7_trees_not_deduplicated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_file_skipped_twice_in_one_tree_names_that_tree_once`

Old text:

```
                "trees": sorted(set(tree_ids)),
```

New text:

```
                "trees": sorted(tree_ids),
```

### `r318-b.N1_no_native_key_dropped`

apply_inbox: the no-native-tree answer carries no skipped_files key, so the payload shape differs by branch

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `N1_no_native_key_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

### `r318-b.W2_cap_halved`

Halve the cap on how many skipped files a warning names, 10 to 5

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318-b.json`, row `W2_cap_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
SKIPPED_NAMED = 10
```

New text:

```
SKIPPED_NAMED = 5
```

### `r318.C1_skipped_files_always_empty`

apply_inbox: skipped_files is always empty, the headline defect R-318 measured, a count and no file

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `C1_skipped_files_always_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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
- Collected: 244 against a baseline of 244
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

### `r318.W1_cap_not_applied`

skipped_warnings: name every file, the cap never applied

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W1_cap_not_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
        named = names[:SKIPPED_NAMED]
```

New text:

```
        named = names
```

### `r318.W3_count_is_named_not_whole`

skipped_warnings: the count is the number named rather than the whole set, so a long list reads as a short one

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W3_count_is_named_not_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warning_counts_every_file_and_caps_the_names`

Old text:

```
                    f"{len(names)} file(s) in the intake folder were not filed because "
```

New text:

```
                    f"{len(named)} file(s) in the intake folder were not filed because "
```

### `r318.W4_reasons_unsorted`

skipped_warnings: reasons in arrival order, so two runs over one state say things in two orders

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W4_reasons_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_skip_warnings_are_one_per_reason_in_a_stable_order`

Old text:

```
    for reason in sorted(by_reason):
```

New text:

```
    for reason in by_reason:
```

### `r318.W5_next_act_dropped`

skipped_warnings: the reason sentence and its next act are replaced by a bare phrase

- File: `src/cratekit/write/routing_cli.py`
- Source: `r318.json`, row `W5_next_act_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

### `r501-d.R2_settled_is_not_imported`

routing_cli._all_settled: count acknowledged tracks as proof, so a run nobody imported is recorded as proven

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R2_settled_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_deferred_routing.py`, `tests/test_routing_workers.py`
- Collected: 329 against a baseline of 329
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`

Old text:

```
    return bool(routed) and not ledger.outstanding(session_id)
```

New text:

```
    return not ledger.outstanding(session_id)
```

### `r501-d.R3_pass_is_proof`

routing_cli._close_if_settled: never record the pass as proof, so after a cutover no landed run can close

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R3_pass_is_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_deferred_routing.py`, `tests/test_routing_workers.py`
- Collected: 329 against a baseline of 329
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`

Old text:

```
        if record.state is session.SessionState.AWAITING_IMPORT and _all_settled(
```

New text:

```
        if False and _all_settled(
```

### `r685-a.V1_route_inbox_export_reads_the_shipped_text`

The export routing verb parses the shipped text instead of loading the library's copy

- File: `src/cratekit/write/routing_cli.py`
- Source: `r685-a.json`, row `V1_route_inbox_export_reads_the_shipped_text`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E1_tracks_counts_every_item`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E2_routed_counts_vocal`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E4_long_tracks_intake_only`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E5_warnings_dropped`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E6_gaps_dropped`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r686.json`, row `E7_subs_not_named`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `B1_owed_rating_blocks_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_second_run_still_owing_ratings_is_nothing_to_route`

Old text:

```
        reason = "nothing-to-route"
    warnings += unrated

```

New text:

```
        reason = "nothing-to-route"
    warnings += unrated
    if unrated and reason == "nothing-to-route":
        reason = "route-blocked"

```

### `r688.C1_rates_flag_ignored`

a bucket declared rates = false is counted as owed a rating

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `C1_rates_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `C2_no_energy_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_with_no_energy_reading_is_filed_and_not_owed`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `C3_files_not_rows`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `G1_zero_owed_still_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_hand_rated_export_track_is_not_owed_a_rating`
  - `tests/test_routing_workers.py::test_a_row_with_no_rating_attribute_is_not_counted_as_owed`
  - `tests/test_routing_workers.py::test_a_second_run_over_its_own_output_adds_nothing`
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_a_track_with_no_energy_reading_is_filed_and_not_owed`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `G2_count_off_by_one`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `N1_long_track_change_not_a_write`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `U1_hand_rated_counted`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `U2_missing_attribute_counted`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `U3_empty_rating_not_unrated`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `V1_applied_envelope_drops_warning`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `V2_gate_drops_warning`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `V3_declined_envelope_drops_warning`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r688.json`, row `W1_rating_written_again`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `F1_routed_counts_vocal`
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

### `r691.P4_digest_over_the_file_list`

the digest is taken over the file list alone, the other half of the defect: a decision recorded against it stays valid while the routing under it changes

- File: `src/cratekit/write/routing_cli.py`
- Source: `r691.json`, row `P4_digest_over_the_file_list`
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
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_names_the_file_it_could_not_file_and_why`
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_over_the_shipped_taxonomy_says_the_vocal_dimension_was_not_compared`
  - `tests/test_routing_workers.py::test_a_file_two_rows_claim_is_reported_ambiguous_with_both_rows`
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_still_names_what_the_finished_tree_left`
  - `tests/test_routing_workers.py::test_a_row_rekordbox_removed_is_reported_withdrawn_not_unimported`
  - `tests/test_routing_workers.py::test_a_second_calibrated_inbox_creates_no_second_vocal_sub`
  - `tests/test_routing_workers.py::test_a_second_process_names_what_the_first_ones_tree_left`
  - `tests/test_routing_workers.py::test_a_taxonomy_with_no_vocal_dimension_warns_on_neither_surface`
  - `tests/test_routing_workers.py::test_an_uncalibrated_inbox_warns_and_files_nothing_under_with_vox`
  - ... and 7 more, see the JSON sidecar

Old text:

```
            placements = planned.placements[tree_id]

```

New text:

```
            placements = ()

```

### `u132.W6_resort_note`

The resort resume carries no skipped step note

- File: `src/cratekit/write/routing_cli.py`
- Source: `u132.json`, row `W6_resort_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`

Old text:

```
                *rebuild.favorites_skipped_warnings(declared, driven),

```

New text:

```
(empty)
```

### `u155.W3_gate_column`

_column: show a genre sub placement in the energy sub column, the round 1 defect

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W3_gate_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W4_gate_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W5_owed_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

### `u155.W6_inbox_item_genre`

plan_inbox: carry an empty genre column on every item, the database gate hiding the second place

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W6_inbox_item_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

### `u155.W7_export_item_genre`

plan_export: carry an empty genre column on every item, the export gate hiding the second place

- File: `src/cratekit/write/routing_cli.py`
- Source: `u155.json`, row `W7_export_item_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 244 against a baseline of 244
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

### `u219-composites.G6_answer_pinned`

_resort_pin: pin the answer to no database file, so an answer over a copy satisfies the live run

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219-composites.json`, row `G6_answer_pinned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 221 against a baseline of 221
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_an_answer_over_one_database_file_does_not_approve_another`

Old text:

```
    return {RESORT_DATABASE_KEY: str(opened)} if opened else None
```

New text:

```
    return None
```

### `u219.G2_nothing_to_add`

route resort: queue a job over a plan with nothing to add

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G2_nothing_to_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`

Old text:

```
    if not adds:
        return ctx.envelope(
```

New text:

```
    if False:
        return ctx.envelope(
```

### `u219.G3_adds_frozen`

route resort: freeze an empty plan in the job, so the worker holds its write to nothing the gate showed

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G3_adds_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 21 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_two_files_that_swap_places_after_the_gate_refuse_by_their_paths`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[above-resort]`
  - `tests/test_routing_workers.py::test_a_calibrated_resume_files_under_with_vox_and_does_not_warn[below-resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[resort]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[resort]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[resort]`
  - `tests/test_routing_workers.py::test_a_queued_resort_runs_its_item_and_the_tree_holds_the_track`
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

### `u219.G4_worker_own_tree`

handle_resort: hand the engine every tree's approved adds, not its own tree's

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G4_worker_own_tree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_each_worker_names_its_own_verb_and_rebuilds_the_item_it_was_handed`

Old text:

```
            if row.get("tree") == tree_id
```

New text:

```
            if row.get("tree") is not None
```

### `u219.G5_resume_run`

resort_argv: drop --run, so the spawned child meets the explicit gate with nothing recorded

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `G5_resume_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_resume_argv_names_the_gate_run`

Old text:

```
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "route", "resort", "--job", job.job_id]
```

New text:

```
    resume = []
    return [*resume, "route", "resort", "--job", job.job_id]
```

### `u219.M3_due_again_said`

_due_again_warnings: count nothing due, so a resort that left a favourite for later reports a clean success (round two's third hold)

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `M3_due_again_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`

Old text:

```
        count = int(report.get("due_again") or 0)
```

New text:

```
        count = 0
```

### `u219.R1_routed_trees`

_routed_trees: every native tree, so the resort queues the intake tree again

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R1_routed_trees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 12 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_library_that_moved_after_the_gate_refuses_before_writing`
  - `tests/test_resort_scope.py::test_a_resort_after_a_genre_sub_writes_nothing_under_the_intake_root`
  - `tests/test_resort_scope.py::test_a_resort_that_left_a_favourite_for_later_says_so`
  - `tests/test_resort_scope.py::test_a_resort_with_no_change_plans_nothing_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_resort_writes_no_favourite_its_gate_did_not_show`
  - `tests/test_resort_scope.py::test_an_abort_queues_nothing_and_writes_nothing`
  - `tests/test_resort_scope.py::test_an_answer_over_one_database_file_does_not_approve_another`
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`
  - `tests/test_resort_scope.py::test_the_digest_is_the_same_over_one_unchanged_library`
  - `tests/test_resort_scope.py::test_the_favourite_a_resort_left_is_shown_and_filed_by_the_next`
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`
  - `tests/test_resort_scope.py::test_two_files_that_swap_places_after_the_gate_refuse_by_their_paths`

Old text:

```
    return tuple(t for t in _native_trees(entries) if rebuild.derivable(declared, t))
```

New text:

```
    return _native_trees(entries)
```

### `u219.R2_inbox_routed_only`

plan_inbox: file the intake folder into every native tree, INBOX included

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R2_inbox_routed_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_route_inbox_files_into_the_routing_tree_only`

Old text:

```
    native = _routed_trees(entries, declared)
```

New text:

```
    native = _native_trees(entries)
```

### `u219.R3_left_alone_named`

_passed_over: name no tree the resort left alone

- File: `src/cratekit/write/routing_cli.py`
- Source: `u219.json`, row `R3_left_alone_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_organize_mirror_edits.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 309 against a baseline of 309
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_the_gate_shows_every_add_and_only_the_routing_trees`

Old text:

```
    skipped = [t for t in _native_trees(entries) if t in others]
    if not skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
```

New text:

```
    skipped = [t for t in _native_trees(entries) if t in others]
    if skipped:
        return []
    named = ", ".join(f"{others[t]} ({t})" for t in skipped)
    return [
        {
            "code": TREE_NOT_DERIVED,
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

### `u53-routing-and-rebuild-workers.U1_unplaced_constant_empty`

Unplaced reports nothing whatever the library holds, which is the defect verbatim

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U1_unplaced_constant_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 4 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_unplaced_compares_on_an_encrypted_library`
  - `tests/test_routing_workers.py::test_unplaced_does_not_report_a_row_rekordbox_removed`
  - `tests/test_routing_workers.py::test_unplaced_reports_the_rows_no_governed_tree_holds`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U2_compared_true_without_a_tree`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U3_held_never_populated`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-routing-and-rebuild-workers.json`, row `U4_tombstones_reported`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u53-zero-rows-remeasured.json`, row `I1_native_filter_dropped`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86-b.json`, row `E14_non_creating_writer`
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

### `u86-b.E15_nothing_inserted_nothing_written`

Write the output file even when nothing was inserted

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86-b.json`, row `E15_nothing_inserted_nothing_written`
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
    if not report.inserted:
        return None, report
```

New text:

```
(empty)
```

### `u86-b.E16_never_in_place`

Write the output over the export it read

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86-b.json`, row `E16_never_in_place`
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
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_a_track_is_never_removed_from_the_playlist`
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`
  - ... and 17 more, see the JSON sidecar

Old text:

```
    destination = export.with_name(export.stem + ROUTED_SUFFIX)
```

New text:

```
    destination = export
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

### `u86.E10_unreadable_not_routed`

Route a track whose file could not be found, through the fallback

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E10_unreadable_not_routed`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E11_is_file`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E12_prefix_map`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E2_governed_tree`
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

### `u86.E3_mount_guard`

Drop the refusal of a library whose root is not there

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E3_mount_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not Path(cfg.library.root).is_dir():
```

New text:

```
    if False:
```

### `u86.E4_export_absent`

Drop the refusal of an export path that is not a file

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E4_export_absent`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E6_intake_absent`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u86.json`, row `E9_row_absent`
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

### `u87.G1a_empty_not_unrated`

_unrated: an EMPTY Rating no longer reads as unrated, only zero does

- File: `src/cratekit/write/routing_cli.py`
- Source: `u87.json`, row `G1a_empty_not_unrated`
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

### `u87.G1b_any_value_unrated`

_unrated: drop the empty-or-zero test, so a hand set rating reads as unrated

- File: `src/cratekit/write/routing_cli.py`
- Source: `u87.json`, row `G1b_any_value_unrated`
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

### `u87.G1c_absent_attribute_unrated`

_unrated: drop the presence check, so a row with no Rating attribute is planned

- File: `src/cratekit/write/routing_cli.py`
- Source: `u87.json`, row `G1c_absent_attribute_unrated`
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
    return (value or "").strip() in ("", "0")
```

### `u87.G2_rates_flag`

_ratings: drop the rates = false skip

- File: `src/cratekit/write/routing_cli.py`
- Source: `u87.json`, row `G2_rates_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 5 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_declined_run_still_says_which_ratings_are_owed`
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
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
(empty)
```

### `u88.D1_zero_is_a_length`

_duration: a TotalTime of zero reads as a length rather than as unknown

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `D1_zero_is_a_length`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `D2_prefix_digits`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `D3_absent_attribute`
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
  - `tests/test_routing_workers.py::test_a_track_in_a_bucket_that_does_not_rate_is_filed_and_not_owed`
  - `tests/test_routing_workers.py::test_a_track_of_exactly_the_bound_is_not_a_member`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `I1_items_outside_intake`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `I2_item_flag`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `L1_bound_strict`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `L2_bound_coefficient`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `L3_existing_members_replanned`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `L4_folder_warning_dropped`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `L5_folder_refusal_bypassed`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u88.json`, row `T1_unreadable_count`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89-e6.json`, row `E6_vox_warnings`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89.json`, row `E1_export_threshold`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89.json`, row `E2_no_vox_subs`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89.json`, row `E3_subs_uncalibrated`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89.json`, row `E4_undeclared_sub`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u89.json`, row `E5_unreachable_tree`
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

### `u91-b.P1_inbox_decide_rows`

plan_export, existing guard sample: hand an intake key with no collection row to _decide anyway

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91-b.json`, row `P1_inbox_decide_rows`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91-b.json`, row `U6_tree_named`
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

### `u91.U10_unmounted_refusal`

_refuse_off_the_bridge: never refuse an absent library root (shared with route inbox --export)

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U10_unmounted_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not Path(cfg.library.root).is_dir():
        raise refuse(
            "library-volume-unmounted",
```

New text:

```
    if False:
        raise refuse(
            "library-volume-unmounted",
```

### `u91.U12_write_warnings`

route_unplaced_export: drop the writer's skipped writes from the warnings

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U12_write_warnings`
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

### `u91.U17_decide_unreadable`

_decide: route a row whose Location names no file here, by absent tags, instead of warning and skipping it

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U17_decide_unreadable`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U18_unplaced_threshold`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U1_unplaced_rule`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U3_tree_absent_refusal`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U4_tree_type`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U5_creating_writer`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U7_nothing_written`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U8_suffix`
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

- File: `src/cratekit/write/routing_cli.py`
- Source: `u91.json`, row `U9_cut_over_refusal`
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

