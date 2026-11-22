# Mutation table: u325-after-l-01

Measured by `scripts/mutate.py` on 2026-11-22 21:51 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 47.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 19:51 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 3, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 85 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
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
| `u88-b.W1_replace_not_append` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 2 | killed |
| `u88-b.W3_dedupe` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 1 | killed |
| `u223.M10_report_wrong_name` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 2 | killed |
| `u223.M1_keep_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 3 | killed |
| `u223.M21_discard_through_link` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u223.M22_discard_unlinks_directory` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M23_intent_link_followed` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M24_report_link_followed` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M2_keep_linked_intent` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u223.M4_subdir_unlinked` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 2 | killed |
| `u223.M5_discard_keeps_report` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M6_discard_keeps_intent` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 4 | killed |
| `u223.M7_report_any_item` | `src/cratekit/analysis/artifacts.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M8_report_not_mapping` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `u223.M9_report_unparsed` | `src/cratekit/analysis/artifacts.py` | maintainer | 1 file(s) | 172 | 1 | killed |
| `r395.M9_worker_literal` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u192.A3_restamp_wrong_resume` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M11_no_fallback` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u223.M12_renamed_to_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M13_resumed_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M14_any_status` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M15_folder_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M17_claim_failure_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M18_refused_rename_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u223.M19_attempt_start_keeps_evidence` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u223.M20_twin_target_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R2_extra_not_required` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.R4_keyless_finalized` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R5_tag_write_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R7_absent_energy_stamped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.R8_title_without_head` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.R9_missing_file_analysed` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u58-workers-and-wav.S2_unchanged_rewritten` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.S3_queue_without_calibration` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u90-a.A1_lower_bound_strict` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-a.A2_upper_bound_strict` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-a.A3_range_guard_off` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 7 | killed |
| `u90-a.A4_max_coefficient` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-a.A5_min_coefficient` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-a.A6_dispatch_truthiness` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-a.A7_exclusive_group_gone` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-b.B1_library_root_unchecked` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-b.B2_method_not_hand` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u90-b.B3_note_reworded` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 3 | killed |
| `u90-b.B4_date_field_dropped` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-b.B5_previous_cut_not_reported` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-b.B6_hand_detail_drops_old_cut` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 4 | killed |
| `u90-b.B7_fit_detail_drops_old_cut` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 2 | killed |
| `u90-b.B8_hand_reads_old_after_write` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 4 | killed |
| `u90-c.C2_unreadable_refuses` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 1 | killed |
| `u90-c.C3_hand_branch_wrong_method` | `src/cratekit/analysis/cli.py` | user | 1 file(s) | 172 | 4 | killed |
| `u58-workers-and-wav.E1_beatless_cap` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 172 | 1 | killed |
| `u58-workers-and-wav.S4_undo_overwritten` | `src/cratekit/analysis/energy.py` | user | 1 file(s) | 172 | 1 | killed |
| `r221-a.S3_flag_reads_a_key_nothing_freezes` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 7 | killed |
| `r221-a.W1_rehearsal_never_said` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r221-a.W2_rehearsal_said_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |
| `r221-a.W3_queue_branch_warning_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-a.W4_twin_branch_warning_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-a.W6_twin_branch_says_it_unconditionally` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-b.M1_refusal_step_dropped` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `r221-b.M2_refusal_step_unconditional` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 4 | killed |
| `r221-b.M4_steps_replaced_not_joined` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r221-b.R1_refusal_is_its_own_cause` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B10_archive_not_compared` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 1 | killed |
| `r222-b.B11_finished_jobs_are_twins` | `src/cratekit/backup/cli.py` | user | 1 file(s) | 99 | 3 | killed |

## Zero rows and what they owe

- `u86.E3_mount_guard` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `u91.U10_unmounted_refusal` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `u223.M10_report_wrong_name`

staged_report: read the report under a name staged_path never writes

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M10_report_wrong_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / _report_name(item.ordinal)
```

New text:

```
    path = _staging_dir(cfg, job.job_id, item.ordinal) / f"{item.ordinal}.json"
```

### `u223.M1_keep_intent`

staged_path: clear the rename intent with everything else, the shipped behaviour

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M1_keep_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`
  - `tests/test_analysis_workers.py::test_an_attempt_whose_source_is_still_there_drops_a_stale_intent`

Old text:

```
                entry.name == RENAME_INTENT_FILENAME
                and entry.is_file()
```

New text:

```
                entry.name == "never-kept.json"
                and entry.is_file()
