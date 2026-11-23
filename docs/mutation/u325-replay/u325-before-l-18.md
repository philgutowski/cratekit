# Mutation table: u325-before-l-18

Measured by `scripts/mutate.py` on 2026-11-23 02:08 UTC, branch `HEAD` at `539638eb`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22663 collected. pytest invocations for this batch: 56.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py compare` at 2026-11-22 22:13 UTC for commit `539638ebe629`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 42, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 78 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22663 against 22663. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `u246.S3_set_playlist_order_set_empty` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 321 | 29 | killed |
| `u246.S4_set_playlist_order_set_read_back` | `src/cratekit/intake/set_playlist.py` | user | 5 file(s) | 321 | 1 | killed |
| `u221.R13_hold_not_read` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 153 | 18 | killed |
| `u221.R14_hold_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 3 file(s) | 153 | 4 | killed |
| `r1255.S6_records_refuses_unlisted` | `src/cratekit/core/session.py` | user | 4 file(s) | 634 | 5 | killed |
| `r1634.M11_reread_reads_the_line` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 293 | 15 | killed |
| `r1634.M12_gone_confirms` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 293 | 6 | killed |
| `r1313.C1_catalogue_failure_alone` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 5 | killed |
| `r1313.C2_catalogue_name_on_any_link` | `src/cratekit/label/tidal_catalogue.py` | user | 3 file(s) | 290 | 1 | killed |
| `u294.M01_rows_narrowed_keeps_all` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 11 | killed |
| `u294.M02_rows_narrowed_changes_unfiltered` | `src/cratekit/tagging/rows.py` | user | 2 file(s) | 128 | 21 | killed |
| `u294.M23_rows_read_back` | `src/cratekit/tagging/rows_cli.py` | user | 2 file(s) | 128 | 1 | killed |
| `r888.R1_roster_serves_one_listing` | `src/cratekit/label/tidal_catalogue.py` | user | 5 file(s) | 578 | 3 | killed |
| `r361-a.A7_mark_verb_forgets_debris` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r361-a.A8_mark_verb_respells_the_word` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `r361-a.A9_reword_the_why` | `src/cratekit/sync/mark_cli.py` | user | 2 file(s) | 116 | 1 | killed |
| `u123.L1_dated_vouched` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 114 | 20 | killed |
| `u123.L2_forget_drops_the_entry` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 114 | 2 | killed |
| `u123.L3_malformed_entry_dropped` | `src/cratekit/modules/outbound/ledger.py` | maintainer | 3 file(s) | 114 | 1 | killed |
| `u211.W1_writer_falls_back` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 263 | 15 | killed |
| `u211.W7_writer_unconfirmed_with_nothing_read` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 263 | 2 | killed |
| `r924.A1_no_plan_line` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 255 | 4 | killed |
| `r924.A2_plan_before_the_bounds` | `src/cratekit/intake/acrcloud.py` | user | 3 file(s) | 255 | 1 | killed |
| `r777.N1_empty_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N2_neither_proof` | `src/cratekit/sync/marks.py` | maintainer | 2 file(s) | 100 | 1 | killed |
| `r777.N3_engine_unchecked` | `src/cratekit/sync/marks.py` | user | 2 file(s) | 100 | 3 | killed |
| `r924.A4_split_on_one_part` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `r924.A5_cadence_halved` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 1 | killed |
| `r924.A6_last_call_unsaid` | `src/cratekit/intake/acrcloud.py` | user | 1 file(s) | 11 | 2 | killed |
| `u129-author.A7_with_archive_omits_digest` | `src/cratekit/intake/land_cli.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r791-b.T1_sources_unread_disposition` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 240 | 12 | killed |
| `r791-b.T2_art_names_unread` | `src/cratekit/tagging/tag.py` | user | 3 file(s) | 240 | 1 | killed |
| `u293.S1_reentrant` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 6 | killed |
| `u293.S2_second_holder_refused` | `src/cratekit/core/staging_lock.py` | user | 4 file(s) | 237 | 5 | killed |
| `sitting4.G10_absent_root_reads_as_untagged` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `sitting4.G3_builders_ignore_the_prefix_map` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 236 | 1 | killed |
| `u212.N1_second_copy_compare` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N3_taken_plain` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 2 | killed |
| `u212.N4_plan_isrc` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `u212.N6_cause_step` | `src/cratekit/write/naming_cli.py` | user | 1 file(s) | 6 | 1 | killed |
| `r290-author.R1_retag_rebuild_drops_the_type` | `src/cratekit/tagging/retag_cli.py` | user | 2 file(s) | 228 | 2 | killed |
| `r290-author.S11_tagging_shell_call_removed` | `src/cratekit/tagging/shell.py` | user | 2 file(s) | 228 | 26 | killed |
| `u89.L1_absent_is_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 126 | killed |
| `u89.L2_tagging_default` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 223 | 12 | killed |
| `r1476.M20_named_first_only` | `src/cratekit/label/registry.py` | user | 6 file(s) | 497 | 7 | killed |
| `r790-d.R1_grouping_kinds` | `src/cratekit/core/review.py` | user | 2 file(s) | 201 | 1 | killed |
| `r790-d.R2_label_beyond` | `src/cratekit/core/review.py` | user | 2 file(s) | 201 | 7 | killed |
| `u90-c.C6_wrapper_reads_nothing` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 198 | 8 | killed |
| `u90-c5.C5_record_threshold_unconverted` | `src/cratekit/write/metadata_cli.py` | user | 2 file(s) | 198 | 1 | killed |
| `r798-c.H6_a_returned_release_passes_at_approval` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 195 | 3 | killed |
| `r798-d.H7_again_an_owned_release_is_not_asked_about` | `src/cratekit/label/approved_cli.py` | user | 2 file(s) | 195 | 1 | killed |
| `u132.V5_nothing` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 2 | killed |
| `u132.V6_backup_name` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 1 | killed |
| `u133-a.P12_verb_warning` | `src/cratekit/cli/verbs/taxonomy.py` | user | 1 file(s) | 57 | 1 | killed |
| `r835-b.M1_only_the_batch_years_marked` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-b.M5_deleted_folder_said` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r835-c.M4_recheck_before_rename_again` | `src/cratekit/label/mark_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r598-a.A6_record_holder_is_a_second_lookup` | `src/cratekit/core/session.py` | maintainer | 2 file(s) | 183 | 1 | killed |
| `r598-a.A7_sweep_ignores_the_shown_list` | `src/cratekit/core/session.py` | user | 2 file(s) | 183 | 1 | killed |
| `u205.S1_account_lookup_ignores_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 177 | 17 | killed |
| `u205.S2_account_rejection_read_as_wait` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 177 | 2 | killed |
| `u202-composites.R2_confined` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.R1_recheck_name` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u202.W1_landed_then_raised` | `src/cratekit/sync/pair_reverse.py` | user | 1 file(s) | 38 | 1 | killed |
| `u277.M11_worker_detail_without_canary` | `src/cratekit/label/cli.py` | user | 3 file(s) | 158 | 3 | killed |
| `u277.M12_worker_message_without_canary` | `src/cratekit/label/cli.py` | user | 3 file(s) | 158 | 2 | killed |
| `u221.R16_release_any_rekordbox_side` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 1 | killed |
| `u221.R17_release_a_pair_that_is_no_twin` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u221.R18_release_writes_nothing` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 6 | killed |
| `u185.G2_unread_refuses` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u185.G3_pending_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 7 | killed |
| `u185.G4_second_reading_leg` | `src/cratekit/core/rb_writer.py` | user | 1 file(s) | 31 | 2 | killed |
| `u267.M6_release_keeps_rows` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 154 | 1 | killed |
| `u267.M9_done_reading_closes_shared` | `src/cratekit/core/rb_writer.py` | user | 3 file(s) | 154 | 64 | killed |
| `r798-c.H2_only_a_hold_in_force_is_dropped` | `src/cratekit/core/review.py` | user | 4 file(s) | 396 | 1 | killed |
| `u123.T1_adapter_vouching` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 149 | 1 | killed |
| `u123.T2_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 149 | 1 | killed |
| `r647-a.B16_serial_recorded_in_the_clear` | `src/cratekit/core/session.py` | maintainer | 1 file(s) | 22663 | 0 (promoted) | zero |
| `r647-a.B17_macos_probe_reads_nothing` | `src/cratekit/core/session.py` | user | 1 file(s) | 22663 | 0 (promoted) | zero |
| `u219.C1_rebuild_items_filtered` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u219.C2_rebuild_named_intake` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 5 | killed |
| `u219.K2_accept_actor` | `src/cratekit/cli/rebuild.py` | user | 1 file(s) | 24 | 1 | killed |
| `u281.C1_refusal_said_as_blocked` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 5 | killed |
| `u281.W7_worker_run_key_without_attempt` | `src/cratekit/tagging/cli.py` | user | 2 file(s) | 138 | 1 | killed |
| `r815-a.W4_the_next_ordinal_is_past_the_floor` | `src/cratekit/core/review.py` | user | 3 file(s) | 376 | 2 | killed |
| `r840-c.C1_the_function_is_handed_the_payload_as_it_stands` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 34 | killed |
| `r840-c.C2_the_function_is_only_handed_an_open_item` | `src/cratekit/core/review.py` | user | 2 file(s) | 137 | 4 | killed |
| `r837-a.A17_sweep_hand_off` | `src/cratekit/sync/cli.py` | user | 5 file(s) | 371 | 1 | killed |
| `r1032.S1_protocol_default_on` | `src/cratekit/modules/outbound/tidal_account.py` | user | 4 file(s) | 367 | 15 | killed |
| `u135.A3_found_vs_made_collapsed` | `src/cratekit/intake/land_cli.py` | user | 2 file(s) | 2 | 2 | killed |

## Zero rows and what they owe

- `u129-author.A7_with_archive_omits_digest` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it
- `r647-a.B16_serial_recorded_in_the_clear` (maintainer facing): maintainer facing, composite not required
- `r647-a.B17_macos_probe_reads_nothing` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `u246.S3_set_playlist_order_set_empty`

assert_read_back (set playlist): an empty set of wanted ids, so a filled playlist always reads as out of order and refuses

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S3_set_playlist_order_set_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 321 against a baseline of 321
- Kills: 29 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_backfill_a_week_later_adds_to_a_playlist_pre_made_under_the_posted_name`
  - `tests/test_set_inspiration_playlist.py::test_a_file_two_collection_rows_claim_is_left_out_rather_than_one_row_picked`
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_failure_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archive_not_renamed_is_a_warning_on_the_envelope`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_archives_the_account_playlist_as_taken_in_its_year_folder`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_creates_the_declared_folder_at_the_root_when_the_library_lacks_it`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_from_a_set_job_writes_the_set_playlist_with_owned_and_landed_rows_in_job_order`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_honours_posted_on_a_pre_freeze_job`
  - `tests/test_set_inspiration_playlist.py::test_a_landing_with_a_page_date_names_the_playlist_for_the_posted_day`
  - `tests/test_set_inspiration_playlist.py::test_a_recorded_playlist_that_was_removed_is_not_added_to_and_a_live_one_is_made`
  - `tests/test_set_inspiration_playlist.py::test_a_removed_namesake_under_the_folder_is_not_written_into`
  - `tests/test_set_inspiration_playlist.py::test_a_rerun_that_adds_nothing_records_no_commit`
  - `tests/test_set_inspiration_playlist.py::test_a_row_neither_owned_nor_landed_is_counted_and_named_and_not_added`
  - `tests/test_set_inspiration_playlist.py::test_a_second_write_that_fills_a_gap_mid_set_is_not_a_failed_write`
  - ... and 14 more, see the JSON sidecar

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set()
```

