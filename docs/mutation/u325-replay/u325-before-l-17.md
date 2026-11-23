# Mutation table: u325-before-l-17

Measured by `scripts/mutate.py` on 2026-11-22 23:45 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 112.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:15 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 31, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r382.M16_parser_moved_lowercase` | `src/cratekit/label/catalogue.py` | maintainer | 10 file(s) | 891 | 2 | killed |
| `u155.W2_destination` | `src/cratekit/write/routing_pass.py` | user | 13 file(s) | 886 | 5 | killed |
| `r679-b.D5_missing_per_row_gate_on_question_alone` | `src/cratekit/intake/missing_cli.py` | user | 3 file(s) | 879 | 1 | killed |
| `r1289.M10_warning_ready_filter` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 1 | killed |
| `r1289.M11_warning_absent` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M12_warning_promise` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `r1289.M13_warning_names` | `src/cratekit/sync/cli.py` | user | 2 file(s) | 146 | 2 | killed |
| `u110-c.C1_apply_playlist` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 262 | 9 | killed |
| `u110-c.C7_intake_lock_prefix` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 262 | 19 | killed |
| `u110-c.C8_plain_dot` | `src/cratekit/intake/landing.py` | user | 7 file(s) | 262 | 3 | killed |
| `u261.A1_account_forget_keeps_the_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 28 | killed |
| `u261.A2_account_reuse_ignores_the_hold` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 3 | killed |
| `u261.A3_account_records_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 5 | killed |
| `u261.A4_refusal_drops_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 1 | killed |
| `u128-b.N1_native_owned_unwritten` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 4 | killed |
| `u128-b.N2_native_record_no_pass` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 2 | killed |
| `u128-b.N4_native_dropped_left_lost` | `src/cratekit/intake/native.py` | user | 7 file(s) | 260 | 1 | killed |
| `u208.M19_adapter_never_records_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 5 | killed |
| `u208.M20_adapter_stale_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 1 | killed |
| `u208.M21_adapter_every_choice_a_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 1 | killed |
| `u208.M22_adapter_hearts_half` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 1 | killed |
| `r1255.S3_log_file_absent` | `src/cratekit/core/session.py` | user | 2 file(s) | 438 | 1 | killed |
| `r1255.S4_under_a_file_unread` | `src/cratekit/core/session.py` | user | 2 file(s) | 438 | 1 | killed |
| `r572.L1_local_track_drop_album` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `r572.S1_album_not_read` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 3 | killed |
| `r879-b.T1_one_track_never_asked_to_agree` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 236 | 1 | killed |
| `r677.E1_export_asked_before_the_library` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 235 | 102 | killed |
| `r677.E2_library_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 235 | 5 | killed |
| `r677.E3_intake_file_check_dropped` | `src/cratekit/intake/landing.py` | user | 5 file(s) | 235 | 4 | killed |
| `u156.L23_label_beside_manifest` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 117 | 2 | killed |
| `u156.L18_digest_native` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 5 | killed |
| `u156.L19_write_called` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 21 | killed |
| `u156.L20_recorded` | `src/cratekit/intake/native.py` | user | 2 file(s) | 117 | 3 | killed |
| `u169.N1_relative_read_against_cwd` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N2_empty_root_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u169.N3_missing_folder_accepted` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 6 | killed |
| `u169.N4_name_apply_bypasses` | `src/cratekit/write/naming_cli.py` | user | 2 file(s) | 113 | 2 | killed |
| `u147-c.M14_made_in_mirror` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 1 | killed |
| `u147-c.M15_malformed_mirrors_read` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 1 | killed |
| `u147-c.M16_folder_made_twice` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 2 | killed |
| `u147-c.M17_playlist_made_twice` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 5 | killed |
| `u147-c.M19_sweep_handoff` | `src/cratekit/sync/cli.py` | user | 1 file(s) | 35 | 1 | killed |
| `r837-a.A7_reserve_reuses_recorded` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 406 | 1 | killed |
| `r837-a.A8_load_carries_sets` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 406 | 20 | killed |
| `r1418.F7_composite_ordering_start_unread` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 20 | killed |
| `r1434.S2_positions_compare_every_track_listed` | `src/cratekit/sync/pair_stopped.py` | user | 10 file(s) | 394 | 2 | killed |
| `u40-author-full.F4_tombstone_indexed` | `src/cratekit/write/trees.py` | user | 7 file(s) | 753 | 3 | killed |
| `u27-reports-round-3-fixes.F4_absent_flag_never_set` | `src/cratekit/deletion/trash.py` | user | 2 file(s) | 744 | 1 | killed |
| `u278.M24_label_sync_not_narrowed` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `u278.M25_sweep_never_refuses` | `src/cratekit/label/sync_cli.py` | user | 4 file(s) | 381 | 1 | killed |
| `r1255.R3_rotation_warning_gate` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 89 | 3 | killed |
| `r1255.R4_rotation_warning_wording` | `src/cratekit/intake/rotate_cli.py` | user | 3 file(s) | 89 | 2 | killed |
| `r1255.R1_rotation_unlisted_from_scan` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 89 | 2 | killed |
| `r1255.R2_plan_carries_unlisted` | `src/cratekit/intake/rotate.py` | user | 3 file(s) | 89 | 1 | killed |
| `r1305.A1_account_name_on_any_link` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 195 | 1 | killed |
| `r1305.A2_account_status_declared_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 195 | 6 | killed |
| `r1305.A4_account_reads_its_own_link_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 195 | 7 | killed |
| `u108-c.G21_listing_skips_already` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 368 | 2 | killed |
| `u108-c.G22_listing_excuse_applies` | `src/cratekit/label/approved_cli.py` | user | 4 file(s) | 368 | 1 | killed |
| `u82-a.A1_stat_oserror_is_the_refusal` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 4 | killed |
| `u82-a.A2_a_folder_is_not_a_file` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 1 | killed |
| `u82-a.A3_an_empty_file_is_not_proof` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 184 | 2 | killed |
| `u46-author.M1_no_items_enqueued` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 17 | killed |
| `u46-round-2.M2_resume_does_not_drive` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 15 | killed |
| `u46-round-2.M6_staging_not_cleared` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 2 | killed |
| `u46-round-2.M7B_engine_refusal_swallowed` | `src/cratekit/master/cli.py` | user | 2 file(s) | 75 | 23 | killed |
| `r835-a.L1_load_carries_the_label_map` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 350 | 28 | killed |
| `r835-a.L3_recorded_year_never_created_again` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 350 | 4 | killed |
| `u128-b.B1_engine_stale_unchecked` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 344 | 1 | killed |
| `u128-b.B2_foreign_host_indexed` | `src/cratekit/intake/landing.py` | user | 10 file(s) | 344 | 1 | killed |
| `u192.T1_typed_label_on_queue` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T2_queue_warnings_lost` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 1 | killed |
| `u192.T3_resume_label_unsaid` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 166 | 2 | killed |
| `u246.S5_inspiration_held_empty` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 331 | 9 | killed |
| `u246.S6_inspiration_planned_live` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 331 | 1 | killed |
| `r501-d.R2_settled_is_not_imported` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 329 | 1 | killed |
| `r501-d.R3_pass_is_proof` | `src/cratekit/write/routing_cli.py` | user | 3 file(s) | 329 | 1 | killed |
| `u211.W4_probe_wrapped_at_commit` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 326 | 2 | killed |
| `u211.W5_probe_wrapped_at_open` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 326 | 2 | killed |
| `u221.R12_hold_not_written` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 153 | 18 | killed |

## Row definitions

### `r382.M16_parser_moved_lowercase`

The moved parser keeps a bare identifier's case, checking the move kept its tests

- File: `src/cratekit/label/catalogue.py`
- Source: `r382.json`, row `M16_parser_moved_lowercase`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/intake/test_workers.py`, `tests/modules/test_labels.py`, `tests/test_incremental_sync.py`, `tests/test_intake_missing.py`, `tests/test_intake_missing_isrc.py`, `tests/test_intake_missing_search.py`, `tests/test_label_approved.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`, `tests/test_sync_all.py`
- Collected: 891 against a baseline of 891
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

