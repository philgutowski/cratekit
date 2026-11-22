# Mutation table: u309-replay-after-f

Measured by `scripts/mutate.py` on 2026-11-22 23:14 UTC, branch `HEAD` at `feafce67`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22910 collected. pytest invocations for this batch: 162.

Full baseline: measured by this driver (the battery's verdict was not read: it was read against another known failures file).

Subset baselines: 56, each measured by this driver.

Known failures: 251 node ids whose failure is this machine's and not the tree's, read from `../rows/known-failures-f.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22910 against 22910. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r229.L13_a_mismatch_is_never_said` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 2 | killed |
| `r229.L14_a_recorded_crate_is_a_claimant` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 1 | killed |
| `r229.L16_a_moved_record_is_not_followed` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 3 file(s) | 300 | 3 | killed |
| `r356-b.B7_heart_back_hands_on_no_title` | `src/cratekit/modules/outbound/hearts.py` | user | 1 file(s) | 64 | 1 | killed |
| `r1411.E4_membership_always_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 2 | killed |
| `r1411.S1_settled_ignores_agreed` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 2 | killed |
| `r1411.S2_agreed_stands_in_for_membership` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1305 | 1 | killed |
| `u246.S16_inspiration_held_per_element` | `src/cratekit/organize/inspiration.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `u142.S3_adopt_by_year_too` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 228 | 1 | killed |
| `r879-b.S8_several_needs_three` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 2 | killed |
| `r837-b.B3_accepted_in_review` | `src/cratekit/export/set_match.py` | user | 1 file(s) | 60 | 2 | killed |
| `r837-b.A3r_held_not_added` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 1 | killed |
| `r837-a.A11_year_folder_adopted` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 60 | 2 | killed |
| `r1017.M12_twin_message_names_to` | `src/cratekit/export/set_rename.py` | user | 4 file(s) | 195 | 1 | killed |
| `u140.B8_flag_conflict_dropped` | `src/cratekit/export/set_rename.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.A5_ledger_never_rekeyed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 9 | killed |
| `u214.M9_inbox_unmirrored` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 199 | 2 | killed |
| `u206.M14_account_keeps_invalid_isrc` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 9 file(s) | 1137 | 2 | killed |
| `u137.A2_sets_gate` | `src/cratekit/organize/account.py` | user | 2 file(s) | 117 | 10 | killed |
| `u123.L1_dated_vouched` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 108 | 20 | killed |
| `u143-d.A7_folder_empty` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 446 | 1 | killed |
| `r835-a.F4_recorded_and_refused_not_asked_again` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 5 | killed |
| `u243.L10_empties_never_said` | `src/cratekit/modules/outbound/prune.py` | user | 2 file(s) | 78 | 1 | killed |
| `u230.M19_every_title` | `src/cratekit/organize/account_mirror.py` | user | 11 file(s) | 209 | 1 | killed |
| `u230.M8_rekordbox_dropped` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 209 | 1 | killed |
| `u230.M18_titles_not_recorded` | `src/cratekit/organize/account_mirror.py` | user | 11 file(s) | 209 | 3 | killed |
| `u227.R9_before_queue` | `src/cratekit/organize/mirror_downloads.py` | user | 7 file(s) | 184 | 1 | killed |
| `u236.M5_mine_not_left` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 223 | 3 | killed |
| `u236.M23_frozen_reads_malformed` | `src/cratekit/organize/mirror_frozen.py` | user | 8 file(s) | 223 | 1 | killed |
| `u236.M15_settle_month_title` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 223 | 8 | killed |
| `u201.O1_latch` | `src/cratekit/organize/mirror_edits.py` | user | 5 file(s) | 185 | 1 | killed |
| `u201.S1_short_undeclared` | `src/cratekit/modules/outbound/service.py` | user | 5 file(s) | 185 | 1 | killed |
| `u201.E7_addition_beats_removal` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 185 | 1 | killed |
| `u204.A1_adopt_landed` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 222 | 1 | killed |
| `u204.P3_off_and_into_month_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u204.P4_two_months_held` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 222 | 1 | killed |
| `u143-b.F4_legacy_record_stale` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 164 | 1 | killed |
| `u142.S20_retitled_detail_called_marked` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.R7_every_batch_suggested` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 1 | killed |
| `u112.A7_no_proof_read` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 8 | killed |
| `u137.C2_only_dropped` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 95 | 23 | killed |
| `u137.R3_refused_rotation_shown` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 1 | killed |
| `u142.S15_second_proof_ignored` | `src/cratekit/organize/account.py` | user | 1 file(s) | 95 | 6 | killed |
| `u116.M6_no_adopt` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 95 | 2 | killed |
| `u185.R2_organize_fact` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 95 | 2 | killed |
| `r1295.M15_plan_passes_no_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 4 | killed |
| `u144-b.B1_unnamed_membership` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 1 | killed |
| `r1295.M13_unread_miss_no_id` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 4 | killed |
| `u144-a.A7_only_matched` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 8 | killed |
| `r1295.M14_unread_miss_blank_title` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 3 | killed |
| `u144-a.A8_empty_not_written` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 38 | 2 | killed |
| `u147-b.M9_link_reused_blind` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u147-b.M11_agree_dropped` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 34 | 1 | killed |
| `u267.M13_downloads_owned_opens_its_own` | `src/cratekit/organize/mirror_downloads.py` | user | 2 file(s) | 51 | 1 | killed |
| `r1031.M13_miss_written_over_a_link` | `src/cratekit/modules/outbound/ledger_settle.py` | maintainer | 2 file(s) | 71 | 1 | killed |
| `r1031.M2_rematch_ignored` | `src/cratekit/modules/outbound/mirror.py` | user | 2 file(s) | 71 | 2 | killed |
| `u222.M10_shown_flag_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 251 | 1 | killed |
| `u222.M22_cli_detail_unchanged` | `src/cratekit/organize/cli.py` | user | 6 file(s) | 251 | 1 | killed |
| `u222.M12_unshown_not_said` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 251 | 1 | killed |
| `u222.M6_load_drops_agreed` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 251 | 6 | killed |
| `u150.M4_retire_in_digest` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 1 | killed |
| `u150.M11_unmade_folder` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 103 | 2 | killed |
| `u150.Z2_frozen_flag_checked` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 2 file(s) | 69 | 1 | killed |
| `u267.M3_report_never_closes` | `src/cratekit/organize/cli.py` | user | 2 file(s) | 109 | 4 | killed |
| `u143-a.R1_missing_tracks` | `src/cratekit/organize/root.py` | user | 1 file(s) | 55 | 1 | killed |
| `u255.C8_no_open_before_and_retry_opens_raw` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 3 | killed |
| `u255.M10_failed_attempt_keeps_the_hold` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 5 | killed |
| `u255.M11_retry_opens_raw` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 338 | 2 | killed |
| `u270.E1_already_on_the_playlist` | `src/cratekit/modules/outbound/export.py` | user | 4 file(s) | 257 | 6 | killed |
| `u270.C3_refused_track_fails_its_item` | `src/cratekit/export/cli.py` | user | 2 file(s) | 145 | 1 | killed |
| `u220.A13_exact_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 1 | killed |
| `u220.A17_settle_once` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 283 | 4 | killed |
| `r1308.M11_count_before_ge` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 1 | killed |
| `r1308.M15_lag_always` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 388 | 12 | killed |
| `r1032.A3_unreadable_tie_broken` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 2 file(s) | 118 | 3 | killed |
| `r356-b.B1_naming_head_left_on_the_release_title` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 8 | killed |
| `r572.H1_hearts_drop_album` | `src/cratekit/modules/outbound/hearts.py` | user | 1 file(s) | 113 | 1 | killed |
| `r358.A2_title_stripped_for_the_write` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 113 | 1 | killed |
| `r572.A2_first_named` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r356-a.A3_any_hearted_rather_than_the_only_hearted` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 4 | killed |
| `r850-a.E5_slug_is_no_reason` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 2 | killed |
| `r850-a.E4_reason_gate` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 1 | killed |
| `u51-item-derivation.A2_default_favorites_playlist` | `src/cratekit/modules/outbound/source.py` | user | 2 file(s) | 143 | 27 | killed |
| `r856-a.S2_tally_bool` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 178 | 3 | killed |
| `u51-item-derivation.S3_empty_job_driven` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 1 | killed |
| `u131.K9_export_refusal_kept` | `src/cratekit/modules/outbound/export.py` | user | 3 file(s) | 234 | 1 | killed |
| `u131.K2_exports_rule` | `src/cratekit/organize/filing.py` | user | 2 file(s) | 109 | 2 | killed |
| `r1305.A2_account_status_declared_only` | `src/cratekit/modules/outbound/account.py` | user | 3 file(s) | 197 | 6 | killed |
| `r836-a.A1_product_made_asked_first` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 112 | 3 | killed |
| `r836-c.L6_date_on_the_confirmed_record` | `src/cratekit/modules/outbound/ledger_reserve.py` | user | 5 file(s) | 404 | 2 | killed |
| `r836-e.P5_apply_asks_the_ledger_again` | `src/cratekit/modules/outbound/prune.py` | user | 5 file(s) | 404 | 1 | killed |
| `u227.R4_folder_compare` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 1 file(s) | 22910 | 0 (promoted) | zero |
| `u174.O3_no_pass_counted` | `src/cratekit/organize/account.py` | user | 2 file(s) | 164 | 1 | killed |
| `u130-c.C6_pair_not_vouched` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 67 | 5 | killed |
| `u221.R14_hold_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 3 file(s) | 153 | 4 | killed |
| `u129-author.A17_empty_add_still_writes` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 24 | 3 | killed |
| `r835-b.T1_folder_create_never_retried` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 56 | 1 | killed |
| `u236.M18_ledger_placement_not_written` | `src/cratekit/modules/outbound/ledger_settle.py` | user | 2 file(s) | 25 | 8 | killed |
| `u147-d.A5_source_title` | `src/cratekit/organize/account_mirror.py` | user | 1 file(s) | 3 | 1 | killed |
| `r1031.M4_signature_dropped` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 37 | 1 | killed |
| `r1032.S1_protocol_default_on` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 15 | killed |
| `r879-b.T1_one_track_never_asked_to_agree` | `src/cratekit/modules/outbound/tidal_reads.py` | user | 1 file(s) | 113 | 1 | killed |
| `r227.S6_no_stale_sentence` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 123 | 8 | killed |

## Zero rows and what they owe

- `u227.R4_folder_compare` (user facing): USER FACING ZERO WITH NO COMPOSITE: pair it or reclassify it

## Row definitions

### `r229.L13_a_mismatch_is_never_said`

A record under the crate's own path written from other music is reported as an ordinary update

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L13_a_mismatch_is_never_said`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L14_a_recorded_crate_is_a_claimant`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r229.json`, row `L16_a_moved_record_is_not_followed`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_workers.py`
- Collected: 300 against a baseline of 300
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

### `r356-b.B7_heart_back_hands_on_no_title`

The hearts engine hands the account no title

- File: `src/cratekit/modules/outbound/hearts.py`
- Source: `r356-b.json`, row `B7_heart_back_hands_on_no_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/modules/test_outbound.py`
- Collected: 64 against a baseline of 64
- Kills: 1 (killed)
- Killed:
  - `tests/modules/test_outbound.py::test_a_heart_back_hands_the_account_the_names_and_reports_its_reasons`

Old text:

```
            title=item.release_title,
```

New text:

```
            title="",
```

### `r1411.E4_membership_always_agrees`

existing guard, U220: a reading after this command's own writes is taken whatever it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `E4_membership_always_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`
  - `tests/test_outbound_remove_lag.py::test_a_pairs_removal_add_and_order_all_land_over_a_read_that_lags_each_write[whole]`

Old text:

```
            return sorted(reading) == sorted(known)
```

New text:

```
            return bool(reading) or True
```

### `r1411.S1_settled_ignores_agreed`

the judged reading never asks the agreed order, so only what it holds is checked

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S1_settled_ignores_agreed`
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
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if False:
                return False
```

### `r1411.S2_agreed_stands_in_for_membership`

a reading in the agreed order is taken without the check of what it holds

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1411.json`, row `S2_agreed_stands_in_for_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1305 against a baseline of 1305
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_the_agreed_order_does_not_stand_in_for_what_the_write_left`

Old text:

```
            if agreed is not None and not _in_agreed_order(reading, agreed):
                return False
```

New text:

```
            if agreed is not None:
                return _in_agreed_order(reading, agreed)
```

### `u246.S16_inspiration_held_per_element`

assert_read_back (inspiration): build the live set once per planned row again (the shape on main)

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S16_inspiration_held_per_element`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_comprehension_sets.py`, `tests/test_organize_inspiration.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_comprehension_sets.py::test_no_comprehension_in_the_package_rebuilds_an_invariant_set_per_element`

Old text:

```
        missing = [row for row in one.members if row not in held]
```

New text:

```
        missing = [row for row in one.members if row not in set(live)]
```

### `u142.S3_adopt_by_year_too`

plan_archive: adopt a root folder named as the plain year as well, so the year folder competes with the sets' folder

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S3_adopt_by_year_too`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 228 against a baseline of 228
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`

Old text:

```
        named = sorted(fid for fid, title in root.items() if title == name)
```

New text:

```
        named = sorted(fid for fid, title in root.items() if title in (name, year))
```

### `r879-b.S8_several_needs_three`

_not_chosen: say several only from three distinct exact matches

- File: `src/cratekit/export/set_match.py`
- Source: `r879-b.json`, row `S8_several_needs_three`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_second_distinct_exact_match_on_the_next_page_leaves_it_out_as_several`
  - `tests/test_export_set.py::test_two_exact_candidates_are_not_chosen_between`

Old text:

```
    elif exact > 1:
```

New text:

```
    elif exact > 2:
```

### `r837-b.B3_accepted_in_review`

set_cli.match_rows: a candidate accepted in review is not used, so the row is left out

- File: `src/cratekit/export/set_match.py`
- Source: `r837-b.json`, row `B3_accepted_in_review`
- Moved: the same text, now in src/cratekit/export/set_match.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_candidate_accepted_in_review_is_used_and_not_searched_for_again`
  - `tests/test_export_set.py::test_a_persons_answer_in_review_wins_over_the_librarys_file`

Old text:

```
                if answered.state == candidates.ACCEPTED and answered.track is not None:
```

New text:

```
                if False:
```

### `r837-b.A3r_held_not_added`

batch a's A3 again: sets.plan_set adds a track already on the playlist and never recorded

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-b.json`, row `A3r_held_not_added`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_already_on_the_playlist_and_never_recorded_is_not_asked_for`

Old text:

```
        add=tuple(one for one in wanted if one not in asked and one not in held),
```

New text:

```
        add=tuple(one for one in wanted if one not in asked),
```

### `r837-a.A11_year_folder_adopted`

sets.plan_archive: a root folder already named as the year is never adopted, so a second is made

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A11_year_folder_adopted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 60 against a baseline of 60
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_folder_named_as_the_year_by_hand_is_adopted_not_doubled`
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`

Old text:

```
        action, folder_id = (ADOPT, named[0]) if named else (CREATE, "")
```

New text:

```
        action, folder_id = (CREATE, "")
```

### `r1017.M12_twin_message_names_to`

Refusal: name the held playlist under the new name rather than the name it is recorded under

- File: `src/cratekit/export/set_rename.py`
- Source: `r1017.json`, row `M12_twin_message_names_to`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_the_frozen_name_ranks_ahead_of_the_landing_record`

Old text:

```
            f"{planned.playlist.remote_id} under {planned.playlist.name!r} and "
```

New text:

```
            f"{planned.playlist.remote_id} under {to!r} and "
```

### `u140.B8_flag_conflict_dropped`

export set --rename accepts a tracklist or --name beside it

- File: `src/cratekit/export/set_rename.py`
- Source: `u140.json`, row `B8_flag_conflict_dropped`
- Moved: the same text, now in src/cratekit/export/set_rename.py, was in src/cratekit/export/set_cli.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_rename_with_a_tracklist_or_name_is_refused_before_anything`

Old text:

```
    if ctx.args.tracklist is not None or ctx.args.name is not None:

```

New text:

```
    if False:

```

### `u140.A5_ledger_never_rekeyed`

apply_rename retitles on the account and leaves the ledger key where it was

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A5_ledger_never_rekeyed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 9 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_backfill_after_the_rename_plans_no_twin_and_a_named_export_adds_to_it`
  - `tests/test_export_set_rename.py::test_a_job_whose_page_words_differ_renames_by_the_name_its_landing_recorded`
  - `tests/test_export_set_rename.py::test_a_job_with_no_frozen_name_is_found_by_the_queued_day_and_refrozen`
  - `tests/test_export_set_rename.py::test_a_ledger_left_under_the_old_key_is_moved_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`
  - `tests/test_export_set_rename.py::test_a_rename_that_failed_after_the_account_finishes_on_the_next_run`
  - `tests/test_export_set_rename.py::test_a_renamed_inspiration_playlist_renames_the_account_playlist_ledger_and_job`
  - `tests/test_export_set_rename.py::test_a_second_rename_is_a_no_op`
  - `tests/test_export_set_rename.py::test_the_backfill_plans_no_twin_after_a_rename_by_the_landing_record`

Old text:

```
        done.rekeyed = ledger.rename_set_playlist(
            cfg, playlist.name, planned.to, playlist.remote_id
        )

```

New text:

```
        done.rekeyed = False

```

### `u214.M9_inbox_unmirrored`

_inbox: hand the folder no unmirrored node

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u214.json`, row `M9_inbox_unmirrored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 199 against a baseline of 199
- Kills: 2 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_playlist_whose_record_cannot_be_read_is_never_said_to_have_none`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_folder_mirrors_the_batch_and_names_the_other_nodes`

Old text:

```
        unmirrored=tuple((node.label(), node.reason) for node in live.left),
```

New text:

```
        unmirrored=(),
```

### `u206.M14_account_keeps_invalid_isrc`

TidalAccount._isrc_tracks: keep any no match as a not found, InvalidISRC included

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `u206.json`, row `M14_account_keeps_invalid_isrc`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_cache.py`, `tests/test_sync_pair.py`, `tests/test_intake_missing_isrc.py`, `tests/test_outbound_tidal_account.py`, `tests/test_label_tidal_catalogue.py`, `tests/test_organize_mirror_tie.py`, `tests/test_intake_land_rehearse.py`, `tests/test_doctor.py`, `tests/test_config.py`
- Collected: 1137 against a baseline of 1137
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_an_invalid_isrc_the_account_reads_as_no_match_is_never_kept`
  - `tests/test_isrc_cache.py::test_an_outage_then_an_invalid_isrc_on_the_retry_keeps_nothing`

Old text:

```
            if last["said_not_found"]:
                self._cache.remember(wanted, country, ())
```

New text:

```
            if True:
                self._cache.remember(wanted, country, ())
```

### `u137.A2_sets_gate`

Plan the set archives whatever the selection

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A2_sets_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 117 against a baseline of 117
- Kills: 10 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`

Old text:

```
    if area.wants(SETS):
```

New text:

```
    if True:
```

### `u123.L1_dated_vouched`

Stop the ledger vouching for a dated playlist it records

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u123.json`, row `L1_dated_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_dated.py`, `tests/test_prune.py`
- Collected: 108 against a baseline of 108
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

### `u143-d.A7_folder_empty`

Adapter: remove a legacy folder that still holds playlists

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A7_folder_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 446 against a baseline of 446
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026 Custom Playlists-2-not-empty]`

Old text:

```
        held = len(self.folder_playlists(identifier)) + len(self.folder_folders(identifier))
