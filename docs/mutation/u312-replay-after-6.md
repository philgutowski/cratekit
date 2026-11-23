# Mutation table: u312-replay-after-6

Measured by `scripts/mutate.py` on 2026-11-23 10:42 UTC, branch `HEAD` at `55e2f3b6`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22479 collected. pytest invocations for this batch: 332.

Full baseline: measured by this driver (the battery's verdict was not read: no battery verdict at `.cloud-battery/verdict.json`).

Subset baselines: 47, each measured by this driver.

Known failures: 250 node ids whose failure is this machine's and not the tree's, read from `~/known/scratch.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries); the names directly under / (25). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots, and the names directly under the filesystem root (R-1917), are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22479 against 22479. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
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
| `u88-b.W1_replace_not_append` | `src/cratekit/write/trees.py` | user | 1 file(s) | 197 | 2 | killed |
| `r686.R1_empty_list_bare_header` | `src/cratekit/cli/render.py` | user | 2 file(s) | 1195 | 3 | killed |
| `r313.G7_handler_opens_with_write_intent` | `src/cratekit/write/routing_export.py` | user | 3 file(s) | 1612 | 1 | killed |
| `u89.L1_absent_is_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 126 | killed |
| `u91.R1_crlf_guard` | `src/cratekit/write/rbxml.py` | user | 4 file(s) | 343 | 2 | killed |
| `r316.M10_derivation_restates_no_gap` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 9 | killed |
| `r316.M8_not_derived_ignores_declaration` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 1 | killed |
| `r316.M9_not_derived_ignores_threshold` | `src/cratekit/write/rebuild.py` | user | 2 file(s) | 307 | 14 | killed |
| `u168.C3_default_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 3 | killed |
| `u168.C4_default_actor_session` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C5_given_actor_ignored` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C6_no_argv_continues` | `src/cratekit/cli/verbs/runs.py` | user | 1 file(s) | 8 | 1 | killed |
| `u168.C10_argv_never` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1006 | 5 | killed |
| `u168.C11_argv_whole_line` | `src/cratekit/cli/__init__.py` | user | 2 file(s) | 1006 | 3 | killed |
| `u168.C7_continue_without_run` | `src/cratekit/cli/verbs/runs.py` | user | 2 file(s) | 1006 | 2 | killed |
| `u168.C12_argv_not_saved` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 1013 | 5 | killed |
| `u170.D1_kept_folded` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.D2_status_week` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.D3_open_runs_short` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.D4_line_dropped` | `src/cratekit/cli/doctor.py` | user | 5 file(s) | 1716 | 3 | killed |
| `u170.G2_idle_from_start_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 3 | killed |
| `u170.G3_idle_from_write_only` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.G5_no_abort_retired` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.G8_malformed_stamp` | `src/cratekit/cli/gates.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R11_digest_ids_only` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R12_default_week` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R3_own_run` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R4_unreadable_dropped` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R5_answers_apply` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.R6_actor_cli` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.R7_declined_applies` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u170.R8_empty_asks` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 2 | killed |
| `u170.R9_kept_planned` | `src/cratekit/cli/verbs/runs.py` | user | 5 file(s) | 1716 | 1 | killed |
| `u295.S10_stuck_accepted` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 4 | killed |
| `u295.S11_no_read_back` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 1 | killed |
| `u295.S12_cleanup_ignores_launchd` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 1 | killed |
| `u295.S13_cleanup_keeps_plist` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 3 | killed |
| `u295.S14_dirs_not_resolved` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 11 | killed |
| `u295.S15_override_relative` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 1 | killed |
| `u295.S17_plist_mode` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 1 | killed |
| `u295.S18_crate_exec_bit` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 1 | killed |
| `u295.S1_platform_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 6 | killed |
| `u295.S2_root_guard` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 3 | killed |
| `u295.S3_argv_widened` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 7 | killed |
| `u295.S4_run_at_load` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 7 | killed |
| `u295.S7_user_domain` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 63 | killed |
| `u295.S8_unknown_read_absent` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 2 | killed |
| `u295.S9_skip_bootout_on_unknown` | `src/cratekit/cli/schedule.py` | user | 2 file(s) | 1094 | 1 | killed |
| `u326.R7_launchctl_refused` | `tests/conftest.py` | maintainer | 2 file(s) | 1094 | 1 | killed |
| `u138.E2_reason_exit_code` | `src/cratekit/core/cause.py` | user | 1 file(s) | 26 | 9 | killed |
| `u138.S7_verb_drops_the_answer` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 7 | killed |
| `u184.A10_summary_always_recorded` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A11_wording_swapped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A3_engine_rule_not_selected` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 9 | killed |
| `u184.A4_valid_record_minted_again` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u184.A5_expired_reported_valid` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A6_unreadable_record_refuses` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A7_already_valid_says_ok` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A8_expiry_row_dropped` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A9_expiry_row_names_the_mint` | `src/cratekit/session/cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u184.A1_flag_ignored` | `src/cratekit/session/cli.py` | user | 3 file(s) | 79 | 10 | killed |
| `u184.A2_any_actor_accepted` | `src/cratekit/session/cli.py` | user | 3 file(s) | 79 | 3 | killed |
| `u49-author.G1_an_explicit_gate_takes_an_inline_answer_again` | `src/cratekit/cli/gates.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B1_sweep_before_the_lock` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B3_orphans_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `r598-b.B4_abandon_only_reported_as_no_op` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B5_kept_reports_nothing` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u311.B2_acknowledgment_hides_what_it_showed` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A2_the_abort_mints_anyway` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A3_the_refusal_names_no_ages` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A4_the_record_on_file_is_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `u49-author.A6_the_authorisation_is_not_spent` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A7_the_check_rows_are_keyed_wrong` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `u49-author.A8_a_damaged_record_locks_the_verb_out` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B7_sample_live_holder_released` | `src/cratekit/core/session_holders.py` | user | 2 file(s) | 185 | 4 | killed |
| `r1255.S1_scan_unlisted_as_empty` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 14 | killed |
| `r1255.S2_absent_log_unread` | `src/cratekit/core/session.py` | user | 7 file(s) | 867 | 46 | killed |
| `r1255.N1_landings_of_pass_refuses` | `src/cratekit/intake/native_plan.py` | user | 2 file(s) | 84 | 2 | killed |
| `u121.S24_ack_before_gate` | `src/cratekit/intake/inspiration_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `u129-author.A19_plan_archive_always_none` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 56 | 3 | killed |
| `u121.S21_landing_skips_set` | `src/cratekit/intake/native.py` | user | 1 file(s) | 56 | 15 | killed |
| `u121.S22_record_unnamed` | `src/cratekit/intake/native.py` | user | 1 file(s) | 56 | 5 | killed |
| `u121-b.S10r_folder_row_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-b.S14r_stale_digest` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-b.S15r_member_order` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-c.S2c_separator` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 2 | killed |
| `u121-d.D1_record_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D2_removed_namesake` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 2 | killed |
| `u121-d.D3_repeated_row_counted_twice` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D4_record_on_nothing` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D5_left_dropped_when_nothing_written` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121-d.D6_recorded_but_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S11_landed_by_target` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 13 | killed |
| `u121.S17_unresolved_dropped` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 4 | killed |
| `u121.S1_uploader_prefix` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 2 | killed |
| `u121.S3_answer_not_read` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S5_missing_word` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 6 | killed |
| `u121.S7_job_handler` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u121.S9_two_folders` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 56 | 1 | killed |
| `u246.S3_set_playlist_order_set_empty` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 300 | 22 | killed |
| `u144-c.C9_parent_of_named` | `src/cratekit/intake/set_playlist.py` | user | 2 file(s) | 94 | 10 | killed |
| `u307.R17_made_on_drops_posted` | `src/cratekit/intake/set_playlist.py` | user | 3 file(s) | 114 | 1 | killed |
| `u135.A14_set_order_reverses` | `src/cratekit/intake/native.py` | user | 2 file(s) | 65 | 2 | killed |
| `r187-a.C1_blank_not_key` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `r187-a.C4_key_beside_name` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `r187-a.C5_empty_name_scans` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `r187-a.C6_no_cache_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 3 | killed |
| `u43-author-light.A1_first_track_wins` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 4 | killed |
| `u43-author-light.A3_containment_not_checked` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u43-author-light.A4_empty_anchor_defaults` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u43-author-round-2.H2_empty_is_a_no_op` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u43-author-round-2.H3_missing_root_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u43-author-round-2.V3_root_check_reports_instead_of_refusing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u98-a.U2_key_missing` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u98-b.E1_existing_containment` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 2 | killed |
| `u98-b.S1_supplied_beside_path` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 3 | killed |
| `u98-b.S2_tempo_half` | `src/cratekit/setbuilder/cli.py` | user | 1 file(s) | 80 | 1 | killed |
| `u279.M12_holder_never_found` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 339 | 2 | killed |
| `u279.M1_walk_ignores_exclude` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 339 | 10 | killed |
| `u279.M2_excluded_folder_walked` | `src/cratekit/modules/tools/setbuilder.py` | user | 4 file(s) | 339 | 10 | killed |
| `u279.M10_tilde_not_expanded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 339 | 1 | killed |
| `u279.M11_excluded_anchor_not_refused` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 339 | 2 | killed |
| `u279.M13_wrong_folder_named` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 339 | 1 | killed |
| `u279.M8_index_call_unexcluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 339 | 6 | killed |
| `u279.M9_staging_not_excluded` | `src/cratekit/setbuilder/cli.py` | user | 4 file(s) | 339 | 4 | killed |
| `u266.M1_seven_opens_again` | `src/cratekit/modules/tools/setbuilder.py` | user | 3 file(s) | 324 | 52 | killed |
| `u283.S15_nothing_entered_fails` | `src/cratekit/cli/setup.py` | user | 2 file(s) | 476 | 2 | killed |
| `u28-skills-independent.K1_composite` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 11 | killed |
| `u28-skills-independent.S14_into_ignored` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 10 | killed |
| `u28-skills-independent.S15_drift_never_warns` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S16_counts_miscounted` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `u28-skills-independent.S18_detail_reworded` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 1 | killed |
| `u28-skills-independent.S5_stamp_quote_strip` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 7 | killed |
| `u28-skills-independent.S9_previous_always_none` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 5 | killed |
| `u311.D1_stamp_name_unstripped` | `src/cratekit/skills/cli.py` | user | 1 file(s) | 16 | 8 | killed |
| `r1890.P12_accessor_held_off_the_naming_convention` | `src/cratekit/core/convergence.py` | maintainer | 1 file(s) | 5 | 1 | killed |
| `u293.S1_reentrant` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 6 | killed |
| `u293.S2_second_holder_refused` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 5 | killed |
| `r359.M5_unwired` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M6_no_append` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r359.M7_note_before_describe` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r504-b.B10_check_no_numbers` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B7_sync_drops_short` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B8_check_passes` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `r504-b.B9_all_withheld_says_no_hearts` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `r515-operator.S13_sweep_no_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A1_plan_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u109-a.A2_guided_empty` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 6 | killed |
| `u109-a.A3_no_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A4_summary_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u109-a.A5_gate_guided` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A6_refusal_step_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u109-a.A7_refusal_step_first` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u109-a.A8_row_reworded` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u73-c.C3_next_only_with_intake_jobs` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 5 | killed |
| `u73-c.C4_next_counts_intake_jobs_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u73-c.C5_next_check_row` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B10_refused_check_status` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B11_gate_screen` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B12_next_step_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B1_source_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 9 | killed |
| `u74-b.B2_compose_skips_inbound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 16 | killed |
| `u74-b.B3_queue_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74-b.B4_filed_outbound_only` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B5_inbound_refusal_not_counted` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B6_inbound_warning` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74-b.B7_block_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 13 | killed |
| `u74-b.B8_check_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 10 | killed |
| `u74-b.B9_check_wording` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A10_export_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 15 | killed |
| `u74.A11_queue_not_bound` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 17 | killed |
| `u74.A12_run_id_dropped` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A3_handler_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A4_source_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A5_library_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 1 | killed |
| `u74.A6_open_filter` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 3 | killed |
| `u74.A7_in_flight_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 2 | killed |
| `u74.A8_empty_guard` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 4 | killed |
| `u74.A9_listing_refusal_raised` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 115 | 19 | killed |
| `r358.S1_set_is_the_cursor` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 2 | killed |
| `r358.S5_recheck_is_a_second_read` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 3 | killed |
| `r358.S7_lazy_listing` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 1 | killed |
| `r358.S9_mark_always_applied` | `src/cratekit/sync/playlists.py` | user | 1 file(s) | 115 | 4 | killed |
| `r1289.M10_warning_ready_filter` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 1 | killed |
| `r1289.M11_warning_absent` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M12_warning_promise` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M13_warning_names` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `u109-b.B1_labels_not_guided` | `src/cratekit/sync/sources.py` | user | 3 file(s) | 228 | 13 | killed |
| `u109-b.B2_command_spelling` | `src/cratekit/sync/sources.py` | user | 2 file(s) | 197 | 9 | killed |
| `r1289.M1_sweep_reads_whole` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 6 | killed |
| `r1289.M2_unread_not_kept` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 5 | killed |
| `r1289.M3_all_unread_branch` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
| `r1289.M4_unread_why_dropped` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r1289.M5_all_unread_message` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M6_report_unread_emptied` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 4 | killed |
| `r1289.M7_per_playlist_reraise` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M8_per_playlist_set` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 1 | killed |
| `r1289.M9_short_check` | `src/cratekit/sync/playlists.py` | user | 3 file(s) | 215 | 2 | killed |
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
| `u179.N1_one_label_only_when_all_named` | `src/cratekit/intake/batch_name.py` | user | 3 file(s) | 54 | 3 | killed |
| `u179.T4_commands_quoted` | `src/cratekit/cli/tail.py` | user | 4 file(s) | 215 | 3 | killed |
| `u179.P1_shared_preflight` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 104 | 3 | killed |
| `u179.T2_rehearsal_ack_attends` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
| `u179.T3_rehearsal_stop_wording` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 214 | 1 | killed |
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
| `u183.M6_unreadable_record` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M7_remember_saves` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 1 | killed |
| `u183.M8_remember_called` | `src/cratekit/cli/sync_land.py` | user | 1 file(s) | 71 | 5 | killed |
| `u165.F5_report_failed` | `src/cratekit/intake/filing.py` | user | 1 file(s) | 22479 | 0 (promoted) | zero |
| `u181.S1_profile_off_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1069 | 1 | killed |
| `u181.S2_gate_never_asked` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 1069 | 6 | killed |
| `r1115.S1_sync_land_stops_on_unsettled` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `r1115.S2_sync_land_names_the_refused` | `src/cratekit/cli/sync_land.py` | user | 2 file(s) | 93 | 2 | killed |
| `u183.M17_record_read_back` | `src/cratekit/cli/gates.py` | user | 3 file(s) | 86 | 7 | killed |
| `u181.T5_rescore_never_run` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 4 | killed |
| `u181.T6_plan_warnings_not_lifted` | `src/cratekit/cli/tail.py` | user | 2 file(s) | 181 | 1 | killed |
| `u181.T2_rescore_ignores_profile` | `src/cratekit/cli/tail.py` | user | 3 file(s) | 215 | 30 | killed |
| `u152.R13_missing_lift` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R14_download_list_match` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R15_download_newest` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R16_download_cancelled` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R17_download_retry` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R20_nothing_downloaded` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 2 | killed |
| `u152.R2_preflight_backup` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R6_lift_failed_checks` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 2 | killed |
| `u152.R7_outbound_held` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 2 | killed |
| `u152.R8_continue_open_pass` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u152.R9_open_passes_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 1184 | 1 | killed |
| `u227.R15_way_on_wording` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R19_take_library` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R20_take_source` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 2 | killed |
| `u227.R21_take_continued` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |
| `u227.R22_take_not_driven` | `src/cratekit/cli/sync_land.py` | user | 3 file(s) | 96 | 1 | killed |

## Zero rows and what they owe

- `u165.F5_report_failed` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

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

### `r686.R1_empty_list_bare_header`

An empty collection in a gate's context renders as a bare header again

- File: `src/cratekit/cli/render.py`
- Source: `r686.json`, row `R1_empty_list_bare_header`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`
- Collected: 1195 against a baseline of 1195
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

### `r313.G7_handler_opens_with_write_intent`

the unplaced report opens the database with require_closed, so it refuses with rekordbox open

- File: `src/cratekit/write/routing_export.py`
- Source: `r313.json`, row `G7_handler_opens_with_write_intent`
- Moved: Anchored where u302-replay-after-a.json replayed it: the same text, now in src/cratekit/write/routing_export.py, was in src/cratekit/write/routing_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_cli_contract.py`, `tests/test_doctor.py`
- Collected: 1612 against a baseline of 1612
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

### `r316.M10_derivation_restates_no_gap`

derive_from_taxonomy stops calling not_derived and reports no gaps, so the resume and the derivation disagree

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M10_derivation_restates_no_gap`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 307 against a baseline of 307
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

### `r316.M8_not_derived_ignores_declaration`

not_derived names the vocal gap whether or not the taxonomy declares an additive sub-playlist

- File: `src/cratekit/write/rebuild.py`
- Source: `r316.json`, row `M8_not_derived_ignores_declaration`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_rebuild.py`
- Collected: 307 against a baseline of 307
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
- Collected: 307 against a baseline of 307
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

### `u168.C10_argv_never`

_dispatched: never record the command line

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C10_argv_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1006 against a baseline of 1006
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_a_continuation_that_refuses_answers_with_its_refusal_and_keeps_the_answer`
  - `tests/test_run_decide_continue.py::test_a_session_answers_and_mints_in_one_command_with_no_actor_given`
  - `tests/test_run_decide_continue.py::test_the_continuation_is_given_the_arguments_its_first_invocation_recorded`

Old text:

```
        if not args.run:
            state.argv = _verb_argv(argv, entry)
```

New text:

```
        if False:
            state.argv = _verb_argv(argv, entry)
```

### `u168.C11_argv_whole_line`

_verb_argv: keep the global options before the verb

- File: `src/cratekit/cli/__init__.py`
- Source: `u168.json`, row `C11_argv_whole_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1006 against a baseline of 1006
- Kills: 3 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_the_continuation_is_given_the_arguments_its_first_invocation_recorded`

Old text:

```
            return tuple(tokens[index:])
```

New text:

```
            return tuple(tokens)
```

### `u168.C7_continue_without_run`

_continued: dispatch the verb again without --run, as a new run

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u168.json`, row `C7_continue_without_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`
- Collected: 1006 against a baseline of 1006
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

### `u168.C12_argv_not_saved`

RunState.to_json: drop the command line from the saved record

- File: `src/cratekit/cli/gates.py`
- Source: `u168.json`, row `C12_argv_not_saved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_decide_continue.py`, `tests/test_cli_contract.py`, `tests/test_gate_pins.py`
- Collected: 1013 against a baseline of 1013
- Kills: 5 (killed)
- Killed:
  - `tests/test_cli_contract.py::test_a_run_continued_by_hand_keeps_the_command_line_its_first_invocation_recorded`
  - `tests/test_cli_contract.py::test_run_decide_continue_resumes_the_owning_verb_with_its_own_arguments`
  - `tests/test_run_decide_continue.py::test_a_continuation_that_refuses_answers_with_its_refusal_and_keeps_the_answer`
  - `tests/test_run_decide_continue.py::test_a_session_answers_and_mints_in_one_command_with_no_actor_given`
  - `tests/test_run_decide_continue.py::test_the_continuation_is_given_the_arguments_its_first_invocation_recorded`

Old text:

```
        if self.argv is not None:
            record["argv"] = list(self.argv)
```

New text:

```
        if False:
            record["argv"] = list(self.argv)
```

### `u170.D1_kept_folded`

status: fold every old gate, the kept ones too

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D1_kept_folded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`

Old text:

```
            if aged is not None and aged.retirable:
```

New text:

```
            if aged is not None:
```

### `u170.D2_status_week`

status: threshold fixed at seven days, not the file's

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D2_status_week`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`

Old text:

```
    runs, folded = _run_report(timedelta(days=cfg.reports.open_gate_stale_days))
```

New text:

```
    runs, folded = _run_report(timedelta(days=7))
```

### `u170.D3_open_runs_short`

status: open_runs leaves the folded gates out

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D3_open_runs_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`

Old text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")) + folded,
```

New text:

```
            "open_runs": sum(1 for f in findings if f.key.startswith("run.")),
```

### `u170.D4_line_dropped`

status: fold the gates and print no line for them

- File: `src/cratekit/cli/doctor.py`
- Source: `u170.json`, row `D4_line_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_status_collapses_old_gates_into_one_line_and_lists_new_ones_as_before`
  - `tests/test_run_retire.py::test_status_reads_the_threshold_from_the_file`
  - `tests/test_run_retire.py::test_the_collapsed_line_names_the_dates_it_spans_and_reaches_a_person`

Old text:

```
    if old and older_than is not None:
```

New text:

```
    if False:
```

### `u170.G2_idle_from_start_only`

idle_since: age from created alone, so a resumed run is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G2_idle_from_start_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 3 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_gate_exactly_at_the_threshold_is_not_yet_old`
  - `tests/test_run_retire.py::test_a_run_resumed_recently_is_not_old_however_long_ago_it_started`
  - `tests/test_run_retire.py::test_an_answer_is_stale_once_a_planned_run_is_resumed_even_if_it_stays_old`

Old text:

```
    return written if started is None else max(started, written)
```

New text:

```
    return written if started is None else started
```

### `u170.G3_idle_from_write_only`

idle_since: age from the record's write alone, so a copied record with an old date is old

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G3_idle_from_write_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_run_started_recently_is_not_old_whatever_its_file_says`

Old text:

```
    return written if started is None else max(started, written)
```

New text:

```
    return written
```

### `u170.G5_no_abort_retired`

old_gate: drop the no abort refusal, so sync.pair gates are planned

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G5_no_abort_retired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 2 (killed)
- Killed:
  - `tests/test_run_retire.py::test_an_old_gate_the_command_would_keep_is_listed_and_never_collapsed`
  - `tests/test_run_retire.py::test_retire_lists_what_it_retired_and_what_it_kept`

Old text:

```
    elif RETIRE_OPTION not in spec.options:
```

New text:

```
    elif False:
```

### `u170.G8_malformed_stamp`

_instant: a malformed created stamp raises instead of reading as unknown

- File: `src/cratekit/cli/gates.py`
- Source: `u170.json`, row `G8_malformed_stamp`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
- Kills: 1 (killed)
- Killed:
  - `tests/test_run_retire.py::test_a_hand_edited_start_stamp_is_aged_by_the_records_last_write`

Old text:

```
    except (TypeError, ValueError):
        return None
    return moment if
```

New text:

```
    except TypeError:
        return None
    return moment if
```

### `u170.R11_digest_ids_only`

retire: digest the planned run ids alone, not when each went idle

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R11_digest_ids_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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

### `u170.R3_own_run`

old_gates: plan the asking run too

- File: `src/cratekit/cli/verbs/runs.py`
- Source: `u170.json`, row `R3_own_run`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_run_retire.py`, `tests/test_doctor.py`, `tests/test_cli_contract.py`, `tests/test_config.py`, `tests/test_run_decide_continue.py`
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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
- Collected: 1716 against a baseline of 1716
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

### `u295.S10_stuck_accepted`

_boot_out: accept an agent still loaded after its bootout

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S10_stuck_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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

### `u295.S17_plist_mode`

PLIST_MODE: the plist readable by everyone on the Mac

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S17_plist_mode`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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

### `u295.S1_platform_guard`

_macos_only: never refuse another platform, so a schedule is attempted where there is no launchd

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S1_platform_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1094 against a baseline of 1094
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

### `u295.S2_root_guard`

_as_the_person: never refuse root, so the agent is bootstrapped into gui/0

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S2_root_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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

### `u295.S7_user_domain`

_domain: load into user/<uid> instead of the person's GUI login

- File: `src/cratekit/cli/schedule.py`
- Source: `u295.json`, row `S7_user_domain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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
- Collected: 1094 against a baseline of 1094
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

### `u326.R7_launchctl_refused`

_no_live_launchd: leave the shipped launchctl seam in place, so a verb on a platform read as the Mac reaches launchd

- File: `tests/conftest.py`
- Source: `u326.json`, row `R7_launchctl_refused`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_schedule.py`, `tests/test_cli_contract.py`
- Collected: 1094 against a baseline of 1094
- Kills: 1 (killed)
- Killed:
  - `tests/test_schedule.py::test_the_suite_stands_launchd_in_for_every_test`

Old text:

```
        monkeypatch.setattr(schedule, "launchctl", refused)
```

New text:

```
        pass
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

### `u138.S7_verb_drops_the_answer`

The verb never hands down who answered the gate

- File: `src/cratekit/session/cli.py`
- Source: `u138.json`, row `S7_verb_drops_the_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 7 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_person_at_a_terminal_mints_by_the_terminal_rule_and_the_record_says_so`
  - `tests/test_session_ack_by_session.py::test_a_session_with_a_terminal_is_still_held_to_the_ages`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-exactly-five]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-never-recorded]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[database-recorded-in-the-future]`
  - `tests/test_session_ack_by_session.py::test_the_session_is_refused_naming_the_portion_over_five_days_or_unknown[files-six-days]`
  - `tests/test_session_ack_by_session.py::test_the_session_mints_with_no_terminal_when_both_ages_are_under_five_days`

Old text:

```
        cfg, now=now, decided_by=answered.actor if answered is not None else None

```

New text:

```
        cfg, now=now, decided_by=None

```

### `u184.A10_summary_always_recorded`

_summary: say recorded whether or not this call minted

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A10_summary_always_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        "recorded": minted,
```

New text:

```
        "recorded": True,
```

### `u184.A11_wording_swapped`

_expiry_row: swap the two phrasings, so a mint reads as already on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A11_wording_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    said = "recorded now" if minted else "already on record, not minted again"
```

New text:

```
    said = "already on record, not minted again" if minted else "recorded now"
```

### `u184.A3_engine_rule_not_selected`

_mint_as_session: hand no actor to the engine, so the terminal rule decides and the ages are not judged

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A3_engine_rule_not_selected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 9 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
        cfg, now=now, decided_by=session.SESSION_ACTOR
    )
