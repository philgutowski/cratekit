# Mutation table: u309-replay-after-e

Measured by `scripts/mutate.py` on 2026-11-22 23:08 UTC, branch `HEAD` at `274eefed`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22913 collected. pytest invocations for this batch: 159.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 23:08 UTC for commit `274eefed7087`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 56, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22913 against 22913. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r229.L10_a_name_matches_by_bare_suffix` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L11_an_empty_name_matches` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L12_the_first_of_several_is_adopted` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r1411.A3_added_tracks_asked_of_the_agreed_order` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 7 | killed |
| `r1411.A5_duplicates_counted_twice` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 1 | killed |
| `r1411.E1_expect_compared_as_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 1 | killed |
| `u234.O19_reading_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 23 file(s) | 1765 | 14 | killed |
| `u142.S5_create_under_the_year` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 231 | 6 | killed |
| `r879-b.S5_codes_from_every_version` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r572.Z1_set_drop_album` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 63 | 1 | killed |
| `r837-a.A4_nothing_matched_writes_nothing` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 63 | 3 | killed |
| `u142.S8_gate_stale_said_without_a_write` | `src/cratekit/export/set_archive.py` | user | 1 file(s) | 63 | 1 | killed |
| `r1017.M8_first_older_name_only` | `src/cratekit/modules/outbound/sets.py` | user | 4 file(s) | 195 | 2 | killed |
| `u140.B10_queued_day_name_dropped` | `src/cratekit/export/set_common.py` | user | 1 file(s) | 29 | 2 | killed |
| `u140.A2_new_name_record_ignored` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 6 | killed |
| `u270.C1_export_names_its_batch_form` | `src/cratekit/export/cli.py` | user | 4 file(s) | 290 | 7 | killed |
| `u206.M17_account_hit_ignored` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 9 file(s) | 1137 | 13 | killed |
| `u117-operator.D14_organize_call` | `src/cratekit/organize/account.py` | user | 2 file(s) | 117 | 3 | killed |
| `u123.L3_malformed_entry_dropped` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 3 file(s) | 108 | 1 | killed |
| `u143-c.A4_empty_videos` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 446 | 2 | killed |
| `r835-a.F12_refused_tracks_recorded` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `u243.L9_prune_ignores_tombstones` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 78 | 6 | killed |
| `u230.M6_no_landing_guard` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 2 | killed |
| `u230.M4_other_bases_ignored` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 5 | killed |
| `u230.M5_any_title` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 1 | killed |
| `u227.R10_one_approval` | `src/cratekit/organize/mirror_downloads.py` | user | 7 file(s) | 184 | 1 | killed |
| `u236.M2_unfavourite_counts_ours` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 7 | killed |
| `u236.M22_frozen_not_written` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 223 | 1 | killed |
| `u236.M14_write_wrong_time` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 223 | 6 | killed |
| `u236.M10_reader_no_time_check` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 223 | 3 | killed |
| `u201.E4_own_genre_no_edit` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 1 | killed |
| `u201.E6_short_unread` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 3 | killed |
| `u201.E3_own_genre_derived_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 2 | killed |
| `u204.P11_inbox_hold_per_batch` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 222 | 4 | killed |
| `u204.P12_favorites_stay` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u143-b.F2_empty_unclaimed` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 164 | 1 | killed |
| `u142.S16_pass_is_not_the_set` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.R3_bridge_tree_planned` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.A2_pending_loses` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.C5_unexpected_failure_stops` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.R8_inbox_mine_unlisted` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 2 | killed |
| `u116.M9_yours_lists_moved` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 3 | killed |
| `u137.R4_rotation_shown_unselected` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 1 | killed |
| `r1295.M12_setrow_keeps_no_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-a.A6_set_name_spelling` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M10_unread_off_misses` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 4 | killed |
| `u144-a.A4_sets_folder_name` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `r1295.M11_again_drops_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-a.A5_recorded_folder` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u147-d.A3_twin_folders_read` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 37 | 1 | killed |
| `u147-b.M13_links_unrecorded` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 4 | killed |
| `r1031.M10_filter_against_raw_links` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M8_misses_not_a_map_read` | `src/cratekit/modules/outbound/ledger.py` | user | 2 file(s) | 71 | 1 | killed |
| `r1031.M9_malformed_miss_kept` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `u222.M21_cli_message_unchanged` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 251 | 2 | killed |
| `u222.M1_overlay_not_read` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 251 | 3 | killed |
| `u222.M9_text_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 251 | 1 | killed |
| `u222.M17_refused_named_by_every_line` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 1 | killed |
| `u150.M1_retire_flag` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 7 | killed |
| `u150.Z1_frozen_retire` | `src/cratekit/organize/mirror_frozen.py` | user | 2 file(s) | 69 | 2 | killed |
| `u267.M2_applying_run_shares` | `src/cratekit/organize/cli.py` | user | 2 file(s) | 109 | 1 | killed |
| `u242.M24_root_reads_the_title_alone` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u143-e.P3_kept_problems` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u255.S4_added_not_remembered` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 5 | killed |
| `u270.L2_row_only_for_a_recorded_track` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 4 file(s) | 257 | 1 | killed |
| `u270.C5_unfiled_said_once` | `src/cratekit/export/cli.py` | user | 3 file(s) | 159 | 2 | killed |
| `u220.A10_wrong_status` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 10 | killed |
| `u220.A12_no_memory_guard` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 2 | killed |
| `r1308.M9_videos_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 2 | killed |
| `r1308.M12_count_after_le` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 1 | killed |
| `r1032.A11_empty_album_narrows` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 1 | killed |
| `r1032.A7_lowest_by_characters` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 1 | killed |
| `r227.A5_half_a_pair` | `src/cratekit/modules/outbound/source.py` | maintainer | 4 file(s) | 371 | 1 | killed |
| `u208.M20_adapter_stale_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 1 | killed |
| `r358-round-2.A5_absent_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A10_provider_title_read_one_way_only` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A14_no_joiner_words` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `u226.M13_removal_window_wrong` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 2 | killed |
| `u51-item-derivation.D5_repeated_deduped` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `u51-item-derivation.D4_dangling_reported` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `r227.S3_utc_date_in_the_sentence` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `r227.S7_floored_age_in_the_sentence` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `u131.K8_export_files_once` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 234 | 1 | killed |
| `r1305.A1_account_name_on_any_link` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 197 | 1 | killed |
| `u261.A2_account_reuse_ignores_the_hold` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 143 | 3 | killed |
| `r836-b.L3_created_false_when_adopted` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 5 file(s) | 404 | 3 | killed |
| `r836-c.L7_row_only_for_a_written_track` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P7_unrowed_with_unmatched_left_alone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `u174.O6_native_refusal_is_a_step` | `src/cratekit/organize/account.py` | user | 2 file(s) | 164 | 2 | killed |
| `u221.R13_hold_not_read` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 153 | 18 | killed |
| `r356-b.B6_export_plan_drops_the_reason` | `src/cratekit/modules/outbound/export.py` | user | 1 file(s) | 64 | 1 | killed |
| `u123.T2_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 38 | 2 | killed |
| `u204.P6_filed_no_month` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 1 file(s) | 42 | 1 | killed |
| `u147-c.M17_playlist_made_twice` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 34 | 5 | killed |
| `r1289.M17_mirror_listing_refusal` | `src/cratekit/organize/mirror_downloads.py` | user | 1 file(s) | 37 | 1 | killed |
| `u150.M8_refusal_kept` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 32 | 1 | killed |
| `u255.C4_held_before_read_and_playlist_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 24 | 2 | killed |
| `r572.L1_local_track_drop_album` | `src/cratekit/modules/outbound/source.py` | user | 1 file(s) | 123 | 1 | killed |
| `r358.A4_false_answer` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r850-a.E2_unmatched_count` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 2 | killed |
| `r850-a.E1_written_count` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 5 | killed |
| `u131.K6_adopt_not_made` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 1 file(s) | 14 | 1 | killed |

## Row definitions

### `r229.L10_a_name_matches_by_bare_suffix`

The name rule drops the separator, so Big Crate is recognised as Crate

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L10_a_name_matches_by_bare_suffix`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_written_before_tracks_were_kept_is_recognised_by_name[2024/Big Crate-Crate-False]`

Old text:

```
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))
```

New text:

```
    return bool(name) and (recorded_key == name or recorded_key.endswith(name))
