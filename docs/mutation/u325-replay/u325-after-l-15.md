# Mutation table: u325-after-l-15

Measured by `scripts/mutate.py` on 2026-11-23 00:22 UTC, branch `HEAD` at `db120fdb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 142.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:22 UTC for commit `db120fdb9f05`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 10, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u154.G7_run_id_shape_unread` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 4 | killed |
| `u154.G8_free_target_no_suffix` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 3 | killed |
| `u154.R1_rows_under_target_not_consulted` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.R3_repeated_name_planned_twice` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.R6_device_probe_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.R7_exact_prefix_filter_dropped` | `src/cratekit/intake/shelve.py` | maintainer | 1 file(s) | 43 | 1 | killed |
| `u235.H1_shelve_four_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 2 | killed |
| `u235.H2_shelve_sixteen_hex_only` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 2 | killed |
| `r682-a.M2_non_string_why_counted` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `r682-a.M3_empty_why_counted` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `r682-a.M4_state_keys_not_seeded` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 3 | killed |
| `r682-a.M5_reason_counted_twice` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 4 | killed |
| `r682-a.M6_reason_counted_outside_state_guard` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `r706-c.C1_parts_note_never_said` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 2 | killed |
| `r706-c.C3_summary_ignores_the_payload` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `r925.S2_out_ignored` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `r925.S4_write_failure_refuses` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `r925.S5_unwritten_note_names_no_job_show` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `u120.L1_date_frozen_when_none` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `u120.L2_date_added_ignored` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `u57-recognition-and-items.C3_missing_ref_not_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 2 | killed |
| `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `u57-recognition-and-items.C7_foreign_job_driven` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 1 | killed |
| `u70.E1_missing_id_refused` | `src/cratekit/intake/cli.py` | user | 1 file(s) | 108 | 2 | killed |
| `u134-a.A10_shared_playlist` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A11_pass_unknown` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A1_outside_inbox` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A2_mirror_is_first` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A3_gone_listed` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A4_others_excluded` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A5_unreadable` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A6_pre_u128_exact_name` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A7_pass_matched` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-a.A8_only_what_it_lacks` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 3 | killed |
| `u134-b.B1c_composite_short_write` | `src/cratekit/intake/refill.py` | maintainer | 1 file(s) | 22 | 8 | killed |
| `u134-b.B2c_composite_reversed_write` | `src/cratekit/intake/refill.py` | maintainer | 1 file(s) | 22 | 8 | killed |
| `u134-b.B4_record_on_success` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-b.B7_again_action` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F1_bridge_name_unasked` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F2_bridge_names_any_account` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F4_bridge_names_any_state` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u175.F5_bridge_names_by_id_order` | `src/cratekit/intake/refill.py` | user | 1 file(s) | 22 | 1 | killed |
| `u134-b.B5_no_writes_no_op` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 22 | 3 | killed |
| `u134-b.B6_ack_before_gate` | `src/cratekit/intake/refill_cli.py` | user | 1 file(s) | 22 | 1 | killed |
| `r239-b.S11_readback_key_on` | `src/cratekit/core/session.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S6_delete_key_off` | `src/cratekit/deletion/cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S10_adopt_apply_key_off` | `src/cratekit/adopt/apply_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S7_metadata_key_off` | `src/cratekit/write/metadata_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `r239-b.S2_unplaced_key_off` | `src/cratekit/write/routing_cli.py` | user | 7 file(s) | 733 | 2 | killed |
| `r239-b.S8_naming_key_off` | `src/cratekit/write/naming_cli.py` | user | 7 file(s) | 733 | 1 | killed |
| `u178.S1_summary_counts_labels` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 5 | killed |
| `u178.S2_unknown_label_refused` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S3_unreadable_registry_refuses_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.S4_genres_frozen` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 13 | killed |
| `u178.S5_worker_takes_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 7 | killed |
| `u178.S6_outranked_needs_label` | `src/cratekit/tagging/cli.py` | user | 3 file(s) | 236 | 4 | killed |
| `u178-e9.E9_label_tag_reset` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E2_no_search_with_picture` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 11 | killed |
| `u178.E3_art_refusal_tolerated` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E4_isrc_withheld` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E6_label_write_checked` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u178.E7_catalogue_write_checked` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 236 | 1 | killed |
| `u174.M10_dedupe` | `src/cratekit/sync/mark_cli.py` | maintainer | 3 file(s) | 191 | 1 | killed |
| `u174.M11_stranger_before_no_jobs` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M1_stranger_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 2 | killed |
| `u174.M2_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 4 | killed |
| `u174.M3_unfinished_refusal` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 3 | killed |
| `u174.M4_unfinished_rows_outstanding` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M5_unfinished_job` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M6_unfinished_reports` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M7_digest_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 2 | killed |
| `u174.M8_screen_names_the_narrowing` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.M9_verb_passes_the_flag` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 5 | killed |
| `u174.P1_bridge_plans_no_native_pass` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `u174.P2_unreachable_is_refused` | `src/cratekit/sync/mark_cli.py` | user | 3 file(s) | 191 | 1 | killed |
| `r1091.K10_available_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K11_year_dropped` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K12_periodic_write_off` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K13_write_error_raised` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 6 | killed |
| `r1091.K14_unkept_never_cleared` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K15_reuse_uncounted` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 3 | killed |
| `r1091.K1_age_never_expires` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K2_future_is_fresh` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K3_age_boundary` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K4_age_coefficient` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 4 | killed |
| `r1091.K5_version_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K6_label_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K7_gone_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `r1091.K8_year_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 2 | killed |
| `r1091.K9_track_shape_unchecked` | `src/cratekit/label/kept_reads.py` | user | 3 file(s) | 124 | 1 | killed |
| `u54-acquisition-worker.G10_absent_result` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G11_not_acquired` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 8 | killed |
| `u54-acquisition-worker.G12_landing_check` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-acquisition-worker.G14_marker_applied` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G15_no_marker_text` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G17_paced_sleep_bound` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 2 | killed |
| `u54-acquisition-worker.G19_frozen_config` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 40 | killed |
| `u54-acquisition-worker.G1_origin_refusal` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G20_output_exists` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G27_remedy_absent_stays_absent` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G28_marker_decided_by_the_file` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G29_auth_failure_parks` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 3 | killed |
| `u54-acquisition-worker.G2_missing_identifier` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G8_park_on_block` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `u54-acquisition-worker.G9_failed_invocation` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 5 | killed |
| `u54-zero-row-remeasured.G7_staging_cleared` | `src/cratekit/acquire/cli.py` | user | 2 file(s) | 93 | 1 | killed |
| `r342.E1_cut_inclusive` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V13_detail_key` | `src/cratekit/write/metadata_cli.py` | maintainer | 1 file(s) | 26 | 10 | killed |
| `r342.V1_default_on_corrupt` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 12 | killed |
| `r342.V2_no_finite_check` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `r342.V3_isnan_for_isfinite` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V4_no_bool_check` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V5_tuple_drops_overflow` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V6_tuple_drops_keyerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r342.V7_tuple_drops_typeerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `r342.V8_tuple_drops_valueerror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `r342.V9_tuple_drops_oserror` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M2_a_noop_claims_a_commit` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M3_witnessed_commit_not_recorded` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M4_summary_keyed_on_the_display_name` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G10_ignore_cut` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G11_gender_without_vox` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G12_apply_by_default` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G13_skip_apply_gate` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 8 | killed |
| `u25.G24_content_column` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `r592-a.A1_occupancy_guard_removed` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-a.A2_database_dropped_from_fileset` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 3 | killed |
| `r592-a.A3_companions_dropped_from_fileset` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |
| `r592-a.A4_fileset_not_rebased` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 4 | killed |
| `r592-a.A5_replacing_existing_inverted` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 8 | killed |
| `r592-a.A6_old_suffix_rule_restored` | `src/cratekit/core/restore.py` | user | 2 file(s) | 257 | 2 | killed |

## Row definitions

### `u154.G7_run_id_shape_unread`

a batch named for its run identifier fits neither shape

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G7_run_id_shape_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
    run = _RUN_ID.match(batch)
    if run is not None:

```