```

New text:

```
        cfg, now=now, decided_by=None
    )
```

### `u184.A4_valid_record_minted_again`

_mint_as_session: never report a valid acknowledgment, so every call mints a fresh one

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A4_valid_record_minted_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if False:
```

### `u184.A5_expired_reported_valid`

_mint_as_session: drop the window check, so an expired acknowledgment is reported as on record

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A5_expired_reported_valid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`

Old text:

```
    if recorded is not None and recorded.valid_at(now):
```

New text:

```
    if recorded is not None:
```

### `u184.A6_unreadable_record_refuses`

_mint_as_session: let an unreadable record raise, so a damaged file can never be replaced by the session

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A6_unreadable_record_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`

Old text:

```
    except CratekitError:
        recorded = None
```

New text:

```
    except CratekitError:
        raise
```

### `u184.A7_already_valid_says_ok`

_mint_as_session: report an existing acknowledgment as an ok run rather than a no op

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A7_already_valid_says_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.NO_OP,
```

New text:

```
                "summary": _summary(recorded, minted=False),
            },
            outcome=Outcome.OK,
```

### `u184.A8_expiry_row_dropped`

_mint_as_session: leave the expiry row out of a mint, so a person at a terminal is never shown it

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A8_expiry_row_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
                _expiry_row(acknowledgment, minted=True),
```