```

### `r229.L11_an_empty_name_matches`

The empty name guard is removed, so a nameless playlist matches any key ending in the separator

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L11_an_empty_name_matches`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_written_before_tracks_were_kept_is_recognised_by_name[2024/--False]`

Old text:

```
    return bool(name) and (recorded_key == name or recorded_key.endswith("/" + name))
```

New text:

```
    return recorded_key == name or recorded_key.endswith("/" + name)
```

### `r229.L12_the_first_of_several_is_adopted`

Two candidates are settled by taking the first rather than reported and left

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L12_the_first_of_several_is_adopted`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_two_candidates_are_both_named_and_neither_is_adopted`
  - `tests/test_outbound_workers.py::test_two_orphaned_records_that_could_each_be_it_adopt_neither`

Old text:

```
    if len(found) != 1:
        return Recognition(crate=len(wanted), candidates=candidates)
```

New text:

```
    if not found:
        return Recognition(crate=len(wanted), candidates=candidates)
```

### `r1411.A3_added_tracks_asked_of_the_agreed_order`

the agreed order check reads every track of the reading, so a track this write added refuses the finish

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `A3_added_tracks_asked_of_the_agreed_order`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
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
- Collected: 1305 against a baseline of 1305
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
- Collected: 1305 against a baseline of 1305
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

### `u234.O19_reading_not_written`

the pair's document never writes the reading after the stop, so a later sync never finds it

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u234.json`, row `O19_reading_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_cli_contract.py`, `tests/test_intake_land_twins.py`, `tests/test_outbound_order.py`, `tests/test_process_scan.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_twins.py`, `tests/test_sync_twins_hold.py`
- Collected: 1765 against a baseline of 1765
- Kills: 14 (killed)
- Killed:
  - `tests/test_sync_pair_settle.py::test_a_pending_pair_the_person_reordered_after_a_sync_read_it_is_merged_as_their_change`
  - `tests/test_sync_pair_settle.py::test_a_reorder_settled_readings_show_keeps_the_unread_track_where_the_person_put_it`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_a_readable_track_beside_an_unread_one_still_leads`
  - `tests/test_sync_pair_settle.py::test_a_settled_move_of_the_unread_track_alone_still_finishes_the_stopped_write`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_part_way_is_kept_where_it_was_put`
  - `tests/test_sync_pair_settle.py::test_of_two_unread_tracks_only_the_one_the_person_moved_keeps_its_place`
  - `tests/test_sync_pair_settle.py::test_two_unread_tracks_dragged_together_both_keep_the_place_the_person_gave_them`
  - `tests/test_sync_pair_stopped.py::test_a_reading_after_a_stop_round_trips_and_goes_when_the_snapshot_moves`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_reorder_seen_changing_between_two_syncs_after_the_stop_leads`
  - `tests/test_sync_pair_stopped_order.py::test_an_order_held_as_the_one_after_waits_afresh_once_the_settled_order_is_read_between`

Old text:

```
        if self.stop_seen is not None:
            record["stop_seen"] = self.stop_seen.to_json()
```

New text:

```
        if False:
            record["stop_seen"] = self.stop_seen.to_json()
```

### `u142.S5_create_under_the_year`

apply_archive: create the folder under the plain year, so a set's folder is made with the filing's name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S5_create_under_the_year`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 231 against a baseline of 231
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

### `r879-b.S5_codes_from_every_version`

file_isrc: read the code of every held version, not only the matched files

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S5_codes_from_every_version`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_another_versions_isrc_is_not_the_rows`

Old text:

```
            if str(held.path) in paths and held.isrc
```

New text:

```
            if held.isrc
```

### `r572.Z1_set_drop_album`

export set stops passing the album to match_track

- File: `src/cratekit/export/set_match.py`
- Source: `r572.json`, row `Z1_set_drop_album`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_held_files_album_tag_is_handed_to_the_account_with_its_isrc`

Old text:

```
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True, album=album
                    )
```

New text:

```
                    remote, said = _isrc_match(
                        account, identity, one, code, agree=True
                    )
```

### `r837-a.A4_nothing_matched_writes_nothing`

SetPlan.writes: a plan with nothing to add still writes, so a set with nothing matched makes an empty playlist

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A4_nothing_matched_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_with_nothing_matched_makes_no_empty_playlist`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`

Old text:

```
        return bool(self.add)
```

New text:

```
        return True
```

### `u142.S8_gate_stale_said_without_a_write`

export archive gate: say a stale record is replaced even when nothing is written

- File: `src/cratekit/export/set_archive.py`
- Source: `u142.json`, row `S8_gate_stale_said_without_a_write`
- Moved: the same text, now in src/cratekit/export/set_archive.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 63 against a baseline of 63
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
    if planned.stale_folder and planned.writes:
```

