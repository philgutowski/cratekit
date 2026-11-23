# Mutation table: u325-after-l-19

Measured by `scripts/mutate.py` on 2026-11-22 22:24 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 134.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:23 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 13, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r301.V1_validator_not_called` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 17 | killed |
| `r301.V2_any_domain` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 4 | killed |
| `r301.V3_suffix_without_dot` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 2 | killed |
| `r301.V4_label_shape_loose` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 4 | killed |
| `r301.V6_bool_is_a_bound` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 1 | killed |
| `r301.V7_zero_is_a_bound` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 1 | killed |
| `r44-a.C1_rule_identity_may_be_a_path` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 3 | killed |
| `r44-a.C2_blank_identity_is_absence` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 2 | killed |
| `r44-a.C3_identity_not_written` | `src/cratekit/core/config.py` | user | 1 file(s) | 241 | 1 | killed |
| `r677-b.V4_after_the_stale_test` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 235 | 1 | killed |
| `r677.V1_no_preflight_before_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 235 | 7 | killed |
| `r677.V2_preflight_on_a_plan_of_nothing` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 235 | 1 | killed |
| `r677.V3_refusal_never_replaces_the_gate` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 235 | 5 | killed |
| `r677.V5_preflight_raises_directly` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 235 | 4 | killed |
| `r677.V6_manifest_rows_not_handed_over` | `src/cratekit/intake/land_cli.py` | user | 5 file(s) | 235 | 1 | killed |
| `r677.E1_export_asked_before_the_library` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 235 | 102 | killed |
| `r677.E2_library_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 235 | 5 | killed |
| `r677.E3_intake_file_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 235 | 4 | killed |
| `u220.A10_wrong_status` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 10 | killed |
| `u220.A11_cause_chain_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A12_no_memory_guard` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 2 | killed |
| `u220.A13_exact_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A14_multiset_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u220.A17_settle_once` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 4 | killed |
| `u220.A1_front_target` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 12 | killed |
| `u220.A23_pause_index` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `u293.G1_night_line_asked` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 6 | killed |
| `u293.G2_night_line_off_by_one` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 5 | killed |
| `u293.G3_total_below_mark` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 1 | killed |
| `u293.G4_child_reads_no_line` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 2 | killed |
| `u293.G5_line_held_to_ceiling` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 5 | killed |
| `u293.G6_nested_lower_line` | `src/cratekit/core/provider_gate.py` | maintainer | 4 file(s) | 280 | 1 | killed |
| `u293.G7_hour_never_raised` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 1 | killed |
| `u293.G8_line_exported` | `src/cratekit/core/provider_gate.py` | user | 4 file(s) | 280 | 2 | killed |
| `u213.M1_first_group_is_the_title` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 13 | killed |
| `u213.M3_first_group_position` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 16 | killed |
| `u213.M4_first_group_keeps_brackets` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 15 | killed |
| `u213.M5_listed_names_artist` | `src/cratekit/acquire/match.py` | user | 3 file(s) | 763 | 3 | killed |
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
| `u146-b.B14_plan_owned_keeps_held_hearts` | `src/cratekit/favorites/backfill.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.A1_superseded_ignored` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-b.A2_owned_reads_carried` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 12 | killed |
| `u146-b.A3_report_paths_dropped` | `src/cratekit/intake/account_playlists.py` | user | 1 file(s) | 18 | 11 | killed |
| `u146-c.L2_empty_landing_no_op` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 18 | 7 | killed |
| `u146-c.L3_gate_asked_for_nothing` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 18 | 4 | killed |
| `u146-c.L4_missing_source_refuses` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-c.N1_owned_held_planned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u146-c.N2_owned_not_written` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 2 | killed |
| `u146-c.N4_owned_needs_a_heart_file` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u146-e.N3_owned_out_of_digest` | `src/cratekit/intake/native.py` | user | 1 file(s) | 22933 | 0 (promoted) | zero |
| `u153.N3_landing_colour_owned` | `src/cratekit/intake/native.py` | user | 1 file(s) | 18 | 1 | killed |
| `u105-b.S10_settings_to_engine` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u105-b.S1_parts_only_when_several` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 3 | killed |
| `u105-b.S2_lufs_frozen` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u105-b.S3_lufs_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S4_parts_in_argv` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S5_queue_time_refusal` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 3 | killed |
| `u105-b.S6_join_order_notice` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S7_staged_parts` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S8_staged_target` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 1 | killed |
| `u105-b.S9_precheck_name` | `src/cratekit/master/cli.py` | user | 3 file(s) | 145 | 2 | killed |
| `u177.A10_clear_word` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 1 | killed |
| `u177.A11_field_flag_guard` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 7 | killed |
| `u177.A9_add_drops_account` | `src/cratekit/label/cli.py` | user | 4 file(s) | 144 | 12 | killed |
| `u177.A1_account_suffix` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 23 | killed |
| `u177.A2_account_shape` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 4 | killed |
| `u177.A3_account_case` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 5 | killed |
| `u177.A4_claim_removed` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u177.A5_claim_self` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 1 | killed |
| `u177.A7_stored_raw` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `u177.A8_edit_drops_account` | `src/cratekit/label/registry.py` | user | 4 file(s) | 144 | 2 | killed |
| `r777-confirm.N4_plain_name` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777-confirm.N7_digest_marks` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N10_screen_says_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N11_exclusive` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N12_no_landing_required` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 4 | killed |
| `r777.N18_unreachable_called_bridge` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N19_digest_landings` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 1 | killed |
| `r777.N5_bridge_accepted` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `r777.N6_no_reread` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 2 | killed |
| `r777.N9_proof_is_file` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 141 | 4 | killed |
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
| `r598-b.B1_sweep_before_the_lock` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B3_orphans_not_shown` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |
| `r598-b.B4_abandon_only_reported_as_no_op` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 1 | killed |
| `r598-b.B5_kept_reports_nothing` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 4 | killed |
| `u49-author.A2_the_abort_mints_anyway` | `src/cratekit/session/cli.py` | user | 1 file(s) | 37 | 2 | killed |