New text:

```
(empty)
```

### `u184.A9_expiry_row_names_the_mint`

_expiry_row: name the moment recorded where the expiry belongs

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A9_expiry_row_names_the_mint`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`

Old text:

```
            f"{acknowledgment.expires_at.isoformat()}"
```

New text:

```
            f"{acknowledgment.recorded_at.isoformat()}"
```

### `u184.A1_flag_ignored`

record_ack: never take the session road, so --as session falls to the gate and leaves a run waiting

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A1_flag_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 79 against a baseline of 79
- Kills: 10 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_a_valid_acknowledgment_a_person_minted_is_reported_over_old_backups`
  - `tests/test_session_ack_by_session.py::test_an_expired_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_an_unreadable_acknowledgment_is_replaced_by_one_command`
  - `tests/test_session_ack_by_session.py::test_one_command_mints_as_the_session_when_both_ages_are_four_days`
  - `tests/test_session_ack_by_session.py::test_one_command_prints_the_expiry_a_person_reads`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[both-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[database-unknown]`
  - `tests/test_session_ack_by_session.py::test_one_command_refuses_naming_the_portion_and_records_nothing[files-five-days]`
  - `tests/test_session_ack_by_session.py::test_one_command_reports_a_valid_acknowledgment_and_does_not_mint_again`

Old text:

```
    if getattr(ctx.args, "as_actor", None) == session.SESSION_ACTOR:
```

New text:

```
    if False:
```

### `u184.A2_any_actor_accepted`

build_ack: drop the one value restriction, so --as names any actor and is parsed

- File: `src/cratekit/session/cli.py`
- Source: `u184.json`, row `A2_any_actor_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_ack_by_session.py`, `tests/test_crate_sync_skill.py`, `tests/test_rekordbox_visit_skill.py`
- Collected: 79 against a baseline of 79
- Kills: 3 (killed)
- Killed:
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[Session]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[a-person]`
  - `tests/test_session_ack_by_session.py::test_the_flag_names_no_actor_but_the_session[cli]`

Old text:

```
        choices=(session.SESSION_ACTOR,),
```

New text:

```
        choices=None,
```

### `u49-author.G1_an_explicit_gate_takes_an_inline_answer_again`

Restore the recorded-is-None qualifier this unit removed, so a flag can overturn a recorded abort and mint the acknowledgment

- File: `src/cratekit/cli/gates.py`
- Source: `u49-author.json`, row `G1_an_explicit_gate_takes_an_inline_answer_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`

Old text:

```
        if inline is not None and spec.explicit:
```

New text:

```
        if inline is not None and spec.explicit and recorded is None:
