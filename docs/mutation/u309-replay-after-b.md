# Mutation table: u309-replay-after-b

Measured by `scripts/mutate.py` on 2026-11-22 23:20 UTC, branch `HEAD` at `221233e4`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22910 collected. pytest invocations for this batch: 74.

Full baseline: measured by this driver (the battery's verdict was not read: this tree has uncommitted or untracked changes).

Subset baselines: 58, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard. 91 row(s) were reused from a prior sidecar and were measured by an earlier process, whose children this run did not watch.

Null control `NULL_CONTROL`: killed 0, collected 22910 against 22910. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r229.L2_exactly_half_is_not_enough` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L3_nothing_shared_is_a_match` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L4_an_eighth_of_the_crate` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r356-b.B8_heart_back_drops_the_reason` | `src/cratekit/modules/outbound/hearts.py` | user | 1 file(s) | 64 | 1 | killed |
| `u231.M5_positions_not_advanced` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 38 | killed |
| `r1394.A1_recorder_never_told` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 5 | killed |
| `u205.S1_account_lookup_ignores_app` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 179 | 17 | killed |
| `u142.S4_ambiguity_bound` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 228 | 1 | killed |
| `u142.S10_gate_folder_item_named_by_year` | `src/cratekit/export/set_archive.py` | user | 2 file(s) | 155 | 1 | killed |
| `r837-a.A2_asked_not_asked_again` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 2 | killed |
| `r879-b.S6_absent_music_folder_unsaid` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 1 | killed |
| `r837-b.B4_sole_exact_listed` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 20 | killed |
| `r837-a.A5_chunk_recorded` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 3 | killed |
| `r1017.M1_no_recorded_names` | `src/cratekit/export/set_rename.py` | user | 4 file(s) | 195 | 5 | killed |
| `u140.A4_rename_always` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 4 | killed |
| `u140.A3_refreeze_against_account_spelling` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 1 | killed |
| `u207.M3_mirror_read_never_screens` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 71 | 1 | killed |
| `u137.A1_labels_gate` | `src/cratekit/organize/account.py` | user | 2 file(s) | 117 | 9 | killed |
| `u143-c.A3_debris_served` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 446 | 2 | killed |
| `r835-c.T3_short_answer_read_again_again` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 286 | 1 | killed |
| `r835-a.F2_two_root_folders_refuse` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 1 | killed |
| `u230.M11_empty_there` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 1 | killed |
| `u227.R23_person_digest` | `src/cratekit/organize/mirror_downloads.py` | user | 7 file(s) | 184 | 1 | killed |
| `u236.M11_reader_never_placed` | `src/cratekit/organize/account_mirror.py` | user | 8 file(s) | 223 | 1 | killed |
| `u236.M6_mine_includes_now` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 1 | killed |
| `u236.M1_ours_empty` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 10 | killed |
| `u201.L1_agreed_own_playlist` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 5 file(s) | 185 | 1 | killed |
| `u201.O3_target_bucket` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 185 | 6 | killed |
| `u204.D4_never_lands_named` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 222 | 2 | killed |
| `u204.D2_write_rereads_queue` | `src/cratekit/organize/mirror_downloads.py` | user | 6 file(s) | 222 | 1 | killed |
| `u204.O4_colour` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u137.C1_named_always` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 95 | 17 | killed |
| `u137.R5_record_labels_gate` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 4 | killed |
| `u142.S14_any_inspiration_proves_every_set` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u116.M5_ambiguous_moves_anyway` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.S1_digest_drops_step_plans` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 95 | 24 | killed |
| `u112-b.C7_outcome_always_ok` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.R2_applied_entries_outstanding` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 1 | killed |
| `u137.S4_selection_ignores_only` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 95 | 21 | killed |
| `r1295.M5_all_unread_branch` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u144-b.B8_commit_recorded` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M3_read_positions_renumbered` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `u144-b.B6_read_back_missing` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M4_unread_positions_renumbered` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 3 | killed |
| `u144-b.B7_writes_the_members` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 8 | killed |
| `u147-d.A6_file_code_trusted` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 37 | 1 | killed |
| `u147-a.M5_persons_playlist` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 2 | killed |
| `r1289.M15_mirror_reads_whole` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 103 | 1 | killed |
| `r1031.M22_record_binding_unchecked` | `src/cratekit/organize/mirror_frozen.py` | user | 2 file(s) | 132 | 2 | killed |
| `r1031.M6_misses_never_gathered` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 6 | killed |
| `r1031.M17_apply_records_no_miss` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 71 | 5 | killed |
| `r1031.M18_unrecordable_ledger_refuses_the_plan` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 71 | 1 | killed |
| `u222.M2_overlay_never_replaces` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 4 | killed |
| `u222.M13_moved_equal_named` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 5 | killed |
| `u222.M23_cli_empty_stale_reworded` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 251 | 1 | killed |
| `u150.A8_landed_workflow` | `src/cratekit/organize/account_mirror.py` | maintainer | 2 file(s) | 90 | 1 | killed |
| `u150.M10_link_before_known` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u150.M6_apply_forgets` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 3 | killed |
| `u150.A2_present_titled` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 69 | 1 | killed |
| `u143-b.K1_legacy_name_exact` | `src/cratekit/modules/outbound/kinds.py` | user | 3 file(s) | 192 | 2 | killed |
| `u143-e.P2_tracks_unchanged` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u255.M2_membership_reads_the_held_object` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.M5_membership_reuses_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u270.E5_noted_rows_are_written` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 134 | 1 | killed |
| `u270.C4_created_said_once` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 2 | killed |
| `u220.A11_cause_chain_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |
| `r1308.M16_no_break` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 10 | killed |
| `r1308.M18_not_forgotten` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 2 | killed |
| `r1308.M23_read_back_bypassed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 34 | killed |
| `r227.A4_no_tolerance` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `r227.A6_conversion_unguarded` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 1 | killed |
| `u208.M21_adapter_every_choice_a_tie` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 134 | 1 | killed |
| `r356-a.A1_first_agreeing_rather_than_the_only_one` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 27 | killed |
| `r572.A4_no_fold` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 3 | killed |
| `r356-a.A5_withdrawn_track_is_a_candidate` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 2 | killed |
| `r834.M3_a_refused_private_step_does_not_lose_the_playlist` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 2 | killed |
| `u226.M10_settle_lag_known_only` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 5 | killed |
| `r850-a.E3_listing_dropped` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 6 | killed |
| `u131.K11_filing_in_digest` | `src/cratekit/export/cli.py` | user | 2 file(s) | 137 | 1 | killed |
| `u51-item-derivation.D6_export_required` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 2 | killed |
| `r227.C4_export_limit_spelled` | `src/cratekit/export/cli.py` | user | 1 file(s) | 123 | 1 | killed |
| `u51-item-derivation.H3_frozen_config_ignored` | `src/cratekit/export/cli.py` | user | 1 file(s) | 32 | 1 | killed |
| `u131.K1_mine_made_only` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 109 | 1 | killed |
| `u131.K3_product_made_left` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 109 | 1 | killed |
| `u261.A3_account_records_no_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 143 | 5 | killed |
| `r836-f.P8_drifted_match_left_alone` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-b.L2_export_records_are_made_here` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 4 | killed |
| `u174.O1_native_loop` | `src/cratekit/organize/account.py` | user | 2 file(s) | 164 | 4 | killed |
| `u202-composites.P1_reserve_held` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 158 | 1 | killed |
| `u221.R16_release_any_rekordbox_side` | `src/cratekit/modules/outbound/pairs.py` | user | 1 file(s) | 32 | 1 | killed |
| `u242.M7_inspiration_reads_the_title_alone` | `src/cratekit/organize/inspiration.py` | user | 2 file(s) | 84 | 1 | killed |
| `r837-a.A7_reserve_reuses_recorded` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 5 file(s) | 416 | 5 | killed |
| `u214.M8_plan_left_lines` | `src/cratekit/modules/outbound/mirror.py` | user | 6 file(s) | 199 | 4 | killed |
| `u143-d.A5_playlist_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 446 | 5 | killed |
| `u230.M13_held_by_dropped` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 28 | killed |
| `u230.M12_queue_not_handed` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 6 | killed |
| `u227.R6_landed_item` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 7 file(s) | 184 | 1 | killed |
| `u201.M1_plan_keeps` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 185 | 6 | killed |
| `u201.M2_plan_skips` | `src/cratekit/modules/outbound/mirror.py` | user | 5 file(s) | 185 | 5 | killed |
| `u255.M3_membership_holds_nothing` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 6 | killed |
| `r1032.A1_adapter_ignores_any_agreeing` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 13 | killed |
| `r358-round-2.A3_editor_check` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `u226.M11_settle_kept_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 442 | 1 | killed |
| `r836-a.A5_removal_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 501 | 1 | killed |
| `u216.M21_reserve_adopt_empty` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 9 | killed |

## Row definitions

### `r229.L2_exactly_half_is_not_enough`

Exactly half no longer qualifies, the boundary moved from at least to more than

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L2_exactly_half_is_not_enough`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L3_nothing_shared_is_a_match`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L4_an_eighth_of_the_crate`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

### `r356-b.B8_heart_back_drops_the_reason`

An unmatched favourite never carries what the account said about it

- File: `src/cratekit/modules/outbound/hearts.py`
- Source: `r356-b.json`, row `B8_heart_back_drops_the_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_heart_back_hands_the_account_the_names_and_reports_its_reasons`

Old text:

```
            if reason:
                reasons.append((item.row_id, reason))
```

New text:

```
            if False:
                reasons.append((item.row_id, reason))
```

### `u231.M5_positions_not_advanced`

adapter order: each move's position is read off the reading as it was, not with the moves before it applied

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u231.json`, row `M5_positions_not_advanced`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 38 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_412_on_a_stale_tag_is_read_again_and_the_move_made_on_the_new_reading`
  - `tests/test_outbound_order.py::test_a_412_on_the_third_move_resends_that_move_once_and_no_other`
  - `tests/test_outbound_order.py::test_a_move_that_lands_anywhere_else_is_not_read_back_and_the_settle_reading_shows_it`
  - `tests/test_outbound_order.py::test_a_provider_whose_move_to_the_length_lands_one_short_still_takes_the_order`
  - `tests/test_outbound_order.py::test_a_read_that_lags_every_move_does_not_stop_the_order`
  - `tests/test_outbound_order.py::test_a_reading_holding_what_the_adds_left_in_another_order_is_not_stale`
  - `tests/test_outbound_order.py::test_a_reading_that_agrees_with_the_expected_one_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_agreed_order_once_is_read_again_and_takes_the_order`
  - `tests/test_outbound_order.py::test_a_reading_that_lags_the_expected_one_is_read_again`
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_order.py::test_an_added_track_the_provider_placed_elsewhere_is_not_refused`
  - `tests/test_outbound_order.py::test_every_move_is_planned_from_one_reading_and_sent_with_no_read_between`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before0-order0]`
  - `tests/test_outbound_order.py::test_the_fake_account_orders_by_the_adapters_rule[before1-order1]`
  - ... and 23 more, see the JSON sidecar

Old text:

```
            now = _fronted(now, one)
            note["moved"] += 1
```

New text:

```
            note["moved"] += 1
```

### `r1394.A1_recorder_never_told`

adapter order: the recorder begun answers is never told before a move, so the record keeps sent and landed at 0 while moves land

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A1_recorder_never_told`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                if told is not None:
                    told(number, number - 1)
```

New text:

```
                if False:
                    told(number, number - 1)
```

### `u205.S1_account_lookup_ignores_app`

outbound account: ISRC lookups go to the account session whatever the opener built

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u205.json`, row `S1_account_lookup_ignores_app`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_catalogue_app.py`, `tests/test_outbound_tidal_account.py`
- Collected: 179 against a baseline of 179
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

### `u142.S4_ambiguity_bound`

plan_archive: refuse only three folders of the name, so one of two Downloaded Sets folders is picked silently

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S4_ambiguity_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_two_folders_named_as_the_year_refuse_and_write_nothing`

Old text:

```
        if len(named) > 1:
            raise _ambiguous_folder(name, named)
```

New text:

```
        if len(named) > 2:
            raise _ambiguous_folder(name, named)
```

### `u142.S10_gate_folder_item_named_by_year`

export archive payload: name the folder item by the plain year, so the plan shows a folder that is not the one written

- File: `src/cratekit/export/set_archive.py`
- Source: `u142.json`, row `S10_gate_folder_item_named_by_year`
- Moved: the same text, now in src/cratekit/export/set_archive.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`
- Collected: 155 against a baseline of 155
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_the_archive_takes_records_and_files_it_in_a_year_folder_made_once`

Old text:

```
                "name": planned.folder_name,
```

New text:

```
                "name": planned.year,
```

### `r837-a.A2_asked_not_asked_again`

sets.plan_set: a track written or refused before is asked for again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A2_asked_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`

Old text:

```
        add=tuple(one for one in wanted if one not in asked and one not in held),
```

New text:

```
        add=tuple(one for one in wanted if one not in held),
```

### `r879-b.S6_absent_music_folder_unsaid`

file_isrc: drop the absent music folder check, so an unmounted volume reads as a library holding nothing

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S6_absent_music_folder_unsaid`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_an_absent_music_folder_is_said_and_never_read_as_holding_nothing`

Old text:

```
        if not self.music.is_dir():
```

New text:

```
        if False:
```

### `r837-b.B4_sole_exact_listed`

set_cli.match_rows: the one exact search candidate is never listed, so every typed row is left out

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B4_sole_exact_listed`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 20 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_full_first_page_with_one_exact_and_a_second_with_none_lists_it`
  - `tests/test_export_set.py::test_a_name_with_a_slash_finds_the_set_it_named_at_build`
  - `tests/test_export_set.py::test_a_playlist_already_in_its_folder_is_left`
  - `tests/test_export_set.py::test_a_playlist_retitled_by_a_person_is_filed_and_its_title_left`
  - `tests/test_export_set.py::test_a_playlist_the_folder_does_not_list_yet_is_not_renamed_or_blamed`
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_export_set.py::test_a_second_run_onto_the_same_set_plans_nothing`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`
  - `tests/test_export_set.py::test_an_exact_match_on_the_second_page_alone_is_listed`
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`
  - ... and 5 more, see the JSON sidecar

Old text:

```
            sole = candidates.sole_exact(answer)
```

New text:

```
            sole = None
```

### `r837-a.A5_chunk_recorded`

sets.apply_set: a chunk written is not recorded, so a resume asks for it again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A5_chunk_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 3 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`
  - `tests/test_export_set.py::test_a_track_taken_off_by_a_person_is_said_and_not_put_back`
  - `tests/test_export_set.py::test_approved_the_account_holds_a_private_playlist_of_four_in_order`

Old text:

```
        ledger.record_set_tracks(cfg, planned.name, added=added, refused=refused)
```

New text:

```
        pass
```

### `r1017.M1_no_recorded_names`

Rename: drop the names the landings recorded from the names looked up, the defect R-1017 names

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M1_no_recorded_names`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`
  - `tests/test_export_set_rename.py::test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record`
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`
  - `tests/test_export_set_rename.py::test_two_playlists_under_two_older_names_are_a_twin_not_a_choice`

Old text:

```
    recorded = tuple(set_name(one) for one in set_playlist.recorded_names(cfg, job.job_id))
```

New text:

```
    recorded = ()
```

### `u140.A4_rename_always`

RenamePlan.rename is always true, so a second run renames on the account again

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A4_rename_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 4 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`

Old text:

```
        return self.playlist.name != self.to

```

New text:

```
        return True

```

### `u140.A3_refreeze_against_account_spelling`

RenamePlan.refreeze compares the frozen name with the account spelling, not the library's

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A3_refreeze_against_account_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`

Old text:

```
        return self.frozen != (self.live or self.to)

```

New text:

```
        return self.frozen != self.to

```

### `u207.M3_mirror_read_never_screens`

account mirror read: the plans' rows are never screened

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u207.json`, row `M3_mirror_read_never_screens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_tie.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any`

Old text:

```
    matcher.screen(
```

New text:

```
    (lambda rows: 0)(
```

### `u137.A1_labels_gate`

Plan the label steps whatever the selection

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A1_labels_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 117 against a baseline of 117
- Kills: 9 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
    if area.wants(LABELS):
```

New text:

```
    if True:
```

### `u143-c.A3_debris_served`

Adapter: accept any served name as debris

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-c.json`, row `A3_debris_served`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 446 against a baseline of 446
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served0-debris]`
  - `tests/test_organize_root.py::test_a_playlist_the_provider_serves_as_not_of_the_kind_is_refused_before_any_delete[served1-debris]`

Old text:

```
            served = is_library_debris(name)