### `u155.W2_destination`

destination: resolve no genre sub, so its playlist has no name

- File: `src/cratekit/write/routing_pass.py`
- Source: `u155.json`, row `W2_destination`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adopt_former_place.py`, `tests/test_adopt_jazz_folder.py`, `tests/test_adopt_move.py`, `tests/test_adopt_placements.py`, `tests/test_adopt_split_place.py`, `tests/test_adopt_vocals.py`, `tests/test_adopt_workers.py`, `tests/test_deferred_routing.py`, `tests/test_genre_sub.py`, `tests/test_intake_imported.py`, `tests/test_intake_land_filing.py`, `tests/test_rebuild.py`, `tests/test_routing_workers.py`
- Collected: 886 against a baseline of 886
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

### `r679-b.D5_missing_per_row_gate_on_question_alone`

missing pass, per row grouping: gate on the needs-review state alone while the other call site still names the predicate

- File: `src/cratekit/intake/missing_cli.py`
- Source: `r679-b.json`, row `D5_missing_per_row_gate_on_question_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_match_states.py`, `tests/intake/test_workers.py`, `tests/test_review_queue.py`
- Collected: 879 against a baseline of 879
- Kills: 1 (killed)
- Killed:
  - `tests/test_match_states.py::test_every_caller_of_adjudicate_gates_on_the_rows_that_touch_the_queue`

Old text:

```
        if match_cli.touches_the_queue(one):
```

New text:

```
        if one.state is match.MatchState.NEEDS_REVIEW:
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

### `u110-c.C1_apply_playlist`

The xml landing no longer hands its batch name to the splice, so the playlist is the intake file's stem again

- File: `src/cratekit/intake/landing.py`
- Source: `u110-c.json`, row `C1_apply_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 262 against a baseline of 262
- Kills: 9 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_label_go_landing_for_one_label_is_named_for_the_date_and_that_label`
  - `tests/test_intake_land_names.py::test_a_second_landing_the_same_day_from_the_same_source_gets_a_distinct_name`
  - `tests/test_intake_land_names.py::test_a_tidal_playlist_sync_landing_is_named_for_the_date_and_tidal_playlists`
  - `tests/test_intake_land_names.py::test_name_overrides_and_names_the_intake_file_when_no_pass_is_given`
  - `tests/test_landing.py::test_three_tagged_files_land_in_one_intake_file`
  - `tests/test_landing_labels.py::test_a_label_row_no_landed_file_matches_is_reported_by_name`
  - `tests/test_landing_labels.py::test_a_tree_the_disk_refuses_after_the_moves_is_named_and_the_file_stays`
  - `tests/test_landing_labels.py::test_the_labelled_intake_file_golden`
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
- Collected: 262 against a baseline of 262
- Kills: 19 (killed)
- Killed:
  - `tests/test_intake_land.py::test_a_landing_in_another_process_refuses_this_one_until_it_ends`
  - `tests/test_intake_land.py::test_a_landing_under_another_batch_name_lands_while_one_is_held`
  - `tests/test_intake_land.py::test_a_landing_without_a_manifest_reports_nothing_about_labels`
  - `tests/test_intake_land.py::test_a_manifest_is_on_the_gate_screen_and_its_labels_are_in_the_envelope`
  - `tests/test_intake_land.py::test_a_manifest_whose_only_row_matched_nothing_still_reports_it`
  - `tests/test_intake_land.py::test_a_recorded_apply_over_an_export_that_went_missing_is_the_engine_s_refusal`
  - `tests/test_intake_land.py::test_a_refused_file_is_a_warning_a_person_reads`
  - `tests/test_intake_land.py::test_an_answered_run_lands_the_batch_and_names_the_xml_in_human_output`
  - `tests/test_intake_land.py::test_the_engine_is_handed_the_fingerprint_of_the_bytes_the_gate_compared`
  - `tests/test_intake_land.py::test_the_landed_envelope_carries_an_import_that_blocks_nothing`
  - `tests/test_intake_land.py::test_the_lock_is_held_for_the_whole_of_the_apply`
  - `tests/test_intake_land.py::test_the_lock_is_released_after_a_landing`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_export_that_is_not_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_an_intake_file_already_there]`
  - `tests/test_intake_land.py::test_the_lock_is_released_by_every_refusal_and_the_name_can_land_after[_every_target_taken]`
  - ... and 4 more, see the JSON sidecar

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
- Collected: 262 against a baseline of 262
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_names.py::test_a_pass_that_is_not_one_plain_file_name_is_refused_before_the_gate[.hidden]`
  - `tests/test_landing.py::test_a_batch_name_that_is_not_one_plain_folder_is_refused[..]`
  - `tests/test_landing.py::test_a_batch_name_that_is_not_one_plain_folder_is_refused[.hidden]`

