# Mutation table: u309-replay-before-c

Measured by `scripts/mutate.py` on 2026-11-22 21:48 UTC, branch `HEAD` at `c9192091`. Pass kind: replay.

A replay pass measures again rows a table under `docs/mutation/` already recorded, so it has no row cap and chooses no rows: every row below names the table and the id it came from. One full baseline and one null control serve the batch, and each row ran on its own subset (U297).

Baseline: green, 22933 collected. pytest invocations for this batch: 162.

Full baseline: READ, not measured by this driver; read from the battery's verdict, `.cloud-battery/verdict.json`, written by `cloud_battery.py baseline` at 2026-11-22 21:47 UTC for commit `c919209162e4`: the same commit on a clean tree, the same machine, checkout and interpreter, and the same known failures file. The null control below ran the full suite in this driver's own environment and was held to that collected count (U271).

Subset baselines: 53, each measured by this driver.

Known failures: 249 node ids whose failure is this machine's and not the tree's, read from `.cloud-battery/baseline.txt` and subtracted from every run, the baselines and the rows alike. The baseline is green net of them, and a death among them is not counted. This is a Linux measure of a macOS suite; the full battery is owed on a Mac.

Temporary files: on disk, the place the known failures were measured in, each run given a fresh directory there as `TMPDIR` (U273).