```

New text:

```
            served = True
```

### `r835-c.T3_short_answer_read_again_again`

TidalAccount.add_tracks: an add answer that leaves a track out is trusted, so a track the playlist holds is reported refused

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-c.json`, row `T3_short_answer_read_again_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`
- Collected: 286 against a baseline of 286
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_an_add_answered_with_nothing_is_read_again_and_not_reported_refused`

Old text:

```
            if unconfirmed:
                del self._members[playlist_id]
```

New text:

```
            if False:
                del self._members[playlist_id]
```

### `r835-a.F2_two_root_folders_refuse`

folders.plan: two root folders under the label's name are not refused, and the first by identifier is adopted

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F2_two_root_folders_refuse`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_two_root_folders_named_as_the_label_refuse_and_write_nothing`

Old text:

```
        if len(named) > 1:
            raise _ambiguous_folder(catalogue.name, named)
```

New text:

```
        if False:
            raise _ambiguous_folder(catalogue.name, named)
```

### `u230.M11_empty_there`

_filed_by_landing: a track rekordbox holds in no band reads as the landing's filing

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M11_empty_there`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_row_taken_out_of_the_tree_in_rekordbox_is_not_lifted_over`

Old text:

```
    return bool(there) and all((place.folder, place.playlist) in places for place in there)