```

New text:

```
        held = 0
```

### `r835-a.F4_recorded_and_refused_not_asked_again`

folders.plan: a track recorded as added or refused is asked for again, so one a person took off is put back and one refused is asked every run

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F4_recorded_and_refused_not_asked_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 5 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_refusal_part_way_leaves_what_was_written_recorded_and_a_resume_finishes`
  - `tests/test_label_playlists.py::test_a_second_mark_plans_nothing_and_a_build_after_it_reuses_the_marked_years`
  - `tests/test_label_playlists.py::test_a_second_run_over_an_unchanged_catalogue_plans_nothing`
  - `tests/test_label_playlists.py::test_a_track_taken_off_by_a_person_is_not_put_back`
  - `tests/test_label_playlists.py::test_a_track_the_provider_will_not_add_is_recorded_and_not_asked_again`

Old text:

```
            skip = held | asked
```

New text:

```
            skip = held
```

### `u243.L10_empties_never_said`

prune._step: a playlist the plan empties is never marked, so the screen does not say so

- File: `src/cratekit/modules/outbound/prune.py`
- Source: `u243.json`, row `L10_empties_never_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_tombstoned.py`, `tests/test_prune.py`
- Collected: 78 against a baseline of 78
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_tombstoned.py::test_a_year_playlist_the_prune_empties_is_named_and_kept`

Old text:

```
        empties=bool(take) and set(order) <= {one.remote_id for one in take},