## Zero rows and what they owe

- `u146-e.N3_owned_out_of_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r301.V1_validator_not_called`

validate never checks the recognition section

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `V1_validator_not_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 17 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[-bad.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[7]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[Identify-EU-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com.example]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[evilacrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[https://identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify eu.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com.attacker.example]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com/v1/identify]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com:443]`
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[-3]`
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[0]`
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[2.5]`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    problems += _validate_recognition(data)

```

New text:

```
(empty)
```

### `r301.V2_any_domain`

The host may sit under any domain, so the credential can travel anywhere

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `V2_any_domain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com.example]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[evilacrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify-eu-west-1.acrcloud.com.attacker.example]`

Old text:

```
    if not all(_HOST_LABEL.match(label) for label in labels) or not value.endswith(
        f".{RECOGNITION_HOST_DOMAIN}"
    ):
```

New text:

```
    if not all(_HOST_LABEL.match(label) for label in labels):
```

### `r301.V3_suffix_without_dot`

The domain is checked as a bare suffix, so evilacrcloud.com passes

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `V3_suffix_without_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[evilacrcloud.com]`

Old text:

```
        f".{RECOGNITION_HOST_DOMAIN}"
```

New text:

```
        f"{RECOGNITION_HOST_DOMAIN}"
```

### `r301.V4_label_shape_loose`