Old text:

```
        and not text.startswith(".")

```

New text:

```
(empty)
```

### `u261.A1_account_forget_keeps_the_session`

account.forget: drop the adapter and keep the shared session, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A1_account_forget_keeps_the_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 28 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[rejected]`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[unreachable]`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_provider_failure_on_one_heart_fails_that_item_and_no_other`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_second_export_finds_its_playlist_and_neither_creates_nor_sets_visibility`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_matches_through_the_isrc_the_file_carries`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_login_that_failed_holds_nothing_and_is_asked_again[rejected]`
  - `tests/test_provider_session_hold.py::test_a_login_that_failed_holds_nothing_and_is_asked_again[unreachable]`
  - ... and 13 more, see the JSON sidecar

Old text:

```
    _OPENED_OVER = None
    provider_session.forget()
```

New text:

```
    _OPENED_OVER = None
```

### `u261.A2_account_reuse_ignores_the_hold`

account.resolve: hand out the held adapter whatever became of its session, so a client the catalogue saw refused is reused by the account

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A2_account_reuse_ignores_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
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

### `u261.A3_account_records_no_session`

account.resolve: record no session under the adapter, so the adapter is opened afresh on every resolve and the one login per process is lost

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A3_account_records_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_process_resolving_both_seams_validates_the_session_once`
  - `tests/test_provider_session_hold.py::test_a_replaced_session_the_provider_rejects_leaves_no_seam_the_old_client`
  - `tests/test_provider_session_hold.py::test_an_old_clients_refusal_on_the_account_keeps_the_session_logged_in_since`

Old text:

```
    _OPENED_OVER = provider_session.held()
    return opened
```

New text:

```
    _OPENED_OVER = None
    return opened
```

### `u261.A4_refusal_drops_no_session`

account._forget_refused: drop the adapter and keep the shared session it was built over, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A4_refusal_drops_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_session_hold.py::test_a_401_on_the_account_drops_the_shared_client_and_the_catalogue_logs_in_again`

Old text:

```
    else:
        provider_session.drop(over)
```

New text:

```
    else:
        pass
```

### `u128-b.N1_native_owned_unwritten`

The native commit joins no owned row to its playlist, the new rows alone

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N1_native_owned_unwritten`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 4 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_of_three_owned_and_two_new_lands_all_five_in_account_order`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_is_read_from_the_record_of_this_pass_alone`
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_an_owned_track_in_two_account_playlists_is_in_both`

Old text:

```
                        member.content_id
                        if member.target is None
```

New text:

```
                        ""
                        if member.target is None
```

### `u128-b.N2_native_record_no_pass`

The native landing's record names no pass, so a rerun cannot find what it mirrored

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N2_native_record_no_pass`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_rerun_of_the_same_pass_adds_nothing_twice`
  - `tests/test_intake_land_account_playlists_native.py::test_the_record_names_each_account_playlist_by_identifier`

Old text:

```
                ingest.INBOX_PASS_KEY: plan.pass_name or "",
```

New text:

```
                ingest.INBOX_PASS_KEY: "",
```

### `u128-b.N4_native_dropped_left_lost`

A native playlist holding nothing writable drops its left rows

- File: `src/cratekit/intake/native.py`
- Source: `u128-b.json`, row `N4_native_dropped_left_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_rotate.py`, `tests/test_inbox_rotate_account_playlists.py`, `tests/test_intake_land_account_playlists_native.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_sync_mark.py`
- Collected: 260 against a baseline of 260
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists_native.py::test_a_playlist_whose_only_file_is_unsupported_still_names_it_as_left`

Old text:

```
            dropped.extend((one.name, row) for row in left)
```

New text:

```
            pass
```

### `u208.M19_adapter_never_records_tie`

match_track: never record a broken tie

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M19_adapter_never_records_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`
  - `tests/test_sync_pair_tie.py::test_the_gate_names_how_many_rows_a_broken_tie_matched`
  - `tests/test_sync_pair_tie.py::test_two_hearted_releases_take_the_lower_hearted_one`

Old text:

```
                    elif tied:
                        self._ties.add(key)
```

New text:

```
                    elif False:
                        self._ties.add(key)
```

### `u208.M20_adapter_stale_tie`

match_track: keep the last match's tie flag across a later match of the same row

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M20_adapter_stale_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
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

### `u208.M21_adapter_every_choice_a_tie`

_among: call every any_agreeing choice a broken tie, an album naming one included

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M21_adapter_every_choice_a_tie`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`

Old text:

```
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
```

New text:

```
            return _lowest(narrowed), "", True
```

### `u208.M22_adapter_hearts_half`

_among: drop the hearts half of the tie flag, so two hearts the album narrows to one are not a tie

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u208.json`, row `M22_adapter_hearts_half`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 132 against a baseline of 132
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`

Old text:

```
            return _lowest(narrowed), "", bool(hearted) or len(narrowed) > 1
```

New text:

```
            return _lowest(narrowed), "", len(narrowed) > 1
```

### `r1255.S3_log_file_absent`

_listed: read a log path that is itself a file as not there, so it is no record

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S3_log_file_absent`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 438 against a baseline of 438
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_path_that_is_a_file_is_there_and_unread`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        return None
```

### `r1255.S4_under_a_file_unread`

_listed: read a log under a file as there and refused, rather than not there

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S4_under_a_file_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_doctor.py`
- Collected: 438 against a baseline of 438
- Kills: 1 (killed)
- Killed:
  - `tests/test_session_log_unlisted.py::test_a_log_under_a_file_is_not_there`

Old text:

```
        if os.path.lexists(directory):
            raise
        return None
```

New text:

```
        raise
```

### `r572.L1_local_track_drop_album`

local_tracks stops carrying the file's album

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `L1_local_track_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_local_tracks_carries_the_files_album_to_the_export_plan`

Old text:

```
            isrc=found.isrc,
            album=found.album,
            release_title=release_title(entry, template=template),
        )
```

New text:

```
            isrc=found.isrc,
            release_title=release_title(entry, template=template),
        )
```

### `r572.S1_album_not_read`

file_identity drops the album it read

