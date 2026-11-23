# Mutation table: u309-replay-after-a

Measured by `scripts/mutate.py` on 2026-11-22 22:38 UTC, branch `HEAD` at `a8eb5df7`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22910 collected. pytest invocations for this batch: 161.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 22:37 UTC for commit `a8eb5df718cb`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 55, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22910 against 22910. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r837-a.A8_load_carries_sets` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 416 | 23 | killed |
| `r229.L18_contents_grow` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 5 | killed |
| `r229.L19_a_copy_not_a_move` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 6 | killed |
| `r229.L1_a_third_suffices` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r572.E1_export_drop_album` | `src/cratekit/modules/outbound/export.py` | user | 1 file(s) | 64 | 1 | killed |
| `r1411.S3_order_does_not_pass_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 2 | killed |
| `u231.M6_settle_lag_taken` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 4 | killed |
| `u142.S1_folder_prefix` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 228 | 13 | killed |
| `u142.S6_reserve_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 228 | 7 | killed |
| `r837-a.A12_in_folder_not_moved` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 3 | killed |
| `r879-b.S10_unnamed_exact_said_to_resemble_nothing` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 1 | killed |
| `r837-b.B1_ref_only_from_the_provider` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 1 | killed |
| `r1017.M9_twin_only_beside_to` | `src/cratekit/modules/outbound/sets.py` | user | 4 file(s) | 195 | 2 | killed |
| `u140.B7_twin_refusal_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 4 | killed |
| `u214.M14_old_not_yours` | `src/cratekit/organize/rekordbox.py` | user | 6 file(s) | 199 | 2 | killed |
| `u207.M2_mirror_counts_a_screen_as_one` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 71 | 2 | killed |
| `u137.A5_filing_for_yours` | `src/cratekit/organize/account.py` | user | 2 file(s) | 117 | 2 | killed |
| `u123.L2_forget_drops_the_entry` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 3 file(s) | 108 | 2 | killed |
| `u143-c.A2_ledger_claimed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 446 | 1 | killed |
| `r835-b.T2_refused_move_raised` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 286 | 1 | killed |
| `r835-c.F7_only_a_provider_failure_is_unreadable_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `u230.K2_u227_known_guard` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 5 | killed |
| `u230.M16_unread_raises` | `src/cratekit/organize/mirror_downloads.py` | user | 11 file(s) | 209 | 1 | killed |
| `u230.M20_queue_not_passed` | `src/cratekit/organize/account_mirror.py` | user | 11 file(s) | 209 | 3 | killed |
| `u230.M15_source_blank` | `src/cratekit/organize/mirror_downloads.py` | user | 11 file(s) | 209 | 6 | killed |
| `u227.R3_all_to_any` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 7 file(s) | 184 | 2 | killed |
| `u236.M8_placed_after_drops_unheld` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 3 | killed |
| `u236.M3_moved_counts_ours` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 3 | killed |
| `u201-composites.C4_settle_none` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 185 | 5 | killed |
| `u201.O2_stale` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 185 | 1 | killed |
| `u201-composites.C5_leave_nothing` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 185 | 6 | killed |
| `u204.D1_one_queue_per_track` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 222 | 1 | killed |
| `u204.P9_unfavourite_settles_out` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u204.D3_owned_recording` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 222 | 2 | killed |
| `u112.C1_report_asks` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 95 | 52 | killed |
| `u137.R2_rotation_for_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 2 | killed |
| `u137-b.A3_marks_gate` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 5 | killed |
| `u116.M12_nested_folders_ignored` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 95 | 1 | killed |
| `u185.R1_organize_not_yours` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 2 | killed |
| `u142.S18_wait_names_no_folder_always` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 3 | killed |
| `u112.O1_year_before_label` | `src/cratekit/organize/own.py` | user | 1 file(s) | 95 | 1 | killed |
| `u137.S1_identity_names_only` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 95 | 1 | killed |
| `r1295.M2_no_id_named` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B5_read_back_exact` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M17_skip_guard` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-b.B2_stale_digest` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M1_refused_row_fatal` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 6 | killed |
| `u144-b.B4_convergence_latch` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u147-d.A2_retired_unnamed` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 37 | 1 | killed |
| `u147-b.M8_move_new_only` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `r1031.M21_run_id_unchecked` | `src/cratekit/organize/mirror_frozen.py` | user | 2 file(s) | 132 | 1 | killed |
| `r1031.M7_remembered_not_counted` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M5_unread_miss_remembered` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 2 | killed |
| `u222.M15_moved_gone_step_silent` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 1 | killed |
| `u222-zeros.M18_label_no_folder` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 1 | killed |
| `u222.M20_every_step_reworded` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 251 | 2 | killed |
| `u150.A7_landed_two_tracks` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 90 | 1 | killed |
| `u150.M3_retire_in_writes` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 5 | killed |
| `u150.A1_inbox_retires` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 69 | 1 | killed |
| `u267.M12_inspiration_set_folder_write_guard` | `src/cratekit/export/set_common.py` | maintainer | 2 file(s) | 87 | 1 | killed |
| `u143-a.R6_one_named_folder` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u255.M12_add_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 7 | killed |
| `u255.M13_add_retried_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u270.E4_row_of_a_recorded_track` | `src/cratekit/modules/outbound/export.py` | user | 4 file(s) | 257 | 1 | killed |
| `u270.C6_one_tracks_failure_is_its_own` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 1 | killed |
| `u220.A1_front_target` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 12 | killed |
| `r1308.M13_accept_tracks_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 8 | killed |
| `r1308.M14_lag_by_or` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 11 | killed |
| `r1308.M20_message_swapped` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 15 | killed |
| `r1032.A8_album_narrow_drops_all` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 11 | killed |
| `r227.A1_floored_days` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 2 | killed |
| `r227.A3_future_clamped` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r356-a.A12_reason_outlives_its_match` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A2_unreadable_track_no_longer_stops_rule_one` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 2 | killed |
| `r572.A5_album_among_all` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A7_artist_not_compared` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 2 | killed |
| `u226.M9_positions_no_lag_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 5 | killed |
| `u51-item-derivation.D3_empty_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 1 | killed |
| `r856-a.S1_tally_zero` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 178 | 7 | killed |
| `r229.C1_the_offer_is_not_digested` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `r229.C2_the_flag_declines_nothing` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 3 | killed |
| `u131.K4_ambiguous_kind` | `src/cratekit/modules/outbound/kinds.py` | user | 2 file(s) | 109 | 2 | killed |
| `u131.K7_kind_folders_kept` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 109 | 5 | killed |
| `u261.O2_account_drops_the_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 209 | 2 | killed |
| `r836-e.P2b_mismatch_read_only_with_nothing_gone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P9_row_in_playlist_keeps_its_track` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 3 | killed |
| `r1255.R5_organize_rotation_warns` | `src/cratekit/organize/rekordbox.py` | user | 3 file(s) | 89 | 1 | killed |
| `u216.M23_read_drops_held` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 12 | killed |
| `u216.M25_dated_no_time` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 3 file(s) | 229 | 1 | killed |
| `u221.R12_hold_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 153 | 18 | killed |
| `u231.M4_resend_with_the_stale_tag` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 6 | killed |
| `r837-a.A1_no_record_creates` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 4 | killed |
| `u140.B1_ledger_folds_into_a_twin` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 29 | 1 | killed |
| `u236.M19_ledger_normalizer_drops` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 223 | 8 | killed |
| `u236.M21_frozen_not_overlaid` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 223 | 2 | killed |
| `u147-c.M16_folder_made_twice` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 34 | 2 | killed |
| `r1031.M3_signature_keys_a_coded_row` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `u150.M7_refusal_scope` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u255.M1_playlist_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `r572.S1_album_not_read` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 3 | killed |
| `r834.M5_a_create_is_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `sitting4.G3_builders_ignore_the_prefix_map` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `sitting4.G10_absent_root_reads_as_untagged` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `r836-a.A4_no_video_declared` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 501 | 1 | killed |
| `u129-author.A12_archive_backfill_swallows_all` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 24 | 1 | killed |

