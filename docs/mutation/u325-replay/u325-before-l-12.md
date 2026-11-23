# Mutation table: u325-before-l-12

Measured by `scripts/mutate.py` on 2026-11-22 22:15 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 133.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:13 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 13, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u219.M3_due_again_said` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.R1_routed_trees` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 12 | killed |
| `u219.R2_inbox_routed_only` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `u219.R3_left_alone_named` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 309 | 1 | killed |
| `r239-b.S11_readback_key_on` | `src/cratekit/core/session.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S6_delete_key_off` | `src/cratekit/deletion/cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S7_metadata_key_off` | `src/cratekit/write/metadata_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S2_unplaced_key_off` | `src/cratekit/write/routing_cli.py` | user | 7 file(s) | 733 | 2 | killed |
| `r239-b.S8_naming_key_off` | `src/cratekit/write/naming_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `u178.G6_fallback_refusal` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G7_fallback_confirm_ignored` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G8_clear_word_case` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G9_accept_without_genre` | `src/cratekit/label/cli.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G1_genre_length_bound` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G2_genre_needs_a_letter` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G3_genre_one_line` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G4_edit_clear_genre` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u178.G5_edit_none_keeps_genre` | `src/cratekit/label/registry.py` | user | 3 file(s) | 284 | 1 | killed |
| `u52-item-derivation.H2_listing_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.H4_verification_boundary_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H6_empty_playlist_reports_ok` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.H7_unresolved_drops_nameless` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-item-derivation.I5_import_queues_no_item` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 4 | killed |
| `u52-item-derivation.I6_import_item_keyed_on_name` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 2 | killed |
| `u52-item-derivation.R1_itemless_job_drives` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 3 | killed |
| `u52-item-derivation.S1_errors_branch_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `u52-zero-rows.H5_verifier_passthrough_gone` | `src/cratekit/label/cli.py` | user | 2 file(s) | 262 | 1 | killed |
| `r838-c.R1_library_bound` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.R2_remark_clears` | `src/cratekit/sync/mark_record.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `r838-d.R3b_stamp_target` | `src/cratekit/sync/mark_record.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U1_refuse_stranger` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U3_pass_filter` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 2 | killed |
| `r838-a.U4_already_unmarked_stamp` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U5_marked_again` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U6_later_order` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-a.U8_title_already_back` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U10_digest_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U13_recheck` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U15_rename_target` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 8 | killed |
| `r838-b.U16_part_way_names` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-b.U9_renamed_since` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r838-c.U7b_not_listed_rerun` | `src/cratekit/sync/unmark_cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `r1394.S10_later_unsent_write_hides_the_pending` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 3 | killed |
| `r1394.S1_counts_beyond_the_moves_trusted` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r1394.S2_missing_counts_read_as_none_sent` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 7 | killed |
| `r1394.S3_bool_count_read` | `src/cratekit/sync/pair_stopped.py` | maintainer | 2 file(s) | 177 | 1 | killed |
| `r1394.S4_negative_count_read` | `src/cratekit/sync/pair_stopped.py` | maintainer | 2 file(s) | 177 | 1 | killed |
| `r1394.S5_sent_read_as_landed` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 6 | killed |
| `r1394.S6_counts_not_wired` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 14 | killed |
| `r1394.S8_positions_first_only` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 2 | killed |
| `r1394.S9_moving_step_counts_dropped` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 19 | killed |
| `u234.O15_reordered_counts_additions` | `src/cratekit/sync/pair_stopped.py` | user | 2 file(s) | 177 | 1 | killed |
| `r235-a.M11_session_lock_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M12_second_record_replaces` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M13_snapshot_check_dropped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 11 | killed |
| `r235-a.M1_unreadable_log_skipped` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M2_margin_zero` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M3_margin_two_days` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M4_unparseable_start_predates` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M5_updates_not_counted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M6_any_tree_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M7_zero_count_counts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 2 | killed |
| `r235-a.M8_open_run_reverts` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `r235-a.M9_library_guard_removed` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 4 | killed |
| `r235-b.M14_empty_export_accepted` | `src/cratekit/core/tree_registry.py` | user | 2 file(s) | 66 | 1 | killed |
| `u79-a.A1_ambiguous_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-a.A2_full_page_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-a.A3_unreadable_ignored` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-a.A4_no_identifier_listed` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-a.A5_two_exact_picked` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 4 | killed |
| `u79-b.B1_floor_halved` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B2_score_before_exact` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B3_no_identifier_offered` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-b.B4_rejected_read_as_accepted` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B5_unspecific_yes_takes_first` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B6_option_track_mismatch` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `u79-b.B7_identity_without_version` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 2 | killed |
| `u79-b.B8_open_item_searched_again` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 56 | 1 | killed |
| `r757-c1.S4_rehearsal_says_it_sent` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 22663 | 0 (promoted) | zero |
| `r757-c2.S5_unread_number_printed_as_zero` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-c2.S6_twin_in_the_other_mode_says_nothing` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 758 | 1 | killed |
| `r757-c2.S7_verb_says_nothing_of_the_comparison` | `src/cratekit/backup/cli.py` | user | 4 file(s) | 22663 | 0 (promoted) | zero |
| `u149.T2_two_folders_not_refused` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T3_folder_names_unread` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 2 | killed |
| `u149.T4_removed_folder_live` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u149.T5_held_name_counted_free` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 3 | killed |
| `u149.T6_taken_name_free` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M14_backfill_reason_check` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M15_backfill_left_action` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 4 | killed |
| `u213.M16_backfill_digest_reason` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M17_backfill_unread_tracks` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 2 | killed |
| `u213.M18_backfill_unread_reasons` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M19_matched_ambiguous_first` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M20_backfill_whole` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `u213.M2_backfill_refused_reason` | `src/cratekit/sync/twins.py` | user | 2 file(s) | 52 | 1 | killed |
| `r815-b.J1_one_refusal_ends_the_asking` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J2_an_unread_catalogue_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J3_a_failing_provider_ends_the_run` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-b.J4_a_record_never_holds_on_its_own` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J11_the_scope_reads_the_registry` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J12_a_release_held_and_gone_is_counted_held` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `r815-c.J13_the_refusal_carries_the_counts` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 7 | killed |
| `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 4 | killed |
| `r815-c.J6_a_decided_item_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 2 | killed |
| `r815-c.J7_a_returned_release_is_not_judged` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 1 | killed |
| `r815-c.J8_a_refusal_parks_and_fails_no_item` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 5 | killed |
| `r815-c.J9_a_park_drops_the_jobs_tools` | `src/cratekit/label/judge_cli.py` | user | 1 file(s) | 76 | 3 | killed |
| `u103-a.A10_write_is_a_merge` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A1_read_serves_only_answers` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A2_write_keeps_only_answers` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A3_document_must_carry_its_plan` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A5_offset_must_be_planned` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 1 | killed |
| `u103-a.A6_digest_in_the_key` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 5 | killed |
| `u103-a.A7_offsets_in_the_key` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 2 | killed |
| `u103-a.A9_refresh_reads_nothing_kept` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 260 | 2 | killed |
| `u146-a.B12_landing_takes_keyless_rows` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.B13_first_of_two_rows` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |

## Zero rows and what they owe

- `r757-c1.S4_rehearsal_says_it_sent` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r757-c2.S7_verb_says_nothing_of_the_comparison` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `r239-b.S11_readback_key_on`

the session read-back pins the old True default, which a plain database cannot open under

- File: `src/cratekit/core/session.py`
- Source: `r239-b.json`, row `S11_readback_key_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg))
```

New text:

```
    open_fresh = reopen or (lambda: rb_writer.open_db(cfg=cfg, unlock=True))
```

### `r239-b.S6_delete_key_off`

delete review's open passes unlock=False

- File: `src/cratekit/deletion/cli.py`
- Source: `r239-b.json`, row `S6_delete_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg)
```

New text:

```
    return rb_writer.open_db(rb_writer.live_db_path(cfg), cfg=cfg, unlock=False)
```

### `r239-b.S7_metadata_key_off`

mytags' open passes unlock=False

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r239-b.json`, row `S7_metadata_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
        require_closed=writing,
        cfg=cfg,

```

New text:

```
        require_closed=writing,
        unlock=False,
        cfg=cfg,

```

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

### `r239-b.S8_naming_key_off`

the naming verb's collection read passes unlock=False

- File: `src/cratekit/write/naming_cli.py`
- Source: `r239-b.json`, row `S8_naming_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
            require_closed=False,
            cfg=cfg,

```

New text:

```
            require_closed=False,
            unlock=False,
            cfg=cfg,

```

### `u178.G6_fallback_refusal`

_declared_genre: never refuse a fallback genre, so Polka is stored unconfirmed

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G6_fallback_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_routing_only_to_the_fallback_is_refused_and_nothing_is_written`

Old text:

```
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
```

New text:

```
    if False:
```

### `u178.G7_fallback_confirm_ignored`

_declared_genre: refuse a fallback genre even with --accept-fallback

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G7_fallback_confirm_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_fallback_genre_is_kept_when_confirmed_and_the_screen_says_it`

Old text:

```
    if resolution.match is routing.Match.FALLBACK and not accept_fallback:
```

New text:

```
    if resolution.match is routing.Match.FALLBACK:
```

### `u178.G8_clear_word_case`

_declared_genre: match the clearing word in its exact case, so --genre Default is stored as a genre

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G8_clear_word_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
    if wanted.casefold() == CLEAR_GENRE:
```

New text:

```
    if wanted == CLEAR_GENRE:
```

### `u178.G9_accept_without_genre`

registry_cmd: accept --accept-fallback with no --genre, so it confirms nothing silently

- File: `src/cratekit/label/cli.py`
- Source: `u178.json`, row `G9_accept_without_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_accept_fallback_with_no_genre_is_refused`

Old text:

```
    if accept_fallback and genre is None:
```

New text:

```
    if False:
```

### `u178.G1_genre_length_bound`

check_genre: the bound read one past GENRE_MAX, so a 65 character genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G1_genre_length_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]`

Old text:

```
        or len(text) > GENRE_MAX

```

New text:

```
        or len(text) > GENRE_MAX + 1

```

### `u178.G2_genre_needs_a_letter`

check_genre: drop the letter or digit rule, so a punctuation only genre is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G2_genre_needs_a_letter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[---]`

Old text:

```
        or not any(char.isalnum() for char in text)

```

New text:

```
(empty)
```

### `u178.G3_genre_one_line`

check_genre: drop the control character rule, so a genre with a newline is stored

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G3_genre_one_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_genre_that_could_never_be_one_refuses_at_the_store[Romi\nnimal]`

Old text:

```
        or any(unicodedata.category(char).startswith("C") for char in text)

```

New text:

```
(empty)
```

### `u178.G4_edit_clear_genre`

edit: ignore clear_genre, so --genre default on set keeps the genre

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G4_edit_clear_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
                genre=None if clear_genre else (genre if genre is not None else existing.genre),
```

New text:

```
                genre=genre if genre is not None else existing.genre,
```

### `u178.G5_edit_none_keeps_genre`

edit: a genre of None drops the held genre, so an unrelated edit clears it

- File: `src/cratekit/label/registry.py`
- Source: `u178.json`, row `G5_edit_none_keeps_genre`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_label_genre_gate.py`, `tests/test_label_workers.py`
- Collected: 284 against a baseline of 284
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_the_word_default_clears_a_genre_and_none_keeps_it`

Old text:

```
                genre=None if clear_genre else (genre if genre is not None else existing.genre),
```

New text:

```
                genre=None if clear_genre else genre,
```

### `u52-item-derivation.H2_listing_passthrough_gone`

REMOVE THE LAYER ALONE: an adapter's own CratekitError refusal is rewritten as an unreadable playlist

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H2_listing_passthrough_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_cratekit_refusal_from_below_is_not_flattened_into_an_unreadable_playlist`

Old text:

```
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
```

New text:

```
    except Exception as exc:
        raise refuse(
            "label-playlist-unreadable",
            f"the playlist {reference!r} could not be listed by the provider "
```

### `u52-item-derivation.H4_verification_boundary_gone`

THE THIRD PROVIDER CALL: hand from_tracks the bare seam method, so a provider that went away mid playlist becomes internal-error with report-defect

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H4_verification_boundary_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_harvest_that_fails_mid_verification_names_what_it_already_offered`
  - `tests/test_label_workers.py::test_a_provider_that_fails_mid_verification_refuses_rather_than_reporting_a_defect`

Old text:

```
            verify=_label_verifier(found, reference),
```

New text:

```
            verify=found.check_label,
```

### `u52-item-derivation.H6_empty_playlist_reports_ok`

An empty playlist reports OK rather than NO_OP, so nothing found is indistinguishable from something found

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H6_empty_playlist_reports_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_empty_harvest_still_names_that_nothing_was_offered`
  - `tests/test_label_workers.py::test_an_empty_playlist_offers_nothing_and_reports_zero_rather_than_refusing`

Old text:

```
        outcome=Outcome.OK if report.offered else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u52-item-derivation.H7_unresolved_drops_nameless`

Count only the names a catalogue refused, so a playlist whose tracks carry no copyright string at all reports a clean zero unresolved

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `H7_unresolved_drops_nameless`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_track_with_no_copyright_string_is_counted_rather_than_dropped_silently`

Old text:

```
    unresolved = len(report.dropped) + nameless