- File: `src/cratekit/modules/outbound/source.py`
- Source: `r572.json`, row `S1_album_not_read`
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
        album=str(read["album"] or "").strip(),
```

New text:

```
        album="",
```

### `r879-b.T1_one_track_never_asked_to_agree`

TidalAccount.match_track: return one track under a code whether or not agree is asked

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r879-b.json`, row `T1_one_track_never_asked_to_agree`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_code_asked_to_agree_lists_its_one_track_only_when_it_is_the_row`

Old text:

```
                if len(tracks) == 1 and not agree:
```

New text:

```
                if len(tracks) == 1:
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

### `u156.L23_label_beside_manifest`

_label_flag: accept --label beside --manifest, so one of two answers silently wins

- File: `src/cratekit/intake/land_cli.py`
- Source: `u156.json`, row `L23_label_beside_manifest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 2 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_label_beside_a_manifest_is_refused_before_the_gate`
  - `tests/test_intake_land_labels_native.py::test_label_from_tags_beside_another_label_source_is_refused_before_the_gate[--manifest]`

Old text:

```
    if manifest is not None:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest
```

New text:

```
    if False:
        raise refuse(
            "intake-list-unusable",
            f"{flag} and --manifest
```

### `u156.L18_digest_native`

native.identity: leave the label plan out of the landing's digest

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L18_digest_native`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 5 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_year_playlist_made_after_the_answer_makes_the_answer_stale`
  - `tests/test_intake_land_labels_native.py::test_an_answer_given_for_one_label_is_stale_for_another`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_between_one_label_and_each_files_own`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_label`
  - `tests/test_intake_land_labels_native.py::test_the_digest_moves_with_the_manifests_bytes`

Old text:

```
    filed = {"labels": label_filing.identity(plan.labels)} if plan.labels is not None else {}
```

New text:

```
    filed = {}
```

### `u156.L19_write_called`

apply_rows: plan the labels and never write them

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L19_write_called`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 21 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_batch_of_two_labels_and_an_unregistered_seller_files_each_under_its_own`
  - `tests/test_intake_land_labels_native.py::test_a_file_left_in_staging_is_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_file_the_move_refused_is_named_and_its_year_holds_the_rest`
  - `tests/test_intake_land_labels_native.py::test_a_file_two_rows_file_in_two_years_names_both_on_its_item`
  - `tests/test_intake_land_labels_native.py::test_a_file_with_no_date_tag_is_named_on_the_screen_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_label_folder_spelled_decomposed_is_the_same_folder`
  - `tests/test_intake_land_labels_native.py::test_a_label_tag_spelled_decomposed_files_under_the_composed_folder`
  - `tests/test_intake_land_labels_native.py::test_a_labelled_file_with_no_year_is_named_with_its_label_and_filed_nowhere`
  - `tests/test_intake_land_labels_native.py::test_a_landing_with_label_records_no_provider_track`
  - `tests/test_intake_land_labels_native.py::test_a_manifest_files_its_matched_rows_under_label_and_year_and_names_the_unmatched`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_a_removed_year_playlist_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_intake_land_labels_native.py::test_a_year_whose_every_file_the_move_refused_makes_no_playlist`
  - `tests/test_intake_land_labels_native.py::test_an_existing_year_playlist_gains_members_and_loses_none`
  - `tests/test_intake_land_labels_native.py::test_an_undated_file_left_in_staging_is_not_said_to_be_in_the_intake_playlist`
  - ... and 6 more, see the JSON sidecar

Old text:

```
                labels_written = label_filing.write(db, plan.labels, by_target=by_target)
```

New text:

```
                labels_written = None
```

### `u156.L20_recorded`

_record_landing_commit: write the labels and record nothing of them on the session

- File: `src/cratekit/intake/native.py`
- Source: `u156.json`, row `L20_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_land_labels_native.py`, `tests/test_intake_land_native.py`
- Collected: 117 against a baseline of 117
- Kills: 3 (killed)
- Killed:
  - `tests/test_intake_land_labels_native.py::test_a_landing_with_label_records_no_provider_track`
  - `tests/test_intake_land_labels_native.py::test_a_puls_batch_of_three_years_lands_as_three_year_playlists_under_its_label`
  - `tests/test_intake_land_labels_native.py::test_the_record_names_each_year_filed_and_counts_it_under_the_catalogue_tree`

Old text:

```
    if labels_written is not None:
        label_filing.record_commit(record, labels_written, cfg)
```

New text:

```
    if False:
        label_filing.record_commit(record, labels_written, cfg)
```

### `u169.N1_relative_read_against_cwd`

root_path: take a relative root as it is, read under the working directory, the base's reading

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N1_relative_read_against_cwd`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_root_option.py::test_a_missing_relative_root_refuses_naming_the_path_it_tried`
  - `tests/test_root_option.py::test_a_relative_root_is_read_against_the_library_root`
  - `tests/test_root_option.py::test_name_apply_reads_a_relative_root_inside_the_library`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`
  - `tests/test_root_option.py::test_repair_apply_reads_a_relative_root_against_the_library_root`
  - `tests/test_root_option.py::test_repair_paths_scans_a_relative_root_inside_the_library`

Old text:

```
    return named if named.is_absolute() else library / named
```

New text:

```
    return named
```

### `u169.N2_empty_root_accepted`

root_path: read an empty root as the working directory instead of refusing it

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N2_empty_root_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_an_empty_root_is_refused_rather_than_read_as_the_working_directory[   ]`
  - `tests/test_root_option.py::test_an_empty_root_is_refused_rather_than_read_as_the_working_directory[]`

Old text:

```
    if not given.strip():
```

New text:

```
    if False:
```

### `u169.N3_missing_folder_accepted`

root_folder: accept a folder that is not there

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N3_missing_folder_accepted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 6 (killed)
- Killed:
  - `tests/test_root_option.py::test_a_file_where_the_folder_should_be_is_refused`
  - `tests/test_root_option.py::test_a_missing_absolute_root_refuses_naming_it`
  - `tests/test_root_option.py::test_a_missing_library_root_is_refused_when_no_root_was_given`
  - `tests/test_root_option.py::test_a_missing_relative_root_refuses_naming_the_path_it_tried`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`
  - `tests/test_root_option.py::test_repair_paths_refuses_a_root_with_no_folder`

Old text:

```
    if tried.is_dir():
        return tried
```

New text:

```
    if True:
        return tried
```

### `u169.N4_name_apply_bypasses`