## Row definitions

### `r837-a.A8_load_carries_sets`

ledger._load: the sets map is dropped on read, so every later write forgets each set playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A8_load_carries_sets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 416 against a baseline of 416
- Kills: 23 (killed)
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
  - ... and 8 more, see the JSON sidecar

Old text:

```
            for key, value in sets.items()
```

New text:

```
            for key, value in ()
```

### `r229.L18_contents_grow`

The recorded contents are appended to rather than replaced, which is the ever growing log the review found

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L18_contents_grow`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 5 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_an_adopted_record_moves_and_no_playlist_is_created`
  - `tests/modules/test_outbound.py::test_the_move_is_reported_once_under_the_per_item_shape`
  - `tests/modules/test_outbound.py::test_the_recorded_contents_are_replaced_and_not_grown`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`

Old text:

```
        record["tracks"] = contents
        dirty = True
```

New text:

```
        record["tracks"] = [*_listed(record, "tracks"), *contents]
        dirty = True
```

### `r229.L19_a_copy_not_a_move`

The adopted record is copied to the new key and left under the old one, so two keys name one remote playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L19_a_copy_not_a_move`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 6 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_an_adopted_record_moves_and_no_playlist_is_created`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - `tests/test_outbound_workers.py::test_a_renamed_crate_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_two_crates_offered_one_orphan_do_not_both_get_it`

Old text:

```
    record = playlists.pop(recorded_key)
```

New text:

```
    record = dict(playlists[recorded_key])
```

### `r229.L1_a_third_suffices`

The share of a record's tracks a crate must still carry drops from a half to a third, so two of five is recognised

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L1_a_third_suffices`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_is_recognised_when_the_crate_still_carries_half_its_tracks[two-of-five]`
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`

Old text:

```
SHARED_DENOMINATOR = 2
```

New text:

```
SHARED_DENOMINATOR = 3
```

### `r572.E1_export_drop_album`

The export engine stops passing the album to match_track

- File: `src/cratekit/modules/outbound/export.py`
- Source: `r572.json`, row `E1_export_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_the_export_plan_hands_the_account_the_files_album_tag`

Old text:

```
            album=track.album,
```

New text:

```
(empty)
```

### `r1411.S3_order_does_not_pass_agreed`

order_tracks takes agreed and never hands it to the judged reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S3_order_does_not_pass_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
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

### `u231.M6_settle_lag_taken`

adapter settle: a reading whose window lags is answered as the order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M6_settle_lag_taken`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_settle_reading_waits_then_reads_once_and_names_a_lag`
  - `tests/test_outbound_window_lag.py::test_a_window_that_catches_up_beside_a_first_page_settles_as_done`
  - `tests/test_outbound_window_lag.py::test_a_window_that_lags_beside_a_first_page_is_not_read_back_between_moves`
  - `tests/test_outbound_window_lag.py::test_every_judged_reading_records_its_readings_and_wait`

Old text:

```
        if window == listing.WINDOW_LAGS:
            note["window_lagged"] += 1
            note["outcome"] = "lags"
            return None
```

New text:

```
        if False:
            return None
```

### `u142.S1_folder_prefix`

sets: drop the Downloaded Sets prefix, so a set is filed into the plain year folder the filing owns

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S1_folder_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 228 against a baseline of 228
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

### `u142.S6_reserve_under_the_year`

apply_archive: record the folder under the plain year key, so the filing reuses the sets' folder

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S6_reserve_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 228 against a baseline of 228
- Kills: 7 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`

Old text:

```
        planned.folder_name,
        lambda: account.create_folder(planned.folder_name),
```

New text:

```
        planned.year,
        lambda: account.create_folder(planned.folder_name),
```

### `r837-a.A12_in_folder_not_moved`

ArchivePlan.move: a playlist already in its folder is moved again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A12_in_folder_not_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
    def move(self) -> bool:
        return self.title is None
```

New text:

```
    def move(self) -> bool:
        return True
```

### `r879-b.S10_unnamed_exact_said_to_resemble_nothing`

_not_chosen: count only identified exact matches before saying none resembles it

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S10_unnamed_exact_said_to_resemble_nothing`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_exact_match_with_no_identifier_is_not_said_to_resemble_nothing`

Old text:

```
        if any(one.exact for one in answer.candidates):
```

New text:

```
        if exact:
```

### `r837-b.B1_ref_only_from_the_provider`

set_cli.match_rows: a list document's row identifier is trusted whatever its origin, so a Spotify id is handed to the account

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B1_ref_only_from_the_provider`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_another_sources_identifier_is_never_handed_to_the_account`

Old text:

```
            if one.ref and one.origin == match.TIDAL:
```

New text:

```
            if one.ref:
```

### `r1017.M9_twin_only_beside_to`

Plan: call a twin only when a record under the new name exists, the pre review rule

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M9_twin_only_beside_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    twin = next((one for one in older if one.remote_id != held.remote_id), None)
```

New text:

```
    twin = next((one for one in older if recorded_to is not None and one.remote_id != held.remote_id), None)
```

### `u140.B7_twin_refusal_dropped`

plan_rename names the twin and goes on to adopt the record under the new name

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B7_twin_refusal_dropped`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    if planned.twin is not None:

```

New text:

```
    if False:

```

### `u214.M14_old_not_yours`

organize rotation step: list Old as the author's own again

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u214.json`, row `M14_old_not_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 199 against a baseline of 199
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_folder_named_old_inside_old_is_a_folder_and_listed_as_yours`
  - `tests/test_inbox_unmirrored.py::test_the_organize_rotation_step_does_not_list_old_as_yours`

Old text:

```
        if node.kind == rotate.LEFT_OLD:
```

New text:

```
        if False:
```

### `u207.M2_mirror_counts_a_screen_as_one`

mirror: Counted counts a screen as one request whatever it spent

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u207.json`, row `M2_mirror_counts_a_screen_as_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_tie.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_mirrors_request_count_holds_what_the_screen_spent_and_no_more`
  - `tests/test_organize_mirror.py::test_soul_with_six_playlists_and_no_mirror_plans_one_folder_and_six_playlists`

Old text:

```
            if name in SCREENS:
```

New text:

```
            if False:
```

### `u137.A5_filing_for_yours`

Skip the filing plan when yours is selected without file

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A5_filing_for_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
    if area.wants(FILE) or area.wants(YOURS):
```

New text:

```
    if area.wants(FILE):
```

### `u123.L2_forget_drops_the_entry`

Keep a removed dated playlist's ledger entry

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u123.json`, row `L2_forget_drops_the_entry`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 108 against a baseline of 108
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_heard_writes_the_ids_merges_and_removes_and_a_second_run_is_a_no_op`

Old text:

```
        kept = {name: pid for name, pid in held.items() if pid != str(remote_id)}
```

New text:

```
        kept = dict(held)
```

### `u143-c.A2_ledger_claimed`

Adapter: remove a root playlist a ledger record names

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A2_ledger_claimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 446 against a baseline of 446
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_ledger_claimed_playlist_or_another_kind_is_refused_with_no_provider_call`

Old text:

```
        if self._cfg is None or self._claimed(identifier):
```

New text:

```
        if self._cfg is None:
```

### `r835-b.T2_refused_move_raised`

TidalAccount.move_to_folder: a move the client answers False is returned as done

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T2_refused_move_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_move_the_client_answers_false_is_a_failure_not_a_quiet_return`

Old text:

```
        if moved is False or moved is _ABSENT:
```

New text:

```
        if moved is _ABSENT:
```

### `r835-c.F7_only_a_provider_failure_is_unreadable_again`

folders.plan: any refusal reading a recorded year outside the folder is passed over as unreadable, a rejected session included

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-c.json`, row `F7_only_a_provider_failure_is_unreadable_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_rejected_session_reading_a_recorded_year_is_raised_not_passed_over`

Old text:

```
                    if placed or exc.cause.reason != "unavailable-transient":
                        raise
```

New text:

```
                    if placed:
                        raise
```

### `u230.K2_u227_known_guard`

_landed_there (U227, sample): a track a snapshot held is still read as landed

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `K2_u227_known_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 5 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u230.py::test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_is_never_read_as_landed`
  - `tests/test_organize_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_keeps_rekordboxs_place`

Old text:

```
    if not places or held:
```

New text:

```
    if not places:
```

### `u230.M16_unread_raises`

queued_from: a queue that cannot be read raises, stopping the organize

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u230.json`, row `M16_unread_raises`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_downloads_queued_from_u230.py::test_a_queue_that_cannot_be_read_names_nothing`

Old text:

```
    except (CratekitError, OSError, ValueError):
        return {}
    held: dict[str, set[str]] = {}
```

New text:

```
    except (CratekitError, OSError, ValueError):
        raise
    held: dict[str, set[str]] = {}
```

### `u230.M20_queue_not_passed`

_read_edits: decide without the queue

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u230.json`, row `M20_queue_not_passed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
landings, queued_on

```

New text:

```
landings, {}

```

### `u230.M15_source_blank`

queued_from: name no source for any job

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u230.json`, row `M15_source_blank`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_downloads_queued_from_u230.py::test_a_cancelled_job_another_source_and_another_library_name_nothing`
  - `tests/test_mirror_downloads_queued_from_u230.py::test_each_track_is_named_with_every_playlist_whose_job_queued_it`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
            held.setdefault(str(remote), set()).add(source)
```

New text:

```
            held.setdefault(str(remote), set()).add("")
```

### `u227.R3_all_to_any`

_landed_there: one band the landing filed is enough, so a second band a person added loses

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R3_all_to_any`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_second_band_added_in_rekordbox_after_the_landing_stands`
  - `tests/test_organize_mirror_edits_u227.py::test_a_refiling_through_adoption_after_the_landing_is_not_the_landings`

Old text:

```
    return bool(there) and all((place.folder, place.playlist) in places for place in there)
```

New text:

```
    return bool(there) and any((place.folder, place.playlist) in places for place in there)
```

### `u236.M8_placed_after_drops_unheld`

placed_after: drop every placement no hold covers, round one's finding 1

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M8_placed_after_drops_unheld`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return {track: at for track, at in placed.items() if track in kept}
```

### `u236.M3_moved_counts_ours`

decide favorites: count a placed month as a move of rekordbox's against a FAVOURITE

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M3_moved_counts_ours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`

Old text:

```
                moved = there_m - was_m - ours - {to}
```