```

New text:

```
    unresolved = len(report.dropped)
```

### `u52-item-derivation.I5_import_queues_no_item`

THE ZERO ITEM RULE at the import end: queue the single label job with no items at all

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `I5_import_queues_no_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`
  - `tests/test_label_workers.py::test_the_import_queues_without_a_warning_now_an_adapter_is_bound`
  - `tests/test_label_workers.py::test_the_unbound_warning_says_the_job_will_fail_at_the_provider_seam`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(),
```

### `u52-item-derivation.I6_import_item_keyed_on_name`

The import's single item names the label by display name, which the worker then cannot resolve by id

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `I6_import_item_keyed_on_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_import_queues_exactly_one_item_and_it_is_the_label_id`
  - `tests/test_label_workers.py::test_an_import_runs_its_one_item_to_done_through_the_same_worker`

Old text:

```
        item_ids=(entry.label_id,),
```

New text:

```
        item_ids=(entry.name,),
```

### `u52-item-derivation.R1_itemless_job_drives`

Drive a label job with no items, which jobs.drive transitions straight to SUCCEEDED over a registry nothing was read from

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `R1_itemless_job_drives`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_job_carrying_no_items_refuses_on_resume_and_is_left_open`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_label_workers.py::test_the_itemless_refusal_of_an_import_still_says_queue_it_again`

Old text:

```
            _refuse_an_itemless_job(store, job)
```

New text:

```
            pass
```

### `u52-item-derivation.S1_errors_branch_gone`

A sweep that could not offer some of the releases it listed exits 0 and reports the job done

- File: `src/cratekit/label/cli.py`
- Source: `u52-item-derivation.json`, row `S1_errors_branch_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_an_increment_that_could_not_offer_every_release_fails_the_item`

Old text:

```
    if result.errors:
        raise refuse(
            "label-sweep-incomplete",
```

New text:

```
    if False:
        raise refuse(
            "label-sweep-incomplete",
```

### `u52-zero-rows.H5_verifier_passthrough_gone`

REMOVE THE LAYER ALONE: the verification boundary swallows an adapter's own refusal into label-playlist-unreadable

- File: `src/cratekit/label/cli.py`
- Source: `u52-zero-rows.json`, row `H5_verifier_passthrough_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_workers.py`
- Collected: 262 against a baseline of 262
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_workers.py::test_a_refusal_the_harvest_verifier_raises_in_kind_keeps_its_own_reason`

Old text:

```
        except CratekitError:
            raise
        except Exception as exc:
```

New text:

```
        except Exception as exc:
```

### `r838-c.R1_library_bound`

mark_record._recognize: accept a record written for another library

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R1_library_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_unreadable_record_refuses_rather_than_reading_as_empty[{"version": 1, "library_id": "another-library", "marks": []}]`

Old text:

```
        if library_id != self.cfg.library.volume_id:
```

New text:

```
        if False:
```

### `r838-c.R2_remark_clears`

mark_record.record_marked: append a second entry for a re-mark by the same pass rather than replacing the first

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-c.json`, row `R2_remark_clears`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_mark_after_an_unmark_clears_the_stamp`

Old text:

```
                    if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                        entries[index] = fresh
                        break
```

New text:

```
                    if False:
                        entries[index] = fresh
                        break
```

### `r838-d.R3b_stamp_target`

mark_record.record_unmarked: stamp the playlist's mark under any pass, so another pass's mark reads as put back

- File: `src/cratekit/sync/mark_record.py`
- Source: `r838-d.json`, row `R3b_stamp_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
                if (entry.pass_name, entry.playlist_id) == (pass_name, playlist_id):
                    entries[index] = replace(entry, unmarked=when)
```

New text:

```
                if entry.playlist_id == playlist_id:
                    entries[index] = replace(entry, unmarked=when)
```

### `r838-a.U1_refuse_stranger`

unmark._narrowed: drop the refusal, so a playlist the pass never marked is silently passed over rather than refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U1_refuse_stranger`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_pass_never_marked_is_refused_whatever_its_title`

Old text:

```
    if strangers:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r838-a.U3_pass_filter`

unmark: take every pass's marks as the named pass's, so a playlist the pass never marked is planned

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U3_pass_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_the_record_holds_nothing_for_is_a_gated_plan_of_nothing`

Old text:

```
        tuple(entry for entry in every if entry.pass_name == name),
```

New text:

```
        tuple(entry for entry in every),
```

### `r838-a.U4_already_unmarked_stamp`

unmark._item: ignore the unmarked stamp, so a second run is decided by the title alone

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U4_already_unmarked_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_second_run_plans_nothing_and_still_asks`

Old text:

```
    if entry.unmarked:
        return {
```

New text:

```
    if False:
        return {
```

### `r838-a.U5_marked_again`

unmark._item: ignore a later mark by another pass, so this pass's unmark takes off that pass's prefix

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U5_marked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
    later = _later(entry, every)
    if later:
```

New text:

```
    later = _later(entry, every)
    if False:
```

### `r838-a.U6_later_order`

unmark._later: an EARLIER mark by another pass also supersedes, so the latest pass's own unmark is refused

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U6_later_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`

Old text:

```
        and other.marked > entry.marked
```

New text:

```
        and other.marked != entry.marked
```

### `r838-a.U8_title_already_back`

unmark._item: no already-put-back branch, so a title already restored is reported as retitled by hand

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-a.json`, row `U8_title_already_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`

Old text:

```
    if current == entry.name:
```

New text:

```
    if False:
```

### `r838-b.U10_digest_names`

unmark._payload: the digest omits the planned renames, so an answer to one plan carries out another

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U10_digest_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_an_answer_is_stale_once_the_account_moves`

Old text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if item["action"] == UNMARK
```

New text:

```
            (item["id"], item["marked_as"], item["to"])
            for item in items
            if False
```

### `r838-b.U13_recheck`

unmark: no recheck against the second listing, so a title changed after the answer is renamed anyway

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U13_recheck`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`

Old text:

```
            if now.get(identity) != entry.to:
```

New text:

```
            if False:
```

### `r838-b.U15_rename_target`

unmark: rename to the title the mark wrote rather than the one before it

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U15_rename_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 8 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_later_mark_by_another_pass_owns_the_prefix`
  - `tests/test_sync_unmark.py::test_a_pass_that_marked_three_plans_three_renames_back_and_applies_them`
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`
  - `tests/test_sync_unmark.py::test_a_playlist_that_changes_between_the_plan_and_the_rename_is_said`
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`
  - `tests/test_sync_unmark.py::test_a_title_already_put_back_is_skipped_without_a_stamp`
  - `tests/test_sync_unmark.py::test_playlist_given_twice_narrows_to_both_marks_named`
  - `tests/test_sync_unmark.py::test_playlist_narrows_to_the_marks_named`