name apply: read --root as the base did, bypassing the helper

- File: `src/cratekit/write/naming_cli.py`
- Source: `u169.json`, row `N4_name_apply_bypasses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_root_option.py`, `tests/test_naming_apply_cli.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_root_option.py::test_name_apply_reads_a_relative_root_inside_the_library`
  - `tests/test_root_option.py::test_name_apply_refuses_a_relative_root_with_no_folder_in_the_library`

Old text:

```
    root = root_folder(ctx.args.root, cfg, verb="name apply")
```

New text:

```
    root = Path(ctx.args.root) if ctx.args.root else Path(cfg.library.root)
```

### `u147-c.M14_made_in_mirror`

ledger._made_in: a mirrored playlist is no longer vouched for, so no track may come off it (R-836)

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M14_made_in_mirror`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`

Old text:

```
    # U147. A mirrored playlist is only ever created, never adopted.
    for record in document["mirrors"].values():
        for entry in (record.get("playlists") or {}).values():
            if str(entry.get("remote_id") or "") == wanted:
                return True

```

New text:

```
(empty)
```

### `u147-c.M15_malformed_mirrors_read`

ledger._load: a malformed mirror record is read rather than refused

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M15_malformed_mirrors_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_malformed_mirror_record_refuses_rather_than_reading_as_none`

Old text:

```
        raise _unusable(path, "mirrors must be a map of mirrored folder records")
```

New text:

```
        mirrors = {}
```

### `u147-c.M16_folder_made_twice`

ledger.reserve_mirror_folder: a recorded folder is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M16_folder_made_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        record = _mirror_entry(document, name)
        recorded = str(record.get("folder_id") or "")
        if recorded and recorded != stale:
            return recorded, False

```

New text:

```
        record = _mirror_entry(document, name)
        recorded = str(record.get("folder_id") or "")

```

### `u147-c.M17_playlist_made_twice`

ledger.reserve_mirror_playlist: a recorded playlist is not reused, so a resume makes a second

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u147-c.json`, row `M17_playlist_made_twice`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_next_run`
  - `tests/test_organize_mirror.py::test_a_removal_the_account_refuses_is_kept_named_and_the_apply_goes_on`
  - `tests/test_organize_mirror.py::test_a_track_added_by_hand_to_a_mirrored_playlist_is_removed_and_named`
  - `tests/test_organize_mirror.py::test_a_track_moved_from_med_to_high_is_added_to_one_and_removed_from_the_other`
  - `tests/test_organize_mirror.py::test_an_apply_stopped_after_the_folder_was_created_resumes_without_a_second_folder`

Old text:

```
        playlists = _mirror_entry(document, folder)["playlists"]
        recorded = str((playlists.get(name) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False

```

New text:

```
        playlists = _mirror_entry(document, folder)["playlists"]

```

### `u147-c.M19_sweep_handoff`

sync.cli: the sync source hands the sweep no mirrored playlist

- File: `src/cratekit/sync/cli.py`
- Source: `u147-c.json`, row `M19_sweep_handoff`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_sync_pass_hands_the_sweep_every_mirrored_playlist`

Old text:

```
            mirrored=mirrored,
```

New text:

```
(empty)
```

### `r837-a.A7_reserve_reuses_recorded`

ledger.reserve_set_playlist: a recorded set playlist is not reused, so the create runs again

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A7_reserve_reuses_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 406 against a baseline of 406
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`

Old text:

```
        recorded = str((document["sets"].get(name) or {}).get("remote_id") or "")
        if recorded:
```

New text:

```
        recorded = str((document["sets"].get(name) or {}).get("remote_id") or "")
        if False:
```

### `r837-a.A8_load_carries_sets`

ledger._load: the sets map is dropped on read, so every later write forgets each set playlist

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r837-a.json`, row `A8_load_carries_sets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 406 against a baseline of 406
- Kills: 20 (killed)
- Killed:
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
  - `tests/test_export_set.py::test_an_archive_with_no_landed_file_refuses_before_anything`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            for key, value in sets.items()
```

New text:

```
            for key, value in ()
```

### `r1418.F7_composite_ordering_start_unread`

what F7 holds: a stopped write with no moving step reads no start from its ordering step, so the start F7 narrows is never read

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1418.json`, row `F7_composite_ordering_start_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 20 (killed)
- Killed:
  - `tests/test_sync_pair_order.py::test_a_continue_of_a_refused_order_holds_a_reorder_made_on_the_account_since`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[all-read]`
  - `tests/test_sync_pair_settle.py::test_a_drag_to_the_top_after_a_write_that_sent_no_move_leads[t9-unread]`
  - `tests/test_sync_pair_settle.py::test_a_move_of_the_unread_track_alone_after_a_stop_that_sent_nothing_is_no_reorder`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_finish_stopped_before_its_first_send_leads`
  - `tests/test_sync_pair_settle.py::test_a_reorder_after_a_track_read_at_the_stop_turned_unread_leads`
  - `tests/test_sync_pair_settle.py::test_a_track_unread_at_the_stop_and_read_since_is_read_as_the_persons_when_moved`
  - `tests/test_sync_pair_settle.py::test_an_unread_track_moved_after_a_stop_before_the_first_send_is_kept_where_it_was_put`
  - `tests/test_sync_pair_stopped.py::test_a_write_begun_ordered_and_not_finished_is_read_back_whole`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_that_moves_again_before_it_settles_is_held_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_differing_order_waits_the_agreement_window`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_off_the_path_no_sync_read_before_is_not_read_as_the_persons`
  - `tests/test_sync_pair_stopped_order.py::test_a_move_the_person_made_on_the_account_after_a_sync_read_it_still_leads`
  - `tests/test_sync_pair_stopped_order.py::test_a_reading_that_moved_before_it_settled_starts_again`
  - `tests/test_sync_pair_stopped_order.py::test_a_released_pair_read_off_the_path_on_its_first_sync_keeps_rekordboxs_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
    begin = sent[1] if sent is not None else start
```

New text:

```
    begin = sent[1] if sent is not None else ()