New text:

```
                moved = there_m - was_m - {to}
```

### `u201-composites.C4_settle_none`

settle_mirror_tracks: the library step settles nothing, the thing L2 narrows

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u201-composites.json`, row `C4_settle_none`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_move_in_rekordbox_after_an_edit_was_taken_is_rekordboxs`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed`
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
    wanted = list(settled)
```

New text:

```
    wanted = []
```

### `u201.O2_stale`

_stale: a library moved since the plan is written

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O2_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`

Old text:

```
    if approved.identity() != now.identity():
```

New text:

```
    if False:
```

### `u201-composites.C5_leave_nothing`

plan: a move leaves no tree playlist, the thing O4 narrows

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201-composites.json`, row `C5_leave_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_library_moved_since_the_plan_writes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_move_to_unsorted_clears_the_energy`
  - `tests/test_organize_mirror_edits.py::test_a_move_within_a_genre_keeps_the_genre_and_moves_the_energy_to_the_nearest`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            leave_ids = [pid for pid in held if pid not in wanted and routed(tree.names[pid])]
```

New text:

```
            leave_ids = []
```

### `u204.D1_one_queue_per_track`

mirror_downloads.plan: a track two playlists want is queued twice

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D1_one_queue_per_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued`

Old text:

```
        if decision.track in taken:
```

New text:

```
        if False:
```

### `u204.P9_unfavourite_settles_out`

_decide_favorites: the settle after an unfavourite reads rekordbox as still holding the track

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P9_unfavourite_settles_out`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_taken_off_all_favorites_is_unfavourited_and_settled_out_of_the_folder`

Old text:

```
            if kind == UNFAVOURITE or one.place in extra.get("away", ()):
```

New text:

```
            if one.place in extra.get("away", ()):
```

### `u204.D3_owned_recording`

mirror_downloads.plan: another release of an owned recording is queued

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D3_owned_recording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_recording_the_library_holds_in_no_playlist_is_never_queued`
  - `tests/test_organize_mirror_edits_u204.py::test_another_release_of_an_owned_recording_is_never_queued_nor_swapped`

Old text:

```
            rows = owned(frozen[track].get("isrc")) if track in frozen else ()
```

New text:

```
            rows = ()
```

### `u112.C1_report_asks`

--report no longer returns before the gates, so a report asks and may write

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C1_report_asks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 52 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_registry_the_profile_does_not_use_does_not_refuse_the_filing`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - ... and 37 more, see the JSON sidecar

Old text:

```
    if report:
        data = _report(areas, report=True, answers={})
```

New text:

```
    if False:
        data = _report(areas, report=True, answers={})
```

### `u137.R2_rotation_for_yours`

Skip the rotation plan when yours is selected without rotate

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R2_rotation_for_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(ROTATE) or area.wants(YOURS):
```

New text:

```
    if area.wants(ROTATE):
```

### `u137-b.A3_marks_gate`

Plan the marks whatever the selection

- File: `src/cratekit/organize/account.py`
- Source: `u137-b.json`, row `A3_marks_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`

Old text:

```
    if area.wants(MARKS):
```

New text:

```
    if True:
```

### `u116.M12_nested_folders_ignored`

playlists_in_folders: nested folders are not walked, so a playlist two deep is read as at the root

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M12_nested_folders_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`

Old text:

```
        pending.extend(remote.folder_folders(folder_id))
```

New text:

```
        pass
```

### `u185.R1_organize_not_yours`

organize: list the DEADCA7 folder among the author's own with a home

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u185.json`, row `R1_organize_not_yours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_deadca7s_folder_is_named_once_as_foreign_and_a_full_apply_leaves_it_as_it_was`

Old text:

```
        if name in declared_roots or str(row.ID) in foreign:
```

New text:

```
        if name in declared_roots:
```

### `u142.S18_wait_names_no_folder_always`

_waiting: say no INSPIRATION folder is declared whatever the read answered

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S18_wait_names_no_folder_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_named_for_it_waits_and_is_not_planned`
  - `tests/test_organize.py::test_a_taxonomy_with_no_inspiration_folder_waits_and_says_why`

Old text:

```
        if inspired is not None
        else "no INSPIRATION folder declared in the taxonomy to hold a playlist of its name"
```

New text:

```
        if inspired is None
        else "no INSPIRATION folder declared in the taxonomy to hold a playlist of its name"
```

### `u112.O1_year_before_label`

A year in an account playlist's name wins over the followed label it starts with

- File: `src/cratekit/organize/own.py`
- Source: `u112.json`, row `O1_year_before_label`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_home_is_a_label_then_a_year_and_otherwise_none[kompakt  2021 picks-the Kompakt label folder]`

Old text:

```
    label = label_of(name, labels)
    if label is not None:
        return f"the {label} label folder"
    year = year_of(name)
    if year is not None:
        return f"the {year} year folder"
```

New text:

```
    year = year_of(name)
    if year is not None:
        return f"the {year} year folder"
    label = label_of(name, labels)
    if label is not None:
        return f"the {label} label folder"
```

### `u137.S1_identity_names_only`

Leave the selection out of the area's digest document

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S1_identity_names_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_selection_alone_moves_the_digest_when_it_names_every_step`

Old text:

```
        if self.only is not None:
            identity["only"] = list(self.only)
```

New text:

```
        pass
```

### `r1295.M2_no_id_named`

_read: a refused row with no provider id is named as a miss rather than leaving its set unread

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M2_no_id_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_whose_unread_track_carries_no_provider_id_is_still_filed_unread`

Old text:

```
            if not one.ref:
```

New text:

```
            if False:
```

### `u144-b.B5_read_back_exact`

Read back: accept a made playlist holding rows the plan did not name, or out of order

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B5_read_back_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
        if missing or (one.created and not exact):
```

New text:

```
        if missing:
```

### `r1295.M17_skip_guard`

plan (existing guard, sample): a set INSPIRATION already holds is read and planned again

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M17_skip_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_already_under_inspiration_is_skipped_and_its_tracks_never_read`

Old text:

```
        if name in held:
```

New text:

```
        if False:
```

### `u144-b.B2_stale_digest`

Write guard: drop the digest comparison of the plan taken again on the write handle

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B2_stale_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale`