Old text:

```
            remote.rename_playlist(identity, entry.name)
```

New text:

```
            remote.rename_playlist(identity, entry.to)
```

### `r838-b.U16_part_way_names`

unmark._failed_part_way: report nothing put back, so a partial failure loses what landed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U16_part_way_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_failure_part_way_names_what_was_put_back`

Old text:

```
        "unmarked": list(landed),
```

New text:

```
        "unmarked": [],
```

### `r838-b.U9_renamed_since`

unmark._item: plan any title carrying the prefix, so a playlist retitled by hand with the prefix kept is renamed

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-b.json`, row `U9_renamed_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_retitled_by_hand_since_the_mark_is_listed_and_left`

Old text:

```
    if current != entry.to:
        how =
```

New text:

```
    if not playlists.is_swept_name(current):
        how =
```

### `r838-c.U7b_not_listed_rerun`

U7 measured again after the not-listed test was added: no NOT_LISTED branch, so a playlist the account dropped falls through to the title comparison

- File: `src/cratekit/sync/unmark_cli.py`
- Source: `r838-c.json`, row `U7b_not_listed_rerun`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_unmark.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_unmark.py::test_a_playlist_the_account_no_longer_lists_is_said_and_left`

Old text:

```
    if current is None:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

New text:

```
    if current is None and False:
        return {
            **base,
            "action": SKIP,
            "reason": NOT_LISTED,
```

### `r1394.S10_later_unsent_write_hides_the_pending`

stopped writes: the latest record is read whether or not it sent a move, so a refused finish hides the pending write it was finishing, round two's BLOCKING row

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S10_later_unsent_write_hides_the_pending`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_stopped.py::test_a_later_write_that_sent_no_move_does_not_hide_a_pending_one`

Old text:

```
            if held is None or (write.pending, write.at) > (held[1].pending, held[1].at):
```

New text:

```
            if held is None or write.at > held[1].at:
```

### `r1394.S1_counts_beyond_the_moves_trusted`

stopped write: counts larger than the write's moves are trusted rather than read as nothing known

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S1_counts_beyond_the_moves_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`

Old text:

```
    if sent is None or landed is None or not landed <= sent <= total:
```

New text:

```
    if sent is None or landed is None or not landed <= sent:
```

### `r1394.S2_missing_counts_read_as_none_sent`

stopped write: a moving step with no counts reads as no move sent, so any agreed path reading finishes it, as before R-1394

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S2_missing_counts_read_as_none_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
        return 0, total
    return landed, sent
```

New text:

```
        return 0, 0
    return landed, sent
```

### `r1394.S3_bool_count_read`

stopped write: a count written as true or false is read as a number

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S3_bool_count_read`
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

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S4_negative_count_read`
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

### `r1394.S5_sent_read_as_landed`

stopped write: the sent count is read from the landed field, so a move in flight reads as known not sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S5_sent_read_as_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`

Old text:

```
    return at, start, end, _count(value.get(SENT)), _count(value.get(LANDED))
```

New text:

```
    return at, start, end, _count(value.get(LANDED)), _count(value.get(LANDED))
```

### `r1394.S6_counts_not_wired`

stopped write: the counts read back never reach the stopped write, which keeps none landed and none sent

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S6_counts_not_wired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - `tests/test_sync_pair_settle.py::test_a_stopped_write_recorded_with_no_counts_is_finished_only_from_the_order_it_leaves`
  - `tests/test_sync_pair_settle.py::test_a_stopped_writes_counts_are_carried_past_its_runs_steps`
  - `tests/test_sync_pair_settle.py::test_every_move_accepted_and_an_agreed_reading_short_of_their_end_is_still_a_lag`
  - `tests/test_sync_pair_stopped.py::test_a_moving_step_reads_back_its_counts`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts0]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts1]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts2]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts3]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts4]`
  - `tests/test_sync_pair_stopped.py::test_counts_missing_or_not_fitting_the_moves_are_read_as_nothing_known[counts5]`
  - `tests/test_sync_pair_stopped.py::test_every_move_accepted_reads_as_every_move_landed_whatever_the_counts`

Old text:

```
        landed=landed,
        sent=reached_by,
```

New text:

```
        landed=0,
        sent=0,
```

### `r1394.S8_positions_first_only`

positions: only the first count on the path that leaves the order is answered, so a track taken off since hides a later one

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S8_positions_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_an_unread_track_taken_off_the_account_after_the_stop_is_never_put_back`
  - `tests/test_sync_pair_stopped.py::test_orders_on_the_path_that_differ_only_by_a_track_taken_off_all_count`

Old text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )
```

New text:

```
    return tuple(
        index
        for index, state in enumerate(passed(start, target))
        if [one for one in dict.fromkeys(state) if one in common] == shown
    )[:1]
```

### `r1394.S9_moving_step_counts_dropped`

moving step: the record written carries a sent count of 0 whatever it is told

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1394.json`, row `S9_moving_step_counts_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[False]`
  - `tests/test_sync_pair_settle.py::test_a_continue_of_a_refused_finish_is_held_to_the_plans_reading_not_the_checks[True]`
  - `tests/test_sync_pair_settle.py::test_a_finish_keeps_an_unread_track_the_stopped_write_did_not_move_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_planned_again_in_the_writing_command_is_held_to_its_own_reading`
  - `tests/test_sync_pair_settle.py::test_a_finish_puts_an_unread_track_the_stopped_move_put_in_front_where_the_write_was_taking_it`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_adds_served_as_the_moves_left_it_finishes`
  - `tests/test_sync_pair_settle.py::test_a_finish_that_also_removes_is_refused_on_a_reading_that_lags_the_stopped_move`
  - `tests/test_sync_pair_settle.py::test_a_finish_the_adapter_refuses_leaves_the_stopped_write_pending`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_sync_pair_settle.py::test_a_finish_whose_stopped_move_was_an_unread_track_is_held_to_it_in_its_place`
  - `tests/test_sync_pair_settle.py::test_a_finish_with_no_unread_track_is_put_in_rekordboxs_order`
  - `tests/test_sync_pair_settle.py::test_a_move_whose_fate_is_unknown_holds_the_order_before_it_and_finishes_the_one_after`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_that_move_leaves_it_is_finished`
  - `tests/test_sync_pair_settle.py::test_a_stop_after_one_of_three_moves_read_as_the_old_order_is_held_however_long_it_agrees`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        SENT: int(sent),
```

New text:

```
        SENT: 0,
```

### `u234.O15_reordered_counts_additions`

reordered compares the readings whole, so a track added between them is read as a reorder

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `u234.json`, row `O15_reordered_counts_additions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`
- Collected: 177 against a baseline of 177
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_between_two_readings_is_no_reorder`