```

New text:

```
    return all((place.folder, place.playlist) in places for place in there)
```

### `u227.R23_person_digest`

filed: read an approval a person gave adopt apply as the landing's (round two's F2)

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R23_person_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_persons_first_filing_after_a_landing_that_filed_nothing_is_not_the_landings`

Old text:

```
        if entry.tree == tree and entry.digest not in by_person:
```

New text:

```
        if entry.tree == tree:
```

### `u236.M11_reader_never_placed`

read edits: hand the rule no placement on a playlist never mirrored, the month the write made

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u236.json`, row `M11_reader_never_placed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted), placed=ours))
```

New text:

```
                read.append(edits.Mirrored(place=place, rekordbox=frozenset(wanted)))
```

### `u236.M6_mine_includes_now`

decide favorites: leave a placed month the account holds too

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M6_mine_includes_now`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_the_placed_month_on_the_account_is_agreed`

Old text:

```
            mine = ours - now_m
```

New text:

```
            mine = ours
```

### `u236.M1_ours_empty`

decide favorites: read no placement, so the library's own month beats the unfavourite again (sitting 88)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M1_ours_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 10 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_a_favourite_put_in_another_month_leaves_the_placed_one`
  - `tests/test_mirror_edits_u236.py::test_an_unfavourite_over_the_month_the_library_placed_is_carried`
  - `tests/test_mirror_edits_u236.py::test_the_same_over_a_placed_month_never_agreed`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
        ours = frozenset(
            one.place for one in playlists if not one.place.primary and track in one.placed
        )
```

New text:

```
        ours = frozenset()
```

### `u201.L1_agreed_own_playlist`

record_mirror_agreed: a snapshot lands on a playlist recorded under the title with another identifier

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u201.json`, row `L1_agreed_own_playlist`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_the_ledger_keeps_a_snapshot_apart_from_none_and_only_on_its_own_playlist`

Old text:

```
            if not entry or str(entry.get("remote_id") or "") != str(remote_id):
                continue
            base =
```

New text:

```
            if not entry:
                continue
            base =
```

### `u201.O3_target_bucket`

target_tags: a genre word filing into another bucket is taken

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O3_target_bucket`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_mirror_made_before_u201_is_agreed_by_its_first_run_and_an_edit_after_it_is_taken`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Minimal / Deep Tech-Low Energy-Deep House-9-expected6]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-Med-Deep House-2-expected0]`
  - `tests/test_organize_mirror_edits.py::test_the_tags_are_the_nearest_pair_routing_files_into_the_place[Tech House-None-Deep House-5-expected4]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
        if routing.resolve_bucket(declared, word).bucket_id != bucket_id:
```

New text:

```
        if False:
```

### `u204.D4_never_lands_named`

mirror_downloads.outcomes: a finished download that found the track owned is said to await its landing

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D4_never_lands_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_finished_download_that_never_lands_is_never_said_to_await_one[missing-could not be fetched]`
  - `tests/test_organize_mirror_edits_u204.py::test_a_finished_download_that_never_lands_is_never_said_to_await_one[owned-already holds it]`

Old text:

```
                why = _NEVER_LANDS.get(str(report.get("state")))
```

New text:

```
                why = None
```

### `u204.D2_write_rereads_queue`

mirror_downloads.write: two plans approved one after the other queue a track twice

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u204.json`, row `D2_write_rereads_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_two_plans_approved_one_after_the_other_queue_a_track_once`