A host label may hold anything, so a scheme, a path or a port passes

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `V4_label_shape_loose`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 4 (killed)
- Killed:
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[-bad.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[Identify-EU-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[https://identify-eu-west-1.acrcloud.com]`
  - `tests/test_config.py::test_a_host_that_is_not_a_bare_name_under_the_service_is_refused[identify eu.acrcloud.com]`

Old text:

```
_HOST_LABEL = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
```

New text:

```
_HOST_LABEL = re.compile(r"^.+$")
```

### `r301.V6_bool_is_a_bound`

A boolean monthly bound is accepted, so true reads as one call a month

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `V6_bool_is_a_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[True]`

Old text:

```
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 1
    ):
```

New text:

```
        not isinstance(bound, int) or bound < 1
    ):
```

### `r301.V7_zero_is_a_bound`

A zero monthly bound is accepted, which refuses every paid call

- File: `src/cratekit/core/config.py`
- Source: `r301.json`, row `V7_zero_is_a_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_monthly_bound_that_is_not_a_positive_call_count_is_refused[0]`

Old text:

```
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 1
    ):
```

New text:

```
        not isinstance(bound, int) or isinstance(bound, bool) or bound < 0
    ):
```

### `r44-a.C1_rule_identity_may_be_a_path`

Accept a mount path as a rule's volume identity

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C1_rule_identity_may_be_a_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 3 (killed)
- Killed:
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[drive-path]`
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[posix-path]`
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[unc-path]`

Old text:

```
                problems += _mount_path_problem(key, identity)
```

New text:

```
                pass
```

### `r44-a.C2_blank_identity_is_absence`

Read a blank rule identity as none recorded instead of as a problem

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C2_blank_identity_is_absence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 2 (killed)
- Killed:
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[blank]`
  - `tests/test_config.py::test_a_rule_identity_that_is_a_path_or_is_unusable_is_named_by_index[empty]`

Old text:

```
            if not isinstance(identity, str) or not identity.strip():
```

New text:

```
            if not isinstance(identity, str):
```

### `r44-a.C3_identity_not_written`

Never write a rule's identity back out, so a saved configuration loses it

- File: `src/cratekit/core/config.py`
- Source: `r44-a.json`, row `C3_identity_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_config.py`
- Collected: 241 against a baseline of 241
- Kills: 1 (killed)
- Killed:
  - `tests/test_config.py::test_a_prefix_rule_carries_the_identity_of_the_volume_it_points_at`

Old text:

```
        if PREFIX_VOLUME_IDENTITY_KEY in out:
```

New text:

```
        if False:
```

### `r677-b.V4_after_the_stale_test`

any gate refusal, a stale answer included, is replaced by the preflight refusal

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677-b.json`, row `V4_after_the_stale_test`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 235 against a baseline of 235
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_stale_answer_stays_stale_over_an_export_that_is_not_there`

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
- Collected: 235 against a baseline of 235
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_over_a_usable_export_reaches_the_gate_with_the_digest_it_had_before`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_a_collection_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_without_the_intake_folder_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_an_intake_file_already_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_an_unmounted_library_is_named_as_the_library_and_not_as_the_export`
  - `tests/test_intake_land.py::test_the_plan_read_hands_the_engine_the_manifest_rows_the_gate_will_show`

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

### `r677.V2_preflight_on_a_plan_of_nothing`

an empty staging folder is refused over the export instead of shown as a plan of nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V2_preflight_on_a_plan_of_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 235 against a baseline of 235
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_of_nothing_asks_nothing_of_the_export`

Old text:

```
    if planned.items:
        try:
```

New text:

```
    if True:
        try:
```

### `r677.V3_refusal_never_replaces_the_gate`

the preflight refusal is caught and dropped, so the gate is offered over an unusable export

- File: `src/cratekit/intake/land_cli.py`
- Source: `r677.json`, row `V3_refusal_never_replaces_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_landing.py`, `tests/test_landing_labels.py`, `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 235 against a baseline of 235
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_a_collection_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_that_is_not_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_a_plan_over_an_export_without_the_intake_folder_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_an_intake_file_already_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_an_unmounted_library_is_named_as_the_library_and_not_as_the_export`

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
- Collected: 235 against a baseline of 235
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_a_library_that_went_missing`
  - `tests/test_intake_land.py::test_a_recorded_abort_is_honored_over_an_export_that_went_missing`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_stale_answer_stays_stale_over_an_export_that_is_not_there`

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
- Collected: 235 against a baseline of 235
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land.py::test_the_plan_read_hands_the_engine_the_manifest_rows_the_gate_will_show`

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
- Collected: 235 against a baseline of 235
- Kills: 102 (killed)
- Killed:
  - `tests/test_intake_imported.py::test_a_landing_followed_step_by_step_passes_the_cutover_precheck`
  - `tests/test_intake_imported.py::test_a_named_run_that_is_not_waiting_is_refused`
  - `tests/test_intake_imported.py::test_a_partly_imported_batch_is_not_imported`
  - `tests/test_intake_imported.py::test_a_refused_close_is_reported_and_tried_again_next_time`
  - `tests/test_intake_imported.py::test_a_retire_that_cannot_rename_is_a_refusal_and_changes_nothing`
  - `tests/test_intake_imported.py::test_a_run_landed_before_the_fix_is_settled_too`
  - `tests/test_intake_imported.py::test_a_run_the_export_does_not_prove_is_named_beside_the_one_it_does`
  - `tests/test_intake_imported.py::test_a_run_the_ledger_names_no_file_for_is_left_alone`
  - `tests/test_intake_imported.py::test_a_stub_listing_is_refused_as_the_export`
  - `tests/test_intake_imported.py::test_a_verified_run_stays_open_with_its_placements_still_owed`
  - `tests/test_intake_imported.py::test_a_waiting_run_with_no_export_named_is_refused_and_says_what_to_pass`
  - `tests/test_intake_imported.py::test_a_waiting_run_with_tracks_still_outstanding_is_not_called_imported`
  - `tests/test_intake_imported.py::test_after_a_cutover_the_pass_placing_every_track_is_proof_and_closes_the_run`
  - `tests/test_intake_imported.py::test_an_export_taken_before_the_import_proves_nothing_and_changes_nothing`
  - `tests/test_intake_imported.py::test_an_intake_file_no_waiting_run_names_is_still_refused_as_the_export`
  - ... and 87 more, see the JSON sidecar

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
- Collected: 235 against a baseline of 235
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_unmounted_library_is_named_as_the_library_and_not_as_the_export`
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
- Collected: 235 against a baseline of 235
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land.py::test_an_intake_file_already_there_refuses_before_the_gate`
  - `tests/test_intake_land.py::test_the_lock_is_released_after_a_landing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_intake_file_already_there]`
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

### `u220.A10_wrong_status`

_stale_tag: look for a 409 rather than the 412 the provider answers

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A10_wrong_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag`
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_whose_tag_never_comes_fresh_is_sent_a_bounded_number_of_times`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`
  - `tests/test_outbound_order.py::test_the_pauses_after_a_412_start_again_for_each_move`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`

Old text:

```
        if status == PRECONDITION_FAILED:
```

New text:

```
        if status == 409:
```

### `u220.A11_cause_chain_only`

_stale_tag: walk the cause chain alone, so a 412 the client failed to decode is missed (round one R3)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A11_cause_chain_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_whose_body_is_not_json_is_still_read_as_a_stale_tag`

Old text:

```
(one.__cause__, one.__context__)
```

New text:

```
(one.__cause__,)
```

### `u220.A12_no_memory_guard`

order_tracks: ignore what this command's adds left, so a first reading lagging them is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A12_no_memory_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_order.py::test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move`

Old text:

```
        known = self._members.get(identifier)
```

New text:

```
        known = None
```

### `u220.A13_exact_agrees`

_settled: read any reading as agreeing with the caller's expected one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A13_exact_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`

Old text:

```
            if exact:
                return list(dict.fromkeys(reading)) == list(dict.fromkeys(known))
```

New text:

```
            if exact:
                return True
```

### `u220.A14_multiset_agrees`

_settled: read any reading as holding what is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A14_multiset_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return True
```

### `u220.A17_settle_once`

_settled: take one reading only, never again after a pause

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A17_settle_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_reading_that_never_agrees_with_the_expected_one_refuses_with_nothing_moved`
  - `tests/test_outbound_order.py::test_the_reading_after_adds_that_lags_them_is_read_again_before_the_first_move`

Old text:

```
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

New text:

```
        last: CratekitError | None = None
        for attempt in range(1):
```

### `u220.A1_front_target`

order_tracks: move each track to the playlist's length instead of the front, the move whose landing depends on how the provider counts

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A1_front_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_every_move_is_to_the_front_where_both_ways_of_counting_agree`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[False]`
  - `tests/test_outbound_order.py::test_the_reading_after_a_412_is_held_to_what_the_adds_left[True]`
  - `tests/test_outbound_order.py::test_the_tracks_before_the_kept_tail_are_moved_last_first`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
playlist.move_by_indices([at], 0)
```

New text:

```
playlist.move_by_indices([at], len(before))
```

### `u220.A23_pause_index`

_pause: index the pauses by the attempt with no repeat of the last

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A23_pause_index`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 287 against a baseline of 287
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_more_412s_than_pauses_repeat_the_last_pause`

Old text:

```
    return ORDER_PAUSES[min(attempt, len(ORDER_PAUSES)) - 1]
```

New text:

```
    return ORDER_PAUSES[attempt - 1]
```

### `u293.G1_night_line_asked`

Gate.call: never ask the night's line, so a night pass spends past its budget

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G1_night_line_asked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops`
  - `tests/test_provider_gate_night.py::test_an_inherited_night_line_stops_a_child_at_the_nights_remainder`
  - `tests/test_provider_gate_night.py::test_another_processs_calls_count_against_the_night`
  - `tests/test_provider_gate_night.py::test_outside_any_command_a_line_off_the_environment_holds_the_call`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`

Old text:

```
                if held_night is not None and (
```

New text:

```
                if False and (
```

### `u293.G2_night_line_off_by_one`

Gate.call: stop only past the line, so one call beyond the night's budget is sent

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G2_night_line_off_by_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_an_inherited_night_line_stops_a_child_at_the_nights_remainder`
  - `tests/test_provider_gate_night.py::test_another_processs_calls_count_against_the_night`
  - `tests/test_provider_gate_night.py::test_outside_any_command_a_line_off_the_environment_holds_the_call`
  - `tests/test_provider_gate_night.py::test_the_call_past_the_nights_line_is_never_sent_and_parks_naming_the_night`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`

Old text:

```
                    state.calls - held_night.start >= held_night.budget
```

New text:

```
                    state.calls - held_night.start > held_night.budget
```

### `u293.G3_total_below_mark`

Gate.call: a total below the night's mark reads as nothing spent rather than stopping

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G3_total_below_mark`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_total_below_the_mark_is_a_spend_nobody_can_read_and_stops`

Old text:

```
                    or state.calls < held_night.start
```

New text:

```
                    or False
```

### `u293.G4_child_reads_no_line`

command: a scope opened in a child reads no night line off the environment

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G4_child_reads_no_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_line_read_off_the_environment_is_held_beside_the_ceiling`
  - `tests/test_provider_gate_night.py::test_an_inherited_night_line_stops_a_child_at_the_nights_remainder`

Old text:

```
        night=_night_from_env(),
```

New text:

```
        night=None,
```

### `u293.G5_line_held_to_ceiling`

night: the firing's line is the night's remainder alone, past one command's ceiling

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G5_line_held_to_ceiling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_ceiling_raised_through_the_environment_never_widens_a_firing`
  - `tests/test_provider_gate_night.py::test_the_line_is_held_to_what_the_command_has_left_of_its_ceiling`
  - `tests/test_provider_gate_night.py::test_the_nights_line_is_held_to_what_is_left_of_the_command_ceiling`
  - `tests/test_sync_night.py::test_a_firing_that_died_is_charged_to_the_next_of_the_same_night`
  - `tests/test_sync_night.py::test_the_pass_runs_under_the_nights_line_and_hour`

Old text:

```
budget=max(0, min(int(calls), left_of_ceiling))
```

New text:

```
budget=max(0, int(calls))
```

### `u293.G6_nested_lower_line`

night: a nested line widens the outer night's remainder

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G6_nested_lower_line`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_a_nested_night_keeps_the_lower_line`

Old text:

```
        if left < held.budget:
```

New text:

```
        if False:
```

### `u293.G7_hour_never_raised`

night: the night's hour replaces the configured one, raising it when set higher

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G7_hour_never_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_night_lowers_the_hour_and_never_raises_it`

Old text:

```
    hour = min(hourly(settings), max(1, int(calls_per_hour)))
```

New text:

```
    hour = max(1, int(calls_per_hour))
```

### `u293.G8_line_exported`

night: the line is not exported, so a detached child runs without it

- File: `src/cratekit/core/provider_gate.py`
- Source: `u293.json`, row `G8_line_exported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_gate_night.py`, `tests/test_provider_gate.py`, `tests/test_provider_budget.py`, `tests/test_sync_night.py`
- Collected: 280 against a baseline of 280
- Kills: 2 (killed)
- Killed:
  - `tests/test_provider_gate_night.py::test_the_line_reaches_a_child_through_the_environment_and_is_put_back`
  - `tests/test_sync_night.py::test_the_pass_runs_under_the_nights_line_and_hour`

Old text:

```
        with _exported(NIGHT_ENV, held.to_env()), _exported(BUDGET_ENV, hour):
```

New text:

```
        with _exported(NIGHT_ENV, None), _exported(BUDGET_ENV, hour):
```

### `u213.M1_first_group_is_the_title`

split_version: drop the first group rule, so a title written wholly in brackets walks off whole and the row names no title

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M1_first_group_is_the_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
- Kills: 13 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[  [Premade Sandwiches]  -expected2]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Premade Sandwiches)-expected1]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Love) (Remix)-expected12]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Or Without You)-expected9]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You)-expected10]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(feat. Mira)-expected13]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (Live)-expected3]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches]-expected0]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[With You]-expected8]`

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
            remaining = inside
            break
```

New text:

```
        if False:
            remaining = inside
            break
```

### `u213.M3_first_group_position`

split_version: take any group as the title, not only the one standing first, so Song (Remix) reads as Remix

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M3_first_group_position`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
- Kills: 16 (killed)
- Killed:
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[spotify-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path (Live) (feat. Mira)-provider0-spelled_addresses0-provider_addresses0]`
  - `tests/test_match_states.py::test_a_credited_listing_is_never_addressed_as_the_plain_record[text-Sun Path [Live] (feat. Mira)-provider1-spelled_addresses1-provider_addresses1]`
  - `tests/test_match_states.py::test_a_credited_rows_suppression_spellings_are_unchanged[Sun Path (Nightwave Remix) (ft Mira)-addresses1]`
  - `tests/test_match_states.py::test_a_featured_credit_is_a_performer_and_never_a_version`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[Featuring Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[feat. Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[ft Anna]`
  - `tests/test_match_states.py::test_a_group_whose_first_word_is_a_credit_still_comes_off[with Anna]`
  - `tests/test_match_states.py::test_a_held_file_crediting_somebody_else_never_calls_the_companion_stale`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_of_two_near_hits_only_the_one_whose_title_resembles_is_offered`
  - `tests/test_match_states.py::test_the_companion_reaches_exactly_what_ownership_reached`
  - `tests/test_match_states.py::test_the_offer_limit_keeps_the_best_scoring_answers_and_says_what_it_kept_back`
  - ... and 1 more, see the JSON sidecar

Old text:

```
        if found.start() == 0 and not _names_a_version(inside):
```

New text:

```
        if found.start() >= 0 and not _names_a_version(inside):
```

### `u213.M4_first_group_keeps_brackets`

split_version: keep the brackets on a title written wholly in them

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M4_first_group_keeps_brackets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
- Kills: 15 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_row_titled_wholly_in_brackets_is_queued_under_its_words`
  - `tests/intake/test_workers.py::test_a_set_aside_track_names_the_half_the_reader_names`
  - `tests/test_match_states.py::test_a_headed_tag_titled_wholly_in_brackets_matches_the_provider_row`
  - `tests/test_match_states.py::test_a_provider_row_titled_wholly_in_brackets_reads_rather_than_refuses`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[  [Premade Sandwiches]  -expected2]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Premade Sandwiches)-expected1]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Love) (Remix)-expected12]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(With Or Without You)-expected9]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(Without You)-expected10]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[(feat. Mira)-expected13]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (Live)-expected3]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches] (feat. Mira)-expected4]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[Premade Sandwiches]-expected0]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[With You]-expected8]`
  - `tests/test_match_states.py::test_a_title_written_wholly_in_brackets_keeps_its_words[[]-expected7]`

Old text:

```
            remaining = inside
            break