Old text:

```
    return [one for one in current if one in common] != [
        one for one in dict.fromkeys(kept) if one in common
    ]


__all__
```

New text:

```
    return current != list(dict.fromkeys(kept))


__all__
```

### `r235-a.M11_session_lock_dropped`

a revert holds the registry lock and not the session lock

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M11_session_lock_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
    with session.session_lock(cfg), config._exclusive_lock(lock_path(cfg)):
```

New text:

```
    with config._exclusive_lock(lock_path(cfg)):
```

### `r235-a.M12_second_record_replaces`

record_cutover replaces a tree already recorded native instead of refusing

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M12_second_record_replaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_tree_already_recorded_is_not_recorded_again`

Old text:

```
        if standing is not None and standing.mode == Mode.DATABASE:
            # ASKED UNDER THE LOCK, which is the only place the answer holds.
```

New text:

```
        if False:
            # ASKED UNDER THE LOCK, which is the only place the answer holds.
```

### `r235-a.M13_snapshot_check_dropped`

the verified snapshot check is no longer in the precheck table

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M13_snapshot_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 11 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_leave_intake_xml-cutover-xml-pending-no-pending-intake-xml]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_open_a_run-cutover-open-run-no-open-run]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_export-cutover-export-missing-fresh-export]`
  - `tests/test_cutover_cli.py::test_each_precheck_failure_refuses_before_anything_is_recorded[_remove_the_snapshot-cutover-snapshot-missing-verified-snapshot]`
  - `tests/test_cutover_cli.py::test_the_plan_names_the_root_and_approval_records_that_tree_alone`
  - `tests/test_cutover_cli.py::test_two_failing_prechecks_are_both_named_on_one_run`
  - `tests/test_cutover_precheck.py::test_a_missing_snapshot_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_unverified_capture_does_not_count_as_a_snapshot`
  - `tests/test_cutover_precheck.py::test_the_report_and_the_assertion_refuse_with_one_cause`
  - `tests/test_cutover_precheck.py::test_the_report_carries_each_refusal_and_does_not_stop_at_the_first`
  - `tests/test_cutover_precheck.py::test_the_report_names_every_check_in_the_order_the_assertion_refuses`

Old text:

```
    ("fresh-export", _export_refusal),
    ("verified-snapshot", _snapshot_refusal),
)
```

New text:

```
    ("fresh-export", _export_refusal),
)
```

### `r235-a.M1_unreadable_log_skipped`

the registry gates no longer refuse on a session record they cannot read, so a torn record reads as no open run and no native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M1_unreadable_log_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_flip_rather_than_reading_as_no_open_run`
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`

Old text:

```
    parsed, unreadable = session.scan_log(cfg)
    if unreadable:
```

New text:

```
    parsed, unreadable = session.scan_log(cfg)
    if False:
```

### `r235-a.M2_margin_zero`

the native write margin is no days, so a write whose universal time date is the day before the cutover day is left out

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M2_margin_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[2026-07-31T23:50:00Z]`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=0)
```

### `r235-a.M3_margin_two_days`

the native write margin is two days, so a write two days before the cutover day still counts

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M3_margin_two_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_the_day_before_the_margin_is_the_first_day_left_out`

Old text:

```
NATIVE_WRITE_MARGIN = timedelta(days=1)
```

New text:

```
NATIVE_WRITE_MARGIN = timedelta(days=2)
```

### `r235-a.M4_unparseable_start_predates`

a session start nothing can parse is read as before the cutover, so its write does not count

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M4_unparseable_start_predates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_write_that_cannot_be_shown_to_predate_the_cutover_counts[not a timestamp]`

Old text:

```
    except ValueError:
        return False
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

New text:

```
    except ValueError:
        return True
    return began < cutover_on - NATIVE_WRITE_MARGIN
```

### `r235-a.M5_updates_not_counted`

only a creation counts as a native write, an update does not

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M5_updates_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_update_counts_as_a_native_write_as_a_creation_does`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id and change.created > 0
```

### `r235-a.M6_any_tree_counts`

a write to any tree counts as a write to this one

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M6_any_tree_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            (change.created > 0 or change.updated > 0)
```

### `r235-a.M7_zero_count_counts`

a record naming the tree with nothing added counts as a native write

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M7_zero_count_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 2 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_a_write_to_another_tree_does_not_close_this_trees_door`
  - `tests/test_cutover_precheck.py::test_a_session_that_wrote_nothing_to_this_tree_leaves_the_revert_open`

Old text:

```
            change.tree == tree_id and (change.created > 0 or change.updated > 0)
```

New text:

```
            change.tree == tree_id
```

### `r235-a.M8_open_run_reverts`

