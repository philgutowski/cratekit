# Mutation table: u312-replay-before-1

Measured by `scripts/mutate.py` on 2026-11-23 10:17 UTC, branch `HEAD` at `bece470e`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 188.

Full baseline: measured by this driver (the battery's verdict was not read: it is for commit `269cecd96b22`, and this tree is at `bece470ea56f`).

Subset baselines: 49, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r388-c.M14_status_registration_dropped` | `src/cratekit/core/cause.py` | maintainer | 70 file(s) | 8155 | 2 | killed |
| `u45-round-1.V1_transfer_failure_is_a_defect` | `src/cratekit/core/cause.py` | user | 33 file(s) | 5490 | 1 | killed |
| `u45-round-1.V2_summary_slug_undeclared` | `src/cratekit/core/cause.py` | user | 33 file(s) | 5490 | 4 | killed |
| `u44-author.D2_reason_slug_removed` | `src/cratekit/core/cause.py` | user | 32 file(s) | 5401 | 7 | killed |
| `u43-author-light.R2_undeclared_refusal_slug` | `src/cratekit/core/cause.py` | user | 31 file(s) | 5344 | 6 | killed |
| `u27-reports-round-1.R2_governed_tree_code` | `src/cratekit/core/cause.py` | user | 26 file(s) | 5087 | 1 | killed |
| `u155.T12_sources_type` | `src/cratekit/core/taxonomy_build.py` | user | 60 file(s) | 6713 | 2 | killed |
| `r431-b.B4_the_engine_never_asks` | `src/cratekit/acquire/match.py` | user | 10 file(s) | 1192 | 7 | killed |
| `r431-b.B7_the_engine_asks_under_the_tombstones_kind` | `src/cratekit/acquire/match_identity.py` | user | 10 file(s) | 1192 | 8 | killed |
| `r664.E4_title_not_split` | `src/cratekit/acquire/match_library.py` | user | 10 file(s) | 1192 | 106 | killed |
| `r118-a.A2_enoent_refuses_too` | `src/cratekit/core/secrets.py` | user | 9 file(s) | 1591 | 169 | killed |
| `u298.H16_reported_extra_under_progress` | `src/cratekit/core/jobs.py` | user | 18 file(s) | 1390 | 121 | killed |
| `r290-author.J3_closed_branch_removed` | `src/cratekit/core/jobs.py` | user | 31 file(s) | 2522 | 111 | killed |
| `r382.M16_parser_moved_lowercase` | `src/cratekit/label/catalogue.py` | maintainer | 10 file(s) | 804 | 2 | killed |
| `r504-a.A10_block_listed` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 804 | 11 | killed |
| `r504-a.A8_withheld_sign` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 804 | 15 | killed |
| `r504-a.A9_summary_reworded` | `src/cratekit/label/catalogue.py` | user | 10 file(s) | 804 | 10 | killed |
| `r431-b.B9_the_freeze_drops_the_field` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 3 | killed |
| `r504-b.B1_verb_drops_short` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 3 | killed |
| `r504-b.B4_no_progress_block` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 5 | killed |
| `r504-b.B5_noop_silent` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 2 | killed |
| `r504-b.B6_warning_reworded` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 3 | killed |
| `u103-b.C8_set_no_op_carries_warnings` | `src/cratekit/intake/cli.py` | user | 9 file(s) | 595 | 2 | killed |
| `u52-item-derivation.A1_acquires_early_return_gone` | `src/cratekit/sync/run.py` | user | 2 file(s) | 211 | 3 | killed |
| `u52-item-derivation.A2_acquires_default_false` | `src/cratekit/sync/run.py` | user | 2 file(s) | 211 | 6 | killed |
| `r704-a.R1_increment_ignores_the_flag` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R2_rate_limit_not_retryable` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R3_remedy_retry_later` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R4_detail_unmarked` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r704-a.R5_flag_not_stored` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 2 | killed |
| `r704-a.R6_sentence_reworded` | `src/cratekit/sync/run.py` | user | 4 file(s) | 442 | 1 | killed |
| `r263.W1_no_unrecorded_state` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 4 | killed |
| `r263.W2_state_word` | `src/cratekit/sync/watermarks.py` | user | 5 file(s) | 569 | 3 | killed |
| `r504-a.A11_boundary_refuses` | `src/cratekit/label/cli.py` | user | 4 file(s) | 0 | collection error | collect-error |
| `r504-a.A12_boundary_drops_short` | `src/cratekit/label/cli.py` | user | 4 file(s) | 551 | 5 | killed |
| `u309.U5_reserve_written` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 9 file(s) | 514 | 136 | killed |
| `r835-a.L1_load_carries_the_label_map` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 356 | 28 | killed |
| `u27-r80-write-probe-replacement.W8_read_probe_flags` | `src/cratekit/core/cause.py` | user | 1 file(s) | 358 | 1 | killed |
| `u45-round-1.V3_marker_restored` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4315 | collection error | collect-error |
| `u45-round-1.V5_module_toggle_dropped` | `src/cratekit/cli/registry.py` | user | 24 file(s) | 4318 | collection error | collect-error |
| `u43-author-light.R1_marker_restored` | `src/cratekit/cli/registry.py` | maintainer | 21 file(s) | 4145 | collection error | collect-error |
| `u27-reports-round-1.R1_delete_review_precondition` | `src/cratekit/cli/registry.py` | user | 14 file(s) | 3856 | 2 | killed |
| `u27-reports-round-2.S5b_engine_default_drift` | `src/cratekit/modules/reports/duplicates.py` | user | 2 file(s) | 382 | 3 | killed |
| `u27-reports-round-1.C1_tree_absent_refusal` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.C2_tree_anchored_at_zero` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.C4_placement_count` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-2.C3_uncovered_order` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-2.C3b_tie_break` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-3-fixes.F6_folder_count_overwrite` | `src/cratekit/modules/reports/coverage.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-1.L1_distinct_tracks` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L3_empty_tempo_is_zero` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L4_median_even` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L5_unused_buckets` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L6_entries_in_no_playlist` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u27-reports-round-1.L7_shape_governed_filter` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-2.L2_genre_parent` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 2 | killed |
| `u27-reports-round-3-fixes.F2_depth_origin` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 1 | killed |
| `u311.D3_tempo_never_read` | `src/cratekit/modules/reports/library.py` | user | 1 file(s) | 24 | 2 | killed |
| `r722.T8_lenient_energy_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2981 | 1 | killed |
| `r722.T9_lenient_open_raises` | `src/cratekit/core/tags.py` | user | 27 file(s) | 2981 | 305 | killed |
| `r221-a.E1_outcome_forgets_the_run` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 722 | 5 | killed |
| `r221-a.E2_outcome_payload_drops_the_key` | `src/cratekit/modules/tools/backup.py` | user | 7 file(s) | 722 | 7 | killed |
| `r338-a.B3_capture_is_a_copy` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r338-a.B8_contained_share_copied_twice` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 8 | killed |
| `r338-b.R6_switch_ignored` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 1 | killed |
| `r338-c.C1_absent_share_never_said` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 4 | killed |
| `r338-c.C2_carried_share_still_warned` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 7 file(s) | 722 | 2 | killed |
| `r154-b.B11_marker_name_safety` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 5 | killed |
| `r222-a.A1_nothing_held` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 5 | killed |
| `r222-a.A5_held_run_takes_no_slot` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 5 | killed |
| `r222-a.A8_floor_read_by_a_rehearsal` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 3 | killed |
| `r222-a.A9_rehearsal_purges` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 277 | 4 | killed |
| `u45-round-1.E1_rehearsal_publishes` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 7 | killed |
| `u45-round-1.E2_publish_unconditional` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 7 | killed |
| `u45-round-1.E4_return_codes_unread` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 16 | killed |
| `u45-round-2.E5_outcome_ok_widened` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 1 | killed |
| `u48-author.E1_listing_return_code_inverted` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 17 | killed |
| `u48-author.P1_listing_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 4 | killed |
| `u48-author.P2_purge_classification_dropped` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 1 | killed |
| `u48-author.P4_warning_not_recorded_on_the_portion` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 5 | killed |
| `u48-author.P6_purge_count_not_named` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 1 | killed |
| `u48-author.P7_listing_message_reworded` | `src/cratekit/modules/tools/backup.py` | user | 6 file(s) | 690 | 1 | killed |
| `r367.E1_a_failed_transfer_is_unread` | `src/cratekit/modules/tools/backup.py` | user | 2 file(s) | 282 | 15 | killed |
| `r367.G12_listing_results_are_discarded` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 2 | killed |
| `r367.G3_membership_is_inverted` | `src/cratekit/modules/tools/backup_snapshot.py` | user | 2 file(s) | 282 | 4 | killed |
| `r187-a.A11_no_cutoff` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 4 | killed |
| `r187-a.A6_first_of_several` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 4 | killed |
| `u43-author-light.E1_anchor_is_its_own_companion` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 8 | killed |
| `u43-author-light.E3_tempo_serialized_as_bpm` | `src/cratekit/modules/tools/setbuilder.py` | user | 2 file(s) | 268 | 4 | killed |
| `u311.C8_unreadable_number_raises` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 339 | 43 | killed |
| `u311.C9_anchor_comes_back` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 339 | 13 | killed |
| `u42-author-round-2.C2_unknown_defaults_lossless` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C1_undecided_derived` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C3_strict_consults_the_marker` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 3 | killed |
| `u42-author.C4_marked_lossless_dropped` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.C5_empty_marker_matches_everything` | `src/cratekit/acquire/cli.py` | user | 1 file(s) | 24 | 1 | killed |
| `u42-author.P2_relative_path_leaks_the_root` | `src/cratekit/acquire/cli.py` | maintainer | 1 file(s) | 24 | 5 | killed |
| `u169.A3_worker_never_declines` | `src/cratekit/acquire/cli.py` | user | 3 file(s) | 250 | 9 | killed |
| `r685-a.V1_route_inbox_export_reads_the_shipped_text` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 215 | 4 | killed |
| `u246.S1_adapter_asked_empty` | `src/cratekit/acquire/adapter.py` | user | 4 file(s) | 258 | 70 | killed |
| `u197.M5_adapter_name` | `src/cratekit/acquire/vendored.py` | user | 3 file(s) | 643 | 11 | killed |
| `r1411.A1_agreed_order_always_stands` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 11 | killed |
| `r1411.A3_added_tracks_asked_of_the_agreed_order` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1309 | 7 | killed |
| `r722.S5_catch_oserror_only` | `src/cratekit/adopt/scan.py` | user | 6 file(s) | 690 | 62 | killed |
| `u59.M9_column_repointed` | `src/cratekit/core/rb_writer.py` | user | 22 file(s) | 2717 | 176 | killed |
| `u138.E1_terminal_check` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 4 | killed |
| `u138.S11_rule_not_written` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 4 | killed |
| `u138.S12_message_names_the_portion` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 4 | killed |
| `u138.S13_remedy_points_back_at_ack` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 8 | killed |
| `u138.S1_session_rule_gone` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 20 | killed |
| `u138.S2_any_answer_gets_the_age_rule` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 13 | killed |
| `u138.S3_stale_not_refused` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 10 | killed |
| `u138.S6_bound_six_days` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 5 | killed |
| `u138.S8_rule_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 6 | killed |
| `u138.S9_answer_not_recorded` | `src/cratekit/core/session_ack.py` | user | 43 file(s) | 4024 | 4 | killed |
| `u49-author.L4_a_malformed_holder_raises_again` | `src/cratekit/core/session_holders.py` | user | 13 file(s) | 2568 | 1 | killed |
| `u254.M07_always_append` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 85 | killed |
| `u254.M19_already_inverted` | `src/cratekit/adopt/apply.py` | user | 6 file(s) | 741 | 33 | killed |
| `u254.C4_append_not_append` | `src/cratekit/core/config.py` | user | 4 file(s) | 963 | 54 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 13 file(s) | 811 | 5 | killed |
| `u219.A4_additions_rows` | `src/cratekit/write/rebuild.py` | user | 11 file(s) | 728 | 21 | killed |
| `u155.W1_derivation` | `src/cratekit/write/rebuild.py` | user | 10 file(s) | 704 | 7 | killed |
| `u58-workers-and-wav.H1_run_unbound` | `src/cratekit/cli/handlers.py` | user | 8 file(s) | 597 | 33 | killed |
| `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 343 | 41 | killed |
| `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound` | `src/cratekit/cli/handlers.py` | user | 6 file(s) | 343 | 21 | killed |
| `u23-round-8-independent.A1_at_risk_always_true` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.A2_at_risk_always_false` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 6 | killed |
| `u23-round-8-independent.A3_at_risk_drops_the_original_clause` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.A4_at_risk_drops_the_record_value` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.A5_at_risk_drops_this_call` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.A6_at_risk_original_by_identity` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 2 | killed |
| `u23-round-8-independent.B1_settled_never_refuses` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.B3_settled_bytes_clause_inverted` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 4 | killed |
| `u23-round-8-independent.C1_shape2_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 3 | killed |
| `u23-round-8-independent.C2_shape3_bypasses_the_check` | `src/cratekit/adopt/revert.py` | user | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.D1_bytes_agree_drops_the_size_gate` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 1 | killed |
| `u23-round-8-independent.D2_bytes_agree_size_gate_inverted` | `src/cratekit/adopt/revert.py` | maintainer | 1 file(s) | 615 | 6 | killed |

## Row definitions

### `r388-c.M14_status_registration_dropped`

Remove the slug from core.cause REASONS, the P5 registration beside the reservation

- File: `src/cratekit/core/cause.py`
- Source: `r388-c.json`, row `M14_status_registration_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_acquire_workers.py`, `tests/test_adapter_listing.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_discovery.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_incremental_sync.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_job_outcome.py`, `tests/test_jobs.py`, `tests/test_label_approved.py`, `tests/test_label_registry_verbs.py`, `tests/test_label_slug.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_listdoc.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_metadata_policy.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_uncredited_tombstone.py`, `tests/test_vocals_cli.py`, `tests/test_write_session.py`
- Collected: 8155 against a baseline of 8155
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

### `u45-round-1.V1_transfer_failure_is_a_defect`

Classify a failed transfer as INTERNAL, so an unreachable remote tells a person to report a bug

- File: `src/cratekit/core/cause.py`
- Source: `u45-round-1.json`, row `V1_transfer_failure_is_a_defect`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5490 against a baseline of 5490
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`

Old text:

```
        "backup-transfer-failed": ExitCode.PRECONDITION,
```

New text:

```
        "backup-transfer-failed": ExitCode.INTERNAL,
```

### `u45-round-1.V2_summary_slug_undeclared`

Remove backup-nothing-ran from the registry, so its raise site raises UnknownReason at the boundary

- File: `src/cratekit/core/cause.py`
- Source: `u45-round-1.json`, row `V2_summary_slug_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5490 against a baseline of 5490
- Kills: 4 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_an_outcome_with_no_portions_refuses_rather_than_raising`
  - `tests/test_backup_cli.py::test_two_portions_refused_for_different_reasons_name_both`
  - `tests/test_reserved_causes.py::test_pinned_populations_derive_totals_and_key_by_module`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        "backup-nothing-ran": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u44-author.D2_reason_slug_removed`

Remove source-missing from the closed reason registry, so the shell's own refusal cannot be built

- File: `src/cratekit/core/cause.py`
- Source: `u44-author.json`, row `D2_reason_slug_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5401 against a baseline of 5401
- Kills: 7 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_empty_recording_and_an_unknown_job_refuse_from_the_vocabulary`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_reserved_causes.py::test_the_at_risk_population_is_recomputed_from_the_tree_and_pinned`

Old text:

```
        "source-missing": ExitCode.PRECONDITION,
```

New text:

```
(empty)
```

### `u43-author-light.R2_undeclared_refusal_slug`

setbuild-anchor-not-indexed leaves cause.REASONS, so refuse raises UnknownReason at the boundary instead of refusing

- File: `src/cratekit/core/cause.py`
- Source: `u43-author-light.json`, row `R2_undeclared_refusal_slug`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_review_queue.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_install.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5344 against a baseline of 5344
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

### `u27-reports-round-1.R2_governed_tree_code`

Move the governed-tree refusal off the library-prerequisite code

- File: `src/cratekit/core/cause.py`
- Source: `u27-reports-round-1.json`, row `R2_governed_tree_code`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_labels.py`, `tests/modules/test_outbound.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/test_adoption.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_incremental_sync.py`, `tests/test_jobs.py`, `tests/test_match_states.py`, `tests/test_metadata_policy.py`, `tests/test_pacing.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_reserved_causes.py`, `tests/test_restore.py`, `tests/test_review_queue.py`, `tests/test_snapshot.py`, `tests/test_tombstones.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 5087 against a baseline of 5087
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
        "governed-tree-absent": ExitCode.LIBRARY_PREREQUISITE,
```

New text:

```
        "governed-tree-absent": ExitCode.PRECONDITION,
```

### `u155.T12_sources_type`

_sources: take any value as the sources, a bare string read letter by letter

- File: `src/cratekit/core/taxonomy_build.py`
- Source: `u155.json`, row `T12_sources_type`
- Moved: Anchored where u299-replay-after-10.json replayed it: the same text, now in src/cratekit/core/taxonomy_build.py, was in src/cratekit/core/taxonomy.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_collection_xml.py`, `tests/intake/test_pipeline.py`, `tests/modules/test_reports.py`, `tests/modules/test_reports_engines.py`, `tests/modules/test_tools.py`, `tests/test_active_taxonomy.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_catalogue_searcher.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_placement.py`, `tests/test_foreign_tree.py`, `tests/test_genre_favorites.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_genre_retag.py`, `tests/test_genre_sub.py`, `tests/test_inbox_analyzed.py`, `tests/test_inbox_rotate.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`, `tests/test_label_genre_gate.py`, `tests/test_landing_labels.py`, `tests/test_metadata_policy.py`, `tests/test_no_beatgrid_ever.py`, `tests/test_organize.py`, `tests/test_published_genre.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_report_genres.py`, `tests/test_reports_cli.py`, `tests/test_routing_parity.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_skills_lint.py`, `tests/test_sync_pair.py`, `tests/test_tag_remap.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tagging_engine.py`, `tests/test_taxonomy.py`, `tests/test_taxonomy_upgrade.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_vocabulary.py`, `tests/test_xml_splice_golden.py`
- Collected: 6713 against a baseline of 6713
- Kills: 2 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[Rominimal]`
  - `tests/test_genre_sub.py::test_sources_must_be_a_non_empty_list_of_words[sources2]`

Old text:

```
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        return ()
    return tuple(raw)
```

New text:

```
    return tuple(raw or ())
```

### `r431-b.B4_the_engine_never_asks`

standing_tombstone asks under the companion kind for nothing, which is the defect the unit closes

- File: `src/cratekit/acquire/match.py`
- Source: `r431-b.json`, row `B4_the_engine_never_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1192 against a baseline of 1192
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

### `r431-b.B7_the_engine_asks_under_the_tombstones_kind`

The engine's copy of the companion kind drifts onto the tombstone's own

- File: `src/cratekit/acquire/match_identity.py`
- Source: `r431-b.json`, row `B7_the_engine_asks_under_the_tombstones_kind`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_identity.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1192 against a baseline of 1192
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

### `r664.E4_title_not_split`

Skip split_title on the chosen title, so a version stays inside the recording token

- File: `src/cratekit/acquire/match_library.py`
- Source: `r664.json`, row `E4_title_not_split`
- Moved: Anchored where u305-replay-after.json replayed it: the same text, now in src/cratekit/acquire/match_library.py, was in src/cratekit/acquire/match.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_pipeline.py`, `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_listdoc.py`, `tests/test_match_states.py`
- Collected: 1192 against a baseline of 1192
- Kills: 106 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_an_intake_job_that_owns_a_row_by_isrc_retires_the_question_an_earlier_job_asked`
  - `tests/intake/test_workers.py::test_an_offered_track_is_a_review_item_asked_once_however_often_it_is_redone`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - ... and 91 more, see the JSON sidecar

Old text:

```
    title, version = split_title(spelled)

```

New text:

```
    title, version = spelled, ""

```

### `r118-a.A2_enoent_refuses_too`

A fresh installation with no index refuses instead of answering nothing recorded, so the product cannot be set up

- File: `src/cratekit/core/secrets.py`
- Source: `r118-a.json`, row `A2_enoent_refuses_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_recognition.py`, `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_adapter_contract.py`, `tests/test_config.py`, `tests/test_doctor.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 1591 against a baseline of 1591
- Kills: 169 (killed)
- Killed:
  - `tests/intake/test_recognition.py::test_the_bound_identifier_resolves_its_seams_at_call_time`
  - `tests/intake/test_recognition.py::test_the_keychain_credentials_are_read_by_name_and_a_missing_one_is_credential_missing`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-credentials]`
  - `tests/intake/test_recognition.py::test_the_paid_path_will_not_run_without_the_section_and_the_gate_runs_first[no-section]`
  - `tests/intake/test_recognition.py::test_the_seam_binds_this_identifier_when_none_is_injected`
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/intake/test_workers.py::test_a_missing_recording_is_refused_by_name_and_a_tilde_is_expanded_before_the_look`
  - `tests/intake/test_workers.py::test_a_recording_over_the_parts_ceiling_is_refused_at_the_queue_and_queues_nothing`
  - `tests/intake/test_workers.py::test_a_repeated_recording_in_one_set_is_one_item_per_play_and_one_per_fold`
  - `tests/intake/test_workers.py::test_a_second_identify_over_the_same_recording_makes_zero_transport_calls`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_nobody_recognised_is_an_honest_zero_that_says_what_it_cost`
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - ... and 154 more, see the JSON sidecar

Old text:

```
    except FileNotFoundError:
        return frozenset()
    except OSError as exc:
```

New text:

```
    except OSError as exc:
```

### `u298.H16_reported_extra_under_progress`

reported: a verb's own detail is dropped from progress

- File: `src/cratekit/core/jobs.py`
- Source: `u298.json`, row `H16_reported_extra_under_progress`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_ahead.py`, `tests/test_analysis_workers.py`, `tests/test_genre_favorites_adoption.py`, `tests/test_intake_missing.py`, `tests/test_label_genre.py`, `tests/test_label_judge.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_refused.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_vocals_cli.py`
- Collected: 1390 against a baseline of 1390
- Kills: 121 (killed)
- Killed:
  - `tests/intake/test_set_fetch.py::test_a_mix_url_runs_the_ordinary_set_pipeline_over_the_fetched_file`
  - `tests/intake/test_set_progress.py::test_json_output_carries_no_progress_and_stays_one_document`
  - `tests/intake/test_workers.py::test_a_playlist_job_runs_pending_to_done_through_the_resume_path`
  - `tests/intake/test_workers.py::test_a_resolution_with_nothing_missing_names_no_next_command`
  - `tests/intake/test_workers.py::test_a_set_identified_over_incomplete_coverage_queues_with_a_warning_and_freezes_the_gap`
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`
  - `tests/intake/test_workers.py::test_favorites_lists_the_hearts_resolves_each_and_rereads_the_reasons_on_every_resume`
  - `tests/intake/test_workers.py::test_identify_and_a_set_job_report_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_identify_then_set_pays_for_recognition_once_and_the_job_says_it_cost_nothing`
  - `tests/intake/test_workers.py::test_queueing_a_set_identifies_it_and_gives_the_driver_one_item_per_track`
  - `tests/intake/test_workers.py::test_queueing_and_resolving_favorites_name_the_job_each_count_its_reasons_and_the_next_command`
  - `tests/intake/test_workers.py::test_set_and_identify_write_the_same_tracklist_naming_every_row_in_order`
  - `tests/intake/test_workers.py::test_the_tracklist_is_a_list_the_match_verb_reads_back_row_for_row`
  - `tests/test_adopt_move.py::test_a_failure_after_the_add_leaves_the_track_in_both_and_a_resume_finishes`
  - ... and 106 more, see the JSON sidecar

Old text:

```
    if extra:
        counted.update(extra)
```

New text:

```
(empty)
```

### `r290-author.J3_closed_branch_removed`

Drop the closed and carrying a cause branch, so a half failed or cancelled job is reported, which is R-225 in every verb at once

- File: `src/cratekit/core/jobs.py`
- Source: `r290-author.json`, row `J3_closed_branch_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_fetch.py`, `tests/intake/test_workers.py`, `tests/test_acquire_cli.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_acquire_workers.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_backup_cli.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_handlers.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_job_outcome.py`, `tests/test_job_resume.py`, `tests/test_job_seam.py`, `tests/test_jobs.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_landing.py`, `tests/test_master_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_tag_workers.py`, `tests/test_vocals_cli.py`
- Collected: 2522 against a baseline of 2522
- Kills: 111 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_failure_mid_set_fails_that_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_network_failure_still_fails`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[deleted]`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_interrupted_job_exits_with_its_own_cause_and_not_ok`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_nested_file_deleted_after_the_queue_refuses_that_item_only`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - `tests/test_analysis_workers.py::test_a_taken_target_name_fails_the_item_and_keeps_the_written_head_in_the_title`
  - `tests/test_analysis_workers.py::test_an_interrupt_after_a_renamed_items_report_is_staged_resumes_by_the_printed_command`
  - `tests/test_analysis_workers.py::test_an_interrupted_restamp_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - ... and 96 more, see the JSON sidecar

Old text:

```
    if not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

New text:

```
    if False and not job.is_open() and job.cause is not None:
        if job.state is JobState.CANCELLED:
```

### `r382.M16_parser_moved_lowercase`

The moved parser keeps a bare identifier's case, checking the move kept its tests

- File: `src/cratekit/label/catalogue.py`
- Source: `r382.json`, row `M16_parser_moved_lowercase`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 804 against a baseline of 804
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_url_a_share_link_and_a_bare_id_all_name_the_playlist[bare-upper]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`

Old text:

```
    if _UUID.fullmatch(text):
        return text.lower()
```

New text:

```
    if _UUID.fullmatch(text):
        return text
```

### `r504-a.A10_block_listed`

The report block carries the declared count where the listed count belongs

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A10_block_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 804 against a baseline of 804
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_playlist_listing_carries_the_shortfall_beside_its_rows`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        return {"declared": self.declared, "listed": self.listed, "withheld": self.withheld}
```

New text:

```
        return {"declared": self.declared, "listed": self.declared, "withheld": self.withheld}
```

### `r504-a.A8_withheld_sign`

The seam subtracts the wrong way round, so the withheld count is negative

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A8_withheld_sign`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 804 against a baseline of 804
- Kills: 15 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_playlist_listing_carries_the_shortfall_beside_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        return self.declared - self.listed
```

New text:

```
        return self.listed - self.declared
```

### `r504-a.A9_summary_reworded`

The seam's one spelling of the three numbers is reworded

- File: `src/cratekit/label/catalogue.py`
- Source: `r504-a.json`, row `A9_summary_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 804 against a baseline of 804
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_a_listing_short_of_the_declared_count_raises_the_shortfall_with_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_a_release_listed_short_of_its_count_carries_the_shortfall_and_its_rows`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_workers.py::test_a_harvest_over_a_short_playlist_offers_what_it_read_and_warns`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            f"{self.withheld} withheld by the provider"
```

New text:

```
            f"{self.withheld} held back by the provider"
```

### `r431-b.B9_the_freeze_drops_the_field`

The intake freeze stops carrying several_artists, so the worker resolves from a track that never looked

- File: `src/cratekit/intake/cli.py`
- Source: `r431-b.json`, row `B9_the_freeze_drops_the_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_queueing_a_playlist_lists_it_through_the_catalogue_and_keys_items_by_provider_id`
  - `tests/test_intake_missing.py::test_a_billed_guest_survives_the_freeze_the_worker_resolves_from`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`

Old text:

```
        "several_artists": row.several_artists,
```

New text:

```
(empty)
```

### `r504-b.B1_verb_drops_short`

intake playlist favorites lists the hearts and throws the shortfall away

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B1_verb_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
            tracks, short = list_favorites(found)
```

New text:

```
            tracks, short = list_favorites(found)[0], None
```

### `r504-b.B4_no_progress_block`

The verb carries no shortfall block under progress

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B4_no_progress_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
        extra = {"shortfall": short.block()} if short is not None else {}
```

New text:

```
        extra = {}
```

### `r504-b.B5_noop_silent`

Every heart withheld is the quiet no-op again, with no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B5_noop_silent`
- Moved: Anchored where u325-replay-after.json replayed it: Same no-tracks return in intake_playlist; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
            )
```

### `r504-b.B6_warning_reworded`

The warning names no numbers

- File: `src/cratekit/intake/cli.py`
- Source: `r504-b.json`, row `B6_warning_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`

Old text:

```
            f"the account's hearts listed short: {short.summary()}. The provider "
```

New text:

```
            f"the account's hearts listed short. The provider "
```

### `u103-b.C8_set_no_op_carries_warnings`

Drop the warnings from intake set's nothing identified envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u103-b.json`, row `C8_set_no_op_carries_warnings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/test_acquire_fallback.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 595 against a baseline of 595
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
```

New text:

```
                outcome=Outcome.NO_OP,
            )