```

### `r1434.S2_positions_compare_every_track_listed`

existing guard, U225: the path compares every track listed now, a track added since included, so an addition reads the account off the path

- File: `src/cratekit/sync/pair_stopped.py`
- Source: `r1434.json`, row `S2_positions_compare_every_track_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_unread.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_order.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_window_lag.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_root_order.py`, `tests/test_sync_twins.py`, `tests/test_outbound_order.py`
- Collected: 394 against a baseline of 394
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_pair_stopped.py::test_a_track_added_or_taken_off_since_is_left_out_of_the_comparison`
  - `tests/test_sync_pair_stopped.py::test_positions_counts_the_moves_that_leave_each_order_on_the_path`

Old text:

```
    common = set(current) & set(start)
```

New text:

```
    common = set(current)
```

### `u40-author-full.F4_tombstone_indexed`

First caller sample: stop dropping tombstones from the active row index, so a removed track claims its location

- File: `src/cratekit/write/trees.py`
- Source: `u40-author-full.json`, row `F4_tombstone_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deferred_routing.py`, `tests/test_deletion.py`, `tests/test_genre_retag.py`, `tests/test_rebuild.py`, `tests/test_tree_registry.py`, `tests/test_tree_writer.py`, `tests/test_xml_splice_golden.py`
- Collected: 753 against a baseline of 753
- Kills: 3 (killed)
- Killed:
  - `tests/test_genre_retag.py::test_a_soft_deleted_row_is_never_retagged`
  - `tests/test_rebuild.py::test_a_membership_pointing_at_a_soft_deleted_row_is_not_a_difference_either`
  - `tests/test_tree_writer.py::test_a_soft_deleted_row_beside_one_active_row_resolves_cleanly`

Old text:

```
    for row in rows:
        if row.deleted:
            continue
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

New text:

```
    for row in rows:
        resolved = _comparable(row.recorded, root=root, prefix_map=prefix_map)
```

### `u27-reports-round-3-fixes.F4_absent_flag_never_set`

Never mark an absent Trash as absent, so doctor cannot tell it from an unwritable one

- File: `src/cratekit/deletion/trash.py`
- Source: `u27-reports-round-3-fixes.json`, row `F4_absent_flag_never_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_deletion.py`, `tests/test_doctor.py`
- Collected: 744 against a baseline of 744
- Kills: 1 (killed)
- Killed:
  - `tests/test_doctor.py::test_the_two_probe_answers_that_made_the_false_red_are_really_different`

Old text:

```
            absent=not target.exists(),
```

New text:

```
            absent=False,
```

### `u278.M24_label_sync_not_narrowed`

label sync: ask and walk spend the reserve

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M24_label_sync_not_narrowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if not args.go:
        provider_gate.reading(
```

New text:

```
    if False:
        provider_gate.reading(
```

### `u278.M25_sweep_never_refuses`

label sync: the estimate never refuses

- File: `src/cratekit/label/sync_cli.py`
- Source: `u278.json`, row `M25_sweep_never_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_budget.py`, `tests/test_provider_gate.py`, `tests/test_label_sync.py`, `tests/test_label_sync_go.py`
- Collected: 381 against a baseline of 381
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_budget.py::test_a_sweep_whose_estimate_crosses_into_the_reserve_refuses_before_its_first_call`

Old text:

```
    if calls > left:
```

New text:

```
    if False:
```

### `r1255.R3_rotation_warning_gate`

records_warnings: never warn, so the rotation ages a batch from its playlist's date unsaid

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R3_rotation_warning_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 3 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_records_it_could_not_read_as_it_did`

Old text:

```
    if not plan.unreadable_records:
        return []
    unread = (
```

New text:

```
    if True:
        return []
    unread = (
```

### `r1255.R4_rotation_warning_wording`

records_warnings: word an unlisted log as a count of records

- File: `src/cratekit/intake/rotate_cli.py`
- Source: `r1255.json`, row `R4_rotation_warning_wording`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_warns_on_a_log_it_could_not_list`

Old text:

```
        if plan.log_unlisted
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

New text:

```
        if False
        else f"{plan.unreadable_records} session record(s) could not be read, so a "
```

### `r1255.R1_rotation_unlisted_from_scan`

landings: never read the listing off the scan, so the classifier's reason counts one record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R1_rotation_unlisted_from_scan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`
  - `tests/test_session_log_unlisted.py::test_the_rotation_reads_the_listing_from_the_scan`

Old text:

```
    unlisted = session.log_unlisted(unreadable, cfg)
```

New text:

```
    unlisted = False
```

### `r1255.R2_plan_carries_unlisted`

plan_rotation: leave the plan's log_unlisted at its default, so the warning counts a record

- File: `src/cratekit/intake/rotate.py`
- Source: `r1255.json`, row `R2_plan_carries_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`
- Collected: 89 against a baseline of 89
- Kills: 1 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_session_log_that_cannot_be_listed_is_never_read_as_no_record`

Old text:

```
        log_unlisted=found.unlisted,
```

New text:

```
        log_unlisted=False,
```

### `r1305.A1_account_name_on_any_link`

_session_refused: read the client's authentication error by name on any link, so a reset met while handling one drops the account and asks for a login

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A1_account_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 195 against a baseline of 195
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

### `r1305.A2_account_status_declared_only`

_session_refused: read a status on the declared chain only, so a session rejected mid sweep with a page is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A2_account_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 195 against a baseline of 195
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_outage_met_while_handling_a_rejected_session_is_a_wait`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_drops_the_held_account`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_an_outage_met_while_handling_a_rejected_session_is_a_wait_not_a_login`

Old text:

```
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

New text:

```
        if declared and answered_status(link) in SESSION_REFUSED_STATUSES:
```

### `r1305.A4_account_reads_its_own_link_only`

_session_refused: read the failure alone and no link of it, so a rejection the client rewraps is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A4_account_reads_its_own_link_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 195 against a baseline of 195
- Kills: 7 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rejection_the_client_rewraps_is_still_read_as_a_rejected_session`
  - `tests/test_provider_rejection_bodies.py::test_a_login_outage_met_while_handling_a_rejected_session_is_a_wait`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_drops_the_held_account`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[401-html]`
  - `tests/test_provider_rejection_bodies.py::test_a_session_rejected_mid_sweep_asks_for_a_login_whatever_the_body[403-html]`
  - `tests/test_provider_rejection_bodies.py::test_an_outage_met_while_handling_a_rejected_session_is_a_wait_not_a_login`

Old text:

```
    for link, declared in failure_links(exc):
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

New text:

```
    for link, declared in [(exc, True)]:
        if answered_status(link) in SESSION_REFUSED_STATUSES:
```

### `u108-c.G21_listing_skips_already`

approved_cli.list_releases: a track another job already holds is listed again

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G21_listing_skips_already`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 368 against a baseline of 368
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_go_killed_between_its_queue_and_its_record_never_asks_for_a_track_twice`
  - `tests/test_label_sync_go.py::test_an_answer_holding_a_release_the_provider_did_not_answer_for_is_kept_for_the_next_go`

Old text:

```
            elif str(settled.wanted.ref or "").strip() in already:
```

New text:

```
            elif False:
```

### `u108-c.G22_listing_excuse_applies`

approved_cli.list_releases: an excused failure kind still refuses an empty listing

- File: `src/cratekit/label/approved_cli.py`
- Source: `u108-c.json`, row `G22_listing_excuse_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_approved.py`, `tests/test_label_sync_go.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_landing_labels.py`
- Collected: 368 against a baseline of 368
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_sync_go.py::test_a_release_gone_from_the_provider_does_not_refuse_every_go_after_it`

Old text:

```
    unexcused = [one for one in failures if one.kind not in excuse]
```

New text:

```
    unexcused = list(failures)
```

### `u82-a.A1_stat_oserror_is_the_refusal`

require_output: stop turning an OSError out of the one stat into sync-marks-blocked, so a file gone at that moment is a bare FileNotFoundError again, which is R-398

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A1_stat_oserror_is_the_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_that_did_not_land_is_offered_again_by_the_next_pass`
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_missing_intake_file_refuses_the_verb_before_anything_is_listed`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    except OSError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

New text:

```
    except ZeroDivisionError as exc:
        raise _blocked(local_output, exc.strerror or type(exc).__name__) from exc
```

### `u82-a.A2_a_folder_is_not_a_file`

require_output: drop the regular file check, so a folder named like the intake file counts as the importable file

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A2_a_folder_is_not_a_file`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if not stat.S_ISREG(found.st_mode):
```

New text:

```
    if False:
```

### `u82-a.A3_an_empty_file_is_not_proof`

require_output: drop the empty file check, so a zero byte file lets the renames through

- File: `src/cratekit/sync/marks.py`
- Source: `u82-a.json`, row `A3_an_empty_file_is_not_proof`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_sync_all.py`
- Collected: 184 against a baseline of 184
- Kills: 2 (killed)
- Killed:
  - `tests/test_sync_all.py::test_a_mark_without_a_real_importable_file_renames_nothing`
  - `tests/test_sync_mark.py::test_a_folder_and_an_empty_file_are_not_an_importable_file`

Old text:

```
    if found.st_size == 0:
```

New text:

```
    if False:
```

### `u46-author.M1_no_items_enqueued`

Queue the recording with no item, so the driver has nothing to claim

- File: `src/cratekit/master/cli.py`
- Source: `u46-author.json`, row `M1_no_items_enqueued`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 17 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_queueing_a_recording_gives_the_driver_one_item_to_claim`
  - ... and 2 more, see the JSON sidecar

Old text:

```
            item_ids=(str(payload[SOURCE]),),
```

New text:

```
(empty)
```

### `u46-round-2.M2_resume_does_not_drive`

Report the queued job on resume without running any of it, which is the state R-198 describes

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M2_resume_does_not_drive`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 15 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_configuration_that_moved_reaches_the_person_as_a_warning_on_the_resume`
  - `tests/test_master_cli.py::test_a_handler_that_raises_an_undeclared_error_fails_the_item_not_the_driver`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`
  - `tests/test_master_cli.py::test_a_queued_recording_runs_from_pending_to_done_through_the_resume_branch`
  - `tests/test_master_cli.py::test_a_queued_split_recording_lands_as_one_master_through_the_resume`
  - `tests/test_master_cli.py::test_a_relative_recording_masters_the_same_file_when_the_resume_runs_elsewhere`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_existing_joined_master_is_refused_on_the_real_destination`
  - `tests/test_master_cli.py::test_an_existing_master_is_refused_before_the_engine_runs`
  - `tests/test_master_cli.py::test_nothing_is_created_beside_a_destination_for_a_recording_that_is_not_there`
  - `tests/test_master_cli.py::test_overwrite_reaches_the_handler_and_replaces_the_previous_master`
  - `tests/test_master_cli.py::test_the_encode_lands_in_staging_and_is_committed_rather_than_written_in_place`

Old text:

```
                _, warnings = ctx.run_job(store, job)
                job = jobs.get(store, job.job_id)
```

New text:

```
                pass
```

### `u46-round-2.M6_staging_not_cleared`

Leave a previous attempt's partial encode in the staging directory

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M6_staging_not_cleared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_seam.py::test_a_driver_killed_inside_the_real_handler_resumes_redoing_exactly_that_item`
  - `tests/test_master_cli.py::test_a_partial_file_left_in_staging_does_not_refuse_the_next_attempt`

Old text:

```
    if directory.exists():
        shutil.rmtree(directory)
```

New text:

```
(empty)
```

### `u46-round-2.M7B_engine_refusal_swallowed`

Translate the engine's encoder-failed into a generic internal defect

- File: `src/cratekit/master/cli.py`
- Source: `u46-round-2.json`, row `M7B_engine_refusal_swallowed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_seam.py`, `tests/test_master_cli.py`
- Collected: 75 against a baseline of 75
- Kills: 23 (killed)
- Killed:
  - `tests/test_master_cli.py::test_a_24_bit_and_a_32_bit_part_are_told_apart_by_codec_alone`
  - `tests/test_master_cli.py::test_a_container_the_engine_does_not_read_refuses_under_its_own_slug`
  - `tests/test_master_cli.py::test_a_corrupt_archive_copy_refuses_and_leaves_no_false_safety_copy`
  - `tests/test_master_cli.py::test_a_failed_encode_under_overwrite_says_what_the_person_is_left_holding`
  - `tests/test_master_cli.py::test_a_failing_encode_does_not_report_success`
  - `tests/test_master_cli.py::test_a_job_that_failed_on_a_missing_source_is_not_reopened_and_a_fresh_job_masters_it`
  - `tests/test_master_cli.py::test_a_missing_encoder_reports_that_refusal_rather_than_an_internal_defect`
  - `tests/test_master_cli.py::test_a_missing_part_refuses_as_missing`
  - `tests/test_master_cli.py::test_a_missing_recording_reports_the_engines_own_cause_on_the_item`
  - `tests/test_master_cli.py::test_a_part_named_twice_refuses`
  - `tests/test_master_cli.py::test_a_recording_that_is_not_there_refuses_rather_than_raising`
  - `tests/test_master_cli.py::test_an_archive_holding_different_audio_refuses_and_keeps_both`
  - `tests/test_master_cli.py::test_an_encode_that_exits_zero_and_writes_nothing_does_not_report_success`
  - `tests/test_master_cli.py::test_an_encode_that_produces_nothing_reaches_the_item_as_the_engines_own_cause`
  - `tests/test_master_cli.py::test_an_encode_that_writes_an_empty_file_does_not_report_success`
  - ... and 8 more, see the JSON sidecar

Old text:

```
            str(exc.refusal),
            exc.detail,