```

### `u223.M21_discard_through_link`

discard_rename_evidence: reach through a linked staging directory

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M21_discard_through_link`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_discard_never_reaches_through_a_linked_staging_directory`

Old text:

```
    if directory.is_symlink() or not directory.is_dir():
        # NOT THROUGH A LINK
```

New text:

```
    if not directory.exists():
        # NOT THROUGH A LINK
```

### `u223.M22_discard_unlinks_directory`

discard_rename_evidence: unlink a directory at the report name, failing the item for good

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M22_discard_unlinks_directory`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`

Old text:

```
        if entry.is_symlink() or not entry.is_dir():
            entry.unlink(missing_ok=True)
```

New text:

```
        if True:
            entry.unlink(missing_ok=True)
```

### `u223.M23_intent_link_followed`

rename_intent: read an intent that is a link

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M23_intent_link_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_linked_intent_or_report_is_never_read_as_the_twin`

Old text:

```
    path = intent_path(cfg, job.job_id, item.ordinal)
    if path.is_symlink() or not path.is_file():
```

New text:

```
    path = intent_path(cfg, job.job_id, item.ordinal)
    if not path.is_file():
```

### `u223.M24_report_link_followed`

staged_report: read a report that is a link

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M24_report_link_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u223.M2_keep_linked_intent`

staged_path: keep an intent that is a link, so the clear keeps it and rename_intent follows it

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M2_keep_linked_intent`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u223.M4_subdir_unlinked`

staged_path: unlink a subdirectory entry instead of removing its tree

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M4_subdir_unlinked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_new_attempt_clears_a_stale_report_and_keeps_only_the_intent`

Old text:

```
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry)
```

New text:

```
            if False:
                shutil.rmtree(entry)
```

### `u223.M5_discard_keeps_report`

discard_rename_evidence: drop the intent only, round one's residual

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M5_discard_keeps_report`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (RENAME_INTENT_FILENAME,):
```

### `u223.M6_discard_keeps_intent`

discard_rename_evidence: drop the report only, keeping the intent

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M6_discard_keeps_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_leaves_no_intent_behind`

Old text:

```
    for name in (RENAME_INTENT_FILENAME, _report_name(item.ordinal)):
```

New text:

```
    for name in (_report_name(item.ordinal),):
```

### `u223.M7_report_any_item`

staged_report: accept a report for another item

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M7_report_any_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_is_a_twin_only_for_this_item_renamed_in_its_own_folder`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    if not isinstance(loaded, dict):
        return None
    return loaded
```

### `u223.M8_report_not_mapping`

staged_report: drop the mapping check, so a list report raises

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M8_report_not_mapping`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_staged_report_that_is_not_json_or_not_a_mapping_is_no_twin`

Old text:

```
    if not isinstance(loaded, dict) or loaded.get("item") != item.item_id:
        return None
    return loaded
```

New text:

```
    if loaded.get("item") != item.item_id:
        return None
    return loaded
```

### `u223.M9_report_unparsed`

staged_report: let a report that is not JSON raise

- File: `src/cratekit/analysis/artifacts.py`
- Source: `u223.json`, row `M9_report_unparsed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `r395.M9_worker_literal`

Put the old bare pip literal back in the analysis worker refusal

- File: `src/cratekit/analysis/cli.py`
- Source: `r395.json`, row `M9_worker_literal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u192.A3_restamp_wrong_resume`

analyze_restamp: name the analyze run command as the one that resumes an interrupted restamp

- File: `src/cratekit/analysis/cli.py`
- Source: `u192.json`, row `A3_restamp_wrong_resume`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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

### `u58-workers-and-wav.R2_extra_not_required`

Drop the missing extra refusal in the run worker

- File: `src/cratekit/analysis/cli.py`
- Source: `u58-workers-and-wav.json`, row `R2_extra_not_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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
- Collected: 172 against a baseline of 172
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

### `u90-a.A1_lower_bound_strict`

The range guard's lower bound made strict, so a cut of 0 is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A1_lower_bound_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if not VOCAL_SCORE_MIN < cut <= VOCAL_SCORE_MAX:
```

### `u90-a.A2_upper_bound_strict`

The range guard's upper bound made strict, so a cut of 100 is refused

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A2_upper_bound_strict`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if not VOCAL_SCORE_MIN <= cut < VOCAL_SCORE_MAX:
```

### `u90-a.A3_range_guard_off`

The whole range guard switched off, so any float is written as the cut

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A3_range_guard_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 7 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[inf]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[nan]`
  - `tests/test_analysis_workers.py::test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte`

Old text:

```
    if not VOCAL_SCORE_MIN <= cut <= VOCAL_SCORE_MAX:
```

New text:

```
    if False:
```

### `u90-a.A4_max_coefficient`

The score range's top moved from 100 to 1000

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A4_max_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[100.5]`
  - `tests/test_analysis_workers.py::test_a_refused_cut_leaves_the_cut_on_record_byte_for_byte`

Old text:

```
VOCAL_SCORE_MAX = 100.0
```

New text:

```
VOCAL_SCORE_MAX = 1000.0
```

### `u90-a.A5_min_coefficient`

The score range's bottom moved from 0 to minus 1

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A5_min_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-0.5]`
  - `tests/test_analysis_workers.py::test_a_cut_outside_the_score_range_refuses_and_writes_nothing[-1]`

Old text:

```
VOCAL_SCORE_MIN = 0.0
```

New text:

```
VOCAL_SCORE_MIN = -1.0
```

### `u90-a.A6_dispatch_truthiness`

The hand path dispatched on truthiness, so a cut of 0 falls through to the fit

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A6_dispatch_truthiness`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u90-a.A7_exclusive_group_gone`

The folder and the flag no longer mutually exclusive in the parser

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-a.json`, row `A7_exclusive_group_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u90-b.B1_library_root_unchecked`

The hand path stops requiring the library root before it writes

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B1_library_root_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u90-b.B2_method_not_hand`

A hand cut recorded under the fit's method, otsu

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B2_method_not_hand`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`

Old text:

```
method=VOCAL_METHOD_HAND, note=
```

New text:

```
method="otsu", note=
```

### `u90-b.B3_note_reworded`

The hand cut's note stops saying set by hand

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B3_note_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 3 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`

Old text:

```
note=f"set by hand on {today}"
```

New text:

```
note=f"entered on {today}"
```

### `u90-b.B4_date_field_dropped`

The hand cut's set_on date field no longer written

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B4_date_field_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`

Old text:

```
note=f"set by hand on {today}", set_on=today
```

New text:

```
note=f"set by hand on {today}"
```

### `u90-b.B5_previous_cut_not_reported`

The summary reports no previous cut whatever was on record

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B5_previous_cut_not_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
"previous_vocal_cut": previous}
```

New text:

```
"previous_vocal_cut": None}
```

### `u90-b.B6_hand_detail_drops_old_cut`

The hand path's check detail stops naming the cut it replaced

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B6_hand_detail_drops_old_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
f"cut set by hand at {cut:g}, written to {target}; {before}; "
```

New text:

```
f"cut set by hand at {cut:g}, written to {target}; "
```

### `u90-b.B7_fit_detail_drops_old_cut`

The fit's check detail stops naming the cut it replaced

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B7_fit_detail_drops_old_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`

Old text:

```
        f"written to {target}; {before}",
```

New text:

```
        f"written to {target}",
```

### `u90-b.B8_hand_reads_old_after_write`

The hand path reads the previous cut after its own write, so it reports itself

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-b.json`, row `B8_hand_reads_old_after_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u90-c.C2_unreadable_refuses`

An unreadable calibration refuses the hand cut instead of being replaced by it

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-c.json`, row `C2_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u90-c.C3_hand_branch_wrong_method`

The replaced cut is named as set by hand only when its method is otsu

- File: `src/cratekit/analysis/cli.py`
- Source: `u90-c.json`, row `C3_hand_branch_wrong_method`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_after_a_hand_cut_replaces_it_and_says_so`
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    if record.get("method") == VOCAL_METHOD_HAND:
```

New text:

```
    if record.get("method") == "otsu":
```

### `u58-workers-and-wav.E1_beatless_cap`

Drop the beatless cap in the energy scorer

- File: `src/cratekit/analysis/energy.py`
- Source: `u58-workers-and-wav.json`, row `E1_beatless_cap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
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

### `u58-workers-and-wav.S4_undo_overwritten`

Let a second restamp overwrite the first previous value

- File: `src/cratekit/analysis/energy.py`
- Source: `u58-workers-and-wav.json`, row `S4_undo_overwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`
- Collected: 172 against a baseline of 172
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_the_undo_log_keeps_the_first_previous_value_across_a_second_restamp`

Old text:

```
        if key in log:
            return False

```

New text:

```
(empty)
```

### `r221-a.S3_flag_reads_a_key_nothing_freezes`

Read the rehearsal flag under a name the build does not freeze, so every job reads as a real backup

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `S3_flag_reads_a_key_nothing_freezes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_rehearsal_says_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return bool((job.payload or {}).get(DRY_RUN))
```

New text:

```
    return bool((job.payload or {}).get("rehearsal"))
```

### `r221-a.W1_rehearsal_never_said`

