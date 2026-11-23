# Mutation table: u312-replay-after-3

Measured by `scripts/mutate.py` on 2026-11-23 10:40 UTC, branch `HEAD` at `55e2f3b6`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 267.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 46, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `known/scratch.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r773-b.P1_proof_granted_whatever_the_export_names` | `src/cratekit/intake/imported_cli.py` | user | 2 file(s) | 128 | 6 | killed |
| `u142.S1_folder_prefix` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 13 | killed |
| `u142.S5_create_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 216 | 6 | killed |
| `u140.B6_mark_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 2 file(s) | 85 | 2 | killed |
| `r1349.E2_open_left` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1211 | 10 | killed |
| `r1349.E3_offer_unrecorded` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1211 | 47 | killed |
| `r1349.N4_open_ignored` | `src/cratekit/cli/gates.py` | user | 8 file(s) | 1211 | 15 | killed |
| `u40-author-full.D5_no_enable` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 5 | killed |
| `u40-author-full.D7_unmatched_dropped` | `src/cratekit/tagging/retag.py` | user | 1 file(s) | 50 | 3 | killed |
| `u40-author-full.F2_genre_unknown_silent` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `u59.M1_permissive_default` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 3 | killed |
| `u59.M2_refusal_removed` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `u59.M4_tombstone_resolves` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 10 | killed |
| `u59.M5_first_row_wins` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 6 | killed |
| `u59.M6_reason_reworded` | `src/cratekit/write/metadata.py` | user | 2 file(s) | 97 | 4 | killed |
| `r1372.K10_carried_read_error_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `r1372.K15_let_go_keeps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 5 | killed |
| `r1372.K2_carry_writes_nothing` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 15 | killed |
| `r1372.K3_carry_empty_steps` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 10 | killed |
| `r1372.K5_carried_under_held_plans` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 3 | killed |
| `u225.M13_unreadable_silent` | `src/cratekit/core/held_plan.py` | user | 7 file(s) | 227 | 2 | killed |
| `u232.A3_stub_raise_exec` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A4_tripwire_records` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A5_tripwire_refuses` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A7_tripwire_on_pids` | `tests/conftest.py` | maintainer | 1 file(s) | 9 | 1 | killed |
| `u232.A8_opt_in` | `tests/conftest.py` | maintainer | 2 file(s) | 55 | 4 | killed |
| `u326.R9_host_process_tripwire` | `tests/conftest.py` | maintainer | 2 file(s) | 55 | 1 | killed |
| `u232.A1_platform_stub` | `tests/conftest.py` | maintainer | 4 file(s) | 90 | 4 | killed |
| `u232.A2_pyrekordbox_stub` | `tests/conftest.py` | maintainer | 4 file(s) | 90 | 26 | killed |
| `u166.A4_no_add` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 14 | killed |
| `u166.A7_record_count` | `src/cratekit/intake/native.py` | user | 7 file(s) | 185 | 5 | killed |
| `u111-b.B1_move_names_every_table` | `src/cratekit/write/trees.py` | user | 2 file(s) | 117 | 1 | killed |
| `r777.N15_any_pass` | `src/cratekit/intake/native_plan.py` | user | 6 file(s) | 197 | 2 | killed |
| `r259.S1_scope_owned_sample` | `src/cratekit/sync/scope.py` | maintainer | 1 file(s) | 31 | 1 | killed |
| `u109-b.B3_no_cursor_reworded` | `src/cratekit/sync/sources.py` | user | 1 file(s) | 31 | 3 | killed |
| `r359.M10_claims_downloaded` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 1 | killed |
| `r359.M1_drop_field` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 3 | killed |
| `r359.M2_token` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.M3_said_silent` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.M8_drop_resolved` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 1 | killed |
| `r359.M9_drop_not_acquired` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 2 | killed |
| `r359.S1_record_on_any_state` | `src/cratekit/sync/playlists.py` | user | 2 file(s) | 146 | 6 | killed |
| `u74.A1_no_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 26 | killed |
| `u74.A2_wrong_inbound_key` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 146 | 14 | killed |
| `r361-a.A10_enum_value_respelled` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r361-a.A2_case_insensitive` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 3 | killed |
| `r361-a.D2_drop_the_placeholder` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r361-a.D3_drop_in_flight` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M11_reconcile_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M12_in_flight_source_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r382.M15_completed_duplicates` | `src/cratekit/sync/playlists.py` | maintainer | 3 file(s) | 215 | 1 | killed |
| `r382.M1_restore_source_filter` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 7 | killed |
| `r382.M2_drop_handler_key` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M3_drop_library` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M4_hearts_recorded` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M5_no_verbatim_for_pass_jobs` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r382.M6_no_parse` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M7_invalid_records_nothing` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 3 | killed |
| `r382.M8_completed_raw` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r382.M9_open_raw` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r501-d.R2_settled_is_not_imported` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 313 | 1 | killed |
| `r501-d.R3_pass_is_proof` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 313 | 1 | killed |
| `u307.R11_imported_session_ignored` | `src/cratekit/intake/imported_cli.py` | user | 2 file(s) | 128 | 1 | killed |
| `r501-c.M1_export_name_check` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `r501-c.M2_export_identity_check` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `r501-c.M3_missing_is_not_imported` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 4 | killed |
| `r501-c.M4_nothing_recorded` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `r501-d.M10_waiting_legacy` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `r501-d.M11_close_refusal_reported` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `r501-d.M13_waiting_needs_export` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `r501-d.M9_waiting_capture` | `src/cratekit/intake/imported_cli.py` | user | 3 file(s) | 1059 | 1 | killed |
| `u127.L6_bridge_ignores_calibration` | `src/cratekit/intake/land_cli.py` | user | 11 file(s) | 454 | 1 | killed |
| `u127.L7_land_warnings_unsaid` | `src/cratekit/intake/land_native.py` | user | 11 file(s) | 454 | 7 | killed |
| `u110-b.B1_pass_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 5 | killed |
| `u110-b.B2_name_names_file` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 18 | killed |
| `u110-b.B3_check_pass` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 5 | killed |
| `u110-b.B4_recheck_xml` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `u110-b.B6_intake_lock` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `u110-b.B7_name_overrides` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 27 | killed |
| `u110-b.B8_shown_playlist` | `src/cratekit/intake/land_cli.py` | user | 8 file(s) | 369 | 1 | killed |
| `r501-a.S1_verify_state_guard` | `src/cratekit/core/session.py` | maintainer | 5 file(s) | 134 | 1 | killed |
| `r501-a.S2_excusal_capture` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-a.S3_excusal_proof` | `src/cratekit/core/session.py` | user | 5 file(s) | 134 | 5 | killed |
| `r501-a.T1_precheck_excusal` | `src/cratekit/core/tree_registry.py` | user | 5 file(s) | 134 | 4 | killed |
| `r501-b.I1_rollback_abandon` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 3 | killed |
| `r501-b.I2_rollback_unlink` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-b.I3_rollback_fresh_only` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 1 | killed |
| `r501-b.I4_mark_awaiting` | `src/cratekit/intake/ingest.py` | user | 5 file(s) | 134 | 23 | killed |
| `r501-b.L1_unretired_name` | `src/cratekit/intake/land_cli.py` | user | 3 file(s) | 130 | 3 | killed |
| `r777-confirm.N4_plain_name` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777-confirm.N7_digest_marks` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N10_screen_says_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N11_exclusive` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N12_no_landing_required` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 4 | killed |
| `r777.N18_unreachable_called_bridge` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N19_digest_landings` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 1 | killed |
| `r777.N5_bridge_accepted` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 2 | killed |
| `r777.N6_no_reread` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 2 | killed |
| `r777.N9_proof_is_file` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 123 | 4 | killed |
| `u219.G3_adds_frozen` | `src/cratekit/write/routing_cli.py` | user | 4 file(s) | 297 | 21 | killed |
| `r312.W2_worker_writes_nothing` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 8 | killed |
| `r312.W3_success_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 5 | killed |
| `r312.W4_failure_exit_silent` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 2 | killed |
| `r312.W5_cause_steps_replaced` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `r312.W7b_pre_drive_refusal_extended` | `src/cratekit/write/routing_cli.py` | maintainer | 2 file(s) | 231 | 1 | killed |
| `r312.W8_list_not_by_job` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 2 | killed |
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
| `u132.W6_resort_note` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u155.W6_inbox_item_genre` | `src/cratekit/write/routing_cli.py` | user | 2 file(s) | 231 | 1 | killed |
| `u155.W3_gate_column` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 3 | killed |
| `u155.W4_gate_count` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 3 | killed |
| `u155.W5_owed_once` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 1 | killed |
| `u155.W7_export_item_genre` | `src/cratekit/write/routing_export.py` | user | 2 file(s) | 231 | 1 | killed |
| `r361-a.A7_mark_verb_forgets_debris` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 103 | 1 | killed |
| `r361-a.A8_mark_verb_respells_the_word` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 103 | 1 | killed |
| `r361-a.A9_reword_the_why` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 103 | 1 | killed |
| `u72.M8_registry_digest_source` | `src/cratekit/cli/registry.py` | user | 1 file(s) | 27 | 7 | killed |
| `u113-a.A3_no_pass_splits_nothing` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u72-b.M20_shown_files` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M10_default_folder` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 19 | killed |
| `u72.M1_abort_applies` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M3_digest_drops_where` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u72.M5_digest_drops_export` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 2 | killed |
| `u72.M9_default_name_colons` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 27 | 1 | killed |
| `u110-a.A2_favorites_word` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 91 | 2 | killed |
| `u110-a.A7_join_order` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 91 | 2 | killed |
| `u110-a.A8_labels_first` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 91 | 1 | killed |
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 198 | 8 | killed |
| `u110-c.C7_intake_lock_prefix` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 198 | 13 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 198 | 3 | killed |
| `r677-b.V4_after_the_stale_test` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r677.V1_no_preflight_before_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 7 | killed |
| `r677.V3_refusal_never_replaces_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 5 | killed |
| `r677.V5_preflight_raises_directly` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 2 | killed |
| `r677.V6_manifest_rows_not_handed_over` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 192 | 1 | killed |
| `r677.E1_export_asked_before_the_library` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 192 | 69 | killed |
| `r677.E2_library_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 192 | 5 | killed |
| `r677.E3_intake_file_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 192 | 4 | killed |
| `u110-c.C5_missing_hint` | `src/cratekit/intake/missing_cli.py` | user | 5 file(s) | 187 | 1 | killed |
| `u307.R21_unrunnable_reason_lost` | `src/cratekit/intake/land_cli.py` | user | 4 file(s) | 152 | 3 | killed |
| `r515-operator.S10_intake_all_withheld_quiet` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `r515-operator.S11_intake_playlist_no_warning` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 40 | 4 | killed |
| `u69-b.M10_out_not_a_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M12_unlisted_status` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M17_lists_folder` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 3 | killed |
| `u69-b.M18_inner_cause` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69-b.M19_resume_step` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M1_handler_key` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M2_succeeded_only` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u69.M4_report_coverage` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M5_by_count` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u69.M6_state_word` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73-b.B2_every_ref_kept` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73-b.B3_first_source_wins` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A10_every_job_skipped` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A1_blank_run` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A2_library_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A3_run_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A4_intake_key_filter` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A5_oldest_first` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u73.A7_open_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A8_failed_refuses` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 1 | killed |
| `u73.A9_skip_failed_ignored` | `src/cratekit/intake/missing_cli.py` | user | 1 file(s) | 40 | 2 | killed |
| `u69-b.M20_registry_schema` | `src/cratekit/cli/registry.py` | user | 2 file(s) | 1038 | 24 | killed |
| `u307.R13_named_by_isrc_resolves_unasked` | `src/cratekit/intake/missing_cli.py` | user | 5 file(s) | 139 | 5 | killed |
| `r502-a.G5_no_adjudicate` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 4 | killed |
| `r502-a.G6_no_mount_guard` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-a2.G7_frozen_config` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-b.G10_since_keys_swapped` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 5 | killed |
| `r502-b.G12_since_check_detail` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r502-b.G9_missing_count_stale` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r502-b2.G13_written_line_for_gained` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-a.G10_owned_key` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 86 | killed |
| `r503-a.G1_no_lookup` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G2_found_is_answered` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-a.G4_offered_not_decremented` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G5_state_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-a.G6_answered_not_counted` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G7_answered_read_as_since` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-a.G8_rejected_not_kept` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-a.G9_answered_last` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-b.E2_offered_listed` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G11_summary` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 3 | killed |
| `r503-b.G12_answered_check` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-b.G13_offered_check` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G14_no_gone` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `r503-b.G15_no_new` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G16_json_uncaught` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 1 | killed |
| `r503-b.G17_no_hint` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 167 | 2 | killed |
| `u307.R12_summary_head_written_zero` | `src/cratekit/intake/missing_cli.py` | user | 4 file(s) | 107 | 23 | killed |
| `u79-a.A3_unreadable_ignored` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B1_floor_halved` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-b.B3_no_identifier_offered` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 2 | killed |
| `u79-b.B4_rejected_read_as_accepted` | `src/cratekit/intake/candidates.py` | user | 1 file(s) | 50 | 1 | killed |
| `u79-c.C2_owned_row_searched` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 2 | killed |
| `u79-c.C3_accepted_held_listed_again` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 1 | killed |
| `u79-c.C4_nothing_found_is_a_no_op` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 2 | killed |
| `u79-c.C7_fixed_name` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 98 | 10 | killed |
| `u305.M3_recorded_version_key_unfolded` | `src/cratekit/acquire/match_identity.py` | user | 2 file(s) | 163 | 3 | killed |
| `r770-a.A5_tree_built_without_the_refusal` | `src/cratekit/intake/ingest.py` | user | 1 file(s) | 33 | 2 | killed |
| `r770-a.A2_unreachable_root_is_read_anyway` | `src/cratekit/intake/ingest.py` | user | 2 file(s) | 60 | 3 | killed |
| `r658-a.C2_keychain_shared` | `tests/conftest.py` | user | 1 file(s) | 3 | 1 | killed |
| `r658-a.C4_recognition_shared` | `tests/conftest.py` | user | 1 file(s) | 3 | 1 | killed |
| `r658-a.C5_fetcher_shared` | `tests/conftest.py` | user | 1 file(s) | 3 | 1 | killed |
| `r658-a.C7_state_roots_not_redirected` | `tests/conftest.py` | user | 1 file(s) | 0 | 0 | error |
| `u326.R4_live_provider_refused` | `tests/conftest.py` | maintainer | 4 file(s) | 273 | 1 | killed |
| `u206-b.M2b_disabled_recall_composite` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1130 | 8 | killed |
| `u206.M13_write_without_merge` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1130 | 5 | killed |
| `u206.M1_recall_never_hits` | `src/cratekit/acquire/isrc_cache.py` | user | 9 file(s) | 1130 | 19 | killed |