```

### `u52-item-derivation.A1_acquires_early_return_gone`

R-140: an offering source writes the intake row, registers the artifact and moves the watermark over releases nobody accepted

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A1_acquires_early_return_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 211 against a baseline of 211
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_an_offering_run_leaves_the_source_watermark_unset`
  - `tests/test_incremental_sync.py::test_an_offering_source_writes_no_intake_file`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if False:
```

### `u52-item-derivation.A2_acquires_default_false`

MUTATE THE COEFFICIENT: flip the getattr default, so every source written before the attribute existed stops recording what it acquired

- File: `src/cratekit/sync/run.py`
- Source: `u52-item-derivation.json`, row `A2_acquires_default_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`
- Collected: 211 against a baseline of 211
- Kills: 6 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`
  - `tests/test_incremental_sync.py::test_a_watermark_does_not_empty_the_scope_of_unowned_items`
  - `tests/test_incremental_sync.py::test_an_acquiring_source_still_writes_the_intake_file_and_advances`
  - `tests/test_incremental_sync.py::test_one_run_records_only_the_acquiring_source_of_a_mixed_pair`
  - `tests/test_incremental_sync.py::test_one_source_failing_does_not_block_the_other`
  - `tests/test_incremental_sync.py::test_two_sources_in_one_run_share_one_importable_file`