```

New text:

```
            "internal-error",
            "the mastering engine refused",
```

### `r835-a.L1_load_carries_the_label_map`

ledger._load: the label map is dropped on load, so any other write to the ledger forgets every label's folder and year playlists

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L1_load_carries_the_label_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 350 against a baseline of 350
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

### `r835-a.L3_recorded_year_never_created_again`

ledger.reserve_label_year: a year already recorded is created again, so a resumed build makes a second playlist for it

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `r835-a.json`, row `L3_recorded_year_never_created_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 350 against a baseline of 350
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`

Old text:

```
        recorded = str((years.get(year) or {}).get("remote_id") or "")
        if recorded:
            return recorded, False
```

New text:

```
        recorded = str((years.get(year) or {}).get("remote_id") or "")
        if False:
            return recorded, False
```

### `u128-b.B1_engine_stale_unchecked`

The bridge engine does not read the owned entries again before its first move

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B1_engine_stale_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 344 against a baseline of 344
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_the_engine_reads_the_owned_entries_again_before_the_first_move`

Old text:

```
    if now != planned:
```

New text:

```
    if False:
```

### `u128-b.B2_foreign_host_indexed`

Index an export entry whose Location names another machine, which raises out of the index

- File: `src/cratekit/intake/landing.py`
- Source: `u128-b.json`, row `B2_foreign_host_indexed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_favorites_backfill.py`, `tests/test_intake_land.py`, `tests/test_intake_land_account_playlists.py`, `tests/test_intake_land_hearts_native.py`, `tests/test_intake_land_names.py`, `tests/test_intake_land_native.py`, `tests/test_intake_writers_native.py`, `tests/test_landing.py`, `tests/test_landing_head.py`, `tests/test_landing_labels.py`
- Collected: 344 against a baseline of 344
- Kills: 1 (killed)
- Killed:
  - `tests/test_intake_land_account_playlists.py::test_an_export_entry_on_another_machine_is_no_owned_row`

Old text:

```
        try:
            locations.location_to_path(recorded)
        except locations.LocationDecodeError:
            continue
        found.append
```

New text:

```
        found.append
```

### `u192.T1_typed_label_on_queue`

tag_folder: hand the queue's own --label to the resume, so a sweep driven at its queue says its label was not applied

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T1_typed_label_on_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
```

New text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=ctx.args.label, queued=label_warnings),
```

### `u192.T2_queue_warnings_lost`

tag_folder: drop the queue's label warnings from the settled answer

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T2_queue_warnings_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_sweep_driven_at_its_queue_keeps_the_label_warning_and_never_calls_its_label_unapplied`

Old text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None, queued=label_warnings),
```

New text:

```
        lambda: _resume(ctx, cfg, job.job_id, typed_label=None),
```

### `u192.T3_resume_label_unsaid`

tag_folder --job: stop passing the typed --label, so a label typed on a resume is applied silently in the report's eyes

- File: `src/cratekit/tagging/cli.py`
- Source: `u192.json`, row `T3_resume_label_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_workers.py`
- Collected: 166 against a baseline of 166
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_label_typed_on_a_resume_is_not_applied_and_says_so`
  - `tests/test_label_genre.py::test_a_label_typed_on_a_resume_is_still_said_to_be_unapplied`

Old text:

```
        return _resume(ctx, cfg, ctx.args.job, typed_label=ctx.args.label)
```

New text:

```
        return _resume(ctx, cfg, ctx.args.job, typed_label=None)
```

### `u246.S5_inspiration_held_empty`

assert_read_back (inspiration): an empty set of live rows, so every planned row reads as missing and the write refuses

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S5_inspiration_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 331 against a baseline of 331
- Kills: 9 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`
  - `tests/test_organize_inspiration.py::test_a_readable_track_with_no_provider_id_is_matched_as_before`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_slash_in_the_account_name_is_written_as_a_dash`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix`

Old text:

```
        held = set(live)
```

New text:

```
        held = set()
```

### `u246.S6_inspiration_planned_live`

assert_read_back (inspiration): the planned set built from the live rows, so the refusal names no unplanned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S6_inspiration_planned_live`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 331 against a baseline of 331
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_read_back_holding_a_row_the_plan_did_not_name_is_refused`

Old text:

```
            planned = set(one.members)
```

New text:

```
            planned = set(live)
```

### `r501-d.R2_settled_is_not_imported`

routing_cli._all_settled: count acknowledged tracks as proof, so a run nobody imported is recorded as proven

- File: `src/cratekit/write/routing_cli.py`
- Source: `r501-d.json`, row `R2_settled_is_not_imported`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_deferred_routing.py`, `tests/test_routing_workers.py`
- Collected: 329 against a baseline of 329
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
- Collected: 329 against a baseline of 329
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

### `u211.W4_probe_wrapped_at_commit`

commit: run the binding's commit without the careful probe, so its own walk meets the dying process

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W4_probe_wrapped_at_commit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 326 against a baseline of 326
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        with _binding_probe(strict=True):
            db.commit()
```

New text:

```
        with nullcontext():
            db.commit()
```

### `u211.W5_probe_wrapped_at_open`

open_db: construct the binding without the careful probe, so the dying process reads as a damaged library

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W5_probe_wrapped_at_open`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_rb_writer_guard.py`, `tests/test_sync_pair.py`
- Collected: 326 against a baseline of 326
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`

Old text:

```
        with _binding_probe(strict=False):
            db = Rekordbox6Database(path=str(target), unlock=unlock)
```

New text:

```
        with nullcontext():
            db = Rekordbox6Database(path=str(target), unlock=unlock)
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

