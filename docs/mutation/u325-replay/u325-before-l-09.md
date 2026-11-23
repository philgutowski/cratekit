# Mutation table: u325-before-l-09

Measured by `scripts/mutate.py` on 2026-11-23 00:21 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 146.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 9, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u71.A1_listing_dotfile` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A2_listing_suffix` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A3_listing_regular_file` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `u71.A4_digest_names_only` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A5_digest_no_mtime` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A6_stale_refusal` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 3 | killed |
| `u71.A7_stale_listing_only` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 2 | killed |
| `u71.A9_plan_empty` | `src/cratekit/intake/landing.py` | user | 1 file(s) | 44 | 1 | killed |
| `r375-a.S10_commit_not_persisted_at_once` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 1 | killed |
| `r375-a.S11_commit_replaces_the_summary` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 2 | killed |
| `r375-a.S1_keep_is_ignored` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 38 | killed |
| `r375-a.S2_record_inside_the_watch` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 3 | killed |
| `r375-a.S3_a_raise_is_not_abandoned` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 13 | killed |
| `r375-a.S4_abandon_failure_replaces_the_error` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 1 | killed |
| `r375-a.S5_clean_close_refusal_leaves_it_open` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 1 | killed |
| `r375-a.S6_close_ignores_the_intent` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 11 | killed |
| `r375-a.S7_close_drops_the_identity_seam` | `src/cratekit/core/session.py` | maintainer | 4 file(s) | 392 | 4 | killed |
| `r375-a.S8_record_names_no_actor` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 2 | killed |
| `r375-a.S9_record_names_no_acknowledgment` | `src/cratekit/core/session.py` | user | 4 file(s) | 392 | 2 | killed |
| `a32.A2_stale_deleted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.A3_stale_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.A5_policy_widened` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.D1_digest_drops_replaced` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 2 | killed |
| `a32.D2_digest_unordered` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.J1_wrong_unjudged` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.J2_planned_across_rows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.J4_moved_not_refused` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 2 | killed |
| `a32.P1_tombstone_plans` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.P2_unknown_row` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 4 | killed |
| `a32.P3_unheld_value` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 2 | killed |
| `a32.P4_count_tombstones` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 5 | killed |
| `a32.P6_writes_always` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 6 | killed |
| `a32.P7_minority_boundary` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.P8_null_fellows` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.V1_any_column` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 4 | killed |
| `a32.V2_link_not_converted` | `src/cratekit/write/row_link.py` | user | 1 file(s) | 59 | 4 | killed |
| `a32.C1_ack_after_gate` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.C2_abort_writes` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.C3_nothing_to_write_applies` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `a32.C4_read_back_unasserted` | `src/cratekit/write/row_link_cli.py` | user | 1 file(s) | 59 | 1 | killed |
| `u102-a.P1_root_boundary` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.P2_root_casefold` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.P3_root_filter` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-a.P4_unchanged` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.P5_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-a.P6_missing_says_what_exists` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U1_no_stored_path` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U2_bare_filename` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-a.U3_empty_name` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U4_same_suffix` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-a.U5_linked_file` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G1_plan_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G2_post_gate_referenced` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G4_plan_collisions` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G5_claim` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G6_abort` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G7_referenced_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.G8_collision_is_owed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.G9_post_gate_missing` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.R1_retryable_seed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `u102-b.R2_retryable_after_gate` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 1 | killed |
| `u102-b.S1_stub_removed` | `src/cratekit/intake/repair_cli.py` | user | 1 file(s) | 33 | 2 | killed |
| `r227.A1_floored_days` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 2 | killed |
| `r227.A2_never_stale` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 13 | killed |
| `r227.A3_future_clamped` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A4_no_tolerance` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A5_half_a_pair` | `src/cratekit/modules/outbound/source.py` | maintainer | 4 file(s) | 371 | 1 | killed |
| `r227.A6_conversion_unguarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A7_unreadable_reads_as_now` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 2 | killed |
| `r356-b.B1_naming_head_left_on_the_release_title` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 8 | killed |
| `r356-b.B2_template_declares_no_lossy_marker` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r356-b.B3_empty_marker_no_longer_guarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r356-b.B4_heart_candidate_carries_no_artist` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 4 | killed |
| `u121-b.S10r_folder_row_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-b.S14r_stale_digest` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-b.S15r_member_order` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-c.S2c_separator` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 2 | killed |
| `u121-d.D1_record_ignored` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D2_removed_namesake` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 2 | killed |
| `u121-d.D3_repeated_row_counted_twice` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D4_record_on_nothing` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D5_left_dropped_when_nothing_written` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121-d.D6_recorded_but_removed` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S11_landed_by_target` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 15 | killed |
| `u121.S17_unresolved_dropped` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 5 | killed |
| `u121.S1_uploader_prefix` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 2 | killed |
| `u121.S3_answer_not_read` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S4_page_beats_flag` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S5_missing_word` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 6 | killed |
| `u121.S7_job_handler` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S8_job_state` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u121.S9_two_folders` | `src/cratekit/intake/set_playlist.py` | user | 1 file(s) | 73 | 1 | killed |
| `u226.M10_settle_lag_known_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 5 | killed |
| `u226.M11_settle_kept_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 1 | killed |
| `u226.M13_removal_window_wrong` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 2 | killed |
| `u226.M15_wait_uncounted` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 2 | killed |
| `u226.M17_removal_positions_unsettled` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 3 | killed |
| `u226.M18_waited_unformatted` | `src/cratekit/modules/outbound/tidal_account.py` | maintainer | 9 file(s) | 22663 | 0 (promoted) | zero |
| `u226.M7_reading_takes_window` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 5 | killed |
| `u226.M8_unpaged_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 3 | killed |
| `u226.M9_positions_no_lag_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 5 | killed |
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
| `r375-b.M1_capture_never_attached` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 3 | killed |
| `r375-b.M2_a_noop_claims_a_commit` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M3_witnessed_commit_not_recorded` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `r375-b.M4_summary_keyed_on_the_display_name` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G10_ignore_cut` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G11_gender_without_vox` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 1 | killed |
| `u25.G12_apply_by_default` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 2 | killed |
| `u25.G13_skip_apply_gate` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 8 | killed |
| `u25.G24_content_column` | `src/cratekit/write/metadata_cli.py` | user | 1 file(s) | 26 | 6 | killed |
| `u154.G10_read_back_path_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G11_kept_columns_unchecked` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G14_reserved_folders_are_candidates` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G15_stored_target_under_mounted_path` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G17_refusal_before_rename_rewrapped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G1_policy_not_registered` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 11 | killed |
| `u154.G2_confinement_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G3_rename_back_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 2 | killed |
| `u154.G4_stale_target_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G5_unmatched_file_shelved_anyway` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G6_subfolder_check_dropped` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |
| `u154.G7_run_id_shape_unread` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 4 | killed |
| `u154.G8_free_target_no_suffix` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 3 | killed |
| `u154.R1_rows_under_target_not_consulted` | `src/cratekit/intake/shelve.py` | user | 1 file(s) | 43 | 1 | killed |

## Zero rows and what they owe

- `u226.M18_waited_unformatted` (maintainer facing): maintainer facing, composite not required

## Row definitions

### `u71.A1_listing_dotfile`

Drop the dotfile skip in the listing, so a hidden file is planned

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A1_listing_dotfile`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    if name.startswith(".") or name == ACQUIRE_STAGING_DIRNAME:
```

New text:

```
    if name == ACQUIRE_STAGING_DIRNAME:
```

### `u71.A2_listing_suffix`

Drop the audio suffix filter, so a text file is planned and moved

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A2_listing_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_an_empty_folder_is_refused_at_plan`
  - `tests/test_landing.py::test_the_listing_is_flat_audio_only_and_skips_dotfiles`

Old text:

```
    if entry.suffix.lower() not in AUDIO_EXTS:
```

New text:

```
    if False:
```

### `u71.A3_listing_regular_file`

Drop the regular file check, so a directory named like audio is planned

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A3_listing_regular_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_a_directory_named_like_audio_is_not_listed`

Old text:

```
    return entry.is_file() and not entry.is_symlink()
```

New text:

```
    return not entry.is_symlink()
```

### `u71.A4_digest_names_only`

Fingerprint names alone, so a file replaced under its name is not stale

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A4_digest_names_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`

Old text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
```

New text:

```
        hasher.update(f"{item.name}\n".encode())
```

### `u71.A5_digest_no_mtime`

Drop the modification time from the fingerprint, keeping name and size

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A5_digest_no_mtime`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`

Old text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
```

New text:

```
        hasher.update(f"{item.name}\0{stat.st_size}\n".encode())
```

### `u71.A6_stale_refusal`

Drop the stale plan refusal whole

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A6_stale_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 3 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`
  - `tests/test_landing.py::test_an_added_file_makes_the_plan_stale`

Old text:

```
    if items != plan.items or _digest(items) != plan.digest:
```

New text:

```
    if False:
```

### `u71.A7_stale_listing_only`

Compare the relisting by path only, dropping the digest half

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A7_stale_listing_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 2 (killed)
- Killed:
  - `tests/test_landing.py::test_a_file_replaced_under_the_same_name_makes_the_plan_stale`
  - `tests/test_landing.py::test_a_touched_file_of_the_same_size_makes_the_plan_stale`

Old text:

```
    if items != plan.items or _digest(items) != plan.digest:
```

New text:

```
    if items != plan.items:
```

### `u71.A9_plan_empty`

Drop the refusal of a folder with nothing to land

- File: `src/cratekit/intake/landing.py`
- Source: `u71.json`, row `A9_plan_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_landing.py`
- Collected: 44 against a baseline of 44
- Kills: 1 (killed)
- Killed:
  - `tests/test_landing.py::test_an_empty_folder_is_refused_at_plan`

Old text:

```
    if not items:
```

New text:

```
    if False:
```

### `r375-a.S10_commit_not_persisted_at_once`

record_commit: mark the source in memory and leave the write to the close, so a hard kill after the commit leaves a record that claims none

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S10_commit_not_persisted_at_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`

Old text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
    write_record(record, cfg)
```

New text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
```

### `r375-a.S11_commit_replaces_the_summary`

record_commit: replace the change summary instead of merging into it, so a second source erases the first one's counts

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S11_commit_replaces_the_summary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`
  - `tests/test_write_session.py::test_a_resume_skips_a_committed_source_and_finishes_the_rest`

Old text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = record.change.merged(change)
```

New text:

```
    record.sources[source] = str(SourceState.COMMITTED)
    record.change = change
```

### `r375-a.S1_keep_is_ignored`

assert_gates: keep a record for nobody, so Keep.RECORD yields Gates.record None

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S1_keep_is_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 38 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_a_library_with_no_tag_category_refuses_through_the_verb`
  - `tests/test_metadata_cli.py::test_a_second_apply_is_idempotent`
  - `tests/test_metadata_cli.py::test_a_second_apply_writes_nothing_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_metadata_cli.py::test_apply_writes_my_tags_and_does_not_write_a_content_column`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_capture_that_did_not_verify_is_recorded_before_the_refusal`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_failure_mid_loop_leaves_nothing_pending_on_the_handle`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            if keep is Keep.RECORD
            else nullcontext()
```

New text:

```
            if keep is Keep.NOTHING
            else nullcontext()
```

### `r375-a.S2_record_inside_the_watch`