```

### `r598-b.B1_sweep_before_the_lock`

release_lock: abandon the orphans before releasing the lock, so a live holder's refusal arrives after records were already ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B1_sweep_before_the_lock`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[live-lock-holder]`

Old text:

```
    cleared = session.release_stale_lock(cfg)
    abandoned = [
```

New text:

```
    abandoned_first = session.abandon_orphaned_sessions(cfg)
    cleared = session.release_stale_lock(cfg)
    abandoned = [record.session_id for record in abandoned_first] + [
```

### `r598-b.B3_orphans_not_shown`

release_lock: show an empty orphan list at the gate, so the person decides without seeing what will be ended

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B3_orphans_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[hard-kill]`
  - `tests/test_session_cli.py::test_a_cut_off_gated_write_blocks_cutover_until_release_abandons_it[power-loss]`

Old text:

```
                for record in orphans
            ],
```

New text:

```
                for record in orphans[:0]
            ],
```

### `r598-b.B4_abandon_only_reported_as_no_op`

release_lock: report a release that only abandoned records as a no-op, telling a person nothing changed

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B4_abandon_only_reported_as_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_release_that_only_abandons_is_a_change_and_passes_the_contract`

Old text:

```
            outcome=Outcome.OK if abandoned else Outcome.NO_OP,
```

New text:

```
            outcome=Outcome.NO_OP,
```

### `r598-b.B5_kept_reports_nothing`

release_lock: report no kept records, hiding an open record the verb deliberately left

- File: `src/cratekit/session/cli.py`
- Source: `r598-b.json`, row `B5_kept_reports_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[alive]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_not_proven_dead_on_this_machine_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`

Old text:

```
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
```

New text:

```
    kept = []
```

### `u311.B2_acknowledgment_hides_what_it_showed`

Both mints report an acknowledgment without the ages it was shown

- File: `src/cratekit/session/cli.py`
- Source: `u311.json`, row `B2_acknowledgment_hides_what_it_showed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_second_mint_replaces_the_record_and_moves_the_window`

Old text:

```
        "shown": [entry.to_json() for entry in acknowledgment.shown],
```

New text:

```
        "shown": [],
```

### `u49-author.A2_the_abort_mints_anyway`

Drop the abort branch in record_ack, so a person who declines gets an acknowledgment

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A2_the_abort_mints_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_an_inline_answer_cannot_overturn_a_recorded_abort`
  - `tests/test_session_cli.py::test_answering_abort_records_nothing_and_says_so`

Old text:

```
    if option == "abort":
        return ctx.envelope(
            data={"checks": [], "summary": {"recorded": False, "ages": shown}},
            outcome=Outcome.NO_OP,
        )

```

New text:

```
(empty)
```

### `u49-author.A3_the_refusal_names_no_ages`

Drop the context argument from the ack gate, so the refusal asks the question over nothing

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A3_the_refusal_names_no_ages`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_a_person_at_a_terminal_reads_the_ages_and_not_only_a_json_consumer`
  - `tests/test_session_cli.py::test_the_refusal_before_acknowledging_names_the_ages_it_consulted`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
    option = ctx.gate.require(
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
    )
```

New text:

```
    option = ctx.gate.require(spec)
```

### `u49-author.A4_the_record_on_file_is_not_shown`

Show the ages but not the acknowledgment already on record, so a person cannot see whether they are covered

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A4_the_record_on_file_is_not_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`
  - `tests/test_session_cli.py::test_the_refusal_names_the_acknowledgment_on_record_in_all_three_states`

Old text:

```
        spec, context={"ages": shown, "acknowledgment": _on_record(cfg, now)}
```

New text:

```
        spec, context={"ages": shown}
```

### `u49-author.A6_the_authorisation_is_not_spent`

Leave the recorded decision in place after the mint, so one run id re-mints the acknowledgment forever (R-217's defect restored)

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A6_the_authorisation_is_not_spent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_spent_acknowledgment_decision_cannot_be_replayed`

Old text:

```
    ctx.run.decisions.pop(spec.name, None)
```

New text:

```
(empty)
```

### `u49-author.A7_the_check_rows_are_keyed_wrong`

Key the ack check rows by name rather than key, so the human check table prints a question mark where the portion should be

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A7_the_check_rows_are_keyed_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_the_check_rows_a_person_reads_name_the_portion`

Old text:

```
                    "key": f"backup.age.{entry['portion']}",
```

New text:

```
                    "name": f"backup.age.{entry['portion']}",
```

### `u49-author.A8_a_damaged_record_locks_the_verb_out`

Let the display read of the acknowledgment raise, so a corrupt record makes the one verb that replaces it refuse

- File: `src/cratekit/session/cli.py`
- Source: `u49-author.json`, row `A8_a_damaged_record_locks_the_verb_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_damaged_acknowledgment_record_can_still_be_replaced`

Old text:

```
    try:
        recorded = session.read_acknowledgment(cfg)
    except CratekitError as exc:
        return {"unreadable": exc.cause.message}
```

New text:

```
    recorded = session.read_acknowledgment(cfg)
```

### `r598-b.B7_sample_live_holder_released`

release_stale_lock: skip the live holder refusal (existing guard, sampled because the sweep now sits behind it)

- File: `src/cratekit/core/session_holders.py`
- Source: `r598-b.json`, row `B7_sample_live_holder_released`
- Moved: Anchored where u300-replay-after-b.json replayed it: the same text, now in src/cratekit/core/session_holders.py, was in src/cratekit/core/session.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_cli.py`, `tests/test_write_session.py`
- Collected: 185 against a baseline of 185
- Kills: 4 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_live_holders_claim_is_refused_and_the_lock_file_is_untouched`
  - `tests/test_session_cli.py::test_a_refused_or_aborted_release_abandons_nothing[live-lock-holder]`
  - `tests/test_write_session.py::test_a_live_holder_this_platform_will_not_describe_is_assumed_alive`
  - `tests/test_write_session.py::test_the_lock_left_by_another_machine_with_this_host_name_is_not_releasable`

Old text:

```
    if holder_alive(recorded):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r1255.S1_scan_unlisted_as_empty`

scan_log: answer a log it is refused as no record and none unread, the defect itself

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S1_scan_unlisted_as_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 14 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_session_log_this_account_cannot_list_is_failed_by_its_own_check`
  - `tests/test_doctor.py::test_status_names_a_session_log_it_cannot_list_and_still_reports_the_rest`
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_a_listed_log_is_read_a_missing_one_is_no_record_and_a_file_in_its_place_is_unread`
  - `tests/test_session_log_unlisted.py::test_a_log_that_cannot_be_listed_is_the_one_unread_entry_and_its_clause_says_so`
  - `tests/test_session_log_unlisted.py::test_every_destructive_session_is_refused_at_its_gate`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[closed-detail1-<lambda>-2026-10-20 Tidal playlists 2-so no batch name can be called free]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[committed-unverified-None-<lambda>-session-committed-unverified-cannot vouch that no session ended unresolved]`
  - `tests/test_session_log_unlisted.py::test_every_gate_refuses_a_log_it_cannot_list[open-None-<lambda>-readable2-so whether a run is still open was not established]`
  - `tests/test_session_log_unlisted.py::test_restore_list_and_run_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_check_refuses_an_unknown_landing_naming_the_listing`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), (directory,)
```

New text:

```
        logger.debug("session log %s could not be listed: %s", directory, exc)
        return (), ()
```

### `r1255.S2_absent_log_unread`

_listed: read a log that is not there as refused, so a library with no session refuses every write

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S2_absent_log_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_intake_shelve.py`, `tests/test_tree_registry.py`, `tests/test_doctor.py`, `tests/test_restore.py`, `tests/test_write_session.py`
- Collected: 867 against a baseline of 867
- Kills: 46 (killed)
- Killed:
  - `tests/test_doctor.py::test_a_green_doctor_exits_zero`
  - `tests/test_doctor.py::test_a_headless_machine_that_opted_into_the_environment_fallback_is_not_red`
  - `tests/test_doctor.py::test_a_library_with_no_sessions_still_reports_a_clean_log`
  - `tests/test_doctor.py::test_a_re_run_repairs_a_spelled_remote_rclone_does_not_know`
  - `tests/test_doctor.py::test_a_second_setup_run_asks_nothing_and_changes_nothing_it_was_not_asked_to`
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_doctor.py::test_no_ok_detail_claims_a_volume_the_run_never_identified`
  - `tests/test_doctor.py::test_the_backup_flags_are_recorded_without_a_question`
  - `tests/test_doctor.py::test_the_disagreeing_remote_refusal_names_the_flag_and_the_flag_repairs_it`
  - `tests/test_doctor.py::test_the_strong_claim_survives_where_the_identity_really_was_compared`
  - `tests/test_doctor.py::test_the_wizard_on_a_clean_machine_produces_a_valid_config_and_a_green_doctor`
  - `tests/test_inbox_unmirrored.py::test_a_dated_playlist_with_no_batch_folder_still_says_so`
  - `tests/test_inbox_unmirrored.py::test_an_absent_session_log_is_no_record_at_all`
  - `tests/test_inbox_unmirrored.py::test_the_live_batches_name_every_other_node_under_inbox_with_its_kind`
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - ... and 31 more, see the JSON sidecar

Old text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        return None
```

New text:

```
        return os.listdir(directory)
    except FileNotFoundError:
        raise
```

### `r1255.N1_landings_of_pass_refuses`

native.landings_of_pass: drop the unread half again, so sync mark says a recorded landing never committed

- File: `src/cratekit/intake/native_plan.py`
- Source: `r1255.json`, row `N1_landings_of_pass_refuses`
- Moved: Anchored where u307-replay-after-a.json replayed it: the same text, now in src/cratekit/intake/native_plan.py, was in src/cratekit/intake/native.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_sync_mark.py`
- Collected: 84 against a baseline of 84
- Kills: 2 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_sync_mark.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_landing`

Old text:

```
    land the pass again.
    """
    records = session.records(cfg)
```

New text:

```
    land the pass again.
    """
    records = session.scan_log(cfg)[0]
```

### `u121.S24_ack_before_gate`

intake_inspiration: the backup acknowledgment is not read before the gate

- File: `src/cratekit/intake/inspiration_cli.py`
- Source: `u121.json`, row `S24_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)
```

New text:

```
    pass
```

### `u129-author.A19_plan_archive_always_none`

A set landing never plans the account archive

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A19_plan_archive_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`

Old text:

```
    try:
        return set_cli.plan_archive_named(cfg, name, pass_name=pass_name)
    except CratekitError:
        # Soft: the landing still lands; archive can run later via export archive.
        return None

```

New text:

```
    return None

```

### `u121.S21_landing_skips_set`

apply_rows: the landing's commit never writes the set playlist

- File: `src/cratekit/intake/native.py`
- Source: `u121.json`, row `S21_landing_skips_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 15 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[flag]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[page]`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`
  - `tests/test_set_inspiration_playlist.py::test_when_every_landed_members_file_is_refused_the_left_list_names_them`

Old text:

```
            if plan.set_playlist is not None:
```

New text:

```
            if False:
```

### `u121.S22_record_unnamed`

_record_landing_commit: the set playlist is not named on the record

- File: `src/cratekit/intake/native.py`
- Source: `u121.json`, row `S22_record_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    if set_written is not None and plan.set_playlist is not None:
```

New text:

```
    if False:
```

### `u121-b.S10r_folder_row_removed`

_folder_row: a folder rekordbox removed since the plan is still written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S10r_folder_row_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_engine_refuses_a_folder_removed_after_the_plan_even_with_no_gate_in_front`

Old text:

```
        if row is None or rb_writer.node_removed(row):
```

New text:

```
        if row is None:
```

### `u121-b.S14r_stale_digest`

apply_alone: a plan whose digest moved since the approval is written anyway

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S14r_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_engine_refuses_a_plan_whose_collection_moved_even_with_no_gate_in_front`

Old text:

```
    if again.digest != plan.digest:
```

New text:

```
    if False:
```

### `u121-b.S15r_member_order`

_members: members in title order rather than set order

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S15r_member_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`

Old text:

```
    return tuple(members), tuple(left)
```

New text:

```
    return tuple(sorted(members, key=lambda one: one.title)), tuple(left)
```

### `u121-c.S2c_separator`

_without_leading: keep the separator after the uploader's name

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-c.json`, row `S2c_separator`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`

Old text:

```
    stripped = re.sub(r"^\s*(?:[-:|\u2013\u2014]+\s*)?", "", rest)
```

New text:

```
    stripped = rest.strip()
```

### `u121-d.D1_record_ignored`

plan_for_landing: the playlist an earlier landing recorded for the job is never read, so a second day makes a twin

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D1_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
    recorded = recorded_playlist(cfg, db, job.job_id, folder_id)
    staged = [source for source, _target in files]
```

New text:

```
    recorded = None
    staged = [source for source, _target in files]
```

### `u121-d.D2_removed_namesake`

_playlist_row: a removed playlist of the name under the folder is written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D2_removed_namesake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`

Old text:

```
        if rb_writer.is_folder(row) or rb_writer.node_removed(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if rb_writer.is_folder(row):
            continue
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

### `u121-d.D3_repeated_row_counted_twice`

write_members: two reports resolving to one row count as two members

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D3_repeated_row_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_rows_of_the_set_resolving_to_one_track_are_one_member`

Old text:

```
    distinct = tuple(dict.fromkeys(ids))
```

New text:

```
    distinct = tuple(ids)
```

### `u121-d.D4_record_on_nothing`

_record_set_commit: a rerun that added nothing still records the folder committed

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D4_record_on_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`

Old text:

```
    if not (written.added or written.playlist_created or written.folder_created):
        return

```

New text:

```
(empty)
```

### `u121-d.D5_left_dropped_when_nothing_written`

write_members: the members whose files did not land are dropped from the left list when nothing is written

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D5_left_dropped_when_nothing_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_when_every_landed_members_file_is_refused_the_left_list_names_them`

Old text:

```
            members=0,
            added=0,
            left=(*left, *plan.left),
        )
```

New text:

```
            members=0,
            added=0,
            left=tuple(plan.left),
        )
```

### `u121-d.D6_recorded_but_removed`

recorded_playlist: a recorded playlist rekordbox removed is still the one added to

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-d.json`, row `D6_recorded_but_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`

Old text:

```
            or rb_writer.node_removed(row)
            or str(getattr(row, "ParentID", "") or "") != folder_id
```

New text:

```
            or str(getattr(row, "ParentID", "") or "") != folder_id
```

### `u121.S11_landed_by_target`

write_members: a landed member's row is not looked up by its target

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S11_landed_by_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 13 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[flag]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[page]`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        held = one.content_id or rows.get(one.target, "")
```

New text:

```
        held = one.content_id
```

### `u121.S17_unresolved_dropped`

_members: a downloaded row tied to nothing is dropped silently rather than listed

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S17_unresolved_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 4 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_set_with_nothing_owned_or_landed_writes_no_playlist_and_says_so`
  - `tests/test_set_inspiration_playlist.py::test_an_unanswered_question_is_left_out_and_the_plan_offers_nothing`
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_over_a_set_with_nothing_owned_asks_and_then_writes_nothing`

Old text:

```
        if not paths:
            left.append(Left(position, artist, title, state, NOT_RESOLVED))
            continue
        if how == LANDED:
```

New text:

```
        if not paths:
            continue
        if how == LANDED:
```

### `u121.S1_uploader_prefix`

_without_leading: never take the uploader's name off the front of the page title

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S1_uploader_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`

Old text:

```
    if head.casefold() != dj.casefold():
```

New text:

```
    if True:
```

### `u121.S3_answer_not_read`

_LibraryView.resolve: a person's review answer is never read back, a question stays one

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S3_answer_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`

Old text:

```
        if found.state is not match.MatchState.NEEDS_REVIEW:
            return found
```

New text:

```
        if True:
            return found
```

### `u121.S5_missing_word`

words_for: a missing word is not refused, the name is made with a hole

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S5_missing_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 6 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page0-flags0-missing0]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page1-flags1-missing1]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page2-flags2-missing2]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page3-flags3-missing3]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page4-flags4-missing4]`

Old text:

```
    if missing:
```

New text:

```
    if False:
```

### `u121.S7_job_handler`

set_job_or_refuse: accept a playlist job as a set

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S7_job_handler`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_playlist_job_named_with_set_is_refused_before_anything_moves`

Old text:

```
    if job.handler_key != SET_KEY:
```

New text:

```
    if False:
```

### `u121.S9_two_folders`

folder_for: two root folders of the name pass, the first is taken

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S9_two_folders`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_two_root_folders_of_the_name_are_refused_rather_than_one_chosen`

Old text:

```
    if len(live) > 1:
```

New text:

```
    if len(live) > 2:
```

### `u246.S3_set_playlist_order_set_empty`

assert_read_back (set playlist): an empty set of wanted ids, so a filled playlist always reads as out of order and refuses

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S3_set_playlist_order_set_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 300 against a baseline of 300
- Kills: 22 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name`
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[not-renamed]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope[raised]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[flag]`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_names_the_playlist_for_the_posted_day[page]`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - ... and 7 more, see the JSON sidecar

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set()
```

### `u144-c.C9_parent_of_named`

Sample of an existing U121 guard, now shared: take a live playlist of the name under any parent

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u144-c.json`, row `C9_parent_of_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`
- Collected: 94 against a baseline of 94
- Kills: 10 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_two_landings_of_one_set_on_two_days_make_one_playlist`

Old text:

```
        if str(getattr(row, "ParentID", "") or "") == parent_id:
```

New text:

```
        if True:
```

### `u307.R17_made_on_drops_posted`

set_playlist._made_on: a pinned day wins over --posted, so a posted override does not survive a re-plan

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u307.json`, row `R17_made_on_drops_posted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_organize_inspiration.py`, `tests/test_u129_set_account_playlist.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`

Old text:

```
    if on is not None and posted is None:
```

New text:

```
    if on is not None:
```

### `u135.A14_set_order_reverses`

INBOX set-order walk appends members in reverse position order

- File: `src/cratekit/intake/native.py`
- Source: `u135.json`, row `A14_set_order_reverses`
- Moved: Anchored where u307-replay-after-a.json replayed it: the same walk over the set's members in position order, now in native.py's _batch_order (U307 folded the loop)
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_u135_set_inbox_join.py`
- Collected: 65 against a baseline of 65
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_u135_set_inbox_join.py::test_one_landing_of_a_set_files_its_inbox_playlist_in_set_order_not_name_order`

Old text:

```
    members = plan.set_playlist.members if plan.set_playlist is not None else ()
```

New text:

```
    members = tuple(reversed(plan.set_playlist.members)) if plan.set_playlist is not None else ()
```

### `r187-a.C1_blank_not_key`

names_something: ask the text and not the comparison key, so a name of punctuation alone is searched for

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C1_blank_not_key`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_name_with_nothing_in_it_is_an_unknown_anchor[ - ]`
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
    return bool(setbuilder.match_key("", text))
```

New text:

```
    return bool(text.strip())
```

### `r187-a.C4_key_beside_name`

set_build: a key beside --named is let through and silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C4_key_beside_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-name]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.named is None and (ctx.args.key is not None or ctx.args.tempo is not None):
```

### `r187-a.C5_empty_name_scans`

set_build: an empty name pays for the library walk before it is refused

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C5_empty_name_scans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_empty_name_refuses_before_any_scan`

Old text:

```
        index = _index(cfg, root) if names_something(ctx.args.named) else ()
```

New text:

```
        index = _index(cfg, root)
```

### `r187-a.C6_no_cache_path`

_index: pass no cache path, which is R-188 itself, every set a full scan

- File: `src/cratekit/setbuilder/cli.py`
- Source: `r187-a.json`, row `C6_no_cache_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_second_run_reads_no_tag_it_already_holds`
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_cli.py::test_the_verb_writes_its_declared_cache_and_nothing_of_the_librarys`

Old text:

```
        cache_path=config.state_path("setbuilder_index_cache", cfg),
```

New text:

```
        cache_path=None,
```

### `u43-author-light.A1_first_track_wins`

anchor_in_index returns the first indexed track instead of the one at the path, which is exactly what the fuzzy lookup this design replaces does when a version suffix is present

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A1_first_track_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[path-not-indexed]`
  - `tests/test_setbuilder_cli.py::test_an_anchor_spelled_through_a_symlink_still_resolves`
  - `tests/test_setbuilder_cli.py::test_an_exact_name_is_never_lost_to_a_longer_title_whichever_came_first`
  - `tests/test_setbuilder_cli.py::test_what_plays_after_a_track_is_asked_by_name`

Old text:

```
    wanted = str(path)
    for track in index:
        if track.path == wanted:
            return track
```

New text:

```
    wanted = str(path)
    for track in index:
        if track.path or wanted:
            return track
```

### `u43-author-light.A3_containment_not_checked`

anchor_path stops checking that the anchor is inside the library, so a path walking out with .. is scanned for and refused as unindexed rather than refused as outside

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A3_containment_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_path_is_taken_against_the_library_and_never_walks_out_or_defaults`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if _within(candidate, root) and False:
```

### `u43-author-light.A4_empty_anchor_defaults`

anchor_path stops refusing an empty anchor, which turns it into the library root and asks the index for a directory

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-light.json`, row `A4_empty_anchor_defaults`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[empty-anchor]`
  - `tests/test_setbuilder_cli.py::test_an_anchor_path_is_taken_against_the_library_and_never_walks_out_or_defaults`

Old text:

```
    if not anchor:
        raise refuse(
```

New text:

```
    if anchor and not anchor:
        raise refuse(
```

### `u43-author-round-2.H2_empty_is_a_no_op`

ROUND ONE: zero. A plan with no companions reports NO_OP rather than OK, which tells a consumer nothing happened when the question was answered

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H2_empty_is_a_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_library_holding_only_the_anchor_is_an_empty_plan_and_not_a_failure`

Old text:

```
    return ctx.envelope(data=plan, outcome=Outcome.OK)
```

New text:

```
    return ctx.envelope(
        data=plan, outcome=Outcome.OK if plan["items"] else Outcome.NO_OP
    )
```

### `u43-author-round-2.H3_missing_root_not_refused`

ROUND ONE: zero. The configured library root is no longer checked before the scan, so an unmounted volume scans zero files and every anchor comes back unindexed

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `H3_missing_root_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
```

New text:

```
    if root.is_dir() and False:
```

### `u43-author-round-2.V3_root_check_reports_instead_of_refusing`

The missing root produces an empty plan and an OK exit rather than a refusal, which is the clean-report-over-unreadable-state shape rather than the crash shape. A guard that only catches the crash is not the guard this row needs

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u43-author-round-2.json`, row `V3_root_check_reports_instead_of_refusing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_unreachable_library_refuses_rather_than_reporting_an_unindexed_anchor`

Old text:

```
    if not root.is_dir():
        raise refuse(
```

New text:

```
    if not root.is_dir():
        return ctx.envelope(
            data=plan_for(
                setbuilder.Track(
                    artist="", title="", key="", bpm=None, genre="",
                    energy=None, vox=None, voxgender=None, match="",
                ),
                (),
                declared=taxonomy.default_taxonomy(),
            ),
            outcome=Outcome.OK,
        )
    if False:
        raise refuse(
```

### `u98-a.U2_key_missing`

unowned_anchor: drop the key missing refusal, so an unresolved anchor reaches the engine

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-a.json`, row `U2_key_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[unowned-no-key]`
  - `tests/test_setbuilder_cli.py::test_an_unowned_anchor_with_no_key_or_no_label_refuses`

Old text:

```
    if resolved.key is None:
```

New text:

```
    if False:
```

### `u98-b.E1_existing_containment`

existing sample: anchor_path drops the library containment refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `E1_existing_containment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_an_anchor_outside_the_library_refuses_before_any_scan`
  - `tests/test_setbuilder_cli.py::test_an_anchor_path_is_taken_against_the_library_and_never_walks_out_or_defaults`

Old text:

```
    if not _within(candidate, root):
```

New text:

```
    if False:
```

### `u98-b.S1_supplied_beside_path`

set_build: drop the refusal of --key or --bpm beside a path anchor, so both are silently ignored

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S1_supplied_beside_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 3 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-name]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[key-beside-path]`
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[tempo-beside-path]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if False:
```

### `u98-b.S2_tempo_half`

set_build: drop only the tempo half of that refusal

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u98-b.json`, row `S2_tempo_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_cli.py`
- Collected: 80 against a baseline of 80
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_a_refused_invocation_is_a_precondition_with_its_own_reason[tempo-beside-path]`

Old text:

```
    if ctx.args.key is not None or ctx.args.tempo is not None:
```

New text:

```
    if ctx.args.key is not None:
```

### `u279.M12_holder_never_found`

Exclusion.holder: answer None for every path, so no anchor is placed in an excluded folder

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M12_holder_never_found`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
            if identity in self.folders:
                return self.folders[identity]
```

New text:

```
            if False:
                return self.folders[identity]
```

### `u279.M1_walk_ignores_exclude`

iter_audio: walk the whole root again, sorted(root.rglob), so the excluded folders are indexed (the defect itself)

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M1_walk_ignores_exclude`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 10 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_a_staging_copy_never_takes_the_library_files_place`
  - `tests/test_setbuilder_excluded.py::test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served`
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
    for candidate in sorted(Exclusion.under(root, exclude).walk(root)):
```

New text:

```
    for candidate in sorted(root.rglob("*")):
```

### `u279.M2_excluded_folder_walked`

Exclusion.walk: drop the skip of an excluded folder, so the hand walk yields it and its contents

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u279.json`, row `M2_excluded_folder_walked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 10 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_a_staging_copy_never_takes_the_library_files_place`
  - `tests/test_setbuilder_excluded.py::test_an_earlier_cache_entry_under_an_excluded_folder_is_not_served`
  - `tests/test_setbuilder_excluded.py::test_an_excluded_folder_is_matched_by_location_whatever_its_spelling`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`
  - `tests/test_setbuilder_excluded.py::test_the_excluded_walk_is_todays_walk_less_the_excluded_folders`

Old text:

```
            if identity in self.folders:
                continue
            yield child
```

New text:

```
            yield child
```

### `u279.M10_tilde_not_expanded`

excluded_folders: read the staging path without expanding a tilde, round one's finding

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M10_tilde_not_expanded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
Path(cfg.paths.download_staging).expanduser())
```

New text:

```
Path(cfg.paths.download_staging))
```

### `u279.M11_excluded_anchor_not_refused`

set_build: drop the excluded anchor refusal, so an anchor in staging gets the generic not indexed wording

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M11_excluded_anchor_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 2 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[state]`