Environment: inherited from the calling shell, then added to. Added: PYTHONDONTWRITEBYTECODE=1; PYTHONPATH (the plugin's temp directory, prepended); MUTATE_REPORT_PATH (the plugin's output file); TMPDIR, with a known failures file only (a fresh directory in the place its baseline was measured in, or on disk for the tests rerun there, U273); the installation state sandbox: CRATEKIT_CONFIG_DIR, CRATEKIT_PROVIDER_GATE_DIR, CRATEKIT_STATE_DIR, HOME, USERPROFILE, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_STATE_HOME (all pointed inside the run's workspace, R-343). Removed: PYTEST_ADDOPTS (an inherited value would edit the command after the driver built it); PYTEST_XDIST_WORKER (the reporting plugin reads it to tell a worker from the controller, so a driver started from inside a parallel worker would hand its child a controller that believes it is a worker and writes no report; xdist sets it afresh in each worker the child starts); PYTEST_XDIST_WORKER_COUNT (the same inherited worker identity, scrubbed with it); PYTEST_XDIST_TESTRUNUID (the same inherited worker identity, scrubbed with it). Nothing else was scrubbed, because a hand built environment is how a missing binary reddens a baseline and every row after it.

Installation state: the watched roots are unchanged. Fingerprinted before the first child this run started and after every one of them: ~/.config/cratekit (0 entries); ~/.local/state/cratekit (0 entries). A change would have stopped the batch at the child that was running. Every child ran with its own throwaway installation state, so a test that undoes the suite's isolation lands there rather than on this machine (R-343). Only those roots are watched; the sandbox also redirects HOME and the data root, and a child reaching one of those is not seen by this guard.

Null control `NULL_CONTROL`: killed 0, collected 22933 against 22933. The control is a semantically empty change, so a zero here is what makes every other number in this table believable.

## Summary

| id | file | surface | subset | collected | kills | status |
| --- | --- | --- | --- | --- | --- | --- |
| `r835-a.L3_recorded_year_never_created_again` | `src/cratekit/modules/outbound/ledger.py` | user | 4 file(s) | 350 | 4 | killed |
| `r229.L5_no_crate_side_bound` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r229.L6_a_living_crate_is_a_candidate` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 3 | killed |
| `r229.L7_a_reused_path_keeps_its_record` | `src/cratekit/modules/outbound/ledger.py` | user | 3 file(s) | 294 | 2 | killed |
| `r1394.A2_sent_one_short` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 5 | killed |
| `r1394.A3_landed_overstated` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 4 | killed |
| `r1394.A4_412_not_brought_down` | `src/cratekit/modules/outbound/tidal_account.py` | user | 24 file(s) | 1311 | 2 | killed |
| `u205.S2_account_rejection_read_as_wait` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 177 | 2 | killed |
| `u142.S7_adoption_is_a_write` | `src/cratekit/modules/outbound/sets.py` | user | 3 file(s) | 229 | 2 | killed |
| `r837-b.B2_isrc_route` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-a.A6_refused_split` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S9_ambiguous_full_said_as_bound` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r879-b.S4_several_codes_take_one` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 56 | 1 | killed |
| `r837-b.A9r_recorded_folder_listed` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 56 | 2 | killed |
| `r1017.M10_older_beats_to` | `src/cratekit/modules/outbound/sets.py` | user | 4 file(s) | 195 | 2 | killed |
| `u140.B9_abort_applies` | `src/cratekit/export/set_cli.py` | user | 1 file(s) | 29 | 1 | killed |
| `u140.A6_refreeze_account_spelling` | `src/cratekit/modules/outbound/sets.py` | user | 1 file(s) | 29 | 1 | killed |
| `u214.M10_detail_names` | `src/cratekit/organize/account_mirror.py` | user | 6 file(s) | 201 | 4 | killed |
| `u207.M1_mirror_screens_settled_rows` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 72 | 2 | killed |
| `u137.A8_labels_module_off` | `src/cratekit/organize/account.py` | user | 2 file(s) | 122 | 1 | killed |
| `u143-d.A6_legacy_name` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 2 | killed |
| `u143-d.A8_folder_read_back` | `src/cratekit/modules/outbound/tidal_account.py` | user | 7 file(s) | 451 | 1 | killed |
| `r835-a.F3_root_folder_adopted_by_name` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 3 | killed |
| `r835-a.F5_unplaced_recorded_year_is_moved` | `src/cratekit/modules/outbound/folders.py` | user | 1 file(s) | 56 | 2 | killed |
| `u230.M22_agreed_lifted` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 225 | 3 | killed |
| `u230.M14_no_titles_guard` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 225 | 6 | killed |
| `u230.M1_no_lift` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 11 file(s) | 225 | 6 | killed |
| `u227.R5_landed_flag` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 7 file(s) | 196 | 2 | killed |
| `u236.M17_ledger_settle_keeps_placement` | `src/cratekit/modules/outbound/ledger.py` | user | 8 file(s) | 233 | 4 | killed |
| `u236.M13_write_records_no_month` | `src/cratekit/organize/mirror_edits.py` | user | 8 file(s) | 233 | 6 | killed |
| `u236.M9_placed_after_ignores_hold` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 233 | 2 | killed |
| `u236.M4_moved_counts_to` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 8 file(s) | 233 | 1 | killed |
| `u201-composites.C2_agrees_never` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 195 | 1 | killed |
| `u201.E10_unknown_time` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 195 | 4 | killed |
| `u201-composites.C1_two_bands_composite` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 5 file(s) | 195 | 1 | killed |
| `u204.P10_inbox_agreed` | `src/cratekit/modules/outbound/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O2_unfavourite_leaves_months` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O3_quarter_refused` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u204.O7_restore_detected` | `src/cratekit/organize/mirror_edits.py` | user | 6 file(s) | 233 | 1 | killed |
| `u112.A4_in_folder_listed` | `src/cratekit/organize/account.py` | user | 1 file(s) | 100 | 1 | killed |
| `u116.M10_year_check` | `src/cratekit/organize/filing.py` | user | 1 file(s) | 22933 | 1 (promoted) | killed |
| `u137.S2_only_fact` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 100 | 2 | killed |
| `u142.S17_proof_not_named` | `src/cratekit/organize/account.py` | user | 1 file(s) | 100 | 1 | killed |
| `u112.R1_no_ack_planned` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 100 | 6 | killed |
| `u137.S3_wants_everything` | `src/cratekit/organize/steps.py` | user | 1 file(s) | 100 | 13 | killed |
| `u112.C6_failure_never_raised` | `src/cratekit/organize/cli.py` | user | 1 file(s) | 100 | 3 | killed |
| `u112.R5_actor_invented` | `src/cratekit/organize/rekordbox.py` | user | 1 file(s) | 100 | 1 | killed |
| `u246.S5_inspiration_held_empty` | `src/cratekit/organize/inspiration.py` | user | 4 file(s) | 333 | 9 | killed |
| `r1295.M8_none_read_withheld_dropped` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-c.C4_missed_coefficient` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M6_none_read_uncapped` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-c.C1_again_now_held` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `r1295.M7_none_read_rest_uncounted` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u144-c.C2_folder_unread` | `src/cratekit/organize/inspiration.py` | user | 1 file(s) | 39 | 1 | killed |
| `u147-c.M15_malformed_mirrors_read` | `src/cratekit/modules/outbound/ledger.py` | user | 1 file(s) | 35 | 1 | killed |
| `u147-b.M2_stale_folder_again` | `src/cratekit/modules/outbound/mirror.py` | user | 1 file(s) | 35 | 1 | killed |
| `r1289.M16_mirror_why` | `src/cratekit/organize/mirror_downloads.py` | user | 3 file(s) | 105 | 1 | killed |
| `r1031.M16_report_records` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 173 | 2 | killed |
| `r1031.M19_unfreezable_plan_refuses` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 73 | 1 | killed |
| `r1031.M20_signature_constant` | `src/cratekit/organize/account_mirror.py` | user | 2 file(s) | 73 | 1 | killed |
| `u222.M19_stale_on_every_run` | `src/cratekit/organize/account_mirror.py` | maintainer | 6 file(s) | 259 | 1 | killed |
| `u222.M8_agreed_list_check` | `src/cratekit/organize/mirror_frozen.py` | maintainer | 6 file(s) | 259 | 1 | killed |
| `u222.M16_lines_inverted` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 259 | 4 | killed |
| `u222-zeros.M5_agreed_none_lost` | `src/cratekit/organize/mirror_frozen.py` | user | 6 file(s) | 259 | 1 | killed |
| `u150.A5_deletes_named` | `src/cratekit/organize/account_mirror.py` | user | 3 file(s) | 167 | 1 | killed |
| `u150.M2_present_guard` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 105 | 2 | killed |
| `u150.M9_known_answers` | `src/cratekit/modules/outbound/mirror.py` | user | 3 file(s) | 105 | 1 | killed |
| `r1032.M1_mirror_never_asks_any_agreeing` | `src/cratekit/modules/outbound/mirror.py` | user | 4 file(s) | 110 | 4 | killed |
| `u143-a.R3_no_count` | `src/cratekit/organize/root.py` | user | 1 file(s) | 56 | 1 | killed |
| `u143-a.R2_short_read` | `src/cratekit/organize/root.py` | user | 1 file(s) | 56 | 1 | killed |
| `u255.M6_held_never_stores` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 3 | killed |
| `u255.M7_held_always_opens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 9 | killed |
| `u255.M9_every_attempt_opens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 5 file(s) | 330 | 11 | killed |
| `u270.A1_failed_attempt_reopens` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 157 | 2 | killed |
| `u270.E3_second_row_of_one_track` | `src/cratekit/modules/outbound/export.py` | user | 2 file(s) | 147 | 1 | killed |
| `u220.A14_multiset_agrees` | `src/cratekit/modules/outbound/tidal_account.py` | user | 6 file(s) | 287 | 1 | killed |
| `r1308.M21_halves_swapped` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 1 | killed |
| `r1308.M22_retryable` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 14 | killed |
| `r1308.M8_count_ignored` | `src/cratekit/modules/outbound/tidal_account.py` | user | 8 file(s) | 387 | 9 | killed |
| `r1032.A6_first_listed_not_lowest` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 116 | 7 | killed |
| `r227.A7_unreadable_reads_as_now` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 2 | killed |
| `r356-b.B4_heart_candidate_carries_no_artist` | `src/cratekit/modules/outbound/source.py` | user | 4 file(s) | 371 | 4 | killed |
| `u208.M19_adapter_never_records_tie` | `src/cratekit/modules/outbound/tidal_account.py` | user | 2 file(s) | 132 | 5 | killed |
| `r356-a.A4_hearts_asked_of_every_track` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r834.M1_a_create_makes_the_playlist_private` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 5 | killed |
| `r356-a.A9_row_may_name_an_artist_nobody_bills` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 1 | killed |
| `u97-c.C1_outbound_refusal_removed` | `src/cratekit/modules/outbound/account.py` | user | 1 file(s) | 111 | 1 | killed |
| `r358.A1_empty_title_refusal` | `src/cratekit/modules/outbound/tidal_account.py` | user | 1 file(s) | 111 | 3 | killed |
| `u226.M17_removal_positions_unsettled` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 3 | killed |
| `u226.M15_wait_uncounted` | `src/cratekit/modules/outbound/tidal_account.py` | user | 9 file(s) | 441 | 2 | killed |
| `r850-a.E6_no_match_sentence` | `src/cratekit/export/cli.py` | user | 2 file(s) | 236 | 2 | killed |
| `u131.K12_filing_as_shown` | `src/cratekit/modules/outbound/kinds.py` | user | 2 file(s) | 139 | 1 | killed |
| `u51-item-derivation.S5_payload_shape` | `src/cratekit/modules/outbound/shell.py` | user | 2 file(s) | 145 | 65 | killed |
| `r229.C3_no_remote_id_is_frozen` | `src/cratekit/export/cli.py` | user | 1 file(s) | 125 | 1 | killed |
| `r227.S1_unknown_is_within_limit` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 125 | 1 | killed |
| `r227.S2_no_sentence_at_the_gate` | `src/cratekit/modules/outbound/shell.py` | user | 1 file(s) | 125 | 5 | killed |
| `u131.K10_kind_created_named` | `src/cratekit/modules/outbound/kinds.py` | maintainer | 2 file(s) | 114 | 1 | killed |
| `r1313.T1_account_skips_the_classifier` | `src/cratekit/modules/outbound/tidal_account.py` | user | 3 file(s) | 227 | 5 | killed |
| `u261.A1_account_forget_keeps_the_session` | `src/cratekit/modules/outbound/account.py` | user | 2 file(s) | 141 | 25 | killed |
| `r836-g.C3_dangling_rows_are_rows` | `src/cratekit/export/prune_cli.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-b.L1_adopted_anywhere_wins` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `r836-b.L5_older_export_refused` | `src/cratekit/modules/outbound/ledger.py` | user | 5 file(s) | 404 | 1 | killed |
| `u174.O4_no_pass_is_no_step` | `src/cratekit/organize/account.py` | user | 2 file(s) | 169 | 1 | killed |
| `u216.M24_read_unvalidated` | `src/cratekit/modules/outbound/pairs.py` | user | 12 file(s) | 383 | 4 | killed |
| `u198.P2_release_side` | `src/cratekit/modules/outbound/pairs.py` | user | 3 file(s) | 166 | 3 | killed |
| `u221.R17_release_a_pair_that_is_no_twin` | `src/cratekit/modules/outbound/pairs.py` | maintainer | 1 file(s) | 32 | 1 | killed |
| `u242.M23_filing_dates_a_found_prefix` | `src/cratekit/organize/filing.py` | user | 3 file(s) | 202 | 3 | killed |

## Row definitions

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

### `r1394.A2_sent_one_short`

adapter order: the recorder is told one move fewer sent than is about to go, so a move in flight is read as known not to have landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A2_sent_one_short`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_recorder_that_cannot_record_has_no_further_move_sent`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number - 1, number - 1)
```

### `r1394.A3_landed_overstated`

adapter order: the recorder is told the move about to go has already landed

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A3_landed_overstated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 4 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_move_that_failed_another_way_is_left_as_maybe_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`
  - `tests/test_outbound_order.py::test_the_caller_is_told_before_each_move_how_many_may_have_landed`

Old text:

```
                    told(number, number - 1)
```

New text:

```
                    told(number, number)
```

### `r1394.A4_412_not_brought_down`

adapter order: a move spent on its 412s is left as maybe landed, its sent count never brought back down

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1394.json`, row `A4_412_not_brought_down`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_adapter_listing.py`, `tests/test_catalogue_app.py`, `tests/test_isrc_cache.py`, `tests/test_isrc_screen.py`, `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_tie.py`, `tests/test_organize_root.py`, `tests/test_outbound_order.py`, `tests/test_outbound_remove_lag.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_window_lag.py`, `tests/test_provider_gate.py`, `tests/test_provider_not_found_bodies.py`, `tests/test_prune.py`, `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_settle.py`, `tests/test_sync_pair_stopped.py`, `tests/test_sync_pair_stopped_order.py`, `tests/test_sync_pair_tie.py`
- Collected: 1311 against a baseline of 1311
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_order.py::test_a_move_spent_on_its_412s_is_told_as_not_landed`
  - `tests/test_outbound_order.py::test_a_stop_in_the_pause_after_a_412_is_recorded_as_no_move_in_flight`

Old text:

```
                        told(number - 1, number - 1)
```

New text:

```
                        pass
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

### `u142.S7_adoption_is_a_write`

ArchivePlan.writes: count an adoption alone as a write again, so a set already filed by hand reads as planned

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u142.json`, row `S7_adoption_is_a_write`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`, `tests/test_organize.py`, `tests/test_set_inspiration_playlist.py`
- Collected: 229 against a baseline of 229
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_organize.py::test_a_set_already_prefixed_in_its_downloaded_sets_folder_plans_nothing`

Old text:

```
        return self.move or self.mark
```

New text:

```
        return self.folder_action in (CREATE, ADOPT) or self.move or self.mark
```

### `r837-b.B2_isrc_route`

set_cli.match_rows: a row's ISRC is never asked of the account, so it goes to the text search

- File: `src/cratekit/export/set_cli.py`
- Source: `r837-b.json`, row `B2_isrc_route`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_row_carrying_an_isrc_is_matched_through_the_accounts_own_match`

Old text:

```
            if one.isrc:
```

New text:

```
            if False:
```

### `r837-a.A6_refused_split`

sets.apply_set: a track the provider would not add is not counted as refused

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-a.json`, row `A6_refused_split`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_track_refused_before_is_said_as_refused_not_as_on_the_playlist`

Old text:

```
        refused = [one for one in chunk if one not in held]
```

New text:

```
        refused = []
```

### `r879-b.S9_ambiguous_full_said_as_bound`

_not_chosen: say two readings only with an exact match, so a full first page of an ambiguous row is said as the bound

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S9_ambiguous_full_said_as_bound`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_title_read_two_ways_on_a_full_page_says_so_and_not_the_bound`

Old text:

```
    if answer.ambiguous and (exact or answer.full):
```

New text:

```
    if answer.ambiguous and exact:
```

### `r879-b.S4_several_codes_take_one`

file_isrc: take one of several distinct codes the held copies carry

- File: `src/cratekit/export/set_cli.py`
- Source: `r879-b.json`, row `S4_several_codes_take_one`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set.py::test_held_copies_carrying_different_isrcs_ask_the_account_nothing`

Old text:

```
        if len(codes) == 1:
```

New text:

```
        if codes:
```

### `r837-b.A9r_recorded_folder_listed`

batch a's A9 again: sets.plan_archive reuses a recorded year folder the account no longer lists

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r837-b.json`, row `A9r_recorded_folder_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set.py::test_a_set_put_in_its_folder_by_hand_writes_nothing_and_its_gate_says_so`
  - `tests/test_export_set.py::test_a_year_folder_deleted_on_the_account_is_made_again`

Old text:

```
    if recorded and recorded in root:
```

New text:

```
    if recorded:
```

### `r1017.M10_older_beats_to`

Plan: hold an older name's record ahead of the one under the new name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `r1017.json`, row `M10_older_beats_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`, `tests/test_set_inspiration_playlist.py`, `tests/test_u129_set_account_playlist.py`, `tests/test_sync_mark.py`
- Collected: 195 against a baseline of 195
- Kills: 2 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_is_refused_rather_than_adopted`
  - `tests/test_export_set_rename.py::test_a_twin_under_the_new_name_still_refuses_when_the_landing_names_the_old`

Old text:

```
    held = recorded_to or (older[0] if older else None)
```

New text:

```
    held = (older[0] if older else None) or recorded_to
```

### `u140.B9_abort_applies`

the rename writes when the gate was answered abort

- File: `src/cratekit/export/set_cli.py`
- Source: `u140.json`, row `B9_abort_applies`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_an_aborted_rename_writes_nothing`

Old text:

```
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if option != "apply" or not built.writes:

```

New text:

```
    option = ctx.gate.require(gate, plan=built.payload, context=built.shown)
    if not built.writes:

```

### `u140.A6_refreeze_account_spelling`

apply_rename refreezes the account spelling rather than the INSPIRATION playlist's own name

- File: `src/cratekit/modules/outbound/sets.py`
- Source: `u140.json`, row `A6_refreeze_account_spelling`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_export_set_rename.py`
- Collected: 29 against a baseline of 29
- Kills: 1 (killed)
- Killed:
  - `tests/test_export_set_rename.py::test_a_name_with_a_slash_freezes_as_the_library_spells_it`

Old text:

```
        refreeze(planned.live or planned.to)

```

New text:

```
        refreeze(planned.to)

```

### `u214.M10_detail_names`

_detail: never name the unmirrored nodes on the step's line, so the report shows only a count

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u214.json`, row `M10_detail_names`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_inbox_unmirrored.py`, `tests/test_inbox_rotate.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_inbox_analyzed.py`, `tests/test_organize_mirror.py`
- Collected: 201 against a baseline of 201
- Kills: 4 (killed)
- Killed:
  - `tests/test_inbox_unmirrored.py::test_a_rebuild_from_the_frozen_plan_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_no_batch_at_all_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_an_inbox_with_nothing_to_write_still_names_them`
  - `tests/test_inbox_unmirrored.py::test_the_inbox_step_names_each_unmirrored_node_on_its_plan_and_its_line`

Old text:

```
    if folder is not None and folder.unmirrored:
```

New text:

```
    if False:
```

### `u207.M1_mirror_screens_settled_rows`

mirror: the matcher screens every row with a code, a link, a recorded track and a remembered miss included

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u207.json`, row `M1_mirror_screens_settled_rows`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_isrc_screen.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_tie.py`
- Collected: 72 against a baseline of 72
- Kills: 2 (killed)
- Killed:
  - `tests/test_isrc_screen.py::test_the_mirror_screens_only_the_rows_it_would_ask_the_provider_about`
  - `tests/test_organize_mirror.py::test_the_plan_screens_every_code_its_rows_will_ask_before_asking_any`

Old text:

```
            if self._settled(row) is None and (said := self._identity(row)).isrc
```

New text:

```
            if (said := self._identity(row)).isrc
```

### `u137.A8_labels_module_off`

Refuse the filing over an unread registry the profile does not use

- File: `src/cratekit/organize/account.py`
- Source: `u137.json`, row `A8_labels_module_off`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_dated.py`, `tests/test_organize.py`
- Collected: 122 against a baseline of 122
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_registry_the_profile_does_not_use_does_not_refuse_the_filing`

Old text:

```
            unfollowed if LABELS_MODULE in available else None,
```

New text:

```
            unfollowed,
```

### `u143-d.A6_legacy_name`

Adapter: remove a root folder whatever its name

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A6_legacy_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[2026-0-not-a-legacy-folder]`
  - `tests/test_organize_root.py::test_a_folder_not_legacy_or_not_empty_is_refused_before_any_removal[Phil's Spotify-0-not-a-legacy-folder]`

Old text:

```
        if not kinds.legacy_year(name):
```

New text:

```
        if False:
```

### `u143-d.A8_folder_read_back`

Adapter: report a folder removed though the root still lists it

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u143-d.json`, row `A8_folder_read_back`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_heard.py`, `tests/test_label_playlists.py`, `tests/test_organize_root.py`, `tests/test_outbound_tidal_account.py`, `tests/test_provider_gate.py`, `tests/test_prune.py`, `tests/test_sync_pair_account.py`
- Collected: 451 against a baseline of 451
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_legacy_folder_still_listed_after_its_removal_is_refused`

Old text:

```
        if identifier in self.folders():
```

New text:

```
        if False:
```

### `r835-a.F3_root_folder_adopted_by_name`

folders.plan: a root folder already named as the label is never adopted, so a second folder of that name is created

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F3_root_folder_adopted_by_name`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 3 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_folder_made_by_hand_at_the_root_is_adopted`
  - `tests/test_label_playlists.py::test_an_unrecorded_marked_year_in_the_folder_is_matched_by_its_marked_name`
  - `tests/test_label_playlists.py::test_two_playlists_named_for_one_year_leave_that_year_alone`

Old text:

```
        if named:
            folder_action, folder_id = ADOPT, named[0]
```

New text:

```
        if False:
            folder_action, folder_id = ADOPT, named[0]
```

### `r835-a.F5_unplaced_recorded_year_is_moved`

folders.plan: a recorded year playlist that is not in the folder is never moved into it, so a build stopped after its create leaves it at the root

- File: `src/cratekit/modules/outbound/folders.py`
- Source: `r835-a.json`, row `F5_unplaced_recorded_year_is_moved`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_label_playlists.py`
- Collected: 56 against a baseline of 56
- Kills: 2 (killed)
- Killed:
  - `tests/test_label_playlists.py::test_a_label_folder_deleted_on_the_account_is_made_again_and_recorded`
  - `tests/test_label_playlists.py::test_a_playlist_made_and_not_yet_moved_is_moved_on_the_resume_and_not_made_again`

Old text:

```
                    move=not placed,
```

New text:

```
                    move=False,
```

### `u230.M22_agreed_lifted`

_as_queued: lift an agreed snapshot too, so a drag back after the carry is carried back (round one's BLOCKING)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M22_agreed_lifted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 225 against a baseline of 225
- Kills: 3 (killed)
- Killed:
  - `tests/test_mirror_edits_u230.py::test_an_agreed_snapshot_that_holds_the_track_is_the_librarys_word`
  - `tests/test_organize_mirror_edits_u230.py::test_a_drag_back_into_the_landings_band_after_the_batch_left_inbox_stands`
  - `tests/test_organize_mirror_edits_u230.py::test_an_agreed_snapshot_holding_the_track_is_the_librarys_word`

Old text:

```
        and one.agreed is None

```

New text:

```
        and True

```

### `u230.M14_no_titles_guard`

_as_queued: a track with landing places and no queue is lifted on every playlist

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M14_no_titles_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 225 against a baseline of 225
- Kills: 6 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_hand_move_back_into_the_landings_band_after_the_edit_was_carried_stands`
  - `tests/test_mirror_edits_u227.py::test_a_landing_filed_into_the_place_the_account_asked_agrees`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`
  - `tests/test_mirror_edits_u227.py::test_a_track_a_snapshot_held_is_read_by_the_later_change_rule_alone`
  - `tests/test_mirror_edits_u230.py::test_the_same_reading_without_the_queue_is_no_edit_at_all_as_before`

Old text:

```
    if not titles or not places:
```

New text:

```
    if not places:
        titles = frozenset(one.place.title for one in playlists)
    if not places:
```

### `u230.M1_no_lift`

decide genre: never lift the queuing playlist's base, so sitting 86's shape reads no edit

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u230.json`, row `M1_no_lift`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_mirror_edits_u230.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_edits_u230.py`, `tests/test_mirror_downloads_queued_from_u230.py`, `tests/test_mirror_downloads_filed_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 225 against a baseline of 225
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
        lifted = _as_queued(track, playlists, filed, queued)
```

New text:

```
        lifted = frozenset()
```

### `u227.R5_landed_flag`

decide genre: carry the landed edit without its landed flag on the plan

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u227.json`, row `R5_landed_flag`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u227.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u227.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`
- Collected: 196 against a baseline of 196
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u227.py::test_a_folder_edit_for_a_landed_track_takes_the_folder_over_the_landings_band`
  - `tests/test_mirror_edits_u227.py::test_a_landings_own_filing_does_not_beat_the_edit_that_queued_it`

Old text:

```
                extra = {"landed": True}
```

New text:

```
                extra = {}
```

### `u236.M17_ledger_settle_keeps_placement`

ledger settle: a settled track keeps its placement on that title

- File: `src/cratekit/modules/outbound/ledger.py`
- Source: `u236.json`, row `M17_ledger_settle_keeps_placement`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_put_in_another_month_on_the_account_leaves_the_placed_month`
  - `tests/test_organize_mirror_edits_u236.py::test_a_favourite_taken_off_again_before_another_organize_is_unfavourited`
  - `tests/test_organize_mirror_edits_u236.py::test_the_placements_are_read_as_the_gate_read_them_after_a_write_between_the_acts`

Old text:

```
                if str(track) in before:
                    _place(record, name, {one: at for one, at in before.items() if one != str(track)})
                    wrote = True
```

New text:

```
                if False:
                    _place(record, name, {one: at for one, at in before.items() if one != str(track)})
                    wrote = True
```

### `u236.M13_write_records_no_month`

write: record no month placement, so settle records none

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u236.json`, row `M13_write_records_no_month`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
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
        if at:
            done.months.append((one.content_id, one.month, at))
```

New text:

```
        if False:
            done.months.append((one.content_id, one.month, at))
```

### `u236.M9_placed_after_ignores_hold`

placed_after: drop a held placement the account holds

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M9_placed_after_ignores_hold`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 2 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_placement_is_dropped_once_the_account_holds_its_track_with_no_hold`
  - `tests/test_mirror_edits_u236.py::test_the_ledger_keeps_a_placement_until_the_mirror_finished_its_playlist`

Old text:

```
    return {track: at for track, at in placed.items() if track in kept or track not in now}
```

New text:

```
    return {track: at for track, at in placed.items() if track not in now}
```

### `u236.M4_moved_counts_to`

decide favorites: count the month the account asked for as rekordbox's move (round one, finding 5)

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u236.json`, row `M4_moved_counts_to`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_mirror_edits_u236.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits_u236.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_frozen_u222.py`, `tests/test_inbox_unmirrored.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits_u236.py::test_a_favourite_both_sides_put_in_another_month_leaves_the_placed_one`

Old text:

```
                moved = there_m - was_m - ours - {to}
```

New text:

```
                moved = there_m - was_m - ours
```

### `u201-composites.C2_agrees_never`

_agrees: a MOVE never agrees with rekordbox, the thing E5's exactness narrows

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201-composites.json`, row `C2_agrees_never`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_both_sides_moving_a_track_to_one_place_agree`

Old text:

```
        return now == frozenset({to})
```

New text:

```
        return False
```

### `u201.E10_unknown_time`

_later: a time unknown lets the account's move win

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201.json`, row `E10_unknown_time`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 4 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00+00:00-]`
  - `tests/test_mirror_edits.py::test_two_moves_with_a_time_unknown_keep_rekordboxs_and_say_so[2026-11-04T12:00:00-2026-11-04 10:00:00.000 +00:00]`
  - `tests/test_organize_mirror_edits.py::test_two_moves_with_the_account_time_unknown_keep_rekordboxs`

Old text:

```
    if account_at is None or rekordbox_at is None:
```

New text:

```
    if False:
```

### `u201-composites.C1_two_bands_composite`

E2 with the guard after it: neither the two bands guard nor the still in two bands guard, so a track added to two bands at once is moved to one

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u201-composites.json`, row `C1_two_bands_composite`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 195 against a baseline of 195
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_a_track_added_to_two_bands_at_once_is_held_on_both_sides`

Old text:

```
    if len(added) > 1:
        return (
            HELD,
            None,
            f"added on the account to {len(added)} band playlists at once "
            f"({', '.join(_titles(added))}), so which one it belongs in is not "
            f"something the account says",
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {', '.join(_titles(removed))} on the account, left in {place.title}"
    if removed and len(now) > 1:
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and still in "
            f"{len(now)} band playlists there, so which one it belongs in is not "
            f"something the account says",
        )

```

New text:

```
    if False:
        return (
            HELD,
            None,
            f"added on the account to {len(added)} band playlists at once "
            f"({', '.join(_titles(added))}), so which one it belongs in is not "
            f"something the account says",
        )
    if removed and len(now) == 1:
        (place,) = now
        return MOVE, place, f"taken off {', '.join(_titles(removed))} on the account, left in {place.title}"
    if False:
        return (
            HELD,
            None,
            f"taken off {', '.join(_titles(removed))} on the account and still in "
            f"{len(now)} band playlists there, so which one it belongs in is not "
            f"something the account says",
        )

```

### `u204.P10_inbox_agreed`

_decide_inbox: a change both sides made to a batch is carried again rather than agreed

- File: `src/cratekit/modules/outbound/mirror_edits.py`
- Source: `u204.json`, row `P10_inbox_agreed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_mirror_edits.py::test_an_inbox_change_both_sides_made_is_agreed`

Old text:

```
            if (track in one.rekordbox) is added:
```

New text:

```
            if False:
```

### `u204.O2_unfavourite_leaves_months`

_plan_favourites: an unfavourite leaves All Favorites alone and stays in its months

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O2_unfavourite_leaves_months`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_removed_from_all_favorites_leaves_the_favorites_folder`

Old text:

```
            leave += [(pid, folder, name) for name, pid in filing if pid in held]
```

New text:

```
            leave += []
```

### `u204.O3_quarter_refused`

_plan_favourites: a favourite put in a quarter is filed into it

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O3_quarter_refused`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_track_put_in_a_quarter_is_named_and_not_filed`

Old text:

```
            if placeholders.MONTH_LABEL.fullmatch(month) is None and month != placeholders.UNDATED:
```

New text:

```
            if False:
```

### `u204.O7_restore_detected`

write: a favourites only write detects no out of band restore

- File: `src/cratekit/organize/mirror_edits.py`
- Source: `u204.json`, row `O7_restore_detected`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_mirror_edits.py`, `tests/test_organize_mirror_edits.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 233 against a baseline of 233
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_a_favourites_only_write_detects_an_out_of_band_restore_and_asks_no_tree_latch`

Old text:

```
    if touched and not touched & {edits.GENRE, edits.INBOX}:
```

New text:

```
    if False:
```

### `u112.A4_in_folder_listed`

An account playlist already in the author's own folder is listed as not organized

- File: `src/cratekit/organize/account.py`
- Source: `u112.json`, row `A4_in_folder_listed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_of_yours_already_in_a_folder_of_yours_is_not_listed`

Old text:

```
            or one.playlist_id in in_folders

```

New text:

```
(empty)
```

### `u116.M10_year_check`

year_of_mark: a stamp that is not a date is accepted as a year

- File: `src/cratekit/organize/filing.py`
- Source: `u116.json`, row `M10_year_check`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 22933 against a baseline of 22933
- Kills: 1 (killed)
- Promoted: subset killed 0, full suite killed 1
- Killed:
  - `tests/test_playlist_kinds.py::test_a_playlist_whose_mark_has_no_year_is_filed_in_mine`

Old text:

```
    except ValueError:
        return ""
```

New text:

```
    except ValueError:
        return "2026"
```

### `u137.S2_only_fact`

Stop naming the selection in the area's facts

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S2_only_fact`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`

Old text:

```
            self.facts[ONLY_FACT] = ", ".join(self.only)
```

New text:

```
            pass
```

### `u142.S17_proof_not_named`

organize set step: name the set alone as the proof, so the gate does not say an INSPIRATION playlist proved it

- File: `src/cratekit/organize/account.py`
- Source: `u142.json`, row `S17_proof_not_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_a_set_with_no_intake_file_and_an_inspiration_playlist_of_its_name_is_archived`

Old text:

```
            proof = f"the INSPIRATION playlist {name}"
```

New text:

```
            proof = name
```

### `u112.R1_no_ack_planned`

With no backup acknowledgment the database area is planned and asked anyway

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R1_no_ack_planned`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 6 (killed)
- Killed:
  - `tests/test_organize.py::test_a_playlist_marked_twice_is_filed_by_its_latest_mark`
  - `tests/test_organize.py::test_a_year_folder_already_on_the_account_is_adopted_with_no_set_to_make_it`
  - `tests/test_organize.py::test_an_answer_ahead_of_a_gate_the_continue_may_not_reach_promises_no_stop_there`
  - `tests/test_organize.py::test_only_files_digest_is_not_the_full_areas_and_an_answer_over_one_is_stale_for_the_other`
  - `tests/test_organize.py::test_the_plan_is_empty_and_still_asks_when_the_root_is_clean`
  - `tests/test_organize.py::test_with_no_acknowledgment_the_verb_refuses_before_the_gate`

Old text:

```
        if not report:
            area.cause = unacknowledged.cause
            return area
```

New text:

```
        if False:
            area.cause = unacknowledged.cause
            return area
```

### `u137.S3_wants_everything`

Let every kind through whatever the selection

- File: `src/cratekit/organize/steps.py`
- Source: `u137.json`, row `S3_wants_everything`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 13 (killed)
- Killed:
  - `tests/test_organize.py::test_a_mixed_selection_plans_the_named_kinds_on_each_side_and_no_other`
  - `tests/test_organize.py::test_an_unread_label_registry_refuses_the_filing_rather_than_plan_it_over_no_label`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[file-called3]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[labels-called0]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[marks-called2]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[root-called4]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[sets-called1]`
  - `tests/test_organize.py::test_each_account_kind_runs_its_own_builder_and_no_other[yours-called5]`
  - `tests/test_organize.py::test_only_a_database_kind_asks_the_database_alone`
  - `tests/test_organize.py::test_only_file_plans_the_filing_alone_and_the_database_is_not_asked`
  - `tests/test_organize.py::test_only_mirror_plans_and_writes_the_mirror_alone_and_a_rerun_plans_nothing`
  - `tests/test_organize.py::test_only_yours_lists_on_each_side_exactly_what_the_full_verb_lists`
  - `tests/test_organize.py::test_only_yours_shows_a_refused_rotation_since_it_is_why_the_listing_is_short`

Old text:

```
        return self.only is None or kind in self.only
```

New text:

```
        return True
```

### `u112.C6_failure_never_raised`

An approved step that failed is never raised, so the run reads as a clean organize

- File: `src/cratekit/organize/cli.py`
- Source: `u112.json`, row `C6_failure_never_raised`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize.py::test_a_provider_cratekit_refusal_mid_pass_carries_the_moved_list`
  - `tests/test_organize.py::test_a_provider_refusal_mid_pass_stops_and_names_what_moved`
  - `tests/test_organize.py::test_a_step_that_fails_unexpectedly_lets_the_rest_run_and_is_raised_after`

Old text:

```
    if not failed:
        return
    wrote = [
```

New text:

```
    if True:
        return
    wrote = [
```

### `u112.R5_actor_invented`

The adoption job's approving actor is the process rather than the person who answered

- File: `src/cratekit/organize/rekordbox.py`
- Source: `u112.json`, row `R5_actor_invented`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize.py`
- Collected: 100 against a baseline of 100
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize.py::test_the_adoption_job_carries_a_run_its_own_resume_can_answer`

Old text:

```
                    apply_cli.ACTOR_KEY: decision.actor if decision is not None else "",
```

New text:

```
                    apply_cli.ACTOR_KEY: "cli",
```

### `u246.S5_inspiration_held_empty`

assert_read_back (inspiration): an empty set of live rows, so every planned row reads as missing and the write refuses

- File: `src/cratekit/organize/inspiration.py`
- Source: `u246.json`, row `S5_inspiration_held_empty`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`, `tests/test_u242_taken.py`, `tests/test_write_session.py`, `tests/test_organize.py`
- Collected: 333 against a baseline of 333
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

### `r1295.M8_none_read_withheld_dropped`

_none_read: say nothing of the tracks the provider withheld

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M8_none_read_withheld_dropped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
    if listing.withheld:
        said +=
```

New text:

```
    if False:
        said +=
```

### `u144-c.C4_missed_coefficient`

Counts: leave the withheld tracks out of the tracks missed

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C4_missed_coefficient`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_short_listing_counts_what_the_provider_withheld`

Old text:

```
            "tracks missed": sum(len(row.misses) + row.withheld for row in self.creates),
```

New text:

```
            "tracks missed": sum(len(row.misses) for row in self.creates),
```

### `r1295.M6_none_read_uncapped`

_none_read: name every unread track rather than the first five

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M6_none_read_uncapped`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
listing.unread[:NAMED_UNREAD])
```

New text:

```
listing.unread)
```

### `u144-c.C1_again_now_held`

B3 measured again after the stale test was tightened: a set given its INSPIRATION playlist since the plan is decided as before, not skipped

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C1_again_now_held`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_given_its_inspiration_playlist_since_the_plan_is_stale`

Old text:

```
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if now
```

New text:

```
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if False
```

### `r1295.M7_none_read_rest_uncounted`

_none_read: say nothing of the unread tracks past the fifth

- File: `src/cratekit/organize/inspiration.py`
- Source: `r1295.json`, row `M7_none_read_rest_uncounted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_set_no_track_of_which_reads_names_five_counts_the_rest_and_the_withheld`

Old text:

```
    if rest > 0:
```

New text:

```
    if False:
```

### `u144-c.C2_folder_unread`

Account sets: let a folder listing refusal refuse the whole step instead of one folder

- File: `src/cratekit/organize/inspiration.py`
- Source: `u144-c.json`, row `C2_folder_unread`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_inspiration.py`
- Collected: 39 against a baseline of 39
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_inspiration.py::test_a_sets_folder_that_cannot_be_listed_is_named_and_the_rest_still_plan`

Old text:

```
            listed = remote.folder_playlists(folder_id)
        except CratekitError as exc:
```

New text:

```
            listed = remote.folder_playlists(folder_id)
        except ZeroDivisionError as exc:
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

### `u147-b.M2_stale_folder_again`

Batch a's zero, measured again after its test: reuse a recorded folder whether or not the root still lists it

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u147-b.json`, row `M2_stale_folder_again`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror.py`
- Collected: 35 against a baseline of 35
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror.py::test_a_recorded_folder_deleted_on_the_account_is_made_again_rather_than_reused`

Old text:

```
    if held_id and held_id in root:
```

New text:

```
    if held_id:
```

### `r1289.M16_mirror_why`

mirror_downloads.plan: the unread track's why reworded so it does not carry the reader's words

- File: `src/cratekit/organize/mirror_downloads.py`
- Source: `r1289.json`, row `M16_mirror_why`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 105 against a baseline of 105
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_edits_u204.py::test_an_untitled_track_on_a_mirrored_playlist_is_named_and_the_others_queue`

Old text:

```
                            f"added on the account, but {unread[track].why}, so the "
```

New text:

```
                            f"added on the account, but it could not be read, so the "
```

### `r1031.M16_report_records`

add_steps: record and freeze on a run that does not ask its gate

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M16_report_records`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 173 against a baseline of 173
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize.py::test_a_library_write_between_the_mirrors_two_acts_applies_the_approved_plan`
  - `tests/test_organize_mirror_frozen.py::test_a_report_records_no_link_no_miss_and_freezes_nothing`

Old text:

```
    elif run is not None and run.record:
```

New text:

```
    elif run is not None:
```

### `r1031.M19_unfreezable_plan_refuses`

_record: let a frozen plan that cannot be written escape the plan instead of saying so

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M19_unfreezable_plan_refuses`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_a_plan_that_cannot_be_frozen_stands_and_the_apply_plans_afresh`

Old text:

```
    except OSError as exc:
        return f"{said}not frozen ({exc}), so the apply plans again"
```

New text:

```
    except ValueError as exc:
        return f"{said}not frozen ({exc}), so the apply plans again"
```

### `r1031.M20_signature_constant`

file_signature: answer one value for every readable file, so a rewritten file looks unchanged

- File: `src/cratekit/organize/account_mirror.py`
- Source: `r1031.json`, row `M20_signature_constant`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror.py`
- Collected: 73 against a baseline of 73
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen.py::test_the_file_signature_moves_when_the_file_is_rewritten`

Old text:

```
        return f"{held.st_size}:{held.st_mtime_ns}"
```

New text:

```
        return "1:1"
```

### `u222.M19_stale_on_every_run`

add_steps: carry stale lines on a gate's own run too

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u222.json`, row `M19_stale_on_every_run`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 259 against a baseline of 259
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_the_gate_run_and_a_report_say_nothing_stale`

Old text:

```
    if run is not None and run.decided:
        area.stale.extend
```

New text:

```
    if run is not None:
        area.stale.extend
```

### `u222.M8_agreed_list_check`

_agreed_of: accept a snapshot that is not a list of text

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M8_agreed_list_check`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 259 against a baseline of 259
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_an_older_record_or_an_unreadable_snapshot_or_step_is_planned_afresh`

Old text:

```
            if agreed is not None and (
```

New text:

```
            if False and (
```

### `u222.M16_lines_inverted`

moved: name the lines that did NOT move

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222.json`, row `M16_lines_inverted`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 259 against a baseline of 259
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize.py::test_an_account_change_between_the_mirrors_acts_is_stale_and_says_what_moved`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_label_step_that_moved_is_named_by_its_folder_line`
  - `tests/test_organize_mirror_frozen_u222.py::test_a_step_new_since_the_gate_and_one_gone_are_named`
  - `tests/test_organize_mirror_frozen_u222.py::test_an_account_change_between_the_acts_is_stale_and_names_its_folder_and_playlist`

Old text:

```
                if lines.get(label) != then.lines.get(label)
```

New text:

```
                if lines.get(label) == then.lines.get(label)
```

### `u222-zeros.M5_agreed_none_lost`

_agreed_json: freeze a never agreed snapshot as an empty one

- File: `src/cratekit/organize/mirror_frozen.py`
- Source: `u222-zeros.json`, row `M5_agreed_none_lost`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_frozen_u222.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize.py`, `tests/test_inbox_unmirrored.py`, `tests/test_organize_mirror_edits_u204.py`, `tests/test_organize_mirror_edits.py`
- Collected: 259 against a baseline of 259
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_frozen_u222.py::test_a_never_agreed_snapshot_is_frozen_and_read_back_as_never_agreed`

Old text:

```
            title: [one.remote_id, None if one.agreed is None else sorted(one.agreed)]
```

New text:

```
            title: [one.remote_id, sorted(one.agreed or ())]
```

### `u150.A5_deletes_named`

account_mirror.add_steps: name no playlist removal on the gate's deletes, so the gate says nothing is removed over one

- File: `src/cratekit/organize/account_mirror.py`
- Source: `u150.json`, row `A5_deletes_named`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize.py`
- Collected: 167 against a baseline of 167
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_the_rotation_moved_into_old_plans_the_removal_of_its_playlist_and_nothing_else`

Old text:

```
                for name, remote_id in planned.retire
            )
```

New text:

```
                for name, remote_id in ()
            )
```

### `u150.M2_present_guard`

mirror.plan: drop the still present test, so a batch still under INBOX that only no longer reads as one is removed from the account

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M2_present_guard`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 105 against a baseline of 105
- Kills: 2 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_batch_still_under_inbox_that_no_longer_reads_as_one_is_left_not_removed`
  - `tests/test_organize_mirror_inbox.py::test_the_digest_covers_the_removal`

Old text:

```
        elif name in folder.present:
```

New text:

```
        elif False:
```

### `u150.M9_known_answers`

Matcher: ignore a row's recorded landing track, so a label batch is matched by ISRC and misses on a tie

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `u150.json`, row `M9_known_answers`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_inbox.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`
- Collected: 105 against a baseline of 105
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_mirror_inbox.py::test_a_live_batch_made_by_a_label_landing_plans_its_playlist_with_the_batchs_tracks`

Old text:

```
        own = self._known.get(row.content_id)
        if own:
```

New text:

```
        own = self._known.get(row.content_id)
        if False:
```

### `r1032.M1_mirror_never_asks_any_agreeing`

Matcher._match: ask the provider without any_agreeing, so the mirror refuses a tie as a heart does

- File: `src/cratekit/modules/outbound/mirror.py`
- Source: `r1032.json`, row `M1_mirror_never_asks_any_agreeing`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_mirror_tie.py`, `tests/test_organize_mirror.py`, `tests/test_organize_mirror_frozen.py`, `tests/test_organize_mirror_inbox.py`
- Collected: 110 against a baseline of 110
- Kills: 4 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_organize_mirror_tie.py::test_a_tie_remembered_as_a_miss_before_the_tie_was_broken_is_asked_again`
  - `tests/test_organize_mirror_tie.py::test_the_next_refresh_keeps_the_chosen_release_and_asks_the_provider_nothing`

Old text:

```
            any_agreeing=True,
```

New text:

```
            any_agreeing=False,
```

### `u143-a.R3_no_count`

Debris: drop the no listed count check that comes before any read

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R3_no_count`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_with_no_listed_count_is_left_before_any_read`

Old text:

```
    if not isinstance(declared, int) or isinstance(declared, bool):
```

New text:

```
    if False:
```

### `u143-a.R2_short_read`

Debris: drop the read short of the declared count check

- File: `src/cratekit/organize/root.py`
- Source: `u143-a.json`, row `R2_short_read`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_organize_root.py`
- Collected: 56 against a baseline of 56
- Kills: 1 (killed)
- Killed:
  - `tests/test_organize_root.py::test_a_debris_copy_whose_tracks_could_not_all_be_read_is_left`

Old text:

```
        if len(tracks) != declared:
```

New text:

```
        if False:
```

### `u255.M6_held_never_stores`

_held: open without holding, so the retry's fresh object is not kept and the next add opens again

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M6_held_never_stores`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`

Old text:

```
            self._opened[playlist_id] = held

```

New text:

```
(empty)
```

### `u255.M7_held_always_opens`

_held: ignore what is held and open every time

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M7_held_always_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 9 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
        held = self._opened.get(playlist_id)

```

New text:

```
        held = None

```

### `u255.M9_every_attempt_opens`

add_to_playlist attempt: open afresh for every add, today's four requests a track

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u255.json`, row `M9_every_attempt_opens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`, `tests/test_outbound_order.py`, `tests/test_adapter_listing.py`, `tests/modules/test_outbound.py`
- Collected: 330 against a baseline of 330
- Kills: 11 (killed)
- Killed:
  - `tests/test_outbound_add_requests.py::test_a_held_playlist_never_outlives_its_adapter`
  - `tests/test_outbound_add_requests.py::test_a_refused_add_drops_the_hold_so_the_next_track_opens_afresh`
  - `tests/test_outbound_add_requests.py::test_a_write_between_the_open_and_the_tracks_read_never_puts_the_add_before_it`
  - `tests/test_outbound_add_requests.py::test_an_add_answered_without_the_track_reads_the_playlist_back_and_refuses`
  - `tests/test_outbound_add_requests.py::test_an_add_refused_for_a_stale_tag_is_sent_once_more_on_a_fresh_open_and_lands`
  - `tests/test_outbound_add_requests.py::test_another_write_through_the_adapter_drops_the_hold`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[100]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[10]`
  - `tests/test_outbound_add_requests.py::test_k_adds_to_one_owned_playlist_make_k_plus_two_gets_and_k_posts[1]`
  - `tests/test_outbound_add_requests.py::test_the_retrys_open_has_a_retry_of_its_own`
  - `tests/test_outbound_add_requests.py::test_two_playlists_added_to_in_turn_each_keep_their_own_held_object`

Old text:

```
            playlist = self._opened.get(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
```

New text:

```
            playlist = self._playlist(playlist_id)
            if playlist is None:
                playlist = self._held(playlist_id)
```

### `u270.A1_failed_attempt_reopens`

add_tracks: keep the object after a failed attempt, so the retry sends its stale tag and is refused 412 (round one's finding)

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `u270.json`, row `A1_failed_attempt_reopens`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_add_requests.py`, `tests/test_outbound_tidal_account.py`
- Collected: 157 against a baseline of 157
- Kills: 2 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_is_retried_on_a_fresh_open_and_recorded`
  - `tests/test_outbound_export_batches.py::test_one_refused_read_after_a_landed_add_through_the_driver_finishes_the_job`

Old text:

```
                except Exception:
                    opened[0] = None
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
```

New text:

```
                except Exception:
                    raise

            for start in range(0, len(lacking), ADD_CHUNK):
```

### `u270.E3_second_row_of_one_track`

apply: report each row matched to one track as added, so the summary counts the track written twice

- File: `src/cratekit/modules/outbound/export.py`
- Source: `u270.json`, row `E3_second_row_of_one_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_export_batches.py`, `tests/test_outbound_workers.py`
- Collected: 147 against a baseline of 147
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_export_batches.py::test_two_rows_matched_to_one_track_send_it_once_and_record_both_rows`

Old text:

```
        if said == ADDED and remote in added:
```

New text:

```
        if False:
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

### `r1032.A6_first_listed_not_lowest`

_lowest: take the first the provider lists, so the choice moves with the listing order

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1032.json`, row `A6_first_listed_not_lowest`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`, `tests/test_organize_mirror_tie.py`
- Collected: 116 against a baseline of 116
- Kills: 7 (killed)
- Killed:
  - `tests/test_organize_mirror_tie.py::test_a_release_that_does_not_agree_is_never_the_one_taken`
  - `tests/test_organize_mirror_tie.py::test_a_tie_between_agreeing_releases_is_mirrored_as_one_and_recorded`
  - `tests/test_outbound_tidal_account.py::test_a_file_album_naming_two_of_three_takes_the_lower_of_those_two`
  - `tests/test_outbound_tidal_account.py::test_a_release_that_does_not_agree_is_never_taken`
  - `tests/test_outbound_tidal_account.py::test_a_tie_broken_by_any_agreeing_is_said_and_no_other_match_is`
  - `tests/test_outbound_tidal_account.py::test_a_tie_with_any_agreeing_takes_the_lowest_identifier_whatever_the_listing_order`
  - `tests/test_outbound_tidal_account.py::test_two_hearts_or_an_album_naming_two_is_a_broken_tie`

Old text:

```
    return min(remotes, key=lambda remote: (len(remote), remote))
```

New text:

```
    return remotes[0]
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

### `r356-a.A4_hearts_asked_of_every_track`

Rule two reads the hearts of every track the ISRC named instead of the agreeing ones, so a heart on the radio edit chooses for the plain record

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A4_hearts_asked_of_every_track`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_heart_on_a_release_the_row_does_not_name_decides_nothing`

Old text:

```
        hearted = [remote for remote in agreeing if remote in hearts]
```

New text:

```
        hearted = [remote for remote in verdicts if remote in hearts]
```

### `r834.M1_a_create_makes_the_playlist_private`

TidalAccount.create_playlist: drop the private step, so a created playlist keeps whatever visibility the provider defaults to, the defect R-834 named

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r834.json`, row `M1_a_create_makes_the_playlist_private`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_created_playlist_is_made_private_once`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_once_is_retried_once_and_lands`
  - `tests/test_outbound_tidal_account.py::test_a_private_step_refused_twice_still_hands_back_the_one_playlist`
  - `tests/test_outbound_tidal_account.py::test_a_second_export_finds_its_playlist_and_neither_creates_nor_sets_visibility`

Old text:

```
        self._make_private(created, identifier)

```

New text:

```
(empty)
```

### `r356-a.A9_row_may_name_an_artist_nobody_bills`

A row billing a third act the track does not agrees

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r356-a.json`, row `A9_row_may_name_an_artist_nobody_bills`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_row_billing_two_artists_agrees_with_a_track_billing_the_same_two`

Old text:

```
    return bool(first) and first <= ours and ours - billed <= _JOINERS
```

New text:

```
    return bool(first) and first <= ours
```

### `u97-c.C1_outbound_refusal_removed`

composite for B4: remove the outbound account's missing session refusal entirely, so the seam opens a client with no credential. Shows what the guard holds when its remedy holds nothing

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u97-c.json`, row `C1_outbound_refusal_removed`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_session_removed_after_an_open_is_refused_rather_than_reused`

Old text:

```
    if not secrets.exists(str(secrets.Credential.PROVIDER_SESSION)):
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
```

New text:

```
    if False:
        raise refuse(
            "credential-missing",
            "no streaming provider session is stored, so there is no account "
            "to write this playlist or these hearts to",
```

### `r358.A1_empty_title_refusal`

Drop the empty-title refusal, so a blank title reaches the client

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r358.json`, row `A1_empty_title_refusal`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_tidal_account.py`
- Collected: 111 against a baseline of 111
- Kills: 3 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[   ]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[\n]`
  - `tests/test_outbound_tidal_account.py::test_a_rename_with_no_title_is_refused_before_the_client_sees_it[]`

Old text:

```
        if not wanted.strip():
            # NOT ``provider_failure``. The provider did not fail, and its
            # remedy is "resume the job to retry this item", which is advice
            # that cannot work: the same empty title fails the same way.
            raise refuse(
                "internal-error",
                f"a rename of the playlist {playlist_id} was asked for with no "
                f"title; the client reads a falsy title as keep the current one "
                f"and answers that it succeeded, so nothing was sent",
                scope=Scope.SOURCE,
                origin=("outbound", "account"),
                detail={"playlist_id": str(playlist_id)},
            )

```

New text:

```
(empty)
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

### `r850-a.E6_no_match_sentence`

export._left_out: leave the reason empty when the account said nothing, so the row is listed with no reason

- File: `src/cratekit/export/cli.py`
- Source: `r850-a.json`, row `E6_no_match_sentence`
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
        "reason": _said(row) or NO_MATCH,
```

New text:

```
        "reason": _said(row),
```

### `u131.K12_filing_as_shown`

kinds.file_new: file whatever the account says now rather than only the decision the gate showed

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K12_filing_as_shown`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_playlist_kinds.py`
- Collected: 139 against a baseline of 139
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`

Old text:

```
    if token(folder) != planned:
```

New text:

```
    if False:
```

### `u51-item-derivation.S5_payload_shape`

Put the outbound summary back at the top level, off the declared schema

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `u51-item-derivation.json`, row `S5_payload_shape`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`, `tests/test_queued_resume_contract.py`
- Collected: 145 against a baseline of 145
- Kills: 65 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_cancelled_job_does_not_report_a_clean_resume`
  - `tests/test_outbound_workers.py::test_a_confirmed_adoption_does_not_authorise_a_create`
  - `tests/test_outbound_workers.py::test_a_crate_dragged_into_a_folder_updates_its_remote_playlist`
  - `tests/test_outbound_workers.py::test_a_crate_the_export_still_carries_is_never_adopted_from`
  - `tests/test_outbound_workers.py::test_a_created_playlist_is_filed_in_exports_as_its_gate_showed`
  - `tests/test_outbound_workers.py::test_a_dangling_track_is_named_in_the_queued_envelope`
  - `tests/test_outbound_workers.py::test_a_failed_favourite_leaves_the_sweep_resumable`
  - `tests/test_outbound_workers.py::test_a_failed_item_leaves_the_job_resumable_and_the_resume_redoes_only_it`
  - `tests/test_outbound_workers.py::test_a_favourite_whose_isrc_names_several_tracks_is_listed_with_that_reason`
  - `tests/test_outbound_workers.py::test_a_favourites_sweep_runs_to_done_and_hearts_every_matched_row`
  - `tests/test_outbound_workers.py::test_a_filing_failure_is_a_warning_on_a_finished_export`
  - `tests/test_outbound_workers.py::test_a_folder_changed_after_the_queue_leaves_the_playlist_at_the_root_with_a_warning`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_fresh_export_shows_its_date_and_warns_of_nothing[sync.favorites]`
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`
  - ... and 50 more, see the JSON sidecar

Old text:

```
        "progress": {
            **jobs.progress(store, job.job_id),
            "outbound": dict(summary(cfg, job.job_id)),
        },
```

New text:

```
        "progress": jobs.progress(store, job.job_id),
        "outbound": dict(summary(cfg, job.job_id)),
```

### `r229.C3_no_remote_id_is_frozen`

The job freezes no remote id, so nothing can follow a record that moves after the job is confirmed

- File: `src/cratekit/export/cli.py`
- Source: `r229.json`, row `C3_no_remote_id_is_frozen`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 125 against a baseline of 125
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_half_driven_job_resumed_after_its_crate_moved_creates_nothing`

Old text:

```
                REMOTE: found.own_remote_id or found.remote_id or None,
```

New text:

```
                REMOTE: None,
```

### `r227.S1_unknown_is_within_limit`

An age that could not be read is called within the limit

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S1_unknown_is_within_limit`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 125 against a baseline of 125
- Kills: 1 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_an_age_that_cannot_be_read_is_unknown_rather_than_fresh`

Old text:

```
    if not age.known:
        return AGE_UNKNOWN
```

New text:

```
    if not age.known:
        return AGE_WITHIN_LIMIT
```

### `r227.S2_no_sentence_at_the_gate`

The shown block carries no warning sentence, so the advice arrives only after the answer

- File: `src/cratekit/modules/outbound/shell.py`
- Source: `r227.json`, row `S2_no_sentence_at_the_gate`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_outbound_workers.py`
- Collected: 125 against a baseline of 125
- Kills: 5 (killed)
- Killed:
  - `tests/test_outbound_workers.py::test_a_date_well_in_the_future_is_not_the_freshest_export_there_could_be`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[export.playlist]`
  - `tests/test_outbound_workers.py::test_a_month_old_export_is_called_old_in_the_plan_the_gate_shows[sync.favorites]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[export.playlist]`
  - `tests/test_outbound_workers.py::test_the_date_reaches_a_person_who_is_not_reading_json[sync.favorites]`

Old text:

```
        export["warning"] = warning["message"]
```

New text:

```
        pass
```

### `u131.K10_kind_created_named`

kinds.reserve: do not name a kind folder created before a failed ledger write

- File: `src/cratekit/modules/outbound/kinds.py`
- Source: `u131.json`, row `K10_kind_created_named`
- Surface: maintainer
- Subset: explicit subset from the row
- Ran: `tests/test_playlist_kinds.py`, `tests/test_organize.py`
- Collected: 114 against a baseline of 114
- Kills: 1 (killed)
- Killed:
  - `tests/test_playlist_kinds.py::test_each_kind_lands_in_its_own_folder`

Old text:

```
        if made is not None:
            made.append(folder.kind)
```

New text:

```
        pass
```

### `r1313.T1_account_skips_the_classifier`

tidal_account._not_found: read the class names alone and stop asking classify_unavailable, so a 404 the account reads by status is retried

- File: `src/cratekit/modules/outbound/tidal_account.py`
- Source: `r1313.json`, row `T1_account_skips_the_classifier`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_not_found_bodies.py`, `tests/test_isrc_cache.py`, `tests/test_outbound_tidal_account.py`
- Collected: 227 against a baseline of 227
- Kills: 5 (killed)
- Killed:
  - `tests/test_isrc_cache.py::test_a_404_status_is_kept_as_a_not_found_at_either_seam[account]`
  - `tests/test_provider_not_found_bodies.py::test_a_404_is_a_not_found_whatever_its_body[404-html-account]`
  - `tests/test_provider_not_found_bodies.py::test_a_rewrapped_404_page_is_a_not_found[account]`
  - `tests/test_provider_not_found_bodies.py::test_an_isrc_answered_by_a_404_page_is_asked_once_and_kept[account]`
  - `tests/test_provider_not_found_bodies.py::test_off_the_declared_chain_a_links_cause_is_nearer_than_what_it_was_handling`

Old text:

```
    return classify_unavailable(exc) is TrackOutcome.UNAVAILABLE_PERMANENT

```

New text:

```
    return False

```

### `u261.A1_account_forget_keeps_the_session`

account.forget: drop the adapter and keep the shared session, so a 401 on the account leaves the catalogue the refused client

- File: `src/cratekit/modules/outbound/account.py`
- Source: `u261.json`, row `A1_account_forget_keeps_the_session`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_provider_session_hold.py`, `tests/test_outbound_tidal_account.py`
- Collected: 141 against a baseline of 141
- Kills: 25 (killed)
- Killed:
  - `tests/test_outbound_tidal_account.py::test_a_hearts_sweep_runs_to_done_and_the_ledger_records_every_heart`
  - `tests/test_outbound_tidal_account.py::test_a_login_that_fails_names_whether_to_log_in_again_or_wait[rejected]`
  - `tests/test_outbound_tidal_account.py::test_a_playlist_export_runs_to_done_and_the_ledger_records_every_add`
  - `tests/test_outbound_tidal_account.py::test_a_provider_failure_on_one_heart_fails_that_item_and_no_other`
  - `tests/test_outbound_tidal_account.py::test_a_release_the_account_already_hearts_is_the_one_an_export_adds`
  - `tests/test_outbound_tidal_account.py::test_a_second_export_finds_its_playlist_and_neither_creates_nor_sets_visibility`
  - `tests/test_outbound_tidal_account.py::test_a_sweep_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_export_resolves_a_shared_isrc_by_the_rows_own_names_and_says_why_it_could_not`
  - `tests/test_outbound_tidal_account.py::test_an_unmatched_row_with_nothing_said_about_it_adds_no_reason_to_the_envelope`
  - `tests/test_outbound_tidal_account.py::test_one_process_logs_in_once_however_many_items_resolve`
  - `tests/test_provider_session_hold.py::test_a_login_that_failed_holds_nothing_and_is_asked_again[rejected]`
  - `tests/test_provider_session_hold.py::test_a_login_that_failed_holds_nothing_and_is_asked_again[unreachable]`
  - `tests/test_provider_session_hold.py::test_a_lost_app_value_is_noted_on_every_resolve_that_falls_back`
  - `tests/test_provider_session_hold.py::test_a_refreshed_login_is_reused_while_the_keychain_holds_the_refresh`
  - `tests/test_provider_session_hold.py::test_a_refusal_answered_through_the_shared_client_drops_it_for_both_seams[401]`
  - ... and 10 more, see the JSON sidecar

Old text:

```
    _OPENED_OVER = None
    provider_session.forget()
```

New text:

```
    _OPENED_OVER = None
```

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

### `u174.O4_no_pass_is_no_step`

_mark_step: a pass that is no sync pass's is planned as a step with nothing to mark

- File: `src/cratekit/organize/account.py`
- Source: `u174.json`, row `O4_no_pass_is_no_step`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_mark.py`, `tests/test_organize.py`
- Collected: 169 against a baseline of 169
- Kills: 1 (killed)
- Killed:
  - `tests/test_sync_mark.py::test_a_native_landing_of_no_sync_pass_is_counted_and_is_no_step`

Old text:

```
    if not planned.of_a_pass:
        return False
```

New text:

```
    if False:
        return False
```

### `u216.M24_read_unvalidated`

_folders: what a folder held is read without checking it is playlist ids

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u216.json`, row `M24_read_unvalidated`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair.py`, `tests/test_sync_pair_account.py`, `tests/test_sync_pair_adopted.py`, `tests/test_sync_pair_back.py`, `tests/test_sync_pair_calls.py`, `tests/test_sync_pair_discover.py`, `tests/test_sync_pair_hold.py`, `tests/test_sync_pair_hold_every.py`, `tests/test_sync_pair_merge.py`, `tests/test_sync_pair_resume.py`, `tests/test_sync_pair_resume_one.py`, `tests/test_sync_pair_tie.py`
- Collected: 383 against a baseline of 383
- Kills: 4 (killed)
- Killed:
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[a]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held1]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held2]`
  - `tests/test_sync_pair_adopted.py::test_a_folder_whose_held_is_not_ids_refuses_the_document[held3]`

Old text:

```
            if held is not None and (
                not isinstance(held, list) or not all(isinstance(one, str) and one for one in held)
            ):
```

New text:

```
            if False:
```

### `u198.P2_release_side`

pairs.release: the survivor is recorded on the wrong side

- File: `src/cratekit/modules/outbound/pairs.py`
- Source: `u198.json`, row `P2_release_side`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_sync_pair_discover.py`, `tests/test_sync_pair.py`, `tests/test_sync_twins.py`
- Collected: 166 against a baseline of 166
- Kills: 3 (killed)
- Killed:
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_in_rekordbox_unpairs_and_leaves_the_account_playlist`
  - `tests/test_sync_pair_discover.py::test_a_playlist_deleted_on_the_account_unpairs_stays_and_is_not_made_again`
  - `tests/test_sync_pair_discover.py::test_a_write_of_the_pairs_alone_keeps_the_folders_misses_and_released`

Old text:

```
            if side == ACCOUNT_SIDE:
```

New text:

```
            if side != ACCOUNT_SIDE:
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

### `u242.M23_filing_dates_a_found_prefix`

filing: read a taken entry the migration found as a dated mark, filing it by the migration's year

- File: `src/cratekit/organize/filing.py`
- Source: `u242.json`, row `M23_filing_dates_a_found_prefix`
- Surface: user
- Subset: explicit subset from the row
- Ran: `tests/test_u242_taken.py`, `tests/test_organize_root.py`, `tests/test_organize.py`
- Collected: 202 against a baseline of 202
- Kills: 3 (killed)
- Killed:
  - `tests/test_organize_root.py::test_filing_reads_a_stripped_hand_mark_as_it_read_the_prefixed_one`
  - `tests/test_u242_taken.py::test_filing_after_a_real_strip_reads_every_playlist_as_it_did_before`
  - `tests/test_u242_taken.py::test_filing_reads_a_found_prefix_as_undated_and_a_pass_mark_as_dated`

Old text:

```
        if entry.held and entry.dated:
```

New text:

```
        if entry.held:
```