The warning is never carried, which is the exact state the ledger entry describes

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W1_rehearsal_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return ()
```

### `r221-a.W2_rehearsal_said_unconditionally`

Every run is told it copied nothing, including the real one that copied and published, which is the same defect pointing the other way

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W2_rehearsal_said_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_real_backup_carries_no_rehearsal_word`
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`
  - `tests/test_backup_cli.py::test_the_flag_on_the_envelope_is_the_jobs_own_and_not_the_command_lines`

Old text:

```
    return (rehearsal_warning(),) if _is_rehearsal(job) else ()
```

New text:

```
    return (rehearsal_warning(),)
```

### `r221-a.W3_queue_branch_warning_dropped`

The identifier is handed back with no word about what it will do, and the detached child a resume spawns writes to a log nobody is watching

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W3_queue_branch_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
                *map(dict, backup.snapshot_identity_warning(cfg)),
                *_rehearsal(job),
            ),
        )
```

New text:

```
                *map(dict, backup.snapshot_identity_warning(cfg)),
            ),
        )
```

### `r221-a.W4_twin_branch_warning_dropped`

A second ask reports the open rehearsal as the backup the person asked for, with nothing saying it is one

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W4_twin_branch_warning_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_rehearsal_is_said_at_queue_time_and_when_the_open_job_is_reported`

Old text:

```
                    *_rehearsal(twin),
                ),
            )
```

New text:

```
                ),
            )
```

### `r221-a.W6_twin_branch_says_it_unconditionally`

The reported twin always carries the word, so a person asking twice for a REAL backup is told the open job copies nothing. Removing the helper's own guard is W2; this is the branch's own reading of the job it hands back

- File: `src/cratekit/backup/cli.py`
- Source: `r221-a.json`, row `W6_twin_branch_says_it_unconditionally`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_second_ask_for_a_real_backup_is_not_told_the_open_job_copies_nothing`

Old text:

```
                    *_rehearsal(twin),
```

New text:

```
                    rehearsal_warning(),
```

### `r221-b.M1_refusal_step_dropped`

No refusal carries the sentence, so a rehearsal that failed reads as a real backup attempt that fell over

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M1_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
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

### `r221-b.M2_refusal_step_unconditional`

Every refusal gains the sentence, so a person whose REAL backup failed is told nothing was copied and stops looking for the half that was

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M2_refusal_step_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_real_backup_that_ended_badly_gains_no_rehearsal_step`
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`
  - `tests/test_backup_cli.py::test_an_unreadable_fact_file_under_a_real_run_gains_no_rehearsal_step`

Old text:

```
    if not _is_rehearsal(job):
        return error
    cause = error.cause
```

New text:

```
    cause = error.cause
```

### `r221-b.M4_steps_replaced_not_joined`

The sentence replaces the failure's own steps rather than joining them, so the thing a person has to do to fix it is gone

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `M4_steps_replaced_not_joined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_rehearsal_that_ended_badly_still_says_it_was_a_rehearsal`

Old text:

```
                steps=(*cause.remediation.steps, rehearsal_warning()["message"]),
```

New text:

```
                steps=(rehearsal_warning()["message"],),
```

### `r221-b.R1_refusal_is_its_own_cause`

Raise the result from the original unconditionally, which is `raise exc from exc` on a real run and truncates the chain cause.classified walks. This is the defect the code review found

- File: `src/cratekit/backup/cli.py`
- Source: `r221-b.json`, row `R1_refusal_is_its_own_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_refusal_this_verb_re_raises_is_never_its_own_cause`

Old text:

```
    extended = _with_rehearsal_step(error, job)
    if extended is error:
        raise error
    raise extended from error
```

New text:

```
    raise _with_rehearsal_step(error, job) from error
```

### `r222-b.B10_archive_not_compared`

Compare only the mirror, so two jobs rotating one archive root from different mirrors are strangers

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B10_archive_not_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_either_shared_destination_is_the_same_backup[archive_root]`

Old text:

```
            frozen.backup.dest == cfg.backup.dest
            or frozen.backup.archive_root == cfg.backup.archive_root
```

New text:

```
            frozen.backup.dest == cfg.backup.dest
```

### `r222-b.B11_finished_jobs_are_twins`

Read every state from the queue, so a backup that is over stands in for a new one for ever

- File: `src/cratekit/backup/cli.py`
- Source: `r222-b.json`, row `B11_finished_jobs_are_twins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_cli.py`
- Collected: 99 against a baseline of 99
- Kills: 3 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`

Old text:

```
    for job in jobs.list_jobs(store, states=open_states):
```

New text:

```
    for job in jobs.list_jobs(store):
```