```

New text:

```
            remaining = found.group(0).strip()
            break
```

### `u213.M5_listed_names_artist`

listed_names: read no artist off a refused row

- File: `src/cratekit/acquire/match.py`
- Source: `u213.json`, row `M5_listed_names_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_sync_twins.py`
- Collected: 763 against a baseline of 763
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_the_readable_listing_sets_aside_a_refused_row_by_id_in_its_place`
  - `tests/test_match_states.py::test_listed_names_reads_a_row_the_reader_refuses`
  - `tests/test_sync_twins.py::test_a_track_listed_with_no_title_is_named_in_its_twin_and_the_rest_are_planned`

Old text:

```
    return str(_field(row, "id", "")).strip(), _artist_of(row), _raw_title(row)
```

New text:

```
    return str(_field(row, "id", "")).strip(), "", _raw_title(row)
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

### `u146-b.B14_plan_owned_keeps_held_hearts`

plan_owned: an owned heart All Favorites holds is planned too, so an empty landing gives it a month

- File: `src/cratekit/favorites/backfill.py`
- Source: `u146-b.json`, row `B14_plan_owned_keeps_held_hearts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing`

Old text:

```
        one for one in owned_in_library(cfg, db, rows) if one.content_id not in in_source
```

New text:

```
        one for one in owned_in_library(cfg, db, rows)