Old text:

```
    _refuse_if_excluded(candidate, cfg, root)

```

New text:

```
(empty)
```

### `u279.M13_wrong_folder_named`

_refuse_if_excluded: say the state folder whichever folder holds the anchor

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M13_wrong_folder_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 1 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`

Old text:

```
    if holder == folders[0]:
```

New text:

```
    if True:
```

### `u279.M8_index_call_unexcluded`

setbuild _index: drop exclude, so the verb's index walks the state and staging folders again

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M8_index_call_unexcluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 6 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_companion_held_only_in_staging_is_left_out_of_the_set`
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[renamed-state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[state-folder]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
        exclude=excluded_folders(cfg),

```

New text:

```
(empty)
```

### `u279.M9_staging_not_excluded`

excluded_folders: leave download staging out of the exclusion, the state folder only

- File: `src/cratekit/setbuilder/cli.py`
- Source: `u279.json`, row `M9_staging_not_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_excluded.py`, `tests/test_setbuilder_cli.py`, `tests/test_setbuilder_one_open.py`, `tests/modules/test_tools.py`
- Collected: 339 against a baseline of 339
- Kills: 4 (killed)
- Killed:
  - `tests/test_setbuilder_excluded.py::test_a_name_held_only_in_staging_is_not_indexed_and_says_what_is`
  - `tests/test_setbuilder_excluded.py::test_an_anchor_inside_an_excluded_folder_is_refused_naming_the_folder[staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[download-staging]`
  - `tests/test_setbuilder_excluded.py::test_setbuild_ranks_around_the_library_file_and_names_no_copy[tilde-staging]`

Old text:

```
    return (config.library_state_dir(cfg), Path(cfg.paths.download_staging).expanduser())
```

New text:

```
    return (config.library_state_dir(cfg), config.library_state_dir(cfg))
```

### `u266.M1_seven_opens_again`

read_index_tags: go back to one read_tag call per field, seven opens a file, the regression the card removes

- File: `src/cratekit/modules/tools/setbuilder.py`
- Source: `u266.json`, row `M1_seven_opens_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setbuilder_one_open.py`, `tests/test_setbuilder_cli.py`, `tests/modules/test_tools.py`
- Collected: 324 against a baseline of 324
- Kills: 52 (killed)
- Killed:
  - `tests/test_setbuilder_cli.py::test_the_first_run_opens_each_file_once_and_the_second_none`
  - `tests/test_setbuilder_one_open.py::test_a_file_one_open_cannot_read_reads_all_absent_and_never_raises`
  - `tests/test_setbuilder_one_open.py::test_an_undecodable_field_reads_none_and_its_neighbours_still_read`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.m4a]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.mp3]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.ogg]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.opus]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[beyond-ascii-.wav]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aif]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.aiff]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.flac]`
  - `tests/test_setbuilder_one_open.py::test_one_open_reads_what_the_seven_reads_read[every-field-.m4a]`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    return tags.read_tags(path, INDEX_FIELDS)
```

New text:

```
    return {name: tags.read_tag(path, name) for name in INDEX_FIELDS}
```

### `u283.S15_nothing_entered_fails`

_link_discogs: an empty entry is a FAIL rather than the skip note

- File: `src/cratekit/cli/setup.py`
- Source: `u283.json`, row `S15_nothing_entered_fails`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_setup_discogs.py`, `tests/test_doctor.py`
- Collected: 476 against a baseline of 476
- Kills: 2 (killed)
- Killed:
  - `tests/test_doctor.py::test_an_empty_credential_leaves_the_exit_code_to_doctor`
  - `tests/test_setup_discogs.py::test_skipping_is_a_note_saying_what_it_costs_and_how_to_link_later[nothing-entered]`

Old text:

```
            wizard.note(key, title, doctor.Status.INFO, f"nothing was entered; {unlinked}")
```

New text:

```
            wizard.note(key, title, doctor.Status.FAIL, f"nothing was entered; {unlinked}")
```

### `u28-skills-independent.K1_composite`

What K1 does hold: break the packaged root's package name so the shipped assets cannot be resolved

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `K1_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 11 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`
  - `tests/test_skills_install.py::test_the_copies_are_copies_and_not_symlinks`
  - `tests/test_skills_install.py::test_the_packaged_root_resolves_through_the_package`

Old text:

```
    return resources.files("cratekit.skills") / "assets"
```

New text:

```
    return resources.files("cratekit.skills") / "skills"
```

### `u28-skills-independent.S14_into_ignored`

--into is ignored and the default target is always used, so a caller's chosen destination is silently overridden

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S14_into_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 10 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_refusal_leaves_no_half_written_target`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_a_target_that_cannot_be_created_refuses_with_a_typed_cause`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_every_shipped_skill_is_installed_and_the_set_is_walked_not_listed`
  - `tests/test_skills_install.py::test_the_copies_are_copies_and_not_symlinks`

Old text:

```
    into = Path(ctx.args.into).expanduser() if ctx.args.into else default_target()
```

New text:

```
    into = default_target()
```

### `u28-skills-independent.S15_drift_never_warns`

every check reports ok, so a refreshed copy no longer tells the person their agent was reading an older build

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S15_drift_never_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`

Old text:

```
                "status": "ok" if was in {"installed", "current"} else "info",
```

New text:

```
                "status": "ok",
```

### `u28-skills-independent.S16_counts_miscounted`

every skill is counted as installed, so the summary claims a first install on every re-run

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S16_counts_miscounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 5 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
        counts[was] += 1
```

New text:

```
        counts["installed"] += 1
```

### `u28-skills-independent.S18_detail_reworded`

the refreshed detail sentence is reworded, dropping the phrase the drift test reads

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S18_detail_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 1 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`

Old text:

```
        f"the copy at {where} was written by a different build and has been "
        f"replaced; anything reading it was following older instructions"
```

New text:

```
        f"the copy at {where} came from another release of this tool and was "
        f"overwritten; whatever read it was following older instructions"
```

### `u28-skills-independent.S5_stamp_quote_strip`

installed_version stops stripping the TOML quotes, so every stamped copy reads as a different version

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S5_stamp_quote_strip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 7 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
            return value.strip().strip('"')
```

New text:

```
            return value.strip()
```

### `u28-skills-independent.S9_previous_always_none`

install_one never reads the existing stamp, so a copy from this same build reports as refreshed

- File: `src/cratekit/skills/cli.py`
- Source: `u28-skills-independent.json`, row `S9_previous_always_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 5 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
    previous = installed_version(destination) if destination.exists() else None
```

New text:

```
    previous = None
```

### `u311.D1_stamp_name_unstripped`

A stamp line's name is not stripped, so a spaced version line is not found

- File: `src/cratekit/skills/cli.py`
- Source: `u311.json`, row `D1_stamp_name_unstripped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_skills_install.py`
- Collected: 16 against a baseline of 16
- Kills: 8 (killed)
- Killed:
  - `tests/test_skills_install.py::test_a_clean_directory_gets_every_shipped_skill_with_a_stamp`
  - `tests/test_skills_install.py::test_a_file_a_previous_install_wrote_and_this_build_withdrew_disappears`
  - `tests/test_skills_install.py::test_a_file_the_product_never_wrote_survives_a_refresh`
  - `tests/test_skills_install.py::test_a_stale_stamp_warns_and_is_repaired_in_the_same_run`
  - `tests/test_skills_install.py::test_an_unstamped_copy_is_drift_rather_than_damage`
  - `tests/test_skills_install.py::test_an_up_to_date_install_writes_nothing_at_all`
  - `tests/test_skills_install.py::test_install_one_reports_which_of_the_three_things_happened`
  - `tests/test_skills_install.py::test_running_it_twice_reports_current_and_not_installed`

Old text:

```
            yield name.strip(), value
```

New text:

```
            yield name, value
```

### `r1890.P12_accessor_held_off_the_naming_convention`

convergence, outside the writer's glob, gains a call time accessor back to the writer, the mark of a part the scans would not read

- File: `src/cratekit/core/convergence.py`
- Source: `r1890.json`, row `P12_accessor_held_off_the_naming_convention`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_split_modules.py`
- Collected: 5 against a baseline of 5
- Kills: 1 (killed)
- Killed:
  - `tests/test_split_modules.py::test_a_module_holding_an_accessor_is_read_with_the_module_it_reaches`

Old text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"

```

New text:

```
SOFT_DELETE_COLUMN = "rb_local_deleted"


def _writer():
    from cratekit.core import rb_writer

    return rb_writer

```

### `u293.S1_reentrant`

held: a process holding the lock takes it again on a second descriptor and refuses itself

- File: `src/cratekit/core/staging_lock.py`
- Source: `u293.json`, row `S1_reentrant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_staging_lock.py`, `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 237 against a baseline of 237
- Kills: 6 (killed)
- Killed:
  - `tests/test_staging_lock.py::test_one_process_holds_it_again_by_count_and_releases_at_the_outermost`
  - `tests/test_sync_night.py::test_a_night_pass_reaches_the_landing_gate_and_answers_nothing_but_the_name_confirm`
  - `tests/test_sync_night.py::test_a_night_pass_that_needs_the_acknowledgment_stops_there_and_mints_none`
  - `tests/test_sync_night.py::test_a_night_pass_the_vocal_model_cannot_score_waits_at_that_gate_and_queues_nothing`
  - `tests/test_sync_night.py::test_a_refused_firing_keeps_the_pass_waiting_at_its_gate`
  - `tests/test_sync_night.py::test_a_track_the_download_refused_is_named_in_the_record`

Old text:

```
    if _HANDLE is not None:
```

New text:

```
    if False:
```

### `u293.S2_second_holder_refused`

held: a second holder goes on beside the first rather than refusing

- File: `src/cratekit/core/staging_lock.py`
- Source: `u293.json`, row `S2_second_holder_refused`
- Moved: Anchored where u325-replay-after.json replayed it: Same refusal in held; U298 moved the non blocking flock into config.lock_now, which returns whether the lock was had, and the raise now sits under if not had, one level shallower, still the refusal of a second holder
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_staging_lock.py`, `tests/test_sync_night.py`, `tests/test_sync_land.py`, `tests/test_label_sync_go.py`
- Collected: 237 against a baseline of 237
- Kills: 5 (killed)
- Killed:
  - `tests/test_staging_lock.py::test_a_holder_that_cannot_be_read_still_refuses`
  - `tests/test_staging_lock.py::test_a_second_holder_refuses_naming_the_first`
  - `tests/test_sync_night.py::test_a_label_go_refuses_while_another_pass_holds_the_lock`
  - `tests/test_sync_night.py::test_a_pass_by_hand_refuses_while_the_night_holds_the_lock`
  - `tests/test_sync_night.py::test_another_pass_holding_the_staging_lock_refuses_the_night_naming_it`

Old text:

```
            raise _held_error(what or verb, _read_holder(handle.read()), path) from None
```

New text:

```
            pass
```

### `r359.M5_unwired`

The playlists planner no longer hands its note to the plan

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M5_unwired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]), note=playlists.said)
```

New text:

```
    plan = _Plan(spec=spec, describe=describe, detail=describe([]))
```

### `r359.M6_no_append`

The check computes the note and never appends it to the detail a person reads

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M6_no_append`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
        check["detail"] += f"; {noted}"
```

New text:

```
        pass
```

### `r359.M7_note_before_describe`

The note reads an empty block instead of the source's own, so it says nothing

- File: `src/cratekit/sync/cli.py`
- Source: `r359.json`, row `M7_note_before_describe`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_recorded_playlist_says_in_the_default_output_it_was_resolved_not_acquired`

Old text:

```
    noted = plan.note(plan.detail or {}) if plan.note is not None else None
```

New text:

```
    noted = plan.note({}) if plan.note is not None else None
```

### `r504-b.B10_check_no_numbers`

The inbound check fails without naming the three numbers

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B10_check_no_numbers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            f"; the listing came back short, {short.summary()}, which does not say which"
```

New text:

```
            "; the listing came back short, which does not say which"
```

### `r504-b.B7_sync_drops_short`

sync all lists the hearts and keeps no shortfall

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B7_sync_drops_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    inbound.shortfall = short
```

New text:

```
    inbound.shortfall = None
```

### `r504-b.B8_check_passes`

A short listing leaves the inbound check at its prior status instead of failing it

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B8_check_passes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        check["status"] = "fail"
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

New text:

```
        if inbound.not_queued == playlists.Excluded.EMPTY:
```

### `r504-b.B9_all_withheld_says_no_hearts`

Every heart withheld still reads as an account that lists no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `r504-b.json`, row `B9_all_withheld_says_no_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
            check["detail"] = "not queued: the provider served none of the account's hearts"
```

New text:

```
            pass
```

### `r515-operator.S13_sweep_no_warning`

The sync all sweep says nothing of a short playlist

- File: `src/cratekit/sync/cli.py`
- Source: `r515-operator.json`, row `S13_sweep_no_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
    if sweep.short:
```

New text:

```
    if False:
```

### `u109-a.A1_plan_guided`

Plan every enabled source again, guided ones included, so labels is planned as a source with no worker

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A1_plan_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    plans = [_plan(spec, ctx) for spec in enabled if spec.guided_by is None]
```

New text:

```
    plans = [_plan(spec, ctx) for spec in enabled]
```

### `u109-a.A2_guided_empty`

Collect no guided source, so nothing names crate label sync anywhere

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A2_guided_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    guided = tuple(spec for spec in enabled if spec.guided_by is not None)
```

New text:

```
    guided = ()
```

### `u109-a.A3_no_check_row`

Drop the guided check row, the one line the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A3_no_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
    checks.extend(_guided_check(spec) for spec in guided)
```

New text:

```
(empty)
```

### `u109-a.A4_summary_guided`

Drop summary.guided from the pass report

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A4_summary_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_profile_without_the_labels_module_names_no_guided_verb`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
        "guided": _guided(guided),
    }
    for plan in plans:
```

New text:

```
    }
    for plan in plans:
```

### `u109-a.A5_gate_guided`

Drop the guided block from what the favourites gate shows

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A5_gate_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`

Old text:

```
            if p.inbound is not None
        },
        "guided": _guided(guided),
    }