```

New text:

```
        empties=False,
```

### `u230.M19_every_title`

_read_edits: name every recorded playlist as the one that queued each track

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u230.json`, row `M19_every_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u230.py::test_a_job_queued_from_another_playlist_does_not_lift_the_edited_ones_base`

Old text:

```
        remote: frozenset(titled[one] for one in sources if one in titled)
```

New text:

```
        remote: frozenset(titled.values())
```

### `u230.M8_rekordbox_dropped`

_as_queued: lift though rekordbox already holds it where the account put it

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M8_rekordbox_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 209 against a baseline of 209
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_a_landing_filed_where_the_account_asked_is_no_edit`

Old text:

```
        and track not in one.rekordbox

```

New text:

```
        and True

```

### `u230.M18_titles_not_recorded`

_read_edits: record no titles for the queue's remote playlists

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u230.json`, row `M18_titles_not_recorded`
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
                titled[mine.remote_id] = source.name
```

New text:

```
                pass
```

### `u227.R9_before_queue`

filed: an entry applied before the track was queued is read as the landing's

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u227.json`, row `R9_before_queue`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 184 against a baseline of 184
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u227.py::test_a_filing_recorded_before_the_download_was_queued_is_not_the_landings`

Old text:

```
            and at >= after
```

New text:

```
            and True