Old text:

```
            fresh = {track: frozen for track, frozen in tracks.items() if track not in already}
```

New text:

```
            fresh = dict(tracks)
```

### `u204.O4_colour`

_plan_favourites: a favourite with no colour is not coloured Pink

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O4_colour`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_added_to_all_favorites_is_favourited_in_its_month_and_coloured`

Old text:

```
        takes = bool(pink) and decision.content_id in colour.sort_rows(db, pink, [decision.content_id]).to_colour
```

New text:

```
        takes = False
```

### `u137.C1_named_always`

Plan an area none of whose kinds is named

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C1_named_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 17 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - ... and 2 more, see the JSON sidecar

Old text:

```
    return selection(kinds, only) != ()
```

New text:

```
    return True
```

### `u137.R5_record_labels_gate`

Plan the record labels listing whatever the selection

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R5_record_labels_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
    if area.wants(RECORD_LABELS):
```

New text:

```
    if True:
```

### `u142.S14_any_inspiration_proves_every_set`

organize set step: take any INSPIRATION playlist as proof for every set, not one of the set's own name

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S14_any_inspiration_proves_every_set`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_of_the_sets_name_outside_inspiration_or_removed_proves_nothing`

Old text:

```
            if held is None or name not in held:
```

New text:

```
            if held is None or not held:
```

### `u116.M5_ambiguous_moves_anyway`

_year_folder: two folders named as the year adopt the first rather than leave

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M5_ambiguous_moves_anyway`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_two_root_folders_named_as_the_year_leave_its_playlists_reported`

Old text:

```
    if len(named) > 1:
```

New text:

```
    if len(named) > 9:
```

### `u112.S1_digest_drops_step_plans`

The area digest covers each step's key and state and not its own plan's digest

- File: `src/cratekit/organize/steps.py`
- Source: `u112.json`, row `S1_digest_drops_step_plans`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 24 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[False]`
  - `tests/test_organize.py::test_a_marked_playlist_already_in_a_folder_is_left_where_it_is[True]`
  - `tests/test_organize.py::test_a_marked_playlist_at_the_root_moves_into_its_year_folder`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_missing_year_folder_is_created_once_and_reused`
  - `tests/test_organize.py::test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied`
  - `tests/test_organize.py::test_a_prefixed_playlist_no_sync_recorded_is_still_filed_in_mine`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[False]`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved[True]`
  - `tests/test_organize.py::test_a_push_stamped_with_the_zero_date_reads_as_no_push_at_all_west_of_utc`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_a_stale_rekordbox_refusal_shows_the_moved_plan_and_the_decide_after_it_files_it`
  - ... and 9 more, see the JSON sidecar

Old text:

```
        said = self.digest if self.cause is None else f"refused:{self.cause.reason}"
```

New text:

```
        said = None if self.cause is None else f"refused:{self.cause.reason}"
```

### `u112-b.C7_outcome_always_ok`

A run that wrote nothing ends OK rather than as a no-op

- File: `src/cratekit/organize/cli.py`
- Source: `u112-b.json`, row `C7_outcome_always_ok`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_run_that_writes_nothing_ends_as_a_no_op`

Old text:

```
        outcome=Outcome.OK if wrote else Outcome.NO_OP,
```

New text:

```
        outcome=Outcome.OK,
```

### `u112.R2_applied_entries_outstanding`

Adoption plans every placeable entry, the ones a finished apply already filed included

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R2_applied_entries_outstanding`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_second_run_after_a_full_apply_plans_nothing`

Old text:

```
        pending = apply_engine.outstanding(plan, apply_engine.read(cfg))
```

New text:

```
        pending = plan.applicable()
```

### `u137.S4_selection_ignores_only`

Take every kind of the area as selected when --only names any

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S4_selection_ignores_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 21 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize.py::test_a_mirror_plan_that_moves_again_after_the_second_answer_is_stale_and_writes_nothing`
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_a_run_resumed_with_no_account_answer_plans_the_mirror_afresh`
  - `tests/test_organize.py::test_a_stale_mirror_refusal_shows_the_moved_plan_and_the_decide_after_it_applies_that_plan`
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_moves_a_marked_playlist_as_the_full_verb_does_and_then_plans_nothing`
  - ... and 6 more, see the JSON sidecar

Old text:

```
    return tuple(kind for kind in kinds if kind in only)
```

New text:

```
    return tuple(kinds)
```

### `r1295.M5_all_unread_branch`

plan: drop the every track unread branch, so such a set reads as one with no match

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M5_all_unread_branch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_is_filed_unread_naming_each`
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
        if listing.unread and not listing.wanted:
```

New text:

```
        if False:
```

### `u144-b.B8_commit_recorded`

Record: record no commit, so a restore cannot weigh the session

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B8_commit_recorded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`

Old text:

```
    made = [one for one in wrote if one.added or one.created]
```

New text:

```
    made = []
```

### `r1295.M3_read_positions_renumbered`

_read: a read track's place counts only the rows read, so a miss after an unread row is misplaced

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M3_read_positions_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
            wanted.append((position, match.read_row(
```

New text:

```
            wanted.append((len(wanted) + 1, match.read_row(
```

### `u144-b.B6_read_back_missing`

Read back: accept a found playlist missing a planned row

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B6_read_back_missing`
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
        if one.created and not exact:
```

### `r1295.M4_unread_positions_renumbered`

_read: an unread track's place counts only the unread rows

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M4_unread_positions_renumbered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`

Old text:

```
            unread.append((position, one))
```

New text:

```
            unread.append((len(unread) + 1, one))
```

### `u144-b.B7_writes_the_members`

Write: add every member but the first

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B7_writes_the_members`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_readable_track_with_no_provider_id_is_matched_as_before`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_artist_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 A b2b B / Night 10-18-5_28_26 A b2b B - Night 10-18]`
  - `tests/test_organize_inspiration.py::test_the_name_written_is_the_account_name_without_its_prefix[DOWNLOADED 5_28_26 Probe DJ Femme House Mix 10-18-5_28_26 Probe DJ Femme House Mix 10-18]`

Old text:

```
        added = rb_writer.add_memberships(db, playlist, row.members)
```

New text:

```
        added = rb_writer.add_memberships(db, playlist, row.members[1:])
```

### `u147-d.A6_file_code_trusted`

account_mirror.identify: a code read off the file does not ask the track to agree

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A6_file_code_trusted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`, `tests/test_organize_mirror_library.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_code_read_off_the_file_asks_the_one_track_to_agree_and_a_database_code_does_not`

Old text:

```
            (isrc, album), agree = pair_cli.file_identity(cfg, row.path), True
```

New text:

```
            (isrc, album), agree = pair_cli.file_identity(cfg, row.path), False
```

### `u147-a.M5_persons_playlist`

mirror.plan: never leave a person's playlist of the same title, make one beside it

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-a.json`, row `M5_persons_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_persons_playlist_left_alone_costs_no_match`
  - `tests/test_organize_mirror.py::test_a_persons_playlist_of_the_same_title_is_left_and_nothing_made_beside_it`

Old text:

```
        theirs = sorted(pid for pid, name in inside.items() if name == source.name)
        if theirs:
```

New text:

```
        theirs = sorted(pid for pid, name in inside.items() if name == source.name)
        if False:
```

### `r1289.M15_mirror_reads_whole`

mirror_downloads._catalogue_listing: read the playlist whole again (the declared reader is asked first), so one untitled row names every wanted track on it

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M15_mirror_reads_whole`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
        return intake_cli.list_playlist_readable(found[0], playlist_id)
```

New text:

```
        intake_cli.list_playlist_declared(found[0], playlist_id)
        return intake_cli.list_playlist_readable(found[0], playlist_id)
```

### `r1031.M22_record_binding_unchecked`

mirror_frozen.load: rebuild from a record of another version or another run

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `r1031.json`, row `M22_record_binding_unchecked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`
- Collected: 132 against a baseline of 132
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_frozen_plan_of_another_version_or_run_is_not_rebuilt`
  - `tests/test_organize_mirror_frozen.py::test_each_folders_edit_rule_survives_the_freeze_and_a_version_3_record_is_planned_afresh`

Old text:

```
        if data.get("version") != VERSION or data.get("run_id") != run_id:
```

New text:

```
        if False:
```

### `r1031.M6_misses_never_gathered`

Matcher._missed: gather no miss, so nothing is remembered

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M6_misses_never_gathered`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_coded_rows_miss_is_kept_whatever_its_file_does`
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`
  - `tests/test_organize_mirror_frozen.py::test_a_miss_is_recorded_by_the_run_that_shows_the_gate_with_nothing_applied`
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_row_matched_later_loses_its_miss`

Old text:

```
            self.missed[row.content_id] = (reason, under)
```

New text:

```
            pass
```

### `r1031.M17_apply_records_no_miss`

_apply: record no miss at the apply, so a plan with no run remembers nothing

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M17_apply_records_no_miss`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_coded_rows_miss_is_kept_whatever_its_file_does`
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_candidate_that_could_not_be_read_is_never_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_refresh_asks_only_the_rows_new_since_the_last_and_names_the_rest_remembered`
  - `tests/test_organize_mirror_frozen.py::test_a_row_matched_later_loses_its_miss`

Old text:

```
            ledger.record_mirror_misses(cfg, matcher.missed)
            mirror.apply(cfg, account, planned, done, links=matcher.fresh)
```

New text:

```
            mirror.apply(cfg, account, planned, done, links=matcher.fresh)
```

### `r1031.M18_unrecordable_ledger_refuses_the_plan`

_record: let a ledger that cannot take the links escape the plan instead of saying so

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M18_unrecordable_ledger_refuses_the_plan`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_ledger_that_cannot_take_the_links_leaves_the_plan_standing_and_says_so`

Old text:

```
    except CratekitError as exc:
        return f"{said}not frozen: what the plan matched could not be recorded ({exc.cause.message})"
```

New text:

```
    except ValueError as exc:
        return f"{said}not frozen: what the plan matched could not be recorded ({exc})"
```

### `u222.M2_overlay_never_replaces`

overlay: keep the live snapshot of every playlist, the frozen one never taken

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M2_overlay_never_replaces`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_playlist_made_again_between_the_acts_reads_its_snapshot_now`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`

Old text:

```
                one = replace(one, agreed=held[1])
```

New text:

```
                one = one
```

### `u222.M13_moved_equal_named`

moved: name every step, moved or not

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M13_moved_equal_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_write_outside_any_mirrored_playlist_between_the_acts_is_not_stale`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`
  - `tests/test_organize_mirror_frozen_u222.py::test_with_nothing_between_the_acts_the_apply_rebuilds_the_frozen_plan`

Old text:

```
        if digest_of(step.identity()) == then.digest:
            continue

```

New text:

```
(empty)
```

### `u222.M23_cli_empty_stale_reworded`

_ask: reword a stale refusal whose area has nothing to add

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M23_cli_empty_stale_reworded`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_plan_that_moves_after_the_answer_is_stale_rather_than_applied`

Old text:

```
        if exc.cause.code != ExitCode.DECISION_STALE or not area.stale:
```

New text:

```
        if exc.cause.code != ExitCode.DECISION_STALE:
```

### `u150.A8_landed_workflow`

landed_tracks: read every workflow's record, not only a native landing's

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A8_landed_workflow`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_intake_land_labels_native.py`
- Collected: 90 against a baseline of 90
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_landed_tracks_reads_every_native_landings_provider_tracks`

Old text:

```
        if record.workflow != native.WORKFLOW:
            continue
        held = record.detail.get(label_filing.PROVIDER_KEY)
```

New text:

```
        held = record.detail.get(label_filing.PROVIDER_KEY)
```

### `u150.M10_link_before_known`

Matcher: take the landing track before the ledger's link, so a linked row is switched to another track

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M10_link_before_known`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_live_batch_made_by_a_label_landing_plans_its_playlist_with_the_batchs_tracks`
  - `tests/test_organize_mirror_inbox.py::test_a_row_the_ledger_already_links_keeps_its_link_over_a_landing_track`

Old text:

```
        linked = self._links.get(row.content_id)
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
```

New text:

```
        linked = self._links.get(row.content_id)
        if row.content_id in self._known:
            return self._known[row.content_id], row.isrc, ""
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
```

### `u150.M6_apply_forgets`

mirror.apply: keep the ledger record of a removed playlist, so every later refresh plans the removal again

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M6_apply_forgets`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_a_playlist_already_gone_from_the_account_is_still_forgotten`

Old text:

```
        ledger.forget_mirror_playlist(cfg, planned.name, name, remote_id)
        done.retired.append(name)
```

New text:

```
        done.retired.append(name)
```

### `u150.A2_present_titled`

account_mirror._inbox: hold INBOX's bare names as present instead of their account titles, so every still present title reads as gone

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A2_present_titled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_library.py`, `tests/test_organize_mirror.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_inbox_folder_reads_each_batch_under_its_account_title_with_its_rows`

Old text:

```
        present=frozenset(mirror.title(name, one) for one in live.present),
```

New text:

```
        present=frozenset(live.present),
```

### `u143-b.K1_legacy_name_exact`

Legacy name: search rather than match the whole name

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u143-b.json`, row `K1_legacy_name_exact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`, `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 192 against a baseline of 192
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_only_a_year_and_these_exact_words_name_a_legacy_folder[2026 Custom Playlists 2-]`
  - `tests/test_organize_root.py::test_only_a_year_and_these_exact_words_name_a_legacy_folder[My 2026 Custom Playlists-]`

Old text:

```
    found = _LEGACY_YEAR.fullmatch(str(name or ""))
```

New text:

```
    found = _LEGACY_YEAR.search(str(name or ""))
```

### `u143-e.P2_tracks_unchanged`

Apply: remove a debris playlist given a track since the gate was answered

- File: `src/cratekit/organize/root.py`
- Source: `u143-e.json`, row `P2_tracks_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_given_a_track_since_the_plan_is_kept_and_the_rest_removed`

Old text:

```
        if not now <= set(row.tracks):
```

New text:

```
        if False:
```

### `u255.M2_membership_reads_the_held_object`