New text:

```
    if planned.stale_folder:
```

### `r1017.M8_first_older_name_only`

Plan: stop at the first older name holding a record, the pre review behaviour

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M8_first_older_name_only`
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
        if found is not None and all(found.remote_id != one.remote_id for one in older):
```

New text:

```
        if found is not None and not older:
```

### `u140.B10_queued_day_name_dropped`

_names_for_job stops giving the queued day's form, which is the name the Signal set was exported under

- File: `src/cratekit/export/set_common.py`
- Source: `u140.json`, row `B10_queued_day_name_dropped`
- Moved: the same text, now in src/cratekit/export/set_common.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`

Old text:

```
    if landing is not None and landing != posted:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))

```

New text:

```
    if False:
        found.append(set_name(set_playlist.playlist_name(words, on=landing)))

```

### `u140.A2_new_name_record_ignored`

plan_rename does not look under the new name, so a rerun after the rekey finds nothing recorded

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A2_new_name_record_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 6 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`

Old text:

```
    recorded_to = ledger.set_playlist(cfg, to) if to else None

```

New text:

```
    recorded_to = None

```

### `u270.C1_export_names_its_batch_form`

export cli: the per item worker names no batch form

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C1_export_names_its_batch_form`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`, `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 290 against a baseline of 290
- Kills: 7 (killed)
- Killed:
  - `tests/test_handlers.py::test_the_export_worker_names_its_batch_form_at_the_providers_add_limit`
  - `tests/test_outbound_export_batches.py::test_a_job_of_two_hundred_and_fifty_tracks_makes_fifteen_requests`
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_refused_request_fails_every_item_it_carried_and_the_resume_adds_each_once`

Old text:

```
handle.batched = (handle_batch, BATCH)  # type: ignore[attr-defined]
```

New text:

```
handle.unbatched = (handle_batch, BATCH)  # type: ignore[attr-defined]
```

### `u206.M17_account_hit_ignored`

TidalAccount._isrc_tracks: never use a remembered answer

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u206.json`, row `M17_account_hit_ignored`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1137 against a baseline of 1137
- Kills: 13 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_isrc_cache.py::test_a_choice_among_several_releases_is_made_from_a_remembered_answer_with_no_call`
  - `tests/test_isrc_cache.py::test_a_copy_run_redirecting_installation_state_shares_answers_through_the_override`
  - `tests/test_isrc_cache.py::test_a_found_answer_is_asked_again_after_the_configured_days`
  - `tests/test_isrc_cache.py::test_a_found_answer_lives_thirty_days_unless_set`
  - `tests/test_isrc_cache.py::test_a_not_found_is_kept_and_asked_again_after_seven_days`
  - `tests/test_isrc_cache.py::test_a_second_account_over_a_fresh_client_asks_nothing_for_an_answered_isrc`
  - `tests/test_isrc_cache.py::test_a_tie_remembered_is_still_refused_with_its_reason`
  - `tests/test_isrc_cache.py::test_an_expired_answer_is_replaced_by_the_new_one`
  - `tests/test_isrc_cache.py::test_an_outage_then_a_not_found_on_the_retry_keeps_the_not_found`
  - `tests/test_isrc_cache.py::test_the_catalogue_and_the_account_share_one_answer`
  - `tests/test_isrc_cache.py::test_the_process_counts_say_what_the_cache_settled_and_what_was_asked`
  - `tests/test_sync_pair.py::test_a_live_plan_after_its_rehearsal_asks_the_provider_no_isrc_again[kept]`

Old text:

```
        if held is not None:
            return held if held else _ABSENT
        # What the LAST attempt said
```

New text:

```
        if False:
            return held if held else _ABSENT
        # What the LAST attempt said
```

### `u117-operator.D14_organize_call`

organize: drop the one call line, so organize never plans a dated playlist

- File: `src/cratekit/organize/account.py`
- Source: `u117-operator.json`, row `D14_organize_call`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_dated.py::test_an_unreadable_record_refuses_the_dated_step_alone`
  - `tests/test_label_dated.py::test_organize_plans_the_dated_playlist_after_the_label_folder_and_applies_in_order`
  - `tests/test_label_dated.py::test_organize_with_nothing_taken_plans_nothing`

Old text:

```
        dated.add_step(cfg, area, entry, planned, remote_of)

```

New text:

```
        pass

```

### `u123.L3_malformed_entry_dropped`

Keep a dated entry with an empty name or identifier

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L3_malformed_entry_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 108 against a baseline of 108
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for`

Old text:

```
            {"dated": {str(name): str(pid) for name, pid in dated.items() if name and pid}}
```

New text:

```
            {"dated": {str(name): str(pid) for name, pid in dated.items()}}
```

### `u143-c.A4_empty_videos`

Adapter: an empty playlist need not declare zero videos

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A4_empty_videos`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 446 against a baseline of 446
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served3-empty]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served4-empty]`

Old text:

```
            served = _count(tracks) and _count(videos) and tracks == 0 and videos == 0
```

New text:

```
            served = _count(tracks) and tracks == 0
```

### `r835-a.F12_refused_tracks_recorded`

folders.apply: a track the provider would not add is not recorded as refused, so every later plan asks for it again

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F12_refused_tracks_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_add_is_recorded_and_not_asked_again`

Old text:

```
            refused = [one for one in chunk if one not in held]
```

New text:

```
            refused = []
```

### `u243.L9_prune_ignores_tombstones`

prune.plan_label: a tombstoned track leaves only when a held or mismatched release says so

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `u243.json`, row `L9_prune_ignores_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`
- Collected: 78 against a baseline of 78
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_removed_single_is_taken_off_though_its_release_is_suppressed`
  - `tests/test_label_tombstoned.py::test_a_removed_track_stays_off_after_a_full_build`
  - `tests/test_label_tombstoned.py::test_a_tombstone_matches_the_version_and_every_billed_artist`
  - `tests/test_label_tombstoned.py::test_a_tombstoned_track_on_a_year_playlist_is_pruned`
  - `tests/test_label_tombstoned.py::test_a_year_playlist_the_prune_empties_is_named_and_kept`
  - `tests/test_label_tombstoned.py::test_hearing_a_dated_playlist_never_puts_a_removed_track_back`

Old text:

```
            if one in taken_away
            or (one not in staying(year) and (one in on_held or one in on_other))
```

New text:

```
            if (one not in staying(year) and (one in on_held or one in on_other))
```

### `u230.M6_no_landing_guard`

_as_queued: lift whatever rekordbox holds, so a band a person chose after the landing is beaten

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M6_no_landing_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_band_a_person_chose_before_any_carry_is_not_lifted_over`
  - `tests/test_mirror_edits_u230.py::test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over`

Old text:

```
    if not _filed_by_landing(there, places):
        return frozenset()
```

New text:

```
    if False:
        return frozenset()
```

### `u230.M4_other_bases_ignored`

landed check: no snapshot counts, so another playlist's word on the row is lost

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M4_other_bases_ignored`
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
bool(held_by.get(track, frozenset()) - lifted)
```

New text:

```
False
```

### `u230.M5_any_title`

_as_queued: lift every playlist holding the track, not only the queuing one

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M5_any_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`

Old text:

```
        if one.place.title in titles

```

New text:

```
        if True

```

### `u227.R10_one_approval`

filed: every entry since the queue is the landing's, whatever its approval (round one's F1)

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R10_one_approval`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_refiling_through_adoption_after_the_landing_is_not_the_landings`

Old text:

```
            if entry.digest != first.digest:
                continue
```

New text:

```
            if False:
                continue
```

### `u236.M2_unfavourite_counts_ours`

decide favorites: count a placed month as rekordbox's addition against an UNFAVOURITE

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M2_unfavourite_counts_ours`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 7 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_an_unfavourite_over_the_month_the_library_placed_is_carried`
  - `tests/test_mirror_edits_u236.py::test_the_same_over_a_placed_month_never_agreed`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                if (there_s and not was_s) or (there_m - was_m - ours):
```

New text:

```
                if (there_s and not was_s) or (there_m - was_m):
```

### `u236.M22_frozen_not_written`

freeze: freeze no placements

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M22_frozen_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
            name: {title: dict(sorted(tracks.items())) for title, tracks in sorted(folder.placed.items())}
```

New text:

```
            name: {}
```

### `u236.M14_write_wrong_time`

write: record a time no membership carries

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M14_write_wrong_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
            done.months.append((one.content_id, one.month, at))
```

New text:

```
            done.months.append((one.content_id, one.month, at + "x"))
```

### `u236.M10_reader_no_time_check`

read edits: hand the rule every recorded placement, whatever membership holds it (round one, finding 2)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M10_reader_no_time_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_membership_a_person_took_off_and_put_back_by_hand_is_theirs`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_deleted_and_made_again_by_hand_is_a_persons_addition[False]`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_deleted_and_made_again_by_hand_is_a_persons_addition[True]`

Old text:

```
                remote for remote, at in recorded_placed.items() if at and added.get(remote) == at
```

New text:

```
                remote for remote, at in recorded_placed.items() if at
```

### `u201.E4_own_genre_no_edit`

_intent: a track added to its own genre's with vox while keeping its band reads as an edit

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E4_own_genre_no_edit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_added_to_its_own_genres_with_vox_is_no_edit`

Old text:

```
    if not removed and folders[0] in {place.folder for place in now}:
```

New text:

```
    if False:
```

### `u201.E6_short_unread`

decide: a short listing marks nothing unread, so a counted, unlisted track reads as taken off

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E6_short_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_short_favorites_listing_holds_what_it_left_out`
  - `tests/test_mirror_edits.py::test_a_short_listing_carries_no_edit_and_holds_what_it_read_differently`
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`

Old text:

```
            unread |= one.agreed - one.account
```

New text:

```
            unread |= set()
```

### `u201.E3_own_genre_derived_held`

_intent: a track taken off its band and left in its own genre's with vox is decided as a genre change

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E3_own_genre_derived_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_taken_off_its_band_and_put_in_its_own_genres_with_vox_is_held`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`

Old text:

```
    if removed and not now and folders[0] in {place.folder for place in removed}:
```

New text:

```
    if False:
```

### `u204.P11_inbox_hold_per_batch`

_holds: an INBOX edit holds every batch rather than its own

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P11_inbox_hold_per_batch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_inbox_edit_holds_its_own_batch_and_no_other`
  - `tests/test_mirror_edits.py::test_an_inbox_track_put_in_joins_and_one_taken_off_leaves`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_an_inbox_batch_joins_it_and_one_taken_off_leaves_it`
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_inbox_or_favorites_that_the_library_lacks_is_queued`

Old text:

```
            key = one.to.title if one.tree == INBOX and one.to is not None else one.tree
```

New text:

```
            key = one.tree
```

### `u204.P12_favorites_stay`

_holds: a Favorites edit keeps no snapshot word on a playlist the plan finds level

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P12_favorites_stay`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favorites_edit_planned_and_not_applied_is_taken_whole_by_the_next_run`

Old text:

```
        stay = frozenset(mine) if one.place.tree == FAVORITES else frozenset()
```

New text:

```
        stay = frozenset()
```

### `u143-b.F2_empty_unclaimed`

Filing: an empty playlist a ledger claims is read as empty too

- File: `src/cratekit/organize/filing.py`
- Source: `u143-b.json`, row `F2_empty_unclaimed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_playlist_kinds.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_an_empty_playlist_the_product_made_or_a_placeholder_is_never_removed`

Old text:

```
        empty = not claimed and one.tracks == 0
```

New text:

```
        empty = one.tracks == 0
```

### `u142.S16_pass_is_not_the_set`

organize set step: record an INSPIRATION proven mark under another pass, so sync unmark with the set's name finds nothing

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S16_pass_is_not_the_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`

Old text:

```
                else set_cli.plan_archive_named(cfg, name, pass_name=name)
```

New text:

```
                else set_cli.plan_archive_named(cfg, name, pass_name="organize")
```

### `u112.R3_bridge_tree_planned`

Adoption over a routing tree still on the bridge is planned rather than refused

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R3_bridge_tree_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_area_with_nothing_to_do_still_asks`

Old text:

```
    if not registry.is_database_native(declared.tree.id):
```

New text:

```
    if False:
```

### `u112.A2_pending_loses`

A pending intake file ranks below a retired one of the same pass

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A2_pending_loses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_latest_retired_landing_wins_by_number_and_a_bracket_is_no_pattern`

Old text:

```
        return 1 << 30
```

New text:

```
        return 0
