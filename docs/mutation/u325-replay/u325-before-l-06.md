# Mutation table: u325-before-l-06

Measured by `scripts/mutate.py` on 2026-11-23 01:29 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 29.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:24 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 6, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 86 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r836-g.C3_dangling_rows_are_rows` | `src/cratekit/export/prune_cli.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-g.C1_holds_judged_again` | `src/cratekit/label/prune_cli.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-d.P1_only_created_years` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-e.P2b_mismatch_read_only_with_nothing_gone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-e.P5_apply_asks_the_ledger_again` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P7_unrowed_with_unmatched_left_alone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P8_drifted_match_left_alone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-f.P9_row_in_playlist_keeps_its_track` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 3 | killed |
| `r836-b.L1_adopted_anywhere_wins` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-b.L2_export_records_are_made_here` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 4 | killed |
| `r836-b.L3_created_false_when_adopted` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 3 | killed |
| `r836-b.L4_pruned_leaves_added` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 5 | killed |
| `r836-b.L5_older_export_refused` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-c.L6_date_on_the_confirmed_record` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 2 | killed |
| `r836-c.L7_row_only_for_a_written_track` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `r1308.M11_count_before_ge` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 1 | killed |
| `r1308.M12_count_after_le` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 1 | killed |
| `r1308.M13_accept_tracks_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 8 | killed |
| `r1308.M14_lag_by_or` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 11 | killed |
| `r1308.M15_lag_always` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 12 | killed |
| `r1308.M16_no_break` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 10 | killed |
| `r1308.M18_not_forgotten` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 2 | killed |
| `r1308.M20_message_swapped` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 15 | killed |
| `r1308.M21_halves_swapped` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 1 | killed |
| `r1308.M22_retryable` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 14 | killed |
| `r1308.M23_read_back_bypassed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 34 | killed |
| `r1308.M24_positions_count` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 2 | killed |
| `r1308.M6_after_by_length` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 4 | killed |
| `r1308.M8_count_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 9 | killed |
| `r1308.M9_videos_unchecked` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 2 | killed |
| `r229.L10_a_name_matches_by_bare_suffix` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L11_an_empty_name_matches` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L12_the_first_of_several_is_adopted` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r229.L13_a_mismatch_is_never_said` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r229.L14_a_recorded_crate_is_a_claimant` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L16_a_moved_record_is_not_followed` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 3 | killed |
| `r229.L18_contents_grow` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 5 | killed |
| `r229.L19_a_copy_not_a_move` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 6 | killed |
| `r229.L1_a_third_suffices` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r229.L2_exactly_half_is_not_enough` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L3_nothing_shared_is_a_match` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L4_an_eighth_of_the_crate` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L5_no_crate_side_bound` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r229.L6_a_living_crate_is_a_candidate` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 3 | killed |
| `r229.L7_a_reused_path_keeps_its_record` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r229.L8_a_living_legacy_record_is_freed` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r229.L9_an_empty_list_is_a_legacy_record` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 1 | killed |
| `r923.N13_judge_compares_raw` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `r923.N2_plan_lists_tombstones` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 13 | killed |
| `r923.N3_plan_sees_no_null` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 8 | killed |
| `r923.N4_stale_fill_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N5_stale_tombstone_accepted` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N6_judge_blind_to_wrong` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N7_judge_blind_to_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N8_read_back_never_refuses` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F11_stale_file_id_not_checked` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F12_read_back_ignores_file_id` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F13_planned_renumber_read_as_moved` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F14_renumber_never_written` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F17_bound_is_zero` | `src/cratekit/write/row_defaults.py` | maintainer | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u115.F21_other_volume_compared` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F22_off_apfs_decides` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F23_loose_digits` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 3 | killed |
| `u115.F5_bound_boundary` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 2 | killed |
| `u115.F6_every_id_above` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 12 | killed |
| `u115.F7_zero_is_not_zero` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 4 | killed |
| `u115.F8_matching_inode_renumbered` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u115.F9_unreadable_file_dropped_silently` | `src/cratekit/write/row_defaults.py` | user | 1 file(s) | 53 | 5 | killed |
| `r923.N14_verb_writes_on_abort` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 7 | killed |
| `r923.N15_verb_writes_empty_plan` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `r923.N16_ack_not_read` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `r923.N17_write_handle_not_closed` | `src/cratekit/write/row_defaults_cli.py` | maintainer | 1 file(s) | 53 | 1 | killed |
| `u115.F18_undecidable_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 1 | killed |
| `u115.F19_unrenumbered_unsaid` | `src/cratekit/write/row_defaults_cli.py` | user | 1 file(s) | 53 | 2 | killed |
| `r289-a.A1_appledouble_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A2_appledouble_one_dot` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r289-a.A3_staging_dirs_gone` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `r289-a.A4_staging_dirs_acquire_only` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `r289-a.A5_staging_dirs_absolute` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r650-a.B3_engine_drops_the_flag_on_the_write` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 3 | killed |
| `r650-a.B4_engine_leaks_the_flag_onto_a_skip` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 7 | killed |
| `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 4 | killed |
| `u85-a.A11_failed_write_is_error` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A13_art_only_refusal_absorbed` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 2 | killed |
| `u85-a.A1_search_skipped_only_with_both` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 11 | killed |
| `u85-a.A2_any_picture_settles` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 8 | killed |
| `u85-a.A3_unreadable_is_unchecked` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A5_no_url_guard` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 22663 | 1 (promoted) | killed |
| `u85-a.A6_no_fetch_guard` | `src/cratekit/tagging/tag.py` | maintainer | 4 file(s) | 242 | 1 | killed |
| `u85-a.A7_fetch_raise_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `u85-a.A9_not_a_picture_is_a_decline` | `src/cratekit/tagging/tag.py` | user | 4 file(s) | 242 | 1 | killed |
| `r1499.L01_go_arrival_after_tail` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.L02_go_kept_after_arrival` | `src/cratekit/cli/label_sync.py` | user | 6 file(s) | 324 | 3 | killed |
| `r1499.S01_download_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 12 | killed |
| `r1499.S02_tail_reading` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S03_arrival_after_tail` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S04_arrival_after_plan` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S05_keep_after_arrival` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S06_keep_called` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 7 | killed |
| `r1499.S07_kept_read` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 4 | killed |
| `r1499.S08_own_pass_proof` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 2 | killed |
| `r1499.S09_own_library` | `src/cratekit/cli/sync_land.py` | maintainer | 6 file(s) | 324 | 1 | killed |
| `r1499.S10_own_by_list` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 66 | killed |
| `r1499.S11_unreadable_refuses` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S12_warnings_in_refusal` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |
| `r1499.S13_own_unnamed_step` | `src/cratekit/cli/sync_land.py` | user | 6 file(s) | 324 | 1 | killed |

## Zero rows and what they owe

- `u115.F17_bound_is_zero` (maintainer facing): maintainer facing, composite not required
- `u115.F8_matching_inode_renumbered` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r836-g.C3_dangling_rows_are_rows`