Old text:

```
        if not getattr(source, "acquires", True):
```

New text:

```
        if not getattr(source, "acquires", False):
```

### `r704-a.R1_increment_ignores_the_flag`

the increment never takes the rate limited branch, every lookup failure is permanent as before R-704

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R1_increment_ignores_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
            if exc.rate_limited:
```

New text:

```
            if False:
```

### `r704-a.R2_rate_limit_not_retryable`

the rate limited refusal says resume and records the item permanent, so the job verdict and jobs.retry still refuse

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R2_rate_limit_not_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    retryable=True,
                    origin=("sync.run",),
```

New text:

```
                    retryable=False,
                    origin=("sync.run",),
```

### `r704-a.R3_remedy_retry_later`

the rate limited refusal names retry later rather than resuming the job

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R3_remedy_retry_later`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    remedy=Remedy.RESUME_JOB,
```

New text:

```
                    remedy=Remedy.RETRY_LATER,
```

### `r704-a.R4_detail_unmarked`

the refusal's detail no longer says rate limited, so a machine reader cannot tell it from an outage

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R4_detail_unmarked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    detail={"source_id": source.id, "rate_limited": True},
```

New text:

```
                    detail={"source_id": source.id},
```

### `r704-a.R5_flag_not_stored`

LookupFailure drops the flag it was handed

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R5_flag_not_stored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_labels.py::test_a_rate_limit_is_recognized_through_the_errors_it_was_declared_from`
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
        self.rate_limited = rate_limited
```

New text:

```
        self.rate_limited = False
```

### `r704-a.R6_sentence_reworded`

the refusal no longer says the provider rate limited the lookup

- File: `src/cratekit/sync/run.py`
- Source: `r704-a.json`, row `R6_sentence_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_lookup_failure_is_permanent_unless_the_source_says_rate_limited`

Old text:

```
                    f"the provider rate limited a lookup {source.id} needed "
```

New text:

```
                    f"the provider throttled a lookup {source.id} needed "
```

### `r263.W1_no_unrecorded_state`

status_rows ignores the declared no_cursor reason, so every absent record reads as never

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W1_no_unrecorded_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_doctor_prints_the_labels_row_it_is_given`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
        reason = no_cursor.get(source_id)
```

New text:

```
        reason = None
```

### `r263.W2_state_word`

A cursorless source is reported with state never, detail unchanged

- File: `src/cratekit/sync/watermarks.py`
- Source: `r263.json`, row `W2_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 569 against a baseline of 569
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_clean_labels_sweep_is_not_reported_as_never_having_run`
  - `tests/test_incremental_sync.py::test_a_stale_cursor_on_a_source_that_records_none_is_not_a_live_completion`
  - `tests/test_incremental_sync.py::test_favorites_is_not_reported_as_never_having_run`

Old text:

```
"state": "unrecorded"
```

New text:

```
"state": "never"
```

### `r504-a.A11_boundary_refuses`

The verb boundary no longer catches the shortfall, so it is refused as an unreadable listing

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A11_boundary_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 0 against a baseline of 551
- Kills: 0 (collect-error)
- Note: collection changed: 0 collected against a baseline of 551. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Collection errors: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`

Old text:

```
    except catalogue.HeartsShortfall as short:
        return list(short.rows), short

```

New text:

```
(empty)
```

### `r504-a.A12_boundary_drops_short`

The verb boundary keeps the rows and drops the shortfall, passing the short listing off as the account

- File: `src/cratekit/label/cli.py`
- Source: `r504-a.json`, row `A12_boundary_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_labels.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 551 against a baseline of 551
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_intake_playlist_favorites_lists_what_came_back_and_names_the_shortfall`
  - `tests/test_label_tidal_catalogue.py::test_the_verb_boundary_keeps_the_rows_and_hands_back_the_shortfall`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        return list(short.rows), short
```

New text:

```
        return list(short.rows), None
```

### `u309.U5_reserve_written`

A reservation's new identifier is never written to the ledger

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u309.json`, row `U5_reserve_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_sync_twins.py`, `tests/test_export_set.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_edits.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 514 against a baseline of 514
- Kills: 136 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_track_settled_twice_on_a_set_playlist_is_recorded_once`
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_tidal_list_documents_own_identifiers_are_used_without_a_search`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - ... and 121 more, see the JSON sidecar

Old text:

```
        held[key] = record(remote_id)
        ledger._write(cfg, document)
        return remote_id, True
```

New text:

```
        held[key] = record(remote_id)
        return remote_id, True
```

### `r835-a.L1_load_carries_the_label_map`

ledger._load: the label map is dropped on load, so any other write to the ledger forgets every label's folder and year playlists

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L1_load_carries_the_label_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 356 against a baseline of 356
- Kills: 28 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_batch_of_another_label_marks_nothing_and_reads_no_account`
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`
  - `tests/test_label_playlists.py::test_a_ledger_written_by_another_verb_keeps_the_label_shape`
  - `tests/test_label_playlists.py::test_a_mark_the_record_cannot_take_names_what_it_took_before`
  - `tests/test_label_playlists.py::test_a_mark_with_no_landed_file_refuses_before_anything`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_recorded_year_deleted_on_the_account_is_left_alone_not_refused`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_mark_says_each_year_is_already_marked`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - ... and 13 more, see the JSON sidecar

Old text:

```
        "labels": {str(key): _label_document(path, value) for key, value in labels.items()},