New text:

```
    run = None
    if run is not None:

```

### `u154.G8_free_target_no_suffix`

a taken target is reused rather than given the next suffix

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G8_free_target_no_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_target_free_on_disk_but_holding_rows_in_the_collection_is_passed_over`
  - `tests/test_intake_shelve.py::test_a_target_made_after_the_plan_is_stale_and_the_folder_stays`
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:

```

New text:

```
    while False:

```

### `u154.R1_rows_under_target_not_consulted`

a target free on disk but holding collection rows is chosen

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R1_rows_under_target_not_consulted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_target_free_on_disk_but_holding_rows_in_the_collection_is_passed_over`

Old text:

```
    while os.path.lexists(candidate) or candidate in planned or spell(candidate) in stored_dirs:

```

New text:

```
    while os.path.lexists(candidate) or candidate in planned:

```

### `u154.R3_repeated_name_planned_twice`

a batch named twice is planned twice

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R3_repeated_name_planned_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_batch_named_twice_is_planned_once`

Old text:

```
    wanted = _candidates(cfg) if everything else list(dict.fromkeys(names))

```

New text:

```
    wanted = _candidates(cfg) if everything else list(names)

```

### `u154.R6_device_probe_dropped`

a processed tree on another device is planned and renamed into

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R6_device_probe_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_processed_tree_on_another_device_refuses_before_any_plan`

Old text:

```
    _assert_one_device(cfg, root)

```

New text:

```
    pass

```

### `u154.R7_exact_prefix_filter_dropped`

the confinement check judges the case blind LIKE result as is

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `R7_exact_prefix_filter_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_a_folder_differing_only_in_case_is_not_this_plans_business`

Old text:

```
            if str(row[1] or "").startswith(one.stored_target + os.sep)

```

New text:

```
            if True

```

### `u235.H1_shelve_four_hex_only`

intake.shelve: the run named batch pattern takes a four hex tail only, the round one finding, so a batch named for a run minted since U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H1_shelve_four_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[sixteen-hex-since-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-11-07T164826Z-ce458ab7cceccb0b-expected6]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{4}$")
```

### `u235.H2_shelve_sixteen_hex_only`

intake.shelve: the run named batch pattern takes a sixteen hex tail only, so a batch named for a run from before U235 is refused as carrying no date

- File: `src/cratekit/intake/shelve.py`
- Source: `u235.json`, row `H2_shelve_sixteen_hex_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_run_identifier_named_batch_files_as_downloads_or_as_the_subject_given[four-hex-before-u235]`
  - `tests/test_intake_shelve.py::test_parse_name_reads_the_two_shapes_and_refuses_the_rest[2026-09-23T222241Z-4773-expected5]`

Old text:

```
T\d{6}Z-(?:[0-9a-f]{4}|[0-9a-f]{16})$")
```

New text:

```
T\d{6}Z-[0-9a-f]{16}$")
```

### `r682-a.M2_non_string_why_counted`

a why that is not a string is counted under its own value as a slug

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M2_non_string_why_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
            if isinstance(why, str) and why:
```

New text:

```
            if why:
```

### `r682-a.M3_empty_why_counted`

an empty why is counted under the empty string as a reason

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M3_empty_why_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
            if isinstance(why, str) and why:
```

New text:

```
            if isinstance(why, str):
```

### `r682-a.M4_state_keys_not_seeded`

by_reason carries only the states some row reached, so suppressed with no rows is absent rather than an empty mapping

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M4_state_keys_not_seeded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 3 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`

Old text:

```
        "by_reason": by_reason,

```

New text:

```
        "by_reason": {word: reasons for word, reasons in by_reason.items() if reasons},

```

### `r682-a.M5_reason_counted_twice`

each row adds two to its reason, a realistic nearby coefficient

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M5_reason_counted_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`
  - `tests/intake/test_workers.py::test_a_set_job_runs_pending_to_done_and_reports_owned_offered_and_missing`
  - `tests/intake/test_workers.py::test_each_resolution_count_is_followed_by_its_reasons`
  - `tests/intake/test_workers.py::test_the_reasons_are_read_back_from_the_reports_on_every_resume`

Old text:

```
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
```

New text:

```
                by_reason[word][why] = by_reason[word].get(why, 0) + 2
```

### `r682-a.M6_reason_counted_outside_state_guard`

a reason is counted before the state word is checked, so a row in a state the counts do not know is counted under it

- File: `src/cratekit/intake/cli.py`
- Source: `r682-a.json`, row `M6_reason_counted_outside_state_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_report_without_a_reason_counts_in_its_state_and_under_no_reason`

Old text:

```
        if word in counts:
            counts[word] += 1
            why = report.get("why")
            if isinstance(why, str) and why:
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
```

New text:

```
        why = report.get("why")
        if isinstance(why, str) and why:
            by_reason.setdefault(word, {})[why] = by_reason.get(word, {}).get(why, 0) + 1
        if word in counts:
            counts[word] += 1
```

### `r706-c.C1_parts_note_never_said`

The recognition-in-parts note is never added

- File: `src/cratekit/intake/cli.py`
- Source: `r706-c.json`, row `C1_parts_note_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`
  - `tests/intake/test_workers.py::test_identify_only_says_the_same_parts_note`

Old text:

```
    if result.parts <= 1:
        return ()
    still = (
```

New text:

```
    if result.parts >= 1:
        return ()
    still = (
```

### `r706-c.C3_summary_ignores_the_payload`

The resume summary reports one part rather than reading the frozen count

- File: `src/cratekit/intake/cli.py`
- Source: `r706-c.json`, row `C3_summary_ignores_the_payload`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_longer_than_one_run_is_queued_as_one_job_with_the_parts_said`

Old text:

```
        "parts": int(payload.get(PARTS) or 1),
```

New text:

```
        "parts": 1,
```

### `r925.S2_out_ignored`

intake set ignores --out and always writes under download staging

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S2_out_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_writes_its_tracklist_where_out_says`

Old text:

```
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
```

New text:

```
        out = _tracklist_dir(cfg, None, local if local is not None else source.strip())
```

### `r925.S4_write_failure_refuses`

A tracklist that cannot be written raises out of intake set after the job is queued

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S4_write_failure_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`

Old text:

```
    try:
        path = _write_tracklist(out, held, result)
    except OSError as exc:
        failed = _tracklist_path(out, held, result)