assert_gates: open the record INSIDE the analysis watch, the ordering fault the review found, so it closes CLOSED before the watch judges

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S2_record_inside_the_watch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 3 (killed)
- Killed:
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_write_session.py::test_the_record_closes_after_the_analysis_watch_has_judged_the_session`

Old text:

```
        with keeping as record:
            with analysis_files_unmoved(watched) if watched else nullcontext():
                yield Gates(
```

New text:

```
        with analysis_files_unmoved(watched) if watched else nullcontext():
            with keeping as record:
                yield Gates(
```

### `r375-a.S3_a_raise_is_not_abandoned`

_recorded: drop the abandoning close, so a body that raised leaves its record OPEN

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S3_a_raise_is_not_abandoned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 13 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_an_apply_whose_commit_lands_and_then_raises_is_recorded_as_committed`
  - `tests/test_restore.py::test_a_restore_the_analysis_watch_refuses_is_not_on_record_as_finished`
  - `tests/test_restore.py::test_the_recovery_session_closes_its_own_record_on_both_paths`
  - `tests/test_tree_writer.py::test_a_capture_that_did_not_verify_is_recorded_before_the_refusal`
  - `tests/test_tree_writer.py::test_a_commit_that_lands_and_then_raises_is_still_recorded_as_committed`
  - `tests/test_tree_writer.py::test_a_failure_after_the_commit_still_reads_as_committed_work`
  - `tests/test_tree_writer.py::test_a_grid_rewritten_during_a_membership_write_refuses_the_session`
  - `tests/test_tree_writer.py::test_a_membership_write_that_fails_is_abandoned_and_claims_no_commit`
  - `tests/test_tree_writer.py::test_a_write_that_fails_after_counting_a_membership_still_claims_no_commit`
  - `tests/test_write_session.py::test_a_body_that_raises_closes_abandoned_and_its_own_error_surfaces`
  - `tests/test_write_session.py::test_a_clean_close_that_refuses_ends_abandoned_rather_than_open`
  - `tests/test_write_session.py::test_the_record_closes_after_the_analysis_watch_has_judged_the_session`

Old text:

```
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
```

New text:

```
            pass
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
```

### `r375-a.S4_abandon_failure_replaces_the_error`

_recorded: re-raise a failed abandonment instead of logging it, so it replaces the error that ended the session

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S4_abandon_failure_replaces_the_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_log_that_cannot_record_the_abandonment_does_not_replace_the_error`

Old text:

```
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise
```

New text:

```
            raise
        raise
```

### `r375-a.S5_clean_close_refusal_leaves_it_open`

_recorded: move the clean close out of the try, so a close that refuses leaves the record OPEN with no verb to abandon it

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S5_clean_close_refusal_leaves_it_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_clean_close_that_refuses_ends_abandoned_rather_than_open`

Old text:

```
    try:
        yield record
        close_session(
            record,
            cfg,
            state=SessionState.CLOSED,
            intent=intent,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
        try:
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise

```

New text:

```
    try:
        yield record
    except BaseException:
        try:
            close_session(record, cfg, state=SessionState.ABANDONED, now=now)
        except Exception:  # noqa: BLE001 - the session's own error is the one to surface
            logger.warning(
                "session %s could not be recorded as abandoned", record.session_id, exc_info=True
            )
        raise
    close_session(
        record,
        cfg,
        state=SessionState.CLOSED,
        intent=intent,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
        now=now,
    )

```

### `r375-a.S6_close_ignores_the_intent`

_recorded: close every record as an ordinary WRITE, so a recovery's close is gated by the latch it is the remedy for

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S6_close_ignores_the_intent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 11 (killed)
- Killed:
  - `tests/test_restore.py::test_a_coupled_file_the_capture_records_as_absent_is_removed_again`
  - `tests/test_restore.py::test_a_recovery_is_not_refused_by_the_latch_whose_remedy_it_is`
  - `tests/test_restore.py::test_a_rehearsal_reports_what_is_outstanding_rather_than_what_it_recorded`
  - `tests/test_restore.py::test_a_restore_returns_the_coupled_state_with_the_database`
  - `tests/test_restore.py::test_blocking_2_a_failure_mid_restore_is_a_structured_refusal`
  - `tests/test_restore.py::test_blocking_5_an_interrupted_restore_in_a_none_effect_window_latches`
  - `tests/test_restore.py::test_round2_a_completed_restore_discharges_an_earlier_interrupted_one`
  - `tests/test_restore.py::test_round2_repeating_a_failing_restore_does_not_accumulate_latches`
  - `tests/test_restore.py::test_round2_three_attempts_stage_their_logs_side_by_side`
  - `tests/test_restore.py::test_round6_the_performing_backstop_names_what_it_already_moved`
  - `tests/test_write_session.py::test_a_recovery_closes_as_a_recovery`

Old text:

```
            state=SessionState.CLOSED,
            intent=intent,
            identity_provider=identity_provider,
```

New text:

```
            state=SessionState.CLOSED,
            intent=Intent.WRITE,
            identity_provider=identity_provider,
```

### `r375-a.S7_close_drops_the_identity_seam`

_recorded: do not forward the identity provider to the gated close, so it asserts the volume through this machine's default

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S7_close_drops_the_identity_seam`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 4 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_recorded_commit_is_on_disk_before_the_session_ends`
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`
  - `tests/test_write_session.py::test_the_record_names_the_holder_the_lock_names`

Old text:

```
            intent=intent,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
```

New text:

```
            intent=intent,
            mount_enumerator=mount_enumerator,
            now=now,
        )
    except BaseException:
```

### `r375-a.S8_record_names_no_actor`

_recorded: record no actor, so the log cannot say who acknowledged the backup this write ran behind

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S8_record_names_no_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`

Old text:

```
        actor=acknowledgment.actor,
```

New text:

```
        actor=None,
```

### `r375-a.S9_record_names_no_acknowledgment`

_recorded: record no acknowledgment instant

- File: `src/cratekit/core/session.py`
- Source: `r375-a.json`, row `S9_record_names_no_acknowledgment`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_tree_writer.py`, `tests/test_metadata_cli.py`, `tests/test_restore.py`
- Collected: 392 against a baseline of 392
- Kills: 2 (killed)
- Killed:
  - `tests/test_tree_writer.py::test_a_membership_write_is_listed_as_restorable_with_its_per_tree_counts`
  - `tests/test_write_session.py::test_the_record_is_the_gates_own_workflow_actor_and_acknowledgment`

Old text:

```
        acknowledged_at=acknowledgment.recorded_at.isoformat(),
```

New text:

```
        acknowledged_at=None,
```

### `a32.A2_stale_deleted`

A row deleted since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A2_stale_deleted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `a32.A3_stale_value`

A row whose column moved since the plan is still written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A3_stale_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_changed_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        elif _text(row.get(probe.column)) != probe.was:
```

New text:

```
        elif False:
```

### `a32.A5_policy_widened`

The commit's policy admits both probe columns whatever the plan writes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `A5_policy_widened`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_writing_one_column_admits_only_that_one_to_the_guard`

Old text:

```
    policy = rb_writer.row_probe_policy(p.column for p in plan.writing)
```

New text:

```
    policy = rb_writer.row_probe_policy(rb_writer.ROW_PROBE_COLUMNS)
```

### `a32.D1_digest_drops_replaced`

Drop the replaced value from the item, so the digest does not move when it changes

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D1_digest_drops_replaced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_moves_with_the_rows_the_columns_and_both_values`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
            "from": self.was,
```

New text:

```
            "from": "",
```

### `a32.D2_digest_unordered`

Keep the triples in the order given, so the same plan digests two ways

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `D2_digest_unordered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_digest_is_equal_whatever_order_the_triples_are_given_in`

Old text:

```
    probes.sort(key=lambda p: (len(p.content_id), p.content_id, p.column))
```

New text:

```
(empty)
```

### `a32.J1_wrong_unjudged`

The judge never reports a value that did not take

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J1_wrong_unjudged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_names_a_value_that_did_not_take_and_a_column_that_moved`

Old text:

```
            if now.get(probe.column) is None or _text(now[probe.column]) != str(probe.value):
```

New text:

```
            if False:
```

### `a32.J2_planned_across_rows`

The judge excuses every column the plan writes on any row, not the row's own

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J2_planned_across_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_judge_counts_a_column_written_on_another_row_as_moved_here`

Old text:

```
        changed = row_defaults.moved_columns(was, now, planned=plan.columns_on(content_id))
```

New text:

```
        changed = row_defaults.moved_columns(was, now, planned=[p.column for p in plan.writing])
```

### `a32.J4_moved_not_refused`

A moved column is reported as a wrong value rather than the guard's defect

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `J4_moved_not_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`
  - `tests/test_repair_link.py::test_assert_read_back_refuses_a_moved_column_as_the_guards_defect`

Old text:

```
    if written.moved:
        raise refuse(
            "whitelist-violation",
```

New text:

```
    if False:
        raise refuse(
            "whitelist-violation",
```

### `a32.P1_tombstone_plans`

Drop the live row filter from the plan's row query, so a tombstone plans

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P1_tombstone_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_tombstone_refuses_as_unknown_though_the_row_is_in_the_table`

Old text:

```
                    f"WHERE ID = :id AND {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
                    f"WHERE ID = :id"
```

### `a32.P2_unknown_row`

Drop the unknown row refusal, so an absent identifier falls through

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P2_unknown_row`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_refusal_reaches_no_gate`
  - `tests/test_repair_link.py::test_a_tombstone_refuses_as_unknown_though_the_row_is_in_the_table`
  - `tests/test_repair_link.py::test_an_unknown_identifier_refuses_by_name_before_any_gate`
  - `tests/test_repair_link.py::test_one_bad_triple_refuses_the_whole_plan`

Old text:

```
        if row is None:
            raise refuse(
                ROW_UNKNOWN,
```

New text:

```
        if row is None and False:
            raise refuse(
                ROW_UNKNOWN,
```

### `a32.P3_unheld_value`

Drop the unheld value refusal, so a value nobody carries is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P3_unheld_value`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_value_no_other_live_row_carries_refuses`
  - `tests/test_repair_link.py::test_a_value_only_a_tombstone_carries_refuses_as_unheld`

Old text:

```
        if probe.writes and carriers == 0:
```

New text:

```
        if probe.writes and carriers < 0:
```

### `a32.P4_count_tombstones`

Count tombstones as carriers and fellows of a value

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P4_count_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_null_counts_its_fellows_as_null_so_writing_one_back_is_the_minority`
  - `tests/test_repair_link.py::test_a_value_only_a_tombstone_carries_refuses_as_unheld`
  - `tests/test_repair_link.py::test_the_bindings_value_onto_a_row_rekordbox_made_refuses_as_the_minority`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`
  - `tests/test_repair_link.py::test_the_two_acts_write_each_triple_and_move_no_other_column`

Old text:

```
            f"AND {rb_writer.SOFT_DELETE_COLUMN} = 0 AND ID != :id"
```

New text:

```
            f"AND ID != :id"
```

### `a32.P6_writes_always`

Every triple writes, a row already at the value included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P6_writes_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 6 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_a_value_nobody_else_carries_still_plans_nothing`
  - `tests/test_repair_link.py::test_a_row_already_at_the_value_plans_nothing_for_that_triple`
  - `tests/test_repair_link.py::test_a_triple_already_at_its_value_is_shown_and_not_written`
  - `tests/test_repair_link.py::test_apply_refuses_a_plan_that_writes_nothing_as_a_defect`
  - `tests/test_repair_link.py::test_judge_skips_a_triple_that_writes_nothing`

Old text:

```
        return self.was != str(self.value)
```

New text:

```
        return True
```

### `a32.P7_minority_boundary`

Move the majority rule's boundary, so a value carried by as many rows as the row's own is written

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P7_minority_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_value_carried_by_as_many_rows_as_the_rows_own_refuses_too`

Old text:

```
        if probe.writes and carriers <= fellows:
```

New text:

```
        if probe.writes and carriers < fellows:
```

### `a32.P8_null_fellows`

Count a NULL's fellows with an equality, which matches nothing, so a NULL has no fellows

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `P8_null_fellows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    test = f"{column} IS NULL" if value is None else f"{column} = :value"
```

New text:

```
    test = f"{column} = :value"
```

### `a32.V1_any_column`

A triple naming a column outside the probe set is parsed, AnalysisUpdated included

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V1_any_column`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:AnalysisUpdated=2]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:BPM=12800]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:Title=x]`
  - `tests/test_repair_link.py::test_a_malformed_triple_refuses_through_the_verb_before_any_gate`

Old text:

```
    if kind is None:
        raise _invalid(
```

New text:

```
    if False:
        raise _invalid(
```

### `a32.V2_link_not_converted`

A ContentLink value is kept as text rather than converted to a whole number

- File: `src/cratekit/write/row_link.py`
- Source: `a32.json`, row `V2_link_not_converted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=]`
  - `tests/test_repair_link.py::test_a_malformed_triple_or_a_column_outside_the_probe_refuses_by_name[101:ContentLink=lots]`
  - `tests/test_repair_link.py::test_a_triple_reads_row_column_and_a_value_of_the_columns_type`
  - `tests/test_repair_link.py::test_the_plan_is_each_triple_its_values_and_who_else_carries_each`

Old text:

```
    if kind is int:
```

New text:

```
    if False:
```

### `a32.C1_ack_after_gate`

The backup acknowledgment is not read before the gate

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C1_ack_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

    plan = _plan(cfg, ctx.args)
```

New text:

```
    plan = _plan(cfg, ctx.args)
```

### `a32.C2_abort_writes`

An abort at the gate proceeds to the write

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C2_abort_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_an_abort_writes_nothing`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) not in ("apply", "abort"):
```

### `a32.C3_nothing_to_write_applies`

A plan that writes nothing reaches the apply

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C3_nothing_to_write_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_plan_where_every_row_is_already_at_its_value_still_asks_and_writes_nothing`

Old text:

```
    if not plan.writes:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

New text:

```
    if False:
        return ctx.envelope(data=data, outcome=Outcome.NO_OP, warnings=[_nothing(plan)])
```

### `a32.C4_read_back_unasserted`

The verb answers OK without asserting the read back

- File: `src/cratekit/write/row_link_cli.py`
- Source: `a32.json`, row `C4_read_back_unasserted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_link.py`
- Collected: 59 against a baseline of 59
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_link.py::test_a_column_moved_after_the_commit_refuses_through_the_verb`

Old text:

```
    row_link.assert_read_back(written)
    data["totals"] = {
```

New text:

```
    data["totals"] = {
```

### `u102-a.P1_root_boundary`

_under: match the root as a bare prefix, without the separator, so a sibling folder sharing the prefix is inside it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P1_root_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_that_only_shares_a_prefix_is_not_the_folder`

Old text:

```
    return held == wanted or held.startswith(wanted + "/")
```

New text:

```
    return held == wanted or held.startswith(wanted)
```

### `u102-a.P2_root_casefold`

_key: compare the root exactly instead of casefolded

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P2_root_casefold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_typed_in_another_case_still_names_the_folder`

Old text:

```
    return locations.norm_for_compare(path).casefold()
```

New text:

```
    return locations.norm_for_compare(path)
```

### `u102-a.P3_root_filter`

_plan_for: ignore the root, so an accepted item outside it is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P3_root_filter`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_root_limits_the_apply_and_counts_what_it_left_out`
  - `tests/intake/test_repair_apply.py::test_a_root_that_only_shares_a_prefix_is_not_the_folder`

Old text:

```
        if accepted.path is not None and not _under(accepted.path, root):
```

New text:

```
        if False:
```

### `u102-a.P4_unchanged`

_plan_for: stop setting aside a proposal that names the file's own name, so it is planned as a rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P4_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_that_asked_for_no_change_is_listed_with_its_reason`

Old text:

```
        if path.name == accepted.proposed:
```

New text:

```
        if False:
```

### `u102-a.P5_missing`

_plan_for: stop setting aside an accepted item whose file is gone, so the run after an apply plans it again

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P5_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_second_apply_converges_and_claims_only_what_it_observed`
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`

Old text:

```
        if not path.is_file():
            # ONE CLASS
```

New text:

```
        if False:
            # ONE CLASS
```

### `u102-a.P6_missing_says_what_exists`

_plan_for: always word a missing file as a rename already carried out, whether or not any file carries the proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `P6_missing_says_what_exists`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_accepted_file_that_is_gone_says_no_file_carries_the_name`

Old text:

```
            if target.is_file():
                why = (
```

New text:

```
            if True:
                why = (
```

### `u102-a.U1_no_stored_path`

_unusable_why: drop the refusal over an item the queue holds no path for

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U1_no_stored_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
    if accepted.path is None:
        return (
```

New text:

```
    if False:
        return (
```

### `u102-a.U2_bare_filename`

_unusable_why: stop requiring the proposed name to be a bare filename, so a path with a separator is applied

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U2_bare_filename`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[../escaped.flac-not a bare filename]`
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[nested/inside.flac-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if not proposed or proposed in {".", ".."}:
```

### `u102-a.U3_empty_name`

_unusable_why: stop refusing an empty proposed name

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U3_empty_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[-not a bare filename]`

Old text:

```
    if not proposed or proposed in {".", ".."} or Path(proposed).name != proposed:
```

New text:

```
    if proposed in {".", ".."} or Path(proposed).name != proposed:
```

### `u102-a.U4_same_suffix`

_unusable_why: drop the check that the proposed name keeps the file's extension

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U4_same_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposed_name_that_is_not_a_same_suffix_filename_is_never_applied[04A - 124 - Song - Artist.txt-change the file's extension]`

Old text:

```
    if Path(proposed).suffix.lower() != Path(accepted.path).suffix.lower():
```

New text:

```
    if False:
```

### `u102-a.U5_linked_file`

_unusable_why: drop the check that the stored path names the file the proposal was shown for, so a link's target is renamed

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-a.json`, row `U5_linked_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_linked_file_is_never_renamed_through_its_link`

Old text:

```
    if accepted.recorded and Path(accepted.path).name != accepted.recorded:
```

New text:

```
    if False:
```

### `u102-b.G1_plan_referenced`

_plan_for: treat no candidate as referenced, leaving only the post gate check to hold the file

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G1_plan_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
        if not naming_cli.is_referenced(path, referenced)
    ]
```

New text:

```
        if True
    ]
```

### `u102-b.G2_post_gate_referenced`

_apply: drop the referenced check made after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G2_post_gate_referenced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_row_that_appears_after_the_gate_holds_the_file`

Old text:

```
        if naming_cli.is_referenced(path, referenced):
            _owed(
```

New text:

```
        if False:
            _owed(
```

### `u102-b.G4_plan_collisions`

_plan_for: detect no collision while the plan is built, leaving it to the claim

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G4_plan_collisions`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
    collides = naming_cli.held_collisions([(path, acc.proposed) for acc, path in free])
```

New text:

```
    collides: dict[str, str] = {}
```

### `u102-b.G5_claim`

_apply: skip the atomic claim, so a name taken after the gate is overwritten by the rename

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G5_claim`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_name_taken_after_the_gate_is_never_overwritten`
  - `tests/intake/test_repair_apply.py::test_a_name_the_filesystem_refuses_to_claim_is_named`

Old text:

```
            claimed = naming.claim_target(target)
```

New text:

```
            claimed = True
```

### `u102-b.G6_abort`

_apply: carry on past an abort answer

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G6_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_the_gate_refuses_unanswered_and_an_abort_touches_nothing`
  - `tests/intake/test_repair_apply.py::test_the_gate_shows_every_item_the_digest_was_taken_over`

Old text:

```
    if option == "abort":
```

New text:

```
    if False:
```

### `u102-b.G7_referenced_is_owed`

_HELD: stop counting a referenced file as an accepted rename that did not happen, so the run answers ok over it

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G7_referenced_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (COLLIDES, UNUSABLE)
```

### `u102-b.G8_collision_is_owed`

_HELD: stop counting a collision as owed, which is R-172 itself, a skipped collision reported as ok

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G8_collision_is_owed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_collision_refuses_that_file_and_names_it`
  - `tests/intake/test_repair_apply.py::test_two_accepted_proposals_for_one_name_rename_neither`

Old text:

```
_HELD = (REFERENCED, COLLIDES, UNUSABLE)
```

New text:

```
_HELD = (REFERENCED, UNUSABLE)
```

### `u102-b.G9_post_gate_missing`

_apply: drop the check that the file is still there after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `G9_post_gate_missing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_file_deleted_after_the_gate_is_named_and_not_called_renamed`

Old text:

```
        if not path.is_file():
            _owed(item, "the file is no longer there")
            continue
```

New text:

```
(empty)
```

### `u102-b.R1_retryable_seed`

_apply: call a run retryable when all it holds is a file only a person can release

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R1_retryable_seed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_proposal_for_a_referenced_file_refuses_and_its_sibling_is_renamed`
  - `tests/intake/test_repair_apply.py::test_an_item_with_no_stored_path_is_held_and_never_guessed_at`

Old text:

```
        item["action"] in _HELD and item["action"] not in _NEEDS_A_PERSON
```

New text:

```
        item["action"] in _HELD
```

### `u102-b.R2_retryable_after_gate`

_owed: stop marking the run retryable when a rename fails after the gate

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `R2_retryable_after_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_refused_rename_is_named_and_leaves_no_stub`

Old text:

```
        nonlocal retryable
        retryable = True
```

New text:

```
        nonlocal retryable
```

### `u102-b.S1_stub_removed`

_apply: leave the zero byte claim behind when the rename did not happen

- File: `src/cratekit/intake/repair_cli.py`
- Source: `u102-b.json`, row `S1_stub_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_repair_apply.py`
- Collected: 33 against a baseline of 33
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_repair_apply.py::test_a_refused_rename_is_named_and_leaves_no_stub`
  - `tests/intake/test_repair_apply.py::test_an_interrupt_between_the_claim_and_the_rename_leaves_no_stub`

Old text:

```
            if not moved:
                target.unlink(missing_ok=True)
```

New text:

```
            if not moved:
                pass
```

### `r227.A1_floored_days`

Staleness is judged on floored whole days, so seven days and one second is not past seven

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A1_floored_days`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return age is not None and age.days > self.limit_days
```

### `r227.A2_never_stale`

No export is ever stale, which is the tree before this unit

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A2_never_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 13 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_old_means_past_the_limit_and_not_at_it`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`
  - `tests/test_sync_all.py::test_a_pass_that_queued_over_an_old_export_warns_and_still_queues`
  - `tests/test_sync_all.py::test_the_composed_gate_names_the_exports_date_beside_what_would_queue`

Old text:

```
        return age is not None and age.total_seconds() > self.limit_days * _SECONDS_PER_DAY
```

New text:

```
        return False
```

### `r227.A3_future_clamped`

A date far in the future is never future dated, so it clamps to an age of nothing and reads as recent

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A3_future_clamped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be`

Old text:

```
        return self.written - self.judged_at > FUTURE_TOLERANCE
```

New text:

```
        return False
```

### `r227.A4_no_tolerance`

No tolerance at all, so a volume whose clock runs a few hours ahead is future dated

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A4_no_tolerance`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_few_hours_ahead_is_a_clock_and_reads_as_written_just_now`

Old text:

```
FUTURE_TOLERANCE = timedelta(days=1)
```

New text:

```
FUTURE_TOLERANCE = timedelta(0)
```

### `r227.A5_half_a_pair`

The constructor accepts a date with no instant to judge it at

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A5_half_a_pair`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_age_is_built_whole_or_not_at_all`

Old text:

```
        if (self.written is None) != (self.judged_at is None):
```

New text:

```
        if False:
```

### `r227.A6_conversion_unguarded`

Only the stat is guarded, so a modification time no date can hold escapes as a traceback

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A6_conversion_unguarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash`

Old text:

```
    except (OSError, OverflowError, ValueError):
```

New text:

```
    except FileNotFoundError:
```

### `r227.A7_unreadable_reads_as_now`

A file that cannot be asked its date is reported as written this instant

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r227.json`, row `A7_unreadable_reads_as_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_modification_time_no_date_can_hold_is_unknown_rather_than_a_crash`
  - `tests/test_outbound_workers.py::test_an_age_that_cannot_be_read_is_unknown_rather_than_fresh`

Old text:

```
        return ExportAge(path=located, limit_days=limit_days)

```

New text:

```
        return ExportAge(path=located, limit_days=limit_days, written=datetime.now(timezone.utc), judged_at=datetime.now(timezone.utc))

```

### `r356-b.B1_naming_head_left_on_the_release_title`

The release title is the display title, key and tempo head and all, which agrees with no provider title

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B1_naming_head_left_on_the_release_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_configuration_with_no_marker_text_still_strips_the_head`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_the_release_title_is_the_display_title_with_the_naming_head_off`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
    return naming.strip_heads(entry.name, template=template)
```

New text:

```
    return entry.name
```

### `r356-b.B2_template_declares_no_lossy_marker`

The template never declares the marker, so a marked lossy copy keeps it in its release title

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B2_template_declares_no_lossy_marker`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_release_title_is_the_display_title_with_the_naming_head_off`

Old text:

```
    if not marker:
        return naming.NameTemplate()
```

New text:

```
    if True:
        return naming.NameTemplate()
```

### `r356-b.B3_empty_marker_no_longer_guarded`

A configuration with no marker text builds a marker rule with an empty literal, which is refused at construction, so every item fails over a naming policy

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B3_empty_marker_no_longer_guarded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_configuration_with_no_marker_text_still_strips_the_head`

Old text:

```
    if not marker:
        return naming.NameTemplate()
```

New text:

```
    if False:
        return naming.NameTemplate()
```

### `r356-b.B4_heart_candidate_carries_no_artist`

A favourite reaches the account with a title and no artist, which chooses nothing

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r356-b.json`, row `B4_heart_candidate_carries_no_artist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`

Old text:

```
            release_title=release_title(entry, template=template),
            artist=entry.artist,

```

New text:

```
            release_title=release_title(entry, template=template),

```

### `u121-b.S10r_folder_row_removed`

_folder_row: a folder rekordbox removed since the plan is still written into

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121-b.json`, row `S10r_folder_row_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_members_keep_the_sets_order_when_it_is_not_alphabetical`

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
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_off_the_jobs_page_when_no_flag_is_given`

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
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_rerun_that_adds_nothing_records_no_commit`

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
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
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
- Collected: 73 against a baseline of 73
- Kills: 15 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_honours_posted_on_a_pre_freeze_job`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_track_accepted_at_review_as_a_library_file_joins_the_playlist_at_a_landing`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_follows_the_live_inspiration_row_on_the_disposable_database`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_refuses_a_playlist_a_legacy_archive_prefixed`
  - `tests/test_set_inspiration_playlist.py::test_export_set_rename_renames_a_set_the_landing_archived_and_it_stays_taken`
  - `tests/test_set_inspiration_playlist.py::test_members_keep_the_sets_order_when_it_is_not_alphabetical`
  - `tests/test_set_inspiration_playlist.py::test_posted_on_a_frozen_job_names_another_day_and_the_frozen_name_wins_with_a_warning`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_off_the_jobs_page_when_no_flag_is_given`
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
- Collected: 73 against a baseline of 73
- Kills: 5 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_row_that_resolves_only_to_a_different_version_is_not_guessed`
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
- Collected: 73 against a baseline of 73
- Kills: 2 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_from_the_page_with_the_uploader_taken_off_the_title`
  - `tests/test_set_inspiration_playlist.py::test_the_words_come_off_the_jobs_page_when_no_flag_is_given`

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
- Collected: 73 against a baseline of 73
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

### `u121.S4_page_beats_flag`

words_for: the page's uploader wins over --dj

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S4_page_beats_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_flag_wins_over_the_page_and_a_day_is_read_as_its_month`

Old text:

```
    who = (dj if dj is not None else str(page.get(fetch.PAGE_UPLOADER) or "")).strip()
```

New text:

```
    who = str(page.get(fetch.PAGE_UPLOADER) or dj or "").strip()
```

### `u121.S5_missing_word`

words_for: a missing word is not refused, the name is made with a hole

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S5_missing_word`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 6 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_page_date_that_is_not_a_date_names_no_month_and_the_flag_is_asked_for`
  - `tests/test_set_inspiration_playlist.py::test_a_set_the_page_and_the_flags_cannot_name_is_refused_before_the_gate`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page0-flags0-missing0]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page1-flags1-missing1]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page2-flags2-missing2]`
  - `tests/test_set_inspiration_playlist.py::test_a_word_neither_the_page_nor_a_flag_gives_is_refused_naming_the_flag[page3-flags3-missing3]`

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
- Collected: 73 against a baseline of 73
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

### `u121.S8_job_state`

set_job_or_refuse: accept a job that has not finished

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u121.json`, row `S8_job_state`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_the_backfill_refuses_a_job_that_is_not_a_set_and_an_unfinished_one`

Old text:

```
    if job.state is not jobs.JobState.SUCCEEDED:
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
- Collected: 73 against a baseline of 73
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

### `u226.M10_settle_lag_known_only`

_settled: a lagging window is read again only when something is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M10_settle_lag_known_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_lags_is_read_again_before_any_move`
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`

Old text:

```
                if problem == "window-lags":

```

New text:

```
                if problem == "window-lags" and known is not None:

```

### `u226.M11_settle_kept_ignored`

_settled: a caller's kept wording is ignored for the order's

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M11_settle_kept_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`

Old text:

```
        if kept is None:
            kept = (
```

New text:

```
        if True:
            kept = (
```

### `u226.M13_removal_window_wrong`

_removal_read_back: a lagging window is read as a wrong track gone, refused at once

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M13_removal_window_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_beside_a_first_page_refuses_after_the_bound`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
                tracks = "window"

```

New text:

```
                tracks = None

```

### `u226.M15_wait_uncounted`

_paused: the pause is taken and not counted in the record

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M15_wait_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`
  - `tests/test_outbound_window_lag.py::test_the_pause_after_a_412_is_counted_in_the_moves_record`

Old text:

```
        self._sleep(seconds)
        note["waited"] += seconds

```

New text:

```
        self._sleep(seconds)

```

### `u226.M17_removal_positions_unsettled`

remove_tracks: the positions read once with no reread of a lag, as before round one's fix

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M17_removal_positions_unsettled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
            playlist, before = self._settled(
                identifier,
                None,
                exact=False,
                after="removal positions",
                kept="nothing was taken off it",
            )
```

New text:

```
            playlist = self._playlist(identifier)
            before = self._positions(identifier, playlist)
```

### `u226.M18_waited_unformatted`

_waited: seconds named as 7.0 rather than 7

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M18_waited_unformatted`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return f"{seconds:g}"
```

New text:

```
    return f"{seconds}"
```

### `u226.M7_reading_takes_window`

_reading: the window read is the reading even when the unpaged read is whole

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M7_reading_takes_window`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_window_lags_and_unpaged_read_does_not_is_taken_as_done`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_planned_after_a_lagging_window_is_planned_from_the_unpaged_read`

Old text:

```
            unpaged if window == listing.WINDOW_UNPAGED else paged,
```

New text:

```
            paged,
```

### `u226.M8_unpaged_first`

_reading: the unpaged read taken before the window, so the window's tag is carried

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M8_unpaged_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_past_the_first_hundred_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_a_removal_planned_from_a_lagging_window_takes_the_track_where_it_stands`
  - `tests/test_outbound_window_lag.py::test_an_order_past_the_first_hundred_moves_the_track_where_it_stands`

Old text:

```
        tracks = self._listed(playlist_id, playlist)
        paged = [listing.row_id(track) for track in tracks]
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks_unpaged(playlist),
            )
        ]
```

New text:

```
        unpaged = [
            listing.row_id(track)
            for track in self._read(
                f"read the playlist {playlist_id}",
                lambda: listing.playlist_tracks_unpaged(playlist),
            )
        ]
        tracks = self._listed(playlist_id, playlist)
        paged = [listing.row_id(track) for track in tracks]
```

### `u226.M9_positions_no_lag_refusal`

_positions: a lagging window is not refused, its positions taken

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M9_positions_no_lag_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 441 against a baseline of 441
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_first_reading_whose_window_never_catches_up_refuses_with_nothing_moved`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_once_is_read_again_and_lands`
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_later_pages_lag_too_is_held_with_nothing_taken_off`
  - `tests/test_outbound_window_lag.py::test_an_order_whose_later_pages_lag_too_is_held_with_nothing_moved`

Old text:

```
        if window == listing.WINDOW_LAGS:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
```

New text:

```
        if False:
            raise _window_lags(str(playlist_id), "nothing was sent on that reading")
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

### `r375-b.M1_capture_never_attached`

mytags_vocals: take the capture and never attach it, which is R-375 itself with a record beside it

- File: `src/cratekit/write/metadata_cli.py`
- Source: `r375-b.json`, row `M1_capture_never_attached`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_metadata_cli.py`
- Collected: 26 against a baseline of 26
- Kills: 3 (killed)
- Killed:
  - `tests/test_metadata_cli.py::test_an_apply_is_listed_by_restore_list_as_a_restorable_session`
  - `tests/test_metadata_cli.py::test_an_apply_that_refuses_mid_write_is_abandoned_and_claims_no_commit`
  - `tests/test_metadata_cli.py::test_the_capture_is_protected_while_the_apply_is_in_flight`

Old text:

```
            session.attach_capture(record, capture.root, cfg)

```

New text:

```
(empty)
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

### `u154.G10_read_back_path_unchecked`

a row committed with a path other than the planned one is reported as shelved

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G10_read_back_path_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            if str(stored or "") != row.folder_path:

```

New text:

```
            if False:

```

### `u154.G11_kept_columns_unchecked`

a column the shelve does not own may change without the read back saying so

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G11_kept_columns_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`

Old text:

```
            if before.get(row.content_id) != after.get(row.content_id):

```

New text:

```
            if False:

```

### `u154.G14_reserved_folders_are_candidates`

the processed tree and the sets folder are planned as batches under --all

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G14_reserved_folders_are_candidates`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_two_batches_filing_to_one_name_get_two_and_a_taken_target_is_passed_over`

Old text:

```
        if entry.name.startswith(".") or entry.name in reserved:

```

New text:

```
        if entry.name.startswith("."):

```

### `u154.G15_stored_target_under_mounted_path`

the confinement check reads under the mounted target and not the stored one

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G15_stored_target_under_mounted_path`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`

Old text:

```
            {"prefix": _like_prefix(one.stored_target)},

```

New text:

```
            {"prefix": _like_prefix(str(one.target))},

```

### `u154.G17_refusal_before_rename_rewrapped`

a stale plan refusal before any rename is rewrapped as a write failure

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G17_refusal_before_rename_rewrapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_engine_refuses_a_target_made_between_its_plan_and_its_apply_in_its_own_words`

Old text:

```
            if not moved and isinstance(exc, CratekitError):

```

New text:

```
            if False:

```

### `u154.G1_policy_not_registered`

the path column is written with no field policy registered for the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G1_policy_not_registered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 11 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_batch_named_twice_is_planned_once`
  - `tests/test_intake_shelve.py::test_a_library_whose_drive_was_renamed_stores_and_confines_under_the_base_drive`
  - `tests/test_intake_shelve.py::test_a_row_under_a_folder_differing_only_in_case_is_not_this_plans_business`
  - `tests/test_intake_shelve.py::test_a_shelved_batch_name_stays_taken_so_a_landing_that_day_takes_the_next`
  - `tests/test_intake_shelve.py::test_a_target_free_on_disk_but_holding_rows_in_the_collection_is_passed_over`
  - `tests/test_intake_shelve.py::test_an_unreadable_session_record_makes_the_name_rule_refuse_rather_than_read_a_name_free`
  - `tests/test_intake_shelve.py::test_apply_moves_the_folder_rewrites_the_paths_and_keeps_every_other_column`
  - `tests/test_intake_shelve.py::test_nothing_under_the_processed_tree_is_touched_by_a_shelve`
  - `tests/test_intake_shelve.py::test_the_grid_suites_still_see_no_tempo_on_the_moved_rows`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[kept-column]`
  - `tests/test_intake_shelve.py::test_the_read_back_refuses_a_row_that_did_not_take_or_lost_a_column[path]`

Old text:

```
            with rb_writer.field_policies_for_commit(rb_writer.SHELVE_POLICY):
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
            if True:
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

### `u154.G2_confinement_dropped`

the SQL confinement check is skipped before the commit

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G2_confinement_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_that_the_plan_did_not_put_there_refuses_the_commit`

Old text:

```
                _assert_confined(db, plan)
                rb_writer.commit_guarded(db)

```

New text:

```
                rb_writer.commit_guarded(db)

```

### `u154.G3_rename_back_dropped`

a failure past the rename leaves the folder at its new name

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G3_rename_back_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_commit_that_fails_after_the_rename_puts_the_folder_back`
  - `tests/test_intake_shelve.py::test_a_row_under_the_target_that_the_plan_did_not_put_there_refuses_the_commit`

Old text:

```
            failed = _rename_back(moved)

```

New text:

```
            failed: list[str] = []

```

### `u154.G4_stale_target_check_dropped`

a target made after the plan is renamed over at apply

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G4_stale_target_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_the_engine_refuses_a_target_made_between_its_plan_and_its_apply_in_its_own_words`

Old text:

```
    if os.path.lexists(one.target):
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

New text:

```
    if False:
        raise refuse(
            "decision-stale",
            f"{one.target} exists now and did not when the plan was made, so nothing "

```

### `u154.G5_unmatched_file_shelved_anyway`

a batch with a file the collection does not hold is moved anyway

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G5_unmatched_file_shelved_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_batch_whose_file_has_no_row_is_refused_whole_and_nothing_moves`

Old text:

```
        if unmatched is not None:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

New text:

```
        if False:
            leave(batch, _why_unmatched(*unmatched))
            continue

```

### `u154.G6_subfolder_check_dropped`

a batch folder holding a subfolder is planned

- File: `src/cratekit/intake/shelve.py`
- Source: `u154.json`, row `G6_subfolder_check_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_shelve.py`
- Collected: 43 against a baseline of 43
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_shelve.py::test_a_folder_with_a_subfolder_and_a_name_of_neither_shape_are_skipped_under_all`

Old text:

```
        if any(entry.is_dir() for entry in folder.iterdir()):

```

New text:

```
        if False:

```

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