```

New text:

```
        "labels": {},
```

### `u27-r80-write-probe-replacement.W8_read_probe_flags`

Make the read probe write capable, the shape the reports allowlist forbids

- File: `src/cratekit/core/cause.py`
- Source: `u27-r80-write-probe-replacement.json`, row `W8_read_probe_flags`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`
- Collected: 358 against a baseline of 358
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_the_allowlist_admits_no_writer_this_guard_cannot_name`

Old text:

```
        handle = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
```

New text:

```
        handle = os.open(path, os.O_RDWR | os.O_NONBLOCK)
```

### `u45-round-1.V3_marker_restored`

Put planned_in back, so the verb reads as unlanded and every conformance property stops arming against it

- File: `src/cratekit/cli/registry.py`
- Source: `u45-round-1.json`, row `V3_marker_restored`
- Moved: Anchored where u303-replay-merged6.json replayed it: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on backup.run, above its landed comment, as before
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4315 against a baseline of 4319
- Kills: 49 (collect-error)
- Note: collection changed: 4315 collected against a baseline of 4319. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_job_carries_one_item_per_declared_portion_and_a_bound_worker`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[cancelled]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[failed]`
  - `tests/test_backup_cli.py::test_a_backup_that_is_over_does_not_stand_in_for_a_new_one[succeeded]`
  - `tests/test_backup_cli.py::test_a_backup_to_a_destination_nobody_is_backing_up_to_is_its_own_job`
  - `tests/test_backup_cli.py::test_a_defect_in_rebuilding_a_configuration_is_not_reported_as_a_queued_backup`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_job_in_which_nothing_ran_never_reports_success`
  - `tests/test_backup_cli.py::test_a_job_queued_before_the_worker_existed_refuses_rather_than_succeeding`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`
  - `tests/test_backup_cli.py::test_a_parked_rehearsal_is_still_blocked_after_the_rehearsal_word_is_added`
  - `tests/test_backup_cli.py::test_a_payload_key_this_build_does_not_read_does_not_make_a_stranger`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - ... and 34 more, see the JSON sidecar

Old text:

```
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        # Landed (U45).
```

New text:

```
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        planned_in="U35",
        # Landed (U45).
```

### `u45-round-1.V5_module_toggle_dropped`

Drop the module toggle, so the verb is offered on a slim install that has no backup module

- File: `src/cratekit/cli/registry.py`
- Source: `u45-round-1.json`, row `V5_module_toggle_dropped`
- Moved: Anchored where u303-replay-merged6.json replayed it: U303 laid the registry out a keyword run per line and shortened its comments; backup.run's module toggle is the same value, dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_acquire_cli.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_master_cli.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4318 against a baseline of 4319
- Kills: 6 (collect-error)
- Note: collection changed: 4318 collected against a baseline of 4319. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
- Killed:
  - `tests/test_backup_cli.py::test_the_verb_is_declared_landed_and_names_this_module`
  - `tests/test_backup_cli.py::test_the_verb_is_offered_on_the_full_profile_and_withheld_on_the_slim_one`
  - `tests/test_cli_contract.py::test_every_declared_module_toggle_is_used_by_at_least_one_verb`
  - `tests/test_cli_contract.py::test_every_feature_row_maps_to_a_verb_at_its_stated_disposition`
  - `tests/test_cli_contract.py::test_every_live_toggle_is_driven_by_the_toggle_test_below`
  - `tests/test_doctor.py::test_a_binary_no_enabled_verb_needs_is_a_note_rather_than_a_failure`

Old text:

```
source_scripts=("backup.sh",), module_id="backup",
```

New text:

```
source_scripts=("backup.sh",),
```

### `u43-author-light.R1_marker_restored`

The planned_in marker is put back on the setbuild entry, which withdraws the verb from every conformance property that only drives landed entries

- File: `src/cratekit/cli/registry.py`
- Source: `u43-author-light.json`, row `R1_marker_restored`
- Moved: Anchored where u303-replay-merged6.json replayed it: U303 laid the registry out a keyword run per line and shortened its comments; the planned marker is put back on setbuild, above its landed comment, as before
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_cutover_parity.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_genre_retag.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_reports_cli.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_setbuilder_cli.py`, `tests/test_write_session.py`
- Collected: 4145 against a baseline of 4149
- Kills: 33 (collect-error)
- Note: collection changed: 4145 collected against a baseline of 4149. A file that fails to collect takes its tests with it and the run still looks green, so this is not a zero.
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

### `u27-reports-round-1.R1_delete_review_precondition`

Stop delete.review declaring the Trash check as a precondition

- File: `src/cratekit/cli/registry.py`
- Source: `u27-reports-round-1.json`, row `R1_delete_review_precondition`
- Moved: Anchored where u303-replay-merged6.json replayed it: U303 laid the registry out a keyword run per line and shortened its comments; delete.review's checks are the same tuple, library.trash dropped the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/modules/test_tools.py`, `tests/test_adoption.py`, `tests/test_analysis.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_doctor.py`, `tests/test_jobs.py`, `tests/test_layering.py`, `tests/test_match_states.py`, `tests/test_packaging.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 3856 against a baseline of 3856
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_trash_probe_the_operating_system_refuses_is_a_failure_with_the_right_act`
  - `tests/test_doctor.py::test_a_volume_with_no_usable_trash_refuses_because_a_verb_depends_on_it`

Old text:

```
            "library.mounted", "library.identity", "library.trash", "rekordbox.closed",
```

New text:

```
            "library.mounted", "library.identity", "rekordbox.closed",
```

### `u27-reports-round-2.S5b_engine_default_drift`

Drift the engine's own copy of the handler key away from the registry's

- File: `src/cratekit/modules/reports/duplicates.py`
- Source: `u27-reports-round-2.json`, row `S5b_engine_default_drift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports.py`, `tests/test_reports_cli.py`
- Collected: 382 against a baseline of 382
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_reports.py::test_every_item_carries_the_handler_key_the_registry_declares`
  - `tests/modules/test_reports.py::test_the_declared_handler_key_is_the_one_the_registry_carries`
  - `tests/test_reports_cli.py::test_the_two_copies_of_the_duplicate_handler_key_cannot_drift`

Old text:

```
HANDLER_KEY = "audit.duplicates"
```

New text:

```
HANDLER_KEY = "duplicates.audit"
```

### `u27-reports-round-1.C1_tree_absent_refusal`

Drop the refusal for a governed tree the export does not hold, so every entry reports uncovered

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C1_tree_absent_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_the_export_does_not_hold_refuses_rather_than_reporting_everything`

Old text:

```
    if not view.has_folder(tree.display):
        raise _refuse_absent(tree)

```

New text:

```
(empty)
```

### `u27-reports-round-1.C2_tree_anchored_at_zero`

Anchor the governed-path filter at position zero, the shape that reported nothing for a nested tree

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C2_tree_anchored_at_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_inside_another_folder_is_still_the_governed_tree`

Old text:

```
        playlist.path for playlist in view.playlists if wanted in playlist.path[:-1]
```

New text:

```
        playlist.path for playlist in view.playlists if playlist.path[:1] == (wanted,)
```

### `u27-reports-round-1.C4_placement_count`

Keep only the first placement per track, so a track filed twice reports one

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-1.json`, row `C4_placement_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_covered_track_names_every_path_under_the_tree_that_holds_it`

Old text:

```
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
            held.setdefault(track_id, [playlist.path])
```

### `u27-reports-round-2.C3_uncovered_order`

Round 1 zero, re-run against the replacement guard: drop the deterministic order

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-2.json`, row `C3_uncovered_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_uncovered_list_is_ordered_BY_ARTIST_AND_NOT_BY_THE_WALK`
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
        uncovered=tuple(sorted(uncovered, key=_by_name)),
```

New text:

```
        uncovered=tuple(uncovered),
```

### `u27-reports-round-2.C3b_tie_break`

Sort on artist and name alone, leaving the tie to the walk

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-2.json`, row `C3b_tie_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_two_entries_sharing_an_artist_and_a_name_still_hold_an_order`

Old text:

```
    return (placement.entry.artist, placement.entry.name, placement.entry.track_id)
```

New text:

```
    return (placement.entry.artist, placement.entry.name, "")
```

### `u27-reports-round-3-fixes.F6_folder_count_overwrite`

Count a playlist's raw length again, so folder rows stop reconciling with placements

- File: `src/cratekit/modules/reports/coverage.py`
- Source: `u27-reports-round-3-fixes.json`, row `F6_folder_count_overwrite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_count_never_exceeds_what_the_collection_can_account_for`
  - `tests/modules/test_reports_engines.py::test_two_playlists_sharing_a_display_path_add_up_rather_than_overwrite`

Old text:

```
        counts.setdefault(playlist.path, 0)
        for track_id in playlist.track_ids:
            if track_id not in known:
                continue
            counts[playlist.path] += 1
            held.setdefault(track_id, []).append(playlist.path)
```

New text:

```
        counts[playlist.path] = len(playlist.track_ids)
        for track_id in playlist.track_ids:
            held.setdefault(track_id, []).append(playlist.path)
```

### `u27-reports-round-1.L1_distinct_tracks`

Sum the sub-playlists instead of counting distinct tracks, the double count the docstring names

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L1_distinct_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_genre_counts_distinct_tracks_rather_than_summing_its_playlists`

Old text:

```
                tracks=len(tracks),
```

New text:

```
                tracks=playlists and sum(len(p.track_ids) for p in view.playlists if p.path[: len(folder)] == folder and len(p.path) > len(folder)),
```

### `u27-reports-round-1.L3_empty_tempo_is_zero`

Report an unreadable library as a tempo range of zero rather than as unknown

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L3_empty_tempo_is_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_library_with_no_readable_head_reports_none_rather_than_zero`

Old text:

```
    if not found:
        return TempoSpread(readable=0, unreadable=unreadable)

```

New text:

```
    if not found:
        return TempoSpread(
            readable=0, unreadable=unreadable, lowest=0.0, highest=0.0, median=0.0
        )

```

### `u27-reports-round-1.L4_median_even`

Take the upper middle instead of averaging the pair on an even population

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L4_median_even`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tempo_median_over_an_even_population_averages_the_middle_pair`

Old text:

```
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2

```

New text:

```
    return ordered[middle]

```

### `u27-reports-round-1.L5_unused_buckets`

Report no unused buckets at all

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L5_unused_buckets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_declared_bucket_with_no_folder_is_a_gap`

Old text:

```
            unused_buckets=tuple(sorted(declared_ids - present_ids)),
```

New text:

```
            unused_buckets=(),
```

### `u27-reports-round-1.L6_entries_in_no_playlist`

Count every entry as in no playlist

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L6_entries_in_no_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_the_gaps_count_entries_with_no_head_and_entries_in_no_playlist`

Old text:

```
            entries_in_no_playlist=sum(1 for entry in view.entries if not entry.playlists),
```

New text:

```
            entries_in_no_playlist=len(view.entries),
```

### `u27-reports-round-1.L7_shape_governed_filter`

Measure the tree shape over every folder in the export rather than the governed tree

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-1.json`, row `L7_shape_governed_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_taxonomy_whose_tree_this_library_does_not_use_reports_no_genres`
  - `tests/modules/test_reports_engines.py::test_the_shape_measures_the_governed_tree_from_its_own_node`

Old text:

```
    governed_folders = [
        path for path in view.folders if tree_display == path[-1] or tree_display in path[:-1]
    ]

```

New text:

```
    governed_folders = list(view.folders)

```

### `u27-reports-round-2.L2_genre_parent`

Round 1 zero, re-run against the replacement guards: loosen the genre filter

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-2.json`, row `L2_genre_parent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_folder_below_a_genre_is_not_itself_a_genre`
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
        if len(folder) < 2 or folder[-2] != tree_display:
```

New text:

```
        if len(folder) < 2 or tree_display not in folder:
```

### `u27-reports-round-3-fixes.F2_depth_origin`

Measure the tree depth from the export root again rather than from the tree's own node

- File: `src/cratekit/modules/reports/library.py`
- Source: `u27-reports-round-3-fixes.json`, row `F2_depth_origin`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tree_nested_under_another_folder_yields_no_genre_from_that_folder`

Old text:

```
    try:
        return len(path) - path.index(tree_display)
    except ValueError:  # pragma: no cover - callers filter to governed paths
        return 0
```

New text:

```
    return len(path)
```

### `u311.D3_tempo_never_read`

The library report reads a field the name head never carries, so no track has a tempo

- File: `src/cratekit/modules/reports/library.py`
- Source: `u311.json`, row `D3_tempo_never_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_reports_engines.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_reports_engines.py::test_a_tempo_median_over_an_even_population_averages_the_middle_pair`
  - `tests/modules/test_reports_engines.py::test_the_tempo_spread_reads_a_marked_head_and_counts_what_it_could_not_read`

Old text:

```
    written = (parse_head(name, template=template) or {}).get("bpm")
```

New text:

```
    written = (parse_head(name, template=template) or {}).get("tempo")
```

### `r722.T8_lenient_energy_raises`

read_energy_from_file stops folding a failed read into None

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T8_lenient_energy_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2981 against a baseline of 2981
- Kills: 1 (killed)
- Killed:
  - `tests/test_adopt_energy.py::test_the_checked_reader_tells_absent_from_unreadable`

Old text:

```
    try:
        return read_energy_checked(path)
    except TagReadFailed as exc:
        log.debug("energy read failed for %s: %s", path, exc)
        return None
```

New text:

```
    return read_energy_checked(path)
```

### `r722.T9_lenient_open_raises`

The lenient reader raises when mutagen cannot open a file

- File: `src/cratekit/core/tags.py`
- Source: `r722.json`, row `T9_lenient_open_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_acquire_fallback_fetch.py`, `tests/test_adopt_apply_cli.py`, `tests/test_adopt_energy.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`, `tests/test_analysis_workers.py`, `tests/test_art.py`, `tests/test_genre_retag.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_match_states.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_paths_resolved.py`, `tests/test_queued_resume_contract.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`, `tests/test_setbuilder_cli.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_tags.py`, `tests/test_vocals_cli.py`
- Collected: 2981 against a baseline of 2981
- Kills: 305 (killed)
- Killed:
  - `tests/test_acquire_fallback_fetch.py::test_a_row_the_library_already_holds_is_not_fetched`
  - `tests/test_match_states.py::test_a_candidate_shows_a_key_that_is_true_of_every_path_it_carries`
  - `tests/test_match_states.py::test_a_candidate_whose_title_folds_to_something_keeps_its_identifier`
  - `tests/test_match_states.py::test_a_file_whose_artist_and_title_are_the_rows_swapped_is_still_offered`
  - `tests/test_match_states.py::test_a_held_emoji_row_does_not_retire_another_emoji_rows_question`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_key_question_answered_elsewhere_does_not_settle_a_version_question`
  - `tests/test_match_states.py::test_a_key_that_disagrees_outright_is_a_different_answer`
  - `tests/test_match_states.py::test_a_list_line_that_names_a_key_is_a_different_question_from_one_that_does_not`
  - `tests/test_match_states.py::test_a_lookup_hit_discovery_ranked_past_the_five_still_leads`
  - `tests/test_match_states.py::test_a_lookup_hit_pushing_a_scored_one_out_of_the_offer_says_so`
  - `tests/test_match_states.py::test_a_lossy_marker_the_template_declares_is_stripped_from_the_recording`
  - `tests/test_match_states.py::test_a_one_letter_title_is_judged_by_the_same_rule`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Acoustic]`
  - `tests/test_match_states.py::test_a_one_word_version_tail_is_asked_about_and_never_re_acquired[Demo]`
  - ... and 290 more, see the JSON sidecar

Old text:

```
        if strict:
            raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
        log.debug("tag read failed for %s: %s", path, exc)
```

New text:

```
        raise TagReadFailed(f"{type(exc).__name__}: {exc}") from exc
```

### `r221-a.E1_outcome_forgets_the_run`

The outcome records False whatever the run was, which is the state before this unit: a rehearsal and a real run render identically

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E1_outcome_forgets_the_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 5 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_outcome_itself_records_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=dry_run)
```

New text:

```
    return BackupOutcome(stamp=plan.stamp, portions=tuple(outcomes), dry_run=False)
```

### `r221-a.E2_outcome_payload_drops_the_key`

The renderer stops carrying the flag, so every reader of a rendered run is back to guessing

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r221-a.json`, row `E2_outcome_payload_drops_the_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 7 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_queued_rehearsal_resumes_to_succeeded_and_says_nothing_was_copied`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_backup_cli.py::test_the_outcome_itself_records_which_kind_of_run_it_was`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        "dry_run": outcome.dry_run,
        "portions": [
```

New text:

```
        "portions": [
```

### `r338-a.B3_capture_is_a_copy`

_plan_database: capture the share with copy and not sync, so a grid rekordbox deleted stays in the mirror for ever and the mirror stops being the share

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B3_capture_is_a_copy`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`

Old text:

```
                    rclone, "sync", str(share), f"{kept}/current",
```

New text:

```
                    rclone, "copy", str(share), f"{kept}/current",
```

### `r338-a.B8_contained_share_copied_twice`

_outside_share: read every layout as the outside one, so a share the mirror already carries is synced a second time

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-a.json`, row `B8_contained_share_copied_twice`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_portion_with_no_prune_command_carries_no_warning`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing`
  - `tests/test_analysis_store.py::test_a_contained_restore_neither_lists_nor_pulls_a_share`
  - `tests/test_analysis_store.py::test_a_contained_share_is_not_copied_twice`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_queued_real_backup_runs_every_portion_and_reports_what_it_did`
  - `tests/test_backup_cli.py::test_a_run_that_succeeded_publishes_an_age_the_session_reads_back`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`

Old text:

```
    if analysis_store.watch_roots(cfg) == (Path(cfg.library.root),):
        return None
    return analysis_store.share_root(cfg)
```

New text:

```
    if False:
        return None
    return analysis_store.share_root(cfg)
```

### `r338-b.R6_switch_ignored`

_plan_restore_inside_the_gates: ignore pull_share, so the bare metal recovery asks the remote about a share it will not pull and can be refused over it

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-b.json`, row `R6_switch_ignored`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_a_caller_that_will_not_spend_the_database_half_is_not_refused_over_the_share`

Old text:

```
        if not pull_share or analysis_store.is_watched(cfg, landing):
```

New text:

```
        if analysis_store.is_watched(cfg, landing):
```

### `r338-c.C1_absent_share_never_said`

absent_analysis_share: never warn, so an outside share that is not a directory reads as a share that was carried

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C1_absent_share_never_said`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 4 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_that_is_not_there_is_said_and_not_synced`
  - `tests/test_analysis_store.py::test_the_absent_share_warning_survives_a_refused_database_portion`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_that_is_absent_is_warned_at_queue_and_at_resume`
  - `tests/test_backup_cli.py::test_the_warnings_beside_a_reported_job_describe_that_job`

Old text:

```
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
```

New text:

```
    share = _outside_share(cfg)
    if True:
        return ()
```

### `r338-c.C2_carried_share_still_warned`

absent_analysis_share: warn whenever the share is outside the root, carried or not, which is the retired warning back under a new code

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r338-c.json`, row `C2_carried_share_still_warned`
- Moved: Anchored where u311-replay-after-d1.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 722 against a baseline of 722
- Kills: 2 (killed)
- Killed:
  - `tests/test_analysis_store.py::test_an_outside_share_rides_the_database_portion_to_its_own_mirror`
  - `tests/test_backup_cli.py::test_an_outside_analysis_share_is_carried_through_the_verb`

Old text:

```
    share = _outside_share(cfg)
    if share is None or share.is_dir():
        return ()
```

New text:

```
    share = _outside_share(cfg)
    if share is None:
        return ()
```

### `r154-b.B11_marker_name_safety`

Write a marker for any identity at all, so one carrying a separator or a dot segment is interpolated into a remote path

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r154-b.json`, row `B11_marker_name_safety`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[..]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[.hidden]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has space]`
  - `tests/modules/test_tools.py::test_an_identity_that_cannot_be_a_filename_writes_no_marker_and_says_so[has/slash]`
  - `tests/test_backup_cli.py::test_a_library_whose_identity_cannot_be_a_marker_is_told_so`

Old text:

```
    if not _MARKER_IDENTITY.fullmatch(folded):
        return None
```

New text:

```
    if False:
        return None
```

### `r222-a.A1_nothing_held`

Hold nothing, which is the finding itself: the rotation counts attempts again and a retry that succeeds purges the failed attempt's archive

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A1_nothing_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_completed_mirror_to_another_destination_settles_nothing_here`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    held = [name for name in names if keep > 0 and (floor is None or name > floor)]
```

New text:

```
    held = []
```

### `r222-a.A5_held_run_takes_no_slot`

Spend the whole keep on settled folders, so the held run is kept on top of the keep rather than as one slot of it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A5_held_run_takes_no_slot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`

Old text:

```
    slots = keep - 1 if held else keep
```

New text:

```
    slots = keep
```

### `r222-a.A8_floor_read_by_a_rehearsal`

Read the record above the rehearsal's return, so a preview fails over a file it never touches

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A8_floor_read_by_a_rehearsal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if keep < 0 or not purge:
        return out, None
    floor = _rotation_floor(cfg)
```

New text:

```
    floor = _rotation_floor(cfg)
    if keep < 0 or not purge:
        return out, None
```

### `r222-a.A9_rehearsal_purges`

EXISTING GUARD, sampled because this round re-armed its tests: a rehearsal runs the real purge

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r222-a.json`, row `A9_rehearsal_purges`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`
- Collected: 277 against a baseline of 277
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
                    purge=not dry_run,
```

New text:

```
                    purge=True,
```

### `u45-round-1.E1_rehearsal_publishes`

Let a dry run publish, so a preview records a backup age for a run that copied not one byte

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E1_rehearsal_publishes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
    if dry_run:
        publish = False
```

New text:

```
    pass
```

### `u45-round-1.E2_publish_unconditional`

Publish regardless of the flag, the same hole reached from the other side

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E2_publish_unconditional`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 7 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_dry_run_publishes_no_backup_age`
  - `tests/modules/test_tools.py::test_a_rehearsal_does_not_read_the_record_to_list_a_rotation`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_a_run_and_publishes_nothing`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - `tests/test_backup_cli.py::test_the_ages_a_rehearsal_reports_are_the_previous_real_runs_and_it_says_so`
  - `tests/test_backup_cli.py::test_the_handler_does_not_fail_an_item_over_the_age_read_back`
  - `tests/test_backup_cli.py::test_the_queued_caller_does_not_read_the_age_back_inside_the_item`

Old text:

```
        if publish:
            backup_facts.record(
```

New text:

```
        if True:
            backup_facts.record(
```

### `u45-round-1.E4_return_codes_unread`

Stop reading return codes in run_backup, which is exactly the defect its sibling run_restore shipped

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-1.json`, row `E4_return_codes_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 16 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_portion_publishes_no_age`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_capture_marks_the_snapshot_after_the_database_and_never_before_it`
  - `tests/modules/test_tools.py::test_the_prune_runs_only_after_the_mirror_succeeded`
  - `tests/test_backup_cli.py::test_a_failed_backup_item_is_re_armed_and_its_record_replaced`
  - `tests/test_backup_cli.py::test_a_failed_portion_leaves_the_job_resumable_and_redoes_only_that_portion`
  - `tests/test_backup_cli.py::test_a_failed_transfer_leaves_the_item_failed_and_job_show_names_its_argv`
  - `tests/test_backup_cli.py::test_a_narrowed_portion_whose_transfer_failed_refuses_by_that_portion`
  - `tests/test_backup_cli.py::test_a_retried_portion_keeps_the_archive_its_failed_attempt_wrote`
  - `tests/test_backup_cli.py::test_a_run_whose_every_transfer_failed_publishes_no_age_at_all`
  - `tests/test_backup_cli.py::test_asking_twice_about_a_half_failed_backup_answers_the_same_way_twice`
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`
  - `tests/test_backup_cli.py::test_the_report_is_built_from_the_outcome_and_never_from_the_plan`
  - ... and 1 more, see the JSON sidecar

Old text:

```
            if result.returncode != 0:
                failed = result
                break