```

New text:

```
    try:
        path = _write_tracklist(out, held, result)
    except ValueError as exc:
        failed = _tracklist_path(out, held, result)
```

### `r925.S5_unwritten_note_names_no_job_show`

The unwritten note no longer names the verb that lists the tracks

- File: `src/cratekit/intake/cli.py`
- Source: `r925.json`, row `S5_unwritten_note_names_no_job_show`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_whose_tracklist_cannot_be_written_is_queued_and_says_where_to_read_it`

Old text:

```
f"{exc.strerror or exc}); the job is queued, and its tracks are listed "
                f"by: crate job show {job_id}"
```

New text:

```
f"{exc.strerror or exc}); the job is queued"
```

### `u120.L1_date_frozen_when_none`

list_favorites: a heart with no date is frozen with no key, as an older build did

- File: `src/cratekit/intake/cli.py`
- Source: `u120.json`, row `L1_date_frozen_when_none`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`

Old text:

```
        if key in frozen and HEARTED not in frozen[key]:
            frozen[key][HEARTED] = hearted_on(row)
```

New text:

```
        if key in frozen and HEARTED not in frozen[key] and hearted_on(row):
            frozen[key][HEARTED] = hearted_on(row)
```

### `u120.L2_date_added_ignored`

hearted_on: the older client's date_added is not read

- File: `src/cratekit/intake/cli.py`
- Source: `u120.json`, row `L2_date_added_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_hearts_job_freezes_when_each_heart_was_made_and_a_playlist_job_does_not`

Old text:

```
    for name in ("user_date_added", "date_added"):
```

New text:

```
    for name in ("user_date_added",):
```

### `u57-recognition-and-items.C3_missing_ref_not_refused`

A provider row without an identifier is queued rather than refused by position

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C3_missing_ref_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_heart_without_an_identifier_is_refused_by_position`
  - `tests/intake/test_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
        if row.origin != match.TEXT and not row.ref
```

New text:

```
        if False
```

### `u57-recognition-and-items.C6_unanswered_zero_reads_as_zero`

A set where chunks got no answer and the rest named nothing is reported as nothing identified

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C6_unanswered_zero_reads_as_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_set_where_chunks_got_no_answer_and_the_rest_named_nothing_is_a_failure_not_a_zero`

Old text:

```
    if not result.unreached:
        return ()
    if not result.rows:
        raise refuse(
```

New text:

```
    if not result.unreached or not result.rows:
        return ()
    if False:
        raise refuse(
```

### `u57-recognition-and-items.C7_foreign_job_driven`

A job of another verb is driven under this verb's envelope

- File: `src/cratekit/intake/cli.py`
- Source: `u57-recognition-and-items.json`, row `C7_foreign_job_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_job_of_another_verb_is_refused_rather_than_driven_under_this_envelope`

Old text:

```
    if job.handler_key not in INTAKE_KEYS:
```

New text:

```
    if False:
```

### `u70.E1_missing_id_refused`

Existing: a provider row with no id is not refused by position, so a heart without one is queued under a blank key

- File: `src/cratekit/intake/cli.py`
- Source: `u70.json`, row `E1_missing_id_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_workers.py::test_a_heart_without_an_identifier_is_refused_by_position`
  - `tests/intake/test_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
        if row.origin != match.TEXT and not row.ref
```

New text:

```
        if row.origin != match.TEXT and False
```

### `u134-a.A10_shared_playlist`

Let two jobs share one playlist unless three do

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A10_shared_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_one_playlist_two_jobs_answer_to_is_neither_jobs`

Old text:

```
counts[one.playlist_id] > 1
```

New text:

```
counts[one.playlist_id] > 2
```

### `u134-a.A11_pass_unknown`

Drop the refusal of a pass with no account playlist job

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A11_pass_unknown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pass_with_no_account_playlist_job_is_refused_naming_the_pass`

Old text:

```
    if not named:
        raise _pass_unknown(cfg, pass_name)

```

New text:

```
(empty)
```

### `u134-a.A1_outside_inbox`

Drop the refusal of a recorded mirror that is live outside INBOX

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A1_outside_inbox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_moved_outside_inbox_is_refused_by_name_before_any_report_is_read`

Old text:

```
        if str(mirror.ID) not in under:
```

New text:

```
        if False:
```

### `u134-a.A2_mirror_is_first`

Take the newest recorded entry of the pass as the mirror instead of the oldest

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A2_mirror_is_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`

Old text:

```
        mirror = _live_playlist(db, recorded[0])
```

New text:

```
        mirror = _live_playlist(db, recorded[-1])
```

### `u134-a.A3_gone_listed`

Fall through to the name match when the recorded mirror is gone

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A3_gone_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`

Old text:

```
    if recorded:
        mirror = _live_playlist(db, recorded[0])
```

New text:

```
    if recorded and _live_playlist(db, recorded[0]) is not None:
        mirror = _live_playlist(db, recorded[0])
```

### `u134-a.A4_others_excluded`

Let the name match take a playlist a record gives another pass

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A4_others_excluded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_not_asked_of_a_playlist_a_record_gives_another_pass`

Old text:

```
            if key not in others
```

New text:

```
            if True
```

### `u134-a.A5_unreadable`

Trust a name match while a session record could not be read

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A5_unreadable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_the_name_is_not_trusted_while_a_session_record_cannot_be_read`

Old text:

```
        if unreadable:
```

New text:

```
        if False:
```

### `u134-a.A6_pre_u128_exact_name`

Match a pre U128 entry by pass alone, so the Name 2 twin counts

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A6_pre_u128_exact_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`

Old text:

```
    return entry.account == account if entry.account else entry.name == name
```

New text:

```
    return entry.account == account if entry.account else True
```

### `u134-a.A7_pass_matched`

Drop the pass comparison, so another pass's record names the mirror

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A7_pass_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_pre_u128_record_is_matched_by_the_accounts_exact_name_so_the_twin_is_left`

Old text:

```
    if entry.pass_name != pass_name:
        return False

```

New text:

```
(empty)
```

### `u134-a.A8_only_what_it_lacks`

Plan every distinct member as an add whatever the playlist holds

- File: `src/cratekit/intake/refill.py`
- Source: `u134-a.json`, row `A8_only_what_it_lacks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_playlist_changed_after_the_approval_is_refused_and_nothing_is_written`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`

Old text:

```
if one not in present)
```

New text:

```
if True)
```

### `u134-b.B1c_composite_short_write`

What B1 holds: the write adds all but the first planned membership

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B1c_composite_short_write`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`

Old text:

```
                    rb_writer.add_memberships(db, playlist, target.adds)
```

New text:

```
                    rb_writer.add_memberships(db, playlist, target.adds[1:])
```

### `u134-b.B2c_composite_reversed_write`

What B2 holds: the write adds the planned memberships in reverse

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B2c_composite_reversed_write`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 8 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`
  - `tests/test_inbox_refill.py::test_a_playlist_no_record_names_is_found_by_the_accounts_name_under_inbox`
  - `tests/test_inbox_refill.py::test_a_playlist_that_holds_some_gets_only_what_it_lacks`
  - `tests/test_inbox_refill.py::test_a_same_pass_twin_recorded_since_u128_is_not_taken_for_the_mirror`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`
  - `tests/test_inbox_refill.py::test_a_track_the_library_lost_is_named_and_left`
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`

Old text:

```
                    rb_writer.add_memberships(db, playlist, target.adds)