```

New text:

```
            if p.inbound is not None
        },
    }
```

### `u109-a.A6_refusal_step_dropped`

A pass that queued nothing refuses without the step naming the guided verb

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A6_refusal_step_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=first.remediation.steps,
```

### `u109-a.A7_refusal_step_first`

Prepend the guided step instead of appending it, so it displaces the refusing source's own first step

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A7_refusal_step_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`

Old text:

```
            steps=(*first.remediation.steps, *(_guided_step(spec) for spec in guided)),
```

New text:

```
            steps=(*(_guided_step(spec) for spec in guided), *first.remediation.steps),
```

### `u109-a.A8_row_reworded`

Reword the guided row so it no longer says the source is not swept here

- File: `src/cratekit/sync/cli.py`
- Source: `u109-a.json`, row `A8_row_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
            f"not swept by sync all; {spec.command()} takes this source on its "
```

New text:

```
            f"left to another verb; {spec.command()} takes this source on its "
```

### `u73-c.C3_next_only_with_intake_jobs`

Name intake missing --run on every pass, including one that queued no intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C3_next_only_with_intake_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_that_finds_only_debris_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_pass_that_queued_no_intake_job_names_no_run_verb`
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`

Old text:

```
    if not filed:
```

New text:

```
    if False:
```

### `u73-c.C4_next_counts_intake_jobs_only`

Count every filed job as an intake job when deciding to name the run verb

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C4_next_counts_intake_jobs_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`