```

New text:

```
            pass
```

### `u45-round-2.E5_outcome_ok_widened`

Answer ok when ANY portion is fine rather than all of them

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u45-round-2.json`, row `E5_outcome_ok_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/test_backup_cli.py::test_the_outcome_answers_not_ok_when_a_portion_failed`

Old text:

```
        return all(p.refusal is not None or p.ran for p in self.portions)
```

New text:

```
        return any(p.refusal is not None or p.ran for p in self.portions)
```

### `u48-author.E1_listing_return_code_inverted`

Existing guard: purge on a failed listing and report a good one as failed

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `E1_listing_return_code_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 17 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_keep_of_zero_is_still_a_keep_of_zero`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/modules/test_tools.py::test_a_rehearsal_whose_listing_succeeded_warns_about_nothing_and_purges_nothing`
  - `tests/modules/test_tools.py::test_a_remote_with_no_completed_mirror_on_record_is_never_purged`
  - `tests/modules/test_tools.py::test_a_retried_mirror_does_not_purge_the_archive_its_failed_attempt_wrote`
  - `tests/modules/test_tools.py::test_a_run_that_overwrote_nothing_still_keeps_the_newest_settled_archive`
  - `tests/modules/test_tools.py::test_a_wider_keep_counts_the_held_run_as_one_of_its_slots`
  - `tests/modules/test_tools.py::test_the_folder_the_last_completed_run_wrote_is_settled_not_held`
  - `tests/modules/test_tools.py::test_the_prune_keeps_the_newest_removes_the_rest_and_warns_about_nothing`
  - `tests/modules/test_tools.py::test_the_retention_the_plan_declared_is_the_retention_the_run_applies`
  - `tests/modules/test_tools.py::test_the_run_after_a_retried_one_rotates_every_attempt_out_together`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode != 0:
```

New text:

```
    result = runner(listing)
    out.append(result)
    if result.returncode == 0:
```

### `u48-author.P1_listing_classification_dropped`

A failed listing returns no warning, so the rotation stops silently again

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P1_listing_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

New text:

```
    if result.returncode != 0:
        return out, None
    if result.returncode != 0:
        return out, {
            "code": ARCHIVE_LISTING_FAILED,
```

### `u48-author.P2_purge_classification_dropped`

Failed purges return no warning, so folders survive with nothing saying so

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P2_purge_classification_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
    if unremoved:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

New text:

```
    if False:
        return out, {
            "code": ARCHIVE_PURGE_FAILED,
```

### `u48-author.P4_warning_not_recorded_on_the_portion`

run_backup reads the classification and drops it instead of carrying it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P4_warning_not_recorded_on_the_portion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`
  - `tests/modules/test_tools.py::test_a_rehearsal_reports_a_failed_listing_and_still_purges_nothing`
  - `tests/test_backup_cli.py::test_a_backup_whose_rotation_stopped_reports_it_and_is_still_a_backup`
  - `tests/test_backup_cli.py::test_a_rehearsal_reports_the_rotation_it_already_knows_it_cannot_run`

Old text:

```
                results += pruned
                if warning is not None:
                    warnings.append(warning)
                continue
```

New text:

```
                results += pruned
                continue
```

### `u48-author.P6_purge_count_not_named`

The purge message drops how many folders survived it

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P6_purge_count_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_purge_reports_how_many_folders_survived_it`

Old text:

```
                f"the archive rotation did not finish: {unremoved} dated folder(s) "
```

New text:

```
                f"the archive rotation did not finish: some dated folder(s) "
```

### `u48-author.P7_listing_message_reworded`

Reword the listing message, not append: the suite asserts with `in`

- File: `src/cratekit/modules/tools/backup.py`
- Source: `u48-author.json`, row `P7_listing_message_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_backup_cli.py`, `tests/test_process_guard.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_write_session.py`
- Collected: 690 against a baseline of 690
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_listing_reports_the_rotation_and_leaves_the_backup_successful`

Old text:

```
                f"nothing was removed and dated archive folders will accumulate "
                f"until it succeeds. The backup itself completed"
```

New text:

```
                f"nothing was removed and the rotation will stay stopped "
                f"until it succeeds. The backup itself completed"
```

### `r367.E1_a_failed_transfer_is_unread`

existing guard sample: run_restore returns results without reading return codes

- File: `src/cratekit/modules/tools/backup.py`
- Source: `r367.json`, row `E1_a_failed_transfer_is_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 15 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_failed_database_copy_still_refuses_when_the_sidecar_is_absent`
  - `tests/modules/test_tools.py::test_a_rehearsed_restore_does_not_clear_the_live_sidecars`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_removes_stale_sidecars_before_copying`
  - `tests/modules/test_tools.py::test_the_sidecars_are_cleared_before_the_mirror_too`
  - `tests/test_restore_cli.py::test_a_backup_landing_after_the_approval_does_not_change_what_is_pulled`
  - `tests/test_restore_cli.py::test_a_target_restores_the_database_into_the_directory_it_names`
  - `tests/test_restore_cli.py::test_a_target_run_rolls_no_session_back_even_by_default`
  - `tests/test_restore_cli.py::test_an_unconfirmed_absence_at_the_database_half_says_what_the_mirror_left`
  - `tests/test_restore_cli.py::test_an_unmarked_newest_snapshot_is_refused_and_a_named_one_is_pulled`
  - `tests/test_restore_cli.py::test_the_from_backup_flag_reaches_the_off_machine_half_through_the_dispatcher`
  - `tests/test_restore_cli.py::test_the_replaced_drive_flag_reaches_the_engine_and_the_digest`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`
  - `tests/test_restore_cli.py::test_what_is_offered_is_what_is_pulled_and_reported`

Old text:

```
        if result.returncode != 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

New text:

```
        if result.returncode == 0:
            raise BackupRefused(
                Refusal.RESTORE_TRANSFER_FAILED,
```

### `r367.G12_listing_results_are_discarded`

the listing runs and its names are thrown away, so every sidecar is treated as absent

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G12_listing_results_are_discarded`
- Moved: Anchored where u311-replay-after-a.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`

Old text:

```
    held = snapshot_filenames(cfg, chosen, runner=runner)
```

New text:

```
    snapshot_filenames(cfg, chosen, runner=runner)
    held = frozenset()
```

### `r367.G3_membership_is_inverted`

copy the sidecar when it is absent and skip it when it is present

- File: `src/cratekit/modules/tools/backup_snapshot.py`
- Source: `r367.json`, row `G3_membership_is_inverted`
- Moved: Anchored where u311-replay-after-a.json replayed it: the same text, now in src/cratekit/modules/tools/backup_snapshot.py, was in src/cratekit/modules/tools/backup.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_restore_cli.py`
- Collected: 282 against a baseline of 282
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_only_the_database_skips_the_absent_sidecar`
  - `tests/modules/test_tools.py::test_a_restore_from_a_snapshot_holding_the_log_copies_it`
  - `tests/modules/test_tools.py::test_restore_writes_back_the_log_and_never_the_shared_memory_index`
  - `tests/test_restore_cli.py::test_the_verb_recovers_both_halves_and_reports_them_apart`

Old text:

```
        if name not in held:
```

New text:

```
        if name in held:
```

### `r187-a.A11_no_cutoff`

match_in_index: score cutoff to zero, so a name nothing answers to reaches the whole index

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A11_no_cutoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_web_lookup_is_a_seam_that_is_absent_by_default`
  - `tests/test_setbuilder_cli.py::test_a_name_longer_than_the_owned_title_is_refused_and_not_shortened`
  - `tests/test_setbuilder_cli.py::test_a_name_nothing_answers_to_is_not_indexed_and_not_ambiguous`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[named-not-indexed]`

Old text:

```
        score_cutoff=threshold,
```

New text:

```
        score_cutoff=0,
```

### `r187-a.A6_first_of_several`

match_in_index: resolve to the first of several holding hits instead of listing them, the defect itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `r187-a.json`, row `A6_first_of_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_that_reaches_two_versions_lists_both_and_picks_neither`
  - `tests/test_setbuilder_cli.py::test_an_ambiguous_name_refuses_through_the_dispatcher_and_lists_the_paths`
  - `tests/test_setbuilder_cli.py::test_the_engine_says_ambiguous_and_never_not_in_your_library`
  - `tests/test_setbuilder_cli.py::test_the_listing_is_capped_and_says_how_many_it_reached`

Old text:

```
    if len(holding) == 1:
        return AnchorMatch(track=holding[0])
```

New text:

```
    if holding:
        return AnchorMatch(track=holding[0])
```

### `u43-author-light.E1_anchor_is_its_own_companion`

build_pool stops excluding the anchor by match key, so the best companion for a track is itself

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E1_anchor_is_its_own_companion`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 8 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
        if anchor_match and track.match == anchor_match:
            continue
```

New text:

```
        if anchor_match and track.match != anchor_match:
            pass
```

### `u43-author-light.E3_tempo_serialized_as_bpm`

as_payload spells the tempo key the way the Vorbis tag dialect does, which is one splat from handing a tempo to a tag writer and seeding a grid at half or double time (R17)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u43-author-light.json`, row `E3_tempo_serialized_as_bpm`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`
- Collected: 268 against a baseline of 268
- Kills: 4 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_structured_payload_carries_a_version`
  - `tests/test_setbuilder_cli.py::test_a_supplied_tempo_narrows_an_unowned_anchor_to_its_band`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_is_ranked_through_the_dispatcher`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`

Old text:

```
            "tempo": plan.anchor.bpm,
```

New text:

```
            "bpm": plan.anchor.bpm,
```

### `u311.C8_unreadable_number_raises`

A tag that is not a number raises instead of reading as absent

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C8_unreadable_number_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 339 against a baseline of 339
- Kills: 43 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[list]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[text]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-missing-fields]`
  - `tests/modules/test_tools.py::test_a_cache_entry_of_the_wrong_shape_costs_one_read_and_never_the_run[track-not-a-mapping]`
  - `tests/modules/test_tools.py::test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded[other-build]`
  - `tests/modules/test_tools.py::test_a_cache_from_another_build_or_with_no_template_stamp_is_discarded[unstamped]`
  - `tests/modules/test_tools.py::test_a_cache_parsed_under_another_template_is_discarded`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[bpm-124]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[energy-True]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[title-None]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[vox-value2]`
  - `tests/modules/test_tools.py::test_a_cached_track_with_the_right_names_and_wrong_types_is_re_read[voxgender-4]`
  - `tests/modules/test_tools.py::test_a_marked_lossy_title_loses_its_marker_along_with_the_head`
  - `tests/modules/test_tools.py::test_a_read_that_returned_nothing_is_never_cached_as_the_files_answer`
  - `tests/modules/test_tools.py::test_new_bytes_under_an_old_modification_time_are_re_read`
  - ... and 28 more, see the JSON sidecar

Old text:

```
    except (TypeError, ValueError):
        return None
```

New text:

```
    except TypeError:
        return None
```

### `u311.C9_anchor_comes_back`

The anchor is no longer excluded from its own pool by match key

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u311.json`, row `C9_anchor_comes_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_tools.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_one_open.py`
- Collected: 339 against a baseline of 339
- Kills: 13 (killed)
- Killed:
  - `tests/modules/test_tools.py::test_the_set_builder_produces_a_sequence_from_a_snapshot_index`
  - `tests/test_setbuilder_cli.py::test_a_cache_that_cannot_be_written_does_not_cost_the_set`
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`
  - `tests/test_setbuilder_cli.py::test_a_path_anchor_is_unchanged_by_the_unowned_form`
  - `tests/test_setbuilder_cli.py::test_every_recommendation_came_out_of_the_index`
  - `tests/test_setbuilder_cli.py::test_one_either_companion_of_an_owned_anchor_is_placed_once`
  - `tests/test_setbuilder_cli.py::test_the_anchor_is_in_the_digest_even_when_the_companions_are_identical`
  - `tests/test_setbuilder_cli.py::test_the_verb_produces_a_compatible_sequence_over_a_real_library`
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        if anchor_match and track.match == anchor_match:
```