_membership: read the tracks through the opened object itself, so the client's tracks read overwrites its tag and leaves its length, round one's BLOCKING

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M2_membership_reads_the_held_object`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_playlist_read_one_write_behind_writes_nothing`
  - `tests/test_outbound_add_requests.py::test_a_tracks_read_one_write_behind_never_reaches_the_add`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`

Old text:

```
            tracks = self._listed(playlist_id, copy.copy(opened))
```

New text:

```
            tracks = self._listed(playlist_id, opened)
```

### `u255.M5_membership_reuses_the_hold`

_membership: read through a held object when one is held, so the read back of an answer without the track reads a held object, not a fresh open

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M5_membership_reuses_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_found_gone_forgets_the_membership_it_was_remembered_with`

Old text:

```
            opened = self._playlist(playlist_id)

```

New text:

```
            opened = self._opened.get(playlist_id) or self._playlist(playlist_id)

```

### `u270.E5_noted_rows_are_written`

apply: write the ledger only when a track landed, so the rows of tracks recorded before R-836 are never named

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E5_noted_rows_are_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_prune.py`
- Collected: 134 against a baseline of 134
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_re_export_names_the_rows_of_tracks_recorded_before_rows_were_kept`

Old text:

```
    if landed or noted:
```

New text:

```
    if landed:
```

### `u270.C4_created_said_once`

run_export_items: every item of the batch that created the playlist reports the create

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C4_created_said_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_created_playlist_is_said_once_for_the_batch`
  - `tests/test_outbound_workers.py::test_an_export_runs_pending_to_done_and_its_artifact_reads_back`

Old text:

```
            "created": report.created and first_said,
```

New text:

```
            "created": report.created,
```

### `u220.A11_cause_chain_only`

_stale_tag: walk the cause chain alone, so a 412 the client failed to decode is missed (round one R3)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A11_cause_chain_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
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

### `r1308.M16_no_break`

_removal_read_back: no break on a wrong reading, so it is read again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M16_no_break`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 10 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
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
- Collected: 388 against a baseline of 388
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

### `r1308.M23_read_back_bypassed`

remove_tracks: take the expected list as read back without reading

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M23_read_back_bypassed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 34 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_track_this_write_took_off_is_not_asked_of_the_reading`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[count]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[tracks]`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_catches_up_on_the_last_reading_is_taken_as_done`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[count]`
  - `tests/test_outbound_remove_lag.py::test_a_read_that_never_catches_up_refuses_saying_the_removal_may_have_landed[tracks]`
  - ... and 19 more, see the JSON sidecar

Old text:

```
            playlist, before = self._removal_read_back(identifier, before, expected)
```

New text:

```
            playlist, before = self._playlist(identifier), expected
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

### `u208.M21_adapter_every_choice_a_tie`

_among: call every any_agreeing choice a broken tie, an album naming one included

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u208.json`, row `M21_adapter_every_choice_a_tie`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_tie.py`
- Collected: 134 against a baseline of 134
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

### `r356-a.A1_first_agreeing_rather_than_the_only_one`

Rule one takes the first agreeing track instead of requiring exactly one, which is the first result the unit's brief forbids

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A1_first_agreeing_rather_than_the_only_one`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 27 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_neither_release_stays_unmatched_and_says_so`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_stays_unmatched_and_says_the_tag_is_missing`
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_lone_heart_and_a_lone_album_choose_as_they_always_did`
  - `tests/test_outbound_tidal_account.py::test_a_lone_release_a_lone_heart_or_a_lone_album_is_never_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_a_reason_does_not_outlive_the_match_it_was_about`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_a_title_that_reads_two_ways_agrees_under_either_and_still_needs_one`
  - ... and 12 more, see the JSON sidecar

Old text:

```
        if len(agreeing) == 1 and not unreadable:
```

New text:

```
        if agreeing and not unreadable:
```

### `r572.A4_no_fold`

Compare the album raw rather than folded

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r572.json`, row `A4_no_fold`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`
  - `tests/test_outbound_tidal_account.py::test_releases_spelled_alike_resolve_to_the_one_the_files_album_names`

Old text:

```
        wanted = match.fold(album)
```

New text:

```
        wanted = album
```

### `r356-a.A5_withdrawn_track_is_a_candidate`

A track the provider will not play is compared like any other, with the version the client never read

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A5_withdrawn_track_is_a_candidate`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_track_the_provider_will_not_play_is_never_the_choice`
  - `tests/test_outbound_tidal_account.py::test_a_withdrawn_release_does_not_stop_the_one_that_plays_from_being_chosen`

Old text:

```
    return getattr(track, "available", True) is not False
```

New text:

```
    return True
```

### `r834.M3_a_refused_private_step_does_not_lose_the_playlist`

_make_private: raise the refusal instead of passing over it, so the create fails after the playlist exists and the ledger never records it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M3_a_refused_private_step_does_not_lose_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_created_playlist_the_client_offers_no_private_call_for_is_still_returned`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_twice_still_hands_back_the_one_playlist`

Old text:

```
        except CratekitError:
            return
```

New text:

```
        except CratekitError:
            raise
```

### `u226.M10_settle_lag_known_only`

_settled: a lagging window is read again only when something is known

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M10_settle_lag_known_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
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

### `r850-a.E3_listing_dropped`

export.summary: build each unmatched row but never list it, so the answer counts a track it does not name

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E3_listing_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_workers.py::test_a_resumed_export_counts_across_both_runs_and_each_item_once`
  - `tests/test_outbound_workers.py::test_an_export_the_provider_matches_nothing_of_says_so_in_the_envelope`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_the_envelope_names_the_tracks_the_provider_could_not_match`

Old text:

```
            left_out.append(listed)
```

New text:

```
            pass
```

### `u131.K11_filing_in_digest`

confirm_digest: leave the Exports filing out of the digest, so a changed folder does not make the answer stale

- File: `src/cratekit/export/cli.py`
- Source: `u131.json`, row `K11_filing_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 137 against a baseline of 137
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_changed_exports_folder_makes_the_old_answer_stale`

Old text:

```
    if filing:
        covered["filing"] = filing
```

New text:

```
    if False:
        covered["filing"] = filing
```

### `u51-item-derivation.D6_export_required`

Let a verb queue with no export document named

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `D6_export_required`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[export.playlist]`
  - `tests/test_outbound_workers.py::test_neither_verb_queues_anything_without_an_export[sync.favorites]`

Old text:

```
    if not text:
```

New text:

```
    if False:
```

### `r227.C4_export_limit_spelled`

export playlist judges against a seven spelled in the shell, not the configured limit

- File: `src/cratekit/export/cli.py`
- Source: `r227.json`, row `C4_export_limit_spelled`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_limit_is_the_configured_one_in_both_directions[export.playlist]`

Old text:

```
    age = source.export_age(exported, limit_days=cfg.outbound.export_stale_days)
```

New text:

```
    age = source.export_age(exported, limit_days=7)
```

### `u51-item-derivation.H3_frozen_config_ignored`

KTD9: the export handler loads a fresh configuration instead of using the frozen one