### `u246.S4_set_playlist_order_set_read_back`

assert_read_back (set playlist): the set built from the read back, so a stranger row in a filled playlist no longer breaks the order

- File: `src/cratekit/intake/set_playlist.py`
- Source: `u246.json`, row `S4_set_playlist_order_set_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_set_inspiration_playlist.py`, `tests/test_export_set.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_write_session.py`, `tests/test_inbox_refill.py`
- Collected: 321 against a baseline of 321
- Kills: 1 (killed)
- Killed:
  - `tests/test_set_inspiration_playlist.py::test_a_filled_playlist_holding_a_row_it_found_still_reads_back_in_set_order`

Old text:

```
    named = set(wanted)
```

New text:

```
    named = set(written.read_back)
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

### `u221.R14_hold_unvalidated`

PairStore._pair: accept a hold that is not ids to words, so a damaged document is read rather than refused

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R14_hold_unvalidated`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`, `tests/test_sync_twins.py`, `tests/test_sync_pair.py`
- Collected: 153 against a baseline of 153
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[bad0]`
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[bad1]`
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[bad2]`
  - `tests/test_sync_twins_hold.py::test_a_hold_that_is_not_ids_to_words_refuses_the_document[t1]`

Old text:

```
        if on_hold is not None and not (
```

New text:

```
        if False and not (
```

### `r1255.S6_records_refuses_unlisted`

records: answer an unlisted log as no session again, so restore list, restore run and session release read it as empty

- File: `src/cratekit/core/session.py`
- Source: `r1255.json`, row `S6_records_refuses_unlisted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_session_log_unlisted.py`, `tests/test_session_cli.py`, `tests/test_restore.py`, `tests/test_doctor.py`
- Collected: 634 against a baseline of 634
- Kills: 5 (killed)
- Killed:
  - `tests/test_session_cli.py::test_a_session_log_that_cannot_be_listed_refuses_the_release_before_its_question`
  - `tests/test_session_log_unlisted.py::test_restore_list_refuses_a_log_it_cannot_list_rather_than_list_nothing`
  - `tests/test_session_log_unlisted.py::test_restore_run_refuses_naming_the_listing_not_an_unrecorded_session`
  - `tests/test_session_log_unlisted.py::test_the_native_landing_lookups_refuse_a_log_they_cannot_list`
  - `tests/test_session_log_unlisted.py::test_the_reporting_reader_refuses_a_log_it_cannot_list`

Old text:

```
    if log_unlisted(unreadable, cfg):
        raise refuse(
```

New text:

```
    if False:
        raise refuse(
```

### `r1634.M11_reread_reads_the_line`

TidalCatalogue.reread_release: judge the listed object's own line instead of reading the album

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M11_reread_reads_the_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 15 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_refuses_though_the_newest_held_release_names_the_label`
  - `tests/test_label_canary.py::test_a_degraded_provider_still_refuses_though_a_held_line_names_the_label`
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_provider_that_answers_with_no_credit_for_the_new_ones_answers_nothing_new`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_an_unanswered_release_with_no_held_release_to_read_refuses_as_before`
  - `tests/test_label_canary.py::test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit`
  - `tests/test_label_canary.py::test_the_shipped_reread_reads_the_provider_though_the_release_carries_a_line`
  - `tests/test_label_canary.py::test_the_worker_answers_nothing_new_when_the_provider_reads_the_held_release`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`
  - `tests/test_label_canary.py::test_with_a_drop_given_no_credit_the_held_label_line_comes_before_another_acts`

Old text:

```
            album = self._album(identity)
        except ReleaseUnresolvable as exc:
```

New text:

```
            album = release
        except ReleaseUnresolvable as exc:
```

### `r1634.M12_gone_confirms`

TidalCatalogue.reread_release: answer a withdrawn release confirmed

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1634.json`, row `M12_gone_confirms`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_label_workers.py`
- Collected: 293 against a baseline of 293
- Kills: 6 (killed)
- Killed:
  - `tests/test_label_canary.py::test_a_lone_withdrawn_held_release_refuses`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_never_replaced_by_another_acts`
  - `tests/test_label_canary.py::test_a_withdrawn_held_release_is_passed_over_for_the_next_and_the_label_has_nothing_new`
  - `tests/test_label_canary.py::test_the_shipped_reread_of_a_release_the_provider_no_longer_has_is_no_credit`
  - `tests/test_label_canary.py::test_the_worker_passes_over_a_withdrawn_held_release_too`
  - `tests/test_label_canary.py::test_two_withdrawn_held_releases_refuse_and_no_third_is_read`

Old text:

```
                "verdict": RELEASE_GONE,
```

New text:

```
                "verdict": "confirmed",
```

### `r1313.C1_catalogue_failure_alone`

_gone: read the 404 off the failure alone, as before R-1313, so a release answered with a 404 page climbs the ladder and fails as an outage

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C1_catalogue_failure_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 5 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_a_release_answered_by_a_404_page_is_gone_at_once`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[catalogue]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return getattr(getattr(exc, "response", None), "status_code", None) == 404
```

### `r1313.C2_catalogue_name_on_any_link`

_gone: read a not found class name on any link, so a parse failure met while handling a not found reads the release as gone

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r1313.json`, row `C2_catalogue_name_on_any_link`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_label_tidal_catalogue.py`
- Collected: 290 against a baseline of 290
- Kills: 1 (killed)
- Killed:
  - `tests/test_provider_not_found_bodies.py::test_a_name_reached_only_as_context_is_not_a_not_found`

Old text:

```
    if "notfound" in type(exc).__name__.lower():
        return True
    return answered_not_found(exc)