Old text:

```
    if now.digest() != approved.digest():
```

New text:

```
    if False:
```

### `r1295.M1_refused_row_fatal`

_read: every refused row raises again, so one untitled track leaves the whole set unread as on main

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M1_refused_row_fatal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_is_filed_unread_naming_each`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
            one = intake_cli.set_aside(row)
            if not one.ref:
```

New text:

```
            one = intake_cli.set_aside(row)
            if True:
```

### `u144-b.B4_convergence_latch`

Write: drop the INSPIRATION tree's convergence latch before the session

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B4_convergence_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_convergence_latch_refuses_the_write_before_anything_is_written`

Old text:

```
        convergence.assert_tree_writable(cfg, db, approved.tree_id, tree_registry.read(cfg))
```

New text:

```
        pass
```

### `u147-d.A2_retired_unnamed`

account_mirror.add_steps: a mirrored folder the library no longer holds is not listed

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A2_retired_unnamed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_library.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_folder_the_library_no_longer_holds_is_left_and_named`

Old text:

```
    for name in sorted(set(recorded) - held):
```

New text:

```
    for name in ():
```

### `u147-b.M8_move_new_only`

mirror.apply: move only a playlist made now, never one made earlier and left at the root

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M8_move_new_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`

Old text:

```
        if made or step.move:
```

New text:

```
        if made:
```

### `r1031.M21_run_id_unchecked`

mirror_frozen._path: name a file from any run identifier

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `r1031.json`, row `M21_run_id_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_run_identifier_that_cannot_name_a_file_is_not_frozen`

Old text:

```
    if not _RUN_ID.match(run_id):
```

New text:

```
    if False:
```

### `r1031.M7_remembered_not_counted`

Matcher._match: count no remembered miss, so the gate never says misses were reused

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M7_remembered_not_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered`

Old text:

```
            self.remembered += 1
```

New text:

```
            self.remembered += 0
```

### `r1031.M5_unread_miss_remembered`

Matcher._missed: remember a miss over a candidate that could not be read

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M5_unread_miss_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered`
  - `tests/test_organize_mirror_frozen.py::test_the_frozen_matches_answer_a_row_the_ledger_could_not_remember`

Old text:

```
        if UNREAD not in reason:
```

New text:

```
        if True:
```

### `u222.M15_moved_gone_step_silent`

moved: say nothing of a step the gate showed and this run did not plan

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M15_moved_gone_step_silent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            said.append(f"{then.title}, which the gate showed and this run did not plan")
```

New text:

```
            pass
```

### `u222-zeros.M18_label_no_folder`

_label: read no folder line, so a folder that moved is never named

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222-zeros.json`, row `M18_label_no_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`

Old text:

```
    for key in ("playlist", "folder"):
```

New text:

```
    for key in ("playlist",):
```

### `u222.M20_every_step_reworded`

_stale: reword the line said when nothing moved

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M20_every_step_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
            else "every step plans as the gate showed it"
```

New text:

```
            else "every step plans as its gate showed it"
```

### `u150.A7_landed_two_tracks`

landed_tracks: keep a row two records name two tracks for, so which track it is decides itself by record order

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A7_landed_two_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_intake_land_labels_native.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_landed_tracks_reads_every_native_landings_provider_tracks`

Old text:

```
    return {cid: next(iter(found)) for cid, found in named.items() if len(found) == 1}
```

New text:

```
    return {cid: sorted(found)[0] for cid, found in named.items()}
```

### `u150.M3_retire_in_writes`

FolderPlan.writes: leave the retirements out, so a folder whose only write is a removal plans nothing and never removes

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M3_retire_in_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_already_gone_from_the_account_is_still_forgotten`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`

Old text:

```
            or bool(self.retire)
        )
```

New text:

```
            or False
        )
```

### `u150.A1_inbox_retires`

account_mirror._inbox: read INBOX as an ordinary folder, so no batch that left it is ever removed

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A1_inbox_retires`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_library.py`, `tests/test_organize_mirror.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_inbox_folder_reads_each_batch_under_its_account_title_with_its_rows`

Old text:

```
        playlists=tuple(sources),
        retire=True,
```

New text:

```
        playlists=tuple(sources),
        retire=False,
```

### `u267.M12_inspiration_set_folder_write_guard`

set_cli._inspiration_folder: drop the refusal of a shared read handed to an opener asked to write

- File: `src/cratekit/export/set_common.py`
- Source: `u267.json`, row `M12_inspiration_set_folder_write_guard`
- Moved: the same text, now in src/cratekit/export/set_common.py, was in src/cratekit/export/set_cli.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 87 against a baseline of 87
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_inspiration_opener_refuses_to_write_through_a_shared_read`

Old text:

```
    if one_read is not None and not read_only:
```

New text:

```
    if False:
```

### `u143-a.R6_one_named_folder`

Label folder: take the first of several root folders of the label's name

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R6_one_named_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_debris_with_no_label_folder_or_two_of_them_is_left_with_why`

Old text:

```
        if len(named) == 1:
            return named[0], ""
```

New text:

```
        if named:
            return named[0], ""
```

### `u255.M12_add_never_retried`

add_to_playlist: no retry at all, so a 412 on a stale held tag fails the item

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M12_add_never_retried`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[412]`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[503]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
        added = self._call(doing, attempt)
```

New text:

```
        added = self._call(doing, attempt, retries=0)
```

### `u255.M13_add_retried_twice`

add_to_playlist: two retries, more than the policy allows a write

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M13_add_retried_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[412]`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_twice_fails_the_item_with_nothing_more_sent[503]`

Old text:

```
        added = self._call(doing, attempt)
```

New text:

```
        added = self._call(doing, attempt, retries=2)
```

### `u270.E4_row_of_a_recorded_track`

apply: never note the row of a track already recorded, so a prune cannot tell a row that left from a match that drifted

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E4_row_of_a_recorded_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_prune.py`, `tests/test_outbound_workers.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_re_export_names_the_rows_of_tracks_recorded_before_rows_were_kept`

Old text:

```
                noted[local] = remote
```

New text:

```
                pass