Old text:

```
if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
if True]
```

### `u73-c.C5_next_check_row`

Keep the command in the summary and drop the check row the human output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u73-c.json`, row `C5_next_check_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_default_output_of_a_pass_that_queued_intake_jobs_names_the_run_verb`

Old text:

```
        checks.append(step["check"])
```

New text:

```
        pass
```

### `u74-b.B10_refused_check_status`

Report a hearts refusal as info rather than fail

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B10_refused_check_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`

Old text:

```
    elif inbound.refused is not None:
        check["status"] = "fail"
```

New text:

```
    elif inbound.refused is not None:
        check["status"] = "info"
```

### `u74-b.B11_gate_screen`

The gate screen says the hearts are queued whatever the answer when the listing refused

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B11_gate_screen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_the_gate_says_when_the_hearts_could_not_be_listed`

Old text:

```
                "queued_whatever_the_answer": p.inbound.queue is not None,
```

New text:

```
                "queued_whatever_the_answer": True,
```

### `u74-b.B12_next_step_outbound_only`

Name no intake missing --run step when only the hearts filed an intake job

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B12_next_step_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
    filed = [job for p in plans for job in _filed(p) if job.handler_key in intake_cli.INTAKE_KEYS]
```

New text:

```
    filed = [job for p in plans for job in p.filed if job.handler_key in intake_cli.INTAKE_KEYS]
```

### `u74-b.B1_source_id_dropped`

Queue the hearts job with no source_id, so the next pass cannot see it is open

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B1_source_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
            )
```

New text:

```
                run_id=run_id,
                source_id=None,
            )
```

### `u74-b.B2_compose_skips_inbound`

The composer never queues the read half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B2_compose_skips_inbound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 16 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if p.inbound is not None and p.inbound.queue is not None:
            ready.append
```

New text:

```
        if False:
            ready.append
```

### `u74-b.B3_queue_refusal_raised`

Raise a queue time refusal instead of recording it against its half

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B3_queue_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_refusal_part_way_through_the_playlists_keeps_the_filed_ones_named`
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`

Old text:

```
                    half.refused, half.not_queued = exc.cause, exc.cause.reason
```

New text:

```
                    raise
```

### `u74-b.B4_filed_outbound_only`

Count only the write half's jobs as filed, so a pass that queued only the hearts refuses or reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B4_filed_outbound_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
    return [*plan.filed, *(plan.inbound.filed if plan.inbound is not None else ())]
```

New text:

```
    return [*plan.filed]
```

### `u74-b.B5_inbound_refusal_not_counted`

Leave the hearts refusal out of the refusal list, so a declined pass it alone stopped reads as a no-op

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B5_inbound_refusal_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`

Old text:

```
        for cause in (p.refused, p.inbound.refused if p.inbound else None)
```

New text:

```
        for cause in (p.refused, None)
```

### `u74-b.B6_inbound_warning`

Emit no warning for a hearts refusal

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B6_inbound_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`

Old text:

```
        if plan.inbound is not None and plan.inbound.refused is not None:
            warnings.append(
```

New text:

```
        if False:
            warnings.append(
```

### `u74-b.B7_block_dropped`

Leave the favourites.inbound block out of the summary

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B7_block_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 13 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`

Old text:

```
            plan.detail = {**(plan.detail or {}), "inbound": plan.inbound.block()}
```

New text:

```
            pass
```

### `u74-b.B8_check_dropped`

Leave the sync.favorites.inbound check out, which is all the default output prints

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B8_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 10 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
            checks.append(_inbound_check(plan, plan.inbound))
```

New text:

```
            pass
```

### `u74-b.B9_check_wording`

Say the hearts were not listed for a half that was listed and refused at the queue

- File: `src/cratekit/sync/cli.py`
- Source: `u74-b.json`, row `B9_check_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`

Old text:

```
            if inbound.hearts is None
```

New text:

```
            if True
```

### `u74.A10_export_refusal_raised`

Raise the write half's export refusal to _plan again, which drops the read half with it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A10_export_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 15 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_output_prints_the_inbound_shortfall`

Old text:

```
        plan.refused, plan.not_queued = exc.cause, exc.cause.reason
        return plan
```

New text:

```
        raise
```

### `u74.A11_queue_not_bound`

Never bind the read half's queue callable, so a listed half queues nothing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A11_queue_not_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 17 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_complete_hearts_listing_carries_no_shortfall`
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_a_declined_favourites_source_says_nothing_about_a_write_it_never_reached`
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_a_hearts_queue_refusal_is_recorded_against_the_hearts_alone`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_short_hearts_listing_is_queued_and_fails_the_inbound_check_by_count`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`
  - `tests/test_sync_all.py::test_the_gate_refusal_queues_no_hearts_listing_either`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    inbound.queue = queue
    return inbound
```

New text:

```
    return inbound
```

### `u74.A12_run_id_dropped`

Queue the hearts job without the shared run id, so intake missing --run cannot find it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A12_run_id_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_confirmed_pass_queues_both_halves`
  - `tests/test_sync_all.py::test_an_abort_still_queues_the_hearts_listing_under_the_shared_run`

Old text:

```
                tracks=tracks,
                run_id=run_id,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

New text:

```
                tracks=tracks,
                run_id=None,
                source_id=intake_cli.FAVORITES_SOURCE_ID,
```

### `u74.A3_handler_filter`

Drop the handler key filter, so an open outbound favourites job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A3_handler_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`

Old text:

```
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

New text:

```
        if True
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
```

### `u74.A4_source_filter`

Drop the source_id filter, so an open playlists job holds the hearts listing

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A4_source_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
        and (job.payload or {}).get("source_id") == intake_cli.FAVORITES_SOURCE_ID
        and job.library_id == cfg.library.volume_id
```

New text:

```
        and True
        and job.library_id == cfg.library.volume_id
```

### `u74.A5_library_filter`

Drop the library filter, so another library's open hearts job holds this one

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A5_library_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_another_librarys_open_hearts_job_does_not_hold_this_one`

Old text:

```
        and job.library_id == cfg.library.volume_id
    )
```

New text:

```
        and True
    )
```

### `u74.A6_open_filter`

Count a finished hearts job as open, so a failed job holds every later pass

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A6_open_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_finished_hearts_job_does_not_hold_the_next_pass`
  - `tests/test_sync_all.py::test_an_open_outbound_favourites_job_does_not_hold_the_hearts`
  - `tests/test_sync_all.py::test_an_open_playlists_job_does_not_hold_the_hearts`

Old text:

```
                if job.is_open()
            )
```

New text:

```
                if True
            )
```

### `u74.A7_in_flight_guard`

Ignore an open hearts job, so every pass queues a second listing beside it

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A7_in_flight_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_hearts_job_queued_by_hand_is_not_queued_beside`
  - `tests/test_sync_all.py::test_an_open_hearts_job_is_not_queued_twice`

Old text:

```
        if in_flight:
            inbound.not_queued
```

New text:

```
        if False:
            inbound.not_queued
```

### `u74.A8_empty_guard`

Queue an empty hearts listing as a job, rather than reporting no hearts

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A8_empty_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_source_refused_at_queue_time_leaves_the_queued_ones_named`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_an_account_with_no_hearts_queues_nothing_for_them`
  - `tests/test_sync_all.py::test_hearts_all_withheld_are_not_reported_as_an_account_with_none`

Old text:

```
    if not tracks:
        inbound.not_queued = playlists.Excluded.EMPTY
```

New text:

```
    if False:
        inbound.not_queued = playlists.Excluded.EMPTY
```

### `u74.A9_listing_refusal_raised`

Raise a hearts listing refusal instead of recording it, so it ends the favourites source

- File: `src/cratekit/sync/cli.py`
- Source: `u74.json`, row `A9_listing_refusal_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 19 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_catalogue_refusal_is_the_hearts_own_and_the_others_still_run`
  - `tests/test_sync_all.py::test_a_declined_pass_whose_hearts_refused_is_a_refusal_not_a_no_op`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_pass_over_a_recent_export_carries_no_age_warning`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_an_unreadable_hearts_listing_is_reported_and_the_playlists_still_queue`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_half_refused_is_still_a_refusal`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_composed_gate_judges_against_the_configured_limit`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`
  - `tests/test_sync_all.py::test_the_composed_gate_shows_the_tracks_the_sweeps_digest_covers`
  - `tests/test_sync_all.py::test_the_composed_pass_carries_the_favourites_verb_standing_warning`
  - `tests/test_sync_all.py::test_the_favourites_job_carries_a_gate_run_its_own_verb_owns`
  - `tests/test_sync_all.py::test_the_gate_asks_over_the_digest_sync_favorites_itself_offers`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - ... and 4 more, see the JSON sidecar

Old text:

```
        inbound.refused, inbound.not_queued = exc.cause, exc.cause.reason
        return inbound
```

New text:

```
        raise
```

### `r358.S1_set_is_the_cursor`

Take the mark set from recorded_now again, the review's finding 1

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S1_set_is_the_cursor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_recorded_debris_playlist_is_not_pending_at_all`

Old text:

```
        for identity in sorted(sweep.recorded)
```

New text:

```
        for identity in sorted(sweep.recorded_now)