## Zero rows and what they owe

- `u113-a.A3_no_pass_splits_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r773-b.P1_proof_granted_whatever_the_export_names`

settle, existing: find no landed track missing, so any export proves any import

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r773-b.json`, row `P1_proof_granted_whatever_the_export_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_intake_imported.py`
- Collected: 128 against a baseline of 128
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_against_an_export_taken_before_the_import`
  - `tests/test_export_collection.py::test_the_import_proof_is_withheld_on_a_moved_library_with_no_rule`
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`

Old text:

```
    missing = [entry for entry in landed if entry.track not in held]
```

New text:

```
    missing = []
```

### `u142.S1_folder_prefix`

sets: drop the Downloaded Sets prefix, so a set is filed into the plain year folder the filing owns

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S1_folder_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 13 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_export_set.py::test_two_folders_named_as_the_year_refuse_and_write_nothing`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
FOLDER_PREFIX = "Downloaded Sets "
```

New text:

```
FOLDER_PREFIX = ""
```

### `u142.S5_create_under_the_year`

apply_archive: create the folder under the plain year, so a set's folder is made with the filing's name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S5_create_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 216 against a baseline of 216
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        lambda: account.create_folder(planned.year),
```

### `u140.B6_mark_refusal_dropped`

plan_rename retitles a playlist the archive marked

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B6_mark_refusal_dropped`
- Moved: Anchored where u309-replay-after-d.json replayed it: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 85 against a baseline of 85
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_playlist_the_archive_marked_is_refused_rather_than_retitled`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`

Old text:

```
        if mark is not None:
            raise _rename_unresolved(

```

New text:

```
        if False:
            raise _rename_unresolved(

```

### `r1349.E2_open_left`

record (existing): the open gate left open after it is answered

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `E2_open_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1211 against a baseline of 1211
- Kills: 10 (killed)
- Killed:
  - `tests/test_gate_not_reached.py::test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide`
  - `tests/test_gate_siblings.py::test_an_answer_thirteen_hours_ago_is_history_and_says_nothing`
  - `tests/test_gate_siblings.py::test_an_answered_run_two_days_old_is_not_blocked`
  - `tests/test_organize.py::test_an_account_answer_ahead_continued_is_refused_before_the_verb_runs`
  - `tests/test_run_retire.py::test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again`
  - `tests/test_run_retire.py::test_a_wider_threshold_retires_fewer`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`
  - `tests/test_run_retire.py::test_retire_reads_its_default_threshold_from_the_file`
  - `tests/test_run_retire.py::test_retire_says_nothing_about_an_old_run_already_answered`

Old text:

```
    if state.open_gate == spec.name:
        state.open_gate = None


def blocked_by
```

New text:

```
    if False:
        state.open_gate = None


def blocked_by
```

### `r1349.E3_offer_unrecorded`

require (existing): the offer never recorded when the gate is reached

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `E3_offer_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1211 against a baseline of 1211
- Kills: 47 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_decision_answered_against_a_plan_that_has_since_moved_is_stale`
  - `tests/test_cli_contract.py::test_an_unanswered_gate_exits_with_the_documented_code_and_leaves_the_run_resumable`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[sync.all]`
  - `tests/test_gate_not_reached.py::test_a_gate_offered_and_answered_takes_a_new_answer_over_its_offer`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_and_left_open_takes_the_answer_and_binds_what_it_showed`
  - `tests/test_gate_pins.py::test_a_moved_digest_is_still_refused_before_the_pin_is_read`
  - `tests/test_gate_pins.py::test_the_open_gate_records_the_pin_and_the_record_carries_it_through_json`
  - `tests/test_gate_siblings.py::test_decide_continue_carries_the_warning_on_the_verbs_own_envelope`
  - `tests/test_gate_siblings.py::test_decide_repeats_over_a_sibling_that_answered_then_stopped_at_another_gate`
  - `tests/test_gate_siblings.py::test_decide_repeats_the_warning_over_a_sibling_answered_apply_on_the_same_plan`
  - `tests/test_gate_stale_screen.py::test_a_digest_gate_with_nothing_to_show_says_so_as_its_open_gate_does`
  - `tests/test_gate_stale_screen.py::test_a_plan_that_moves_again_after_the_second_answer_is_stale_and_shows_the_newer_plan`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_and_its_message_are_otherwise_the_gates_own`
  - `tests/test_gate_stale_screen.py::test_a_stale_refusal_carries_the_moved_plan_as_an_open_gate_shows_it`
  - `tests/test_gate_stale_screen.py::test_an_unknown_inline_option_shows_the_plan_its_offer_recorded`
  - ... and 32 more, see the JSON sidecar

Old text:

```
        if spec.digest_source is not None and digest is not None:
            self.state.offers[spec.name] = digest
```

New text:

```
        if False:
            self.state.offers[spec.name] = digest
```

### `r1349.N4_open_ignored`

record: the open gate clause dropped, so a gate reached with no digest and left open is refused

- File: `src/cratekit/cli/gates.py`
- Source: `r1349.json`, row `N4_open_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_gate_not_reached.py`, `tests/test_organize.py`, `tests/test_gate_stale_screen.py`, `tests/test_run_decide_continue.py`, `tests/test_gate_pins.py`, `tests/test_cli_contract.py`, `tests/test_run_retire.py`, `tests/test_gate_siblings.py`
- Collected: 1211 against a baseline of 1211
- Kills: 15 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_conformance_3_admits_a_verb_carrying_two_gates[explicit-then-explicit]`
  - `tests/test_cli_contract.py::test_conformance_3_every_gate_refuses_and_then_the_verb_proceeds[run.retire]`
  - `tests/test_gate_not_reached.py::test_a_gate_already_answered_takes_a_new_answer_once_the_run_waits_elsewhere`
  - `tests/test_gate_not_reached.py::test_a_gate_reached_with_no_digest_and_left_open_still_takes_a_decide`
  - `tests/test_gate_siblings.py::test_an_answered_run_two_days_old_is_not_blocked`
  - `tests/test_gate_siblings.py::test_decide_says_nothing_when_this_run_was_offered_no_digest`
  - `tests/test_run_retire.py::test_a_gate_answered_after_the_plan_was_read_is_said_and_not_answered_again`
  - `tests/test_run_retire.py::test_a_record_retire_cannot_read_is_said_and_not_dropped`
  - `tests/test_run_retire.py::test_a_wider_threshold_retires_fewer`
  - `tests/test_run_retire.py::test_an_explicit_gate_is_retired_with_abort_and_never_apply`
  - `tests/test_run_retire.py::test_retire_asks_once_over_every_old_gate_and_answers_only_those`
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`
  - `tests/test_run_retire.py::test_retire_never_retires_its_own_run`
  - `tests/test_run_retire.py::test_retire_reads_its_default_threshold_from_the_file`
  - `tests/test_run_retire.py::test_retire_says_nothing_about_an_old_run_already_answered`

Old text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and state.open_gate != spec.name
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

New text:

```
        spec.digest_source is not None
        and spec.name not in state.offers
        and spec.name not in state.decisions
    ):
        raise GateNotReached(state, spec)
```

### `u40-author-full.D5_no_enable`

Do not register the operation, so every change decides SKIP_UNOWNED and the sweep reports a clean run over a library it did not touch

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D5_no_enable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 5 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`

Old text:

```
    metadata.enable((metadata.RETAG_GENRE,))
    metadata.assert_within_policy(library_plan.plan)
```

New text:

```
    metadata.assert_within_policy(library_plan.plan)
```

### `u40-author-full.D7_unmatched_dropped`

Do not surface a written file no row claims, so a half-applied sweep reports as a full one

- File: `src/cratekit/tagging/retag.py`
- Source: `u40-author-full.json`, row `D7_unmatched_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`
- Collected: 50 against a baseline of 50
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_genre_retag.py::test_a_written_file_no_live_row_claims_is_surfaced_rather_than_dropped`
  - `tests/test_genre_retag.py::test_two_live_rows_on_one_location_are_surfaced_rather_than_written_to_both`

Old text:

```
            unmatched.append(
                Unmatched(
                    path=str(result.path),
                    outcome=str(match.outcome.value),
                    content_ids=tuple(match.content_ids),
                )
            )
            continue
```

New text:

```
            continue
```

### `u40-author-full.F2_genre_unknown_silent`

First caller sample: drop the genre-unknown skip, so an unresolvable answer disappears from the plan

- File: `src/cratekit/write/metadata.py`
- Source: `u40-author-full.json`, row `F2_genre_unknown_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_genre_the_library_has_never_seen_is_skipped_and_surfaced`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_metadata_policy.py::test_a_genre_with_no_lookup_row_is_skipped_and_surfaced`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        if genre_id is None:
            skipped.append(Skipped(content_id, "genre-unknown", wanted))
            continue
```

New text:

```
        if genre_id is None:
            continue
```

### `u59.M1_permissive_default`

Restore the permissive default: an unreadable marker reads as active

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M1_permissive_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, _MARKER_ABSENT)
```

New text:

```
        marker = getattr(row, rb_writer.SOFT_DELETE_COLUMN, 0)
```

### `u59.M2_refusal_removed`

Delete the refusal entirely, so an absent marker falls through as falsey

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M2_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
        if marker is _MARKER_ABSENT or marker is None:
```

New text:

```
        if False:
```

### `u59.M4_tombstone_resolves`

Invert the active test, so a soft-deleted genre is the one that resolves

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M4_tombstone_resolves`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 10 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_genre_retag.py::test_a_written_file_is_relinked_to_the_existing_genre_row`
  - `tests/test_genre_retag.py::test_an_unregistered_operation_writes_nothing_and_the_apply_is_what_prevents_it`
  - `tests/test_genre_retag.py::test_re_applying_a_plan_over_an_already_linked_row_is_a_no_op`
  - `tests/test_metadata_policy.py::test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track`
  - `tests/test_metadata_policy.py::test_a_genre_that_exists_is_linked_by_identifier`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
```

New text:

```
        if marker:
            return row.ID
```

### `u59.M5_first_row_wins`

Return the first row rather than the first ACTIVE one, ending the loop

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M5_first_row_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 6 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_live_namesake_behind_a_tombstone_is_still_found_through_the_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_genre_is_invisible_through_the_shipped_reader`
  - `tests/test_genre_retag.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`
  - `tests/test_metadata_policy.py::test_a_deleted_marker_is_not_an_error_here_the_way_it_is_for_a_track`
  - `tests/test_metadata_policy.py::test_a_genre_whose_only_row_is_soft_deleted_resolves_to_nothing`
  - `tests/test_metadata_policy.py::test_a_soft_deleted_namesake_does_not_mask_the_live_genre_row`

Old text:

```
        if not marker:
            return row.ID
    return None
```

New text:

```
        return row.ID
    return None
```

### `u59.M6_reason_reworded`

Reword the refusal reason, which the plan and the report both key on

- File: `src/cratekit/write/metadata.py`
- Source: `u59.json`, row `M6_reason_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_metadata_policy.py`
- Collected: 97 against a baseline of 97
- Kills: 4 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_an_unreadable_marker_stops_the_run_rather_than_skipping_one_row`
  - `tests/test_metadata_policy.py::test_a_genre_row_that_cannot_report_the_marker_refuses_rather_than_resolving`
  - `tests/test_metadata_policy.py::test_an_explicit_none_marker_refuses_alongside_a_missing_attribute`
  - `tests/test_metadata_policy.py::test_an_unreadable_marker_is_not_collapsed_into_the_genre_unknown_skip`

Old text:

```
                "soft-delete-marker-unreadable",
```

New text:

```
                "soft-delete-marker-unknown",
```

### `r1372.K10_carried_read_error_silent`

carried: a record that cannot be read is skipped without a word

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K10_carried_read_error_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`

Old text:

```
            problems.append(
                f"run {run_id}'s carried steps could not be read ({type(exc).__name__}: {exc})"
            )
            continue
```

New text:

```
            continue
```

### `r1372.K15_let_go_keeps`

let_go: the record is never removed

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K15_let_go_keeps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`

Old text:

```
        carried_path(run_id, key).unlink(missing_ok=True)
```

New text:

```
        carried_path(run_id, key).exists()
```

### `r1372.K2_carry_writes_nothing`

carry: the record is built and never written

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K2_carry_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age`
  - `tests/test_sync_pair_stopped.py::test_a_carried_record_that_cannot_be_read_is_named_never_read_as_no_write`
  - `tests/test_sync_pair_stopped.py::test_a_carry_that_cannot_be_written_raises`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_that_cannot_be_read_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_the_snapshot_passed_is_read_as_no_write_even_when_still_on_disk`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_run_that_finished_the_pair_without_moving_its_snapshot_keeps_nothing_of_its_own`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
    config.atomic_write_bytes(payload, carried_path(steps.run_id, key))
```

New text:

```
    payload = payload
```

### `r1372.K3_carry_empty_steps`

carry: the record keeps an empty item, so its ordering detail is lost

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K3_carry_empty_steps`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_pair_resume_one.py::test_a_stop_in_the_middle_of_an_order_sends_no_move_again_and_a_later_sync_finishes_it`
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_reads_back_as_its_runs_steps_for_that_item_whatever_its_age`
  - `tests/test_sync_pair_stopped.py::test_two_items_of_one_run_are_carried_apart`
  - `tests/test_sync_pair_stopped_order.py::test_a_continue_of_the_stopped_run_after_its_plan_aged_out_still_finishes_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_after_its_steps_were_pruned_never_takes_the_scramble`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_paired_again_over_a_pending_order_is_held_until_the_provider_serves_it`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_older_than_a_held_plan_is_kept_is_still_finished_from_the_side_that_led`
  - `tests/test_sync_pair_stopped_order.py::test_a_stop_whose_held_plan_and_steps_were_pruned_is_still_finished`

Old text:

```
        "steps": dict(steps.done.get(str(key), {})),
```

New text:

```
        "steps": {},
```

### `r1372.K5_carried_under_held_plans`

carried_dir: the records are kept beside the held plans, where prune takes them

- File: `src/cratekit/core/held_plan.py`
- Source: `r1372.json`, row `K5_carried_under_held_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_carried_copy_gives_way_to_its_own_runs_steps_kept_under_the_same_plan`
  - `tests/test_sync_pair_stopped.py::test_a_carried_item_is_kept_from_prune_and_release_and_let_go_only_when_asked`
  - `tests/test_sync_pair_stopped_order.py::test_a_kept_stop_whose_pair_a_later_sync_finished_is_let_go`

Old text:

```
    return config.state_path(STATE_KEY) / CARRIED_DIR
```

New text:

```
    return config.state_path(STATE_KEY)
```

### `u225.M13_unreadable_silent`

recorded_steps: a record that cannot be read is dropped unnamed

- File: `src/cratekit/core/held_plan.py`
- Source: `u225.json`, row `M13_unreadable_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_held_plan_steps.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`
- Collected: 227 against a baseline of 227
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_every_kept_runs_steps_are_read_and_an_unreadable_one_is_named`
  - `tests/test_sync_pair_stopped_order.py::test_a_runs_steps_that_cannot_be_read_are_named_never_read_as_no_write`

Old text:

```
            problems.append(
                f"run {run_id}'s steps could not be read ({type(exc).__name__}: {exc})"
            )
```

New text:

```
            pass
```

### `u232.A3_stub_raise_exec`

_no_host_process_table: the no process stub answers zero under raise_exec, where pyrekordbox raises

- File: `tests/conftest.py`
- Source: `u232.json`, row `A3_stub_raise_exec`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_pyrekordbox_reads_no_rekordbox_with_rekordbox_open_on_the_host`

Old text:

```
        if raise_exec:
            # pyrekordbox's own words, which name rekordbox whatever was asked.
```

New text:

```
        if False:
            # pyrekordbox's own words, which name rekordbox whatever was asked.
```

### `u232.A4_tripwire_records`

tripwire: refuse without recording, so a call the code swallows passes silently

- File: `tests/conftest.py`
- Source: `u232.json`, row `A4_tripwire_records`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
            reached.append(f"psutil.{name} was called from:\n{where}")
```

New text:

```
            where = where
```

### `u232.A5_tripwire_refuses`

tripwire: record without refusing, answering an empty listing instead

- File: `tests/conftest.py`
- Source: `u232.json`, row `A5_tripwire_refuses`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
            raise AssertionError(
                f"a test reached the host's real process table through psutil.{name}; "
```

New text:

```
            return []
            raise AssertionError(
                f"a test reached the host's real process table through psutil.{name}; "
```

### `u232.A7_tripwire_on_pids`

_no_host_process_table: trip on process_iter only, leaving psutil.pids, the careful scan's own read, open

- File: `tests/conftest.py`
- Source: `u232.json`, row `A7_tripwire_on_pids`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`
- Collected: 9 against a baseline of 9
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
        monkeypatch.setattr(psutil, "pids", tripwire("pids"))
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

### `u326.R9_host_process_tripwire`

_no_host_process_table: leave psutil.process_iter real, so pyrekordbox's walk reads the host's process table

- File: `tests/conftest.py`
- Source: `u326.json`, row `R9_host_process_tripwire`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_host_process_table.py`, `tests/test_process_scan.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_host_process_table.py::test_a_test_reaching_psutils_enumeration_without_the_opt_in_fails`

Old text:

```
        monkeypatch.setattr(psutil, "process_iter", tripwire("process_iter"))
```

New text:

```
        pass
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

### `u166.A4_no_add`

apply_rows: add nothing to Analyze

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A4_no_add`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 14 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_held_row_is_not_added_to_analyze_and_analyze_removed_after_approval_refuses`
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_inbox_analyzed.py::test_a_removal_that_did_not_take_is_refused_after_the_commit`
  - `tests/test_inbox_analyzed.py::test_a_removed_smart_or_outside_node_named_analyze_is_never_written_into`
  - `tests/test_inbox_analyzed.py::test_a_row_removed_from_the_collection_or_missing_from_it_stays_and_is_named`
  - `tests/test_inbox_analyzed.py::test_a_row_with_no_analysis_path_or_analysed_unset_stays`
  - `tests/test_inbox_analyzed.py::test_after_an_analysis_of_three_the_clear_removes_exactly_three_and_no_track`
  - `tests/test_inbox_analyzed.py::test_inbox_refill_never_takes_analyze_for_an_account_playlist_of_that_name`
  - `tests/test_inbox_analyzed.py::test_nothing_analysed_asks_a_late_analysis_is_stale_a_track_held_twice_clears_once_then_nothing`
  - `tests/test_intake_land_account_playlists_native.py::test_a_file_no_account_playlist_claimed_stays_in_the_batch_playlist`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
            if added_ids:
                analyze = _analyze_row(db, plan, anchor)
```

New text:

```
            if False:
                analyze = _analyze_row(db, plan, anchor)
```

### `u166.A7_record_count`

apply_rows: record the batch's memberships only on success

- File: `src/cratekit/intake/native.py`
- Source: `u166.json`, row `A7_record_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_analyzed.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`, `tests/test_intake_land_hearts_native.py`
- Collected: 185 against a baseline of 185
- Kills: 5 (killed)
- Killed:
  - `tests/test_inbox_analyzed.py::test_a_landing_fills_analyze_once_names_it_made_then_found_and_the_rotation_leaves_it`
  - `tests/test_intake_land_hearts_native.py::test_once_a_band_holds_the_heart_the_additive_refresh_puts_it_in_that_folders_favorites`
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_writers_native.py::test_one_file_becomes_one_row_and_one_playlist_under_the_adopted_root`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships + analyze_added,
```

New text:

```
        _record_landing_commit(
            record,
            plan,
            len(added_ids),
            memberships,
```

### `u111-b.B1_move_names_every_table`

The membership move's commit admits the whole removable set again, the playlist table included

- File: `src/cratekit/write/trees.py`
- Source: `u111-b.json`, row `B1_move_names_every_table`
- Moved: Anchored where u302-replay-after-d.json replayed it: the removal commit is now in the step _remove_leavers, one level less indented, the same call
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_adopt_move.py`
- Collected: 117 against a baseline of 117
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_rotate.py::test_only_the_rotation_asks_its_commit_to_admit_a_removed_playlist`

Old text:

```
            rb_writer.commit_guarded(db, removals=(rb_writer.MEMBERSHIP_TABLE,))
```

New text:

```
            rb_writer.commit_guarded(db, removals=rb_writer.REMOVABLE_TABLES)
```

### `r777.N15_any_pass`

landings_of_pass counts a landing of another pass

- File: `src/cratekit/intake/native_plan.py`
- Source: `r777.json`, row `N15_any_pass`
- Moved: Anchored where u307-replay-after-a.json replayed it: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 197 against a baseline of 197
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_a_landing_names_the_pass_it_was_given_on_the_record_sync_mark_reads[RUN_synced]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`

Old text:

```
            and record.detail.get(PASS_KEY) == name

```

New text:

```
(empty)
```

### `r259.S1_scope_owned_sample`

Existing guard sample: scope.scoped no longer drops owned identities

- File: `src/cratekit/sync/scope.py`
- Source: `r259.json`, row `S1_scope_owned_sample`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`
- Collected: 31 against a baseline of 31
- Kills: 1 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_a_rerun_after_a_clean_sync_processes_only_unowned_items`

Old text:

```
        if item.identity in owned:
```

New text:

```
        if False:
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

### `r359.M10_claims_downloaded`

Reword the sentence into the false claim the defect is about, that the files were downloaded

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M10_claims_downloaded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
            "the library, crate intake missing lists it, and no later sync offers "
```

New text:

```
            "the library until downloaded, and no later sync offers "
```

### `r359.M1_drop_field`

Drop the swept_means field from the playlists block, the row the brief names

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M1_drop_field`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired`
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
        "swept_means": SWEPT_MEANS,

```

New text:

```
(empty)
```

### `r359.M2_token`

Change the machine token to a nearby word that no longer says not acquired

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M2_token`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_json_its_tracks_were_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
SWEPT_MEANS = "resolved-not-acquired"
```

New text:

```
SWEPT_MEANS = "resolved"
```

### `r359.M3_said_silent`

said returns nothing, so the check carries no sentence while the json field stays

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M3_said_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))
```

New text:

```
    return None
```

### `r359.M8_drop_resolved`

Reword the sentence so it no longer says the tracks were resolved

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M8_drop_resolved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
            "a recorded playlist had its tracks resolved against the library, not "
```

New text:

```
            "a recorded playlist had its tracks checked against the library, not "
```

### `r359.M9_drop_not_acquired`

Reword the sentence so it no longer says the tracks were not acquired

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `M9_drop_not_acquired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`
  - `tests/test_sync_all.py::test_the_block_says_what_swept_means_whatever_the_pass_found`

Old text:

```
            "acquired, so a track its intake job reported missing is still not in "
```

New text:

```
            "fetched, so a track its intake job reported missing is still not in "
```

### `r359.S1_record_on_any_state`

Existing guard sample: the cursor records a playlist whatever state its job ended in

- File: `src/cratekit/sync/playlists.py`
- Source: `r359.json`, row `S1_record_on_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`
- Collected: 146 against a baseline of 146
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_failed_job_is_not_recorded_and_its_playlist_is_offered_again`
  - `tests/test_sync_all.py::test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded[cancelled]`
  - `tests/test_sync_all.py::test_a_playlist_intake_by_hand_that_did_not_succeed_is_not_recorded[failed]`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_the_cursor_records_ids_only_once_a_job_succeeds`

Old text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
```

New text:

```
        if identity and identity not in seen:
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

### `r361-a.A10_enum_value_respelled`

The enum member's kebab value changes, so the report and the check say another word

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A10_enum_value_respelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
    LABEL_DEBRIS = "label-debris"
```

New text:

```
    LABEL_DEBRIS = "label-library"
```

### `r361-a.A2_case_insensitive`

The rule widens to any case, so a person's Colorize Library is excluded too

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `A2_case_insensitive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_label_batch_debris_is_excluded_by_the_source_systems_own_rule`
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`
  - `tests/test_sync_all.py::test_the_label_batch_debris_is_not_queued_as_intake`

Old text:

```
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)
```

New text:

```
    return str(name or "").upper().endswith(LIBRARY_PLAYLIST_SUFFIX)
```

### `r361-a.D2_drop_the_placeholder`

Existing: the favourites placeholder is queued by the playlists source

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D2_drop_the_placeholder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`
  - `tests/test_sync_all.py::test_the_favourites_placeholders_are_left_to_the_favourites_source`

Old text:

```
    if placeholders.is_placeholder(playlist.name):
        return Excluded.PLACEHOLDER

```

New text:

```
(empty)
```

### `r361-a.D3_drop_in_flight`

Existing: an open job no longer holds its playlist back, so it is queued twice

- File: `src/cratekit/sync/playlists.py`
- Source: `r361-a.json`, row `D3_drop_in_flight`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_the_playlist_exclusions_in_the_order_a_person_is_told`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_the_cursor_records_ids_only_once_a_job_succeeds`

Old text:

```
    if playlist.playlist_id in in_flight:
        return Excluded.IN_FLIGHT

```

New text:

```
(empty)
```

### `r382.M11_reconcile_source_jobs`

reconcile reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M11_reconcile_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        for identity in completed(playlist_jobs(store, cfg, handler_key=handler_key))
```

New text:

```
        for identity in completed(source_jobs(store, cfg, handler_key=handler_key))
```

### `r382.M12_in_flight_source_jobs`

plan's in flight set reads source_jobs again instead of playlist_jobs

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M12_in_flight_source_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`

Old text:

```
    in_flight = open_playlists(playlist_jobs(store, cfg, handler_key=handler_key))
```

New text:

```
    in_flight = open_playlists(source_jobs(store, cfg, handler_key=handler_key))
```

### `r382.M15_completed_duplicates`

Sample of an existing guard: completed records a playlist once per succeeded job

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M15_completed_duplicates`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_two_succeeded_jobs_for_one_playlist_record_it_once`

Old text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
```

New text:

```
        if job.state == jobs.JobState.SUCCEEDED and identity:
```

### `r382.M1_restore_source_filter`

Restore the source_id == playlists filter on playlist_jobs, the brief's named row: a hand queued job is no longer reconciled or in flight

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M1_restore_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
        and (job.payload or {}).get("source_id") == SOURCE_ID
    )
```

### `r382.M2_drop_handler_key`

Drop the handler key filter from playlist_jobs, so an intake.set job naming a playlist is reconciled

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M2_drop_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_set_intake_naming_the_playlist_is_not_a_playlist_intake`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.library_id == cfg.library.volume_id
    )
```

### `r382.M3_drop_library`

Drop the library filter from playlist_jobs, so another library's finished job records here

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M3_drop_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_finished_job_is_not_this_librarys_sweep`

Old text:

```
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        if job.handler_key == handler_key
    )