```

New text:

```
                    rb_writer.add_memberships(db, playlist, target.adds[::-1])
```

### `u134-b.B4_record_on_success`

Drop the success path's record of the commit

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B4_record_on_success`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_three_owned_and_two_new_refill_an_empty_playlist_as_five_in_account_order`

Old text:

```
        _record_refill_commit(record, plan, added, cfg)
        convergence.record_fingerprint(cfg, db)
```

New text:

```
        convergence.record_fingerprint(cfg, db)
```

### `u134-b.B7_again_action`

Show a repeated track's second row as held, not again

- File: `src/cratekit/intake/refill.py`
- Source: `u134-b.json`, row `B7_again_action`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_track_the_account_lists_twice_is_one_membership_and_counted_once`

Old text:

```
            if one.content_id in seen:
```

New text:

```
            if False:
```

### `u175.F1_bridge_name_unasked`

refill.locate: ask only the account's bare name again, so a dated playlist an intake file recorded by name alone is called unfound

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F1_bridge_name_unasked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_dated_playlist_an_intake_file_recorded_by_name_alone_is_found_by_that_name`

Old text:

```
        asked = {name, recorded_name} - {"", native.ANALYZE}
```

New text:

```
        asked = {name} - {"", native.ANALYZE}
```

### `u175.F2_bridge_names_any_account`

refill.bridge_names: take an intake file's entry of any account, so another account playlist's dated name is asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F2_bridge_names_any_account`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
                and str(entry.get(ingest.INBOX_ACCOUNT_KEY) or "") == account
```

New text:

```
                and True
```

### `u175.F4_bridge_names_any_state`

refill.bridge_names: read an intake record that no longer stands, so an abandoned landing's name is asked

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F4_bridge_names_any_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW or record.state not in _STANDING:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if (
```

New text:

```
        if record.workflow != ingest.INTAKE_WORKFLOW:
            continue
        for entry in record.detail.get(ingest.INBOX_PLAYLISTS_KEY) or ():
            if (
```

### `u175.F5_bridge_names_by_id_order`

refill.bridge_names: order the records by identifier alone, so a later landing whose identifier sorts first is asked as the first

- File: `src/cratekit/intake/refill.py`
- Source: `u175.json`, row `F5_bridge_names_by_id_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_bridge_names_reads_only_this_accounts_entries_of_this_pass_with_no_id`

Old text:

```
    names: list[str] = []
    for record in sorted(records, key=lambda one: (one.started, one.session_id)):
```

New text:

```
    names: list[str] = []
    for record in sorted(records, key=lambda one: one.session_id):
```

### `u134-b.B5_no_writes_no_op`

Apply a plan that adds nothing instead of ending no_op

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B5_no_writes_no_op`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_a_recorded_playlist_that_is_gone_is_listed_and_no_name_is_guessed`
  - `tests/test_inbox_refill.py::test_a_second_run_plans_nothing_and_ends_no_op`
  - `tests/test_inbox_refill.py::test_two_playlists_of_the_accounts_name_under_inbox_are_neither_filled`

Old text:

```
    if not plan.writes:
```

New text:

```
    if False:
```

### `u134-b.B6_ack_before_gate`

Drop the backup acknowledgment read before the plan and the gate

- File: `src/cratekit/intake/refill_cli.py`
- Source: `u134-b.json`, row `B6_ack_before_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_refill.py`
- Collected: 22 against a baseline of 22
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_refill.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
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

### `r239-b.S10_adopt_apply_key_off`

adopt apply's write open passes unlock=False

- File: `src/cratekit/adopt/apply_cli.py`
- Source: `r239-b.json`, row `S10_adopt_apply_key_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_rb_writer_db.py`, `tests/test_routing_workers.py`, `tests/test_adopt_collection.py`, `tests/test_deletion.py`, `tests/test_metadata_cli.py`, `tests/test_naming_apply_cli.py`, `tests/test_adopt_apply_cli.py`
- Collected: 733 against a baseline of 733
- Kills: 1 (killed)
- Killed:
  - `tests/test_rb_writer_db.py::test_no_caller_in_src_answers_the_key_question_for_itself`

Old text:

```
        require_closed=True,
        cfg=cfg,
    )

```

New text:

```
        require_closed=True,
        unlock=False,
        cfg=cfg,
    )

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

### `u178.S1_summary_counts_labels`

_summary: never count a file per label, so label_genres stays empty

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S1_summary_counts_labels`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
            if wrote == tag_engine.LABEL_GENRE:
```

New text:

```
            if False:
```

### `u178.S2_unknown_label_refused`

_label_payload: a --label nobody registered queues the sweep with no label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S2_unknown_label_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_nobody_registered_is_refused_and_nothing_is_queued`

Old text:

```
        if entry is None:
            raise refuse(
                "label-unknown",
```

New text:

```
        if entry is None and False:
            raise refuse(
                "label-unknown",
```

### `u178.S3_unreadable_registry_refuses_label`

_label_payload: an unreadable registry warns rather than refusing a sweep given --label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S3_unreadable_registry_refuses_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_unreadable_registry_warns_and_refuses_only_a_sweep_that_named_a_label`

Old text:

```
    except CratekitError as exc:
        if label is not None:
            raise

```

New text:

```
    except CratekitError as exc:

```

### `u178.S4_genres_frozen`

_label_payload: freeze no genres, so a registered label genre never reaches the worker

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S4_genres_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 13 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
    if genres:
        frozen["label_genres"] = genres
```

New text:

```
    if False:
        frozen["label_genres"] = genres
```

### `u178.S5_worker_takes_label`

handle: hand the engine no --label, so a folder of untagged files is searched

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S5_worker_takes_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_files_whose_own_tag_outranked_the_label_are_counted_and_named`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`

Old text:

```
        label=str(payload.get("label") or "") or None,
```

New text:

```
        label=None,
```

### `u178.S6_outranked_needs_label`

_label_warnings: warn about outranked tags on a sweep given no --label

- File: `src/cratekit/tagging/cli.py`
- Source: `u178.json`, row `S6_outranked_needs_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_tag_that_could_never_name_a_label_is_searched_and_never_fails`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_tag_naming_no_genre_says_nothing_on_a_sweep_given_no_label`

Old text:

```
    if payload.get("label") and outranked:
```

New text:

```
    if outranked:
```

### `u178-e9.E9_label_tag_reset`

tag_one: keep the file's tag in label_tag on a file the label answered for

- File: `src/cratekit/tagging/tag.py`
- Source: `u178-e9.json`, row `E9_label_tag_reset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_its_own_label_answered_for_is_never_named_as_outranked`

Old text:

```
        label_tag = ""
        _written(
```

New text:

```
        _written(
```

### `u178.E2_no_search_with_picture`

tag_one: drop the early return for a labelled file with a picture, so the catalogues are searched

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E2_no_search_with_picture`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 11 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_folder_of_mixed_labels_tags_each_by_its_own`
  - `tests/test_label_genre.py::test_a_label_tag_reaches_its_genre_with_no_label_named`
  - `tests/test_label_genre.py::test_a_name_that_is_another_labels_identifier_is_the_label_named_so`
  - `tests/test_label_genre.py::test_a_puls_batch_is_tagged_by_the_label_and_the_report_counts_it_apart`
  - `tests/test_label_genre.py::test_a_puls_file_with_no_genre_gets_its_labels_genre_with_no_searcher_called`
  - `tests/test_label_genre.py::test_a_sweep_queued_before_the_identifier_was_frozen_still_tags_by_its_labels_name`
  - `tests/test_label_genre.py::test_a_tag_carrying_a_labels_name_from_before_its_rename_still_reaches_it`
  - `tests/test_label_genre.py::test_a_tag_naming_a_label_whose_name_is_another_labels_identifier_takes_its_genre`
  - `tests/test_label_genre.py::test_the_genres_are_frozen_when_the_sweep_is_queued`
  - `tests/test_label_genre.py::test_the_label_carrying_the_genre_still_gives_it_under_the_shared_name`
  - `tests/test_label_genre.py::test_the_verbs_label_names_the_label_of_a_file_with_no_tag_and_the_tag_wins`

Old text:

```
        if settled is not None:
            return TagResult(path=path, **labelled, **repaired, **settled)

```

New text:

```
(empty)
```

### `u178.E3_art_refusal_tolerated`

tag_one: a refusal on a labelled file's art search fails the item

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E3_art_refusal_tolerated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_refusal_on_the_art_search_does_not_fail_a_puls_file`

Old text:

```
        if needs_genre:
            raise
```

New text:

```
        if not existing:
            raise
```

### `u178.E4_isrc_withheld`

tag_one: offer the general catalogue the ISRC of a labelled file searched for art

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E4_isrc_withheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_an_art_search_for_a_labelled_file_never_offers_the_general_catalogue_its_isrc`

Old text:

```
        wanted = needs_genre and not hit.genre
```

New text:

```
        wanted = not existing and not hit.genre
```

### `u178.E6_label_write_checked`

tag_one: the label genre write's False is ignored, so a locked file is reported tagged

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E6_label_write_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_its_labels_genre_fails_and_is_never_counted_tagged`

Old text:

```
        _written(path, by_label.genre, f"its label {by_label.label}")
```

New text:

```
        tags.write_genre(path, by_label.genre)
```

### `u178.E7_catalogue_write_checked`

tag_one: the catalogue genre write's False is ignored, as on main

- File: `src/cratekit/tagging/tag.py`
- Source: `u178.json`, row `E7_catalogue_write_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_file_that_will_not_take_a_catalogues_genre_fails_too`

Old text:

```
        written = _written(path, hit.genre, hit.source or "a catalogue")
```

New text:

```
        tags.write_genre(path, hit.genre)
        written = hit.genre
```

### `u174.M10_dedupe`

plan_pass: keep a playlist named twice twice in the narrowing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M10_dedupe`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
    named = tuple(dict.fromkeys(str(one) for one in playlists_named))
```

New text:

```
    named = tuple(str(one) for one in playlists_named)
```

### `u174.M11_stranger_before_no_jobs`

plan_pass: refuse a stranger only after the no jobs return, so a file of no pass given --playlist asks a gate

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M11_stranger_before_no_jobs`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    _refuse_strangers(named, found, name)
    if not found:
```

New text:

```
    if found:
        _refuse_strangers(named, found, name)
    if not found:
```

### `u174.M1_stranger_refusal`

plan_pass: drop the refusal of a named playlist that is not the pass's, so it plans nothing and says nothing

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M1_stranger_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
    strangers = [identity for identity in named if identity not in held]
    if strangers:
```

New text:

```
    strangers = [identity for identity in named if identity not in held]
    if False:
```

### `u174.M2_narrowing`

plan_pass: drop the narrowing of the decided playlists, so --playlist plans the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M2_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_already_marked_is_a_skip_and_not_a_refusal`
  - `tests/test_sync_mark.py::test_a_native_pass_takes_playlist_as_the_file_does`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_the_library_is_walked_only_for_the_named_playlist`

Old text:

```
        decided = [entry for entry in decided if entry.identity in named]
```

New text:

```
        decided = list(decided)
```

### `u174.M3_unfinished_refusal`

plan_pass: drop the refusal of a named playlist the pass did not complete, so it is shown as a skip

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M3_unfinished_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if unfinished:
```

New text:

```
    unfinished = [entry for entry in decided if entry.reason in UNFINISHED]
    if False:
```

### `u174.M4_unfinished_rows_outstanding`

UNFINISHED: leave out rows-outstanding, so a playlist with a missing track is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M4_unfinished_rows_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE})
```

### `u174.M5_unfinished_job`

UNFINISHED: leave out job-unfinished, so a playlist whose job failed is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M5_unfinished_job`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_job_failed_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

### `u174.M6_unfinished_reports`

UNFINISHED: leave out reports-unreadable, so a playlist whose reports cannot be read is a skip when named

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M6_unfinished_reports`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_whose_reports_cannot_be_read_is_refused_by_name`

Old text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, REPORTS_UNREADABLE, ROWS_OUTSTANDING})
```

New text:

```
UNFINISHED = frozenset({JOB_UNFINISHED, ROWS_OUTSTANDING})
```

### `u174.M7_digest_names_the_narrowing`

_payload: leave the narrowing out of the digest, so an answer to one playlist's screen carries out the whole pass

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M7_digest_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_repeated_takes_each_named_and_no_playlist_is_the_whole_pass`

Old text:

```
        identity["only"] = sorted(named)
```

New text:

```
        pass
```

### `u174.M8_screen_names_the_narrowing`

_shown: drop the gate screen's line naming the playlists the plan was narrowed to

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M8_screen_names_the_narrowing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`

Old text:

```
        shown[ONLY_SAID] = list(named)
```

New text:

```
        pass
```

### `u174.M9_verb_passes_the_flag`

sync_mark: hand plan_pass no playlists, so --playlist is parsed and ignored

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `M9_verb_passes_the_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_named_playlist_the_pass_did_not_complete_is_refused_by_name`
  - `tests/test_sync_mark.py::test_a_playlist_of_no_pass_of_this_name_is_refused_before_the_account_is_listed`
  - `tests/test_sync_mark.py::test_an_answer_to_the_narrowed_plan_does_not_carry_out_the_whole_pass`
  - `tests/test_sync_mark.py::test_playlist_narrows_the_plan_the_gate_and_the_renames_to_the_one_named`
  - `tests/test_sync_mark.py::test_playlist_on_a_file_of_no_pass_is_refused_and_asks_no_gate`

Old text:

```
        playlists_named=list(getattr(ctx.args, "playlist", None) or ()),
```

New text:

```
        playlists_named=(),
```

### `u174.P1_bridge_plans_no_native_pass`

native_passes: read native records on a tree on the bridge too, so every old record is planned as a refusal

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P1_bridge_plans_no_native_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_tree_on_the_bridge_plans_no_native_record`

Old text:

```
    if not medium.native:
        return ()
    return native.landed_passes(cfg)
```

New text:

```
    return native.landed_passes(cfg)
```