- File: `src/cratekit/export/cli.py`
- Source: `u51-item-derivation.json`, row `H3_frozen_config_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_handlers.py`
- Collected: 32 against a baseline of 32
- Kills: 1 (killed)
- Killed:
  - `tests/test_handlers.py::test_no_declared_handler_loads_a_fresh_configuration`

Old text:

```
    report = run_export_item(payload, str(item.item_id), cfg, account.resolve(cfg))
```

New text:

```
    report = run_export_item(
        payload, str(item.item_id), config.load(), account.resolve(cfg)
    )
```

### `u131.K1_mine_made_only`

filing.plan: read a Mine adopted by its name for marks too, so a playlist leaves a folder a person made

- File: `src/cratekit/organize/filing.py`
- Source: `u131.json`, row `K1_mine_made_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_hand_made_folder_named_mine_is_adopted_and_never_emptied`

Old text:

```
    if mine.made and mine.folder_id:
```

New text:

```
    if mine.folder_id:
```

### `u131.K3_product_made_left`

filing.plan: drop the product made leave, so a label's dated playlist is filed in Mine

- File: `src/cratekit/organize/filing.py`
- Source: `u131.json`, row `K3_product_made_left`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_matching_no_rule_is_listed_and_left`

Old text:

```
        if identity in made:
            rows.append(Placement(identity, name, LEFT, why=PRODUCT_MADE))
```

New text:

```
        if False:
            rows.append(Placement(identity, name, LEFT, why=PRODUCT_MADE))
```

### `u261.A3_account_records_no_session`

account.resolve: record no session under the adapter, so the adapter is opened afresh on every resolve and the one login per process is lost

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A3_account_records_no_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 143 against a baseline of 143
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

### `u174.O1_native_loop`

_mark_steps: plan no native pass, R-915 as it was

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O1_native_loop`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 164 against a baseline of 164
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step`
  - `tests/test_sync_mark.py::test_a_native_pass_whose_plan_refuses_is_a_refused_step_and_not_dropped`
  - `tests/test_sync_mark.py::test_organize_marks_a_native_pass_through_its_gate`
  - `tests/test_sync_mark.py::test_organize_plans_every_native_pass_not_only_the_latest`

Old text:

```
    for name in native_names:
```

New text:

```
    for name in ():
```

### `u202-composites.P1_reserve_held`

reserve_made_rekordbox: an account playlist a pair already holds is made a second rekordbox playlist

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u202-composites.json`, row `P1_reserve_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_back.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`
- Collected: 158 against a baseline of 158
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_pair_back.py::test_reserving_an_account_playlist_a_pair_holds_answers_that_pair_and_makes_nothing`

Old text:

```
            held = document.pairs.get(account_id)
            if held is not None:
                return held.rekordbox_id, False
            rekordbox_id = str(create())
```

New text:

```
            rekordbox_id = str(create())
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

### `u242.M7_inspiration_reads_the_title_alone`

INSPIRATION step: read a set in a sets folder by its prefix alone, so a stripped set is shown unprefixed and never backfilled

- File: `src/cratekit/organize/inspiration.py`
- Source: `u242.json`, row `M7_inspiration_reads_the_title_alone`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_organize_inspiration.py`
- Collected: 84 against a baseline of 84
- Kills: 1 (killed)
- Killed:
  - `tests/test_u242_taken.py::test_the_inspiration_set_rule_reads_a_stripped_set_as_the_prefixed_one`

Old text:

```
            stripped = untaken_name(name) if is_taken(playlist_id, name, held) else ""
```

New text:

```
            stripped = untaken_name(name) if name.startswith("DOWNLOADED ") else ""
```

### `r837-a.A7_reserve_reuses_recorded`

ledger.reserve_set_playlist: a recorded set playlist is not reused, so the create runs again

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r837-a.json`, row `A7_reserve_reuses_recorded`
- Moved: the reuse check left ledger.reserve_set_playlist for ledger_reserve._reserve, the one reserve shared by the set, label year and mirrored playlists, so the record is read through the table it is handed; same condition reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_export_set.py`, `tests/test_label_playlists.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 416 against a baseline of 416
- Kills: 5 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_added_to_the_tracklist_later_is_added_to_the_same_playlist`
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_new_year_made_by_hand_under_the_folder_is_reused_not_duplicated`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`

Old text:

```
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if recorded:
```

New text:

```
        recorded = str((held.get(key) or {}).get("remote_id") or "")
        if False:
```

### `u214.M8_plan_left_lines`

mirror.plan: start left empty, so no unmirrored node reaches the step's plan or left count

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u214.json`, row `M8_plan_left_lines`
- Moved: the unmirrored lines still open mirror.plan's left list in mirror.py, written without the list[str] annotation; same list emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 199 against a baseline of 199
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_rebuild_from_the_frozen_plan_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_no_batch_at_all_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_nothing_to_write_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_step_names_each_unmirrored_node_on_its_plan_and_its_line`

Old text:

```
    left = [f"{label}: not mirrored, {reason}" for label, reason in folder.unmirrored]
```

New text:

```
    left = []
```

### `u143-d.A5_playlist_read_back`

Adapter: report a root playlist removed though the provider still serves it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A5_playlist_read_back`
- Moved: the root removal's read back moved into tidal_account._sent_and_read_back, shared with remove_playlist, which reads the playlist through _served and answers None for absent; same still served check reverted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 446 against a baseline of 446
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_heard.py::test_a_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_label_heard.py::test_the_adapter_removes_a_vouched_playlist_and_reads_it_back_gone`
  - `tests/test_organize_root.py::test_a_root_playlist_still_served_after_its_delete_is_refused_not_reported_removed`
  - `tests/test_organize_root.py::test_the_adapter_removes_a_root_playlist_of_its_kind_and_reads_it_back_gone[served0-debris]`
  - `tests/test_organize_root.py::test_the_adapter_removes_a_root_playlist_of_its_kind_and_reads_it_back_gone[served1-empty]`

Old text:

```
        if self._served(doing, identifier) is not None:
```

New text:

```
        if False:
```

### `u230.M13_held_by_dropped`

decide: hand the genre rule no per playlist holders, so the lift never reaches the landed check

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M13_held_by_dropped`
- Moved: decide now builds its decisions in one list, so the _decide_genre call in mirror_edits.py sits four spaces shallower; same holders argument dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 28 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_at_one_moment_keep_rekordboxs`
  - `tests/test_mirror_edits.py::test_two_moves_follow_the_account_when_its_is_the_later`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00+00:00-]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`
  - `tests/test_mirror_edits_u227.py::test_a_move_made_in_rekordbox_after_the_landing_stands`
  - `tests/test_mirror_edits_u227.py::test_a_second_band_added_in_rekordbox_after_the_landing_stands`
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_later_account_move_then_a_rekordbox_move_back_into_the_landings_band_stands`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_mirror_edits_u230.py::test_another_playlists_snapshot_holding_the_track_is_never_read_as_landed`
  - ... and 13 more, see the JSON sidecar

Old text:

```
            held_by={track: frozenset(titles) for track, titles in held_by.items()},
```

New text:

```
            held_by=None,
```

### `u230.M12_queue_not_handed`