New text:

```
        if False:
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

### `u246.S1_adapter_asked_empty`

InvocationResult: an empty set of requested keys, so every result reads as a track nobody asked for

- File: `src/cratekit/acquire/adapter.py`
- Source: `u246.json`, row `S1_adapter_asked_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_contract.py`, `tests/test_acquire_workers.py`, `tests/test_acquire_cli.py`, `tests/intake/test_pipeline.py`
- Collected: 258 against a baseline of 258
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

### `r1411.A1_agreed_order_always_stands`

the agreed order check passes every reading, so a reading in the order from before the stopped moves is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A1_agreed_order_always_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
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

### `r1411.A3_added_tracks_asked_of_the_agreed_order`

the agreed order check reads every track of the reading, so a track this write added refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A3_added_tracks_asked_of_the_agreed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1309 against a baseline of 1309
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

### `r722.S5_catch_oserror_only`

The census catches only OSError from the reader, so a failed read ends the walk

- File: `src/cratekit/adopt/scan.py`
- Source: `r722.json`, row `S5_catch_oserror_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_energy.py`, `tests/test_adopt_workers.py`, `tests/test_adoption.py`, `tests/test_adoption_hardware.py`
- Collected: 690 against a baseline of 690
- Kills: 62 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_declined_run_queues_nothing_at_all`
  - `tests/test_adopt_apply_cli.py::test_a_resume_reconciles_a_claim_a_dead_driver_left_behind`
  - `tests/test_adopt_apply_cli.py::test_an_approval_recorded_against_a_plan_that_has_since_moved_is_refused`
  - `tests/test_adopt_apply_cli.py::test_an_approved_run_queues_one_job_carrying_the_tree_and_the_digest`
  - `tests/test_adopt_apply_cli.py::test_the_approval_gate_shows_every_entry_the_digest_was_taken_over`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_energy.py::test_a_container_the_tag_library_does_not_recognise_is_unreadable`
  - `tests/test_adopt_energy.py::test_a_file_whose_tags_cannot_be_read_is_reported`
  - `tests/test_adopt_energy.py::test_a_value_that_is_not_a_number_is_reported_as_unreadable`
  - `tests/test_adopt_energy.py::test_an_unreadable_file_and_an_untagged_one_are_different_plans`
  - `tests/test_adopt_workers.py::test_a_collection_that_moved_after_approval_refuses_rather_than_applying`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_copy_edited_during_a_scan_judges_every_row_after_the_edit`
  - `tests/test_adopt_workers.py::test_a_job_queued_with_no_items_refuses_rather_than_reporting_success[adopt.apply]`
  - `tests/test_adopt_workers.py::test_a_parked_adoption_leaves_blocked_and_non_zero`
  - ... and 47 more, see the JSON sidecar

Old text:

```
    except (tags.TagReadFailed, OSError):
```

New text:

```
    except OSError:
```

### `u59.M9_column_repointed`

Point SOFT_DELETE_COLUMN at a neighbouring bookkeeping column

- File: `src/cratekit/core/rb_writer.py`
- Source: `u59.json`, row `M9_column_repointed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_collection.py`, `tests/test_adopt_workers.py`, `tests/test_cli_contract.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`, `tests/test_process_guard.py`, `tests/test_queued_resume_contract.py`, `tests/test_rb_snapshot.py`, `tests/test_rb_writer_db.py`, `tests/test_rb_writer_guard.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_cli.py`, `tests/test_snapshot.py`, `tests/test_tree_writer.py`, `tests/test_write_guard_completeness.py`, `tests/test_write_session.py`
- Collected: 2717 against a baseline of 2717
- Kills: 176 (killed)
- Killed:
  - `tests/test_adopt_apply_cli.py::test_a_library_of_tombstones_and_an_empty_one_both_census_to_nothing`
  - `tests/test_adopt_apply_cli.py::test_the_census_is_the_library_and_every_row_of_it_is_carried`
  - `tests/test_adopt_collection.py::test_a_null_location_and_a_null_genre_are_empty_strings_not_none`
  - `tests/test_adopt_collection.py::test_a_tombstone_is_carried_rather_than_dropped`
  - `tests/test_adopt_collection.py::test_every_field_comes_off_the_row_it_belongs_to`
  - `tests/test_adopt_collection.py::test_the_reader_yields_the_rows_the_database_holds`
  - `tests/test_adopt_workers.py::test_a_configured_volume_rewrite_reaches_the_census`
  - `tests/test_adopt_workers.py::test_a_plan_with_nothing_applicable_queues_nothing`
  - `tests/test_adopt_workers.py::test_a_row_removed_between_queueing_and_driving_fails_only_its_own_item[tombstoned]`
  - `tests/test_adopt_workers.py::test_an_empty_library_queues_nothing_and_says_so[True]`
  - `tests/test_deferred_routing.py::test_content_rows_reads_the_soft_delete_marker_off_the_row`
  - `tests/test_deletion.py::test_a_binding_that_cannot_say_how_many_memberships_it_holds_refuses`
  - `tests/test_deletion.py::test_a_collection_row_with_no_id_reaches_the_pass_as_unidentifiable`
  - `tests/test_deletion.py::test_a_confirmed_ambiguous_row_is_refused_at_move_time_too`
  - `tests/test_deletion.py::test_a_confirmed_file_is_trashed_and_leaves_a_tombstone`
  - ... and 161 more, see the JSON sidecar

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"
```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_synced"
```

### `u138.E1_terminal_check`

Existing guard sample: the terminal check on a person's answer

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `E1_terminal_check`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

### `u138.S11_rule_not_written`

The record's rule key is not written to the file

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S11_rule_not_written`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S12_message_names_the_portion`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S13_remedy_points_back_at_ack`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S1_session_rule_gone`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S2_any_answer_gets_the_age_rule`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
- Kills: 13 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[session.ack]`
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_person_without_a_terminal_is_still_refused_over_fresh_backups`
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S3_stale_not_refused`
- Moved: Anchored where u300-replay-after-b.json replayed it: moved by U300's split from src/cratekit/core/session.py to session_ack.py, the same refusal of a stale portion in the acknowledgment
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S6_bound_six_days`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S8_rule_not_recorded`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

- File: `src/cratekit/core/session_ack.py`
- Source: `u138.json`, row `S9_answer_not_recorded`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_ack.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_adopt_move.py`, `tests/test_adopt_workers.py`, `tests/test_analysis_store.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_cli.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_export_collection.py`, `tests/test_favorites_backfill.py`, `tests/test_genre_favorites.py`, `tests/test_inbox_refill.py`, `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_metadata_cli.py`, `tests/test_organize.py`, `tests/test_paths_resolved.py`, `tests/test_rebuild.py`, `tests/test_repair_link.py`, `tests/test_repair_rows.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_routing_workers.py`, `tests/test_session_ack_by_session.py`, `tests/test_session_cli.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_pair.py`, `tests/test_tag_rows.py`, `tests/test_tag_suggest.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 4024 against a baseline of 4024
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

### `u49-author.L4_a_malformed_holder_raises_again`

Remove the coercion guard from read_lock_holder, so a lock record with a non numeric pid escapes as a traceback rather than a typed refusal

- File: `src/cratekit/core/session_holders.py`
- Source: `u49-author.json`, row `L4_a_malformed_holder_raises_again`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_cli.py`, `tests/test_backup_cli.py`, `tests/test_cli_contract.py`, `tests/test_cutover_precheck.py`, `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_doctor.py`, `tests/test_rebuild.py`, `tests/test_restore.py`, `tests/test_restore_cli.py`, `tests/test_session_cli.py`, `tests/test_tree_writer.py`, `tests/test_write_session.py`
- Collected: 2568 against a baseline of 2568
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_lock_record_that_cannot_be_understood_refuses_by_name`

Old text:

```
    try:
        return Holder.from_json(data["holder"])
    except (TypeError, ValueError, AttributeError):
```

New text:

```
    if True:
        return Holder.from_json(data["holder"])
    if False:
```

### `u254.M07_always_append`

mark_applied: append even to a torn, absent or schema 1 ledger

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M07_always_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 85 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_ledger_damaged_since_this_process_left_it_refuses_the_next_mark`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[actor]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[content_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[entry_id]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_the_reader_would_refuse_is_never_written[tree]`
  - ... and 70 more, see the JSON sidecar

Old text:

```
            if appendable:
                config.append_durable_bytes(line, path)
```

New text:

```
            if True:
                config.append_durable_bytes(line, path)
```

### `u254.M19_already_inverted`

apply_plan: report as already applied the entries the ledger does not hold

- File: `src/cratekit/adopt/apply.py`
- Source: `u254.json`, row `M19_already_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_adoption.py`, `tests/test_adopt_workers.py`, `tests/test_intake_land_filing.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_mirror_downloads_filed_u227.py`
- Collected: 741 against a baseline of 741
- Kills: 33 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-3]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-two-4]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-1]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-2]`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[none-3]`
  - ... and 18 more, see the JSON sidecar

Old text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id in done
```

New text:

```
        entry.entry_id for entry in plan.applicable() if entry.entry_id not in done
```

### `u254.C4_append_not_append`

append_durable_bytes: open for writing at the start of the file rather than its end

- File: `src/cratekit/core/config.py`
- Source: `u254.json`, row `C4_append_not_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_apply_journal_u254.py`, `tests/test_config_test_root.py`, `tests/test_config.py`, `tests/test_adoption.py`
- Collected: 963 against a baseline of 963
- Kills: 54 (killed)
- Killed:
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_put_in_place_with_the_same_size_and_time_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_file_rewritten_in_place_at_the_same_size_is_read_again`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[1]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[2]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[3]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_kill_after_the_whole_record_landed_counts_the_mark[4]`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_does_not_parse_the_ledger_it_appends_to`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_journal_this_process_never_wrote_appends`
  - `tests/test_adopt_apply_journal_u254.py::test_a_mark_on_a_ledger_written_before_u254_keeps_every_record`
  - `tests/test_adopt_apply_journal_u254.py::test_a_re_mark_replaces_the_earlier_record_as_the_document_did`
  - `tests/test_adopt_apply_journal_u254.py::test_a_record_another_process_appended_is_kept`
  - `tests/test_adopt_apply_journal_u254.py::test_a_revert_after_a_partial_apply_restores_what_it_wrote`
  - `tests/test_adopt_apply_journal_u254.py::test_a_torn_tail_left_inside_one_clock_tick_is_still_cut`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_the_system_writes_in_pieces_still_lands_whole`
  - `tests/test_adopt_apply_journal_u254.py::test_an_append_torn_by_a_kill_resumes_with_exactly_the_marks_before_it[all-but-newline-1]`
  - ... and 39 more, see the JSON sidecar

Old text:

```
    fd = os.open(path, os.O_WRONLY | os.O_APPEND)
```

New text:

```
    fd = os.open(path, os.O_WRONLY)
```

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_sub.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_filing.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 811 against a baseline of 811
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_rominimal_track_at_energy_3_lands_in_its_band_and_in_rominimal`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

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

### `u219.A4_additions_rows`

additions: report nothing missing, so the gate shows no add and the resort queues nothing

- File: `src/cratekit/write/rebuild.py`
- Source: `u219.json`, row `A4_additions_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_resort_scope.py`, `tests/test_routing_workers.py`
- Collected: 728 against a baseline of 728
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

### `u155.W1_derivation`

derive_from_taxonomy: place no genre sub, so the rebuild and resort never write it

- File: `src/cratekit/write/rebuild.py`
- Source: `u155.json`, row `W1_derivation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_genre_favorites.py`, `tests/test_genre_sub.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 704 against a baseline of 704
- Kills: 7 (killed)
- Killed:
  - `tests/test_genre_sub.py::test_a_rominimal_track_at_energy_3_lands_in_its_band_and_in_rominimal`
  - `tests/test_genre_sub.py::test_a_rominimal_track_with_no_reading_lands_in_unsorted_and_in_rominimal`
  - `tests/test_genre_sub.py::test_route_resort_moves_the_96_puls_tracks_additively`
  - `tests/test_rebuild.py::test_a_genre_sub_is_created_once_beside_the_band_and_a_second_rebuild_plans_nothing`
  - `tests/test_routing_workers.py::test_the_database_inbox_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_export_gate_shows_a_genre_sub_beside_the_band_and_files_both`
  - `tests/test_routing_workers.py::test_the_unplaced_export_names_a_genre_sub_beside_the_band_and_files_both`

Old text:

```
        if genre is not None:
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, genre.id))
```

New text:

```
        if False:
            out.append(DeclaredPlacement(entry.location, resolution.bucket_id, genre.id))
```

### `u58-workers-and-wav.H1_run_unbound`

Drop the analyze.run binding from the handler table

- File: `src/cratekit/cli/handlers.py`
- Source: `u58-workers-and-wav.json`, row `H1_run_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_analysis_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_label_workers.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 597 against a baseline of 597
- Kills: 33 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_calibrated_level_is_written_and_routes_to_a_band`
  - `tests/test_analysis_workers.py::test_a_container_the_tag_writer_does_not_know_fails_under_the_analysis_slug`
  - `tests/test_analysis_workers.py::test_a_corrupt_calibration_reaches_the_person_as_a_remedy_not_a_defect`
  - `tests/test_analysis_workers.py::test_a_deleted_source_beside_an_unrelated_twin_is_refused_not_reported_analysed`
  - `tests/test_analysis_workers.py::test_a_detector_shaped_like_the_batch_fakes_is_accepted`
  - `tests/test_analysis_workers.py::test_a_directory_at_the_report_name_is_cleared_and_the_attempt_finishes`
  - `tests/test_analysis_workers.py::test_a_failed_tag_write_fails_the_item_and_leaves_the_name_alone`
  - `tests/test_analysis_workers.py::test_a_file_removed_between_queueing_and_drive_is_refused_by_name`
  - `tests/test_analysis_workers.py::test_a_job_the_shipped_code_left_with_no_intent_resumes_from_its_staged_report`
  - `tests/test_analysis_workers.py::test_a_keyless_track_is_a_terminal_skip_with_nothing_written`
  - `tests/test_analysis_workers.py::test_a_kill_after_an_attempt_starts_leaves_no_stale_report_to_read_as_a_twin`
  - `tests/test_analysis_workers.py::test_a_prefixed_file_is_the_resume_marker_and_is_skipped_without_a_read`
  - `tests/test_analysis_workers.py::test_a_prefixed_source_drops_a_stale_intent_too`
  - `tests/test_analysis_workers.py::test_a_refused_rename_leaves_no_intent_behind`
  - `tests/test_analysis_workers.py::test_a_resume_interrupted_in_the_same_window_is_resumed_again`
  - ... and 18 more, see the JSON sidecar

Old text:

```
    "analyze.run": "cratekit.analysis.cli:handle_run",

```

New text:

```
(empty)
```

### `u56-catalogue-searcher-and-tag-workers.R39_tag_folder_unbound`

The handler key goes back to declaring no worker, which is the state this whole unit exists to leave

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R39_tag_folder_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 343 against a baseline of 343
- Kills: 41 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_tag_workers.py::test_a_block_on_a_file_a_record_shop_declined_is_still_said`
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tag_workers.py::test_a_file_removed_between_the_queueing_and_the_drive_is_refused_by_name`
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_some_files_says_how_many_of_how_many`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_published_genre_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_a_published_word_with_no_folder_is_listed_as_unresolved`
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`
  - `tests/test_tag_workers.py::test_a_retried_job_drives_only_the_item_that_failed`
  - `tests/test_tag_workers.py::test_a_searcher_that_raises_part_way_fails_only_its_own_item`
  - ... and 26 more, see the JSON sidecar

Old text:

```
    "tag.folder": "cratekit.tagging.cli:handle",
```

New text:

```
(empty)
```

### `u56-catalogue-searcher-and-tag-workers.R40_tag_retag_unbound`

The same for the correction verb

- File: `src/cratekit/cli/handlers.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R40_tag_retag_unbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_workers.py`, `tests/test_handlers.py`, `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_outbound_workers.py`, `tests/test_tag_workers.py`
- Collected: 343 against a baseline of 343
- Kills: 21 (killed)
- Killed:
  - `tests/test_handlers.py::test_every_queued_verb_is_either_bound_or_named_as_unbound`
  - `tests/test_tag_workers.py::test_a_corrected_retag_ends_by_naming_the_reload_the_stale_row_needs`
  - `tests/test_tag_workers.py::test_a_file_gone_at_drive_time_is_refused_rather_than_reported_done`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[-read_back1-no-genre]`
  - `tests/test_tag_workers.py::test_a_genre_changed_between_the_confirm_and_the_drive_is_left_to_its_owner[Ambient-read_back0-genre-specific]`
  - `tests/test_tag_workers.py::test_a_half_corrected_retag_carries_the_reload_on_its_refusal`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`
  - `tests/test_tag_workers.py::test_a_recorded_acceptance_is_used_and_the_searcher_is_never_asked`
  - `tests/test_tag_workers.py::test_a_resume_after_a_partial_run_meets_its_gate_rather_than_going_stale`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_fails_its_item_and_the_rest_are_corrected`
  - `tests/test_tag_workers.py::test_a_retag_file_that_will_not_take_its_genre_is_named_in_the_human_answer`
  - `tests/test_tag_workers.py::test_a_retag_parses_the_active_taxonomy_once_however_many_files_it_corrects`
  - `tests/test_tag_workers.py::test_a_retag_that_corrected_nothing_does_not_send_a_person_to_rekordbox`
  - `tests/test_tag_workers.py::test_a_retag_whose_only_file_will_not_take_its_genre_names_no_reload`
  - `tests/test_tag_workers.py::test_a_retried_retag_drives_only_the_item_that_failed`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    "tag.retag": "cratekit.tagging.retag_cli:handle",
```

New text:

```
(empty)
```

### `u23-round-8-independent.A1_at_risk_always_true`

Nothing is ever at risk, so _settled_or_refused can never refuse

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A1_at_risk_always_true`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    return True

```

### `u23-round-8-independent.A2_at_risk_always_false`

Everything is at risk, so every re-run falls through to the digest

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A2_at_risk_always_false`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 6 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`
  - `tests/test_adoption.py::test_a_TAG_EDITED_IN_PLACE_is_still_accepted_because_nothing_is_at_risk`
  - `tests/test_adoption.py::test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`
  - `tests/test_adoption.py::test_the_FIRST_ADOPTION_of_a_library_hashes_NOTHING`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    return False

```

### `u23-round-8-independent.A3_at_risk_drops_the_original_clause`

A field holding this record's own original is no longer accounted for

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A3_at_risk_drops_the_original_clause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    return held in ((record.written,), (written,))

```

### `u23-round-8-independent.A4_at_risk_drops_the_record_value`

The value the record says adoption wrote no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A4_at_risk_drops_the_record_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_SECOND_TAXONOMY_accepts_because_ADOPTIONS_OWN_value_is_in_the_field`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((written,),)

```

### `u23-round-8-independent.A5_at_risk_drops_this_call`

The value THIS call is about to write no longer accounts for the field

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A5_at_risk_drops_this_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_THIRD_adoption_accepts_when_the_field_ALREADY_holds_what_it_would_write`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,),)

```

### `u23-round-8-independent.A6_at_risk_original_by_identity`

The original clause compares by object identity rather than by value

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `A6_at_risk_original_by_identity`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 2 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_CRASH_SEAM_record_with_no_digest_still_matches_its_own_file`
  - `tests/test_adoption.py::test_a_ledger_written_by_the_PATH_DIGEST_scheme_is_migrated_not_doubled`

Old text:

```
    held = current()
    if held == record.original:
        return True
    return held in ((record.written,), (written,))

```

New text:

```
    held = current()
    if held is record.original:
        return True
    return held in ((record.written,), (written,))

```

### `u23-round-8-independent.B1_settled_never_refuses`

Round 7 restored: the two converging-address shapes accept unconditionally

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `B1_settled_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    if _nothing_unrecorded_is_at_risk(record, written=written, current=current):
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):

```

New text:

```
    if True:
        return _re_addressed(
            record, identity=identity, path_text=path_text, keep_path=keep_path
        )
    if _the_bytes_agree(record, look, size_here):

```

### `u23-round-8-independent.B3_settled_bytes_clause_inverted`

The bytes acceptance fires when the bytes DISAGREE

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `B3_settled_bytes_clause_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 4 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
    if _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT
```

New text:

```
    if not _the_bytes_agree(record, look, size_here):
        # THE BYTES ARE EXACTLY WHAT ADOPTION LEFT
```

### `u23-round-8-independent.C1_shape2_bypasses_the_check`

Shape 2, both addresses agreeing, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `C1_shape2_bypasses_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 3 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_DIFFERENT_RECORDING_put_here_IN_PLACE_is_refused_not_re_stamped`
  - `tests/test_adoption.py::test_a_SAME_LENGTH_rewrite_reaches_the_DIGEST_rather_than_the_size_shortcut`
  - `tests/test_adoption.py::test_no_refusal_in_this_module_tells_the_person_to_RUN_A_VERB_THAT_IS_PLANNED`

Old text:

```
        if by_identity is by_path:
            return _settled_or_refused(
                by_identity,
                resolved,
                identity=identity,
                path_text=path_text,
                keep_path=True,
                written=written,
                look=look,
                current=current,
                size_here=size_here,
            )

```

New text:

```
        if by_identity is by_path:
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=True
            )

```

### `u23-round-8-independent.C2_shape3_bypasses_the_check`

Shape 3, one file under two names, returns re-addressed with no check at all

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `C2_shape3_bypasses_the_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_HARDLINKED_second_name_asks_the_BYTES_when_the_field_holds_a_stranger`

Old text:

```
            # a different question and the shape below is where it is asked.
            return _settled_or_refused(

```

New text:

```
            # a different question and the shape below is where it is asked.
            return _re_addressed(
                by_identity, identity=identity, path_text=path_text, keep_path=True
            )
            return _settled_or_refused(

```

### `u23-round-8-independent.D1_bytes_agree_drops_the_size_gate`

The size shortcut round 8 restored is removed again

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `D1_bytes_agree_drops_the_size_gate`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 1 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`

Old text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
        return False

```

New text:

```
(empty)
```

### `u23-round-8-independent.D2_bytes_agree_size_gate_inverted`

The size shortcut refuses on AGREEING sizes

- File: `src/cratekit/adopt/revert.py`
- Source: `u23-round-8-independent.json`, row `D2_bytes_agree_size_gate_inverted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_adoption.py`
- Collected: 615 against a baseline of 615
- Kills: 6 (killed)
- Killed:
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[both]`
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[inode-renumbered]`
  - `tests/test_adoption.py::test_a_REMOUNT_does_not_produce_a_SECOND_record[mounted-in-another-order]`
  - `tests/test_adoption.py::test_a_file_RENAMED_between_two_adoptions_is_still_one_record`
  - `tests/test_adoption.py::test_a_record_whose_SIZE_is_not_this_files_size_is_never_a_reason_to_HASH`
  - `tests/test_adoption.py::test_an_UNMOUNTED_VOLUME_does_not_let_a_COPY_take_a_LIVE_files_record`

Old text:

```
    if record.size is not None and size_here is not None and record.size != size_here:
```

New text:

```
    if record.size is not None and size_here is not None and record.size == size_here:
```