```

### `u236.M5_mine_not_left`

decide favorites: a favourite put in another month keeps the placed month

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M5_mine_not_left`
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
            mine = ours - now_m
```

New text:

```
            mine = frozenset()
```

### `u236.M23_frozen_reads_malformed`

load: accept placements that are not tracks to times

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u236.json`, row `M23_frozen_reads_malformed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
            if not isinstance(tracks, dict) or not all(
                isinstance(track, str) and isinstance(at, str) for track, at in tracks.items()
            ):
```

New text:

```
            if False:
```

### `u236.M15_settle_month_title`

settle: record the placement under the month's bare name, not its account title

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M15_settle_month_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 223 against a baseline of 223
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_a_hand_addition_after_the_placement_is_dropped_is_read_as_one`
  - `tests/test_organize_mirror_edits_u236.py::test_a_month_whose_listing_fails_at_the_unfavourite_still_reads_its_placement`
  - `tests/test_organize_mirror_edits_u236.py::test_a_placement_the_account_refused_to_take_still_lets_the_unfavourite_through`
  - `tests/test_organize_mirror_edits_u236.py::test_the_organize_after_the_favourite_puts_it_in_the_accounts_month`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`
  - `tests/test_organize_mirror_edits_u236.py::test_the_same_when_the_write_made_the_month`

Old text:

```
                mirror.title(decision.to.folder, month_of[decision.content_id][0]),
```

New text:

```
                month_of[decision.content_id][0],
```

### `u201.O1_latch`

write: the tree's convergence latch is not asked

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u201.json`, row `O1_latch`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_tree_the_product_latched_refuses_the_write_before_any_file_is_tagged`

Old text:

```
        convergence.assert_tree_writable(cfg, db, tree_id, registry)
```

New text:

```
        pass
```

### `u201.S1_short_undeclared`

PlaylistListing.short: a listing that declares no count is whole

- File: `src/cratekit/modules/outbound/service.py`
- Source: `u201.json`, row `S1_short_undeclared`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits.py::test_a_listing_with_no_declared_count_is_short`

Old text:

```
        return self.declared is None or self.listed < self.declared
```

New text:

```
        return self.declared is not None and self.listed < self.declared
```

### `u201.E7_addition_beats_removal`

decide: an unfile on the account against rekordbox placing the track is carried, the removal beating the addition

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E7_addition_beats_removal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 185 against a baseline of 185
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_unfile_on_the_account_against_a_move_in_rekordbox_keeps_rekordboxs`

Old text:

```
            if kind == UNFILE:
```

New text:

```
            if False:
```

### `u204.A1_adopt_landed`

_read_edits: a landed row tied by its ISRC is not answered as the track the account holds

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u204.json`, row `A1_adopt_landed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_landed_track_the_provider_ties_to_another_release_is_still_filed`

Old text:

```
            matcher.adopt(content_id, remote)
```

New text:

```
            pass
```

### `u204.P3_off_and_into_month_held`

_decide_favorites: a track taken off All Favorites and put in a month at once is unfavourited rather than held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P3_off_and_into_month_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_favorites_edit_the_account_does_not_decide_is_held[af2-oct_2-nov2-at once]`

Old text:

```
        if removed_s and added_m:
```

New text:

```
        if False:
```

### `u204.P4_two_months_held`

_decide_favorites: a track added to two months at once is favourited into one of them rather than held

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P4_two_months_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 222 against a baseline of 222
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_favorites_edit_the_account_does_not_decide_is_held[af1-oct_1-nov1-2 month playlists]`

Old text:

```
        elif len(added_m) > 1:
```

New text:

```
        elif False:
```

### `u143-b.F4_legacy_record_stale`

Year folder: reuse a recorded folder now named as a legacy year folder

- File: `src/cratekit/organize/filing.py`
- Source: `u143-b.json`, row `F4_legacy_record_stale`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`, `tests/test_organize_root.py`, `tests/test_playlist_kinds.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_year_record_whose_folder_now_carries_a_legacy_name_is_not_reused`

Old text:

```
        and not kinds.legacy_year(root[recorded])
    ):
```

New text:

```
    ):
```

### `u142.S20_retitled_detail_called_marked`

organize set step: call a set a person retitled in its folder marked

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S20_retitled_detail_called_marked`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`

Old text:

```
        elif planned is not None and planned.left == sets.RETITLED:
```

New text:

```
        elif False:
```

### `u112.R7_every_batch_suggested`

Every batch is suggested a rename, a readably named one included

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R7_every_batch_suggested`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_what_the_author_made_is_listed_with_a_home_and_never_a_write`

Old text:

```
        if batch.recognised_by == rotate.BY_SUFFIX:
```

New text:

```
        if True:
```

### `u112.A7_no_proof_read`

No intake file is read as a set's proof, so no downloaded set is ever archived

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A7_no_proof_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize.py::test_a_downloaded_sets_folder_made_by_hand_is_adopted_and_the_filing_keeps_its_year`
  - `tests/test_organize.py::test_a_set_proven_by_its_intake_file_never_opens_the_database_for_inspiration`
  - `tests/test_organize.py::test_a_year_record_whose_folder_now_carries_the_sets_name_is_not_the_filings`
  - `tests/test_organize.py::test_aborting_rekordbox_and_applying_the_account_writes_only_the_account`
  - `tests/test_organize.py::test_an_unreadable_label_registry_refuses_the_label_step_alone`
  - `tests/test_organize.py::test_no_downloaded_sets_folder_is_made_once_and_the_year_folder_beside_it`
  - `tests/test_organize.py::test_one_step_of_each_kind_is_planned_in_its_own_area`
  - `tests/test_organize.py::test_one_steps_refusal_leaves_every_other_plan_on_screen`

Old text:

```
        xml = _proof(cfg, name)
```

New text:

```
        xml = None
```

### `u137.C2_only_dropped`

Read --only and then plan as if it were absent

- File: `src/cratekit/organize/cli.py`
- Source: `u137.json`, row `C2_only_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 23 (killed)
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
  - ... and 8 more, see the JSON sidecar

Old text:

```
    only = frozenset(chosen) if chosen else None
```

New text:

```
    only = None
```

### `u137.R3_refused_rotation_shown`

Hide a rotation that refused when it was planned only for yours

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u137.json`, row `R3_refused_rotation_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
        if area.wants(ROTATE) or rotation.cause is not None:
```

New text:

```
        if area.wants(ROTATE):
```

### `u142.S15_second_proof_ignored`

organize set step: list a set with an INSPIRATION playlist of its name as waiting, the behaviour before this unit

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S15_second_proof_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`
  - `tests/test_organize.py::test_a_set_archived_by_its_inspiration_proof_stays_archived_once_that_playlist_goes`
  - `tests/test_organize.py::test_a_set_found_prefixed_by_the_migration_is_still_filed_by_the_archive`
  - `tests/test_organize.py::test_a_set_in_its_folder_with_its_built_title_is_taken_and_not_moved`
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`
  - `tests/test_organize.py::test_the_inspiration_proof_is_read_while_rekordbox_runs`

Old text:

```
            if held is None or name not in held:
```

New text:

```
            if True:
```

### `u116.M6_no_adopt`

_year_folder: a root folder named as the year is ignored and a second made

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M6_no_adopt`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 95 against a baseline of 95
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_year_folder_already_on_the_account_is_adopted_with_no_set_to_make_it`
  - `tests/test_organize.py::test_an_existing_year_folder_on_the_account_is_adopted_not_made_again`

Old text:

```
    if named:
        return YearFolder(year=year, action=sets.ADOPT, folder_id=named[0], stale=recorded)
```

New text:

```
    if False:
        return YearFolder(year=year, action=sets.ADOPT, folder_id=named[0], stale=recorded)
```

### `u185.R2_organize_fact`

organize: name the folder nowhere, so the report is silent about it

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u185.json`, row `R2_organize_fact`
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
    if foreign:
        area.facts[FOREIGN_FACT]
```

New text:

```
    if foreign and False:
        area.facts[FOREIGN_FACT]
```

### `r1295.M15_plan_passes_no_unread`

plan: the readable sets are decided with no unread misses

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M15_plan_passes_no_unread`
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
                    tuple(_unread_miss(place, one) for place, one in listing.unread),
```

New text:

```
                    (),
```

### `u144-b.B1_unnamed_membership`

Write guard: drop the refusal of a membership the approved plan did not name

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-b.json`, row `B1_unnamed_membership`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        if unnamed:
```

New text:

```
        if False:
```

### `r1295.M13_unread_miss_no_id`

_unread_miss: the miss line names no track id

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M13_unread_miss_no_id`
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
f"{one.why} (track {one.ref}), so it was not asked of the library"
```

New text:

```
f"{one.why}, so it was not asked of the library"
```

### `u144-a.A7_only_matched`

Match: take a track with no row as a member, an empty id in the playlist

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A7_only_matched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 8 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_near_match_is_a_question_named_as_a_miss_and_never_written`
  - `tests/test_organize_inspiration.py::test_a_second_run_plans_nothing`
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`
  - `tests/test_organize_inspiration.py::test_eighteen_tracks_fifteen_in_the_library_plan_fifteen_and_name_three`
  - `tests/test_organize_inspiration.py::test_the_writer_refuses_a_membership_the_plan_did_not_name`

Old text:

```
        held, why = row_of(one)
        if held:
```

New text:

```
        held, why = row_of(one)
        if True:
```

### `r1295.M14_unread_miss_blank_title`

_unread_miss: an absent title shown blank rather than as no title

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M14_unread_miss_blank_title`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_miss_the_library_lacks_ahead_of_an_unread_track_keeps_set_order`
  - `tests/test_organize_inspiration.py::test_a_track_with_no_title_is_named_and_the_sets_other_tracks_are_written`
  - `tests/test_organize_inspiration.py::test_an_unread_track_keeps_the_sets_positions_for_every_other_miss`

Old text:

```
        one.title or "no title",
```

New text:

```
        one.title,
```

### `u144-a.A8_empty_not_written`

Decide: plan a set with no match as a create, an empty playlist

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-a.json`, row `A8_empty_not_written`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 38 against a baseline of 38
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_with_no_match_is_reported_and_no_empty_playlist_is_written`
  - `tests/test_organize_inspiration.py::test_a_step_whose_every_set_has_no_match_plans_nothing_and_writes_nothing`

Old text:

```
        action=CREATE if members else EMPTY,
```

New text:

```
        action=CREATE,
```

### `u147-b.M9_link_reused_blind`

Matcher: reuse a link even when the row's database code changed

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M9_link_reused_blind`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_row_whose_database_code_changed_is_matched_again`

Old text:

```
        if linked is not None and (not row.isrc or row.isrc == linked[1]):
```

New text:

```
        if linked is not None:
```

### `u147-b.M11_agree_dropped`

Matcher: never ask the one track to agree, a file's code included (R-879)

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M11_agree_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 34 against a baseline of 34
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_code_read_off_the_file_asks_the_one_track_to_agree_and_a_database_code_does_not`

Old text:

```
            agree=said.agree,
```

New text:

```
            agree=False,
```

### `u267.M13_downloads_owned_opens_its_own`

mirror_downloads.plan: hand no shared read to the ISRC read, which then opens its own handle in the report

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `u267.json`, row `M13_downloads_owned_opens_its_own`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_one_read.py`
- Collected: 51 against a baseline of 51
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_the_downloads_plan_reads_the_library_through_a_reports_one_handle`

Old text:

```
        owned = _owned(cfg, reading, one_read)
```

New text:

```
        owned = _owned(cfg, reading)
```

### `r1031.M13_miss_written_over_a_link`

ledger.record_mirror_misses: write a miss for a row the ledger already links

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `r1031.json`, row `M13_miss_written_over_a_link`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_settle.py, was in src/cratekit/modules/outbound/ledger.py
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_miss_over_a_linked_row_is_never_written_to_the_document`

Old text:

```
            if str(content_id) in document["mirror_links"]:
                continue
```

New text:

```
            if False:
                continue
```

### `r1031.M2_rematch_ignored`

Matcher: keep the remembered misses under rematch, so --rematch asks nothing

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M2_rematch_ignored`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 71 against a baseline of 71
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_row_matched_later_loses_its_miss`
  - `tests/test_organize_mirror_frozen.py::test_rematch_asks_every_remembered_miss_again`

Old text:

```
        self._misses = {} if rematch else dict(misses or {})
```

New text:

```
        self._misses = dict(misses or {})
```

### `u222.M10_shown_flag_check`

load: accept a shown flag that is not true or false

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M10_shown_flag_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
        if not isinstance(shown, bool):
```

New text:

```
        if False:
```

### `u222.M22_cli_detail_unchanged`

_ask: carry no stale lines in the refusal's detail

- File: `src/cratekit/organize/cli.py`
- Source: `u222.json`, row `M22_cli_detail_unchanged`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`

Old text:

```
                detail={**dict(cause.detail or {}), "stale": list(area.stale)},
```

New text:

```
                detail=cause.detail,
```

### `u222.M12_unshown_not_said`

_stale: read a record no gate showed as one it did

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M12_unshown_not_said`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_plan_made_afresh_by_a_decided_run_is_never_read_as_what_the_gate_showed`

Old text:

```
    if frozen is not None and not frozen.shown:
```

New text:

```
    if False:
```

### `u222.M6_load_drops_agreed`

load: read no frozen snapshot, so the overlay has nothing to take

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M6_load_drops_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 251 against a baseline of 251
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_genre_edit_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_join_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_inbox_leave_the_library_took_between_the_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`
  - `tests/test_organize_mirror_frozen_u222.py::test_the_frozen_snapshot_is_the_one_the_gates_plan_read_not_the_one_it_recorded`

Old text:

```
        agreed = _agreed_of(data["agreed"])
```

New text:

```
        agreed = {}
```

### `u150.M4_retire_in_digest`

FolderPlan.identity: leave the retirements out of the digest, so an approval given for one removal covers another

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M4_retire_in_digest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_the_digest_covers_the_removal`

Old text:

```
            "retire": [list(one) for one in self.retire],