```

### `r382.M4_hearts_recorded`

Drop the reserved hearts reference check in recorded_as, so a hearts job records favorites

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M4_hearts_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_intake_is_not_recorded_as_a_playlist`

Old text:

```
    if intake_cli.is_favorites(reference):
        return ""
```

New text:

```
(empty)
```

### `r382.M5_no_verbatim_for_pass_jobs`

Drop the verbatim return for a pass's own job, so its listing id goes through the lowercasing parser

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M5_no_verbatim_for_pass_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_queued_job_records_the_listing_identifier_verbatim`

Old text:

```
    if (job.payload or {}).get("source_id") == SOURCE_ID:
        return reference

```

New text:

```
(empty)
```

### `r382.M6_no_parse`

Record a hand typed reference verbatim instead of parsing it, so a typed URL is recorded as the URL

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M6_no_parse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        return typed_playlist_id(reference)
```

New text:

```
        return reference
```

### `r382.M7_invalid_records_nothing`

An unparseable hand reference records nothing instead of itself

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M7_invalid_records_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_reads_a_playlist_ingested_by_hand_as_recorded`
  - `tests/test_sync_all.py::test_a_playlist_ingested_by_hand_is_recorded_on_the_next_pass`
  - `tests/test_sync_all.py::test_a_playlist_intake_still_open_by_hand_is_in_flight_not_queued`

Old text:

```
    except PlaylistReferenceInvalid:
        return reference