```

### `r358.S5_recheck_is_a_second_read`

Serve the recheck from the plan's own listing instead of a fresh read

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S5_recheck_is_a_second_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_after_a_real_importable_file_takes_the_recorded_playlist`
  - `tests/test_sync_all.py::test_a_playlist_renamed_or_gone_on_the_account_since_the_plan_is_left_alone[gone]`
  - `tests/test_sync_all.py::test_a_playlist_renamed_or_gone_on_the_account_since_the_plan_is_left_alone[renamed]`

Old text:

```
        name = listed.get(mark.target_id) or ""
        return bool(name) and current().get(mark.target_id) == name
```

New text:

```
        name = listed.get(mark.target_id) or ""
        return bool(name) and listed.get(mark.target_id) == name
```

### `r358.S7_lazy_listing`

Read the account eagerly, so a call with no file still spends a listing

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S7_lazy_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`

Old text:

```
    held: list[dict[str, str]] = []

    def current() -> dict[str, str]:
```

New text:

```
    held: list[dict[str, str]] = [
        {playlist.playlist_id: playlist.name for playlist in _listed_or_refuse(found)}
    ]

    def current() -> dict[str, str]:
```

### `r358.S9_mark_always_applied`

Report the mark applied whether or not the step ran

- File: `src/cratekit/sync/playlists.py`
- Source: `r358.json`, row `S9_mark_always_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`
- Collected: 115 against a baseline of 115
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_renames_nothing_even_over_a_recorded_playlist_with_its_file_landed`
  - `tests/test_sync_all.py::test_a_slim_pass_queues_each_new_account_playlist_under_the_shared_run`
  - `tests/test_sync_all.py::test_the_block_tells_a_mark_that_ran_apart_from_a_mark_that_never_ran`
  - `tests/test_sync_all.py::test_the_current_intake_path_marks_nothing_and_still_reports_unbound`

Old text:

```
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
```

New text:

```
        "mark": MARK_APPLIED,
```

### `r1289.M10_warning_ready_filter`

_plan_playlists: the unread warning covers a playlist that was not queued, saying its other tracks are

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M10_warning_ready_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if identity in sweep.ready
```

New text:

```
        identity: tracks for identity, tracks in sweep.unread.items() if True
```

### `r1289.M11_warning_absent`

_plan_playlists: no unread warning at all

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M11_warning_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
    if left:
```

New text:

```
    if False:
```

### `r1289.M12_warning_promise`

_plan_playlists: the warning reworded to promise a later sync offers the playlist again, which is false once its job succeeds

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M12_warning_promise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                    "playlist's intake job succeeds no later sync offers it again, so "
```

New text:

```
                    "playlist's intake job succeeds the next sync takes it up again, so "
```

### `r1289.M13_warning_names`

_plan_playlists: the warning names each playlist but not its unread tracks

- File: `src/cratekit/sync/cli.py`
- Source: `r1289.json`, row `M13_warning_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`
- Collected: 146 against a baseline of 146
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                        + ", ".join(f"{ref} ({one['why']})" for ref, one in tracks.items())
```

New text:

```
                        + "some tracks"
```

### `u109-b.B1_labels_not_guided`

Drop guided_by from the labels spec, so labels is an ordinary source with no worker

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B1_labels_not_guided`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_incremental_sync.py`, `tests/test_label_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_full_pass_queues_each_source_under_its_own_key_with_one_run`
  - `tests/test_sync_all.py::test_a_missing_export_still_queues_the_hearts_and_the_pass_is_not_a_refusal`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_a_source_that_refuses_does_not_stop_the_other`
  - `tests/test_sync_all.py::test_aborting_the_confirmation_queues_no_favourites_job_and_says_so`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        guided_by="label.sync",
```

New text:

```
(empty)
```

### `u109-b.B2_command_spelling`

Spell the guided command with the registry's dotted name, crate label.sync

- File: `src/cratekit/sync/sources.py`
- Source: `u109-b.json`, row `B2_command_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_label_workers.py`
- Collected: 197 against a baseline of 197
- Kills: 9 (killed)
- Killed:
  - `tests/test_label_workers.py::test_sync_labels_refuses_to_queue_and_names_the_guided_verb`
  - `tests/test_label_workers.py::test_the_itemless_refusal_names_the_cancel_that_gets_a_person_out`
  - `tests/test_sync_all.py::test_a_pass_with_labels_enabled_and_registered_calls_no_label_provider`
  - `tests/test_sync_all.py::test_every_guided_source_names_a_verb_the_registry_declares_and_queues_nothing`
  - `tests/test_sync_all.py::test_nothing_queued_because_every_source_refused_is_a_refusal`
  - `tests/test_sync_all.py::test_the_gate_names_the_guided_verb_and_nothing_for_labels_to_queue`
  - `tests/test_sync_all.py::test_the_human_output_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_human_refusal_names_the_guided_verb`
  - `tests/test_sync_all.py::test_the_pass_names_the_guided_verb_in_one_check_row`

Old text:

```
        return "crate " + self.guided_by.replace(".", " ")
```

New text:

```
        return "crate " + self.guided_by
```

### `r1289.M1_sweep_reads_whole`

plan: read each swept playlist whole again (the declared reader is asked first), so one untitled row leaves the whole playlist out as unreadable

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M1_sweep_reads_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_playlist_with_no_tracks_queues_nothing_and_is_reported`
  - `tests/test_sync_all.py::test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
```

New text:

```
            intake_cli.list_playlist_declared(found, playlist.playlist_id)
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
```

### `r1289.M2_unread_not_kept`

plan: keep no unread track on the sweep, so the summary names none and a playlist with every track unread reads as empty

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M2_unread_not_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
        if listing.unread:
```

New text:

```
        if False:
```

### `r1289.M3_all_unread_branch`

plan: drop the every track unread branch, so such a playlist is excluded as empty rather than unreadable

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M3_all_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_pass_whose_only_playlist_left_every_track_unread_says_so_on_the_check`
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
            if not tracks:
                # EVERY TRACK UNREAD
```

New text:

```
            if False:
                # EVERY TRACK UNREAD
```

### `r1289.M4_unread_why_dropped`

plan: record an unread track without the reader's why

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M4_unread_why_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_queued_playlist_that_left_a_track_unread_is_recorded_when_its_job_succeeds`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
                ref: {**one.said(), "why": one.why} for ref, one in listing.unread.items()
```

New text:

```
                ref: {**one.said()} for ref, one in listing.unread.items()
```

### `r1289.M5_all_unread_message`

plan: the every track unread playlist's unreadable message reworded so it names no track

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M5_all_unread_message`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`

Old text:

```
                    "no track on it could be queued: "
                    + ", ".join(f"{ref} ({one.why})" for ref, one in listing.unread.items())
```

New text:

```
                    "the playlist could not be read"
```

### `r1289.M6_report_unread_emptied`

report: the unread block names each playlist with no tracks under it

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M6_report_unread_emptied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_playlist_whose_every_track_is_unread_is_unreadable_not_empty`
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled0-title]`
  - `tests/test_sync_all.py::test_a_track_with_no_title_or_artist_is_named_and_its_playlist_still_queues[untitled1-artist]`

Old text:

```
            identity: {"name": names.get(identity, ""), "tracks": dict(tracks)}
```

New text:

```
            identity: {"name": names.get(identity, ""), "tracks": {}}
```

### `r1289.M7_per_playlist_reraise`

plan (existing guard, sample): take any refusal as one playlist's, so an expired session reads as one unreadable playlist and the sweep goes on

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M7_per_playlist_reraise`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_refusal_not_about_one_playlist_still_stops_the_sweep`

Old text:

```
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
```

New text:

```
            if False:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
```

### `r1289.M8_per_playlist_set`

PER_PLAYLIST_REASONS (existing guard, sample): drop the reader's refusal, so a row with no provider id stops the whole sweep

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M8_per_playlist_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_row_with_no_provider_id_still_leaves_its_playlist_out_by_name`

Old text:

```
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable", "intake-list-unusable"})
```

New text:

```
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable"})
```

### `r1289.M9_short_check`

plan (existing guard, sample): drop the declared count check, so a short listing is queued without saying what the provider withheld

- File: `src/cratekit/sync/playlists.py`
- Source: `r1289.json`, row `M9_short_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_all.py`, `tests/test_sync_mark.py`, `tests/test_incremental_sync.py`
- Collected: 215 against a baseline of 215
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_short_listing_with_an_unread_track_carries_both`
  - `tests/test_sync_all.py::test_the_sweep_summary_carries_the_shortfall_per_playlist`

Old text:

```
        if listing.short is not None:
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

### `u179.N1_one_label_only_when_all_named`

bandcamp name: name the batch for its one label even when a file carries none

- File: `src/cratekit/intake/batch_name.py`
- Source: `u179.json`, row `N1_one_label_only_when_all_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_bandcamp.py`, `tests/test_sync_bandcamp_native.py`, `tests/test_intake_land_names.py`
- Collected: 54 against a baseline of 54
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_bandcamp.py::test_a_batch_of_a_label_and_an_unregistered_seller_files_by_tag_under_a_plain_name`
  - `tests/test_sync_bandcamp.py::test_a_file_whose_tags_cannot_be_read_is_unread_not_ungenred_and_names_no_label`
  - `tests/test_sync_bandcamp.py::test_the_batch_name_is_the_one_label_every_file_names_or_plain[labels3-Bandcamp]`

Old text:

```
    if len(named) == 1 and not unnamed:
```

New text:

```
    if len(named) == 1:
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

### `u165.F5_report_failed`

file_landed: report a filing whose entries failed as filed

- File: `src/cratekit/intake/filing.py`
- Source: `u165.json`, row `F5_report_failed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`
- Collected: 22479 against a baseline of 22479
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    if report.failed:
        return Filed(
            state=NOT_FILED,
```

New text:

```
    if False:
        return Filed(
            state=NOT_FILED,
```

### `u181.S1_profile_off_asked`

sync land _vocals: ask the model on a profile with the vocals module off

- File: `src/cratekit/cli/sync_land.py`
- Source: `u181.json`, row `S1_profile_off_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_cli_contract.py`
- Collected: 1069 against a baseline of 1069
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
- Collected: 1069 against a baseline of 1069
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

### `u183.M17_record_read_back`

RunState.from_json: read related_runs as empty, so a saved pass is lost on load

- File: `src/cratekit/cli/gates.py`
- Source: `u183.json`, row `M17_record_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_gate_pins.py`, `tests/test_run_decide_continue.py`
- Collected: 86 against a baseline of 86
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_land_run_whose_pass_no_intake_job_carries_is_refused_not_continued`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_record_with_no_related_runs_is_the_record_it_was_and_one_with_them_round_trips`
  - `tests/test_sync_land.py::test_a_refused_id_names_the_land_run_recorded_beside_each_pass`
  - `tests/test_sync_land.py::test_a_run_interrupted_after_sync_all_continues_by_its_own_id`
  - `tests/test_sync_land.py::test_a_run_record_that_is_not_an_object_leaves_the_refusal_whole`

Old text:

```
                {str(role): str(run) for role, run in data["related_runs"].items()}
                if isinstance(data.get("related_runs"), dict)
```

New text:

```
                {}
                if isinstance(data.get("related_runs"), dict)
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

### `u152.R13_missing_lift`

_missing: carry none of the listing's failing rows

- File: `src/cratekit/cli/sync_land.py`
- Source: `u152.json`, row `R13_missing_lift`
- Moved: Anchored where u303-replay-merged5.json replayed it: U303 shortened the comment above the call to one line; the lift of the listing's failing rows in _missing, the guard this row removes, is unchanged in the same place
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land.py`, `tests/test_sync_all.py`, `tests/test_cli_contract.py`
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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
- Collected: 1184 against a baseline of 1184
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