```

### `u270.C6_one_tracks_failure_is_its_own`

run_export_items: a plain exception planning one track fails the whole batch

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C6_one_tracks_failure_is_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_resume_of_a_half_failed_export_does_not_exit_ok`

Old text:

```
        except Exception as exc:  # noqa: BLE001 - this track's outcome
```

New text:

```
        except CratekitError as exc:  # noqa: BLE001 - this track's outcome
```

### `u220.A1_front_target`

order_tracks: move each track to the playlist's length instead of the front, the move whose landing depends on how the provider counts

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A1_front_target`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
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

### `r1308.M13_accept_tracks_only`

_removal_read_back: accept a reading whose tracks are after, whatever its count

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M13_accept_tracks_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`

Old text:

```
if tracks == counted == "after":
```

New text:

```
if tracks == "after":
```

### `r1308.M14_lag_by_or`

_removal_read_back: a lag needs only one half known, the other may be neither

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M14_lag_by_or`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
lagged = tracks is not None and counted is not None
```

New text:

```
lagged = tracks is not None or counted is not None
```

### `r1308.M20_message_swapped`

_removal_read_back: a lag says a wrong track may have come off

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M20_message_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
            if lagged
            else (
                f"the playlist {identifier} read back after a removal is not "
```

New text:

```
            if not lagged
            else (
                f"the playlist {identifier} read back after a removal is not "
```

### `r1032.A8_album_narrow_drops_all`

_on_album: when the album names none, answer the named list alone, empty

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A8_album_narrow_drops_all`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 11 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_none_of_the_tied_releases_still_takes_one`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
    return named or remotes
```

New text:

```
    return named
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

### `r356-a.A12_reason_outlives_its_match`

A reason is not cleared when the row is matched again, so a row that resolved still says it could not be

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A12_reason_outlives_its_match`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`

Old text:

```
        self._reasons.pop(key, None)

```

New text:

```
(empty)
```

### `r356-a.A2_unreadable_track_no_longer_stops_rule_one`

A lone agreeing track is chosen beside one nobody could read

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A2_unreadable_track_no_longer_stops_rule_one`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_release_that_cannot_be_read_stops_a_lone_agreeing_one_from_being_chosen`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_track_stops_the_album_from_choosing_the_lone_agreeing_one`

Old text:

```
        if len(agreeing) == 1 and not unreadable:
```

New text:

```
        if len(agreeing) == 1:
```

### `r572.A5_album_among_all`

Choose by album among every candidate, not only the agreeing ones

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r572.json`, row `A5_album_among_all`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`

Old text:

```
            remote for remote in agreeing if match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
            remote for remote in tracks if match.fold(_album_name(tracks[remote])) == wanted
```

### `r356-a.A7_artist_not_compared`

Agreement ignores the artist, so another act's record under the same title agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A7_artist_not_compared`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`
  - `tests/test_outbound_tidal_account.py::test_another_artist_under_the_same_title_does_not_agree`

Old text:

```
    if not _artist_agrees(row.artist, listed.artist, track):
        return False

```

New text:

```
(empty)
```

### `u226.M9_positions_no_lag_refusal`

_positions: a lagging window is not refused, its positions taken

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M9_positions_no_lag_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
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

### `u51-item-derivation.D3_empty_playlist`

THE ZERO ITEM RULE: let a playlist with no writable track queue

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D3_empty_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`

Old text:

```
    if not kept:
```

New text:

```
    if False:
```

### `r856-a.S1_tally_zero`

shell.unmatched_tally: report a tally when nothing went unmatched, so a clean sweep and a clean export carry the warning

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r856-a.json`, row `S1_tally_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_created_playlist_is_filed_in_exports_as_its_gate_showed`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_an_export_where_every_track_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_the_sweep_warning_counts_only_whole_numbers`
  - `tests/test_outbound_workers.py::test_the_unmatched_warning_reads_only_whole_counts[none-left-out]`

Old text:

```
    if not _whole(missed) or missed <= 0:
```

New text:

```
    if not _whole(missed) or missed < 0:
```

### `r229.C1_the_offer_is_not_digested`

The adoption never joins the confirm digest, so a confirmed update authorises a queue that creates

- File: `src/cratekit/export/cli.py`
- Source: `r229.json`, row `C1_the_offer_is_not_digested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_export_that_adopts_nothing_digests_as_it_always_did`

Old text:

```
    if adopts:
        covered["adopts"] = adopts
```

New text:

```
    if False:
        covered["adopts"] = adopts
```

### `r229.C2_the_flag_declines_nothing`

The new playlist flag is read and ignored, so a wrong offer cannot be declined

- File: `src/cratekit/export/cli.py`
- Source: `r229.json`, row `C2_the_flag_declines_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_confirmed_adoption_does_not_authorise_a_create`
  - `tests/test_outbound_workers.py::test_new_playlist_declines_the_adoption_and_creates`
  - `tests/test_outbound_workers.py::test_two_orphaned_records_that_could_each_be_it_adopt_neither`

Old text:

```
        found = found.without_offer()
```

New text:

```
        pass
```

### `u131.K4_ambiguous_kind`

kinds.decide: take the first of two root folders named as the kind rather than leave its playlists

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K4_ambiguous_kind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 2 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_an_export_whose_folder_a_name_cannot_decide_stays_at_the_root`
  - `tests/test_playlist_kinds.py::test_two_folders_named_mine_leave_the_authors_playlists_listed`

Old text:

```
    if len(named) > 1:
```

New text:

```
    if len(named) > 99:
```

### `u131.K7_kind_folders_kept`

ledger._load: drop the kind folder records on read, so the next write forgets them

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u131.json`, row `K7_kind_folders_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 5 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_marked_after_it_was_filed_in_mine_reaches_its_year`
  - `tests/test_playlist_kinds.py::test_a_renamed_playlist_and_a_renamed_folder_stay_where_they_are`
  - `tests/test_playlist_kinds.py::test_a_stale_kind_folder_record_is_replaced`
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`
  - `tests/test_playlist_kinds.py::test_the_kind_folders_record_survives_another_write`

Old text:

```
            for kind, value in kind_folders.items()
            if value.get("folder_id")
```

New text:

```
            for kind, value in kind_folders.items()
            if False
```

### `u261.O2_account_drops_the_app`

open_account: build the account without the held app client, so its ISRC lookups go to the account

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u261.json`, row `O2_account_drops_the_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_open_account_and_open_catalogue_hand_the_app_client_on`
  - `tests/test_provider_session_hold.py::test_the_app_client_is_held_with_the_session_and_asks_one_token`

Old text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=held.app)
```

New text:

```
    return TidalAccount(held.client, cfg=cfg, catalogue=None)
```

### `r836-e.P2b_mismatch_read_only_with_nothing_gone`

prune.plan_label: a release credited elsewhere is read and judged while a confirmed release is gone, so a track the gone one carries can leave. P2 measured the same guard's second copy in the leaving rule at zero; that copy was removed as redundant and this is the one left

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-e.json`, row `P2b_mismatch_read_only_with_nothing_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_release_the_provider_no_longer_has_stops_the_unconfirmed_judgement`

Old text:

```
    if judged:
        unread += sorted(set(catalogue.mismatched) - set(catalogue.by_release))
```

New text:

```
    unread += sorted(set(catalogue.mismatched) - set(catalogue.by_release))
```

### `r836-f.P9_row_in_playlist_keeps_its_track`

prune.plan_export: a track whose row is still in the playlist leaves when today's match of that row failed

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-f.json`, row `P9_row_in_playlist_keeps_its_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 3 (killed)
- Killed:
  - `tests/test_prune.py::test_a_match_that_moved_never_takes_off_a_track_recorded_by_its_row`
  - `tests/test_prune.py::test_a_row_the_export_names_and_does_not_carry_keeps_its_track`
  - `tests/test_prune.py::test_a_row_whose_match_failed_today_does_not_stop_a_track_recorded_by_its_row`

Old text:

```
    staying = matched_now | {one for row, one in record.rows.items() if row in rows_now}
```

New text:

```
    staying = matched_now
```

### `r1255.R5_organize_rotation_warns`

organize _rotation: drop the shared warning, so crate organize ages a batch unsaid

- File: `src/cratekit/organize/rekordbox.py`
- Source: `r1255.json`, row `R5_organize_rotation_warns`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
    step.warnings.extend(rotate_cli.records_warnings(plan))
```

New text:

```
    pass
```

### `u216.M23_read_drops_held`

_folders: what a folder held is never read back

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M23_read_drops_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_playlist_no_pair_names_still_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_folder_record_keeps_what_it_held_through_another_write`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_a_created_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_made_in_the_adopted_folder_after_the_sync_comes_in`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                None if held is None else frozenset(held),
            )
```

New text:

```
                None,
            )