a revert no longer refuses over an open run

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M8_open_run_reverts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`

Old text:

```
    if open_runs:
        raise refuse(
            "cutover-open-run",
            f"session {open_runs[0].session_id} has not reached a terminal "
```

New text:

```
    if False:
        raise refuse(
            "cutover-open-run",
            f"session {open_runs[0].session_id} has not reached a terminal "
```

### `r235-a.M9_library_guard_removed`

revert_cutover no longer asserts the tree is revertible, leaving only the verb's own check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-a.json`, row `M9_library_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 4 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_a_record_nobody_can_read_refuses_the_revert_rather_than_reading_as_no_write`
  - `tests/test_cutover_precheck.py::test_a_revert_after_a_native_write_is_refused_by_the_library_itself`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_cutover_precheck.py::test_the_revert_holds_the_session_lock_while_it_asks_and_writes`

Old text:

```
        assert_revertible(cfg, tree_id)
        updated = read(cfg).without_record(tree_id)
```

New text:

```
        updated = read(cfg).without_record(tree_id)
```

### `r235-b.M14_empty_export_accepted`

an export of no bytes passes the fresh export check

- File: `src/cratekit/core/tree_registry.py`
- Source: `r235-b.json`, row `M14_empty_export_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cutover_precheck.py`, `tests/test_cutover_cli.py`
- Collected: 66 against a baseline of 66
- Kills: 1 (killed)
- Killed:
  - `tests/test_cutover_cli.py::test_an_empty_export_is_no_export`

Old text:

```
    if export_path.is_file() and export_path.stat().st_size != 0:
```

New text:

```
    if export_path.is_file():
```

### `u79-a.A1_ambiguous_listed`

A title that reads two ways is listed on one candidate without a person

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A1_ambiguous_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-title-reading]`
  - `tests/test_intake_missing_search.py::test_a_title_with_two_readings_is_never_listed_on_one_candidate[the-version-reading]`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.full:
        return None
```

### `u79-a.A2_full_page_listed`

A full page is read as the whole answer, so its one exact hit is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A2_full_page_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_full_page_is_never_the_whole_answer_so_its_one_exact_hit_is_offered`

Old text:

```
    if answer.ambiguous or answer.full:
        return None
```

New text:

```
    if answer.ambiguous:
        return None
```

### `u79-a.A3_unreadable_ignored`

A row of the answer that could not be read no longer stops a listing

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A3_unreadable_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_a_row_that_cannot_be_read_is_offered`

Old text:

```
    if answer.unreadable or not exact:
```

New text:

```
    if not exact:
```

### `u79-a.A4_no_identifier_listed`

Exact candidates carrying no identifier are one distinct value and are listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A4_no_identifier_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`
  - `tests/test_intake_missing_search.py::test_the_only_exact_candidate_carrying_no_identifier_is_not_listed`

Old text:

```
    if any(not one.track.ref for one in exact):
        return None
```

New text:

```
    if False:
        return None
```

### `u79-a.A5_two_exact_picked`

Two exact candidates list the first, the pick the brief forbids

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A5_two_exact_picked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_acceptance_naming_none_of_several_candidates_lists_nothing`
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`
  - `tests/test_intake_missing_search.py::test_more_candidates_than_the_screen_holds_are_truncated_and_counted`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if len({one.track.ref for one in exact}) != 1:
```

New text:

```
    if len({one.track.ref for one in exact}) < 1:
```

### `u79-b.B1_floor_halved`

The floor's value is halved, so a weaker hit is shown

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B1_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`

Old text:

```
CANDIDATE_FLOOR = 60.0
```

New text:

```
CANDIDATE_FLOOR = 30.0
```

### `u79-b.B2_score_before_exact`

A near miss scoring 100 leads an exact candidate

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B2_score_before_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_under_the_floor_of_nothing_is_still_first`

Old text:

```
            (not one.exact, -one.score, position, one)
```

New text:

```
            (False, -one.score, position, one)
```

### `u79-b.B3_no_identifier_offered`

A candidate with no identifier is offered as an option

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B3_no_identifier_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_exact_candidate_beside_an_exact_one_with_no_identifier_is_offered`
  - `tests/test_intake_missing_search.py::test_exact_hits_with_no_identifier_are_reported_as_that_and_not_as_no_resemblance`

Old text:

```
            if one.track.ref and (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

New text:

```
            if (one.exact or one.score >= CANDIDATE_FLOOR)
        ),
        key=
```

### `u79-b.B4_rejected_read_as_accepted`

A rejected row falls through to the accepted path and its one candidate is listed

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B4_rejected_read_as_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_rejected_row_is_reported_and_never_searched_again`

Old text:

```
    if held.verdict is review.Verdict.REJECTED:
```

New text:

```
    if False:
```

### `u79-b.B5_unspecific_yes_takes_first`

An acceptance naming none of several candidates lists the first

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B5_unspecific_yes_takes_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_acceptance_naming_none_of_several_candidates_lists_nothing`

Old text:

```
    if chosen is None and len(held.options) == 1:
```

New text:

```
    if chosen is None and len(held.options) >= 1:
```

### `u79-b.B6_option_track_mismatch`

An accepted option whose detail names another track is listed as that track

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B6_option_track_mismatch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_option_that_does_not_carry_its_own_track_lists_nothing`

Old text:

```
    if track is None or not track.ref or track.ref != option.option_id:
```

New text:

```
    if track is None or not track.ref:
```

### `u79-b.B7_identity_without_version`

The question is keyed without the version, so two versions are one item

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B7_identity_without_version`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_search_question_about_one_emoji_title_is_not_another_ones`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`

Old text:

```
        "version": wanted.version_key,
    }
```

New text:

```
        "version": "",
    }
```

### `u79-b.B8_open_item_searched_again`

A row already in front of a person is searched for again

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B8_open_item_searched_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_second_run_offers_nothing_new_and_spends_no_search`

Old text:

```
    if held.verdict is None:
        return Proposal(
```

New text:

```
    if held.verdict is None:
        return None
    if held.verdict is None:
        return Proposal(
```

### `r757-c1.S4_rehearsal_says_it_sent`

comparison_warning: say sent over a rehearsal, the review's fix

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c1.json`, row `S4_rehearsal_says_it_sent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if recorded.get("dry_run")
```

New text:

```
        if False
```

### `r757-c2.S5_unread_number_printed_as_zero`

comparison_warning: print a total that was not read as 0

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S5_unread_number_printed_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_the_sentence_never_prints_an_unread_number_as_zero`

Old text:

```
            return f"an unread number of {unit}"
```

New text:

```
            return f"0 {unit}"
```

### `r757-c2.S6_twin_in_the_other_mode_says_nothing`

_already_queued: drop the sentence saying the open job runs the other comparison, the review's fix

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S6_twin_in_the_other_mode_says_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 758 against a baseline of 758
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_comparison.py::test_a_second_ask_in_the_other_mode_is_told_the_open_job_differs`

Old text:

```
    if asked_full is not None and asked_full != _is_full(job):
```

New text:

```
    if False:
```

### `r757-c2.S7_verb_says_nothing_of_the_comparison`

backup_library: leave the comparison sentence off the resumed envelope

- File: `src/cratekit/backup/cli.py`
- Source: `r757-c2.json`, row `S7_verb_says_nothing_of_the_comparison`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_backup_comparison.py`, `tests/test_backup_cli.py`, `tests/modules/test_tools.py`, `tests/test_doctor.py`
- Collected: 22663 against a baseline of 22663
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

### `u149.T2_two_folders_not_refused`

find_folder: drop the refusal of two live top level folders of one year, so the first is written to

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T2_two_folders_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_existing_folder_is_reused_and_two_of_one_year_place_nothing`

Old text:

```
    if len(found) > 1:
```

New text:

```
    if len(found) > 2:
```

### `u149.T3_folder_names_unread`

find_folder: read no names inside a live folder, so a held name is not seen

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T3_folder_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`
  - `tests/test_sync_twins.py::test_a_name_the_folder_already_holds_is_refused_by_name_never_counted`

Old text:

```
held=_live_children(db, found[0]))
```

New text:

```
held=frozenset())
```

### `u149.T4_removed_folder_live`

_live_top_folders: drop the soft delete filter, so a removed folder is reused

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T4_removed_folder_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_removed_year_folder_is_not_reused_and_a_live_one_is_made`

Old text:

```
        f"AND COALESCE({rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 ORDER BY ID"
```

New text:

```
        f"ORDER BY ID"
```

### `u149.T5_held_name_counted_free`

place: drop the refusal of a name the folder holds, so a second twin of one name is made

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T5_held_name_counted_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_twins.py::test_a_twin_name_the_folder_holds_is_left_and_named_and_the_landing_still_lands`
  - `tests/test_sync_twins.py::test_a_name_the_folder_already_holds_is_refused_by_name_never_counted`
  - `tests/test_sync_twins.py::test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year`