```

### `u146-b.A1_superseded_ignored`

owned_hearts: an older pass places its owned hearts though a later hearts job ran, putting back a heart dropped since

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A1_superseded_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_landing_an_older_pass_places_no_owned_heart_once_a_later_hearts_job_ran`

Old text:

```
    if superseded:
        return ()
```

New text:

```
    if superseded and False:
        return ()
```

### `u146-b.A2_owned_reads_carried`

owned_hearts: reads the carried states, so the landing finds no owned heart

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A2_owned_reads_carried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 12 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
    return hearts(cfg, pass_name, states=frozenset({OWNED}))
```

New text:

```
    return hearts(cfg, pass_name)
```

### `u146-b.A3_report_paths_dropped`

carried_hearts: the report's files are not carried on the row, so no owned heart has a row to place

- File: `src/cratekit/intake/account_playlists.py`
- Source: `u146-b.json`, row `A3_report_paths_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_present_coloured_owned_heart_beside_a_landed_file_is_held_and_named`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`

Old text:

```
                known=intake_cli.HEARTED in said,
                paths=tuple(str(path) for path in (report.get("paths") or ())),
```

New text:

```
                known=intake_cli.HEARTED in said,
                paths=(),
```

### `u146-c.L2_empty_landing_no_op`

_land_native: an empty landing ends NO_OP as before, its owned hearts never placed

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L2_empty_landing_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 7 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_a_track_removed_from_all_favorites_by_hand_and_still_hearted_joins_again`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_is_coloured_pink_and_one_a_person_coloured_is_held`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_the_account_dates_nowhere_goes_to_undated`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_only_pass_refuses_before_the_gate_with_no_acknowledgment`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_track_hearted_today_joins_all_favorites_and_its_month_with_nothing_downloaded`
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if owned:
            return _place_owned(
```