```

New text:

```
    if any("notfound" in type(one).__name__.lower() for one, _ in provider_session.failure_links(exc)):
        return True
    return answered_not_found(exc)
```

### `u294.M01_rows_narrowed_keeps_all`

rows.narrowed: hold out no write, so the campaign's tag rows step writes every row the verb would, joining and other routed rows included

- File: `src/cratekit/tagging/rows.py`
- Source: `u294.json`, row `M01_rows_narrowed_keeps_all`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 11 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_to_nothing_writes_nothing`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written`
  - `tests/test_tag_campaign.py::test_the_whole_campaign_lands_and_needs_genre_falls_as_measured`

Old text:

```
    held = {item.content_id for item in plan.writes if item.content_id not in kept}
```

New text:

```
    held = set()
```

### `u294.M02_rows_narrowed_changes_unfiltered`

rows.narrowed: leave every change in the write, so a held row is written though its item says held

- File: `src/cratekit/tagging/rows.py`
- Source: `u294.json`, row `M02_rows_narrowed_changes_unfiltered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 21 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_file_that_comes_to_carry_the_word_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_folder_answer_makes_the_folder_and_the_rows_follow_their_files`
  - `tests/test_tag_campaign.py::test_a_folder_that_would_copy_another_bucket_after_the_gate_stops_the_words_as_stale`
  - `tests/test_tag_campaign.py::test_a_follower_whose_file_carries_another_spelling_is_held_out`
  - `tests/test_tag_campaign.py::test_a_person_reads_the_campaign_and_the_resort_it_leaves`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_to_nothing_writes_nothing`
  - `tests/test_tag_campaign.py::test_a_rows_plan_narrowed_writes_only_the_rows_kept_and_holds_the_rest_out`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_after_part_of_it_landed_reports_what_the_census_reads`
  - `tests/test_tag_campaign.py::test_a_step_that_refuses_stops_the_campaign_with_the_earlier_writes_named`
  - `tests/test_tag_campaign.py::test_a_word_left_or_unanswered_is_named_and_nothing_retags_it`
  - `tests/test_tag_campaign.py::test_an_alias_to_the_folder_another_answer_makes_is_planned_on_that_folder`
  - `tests/test_tag_campaign.py::test_an_unexpected_failure_in_a_step_is_this_builds_defect_with_what_landed`
  - `tests/test_tag_campaign.py::test_every_file_an_alias_retags_is_on_the_gate_and_in_the_digest`
  - `tests/test_tag_campaign.py::test_only_the_genre_column_moves_on_a_written_row`
  - `tests/test_tag_campaign.py::test_rows_joining_needs_genre_and_any_other_routed_row_are_never_written`
  - ... and 6 more, see the JSON sidecar

Old text:

```
        changes=tuple(change for change in plan.changes.changes if change.content_id not in held),
```

New text:

```
        changes=tuple(plan.changes.changes),
```

### `u294.M23_rows_read_back`

tag rows' apply path no longer refuses over a row that does not read back

- File: `src/cratekit/tagging/rows_cli.py`
- Source: `u294.json`, row `M23_rows_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_campaign.py`, `tests/test_tag_rows.py`
- Collected: 128 against a baseline of 128
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_campaign.py::test_a_row_that_does_not_read_back_refuses_the_rows_step`

Old text:

```
    rows.assert_read_back(written)
    return written
```

New text:

```
    return written
```

### `r888.R1_roster_serves_one_listing`

LabelRoster.held: the roster answers its albums for every listing, so its singles are never read

- File: `src/cratekit/label/tidal_catalogue.py`
- Source: `r888.json`, row `R1_roster_serves_one_listing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tidal_catalogue.py`, `tests/modules/test_labels.py`, `tests/test_label_workers.py`, `tests/test_adapter_listing.py`, `tests/test_label_playlists.py`
- Collected: 578 against a baseline of 578
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_tidal_catalogue.py::test_a_listing_a_roster_does_not_hold_is_skipped_and_recorded`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_crawls_the_label_page_and_every_seed_through_the_listing`
  - `tests/test_label_tidal_catalogue.py::test_the_roster_lists_once_when_it_is_built_and_the_crawl_reads_memory`

Old text:

```
        return self._listed.get(method)
```

New text:

```
        return self._listed.get("get_albums")
```

### `r361-a.A7_mark_verb_forgets_debris`

The mark verb's plan no longer decides label-debris, so the playlist falls through to the reports

- File: `src/cratekit/sync/mark_cli.py`
- Source: `r361-a.json`, row `A7_mark_verb_forgets_debris`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_intake_imported.py`, `tests/test_sync_mark.py`
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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
- Collected: 116 against a baseline of 116
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

### `u123.L1_dated_vouched`

Stop the ledger vouching for a dated playlist it records

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L1_dated_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 114 against a baseline of 114
- Kills: 20 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_dated_entry_that_is_not_a_name_to_an_identifier_is_not_vouched_for`
  - `tests/test_label_heard.py::test_a_dated_playlist_made_by_the_dated_plan_is_vouched_for_and_one_reused_is_not`
  - `tests/test_label_heard.py::test_a_delete_the_client_answers_false_is_a_failure`
  - `tests/test_label_heard.py::test_a_folder_with_no_year_playlist_refuses_when_there_is_something_to_add`
  - `tests/test_label_heard.py::test_a_named_release_already_heard_is_said_and_writes_nothing`
  - `tests/test_label_heard.py::test_a_playlist_already_gone_is_removed_with_no_delete`
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_a_playlist_the_client_does_not_serve_as_owned_is_refused_in_words`
  - `tests/test_label_heard.py::test_a_removal_refused_part_way_names_the_adds_marks_nothing_and_a_resume_finishes`
  - `tests/test_label_heard.py::test_a_track_an_unheard_release_also_carries_stays_on_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_track_the_year_will_not_take_keeps_the_dated_playlist`
  - `tests/test_label_heard.py::test_a_year_known_only_by_the_marks_prefixed_name_is_the_year`
  - `tests/test_label_heard.py::test_an_adopted_year_still_wins_over_a_dated_entry_for_the_same_identifier`
  - `tests/test_label_heard.py::test_declined_nothing_is_written`
  - `tests/test_label_heard.py::test_every_run_says_the_record_labels_tree_is_not_changed`
  - ... and 5 more, see the JSON sidecar

Old text:

```
        if wanted in (record.get("dated") or {}).values():
            made = True
```

New text:

```
        if False:
            made = True
```

### `u123.L2_forget_drops_the_entry`

Keep a removed dated playlist's ledger entry

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L2_forget_drops_the_entry`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 114 against a baseline of 114
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

### `u123.L3_malformed_entry_dropped`

Keep a dated entry with an empty name or identifier

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L3_malformed_entry_dropped`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 114 against a baseline of 114
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

### `u211.W1_writer_falls_back`

_asked_or_scanned: re-raise pyrekordbox's error instead of asking the careful scan, the defect itself

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W1_writer_falls_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 263 against a baseline of 263
- Kills: 15 (killed)
- Killed:
  - `tests/test_process_scan.py::test_a_gated_sync_pair_refused_by_the_scan_is_kept_and_continues_with_run`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[agent]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[both]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[rekordbox]`
  - `tests/test_process_scan.py::test_the_binding_probe_at_open_only_loses_a_warning`
  - `tests/test_process_scan.py::test_the_binding_probe_is_put_back_after_a_refusal`
  - `tests/test_process_scan.py::test_the_binding_probe_names_rekordbox_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_refuses_a_live_unreadable_process_at_commit`
  - `tests/test_process_scan.py::test_the_binding_probe_skips_a_zombie_at_commit`
  - `tests/test_process_scan.py::test_the_gated_sync_pair_scenario_reads_the_same_with_rekordbox_open_on_the_host`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_read_agent_as_running_not_as_unconfirmed`
  - `tests/test_process_scan.py::test_the_writer_skips_a_zombie_pyrekordbox_could_not_read`
  - `tests/test_process_scan.py::test_the_writer_still_sees_rekordbox_beside_the_dying_process`

Old text:

```
        return processes.rekordbox_pid(name)
