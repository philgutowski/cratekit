# Mutation table: u325-before-01

Measured by `scripts/mutate.py` on 2026-11-22 18:30 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 15.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 16:21 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 3, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 117 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u138-rerun.S5_bound_exclusive` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 1 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 4 | killed |
| `u138.S10_older_record_reads_as_session` | `src/cratekit/core/session.py` | maintainer | 43 file(s) | 4218 | 1 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 13 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 10 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session.py` | user | 43 file(s) | 4218 | 4 | killed |
| `u132.W5_rebuild_note` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.I3_rebuild_items_dropped` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 21 | killed |
| `u53-routing-and-rebuild-workers.R2_rebuild_drives_a_foreign_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-routing-and-rebuild-workers.R4_rebuild_drives_an_itemless_job` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I6_tree_items_ignores_native` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u53-zero-rows-remeasured.I7_tree_items_ignores_the_named_tree` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 1 | killed |
| `u89.W4_rebuild_worker` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 4 | killed |
| `u89.W6_rebuild_resume_loads_first` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 197 | 3 | killed |
| `r316.M3_inbox_gaps_leak_into_totals` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 197 | 1 | killed |
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
| `u86.E3_mount_guard` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
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
| `u91.U10_unmounted_refusal` | `src/cratekit/write/routing_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
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
| `u88-b.W1_replace_not_append` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 2 | killed |
| `u88-b.W3_dedupe` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 1 | killed |
| `r1394.A1_recorder_never_told` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 5 | killed |
| `r1394.A2_sent_one_short` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 5 | killed |
| `r1394.A3_landed_overstated` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 4 | killed |
| `r1394.A4_412_not_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `r1394.A5_any_failure_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 3 | killed |
| `r1411.A1_agreed_order_always_stands` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 11 | killed |
| `r1411.A2_removed_tracks_asked_of_the_reading` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 3 | killed |
| `r1411.A3_added_tracks_asked_of_the_agreed_order` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 7 | killed |
| `r1411.A5_duplicates_counted_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 1 | killed |
| `r1411.E1_expect_compared_as_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 1 | killed |
| `r1411.E4_membership_always_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `r1411.S1_settled_ignores_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `r1411.S2_agreed_stands_in_for_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 1 | killed |
| `r1411.S3_order_does_not_pass_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `u231.M4_resend_with_the_stale_tag` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 6 | killed |

## Zero rows and what they owe

- `u86.E3_mount_guard` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u91.U10_unmounted_refusal` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u138-rerun.S5_bound_exclusive`

A portion exactly five days old is under the bound

- File: `src/cratekit/core/session.py`
- Source: `u138-rerun.json`, row `S5_bound_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`

Old text:

```
        elif entry.age_seconds >= limit:

```

New text:

```
        elif entry.age_seconds > limit:

```

### `u138.E1_terminal_check`

Existing guard sample: the terminal check on a person's answer

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `E1_terminal_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_write_session.py::test_an_agent_shaped_invocation_cannot_mint_the_acknowledgment`
  - `tests/test_write_session.py::test_the_terminal_probe_the_mint_uses_by_default_is_the_real_one`

Old text:

```
        if not probe():

```

New text:

```
        if False:

```

### `u138.S10_older_record_reads_as_session`

A record from before U138 reads as minted by the session's rule

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S10_older_record_reads_as_session`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_record_written_before_u138_reads_as_the_terminal_rule`

Old text:

```
            rule=str(data.get("rule") or RULE_TERMINAL),

```

New text:

```
            rule=str(data.get("rule") or RULE_SESSION_AGES),

```

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 4 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
            "rule": self.rule,

```

New text:

```
(empty)
```

### `u138.S12_message_names_the_portion`

Reword the refusal so it no longer names the portion's age

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S12_message_names_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
                f"the {entry.portion} portion is {entry.age_seconds / 86400:.1f} days old"

```

New text:

```
                f"a backup portion is too old ({entry.portion})"

```

### `u138.S13_remedy_points_back_at_ack`