### `u174.P2_unreachable_is_refused`

native_passes: read an unreachable root as no pass, so organize asks over a clean plan

- File: `src/cratekit/sync/mark_cli.py`
- Source: `u174.json`, row `P2_unreachable_is_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`, `tests/test_crate_sync_skill.py`
- Collected: 191 against a baseline of 191
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_root_is_a_refused_step_and_never_no_pass`

Old text:

```
    if medium.declared is None:
        raise _blocked(
```

New text:

```
    if medium.declared is None:
        return ()
        raise _blocked(
```

### `r1091.K10_available_dropped`

_row: keep every track as playable, so a track the provider will not play is asked for from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K10_available_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_a_track_the_provider_will_not_play_out_of_the_year`

Old text:

```
        "available": getattr(track, "available", True) is not False,
```

New text:

```
        "available": True,
```

### `r1091.K11_year_dropped`

keep: store no year, so a release the provider dates is planned under its listed year from a kept read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K11_year_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_kept_read_keeps_the_year_the_provider_stated_over_the_listed_one`

Old text:

```
                year=stated,
```

New text:

```
                year=None,
```

### `r1091.K12_periodic_write_off`

_hold: never write mid run, so a killed build keeps nothing it read

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K12_periodic_write_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_reads_are_written_every_flush_and_not_only_at_the_end`

Old text:

```
        if self._since >= FLUSH_EVERY:
```

New text:

```
        if False:
```

### `r1091.K13_write_error_raised`

flush: let a write the filesystem refuses raise, the round 1 blocking finding

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K13_write_error_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_file_where_the_labels_directory_belongs_still_shows_the_plan`
  - `tests/test_label_playlists_kept.py::test_a_periodic_write_that_fails_does_not_stop_the_read`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_written_still_shows_the_plan_and_says_so`
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`
  - `tests/test_label_playlists_kept.py::test_an_abort_after_a_failed_write_still_warns_the_reads_were_not_kept`

Old text:

```
        except OSError as exc:
            self.unkept = f"{type(exc).__name__}: {exc}"
            return
```

New text:

```
        except OSError as exc:
            raise
```

### `r1091.K14_unkept_never_cleared`

flush: leave the failure said after a later write succeeds

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K14_unkept_never_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_write_that_succeeds_after_one_failed_clears_what_was_said`

Old text:

```
        self._unwritten = 0
        self.unkept = ""
```

New text:

```
        self._unwritten = 0
```

### `r1091.K15_reuse_uncounted`

fresh: count no reuse, so the screen says every read was made by this run

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K15_reuse_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_build_parked_part_way_resumes_and_reads_only_what_it_had_not`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_a_resumed_run_that_cannot_write_says_both_the_reuse_and_the_loss`

Old text:

```
        self.reused += 1
```

New text:

```
        self.reused += 0
```

### `r1091.K1_age_never_expires`

_is_fresh: drop the upper bound, so a read is kept for ever and a changed release is planned from old tracks

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K1_age_never_expires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`
  - `tests/test_label_playlists_kept.py::test_a_read_older_than_the_age_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age
```

### `r1091.K2_future_is_fresh`

_is_fresh: drop the lower bound, so a read dated in the future is kept for as long as the clock is wrong

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K2_future_is_fresh`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_dated_in_the_future_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return age < KEPT_FOR
```

### `r1091.K3_age_boundary`

_is_fresh: a read exactly the age old is still fresh

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K3_age_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_read_exactly_the_age_old_is_read_again`

Old text:

```
        return timedelta(0) <= age < KEPT_FOR
```

New text:

```
        return timedelta(0) <= age <= KEPT_FOR
```

### `r1091.K4_age_coefficient`

KEPT_FOR: eight days instead of seven, a realistic nearby value

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K4_age_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_first_build_says_its_reads_are_kept_for_the_apply_run`
  - `tests/test_label_playlists_kept.py::test_a_read_just_inside_the_age_is_reused_and_named_as_old`
  - `tests/test_label_playlists_kept.py::test_the_age_is_seven_days`
  - `tests/test_label_playlists_kept.py::test_the_crawl_gate_counts_the_kept_reads_and_estimates_only_the_rest`

Old text:

```
KEPT_FOR = timedelta(days=7)
```

New text:

```
KEPT_FOR = timedelta(days=8)
```

### `r1091.K5_version_unchecked`

load: read a document of another version as if it were this one

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K5_version_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 99, "label_id": "kompakt", "reads": {}}-it says version 99]`

Old text:

```
        if version != VERSION:
```

New text:

```
        if False:
```

### `r1091.K6_label_unchecked`

load: read another label's document as this label's reads

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K6_label_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[{"version": 1, "label_id": "another", "reads": {}}-it names the label]`

Old text:

```
        if raw.get("label_id") != label_id:
```

New text:

```
        if False:
```

### `r1091.K7_gone_shape_unchecked`

_entry: accept a gone flag that is not a bool, so a string reads as gone

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K7_gone_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written8-says gone]`

Old text:

```
    if not isinstance(gone, bool):
```

New text:

```
    if False:
```

### `r1091.K8_year_shape_unchecked`

_entry: accept a year of any type, so a string or bool year reaches the plan

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K8_year_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written7-carries the year]`
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written9-carries the year]`

Old text:

```
    if year is not None and (isinstance(year, bool) or not isinstance(year, int)):
```

New text:

```
    if False:
```

### `r1091.K9_track_shape_unchecked`

_entry: accept a malformed track entry

- File: `src/cratekit/label/kept_reads.py`
- Source: `r1091.json`, row `K9_track_shape_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists_kept.py`, `tests/test_label_playlists.py`, `tests/test_label_playlists_releases.py`
- Collected: 124 against a baseline of 124
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists_kept.py::test_a_store_that_cannot_be_read_refuses_before_any_release_is_read[written6-is malformed]`

Old text:

```
            not isinstance(track, Mapping)
            or not isinstance(track.get("id"), str)
            or not isinstance(track.get("available"), bool)
```

New text:

```
            not isinstance(track, Mapping)
```

### `u54-acquisition-worker.G10_absent_result`

Drop the refusal for a run that reported OK with no result for this key

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G10_absent_result`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_run_reporting_nothing_for_the_key_is_refused_rather_than_read_as_success`

Old text:

```
    if result is None:
        raise refuse(
            "unavailable-transient",
            f"{invocation.adapter} finished without reporting on {request.key}, "
            f"so nothing is known about it and it stays queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=("acquire.cli",),
            detail={"adapter": invocation.adapter, "key": request.key},
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G11_not_acquired`

Commit a per-track result that is not an acquisition

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G11_not_acquired`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 8 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_offer_under_strict_policy_is_refused_before_anything_is_fetched`
  - `tests/test_acquire_workers.py::test_a_refusal_beside_a_network_failure_fails_and_keeps_the_refusal_skipped`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`
  - `tests/test_acquire_workers.py::test_a_track_the_provider_no_longer_has_is_declined_as_well`
  - `tests/test_acquire_workers.py::test_the_declined_warnings_name_skipped_tracks_and_never_a_failed_one`
  - `tests/test_acquire_workers.py::test_the_human_output_says_ok_and_names_the_refused_track`
  - `tests/test_acquire_workers.py::test_the_warning_is_the_same_when_the_finished_job_is_asked_about_again`
  - `tests/test_acquire_workers.py::test_three_landed_and_one_refused_by_policy_ends_ok_with_a_warning_naming_it`

Old text:

```
    if result.outcome is not TrackOutcome.ACQUIRED:
        raise _refused_track(result, invocation.adapter)

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G12_landing_check`

Take the adapter's word for the landed file, skipping the policy check at the file

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G12_landing_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_strict_policy_is_refused_at_the_item_with_the_codec_named`
  - `tests/test_acquire_workers.py::test_an_unreadable_landing_is_transient_and_not_a_policy_refusal`
  - `tests/test_acquire_workers.py::test_the_frozen_policy_reaches_the_worker_not_the_live_one`
  - `tests/test_acquire_workers.py::test_the_refused_landing_left_as_evidence_survives_the_sweep`
  - `tests/test_acquire_workers.py::test_the_sweep_does_not_report_a_directory_it_could_not_remove`

Old text:

```
    landed = checked_landing(Path(str(result.path)), request.key, policy=per_item.lossless_policy)
```

New text:

```
    landed = Path(str(result.path))
```

### `u54-acquisition-worker.G14_marker_applied`

Commit a lossy landing under its unmarked name whatever the policy required

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G14_marker_applied`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_under_the_permissive_policy_is_committed_marked`
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    if not required:
        return landed.name

```

New text:

```
    return landed.name

```

### `u54-acquisition-worker.G15_no_marker_text`

Commit a lossy landing unmarked when the configuration names no marker text

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G15_no_marker_text`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lossy_landing_with_no_marker_text_is_refused_rather_than_committed_unmarked`

Old text:

```
    if not text:
        raise refuse(
            "lossy-refused",
            f"{landed.name} landed lossy under a policy that permits lossy only "
            f"when marked, and the configuration names no marker text, so it "
            f"cannot be marked and is not kept",
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=("acquire.cli",),
            detail={"path": str(landed)},
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G17_paced_sleep_bound`

Let the pool bind its own definition time sleep instead of the one the frozen configuration paces

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G17_paced_sleep_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 2 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_rate_limit_that_never_clears_fails_the_item_as_transient`
  - `tests/test_acquire_workers.py::test_the_pacing_delay_comes_from_the_frozen_configuration_not_a_fresh_load`

Old text:

```
    run = download.acquire_paced(adapter, (request,), sleep=_SLEEP)
```

New text:

```
    run = download.acquire_paced(adapter, (request,))
```

### `u54-acquisition-worker.G19_frozen_config`

Build the adapter settings from a fresh load rather than the configuration the job was frozen against

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G19_frozen_config`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 40 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_configuration_naming_an_unknown_adapter_fails_the_item_by_name`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
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
  - ... and 25 more, see the JSON sidecar

Old text:

```
    settings = AdapterSettings.from_config(cfg)
```

New text:

```
    settings = AdapterSettings.from_config(_load())
```

### `u54-acquisition-worker.G1_origin_refusal`

Queue a list from any provider, dropping the refusal that only the provider's own list carries acquirable identifiers

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G1_origin_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_pasted_tracklist_is_refused_at_the_queue_rather_than_queued_unacquirable`

Old text:

```
    if origin != match.TIDAL:
        raise _unusable(
            f"this is a {origin} list, and acquiring needs the provider's own track "
            f"identifiers, which only a list fetched from the provider carries",
            "fetch the playlist from the provider into a list document first, "
            "then acquire that",
            "a pasted tracklist is matched against the library with match.run; "
            "its missing rows carry acquisition options, not identifiers",
            origin=origin,
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G20_output_exists`

Replace a file already at the destination instead of refusing

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G20_output_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_an_existing_file_at_the_destination_refuses_rather_than_replacing_it`

Old text:

```
    if final.exists():
```

New text:

```
    if False:
```

### `u54-acquisition-worker.G27_remedy_absent_stays_absent`

Restore the non-transient remedy fallback, so a delisted track is told to relax the lossless policy

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G27_remedy_absent_stays_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_track_the_provider_does_not_have_is_permanent_and_carries_no_remedy`

Old text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else None),
```

New text:

```
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else Remedy.RELAX_LOSSLESS_POLICY),
```

### `u54-acquisition-worker.G28_marker_decided_by_the_file`

Take the marker requirement from the offer's claim alone, so a lying offer commits an unmarked lossy file

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G28_marker_decided_by_the_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_lying_offer_under_the_permissive_policy_is_still_committed_marked`