```

### `u216.M25_dated_no_time`

folder_playlists_dated: every playlist reads as made at no known time

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u216.json`, row `M25_dated_no_time`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_adopted.py`, `tests/test_outbound_tidal_account.py`, `tests/test_adapter_listing.py`
- Collected: 229 against a baseline of 229
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_the_dated_folder_read_gives_each_playlists_creation_time_from_the_same_pages`

Old text:

```
                made if isinstance(made, datetime) else None,
```

New text:

```
                None,
```

### `u221.R12_hold_not_written`

Pair.to_json: write no hold, so the next read finds none and a twin made since U221 falls to the time rule

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R12_hold_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 153 against a baseline of 153
- Kills: 18 (killed)
- Killed:
  - `tests/test_sync_twins.py::test_a_backfilled_pair_merges_both_ways_and_queues_the_added_track_once`
  - `tests/test_sync_twins_hold.py::test_a_held_track_whose_linked_row_left_the_library_is_still_counted_and_released`
  - `tests/test_sync_twins_hold.py::test_a_landing_twin_records_an_empty_hold`
  - `tests/test_sync_twins_hold.py::test_a_name_that_is_no_twin_is_refused_and_nothing_is_planned`
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_added_later_on_the_account_is_queued_and_the_held_stay_held`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_a_twin_with_three_missing_tracks_queues_none_and_names_three_on_hold`
  - `tests/test_sync_twins_hold.py::test_an_abort_lets_nothing_go`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`
  - `tests/test_sync_twins_hold.py::test_release_needs_names_or_all_and_not_both[args0]`
  - ... and 3 more, see the JSON sidecar

Old text:

```
        if self.on_hold is not None:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
```

New text:

```
        if False:
            record["on_hold"] = dict(sorted(self.on_hold.items()))
```

### `u231.M4_resend_with_the_stale_tag`

adapter order: a 412's move is sent again without opening the playlist for its current tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M4_resend_with_the_stale_tag`
- Moved: the reopen after a 412 is still in order_tracks in tidal_account.py, but the retry loop now breaks on success instead of ending each 412 with continue, so the anchor is the pause line and the reopen; same reopen removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
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
                    self._paused(note, _pause(stale))
                    playlist = self._playlist(identifier)

```

New text:

```
                    self._paused(note, _pause(stale))

```

### `r837-a.A1_no_record_creates`

sets.plan_set: a set already recorded is planned as a create, so a second run makes a second playlist

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A1_no_record_creates`
- Moved: the no record guard is still in sets.plan_set, its SetPlan now built with positional arguments instead of keywords; same condition forced true
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`

Old text:

```
    if recorded is None:
        return SetPlan(name, year, CREATE, tuple(rows), add=wanted)

```

New text:

```
    if True:
        return SetPlan(name, year, CREATE, tuple(rows), add=wanted)