export.prune_cli: a row the export names and does not carry is read as gone, so its track is taken off

- File: `src/cratekit/export/prune_cli.py`
- Source: `r836-g.json`, row `C3_dangling_rows_are_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_row_the_export_names_and_does_not_carry_keeps_its_track`

Old text:

```
        (*resolved.track_ids, *resolved.dangling),
```

New text:

```
        resolved.track_ids,
```

### `r836-g.C1_holds_judged_again`

label.prune_cli.held_releases: a hold the gate would now release still takes the release's tracks off

- File: `src/cratekit/label/prune_cli.py`
- Source: `r836-g.json`, row `C1_holds_judged_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_hold_the_gate_would_now_release_takes_nothing_off`

Old text:

```
        and (hold.payload.get(review.WITHHELD_FIELD) or judge.rejudge(entry, hold).held)
```

New text:

```
(empty)
```

### `r836-d.P1_only_created_years`

prune.plan_label: a year recorded before the created field is pruned as though made here

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-d.json`, row `P1_only_created_years`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_year_recorded_before_the_field_is_said_as_such_not_as_adopted`

Old text:

```
        if recorded.created is not True:
```

New text:

```
        if recorded.created is False:
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

### `r836-e.P5_apply_asks_the_ledger_again`

prune.apply: a plan built in another invocation removes from a playlist the ledger no longer vouches for

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-e.json`, row `P5_apply_asks_the_ledger_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_the_apply_asks_the_ledger_again_and_refuses_a_playlist_it_no_longer_vouches_for`

Old text:

```
        if not ledger.product_made(cfg, step.remote_id):
            raise _not_made(step.remote_id)
```

New text:

```
(empty)
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

### `r836-f.P8_drifted_match_left_alone`

prune.plan_export: a row matching a track never written here does not stop the match reading, so a drifted match takes a track off

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `r836-f.json`, row `P8_drifted_match_left_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_match_that_moved_leaves_a_playlist_written_before_rows_alone`

Old text:

```
    elif unrowed and fresh:
```

New text:

```
    elif False:
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

### `r836-b.L1_adopted_anywhere_wins`

ledger.product_made: a label year adopted from the account no longer answers no, so another record of the same id vouches for it

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L1_adopted_anywhere_wins`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_adopted_anywhere_wins_over_another_record_of_the_same_playlist`

Old text:

```
                if entry.get("created") is not True:
                    return False
                made = True
```

New text:

```
                if entry.get("created") is True:
                    made = True
```

### `r836-b.L2_export_records_are_made_here`

ledger.product_made: an exported playlist's record no longer vouches, so export prune can never take a track off

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L2_export_records_are_made_here`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 4 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_written_before_rows_is_pruned_by_match_when_every_row_agrees`
  - `tests/test_prune.py::test_a_row_whose_match_failed_today_does_not_stop_a_track_recorded_by_its_row`
  - `tests/test_prune.py::test_an_exported_playlist_whose_library_playlist_lost_a_track_plans_exactly_it`
  - `tests/test_prune.py::test_product_made_says_yes_only_where_a_record_does`

Old text:

```
    for record in (*document["playlists"].values(), *document["sets"].values()):
```

New text:

```
    for record in document["sets"].values():
```

### `r836-b.L3_created_false_when_adopted`

ledger.reserve_label_year: an adopted year is written as created, so a prune takes tracks off a playlist the source system made

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L3_created_false_when_adopted`
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

### `r836-b.L4_pruned_leaves_added`

ledger._moved_to_pruned: a taken track stays in added, so the next prune asks the account for it again

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L4_pruned_leaves_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 5 (killed)
- Killed:
  - `tests/test_prune.py::test_a_held_release_plans_exactly_its_tracks_and_approved_only_they_leave`
  - `tests/test_prune.py::test_a_refusal_part_way_resumes_without_taking_anything_off_twice`
  - `tests/test_prune.py::test_a_second_run_plans_nothing`
  - `tests/test_prune.py::test_a_track_already_off_the_playlist_is_settled_through_the_removals_own_read`
  - `tests/test_prune.py::test_an_exported_playlist_whose_library_playlist_lost_a_track_plans_exactly_it`

Old text:

```
    entry["added"] = [one for one in _listed(entry, "added") if one not in gone]
```

New text:

```
(empty)
```

### `r836-b.L5_older_export_refused`

ledger.older_than: an export whose date could not be read is not older, so it is read for a prune

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-b.json`, row `L5_older_export_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_the_export_worker_records_the_date_of_the_export_it_read`

Old text:

```
    return not given or _later(recorded, given)
```

New text:

```
    return bool(given) and _later(recorded, given)
```

### `r836-c.L6_date_on_the_confirmed_record`

ledger._note_written: the export date goes on the key's own record, not the one the job was confirmed to update

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-c.json`, row `L6_date_on_the_confirmed_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 404 against a baseline of 404
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - `tests/test_prune.py::test_the_export_date_goes_on_the_record_the_job_was_confirmed_to_update`

Old text:

```
    if expected and str((record or {}).get("remote_id") or "") != expected:
```

New text:

```
    if False:
```

### `r836-c.L7_row_only_for_a_written_track`

ledger.record_playlist_row: a row is recorded for a track this product never wrote, which a prune then reads as its own

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r836-c.json`, row `L7_row_only_for_a_written_track`
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

### `r1308.M11_count_before_ge`

_removal_read_back: a count at or over before's reads as before

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M11_count_before_ge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`

Old text:

```
if declared == len(before)
```

New text:

```
if declared >= len(before)
```

### `r1308.M12_count_after_le`

_removal_read_back: a count at or under after's reads as after

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M12_count_after_le`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
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

### `r1308.M13_accept_tracks_only`

_removal_read_back: accept a reading whose tracks are after, whatever its count

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M13_accept_tracks_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
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
- Collected: 387 against a baseline of 387
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_reading_as_long_as_before_with_another_track_is_not_a_lag`
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