```

### `u112.C5_unexpected_failure_stops`

A step failing in a way the build does not expect stops every later approved step

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C5_unexpected_failure_stops`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after`

Old text:

```
            step.error = refuse(
                "internal-error",
```

New text:

```
            raise
            step.error = refuse(
                "internal-error",
```

### `u112.R8_inbox_mine_unlisted`

A playlist of the author's that the rotation leaves alone under INBOX is not listed

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R8_inbox_mine_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_what_the_author_made_is_listed_with_a_home_and_never_a_write`

Old text:

```
    for node in plan.left:
```

New text:

```
    for node in ():
```

### `u116.M9_yours_lists_moved`

_yours: a playlist the filing step moves is still listed as yours, not moved

- File: `src/cratekit/organize/account.py`
- Source: `u116.json`, row `M9_yours_lists_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_the_full_verb_lists_the_working_custom_and_never_the_root_steps_removals`

Old text:

```
            or one.playlist_id in moving

```

New text:

```
(empty)
```

### `u137.R4_rotation_shown_unselected`

Show a planned rotation that was planned only for yours

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R4_rotation_shown_unselected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
        if area.wants(ROTATE) or rotation.cause is not None:
```

New text:

```
        if True:
```

### `r1295.M12_setrow_keeps_no_unread`

_decided: the set row keeps no unread tracks for the write to decide from

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M12_setrow_keeps_no_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
        unread=unread,
    )
```

New text:

```
        unread=(),
    )
```

### `u144-a.A6_set_name_spelling`

Account sets: write the stripped account name as it is, slash and all

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A6_set_name_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 A b2b B / Night 10-18-5_28_26 A b2b B - Night 10-18]`

Old text:

```
            sets_found.append((folder_name, playlist_id, set_cli.set_name(stripped)))
```

New text:

```
            sets_found.append((folder_name, playlist_id, stripped))
```

### `r1295.M10_unread_off_misses`

_matched: an unread track is not among the set's misses

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M10_unread_off_misses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
    misses: list[Miss] = list(unread)
```

New text:

```
    misses: list[Miss] = []
```

### `u144-a.A4_sets_folder_name`

Account sets: read every root folder, not only a Downloaded Sets year or a recorded one

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A4_sets_folder_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now`
  - `tests/test_organize_inspiration.py::test_only_prefixed_playlists_in_a_downloaded_sets_folder_are_sets`

Old text:

```
        if not sets_folder(folder_name) and folder_id not in marked:
```

New text:

```
        if False:
```

### `r1295.M11_again_drops_unread`

again: the write re-decides without the unread tracks, so the approved plan reads stale

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M11_again_drops_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
                    row.withheld,
                    row_of,
                    row.unread,
```

New text:

```
                    row.withheld,
                    row_of,
                    (),
```

### `u144-a.A5_recorded_folder`

Account sets: ignore the ledger's record, so a renamed sets folder is passed over

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A5_recorded_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_the_archive_recorded_is_read_whatever_it_is_called_now`

Old text:

```
        if not sets_folder(folder_name) and folder_id not in marked:
```

New text:

```
        if not sets_folder(folder_name):
```

### `u147-d.A3_twin_folders_read`

account_mirror.read_library: two rekordbox folders of one name are both mirrored into one

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A3_twin_folders_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_library.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_library.py::test_two_tree_folders_of_one_name_refuse_that_name_and_read_the_rest`

Old text:

```
        if counted[name] > 1:
```

New text:

```
        if counted[name] > 99:
```

### `u147-b.M13_links_unrecorded`

mirror.apply: record no link, so every refresh matches every row again

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M13_links_unrecorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_second_run_plans_nothing_writes_nothing_and_asks_no_match_again`
  - `tests/test_organize_mirror.py::test_a_write_elsewhere_in_the_ledger_carries_the_mirror_record_through`
  - `tests/test_organize_mirror.py::test_rows_a_folder_with_nothing_to_write_matched_are_linked_by_another_folders_apply`
  - `tests/test_organize_mirror.py::test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any`

Old text:

```
    ledger.record_mirror_links(cfg, planned.links if links is None else links)
```

New text:

```
    pass
```

### `r1031.M10_filter_against_raw_links`

ledger._load: drop a miss beside a raw link entry with no account track, the review's round one finding

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M10_filter_against_raw_links`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_link_with_no_account_track_does_not_hide_a_miss`

Old text:

```
            and str(content_id) not in linked
```

New text:

```
            and str(content_id) not in links
```

### `r1031.M8_misses_not_a_map_read`

ledger._load: read a mirror_misses that is not a map instead of refusing

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M8_misses_not_a_map_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_whose_misses_are_not_a_map_refuses`

Old text:

```
    if not isinstance(misses, Mapping):
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

New text:

```
    if False:
        raise _unusable(path, "mirror_misses must be a map of content row to its miss")
```

### `r1031.M9_malformed_miss_kept`

ledger._load: keep a miss whose key is not a list

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r1031.json`, row `M9_malformed_miss_kept`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_malformed_miss_is_dropped_and_asked_again_rather_than_refusing`

Old text:

```
            and isinstance(value.get("under"), list)
```

New text:

```
            and True
```

### `u222.M21_cli_message_unchanged`

_ask: keep the gate's bare message on a stale answer

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M21_cli_message_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_without_the_frozen_plan_the_same_two_acts_are_refused_stale`

Old text:

```
                message=f"{cause.message}; {area.name}: " + "; ".join(area.stale),
```

New text:

```
                message=cause.message,
```

### `u222.M1_overlay_not_read`

read: never overlay the frozen snapshots, so the decided run reads the ledger's live snapshot as before U222 (sitting 66)

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M1_overlay_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`

Old text:

```
    if frozen is not None:
        # THE GATE'S SNAPSHOTS
```

New text:

```
    if False:
        # THE GATE'S SNAPSHOTS
```

### `u222.M9_text_check`

_text: accept anything as text

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M9_text_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
    if not isinstance(value, str):
        raise ValueError(f"{what} is {value!r}, not text")
```

New text:

```
    if False:
        raise ValueError(f"{what} is {value!r}, not text")
```

### `u222.M17_refused_named_by_every_line`

moved: name a refused step by every line the gate showed (review round one)

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M17_refused_named_by_every_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`

Old text:

```
            if lines and then.lines
            else []
```

New text:

```
            if lines or then.lines
            else []
```

### `u150.M1_retire_flag`

mirror.plan: drop the retiring folder's flag, so a playlist whose batch left INBOX is left on the account instead of removed

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M1_retire_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 7 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_still_under_inbox_that_no_longer_reads_as_one_is_left_not_removed`
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_already_gone_from_the_account_is_still_forgotten`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_for_any_other_reason_is_raised`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`
  - `tests/test_organize_mirror_inbox.py::test_the_digest_covers_the_removal`

Old text:

```
        if not folder.retire:
            left.append(
```

New text:

```
        if True:
            left.append(
```

### `u150.Z1_frozen_retire`

mirror_frozen: rebuild every frozen folder as not retiring, so the apply after a gate removes nothing the gate named

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u150.json`, row `Z1_frozen_retire`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 69 against a baseline of 69
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_frozen_folder_whose_retire_is_not_a_boolean_is_not_read[retire-yes]`
  - `tests/test_organize_mirror_inbox.py::test_the_frozen_plan_carries_inbox_its_retirement_and_its_titles`

Old text:

```
                retire=_flag(folder["retire"]),
```

New text:

```
                retire=False,
```

### `u267.M2_applying_run_shares`

organize: the run that answers a gate makes a shared read too, so its plans read through one handle

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M2_applying_run_shares`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_the_applying_run_opens_exactly_as_it_did`

Old text:

```
    one_read = rb_writer.SharedRead(cfg) if report else None
```

New text:

```
    one_read = rb_writer.SharedRead(cfg)
```

### `u242.M24_root_reads_the_title_alone`

root step: count a label folder's downloaded playlists by the title alone

- File: `src/cratekit/organize/root.py`
- Source: `u242.json`, row `M24_root_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_year_playlist_held_as_taken_with_no_prefix_proves_its_tracks_downloaded`

Old text:

```
                if is_taken(playlist_id, name, self._taken)
```

New text:

```
                if name.startswith("DOWNLOADED ")
```

### `u143-e.P3_kept_problems`

Apply: stop on every refusal, so a refusal before sending stops the rest

- File: `src/cratekit/organize/root.py`
- Source: `u143-e.json`, row `P3_kept_problems`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_removal_the_account_refuses_before_sending_is_kept_and_the_apply_goes_on`

Old text:

```
                if exc.cause.detail.get("problem") not in KEPT_PROBLEMS:
```

New text:

```
                if True:
```

### `u255.S4_added_not_remembered`

add_to_playlist: a landed add is not appended to the membership, an existing guard

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `S4_added_not_remembered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_tidal_account.py::test_a_member_already_on_the_playlist_makes_no_write`

Old text:

```
            return
        members.append(identifier)

```

New text:

```
            return

```

### `u270.L2_row_only_for_a_recorded_track`

record_playlist_tracks: note a row for a track not recorded as added, claiming a person's track by its row

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u270.json`, row `L2_row_only_for_a_recorded_track`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 257 against a baseline of 257
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_the_ledger_never_notes_a_row_for_a_track_it_does_not_hold_as_added`

Old text:

```
            if str(track) in added:
                known[str(row)] = str(track)
```

New text:

```
            if True:
                known[str(row)] = str(track)
```

### `u270.C5_unfiled_said_once`

run_export_items: every item of the batch carries the filing warning, one per track in the summary

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C5_unfiled_said_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 159 against a baseline of 159
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`

Old text:

```
            "unfiled": report.unfiled if first_said else "",
```

New text:

```
            "unfiled": report.unfiled,
```

### `u220.A10_wrong_status`

_stale_tag: look for a 409 rather than the 412 the provider answers

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A10_wrong_status`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
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

### `u220.A12_no_memory_guard`

order_tracks: ignore what this command's adds left, so a first reading lagging them is planned from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A12_no_memory_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
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

### `r1308.M9_videos_unchecked`

_removal_read_back: drop the no video check

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M9_videos_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`

Old text:

```
if not _count(declared) or not _count(videos) or videos != 0
```

New text:

```
if not _count(declared)
```

### `r1308.M12_count_after_le`

_removal_read_back: a count at or under after's reads as after

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M12_count_after_le`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`

Old text:

```
if declared == len(expected)
```

New text:

```
if declared <= len(expected)
```

### `r1032.A11_empty_album_narrows`

_on_album: drop the empty tag guard, so a file with no album narrows a tie to the releases the provider left unnamed

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A11_empty_album_narrows`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`

Old text:

```
        remote for remote in remotes if wanted and match.fold(_album_name(tracks[remote])) == wanted
```

New text:

```
        remote for remote in remotes if match.fold(_album_name(tracks[remote])) == wanted
```

### `r1032.A7_lowest_by_characters`

_lowest: order the identifiers as text, so 100 sorts before 99

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A7_lowest_by_characters`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`

Old text:

```
    return min(remotes, key=lambda remote: (len(remote), remote))
```

New text:

```
    return min(remotes)
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

### `u208.M20_adapter_stale_tie`

match_track: keep the last match's tie flag across a later match of the same row

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M20_adapter_stale_tie`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`

Old text:

```
        self._ties.discard(key)
```

New text:

```
        pass
```

### `r358-round-2.A5_absent_answer`

Accept an explicit not found as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A5_absent_answer`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_deleted_between_the_open_and_the_edit_is_the_items_cause`

Old text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False or accepted is _ABSENT:
```

New text:

```
        accepted = self._call(doing, lambda: retitle(title=wanted))
        if accepted is False:
```

### `r356-a.A10_provider_title_read_one_way_only`

Only the first reading of the provider's title is compared, so a version the provider spelled after a dash never agrees

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A10_provider_title_read_one_way_only`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_provider_title_that_reads_two_ways_agrees_under_either_too`

Old text:

```
for one in listed.readings}
```

New text:

```
for one in (listed,)}
```

### `r356-a.A14_no_joiner_words`

A row spelling two artists with feat no longer agrees with the track billing both

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A14_no_joiner_words`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
_JOINERS = frozenset({"feat", "ft", "featuring", "with", "and", "vs", "x"})
```

New text:

```
_JOINERS = frozenset()
```

### `u226.M13_removal_window_wrong`

_removal_read_back: a lagging window is read as a wrong track gone, refused at once

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M13_removal_window_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
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

### `u51-item-derivation.D5_repeated_deduped`

Queue a repeated identifier twice instead of once

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D5_repeated_deduped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_repeated_track_id_becomes_one_item`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
        if track_id in seen:
```

New text:

```
        if False:
```

### `u51-item-derivation.D4_dangling_reported`

Stop reporting a TrackID the playlist names and the collection lacks

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D4_dangling_reported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_dangling_track_id_is_reported_and_not_queued`
  - `tests/test_outbound_workers.py::test_the_queued_envelope_names_a_missing_and_a_repeated_track`

Old text:

```
            dangling.append(track_id)
            continue
```

New text:

```
            continue
```

### `r227.S3_utc_date_in_the_sentence`

The warning names the UTC date rather than the person's own

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S3_utc_date_in_the_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`

Old text:

```
    return moment.astimezone().date().isoformat()
```

New text:

```
    return moment.date().isoformat()
```

### `r227.S7_floored_age_in_the_sentence`

The age is spelled in whole days only, so the sentence says seven is past seven

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S7_floored_age_in_the_sentence`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
    return f"{elapsed.days} days {hours} hours"
```

New text:

```
    return f"{elapsed.days} days"
```

### `u131.K8_export_files_once`

export.apply: file on every apply rather than only the one that created the playlist

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u131.json`, row `K8_export_files_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_export_collection.py`, `tests/test_outbound_workers.py`
- Collected: 234 against a baseline of 234
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_new_export_is_filed_in_exports_at_creation`

Old text:

```
    if reserved.created:
        # FILED AT CREATION
```

New text:

```
    if True:
        # FILED AT CREATION
```

### `r1305.A1_account_name_on_any_link`

_session_refused: read the client's authentication error by name on any link, so a reset met while handling one drops the account and asks for a login

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A1_account_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 197 against a baseline of 197
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_an_authentication_error_reached_only_as_context_is_not_a_rejected_session`

Old text:

```
        if declared and type(link).__name__ == "AuthenticationError":
```

New text:

```
        if type(link).__name__ == "AuthenticationError":
```

### `u261.A2_account_reuse_ignores_the_hold`

account.resolve: hand out the held adapter whatever became of its session, so a client the catalogue saw refused is reused by the account

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A2_account_reuse_ignores_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 143 against a baseline of 143
- Kills: 3 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[403]`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`

Old text:

```
    if _OPENED is not None and _OPENED_OVER is provider_session.held():
```

New text:

```
    if _OPENED is not None:
```

### `r836-b.L3_created_false_when_adopted`

ledger.reserve_label_year: an adopted year is written as created, so a prune takes tracks off a playlist the source system made

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r836-b.json`, row `L3_created_false_when_adopted`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 3 (killed)
- Killed:
  - `tests/test_prune.py::test_a_year_adopted_from_the_account_is_said_and_left_alone`
  - `tests/test_prune.py::test_adopted_anywhere_wins_over_another_record_of_the_same_playlist`
  - `tests/test_prune.py::test_product_made_says_yes_only_where_a_record_does`

Old text:

```
            "created": not adopt,
```

New text:

```
            "created": True,
```

### `r836-c.L7_row_only_for_a_written_track`

ledger.record_playlist_row: a row is recorded for a track this product never wrote, which a prune then reads as its own

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r836-c.json`, row `L7_row_only_for_a_written_track`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_row_is_never_recorded_for_a_track_this_product_did_not_write`

Old text:

```
        if not record or str(remote_id) not in _listed(record, "added"):
            return
        rows = _rows(record)
```

New text:

```
        if not record:
            return
        rows = _rows(record)
```

### `r836-f.P7_unrowed_with_unmatched_left_alone`

prune.plan_export: a playlist written before rows were kept is pruned by match while a row matched nothing today

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-f.json`, row `P7_unrowed_with_unmatched_left_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_an_unmatched_row_leaves_a_playlist_written_before_rows_alone`

Old text:

```
    elif unrowed and unmatched:
```

New text:

```
    elif False:
```

### `u174.O6_native_refusal_is_a_step`

_mark_steps: let native_passes' refusal escape, so the whole organize refuses and the file proven passes are not planned

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O6_native_refusal_is_a_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 164 against a baseline of 164
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_an_unreachable_root_is_a_refused_step_and_never_no_pass`
  - `tests/test_sync_mark.py::test_an_unreadable_tree_registry_refuses_the_native_step_alone`

Old text:

```
    try:
        native_names = mark_cli.native_passes(cfg)
    except CratekitError as exc:
```

New text:

```
    try:
        native_names = mark_cli.native_passes(cfg)
    except ZeroDivisionError as exc:
```

### `u221.R13_hold_not_read`

PairStore._pair: read no hold, so every twin falls to the time rule and a released one is held again

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R13_hold_not_read`
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
            on_hold=None if on_hold is None else MappingProxyType(dict(on_hold)),
```

New text:

```
            on_hold=None,
```

### `r356-b.B6_export_plan_drops_the_reason`

An unmatched export row never carries what the account said about it

- File: `src/cratekit/modules/outbound/export.py`
- Source: `r356-b.json`, row `B6_export_plan_drops_the_reason`
- Moved: the reason export.plan gives an unmatched row moved out of the Unmatched constructor's keyword arguments into a local reason the row is built from on the next line; the same account reason is dropped for the bare word
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_an_unmatched_export_row_carries_what_the_account_said_about_it`

Old text:

```
            reason = account.unmatched_reason(track.identity) or "unmatched"

```

New text:

```
            reason = "unmatched"

```

### `u123.T2_read_back`

Trust the delete and never read the playlist back

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T2_read_back`
- Moved: the read back after a playlist's delete moved out of remove_playlist into _sent_and_read_back, shared with the kind playlist removal, and reads the playlist through _served, which answers None for an absent one; the same still served check is made never true
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`

Old text:

```
        if self._served(doing, identifier) is not None:

```

New text:

```
        if False:

```

### `u204.P6_filed_no_month`

_decide_favorites: a track put in All Favorites that sits in a month is given a second month by its time

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P6_filed_no_month`
- Moved: the extra carried for a track put in All Favorites in _decide_favorites was folded from a multi line dict onto one line with its when read into a local first; the same filed flag is forced False
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`
- Collected: 42 against a baseline of 42
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_put_in_all_favorites_that_sits_in_a_month_takes_no_month`

Old text:

```
            extra = {"when": next(when, ""), "filed": bool(now_m or there_m)}

```

New text:

```
            extra = {"when": next(when, ""), "filed": False}

```

### `u147-c.M17_playlist_made_twice`

ledger.reserve_mirror_playlist: a recorded playlist is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u147-c.json`, row `M17_playlist_made_twice`
- Moved: the reuse of a recorded playlist moved from ledger.reserve_mirror_playlist into ledger_reserve._reserve, shared by reserve_mirror_playlist and the other playlist reserves, where the mirror entry arrives as a table and the key as a parameter; the same lookup and early return are deleted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on`
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`
  - `tests/test_organize_mirror.py::test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        held = table(document)
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False

```

New text:

```
        held = table(document)

```

### `r1289.M17_mirror_listing_refusal`

mirror_downloads.plan (existing guard, sample): a playlist the provider cannot list names nothing for its tracks

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M17_mirror_listing_refusal`
- Moved: the not queued entry mirror_downloads.plan names for a playlist the provider cannot list is now built by the shared _not_queued helper instead of an inline dict; the same loop over its tracks is emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_playlist_the_provider_cannot_list_is_named_and_the_others_queue`

Old text:

```
                _not_queued(track, title, f"the provider could not list the playlist: {exc.cause.message}")
                for track in sorted(set(tracks))

```

New text:

```
                _not_queued(track, title, f"the provider could not list the playlist: {exc.cause.message}")
                for track in ()

```

### `u150.M8_refusal_kept`

mirror.apply: raise a playlist removal refused with nothing sent, so one unvouched playlist stops the folder's apply

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M8_refusal_kept`
- Moved: the retire loop in mirror.apply now keeps a refused removal through the _kept helper it shares with the track removals, which raises any other refusal itself; the same keep and continue at the retire call site are replaced by a raise
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_removal_refused_with_nothing_sent_is_kept_named_and_planned_again`

Old text:

```
            _kept(exc, name, done)
            continue
        ledger.forget_mirror_playlist
```

New text:

```
            raise
        ledger.forget_mirror_playlist
```

### `u255.C4_held_before_read_and_playlist_keeps_the_hold`

M4 with _playlist's drop removed too: a failed tracks read leaves the opened object held, and the next membership read reuses nothing that drops it, drive H of round one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `C4_held_before_read_and_playlist_keeps_the_hold`
- Moved: the span from _playlist's dropped hold to _membership's open is shorter now, with _listed moved out from between them and the _held docstring cut down; the same two edits are made, the drop in _playlist removed and the hold taken before the tracks read
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`
- Collected: 24 against a baseline of 24
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
        self._opened.pop(playlist_id, None)
        doing = f"open the playlist {playlist_id}"
        found = self._call(doing, lambda: self._session.playlist(playlist_id))
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"), doing
            )
        return found

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS (U255): an open is two GETs and the client's
        add reads the playlist again after its POST, so opening per add cost
        four requests a track. THE TAG AND THE POSITION COME FROM ONE ANSWER:
        the client's add sends the object's tag and puts the track at its
        length, both set by one read, which is why :meth:`_membership` reads the
        tracks through a copy and holds nothing until that read succeeds. A
        stale held tag is refused 412 with nothing changed (Sitting 62), and
        :meth:`add_to_playlist` then opens afresh.
        """
        held = self._opened.get(playlist_id)
        if held is None:
... truncated ...
```

New text:

```
        doing = f"open the playlist {playlist_id}"
        found = self._call(doing, lambda: self._session.playlist(playlist_id))
        if found is _ABSENT or found is None:
            raise account.provider_failure(
                LookupError(f"the provider has no playlist {playlist_id!r}"), doing
            )
        return found

    def _held(self, playlist_id: str) -> Any:
        """The playlist's held object, opened through :meth:`_playlist` only if none is held.

        ONE OPEN FOR A RUN OF ADDS (U255): an open is two GETs and the client's
        add reads the playlist again after its POST, so opening per add cost
        four requests a track. THE TAG AND THE POSITION COME FROM ONE ANSWER:
        the client's add sends the object's tag and puts the track at its
        length, both set by one read, which is why :meth:`_membership` reads the
        tracks through a copy and holds nothing until that read succeeds. A
        stale held tag is refused 412 with nothing changed (Sitting 62), and
        :meth:`add_to_playlist` then opens afresh.
        """
        held = self._opened.get(playlist_id)
        if held is None:
            held = self._playlist(playlist_
... truncated ...
```

### `r572.L1_local_track_drop_album`

local_tracks stops carrying the file's album

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `L1_local_track_drop_album`
- Moved: local_tracks now builds each LocalTrack on one line from the shared _identified rows, with the other fields positional; the same album keyword is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`

Old text:

```
        LocalTrack(track_id, entry.name, entry.artist, found.isrc, title, album=found.album)

```

New text:

```
        LocalTrack(track_id, entry.name, entry.artist, found.isrc, title)

```

### `r358.A4_false_answer`

Accept a False answer as a rename that landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A4_false_answer`
- Moved: the rename refusal in tidal_account is the same check with the provider_failure call rewrapped, its doing argument joined to the message line; the same False case is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_the_client_answers_false_is_the_items_cause_not_a_quiet_return`

Old text:

```
        if accepted is False or accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"), doing

```

New text:

```
        if accepted is _ABSENT:
            raise account.provider_failure(
                RuntimeError("the provider did not accept the new playlist title"), doing

```

### `r850-a.E2_unmatched_count`

export.summary: count unmatched as the reason sentences, so a row the account said nothing about is not counted

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E2_unmatched_count`
- Moved: export.summary's counts were folded from a multi line dict onto one line in the same function, where the old line had a twin in favorites/cli.py; the same unmatched count is taken from the reasons
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        "counts": {"written": len(added), "already": len(already), "unmatched": len(unmatched)},

```

New text:

```
        "counts": {"written": len(added), "already": len(already), "unmatched": len(reasons)},

```

### `r850-a.E1_written_count`

export.summary: count written as the already list's length, so the answer's written count is the wrong list

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E1_written_count`
- Moved: export.summary's counts were folded from a multi line dict onto one line in the same function; the same written count is taken from the already list
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`
  - `tests/test_outbound_workers.py::test_a_second_export_counts_what_the_playlist_already_held`
  - `tests/test_outbound_workers.py::test_an_export_where_every_track_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
        "counts": {"written": len(added), "already": len(already), "unmatched": len(unmatched)},

```

New text:

```
        "counts": {"written": len(already), "already": len(already), "unmatched": len(unmatched)},

```

### `u131.K6_adopt_not_made`

ledger.reserve_kind_folder: record an adopted folder as made here

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `u131.json`, row `K6_adopt_not_made`
- Moved: reserve_kind_folder moved into ledger_reserve and records through _reserve_folder, which passes created False for an adopted folder to the kind's own keep lambda; that lambda's record is made to say created True, so an adopted kind folder is again recorded as made here and the answer is unchanged
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`
- Collected: 14 against a baseline of 14
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_hand_made_folder_named_mine_is_adopted_and_never_emptied`

Old text:

```
            {kind: {"folder_id": folder_id, "created": created}}

```

New text:

```
            {kind: {"folder_id": folder_id, "created": True}}

```