```

New text:

```
    except PlaylistReferenceInvalid:
        return ""
```

### `r382.M8_completed_raw`

completed reads the raw payload reference instead of recorded_as

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M8_completed_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_intake_is_not_recorded_as_a_playlist`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[0F1E2D3C-4B5A-6978-8A9B-ACBDCEDFE0F1]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://listen.tidal.com/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1?u]`
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_by_hand_records_its_identifier[https://tidal.com/browse/playlist/0f1e2d3c-4b5a-6978-8a9b-acbdcedfe0f1]`

Old text:

```
        identity = recorded_as(job)
        if job.state == jobs.JobState.SUCCEEDED
```

New text:

```
        identity = _playlist_of(job)
        if job.state == jobs.JobState.SUCCEEDED
```

### `r382.M9_open_raw`

open_playlists reads the raw payload reference instead of recorded_as

- File: `src/cratekit/sync/playlists.py`
- Source: `r382.json`, row `M9_open_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_all.py`, `tests/test_sync_mark.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_typed_as_a_url_and_still_open_is_in_flight`

Old text:

```
    return frozenset(recorded_as(job) for job in found if job.is_open() and recorded_as(job))
```

New text:

```
    return frozenset(_playlist_of(job) for job in found if job.is_open() and _playlist_of(job))
```

### `r501-d.R2_settled_is_not_imported`

routing_cli._all_settled: count acknowledged tracks as proof, so a run nobody imported is recorded as proven

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R2_settled_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_deferred_routing.py`, `tests/test_routing_workers.py`
- Collected: 313 against a baseline of 313
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
- Collected: 313 against a baseline of 313
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

### `u307.R11_imported_session_ignored`

imported_cli._considered: ignore --session, so every intake run is considered and an unknown run is not refused

- File: `src/cratekit/intake/imported_cli.py`
- Source: `u307.json`, row `R11_imported_session_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_export_collection.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW or wanted not in (None, record.session_id):
```

New text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW:
```

### `r501-c.M1_export_name_check`

imported_cli.read_export: drop the refusal of an export carrying an intake file's name, leaving only the identity check

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M1_export_name_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
    if any(export.name.endswith(suffix) for suffix in tree_registry.PENDING_XML_SUFFIXES):
        raise _refuse_export(
```

New text:

```
    if False:
        raise _refuse_export(
```

### `r501-c.M2_export_identity_check`

imported_cli.read_export: drop the refusal of the file a waiting run names, so a link to the intake file proves its own import

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M2_export_identity_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
        if artifact and _same_file(export, Path(artifact)):
```

New text:

```
        if False:
```

### `r501-c.M3_missing_is_not_imported`

imported_cli.settle: ignore missing tracks, so an export taken before the import proves it

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M3_missing_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`

Old text:

```
    if missing:
        return {
```

New text:

```
    if False:
        return {
```

### `r501-c.M4_nothing_recorded`

imported_cli.settle: drop the unverifiable answer, so a run the ledger names no file for is proven by any export

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-c.json`, row `M4_nothing_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`

Old text:

```
    if not landed:
        # NOTHING RECORDED IS NOT NOTHING OWED.
```

New text:

```
    if False:
        # NOTHING RECORDED IS NOT NOTHING OWED.
```

### `r501-d.M10_waiting_legacy`

imported_cli._waiting: look only for awaiting-import, so every landing made before the fix is left where it was

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M10_waiting_legacy`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`

Old text:

```
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return (
```

New text:

```
    if record.state is session.SessionState.AWAITING_IMPORT:
        return True
    return False and (
```

### `r501-d.M11_close_refusal_reported`

imported_cli._close_if_nothing_is_owed: raise the gated close's refusal, ending the verb after the file is retired and the proof recorded

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M11_close_refusal_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`

Old text:

```
    except CratekitError as exc:
        return {"closed": False, "close_refused": exc.cause.reason, "why": exc.cause.message}
```

New text:

```
    except CratekitError:
        raise
```

### `r501-d.M13_waiting_needs_export`

imported_cli.intake_imported: drop the refusal when a run is waiting and no export is named, so the verb answers no-op over a waiting run

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M13_waiting_needs_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`

Old text:

```
    if waiting and export is None:
        raise _no_export(waiting)
```

New text:

```
    if waiting and export is None:
        waiting = []
```

### `r501-d.M9_waiting_capture`

imported_cli._waiting: drop the no capture condition, so an open destructive session is taken for a landing

- File: `src/cratekit/intake/imported_cli.py`
- Source: `r501-d.json`, row `M9_waiting_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_cli_contract.py`
- Collected: 1059 against a baseline of 1059
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`

Old text:

```
        record.state is session.SessionState.OPEN
        and record.snapshot_path is None
        and record.pending is None
```

New text:

```
        record.state is session.SessionState.OPEN
        and record.pending is None
```

### `u127.L6_bridge_ignores_calibration`

The bridge names the vocals verb as owed on an uncalibrated library

- File: `src/cratekit/intake/land_cli.py`
- Source: `u127.json`, row `L6_bridge_ignores_calibration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if cut is None:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

New text:

```
    if False:
        return f"{BRIDGE_VOX_NONE}, and {native.VOX_UNCALIBRATED}"
```

### `u127.L7_land_warnings_unsaid`

intake land gives no vox warning

- File: `src/cratekit/intake/land_native.py`
- Source: `u127.json`, row `L7_land_warnings_unsaid`
- Moved: Anchored where u307-replay-after-b.json replayed it: the same text, now in src/cratekit/intake/land_native.py, was in src/cratekit/intake/land_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_land_vox_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 454 against a baseline of 454
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_three_files_become_three_rows_and_one_playlist_under_the_adopted_root`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_no_category]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_uncalibrated]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_that_cannot_be_written_tags_nothing_says_why_and_lands_the_batch[_unreadable]`
  - `tests/test_intake_land_vox_native.py::test_a_tag_written_under_a_removed_category_is_said_and_never_counted`
  - `tests/test_intake_land_vox_native.py::test_the_tag_is_written_under_the_vocals_category_and_a_file_with_no_score_is_named`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    warnings.extend(vox_warnings(landed.collection))
```

New text:

```
    warnings.extend([])
```

### `u110-b.B1_pass_names_file`

--pass no longer names the intake file, so sync mark cannot find the pass

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B1_pass_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_gets_a_distinct_name_and_one_pass_is_never_merged`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`

Old text:

```
    if pass_name is not None:
        return pass_name
    if name
```

New text:

```
    if name
```

### `u110-b.B2_name_names_file`

--name alone no longer names the intake file, breaking a landing typed the old way

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B2_name_names_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 18 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
    if name is not None:
        return name
    return default_name
```

New text:

```
    return default_name
```

### `u110-b.B3_check_pass`

A --pass holding a slash or nothing is not refused before the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B3_check_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[ padded]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[a/b]`
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[a\\b]`

Old text:

```
    _check_pass(pass_name)

```

New text:

```
(empty)
```

### `u110-b.B4_recheck_xml`

The xml landing does not ask again under the lock whether its default name is still free

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B4_recheck_xml`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_default_name_taken_after_the_gate_is_refused_under_the_lock`

Old text:

```
            _still_free(cfg, batch)

```

New text:

```
            pass

```

### `u110-b.B6_intake_lock`

The landing takes only the batch lock and not the intake file's

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B6_intake_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`

Old text:

```
    with landing.batch_lock(batch), landing.intake_lock(stem):
```

New text:

```
    with landing.batch_lock(batch):
```

### `u110-b.B7_name_overrides`

--name is ignored and the default name is always taken

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B7_name_overrides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 27 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_intake_land_names.py::test_name_and_pass_together_name_the_batch_and_the_file_apart`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_intake_land_native.py::test_a_failure_on_the_second_file_leaves_the_database_as_it_was_and_names_the_moves`
  - `tests/test_intake_land_native.py::test_a_file_already_in_the_collection_is_present_and_not_added_twice`
  - `tests/test_intake_land_native.py::test_a_file_whose_tags_resolve_to_no_sub_stays_in_staging_on_the_native_medium_too`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        ctx.args.name
        if ctx.args.name is not None
        else batch_name.readable(
```

New text:

```
        batch_name.readable(
```

### `u110-b.B8_shown_playlist`

The xml gate screen no longer names the batch playlist

- File: `src/cratekit/intake/land_cli.py`
- Source: `u110-b.json`, row `B8_shown_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_label_sync_go.py`, `tests/test_sync_mark.py`, `tests/test_sync_unmark.py`
- Collected: 369 against a baseline of 369
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`

Old text:

```
        "playlist": planned.batch,

```

New text:

```
(empty)
```

### `r501-a.S1_verify_state_guard`

session.mark_import_verified: drop the refusal of any state but awaiting-import, so any record can be marked proven

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S1_verify_state_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_only_a_run_waiting_on_an_import_has_one_to_verify`

Old text:

```
    if record.state is not SessionState.AWAITING_IMPORT:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

New text:

```
    if False:
        raise refuse(
            "internal-error",
            f"session {record.session_id} is {str(record.state)!r}, not "
            f"{str(SessionState.AWAITING_IMPORT)!r}; only a session waiting on an "
            f"import has one to verify",
```

### `r501-a.S2_excusal_capture`

session.owes_only_deferred_routing: drop the no capture condition, so a run holding a capture is excused from the cutover precheck

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S2_excusal_capture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_the_precheck_refuses_a_verified_run_that_holds_a_capture[holding-a-capture]`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and IMPORT_VERIFIED_KEY in record.detail
```

### `r501-a.S3_excusal_proof`

session.owes_only_deferred_routing: drop the proof condition, so any open run with no capture is excused, a crashed landing included

- File: `src/cratekit/core/session.py`
- Source: `r501-a.json`, row `S3_excusal_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 5 (killed)
- Killed:
  - `tests/test_cutover_precheck.py::test_an_open_run_blocks_the_flip`
  - `tests/test_cutover_precheck.py::test_an_open_run_refuses_the_revert_because_it_may_have_written`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_doctor_reads_a_proven_run_as_proven_and_not_as_in_progress`
  - `tests/test_intake_imported.py::test_the_precheck_refuses_an_open_run_with_no_proof_recorded`

Old text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
        and IMPORT_VERIFIED_KEY in record.detail
```

New text:

```
        record.state is SessionState.OPEN
        and record.snapshot_path is None
```

### `r501-a.T1_precheck_excusal`

tree_registry.assert_cutover_ready: drop the excusal, so a proven landing refuses the cutover for ever, which is R-501 itself

- File: `src/cratekit/core/tree_registry.py`
- Source: `r501-a.json`, row `T1_precheck_excusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_precheck_excuses_a_verified_run_holding_no_capture`

Old text:

```
        if not record.terminal and not session.owes_only_deferred_routing(record)
```

New text:

```
        if not record.terminal
```

### `r501-b.I1_rollback_abandon`

ingest.place_files: drop the abandon in the rollback, so a refused call leaves its session non terminal

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I1_rollback_abandon`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_records_no_track_the_ledger_cannot_withdraw`
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`
  - `tests/test_intake_imported.py::test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file`

Old text:

```
        with contextlib.suppress(Exception):
            routing_pass.close_run(record, cfg, state=session.SessionState.ABANDONED)
        raise
```

New text:

```
        raise
```

### `r501-b.I2_rollback_unlink`

ingest.place_files: drop the unlink in the rollback, so a refused call leaves an intake file with no run behind it

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I2_rollback_unlink`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_refusal_after_the_session_opens_abandons_it_and_removes_the_file`

Old text:

```
        if wrote and fresh:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
```

New text:

```
        if False:
            with contextlib.suppress(OSError):
                destination.unlink(missing_ok=True)
```

### `r501-b.I3_rollback_fresh_only`

ingest.place_files: unlink whatever is at the destination, so a failed call removes an earlier run's intake file

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I3_rollback_fresh_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`

Old text:

```
        if wrote and fresh:
```

New text:

```
        if wrote:
```

### `r501-b.I4_mark_awaiting`

ingest.place_files: never mark the session awaiting-import, so every landing leaves an open record again

- File: `src/cratekit/intake/ingest.py`
- Source: `r501-b.json`, row `I4_mark_awaiting`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_cutover_precheck.py`, `tests/intake/test_pipeline.py`
- Collected: 134 against a baseline of 134
- Kills: 23 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_failed_call_records_no_track_the_ledger_cannot_withdraw`
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_placed_call_ends_awaiting_import_with_the_action_persisted`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`
  - `tests/test_intake_imported.py::test_intake_file_ends_pending_and_is_settled_the_same_way`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - ... and 8 more, see the JSON sidecar

Old text:

```
        wrote = True
        session.mark_awaiting_import(
```

New text:

```
        wrote = True
        session.pending_import if False else (lambda *a, **k: None)(
```

### `r501-b.L1_unretired_name`

land_cli.unretired_name: return the name unchanged, so sync mark cannot find its pass from a retired intake file

- File: `src/cratekit/intake/land_cli.py`
- Source: `r501-b.json`, row `L1_unretired_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land.py`, `tests/test_sync_mark.py`
- Collected: 130 against a baseline of 130
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_sync_mark_reads_the_same_pass_off_a_retired_intake_file[RUN_synced_inboxed.xml.imported-2]`
  - `tests/test_intake_imported.py::test_sync_mark_reads_the_same_pass_off_a_retired_intake_file[RUN_synced_inboxed.xml.imported]`
  - `tests/test_intake_imported.py::test_the_retired_name_is_out_of_the_pending_scan_and_reads_back`

Old text:

```
    return _RETIRED_TAIL.sub("", name)
```

New text:

```
    return name
```

### `r777-confirm.N4_plain_name`

Confirm: _native_proof takes a pass name no landing could have been given, after the test that pins its message

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N4_plain_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_name_no_landing_could_have_been_given_is_refused`

Old text:

```
    if not landing.plain_name(name):
```

New text:

```
    if False:
```

### `r777-confirm.N7_digest_marks`

Confirm, the first table's old text was moved by the fix round: the native digest no longer covers the planned marks

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N7_digest_marks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_answer_is_stale_once_another_playlist_becomes_whole`

Old text:

```
            "landings": list(proof.landings),
            "marks": planned,
```

New text:

```
            "landings": list(proof.landings),
```

### `r777.N10_screen_says_pass`

The gate screen on a native pass shows an intake file line instead of the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N10_screen_says_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`

Old text:

```
        if isinstance(proof, marks.NativeLanding)
        else {"intake file": str(proof)}
```

New text:

```
        if False
        else {"intake file": str(proof)}
```

### `r777.N11_exclusive`

--xml and --pass are no longer one or the other

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N11_exclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_file_and_the_pass_are_one_or_the_other`

Old text:

```
    proof = parser.add_mutually_exclusive_group(required=True)
```

New text:

```
    proof = parser
```

### `r777.N12_no_landing_required`

_native_proof makes a proof when no closed landing of the pass committed

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N12_no_landing_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[abandoned]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[another-pass]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[never-committed]`
  - `tests/test_sync_mark.py::test_a_native_pass_no_closed_committed_landing_names_is_refused[no-landing]`

Old text:

```
    if not landings:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N18_unreachable_called_bridge`

An unreachable library falls through to the bridge refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N18_unreachable_called_bridge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_library_is_named_and_never_called_the_bridge`

Old text:

```
    if medium.declared is None:
        # AN UNREACHABLE ROOT
```

New text:

```
    if False:
        # AN UNREACHABLE ROOT
```

### `r777.N19_digest_landings`

The native digest no longer covers the landings that prove the pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N19_digest_landings`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_second_landing_of_the_pass_since_the_plan_makes_the_answer_stale`

Old text:

```
            "landings": list(proof.landings),

```

New text:

```
(empty)
```

### `r777.N5_bridge_accepted`

_native_proof accepts --pass on an intake tree still on the xml bridge

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N5_bridge_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_pass_named_on_a_tree_still_on_the_bridge_is_refused_naming_the_file`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
    if not medium.native:
        raise _blocked(
```

New text:

```
    if False:
        raise _blocked(
```

### `r777.N6_no_reread`

apply_pass no longer reads the proof again before the first rename

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N6_no_reread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_landing_recorded_between_the_plan_and_the_apply_renames_nothing`
  - `tests/test_sync_mark.py::test_a_tree_put_back_on_the_bridge_after_the_plan_renames_nothing`

Old text:

```
        if _native_proof(cfg, planned.name) != planned.native:
```

New text:

```
        if False:
```

### `r777.N9_proof_is_file`

PassPlan.proof hands the engine the absent file on a native pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777.json`, row `N9_proof_is_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 123 against a baseline of 123
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_a_native_pass_whose_tracks_the_library_holds_is_marked_after_the_answer`
  - `tests/test_sync_mark.py::test_a_native_pass_with_one_track_not_held_leaves_that_playlist_alone`
  - `tests/test_sync_mark.py::test_organize_marks_a_native_pass_through_its_gate`

Old text:

```
        return self.native if self.native is not None else self.xml
```

New text:

```
        return self.xml
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

### `r312.W2_worker_writes_nothing`

handle_resort: the item report always says nothing was left

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W2_worker_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
- Kills: 8 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_names_the_membership_it_left_where_it_was`
  - `tests/test_routing_workers.py::test_a_resort_resume_that_drove_nothing_names_no_leftover`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`
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
- Collected: 231 against a baseline of 231
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
- Collected: 231 against a baseline of 231
- Kills: 2 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_refusal_raised_before_the_drive_carries_no_leftover_step`
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`

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
- Collected: 231 against a baseline of 231
- Kills: 1 (killed)
- Killed:
  - `tests/test_routing_workers.py::test_a_resort_that_failed_part_way_names_only_what_the_finished_tree_left[left-behind]`

Old text:

```
                cause.remediation, steps=(*cause.remediation.steps, message)
```

New text:

```
                cause.remediation, steps=(message,)
```

### `r312.W7b_pre_drive_refusal_extended`

_resume: drop the guard that re-raises a refusal raised before the drive. Measured ZERO on the first pass over a full run of 9679, then re-measured after test_a_refusal_raised_before_the_drive_carries_no_leftover_step was written against it

- File: `src/cratekit/write/routing_cli.py`
- Source: `r312.json`, row `W7b_pre_drive_refusal_extended`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
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
- Collected: 231 against a baseline of 231
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

### `u132.W6_resort_note`

The resort resume carries no skipped step note

- File: `src/cratekit/write/routing_cli.py`
- Source: `u132.json`, row `W6_resort_note`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_routing_workers.py`
- Collected: 231 against a baseline of 231
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

### `r361-a.A7_mark_verb_forgets_debris`

The mark verb's plan no longer decides label-debris, so the playlist falls through to the reports

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A7_mark_verb_forgets_debris`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        elif playlists.is_library_debris(entry.name):
            entry.reason = LABEL_DEBRIS
        elif job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
        elif job.state is not jobs.JobState.SUCCEEDED:
```

### `r361-a.A8_mark_verb_respells_the_word`

The mark verb spells its own word for the reason instead of reading the enum

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A8_mark_verb_respells_the_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
LABEL_DEBRIS = str(playlists.Excluded.LABEL_DEBRIS)
```

New text:

```
LABEL_DEBRIS = "label-library"
```

### `r361-a.A9_reword_the_why`

The why sentence is reworded, never appended to, since the suite asserts with in

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A9_reword_the_why`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_label_batch_debris_is_said_and_never_renamed`

Old text:

```
        "its name is the source system's label run debris, which a sync never "
        "offers and never renames"
```

New text:

```
        "its name is a throwaway the other system left, which a sync never "
        "offers and never renames"
```

### `u72.M8_registry_digest_source`

The registry gate declares no digest source

- File: `src/cratekit/cli/registry.py`
- Source: `u72.json`, row `M8_registry_digest_source`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[a file arrived]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[batch name]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[export]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[folder]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
                prompt="Move these files into the library and write the intake file?",
                digest_source="plan",
```

New text:

```
                prompt="Move these files into the library and write the intake file?",
```

### `u113-a.A3_no_pass_splits_nothing`

A landing given no pass still splits, by every named job on the library

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u113-a.json`, row `A3_no_pass_splits_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if not pass_name or not files:
        return ()
    found = sources(cfg, pass_name)
```

New text:

```
    if not files:
        return ()
    found = sources(cfg, pass_name or "")
```

### `u72-b.M20_shown_files`

The gate context lists no file names

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72-b.json`, row `M20_shown_files`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
        "files": [item.name for item in planned.items],
```

New text:

```
        "files": [],
```

### `u72.M10_default_folder`

The default folder is the library root, not download staging

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M10_default_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[a file arrived]`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`
  - ... and 4 more, see the JSON sidecar

Old text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.paths.download_staging)
```

New text:

```
    folder = Path(ctx.args.folder) if ctx.args.folder else Path(cfg.library.root)
```

### `u72.M1_abort_applies`

An abort no longer stops the verb: only an empty plan returns NO_OP

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M1_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if option != "apply" or not planned.items:
```

New text:

```
    if not planned.items:
```

### `u72.M3_digest_drops_where`

The digest drops the batch, the target and the intake file, so an answer for one name applies under another

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M3_digest_drops_where`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[batch name]`

Old text:

```
        "batch": planned.batch,
        "target": str(target),
        "destination": str(destination),

```

New text:

```
(empty)
```

### `u72.M5_digest_drops_export`

The digest drops the export path

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M5_digest_drops_export`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answer_is_stale_for_any_other_plan[export]`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        "export": str(export),

```

New text:

```
(empty)
```

### `u72.M9_default_name_colons`

The default batch name keeps the run id's colons

- File: `src/cratekit/intake/land_cli.py`
- Source: `u72.json`, row `M9_default_name_colons`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`
- Collected: 27 against a baseline of 27
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`

Old text:

```
    return run_id.replace(":", "")
```

New text:

```
    return run_id
```

### `u110-a.A2_favorites_word`

A hearts job says Tidal playlists instead of Favorites

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A2_favorites_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_job_the_pass_lost_does_not_name_the_batch`
  - `tests/test_intake_land_names.py::test_each_kind_of_pass_job_says_its_own_word`

Old text:

```
        return FAVORITES if source_id == intake_cli.FAVORITES_SOURCE_ID else PLAYLISTS
```

New text:

```
        return PLAYLISTS
```

### `u110-a.A7_join_order`

Several pass words are joined alphabetically instead of in the fixed order

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A7_join_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 91 against a baseline of 91
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_job_the_pass_lost_does_not_name_the_batch`
  - `tests/test_intake_land_names.py::test_several_words_are_joined_in_one_order_whatever_order_they_arrive_in`

Old text:

```
    ordered = [word for word in _ORDER if word in present]
```

New text:

```
    ordered = [word for word in sorted(present) if word in _ORDER]
```

### `u110-a.A8_labels_first`

Label rows lose their precedence over the pass's jobs

- File: `src/cratekit/intake/batch_name.py`
- Source: `u110-a.json`, row `A8_labels_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`
- Collected: 91 against a baseline of 91
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`

Old text:

```
    said = label_words(label_rows)
    if said is not None:
        return said
    if pass_name:
```

New text:

```
    if pass_name:
```

### `u110-c.C1_apply_playlist`

The xml landing no longer hands its batch name to the splice, so the playlist is the intake file's stem again

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C1_apply_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 198 against a baseline of 198
- Kills: 8 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_gets_a_distinct_name_and_one_pass_is_never_merged`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_and_its_intake_file_keeps_the_pass`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_landing.py::test_three_tagged_files_land_in_one_intake_file`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`
  - `tests/test_landing_labels.py::test_two_labels_across_two_years_are_four_playlists_in_the_intake_file`

Old text:

```
            playlist=plan.batch,

```

New text:

```
(empty)
```

### `u110-c.C7_intake_lock_prefix`

The intake lock shares its key with a batch of the same name

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C7_intake_lock_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 198 against a baseline of 198
- Kills: 13 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_refused_file_is_warned_and_marked`
  - `tests/test_intake_land.py::test_an_answer_is_stale_once_its_manifest_is_rewritten`
  - `tests/test_intake_land.py::test_an_answered_run_lands_with_an_import_blocking_nothing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_engine_failing_with_no_refusal]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_every_target_taken]`
  - `tests/test_intake_land_names.py::test_a_landing_whose_intake_file_another_landing_is_writing_is_refused`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`

Old text:

```
lock_key("intake file\0" + stem)
```

New text:

```
lock_key(stem)
```

### `u110-c.C8_plain_dot`

A name starting with a dot passes the plain name rule

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C8_plain_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 198 against a baseline of 198
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_landing.py::test_an_empty_folder_or_a_batch_name_that_is_no_plain_folder_is_refused[..]`
  - `tests/test_landing.py::test_an_empty_folder_or_a_batch_name_that_is_no_plain_folder_is_refused[.hidden]`

Old text:

```
        and not text.startswith(".")

```

New text:

```
(empty)
```

### `r677-b.V4_after_the_stale_test`

any gate refusal, a stale answer included, is replaced by the preflight refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677-b.json`, row `V4_after_the_stale_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
```

New text:

```
        if unusable is not None:
```

### `r677.V1_no_preflight_before_the_gate`

the original defect: the plan read never asks the engine, so a missing export reaches the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V1_no_preflight_before_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_the_first_run_stops_at_the_gate_and_an_abort_moves_nothing`

Old text:

```
    if planned.items:
        try:
```

New text:

```
    if False:
        try:
```

### `r677.V3_refusal_never_replaces_the_gate`

the preflight refusal is caught and dropped, so the gate is offered over an unusable export

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V3_refusal_never_replaces_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_no_intake_folder-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_not_a_collection-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`

Old text:

```
        if unusable is not None and exc.cause.remediation.remedy is Remedy.ANSWER_DECISION:
            raise unusable from None
```

New text:

```
        if False:
            raise unusable from None
```

### `r677.V5_preflight_raises_directly`

the preflight refusal is raised at once, so a recorded abort over a missing export refuses instead of ending in nothing done

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V5_preflight_raises_directly`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_land.py::test_an_apply_over_a_missing_export_is_the_engine_s_refusal`

Old text:

```
        except CratekitError as exc:
            unusable = exc
```

New text:

```
        except CratekitError as exc:
            raise exc
```

### `r677.V6_manifest_rows_not_handed_over`

the plan read asks the export check without the manifest's label rows, so a label layout the export cannot take reaches the gate

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V6_manifest_rows_not_handed_over`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`

Old text:

```
                label_rows=manifest.rows if manifest is not None else (),
```

New text:

```
                label_rows=(),
```

### `r677.E1_export_asked_before_the_library`

the preflight asks the export before the library, so an unmounted volume is named as a missing export

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E1_export_asked_before_the_library`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 69 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`
  - `tests/test_intake_imported.py::test_the_intake_file_is_refused_as_its_own_proof`
  - `tests/test_intake_imported.py::test_the_proof_names_the_tracks_it_proved_and_the_file_it_retired`
  - `tests/test_intake_imported.py::test_tracks_acknowledged_as_gone_are_not_proof_of_an_import`
  - `tests/test_intake_imported.py::test_two_waiting_runs_are_settled_independently`
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_and_its_labels_reported`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_absent-library-export-unusable-30]`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - ... and 54 more, see the JSON sidecar

Old text:

```
    _check_batch(plan.batch)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
```

New text:

```
    _check_batch(plan.batch)
    _check_export(export, destination, tree_registry.read(cfg), label_rows)
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
```

### `r677.E2_library_check_dropped`

the preflight never asks the library

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E2_library_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_landing.py::test_a_folder_the_library_already_owns_is_refused`
  - `tests/test_landing.py::test_a_landing_target_under_staging_is_refused`
  - `tests/test_landing.py::test_a_staging_folder_on_another_device_is_refused_by_name`
  - `tests/test_landing.py::test_an_absent_library_root_is_refused_before_the_device_probe`

Old text:

```
    _check_library(cfg, plan.folder, target_dir(cfg, plan.batch))
    if destination.exists():
```

New text:

```
    if destination.exists():
```

### `r677.E3_intake_file_check_dropped`

the preflight never asks whether the intake file is already there

- File: `src/cratekit/intake/landing.py`
- Source: `r677.json`, row `E3_intake_file_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 192 against a baseline of 192
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_held_batch_name_refuses_a_second_landing`
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_intake_there-output-exists-30]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal[_an_intake_file_already_there]`
  - `tests/test_landing.py::test_an_existing_intake_file_is_never_overwritten`

Old text:

```
    if destination.exists():
        raise refuse(
            "output-exists",
```

New text:

```
    if False:
        raise refuse(
            "output-exists",
```

### `u110-c.C5_missing_hint`

intake missing --run prints --name RUN again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u110-c.json`, row `C5_missing_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_names.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 187 against a baseline of 187
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
f"--pass {name}, adding
```

New text:

```
f"--name {name}, adding
```

### `u307.R21_unrunnable_reason_lost`

land_cli._unrunnable: a command line the landing cannot run is refused as internal-error, not intake-list-unusable

- File: `src/cratekit/intake/land_cli.py`
- Source: `u307.json`, row `R21_unrunnable_reason_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_native.py`, `tests/test_intake_land.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_intake_land_rehearse.py`
- Collected: 152 against a baseline of 152
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_native.py::test_rekordbox_running_or_an_export_on_a_native_tree_is_refused_before_the_gate`
  - `tests/test_intake_land_rehearse.py::test_a_rehearsal_on_the_bridge_is_refused`
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`

Old text:

```
        "intake-list-unusable", message, remedy=Remedy.FIX_COMMAND_LINE, steps=steps,
```

New text:

```
        "internal-error", message, remedy=Remedy.FIX_COMMAND_LINE, steps=steps,
```

### `r515-operator.S10_intake_all_withheld_quiet`

An intake playlist with every track withheld is a quiet no op

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S10_intake_all_withheld_quiet`
- Moved: Anchored where u325-replay-after.json replayed it: Same no-tracks return in intake_playlist; U298 replaced the local _no_op with cli.output.no_job
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
```

New text:

```
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
```

### `r515-operator.S11_intake_playlist_no_warning`

An intake playlist listed short carries no warning

- File: `src/cratekit/intake/cli.py`
- Source: `r515-operator.json`, row `S11_intake_playlist_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_playlist_declaring_ten_with_two_withheld_queues_eight_and_warns`
  - `tests/test_intake_missing.py::test_a_playlist_whose_every_track_is_withheld_is_not_a_quiet_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_hearts_all_withheld_are_not_read_as_an_account_with_none`

Old text:

```
        warnings = (warned(short),) if short is not None else ()
```

New text:

```
        warnings = ()
```

### `u69-b.M10_out_not_a_folder`

Drop the refusal of an --out that exists and is not a folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M10_out_not_a_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    if out.exists() and not out.is_dir():
```

New text:

```
    if False:
```

### `u69-b.M12_unlisted_status`

Report unlisted missing tracks as a note instead of a failing check

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M12_unlisted_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
"fail" if unlisted else "ok",
```

New text:

```
"info" if unlisted else "ok",
```

### `u69-b.M17_lists_folder`

Write into download staging itself rather than its lists folder

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M17_lists_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_missing_tracks_none_of_which_can_be_listed_write_the_unlisted_list_not_a_no_op`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
out = intake_cli._load().paths.download_staging / LISTS_DIR
```

New text:

```
out = intake_cli._load().paths.download_staging
```

### `u69-b.M18_inner_cause`

Drop the failed job's own cause from the refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M18_inner_cause`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`

Old text:

```
            inner=job.cause,
```

New text:

```
            inner=None,
```

### `u69-b.M19_resume_step`

Drop the resume command from an open job's refusal

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69-b.json`, row `M19_resume_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
            f"finish it with: crate {argv}" if job.is_open() else
```

New text:

```
            "finish it first" if job.is_open() else
```

### `u69.M1_handler_key`

Drop the refusal of a job queued under another verb's handler key

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M1_handler_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_job_of_another_verb_is_refused`

Old text:

```
    if job.handler_key not in intake_cli.INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u69.M2_succeeded_only`

Drop the refusal of a job that is not succeeded (open, failed, cancelled)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M2_succeeded_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_failed_job_is_refused_carrying_its_own_cause`
  - `tests/test_intake_missing.py::test_an_open_job_is_refused_and_nothing_is_written`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
```

New text:

```
    if False:
```

### `u69.M4_report_coverage`

Drop the refusal when the reports do not cover the items one for one

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M4_report_coverage`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if False:
```

### `u69.M5_by_count`

Compare reports to items by count instead of by identifier

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M5_by_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
    if sorted(reported) != sorted(wanted):
```

New text:

```
    if len(reported) != len(wanted):
```

### `u69.M6_state_word`

Drop the refusal of a report whose state word this verb cannot read

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u69.json`, row `M6_state_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_fewer_readable_reports_than_items_refuses_rather_than_listing_a_subset`

Old text:

```
        if report.get("state") not in _WORDS or not isinstance(report.get("track"), Mapping):
```

New text:

```
        if not isinstance(report.get("track"), Mapping):
```

### `u73-b.B2_every_ref_kept`

Stop accumulating every reference an id came from

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B2_every_ref_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
            refs.append(said)
```

New text:

```
            pass
```

### `u73-b.B3_first_source_wins`

Let the last job an id came from win its provenance instead of the first

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73-b.json`, row `B3_first_source_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        first.setdefault(ref, job)
```

New text:

```
        first[ref] = job
```

### `u73.A10_every_job_skipped`

Drop the refusal of a run whose every job failed, left to the layer after it

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A10_every_job_skipped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `u73.A1_blank_run`

Drop the refusal of a blank --run, so a blank run is compared as it stands

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A1_blank_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_blank_run_is_refused_and_does_not_match_a_job_queued_with_no_run`

Old text:

```
    if not run_id.strip():
```

New text:

```
    if False:
```

### `u73.A2_library_filter`

Drop the library half of the run selection, so the run alone picks jobs

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A2_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
and job.library_id == library_id
```

New text:

```
and True
```

### `u73.A3_run_filter`

Drop the run half of the selection, so every intake job for the library is listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A3_run_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
(job.payload or {}).get(RUN_ID) == run_id
```

New text:

```
True
```

### `u73.A4_intake_key_filter`

Drop the intake handler key filter, so a labels or favourites job in the run is selected

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A4_intake_key_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
            if job.handler_key in intake_cli.INTAKE_KEYS
```

New text:

```
            if True
```

### `u73.A5_oldest_first`

Reverse the job order, newest first, so first source wins picks the later playlist

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A5_oldest_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
key=lambda job: (job.created, job.job_id),
```

New text:

```
key=lambda job: (job.created, job.job_id), reverse=True,
```

### `u73.A7_open_refuses`

Drop the refusal of a run holding an open job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A7_open_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
    if still_open:
```

New text:

```
    if False:
```

### `u73.A8_failed_refuses`

Drop the refusal of a run holding a failed or cancelled job

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A8_failed_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if False:
```

### `u73.A9_skip_failed_ignored`

Ignore --skip-failed, so a failed job refuses the run whatever the flag says

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u73.json`, row `A9_skip_failed_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`
- Collected: 40 against a baseline of 40
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_every_job_failed_refuses_even_with_skip_failed`

Old text:

```
    if unfinished and not skip_failed:
```

New text:

```
    if unfinished:
```

### `u69-b.M20_registry_schema`

Declare the verb plan/1 in the registry, which the human renderer does not show

- File: `src/cratekit/cli/registry.py`
- Source: `u69-b.json`, row `M20_registry_schema`
- Moved: Anchored where u303-replay-merged.json replayed it: U303 laid the registry out a keyword run per line and shortened its comments; intake.missing's schema is the same pair, swapped to plan the same way
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_cli_contract.py`
- Collected: 1038 against a baseline of 1038
- Kills: 24 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_is_no_op_and_writes_nothing`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_a_run_with_nothing_missing_and_nothing_skipped_is_a_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - ... and 9 more, see the JSON sidecar

Old text:

```
        # the list's path and the download command (R-400).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
```

New text:

```
        # the list's path and the download command (R-400).
        emits=frozenset({"plan"}), output_schema="plan/1",
```

### `u307.R13_named_by_isrc_resolves_unasked`

missing_cli._named_by_isrc: resolve the catalogue even when no row carries an askable ISRC, so a job with none spends a login

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u307.json`, row `R13_named_by_isrc_resolves_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_staged.py`, `tests/test_isrc_screen.py`
- Collected: 139 against a baseline of 139
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`
  - `tests/test_intake_missing_isrc.py::test_a_set_with_no_isrc_resolves_no_catalogue_and_spends_no_login`
  - `tests/test_intake_missing_isrc.py::test_missing_tracks_none_named_and_none_writable_refuse_rather_than_no_op`

Old text:

```
    if askable:
        found = (resolve or _catalogue_once())()
```

New text:

```
    if True:
        found = (resolve or _catalogue_once())()
```

### `r502-a.G5_no_adjudicate`

Skip reading a person's answer back, so a row answered as another track reads as a fresh question and drops out

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G5_no_adjudicate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    if asked:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

New text:

```
    if False:
        with review.open_store(cfg) as items:
            for handler_key, at in asked.items():
```

### `r502-a.G6_no_mount_guard`

Drop the absent music folder refusal before the library walk

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a.json`, row `G6_no_mount_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    if not music.is_dir():
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

New text:

```
    if False:
        raise refuse(
            "library-volume-unmounted",
            f"this library's music folder {str(music)!r} is not there, so no track "
```

### `r502-a2.G7_frozen_config`

Ask the library at the root the first job froze rather than the current configuration (the review's finding)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-a2.json`, row `G7_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`

Old text:

```
    cfg = intake_cli._load()
    music = Path(cfg.library.root) / cfg.library.music_dir
```

New text:

```
    cfg = jobs.frozen_config(origins[0])
    music = Path(cfg.library.root) / cfg.library.music_dir
```

### `r502-b.G10_since_keys_swapped`

Count a row held since under suppressed_since and a row deleted since under owned_since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G10_since_keys_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_the_library_is_asked_where_it_is_now_not_where_the_job_froze_it`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
    match.MatchState.MATCHED: "owned_since",
    match.MatchState.SUPPRESSED: "suppressed_since",
```

New text:

```
    match.MatchState.MATCHED: "suppressed_since",
    match.MatchState.SUPPRESSED: "owned_since",
```

### `r502-b.G12_since_check_detail`

Reword the since check so it no longer names the rows in the library since

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G12_since_check_detail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
            f"{since['owned_since']} in the library since, {since['suppressed_since']} "
```

New text:

```
            f"{since['owned_since']} held now, {since['suppressed_since']} "
```

### `r502-b.G9_missing_count_stale`

Report the job's missing count rather than the count still missing now

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b.json`, row `G9_missing_count_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`

Old text:

```
        counts["missing"] = len(missing)

```

New text:

```
(empty)
```

### `r502-b2.G13_written_line_for_gained`

Drop the written line's gained branch, so a job whose rows were all gained reads as a job with nothing missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r502-b2.json`, row `G13_written_line_for_gained`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    elif gained:
        said = (
```

New text:

```
    elif False:
        said = (
```

### `r503-a.G10_owned_key`

File an answered row now owned under answered_missing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G10_owned_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 86 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_deleted_track_whose_row_kept_a_credit_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[04A - 126 - Malive, Tito Azevedo, MRQZ - Burning (Extended Mix).flac-tags1-row1]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[07A - 128 - Traumer, antraum, Anton - Hyaku.flac-tags2-row2]`
  - `tests/test_intake_missing.py::test_a_held_track_is_owned_and_nothing_is_listed[08A - 124 - Aurora Bloom - Sun Path.flac-tags0-row0]`
  - `tests/test_intake_missing.py::test_a_job_with_nothing_missing_is_no_op_and_writes_nothing`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_run_lists_only_its_own_finished_jobs_and_names_the_rest`
  - `tests/test_intake_missing.py::test_a_run_whose_rows_were_all_acquired_since_names_no_download`
  - `tests/test_intake_missing.py::test_a_run_with_nothing_missing_and_nothing_skipped_is_a_no_op`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - ... and 71 more, see the JSON sidecar

Old text:

```
    match.MatchState.MATCHED: "answered_owned",
```

New text:

```
    match.MatchState.MATCHED: "answered_missing",
```

### `r503-a.G1_no_lookup`

Read no answer at all, so every offered row stays offered whatever a person said (R-503 as filed)

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G1_no_lookup`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    answered = iter(_answered(offered))
```

New text:

```
    answered = iter([False] * len(offered))
```

### `r503-a.G2_found_is_answered`

Treat an item that exists as answered, so an unanswered row is asked again and offered again from the listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G2_found_is_answered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            said.append(held is not None and held.resolved)
```

New text:

```
            said.append(held is not None)
```

### `r503-a.G4_offered_not_decremented`

Leave an answered row in the offered count, so a rejected row still reads offered 1

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G4_offered_not_decremented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts["offered"] -= 1

```

New text:

```
(empty)
```

### `r503-a.G5_state_not_counted`

Do not count an answered row under the word it resolved to, so an accepted row is not owned

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G5_state_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                counts[_WORD[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G6_answered_not_counted`

Do not count answered rows under answered_*

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G6_answered_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
                now_answered[_ANSWERED[one.state]] += 1

```

New text:

```
(empty)
```

### `r503-a.G7_answered_read_as_since`

Count an answered row as a missing row would be counted, under since, rather than as answered

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G7_answered_read_as_since`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if report["state"] == "offered":
                # COUNTED
```

New text:

```
            if report["state"] == "never":
                # COUNTED
```

### `r503-a.G8_rejected_not_kept`

Keep only rows the job found missing, so a rejected row is counted and never listed

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G8_rejected_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            if one.state is match.MatchState.MISSING:
                kept.append(n)
```

New text:

```
            if one.state is match.MatchState.MISSING and report["state"] == "missing":
                kept.append(n)
```

### `r503-a.G9_answered_last`

Ask answered rows after missing ones, so a rejected row is listed out of its playlist order

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-a.json`, row `G9_answered_last`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    asking = [
        (job, report)
        for job, report in rows_in
        if report["state"] == "missing" or next(answered)
    ]
```

New text:

```
    asking = sorted(
        [
            (job, report)
            for job, report in rows_in
            if report["state"] == "missing" or next(answered)
        ],
        key=lambda pair: pair[1]["state"] == "offered",
    )
```

### `r503-b.E2_offered_listed`

Existing: list every offered report as missing without asking, the shape the brief forbids

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `E2_offered_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
        if report["state"] == "missing" or next(answered)
```

New text:

```
        if report["state"] == "missing" or next(answered) or True
```

### `r503-b.G11_summary`

Drop the answered_* counts from the summary

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G11_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
        **now_answered,

```

New text:

```
(empty)
```

### `r503-b.G12_answered_check`

Reword the answered check's breakdown

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G12_answered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
            f"missing, {now_answered['answered_owned']} in the library, "
```

New text:

```
            f"listed, {now_answered['answered_owned']} owned, "
```

### `r503-b.G13_offered_check`

Reword the offered check's route back to this listing

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G13_offered_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_nobody_answered_is_unchanged_and_asks_nothing`

Old text:

```
            f"see: crate review list, then list this again",
```

New text:

```
            f"see: crate review list",
```

### `r503-b.G14_no_gone`

Never name the tracks the earlier list holds and this one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G14_no_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
    if gone:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G15_no_new`

Never name the tracks this list holds and the earlier one does not

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G15_no_new`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`

Old text:

```
    if new:
        why.append(
```

New text:

```
    if False:
        why.append(
```

### `r503-b.G16_json_uncaught`

Let an earlier file that is not JSON escape the hint as an internal error

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G16_json_uncaught`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError):
        return []
```

New text:

```
    except (OSError, KeyError, TypeError):
        return []
```

### `r503-b.G17_no_hint`

Drop the hint read from the earlier file altogether

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r503-b.json`, row `G17_no_hint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_sync_mark.py`
- Collected: 167 against a baseline of 167
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`

Old text:

```
        why = _changed_since(out, name, rows)
```

New text:

```
        why = []
```

### `u307.R12_summary_head_written_zero`

missing_cli._summary_head: report written as zero, so the summary says nothing was listed when rows were written

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u307.json`, row `R12_summary_head_written_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing.py`, `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_staged.py`
- Collected: 107 against a baseline of 107
- Kills: 23 (killed)
- Killed:
  - `tests/test_intake_missing.py::test_a_deleted_credited_row_never_withholds_another_remix_of_the_recording`
  - `tests/test_intake_missing.py::test_a_mixed_job_writes_only_the_missing_rows`
  - `tests/test_intake_missing.py::test_a_row_a_person_answered_as_another_track_stays_listed`
  - `tests/test_intake_missing.py::test_a_row_held_in_another_version_since_is_offered_not_listed`
  - `tests/test_intake_missing.py::test_a_run_lists_an_offered_row_a_person_answered_as_a_job_does`
  - `tests/test_intake_missing.py::test_a_short_hearts_listing_is_queued_and_says_by_how_much`
  - `tests/test_intake_missing.py::test_a_track_deleted_on_purpose_is_suppressed_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_accepted_since_is_owned_and_not_listed`
  - `tests/test_intake_missing.py::test_an_offered_row_rejected_since_is_listed_and_no_longer_offered`
  - `tests/test_intake_missing.py::test_rows_acquired_since_the_job_are_not_listed_and_name_no_download`
  - `tests/test_intake_missing.py::test_two_playlists_sharing_a_track_list_it_once_with_both_provenances`
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_intake_missing_isrc.py::test_a_track_that_cannot_be_a_text_line_is_named_and_the_rest_are_still_written`
  - `tests/test_intake_missing_isrc.py::test_an_isrc_is_folded_before_it_is_asked_and_a_malformed_one_is_never_asked`
  - `tests/test_intake_missing_isrc.py::test_the_same_id_twice_in_one_answer_is_one_id_and_is_listed`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    head.update(written=len(written.listed))
```

New text:

```
    head.update(written=0)
```

### `u79-a.A3_unreadable_ignored`

A row of the answer that could not be read no longer stops a listing

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-a.json`, row `A3_unreadable_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
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

### `u79-b.B1_floor_halved`

The floor's value is halved, so a weaker hit is shown

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B1_floor_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
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

### `u79-b.B3_no_identifier_offered`

A candidate with no identifier is offered as an option

- File: `src/cratekit/intake/candidates.py`
- Source: `u79-b.json`, row `B3_no_identifier_offered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`
- Collected: 50 against a baseline of 50
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
- Collected: 50 against a baseline of 50
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

### `u79-c.C2_owned_row_searched`

A row the library holds is counted missing and searched for

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C2_owned_row_searched`
- Moved: Anchored where u325-replay-after.json replayed it: Same loop in _missing_for_list; U298 replaced its three state branches with a lookup in match_cli.SETTLED_WORDS, whose MATCHED entry is owned, so excluding owned sends a matched row to the missing branch, which is what disabling the MATCHED branch did
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_a_list_the_library_holds_entirely_is_a_no_op_that_spends_no_login`
  - `tests/test_intake_missing_search.py::test_an_owned_row_is_never_searched_for`

Old text:

```
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None:
            counts[word] += 1
```

New text:

```
        word = match_cli.SETTLED_WORDS.get(settled.state)
        if word is not None and word != "owned":
            counts[word] += 1
```

### `u79-c.C3_accepted_held_listed_again`

An accepted candidate the library now holds is listed for download again

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C3_accepted_held_listed_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_accepted_candidate_the_library_now_holds_is_not_listed_again`

Old text:

```
            if now.state in (match.MatchState.MATCHED, match.MatchState.SUPPRESSED):
                proposals[n]
```

New text:

```
            if False:
                proposals[n]
```

### `u79-c.C4_nothing_found_is_a_no_op`

Missing rows with no route to any of them end as nothing to do

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C4_nothing_found_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_no_candidate_for_any_row_refuses_rather_than_reading_as_nothing_to_do`
  - `tests/test_intake_missing_search.py::test_two_exact_candidates_are_offered_and_neither_is_picked`

Old text:

```
    if unfound and not listed and not asked:
```

New text:

```
    if False:
```

### `u79-c.C7_fixed_name`

The found list takes one fixed name, so the run after an answer is refused

- File: `src/cratekit/intake/missing_cli.py`
- Source: `u79-c.json`, row `C7_fixed_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing.py`
- Collected: 98 against a baseline of 98
- Kills: 10 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_one_exact_candidate_is_listed_without_review`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[.txt-txt-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[\xa7\xa7\xa7.txt-tracklist-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[friday set (2026).txt-friday-set-2026-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[intake-j1.unlisted.json-intake-j1-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[notes-notes-found]`
  - `tests/test_intake_missing_search.py::test_the_found_list_is_named_for_its_input[warmup.list.json-warmup-found]`
  - `tests/test_intake_missing_search.py::test_the_run_after_an_answer_lists_more_than_the_first_and_is_not_refused`
  - `tests/test_intake_missing_search.py::test_the_unlisted_list_is_read_and_its_found_list_sits_beside_the_jobs`
  - `tests/test_intake_missing_search.py::test_two_tracklists_of_one_file_name_in_two_folders_do_not_collide`

Old text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}-{digest}"
```

New text:

```
    return f"{stem or 'tracklist'}{FOUND_SUFFIX}"
```

### `u305.M3_recorded_version_key_unfolded`

Recorded.version_key: fold the version without dropping the no-op qualifiers, so Original Mix and nothing are two versions

- File: `src/cratekit/acquire/match_identity.py`
- Source: `u305.json`, row `M3_recorded_version_key_unfolded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_missing_search.py`, `tests/test_outbound_tidal_account.py`
- Collected: 163 against a baseline of 163
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_missing_search.py::test_an_original_mix_row_and_a_bare_candidate_are_one_version`
  - `tests/test_intake_missing_search.py::test_the_identity_is_the_folded_row_and_not_its_spelling`
  - `tests/test_outbound_tidal_account.py::test_a_row_with_no_version_agrees_with_an_original_mix_and_not_with_an_edit`

Old text:

```
        return version_token(self.version)
```

New text:

```
        return fold(self.version)
```

### `r770-a.A5_tree_built_without_the_refusal`

bridge_intake_tree: build the tree without asking first, the layer the landing's pre-move check rests on alone

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A5_tree_built_without_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_writers_native.py::test_every_intake_emitter_caller_builds_its_tree_through_the_one_refusing_builder`
  - `tests/test_intake_writers_native.py::test_the_bridge_landing_engine_refuses_a_native_tree_the_same_way_and_moves_nothing`

Old text:

```
    assert_intake_on_the_bridge(declared, registry)
    return rbxml.intake_tree(declared, registry)
```

New text:

```
    return rbxml.intake_tree(declared, registry)
```

### `r770-a.A2_unreachable_root_is_read_anyway`

intake_medium: read the taxonomy and the registry of a library root that is not there

- File: `src/cratekit/intake/ingest.py`
- Source: `r770-a.json`, row `A2_unreachable_root_is_read_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_writers_native.py`, `tests/test_intake_land.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_the_engine_would_refuse_refuses_before_the_gate[_unmounted-library-root-unreachable-22]`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_what_went_missing`
  - `tests/test_intake_writers_native.py::test_the_switch_reads_the_recorded_mode_and_nothing_else`

Old text:

```
    if not Path(cfg.library.root).is_dir():
```

New text:

```
    if False:
```

### `r658-a.C2_keychain_shared`

Keychain stub recorded on the shared monkeypatch again, so a body undo restores the real keychain

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C2_keychain_shared`
- Moved: The same mutation on the same fixture: U312 cut the fixture's docstring to its rule, so the recorded text, which quoted the whole fixture, no longer occurs; the stub is still moved from the fixture's own MonkeyPatch onto the test's shared one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```

def _isolate_keychain():
    """Swap the OS keychain for an in-memory dictionary.

    Replacing keyring's three module functions does not depend on its backend
    protocol. Without it a credential test on macOS pops a real dialog, and a
    headless run hangs rather than fails.
    """
    try:
        import keyring
    except ImportError:  # pragma: no cover - keyring is a core dependency
        yield {}
        return

    store: dict[tuple[str, str], str] = {}

    def _set(service: str, username: str, password: str) -> None:
        store[(service, username)] = password

    def _get(service: str, username: str):
        return store.get((service, username))

    def _delete(service: str, username: str) -> None:
        store.pop((service, username), None)

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(keyring, "set_password", _set)
        monkeypatch.setattr(keyring, "get_password", _get)
        monkeypatch.setattr(keyring, "delete_password", _delete)
        yield store

```

New text:

```

def _isolate_keychain(monkeypatch):
    """Swap the OS keychain for an in-memory dictionary.

    Replacing keyring's three module functions does not depend on its backend
    protocol. Without it a credential test on macOS pops a real dialog, and a
    headless run hangs rather than fails.
    """
    try:
        import keyring
    except ImportError:  # pragma: no cover - keyring is a core dependency
        yield {}
        return

    store: dict[tuple[str, str], str] = {}

    def _set(service: str, username: str, password: str) -> None:
        store[(service, username)] = password

    def _get(service: str, username: str):
        return store.get((service, username))

    def _delete(service: str, username: str) -> None:
        store.pop((service, username), None)

    monkeypatch.setattr(keyring, "set_password", _set)
    monkeypatch.setattr(keyring, "get_password", _get)
    monkeypatch.setattr(keyring, "delete_password", _delete)
    yield store

```

### `r658-a.C4_recognition_shared`

Recognition transport refusal on the shared monkeypatch again

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C4_recognition_shared`
- Moved: The same mutation on the same fixture: U312 cut the fixture's docstring to its rule, so the recorded text, which quoted the whole fixture, no longer occurs; the stub is still moved from the fixture's own MonkeyPatch onto the test's shared one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```

def _no_paid_recognition():
    """Refuse the live ACRCloud transport (U57); a test injects its own."""
    from cratekit.intake import acrcloud

    def refused(request):
        raise AssertionError(
            "a test reached the live recognition transport; inject a fake one"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(acrcloud, "http_transport", refused)
        yield

```

New text:

```

def _no_paid_recognition(monkeypatch):
    """Refuse the live ACRCloud transport (U57); a test injects its own."""
    from cratekit.intake import acrcloud

    def refused(request):
        raise AssertionError(
            "a test reached the live recognition transport; inject a fake one"
        )

    monkeypatch.setattr(acrcloud, "http_transport", refused)
    yield

```

### `r658-a.C5_fetcher_shared`

Mix fetcher refusal on the shared monkeypatch again

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C5_fetcher_shared`
- Moved: The same mutation on the same fixture: U312 cut the fixture's docstring to its rule, so the recorded text, which quoted the whole fixture, no longer occurs; the stub is still moved from the fixture's own MonkeyPatch onto the test's shared one.
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```

def _no_real_mix_download():
    """Refuse the shipped mix fetcher (U104); a test sets ``fetch.fetcher``."""
    from cratekit.intake import fetch

    def refused():
        raise AssertionError(
            "a test reached the shipped mix fetcher; set fetch.fetcher to a fake"
        )

    with _own_patch() as monkeypatch:
        monkeypatch.setattr(fetch, "fetcher", refused)
        yield

```

New text:

```

def _no_real_mix_download(monkeypatch):
    """Refuse the shipped mix fetcher (U104); a test sets ``fetch.fetcher``."""
    from cratekit.intake import fetch

    def refused():
        raise AssertionError(
            "a test reached the shipped mix fetcher; set fetch.fetcher to a fake"
        )

    monkeypatch.setattr(fetch, "fetcher", refused)
    yield

```

### `r658-a.C7_state_roots_not_redirected`

Composite for C1: the state roots fixture sets no HOME, so the platformdirs config resolves to the process home

- File: `tests/conftest.py`
- Source: `r658-a.json`, row `C7_state_roots_not_redirected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`
- Collected: 0 against a baseline of 3
- Kills: 0 (error)
- Note: MeasurementFailure: pytest produced no report file, so nothing was measured. exit 4

ImportError while loading conftest 'tests/conftest.py'.
/usr/lib/python3.12/ast.py:52: in parse
    return compile(source, filename, mode, flags,
E     File "tests/conftest.py", line 77
E       monkeypatch.setenv("USERPROFILE", str(home))  # Windows equivalent
E   IndentationError: unexpected indent


Old text:

```
    monkeypatch.setenv("HOME", str(home))

```

New text:

```
(empty)
```

### `u326.R4_live_provider_refused`

_no_live_provider_client: leave the shipped provider client factory in place, the no live provider detonator

- File: `tests/conftest.py`
- Source: `u326.json`, row `R4_live_provider_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_isolation_survives_undo.py`, `tests/test_provider_session_hold.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_catalogue_app.py`
- Collected: 273 against a baseline of 273
- Kills: 1 (killed)
- Killed:
  - `tests/test_isolation_survives_undo.py::test_every_redirect_survives_an_undo_of_the_body_s_own_patch`

Old text:

```
        monkeypatch.setattr(provider_session, "CLIENT_FACTORY", refused)
```

New text:

```
        pass
```

### `u206-b.M2b_disabled_recall_composite`

Composite: drop recall's days 0 guard AND give every entry at least a day's life, so answers kept before the cache was turned off still answer

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206-b.json`, row `M2b_disabled_recall_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 8 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_answers_kept_before_the_cache_was_turned_off_answer_nothing`
  - `tests/test_isrc_cache.py::test_zero_days_asks_every_time_and_writes_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[cache-off]`

Old text:

```
        global _PROCESS_HITS
        if not self.enabled:
            return None
```

New text:

```
        global _PROCESS_HITS
        self.days = max(self.days, 1)
```

### `u206.M13_write_without_merge`

Cache.remember: write only this entry, dropping what another process wrote since

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M13_write_without_merge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_isrc_cache.py::test_a_different_country_is_a_different_key`
  - `tests/test_isrc_cache.py::test_another_processs_answer_written_since_this_one_read_survives`
  - `tests/test_isrc_cache.py::test_two_writer_processes_leave_one_readable_file_holding_both`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
            merged = {
                name: entry for name, entry in entries.items() if self._fresh(entry, now) is not None
            }
```

New text:

```
            merged = {}
```

### `u206.M1_recall_never_hits`

Cache.recall: never answer from the file, so every lookup asks the provider again

- File: `src/cratekit/acquire/isrc_cache.py`
- Source: `u206.json`, row `M1_recall_never_hits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1130 against a baseline of 1130
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_missing_isrc.py::test_a_one_id_isrc_is_listed_and_two_ids_and_no_isrc_are_handed_on`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[catalogue]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[streamable]`
  - `tests/test_isrc_cache.py::test_a_remembered_client_track_reads_as_the_client_track_does[withdrawn]`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        held = self._fresh(entries.get(key), self.clock())
```

New text:

```
        held = None
```