### `r1308.M15_lag_always`

_removal_read_back: every reading is a lag, so a wrong track is read again to the bound

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M15_lag_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound`
  - `tests/test_outbound_remove_lag.py::test_a_reading_as_long_as_before_with_another_track_is_not_a_lag`
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
lagged = True
```

### `r1308.M16_no_break`

_removal_read_back: no break on a wrong reading, so it is read again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M16_no_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound`
  - `tests/test_outbound_remove_lag.py::test_a_reading_as_long_as_before_with_another_track_is_not_a_lag`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`

Old text:

```
            if not lagged:
                break
        # WHAT
```

New text:

```
            if not lagged:
                pass
        # WHAT
```

### `r1308.M18_not_forgotten`

_removal_read_back: keep what was remembered of the playlist after a refusal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M18_not_forgotten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[99]`

Old text:

```
        self._members.pop(identifier, None)
        shown
```

New text:

```
        shown
```

### `r1308.M20_message_swapped`

_removal_read_back: a lag says a wrong track may have come off

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M20_message_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_reading_as_long_as_before_with_another_track_is_not_a_lag`
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

### `r1308.M21_halves_swapped`

_removal_read_back: the message names the other half

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M21_halves_swapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`

Old text:

```
("before", "after"): (
                "read after a removal with its declared count changed
```

New text:

```
("after", "before"): (
                "read after a removal with its declared count changed
```

### `r1308.M22_retryable`

_removal_read_back: the refusal as provider_failure, retryable, whose remedy is to run again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M22_retryable`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 14 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_reading_as_long_as_before_with_another_track_is_not_a_lag`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
        raise refuse(
            "outbound-remove-refused",
            (
                f"the playlist {identifier} {shown
```

New text:

```
        raise account.provider_failure(RuntimeError('lag'), 'remove')
        raise refuse(
            "outbound-remove-refused",
            (
                f"the playlist {identifier} {shown
```

### `r1308.M23_read_back_bypassed`

remove_tracks: take the expected list as read back without reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M23_read_back_bypassed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 34 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_catches_up_on_the_last_reading_is_taken_as_done`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            playlist, before = self._removal_read_back(identifier, before, expected)
```

New text:

```
            playlist, before = self._playlist(identifier), expected
```

### `r1308.M24_positions_count`

_positions: drop the declared count's match with the tracks read, the guard _reading was split from

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M24_positions_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 2 (killed)
- Killed:
  - `tests/test_prune.py::test_a_playlist_with_a_track_the_account_cannot_see_is_refused_with_nothing_sent`
  - `tests/test_prune.py::test_a_settled_track_the_listing_hides_is_not_recorded_as_off`

Old text:

```
            or declared != len(members)

```

New text:

```
(empty)
```

### `r1308.M6_after_by_length`

_removal_read_back: judge the tracks after by their number, not their content

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M6_after_by_length`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_refused_read_back_forgets_what_was_remembered_of_the_playlist[0]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_that_took_the_wrong_track_refuses_at_once_with_no_pause`
  - `tests/test_outbound_remove_lag.py::test_a_wrong_track_behind_a_lagging_count_refuses_at_once`
  - `tests/test_prune.py::test_a_removal_that_took_the_wrong_position_is_read_back_and_refused`

Old text:

```
else "after" if reading == expected else None
```

New text:

```
else "after" if len(reading) == len(expected) else None
```

### `r1308.M8_count_ignored`

_removal_read_back: take the count as after whatever it declares

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M8_count_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
- Kills: 9 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_removal_whose_read_lags_one_write_is_taken_as_done[count]`

Old text:

```
            counted = (
                None
                if not _count(declared)
```

New text:

```
            counted = "after" or (
                None
                if not _count(declared)
```

### `r1308.M9_videos_unchecked`

_removal_read_back: drop the no video check

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M9_videos_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 387 against a baseline of 387
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

### `r229.L10_a_name_matches_by_bare_suffix`

The name rule drops the separator, so Big Crate is recognised as Crate

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L10_a_name_matches_by_bare_suffix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
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

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L11_an_empty_name_matches`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
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

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L12_the_first_of_several_is_adopted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
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

### `r229.L13_a_mismatch_is_never_said`

A record under the crate's own path written from other music is reported as an ordinary update

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L13_a_mismatch_is_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`
  - `tests/test_outbound_workers.py::test_a_path_reused_for_a_different_crate_is_said_at_the_gate`

Old text:

```
        mismatched = bool(written) and not _still_carries(written, wanted)
```

New text:

```
        mismatched = False
```

### `r229.L14_a_recorded_crate_is_a_claimant`

A living crate with its own remote playlist is named as the one a mismatched record belongs to

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L14_a_recorded_crate_is_a_claimant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_under_the_crates_own_path_written_from_other_music_is_said`

Old text:

```
                and not (playlists.get(key) or {}).get("remote_id")

```

New text:

```
(empty)
```

### `r229.L16_a_moved_record_is_not_followed`

The confirmed remote id is ignored, so a half driven job whose record moved creates a second playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L16_a_moved_record_is_not_followed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_job_confirmed_before_its_record_moved_goes_on_writing_to_it`
  - `tests/modules/test_outbound.py::test_a_job_whose_confirmed_remote_playlist_nothing_records_refuses`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`

Old text:

```
        if expected and own != expected:
```

New text:

```
        if False:
```

### `r229.L18_contents_grow`

The recorded contents are appended to rather than replaced, which is the ever growing log the review found

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L18_contents_grow`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
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

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L19_a_copy_not_a_move`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
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

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L1_a_third_suffices`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
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

### `r229.L2_exactly_half_is_not_enough`

Exactly half no longer qualifies, the boundary moved from at least to more than

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L2_exactly_half_is_not_enough`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_is_recognised_when_the_crate_still_carries_half_its_tracks[exactly-half]`

Old text:

```
    return shared >= 1 and shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR
```

New text:

```
    return shared >= 1 and shared * SHARED_DENOMINATOR > len(written) * SHARED_NUMERATOR
```

### `r229.L3_nothing_shared_is_a_match`

The at least one shared track guard is removed, so an empty record is carried by anything

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L3_nothing_shared_is_a_match`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_that_holds_nothing_is_carried_by_nothing`

Old text:

```
    return shared >= 1 and shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR
```

New text:

```
    return shared * SHARED_DENOMINATOR >= len(written) * SHARED_NUMERATOR
```

### `r229.L4_an_eighth_of_the_crate`

The crate side bound loosens from a quarter to an eighth, so a crate one past quadrupled is recognised

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L4_an_eighth_of_the_crate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_crate_the_record_is_a_sliver_of_is_not_that_crate[one-past-quadrupled]`

Old text:

```
GROWN_DENOMINATOR = 4
```

New text:

```
GROWN_DENOMINATOR = 8
```

### `r229.L5_no_crate_side_bound`

A candidate is judged on the record's side alone, so a three thousand track crate is offered an eight track orphan

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L5_no_crate_side_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_crate_the_record_is_a_sliver_of_is_not_that_crate[a-crate-that-merely-contains-it]`
  - `tests/modules/test_outbound.py::test_a_crate_the_record_is_a_sliver_of_is_not_that_crate[one-past-quadrupled]`

Old text:

```
            if _still_carries(written, wanted) and _grown_within(written, wanted):
```

New text:

```
            if _still_carries(written, wanted):
```

### `r229.L6_a_living_crate_is_a_candidate`

A recorded key the export still carries is offered, so two crates sharing their tracks adopt each other

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L6_a_living_crate_is_a_candidate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 3 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_key_the_export_still_carries_is_not_a_candidate`
  - `tests/modules/test_outbound.py::test_a_legacy_record_under_a_living_path_is_never_freed`
  - `tests/test_outbound_workers.py::test_a_crate_the_export_still_carries_is_never_adopted_from`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if False and (not written or _still_carries(written, living[key])):
```

### `r229.L7_a_reused_path_keeps_its_record`

A displaced record is never freed, so a crate renamed away from a reused path forks as it did before

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L7_a_reused_path_keeps_its_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 2 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_path_reused_for_a_different_crate_frees_its_record`
  - `tests/test_outbound_workers.py::test_a_path_reused_for_a_different_crate_is_said_at_the_gate`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if key in living:
```

### `r229.L8_a_living_legacy_record_is_freed`

A legacy record under a living path is freed with no contents to say the path was reused

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L8_a_living_legacy_record_is_freed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_legacy_record_under_a_living_path_is_never_freed`

Old text:

```
        if key in living and (not written or _still_carries(written, living[key])):
```

New text:

```
        if key in living and _still_carries(written, living[key]):
```

### `r229.L9_an_empty_list_is_a_legacy_record`

A record this build wrote with no contents qualifies by name, as a record from before the field existed does

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r229.json`, row `L9_an_empty_list_is_a_legacy_record`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 294 against a baseline of 294
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_record_this_build_wrote_with_no_tracks_is_not_a_legacy_record`

Old text:

```
        elif _legacy(record) and _same_name(key, name):
```

New text:

```
        elif _same_name(key, name):
```

### `r923.N13_judge_compares_raw`

The read back compares a default by raw value, so the live table's integer reads as wrong against the binding's string

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N13_judge_compares_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            or str(now[column]) != str(rb_writer.CONTENT_ROW_DEFAULTS[column])
```

New text:

```
            or now[column] != rb_writer.CONTENT_ROW_DEFAULTS[column]
```

### `r923.N2_plan_lists_tombstones`

The repair plans soft deleted rows beside live ones

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N2_plan_lists_tombstones`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 13 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_plan_that_renumbers_nothing_registers_no_file_id_policy`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            f"WHERE {rb_writer.SOFT_DELETE_COLUMN} = 0"
```

New text:

```
            ""
```

### `r923.N3_plan_sees_no_null`

The repair never finds a NULL default, so it plans nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N3_plan_sees_no_null`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 8 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_planned_column_set_since_the_plan_refuses_stale_and_writes_nothing`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_nothing_is_judged_random`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_the_digest_moves_when_a_planned_column_is_filled_elsewhere`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        missing = tuple(column for column in COLUMNS if row[column] is None)
```

New text:

```
        missing = tuple(column for column in COLUMNS if False)
```

### `r923.N4_stale_fill_accepted`

A planned column set since the plan is written over anyway

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N4_stale_fill_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_planned_column_set_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if filled:
```

New text:

```
        if False:
```

### `r923.N5_stale_tombstone_accepted`

A row soft deleted since the plan is still written

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N5_stale_tombstone_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_deleted_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if row is None or row[rb_writer.SOFT_DELETE_COLUMN] != 0:
```

New text:

```
        if row is None:
```

### `r923.N6_judge_blind_to_wrong`

The read back no longer names a planned column that did not take its default

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N6_judge_blind_to_wrong`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`

Old text:

```
        if off:
```

New text:

```
        if False:
```

### `r923.N7_judge_blind_to_moved`

The read back no longer names a column outside the plan that moved

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N7_judge_blind_to_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_planned_column_still_null_and_a_column_that_moved`
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`

Old text:

```
        if changed:
```

New text:

```
        if False:
```

### `r923.N8_read_back_never_refuses`

assert_read_back returns whatever the read back found

- File: `src/cratekit/write/row_defaults.py`
- Source: `r923.json`, row `N8_read_back_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_a_moved_column_as_the_guards_defect`
  - `tests/test_repair_rows.py::test_assert_read_back_refuses_a_wrong_value`

Old text:

```
    if not written.wrong and not written.moved:
        return
```

New text:

```
    if True:
        return
```

### `u115.F11_stale_file_id_not_checked`

A file id changed since the plan is written over without a staleness refusal

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F11_stale_file_id_not_checked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_changed_since_the_plan_refuses_stale_and_writes_nothing`

Old text:

```
        if item.renumbers and str(row.get(FILE_ID) or "").strip() != item.file_id_was:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

New text:

```
        if False:
            moved.append(f"{item.content_id}: {FILE_ID} changed since the plan")
```

### `u115.F12_read_back_ignores_file_id`

The read back never checks that the inode took, so a renumber that did not land reads as written

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F12_read_back_ignores_file_id`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_names_a_renumber_that_did_not_take`

Old text:

```
        if item.renumbers and str(now.get(FILE_ID) or "").strip() != str(item.file_id):
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

New text:

```
        if False:
            wrong.append(f"{item.content_id}: {FILE_ID} not the file's inode")
```

### `u115.F13_planned_renumber_read_as_moved`

The read back forgets the file id was planned, so every renumber is reported as a column the guard let move

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F13_planned_renumber_read_as_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_judge_reads_a_planned_renumber_as_written_and_an_unplanned_one_as_moved`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            planned.add(FILE_ID)
```

New text:

```
        if False:
            planned.add(FILE_ID)
```

### `u115.F14_renumber_never_written`

The apply fills the defaults and never writes the planned file id

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F14_renumber_never_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
        if item.renumbers:
            writes.append((file_owner, FILE_ID, item.file_id))
```

New text:

```
        if False:
            writes.append((file_owner, FILE_ID, item.file_id))
```

### `u115.F17_bound_is_zero`

The volume's inode bound is reported as zero rather than measured from a fresh file

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F17_bound_is_zero`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        inode=measured.st_ino, device=measured.st_dev, filesystem=filesystem_of(directory)
```

New text:

```
        inode=0, device=measured.st_dev, filesystem=filesystem_of(directory)
```

### `u115.F21_other_volume_compared`

A file on another volume than the bound is stat'ed and its inode compared, so rekordbox's rows there can be renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F21_other_volume_compared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`

Old text:

```
    if found.st_dev != device:
        return None, ON_ANOTHER_VOLUME
```

New text:

```
    if False:
        return None, ON_ANOTHER_VOLUME
```

### `u115.F22_off_apfs_decides`

The bound is trusted on any filesystem, so an exFAT or HFS+ library has rekordbox's rows renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F22_off_apfs_decides`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`

Old text:

```
        if self.filesystem != APFS:
            named = self.filesystem or "unknown"
```

New text:

```
        if False:
            named = self.filesystem or "unknown"
```

### `u115.F23_loose_digits`

A signed or underscored text, or a digit from another script, is parsed as a number and judged above the bound

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F23_loose_digits`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 3 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[+200000000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[300_000_000-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663\u0663-within]`

Old text:

```
    if not (text.isascii() and text.isdigit()):
        return WITHIN
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    try:
        number = int(text)
    except ValueError:
        return WITHIN
    return ABOVE if number > bound else WITHIN
```

### `u115.F5_bound_boundary`

An id equal to the bound is judged above it

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F5_bound_boundary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE if int(text) >= bound else WITHIN
```

### `u115.F6_every_id_above`

Every nonzero id is judged above the bound, so stale rows rekordbox tolerates are renumbered

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F6_every_id_above`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 12 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[1-within]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[2000000-within1]`
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_policy_registered_before_the_apply_survives_it`
  - `tests/test_repair_rows.py::test_a_random_id_on_a_row_with_every_default_is_an_item_of_its_own`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_a_tombstone_is_never_listed_though_every_default_is_null`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    return ABOVE if int(text) > bound else WITHIN
```

New text:

```
    return ABOVE
```

### `u115.F7_zero_is_not_zero`

A stored 0 is no longer read as the zero form rekordbox tolerates

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F7_zero_is_not_zero`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 4 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero0]`
  - `tests/test_repair_rows.py::test_a_file_id_is_judged_against_the_bound_alone[0-zero1]`
  - `tests/test_repair_rows.py::test_off_apfs_nothing_is_judged_random_and_the_plan_says_which_filesystem`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`

Old text:

```
    if text in ("", "0"):
        return ZERO
```

New text:

```
    if text == "":
        return ZERO
```

### `u115.F8_matching_inode_renumbered`

A row above the bound whose file reads the same inode is renumbered to itself rather than left

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F8_matching_inode_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
            elif str(inode) == str(row[FILE_ID]).strip():
                matched += 1
```

New text:

```
            elif False:
                matched += 1
```

### `u115.F9_unreadable_file_dropped_silently`

A row above the bound whose file cannot be read is neither listed nor written, and the gate says nothing

- File: `src/cratekit/write/row_defaults.py`
- Source: `u115.json`, row `F9_unreadable_file_dropped_silently`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 5 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_file_on_another_volume_than_the_bound_is_left_and_names_why`
  - `tests/test_repair_rows.py::test_a_path_that_does_not_resolve_leaves_the_row_and_names_why`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_plan_lists_each_live_row_missing_a_default_with_exactly_its_null_columns`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
            if inode is None:
                unrenumbered.append(
```

New text:

```
            if False:
                unrenumbered.append(
```

### `r923.N14_verb_writes_on_abort`

The verb proceeds to write whatever the gate answered

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N14_verb_writes_on_abort`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 7 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_an_abort_writes_nothing`
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`
  - `tests/test_repair_rows.py::test_rekordbox_running_refuses_at_the_apply_and_writes_nothing`
  - `tests/test_repair_rows.py::test_the_gate_takes_no_inline_answer`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    if ctx.gate.require(spec, plan=data, context=_facts(plan)) != "apply":
```

New text:

```
    if False:
```

### `r923.N15_verb_writes_empty_plan`

An empty plan opens the database to write instead of ending as a no op

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N15_verb_writes_empty_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_library_with_no_row_missing_a_default_still_asks_and_then_writes_nothing`
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`

Old text:

```
    if not plan.items:
```

New text:

```
    if False:
```

### `r923.N16_ack_not_read`

The verb no longer reads the backup acknowledgment before the plan and the gate

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N16_ack_not_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
    session.assert_backup_acknowledged(cfg)

```

New text:

```
(empty)
```

### `r923.N17_write_handle_not_closed`

The write handle no longer requires rekordbox closed at open

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `r923.json`, row `N17_write_handle_not_closed`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_rekordbox_running_refuses_at_the_apply_and_writes_nothing`

Old text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
```

New text:

```
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=False, cfg=cfg)
```

### `u115.F18_undecidable_unsaid`

The gate and the envelope say nothing when the volume's counter has passed the binding's range

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `u115.json`, row `F18_undecidable_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 1 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_past_the_bindings_range_the_gate_says_why_no_id_is_renumbered`

Old text:

```
    if plan.undecidable:
        notes.append(_undecidable(plan))
```

New text:

```
    if False:
        notes.append(_undecidable(plan))
```

### `u115.F19_unrenumbered_unsaid`

The envelope says nothing about the rows left with a random id because their file could not be read

- File: `src/cratekit/write/row_defaults_cli.py`
- Source: `u115.json`, row `F19_unrenumbered_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 53 against a baseline of 53
- Kills: 2 (killed)
- Killed:
  - `tests/test_repair_rows.py::test_a_row_whose_file_is_gone_is_named_on_a_run_that_writes_nothing`
  - `tests/test_repair_rows.py::test_the_two_acts_fill_every_null_default_and_move_no_other_column`

Old text:

```
    if plan.unrenumbered:
        notes.append(_unrenumbered(plan))
```

New text:

```
    if False:
        notes.append(_unrenumbered(plan))
```

### `r289-a.A1_appledouble_gone`

Drop the AppleDouble skip, so a sidecar is walked as a track

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A1_appledouble_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_the_walk_skips_the_appledouble_sidecar_beside_a_real_track`

Old text:

```
        and not path.name.startswith(APPLEDOUBLE_PREFIX)
```

New text:

```
        and True
```

### `r289-a.A2_appledouble_one_dot`

Widen the sidecar prefix to a bare dot, the defect the review caught

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A2_appledouble_one_dot`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it`

Old text:

```
APPLEDOUBLE_PREFIX = "._"
```

New text:

```
APPLEDOUBLE_PREFIX = "."
```

### `r289-a.A3_staging_dirs_gone`

Drop the staging tree skip, so a partial download is queued as a track

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A3_staging_dirs_gone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_real_track_beside_the_staging_tree_is_still_queued`
  - `tests/test_tag_workers.py::test_tagging_the_download_root_queues_nothing_from_the_acquisition_staging_tree`
  - `tests/test_tagging_engine.py::test_the_master_staging_tree_is_skipped_too`
  - `tests/test_tagging_engine.py::test_the_walk_does_not_descend_into_the_acquisition_staging_tree`

Old text:

```
        and not SKIPPED_DIRNAMES.intersection(path.relative_to(root).parts[:-1])
```

New text:

```
        and True
```

### `r289-a.A4_staging_dirs_acquire_only`

Forget the master staging tree, keeping the acquisition one

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A4_staging_dirs_acquire_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_the_master_staging_tree_is_skipped_too`
  - `tests/test_tagging_engine.py::test_the_skipped_dirnames_are_the_two_constants_that_own_them`

Old text:

```
SKIPPED_DIRNAMES: frozenset[str] = frozenset(
    {".cratekit-acquire-staging", ".cratekit-master-staging"}
)
```

New text:

```
SKIPPED_DIRNAMES: frozenset[str] = frozenset({".cratekit-acquire-staging"})
```

### `r289-a.A5_staging_dirs_absolute`

Match the staging names on the absolute path, not relative to the root

- File: `src/cratekit/tagging/tag.py`
- Source: `r289-a.json`, row `A5_staging_dirs_absolute`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_root_that_is_itself_a_staging_tree_is_still_walked`

Old text:

```
        and not SKIPPED_DIRNAMES.intersection(path.relative_to(root).parts[:-1])
```

New text:

```
        and not SKIPPED_DIRNAMES.intersection(path.parts)
```

### `r650-a.B3_engine_drops_the_flag_on_the_write`

The one branch that wrote a word stops recording where the word came from

- File: `src/cratekit/tagging/tag.py`
- Source: `r650-a.json`, row `B3_engine_drops_the_flag_on_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 3 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`
  - `tests/test_tag_workers.py::test_the_sweep_names_a_folders_own_name_with_its_one_answer_and_falls_back_when_the_copy_breaks`
  - `tests/test_tagging_engine.py::test_a_word_the_taxonomy_does_not_know_is_written_and_reported`

Old text:

```
        off_taxonomy = hit.off_taxonomy
```

New text:

```
        off_taxonomy = False
```

### `r650-a.B4_engine_leaks_the_flag_onto_a_skip`

The flag is read off the hit for every file, so a has-genre skip claims a word this run did not write

- File: `src/cratekit/tagging/tag.py`
- Source: `r650-a.json`, row `B4_engine_leaks_the_flag_onto_a_skip`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_file_this_engine_did_not_tag_is_never_off_taxonomy`

Old text:

```
    written: str | None = None
    off_taxonomy = False
```

New text:

```
    written: str | None = None
    off_taxonomy = bool(hit and hit.off_taxonomy)
```

### `u56-catalogue-searcher-and-tag-workers.R14_walk_unsorted`

The walk stops sorting, so an enqueue and a later walk disagree about ordinal order and one file's report is filed under another's name

- File: `src/cratekit/tagging/tag.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R14_walk_unsorted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 7 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_tag_folder_by_hand_queues_and_drives_its_sweep_to_succeeded_in_one_call`
  - `tests/test_tag_workers.py::test_the_report_names_each_off_taxonomy_genre_and_the_sweep_warns`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in root.rglob("*")
```

### `u56-catalogue-searcher-and-tag-workers.R15_walk_not_recursive`

The walk stops recursing, so a folder of subfolders queues nothing and reports the honest zero over a library

- File: `src/cratekit/tagging/tag.py`
- Source: `u56-catalogue-searcher-and-tag-workers.json`, row `R15_walk_not_recursive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 4 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_file_in_a_subfolder_keeps_its_relative_identifier_and_is_still_tagged`
  - `tests/test_tagging_engine.py::test_a_title_that_opens_with_dots_is_walked_and_so_is_the_album_holding_it`
  - `tests/test_tagging_engine.py::test_the_skip_does_not_stop_the_walk_recursing`
  - `tests/test_tagging_engine.py::test_the_walk_recurses_and_comes_back_sorted`

Old text:

```
        for path in sorted(root.rglob("*"))
```

New text:

```
        for path in sorted(root.glob("*"))
```

### `u85-a.A11_failed_write_is_error`

A write the file refused is reported embedded

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A11_failed_write_is_error`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_picture_the_file_will_not_take_is_an_error_and_the_genre_stands`

Old text:

```
    if not written:
```

New text:

```
    if False:
```

### `u85-a.A13_art_only_refusal_absorbed`

A refusal on a tagged file searched only for art fails the item again

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A13_art_only_refusal_absorbed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 2 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-parse-broken]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-unreachable]`

Old text:

```
    except CratekitError as exc:
```

New text:

```
    except ZeroDivisionError as exc:
```

### `u85-a.A1_search_skipped_only_with_both`

A tagged file skips the search whatever its art, so a tagged file with no picture is never given one

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A1_search_skipped_only_with_both`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_an_interrupted_sweep_names_its_job_command_and_that_command_finishes_it`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tag_workers.py::test_the_skip_reason_reaches_the_report_and_not_only_the_artifact`
  - `tests/test_tagging_engine.py::test_a_file_this_engine_did_not_tag_is_never_off_taxonomy`
  - `tests/test_tagging_engine.py::test_a_file_with_a_genre_and_no_art_gets_art_and_its_genre_is_untouched`
  - `tests/test_tagging_engine.py::test_a_tagged_file_nobody_carries_is_still_has_genre_and_art_unavailable`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-parse-broken]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_searched_only_for_art_is_not_failed_by_a_refusal[catalogue-unreachable]`
  - `tests/test_tagging_engine.py::test_a_tagged_file_whose_searcher_breaks_outright_still_raises`
  - `tests/test_tagging_engine.py::test_the_folder_pass_produces_exactly_what_the_per_file_calls_produce`

Old text:

```
if existing and settled is not None:
```

New text:

```
if existing:
```

### `u85-a.A2_any_picture_settles`

A file carrying a picture is treated as needing one, so art it already has is re-downloaded over

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A2_any_picture_settles`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 8 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_folder_of_three_tags_the_two_with_no_genre_and_leaves_the_third`
  - `tests/test_tag_workers.py::test_a_sweep_discogs_decides_asks_beatport_only_for_missing_covers_and_counts_discogs_first`
  - `tests/test_tag_workers.py::test_new_art_reaches_the_file_the_artifact_and_the_summary`
  - `tests/test_tagging_engine.py::test_a_file_that_already_carries_a_genre_is_skipped_and_never_overwritten`
  - `tests/test_tagging_engine.py::test_a_file_that_already_has_a_genre_is_still_repaired`
  - `tests/test_tagging_engine.py::test_a_tagged_file_with_zeroed_art_is_repaired_and_never_fetched`
  - `tests/test_tagging_engine.py::test_an_untagged_file_with_zeroed_art_gets_its_genre_and_keeps_its_picture`
  - `tests/test_tagging_engine.py::test_the_folder_pass_asks_once_per_untagged_file`

Old text:

```
    if pictures:
        return {"art_fetch": ART_PRESENT
```

New text:

```
    if False:
        return {"art_fetch": ART_PRESENT
```

### `u85-a.A3_unreadable_is_unchecked`

A file whose pictures cannot be read raises out of the item instead of reporting unchecked

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A3_unreadable_is_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_file_whose_pictures_cannot_be_read_is_unchecked_and_not_fetched`

Old text:

```
except (tags.UnsupportedContainer, art.UnreadableFile) as exc:
```

New text:

```
except tags.UnsupportedContainer as exc:
```

### `u85-a.A5_no_url_guard`

A hit naming no picture is still fetched, with an empty URL

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A5_no_url_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 22663 against a baseline of 22663
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_published_genre.py::test_a_picture_from_beatports_row_is_reported_as_beatports`

Old text:

```
    if not hit.art_url:
```

New text:

```
    if False:
```

### `u85-a.A6_no_fetch_guard`

No fetch supplied calls None and reports the TypeError as a fetch failure

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A6_no_fetch_guard`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_no_fetch_supplied_is_unavailable_rather_than_a_silent_skip`

Old text:

```
    if fetch_image is None:
```

New text:

```
    if False:
```

### `u85-a.A7_fetch_raise_is_a_decline`

A fetch that raises fails the item instead of reporting art unavailable

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A7_fetch_raise_is_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_fetch_that_raises_is_unavailable_and_never_fails_the_item`

Old text:

```
    except Exception as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
```

New text:

```
    except ZeroDivisionError as exc:  # noqa: BLE001
        return result(ART_UNAVAILABLE, f"the picture at {url} could not be fetched: {exc}")
```

### `u85-a.A9_not_a_picture_is_a_decline`

Bytes that are not an image fail the item instead of reporting art unavailable

- File: `src/cratekit/tagging/tag.py`
- Source: `u85-a.json`, row `A9_not_a_picture_is_a_decline`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_genre_retag.py`, `tests/test_queued_resume_contract.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`
- Collected: 242 against a baseline of 242
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_bytes_that_are_not_a_picture_are_unavailable_and_nothing_is_embedded`

Old text:

```
    except art.ArtError as exc:
        return result(ART_UNAVAILABLE, f"what
```

New text:

```
    except ZeroDivisionError as exc:
        return result(ART_UNAVAILABLE, f"what
```

### `r1499.L01_go_arrival_after_tail`

label sync: no check after the go's name apply, so an arrival is planned into the go's landing

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L01_go_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`

Old text:

```
        if changed is not None:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

New text:

```
        if False:
            raise tail.Stop(tail.LAND, changed, continues=False)
```

### `r1499.L02_go_kept_after_arrival`

_kept: the go keeps its record although something arrived

- File: `src/cratekit/cli/label_sync.py`
- Source: `r1499.json`, row `L02_go_kept_after_arrival`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_a_gos_landing_is_planned_refuses_it`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_a_gos_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_gos_tail_that_fails_while_a_download_arrives_says_its_record_was_not_kept`

Old text:

```
    if changed is not None:
        return [_unkept(folder, job, _changed_said(changed))]
```

New text:

```
    if False:
        return [_unkept(folder, job, _changed_said(changed))]
```

### `r1499.S01_download_reading`

sync land: the reading before the download never refuses, so a pass downloads beside a go's download at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S01_download_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 12 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_file_the_passes_tail_left_and_then_changed_is_not_its_own`
  - `tests/test_sync_land_beside.py::test_a_label_gos_download_at_its_landings_gate_renamed_refuses_the_pass_before_it_downloads`
  - `tests/test_sync_land_beside.py::test_a_pass_whose_landing_is_proven_is_not_named`
  - `tests/test_sync_land_beside.py::test_a_plain_download_beside_the_pass_refuses_naming_it`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_earlier_pass_renamed_at_its_gate_is_named_by_its_pass`
  - `tests/test_sync_land_beside.py::test_an_earlier_passes_unlanded_download_refuses_a_new_pass_naming_how_it_lands`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`
  - `tests/test_sync_land_staged.py::test_a_pass_whose_every_missing_track_is_staged_downloads_nothing_and_refuses`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_an_unlanded_first_refuses_before_any_download_is_refused`
  - `tests/test_sync_land_staged.py::test_a_second_pass_beside_the_unlanded_first_lists_only_what_it_did_not_stage_and_refuses`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == DOWNLOAD:
        return settled

```

### `r1499.S02_tail_reading`

sync land: the reading before the tail never refuses, so a download finished during the pass's download is tailed and landed with it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S02_tail_reading`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_gos_download_arriving_while_the_pass_downloads_refuses_its_tail`

Old text:

```
    if not found:
        return settled

```

New text:

```
    if not found or step == TAG:
        return settled

```

### `r1499.S03_arrival_after_tail`

sync land: no check after name apply, so a download finished during the tail is renamed and planned into the landing

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S03_arrival_after_tail`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_a_person_put_there_while_the_tail_ran_refuses_its_landing`

Old text:

```
            if changed is not None:
                # NOT CONTINUED
```

New text:

```
            if False:
                # NOT CONTINUED
```

### `r1499.S04_arrival_after_plan`

sync land: a landing planned over an arrival is handed on at its gate

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S04_arrival_after_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`

Old text:

```
                changed = _arrived(cfg, staging, name, before)
                if changed is None:
                    raise

```

New text:

```
                changed = None
                if changed is None:
                    raise

```

### `r1499.S05_keep_after_arrival`

_keep: keep the record although something arrived, so the arrival reads as the pass's own on its next run

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S05_keep_after_arrival`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_as_the_landing_is_planned_refuses_the_planned_landing`
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if why is not None:
        report.warnings.append(
```

New text:

```
    if False:
        report.warnings.append(
```

### `r1499.S06_keep_called`

sync land: keep no record at the tail's stop, so the pass continued refuses beside its own renamed tracks

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S06_keep_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 7 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`
  - `tests/test_sync_land_beside.py::test_the_record_is_kept_under_the_pass_at_each_tail_stop`

Old text:

```
            _keep(report, cfg, staging, name, before)
```

New text:

```
            pass
```

### `r1499.S07_kept_read`

_alone: read no kept record, so the pass's own renamed tracks are beside it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S07_kept_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_file_put_there_since_the_tail_stopped_is_not_the_passes_own`
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[failed]`
  - `tests/test_sync_land_beside.py::test_the_passes_own_renamed_tracks_after_its_tail_stopped_run_on[gate]`

Old text:

```
                kept=staged.kept(staged.pass_record(cfg, name)),
```

New text:

```
                kept=frozenset(),
```

### `r1499.S08_own_pass_proof`

_alone: never read the pass's landing proof, so a landed pass's record still reads files as its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S08_own_pass_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`
  - `tests/test_sync_land_beside.py::test_once_the_passes_landing_is_proven_its_record_reads_nothing_as_its_own`

Old text:

```
                own_pass=name,
                origin=_ORIGIN,
```

New text:

```
                own_pass=None,
                origin=_ORIGIN,
```

### `r1499.S09_own_library`

_own_downloads: a download of another library over the pass's list is its own

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S09_own_library`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_passes_own_downloads_are_this_librarys_over_its_own_list_by_name`

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name
```

### `r1499.S10_own_by_list`

_own_downloads: no download is the pass's own, so its own fresh tracks refuse it

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S10_own_by_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 66 (killed)
- Killed:
  - `tests/test_sync_land.py::test_a_cancelled_download_over_the_same_list_is_not_reused`
  - `tests/test_sync_land.py::test_a_continued_pass_drives_the_download_it_queued_and_queues_no_second`
  - `tests/test_sync_land.py::test_a_continued_pass_never_drives_a_cancelled_job_and_lists_the_rest`
  - `tests/test_sync_land.py::test_a_continued_pass_over_an_open_intake_job_drives_it_first`
  - `tests/test_sync_land.py::test_a_continued_pass_refused_while_rekordbox_runs_names_the_way_back`
  - `tests/test_sync_land.py::test_a_continued_pass_retries_a_download_that_failed_transiently`
  - `tests/test_sync_land.py::test_a_failed_tail_step_plans_no_landing_and_names_the_continuation`
  - `tests/test_sync_land.py::test_a_fresh_pass_never_reuses_another_lists_download_job`
  - `tests/test_sync_land.py::test_a_gate_any_earlier_step_stops_at_is_the_steps_own_not_the_passes`
  - `tests/test_sync_land.py::test_a_job_command_that_stops_at_a_gate_is_that_commands_gate`
  - `tests/test_sync_land.py::test_a_landing_that_needs_the_backup_acknowledgment_stops_without_minting_one`
  - `tests/test_sync_land.py::test_a_name_apply_refusal_ends_the_pass_before_the_landing`
  - `tests/test_sync_land.py::test_a_pass_continued_by_its_land_run_id_reaches_the_same_jobs_as_by_its_pass_id`
  - `tests/test_sync_land.py::test_a_pass_queued_by_hand_and_never_driven_is_the_one_this_verb_takes`
  - `tests/test_sync_land.py::test_a_pass_whose_vocal_model_can_score_says_so_and_asks_nothing`
  - ... and 51 more, see the JSON sidecar

Old text:

```
        if staged.pass_of(job) == name and job.library_id == cfg.library.volume_id
```

New text:

```
        if staged.pass_of(job) == name + '-' and job.library_id == cfg.library.volume_id
```

### `r1499.S11_unreadable_refuses`

_alone: a refusal of the reading (an unlistable folder, an unreadable root) reads as nothing beside

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S11_unreadable_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_an_unreadable_library_root_refuses_over_the_passes_renamed_tracks`

Old text:

```
    except CratekitError as exc:
        raise _Stop(step, exc) from None
    except OSError
```

New text:

```
    except CratekitError:
        return staged.Settled(frozenset(), 0)
    except OSError
```

### `r1499.S12_warnings_in_refusal`

_with_warnings: a refusal drops the pass's warnings

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S12_warnings_in_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_download_finished_while_the_passes_tail_runs_refuses_its_landing`

Old text:

```
    if report.warnings:
        data["warnings"]
```

New text:

```
    if False:
        data["warnings"]
```

### `r1499.S13_own_unnamed_step`

_own_unnamed: never name the landing under the pass for files no download names

- File: `src/cratekit/cli/sync_land.py`
- Source: `r1499.json`, row `S13_own_unnamed_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_land_beside.py`, `tests/test_sync_land.py`, `tests/test_sync_land_staged.py`, `tests/test_label_sync_go.py`, `tests/test_label_sync.py`, `tests/test_sync_land_mirror_downloads.py`
- Collected: 324 against a baseline of 324
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_land_beside.py::test_a_record_that_cannot_be_kept_is_a_warning_and_the_next_run_refuses`

Old text:

```
    if not (found.unnamed and own):
        return ()
```

New text:

```
    if True:
        return ()
```