```

New text:

```
        raise
```

### `u211.W7_writer_unconfirmed_with_nothing_read`

rekordbox_processes_running in the writer: a probe that could not confirm, with no rekordbox process read at all, answers clear instead of refusing

- File: `src/cratekit/core/rb_writer.py`
- Source: `u211.json`, row `W7_writer_unconfirmed_with_nothing_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_process_scan.py`, `tests/test_process_guard.py`, `tests/test_rb_writer_guard.py`
- Collected: 263 against a baseline of 263
- Kills: 2 (killed)
- Killed:
  - `tests/test_process_scan.py::test_both_mechanisms_agree_beside_a_live_unreadable_process[none]`
  - `tests/test_process_scan.py::test_the_writer_refuses_a_live_unreadable_process_by_name_not_as_internal`

Old text:

```
        if not running:
            raise unconfirmed
```

New text:

```
        if False:
            raise unconfirmed
```

### `r924.A1_no_plan_line`

Identification never states its plan before the first call

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A1_no_plan_line`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 255 against a baseline of 255
- Kills: 4 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_cached_recording_says_so_and_counts_no_calls`
  - `tests/intake/test_set_progress.py::test_a_parted_set_says_its_parts_in_the_plan`
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
    if False:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

### `r924.A2_plan_before_the_bounds`

The plan line is said before the month bound and the credential read, so a refused run is told it will pay

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A2_plan_before_the_bounds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`, `tests/intake/test_workers.py`, `tests/intake/test_recognition.py`
- Collected: 255 against a baseline of 255
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_a_run_the_month_refuses_is_not_told_it_will_pay`

Old text:

```
    keys = ("", "")
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
    # AFTER EVERY REFUSAL THAT SPENDS NOTHING, so a run told it is about to pay
    # is a run that will, and one refused by a bound or a missing key is told
    # only the refusal.
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
```

New text:

```
    keys = ("", "")
    offsets = tuple(offset for part in parts for offset in part)
    if progress is not None:
        progress(_plan_line(len(offsets), cached=len(offsets) - len(owed), parts=len(parts)))
    if owed:
        assert_month_within(spend, planned=len(owed), used_this_month=counter.used(month))
        keys = credentials()
```

### `r777.N1_empty_proof`

marks.require_proof accepts a NativeLanding naming no tree, no pass or no landing

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N1_empty_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
        if not local_output.tree_id or not local_output.pass_name or not local_output.landings:
```

New text:

```
        if False:
```

### `r777.N2_neither_proof`

marks.require_proof hands anything that is not a NativeLanding to require_output, so None is no longer refused by name

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N2_neither_proof`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`

Old text:

```
    if not isinstance(local_output, Path):
```

New text:

```
    if False:
```

### `r777.N3_engine_unchecked`

apply_deferred no longer checks its proof before renaming

- File: `src/cratekit/sync/marks.py`
- Source: `r777.json`, row `N3_engine_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_incremental_sync.py`, `tests/test_sync_mark.py`
- Collected: 100 against a baseline of 100
- Kills: 3 (killed)
- Killed:
  - `tests/test_incremental_sync.py::test_external_marks_wait_for_local_output_and_recheck`
  - `tests/test_sync_mark.py::test_the_engine_refuses_a_mark_with_neither_proof`
  - `tests/test_sync_mark.py::test_the_file_check_makes_one_stat_and_refuses_whatever_it_raises`

Old text:

```
    require_proof(local_output)
    applied: list[str] = []
```

New text:

```
    applied: list[str] = []
```

### `r924.A4_split_on_one_part`

A set identified in one part is said to be in parts

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A4_split_on_one_part`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`

Old text:

```
    split = f" in {parts} parts" if parts > 1 else ""
```

New text:

```
    split = f" in {parts} parts" if parts >= 1 else ""
```

### `r924.A5_cadence_halved`

The counter speaks every tenth call rather than every twentieth

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A5_cadence_halved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 1 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    return calls == 1 or calls == owed or calls % PROGRESS_EVERY == 0
```

New text:

```
    return calls == 1 or calls == owed or calls % (PROGRESS_EVERY // 2) == 0
```

### `r924.A6_last_call_unsaid`

The counter does not say the last call

- File: `src/cratekit/intake/acrcloud.py`
- Source: `r924.json`, row `A6_last_call_unsaid`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 11 against a baseline of 11
- Kills: 2 (killed)
- Killed:
  - `tests/intake/test_set_progress.py::test_human_output_says_the_fetch_then_the_plan_then_the_count`
  - `tests/intake/test_set_progress.py::test_the_planned_count_is_the_chunks_the_carver_is_asked_for`

Old text:

```
    return calls == 1 or calls == owed or calls % PROGRESS_EVERY == 0
```

New text:

```
    return calls == 1 or calls % PROGRESS_EVERY == 0
```

### `u129-author.A7_with_archive_omits_digest`

Fold archive items into the landing without changing the digest

- File: `src/cratekit/intake/land_cli.py`
- Source: `u129-author.json`, row `A7_with_archive_omits_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/intake/test_set_progress.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    identity = {
        "land": payload["digest"],
        "archive": archived.payload["digest"],
    }

```

New text:

```
    identity = {
        "land": payload["digest"],
    }

```

### `r791-b.T1_sources_unread_disposition`

tag_one: a decline naming unread sources is reported no-hit

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T1_sources_unread_disposition`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 12 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_fallback_blocked_on_every_file_it_was_asked_about_is_named_by_the_warning`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_parse_break_at_the_general_catalogue_says_a_rerun_will_not_move_it`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_a_sweep_with_no_discogs_token_says_so_and_reads_no_file_as_no_hit`
  - `tests/test_tag_workers.py::test_an_outage_keeps_its_own_word_in_the_sweeps_warning`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`
  - `tests/test_tag_workers.py::test_files_with_no_isrc_are_counted_and_warned_about_whatever_their_skip_reason`
  - `tests/test_tag_workers.py::test_one_unread_file_beside_a_parse_break_is_counted_and_the_defect_is_said`
  - `tests/test_tag_workers.py::test_the_sweeps_unread_warning_names_discogs_first`
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        elif hit.unread:
```

New text:

```
        elif False:
```

### `r791-b.T2_art_names_unread`

_art_embedded: the picture decline never names the unread sources

- File: `src/cratekit/tagging/tag.py`
- Source: `r791-b.json`, row `T2_art_names_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tagging_engine.py`, `tests/test_tag_workers.py`, `tests/test_catalogue_searcher.py`
- Collected: 240 against a baseline of 240
- Kills: 1 (killed)
- Killed:
  - `tests/test_tagging_engine.py::test_a_decline_beside_an_unread_catalogue_is_sources_unread_and_not_no_hit`

Old text:

```
        unread = hit.unread if hit is not None else ()
```

New text:

```
        unread = ()
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

### `sitting4.G10_absent_root_reads_as_untagged`

The mount guard is removed, so an unplugged volume reads as a library of untagged files and the sweep succeeds unmatched

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G10_absent_root_reads_as_untagged`
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
        f"the library root {root} is not a directory on this machine, so no "
```

New text:

```
    root = Path(cfg.library.root)
    if True:
        return
    raise refuse(
        "library-volume-unmounted",
        f"the library root {root} is not a directory on this machine, so no "
```

### `sitting4.G3_builders_ignore_the_prefix_map`

The builders hand the resolver an empty map, so a renamed drive resolves no row (R-372)

- File: `src/cratekit/modules/outbound/source.py`
- Source: `sitting4.json`, row `G3_builders_ignore_the_prefix_map`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_row_builders_use_the_configured_prefix_map`

Old text:

```
    return [
        locations.PrefixRule(source_prefix, target)
        for source_prefix, target in cfg.resolved_prefix_map()
    ]
```

New text:

```
    return []
```

### `u212.N1_second_copy_compare`

naming_cli.second_copy: two different ISRCs read as one recording

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N1_second_copy_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_another_recording_keeps_the_plain_collision`

Old text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) == mine else ""
```

New text:

```
    return mine if tags.isrc_token(tags.read_tag(target, "isrc")) != "" else ""
```

### `u212.N3_taken_plain`

naming_cli._taken: always the plain collision, never a second copy

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N3_taken_plain`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 2 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_copy_that_takes_the_name_after_the_plan_is_said_a_second_copy`
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    same = second_copy(path, target)
    if same:
```

New text:

```
    same = second_copy(path, target)
    if False:
```

### `u212.N4_plan_isrc`