Old text:

```
    required = result.requires_lossy_marker or lossy_landing(
        landed, policy=per_item.lossless_policy
    )
```

New text:

```
    required = result.requires_lossy_marker
```

### `u54-acquisition-worker.G29_auth_failure_parks`

Fail the item on a dead credential instead of parking, so the driver re-authenticates once per remaining track

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G29_auth_failure_parks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 3 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
        if invocation.outcome is InvocationOutcome.AUTH_FAILED:
```

New text:

```
        if False:
```

### `u54-acquisition-worker.G2_missing_identifier`

Queue a provider list whose rows carry no identifier, dropping the by-position refusal

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G2_missing_identifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_row_without_an_identifier_is_refused_by_position`

Old text:

```
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this list carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing can ask the "
            f"provider for them",
            "fetch the list from the provider again so every row carries its id",
            positions=missing,
        )

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G8_park_on_block`

Read a parked run as an ordinary result, so the driver claims the next item into a provider block

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G8_park_on_block`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_provider_block_parks_the_job_and_makes_no_further_request`

Old text:

```
    if run.parked is not None:
        raise jobs.Parked(run.parked)

```

New text:

```
(empty)
```

### `u54-acquisition-worker.G9_failed_invocation`

Ignore an invocation the adapter could not run at all

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-acquisition-worker.json`, row `G9_failed_invocation`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 5 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_broken_adapter_fails_the_item_and_does_not_park_the_run`
  - `tests/test_acquire_workers.py::test_a_dead_session_logs_in_once_and_not_once_per_track`
  - `tests/test_acquire_workers.py::test_a_mid_batch_defect_fails_that_item_and_the_resume_the_job_refuses_fetches_nothing`
  - `tests/test_acquire_workers.py::test_an_authentication_failure_parks_the_run_and_names_the_replacement_path`
  - `tests/test_acquire_workers.py::test_the_shipped_adapter_is_constructed_through_build_and_refuses_with_a_named_remedy`

Old text:

```
    if invocation.outcome in FAILED_INVOCATIONS:
```

New text:

```
    if False:
```

### `u54-zero-row-remeasured.G7_staging_cleared`

Keep whatever a killed attempt left in the item's staging directory, re-measured after the fake was taught to skip

- File: `src/cratekit/acquire/cli.py`
- Source: `u54-zero-row-remeasured.json`, row `G7_staging_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_acquire_cli.py`, `tests/test_acquire_workers.py`
- Collected: 93 against a baseline of 93
- Kills: 1 (killed)
- Killed:
  - `tests/test_acquire_workers.py::test_a_partial_file_left_in_staging_does_not_poison_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)

```

New text:

```
(empty)
```

### `r342.E1_cut_inclusive`