```

### `u140.B1_ledger_folds_into_a_twin`

rename_set_playlist drops its refusal when the new name already holds another playlist

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u140.json`, row `B1_ledger_folds_into_a_twin`
- Moved: rename_set_playlist moved from ledger.py to ledger_reserve.py and raises through the shared _refused instead of _unusable with a path; same refusal condition reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_ledger_refuses_to_fold_a_rename_into_another_playlist`

Old text:

```
        if held:
            raise _refused(

```

New text:

```
        if False:
            raise _refused(

```

### `u236.M19_ledger_normalizer_drops`

ledger load: drop every folder's placements on read and write

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M19_ledger_normalizer_drops`
- Moved: the placements kept on load are still in ledger.py, but the mirrored folder normalizer was pulled out of _load into _mirror_document, so the lines sit eight spaces shallower; same placements dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 8 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_survives_the_ledgers_own_read_and_write`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            {"placed": placed}
            if (placed := _placements(value.get("placed")))
            else {}

```

New text:

```
            {}

```

### `u236.M21_frozen_not_overlaid`

overlay: read the ledger's placements now beside the gate's snapshot

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M21_frozen_not_overlaid`
- Moved: the overlay of the gate's placements is still in mirror_frozen.overlay, the replace call now written on one line instead of two; same snapshot read dropped for the ledger's own
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_frozen_folder_with_no_placements_reads_none_and_one_unread_reads_the_ledgers`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
placed=frozen.placed.get(name, folder.placed))
```

New text:

```
placed=folder.placed)
```

### `u147-c.M16_folder_made_twice`

ledger.reserve_mirror_folder: a recorded folder is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u147-c.json`, row `M16_folder_made_twice`
- Moved: reserve_mirror_folder moved from ledger.py to ledger_reserve.py and its reuse of a recorded folder is now the shared _reserve_folder, used by the label, set and mirror folders alike; same reuse guard removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        recorded = entry(document)
        if recorded and recorded != stale:
            return recorded, False

```

New text:

```
        recorded = entry(document)

```

### `r1031.M3_signature_keys_a_coded_row`

Matcher.under: key every miss on its file signature, so a coded row is asked again on any file touch

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M3_signature_keys_a_coded_row`
- Moved: Matcher.under in mirror.py now returns its key tuple on one line instead of one field a line; same signature made to key a coded row
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_coded_rows_miss_is_kept_whatever_its_file_does`

Old text:

```
"" if row.isrc else self._signature(row))
```

New text:

```
self._signature(row))
```

### `u150.M7_refusal_scope`

mirror.apply: keep a playlist removal refused at run scope instead of raising, so a removal whose read back differs reads as kept

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M7_refusal_scope`
- Moved: the playlist removal refusal in mirror.apply now goes through the helper _kept, shared with the track removals, instead of its own inline check; same scope test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_removal_whose_read_back_differs_is_raised_never_kept`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`

Old text:

```
    if exc.cause.reason != "outbound-remove-refused" or exc.cause.scope != Scope.SOURCE:

```

New text:

```
    if exc.cause.reason != "outbound-remove-refused":

```

### `u255.M1_playlist_keeps_the_hold`

_playlist: drop nothing, so a member that opens and writes through its own object leaves the held one stale

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M1_playlist_keeps_the_hold`
- Moved: the hold dropped first is still in tidal_account._playlist, now followed by a doing string the open shares instead of the open call itself; same drop removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
        self._opened.pop(playlist_id, None)
        doing = f"open the playlist {playlist_id}"

```

New text:

```
        doing = f"open the playlist {playlist_id}"

```

### `r572.S1_album_not_read`

file_identity drops the album it read

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `S1_album_not_read`
- Moved: source.file_identity still reads the album, its FileIdentity now built on one line with the ISRC positional; same album dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`
  - `tests/test_outbound_workers.py::test_the_files_album_is_read_beside_its_isrc_in_one_read`

Old text:

```
album=str(read["album"] or "").strip())
```

New text:

```
album="")
```

### `r834.M5_a_create_is_never_retried`

create_playlist: retry the create like a write, so a create that reached the provider and timed out is retried into a second playlist (an existing guard, sampled)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M5_a_create_is_never_retried`
- Moved: create_playlist in tidal_account.py now makes its call on one line with a shared doing string; same retries=0 removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_create_is_never_retried_into_a_second_playlist`

Old text:

```
lambda: self._session.user.create_playlist(name, ""), retries=0)
```

New text:

```
lambda: self._session.user.create_playlist(name, ""))
```

### `sitting4.G3_builders_ignore_the_prefix_map`

The builders hand the resolver an empty map, so a renamed drive resolves no row (R-372)

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G3_builders_ignore_the_prefix_map`
- Moved: source.prefix_rules builds the same list in one comprehension line, its loop name shortened to prefix; same map replaced by an empty one
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
    return [locations.PrefixRule(prefix, target) for prefix, target in cfg.resolved_prefix_map()]

```

New text:

```
    return []

```

### `sitting4.G10_absent_root_reads_as_untagged`

The mount guard is removed, so an unplugged volume reads as a library of untagged files and the sweep succeeds unmatched

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G10_absent_root_reads_as_untagged`
- Moved: the mount guard is still in source.py, its refusal message rewrapped onto longer lines so the old anchor's message line no longer matches; same condition forced true
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_absent_library_root_refuses_rather_than_reading_every_row_untagged`

Old text:

```
    root = Path(cfg.library.root)
    if root.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",

```

New text:

```
    root = Path(cfg.library.root)
    if True:
        return
    raise refuse(
        "library-volume-unmounted",

```

### `r836-a.A4_no_video_declared`

tidal_account._positions: a playlist holding a video is read by track position, which the item removal does not use

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A4_no_video_declared`
- Moved: the video check in tidal_account._positions is now one if line instead of a parenthesised condition a clause a line; same videos clause removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 501 against a baseline of 501
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_holding_a_video_is_refused_with_nothing_sent`

Old text:

```
declared != len(members) or not _count(videos) or videos != 0:
```

New text:

```
declared != len(members) or not _count(videos):
```

### `u129-author.A12_archive_backfill_swallows_all`

Catch Exception around plan_archive so a credential refusal becomes a warning

- File: `src/cratekit/export/set_cli.py`
- Source: `u129-author.json`, row `A12_archive_backfill_swallows_all`
- Moved: the backfill's soft skip is still in set_cli._export_archive_backfill, its warning now built by the shared warning helper from a said string; same catch widened to Exception
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_export_archive_backfill_refuses_a_credential_error`

Old text:

```
        except CratekitError as exc:
            # Soft skip per set, as a landing's _plan_set_archive does. A
            # CredentialError (not a CratekitError) still refuses the verb.
            said = f"{name}: {exc.cause.message}"
            warnings.append(warning("export-archive-backfill-refused", said))
            continue

```

New text:

```
        except Exception as exc:
            said = f"{name}: {exc}"
            warnings.append(warning("export-archive-backfill-refused", said))
            continue

```