Old text:

```
    if name in folder.held:
```

New text:

```
    if False:
```

### `u149.T6_taken_name_free`

place: drop the refusal of a name this run already gave, so two twins share one name

- File: `src/cratekit/sync/twins.py`
- Source: `u149.json`, row `T6_taken_name_free`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_place_refuses_a_held_name_a_taken_name_an_empty_name_and_an_unplaced_year`

Old text:

```
    if name in taken:
```

New text:

```
    if False:
```

### `u213.M14_backfill_reason_check`

plan_backfill: leave a playlist for any refusal, so an expired session leaves every playlist instead of naming its act

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M14_backfill_reason_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_refusal_that_is_not_about_one_playlist_still_stops_the_run`

Old text:

```
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            twins.append(
```

New text:

```
            if False:
                raise
            twins.append(
```

### `u213.M15_backfill_left_action`

plan_backfill: plan a playlist whose listing was refused as a twin to make, with no rows

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M15_backfill_left_action`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`
  - `tests/test_sync_twins.py::test_a_playlist_the_provider_cannot_list_is_left_named_and_the_other_is_made`
  - `tests/test_sync_twins.py::test_a_playlist_whose_row_carries_no_id_is_left_and_the_other_is_planned`
  - `tests/test_sync_twins.py::test_every_playlist_left_writes_nothing_and_opens_no_gate`

Old text:

```
                    action=LEFT,
                    why=f"the account playlist could not be read: {exc.cause.message}",
```

New text:

```
                    action=CREATE,
                    why=f"the account playlist could not be read: {exc.cause.message}",
```

### `u213.M16_backfill_digest_reason`

Twin.identity: put the provider's words in the digest again, so a varying message makes the approved run stale

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M16_backfill_digest_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`

Old text:

```
            "why": self.refused or self.why,
```

New text:

```
            "why": self.why,
```

### `u213.M17_backfill_unread_tracks`

plan_backfill: plan from the read tracks alone, so an unread track is in neither the twin's misses nor its snapshot

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M17_backfill_unread_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
            ref: listing.tracks[ref] if ref in listing.tracks else listing.unread[ref].said()
            for ref in listing.order
```

New text:

```
            ref: listing.tracks[ref]
            for ref in listing.order
            if ref in listing.tracks
```

### `u213.M18_backfill_unread_reasons`

plan_backfill: hand matched no unread reasons, so an unread track the library lacks reads as merely not owned

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M18_backfill_unread_reasons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
            {ref: one.why for ref, one in listing.unread.items()},
```

New text:

```
            {},
```

### `u213.M19_matched_ambiguous_first`

matched: say an unread track two rows carry is unreadable rather than ambiguous

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M19_matched_ambiguous_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_an_untitled_track_two_library_rows_carry_is_ambiguous_not_unreadable`

Old text:

```
                    AMBIGUOUS
                    if found
                    else f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else NOT_OWNED
```

New text:

```
                    f"{unread[remote_id]}, {UNREAD_NOT_FOUND}"
                    if remote_id in unread
                    else AMBIGUOUS
                    if found
                    else NOT_OWNED
```

### `u213.M20_backfill_whole`

plan_backfill: read every listing as whole, so a short one is paired with a snapshot it does not have

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M20_backfill_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_short_listing_pairs_the_twin_with_no_snapshot`

Old text:

```
                whole=listing.short is None,
```

New text:

```
                whole=True,
```

### `u213.M2_backfill_refused_reason`

plan_backfill: record no refusal reason on a left playlist, so its digest carries the provider's words

- File: `src/cratekit/sync/twins.py`
- Source: `u213.json`, row `M2_backfill_refused_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins.py`, `tests/test_intake_land_twins.py`
- Collected: 52 against a baseline of 52
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_left_playlists_digest_holds_its_refusal_not_the_providers_words`

Old text:

```
                    refused=exc.cause.reason,
```

New text:

```
                    refused="",
```

### `r815-b.J1_one_refusal_ends_the_asking`

_asked: remember no refusal

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J1_one_refusal_ends_the_asking`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`

Old text:

```
    if judged.answer == searchers.Answer.BLOCKED.value:
        tools.refused = judged.reason
```

New text:

```
    if False:
        tools.refused = judged.reason
```

### `r815-b.J2_an_unread_catalogue_ends_the_run`

_asked: never stop on the gate's bound of unread releases

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J2_an_unread_catalogue_ends_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`

Old text:

```
    if tools.asking.given_up:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r815-b.J3_a_failing_provider_ends_the_run`

_asked: never stop on the reader's bound of failed reads

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J3_a_failing_provider_ends_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    if tools.reader.given_up:
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r815-b.J4_a_record_never_holds_on_its_own`

_judged: take a hold from recorded words without asking

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-b.json`, row `J4_a_record_never_holds_on_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_record_of_one_tracks_album_does_not_hold_a_release_its_next_track_passes`
  - `tests/test_label_judge.py::test_recorded_words_that_would_hold_are_asked_about_before_the_release_is_held`

Old text:

```
    if recorded is not None and not recorded.held:
        return recorded, False
```

New text:

```
    if recorded is not None:
        return recorded, False
```

### `r815-c.J11_the_scope_reads_the_registry`

_Scope.holds: compare the identifier as text

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J11_the_scope_reads_the_registry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_filed_under_a_labels_old_identifier_is_in_a_run_scoped_to_the_label`

Old text:

```
        return entry is not None and entry.label_id in self.label_ids
```

New text:

```
        return label_id in self.label_ids
```

### `r815-c.J12_a_release_held_and_gone_is_counted_held`

_left_review: report gone whatever holds the release

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J12_a_release_held_and_gone_is_counted_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_release_another_job_held_while_this_one_was_asking_is_counted_held`
  - `tests/test_label_judge.py::test_a_release_held_under_an_earlier_holds_run_is_counted_held_when_it_is_redone`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`

Old text:

```
    if standing is not None and standing.state == review.HOLD_HELD:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
```

New text:

```
    if False:
        return _report(item_id, HELD, _held_already(standing), reason=standing.reason)
```

### `r815-c.J13_the_refusal_carries_the_counts`

_resume: let the refusal leave without the summary

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J13_the_refusal_carries_the_counts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_refusal_from_the_provider_parks_the_run_on_that_refusal`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-held-release]`
  - `tests/test_label_judge.py::test_a_run_stopped_part_way_and_resumed_judges_none_twice_and_skips_none[stopped-on-a-passed-release]`
  - `tests/test_label_judge.py::test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
            raise _with_summary(failed, cfg, store, queued.job_id) from failed
```

New text:

```
            raise
```

### `r815-c.J5_a_recorded_no_word_answer_is_not_asked_again`