The too old refusal tells a person to acknowledge again rather than to run a backup

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S13_remedy_points_back_at_ack`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 8 (killed)
- Killed:
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
                remedy=Remedy.RUN_BACKUP,

```

New text:

```
                remedy=Remedy.ACKNOWLEDGE_BACKUP,

```

### `u138.S1_session_rule_gone`

A session's answer falls to the terminal check, as before U138

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 20 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_names_when_an_acknowledgment_lapsed`
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_doctor.py::test_no_acknowledgment_is_claimed_absent_off_a_volume_nobody_read`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if False:

```

### `u138.S2_any_answer_gets_the_age_rule`

Any recorded answer, a person's included, mints without a terminal on young backups

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`
  - `tests/test_session_cli.py::test_the_answering_invocation_refuses_when_nobody_is_there`
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`
  - `tests/test_session_cli.py::test_the_cli_mints_an_acknowledgment_a_real_destructive_verb_then_spends`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    if decided_by == SESSION_ACTOR:

```

New text:

```
    if decided_by is not None:

```

### `u138.S3_stale_not_refused`

The session mints over a portion five days old or of unknown age

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`

Old text:

```
        if stale:

```

New text:

```
        if False:

```

### `u138.S6_bound_six_days`

The bound is six days rather than five

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_five_days_as_the_author_set_it`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[exactly-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`

Old text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=5)

```

New text:

```
SESSION_MAX_BACKUP_AGE = timedelta(days=6)

```

### `u138.S8_rule_not_recorded`

The record always says the terminal rule minted it

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 6 (killed)
- Killed:
  - `tests/test_doctor.py::test_doctor_shows_the_acknowledgments_expiry_beside_the_two_backup_ages`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        shown=shown,
        rule=rule,

```

New text:

```
        shown=shown,
        rule=RULE_TERMINAL,

```

### `u138.S9_answer_not_recorded`

The record never says who answered the gate

- File: `src/cratekit/core/session.py`
- Source: `u138.json`, row `S9_answer_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4218 against a baseline of 4218
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_the_bound_is_strict_at_exactly_five_days[a-second-under-five-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        rule=rule,
        decided_by=decided_by,

```

New text:

```
        rule=rule,
        decided_by=None,

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
  - `tests/test_routing_workers.py::test_a_driven_rebuild_watches_the_grids_where_they_actually_live`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_whose_root_the_database_lacks_fails_the_item`
  - `tests/test_routing_workers.py::test_a_driven_rebuild_without_an_acknowledgment_refuses_through_the_real_gates`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_no_favorites_class_names_the_skipped_step[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_over_the_declared_class_says_nothing_of_it[rebuild]`
  - `tests/test_routing_workers.py::test_a_driven_resume_says_the_vocal_dimension_was_not_compared_beside_drift[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_and_resort_run_on_an_encrypted_library[rebuild]`
  - `tests/test_routing_workers.py::test_a_queued_rebuild_runs_its_item_and_the_tree_holds_the_track`
  - `tests/test_routing_workers.py::test_a_rebuild_of_another_tree_says_nothing_of_the_routing_trees_favorites[rebuild]`
  - `tests/test_routing_workers.py::test_a_rebuild_of_one_named_tree_queues_that_tree_alone`
  - `tests/test_routing_workers.py::test_a_resume_reads_no_registry_of_its_own`
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
- Collected: 22663 against a baseline of 22663
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
- Collected: 22663 against a baseline of 22663
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

### `u88-b.W3_dedupe`

add_to_root_playlist: drop the dedupe, so a repeated id or an existing member is added again

- File: `src/cratekit/write/trees.py`
- Source: `u88-b.json`, row `W3_dedupe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_the_add_only_writer_counts_each_new_track_once`

Old text:

```
        if key not in held:
```

New text:

```
        if True:
```

### `r1394.A1_recorder_never_told`

adapter order: the recorder begun answers is never told before a move, so the record keeps sent and landed at 0 while moves land

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A1_recorder_never_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                if told is not None:
                    told(number, number - 1)
```

New text:

```
                if False:
                    told(number, number - 1)
```

### `r1394.A2_sent_one_short`

adapter order: the recorder is told one move fewer sent than is about to go, so a move in flight is read as known not to have landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A2_sent_one_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number - 1, number - 1)
```

### `r1394.A3_landed_overstated`

adapter order: the recorder is told the move about to go has already landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A3_landed_overstated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number, number)
```

### `r1394.A4_412_not_brought_down`

adapter order: a move spent on its 412s is left as maybe landed, its sent count never brought back down

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A4_412_not_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                        told(number - 1, number - 1)
```

New text:

```
                        pass
```

### `r1394.A5_any_failure_brought_down`

adapter order: a move that failed any way, a dropped connection included, is told as not landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A5_any_failure_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

New text:

```
                    if told is not None:
                        told(number - 1, number - 1)
                    if not _stale_tag(exc):
                        raise
                    if told is not None:
```

### `r1411.A1_agreed_order_always_stands`

the agreed order check passes every reading, so a reading in the order from before the stopped moves is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A1_agreed_order_always_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading1-agreed1-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading5-agreed5-False]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading7-agreed7-False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
    ]