decide: hand the genre rule no queue

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M12_queue_not_handed`
- Moved: decide now builds its decisions in one list, so the _decide_genre call in mirror_edits.py sits four spaces shallower; same queue emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_folder_edit_on_a_never_agreed_derived_playlist_is_carried_too`
  - `tests/test_mirror_edits_u230.py::test_a_never_agreed_playlist_whose_account_side_holds_the_track_carries_it`
  - `tests/test_mirror_edits_u230.py::test_another_playlist_the_account_still_lists_it_on_counts_too`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_move_in_rekordbox_after_the_carry_still_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_a_never_agreed_playlist_holding_the_track_files_it_where_the_account_put_it`

Old text:

```
            queued=by_queue,
```

New text:

```
            queued={},
```

### `u227.R6_landed_item`

Decision.item: drop the landed flag from what the gate shows

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R6_landed_item`
- Moved: Decision.item now shows its optional keys from one table of pairs kept when true, so the landed flag is its own entry there rather than an if; same flag left off what the gate shows
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`

Old text:

```
            ("landed", self.landed),

```

New text:

```
(empty)
```

### `u201.M1_plan_keeps`

mirror.plan: removes an account track the hold keeps

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u201.json`, row `M1_plan_keeps`
- Moved: the reused playlist's plan left the body of mirror.plan for the helper mirror._reused, so the same line sits eight spaces shallower; same hold.keep test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`
  - `tests/test_organize_mirror_edits.py::test_a_track_the_library_lacks_added_on_the_account_is_held_there`
  - `tests/test_organize_mirror_edits.py::test_a_track_whose_file_is_gone_is_named_and_nothing_of_it_is_written`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
    remove = tuple(one for one in names if one not in keep and one not in hold.keep)
```

New text:

```
    remove = tuple(one for one in names if one not in keep)
```

### `u201.M2_plan_skips`

mirror.plan: adds back a track the hold skips

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u201.json`, row `M2_plan_skips`
- Moved: the reused playlist's plan left the body of mirror.plan for the helper mirror._reused, where the comprehension is folded onto one line; same hold.skip test dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 5 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_short_listing_changes_nothing_in_the_library_and_undoes_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_on_the_account_is_retagged_refiled_and_the_next_run_plans_nothing`
  - `tests/test_organize_mirror_edits.py::test_a_track_moved_to_its_own_genres_with_vox_is_held_and_nothing_is_written`
  - `tests/test_organize_mirror_edits.py::test_a_track_removed_on_the_account_and_added_nowhere_is_unfiled_and_listed`
  - `tests/test_organize_mirror_edits.py::test_two_moves_follow_the_later_account_move`

Old text:

```
            one for one in wanted if one not in on and one not in mine.refused and one not in hold.skip
```

New text:

```
            one for one in wanted if one not in on and one not in mine.refused
```

### `u255.M3_membership_holds_nothing`

_membership: never hold the opened object, so the first add opens again, K + 4 GETs

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M3_membership_holds_nothing`
- Moved: tidal_account._membership now lists its identifiers on one line through _identifier, so the line before the hold differs; same hold of the opened object removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
            self._opened[playlist_id] = opened

```

New text:

```
(empty)
```

### `r1032.A1_adapter_ignores_any_agreeing`

match_track: drop any_agreeing on its way to _among, so the adapter refuses the tie for the mirror too

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A1_adapter_ignores_any_agreeing`
- Moved: match_track moved from tidal_account.py into the Reads mixin in tidal_reads.py and its _among call is folded shallower; same any_agreeing dropped on its way to _among
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 13 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_none_of_the_tied_releases_still_takes_one`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_file_with_no_album_tag_never_narrows_to_releases_with_no_album_name`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_take_the_lower_hearted_one_never_an_unhearted_one`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
                    any_agreeing=any_agreeing,
```

New text:

```
                    any_agreeing=False,
```

### `r358-round-2.A3_editor_check`

Drop the editor check, so a playlist the account cannot edit is renamed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358-round-2.json`, row `A3_editor_check`
- Moved: the editor check in rename_playlist stays in tidal_account.py with its refusal folded onto fewer lines and one message string; same check removed
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_playlist_the_account_cannot_edit_refuses_rather_than_reporting_a_rename`

Old text:

```
        if not callable(retitle):
            raise account.provider_failure(LookupError(
                f"the provider's playlist {playlist_id!r} cannot be retitled by this account"
            ), doing)

```

New text:

```
(empty)
```

### `u226.M11_settle_kept_ignored`

_settled: a caller's kept wording is ignored for the order's

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u226.json`, row `M11_settle_kept_ignored`
- Moved: _settled's if kept is None fallback became the parameter's default, no track was moved, since no caller ever passed pauses_from; ignoring the caller's wording is now a reassignment to that default at the top of _settled, the same effect the reverted condition had
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_window_lag.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/modules/test_outbound.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`
- Collected: 442 against a baseline of 442
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_window_lag.py::test_a_removal_whose_first_reading_lags_beside_a_first_page_sends_nothing`

Old text:

```
        note = self._noting(identifier, after)
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

New text:

```
        kept = "no track was moved"
        note = self._noting(identifier, after)
        last: CratekitError | None = None
        for attempt in range(ORDER_REREADS + 1):
```

### `r836-a.A5_removal_never_retried`

tidal_account.remove_tracks: a removal by position is retried once, so a request that landed and timed out takes off whatever moved up

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A5_removal_never_retried`
- Moved: remove_tracks' removal by position stays in tidal_account.py, now one line with a lambda that binds nothing, since it is called before the loop moves on; same retries=0 dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_prune.py`, `tests/test_label_playlists.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`, `tests/test_export_collection.py`
- Collected: 501 against a baseline of 501
- Kills: 1 (killed)
- Killed:
  - `tests/test_prune.py::test_a_removal_the_provider_refuses_once_is_never_sent_again`

Old text:

```
            accepted = self._call(doing, lambda: playlist.remove_by_indices(at), retries=0)
```

New text:

```
            accepted = self._call(doing, lambda: playlist.remove_by_indices(at))
```

### `u216.M21_reserve_adopt_empty`

reserve_folder: an adoption records an empty set whatever the plan listed

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M21_reserve_adopt_empty`
- Moved: PairStore.reserve_folder's adoption in pairs.py writes the same expression on one line without the parentheses; same record of what it held emptied
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 9 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Genre Trivia! Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[DOWNLOADED Techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_made_after_the_sync_beside_its_pair_is_named_a_copy[downloaded techno]`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_of_a_playlist_no_pair_holds_comes_in`
  - `tests/test_sync_pair_adopted.py::test_a_downloaded_copy_the_adopted_folder_held_is_named_and_never_made`
  - `tests/test_sync_pair_adopted.py::test_a_playlist_and_its_downloaded_copy_made_in_one_sync_bring_in_the_one`
  - `tests/test_sync_pair_adopted.py::test_an_adoption_whose_plan_did_not_say_what_it_held_is_recorded_as_unknown`
  - `tests/test_sync_pair_adopted.py::test_reserving_an_adopted_folder_records_what_it_held_and_a_created_one_nothing`
  - `tests/test_sync_pair_adopted.py::test_the_adoption_records_what_the_folder_held`

Old text:

```
                before = None if held is None else frozenset(str(one) for one in held if str(one))
```

New text:

```
                before = frozenset()
```