```

New text:

```
            "retire": [],
```

### `u150.M11_unmade_folder`

mirror.plan: make the retiring folder even when nothing goes in it, so an empty INBOX root folder is created

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M11_unmade_folder`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 103 against a baseline of 103
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_deleted_inbox_folder_with_only_removals_left_is_not_made_again`
  - `tests/test_organize_mirror_inbox.py::test_an_inbox_with_no_live_batch_makes_no_empty_folder`

Old text:

```
    if folder_action == CREATE and folder.retire and not folder.playlists:
        folder_action = UNMADE
```

New text:

```
    if False:
        folder_action = UNMADE
```

### `u150.Z2_frozen_flag_checked`

mirror_frozen._flag: accept any value as a retire flag, so a damaged record retires on a string

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u150.json`, row `Z2_frozen_flag_checked`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 69 against a baseline of 69
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_frozen_folder_whose_retire_is_not_a_boolean_is_not_read[retire-yes]`

Old text:

```
    if not isinstance(value, bool):
```

New text:

```
    if False:
```

### `u267.M3_report_never_closes`

organize: the finally closes no shared read, so the report leaves its handle and engine open

- File: `src/cratekit/organize/cli.py`
- Source: `u267.json`, row `M3_report_never_closes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_one_read.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_one_read.py::test_a_failure_nobody_expected_still_closes_the_handle`
  - `tests/test_organize_one_read.py::test_a_step_that_refuses_after_the_open_leaves_no_handle_open`
  - `tests/test_organize_one_read.py::test_the_report_opens_the_database_once_and_closes_it_once`
  - `tests/test_organize_one_read.py::test_the_sets_step_reads_inspiration_through_the_one_handle`

Old text:

```
        if one_read is not None:
            one_read.close()
```

New text:

```
        if one_read is not None:
            pass
```

### `u143-a.R1_missing_tracks`

Debris: read no track as missing, so a copy holding a track the label folder lacks is planned for removal

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R1_missing_tracks`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 55 against a baseline of 55
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_with_a_track_the_label_folder_lacks_is_left_naming_it`

Old text:

```
        missing = [one for one in dict.fromkeys(tracks) if one not in held]
```

New text:

```
        missing = []
```

### `u255.C8_no_open_before_and_retry_opens_raw`

M8 with the attempt's open made raw through the session: the first open then rides inside the add's attempts with no retry or refusal of its own

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `C8_no_open_before_and_retry_opens_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_an_open_that_fails_is_refused_on_its_own_retry_before_any_add_is_sent`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
        self._held(playlist_id)
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
            try:
```

New text:

```
        doing = f"add the track {identifier} to the playlist {playlist_id}"

        def attempt() -> Any:
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._session.playlist(playlist_id)
            try:
```

### `u255.M10_failed_attempt_keeps_the_hold`

add_to_playlist attempt: keep the held object after a failed add, so the retry resends the refused tag

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M10_failed_attempt_keeps_the_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_a_track_added_elsewhere_meanwhile_lands_once_and_is_read_back`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
            except Exception:
                self._opened.pop(playlist_id, None)
                raise
```

New text:

```
            except Exception:
                raise
```

### `u255.M11_retry_opens_raw`

add_to_playlist attempt: the retry opens through the session with no retry of its own and no hold, round one's finding three

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M11_retry_opens_raw`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 338 against a baseline of 338
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`

Old text:

```
                playlist = self._held(playlist_id)
            try:
```

New text:

```
                playlist = self._session.playlist(playlist_id)
            try:
```

### `u270.E1_already_on_the_playlist`

apply: read only the ledger for what is already there, so a track a person put on the playlist is sent and recorded as ours

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E1_already_on_the_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/modules/test_outbound.py`, `tests/test_outbound_workers.py`, `tests/test_prune.py`
- Collected: 257 against a baseline of 257
- Kills: 6 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_a_park_between_the_request_and_the_record_blocks_and_the_resume_adds_nothing_twice`
  - `tests/test_outbound_export_batches.py::test_a_stop_between_the_request_and_the_record_adds_nothing_twice_and_records_nothing_unanswered[ceiling-park]`
  - `tests/test_outbound_export_batches.py::test_a_stop_between_the_request_and_the_record_adds_nothing_twice_and_records_nothing_unanswered[refused-read]`
  - `tests/test_outbound_export_batches.py::test_a_track_a_person_adds_after_a_refused_add_is_never_claimed`
  - `tests/test_outbound_export_batches.py::test_a_track_on_the_playlist_or_recorded_is_not_sent`
  - `tests/test_outbound_export_batches.py::test_reads_refused_past_the_retry_fail_the_batch_and_the_resume_adds_nothing_twice`

Old text:

```
        if remote in already_on or remote in already_recorded:
```

New text:

```
        if remote in already_recorded:
```

### `u270.C3_refused_track_fails_its_item`

run_export_items: report a track the provider would not add as an item done with nothing added

- File: `src/cratekit/export/cli.py`
- Source: `u270.json`, row `C3_refused_track_fails_its_item`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 145 against a baseline of 145
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_track_the_provider_would_not_add_fails_its_item_alone_and_is_never_recorded`

Old text:

```
        if refused:
            answered[track_id] = _refused(refused[0], report.remote_id)
            continue
```

New text:

```
        if False:
            answered[track_id] = _refused(refused[0], report.remote_id)
            continue
```

### `u220.A13_exact_agrees`

_settled: read any reading as agreeing with the caller's expected one

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A13_exact_agrees`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
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

### `u220.A17_settle_once`

_settled: take one reading only, never again after a pause

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u220.json`, row `A17_settle_once`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_order.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_calls.py`, `tests/test_prune.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_order.py`
- Collected: 283 against a baseline of 283
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

### `r1308.M11_count_before_ge`

_removal_read_back: a count at or over before's reads as before

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M11_count_before_ge`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
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

### `r1308.M15_lag_always`

_removal_read_back: every reading is a lag, so a wrong track is read again to the bound

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1308.json`, row `M15_lag_always`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_remove_lag.py`, `tests/test_outbound_order.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`, `tests/test_organize_mirror.py`, `tests/test_outbound_tidal_account.py`, `tests/test_sync_pair_calls.py`, `tests/modules/test_outbound.py`
- Collected: 388 against a baseline of 388
- Kills: 12 (killed)
- Killed:
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[a-video]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-flag]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-neither]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-none]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[count-short]`
  - `tests/test_outbound_remove_lag.py::test_a_count_that_is_neither_before_nor_after_refuses_at_once[videos-none]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[as-long-as-before]`
  - `tests/test_outbound_remove_lag.py::test_a_lagging_reading_then_a_wrong_one_refuses_without_spending_the_bound[then-wrong]`
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

### `r1032.A3_unreadable_tie_broken`

_among: break a tie beside a candidate that could not be read

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `A3_unreadable_tie_broken`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 118 against a baseline of 118
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_tie_beside_a_release_that_cannot_be_read_is_left_out_and_asked_again`
  - `tests/test_outbound_tidal_account.py::test_a_refused_tie_is_never_said_to_be_broken`
  - `tests/test_outbound_tidal_account.py::test_an_unreadable_release_beside_the_tie_still_refuses_with_any_agreeing`

Old text:

```
        if any_agreeing and not unreadable:
```

New text:

```
        if any_agreeing:
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

### `r572.H1_hearts_drop_album`

The hearts engine stops passing the album to match_track

- File: `src/cratekit/modules/outbound/hearts.py`
- Source: `r572.json`, row `H1_hearts_drop_album`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_sweep_hearts_the_release_the_files_album_tag_names`

Old text:

```
            album=item.album,
```

New text:

```
(empty)
```

### `r358.A2_title_stripped_for_the_write`

Strip the title for the write as well as for the emptiness test

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A2_title_stripped_for_the_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_title_the_caller_padded_is_written_as_the_caller_asked`

Old text:

```
        wanted = str(name)
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
```

New text:

```
        wanted = str(name).strip()
        doing = f"rename the playlist {playlist_id} to {wanted!r}"
```

### `r572.A2_first_named`

Take the first release the album names even when several do

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r572.json`, row `A2_first_named`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_file_album_matching_both_releases_stays_unmatched`

Old text:

```
        if len(named_album) == 1:
```

New text:

```
        if len(named_album) >= 1:
```

### `r356-a.A3_any_hearted_rather_than_the_only_hearted`

Rule two takes the first hearted release when the account hearts two

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r356-a.json`, row `A3_any_hearted_rather_than_the_only_hearted`
- Moved: the same text, now in src/cratekit/modules/outbound/tidal_reads.py, was in src/cratekit/modules/outbound/tidal_account.py
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_the_album_never_overrides_a_heart_or_breaks_a_tie_between_two`
  - `tests/test_outbound_tidal_account.py::test_two_hearted_releases_spelled_alike_are_still_no_match`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_and_an_album_naming_one_of_them_is_a_broken_tie`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
        if len(hearted) == 1:
```

New text:

```
        if hearted:
```

### `r850-a.E5_slug_is_no_reason`

export._said: take the engine's slug unmatched as something the account said, so it is shown instead of the sentence

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E5_slug_is_no_reason`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_workers.py::test_an_export_with_an_unmatched_track_counts_and_names_it_on_both_renderers`

Old text:

```
    return "" if said == "unmatched" else said
```

New text:

```
    return said
```

### `r850-a.E4_reason_gate`

export.summary: write a reason sentence for every unmatched row, so reasons carries rows the account said nothing about

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E4_reason_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_outbound_tidal_account.py`
- Collected: 236 against a baseline of 236
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`

Old text:

```
            if _said(item):
```

New text:

```
            if True:
```

### `u51-item-derivation.A2_default_favorites_playlist`

Default the sweep to the FOLDER name the live library uses

- File: `src/cratekit/modules/outbound/source.py`
- Source: `u51-item-derivation.json`, row `A2_default_favorites_playlist`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 143 against a baseline of 143
- Kills: 27 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_provider_that_already_hearts_a_row_is_reported_rather_than_written`
  - `tests/test_outbound_workers.py::test_a_second_sweep_writes_nothing_because_the_ledger_remembers`
  - `tests/test_outbound_workers.py::test_a_sweep_runs_with_rekordbox_open_and_never_opens_the_database`
  - `tests/test_outbound_workers.py::test_a_sweep_where_every_favourite_matches_answers_with_no_unmatched_line`
  - `tests/test_outbound_workers.py::test_a_sweep_with_an_unmatched_favourite_counts_and_names_it_on_both_renderers`
  - `tests/test_outbound_workers.py::test_an_empty_playlist_refuses_distinguishably_from_an_absent_one`
  - `tests/test_outbound_workers.py::test_an_item_report_carries_no_empty_colored_list`
  - `tests/test_outbound_workers.py::test_an_unmatched_favourite_is_reported_and_does_not_fail_its_item`
  - `tests/test_outbound_workers.py::test_job_show_reports_the_bound_worker_for_a_queued_sweep`
  - `tests/test_outbound_workers.py::test_no_colour_writer_reaches_the_engine_from_a_queued_sweep`
  - ... and 12 more, see the JSON sidecar

Old text:

```
DEFAULT_FAVORITES_PLAYLIST = "All Favorites"
```

New text:

```
DEFAULT_FAVORITES_PLAYLIST = "Favorites"
```

### `r856-a.S2_tally_bool`

shell._whole: take a bool for a count, so True reads as one unmatched and as one in the total

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r856-a.json`, row `S2_tally_bool`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_render_payloads.py`
- Collected: 178 against a baseline of 178
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_the_sweep_warning_counts_only_whole_numbers`
  - `tests/test_outbound_workers.py::test_the_unmatched_warning_reads_only_whole_counts[bool-is-no-count]`
  - `tests/test_outbound_workers.py::test_the_unmatched_warning_reads_only_whole_counts[bool-unmatched]`

Old text:

```
    return isinstance(value, int) and not isinstance(value, bool)
```

New text:

```
    return isinstance(value, int)
```

### `u51-item-derivation.S3_empty_job_driven`

Drive a job with no items, which core.jobs reports as SUCCEEDED

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `u51-item-derivation.json`, row `S3_empty_job_driven`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_job_with_no_items_refuses_rather_than_reporting_a_clean_success`

Old text:

```
            if not jobs.items(store, job.job_id):
```

New text:

```
            if False:
```

### `u131.K9_export_refusal_kept`

export.apply: let a ledger or raw error filing at creation fail the finished export

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u131.json`, row `K9_export_refusal_kept`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_export_collection.py`, `tests/test_outbound_workers.py`
- Collected: 234 against a baseline of 234
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`

Old text:

```
        except Exception as exc:  # noqa: BLE001 - reported as the warning
```

New text:

```
        except KeyError as exc:  # noqa: BLE001 - reported as the warning
```

### `u131.K2_exports_rule`

filing.plan: drop the Exports rule, so an exported playlist is read as product made and left

- File: `src/cratekit/organize/filing.py`
- Source: `u131.json`, row `K2_exports_rule`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 109 against a baseline of 109
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_an_exported_playlist_the_product_made_is_not_listed_as_yours`
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`

Old text:

```
        if identity in exported:
```

New text:

```
        if False:
```

### `r1305.A2_account_status_declared_only`

_session_refused: read a status on the declared chain only, so a session rejected mid sweep with a page is told to wait

- File: `src/cratekit/modules/outbound/account.py`
- Source: `r1305.json`, row `A2_account_status_declared_only`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_rejection_bodies.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`
- Collected: 197 against a baseline of 197
- Kills: 6 (killed)
- Killed:
  - `tests/test_provider_rejection_bodies.py::test_a_login_failure_that_is_no_rejection_is_a_wait[outage]`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_drops_the_held_account`
  - `tests/test_provider_rejection_bodies.py::test_a_rejection_whose_body_is_not_json_rewrapped_by_the_client_still_asks_for_a_login`
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

### `r836-a.A1_product_made_asked_first`

tidal_account.remove_tracks: the ledger is never asked, so a playlist the product did not create loses tracks

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r836-a.json`, row `A1_product_made_asked_first`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_organize_root.py`, `tests/test_sync_pair_account.py`
- Collected: 112 against a baseline of 112
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_heard.py::test_the_adapter_refuses_a_playlist_the_ledger_does_not_vouch_for_unasked`
  - `tests/test_organize_root.py::test_the_generic_removal_still_refuses_an_unrecorded_playlist`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_is_never_removed_whole`

Old text:

```
        if self._cfg is None or not ledger.product_made(self._cfg, identifier):
```

New text:

```
        if False:
```

### `r836-c.L6_date_on_the_confirmed_record`

ledger._note_written: the export date goes on the key's own record, not the one the job was confirmed to update

- File: `src/cratekit/modules/outbound/ledger_reserve.py`
- Source: `r836-c.json`, row `L6_date_on_the_confirmed_record`
- Moved: the same text, now in src/cratekit/modules/outbound/ledger_reserve.py, was in src/cratekit/modules/outbound/ledger.py
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

### `u227.R4_folder_compare`

_landed_there: compare the playlist alone, so another genre's band of the same name reads as the landing's

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R4_folder_compare`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_repair_rows.py`
- Collected: 22910 against a baseline of 22910
- Kills: 0 (zero)
- Promoted: subset killed 0, full suite killed 0
- Note: confirmed on the full suite

Old text:

```
    return bool(there) and all((place.folder, place.playlist) in places for place in there)
```

New text:

```
    return bool(there) and all(any(place.playlist == one[1] for one in places) for place in there)
```

### `u174.O3_no_pass_counted`

_mark_steps: drop the fact counting native landings of no sync pass

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O3_no_pass_counted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 164 against a baseline of 164
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step`

Old text:

```
        area.facts["native landings of no sync pass"] = unlanded
```

New text:

```
        pass
```

### `u130-c.C6_pair_not_vouched`

The account seam refuses a removal from a paired playlist

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u130-c.json`, row `C6_pair_not_vouched`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_account.py`, `tests/test_prune.py`
- Collected: 67 against a baseline of 67
- Kills: 5 (killed)
- Killed:
  - `tests/test_sync_pair_account.py::test_a_move_that_landed_elsewhere_is_left_to_the_settle_reading_with_every_track_kept`
  - `tests/test_sync_pair_account.py::test_a_paired_playlist_takes_a_removal`
  - `tests/test_sync_pair_account.py::test_a_track_held_twice_is_not_moved`
  - `tests/test_sync_pair_account.py::test_an_order_already_standing_sends_nothing`
  - `tests/test_sync_pair_account.py::test_the_order_moves_each_track_to_the_front_and_reads_back`

Old text:

```
            ledger.product_made(self._cfg, identifier) or pairs.paired(self._cfg, identifier)
```

New text:

```
            ledger.product_made(self._cfg, identifier)
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

### `u129-author.A17_empty_add_still_writes`

Force writes true when every row of the set is unmatched

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u129-author.json`, row `A17_empty_add_still_writes`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u129_set_account_playlist.py`
- Collected: 24 against a baseline of 24
- Kills: 3 (killed)
- Killed:
  - `tests/test_u129_set_account_playlist.py::test_a_rerun_of_export_set_plans_nothing_when_every_matched_track_is_on_it`
  - `tests/test_u129_set_account_playlist.py::test_a_rerun_of_intake_set_plans_nothing_when_the_playlist_already_holds_the_tracks`
  - `tests/test_u129_set_account_playlist.py::test_a_set_with_no_matches_makes_nothing_and_says_so`

Old text:

```
        return bool(self.add)

```

New text:

```
        return True

```

### `r835-b.T1_folder_create_never_retried`

TidalAccount.create_folder: a create that timed out after reaching the provider is retried into a second folder

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r835-b.json`, row `T1_folder_create_never_retried`
- Moved: the never retried folder create stayed in TidalAccount.create_folder in tidal_account.py, but its call to _call now sits on one line assigned to created; the same retries=0 is raised to 1
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folder_create_is_never_retried_into_a_second_folder`

Old text:

```
        created = self._call(doing, lambda: self._session.user.create_folder(name), retries=0)

```

New text:

```
        created = self._call(doing, lambda: self._session.user.create_folder(name), retries=1)

```

### `u236.M18_ledger_placement_not_written`

ledger settle: never write a placement

- File: `src/cratekit/modules/outbound/ledger_settle.py`
- Source: `u236.json`, row `M18_ledger_placement_not_written`
- Moved: the placement write in settle_mirror_tracks moved from ledger.py into ledger_settle.settle_mirror_tracks, with record and name now on one line; the same _place call is deleted
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits_u236.py`
- Collected: 25 against a baseline of 25
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
            _place(
                record, name,
                {**_placements(record.get("placed")).get(str(name), {}), str(track): str(at)},
            )
            wrote = True

```

New text:

```
            wrote = True

```

### `u147-d.A5_source_title`

account_mirror.read_library: All Favorites takes the folder's prefix like every other playlist

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u147-d.json`, row `A5_source_title`
- Moved: the favorites folder titler stayed in account_mirror.read_library but sits one level shallower after the function was reshaped, so only its indentation changed; the same source title exemption is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_library.py`
- Collected: 3 against a baseline of 3
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_library.py::test_every_genre_folder_and_the_favorites_folder_is_read_under_its_account_titles`

Old text:

```
                return shown if shown == source else mirror.title(name, shown)

```

New text:

```
                return mirror.title(name, shown)

```

### `r1031.M4_signature_dropped`

Matcher.under: drop the file signature, so a file that gains a code is never asked again

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1031.json`, row `M4_signature_dropped`
- Moved: Matcher.under in mirror.py now returns its tuple on one line instead of one element per line; the same signature element is replaced by an empty string
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`
- Collected: 37 against a baseline of 37
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_file_that_gains_a_code_is_asked_again_and_an_unchanged_one_is_not`

Old text:

```
        return (row.isrc, row.title, row.artist, row.path, "" if row.isrc else self._signature(row))

```

New text:

```
        return (row.isrc, row.title, row.artist, row.path, "")

```

### `r1032.S1_protocol_default_on`

TidalAccount.match_track: default any_agreeing on, so the hearts, the pairs and the exports, which never pass it, break the tie R-572 refuses

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r1032.json`, row `S1_protocol_default_on`
- Moved: match_track moved from TidalAccount in tidal_account.py to the Reads base class in tidal_reads.py, which TidalAccount inherits, with its keyword parameters packed onto two lines; the same any_agreeing default is turned on
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
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
        agree: bool = False, album: str = "", any_agreeing: bool = False,
    ) -> str | None:

```

New text:

```
        agree: bool = False, album: str = "", any_agreeing: bool = True,
    ) -> str | None:

```

### `r879-b.T1_one_track_never_asked_to_agree`

TidalAccount.match_track: return one track under a code whether or not agree is asked

- File: `src/cratekit/modules/outbound/tidal_reads.py`
- Source: `r879-b.json`, row `T1_one_track_never_asked_to_agree`
- Moved: the one track shortcut moved with match_track from TidalAccount in tidal_account.py to Reads in tidal_reads.py, one level shallower; the same not agree condition is dropped
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 113 against a baseline of 113
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

### `r227.S6_no_stale_sentence`

A stale export produces no warning at all

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S6_no_stale_sentence`
- Moved: age_warnings in shell.py was rewritten as one if and elif chain that sets the code and message, so the stale branch is now an elif rather than its own if returning the warning; the same stale condition is made false
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 123 against a baseline of 123
- Kills: 8 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_date_is_the_persons_own_and_not_greenwichs`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_queueing_envelope_warns_that_the_export_is_old[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_sentence_does_not_say_seven_is_past_seven`

Old text:

```
    elif age.stale:

```

New text:

```
    elif False:

```