naming_cli._plan_for: the plan item carries no ISRC

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N4_plan_isrc`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
            if str(path) in seconds:
                item["isrc"] = seconds[str(path)]
```

New text:

```
(empty)
```

### `u212.N6_cause_step`

naming_cli._incomplete_cause: the second copy step is never added

- File: `src/cratekit/write/naming_cli.py`
- Source: `u212.json`, row `N6_cause_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_naming_second_copy.py`
- Collected: 6 against a baseline of 6
- Kills: 1 (killed)
- Killed:
  - `tests/test_naming_second_copy.py::test_a_target_held_by_the_same_recording_is_said_as_a_second_copy`

Old text:

```
    if any(item.get("isrc") for item in incomplete):
```

New text:

```
    if False:
```

### `r290-author.R1_retag_rebuild_drops_the_type`

Rebuild the retag refusal as a plain CratekitError again, so a retag parked after correcting a file says failed

- File: `src/cratekit/tagging/retag_cli.py`
- Source: `r290-author.json`, row `R1_retag_rebuild_drops_the_type`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 2 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_reworded_refusal_is_rebuilt_in_one_place_only`
  - `tests/test_tag_workers.py::test_a_parked_retag_keeps_both_the_block_and_the_reload`

Old text:

```
    return rebuilt(
        error,
        replace(
```

New text:

```
    return CratekitError(
        replace(
```

### `r290-author.S11_tagging_shell_call_removed`

Remove the one jobs.raise_for_state call from tagging/shell.py, so this shell reports a parked or half failed job and exits 0

- File: `src/cratekit/tagging/shell.py`
- Source: `r290-author.json`, row `S11_tagging_shell_call_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_job_outcome.py`, `tests/test_tag_workers.py`
- Collected: 228 against a baseline of 228
- Kills: 26 (killed)
- Killed:
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_cancelled_job_leaves_every_queued_verb_cancelled_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.folder]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_is_still_refused_the_second_time_it_is_asked[tag.retag]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_half_failed_job_leaves_every_queued_verb_failed_and_non_zero[tag.retag]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_answers_the_same_way_the_second_time_it_is_asked[tag.retag]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[label.judge]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[tag.folder]`
  - `tests/test_job_outcome.py::test_a_parked_job_leaves_every_queued_verb_blocked_and_non_zero[tag.retag]`
  - ... and 11 more, see the JSON sidecar

Old text:

```
jobs.raise_for_state(job)
```

New text:

```
jobs.get  # the mapping call, removed
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
  - `tests/test_routing_workers.py::test_a_confirmed_inbox_applies_on_an_encrypted_library`
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

### `u89.L2_tagging_default`

vocal_cut: drop the default fallback, so an uncalibrated My Tags pass has no cut

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u89.json`, row `L2_tagging_default`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_routing_workers.py`, `tests/test_metadata_cli.py`
- Collected: 223 against a baseline of 223
- Kills: 12 (killed)
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
  - `tests/test_routing_workers.py::test_the_loader_says_absent_as_none_and_the_tagging_cut_still_defaults`

Old text:

```
    return DEFAULT_VOCAL_THRESHOLD if threshold is None else threshold
```

New text:

```
    return threshold
```

### `r1476.M20_named_first_only`

Registry.named: answer only the first holder, as by_name does

- File: `src/cratekit/label/registry.py`
- Source: `r1476.json`, row `M20_named_first_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre.py`, `tests/test_tag_folder_copyright.py`, `tests/test_tag_workers.py`, `tests/test_tagging_engine.py`, `tests/test_label_registry_verbs.py`, `tests/modules/test_labels.py`
- Collected: 497 against a baseline of 497
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_genre.py::test_a_files_own_tag_naming_a_shared_name_is_given_neither_labels_genre`
  - `tests/test_label_genre.py::test_a_label_sharing_its_name_with_one_carrying_a_genre_is_never_given_that_genre`
  - `tests/test_label_genre.py::test_a_shared_name_outranking_the_folders_label_is_named_truly`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ Alpha ]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[ALPHA]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[Alpha]`
  - `tests/test_label_genre.py::test_a_tag_naming_a_display_name_two_labels_share_names_neither[alpha]`

Old text:

```
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)
```

New text:

```
        return tuple(entry for entry in self.labels.values() if _name_key(entry.name) == wanted)[:1]
```

### `r790-d.R1_grouping_kinds`

grouped: count every kind in the queue, harvested label names included

- File: `src/cratekit/core/review.py`
- Source: `r790-d.json`, row `R1_grouping_kinds`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 201 against a baseline of 201
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_harvested_label_name_is_not_counted_as_a_label_release`

Old text:

```
    kinds = kinds or GROUPED_KINDS.get(declared)
```

New text:

```
    kinds = kinds
```

### `r790-d.R2_label_beyond`

grouped by label: report no recorded beyond

- File: `src/cratekit/core/review.py`
- Source: `r790-d.json`, row `R2_label_beyond`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_offer_window.py`, `tests/test_review_queue.py`
- Collected: 201 against a baseline of 201
- Kills: 7 (killed)
- Killed:
  - `tests/test_label_offer_window.py::test_a_first_sweep_files_the_default_ten_and_counts_the_other_forty`
  - `tests/test_label_offer_window.py::test_a_label_whose_offer_is_raised_to_thirty_files_thirty`
  - `tests/test_label_offer_window.py::test_a_round_records_the_most_the_label_could_still_offer`
  - `tests/test_label_offer_window.py::test_a_run_over_two_labels_counts_what_both_left_beyond`
  - `tests/test_label_offer_window.py::test_a_second_sweep_files_only_the_new_release_and_refiles_nothing`
  - `tests/test_label_offer_window.py::test_a_track_limit_below_the_offer_bounds_it_and_the_rest_is_still_counted`
  - `tests/test_label_offer_window.py::test_the_configured_offer_is_the_default_for_every_label`

Old text:

```
                "beyond": latest[key].beyond if key in latest else None,
```

New text:

```
                "beyond": None,
```

### `u90-c.C6_wrapper_reads_nothing`

load_vocal_threshold stops delegating, so every caller sees an uncalibrated library

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c.json`, row `C6_wrapper_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 198 against a baseline of 198
- Kills: 8 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_fit_over_a_fitted_cut_names_the_fit_it_replaces`
  - `tests/test_analysis_workers.py::test_a_hand_cut_is_written_and_the_one_loader_reads_it_back`
  - `tests/test_analysis_workers.py::test_a_hand_cut_replaces_an_unreadable_calibration_and_says_it_could_not_be_read`
  - `tests/test_analysis_workers.py::test_a_second_hand_cut_reports_the_cut_it_replaces`
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[0]`
  - `tests/test_analysis_workers.py::test_the_ends_of_the_score_range_are_cuts[100]`
  - `tests/test_metadata_cli.py::test_a_present_vocal_calibration_is_its_own_threshold`

Old text:

```
    return None if record is None else record["threshold"]
```

New text:

```
    return None
```

### `u90-c5.C5_record_threshold_unconverted`

The one reader returns the stored threshold as written rather than the checked float

- File: `src/cratekit/write/metadata_cli.py`
- Source: `u90-c5.json`, row `C5_record_threshold_unconverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_analysis_workers.py`, `tests/test_metadata_cli.py`
- Collected: 198 against a baseline of 198
- Kills: 1 (killed)
- Killed:
  - `tests/test_analysis_workers.py::test_a_threshold_written_as_text_comes_back_from_the_one_reader_as_a_float`

Old text:

```
    return {**record, "threshold": threshold}
```

New text:

```
    return dict(record)
```

### `r798-c.H6_a_returned_release_passes_at_approval`

label approved: judge a release a person returned, so it is held a second time when it is accepted

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-c.json`, row `H6_a_returned_release_passes_at_approval`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`
- Collected: 195 against a baseline of 195
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_a_release_held_at_approval_is_returned_by_name_and_listed_the_next_time`
  - `tests/test_label_genre_gate.py::test_a_returned_mark_on_the_payload_alone_is_believed`
  - `tests/test_label_genre_gate.py::test_a_returned_release_is_listed_at_approval_and_not_judged_again`

Old text:

```
        if release.returned:
            continue
```

New text:

```
        if False:
            continue
```

### `r798-d.H7_again_an_owned_release_is_not_asked_about`

label approved: ask the general catalogue about a release the library holds in full. H7 measured again, against the line as the second review left it, where ownership is read off the one resolution of each release

- File: `src/cratekit/label/approved_cli.py`
- Source: `r798-d.json`, row `H7_again_an_owned_release_is_not_asked_about`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_label_approved.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_the_catalogue_is_not_asked_about_a_release_the_library_already_holds`

Old text:

```
        elif owned(release):
```

New text:

```
        elif False:
```

### `u132.V5_nothing`

A plan that writes nothing still asks the gate

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V5_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 2 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_second_run_plans_nothing_and_asks_nothing`
  - `tests/test_taxonomy_upgrade.py::test_what_is_held_is_said_and_written_around`

Old text:

```
    if not found.writes:

```

New text:

```
    if False:

```

### `u132.V6_backup_name`

A backup takes the name an earlier backup holds

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u132.json`, row `V6_backup_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_a_backup_never_takes_an_earlier_backups_name`

Old text:

```
    while candidate.exists():

```

New text:

```
    while False:

```

### `u133-a.P12_verb_warning`

The verb drops the keyword rule warning

- File: `src/cratekit/cli/verbs/taxonomy.py`
- Source: `u133-a.json`, row `P12_verb_warning`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_taxonomy_upgrade.py`
- Collected: 57 against a baseline of 57
- Kills: 1 (killed)
- Killed:
  - `tests/test_taxonomy_upgrade.py::test_the_upgrade_that_adds_jazz_says_the_copys_keyword_rule_is_left`

Old text:

```
    ] + [{"code": KEYWORD_RULE, "message": sentence} for sentence in found.keywords]

```

New text:

```
    ]

```

### `r835-b.M1_only_the_batch_years_marked`

mark_cli._item: a year the landed batch did not file is marked anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M1_only_the_batch_years_marked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_year_the_batch_did_not_file_is_left_alone`

Old text:

```
    if year.year not in filed:
        return {
```

New text:

```
    if False:
        return {
```

### `r835-b.M5_deleted_folder_said`

mark_cli.label_mark: a label folder deleted on the account is listed as if it were there, and the read fails every run

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-b.json`, row `M5_deleted_folder_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_said_not_failed`

Old text:

```
            if shape.folder_id in remote.folders()
```

New text:

```
            if True
```

### `r835-c.M4_recheck_before_rename_again`

mark_cli.label_mark: a title changed between the plan and the write is renamed anyway

- File: `src/cratekit/label/mark_cli.py`
- Source: `r835-c.json`, row `M4_recheck_before_rename_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_title_changed_between_the_plan_and_the_write_is_not_renamed`

Old text:

```
            if now.get(identity) != item["built_as"]:
```

New text:

```
            if False:
```

### `r598-a.A6_record_holder_is_a_second_lookup`

assert_gates: record current_holder() in the record rather than the claimant the lock took, so a supplied holder splits the two copies

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A6_record_holder_is_a_second_lookup`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_a_supplied_holder_reaches_the_record_as_well_as_the_lock`

Old text:

```
                holder=claimant,
                intent=intent,
```

New text:

```
                holder=current_holder(),
                intent=intent,
```

### `r598-a.A7_sweep_ignores_the_shown_list`

abandon_orphaned_sessions: end every orphan rather than only those shown, so one answer ends records the question never listed

- File: `src/cratekit/core/session.py`
- Source: `r598-a.json`, row `A7_sweep_ignores_the_shown_list`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`, `tests/test_session_cli.py`
- Collected: 183 against a baseline of 183
- Kills: 1 (killed)
- Killed:
  - `tests/test_write_session.py::test_the_sweep_ends_only_the_orphans_it_was_shown`

Old text:

```
        if (shown is None or record.session_id in shown) and orphaned(record, here=here)
```

New text:

```
        if orphaned(record, here=here)
```

### `u205.S1_account_lookup_ignores_app`

outbound account: ISRC lookups go to the account session whatever the opener built

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S1_account_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 177 against a baseline of 177
- Kills: 17 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_404_on_a_track_read_is_no_track_and_is_asked_once`
  - `tests/test_catalogue_app.py::test_a_404_on_the_isrc_collection_is_an_outage_and_never_no_track`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[400]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[500]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[503]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[data-not-a-list]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-an-object]`
  - `tests/test_catalogue_app.py::test_a_failed_lookup_climbs_the_ladder_and_refuses_rather_than_reading_as_no_match[not-json]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_that_was_only_expired_is_answered_on_the_next_rung`
  - `tests/test_catalogue_app.py::test_a_release_whose_artists_did_not_come_back_is_unreadable_and_chooses_nothing`
  - `tests/test_catalogue_app.py::test_a_transport_failure_whose_text_holds_404_is_not_read_as_no_track`
  - `tests/test_catalogue_app.py::test_an_exact_track_reference_is_read_from_the_app`
  - `tests/test_catalogue_app.py::test_an_isrc_match_with_the_app_recorded_makes_no_account_call`
  - ... and 2 more, see the JSON sidecar

Old text:

```
        self._lookups = catalogue if catalogue is not None else session
```

New text:

```
        self._lookups = session
```

### `u205.S2_account_rejection_read_as_wait`

outbound account: a rejected app credential is translated as the account's failure, a wait, never naming the app

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S2_account_rejection_read_as_wait`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 177 against a baseline of 177
- Kills: 2 (killed)
- Killed:
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[401]`
  - `tests/test_catalogue_app.py::test_a_rejected_app_token_climbs_the_ladder_then_refuses_naming_the_app[403]`

Old text:

```
        except catalogue_api.AppCredentialsRejected as exc:
            # THE APP'S CREDENTIAL, NOT THE ACCOUNT'S.
```

New text:

```
        except ZeroDivisionError as exc:
            # THE APP'S CREDENTIAL, NOT THE ACCOUNT'S.
```

### `u202-composites.R2_confined`

pair_reverse.create: the twins' confinement check is not run before the commit

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202-composites.json`, row `R2_confined`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_write_outside_the_playlist_made_is_refused_with_nothing_written`

Old text:

```
                twins.assert_confined(
                    db,
```

New text:

```
                (lambda *a, **k: None)(
                    db,
```

### `u202.R1_recheck_name`

pair_reverse.recheck: a name taken since the plan is made again

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `R1_recheck_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_the_write_refuses_a_name_taken_since_the_plan`

Old text:

```
    if taken:
        raise _stale(
```

New text:

```
    if False:
        raise _stale(
```

### `u202.W1_landed_then_raised`

pair_reverse.create: a commit that lands and then raises no longer tells the caller, so the playlist made stays unpaired (the second review's BLOCKING finding)

- File: `src/cratekit/sync/pair_reverse.py`
- Source: `u202.json`, row `W1_landed_then_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_a_commit_that_lands_and_then_raises_still_pairs_the_playlist`

Old text:

```
                    if on_commit is not None and playlist_id:
                        on_commit(playlist_id)
                raise
```

New text:

```
                raise
```

### `u277.M11_worker_detail_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's detail

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M11_worker_detail_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_offer_window.py`
- Collected: 158 against a baseline of 158
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_over_held_lines_that_name_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
                **({"reverified": canaries[0].to_json()} if canaries else {}),
```

New text:

```
                **({}),
```

### `u277.M12_worker_message_without_canary`

the worker's label-sweep-incomplete: leave the canary out of the refusal's message

- File: `src/cratekit/label/cli.py`
- Source: `u277.json`, row `M12_worker_message_without_canary`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_canary.py`, `tests/test_label_workers.py`, `tests/test_label_offer_window.py`
- Collected: 158 against a baseline of 158
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_canary.py::test_the_worker_refuses_a_degraded_provider_though_every_held_line_names_the_label`
  - `tests/test_label_canary.py::test_the_worker_refuses_held_lines_naming_another_act_and_names_the_canary`

Old text:

```
            f"{asked_again}",
```

New text:

```
            f"",
```

### `u221.R16_release_any_rekordbox_side`

PairStore.release_hold: drop the rekordbox check, so a twin paired again since the plan is released

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R16_release_any_rekordbox_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_again_since_the_plan_is_left_held`

Old text:

```
                    or held.rekordbox_id != str(rekordbox_id)
```

New text:

```
                    or False
```

### `u221.R17_release_a_pair_that_is_no_twin`

PairStore.release_hold: drop the twin check, so a pair that is no twin records a hold

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R17_release_a_pair_that_is_no_twin`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_release_hold_passes_over_a_pair_that_is_no_twin_and_one_holding_nothing`

Old text:

```
                    or not held.twin
                    or held.rekordbox_id
```

New text:

```
                    or held.rekordbox_id
```

### `u221.R18_release_writes_nothing`

PairStore.release_hold: never write, so an approved release answers released and the next sync still holds

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u221.json`, row `R18_release_writes_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_twins_hold.py`
- Collected: 32 against a baseline of 32
- Kills: 6 (killed)
- Killed:
  - `tests/test_sync_twins_hold.py::test_a_released_twin_asks_nothing_the_second_time`
  - `tests/test_sync_twins_hold.py::test_a_second_twin_stays_held_when_the_first_is_released`
  - `tests/test_sync_twins_hold.py::test_a_track_an_earlier_sync_queued_is_awaiting_not_on_hold`
  - `tests/test_sync_twins_hold.py::test_a_twin_paired_before_u221_is_released_by_name_and_counted_by_time`
  - `tests/test_sync_twins_hold.py::test_release_all_lets_every_twin_go`
  - `tests/test_sync_twins_hold.py::test_releasing_the_twin_queues_its_three_at_the_next_sync`

Old text:

```
            if released:
                self._write(pairs)
            return released
```

New text:

```
            return released
```

### `u185.G2_unread_refuses`

assert_foreign_untouched: a handle with no reading at open reads the subtree now and goes on

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G2_unread_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_handle_with_no_reading_at_open_refuses_rather_than_assuming_nothing_is_there`
  - `tests/test_foreign_tree.py::test_a_reading_that_failed_at_open_is_kept_as_unread_and_refuses`

Old text:

```
    before = foreign_tree.reading_at_open(db)
    if before is None:
```

New text:

```
    before = foreign_tree.reading_at_open(db) or foreign_tree.read(db.session)
    if before is None:
```

### `u185.G3_pending_leg`

assert_foreign_untouched: drop the pending object leg, keep the second reading

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G3_pending_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 7 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_membership_added_to_a_pushed_playlist_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_made_inside_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_playlist_of_ones_own_moved_into_the_folder_is_refused`
  - `tests/test_foreign_tree.py::test_a_pushed_membership_rewritten_to_another_owner_is_refused`
  - `tests/test_foreign_tree.py::test_a_second_folder_of_the_name_at_the_top_is_refused`
  - `tests/test_foreign_tree.py::test_a_soft_delete_of_a_pushed_playlist_is_refused_even_where_the_commit_admits_removals`
  - `tests/test_foreign_tree.py::test_renaming_the_folder_is_refused_and_rolled_back`

Old text:

```
    violations = foreign_tree.pending_touches(pending_objects(session, db), before)
```

New text:

```
    violations = []
```

### `u185.G4_second_reading_leg`

assert_foreign_untouched: drop the second reading from SQL, keep the pending objects

- File: `src/cratekit/core/rb_writer.py`
- Source: `u185.json`, row `G4_second_reading_leg`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_foreign_tree.py`
- Collected: 31 against a baseline of 31
- Kills: 2 (killed)
- Killed:
  - `tests/test_foreign_tree.py::test_a_push_that_lands_while_a_handle_is_open_refuses_that_handles_commit`
  - `tests/test_foreign_tree.py::test_raw_sql_into_the_folder_is_seen_by_the_reading_again_from_sql`

Old text:

```
    violations += foreign_tree.differences(before, foreign_tree.read(session))
```

New text:

```
    violations += []
```

### `u267.M6_release_keeps_rows`

SharedRead.release: keep the identity map, so the next reader takes a row an earlier reader loaded as the row the database holds now

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M6_release_keeps_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 154 against a baseline of 154
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_release_forgets_every_row_so_the_next_reader_reads_afresh`

Old text:

```
        db.session.expunge_all()
```

New text:

```
        db.session.flush()
```

### `u267.M9_done_reading_closes_shared`

done_reading: close the handle whatever its owner, so the first reader closes the shared handle under the rest

- File: `src/cratekit/core/rb_writer.py`
- Source: `u267.json`, row `M9_done_reading_closes_shared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`, `tests/test_organize_inspiration.py`
- Collected: 154 against a baseline of 154
- Kills: 64 (killed)
- Killed:
  - `tests/test_organize.py::test_a_label_playlist_is_the_label_steps_and_a_set_the_archives`
  - `tests/test_organize.py::test_a_mark_put_back_is_no_mark_and_the_playlist_stays`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`
  - `tests/test_organize.py::test_a_playlist_two_folders_down_is_left_where_it_is`
  - `tests/test_organize.py::test_a_prefixed_but_unmarked_playlist_has_its_own_reason`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - ... and 49 more, see the JSON sidecar

Old text:

```
    if shared is None:
        close_db(db)
    else:
        shared.release(db)
```

New text:

```
    close_db(db)
```

### `r798-c.H2_only_a_hold_in_force_is_dropped`

review.release_hold: drop a hold in any state, so the record that a person returned a release is lost and it can be held again

- File: `src/cratekit/core/review.py`
- Source: `r798-c.json`, row `H2_only_a_hold_in_force_is_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_genre_gate.py`, `tests/test_review_queue.py`, `tests/test_label_offer_window.py`, `tests/test_label_approved.py`
- Collected: 396 against a baseline of 396
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_genre_gate.py::test_releasing_drops_a_hold_in_force_and_keeps_a_returned_one`

Old text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ? AND state = ?",
            (_assert_declared_queue(queue), item_id, HOLD_HELD),
```

New text:

```
            "DELETE FROM held_offers WHERE queue = ? AND item_id = ?",
            (_assert_declared_queue(queue), item_id),
```

### `u123.T1_adapter_vouching`

Drop the adapter's ledger check before a playlist removal

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T1_adapter_vouching`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_outbound_tidal_account.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
            raise refuse(
                "outbound-remove-refused",
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

New text:

```
        if False:
            raise refuse(
                "outbound-remove-refused",
                f"the outbound ledger does not record the playlist {identifier} as "
                f"one this product created, so it was not removed and the provider "
```

### `u123.T2_read_back`

Trust the delete and never read the playlist back

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u123.json`, row `T2_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_outbound_tidal_account.py`
- Collected: 149 against a baseline of 149
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`

Old text:

```
        if again is not _ABSENT and again is not None:
```

New text:

```
        if False:
```

### `r647-a.B16_serial_recorded_in_the_clear`

machine_identity: return the raw platform identifier instead of its digest, so a hardware serial is written into every lock and session record

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B16_serial_recorded_in_the_clear`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return hashlib.sha256(f"cratekit-machine:{raw}".encode()).hexdigest()[:32]
```

New text:

```
    return raw
```

### `r647-a.B17_macos_probe_reads_nothing`

_raw_machine_identity: the macOS branch finds nothing, so every holder on a Mac names no machine and a power loss is a dead end there

- File: `src/cratekit/core/session.py`
- Source: `r647-a.json`, row `B17_macos_probe_reads_nothing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_write_session.py`
- Collected: 22663 against a baseline of 22663
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
        return found.group(1) if found else None
```

New text:

```
        return None
```

### `u219.C1_rebuild_items_filtered`

crate rebuild: queue every native tree again, the intake tree included

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `C1_rebuild_items_filtered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_of_every_tree_leaves_the_intake_tree_alone`

Old text:

```
        items = tuple(t for t in tree_items(entries, tree_id) if engine.derivable(declared, t))
```

New text:

```
        items = tuple(t for t in tree_items(entries, tree_id))
```

### `u219.C2_rebuild_named_intake`

crate rebuild --tree inbox: queue it rather than asking the acceptance gate

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `C2_rebuild_named_intake`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 5 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_rebuild_naming_the_intake_tree_refuses_and_queues_nothing`
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`
  - `tests/test_resort_scope.py::test_a_second_restore_clears_the_acceptance_of_the_first`
  - `tests/test_resort_scope.py::test_an_aborted_acceptance_leaves_the_inbox_refusing`
  - `tests/test_resort_scope.py::test_the_routing_tree_stays_marked_after_inbox_is_accepted`

Old text:

```
        if tree_id is not None and not engine.derivable(declared, tree_id):
```

New text:

```
        if False:
```

### `u219.K2_accept_actor`

rebuild accept: record the command line's actor string rather than who answered the gate (R34)

- File: `src/cratekit/cli/rebuild.py`
- Source: `u219.json`, row `K2_accept_actor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_resort_scope.py`
- Collected: 24 against a baseline of 24
- Kills: 1 (killed)
- Killed:
  - `tests/test_resort_scope.py::test_a_restore_marked_inbox_is_accepted_by_a_named_person`

Old text:

```
        cfg, declared, tree_id, actor=ctx.gate.state.decisions[spec.name].actor
    )
```

New text:

```
        cfg, declared, tree_id, actor=ctx.args.actor
    )
```

### `u281.C1_refusal_said_as_blocked`

_unread_phrase: say a refusal as 'blocked on N' again, the wording the card replaces

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `C1_refusal_said_as_blocked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 5 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_discogs_refusal_remembered_for_the_run_is_not_counted_as_a_search_sent`
  - `tests/test_tag_workers.py::test_a_general_catalogue_unread_on_every_file_is_named_in_the_summary`
  - `tests/test_tag_workers.py::test_a_sweep_some_of_whose_refusals_were_a_challenge_says_how_many`
  - `tests/test_tag_workers.py::test_a_sweep_stops_asking_a_refusing_beatport_after_three_and_says_it_refused`
  - `tests/test_tag_workers.py::test_blocked_fallbacks_reach_every_artifact_and_the_summary_and_never_read_as_no_hit`

Old text:

```
    if word != searchers.Answer.BLOCKED.value:
        return f"{source} {word} on {count}"
```

New text:

```
    if True:
        return f"{source} {word} on {count}"
```

### `u281.W7_worker_run_key_without_attempt`

tagging.cli.handle: name the run by the job alone, so a resumed run inherits the last run's stop

- File: `src/cratekit/tagging/cli.py`
- Source: `u281.json`, row `W7_worker_run_key_without_attempt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_tag_workers.py`, `tests/test_beatport_refusal.py`
- Collected: 138 against a baseline of 138
- Kills: 1 (killed)
- Killed:
  - `tests/test_tag_workers.py::test_a_resumed_run_asks_a_refusing_beatport_again_from_its_first_file`

Old text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}@{job.attempts}")
```

New text:

```
            declared, refusals=searchers.for_run(f"{job.job_id}")
```

### `r815-a.W4_the_next_ordinal_is_past_the_floor`

_NEXT_ORDINAL: allocate one past the highest item alone, as before

- File: `src/cratekit/core/review.py`
- Source: `r815-a.json`, row `W4_the_next_ordinal_is_past_the_floor`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_judge.py`, `tests/test_label_genre_gate.py`, `tests/test_review_queue.py`
- Collected: 376 against a baseline of 376
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_judge.py::test_an_ordinal_a_withheld_item_held_is_never_given_to_a_later_one`
  - `tests/test_label_judge.py::test_the_floor_is_raised_and_never_lowered`

Old text:

```
    "(SELECT MAX(COALESCE((SELECT MAX(ordinal) FROM review_items), 0), "
    "COALESCE((SELECT MAX(ordinal) FROM ordinal_floor), 0)) + 1)"
```

New text:

```
    "(SELECT COALESCE((SELECT MAX(ordinal) FROM review_items), 0) + 1)"
```

### `r840-c.C1_the_function_is_handed_the_payload_as_it_stands`

review.redescribe: hand the function an empty payload and not the stored one, so a caller changing one field writes that field alone

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C1_the_function_is_handed_the_payload_as_it_stands`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 34 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_person_reads_each_release_without_asking_for_json`
  - `tests/test_label_artists.py::test_a_rewrite_given_a_function_is_handed_the_payload_and_writes_what_it_returns`
  - `tests/test_label_artists.py::test_a_second_run_asks_about_nothing_the_first_repaired`
  - `tests/test_label_artists.py::test_an_answer_between_failures_keeps_the_run_going`
  - `tests/test_label_artists.py::test_an_imported_item_is_read_by_the_identifier_its_payload_carries`
  - `tests/test_label_artists.py::test_an_open_item_reading_an_address_is_given_the_name_and_nothing_else_moves`
  - `tests/test_label_artists.py::test_the_counts_always_sum_to_the_addresses_and_the_items_left_alone`
  - `tests/test_label_artists.py::test_the_provider_is_asked_once_for_each_repaired_item_and_never_for_the_others`
  - `tests/test_label_artists.py::test_the_seams_own_refusal_stops_the_run_and_carries_what_was_repaired`
  - `tests/test_label_artists.py::test_two_items_naming_one_release_are_two_lines_under_two_keys`
  - `tests/test_label_artists.py::test_what_a_judging_job_stamped_meanwhile_is_kept`
  - `tests/test_label_judge.py::test_a_catalogue_that_refuses_stops_the_run_at_once_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_catalogue_unread_three_times_in_a_row_stops_the_run_and_says_how_many_were_left`
  - `tests/test_label_judge.py::test_a_fresh_answer_with_no_word_takes_the_old_words_off_the_item`
  - `tests/test_label_judge.py::test_a_label_marked_any_has_nothing_held_and_nobody_is_asked`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            wanted = payload(_payload_of(held["payload"]))
```

New text:

```
            wanted = payload({})
```

### `r840-c.C2_the_function_is_only_handed_an_open_item`

review.redescribe: read the payload of any item, so the function is called for one that is decided or carries a verdict this build cannot read

- File: `src/cratekit/core/review.py`
- Source: `r840-c.json`, row `C2_the_function_is_only_handed_an_open_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_artists.py`, `tests/test_label_judge.py`
- Collected: 137 against a baseline of 137
- Kills: 4 (killed)
- Killed:
  - `tests/test_label_artists.py::test_a_release_decided_while_it_was_being_read_is_not_rewritten`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[accepted]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_a_decided_item[rejected]`
  - `tests/test_label_artists.py::test_a_rewrite_is_not_handed_the_payload_of_an_item_with_an_unreadable_verdict`

Old text:

```
                "SELECT payload FROM review_items WHERE item_id = ? AND verdict IS NULL",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

New text:

```
                "SELECT payload FROM review_items WHERE item_id = ?",
                (item_id,),
            ).fetchone()
            if held is None:
                return None
            wanted = payload(
```

### `r837-a.A17_sweep_hand_off`

sync.cli: the sweep is handed no set playlist, so the exclusion has nothing to exclude

- File: `src/cratekit/sync/cli.py`
- Source: `r837-a.json`, row `A17_sweep_hand_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_collection.py`, `tests/test_export_set.py`, `tests/test_intake_writers_native.py`, `tests/test_label_playlists.py`, `tests/test_sync_all.py`
- Collected: 371 against a baseline of 371
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_sweep_never_reads_a_set_playlist_as_intake`

Old text:

```
            set_built=set_built,
```

New text:

```
            set_built=frozenset(),
```

### `r1032.S1_protocol_default_on`

TidalAccount.match_track: default any_agreeing on, so the hearts, the pairs and the exports, which never pass it, break the tie R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `S1_protocol_default_on`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_set.py`, `tests/test_sync_pair.py`
- Collected: 367 against a baseline of 367
- Kills: 15 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_stay_unmatched_and_the_reason_counts_them`
  - `tests/test_outbound_tidal_account.py::test_the_album_chooses_only_among_releases_that_agree_with_the_row`
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_without_any_agreeing_the_same_tie_still_refuses_in_the_words_the_mirror_reads`

Old text:

```
        album: str = "",
        any_agreeing: bool = False,
    ) -> str | None:
        """The one provider track this row names exactly, or ``None``.
```

New text:

```
        album: str = "",
        any_agreeing: bool = True,
    ) -> str | None:
        """The one provider track this row names exactly, or ``None``.
```

### `u135.A3_found_vs_made_collapsed`

The gate screen always says found-or-made when no recorded INBOX playlist is named

- File: `src/cratekit/intake/land_cli.py`
- Source: `u135.json`, row `A3_found_vs_made_collapsed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`, `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
- Collected: 2 against a baseline of 2
- Kills: 2 (killed)
- Killed:
  - `tests/test_u135_set_inbox_join.py::test_a_hand_made_inbox_playlist_of_the_set_name_is_named_found_not_recorded`
  - `tests/test_u135_set_inbox_join.py::test_a_set_landed_once_keeps_one_inbox_playlist_named_for_the_set`

Old text:

```
        if rows.batch_playlist_id:
            facts["inbox"] = (
                f"adds to the playlist an earlier landing of this set made "
                f"(row {rows.batch_playlist_id})"
            )
        elif rows.inbox_found_by_name:
            facts["inbox"] = "found live by name, not recorded"
        else:
            facts["inbox"] = "made"

```

New text:

```
        facts["inbox"] = (
            f"adds to the playlist an earlier landing of this set made "
            f"(row {rows.batch_playlist_id})"
            if rows.batch_playlist_id
            else "found live by its name under INBOX, or made"
        )

```