New text:

```
        if owned and False:
            return _place_owned(
```

### `u146-c.L3_gate_asked_for_nothing`

_place_owned: a pass whose owned hearts are all placed opens the database to write and asks the gate over nothing

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L3_gate_asked_for_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_a_pass_whose_owned_hearts_are_all_placed_asks_nothing_and_ends_no_op`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_without_a_month_is_no_write_for_an_empty_landing`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_file_two_rows_claim_is_not_placed_by_a_guess`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_whose_job_froze_no_date_key_is_left_to_the_backfill`

Old text:

```
    if not first.writes:
        return ctx.envelope(data=empty, outcome=Outcome.NO_OP)
```

New text:

```
(empty)
```

### `u146-c.L4_missing_source_refuses`

_place_owned: a library with no All Favorites refuses the empty landing instead of ending NO_OP and saying why

- File: `src/cratekit/intake/land_cli.py`
- Source: `u146-c.json`, row `L4_missing_source_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_with_no_all_favorites_an_owned_only_pass_ends_no_op_and_says_why`

Old text:

```
        if exc.cause.reason != placement.SOURCE_MISSING:
            raise
        return ctx.envelope(
            data=empty,
```

New text:

```
        raise
        return ctx.envelope(
            data=empty,
```

### `u146-c.N1_owned_held_planned`

_favorites_plan: an owned heart All Favorites holds is planned again beside a landing, and its month made

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N1_owned_held_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_all_favorites_holds_is_no_write_beside_a_landing`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_placed_by_hand_between_the_two_acts_makes_the_answer_stale`

Old text:

```
        if one.content_id in in_source or one.content_id in seen:
```

New text:

```
        if one.content_id in seen:
```

### `u146-c.N2_owned_not_written`

apply_rows: the owned hearts are planned and shown and never written

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N2_owned_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_in_the_same_commit_as_a_downloaded_one`

Old text:

```
                pairs.extend((one.content_id, one.month) for one in plan.favorites.owned)
```

New text:

```
(empty)
```

### `u146-c.N4_owned_needs_a_heart_file`

_favorites_plan: owned hearts are placed only when a landed file is a heart too

- File: `src/cratekit/intake/native.py`
- Source: `u146-c.json`, row `N4_owned_needs_a_heart_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_joins_beside_a_landed_file_that_is_no_heart`

Old text:

```
    if not (kept or owned) or not source:
```

New text:

```
    if not kept or not source:
```

### `u146-e.N3_owned_out_of_digest`

FavoritesPlan.identity: the owned hearts are not digested, so an answer given for one set of them stands for another

- File: `src/cratekit/intake/native.py`
- Source: `u146-e.json`, row `N3_owned_out_of_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 22933 against a baseline of 22933
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        if self.owned:
            identity["owned"] = [
```

New text:

```
        if self.owned and False:
            identity["owned"] = [
```

### `u153.N3_landing_colour_owned`

native apply: drop the owned hearts from the colour set, so an owned heart is placed but not coloured

- File: `src/cratekit/intake/native.py`
- Source: `u153.json`, row `N3_landing_colour_owned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_owned_hearts_native.py`
- Collected: 18 against a baseline of 18
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_owned_hearts_native.py::test_an_owned_heart_beside_a_landed_file_takes_pink_in_the_same_commit`

Old text:

```
                to_colour.extend(plan.favorites.colour)
```

New text:

```
                to_colour.extend([])
```

### `u105-b.S10_settings_to_engine`

Call the engine without the settings built from the frozen target

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S10_settings_to_engine`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
            settings=settings,
            output_dir=Path(output_dir) if output_dir else None,
```

New text:

```
            output_dir=Path(output_dir) if output_dir else None,
```

### `u105-b.S1_parts_only_when_several`

Freeze the parts key for a single recording too

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S1_parts_only_when_several`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 3 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_job_seam.py::test_the_partial_encode_a_kill_leaves_behind_is_in_staging_not_at_the_destination`
  - `tests/test_master_cli.py::test_one_input_freezes_queues_and_resumes_exactly_as_before`

Old text:

```
    if len(frozen) > 1:
```

New text:

```
    if frozen:
```

### `u105-b.S2_lufs_frozen`

Do not freeze --lufs into the payload

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S2_lufs_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_the_target_reaches_every_loudnorm_filter`

Old text:

```
        payload[TARGET_LUFS] = float(lufs)
```

New text:

```
        pass
```

### `u105-b.S3_lufs_in_argv`

Drop --lufs from the resume command line

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S3_lufs_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
        argv.append(f"--lufs={lufs}")
```

New text:

```
        pass
```

### `u105-b.S4_parts_in_argv`

Rebuild the resume command line from the first part alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S4_parts_in_argv`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_split_recording_and_its_target_survive_the_resume_argv`

Old text:

```
    argv = ["master", *frozen_parts(payload)]
```

New text:

```
    argv = ["master", str(payload.get(SOURCE) or "")]
```

### `u105-b.S5_queue_time_refusal`

Stop validating --lufs at queue time

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S5_queue_time_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 3 (killed)
- Killed:
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-4]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[-71]`
  - `tests/test_master_cli.py::test_an_out_of_range_target_refuses_and_queues_nothing[nan]`

Old text:

```
    settings_for(ctx.args.lufs)
```

New text:

```
    pass
```

### `u105-b.S6_join_order_notice`

Queue a split recording without saying its order back

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S6_join_order_notice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_the_order_printed_is_the_order_given`

Old text:

```
        notices = (join_order_warning(frozen_parts(payload)),) if PARTS in payload else ()
```

New text:

```
        notices = ()
```

### `u105-b.S7_staged_parts`

Stage a split recording's run without its parts, mastering part one alone

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S7_staged_parts`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[PARTS] = [str(p) for p in parts]
```

New text:

```
        pass
```

### `u105-b.S8_staged_target`

Stage the run without the frozen target, mastering at the default

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S8_staged_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`

Old text:

```
        staged[TARGET_LUFS] = payload[TARGET_LUFS]
```

New text:

```
        pass
```

### `u105-b.S9_precheck_name`

Pre-check the destination with part one's master name instead of the joined one

- File: `src/cratekit/master/cli.py`
- Source: `u105-b.json`, row `S9_precheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`, `tests/test_tagging_engine.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`

Old text:

```
    final = mastering.planned_output(
        parts, output_dir=Path(str(output_dir)) if output_dir else None
    )
```

New text:

```
    final = mastering.output_path(
        parts[0], output_dir=Path(str(output_dir)) if output_dir else None
    )
```

### `u177.A10_clear_word`

registry_cmd: drop the clear word, so --bandcamp default stores an account named default

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A10_clear_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`

Old text:

```
    clear_bandcamp = bandcamp is not None and bandcamp.strip().lower() == labels.CLEAR_BANDCAMP

```

New text:

```
    clear_bandcamp = False

```

### `u177.A11_field_flag_guard`

registry_cmd: leave --bandcamp out of the fields given, so remove --bandcamp is silently ignored and set --bandcamp alone refused

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A11_field_flag_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_label_setting_its_own_account_again_is_no_conflict`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_bandcamp_on_an_action_that_does_not_set_it_refuses[action0]`
  - `tests/test_label_bandcamp_account.py::test_bandcamp_on_an_action_that_does_not_set_it_refuses[action1]`
  - `tests/test_label_bandcamp_account.py::test_bandcamp_on_an_action_that_does_not_set_it_refuses[action2]`
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`
  - `tests/test_label_bandcamp_account.py::test_set_with_only_bandcamp_is_a_field_to_change`

Old text:

```
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre, bandcamp)

```

New text:

```
    fields_given = (seeds, track_limit, ctx.args.match, offer, kind, genre)

```

### `u177.A9_add_drops_account`

registry_cmd add: pass no account to the store, so add --bandcamp is accepted and never written

- File: `src/cratekit/label/cli.py`
- Source: `u177.json`, row `A9_add_drops_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 12 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_rename_of_the_label_keeps_its_seller`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_a_seller_on_its_own_domain_keeps_the_whole_host`
  - `tests/test_label_bandcamp_account.py::test_add_with_an_account_round_trips_through_list`
  - `tests/test_label_bandcamp_account.py::test_an_account_named_default_is_set_by_its_address`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[  pulsromania  ]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[PulsRomania]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://PulsRomania.bandcamp.com/music]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[https://pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com/album/sun-path]`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[pulsromania.bandcamp.com]`
  - `tests/test_label_bandcamp_account.py::test_set_of_another_field_keeps_the_account`

Old text:

```
            genre=genre,
            clear_genre=clear_genre,
            bandcamp=bandcamp,
            clear_bandcamp=clear_bandcamp,
        )
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held, _routed(label_id, route)),

```

New text:

```
            genre=genre,
            clear_genre=clear_genre,
            bandcamp=None,
            clear_bandcamp=clear_bandcamp,
        )
        held = store.load()
        return ctx.envelope(
            data={
                "checks": _checks_for(held, _routed(label_id, route)),

```

### `u177.A1_account_suffix`

bandcamp_account: keep .bandcamp.com on the host, so an address is stored as a host no purchase's seller equals

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A1_account_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 23 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_a_fetch_of_no_labels_release_names_no_label_landing`
  - `tests/test_bandcamp_labels.py::test_a_file_that_would_not_take_the_label_is_staged_named_and_fails_its_item`
  - `tests/test_bandcamp_labels.py::test_a_label_whose_purchases_are_all_filtered_is_not_said_to_stage`
  - `tests/test_bandcamp_labels.py::test_a_registered_sellers_files_stage_with_the_label_on_every_one`
  - `tests/test_bandcamp_labels.py::test_a_rename_after_the_queue_tags_by_the_label_frozen_with_the_job`
  - `tests/test_bandcamp_labels.py::test_a_resumed_fetch_names_the_label_landing_too`
  - `tests/test_bandcamp_labels.py::test_a_seller_with_nothing_to_fetch_is_not_asked_to_register`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_seller_is_named_with_the_command_that_registers_it`
  - `tests/test_bandcamp_labels.py::test_an_unregistered_sellers_files_stage_with_no_label_tag`
  - `tests/test_bandcamp_labels.py::test_seller_by_label_name_fetches_only_that_labels_releases`
  - `tests/test_bandcamp_labels.py::test_seller_takes_a_registered_labels_name_and_plans_what_its_account_does`
  - `tests/test_bandcamp_labels.py::test_the_fetch_names_the_landing_that_files_the_batch_by_label`
  - `tests/test_bandcamp_labels.py::test_the_job_freezes_each_releases_label`
  - `tests/test_bandcamp_labels.py::test_the_landing_the_fetch_names_is_one_the_landing_verb_parses`
  - `tests/test_bandcamp_labels.py::test_the_plan_names_each_rows_label_and_none_for_a_seller_no_label_names`
  - ... and 8 more, see the JSON sidecar