_judged: ask about a release the catalogue already had no word for

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J5_a_recorded_no_word_answer_is_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[matched]`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[miss]`
  - `tests/test_label_judge.py::test_a_release_the_catalogue_already_had_no_word_for_is_not_asked_about_again[no-isrc]`

Old text:

```
    if recorded is None and isinstance(said, str) and said in genre_gate.NO_WORD_ANSWERS:
```

New text:

```
    if False:
```

### `r815-c.J6_a_decided_item_is_not_judged`

_judge_one: judge an item a person has decided

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J6_a_decided_item_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_item_decided_after_the_job_was_queued_is_untouched[accepted]`
  - `tests/test_label_judge.py::test_an_item_decided_after_the_job_was_queued_is_untouched[rejected]`

Old text:

```
        if found.stored_verdict is not None:
            return _report(
```

New text:

```
        if False:
            return _report(
```

### `r815-c.J7_a_returned_release_is_not_judged`

_judge_one: judge a release a person returned

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J7_a_returned_release_is_not_judged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_returned_release_is_not_judged_again_and_nobody_is_asked`

Old text:

```
        if genre_gate.returned_by(standing, found.payload):
            return _report(
```

New text:

```
        if False:
            return _report(
```

### `r815-c.J8_a_refusal_parks_and_fails_no_item`

handle: let a refusal fail the item

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J8_a_refusal_parks_and_fails_no_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_refusal_from_the_provider_parks_the_run_on_that_refusal`
  - `tests/test_label_judge.py::test_a_taxonomy_that_stops_being_readable_parks_the_run_and_fails_no_release`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    except CratekitError as exc:
        raise _parked(job, exc) from exc
    return artifacts.produced(ARTIFACTS, cfg, job, item, report)
```

New text:

```
    except CratekitError:
        raise
    return artifacts.produced(ARTIFACTS, cfg, job, item, report)
```

### `r815-c.J9_a_park_drops_the_jobs_tools`

_parked: keep the job's tools across a park

- File: `src/cratekit/label/judge_cli.py`
- Source: `r815-c.json`, row `J9_a_park_drops_the_jobs_tools`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`
- Collected: 76 against a baseline of 76
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_three_provider_reads_failing_in_a_row_stop_the_run`

Old text:

```
    _JOB_TOOLS.pop(str(job.job_id), None)
    if isinstance(error, jobs.Parked):
```

New text:

```
    if isinstance(error, jobs.Parked):
```

### `u103-a.A10_write_is_a_merge`

Replace the cache document with this pass's answers instead of laying them over what is kept

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A10_write_is_a_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_write_is_a_merge_so_an_overlapping_pass_does_not_drop_what_another_paid_for`

Old text:

```
            merged = {**self.read(plan), **answers}
```

New text:

```
            merged = dict(answers)
```

### `u103-a.A1_read_serves_only_answers`

Drop the reader's rule that only a match or a miss is served from a cache document

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A1_read_serves_only_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_only_an_answer_is_kept_or_served_in_either_direction`

Old text:

```
            if classify(payload)[0] not in _KEPT_OUTCOMES:
                continue
            answers[offset] = payload
```

New text:

```
            answers[offset] = payload
```

### `u103-a.A2_write_keeps_only_answers`

Drop the writer's rule that only a match or a miss is kept, removed alone so the reader's copy of the rule is not what is measured

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A2_write_keeps_only_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_only_an_answer_is_kept_or_served_in_either_direction`

Old text:

```
                    for offset in sorted(merged)
                    if classify(merged[offset])[0] in _KEPT_OUTCOMES
```

New text:

```
                    for offset in sorted(merged)
```

### `u103-a.A3_document_must_carry_its_plan`

Stop checking that a cache document carries the plan it was asked for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A3_document_must_carry_its_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
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

### `u103-a.A5_offset_must_be_planned`

Serve a kept answer at an offset the plan never asked for

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A5_offset_must_be_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_only_an_answer_is_kept_or_served_in_either_direction`

Old text:

```
            if offset not in planned or not isinstance(payload, dict):
```

New text:

```
            if not isinstance(payload, dict):
```

### `u103-a.A6_digest_in_the_key`

Take the recording's content digest out of the key material, so a changed file keeps its old key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A6_digest_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 5 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_file_misses_the_cache`
  - `tests/intake/test_recognition.py::test_every_field_of_the_plan_moves_the_key[digest]`
  - `tests/intake/test_recognition.py::test_the_monthly_bound_reads_what_is_owed_and_the_parts_ceiling_reads_the_grid`
  - `tests/intake/test_workers.py::test_a_changed_recording_misses_the_cache_and_is_paid_for`
  - `tests/intake/test_workers.py::test_two_recordings_sharing_a_stem_keep_a_tracklist_each`

Old text:

```
            "digest": self.digest,
            "offsets": list(self.offsets),
```

New text:

```
            "digest": "",
            "offsets": list(self.offsets),
```

### `u103-a.A7_offsets_in_the_key`

Take the offsets out of the key material, so a changed chunk plan keeps its old key

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A7_offsets_in_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_a_changed_chunk_plan_misses_the_cache`
  - `tests/intake/test_recognition.py::test_every_field_of_the_plan_moves_the_key[offsets]`

Old text:

```
            "offsets": list(self.offsets),
            "chunk_s": self.chunk_s,
```

New text:

```
            "offsets": [],
            "chunk_s": self.chunk_s,
```

### `u103-a.A9_refresh_reads_nothing_kept`

Let a refreshing pass read the kept answers anyway

- File: `src/cratekit/intake/acrcloud.py`
- Source: `u103-a.json`, row `A9_refresh_reads_nothing_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_intake_missing_isrc.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_refresh_reads_nothing_kept_and_lays_the_new_answers_over_the_document`
  - `tests/intake/test_workers.py::test_refresh_pays_for_every_chunk_again_and_the_new_answers_replace_the_kept_ones`

Old text:

```
    kept = kept_in.read(plan) if plan is not None and not refresh else {}
```

New text:

```
    kept = kept_in.read(plan) if plan is not None else {}
```

### `u146-a.B12_landing_takes_keyless_rows`

owned_in_library: a row whose job froze no date key is placed by the landing, into Undated for good

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-a.json`, row `B12_landing_takes_keyless_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill`

Old text:

```
    known = [row for row in rows if row.known and row.paths]
```

New text:

```
    known = [row for row in rows if row.paths]
```

### `u146-b.B13_first_of_two_rows`

owned_in_library: a file two active rows claim answers with the first, so a duplicate import joins All Favorites by a guess

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-b.json`, row `B13_first_of_two_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess`

Old text:

```
    by_path = native.single_rows_for(db, cfg, paths)
```

New text:

```
    by_path = native.content_ids_for(db, cfg, paths)
```