Existing guard sample: the with-vox cut becomes exclusive

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `E1_cut_inclusive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
if voxlevel is None or voxlevel < cut:
```

New text:

```
if voxlevel is None or voxlevel <= cut:
```

### `r342.V13_detail_key`

Rename the calibration detail key the refusal carries

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V13_detail_key`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 10 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
detail={"calibration": str(path), "kind": type(exc).__name__},
```

New text:

```
detail={"path": str(path), "kind": type(exc).__name__},
```

### `r342.V1_default_on_corrupt`

Restore the defect: an unreadable calibration returns the default cut instead of refusing

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V1_default_on_corrupt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 12 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_a_vocal_calibration_this_account_cannot_read_refuses`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        raise refuse(

```

New text:

```
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        return DEFAULT_VOCAL_THRESHOLD
        raise refuse(

```

### `r342.V2_no_finite_check`

Drop the finiteness check, so NaN and Infinity read as a cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V2_no_finite_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`

Old text:

```
        if not math.isfinite(threshold):
            raise ValueError(f"threshold {threshold} is not a finite number")

```

New text:

```
(empty)
```

### `r342.V3_isnan_for_isfinite`

Nearby value: check only for NaN, so Infinity reads as a cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V3_isnan_for_isfinite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`

Old text:

```
if not math.isfinite(threshold):
```

New text:

```
if math.isnan(threshold):
```

### `r342.V4_no_bool_check`

Drop the boolean check, so true reads as a cut of 1.0

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V4_no_bool_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`

Old text:

```
        if isinstance(raw, bool):
            raise TypeError(f"threshold {raw} is a boolean, not a number")

```

New text:

```
(empty)
```

### `r342.V5_tuple_drops_overflow`

Drop OverflowError from the except tuple, the review's finding

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V5_tuple_drops_overflow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[overflow]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, KeyError, TypeError) as exc:
```

### `r342.V6_tuple_drops_keyerror`

Drop KeyError from the except tuple, so a file with no threshold key crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V6_tuple_drops_keyerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[no-key]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, TypeError, OverflowError) as exc:
```

### `r342.V7_tuple_drops_typeerror`

Drop TypeError from the except tuple, so a list, null or boolean payload crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V7_tuple_drops_typeerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[boolean]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[list]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[null]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, ValueError, KeyError, OverflowError) as exc:
```

### `r342.V8_tuple_drops_valueerror`

Drop ValueError from the except tuple, so truncated JSON crashes

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V8_tuple_drops_valueerror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_corrupt_vocal_calibration_refuses_through_the_verb_and_writes_nothing`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[empty]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[infinity]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[nan]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[text]`
  - `tests/test_metadata_cli.py::test_an_unreadable_vocal_calibration_refuses_rather_than_defaulting[truncated]`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (OSError, KeyError, TypeError, OverflowError) as exc:
```

### `r342.V9_tuple_drops_oserror`

Drop OSError from the except tuple, so an unreadable file escapes unnamed

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r342.json`, row `V9_tuple_drops_oserror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_vocal_calibration_this_account_cannot_read_refuses`

Old text:

```
except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
```

New text:

```
except (ValueError, KeyError, TypeError, OverflowError) as exc:
```

### `r375-b.M2_a_noop_claims_a_commit`

_record_mytags_commit: record a commit for an apply that wrote nothing

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M2_a_noop_claims_a_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`

Old text:

```
    if written <= 0:
        return

```

New text:

```
(empty)
```

### `r375-b.M3_witnessed_commit_not_recorded`

mytags_vocals: ignore the witness, so a commit that landed and then raised closes as though nothing landed

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M3_witnessed_commit_not_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`

Old text:

```
                if witness.landed:
```

New text:

```
                if False:
```

### `r375-b.M4_summary_keyed_on_the_display_name`

_record_mytags_commit: key the change summary on the category's display name, which a person can rename (R19)

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M4_summary_keyed_on_the_display_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`

Old text:

```
session.TreeChange(tree=CHANGE_KEY, created=written)
```

New text:

```
session.TreeChange(tree=CATEGORY, created=written)
```

### `u25.G10_ignore_cut`

Every scored track is tagged, including those below the cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G10_ignore_cut`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
    if voxlevel is None or voxlevel < cut:
        return []

```

New text:

```
    if voxlevel is None:
        return []

```

### `u25.G11_gender_without_vox`

Gender tags are applied even when the track is below the cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G11_gender_without_vox`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 1 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_vocal_tag_values_are_empty_below_the_cut`

Old text:

```
    if voxlevel is None or voxlevel < cut:
        return []
    values = [VALUE_VOX]
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values

```

New text:

```
    values = []
    if voxlevel is not None and voxlevel >= cut:
        values.append(VALUE_VOX)
    if voxgender == "M":
        values.append(VALUE_MALE)
    elif voxgender == "F":
        values.append(VALUE_FEMALE)
    return values

```

### `u25.G12_apply_by_default`

The plan path writes, so a dry run mutates the database

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G12_apply_by_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 2 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_plan_only_run_leaves_no_record`
  - `tests/test_metadata_cli.py::test_the_plan_names_existing_rows_and_writes_nothing`

Old text:

```
        action="store_true",
        default=False,

```

New text:

```
        action="store_true",
        default=True,

```

### `u25.G13_skip_apply_gate`

Return the plan even when apply was requested, so nothing is written

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G13_skip_apply_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 8 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
        if not writing:
            return ctx.envelope(data=plan, outcome=Outcome.OK)

```

New text:

```
        if True:
            return ctx.envelope(data=plan, outcome=Outcome.OK)

```

### `u25.G24_content_column`

The My Tags apply also writes Rating, a content column

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u25.json`, row `G24_content_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 6 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1

```

New text:

```
            if rb_writer.add_my_tag(db, value_row, content_id):
                written += 1
            else:
                already += 1
            row = db.get_content(ID=content_id)
            if row is not None:
                row.Rating = 5

```

### `r592-a.A1_occupancy_guard_removed`

assert_recovery_target: find nothing occupied whatever the target holds, so a library whose database sits where this one lands is replaced unasked

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A1_occupancy_guard_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
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

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A2_database_dropped_from_fileset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
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

### `r592-a.A3_companions_dropped_from_fileset`

recovered_database_fileset: return the database only, so a lone write-ahead log the database half would clear is not an occupied target

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A3_companions_dropped_from_fileset`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
- Kills: 2 (killed)
- Killed:
  - `tests/test_restore.py::test_bare_metal_recovery_refuses_a_target_that_already_holds_a_library`
  - `tests/test_restore.py::test_the_occupancy_fileset_is_the_one_the_restore_plan_writes`

Old text:

```
    return (landing, *companions)
```

New text:

```
    return (landing,)
```

### `r592-a.A4_fileset_not_rebased`

recovered_database_fileset: land the database at its bare name at the top of the target for every layout, so the guard tests a path the transfer never writes

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A4_fileset_not_rebased`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
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

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A5_replacing_existing_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
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

- File: `src/cratekit/core/restore.py`
- Source: `r592-a.json`, row `A6_old_suffix_rule_restored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_restore.py`, `tests/test_restore_cli.py`
- Collected: 257 against a baseline of 257
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