Old text:

```
    if host.endswith(_ACCOUNT_HOST):
        host = host[: -len(_ACCOUNT_HOST)]
    if not host or not _ACCOUNT.fullmatch(host):

```

New text:

```
    if not host or not _ACCOUNT.fullmatch(host):

```

### `u177.A2_account_shape`

bandcamp_account: drop the shape check, so an account with a space is stored and matches no purchase

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A2_account_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_malformed_stored_account_is_no_account_and_the_label_keeps_the_rest`
  - `tests/test_label_bandcamp_account.py::test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing[-puls]`
  - `tests/test_label_bandcamp_account.py::test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing[puls romania]`
  - `tests/test_label_bandcamp_account.py::test_an_account_that_could_match_no_purchase_is_refused_and_writes_nothing[puls_romania]`

Old text:

```
    if not host or not _ACCOUNT.fullmatch(host):

```

New text:

```
    if not host:

```

### `u177.A3_account_case`

bandcamp_account: keep the case typed, so PulsRomania never equals the purchase's pulsromania

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A3_account_case`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 5 (killed)
- Killed:
  - `tests/test_bandcamp_labels.py::test_the_label_written_is_the_display_name_and_the_record_names_it`
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_an_account_is_looked_up_in_any_form_a_purchase_could_name_it`
  - `tests/test_label_bandcamp_account.py::test_an_address_or_any_case_is_stored_as_the_account_a_purchase_is_read_as[PulsRomania]`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
    text = account.strip().lower() if isinstance(account, str) else ""

```

New text:

```
    text = account.strip() if isinstance(account, str) else ""

```

### `u177.A4_claim_removed`

_claim: return at once, so a second label naming a held account is written beside the first

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A4_claim_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_second_label_naming_a_held_account_is_refused_by_the_holders_name`
  - `tests/test_label_bandcamp_account.py::test_the_store_refuses_a_second_claimant_from_a_python_caller`

Old text:

```
    if account is None:
        return
    for other in current.values():

```

New text:

```
    if True:
        return
    for other in current.values():

```

### `u177.A5_claim_self`

_claim: count the label itself as a claimant, so setting its own account again is refused

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A5_claim_self`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_label_setting_its_own_account_again_is_no_conflict`

Old text:

```
        if other.label_id != label_id and other.bandcamp == account:

```

New text:

```
        if other.bandcamp == account:

```

### `u177.A7_stored_raw`

_stored_account: keep a stored account as written, so a hand written address matches no purchase

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A7_stored_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_a_malformed_stored_account_is_no_account_and_the_label_keeps_the_rest`
  - `tests/test_label_bandcamp_account.py::test_two_labels_naming_one_account_by_hand_answer_no_label`

Old text:

```
    try:
        return bandcamp_account(value)
    except CratekitError:
        return None

```

New text:

```
    return value

```

### `u177.A8_edit_drops_account`

edit: keep the held account, so registry set --bandcamp reports a change it never writes

- File: `src/cratekit/label/registry.py`
- Source: `u177.json`, row `A8_edit_drops_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_bandcamp_account.py`, `tests/test_label_registry_verbs.py`, `tests/test_bandcamp_labels.py`, `tests/test_label_genre.py`
- Collected: 144 against a baseline of 144
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_bandcamp_account.py::test_default_clears_the_account_and_frees_it_for_another_label`
  - `tests/test_label_bandcamp_account.py::test_set_with_only_bandcamp_is_a_field_to_change`

Old text:

```
                else (bandcamp if bandcamp is not None else existing.bandcamp),

```

New text:

```
                else existing.bandcamp,

```

### `r777-confirm.N4_plain_name`

Confirm: _native_proof takes a pass name no landing could have been given, after the test that pins its message

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r777-confirm.json`, row `N4_plain_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_intake_land_names.py`, `tests/test_sync_mark.py`
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
- Collected: 141 against a baseline of 141
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
  - `tests/test_session_cli.py::test_a_live_lock_holder_refuses_and_abandons_nothing`

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
  - `tests/test_session_cli.py::test_a_hard_killed_gated_write_blocks_cutover_until_release_abandons_it`
  - `tests/test_session_cli.py::test_a_power_loss_blocks_cutover_until_release_abandons_it`

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
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[another-machine-with-this-host-name]`
  - `tests/test_session_cli.py::test_a_record_from_another_boot_not_proven_this_machines_is_kept[recorded-before-the-machine-identity]`
  - `tests/test_session_cli.py::test_a_record_whose_holder_is_alive_is_kept_open`
  - `tests/test_session_cli.py::test_an_open_record_that_names_no_holder_is_never_abandoned`

Old text:

```
    kept = [record.session_id for record in session.records(cfg) if not record.terminal]
```

New text:

```
    kept = []
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