```

New text:

```
    return bool(named or held or True)
```

### `r1411.A2_removed_tracks_asked_of_the_reading`

the agreed order check asks every agreed track of the reading, so a track this write took off refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A2_removed_tracks_asked_of_the_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading6-agreed6-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading9-agreed9-True]`

Old text:

```
        one for one in dict.fromkeys(str(one) for one in agreed) if one in held
```

New text:

```
        one for one in dict.fromkeys(str(one) for one in agreed)
```

### `r1411.A3_added_tracks_asked_of_the_agreed_order`

the agreed order check reads every track of the reading, so a track this write added refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A3_added_tracks_asked_of_the_agreed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading10-agreed10-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading2-agreed2-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading3-agreed3-True]`
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading4-agreed4-True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in dict.fromkeys(reading)] == [
```

### `r1411.A5_duplicates_counted_twice`

the agreed order check reads a track the reading holds twice at both places

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A5_duplicates_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_is_read_over_the_tracks_both_hold[reading8-agreed8-True]`

Old text:

```
    return [one for one in dict.fromkeys(reading) if one in named] == [
```

New text:

```
    return [one for one in reading if one in named] == [
```

### `r1411.E1_expect_compared_as_membership`

existing guard, U220: an expected reading is compared by the tracks it holds, not their order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E1_expect_compared_as_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`

Old text:

```
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
```

New text:

```
                return sorted(dict.fromkeys(reading)) == sorted(dict.fromkeys(known))
```

### `r1411.E4_membership_always_agrees`

existing guard, U220: a reading after this command's own writes is taken whatever it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E4_membership_always_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return bool(reading) or True
```

### `r1411.S1_settled_ignores_agreed`

the judged reading never asks the agreed order, so only what it holds is checked

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S1_settled_ignores_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`

Old text:

```
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if False:
                return False
```

### `r1411.S2_agreed_stands_in_for_membership`

a reading in the agreed order is taken without the check of what it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S2_agreed_stands_in_for_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if agreed is not None:
                return _in_agreed_order(reading, agreed)
```

### `r1411.S3_order_does_not_pass_agreed`

order_tracks takes agreed and never hands it to the judged reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S3_order_does_not_pass_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_after_an_add_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`

Old text:

```
            agreed=tuple(str(one) for one in agreed) if agreed is not None else None,
```

New text:

```
            agreed=None,
```

### `u231.M4_resend_with_the_stale_tag`

adapter order: a 412's move is sent again without opening the playlist for its current tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M4_resend_with_the_stale_tag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_window_lag.py::test_the_pause_after_a_412_is_counted_in_the_moves_record`

Old text:

```
                    playlist = self._playlist(identifier)
                    continue
```

New text:

```
                    continue
```

